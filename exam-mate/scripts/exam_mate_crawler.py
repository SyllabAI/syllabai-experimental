"""exam-mate TOPICAL PAST PAPERS crawler v2 — resumable production harvest.

Architecture:
  * DOM clicks drive category/subject transitions (filter-box.topical-filter-box).
  * The questions list (list.questions-list) re-renders itself on the
    filterResults dispatch; we CAPTURE its Livewire POST response to obtain the
    component's live serverMemo (correct filters for the current subject).
  * Pagination = in-page fetch replay of gotoPage(N) on that captured snapshot,
    chaining serverMemo from each response. Cards are parsed straight from the
    response HTML (each card embeds its full payload in onclick=selectQuestion).

Outputs under BASE:
  catalog.json, progress.json
  topical/<catID>_<label>/<subjID>_<label>/meta.json + questions.jsonl
"""
import json, os, re, sys, time, traceback, html as H

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_mate_client import ExamMateClient

BASE = "/home/z/my-project/syllabai-experimental/exam-mate/resources/topical_papers"
PROGRESS = f"{BASE}/progress.json"
CATALOG = f"{BASE}/catalog.json"
ORIGIN = "https://www.exam-mate.com"
PAGE_URL = f"{ORIGIN}/topicalpastpapers"

JS_HELPERS = r"""
() => {
  window.__emClick = (substr, value) => {
    const all = Array.from(document.querySelectorAll('*'))
      .filter(el => (el.getAttribute('wire:click') || '').includes(substr));
    let target = null;
    if (value === null) {
      target = all.find(el => (el.getAttribute('wire:click') || '') === substr) || all[0];
    } else {
      target = all.find(el => (el.getAttribute('wire:click') || '').includes(String(value)));
    }
    if (target) { target.click(); return true; }
    return false;
  };
  window.__emState = () => ({
    topics: Array.from(document.querySelectorAll('input[name="topics[]"]'))
      .map(i => ({v: i.value, n: i.getAttribute('data-name')})),
    zones: Array.from(document.querySelectorAll('input[name="zones[]"]')).map(i => i.value),
    papers: Array.from(document.querySelectorAll('input[name="papers[]"]'))
      .map(i => ({v: i.value, n: i.getAttribute('data-name')})),
    seasons: Array.from(document.querySelectorAll('input[name="seasons[]"]'))
      .map(i => ({v: i.value, n: i.getAttribute('data-name')})),
    years: Array.from(document.querySelectorAll('input[name="years[]"]')).map(i => i.value),
    subjects: Array.from(document.querySelectorAll('*'))
      .filter(el => (el.getAttribute('wire:click') || '').includes("$set('subjectID'"))
      .map(el => {
        const m = el.getAttribute('wire:click').match(/subjectID',\s*(\d+)/);
        return {id: m ? parseInt(m[1]) : null, label: el.textContent.trim().replace(/\s+/g, ' ').slice(0, 80)};
      }).filter(x => x.id),
    categories: Array.from(document.querySelectorAll('*'))
      .filter(el => (el.getAttribute('wire:click') || '').includes("$set('categoryID'"))
      .map(el => {
        const m = el.getAttribute('wire:click').match(/categoryID',\s*(\d+)/);
        return {id: m ? parseInt(m[1]) : null, label: el.textContent.trim().replace(/\s+/g, ' ').slice(0, 60)};
      }).filter(x => x.id),
    questions: Array.from(document.querySelectorAll('li[id^="qid-"]')).map(li => {
      const oc = li.getAttribute('onclick') || '';
      const idm = oc.match(/selectQuestion\((\d+),(\d+)/);
      let payload = null;
      const jm = oc.match(/'(\{.*\})'\s*\)\s*;?\s*$/) || oc.match(/'(\{.*\})'/);
      if (jm) {
        let raw = jm[1].replace(/&quot;/g, '"');
        try { payload = JSON.parse(raw); }
        catch (e) { try { payload = JSON.parse(raw.replace(/\\\\/g, '\\')); } catch (e2) {} }
      }
      return {
        qid: idm ? parseInt(idm[1]) : null,
        eventKey: idm ? parseInt(idm[2]) : null,
        text: li.textContent.trim().replace(/\s+/g, ' ').slice(0, 160),
        payload,
      };
    }),
    badges: Array.from(document.querySelectorAll('.sortable-header .badge')).map(b => b.textContent.trim()),
    hasNext: (() => {
      const el = Array.from(document.querySelectorAll('*'))
        .find(e => (e.getAttribute('wire:click') || '') === 'nextPage');
      return !!el && !String(el.closest('li')?.className || el.className || '').includes('disabled');
    })(),
  });
}
"""


