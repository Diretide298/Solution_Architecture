# WS46 — Promotions   Bundles Management board 2

**10 screens · 11 operations · 14 schemas · 2 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
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
| `ADM-148` | Promotion Rule Builder | A | 0 | 0 | 6 | 0 | 1 | 2 | — | notStarted (generated) |
| `ADM-149` | Percentage & Fixed Discount Configurator | B–D | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-150` | Cart & Transaction Threshold Rules | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-151` | Volume, Bulk & Tier Discount Configurator | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-152` | Time-Based & Seasonal Discount Rules | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-153` | Customer, Membership & Segment Discount Rules | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `ADM-154` | Payment Method, Bank & Partner Discount Rules | B–D | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-155` | Special Price & Guest Offer Configurator | B–D | 12 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-156` | Discount Limits, Guardrails & Commercial Controls | B–D | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-157` | Rule Test, Simulation & AI Recommendation Workspace | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-148, ADM-150, ADM-151, ADM-152, ADM-153 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-148` Promotion Rule Builder

**Provide the main no-code workspace for creating the commercial logic behind a promotion.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20647 (APP-SETUP-ADM-148) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/promotion-rule-builder-adm-148` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 1 operation.** Unserved: Nested condition groups. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Nested condition groups (primary button) | navigation or local | — | — | — | — |
| Rule ordering (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-149` Percentage & Fixed Discount Configurator: *Works in Percentage & Fixed Discount Configurator*; calls `setPromotionRule`
- → `ADM-150` Cart & Transaction Threshold Rules: *Works in Cart & Transaction Threshold Rules*; calls `setPromotionRule`
- → `ADM-151` Volume, Bulk & Tier Discount Configurator: *Works in Volume, Bulk & Tier Discount Configurator*; calls `setPromotionRule`
- → `ADM-152` Time-Based & Seasonal Discount Rules: *Works in Time-Based & Seasonal Discount Rules*; calls `setPromotionRule`
- → `ADM-153` Customer, Membership & Segment Discount Rules: *Works in Customer, Membership & Segment Discount Rules*; calls `setPromotionRule`
- → `ADM-154` Payment Method, Bank & Partner Discount Rules: *Works in Payment Method, Bank & Partner Discount Rules*; calls `setPromotionRule`
- → `ADM-155` Special Price & Guest Offer Configurator: *Works in Special Price & Guest Offer Configurator*; calls `setPromotionRule`
- → `ADM-156` Discount Limits, Guardrails & Commercial Controls: *Works in Discount Limits, Guardrails & Commercial Controls*; calls `setPromotionRule`
- → `ADM-157` Rule Test, Simulation & AI Recommendation Workspace: *Works in Rule Test, Simulation & AI Recommendation Workspace*; calls `setPromotionRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPromotionRule` → `PRICE_CONFIGURE` (configure) · staff
- `setPromotionStackingRule` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-148` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-148`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 1: Opens Promotion Rule Builder → Provide the main no-code workspace for creating the commercial logic behind a promotion.
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F155 branch at step 1 (expected): when Nothing has been set up on Promotion Rule Builder yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F155 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-148?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Nested condition groups, Rule ordering.
- [ ] Every transition is wired: `ADM-002`, `ADM-149`, `ADM-150`, `ADM-151`, `ADM-152`, `ADM-153`, `ADM-154`, `ADM-155`, `ADM-156`, `ADM-157`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-149` Percentage & Fixed Discount Configurator

**Configure the two fundamental discount types required by the matrix. The matrix explicitly states that discounts may be defined as percentage or fixed value.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/percentage-fixed-discount-configurator-adm-149` |

