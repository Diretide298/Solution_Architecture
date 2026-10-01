# WS190 — Wallet Configuration Backend Structure v1.0 board 5

**10 screens · 10 operations · 8 schemas · 3 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
true. **None of it is the subject.** The subject is the person in front of the screen and the one
thing they came to do.

## What to build

**A working surface, not a drawing of one.** Two references, both built from these same sources:

- `sources/designs/TICVAI_Mobile.dc.html` — 54 screens in one navigable file, 133 animations,
  a live seat map, a five-stage payment flow. **This is the bar for finish.**
- `sources/designs/TICVAI_POS_Terminal_client_approved.html` — the client-approved POS build. **This is the bar for operator density.**

`sources/designs/ticvai-motion-and-interaction.md` names every mechanism in them. Open them and
match their depth. Do not describe them, read them.

## The one rule that outranks the rest

**Nothing in this bundle may appear as text a user can read.** Not an operation id, not a schema
field name, not a permission key, not a screen id, not a file path, not a finding reference.

A homepage that prints `getTenantAppStatus → listProducts` under its header, or labels a column
`venueId · scopePath`, has published its own homework. It happened on `WEB-001`: four products on
sale and not a single price on the page, because the build rendered what `listProducts` returns
instead of what a guest wants — a photo, a name, a price, and a way to book.

**The test: would the person this screen is for understand every word on it?** If a line would
confuse them, it is spec leakage, not design. `bindsTo` tells you what data to invent
convincingly. It is never a caption.

## What is in this folder

| file | what it is |
|---|---|
| `BUNDLE.md` | **The one file to hand a design session.** This brief; then **Screen by screen**, a full specification of each screen (what the user enters and picks, what it shows and produces, every state, who may do what, the requirements it meets, what the client said about it in the meetings, the tracker items, what the tenant configures, the references and an acceptance checklist); then what applies to the whole batch; then the raw data. |
| `screens.json` | Every field of every screen in the batch, as the package holds it. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-1123` | Gift Card & Digital Benefit Command Center | B–D | 0 | 48 | 6 | 2 | 0 | 6 | — | notStarted (—) |
| `BO-1124` | Gift Card Product Configuration | B–D | 0 | 50 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1125` | Gift Card Issuance, Activation & Distribution | B–D | 12 | 0 | 6 | 1 | 0 | 6 | — | notStarted (—) |
| `BO-1126` | Voucher & Coupon Type Configuration | B–D | 22 | 0 | 6 | 0 | 2 | 2 | — | notStarted (—) |
| `BO-1127` | Voucher Eligibility & Redemption Rule Studio | B–D | 30 | 0 | 6 | 0 | 2 | 2 | — | notStarted (—) |
| `BO-1128` | Membership Benefits & Entitlement Mapping | B–D | 22 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1129` | Benefit Packaging & Digital Wallet Presentation | B–D | 21 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1130` | Gift Card & Voucher Expiry Management | B–D | 10 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1131` | Gift Card Balance, Liability & Breakage Control | B–D | 0 | 20 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1132` | Gift Card & Voucher Simulator, Validation & Publication | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-1131, BO-1132 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1123` Gift Card & Digital Benefit Command Center

**Provide administrators with a consolidated operational view of gift cards, vouchers and digital benefits across all tenants and venues. Dashboard KPIs**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/orders-money/gift-card-digital-benefit-command-center-bo-1123` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every gift card digital** (data table)

| Shows | Format | Notes |
|---|---|---|
| Active gift cards | text | not in the schema: `Active Gift Cards` |
| Outstanding gift card value | text | not in the schema: `Outstanding Gift Card Value` |
| Gift cards sold | text | not in the schema: `Gift Cards Sold` |
| Gift cards redeemed | text | not in the schema: `Gift Cards Redeemed` |
| Partial balances | text | not in the schema: `Partial Balances` |
| Expiring gift cards | text | not in the schema: `Expiring Gift Cards` |
| Active vouchers | text | not in the schema: `Active Vouchers` |
| Vouchers redeemed | text | not in the schema: `Vouchers Redeemed` |
| Expiring vouchers | text | not in the schema: `Expiring Vouchers` |
| Membership benefits issued | text | not in the schema: `Membership Benefits Issued` |
| Membership benefits redeemed | text | not in the schema: `Membership Benefits Redeemed` |
| Promotional credits outstanding | text | not in the schema: `Promotional Credits Outstanding` |
| Breakdown by | text | not in the schema: `Breakdown By` |
| Gift card type | text | not in the schema: `Gift card type` |
| Voucher type | text | not in the schema: `Voucher type` |
| Benefit type | text | not in the schema: `Benefit type` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Channel | text | not in the schema: `Channel` |
| Campaign | text | not in the schema: `Campaign` |
| Membership tier | text | not in the schema: `Membership tier` |
| Status | text | not in the schema: `Status` |
| Operational alerts | text | not in the schema: `Operational Alerts` |

**The selected gift card digital** (detail panel): The pack groups this record's detail under its own headings: “Highlight”.

