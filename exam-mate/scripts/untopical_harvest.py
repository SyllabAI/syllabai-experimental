#!/usr/bin/env python3
"""Untopical bank harvester — 27 subjects x years 2020-2026, anonymous.

Writes the SAME ledger formats as the existing topical corpus:
  questions.jsonl  (per-question, schema of topical corpus ledger)
     -> repo 1  exam-mate/resources/topical_papers/untopical/<cat>/<subj>/
  images/ + INDEX.jsonl (per-image schema of exam_mate_image_bulk.py)
     -> repo 2  exam-mate/resources/topical_papers/untopical/<cat>/<subj>/images/

Resumable: state file + append-only INDEX; skip completed subject-phases.
Shardable: --shard i --shards n processes disjoint subject subsets.

Usage:
  python3 untopical_harvest.py --phase all [--only 0452,9706]
      [--shard 0 --shards 1] [--batch 4] [--delay 1.0]
"""
import argparse, base64, hashlib, json, os, re, sys, time
from datetime import datetime, timezone
from urllib.parse import urlparse

sys.path.insert(0, "/home/z/my-project/syllabai-experimental/exam-mate/scripts")
from exam_mate_client import ExamMateClient  # noqa: E402

REPO1 = "/home/z/my-project/syllabai-experimental"
REPO2 = "/home/z/my-project/syllabai-experimental-2"
TP1 = f"{REPO1}/exam-mate/resources/topical_papers"
TP2 = f"{REPO2}/exam-mate/resources/topical_papers"
WORK = "/home/z/my-project/pp_harvest_work/untopical"
STATE = f"{WORK}/state.json"
CENSUS = "/home/z/my-project/exam-mate-probe/pp2026/untopical_census_2020plus.json"
BANK = "https://www.exam-mate.com/untopicalpastpapers"
BASE = "https://www.exam-mate.com"

CAT_DIR = {3: "3_IGCSE", 5: "5_A-LEVEL", 7: "7_DIPLOMA", 13: "13_SPM"}
ROWS_PER_PAGE = 25

PAPER_RE = re.compile(r"^(\S+)/([A-Za-z0-9]+)_([A-Za-z]+)_(\d{4})_Q(.+)$")
URL_RE_MEDIA = re.compile(r"^/media/questions/(\d+)/([^/]+\.png)$")
URL_RE_LEGACY = re.compile(r"^/questions/(\d+)/(\d+)/([^/]+\.png)$")
OC_RE = re.compile(r"selectQuestion\((\d+),(\d+),'(.*)'\)\s*$", re.S)
REF_RE = re.compile(r"^[A-Za-z0-9()&+.,'\- ]+/\S+$")

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

JS_ROWS = """() => Array.from(document.querySelectorAll('li[id^="qid-"]'))
    .map(li => ({id: li.id, oc: li.getAttribute('onclick') || '',
                 t: (li.innerText || '').trim().replace(/\\s+/g, ' ')}))"""


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def disk_free_gb():
    import shutil
    return shutil.disk_usage("/home/z").free / 1e9


def log(msg):
    print(f"[utop] {msg}", flush=True)


def state_load():
    try:
        return json.load(open(STATE))
    except Exception:
        return {}


def state_save(st):
    json.dump(st, open(STATE, "w"), indent=1)


def parse_paper_ref(text):
    m = PAPER_RE.match(text or "")
    if not m:
        return None
    return {"syllabus": m.group(1), "paper": m.group(2),
            "season": m.group(3), "year": m.group(4), "question": m.group(5)}


def sanitize(label):
    return re.sub(r"[^A-Za-z0-9]+", "_", label)


def subject_dirs(rec):
    cat = rec["cat"]
    subj_dir = f"{rec['subjectID']}_{sanitize(rec['subject'])}"
    d1 = f"{TP1}/untopical/{CAT_DIR[cat]}/{subj_dir}"
    d2 = f"{TP2}/untopical/{CAT_DIR[cat]}/{subj_dir}"
    return d1, f"{d2}/images"


# ------------------------------------------------------------- questions ----

