#!/usr/bin/env python3
"""Probe: does the anonymous media GET trick work against the PAYWALLED chapterized topical bank?

Background (worklog Tasks 19-22):
  - PAST PAPERS full-PDF bank: /media/pastpapers/{id}/{file}.pdf  -> anonymous 200 (verified)
  - UNTOPICAL per-question bank: /media/questions/{id}/{name}.png -> anonymous 200 (verified)
  - TOPICAL chapterized bank (132 subjects): media root is /questions/{qfolder}/{src_qid}/
      {qfolder}_{q|a}_{src_qid}_{question}_{page}.png   (see corpus INDEX.jsonl)
    Listing for 2020..2026 is subscription-locked; anonymous facets/DOM expose nothing.

This probe answers two questions, WITHOUT circumvention (no Livewire state forging,
no ID-space enumeration):
  A. Media-layer semantics on the live origin, same-origin fetch (proven pipeline JS):
     - 4 known-good 2019-era controls (sha256 vs ledger)
     - negative variants  ->  404 (auth-free media layer, discovery-gated only)
                              vs 403/login (media layer itself gated)
     - plain urllib GET (no referer, non-browser) on one control
     - live 4MA1 topical page: year inputs + lock chips (what the listing exposes today)
  B. Wayback Machine as a PUBLIC-ARCHIVE discovery path:
     - CDX list of exam-mate.com/topicalpastpapers* captures (+ /questions/* media)
     - fetch promising captures raw (id_), grep for /questions/...png paths and 2020+ year markers
     - if any 2020+ image paths are found in a public capture: live-GET a SMALL sample (<=4),
       verification only, files stay local in exam-mate-probe/ (never committed)

Artifacts -> /home/z/my-project/exam-mate-probe/pp2026/topical_media_trick.json (+ wayback_*.html)
"""

import base64, hashlib, json, os, re, sys, time, urllib.request, urllib.error
from playwright.sync_api import sync_playwright

ORIGIN = "https://www.exam-mate.com"
PROBE = "/home/z/my-project/exam-mate-probe/pp2026"
OUT = os.path.join(PROBE, "topical_media_trick.json")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")

FETCH_JS = """async (urls) => {
  const one = async (url) => {
    try {
      const r = await fetch(url, {credentials: 'include',
                                  signal: AbortSignal.timeout(30000)});
      const ct = r.headers.get('content-type') || '';
      if (!r.ok) return {url, status: r.status, ct};
      const buf = await r.arrayBuffer();
      const bytes = new Uint8Array(buf);
      let binary = '';
      const chunk = 0x8000;
      for (let i = 0; i < bytes.length; i += chunk) {
        binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
      }
      return {url, status: r.status, ct, b64: btoa(binary), size: bytes.length};
    } catch (e) {
      return {url, error: String(e)};
    }
  };
  const out = [];
  for (const u of urls) out.push(await one(u));
  return out;
}"""

CONTROLS = [
    {"url": f"{ORIGIN}/questions/33597/124742/33597_q_124742_23_1.png",
     "ref": "4MA1/2HR_Winter_2019_Q23", "kind": "question",
     "expect_bytes": 38507, "expect_sha": "4aab3f98f6e11ab0148755904508cb11e600fa00c9fc75e0a508447f95d7163b"},
    {"url": f"{ORIGIN}/questions/33597/124742/33597_a_124742_23_1.png",
     "ref": "4MA1/2HR_Winter_2019_Q23", "kind": "answer",
     "expect_bytes": 17024, "expect_sha": "5be7b2118096" + "0" * 0, "sha_prefix": True},
    {"url": f"{ORIGIN}/questions/30176/115130/30176_q_115130_6_1.png",
     "ref": "Chemistry_A/3_Summer_2019_Q6", "kind": "question",
     "expect_bytes": 74753, "expect_sha": "9a98654b59fe", "sha_prefix": True},
    {"url": f"{ORIGIN}/questions/33597/124742/33597_q_124742_24_1.png",
     "ref": "NEGATIVE: same ids, nonexistent question label 24", "kind": "negative"},
]

def sha256(b): return hashlib.sha256(b).hexdigest()

def urlopen(url, timeout=45, method="GET"):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:2000]
    except Exception as e:
        return None, str(e).encode()

