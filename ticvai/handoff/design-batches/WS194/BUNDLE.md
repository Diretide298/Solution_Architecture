# WS194 — Wallet Configuration Backend Structure v1.0 board 9

**10 screens · 9 operations · 12 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `LEDGER_APPROVE, LEDGER_VIEW, WALLET_CONFIGURE, WALLET_OPERATE, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-1163` | Wallet Finance & Liability Command Center | B–D | 0 | 66 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1164` | Wallet Financial Classification & Accounting Mapping | B–D | 23 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1165` | Wallet Sub-Ledger & Balance Control | B–D | 2 | 25 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1166` | Multi-Source Reconciliation Configuration | B–D | 32 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1167` | Reconciliation Exception & Resolution Workbench | B–D | 0 | 24 | 6 | 1 | 2 | 0 | — | notStarted (—) |
| `BO-1168` | Gift Card Liability Management | B–D | 0 | 42 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1169` | Breakage & Revenue Recognition Policy | B–D | 0 | 6 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-1170` | Wallet Financial Period & Closing Controls | B–D | 18 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-1171` | Wallet Analytics & Management Reporting | B–D | 0 | 34 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-1172` | Finance Validation, Reporting & Audit Center | B–D | 0 | 10 | 6 | 1 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-1163, BO-1167, BO-1168, BO-1169, BO-1171 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1163` Wallet Finance & Liability Command Center

**Provide Finance and authorized management users with a consolidated financial view of all wallet obligations and movements. Executive KPIs**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-finance-liability-command-center-bo-1163` |

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

**Every wallet finance liability** (data table)

| Shows | Format | Notes |
|---|---|---|
| Total wallet liability | text | not in the schema: `Total Wallet Liability` |
| Cash credit liability | text | not in the schema: `Cash Credit Liability` |
| Gift card liability | text | not in the schema: `Gift Card Liability` |
| Refund credit liability | text | not in the schema: `Refund Credit Liability` |
| Bonus/promotional value | text | not in the schema: `Bonus/Promotional Value` |
| Membership credit exposure | text | not in the schema: `Membership Credit Exposure` |
| Outstanding stored value | text | not in the schema: `Outstanding Stored Value` |
| Issued value | text | not in the schema: `Issued Value` |
| Redeemed value | text | not in the schema: `Redeemed Value` |
| Expired value | text | not in the schema: `Expired Value` |
| Breakage recognized | text | not in the schema: `Breakage Recognized` |
| Unreconciled value | text | not in the schema: `Unreconciled Value` |
| Suspended/frozen value | text | not in the schema: `Suspended/Frozen Value` |
| Liability breakdown | text | not in the schema: `Liability Breakdown` |
| Credit type | text | not in the schema: `Credit type` |
| Wallet type | text | not in the schema: `Wallet type` |
| Gift card | text | not in the schema: `Gift card` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Customer type | text | not in the schema: `Customer type` |
| Accounting period | text | not in the schema: `Accounting period` |
| Movement analysis | text | not in the schema: `Movement Analysis` |
| Opening liability | text | not in the schema: `Opening Liability` |
| Funding | text | not in the schema: `Funding` |
| Gift cards issued | text | not in the schema: `Gift Cards Issued` |
| Credits issued | text | not in the schema: `Credits Issued` |
| Refunds to wallet | text | not in the schema: `Refunds to Wallet` |
| − redemptions | text | not in the schema: `− Redemptions` |
| − expirations | text | not in the schema: `− Expirations` |
| … 3 more | | `schemas.json` |

**The selected wallet finance liability** (detail panel): The pack groups this record's detail under its own headings: “Highlight”.

| Shows | Format | Notes |
|---|---|---|
| Total wallet liability | text | not in the schema: `Total Wallet Liability` |
| Cash credit liability | text | not in the schema: `Cash Credit Liability` |
| Gift card liability | text | not in the schema: `Gift Card Liability` |
| Refund credit liability | text | not in the schema: `Refund Credit Liability` |
| Bonus/promotional value | text | not in the schema: `Bonus/Promotional Value` |
| Membership credit exposure | text | not in the schema: `Membership Credit Exposure` |
| Outstanding stored value | text | not in the schema: `Outstanding Stored Value` |
| Issued value | text | not in the schema: `Issued Value` |
| Redeemed value | text | not in the schema: `Redeemed Value` |
| Expired value | text | not in the schema: `Expired Value` |
| Breakage recognized | text | not in the schema: `Breakage Recognized` |
| Unreconciled value | text | not in the schema: `Unreconciled Value` |
| Suspended/frozen value | text | not in the schema: `Suspended/Frozen Value` |
| Liability breakdown | text | not in the schema: `Liability Breakdown` |
| Credit type | text | not in the schema: `Credit type` |
| Wallet type | text | not in the schema: `Wallet type` |
| Gift card | text | not in the schema: `Gift card` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Customer type | text | not in the schema: `Customer type` |
| Accounting period | text | not in the schema: `Accounting period` |
| Movement analysis | text | not in the schema: `Movement Analysis` |
| Opening liability | text | not in the schema: `Opening Liability` |
| Funding | text | not in the schema: `Funding` |
| Gift cards issued | text | not in the schema: `Gift Cards Issued` |
| Credits issued | text | not in the schema: `Credits Issued` |
| Refunds to wallet | text | not in the schema: `Refunds to Wallet` |
| − redemptions | text | not in the schema: `− Redemptions` |
| − expirations | text | not in the schema: `− Expirations` |
| … 3 more | | `schemas.json` |