def jsclick(c, sel):
    return c.page.evaluate(
        """(sel) => { const el = document.querySelector(sel);
                      if (!el) return 'missing';
                      el.addEventListener('click', e => e.preventDefault(),
                                          {once: true, capture: true});
                      el.click(); return 'clicked'; }""",
        sel)


def list_component_ok(c):
    """The Livewire JS boot is intermittently PARTIAL: the filter-box
    registers but the list component never does (rows frozen at the
    server-rendered default). Detect registration of the list component."""
    try:
        return c.page.evaluate("""() => {
            const row = document.querySelector('li[id^="qid-"]');
            if (!row || !window.Livewire) return false;
            const root = row.closest('[wire\\\\:id]');
            if (!root) return false;
            try { window.Livewire.find(root.getAttribute('wire:id'));
                  return true; } catch (e) { return false; }
        }""")
    except Exception:
        return False


def lw_ready(c, timeout=12.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            if c.page.evaluate("() => !!window.Livewire"):
                time.sleep(0.6)
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def click_lw(c, sel, wait_commit=6.0, tries=1):
    """Click a wire:click element; verify a Livewire commit actually fired
    (xhr_log grows); re-click on boot races / dropped commits."""
    for t in range(tries):
        lw_ready(c)
        n0 = len(c.xhr_log)
        r = jsclick(c, sel)
        if r == "missing":
            return "missing"
        t0 = time.time()
        while time.time() - t0 < wait_commit:
            if len(c.xhr_log) > n0:
                time.sleep(0.8)  # let the morph land
                return "committed"
            time.sleep(0.4)
        log(f"  click_lw: no commit for {sel[-44:]} (try {t + 1}/{tries})")
    return "no-commit"


def active_page(c):
    try:
        return c.page.evaluate(
            """() => { const el = document.querySelector(
                           'li.page-item.active .page-link, ul.pagination li.active span');
                       return el ? (el.innerText||'').trim() : ''; }""")
    except Exception as e:
        return f"EXC:{type(e).__name__}"


def wait_active_page(c, target, timeout=12.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if active_page(c) == str(target):
            return True
        time.sleep(0.5)
    return False


def livewire_goto(c, p):
    """Direct component call fallback: list.untopical-questions-list."""
    return c.page.evaluate(
        """(p) => {
            const root = document.querySelector('ul.pagination') &&
                document.querySelector('ul.pagination').closest('[wire\\\\:id]');
            const id = root && root.getAttribute('wire:id');
            if (id && window.Livewire && window.Livewire.find) {
                try { window.Livewire.find(id).call('gotoPage', p);
                      return 'called:' + id; } catch (e) { return 'err:' + e; }
            }
            return 'no-component';
        }""", p)


def reload_jump(c, p):
    """Last resort: hard reload current URL, re-tick years, re-apply, jump."""
    try:
        url = c.page.url
        c.fetch(url, settle_ms=1500)
        c.page.evaluate(
            """() => { for (const i of document.querySelectorAll('input[name="years[]"]'))
                 if (parseInt(i.value) >= 2020) i.checked = true; }""")
        jsclick(c, ".filter-button")
        time.sleep(6.0)
        return livewire_goto(c, p)
    except Exception as e:
        return f"exc:{e}"[:60]


def turn_page(c, p, want_rows=25):
    """Resilient page turn: up to 4 strategies; verify active page + rows."""
    attempts = [
        ("btn", lambda: jsclick(c, f'[wire\\:click="gotoPage({p})"]'), 9.0),
        ("btn2", lambda: jsclick(c, f'[wire\\:click="gotoPage({p})"]'), 9.0),
        ("lw", lambda: livewire_goto(c, p), 12.0),
        ("next", lambda: jsclick(c, 'a.page-link[rel="next"]'), 12.0),
        ("reload-jump", lambda: reload_jump(c, p), 16.0),
    ]
    for name, fn, wait in attempts:
        try:
            r = fn()
        except Exception as e:
            r = f"exc:{e}"[:60]
        if r == "missing":
            continue
        time.sleep(1.2)
        if wait_active_page(c, p, timeout=wait):
            rows, _bad = scrape_rows(c, p)
            if len(rows) > 0 and (len(rows) >= want_rows or p < 200):
                return True
        diag = c.page.evaluate("""() => ({
            active: (document.querySelector('li.page-item.active .page-link')||{innerText:''}).innerText,
            rows: document.querySelectorAll('li[id^="qid-"]').length,
            first: (document.querySelector('li[id^="qid-"]')||{id:''}).id,
            url: location.href.slice(-40),
            title: document.title.slice(0, 40)
        })""") if not active_page(c).startswith("EXC") else "page-eval-dead"
        log(f"  page {p}: attempt {name} -> {r} no activation; diag={diag}")
    return wait_active_page(c, p, timeout=4.0)


def scrape_rows(c, page_no):
    rows = c.page.evaluate(JS_ROWS)
    out, bad = [], 0
    for r in rows:
        m = OC_RE.search(r["oc"] or "")
        if not m:
            bad += 1
            continue
        try:
            payload = json.loads(m.group(3))
        except Exception:
            bad += 1
            continue
        text = ""
        for cand in r["t"].split(" "):
            if "/" in cand and REF_RE.match(cand):
                text = cand
                break
        if not text and r["t"]:
            text = r["t"].split(" ")[0]
        out.append({"qid": int(m.group(1)), "eventKey": int(m.group(2)),
                    "payload": payload, "text": text})
    return out, bad


def parse_rows_html(html):
    """Parse row payloads from raw rendered HTML (effects.html or page)."""
    import html as html_mod
    out = []
    for chunk in html.split('<li id="qid-')[1:]:
        chunk = chunk.split("</li>")[0]
        m = re.search(r"selectQuestion\((\d+),(\d+),'(.*?)'\)\s*\"", chunk, re.S)
        if not m:
            m = re.search(r"selectQuestion\((\d+),(\d+),'(.*)'\)", chunk, re.S)
        if not m:
            continue
        try:
            payload = json.loads(html_mod.unescape(m.group(3)))
        except Exception:
            continue
        rref = re.search(r">\s*([^<>]*?/\S+?)\s*</span>", chunk)
        text = rref.group(1).strip() if rref else ""
        out.append({"qid": int(m.group(1)), "eventKey": int(m.group(2)),
                    "payload": payload, "text": text})
    return out


def list_message_template(c):
    """Capture the last list.untopical-questions-list commit body."""
    for entry in reversed(c.xhr_log):
        if "list.untopical" in entry.get("url", "") and entry.get("post_data"):
            try:
                return json.loads(entry["post_data"])
            except Exception:
                continue
    return None


REPLAY_JS = """async ([url, body, csrf]) => {
    try {
        const r = await fetch(url, {method: 'POST', credentials: 'include',
            headers: {'Content-Type': 'application/json',
                      'Accept': 'text/html, application/xhtml+xml',
                      'X-Requested-With': 'XMLHttpRequest',
                      'X-Livewire': 'true',
                      'X-CSRF-TOKEN': csrf},
            body: body, signal: AbortSignal.timeout(30000)});
        const ct = r.headers.get('content-type') || '';
        const text = await r.text();
        return {status: r.status, ct, text: text};
    } catch (e) { return {error: String(e)}; }
}"""


def replay_goto(c, tmpl, page_no):
    """POST a gotoPage(page_no) callMethod replay via IN-PAGE fetch
    (WAF-immune). Returns (effects_html, status)."""
    body = json.loads(json.dumps(tmpl))
    body["updates"] = [{"type": "callMethod",
                        "payload": {"method": "gotoPage",
                                    "params": [int(page_no)]}}]
    csrf = getattr(c, "_utop_csrf", None) or c.page.evaluate(
        "() => (window.livewireScriptConfig && window.livewireScriptConfig.csrf) || null")
    res = c.page.evaluate(
        REPLAY_JS,
        [f"{BASE}/livewire/message/list.untopical-questions-list",
         json.dumps(body), csrf])
    if res.get("error"):
        return None, str(res["error"])[:60]
    if "text/html" in res.get("ct", ""):
        open(f"{WORK}/last_replay_fail.txt", "w").write(res["text"][:2500])
        return None, f"{res.get('status')} html(waf)"
    try:
        data = json.loads(res["text"])
    except Exception:
        open(f"{WORK}/last_replay_fail.txt", "w").write(res["text"][:2500])
        return None, f"{res.get('status')} json-err"
    eff = data.get("effects") or {}
    html = eff.get("html") or ""
    if not html:
        open(f"{WORK}/last_replay_fail.txt", "w").write(
            json.dumps({"keys": list(data.keys()),
                        "effect_keys": list(eff.keys())})[:2000])
    return html, res.get("status")


def select_subject(c, rec, expected_pager=None):
    """Select category+subject on the LIVE bank page.

    Site mechanics (established by probes):
    - subject/category $set commits pushState a canonical deep-link URL
      (STALE by one subject — cosmetic; page stays alive);
    - a filter commit fired while the URL is still bare triggers a REAL
      redirect that kills Livewire. Remedy: force a real subject transition
      first (sacrificial click) so the URL is already deep when filtering.
    Validated by: rows starting with subject code + pager size."""
    code = re.search(r"\(([A-Za-z0-9]+)\)", rec["subject"])
    code = code.group(1) if code else None
    if not getattr(c, "_utop_csrf_listener", False):
        def _cap(req, _c=c):
            if "/livewire/message/" in req.url:
                try:
                    t = (req.headers or {}).get("x-csrf-token")
                    if t:
                        _c._utop_csrf = t
                except Exception:
                    pass
        c.page.on("request", _cap)
        c._utop_csrf_listener = True
    for attempt in range(1, 3):
        try:
            for _boot in range(6):
                c.fetch(BANK)
                lw_ready(c)
                if list_component_ok(c):
                    break
                log(f"  boot: list component not registered; reloading "
                    f"({_boot + 1}/6)")
            else:
                continue
            click_lw(c, f"[wire\\:click=\"$set('categoryID', {rec['cat']})\"]")
            t0 = time.time()
            while time.time() - t0 < 9:
                if c.page.evaluate(
                    """(s) => !!document.querySelector(s)""",
                        f"[wire\\:click=\"$set('subjectID', {rec['subjectID']})\"]"):
                    break
                time.sleep(0.8)
            time.sleep(1.0)
            click_lw(c, f"[wire\\:click=\"$set('subjectID', {rec['subjectID']})\"]")
            # wait: rows belong to the target subject (URL-agnostic)
            t0 = time.time()
            ok = False
            while time.time() - t0 < 14:
                n = c.page.evaluate(
                    """() => document.querySelectorAll('li[id^="qid-"]').length""")
                if n:
                    if code:
                        t1 = c.page.evaluate(
                            """() => (document.querySelector('li[id^="qid-"]')||{innerText:''}).innerText.trim()""")
                        if t1.startswith(code + "/"):
                            ok = True
                            break
                    else:
                        ok = True
                        break
                time.sleep(0.8)
            if not ok:
                diag = c.page.evaluate(
                    """() => ({n: document.querySelectorAll('li[id^="qid-"]').length,
                             first: (document.querySelector('li[id^="qid-"]')||{innerText:''}).innerText.trim().slice(0,40),
                             url: location.href.slice(-52)})""")
                log(f"  select attempt {attempt}: rows not confirmed for {code} "
                    f"diag={diag}")
                continue
            c.page.evaluate(
                """() => { for (const i of document.querySelectorAll('input[name="years[]"]'))
                     if (parseInt(i.value) >= 2020) i.checked = true; }""")
            c.xhr_log.clear()
            r = jsclick(c, ".filter-button")
            if r == "missing":
                c.page.evaluate(
                    """() => { const b = document.querySelector('.filter-button');
                         if (b) b.click(); }""")
            time.sleep(6.0)
            btns = pager_info(c)
            if expected_pager and btns:
                if abs(max(btns) - expected_pager) > max(2, int(expected_pager * 0.05)):
                    log(f"  select attempt {attempt}: pager {max(btns)} != expected "
                        f"{expected_pager} (filter not applied?)")
                    continue
            rows, _ = scrape_rows(c, 1)
            if rows:
                if not list_message_template(c):
                    livewire_goto(c, 1)
                    time.sleep(2.5)
                tmpl = list_message_template(c)
                if tmpl:
                    os.makedirs(f"{WORK}/templates", exist_ok=True)
                    json.dump(tmpl, open(
                        f"{WORK}/templates/{rec['cat']}_{rec['subjectID']}.json", "w"))
                    return
                log(f"  select attempt {attempt}: rows ok but no list template")
                continue
            log(f"  select attempt {attempt}: no rows after apply")
        except Exception as e:
            log(f"  select attempt {attempt} exc: {type(e).__name__}: {e}"[:140])
            time.sleep(2)
        time.sleep(20.0 if attempt < 2 else 0)
    raise RuntimeError("select_subject failed after 2 attempts")


def pager_info(c):
    html = c.page.content()
    btns = sorted({int(x) for x in re.findall(r'gotoPage\((\d+)\)', html)})
    return btns


def phase_questions(c, rec):
    """Pure-GET harvest: the static ?cat=&sub=&years[]=&page= variant of the
    bank serves the same rows server-side — no Livewire UI, no POSTs.
    (Established 2026-10-24 after the Livewire boot lottery.)"""
    d1, _ = subject_dirs(rec)
    os.makedirs(d1, exist_ok=True)
    years_q = "&".join(f"years%5B%5D={y}" for y in range(2020, 2027))
    base = f"{BANK}?cat={rec['cat']}&sub={rec['subjectID']}&{years_q}"
    rows, seen_qids = [], set()
    bad_total = 0
    pages, pno = None, 1
    while True:
        html = c.fetch(f"{base}&page={pno}")
        if pages is None:
            btns = sorted({int(x) for x in re.findall(r"gotoPage\((\d+)\)", html)})
            pages = max(btns) if btns else 1
        page_rows = parse_rows_html(html)
        bad_total += sum(1 for _ in re.findall(r'<li id="qid-', html)) - len(page_rows)
        # validate years loosely (SPM refs can be non-standard formats)
        off = []
        for r in page_rows:
            ys = [int(y) for y in re.findall(r"(20\d\d)", r["text"] or "")]
            if ys and not any(2020 <= y <= 2026 for y in ys):
                off.append(r["text"])
        if off:
            raise RuntimeError(f"page {pno}: rows outside 2020-2026 "
                               f"(filter failed): {off[:2]}")
        new = [r for r in page_rows if r["qid"] not in seen_qids]
        if page_rows and not new:
            log(f"  page {pno}: all rows duplicate; stop")
            break
        for r in new:
            seen_qids.add(r["qid"])
            r["page"] = pno
        rows.extend(new)
        if pno % 10 == 0 or pno == pages or not page_rows:
            log(f"  page {pno}/{pages}: cumulative {len(rows)} rows")
        if pno >= pages or not page_rows:
            break
        pno += 1
        time.sleep(0.8)
    # write ledger (atomic)
    lines = []
    for r in rows:
        lines.append(json.dumps({
            "page": r["page"], "categoryID": rec["cat"],
            "subjectID": rec["subjectID"], "category": rec["category"],
            "subject": rec["subject"], "qid": r["qid"],
            "eventKey": r["eventKey"], "text": r["text"],
            "payload": r["payload"],
        }, ensure_ascii=False))
    tmp = f"{d1}/questions.jsonl.tmp"
    open(tmp, "w").write("\n".join(lines) + ("\n" if lines else ""))
    os.replace(tmp, f"{d1}/questions.jsonl")
    meta = {
        "category": {"id": rec["cat"], "label": rec["category"]},
        "subject": {"id": rec["subjectID"], "label": rec["subject"]},
        "bank": "untopical",
        "source": BANK,
        "url_pattern": BANK + "?cat=&sub=&years%5B%5D=YYYY&page=N",
        "years_filter": list(range(2020, 2027)),
        "questions": len(rows),
        "pages": pages,
        "unparsable_rows": bad_total,
        "harvested_at": now_iso(),
        "harvester": "scripts/untopical_harvest.py",
        "images_repo": "SyllabAI/syllabai-experimental-2",
        "notes": "NON-TOPICAL bank (non-chapterized subjects); topics empty "
                 "site-side; text refs from site row labels",
    }
    json.dump(meta, open(f"{d1}/meta.json", "w"), indent=1, ensure_ascii=False)
    return {"rows": len(rows), "pages": pages, "bad": bad_total}


# ---------------------------------------------------------------- images ----

def build_tasks(d1):
    tasks, seen = [], set()
    with open(f"{d1}/questions.jsonl") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            p = r.get("payload", {})
            for kind, key in (("question", "question_images"),
                              ("answer", "answer_images")):
                for url in p.get(key, []):
                    if url in seen:
                        continue
                    seen.add(url)
                    path = urlparse(url).path
                    mm = URL_RE_MEDIA.match(path)
                    ml = URL_RE_LEGACY.match(path)
                    if mm:
                        rel, src_qid, qfolder = path.lstrip("/"), int(mm.group(1)), None
                    elif ml:
                        rel, src_qid, qfolder = (path.lstrip("/"),
                                                 int(ml.group(2)), int(ml.group(1)))
                    else:
                        log(f"  WARN url not matching: {url[:90]}")
                        continue
                    tasks.append({
                        "url": url, "rel": rel, "kind": kind,
                        "qid": r.get("qid"), "event_key": r.get("eventKey"),
                        "page": r.get("page"), "paper_ref": r.get("text", ""),
                        "parsed": parse_paper_ref(r.get("text", "")),
                        "topics": p.get("topics", ""),
                        "mcq_answer": p.get("mcq_answer", ""),
                        "src_qid": src_qid, "qfolder": qfolder,
                        "category_id": r.get("categoryID"),
                        "subject_id": r.get("subjectID"),
                    })
    return tasks


def load_done(images_dir):
    done = {}
    idx = f"{images_dir}/INDEX.jsonl"
    if not os.path.exists(idx):
        return done
    with open(idx) as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get("status") != 200:
                continue
            fp = os.path.join(images_dir, e["file"])
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


def phase_images(c, rec, batch, delay, max_consec, img_limit=0):
    d1, images_dir = subject_dirs(rec)
    if not os.path.exists(f"{d1}/questions.jsonl"):
        raise RuntimeError("questions.jsonl missing; run questions phase")
    tasks = build_tasks(d1)
    done = load_done(images_dir)
    todo = [t for t in tasks if t["url"] not in done]
    log(f"  images: tasks={len(tasks)} done={len(done)} todo={len(todo)}")
    if not todo:
        return {"tasks": len(tasks), "downloaded": 0, "failed": 0}
    os.makedirs(images_dir, exist_ok=True)
    c.fetch(BANK, settle_ms=800)
    idx = open(f"{images_dir}/INDEX.jsonl", "a", buffering=1)
    ok = fail = consec = 0
    total_bytes = sum(done.values())
    try:
        for i in range(0, len(todo), batch if img_limit <= 0 else min(batch, img_limit)):
            if img_limit > 0 and i >= img_limit:
                log(f"  images: --img-limit {img_limit} reached; resume next run")
                break
            chunk = todo[i:i + batch]
            results = c.page.evaluate(FETCH_JS, [t["url"] for t in chunk])
            by_url = {r["url"]: r for r in results}
            retry = []
            for t in chunk:
                r = by_url.get(t["url"], {"url": t["url"], "error": "no-result"})
                ct = r.get("ct", "")
                data = None
                if r.get("b64"):
                    try:
                        data = base64.b64decode(r["b64"])
                    except Exception:
                        data = None
                if r.get("error") or "text/html" in ct or data is None:
                    retry.append(t)
                    continue
                fp = os.path.join(images_dir, t["rel"])
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
                consec = 0
            if retry:
                time.sleep(2.0)
                results2 = c.page.evaluate(FETCH_JS, [t["url"] for t in retry])
                by2 = {r["url"]: r for r in results2}
                if any("text/html" in r.get("ct", "") or r.get("error")
                       for r in by2.values()):
                    try:
                        c.fetch(BASE + "/", settle_ms=400)
                    except Exception as e:
                        log(f"  heal failed: {e}")
                for t in retry:
                    r = by2.get(t["url"], {"url": t["url"], "error": "no-result"})
                    ct = r.get("ct", "")
                    data = None
                    if r.get("b64"):
                        try:
                            data = base64.b64decode(r["b64"])
                        except Exception:
                            data = None
                    if r.get("error") or "text/html" in ct or data is None:
                        fail += 1
                        consec += 1
                        idx.write(json.dumps(
                            dict(t, file=t["rel"],
                                 status=r.get("status") or 0, bytes=0,
                                 content_type=ct or "",
                                 error=str(r.get("error") or "non-image"),
                                 downloaded_at=now_iso()),
                            ensure_ascii=False) + "\n")
                        continue
                    fp = os.path.join(images_dir, t["rel"])
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
                    consec = 0
            if (i // batch) % 20 == 0 or i + batch >= len(todo):
                log(f"  images {i + len(chunk)}/{len(todo)} ok={ok} fail={fail} "
                    f"{total_bytes / 1e6:.1f}MB")
            if consec >= max_consec:
                log(f"  {max_consec} consecutive failures — abort (resumable)")
                break
            time.sleep(delay)
    finally:
        idx.close()
    return {"tasks": len(tasks), "downloaded": ok, "failed": fail}


# --------------------------------------------------------------- organize ---

def nat_key(s):
    return (0, int(s)) if str(s).isdigit() else (1, str(s))


def phase_organize(rec):
    d1, images_dir = subject_dirs(rec)
    idx = f"{images_dir}/INDEX.jsonl"
    best, order = {}, []
    if os.path.exists(idx):
        with open(idx) as f:
            for line in f:
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
    os.makedirs(images_dir, exist_ok=True)
    q = [e for e in entries if e["kind"] == "question"]
    a = [e for e in entries if e["kind"] == "answer"]
    bad = [e for e in entries if e.get("bytes") == 0]
    total = sum(e["bytes"] for e in entries)
    files_on_disk = sum(1 for e in entries
                        if os.path.exists(os.path.join(images_dir, e["file"])))

    by_paper = {}
    for e in entries:
        ref = e.get("paper_ref") or "?"
        slot = by_paper.setdefault(ref, {
            "qid": e["qid"], "page": e.get("page"),
            "topics": e.get("topics", ""), "mcq_answer": e.get("mcq_answer", ""),
            "parsed": e.get("parsed"),
            "question_images": [], "answer_images": []})
        slot[("question" if e["kind"] == "question" else "answer") + "_images"]\
            .append(e["file"])

    def sort_key(item):
        p = item[1].get("parsed") or {}
        return (-(int(p.get("year") or 0)), p.get("season") or "",
                nat_key(p.get("paper") or ""), nat_key(p.get("question") or ""))

    by_paper = {k: by_paper[k]
                for k in sorted(by_paper, key=lambda k: sort_key((k, by_paper[k])))}
    header = {
        "_note": "Derived view of INDEX.jsonl — provenance lives there.",
        "source": "exam-mate.com NON-TOPICAL PAST PAPER QUESTIONS bank "
                  "(/untopicalpastpapers)",
        "generated_at": now_iso(),
        "images_dir": "images/",
        "url_reconstruction": "https://www.exam-mate.com/" + "<file>",
    }
    json.dump({**header, "_kind": "by_paper", "papers": by_paper},
              open(f"{images_dir}/by_paper.json", "w"),
              ensure_ascii=False, indent=1)
    json.dump({**header, "_kind": "by_topic", "topics": {}},
              open(f"{images_dir}/by_topic.json", "w"),
              ensure_ascii=False, indent=1)
    years = sorted({(e.get("parsed") or {}).get("year", "?") for e in entries})
    summary = {
        "generated_at": now_iso(), "index_entries": len(entries),
        "question_images": len(q), "answer_images": len(a),
        "failed": len(bad), "files_on_disk": files_on_disk,
        "total_bytes": total, "distinct_papers": len(by_paper),
        "years_covered": years,
    }
    json.dump(summary, open(f"{images_dir}/_summary.json", "w"), indent=1)
    return summary


# ------------------------------------------------------------------ main ----

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["questions", "images", "organize", "all"],
                    default="all")
    ap.add_argument("--img-limit", type=int, default=0,
                    help="max image downloads per subject per invocation")
    ap.add_argument("--budget-sec", type=float, default=0,
                    help="stop starting new subject units after this many sec")
    ap.add_argument("--only", default=None, help="comma list of subject codes")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--shards", type=int, default=1)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--max-consec", type=int, default=30)
    args = ap.parse_args()

    census = json.load(open(CENSUS))["done"]
    subjects = []
    for skey, r in census.items():
        subjects.append({
            "cat": r["cat"], "category": r["category"],
            "subjectID": r["subjectID"], "subject": r["subject"],
            "pager_last": max(r.get("pager_pages") or [1]),
            "badge": r.get("badge_total"),
        })
    subjects.sort(key=lambda s: -s["pager_last"])
    if args.only:
        keep = set(args.only.split(","))
        subjects = [s for s in subjects
                    if (re.search(r"\((\w+)\)", s["subject"]) or [None, s["subject"]])[1] in keep]
    mine = subjects[args.shard::args.shards]
    log(f"shard {args.shard}/{args.shards}: {len(mine)} subjects: "
        + ", ".join(s["subject"] for s in mine))

    st = state_load()
    t0 = time.time()
    for rec in mine:
        if args.budget_sec and time.time() - t0 > args.budget_sec:
            log("budget reached, exiting cleanly")
            break
        if disk_free_gb() < 1.2:
            log(f"DISK GUARD: only {disk_free_gb():.2f} GB free — stopping "
                "(commit+prune completed subjects first)")
            break
        skey = f"{rec['cat']}:{rec['subjectID']}"
        d1, images_dir = subject_dirs(rec)
        log(f"== {rec['category']} / {rec['subject']} ({skey})")
        st.setdefault(skey, {})
        c = ExamMateClient(restore_state=False, verbose=False)
        try:
            if args.phase in ("questions", "all"):
                if st[skey].get("questions", {}).get("done"):
                    log("  questions: already done, skip")
                else:
                    try:
                        res = phase_questions(c, rec)
                        st[skey]["questions"] = {**res, "done": True,
                                                 "at": now_iso()}
                        log(f"  questions done: {res}")
                    except Exception as e:
                        log(f"  questions FAIL: {type(e).__name__}: {e}"[:200])
                        st[skey]["questions"] = {
                            "done": False,
                            "error": f"{type(e).__name__}: {e}"[:200]}
                    state_save(st)
            if args.phase in ("images", "all"):
                if st[skey].get("questions", {}).get("done") or \
                        os.path.exists(f"{d1}/questions.jsonl"):
                    try:
                        res = phase_images(c, rec, args.batch, args.delay,
                                           args.max_consec, args.img_limit)
                        st[skey]["images"] = {**res, "at": now_iso()}
                        log(f"  images done: {res}")
                    except Exception as e:
                        log(f"  images FAIL: {type(e).__name__}: {e}"[:200])
                        st[skey]["images"] = {
                            "error": f"{type(e).__name__}: {e}"[:200]}
                    state_save(st)
                else:
                    log("  images: skip (no ledger)")
            if args.phase in ("organize", "all"):
                if st[skey].get("questions", {}).get("done"):
                    summ = phase_organize(rec)
                    st[skey]["organize"] = {"at": now_iso(),
                                            "index_entries": summ["index_entries"]}
                    state_save(st)
                    log(f"  organize done: {summ['index_entries']} entries")
        finally:
            try:
                c.close()
            except Exception:
                pass
    log("shard complete")


if __name__ == "__main__":
    main()