| Shows | Format | Notes |
|---|---|---|
| Active gift cards | text | not in the schema: `Active Gift Cards` |
| Outstanding gift card value | text | not in the schema: `Outstanding Gift Card Value` |
| Gift cards sold | text | not in the schema: `Gift Cards Sold` |
| Gift cards redeemed | text | not in the schema: `Gift Cards Redeemed` |
| Partial balances | text | not in the schema: `Partial Balances` |
| Expiring gift cards | text | not in the schema: `Expiring Gift Cards` |
| Active vouchers | text | not in the schema: `Active Vouchers` |
| Vouchers redeemed | text | not in the schema: `Vouchers Redeemed` |
| Expiring vouchers | text | not in the schema: `Expiring Vouchers` |
| Membership benefits issued | text | not in the schema: `Membership Benefits Issued` |
| Membership benefits redeemed | text | not in the schema: `Membership Benefits Redeemed` |
| Promotional credits outstanding | text | not in the schema: `Promotional Credits Outstanding` |
| Breakdown by | text | not in the schema: `Breakdown By` |
| Gift card type | text | not in the schema: `Gift card type` |
| Voucher type | text | not in the schema: `Voucher type` |
| Benefit type | text | not in the schema: `Benefit type` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Channel | text | not in the schema: `Channel` |
| Campaign | text | not in the schema: `Campaign` |
| Membership tier | text | not in the schema: `Membership tier` |
| Status | text | not in the schema: `Status` |
| Operational alerts | text | not in the schema: `Operational Alerts` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create Gift Card (primary button) | navigation or local | — | — | — | — |
| Create Voucher (secondary button) | navigation or local | — | — | — | — |
| Create Benefit (secondary button) | navigation or local | — | — | — | — |
| Issue Value (secondary button) | navigation or local | — | — | — | — |
| Search Instrument (secondary button) | navigation or local | — | — | — | — |
| Check Balance (secondary button) | navigation or local | — | — | — | — |
| Investigate Redemption (secondary button) | navigation or local | — | — | — | — |
| View Liability (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getWalletLiability` (onLoad, Gift card liability)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1124` Gift Card Product Configuration: *Gift Card Product Configuration*
- → `BO-1125` Gift Card Issuance, Activation & Distribution: *Gift Card Issuance, Activation & Distribution*
- → `BO-1126` Voucher & Coupon Type Configuration: *Voucher & Coupon Type Configuration*
- → `BO-1127` Voucher Eligibility & Redemption Rule Studio: *Voucher Eligibility & Redemption Rule Studio*
- → `BO-1128` Membership Benefits & Entitlement Mapping: *Membership Benefits & Entitlement Mapping*
- → `BO-1129` Benefit Packaging & Digital Wallet Presentation: *Benefit Packaging & Digital Wallet Presentation*
- → `BO-1130` Gift Card & Voucher Expiry Management: *Gift Card & Voucher Expiry Management*
- → `BO-1131` Gift Card Balance, Liability & Breakage Control: *Gift Card Balance, Liability & Breakage Control*
- → `BO-1132` Gift Card & Voucher Simulator, Validation & Publication: *Gift Card & Voucher Simulator, Validation & Publication*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift card digital list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift card digital untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gift card digital yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gift card digital are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Card already activated, or the code is unknown |

#### Permissions

- `getWalletLiability` → `WALLET_VIEW` (read) · staff
- `setGiftCardProduct` → `WALLET_CONFIGURE` (configure) · staff
- `createVoucherType` → `WALLET_CONFIGURE` (configure) · staff
- `issueGiftCard` → `WALLET_OPERATE` (operate) · staff
- `getGiftCard` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.35 | Website should have the ability to purchase Gift Vouchers such as Money card where the customer will be able to load money on their wallet using their credit card. Customer should be able to use … | Ticketing Sales | CONTRACTED | `issueGiftCard` |
| 19.2.40 | Gift Card Wallet - System shall support gift card storage. | Guest Mobile App & Branding | CONTRACTED | `getGiftCard` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1123` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1123`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 1: Opens Gift Card & Digital Benefit Command Center → Provide administrators with a consolidated operational view of gift cards, vouchers and digital benefits across all tenants and venues. Dashboard KPIs
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F297 branch at step 1 (expected): when Nothing has been set up on Gift Card & Digital Benefit Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F297 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 412).
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1123?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create Gift Card, Create Voucher, Create Benefit, Issue Value, Search Instrument, Check Balance, Investigate Redemption, View Liability.
- [ ] Every transition is wired: `BO-100`, `BO-1124`, `BO-1125`, `BO-1126`, `BO-1127`, `BO-1128`, `BO-1129`, `BO-1130`, `BO-1131`, `BO-1132`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1124` Gift Card Product Configuration

**Create reusable gift-card products that can be sold or issued across TICVAI. The source specifically requires gift-card balances including activation, redemption, partial usage, expiry, balance inquiry and transaction history. Gift Card Types**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§For each gift card define) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/gift-card-product-configuration-bo-1124` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every gift card product** (data table)

| Shows | Format | Notes |
|---|---|---|
| Product name | text | not in the schema: `Product name` |
| Internal code | text | not in the schema: `Internal code` |
| Description | text | not in the schema: `Description` |
| Fixed / variable value | text | not in the schema: `Fixed / variable value` |
| Minimum value | text | not in the schema: `Minimum value` |
| Maximum value | text | not in the schema: `Maximum value` |
| Currency | text | not in the schema: `Currency` |
| Reloadable | text | not in the schema: `Reloadable` |
| Partial redemption allowed | text | not in the schema: `Partial redemption allowed` |
| Multiple redemption allowed | text | not in the schema: `Multiple redemption allowed` |
| Transferable | text | not in the schema: `Transferable` |
| Refundable | text | not in the schema: `Refundable` |
| Cash out permitted | text | not in the schema: `Cash-out permitted` |
| Expiry policy | text | not in the schema: `Expiry policy` |
| Applicable tenant | text | not in the schema: `Applicable tenant` |
| Applicable venues | text | not in the schema: `Applicable venues` |
| Applicable channels | text | not in the schema: `Applicable channels` |
| Applicable products | text | not in the schema: `Applicable products` |
| Activation method | text | not in the schema: `Activation method` |
| Wallet storage allowed | text | not in the schema: `Wallet storage allowed` |
| Customer registration required | text | not in the schema: `Customer registration required` |
| Gift recipient details required | text | not in the schema: `Gift recipient details required` |
| Effective dates | text | not in the schema: `Effective dates` |
| Status | text | not in the schema: `Status` |
| Lifecycle | text | not in the schema: `Lifecycle` |

