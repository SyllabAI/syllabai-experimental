# TICKET-P5-UGM-PILOT — "Explore further" Mode-2 deep-link pilot, IAL P1 Quadratics lane

| | |
|---|---|
| **Ticket** | TICKET-P5-UGM-PILOT |
| **Status** | **READY** — implementation gate open per ADR-UGM-0001 (operator-ratified 2026-10-22) |
| **Repo of record** | `SyllabAI/syllabai-v2` → `apps/hub/` (this ticket + pilot kit versioned in `SyllabAI/syllabai-experimental/undergroundmathematics/pilot/`) |
| **Basis** | `docs/ADR-UGM-0001-ugm-integration-mode.md` §Decision item 3 (Accepted) · `docs/cross-map-quadratics.md` §6 shortlists · `syllabai-v2/docs/adr/ADR-CLASS-0001` toggle practice · pilot kit: `pilot/pilot-links-quadratics.json`, `pilot/link-health-check.sh`, `pilot/wayback-bootstrap.sh` |
| **Estimate** | ≈3 dev-days (bootstrap 0.5 · module 1 · health job 0.5 · instrumentation 0.5 · readout 0.25 · review 0.25) |
| **Owners** | Hub track (implementation) + UGM track (curation, review, health-job support) |
| **Kill switch** | One flag flip; see §5 — no data migration, no rollback hazard |

## 1. Summary

Render a feature-flagged **"Explore further"** module on the **IAL P1 Quadratics** lane page only, offering learners 5 curated deep links into Underground Mathematics (UGM) review questions matched to that lane's five spec points (alignment confidence 56/59 = 95%, `docs/cross-map-quadratics.md`). Links are `rel="nofollow"`, carry UGM/Cambridge attribution and a staleness note, and are guarded by a weekly link-health job with per-link Wayback fallback. Click-through is instrumented against the ADR's floors: **≥1.0% of lane-page uniques in a 28-day window (after a 2-week grace) = continue; ≥3.0% = strong-generalise signal; below floor = the module is killed by the flag and ADR-UGM-0001 is amended.** This is the evidence producer for any future Mode-3 licensing conversation; it imports no UGM content of record.

## 2. Scope and non-goals

**In scope.** One hub lane page (IAL P1 Quadratics), one content module, one flag, one scheduled job, one analytics event, one readout query. The pilot kit in this directory is the contract for all four.

**Out of scope (each is separately gated).** Any other lane (generalisation = floor met + lane cross-map completed + operator ack, per ADR). Any UGM body text, images, or teacher-support content in the hub — the module renders **titles, slugs, type labels and hub-authored one-line hooks only**; question text is never shipped or iframed. Mode-4 doctrine changes (SmartChat hint layer, Test Builder archetypes, second tagging axis, Workbench prompt tables) land via their owning specs' PRs. Mode-3 outreach — the S1 census this ticket enables feeds it, but no conversation starts before pilot CTR evidence exists (ADR §Decision item 4).

## 3. Evidence recap and baseline (measured 2026-10-22)

- **Alignment**: 56/59 UGM quadratics resources aligned to 9709 P1 spec points 1.1.1–1.1.5 (95%), 3 explicit non-overlaps kept out of the pool; curated shortlists per spec point in `cross-map-quadratics.md` §6, machine-readable pool in `pilot/pilot-links-quadratics.json` (24 links, 5 marked `primary`).
- **Live-site health at baseline**: **24/24 links return HTTP 200** (HEAD, UA `SyllabAI-pilot-healthcheck/1.0`, 0.6 s spacing). The site is dormant but currently fully up.
- **Wayback coverage at baseline**: **0/24 resource pages archived** (availability API and CDX both checked; the station page has one 2026-01-06 snapshot). This is the pilot's principal engineering risk and the reason for launch gate **G1** (§8): *no link renders until its fallback snapshot exists* — the ADR's fallback law must not be a promise pointing at URLs that don't exist.

## 4. Pilot link set (the content contract)

The 5 **primary** links (one per spec point; swap only within the pool, keeping one per spec point):

