#!/usr/bin/env python3
"""Rebuild the two committed metadata JSONLs from the cached full
payloads, applying the title rule:

  - courseSection / quiz rows: keep `title` (structural names)
  - examQuestion rows: DROP `title` (title == plain-text question stem
    == content body; bulk stems are not metadata). Keep id/tags/
    breadcrumbs/marks/counts for structure analysis.

No network needed — reads the local-only cached pages.
"""
import json, pathlib

BASE = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3")
LOCAL = BASE / "local-only-full-payloads"
META = BASE / "metadata"
RH = pathlib.Path("/home/z/my-project/work/seneca-recon/syllabai-experimental/senecalearning/resources/captures/resource-hub")
SUBJ = "8c71d055-ff40-4536-8629-5073c618ea53"

def to_row(src):
    rtype = src.get("type")
    keep_title = rtype in ("courseSection", "quiz")
    return {
        "id": src.get("id"), "type": rtype,
        "title": src.get("title") if keep_title else None,
        "region": src.get("region"), "timeCreated": src.get("timeCreated"),
        "questionType": src.get("questionType"), "publisher": src.get("publisher"),
        "marksTotal": src.get("marksTotal"), "answerCount": src.get("answerCount"),
        "difficulty": src.get("difficulty"),
        "courseIds": (src.get("meta") or {}).get("courseIds"),
        "topicBreadcrumbs": src.get("topicBreadcrumbs"),
        "tagValues": {k: sorted(t.get("value") for t in v)
                      for k, v in (src.get("tags") or {}).items()},
    }

subjects = {}
for t in json.loads((META / "tags-taxonomy.json").read_text())["tags"]:
    if t.get("semanticCategory") == "subject":
        subjects[t["text"]] = t["id"]

def collect(slug_prefix, subject_id, rtype, full, sample):
    rows, frm = [], 0
    while True:
        p = LOCAL / f"{slug_prefix}-{rtype}-{frm:06d}.json"
        if not p.exists() or p.stat().st_size <= 2:
            break
        d = json.loads(p.read_text())
        items = d.get("items", [])
        rows += [to_row(it.get("_source", {})) for it in items]
        frm += len(items)
        if not items or frm >= d.get("total", 0) or (not full and frm >= sample) or len(items) < 200:
            break
    return rows

# chemistry full
chem_rows = []
for rtype in ("courseSection", "examQuestion", "quiz"):
    chem_rows += collect("Chemistry", subjects["Chemistry"], rtype, True, 200)
(RH / "chemistry-resources-metadata.jsonl").write_text(
    "\n".join(json.dumps(r) for r in chem_rows))
from collections import Counter
c = Counter(r["type"] for r in chem_rows)
print("chemistry:", dict(c), "titles kept for", c["courseSection"] + c["quiz"])

# samples for other subjects
sample_rows = []
for name, sid in sorted(subjects.items()):
    if name == "Chemistry":
        continue
    for rtype in ("courseSection", "examQuestion", "quiz"):
        sample_rows += collect(name.replace(' ', '_').replace('/', '-'), sid, rtype, False, 200)
(RH / "all-subjects-sample-metadata.jsonl").write_text(
    "\n".join(json.dumps(r) for r in sample_rows))
print("samples:", dict(Counter(r["type"] for r in sample_rows)))
print("DONE")
