# Brief — generating new boards

For Claude Code, when a platform needs a board that does not exist yet, or an existing board
needs screens added.

**Read this and one existing board before starting.** `P07 Staff Scanner.dc.html` is the
smallest and shows every pattern; `P08 Staff Web Back Office.dc.html` is the largest and shows
how the patterns hold at scale.

---

## What a board is

One self-contained HTML file per platform. Every screen for that platform, on one scrolling
page, at low fidelity. **A reviewer opens it in a browser and reads the whole surface in one
pass** — that is the only thing a board is for, and every decision below follows from it.

Not a prototype. Nothing is clickable except the navigation between screens and boards. No
imagery, no real copy beyond field labels, no interaction states.

---

## The five sources — read all of them

| | Where | What you take |
|---|---|---|
| **Screen definitions** | `screens/P*.yaml` | Ids, names, purposes, operations, layout regions, states, navigation. **This is the specification** |
| **Design tokens** | `designs/Park_POS_dc.html` | Manrope, `#0D6EFD → #00B8FF`, `#E5E7EB` borders, 10–16px radii, `#0B1324` rail |
| **Client references** | `designs/*UI_Reference*.pdf` | Board format, status pill vocabulary, the device frame, dark venue-staff-app theme |
| **Data lineage** | `handoff/api-data-lineage.json` | Which tables an operation reads, so a table can render real column names |
| **Screen index** | `handoff/screen-index.json` | The pre-computed join — board link, operations, service, tables, per screen |

**Do not invent field names.** A data table renders the columns the operation's response schema
actually carries; `api-data-lineage.json` and the contracts have them. A wireframe with plausible
invented columns is worse than one with none, because it gets reviewed and approved.

---

## Structure

    ← All boards                                    (back-link, top left)

    TICVAI          BOARD n: PLATFORM NAME (n SCREENS)          context · actions
    ─────────────────────────────────────────────────────────────────────────────
    ① screen   ② screen   ③ screen   ④ screen   ⑤ screen
    ⑥ screen   ⑦ screen   ⑧ screen   ⑨ screen   ⑩ screen
    ─────────────────────────────────────────────────────────────────────────────
    reassurance          tenant · environment          help · primary action

**Ten screens to a row group**, matching the client's own reference boards. A board with 73
screens is eight groups, each with a heading naming what that group is for.

### Each screen frame

    ┌──────────────────────────────────────────┐
    │ SCN-004 · Admitted                wave 1 │   ← id in mono, name in 800 weight
    │ Purpose, one line, from the YAML         │
    ├──────────────────────────────────────────┤
    │  the frame — chrome and regions          │
    ├──────────────────────────────────────────┤
    │ OPERATIONS · validateAccess              │
    │ STATES · loading · empty · error · offline│
    │ GOES TO · SCN-003                         │
    └──────────────────────────────────────────┘

**The anchor is `id="scn-004"`** — lowercase, matching the screen id. Everything links on that,
in both directions, and `check-wireframes.py` fails if it does not resolve.

---

## Rendering the frame

Regions go where they belong, not stacked. A reviewer judging whether the cart belongs beside
the board or beneath it cannot answer that from a stack.

| Region | Renders as |
|---|---|
| `sideNav` | Dark rail, 96px, gradient active state |
| `statusStrip` | Thin bar under the header. **Offline platforms only** |
| `appHeader` | Search, platform name, user |
| `contentBody` | The main column |
| `contextPanel` | Right column, 264px |
| `actionBar` | Pinned bottom, buttons left to right as declared |
| `bottomNav` | Mobile only, five items |

**Component kinds render to shapes**, and the vocabulary is in `screens/_components.yaml` — 34
kinds. A `dataTable` gets real headers and three plausible rows; a `metricTile` gets a value and
a label; a `seatMap` gets a hatched placeholder at the venue aspect ratio.

---

## Six rules that matter more than the styling

**1. Every declared state appears on the frame.** Loading, empty, error, and on an
offline-capable platform, offline. **The offline state is the most important line on a venue-scanner
or POS screen and a static mockup hides it** — list it under the frame rather than pretending
the happy path is the screen.

**2. The `notes` on a component are rendered.** They carry the reasoning — *"`unknown` is the
important one: a terminal that charged a card and never returned a response"* — and a board
without them is a board that loses why.

**3. Nothing is invented.** If the YAML declares no operations, the frame says `OPERATIONS ·
none declared` rather than guessing. That gap is real and should be visible.

**4. Ugly on purpose.** Grey boxes, no imagery, no real copy. **A wireframe that looks designed
invites comment on the design; one that looks like a wireframe invites comment on whether the
right things are on the screen**, which is the only question worth asking at this stage.

**5. Cross-platform jumps are drawn and declared.** Where a screen reaches another platform —
accreditation-web reaching `SCN-003`, support reaching `ADM-035` — draw it in a "Reaches other
platforms" panel **and add `reachesOtherPlatforms` to the platform block in the YAML.** The
checker verifies both ends.

**6. Back-link on every board.** `← All boards` at the top, pointing at
`TICVAI%20Wireframe%20Boards.dc.html`. There was no way home until 14 August and it was the
first thing anyone noticed.

---

## Theme by audience, not by platform

Three visual languages exist in the delivered references and **they are a decision, not an
accident**:

| | Theme |
|---|---|
| Guest surfaces — web, app, kiosk | **Light.** Navy `#0C2340`, white cards |
| Staff surfaces — POS, venue-scanner, back office, admin | **Light**, TICVAI-branded, `#0D6EFD` gradient |
| Employee mobile app | **Dark.** Navy ground, cyan accent, raised centre action |

**The kiosk is the case that makes the rule.** It is venue hardware and a guest-app uses it, so it
is white-labelled like the website, not TICVAI-branded like the POS beside it. Confirmed
14 August.

---

## When you finish

    python3 tools/check-wireframes.py

It verifies that every screen points at an anchor that exists, every anchor has a definition,
every href resolves file and anchor, every cross-platform reach is declared, and that a
platform's board matches its code.

**Then update the screen definitions**: `wireframe.board` on each screen, `wireframeBoard` on
the platform. A board nothing points at is a board nobody finds.

---

## If a screen has no definition

**Stop and write the definition first.** A board drawn from a name produces a picture the
contract will contradict, and the contradiction surfaces during build rather than during
review.

Adding a definition is cheap: the operation usually exists with a request body already written,
so the fields are there and simply have not been transcribed onto a screen.
