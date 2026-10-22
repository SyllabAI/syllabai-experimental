#!/usr/bin/env python3
"""exam-mate AI features probe (2026-10-23 session).

Targets the three free AI features (+ sibling mockexam route):
  /prediction-exam   AI Exam Prediction (Free)
  /revision          AI Revision Assistant (Free)
  /exam-marker       AI Exam Marker (Free)
  /mockexam          AI Mock Exam (Free, same nav family)

Usage:
  python3 -u exam_mate_probe_ai.py recon          # anonymous + auth dumps of all 4 routes
  python3 -u exam_mate_probe_ai.py interact       # phase 2: drive the actual AI flows

Artifacts -> /home/z/my-project/exam-mate-probe/4x_*.html/.png/.json (local only).
Session learnings that still apply:
  * log in INSIDE the working browser context (cookie restore across contexts fails)
  * run with: python3 -u  (stdout block buffering when piped)
"""
import json, os, re, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exam_mate_client import ExamMateClient  # noqa: E402

PROBE = "/home/z/my-project/exam-mate-probe"
BASE = "https://www.exam-mate.com"
ROUTES = ["prediction-exam", "revision", "exam-marker", "mockexam"]


def account():
    d = json.load(open(f"{PROBE}/research_account.json"))
    return d["email"], d["password"]


def js(c, expr):
    try:
        return c.page.evaluate(expr)
    except Exception as e:
        return f"<error {str(e)[:80]}>"


def snapshot_dom(c):
    """Component inventory + forms + wire actions + visible text."""
    comps = js(c, """() => Array.from(document.querySelectorAll('[wire\\\\:id]')).map(el => {
        const raw = el.getAttribute('wire:initial-data') || '';
        let name = null, memo = null;
        try { const j = JSON.parse(raw);
              name = (j.fingerprint || {}).name || null;
              memo = j.serverMemo ? Object.keys(j.serverMemo.data || {}) : null;
        } catch(e) { const m = raw.match(/"name":"([^"]+)"/); name = m ? m[1] : null; }
        return {id: el.getAttribute('wire:id'), name, memo};
    })""")
    forms = js(c, """() => Array.from(document.querySelectorAll('input,select,textarea')).map(e => ({
        tag: e.tagName.toLowerCase(), type: e.type || null, name: e.name || null,
        model: e.getAttribute('wire:model') || e.getAttribute('wire:model.defer')
               || e.getAttribute('x-model') || null,
        ph: (e.placeholder || '').slice(0, 60), id: e.id || null,
        accept: e.accept || null, options: e.tagName === 'SELECT' ? e.options.length : null
    }))""")
    actions = js(c, """() => Array.from(document.querySelectorAll('[wire\\\\:click]')).map(e =>
        e.getAttribute('wire:click') + ' :: ' + (e.innerText || '').trim().slice(0, 50)).slice(0, 80)""")
    alpine = js(c, """() => Array.from(document.querySelectorAll('[x-data],[\\\\@click],[x-on\\\\:click]')).length""")
    text = js(c, "() => (document.body.innerText || '').replace(/\\n{2,}/g, '\\n').slice(0, 2600)")
    ext = js(c, """() => {
        const urls = new Set();
        document.querySelectorAll('script[src],iframe,form[action]').forEach(e => {
            const u = e.src || e.getAttribute('action');
            if (u && !u.includes('exam-mate')) urls.add(u);
        });
        return Array.from(urls);
    }""")
    return {"components": comps, "forms": forms, "wire_actions": actions,
            "alpine_nodes": alpine, "text": text, "external": ext}


def dump(c, tag, route):
    final = c.page.evaluate("() => location.href")
    html = c.page.content()
    hp = f"{PROBE}/{tag}_{route}.html"
    open(hp, "w").write(html)
    try:
        c.page.screenshot(path=f"{PROBE}/{tag}_{route}.png", full_page=False)
    except Exception:
        pass
    snap = snapshot_dom(c)
    open(f"{PROBE}/{tag}_{route}.dom.json", "w").write(json.dumps(snap, indent=1))
    wire = [x for x in c.xhr_log if "/livewire/message" in x["url"] or "xhr" in x["url"]]
    open(f"{PROBE}/{tag}_{route}.wire.json", "w").write(json.dumps(c.xhr_log, indent=1))
    comps = [x["name"] for x in snap["components"] if x.get("name")]
    print(f"\n===== {tag} /{route} -> {final}  ({len(html)}b) =====")
    print(f"components({len(comps)}): {comps}")
    print(f"forms: {json.dumps(snap['forms'])[:600]}")
    print(f"actions: {snap['wire_actions'][:12]}")
    print(f"alpine nodes: {snap['alpine_nodes']}  external: {snap['external']}")
    print(f"text[:900]:\n{snap['text'][:900]}")
    return snap


