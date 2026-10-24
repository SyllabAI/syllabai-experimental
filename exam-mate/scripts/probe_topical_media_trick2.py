#!/usr/bin/env python3
"""Probe v2 (urllib-only, no browser): anonymous GET semantics of exam-mate media roots.

v1 finding: fresh headless Chromium gets a 7183B HTML interstitial, but PLAIN urllib
(no referer/cookies) retrieved the exact 2019 topical PNG (38,507B, ledger match).
So the media layer is open to plain HTTP clients; browser-fingerprint challenge only.

This probe (all plain urllib, 1 req each unless noted):
  A. chapterized-topical controls via urllib (sha256 vs ledger)
  B. negative variants -> 404-vs-200 semantics (wrong kind / src_qid / qfolder / dir)
  C. adjacency semantic check: src_qid+1 (1 request; establishes whether ids are
     dense/enumerable -- NOT an enumeration attempt, sample size 1)
  D. untopical bank media via urllib (prior record said page-context needed -- retest)
  E. live 4MA1 topical LISTING html via urllib (server-rendered Livewire): year inputs,
     lock chips, any 2020+ strings
  F. Wayback CDX retry (120s cap; unreachable is a finding too)

Artifacts -> exam-mate-probe/pp2026/topical_media_trick2.json
"""

import hashlib, json, os, re, time, urllib.request, urllib.error

ORIGIN = "https://www.exam-mate.com"
PROBE = "/home/z/my-project/exam-mate-probe/pp2026"
OUT = os.path.join(PROBE, "topical_media_trick2.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return {"status": r.status, "ct": r.headers.get("content-type", ""),
                    "bytes": r.read()}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "ct": e.headers.get("content-type", ""),
                "bytes": e.read()[:500]}
    except Exception as e:
        return {"status": None, "err": str(e), "bytes": b""}
    finally:
        pass

def summarize(r, expect_sha=None, sha_prefix=False, expect_bytes=None):
    d = {"status": r["status"], "ct": r["ct"][:40], "size": len(r["bytes"]),
         "first4": r["bytes"][:4].decode("latin1")}
    if r["bytes"][:4] == b"\x89PNG":
        d["png"] = True
        h = hashlib.sha256(r["bytes"]).hexdigest()
        d["sha256"] = h
        if expect_sha:
            d["sha_match"] = h == expect_sha if not sha_prefix else h.startswith(expect_sha)
        if expect_bytes:
            d["size_match"] = len(r["bytes"]) == expect_bytes
    return d

def main():
    res = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    # A. controls (chapterized topical bank, /questions/ root)
    controls = [
        ("4MA1_q_2019W_Q23", f"{ORIGIN}/questions/33597/124742/33597_q_124742_23_1.png",
         "4aab3f98f6e11ab0148755904508cb11e600fa00c9fc75e0a508447f95d7163b", False, 38507),
        ("4MA1_a_2019W_Q23", f"{ORIGIN}/questions/33597/124742/33597_a_124742_23_1.png",
         "5be7b2118096", True, 17024),
        ("H432_q_2019S_Q6", f"{ORIGIN}/questions/30176/115130/30176_q_115130_6_1.png",
         "9a98654b59fe", True, 74753),
    ]
    A = {}
    for name, url, sha, pre, nb in controls:
        A[name] = {"url": url, **summarize(get(url), sha, pre, nb)}
    res["A_topical_controls_urllib"] = A

    # B. negative variants (all on known qfolder/src_qid)
    B = {}
    variants = [
        ("wrong_kind",   f"{ORIGIN}/questions/33597/124742/33597_x_124742_23_1.png"),
        ("wrong_qnum",   f"{ORIGIN}/questions/33597/124742/33597_q_124742_24_1.png"),
        ("wrong_srcqid", f"{ORIGIN}/questions/33597/124742/33597_q_115130_23_1.png"),
        ("wrong_qfolder",f"{ORIGIN}/questions/999999/124742/999999_q_124742_23_1.png"),
        ("dir_list",     f"{ORIGIN}/questions/33597/124742/"),
        ("missing_tail", f"{ORIGIN}/questions/33597/124742/"),
    ]
    for name, url in variants[:5]:
        B[name] = summarize(get(url))
    res["B_topical_variants_urllib"] = B

    # C. adjacency semantics: src_qid+1 under same qfolder (exactly one request)
    C = summarize(get(f"{ORIGIN}/questions/33597/124742/33597_q_124743_23_1.png"))
    res["C_adjacency_srcqid_plus1"] = C

    # D. untopical bank media via plain urllib (retest of page-context claim)
    D = summarize(get(f"{ORIGIN}/media/questions/519564/0452_s25_qp_23_Q5-1.png"))
    res["D_untopical_media_urllib"] = D

    # E. live listing page via urllib (server-rendered initial Livewire HTML)
    r = get(f"{ORIGIN}/topicalpastpapers", timeout=60)
    html = r["bytes"].decode("utf-8", "replace") if r["status"] == 200 else ""
    years_inputs = sorted(set(re.findall(r'name="years\[\]"[^>]*value="([^"]+)"', html)))
    res["E_live_4MA1_listing_urllib"] = {
        "status": r["status"], "bytes": len(r["bytes"]),
        "looks_like_app": "Livewire" in html or "wire:id" in html,
        "years_inputs": years_inputs,
        "lock_chips": html.count("fa-lock"),
        "img_paths": len(re.findall(r'/questions/\d+/\d+/[^"\']+\.png', html)),
        "select_question_calls": html.count("selectQuestion("),
        "strings_2020plus": sorted(set(re.findall(r'20(2[0-6])', html)))[:10],
        "challenge_page": "challenge" in html.lower() or len(r["bytes"]) == 7183,
    }

    # F. Wayback CDX retry (long timeout; unreachable is a finding)
    F = {}
    for tag, q in [("topical", "exam-mate.com/topicalpastpapers*"),
                   ("media", "exam-mate.com/questions/*")]:
        u = (f"https://web.archive.org/cdx/search/cdx?url={q}&output=json"
             f"&fl=timestamp,original,statuscode&collapse=urlkey&limit=300")
        t0 = time.time()
        rr = get(u, timeout=120)
        F[tag] = {"status": rr["status"], "secs": round(time.time() - t0, 1),
                  "is_json": rr["bytes"][:1] == b"["}
        if F[tag]["is_json"]:
            rows = json.loads(rr["bytes"].decode("utf-8", "replace"))
            F[tag]["captures"] = len(rows) - 1 if rows else 0
            F[tag]["sample"] = rows[1:6] if len(rows) > 1 else []
    res["F_wayback_cdx"] = F

    json.dump(res, open(OUT, "w"), indent=1)
    for sec in ("A_topical_controls_urllib", "B_topical_variants_urllib"):
        print(f"== {sec} ==")
        for k, v in res[sec].items():
            print(f"  {k:14s} {v['status']} size={v['size']:6d} png={v.get('png')} "
                  f"sha_match={v.get('sha_match')} ct={v['ct'][:20]}")
    print("== C adjacency src_qid+1 ==", res["C_adjacency_srcqid_plus1"])
    print("== D untopical via urllib ==", res["D_untopical_media_urllib"])
    print("== E live listing ==")
    for k, v in res["E_live_4MA1_listing_urllib"].items():
        print(f"  {k}: {v}")
    print("== F wayback ==")
    for k, v in res["F_wayback_cdx"].items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
