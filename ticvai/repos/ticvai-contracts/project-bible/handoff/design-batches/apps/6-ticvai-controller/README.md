# TICVAI main controller

> **One working file for the whole app** (decided 30 September): `return/TICVAI Main Controller.dc.html` in this folder. Every batch below adds its screens to that one file.

TICVAI's own console for running the platform (P09), with tenant sign-up and purchase (P17) and the developer portal (P14).

**Run order:** Block A batches first, in the order each section below lists them. Special folders that belong to this app: none.

Sections: P09, P17, P14

## P09: TICVAI Control, web

**What it is.** TICVAI's own console. Tenants, licences, releases, security, platform health and the AI set-up.

**Who uses it.** TICVAI platform staff, on a desktop.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

### Where it stands

- **676 screens.** 44 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P09-ai-01`](../../P09-ai-01/) | P09 · AI | 1 | to draw | 1 Block A; changed: ADM-037 |
| [`WS36`](../../WS36/) | Pricing   Revenue Management board 3 | 10 | to draw | 3 Block A; changed: ADM-069, ADM-077; 1 thin |
| [`WS151`](../../WS151/) | Payment Payment Orchestration board 5 | 10 | to draw | 1 Block A; changed: ADM-603; 2 thin |
| [`WS124`](../../WS124/) | AI Governance board 4 | 10 | to draw | 2 Block A; changed: ADM-554, ADM-556; 3 thin |
| [`WS18`](../../WS18/) | Approval Workflows and Governance board 6 | 10 | to draw | 1 Block A; changed: ADM-342; 4 thin |
| [`WS122`](../../WS122/) | AI Governance board 2 | 10 | to draw | 1 Block A; changed: ADM-536; 4 thin |
| [`WS121`](../../WS121/) | AI Governance board 1 | 10 | to draw | 5 Block A; changed: ADM-520, ADM-523, ADM-526, ADM-527, ADM-528; 5 thin |
| [`WS19`](../../WS19/) | Approval Workflows and Governance board 7 | 10 | to draw | 1 Block A; changed: ADM-354; 6 thin |
| [`WS119`](../../WS119/) | AI Forecasting and Predictive Intelligence board 1 | 10 | to draw | 1 Block A; changed: ADM-508; 7 thin |
| [`P09-branding-localisation-01`](../../P09-branding-localisation-01/) | P09 · Branding & Localisation | 4 | to draw | 3 Block A |
| [`P09-security-compliance-01`](../../P09-security-compliance-01/) | P09 · Security & Compliance | 2 | to draw | 1 Block A |
| [`P09-tenants-licensing-01`](../../P09-tenants-licensing-01/) | P09 · Tenants & Licensing | 9 | to draw | 2 Block A |
| [`WS34`](../../WS34/) | Pricing   Revenue Management board 1 | 10 | to draw | 4 Block A; 2 thin |
| [`WS38`](../../WS38/) | Pricing   Revenue Management board 5 | 10 | to draw | 3 Block A; 2 thin |
| [`WS49`](../../WS49/) | Promotions   Bundles Management board 5 | 10 | to draw | 3 Block A; 2 thin |
| [`WS48`](../../WS48/) | Promotions   Bundles Management board 4 | 10 | to draw | 4 Block A; 3 thin |
| [`WS148`](../../WS148/) | Payment Payment Orchestration board 2 | 10 | to draw | 1 Block A; 4 thin |
| [`WS46`](../../WS46/) | Promotions   Bundles Management board 2 | 10 | to draw | 1 Block A; 5 thin |
| [`WS53`](../../WS53/) | Promotions   Bundles Management board 9 | 10 | to draw | 1 Block A; 5 thin |
| [`WS47`](../../WS47/) | Promotions   Bundles Management board 3 | 10 | to draw | 2 Block A; 6 thin |
| [`WS51`](../../WS51/) | Promotions   Bundles Management board 7 | 10 | to draw | 1 Block A; 6 thin |
| [`WS102`](../../WS102/) | Subscription Licensing AI Self Service board 5 | 10 | to draw | 1 Block A; 7 thin |
| [`WS43`](../../WS43/) | Product Lifecycle   Catalogue Governance board 1 | 10 | to draw | 1 Block A; 9 thin |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P09-infrastructure-resilienc-01`](../../P09-infrastructure-resilienc-01/) | P09 · Infrastructure & Resilience | 4 | to draw |  |
| [`P09-overview-health-01`](../../P09-overview-health-01/) | P09 · Overview & Health | 5 | to draw |  |
| [`P09-platform-ops-01`](../../P09-platform-ops-01/) | P09 · Platform Ops | 1 | to draw |  |
| [`P09-support-communications-01`](../../P09-support-communications-01/) | P09 · Support & Communications | 2 | to draw |  |
| [`P09-access-identity-01`](../../P09-access-identity-01/) | P09 · Access & Identity | 3 | to draw | 1 thin |
| [`WS62`](../../WS62/) | Ticket Resale Marketplace board 1 | 10 | to draw | 1 thin |
| [`P09-releases-environments-01`](../../P09-releases-environments-01/) | P09 · Releases & Environments | 7 | to draw | 2 thin |
| [`WS40`](../../WS40/) | Pricing   Revenue Management board 7 | 10 | to draw | 2 thin |
| [`WS54`](../../WS54/) | Promotions   Bundles Management board 10 | 10 | to draw | 2 thin |
| [`WS55`](../../WS55/) | Rules  Workflow  Approval   Automation Engine board 1 | 10 | to draw | 2 thin |
| [`WS57`](../../WS57/) | Sales Channel Management board 1 | 10 | to draw | 2 thin |
| [`WS58`](../../WS58/) | Sales Channel Management board 2 | 10 | to draw | 2 thin |
| [`WS63`](../../WS63/) | Ticket Resale Marketplace board 2 | 10 | to draw | 2 thin |
| [`WS98`](../../WS98/) | Subscription Licensing AI Self Service board 1 | 10 | to draw | 2 thin |
| [`WS150`](../../WS150/) | Payment Payment Orchestration board 4 | 10 | to draw | 2 thin |
| [`WS37`](../../WS37/) | Pricing   Revenue Management board 4 | 10 | to draw | 3 thin |
| [`WS45`](../../WS45/) | Promotions   Bundles Management board 1 | 10 | to draw | 3 thin |
| [`WS65`](../../WS65/) | Ticket Upgrade, Exchange & Conversion board 1 | 10 | to draw | 3 thin |
| [`WS147`](../../WS147/) | Payment Payment Orchestration board 1 | 10 | to draw | 3 thin |
| [`WS154`](../../WS154/) | Payment Payment Orchestration board 8 | 10 | to draw | 3 thin |
| [`WS183`](../../WS183/) | Upsell,CrossSellEngine board 4 | 10 | to draw | 3 thin |
| [`WS185`](../../WS185/) | Upsell,CrossSellEngine board 6 | 10 | to draw | 3 thin |
| [`WS24`](../../WS24/) | Communication & Notification Platform Services board 1 | 10 | to draw | 4 thin |
| [`WS35`](../../WS35/) | Pricing   Revenue Management board 2 | 10 | to draw | 4 thin |
| [`WS100`](../../WS100/) | Subscription Licensing AI Self Service board 3 | 10 | to draw | 4 thin |
| [`WS149`](../../WS149/) | Payment Payment Orchestration board 3 | 10 | to draw | 4 thin |
| [`WS44`](../../WS44/) | Product Lifecycle   Catalogue Governance board 2 | 10 | to draw | 5 thin |
| [`WS56`](../../WS56/) | Rules  Workflow  Approval   Automation Engine board 2 | 10 | to draw | 5 thin |
| [`WS116`](../../WS116/) | AI Configuration Assistant board 1 | 10 | to draw | 5 thin |
| [`WS181`](../../WS181/) | Upsell,CrossSellEngine board 2 | 10 | to draw | 5 thin |
| [`WS39`](../../WS39/) | Pricing   Revenue Management board 6 | 10 | to draw | 6 thin |
| [`WS50`](../../WS50/) | Promotions   Bundles Management board 6 | 10 | to draw | 6 thin |
| [`WS52`](../../WS52/) | Promotions   Bundles Management board 8 | 10 | to draw | 6 thin |
| [`WS64`](../../WS64/) | Ticket Resale Marketplace board 3 | 10 | to draw | 6 thin |
| [`WS103`](../../WS103/) | Subscription Licensing AI Self Service board 6 | 9 | to draw | 6 thin |
| [`WS107`](../../WS107/) | Subscription Licensing AI Self Service board 10 | 10 | to draw | 6 thin |
| [`WS118`](../../WS118/) | AI Configuration Assistant board 3 | 10 | to draw | 6 thin |
| [`WS152`](../../WS152/) | Payment Payment Orchestration board 6 | 10 | to draw | 6 thin |
| [`WS153`](../../WS153/) | Payment Payment Orchestration board 7 | 10 | to draw | 6 thin |
| [`WS180`](../../WS180/) | Upsell,CrossSellEngine board 1 | 10 | to draw | 6 thin |
| [`WS14`](../../WS14/) | Approval Workflows and Governance board 2 | 9 | to draw | 7 thin |
| [`WS99`](../../WS99/) | Subscription Licensing AI Self Service board 2 | 10 | to draw | 7 thin |
| [`WS117`](../../WS117/) | AI Configuration Assistant board 2 | 10 | to draw | 7 thin |
| [`WS120`](../../WS120/) | AI Forecasting and Predictive Intelligence board 2 | 10 | to draw | 7 thin |
| [`WS123`](../../WS123/) | AI Governance board 3 | 10 | to draw | 7 thin |
| [`WS182`](../../WS182/) | Upsell,CrossSellEngine board 3 | 10 | to draw | 7 thin |
| [`WS184`](../../WS184/) | Upsell,CrossSellEngine board 5 | 10 | to draw | 7 thin |
| [`WS15`](../../WS15/) | Approval Workflows and Governance board 3 | 10 | to draw | 8 thin |
| [`WS106`](../../WS106/) | Subscription Licensing AI Self Service board 9 | 10 | to draw | 8 thin |
| [`WS20`](../../WS20/) | Approval Workflows and Governance board 8 | 10 | to draw | 9 thin |
| [`WS101`](../../WS101/) | Subscription Licensing AI Self Service board 4 | 10 | to draw | 10 thin |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, web. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/6-ticvai-controller/return/TICVAI Main Controller.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Main Controller file". Claude Code captures each of that batch's screens from `return/TICVAI Main Controller.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P17: TICVAI Control, sign-up

