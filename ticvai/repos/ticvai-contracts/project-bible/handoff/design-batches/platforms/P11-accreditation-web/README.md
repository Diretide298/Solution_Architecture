# P11: TICVAI Control, accreditation web

**What it is.** The public accreditation portal. Media, staff and suppliers apply for event credentials; reviewers decide.

**Who uses it.** Applicants from outside (public) and TICVAI or venue reviewers.

## Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for forms and finish.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for the reviewer screens' density.

Open the file and match it. Do not describe it in words.

## Where it stands

- **8 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P11-applicant-journey-01`](../../P11-applicant-journey-01/) | P11 · Applicant Journey | 5 | to draw |  |
| [`P11-reviewer-internal-01`](../../P11-reviewer-internal-01/) | P11 · Reviewer (Internal) | 3 | to draw |  |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, accreditation web. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html` and `sources/designs/TICVAI_POS_Terminal_client_approved.html`. This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
