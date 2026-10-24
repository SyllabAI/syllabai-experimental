#!/usr/bin/env python3
"""Probe v3: clean semantics for ambiguous URLs from v2 (which hit the sporadic
'One moment, please...' 200-HTML anti-burst challenge). Strategy: challenge-aware
retry (200 + HTML => sleep & retry), 2.5s spacing, max 5 tries.

Also: extract one full selectQuestion payload from the already-saved real listing
HTML to document the payload->media-URL binding (no request needed).

Artifacts -> exam-mate-probe/pp2026/topical_media_trick3.json
"""
import hashlib, html as htmlmod, json, os, re, time, urllib.request, urllib.error

ORIGIN = "https://www.exam-mate.com"
PROBE = "/home/z/my-project/exam-mate-probe/pp2026"
OUT = os.path.join(PROBE, "topical_media_trick3.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

def get_retry(url, tries=5):
    last = {"status": None, "err": "no-attempt", "bytes": b""}
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                last = {"status": r.status, "ct": r.headers.get("content-type", ""),
                        "bytes": r.read()}
        except urllib.error.HTTPError as e:
            last = {"status": e.code, "ct": e.headers.get("content-type", ""),
                    "bytes": e.read()[:800]}
        except Exception as e:
            last = {"status": None, "err": str(e), "bytes": b""}
        body = last.get("bytes", b"")
        challenged = (last.get("status") == 200
                      and b"text/html" in last.get("ct", "").encode()
                      and (b"One moment" in body or b"setTimeout" in body))
        if not challenged:
            return last, i + 1, challenged
        time.sleep(6 + 2 * i)
    return last, tries, True

def summarize(r):
    d = {"status": r["status"], "ct": r.get("ct", "")[:40], "size": len(r.get("bytes", b"")),
         "first4": r.get("bytes", b"")[:4].decode("latin1")}
    if r.get("bytes", b"")[:4] == b"\x89PNG":
        d["png"] = True
        d["sha256"] = hashlib.sha256(r["bytes"]).hexdigest()
    return d

def main():
    res = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    # payload format from saved real listing HTML (no request)
    t = open(os.path.join(PROBE, "inters_listing.html"), encoding="utf-8", errors="replace").read()
    m = re.search(r"selectQuestion\((\d+),(\d+),'((?:[^'\\]|\\.)*)'\)", t)
    payload_doc = None
    if m:
        raw = htmlmod.unescape(m.group(3)).encode().decode("unicode_escape", "replace")
        try:
            pj = json.loads(raw)
            payload_doc = {"row_qid": m.group(1), "keys": list(pj.keys())[:12],
                           "question_images": pj.get("question_images", [])[:2],
                           "answer_images": pj.get("answer_images", [])[:2],
                           "paper_hint": {k: pj[k] for k in pj if k in
                                          ("paper", "year", "season", "question_no", "session", "subject")}}
        except Exception as e:
            payload_doc = {"parse_error": str(e), "raw_head": raw[:300]}
    res["payload_format"] = payload_doc

    urls = [
        ("H432_ctrl_2019", f"{ORIGIN}/questions/30176/115130/30176_q_115130_6_1.png"),
        ("untopical_2025", f"{ORIGIN}/media/questions/519564/0452_s25_qp_23_Q5-1.png"),
        ("wrong_qnum",     f"{ORIGIN}/questions/33597/124742/33597_q_124742_24_1.png"),
        ("wrong_srcqid",   f"{ORIGIN}/questions/33597/124742/33597_q_115130_23_1.png"),
        ("wrong_qfolder",  f"{ORIGIN}/questions/999999/124742/999999_q_124742_23_1.png"),
    ]
    R = {}
    for name, u in urls:
        r, tries, ch = get_retry(u)
        d = summarize(r)
        d["tries"] = tries
        d["was_challenged_then_ok"] = ch
        R[name] = {"url": u, **d}
        time.sleep(2.5)
    res["results"] = R
    json.dump(res, open(OUT, "w"), indent=1)

    print("payload_format:", json.dumps(payload_doc, indent=1)[:600])
    for k, v in R.items():
        print(f"{k:14s} status={v['status']} ct={v['ct'][:24]} size={v['size']:6d} "
              f"png={v.get('png')} tries={v['tries']}")

if __name__ == "__main__":
    main()
