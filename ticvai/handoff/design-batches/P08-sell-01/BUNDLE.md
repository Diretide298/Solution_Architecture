# P08-sell-01 — P08 · Sell (1 of 4)

**10 screens · 87 operations · 99 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `CAPACITY_CONFIGURE, EVENT_CONFIGURE, PERFORMANCE_CONFIGURE, PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `BO-007` | Product Directory | A | 86 | 62 | 6 | 75 | 3 | 0 | — | notStarted (generated) |
| `BO-009` | Pricing Rules | A | 23 | 25 | 6 | 19 | 3 | 0 | — | notStarted (generated) |
| `BO-010` | Promotions & Coupons | A | 165 | 70 | 6 | 51 | 3 | 2 | — | notStarted (generated) |
| `BO-011` | Packages & Bundles | A | 75 | 47 | 6 | 12 | 4 | 0 | — | notStarted (generated) |
| `BO-012` | Membership Products | A | 115 | 53 | 6 | 112 | 0 | 0 | — | notStarted (generated) |
| `BO-013` | Channel & Distribution | B–D | 27 | 54 | 6 | 34 | 2 | 0 | — | notStarted (generated) |
| `BO-014` | Catalogue Publishing | B–D | 78 | 46 | 6 | 71 | 0 | 6 | — | notStarted (generated) |
| `BO-015` | Performance Calendar | B–D | 39 | 58 | 6 | 38 | 5 | 0 | — | notStarted (generated) |
| `BO-016` | Performance Template | B–D | 19 | 15 | 6 | 0 | 5 | 0 | — | notStarted (generated) |
| `BO-017` | Capacity Management | B–D | 24 | 30 | 6 | 14 | 7 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-016 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-007` Product Directory

**Find anything sellable at this venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18007 (APP-SETUP-BO-007) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read); in the flows as supervisor, venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listProducts` reads the population and `getProduct` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `productId` (deepLink), `venueId` (session) · cold entry: **A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does. |
| Route | `/venue-operations/product-directory` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 5 board screen(s): Menu & Product Command Center; Product / PLU Master; Variants, Modifiers & Special Selling Rules and 2 more. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real. **Retail board operations wired 24 August.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listProducts`. | `listProducts` ?venueId |
| Kind | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Sends `?kind=` to `listProducts`. | `listProducts` ?kind |
| Is sellable | toggle | optional | — | — | — | Sends `?isSellable=` to `listProducts`. | `listProducts` ?isSellable |
| Booking flow | picker: choose a booking flow | optional | — | — | shows names, sends the id | The venue's booking flows from CMS-103 (`white-label.listBookingFlows`). Empty means the category's flow, then the venue's flow for the product kind (W8, W12). Saved with `createProduct` or … | `Product.bookingFlowId` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |
| Outlet | picker: choose an outlet | — | — | `listMenus` ?outletId |
| Active at | date and time picker | — | — | `listMenus` ?activeAt |
| Outlet | picker: choose an outlet | — | — | `listMerchandise` ?outletId |
| Category | picker: choose a category | — | — | `listMerchandise` ?categoryId |
| In stock only | toggle | off | — | `listMerchandise` ?inStockOnly |
| Search | text field | — | min length 1; max length 100 | `listMerchandise` ?search |

**Form: Create product** (modal, opened by *Create product*; *Create product* calls `createProduct`, *Cancel* sends nothing)

