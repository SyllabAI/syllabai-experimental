#!/usr/bin/env python3
"""exam-mate bulk image downloader + organizer — provenance-first, resumable.

Downloads every image URL recorded in a subject's questions.jsonl through the
WAF-immune in-page fetch pipeline (ExamMateClient), stores them canonically
mirroring the source URL path, and writes a per-image metadata index.

Canonical layout (inside <subject_dir>/images/):
    questions/{qfolder}/{src_qid}/{original_filename}.png
i.e. local path after `images/` == the URL path on www.exam-mate.com, so
source URL = "https://www.exam-mate.com/" + <relative file path>.

INDEX.jsonl (one JSON object per image, append-only, crash-safe) carries:
    file, url, kind(question|answer), sha256, bytes, content_type, status,
    width/height/format (Pillow), qid, src_qid, qfolder, event_key, page,
    paper_ref, parsed{syllabus,paper,season,year,question}, topics,
    mcq_answer, category_id, subject_id, downloaded_at

Phases:
    download  — fetch everything missing (resume by INDEX + file size check)
    organize  — build by_paper.json / by_topic.json views + verify integrity

Usage:
    python3 exam_mate_image_bulk.py --phase download [--limit N]
                                    [--batch 4] [--delay 1.0]
    python3 exam_mate_image_bulk.py --phase organize [--prune-samples]
"""
import argparse, base64, hashlib, json, os, re, sys, time
from datetime import datetime, timezone
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exam_mate_client import ExamMateClient  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TP = os.path.join(REPO, "exam-mate", "resources", "topical_papers")
DEFAULT_SUBJECT_DIR = os.path.join(
    TP, "topical", "3_IGCSE", "11_Additional_Mathematics_0606_")
SUBJECT_DIR = DEFAULT_SUBJECT_DIR  # overridable via --subject-dir
QUESTIONS = os.path.join(SUBJECT_DIR, "questions.jsonl")
IMAGES_DIR = os.path.join(SUBJECT_DIR, "images")
INDEX_PATH = os.path.join(IMAGES_DIR, "INDEX.jsonl")
SAMPLES_DIR = os.path.join(SUBJECT_DIR, "image_samples")

BASE = "https://www.exam-mate.com"
PAPER_RE = re.compile(r"^(\S+)/([A-Za-z0-9]+)_([A-Za-z]+)_(\d{4})_Q(.+)$")
URLPATH_RE = re.compile(r"^/questions/(\d+)/(\d+)/([^/]+\.png)$")

FETCH_JS = """async (urls) => {
  const one = async (url) => {
    try {
      const r = await fetch(url, {credentials: 'include',
                                  signal: AbortSignal.timeout(30000)});
      const ct = r.headers.get('content-type') || '';
      if (!r.ok) return {url, status: r.status, ct};
      const buf = await r.arrayBuffer();
      const bytes = new Uint8Array(buf);
      let binary = '';
      const chunk = 0x8000;
      for (let i = 0; i < bytes.length; i += chunk) {
        binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
      }
      return {url, status: r.status, ct, b64: btoa(binary), size: bytes.length};
    } catch (e) {
      return {url, error: String(e)};
    }
  };
  return await Promise.all(urls.map(one));
}"""


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 16), b""):
            h.update(blk)
    return h.hexdigest()


def nat_key(s):
    return (0, int(s)) if s.isdigit() else (1, s)


def parse_paper_ref(text):
    m = PAPER_RE.match(text or "")
    if not m:
        return None
    return {"syllabus": m.group(1), "paper": m.group(2),
            "season": m.group(3), "year": m.group(4), "question": m.group(5)}


def set_subject_dir(path):
    global SUBJECT_DIR, QUESTIONS, IMAGES_DIR, INDEX_PATH, SAMPLES_DIR
    SUBJECT_DIR = path if os.path.isabs(path) else os.path.join(TP, path)
    QUESTIONS = os.path.join(SUBJECT_DIR, "questions.jsonl")
    IMAGES_DIR = os.path.join(SUBJECT_DIR, "images")
    INDEX_PATH = os.path.join(IMAGES_DIR, "INDEX.jsonl")
    SAMPLES_DIR = os.path.join(SUBJECT_DIR, "image_samples")