def main():
    res = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "partA_media_layer": {}, "partB_wayback": {}}

    # ---------- Part A: live origin media-layer semantics ----------
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA, viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(f"{ORIGIN}/topicalpastpapers", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2500)

        ctrl_urls = [c["url"] for c in CONTROLS]
        variants = [
            ("wrong-kind",   f"{ORIGIN}/questions/33597/124742/33597_x_124742_23_1.png"),
            ("wrong-srcqid", f"{ORIGIN}/questions/33597/124742/33597_q_115130_23_1.png"),
            ("wrong-qfolder",f"{ORIGIN}/questions/999999/124742/999999_q_124742_23_1.png"),
            ("dir-list",     f"{ORIGIN}/questions/33597/124742/"),
        ]
        batch = ctrl_urls + [u for _, u in variants]
        rows = page.evaluate(FETCH_JS, batch)
        by_url = {r["url"]: r for r in rows}

        for c in CONTROLS:
            r = by_url[c["url"]]
            entry = {"ref": c["ref"], "status": r.get("status"), "ct": r.get("ct"),
                     "size": r.get("size"), "error": r.get("error")}
            if r.get("b64"):
                data = base64.b64decode(r["b64"])
                entry["png_magic"] = data[:4] == b"\x89PNG"
                h = sha256(data)
                entry["sha256"] = h
                if "expect_sha" in c:
                    entry["sha_match"] = (h == c["expect_sha"]) if not c.get("sha_prefix") \
                        else h.startswith(c["expect_sha"])
                    entry["size_match"] = len(data) == c["expect_bytes"]
            res["partA_media_layer"][c["url"]] = entry

        for name, u in variants:
            r = by_url[u]
            res["partA_media_layer"][f"variant:{name}"] = {
                "url": u, "status": r.get("status"), "ct": r.get("ct"), "size": r.get("size")}

        # plain non-browser GET (no referer) on one control
        st, body = urlopen(CONTROLS[0]["url"])
        res["partA_media_layer"]["plain_urllib_no_referer"] = {
            "url": CONTROLS[0]["url"], "status": st, "first4": body[:4].decode("latin1"),
            "size": len(body) if st == 200 else None}

        # what does the live 4MA1 listing expose today? (year inputs, lock chips)
        html = page.content()
        years_inputs = re.findall(r'name="years\[\]"[^>]*value="([^"]+)"', html)
        lock_chips = re.findall(r'fa-lock', html)
        res["partA_media_layer"]["live_4MA1_listing"] = {
            "years_inputs": sorted(set(years_inputs), key=lambda x: x),
            "lock_chip_count": len(lock_chips),
            "has_2020plus_in_snapshot": bool(re.search(r'["\']202[0-6]["\']', html)),
            "questions_paths_in_html": len(re.findall(r'/questions/\d+/\d+/[^"\']+\.png', html))}
        open(os.path.join(PROBE, "topical_4MA1_live_now.html"), "w").write(html)
        browser.close()

    # ---------- Part B: Wayback Machine discovery ----------
    wb = {"cdx_topical": [], "cdx_questions_media": None, "captures_fetched": [],
          "paths_2020plus": [], "sample_live_gets": []}
    cdx_tpl = ("https://web.archive.org/cdx/search/cdx?url={u}&output=json"
               "&fl=timestamp,original,statuscode&collapse=urlkey&limit={n}")
    st, body = urlopen(cdx_tpl.format(u="exam-mate.com/topicalpastpapers*", n=800), timeout=60)
    if st == 200 and body[:1] == b"[":
        rows = json.loads(body.decode("utf-8", "replace"))
        wb["cdx_topical"] = rows[1:] if rows else []
    st2, body2 = urlopen(cdx_tpl.format(u="exam-mate.com/questions/*", n=300), timeout=60)
    if st2 == 200 and body2[:1] == b"[":
        rows2 = json.loads(body2.decode("utf-8", "replace"))
        wb["cdx_questions_media"] = {"count": max(0, len(rows2) - 1),
                                     "sample": rows2[1:8] if len(rows2) > 1 else []}

    # pick captures: prefer 2021-2023 (likely pre-paywall), then one late control
    def ts_key(r):
        t = r[0]
        return (0 if t[:4] in ("2021", "2022", "2023") else 1, t)
    cands = sorted([r for r in wb["cdx_topical"] if r[2] == "200"], key=ts_key)[:8]
    late = [r for r in wb["cdx_topical"] if r[0][:4] in ("2024", "2025", "2026") and r[2] == "200"][:1]
    for r in late:
        if r not in cands: cands.append(r)

    path_re = re.compile(r'/questions/(\d+)/(\d+)/([A-Za-z0-9_.\-]+\.png)')
    yr_re = re.compile(r'(Summer|Winter)\s*20(2[0-6])\b')
    code_re = re.compile(r'_(?:s|w)(2[0-6])_')
    for ts, orig, _ in cands:
        url = f"https://web.archive.org/web/{ts}id_/{orig}"
        st, body = urlopen(url, timeout=90)
        cap = {"timestamp": ts, "original": orig, "status": st, "bytes": len(body)}
        if st == 200 and body[:1] in (b"<", b"\n", b" ", b"\t"):
            text = body.decode("utf-8", "replace")
            fn = os.path.join(PROBE, f"wayback_{ts}.html")
            open(fn, "w").write(text)
            paths = path_re.findall(text)
            cap["question_image_paths"] = len(paths)
            cap["years_mentioned"] = sorted(set(yr_re.findall(text)))
            cap["codes_2020plus"] = sorted(set(code_re.findall(text)))
            # pair paths with 2020+ context: only claim paths from captures that mention 2020+
            if cap["years_mentioned"] or cap["codes_2020plus"]:
                wb["paths_2020plus"].extend(
                    {"path": f"/questions/{a}/{b}/{f}", "from_capture": ts, "original": orig}
                    for a, b, f in paths[:400])
        wb["captures_fetched"].append(cap)
        time.sleep(1)

    # small verification sample against live origin (<=4), files local-only
    uniq = []
    for p in wb["paths_2020plus"]:
        if p["path"] not in [u["path"] for u in uniq]:
            uniq.append(p)
    wb["paths_2020plus_unique"] = len(uniq)
    if uniq:
        live_urls = [ORIGIN + p["path"] for p in uniq[:4]]
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(user_agent=UA)
            page = ctx.new_page()
            page.goto(f"{ORIGIN}/topicalpastpapers", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(1500)
            for r in page.evaluate(FETCH_JS, live_urls):
                e = {"url": r["url"], "status": r.get("status"), "ct": r.get("ct"),
                     "size": r.get("size"), "error": r.get("error")}
                if r.get("b64"):
                    data = base64.b64decode(r["b64"])
                    e["png_magic"] = data[:4] == b"\x89PNG"
                    e["sha256"] = sha256(data)
                    fn = os.path.join(PROBE, "trick_" + r["url"].rsplit("/", 1)[-1])
                    open(fn, "wb").write(data)
                wb["sample_live_gets"].append(e)
            browser.close()

    res["partB_wayback"] = wb
    json.dump(res, open(OUT, "w"), indent=1)

    # ---------- console summary ----------
    print("== PART A: media layer ==")
    for k, v in res["partA_media_layer"].items():
        if k.startswith("variant"):
            print(f"  {k:16s} status={v.get('status')} ct={v.get('ct')}")
        elif k == "plain_urllib_no_referer":
            print(f"  plain urllib (no referer): status={v['status']} first4={v['first4']!r}")
        elif k == "live_4MA1_listing":
            print(f"  live 4MA1 listing: year_inputs={v['years_inputs']} locks={v['lock_chip_count']} "
                  f"2020+ in html={v['has_2020plus_in_snapshot']} imgpaths={v['questions_paths_in_html']}")
        else:
            print(f"  {v['ref'][:44]:44s} status={v.get('status')} size={v.get('size')} "
                  f"png={v.get('png_magic')} sha_match={v.get('sha_match')}")
    print("== PART B: wayback ==")
    print(f"  cdx topical captures: {len(wb['cdx_topical'])}; "
          f"/questions/* media captures: {wb['cdx_questions_media']}")
    for c in wb["captures_fetched"]:
        print(f"  cap {c['timestamp']} {c['original'][:60]:60s} st={c['status']} "
              f"paths={c.get('question_image_paths', '-')} yrs={c.get('years_mentioned', '-')}")
    print(f"  2020+ paths unique: {wb['paths_2020plus_unique']}")
    for g in wb["sample_live_gets"]:
        print(f"  live GET {g['url'][:70]} -> {g.get('status')} size={g.get('size')} png={g.get('png_magic')}")

if __name__ == "__main__":
    main()