**The selected gift card product** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Product name | text | not in the schema: `Product name` |
| Internal code | text | not in the schema: `Internal code` |
| Description | text | not in the schema: `Description` |
| Fixed / variable value | text | not in the schema: `Fixed / variable value` |
| Minimum value | text | not in the schema: `Minimum value` |
| Maximum value | text | not in the schema: `Maximum value` |
| Currency | text | not in the schema: `Currency` |
| Reloadable | text | not in the schema: `Reloadable` |
| Partial redemption allowed | text | not in the schema: `Partial redemption allowed` |
| Multiple redemption allowed | text | not in the schema: `Multiple redemption allowed` |
| Transferable | text | not in the schema: `Transferable` |
| Refundable | text | not in the schema: `Refundable` |
| Cash out permitted | text | not in the schema: `Cash-out permitted` |
| Expiry policy | text | not in the schema: `Expiry policy` |
| Applicable tenant | text | not in the schema: `Applicable tenant` |
| Applicable venues | text | not in the schema: `Applicable venues` |
| Applicable channels | text | not in the schema: `Applicable channels` |
| Applicable products | text | not in the schema: `Applicable products` |
| Activation method | text | not in the schema: `Activation method` |
| Wallet storage allowed | text | not in the schema: `Wallet storage allowed` |
| Customer registration required | text | not in the schema: `Customer registration required` |
| Gift recipient details required | text | not in the schema: `Gift recipient details required` |
| Effective dates | text | not in the schema: `Effective dates` |
| Status | text | not in the schema: `Status` |
| Lifecycle | text | not in the schema: `Lifecycle` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fixed Value (primary button) | navigation or local | — | — | — | — |
| Variable Value (secondary button) | navigation or local | — | — | — | — |
| Promotional Gift Card (secondary button) | navigation or local | — | — | — | — |
| Corporate Gift Card (secondary button) | navigation or local | — | — | — | — |
| Digital Gift Card (secondary button) | navigation or local | — | — | — | — |
| Physical Gift Card (secondary button) | navigation or local | — | — | — | — |
| Event Gift Card (secondary button) | navigation or local | — | — | — | — |
| Venue Gift Card (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1123` Gift Card & Digital Benefit Command Center: *Back to Gift Card & Digital Benefit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift card product list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift card product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gift card product yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gift card product are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGiftCardProduct` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A120** Build the product creation wizard with four paths (from scratch · save as reusable template · clone · file upload using a standard tenant data-collection template) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'product creation wizard')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker · keyword 'ticket type')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1124` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1124`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 2: Works in Gift Card Product Configuration → Create reusable gift-card products that can be sold or issued across TICVAI. The source specifically requires gift-card balances including activation, redemption, partial usage, expiry, balance …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (50 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1124?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fixed Value, Variable Value, Promotional Gift Card, Corporate Gift Card, Digital Gift Card, Physical Gift Card, Event Gift Card, Venue Gift Card.
- [ ] Every transition is wired: `BO-1123`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1125` Gift Card Issuance, Activation & Distribution

**Configure how gift cards are created, sold, activated and delivered. Issuance Sources B2C Website Mobile App POS Kiosk Customer Service Corporate Portal B2B/Reseller Campaign Administrative issuance API Activation Methods Activate on sale Activate on payment confirmation Manual activation Scheduled activation API activation Bulk activation Distribution**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_OPERATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `giftCardId` (navigation) |
| Route | `/orders-money/gift-card-issuance-activation-distribution-bo-1125` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Card number format | select field | — | — | — | — | — | — |
| PIN/security code | select field | — | — | — | — | — | — |
| Activation trigger | select field | — | — | — | — | — | — |
| Recipient | select field | — | — | — | — | — | — |
| Sender | select field | — | — | — | — | — | — |
| Personal message | select field | — | — | — | — | — | — |
| Delivery date | select field | — | — | — | — | — | — |
| Delivery channel | select field | — | — | — | — | — | — |
| Activation validity | select field | — | — | — | — | — | — |
| Resend rules | select field | — | — | — | — | — | — |
| Replacement rules | select field | — | — | — | — | — | — |
| Corporate Bulk Issuance | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Digital delivery (primary button) | navigation or local | — | — | — | — |
| Physical card (secondary button) | navigation or local | — | — | — | — |
| RFID/NFC card (secondary button) | navigation or local | — | — | — | — |
| Wallet (secondary button) | navigation or local | — | — | — | — |
| Printable voucher (secondary button) | navigation or local | — | — | — | — |
| Distribution (secondary button) | navigation or local | — | — | — | — |
| Expiry (secondary button) | navigation or local | — | — | — | — |
| Cost center (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1123` Gift Card & Digital Benefit Command Center: *Back to Gift Card & Digital Benefit Command Center*; carries `cardCode`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift card issuance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift card issuance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gift card issuance configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Card already activated, or the code is unknown; 409 The card cannot be spent, or cannot cover the amount. Only an `active` or `partiallyRedeemed` card is spent against; a card not yet activated, blocked, expired … (GiftCardProblem); 409 The card is fully redeemed or expired. Activation moves an `issued` card, or a `blocked` one that was found, to `active`; it does not revive a card whose … |

#### Permissions

- `issueGiftCard` → `WALLET_OPERATE` (operate) · staff
- `activateGiftCard` → `WALLET_OPERATE` (operate) · staff
- `redeemGiftCard` → `WALLET_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.35 | Website should have the ability to purchase Gift Vouchers such as Money card where the customer will be able to load money on their wallet using their credit card. Customer should be able to use … | Ticketing Sales | CONTRACTED | `issueGiftCard` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1125` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1125`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 4: Works in Gift Card Issuance, Activation & Distribution → Configure how gift cards are created, sold, activated and delivered. Issuance Sources B2C Website Mobile App POS Kiosk Customer Service Corporate Portal B2B/Reseller Campaign Administrative issuance …

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1125?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, Digital delivery, Physical card, RFID/NFC card, Wallet, Printable voucher, Distribution, Expiry, Cost center.
- [ ] Every transition is wired: `BO-1123`.
- [ ] Every gated control is gated: `WALLET_OPERATE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1126` Voucher & Coupon Type Configuration

**Create and manage digital vouchers and non-cash redemption instruments. The source requires the wallet to store and manage digital vouchers, coupons, meal vouchers, parking vouchers, attraction credits and campaign rewards. Voucher Types Monetary Voucher Percentage Voucher Complimentary Ticket Meal Voucher F&B Voucher Retail Voucher Parking Voucher Attraction Voucher Ride Voucher Rental Voucher Upgrade Voucher Campaign Reward Service Recovery Voucher Custom Voucher**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE`, `WALLET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/voucher-coupon-type-configuration-bo-1126` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Voucher name | select field | — | — | — | — | — | — |
| Voucher code | select field | — | — | — | — | — | — |
| Voucher category | select field | — | — | — | — | — | — |
| Monetary/non-monetary | select field | — | — | — | — | — | — |
| Fixed value | select field | — | — | — | — | — | — |
| Percentage value | select field | — | — | — | — | — | — |
| Quantity entitlement | select field | — | — | — | — | — | — |
| Applicable products | select field | — | — | — | — | — | — |
| Applicable categories | select field | — | — | — | — | — | — |
| Applicable venues | select field | — | — | — | — | — | — |
| Applicable channels | select field | — | — | — | — | — | — |
| Minimum spend | select field | — | — | — | — | — | — |
| Maximum benefit | select field | — | — | — | — | — | — |
| Validity | select field | — | — | — | — | — | — |
| Single-use/multi-use | select field | — | — | — | — | — | — |
| Partial redemption | select field | — | — | — | — | — | — |
| Stackable | select field | — | — | — | — | — | — |
| Transferable | select field | — | — | — | — | — | — |
| Customer-specific | select field | — | — | — | — | — | — |
| Wallet storage | select field | — | — | — | — | — | — |
| Barcode / QR | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listVoucherTypes` (onLoad, Voucher and coupon types)

**Where the user goes next**

- → `BO-1123` Gift Card & Digital Benefit Command Center: *Back to Gift Card & Digital Benefit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The voucher coupon type configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the voucher coupon type untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No voucher coupon type configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listVoucherTypes` → `WALLET_VIEW` (read) · staff
- `createVoucherType` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)*
- Coupons as one shared promo code (e.g. for social media) or a batch of unique single-use codes, with configurable reuse rules. *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-173)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1126` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1126`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 6: Works in Voucher & Coupon Type Configuration → Create and manage digital vouchers and non-cash redemption instruments. The source requires the wallet to store and manage digital vouchers, coupons, meal vouchers, parking vouchers, attraction …

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1126?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1123`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1127` Voucher Eligibility & Redemption Rule Studio

