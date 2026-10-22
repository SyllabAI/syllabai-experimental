#!/usr/bin/env bash
# TICKET-P5-UGM-PILOT / ADR-UGM-0001 §Decision 3 — weekly UGM link-health job.
# Contract: 3 consecutive failures -> SWAP to stored Wayback snapshot (or HIDE if
# none stored: fail-closed). Origin-dark across the set = ADR early-revisit trigger 1.
# Usage: link-health-check.sh [dir-containing-pilot-links-quadratics.json]
# Exit codes: 0 all ok · 1 actions fired (swap/hide/alert) · 2 usage/IO error
set -u
DIR="${1:-$(cd "$(dirname "$0")" && pwd)}"
JSON="$DIR/pilot-links-quadratics.json"
STATE="$DIR/.pilot-health-state.json"
REPORT_DIR="$DIR/pilot-health"
UA="SyllabAI-pilot-healthcheck/1.0 (ADR-UGM-0001 Mode-2 pilot)"
[ -f "$JSON" ] || { echo "FATAL: $JSON not found" >&2; exit 2; }
mkdir -p "$REPORT_DIR"
DATE=$(date -u +%Y-%m-%d)
REPORT="$REPORT_DIR/$DATE.txt"
RAW="$(mktemp)"

# probe every link (curl handles redirects/TLS; python handles all logic once, after)
slugs=$(python3 -c "import json,sys;[print(l['slug']) for l in json.load(open(sys.argv[1]))['links']]" "$JSON")
for slug in $slugs; do
  url=$(python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(next(l['url'] for l in d['links'] if l['slug']=='$slug'))" "$JSON")
  code=$(curl -s -o /dev/null -w "%{http_code}" -I -L --max-time 10 -A "$UA" "$url" 2>/dev/null || echo "000")
  echo "$slug $code" >> "$RAW"
  sleep 0.5
done

python3 - "$JSON" "$STATE" "$REPORT" "$RAW" <<'PY'
import json, sys
json_path, state_path, report_path, raw_path = sys.argv[1:5]
d = json.load(open(json_path))
try: state = json.load(open(state_path))
except Exception: state = {}
meta = {l["slug"]: l for l in d["links"]}
rows = [ln.split() for ln in open(raw_path) if ln.strip()]
report, actions, ok_count, dark = [], 0, 0, 0
report.append(f"# UGM pilot link-health report {report_path.split('/')[-1][:-4]} (UTC)")
report.append(f"# probed {len(rows)} links; law: 3 consecutive fails -> SWAP (or HIDE if no snapshot)")
for slug, code in rows:
    ok = code in ("200", "301", "302")
    entry = state.setdefault(slug, {})
    if ok:
        entry["fails"] = 0; ok_count += 1
        report.append(f"OK   {slug} {code}")
    else:
        nf = entry.get("fails", 0) + 1
        entry["fails"] = nf
        report.append(f"FAIL {slug} {code} (consecutive: {nf})")
        if nf >= 3:
            snap = meta[slug].get("waybackSnapshotUrl")
            if snap:
                report.append(f"SWAP {slug} -> {snap}  (live retried weekly; swap back on recovery)")
            else:
                report.append(f"HIDE {slug}  (no stored snapshot — fail-closed; run wayback-bootstrap for this link)")
            report.append(f"ALERT owner: {slug} failed 3 consecutive weekly checks (HTTP {code})")
            actions += 1
if rows and ok_count == 0:
    dark = 1
    report.append("TRIGGER-1: origin dark across the whole set — force ADR-UGM-0001 early-revisit trigger 1 to the operator")
report.append(f"# summary: {ok_count}/{len(rows)} ok; actions={actions}")
json.dump(state, open(state_path, "w"), indent=1)
open(report_path, "w").write("\n".join(report) + "\n")
print("\n".join(report))
sys.exit(1 if (actions or dark) else 0)
PY
rc=$?
rm -f "$RAW"
exit $rc