| Spec point | Resource | Why it leads its group |
|---|---|---|
| 1.1.1 | Name that graph | graph↔equation matching across representations; lowest threshold of the pool |
| 1.1.2 | Discriminating | flagship discriminant task; MUST/MAY/CAN'T proof classification is the Mode-4 archetype exemplar |
| 1.1.3 | Quadratic solving sorter | method-selection card sort = decision-required archetype |
| 1.1.4 | When is this line a tangent to this parabola? (r7328) | tangency/simultaneous-equations in classic P1 exam style |
| 1.1.5 | How do we solve $x+3\sqrt{x}-\tfrac12=0$? (r6215) | disguised-quadratic substitution — the 1.1.5 theme, approachable entry |

The remaining 19 links are the rotation/extension pool (Appendix A / the JSON). **One-line hooks shown under each title must be hub-authored** (≤15 words, describe the mathematical activity) — never copied from UGM page descriptions. Type badges (review question / investigation / fluency) come from the JSON's UGM type metadata, which is a fact.

## 5. Feature flag (per ADR-CLASS-0001 practice, adapted to a content module)

Recommendation: a **registry JSON, not a schema change** — `apps/hub/content/pilot-flags.json` (lane rendering reads it at render time; nothing client-side):

```json
{
  "ugmExploreFurther": {
    "enabled": true,
    "linkSetRev": 1,
    "lanes": { "ial-p1-quadratics": { "enabled": true, "primaryOnly": true } }
  }
}
```

Laws, mirroring ADR-CLASS-0001's conservatism: **absent key = OFF** (unknown lane ⇒ module never renders); the flag is checked **at render time** so a kill propagates on next render without client-cache concerns; `linkSetRev` must equal the JSON's rev so a kit update and a flag flip cannot half-apply. If the hub team prefers the `class_features` side-table pattern for governance reasons, that is acceptable — the laws (default-off, render-time check, one-flip kill) are the contract, not the storage. **Kill runbook**: set `enabled:false`, redeploy/config-reload, verify module absent, then ADR amendment with the measured CTR (ADR §Decision item 3: killed by the flag, not argued).

## 6. Module rendering spec

