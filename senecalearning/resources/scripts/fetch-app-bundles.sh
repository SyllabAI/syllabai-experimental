#!/usr/bin/env bash
# Reproduce the Seneca app-bundle capture (Phase 1, 2026-10-22).
# Fetches the SPA shell, extracts the JS chunk graph, downloads all chunks
# into resources/captures/js/ (git-ignored), and re-runs path extraction.
# Polite: static CDN assets, parallelism 8, descriptive UA.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CAP="$HERE/../captures"
JS="$CAP/js"
UA="Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0 (SyllabAI-research-contact-research@syllabai)"
mkdir -p "$JS"

echo "[1/3] shell + entry chunks"
curl -s --compressed "https://app.senecalearning.com/" -H "User-Agent: $UA" -o "$JS/index.html"
ENTRY=$(grep -oE '/assets/index-[A-Za-z0-9_-]+\.js' "$JS/index.html" | head -1)
ROUTES=$(grep -oE '/assets/routes-[A-Za-z0-9_-]+\.js' "$JS/index.html" | head -1)
curl -s --compressed "https://app.senecalearning.com$ENTRY"  -H "User-Agent: $UA" -o "$JS/$(basename "$ENTRY")"
curl -s --compressed "https://app.senecalearning.com$ROUTES" -H "User-Agent: $UA" -o "$JS/$(basename "$ROUTES")"

echo "[2/3] chunk graph + fetch"
grep -ohE 'assets/[a-zA-Z0-9_.-]+\.js' "$JS/$(basename "$ENTRY")" "$JS/$(basename "$ROUTES")" | sort -u > "$CAP/chunk-list.txt"
wc -l "$CAP/chunk-list.txt"
python3 "$(dirname "$HERE")/../../../../../scripts/seneca_fetch_chunks.py" 2>/dev/null || \
  echo "extraction script lives in the SyllabAI workspace; run seneca_fetch_chunks.py manually"

echo "[3/3] done — js corpus stays local (git-ignored)"
