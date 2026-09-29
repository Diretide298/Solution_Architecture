# P08: TICVAI Venue Management, web

**What it is.** The venue's back office. Set up products, prices, access, staff, stock and outlets, and see what happened.

**Who uses it.** Venue managers, finance, operations and set-up staff, on a desktop.

## Reference design to match

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

Open the file and match it. Do not describe it in words.

## Where it stands

- **1186 screens.** 66 are Block A (the first 35 days of the build, from Monday 5 October).
- **0 have a frame; 0 of those are client-verified** (a capture of the client-approved prototype).

See `../../VENUE-MANAGEMENT.md` for how a batch session runs. **Block A needs the set-up screens first**: the Venue Home hub and the screens a venue fills in before it can sell.

## Batches, in the order to run them

Block A first: batches with a new or changed screen, then the rest of Block A. Then the rest, cheapest first (the manifest order: fully specified before thin).

### Block A

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

### After Block A

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

## The prompt

Paste this into the Claude Design session with the batch folder and the reference file linked. Fill in the batch id.

```
Build batch <BATCH ID> of TICVAI Venue Management, web. Read BRIEF.md in the batch folder first, then BUNDLE.md (screens, operations, schemas, permissions); BRIEF.md outranks this prompt. Match the look of `sources/designs/TICVAI_POS_Terminal_client_approved.html` and `sources/designs/TICVAI_Mobile.dc.html`. This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. Save one fragment per screen to wireframes/incoming/<BATCH ID>/<screen id>.html (lower-case id, root element id="<screen id>", no <html>, <head>, <body> or <script>, over 200 bytes), then one working file, return/<BATCH ID>.dc.html, where every screen opens from #<screen id> in its main populated state and every declared state opens from #<screen id>?state=<state>. Seed realistic UAE data from schemas.json (AED, venues, staff names), never lorem ipsum. Gate every control that needs a permission. Never show an operation id, field name, permission key or screen id as text. If a screen needs something the bundle does not have, draw it greyed with a short note and list it in return/FINDINGS.md; never invent an endpoint.
```

## When it comes back

```bash
python tools/import-design-frames.py <BATCH ID> wireframes/incoming/<BATCH ID> --apply
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

The standing overnight prompt and the importer's rules are in `docs/active/claude-design-runbook.md`.