**Data it reads**: `getWalletLiability` (onLoad, Liability at a glance)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-1164` Wallet Financial Classification & Accounting Mapping: *Wallet Financial Classification & Accounting Mapping*
- → `BO-1165` Wallet Sub-Ledger & Balance Control: *Wallet Sub-Ledger & Balance Control*
- → `BO-1166` Multi-Source Reconciliation Configuration: *Multi-Source Reconciliation Configuration*
- → `BO-1167` Reconciliation Exception & Resolution Workbench: *Reconciliation Exception & Resolution Workbench*
- → `BO-1168` Gift Card Liability Management: *Gift Card Liability Management*
- → `BO-1169` Breakage & Revenue Recognition Policy: *Breakage & Revenue Recognition Policy*
- → `BO-1170` Wallet Financial Period & Closing Controls: *Wallet Financial Period & Closing Controls*
- → `BO-1171` Wallet Analytics & Management Reporting: *Wallet Analytics & Management Reporting*
- → `BO-1172` Finance Validation, Reporting & Audit Center: *Finance Validation, Reporting & Audit Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet finance liability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet finance liability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet finance liability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet finance liability are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1163` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1163`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 1: Opens Wallet Finance & Liability Command Center → Provide Finance and authorized management users with a consolidated financial view of all wallet obligations and movements. Executive KPIs
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F301 branch at step 1 (expected): when Nothing has been set up on Wallet Finance & Liability Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F301 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (66 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1163?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-1164`, `BO-1165`, `BO-1166`, `BO-1167`, `BO-1168`, `BO-1169`, `BO-1170`, `BO-1171`, `BO-1172`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1164` Wallet Financial Classification & Accounting Mapping

**Define the financial classification of every wallet credit and transaction type. Credit Mapping**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure accounting treatment for; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-financial-classification-accounting-mapping-bo-1164` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Cash Credit | select field | — | — | — | — | — | — |
| Refund Credit | select field | — | — | — | — | — | — |
| Gift Card | select field | — | — | — | — | — | — |
| Bonus Credit | select field | — | — | — | — | — | — |
| Promotional Credit | select field | — | — | — | — | — | — |
| Membership Credit | select field | — | — | — | — | — | — |
| Ride Credit | select field | — | — | — | — | — | — |
| F&B Credit | select field | — | — | — | — | — | — |
| Retail Credit | select field | — | — | — | — | — | — |
| Parking Credit | select field | — | — | — | — | — | — |
| Other credits | select field | — | — | — | — | — | — |
| Transaction Mapping | select field | — | — | — | — | — | — |
| Top-Up | select field | — | — | — | — | — | — |
| Redemption | select field | — | — | — | — | — | — |
| Refund | select field | — | — | — | — | — | — |
| Transfer | select field | — | — | — | — | — | — |
| Adjustment | select field | — | — | — | — | — | — |
| Reversal | select field | — | — | — | — | — | — |
| Expiration | select field | — | — | — | — | — | — |
| Gift Card Sale | select field | — | — | — | — | — | — |
| Gift Card Redemption | select field | — | — | — | — | — | — |
| Breakage | select field | — | — | — | — | — | — |
| Mapping Dimensions | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet financial classification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet financial classification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet financial classification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setWalletAccountingMapping` → `WALLET_CONFIGURE` (configure) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1164` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1164`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 2: Works in Wallet Financial Classification & Accounting Mapping → Define the financial classification of every wallet credit and transaction type. Credit Mapping

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1164?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1165` Wallet Sub-Ledger & Balance Control

