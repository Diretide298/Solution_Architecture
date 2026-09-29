# P12: TICVAI Venue Management, support section

**What it is.** The support agent console. Conversations, the knowledge base and agent availability.

**Who uses it.** Venue support agents, on a desktop, often handling several chats at once.

## Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for operator density.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

## Where it stands

- **28 screens.** 1 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P12-overview-01`](../../P12-overview-01/) | P12 · Overview | 2 | to draw | 1 Block A |

### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P12-access-availability-01`](../../P12-access-availability-01/) | P12 · Access & Availability | 2 | to draw |  |
| [`P12-conversations-01`](../../P12-conversations-01/) | P12 · Conversations | 2 | to draw |  |
| [`P12-knowledge-responses-01`](../../P12-knowledge-responses-01/) | P12 · Knowledge & Responses | 2 | to draw | 1 thin |
| [`WS25`](../../WS25/) | Customer Service board 1 | 10 | to draw | 3 thin |
| [`WS26`](../../WS26/) | Customer Service board 2 | 10 | to draw | 4 thin |

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, support section. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
