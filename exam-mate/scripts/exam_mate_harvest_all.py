#!/usr/bin/env python3
"""exam-mate full-archive harvester — every subject, one by one.

Design:
  * Work list = catalog.json (180 subjects), ordered with SyllabAI-relevant
    boards first.
  * Per subject: fresh page load -> category $set -> subject $set -> apply
    button -> list reload (logged-in session; credentials/session outside repo).
  * Quota wall (403 "request limit") -> auto re-login once per subject, else
    stop cleanly; progress.json checkpoints after every subject.
  * Giants (> 4,900 questions) are year-sharded (site pagination caps at 200
    pages = 5,000 rows): per-year filters -> shard harvest -> merge.
  * Resumable: subjects marked done are skipped; partial writes are redone.

Usage:
  python3 exam_mate_harvest_all.py                 # loop until killed/wall
  python3 exam_mate_harvest_all.py --only 4:34     # one subject
  python3 exam_mate_harvest_all.py --status        # print progress
"""
import json, os, re, shutil, sys, time, traceback

sys.path.insert(0, "/home/z/my-project/syllabai-experimental/exam-mate/scripts")
import exam_mate_crawler as cw
from exam_mate_client import ExamMateClient, PROBE, UA

BASE = cw.BASE
PROGRESS = f"{BASE}/progress.json"
CATALOG = f"{BASE}/catalog.json"
PAGE_CAP_ROWS = 4900          # > this -> year-shard (site caps 200 pages x 25)
CATEGORY_ORDER = [4, 21, 3, 12, 5, 6, 14, 15, 16, 17, 18, 19,
                  7, 56, 57, 58, 59, 53, 54, 55, 13]


def load_progress():
    if os.path.exists(PROGRESS):
        return json.load(open(PROGRESS))
    return {"done": {"3:11": {"questions": 1333, "note": "anonymous full harvest"},
                     "21:614": {"questions": 40, "note": "logged-in full harvest"}},
            "empty": {}, "failed": {}, "quota_wall": False}


def deep_link(cat, subj):
    lab = lambda s: re.sub(r"\s+", "_", s or "x")
    return (f"{cw.ORIGIN}/topicalpastpapers/"
            f"{lab(cat['label'])}-{cat['id']}/{lab(subj['label'])}-{subj['id']}")


def subj_code(label):
    """Syllabus code from the site label, e.g. 'Biology(0610)' -> '0610'."""
    m = re.findall(r"\(([A-Za-z0-9]+)\)", label or "")
    return m[-1] if m else None



def acceptable_prefixes(label):
    """Row paper-ref prefixes that count as 'right subject': the syllabus
    code AND the slugified label head (OCR/AQA rows use name slugs like
    'Biology_B' instead of codes like 'H022')."""
    out = set()
    m = re.findall(r"\(([A-Za-z0-9]+)\)", label or "")
    if m:
        out.add(m[-1].lower())
    head = re.split(r"\(", label or "x")[0]
    out.add(re.sub(r"[^a-z0-9]", "", head.lower()))
    out.discard("")
    return out


def _prefix_ok(p, h):
    """Prefix-family match (either direction), min 4 chars, so '0610' vs
    '0620' and '4CH0' vs '4CH1' stay rejected while 'CHEMI'~'chemistry',
    'BIOL'~'biology', 'Mathematics_A'~'Mathematics_A,_Further' pass."""
    return len(p) >= 4 and len(h) >= 4 and (h.startswith(p) or p.startswith(h))


def rows_match_subject(rows, label):
    pref = {re.sub(r"[^a-z0-9]", "", (r.get("text") or "x").split("/")[0].lower())
            for r in rows if r.get("text")}
    pref.discard("")
    acc = acceptable_prefixes(label)
    return bool(pref) and all(
        any(p == a or _prefix_ok(p, a) for a in acc) for p in pref)


def row_sig(state):
    qs = state.get("questions") or []
    return (qs[0]["qid"] if qs else None,
            tuple(state.get("badges") or []))


PRIME_CAT = 12  # for cat-3 subjects: prime the list via a real 12 -> 3 transition