def fetch(c, route):
    c.xhr_log.clear()
    c.fetch(f"{BASE}/{route}")
    time.sleep(1.5)


def login(c):
    email, password = account()
    fetch(c, "login")
    c.page.fill("input[name=email]", email)
    c.page.fill("input[name=password]", password)
    c.page.click("button:has-text('Log In')")
    time.sleep(4)
    print("logged in ->", c.page.evaluate("() => location.href"))


def recon():
    c = ExamMateClient(restore_state=False, verbose=False)
    try:
        for i, r in enumerate(ROUTES):
            fetch(c, r)
            dump(c, f"4{i}_anon", r)
        login(c)
        for i, r in enumerate(ROUTES):
            fetch(c, r)
            dump(c, f"4{i}_auth", r)
    finally:
        c.close()


def hydrated_components(c):
    return js(c, """() => {
        if (!window.Livewire) return '<no livewire>';
        try {
            return Object.values(window.Livewire.components || {}).map(x => {
                if (!x) return null;
                const fp = x.fingerprint || {};
                const memo = (x.serverMemo || {}).data || {};
                return {id: x.id || null, name: fp.name || x.name || null,
                        categoryID: memo.categoryID !== undefined ? memo.categoryID : null,
                        subjectID: memo.subjectID !== undefined ? memo.subjectID : null};
            }).filter(Boolean);
        } catch(e) { return '<err ' + e + '>'; }
    }""")


def go_state(c):
    return js(c, """() => {
        const a = Array.from(document.querySelectorAll('a')).find(e =>
            /Lets\\s*GO/i.test(e.innerText || ''));
        if (!a) return null;
        return {href: a.getAttribute('href'), cls: a.className,
                disabled: a.classList.contains('disabled'),
                target: a.getAttribute('target')};
    }""")


def subject_items(c):
    return js(c, """() => Array.from(document.querySelectorAll(
        '[wire\\\\:click*="subjectID"]'))
        .map(e => ({w: e.getAttribute('wire:click'),
                    t: (e.innerText || '').trim().slice(0, 50),
                    vis: e.offsetParent !== null}))
        .slice(0, 120)""")


def drive_ai(c, route, tag):
    """Select category+subject on an AI landing page; capture GO target."""
    fetch(c, route)
    print(f"\n===== {tag} /{route} =====")
    print("hydrated:", json.dumps(hydrated_components(c)))
    # click first category of the AI page's own list (bare-word match, no quotes)
    cat = js(c, """() => { const el = document.querySelector(
        '[wire\\\\:click*="categoryID"]');
        if (!el) return null; const w = el.getAttribute('wire:click');
        el.click(); return w; }""")
    print("clicked:", cat)
    time.sleep(3.5)
    subs = subject_items(c)
    vis = [s for s in subs if s.get("vis")]
    print(f"subjects total({len(subs)}) visible({len(vis)}):",
          json.dumps(vis[:15] or subs[:15]))
    picked = js(c, """() => {
        const els = Array.from(document.querySelectorAll(
            '[wire\\\\:click*="subjectID"]'));
        const el = els.find(e => e.offsetParent !== null) || els[0];
        if (!el) return null; const w = el.getAttribute('wire:click');
        el.click(); return w; }""")
    print("picked subject:", picked)
    time.sleep(4)
    print("GO now:", json.dumps(go_state(c)))
    print("hydrated:", json.dumps(hydrated_components(c)))
    # any gemini/external AI link now present anywhere?
    ext = js(c, """() => Array.from(document.querySelectorAll('a[href]'))
        .map(a => a.href).filter(h => /gemini|chatgpt|openai|claude|chat\\./i.test(h))""")
    print("AI links:", ext)
    dump(c, tag, route)
    return go_state(c)


def interact():
    c = ExamMateClient(restore_state=False, verbose=False)
    try:
        # anonymous first — landing pages render without login
        for tag, r in [("5a_anon", "prediction-exam"), ("5b_anon", "revision")]:
            drive_ai(c, r, tag)
    finally:
        c.close()


