#!/usr/bin/env python3
"""SyllabAI — build the FULL-CONTENT resource corpus for the repo (v2 layout).

Supersedes the metadata-only session-7 build. Operator approved storing
Seneca content (2026-10-23), so this builder KEEPS the teaching content:

  examQuestion  -> questionTitleMd, markScheme, generationScript, title, meta
  courseSection -> topicNotes, description, imageUrl
  quiz          -> quizSummary  (creator/school identifiers SCRUBBED)

Outputs (senecalearning/resources/captures/resource-hub-content/):
  by-subject/<Subject>.jsonl.gz   one gzip JSONL per subject, full _source
  by-subject/catalog.csv          subject -> rows/type counts/bytes/sha256
  courses/edexcel-igcse-chemistry/<CourseSlug>.json  per-course tree + resources
  README.md                       schema + provenance + PII policy

Run AFTER the full harvest completes (reads local-only-full-payloads pages).
"""
import csv
import glob
import gzip
import hashlib
import json
import pathlib
import re
import sys

BASE = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3")
LOCAL = BASE / "local-only-full-payloads"
META = BASE / "metadata"
REPO = pathlib.Path(
    "/home/z/my-project/work/seneca-recon/syllabai-experimental/"
    "senecalearning/resources/captures/resource-hub-content"
)
TYPES = ("courseSection", "examQuestion", "quiz")

PII_FIELDS = ("creatorName", "creatorId", "schoolId", "schoolGroupId")


def slugify(name: str) -> str:
    # MUST match the harvest engine's slug: spaces -> _, slashes -> -, nothing else
    return name.replace(" ", "_").replace("/", "-") or "subject"


def load_matrix_subjects():
    matrix = json.loads((META / "subject-type-count-matrix.json").read_text())
    tags = json.loads((META / "tags-taxonomy.json").read_text())["tags"]
    subjects = {t["text"]: t["id"] for t in tags if t.get("semanticCategory") == "subject"}
    return matrix, subjects


def collect_pages():
    """subjectSlug -> type -> {resourceId: _source} (dedup across shards/pages)."""
    buckets: dict[str, dict[str, dict[str, dict[str, any]]]] = {}
    for f in sorted(LOCAL.glob("*.json")):
        m = re.match(r"^(.+?)-(age[0-9a-f]{8}-)?(courseSection|examQuestion|quiz)-\d+\.json$", f.name)
        if not m:
            continue
        slug, _age, rtype = m.group(1), m.group(2), m.group(3)
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        items = d.get("items") or []
        if not items:
            continue
        b = buckets.setdefault(slug, {}).setdefault(rtype, {})
        for it in items:
            src = it.get("_source") or {}
            rid = src.get("id") or it.get("_id")
            if rid:
                b[rid] = src
    return buckets


def clean(v):
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def scrub(src: dict) -> dict:
    return {k: v for k, v in src.items() if k not in PII_FIELDS}


def keep_fields(src: dict) -> dict:
    t = src.get("type")
    out = {
        "id": src.get("id"),
        "type": t,
        "title": clean(src.get("title")),
        "region": clean(src.get("region")),
        "timeCreated": clean(src.get("timeCreated")),
        "publisher": clean(src.get("publisher")),
        "tags": {
            tt: [{"id": v.get("id"), "value": v.get("value")} for v in (vals or [])]
            for tt, vals in (src.get("tags") or {}).items()
        },
    }
    if t == "courseSection":
        out["content"] = {
            "description": clean(src.get("description")),
            "topicNotes": clean(src.get("topicNotes")),
            "imageUrl": clean(src.get("imageUrl")),
            "previewUrl": clean(src.get("previewUrl")),
            "contentUrl": clean(src.get("contentUrl")),
        }
    elif t == "examQuestion":
        out["questionType"] = clean(src.get("questionType"))
        out["marksTotal"] = src.get("marksTotal")
        out["difficulty"] = clean(src.get("difficulty"))
        out["answerCount"] = src.get("answerCount")
        out["content"] = {
            "questionTitleMd": clean(src.get("questionTitleMd")),
            "markScheme": clean(src.get("markScheme")),
            "generationScript": clean(src.get("generationScript")),
            "topicBreadcrumbs": [
                clean(x) for x in (src.get("topicBreadcrumbs") or "").split("\n") if clean(x)
            ],
        }
        meta = src.get("meta") or {}
        if meta.get("courseIds"):
            out["courseIds"] = meta["courseIds"]
    elif t == "quiz":
        out["access"] = clean(src.get("access"))
        out["isPublic"] = src.get("isPublic")
        out["saveCount"] = src.get("saveCount")
        out["content"] = {"quizSummary": clean(src.get("quizSummary"))}
    return out


