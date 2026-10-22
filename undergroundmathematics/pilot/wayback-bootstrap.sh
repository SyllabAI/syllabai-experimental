#!/usr/bin/env bash
# TICKET-P5-UGM-PILOT — LAUNCH GATE G1: Wayback bootstrap.
# Captures every pilot link that has no stored snapshot via Save Page Now,
# CDX-verifies the result, writes wayback-bootstrap-results.json for merge.
#
# Run from a normal network (anonymous SPN was unresponsive from the research
# sandbox on 2026-10-22). Recommended: authenticate with a free archive.org
# account:  export WB_AUTH="user:pass"   (S3-style login works for /save).
# Usage: wayback-bootstrap.sh [dir-containing-pilot-links-quadratics.json]
set -u
DIR="${1:-$(cd "$(dirname "$0")" && pwd)}"
JSON="$DIR/pilot-links-quadratics.json"
OUT="$DIR/wayback-bootstrap-results.json"
UA="SyllabAI-pilot-bootstrap/1.0 (ADR-UGM-0001 Mode-2 pilot, launch gate G1)"
[ -f "$JSON" ] || { echo "FATAL: $JSON not found" >&2; exit 2; }

AUTH=(); [ -n "${WB_AUTH:-}" ] && AUTH=(-u "$WB_AUTH")
echo "# wayback bootstrap $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$OUT.raw.log"

python3 - "$JSON" > "$OUT" <<'PY'
import json, subprocess, sys, time, urllib.parse
d = json.load(open(sys.argv[1]))
results = []
todo = [l for l in d["links"] if not l.get("waybackSnapshotUrl")]
print(f"bootstrap needed for {len(todo)}/{len(d['links'])} links", file=sys.stderr)
for i, l in enumerate(todo, 1):
    url = l["url"]
    print(f"[{i}/{len(todo)}] SPN {url}", file=sys.stderr)
    # Save Page Now: GET /save/<url>; slow — be generous, be polite (15s spacing)
    subprocess.run(["curl", "-s", "-L", "-A", UA, "--max-time", "120", *AUTH,
                    f"https://web.archive.org/save/{url}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(15)
    # CDX verify (authoritative index)
    cdx = urllib.parse.quote(url.replace("https://", "").rstrip("/"), safe="")
    r = subprocess.run(["curl", "-s", "--max-time", "30",
                        f"http://web.archive.org/cdx/search/cdx?url={cdx}&output=json&limit=1&filter=statuscode:200"],
                       capture_output=True, text=True)
    ts, snap = None, None
    try:
        rows = json.loads(r.stdout)
        if rows and len(rows) > 1:
            ts = rows[1][1]
            snap = f"https://web.archive.org/web/{ts}/{url}"
    except Exception:
        pass
    results.append({"slug": l["slug"], "url": url, "waybackSnapshotUrl": snap, "waybackTimestamp": ts})
    print(f"    -> {'OK ' + ts if ts else 'MISSING (retry next run)'}", file=sys.stderr)
    time.sleep(5)
json.dump({"generatedAt": time.strftime("%Y-%m-%d"), "results": results},
          open(sys.argv[2] if False else "/dev/stdout", "w"), indent=1)
PY

echo "Done. Results: $OUT"
echo "MERGE (G1 completion): for each result with a snapshot, set waybackSnapshotUrl/waybackTimestamp"
echo "in pilot-links-quadratics.json, commit, and re-run link-health-check.sh (expect all OK)."
echo "Links still MISSING after a second run: raise at the hub sync — do NOT render without a stored fallback."
