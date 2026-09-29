# P06: TICVAI Venue Staff, mobile shell

**What it is.** The staff phone app for work on the floor: tasks, orders at the table, stock counts, rentals and incidents. It works offline.

**Who uses it.** Floor staff, supervisors and runners, carrying the phone all shift.

## Reference design to match

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the client's employee app reference: dark theme, Home, Tasks, Scan, AI, More.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.

Open the file and match it. Do not describe it in words.

## Where it stands

- **96 screens.** 3 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P06-stock-on-the-floor-01`](../../P06-stock-on-the-floor-01/) | P06 · Stock on the Floor | 10 | to draw | 2 Block A |
| [`P06-operations-05`](../../P06-operations-05/) | P06 · Operations (5 of 5) | 6 | to draw | 1 Block A; 2 thin |

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P06-floor-service-01`](../../P06-floor-service-01/) | P06 · Floor Service | 10 | to draw |  |
| [`P06-operations-01`](../../P06-operations-01/) | P06 · Operations (1 of 5) | 10 | to draw |  |
| [`P06-operations-02`](../../P06-operations-02/) | P06 · Operations (2 of 5) | 10 | to draw |  |
| [`P06-operations-03`](../../P06-operations-03/) | P06 · Operations (3 of 5) | 10 | to draw |  |
| [`P06-operations-04`](../../P06-operations-04/) | P06 · Operations (4 of 5) | 10 | to draw | 3 thin |
| [`P06-rentals-02`](../../P06-rentals-02/) | P06 · Rentals (2 of 3) | 10 | to draw | 8 thin |
| [`P06-rentals-01`](../../P06-rentals-01/) | P06 · Rentals (1 of 3) | 10 | to draw | 9 thin |
| [`P06-rentals-03`](../../P06-rentals-03/) | P06 · Rentals (3 of 3) | 10 | to draw | 9 thin |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Staff, mobile shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf` and `sources/designs/TICVAI_POS_Terminal_client_approved.html`. This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