def sweep(features=("prediction", "revision")):
    """Walk every category x subject on the GPT-backed features; record GO hrefs."""
    c = ExamMateClient(restore_state=False, verbose=False)
    cat_path = f"{PROBE}/ai_gpt_catalog.json"
    catlog = json.load(open(cat_path)) if os.path.exists(cat_path) else {}
    routes = {"prediction": "prediction-exam", "revision": "revision"}
    try:
        for feature in features:
            fetch(c, routes[feature])
            cats = js(c, """() => Array.from(document.querySelectorAll(
                    '[wire\\\\:click*="categoryID"]'))
                .map(e => ({w: e.getAttribute('wire:click'),
                            t: (e.innerText || '').trim().slice(0, 40)}))
                .filter(x => /categoryID/.test(x.w))""")
            # de-dup by id
            seen, cats_u = set(), []
            for x in cats:
                m = re.search(r"categoryID'\s*,\s*(\d+)", x["w"])
                if m and m.group(1) not in seen:
                    seen.add(m.group(1)); cats_u.append((m.group(1), x["t"]))
            print(f"\n### {feature}: {len(cats_u)} categories: {cats_u}", flush=True)
            for cid, clabel in cats_u:
                js(c, f"""() => {{
                    const el = Array.from(document.querySelectorAll(
                        '[wire\\\\:click*="categoryID"]'))
                        .find(e => /categoryID'\\s*,\\s*{cid}\\)/.test(e.getAttribute('wire:click') || ''));
                    if (el) el.click(); }}""")
                time.sleep(2.2)
                subs = subject_items(c)
                for s in subs:
                    m = re.search(r"subjectID'\s*,\s*(\d+)", s["w"])
                    if not m:
                        continue
                    sid = m.group(1)
                    js(c, f"""() => {{
                        const el = Array.from(document.querySelectorAll(
                            '[wire\\\\:click*="subjectID"]'))
                            .find(e => (e.getAttribute('wire:click') || '').includes("subjectID', {sid}"));
                        if (el) el.click(); }}""")
                    time.sleep(2.0)
                    g = go_state(c) or {}
                    key = f"{cid}:{sid}"
                    ent = catlog.setdefault(key, {"category": clabel, "subject": s["t"]})
                    ent[feature] = {"href": g.get("href"), "disabled": g.get("disabled")}
                    href = g.get("href", "")
                    mark = "OK " if href and href != "#" else "-- "
                    print(f"{mark}{key} {clabel} / {s['t']} -> {href[:110]}", flush=True)
                    json.dump(catlog, open(cat_path, "w"), indent=1)  # checkpoint every step
        n_pred = sum(1 for v in catlog.values() if v.get("prediction", {}).get("href") not in (None, "#"))
        n_rev = sum(1 for v in catlog.values() if v.get("revision", {}).get("href") not in (None, "#"))
        print(f"\nCATALOG: {len(catlog)} subjects; prediction GPTs={n_pred}, revision GPTs={n_rev}")
    finally:
        c.close()


def gem_landing():
    """Try to view the Gemini Gem share page + one ChatGPT GPT landing anonymously."""
    c = ExamMateClient(restore_state=False, verbose=False)
    try:
        for tag, url in [
            ("gem_marker", "https://gemini.google.com/gem/1pbFQkuKQifVUtkF-YSgdvq2xp4Ow96Ye?usp=sharing"),
            ("gpt_pred", "https://chatgpt.com/g/g-693fb620e04c8191a4bee4ceefb14b8f-igcse-additional-maths-0606-exam-prediction-ai"),
            ("gpt_rev", "https://chatgpt.com/g/g-69674e7cdf1c81919c3aee81739b0552-exam-mate-igcse-additional-mathematics-revision"),
        ]:
            try:
                c.fetch(url, max_rounds=2)
                time.sleep(2)
                info = js(c, """() => ({
                    url: location.href, title: document.title,
                    desc: (document.querySelector('meta[name=description]') || {}).content || null,
                    h1: Array.from(document.querySelectorAll('h1')).map(h => h.innerText.trim()).slice(0, 3),
                    text: (document.body.innerText || '').replace(/\\n{2,}/g, '\\n').slice(0, 1200)})""")
                print(f"\n===== {tag} =====\n{json.dumps(info, indent=1)[:2000]}")
                open(f"{PROBE}/6_{tag}.html", "w").write(c.page.content())
                open(f"{PROBE}/6_{tag}.json", "w").write(json.dumps(info, indent=1))
            except Exception as e:
                print(f"\n===== {tag} FAILED: {str(e)[:150]}")
    finally:
        c.close()


if __name__ == "__main__":
    os.makedirs(PROBE, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "recon"
    if mode == "sweep":
        sweep(sys.argv[2:] or ("prediction", "revision"))
    else:
        {"recon": recon, "interact": interact, "gem": gem_landing}[mode]()