**Maintain the authoritative financial transaction history behind every wallet balance. Sub-Ledger View**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-sub-ledger-balance-control-bo-1165` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Sub-ledger total** (metric tile, from `getWalletReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| Sub ledger total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**General ledger total** (metric tile, from `getWalletReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| General ledger total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Acquirer total** (metric tile, from `getWalletReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| Acquirer total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Balance exceptions** (data table, from `getWalletReconciliation`): The pack's balance integrity check: any mismatch is a financial exception.

| Shows | Format | Notes |
|---|---|---|
| Pair | chip: Sub ledger vs general ledger, Sub ledger vs acquirer, General ledger vs acquirer | — |
| Difference | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Transactions | list or chips (count when long) | — |
| Likely cause | text | — |

**Sub-ledger entries** (data table): No ledger-entry read is bound to this screen.

| Shows | Format | Notes |
|---|---|---|
| Ledger entry ID | text | not in the schema: `Ledger entry ID` |
| Wallet ID | text | not in the schema: `Wallet ID` |
| Customer / account | text | not in the schema: `Customer / account` |
| Transaction ID | text | not in the schema: `Transaction ID` |
| Transaction type | text | not in the schema: `Transaction type` |
| Credit bucket | text | not in the schema: `Credit bucket` |
| Credit lot | text | not in the schema: `Credit lot` |
| Debit | text | not in the schema: `Debit` |
| Credit | text | not in the schema: `Credit` |
| Currency | text | not in the schema: `Currency` |
| Balance before | text | not in the schema: `Balance before` |
| Balance after | text | not in the schema: `Balance after` |
| Source system | text | not in the schema: `Source system` |
| Venue | text | not in the schema: `Venue` |
| Channel | text | not in the schema: `Channel` |
| Timestamp | text | not in the schema: `Timestamp` |
| Financial status | text | not in the schema: `Financial status` |
| Related transaction | text | not in the schema: `Related transaction` |

**Data it reads**: `getWalletReconciliation` (onLoad, Sub-ledger against the ledger)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet sub-ledger balance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet sub-ledger balance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet sub-ledger balance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet sub-ledger balance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1165` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1165`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 4: Works in Wallet Sub-Ledger & Balance Control → Maintain the authoritative financial transaction history behind every wallet balance. Sub-Ledger View

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1165?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1166` Multi-Source Reconciliation Configuration

**Reconcile wallet financial events across Wallet, Payments, Sales Channels and Finance. The supplied requirements specifically call for reconciliation of payment status between sales channels, the bank/payment gateway and the ticketing system. Reconciliation Sources**

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
| Route | `/orders-money/multi-source-reconciliation-configuration-bo-1166` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Transaction ID | select field | — | — | — | — | — | — |
| Wallet ID | select field | — | — | — | — | — | — |
| Payment reference | select field | — | — | — | — | — | — |
| Order number | select field | — | — | — | — | — | — |
| Amount | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Date | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Terminal | select field | — | — | — | — | — | — |
| External reference | select field | — | — | — | — | — | — |
| Reconciliation Status | select field | — | — | — | — | — | — |
| Matched | select field | — | — | — | — | — | — |
| Partially Matched | select field | — | — | — | — | — | — |
| Unmatched | select field | — | — | — | — | — | — |
| Duplicate | select field | — | — | — | — | — | — |
| Amount Mismatch | select field | — | — | — | — | — | — |
| Currency Mismatch | select field | — | — | — | — | — | — |
| Missing Wallet Entry | select field | — | — | — | — | — | — |
| Missing Payment Entry | select field | — | — | — | — | — | — |
| Reconciliation Frequency | select field | — | — | — | — | — | — |
| Real-time | select field | — | — | — | — | — | — |
| Hourly | select field | — | — | — | — | — | — |
| End of day | select field | — | — | — | — | — | — |
| Scheduled | select field | — | — | — | — | — | — |
| Manual | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |

**Sent by *Save reconciliation sources*** (`setWalletReconciliationSources`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Sources `sources` | repeatable rows | required | — | at least 1 | — | — | `setWalletReconciliationSources` body |
| Kind `sources[].kind` | select | required | — | Wallet ledger · POS · Payment gateway · Payment server · Gift card · Finance | — | — | `setWalletReconciliationSources` body |
| Enabled `sources[].enabled` | toggle | required | on | — | — | — | `setWalletReconciliationSources` body |
| Match keys `sources[].matchKeys` | list of values (chips) | optional | — | — | — | Fields a movement is matched on, e.g. transactionId, authorisationCode, terminalId, amount, businessDate. | `setWalletReconciliationSources` body |
| Tolerance amount `sources[].toleranceAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | A pair differing by no more than this is agreed. Default zero. | `setWalletReconciliationSources` body |
| Schedule `sources[].schedule` | radio group | optional | End of business day | Real time · Hourly · Daily · End of business day | — | — | `setWalletReconciliationSources` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setWalletReconciliationSources` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Wallet Ledger (primary button) | navigation or local | — | — | — | — |
| POS (secondary button) | navigation or local | — | — | — | — |
| Payment Gateway (secondary button) | navigation or local | — | — | — | — |
| Payment Server (secondary button) | navigation or local | — | — | — | — |
| Gift Card (secondary button) | navigation or local | — | — | — | — |
| Finance (secondary button) | navigation or local | — | — | — | — |
| Save reconciliation sources (primary button) | `setWalletReconciliationSources` PUT `/wallet-reconciliation-sources` | WalletReconciliationSources | WalletReconciliationSources | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 `walletLedger` disabled or missing, or a source kind listed twice. | — |

**Data it reads**: `getWalletReconciliation` (onLoad, Three sources compared)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-source reconciliation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-source reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-source reconciliation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `walletLedger` disabled or missing, or a source kind listed twice. |

#### Permissions

- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff
- `setWalletReconciliationSources` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1166` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1166`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 6: Works in Multi-Source Reconciliation Configuration → Reconcile wallet financial events across Wallet, Payments, Sales Channels and Finance. The supplied requirements specifically call for reconciliation of payment status between sales channels, the …

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1166?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Wallet Ledger, POS, Payment Gateway, Payment Server, Gift Card, Finance, Save reconciliation sources.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1167` Reconciliation Exception & Resolution Workbench

**Provide Finance and Operations with a governed workspace to investigate reconciliation failures. Exception Examples Payment successful / Wallet not funded Wallet funded / Payment failed Wallet debited / POS transaction missing Duplicate wallet debit Refund issued / Finance event missing Gift card redeemed / Liability unchanged**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_OPERATE`, `WALLET_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/orders-money/reconciliation-exception-resolution-workbench-bo-1167` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every reconciliation exception resolution** (data table)

| Shows | Format | Notes |
|---|---|---|
| Exception ID | text | not in the schema: `Exception ID` |
| Transaction | text | not in the schema: `Transaction` |
| Wallet | text | not in the schema: `Wallet` |
| Source | text | not in the schema: `Source` |
| Expected amount | text | not in the schema: `Expected amount` |
| Actual amount | text | not in the schema: `Actual amount` |
| Difference | text | not in the schema: `Difference` |
| Currency | text | not in the schema: `Currency` |
| Age | text | not in the schema: `Age` |
| Priority | text | not in the schema: `Priority` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |

**The selected reconciliation exception resolution** (detail panel): The pack groups this record's detail under its own headings: “Workflow”.

| Shows | Format | Notes |
|---|---|---|
| Exception ID | text | not in the schema: `Exception ID` |
| Transaction | text | not in the schema: `Transaction` |
| Wallet | text | not in the schema: `Wallet` |
| Source | text | not in the schema: `Source` |
| Expected amount | text | not in the schema: `Expected amount` |
| Actual amount | text | not in the schema: `Actual amount` |
| Difference | text | not in the schema: `Difference` |
| Currency | text | not in the schema: `Currency` |
| Age | text | not in the schema: `Age` |
| Priority | text | not in the schema: `Priority` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |

**Data it reads**: `getWalletReconciliation` (onLoad, Exceptions to resolve)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reconciliation exception resolution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reconciliation exception resolution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reconciliation exception resolution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reconciliation exception resolution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff
- `adjustWallet` → `WALLET_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.113 | Refund management | Ticketing Catalogue | CONTRACTED | `adjustWallet` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A financial approval centre / controls screen surfaces transactions with exceptions or variances needing review. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-277)*
- Weekly/monthly reconciliation runs ingest → parse → match → classify → auto-resolve, so only genuinely mismatched amounts are shown for human review. *(agreed · MoM 12 Aug 2026, 11. Settlement and Reconciliation Process · DI-258)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1167` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1167`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 8: Works in Reconciliation Exception & Resolution Workbench → Provide Finance and Operations with a governed workspace to investigate reconciliation failures. Exception Examples Payment successful / Wallet not funded Wallet funded / Payment failed Wallet …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1167?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_OPERATE`, `WALLET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1168` Gift Card Liability Management

**Provide detailed financial control of outstanding gift-card obligations. Requirement 4.3.36 explicitly requires reporting of outstanding gift-card balances, redeemed value, unredeemed balances, expired balances and liability exposure by venue, tenant, currency and accounting period. Liability Dashboard**

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
| Route | `/orders-money/gift-card-liability-management-bo-1168` |

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

**Every gift card liability** (data table)

| Shows | Format | Notes |
|---|---|---|
| Gift cards issued | text | not in the schema: `Gift Cards Issued` |
| Original issued value | text | not in the schema: `Original Issued Value` |
| Outstanding value | text | not in the schema: `Outstanding Value` |
| Redeemed value | text | not in the schema: `Redeemed Value` |
| Partially redeemed value | text | not in the schema: `Partially Redeemed Value` |
| Unredeemed value | text | not in the schema: `Unredeemed Value` |
| Expired value | text | not in the schema: `Expired Value` |
| Suspended value | text | not in the schema: `Suspended Value` |
| Breakage | text | not in the schema: `Breakage` |
| Liability exposure | text | not in the schema: `Liability Exposure` |
| Breakdown | text | not in the schema: `Breakdown` |
| Gift card program | text | not in the schema: `Gift card program` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Issuance date | text | not in the schema: `Issuance date` |
| Expiry date | text | not in the schema: `Expiry date` |
| Accounting period | text | not in the schema: `Accounting period` |
| Sales channel | text | not in the schema: `Sales channel` |
| Corporate program | text | not in the schema: `Corporate program` |
| Aging analysis | text | not in the schema: `Aging Analysis` |

**The selected gift card liability** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Gift cards issued | text | not in the schema: `Gift Cards Issued` |
| Original issued value | text | not in the schema: `Original Issued Value` |
| Outstanding value | text | not in the schema: `Outstanding Value` |
| Redeemed value | text | not in the schema: `Redeemed Value` |
| Partially redeemed value | text | not in the schema: `Partially Redeemed Value` |
| Unredeemed value | text | not in the schema: `Unredeemed Value` |
| Expired value | text | not in the schema: `Expired Value` |
| Suspended value | text | not in the schema: `Suspended Value` |
| Breakage | text | not in the schema: `Breakage` |
| Liability exposure | text | not in the schema: `Liability Exposure` |
| Breakdown | text | not in the schema: `Breakdown` |
| Gift card program | text | not in the schema: `Gift card program` |
| Tenant | text | not in the schema: `Tenant` |
| Venue | text | not in the schema: `Venue` |
| Currency | text | not in the schema: `Currency` |
| Issuance date | text | not in the schema: `Issuance date` |
| Expiry date | text | not in the schema: `Expiry date` |
| Accounting period | text | not in the schema: `Accounting period` |
| Sales channel | text | not in the schema: `Sales channel` |
| Corporate program | text | not in the schema: `Corporate program` |
| Aging analysis | text | not in the schema: `Aging Analysis` |

**Data it reads**: `getWalletLiability` (onLoad, Gift card liability)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift card liability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift card liability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gift card liability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gift card liability are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1168` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1168`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 10: Works in Gift Card Liability Management → Provide detailed financial control of outstanding gift-card obligations. Requirement 4.3.36 explicitly requires reporting of outstanding gift-card balances, redeemed value, unredeemed balances …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1168?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1169` Breakage & Revenue Recognition Policy