**What it is.** The public sign-up. A venue business finds out if TICVAI fits, builds a package, buys it and activates it.

**Who uses it.** Prospects: owners and managers of venues, not yet customers.

### Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for finish.

Open the file and match it. Do not describe it in words.

### Where it stands

- **24 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

**Every screen here declares no operation** (`apis: []`). Build from the screen content only; there is no data to seed from a schema.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P17-onboarding-assessment-01`](../../P17-onboarding-assessment-01/) | P17 · Onboarding & Assessment | 10 | to draw | 7 thin |
| [`P17-package-builder-01`](../../P17-package-builder-01/) | P17 · Package Builder | 7 | to draw | 7 thin |
| [`P17-purchase-activation-01`](../../P17-purchase-activation-01/) | P17 · Purchase & Activation | 7 | to draw | 7 thin |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, sign-up. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. This is a public marketing and sign-up web flow, 1440 desktop and 390 phone widths, in TICVAI's own brand. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/6-ticvai-controller/return/TICVAI Main Controller.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Main Controller file". Claude Code captures each of that batch's screens from `return/TICVAI Main Controller.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P14: TICVAI Control, developer portal

**What it is.** The developer portal. Partners register, get API keys, read the docs and ask for production access.

**Who uses it.** Developers at partner companies.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish.

Open the file and match it. Do not describe it in words.

### Where it stands

- **8 screens.** 3 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P14-developer-api-01`](../../P14-developer-api-01/) | P14 · Developer & API | 8 | to draw | 3 Block A; changed: DEV-003, DEV-008 |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, developer portal. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is a developer portal on a desktop browser, 1440 wide, with a docs-style left navigation. Add this batch's screens to the one working file for the whole app, handoff/design-batches/apps/6-ticvai-controller/return/TICVAI Main Controller.dc.html (create it with the first batch; every later batch extends the same file and keeps every earlier screen working, with one shared navigation, one shared seeded dataset and one look), where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

When a batch is back, tell Claude Code "batch <BATCH ID> is in the Main Controller file". Claude Code captures each of that batch's screens from `return/TICVAI Main Controller.dc.html` as a frame (by its `#<screen id>` link), imports the frames, and refreshes the boards:

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
