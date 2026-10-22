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

## Session 4 addendum (2026-10-22) — session/quiz captures under operator authorisation

Phase 2 session 4 walked a Magic Quiz generation and a real Adaptive study
session under the operator-provided teacher account, per the operator's
explicit direction to exercise the product's AI + session flows. Posture:

- **Machine-generated output, not Seneca-authored content.** The Magic Quiz
  artefact was generated from *our own probe paragraph* by Seneca's LLM
  pipeline. Committed shape files truncate the generated bodies anyway
  (title rule spirit): structural fields verbatim, `correctAnswer`,
  `wrongAnswers`, and wordfill token streams redacted, markdown bodies cut
  at ~120 chars.
- **Lesson/question content in the session emit** (concept-card examples,
  question text) is Seneca-authored course content: truncated at ~120
  chars in committed captures, structure and scoring fields verbatim,
  full payloads local-only (`/tmp` lineage, not committed).
- **JWT hygiene**: the session-ws URL carries the Firebase token in its
  query string; committed frame captures are scrubbed of tokens and
  userIds. Tokens never leave RAM / `/tmp`.
- **Account side-effects recorded**: one quiz draft (unpublished; free
  tier forbids private quizzes — documented), one completed study session
  + memory deposit on the teacher's own preview study, XP 214/level 2.
  Zero assignments, zero class changes. The quiz draft cannot be deleted
  (no delete endpoint); accepted as residual state of the throwaway
  teacher account.
- No automated bulk querying occurred this session; every request was a
  page-action-driven interactive call.

## Session 5 addendum (2026-10-22) — lazy-chunk extension for learner-model math

Session 5 was static analysis only (no authenticated API traffic, no content
fetches). The Phase-1 bundle-corpus policy was extended as follows:

- The local JS corpus grew 292 → ~360 chunks by fetching **public static app
  assets** (`app.senecalearning.com/assets/<name>`) discovered from the
  router's lazy-import dependency array. Same posture as Phase 1: descriptive
  UA, bounded candidate set (not the full 1,445-asset graph), chunks kept out
  of git (`.gitignore`); the reproducible recipe is committed in
  `research/2026-10-22-memory-math.md` §6.
- What was committed: **mathematical formulas, constants, and behavioral
  facts** decoded from the code (fade equation, scheduler increments, endpoint
  list, enum values). Formulas and constants are facts, not copyrightable
  expression; no Seneca code is reproduced in the repository beyond short
  verbatim snippets already necessary to document protocol shapes, consistent
  with the existing notes.
- Source maps were probed once (`.js.map` → SPA HTML shell) and abandoned —
  no de-obfuscation beyond ordinary bundle reading was performed or needed.

## Session 6 addendum (2026-10-22, posterior-formula chase)

- Three additional controlled-scoring study sessions were walked on the same
  section (same authorization scope as session 4; ≤1 req/s API pacing; all
  evidence stays client-side captures). Two emit bodies committed as
  `resources/captures/sessions/session-emit-{A,C}-*.json` with `userId`
  redacted; question stems/answers are short course metadata consistent with
  the existing session-4 exemplar treatment (the "title rule" extension for
  bulk resource-hub exports is not implicated — these are single exemplars,
  bodies truncated where long).
- The JS corpus grew to 948 chunks (player + end-session closure set) and was
  **fully decompressed in place** — 602 files had been saved gzip-encoded by
  curl and were invisible to prior greps (tooling lesson recorded in the
  research note). Chunks remain local-only per `.gitignore`; nothing from the
  bundles enters git except short verbatim snippets required to document the
  decoded formula (constants `h=3, g=0.9, 50/50` weights — facts, not
  protectable expression).
- The runtime store tap (React fiber walk → redux `subscribe`) is documented
  as a reproduction recipe; no anti-bot circumvention was involved (standard
  web APIs on the operator's own logged-in session).

### Session 7 addendum (2026-10-22)

The title rule was applied to the **full 74-subject harvest**:
`by-subject/*.jsonl.gz` (206,982 rows) — automated scan shows
`examQuestion` title violations: **0**. All raw pages with content
bodies remain local-only (`probe-results/rh3/local-only-full-payloads/`,
~1,100 files, gitignored path).