- **Placement**: lane page, below the lane's practice content, above the footer — visually a quiet sidebar-grade section, not a hero.
- **Header**: "Explore further" + one hub-authored line: *"Curated challenges from Underground Mathematics (University of Cambridge), matched to this lane. Site content frozen around 2016–17."* — the attribution + staleness note are mandatory on every render (ADR Consequences §Neutral).
- **Cards**: title (links out), type badge, one-line hook. All anchors: `rel="nofollow"` + `target="_blank"` + `referrer-policy="no-referrer"` when falling back to Wayback (don't leak hub URLs to the archive) — `target="_blank"` alone for live links is fine.
- **Clicks**: every UGM anchor click fires the §9 event; use the hub's link-click handler (client) or an intermediate redirect route (server) — hub's choice per its analytics conventions; the event contract is what matters.
- **Non-goals in render**: no UGM thumbnails, no LaTeX, no solution previews, no iframes. Titles only.

## 7. Weekly link-health job

Reference implementation: `pilot/link-health-check.sh` (the contract; the hub may re-implement natively in its job runner, obeying the same state machine). Weekly cron, e.g. Mon 06:00 UTC.

State machine per link (state persisted in `.pilot-health-state.json` next to the link set): HEAD request, 10 s timeout, identifying UA, 0.5 s spacing → on HTTP 2xx: reset fail count. On failure: increment **consecutive** count. At **3 consecutive failures**: if `waybackSnapshotUrl` is stored → emit `SWAP <slug> <snapshotUrl>` (module serves the snapshot; live URL retried weekly and swapped back on recovery) and alert the owner; if **no** snapshot → emit `HIDE <slug>` (card suppressed, flag stays on) and alert. **Fail-closed is the law**: a link is never left pointing at a dead origin, and never pointed at a snapshot that was never verified to exist. The job writes a dated report (`pilot-health/<date>.txt`: per-link status, actions, deltas) and exits non-zero when any action fired, so the hub's job runner routes the alert. Origin-dark across the whole set = **ADR early-revisit trigger 1** — the job report must say so explicitly so the operator decision (pivot to Wayback permanently / accelerate Mode-3 ask) is forced, not discovered.

## 8. Launch gate G1 — Wayback bootstrap (blocking)

Status: **NOT DONE** — 0/24 snapshots exist (verified via availability API + CDX on 2026-10-22; anonymous Save-Page-Now was unresponsive from the research environment, so this needs a proper run from a normal network).

Procedure (`pilot/wayback-bootstrap.sh`): for each link without a stored snapshot → `GET https://web.archive.org/save/<url>` (15 s spacing, generous timeouts — SPN is slow), then CDX-verify (`statuscode:200`), write snapshot URL + timestamp into `pilot-links-quadratics.json`, commit. **Recommended**: run authenticated (free archive.org account) for reliability; 24 pages ≈ one quiet coffee. Until G1 completes for a link, that link renders **suppressed** (fail-closed from day 0, not retrofitted). Re-run after any UGM-site incident (pages re-archived while still reachable).

## 9. CTR instrumentation and the ADR floors

- **Events** (schema-agnostic; land in the hub's existing analytics store — if none exists, a single append-only table suffices):
  - `lane_page_view { laneSlug, viewerRef, ts }` — fire on the lane page render (or reuse the hub's existing pageview if it carries laneSlug + a stable viewerRef).
  - `ugm_explore_click { laneSlug, specPoint, ugmSlug, target: "live"|"wayback", viewerRef, ts }`.
  - `viewerRef` = pseudonymous (hashed session or learner id) — enough for uniques, never a raw identifier; this is aggregate CTR measurement, not profiling.
- **Definitions** (fixed by ADR §Decision item 3 — do not redefine at readout time): *lane-page uniques* = distinct `viewerRef` with ≥1 `lane_page_view` in the window; *CTR* = uniques with ≥1 `ugm_explore_click` ÷ lane-page uniques; **window** = rolling 28 days; **grace** = the first 14 days after enable are excluded from verdicts.
- **Verdict mechanics**: ≥1.0% ⇒ pilot continues; ≥3.0% ⇒ record a strong-generalise signal (still needs lane cross-map + operator ack per lane); <1.0% after any full 28-day post-grace window ⇒ kill by flag, amend ADR-UGM-0001 with the measured number. The first readout is due ~6 weeks after enable (2-week grace + 28-day window) and lands as a dated row in the ADR's Status Tracking.
- **Readout**: one committed query/aggregate + a five-line result note in the ADR. No dashboard required for the pilot.

## 10. Acceptance criteria

- [ ] **G1**: 24/24 snapshot URLs stored in `pilot-links-quadratics.json` and CDX-verified; committed
- [ ] Flag merged **default-OFF**; enabled only for `ial-p1-quadratics`; kill-flip rehearsed once in staging
- [ ] Module renders the 5 primary cards with `rel="nofollow"`, attribution line, staleness note, hub-authored hooks; absent flag ⇒ absent module (verified on a second lane)
- [ ] Health job scheduled; one dry-run report committed (all-200 baseline expected)
- [ ] Click events verified end-to-end by a real click in staging (both `target` values exercised)
- [ ] Readout query committed; verdict-due date calendared (enable date + 42 days)
- [ ] PR references this ticket + ADR-UGM-0001; UGM track reviews the render before enable

## 11. Rollout plan

PR to `syllabai-v2` (implementation, referencing this ticket) → staging verify (§10 rows 2–5) → enable flag for the pilot lane → day-0 note with enable date in the ADR Status Tracking → weekly job runs → **first CTR readout at enable+42 days** → verdict row appended to the ADR (continue / generalise-signal / kill). Total ≈3 dev-days; no data migrations; no core-era schema contact (side-table law respected by using config, not columns).

## 12. Open questions for the hub team

1. **Lane-page component path** — exact route/component for the IAL P1 Quadratics lane page under `apps/hub/` (this ticket specifies behaviour, not file paths; hub owns placement).
2. **Flag storage** — registry JSON as recommended, or side-table pattern? (§5 laws are the contract either way.)
3. **Analytics store** — existing event pipeline to reuse, or ship the minimal append-only table? If a pipeline exists, confirm it accepts custom events with the §9 properties.
4. **viewerRef source** — hashed session id vs learner id; confirm the pseudonymisation choice against hub privacy conventions (§9 requires pseudonymous only).
5. **Job runner** — cron via their infra vs native scheduled job; if native, port `link-health-check.sh`'s state machine and keep the report format for ADR-conformant auditability.

## Appendix A — full 24-link pool (baseline 2026-10-22: all live=200; Wayback = pending G1)

| # | Spec point | Resource | Slug | Live baseline | Wayback fallback |
|---|---|---|---|---|---|
| 1 | 1.1.1 | Name that graph | `name-that-graph` | 200 | **no snapshot — gap** |
| 2 | 1.1.1 | Paired parabolas | `paired-parabolas` | 200 | **no snapshot — gap** |
| 3 | 1.1.1 | Quadratic symmetry | `quad-symmetry` | 200 | **no snapshot — gap** |
| 4 | 1.1.1 | Which parabola? | `which-parabola` | 200 | **no snapshot — gap** |
| 5 | 1.1.1 | Which quadratic? | `which-quadratic` | 200 | **no snapshot — gap** |
| 6 | 1.1.2 | Discriminating | `discriminating` | 200 | **no snapshot — gap** |
| 7 | 1.1.2 | When are the roots for $x^2-bx+c=0$ real and positive? | `r5138` | 200 | **no snapshot — gap** |
| 8 | 1.1.2 | When does $x^2-4x-1=2k(x-5)$ have equal roots? | `r5316` | 200 | **no snapshot — gap** |
| 9 | 1.1.2 | For what values of $k$ is $x^2 + 6kx +144$ always positive? | `r6526` | 200 | **no snapshot — gap** |
| 10 | 1.1.2 | When does $x^2+(3k-7)x+(2k+6)=0$ have real roots? | `r6828` | 200 | **no snapshot — gap** |
| 11 | 1.1.3 | Factorisable quadratics | `factorisable-quads` | 200 | **no snapshot — gap** |
| 12 | 1.1.3 | Inequalities for some occasions | `inequalities-for-some-occasions` | 200 | **no snapshot — gap** |
| 13 | 1.1.3 | Irrational roots | `irrational-roots` | 200 | **no snapshot — gap** |
| 14 | 1.1.3 | Pick a card... | `pick-a-card` | 200 | **no snapshot — gap** |
| 15 | 1.1.3 | Quadratic solving sorter | `quad-solving-sorter` | 200 | **no snapshot — gap** |
| 16 | 1.1.4 | When does $y=mx-5$ intersect $y=x^2-1$  twice? | `r5287` | 200 | **no snapshot — gap** |
| 17 | 1.1.4 | Can we solve these simultaneous equations, one linear, one quadratic? | `r6429` | 200 | **no snapshot — gap** |
| 18 | 1.1.4 | When is this line a tangent to this parabola? | `r7328` | 200 | **no snapshot — gap** |
| 19 | 1.1.4 | Can we find the midpoint of a chord of this parabola? | `r8045` | 200 | **no snapshot — gap** |
| 20 | 1.1.4 | When does $y=kx$ intersect the parabola $y=(x-1)^2$? | `r9614` | 200 | **no snapshot — gap** |
| 21 | 1.1.5 | How do we  solve $x + 3\sqrt{x} − 1/2 = 0$? | `r6215` | 200 | **no snapshot — gap** |
| 22 | 1.1.5 | If $2y = a^x + a^{-x}$, can we find $a^x$? | `r6816` | 200 | **no snapshot — gap** |
| 23 | 1.1.5 | Can we solve $\sqrt{3-3x} - \sqrt{2-x} = 1$? | `r7485` | 200 | **no snapshot — gap** |
| 24 | 1.1.5 | When does $x^4=(x-c)^2$ have four real roots? | `r9546` | 200 | **no snapshot — gap** |

## Appendix B — ADR conformance map

| ADR-UGM-0001 requirement (§Decision 3) | Ticket section |
|---|---|
| One lane only (IAL P1 Quadratics) | §2, §5 (`lanes` map) |
| Feature flag, class-toggle practice | §5 |
| `rel="nofollow"` | §6 |
| Weekly link-health job; 3 consecutive failures ⇒ Wayback fallback + alert | §7 (plus fail-closed law where no snapshot exists) |
| CTR floor 1.0% continue / 3.0% generalise / below = kill + ADR amendment | §9 |
| 28-day window, 2-week grace | §9 (definitions fixed) |
| No UGM body text of record (hard line) | §2, §6 |
| Attribution + staleness on every render | §6 |
| Early-revisit trigger 1 (origin dark) surfaced to operator | §7 |
| Reversibility (flag kill) | §5, §11 |