**Define precisely when, where and by whom a voucher may be redeemed. Eligibility Rules**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/voucher-eligibility-redemption-rule-studio-bo-1127` |

**Known gaps.** **Voucher Eligibility & Redemption Rule Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer | select field | — | — | — | — | — | — |
| Customer segment | select field | — | — | — | — | — | — |
| Membership tier | select field | — | — | — | — | — | — |
| Age | select field | — | — | — | — | — | — |
| Family role | select field | — | — | — | — | — | — |
| Corporate account | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Ticket | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Ride | select field | — | — | — | — | — | — |
| F&B | select field | — | — | — | — | — | — |
| Retail | select field | — | — | — | — | — | — |
| Rental | select field | — | — | — | — | — | — |
| Parking | select field | — | — | — | — | — | — |
| Add-on | select field | — | — | — | — | — | — |
| Location | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Outlet | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| B2C | select field | — | — | — | — | — | — |
| Mobile App | select field | — | — | — | — | — | — |
| Kiosk | select field | — | — | — | — | — | — |
| API | select field | — | — | — | — | — | — |
| Time | select field | — | — | — | — | — | — |
| Valid dates | select field | — | — | — | — | — | — |
| Days of week | select field | — | — | — | — | — | — |
| Time window | select field | — | — | — | — | — | — |
| Season | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1123` Gift Card & Digital Benefit Command Center: *Back to Gift Card & Digital Benefit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The voucher eligibility redemption configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the voucher eligibility redemption untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No voucher eligibility redemption configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createVoucherType` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)*
- Partial vs full redemption is configurable per wallet/gift-card type: some allow spending part and keeping the remainder, others require full redemption in a single transaction. *(agreed · MoM 27 Aug 2026, 4.7 Split-Tender, Redemption Rules & Configuration Simulation · DI-526)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1127` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1127`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 8: Works in Voucher Eligibility & Redemption Rule Studio → Define precisely when, where and by whom a voucher may be redeemed. Eligibility Rules

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1127?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1123`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1128` Membership Benefits & Entitlement Mapping

**Connect Membership & Loyalty benefits into the Wallet without making Wallet responsible for membership logic. Requirement 4.3.25 requires membership-related benefits, credits, entitlements, guest passes, reservation quotas and included benefits to be available within the guest wallet. Membership Benefit Examples Gold Membership → AED 200 F&B Credit → 5 Guest Passes → 2 Parking Credits → 3 Complimentary Ride Credits → 1 Birthday Voucher Configure Mapping Membership Product → Membership Tier → Benefit Type → Wallet Credit/Voucher/Entitlement**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/membership-benefits-entitlement-mapping-bo-1128` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Membership tier | select field | — | — | — | — | — | — |
| Benefit | select field | — | — | — | — | — | — |
| Quantity/value | select field | — | — | — | — | — | — |
| Issuance timing | select field | — | — | — | — | — | — |
| Renewal behavior | select field | — | — | — | — | — | — |
| Validity | select field | — | — | — | — | — | — |
| Usage frequency | select field | — | — | — | — | — | — |
| Applicable venue | select field | — | — | — | — | — | — |
| Applicable product | select field | — | — | — | — | — | — |
| Carry-forward | select field | — | — | — | — | — | — |
| Transferability | select field | — | — | — | — | — | — |
| Family sharing | select field | — | — | — | — | — | — |
| Replacement rules | select field | — | — | — | — | — | — |
| Issuance Triggers | select field | — | — | — | — | — | — |
| Membership activation | select field | — | — | — | — | — | — |
| Membership renewal | select field | — | — | — | — | — | — |
| Tier upgrade | select field | — | — | — | — | — | — |
| Anniversary | select field | — | — | — | — | — | — |
| Birthday | select field | — | — | — | — | — | — |
| Visit milestone | select field | — | — | — | — | — | — |
| Campaign | select field | — | — | — | — | — | — |
| Manual award | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listVoucherTypes` (onLoad, Benefits mapped to memberships)

**Where the user goes next**

- → `BO-1123` Gift Card & Digital Benefit Command Center: *Back to Gift Card & Digital Benefit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership benefits entitlement configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership benefits entitlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership benefits entitlement configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listVoucherTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1128` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1128`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 10: Works in Membership Benefits & Entitlement Mapping → Connect Membership & Loyalty benefits into the Wallet without making Wallet responsible for membership logic. Requirement 4.3.25 requires membership-related benefits, credits, entitlements, guest …

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1128?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1123`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1129` Benefit Packaging & Digital Wallet Presentation

**Configure how different instruments appear to customers in B2C and mobile wallet experiences. Wallet Sections Administrators can define presentation categories: Money Cash Balance Refund Credit Gift Cards Gift Card Balance Vouchers Meal Voucher Parking Voucher Attraction Voucher Membership Guest Passes Complimentary Tickets Member Credits Rewards Promotional Credits Campaign Rewards**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure states) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/benefit-packaging-digital-wallet-presentation-bo-1129` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Display name | select field | — | — | — | — | — | — |
| Customer description | select field | — | — | — | — | — | — |
| Icon | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Balance visibility | select field | — | — | — | — | — | — |
| Expiry visibility | select field | — | — | — | — | — | — |
| Terms link | select field | — | — | — | — | — | — |
| QR visibility | select field | — | — | — | — | — | — |
| Barcode visibility | select field | — | — | — | — | — | — |
| Redeem button | select field | — | — | — | — | — | — |
| Transfer button | select field | — | — | — | — | — | — |
| Gift button | select field | — | — | — | — | — | — |
| Applicable channels | select field | — | — | — | — | — | — |
| Display priority | select field | — | — | — | — | — | — |
| Available | select field | — | — | — | — | — | — |
| Reserved | select field | — | — | — | — | — | — |
| Partially Used | select field | — | — | — | — | — | — |
| Used | select field | — | — | — | — | — | — |
| Expiring Soon | select field | — | — | — | — | — | — |
| Expired | select field | — | — | — | — | — | — |
| Suspended | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listVoucherTypes` (onLoad, How benefits are presented)

**Where the user goes next**

- → `BO-1123` Gift Card & Digital Benefit Command Center: *Back to Gift Card & Digital Benefit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The benefit packaging digital configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the benefit packaging digital untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No benefit packaging digital configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listVoucherTypes` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1129` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1129`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 12: Works in Benefit Packaging & Digital Wallet Presentation → Configure how different instruments appear to customers in B2C and mobile wallet experiences. Wallet Sections Administrators can define presentation categories: Money Cash Balance Refund Credit Gift …

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1129?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1123`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1130` Gift Card & Voucher Expiry Management

