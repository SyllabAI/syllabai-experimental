#!/usr/bin/env python3
"""Pre-harvest probes (session 7):
1. token sanity: GET assignments service (teacher) — expect 200 with a list
2. vocabulary resource-type probe on 3 subjects — decides whether the
   full harvest gains a 4th resource type (matrix from session 3 lacked it)
Prints only counts/statuses — never the token.
"""
import json, subprocess, time, uuid, pathlib, sys

TOK = pathlib.Path("/tmp/seneca_token.txt").read_text().strip()
CID = f"{int(time.time()*1000)}::{uuid.uuid4()}"
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0 (SyllabAI-research)"
TUTOR = "https://tutor-resources.app.senecalearning.com/api/v2/query-resources"
SUBJ = "8c71d055-ff40-4536-8629-5073c618ea53"
META = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3/metadata")


def curl(method, url, body=None, extra=()):
    cmd = ["curl", "-s", "-m", "40", "--compressed", "-X", method, url,
           "-H", f"correlationId: {CID}", "-H", f"access-key: {TOK}",
           "-H", f"User-Agent: {UA}", "-H", "user-region: GB",
           "-H", "Origin: https://app.senecalearning.com",
           "-H", "Accept: application/json, text/plain, */*", "-w",
           "\n---STATUS:%{http_code}---"]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]
    cmd += list(extra)
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout
    status = out.rsplit("---STATUS:", 1)[-1].split("---")[0] if "---STATUS:" in out else "?"
    txt = out.rsplit("\n---STATUS:", 1)[0]
    time.sleep(1.0)
    return status, txt


def subject_id(name):
    for t in json.loads((META / "tags-taxonomy.json").read_text())["tags"]:
        if t.get("semanticCategory") == "subject" and t["text"] == name:
            return t["id"]
    raise KeyError(name)


# 1. token sanity — assignments list (light)
s, txt = curl("GET", "https://assignments.app.senecalearning.com/api/teacher/me/assignments")
n = len(json.loads(txt)) if s.startswith("2") and txt.strip() else None
print(f"[1] teacher assignments: {s} (items={n})")

# 2. vocabulary probe on 3 subjects of different sizes
for subj in ("French", "Maths", "Biology"):
    body = {"query": "", "filters": {"tags": {SUBJ: [subject_id(subj)]}},
            "resourceFilters": [{"type": "vocabulary", "must": {}}],
            "from": 0, "size": 1, "aggregatePublishers": False,
            "aggregateResourceTypes": False,
            "aggregateExamQuestionMarksTotal": False,
            "globalAggregations": False}
    s, txt = curl("POST", TUTOR, body)
    head = ""
    if s.startswith("2"):
        d = json.loads(txt)
        head = f"total={d.get('total')}"
    else:
        head = txt[:120].replace("\n", " ")
    print(f"[2] vocabulary probe {subj}: {s} {head}")
