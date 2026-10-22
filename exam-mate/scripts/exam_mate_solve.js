// exam-mate challenge solver: run the served obfuscated JS in a browser shim,
// capture the clearance URL it would submit, print it.
// Usage: node exam_mate_solve.js <challenge_html_file>
const fs = require("fs");

const htmlFile = process.argv[2];
if (!htmlFile) { console.error("need challenge html path"); process.exit(1); }
const html = fs.readFileSync(htmlFile, "utf8");

// extract the LAST <script> block (the obfuscated challenge; first one is the reload timer)
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (scripts.length < 2) { console.error("challenge script not found"); process.exit(1); }
const challengeJs = scripts[scripts.length - 1];

// ---- browser environment shim (designed to PASS all 7 checks) ----
class Plugin {}
class PluginArray {}
class MimeType {}
class MimeTypeArray {}

const plugins = Object.create(PluginArray.prototype);
for (let i = 0; i < 5; i++) {
  const pl = Object.create(Plugin.prototype);
  pl.name = "Chrome PDF Plugin " + i;
  plugins[i] = pl;
}
Object.defineProperty(plugins, "length", { value: 5, enumerable: false });

const mimeTypes = Object.create(MimeTypeArray.prototype);
for (let i = 0; i < 4; i++) {
  const mt = Object.create(MimeType.prototype);
  mt.type = "application/pdf" + i;
  mimeTypes[i] = mt;
}
Object.defineProperty(mimeTypes, "length", { value: 4, enumerable: false });

const navigatorObj = {
  webdriver: false,
  userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
  appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
  language: "en-US",
  languages: ["en-US", "en", "ms"],
  plugins: plugins,
  mimeTypes: mimeTypes,
  hardwareConcurrency: 8,
};

let capturedSubmit = null;   // {action, method, fields: [{name, value}]}
let capturedXhr = null;      // {url, method}

function makeElement(tag) {
  const el = {
    _tag: tag,
    children: [],
    style: {},
    appendChild(c) { this.children.push(c); },
    setAttribute(k, v) { this[k] = v; },
    submit() {
      capturedSubmit = {
        action: this.action,
        method: this.method,
        fields: this.children.map(c => ({ name: c.name, value: c.value, id: c.id })),
      };
    },
  };
  return el;
}

const documentObj = {
  getElementById() { return makeElement("div"); },
  createElement(tag) { return makeElement(String(tag)); },
  readyState: "complete",
};
documentObj.addEventListener = (type, fn) => {
  (listeners[type] = listeners[type] || []).push(fn);
};
documentObj.attachEvent = (type, fn) => {
  (listeners[type] = listeners[type] || []).push(fn);
};

const listeners = {};
const windowObj = {
  navigator: navigatorObj,
  document: documentObj,
  outerWidth: 1440,
  outerHeight: 900,
  location: { href: "https://www.exam-mate.com/", reload() {} },
  addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
  attachEvent(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
};

class ShimXHR {
  open(method, url) { this._method = method; this._url = url; }
  send(body) { capturedXhr = { method: this._method, url: this._url, body }; }
}

// build the sandbox
const vm = require("vm");
const sandbox = {
  window: windowObj,
  document: documentObj,
  navigator: navigatorObj,
  Plugin, PluginArray, MimeType, MimeTypeArray,
  XMLHttpRequest: ShimXHR,
  URLSearchParams,
  Object, Array, setTimeout,
  console,
};
sandbox.globalThis = sandbox;
// 'webdriver' must NOT be a key on window (check: 'webdriver' in window)
vm.createContext(sandbox);

try {
  vm.runInContext(challengeJs, sandbox, { timeout: 5000 });
} catch (e) {
  console.error("EVAL ERROR:", e.message);
}

// fire DOMContentLoaded handlers (the script defers the build by 1s via setTimeout)
(listeners["DOMContentLoaded"] || []).forEach(fn => { try { fn(); } catch (e) {} });

setTimeout(() => {
  const out = { capturedSubmit, capturedXhr };
  if (capturedSubmit) {
    const sp = new URLSearchParams();
    for (const f of capturedSubmit.fields) sp.append(f.name, f.value);
    const base = "https://www.exam-mate.com" + capturedSubmit.action;
    out.validationUrl = base + "?" + sp.toString();
  }
  console.log(JSON.stringify(out, null, 2));
}, 1600);
