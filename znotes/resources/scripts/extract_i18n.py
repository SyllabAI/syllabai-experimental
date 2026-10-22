#!/usr/bin/env python3
"""Extract dashEduAi i18n keys, auth endpoints, usage counters from main bundle."""
import re

s = open('/home/z/my-project/syllabai-experimental/znotes/resources/captures/app-bundle.js',
         encoding='utf-8', errors='ignore').read()

keys = sorted(set(re.findall(r'(dashEduAi_[a-zA-Z0-9_]+)', s)))
print(f'{len(keys)} dashEduAi i18n keys:')
for k in keys:
    print(' ', k)

auth = sorted(set(re.findall(r'"(/v2?/auth[a-zA-Z0-9/_${}.-]*)"', s)))
print('AUTH ENDPOINTS:', auth)

for kw in ['educatorAiUsageCount', 'lifetimeEducatorAiUsageCount', 'updateUserInteraction']:
    print(kw, len(re.findall(re.escape(kw), s)))

# extract the dashEduAi string values (en)
vals = re.findall(r'dashEduAi_([a-zA-Z0-9_]+):"([^"]{0,120})"', s)
seen = {}
for k, v in vals:
    seen.setdefault(k, v)
print()
print('=== dashEduAi VALUES (en) ===')
for k, v in sorted(seen.items()):
    print(f'  {k}: {v}')
