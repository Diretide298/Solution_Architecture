# Venue Management

The venue's back office on the web: setup and daily management (P08), the CMS and flow builder (P13), analytics (P16), the support agent console (P12) and the accreditation applicant web (P11).

**Run order:** Block A batches first, in the order each section below lists them. Special folders that belong to this app: [CMS flow builder](../../CMS-FLOW-BUILDER/) (Block A, run first).

Sections: P08, P13, P16, P12, P11

## P08: TICVAI Venue Management, web

**What it is.** The venue's back office. Set up products, prices, access, staff, stock and outlets, and see what happened.

**Who uses it.** Venue managers, finance, operations and set-up staff, on a desktop.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

### Where it stands

- **1186 screens.** 66 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

See `../../VENUE-MANAGEMENT.md` for how a batch session runs. **Block A needs the set-up screens first**: the Venue Home hub and the screens a venue fills in before it can sell.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P08-access-venue-01`](../../P08-access-venue-01/) | P08 · Access & Venue (1 of 3) | 10 | to draw | 5 Block A; changed: BO-005 |
| [`P08-orders-money-01`](../../P08-orders-money-01/) | P08 · Orders & Money (1 of 3) | 10 | to draw | 2 Block A; changed: BO-008 |
| [`P08-orders-money-02`](../../P08-orders-money-02/) | P08 · Orders & Money (2 of 3) | 10 | to draw | 1 Block A; changed: BO-065 |
| [`P08-venue-operations-01`](../../P08-venue-operations-01/) | P08 · Venue Operations (1 of 2) | 10 | to draw | 2 Block A; changed: BO-044 |
| [`P08-access-venue-02`](../../P08-access-venue-02/) | P08 · Access & Venue (2 of 3) | 10 | to draw | 3 Block A; changed: BO-093, BO-094; 1 thin |
| [`P08-guests-marketing-01`](../../P08-guests-marketing-01/) | P08 · Guests & Marketing | 4 | to draw | 1 Block A; changed: BO-091; 1 thin |
| [`P08-people-access-rights-01`](../../P08-people-access-rights-01/) | P08 · People & Access Rights (1 of 2) | 10 | to draw | 3 Block A; changed: BO-053, BO-054, BO-087; 1 thin |
| [`P08-sell-01`](../../P08-sell-01/) | P08 · Sell (1 of 4) | 10 | to draw | 5 Block A; changed: BO-007, BO-011; 1 thin |
| [`P08-stock-supply-01`](../../P08-stock-supply-01/) | P08 · Stock & Supply (1 of 2) | 10 | to draw | 1 Block A; changed: BO-081; 1 thin |
| [`WS156`](../../WS156/) | Resource Management Configuration board 2 | 9 | to draw | 2 Block A; changed: BO-866; 4 thin |
| [`WS161`](../../WS161/) | Resource Management Configuration board 7 | 10 | to draw | 1 Block A; changed: BO-919; 5 thin |
| [`WS10`](../../WS10/) | Access Control board 10 | 10 | to draw | 3 Block A; changed: BO-234, BO-243; 6 thin |
| [`WS162`](../../WS162/) | Resource Management Configuration board 8 | 10 | to draw | 1 Block A; changed: BO-927; 8 thin |
| [`WS138`](../../WS138/) | Marketing CRM Configuration Reference v1.0 board 4 | 10 | to draw | 1 Block A; changed: BO-766; 9 thin |
| [`WS145`](../../WS145/) | Marketing CRM Configuration Reference v1.0 board 11 | 10 | to draw | 1 Block A; changed: BO-839; 9 thin |
| [`WS108`](../../WS108/) | ACCREDITATION board 1 | 10 | to draw | 1 Block A; changed: BO-618; 10 thin |
| [`WS140`](../../WS140/) | Marketing CRM Configuration Reference v1.0 board 6 | 10 | to draw | 1 Block A; changed: BO-785; 10 thin |
| [`P08-orders-money-03`](../../P08-orders-money-03/) | P08 · Orders & Money (3 of 3) | 7 | to draw | 3 Block A |
| [`P08-sell-02`](../../P08-sell-02/) | P08 · Sell (2 of 4) | 10 | to draw | 1 Block A |
| [`P08-sell-03`](../../P08-sell-03/) | P08 · Sell (3 of 4) | 10 | to draw | 2 Block A |
| [`P08-venue-operations-02`](../../P08-venue-operations-02/) | P08 · Venue Operations (2 of 2) | 5 | to draw | 1 Block A |
| [`WS60`](../../WS60/) | Ticket Media   Credential Management board 2 | 10 | to draw | 1 Block A |
| [`P08-food-beverage-01`](../../P08-food-beverage-01/) | P08 · Food & Beverage | 8 | to draw | 2 Block A; 1 thin |
| [`P08-sell-04`](../../P08-sell-04/) | P08 · Sell (4 of 4) | 6 | to draw | 1 Block A; 1 thin |
| [`WS06`](../../WS06/) | Access Control board 6 | 10 | to draw | 1 Block A; 2 thin |
| [`WS05`](../../WS05/) | Access Control board 5 | 10 | to draw | 3 Block A; 3 thin |
| [`WS59`](../../WS59/) | Ticket Media   Credential Management board 1 | 10 | to draw | 1 Block A; 3 thin |
| [`WS82`](../../WS82/) | Game and Ride board 5 | 10 | to draw | 1 Block A; 3 thin |
| [`WS125`](../../WS125/) | Event Management Configuration Backend Structure v1.0 board 1 | 3 | to draw | 1 Block A; 3 thin |
| [`WS155`](../../WS155/) | Resource Management Configuration board 1 | 10 | to draw | 2 Block A; 3 thin |
| [`WS157`](../../WS157/) | Resource Management Configuration board 3 | 10 | to draw | 1 Block A; 3 thin |
| [`WS02`](../../WS02/) | Access Control board 2 | 10 | to draw | 2 Block A; 4 thin |
| [`WS08`](../../WS08/) | Access Control board 8 | 10 | to draw | 1 Block A; 4 thin |
| [`WS03`](../../WS03/) | Access Control board 3 | 10 | to draw | 3 Block A; 5 thin |
| [`WS131`](../../WS131/) | Event Management Configuration Backend Structure v1.0 board 7 | 5 | to draw | 1 Block A; 5 thin |
| [`WS01`](../../WS01/) | Access Control board 1 | 10 | to draw | 1 Block A; 8 thin |
| [`WS144`](../../WS144/) | Marketing CRM Configuration Reference v1.0 board 10 | 10 | to draw | 2 Block A; 8 thin |
| [`WS137`](../../WS137/) | Marketing CRM Configuration Reference v1.0 board 3 | 10 | to draw | 1 Block A; 9 thin |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P08-access-venue-03`](../../P08-access-venue-03/) | P08 · Access & Venue (3 of 3) | 5 | to draw |  |
| [`P08-setup-go-live-01`](../../P08-setup-go-live-01/) | P08 · Setup & Go-Live | 1 | to draw |  |
| [`P08-stock-supply-02`](../../P08-stock-supply-02/) | P08 · Stock & Supply (2 of 2) | 6 | to draw |  |
| [`P08-transport-01`](../../P08-transport-01/) | P08 · Transport | 7 | to draw |  |
| [`WS187`](../../WS187/) | Wallet Configuration Backend Structure v1.0 board 2 | 10 | to draw |  |
| [`P08-people-access-rights-02`](../../P08-people-access-rights-02/) | P08 · People & Access Rights (2 of 2) | 2 | to draw | 1 thin |
| [`WS32`](../../WS32/) | Order   Reservation Management board 2 | 9 | to draw | 1 thin |
| [`WS61`](../../WS61/) | Ticket Media   Credential Management board 3 | 10 | to draw | 1 thin |
| [`WS178`](../../WS178/) | TICVAI Finance Backend Structure Reference v1.0 board 1 | 1 | to draw | 1 thin |
| [`WS179`](../../WS179/) | TICVAI Finance Backend Structure Reference v1.0 board 2 | 1 | to draw | 1 thin |
| [`WS186`](../../WS186/) | Wallet Configuration Backend Structure v1.0 board 1 | 10 | to draw | 1 thin |
| [`WS189`](../../WS189/) | Wallet Configuration Backend Structure v1.0 board 4 | 10 | to draw | 1 thin |
| [`WS191`](../../WS191/) | Wallet Configuration Backend Structure v1.0 board 6 | 10 | to draw | 1 thin |
| [`WS192`](../../WS192/) | Wallet Configuration Backend Structure v1.0 board 7 | 10 | to draw | 1 thin |
| [`WS195`](../../WS195/) | Wallet Configuration Backend Structure v1.0 board 10 | 10 | to draw | 1 thin |
| [`WS29`](../../WS29/) | Membership   Annual Pass Management board 1 | 10 | to draw | 2 thin |
| [`WS30`](../../WS30/) | Membership   Annual Pass Management board 2 | 10 | to draw | 2 thin |
| [`WS33`](../../WS33/) | Order   Reservation Management board 3 | 10 | to draw | 2 thin |
| [`WS133`](../../WS133/) | Event Management Configuration Backend Structure v1.0 board 9 | 2 | to draw | 2 thin |
| [`WS190`](../../WS190/) | Wallet Configuration Backend Structure v1.0 board 5 | 10 | to draw | 2 thin |
| [`WS28`](../../WS28/) | Group Sales   Corporate Booking Management board 2 | 10 | to draw | 3 thin |
| [`WS31`](../../WS31/) | Order   Reservation Management board 1 | 10 | to draw | 3 thin |
| [`WS78`](../../WS78/) | Game and Ride board 1 | 10 | to draw | 3 thin |
| [`WS97`](../../WS97/) | Rental Management board 10 | 10 | to draw | 3 thin |
| [`WS126`](../../WS126/) | Event Management Configuration Backend Structure v1.0 board 2 | 3 | to draw | 3 thin |
| [`WS127`](../../WS127/) | Event Management Configuration Backend Structure v1.0 board 3 | 3 | to draw | 3 thin |
| [`WS128`](../../WS128/) | Event Management Configuration Backend Structure v1.0 board 4 | 3 | to draw | 3 thin |
| [`WS159`](../../WS159/) | Resource Management Configuration board 5 | 10 | to draw | 3 thin |
| [`WS160`](../../WS160/) | Resource Management Configuration board 6 | 10 | to draw | 3 thin |
| [`WS188`](../../WS188/) | Wallet Configuration Backend Structure v1.0 board 3 | 10 | to draw | 3 thin |
| [`WS193`](../../WS193/) | Wallet Configuration Backend Structure v1.0 board 8 | 10 | to draw | 3 thin |
| [`WS11`](../../WS11/) | Access Control board 11 | 10 | to draw | 4 thin |
| [`WS27`](../../WS27/) | Group Sales   Corporate Booking Management board 1 | 10 | to draw | 4 thin |
| [`WS79`](../../WS79/) | Game and Ride board 2 | 10 | to draw | 4 thin |
| [`WS129`](../../WS129/) | Event Management Configuration Backend Structure v1.0 board 5 | 4 | to draw | 4 thin |
| [`WS132`](../../WS132/) | Event Management Configuration Backend Structure v1.0 board 8 | 4 | to draw | 4 thin |
| [`WS164`](../../WS164/) | Resource Management Configuration board 10 | 10 | to draw | 4 thin |
| [`WS85`](../../WS85/) | Game and Ride board 8 | 9 | to draw | 5 thin |
| [`WS88`](../../WS88/) | Rental Management board 1 | 10 | to draw | 5 thin |
| [`WS90`](../../WS90/) | Rental Management board 3 | 10 | to draw | 5 thin |
| [`WS91`](../../WS91/) | Rental Management board 4 | 10 | to draw | 5 thin |
| [`WS92`](../../WS92/) | Rental Management board 5 | 10 | to draw | 5 thin |
| [`WS96`](../../WS96/) | Rental Management board 9 | 10 | to draw | 5 thin |
| [`WS158`](../../WS158/) | Resource Management Configuration board 4 | 10 | to draw | 5 thin |
| [`WS163`](../../WS163/) | Resource Management Configuration board 9 | 10 | to draw | 5 thin |
| [`WS194`](../../WS194/) | Wallet Configuration Backend Structure v1.0 board 9 | 10 | to draw | 5 thin |
| [`WS04`](../../WS04/) | Access Control board 4 | 10 | to draw | 6 thin |
| [`WS07`](../../WS07/) | Access Control board 7 | 10 | to draw | 6 thin |
| [`WS12`](../../WS12/) | Access Control board 12 | 10 | to draw | 6 thin |
| [`WS17`](../../WS17/) | Approval Workflows and Governance board 5 | 10 | to draw | 6 thin |
| [`WS80`](../../WS80/) | Game and Ride board 3 | 10 | to draw | 6 thin |
| [`WS83`](../../WS83/) | Game and Ride board 6 | 10 | to draw | 6 thin |
| [`WS89`](../../WS89/) | Rental Management board 2 | 10 | to draw | 6 thin |
| [`WS114`](../../WS114/) | ACCREDITATION board 7 | 10 | to draw | 6 thin |
| [`WS130`](../../WS130/) | Event Management Configuration Backend Structure v1.0 board 6 | 6 | to draw | 6 thin |
| [`WS134`](../../WS134/) | F&B Backend Structure Module Sample Reference v1.0 board 1 | 7 | to draw | 6 thin |
| [`WS167`](../../WS167/) | Seat Management Venue Mapping Reference v1.0 board 3 | 10 | to draw | 6 thin |
| [`WS168`](../../WS168/) | Seat Management Venue Mapping Reference v1.0 board 4 | 10 | to draw | 6 thin |
| [`WS175`](../../WS175/) | Seat Management Venue Mapping Reference v1.0 board 11 | 10 | to draw | 6 thin |
| [`WS09`](../../WS09/) | Access Control board 9 | 10 | to draw | 7 thin |
| [`WS81`](../../WS81/) | Game and Ride board 4 | 10 | to draw | 7 thin |
| [`WS84`](../../WS84/) | Game and Ride board 7 | 10 | to draw | 7 thin |
| [`WS86`](../../WS86/) | Game and Ride board 9 | 10 | to draw | 7 thin |
| [`WS87`](../../WS87/) | Game and Ride board 10 | 10 | to draw | 7 thin |
| [`WS105`](../../WS105/) | Subscription Licensing AI Self Service board 8 | 10 | to draw | 7 thin |
| [`WS113`](../../WS113/) | ACCREDITATION board 6 | 10 | to draw | 7 thin |
| [`WS115`](../../WS115/) | ACCREDITATION board 8 | 10 | to draw | 7 thin |
| [`WS142`](../../WS142/) | Marketing CRM Configuration Reference v1.0 board 8 | 10 | to draw | 7 thin |
| [`WS94`](../../WS94/) | Rental Management board 7 | 10 | to draw | 8 thin |
| [`WS104`](../../WS104/) | Subscription Licensing AI Self Service board 7 | 10 | to draw | 8 thin |
| [`WS110`](../../WS110/) | ACCREDITATION board 3 | 9 | to draw | 8 thin |
| [`WS112`](../../WS112/) | ACCREDITATION board 5 | 10 | to draw | 8 thin |
| [`WS135`](../../WS135/) | Marketing CRM Configuration Reference v1.0 board 1 | 10 | to draw | 8 thin |
| [`WS165`](../../WS165/) | Seat Management Venue Mapping Reference v1.0 board 1 | 10 | to draw | 8 thin |
| [`WS171`](../../WS171/) | Seat Management Venue Mapping Reference v1.0 board 7 | 10 | to draw | 8 thin |
| [`WS173`](../../WS173/) | Seat Management Venue Mapping Reference v1.0 board 9 | 10 | to draw | 8 thin |
| [`WS174`](../../WS174/) | Seat Management Venue Mapping Reference v1.0 board 10 | 8 | to draw | 8 thin |
| [`WS177`](../../WS177/) | Seat Management Venue Mapping Reference v1.0 board 13 | 10 | to draw | 8 thin |
| [`WS13`](../../WS13/) | Approval Workflows and Governance board 1 | 10 | to draw | 9 thin |
| [`WS16`](../../WS16/) | Approval Workflows and Governance board 4 | 10 | to draw | 9 thin |
| [`WS93`](../../WS93/) | Rental Management board 6 | 10 | to draw | 9 thin |
| [`WS95`](../../WS95/) | Rental Management board 8 | 10 | to draw | 9 thin |
| [`WS109`](../../WS109/) | ACCREDITATION board 2 | 10 | to draw | 9 thin |
| [`WS111`](../../WS111/) | ACCREDITATION board 4 | 9 | to draw | 9 thin |
| [`WS141`](../../WS141/) | Marketing CRM Configuration Reference v1.0 board 7 | 10 | to draw | 9 thin |
| [`WS172`](../../WS172/) | Seat Management Venue Mapping Reference v1.0 board 8 | 10 | to draw | 9 thin |
| [`WS176`](../../WS176/) | Seat Management Venue Mapping Reference v1.0 board 12 | 10 | to draw | 9 thin |
| [`WS136`](../../WS136/) | Marketing CRM Configuration Reference v1.0 board 2 | 10 | to draw | 10 thin |
| [`WS139`](../../WS139/) | Marketing CRM Configuration Reference v1.0 board 5 | 10 | to draw | 10 thin |
| [`WS143`](../../WS143/) | Marketing CRM Configuration Reference v1.0 board 9 | 10 | to draw | 10 thin |
| [`WS146`](../../WS146/) | Marketing CRM Configuration Reference v1.0 board 12 | 10 | to draw | 10 thin |
| [`WS166`](../../WS166/) | Seat Management Venue Mapping Reference v1.0 board 2 | 10 | to draw | 10 thin |
| [`WS169`](../../WS169/) | Seat Management Venue Mapping Reference v1.0 board 5 | 10 | to draw | 10 thin |
| [`WS170`](../../WS170/) | Seat Management Venue Mapping Reference v1.0 board 6 | 10 | to draw | 10 thin |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, web. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P13: TICVAI Venue Management, CMS section