**Control validity, expiration, extension and customer notification. Expiry Models Never expires Fixed date X days after purchase X days after activation X days after issuance End of campaign End of event Membership expiry**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_OPERATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/gift-card-voucher-expiry-management-bo-1130` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Valid-from | select field | — | — | — | — | — | — |
| Valid-until | select field | — | — | — | — | — | — |
| Grace period | select field | — | — | — | — | — | — |
| Extension allowed | select field | — | — | — | — | — | — |
| Maximum extension | select field | — | — | — | — | — | — |
| Manual extension | select field | — | — | — | — | — | — |
| Renewal | select field | — | — | — | — | — | — |
| Remaining-balance behavior | select field | — | — | — | — | — | — |
| Expired-value treatment | select field | — | — | — | — | — | — |
| Notification Schedule | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Extend, Reinstate, Suspend, Cancel, Replace, Reissue. Each needs attaching to the control it gates, or the screen needs the control.

**Where the user goes next**

- → `BO-1123` Gift Card & Digital Benefit Command Center: *Back to Gift Card & Digital Benefit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift card voucher configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift card voucher untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gift card voucher configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `expireCreditLots` → `WALLET_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1130` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1130`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 14: Works in Gift Card & Voucher Expiry Management → Control validity, expiration, extension and customer notification. Expiry Models Never expires Fixed date X days after purchase X days after activation X days after issuance End of campaign End of …

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1130?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1123`.
- [ ] Every gated control is gated: `WALLET_OPERATE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1131` Gift Card Balance, Liability & Breakage Control

**Connect gift-card operations to financial liability management without duplicating the Finance module. The source explicitly requires Gift Card Liability Reporting and Gift Card Breakage & Revenue Recognition. Liability Dashboard**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/gift-card-balance-liability-breakage-control-bo-1131` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every gift card balance** (data table)

