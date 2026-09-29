# P16: TICVAI Venue Management, analytics section

**What it is.** Venue analytics. Dashboards and reports across sales, visits, food and retail, with AI explanations.

**Who uses it.** Venue managers and analysts, on a desktop.

## Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

## Where it stands

- **70 screens.** 4 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

ANL-071 is new on 29 September (batch P16-analytics-02).

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`WS66`](../../WS66/) | Unified BI Reporting and AI Analytics Platform board 1 | 9 | to draw | 1 Block A; changed: ANL-019; 2 thin |
| [`WS71`](../../WS71/) | Unified BI Reporting and AI Analytics Platform board 10 | 10 | to draw | 1 Block A; 4 thin |
| [`WS67`](../../WS67/) | Unified BI Reporting and AI Analytics Platform board 2 | 10 | to draw | 2 Block A; 5 thin |

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P16-analytics-01`](../../P16-analytics-01/) | P16 · Analytics (1 of 2) | 10 | to draw |  |
| [`P16-analytics-02`](../../P16-analytics-02/) | P16 · Analytics (2 of 2) | 1 | to draw | new: ANL-071 |
| [`WS69`](../../WS69/) | Unified BI Reporting and AI Analytics Platform board 4 | 10 | to draw | 4 thin |
| [`WS68`](../../WS68/) | Unified BI Reporting and AI Analytics Platform board 3 | 10 | to draw | 6 thin |
| [`WS70`](../../WS70/) | Unified BI Reporting and AI Analytics Platform board 9 | 10 | to draw | 7 thin |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, analytics section. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