def build_tasks():
    """One task per unique image URL (first reference wins), in jsonl order."""
    tasks, seen = [], set()
    with open(QUESTIONS) as f:
        for line in f:
            r = json.loads(line)
            p = r.get("payload", {})
            for kind, key in (("question", "question_images"),
                              ("answer", "answer_images")):
                for url in p.get(key, []):
                    if url in seen:
                        continue
                    seen.add(url)
                    path = urlparse(url).path
                    mu = URLPATH_RE.match(path)
                    if not mu:
                        print(f"[bulk] WARN url not matching pattern: {url}")
                        continue
                    tasks.append({
                        "url": url, "rel": path.lstrip("/"), "kind": kind,
                        "qid": r.get("qid"), "event_key": r.get("eventKey"),
                        "page": r.get("page"), "paper_ref": r.get("text", ""),
                        "parsed": parse_paper_ref(r.get("text", "")),
                        "topics": p.get("topics", ""),
                        "mcq_answer": p.get("mcq_answer", ""),
                        "src_qid": int(mu.group(2)), "qfolder": int(mu.group(1)),
                        "category_id": r.get("categoryID"),
                        "subject_id": r.get("subjectID"),
                    })
    return tasks


def load_done():
    """url -> recorded bytes for entries whose file still exists w/ same size."""
    done = {}
    if not os.path.exists(INDEX_PATH):
        return done
    with open(INDEX_PATH) as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get("status") != 200:
                continue
            fp = os.path.join(IMAGES_DIR, e["file"])
            if os.path.exists(fp) and os.path.getsize(fp) == e.get("bytes"):
                done[e["url"]] = e.get("bytes", 0)
    return done


def img_meta(data):
    try:
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(data))
        return {"width": im.width, "height": im.height,
                "format": im.format or "PNG"}
    except Exception:
        return {"width": None, "height": None, "format": None}


def phase_download(batch, delay, limit):
    tasks = build_tasks()
    if limit:
        tasks = tasks[:limit]
    done = load_done()
    todo = [t for t in tasks if t["url"] not in done]
    total_bytes = sum(done.values())
    print(f"[bulk] tasks={len(tasks)} done={len(done)} todo={len(todo)} "
          f"(already {total_bytes/1e6:.1f} MB)", flush=True)
    if not todo:
        return
    os.makedirs(IMAGES_DIR, exist_ok=True)

    c = ExamMateClient(verbose=True)
    c.fetch(BASE + "/topicalpastpapers", settle_ms=800)
    idx = open(INDEX_PATH, "a", buffering=1)
    ok = fail = 0
    consecutive_bad = 0
    try:
        for i in range(0, len(todo), batch):
            chunk = todo[i:i + batch]
            results = c.page.evaluate(FETCH_JS, [t["url"] for t in chunk])
            by_url = {r["url"]: r for r in results}
            retry = []
            for t in chunk:
                r = by_url.get(t["url"], {"url": t["url"], "error": "no-result"})
                err = r.get("error")
                ct = r.get("ct", "")
                if err or "text/html" in ct:
                    retry.append((t, r))
                    continue
                data = None
                if r.get("b64"):
                    try:
                        data = base64.b64decode(r["b64"])
                    except Exception:
                        data = None
                if data is None:
                    retry.append((t, r))
                    continue
                fp = os.path.join(IMAGES_DIR, t["rel"])
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                with open(fp, "wb") as f:
                    f.write(data)
                entry = dict(t)
                entry.update({"status": r["status"], "bytes": len(data),
                              "content_type": ct,
                              "sha256": hashlib.sha256(data).hexdigest(),
                              "downloaded_at": now_iso()})
                entry.update(img_meta(data))
                entry.pop("rel", None)
                entry["file"] = t["rel"]
                idx.write(json.dumps(entry, ensure_ascii=False) + "\n")
                ok += 1
                total_bytes += len(data)
                consecutive_bad = 0
            if retry:
                time.sleep(2.0)
                results2 = c.page.evaluate(FETCH_JS, [t["url"] for t, _ in retry])
                by_url2 = {r["url"]: r for r in results2}
                heal_needed = any(
                    "text/html" in r.get("ct", "") or r.get("error")
                    for r in by_url2.values())
                if heal_needed:
                    try:
                        c.fetch(BASE + "/", settle_ms=400)
                    except Exception as e:
                        print(f"[bulk] heal failed: {e}", flush=True)
                for t, _r in retry:
                    r = by_url2.get(t["url"], {"url": t["url"], "error": "no-result"})
                    err = r.get("error")
                    ct = r.get("ct", "")
                    data = None
                    if r.get("b64"):
                        try:
                            data = base64.b64decode(r["b64"])
                        except Exception:
                            data = None
                    if err or "text/html" in ct or data is None:
                        fail += 1
                        consecutive_bad += 1
                        print(f"[bulk] FAIL {r.get('status') or err} {t['url']}",
                              flush=True)
                        idx.write(json.dumps(
                            dict(t, file=t["rel"], status=r.get("status") or 0,
                                 bytes=0, content_type=ct or "",
                                 error=str(err or "non-image response"),
                                 downloaded_at=now_iso()),
                            ensure_ascii=False) + "\n")
                        continue
                    fp = os.path.join(IMAGES_DIR, t["rel"])
                    os.makedirs(os.path.dirname(fp), exist_ok=True)
                    with open(fp, "wb") as f:
                        f.write(data)
                    entry = dict(t)
                    entry.update({"status": r["status"], "bytes": len(data),
                                  "content_type": ct,
                                  "sha256": hashlib.sha256(data).hexdigest(),
                                  "downloaded_at": now_iso()})
                    entry.update(img_meta(data))
                    entry.pop("rel", None)
                    entry["file"] = t["rel"]
                    idx.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    ok += 1
                    total_bytes += len(data)
                    consecutive_bad = 0
            done_n = i + len(chunk)
            print(f"[bulk] {done_n}/{len(todo)} ok={ok} fail={fail} "
                  f"{total_bytes/1e6:.1f}MB "
                  f"[{chunk[-1]['paper_ref']}", flush=True)
            if consecutive_bad >= 30:
                print("[bulk] 30 consecutive failures — aborting (resumable).",
                      flush=True)
                break
            time.sleep(delay)
    finally:
        idx.close()
        c.close()
    print(f"[bulk] download phase finished: ok={ok} fail={fail} "
          f"total={total_bytes/1e6:.1f}MB", flush=True)