**Configure the wallet-side business rules for expired/unredeemed gift-card value. Requirement 4.3.37 requires configurable expiration policies, gift-card breakage calculation and generation of revenue- recognition entries according to configured accounting policies. Breakage Configuration**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Gift Card) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/breakage-revenue-recognition-policy-bo-1169` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every breakage revenue recognition** (data table)

| Shows | Format | Notes |
|---|---|---|
| Original value → AED 500 | text | not in the schema: `Original value → AED 500` |
| Redeemed → AED 350 | text | not in the schema: `Redeemed → AED 350` |
| Expired remaining balance → AED 150 | text | not in the schema: `Expired remaining balance → AED 150` |

**The selected breakage revenue recognition** (detail panel): The pack groups this record's detail under its own headings: “Finance approval”, “Instead”.

| Shows | Format | Notes |
|---|---|---|
| Original value → AED 500 | text | not in the schema: `Original value → AED 500` |
| Redeemed → AED 350 | text | not in the schema: `Redeemed → AED 350` |
| Expired remaining balance → AED 150 | text | not in the schema: `Expired remaining balance → AED 150` |

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The breakage revenue recognition list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the breakage revenue recognition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No breakage revenue recognition yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the breakage revenue recognition are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setWalletAccountingMapping` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1169` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1169`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 12: Works in Breakage & Revenue Recognition Policy → Configure the wallet-side business rules for expired/unredeemed gift-card value. Requirement 4.3.37 requires configurable expiration policies, gift-card breakage calculation and generation of …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1169?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1170` Wallet Financial Period & Closing Controls

**Support controlled month-end and financial-period processing for wallet balances. Period Status Open → Closing → Under Review → Closed → Reopened with Authorization Pre-Close Validation Unreconciled transactions Pending refunds Pending reversals Pending adjustments Negative balances Missing accounting mappings Failed integrations Unprocessed expirations Gift-card breakage candidates Pending approvals Closing Snapshot**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_VIEW`, `WALLET_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-financial-period-closing-controls-bo-1170` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Opening liability | select field | — | — | — | — | — | — |
| Funding | select field | — | — | — | — | — | — |
| Credits issued | select field | — | — | — | — | — | — |
| Redemption | select field | — | — | — | — | — | — |
| Refunds | select field | — | — | — | — | — | — |
| Transfers | select field | — | — | — | — | — | — |
| Adjustments | select field | — | — | — | — | — | — |
| Expiration | select field | — | — | — | — | — | — |
| Breakage | select field | — | — | — | — | — | — |
| Closing liability | select field | — | — | — | — | — | — |
| Controls | select field | — | — | — | — | — | — |
| Close by tenant | select field | — | — | — | — | — | — |
| Close by venue | select field | — | — | — | — | — | — |
| Close by currency | select field | — | — | — | — | — | — |
| Lock financial period | select field | — | — | — | — | — | — |
| Reopen with approval | select field | — | — | — | — | — | — |
| Carry exceptions forward | select field | — | — | — | — | — | — |
| Export close package | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Legal entity | picker: choose a legal entity | — | — | `listFiscalPeriods` ?legalEntityId |
| Status | segmented control | — | Open · Closing · Closed | `listFiscalPeriods` ?status |
| As of | date picker | — | — | `getWalletLiability` ?asOf |
| Group by | radio group | — | Credit type · Wallet type · Venue · Age band | `getWalletLiability` ?groupBy |

