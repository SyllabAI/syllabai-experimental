#!/usr/bin/env python3
"""Seneca Resource Hub — focused metadata downloads (phase 2 s3, contd).

1. Chemistry (SyllabAI Cycle-1 focus): ALL resources, 3 types, paginated.
2. Every other subject: first-page (200) metadata sample for coverage.
Full payloads -> LOCAL_ONLY (content bodies stay out of the repo).
Metadata-only JSONL -> metadata/ for commit.
"""
import json, subprocess, time, pathlib

TOK = pathlib.Path("/tmp/seneca_token.txt").read_text().strip()
CID = "1792627721745::37836ca6-34af-4d0e-a5f7-8f83a3f45c71"
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0 (SyllabAI-research)"
BASE = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3")
LOCAL = BASE / "local-only-full-payloads"
META = BASE / "metadata"
LOCAL.mkdir(parents=True, exist_ok=True)
META.mkdir(parents=True, exist_ok=True)
TUTOR = "https://tutor-resources.app.senecalearning.com/api/v2/query-resources"
SUBJ = "8c71d055-ff40-4536-8629-5073c618ea53"

matrix = json.loads((META / "subject-type-count-matrix.json").read_text())
subjects = {}
for t in json.loads((META / "tags-taxonomy.json").read_text())["tags"]:
    if t.get("semanticCategory") == "subject":
        subjects[t["text"]] = t["id"]

def call(body, save=None):
    cmd = ["curl", "-s", "-m", "40", "--compressed", "-X", "POST", TUTOR,
           "-H", f"correlationId: {CID}", "-H", "Content-Type: application/json",
           "-H", f"access-key: {TOK}", "-H", f"User-Agent: {UA}",
           "-H", "user-region: GB",
           "-H", "Origin: https://app.senecalearning.com",
           "-d", json.dumps(body), "-w", "\n---STATUS:%{http_code}---"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout
    status = out.rsplit("---STATUS:", 1)[-1].split("---")[0] if "---STATUS:" in out else "?"
    txt = out.rsplit("\n---STATUS:", 1)[0]
    if save:
        (LOCAL / save).write_text(txt)
    time.sleep(0.8)
    return status, txt

def to_row(src):
    return {
        "id": src.get("id"), "type": src.get("type"), "title": src.get("title"),
        "region": src.get("region"), "timeCreated": src.get("timeCreated"),
        "questionType": src.get("questionType"), "publisher": src.get("publisher"),
        "marksTotal": src.get("marksTotal"), "answerCount": src.get("answerCount"),
        "difficulty": src.get("difficulty"),
        "courseIds": (src.get("meta") or {}).get("courseIds"),
        "topicBreadcrumbs": src.get("topicBreadcrumbs"),
        "tagValues": {k: sorted(t.get("value") for t in v)
                      for k, v in (src.get("tags") or {}).items()},
    }

def dl(subject_name, subject_id, rtype, full=True, sample=200):
    rows, frm, total = [], 0, None
    slug = subject_name.replace(' ', '_').replace('/', '-')
    while True:
        save = f"{slug}-{rtype}-{frm:06d}.json"
        p = LOCAL / save
        if p.exists() and p.stat().st_size > 2:
            txt = p.read_text()
            s = "200"
        else:
            body = {"query": "", "filters": {"tags": {SUBJ: [subject_id]}},
                    "resourceFilters": [{"type": rtype, "must": {}}],
                    "from": frm, "size": 200, "aggregatePublishers": False,
                    "aggregateResourceTypes": False,
                    "aggregateExamQuestionMarksTotal": False,
                    "globalAggregations": False}
            s, txt = call(body, save=save)
        if not s.startswith("2"):
            print(f"   {subject_name}/{rtype}@{frm}: {s} STOP"); break
        d = json.loads(txt)
        total = d.get("total", total)
        items = d.get("items", [])
        rows += [to_row(it.get("_source", {})) for it in items]
        frm += len(items)
        if not items or frm >= (total or 0) or (not full and frm >= sample) or len(items) < 200:
            break
    return rows, total

all_rows = []
# 1. Chemistry full
chem_id = subjects["Chemistry"]
for rtype in ("courseSection", "examQuestion", "quiz"):
    rows, total = dl("Chemistry", chem_id, rtype, full=True)
    print(f"Chemistry/{rtype}: {len(rows)} rows (total={total})")
    all_rows += rows
(META / "chemistry-resources-metadata.jsonl").write_text(
    "\n".join(json.dumps(r) for r in all_rows))
print(f"CHEMISTRY DONE rows={len(all_rows)}")

# 2. other subjects: 200-row sample
others = {}
for name, sid in sorted(subjects.items()):
    if name == "Chemistry":
        continue
    srows = []
    for rtype in ("courseSection", "examQuestion", "quiz"):
        rows, _t = dl(name, sid, rtype, full=False, sample=200)
        srows += rows
    if srows:
        others[name] = srows
        print(f"sample {name}: {len(srows)}")
sample_rows = [r for v in others.values() for r in v]
(META / "all-subjects-sample-metadata.jsonl").write_text(
    "\n".join(json.dumps(r) for r in sample_rows))
print(f"SAMPLES DONE rows={len(sample_rows)} subjects={len(others)}")
