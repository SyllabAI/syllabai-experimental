#!/usr/bin/env bash
# Fetch all asset chunks referenced in the main app bundle (public static assets).
set -u
BASE="https://d11xgklg0c0p8q.cloudfront.net/assets"
DIR="/home/z/my-project/syllabai-experimental/znotes/resources/captures/chunks"
mkdir -p "$DIR"
cd /home/z/my-project/syllabai-experimental/znotes/resources/captures
python3 - <<'EOF'
import re
s = open('app-bundle.js', encoding='utf-8', errors='ignore').read()
chunks = sorted(set(re.findall(r'assets/([A-Za-z0-9_.\-]+\.js)', s)))
open('chunk-list.txt', 'w').write('\n'.join(chunks))
print(f'{len(chunks)} chunks listed')
EOF
ok=0; fail=0
while read -r f; do
  if [ ! -s "$DIR/$f" ]; then
    code=$(curl -s -o "$DIR/$f" -w "%{http_code}" "$BASE/$f")
    if [ "$code" = "200" ]; then ok=$((ok+1)); else fail=$((fail+1)); rm -f "$DIR/$f"; fi
  else
    ok=$((ok+1))
  fi
done < chunk-list.txt
echo "downloaded ok=$ok fail=$fail"
du -sh "$DIR" | cut -f1
