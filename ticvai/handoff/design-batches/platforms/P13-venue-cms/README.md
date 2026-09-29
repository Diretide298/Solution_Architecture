# P13: TICVAI Venue Management, CMS section

**What it is.** The white-label CMS. The venue builds and publishes its website and app: brand, pages, booking flows, the mobile app and store publishing.

**Who uses it.** The venue's marketing or digital team, and TICVAI's set-up team on day one.

## Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html`: the look of the controls: every configuration control, laid out and explained.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the configuration side panel, for the controls, and the guest booking the live preview shows.
- `sources/designs/TICVAI_White_Label_Guest_App_UI_Reference_1.pdf`: the client's White Label Builder boards.

Open the file and match it. Do not describe it in words.

## Where it stands

- **103 screens.** 25 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

**Start with the flow builder** (`../../CMS-FLOW-BUILDER/`): CMS-101 Help me choose and the new CMS-102 Site Builder, CMS-103 Booking Flows and CMS-104 App Build & Store Publishing, drawn as one flow.

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P13-white-label-03`](../../P13-white-label-03/) | P13 · White Label (3 of 3) | 3 | to draw | 3 Block A; new: CMS-102, CMS-103, CMS-104 |
| [`P13-white-label-01`](../../P13-white-label-01/) | P13 · White Label (1 of 3) | 10 | to draw | 10 Block A; changed: CMS-001, CMS-004, CMS-005, CMS-007, CMS-008, CMS-009, CMS-010; 1 thin |
| [`P13-white-label-02`](../../P13-white-label-02/) | P13 · White Label (2 of 3) | 10 | to draw | 10 Block A; changed: CMS-014, CMS-016, CMS-101; 2 thin |
| [`WS41`](../../WS41/) | Privacy  Consent   Preference Management board 1 | 10 | to draw | 2 Block A; changed: CMS-025, CMS-026; 3 thin |

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`WS72`](../../WS72/) | Waiver, Consent & Digital Form Management board 1 | 10 | to draw | 2 thin |
| [`WS42`](../../WS42/) | Privacy  Consent   Preference Management board 2 | 10 | to draw | 3 thin |
| [`WS74`](../../WS74/) | Digital Asset Management DAM board 1 | 10 | to draw | 3 thin |
| [`WS75`](../../WS75/) | Digital Asset Management DAM board 2 | 10 | to draw | 3 thin |
| [`WS77`](../../WS77/) | Digital Asset Management DAM board 4 | 10 | to draw | 3 thin |
| [`WS73`](../../WS73/) | Waiver, Consent & Digital Form Management board 2 | 10 | to draw | 4 thin |
| [`WS76`](../../WS76/) | Digital Asset Management DAM board 3 | 10 | to draw | 6 thin |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, CMS section. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html` and `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of the guest site or app on the right where a screen changes what guests see. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
