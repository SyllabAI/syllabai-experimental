// This should never be set to a version that is greater than the
// currently deployed version of the app.
// It is used to force updates for returning users after the Summer.
const AUTO_UPDATE_VERSION = "4.6.0";

const MIN_VERSION_PARAM_KEY = "min-version";

(function () {
  const version = window.Seneca && window.Seneca.version;
  const urlParams = new URLSearchParams(window.location.search);
  const forceLatest = urlParams.get(MIN_VERSION_PARAM_KEY) === "latest";

  if (!version || isLessThan(version, AUTO_UPDATE_VERSION) || forceLatest) {
    console.log("Forcing app update...");

    if (canForceUpgrade()) {
      forceUpgrade().then(() => {
        if (forceLatest) {
          window.location.replace(removeMinVersionFromUrl());
        } else {
          // Hard reload to get fresh content
          window.location.reload(true);
        }
      });
    }
  }
})();

function canForceUpgrade() {
  return "serviceWorker" in navigator && "caches" in window;
}

function forceUpgrade() {
  return caches
    .keys()
    .then(names => Promise.all(names.map(name => caches.delete(name))))
    .then(() => navigator.serviceWorker.getRegistrations())
    .then(registrations =>
      Promise.all(registrations.map(reg => reg.unregister()))
    );
}

function removeMinVersionFromUrl() {
  const urlParams = new URLSearchParams(window.location.search);
  urlParams.delete(MIN_VERSION_PARAM_KEY);
  const newSearch = urlParams.toString();
  return (
    window.location.pathname +
    (newSearch ? "?" + newSearch : "") +
    window.location.hash
  );
}

function findMatch(myVersion, rules) {
  return rules.some(rule => {
    if (myVersion === rule) return true;
    if (rule.startsWith("<")) {
      const version = rule.replace("<", "");
      return compare(myVersion, version) < 0;
    }
    return false;
  });
}

function compare(a, b) {
  const pa = a.split(".");
  const pb = b.split(".");
  for (var i = 0; i < 3; i++) {
    var na = Number(pa[i]);
    var nb = Number(pb[i]);
    if (na > nb) return 1;
    if (nb > na) return -1;
    if (!isNaN(na) && isNaN(nb)) return 1;
    if (isNaN(na) && !isNaN(nb)) return -1;
  }
}

function isLessThan(myVersion, version) {
  return compare(myVersion, version) < 0;
}

const versions = {
  findMatch,
  canForceUpgrade,
  forceUpgrade
};

if (!window.Seneca) window.Seneca = {};
window.Seneca.versions = versions;