**What it is.** The white-label CMS. The venue builds and publishes its website and app: brand, pages, booking flows, the mobile app and store publishing.

**Who uses it.** The venue's marketing or digital team, and TICVAI's set-up team on day one.

### Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html`: the look of the controls: every configuration control, laid out and explained.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the configuration side panel, for the controls, and the guest booking the live preview shows.
- `sources/designs/TICVAI_White_Label_Guest_App_UI_Reference_1.pdf`: the client's White Label Builder boards.

Open the file and match it. Do not describe it in words.

### Where it stands

- **103 screens.** 25 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

**Start with the flow builder** (`../../CMS-FLOW-BUILDER/`): CMS-101 Help me choose and the new CMS-102 Site Builder, CMS-103 Booking Flows and CMS-104 App Build & Store Publishing, drawn as one flow.

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P13-white-label-03`](../../P13-white-label-03/) | P13 · White Label (3 of 3) | 3 | to draw | 3 Block A; new: CMS-102, CMS-103, CMS-104 |
| [`P13-white-label-01`](../../P13-white-label-01/) | P13 · White Label (1 of 3) | 10 | to draw | 10 Block A; changed: CMS-001, CMS-004, CMS-005, CMS-007, CMS-008, CMS-009, CMS-010; 1 thin |
| [`P13-white-label-02`](../../P13-white-label-02/) | P13 · White Label (2 of 3) | 10 | to draw | 10 Block A; changed: CMS-014, CMS-016, CMS-101; 2 thin |
| [`WS41`](../../WS41/) | Privacy  Consent   Preference Management board 1 | 10 | to draw | 2 Block A; changed: CMS-025, CMS-026; 3 thin |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`WS72`](../../WS72/) | Waiver, Consent & Digital Form Management board 1 | 10 | to draw | 2 thin |
| [`WS42`](../../WS42/) | Privacy  Consent   Preference Management board 2 | 10 | to draw | 3 thin |
| [`WS74`](../../WS74/) | Digital Asset Management DAM board 1 | 10 | to draw | 3 thin |
| [`WS75`](../../WS75/) | Digital Asset Management DAM board 2 | 10 | to draw | 3 thin |
| [`WS77`](../../WS77/) | Digital Asset Management DAM board 4 | 10 | to draw | 3 thin |
| [`WS73`](../../WS73/) | Waiver, Consent & Digital Form Management board 2 | 10 | to draw | 4 thin |
| [`WS76`](../../WS76/) | Digital Asset Management DAM board 3 | 10 | to draw | 6 thin |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, CMS section. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html` and `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of the guest site or app on the right where a screen changes what guests see. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P16: TICVAI Venue Management, analytics section

**What it is.** Venue analytics. Dashboards and reports across sales, visits, food and retail, with AI explanations.

**Who uses it.** Venue managers and analysts, on a desktop.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

### Where it stands

- **70 screens.** 4 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

ANL-071 is new on 29 September (batch P16-analytics-02).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`WS66`](../../WS66/) | Unified BI Reporting and AI Analytics Platform board 1 | 9 | to draw | 1 Block A; changed: ANL-019; 2 thin |
| [`WS71`](../../WS71/) | Unified BI Reporting and AI Analytics Platform board 10 | 10 | to draw | 1 Block A; 4 thin |
| [`WS67`](../../WS67/) | Unified BI Reporting and AI Analytics Platform board 2 | 10 | to draw | 2 Block A; 5 thin |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P16-analytics-01`](../../P16-analytics-01/) | P16 · Analytics (1 of 2) | 10 | to draw |  |
| [`P16-analytics-02`](../../P16-analytics-02/) | P16 · Analytics (2 of 2) | 1 | to draw | new: ANL-071 |
| [`WS69`](../../WS69/) | Unified BI Reporting and AI Analytics Platform board 4 | 10 | to draw | 4 thin |
| [`WS68`](../../WS68/) | Unified BI Reporting and AI Analytics Platform board 3 | 10 | to draw | 6 thin |
| [`WS70`](../../WS70/) | Unified BI Reporting and AI Analytics Platform board 9 | 10 | to draw | 7 thin |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, analytics section. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P12: TICVAI Venue Management, support section

