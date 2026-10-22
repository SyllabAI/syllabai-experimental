#!/usr/bin/env python3
"""Scan a JS bundle/chunk for API endpoints and keyword hits."""
import re, sys

path = sys.argv[1]
kws = sys.argv[2].split(',') if len(sys.argv) > 2 else []

s = open(path, encoding='utf-8', errors='ignore').read()
print(f'== {path} (size {len(s)}) ==')

# endpoint-ish strings: /v1/..., /api/..., template literals with ${}
eps = set()
eps.update(re.findall(r'"(/(?:api/)?v?\d?/?[a-zA-Z0-9\-_]{3,60}(?:/[a-zA-Z0-9\-_${}.]{1,40})*)"', s))
eps.update(re.findall(r'`(/(?:api/)?v?\d?/?[a-zA-Z0-9\-_]{3,60}(?:/\$\{[^}]+\})?(?:/[a-zA-Z0-9\-_${}.]{1,40})*`)', s))
eps = sorted(e for e in eps if '/' in e and not e.endswith('.js'))
print('ENDPOINT-LIKE STRINGS:')
for e in eps:
    print('  ', e)

for kw in kws:
    n = len(re.findall(re.escape(kw), s, re.I))
    if n:
        print(f'KW {kw}: {n} hits')
        for m in list(re.finditer(re.escape(kw), s, re.I))[:4]:
            i = m.start()
            print('     ...', s[max(0, i - 100):i + 120].replace('\n', ' '))