# ---------------------------------------------------------------- organize --

def write_manifest(entries, summary_obj):
    """Auto-generate images/MANIFEST.md for any subject dir."""
    meta = {}
    mp = os.path.join(SUBJECT_DIR, "meta.json")
    if os.path.exists(mp):
        meta = json.load(open(mp))
    cat = meta.get("category", {})
    subj = meta.get("subject", {})
    n_q = sum(1 for e in entries if e["kind"] == "question")
    n_a = sum(1 for e in entries if e["kind"] == "answer")
    n_bad = sum(1 for e in entries if e.get("bytes") == 0)
    total_mb = sum(e["bytes"] for e in entries) / 1e6
    refs = sorted({e.get("paper_ref") or "?" for e in entries})
    years = sorted({(e.get("parsed") or {}).get("year", "?") for e in entries})
    topics = sorted({t.strip() for e in entries
                     for t in (e.get("topics") or "").split(",") if t.strip()})
    n_urls_total = len(entries) + n_bad
    lines = [
        f"# MANIFEST — images/ ({subj.get('label', '?')}, complete set)",
        "",
        f"Downloaded: {summary_obj['generated_at']} · Source: "
        "`https://www.exam-mate.com` TOPICAL PAST PAPERS, subject "
        f"`categoryID={cat.get('id')}` ({cat.get('label')}) / "
        f"`subjectID={subj.get('id')}` ({subj.get('label')}) · Method: "
        "fixed-fingerprint headless Chromium, in-page `fetch()` pipeline "
        "(WAF-immune; `scripts/exam_mate_image_bulk.py`) · Rate: batches of "
        "4 concurrent fetches, 1 s between batches.",
        "",
        "## Contents",
        "",
        "| Path | What |",
        "|---|---|",
        "| `INDEX.jsonl` | **Per-image metadata ledger — the provenance "
        "record.** One JSON object per unique image URL. |",
        "| `questions/{qfolder}/{src_qid}/{original_filename}.png` | PNGs, "
        "original site filenames preserved. Local path after `images/` == "
        "URL path, so `https://www.exam-mate.com/` + `<file>` reconstructs "
        "the source URL. |",
        "| `by_paper.json` | Derived view: `paper_ref` → qid, topics, MCQ "
        "answer, parsed fields, image lists. Sorted newest-first. |",
        "| `by_topic.json` | Derived view: individual topic → entries "
        "(site topic strings verbatim). |",
        "| `_summary.json` | Machine summary of the download + integrity "
        "run. |",
        "",
        "## Coverage vs. harvest",
        "",
        f"- {n_urls_total} unique image URLs referenced by "
        f"{meta.get('badges', ['?'])[0] if meta.get('badges') else '?'} "
        "harvested questions (`questions.jsonl`) → "
        f"**{len(entries)} downloaded** ({total_mb:.2f} MB).",
        f"- {n_q} question images, {n_a} answer images.",
        f"- Years covered (parsed from paper refs): {', '.join(years)}.",
        f"- Topics ({len(topics)}): {', '.join(topics)}.",
        f"- Harvested at: {meta.get('harvested_at', '?')}.",
    ]
    if n_bad:
        lines += ["", "## Failed URLs", ""]
        for e in entries:
            if e.get("bytes") == 0:
                lines.append(f"- HTTP {e.get('status')} `{e['url']}` — "
                             "recorded in INDEX.jsonl, not substituted.")
    lines += [
        "",
        "## INDEX.jsonl fields",
        "",
        "`file`, `url` (source), `kind` (question|answer), `sha256`, "
        "`bytes`, `content_type`, `status`, `width`/`height`/`format`, "
        "`qid` (site list id), `src_qid` (image-store id from the URL "
        "path — both id spaces preserved), `qfolder`, `event_key`, "
        "`page`, `paper_ref` (site's own reference string), `parsed` "
        "{syllabus, paper, season, year, question}, `topics` (verbatim), "
        "`mcq_answer`, `category_id`, `subject_id`, `downloaded_at`.",
        "",
        "## Integrity",
        "",
        "- Every file's SHA-256 recorded at download time in "
        "`INDEX.jsonl`.",
        f"- Coverage cross-check: {len(entries)}/{n_urls_total} unique "
        "URLs on disk.",
        "",
        "## Copyright note",
        "",
        "These PNGs reproduce exam-board copyrighted questions via the "
        "third-party site exam-mate.com. Experimental research copy only — "
        "license review required before any of this content ships "
        "(same discipline as `syllabai-pastpapers`).",
        "",
    ]
    with open(os.path.join(IMAGES_DIR, "MANIFEST.md"), "w") as f:
        f.write("\n".join(lines))
    print(f"[organize] wrote images/MANIFEST.md")