| Shows | Format | Notes |
|---|---|---|
| Gift cards sold | text | not in the schema: `Gift cards sold` |
| Original issued value | text | not in the schema: `Original issued value` |
| Outstanding balance | text | not in the schema: `Outstanding balance` |
| Redeemed balance | text | not in the schema: `Redeemed balance` |
| Expired balance | text | not in the schema: `Expired balance` |
| Suspended balance | text | not in the schema: `Suspended balance` |
| Unredeemed balance | text | not in the schema: `Unredeemed balance` |
| Breakage amount | text | not in the schema: `Breakage amount` |
| Recognized revenue | text | not in the schema: `Recognized revenue` |
| Deferred liability | text | not in the schema: `Deferred liability` |

**The selected gift card balance** (detail panel): The pack groups this record's detail under its own headings: “Break down by”.

| Shows | Format | Notes |
|---|---|---|
| Gift cards sold | text | not in the schema: `Gift cards sold` |
| Original issued value | text | not in the schema: `Original issued value` |
| Outstanding balance | text | not in the schema: `Outstanding balance` |
| Redeemed balance | text | not in the schema: `Redeemed balance` |
| Expired balance | text | not in the schema: `Expired balance` |
| Suspended balance | text | not in the schema: `Suspended balance` |
| Unredeemed balance | text | not in the schema: `Unredeemed balance` |
| Breakage amount | text | not in the schema: `Breakage amount` |
| Recognized revenue | text | not in the schema: `Recognized revenue` |
| Deferred liability | text | not in the schema: `Deferred liability` |

**Data it reads**: `getWalletLiability` (onLoad, Balance, liability and breakage)

**Where the user goes next**

