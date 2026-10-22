"""Harvest per-subject filter metadata (topics/zones/papers/seasons/years) for
ALL subjects via deep-link page loads (quota-free — no list-serving calls).

Also fixes the catalog's subject lists for every category from the fresh page.
"""
import json, os, re, sys, time
sys.path.insert(0, "/home/z/my-project/scripts")
from exam_mate_client import ExamMateClient

BASE = "/home/z/my-project/syllabai-experimental/exam-mate/resources/topical_papers"
CATALOG = f"{BASE}/catalog.json"
ORIGIN = "https://www.exam-mate.com"

HARVEST_JS = r"""
() => ({
  topics: Array.from(document.querySelectorAll('input[name="topics[]"]'))
    .map(i => ({v: i.value, n: i.getAttribute('data-name')})),
  chapters: Array.from(document.querySelectorAll('input[name="chapterIDs[]"], input[name="chapters[]"]'))
    .map(i => ({v: i.value, n: i.getAttribute('data-name')})),
  zones: Array.from(document.querySelectorAll('input[name="zones[]"]'))
    .map(i => ({v: i.value, n: i.getAttribute('data-name') || i.value})),
  papers: Array.from(document.querySelectorAll('input[name="papers[]"]'))
    .map(i => ({v: i.value, n: i.getAttribute('data-name')})),
  seasons: Array.from(document.querySelectorAll('input[name="seasons[]"]'))
    .map(i => ({v: i.value, n: i.getAttribute('data-name')})),
  years: Array.from(document.querySelectorAll('input[name="years[]"]')).map(i => i.value),
  subjects: Array.from(document.querySelectorAll('*'))
    .filter(el => (el.getAttribute('wire:click') || '').includes("$set('subjectID'"))
    .map(el => {
      const m = el.getAttribute('wire:click').match(/subjectID',\s*(\d+)/);
      return {id: m ? parseInt(m[1]) : null, label: el.textContent.trim().replace(/\s+/g, ' ').slice(0, 80)};
    }).filter(x => x.id),
})
"""


def slug(label):
    return re.sub(r"\s+", "_", label.strip())


def main():
    cat = json.load(open(CATALOG))
    out_path = f"{BASE}/subject_taxonomy.json"
    tax = json.load(open(out_path)) if os.path.exists(out_path) else {}
    c = ExamMateClient()
    n_done = 0
    try:
        for category in cat["categories"]:
            cid, clabel = category["id"], category["label"]
            # subjects: from catalog (which may hold stale lists for 5/6/7) —
            # re-read the true list from THIS category's deep-link page
            url = f"{ORIGIN}/topicalpastpapers/{slug(clabel)}-{cid}"
            c.page.goto(url, wait_until="domcontentloaded", timeout=60000)
            w = 0
            while "moment" in (c.page.title() or "").lower() and w < 25:
                time.sleep(2); w += 2
            time.sleep(2.2)
            st = c.page.evaluate(HARVEST_JS)
            subjects = st["subjects"]
            if subjects:
                cat.setdefault("subjects_by_category", {})[str(cid)] = subjects
            print(f"[{clabel}-{cid}] {len(subjects)} subjects")
            for subj in subjects:
                sid, slabel = subj["id"], subj["label"]
                key = f"{cid}_{sid}"
                if key in tax:
                    continue
                surl = f"{ORIGIN}/topicalpastpapers/{slug(clabel)}-{cid}/{slug(slabel)}-{sid}"
                try:
                    c.page.goto(surl, wait_until="domcontentloaded", timeout=60000)
                    w = 0
                    while "moment" in (c.page.title() or "").lower() and w < 25:
                        time.sleep(2); w += 2
                    time.sleep(2.0)
                    st2 = c.page.evaluate(HARVEST_JS)
                    tax[key] = {
                        "categoryID": cid, "category": clabel,
                        "subjectID": sid, "subject": slabel,
                        "url": f"/topicalpastpapers/{slug(clabel)}-{cid}/{slug(slabel)}-{sid}",
                        "topics": st2["topics"], "chapters": st2["chapters"],
                        "zones": st2["zones"], "papers": st2["papers"],
                        "seasons": st2["seasons"], "years": st2["years"],
                        "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    }
                    n_done += 1
                    nt = len(st2["topics"])
                    print(f"    {sid} {slabel[:44]!r}: {nt} topics, {len(st2['zones'])} zones, {len(st2['years'])} years")
                except Exception as e:
                    print(f"    {sid} {slabel[:40]!r}: ERROR {e}")
                # checkpoint every 5 subjects
                if n_done % 5 == 0:
                    json.dump(tax, open(out_path, "w"), indent=1, ensure_ascii=False)
            json.dump(cat, open(CATALOG, "w"), indent=1, ensure_ascii=False)
    finally:
        json.dump(tax, open(out_path, "w"), indent=1, ensure_ascii=False)
        json.dump(cat, open(CATALOG, "w"), indent=1, ensure_ascii=False)
        print(f"\ntaxonomy entries: {len(tax)} (this run: {n_done})")
        c.close()


if __name__ == "__main__":
    main()
