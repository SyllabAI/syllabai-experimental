#!/usr/bin/env python3
"""Session 7 probes part 2: vocabulary shape, pdf-type count, assignments peek.
All output = counts/shapes only; raw payloads -> LOCAL_ONLY dir."""
import json, subprocess, time, uuid, pathlib

TOK = pathlib.Path("/tmp/seneca_token.txt").read_text().strip()
CID = f"{int(time.time()*1000)}::{uuid.uuid4()}"
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0 (SyllabAI-research)"
LOCAL = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3/local-only-full-payloads")
SUBJ = "8c71d055-ff40-4536-8629-5073c618ea53"
META = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3/metadata")


def curl(method, url, body=None, save=None):
    cmd = ["curl", "-s", "-m", "40", "--compressed", "-X", method, url,
           "-H", f"correlationId: {CID}", "-H", f"access-key: {TOK}",
           "-H", f"User-Agent: {UA}", "-H", "user-region: GB",
           "-H", "Origin: https://app.senecalearning.com",
           "-H", "Accept: application/json, text/plain, */*", "-w",
           "\n---STATUS:%{http_code}---"]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout
    status = out.rsplit("---STATUS:", 1)[-1].split("---")[0] if "---STATUS:" in out else "?"
    txt = out.rsplit("\n---STATUS:", 1)[0]
    if save:
        (LOCAL / save).write_text(txt)
    time.sleep(1.0)
    return status, txt


def subject_id(name):
    for t in json.loads((META / "tags-taxonomy.json").read_text())["tags"]:
        if t.get("semanticCategory") == "subject" and t["text"] == name:
            return t["id"]
    raise KeyError(name)


# 1. vocabulary shape (course = Science Double Award Chemistry Edexcel iGCSE)
s, txt = curl("GET", "https://course.app.senecalearning.com/api/courses/ce0bd53d-5588-4b5c-948d-2b8517097cab/vocabulary?limit=100",
              save="vocab-da-chem-p0.json")
if s.startswith("2"):
    d = json.loads(txt)
    if isinstance(d, dict):
        print(f"[1] vocabulary: {s} keys={list(d.keys())[:8]} total={d.get('total')}")
        lists = d.get("lists") or d.get("items") or []
    else:
        print(f"[1] vocabulary: {s} array len={len(d)}")
        lists = d
    if lists:
        one = lists[0]
        print("    item keys:", list(one.keys())[:12] if isinstance(one, dict) else type(one))
else:
    print(f"[1] vocabulary: {s} {txt[:120]}")

# 2. pdf-type count for two subjects
for subj in ("Chemistry", "Maths"):
    body = {"query": "", "filters": {"tags": {SUBJ: [subject_id(subj)]}},
            "resourceFilters": [{"type": "pdf", "must": {}}],
            "from": 0, "size": 1, "aggregatePublishers": False,
            "aggregateResourceTypes": False,
            "aggregateExamQuestionMarksTotal": False,
            "globalAggregations": False}
    s, txt = curl("POST", "https://tutor-resources.app.senecalearning.com/api/v2/query-resources", body)
    tot = json.loads(txt).get("total") if s.startswith("2") else txt[:100]
    print(f"[2] pdf-type {subj}: {s} total={tot}")

# 3. assignments peek (read-only; statuses only)
s, txt = curl("GET", "https://assignments.app.senecalearning.com/api/teacher/me/assignments")
if s.startswith("2"):
    d = json.loads(txt)
    for a in (d if isinstance(d, list) else d.get("items", []))[:5]:
        print(f"[3] assignment id={a.get('id','?')[:8]}… name={str(a.get('name'))[:40]!r} status={a.get('status')} archived={a.get('archived')} classes={len(a.get('classes', []))}")
else:
    print(f"[3] assignments: {s} {txt[:120]}")