#### Outputs: what the screen shows and produces

**Data it reads**: `listFiscalPeriods` (onLoad, The period being closed); `getWalletLiability` (onLoad, Closing balance)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet financial period configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet financial period untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet financial period configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listFiscalPeriods` → `LEDGER_VIEW` (read) · staff
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1170` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1170`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 14: Works in Wallet Financial Period & Closing Controls → Support controlled month-end and financial-period processing for wallet balances. Period Status Open → Closing → Under Review → Closed → Reopened with Authorization Pre-Close Validation Unreconciled …

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1170?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1171` Wallet Analytics & Management Reporting

**Provide comprehensive analytics for wallet usage, financial performance and customer behavior. Requirement 4.3.17 requires intensive reporting across wallet credit types, including usage, balance and expiry, while 4.3.33 calls for dashboards covering balances, top-ups, redemptions, refunds, outstanding liability, expired value, usage by channel and transaction volume. Financial Analytics Wallet Liability Outstanding Stored Value Funding Redemption Refunds Transfers Expired Value Breakage Gift Card Liability Operational Analytics Active wallets Average wallet balance Average top-up Average spend Transaction volume Wallet usage frequency Dormant wallets Credit utilization Channel Analytics**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare; Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/wallet-analytics-management-reporting-bo-1171` |

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

**Every wallet analytics reporting** (data table)

| Shows | Format | Notes |
|---|---|---|
| POS | text | not in the schema: `POS` |
| Mobile app | text | not in the schema: `Mobile App` |
| B2 c | text | not in the schema: `B2C` |
| Kiosk | text | not in the schema: `Kiosk` |
| Wearables | text | not in the schema: `Wearables` |
| API | text | not in the schema: `API` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Attractions | text | not in the schema: `Attractions` |
| Customer analytics | text | not in the schema: `Customer Analytics` |
| Individual | text | not in the schema: `Individual` |
| Family | text | not in the schema: `Family` |
| Membership | text | not in the schema: `Membership` |
| Corporate | text | not in the schema: `Corporate` |
| Employee | text | not in the schema: `Employee` |
| Guest | text | not in the schema: `Guest` |
| AI insights | text | not in the schema: `AI Insights` |

**The selected wallet analytics reporting** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| POS | text | not in the schema: `POS` |
| Mobile app | text | not in the schema: `Mobile App` |
| B2 c | text | not in the schema: `B2C` |
| Kiosk | text | not in the schema: `Kiosk` |
| Wearables | text | not in the schema: `Wearables` |
| API | text | not in the schema: `API` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Attractions | text | not in the schema: `Attractions` |
| Customer analytics | text | not in the schema: `Customer Analytics` |
| Individual | text | not in the schema: `Individual` |
| Family | text | not in the schema: `Family` |
| Membership | text | not in the schema: `Membership` |
| Corporate | text | not in the schema: `Corporate` |
| Employee | text | not in the schema: `Employee` |
| Guest | text | not in the schema: `Guest` |
| AI insights | text | not in the schema: `AI Insights` |

**Data it reads**: `getWalletLiability` (onLoad, Management reporting)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet analytics reporting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet analytics reporting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet analytics reporting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet analytics reporting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getWalletLiability` → `WALLET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Wallet spend reported by department/category (F&B, attractions, retail, partners) and by channel (B2C, POS); payment/redemption policy can set rules such as a minimum spend to use the wallet as a payment method. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-534)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1171` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1171`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 16: Works in Wallet Analytics & Management Reporting → Provide comprehensive analytics for wallet usage, financial performance and customer behavior. Requirement 4.3.17 requires intensive reporting across wallet credit types, including usage, balance and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1171?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-1172` Finance Validation, Reporting & Audit Center

