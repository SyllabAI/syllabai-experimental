# Information architecture — tubemap, stations, lines, pervasive ideas

**Captured**: 2026-10-22 · data: `../resources/api/{stations,lines,pervasive-ideas,key-questions}.json`

## The tubemap metaphor

The site organises A level mathematics like a **London tube map**. From
`/about`: the tubemap "emphasises the connectedness of mathematics … organised
in a way that makes sense from a mathematical point of view, and is not tied
to any syllabus … doesn't place a strong emphasis of doing one topic before
another."

Entities (all present in the public API payloads):

- **Station** — a mathematical topic ("location" on the map). Each has:
  - `friendlyId` (slug), `title`, and a guiding **question**
    (e.g. quadratics → "How can we use the discriminant?" — every station
    frames itself as a question, not a chapter name).
  - `mapPositionX/mapPositionY` (floats) + `mapTextAngle` +
    `mapTextMaxWidth` — the station's rendered position on the SVG tubemap.
    The map layout is *data*, editable in their admin.
  - `publishStatus`, `hidden`, `underConstructionWarning` flags.
- **Line** — a curriculum thread crossing stations, with a tube-line colour:
  Number `#00a8e6`, Geometry `#ed1c24`, Algebra `#1900a4`, Functions
  `#c600d1`, Calculus `#18b300`. Each line lists its member `stationIds`
  (10–14 stations each); stations sit on 3–4 lines simultaneously — that
  overlap *is* the connectedness claim.
- **Pervasive idea** — a cross-cutting theme with its own page:
  averages, constraints, invariance, limits, symmetry, transforming.
- **Key question** — per station, a short list (3–6) of the questions the
  station is built around; resources link to key questions
  (`resource-key-questions` API). 113 captured.

Navigation UX detail (from `/about/website`): map/search/browse are **modal
dialogs** so users never lose their current location; the site deliberately
maintains "being at a particular location".

## Station inventory (24 live)

| Station (friendlyId) | Title | Resources | Key questions |
|---|---|---|---|
| quadratics | Quadratics | 59 | 3 |
| counting-and-binomials | Counting & Binomials | 51 | 4 |
| polynomials | Polynomials & Rational Functions | 51 | 5 |
| chain-rule | Chain Rule & Integration by Substitution | 49 | 5 |
| trigonometry-triangles-to-functions | Trigonometry: Triangles to Functions | 48 | 5 |
| circles | Circles | 47 | 5 |
| calculus-of-powers | Calculus of Powers | 48 | 5 |
| thinking-about-geometry | Thinking about Geometry | 43 | 4 |
| sequences | Sequences | 42 | 6 |
| calculus-meets-functions | Calculus meets Functions | 40 | 5 |
| exp-and-log | Exponentials & Logarithms | 40 | 5 |
| combining-functions | Combining Functions | 38 | 5 |
| geometry-of-equations | Geometry of Equations | 38 | 5 |
| thinking-about-algebra | Thinking about Algebra | 32 | 4 |
| thinking-about-numbers | Thinking about Numbers | 30 | 5 |
| product-rule | Product Rule & Integration by Parts | 28 | 4 |
| introducing-calculus | Introducing Calculus | 27 | 4 |
| trigonometry-compound-angles | Trigonometry: Compound Angles | 27 | 5 |
| vector-geometry | Vector Geometry | 27 | 5 |
| divisibility-and-induction | Divisibility & Induction | 25 | 5 |
| thinking-about-functions | Thinking about Functions | 23 | 5 |
| calculus-trig-log | Calculus of Trigonometry & Logarithms | 20 | 3 |
| combining-vectors | Combining Vectors | 12 | 4 |
| hyperbolic-functions | Hyperbolic Functions | 7 | 5 |

Under construction (API returns 401, no resources): `complex-numbers-plane`,
`complex-numbers-faces`, `differential-equations`,
`matrices-linear-transformations`.

Note the three "Thinking about …" stations — pure problem-solving/heuristics
stations sitting outside the topic canon, plus "Introducing calculus" as an
on-ramp. The naming encodes pedagogical role, not just topic.

## Lines × stations matrix (from `lines.json`)

| Line | Colour | # stations | Members |
|---|---|---|---|
| Number | `#00a8e6` | 14 | counting-and-binomials, thinking-about-numbers, thinking-about-algebra, thinking-about-geometry, divisibility-and-induction, polynomials, geometry-of-equations, circles, sequences, exp-and-log, trigonometry-*, vector-geometry, complex-numbers-faces |
| Geometry | `#ed1c24` | 14 | circles, geometry-of-equations, trigonometry-*, vector-geometry, thinking-about-geometry, exp-and-log, hyperbolic-functions, combining-vectors, complex-numbers-plane, matrices-linear-transformations, … |
| Algebra | `#1900a4` | 12 | polynomials, quadratics, thinking-about-algebra, divisibility-and-induction, sequences, counting-and-binomials, exp-and-log, … |
| Functions | `#c600d1` | 14 | combining-functions, thinking-about-functions, quadratics, polynomials, exp-and-log, trigonometry-*, calculus-*, … |
| Calculus | `#18b300` | 10 | introducing-calculus, calculus-of-powers, calculus-meets-functions, chain-rule, product-rule, calculus-trig-log, differential-equations, power-series, hyperbolic-functions, combining-functions |

(Exact membership per line in `../resources/api/lines.json`.)

## Pervasive ideas

Six pages, each arguing the idea's role across the whole A level:

averages · constraints · invariance · limits · symmetry · transforming

Resources link to pervasive ideas via `resource-related-pervasive-ideas`.
This is a **second, orthogonal taxonomy** on top of stations/lines — a
misconception/insight-oriented one. SyllabAI analogue: cross-topic learner
struggles (Paper A four-layer model).

## Key questions

Each station declares 3–6 key questions (e.g. quadratics:
`connect-alg-graph`, `quad-roots`, `discriminant` — slug + question text).
Resources carry `resource-key-questions` links, so a question page can
aggregate all resources addressing it. Key questions are the **third
navigation axis** (station → line → key question → pervasive idea).

## Observations for SyllabAI

1. **Four orthogonal taxonomies** (station, line, key question, pervasive
   idea) over one resource corpus — all stored as simple relation tables
   (`resource-lines`, `resource-key-questions`, `resource-related-pervasive-ideas`).
   Cheap to model, expensive to author well; the value is in the curation.
2. Station positions on the map are **content data** (DB columns), not
   design assets — the map is a view over relations.
3. The tubemap deliberately avoids syllabus ordering; syllabus mapping
   (2017 A level page) is a separate surface. SyllabAI can keep its
   exam-board spines and cross-map to a mathematical organisation like this.
4. Every station is a **question**, and every key question is a question —
   the taxonomy itself is inquisitive rather than declarative; worth
   mimicking in tutor-facing UI.
