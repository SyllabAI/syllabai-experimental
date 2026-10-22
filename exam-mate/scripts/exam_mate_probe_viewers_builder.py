#!/usr/bin/env python3
"""exam-mate viewers + Build Exam/Worksheet probe (2026-10-23 session).

Consolidated, sanitized probe for the two feature families reverse-
engineered in research/2026-10-23-exam-mate-build-exam-and-viewers.md:

  A. /pastpapers  — yearly past-paper viewer (PDF tabs, QP/MS choosable)
  B. /myexams|/list — Build Exam or Worksheet editor + PDF export modes

Usage:
  python3 exam_mate_probe_viewers_builder.py viewers   # anonymous, pastpapers
  python3 exam_mate_probe_viewers_builder.py builder   # needs an account:
      #   edit ACCOUNT_EMAIL / ACCOUNT_PASSWORD or set env vars
Requires exam_mate_client.py (WAF-immune fixed-fingerprint Chromium client).

IMPORTANT (session 2026-10-23 learnings):
  * log in INSIDE the working browser context — a saved exam_mate_session
    cookie restored into a fresh context is rejected by the app (the WAF
    clearance alone is not enough); "only 2 active sessions per account".
  * the export tab's build table refreshes via wire:poll.10s.visible —
    activate the tab (a[href="#export"]) before polling.
  * exportMode1/2 + exportAnswers return HTTP 500 for non-subscribed
    accounts (verified; see research note §4.4/§5).
"""
import json, os, re, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_mate_client import ExamMateClient  # noqa: E402

ACCOUNT_EMAIL = os.environ.get("EXAM_MATE_EMAIL", "")
ACCOUNT_PASSWORD = os.environ.get("EXAM_MATE_PASSWORD", "")
OUT = os.environ.get("PROBE_OUT", "/tmp/exam-mate-probe")


def jsclick(c, sel):
    return c.page.evaluate(f"""() => {{
        const el = document.querySelector({json.dumps(sel)});
        if (!el) return 'missing';
        el.click(); return 'clicked';
    }}""")


def decode_wire(post_data):
    """v2.12 flat body: {fingerprint, serverMemo, updates[]}."""
    j = json.loads(post_data)
    fp = j.get("fingerprint", {})
    calls, syncs = [], {}
    for u in j.get("updates", []):
        p = u.get("payload", {})
        if u.get("type") == "callMethod":
            calls.append((p.get("method"), p.get("params")))
        elif u.get("type") == "syncInput":
            syncs[p.get("name")] = p.get("value")
    return {"comp": fp.get("name"), "calls": calls, "syncs": syncs,
            "data": j.get("serverMemo", {}).get("data")}


def probe_viewers(c):
    """Anonymous: /pastpapers components, paper list, viewer PDFs, download."""
    c.fetch("https://www.exam-mate.com/pastpapers")
    time.sleep(1.5)
    c.xhr_log.clear()

    jsclick(c, "[wire\\:click=\"$set('categoryID', 3)\"]")
    time.sleep(3)
    jsclick(c, "[wire\\:click=\"$set('subjectID', 11)\"]")
    time.sleep(3)
    c.page.evaluate("() => { const b = document.querySelector('.filter-button'); if (b) b.click(); }")
    time.sleep(4.5)

    rows = c.page.evaluate(
        "() => Array.from(document.querySelectorAll('#paper-list li[wire\\\\:click]'))"
        ".map(li => li.getAttribute('wire:click') + ' :: ' + li.innerText.trim())")
    print("paper rows:", rows[:5])

    c.page.evaluate("""() => {
        const li = document.querySelector('#paper-list li[wire\\\\:click*="selectPastpaper"]');
        if (li) li.click();
    }""")
    time.sleep(4)

    viewer = c.page.evaluate("""() => ({
        iframes: Array.from(document.querySelectorAll('iframe')).map(f => f.src)
                    .filter(s => /media|pdf/i.test(s)),
        tabs: Array.from(document.querySelectorAll('[data-bs-toggle="tab"]'))
              .map(a => a.getAttribute('href')).filter(h => h && h.includes('tab')),
        nav: Array.from(document.querySelectorAll('[onclick*="elect"]'))
            .map(e => e.getAttribute('onclick')).slice(0, 4)
    })""")
    print("viewer:", json.dumps(viewer, indent=1))

    for x in c.xhr_log:
        if "/livewire/message" in x["url"] and x.get("post_data"):
            d = decode_wire(x["post_data"])
            print(f"wire {d['comp']}: calls={d['calls']} syncs={json.dumps(d['syncs'])[:120]}")
            print(f"   data={json.dumps(d['data'])[:300]}")

    if viewer["iframes"]:
        out = os.path.join(OUT, "qp_anon.pdf")
        c.download(viewer["iframes"][0], out)
        head = open(out, "rb").read(5)
        print(f"anonymous PDF download: {os.path.getsize(out)} bytes, head={head}")


def probe_builder(c):
    """Authenticated: create exam, editor anatomy, export modes, gating."""
    assert ACCOUNT_EMAIL and ACCOUNT_PASSWORD, "set EXAM_MATE_EMAIL/PASSWORD"
    c.fetch("https://www.exam-mate.com/login")
    time.sleep(1.2)
    c.page.fill("input[name=email]", ACCOUNT_EMAIL)
    c.page.fill("input[name=password]", ACCOUNT_PASSWORD)
    c.page.click("button:has-text('Log In')")
    time.sleep(3)
    print("logged in ->", c.page.evaluate("() => location.href"))

    c.fetch("https://www.exam-mate.com/myexams")
    time.sleep(2)
    c.page.evaluate("""() => {
        const inp = document.querySelector('#exam-name');
        if (inp) { inp.focus(); inp.value = 'probe-exam';
            inp.dispatchEvent(new Event('input', {bubbles: true})); }
    }""")
    c.page.evaluate("""() => {
        const b = document.querySelector('#new-exam-modal button[wire\\\\:click="createExam"]');
        if (b) b.click();
    }""")
    time.sleep(4)
    url = c.page.evaluate("() => location.href")
    print("exam editor:", url)

    html = c.page.content()
    open(os.path.join(OUT, "exam_editor.html"), "w").write(html)
    print("tabs:", sorted(set(re.findall(r'href="#(\\w[\\w-]*)"', html))))
    print("export samples:", sorted(set(re.findall(r'storage/([a-z0-9_]+\\.pdf)', html))))
    print("export methods:", sorted(set(re.findall(r'wire:click="(export\\w+)"', html))))
    print("state props:", sorted(set(re.findall(r'wire:model(?:\\.defer)?="(state\\.[\\w_]+)"', html))))
    print("quota badge ctx:", re.findall(r'(\\d+ / \\d+)\\s*</span>\\s*PDF', html)[:3])


def main():
    os.makedirs(OUT, exist_ok=True)
    what = sys.argv[1] if len(sys.argv) > 1 else "viewers"
    c = ExamMateClient(restore_state=False, verbose=False)
    try:
        if what == "viewers":
            probe_viewers(c)
        elif what == "builder":
            probe_builder(c)
        else:
            print(__doc__)
    finally:
        c.close()


if __name__ == "__main__":
    main()
