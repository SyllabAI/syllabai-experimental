#!/usr/bin/env python3
"""Census sweep of the UNTOPICAL bank (/untopicalpastpapers).

For each of the 27 subjects (4 categories) tick years 2020-2026, apply,
and record: total-question badge, pager page count, first-page row refs,
year distribution on page 1. Output: checkpointed census JSON, resumable
(per-subject skip).

Usage: python3 untopical_census.py [--only 0452,9706]
"""
import json, re, sys, time
sys.path.insert(0, "/home/z/my-project/syllabai-experimental/exam-mate/scripts")
from exam_mate_client import ExamMateClient

OUT = "/home/z/my-project/exam-mate-probe/pp2026"
CENSUS = f"{OUT}/untopical_census_2020plus.json"
BANK = "https://www.exam-mate.com/untopicalpastpapers"

CATS = [(3, "CIE IGCSE"), (5, "CIE A-LEVEL"), (7, "IB DIPLOMA"), (13, "SPM")]
# from untopical_catalog.json (subject ids captured live in Task 22)
SUBJECTS = {
    3: [(10, "Accounting(0452)"), (235, "Agriculture(0600)"),
        (14, "Business Studies(0450)"), (236, "Child Development(0637)"),
        (130, "Design & Technology(0445)"), (241, "Islamiyat(0493)"),
        (137, "Physical Education(0413)"), (286, "Physical Science(0652)")],
    5: [(46, "Accounting(9706)"), (146, "Business(9609)"),
        (182, "Design & Technology(9705)"), (151, "Design & Textiles(9631)"),
        (289, "Environmental Management(8291)"),
        (166, "Information Technology(9626)"), (167, "Islamic Studies(9013)"),
        (168, "LAW(9084)")],
    7: [(113, "Computer Science"), (114, "Design Technology"),
        (120, "Sports,Exercise & Health Science")],
    13: [(334, "Bahasa Melayu(1103)"), (331, "Ekonomi(3767)"),
         (328, "Geography(2280)"),
         (335, "Pendidikan Al-Quran Dan Al-Sunnah(5227)"),
         (333, "Pendidikan Islam(1223)"),
         (329, "Pendidikan Syari'ah Islamiah(5228)"),
         (330, "Sejarah(1249)"), (332, "Tasawwur Islam(5226)")],
}

JS_ROWS = """() => Array.from(document.querySelectorAll('li[id^="qid-"]'))
    .map(li => ({
        id: li.id,
        oc: li.getAttribute('onclick') || '',
        t: (li.innerText || '').trim().replace(/\\s+/g, ' ')
    }))"""


def jsclick(c, sel):
    return c.page.evaluate(
        """(sel) => { const el = document.querySelector(sel);
                      if (!el) return 'missing'; el.click(); return 'clicked'; }""",
        sel)


def scrape_page(c):
    rows = c.page.evaluate(JS_ROWS)
    out = []
    for r in rows:
        m = re.search(r"selectQuestion\((\d+),(\d+),", r["oc"] or "")
        if not m:
            continue
        out.append({"qid": int(m.group(1)), "eventKey": int(m.group(2)),
                    "text": r["t"]})
    return out


def census_one(c, cat, cat_label, sid, slabel):
    c.fetch(BANK)
    time.sleep(2.0)
    jsclick(c, f"[wire\\:click=\"$set('categoryID', {cat})\"]")
    time.sleep(2.0)
    jsclick(c, f"[wire\\:click=\"$set('subjectID', {sid})\"]")
    time.sleep(2.0)
    years_present = c.page.evaluate(
        """() => Array.from(document.querySelectorAll('input[name="years[]"]'))
             .map(i => i.value)""")
    ticked = c.page.evaluate(
        """() => { const out = [];
           for (const i of document.querySelectorAll('input[name="years[]"]'))
             if (parseInt(i.value) >= 2020) { i.checked = true; out.push(i.value); }
           return out; }""")
    c.page.evaluate(
        """() => { const b = document.querySelector('.filter-button') ||
             Array.from(document.querySelectorAll('button'))
               .find(x => /apply|filter|search/i.test(x.innerText||''));
           if (b) b.click(); }""")
    time.sleep(6.0)
    body = c.page.evaluate("() => document.body.innerText")
    mb = re.search(r"([\d,]+)\s*Questions?", body)
    total = int(mb.group(1).replace(",", "")) if mb else None
    html = c.page.content()
    pages_btn = sorted({int(x) for x in re.findall(r"gotoPage\((\d+)\)", html)})
    rows = scrape_page(c)
    years_in_rows = sorted({m for r in rows
                            for m in re.findall(r"20\d\d", r["text"])})
    return {
        "cat": cat, "category": cat_label, "subjectID": sid, "subject": slabel,
        "year_inputs": years_present, "years_ticked": ticked,
        "badge_total": total, "pager_pages": pages_btn,
        "page1_rows": len(rows),
        "page1_sample": [r["text"] for r in rows[:3]],
        "page1_years": years_in_rows,
        "error": None if total is not None or rows else "no rows/badge",
    }


def main():
    only = None
    key_filter = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    if "--key" in sys.argv:
        key_filter = sys.argv[sys.argv.index("--key") + 1]
    budget = None
    if "--budget-sec" in sys.argv:
        budget = float(sys.argv[sys.argv.index("--budget-sec") + 1])
    try:
        census = json.load(open(CENSUS))
    except Exception:
        census = {"done": {}}
    t0 = time.time()
    for cat, cat_label in CATS:
            for sid, slabel in SUBJECTS[cat]:
                code = re.search(r"\((\w+)\)", slabel)
                key = code.group(1) if code else slabel
                if only and key not in only:
                    continue
                skey = f"{cat}:{sid}"
                if key_filter and skey != key_filter:
                    continue
                if skey in census["done"] and not census["done"][skey].get("error") and not key_filter:
                    print(f"[census] skip done {skey} {slabel}", flush=True)
                    continue
                if budget is not None and time.time() - t0 > budget:
                    print("[census] budget reached, exiting cleanly", flush=True)
                    break
                print(f"[census] == {cat_label} / {slabel} ({skey})", flush=True)
                c = ExamMateClient(restore_state=False, verbose=False)
                try:
                    rec = census_one(c, cat, cat_label, sid, slabel)
                except Exception as e:
                    rec = {"cat": cat, "category": cat_label,
                           "subjectID": sid, "subject": slabel,
                           "error": f"{type(e).__name__}: {e}"[:200]}
                census["done"][skey] = rec
                json.dump(census, open(CENSUS, "w"), indent=1, ensure_ascii=False)
                print(f"    badge={rec.get('badge_total')} "
                      f"pager={rec.get('pager_pages')} "
                      f"p1rows={rec.get('page1_rows')} "
                      f"years={rec.get('page1_years')} "
                      f"err={rec.get('error')}", flush=True)
                try:
                    c.close()
                except Exception:
                    pass
                time.sleep(1.0)
    # summary
    tot = 0
    print("\n=== CENSUS SUMMARY (2020-2026) ===")
    for skey, r in sorted(census["done"].items()):
        n = r.get("badge_total") or 0
        tot += n
        print(f"  {r['category']:<12} {r['subject']:<45} "
              f"total={n:>6} pages={max(r.get('pager_pages') or [0]):>3} "
              f"err={r.get('error')}")
    print(f"  TOTAL questions 2020-2026 (badge sum): {tot}")
    print("DONE")


if __name__ == "__main__":
    main()