**What it is.** The support agent console. Conversations, the knowledge base and agent availability.

**Who uses it.** Venue support agents, on a desktop, often handling several chats at once.

### Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for operator density.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

### Where it stands

- **28 screens.** 1 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P12-overview-01`](../../P12-overview-01/) | P12 · Overview | 2 | to draw | 1 Block A |

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P12-access-availability-01`](../../P12-access-availability-01/) | P12 · Access & Availability | 2 | to draw |  |
| [`P12-conversations-01`](../../P12-conversations-01/) | P12 · Conversations | 2 | to draw |  |
| [`P12-knowledge-responses-01`](../../P12-knowledge-responses-01/) | P12 · Knowledge & Responses | 2 | to draw | 1 thin |
| [`WS25`](../../WS25/) | Customer Service board 1 | 10 | to draw | 3 thin |
| [`WS26`](../../WS26/) | Customer Service board 2 | 10 | to draw | 4 thin |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, support section. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.

## P11: TICVAI Control, accreditation web

**What it is.** The public accreditation portal. Media, staff and suppliers apply for event credentials; reviewers decide.

**Who uses it.** Applicants from outside (public) and TICVAI or venue reviewers.

### Reference design to match

- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the newest client-approved public look, for forms and finish.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for the reviewer screens' density.

Open the file and match it. Do not describe it in words.

### Where it stands

- **8 screens.** 0 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

### Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

#### After Block A

| batch | label | screens | status | notes |
|---|---|---|---|---|
| [`P11-applicant-journey-01`](../../P11-applicant-journey-01/) | P11 · Applicant Journey | 5 | to draw |  |
| [`P11-reviewer-internal-01`](../../P11-reviewer-internal-01/) | P11 · Reviewer (Internal) | 3 | to draw |  |

### The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Control, accreditation web. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html` and `sources/designs/TICVAI_POS_Terminal_client_approved.html`. This is a public web form flow, 1440 desktop and 390 phone widths; reviewer screens as a desktop back office. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

### When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