**Collects what `createProduct` sends before it is called.** Required: `code`, `name`, `kind`, `venueId`. Optional: `description`, `channels`, `entitlementTemplateId`, `dataMaskValues`, `guestListing` and `notBookableLabel` (REV3-14), `displayTags` (23SEP-3), `media` (23SEP-4), `consentQuestionIds` (REV3-26), `requiresTimeWindow` (REV3-13), all decided 29 September, rev 3; `salesContact` (W3: who a guest calls or emails to book an info-only product) and `bookingFlowId` (W8, W12: the booking flow the product is sold through; empty means the category's flow, then the venue's flow for its kind), decided 29 September. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; A code already used by any product in the tenant, at any venue, is refused with `409 duplicate-code`. | — | Unique per tenant (decided 28 September, audit R108). A code already used by any product in the tenant, at any venue, is refused with `409 duplicate-code`. | `createProduct` body |
| Family key `familyKey` | text field | optional | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; At most one product per venue in a family, else `409 duplicate-code`. | — | The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. | `createProduct` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createProduct` body |
| Description `description` | text area | optional | — | — | — | — | `createProduct` body |
| Kind `kind` | select | required | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: valid on any date within an eligible … | `createProduct` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createProduct` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createProduct` body |
| Entitlement template `entitlementTemplateId` | picker: choose an entitlement template | optional | — | — | shows names, sends the id | — | `createProduct` body |
| Data mask values `dataMaskValues` | key and value settings | optional | — | — | — | — | `createProduct` body |
| Guest listing `guestListing` | segmented control | optional | Bookable | Bookable · Info only · Hidden; `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. | — | How a product appears to a guest (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. | `createProduct` body |
| Not bookable label `notBookableLabel` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createProduct` body |
| Sales contact `salesContact` | group | optional | — | — | — | See `Product.salesContact` (W3, 29 September). | `createProduct` body |
| Phone `salesContact.phone` | phone field | optional | — | max length 32 | +971 5X XXX XXXX (E.164) | — | `createProduct` body |
| Email `salesContact.email` | email field | optional | — | max length 254 | name@example.ae | — | `createProduct` body |
| Note `salesContact.note` | text, one per language | optional | — | At most 200 characters per language. | English and Arabic (Arabic right to left) | A line shown under the contact, e.g. *Group courses are booked by phone*. | `createProduct` body |
| Booking flow `bookingFlowId` | picker: choose a booking flow | optional | — | — | shows names, sends the id | See `Product.bookingFlowId` (W8, W12, 29 September). | `createProduct` body |
| Display tags `displayTags` | repeatable rows | optional | — | at most 6 | — | — | `createProduct` body |
| Kind `displayTags[].kind` | radio group | required | — | Clock · Height · Free · Calendar · ID | — | `clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring. | `createProduct` body |
| Label `displayTags[].label` | text, one per language | required | — | Each language value at most 40 characters. | English and Arabic (Arabic right to left) | What the guest reads, e.g. *2 Hours*. | `createProduct` body |
| Media `media` | repeatable rows | optional | — | at most 20 | — | — | `createProduct` body |
| Asset `media[].assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | A `MediaAsset` of `assets.yaml`, in status `ready`. | `createProduct` body |
| Kind `media[].kind` | segmented control | required | — | Image · Video | — | — | `createProduct` body |
| Is primary `media[].isPrimary` | toggle | required | off | — | — | The item *Read more* opens on and a listing shows. Exactly one per product. | `createProduct` body |
| Display order `media[].displayOrder` | number field | optional | 100 | — | — | — | `createProduct` body |
| Alt text `media[].altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createProduct` body |
| Consent questions `consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates | — | — | `createProduct` body |
| Requires time window `requiresTimeWindow` | toggle | optional | — | — | — | — | `createProduct` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A `media` asset that is not `ready` or whose kind does not match, a `consentQuestionIds` entry that names no active consent question of the tenant, or …

**Form: Save alternative codes** (modal, opened by *Save alternative codes*; *Save alternative codes* calls `setAlternativeCodes`, *Cancel* sends nothing)

**Collects what `setAlternativeCodes` sends before it is called.** Required: `codes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Codes `codes` | repeatable rows | required | — | — | — | — | `setAlternativeCodes` body |
| Code `codes[].code` | text field | required | — | max length 128 | — | — | `setAlternativeCodes` body |
| Partner `codes[].partnerId` | picker: choose a partner | required | — | — | shows names, sends the id | — | `setAlternativeCodes` body |
| Partner name `codes[].partnerName` | text field | optional | — | — | — | — | `setAlternativeCodes` body |
| Variant `codes[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `setAlternativeCodes` body |
| Note `codes[].note` | text area | optional | — | max length 200 | — | — | `setAlternativeCodes` body |

Errors to draw in the form: 400 A `variantId` is not a variant of this product, or the body sends one code twice for the same partner.; 409 Code already mapped to a different product for that partner

**Form: Save product attributes** (modal, opened by *Save product attributes*; *Save product attributes* calls `setProductAttributes`, *Cancel* sends nothing)

**Collects what `setProductAttributes` sends before it is called.** Required: `axes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Axes `axes` | repeatable rows | required | — | — | — | — | `setProductAttributes` body |
| Code `axes[].code` | text field | required | — | max length 64 | — | — | `setProductAttributes` body |
| Name `axes[].name` | text field | required | — | max length 200 | — | — | `setProductAttributes` body |
| Values `axes[].values` | repeatable rows | required | — | at least 1 | — | — | `setProductAttributes` body |
| Code `axes[].values[].code` | text field | required | — | max length 64 | — | — | `setProductAttributes` body |
| Label `axes[].values[].label` | text field | required | — | max length 200 | — | — | `setProductAttributes` body |
| Price delta `axes[].values[].priceDelta` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setProductAttributes` body |
| Duration minutes `axes[].values[].durationMinutes` | number field (minutes) | optional | — | min 15; max 1440; One axis per product at most may carry it; a second is a `400`. | — | How long a variant carrying this value books its space for, on a `length` axis of a product with `requiresTimeWindow` (decided 29 September, rev 3 REV3-13). | `setProductAttributes` body |

Errors to draw in the form: 400 Two axes share a code, or one axis repeats a value code.; 403 Authenticated but not permitted at the requested scope; 409 Regeneration would exceed the variant ceiling for this product: `VenueSettings.catalogue.maxVariantsPerProduct`, a venue setting with a tenant default (decided …

**Form: Transition product lifecycle** (modal, opened by *Transition product lifecycle*; *Transition product lifecycle* calls `transitionProductLifecycle`, *Cancel* sends nothing)

**Collects what `transitionProductLifecycle` sends before it is called.** Required: `transition`, `reason`. Optional: `effectiveAt`. The transition picker lists only what the principal may do — approve needs `PRODUCT_APPROVE`, publish needs `PRODUCT_PUBLISH` (decided 28 September, audit R091 (2)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Transition `transition` | select | required | — | Submit for review · Approve · Reject · Publish · Withdraw · Archive · Restore | — | — | `transitionProductLifecycle` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `transitionProductLifecycle` body |
| Effective at `effectiveAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `transitionProductLifecycle` body |

Errors to draw in the form: 403 Approval attempted by the principal who submitted it (`approver-is-submitter`). Segregation applies here as it does to journals.; 409 Transition not valid from the current state, or archiving attempted while unexpired entitlements exist.

**Form: Save product** (modal, opened by *Save product*; *Save product* calls `updateProduct`, *Cancel* sends nothing)

**Collects what `updateProduct` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `channels`, `dataMaskValues`, `guestListing`, `notBookableLabel`, `displayTags`, `media`, `consentQuestionIds`, `requiresTimeWindow` (decided 29 September, rev 3 REV3-14, 23SEP-3, 23SEP-4, REV3-26, REV3-13), `salesContact` (W3) and `bookingFlowId` (W8, W12), decided 29 September. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Family key `familyKey` | text field | optional | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; At most one product per venue in a family, else `409 duplicate-code`. | — | The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. | `updateProduct` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `updateProduct` body |
| Description `description` | text area | optional | — | — | — | — | `updateProduct` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `updateProduct` body |
| Data mask values `dataMaskValues` | key and value settings | optional | — | — | — | — | `updateProduct` body |
| Guest listing `guestListing` | segmented control | optional | Bookable | Bookable · Info only · Hidden; `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. | — | How a product appears to a guest (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. | `updateProduct` body |
| Not bookable label `notBookableLabel` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateProduct` body |
| Sales contact `salesContact` | group | optional | — | — | — | See `Product.salesContact` (W3, 29 September). | `updateProduct` body |
| Phone `salesContact.phone` | phone field | optional | — | max length 32 | +971 5X XXX XXXX (E.164) | — | `updateProduct` body |
| Email `salesContact.email` | email field | optional | — | max length 254 | name@example.ae | — | `updateProduct` body |
| Note `salesContact.note` | text, one per language | optional | — | At most 200 characters per language. | English and Arabic (Arabic right to left) | A line shown under the contact, e.g. *Group courses are booked by phone*. | `updateProduct` body |
| Booking flow `bookingFlowId` | picker: choose a booking flow | optional | — | — | shows names, sends the id | See `Product.bookingFlowId` (W8, W12, 29 September). | `updateProduct` body |
| Display tags `displayTags` | repeatable rows | optional | — | at most 6 | — | — | `updateProduct` body |
| Kind `displayTags[].kind` | radio group | required | — | Clock · Height · Free · Calendar · ID | — | `clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring. | `updateProduct` body |
| Label `displayTags[].label` | text, one per language | required | — | Each language value at most 40 characters. | English and Arabic (Arabic right to left) | What the guest reads, e.g. *2 Hours*. | `updateProduct` body |
| Media `media` | repeatable rows | optional | — | at most 20 | — | — | `updateProduct` body |
| Asset `media[].assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | A `MediaAsset` of `assets.yaml`, in status `ready`. | `updateProduct` body |
| Kind `media[].kind` | segmented control | required | — | Image · Video | — | — | `updateProduct` body |
| Is primary `media[].isPrimary` | toggle | required | off | — | — | The item *Read more* opens on and a listing shows. Exactly one per product. | `updateProduct` body |
| Display order `media[].displayOrder` | number field | optional | 100 | — | — | — | `updateProduct` body |
| Alt text `media[].altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateProduct` body |
| Consent questions `consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates | — | — | `updateProduct` body |
| Requires time window `requiresTimeWindow` | toggle | optional | — | — | — | — | `updateProduct` body |

Errors to draw in the form: 400 `media` with no `isPrimary` item or more than one, or one asset twice.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A `media` asset that is not `ready` or whose kind does not match, a `consentQuestionIds` entry that names no active consent question of the tenant, or …

**Form: Create merchandise** (modal, opened by *Create merchandise*; *Create merchandise* calls `createMerchandise`, *Cancel* sends nothing)

**Collects what `createMerchandise` sends before it is called.** Required: `sku`, `name`, `outletId`, `variantId`. Optional: `barcode`, `description`, `categoryId`, `inventoryItemId`, `isReturnable`, `returnWindowDays`, `requiresSerialNumber`, `imageAssetRef`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| SKU `sku` | text field | required | — | max length 64 | — | — | `createMerchandise` body |
| Barcode `barcode` | text field | optional | — | max length 128 | — | — | `createMerchandise` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createMerchandise` body |
| Description `description` | text area | optional | — | — | — | What the item is, in the guest's words. Indexed for guest-app search. | `createMerchandise` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createMerchandise` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createMerchandise` body |
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createMerchandise` body |
| Inventory item `inventoryItemId` | picker: choose an inventory item | optional | — | — | shows names, sends the id | — | `createMerchandise` body |
| Is returnable `isReturnable` | toggle | optional | on | — | — | — | `createMerchandise` body |
| Return window days `returnWindowDays` | number field (days) | optional | — | — | — | — | `createMerchandise` body |
| Requires serial number `requiresSerialNumber` | toggle | optional | off | — | — | — | `createMerchandise` body |
| Image `imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createMerchandise` body |

Errors to draw in the form: 400 Validation failed; 409 Barcode already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem)

**Form: Bulk update products** (modal, opened by *Bulk update products*; *Bulk update products* calls `bulkUpdateProducts`, *Cancel* sends nothing)

**Collects what `bulkUpdateProducts` sends before it is called.** Required: `selector`, `changes`. Optional: `previewOnly`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Preview only `previewOnly` | toggle | optional | on | — | — | — | `bulkUpdateProducts` body |
| Selector `selector` | key and value settings | required | — | — | — | — | `bulkUpdateProducts` body |
| Changes `changes` | key and value settings | required | — | — | — | — | `bulkUpdateProducts` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**Every alternative code** (data table, from `listAlternativeCodes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Partner | the name it points at, never the id | — |
| Partner name | text | — |
| Variant | the name it points at, never the id | — |
| Note | text | — |

**Every product variant** (data table, from `listProductVariants`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| SKU | text | — |
| Axis values | grouped details | — |
| Name | text | Taken from their variant tables, 20 September. `axisValues` gives `{size: L}` and no string a guest can read. |
| Barcode | text | Taken from their variant tables, 20 September. `catalogue.alternative_code` is a partner's own code for a variant and requires `partnerId` … |
| Is default | yes / no (icon or chip) | Taken from their variant tables. Which variant a product page opens on. |
| Is active | yes / no (icon or chip) | False when retired. Retired variants are never deleted — orders reference them. |

**Every menu** (data table, from `listMenus`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Availability | grouped details | When this menu is in force. Absent means always. |
| Sections | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |
| Published version | 1,234 | The `MenuVersion.version` live now. Null for a menu never published. |
| Published at | 1 Oct 2026, 14:30 | — |

**Every merchandise** (data table, from `listMerchandise`)

| Shows | Format | Notes |
|---|---|---|
| Description | text | What the item is, in the guest's words. Indexed for guest-app search. |
| ID | the name it points at, never the id | — |
| SKU | text | — |
| Barcode | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Variant | the name it points at, never the id | The catalogue variant sold. Price and tax come from there. |
| Inventory item | the name it points at, never the id | The stock item depleted on sale. Null means the item sells but never runs out, which is almost always a configuration error. |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| On hand | 1,234.5 | — |
| Is returnable | yes / no (icon or chip) | — |

**The selected product** (detail panel, from `getProduct`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create product (primary button) | `createProduct` POST `/products` | CreateProductRequest | Product | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names … | opens modal first |
| Resolve product by code (secondary button) | `resolveProductByCode` GET `/products/resolve` | — | ProductVariant | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save alternative codes (secondary button) | `setAlternativeCodes` PUT `/products/{productId}/alternative-codes` | inline | AlternativeCode[] | 400 A `variantId` is not a variant of this product, or the body sends one code twice for the same partner.; 409 Code already mapped to a different product for that partner | opens modal first |
| Save product attributes (secondary button) | `setProductAttributes` PUT `/products/{productId}/attributes` | inline | inline | 400 Two axes share a code, or one axis repeats a value code.; 403 Authenticated but not permitted at the requested scope; 409 Regeneration would exceed the variant ceiling for this product … | opens modal first |
| Transition product lifecycle (secondary button) | `transitionProductLifecycle` POST `/products/{productId}/lifecycle` | inline | Product | 403 Approval attempted by the principal who submitted it (`approver-is-submitter`). Segregation applies here as it does to journals.; 409 Transition not valid from the current state, or archiving attempted while … | opens modal first |
| Save product (secondary button) | `updateProduct` PATCH `/products/{productId}` | UpdateProductRequest | Product | 400 `media` with no `isPrimary` item or more than one, or one asset twice.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a … | opens modal first |
| Create merchandise (secondary button) | `createMerchandise` POST `/merchandise` | CreateMerchandiseRequest | MerchandiseItem | 400 Validation failed; 409 Barcode already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem) | opens modal first |
| Bulk update products (secondary button) | `bulkUpdateProducts` POST `/products/bulk` | inline | inline | — | opens modal first |

**Data it reads**: `listProducts` (onLoad, List products); `listMenus` (onLoad, List menus); `listMerchandise` (onLoad, List merchandise)

**Where the user goes next**

- → `BO-112` Production Planning & Production Sheets: *Production Planning & Production Sheets*
- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `productId`, `variantId`
- → `BO-009` Pricing Rules: *Pricing Rules*
- → `BO-010` Promotions & Coupons: *Promotions & Coupons*; carries `code`
- → `BO-045` Menu Management: *Menu Management*; carries `menuId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product yet. Offers Create product (`createProduct`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind, isSellable and the product are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A `variantId` is not a variant of this product, or the body sends one code twice for the same partner.; 400 Two axes share a code, or one axis repeats a value code.; 400 Validation failed |

#### Permissions

- `listBookingFlows` → `TENANT_CONFIGURE` (configure) · staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `createProduct` → `PRODUCT_CONFIGURE` (configure) · staff
- `listAlternativeCodes` → `PRODUCT_VIEW` (read) · staff, partner
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `resolveProductByCode` → `PRODUCT_VIEW` (read) · staff, partner
- `setAlternativeCodes` → `PRODUCT_CONFIGURE` (configure) · staff
- `setProductAttributes` → `PRODUCT_CONFIGURE` (configure) · staff
- `transitionProductLifecycle` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateProduct` → `PRODUCT_CONFIGURE` (configure) · staff
- `createMerchandise` → `PRODUCT_CONFIGURE` (configure) · staff
- `listMenus` → `PRODUCT_VIEW` (read) · staff
- `listMerchandise` → `PRODUCT_VIEW` (read) · staff, guest
- `bulkUpdateProducts` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

75 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.21 | VIP Package Purchases - System shall support VIP package purchases. | Guest Mobile App & Branding | CONTRACTED | `createProduct` |
| 1.1.1 | The system should be able to sell open-dated tickets for attractions. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.6 | The system should be able to sell membership passes for an attraction (e.g. annual pass, monthly pass) for configurable duration. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.8 | The system should be able to sell add-on items for all type of tickets. Add-ons can also be configured as a stand-alone product and able to be purchased on their own. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.42 | Configure unlimited ticket products and categories | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.44 | Support admission, membership, voucher, package and pass products | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.93 | Membership product management | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.124 | Channel-based restrictions | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.3.52 | Wall climbing activities (product management, sales, ticketing, bookings). | Ticketing Catalogue | CONTRACTED | `createProduct` |
| … 63 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Identity & classification: product name, product ID, main/sub-category, venue (multi-venue), ticket type. A category hierarchy manager groups and sorts packages and ticket types (e.g. admission > general admission > single-day, multi-day, annual pass, packages, vouchers). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-441)*
- Product lifecycle dashboard shows counts of products in draft, in approval and published, filterable by venue/department; every product must be authorised before publishing online or on-site. *(client request · MoM 25 Aug 2026, 4.1 Product / Ticket Catalog Creation · DI-438)*
- Ticket configuration flow runs basic information → ticket type configuration → validation → publish. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-432)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-007` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 2.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 2.dc.html#fnb-2c`, `Retail Board 2.dc.html#ret-2a`, `Retail Board 2.dc.html#ret-2b`
- Flow F78 *A supplier is set up and a catalogue is priced and published*, step 2: The new range becomes products in the directory. → **One product per sellable thing, with its barcodes.** A range that is not in the directory cannot be priced or scanned.
- Flow F85 *Production is planned, costed and released*, step 4: Product Directory. → **Drawn by the client as FNB-2C.** 4 operations on this step.
- Flow F93 *A recipe changes and its allergen claim is re-verified*, step 4: Product Directory. → **Drawn by the client as FNB-2C.**
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (86), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (62 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create product, Resolve product by code, Save alternative codes, Save product attributes, Transition product lifecycle, Save product, Create merchandise, Bulk update products.
- [ ] Every transition is wired: `BO-112`, `BO-008`, `BO-009`, `BO-010`, `BO-045`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-009` Pricing Rules

**Set what something costs, and when that changes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #20669 (APP-SETUP-BO-009) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPriceLists` reads the population and `getPriceList` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `priceListId` (deepLink), `ruleId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/pricing-rules` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 1 board screen(s): Price Book & Retail Pricing Management. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel | select | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | Sends `?channel=` to `listPriceLists`. | `listPriceLists` ?channel |

**Form: Create price list** (modal, opened by *Create price list*; *Create price list* calls `createPriceList`, *Cancel* sends nothing)

**Collects what `createPriceList` sends before it is called.** Required: `code`, `name`, `venueId`, `channels`. Optional: `validFrom`, `validTo`, `priority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createPriceList` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createPriceList` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createPriceList` body |
| Channels `channels` | multi-select chips | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre; at least 1 | — | — | `createPriceList` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPriceList` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPriceList` body |
| Priority `priority` | number field | optional | 0 | — | — | — | `createPriceList` body |

Errors to draw in the form: 400 Validation failed

**Form: Copy price list** (modal, opened by *Copy price list*; *Copy price list* calls `copyPriceList`, *Cancel* sends nothing)

**Collects what `copyPriceList` sends before it is called.** Required: `code`, `name`. Optional: `adjustmentPercent`, `roundTo`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `copyPriceList` body |
| Name `name` | text field | required | — | max length 200 | — | — | `copyPriceList` body |
| Adjustment percent `adjustmentPercent` | number field | optional | — | — | — | Applied to every copied price. Negative reduces. | `copyPriceList` body |
| Round to `roundTo` | text field | optional | — | pattern `^\d+(\.\d{1,4})?$` | — | Round adjusted prices to this increment, e.g. `0.5` or `5`. | `copyPriceList` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `copyPriceList` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `copyPriceList` body |

**Form: Save prices** (modal, opened by *Save prices*; *Save prices* calls `setPrices`, *Cancel* sends nothing)

**Collects what `setPrices` sends before it is called.** Required: `prices`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Prices `prices` | repeatable rows | required | — | at most 5000 | — | — | `setPrices` body |
| Variant `prices[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `setPrices` body |
| Amount `prices[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPrices` body |
| Tax code `prices[].taxCodeId` | picker: choose a tax code | optional | — | — | shows names, sends the id | — | `setPrices` body |

Errors to draw in the form: 400 Currency or scale mismatch against the region

**Form: Save price list** (modal, opened by *Save price list*; *Save price list* calls `updatePriceList`, *Cancel* sends nothing)

**Collects what `updatePriceList` sends before it is called.** Nothing in the body is required. Optional: `name`, `validFrom`, `validTo`, `priority`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updatePriceList` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePriceList` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePriceList` body |
| Priority `priority` | number field | optional | — | — | — | — | `updatePriceList` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updatePriceList` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every price list** (data table, from `listPriceLists`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Channels | list or chips (count when long) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Priority | 1,234 | Where lists overlap, higher priority wins. |

**Every price** (data table, from `listPrices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Price list | the name it points at, never the id | — |
| Variant | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax code | the name it points at, never the id | — |

**The selected price list** (detail panel, from `getPriceList`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and … |
| Channels | list or chips (count when long) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Priority | 1,234 | Where lists overlap, higher priority wins. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create price list (primary button) | `createPriceList` POST `/price-lists` | CreatePriceListRequest | PriceList | 400 Validation failed | opens modal first |
| Copy price list (secondary button) | `copyPriceList` POST `/price-lists/{priceListId}/copy` | inline | inline | — | opens modal first |
| Save prices (secondary button) | `setPrices` PUT `/price-lists/{priceListId}/prices` | inline | inline | 400 Currency or scale mismatch against the region | opens modal first |
| Save price list (secondary button) | `updatePriceList` PATCH `/price-lists/{priceListId}` | inline | PriceList | — | opens modal first |

**Data it reads**: `listPriceLists` (onLoad, List price lists); `listDynamicPriceRules` (onLoad, Dynamic price rules)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*; carries `productId`
- → `BO-010` Promotions & Coupons: *Promotions & Coupons*; carries `code`
- → `BO-014` Catalogue Publishing: *The priced range is published to the tills*; carries `priceListId`, `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing rules yet. Offers Create price list (`createPriceList`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on channel and the pricing rules are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRICE_VIEW`, which `listPriceLists` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Currency or scale mismatch against the region; 400 Validation failed |

#### Permissions

- `listPriceLists` → `PRICE_VIEW` (read) · staff, partner
- `listPrices` → `PRICE_VIEW` (read) · staff, partner
- `createPriceList` → `PRICE_CONFIGURE` (configure) · staff
- `copyPriceList` → `PRICE_CONFIGURE` (configure) · staff
- `getPriceList` → `PRICE_VIEW` (read) · staff, partner
- `setPrices` → `PRICE_CONFIGURE` (configure) · staff
- `updatePriceList` → `PRICE_CONFIGURE` (configure) · staff
- `bulkChangePrices` → `PRODUCT_CONFIGURE` (configure) · staff
- `listDynamicPriceRules` → `PRICE_VIEW` (read) · staff
- `getDynamicPriceRule` → `PRICE_VIEW` (read) · staff
- `setDynamicPriceRule` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRICE_VIEW`, which `listPriceLists` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

19 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.22 | Dynamic Pricing Display - System shall display dynamic pricing. | Guest Mobile App & Branding | CONTRACTED | `listPrices` |
| 2.9.8 | The system should be able to regroup prices by category: Full price / reduced price / complimentary. | Ticketing Sales | CONTRACTED | `listPrices` |
| 2.9.6 | The system should have the ability to - Create multiple pricelist templates, archive, copy, sort, hide and remove items. - Add several items to a list: full price, reduced price, group price, etc. … | Ticketing Sales | CONTRACTED | `copyPriceList` |
| 2.10.4 | The system should allow sales of free tickets. These tickets can be configured as a standard ticket with a price of zero or as a full price ticket with a 100% discount. | Ticketing Sales | CONTRACTED | `setPrices` |
| 7.4.17 | For each PLU, it is possible to manage its Unit price and the related currency | F&B POS | CONTRACTED | `setPrices` |
| 7.4.19 | For each PLU, it is possible to manage its VAT rate | F&B POS | CONTRACTED | `setPrices` |
| 2.9.9 | The system should have the ability to enact bulk price changes (i.e., whole category), including global changes. Example: Change price of all Admissions from one price to another. | Ticketing Sales | CONTRACTED | `bulkChangePrices` |
| 2.1.23 | POS shall retrieve real-time prices from the Dynamic Pricing Engine based on date, timeslot, demand, capacity, promotions, customer segment, and channel. | Ticketing Sales | CONTRACTED | `listDynamicPriceRules` |
| 2.6.17 | - Dynamic Pricing | Ticketing Sales | CONTRACTED | `setDynamicPriceRule` |
| 2.9.10 | The system should have the ability to setup dynamic pricing rules of onsite and digital tickets based on seasonality, day of the week, guest type, time of day, capacity and group size. | Ticketing Sales | CONTRACTED | `setDynamicPriceRule` |
| 2.13.39 | Dynamic Pricing Support | Ticketing Sales | CONTRACTED | `setDynamicPriceRule` |
| 8.5.5 | System shall support seasonal pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| … 7 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price Book supports date-based pricing (regular this month, promotional next month). Promotion Builder supports rules such as "buy X get Y", "buy 2 get 1 free" and "buy 3, lowest-priced item discounted" (fully or partially). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog; 4.3 Pricing, Bundles & Promotions · DI-357)*
- Product record holds: price (tax inclusive/exclusive), linked print template, system product code, a toggle for capturing reservation details at sale, and entitlements (upgradeable, stored-value load, linked event, re-entry, linked performance). Multiple price lists per channel and season (winter/summer). *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-163)*
- Prices are set per channel (web store, mobile app, kiosk, walk-up/POS) in one centralised "price matrix"; each channel picks up its price automatically once published. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-140)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-009` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 2.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 2.dc.html#ret-2f`
- Flow F78 *A supplier is set up and a catalogue is priced and published*, step 3: The range is priced. → What the tills will charge, from when.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create price list, Copy price list, Save prices, Save price list.
- [ ] Every transition is wired: `BO-007`, `BO-010`, `BO-014`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-010` Promotions & Coupons

**Issue a code and control what it does.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | Block A · ticket #18008 (APP-SETUP-BO-010) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW`, `REPORT_VIEW_VENUE` (1 configure, 1 read, 1 operate); in the flows as marketer |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPromotions` reads the population and `getPromotion` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `campaignId` (deepLink), `dashboardId` (deepLink), `promotionId` (deepLink), `reportId` (deepLink), `code` (deepLink), `voucherId` (navigation) · cold entry: A dashboard opened from a link or a saved view. A coupon code opened from the list, or scanned at a till. |
| Route | `/venue-operations/promotions-coupons` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 6 board screen(s): Retail Commercial Command Center; Promotion & Offer Builder; Promotion Eligibility, Priority & Conflict Rules and 3 more. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real. **Owns POS board frame(s) POS-4E** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Retail board operations wired 24 August.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listPromotions`. | `listPromotions` ?venueId |
| Status | select | optional | — | Draft · Scheduled · Live · Paused · Expired · Ended | — | Sends `?status=` to `listPromotions`. | `listPromotions` ?status |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listPromotions`. | `listPromotions` ?activeAt |
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?venueId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?activeAt |
| Owner principal id | picker: choose an owner principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ownerPrincipalId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?ownerPrincipalId |
| Q | text field | optional | — | max length 100 | — | Sends `?q=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?q |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |

**Form: Create coupon campaign** (modal, opened by *Create coupon campaign*; *Create coupon campaign* calls `createCouponCampaign`, *Cancel* sends nothing)

**Collects what `createCouponCampaign` sends before it is called.** Required: `code`, `name`, `venueId`, `discount`, `validFrom`. Optional: `conditions`, `isSingleUse`, `maxRedemptionsPerCode`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createCouponCampaign` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createCouponCampaign` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createCouponCampaign` body |
| Discount `discount` | group | required | — | — | — | — | `createCouponCampaign` body |
| Kind `discount.kind` | select | required | — | Percentage · Fixed amount · Fixed price · Buy x get y · Free item · Tiered percentage | — | — | `createCouponCampaign` body |
| Percentage `discount.percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `createCouponCampaign` body |
| Amount `discount.amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createCouponCampaign` body |
| Fixed price `discount.fixedPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createCouponCampaign` body |
| Buy quantity `discount.buyQuantity` | number field | optional | — | min 1 | — | — | `createCouponCampaign` body |
| Get quantity `discount.getQuantity` | number field | optional | — | min 1 | — | — | `createCouponCampaign` body |
| Get discount percentage `discount.getDiscountPercentage` | stepper or slider | optional | — | min 0; max 100 | — | 100 makes the free items actually free; lower values give a partial discount. | `createCouponCampaign` body |
| Tiers `discount.tiers` | repeatable rows | optional | — | — | — | For `tieredPercentage` — more units, larger discount. | `createCouponCampaign` body |
| Min quantity `discount.tiers[].minQuantity` | number field | required | — | min 1 | — | — | `createCouponCampaign` body |
| Percentage `discount.tiers[].percentage` | stepper or slider (%) | required | — | min 0; max 100 | — | — | `createCouponCampaign` body |
| Max discount amount `discount.maxDiscountAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Cap on a percentage discount. Prevents an unbounded discount on a large basket. | `createCouponCampaign` body |
| Reward variants `discount.rewardVariantIds` | multi-picker: choose reward variants | optional | — | — | — | The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the "different product" of a `buyXGetY` (setGiftFreeProduct, setBuyGetBogo). | `createCouponCampaign` body |
| Max applications per basket `discount.maxApplicationsPerBasket` | number field | optional | — | min 1 | — | How many times the offer repeats in one basket: the "maximum repetitions" of an N-for-X offer (setFixedPriceOffer). | `createCouponCampaign` body |
| Conditions `conditions` | group | optional | — | — | — | All conditions must hold. An empty object matches everything. | `createCouponCampaign` body |
| Variants `conditions.variantIds` | multi-picker: choose variants | optional | — | — | — | — | `createCouponCampaign` body |
| Product kinds `conditions.productKinds` | list of values (chips) | optional | — | — | — | — | `createCouponCampaign` body |
| Categorys `conditions.categoryIds` | multi-picker: choose categorys | optional | — | — | — | — | `createCouponCampaign` body |
| Min quantity `conditions.minQuantity` | number field | optional | — | min 1 | — | — | `createCouponCampaign` body |
| Min basket value `conditions.minBasketValue` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createCouponCampaign` body |
| Channels `conditions.channels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Empty or absent matches every channel. | `createCouponCampaign` body |
| Purchase gate `conditions.purchaseGate` | toggle | optional | off | True makes these conditions a precondition of purchase: fail them and the line cannot be added, not merely charged more. | — | BL-037. `evaluatePromotions` gates a price and nothing gated a sale. | `createCouponCampaign` body |
| Payment method `conditions.paymentMethod` | list of values (chips) | optional | — | — | — | BL-113. Card-issuer and payment-type promotions — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible. | `createCouponCampaign` body |
| Issuer bins `conditions.issuerBins` | list of values (chips) | optional | — | — | — | Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. | `createCouponCampaign` body |
| Component redemption `conditions.componentRedemption` | segmented control | optional | — | All together · Independently · Sequenced | — | BL-112. Per-component redemption inside a bundle was unstated. | `createCouponCampaign` body |
| Days of week `conditions.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createCouponCampaign` body |
| Start time `conditions.startTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | — | `createCouponCampaign` body |
| End time `conditions.endTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | — | `createCouponCampaign` body |
| Membership tiers `conditions.membershipTierIds` | multi-picker: choose membership tiers | optional | — | — | — | — | `createCouponCampaign` body |
| Requires coupon `conditions.requiresCoupon` | toggle | optional | off | — | — | — | `createCouponCampaign` body |
| First purchase only `conditions.firstPurchaseOnly` | toggle | optional | off | — | — | — | `createCouponCampaign` body |
| Performances `conditions.performanceIds` | multi-picker: choose performances | optional | — | — | — | — | `createCouponCampaign` body |
| Advance days min `conditions.advanceDaysMin` | number field | optional | — | — | — | Early-bird — booked at least this many days ahead. | `createCouponCampaign` body |
| Advance days max `conditions.advanceDaysMax` | number field | optional | — | — | — | Last-minute — booked no more than this many days ahead. | `createCouponCampaign` body |
| Eligibility rules `conditions.eligibilityRuleIds` | multi-picker: choose eligibility rules | optional | — | — | — | Reusable eligibility rules (`promotions.promotion_rule` rows of `ruleType: eligibility` with no promotion of their own, saved by setEligibilityRule) that must also hold. | `createCouponCampaign` body |
| Is single use `isSingleUse` | toggle | optional | on | — | — | True generates individually redeemable codes. False issues one shared code with a redemption limit. | `createCouponCampaign` body |
| Max redemptions per code `maxRedemptionsPerCode` | number field | optional | 1 | — | — | — | `createCouponCampaign` body |
| Valid from `validFrom` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCouponCampaign` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCouponCampaign` body |
| Campaign `campaignId` | picker: choose a campaign | optional | — | — | shows names, sends the id | The commercial campaign (`promotions.campaign`) the codes are issued under, as the Coupon & Promo Code Builder names it. | `createCouponCampaign` body |

**Form: Create promotion** (modal, opened by *Create promotion*; *Create promotion* calls `createPromotion`, *Cancel* sends nothing)

**Collects what `createPromotion` sends before it is called.** Required: `code`, `name`, `venueId`, `discount`, `validFrom`. Optional: `description`, `conditions`, `stackingMode`, `stackingGroup`, `precedence`, `validTo`, `maxRedemptions`, `maxRedemptionsPerGuest`, `budgetCap`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9_-]+$` | — | — | `createPromotion` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createPromotion` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createPromotion` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createPromotion` body |
| Discount `discount` | group | required | — | — | — | — | `createPromotion` body |
| Kind `discount.kind` | select | required | — | Percentage · Fixed amount · Fixed price · Buy x get y · Free item · Tiered percentage | — | — | `createPromotion` body |
| Percentage `discount.percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `createPromotion` body |
| Amount `discount.amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPromotion` body |
| Fixed price `discount.fixedPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPromotion` body |
| Buy quantity `discount.buyQuantity` | number field | optional | — | min 1 | — | — | `createPromotion` body |
| Get quantity `discount.getQuantity` | number field | optional | — | min 1 | — | — | `createPromotion` body |
| Get discount percentage `discount.getDiscountPercentage` | stepper or slider | optional | — | min 0; max 100 | — | 100 makes the free items actually free; lower values give a partial discount. | `createPromotion` body |
| Tiers `discount.tiers` | repeatable rows | optional | — | — | — | For `tieredPercentage` — more units, larger discount. | `createPromotion` body |
| Min quantity `discount.tiers[].minQuantity` | number field | required | — | min 1 | — | — | `createPromotion` body |
| Percentage `discount.tiers[].percentage` | stepper or slider (%) | required | — | min 0; max 100 | — | — | `createPromotion` body |
| Max discount amount `discount.maxDiscountAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Cap on a percentage discount. Prevents an unbounded discount on a large basket. | `createPromotion` body |
| Reward variants `discount.rewardVariantIds` | multi-picker: choose reward variants | optional | — | — | — | The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the "different product" of a `buyXGetY` (setGiftFreeProduct, setBuyGetBogo). | `createPromotion` body |
| Max applications per basket `discount.maxApplicationsPerBasket` | number field | optional | — | min 1 | — | How many times the offer repeats in one basket: the "maximum repetitions" of an N-for-X offer (setFixedPriceOffer). | `createPromotion` body |
| Conditions `conditions` | group | optional | — | — | — | All conditions must hold. An empty object matches everything. | `createPromotion` body |
| Variants `conditions.variantIds` | multi-picker: choose variants | optional | — | — | — | — | `createPromotion` body |
| Product kinds `conditions.productKinds` | list of values (chips) | optional | — | — | — | — | `createPromotion` body |
| Categorys `conditions.categoryIds` | multi-picker: choose categorys | optional | — | — | — | — | `createPromotion` body |
| Min quantity `conditions.minQuantity` | number field | optional | — | min 1 | — | — | `createPromotion` body |
| Min basket value `conditions.minBasketValue` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createPromotion` body |
| Channels `conditions.channels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Empty or absent matches every channel. | `createPromotion` body |
| Purchase gate `conditions.purchaseGate` | toggle | optional | off | True makes these conditions a precondition of purchase: fail them and the line cannot be added, not merely charged more. | — | BL-037. `evaluatePromotions` gates a price and nothing gated a sale. | `createPromotion` body |
| Payment method `conditions.paymentMethod` | list of values (chips) | optional | — | — | — | BL-113. Card-issuer and payment-type promotions — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible. | `createPromotion` body |
| Issuer bins `conditions.issuerBins` | list of values (chips) | optional | — | — | — | Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. | `createPromotion` body |
| Component redemption `conditions.componentRedemption` | segmented control | optional | — | All together · Independently · Sequenced | — | BL-112. Per-component redemption inside a bundle was unstated. | `createPromotion` body |
| Days of week `conditions.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createPromotion` body |
| Start time `conditions.startTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | — | `createPromotion` body |
| End time `conditions.endTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | — | `createPromotion` body |
| Membership tiers `conditions.membershipTierIds` | multi-picker: choose membership tiers | optional | — | — | — | — | `createPromotion` body |
| Requires coupon `conditions.requiresCoupon` | toggle | optional | off | — | — | — | `createPromotion` body |
| First purchase only `conditions.firstPurchaseOnly` | toggle | optional | off | — | — | — | `createPromotion` body |
| Performances `conditions.performanceIds` | multi-picker: choose performances | optional | — | — | — | — | `createPromotion` body |
| Advance days min `conditions.advanceDaysMin` | number field | optional | — | — | — | Early-bird — booked at least this many days ahead. | `createPromotion` body |
| Advance days max `conditions.advanceDaysMax` | number field | optional | — | — | — | Last-minute — booked no more than this many days ahead. | `createPromotion` body |
| Eligibility rules `conditions.eligibilityRuleIds` | multi-picker: choose eligibility rules | optional | — | — | — | Reusable eligibility rules (`promotions.promotion_rule` rows of `ruleType: eligibility` with no promotion of their own, saved by setEligibilityRule) that must also hold. | `createPromotion` body |
| Stacking mode `stackingMode` | radio group | optional | Best only | Exclusive · Stackable · Best only · Stack with group | — | How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine into a free ticket. | `createPromotion` body |
| Stacking group `stackingGroup` | text field | optional | — | max length 64 | — | — | `createPromotion` body |
| Precedence `precedence` | number field | optional | 0 | — | — | Higher evaluates first where several could apply. | `createPromotion` body |
| Valid from `validFrom` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPromotion` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPromotion` body |
| Max redemptions `maxRedemptions` | number field | optional | — | — | — | — | `createPromotion` body |
| … 5 more | | | | | | the rest are in `schemas.json` | `createPromotion` body |

Errors to draw in the form: 400 Conditions are unsatisfiable, or the discount exceeds the configured cap. The cap is `VenueSettings.promotions.maxDiscountPercent`, a venue setting with a …

**Form: End promotion** (modal, opened by *End promotion*; *End promotion* calls `endPromotion`, *Cancel* sends nothing)

**Collects what `endPromotion` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `endPromotion` body |

Errors to draw in the form: 409 Not in a state that permits this

**Form: Evaluate promotions** (modal, opened by *Evaluate promotions*; *Evaluate promotions* calls `evaluatePromotions`, *Cancel* sends nothing)

**Collects what `evaluatePromotions` sends before it is called.** Required: `venueId`, `channel`, `lines`. Optional: `subjectId`, `membershipTierId`, `couponCodes`, `evaluateAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Channel `channel` | select | required | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary. | `evaluatePromotions` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Membership tier `membershipTierId` | picker: choose a membership tier | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Coupon codes `couponCodes` | list of values (chips) | optional | — | — | — | — | `evaluatePromotions` body |
| Evaluate at `evaluateAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | For back-office testing of a rule before publishing. | `evaluatePromotions` body |
| Order `orderId` | picker: choose an order | optional | — | — | shows names, sends the id | The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one … | `evaluatePromotions` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `evaluatePromotions` body |
| Line `lines[].lineId` | text field | required | — | — | — | — | `evaluatePromotions` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `evaluatePromotions` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `evaluatePromotions` body |
| Unit price `lines[].unitPrice` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `evaluatePromotions` body |

Errors to draw in the form: 400 Validation failed

**Form: Generate coupon codes** (modal, opened by *Generate coupon codes*; *Generate coupon codes* calls `generateCouponCodes`, *Cancel* sends nothing)

**Collects what `generateCouponCodes` sends before it is called.** Required: `quantity`. Optional: `prefix`, `length`, `assignToSubjectIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Quantity `quantity` | number field | required | — | min 1; max 50000 | — | — | `generateCouponCodes` body |
| Prefix `prefix` | text field | optional | — | max length 16 | — | — | `generateCouponCodes` body |
| Length `length` | stepper or slider | optional | 12 | min 6; max 32 | — | — | `generateCouponCodes` body |
| Assign to subjects `assignToSubjectIds` | multi-picker: choose assign to subjects | optional | — | at most 50000 | — | Personalised codes bound to named guests. Omit for anonymous codes. | `generateCouponCodes` body |

Errors to draw in the form: 400 More guests in `assignToSubjectIds` than `quantity` codes (audit R101)

**Form: Pause promotion** (modal, opened by *Pause promotion*; *Pause promotion* calls `pausePromotion`, *Cancel* sends nothing)

**Collects what `pausePromotion` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `pausePromotion` body |

Errors to draw in the form: 409 Not in a state that permits this

**Form: Save promotion** (modal, opened by *Save promotion*; *Save promotion* calls `updatePromotion`, *Cancel* sends nothing)

**Collects what `updatePromotion` sends before it is called.** Nothing in the body is required. Optional: `name`, `validTo`, `isPaused`, `conditions`, `discount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updatePromotion` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePromotion` body |
| Is paused `isPaused` | toggle | optional | — | — | — | — | `updatePromotion` body |
| Conditions `conditions` | group | optional | — | — | — | All conditions must hold. An empty object matches everything. | `updatePromotion` body |
| Variants `conditions.variantIds` | multi-picker: choose variants | optional | — | — | — | — | `updatePromotion` body |
| Product kinds `conditions.productKinds` | list of values (chips) | optional | — | — | — | — | `updatePromotion` body |
| Categorys `conditions.categoryIds` | multi-picker: choose categorys | optional | — | — | — | — | `updatePromotion` body |
| Min quantity `conditions.minQuantity` | number field | optional | — | min 1 | — | — | `updatePromotion` body |
| Min basket value `conditions.minBasketValue` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updatePromotion` body |
| Channels `conditions.channels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Empty or absent matches every channel. | `updatePromotion` body |
| Purchase gate `conditions.purchaseGate` | toggle | optional | off | True makes these conditions a precondition of purchase: fail them and the line cannot be added, not merely charged more. | — | BL-037. `evaluatePromotions` gates a price and nothing gated a sale. | `updatePromotion` body |
| Payment method `conditions.paymentMethod` | list of values (chips) | optional | — | — | — | BL-113. Card-issuer and payment-type promotions — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible. | `updatePromotion` body |
| Issuer bins `conditions.issuerBins` | list of values (chips) | optional | — | — | — | Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. | `updatePromotion` body |
| Component redemption `conditions.componentRedemption` | segmented control | optional | — | All together · Independently · Sequenced | — | BL-112. Per-component redemption inside a bundle was unstated. | `updatePromotion` body |
| Days of week `conditions.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `updatePromotion` body |
| Start time `conditions.startTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | — | `updatePromotion` body |
| End time `conditions.endTime` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | — | `updatePromotion` body |
| Membership tiers `conditions.membershipTierIds` | multi-picker: choose membership tiers | optional | — | — | — | — | `updatePromotion` body |
| Requires coupon `conditions.requiresCoupon` | toggle | optional | off | — | — | — | `updatePromotion` body |
| First purchase only `conditions.firstPurchaseOnly` | toggle | optional | off | — | — | — | `updatePromotion` body |
| Performances `conditions.performanceIds` | multi-picker: choose performances | optional | — | — | — | — | `updatePromotion` body |
| Advance days min `conditions.advanceDaysMin` | number field | optional | — | — | — | Early-bird — booked at least this many days ahead. | `updatePromotion` body |
| Advance days max `conditions.advanceDaysMax` | number field | optional | — | — | — | Last-minute — booked no more than this many days ahead. | `updatePromotion` body |
| Eligibility rules `conditions.eligibilityRuleIds` | multi-picker: choose eligibility rules | optional | — | — | — | Reusable eligibility rules (`promotions.promotion_rule` rows of `ruleType: eligibility` with no promotion of their own, saved by setEligibilityRule) that must also hold. | `updatePromotion` body |
| Discount `discount` | group | optional | — | — | — | — | `updatePromotion` body |
| Kind `discount.kind` | select | required | — | Percentage · Fixed amount · Fixed price · Buy x get y · Free item · Tiered percentage | — | — | `updatePromotion` body |
| Percentage `discount.percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `updatePromotion` body |
| Amount `discount.amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updatePromotion` body |
| Fixed price `discount.fixedPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updatePromotion` body |
| Buy quantity `discount.buyQuantity` | number field | optional | — | min 1 | — | — | `updatePromotion` body |
| Get quantity `discount.getQuantity` | number field | optional | — | min 1 | — | — | `updatePromotion` body |
| Get discount percentage `discount.getDiscountPercentage` | stepper or slider | optional | — | min 0; max 100 | — | 100 makes the free items actually free; lower values give a partial discount. | `updatePromotion` body |
| Tiers `discount.tiers` | repeatable rows | optional | — | — | — | For `tieredPercentage` — more units, larger discount. | `updatePromotion` body |
| Min quantity `discount.tiers[].minQuantity` | number field | required | — | min 1 | — | — | `updatePromotion` body |
| Percentage `discount.tiers[].percentage` | stepper or slider (%) | required | — | min 0; max 100 | — | — | `updatePromotion` body |
| Max discount amount `discount.maxDiscountAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Cap on a percentage discount. Prevents an unbounded discount on a large basket. | `updatePromotion` body |
| Reward variants `discount.rewardVariantIds` | multi-picker: choose reward variants | optional | — | — | — | The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the "different product" of a `buyXGetY` (setGiftFreeProduct, setBuyGetBogo). | `updatePromotion` body |
| Max applications per basket `discount.maxApplicationsPerBasket` | number field | optional | — | min 1 | — | How many times the offer repeats in one basket: the "maximum repetitions" of an N-for-X offer (setFixedPriceOffer). | `updatePromotion` body |

Errors to draw in the form: 409 Conditions or discount amended on a live promotion

**Form: Simulate promotion** (modal, opened by *Simulate promotion*; *Simulate promotion* calls `simulatePromotion`, *Cancel* sends nothing)

**Collects what `simulatePromotion` sends before it is called.** Required: `periodFrom`, `periodTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Period from `periodFrom` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `simulatePromotion` body |
| Period to `periodTo` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `simulatePromotion` body |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Sent by *Void coupon code*** (`voidCouponCode`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `voidCouponCode` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every promotion** (data table, from `listPromotions`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Discount | grouped details | — |
| Conditions | grouped details | All conditions must hold. An empty object matches everything. |
| Stacking mode | chip: Exclusive, Stackable, Best only, Stack with group | How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine … |
| Stacking group | text | — |
| Precedence | 1,234 | Higher evaluates first where several could apply. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Max redemptions | 1,234 | — |

**Every coupon campaign** (data table, from `listCouponCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Discount | grouped details | — |
| Conditions | grouped details | All conditions must hold. An empty object matches everything. |
| Is single use | yes / no (icon or chip) | True generates individually redeemable codes. False issues one shared code with a redemption limit. |
| Max redemptions per code | 1,234 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| ID | the name it points at, never the id | — |
| Generated count | 1,234 | — |
| Redeemed count | 1,234 | — |

**Every coupon code** (data table, from `listCouponCodes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Campaign | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `generateCouponCodes` batch that issued this code. Null where no batch did. |
| Status | chip: Issued, Assigned, Redeemed, Expired, Voided | — |
| Assigned subject | the name it points at, never the id | — |
| Redemption count | 1,234 | — |
| Max redemptions | 1,234 | — |
| Discount | grouped details | — |
| Invalid reason | chip: Expired, Already redeemed, Voided, Not yet valid, Wrong venue, Conditions not met… | Why the code cannot be applied. A cashier reading `expired` to a guest is a very different conversation from reading `already used`. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Redeemed at | 1 Oct 2026, 14:30 | — |

**Every commercial campaign** (data table, from `listCommercialCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Owner principal | the name it points at, never the id | The campaign (and budget) owner. |
| Legal entity | the name it points at, never the id | The business entity that funds and books the campaign. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Budgets | list or chips (count when long) | The rows of `promotions.campaign_budget`, one per budget line. |

**The selected promotion** (detail panel, from `getPromotion`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Discount | grouped details | — |
| Conditions | grouped details | All conditions must hold. An empty object matches everything. |
| Stacking mode | chip: Exclusive, Stackable, Best only, Stack with group | How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine … |
| Stacking group | text | — |
| Precedence | 1,234 | Higher evaluates first where several could apply. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Max redemptions | 1,234 | — |
| Max redemptions per guest | 1,234 | — |
| Budget cap | AED 1,234.50 | Total discount value after which the promotion stops automatically. Enforced at checkout, where an order whose discount would take the … |
| ID | the name it points at, never the id | — |
| Status | chip: Draft, Scheduled, Live, Paused, Expired, Ended | — |

**The promotion usage** (detail panel, from `getPromotionUsage`)

| Shows | Format | Notes |
|---|---|---|
| Promotion | the name it points at, never the id | — |
| Redemption count | 1,234 | — |
| Discount given | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Budget cap | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Budget remaining | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Is budget exhausted | yes / no (icon or chip) | — |
| By channel | list or chips (count when long) | — |

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
|  (publish gate) | navigation or local | — | — | — | — |
| Analyse promotion conflicts (primary button) | `analysePromotionConflicts` GET `/promotions/{promotionId}/conflicts` | — | ConflictAnalysis | — | — |
| Create coupon campaign (secondary button) | `createCouponCampaign` POST `/coupon-campaigns` | CreateCouponCampaignRequest | CouponCampaign | — | opens modal first |
| Create promotion (secondary button) | `createPromotion` POST `/promotions` | CreatePromotionRequest | Promotion | 400 Conditions are unsatisfiable, or the discount exceeds the configured cap. The cap is `VenueSettings.promotions.maxDiscountPercent`, a venue setting with a … | opens modal first |
| End promotion (secondary button) | `endPromotion` POST `/promotions/{promotionId}/end` | inline | no body | 409 Not in a state that permits this | opens modal first |
| Evaluate promotions (secondary button) | `evaluatePromotions` POST `/promotions/evaluate` | EvaluatePromotionsRequest | PromotionEvaluation | 400 Validation failed | opens modal first |
| Generate coupon codes (secondary button) | `generateCouponCodes` POST `/coupon-campaigns/{campaignId}/codes` | inline | inline | 400 More guests in `assignToSubjectIds` than `quantity` codes (audit R101) | opens modal first |
| Pause promotion (secondary button) | `pausePromotion` POST `/promotions/{promotionId}/pause` | inline | no body | 409 Not in a state that permits this | opens modal first |
| Publish promotion (secondary button) | `publishPromotion` POST `/promotions/{promotionId}/publish` | — | Promotion | 409 Conflict analysis failed. (StackingProblem) | — |
| Unschedule promotion (secondary button) | `unschedulePromotion` POST `/promotions/{promotionId}/unschedule` | — | no body | 409 Not in a state that permits this | — |
| Save promotion (secondary button) | `updatePromotion` PATCH `/promotions/{promotionId}` | inline | Promotion | 409 Conditions or discount amended on a live promotion | opens modal first |
| Simulate promotion (secondary button) | `simulatePromotion` POST `/promotions/{promotionId}/simulate` | inline | inline | — | opens modal first |
| Run report (secondary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Void coupon code (destructive button) | `voidCouponCode` POST `/coupon-codes/{code}/void` | inline | CouponCode | 409 Already redeemed. | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listPromotions` (onLoad, List promotions); `listCouponCampaigns` (onLoad, List coupon campaigns); `getDashboard` (onLoad, Read a dashboard with tile data); `listVoucherBatches` (onLoad, Voucher batches issued); `listCommercialCampaigns` (onLoad, List commercial campaigns); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*
- → `ANL-009` AI Assistant & Action Center: *AI Assistant & Action Center*; carries `reportId`

**What opens over it**

- confirmDialog *Void coupon code*: **Names what `voidCouponCode` changes and what it leaves alone**, in the consequence rather than the verb. A promotions coupons this affects should be identified in the dialog, not just counted. **Collects what `voidCouponCode` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotions coupons list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotions coupons untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotions coupons yet. Offers Create coupon campaign (`createCouponCampaign`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, status, activeAt and the promotions coupons are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRICE_VIEW`, which `listPromotions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Conditions are unsatisfiable, or the discount exceeds the configured cap. The cap is `VenueSettings.promotions.maxDiscountPercent`, a venue setting with a …; 400 More guests in `assignToSubjectIds` than `quantity` codes (audit R101); 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 400 The variants' … |

#### Permissions

- `listPromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `listCouponCampaigns` → `PRICE_VIEW` (read) · staff
- `analysePromotionConflicts` → `PRICE_VIEW` (read) · staff, partner
- `createCouponCampaign` → `PRICE_CONFIGURE` (configure) · staff
- `createPromotion` → `PRICE_CONFIGURE` (configure) · staff, partner
- `endPromotion` → `PRICE_CONFIGURE` (configure) · staff, partner
- `evaluatePromotions` → `PRICE_VIEW` (read) · staff, guest, partner
- `generateCouponCodes` → `PRICE_CONFIGURE` (configure) · staff
- `getPromotion` → `PRICE_VIEW` (read) · staff, guest, partner
- `getPromotionUsage` → `PRICE_VIEW` (read) · staff, partner
- `listCouponCodes` → `PRICE_VIEW` (read) · staff
- `pausePromotion` → `PRICE_CONFIGURE` (configure) · staff, partner
- `publishPromotion` → `PRICE_CONFIGURE` (configure) · staff, partner
- `unschedulePromotion` → `PRICE_CONFIGURE` (configure) · staff, partner
- `updatePromotion` → `PRICE_CONFIGURE` (configure) · staff, partner
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `simulatePromotion` → `PRICE_VIEW` (read) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `voidCouponCode` → `PRICE_CONFIGURE` (configure) · staff
- `setPromotionVariants` → `PRICE_CONFIGURE` (configure) · staff
- `assignCoupon` → `PRICE_CONFIGURE` (configure) · staff
- `listVoucherBatches` → `PRICE_VIEW` (read) · staff
- `createVoucherBatch` → `PRICE_CONFIGURE` (configure) · staff
- `voidVoucher` → `PRICE_CONFIGURE` (configure) · staff
- `listCommercialCampaigns` → `PRICE_VIEW` (read) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PRICE_VIEW`, which `listPromotions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

51 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.6.12 | The system should be able to manage all promotions in Backoffice application, where the positioning of the promotions fits in with the mechanics of the booking platform. In this way the Shop Cart is … | Admission and Access | CONTRACTED | `listPromotions` |
| 3.6.7 | The system should allow configuration of a hierarchy pattern for promotions to determine the order of application when multiple promotions are used. | Admission and Access | CONTRACTED | `analysePromotionConflicts` |
| 3.6.35 | System shall support configurable promotion hierarchy and conflict resolution rules when multiple promotions, discounts, loyalty rewards, vouchers, coupons, and membership benefits are applicable … | Admission and Access | CONTRACTED | `analysePromotionConflicts` |
| 4.2.1 | The system should be able to combine promotions and make sure only that the correct discounts are given | Bundles and Promotions | CONTRACTED | `analysePromotionConflicts` |
| 1.1.123 | Quantity restrictions | Ticketing Catalogue | CONTRACTED | `createPromotion` |
| 3.5.4 | It is possible to manage all kind of promotions, such as reentry promotions, buy one get one free etc. | Admission and Access | CONTRACTED | `createPromotion` |
| 3.6.5 | The system should be able to handle - if more than X tickets are purchased, then Y discount is applied to the entire transaction. | Admission and Access | CONTRACTED | `createPromotion` |
| 3.6.6 | The system should be able to support discounts for bulk purchase of tickets. The threshold for bulk quantity and applicable discount percentage need to be configurable. | Admission and Access | CONTRACTED | `createPromotion` |
| 3.6.27 | The system should allow limiting the usage of promotions and discounts to users with specific access levels. | Admission and Access | CONTRACTED | `createPromotion` |
| 3.6.28 | It is possible for Groups of 15 people or more have dedicated Group prices. | Admission and Access | CONTRACTED | `createPromotion` |
| 3.6.33 | Bulk-purchase discount configurator with tier pricing and auto-generated voucher/PDF packs | Admission and Access | CONTRACTED | `createPromotion` |
| 3.6.36 | System shall allow administrators to define maximum campaign budgets, redemption limits, discount caps, and automated campaign suspension once thresholds are reached. | Admission and Access | CONTRACTED | `createPromotion` |
| … 39 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price Book supports date-based pricing (regular this month, promotional next month). Promotion Builder supports rules such as "buy X get Y", "buy 2 get 1 free" and "buy 3, lowest-priced item discounted" (fully or partially). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog; 4.3 Pricing, Bundles & Promotions · DI-357)*
- Dynamic offers apply automatically without a code (buy-2-get-1-free, buy-3-get-2-at-50%-off, fixed amount off a minimum quantity); the discounted item is added to the cart automatically with its price adjusted (e.g. to zero). *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-174)*
- Coupons as one shared promo code (e.g. for social media) or a batch of unique single-use codes, with configurable reuse rules. *(agreed · MoM 7 Aug 2026, 17. Promotions & Dynamic Offers · DI-173)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-010` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 4.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 4.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 4.dc.html#pos-4e`, `Retail Board 5.dc.html#ret-5a`, `Retail Board 5.dc.html#ret-5b`, `Retail Board 5.dc.html#ret-5c`, `Retail Board 5.dc.html#ret-5e`
- Flow F77 *A promotion is built, bundled, published and measured*, step 4: Promotions & Coupons. → **Drawn by the client as RET-5A.** 15 operations on this step.
- Flow F90 *An audience is built, offered to, and the result is judged*, step 2: Promotions & Coupons. → **Drawn by the client as RET-5E.**

#### Acceptance for the design

- [ ] Every input above is drawn (165), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (70 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, , Analyse promotion conflicts, Create coupon campaign, Create promotion, End promotion, Evaluate promotions, Generate coupon codes, Pause promotion, Publish promotion, Unschedule promotion, Save promotion, Simulate promotion, Run report, Void coupon code, What publishing changes.
- [ ] Every transition is wired: `BO-007`, `BO-009`, `ANL-009`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-011` Packages & Bundles

**Sell several products as one line.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | Block A · ticket #18009 (APP-SETUP-BO-011) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 2 read); in the flows as marketer |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCatalogueBundles` reads the population and `getLatestBundle` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `version` (deepLink), `productId` (navigation), `bundleId` (navigation), `comboId` (navigation) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/venue-operations/packages-bundles` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 2 board screen(s): Combo & Meal Builder; Bundle, Kit & Gift Set Builder. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?venueId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?activeAt |
| Owner principal id | picker: choose an owner principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ownerPrincipalId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?ownerPrincipalId |
| Q | text field | optional | — | max length 100 | — | Sends `?q=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?q |
| Component kind | radio group | optional | Admission | Admission · Fnb menu item · Retail · Add on · Other | — | **Admission, F&B menu item, retail, add-on or other** (decided 29 September, MOB-4). A *meal combo with admission* is one admission component and one F&B menu-item component; the guest buys it from a … | `BundleComponent.componentKind` |
| Menu item | picker: choose a menu item | optional | — | Required when `componentKind` is `fnbMenuItem`, else ignored; a menu item that does not sell `variantId` is a `422` on `createBundle`. | shows names, sends the id | For an F&B menu-item component; the outlets that redeem it are `redeemAtOutletIds` (empty means any outlet with the item on a live menu). | `BundleComponent.menuItemId` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since | text field | — | — | `getLatestBundle` ?since |

**Form: Save group package definition** (modal, opened by *Save group package definition*; *Save group package definition* calls `setGroupPackageDefinition`, *Cancel* sends nothing)

**Collects what `setGroupPackageDefinition` sends before it is called.** Required: `kind`, `maxParticipants`, `durationMinutes`. Optional: `id`, `productId`, `hostCount`, `pricingBasis`, `freeLeaderRatio`, `paymentMode`, `includes`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | segmented control | required | — | School · Party | — | — | `setGroupPackageDefinition` body |
| Max participants `maxParticipants` | number field | required | — | min 1 | — | Pupils or children, e.g. 30 or 10. | `setGroupPackageDefinition` body |
| Duration minutes `durationMinutes` | number field (minutes) | required | — | min 15 | — | — | `setGroupPackageDefinition` body |
| Host count `hostCount` | number field | optional | 1 | min 0 | — | Party hosts included. | `setGroupPackageDefinition` body |
| Pricing basis `pricingBasis` | segmented control | optional | — | Per participant · Per package | — | — | `setGroupPackageDefinition` body |
| Free leader ratio `freeLeaderRatio` | number field | optional | 10 | — | — | Schools: one teacher or assistant enters free per this many pupils. | `setGroupPackageDefinition` body |
| Payment mode `paymentMode` | segmented control | optional | — | Invoice · Deposit · Full | — | Schools are invoiced; parties take a deposit (see `DepositPolicy`). | `setGroupPackageDefinition` body |
| Includes `includes` | list of values (chips) | optional | — | — | — | — | `setGroupPackageDefinition` body |

Carried, not typed: `productId`

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Publish bundle** (modal, opened by *Publish bundle*; *Publish bundle* calls `publishBundle`, *Cancel* sends nothing)

**Collects what `publishBundle` sends before it is called.** Required: `venueId`. Optional: `note`, `staleAfterHours`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `publishBundle` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `publishBundle` body |
| Stale after hours `staleAfterHours` | number field (hours) | optional | — | min 1 | — | How long a terminal may trade on this bundle before refusing. Defaults to the venue's configured bound. | `publishBundle` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue

**Form: Report bundle applied** (modal, opened by *Report bundle applied*; *Report bundle applied* calls `reportBundleApplied`, *Cancel* sends nothing)

**Collects what `reportBundleApplied` sends before it is called.** Required: `appliedAt`, `outcome`. Optional: `error`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Applied at `appliedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportBundleApplied` body |
| Outcome `outcome` | segmented control | required | — | Applied · Rolled back · Signature invalid | — | — | `reportBundleApplied` body |
| Error `error` | text field | optional | — | — | — | — | `reportBundleApplied` body |

**Form: Create bundle** (modal, opened by *Create bundle*; *Create bundle* calls `createBundle`, *Cancel* sends nothing)

**Collects what `createBundle` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`, `price`, `components`, `allocation`. Optional: `description`, `choiceGroups`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createBundle` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createBundle` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createBundle` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createBundle` body |
| Kind `kind` | radio group | required | — | Fixed · Dynamic · Mandatory · Optional · Promotional | — | — | `createBundle` body |
| Price `price` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createBundle` body |
| Components `components` | repeatable rows | required | — | at least 0 | — | — | `createBundle` body |
| Variant `components[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createBundle` body |
| Component kind `components[].componentKind` | radio group | optional | Admission | Admission · Fnb menu item · Retail · Add on · Other | — | What a bundle component entitles the guest to (decided 29 September, MOB-4). `admission` is a ticket; `fnbMenuItem` is a meal redeemed at an F&B outlet, issued as an entitlement … | `createBundle` body |
| Menu item `components[].menuItemId` | picker: choose a menu item | optional | — | Required when `componentKind` is `fnbMenuItem`, else ignored; a menu item that does not sell `variantId` is a `422` on `createBundle`. | shows names, sends the id | The F&B menu item a `fnbMenuItem` component entitles the guest to (decided 29 September, MOB-4): the meal of a *meal combo with admission*. | `createBundle` body |
| Redeem at outlets `components[].redeemAtOutletIds` | multi-picker: choose redeem at outlets | optional | — | at most 20 | — | Outlets that redeem an `fnbMenuItem` component; empty means any outlet of the component's venue that has the menu item on a live menu (MOB-4). | `createBundle` body |
| Quantity `components[].quantity` | number field | required | — | min 1 | — | — | `createBundle` body |
| Is optional `components[].isOptional` | toggle | optional | off | — | — | — | `createBundle` body |
| Substitute variants `components[].substituteVariantIds` | multi-picker: choose substitute variants | optional | — | — | — | For dynamic bundles — guest chooses among these. | `createBundle` body |
| Substitution triggers `components[].substitutionTriggers` | multi-select chips | optional | — | Sold out · Capacity exhausted · Product suspended · Venue closed · External API unavailable · Inventory below threshold | — | When a substitute from `substituteVariantIds` may replace this component (Dynamic Component Substitution Engine). | `createBundle` body |
| Substitution price effect `components[].substitutionPriceEffect` | segmented control | optional | Same price | Same price · Surcharge · Reduced price | — | What a substitution does to the bundle price. | `createBundle` body |
| Substitution approval `components[].substitutionApproval` | segmented control | optional | Customer | None · Customer · Operator | — | Who must accept a substitution before it stands. Customer by default, because a substitution the guest did not choose is a complaint at the gate. | `createBundle` body |
| Venue `components[].venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Where this component is redeemed. Differs from the selling venue for multi-venue passes, which is why the allocation split exists. | `createBundle` body |
| Choice groups `choiceGroups` | repeatable rows | optional | — | — | — | Dynamic bundles (3.5.10). A bundle may carry fixed components and choice groups at once — a family pass with fixed parking and two groups the guest chooses from. | `createBundle` body |
| Label `choiceGroups[].label` | text field | required | — | — | — | What the guest is asked. "Choose 3 attractions". | `createBundle` body |
| Choose `choiceGroups[].choose` | number field | required | — | min 1 | — | How many options the guest picks. | `createBundle` body |
| Allow duplicates `choiceGroups[].allowDuplicates` | toggle | optional | off | — | — | Whether the same option may be picked twice. False for attractions, sometimes true for F&B. | `createBundle` body |
| Options `choiceGroups[].options` | repeatable rows | required | — | at least 2 | — | The rows of `promotions.bundle_choice_option`, one per option, each keyed to its group. | `createBundle` body |
| Variant `choiceGroups[].options[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createBundle` body |
| Quantity `choiceGroups[].options[].quantity` | number field | optional | 1 | — | — | — | `createBundle` body |
| Is default `choiceGroups[].options[].isDefault` | toggle | optional | off | — | — | — | `createBundle` body |
| Unavailable behaviour `choiceGroups[].unavailableBehaviour` | segmented control | optional | Hide option | Hide option · Hide bundle; Where the group can no longer be satisfied at all, the bundle itself becomes unavailable — it is never sold with a component that cannot be delivered, because a substitution the guest did not choose … | — | An option that has sold out for the chosen date is not offered. Where the group can no longer be satisfied at all, the bundle itself becomes unavailable — it is never sold with a … | `createBundle` body |
| Allocation `allocation` | group | required | — | — | — | — | `createBundle` body |
| Method `allocation.method` | segmented control | required | Pro rata list price | Percentage · Fixed amount · Pro rata list price | — | Proportional to list price by default. The rounding remainder in the currency's minor unit goes to the first component (decided 28 September, audit R101). | `createBundle` body |
| Components `allocation.components` | repeatable rows | required | — | — | — | — | `createBundle` body |
| Variant `allocation.components[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createBundle` body |
| Percentage `allocation.components[].percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `createBundle` body |
| Fixed amount `allocation.components[].fixedAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createBundle` body |
| List price `allocation.components[].listPrice` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | For `proRataListPrice` — weights derived from list prices. The variant's current price when the bundle is created (decided 28 September, audit R101), then frozen with the … | `createBundle` body |
| Revenue account `allocation.components[].revenueAccountId` | picker: choose a revenue account | optional | — | — | shows names, sends the id | — | `createBundle` body |
| Legal entity `allocation.components[].legalEntityId` | picker: choose a legal entity | optional | — | — | shows names, sends the id | Set where the component is earned by a different legal entity. Cross-currency allocation is deferred pending the FX policy decision. | `createBundle` body |
| Venue `allocation.components[].venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createBundle` body |
| Valid from `validFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createBundle` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createBundle` body |
| Campaign `campaignId` | picker: choose a campaign | optional | — | — | shows names, sends the id | The commercial campaign (`promotions.campaign`) the bundle is sold under. | `createBundle` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | The bundle owner (Bundle Definition & Setup). | `createBundle` body |
| Category `category` | text field | optional | — | max length 100 | — | The bundle category the setup screen files it under. | `createBundle` body |
| Is standalone product `isStandaloneProduct` | toggle | optional | on | — | — | Whether the bundle appears as a product in its own right, or only as an offer on another product. | `createBundle` body |
| Is recommended at checkout `isRecommendedAtCheckout` | toggle | optional | off | — | — | Whether checkout recommends the bundle. | `createBundle` body |
| Required variants `requiredVariantIds` | multi-picker: choose required variants | optional | — | — | — | Products that must already be in the basket for the bundle to be sold (the setup screen's "requires another product"). | `createBundle` body |

Errors to draw in the form: 400 Allocation does not sum to 100 per cent, or fixed amounts do not sum to the bundle price.; 422 A `fnbMenuItem` component with no `menuItemId`, or whose menu item does not sell the component's `variantId` (MOB-4, 29 September).

**Form: Save package pricing definition** (modal, opened by *Save package pricing definition*; *Save package pricing definition* calls `setPackagePricingDefinition`, *Cancel* sends nothing)

**Collects what `setPackagePricingDefinition` sends before it is called.** Required: `id`, `scopePath`, `productId`, `recordKind`, `pricingModel`, `status`. Optional: `name`, `priceListId`, `addOnType`, `packagePrice`, `components`, `componentPriceVisibility`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Product `productId` | picker: choose a product | required | — | — | shows names, sends the id | — | `setPackagePricingDefinition` body |
| Record kind `recordKind` | segmented control | required | — | Package · Bundle · Add on | — | — | `setPackagePricingDefinition` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setPackagePricingDefinition` body |
| Price list `priceListId` | picker: choose a price list | optional | — | — | shows names, sends the id | — | `setPackagePricingDefinition` body |
| Pricing model `pricingModel` | radio group | required | — | Fixed package price · Sum of components · Discounted component sum · Component override | — | — | `setPackagePricingDefinition` body |
| Add on type `addOnType` | select | optional | — | Fast track · Parking · Meal · Photo · Equipment · Upgrade · Additional performance · Premium access · Other | — | — | `setPackagePricingDefinition` body |
| Package price `packagePrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPackagePricingDefinition` body |
| Components `components` | key and value settings | optional | — | `[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`. | — | `[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`. | `setPackagePricingDefinition` body |
| Component price visibility `componentPriceVisibility` | segmented control | optional | Package total only | Package total only · Individual components · Component and saving | — | — | `setPackagePricingDefinition` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setPackagePricingDefinition` body |

Errors to draw in the form: 409 `changeRequestRequired`.; 422 `priceRequired` or `circularComponent`.

#### Outputs: what the screen shows and produces

**Shown**

**Every bundle** (data table, from `listCatalogueBundles`)

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Content hash | text | — |
| Signature key | text | Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle. |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |
| Applied by workstations | 1,234 | — |

**Every commercial campaign** (data table, from `listCommercialCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Owner principal | the name it points at, never the id | The campaign (and budget) owner. |
| Legal entity | the name it points at, never the id | The business entity that funds and books the campaign. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Budgets | list or chips (count when long) | The rows of `promotions.campaign_budget`, one per budget line. |

**The selected bundle** (detail panel, from `listCatalogueBundles`)

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | — |
| Content hash | text | — |
| Signature key | text | Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle. |
| Stale after | 1 Oct 2026, 14:30 | — |
| Size bytes | 1,234 | — |
| Note | text | — |
| Applied by workstations | 1,234 | — |

**The group package definition** (detail panel, from `getGroupPackageDefinition`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Product | text | — |
| Kind | chip: School, Party | — |
| Max participants | 1,234 | Pupils or children, e.g. 30 or 10. |
| Duration minutes | 1,234 | — |
| Host count | 1,234 | Party hosts included. |
| Pricing basis | chip: Per participant, Per package | — |
| Free leader ratio | 1,234 | Schools: one teacher or assistant enters free per this many pupils. |
| Payment mode | chip: Invoice, Deposit, Full | Schools are invoiced; parties take a deposit (see `DepositPolicy`). |
| Includes | list or chips (count when long) | — |
| Scope path | text | The partition key (ADR-0005). Operations write it at `venue` scope. |

**The catalogue bundle** (detail panel, from `getLatestBundle`)

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Is delta | yes / no (icon or chip) | — |
| Base version | text | Present when `isDelta`. The version this delta applies to. |
| Signature | text | Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never … |
| Signature key | text | — |
| Content hash | text | — |
| Stale after | 1 Oct 2026, 14:30 | — |
| Payload | grouped details | Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Publish bundle (primary button) | `publishBundle` POST `/catalogue/bundles` | inline | BundleSummary | 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue | opens modal first |
| Report bundle applied (secondary button) | `reportBundleApplied` POST `/catalogue/bundles/{version}/applied` | inline | — | — | opens modal first |
| Create bundle (secondary button) | `createBundle` POST `/bundles` | CreateBundleRequest | Bundle | 400 Allocation does not sum to 100 per cent, or fixed amounts do not sum to the bundle price.; 422 A `fnbMenuItem` component with no `menuItemId`, or whose menu item does not sell the component's `variantId` (MOB-4, 29 … | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Save group package definition (secondary button) | `setGroupPackageDefinition` PUT `/products/{productId}/group-package` | GroupPackageDefinition | GroupPackageDefinition | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save package pricing definition (secondary button) | `setPackagePricingDefinition` PUT `/package-pricing` | PackagePricing | PackagePricing | 409 `changeRequestRequired`.; 422 `priceRequired` or `circularComponent`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listCatalogueBundles` (onLoad, List published bundles); `getLatestBundle` (onLoad, Pull the current bundle for this workstation's venue); `listCommercialCampaigns` (onLoad, List commercial campaigns)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*; carries `productId`
- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `productId`, `version`
- → `BO-009` Pricing Rules: *Pricing Rules*; carries `priceListId`
- → `ANL-009` AI Assistant & Action Center: *AI Assistant & Action Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The packages bundles list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the packages bundles untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No packages bundles yet. Offers Create bundle (`createBundle`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCatalogueBundles` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getGroupPackageDefinition` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Allocation does not sum to 100 per cent, or fixed amounts do not sum to the bundle price.; 400 The bundle's allocation is `fixedAmount` and the new price no longer equals the sum of the fixed amounts.; 400 Validation failed; 409 A publish is already in progress for this venue |

#### Permissions

- `listMenus` → `PRODUCT_VIEW` (read) · staff
- `getGroupPackageDefinition` → `PRODUCT_VIEW` (read) · staff, guest
- `setGroupPackageDefinition` → `PRODUCT_CONFIGURE` (configure) · staff
- `listCatalogueBundles` → `PRODUCT_VIEW` (read) · staff, guest
- `getLatestBundle` → `PRODUCT_VIEW` (read) · staff
- `publishBundle` → `PRODUCT_CONFIGURE` (configure) · staff
- `reportBundleApplied` → `PRODUCT_VIEW` (read) · staff
- `createBundle` → `PRODUCT_CONFIGURE` (configure) · staff
- `createCombo` → `PRODUCT_CONFIGURE` (configure) · staff
- `setComboSlots` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateBundle` → `PRODUCT_CONFIGURE` (configure) · staff
- `listCommercialCampaigns` → `PRICE_VIEW` (read) · staff
- `setPackagePricingDefinition` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getGroupPackageDefinition` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.4.7 | System shall allow publishing products to selected sales channels including Website, Mobile App, POS, API and Reseller channels. | Ticketing Catalogue | CONTRACTED | `publishBundle` |
| 1.1.17 | System shall support bundled ticket products combining multiple tickets, attractions, products, services, parking, F&B, retail items, memberships or vouchers into a single sellable product. | Ticketing Catalogue | CONTRACTED | `createBundle` |
| 1.1.43 | Configure ticket hierarchies and product bundles | Ticketing Catalogue | CONTRACTED | `createBundle` |
| 1.1.53 | F&B entitlement management | Ticketing Catalogue | CONTRACTED | `createBundle` |
| 1.1.54 | Merchandise entitlement management | Ticketing Catalogue | CONTRACTED | `createBundle` |
| 1.4.13 | System shall support grouping multiple products into a single package, bundle or offer. | Ticketing Catalogue | CONTRACTED | `createBundle` |
| 3.5.10 | System shall allow operators to configure dynamic bundles where guests can select attractions, experiences, F&B items, retail products, or services from predefined categories while maintaining bundle … | Admission and Access | CONTRACTED | `createBundle` |
| 3.6.3 | The system should be able to make combo bundles with all type of tickets being offered across every attraction/complex. and other Retail and F&B offers | Admission and Access | CONTRACTED | `createBundle` |
| 3.6.4 | The system should be able to make combo bundles with pre-configured combos or have the ability to choose as per the guests choice. | Admission and Access | CONTRACTED | `createBundle` |
| 3.6.26 | The system should be able to setup the offers to package tickets with F&B and/or Retail as well. | Admission and Access | CONTRACTED | `createBundle` |
| 7.4.26 | For each PLU, it is possible to manage Packages | F&B POS | CONTRACTED | `createBundle` |
| 7.4.48 | Support fixed, dynamic, mandatory, optional and promotional bundles. Allow bundled pricing, discount rules and cross-sell recommendations. | F&B POS | CONTRACTED | `createBundle` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multi-park / multi-attraction / multi-venue bundles are visually mapped, showing which venues, meal vouchers, VIP parking or upgrade options a bundle includes. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-469)*
- Packages bundle any combination of ticket-type components with package-level pricing (e.g. admission + F&B item + retail item, or admission + show); F&B or retail is not required. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-435)*
- Retail items (e.g. a t-shirt plus a cap) can be combined into a combo package with bundle-level pricing, presented both on-site and online with product images and descriptions. *(client request · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions · DI-358)*
- Bundle packages combine components within one attraction (ticket + meal + retail, or ticket + event ticket) at a discount — not a cross-attraction itinerary. *(agreed · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-220)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-011` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 5.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 2.dc.html#fnb-2g`, `Retail Board 5.dc.html#ret-5h`
- Flow F77 *A promotion is built, bundled, published and measured*, step 2: Packages & Bundles. → **Drawn by the client as RET-5H.** 2 operations on this step.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (75), with its required mark, default, format and its error state (400, 403, 404, 409, 412, 422).
- [ ] Every output is drawn (47 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-011?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish bundle, Report bundle applied, Create bundle, What publishing changes, Save group package definition, Save package pricing definition.
- [ ] Every transition is wired: `BO-007`, `BO-008`, `BO-009`, `ANL-009`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-012` Membership Products

**Define what a membership includes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | Block A · ticket #17864 (APP-SETUP-BO-012) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listProducts` reads the population and `getProduct` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `productId` (deepLink) · cold entry: **A shared product link after the product retired.** Shows what replaced it where a successor exists, and the catalogue where none does. |
| Route | `/venue-operations/membership-products` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listProducts`. | `listProducts` ?venueId |
| Kind | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Sends `?kind=` to `listProducts`. | `listProducts` ?kind |
| Is sellable | toggle | optional | — | — | — | Sends `?isSellable=` to `listProducts`. | `listProducts` ?isSellable |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Form: Create entitlement template** (modal, opened by *Create entitlement template*; *Create entitlement template* calls `createEntitlementTemplate`, *Cancel* sends nothing)

**Collects what `createEntitlementTemplate` sends before it is called.** Required: `id`, `code`, `name`, `validityKind`. Optional: `description`, `validFromOffsetDays`, `validForDays`, `daysOfWeek`, `expiryAnchor`, `expiryDate`, `carriesStoredValue`, `includedValue`, `validTimeWindows`, `blackoutDates`, `fastTrackTier`, `entriesAllowed` and 15 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Description `description` | text area | optional | — | — | — | Validity, re-entry and transfer rules in prose. "Can I leave and come back" is answered from here, and a name cannot answer it. | `createEntitlementTemplate` body |
| Code `code` | text field | required | — | max length 64 | — | — | `createEntitlementTemplate` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createEntitlementTemplate` body |
| Validity kind `validityKind` | select | required | — | Single use · Dated · Date range · Rolling · Unlimited · Count limited | — | — | `createEntitlementTemplate` body |
| Valid from offset days `validFromOffsetDays` | number field (days) | optional | — | — | — | — | `createEntitlementTemplate` body |
| Valid for days `validForDays` | number field (days) | optional | — | — | — | — | `createEntitlementTemplate` body |
| Days of week `daysOfWeek` | multi-select chips | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | 1.1.7 and 1.1.82. A camp ticket admits on Tuesdays and Thursdays for six weeks, and `validityKind` had six values with no day pattern among them. | `createEntitlementTemplate` body |
| Expiry anchor `expiryAnchor` | select | optional | — | Offset days · End of month · End of quarter · End of year · Fixed date · Season end; A pass bought on the 20th and expiring on the 31st cannot be expressed by an offset in days. | — | 1.1.90 to 1.1.92. A pass bought on the 20th and expiring on the 31st cannot be expressed by an offset in days. | `createEntitlementTemplate` body |
| Expiry date `expiryDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Where `expiryAnchor` is `fixedDate`. Every pass expires the same day regardless of purchase. | `createEntitlementTemplate` body |
| Expiry notice days `expiryNoticeDays` | number field (days) | optional | — | min 1; max 180 | — | How many days before `validTo` access raises `entitlement.expiringSoon` for an entitlement of this template still `issued` or `partiallyConsumed` (29 September, build pass, group … | `createEntitlementTemplate` body |
| Carries stored value `carriesStoredValue` | toggle | optional | off | — | — | BL-033. A ticket that is also a wallet — a resort pass with 200 dirhams of spend on it, deducted at a gate or a till. | `createEntitlementTemplate` body |
| Included value `includedValue` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createEntitlementTemplate` body |
| Valid time windows `validTimeWindows` | repeatable rows | optional | — | — | — | BL-036, 1.1.81 and 1.1.83. A time-window entitlement needed a performance to express — valid 09:00 to 13:00 on any day was a thing you built by creating performances. | `createEntitlementTemplate` body |
| From `validTimeWindows[].from` | text field | optional | — | — | — | — | `createEntitlementTemplate` body |
| To `validTimeWindows[].to` | text field | optional | — | — | — | — | `createEntitlementTemplate` body |
| Days of week `validTimeWindows[].daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createEntitlementTemplate` body |
| Blackout dates `blackoutDates` | list of values (chips) | optional | — | — | — | Calendar exceptions on the entitlement. An annual pass excluding public holidays is the normal case and had nowhere to live. | `createEntitlementTemplate` body |
| Fast track tier `fastTrackTier` | radio group | optional | — | None · Priority · Express · Unlimited | — | 19.2.20, BL-015. Fast track existed nowhere in the package — not an enum value, not a description, not a screen. | `createEntitlementTemplate` body |
| Entries allowed `entriesAllowed` | number field | optional | — | — | — | Null means unlimited. The Fast Pass consumption counter lives here. | `createEntitlementTemplate` body |
| Transport restriction `transportRestriction` | group | optional | — | — | — | The journey a transport pass is good for (decided 29 September, rev 3 REV3-21). Set on the template `transport.createTransportPassType` creates, from the station pair the guest … | `createEntitlementTemplate` body |
| From station `transportRestriction.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | A `transport.Station`. | `createEntitlementTemplate` body |
| To station `transportRestriction.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | — | `createEntitlementTemplate` body |
| Both directions `transportRestriction.bothDirections` | toggle | optional | on | — | — | Valid from either station to the other, as the prototype sells it. | `createEntitlementTemplate` body |
| Routes `transportRestriction.routeIds` | multi-picker: choose routes | optional | — | — | — | The routes it may be used on. Empty means any active route serving both stations. | `createEntitlementTemplate` body |
| Reentry allowed `reentryAllowed` | toggle | optional | off | — | — | — | `createEntitlementTemplate` body |
| Purchase eligibility `purchaseEligibility` | group | optional | — | — | — | 1.1.38, 1.1.121, 1.1.125, 1.1.126. `admissionRulesId` governs where an entitlement admits, not who may buy it, and `promotions.evaluatePromotions` gates a discount rather than a … | `createEntitlementTemplate` body |
| Min age years `purchaseEligibility.minAgeYears` | number field | optional | — | — | — | — | `createEntitlementTemplate` body |
| Max age years `purchaseEligibility.maxAgeYears` | number field | optional | — | — | — | — | `createEntitlementTemplate` body |
| Min height cm `purchaseEligibility.minHeightCm` | number field | optional | — | — | — | Height gates a ride and can gate a sale. A ticket sold to somebody who cannot ride it is a refund at the gate. | `createEntitlementTemplate` body |
| Residency required `purchaseEligibility.residencyRequired` | toggle | optional | off | — | — | — | `createEntitlementTemplate` body |
| Nationalities `purchaseEligibility.nationalities` | list of values (chips) | optional | — | — | — | — | `createEntitlementTemplate` body |
| Min loyalty tier `purchaseEligibility.minLoyaltyTier` | text field | optional | — | — | — | — | `createEntitlementTemplate` body |
| Requires verification `purchaseEligibility.requiresVerification` | toggle | optional | off | — | — | Whether the claim is checked or taken on trust. A resident rate sold unverified and refused at the gate is worse than one that could not be bought. | `createEntitlementTemplate` body |
| Person type `personType` | select | optional | — | Adult · Child · Infant · Senior · Student · Resident · Staff | — | 2.11.7. Adult, child and senior existed only as `ProductVariant.axisValues` — a variant axis rather than an attribute of the holder. | `createEntitlementTemplate` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | optional | — | — | shows names, sends the id | — | `createEntitlementTemplate` body |
| Is transferable `isTransferable` | toggle | optional | on | — | — | — | `createEntitlementTemplate` body |
| Can share media `canShareMedia` | toggle | optional | on | — | — | Whether this entitlement may be appended to media a guest already holds (CF-58). | `createEntitlementTemplate` body |
| Can claim shop and drop `canClaimShopAndDrop` | toggle | optional | off | — | — | Whether this entitlement may be scanned to claim goods left under 4.4.7. False for a single-entry ticket that is surrendered at the gate — a claim token the guest no longer holds … | `createEntitlementTemplate` body |
| Is name bound `isNameBound` | toggle | optional | off | — | — | True requires a holder name at sale. Most entitlements carry none — identity and entitlement are separate concerns. | `createEntitlementTemplate` body |
| Auto renew default `autoRenewDefault` | toggle | optional | off | — | — | Taken from their `membership_plan`, 20 September — the "take those" half of the TAKE BODY verdict. | `createEntitlementTemplate` body |
| Renewal term days `renewalTermDays` | number field (days) | optional | — | — | — | What a renewal extends the membership by. `orders.membership_renewal` records `previousExpiryAt` and `newExpiryAt` and the number between them lived nowhere. | `createEntitlementTemplate` body |
| Renewal grace days `renewalGraceDays` | number field (days) | optional | 0 | — | — | How long after expiry a membership can still be renewed rather than rejoined. `membership_renewal.failureReason` implies a window and there was none, so a failed card on the … | `createEntitlementTemplate` body |
| Renewal variant `renewalVariantId` | picker: choose a renewal variant | optional | — | — | shows names, sends the id | What a renewal sells, which is usually not what joining sold. A first-year price and a renewal price are different products, and pointing both at one variant makes a loyalty … | `createEntitlementTemplate` body |
| Crosses cells `crossesCells` | toggle | optional | off | — | — | True propagates a redemption right to other cells on issue (ADR-0010). | `createEntitlementTemplate` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createEntitlementTemplate` body |

**Form: Create product** (modal, opened by *Create product*; *Create product* calls `createProduct`, *Cancel* sends nothing)

**Collects what `createProduct` sends before it is called.** Required: `code`, `name`, `kind`, `venueId`. Optional: `description`, `channels`, `entitlementTemplateId`, `dataMaskValues`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; A code already used by any product in the tenant, at any venue, is refused with `409 duplicate-code`. | — | Unique per tenant (decided 28 September, audit R108). A code already used by any product in the tenant, at any venue, is refused with `409 duplicate-code`. | `createProduct` body |
| Family key `familyKey` | text field | optional | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; At most one product per venue in a family, else `409 duplicate-code`. | — | The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. | `createProduct` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createProduct` body |
| Description `description` | text area | optional | — | — | — | — | `createProduct` body |
| Kind `kind` | select | required | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: valid on any date within an eligible … | `createProduct` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createProduct` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createProduct` body |
| Entitlement template `entitlementTemplateId` | picker: choose an entitlement template | optional | — | — | shows names, sends the id | — | `createProduct` body |
| Data mask values `dataMaskValues` | key and value settings | optional | — | — | — | — | `createProduct` body |
| Guest listing `guestListing` | segmented control | optional | Bookable | Bookable · Info only · Hidden; `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. | — | How a product appears to a guest (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. | `createProduct` body |
| Not bookable label `notBookableLabel` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createProduct` body |
| Sales contact `salesContact` | group | optional | — | — | — | See `Product.salesContact` (W3, 29 September). | `createProduct` body |
| Phone `salesContact.phone` | phone field | optional | — | max length 32 | +971 5X XXX XXXX (E.164) | — | `createProduct` body |
| Email `salesContact.email` | email field | optional | — | max length 254 | name@example.ae | — | `createProduct` body |
| Note `salesContact.note` | text, one per language | optional | — | At most 200 characters per language. | English and Arabic (Arabic right to left) | A line shown under the contact, e.g. *Group courses are booked by phone*. | `createProduct` body |
| Booking flow `bookingFlowId` | picker: choose a booking flow | optional | — | — | shows names, sends the id | See `Product.bookingFlowId` (W8, W12, 29 September). | `createProduct` body |
| Display tags `displayTags` | repeatable rows | optional | — | at most 6 | — | — | `createProduct` body |
| Kind `displayTags[].kind` | radio group | required | — | Clock · Height · Free · Calendar · ID | — | `clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring. | `createProduct` body |
| Label `displayTags[].label` | text, one per language | required | — | Each language value at most 40 characters. | English and Arabic (Arabic right to left) | What the guest reads, e.g. *2 Hours*. | `createProduct` body |
| Media `media` | repeatable rows | optional | — | at most 20 | — | — | `createProduct` body |
| Asset `media[].assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | A `MediaAsset` of `assets.yaml`, in status `ready`. | `createProduct` body |
| Kind `media[].kind` | segmented control | required | — | Image · Video | — | — | `createProduct` body |
| Is primary `media[].isPrimary` | toggle | required | off | — | — | The item *Read more* opens on and a listing shows. Exactly one per product. | `createProduct` body |
| Display order `media[].displayOrder` | number field | optional | 100 | — | — | — | `createProduct` body |
| Alt text `media[].altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createProduct` body |
| Consent questions `consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates | — | — | `createProduct` body |
| Requires time window `requiresTimeWindow` | toggle | optional | — | — | — | — | `createProduct` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A `media` asset that is not `ready` or whose kind does not match, a `consentQuestionIds` entry that names no active consent question of the tenant, or …

**Form: Save alternative codes** (modal, opened by *Save alternative codes*; *Save alternative codes* calls `setAlternativeCodes`, *Cancel* sends nothing)

**Collects what `setAlternativeCodes` sends before it is called.** Required: `codes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Codes `codes` | repeatable rows | required | — | — | — | — | `setAlternativeCodes` body |
| Code `codes[].code` | text field | required | — | max length 128 | — | — | `setAlternativeCodes` body |
| Partner `codes[].partnerId` | picker: choose a partner | required | — | — | shows names, sends the id | — | `setAlternativeCodes` body |
| Partner name `codes[].partnerName` | text field | optional | — | — | — | — | `setAlternativeCodes` body |
| Variant `codes[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `setAlternativeCodes` body |
| Note `codes[].note` | text area | optional | — | max length 200 | — | — | `setAlternativeCodes` body |

Errors to draw in the form: 400 A `variantId` is not a variant of this product, or the body sends one code twice for the same partner.; 409 Code already mapped to a different product for that partner

**Form: Save product attributes** (modal, opened by *Save product attributes*; *Save product attributes* calls `setProductAttributes`, *Cancel* sends nothing)

**Collects what `setProductAttributes` sends before it is called.** Required: `axes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Axes `axes` | repeatable rows | required | — | — | — | — | `setProductAttributes` body |
| Code `axes[].code` | text field | required | — | max length 64 | — | — | `setProductAttributes` body |
| Name `axes[].name` | text field | required | — | max length 200 | — | — | `setProductAttributes` body |
| Values `axes[].values` | repeatable rows | required | — | at least 1 | — | — | `setProductAttributes` body |
| Code `axes[].values[].code` | text field | required | — | max length 64 | — | — | `setProductAttributes` body |
| Label `axes[].values[].label` | text field | required | — | max length 200 | — | — | `setProductAttributes` body |
| Price delta `axes[].values[].priceDelta` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setProductAttributes` body |
| Duration minutes `axes[].values[].durationMinutes` | number field (minutes) | optional | — | min 15; max 1440; One axis per product at most may carry it; a second is a `400`. | — | How long a variant carrying this value books its space for, on a `length` axis of a product with `requiresTimeWindow` (decided 29 September, rev 3 REV3-13). | `setProductAttributes` body |

Errors to draw in the form: 400 Two axes share a code, or one axis repeats a value code.; 403 Authenticated but not permitted at the requested scope; 409 Regeneration would exceed the variant ceiling for this product: `VenueSettings.catalogue.maxVariantsPerProduct`, a venue setting with a tenant default (decided …

**Form: Transition product lifecycle** (modal, opened by *Transition product lifecycle*; *Transition product lifecycle* calls `transitionProductLifecycle`, *Cancel* sends nothing)

**Collects what `transitionProductLifecycle` sends before it is called.** Required: `transition`, `reason`. Optional: `effectiveAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Transition `transition` | select | required | — | Submit for review · Approve · Reject · Publish · Withdraw · Archive · Restore | — | — | `transitionProductLifecycle` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `transitionProductLifecycle` body |
| Effective at `effectiveAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `transitionProductLifecycle` body |

Errors to draw in the form: 403 Approval attempted by the principal who submitted it (`approver-is-submitter`). Segregation applies here as it does to journals.; 409 Transition not valid from the current state, or archiving attempted while unexpired entitlements exist.

**Form: Save product** (modal, opened by *Save product*; *Save product* calls `updateProduct`, *Cancel* sends nothing)

**Collects what `updateProduct` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `channels`, `dataMaskValues`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Family key `familyKey` | text field | optional | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; At most one product per venue in a family, else `409 duplicate-code`. | — | The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. | `updateProduct` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `updateProduct` body |
| Description `description` | text area | optional | — | — | — | — | `updateProduct` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `updateProduct` body |
| Data mask values `dataMaskValues` | key and value settings | optional | — | — | — | — | `updateProduct` body |
| Guest listing `guestListing` | segmented control | optional | Bookable | Bookable · Info only · Hidden; `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. | — | How a product appears to a guest (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. | `updateProduct` body |
| Not bookable label `notBookableLabel` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateProduct` body |
| Sales contact `salesContact` | group | optional | — | — | — | See `Product.salesContact` (W3, 29 September). | `updateProduct` body |
| Phone `salesContact.phone` | phone field | optional | — | max length 32 | +971 5X XXX XXXX (E.164) | — | `updateProduct` body |
| Email `salesContact.email` | email field | optional | — | max length 254 | name@example.ae | — | `updateProduct` body |
| Note `salesContact.note` | text, one per language | optional | — | At most 200 characters per language. | English and Arabic (Arabic right to left) | A line shown under the contact, e.g. *Group courses are booked by phone*. | `updateProduct` body |
| Booking flow `bookingFlowId` | picker: choose a booking flow | optional | — | — | shows names, sends the id | See `Product.bookingFlowId` (W8, W12, 29 September). | `updateProduct` body |
| Display tags `displayTags` | repeatable rows | optional | — | at most 6 | — | — | `updateProduct` body |
| Kind `displayTags[].kind` | radio group | required | — | Clock · Height · Free · Calendar · ID | — | `clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring. | `updateProduct` body |
| Label `displayTags[].label` | text, one per language | required | — | Each language value at most 40 characters. | English and Arabic (Arabic right to left) | What the guest reads, e.g. *2 Hours*. | `updateProduct` body |
| Media `media` | repeatable rows | optional | — | at most 20 | — | — | `updateProduct` body |
| Asset `media[].assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | A `MediaAsset` of `assets.yaml`, in status `ready`. | `updateProduct` body |
| Kind `media[].kind` | segmented control | required | — | Image · Video | — | — | `updateProduct` body |
| Is primary `media[].isPrimary` | toggle | required | off | — | — | The item *Read more* opens on and a listing shows. Exactly one per product. | `updateProduct` body |
| Display order `media[].displayOrder` | number field | optional | 100 | — | — | — | `updateProduct` body |
| Alt text `media[].altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateProduct` body |
| Consent questions `consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates | — | — | `updateProduct` body |
| Requires time window `requiresTimeWindow` | toggle | optional | — | — | — | — | `updateProduct` body |

Errors to draw in the form: 400 `media` with no `isPrimary` item or more than one, or one asset twice.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A `media` asset that is not `ready` or whose kind does not match, a `consentQuestionIds` entry that names no active consent question of the tenant, or …

#### Outputs: what the screen shows and produces

**Shown**

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**Every entitlement template** (data table, from `listEntitlementTemplates`)

| Shows | Format | Notes |
|---|---|---|
| Description | text | Validity, re-entry and transfer rules in prose. "Can I leave and come back" is answered from here, and a name cannot answer it. |
| ID | the name it points at, never the id | Assigned by the server on create; `createEntitlementTemplate` does not take it. |
| Code | text | — |
| Name | text | — |
| Validity kind | chip: Single use, Dated, Date range, Rolling, Unlimited, Count limited | — |
| Valid from offset days | 1,234 | — |
| Valid for days | 1,234 | — |
| Days of week | list or chips (count when long) | 1.1.7 and 1.1.82. A camp ticket admits on Tuesdays and Thursdays for six weeks, and `validityKind` had six values with no day pattern among … |
| Expiry anchor | chip: Offset days, End of month, End of quarter, End of year, Fixed date, Season end | 1.1.90 to 1.1.92. A pass bought on the 20th and expiring on the 31st cannot be expressed by an offset in days. |
| Expiry date | 1 Oct 2026 | Where `expiryAnchor` is `fixedDate`. Every pass expires the same day regardless of purchase. |
| Carries stored value | yes / no (icon or chip) | BL-033. A ticket that is also a wallet — a resort pass with 200 dirhams of spend on it, deducted at a gate or a till. |
| Included value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Every alternative code** (data table, from `listAlternativeCodes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Partner | the name it points at, never the id | — |
| Partner name | text | — |
| Variant | the name it points at, never the id | — |
| Note | text | — |

**Every product variant** (data table, from `listProductVariants`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| SKU | text | — |
| Axis values | grouped details | — |
| Name | text | Taken from their variant tables, 20 September. `axisValues` gives `{size: L}` and no string a guest can read. |
| Barcode | text | Taken from their variant tables, 20 September. `catalogue.alternative_code` is a partner's own code for a variant and requires `partnerId` … |
| Is default | yes / no (icon or chip) | Taken from their variant tables. Which variant a product page opens on. |
| Is active | yes / no (icon or chip) | False when retired. Retired variants are never deleted — orders reference them. |

**The selected product** (detail panel, from `getProduct`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create entitlement template (primary button) | `createEntitlementTemplate` POST `/entitlement-templates` | EntitlementTemplate | EntitlementTemplate | — | opens modal first |
| Create product (secondary button) | `createProduct` POST `/products` | CreateProductRequest | Product | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names … | opens modal first |
| Resolve product by code (secondary button) | `resolveProductByCode` GET `/products/resolve` | — | ProductVariant | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save alternative codes (secondary button) | `setAlternativeCodes` PUT `/products/{productId}/alternative-codes` | inline | AlternativeCode[] | 400 A `variantId` is not a variant of this product, or the body sends one code twice for the same partner.; 409 Code already mapped to a different product for that partner | opens modal first |
| Save product attributes (secondary button) | `setProductAttributes` PUT `/products/{productId}/attributes` | inline | inline | 400 Two axes share a code, or one axis repeats a value code.; 403 Authenticated but not permitted at the requested scope; 409 Regeneration would exceed the variant ceiling for this product … | opens modal first |
| Transition product lifecycle (secondary button) | `transitionProductLifecycle` POST `/products/{productId}/lifecycle` | inline | Product | 403 Approval attempted by the principal who submitted it (`approver-is-submitter`). Segregation applies here as it does to journals.; 409 Transition not valid from the current state, or archiving attempted while … | opens modal first |
| Save product (secondary button) | `updateProduct` PATCH `/products/{productId}` | UpdateProductRequest | Product | 400 `media` with no `isPrimary` item or more than one, or one asset twice.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a … | opens modal first |

**Data it reads**: `listProducts` (onLoad, List products); `listEntitlementTemplates` (onLoad, List entitlement templates)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*; carries `productId`
- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `productId`, `variantId`
- → `BO-009` Pricing Rules: *Pricing Rules*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership products list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership products untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership products yet. Offers Create entitlement template (`createEntitlementTemplate`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind, isSellable and the membership products are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A `variantId` is not a variant of this product, or the body sends one code twice for the same partner.; 400 Two axes share a code, or one axis repeats a value code.; 400 Validation failed |

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listEntitlementTemplates` → `PRODUCT_VIEW` (read) · staff
- `createEntitlementTemplate` → `PRODUCT_CONFIGURE` (configure) · staff
- `createProduct` → `PRODUCT_CONFIGURE` (configure) · staff
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listAlternativeCodes` → `PRODUCT_VIEW` (read) · staff, partner
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `resolveProductByCode` → `PRODUCT_VIEW` (read) · staff, partner
- `setAlternativeCodes` → `PRODUCT_CONFIGURE` (configure) · staff
- `setProductAttributes` → `PRODUCT_CONFIGURE` (configure) · staff
- `transitionProductLifecycle` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateProduct` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

112 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.32 | Membership & Annual Pass Sales | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 2.14.11 | Support validity periods, renewals and expiry rules. | Ticketing Sales | CONTRACTED | `listEntitlementTemplates` |
| 5.3.15 | Maintain membership type, tier, status, activation date, expiration date, benefits, renewal history, suspension history, and usage history. | F&B & Guest Management | CONTRACTED | `listEntitlementTemplates` |
| 6.1.37 | The system should be able to provide aging report for ticketing & reward age. | Retail POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.21 | For each PLU, it is possible to manage a validity date range | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.23 | For each PLU, it is possible to manage Events having a scheduled usage, based on slot date and time | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.24 | For each PLU, it is possible to have Capacity management rules (valid until there is no available place) | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 7.4.29 | For each PLU, it is possible to Allow re-entry or not | F&B POS | CONTRACTED | `listEntitlementTemplates` |
| 1.1.5 | The system should be able to sell multiple day tickets for attractions. The number of days should be configurable. This type of ticket should require a start date to be specified before first entry. | Ticketing Catalogue | CONTRACTED | `createEntitlementTemplate` |
| … 100 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-012` · status **notStarted** · provenance generated
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (115), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (53 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-012?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create entitlement template, Create product, Resolve product by code, Save alternative codes, Save product attributes, Transition product lifecycle, Save product.
- [ ] Every transition is wired: `BO-007`, `BO-008`, `BO-009`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-013` Channel & Distribution

**Decide where each product can be sold.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 1 read); in the flows as marketer |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `channelCapacityId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/channel-distribution` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 2 board screen(s): Catalog Builder & Store Assortment; Ticketing, Event & Experience Commerce Integration. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real. **Improved 20 August against the client design board**, answering 1 board screen(s): Sales Channel Configuration. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Retail board operations wired 24 August.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Performance id | picker: choose a performance (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?performanceId=` to `listChannelCapacities`. | `listChannelCapacities` ?performanceId |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | `listProducts` ?kind |
| Is sellable | toggle | — | — | `listProducts` ?isSellable |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Form: Save channel allocations** (modal, opened by *Save channel allocations*; *Save channel allocations* calls `setChannelAllocations`, *Cancel* sends nothing)

**Collects what `setChannelAllocations` sends before it is called.** Required: `allocations`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Allocations `allocations` | repeatable rows | required | — | at least 1 | — | — | `setChannelAllocations` body |
| Channel `allocations[].channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `setChannelAllocations` body |
| Allocated units `allocations[].allocatedUnits` | number field | required | — | min 0 | — | — | `setChannelAllocations` body |
| Release at `allocations[].releaseAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it. | `setChannelAllocations` body |
| Sales channel `allocations[].salesChannelId` | picker: choose a sales channel | optional | — | — | shows names, sends the id | The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3). | `setChannelAllocations` body |
| Allocation type `allocations[].allocationType` | radio group | optional | Dedicated | Shared pool · Dedicated · Percentage · Dynamic | — | How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row. | `setChannelAllocations` body |
| Minimum units `allocations[].minimumUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Maximum units `allocations[].maximumUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Replenishment rule `allocations[].replenishmentRule` | key and value settings | optional | — | — | — | `{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`. | `setChannelAllocations` body |
| Waitlist behavior `allocations[].waitlistBehavior` | segmented control | optional | None | None · Join waitlist · Notify on release | — | — | `setChannelAllocations` body |
| Release threshold units `allocations[].releaseThresholdUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Release hours before event `allocations[].releaseHoursBeforeEvent` | number field | optional | — | min 0 | — | Alternative to `releaseAt`, relative to the performance start. | `setChannelAllocations` body |
| Contractual units `allocations[].contractualUnits` | number field | optional | — | min 0 | — | Units a partner agreement guarantees; rebalancing never goes below it. | `setChannelAllocations` body |
| Minimum guaranteed units `allocations[].minimumGuaranteedUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Is frozen `allocations[].isFrozen` | toggle | optional | off | — | — | Excluded from rebalancing. | `setChannelAllocations` body |

Errors to draw in the form: 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101)

**Form: Create channel capacity** (modal, opened by *Create channel capacity*; *Create channel capacity* calls `createChannelCapacity`, *Cancel* sends nothing)

**Collects what `createChannelCapacity` sends before it is called.** Required: `performanceId`, `name`, `capacity`. Optional: `seatCategoryId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Performance `performanceId` | picker: choose a performance | required | — | — | shows names, sends the id | — | `createChannelCapacity` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createChannelCapacity` body |
| Seat category `seatCategoryId` | picker: choose a seat category | optional | — | — | shows names, sends the id | — | `createChannelCapacity` body |
| Capacity `capacity` | number field | required | — | min 0 | — | — | `createChannelCapacity` body |

**Form: Release channel allocation** (modal, opened by *Release channel allocation*; *Release channel allocation* calls `relinquishChannelAllocation`, *Cancel* sends nothing)

**Collects what `relinquishChannelAllocation` sends before it is called.** Required: `channels`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channels `channels` | multi-select chips | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre; at least 1 | — | — | `relinquishChannelAllocation` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `relinquishChannelAllocation` body |

**Form: Save channel capacity** (modal, opened by *Save channel capacity*; *Save channel capacity* calls `updateChannelCapacity`, *Cancel* sends nothing)

**Collects what `updateChannelCapacity` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacity`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateChannelCapacity` body |
| Capacity `capacity` | number field | optional | — | min 0 | — | — | `updateChannelCapacity` body |

Errors to draw in the form: 409 Capacity reduced below units already sold plus units under an unexpired lease (audit R101)

**Form: Publish bundle** (modal, opened by *Publish bundle*; *Publish bundle* calls `publishBundle`, *Cancel* sends nothing)

**Collects what `publishBundle` sends before it is called.** Required: `venueId`. Optional: `note`, `staleAfterHours`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `publishBundle` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `publishBundle` body |
| Stale after hours `staleAfterHours` | number field (hours) | optional | — | min 1 | — | How long a terminal may trade on this bundle before refusing. Defaults to the venue's configured bound. | `publishBundle` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue

**Form: Save channel listing** (modal, opened by *Save channel listing*; *Save channel listing* calls `setChannelListing`, *Cancel* sends nothing)

**Collects what `setChannelListing` sends before it is called.** Required: `id`, `channelName`, `productId`, `status`. Optional: `externalProductRef`, `allocationUnits`, `priceListId`, `adapter`, `adapterCredentialRef`, `pushIntervalMinutes`, `guestDataScope`, `lastPushedAt`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

`setChannelListing` is not in any contract: draw the form greyed and list it in FINDINGS.md.

#### Outputs: what the screen shows and produces

**Shown**

**Every channel capacity** (data table, from `listChannelCapacities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Name | text | — |
| Seat category | the name it points at, never the id | — |
| Oversell allowance | 1,234 | BL-046, 1.3.13. The guard existed in one direction — an envelope could be raised freely and refused reduction below what had sold. |
| Oversell basis | chip: Fixed count, Historic no show rate, Percentage | — |
| Capacity | 1,234 | — |
| Sold | 1,234 | Units sold. Maintained on write (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by … |
| Leased | 1,234 | Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023). |
| Remaining | 1,234 | What can still be held. Decremented at the hold with a guarded statement (`remaining >= n`) under the row lock, never at the sale, so two … |
| Has channel allocations | yes / no (icon or chip) | True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity. |
| Is seated | yes / no (icon or chip) | Seated envelopes cannot be leased and are blocked offline. A seat map is not a count. |

**Every channel listing** (data table, from `listChannelListings`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `ChannelListing.id` |
| Channel name | text | not in the schema: `ChannelListing.channelName` |
| Product ID | text | not in the schema: `ChannelListing.productId` |
| External product ref | text | not in the schema: `ChannelListing.externalProductRef` |
| Status | text | not in the schema: `ChannelListing.status` |
| Allocation units | text | not in the schema: `ChannelListing.allocationUnits` |
| Price list ID | text | not in the schema: `ChannelListing.priceListId` |
| Adapter | text | not in the schema: `ChannelListing.adapter` |
| Adapter credential ref | text | not in the schema: `ChannelListing.adapterCredentialRef` |
| Push interval minutes | text | not in the schema: `ChannelListing.pushIntervalMinutes` |
| Guest data scope | text | not in the schema: `ChannelListing.guestDataScope` |
| Last pushed at | text | not in the schema: `ChannelListing.lastPushedAt` |

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**The selected channel capacity** (detail panel, from `listChannelCapacities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Name | text | — |
| Seat category | the name it points at, never the id | — |
| Oversell allowance | 1,234 | BL-046, 1.3.13. The guard existed in one direction — an envelope could be raised freely and refused reduction below what had sold. |
| Oversell basis | chip: Fixed count, Historic no show rate, Percentage | — |
| Capacity | 1,234 | — |
| Sold | 1,234 | Units sold. Maintained on write (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by … |
| Leased | 1,234 | Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023). |
| Remaining | 1,234 | What can still be held. Decremented at the hold with a guarded statement (`remaining >= n`) under the row lock, never at the sale, so two … |
| Has channel allocations | yes / no (icon or chip) | True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity. |
| Is seated | yes / no (icon or chip) | Seated envelopes cannot be leased and are blocked offline. A seat map is not a count. |

**The channel allocation set** (detail panel, from `getChannelAllocations`)

| Shows | Format | Notes |
|---|---|---|
| Channel capacity | the name it points at, never the id | — |
| Capacity | 1,234 | — |
| Allocations | list or chips (count when long) | — |
| General pool units | 1,234 | Unallocated remainder. Any channel may draw from it once its own allocation is exhausted. |
| Total sold | 1,234 | — |
| Total remaining | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Save channel allocations (primary button) | `setChannelAllocations` PUT `/channel-capacities/{channelCapacityId}/channel-allocations` | inline | ChannelAllocationSet | 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101) | opens modal first |
| Create channel capacity (secondary button) | `createChannelCapacity` POST `/channel-capacities` | CreateEnvelopeRequest | ChannelCapacity | — | opens modal first |
| Release channel allocation (secondary button) | `relinquishChannelAllocation` POST `/channel-capacities/{channelCapacityId}/channel-allocations/release` | inline | ChannelAllocationSet | — | opens modal first |
| Save channel capacity (secondary button) | `updateChannelCapacity` PATCH `/channel-capacities/{channelCapacityId}` | inline | ChannelCapacity | 409 Capacity reduced below units already sold plus units under an unexpired lease (audit R101) | opens modal first |
| Publish bundle (secondary button) | `publishBundle` POST `/catalogue/bundles` | inline | BundleSummary | 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue | opens modal first |
| Save channel listing (secondary button) | `setChannelListing` (not in any contract) | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listChannelCapacities` (onLoad, List capacity envelopes); `listChannelListings` (onLoad, What is listed on which OTA); `listProducts` (onLoad, List products)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*; carries `productId`
- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `productId`, `version`
- → `BO-009` Pricing Rules: *Pricing Rules*
- → `BO-011` Packages & Bundles: *Packages & Bundles*; carries `productId`, `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel distribution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel distribution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel distribution yet. Offers Create channel capacity (`createChannelCapacity`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on performanceId and the channel distribution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getChannelAllocations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 A publish is already in progress for this venue; 409 An allocation is below what that channel has already sold plus its leased units (audit R101) |

#### Permissions

- `getChannelAllocations` → `PRODUCT_VIEW` (read) · staff, partner
- `setChannelAllocations` → `CAPACITY_CONFIGURE` (configure) · staff
- `createChannelCapacity` → `CAPACITY_CONFIGURE` (configure) · staff
- `listChannelCapacities` → `PRODUCT_VIEW` (read) · staff, partner
- `relinquishChannelAllocation` → `CAPACITY_CONFIGURE` (configure) · staff, partner
- `updateChannelCapacity` → `CAPACITY_CONFIGURE` (configure) · staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `publishBundle` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getChannelAllocations` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

34 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.10 | The system should allow the capacity for all type of ticket to be configurable. Capacity of a ticket can be configurable at multiple levels: 1) Sales Capacity: Allow only a fixed number of tickets to … | Ticketing Catalogue | CONTRACTED | `setChannelAllocations` |
| 1.1.127 | Maximum sellable quantity controls | Ticketing Catalogue | CONTRACTED | `setChannelAllocations` |
| 2.1.1 | The system should have the ability to create as many sales channels as necessary by the system admin. Sales Channels creation should involve capture of all required data such as account assignment … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.1.2 | The system should support the configuration of products, prices, quotas, sales limits and sales schedule for each sales channels. Some sales channels can be configured to be accessible to only … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.1.3 | The system should store and manage all rules for product compatibility, eligibility and pricing that will be applicable to for each sales channel. These rules will be part of the system and not … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.5 | For BtoB online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.11 | - Only BtoB PLUs | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.15 | - Quotas can be applied for one Customer or a category of Customers | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 7.3.3 | Channel-based & slot-based inventory controls to stop OTAs or B2B partners overselling peak capacity | F&B POS | CONTRACTED | `setChannelAllocations` |
| 1.1.3 | The system should be able to sell time-slot based tickets for attractions. The system should support: - Creation of timeslots for a whole day or for a period - Configuration of capacity for each … | Ticketing Catalogue | CONTRACTED | `createChannelCapacity` |
| 7.3.2 | Allow configure inventory and capacity for parks | F&B POS | CONTRACTED | `createChannelCapacity` |
| 2.13.40 | Capacity Management Visibility | Ticketing Sales | CONTRACTED | `listChannelCapacities` |
| … 22 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Catalog Builder & Store Assortment maps which products sell on which channel (on-site, online, or restricted), managed at catalog level rather than per individual product. *(client request · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management · DI-356)*
- Prices are set per channel (web store, mobile app, kiosk, walk-up/POS) in one centralised "price matrix"; each channel picks up its price automatically once published. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-140)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-013` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 5.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 5.dc.html#ret-5g`
- Flow F77 *A promotion is built, bundled, published and measured*, step 1: Channel & Distribution. → **Drawn by the client as RET-5G.** 6 operations on this step.
- Flow F77 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (54 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-013?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Save channel allocations, Create channel capacity, Release channel allocation, Save channel capacity, Publish bundle, Save channel listing, What publishing changes.
- [ ] Every transition is wired: `BO-007`, `BO-008`, `BO-009`, `BO-011`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-014` Catalogue Publishing

**Push catalogue changes live, or schedule them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listProducts` reads the population and `getProduct` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `itemId` (deepLink), `priceListId` (deepLink), `productId` (deepLink) · cold entry: An item opened from the catalogue. A price list opened from the price book. A product opened from the directory. |
| Route | `/venue-operations/catalogue-publishing` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board.** Answers 2 board screen(s): Availability, Pricing, Channels & Publishing; Product Availability, Lifecycle & Publishing. **The board specifies this screen further rather than replacing it** — the id, its flows and its navigation are unchanged, which is what keeps 3,184 traceability rows and every board anchor pointing at something real.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listProducts`. | `listProducts` ?venueId |
| Kind | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Sends `?kind=` to `listProducts`. | `listProducts` ?kind |
| Is sellable | toggle | optional | — | — | — | Sends `?isSellable=` to `listProducts`. | `listProducts` ?isSellable |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Form: Create product** (modal, opened by *Create product*; *Create product* calls `createProduct`, *Cancel* sends nothing)

**Collects what `createProduct` sends before it is called.** Required: `code`, `name`, `kind`, `venueId`. Optional: `description`, `channels`, `entitlementTemplateId`, `dataMaskValues`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; A code already used by any product in the tenant, at any venue, is refused with `409 duplicate-code`. | — | Unique per tenant (decided 28 September, audit R108). A code already used by any product in the tenant, at any venue, is refused with `409 duplicate-code`. | `createProduct` body |
| Family key `familyKey` | text field | optional | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; At most one product per venue in a family, else `409 duplicate-code`. | — | The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. | `createProduct` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createProduct` body |
| Description `description` | text area | optional | — | — | — | — | `createProduct` body |
| Kind `kind` | select | required | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: valid on any date within an eligible … | `createProduct` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createProduct` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createProduct` body |
| Entitlement template `entitlementTemplateId` | picker: choose an entitlement template | optional | — | — | shows names, sends the id | — | `createProduct` body |
| Data mask values `dataMaskValues` | key and value settings | optional | — | — | — | — | `createProduct` body |
| Guest listing `guestListing` | segmented control | optional | Bookable | Bookable · Info only · Hidden; `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. | — | How a product appears to a guest (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. | `createProduct` body |
| Not bookable label `notBookableLabel` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createProduct` body |
| Sales contact `salesContact` | group | optional | — | — | — | See `Product.salesContact` (W3, 29 September). | `createProduct` body |
| Phone `salesContact.phone` | phone field | optional | — | max length 32 | +971 5X XXX XXXX (E.164) | — | `createProduct` body |
| Email `salesContact.email` | email field | optional | — | max length 254 | name@example.ae | — | `createProduct` body |
| Note `salesContact.note` | text, one per language | optional | — | At most 200 characters per language. | English and Arabic (Arabic right to left) | A line shown under the contact, e.g. *Group courses are booked by phone*. | `createProduct` body |
| Booking flow `bookingFlowId` | picker: choose a booking flow | optional | — | — | shows names, sends the id | See `Product.bookingFlowId` (W8, W12, 29 September). | `createProduct` body |
| Display tags `displayTags` | repeatable rows | optional | — | at most 6 | — | — | `createProduct` body |
| Kind `displayTags[].kind` | radio group | required | — | Clock · Height · Free · Calendar · ID | — | `clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring. | `createProduct` body |
| Label `displayTags[].label` | text, one per language | required | — | Each language value at most 40 characters. | English and Arabic (Arabic right to left) | What the guest reads, e.g. *2 Hours*. | `createProduct` body |
| Media `media` | repeatable rows | optional | — | at most 20 | — | — | `createProduct` body |
| Asset `media[].assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | A `MediaAsset` of `assets.yaml`, in status `ready`. | `createProduct` body |
| Kind `media[].kind` | segmented control | required | — | Image · Video | — | — | `createProduct` body |
| Is primary `media[].isPrimary` | toggle | required | off | — | — | The item *Read more* opens on and a listing shows. Exactly one per product. | `createProduct` body |
| Display order `media[].displayOrder` | number field | optional | 100 | — | — | — | `createProduct` body |
| Alt text `media[].altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createProduct` body |
| Consent questions `consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates | — | — | `createProduct` body |
| Requires time window `requiresTimeWindow` | toggle | optional | — | — | — | — | `createProduct` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A `media` asset that is not `ready` or whose kind does not match, a `consentQuestionIds` entry that names no active consent question of the tenant, or …

**Form: Save alternative codes** (modal, opened by *Save alternative codes*; *Save alternative codes* calls `setAlternativeCodes`, *Cancel* sends nothing)

**Collects what `setAlternativeCodes` sends before it is called.** Required: `codes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Codes `codes` | repeatable rows | required | — | — | — | — | `setAlternativeCodes` body |
| Code `codes[].code` | text field | required | — | max length 128 | — | — | `setAlternativeCodes` body |
| Partner `codes[].partnerId` | picker: choose a partner | required | — | — | shows names, sends the id | — | `setAlternativeCodes` body |
| Partner name `codes[].partnerName` | text field | optional | — | — | — | — | `setAlternativeCodes` body |
| Variant `codes[].variantId` | picker: choose a variant | optional | — | — | shows names, sends the id | — | `setAlternativeCodes` body |
| Note `codes[].note` | text area | optional | — | max length 200 | — | — | `setAlternativeCodes` body |

Errors to draw in the form: 400 A `variantId` is not a variant of this product, or the body sends one code twice for the same partner.; 409 Code already mapped to a different product for that partner

**Form: Save product attributes** (modal, opened by *Save product attributes*; *Save product attributes* calls `setProductAttributes`, *Cancel* sends nothing)

**Collects what `setProductAttributes` sends before it is called.** Required: `axes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Axes `axes` | repeatable rows | required | — | — | — | — | `setProductAttributes` body |
| Code `axes[].code` | text field | required | — | max length 64 | — | — | `setProductAttributes` body |
| Name `axes[].name` | text field | required | — | max length 200 | — | — | `setProductAttributes` body |
| Values `axes[].values` | repeatable rows | required | — | at least 1 | — | — | `setProductAttributes` body |
| Code `axes[].values[].code` | text field | required | — | max length 64 | — | — | `setProductAttributes` body |
| Label `axes[].values[].label` | text field | required | — | max length 200 | — | — | `setProductAttributes` body |
| Price delta `axes[].values[].priceDelta` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setProductAttributes` body |
| Duration minutes `axes[].values[].durationMinutes` | number field (minutes) | optional | — | min 15; max 1440; One axis per product at most may carry it; a second is a `400`. | — | How long a variant carrying this value books its space for, on a `length` axis of a product with `requiresTimeWindow` (decided 29 September, rev 3 REV3-13). | `setProductAttributes` body |

Errors to draw in the form: 400 Two axes share a code, or one axis repeats a value code.; 403 Authenticated but not permitted at the requested scope; 409 Regeneration would exceed the variant ceiling for this product: `VenueSettings.catalogue.maxVariantsPerProduct`, a venue setting with a tenant default (decided …

**Form: Transition product lifecycle** (modal, opened by *Transition product lifecycle*; *Transition product lifecycle* calls `transitionProductLifecycle`, *Cancel* sends nothing)

**Collects what `transitionProductLifecycle` sends before it is called.** Required: `transition`, `reason`. Optional: `effectiveAt`. The transition picker lists only what the principal may do — approve needs `PRODUCT_APPROVE`, publish needs `PRODUCT_PUBLISH` (decided 28 September, audit R091 (2)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Transition `transition` | select | required | — | Submit for review · Approve · Reject · Publish · Withdraw · Archive · Restore | — | — | `transitionProductLifecycle` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `transitionProductLifecycle` body |
| Effective at `effectiveAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `transitionProductLifecycle` body |

Errors to draw in the form: 403 Approval attempted by the principal who submitted it (`approver-is-submitter`). Segregation applies here as it does to journals.; 409 Transition not valid from the current state, or archiving attempted while unexpired entitlements exist.

**Form: Save product** (modal, opened by *Save product*; *Save product* calls `updateProduct`, *Cancel* sends nothing)

**Collects what `updateProduct` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `channels`, `dataMaskValues`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Family key `familyKey` | text field | optional | — | max length 64; pattern `^[A-Za-z0-9_-]+$`; At most one product per venue in a family, else `409 duplicate-code`. | — | The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. | `updateProduct` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `updateProduct` body |
| Description `description` | text area | optional | — | — | — | — | `updateProduct` body |
| Channels `channels` | multi-select chips | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `updateProduct` body |
| Data mask values `dataMaskValues` | key and value settings | optional | — | — | — | — | `updateProduct` body |
| Guest listing `guestListing` | segmented control | optional | Bookable | Bookable · Info only · Hidden; `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. | — | How a product appears to a guest (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. | `updateProduct` body |
| Not bookable label `notBookableLabel` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateProduct` body |
| Sales contact `salesContact` | group | optional | — | — | — | See `Product.salesContact` (W3, 29 September). | `updateProduct` body |
| Phone `salesContact.phone` | phone field | optional | — | max length 32 | +971 5X XXX XXXX (E.164) | — | `updateProduct` body |
| Email `salesContact.email` | email field | optional | — | max length 254 | name@example.ae | — | `updateProduct` body |
| Note `salesContact.note` | text, one per language | optional | — | At most 200 characters per language. | English and Arabic (Arabic right to left) | A line shown under the contact, e.g. *Group courses are booked by phone*. | `updateProduct` body |
| Booking flow `bookingFlowId` | picker: choose a booking flow | optional | — | — | shows names, sends the id | See `Product.bookingFlowId` (W8, W12, 29 September). | `updateProduct` body |
| Display tags `displayTags` | repeatable rows | optional | — | at most 6 | — | — | `updateProduct` body |
| Kind `displayTags[].kind` | radio group | required | — | Clock · Height · Free · Calendar · ID | — | `clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring. | `updateProduct` body |
| Label `displayTags[].label` | text, one per language | required | — | Each language value at most 40 characters. | English and Arabic (Arabic right to left) | What the guest reads, e.g. *2 Hours*. | `updateProduct` body |
| Media `media` | repeatable rows | optional | — | at most 20 | — | — | `updateProduct` body |
| Asset `media[].assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | A `MediaAsset` of `assets.yaml`, in status `ready`. | `updateProduct` body |
| Kind `media[].kind` | segmented control | required | — | Image · Video | — | — | `updateProduct` body |
| Is primary `media[].isPrimary` | toggle | required | off | — | — | The item *Read more* opens on and a listing shows. Exactly one per product. | `updateProduct` body |
| Display order `media[].displayOrder` | number field | optional | 100 | — | — | — | `updateProduct` body |
| Alt text `media[].altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateProduct` body |
| Consent questions `consentQuestionIds` | multi-picker: choose consent questions | optional | — | at most 10; no duplicates | — | — | `updateProduct` body |
| Requires time window `requiresTimeWindow` | toggle | optional | — | — | — | — | `updateProduct` body |

Errors to draw in the form: 400 `media` with no `isPrimary` item or more than one, or one asset twice.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A `media` asset that is not `ready` or whose kind does not match, a `consentQuestionIds` entry that names no active consent question of the tenant, or …

**Form: Publish bundle** (modal, opened by *Publish bundle*; *Publish bundle* calls `publishBundle`, *Cancel* sends nothing)

**Collects what `publishBundle` sends before it is called.** Required: `venueId`. Optional: `note`, `staleAfterHours`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `publishBundle` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `publishBundle` body |
| Stale after hours `staleAfterHours` | number field (hours) | optional | — | min 1 | — | How long a terminal may trade on this bundle before refusing. Defaults to the venue's configured bound. | `publishBundle` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue

**Form: Save item availability** (modal, opened by *Save item availability*; *Save item availability* calls `setItemAvailability`, *Cancel* sends nothing)

**Collects what `setItemAvailability` sends before it is called.** Required: `isAvailable`, `recordedAt`. Optional: `reason`, `restoreAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is available `isAvailable` | toggle | required | — | — | — | — | `setItemAvailability` body |
| Reason `reason` | radio group | optional | — | Sold out · Ingredient unavailable · Equipment down · Seasonal · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `setItemAvailability` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `setItemAvailability` body |
| Restore at `restoreAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Automatic restore, typically at next service. Kept as `MenuItem.restoreAt`. | `setItemAvailability` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `setItemAvailability` body |

Errors to draw in the form: 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

#### Outputs: what the screen shows and produces

**Shown**

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**Every alternative code** (data table, from `listAlternativeCodes`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Partner | the name it points at, never the id | — |
| Partner name | text | — |
| Variant | the name it points at, never the id | — |
| Note | text | — |

**Every product variant** (data table, from `listProductVariants`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| SKU | text | — |
| Axis values | grouped details | — |
| Name | text | Taken from their variant tables, 20 September. `axisValues` gives `{size: L}` and no string a guest can read. |
| Barcode | text | Taken from their variant tables, 20 September. `catalogue.alternative_code` is a partner's own code for a variant and requires `partnerId` … |
| Is default | yes / no (icon or chip) | Taken from their variant tables. Which variant a product page opens on. |
| Is active | yes / no (icon or chip) | False when retired. Retired variants are never deleted — orders reference them. |

**Every price** (data table, from `listPrices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Price list | the name it points at, never the id | — |
| Variant | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax code | the name it points at, never the id | — |

**The selected product** (detail panel, from `getProduct`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Created by principal | the name it points at, never the id | 1.4.18. The approval gate refuses an approver who is the author, and nothing recorded either. |
| Approved by principal | the name it points at, never the id | — |
| Responsible department | the name it points at, never the id | Who owns this product commercially. A scope node at `department` level. |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Has variants | yes / no (icon or chip) | — |
| Variant count | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Create product (primary button) | `createProduct` POST `/products` | CreateProductRequest | Product | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names … | opens modal first |
| Resolve product by code (secondary button) | `resolveProductByCode` GET `/products/resolve` | — | ProductVariant | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Save alternative codes (secondary button) | `setAlternativeCodes` PUT `/products/{productId}/alternative-codes` | inline | AlternativeCode[] | 400 A `variantId` is not a variant of this product, or the body sends one code twice for the same partner.; 409 Code already mapped to a different product for that partner | opens modal first |
| Save product attributes (secondary button) | `setProductAttributes` PUT `/products/{productId}/attributes` | inline | inline | 400 Two axes share a code, or one axis repeats a value code.; 403 Authenticated but not permitted at the requested scope; 409 Regeneration would exceed the variant ceiling for this product … | opens modal first |
| Transition product lifecycle (secondary button) | `transitionProductLifecycle` POST `/products/{productId}/lifecycle` | inline | Product | 403 Approval attempted by the principal who submitted it (`approver-is-submitter`). Segregation applies here as it does to journals.; 409 Transition not valid from the current state, or archiving attempted while … | opens modal first |
| Save product (secondary button) | `updateProduct` PATCH `/products/{productId}` | UpdateProductRequest | Product | 400 `media` with no `isPrimary` item or more than one, or one asset twice.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a … | opens modal first |
| Publish bundle (secondary button) | `publishBundle` POST `/catalogue/bundles` | inline | BundleSummary | 403 Authenticated but not permitted at the requested scope; 409 A publish is already in progress for this venue | opens modal first |
| Save item availability (secondary button) | `setItemAvailability` PUT `/menu-items/{itemId}/availability` | inline | MenuItem | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listProducts` (onLoad, List products); `listPrices` (onLoad, List prices in a list)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*; carries `productId`
- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `productId`, `variantId`, `version`
- → `BO-009` Pricing Rules: *Pricing Rules*; carries `priceListId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The catalogue publishing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the catalogue publishing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No catalogue publishing yet. Offers Create product (`createProduct`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind, isSellable and the catalogue publishing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A `variantId` is not a variant of this product, or the body sends one code twice for the same partner.; 400 Two axes share a code, or one axis repeats a value code.; 400 Validation failed |

#### Permissions

- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `createProduct` → `PRODUCT_CONFIGURE` (configure) · staff
- `listAlternativeCodes` → `PRODUCT_VIEW` (read) · staff, partner
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `resolveProductByCode` → `PRODUCT_VIEW` (read) · staff, partner
- `setAlternativeCodes` → `PRODUCT_CONFIGURE` (configure) · staff
- `setProductAttributes` → `PRODUCT_CONFIGURE` (configure) · staff
- `transitionProductLifecycle` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateProduct` → `PRODUCT_CONFIGURE` (configure) · staff
- `listPrices` → `PRICE_VIEW` (read) · staff, partner
- `publishBundle` → `PRODUCT_CONFIGURE` (configure) · staff
- `setItemAvailability` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listProducts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

71 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 19.2.21 | VIP Package Purchases - System shall support VIP package purchases. | Guest Mobile App & Branding | CONTRACTED | `createProduct` |
| 1.1.1 | The system should be able to sell open-dated tickets for attractions. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.6 | The system should be able to sell membership passes for an attraction (e.g. annual pass, monthly pass) for configurable duration. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.8 | The system should be able to sell add-on items for all type of tickets. Add-ons can also be configured as a stand-alone product and able to be purchased on their own. | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.42 | Configure unlimited ticket products and categories | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.44 | Support admission, membership, voucher, package and pass products | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.93 | Membership product management | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.1.124 | Channel-based restrictions | Ticketing Catalogue | CONTRACTED | `createProduct` |
| 1.3.52 | Wall climbing activities (product management, sales, ticketing, bookings). | Ticketing Catalogue | CONTRACTED | `createProduct` |
| … 59 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-014` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 2.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 2.dc.html#fnb-2h`, `Retail Board 2.dc.html#ret-2h`
- Flow F78 *A supplier is set up and a catalogue is priced and published*, step 4: The priced range is published to the tills. → **Publishing is what changes what every till charges**, which is why it is its own step.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (78), with its required mark, default, format and its error state (400, 403, 404, 409, 412, 422).
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Create product, Resolve product by code, Save alternative codes, Save product attributes, Transition product lifecycle, Save product, Publish bundle, Save item availability, What publishing changes.
- [ ] Every transition is wired: `BO-007`, `BO-008`, `BO-009`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-015` Performance Calendar

**See what is scheduled and how full it is.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPerformances` reads the population and `getPerformance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `eventId` (deepLink), `performanceId` (deepLink) · cold entry: **A link to a performance that has happened.** Offers the next performance of the same event. |
| Route | `/venue-operations/session-calendar` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2a`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.** **Kept separate from BO-016 (decided 28 September, audit R276)** — this screen lists, creates, changes and cancels performances; the template they are generated from is BO-016 Performance Template.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?from=` to `listPerformances`. | `listPerformances` ?from |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?to=` to `listPerformances`. | `listPerformances` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Section code | text field | — | — | `getSeatAvailability` ?sectionCode |
| Category | picker: choose a category | — | — | `getSeatAvailability` ?categoryId |
| Available only | toggle | off | — | `getSeatAvailability` ?availableOnly |
| Mode | segmented control | Auto | Auto · Graphical · List | `getSeatAvailability` ?mode |

**Form: Create performances** (modal, opened by *Create performances*; *Create performances* calls `createPerformances`, *Cancel* sends nothing)

**Collects what `createPerformances` sends before it is called.** Required: `startsAt`, `endsAt`. Optional: `admissionRulesId`, `seatMapId`, `language` (BCP 47, e.g. `ar`, `fr`) and `format` (e.g. 2D, 3D, subtitled) for a tour or a screening (decided 29 September, rev 3 REV3-17), `recurrence`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | optional | — | — | shows names, sends the id | — | `createPerformances` body |
| Seat map `seatMapId` | picker: choose a seat map | optional | — | — | shows names, sends the id | — | `createPerformances` body |
| Language `language` | text field | optional | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | — | As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17). | `createPerformances` body |
| Format `format` | text field | optional | — | max length 40 | — | As `Performance.format` (decided 29 September, rev 3 REV3-17). | `createPerformances` body |
| Recurrence `recurrence` | group | optional | — | — | — | Generate a series rather than a single performance. Read in the region's time zone: the Region owns the zone and every venue inherits it without override (tenancy), so … | `createPerformances` body |
| Interval minutes `recurrence.intervalMinutes` | number field (minutes) | optional | — | min 1 | — | — | `createPerformances` body |
| Until `recurrence.until` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPerformances` body |
| Days of week `recurrence.daysOfWeek` | list of values (chips) | optional | — | — | — | — | `createPerformances` body |

**Form: Create event** (modal, opened by *Create event*; *Create event* calls `createEvent`, *Cancel* sends nothing)

**Collects what `createEvent` sends before it is called.** Required: `code`, `name`, `venueId`. Optional: `parentEventId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; A code already used by any event in the tenant is refused with `409 duplicate-code`. | — | Unique per tenant (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`. | `createEvent` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createEvent` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createEvent` body |
| Parent event `parentEventId` | picker: choose a parent event | optional | — | — | shows names, sends the id | — | `createEvent` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

**Form: Recommend seats** (modal, opened by *Recommend seats*; *Recommend seats* calls `recommendSeats`, *Cancel* sends nothing)

**Collects what `recommendSeats` sends before it is called.** Required: `partySize`, `strategy`. Optional: `categoryIds`, `maxPrice`, `accessibleCount`, `maxOptions`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Party size `partySize` | stepper or slider | required | — | min 1; max 50 | — | — | `recommendSeats` body |
| Strategy `strategy` | radio group | required | — | Best available · Best value · Closest to stage · Accessible · Contiguous | — | — | `recommendSeats` body |
| Categorys `categoryIds` | multi-picker: choose categorys | optional | — | — | — | — | `recommendSeats` body |
| Max price `maxPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `recommendSeats` body |
| Accessible count `accessibleCount` | number field | optional | 0 | — | — | Wheelchair spaces in the party. Companions are added automatically. | `recommendSeats` body |
| Max options `maxOptions` | number field | optional | 3 | max 10 | — | — | `recommendSeats` body |

Errors to draw in the form: 404 No selection satisfies the constraints

**Form: Save event** (modal, opened by *Save event*; *Save event* calls `updateEvent`, *Cancel* sends nothing)

**Collects what `updateEvent` sends before it is called.** Nothing in the body is required. Optional: `name`, `parentEventId`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateEvent` body |
| Parent event `parentEventId` | picker: choose a parent event | optional | — | — | shows names, sends the id | — | `updateEvent` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateEvent` body |

**Form: Save performance** (modal, opened by *Save performance*; *Save performance* calls `updatePerformance`, *Cancel* sends nothing)

**Collects what `updatePerformance` sends before it is called.** Nothing in the body is required. Optional: `startsAt`, `endsAt`, `status`, `admissionRulesId`, `language`, `format` (rev 3 REV3-17). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Starts at `startsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePerformance` body |
| Ends at `endsAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePerformance` body |
| Status `status` | segmented control | optional | — | Scheduled · On sale · Suspended | — | — | `updatePerformance` body |
| Admission rules `admissionRulesId` | picker: choose an admission rules | optional | — | — | shows names, sends the id | — | `updatePerformance` body |
| Language `language` | text field | optional | — | max length 35; pattern `^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$` | — | As `Performance.language` (decided 29 September, rev 3 REV3-17). | `updatePerformance` body |
| Format `format` | text field | optional | — | max length 40 | — | As `Performance.format` (decided 29 September, rev 3 REV3-17). | `updatePerformance` body |

Errors to draw in the form: 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow.

**Sent by *Cancel performance*** (`cancelPerformance`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `cancelPerformance` body |
| Guest message `guestMessage` | key and value settings | optional | — | — | — | — | `cancelPerformance` body |
| Refund percentage `refundPercentage` | stepper or slider | optional | 100 | min 0; max 100 | — | — | `cancelPerformance` body |
| Offer alternative performance `offerAlternativePerformanceId` | picker: choose an offer alternative performance | optional | — | — | shows names, sends the id | — | `cancelPerformance` body |
| Dry run `dryRun` | toggle | optional | off | — | — | — | `cancelPerformance` body |
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | Required unless `dryRun` (audit R144, proposed by the coordinator). | `cancelPerformance` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `cancelPerformance` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `cancelPerformance` body |

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `listPerformances`): Performances by day, week or month; a slot opens its performance. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Sends the visible window as `from`/`to` and the category filter as `categoryId`.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Language | text | The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). |
| Format | text | How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Every performance** (data table, from `listPerformances`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Language | text | The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). |
| Format | text | How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. |

**Every event** (data table, from `listEvents`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Parent event | the name it points at, never the id | For grouped events. |
| Performance count | 1,234 | How many performances the event has. Counted by the server; never sent by a client. |
| Is active | yes / no (icon or chip) | — |

**The selected performance** (detail panel, from `getPerformance`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Approval request | the name it points at, never the id | BL-048. The approval chain and the occurrence lifecycle sat on different entities, so neither was complete: `states/performance.yaml` … |
| Requires approval to cancel | yes / no (icon or chip) | Cancelling a sold performance is the one transition that needs a name against it. |
| Status | chip: Scheduled, On sale, Sold out, Suspended, Cancelled, Completed | — |
| Admission rules | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Language | text | The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). |
| Format | text | How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. |

**The event** (detail panel, from `getEvent`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Parent event | the name it points at, never the id | For grouped events. |
| Performance count | 1,234 | How many performances the event has. Counted by the server; never sent by a client. |
| Is active | yes / no (icon or chip) | — |

**The seat availability** (detail panel, from `getSeatAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Performance | the name it points at, never the id | — |
| Seat map | the name it points at, never the id | — |
| Render mode | chip: Graphical, List | The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat … |
| Totals | grouped details | — |
| By category | list or chips (count when long) | — |
| Seats | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create time slots (primary button) | `createPerformances` POST `/events/{eventId}/performances` | CreatePerformancesRequest | inline | — | opens modal first |
| Cancel performance (destructive button) | `cancelPerformance` POST `/performances/{performanceId}/cancel` | inline | PerformanceCancellationResult | 403 The supervisor step-up is missing or failed (audit R144). The PIN did not verify, or the principal does not hold `PERFORMANCE_CONFIGURE` at this venue.; 409 The performance is `cancelled`, `completed` or `soldOut`. … | step-up: pin (Cancels a performance and queues refunds to every holder; a supervisor signs it in place (proposed by the coordinator …) |
| Create event (secondary button) | `createEvent` POST `/events` | CreateEventRequest | Event | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |
| Recommend seats (secondary button) | `recommendSeats` POST `/performances/{performanceId}/seat-recommendations` | SeatRecommendationRequest | inline | 404 No selection satisfies the constraints | opens modal first |
| Save event (secondary button) | `updateEvent` PATCH `/events/{eventId}` | inline | Event | — | opens modal first |
| Save performance (secondary button) | `updatePerformance` PATCH `/performances/{performanceId}` | inline | Performance | 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow. | opens modal first |

**Data it reads**: `getPerformance` (onLoad, Read a performance); `getSeatAvailability` (onLoad, Seat status for a performance); `listEvents` (onLoad, List events)

**Where the user goes next**

- → `BO-001` Queue Directory: *Queue Directory*; carries `eventId`
- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*
- → `BO-099` Performance Manifest: *Performance manifest*; carries `performanceId`

**What opens over it**

- confirmDialog *Cancel performance*: **Names what `cancelPerformance` changes and what it leaves alone**, in the consequence rather than the verb. A session calendar this affects should be identified in the dialog, not just counted. **Collects what `cancelPerformance` sends before it is called.** Required: `reason`. Optional …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The session calendar list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the session calendar untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No session calendar yet. Offers Create performances (`createPerformances`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on from, to and the session calendar are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 A timing change on a performance with sold tickets, or a `status` move the state model does not allow.; 409 The performance is `cancelled`, `completed` or `soldOut`. `states/performance.yaml` cancels only from `scheduled`, `onSale` … |

#### Permissions

- `listPerformances` → `PRODUCT_VIEW` (read) · staff, guest
- `getPerformance` → `PRODUCT_VIEW` (read) · staff, guest
- `createPerformances` → `PERFORMANCE_CONFIGURE` (configure) · staff
- `cancelPerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff · step-up pin
- `createEvent` → `EVENT_CONFIGURE` (configure) · staff
- `getEvent` → `PRODUCT_VIEW` (read) · staff
- `getSeatAvailability` → `PRODUCT_VIEW` (read) · staff, guest
- `listEvents` → `PRODUCT_VIEW` (read) · staff
- `recommendSeats` → `PRODUCT_VIEW` (read) · staff, guest
- `updateEvent` → `EVENT_CONFIGURE` (configure) · staff
- `updatePerformance` → `PERFORMANCE_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listPerformances` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

38 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.34 | Time Slot Reservations - System shall support time slot reservations. | Guest Mobile App & Branding | CONTRACTED | `listPerformances` |
| 2.6.15 | - Time slots for events | Ticketing Sales | CONTRACTED | `listPerformances` |
| 2.7.16 | - Dedicated sales calendar | Ticketing Sales | CONTRACTED | `listPerformances` |
| 1.1.2 | The system should be able to sell dated tickets for attractions that allow access only for selected dates by guest. Special day tickets should also be supported. These are dated tickets that skip … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.4 | The system should provide an easy-to-use interface for creation and configuration of timeslots. A calendar view should be available for the user to define the timeslot and recurrence rules. The user … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.85 | Performance-based validity | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.1.86 | Performance date/time validity | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.3.2 | The system should allow configuration of event details such as start time (date & time), end time, duration of event, capacity (amount of places that can be sold for an event), seating categories … | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.3.3 | The system should support multiple occurrences/sessions, defined by a date, time, space, capacity and/or seating arrangement. | Ticketing Catalogue | CONTRACTED | `createPerformances` |
| 1.3.20 | System shall support event cancellation workflows including refunds, exchanges, notifications and audit tracking. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.3.21 | System shall support changing event dates, times and venues while automatically updating tickets, reservations and guest communications. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| 1.4.4 | The system should propagate any changes made to the properties of a product to the already sold tickets as well. | Ticketing Catalogue | CONTRACTED | `cancelPerformance` |
| … 26 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Time-slot creation asks for start and end date, first and last start time of the day, interval between starts (e.g. every 30 minutes), slot length, days of the week, language and format, and previews the slots before any is created. *(agreed · MoM 24 Sep 2026, M24-01 · DI-995)*
- Example the configuration screens must show concretely: how time slots are created, including start/end dates, times and interval parameters. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-986)*
- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Performance capacity is edited individually or by multi-select bulk edit; a performance can be suspended, resumed (any time before start) or cancelled — a state change, never a delete. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-168)*
- Performance (time-slot) creation: date range with chosen weekdays or all days, start/end time, slot duration (e.g. 30 or 60 min), "minutes on screen" (e.g. a 10:00 slot sellable at POS until 10:10), separate entry window (e.g. from 9:30, cut-off 10:20), and an on-sale date range; bulk creation across a date range. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-167)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-015` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 2.dc.html`
- Client design-board frames: `Seat Board 2.dc.html#seat-2a`

#### Acceptance for the design

- [ ] Every input above is drawn (39), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (58 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create time slots, Cancel performance, Create event, Recommend seats, Save event, Save performance.
- [ ] Every transition is wired: `BO-001`, `BO-007`, `BO-009`, `BO-099`.
- [ ] Every gated control is gated: `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-016` Performance Template

**Define the pattern the calendar is generated from — slot length, turnaround, concurrent capacity, peak bands and walk-in rules. BO-015 Performance Calendar generates and manages the performances themselves (kept separate, decided 28 September, audit R276).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PERFORMANCE_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPerformanceTemplates` reads the population and the selected row is the detail; `setPerformanceTemplate` saves one — list, select, act |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/session-template` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 26 August** — `Seat Board 2.dc.html` frame `seat-2b`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.** **Split from BO-015 on 28 September (audit R276)** — the two carried identical performance and event operations; this screen now owns the performance template (`listPerformanceTemplates`, `setPerformanceTemplate`) and BO-015 keeps the calendar of performances.

#### Inputs: what the user enters or picks

**Form: Save performance template** (modal, opened by *Save performance template*; *Save performance template* calls `setPerformanceTemplate`, *Cancel* sends nothing)

**Collects what `setPerformanceTemplate` sends before it is called.** Required: `code`. Optional: `id`, `name`, `spaceId`, `slotMinutes`, `turnaroundMinutes`, `concurrentCapacity`, `bands`, `walkIn`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `setPerformanceTemplate` body |
| Code `code` | text field | required | — | — | — | — | `setPerformanceTemplate` body |
| Name `name` | text field | optional | — | — | — | — | `setPerformanceTemplate` body |
| Space `spaceId` | picker: choose a space | optional | — | — | shows names, sends the id | — | `setPerformanceTemplate` body |
| Slot minutes `slotMinutes` | number field (minutes) | optional | — | — | — | — | `setPerformanceTemplate` body |
| Turnaround minutes `turnaroundMinutes` | number field (minutes) | optional | 0 | — | — | — | `setPerformanceTemplate` body |
| Concurrent capacity `concurrentCapacity` | number field | optional | — | — | — | — | `setPerformanceTemplate` body |
| Bands `bands` | repeatable rows | optional | — | — | — | — | `setPerformanceTemplate` body |
| Kind `bands[].kind` | radio group | optional | — | Off peak · Standard · Peak · Super prime | — | — | `setPerformanceTemplate` body |
| Days of week `bands[].daysOfWeek` | list of values (chips) | optional | — | — | — | — | `setPerformanceTemplate` body |
| From `bands[].from` | text field | optional | — | — | — | — | `setPerformanceTemplate` body |
| To `bands[].to` | text field | optional | — | — | — | — | `setPerformanceTemplate` body |
| Price multiplier `bands[].priceMultiplier` | number field | optional | — | — | — | — | `setPerformanceTemplate` body |
| Minute multiplier `bands[].minuteMultiplier` | number field | optional | — | — | — | — | `setPerformanceTemplate` body |
| Walk in `walkIn` | group | optional | — | — | — | Configured, not assumed. It decides whether a family turning up on a Sunday is turned away. | `setPerformanceTemplate` body |
| Allowed `walkIn.allowed` | toggle | optional | on | — | — | — | `setPerformanceTemplate` body |
| Held back percent `walkIn.heldBackPercent` | number field | optional | 0 | — | — | — | `setPerformanceTemplate` body |
| Cutoff minutes before `walkIn.cutoffMinutesBefore` | number field (minutes) | optional | — | — | — | — | `setPerformanceTemplate` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setPerformanceTemplate` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every performance template** (data table, from `listPerformanceTemplates`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Space | the name it points at, never the id | — |
| Slot minutes | 1,234 | — |
| Turnaround minutes | 1,234 | — |
| Concurrent capacity | 1,234 | — |

**The selected performance template** (detail panel, from `listPerformanceTemplates`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Space | the name it points at, never the id | — |
| Slot minutes | 1,234 | — |
| Turnaround minutes | 1,234 | — |
| Concurrent capacity | 1,234 | — |
| Bands | list or chips (count when long) | — |
| Walk in | grouped details | Configured, not assumed. It decides whether a family turning up on a Sunday is turned away. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save performance template (primary button) | `setPerformanceTemplate` PUT `/performance-templates` | PerformanceTemplate | PerformanceTemplate | — | opens modal first |

**Data it reads**: `listPerformanceTemplates` (onLoad, Slot templates, peak bands and walk-in rules)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The performance template list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the performance templates untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No performance template yet. Offers Save performance template (`setPerformanceTemplate`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listPerformanceTemplates` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PERFORMANCE_CONFIGURE`, which `listPerformanceTemplates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPerformanceTemplates` → `PERFORMANCE_CONFIGURE` (configure) · staff
- `setPerformanceTemplate` → `PERFORMANCE_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PERFORMANCE_CONFIGURE`, which `listPerformanceTemplates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Example the configuration screens must show concretely: how time slots are created, including start/end dates, times and interval parameters. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-986)*
- Performances are created individually or from a reusable time-slot template (e.g. every 30 minutes between start and end) that auto-generates the schedule. Capacity set at event level is inherited by performances, with per-performance override (e.g. evening slots). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-453)*
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)*
- Event ticket setup: validity window; recurring performances; admission model (general admission, capacity control, reserved seating, resource control, none); seat map, section and quota per sales channel (shared pool or split); resources (e.g. vehicle + driver for a desert safari) checked for availability before sale. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-436)*
- Performance (time-slot) creation: date range with chosen weekdays or all days, start/end time, slot duration (e.g. 30 or 60 min), "minutes on screen" (e.g. a 10:00 slot sellable at POS until 10:10), separate entry window (e.g. from 9:30, cut-off 10:20), and an on-sale date range; bulk creation across a date range. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-167)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-016` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/Seat Board 2.dc.html`
- Client design-board frames: `Seat Board 2.dc.html#seat-2b`

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state.
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-016?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save performance template.
- [ ] Every transition is wired: `BO-007`, `BO-009`.
- [ ] Every gated control is gated: `PERFORMANCE_CONFIGURE`.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-017` Capacity Management

**Change how many people a performance can take (renamed from session, decided 28 September, audit R165).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listChannelCapacities` reads the population and `getChannelAllocations` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `channelCapacityId` (deepLink), `entryId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/capacity-management` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Performance id | picker: choose a performance (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?performanceId=` to `listChannelCapacities`. | `listChannelCapacities` ?performanceId |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listWaitlistEntries` ?performanceId |

**Form: Create channel capacity** (modal, opened by *Create channel capacity*; *Create channel capacity* calls `createChannelCapacity`, *Cancel* sends nothing)

**Collects what `createChannelCapacity` sends before it is called.** Required: `performanceId`, `name`, `capacity`. Optional: `seatCategoryId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Performance `performanceId` | picker: choose a performance | required | — | — | shows names, sends the id | — | `createChannelCapacity` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createChannelCapacity` body |
| Seat category `seatCategoryId` | picker: choose a seat category | optional | — | — | shows names, sends the id | — | `createChannelCapacity` body |
| Capacity `capacity` | number field | required | — | min 0 | — | — | `createChannelCapacity` body |

**Form: Release channel allocation** (modal, opened by *Release channel allocation*; *Release channel allocation* calls `relinquishChannelAllocation`, *Cancel* sends nothing)

**Collects what `relinquishChannelAllocation` sends before it is called.** Required: `channels`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channels `channels` | multi-select chips | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre; at least 1 | — | — | `relinquishChannelAllocation` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `relinquishChannelAllocation` body |

**Form: Save channel allocations** (modal, opened by *Save channel allocations*; *Save channel allocations* calls `setChannelAllocations`, *Cancel* sends nothing)

**Collects what `setChannelAllocations` sends before it is called.** Required: `allocations`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Allocations `allocations` | repeatable rows | required | — | at least 1 | — | — | `setChannelAllocations` body |
| Channel `allocations[].channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `setChannelAllocations` body |
| Allocated units `allocations[].allocatedUnits` | number field | required | — | min 0 | — | — | `setChannelAllocations` body |
| Release at `allocations[].releaseAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it. | `setChannelAllocations` body |
| Sales channel `allocations[].salesChannelId` | picker: choose a sales channel | optional | — | — | shows names, sends the id | The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3). | `setChannelAllocations` body |
| Allocation type `allocations[].allocationType` | radio group | optional | Dedicated | Shared pool · Dedicated · Percentage · Dynamic | — | How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row. | `setChannelAllocations` body |
| Minimum units `allocations[].minimumUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Maximum units `allocations[].maximumUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Replenishment rule `allocations[].replenishmentRule` | key and value settings | optional | — | — | — | `{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`. | `setChannelAllocations` body |
| Waitlist behavior `allocations[].waitlistBehavior` | segmented control | optional | None | None · Join waitlist · Notify on release | — | — | `setChannelAllocations` body |
| Release threshold units `allocations[].releaseThresholdUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Release hours before event `allocations[].releaseHoursBeforeEvent` | number field | optional | — | min 0 | — | Alternative to `releaseAt`, relative to the performance start. | `setChannelAllocations` body |
| Contractual units `allocations[].contractualUnits` | number field | optional | — | min 0 | — | Units a partner agreement guarantees; rebalancing never goes below it. | `setChannelAllocations` body |
| Minimum guaranteed units `allocations[].minimumGuaranteedUnits` | number field | optional | — | min 0 | — | — | `setChannelAllocations` body |
| Is frozen `allocations[].isFrozen` | toggle | optional | off | — | — | Excluded from rebalancing. | `setChannelAllocations` body |

Errors to draw in the form: 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101)

**Form: Save channel capacity** (modal, opened by *Save channel capacity*; *Save channel capacity* calls `updateChannelCapacity`, *Cancel* sends nothing)

**Collects what `updateChannelCapacity` sends before it is called.** Nothing in the body is required. Optional: `name`, `capacity`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateChannelCapacity` body |
| Capacity `capacity` | number field | optional | — | min 0 | — | — | `updateChannelCapacity` body |

Errors to draw in the form: 409 Capacity reduced below units already sold plus units under an unexpired lease (audit R101)

#### Outputs: what the screen shows and produces

**Shown**

**Every channel capacity** (data table, from `listChannelCapacities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Name | text | — |
| Seat category | the name it points at, never the id | — |
| Oversell allowance | 1,234 | BL-046, 1.3.13. The guard existed in one direction — an envelope could be raised freely and refused reduction below what had sold. |
| Oversell basis | chip: Fixed count, Historic no show rate, Percentage | — |
| Capacity | 1,234 | — |
| Sold | 1,234 | Units sold. Maintained on write (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by … |
| Leased | 1,234 | Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023). |
| Remaining | 1,234 | What can still be held. Decremented at the hold with a guarded statement (`remaining >= n`) under the row lock, never at the sale, so two … |
| Has channel allocations | yes / no (icon or chip) | True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity. |
| Is seated | yes / no (icon or chip) | Seated envelopes cannot be leased and are blocked offline. A seat map is not a count. |

**The selected channel capacity** (detail panel, from `listChannelCapacities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Performance | the name it points at, never the id | — |
| Name | text | — |
| Seat category | the name it points at, never the id | — |
| Oversell allowance | 1,234 | BL-046, 1.3.13. The guard existed in one direction — an envelope could be raised freely and refused reduction below what had sold. |
| Oversell basis | chip: Fixed count, Historic no show rate, Percentage | — |
| Capacity | 1,234 | — |
| Sold | 1,234 | Units sold. Maintained on write (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by … |
| Leased | 1,234 | Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023). |
| Remaining | 1,234 | What can still be held. Decremented at the hold with a guarded statement (`remaining >= n`) under the row lock, never at the sale, so two … |
| Has channel allocations | yes / no (icon or chip) | True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity. |
| Is seated | yes / no (icon or chip) | Seated envelopes cannot be leased and are blocked offline. A seat map is not a count. |

**The channel allocation set** (detail panel, from `getChannelAllocations`)

| Shows | Format | Notes |
|---|---|---|
| Channel capacity | the name it points at, never the id | — |
| Capacity | 1,234 | — |
| Allocations | list or chips (count when long) | — |
| General pool units | 1,234 | Unallocated remainder. Any channel may draw from it once its own allocation is exhausted. |
| Total sold | 1,234 | — |
| Total remaining | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create channel capacity (primary button) | `createChannelCapacity` POST `/channel-capacities` | CreateEnvelopeRequest | ChannelCapacity | — | opens modal first |
| Release channel allocation (secondary button) | `relinquishChannelAllocation` POST `/channel-capacities/{channelCapacityId}/channel-allocations/release` | inline | ChannelAllocationSet | — | opens modal first |
| Save channel allocations (secondary button) | `setChannelAllocations` PUT `/channel-capacities/{channelCapacityId}/channel-allocations` | inline | ChannelAllocationSet | 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101) | opens modal first |
| Save channel capacity (secondary button) | `updateChannelCapacity` PATCH `/channel-capacities/{channelCapacityId}` | inline | ChannelCapacity | 409 Capacity reduced below units already sold plus units under an unexpired lease (audit R101) | opens modal first |

**Data it reads**: `listChannelCapacities` (onLoad, List capacity envelopes); `listWaitlistEntries` (onLoad, Guests waiting for capacity)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*
- → `BO-009` Pricing Rules: *Pricing Rules*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The capacity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the capacity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No capacity yet. Offers Create channel capacity (`createChannelCapacity`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on performanceId and the capacity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Allocations exceed the channel capacity in total, or a channel appears twice; 409 An allocation is below what that channel has already sold plus its leased units (audit R101); 409 Capacity reduced below units already sold plus units under an unexpired lease (audit R101) |

#### Permissions

- `listChannelCapacities` → `PRODUCT_VIEW` (read) · staff, partner
- `getChannelAllocations` → `PRODUCT_VIEW` (read) · staff, partner
- `createChannelCapacity` → `CAPACITY_CONFIGURE` (configure) · staff
- `relinquishChannelAllocation` → `CAPACITY_CONFIGURE` (configure) · staff, partner
- `setChannelAllocations` → `CAPACITY_CONFIGURE` (configure) · staff
- `updateChannelCapacity` → `CAPACITY_CONFIGURE` (configure) · staff
- `listWaitlistEntries` → `PRODUCT_VIEW` (read) · staff
- `offerWaitlistCapacity` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listChannelCapacities` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.40 | Capacity Management Visibility | Ticketing Sales | CONTRACTED | `listChannelCapacities` |
| 8.9.2 | System shall display current attendance, occupancy levels, capacity utilization, and crowd distribution across parks, venues, facilities, and attractions. | Unified Operations Dashboard | CONTRACTED | `listChannelCapacities` |
| 1.1.3 | The system should be able to sell time-slot based tickets for attractions. The system should support: - Creation of timeslots for a whole day or for a period - Configuration of capacity for each … | Ticketing Catalogue | CONTRACTED | `createChannelCapacity` |
| 7.3.2 | Allow configure inventory and capacity for parks | F&B POS | CONTRACTED | `createChannelCapacity` |
| 1.1.10 | The system should allow the capacity for all type of ticket to be configurable. Capacity of a ticket can be configurable at multiple levels: 1) Sales Capacity: Allow only a fixed number of tickets to … | Ticketing Catalogue | CONTRACTED | `setChannelAllocations` |
| 1.1.127 | Maximum sellable quantity controls | Ticketing Catalogue | CONTRACTED | `setChannelAllocations` |
| 2.1.1 | The system should have the ability to create as many sales channels as necessary by the system admin. Sales Channels creation should involve capture of all required data such as account assignment … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.1.2 | The system should support the configuration of products, prices, quotas, sales limits and sales schedule for each sales channels. Some sales channels can be configured to be accessible to only … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.1.3 | The system should store and manage all rules for product compatibility, eligibility and pricing that will be applicable to for each sales channel. These rules will be part of the system and not … | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.5 | For BtoB online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.11 | - Only BtoB PLUs | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| 2.7.15 | - Quotas can be applied for one Customer or a category of Customers | Ticketing Sales | CONTRACTED | `setChannelAllocations` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory pools split capacity by ticket type (e.g. 50% GA, 30% child, 20% senior) and/or sales channel (e.g. 50% online, 50% on-site), configurable at venue/event level, under a hierarchy global → attraction → product → variant → time slot. On cancel/refund/reschedule the business chooses whether capacity is released or held. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 4.11 UX Simplification & Distributed Inventory · DI-457)*
- Decision: venue-level admission capacity supersedes event-level capacity; a system prompt/validation prevents configuring or selling an event beyond the remaining venue capacity. Overriding is an authorisation-gated (RBAC) action for authorised users only. *(agreed · MoM 25 Aug 2026, 4.6 Performances & Capacity Management; 5. Key Decisions · DI-456)*
- Two capacity types shown distinctly: sales capacity (tickets sellable per performance) and admission capacity (a real-time, scan-based count of guests inside via entry/exit turnstiles), capping on-site attendance independent of tickets sold. *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-455)*
- AI suggestions from sales forecasts: add/remove time slots, merge under-sold adjacent slots (with guest notification of the time change), and dynamic pricing (raise when a slot is >~80% sold, lower when <~20–30%). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-454)*
- Performances are created individually or from a reusable time-slot template (e.g. every 30 minutes between start and end) that auto-generates the schedule. Capacity set at event level is inherited by performances, with per-performance override (e.g. evening slots). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-453)*
- "Envelopes" split a performance's capacity by channel (e.g. of 100: 30 B2C, 40 B2B, 30 on-site); each channel shows only its own share as available. Configured once and applied to all linked performances. *(agreed · MoM 7 Aug 2026, 15. Capacity Splitting via Envelopes · DI-170)*
- Performance capacity is edited individually or by multi-select bulk edit; a performance can be suspended, resumed (any time before start) or cancelled — a state change, never a delete. *(agreed · MoM 7 Aug 2026, 14. Events, Integrations & Performances (Time Slots) · DI-168)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-017` · status **notStarted** · provenance generated
- ADR-0012 *Queue Integration — Adaptor-First, Vendor Deferred* (`docs/adr/0012-queue-integration-adaptor-first.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create channel capacity, Release channel allocation, Save channel allocations, Save channel capacity.
- [ ] Every transition is wired: `BO-007`, `BO-009`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 7 client meeting input(s) for this screen are applied; open questions are built to their default.
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

### In P08 · Sell

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**32 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"analysePromotionConflicts": {"method":"GET","path":"/promotions/{promotionId}/conflicts","contract":"promotions","summary":"Analyse stacking against live promotions","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConflictAnalysis"},
"assignCoupon": {"method":"POST","path":"/coupon-codes/{code}/assign","contract":"promotions","summary":"Assign a coupon to a named guest","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"bulkChangePrices": {"method":"POST","path":"/products/bulk-price","contract":"catalogue","summary":"Reprice a category or a whole catalogue","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BulkPriceResult"},
"bulkUpdateProducts": {"method":"POST","path":"/products/bulk","contract":"inventory","summary":"Change many products at once, with a preview","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"cancelPerformance": {"method":"POST","path":"/performances/{performanceId}/cancel","contract":"catalogue","summary":"Cancel a performance","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PerformanceCancellationResult"},
"copyPriceList": {"method":"POST","path":"/price-lists/{priceListId}/copy","contract":"catalogue","summary":"Copy a price list, optionally with an adjustment","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createBundle": {"method":"POST","path":"/bundles","contract":"promotions","summary":"Create a bundle","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateBundleRequest","responds":"Bundle"},
"createChannelCapacity": {"method":"POST","path":"/channel-capacities","contract":"catalogue","summary":"Create a channel capacity","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateEnvelopeRequest","responds":"ChannelCapacity"},
"createCombo": {"method":"POST","path":"/combos","contract":"fnb","summary":"A meal deal, priced as one thing","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Combo","responds":"Combo"},
"createCouponCampaign": {"method":"POST","path":"/coupon-campaigns","contract":"promotions","summary":"Create a coupon campaign","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCouponCampaignRequest","responds":"CouponCampaign"},
"createEntitlementTemplate": {"method":"POST","path":"/entitlement-templates","contract":"catalogue","summary":"Create an entitlement template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EntitlementTemplate","responds":"EntitlementTemplate"},
"createEvent": {"method":"POST","path":"/events","contract":"catalogue","summary":"Create an event","permission":"EVENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateEventRequest","responds":"Event"},
"createMerchandise": {"method":"POST","path":"/merchandise","contract":"retail","summary":"Create a merchandise item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateMerchandiseRequest","responds":"MerchandiseItem"},
"createPerformances": {"method":"POST","path":"/events/{eventId}/performances","contract":"catalogue","summary":"Create performances, singly or by schedule","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreatePerformancesRequest","responds":null},
"createPriceList": {"method":"POST","path":"/price-lists","contract":"catalogue","summary":"Create a price list","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreatePriceListRequest","responds":"PriceList"},
"createProduct": {"method":"POST","path":"/products","contract":"catalogue","summary":"Create a product","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreateProductRequest","responds":"Product"},
"createPromotion": {"method":"POST","path":"/promotions","contract":"promotions","summary":"Create a promotion","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePromotionRequest","responds":"Promotion"},
"createVoucherBatch": {"method":"POST","path":"/voucher-batches","contract":"promotions","summary":"Issue a voucher batch","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateVoucherBatchRequest","responds":"VoucherBatch"},
"endPromotion": {"method":"POST","path":"/promotions/{promotionId}/end","contract":"promotions","summary":"End a promotion early","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"evaluatePromotions": {"method":"POST","path":"/promotions/evaluate","contract":"promotions","summary":"Evaluate promotions against a cart","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EvaluatePromotionsRequest","responds":"PromotionEvaluation"},
"generateCouponCodes": {"method":"POST","path":"/coupon-campaigns/{campaignId}/codes","contract":"promotions","summary":"Generate codes in bulk","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getChannelAllocations": {"method":"GET","path":"/channel-capacities/{channelCapacityId}/channel-allocations","contract":"catalogue","summary":"Capacity allocated to each channel","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ChannelAllocationSet"},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getDynamicPriceRule": {"method":"GET","path":"/pricing/dynamic-rules/{ruleId}","contract":"catalogue","summary":"One rule with its conditions and actions","permission":"PRICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"ruleId","in":"path","required":true}],"requestBody":null,"responds":"DynamicPriceRuleDetail"},
"getEvent": {"method":"GET","path":"/events/{eventId}","contract":"catalogue","summary":"Read an event","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Event"},
"getGroupPackageDefinition": {"method":"GET","path":"/products/{productId}/group-package","contract":"catalogue","summary":"A school-trip format or party package","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"productId","in":"path","required":true}],"requestBody":null,"responds":"GroupPackageDefinition"},
"getLatestBundle": {"method":"GET","path":"/catalogue/bundles/latest","contract":"catalogue","summary":"Pull the current bundle for this workstation's venue","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"since","in":"query","required":null},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"CatalogueBundle"},
"getPerformance": {"method":"GET","path":"/performances/{performanceId}","contract":"catalogue","summary":"Read a performance","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Performance"},
"getPriceList": {"method":"GET","path":"/price-lists/{priceListId}","contract":"catalogue","summary":"Read a price list","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PriceList"},
"getProduct": {"method":"GET","path":"/products/{productId}","contract":"catalogue","summary":"Read a product","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Product"},
"getPromotion": {"method":"GET","path":"/promotions/{promotionId}","contract":"promotions","summary":"Read a promotion","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Promotion"},
"getPromotionUsage": {"method":"GET","path":"/promotions/{promotionId}/usage","contract":"promotions","summary":"Redemption count and discount given","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionUsage"},
"getSeatAvailability": {"method":"GET","path":"/performances/{performanceId}/seat-availability","contract":"seating","summary":"Seat status for a performance","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sectionCode","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"availableOnly","in":"query","required":null},{"name":"mode","in":"query","required":null}],"requestBody":null,"responds":"SeatAvailability"},
"listAlternativeCodes": {"method":"GET","path":"/products/{productId}/alternative-codes","contract":"catalogue","summary":"External identifiers for a product","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AlternativeCode"},
"listBookingFlows": {"method":"GET","path":"/venues/{venueId}/booking-flows","contract":"white-label","summary":"A venue's booking flows, in the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"flowTypeKey","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCatalogueBundles": {"method":"GET","path":"/catalogue/bundles","contract":"catalogue","summary":"List published catalogue bundles","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleSummary"},
"listChannelCapacities": {"method":"GET","path":"/channel-capacities","contract":"catalogue","summary":"List channel capacities","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCommercialCampaigns": {"method":"GET","path":"/commercial-campaigns","contract":"promotions","summary":"List commercial campaigns","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":"ownerPrincipalId","in":"query","required":null},{"name":"q","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCouponCampaigns": {"method":"GET","path":"/coupon-campaigns","contract":"promotions","summary":"List coupon campaigns","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCouponCodes": {"method":"GET","path":"/coupon-campaigns/{campaignId}/codes","contract":"promotions","summary":"List generated codes","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"batchId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicPriceRules": {"method":"GET","path":"/pricing/dynamic-rules","contract":"catalogue","summary":"Dynamic pricing rules","permission":"PRICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PricingDynamicPriceRule"},
"listEntitlementTemplates": {"method":"GET","path":"/entitlement-templates","contract":"catalogue","summary":"List entitlement templates","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"EntitlementTemplate"},
"listEvents": {"method":"GET","path":"/events","contract":"catalogue","summary":"List events","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMenus": {"method":"GET","path":"/menus","contract":"fnb","summary":"List menus","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMerchandise": {"method":"GET","path":"/merchandise","contract":"retail","summary":"List merchandise","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"inStockOnly","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPerformanceTemplates": {"method":"GET","path":"/performance-templates","contract":"catalogue","summary":"Slot templates, peak bands and walk-in rules","permission":"PERFORMANCE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PerformanceTemplate"},
"listPerformances": {"method":"GET","path":"/events/{eventId}/performances","contract":"catalogue","summary":"List performances of an event","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"language","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceLists": {"method":"GET","path":"/price-lists","contract":"catalogue","summary":"List price lists","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrices": {"method":"GET","path":"/price-lists/{priceListId}/prices","contract":"catalogue","summary":"List prices in a list","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductVariants": {"method":"GET","path":"/products/{productId}/variants","contract":"catalogue","summary":"List generated variants","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPromotions": {"method":"GET","path":"/promotions","contract":"promotions","summary":"List promotions","permission":"PRICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVoucherBatches": {"method":"GET","path":"/voucher-batches","contract":"promotions","summary":"List voucher batches","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWaitlistEntries": {"method":"GET","path":"/waitlist-entries","contract":"catalogue","summary":"Who is waiting for capacity","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null}],"requestBody":null,"responds":"WaitlistEntry"},
"offerWaitlistCapacity": {"method":"POST","path":"/waitlist-entries/{entryId}/offer","contract":"catalogue","summary":"Tell a waiting guest that capacity appeared","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WaitlistEntry"},
"pausePromotion": {"method":"POST","path":"/promotions/{promotionId}/pause","contract":"promotions","summary":"Pause a live promotion","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"publishBundle": {"method":"POST","path":"/catalogue/bundles","contract":"catalogue","summary":"Compute, sign and publish a catalogue bundle","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"BundleSummary"},
"publishPromotion": {"method":"POST","path":"/promotions/{promotionId}/publish","contract":"promotions","summary":"Publish a promotion","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Promotion"},
"recommendSeats": {"method":"POST","path":"/performances/{performanceId}/seat-recommendations","contract":"seating","summary":"Recommend seats for a party","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatRecommendationRequest","responds":null},
"recordDashboardView": {"method":"POST","path":"/dashboards/{dashboardId}/views","contract":"reporting","summary":"Record that a dashboard was opened","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"relinquishChannelAllocation": {"method":"POST","path":"/channel-capacities/{channelCapacityId}/channel-allocations/release","contract":"catalogue","summary":"Return unsold channel allocation to the general pool","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelAllocationSet"},
"reportBundleApplied": {"method":"POST","path":"/catalogue/bundles/{version}/applied","contract":"catalogue","summary":"Report that a workstation applied a bundle","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"resolveProductByCode": {"method":"GET","path":"/products/resolve","contract":"catalogue","summary":"Resolve a partner code to a product","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"code","in":"query","required":true},{"name":"partnerId","in":"query","required":null}],"requestBody":null,"responds":"ProductVariant"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"setAlternativeCodes": {"method":"PUT","path":"/products/{productId}/alternative-codes","contract":"catalogue","summary":"Set external identifiers","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AlternativeCode"},
"setChannelAllocations": {"method":"PUT","path":"/channel-capacities/{channelCapacityId}/channel-allocations","contract":"catalogue","summary":"Allocate a channel capacity across sales channels","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelAllocationSet"},
"setComboSlots": {"method":"PUT","path":"/combos/{comboId}/slots","contract":"fnb","summary":"What the guest chooses, and what it costs extra","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Combo"},
"setDynamicPriceRule": {"method":"PUT","path":"/pricing/dynamic-rules/{ruleId}","contract":"catalogue","summary":"Replace a rule, its conditions and its actions","permission":"PRICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"ruleId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"DynamicPriceRuleDetail","responds":"DynamicPriceRuleDetail"},
"setGroupPackageDefinition": {"method":"PUT","path":"/products/{productId}/group-package","contract":"catalogue","summary":"Define a school-trip format or party package","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"productId","in":"path","required":true}],"requestBody":"GroupPackageDefinition","responds":"GroupPackageDefinition"},
"setItemAvailability": {"method":"PUT","path":"/menu-items/{itemId}/availability","contract":"fnb","summary":"Mark an item available or eighty-sixed","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuItem"},
"setPackagePricingDefinition": {"method":"PUT","path":"/package-pricing","contract":"catalogue","summary":"Set how a package, bundle or add-on is priced","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PackagePricing","responds":"PackagePricing"},
"setPerformanceTemplate": {"method":"PUT","path":"/performance-templates","contract":"catalogue","summary":"Define slot length, capacity, bands and walk-in policy","permission":"PERFORMANCE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PerformanceTemplate","responds":"PerformanceTemplate"},
"setPrices": {"method":"PUT","path":"/price-lists/{priceListId}/prices","contract":"catalogue","summary":"Set prices in bulk","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setProductAttributes": {"method":"PUT","path":"/products/{productId}/attributes","contract":"catalogue","summary":"Set the attribute axes for a product","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setPromotionVariants": {"method":"PUT","path":"/promotions/{promotionId}/variants","contract":"promotions","summary":"A/B test two versions against each other","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"simulatePromotion": {"method":"POST","path":"/promotions/{promotionId}/simulate","contract":"promotions","summary":"What this promotion would have cost on real history","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"transitionProductLifecycle": {"method":"POST","path":"/products/{productId}/lifecycle","contract":"catalogue","summary":"Move a product through its lifecycle","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Product"},
"unschedulePromotion": {"method":"POST","path":"/promotions/{promotionId}/unschedule","contract":"promotions","summary":"Pull a scheduled promotion before it starts","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateBundle": {"method":"PATCH","path":"/bundles/{bundleId}","contract":"promotions","summary":"Amend a bundle","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Bundle"},
"updateChannelCapacity": {"method":"PATCH","path":"/channel-capacities/{channelCapacityId}","contract":"catalogue","summary":"Amend a channel capacity","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ChannelCapacity"},
"updateEvent": {"method":"PATCH","path":"/events/{eventId}","contract":"catalogue","summary":"Amend an event","permission":"EVENT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Event"},
"updatePerformance": {"method":"PATCH","path":"/performances/{performanceId}","contract":"catalogue","summary":"Amend a performance","permission":"PERFORMANCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Performance"},
"updatePriceList": {"method":"PATCH","path":"/price-lists/{priceListId}","contract":"catalogue","summary":"Amend a price list","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PriceList"},
"updateProduct": {"method":"PATCH","path":"/products/{productId}","contract":"catalogue","summary":"Update a product","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"UpdateProductRequest","responds":"Product"},
"updatePromotion": {"method":"PATCH","path":"/promotions/{promotionId}","contract":"promotions","summary":"Amend a promotion","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Promotion"},
"voidCouponCode": {"method":"POST","path":"/coupon-codes/{code}/void","contract":"promotions","summary":"Void a code","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CouponCode"},
"voidVoucher": {"method":"POST","path":"/vouchers/{voucherId}/void","contract":"promotions","summary":"Cancel a voucher","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Voucher"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AllocationComponent": {"x-ticvai-persistence":"promotions.allocation_component","type":"object","required":["variantId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"variantId":{"type":"string","format":"uuid"},"percentage":{"type":"number","minimum":0,"maximum":100},"fixedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"listPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"For `proRataListPrice` — weights derived from list prices. **The variant's current price when the bundle is created** (decided 28 September, audit R101), then frozen with the allocation."},"revenueAccountId":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"Set where the component is earned by a different legal entity. Cross-currency allocation is deferred pending the FX policy decision.\n"},"venueId":{"type":"string","format":"uuid","nullable":true}}},
"AllocationMethod": {"type":"string","enum":["percentage","fixedAmount","proRataListPrice"]},
"AlternativeCode": {"x-ticvai-persistence":"catalogue.alternative_code","type":"object","required":["code","partnerId"],"properties":{"code":{"type":"string","maxLength":128},"partnerId":{"type":"string","format":"uuid"},"partnerName":{"type":"string"},"variantId":{"type":"string","format":"uuid"},"note":{"type":"string","maxLength":200}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowLevelSettings": {"x-ticvai-persistence":"none — jsonb column on whitelabel.booking_flow","type":"object","description":"**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n","properties":{"performanceReveal":{"type":"string","enum":["dateTimeTicket","allAtOnce"],"default":"dateTimeTicket","description":"**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"},"signInAt":{"type":"string","enum":["afterAddOns","atPayment"],"default":"afterAddOns","description":"**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"},"seatEventDateMode":{"type":"string","enum":["inlineStep","popupOnSeatMap"],"default":"inlineStep","description":"**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"},"extrasStep":{"type":"string","enum":["auto","always","never"],"default":"auto","description":"`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."},"quickTour":{"type":"boolean","default":false,"description":"**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"default":[],"description":"**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n","items":{"type":"string","format":"uuid"}}}},
"BookingFlowStep": {"x-ticvai-persistence":"whitelabel.booking_flow_step","type":"object","description":"One step of a venue's flow, in the venue's order (decided 29 September, W12).","required":["stepKey","enabled","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bookingFlowId":{"type":"string","format":"uuid","readOnly":true},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"enabled":{"type":"boolean","description":"A `required` step cannot be off; the flow saves and `isValid` turns false."},"sortOrder":{"type":"integer","minimum":0},"requirement":{"type":"string","enum":["required","optional","conditional"],"readOnly":true,"x-ticvai-derived":"onRead","description":"From the flow type, so the CMS can mark the step without a second read."},"settings":{"type":"object","additionalProperties":true,"default":{},"description":"The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."}}},
"BookingFlowTypeKey": {"type":"string","description":"**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n","enum":["datedDayPass","timedEntry","openDated","seatedFixedPerformance","seatedDateTimeSeatMap","experienceWorkshop","surfSession","meetingRoomHourly","cabanaMap","cabanaBySize","guidedTourByLanguage","transport","tableReservation","membership","giftCard","multiLocation"]},
"BulkPriceResult": {"type":"object","description":"2.9.9. Dry run or applied — the shape is the same, `applied` says which.","required":["applied","productsMatched"],"properties":{"applied":{"type":"boolean"},"productsMatched":{"type":"integer"},"pricesChanged":{"type":"integer"},"skipped":{"type":"array","description":"**Products the selection matched and the adjustment could not touch** — a fixed-price bundle, a partner net rate, a product in an open period. Named rather than counted, because whoever ran this will be asked why the total is short.\n","items":{"type":"object","properties":{"productId":{"type":"string","format":"uuid"},"reason":{"type":"string"}}}}}},
"Bundle": {"x-ticvai-persistence":"promotions.bundle + promotions.bundle_component","allOf":[{"$ref":"#/components/schemas/CreateBundleRequest"},{"type":"object","required":["id","savingsAmount","isActive","hasBeenSold"],"properties":{"id":{"type":"string","format":"uuid"},"savingsAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum of component list prices less the bundle price."},"savingsPercentage":{"type":"number"},"hasBeenSold":{"type":"boolean","description":"True locks components and allocation against amendment."},"isActive":{"type":"boolean"}}}]},
"BundleChoiceGroup": {"type":"object","x-ticvai-persistence":"promotions.bundle_choice_group + promotions.bundle_choice_option","description":"**Pick n from a set** (3.5.10). The shape a dynamic bundle needs and `BundleComponent` could not express — it names specific variants, which describes a fixed bundle with swaps.\nThe bundle price does not move with the choice (ADR-0019). **The allocation does.**\n","required":["label","choose","options"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"label":{"type":"string","description":"What the guest is asked. \"Choose 3 attractions\"."},"choose":{"type":"integer","minimum":1,"description":"How many options the guest picks."},"allowDuplicates":{"type":"boolean","default":false,"description":"Whether the same option may be picked twice. False for attractions, sometimes true for F&B.\n"},"options":{"type":"array","minItems":2,"description":"The rows of `promotions.bundle_choice_option`, one per option, each keyed to its group. A required array with nowhere to be stored was a group whose choices were lost on write.\n","items":{"type":"object","required":["variantId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","default":1},"isDefault":{"type":"boolean","default":false}}}},"unavailableBehaviour":{"type":"string","enum":["hideOption","hideBundle"],"default":"hideOption","description":"An option that has sold out for the chosen date is **not offered**. Where the group can no longer be satisfied at all, the bundle itself becomes unavailable — **it is never sold with a component that cannot be delivered**, because a substitution the guest did not choose is a complaint at the gate.\n"}}},
"BundleComponent": {"x-ticvai-persistence":"promotions.bundle_component","type":"object","required":["variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"variantId":{"type":"string","format":"uuid"},"componentKind":{"$ref":"#/components/schemas/BundleComponentKind"},"menuItemId":{"type":"string","format":"uuid","nullable":true,"description":"**The F&B menu item a `fnbMenuItem` component entitles the guest to** (decided 29 September, MOB-4): the meal of a *meal combo with admission*. `variantId` is still the catalogue variant the menu item sells (fnb `MenuItem.variantId`), which prices and taxes it; this names what the outlet redeems. Required when `componentKind` is `fnbMenuItem`, else ignored; a menu item that does not sell `variantId` is a `422` on `createBundle`.\n"},"redeemAtOutletIds":{"type":"array","maxItems":20,"items":{"type":"string","format":"uuid"},"description":"Outlets that redeem an `fnbMenuItem` component; empty means any outlet of the component's venue that has the menu item on a live menu (MOB-4)."},"quantity":{"type":"integer","minimum":1},"isOptional":{"type":"boolean","default":false},"substituteVariantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"For dynamic bundles — guest chooses among these."},"substitutionTriggers":{"type":"array","nullable":true,"items":{"type":"string","enum":["soldOut","capacityExhausted","productSuspended","venueClosed","externalApiUnavailable","inventoryBelowThreshold"]},"description":"When a substitute from `substituteVariantIds` may replace this component (Dynamic Component Substitution Engine). Empty: never substituted. (DM5, 29 September: data model for the agreed operations)"},"substitutionPriceEffect":{"type":"string","enum":["samePrice","surcharge","reducedPrice"],"default":"samePrice","description":"What a substitution does to the bundle price. (DM5, 29 September: data model for the agreed operations)"},"substitutionApproval":{"type":"string","enum":["none","customer","operator"],"default":"customer","description":"Who must accept a substitution before it stands. Customer by default, because a substitution the guest did not choose is a complaint at the gate. (DM5, 29 September: data model for the agreed operations)"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Where this component is redeemed. Differs from the selling venue for multi-venue passes, which is why the allocation split exists.\n"}}},
"BundleKind": {"type":"string","enum":["fixed","dynamic","mandatory","optional","promotional"]},
"BundleSummary": {"x-ticvai-persistence":"none — projection over bundle","type":"object","description":"One published catalogue bundle — the signed snapshot terminals pull (ADR-0013). Not `promotions.Bundle`, which is a sellable product made of other products.","required":["version","venueId","publishedAt","publishedBy","contentHash","staleAfter","sizeBytes"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedBy":{"type":"string","format":"uuid"},"contentHash":{"type":"string"},"signatureKeyId":{"type":"string","description":"Key that signed this bundle. A terminal offline across a key rotation needs a grace window, or it cannot verify the next bundle.\n"},"staleAfter":{"type":"string","format":"date-time"},"sizeBytes":{"type":"integer"},"note":{"type":"string"},"appliedByWorkstations":{"type":"integer"}}},
"CampaignBudget": {"x-ticvai-persistence":"promotions.campaign_budget","type":"object","description":"One budget line of a commercial campaign (setCampaignBudgetFinancial): what kind of spend it caps, who funds it, what it covers, and what happens as it is consumed. **Consumed, committed and reserved are not stored**: consumed is the discount given on orders (`orders.discount`, `promotions.promotion.discount_given`), committed and reserved are priced carts not yet paid, all worked out on read so they cannot drift from the orders they summarise. (DM5, 29 September: data model for the agreed operations)","required":["budgetType","amount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"budgetType":{"type":"string","enum":["total","discount","reward","freeProduct"],"description":"The spend this line caps (total campaign, discount, reward or free-product budget)."},"fundingSource":{"type":"string","nullable":true,"enum":["venue","department","marketing","partner"],"description":"Who pays for it; `partner` is a co-funded (e.g. bank or partner-funded) line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scope":{"type":"string","enum":["entireCampaign","promotion","product","channel","partner","customerSegment"],"default":"entireCampaign","description":"What the line covers."},"scopeRef":{"type":"string","nullable":true,"description":"The promotion, product, partner or segment id, or the SalesChannel value, that `scope` names. Null for `entireCampaign`."},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The budget owner."},"costCentre":{"type":"string","maxLength":64,"nullable":true},"department":{"type":"string","maxLength":100,"nullable":true},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"thresholdPolicy":{"$ref":"#/components/schemas/BudgetThresholdPolicy"}}},
"CatalogueBundle": {"x-ticvai-persistence":"catalogue.published_bundle","type":"object","required":["version","venueId","isDelta","signature","signatureKeyId","contentHash","staleAfter","payload"],"properties":{"version":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"isDelta":{"type":"boolean"},"baseVersion":{"type":"string","nullable":true,"description":"Present when `isDelta`. The version this delta applies to."},"signature":{"type":"string","description":"Detached signature over `contentHash`. The terminal verifies before applying and rolls back on failure — a half-applied catalogue is never traded against.\n"},"signatureKeyId":{"type":"string"},"contentHash":{"type":"string"},"staleAfter":{"type":"string","format":"date-time"},"payload":{"type":"object","description":"Products, variants, price lists, prices, tax codes, events, performances, envelope definitions, data mask field definitions and the venue's sale boards. Shape is versioned with the bundle format, not with this API.\n","additionalProperties":true,"properties":{"saleBoards":{"type":"array","description":"**The venue's sale boards as `tenancy.listSaleBoards` returns them**, read from `platform.sale_board` when the bundle is snapshotted (decided 28 September, audit R129 (4)). A board changed by `updateSaleBoard` reaches terminals here, with the next bundle, and never mid-transaction.\n","items":{"type":"object","additionalProperties":true}}}}}},
"CatalogueConfigStatus": {"type":"string","enum":["draft","active","inactive","retired"],"description":"**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ChannelAllocation": {"x-ticvai-persistence":"catalogue.channel_allocation","type":"object","required":["channel","allocatedUnits"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"channel":{"$ref":"#/components/schemas/Channel"},"allocatedUnits":{"type":"integer","minimum":0},"soldUnits":{"type":"integer","readOnly":true},"leasedUnits":{"type":"integer","readOnly":true,"description":"Held by terminals on this channel but not yet sold."},"remainingUnits":{"type":"integer","readOnly":true},"releaseAt":{"type":"string","format":"date-time","nullable":true,"description":"Unsold units return to the general pool at this time. How distribution holds are freed close to a performance without someone remembering to do it.\n"},"salesChannelId":{"type":"string","format":"uuid","nullable":true,"description":"The channel profile (`catalogue.sales_channel`) this allocation serves (29 September, data model DM3)."},"allocationType":{"type":"string","enum":["sharedPool","dedicated","percentage","dynamic"],"default":"dedicated","description":"How the allocation is sized (29 September, data model DM3); the allocation rule of ADM-262 lives on this row."},"minimumUnits":{"type":"integer","nullable":true,"minimum":0},"maximumUnits":{"type":"integer","nullable":true,"minimum":0},"replenishmentRule":{"type":"object","additionalProperties":true,"nullable":true,"description":"`{sourceChannelId, trigger, thresholdUnits, sharePercent, units}`."},"waitlistBehavior":{"type":"string","enum":["none","joinWaitlist","notifyOnRelease"],"default":"none"},"releaseThresholdUnits":{"type":"integer","nullable":true,"minimum":0},"releaseHoursBeforeEvent":{"type":"integer","nullable":true,"minimum":0,"description":"Alternative to `releaseAt`, relative to the performance start."},"contractualUnits":{"type":"integer","nullable":true,"minimum":0,"description":"Units a partner agreement guarantees; rebalancing never goes below it."},"minimumGuaranteedUnits":{"type":"integer","nullable":true,"minimum":0},"isFrozen":{"type":"boolean","default":false,"description":"Excluded from rebalancing."}}},
"ChannelAllocationSet": {"x-ticvai-persistence":"none — projection","type":"object","required":["channelCapacityId","capacity","allocations","generalPoolUnits"],"properties":{"channelCapacityId":{"type":"string","format":"uuid"},"capacity":{"type":"integer"},"allocations":{"type":"array","items":{"$ref":"#/components/schemas/ChannelAllocation"}},"generalPoolUnits":{"type":"integer","description":"Unallocated remainder. Any channel may draw from it once its own allocation is exhausted.\n"},"totalSold":{"type":"integer"},"totalRemaining":{"type":"integer"}}},
"ChannelCapacity": {"x-ticvai-persistence":"catalogue.channel_capacity","type":"object","required":["id","performanceId","capacity","sold","leased","remaining","isSeated"],"properties":{"id":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"name":{"type":"string"},"seatCategoryId":{"type":"string","format":"uuid","nullable":true},"oversellAllowance":{"type":"integer","default":0,"description":"BL-046, 1.3.13. **The guard existed in one direction** — an envelope could be raised freely and refused reduction below what had sold.\n**Free events oversell deliberately because no-show rates are known.** An allowance on the envelope rather than an admission policy, because **the gate must still refuse when actual capacity is reached** — overselling is a sales decision and admission is a safety one, and they must not share a number.\n"},"oversellBasis":{"type":"string","nullable":true,"enum":["fixedCount","historicNoShowRate","percentage"]},"capacity":{"type":"integer","minimum":0},"sold":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Units sold. **Maintained on write** (decided 29 September, SD-023): raised by `convertInventoryHold` in the order transaction and by consumption a workstation reports on `renewInventoryHold` or `relinquishInventoryHold`, lowered when a refund or cancellation returns the units. Always `capacity + oversellAllowance = sold + leased + remaining`.\n"},"leased":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Units in `active` holds, not yet sold. Raised at acquire, lowered at conversion, release, force-release and expiry (SD-023)."},"remaining":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"What can still be held. **Decremented at the hold with a guarded statement** (`remaining >= n`) under the row lock, never at the sale, so two buyers cannot both take the last unit (SD-023, 29 September).\n"},"hasChannelAllocations":{"type":"boolean","description":"True where capacity is divided across channels. Leases then draw from a channel allocation rather than from raw capacity.\n"},"isSeated":{"type":"boolean","description":"Seated envelopes cannot be leased and are blocked offline. A seat map is not a count.\n"}}},
"Combo": {"type":"object","x-ticvai-persistence":"fnb.combo","description":"Board 2G, 24 August. **A meal deal is one product with slots, not a bundle of products.** `listCatalogueBundles` bundles ticketing products — a ticket and a parking pass, both fixed — and **a burger with a choice of side and a choice of drink is a different shape entirely.**\n**The price is on the combo, not the sum of its parts.** That is the whole commercial point: a meal deal is cheaper than its items, and a model that prices by summing cannot express it.\n**Upcharges live on the slot options.** A large drink in a meal deal costs two dirhams more than a regular, and it is not a separate combo.\n","required":["id","name","price","slots"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"name":{"type":"string"},"nameLocalised":{"type":"object","additionalProperties":{"type":"string"}},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"slots":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ComboSlot"}},"availability":{"allOf":[{"$ref":"#/components/schemas/MenuAvailability"}],"nullable":true,"description":"Service periods it sells in, in the same shape as a menu's. **A lunch deal at 9pm is a margin leak** and the venue only notices at month end.\n"},"isActive":{"type":"boolean","default":true}}},
"ComboSlot": {"type":"object","x-ticvai-persistence":"fnb.combo_slot","description":"One choice within a combo. **`minSelect` and `maxSelect` are what make it a slot rather than a line** — a main is exactly one, a side is one of four, and a sauce might be none or two.\n","required":["id","name","options"],"properties":{"id":{"type":"string","format":"uuid"},"comboId":{"type":"string","format":"uuid"},"name":{"type":"string"},"minSelect":{"type":"integer","default":1},"maxSelect":{"type":"integer","default":1},"sortOrder":{"type":"integer","default":100},"options":{"type":"array","items":{"type":"object","required":["menuItemId"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"upcharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isDefault":{"type":"boolean","default":false,"description":"**The one a cashier gets without asking.** A combo with no default is four taps at every till in the venue.\n"}}}}}},
"CommercialCampaign": {"x-ticvai-persistence":"promotions.campaign + promotions.campaign_budget","type":"object","description":"A commercial campaign: the grouping of promotions, coupon campaigns and bundles that share an owner, a business entity, dates and a budget. **Not `marketing.campaign`**, which is the CRM send campaign in another service. The header is saved with its budget lines by setCampaignBudgetFinancial (the budget screen is where the pack captures campaign, owner, business entity and effective dates), and on its own by createCommercialCampaign and updateCommercialCampaign; listCommercialCampaigns lists it (decided 29 September, writers pass); promotions, coupon campaigns and bundles point at it by `campaignId`. No status of its own: a campaign is live while its promotions are, and a threshold action that stops it pauses them. (DM5, 29 September: data model for the agreed operations)","required":["id","venueId","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64,"nullable":true},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The campaign (and budget) owner."},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The business entity that funds and books the campaign."},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"budgets":{"type":"array","description":"The rows of `promotions.campaign_budget`, one per budget line.","items":{"$ref":"#/components/schemas/CampaignBudget"}}}},
"ConflictAnalysis": {"x-ticvai-persistence":"none — computed","type":"object","required":["promotionId","conflicts","worstCaseDiscount"],"properties":{"promotionId":{"type":"string","format":"uuid"},"conflicts":{"type":"array","items":{"type":"object","required":["otherPromotionId","otherPromotionCode","overlap","combinedDiscount"],"properties":{"otherPromotionId":{"type":"string","format":"uuid"},"otherPromotionCode":{"type":"string"},"overlap":{"type":"string","enum":["products","period","channel","full"]},"combinedDiscount":{"type":"number","description":"Combined percentage where both apply to the same line."},"isBlocking":{"type":"boolean","description":"True where the combination would produce a line price of zero or below (decided 28 September, audit R101)."},"isNearZero":{"type":"boolean","description":"True where the combination leaves a net line price above zero but below the venue setting `promotions.nearZeroLinePrice` (proposed AED 1.00; decided 28 September, audit R096 (5)). A warning, not a refusal."}}}},"worstCaseDiscount":{"type":"number","description":"Largest combined discount any single line could receive."}}},
"CouponCampaign": {"x-ticvai-persistence":"promotions.coupon_campaign","allOf":[{"$ref":"#/components/schemas/CreateCouponCampaignRequest"},{"type":"object","required":["id","generatedCount","redeemedCount"],"properties":{"id":{"type":"string","format":"uuid"},"generatedCount":{"type":"integer"},"redeemedCount":{"type":"integer"},"isActive":{"type":"boolean"}}}]},
"CouponCode": {"x-ticvai-persistence":"promotions.coupon_code","type":"object","required":["code","campaignId","status"],"properties":{"code":{"type":"string"},"campaignId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"description":"The `generateCouponCodes` batch that issued this code. Null where no batch did."},"status":{"$ref":"#/components/schemas/CouponStatus"},"assignedSubjectId":{"type":"string","format":"uuid","nullable":true},"redemptionCount":{"type":"integer"},"maxRedemptions":{"type":"integer"},"discount":{"$ref":"#/components/schemas/Discount"},"invalidReason":{"type":"string","nullable":true,"description":"Why the code cannot be applied. A cashier reading `expired` to a guest is a very different conversation from reading `already used`.\n","enum":["expired","alreadyRedeemed","voided","notYetValid","wrongVenue","conditionsNotMet","notAssignedToGuest"]},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"redeemedOrderId":{"type":"string","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"CouponStatus": {"type":"string","enum":["issued","assigned","redeemed","expired","voided"]},
"CreateBundleRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","kind","price","components","allocation"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/BundleKind"},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"components":{"type":"array","minItems":0,"items":{"$ref":"#/components/schemas/BundleComponent"}},"choiceGroups":{"type":"array","description":"Dynamic bundles (3.5.10). A bundle may carry fixed components and choice groups at once — a family pass with fixed parking and two groups the guest chooses from. **The bundle price does not move with the choice** (ADR-0019).\n","items":{"$ref":"#/components/schemas/BundleChoiceGroup"}},"allocation":{"type":"object","required":["method","components"],"properties":{"method":{"allOf":[{"$ref":"#/components/schemas/AllocationMethod"}],"default":"proRataListPrice","description":"Proportional to list price by default. The rounding remainder in the currency's minor unit goes to the first component (decided 28 September, audit R101).\n"},"components":{"type":"array","items":{"$ref":"#/components/schemas/AllocationComponent"}}}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"campaignId":{"type":"string","format":"uuid","nullable":true,"description":"The commercial campaign (`promotions.campaign`) the bundle is sold under. (DM5, 29 September: data model for the agreed operations)"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The bundle owner (Bundle Definition & Setup). (DM5, 29 September: data model for the agreed operations)"},"category":{"type":"string","maxLength":100,"nullable":true,"description":"The bundle category the setup screen files it under. (DM5, 29 September: data model for the agreed operations)"},"isStandaloneProduct":{"type":"boolean","default":true,"description":"Whether the bundle appears as a product in its own right, or only as an offer on another product. (DM5, 29 September: data model for the agreed operations)"},"isRecommendedAtCheckout":{"type":"boolean","default":false,"description":"Whether checkout recommends the bundle. (DM5, 29 September: data model for the agreed operations)"},"requiredVariantIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"Products that must already be in the basket for the bundle to be sold (the setup screen's \"requires another product\"). (DM5, 29 September: data model for the agreed operations)"}}},
"CreateCouponCampaignRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","discount","validFrom"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"isSingleUse":{"type":"boolean","default":true,"description":"True generates individually redeemable codes. False issues one shared code with a redemption limit.\n"},"maxRedemptionsPerCode":{"type":"integer","default":1},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"campaignId":{"type":"string","format":"uuid","nullable":true,"description":"The commercial campaign (`promotions.campaign`) the codes are issued under, as the Coupon & Promo Code Builder names it. (DM5, 29 September: data model for the agreed operations)"}}},
"CreateEnvelopeRequest": {"type":"object","description":"The body of `createChannelCapacity`. **Named before the 26 August rename** (envelope to `ChannelCapacity`); the name stays because generated code is keyed on it.","required":["performanceId","name","capacity"],"properties":{"performanceId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"seatCategoryId":{"type":"string","format":"uuid"},"capacity":{"type":"integer","minimum":0}}},
"CreateEventRequest": {"type":"object","required":["code","name","venueId"],"properties":{"code":{"type":"string","maxLength":64,"x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A code already used by any event in the tenant is refused with `409 duplicate-code`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"parentEventId":{"type":"string","format":"uuid"}}},
"CreateMerchandiseRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["sku","name","outletId","variantId"],"properties":{"sku":{"type":"string","maxLength":64},"barcode":{"type":"string","maxLength":128},"name":{"type":"string","maxLength":200},"description":{"type":"string","description":"What the item is, in the guest's words. Indexed for guest-app search."},"outletId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"inventoryItemId":{"type":"string","format":"uuid"},"isReturnable":{"type":"boolean","default":true},"returnWindowDays":{"type":"integer"},"requiresSerialNumber":{"type":"boolean","default":false},"imageAssetRef":{"type":"string"}}},
"CreatePerformancesRequest": {"type":"object","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"admissionRulesId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"As `Performance.language`; every performance of a generated series takes it (decided 29 September, rev 3 REV3-17)."},"format":{"type":"string","nullable":true,"maxLength":40,"description":"As `Performance.format` (decided 29 September, rev 3 REV3-17)."},"recurrence":{"type":"object","description":"Generate a series rather than a single performance. **Read in the region's time zone**: the Region owns the zone and every venue inherits it without override (tenancy), so `daysOfWeek` are the region's calendar days and `until` is compared on the region's clock.\n","properties":{"intervalMinutes":{"type":"integer","minimum":1},"until":{"type":"string","format":"date-time"},"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}}}}}},
"CreatePriceListRequest": {"type":"object","required":["code","name","venueId","channels"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"channels":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/Channel"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"priority":{"type":"integer","default":0}}},
"CreateProductRequest": {"type":"object","required":["code","name","kind","venueId"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A code already used by any product in the tenant, at any venue, is refused with `409 duplicate-code`.\n"},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. At most one product per venue in a family, else `409 duplicate-code`."},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid"},"dataMaskValues":{"type":"object","additionalProperties":true},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"See `Product.salesContact` (W3, 29 September)."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"See `Product.bookingFlowId` (W8, W12, 29 September)."},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"}},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"}},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"}},"requiresTimeWindow":{"type":"boolean"}}},
"CreatePromotionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","discount","validFrom"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$"},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"stackingMode":{"allOf":[{"$ref":"#/components/schemas/StackingMode"}],"default":"bestOnly"},"stackingGroup":{"type":"string","maxLength":64},"precedence":{"type":"integer","default":0,"description":"Higher evaluates first where several could apply."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"maxRedemptions":{"type":"integer","nullable":true},"maxRedemptionsPerGuest":{"type":"integer","nullable":true},"budgetCap":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Total discount value after which the promotion stops automatically. **Enforced at checkout**, where an order whose discount would take the total past the cap does not receive the promotion (decided 28 September, audit R101)."},"campaignId":{"type":"string","format":"uuid","nullable":true,"description":"The commercial campaign (`promotions.campaign`) this promotion belongs to; null for a promotion run on its own. The directory, calendar and campaign budget screens group by it. (DM5, 29 September: data model for the agreed operations)"},"recommendable":{"type":"boolean","default":false,"description":"**May the recommendation engine show this offer to a guest** (8.6.30 to 8.6.36; 29 September, build pass, group G2, from group G1's handoff). False keeps a promotion to the basket, where `evaluatePromotions` applies it as before. True makes a live promotion a candidate item of kind `offer` in `ai.decideRecommendations` for the guests its conditions and `recommendableSegmentIds` admit: while it is live, `promotions.recommendationStrategyPublished` (kind `offers`) keeps the engine's candidate cache current, and it leaves the cache when it is paused, ends or expires. **The engine shows the offer; the discount is still computed here at the basket**, never by ai."},"recommendableSegmentIds":{"type":"array","nullable":true,"description":"The marketing-crm segments the offer may be recommended to; null means every guest its own conditions admit.","items":{"type":"string","format":"uuid"}}}},
"CreateVoucherBatchRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","venueId","faceValue","quantity","validTo"],"properties":{"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"faceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"quantity":{"type":"integer","minimum":1,"maximum":50000},"allowPartialRedemption":{"type":"boolean","default":true,"description":"False forfeits any unused balance, which is then recognised as breakage.\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"restrictToVariantIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"Discount": {"x-ticvai-persistence":"none — embedded in promotion","type":"object","required":["kind"],"properties":{"kind":{"$ref":"#/components/schemas/DiscountKind"},"percentage":{"type":"number","minimum":0,"maximum":100},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fixedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"buyQuantity":{"type":"integer","minimum":1},"getQuantity":{"type":"integer","minimum":1},"getDiscountPercentage":{"type":"number","minimum":0,"maximum":100,"description":"100 makes the free items actually free; lower values give a partial discount."},"tiers":{"type":"array","description":"For `tieredPercentage` — more units, larger discount.","items":{"type":"object","required":["minQuantity","percentage"],"properties":{"minQuantity":{"type":"integer","minimum":1},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"maxDiscountAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Cap on a percentage discount. Prevents an unbounded discount on a large basket."},"rewardVariantIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"The reward products, where the reward is not the qualifying product: the free gift of `freeItem`, the \"different product\" of a `buyXGetY` (setGiftFreeProduct, setBuyGetBogo). Absent means the reward is taken from the qualifying lines. (DM5, 29 September: data model for the agreed operations)"},"maxApplicationsPerBasket":{"type":"integer","minimum":1,"nullable":true,"description":"How many times the offer repeats in one basket: the \"maximum repetitions\" of an N-for-X offer (setFixedPriceOffer). Null repeats for every complete set. (DM5, 29 September: data model for the agreed operations)"}}},
"DiscountKind": {"type":"string","enum":["percentage","fixedAmount","fixedPrice","buyXGetY","freeItem","tieredPercentage"]},
"DynamicPriceRuleDetail": {"type":"object","x-ticvai-persistence":"none — composed from a rule, its conditions and its actions","description":"**A rule is unreadable without both halves.** The conditions say when it fires, the actions say what it does to the price, and `minPrice`/`maxPrice` on the action are the guard rails a reviewer looks for first.\n","required":["rule"],"properties":{"rule":{"$ref":"#/components/schemas/PricingDynamicPriceRule"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/PricingDynamicPriceCondition"}},"actions":{"type":"array","items":{"$ref":"#/components/schemas/PricingDynamicPriceAction"}}}},
"EntitlementTemplate": {"x-ticvai-persistence":"catalogue.entitlement_template","type":"object","required":["id","code","name","validityKind"],"properties":{"description":{"type":"string","description":"**Validity, re-entry and transfer rules in prose.** \"Can I leave and come back\" is answered from here, and a name cannot answer it.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on create; `createEntitlementTemplate` does not take it."},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"validityKind":{"type":"string","enum":["singleUse","dated","dateRange","rolling","unlimited","countLimited"]},"validFromOffsetDays":{"type":"integer","nullable":true},"validForDays":{"type":"integer","nullable":true},"daysOfWeek":{"type":"array","nullable":true,"description":"1.1.7 and 1.1.82. **A camp ticket admits on Tuesdays and Thursdays for six weeks**, and `validityKind` had six values with no day pattern among them.\nThe shape is settled elsewhere in the package — `fnb.MenuAvailability` and `promotions.PromotionConditions` both carry it. **Null means every day**, which is what every existing entitlement means today.\n","items":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]}},"expiryAnchor":{"type":"string","nullable":true,"enum":["offsetDays","endOfMonth","endOfQuarter","endOfYear","fixedDate","seasonEnd"],"description":"1.1.90 to 1.1.92. **A pass bought on the 20th and expiring on the 31st cannot be expressed by an offset in days.** `offsetDays` is the existing behaviour and stays the default.\n`seasonEnd` anchors to the venue's own season rather than the calendar — a water park closing in October is not a quarter boundary.\n"},"expiryDate":{"type":"string","format":"date","nullable":true,"description":"Where `expiryAnchor` is `fixedDate`. Every pass expires the same day regardless of purchase."},"expiryNoticeDays":{"type":"integer","minimum":1,"maximum":180,"nullable":true,"description":"**How many days before `validTo` access raises `entitlement.expiringSoon`** for an entitlement of this template still `issued` or `partiallyConsumed` (29 September, build pass, group G2; 5.5.30). What a pre-expiry message or campaign is triggered by. Null, the default, means no notice: a day ticket needs none, an annual pass might want 30. An entitlement bought inside its own notice period raises nothing."},"carriesStoredValue":{"type":"boolean","default":false,"description":"BL-033. **A ticket that is also a wallet** — a resort pass with 200 dirhams of spend on it, deducted at a gate or a till.\n**The value is a `retail.Wallet` bound to the entitlement, not a balance on the ticket.** One balance mechanism (CF-126), so it holds authorisations, expires by credit type and appears in the same reports — a second balance on the entitlement would have been the seventh implementation.\n"},"includedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"validTimeWindows":{"type":"array","nullable":true,"description":"BL-036, 1.1.81 and 1.1.83. **A time-window entitlement needed a performance to express** — valid 09:00 to 13:00 on any day was a thing you built by creating performances.\n**A window is a property of the entitlement and a performance is an occurrence**, and conflating them means a morning pass generates 365 performances a year.\n","items":{"type":"object","properties":{"from":{"type":"string"},"to":{"type":"string"},"daysOfWeek":{"type":"array","items":{"type":"string"}}}}},"blackoutDates":{"type":"array","nullable":true,"description":"**Calendar exceptions on the entitlement.** An annual pass excluding public holidays is the normal case and had nowhere to live.\n","items":{"type":"string","format":"date"}},"fastTrackTier":{"type":"string","nullable":true,"enum":["none","priority","express","unlimited"],"description":"19.2.20, BL-015. **Fast track existed nowhere in the package** — not an enum value, not a description, not a screen.\n**An attribute of the entitlement rather than a queue class or a product kind**, because the same ride serves standby and fast-track guests from one capacity: `queue` already has `isFastPass` on an entry and needed something to read it from.\n"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited. The Fast Pass consumption counter lives here."},"transportRestriction":{"type":"object","nullable":true,"description":"**The journey a transport pass is good for** (decided 29 September, rev 3 REV3-21). Set on the template `transport.createTransportPassType` creates, from the station pair the guest bought the pass for, and copied to the entitlement. `access` refuses a boarding scan whose departure does not serve both stations in a direction the restriction allows, and consumes one of `entriesAllowed` per boarding. Null on every other template.\n","required":["fromStationId","toStationId"],"properties":{"fromStationId":{"type":"string","format":"uuid","description":"A `transport.Station`."},"toStationId":{"type":"string","format":"uuid"},"bothDirections":{"type":"boolean","default":true,"description":"Valid from either station to the other, as the prototype sells it."},"routeIds":{"type":"array","description":"The routes it may be used on. Empty means any active route serving both stations.","items":{"type":"string","format":"uuid"}}}},"reentryAllowed":{"type":"boolean","default":false},"purchaseEligibility":{"type":"object","nullable":true,"description":"1.1.38, 1.1.121, 1.1.125, 1.1.126. **`admissionRulesId` governs where an entitlement admits, not who may buy it**, and `promotions.evaluatePromotions` gates a discount rather than a sale. Neither refuses a purchase.\n**Evaluated at add-to-cart, not at checkout.** A guest told at payment that they cannot buy a resident rate has already entered a card.\n","properties":{"minAgeYears":{"type":"integer","nullable":true},"maxAgeYears":{"type":"integer","nullable":true},"minHeightCm":{"type":"integer","nullable":true,"description":"**Height gates a ride and can gate a sale.** A ticket sold to somebody who cannot ride it is a refund at the gate.\n"},"residencyRequired":{"type":"boolean","default":false},"nationalities":{"type":"array","nullable":true,"items":{"type":"string"}},"minLoyaltyTier":{"type":"string","nullable":true},"requiresVerification":{"type":"boolean","default":false,"description":"**Whether the claim is checked or taken on trust.** A resident rate sold unverified and refused at the gate is worse than one that could not be bought.\n"}}},"personType":{"type":"string","nullable":true,"enum":["adult","child","infant","senior","student","resident","staff"],"description":"2.11.7. **Adult, child and senior existed only as `ProductVariant.axisValues` — a variant axis rather than an attribute of the holder.** So changing a child ticket to an adult one was an exchange to a different product, and an upgrade that should be a price difference became a cancel-and-rebuy.\nRecorded here as well as on the variant, because **the guest ages and the product does not.**\n"},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"isTransferable":{"type":"boolean","default":true},"canShareMedia":{"type":"boolean","default":true,"description":"Whether this entitlement may be appended to media a guest already holds (CF-58). False for anything surrendered at use — a single-entry ticket taken at the gate is not a claim token for a locker bought afterwards.\n"},"canClaimShopAndDrop":{"type":"boolean","default":false,"description":"Whether this entitlement may be scanned to claim goods left under 4.4.7. False for a single-entry ticket that is surrendered at the gate — a claim token the guest no longer holds is not a claim token.\n"},"isNameBound":{"type":"boolean","default":false,"description":"True requires a holder name at sale. Most entitlements carry none — identity and entitlement are separate concerns.\n"},"autoRenewDefault":{"type":"boolean","default":false,"description":"**Taken from their `membership_plan`, 20 September — the \"take those\" half of the TAKE BODY verdict.** `identity.customer_membership.auto_renew` carries the flag per holder and nothing said what it should start as.\n"},"renewalTermDays":{"type":"integer","nullable":true,"description":"What a renewal extends the membership by. `orders.membership_renewal` records `previousExpiryAt` and `newExpiryAt` and **the number between them lived nowhere**.\n"},"renewalGraceDays":{"type":"integer","default":0,"description":"How long after expiry a membership can still be renewed rather than rejoined. `membership_renewal.failureReason` implies a window and there was none, so a failed card on the expiry date had no defined consequence.\n"},"renewalVariantId":{"type":"string","format":"uuid","nullable":true,"description":"**What a renewal sells, which is usually not what joining sold.** A first-year price and a renewal price are different products, and pointing both at one variant makes a loyalty discount unrepresentable. Null means renewal sells the same thing.\n"},"crossesCells":{"type":"boolean","default":false,"description":"True propagates a redemption right to other cells on issue (ADR-0010).\n"},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.** Set by the server, never taken from a body."}}},
"EvaluatePromotionsRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["venueId","channel","lines"],"properties":{"venueId":{"type":"string","format":"uuid"},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"description":"Where the sale is being made. Matched against `PromotionConditions.channels`, so both sides use the one shared vocabulary.\n"},"subjectId":{"type":"string","format":"uuid"},"membershipTierId":{"type":"string","format":"uuid"},"couponCodes":{"type":"array","items":{"type":"string"}},"evaluateAt":{"type":"string","format":"date-time","description":"For back-office testing of a rule before publishing."},"orderId":{"type":"string","format":"uuid","nullable":true,"description":"The order (`orders.sales_order`) being priced for payment. Sent only by the order service when it confirms an order; when present the evaluation writes one `promotions.promotion_evaluation_trace` row for it. (decided 29 September, writers pass)"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["lineId","variantId","quantity","unitPrice"],"properties":{"lineId":{"type":"string"},"variantId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"Event": {"x-ticvai-persistence":"catalogue.event","type":"object","required":["id","code","name","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentEventId":{"type":"string","format":"uuid","nullable":true,"description":"For grouped events."},"performanceCount":{"type":"integer","readOnly":true,"description":"How many performances the event has. Counted by the server; never sent by a client."},"isActive":{"type":"boolean"}}},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"GroupPackageDefinition": {"type":"object","x-ticvai-persistence":"catalogue.group_package","required":["kind","maxParticipants","durationMinutes"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"productId":{"type":"string","readOnly":true},"kind":{"type":"string","enum":["school","party"]},"maxParticipants":{"type":"integer","minimum":1,"description":"Pupils or children, e.g. 30 or 10."},"durationMinutes":{"type":"integer","minimum":15},"hostCount":{"type":"integer","minimum":0,"default":1,"description":"Party hosts included."},"pricingBasis":{"type":"string","enum":["perParticipant","perPackage"]},"freeLeaderRatio":{"type":"integer","nullable":true,"default":10,"description":"Schools: one teacher or assistant enters free per this many pupils."},"paymentMode":{"type":"string","enum":["invoice","deposit","full"],"description":"Schools are invoiced; parties take a deposit (see `DepositPolicy`)."},"includes":{"type":"array","items":{"type":"string","maxLength":120}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuestMerchandiseItem": {"x-ticvai-persistence":"none — guest projection of MerchandiseItem","type":"object","description":"**What a guest caller of `listMerchandise` receives.** The fields a shop screen shows and the ids a guest needs to reserve or buy, and nothing else: no inventory link, no catalogue variant, no stock count, no serial-number flag. `additionalProperties: false` is the guarantee: a staff field added to `MerchandiseItem` does not reach a guest by default.\n","additionalProperties":false,"required":["id","name","outletId","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"sku":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"outletId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isAvailable":{"type":"boolean","description":"True when the item is active and in stock at its outlet. An item with no `inventoryItemId` never runs out, so it is available while active.\n"},"isReturnable":{"type":"boolean"},"returnWindowDays":{"type":"integer","nullable":true},"imageAssetRef":{"type":"string","nullable":true}}},
"GuestPromotion": {"x-ticvai-persistence":"none — guest projection of promotions.promotion","type":"object","description":"**What a guest may see of a promotion.** `Promotion` carries the commercial internals (`budgetCap`, `maxRedemptions`, `redemptionCount`, `discountGiven`, `precedence`, `stackingGroup`), and `listPromotions` and `getPromotion` are guest-audience. A guest caller receives this shape instead. `additionalProperties: false` is the point: a server that adds an internal field to it fails validation instead of publishing the field.\n","additionalProperties":false,"required":["id","code","name","discount","validFrom"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string"},"discount":{"$ref":"#/components/schemas/Discount"},"conditions":{"$ref":"#/components/schemas/PromotionConditions"},"stackingMode":{"$ref":"#/components/schemas/StackingMode"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"maxRedemptionsPerGuest":{"type":"integer","nullable":true}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Menu": {"x-ticvai-persistence":"fnb.menu","type":"object","required":["id","code","name","outletId","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/MenuSection"}},"isActive":{"type":"boolean"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` live now. Null for a menu never published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"MenuAvailability": {"x-ticvai-persistence":"none — embedded in menu","type":"object","description":"When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.","properties":{"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"validFrom":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."},"validTo":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"The catalogue variant this item sells. Pricing and tax come from there — a menu is a presentation of the catalogue, not a second catalogue.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"MenuSection": {"x-ticvai-persistence":"fnb.menu_section","type":"object","required":["code","name","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string"},"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","description":"The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.","items":{"$ref":"#/components/schemas/MenuItem"}}}},
"MerchandiseItem": {"x-ticvai-persistence":"retail.merchandise","type":"object","required":["id","sku","name","outletId","variantId","price","onHand","isActive"],"properties":{"description":{"type":"string","description":"What the item is, in the guest's words. Indexed for guest-app search.\n"},"id":{"type":"string","format":"uuid"},"sku":{"type":"string"},"barcode":{"type":"string","nullable":true},"name":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true},"variantId":{"type":"string","format":"uuid","description":"The catalogue variant sold. Price and tax come from there."},"inventoryItemId":{"type":"string","format":"uuid","nullable":true,"description":"The stock item depleted on sale. Null means the item sells but never runs out, which is almost always a configuration error.\n"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"list_price"},"onHand":{"type":"number"},"isReturnable":{"type":"boolean","default":true},"returnWindowDays":{"type":"integer","nullable":true},"requiresSerialNumber":{"type":"boolean","default":false},"imageAssetRef":{"type":"string","nullable":true},"isActive":{"type":"boolean"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"PackagePricing": {"type":"object","x-ticvai-persistence":"catalogue.package_pricing","description":"**How a package, bundle or add-on is priced from its components** (29 September, data model DM3). ADM-062. The bundle's composition for sale stays `catalogue.published_bundle`; this row is its pricing model. `normalTotal` and `packageSaving` are computed on read from the component rates.","required":["id","scopePath","productId","recordKind","pricingModel","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"productId":{"type":"string","format":"uuid"},"recordKind":{"type":"string","enum":["package","bundle","addOn"]},"name":{"type":"string","maxLength":200,"nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"pricingModel":{"type":"string","enum":["fixedPackagePrice","sumOfComponents","discountedComponentSum","componentOverride"]},"addOnType":{"type":"string","enum":["fastTrack","parking","meal","photo","equipment","upgrade","additionalPerformance","premiumAccess","other",null],"nullable":true},"packagePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"components":{"type":"object","additionalProperties":true,"description":"`[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`."},"componentPriceVisibility":{"type":"string","enum":["packageTotalOnly","individualComponents","componentAndSaving"],"default":"packageTotalOnly"},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Performance": {"x-ticvai-persistence":"catalogue.performance","type":"object","required":["id","eventId","startsAt","endsAt","status"],"properties":{"id":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"BL-048. **The approval chain and the occurrence lifecycle sat on different entities**, so neither was complete: `states/performance.yaml` models scheduled, onSale, soldOut, suspended, cancelled and completed properly, and nothing said which of those transitions somebody had to sign.\n**Set on the transition that needs it, not on the performance.** Publishing a performance is routine; cancelling one that has sold is the act somebody signs — and binding approval to the whole entity would have required a signature to reschedule a wet Tuesday.\n"},"requiresApprovalToCancel":{"type":"boolean","default":true,"description":"**Cancelling a sold performance is the one transition that needs a name against it.** `assessProductChange` already answers how many tickets are affected; this decides who has to look at that number before the button works.\n"},"status":{"type":"string","enum":["scheduled","onSale","soldOut","suspended","cancelled","completed"]},"admissionRulesId":{"type":"string","format":"uuid","nullable":true},"seatMapId":{"type":"string","format":"uuid","nullable":true},"language":{"type":"string","nullable":true,"maxLength":35,"pattern":"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$","description":"The language the performance is given in, as a BCP 47 tag (`en`, `ar`, `fr`, `de`, `zh`, `ru`, `ar-AE`). **A guided tour at 10:00 in French and one at 10:00 in Arabic are two performances**, so a guest who picks a language sees only the tours in it (`listPerformances` `language`). Null when the performance is not language-specific (decided 29 September, rev 3 REV3-17).\n"},"format":{"type":"string","nullable":true,"maxLength":40,"description":"How it is presented, free text the venue chooses, e.g. `2D`, `3D`, `IMAX`, `subtitled`. A cinema screening shows language and format together. Null when it does not apply (decided 29 September, rev 3 REV3-17).\n"}}},
"PerformanceCancellationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["performanceId","dryRun","affectedOrders","refundExposure"],"properties":{"performanceId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"affectedOrders":{"type":"integer"},"affectedGuests":{"type":"integer"},"refundExposure":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the cancellation costs. Returned before committing, so the person cancelling sees the number at the moment they decide.\n"},"bulkRefundBatchId":{"type":"string","nullable":true,"description":"**Null on this response.** The refund batch is created by `orders` when it consumes `performance.cancelled` (F09), after this call has returned, and is queued there for approval — refunds are not issued automatically. Read it from orders, not from here.\n"},"notificationsQueued":{"type":"integer"}}},
"PerformanceTemplate": {"type":"object","x-ticvai-persistence":"catalogue.performance_template","description":"Event board 8. **An activity venue sells time, not seats.** Each slot the template produces is a Performance. Formerly `SessionTemplate` on `catalogue.session_template`: a session is a Performance (decided 28 September, audit R165).","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"spaceId":{"type":"string","format":"uuid","nullable":true},"slotMinutes":{"type":"integer"},"turnaroundMinutes":{"type":"integer","default":0},"concurrentCapacity":{"type":"integer"},"bands":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["offPeak","standard","peak","superPrime"]},"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string"},"to":{"type":"string"},"priceMultiplier":{"type":"number","nullable":true},"minuteMultiplier":{"type":"number","nullable":true}}}},"walkIn":{"type":"object","description":"**Configured, not assumed.** It decides whether a family turning up on a Sunday is turned away.\n","properties":{"allowed":{"type":"boolean","default":true},"heldBackPercent":{"type":"integer","default":0},"cutoffMinutesBefore":{"type":"integer","nullable":true}}},"scopePath":{"type":"string"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"Price": {"x-ticvai-persistence":"catalogue.price","type":"object","required":["priceListId","variantId","amount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"priceListId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true}}},
"PriceList": {"x-ticvai-persistence":"catalogue.price_list","type":"object","required":["id","code","name","venueId","currency","currencyScale","channels"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire, removed from the table** — a client should not walk a hierarchy to read a figure, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overridable below, so a row in a UAE region is AED and cannot be anything else — storing it per row is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a client reading a figure should not walk a hierarchy to know what it means, and the database should not hold nine million copies of AED. Four tables genuinely differ from their region and keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a workstation with its own currency is a misconfiguration.**\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"priority":{"type":"integer","description":"Where lists overlap, higher priority wins."},"description":{"type":"string","nullable":true,"description":"Price list master fields (29 September, data model DM3), set with `setPriceListMaster` (ADM-058)."},"priceListType":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"default":"standardRetail"},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"active"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"tags":{"type":"array","items":{"type":"string"}},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"brand":{"type":"string","maxLength":100,"nullable":true},"businessUnit":{"type":"string","maxLength":100,"nullable":true},"countryCode":{"type":"string","maxLength":2,"nullable":true,"pattern":"^[A-Z]{2}$"},"marketCode":{"type":"string","maxLength":40,"nullable":true},"scopeLevel":{"type":"string","enum":["global","country","market","brand","venue","event","businessUnit"],"default":"venue"},"defaultPriceCategoryId":{"type":"string","format":"uuid","nullable":true},"roundingProfileId":{"type":"string","format":"uuid","nullable":true},"priceResolutionPolicyId":{"type":"string","format":"uuid","nullable":true},"allowOverrides":{"type":"boolean","default":false},"allowInheritance":{"type":"boolean","default":true},"allowMultipleCurrencies":{"type":"boolean","default":false},"allowProductSpecificRates":{"type":"boolean","default":true},"clonedFromPriceListId":{"type":"string","format":"uuid","nullable":true},"currentVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The active `catalogue.price_list_version`."}}},
"PricingDynamicPriceAction": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_action","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price action.","required":["dynamicPriceRuleId","type","value"],"properties":{"id":{"type":"string","format":"uuid"},"dynamicPriceRuleId":{"type":"string","format":"uuid"},"type":{"type":"string","maxLength":30},"value":{"type":"number"},"minPrice":{"type":"number","nullable":true},"maxPrice":{"type":"number","nullable":true}}},
"PricingDynamicPriceCondition": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_condition","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price rule condition.","required":["actionId","dynamicPriceRuleId","type","ruleOperator","valueJson","sequenceNo"],"properties":{"actionId":{"type":"string","format":"uuid"},"dynamicPriceRuleId":{"type":"string","format":"uuid"},"type":{"type":"string","maxLength":50},"ruleOperator":{"type":"string","maxLength":20},"valueJson":{"type":"string"},"sequenceNo":{"type":"integer"}}},
"PricingDynamicPriceRule": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_rule","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price rule.","required":["pricingRuleCode","name","priority","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"pricingRuleCode":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":200},"productId":{"type":"string","format":"uuid","nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","nullable":true},"channelId":{"type":"string","format":"uuid","nullable":true},"priority":{"type":"integer"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"dynamicPricingStrategyId":{"type":"string","format":"uuid","nullable":true,"description":"The `catalogue.dynamic_pricing_strategy` a dynamic rule belongs to (29 September, data model DM3). Null for a static pricing rule."},"ruleType":{"type":"string","maxLength":40,"nullable":true,"description":"Static rules: `PricingRuleCommandCenterView.ruleType`; dynamic rules: the builder's `ruleKind`."},"inputMetric":{"type":"string","maxLength":40,"nullable":true},"conditionLogic":{"type":"string","enum":["all","any"],"default":"all"},"cooldownMinutes":{"type":"integer","nullable":true,"minimum":0},"minimumDurationMinutes":{"type":"integer","nullable":true,"minimum":0},"exitThresholdOffset":{"type":"number","nullable":true},"rangeMinPercent":{"type":"number","nullable":true},"rangeMaxPercent":{"type":"number","nullable":true},"isProtected":{"type":"boolean","default":false,"description":"A protected segment or channel: dynamic adjustments never apply."}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProductVariant": {"x-ticvai-persistence":"catalogue.variant","type":"object","required":["id","productId","sku","axisValues","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"sku":{"type":"string"},"axisValues":{"type":"object","additionalProperties":{"type":"string"}},"name":{"type":"string","maxLength":150,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"},"barcode":{"type":"string","maxLength":64,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"},"isDefault":{"type":"boolean","default":false,"description":"Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"},"isActive":{"type":"boolean","description":"False when retired. Retired variants are never deleted — orders reference them."},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"}}},
"Promotion": {"x-ticvai-persistence":"promotions.promotion","allOf":[{"$ref":"#/components/schemas/CreatePromotionRequest"},{"type":"object","required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/PromotionStatus"},"isPaused":{"type":"boolean"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"publishedAt":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"Starts at 1 and goes up by one on every saved change. The version the directory, the audit history (`promotions.promotion_audit`) and the channel publication monitor (`promotions.promotion_channel_publication`) name. (DM5, 29 September: data model for the agreed operations)"}}}]},
"PromotionConditions": {"x-ticvai-persistence":"none — embedded in promotion","type":"object","description":"All conditions must hold. An empty object matches everything.","properties":{"variantIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productKinds":{"type":"array","items":{"type":"string"}},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minQuantity":{"type":"integer","minimum":1},"minBasketValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channels":{"type":"array","description":"Empty or absent matches every channel.","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"purchaseGate":{"type":"boolean","default":false,"description":"BL-037. **`evaluatePromotions` gates a price and nothing gated a sale.** A non-member could buy a member-only product at the member price refused, which is a discount failure rather than an eligibility one.\nTrue makes these conditions a **precondition of purchase**: fail them and the line cannot be added, not merely charged more. **Evaluated at add-to-cart**, because a guest told at payment has already entered a card.\n"},"paymentMethod":{"type":"array","nullable":true,"description":"BL-113. **Card-issuer and payment-type promotions** — *10% with a Network International card* is a real campaign a bank co-funds, and it was unexpressible.\n**Evaluated at payment, not at cart**, which is the awkward part: the discount appears after the tender is chosen, and the basket total must be allowed to move at that point.\n","items":{"type":"string"}},"issuerBins":{"type":"array","nullable":true,"description":"Card BIN ranges, where the campaign is issuer-specific rather than scheme-specific. **The bank supplies these and they change**, so they are data rather than configuration.\n","items":{"type":"string"}},"componentRedemption":{"type":"string","nullable":true,"enum":["allTogether","independently","sequenced"],"description":"BL-112. **Per-component redemption inside a bundle was unstated.** A park-plus-lunch bundle where lunch may be used another day behaves differently from one where both must be used on the same visit, and **the difference is revenue recognition, not just convenience.**\n"},"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"membershipTierIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresCoupon":{"type":"boolean","default":false},"firstPurchaseOnly":{"type":"boolean","default":false},"performanceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"advanceDaysMin":{"type":"integer","description":"Early-bird — booked at least this many days ahead."},"advanceDaysMax":{"type":"integer","description":"Last-minute — booked no more than this many days ahead."},"eligibilityRuleIds":{"type":"array","nullable":true,"items":{"type":"string","format":"uuid"},"description":"Reusable eligibility rules (`promotions.promotion_rule` rows of `ruleType: eligibility` with no promotion of their own, saved by setEligibilityRule) that must also hold. Each is evaluated with its own `effect`. (DM5, 29 September: data model for the agreed operations)"}}},
"PromotionEvaluation": {"x-ticvai-persistence":"none — computed","type":"object","required":["totalDiscount","lines","applied","rejected"],"properties":{"totalDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lines":{"type":"array","items":{"type":"object","required":["lineId","originalPrice","discountedPrice","discount"],"properties":{"lineId":{"type":"string"},"originalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"applied":{"type":"array","items":{"type":"object","required":["promotionId","promotionCode","discount"],"properties":{"promotionId":{"type":"string","format":"uuid"},"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"couponCode":{"type":"string","nullable":true}}}},"rejected":{"type":"array","description":"Promotions that matched the products but did not apply, with the reason. This is what a cashier reads to a guest who expected a discount.\n","items":{"type":"object","required":["promotionCode","reason"],"properties":{"promotionCode":{"type":"string"},"promotionName":{"type":"string"},"reason":{"type":"string","enum":["conditionsNotMet","supersededByBetterOffer","exclusivePromotionApplied","redemptionLimitReached","budgetExhausted","outsideValidPeriod","wrongChannel","membershipRequired","couponRequired"]},"detail":{"type":"string"}}}}}},
"PromotionStatus": {"type":"string","enum":["draft","scheduled","live","paused","expired","ended"]},
"PromotionUsage": {"x-ticvai-persistence":"none — aggregated from ledger and orders","type":"object","required":["promotionId","redemptionCount","discountGiven"],"properties":{"promotionId":{"type":"string","format":"uuid"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetCap":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budgetRemaining":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isBudgetExhausted":{"type":"boolean"},"byChannel":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"redemptionCount":{"type":"integer"},"discountGiven":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"PromotionVariant": {"x-ticvai-persistence":"promotions.promotion_variant","type":"object","description":"One arm of a promotion A/B test (BL-114), written by `setPromotionVariants`. **Stored as rows** because the split has to be read back at evaluation time. The body used to be a free object with no table behind it, so the variants a caller set could not be persisted.\n","required":["label","trafficPercent"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"promotionId":{"type":"string","format":"uuid","readOnly":true,"description":"Taken from the path."},"label":{"type":"string"},"trafficPercent":{"type":"integer","minimum":0,"maximum":100,"description":"Share of traffic. All variants of a promotion sum to 100, with no minimum per variant (decided 28 September, audit R101)."},"discountPercent":{"type":"number"}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"SalesChannel": {"type":"string","description":"**Where a sale came from.** Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing.\n**Not interchangeable with the local `Channel` enums.** `catalogue.Channel` and `orders.Channel` are byte-identical duplicates of each other listing `pos, kiosk, web, mobile, b2b, ota, callCentre`; `orders.OrderChannel` lists `guestApp, guestWeb, partner, api, backOffice` on top. **Pointing the nine at a local enum would silently narrow them** — and the duplication between the two `Channel` enums is the reason a shared one existed in the first place.\n**This is the reporting dimension**: attribution, promotion eligibility and settlement all group by it, which is why it has to mean the same thing in `orders`, `catalogue`, `subscription` and `marketing-crm` rather than four things that nearly line up.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice","b2b","ota"]},
"SeatAvailability": {"x-ticvai-persistence":"none — computed from seat, hold and block","type":"object","required":["performanceId","seatMapId","renderMode","totals","seats"],"properties":{"performanceId":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"renderMode":{"type":"string","enum":["graphical","list"],"description":"The mode the server actually used. With `mode=auto` this is how a client knows what it got: `list` means the map has no geometry (the seat map's `noGeometry` state), so the client sells from categories and best-available groups and does not draw a plan. `graphical` means every seat carries `position`.\n"},"totals":{"type":"object","properties":{"total":{"type":"integer"},"available":{"type":"integer"},"held":{"type":"integer"},"sold":{"type":"integer"},"blocked":{"type":"integer"},"buffered":{"type":"integer"}}},"byCategory":{"type":"array","items":{"type":"object","properties":{"categoryId":{"type":"string","format":"uuid"},"available":{"type":"integer"},"sold":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"sections":{"type":"array","description":"The map's sections with what a guest screen needs to show the view from each (decided 29 September, rev 3 23SEP-14): the photo where the venue supplied one, otherwise null and the client renders the view from `boundary` and the seat positions. In this response so WEB-007 and GST-049 need no second call.\n","items":{"type":"object","required":["code","name"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"description":"As `Section.viewAssetId`. Null means render the view from geometry."},"boundary":{"type":"array","nullable":true,"items":{"$ref":"#/components/schemas/Point"},"description":"As `Section.boundary`. Null when `renderMode` is `list`."}}}},"seats":{"type":"array","items":{"type":"object","required":["seatId","status"],"properties":{"seatId":{"type":"string"},"status":{"$ref":"#/components/schemas/SeatStatus"},"categoryId":{"type":"string","format":"uuid","nullable":true},"displayLabel":{"type":"string","description":"What the guest sees, e.g. `A2-7-11`, as on `Seat`."},"position":{"allOf":[{"$ref":"#/components/schemas/Point"}],"nullable":true,"description":"The seat's coordinates on the map, as on `Seat`. Present when `renderMode` is `graphical`; null when it is `list`."}}}}}},
"SeatRecommendation": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatIds","totalPrice","isContiguous","rank"],"properties":{"seatIds":{"type":"array","items":{"type":"string"}},"displayLabels":{"type":"array","items":{"type":"string"}},"totalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryId":{"type":"string","format":"uuid"},"isContiguous":{"type":"boolean"},"rank":{"type":"integer","description":"Best first."},"rationale":{"type":"string","description":"Why this option was chosen — closest to stage, best value in category, only contiguous block remaining. Shown to a call-centre agent, not the guest.\n"}}},
"SeatRecommendationRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["partySize","strategy"],"properties":{"partySize":{"type":"integer","minimum":1,"maximum":50},"strategy":{"$ref":"#/components/schemas/SeatRecommendationStrategy"},"categoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"maxPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accessibleCount":{"type":"integer","default":0,"description":"Wheelchair spaces in the party. Companions are added automatically."},"maxOptions":{"type":"integer","default":3,"maximum":10}}},
"SeatRecommendationStrategy": {"type":"string","enum":["bestAvailable","bestValue","closestToStage","accessible","contiguous"]},
"SeatStatus": {"type":"string","enum":["available","held","sold","blocked","buffered","unavailable"]},
"SetPriceRequest": {"type":"object","required":["variantId","amount"],"properties":{"variantId":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid"}}},
"StackingMode": {"type":"string","description":"How this promotion combines with others. Declared, never inferred from creation order — two reasonable promotions can otherwise combine into a free ticket.\n","enum":["exclusive","stackable","bestOnly","stackWithGroup"]},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"UpdateProductRequest": {"type":"object","minProperties":1,"properties":{"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. At most one product per venue in a family, else `409 duplicate-code`."},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"dataMaskValues":{"type":"object","additionalProperties":true},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"See `Product.salesContact` (W3, 29 September)."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"See `Product.bookingFlowId` (W8, W12, 29 September)."},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"}},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"}},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"}},"requiresTimeWindow":{"type":"boolean"}}},
"VariantDimension": {"x-ticvai-persistence":"catalogue.variant_dimension","type":"object","description":"**A length is an axis like any other** (decided 29 September, rev 3 REV3-13). A meeting room type sold by the hour has an axis `length` with values `1h`, `2h`, `halfDay`, `fullDay`, each carrying `durationMinutes` (proposed 60, 120, 240 and 480, client to correct), and each generated variant is priced on its own, so a half day need not cost four single hours.\n","required":["code","name","values"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"values":{"type":"array","minItems":1,"items":{"type":"object","required":["code","label"],"properties":{"code":{"type":"string","maxLength":64},"label":{"type":"string","maxLength":200},"priceDelta":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"durationMinutes":{"type":"integer","minimum":15,"maximum":1440,"nullable":true,"description":"How long a variant carrying this value books its space for, on a `length` axis of a product with `requiresTimeWindow` (decided 29 September, rev 3 REV3-13). Null on any other axis. One axis per product at most may carry it; a second is a `400`."}}}}}},
"Voucher": {"x-ticvai-persistence":"promotions.voucher","type":"object","required":["code","batchId","faceValue","balance","status"],"properties":{"code":{"type":"string"},"batchId":{"type":"string","format":"uuid"},"faceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["issued","partiallyRedeemed","redeemed","expired","voided"]},"validTo":{"type":"string","format":"date-time"}}},
"VoucherBatch": {"x-ticvai-persistence":"promotions.voucher_batch","allOf":[{"$ref":"#/components/schemas/CreateVoucherBatchRequest"},{"type":"object","required":["id","issuedCount","redeemedValue","outstandingLiability"],"properties":{"id":{"type":"string","format":"uuid"},"issuedCount":{"type":"integer"},"redeemedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"outstandingLiability":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Unredeemed value. A liability until redeemed or expired."}}}]},
"WaitlistEntry": {"type":"object","x-ticvai-persistence":"catalogue.waitlist_entry","required":["performanceId","partySize"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"performanceId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"contactPoint":{"type":"string","description":"**Where the offer goes.** An entry with no way to reach the guest is an entry that can never be honoured, so this is required even for an anonymous guest.\n"},"partySize":{"type":"integer","minimum":1},"status":{"allOf":[{"$ref":"#/components/schemas/WaitlistStatus"}],"readOnly":true,"description":"Set by the server. `joinWaitlist` does not take it; a new entry is `waiting`."},"position":{"type":"integer","readOnly":true,"description":"First in, first offered. Shown to the guest, because not knowing is worse than waiting."},"offeredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"offerExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**The offer moves on when this passes.** Notifying everyone at once produces a race the fastest guest wins; holding indefinitely for someone asleep leaves the seat unsold.\n"},"joinedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WaitlistStatus": {"type":"string","enum":["waiting","offered","converted","expired","left"]}
}
```
