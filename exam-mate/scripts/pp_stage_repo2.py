#!/usr/bin/env python3
"""Stage a harvested subject into repo 2 (syllabai-experimental-2) and push.

Layout:
  exam-mate/resources/past_papers/MANIFEST.md                      (appended)
  exam-mate/resources/past_papers/<cat_dir>/<subject_dir>/
      INDEX.jsonl  _summary.json  discovery_rows.json  discovery_urls.json
      <paper_ref_dir>/QP/*.png  MS/*.png  paper.json

Only past_papers paths are staged (repo has unrelated local modifications).
"""
import json, os, re, shutil, subprocess, sys

WORK = "/home/z/my-project/pp_harvest_work"
REPO2 = "/home/z/my-project/syllabai-experimental-2"
CAT_LABEL = {3: "3_IGCSE", 4: "4_IGCSE", 5: "5_A-LEVEL", 6: "6_A-LEVEL",
             7: "7_DIPLOMA", 12: "12_O-LEVEL", 14: "14_GCSE_9-1_", 15: "15_GCSE",
             16: "16_A-LEVEL", 17: "17_A-LEVEL", 18: "18_AS", 19: "19_AS",
             21: "21_IGCSE_9-1_", 11: "11_CHECKPOINT", 20: "20_PRE-U",
             53: "53_TYT_YKS_", 54: "54_AYT_YKS_", 55: "55_YDT_YKS_"}

def sh(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"  !! cmd failed: {cmd}\n{r.stdout[-800:]}\n{r.stderr[-800:]}")
        sys.exit(1)
    return r.stdout.strip()

def main():
    cat, subject = int(sys.argv[1]), int(sys.argv[2])
    label = sys.argv[3]
    work_subj = os.path.join(WORK, f"cat{cat}_subj{subject}")
    summ = json.load(open(os.path.join(work_subj, "_summary.json")))
    cat_dir = CAT_LABEL.get(cat, f"cat{cat}")
    subj_dir = f"{subject}_{label}"
    dest = os.path.join(REPO2, "exam-mate/resources/past_papers", cat_dir, subj_dir)
    os.makedirs(dest, exist_ok=True)

    # copy per-paper trees (pngs + paper.json), skip pdfs if any remain
    n_files = 0
    for pdir in sorted(os.listdir(work_subj)):
        ppath = os.path.join(work_subj, pdir)
        if not os.path.isdir(ppath):
            continue
        ddest = os.path.join(dest, pdir)
        os.makedirs(ddest, exist_ok=True)
        for sub in ("QP", "MS"):
            s = os.path.join(ppath, sub)
            if os.path.isdir(s):
                d = os.path.join(ddest, sub)
                os.makedirs(d, exist_ok=True)
                for f in os.listdir(s):
                    shutil.copy2(os.path.join(s, f), os.path.join(d, f))
                    n_files += 1
        for f in ("paper.json",):
            if os.path.exists(os.path.join(ppath, f)):
                shutil.copy2(os.path.join(ppath, f), os.path.join(ddest, f))
    for f in ("INDEX.jsonl", "_summary.json"):
        if os.path.exists(os.path.join(work_subj, f)):
            shutil.copy2(os.path.join(work_subj, f), os.path.join(dest, f))
    for src, dst in (("rows.json", "discovery_rows.json"),
                     ("paper_urls.json", "discovery_urls.json")):
        if os.path.exists(os.path.join(work_subj, src)):
            shutil.copy2(os.path.join(work_subj, src), os.path.join(dest, dst))

    # subject MANIFEST.md
    papers = sorted(x for x in os.listdir(dest) if os.path.isdir(os.path.join(dest, x)))
    n_qp = sum(1 for r in map(json.loads, open(os.path.join(dest, "INDEX.jsonl")))
               if r["kind"] == "qp" and "q" in r)
    n_ms = sum(1 for r in map(json.loads, open(os.path.join(dest, "INDEX.jsonl")))
               if r["kind"] == "ms" and "q" in r)
    yrs = sorted({m.group(1) for r in map(json.loads, open(os.path.join(dest, "INDEX.jsonl")))
                  for m in [re.search(r"(20\d\d)", r["paper_ref"] or "")] if m})
    with open(os.path.join(dest, "MANIFEST.md"), "w") as f:
        f.write(f"""# past_papers — {label} (subject {subject}, category {cat})

Source: exam-mate.com PAST PAPERS library (full papers, QP + MS PDFs),
harvested {summ.get('generated', '2026-10-23')} via scripts/pp_harvest_2020.py
(anonymous session, in-page fetch downloads, PyMuPDF rasterize @150 dpi +
text-layer question segmentation).

- Papers: {len(papers)} ({' '.join(yrs)})
- Question-segment PNGs: QP {n_qp}, MS {n_ms} (one PNG per segment; multi-page
  questions carry `_cont` continuation segments; page-level PNGs kept only for
  front-matter/undetected pages)
- Per paper: paper.json (source PDF sha256 + URLs + per-segment bbox provenance)
- Cross-check: files_on_disk == INDEX.jsonl entries (see _summary.json)
- Copyright: exam-board copyrighted content via third-party site; research copy
  only, license review required before shipping.
""")

    # repo2 MANIFEST.md top-level: append/refresh subject line
    top = os.path.join(REPO2, "exam-mate/resources/past_papers/MANIFEST.md")
    line = f"| {cat_dir}/{subj_dir} | {label} | {len(papers)} papers | QP {n_qp} + MS {n_ms} segments | {yrs[0]}–{yrs[-1]} |\n"
    if not os.path.exists(top):
        with open(top, "w") as f:
            f.write("# MANIFEST — past_papers dataset (2020–2026 full papers → per-question PNGs)\n\n"
                    "| Subject dir | Label | Papers | Segments | Years |\n|---|---|---|---|---|\n")
    txt = open(top).read()
    if subj_dir not in txt:
        with open(top, "a") as f:
            f.write(line)

    # git: stage ONLY past_papers
    rel = "exam-mate/resources/past_papers"
    sh(f"git add '{rel}'", cwd=REPO2)
    msg = (f"exam-mate past papers: {label} — {len(papers)} papers {yrs[0]}-{yrs[-1]}, "
           f"{n_qp} QP + {n_ms} MS question segments (@150dpi, text-layer split)")
    sh(f"git commit -m {json.dumps(msg)}", cwd=REPO2)
    print(sh("git log --oneline -1", cwd=REPO2))
    if "--no-push" not in sys.argv:
        sh("git pull --rebase origin main", cwd=REPO2)
        sh("git push origin main", cwd=REPO2)
        print("pushed; status:", sh("git status -sb | head -1", cwd=REPO2))
    print(f"staged {n_files} png files -> {rel}/{cat_dir}/{subj_dir}")

if __name__ == "__main__":
    main()
