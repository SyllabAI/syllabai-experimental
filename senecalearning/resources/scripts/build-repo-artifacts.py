#!/usr/bin/env python3
"""Build the committed, organized + categorized repo artifacts from rh3
probe results. Metadata-only, redacted, documented."""
import json, pathlib, csv, io, datetime

SRC = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3")
LOCAL = SRC / "local-only-full-payloads"
META = SRC / "metadata"
REPO = pathlib.Path("/home/z/my-project/work/seneca-recon/syllabai-experimental/senecalearning/resources/captures")
RH = REPO / "resource-hub"
ASG = REPO / "assignments"
RH.mkdir(parents=True, exist_ok=True)
ASG.mkdir(parents=True, exist_ok=True)

# ---------- 1. tidy count matrix ----------
raw = json.loads((META / "subject-type-count-matrix.json").read_text())
rows = []
for subj, agg in raw.items():
    rt = (agg.get("resourceTypes") or {})
    counts = {"courseSection": 0, "examQuestion": 0, "quiz": 0}
    for b in (rt.get("filtered") or {}).get("buckets", []):
        if b.get("key") in counts:
            counts[b["key"]] = b["doc_count"]
    total = rt.get("doc_count", 0)
    rows.append({"subject": subj, **counts, "total": total})
rows.sort(key=lambda r: -r["total"])
with (RH / "subject-resource-counts.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["subject", "courseSection", "examQuestion", "quiz", "total"])
    w.writeheader(); w.writerows(rows)
grand = sum(r["total"] for r in rows)
print(f"count matrix: {len(rows)} subjects, grand total {grand}")

# ---------- 2. tag taxonomy slim ----------
tags = json.loads((META / "tags-taxonomy.json").read_text())["tags"]
slim = [{"id": t.get("id"), "text": t.get("text"),
         "semanticCategory": t.get("semanticCategory"),
         "parentId": t.get("parentId"), "subjectGroup": t.get("subjectGroup"),
         "aliases": (t.get("details") or {}).get("aliases") if isinstance(t.get("details"), dict) else None}
        for t in tags]
(RH / "tags-taxonomy-slim.json").write_text(json.dumps(slim, indent=1))
from collections import Counter
print("tag categories:", Counter(t["semanticCategory"] for t in slim))

# ---------- 3. copy the two big metadata jsonl ----------
for name in ("chemistry-resources-metadata.jsonl", "all-subjects-sample-metadata.jsonl"):
    (RH / name).write_text((META / name).read_text())

# ---------- 4. edexcel igcse chemistry structure ----------
secs = json.loads((META / "edexcel-igcse-chemistry-sections.json").read_text())
courses = json.loads((META / "edexcel-igcse-chemistry-courses.json").read_text())
# slim: drop heavy nothing; these are already metadata-only
(RH / "edexcel-igcse-chemistry-sections.json").write_text(json.dumps(secs, indent=1))
(RH / "edexcel-igcse-chemistry-courses.json").write_text(json.dumps(courses, indent=1))
# build a readable section tree for the main Free course
main = next(c for c in courses["courses"] if c.get("id") == "967b4370-21e8-11e8-8c0c-d79041e9c8a6")
smain = [s for s in secs["sections"] if s.get("parentId") == main["id"]]
smain.sort(key=lambda s: int(s.get("sectionNumber", 0)) if str(s.get("sectionNumber", "")).isdigit() else 999)
tree = [{"num": s.get("sectionNumber"), "id": s["id"], "title": s.get("title"),
         "level": s.get("sectionLevel"),
         "children": [{"id": c["id"], "title": c.get("title"), "level": c.get("sectionLevel")}
                      for c in sorted([x for x in secs["sections"] if x.get("parentId") == s["id"]],
                                      key=lambda x: str(x.get("sectionNumber", "")))]}
        for s in smain]
(RH / "edexcel-igcse-chemistry-section-tree.json").write_text(json.dumps({
    "courseId": main["id"], "courseTitle": main.get("title"),
    "subscriptionTier": main.get("subscriptionTier"), "sections": tree}, indent=1))
print(f"edexcel igcse: {len(smain)} top sections in main course; tree built")

# ---------- 5. assignment exemplars (redacted) ----------
create_req = {
    "name": "SyllabAI Research - structural probe (draft)",
    "spec": {"tasks": [
        {"id": "242377c1-835e-4ac9-a755-46942035b181", "taskType": "resource",
         "resourceType": "exam-question", "courseId": "4c2bb850-1d46-11e8-840a-ed991cd3461d"},
        {"id": "bd04e8be-7780-4e80-94f2-c74ec58f1852", "taskType": "resource",
         "resourceType": "exam-question", "courseId": "4c2bb850-1d46-11e8-840a-ed991cd3461d"}]},
    "autoEnrolNewUsers": True,
    "classes": [{"classId": "s11w5yatia",
                 "startDate": "2026-10-22T00:30:00.767Z",
                 "dueDate": "2026-10-29T00:45:00.767Z"}]}
(ASG / "assignment-create-request.json").write_text(json.dumps(create_req, indent=1))

create_resp = {
    "assignmentId": "cd2cc906-fc2a-4c5b-b72d-45242d29ba18",
    "assignmentName": "SyllabAI Research - structural probe (draft)",
    "autoEnrolNewUsers": True,
    "creatorId": "<REDACTED-userId>",
    "timeCreated": "2026-10-22T00:42:39.215Z",
    "timeUpdated": "2026-10-22T00:42:39.215Z",
    "spec": create_req["spec"],
    "classIds": ["s11w5yatia"],
    "numAssignees": 0}
(ASG / "assignment-create-response.json").write_text(json.dumps(create_resp, indent=1))

class_view = {
    "startDate": "2026-10-22T00:30:00.767Z",
    "dueDate": "2026-10-29T00:45:00.767Z",
    "classId": "s11w5yatia",
    "id": "cd2cc906-fc2a-4c5b-b72d-45242d29ba18",
    "numAssignees": 0,
    "timeCreated": "2026-10-22T00:42:39.215Z",
    "timeUpdated": "2026-10-22T00:44:55.859Z",
    "archived": False,
    "name": "SyllabAI Research - structural probe (draft)",
    "spec": create_req["spec"],
    "creatorId": "<REDACTED-userId>",
    "autoEnrolNewUsers": True,
    "assignees": [],
    "assignmentCutoffDate": "2026-11-12T00:45:00+00:00",
    "sectionAggregations": [],
    "contentAggregations": [],
    "questionAggregations": {"questions": [], "marksTotal": 0, "averageMark": 0},
    "totalAggregations": {"completionRate": 0, "averageScore": 0, "bestScore": 0,
                          "averageStudyTime": 0, "totalCompleted": 0},
    "teacherName": "Nawaf Sir"}
(ASG / "assignment-class-view-with-stats.json").write_text(json.dumps(class_view, indent=1))

update_req = {"startDate": "2026-10-22T00:30:00.767Z", "dueDate": "2026-10-29T00:45:00.767Z",
              "name": "SyllabAI Research - structural probe (draft)", "assignees": [],
              "spec": create_req["spec"], "autoEnrolNewUsers": True}
(ASG / "assignment-update-request.json").write_text(json.dumps(update_req, indent=1))
print("assignment exemplars written")
print("DONE")
