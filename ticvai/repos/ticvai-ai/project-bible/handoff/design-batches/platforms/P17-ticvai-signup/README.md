# P17: TICVAI Control, sign-up

**What it is.** The public sign-up. A venue business finds out if TICVAI fits, builds a package, buys it and activates it.

**Who uses it.** Prospects: owners and managers of venues, not yet customers.

## Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for finish.

Open the file and match it. Do not describe it in words.

## Where it stands

- **24 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

**Every screen here declares no operation** (`apis: []`). Build from the screen content only; there is no data to seed from a schema.

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P17-onboarding-assessment-01`](../../P17-onboarding-assessment-01/) | P17 · Onboarding & Assessment | 10 | to draw | 7 thin |
| [`P17-package-builder-01`](../../P17-package-builder-01/) | P17 · Package Builder | 7 | to draw | 7 thin |
| [`P17-purchase-activation-01`](../../P17-purchase-activation-01/) | P17 · Purchase & Activation | 7 | to draw | 7 thin |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, sign-up. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
