# IP and copyright notes — znotes experiment

**Standing rule**: this note governs what may be committed to this public
repo from the ZNotes experiment. It mirrors the `senecalearning` posture.

## Why this posture

ZNotes is a freemium platform (ZNotes Education Limited) whose revision
notes, videos, quizzes and generated teacher resources are its product;
revenue rides on ZNotes Boost subscriptions and school packages. The
educator AI toolkit generates resources **grounded in ZNotes' own notes
corpus** — so generated outputs may embed substantial platform content.
Anything that reproduces, bypasses or undermines that wall is off-limits,
both as law (copyright + their Terms) and as SyllabAI research ethics.

## What we capture and commit

- **Infrastructure metadata**: API host and endpoint paths, chunk/file
  names, auth *mechanism* descriptions, quota constants — configuration
  facts observable by any client of the public app; not secrets, not
  security-sensitive (no internal endpoints, no admin surface probed).
- **Public marketing/legals**: company facts, public pricing (Boost),
  public educators page claims, sitemap/robots.
- **Structural observations**: route map, panel names, form field names
  and option preset lists (these are UI vocabulary, not content), the
  generator request/response protocol shapes.
- **Our own analysis**: all documents in `research/`.

## What we capture but do NOT commit

- **Minified JS bundles/chunks** (`resources/captures/chunks/`, 99 files,
  ~5.8 MB): re-fetchable public static assets; kept locally for analysis
  only, excluded from git. `resources/scripts/fetch-app-bundles.sh`
  reproduces the corpus; the chunk manifest is committed instead.
- **Notes/chapter/card content bodies** — never scraped, never committed.
  Chapter *titles* appear in this repo only as UI-mechanism evidence where
  unavoidable (e.g. a single example), and never as a corpus.
- **Screenshots of authenticated content** — none taken; none committed.
- **Generated AI resource bodies** (Phase 2): if a generation is executed
  for protocol verification, only field names / sizes / status codes are
  recorded; output text stays out of the repo.

## What we never do

- Never scrape, store or redistribute **notes bodies, quiz banks, videos,
  PDFs or generated resource bodies**.
- Never attempt auth bypass, token forgery, rate-limit stress, or access
  to other users' data. Probes use only endpoints the public app itself
  calls, with the app's own client identity.
- Never use the teacher account beyond interactive-equivalent exploration;
  never touch school/class/student data associated with it.
- **Never publish credentials, tokens or session identifiers to this
  repo.** (The experiment's login credentials live only in the operator's
  head/imChannel — not in any file here.)

## Account-credentialed work (Phase 2)

Requires the operator decision recorded in the plan doc. Authenticated
captures stay metadata-only (JSON shapes with values truncated/redacted).
Service terms are respected: no automated querying beyond what interactive
use produces, no commercial-use reproduction of anything observed.

## Takedown / correction

If ZNotes Education Limited objects to any committed artifact, we remove
it on request — the experiment is internal research; nothing here is
load-bearing for SyllabAI of-record systems.
