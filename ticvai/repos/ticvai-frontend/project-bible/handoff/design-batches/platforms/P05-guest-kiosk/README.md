# P05: TICVAI Guest, kiosk shell

**What it is.** The self-service kiosk at the venue entrance. The guest product in a fixed frame, with no keyboard.

**Who uses it.** Guests at the gate who did not buy online. They want a ticket fast and a printed receipt.

## Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved guest look. The kiosk is the same product, narrower.
- `wireframes/reference/Kiosk Board 1.dc.html`: the client's kiosk board, for layout (and Kiosk Board 2).

Open the file and match it. Do not describe it in words.

## Where it stands

- **17 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P05-ai-01`](../../P05-ai-01/) | P05 · AI | 1 | to draw |  |
| [`P05-sell-02`](../../P05-sell-02/) | P05 · Sell (2 of 2) | 6 | to draw | 3 thin |
| [`P05-sell-01`](../../P05-sell-01/) | P05 · Sell (1 of 2) | 10 | to draw | 6 thin |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Guest, kiosk shell. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html` and `wireframes/reference/Kiosk Board 1.dc.html`. This is a portrait touch kiosk, 1080 x 1920, large touch targets, no keyboard, an attract screen when idle. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