**Known gaps.** **Percentage & Fixed Discount Configurator declares no operation that writes anything** — its only declared call is `listPercentageFixedDiscount`, a read. The name promises authoring and the contract …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Discount percentage | select field | — | — | — | — | — | — |
| Maximum percentage | select field | — | — | — | — | — | — |
| Maximum monetary discount | select field | — | — | — | — | — | — |
| Minimum qualifying amount | select field | — | — | — | — | — | — |
| Rounding method | select field | — | — | — | — | — | — |
| Discount amount | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Minimum basket value | select field | — | — | — | — | — | — |
| Maximum uses | select field | — | — | — | — | — | — |
| Whether applied per item or transaction | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listPercentageFixedDiscount` (onLoad, Percentage & Fixed Discount Configurator)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listPercentageFixedDiscount`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The percentage fixed discount configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the percentage fixed discount untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No percentage fixed discount configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPercentageFixedDiscount` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-149` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-149`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 2: Works in Percentage & Fixed Discount Configurator → Configure the two fundamental discount types required by the matrix. The matrix explicitly states that discounts may be defined as percentage or fixed value.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-149?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-150` Cart & Transaction Threshold Rules

**Configure promotions triggered by basket value, ticket quantity, transaction value, or purchase composition. The matrix specifically requires rules such as if more than X tickets are purchased, apply Y discount to the entire transaction.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/cart-transaction-threshold-rules-adm-150` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCartTransactionThreshold` (onLoad, Cart & Transaction Threshold Rules)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listCartTransactionThreshold`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cart transaction threshold list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cart transaction threshold untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cart transaction threshold yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cart transaction threshold are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCartTransactionThreshold` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-150` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-150`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 4: Works in Cart & Transaction Threshold Rules → Configure promotions triggered by basket value, ticket quantity, transaction value, or purchase composition. The matrix specifically requires rules such as if more than X tickets are purchased, apply …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-150?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-151` Volume, Bulk & Tier Discount Configurator

**Manage quantity-based and bulk-purchase commercial rules. The matrix requires configurable bulk thresholds and discount percentages, dedicated group pricing, and tiered bulk purchasing.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/volume-bulk-tier-discount-configurator-adm-151` |

**Known gaps.** **Volume, Bulk & Tier Discount Configurator declares no operation that writes anything** — its only declared call is `listVolumeBulkTier`, a read. The name promises authoring and the contract offers … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listVolumeBulkTier` (onLoad, Volume, Bulk & Tier Discount Configurator)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listVolumeBulkTier`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The volume bulk tier list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the volume bulk tier untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No volume bulk tier yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the volume bulk tier are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listVolumeBulkTier` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-151` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-151`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 6: Works in Volume, Bulk & Tier Discount Configurator → Manage quantity-based and bulk-purchase commercial rules. The matrix requires configurable bulk thresholds and discount percentages, dedicated group pricing, and tiered bulk purchasing.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-151?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-152` Time-Based & Seasonal Discount Rules

