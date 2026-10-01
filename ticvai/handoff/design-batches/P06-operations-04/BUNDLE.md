# P06-operations-04 — P06 · Operations (4 of 5)

**10 screens · 25 operations · 33 schemas · 9 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `AI_USE, ANNOUNCEMENT_PUBLISH, ASSET_LIBRARY_VIEW, DEVICE_CONFIGURE, DEVICE_VIEW, ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **12 of these operations work offline**: acknowledgeAnnouncement, addTip, createPayment, getCurrentSession, getMediaAsset, getMediaEntitlements, listAnnouncements, listDevices
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `EMP-035` | Payment on device | B–D | 25 | 0 | 5 | 10 | 2 | 0 | — | notStarted (generated) |
| `EMP-036` | Issue media | B–D | 8 | 23 | 5 | 23 | 1 | 0 | — | notStarted (generated) |
| `EMP-037` | Notifications | B–D | 12 | 29 | 6 | 5 | 2 | 0 | — | notStarted (generated) |
| `EMP-039` | Announcements | B–D | 12 | 29 | 6 | 4 | 1 | 0 | — | notStarted (generated) |
| `EMP-038` | Broadcast to team | B–D | 12 | 29 | 6 | 4 | 0 | 0 | — | notStarted (generated) |
| `EMP-040` | Knowledge base | B–D | 6 | 0 | 5 | 2 | 0 | 0 | — | notStarted (generated) |
| `EMP-041` | Training | B–D | 3 | 16 | 6 | 2 | 0 | 0 | — | notStarted (generated) |
| `EMP-042` | Profile | B–D | 3 | 33 | 5 | 3 | 0 | 0 | — | notStarted (generated) |
| `EMP-043` | Device settings | B–D | 15 | 28 | 6 | 48 | 0 | 0 | — | notStarted (generated) |
| `EMP-044` | Accessibility | B–D | 0 | 0 | 4 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**EMP-036, EMP-041, EMP-044 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-035` Payment on device

**Take a card payment on the handheld.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_MODIFY` (2 operate); in the flows as cashier |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`createPayment`, `inquirePaymentStatus`, `addTip`) and no read of a population — it is settings, not a list |
| Offline | Not available for card |
| Opens with | `paymentId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/payment-on-device` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. Card on a handheld. **Tender currency equals base currency** — a staff member taking payment away from a till has no float and cannot accept foreign cash.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `CreatePaymentRequest.id` |
| orderId | picker: choose an order (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `CreatePaymentRequest.orderId` |
| tender | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). | `CreatePaymentRequest.tender` |
| amount | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `CreatePaymentRequest.amount` |
| tenderedAmount | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `CreatePaymentRequest.tenderAmount` |
| walletAuthorisationId | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `CreatePaymentRequest.walletAuthorisationId` |
| deviceId | picker: choose a device (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `CreatePaymentRequest.deviceId` |
| recordedAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `CreatePaymentRequest.recordedAt` |

**Form: Add tip** (modal, opened by *Add tip*; *Add tip* calls `addTip`, *Cancel* sends nothing)

**Collects what `addTip` sends before it is called.** Required: `amount`, `source`, `recordedAt`. Optional: `allocateToPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `addTip` body |
| Source `source` | radio group | required | — | Terminal prompt · Cashier entered · Guest app · Service charge | — | `serviceCharge` is not a tip and is separated deliberately — it is revenue in most jurisdictions, and pooling it with tips is how a payroll dispute starts. | `addTip` body |
| Allocate to principal `allocateToPrincipalId` | picker: choose an allocate to principal | optional | — | — | shows names, sends the id | Where the venue allocates rather than pools. | `addTip` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addTip` body |

Errors to draw in the form: 409 Payment not settled — not yet `captured` (`notCaptured`) — or a tip is already recorded against it (`tipAlreadyRecorded`). (PaymentProblem)

**Form: Capture payment** (modal, opened by *Capture payment*; *Capture payment* calls `capturePayment`, *Cancel* sends nothing)

**Collects what `capturePayment` sends before it is called.** Required: `amount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `capturePayment` body |

Errors to draw in the form: 402 Capture refused by the issuer (`providerDeclined`); the payment moves to `declined` (states/payment.yaml). (PaymentProblem); 409 Only an `authorised` payment is captured (`notAuthorised`). The amount may not exceed what was authorised (`aboveAuthorisedAmount`), and less than that is … (PaymentProblem)

