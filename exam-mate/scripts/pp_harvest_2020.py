#!/usr/bin/env python3
"""exam-mate PAST PAPERS harvester (2020-2026) — QP/MS PDFs -> per-question PNGs.

Pipeline per subject:
  1. UI-drive /pastpapers: category -> subject -> tick year checkboxes -> apply
  2. Walk result pages, scrape paper rows {rowID, paper_ref}
  3. Click each row (UI), read viewer iframes -> QP/MS/Extra PDF urls
  4. Download PDFs via in-page fetch (WAF-immune)
  5. PyMuPDF: render pages (150 dpi) -> detect question-number markers in text
     layer -> crop per-question PNGs; front-matter/undetected pages stay
     page-level
  6. Ledger: paper.json (provenance incl. source pdf sha256) + INDEX.jsonl
     (per-image sha256/dims/bbox/qnum) + subject MANIFEST.md

Usage:
  python3 pp_harvest_2020.py --cat 21 --subject 615 [--years 2020,2021,...]
      [--limit N] [--out DIR] [--no-push]
"""
import argparse, hashlib, json, os, re, sys, time

sys.path.insert(0, "/home/z/my-project/syllabai-experimental/exam-mate/scripts")
from exam_mate_client import ExamMateClient
import fitz  # PyMuPDF

