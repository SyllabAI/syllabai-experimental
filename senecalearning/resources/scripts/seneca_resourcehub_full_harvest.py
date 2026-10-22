#!/usr/bin/env python3
"""Seneca Resource Hub — FULL 74-subject metadata harvest (session 7).

Completes session 3's partial pass (Chemistry full + 69 first-page samples)
by downloading the metadata of ALL 207,629 resources across
courseSection / examQuestion / quiz types.

Conduct: <=1 req/s (0.8s sleep + latency), descriptive UA, resumable page
cache, backoff on errors, NO content fields stored beyond what the
rebuild step keeps (rebuild applies the IP title rule).

Sharding: cells whose matrix count > 9,800 (ES from+size window) are
sharded by ageGroup tag; shards deduped by resource id at rebuild time.

Pages -> LOCAL_ONLY cache dir. Done-markers -> {cell}.done files.
"""
import json, subprocess, time, uuid, pathlib, sys, collections, argparse

TOKFILE = pathlib.Path("/tmp/seneca_token.txt")
CID = f"{int(time.time()*1000)}::{uuid.uuid4()}"
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0 (SyllabAI-research)"
BASE = pathlib.Path("/home/z/my-project/work/seneca-recon/probe-results/rh3")
LOCAL = BASE / "local-only-full-payloads"
META = BASE / "metadata"
LOCAL.mkdir(parents=True, exist_ok=True)
TUTOR = "https://tutor-resources.app.senecalearning.com/api/v2/query-resources"
COURSE = "https://course.app.senecalearning.com"
SUBJ = "8c71d055-ff40-4536-8629-5073c618ea53"
WINDOW = 9800          # safe ES from+size margin
SIZE = 200
TYPES = ("courseSection", "examQuestion", "quiz")

matrix = json.loads((META / "subject-type-count-matrix.json").read_text())
tags = json.loads((META / "tags-taxonomy.json").read_text())["tags"]
subjects = {t["text"]: t["id"] for t in tags if t.get("semanticCategory") == "subject"}
age_groups = {t["text"]: t["id"] for t in tags if t.get("semanticCategory") == "ageGroup"}
# tagTypeId for a semanticCategory = the tags' parentId (verified: subject
# tags' parentId == 8c71d055-…, ageGroup tags' parentId == 3df4913a-… which
# also appeared in the live vocab-tab capture's aggregationCategoryIds)
AGE_TYPE_ID = next(t["parentId"] for t in tags
                   if t.get("semanticCategory") == "ageGroup" and t.get("parentId"))


def log(msg):
    print(msg, flush=True)


def req(body, save):
    p = LOCAL / save
    if p.exists() and p.stat().st_size > 2:
        return "200(cache)", p.read_text()
    for attempt in range(4):
        tok = TOKFILE.read_text().strip()
        cmd = ["curl", "-s", "-m", "40", "--compressed", "-X", "POST", TUTOR,
               "-H", f"correlationId: {CID}", "-H", "Content-Type: application/json",
               "-H", f"access-key: {tok}", "-H", f"User-Agent: {UA}",
               "-H", "user-region: GB",
               "-H", "Origin: https://app.senecalearning.com",
               "-d", json.dumps(body), "-w", "\n---STATUS:%{http_code}---"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = r.stdout
        status = out.rsplit("---STATUS:", 1)[-1].split("---")[0] if "---STATUS:" in out else "?"
        txt = out.rsplit("\n---STATUS:", 1)[0]
        if status.startswith("2"):
            p.write_text(txt)
            time.sleep(0.8)
            return status, txt
        if status == "401":
            log(f"    401 — token expired; save progress and re-login. ({save})")
            sys.exit(2)
        wait = [10, 20, 40][min(attempt, 2)]
        log(f"    {status} on {save}, retry in {wait}s")
        time.sleep(wait)
    log(f"    GIVE UP cell page {save}")
    return "ERR", ""


def harvest_cell(subject, sid, rtype, count):
    """Returns (rows_loaded_pages, total_seen). Resumable via cache+markers."""
    slug = subject.replace(" ", "_").replace("/", "-")
    marker = LOCAL / f"{slug}__{rtype}.done"
    if marker.exists():
        return
    use_shard = count > WINDOW
    shards = [None]
    if use_shard:
        shards = []
        for aname, aid in sorted(age_groups.items()):
            shards.append({"slug": slug, "aid8": aid[:8], "aid": aid, "aname": aname})
        log(f"  {subject}/{rtype}: {count} > {WINDOW} -> {len(shards)} ageGroup shards")
    grand = 0
    for shard in shards:
        frm = 0
        seen_total = None
        while True:
            if shard:
                save = f"{slug}-age{shard['aid8']}-{rtype}-{frm:06d}.json"
                tags_filter = {SUBJ: [sid], AGE_TYPE_ID: [shard["aid"]]}
            else:
                save = f"{slug}-{rtype}-{frm:06d}.json"
                tags_filter = {SUBJ: [sid]}
            # resume: find first missing page offset (cache is contiguous)
            body = {"query": "", "filters": {"tags": tags_filter},
                    "resourceFilters": [{"type": rtype, "must": {}}],
                    "from": frm, "size": SIZE, "aggregatePublishers": False,
                    "aggregateResourceTypes": False,
                    "aggregateExamQuestionMarksTotal": False,
                    "globalAggregations": False}
            status, txt = req(body, save)
            if not status.startswith("2") and status != "200(cache)":
                break
            if not txt.strip():
                break
            d = json.loads(txt)
            items = d.get("items", [])
            seen_total = d.get("total", seen_total)
            if not items:
                break
            frm += len(items)
            if frm >= (seen_total or 0) or len(items) < SIZE:
                break
            if not shard and frm >= WINDOW:
                log(f"    window cap hit unsharded {subject}/{rtype} @ {seen_total} -> needs shard")
                break
        grand += frm
    marker.write_text(str(grand))
    log(f"  {subject}/{rtype}: done, pages_covered_rows={grand}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=10_000_000,
                    help="wall-clock seconds to run before clean exit "
                         "(sandbox-safe slicing; resume via cache)")
    args = ap.parse_args()
    deadline = time.monotonic() + args.budget
    cells = []
    for name, agg in matrix.items():
        sid = subjects.get(name)
        if not sid:
            log(f"!! no tag id for subject {name}")
            continue
        buckets = (agg.get("resourceTypes", {}).get("filtered", {})
                   .get("buckets", []))
        counts = {b["key"]: b["doc_count"] for b in buckets}
        for rtype in TYPES:
            c = counts.get(rtype, 0)
            if c:
                cells.append((name, sid, rtype, c))
    # Chemistry first (cache hit), then small->large for better interruption profile
    cells.sort(key=lambda c: (c[0] == "Chemistry", c[3]))
    log(f"work list: {len(cells)} cells, est rows {sum(c[3] for c in cells)}")
    done = sum(1 for c in cells if (LOCAL / f"{c[0].replace(' ', '_').replace('/', '-')}__{c[2]}.done").exists())
    log(f"already done: {done}")
    for i, (name, sid, rtype, c) in enumerate(cells):
        if time.monotonic() > deadline:
            log(f"BUDGET REACHED at cell {i}/{len(cells)} — clean exit, resume later")
            return
        if i % 10 == 0:
            log(f"[{i+1}/{len(cells)}] next: {name}/{rtype} ({c})")
        harvest_cell(name, sid, rtype, c)
    log("HARVEST COMPLETE")


if __name__ == "__main__":
    main()
