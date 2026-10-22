# IP and copyright notes — senecalearning experiment

**Standing rule**: this note governs what may be committed to this public
repo from the Seneca Learning experiment. It mirrors the
`undergroundmathematics/docs/IP-AND-COPYRIGHT-NOTES.md` posture and is
stricter where Seneca is stricter.

## Why stricter

Undergroundmathematics is an open educational resource site with explicit
permissive intent; Seneca is a **commercial, login-walled platform** whose
course content is its product. Acquired by GoStudent (2022), it monetises
via Premium subscriptions, school contracts and white-label deals
(GoStudent, Studienkreis, Plurall). Anything that reproduces, bypasses or
undermines that wall is off-limits — both as law (copyright + CFAA-type
misuse + their ToS) and as SyllabAI research ethics.

## What we capture and commit

- **Infrastructure metadata**: host names, service names, endpoint paths,
  auth *mechanism* descriptions (pool IDs, flow names) — these are
  configuration facts observable by any client of the public app, useful
  for architecture study, and not security-sensitive secrets.
- **Public marketing/legals**: company facts, public pricing pages, public
  help-centre article titles/URLs, public App Store metadata.
- **Structural observations**: route names, chunk names, feature-module
  names, service → feature mapping.
- **Our own analysis**: all documents in `research/`.

## What we capture but do NOT commit

- **Minified JS bundles** (`resources/captures/js/`, 290 chunks, ~4.6 MB):
  re-fetchable public static assets; kept locally for analysis only,
  excluded from git by `resources/captures/js/.gitignore`. The chunk
  manifest + extraction results are committed instead, and
  `resources/scripts/fetch-app-bundles.sh` reproduces the corpus.
- **Screenshots/captures of authenticated course content** — none taken in
  Phase 1; none will be committed in any phase.

## What we never do

- Never scrape, store or redistribute **course content bodies** (lesson
  text, questions, images, GIFs, audio, PDFs). Content metadata (ids,
  titles, section counts, structure) is the maximum, and only from our own
  legitimate account.
- Never attempt **auth bypass, token forgery, rate-limit stress, or
  access to other users' data**. Our probes use only endpoints the app
  itself calls, with the app's own client identity.
- Never create more accounts than the experiment needs (one student, at
  most one teacher), never enrol in real schools/classes, never interact
  with real students' data.
- Never publish credentials, JWTs or session tokens to this repo.

## Account-credentialed work (Phase 2+)

Requires an operator decision recorded in the plan doc. Any authenticated
captures stay metadata-only (JSON shapes with values truncated/redacted),
and the account is throwaway (randomised identity, no real school).
Service terms are respected: no automated querying beyond what interactive
use produces, no commercial-use reproduction of anything observed.

## Takedown / correction

If Seneca Learning Ltd or GoStudent objects to any committed artifact
(their config files, bundle analyses), we remove it on request — the
experiment is internal research, and nothing here is load-bearing for
SyllabAI of-record systems.

## Session 3 addendum (2026-10-22) — the title rule

Phase 2 session 3 (Resource Hub catalogue) exposed a nuance the original
rule set didn't anticipate: for `examQuestion` resources the `title`
field is the plain-text **question stem** — the content itself, not a
structural name. Standing rule refined accordingly:

- **Structural titles** (course names, section names, quiz names) remain
  committable metadata — they are the catalogue/ToC layer.
- **Exam-question titles (= stems)** are treated as content: nulled in
  committed metadata files (`"title": null`), full text kept only in the
  local-only payload store, same posture as mark schemes and generation
  scripts.
- Metadata retained per question: id, type, tag values, topic
  breadcrumbs, marks, answer counts, publisher, questionType — enough
  for structure/coverage analysis, none of it teaches or assesses.