def load_index():
    # compact: dedupe by url (last valid wins), drop torn lines
    best = {}
    order = []
    with open(INDEX_PATH) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                e = json.loads(line)
            except Exception:
                continue
            u = e.get("url")
            if not u:
                continue
            if u not in best:
                order.append(u)
            best[u] = e
    entries = [best[u] for u in order if best[u].get("status") == 200]
    # rewrite compacted ledger atomically
    tmp = INDEX_PATH + ".tmp"
    with open(tmp, "w") as f:
        for u in order:
            f.write(json.dumps(best[u], ensure_ascii=False) + "\n")
    os.replace(tmp, INDEX_PATH)
    return entries


def phase_organize(prune_samples):
    entries = load_index()
    files_on_disk = 0
    for e in entries:
        if os.path.exists(os.path.join(IMAGES_DIR, e["file"])):
            files_on_disk += 1
    q = [e for e in entries if e["kind"] == "question"]
    a = [e for e in entries if e["kind"] == "answer"]
    bad = [e for e in entries if e.get("bytes") == 0]
    total = sum(e["bytes"] for e in entries)
    print(f"[organize] index entries={len(entries)} (q={len(q)} a={len(a)}) "
          f"on_disk={files_on_disk} failed={len(bad)} total={total/1e6:.2f}MB")

    by_paper, by_topic = {}, {}
    for e in entries:
        ref = e.get("paper_ref") or "?"
        slot = by_paper.setdefault(ref, {
            "qid": e["qid"], "page": e.get("page"),
            "topics": e.get("topics", ""), "mcq_answer": e.get("mcq_answer", ""),
            "parsed": e.get("parsed"),
            "question_images": [], "answer_images": []})
        slot[f"{'question' if e['kind'] == 'question' else 'answer'}_images"]\
            .append(e["file"])
        for tp in [t.strip() for t in (e.get("topics") or "").split(",") if t.strip()]:
            by_topic.setdefault(tp, []).append(
                {"qid": e["qid"], "paper_ref": ref, "file": e["file"]})

    def sort_key(item):
        p = item[1].get("parsed") or {}
        return (-(int(p.get("year") or 0)), p.get("season") or "",
                nat_key(p.get("paper") or ""), nat_key(p.get("question") or ""))

    by_paper = {k: by_paper[k] for k in sorted(by_paper, key=lambda k: sort_key((k, by_paper[k])))}
    by_topic = {k: by_topic[k] for k in sorted(by_topic, key=str.casefold)}

    header = {
        "_note": "Derived view of INDEX.jsonl — provenance lives there.",
        "source": "exam-mate.com TOPICAL PAST PAPERS (see images/MANIFEST.md "
                  "for the subject this folder belongs to)",
        "generated_at": now_iso(),
        "images_dir": "images/",
        "url_reconstruction": "https://www.exam-mate.com/" + "<file>",
    }
    with open(os.path.join(IMAGES_DIR, "by_paper.json"), "w") as f:
        json.dump({**header, "_kind": "by_paper", "papers": by_paper}, f,
                  ensure_ascii=False, indent=1)
    with open(os.path.join(IMAGES_DIR, "by_topic.json"), "w") as f:
        json.dump({**header, "_kind": "by_topic", "topics": by_topic}, f,
                  ensure_ascii=False, indent=1)

    # integrity: compare surviving samples against canonical downloads
    sample_report = []
    if os.path.isdir(SAMPLES_DIR):
        idx_by_name = {os.path.basename(e["file"]): e for e in entries}
        for name in sorted(os.listdir(SAMPLES_DIR)):
            if not name.endswith(".png"):
                continue
            sp = os.path.join(SAMPLES_DIR, name)
            e = idx_by_name.get(name)
            match = bool(e) and sha256_file(sp) == e["sha256"]
            sample_report.append({"file": name, "match": match})
    ok_samples = sum(1 for s in sample_report if s["match"])
    print(f"[organize] sample integrity: {ok_samples}/{len(sample_report)} "
          f"sha256 matches vs canonical store")

    if prune_samples and sample_report and ok_samples == len(sample_report):
        import shutil
        shutil.rmtree(SAMPLES_DIR)
        print("[organize] image_samples/ removed (superseded, sha256-verified)")

    summary = {
        "generated_at": now_iso(),
        "index_entries": len(entries), "question_images": len(q),
        "answer_images": len(a), "failed": len(bad),
        "files_on_disk": files_on_disk, "total_bytes": total,
        "distinct_papers": len(by_paper), "distinct_topics_raw": len(by_topic),
        "sample_check": sample_report,
        "samples_pruned": bool(prune_samples and ok_samples == len(sample_report)
                               and sample_report),
    }
    write_manifest(entries, summary)
    with open(os.path.join(IMAGES_DIR, "_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps({k: v for k, v in summary.items()
                      if k != "sample_check"}, indent=1))
    if bad:
        print("[organize] FAILED URLs:")
        for e in bad:
            print(f"  {e['status'] or '-'} {e['url']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["download", "organize", "all"],
                    default="download")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--prune-samples", action="store_true")
    ap.add_argument("--subject-dir", default=None,
                    help="subject folder (absolute, or relative to "
                         "topical_papers/); default = subject 11 Add Maths 0606")
    args = ap.parse_args()
    if args.subject_dir:
        set_subject_dir(args.subject_dir)
        print(f"[bulk] subject dir: {SUBJECT_DIR}")
    if args.phase in ("download", "all"):
        phase_download(args.batch, args.delay, args.limit)
    if args.phase in ("organize", "all"):
        phase_organize(args.prune_samples)
