#!/usr/bin/env python3
"""Seneca Resource Hub metadata downloader — Phase 2 session 3.

Downloads STRUCTURAL/METADATA only, per IP-AND-COPYRIGHT-NOTES.md:
  - tags taxonomy
  - subject x resource-type aggregation matrix
  - Chemistry (focus subject) paginated resource metadata

Full API responses (which contain content bodies such as mark schemes)
are stored OUTSIDE the repo (LOCAL_ONLY dir). Committed artifacts are
metadata-only projections produced by a separate step.
Polite pacing: >=0.8s between requests. Never prints token.
"""
import json, subprocess, time, pathlib, sys

TOK = pathlib.Path("/tmp/seneca_token.txt").read_text().strip()
CID = "1792627721745::37836ca6-34af-4d0e-a5f7-8f83a3f45c71"
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0 (SyllabAI-research)"
OUT = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3")
LOCAL = OUT / "local-only-full-payloads"
META = OUT / "metadata"
LOCAL.mkdir(parents=True, exist_ok=True)
META.mkdir(parents=True, exist_ok=True)

TUTOR = "https://tutor-resources.app.senecalearning.com/api/v2/query-resources"
TAGS = "https://tags.app.senecalearning.com/api/tags?includeNonCourseFilters=true"

def call(url, method="GET", body=None, name=None, save=None):
    cmd = ["curl", "-s", "-m", "40", "--compressed", "-X", method, url,
           "-H", f"correlationId: {CID}", "-H", "Content-Type: application/json",
           "-H", f"access-key: {TOK}", "-H", f"User-Agent: {UA}",
           "-H", "user-region: GB",
           "-H", "Origin: https://app.senecalearning.com",
           "-w", "\n---STATUS:%{http_code}---"]
    if body is not None:
        cmd += ["-d", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout
    status = out.rsplit("---STATUS:", 1)[-1].split("---")[0] if "---STATUS:" in out else "?"
    body_txt = out.rsplit("\n---STATUS:", 1)[0]
    if save:
        (LOCAL / save).write_text(body_txt)
    time.sleep(0.85)
    return status, body_txt

# ---------- 1. tags taxonomy ----------
print("== tags taxonomy ==")
s, tags_txt = call(TAGS, name="tags", save="tags-full.json")
print("   status", s, "len", len(tags_txt))
tags = json.loads(tags_txt)
(META / "tags-taxonomy.json").write_text(json.dumps(tags, indent=1))

# flat tag list: {text, semanticCategory, parentId, id, subjectGroup, region...}
tag_list = tags.get("tags", tags if isinstance(tags, list) else [])
(META / "tags-taxonomy.json").write_text(json.dumps(tags, indent=1))

# semanticCategory -> tag-type id map
sem_cats = {}
for t in tag_list:
    sem_cats.setdefault(t.get("semanticCategory"), t.get("parentId"))
print("   semanticCategories:", {k: v for k, v in sem_cats.items()})

# subject tags: parentId == subject category id
SUBJ = sem_cats.get("subject", "8c71d055-ff40-4536-8629-5073c618ea53")
subjects = {t["text"]: t["id"] for t in tag_list if t.get("semanticCategory") == "subject"}
print(f"   {len(subjects)} subjects")

# ---------- 2. aggregation matrix ----------
print("== aggregation matrix ==")
def agg_query(subject_id, subject_value):
    body = {
        "query": "",
        "filters": {"tags": {SUBJ: [subject_id]}},
        "resourceFilters": [], "from": 0, "size": 0,
        "aggregatePublishers": False, "aggregateResourceTypes": True,
        "aggregateExamQuestionMarksTotal": False, "globalAggregations": False,
    }
    s, txt = call(TUTOR, "POST", body, save=f"agg-{subject_value.replace(' ','_').replace('/','-')}.json")
    if s.startswith("2"):
        d = json.loads(txt)
        return d.get("aggregations") or d.get("resourceTypeAggregations") or {k: d[k] for k in d if "ount" in str(k)}
    return {"_status": s}

matrix = {}
for sv, sid in sorted(subjects.items()):
    if sv in ("Free", "Premium", "Updated", "Standard", "Foundation", "Higher", "Combined", "Triple", "GCSE", "A Level", "KS2", "KS3", "IGCSE", "National Curriculum", "International Baccalaureate"):
        continue
    a = agg_query(sid, sv)
    matrix[sv] = a
    print(f"   {sv}: {json.dumps(a)[:160]}")
(META / "subject-type-count-matrix.json").write_text(json.dumps(matrix, indent=1))
print("saved matrix")

# ---------- 3. Chemistry metadata download ----------
print("== chemistry metadata (paginated) ==")
def page_query(subject_id, rtype, frm, size=200):
    body = {
        "query": "", "filters": {"tags": {SUBJ: [subject_id]}},
        "resourceFilters": [{"type": rtype, "must": {}}],
        "from": frm, "size": size,
        "aggregatePublishers": False, "aggregateResourceTypes": False,
        "aggregateExamQuestionMarksTotal": False, "globalAggregations": False,
    }
    s, txt = call(TUTOR, "POST", body)
    return s, txt

CHEM = subjects.get("Chemistry")
if not CHEM:
    print("!! Chemistry tag id not found; aborting chem download"); sys.exit(1)

RESOURCE_TYPES = [("coreContent", "core-content"), ("examQuestion", "exam-question"), ("quiz", "quiz")]
rows = []
for rtype, _slug in RESOURCE_TYPES:
    frm, total, guard = 0, None, 0
    while True:
        s, txt = page_query(CHEM, rtype, frm)
        if not s.startswith("2"):
            print(f"   {rtype}@{frm}: status {s} — stop"); break
        d = json.loads(txt)
        total = d.get("count", total)
        items = d.get("items", [])
        (LOCAL / f"chem-{rtype}-{frm:06d}.json").write_text(txt)
        for it in items:
            src = it.get("_source", {})
            tb = src.get("topicBreadcrumbs", "")
            rows.append({
                "id": src.get("id"), "type": src.get("type"),
                "title": src.get("title"), "region": src.get("region"),
                "timeCreated": src.get("timeCreated"),
                "questionType": src.get("questionType"),
                "publisher": src.get("publisher"),
                "marksTotal": src.get("marksTotal"),
                "answerCount": src.get("answerCount"),
                "difficulty": src.get("difficulty"),
                "courseIds": (src.get("meta") or {}).get("courseIds"),
                "topicBreadcrumbs": tb,
                "tagValues": {k: [t.get("value") for t in v] for k, v in (src.get("tags") or {}).items()},
            })
        print(f"   {rtype}@{frm}: +{len(items)} (total={total})")
        frm += len(items)
        if not items or frm >= (total or 0):
            break
        guard += 1
        if guard > 90:
            print("   guard stop"); break

(META / "chemistry-resources-metadata.jsonl").write_text(
    "\n".join(json.dumps(r) for r in rows))
print(f"DONE chemistry rows={len(rows)}")
