#!/usr/bin/env python3
"""exam-mate login — operator-provided credentials, session state kept OUTSIDE the repo.

1. Probes the site for the login route/form.
2. Fills credentials, submits.
3. Verifies logged-in state and saves Playwright storage state to
   /home/z/my-project/exam-mate-probe/auth_state.json (git-ignored area).
"""
import json, os, sys, time

sys.path.insert(0, "/home/z/my-project/syllabai-experimental/exam-mate/scripts")
from exam_mate_client import ExamMateClient  # noqa: E402

PROBE = "/home/z/my-project/exam-mate-probe"
STATE_OUT = f"{PROBE}/auth_state.json"
# operator credentials (private, never committed)
CREDS = json.load(open(f"{PROBE}/creds.json"))

BASE = "https://www.exam-mate.com"


def dump_links(c):
    links = c.page.evaluate("""() => {
        const out = [];
        for (const a of document.querySelectorAll('a[href]')) {
            const t = (a.textContent || '').trim().toLowerCase();
            const h = a.getAttribute('href');
            if (/log\\s?in|sign\\s?in|register|subscription|account/.test(t))
                out.push({text: t.slice(0, 40), href: h});
        }
        return out;
    }""")
    seen = set()
    for l in links:
        k = (l["text"], l["href"])
        if k not in seen:
            seen.add(k)
            print("  link:", l)
    return links


def main():
    c = ExamMateClient(verbose=True)
    try:
        c.fetch(BASE + "/topicalpastpapers", settle_ms=1000)
        print("== nav links mentioning login/account:")
        links = dump_links(c)

        # choose login route
        login_href = None
        for l in links:
            if "log" in l["text"] or "sign" in l["text"]:
                login_href = l["href"]
                break
        if not login_href:
            login_href = "/login"
        url = login_href if login_href.startswith("http") else BASE + login_href
        print(f"== navigating to {url}")
        c.fetch(url, settle_ms=1200)

        inputs = c.page.evaluate("""() =>
            [...document.querySelectorAll('input,button[type=submit],button')].map(i => ({
                tag: i.tagName, type: i.type || '', name: i.name || '',
                id: i.id || '', ph: i.placeholder || '',
                text: (i.textContent || '').trim().slice(0, 30),
                form: i.form ? (i.form.id || i.form.action) : null}))
            .filter(i => !['hidden'].includes(i.type))""")
        print("== form controls on page:")
        for i in inputs:
            print("  ", i)

        # locate email/password fields and submit
        email_sel = None
        pw_sel = None
        for i in inputs:
            if i["tag"] == "INPUT" and i["type"] in ("email", "text"):
                if "mail" in (i["name"] + i["id"] + i["ph"]).lower() and not email_sel:
                    email_sel = f'input[name="{i["name"]}"]' if i["name"] else f'#{i["id"]}'
            if i["tag"] == "INPUT" and i["type"] == "password":
                pw_sel = f'input[name="{i["name"]}"]' if i["name"] else f'#{i["id"]}'
        print(f"== selectors: email={email_sel} pw={pw_sel}")
        if not (email_sel and pw_sel):
            print("!! could not locate login fields — dumping page title/url")
            print(c.page.title(), c.page.url)
            open(f"{PROBE}/login_page.html", "w").write(c.page.content())
            return 1

        c.page.fill(email_sel, CREDS["email"])
        c.page.fill(pw_sel, CREDS["password"])
        # submit: prefer explicit submit button, else Enter
        sub = c.page.query_selector('button[type="submit"], input[type="submit"]')
        if sub:
            sub.click()
        else:
            c.page.press(pw_sel, "Enter")
        time.sleep(4)
        # wait for navigation away from login
        for _ in range(10):
            if "/login" not in c.page.url:
                break
            time.sleep(1)
        print("== after submit:", c.page.url, "| title:", c.page.title())
        html = c.page.content()
        open(f"{PROBE}/after_login.html", "w").write(html)
        low = html.lower()
        still_login = ("logout" not in low and ("log in" in low or "sign in" in low))
        print("== logout marker present:", "logout" in low)
        dump_links(c)
        ok = ("logout" in low) or ("/login" not in c.page.url and not still_login)
        print("== LOGIN VERDICT:", "SUCCESS" if ok else "UNCERTAIN/FAILED")
        if ok or "logout" in low:
            ctx = c.ctx
            import playwright.sync_api  # noqa
            state = {
                "cookies": ctx.cookies(),
                "origins": [],
            }
            json.dump(state, open(STATE_OUT, "w"))
            print("== state saved:", STATE_OUT, f"({len(state['cookies'])} cookies)")
            for ck in state["cookies"]:
                print(f"   cookie {ck['name']} domain={ck['domain']} expires_in={int(ck.get('expires',0))>0}")
            return 0
        return 1
    finally:
        c.close()


if __name__ == "__main__":
    sys.exit(main())