**Provide a final finance-control screen for validating wallet financial integrity and reviewing all financial configuration changes. Finance Health Check Complete the TICVAI Wallet module with the enterprise integration and governance layer that allows Wallet to operate securely across the entire TICVAI ecosystem and with approved third-party platforms. This board covers Wallet APIs, integration profiles, event/webhook orchestration, synchronization, integration monitoring, access/security governance, configuration versioning, approval and publication, audit governance, and end-to-end platform health. It directly addresses requirements 4.3.20 and 4.3.34, while consolidating governance and administration capabilities required across the full wallet scope. The source specifically requires integration with internal and external systems through APIs, including balance inquiry, transaction history, wallet funding, wallet payment, refund processing and wallet-to-wallet transfers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `LEDGER_VIEW`, `WALLET_VIEW` (1 operate, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare) and no metric row |
| Offline | online only |
| Opens with | `periodId` (navigation) |
| Route | `/orders-money/finance-validation-reporting-audit-center-bo-1172` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getWalletReconciliation` ?from |
| To | date picker | — | — | `getWalletReconciliation` ?to |
| Legal entity | picker: choose a legal entity | — | — | `listFiscalPeriods` ?legalEntityId |
| Status | segmented control | — | Open · Closing · Closed | `listFiscalPeriods` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every finance validation reporting** (data table)

| Shows | Format | Notes |
|---|---|---|
| Sum of customer wallet balances | text | not in the schema: `Sum of Customer Wallet Balances` |
| Against | text | not in the schema: `against` |
| Wallet sub ledger liability | text | not in the schema: `Wallet Sub-Ledger Liability` |
| Finance interface control total | text | not in the schema: `Finance Interface Control Total` |
| Configuration audit | text | not in the schema: `Configuration Audit` |

**The selected finance validation reporting** (detail panel): The pack groups this record's detail under its own headings: “Validate”, “Record changes to”, “For every change record”, “So we now have”, “Administration”.

| Shows | Format | Notes |
|---|---|---|
| Sum of customer wallet balances | text | not in the schema: `Sum of Customer Wallet Balances` |
| Against | text | not in the schema: `against` |
| Wallet sub ledger liability | text | not in the schema: `Wallet Sub-Ledger Liability` |
| Finance interface control total | text | not in the schema: `Finance Interface Control Total` |
| Configuration audit | text | not in the schema: `Configuration Audit` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run Finance Validation (primary button) | navigation or local | — | — | — | — |
| Review Exceptions (secondary button) | navigation or local | — | — | — | — |
| Submit Close (secondary button) | navigation or local | — | — | — | — |
| Approve Close (secondary button) | navigation or local | — | — | — | — |
| Generate Liability Report (secondary button) | navigation or local | — | — | — | — |
| Generate Reconciliation Report (secondary button) | navigation or local | — | — | — | — |
| Export Audit (secondary button) | navigation or local | — | — | — | — |
| Send to Finance (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getWalletReconciliation` (onLoad, Validation and audit); `listFiscalPeriods` (onLoad, The fiscal periods to begin closing or close)

**Where the user goes next**

