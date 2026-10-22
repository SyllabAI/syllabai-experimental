#!/usr/bin/env python3
"""Image-phase driver: walk every harvested subject in priority order and
run the (resumable) bulk image downloader per subject. Chunk-safe: killed at
any moment, resumes at subject granularity; within-subject via INDEX.jsonl.

Usage: python3 exam_mate_images_all.py            # loop until killed
       python3 exam_mate_images_all.py --status
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
BULK = "/home/z/my-project/syllabai-experimental/exam-mate/scripts/exam_mate_image_bulk.py"
TP = "/home/z/my-project/syllabai-experimental/exam-mate/resources/topical_papers"
DEFAULT_STATE = f"{TP}/images_progress.json"
TIER_A = ["4", "21", "3"]
TIER_B = ["5", "6", "14", "15", "16", "17", "18", "19", "7", "13", "53", "54", "55"]


def load_state(state_file):
    if os.path.exists(state_file):
        return json.load(open(state_file))
    return {"done": {}, "current": None}


def work_list(cats):
    p = json.load(open(f"{TP}/progress.json"))
    import glob
    items = []
    for tier in [cats]:
        tier_items = []
        for key, info in p["done"].items():
            cid = key.split(":")[0]
            if cid not in cats:
                continue
            cands = glob.glob(f"{TP}/topical/{cid}_*/{key.split(':')[1]}_*/questions.jsonl")
            if not cands:
                continue
            n = 0
            for l in open(cands[0]):
                r = json.loads(l).get("payload", {})
                n += len(r.get("question_images", [])) + len(r.get("answer_images", []))
            if n == 0:
                continue
            tier_items.append((n, key, os.path.dirname(cands[0])))
        tier_items.sort(reverse=True)
        items.extend(tier_items)
    return items


def unique_urls(d):
    """Unique downloadable URLs — same filter as the bulk task builder
    (skips malformed paths the downloader would refuse anyway)."""
    from urllib.parse import urlparse
    import re
    pat = re.compile(r"^/questions/(\d+)/(\d+)/([^/]+\.png)$")
    urls = set()
    for l in open(os.path.join(d, "questions.jsonl")):
        p = json.loads(l).get("payload", {})
        for u in p.get("question_images", []) + p.get("answer_images", []):
            if pat.match(urlparse(u).path):
                urls.add(u)
    return len(urls)


def subject_complete(d):
    s = os.path.join(d, "images", "_summary.json")
    if not os.path.exists(s) or not os.path.exists(os.path.join(d, "questions.jsonl")):
        return False
    try:
        summ = json.load(open(s))
        # complete = every unique URL attempted (ok or genuine origin fail)
        # and every successful file present on disk
        return (summ.get("index_entries", 0) > 0
                and summ.get("files_on_disk") == summ.get("index_entries")
                and summ.get("index_entries", 0) + summ.get("failed", 0)
                >= unique_urls(d) - 2)  # -2 tolerance for ledger dupes
    except Exception:
        return False


def main(cats, state_file, batch, delay):
    st = load_state(state_file)
    items = work_list(cats)
    todo = [(n, k, d) for n, k, d in items if not subject_complete(d)]
    print(f"[images-all] subjects with images todo: {len(todo)} "
          f"(done already: {len(st['done'])})", flush=True)
    for n, key, d in todo:
        if subject_complete(d):
            continue
        print(f"[images-all] == {key} ({n} urls) {os.path.basename(d)}", flush=True)
        r = subprocess.run(
            [sys.executable, BULK, "--phase", "all", "--subject-dir",
             os.path.relpath(d, TP), "--batch", str(batch), "--delay", str(delay)],
            cwd=os.path.dirname(BULK), capture_output=True, text=True)
        tail = "\n".join((r.stdout or "").splitlines()[-3:])
        summ_path = os.path.join(d, "images", "_summary.json")
        if subject_complete(d):
            summ = json.load(open(summ_path))
            st["done"][key] = {"entries": summ["index_entries"],
                               "mb": round(summ["total_bytes"] / 1e6, 1)}
            print(f"[images-all] DONE {key}: {summ['index_entries']} images "
                  f"({summ['total_bytes']/1e6:.1f} MB)", flush=True)
        else:
            print(f"[images-all] PARTIAL {key} (resumable) rc={r.returncode}\n{tail}",
                  flush=True)
        json.dump(st, open(state_file, "w"), indent=1, ensure_ascii=False)
    print("[images-all] all subjects processed", flush=True)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--cats", default=",".join(TIER_A + TIER_B))
    ap.add_argument("--state-file", default=DEFAULT_STATE)
    ap.add_argument("--batch", type=int, default=6)
    ap.add_argument("--delay", type=float, default=0.7)
    a = ap.parse_args()
    if a.status:
        st = load_state(a.state_file)
        n = sum(v["entries"] for v in st["done"].values())
        mb = sum(v["mb"] for v in st["done"].values())
        print(f"subjects imaged: {len(st['done'])} | images: {n} | {mb:.0f} MB")
        sys.exit(0)
    main(a.cats.split(","), a.state_file, a.batch, a.delay)