class Harvester:
    def __init__(self):
        self.cr = cw.Crawler(fresh_session=False)
        self.progress = load_progress()
        self.catalog = json.load(open(CATALOG))

    # ---------------- session ----------------
    def relogin(self):
        """Fresh browser + login form submit; restores serving allowance."""
        try:
            self.cr.c.close()
        except Exception:
            pass
        creds = json.load(open(f"{PROBE}/creds.json"))
        ok = False
        c = ExamMateClient(restore_state=False)
        try:
            c.fetch(f"{cw.ORIGIN}/login", settle_ms=1000)
            c.page.fill('input[name="email"]', creds["email"])
            c.page.fill('input[name="password"]', creds["password"])
            c.page.click('button[type="submit"]')
            time.sleep(4)
            for _ in range(8):
                if "/login" not in c.page.url:
                    break
                time.sleep(1)
            ok = "logout" in c.page.content().lower()
            if ok:
                c._save_state()  # persist auth cookies for the next client
            print(f"[harvest-all] relogin: {'ok' if ok else 'FAILED'}")
        finally:
            c.close()
        if not ok:
            return False
        self.cr = cw.Crawler(fresh_session=False)
        return True

    # ---------------- subject selection ----------------
    def select_subject(self, cat, subj):
        """Fresh load -> category -> subject -> apply. Returns list state.
        Evidence of a REAL list switch is required (row signature change);
        falls back to deep-link navigation; validates rows against the
        subject's syllabus code when the label carries one."""
        c = self.cr.c
        c.fetch(cw.PAGE_URL, settle_ms=1200)
        c.page.evaluate(cw.JS_HELPERS)
        self.cr._install_listener()
        st = self.cr.refresh_state()
        source = "apply"
        if cat["id"] == 3:
            # cat 3 is the load default: a no-op $set wedges the bus, and
            # skipping the transition entirely leaves the list component
            # unprimed (apply dispatch never reaches it) — so PRIME it with
            # a real transition to another category and back.
            prime = next((x for x in st["categories"] if x["id"] == PRIME_CAT), None)
            if prime:
                self.cr.open_category(prime)
            back = next((x for x in self.cr.refresh_state()["categories"]
                         if x["id"] == 3), None)
            st2 = self.cr.open_category(back) if back else self.cr.refresh_state()
        else:
            cat_live = next((x for x in st["categories"] if x["id"] == cat["id"]), None)
            if cat_live is None:
                print(f"[harvest-all] category {cat['id']} not on page!")
                return None
            st2 = self.cr.open_category(cat_live)
            if not st2:
                return None
        subj_live = next((x for x in st2["subjects"] if x["id"] == subj["id"]), None)
        if subj_live is None:
            print(f"[harvest-all] subject {subj['id']} not under cat {cat['id']}")
            return None
        exp = subj_code(subj["label"])
        pre_sig = row_sig(self.cr.refresh_state())

        def apply_and_wait():
            self.cr.click("subjectID", subj["id"])
            time.sleep(2.5)
            c.page.evaluate(
                "() => { const b = document.querySelector('.filter-button, .filterBtn');"
                " if (b) { b.click(); return true; } return false; }")
            return self.cr.poll(
                lambda: self.cr.refresh_state(),
                lambda s: self.cr.quota_exhausted or row_sig(s) != pre_sig,
                timeout=12, desc="apply switch evidence")

        st3 = apply_and_wait()
        if not isinstance(st3, dict) or row_sig(st3) == pre_sig:
            print("    no switch evidence -> one retry")
            st3 = apply_and_wait()
        if self.cr.quota_exhausted:
            return "QUOTA"
        if not isinstance(st3, dict) or row_sig(st3) == pre_sig:
            print("    apply produced no switch -> deep-link fallback")
            source = "deeplink"
            c.fetch(deep_link(cat, subj), settle_ms=2500)
            c.page.evaluate(cw.JS_HELPERS)
            self.cr._install_listener()
            st3 = self.cr.poll(
                lambda: self.cr.refresh_state(),
                lambda s: self.cr.quota_exhausted or row_sig(s) != pre_sig,
                timeout=14, desc="deeplink switch evidence")
            time.sleep(1.5)
            st3 = self.cr.refresh_state()
        if self.cr.quota_exhausted:
            return "QUOTA"
        if not isinstance(st3, dict):
            return None
        # validate the rows actually belong to this subject
        qs = st3.get("questions") or []
        if qs:
            pref = {re.sub(r"[^a-z0-9]", "", (q.get("text") or "x").split("/")[0].lower())
                    for q in qs[:5] if q.get("text")}
            pref.discard("")
            if not rows_match_subject(qs[:5], subj["label"]):
                if len(pref) == 1:
                    # uniform unknown slug (IB 'CHEMI'/'MAT'/'GLPOL' style):
                    # exact-matched click + fresh badges + uniform rows is
                    # sufficient identity evidence — capture and trust it.
                    st3["_row_prefix"] = next(iter(pref))
                    print(f"    uniform site slug {st3['_row_prefix']!r} accepted")
                else:
                    print(f"    ROWS WRONG: expected {acceptable_prefixes(subj['label'])}, "
                          f"saw {sorted(pref)}")
                    return None
        if qs or any(b.isdigit() for b in (st3.get("badges") or [])):
            st3["_source"] = source
            return st3
        return None

    def badge_total(self, state):
        for b in state.get("badges") or []:
            if b.isdigit():
                return int(b)
        return len(state.get("questions") or [])

    # ---------------- year sharding ----------------
    def set_checkboxes(self, name, values):
        self.cr.c.page.evaluate("""([name, values]) => {
            document.querySelectorAll(`input[name="${name}"]`).forEach(i => {
                i.checked = values.includes(String(i.value));
                // Livewire v2 deferred binding only syncs on change events
                i.dispatchEvent(new Event('change', {bubbles: true}));
            });
        }""", [name, [str(v) for v in values]])
        time.sleep(0.4)
        self.cr.c.page.evaluate(
            "() => { const b = document.querySelector('.filter-button, .filterBtn');"
            " if (b) { b.click(); return true; } return false; }")
        time.sleep(4)

    def harvest_sharded(self, cat, subj, state):
        """Year-shard a giant subject; per-shard checkpoint files survive
        chunk restarts (kept outside the repo under exam-mate-probe/).

        Wedge-proofing: EVERY shard starts from a fresh page load +
        select_subject (repeated in-place applies wedge the Livewire commit
        bus — silent stale lists, the 0620 lesson). Every checkpoint is
        validated two ways before it is trusted: row year matches the tag
        AND row count >= 0.95 x shard badge."""
        years = [str(y) for y in state.get("years") or []]
        if not years:
            print("    giant subject but no year facets — aborting subject")
            return 0
        seasons = [x.get("v") if isinstance(x, dict) else x
                   for x in (state.get("seasons") or [])]
        final_dir = self.cr.subject_dir(cat, subj)
        tmp = f"{PROBE}/shards/{cat['id']}_{subj['id']}"
        os.makedirs(tmp, exist_ok=True)
        total_n = 0
        shard_jsonls = []

        def shard_file(tag):
            return f"{tmp}/{tag}.jsonl"

        def badge_file(tag):
            return f"{tmp}/{tag}.badge"

        def count_rows(path):
            n = 0
            if not os.path.exists(path):
                return 0
            for l in open(path):
                if l.strip():
                    n += 1
            return n

        def shard_valid(tag):
            """Checkpoint exists, year matches rows, count >= 0.95 badge."""
            p = shard_file(tag)
            if not os.path.exists(p) or os.path.getsize(p) < 2:
                return False
            yr = tag.split("_")[1]
            lines = [l for l in open(p) if l.strip()]
            try:
                first = json.loads(lines[0])
                if f"_{yr}_" not in (first.get("text") or ""):
                    return False
            except Exception:
                return False
            if not os.path.exists(badge_file(tag)):
                return False  # no recorded badge -> cannot verify -> redo
            badge = int(open(badge_file(tag)).read().strip() or 0)
            return count_rows(p) >= badge * 0.95

        def collect_shard(tag, badge):
            """Validate the just-harvested shard; checkpoint if complete."""
            shard_dir = self.cr.subject_dir(cat, subj)
            src = f"{shard_dir}/questions.jsonl"
            n = count_rows(src)
            if badge and n < badge * 0.95:
                print(f"    shard {tag}: TRUNCATED {n}/{badge} — no checkpoint")
                return False
            shutil.copy(src, shard_file(tag))
            open(badge_file(tag), "w").write(str(badge))
            shard_jsonls.append(shard_file(tag))
            return True

        def apply_shard_filters(year=None, season=None):
            """Fresh page -> subject -> optional year/season filter."""
            st0 = self.select_subject(cat, subj)
            if not isinstance(st0, dict) or self.cr.quota_exhausted:
                return None
            if year is not None:
                self.set_checkboxes("years[]", [year])
                self.set_checkboxes("seasons[]", [season] if season else [])
                if self.cr.quota_exhausted:
                    return None
                st1 = self.cr.refresh_state()
                return st1
            return st0

        try:
            for y in years:
                tag = f"y_{y}"
                if shard_valid(tag):
                    print(f"    year {y}: checkpointed, skip")
                    shard_jsonls.append(shard_file(tag))
                    continue
                st = apply_shard_filters(year=y)
                if st is None:
                    if self.cr.quota_exhausted:
                        break
                    continue
                shard_total = self.badge_total(st)
                print(f"    year {y}: {shard_total} questions")
                open(badge_file(tag), "w").write(str(shard_total))
                if shard_total == 0:
                    open(shard_file(tag), "w").close()
                    shard_jsonls.append(shard_file(tag))
                    continue
                if shard_total > PAGE_CAP_ROWS + 100:
                    # secondary shard by season within the year
                    ok_all = True
                    for s in seasons:
                        stag = f"y_{y}_s_{s}"
                        if shard_valid(stag):
                            shard_jsonls.append(shard_file(stag))
                            continue
                        st2 = apply_shard_filters(year=y, season=s)
                        if st2 is None:
                            if self.cr.quota_exhausted:
                                ok_all = False
                                break
                            continue
                        st_total = self.badge_total(st2)
                        print(f"    year {y} season {s}: {st_total} questions")
                        open(badge_file(stag), "w").write(str(st_total))
                        if st_total == 0:
                            open(shard_file(stag), "w").close()
                            shard_jsonls.append(shard_file(stag))
                            continue
                        if st_total > PAGE_CAP_ROWS + 100:
                            print(f"    year {y} season {s} STILL giant — skipped")
                            continue
                        self.cr.harvest_subject(cat, subj, st2, resp_marker=0)
                        if not collect_shard(stag, st_total):
                            ok_all = False
                    if not ok_all and self.cr.quota_exhausted:
                        break
                    continue
                self.cr.harvest_subject(cat, subj, st, resp_marker=0)
                collect_shard(tag, shard_total)
            # merge
            seen, merged = set(), []
            for p in shard_jsonls:
                if not os.path.exists(p):
                    continue
                for line in open(p):
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    if r.get("qid") and r["qid"] not in seen:
                        seen.add(r["qid"])
                        merged.append(r)
            os.makedirs(final_dir, exist_ok=True)
            with open(f"{final_dir}/questions.jsonl", "w") as f:
                for r in merged:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            meta = {"category": cat, "subject": subj,
                    "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "sharded_by_year": True, "years_sharded": years,
                    "badges": state.get("badges")}
            json.dump(meta, open(f"{final_dir}/meta.json", "w"), indent=1,
                      ensure_ascii=False)
            total_n = len(merged)
        finally:
            pass
        return total_n

    # ---------------- main loop ----------------
    def work_list(self):
        items = []
        for cid in CATEGORY_ORDER:
            subs = self.catalog.get("subjects_by_category", {}).get(str(cid)) or []
            cat = next((c for c in self.catalog["categories"] if c["id"] == cid),
                       {"id": cid, "label": str(cid)})
            for s in subs:
                items.append((cat, s))
        return items

    def run(self, only=None):
        items = self.work_list()
        print(f"[harvest-all] work list: {len(items)} subjects; "
              f"done={len(self.progress['done'])} empty={len(self.progress['empty'])}")
        for cat, subj in items:
            key = f"{cat['id']}:{subj['id']}"
            if only and key != only:
                continue
            if key in self.progress["done"] or key in self.progress["empty"]:
                continue
            if key in self.progress["failed"] and self.progress["failed"][key].get("attempts", 0) >= 2:
                continue
            print(f"== [{key}] {subj['label']} (cat {cat['id']} {cat['label']})")
            try:
                state = self.select_subject(cat, subj)
                if state == "QUOTA":
                    print("    quota wall -> relogin")
                    self.progress["quota_wall"] = True
                    self.save()
                    if not self.relogin():
                        print("    relogin failed — stopping run")
                        return 2
                    self.cr.quota_exhausted = False
                    self.progress["quota_wall"] = False
                    state = self.select_subject(cat, subj)
                    if state == "QUOTA" or state is None:
                        self.fail(key, cat, subj, "quota after relogin")
                        continue
                if state is None:
                    self.fail(key, cat, subj, "list did not reload")
                    continue
                total = self.badge_total(state)
                if total == 0:
                    if state.get("_source") != "apply":
                        self.fail(key, cat, subj,
                                  "0 rows from deep-link (string-seed bug) — not trusted as empty")
                        continue
                    d = self.cr.subject_dir(cat, subj)
                    json.dump({"category": cat, "subject": subj,
                               "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                               "badges": state.get("badges"), "total": 0,
                               "facet_evidence": {
                                   "topics": len(state.get("topics") or []),
                                   "years": len(state.get("years") or []),
                                   "papers": len(state.get("papers") or []),
                                   "seasons": len(state.get("seasons") or [])},
                               "note": "apply-path re-render served 0 rows; "
                                       "site itself reports no questions for "
                                       "this subject (facet evidence above)"},
                              open(f"{d}/meta.json", "w"), indent=1, ensure_ascii=False)
                    open(f"{d}/questions.jsonl", "w").close()
                    self.progress["empty"][key] = {"label": subj["label"]}
                    self.save()
                    print(f"    empty subject (0 questions) — recorded")
                    continue
                if total > PAGE_CAP_ROWS:
                    n = self.harvest_sharded(cat, subj, state)
                else:
                    n = self.cr.harvest_subject(cat, subj, state, resp_marker=0)
                    n = n if isinstance(n, int) else 0
                # post-harvest validation: right subject + completeness
                d = self.cr.subject_dir(cat, subj)
                qf = f"{d}/questions.jsonl"
                recs = [json.loads(l) for l in open(qf)][:5] if os.path.exists(qf) else []
                ok_rows = rows_match_subject(recs, subj["label"]) or (
                    state.get("_row_prefix") and recs and all(
                        (r.get("text") or "").split("/")[0].lower() == state["_row_prefix"]
                        for r in recs if r.get("text")))
                if recs and not ok_rows:
                    os.remove(qf)
                    self.fail(key, cat, subj,
                              f"contaminated rows {sorted({r['text'].split('/')[0] for r in recs})}")
                    continue
                if n < total * 0.95:
                    if os.path.exists(qf):
                        os.remove(qf)
                    self.fail(key, cat, subj, f"incomplete {n}/{total}")
                    continue
                self.progress["done"][key] = {
                    "label": subj["label"], "cat_label": cat["label"],
                    "badge_total": total, "questions": n,
                    "at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
                self.progress["failed"].pop(key, None)
                self.save()
                print(f"    DONE {key}: {n}/{total} questions")
                if self.cr.quota_exhausted:
                    print("    quota hit during harvest -> relogin next subject")
                    if not self.relogin():
                        return 2
                    self.cr.quota_exhausted = False
            except SystemExit:
                raise
            except Exception as e:
                traceback.print_exc()
                self.fail(key, cat, subj, repr(e)[:160])
                try:
                    self.relogin()
                except Exception:
                    pass
        return 0

    def fail(self, key, cat, subj, why):
        f = self.progress["failed"].setdefault(key, {"attempts": 0})
        f.update({"attempts": f.get("attempts", 0) + 1, "last_error": why,
                  "label": subj["label"],
                  "at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
        self.save()
        print(f"    FAIL {key}: {why}")

    def save(self):
        json.dump(self.progress, open(PROGRESS, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    if "--status" in sys.argv:
        p = load_progress()
        print(json.dumps({k: (len(v) if isinstance(v, dict) else v)
                          for k, v in p.items()}, indent=1))
        print("done:", json.dumps(p["done"], indent=1, ensure_ascii=False)[:1500])
        print("failed:", json.dumps(p["failed"], indent=1, ensure_ascii=False)[:800])
        sys.exit(0)
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    h = Harvester()
    sys.exit(h.run(only=only))
