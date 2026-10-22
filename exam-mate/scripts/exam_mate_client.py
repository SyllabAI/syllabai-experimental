"""exam-mate client: Playwright-based fetcher with automatic WAF challenge solving.

The exam-mate WAF ("One moment, please..." splash) runs 7 fingerprint checks.
A Chromium with:
  - --disable-blink-features=AutomationControlled  (real webdriver=false)
  - UA without "Headless"
  - window.outerWidth/outerHeight patched (headless reports 0)
passes all checks, so the challenge page SELF-SOLVES: its own JS builds the
clearance form and navigates -> 302 -> real content, in ~2-6 seconds.

Usage:
  from exam_mate_client import ExamMateClient
  c = ExamMateClient()
  html = c.fetch("https://www.exam-mate.com/topicalpastpapers")
  c.close()
"""
import json, os, re, time
from playwright.sync_api import sync_playwright

PROBE = "/home/z/my-project/exam-mate-probe"
STATE = f"{PROBE}/client_state.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


class ExamMateClient:
    def __init__(self, state_path=STATE, headless=True, verbose=True, restore_state=True):
        self.verbose = verbose
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled",
                  "--no-sandbox", "--disable-dev-shm-usage"],
        )
        self.ctx = self.browser.new_context(
            user_agent=UA, viewport={"width": 1440, "height": 900},
            locale="en-US", timezone_id="Asia/Kuala_Lumpur",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9,ms;q=0.8"},
        )
        self.ctx.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(window, 'outerWidth', {get: () => 1440});
            Object.defineProperty(window, 'outerHeight', {get: () => 900});
        """)
        if restore_state and os.path.exists(state_path):
            try:
                # restore cookies into context
                state = json.load(open(state_path))
                if state.get("cookies"):
                    self.ctx.add_cookies(state["cookies"])
                    self.log(f"restored {len(state['cookies'])} cookies from state")
            except Exception as e:
                self.log(f"state restore failed: {e}")
        self.page = self.ctx.new_page()
        self.xhr_log = []
        self.csrf_token = None
        self.page.on("response", self._log_xhr)

    def log(self, msg):
        if self.verbose:
            print(f"[exam-mate] {msg}", flush=True)

    def _log_xhr(self, resp):
        rt = resp.request.resource_type
        if rt in ("xhr", "fetch"):
            self.xhr_log.append({
                "url": resp.url, "status": resp.status,
                "method": resp.request.method,
                "post_data": resp.request.post_data,
            })

    def _csrf_from_page(self):
        """Livewire v2 csrf token from the boot config."""
        try:
            val = self.page.evaluate(
                "() => (window.livewireScriptConfig && window.livewireScriptConfig.csrf) "
                "|| (window.Livewire && window.Livewire.csrfTokenFor) "
                "|| null")
            if val:
                return val
        except Exception:
            pass
        return None

    def is_challenge(self):
        try:
            return "moment" in (self.page.title() or "").lower()
        except Exception:
            return True

    def fetch(self, url, max_rounds=4, settle_ms=1200, referer=None):
        """Navigate to url, auto-solving WAF splashes; return final HTML."""
        for round_i in range(max_rounds):
            self.log(f"GET {url} (round {round_i+1})")
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=45000,
                               referer=referer)
            except Exception as e:
                self.log(f"  goto error: {e}")
                time.sleep(2)
                continue
            # challenge loop: wait for self-solve (page reloads itself)
            waited = 0
            while self.is_challenge() and waited < 25:
                time.sleep(2)
                waited += 2
            if self.is_challenge():
                self.log("  still challenged after wait, retrying round")
                continue
            time.sleep(settle_ms / 1000)
            html = self.page.content()
            self.csrf_token = self.csrf_token or self._csrf_from_page()
            self._save_state()
            return html
        raise RuntimeError(f"challenge unsolved after {max_rounds} rounds: {url}")

    def download(self, url, out_path, max_rounds=3):
        """Fetch binary content through the browser page context (fetch ->
        arrayBuffer -> base64). Immune to the requests-TLS fingerprinting."""
        for attempt in range(max_rounds):
            res = self.page.evaluate("""async (url) => {
                try {
                    const r = await fetch(url, {credentials: 'include'});
                    const ct = r.headers.get('content-type') || '';
                    if (!r.ok) return {status: r.status, ct};
                    const buf = await r.arrayBuffer();
                    let binary = '';
                    const bytes = new Uint8Array(buf);
                    const chunk = 0x8000;
                    for (let i = 0; i < bytes.length; i += chunk) {
                        binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
                    }
                    return {status: r.status, ct, b64: btoa(binary), size: bytes.length};
                } catch (e) {
                    return {error: String(e)};
                }
            }""", url)
            if res.get("error"):
                self.log(f"download fetch error: {res['error'][:80]}")
                time.sleep(1)
                continue
            ct = res.get("ct", "")
            if "text/html" in ct:
                # challenged or error page — heal clearance via any page load
                self.fetch("https://www.exam-mate.com/", settle_ms=400)
                continue
            import base64
            data = base64.b64decode(res["b64"])
            open(out_path, "wb").write(data)
            return res["status"], len(data), ct
        return 0, 0, "failed"

    def livewire_post(self, component_name, body, referer_url=None):
        """POST a Livewire message through the browser network stack
        (context.request inherits cookies + browser TLS fingerprint)."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/html, application/xhtml+xml",
            "X-Requested-With": "XMLHttpRequest",
            "X-Livewire": "true",
        }
        if self.csrf_token:
            headers["X-CSRF-TOKEN"] = self.csrf_token
        url = f"https://www.exam-mate.com/livewire/message/{component_name}"
        resp = self.ctx.request.post(url, data=json.dumps(body), headers=headers,
                                     fail_on_status_code=False,
                                     max_redirects=0)
        return resp

    def capture_csrf(self, html):
        """Livewire's csrf lives in window.livewireScriptConfig / inline boot."""
        m = re.search(r'csrf["\']?\s*[:=]\s*["\']([A-Za-z0-9_-]{20,})["\']', html)
        if m:
            self.csrf_token = m.group(1)
        return self.csrf_token

    def cookies_for_curl(self, jar_path=None):
        """Export cookies in Netscape jar format for curl reuse."""
        jar_path = jar_path or f"{PROBE}/client_jar.txt"
        lines = ["# Netscape HTTP Cookie File"]
        for c in self.ctx.cookies():
            lines.append(f"{c['domain']}\tTRUE\t{c['path']}\t"
                         f"{'TRUE' if c.get('secure') else 'FALSE'}\t"
                         f"{int(c.get('expires', 0))}\t{c['name']}\t{c['value']}")
        open(jar_path, "w").write("\n".join(lines) + "\n")
        self.log(f"cookie jar exported: {jar_path}")
        return jar_path

    def _save_state(self):
        try:
            json.dump({"cookies": self.ctx.cookies()}, open(STATE, "w"))
        except Exception:
            pass

    def close(self):
        try:
            self._save_state()
        except Exception:
            pass
        self.browser.close()
        self.pw.stop()


if __name__ == "__main__":
    import sys
    c = ExamMateClient()
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.exam-mate.com/topicalpastpapers"
    html = c.fetch(url)
    out = sys.argv[2] if len(sys.argv) > 2 else f"{PROBE}/client_fetch.html"
    open(out, "w").write(html)
    print(f"saved {len(html)}b to {out}")
    if c.xhr_log:
        print("--- XHRs seen ---")
        for x in c.xhr_log[-15:]:
            print(f"  [{x['status']}] {x['method']} {x['url'][:140]}"
                  + (f"  data={str(x['post_data'])[:100]}" if x["post_data"] else ""))
    c.close()