def main():
    matrix, subjects = load_matrix_subjects()
    buckets = collect_pages()
    REPO.mkdir(parents=True, exist_ok=True)
    (REPO / "by-subject").mkdir(exist_ok=True)
    (REPO / "courses" / "edexcel-igcse-chemistry").mkdir(parents=True, exist_ok=True)

    # ---- per-subject JSONL.gz + catalog ----
    catalog = []
    total_rows = 0
    for subj_name, agg in sorted(matrix.items()):
        sid = subjects.get(subj_name)
        if not sid:
            continue
        slug = slugify(subj_name)
        rows_by_type = buckets.get(slug, {})
        rows = []
        for rtype in TYPES:
            for rid in sorted(rows_by_type.get(rtype, {})):
                rows.append(keep_fields(rows_by_type[rtype][rid]))
        if not rows:
            continue
        payload = "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows)
        blob = gzip.compress(payload.encode("utf-8"), 9)
        out = REPO / "by-subject" / f"{slug}.jsonl.gz"
        out.write_bytes(blob)
        counts = {t: sum(1 for r in rows if r["type"] == t) for t in TYPES}
        catalog.append({
            "subject": subj_name,
            "rows": len(rows),
            **counts,
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
        })
        total_rows += len(rows)
        print(f"  {subj_name}: {len(rows)} rows ({', '.join(f'{t}={counts[t]}' for t in TYPES)})", flush=True)

    with open(REPO / "by-subject" / "catalog.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["subject", "rows", *TYPES, "bytes", "sha256"])
        w.writeheader()
        w.writerows(catalog)
    print(f"TOTAL: {total_rows} rows across {len(catalog)} subjects")

    # ---- per-course trees for the Edexcel iGCSE Chemistry family ----
    hub = pathlib.Path(
        "/home/z/my-project/work/seneca-recon/syllabai-experimental/"
        "senecalearning/resources/captures/resource-hub"
    )
    fam_courses = json.loads((hub / "edexcel-igcse-chemistry-courses.json").read_text())["courses"]
    fam_sections = json.loads((hub / "edexcel-igcse-chemistry-sections.json").read_text())["sections"]
    chem = buckets.get("Chemistry", {})
    sec_by_id = {}
    for rid, src in chem.get("courseSection", {}).items():
        sec_by_id[rid] = keep_fields(src)
    eq_by_course: dict[str, list] = {}
    for rid, src in chem.get("examQuestion", {}).items():
        k = keep_fields(src)
        for cid in k.get("courseIds", []):
            eq_by_course.setdefault(cid, []).append(k)
    quiz_rows = [keep_fields(s) for s in chem.get("quiz", {}).values()]

    family_index = []
    for c in fam_courses:
        cid, title = c["id"], c["title"]
        cslug = re.sub(r"[^\w-]+", "_", title).strip("_") or "course"
        secs = [sec_by_id[s["id"]] for s in fam_sections if s["courseId"] == cid and s["id"] in sec_by_id]
        secs.sort(key=lambda s: (s.get("title") or ""))
        doc = {
            "courseId": cid,
            "courseTitle": title,
            "subscriptionTier": c.get("subscriptionTier") or c.get("tier"),
            "sectionCount": len(secs),
            "sections": secs,
            "examQuestions": sorted(
                eq_by_course.get(cid, []),
                key=lambda q: (
                    (q.get("content") or {}).get("topicBreadcrumbs") or [""]
                )[0]
                or (q.get("title") or ""),
            ),
        }
        (REPO / "courses" / "edexcel-igcse-chemistry" / f"{cslug}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=1)
        )
        family_index.append({
            "courseId": cid,
            "title": title,
            "sections": len(secs),
            "examQuestions": len(doc["examQuestions"]),
        })
        print(f"  course {title!r}: {len(secs)} sections, {len(doc['examQuestions'])} examQuestions", flush=True)

    (REPO / "courses" / "edexcel-igcse-chemistry" / "family-index.json").write_text(
        json.dumps({
            "family": "Chemistry: Edexcel iGCSE",
            "courses": family_index,
            "subjectQuizzes": {"count": len(quiz_rows), "note": "subject-tagged (not course-scoped); in Chemistry.jsonl.gz"},
        }, ensure_ascii=False, indent=1)
    )
    print("course layer written")


if __name__ == "__main__":
    sys.exit(main())
