#!/usr/bin/env python3
"""Rebuild the FULL per-subject metadata catalogue from the local-only
page cache (harvest output), apply the IP title rule, gzip per subject
into the repo, and emit catalog.csv + verification counts.

Title rule (IP-AND-COPYRIGHT-NOTES.md):
  courseSection / quiz rows keep `title` (structural names)
  examQuestion rows: title -> None (title == plain-text question stem)

Row schema (unchanged from session 3):
  id,type,title,region,timeCreated,questionType,publisher,marksTotal,
  answerCount,difficulty,courseIds,topicBreadcrumbs,tagValues
"""
import json, pathlib, gzip, hashlib, csv, collections

BASE = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3")
LOCAL = BASE / "local-only-full-payloads"
META = BASE / "metadata"
REPO = pathlib.Path("/home/z/my-project/work/seneca-recon/syllabai-experimental/senecalearning/resources/captures/resource-hub")
OUT = REPO / "by-subject"
OUT.mkdir(parents=True, exist_ok=True)
TYPES = ("courseSection", "examQuestion", "quiz")

matrix = json.loads((META / "subject-type-count-matrix.json").read_text())
tags = json.loads((META / "tags-taxonomy.json").read_text())["tags"]
subjects = {t["text"]: t["id"] for t in tags if t.get("semanticCategory") == "subject"}
age_groups = {t["text"]: t["id"] for t in tags if t.get("semanticCategory") == "ageGroup"}
AGE_TYPE_ID = next(t["parentId"] for t in tags
                   if t.get("semanticCategory") == "ageGroup" and t.get("parentId"))


def to_row(src):
    rtype = src.get("type")
    keep_title = rtype in ("courseSection", "quiz")
    return {
        "id": src.get("id"), "type": rtype,
        "title": src.get("title") if keep_title else None,
        "region": src.get("region"), "timeCreated": src.get("timeCreated"),
        "questionType": src.get("questionType"), "publisher": src.get("publisher"),
        "marksTotal": src.get("marksTotal"), "answerCount": src.get("answerCount"),
        "difficulty": src.get("difficulty"),
        "courseIds": (src.get("meta") or {}).get("courseIds"),
        "topicBreadcrumbs": src.get("topicBreadcrumbs"),
        "tagValues": {k: sorted(t.get("value") for t in v)
                      for k, v in (src.get("tags") or {}).items()},
    }


def read_cell(slug, rtype, shard=False, aid8=None):
    """Read a cell's pages sequentially (unsharded or one shard)."""
    rows, frm = [], 0
    while True:
        if shard:
            p = LOCAL / f"{slug}-age{aid8}-{rtype}-{frm:06d}.json"
        else:
            p = LOCAL / f"{slug}-{rtype}-{frm:06d}.json"
        if not p.exists() or p.stat().st_size <= 2:
            break
        d = json.loads(p.read_text())
        items = d.get("items", [])
        rows += [to_row(it.get("_source", {})) for it in items]
        frm += len(items)
        if not items or frm >= d.get("total", 0) or len(items) < 200:
            break
        if not shard and frm >= 9800:
            break  # window cap — cell must be sharded; handled by caller
    return rows


def collect_cell(slug, rtype, count):
    """Collect a full cell (sharded if matrix count > window). Unsharded
    pages are used as a seed when present (identical query, first pages)."""
    rows, seen = [], set()
    def add(rs):
        for r in rs:
            if r["id"] and r["id"] not in seen:
                seen.add(r["id"])
                rows.append(r)
    if count <= 9800:
        add(read_cell(slug, rtype))
        return rows
    # sharded: seed from unsharded prefix if present, then ageGroup shards
    add(read_cell(slug, rtype))
    for aid in sorted(age_groups.values()):
        add(read_cell(slug, rtype, shard=True, aid8=aid[:8]))
    return rows


def slugify(name):
    return name.replace(" ", "_").replace("/", "-")


def main():
    catalog, problems = [], []
    grand = collections.Counter()
    for name in sorted(matrix):
        sid = subjects.get(name)
        if not sid:
            continue
        buckets = matrix[name].get("resourceTypes", {}).get("filtered", {}).get("buckets", [])
        counts = {b["key"]: b["doc_count"] for b in buckets}
        slug = slugify(name)
        rows = []
        per_type = {}
        for rtype in TYPES:
            c = counts.get(rtype, 0)
            if not c:
                per_type[rtype] = 0
                continue
            cell_rows = collect_cell(slug, rtype, c)
            per_type[rtype] = len(cell_rows)
            if len(cell_rows) < c:
                problems.append(f"{name}/{rtype}: harvested {len(cell_rows)} < matrix {c}")
            elif len(cell_rows) > c + 50:  # tolerance for same-day content drift
                problems.append(f"{name}/{rtype}: harvested {len(cell_rows)} > matrix {c} (+{len(cell_rows)-c})")
            rows += cell_rows
            grand[rtype] += len(cell_rows)
        if not rows:
            continue
        rows.sort(key=lambda r: (r["type"], r["id"]))
        out = OUT / f"{slug}.jsonl.gz"
        payload = "\n".join(json.dumps(r) for r in rows)
        out.write_bytes(gzip.compress(payload.encode()))
        h = hashlib.sha256(out.read_bytes()).hexdigest()
        catalog.append({"subject": name, "rows": len(rows),
                        "courseSection": per_type["courseSection"],
                        "examQuestion": per_type["examQuestion"],
                        "quiz": per_type["quiz"],
                        "bytes": out.stat().st_size, "sha256": h})
        print(f"{name}: {len(rows)} rows ({per_type})")
    with (REPO / "by-subject" / "catalog.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["subject", "rows", "courseSection",
                                          "examQuestion", "quiz", "bytes", "sha256"])
        w.writeheader()
        w.writerows(catalog)
    print("\nGRAND TOTAL:", dict(grand), "sum:", sum(grand.values()))
    print("\nPROBLEMS:" if problems else "\nNO COUNT MISMATCHES")
    for p in problems:
        print(" -", p)


if __name__ == "__main__":
    main()