- → `BO-1123` Gift Card & Digital Benefit Command Center: *Back to Gift Card & Digital Benefit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift card balance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift card balance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gift card balance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gift card balance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getWalletLiability` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1131` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1131`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 16: Works in Gift Card Balance, Liability & Breakage Control → Connect gift-card operations to financial liability management without duplicating the Finance module. The source explicitly requires Gift Card Liability Reporting and Gift Card Breakage & Revenue …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1131?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1123`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1132` Gift Card & Voucher Simulator, Validation & Publication

**Allow administrators to test complete gift-card, voucher and benefit configurations before activation. Scenario Example Customer: Gold Member Venue: Theme Park Configure how customers actually use TICVAI Wallet value across every sales and venue touchpoint—POS, mobile app, B2C website, kiosk, RFID/NFC wristbands, QR credentials, attractions, F&B, Retail, Parking, Rental and integrated third-party systems. This board primarily covers requirements 4.3.7, 4.3.8, 4.3.10, 4.3.12, 4.3.13 and 4.3.20, including cross-channel wallet usage, wearables, NFC/RFID/QR, Digital Key authentication and integration-based wallet usage.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/gift-card-voucher-simulator-validation-publication-bo-1132` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish wallet configuration (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-1123` Gift Card & Digital Benefit Command Center: *Back to Gift Card & Digital Benefit Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift card voucher list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift card voucher untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gift card voucher yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gift card voucher are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `publishWalletConfiguration` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Configuration simulation/test mode lets an admin run sample transactions against a wallet configuration (e.g. spend-category restrictions) before publishing, instead of discovering errors live. *(agreed · MoM 27 Aug 2026, 4.7 Configuration simulation tool · DI-528)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1132` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS190 Wallet Configuration Backend Structure v1.0 Board 5.dc.html#bo-1132`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 5
- Flow F297 *Wallet Configuration Backend Structure v1.0 board 5: Gift Card & Digital …*, step 18: Works in Gift Card & Voucher Simulator, Validation & Publication → Allow administrators to test complete gift-card, voucher and benefit configurations before activation. Scenario Example Customer: Gold Member Venue: Theme Park

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1132?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish wallet configuration, Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-1123`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P08 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-030, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051, DI-052 (each is in the design inputs below).

**Workshop tracker rows about P08 as a whole** (1: 1 open, 0 closed). Open first; a closed row says where it went on 30 September.

- **S8** Venue Management back-end configuration wireframes *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*

## Design inputs from the client meetings

**What the client asked for in the meetings and design reviews, for these screens.** Apply every item. They are the client's own requirements and they are later than the reference files: where a reference design or a screen's fields disagree with an item here, the item wins. Newest first; where two items disagree, the newer one wins (anything a later meeting replaced is already left out). An **Open question** is not settled: build the default it states and keep it easy to change. The text in brackets is for traceability and, like everything else in this bundle, never appears on a screen.

### Everywhere, on every app

- Allam (platform-wide requirement): every calendar throughout the platform, not just maintenance, must support day, week and month views, with the day view further broken down by hour from a defined start hour through the day. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-907)*
- Minimise the number of separate screens an end user navigates: consolidate related information wherever it can reasonably be shown together, rather than mirroring every workshop board as its own screen. *(agreed · MoM 7 Sep 2026, 4.10 Screen consolidation / 5. Key Decisions · DI-671)*
- Region-configurable tax on pre-discount price (e.g. Egypt: AED 100 ticket with 20% off is paid at AED 80 but taxed on AED 100). Rounding must support up to three decimal places without dropping the third decimal where the currency requires it. *(agreed · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-598)*
- "Powered by TICVAI" is shown consistently across staff and guest-facing surfaces. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-297)*
- Full multi-language support (Arabic and others such as Chinese) consistent with the agreed i18n/RTL architecture. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-210)*
- The reference system is a functional reference only: its dated UI/UX is not to be replicated; TICVAI delivers equivalent depth with a modern, AI-friendly, easy-to-configure experience. *(agreed · MoM 7 Aug 2026, 23. Reference System Access & Documentation · DI-186)*
- Direction: modern, minimalistic, spacious, cross-device designs that still convey a sense of place (venue or park); Softlabs proposes two to three enhanced visual concepts for TICVAI to steer. *(agreed · MoM 3 Aug 2026, 11. Design Alignment & Team Input · DI-126)*
- Languages: English and Arabic at minimum, with Russian, Spanish and Mandarin. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-080)*
- Clarity first; reduce cognitive load (simple layouts, familiar patterns); consistency ("Use the system. Do not recreate."); accessibility; hierarchy (guide attention with contrast, spacing and visual weight); feedback (every action has a clear response). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Design Principles in Action · DI-051)*
- Standard components: search bar with Cmd+K; tabs (Overview, Events, Sales, Reports); pagination; badges (New, Pending, Sold Out, Completed); toggle (Off/On); dropdown; removable chip ("VIP x"). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Example UI Components · DI-050)*
- Spacing on an 8px base grid: 4, 8, 12, 16, 24, 32, 40, 48, 64, 80. Border radius scale 4, 8, 12, 16, 24px, consistent across the platform. Soft shadows: sm 0 1px 2px rgba(0,0,0,.05); md 0 4px 6px rgba(0,0,0,.08); lg 0 10px 15px rgba(0,0,0,.10); xl 0 20px 40px rgba(0,0,0,.14). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 6. Spacing / 7. Border Radius / 8. Shadows · DI-049)*
- Icons: line style, outline, 2px stroke, round corners, clean and consistent. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 5. Icons · DI-048)*
- Component principles: clarity first; consistent spacing on an 8px grid; meaningful colour (colours communicate status and guide the user); accessible by design; mobile ready (components adapt across all screen sizes). Components are consistent, flexible, accessible and composable. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Component principles · DI-045)*
- Empty states have a title, one explanatory line and one action: "No events yet / Create your first event to get started / Create Event"; "No data available / We couldn't find anything to show here / Refresh". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Empty States · DI-044)*
- Notification list: status icon, title, one-line detail and relative time (e.g. "Payment received ... 2m ago", "High demand detected ... 10m ago"), with "View all notifications". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Notifications · DI-042)*
- Forms: label above field; text input, select ("Choose an option"), date picker, toggle, checkbox. Input states: Default, Focused, Filled, Disabled and Error with inline message (e.g. "This field is required"). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Forms; 08 Design System (p8) - 4. Inputs · DI-040)*
- Card types: event card (title, date and time, venue, "From 120.00 AED"); KPI card (label, value, delta, "vs last 7 days"); onboarding checklist card ("3 of 6 completed": Create Event, Add Staff, Configure Seating, Connect Payment). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Cards · DI-038)*
- Button hierarchy Primary, Secondary, Tertiary (text) and Icon buttons, each with Default, Hover, Pressed and Disabled states. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Buttons; 08 Design System (p8) - 3. Buttons · DI-036)*
- Regardless of the module a user is working in, the experience should feel like one product, not a collection of separate applications. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) · DI-034)*
- DO: focus on clarity and hierarchy, use clear simple interactive elements, give relevant information at a glance (card example: "Annual Membership / All Venues / 4.4 (388) / BESTSELLER"). DON'T: clutter and overload (e.g. "-10% NEW PROMO AED 450.00 !!! BOOK NOW!!!"), complex forms and flows, hard-to-read data visualisations. *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - DO / DON'T · DI-033)*
- Eight principles on every screen: User-Centric, AI-First, Simple & Clear (clean layouts, clear hierarchy, minimal noise), Fast & Efficient (optimised for quick actions), Reliable & Secure (permissions, data protection), Data-Driven (data visual, actionable, easy to understand), Scalable, Consistent (same patterns, components and interactions across the ecosystem). *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - Our Design Principles · DI-032)*
- Accessibility: high contrast, readable text, keyboard navigation and inclusive components throughout; WCAG AA standards minimum ("Design for everyone"). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Better Accessibility; 06 Component principles (p6); 08 Design principles in action (p8) · DI-029)*
- AI everywhere: AI insights, recommendations and smart assistance are embedded across the platform, not hidden. AI is not an add-on: it assists, predicts, recommends and automates. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - How TICVAI improves this concept; 05 Design Principles (p5) - 2. AI-First · DI-027)*
- Global Search: prominent, AI-powered search that finds anything, in the top bar with a Cmd+K shortcut (placeholder e.g. "Search events, customers, orders, venues or ask AI..."). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, item 1; 08 Design System (p8) - Search Bar · DI-025)*
- Visual direction: Purposeful (every element has a clear purpose), Consistent (one visual system across all modules and devices), Clear (easy to scan, understand and act on), Modern. Key takeaway: clean, modern, product-first layout with clear hierarchy and minimal visual noise; deep, modern, trustworthy; built for enterprise scale. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) · DI-024)*
- The brand is presented consistently across Web Platform, Mobile App and Admin Portal (and print). Ticvai identity, colours and typography are applied consistently across all screens and devices. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand in action; 03 Visual Direction (p3) - Consistent Branding · DI-023)*
- Copy is Professional, Friendly, Clear, Confident, Concise and Helpful. Avoid jargon, overly technical language, clutter, outdated language and complexity. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand voice · DI-022)*
- Brand personality: Modern, AI-First, Enterprise, Premium, Reliable, Minimal, Scalable, Human-Centred. Visual essence: intelligent and forward-thinking, clean and minimal, trustworthy and secure, modern and timeless, scalable and flexible. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand personality / Visual essence · DI-021)*
- Arabic is a core requirement, not later localisation: full Arabic RTL across web, mobile, POS, reports, emails, WhatsApp, SMS, notifications, tickets and receipts, and administrative interfaces. *(agreed · MoM 28 Jul 2026, 27. Internationalisation and Arabic Support · DI-019)*

### Across P08 Venue Management

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"activateGiftCard": {"method":"POST","path":"/gift-cards/{giftCardId}/activate","contract":"wallet","summary":"Activate a card at the point of sale","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GiftCard"},
"createVoucherType": {"method":"POST","path":"/voucher-types","contract":"wallet","summary":"Define a voucher or benefit","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VoucherType","responds":"VoucherType"},
"expireCreditLots": {"method":"POST","path":"/credit-lots/expire","contract":"wallet","summary":"Expire, extend or forfeit credit that has run out of time","permission":"WALLET_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CreditExpiryResult"},
"getGiftCard": {"method":"GET","path":"/gift-cards/{cardCode}","contract":"wallet","summary":"Check a gift card balance","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GiftCard"},
"getWalletLiability": {"method":"GET","path":"/wallet-liability","contract":"wallet","summary":"What is outstanding, and what is breakage","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"asOf","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"WalletLiabilityRow"},
"issueGiftCard": {"method":"POST","path":"/gift-cards","contract":"wallet","summary":"Issue or activate a gift card","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IssueGiftCardRequest","responds":"GiftCard"},
"listVoucherTypes": {"method":"GET","path":"/voucher-types","contract":"wallet","summary":"Voucher, coupon and benefit definitions","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VoucherType"},
"publishWalletConfiguration": {"method":"POST","path":"/wallet-configuration/publish","contract":"wallet","summary":"Validate and publish the wallet configuration as a version","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletConfigurationVersion"},
"redeemGiftCard": {"method":"POST","path":"/gift-cards/{giftCardId}/redeem","contract":"wallet","summary":"Spend against a card","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GiftCard"},
"setGiftCardProduct": {"method":"PUT","path":"/gift-card-products","contract":"wallet","summary":"Denominations, validity, activation and distribution","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GiftCardProduct","responds":"GiftCardProduct"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreditExpiryResult": {"type":"object","description":"Board 3.9. **Expiry has an accounting consequence**, so the preview carries it.","properties":{"lotsAffected":{"type":"integer"},"totalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"walletsAffected":{"type":"integer"},"applied":{"type":"boolean"},"asOf":{"type":"string","format":"date"}}},
"GiftCard": {"x-ticvai-persistence":"wallet.gift_card","type":"object","required":["cardCode","faceValue","balance","status","issuedAt"],"properties":{"cardCode":{"type":"string"},"kind":{"type":"string"},"faceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["issued","active","partiallyRedeemed","redeemed","expired","blocked"]},"blockedReason":{"type":"string","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},
"GiftCardProduct": {"type":"object","x-ticvai-persistence":"wallet.gift_card_product","description":"Boards 5.2 and 5.3. **Activation separate from issuance is a theft control.**","properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"denominations":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/Money"}},"openAmountAllowed":{"type":"boolean","default":false},"minimumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reloadable":{"type":"boolean","default":false},"validityMonths":{"type":"integer","nullable":true},"activationRequired":{"type":"boolean","default":true},"creditTypeId":{"type":"string","format":"uuid"},"physical":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"IssueGiftCardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","faceValue","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["physical","digital"]},"cardCode":{"type":"string","description":"Required for physical cards, which are pre-printed. Generated for digital."},"faceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"recipientEmail":{"type":"string","nullable":true},"recipientPhone":{"type":"string","nullable":true},"message":{"type":"string","maxLength":500},"validMonths":{"type":"integer","minimum":1}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"VoucherType": {"type":"object","x-ticvai-persistence":"wallet.voucher_type","description":"Board 5.4. **An entitlement with conditions, not a balance.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"benefitKind":{"type":"string","enum":["freeItem","percentDiscount","fixedDiscount","upgrade","accessEntitlement","companionEntry"]},"benefitValue":{"type":"number","nullable":true},"conditions":{"type":"object","additionalProperties":true},"singleUse":{"type":"boolean","default":true},"combinable":{"type":"boolean","default":false},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"issueLimit":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"WalletConfigurationVersion": {"type":"object","x-ticvai-persistence":"wallet.configuration_version","description":"Boards 1.10 and 10.8. **Ten boards of configuration that interact.**","properties":{"version":{"type":"integer"},"publishedAt":{"type":"string","format":"date-time","nullable":true},"publishedBy":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning"]},"code":{"type":"string"},"message":{"type":"string"}}}},"scopePath":{"type":"string"}}},
"WalletLiabilityRow": {"type":"object","description":"Boards 9.5 and 9.6. **The number the finance director asks for.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"outstanding":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expiringThisPeriod":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageRecognised":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"walletCount":{"type":"integer"},"oldestLotAt":{"type":"string","format":"date","nullable":true}}}
}
```
