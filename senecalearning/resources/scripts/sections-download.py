#!/usr/bin/env python3
"""Download the full section tree for all 'Chemistry: Edexcel iGCSE' family
courses via course-entities-v2 ES (queryCourses types=[section])."""
import json, subprocess, time, pathlib

TOK = pathlib.Path("/tmp/seneca_token.txt").read_text().strip()
CID = "1792627721745::37836ca6-34af-4d0e-a5f7-8f83a3f45c71"
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0 (SyllabAI-research)"
OUT = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3")
(OUT / "local-only-full-payloads").mkdir(parents=True, exist_ok=True)
QC = "https://course.app.senecalearning.com/api/courses/queryCourses"

def call(body, save=None):
    cmd = ["curl", "-s", "-m", "30", "--compressed", "-X", "POST", QC,
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
        (OUT / "local-only-full-payloads" / save).write_text(txt)
    time.sleep(0.8)
    return status, txt

sections, frm, total = [], 0, None
while True:
    body = {"query": "Chemistry: Edexcel iGCSE >", "types": ["section"],
            "from": frm, "size": 200}
    s, txt = call(body, save=f"sections-igcse-chem-{frm:05d}.json")
    if not s.startswith("2"):
        print("status", s, "at", frm); break
    d = json.loads(txt)
    total = d.get("results", {}).get("total", total)
    hits = d.get("results", {}).get("hits", [])
    sections += [h["_source"] for h in hits]
    frm += len(hits)
    print(f"  @ {frm}/{total}")
    if not hits or frm >= (total or 0):
        break

# dedupe by id, keep all fields except nothing — all metadata
uniq = {s["id"]: s for s in sections if s.get("id")}
# also pull the course family records (query without '>')
cs, frm2, tot2 = [], 0, None
while True:
    body = {"query": "Chemistry: Edexcel iGCSE", "types": ["course"],
            "from": frm2, "size": 50}
    s, txt = call(body, save=f"courses-igcse-chem-{frm2:05d}.json")
    if not s.startswith("2"):
        print("course status", s); break
    d = json.loads(txt)
    tot2 = d.get("results", {}).get("total", tot2)
    hits = d.get("results", {}).get("hits", [])
    cs += [h["_source"] for h in hits]
    frm2 += len(hits)
    if not hits or frm2 >= (tot2 or 0):
        break
courses = {c["id"]: c for c in cs if c.get("id")}

(OUT / "metadata" / "edexcel-igcse-chemistry-sections.json").write_text(
    json.dumps({"count": len(uniq), "sections": list(uniq.values())}, indent=1))
(OUT / "metadata" / "edexcel-igcse-chemistry-courses.json").write_text(
    json.dumps({"count": len(courses), "courses": list(courses.values())}, indent=1))
print(f"DONE sections={len(uniq)} courses={len(courses)}")