def parse_cards_from_html(htmlout):
    """Extract question cards from a Livewire effects.html string."""
    cards = []
    for m in re.finditer(r'<li[^>]*id="qid-(\d+)-(\d+)"[^>]*onclick="([^"]*)"', htmlout):
        qid, evk, oc = int(m.group(1)), int(m.group(2)), H.unescape(m.group(3))
        payload = None
        jm = re.search(r"'(\{.*\})'\s*\)\s*;?\s*$", oc) or re.search(r"'(\{.*\})'", oc)
        if jm:
            raw = jm.group(1).replace('\\"', '"').replace("&quot;", '"')
            try:
                payload = json.loads(raw)
            except Exception:
                try:
                    payload = json.loads(raw.replace("\\\\", "\\"))
                except Exception:
                    payload = None
        cards.append({"qid": qid, "eventKey": evk, "payload": payload})
    return cards


class Crawler:
    def __init__(self, fresh_session=True):
        os.makedirs(BASE, exist_ok=True)
        self.c = ExamMateClient(restore_state=not fresh_session)
        self.quota_exhausted = False
        self.list_responses = []      # latest questions-list Livewire responses
        self._install_listener()
        self.c.page.goto(PAGE_URL, wait_until="domcontentloaded", timeout=60000)
        waited = 0
        while "moment" in (self.c.page.title() or "").lower() and waited < 30:
            time.sleep(2); waited += 2
        time.sleep(2.5)
        self.c.page.evaluate(JS_HELPERS)
        self.progress = json.load(open(PROGRESS)) if os.path.exists(PROGRESS) else {"subjects_done": [], "subjects_partial": {}}
        self.catalog = json.load(open(CATALOG)) if os.path.exists(CATALOG) else {}
        self.pw_note = "crawler v2"

    def _install_listener(self):
        QUOTA_MARK = "request limit"
        def on_response(resp):
            if "/livewire/message/list.questions-list" in resp.url:
                try:
                    body = resp.text()
                    if QUOTA_MARK in body:
                        self.quota_exhausted = True
                        print("    [QUOTA] request limit hit — list serving denied")
                    if body.startswith("{"):
                        self.list_responses.append({
                            "t": time.time(),
                            "req": json.loads(resp.request.post_data or "{}"),
                            "resp": json.loads(body),
                        })
                        del self.list_responses[:-4]  # keep last 4
                except Exception:
                    pass
        self.c.page.on("response", on_response)

    def refresh_state(self):
        return self.c.page.evaluate("() => window.__emState()")

    def click(self, substr, value=None):
        return self.c.page.evaluate("([s, v]) => window.__emClick(s, v)", [substr, value])

    def poll(self, fn, want, timeout=25, interval=0.8, desc=""):
        t0 = time.time()
        last = None
        while time.time() - t0 < timeout:
            try:
                cur = fn()
                if want(cur):
                    return cur
                last = cur
            except Exception:
                pass
            time.sleep(interval)
        print(f"    [poll timeout] {desc}")
        return last

    # ---------- subject / category transitions ----------
    def open_category(self, cat):
        before_ids = sorted(s["id"] for s in self.refresh_state()["subjects"])
        tnames = [t["n"] for t in self.refresh_state()["topics"]]
        self.click("categoryID", cat["id"])
        def changed(s):
            ids = sorted(x["id"] for x in s["subjects"])
            t_n = [t["n"] for t in s["topics"]]
            return len(s["subjects"]) > 0 and (ids != before_ids or t_n != tnames)
        st = self.poll(lambda: self.refresh_state(), changed,
                       timeout=30, desc=f"category {cat['id']}")
        if st is None:
            # one retry
            self.click("categoryID", cat["id"])
            st = self.poll(lambda: self.refresh_state(), changed,
                           timeout=30, desc=f"category {cat['id']} retry")
        return st

    def open_subject(self, subj):
        """Click subject; wait for filter-box re-render (topics change) AND a
        questions-list reload captured AFTER the click. If nothing changes and
        the list already sits on page 1, treat the subject as already-active
        (default) and proceed. Returns (state, resp_marker)."""
        before = self.refresh_state()
        tn = [t["n"] for t in before["topics"]]
        n_resp = len(self.list_responses)
        ok = self.click("subjectID", subj["id"])
        if not ok:
            return before, None
        st = self.poll(lambda: self.refresh_state(),
                       lambda s: [t["n"] for t in s["topics"]] != tn and len(s["topics"]) > 0,
                       timeout=20, desc=f"subject {subj['id']}")
        got = self.poll(lambda: len(self.list_responses) > n_resp, lambda x: x,
                        timeout=12, desc="list reload")
        time.sleep(1.0)
        st = self.refresh_state()
        if st is None or [t["n"] for t in st["topics"]] == tn:
            # no re-render — subject was probably already active (default)
            badges = st.get("badges") or [] if st else []
            if any(b.startswith("1 - ") for b in badges) and st.get("questions"):
                return st, (n_resp if got else None)
            # one real retry, then give up
            ok = self.click("subjectID", subj["id"])
            time.sleep(4)
            st = self.refresh_state()
            tn2 = [t["n"] for t in st["topics"]]
            if tn2 == tn:
                return st, None
        return st, (n_resp if got else None)

    # ---------- question harvest ----------
    def latest_list_snapshot(self, min_idx=0, subject_id=None):
        """Return (fingerprint, serverMemo) from a captured list response that
        arrived at/after min_idx. memo = post-reload state of the component.
        Optionally require the request filters to match subject_id."""
        idx_lo = min(min_idx, len(self.list_responses))
        for r in reversed(self.list_responses[idx_lo:]):
            req = r.get("req", {})
            resp = r.get("resp", {})
            fp = req.get("fingerprint")
            memo = resp.get("serverMemo")
            if not (fp and memo):
                continue
            if subject_id is not None:
                f = (memo.get("data") or {}).get("filters") or {}
                if str(f.get("subjectID")) != str(subject_id):
                    continue
            return fp, memo
        return None, None

    def lw_list_call(self, fp, memo, method, params):
        body = {
            "fingerprint": dict(fp, path="topicalpastpapers"),
            "serverMemo": memo,
            "updates": [{"type": "callMethod", "payload": {
                "id": f"c{int(time.time()*1000)%100000}",
                "method": method, "params": params}}],
        }
        res = self.c.page.evaluate("""async (body) => {
            const csrf = window.livewire_token || '';
            const r = await fetch('/livewire/message/' + body.fingerprint.name, {
                method: 'POST',
                headers: {'Content-Type': 'application/json',
                          'Accept': 'text/html, application/xhtml+xml',
                          'X-Requested-With': 'XMLHttpRequest', 'X-Livewire': 'true',
                          'X-CSRF-TOKEN': csrf},
                credentials: 'include', body: JSON.stringify(body)
            });
            const t = await r.text();
            if (t.includes('One moment, please')) return {challenge: true, status: r.status};
            try { return {status: r.status, json: JSON.parse(t)}; }
            catch (e) { return {status: r.status, head: t.slice(0, 200)}; }
        }""", body)
        return res

    def goto_page_one(self, state):
        """Ensure the list sits on page 1 (badge '1 - N')."""
        badges = state.get("badges") or []
        if any(b.startswith("1 - ") for b in badges):
            return state
        if self.click("gotoPage", 1):
            state = self.poll(lambda: self.refresh_state(),
                              lambda s: any(b.startswith("1 - ") for b in (s.get("badges") or [])),
                              timeout=15, desc="gotoPage(1)") or self.refresh_state()
        return state

    def harvest_subject(self, cat, subj, state, resp_marker=None, max_pages=None):
        d = self.subject_dir(cat, subj)
        meta = {k: state[k] for k in ("topics", "zones", "papers", "seasons", "years")}
        meta.update({"category": cat, "subject": subj,
                     "badges": state["badges"],
                     "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
        json.dump(meta, open(f"{d}/meta.json", "w"), indent=1, ensure_ascii=False)

        qfile = f"{d}/questions.jsonl"
        seen = set()
        fout = open(qfile, "w")

        def write_cards(cards, page_no):
            n = 0
            for q in cards:
                if not q.get("qid") or q["qid"] in seen:
                    continue
                seen.add(q["qid"])
                rec = {"page": page_no, "categoryID": cat["id"], "subjectID": subj["id"],
                       "category": cat["label"], "subject": subj["label"], **q}
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n += 1
            fout.flush()
            return n

        # page 1: ensure we're on page 1, then harvest from DOM
        state = self.goto_page_one(state)
        n1 = write_cards(state["questions"], 1)
        badges = state["badges"]
        print(f"    page 1: +{n1} (total {len(seen)}) badges={badges[:2]}")

        # total pages from badge "X - Y" / total badge
        total = None
        for b in badges:
            if b.isdigit() and int(b) >= len(seen):
                total = int(b)
        max_pages_cap = min(200, ((total or 25 * len(seen)) + 24) // 25) if total else 60
        if max_pages:
            max_pages_cap = min(max_pages_cap, max_pages)

        # pagination: replay ONLY with a snapshot captured after this subject's
        # click (resp_marker) whose filters match the subject; else DOM fallback
        fp, memo = (None, None)
        if resp_marker is not None:
            fp, memo = self.latest_list_snapshot(min_idx=resp_marker, subject_id=subj["id"])
        stall = 0
        page = 2
        used_replay = bool(fp and memo)
        if used_replay:
            print("    pagination mode: livewire replay")
            while page <= max_pages_cap and stall < 2:
                if self.quota_exhausted:
                    break
                r = self.lw_list_call(fp, memo, "gotoPage", [page])
                if r.get("challenge"):
                    print("    [WAF] challenge during pagination — switch to DOM")
                    used_replay = False
                    break
                j = r.get("json")
                if not j or r.get("status") != 200:
                    print(f"    page {page}: bad response {r.get('status')} {str(r.get('head', ''))[:120]}")
                    stall += 1
                    if stall >= 2:
                        used_replay = False
                        break
                    continue
                htmlout = (j.get("effects") or {}).get("html") or ""
                cards = parse_cards_from_html(htmlout)
                new = write_cards(cards, page)
                if j.get("serverMemo"):
                    memo = j["serverMemo"]
                print(f"    page {page}: {len(cards)} cards (+{new}, total {len(seen)})")
                if new == 0:
                    stall += 1
                else:
                    stall = 0
                    state = self.refresh_state() if page % 10 == 0 else state
                page += 1
                time.sleep(0.55)
        if not used_replay:
            if fp and memo:
                print("    pagination mode: DOM fallback (replay unavailable/failed)")
                state = self.goto_page_one(self.refresh_state())
            else:
                print("    pagination mode: DOM fallback (no snapshot)")
            cur_state = state
            stall = 0
            page = 2
            for page in range(2, max_pages_cap + 1):
                if self.quota_exhausted:
                    break
                before_ids = {q["qid"] for q in cur_state["questions"]}
                if not cur_state.get("hasNext"):
                    break
                self.click("nextPage")
                cur_state = self.poll(
                    lambda: self.refresh_state(),
                    lambda s: s["questions"] and {q["qid"] for q in s["questions"]} != before_ids,
                    timeout=20, desc=f"dom page {page}")
                if not cur_state:
                    break
                new = write_cards(cur_state["questions"], page)
                print(f"    dom page {page}: +{new} (total {len(seen)})")
                if new == 0:
                    stall += 1
                    if stall >= 2:
                        break
                else:
                    stall = 0
                time.sleep(0.55)
        fout.close()
        return len(seen)

    def subject_dir(self, cat, subj):
        safe_cat = re.sub(r"[^\w.-]+", "_", cat["label"])[:40]
        safe_sub = re.sub(r"[^\w.-]+", "_", subj["label"])[:50]
        d = f"{BASE}/topical/{cat['id']}_{safe_cat}/{subj['id']}_{safe_sub}"
        os.makedirs(d, exist_ok=True)
        return d

    # ---------- main ----------
    def run(self, only_category=None, max_subjects=None, catalog_only=False,
            max_pages_per_subject=None, only_subject=None, skip_transitions=False):
        cats = self.catalog.get("categories") or self.refresh_state()["categories"]
        if not cats:
            cats = self.refresh_state()["categories"]
        self.catalog["categories"] = cats
        json.dump(self.catalog, open(CATALOG, "w"), indent=1, ensure_ascii=False)
        if skip_transitions:
            # harvest the CURRENTLY loaded state directly (default subject path)
            want_cat = only_category[0] if only_category else 3
            cat = next(c for c in cats if c["id"] == want_cat)
            subj = {"id": only_subject or 11, "label": "(current default)"}
            st = self.refresh_state()
            if st.get("questions"):
                n = self.harvest_subject(cat, subj, st, resp_marker=None,
                                         max_pages=max_pages_per_subject)
                print(f"OK: {n} questions (skip-transitions mode)")
            return
        if only_category:
            cats = [c for c in cats if c["id"] in only_category]
        for cat in cats:
            if self.quota_exhausted:
                print("\n[stop] quota exhausted — session done (resume later)")
                break
            print(f"\n=== CATEGORY {cat['id']} {cat['label']} ===")
            try:
                st = self.open_category(cat)
                subs = st["subjects"]
                self.catalog.setdefault("subjects_by_category", {})[str(cat["id"])] = subs
                json.dump(self.catalog, open(CATALOG, "w"), indent=1, ensure_ascii=False)
                print(f"  {len(subs)} subjects: {[s['label'][:24] for s in subs][:8]}...")
            except Exception:
                traceback.print_exc()
                continue
            if catalog_only:
                continue
            todo = subs[:max_subjects] if max_subjects else subs
            if only_subject:
                todo = [s for s in todo if s["id"] == only_subject]
            for subj in todo:
                if self.quota_exhausted:
                    print("\n[stop] quota exhausted — session done (resume later)")
                    break
                skey = f"{cat['id']}_{subj['id']}"
                if skey in self.progress["subjects_done"]:
                    print(f"  -- skip (done) {subj['label'][:40]}")
                    continue
                print(f"  -- subject {subj['id']} {subj['label'][:50]!r}")
                try:
                    st2, marker = self.open_subject(subj)
                    if st2 is None:
                        print("     click failed — skip")
                        continue
                    n = self.harvest_subject(cat, subj, st2, resp_marker=marker,
                                             max_pages=max_pages_per_subject)
                    if self.quota_exhausted:
                        self.progress["subjects_partial"][skey] = n
                        print(f"     PARTIAL (quota): {n} questions")
                    else:
                        self.progress["subjects_done"].append(skey)
                        print(f"     OK: {n} questions")
                    json.dump(self.progress, open(PROGRESS, "w"), indent=1)
                except Exception:
                    traceback.print_exc()
                time.sleep(0.6)

    def close(self):
        self.c.close()


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cats", nargs="?", default="", help="comma-separated category IDs")
    ap.add_argument("--max-subjects", type=int, default=None)
    ap.add_argument("--catalog-only", action="store_true")
    ap.add_argument("--max-pages", type=int, default=None, help="cap pages per subject")
    ap.add_argument("--subject", type=int, default=None, help="only this subject ID")
    ap.add_argument("--skip-transitions", action="store_true",
                    help="harvest the currently-loaded default state without clicks")
    a = ap.parse_args()
    only = [int(x) for x in a.cats.split(",")] if a.cats else None
    cr = Crawler()
    try:
        cr.run(only_category=only, max_subjects=a.max_subjects,
               catalog_only=a.catalog_only, max_pages_per_subject=a.max_pages,
               only_subject=a.subject, skip_transitions=a.skip_transitions)
    finally:
        cr.close()