WORK = "/home/z/my-project/pp_harvest_work"
REPO2 = "/home/z/my-project/syllabai-experimental-2"
CAT_LABEL = {3: "3_IGCSE", 4: "4_IGCSE", 5: "5_A-LEVEL", 6: "6_A-LEVEL",
             7: "7_DIPLOMA", 12: "12_O-LEVEL", 14: "14_GCSE_9-1_", 15: "15_GCSE",
             16: "16_A-LEVEL", 17: "17_A-LEVEL", 18: "18_AS", 19: "19_AS",
             21: "21_IGCSE_9-1_", 11: "11_CHECKPOINT", 20: "20_PRE-U",
             53: "53_TYT_YKS_", 54: "54_AYT_YKS_", 55: "55_YDT_YKS_"}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def safe(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")

# ---------------------------------------------------------------- browser part

def jsclick(c, sel):
    return c.page.evaluate(f"""() => {{
        const el = document.querySelector({json.dumps(sel)});
        if (!el) return 'missing';
        el.click(); return 'clicked';
    }}""")

def setup_state(c, cat_id, subject_id, years, log=print):
    """Navigate + select category/subject + tick years + apply. Always required."""
    c.fetch("https://www.exam-mate.com/pastpapers")
    time.sleep(2)
    jsclick(c, f"[wire\\:click=\"$set('categoryID', {cat_id})\"]"); time.sleep(2.5)
    jsclick(c, f"[wire\\:click=\"$set('subjectID', {subject_id})\"]"); time.sleep(2.5)
    c.page.evaluate("() => { const b=document.querySelector('.filter-button'); if(b) b.click(); }")
    time.sleep(4)
    if years:
        got = c.page.evaluate("""(years) => {
            const out = [];
            for (const y of years) {
                const cb = document.getElementById('year-' + y);
                if (!cb) continue;
                if (!cb.checked) (cb.closest('label') || cb).click();
                out.push(y);
            }
            return out;
        }""", [str(y) for y in years])
        log(f"  years ticked: {got}")
        c.page.evaluate("() => { const b=document.querySelector('.filter-button'); if(b) b.click(); }")
        time.sleep(4.5)

def discover_rows(c, cat_id, subject_id, years, log=print):
    setup_state(c, cat_id, subject_id, years, log=log)

    def scrape():
        return c.page.evaluate("""
          () => Array.from(document.querySelectorAll('#paper-list li[wire\\\\:click*="selectPastpaper"]'))
                .map(li => { const m = li.getAttribute('wire:click').match(/selectPastpaper\\((\\d+)\\)/);
                             return m ? {id: m[1],
                                         txt: (li.innerText||'').trim().replace(/\\s+/g, ' ')} : null; })
                .filter(Boolean)
        """)

    rows, page_no = [], 1
    while True:
        rows.extend(scrape())
        has_next = c.page.evaluate("""() => {
            const el = document.querySelector('[wire\\\\:click="nextPage"]');
            return !!(el && !el.classList.contains('disabled') && el.offsetParent !== null);
        }""")
        log(f"  page {page_no}: cumulative {len(rows)} rows")
        if not has_next or page_no > 40:
            break
        c.page.evaluate("() => { const el=document.querySelector('[wire\\\\:click=\"nextPage\"]'); el && el.click(); }")
        time.sleep(3)
        page_no += 1
    # dedupe
    seen, uniq = set(), []
    for r in rows:
        if r["id"] not in seen:
            seen.add(r["id"]); uniq.append(r)
    return uniq

def viewer_urls(c, row_id, log=print):
    """Click a visible row; return {qp, ms, extra} pdf urls (early-exit on 2+)."""
    c.page.evaluate("""(id) => {
        const li = document.querySelector('#paper-list li[wire\\\\:click="selectPastpaper(' + id + ')"]');
        if (li) li.click();
        return !!li;
    }""", row_id)
    urls = []
    for _ in range(20):  # up to 8 s
        time.sleep(0.4)
        urls = c.page.evaluate("""() => Array.from(document.querySelectorAll('iframe'))
              .map(f => f.src).filter(s => /media\\/pastpapers\\/.*\\.pdf/i.test(s))""")
        if len(urls) >= 2:
            break
    time.sleep(0.4)
    qp = ms = extra = None
    for u in urls:
        low = u.lower()
        if re.search(r"_qp[_\d]*\.pdf|/\d+/[^/]*qp[^/]*\.pdf", low) or "_question" in low:
            qp = qp or u
        elif re.search(r"_ms[_\d]*\.pdf|mark|scheme|answer", low):
            ms = ms or u
        else:
            extra = extra or u
    if not qp and urls: qp = urls[0]
    if not ms and len(urls) > 1: ms = urls[1]
    return {"qp": qp, "ms": ms, "extra": extra, "all": urls}

# ---------------------------------------------------------------- pdf part

QNUM_RE = re.compile(r"^(?:Q\s*)?(\d{1,2})[).\s]*$")

def collect_markers(doc, log=print):
    """Paper-level scan: strict left-margin question-number markers.

    Edexcel/CIE/AQA/OCR QP+MS print question numbers in the left margin:
    x0 < 13% page width, height ~17pt (size 12), above the footer zone.
    Footer page numbers (y>88%, size 10) and in-diagram values (x>13%)
    are excluded by these thresholds.
    """
    markers = []
    for pno in range(len(doc)):
        page = doc[pno]
        pw, ph = page.rect.width, page.rect.height
        d = page.get_text("dict")
        for block in d.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    t = (span.get("text") or "").strip()
                    m = QNUM_RE.match(t)
                    if not m:
                        continue
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 > pw * 0.13:
                        continue
                    if y0 > ph * 0.88:          # footer page numbers
                        continue
                    h = y1 - y0
                    if h > 30 or h < 8:         # giant numerals / tiny fragments
                        continue
                    n = int(m.group(1))
                    if not (1 <= n <= 30):
                        continue
                    if span.get("size", 12) < 9.5:
                        continue
                    markers.append({"page": pno, "n": n, "x0": x0, "y0": y0,
                                    "y1": y1, "ph": ph})
    # paper-level sequential walk: keep markers forming 1,2,3,...
    keep, expected = [], 1
    for mkr in markers:
        if mkr["n"] == expected:
            keep.append(mkr)
            expected += 1
        elif mkr["n"] > expected and keep:
            # tolerate a missing marker (undetected number): swallow the gap
            # only if the NEXT expected marker never appears — we can't know
            # yet, so accept out-of-order larger n as the next question
            keep.append(mkr)
            expected = mkr["n"] + 1
    return keep

def split_pdf(pdf_path, out_dir, kind, dpi=150, log=print):
    """Rasterize + question-split one PDF. Returns (entries, n_pages, n_kept_pages)."""
    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    markers = collect_markers(doc, log=log)
    entries = []

    def render_page_png(page, pno, tag):
        png = os.path.join(out_dir, f"{kind}_p{pno+1:02d}{tag}.png")
        page.get_pixmap(matrix=mat, alpha=False).save(png)
        return {"kind": kind, "page": pno + 1, "png": os.path.basename(png),
                "w": round(page.rect.width * zoom), "h": round(page.rect.height * zoom),
                "sha256": sha256(png), "bytes": os.path.getsize(png), "questions": []}

    if len(markers) < 2 or markers[0]["n"] != 1:
        log(f"    {kind}: markers={len(markers)} -> page-level fallback")
        for pno in range(len(doc)):
            entries.append(render_page_png(doc[pno], pno, ""))
        n = len(doc)
        doc.close()
        return entries, n, n

    # build question regions (cross-page): marker i -> marker i+1
    regions = []
    for i, m in enumerate(markers):
        if i + 1 < len(markers):
            nx = markers[i + 1]
        else:
            nx = {"page": m["page"], "y0": doc[m["page"]].rect.height}  # stop at page end
        segs = []
        if nx["page"] == m["page"]:
            segs.append((m["page"], m["y0"] - 4, nx["y0"]))
        else:
            segs.append((m["page"], m["y0"] - 4, doc[m["page"]].rect.height))
            for pp in range(m["page"] + 1, nx["page"]):
                segs.append((pp, 0.0, doc[pp].rect.height))
            segs.append((nx["page"], 0.0, nx["y0"]))
        regions.append({"q": m["n"], "segs": segs})

    q_pages = set()
    for r in regions:
        for (pp, y0, y1) in r["segs"]:
            q_pages.add(pp)

    # front pages (before first marker) + any non-question page: keep page png
    first_page = markers[0]["page"]
    page_entries = {}
    for pno in range(len(doc)):
        if pno not in q_pages:
            page_entries[pno] = render_page_png(doc[pno], pno, "")
            entries.append(page_entries[pno])

    for r in regions:
        for seg_i, (pp, y0, y1) in enumerate(r["segs"]):
            if y1 - y0 < 12:
                continue
            page = doc[pp]
            clip = fitz.Rect(0, max(0, y0), page.rect.width, min(page.rect.height, y1))
            tag = "" if seg_i == 0 else "_cont"
            qpng = os.path.join(out_dir, f"{kind}_q{r['q']:02d}_p{pp+1:02d}{tag}.png")
            page.get_pixmap(matrix=mat, alpha=False, clip=clip).save(qpng)
            # attach to a page entry anchor (for ordering) — use first segment's page
            entries.append({"kind": kind, "page": pp + 1, "png": os.path.basename(qpng),
                            "w": round(clip.width * zoom), "h": round(clip.height * zoom),
                            "sha256": sha256(qpng), "bytes": os.path.getsize(qpng),
                            "questions": [{"q": r["q"], "cont": seg_i > 0,
                                           "bbox": [round(y0, 1), round(y1, 1)]}]})
    n = len(doc)
    doc.close()
    return entries, n, len(page_entries)

# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cat", type=int, required=True)
    ap.add_argument("--subject", type=int, required=True)
    ap.add_argument("--subject-label", default="")
    ap.add_argument("--years", default="2020,2021,2022,2023,2024,2025,2026")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--budget", type=int, default=540,
                    help="stop resolving/downloading after N seconds (checkpointed)")
    ap.add_argument("--no-split", action="store_true",
                    help="skip the pdf->png phase (intermediate chunk runs)")
    ap.add_argument("--skip-discover", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()
    years = [y.strip() for y in args.years.split(",") if y.strip()]

    os.makedirs(WORK, exist_ok=True)
    subj_tag = args.subject_label or f"{args.cat}-{args.subject}"
    work_subj = os.path.join(WORK, f"cat{args.cat}_subj{args.subject}")
    os.makedirs(work_subj, exist_ok=True)
    rows_file = os.path.join(work_subj, "rows.json")

    c = ExamMateClient(restore_state=False, verbose=False)
    try:
        if args.skip_discover and os.path.exists(rows_file):
            rows = json.load(open(rows_file))
            print(f"loaded {len(rows)} cached rows")
            setup_state(c, args.cat, args.subject, years)
        else:
            print(f"== discovering rows cat={args.cat} subj={args.subject} years={years}")
            rows = discover_rows(c, args.cat, args.subject, years)
            json.dump(rows, open(rows_file, "w"), indent=1)
            print(f"== {len(rows)} unique rows cached")

        if args.limit:
            rows = rows[:args.limit]

        # step 2: per-row viewer urls + immediate download (browser session live)
        urls_file = os.path.join(work_subj, "paper_urls.json")
        paper_urls = json.load(open(urls_file)) if os.path.exists(urls_file) else {}
        print("== resolving viewer urls + downloading pdfs (click per paper)")
        need = {r["id"] for r in rows if r["id"] not in paper_urls or not paper_urls[r["id"]].get("qp")}
        t0 = time.time()
        rows_by_id = {r["id"]: r["txt"] for r in rows}

        def visible_ids():
            try:
                return c.page.evaluate("""
                  () => Array.from(document.querySelectorAll('#paper-list li[wire\\\\:click*="selectPastpaper"]'))
                        .map(li => (li.getAttribute('wire:click').match(/selectPastpaper\\((\\d+)\\)/) || [])[1])
                """)
            except Exception:
                return []

        def goto_page(p, expected_ids=None):
            """Click gotoPage(p) and VERIFY the expected rows became visible."""
            for wait_s in (3.0, 5.0, 8.0):
                try:
                    c.page.evaluate(f"""() => {{
                        const el = document.querySelector('[wire\\\\:click="gotoPage({p})"]');
                        if (el) {{ el.click(); return true; }}
                        return false;
                    }}""")
                except Exception:
                    pass
                time.sleep(wait_s)
                if expected_ids:
                    vis = visible_ids()
                    if len(set(vis) & set(expected_ids)) >= min(20, len(expected_ids)):
                        return True
                else:
                    return True
            return False

        page_ids = {}
        per = 25
        for i, r in enumerate(rows):
            page_ids.setdefault(i // per + 1, []).append(r["id"])

        for p in range(1, 8):
            if not need or time.time() - t0 > args.budget:
                break
            goto_page(p, page_ids.get(p))
            for attempt in range(3):
                if not need or time.time() - t0 > args.budget:
                    break
                visible = visible_ids()
                todo = [r for r in visible if r in need]
                print(f"  [page {p} try {attempt+1}] visible={len(visible)} todo={len(todo)} need={len(need)} t={int(time.time()-t0)}s", flush=True)
                if not todo:
                    break
                for rid in todo:
                    if not need or time.time() - t0 > args.budget:
                        break
                    info = viewer_urls(c, rid)
                    txt = rows_by_id.get(rid, "")
                    paper_urls[rid] = {"txt": txt, **info}
                    need.discard(rid)
                    print(f"  {txt[:44]:44s} qp={'Y' if info['qp'] else '-'} ms={'Y' if info['ms'] else '-'} extra={'Y' if info['extra'] else '-'}", flush=True)
                    json.dump(paper_urls, open(urls_file, "w"), indent=1)
                    # interleave: download this paper's pdfs right away
                    ref = safe(txt or f"row{rid}")
                    pdir = os.path.join(work_subj, ref)
                    os.makedirs(pdir, exist_ok=True)
                    for kind in ("qp", "ms"):
                        url = info.get(kind)
                        fn = os.path.join(pdir, f"{kind}.pdf")
                        if os.path.exists(fn) and os.path.getsize(fn) > 1000:
                            continue
                        if not url:
                            continue
                        st, sz, ct = c.download(url, fn)
                        ok = sz > 1000 and open(fn, "rb").read(5).startswith(b"%PDF")
                        print(f"    dl {kind}: st={st} sz={sz} {'OK' if ok else 'FAIL'}", flush=True)
                        if not ok and os.path.exists(fn):
                            os.remove(fn)
                        time.sleep(0.3)
                    time.sleep(0.3)
                else:
                    continue
                break
        if need:
            print(f"  [budget/pages] {len(need)} still unresolved (resume next run)")
        print(f"== resolved urls for {len(paper_urls)} papers")

        # downloads INSIDE the session (in-page fetch needs site origin + clearance)
        for rid, u in sorted(paper_urls.items()):
            if not u.get("qp"):
                continue
            if time.time() - t0 > args.budget * 1.9:
                print("  [budget] download stop (resume next run)")
                break
            ref = safe(u.get("txt") or f"row{rid}")
            pdir = os.path.join(work_subj, ref)
            os.makedirs(pdir, exist_ok=True)
            for kind in ("qp", "ms"):
                url = u.get(kind)
                fn = os.path.join(pdir, f"{kind}.pdf")
                if os.path.exists(fn) and os.path.getsize(fn) > 1000:
                    continue
                if not url:
                    continue
                st, sz, ct = c.download(url, fn)
                ok = sz > 1000 and open(fn, "rb").read(5).startswith(b"%PDF")
                print(f"  dl {ref} {kind}: st={st} sz={sz} {'OK' if ok else 'FAIL'}")
                if not ok and os.path.exists(fn):
                    os.remove(fn)
                time.sleep(0.4)
    finally:
        c.close()

    # step 3-5 (no browser): split pdfs -> pngs + ledger
    if args.no_split:
        print("[no-split] skipping raster phase")
        return
    papers = []
    for rid, u in sorted(paper_urls.items()):
        if not u.get("qp"):
            continue
        ref = safe(u.get("txt") or f"row{rid}")
        pdir = os.path.join(work_subj, ref)
        try:
            kinds = {}
            for kind in ("qp", "ms"):
                fn = os.path.join(pdir, f"{kind}.pdf")
                if os.path.exists(fn) and os.path.getsize(fn) > 1000:
                    kinds[kind] = {"sha256": sha256(fn), "bytes": os.path.getsize(fn)}
            if "qp" not in kinds:
                continue
            images = {}
            for kind in ("qp", "ms"):
                fn = os.path.join(pdir, f"{kind}.pdf")
                if not os.path.exists(fn):
                    continue
                imgdir = os.path.join(pdir, kind.upper())
                os.makedirs(imgdir, exist_ok=True)
                ents, npages, nkept = split_pdf(fn, imgdir, kind, dpi=args.dpi)
                images[kind] = {"pages": npages, "page_pngs_kept": nkept, "entries": ents}
            rec = {"row_id": rid, "paper_ref": u.get("txt"),
                   "urls": {k: u.get(k) for k in ("qp", "ms", "extra")},
                   "pdfs": kinds, "images": images}
            json.dump(rec, open(os.path.join(pdir, "paper.json"), "w"), indent=1)
            papers.append(rec)
            nq = sum(len(e["questions"]) for e in images.get("qp", {}).get("entries", []))
            nqms = sum(len(e["questions"]) for e in images.get("ms", {}).get("entries", []))
            print(f"  split {ref}: qp {images['qp']['pages']}p/{nq}q, ms {images.get('ms', {}).get('pages', 0)}p/{nqms}q")
            # free disk: delete PDFs after successful split
            for kind in ("qp", "ms"):
                fn = os.path.join(pdir, f"{kind}.pdf")
                if os.path.exists(fn) and images.get(kind):
                    os.remove(fn)
        except Exception as e:
            print(f"  !! error on {ref}: {e}")

    # INDEX.jsonl for subject — one line per PNG (page-level or question segment)
    idx = []
    for rec in papers:
        for kind in ("qp", "ms"):
            for ent in rec["images"].get(kind, {}).get("entries", []):
                row = {"paper_ref": rec["paper_ref"], "row_id": rec["row_id"],
                       "kind": kind, "page": ent["page"], "png": ent["png"],
                       "w": ent["w"], "h": ent["h"], "sha256": ent["sha256"],
                       "bytes": ent["bytes"]}
                if ent["questions"]:
                    q = ent["questions"][0]
                    row.update({"q": q["q"], "cont": q["cont"], "bbox_y": q["bbox"]})
                idx.append(row)
    with open(os.path.join(work_subj, "INDEX.jsonl"), "w") as f:
        for r in idx:
            f.write(json.dumps(r) + "\n")
    json.dump({"cat": args.cat, "subject": args.subject, "label": subj_tag,
               "years": years, "papers": len(papers),
               "page_pngs": sum(1 for r in idx if "q" not in r),
               "question_pngs": sum(1 for r in idx if "q" in r)},
              open(os.path.join(work_subj, "_summary.json"), "w"), indent=1)
    print(f"== DONE {subj_tag}: {len(papers)} papers, "
          f"{sum(1 for r in idx if 'q' in r)} question PNGs, "
          f"{sum(1 for r in idx if 'q' not in r)} page PNGs")

if __name__ == "__main__":
    main()