**Sent by *Create payment*** (`createPayment`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `createPayment` body |
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createPayment` body |
| Tender `tender` | select | required | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createPayment` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPayment` body |
| Tender currency `tenderCurrency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. | `createPayment` body |
| Tender amount `tenderAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `createPayment` body |
| Wallet authorisation `walletAuthorisationId` | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `createPayment` body |
| Wallet hold `walletHoldId` | picker: choose a wallet hold | optional | — | — | shows names, sends the id | For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table. | `createPayment` body |
| Return URL `returnUrl` | URL field | optional | — | — | https:// | Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). | `createPayment` body |
| Terminal `terminalId` | picker: choose a terminal | optional | — | — | shows names, sends the id | The card terminal to instruct, for a card payment at a till (ECR flow, SD-034). | `createPayment` body |
| Device `deviceId` | picker: choose a device | optional | — | — | shows names, sends the id | — | `createPayment` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPayment` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create payment (primary button) | `createPayment` POST `/payments` | CreatePaymentRequest | Payment | 402 Declined by the provider (`providerDeclined`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a guest channel sent a tender … | emits `payment.captured`, `order.paid`; works offline |
| Inquire payment status (secondary button) | `inquirePaymentStatus` POST `/payments/{paymentId}/inquiry` | — | Payment | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Add tip (secondary button) | `addTip` POST `/payments/{paymentId}/tip` | inline | Payment | 409 Payment not settled — not yet `captured` (`notCaptured`) — or a tip is already recorded against it (`tipAlreadyRecorded`). (PaymentProblem) | works offline; opens modal first |
| Capture payment (secondary button) | `capturePayment` POST `/payments/{paymentId}/capture` | inline | Payment | 402 Capture refused by the issuer (`providerDeclined`); the payment moves to `declined` (states/payment.yaml). (PaymentProblem); 409 Only an `authorised` payment is captured (`notAuthorised`). The amount may not exceed … | emits `payment.captured`, `order.paid`; opens modal first |

**Where the user goes next**

- → `EMP-036` Issue media: *Media is issued on the spot*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved payment device. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment device untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment device configured. The form opens empty and `createPayment` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_CREATE`, which `createPayment` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Not available for card |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Only an `authorised` payment is captured (`notAuthorised`). The amount may not exceed what was authorised (`aboveAuthorisedAmount`), and less than that is … (PaymentProblem); 409 Payment not settled — not yet `captured` (`notCaptured`) — or a tip is already recorded against it (`tipAlreadyRecorded`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds … |

#### Permissions

- `createPayment` → `ORDER_CREATE` (operate) · staff, guest, partner
- `inquirePaymentStatus` → `ORDER_CREATE` (operate) · staff, guest, partner
- `addTip` → `ORDER_MODIFY` (operate) · staff, partner
- `capturePayment` → `ORDER_CREATE` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `ORDER_CREATE`, which `createPayment` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.23 | Payment can be done online. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.12.35 | System shall support multiple payment methods within a single transaction including cash, credit card, wallet, loyalty points, vouchers, gift cards, bank transfers, and credit balances. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.13.2 | The operator can register the payment. | Ticketing Sales | CONTRACTED | `createPayment` |
| 2.15.3 | The operator can register the payment and print the pass. | Ticketing Sales | CONTRACTED | `createPayment` |
| 4.2.6 | The system should be able to accept several currencies in one transaction (a guest pays in USD and gets the change in AED). | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.7 | The system should be accept multiple payments in one transaction. For example, there must be an option to split the payment within a group of guests | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.13 | The system should be able to support payment of one transaction with multiple payment methods. | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.2.22 | The system shall support mixed payment scenarios using any combination of loyalty points, wallet balances, gift cards, vouchers, cash, and payment cards within the same transaction. | Bundles and Promotions | CONTRACTED | `createPayment` |
| 4.6.27 | Support mobile payment for F&B and retail orders. | Bundles and Promotions | CONTRACTED | `createPayment` |
| 2.6.25 | No ticket can be issued until the payment has been done. | Ticketing Sales | CONTRACTED | `capturePayment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Apple Pay / Google Pay tap-to-pay are the primary regional digital payment methods; UPI-style QR payments may come later, not in initial scope. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-079)*
- Only cash payments are available while offline; card payment requires connectivity. *(agreed · MoM 31 Jul 2026, 12. Payments & Regional Preferences · DI-078)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-035` · status **notStarted** · provenance generated
- Flow F66 *A walk-up sale is taken on a handheld*, step 2: The guest taps a card on the device. → **`inquirePaymentStatus` exists because a handheld payment fails differently** — a card reader out of range does not report cleanly, and asking is safer than assuming.
- Flow F66 branch at step 2 (high): when The payment status is unknown — the reader lost signal mid-tap., **`inquirePaymentStatus` before retrying, always.** Retrying a payment that actually succeeded charges a guest twice, and on a handheld that is the common failure.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (402, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-035?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create payment, Inquire payment status, Add tip, Capture payment.
- [ ] Every transition is wired: `EMP-036`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_MODIFY`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-036` Issue media

**Give the guest something the gate can read.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_VIEW` (2 read, 1 operate); in the flows as cashier |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getMediaEntitlements` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | Issues from the local range allocated at shift start |
| Opens with | `mediaCode` (deepLink), `mediaId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/issue-media` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **9 assets operations removed 18 August (CF-114).** The whole media contract was attached to this screen. **A till adding an item to a ticket does not manage a media library** — it reads the asset it needs and nothing else. Same shape as CF-87, one level up: that attached sibling operations, this attached a whole contract.

#### Inputs: what the user enters or picks

**Form: Append entitlement to media** (modal, opened by *Append entitlement to media*; *Append entitlement to media* calls `appendEntitlementToMedia`, *Cancel* sends nothing)

**Collects what `appendEntitlementToMedia` sends before it is called.** Required: `id`, `lines`, `recordedAt`. Optional: `paymentMethod`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header. | `appendEntitlementToMedia` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `appendEntitlementToMedia` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `appendEntitlementToMedia` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `appendEntitlementToMedia` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `appendEntitlementToMedia` body |
| Payment method `paymentMethod` | radio group | optional | — | Card · Cash · Wallet · Gift card · Charge to account | — | — | `appendEntitlementToMedia` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `appendEntitlementToMedia` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `appendEntitlementToMedia` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media … (AppendRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The media entitlements** (detail panel, from `getMediaEntitlements`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Media kind | chip: QR, Wristband, Card, NFC, Mobile pass | — |
| Subject | the name it points at, never the id | — |
| Is valid | yes / no (icon or chip) | — |
| Invalid reason | text | — |
| Can accept more | yes / no (icon or chip) | False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after. |
| Entitlements | list or chips (count when long) | — |

**The media asset** (detail panel, from `getMediaAsset`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | — |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Description | in the reader's language | Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored. |
| Alt text | in the reader's language | Required before use in a guest-facing surface. WCAG 2.2 AA. |
| Width | 1,234 | — |
| Height | 1,234 | — |
| Duration seconds | 1,234.5 | — |
| Custom metadata | grouped details | BL-178. `assets` is a strong contract and its metadata was fixed — kind, title, alt text, dimensions, rights. |
| Shared with tenants | list or chips (count when long) | BL-178. Cross-tenant sharing, and it is refused by default for a reason. |
| Tags | list or chips (count when long) | — |
| Venue | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Append entitlement to media (primary button) | `appendEntitlementToMedia` POST `/media/{mediaCode}/entitlements` | AppendEntitlementRequest | AppendEntitlementResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or … | opens modal first; produces a document or message: Add something to a ticket the guest already holds |

**Data it reads**: `getMediaEntitlements` (onLoad, What is already on this media); `getMediaAsset` (onLoad, Read an asset with derivatives and usage)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The issue media, read by `getMediaEntitlements`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the issue media untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No issue media yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Issues from the local range allocated at shift start |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media … (AppendRefusedProblem) |

#### Permissions

- `getMediaEntitlements` → `ORDER_VIEW` (read) · staff
- `appendEntitlementToMedia` → `ORDER_CREATE` (operate) · staff
- `getMediaAsset` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

23 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.11 | Ticket Storage - System shall store digital tickets. | Guest Mobile App & Branding | CONTRACTED | `getMediaEntitlements` |
| 2.6.18 | - Dynamic QR code | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.7.24 | The BtoB Customer can also receive simple QR Codes, vouchers or packaged PLUs. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.13.3 | Tickets can be issued and sent either by email (PDF or M-ticket, E-ticket). | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.14.16 | Generate digital cards with QR/NFC/barcode. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.16.2 | The system should support multiple media types for a ticket. Expected formats: - Paper/thermal tickets with QR, Barcode, RFID - Print at home tickets with QR, Barcode - Smartphones: NFC (near-field … | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.16.17 | The system shall allow multiple media types to be linked to the same guest account and entitlement simultaneously, including QR tickets, RFID wristbands, membership cards, and mobile wallets. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 3.1.1 | Dynamic QR Code Supports: 1. Registration: Customers select "Digital Ticket" via the confirmation page, email, or ticket PDF to begin the enrollment process. 2.Activation: After registration, the … | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.1.2 | Unique Code per Ticket: Generate a unique QR code for every issued ticket or pass. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.1.7 | Dynamic QR technology shall support memberships, annual passes, loyalty accounts, wallets, and other digital credentials in addition to standard tickets. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.2.63 | It is expected that the access code created by the system is unique and randomized to improve fraud prevention. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 5.4.18 | Provide digital loyalty card in app. | F&B & Guest Management | CONTRACTED | `getMediaEntitlements` |
| … 11 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Media swap: zero-value transaction converting a ticket's media on-site, e.g. scanning an online QR at a kiosk to issue a physical wristband instead. *(client request · MoM 2 Sep 2026, 4.9 Media swap · DI-637)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-036` · status **notStarted** · provenance generated
- Flow F66 *A walk-up sale is taken on a handheld*, step 3: Media is issued on the spot. → **Issued to a wristband or a phone, not printed.** A roaming seller has no printer, which is why this path exists at all.
- Flow F66 branch at step 3 (medium): when The guest has no phone and no wristband., Directed to a window for printed media. **A roaming sale that cannot deliver is a sale that should not have been taken.**

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-036?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Append entitlement to media.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-037` Notifications

**Tell the right person the right thing.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act |
| Offline | Cached, with age. Acknowledgements queue |
| Opens with | `announcementId` (deepLink), `conversationId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/notifications` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Unacknowledged only | toggle | optional | — | — | — | Sends `?unacknowledgedOnly=` to `listAnnouncements`. | `listAnnouncements` ?unacknowledgedOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Unread only | toggle | off | — | `listStaffConversations` ?unreadOnly |

**Form: Publish announcement** (modal, opened by *Publish announcement*; *Publish announcement* calls `publishAnnouncement`, *Cancel* sends nothing)

**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text field | required | — | max length 140 | — | — | `publishAnnouncement` body |
| Body `body` | text area | required | — | max length 4000 | — | — | `publishAnnouncement` body |
| Kind `kind` | radio group | required | — | Operational · Safety · Emergency · Hr · Celebration | — | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission. | `publishAnnouncement` body |
| Venues `venueIds` | multi-picker: choose venues | optional | — | — | — | — | `publishAnnouncement` body |
| Departments `departmentIds` | multi-picker: choose departments | optional | — | — | — | — | `publishAnnouncement` body |
| Roles `roleIds` | multi-picker: choose roles | optional | — | — | — | — | `publishAnnouncement` body |
| Requires acknowledgement `requiresAcknowledgement` | toggle | optional | — | — | — | — | `publishAnnouncement` body |
| Delivery channels `deliveryChannels` | multi-select chips | optional | In app, Push | In app · Push | — | How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). | `publishAnnouncement` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Published at `publishedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Locale `locale` | text field | optional | — | — | — | — | `publishAnnouncement` body |

Errors to draw in the form: 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type …

#### Outputs: what the screen shows and produces

**Shown**

**Every announcement** (data table, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The selected announcement** (detail panel, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The announcement reach** (detail panel, from `getAnnouncementReach`)

| Shows | Format | Notes |
|---|---|---|
| Announcement | the name it points at, never the id | — |
| Targeted | 1,234 | — |
| Delivered | 1,234 | — |
| Acknowledged | 1,234 | — |
| Outstanding | list or chips (count when long) | The list that matters. For an operational notice it measures whether anyone read it; during an emergency it is the roll call. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Acknowledge announcement (primary button) | `acknowledgeAnnouncement` POST `/announcements/{announcementId}/acknowledge` | — | — | — | works offline |
| Publish announcement (secondary button) | `publishAnnouncement` POST `/announcements` | Announcement | Announcement | 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type … | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listAnnouncements` (onLoad, What staff have been told); `listStaffConversations` (onLoad, My conversations with colleagues, unread first)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The notifications list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the notifications untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No notifications yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on unacknowledgedOnly and the notifications are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached, with age. Acknowledgements queue |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Neither conversationId nor recipientPrincipalIds, a recipient who is not staff of the caller's venue, or a group over 50 participants |

#### Permissions

- `listAnnouncements` → `WORKFORCE_VIEW` (read) · staff
- `acknowledgeAnnouncement` → `WORKFORCE_VIEW` (read) · staff
- `getAnnouncementReach` → `WORKFORCE_VIEW` (read) · staff
- `publishAnnouncement` → `ANNOUNCEMENT_PUBLISH` (configure) · staff
- `listStaffConversations` → `WORKFORCE_VIEW` (read) · staff
- `listStaffMessages` → `WORKFORCE_VIEW` (read) · staff
- `sendStaffMessage` → `WORKFORCE_VIEW` (read) · staff
- `markStaffConversationRead` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.66 | System shall send assignment and schedule notifications. | Ticketing Catalogue | CONTRACTED | `publishAnnouncement` |
| 18.1.5 | Push Notifications - System shall support push notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.3 | Announcements - Users shall receive announcements. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.4 | Emergency Alerts - Users shall receive emergency notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.5 | Internal Messaging - Users shall receive operational communications. | Employee Mobile App & AI Assistant | CONTRACTED | `sendStaffMessage` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Real-time health view of device connectivity. Device-pushed events (anti-passback attempts, power loss, network loss) are surfaced as alerts and reports, e.g. notifying the operations team when a turnstile goes offline. *(agreed · MoM 2 Sep 2026, 4.1 / 4.2 Health Monitoring & Alerts · DI-625)*
- Notifications categorised by type — action-required vs purely informational — and search across tasks and incidents. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-229)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-037` · status **notStarted** · provenance generated
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403, 404, 422).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-037?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Acknowledge announcement, Publish announcement, What publishing changes.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-039` Announcements

**Read what the venue told everybody.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act |
| Offline | Cached. **Acknowledgement queues** — an emergency acknowledgement needing a network does not arrive when it matters |
| Opens with | `announcementId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/announcements` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Unacknowledged only | toggle | optional | — | — | — | Sends `?unacknowledgedOnly=` to `listAnnouncements`. | `listAnnouncements` ?unacknowledgedOnly |

**Form: Publish announcement** (modal, opened by *Publish announcement*; *Publish announcement* calls `publishAnnouncement`, *Cancel* sends nothing)

**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text field | required | — | max length 140 | — | — | `publishAnnouncement` body |
| Body `body` | text area | required | — | max length 4000 | — | — | `publishAnnouncement` body |
| Kind `kind` | radio group | required | — | Operational · Safety · Emergency · Hr · Celebration | — | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission. | `publishAnnouncement` body |
| Venues `venueIds` | multi-picker: choose venues | optional | — | — | — | — | `publishAnnouncement` body |
| Departments `departmentIds` | multi-picker: choose departments | optional | — | — | — | — | `publishAnnouncement` body |
| Roles `roleIds` | multi-picker: choose roles | optional | — | — | — | — | `publishAnnouncement` body |
| Requires acknowledgement `requiresAcknowledgement` | toggle | optional | — | — | — | — | `publishAnnouncement` body |
| Delivery channels `deliveryChannels` | multi-select chips | optional | In app, Push | In app · Push | — | How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). | `publishAnnouncement` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Published at `publishedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Locale `locale` | text field | optional | — | — | — | — | `publishAnnouncement` body |

Errors to draw in the form: 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type …

#### Outputs: what the screen shows and produces

**Shown**

**Every announcement** (data table, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The selected announcement** (detail panel, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The announcement reach** (detail panel, from `getAnnouncementReach`)

| Shows | Format | Notes |
|---|---|---|
| Announcement | the name it points at, never the id | — |
| Targeted | 1,234 | — |
| Delivered | 1,234 | — |
| Acknowledged | 1,234 | — |
| Outstanding | list or chips (count when long) | The list that matters. For an operational notice it measures whether anyone read it; during an emergency it is the roll call. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Acknowledge announcement (primary button) | `acknowledgeAnnouncement` POST `/announcements/{announcementId}/acknowledge` | — | — | — | works offline |
| Publish announcement (secondary button) | `publishAnnouncement` POST `/announcements` | Announcement | Announcement | 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type … | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listAnnouncements` (onLoad, What staff have been told)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The announcements list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the announcements untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No announcements yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on unacknowledgedOnly and the announcements are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached. **Acknowledgement queues** — an emergency acknowledgement needing a network does not arrive when it matters |

#### Permissions

- `listAnnouncements` → `WORKFORCE_VIEW` (read) · staff
- `acknowledgeAnnouncement` → `WORKFORCE_VIEW` (read) · staff
- `getAnnouncementReach` → `WORKFORCE_VIEW` (read) · staff
- `publishAnnouncement` → `ANNOUNCEMENT_PUBLISH` (configure) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.66 | System shall send assignment and schedule notifications. | Ticketing Catalogue | CONTRACTED | `publishAnnouncement` |
| 18.1.5 | Push Notifications - System shall support push notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.3 | Announcements - Users shall receive announcements. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.4 | Emergency Alerts - Users shall receive emergency notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Guest assistance: quick access to supervisors, announcements and venue information (e.g. opening hours), live ride/attraction status, and logging found items that surface for guest claim. *(client request · MoM 10 Aug 2026, 5.6 Roster, Leave & Break Management, Resources · DI-238)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-039` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-039?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Acknowledge announcement, Publish announcement, What publishing changes.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-038` Broadcast to team

**Reach everybody on shift at once.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW` (1 configure, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act |
| Offline | Queues, and states that it has not gone yet |
| Opens with | `announcementId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/broadcast-to-team` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Unacknowledged only | toggle | optional | — | — | — | Sends `?unacknowledgedOnly=` to `listAnnouncements`. | `listAnnouncements` ?unacknowledgedOnly |

**Form: Publish announcement** (modal, opened by *Publish announcement*; *Publish announcement* calls `publishAnnouncement`, *Cancel* sends nothing)

**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. **An `emergency` kind requires ANNOUNCEMENT_EMERGENCY** (audit R091 (1)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text field | required | — | max length 140 | — | — | `publishAnnouncement` body |
| Body `body` | text area | required | — | max length 4000 | — | — | `publishAnnouncement` body |
| Kind `kind` | radio group | required | — | Operational · Safety · Emergency · Hr · Celebration | — | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission. | `publishAnnouncement` body |
| Venues `venueIds` | multi-picker: choose venues | optional | — | — | — | — | `publishAnnouncement` body |
| Departments `departmentIds` | multi-picker: choose departments | optional | — | — | — | — | `publishAnnouncement` body |
| Roles `roleIds` | multi-picker: choose roles | optional | — | — | — | — | `publishAnnouncement` body |
| Requires acknowledgement `requiresAcknowledgement` | toggle | optional | — | — | — | — | `publishAnnouncement` body |
| Delivery channels `deliveryChannels` | multi-select chips | optional | In app, Push | In app · Push | — | How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). | `publishAnnouncement` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Published at `publishedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Locale `locale` | text field | optional | — | — | — | — | `publishAnnouncement` body |

Errors to draw in the form: 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type …

#### Outputs: what the screen shows and produces

**Shown**

**Every announcement** (data table, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The selected announcement** (detail panel, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The announcement reach** (detail panel, from `getAnnouncementReach`)

| Shows | Format | Notes |
|---|---|---|
| Announcement | the name it points at, never the id | — |
| Targeted | 1,234 | — |
| Delivered | 1,234 | — |
| Acknowledged | 1,234 | — |
| Outstanding | list or chips (count when long) | The list that matters. For an operational notice it measures whether anyone read it; during an emergency it is the roll call. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Publish announcement (primary button) | `publishAnnouncement` POST `/announcements` | Announcement | Announcement | 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type … | opens modal first |
| Acknowledge announcement (secondary button) | `acknowledgeAnnouncement` POST `/announcements/{announcementId}/acknowledge` | — | — | — | works offline |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listAnnouncements` (onLoad, What staff have been told)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The broadcast team list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the broadcast team untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No broadcast team yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on unacknowledgedOnly and the broadcast team are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `getAnnouncementReach` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Queues, and states that it has not gone yet |

#### Permissions

- `publishAnnouncement` → `ANNOUNCEMENT_PUBLISH` (configure) · staff
- `getAnnouncementReach` → `WORKFORCE_VIEW` (read) · staff
- `acknowledgeAnnouncement` → `WORKFORCE_VIEW` (read) · staff
- `listAnnouncements` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `getAnnouncementReach` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.66 | System shall send assignment and schedule notifications. | Ticketing Catalogue | CONTRACTED | `publishAnnouncement` |
| 18.1.5 | Push Notifications - System shall support push notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.3 | Announcements - Users shall receive announcements. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.4 | Emergency Alerts - Users shall receive emergency notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-038` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-038?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish announcement, Acknowledge announcement, What publishing changes.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-040` Knowledge base

**Look up the rule rather than guess it.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the screen declares only writes (`semanticSearch`) and no read of a population — it is settings, not a list |
| Offline | **Cached articles only**, with a note that newer ones may exist |
| Opens with | nothing: it opens on its own |
| Route | `/operations/knowledge-base` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Query | search field | — | — | — | — | Required. | `semanticSearch` |
| Kinds | multi select | — | — | — | — | — | — |
| Limit | number field | — | — | — | — | — | — |

**Sent by *Semantic search*** (`semanticSearch`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Query `query` | text area | required | — | min length 2; max length 500 | — | — | `semanticSearch` body |
| Kinds `kinds` | multi-select chips | optional | — | Product · Entitlement · Membership · Document · Knowledge · FAQ · Report · Media | — | — | `semanticSearch` body |
| Limit `limit` | number field | optional | 20 | max 100 | — | — | `semanticSearch` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Semantic search (primary button) | `semanticSearch` POST `/search` | inline | SearchResult[] | — | — |

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved knowledge base. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the knowledge base untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No knowledge base configured. The form opens empty and `semanticSearch` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `semanticSearch` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Cached articles only**, with a note that newer ones may exist |

#### Permissions

- `semanticSearch` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `semanticSearch` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.39 | System shall support semantic search across products, tickets, memberships, documents, knowledge bases, support content, assets, and operational data using vector-based retrieval and relevance … | Unified Operations Dashboard | CONTRACTED | `semanticSearch` |
| 23.1.6 | AI shall support semantic search allowing users to locate assets using natural language queries. | Digital Asset Management | CONTRACTED | `semanticSearch` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-040` · status **notStarted** · provenance generated
- Flow F101 *A staff member asks the assistant and it answers from the venue*, step 3: Knowledge base. → 1 operations, 1 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-040?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Semantic search.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-041` Training

**Do the module that unlocks the role.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `WORKFORCE_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listTrainingRecords` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | Cached progress; completions queue |
| Opens with | nothing: it opens on its own |
| Route | `/operations/training` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**Form: Semantic search** (modal, opened by *Semantic search*; *Semantic search* calls `semanticSearch`, *Cancel* sends nothing)

**Collects what `semanticSearch` sends before it is called.** Required: `query`. Optional: `kinds`, `limit`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Query `query` | text area | required | — | min length 2; max length 500 | — | — | `semanticSearch` body |
| Kinds `kinds` | multi-select chips | optional | — | Product · Entitlement · Membership · Document · Knowledge · FAQ · Report · Media | — | — | `semanticSearch` body |
| Limit `limit` | number field | optional | 20 | max 100 | — | — | `semanticSearch` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every training** (data table, from `listTrainingRecords`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Course name | text | — |
| Required | yes / no (icon or chip) | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| State | chip: Not started, In progress, Passed, Failed, Expired | — |
| Evidence ref | text | — |

**The selected training** (detail panel, from `listTrainingRecords`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Course name | text | — |
| Required | yes / no (icon or chip) | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| State | chip: Not started, In progress, Passed, Failed, Expired | — |
| Evidence ref | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Semantic search (primary button) | `semanticSearch` POST `/search` | inline | SearchResult[] | — | opens modal first |

**Data it reads**: `listTrainingRecords` (onLoad, Training completed and what is expiring)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The training list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the training untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No training yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listTrainingRecords` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listTrainingRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached progress; completions queue |

#### Permissions

- `semanticSearch` → `AI_USE` (operate) · staff
- `listTrainingRecords` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listTrainingRecords` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.39 | System shall support semantic search across products, tickets, memberships, documents, knowledge bases, support content, assets, and operational data using vector-based retrieval and relevance … | Unified Operations Dashboard | CONTRACTED | `semanticSearch` |
| 23.1.6 | AI shall support semantic search allowing users to locate assets using natural language queries. | Digital Asset Management | CONTRACTED | `semanticSearch` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-041` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Semantic search.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `AI_USE`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-042` Profile

**Change what this person controls about themselves.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listMfaMethods` reads the population and `getCurrentSession` reads one of them — list, select, act |
| Offline | Cached |
| Opens with | `sessionId` (session), `methodId` (navigation) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/operations/profile` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: forceLogout, listActiveSessions, revokeAllSessions. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**

**Known gaps.** **1 declared operation reaches no component on this screen**: listSsoProviders. Either the screen is missing what calls them, or the declaration is residue.

#### Inputs: what the user enters or picks

**Form: Add a sign-in method** (modal, opened by *Add a sign-in method*; *Add method* calls `enrolMfaMethod`, *Cancel* sends nothing)

**Collects what `enrolMfaMethod` sends before it is called.** Required: `kind`, offered as authenticator app (`totp`) or email (`emailOtp`) only (audit R126 (5)). Optional: `target`, the email address for the email method. The response carries the secret and QR code for an authenticator app. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Totp · SMS OTP · Email OTP · Biometric · Hardware token | — | — | `enrolMfaMethod` body |
| Target `target` | text field | optional | — | — | — | Phone or email for OTP methods. | `enrolMfaMethod` body |

Errors to draw in the form: 403 A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1).

**Form: Verify the new method** (modal, opened by *Verify the new method*; *Verify* calls `verifyMfaEnrolment`, *Cancel* sends nothing)

**Collects what `verifyMfaEnrolment` sends before it is called.** Required: `code`. The method is active only after this. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `verifyMfaEnrolment` body |

**Form: Remove this method** (confirmDialog, opened by *Remove this method*; *Remove method* calls `removeMfaMethod`, *Keep it* sends nothing)

**Names the method being removed.** Removing the last active method is refused 409 while the person holds a permission in `PasswordPolicy.mfaRequiredForPermissions`, and the dialog says so before the call rather than after (decided 28 September, audit R135).

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135)

#### Outputs: what the screen shows and produces

**Shown**

**Every MFA method** (data table, from `listMfaMethods`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**Every SSO provider** (data table, from `listSsoProviders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Display name | text | — |
| Protocol | chip: Oidc, Saml2 | — |
| Icon | the image or video | — |
| Is enforced | yes / no (icon or chip) | True disables password login for principals covered by this provider. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected MFA method** (detail panel, from `listMfaMethods`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**The session** (detail panel, from `getCurrentSession`)

| Shows | Format | Notes |
|---|---|---|
| Session | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Role | the name it points at, never the id | — |
| Display name | text | — |
| Scope | list or chips (count when long) | Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. |
| Effective permissions | list or chips (count when long) | Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. |
| Permissions by scope | list or chips (count when long) | Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves. |
| Sale board | the name it points at, never the id | Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board. |
| Workstation | grouped details | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add a sign-in method (primary button) | `enrolMfaMethod` POST `/auth/mfa/methods` | inline | MfaEnrolment | 403 A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest … | opens modal first |
| Verify the new method (secondary button) | `verifyMfaEnrolment` POST `/auth/mfa/methods/{methodId}` | inline | MfaMethod | — | opens modal first |
| Remove this method (destructive button) | `removeMfaMethod` DELETE `/auth/mfa/methods/{methodId}` | — | — | 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135) | opens confirmDialog first |

**Data it reads**: `getCurrentSession` (onLoad, Current session and effective permissions); `listMfaMethods` (onLoad, Enrolled MFA methods); `listSsoProviders` (onLoad, Identity providers configured for this tenant)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No profile yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listMfaMethods` takes no filter, so an empty list is always the first-run state above. |
| Offline (`?state=offline`) | Cached |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135); 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1). |

#### Permissions

- `getCurrentSession` → no permission · staff, partner
- `listMfaMethods` → no permission · staff, partner, guest
- `enrolMfaMethod` → no permission · staff, partner, guest
- `verifyMfaEnrolment` → no permission · staff, partner, guest
- `removeMfaMethod` → no permission · staff, partner, guest
- `listSsoProviders` → no permission · anonymous, partner

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |
| 7.1.16 | The system shall support MFA using Email OTP, SMS OTP, Authenticator Apps, and future supported authentication mechanisms. | F&B POS | CONTRACTED | `enrolMfaMethod` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-042` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (403, 409, 422).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-042?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Add a sign-in method, Verify the new method, Remove this method.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-043` Device settings

**Set how this handheld behaves.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listDevices` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Fully offline** — device settings are local by definition |
| Opens with | `subjectId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/operations/device-settings` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: listGuestDevices, adjustLoyaltyPoints, getConsentHistory, getGuestConsents, getGuestLoyalty, getGuestProfile, getWishlist. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Removed 24 August**: mergeGuestProfiles, searchGuests, updateGuestProfile. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listDevices`. | `listDevices` ?workstationId |
| Kind | select | optional | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | — | Sends `?kind=` to `listDevices`. | `listDevices` ?kind |

**Form: Register device** (modal, opened by *Register device*; *Register device* calls `registerDevice`, *Cancel* sends nothing)

**Collects what `registerDevice` sends before it is called.** Required: `id`, `kind`, `driver`, `workstationId`. Optional: `identifier`, `model`, `pushToken`, `pushPlatform`, `pushFailureCount`, `offlineScope`, `firmwareVersion`, `isRequired`, `status`, `batteryPercent`, `lastCheckedAt`, `health` and 5 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | — | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation. | `registerDevice` body |
| Driver `driver` | text field | required | — | — | — | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015). | `registerDevice` body |
| Identifier `identifier` | text field | optional | — | — | — | — | `registerDevice` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is … | `registerDevice` body |
| Model `model` | text field | optional | — | — | — | — | `registerDevice` body |
| Hardware type `hardwareType` | select | optional | — | Standard turnstile · Full height turnstile · Tripod turnstile · Speed gate · Wide lane · Accessible pod gate · Buggy gate · Vip gate · Staff gate · Android handheld · Ios device · Tablet … | — | The specific hardware under `kind` (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. | `registerDevice` body |
| Hardware model `hardwareModelId` | picker: choose a hardware model | optional | — | — | shows names, sends the id | The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it. | `registerDevice` body |
| Serial number `serialNumber` | text field | optional | — | max length 100; A serial already registered in the tenant is refused `409` by `registerDevice`. | — | The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). | `registerDevice` body |
| Ip network reference `ipNetworkReference` | text field | optional | — | — | — | Network address or reference the device is reached at (ADR-0067). | `registerDevice` body |
| Push token `pushToken` | text field | optional | — | Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has … | — | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told … | `registerDevice` body |
| Push platform `pushPlatform` | radio group | optional | — | Ios · Android · Web · Windows | — | — | `registerDevice` body |
| Offline scope `offlineScope` | radio group | optional | — | None · Read only · Sell and scan · Full venue | — | BL-163. What this device may do with no connection, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled. | `registerDevice` body |
| Is required `isRequired` | toggle | optional | — | — | — | True blocks shift open when the device is unreachable. | `registerDevice` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 422 `workstationId` missing for a kind other than `mobileHandset`, or given for a `mobileHandset` (18.1.5).

#### Outputs: what the screen shows and produces

**Shown**

**Every registered device** (data table, from `listDevices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Driver | text | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change … |
| Identifier | text | — |
| Workstation | the name it points at, never the id | Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control … |
| Model | text | — |
| Push token | text | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count … |
| Push platform | chip: Ios, Android, Web, Windows | — |
| Push failure count | 1,234 | Consecutive failures. A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a … |
| Offline scope | chip: None, Read only, Sell and scan, Full venue | BL-163. What this device may do with no connection, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it … |
| Firmware version | text | As the device last reported it on its heartbeat. |
| Is required | yes / no (icon or chip) | True blocks shift open when the device is unreachable. |

**The selected registered device** (detail panel, from `listDevices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Driver | text | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change … |
| Identifier | text | — |
| Workstation | the name it points at, never the id | Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control … |
| Model | text | — |
| Push token | text | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count … |
| Push platform | chip: Ios, Android, Web, Windows | — |
| Push failure count | 1,234 | Consecutive failures. A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a … |
| Offline scope | chip: None, Read only, Sell and scan, Full venue | BL-163. What this device may do with no connection, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it … |
| Firmware version | text | As the device last reported it on its heartbeat. |
| Is required | yes / no (icon or chip) | True blocks shift open when the device is unreachable. |
| Status | chip: Online, Offline, Error, Consumable low, Needs attention, Local mode… | What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline … |
| Battery percent | 1,234 | Board 1 of the client's POS design set, 20 August. A wristband encoder at 8% is a gate that stops working in an hour, and nothing in the … |
| Last checked at | 1 Oct 2026, 14:30 | Distinct from `lastHeartbeatAt`. A heartbeat is the workstation saying the device is attached; a check is the device answering. |
| Health | chip: Healthy, Warning, Degraded, Offline, Unknown | Derived, not reported. Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Register device (primary button) | `registerDevice` POST `/devices` | RegisteredDevice | RegisteredDevice | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here … | opens modal first |

**Data it reads**: `listDevices` (onLoad, List registered devices)

**Where the user goes next**

- → `EMP-018` Offline package: *It pulls its offline package*; calls `listDevices`
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device settings list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device settings untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device settings yet. Offers Register device (`registerDevice`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, kind and the device settings are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `DEVICE_VIEW`, which `listDevices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Fully offline** — device settings are local by definition |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 422 `workstationId` missing for a kind other than `mobileHandset`, or given for a `mobileHandset` (18.1.5). |

#### Permissions

- `listDevices` → `DEVICE_VIEW` (read) · staff
- `registerDevice` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `DEVICE_VIEW`, which `listDevices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

48 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.18 | POS and kiosk devices shall be linked to the Device Management module so administrators can monitor device status, location, software version, connectivity, errors, paper levels, and assigned … | Ticketing Sales | CONTRACTED | `listDevices` |
| 2.1.26 | System shall provide centralized monitoring of kiosk health including online status, stock levels, payment devices, printers, connectivity, and alerts. | Ticketing Sales | CONTRACTED | `listDevices` |
| 8.9.6 | System shall monitor scanners, POS devices, kiosks, handhelds, printers, gates, network connectivity, and infrastructure health. | Unified Operations Dashboard | CONTRACTED | `listDevices` |
| 16.2.7 | Device Inventory Management - System shall maintain device inventories. | Device Management | CONTRACTED | `listDevices` |
| 16.2.8 | Device Classification - System shall support device categorization. | Device Management | CONTRACTED | `listDevices` |
| 16.2.12 | Device Asset Tracking - System shall maintain device asset records. | Device Management | CONTRACTED | `listDevices` |
| 16.9.55 | Device APIs - System shall expose device management APIs. | Device Management | CONTRACTED | `listDevices` |
| 2.1.14 | The system should be able to identify each ticketing kiosk individually by an ID, locate it geographically and administer it remotely. The kiosks should include a supervision interface and alert … | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.6 | It is expected that front gate sales can be performed by the operators using a POS having a touch screen. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.7 | The POS can be connected to a keyboard for which the function touches can be setup by the system administrator. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.8 | The POS can be connected to a cash drawer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.9 | The POS can be connected to a BOCA printer (it is expected to have the list of ticket printing hardware compatible) | Ticketing Sales | CONTRACTED | `registerDevice` |
| … 36 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-043` · status **notStarted** · provenance generated
- Flow F71 *A device is prepared, used and handed over*, step 1: The device is checked and registered. → **A heartbeat is the test.** `testPeripheral` was drawn on the client board and resolves here — a separate test would report a different truth from the one the fleet view reads.
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)
- ADR-0015 *Standards-First Device Drivers* (`docs/adr/0015-standards-first-device-drivers.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 409, 422).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-043?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Register device.
- [ ] Every transition is wired: `EMP-018`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-044` Accessibility

**Make the app usable in the conditions it is used in.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **the screen's operations choose no pattern** — no list, no get, no write that groups. It falls to the default, and the fallback is recorded rather than passed off as a decision |
| Offline | **Fully offline.** Accessibility settings are device-local and must never depend on a network |
| Opens with | nothing: it opens on its own |
| Route | `/operations/accessibility` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** **This screen declares no operation the contracts recognise.** Nothing fills it, nothing it does is committed anywhere, and its shape below is a default rather than a reading.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | — |
| Error (`?state=error`) | — |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Offline (`?state=offline`) | **Fully offline.** Accessibility settings are device-local and must never depend on a network |

#### Permissions

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-044` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-044?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P06 reference designs** (from `handoff/design-batches/apps/4-staff-app/README.md`)

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the client's employee app reference: dark theme, Home, Tasks, Scan, AI, More.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P06 as a whole** (3: 0 open, 3 closed). Open first; a closed row says where it went on 30 September.

- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A49** Confirm scope: deliver a lightweight standalone ticket-validation app for dedicated scanner devices, in addition to the scan/validate function embedded in the full Staff Operations App *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A71** Design an offline-first, native ticket-scanning/access-control capability (local scan storage with sync-on-reconnect) for both the dedicated scanner app and the scanning function embedded in the Employee App *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 10 Aug 2026 · workshop tracker)*

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

### Across P06 Venue Staff App

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### In P06 · Operations

- Employee app navigation: Work Orders, Task & Assets, Inventory/Safety/Inspections, Attendance, Approvals/Requests, Incidents, Communications, Venue Map; plus employee ID/profile and preferences. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-228)*

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acknowledgeAnnouncement": {"method":"POST","path":"/announcements/{announcementId}/acknowledge","contract":"workforce","summary":"Confirm you have read it","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"addTip": {"method":"POST","path":"/payments/{paymentId}/tip","contract":"orders","summary":"Record a tip against a payment","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"appendEntitlementToMedia": {"method":"POST","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"Add something to a ticket the guest already holds","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AppendEntitlementRequest","responds":"AppendEntitlementResult"},
"capturePayment": {"method":"POST","path":"/payments/{paymentId}/capture","contract":"orders","summary":"Capture a previously authorised payment","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"createPayment": {"method":"POST","path":"/payments","contract":"orders","summary":"Take a payment against an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePaymentRequest","responds":"Payment"},
"enrolMfaMethod": {"method":"POST","path":"/auth/mfa/methods","contract":"identity","summary":"Enrol an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaEnrolment"},
"getAnnouncementReach": {"method":"GET","path":"/announcements/{announcementId}/reach","contract":"workforce","summary":"Who has acknowledged, and who has not","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AnnouncementReach"},
"getCurrentSession": {"method":"GET","path":"/auth/session","contract":"identity","summary":"Current session and effective permissions","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Session"},
"getMediaAsset": {"method":"GET","path":"/media/{mediaId}","contract":"assets","summary":"Read an asset with derivatives and usage","permission":"ASSET_LIBRARY_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetDetail"},
"getMediaEntitlements": {"method":"GET","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"What is already on this media","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaEntitlements"},
"inquirePaymentStatus": {"method":"POST","path":"/payments/{paymentId}/inquiry","contract":"orders","summary":"Ask the provider what actually happened","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"listAnnouncements": {"method":"GET","path":"/announcements","contract":"workforce","summary":"What staff have been told","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"unacknowledgedOnly","in":"query","required":null}],"requestBody":null,"responds":"Announcement"},
"listDevices": {"method":"GET","path":"/devices","contract":"tenancy","summary":"List registered devices","permission":"DEVICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMfaMethods": {"method":"GET","path":"/auth/mfa/methods","contract":"identity","summary":"Enrolled MFA methods","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MfaMethod"},
"listSsoProviders": {"method":"GET","path":"/auth/sso/providers","contract":"identity","summary":"Identity providers configured for this tenant","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProvider"},
"listStaffConversations": {"method":"GET","path":"/staff-conversations","contract":"workforce","summary":"The caller's staff conversations, newest activity first","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"unreadOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStaffMessages": {"method":"GET","path":"/staff-conversations/{conversationId}/messages","contract":"workforce","summary":"Messages in one staff conversation, newest first","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTrainingRecords": {"method":"GET","path":"/training-records","contract":"workforce","summary":"Training completed and what is expiring","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TrainingRecord"},
"markStaffConversationRead": {"method":"POST","path":"/staff-conversations/{conversationId}/read","contract":"workforce","summary":"Mark a staff conversation read up to a message","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"publishAnnouncement": {"method":"POST","path":"/announcements","contract":"workforce","summary":"Tell staff something","permission":"ANNOUNCEMENT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Announcement","responds":"Announcement"},
"registerDevice": {"method":"POST","path":"/devices","contract":"tenancy","summary":"Register a device","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegisteredDevice","responds":"RegisteredDevice"},
"removeMfaMethod": {"method":"DELETE","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Remove an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"semanticSearch": {"method":"POST","path":"/search","contract":"ai","summary":"Search meaning, not words","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SearchResult"},
"sendStaffMessage": {"method":"POST","path":"/staff-messages","contract":"workforce","summary":"Send a message to a colleague or a small group","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkforceSendStaffMessageRequest","responds":"WorkforceStaffMessage"},
"verifyMfaEnrolment": {"method":"POST","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Complete enrolment","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaMethod"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Announcement": {"type":"object","x-ticvai-persistence":"workforce.announcement","required":["title","body","kind","publishedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"type":"string","maxLength":140},"body":{"type":"string","maxLength":4000},"kind":{"$ref":"#/components/schemas/AnnouncementKind"},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresAcknowledgement":{"type":"boolean"},"deliveryChannels":{"type":"array","description":"How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n","items":{"type":"string","enum":["inApp","push"]},"default":["inApp","push"]},"expiresAt":{"type":"string","format":"date-time","nullable":true},"publishedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"publishedAt":{"type":"string","format":"date-time"},"locale":{"type":"string","nullable":true}}},
"AnnouncementKind": {"type":"string","description":"`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n","enum":["operational","safety","emergency","hr","celebration"]},
"AnnouncementReach": {"type":"object","x-ticvai-persistence":"none — computed from workforce.announcement_receipt","properties":{"announcementId":{"type":"string","format":"uuid"},"targeted":{"type":"integer"},"delivered":{"type":"integer"},"acknowledged":{"type":"integer"},"outstanding":{"type":"array","description":"**The list that matters.** For an operational notice it measures whether anyone read it; during an emergency it is the roll call.\n","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"onShift":{"type":"boolean"}}}}}},
"AppendEntitlementRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header."},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true}}}},"paymentMethod":{"type":"string","enum":["card","cash","wallet","giftCard","chargeToAccount"]},"note":{"type":"string","maxLength":300},"recordedAt":{"type":"string","format":"date-time"}}},
"AppendEntitlementResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","media"],"properties":{"order":{"allOf":[{"$ref":"#/components/schemas/Order"}],"description":"A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"},"media":{"allOf":[{"$ref":"#/components/schemas/MediaEntitlements"}],"description":"The full set now on the media, so the cashier can say what the QR does."},"addedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"DeviceCapability": {"type":"string","description":"BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n","enum":["genderClassification","dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},
"DeviceKind": {"type":"string","enum":["receiptPrinter","ticketPrinter","labelPrinter","cashDrawer","barcodeScanner","rfidReader","nfcReader","cardReader","idReader","biometricReader","accessReader","paymentTerminal","customerDisplay","signageDisplay","kitchenDisplay","turnstileController","wristbandEncoder","signaturePad","scale","camera","mobileHandset","handheldScanner","accessPodium","bleBeacon"],"description":"`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"},
"EntitlementStatus": {"type":"string","description":"**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n","enum":["issued","partiallyConsumed","fullyConsumed","expired","cancelled","surrendered"]},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetDetail": {"x-ticvai-persistence":"assets.media_asset","allOf":[{"$ref":"#/components/schemas/MediaAsset"},{"type":"object","properties":{"derivatives":{"type":"array","description":"Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n","items":{"type":"object","properties":{"label":{"type":"string"},"width":{"type":"integer"},"height":{"type":"integer"},"sizeBytes":{"type":"integer"},"url":{"type":"string"}}}},"usage":{"type":"array","description":"Every place this asset is referenced.","items":{"$ref":"#/components/schemas/MediaUsage"}},"collections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"previousVersions":{"type":"array","items":{"type":"object","properties":{"version":{"type":"integer"},"replacedAt":{"type":"string","format":"date-time"},"replacedByPrincipalId":{"type":"string","format":"uuid"}}}}}}]},
"MediaEntitlements": {"type":"object","x-ticvai-persistence":"none — projection over entitlement and scan history","required":["mediaCode","isValid","entitlements"],"properties":{"mediaCode":{"type":"string"},"mediaKind":{"type":"string","enum":["qr","wristband","card","nfc","mobilePass"]},"subjectId":{"type":"string","format":"uuid","nullable":true},"isValid":{"type":"boolean"},"invalidReason":{"type":"string","nullable":true},"canAcceptMore":{"type":"boolean","description":"False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"},"entitlements":{"type":"array","items":{"type":"object","properties":{"entitlementId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["admission","locker","fnb","retail","parking","rental","experience","membership"]},"orderId":{"type":"string","format":"uuid"},"addedAt":{"type":"string","format":"date-time"},"status":{"allOf":[{"$ref":"#/components/schemas/EntitlementStatus"}],"description":"**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"transferredToSubjectId":{"type":"string","format":"uuid","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true}}}}}},
"MediaUsage": {"x-ticvai-persistence":"assets.media_usage","type":"object","description":"One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n","required":["surface","referenceId"],"properties":{"extractedText":{"type":"string","description":"**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"surface":{"type":"string","enum":["tenantBranding","homepageBanner","promoBlock","contentPage","product","event","menuItem","merchandise","workOrder","incident","inspection","campaign"]},"referenceId":{"type":"string"},"label":{"type":"string"},"isLive":{"type":"boolean","description":"True where the referencing surface is published to guests."}}},
"MfaEnrolment": {"x-ticvai-persistence":"none — transient","type":"object","required":["methodId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"methodId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"secret":{"type":"string","nullable":true,"description":"TOTP shared secret. Returned once, at enrolment, and never again."},"qrCodeUri":{"type":"string","nullable":true},"recoveryCodes":{"type":"array","description":"Returned once, in this enrolment response (`enrolMfaMethod` writes them, hashed, to `identity.mfa_recovery_code`). Not retrievable afterwards — `verifyMfaEnrolment` does not return them.\n","items":{"type":"string"}},"expiresAt":{"type":"string","format":"date-time"}}},
"MfaKind": {"type":"string","enum":["totp","smsOtp","emailOtp","biometric","hardwareToken"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"RegisteredDevice": {"x-ticvai-persistence":"platform.device","type":"object","description":"**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n","required":["id","kind","driver"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"},"identifier":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"},"model":{"type":"string","nullable":true},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType","nullable":true,"description":"**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"},"hardwareModelId":{"type":"string","format":"uuid","nullable":true,"description":"The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"},"serialNumber":{"type":"string","nullable":true,"maxLength":100,"description":"The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"},"ipNetworkReference":{"type":"string","nullable":true,"description":"Network address or reference the device is reached at (ADR-0067)."},"configurationVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Access configuration version the device reports running (ADR-0067)."},"localRuleVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Admission rule package the device reports running (ADR-0067)."},"credentialSecurityPackageVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Credential security package the device reports running (ADR-0067)."},"scannerHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Component health as the device or vendor reports it on its heartbeat (ADR-0067)."},"controllerHealth":{"type":"string","nullable":true,"readOnly":true},"cameraHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Where the device has a camera."},"connectivity":{"type":"string","nullable":true,"readOnly":true,"description":"Reported connectivity."},"pushToken":{"type":"string","format":"password","nullable":true,"writeOnly":true,"description":"BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"},"pushPlatform":{"type":"string","nullable":true,"enum":["ios","android","web","windows"]},"pushFailureCount":{"type":"integer","default":0,"readOnly":true,"description":"**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"},"offlineScope":{"type":"string","nullable":true,"enum":["none","readOnly","sellAndScan","fullVenue"],"description":"BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"},"firmwareVersion":{"type":"string","nullable":true,"readOnly":true,"description":"As the device last reported it on its heartbeat."},"isRequired":{"type":"boolean","description":"True blocks shift open when the device is unreachable."},"status":{"type":"string","readOnly":true,"enum":["online","offline","error","consumableLow","needsAttention","localMode","unknown"],"description":"What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"},"batteryPercent":{"type":"integer","nullable":true,"readOnly":true,"minimum":0,"maximum":100,"description":"Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"},"health":{"type":"string","enum":["healthy","warning","degraded","offline","unknown"],"default":"unknown","readOnly":true,"description":"**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"capabilities":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/DeviceCapability"},"description":"BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"},"enrolmentState":{"type":"string","enum":["registered","enrolled","provisioned","active","deactivated","retired"],"default":"registered","readOnly":true,"description":"BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"},"retiredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"}}},
"SearchResult": {"type":"object","x-ticvai-persistence":"none — computed","properties":{"kind":{"type":"string"},"id":{"type":"string"},"title":{"type":"string"},"excerpt":{"type":"string"},"relevance":{"type":"number"},"collectionId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"For kind `media`, the asset (29 September, build; 23.1.6)."},"mediaType":{"type":"string","nullable":true,"enum":["image","video","audio","document"]},"matchedOn":{"type":"string","nullable":true,"enum":["title","description","tags","aiDescription"],"description":"Which text the match came from, so a wrong hit can be traced to a wrong tag."}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions","saleBoardId"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProvider": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"iconAssetRef":{"type":"string","nullable":true},"isEnforced":{"type":"boolean","description":"True disables password login for principals covered by this provider."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]},
"TrainingRecord": {"type":"object","x-ticvai-persistence":"workforce.training_record","description":"**Drafted 4 September.** One person, one course, one outcome. **The field that matters is the expiry** - a lapsed food-safety or first-aid certificate is a person who may not work a station, and a list without it is a list nobody can roster from.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"courseName":{"type":"string"},"required":{"type":"boolean"},"completedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"},"state":{"type":"string","enum":["notStarted","inProgress","passed","failed","expired"]},"evidenceRef":{"type":"string"}}},
"WorkforceSendStaffMessageRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","body","sentAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7; a replay of the same id returns the stored message."},"conversationId":{"type":"string","format":"uuid","nullable":true,"description":"An existing conversation the caller is in. Absent means `recipientPrincipalIds`."},"recipientPrincipalIds":{"type":"array","maxItems":49,"items":{"type":"string","format":"uuid"},"description":"Colleagues to message when there is no `conversationId`. One reuses the direct conversation; several start a group."},"title":{"type":"string","maxLength":120,"nullable":true,"description":"A new group's title; ignored otherwise."},"body":{"type":"string","minLength":1,"maxLength":2000},"attachmentAssetId":{"type":"string","format":"uuid","nullable":true},"sentAt":{"type":"string","format":"date-time"}}},
"WorkforceStaffConversation": {"type":"object","x-ticvai-persistence":"workforce.staff_conversation","description":"**One direct or group conversation between staff of a venue** (18.9.5 Internal Messaging; decided 29 September, build pass). Created by `sendStaffMessage` the first time colleagues are messaged; its participants are `workforce.staff_conversation_participant` rows. Announcements stay the one-to-many channel; this is the one-to-one and small-group one.","required":["id","venueId","kind","createdByPrincipalId","createdAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"kind":{"type":"string","enum":["direct","group"],"description":"A direct conversation has exactly two participants and at most one exists per pair."},"title":{"type":"string","maxLength":120,"nullable":true,"description":"Group conversations only; null on a direct one."},"createdByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"lastMessageAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"WorkforceStaffConversationSummary": {"type":"object","x-ticvai-persistence":"none — projection over workforce.staff_conversation, its participants and its latest message, for the caller","description":"One row of `listStaffConversations`, as the caller sees it.","required":["conversation","unreadCount"],"properties":{"conversation":{"$ref":"#/components/schemas/WorkforceStaffConversation"},"participants":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"onShift":{"type":"boolean"}}}},"lastMessage":{"allOf":[{"$ref":"#/components/schemas/WorkforceStaffMessage"}],"nullable":true},"unreadCount":{"type":"integer","minimum":0}}},
"WorkforceStaffMessage": {"type":"object","x-ticvai-persistence":"workforce.staff_message","description":"One message in a staff conversation (decided 29 September, build pass). Never edited through the API, so a conversation reads the same to everyone in it afterwards.","required":["id","staffConversationId","senderPrincipalId","body","sentAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client-generated UUIDv7 from the send, the key an offline replay deduplicates on."},"staffConversationId":{"type":"string","format":"uuid"},"senderPrincipalId":{"type":"string","format":"uuid"},"body":{"type":"string","maxLength":2000},"attachmentAssetId":{"type":"string","format":"uuid","nullable":true,"description":"A photo or file, held as a media asset."},"sentAt":{"type":"string","format":"date-time","description":"When the sender sent it, which for a message queued offline is before it arrived."},"receivedAt":{"type":"string","format":"date-time","readOnly":true,"nullable":true}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