**Configure promotional pricing based on when the customer purchases or visits.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/time-based-seasonal-discount-rules-adm-152` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listTimeBasedSeasonal` (onLoad, Time-Based & Seasonal Discount Rules)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listTimeBasedSeasonal`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The time-based seasonal discount list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the time-based seasonal discount untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No time-based seasonal discount yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the time-based seasonal discount are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listTimeBasedSeasonal` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-152` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-152`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 8: Works in Time-Based & Seasonal Discount Rules → Configure promotional pricing based on when the customer purchases or visits.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-152?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-153` Customer, Membership & Segment Discount Rules

**Configure discounts based on who the customer is.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/customer-membership-segment-discount-rules-adm-153` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCustomerMembershipSegment` (onLoad, Customer, Membership & Segment Discount Rules)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listCustomerMembershipSegment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer membership segment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer membership segment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer membership segment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer membership segment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCustomerMembershipSegment` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-153` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-153`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 10: Works in Customer, Membership & Segment Discount Rules → Configure discounts based on who the customer is.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-153?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-154` Payment Method, Bank & Partner Discount Rules

**Configure discounts triggered by how the guest pays or which commercial partner they belong to. The matrix specifically includes discounts for payment types and bank credit/debit cards.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/payment-method-bank-partner-discount-rules-adm-154` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Membership programs. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Partner bank | select field | — | — | — | — | — | — |
| BIN/IIN eligibility reference | select field | — | — | — | — | — | — |
| Promotion period | select field | — | — | — | — | — | — |
| Eligible products | select field | — | — | — | — | — | — |
| Minimum spend | select field | — | — | — | — | — | — |
| Discount % | select field | — | — | — | — | — | — |
| Maximum discount | select field | — | — | — | — | — | — |
| Number of uses | select field | — | — | — | — | — | — |
| Customer limit | select field | — | — | — | — | — | — |
| Campaign budget | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Membership programs (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentMethodBank` (onLoad, Payment Method, Bank & Partner Discount Rules)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listPaymentMethodBank`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment method bank configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment method bank untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment method bank configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPaymentMethodBank` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-154` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-154`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 12: Works in Payment Method, Bank & Partner Discount Rules → Configure discounts triggered by how the guest pays or which commercial partner they belong to. The matrix specifically includes discounts for payment types and bank credit/debit cards.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-154?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Membership programs.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-155` Special Price & Guest Offer Configurator

**Manage commercially distinct special-price products and targeted offers without unnecessarily duplicating product SKUs.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/special-price-guest-offer-configurator-adm-155` |

**Known gaps.** **Special Price & Guest Offer Configurator declares no operation that writes anything** — its only declared call is `listSpecialPriceGuest`, a read. The name promises authoring and the contract …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Offer name | select field | — | — | — | — | — | — |
| Eligible product | select field | — | — | — | — | — | — |
| Eligible guest | select field | — | — | — | — | — | — |
| Price | select field | — | — | — | — | — | — |
| Discount | select field | — | — | — | — | — | — |
| Valid dates | select field | — | — | — | — | — | — |
| Valid visit dates | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Capacity | select field | — | — | — | — | — | — |
| Restrictions | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listSpecialPriceGuest` (onLoad, Special Price & Guest Offer Configurator)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listSpecialPriceGuest`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The special price guest configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the special price guest untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No special price guest configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listSpecialPriceGuest` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-155` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-155`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 14: Works in Special Price & Guest Offer Configurator → Manage commercially distinct special-price products and targeted offers without unnecessarily duplicating product SKUs.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-155?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-156` Discount Limits, Guardrails & Commercial Controls

**Protect the business from incorrectly configured discounts and excessive commercial exposure.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/discount-limits-guardrails-commercial-controls-adm-156` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Maximum discount % | select field | — | — | — | — | — | — |
| Maximum discount value | select field | — | — | — | — | — | — |
| Minimum selling price | select field | — | — | — | — | — | — |
| Minimum margin | select field | — | — | — | — | — | — |
| Maximum transaction discount | select field | — | — | — | — | — | — |
| Maximum customer discount | select field | — | — | — | — | — | — |
| Maximum campaign exposure | select field | — | — | — | — | — | — |
| Maximum redemption count | select field | — | — | — | — | — | — |
| Per-customer usage | select field | — | — | — | — | — | — |
| Per-account usage | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listDiscountLimitGuardrail` (onLoad, Discount Limits, Guardrails & Commercial Controls)

**Where the user goes next**

- → `ADM-148` Promotion Rule Builder: *Returns to the board's landing screen*; calls `listDiscountLimitGuardrail`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The discount limits guardrails configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the discount limits guardrails untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No discount limits guardrails configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listDiscountLimitGuardrail` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-156` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-156`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 16: Works in Discount Limits, Guardrails & Commercial Controls → Protect the business from incorrectly configured discounts and excessive commercial exposure.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-156?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-148`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-157` Rule Test, Simulation & AI Recommendation Workspace

**Allow administrators to test promotional rules before activating them. This is critical because the matrix requires simulation of redemption, discount exposure, revenue impact, margin impact and financial performance before activation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/rule-test-simulation-ai-recommendation-workspace-adm-157` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Campaign Manager, Commercial Manager, Revenue Manager, Finance, B2B Manager, Venue Manager. Each needs an … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Create rules, Edit rules, Change discount, Change thresholds, Change segments, Change dates, Override limits, Run simulation, Submit, Approve, Activate. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Campaign Manager (primary button) | navigation or local | — | — | — | — |
| Commercial Manager (secondary button) | navigation or local | — | — | — | — |
| Revenue Manager (secondary button) | navigation or local | — | — | — | — |
| Finance (secondary button) | navigation or local | — | — | — | — |
| B2B Manager (secondary button) | navigation or local | — | — | — | — |
| Venue Manager (secondary button) | navigation or local | — | — | — | — |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rule test simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rule test simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rule test simulation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rule test simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRuleTestRecommendation` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-157` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS107 Promotions   Bundles Management Board 2.dc.html#adm-157`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 2
- Flow F155 *Promotions Bundles Management board 2: Promotion Rule Builder*, step 18: Works in Rule Test, Simulation & AI Recommendation Workspace → Allow administrators to test promotional rules before activating them. This is critical because the matrix requires simulation of redemption, discount exposure, revenue impact, margin impact and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-157?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Campaign Manager, Commercial Manager, Revenue Manager, Finance, B2B Manager, Venue Manager.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P09 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P09 TICVAI Web

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listCartTransactionThreshold": {"method":"GET","path":"/cart-transaction-threshold","contract":"promotions","summary":"Cart & Transaction Threshold Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CartTransactionThresholdRulesView"},
"listCustomerMembershipSegment": {"method":"GET","path":"/customer-membership-segment","contract":"promotions","summary":"Customer, Membership & Segment Discount Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomerMembershipSegmentDiscountRulesView"},
"listDiscountLimitGuardrail": {"method":"GET","path":"/discount-limit-guardrail","contract":"promotions","summary":"Discount Limits, Guardrails & Commercial Controls","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"DiscountLimitsGuardrailsCommercialControlsView"},
"listPaymentMethodBank": {"method":"GET","path":"/payment-method-bank","contract":"promotions","summary":"Payment Method, Bank & Partner Discount Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PaymentMethodBankPartnerDiscountRulesView"},
"listPercentageFixedDiscount": {"method":"GET","path":"/percentage-fixed-discount","contract":"promotions","summary":"Percentage & Fixed Discount Configurator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PercentageFixedDiscountConfiguratorView"},
"listSpecialPriceGuest": {"method":"GET","path":"/special-price-guest","contract":"promotions","summary":"Special Price & Guest Offer Configurator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SpecialPriceGuestOfferConfiguratorView"},
"listTimeBasedSeasonal": {"method":"GET","path":"/time-based-seasonal","contract":"promotions","summary":"Time-Based & Seasonal Discount Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TimeBasedSeasonalDiscountRulesView"},
"listVolumeBulkTier": {"method":"GET","path":"/volume-bulk-tier","contract":"promotions","summary":"Volume, Bulk & Tier Discount Configurator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VolumeBulkTierDiscountConfiguratorView"},
"setPromotionRule": {"method":"PUT","path":"/promotion-rule","contract":"promotions","summary":"Promotion Rule Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PromotionRuleBuilderInput","responds":"PromotionRuleBuilderView"},
"setPromotionStackingRule": {"method":"PUT","path":"/promotion-stacking-rule","contract":"promotions","summary":"Promotion Stacking Rule Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PromotionStackingRuleBuilderInput","responds":"PromotionStackingRuleBuilderView"},
"setRuleTestRecommendation": {"method":"PUT","path":"/rule-test-recommendation","contract":"promotions","summary":"Rule Test, Simulation & AI Recommendation Workspace","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RuleTestSimulationAiRecommendationWorkspaceInput","responds":"RuleTestSimulationAiRecommendationWorkspaceView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CartTransactionThresholdRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Cart & Transaction Threshold Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"taxCountsTowardThreshold":{"type":"integer","description":"Tax counts toward threshold"},"feesCount":{"type":"integer","description":"Fees count"},"vouchersCount":{"type":"integer","description":"Vouchers count"},"discountsAreEvaluatedBeforeAfterThreshold":{"type":"integer","description":"Discounts are evaluated before/after threshold"},"voidedItemsAreExcluded":{"type":"string","description":"Voided items are excluded"},"refundedItemsAffectQualification":{"type":"string","description":"Refunded items affect qualification"}}},
"CustomerMembershipSegmentDiscountRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Customer, Membership & Segment Discount Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"customerSegment":{"type":"string","description":"Customer segment"},"crmSegment":{"type":"string","description":"CRM segment"},"guestCategory":{"type":"string","description":"Guest category"},"ageCategory":{"type":"string","description":"Age category"},"membershipStatus":{"type":"string","description":"Membership status"},"membershipTier":{"type":"string","description":"Membership tier"},"loyaltyTier":{"type":"string","description":"Loyalty tier"},"annualPassHolder":{"type":"string","description":"Annual pass holder"},"corporateAffiliation":{"type":"string","description":"Corporate affiliation"},"partnerAffiliation":{"type":"string","description":"Partner affiliation"},"account":{"type":"string","description":"Account"},"countryResidency":{"type":"string","description":"Country/residency"},"b2bCustomer":{"type":"string","description":"B2B customer"}}},
"DiscountLimitsGuardrailsCommercialControlsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Discount Limits, Guardrails & Commercial Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumDiscount":{"type":"number","description":"Maximum discount %"},"maximumDiscountValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum discount value"},"minimumSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum selling price"},"minimumMargin":{"type":"number","description":"Minimum margin"},"maximumTransactionDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum transaction discount"},"maximumCustomerDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum customer discount"},"maximumCampaignExposure":{"type":"string","description":"Maximum campaign exposure"},"maximumRedemptionCount":{"type":"integer","description":"Maximum redemption count"},"perCustomerUsage":{"type":"string","description":"Per-customer usage"},"perAccountUsage":{"type":"string","description":"Per-account usage"},"requireApproval":{"type":"boolean","description":"Require approval"}}},
"PaymentMethodBankPartnerDiscountRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Payment Method, Bank & Partner Discount Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"selectedPaymentGateway":{"type":"string","description":"Selected payment gateway"},"partnerBank":{"type":"string","description":"Partner bank"},"binIinEligibilityReference":{"type":"string","description":"BIN/IIN eligibility reference"},"promotionPeriod":{"type":"string","format":"date-time","description":"Promotion period"},"eligibleProducts":{"type":"string","description":"Eligible products"},"minimumSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum spend"},"discount":{"type":"number","description":"Discount %"},"maximumDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum discount"},"numberOfUses":{"type":"integer","description":"Number of uses"},"customerLimit":{"type":"integer","description":"Customer limit"},"campaignBudget":{"type":"string","description":"Campaign budget"},"banks":{"type":"string","description":"Banks"},"paymentConditions":{"type":"array","items":{"type":"string","enum":["creditCard","debitCard","visa","mastercard","mada","applePay","wallet","giftCard","bankSpecificCard"]},"description":"Payment methods that qualify."},"partnerType":{"type":"string","enum":["hotels","airlines","tourismPartners","corporatePartners","governmentPartners","membershipPrograms"],"description":"Partner behind the offer."}}},
"PercentageFixedDiscountConfiguratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Percentage & Fixed Discount Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"discountPercentage":{"type":"number","description":"Discount percentage"},"maximumPercentage":{"type":"number","description":"Maximum percentage"},"maximumMonetaryDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum monetary discount"},"minimumQualifyingAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum qualifying amount"},"roundingMethod":{"type":"string","description":"Rounding method"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount amount"},"currency":{"type":"string","description":"Currency"},"minimumBasketValue":{"type":"string","description":"Minimum basket value"},"maximumUses":{"type":"string","description":"Maximum uses"},"priceBasis":{"type":"string","enum":["currentSellingPrice","dynamicPrice","membershipPrice","b2bPrice","packagePrice"],"description":"The price the discount applies against."}}},
"PromotionRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; saved as a `promotions.promotion_rule` row (PromotionRule, ruleType benefit) (DM5, 29 September: data model for the agreed operations)","description":"**What Promotion Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"ruleName":{"type":"string","description":"Rule name"},"ruleId":{"type":"string","description":"Rule ID"},"promotion":{"type":"string","description":"Promotion"},"description":{"type":"string","description":"Description"},"owner":{"type":"string","description":"Owner"},"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"ruleStatus":{"type":"string","description":"Rule status"},"priority":{"type":"string","description":"Priority"},"percentageDiscount":{"type":"number","description":"Percentage discount"},"fixedDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed discount"},"fixedSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed selling price"},"freeProduct":{"type":"string","description":"Free product"},"freeTicket":{"type":"string","description":"Free ticket"},"addedValue":{"type":"string","description":"Added value"},"voucher":{"type":"string","description":"Voucher"},"rewardEntitlement":{"type":"string","description":"Reward entitlement"},"nestedConditionGroups":{"type":"string","description":"Nested condition groups"},"multipleOutcomes":{"type":"string","description":"Multiple outcomes"},"ruleOrdering":{"type":"string","description":"Rule ordering"}}},
"PromotionRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleName":{"type":"string","description":"Rule name"},"ruleId":{"type":"string","description":"Rule ID"},"promotion":{"type":"string","description":"Promotion"},"description":{"type":"string","description":"Description"},"owner":{"type":"string","description":"Owner"},"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"ruleStatus":{"type":"string","description":"Rule status"},"priority":{"type":"string","description":"Priority"},"percentageDiscount":{"type":"number","description":"Percentage discount"},"fixedDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed discount"},"fixedSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed selling price"},"freeProduct":{"type":"string","description":"Free product"},"freeTicket":{"type":"string","description":"Free ticket"},"addedValue":{"type":"string","description":"Added value"},"voucher":{"type":"string","description":"Voucher"},"rewardEntitlement":{"type":"string","description":"Reward entitlement"},"nestedConditionGroups":{"type":"string","description":"Nested condition groups"},"multipleOutcomes":{"type":"string","description":"Multiple outcomes"},"ruleOrdering":{"type":"string","description":"Rule ordering"}}},
"PromotionStackingRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; the configurable part of a `promotions.stacking_rule` row (StackingRule composes it) (DM5, 29 September: data model for the agreed operations)","description":"**What Promotion Stacking Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"scope":{"type":"string","enum":["entireTransaction","product","productCategory","individualTicket","bundleComponent","customer","channel"],"description":"What the rule applies to."},"stackingModel":{"type":"string","enum":["fullyStackable","nonStackable","conditional","categoryStacking","maximumN"],"description":"Stacking model"},"maximumPromotions":{"type":"integer","description":"For maximumN: most promotions per transaction"},"promotionTypeA":{"type":"string","description":"First promotion type in the rule"},"promotionTypeB":{"type":"string","description":"Second promotion type in the rule"},"canStack":{"type":"boolean","description":"Whether A can stack with B"}}},
"PromotionStackingRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Stacking Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"scope":{"type":"string","enum":["entireTransaction","product","productCategory","individualTicket","bundleComponent","customer","channel"],"description":"What the rule applies to."},"stackingModel":{"type":"string","enum":["fullyStackable","nonStackable","conditional","categoryStacking","maximumN"],"description":"Stacking model"},"maximumPromotions":{"type":"integer","description":"For maximumN: most promotions per transaction"},"promotionTypeA":{"type":"string","description":"First promotion type in the rule"},"promotionTypeB":{"type":"string","description":"Second promotion type in the rule"},"canStack":{"type":"boolean","description":"Whether A can stack with B"}}},
"RuleTestSimulationAiRecommendationWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is promotions.bundle_component at 3%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Rule Test, Simulation & AI Recommendation Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"guest":{"type":"string","description":"Guest"},"segment":{"type":"string","description":"Segment"},"products":{"type":"string","description":"Products"},"quantity":{"type":"integer","description":"Quantity"},"channel":{"type":"string","description":"Channel"},"date":{"type":"string","format":"date-time","description":"Date"},"venue":{"type":"string","description":"Venue"},"membership":{"type":"string","description":"Membership"},"loyalty":{"type":"string","description":"Loyalty"},"paymentType":{"type":"string","description":"Payment type"},"promoCode":{"type":"string","description":"Promo code"}}},
"RuleTestSimulationAiRecommendationWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Rule Test, Simulation & AI Recommendation Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"guest":{"type":"string","description":"Guest"},"segment":{"type":"string","description":"Segment"},"products":{"type":"string","description":"Products"},"quantity":{"type":"integer","description":"Quantity"},"channel":{"type":"string","description":"Channel"},"date":{"type":"string","format":"date-time","description":"Date"},"venue":{"type":"string","description":"Venue"},"membership":{"type":"string","description":"Membership"},"loyalty":{"type":"string","description":"Loyalty"},"paymentType":{"type":"string","description":"Payment type"},"promoCode":{"type":"string","description":"Promo code"},"appliedRules":{"type":"array","items":{"type":"string"},"description":"Rules that qualified and applied to the sample transaction"},"rejectedRules":{"type":"array","items":{"type":"string"},"description":"Rules evaluated and not applied, each with its reason"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount granted to the sample transaction"},"finalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final amount after promotions"},"marginImpact":{"type":"number","description":"Margin impact of the tested rules, percent"},"aiRecommendation":{"type":"string","description":"AI recommendation (decision support only; never applied without authorisation)"}}},
"SpecialPriceGuestOfferConfiguratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Special Price & Guest Offer Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"offerName":{"type":"string","description":"Offer name"},"eligibleProduct":{"type":"string","description":"Eligible product"},"eligibleGuest":{"type":"string","description":"Eligible guest"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"validDates":{"type":"string","description":"Valid dates"},"validVisitDates":{"type":"string","description":"Valid visit dates"},"quantity":{"type":"integer","description":"Quantity"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"capacity":{"type":"integer","description":"Capacity"},"restrictions":{"type":"string","description":"Restrictions"},"residentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Resident price"},"touristPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Tourist price"},"employeePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Employee price"},"studentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Student price"},"schoolPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"School price"},"familyPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Family price"},"groupPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Group price"},"partnerPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Partner price"}}},
"TimeBasedSeasonalDiscountRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Time-Based & Seasonal Discount Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"purchaseDate":{"type":"string","format":"date-time","description":"Purchase date"},"visitDate":{"type":"string","format":"date-time","description":"Visit date"},"daysBeforeVisit":{"type":"string","description":"Days-before-visit"},"hoursBeforeVisit":{"type":"string","description":"Hours-before-visit"},"dayOfWeek":{"type":"string","description":"Day of week"},"time":{"type":"string","format":"date-time","description":"Time"},"timeslot":{"type":"string","description":"Timeslot"},"season":{"type":"string","description":"Season"},"eventPeriod":{"type":"string","format":"date-time","description":"Event period"},"seasonType":{"type":"string","enum":["summer","ramadan","eid","schoolHolidays","nationalDay","peakOffPeak","customSeasons"],"description":"Season the rule applies in."}}},
"VolumeBulkTierDiscountConfiguratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Volume, Bulk & Tier Discount Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"minimumQuantity":{"type":"integer","description":"Minimum quantity"},"maximumQuantity":{"type":"integer","description":"Maximum quantity"},"discount":{"type":"number","description":"Discount %"},"discountValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount value"},"fixedUnitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed unit price"},"eligibleProduct":{"type":"string","description":"Eligible product"},"eligibleCustomer":{"type":"string","description":"Eligible customer"},"eligibleChannel":{"type":"string","description":"Eligible channel"}}}
}
```
