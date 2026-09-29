# P07: TICVAI Venue Staff, handheld shell

**What it is.** The gate scanner. It scans tickets and passes, shows pass or fail at a glance, and keeps working offline.

**Who uses it.** Gate staff, scanning hundreds of guests an hour, often in the sun.

## Reference design to match

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the employee app reference. The scanner shares its look and its offline strip.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for density.

Open the file and match it. Do not describe it in words.

## Where it stands

- **11 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P07-access-02`](../../P07-access-02/) | P07 · Access (2 of 2) | 1 | to draw |  |
| [`P07-access-01`](../../P07-access-01/) | P07 · Access (1 of 2) | 10 | to draw | 1 thin |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Staff, handheld shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf` and `sources/designs/TICVAI_POS_Terminal_client_approved.html`. This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
