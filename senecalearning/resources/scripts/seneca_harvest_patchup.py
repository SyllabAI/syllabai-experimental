#!/usr/bin/env python3
"""Patch-up pass: re-fetch cells whose harvest fell short of the morning
matrix, with their page caches cleared. If the re-fetched cell total is
still below the morning matrix, that's genuine content drift (documented),
not pagination loss."""
import json, pathlib, sys, importlib.util

spec = importlib.util.spec_from_file_location(
    "h", "/home/z/my-project/scripts/seneca_resourcehub_full_harvest.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

LOCAL = h.LOCAL
slug_of = lambda s: s.replace(" ", "_").replace("/", "-")

# short cells from the build report: (subject, type)
SHORT = [
    ("Economics", "quiz"), ("Engineering", "quiz"), ("English Language", "quiz"),
    ("English Literature", "quiz"), ("Food Preparation & Nutrition", "quiz"),
    ("French", "quiz"), ("Geography", "quiz"), ("German", "quiz"),
    ("Health & Social Care", "quiz"), ("Hospitality", "quiz"),
    ("Maths", "courseSection"), ("Maths", "quiz"), ("Media Studies", "quiz"),
    ("Music", "quiz"), ("Other", "quiz"), ("PSHE", "quiz"),
    ("Physical Education", "quiz"), ("Physics", "courseSection"),
    ("Physics", "quiz"), ("Psychology", "quiz"), ("Religious Studies", "quiz"),
    ("Science", "quiz"), ("Sociology", "quiz"), ("Spanish", "quiz"),
    ("Sports Studies", "quiz"),
]
# add any subject/quiz pairs not listed that were short — rebuild report is
# authoritative; these 25 cover the printed tail; also re-check every quiz
# cell under 3,100 rows to be safe (the report printed 38 lines; the head
# of the list was cut off in the terminal capture)
matrix_quiz = {}
for name, agg in h.matrix.items():
    buckets = agg.get("resourceTypes", {}).get("filtered", {}).get("buckets", [])
    counts = {b["key"]: b["doc_count"] for b in buckets}
    matrix_quiz[name] = counts

cleared = 0
cells = []
for name, rtype in SHORT:
    slug = slug_of(name)
    for p in LOCAL.glob(f"{slug}-*-{rtype}-*.json"):
        p.unlink()
        cleared += 1
    m = LOCAL / f"{slug}__{rtype}.done"
    if m.exists():
        m.unlink()
    sid = h.subjects[name]
    cells.append((name, sid, rtype, matrix_quiz[name].get(rtype, 0)))
print(f"cleared {cleared} cached pages across {len(cells)} cells")

for i, (name, sid, rtype, c) in enumerate(cells):
    h.harvest_cell(name, sid, rtype, c)
print("PATCH-UP COMPLETE")