- → `BO-1163` Wallet Finance & Liability Command Center: *Back to Wallet Finance & Liability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The finance validation reporting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the finance validation reporting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No finance validation reporting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the finance validation reporting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The period is already `closed`, or one or more of the close checks failed. The checks are exactly the values of `PeriodCloseResult.checks[].check` … (PeriodCloseProblem); 409 The period is not `open`. |

#### Permissions

- `getWalletReconciliation` → `WALLET_VIEW` (read) · staff
- `getUnifiedReconciliation` → `LEDGER_VIEW` (read) · staff
- `beginPeriodClose` → `LEDGER_APPROVE` (operate) · staff
- `closeFiscalPeriod` → `LEDGER_APPROVE` (operate) · staff
- `getWalletLiability` → `WALLET_VIEW` (read) · staff
- `listFiscalPeriods` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.89 | The system shall support fiscal year management, fiscal periods, month-end and year-end closing. Authorized users shall be able to open, close, lock, unlock, and re-open accounting periods with … | F&B & Guest Management | CONTRACTED | `closeFiscalPeriod` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A financial approval centre / controls screen surfaces transactions with exceptions or variances needing review. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-277)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1172` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS194 Wallet Configuration Backend Structure v1.0 Board 9.dc.html#bo-1172`
- Workshop pack: Wallet_Configuration_Backend_Structure_v1.0.pdf board 9
- Flow F301 *Wallet Configuration Backend Structure v1.0 board 9: Wallet Finance & Liability …*, step 18: Works in Finance Validation, Reporting & Audit Center → Provide a final finance-control screen for validating wallet financial integrity and reviewing all financial configuration changes. Finance Health Check

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1172?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run Finance Validation, Review Exceptions, Submit Close, Approve Close, Generate Liability Report, Generate Reconciliation Report, Export Audit, Send to Finance.
- [ ] Every transition is wired: `BO-1163`.
- [ ] Every gated control is gated: `LEDGER_APPROVE`, `LEDGER_VIEW`, `WALLET_VIEW`.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"adjustWallet": {"method":"POST","path":"/wallets/{subjectId}/adjust","contract":"wallet","summary":"Manually adjust a wallet balance","permission":"WALLET_OPERATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"beginPeriodClose": {"method":"POST","path":"/fiscal-periods/{periodId}/begin-close","contract":"finance","summary":"Begin closing a period","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FiscalPeriod"},
"closeFiscalPeriod": {"method":"POST","path":"/fiscal-periods/{periodId}/close","contract":"finance","summary":"Close a period and lock postings","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PeriodCloseResult"},
"getUnifiedReconciliation": {"method":"GET","path":"/reconciliation/unified","contract":"finance","summary":"Every money source against the ledger, in one view","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"UnifiedReconciliation"},
"getWalletLiability": {"method":"GET","path":"/wallet-liability","contract":"wallet","summary":"What is outstanding, and what is breakage","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"asOf","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"WalletLiabilityRow"},
"getWalletReconciliation": {"method":"GET","path":"/wallet-reconciliation","contract":"wallet","summary":"The wallet sub-ledger against the general ledger and the acquirer","permission":"WALLET_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"WalletReconciliation"},
"listFiscalPeriods": {"method":"GET","path":"/fiscal-periods","contract":"finance","summary":"List fiscal periods","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setWalletAccountingMapping": {"method":"PUT","path":"/wallet-accounting","contract":"wallet","summary":"Which ledger account each credit type sits in","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletAccountingMapping","responds":"WalletAccountingMapping"},
"setWalletReconciliationSources": {"method":"PUT","path":"/wallet-reconciliation-sources","contract":"wallet","summary":"Which sources the wallet reconciles against, matched how, and when","permission":"WALLET_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"WalletReconciliationSources","responds":"WalletReconciliationSources"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"FiscalPeriod": {"x-ticvai-persistence":"ledger.fiscal_period + ledger.fiscal_period_event","type":"object","description":"`startDate` and `endDate` are days in the region's time zone: a posting belongs to the period when its `postedAt`, in that zone, falls on or between them.\n","required":["id","legalEntityId","name","startDate","endDate","status"],"properties":{"id":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid"},"name":{"type":"string"},"startDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"endDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"status":{"$ref":"#/components/schemas/PeriodStatus"},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"closedAt":{"type":"string","format":"date-time","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The approval request a close or reopen is waiting on (`approvals`), routed to a finance approver (decided 28 September, audit R144). Null when nothing is waiting."},"events":{"type":"array","description":"**Every step of the period's close, oldest first**: begin, abandon, close and reopen, each with who, when and (for abandon and reopen) why. A reopened period restates figures somebody has already reported, so the reason is kept, not just the latest status.\n","items":{"$ref":"#/components/schemas/FiscalPeriodEvent"}}}},
"FiscalPeriodEvent": {"type":"object","description":"One step in a fiscal period's close. Written by the operation that took the step; never edited.","required":["action","principalId","occurredAt"],"properties":{"action":{"type":"string","enum":["beginClose","abandonClose","close","reopen"]},"reason":{"type":"string","nullable":true,"description":"Required by `abandonPeriodClose` and `reopenPeriod`; null for the other steps."},"principalId":{"type":"string","format":"uuid","description":"Who took the step."},"approverPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The approver of a `reopen`. Null for the other steps."},"occurredAt":{"type":"string","format":"date-time"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PeriodCloseResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["fiscalPeriodId","dryRun","passed","checks"],"properties":{"fiscalPeriodId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"passed":{"type":"boolean"},"checks":{"type":"array","items":{"type":"object","required":["check","passed"],"properties":{"check":{"type":"string","enum":["trialBalanceBalances","noUnapprovedJournals","noOpenShifts","settlementsReconciled","recognitionRunComplete","priorPeriodClosed","varianceExceptionsReviewed"]},"passed":{"type":"boolean"},"detail":{"type":"string"},"blockingCount":{"type":"integer"}}}}}},
"PeriodStatus": {"type":"string","enum":["open","closing","closed"]},
"UnifiedReconciliation": {"type":"object","description":"4.2.19. **Four sources and the variances between them.** A view showing each balanced against itself has not reconciled anything.\n","properties":{"from":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"to":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"sources":{"type":"array","items":{"type":"object","properties":{"source":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]},"providerName":{"type":"string","nullable":true},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transactionCount":{"type":"integer"}}}},"variances":{"type":"array","description":"**Where two sources disagree, named.** A discrepancy is usually the gap between two of them rather than inside one, and *\"out by 240\"* without saying between what is not actionable.\n","items":{"type":"object","properties":{"between":{"type":"array","description":"The two sources that disagree, as named in `sources[].source`.","minItems":2,"maxItems":2,"items":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]}},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"likelyCause":{"type":"string","nullable":true}}}}}},
"Wallet": {"x-ticvai-persistence":"wallet.wallet + wallet.credit_lot","type":"object","required":["subjectId","balance","currency","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credits":{"type":"array","description":"4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n","items":{"type":"object","required":["kind","amount"],"properties":{"kind":{"type":"string","enum":["cash","bonus","redemption","refund","goodwill"],"description":"**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n","x-ticvai-persisted":false},"amount":{"x-ticvai-column":"remaining_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceRef":{"type":"string","nullable":true,"x-ticvai-column":"source_reference"},"isRefundable":{"type":"boolean","default":false,"x-ticvai-persisted":false,"description":"**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"}}}},"bonusBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Promotional value. Typically non-refundable and spent first."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"status":{"type":"string","enum":["active","suspended","closed"]},"homeCellName":{"type":"string","nullable":true,"description":"Where the authoritative balance lives. Present when the guest is linked across cells.\n"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"lastActivityAt":{"type":"string","format":"date-time","nullable":true}}},
"WalletAccountingMapping": {"type":"object","x-ticvai-persistence":"wallet.accounting_mapping","description":"Boards 9.2 and 9.3. **Different credit types are different liabilities.**","properties":{"mappings":{"type":"array","items":{"type":"object","properties":{"creditTypeId":{"type":"string","format":"uuid"},"liabilityAccountCode":{"type":"string"},"breakageRevenueAccountCode":{"type":"string","nullable":true},"costAccountCode":{"type":"string","nullable":true,"description":"**For credit the venue gave away.** Promotional credit is a marketing cost already incurred, not money owed back, and booking it as a liability overstates what the venue owes by whatever marketing did last quarter.\n"}}}},"breakagePolicy":{"type":"object","properties":{"recogniseAfterMonths":{"type":"integer","nullable":true,"description":"**Recognised on a policy, not on the expiry date.** Some jurisdictions require the liability to be held long after the printed expiry.\n"},"requiresApproval":{"type":"boolean","default":true}}},"scopePath":{"type":"string"}}},
"WalletLiabilityRow": {"type":"object","description":"Boards 9.5 and 9.6. **The number the finance director asks for.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"outstanding":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expiringThisPeriod":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageRecognised":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"walletCount":{"type":"integer"},"oldestLotAt":{"type":"string","format":"date","nullable":true}}},
"WalletReconciliation": {"type":"object","description":"Board 9.4. **Three sources, and the exception names which pair disagrees.**","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"subLedgerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"generalLedgerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquirerTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exceptions":{"type":"array","items":{"type":"object","properties":{"pair":{"type":"string","enum":["subLedgerVsGeneralLedger","subLedgerVsAcquirer","generalLedgerVsAcquirer"]},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transactionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"likelyCause":{"type":"string","nullable":true}}}}}},
"WalletReconciliationSources": {"type":"object","x-ticvai-persistence":"wallet.reconciliation_source","description":"Board 9, p.105. **What `getWalletReconciliation` compares.** `walletLedger` is always on.","required":["sources"],"properties":{"sources":{"type":"array","minItems":1,"items":{"type":"object","required":["kind","enabled"],"properties":{"kind":{"type":"string","enum":["walletLedger","pos","paymentGateway","paymentServer","giftCard","finance"]},"enabled":{"type":"boolean","default":true},"matchKeys":{"type":"array","description":"Fields a movement is matched on, e.g. transactionId, authorisationCode, terminalId, amount, businessDate.","items":{"type":"string"}},"toleranceAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"A pair differing by no more than this is agreed. Default zero."},"schedule":{"type":"string","enum":["realTime","hourly","daily","endOfBusinessDay"],"default":"endOfBusinessDay"}}}},"scopePath":{"type":"string"}}}
}
```
