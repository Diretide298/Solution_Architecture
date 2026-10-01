# P08-orders-money-01 — P08 · Orders & Money (1 of 3)

**10 screens · 80 operations · 113 schemas · 32 permissions**

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

- **Every control that can be refused must be gated.** 32 permissions apply here:
  `ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW, CASH_LIFT, CASH_NO_SALE, GUEST_VIEW, LEDGER_POST, LEDGER_VIEW, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REFUND`…. A control nobody can use must say so,
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
| `BO-008` | Product Detail & Variants | A | 41 | 39 | 6 | 37 | 22 | 3 | — | notStarted (generated) |
| `BO-022` | Order Detail | B–D | 127 | 53 | 6 | 72 | 1 | 0 | — | notStarted (generated) |
| `BO-023` | Refunds & Exchanges | B–D | 121 | 71 | 6 | 71 | 3 | 6 | — | notStarted (generated) |
| `BO-024` | Payment Exceptions | B–D | 45 | 0 | 5 | 11 | 0 | 0 | — | notStarted (generated) |
| `BO-025` | Chargebacks & Disputes | B–D | 10 | 49 | 6 | 5 | 0 | 0 | — | notStarted (generated) |
| `BO-026` | Group Bookings | B–D | 158 | 69 | 6 | 77 | 2 | 6 | — | notStarted (generated) |
| `BO-027` | Reissue & Media Replacement | B–D | 10 | 23 | 6 | 24 | 0 | 0 | — | notStarted (generated) |
| `BO-028` | Refund Approval Queue | B–D | 6 | 0 | 4 | 10 | 5 | 6 | — | notStarted (generated) |
| `BO-029` | Report Builder | A | 64 | 35 | 6 | 93 | 1 | 0 | — | notStarted (generated) |
| `BO-039` | Shift Directory | B–D | 61 | 56 | 6 | 6 | 2 | 6 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-008` Product Detail & Variants

**Define what is sold and the ticket types under it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #20668 (APP-SETUP-BO-008) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW`, `GUEST_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE` (3 read, 2 configure); in the flows as partner, supervisor, venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listProductVariants` reads the population and `getProduct` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `productId` (deepLink), `variantId` (navigation), `version` (navigation) · cold entry: A product opened from the directory or a shared link. Shows what replaced it where it retired. |
| Route | `/venue-operations/product-detail-variants` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Carried `runFxRevaluation`, `getForeignTenderReport` and `listInterEntityObligations` until 20 August** — a product screen doing foreign-exchange revaluation. Operations were attached from the 14 August wireframe board by a heuristic that matched nothing. **Rewired 20 August.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Photos and videos | repeatable rows | optional | — | at most 20 | — | Picks from the asset library (`searchMedia`); one item is marked primary. Saved with `updateProduct`, which registers the use of each asset (decided 29 September, rev 3 23SEP-4). | `Product.media` |
| Consent questions this product asks | multi-picker: choose consent questions | optional | — | at most 10; no duplicates | — | Active questions from `listConsentQuestions`, written on CMS-018; ordered as the guest meets them. The guest is asked these together with the booking flow's own, each once (decided 29 September, rev … | `Product.consentQuestionIds` |
| Booking flow | picker: choose a booking flow | optional | — | — | shows names, sends the id | **Which booking flow sells this product** (decided 29 September, W8 and W12): a flow from CMS-103, e.g. *workshop: product first, then date and time*. Empty means the category's flow, then the … | `Product.bookingFlowId` |
| Sales phone | phone field | optional | — | max length 32 | +971 5X XXX XXXX (E.164) | **Contact sales to book** (decided 29 September, W3). Shown beside `guestListing`; used only when the product is info only, as *Call sales* on WEB-004 and GST-004. Empty phone and email means the … | `Product.salesContact.phone` |
| Sales email | email field | optional | — | max length 254 | name@example.ae | — | `Product.salesContact.email` |
| Note under the contact | text, one per language | optional | — | At most 200 characters per language. | English and Arabic (Arabic right to left) | At most 200 characters per language, e.g. *Group courses are booked by phone*. | `Product.salesContact.note` |

**Form: Save product attributes** (modal, opened by *Save product attributes*; *Save product attributes* calls `setProductAttributes`, *Cancel* sends nothing)

**Collects what `setProductAttributes` sends before it is called.** Required: `axes`. **A meeting-room type sells by length**: a `length` axis whose values each carry `durationMinutes` (e.g. 60, 120, 240, 480; minimum 15), one such axis per product, on a product with `requiresTimeWindow` on; each length is a variant priced on its own (decided 29 September, rev 3 REV3-13). Dismissing sends nothing; the screen behind is unchanged.

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

**Form: Save product** (modal, opened by *Save product*; *Save product* calls `updateProduct`, *Cancel* sends nothing)

**Collects what `updateProduct` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `channels`, `dataMaskValues`, and what the guest sees (decided 29 September, rev 3): `guestListing` and `notBookableLabel` (REV3-14), `displayTags` (at most six, 23SEP-3), `media` (23SEP-4), `consentQuestionIds` (REV3-26) and `requiresTimeWindow` (REV3-13); `salesContact` (W3) and `bookingFlowId` (W8, W12), decided 29 September. Dismissing sends nothing; the screen behind is unchanged.

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

**Form: Save ticket type** (modal, opened by *Save ticket type*; *Save ticket type* calls `updateProductVariant`, *Cancel* sends nothing)

**Collects what `updateProductVariant` sends before it is called.** Nothing in the body is required. Optional: `name`, `description` (who the ticket type is for and what it includes, at most 300 characters per language, shown behind the (i) when the booking flow has `cardInfo` on; decided 29 September, rev 3 23SEP-6), `barcode`, `isDefault` (setting it clears the default on the product's other variants). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 150 | — | — | `updateProductVariant` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateProductVariant` body |
| Barcode `barcode` | text field | optional | — | max length 64 | — | — | `updateProductVariant` body |
| Is default `isDefault` | toggle | optional | — | — | — | — | `updateProductVariant` body |

Errors to draw in the form: 400 A `description` value longer than 300 characters.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The variant is retired (`isActive` false), or is not a variant of this product.

#### Outputs: what the screen shows and produces

**Shown**

**Every product variant** (data table, from `listProductVariants`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| SKU | text | — |
| Axis values | grouped details | — |
| Is active | yes / no (icon or chip) | False when retired. Retired variants are never deleted — orders reference them. |

**The selected product variant** (detail panel, from `listProductVariants`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| SKU | text | — |
| Axis values | grouped details | — |
| Name | text | Taken from their variant tables, 20 September. `axisValues` gives `{size: L}` and no string a guest can read. |
| Barcode | text | Taken from their variant tables, 20 September. `catalogue.alternative_code` is a partner's own code for a variant and requires `partnerId` … |
| Description | in the reader's language | Who this ticket type is for and what it includes, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September … |
| Is default | yes / no (icon or chip) | Taken from their variant tables. Which variant a product page opens on. |
| Is active | yes / no (icon or chip) | False when retired. Retired variants are never deleted — orders reference them. |

**The product** (detail panel, from `getProduct`)

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
| Category | the name it points at, never the id | Taken from their `fnb.product` and `retail.product`, 20 September. `catalogue.product_category` has existed since 20 August with two … |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |
| Is stock tracked | yes / no (icon or chip) | Taken from their `fnb.product`, 20 September. Whether a sale decrements stock, which is not what `isSellable` asks. |

**What the guest sees** (detail panel, from `getProduct`): **What the guest sees of the product** (decided 29 September, rev 3). `guestListing`: bookable (the default), info only, or hidden; an info-only product keeps its details and photo, shows `notBookableLabel` (default "Info only / Not bookable online") and opens details instead of Add to basket, and `addCartLine` refuses it `409` (REV3-14). `displayTags`: up to six, each a kind (clock, height …

| Shows | Format | Notes |
|---|---|---|
| Guest listing | chip: Bookable, Info only, Hidden | How a product appears to a guest (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to … |
| Not bookable label | in the reader's language | The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 … |
| Display tags | list or chips (count when long) | Short facts a guest reads on the ticket card and under *Read more*: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates … |
| Media | list or chips (count when long) | The product's own photos and video (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each … |
| Consent questions | list or chips (count when long) | The consent questions a guest answers when booking this product, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are … |
| Requires time window | yes / no (icon or chip) | True for a space sold by the hour, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). |
| Segment tags | list or chips (count when long) | 7.3.5. A channel and a segment tag are mandatory and nothing required either. |
| Sales contact | grouped details | Who a guest contacts to book a view-only product (decided 29 September, W3), e.g. |
| Booking flow | the name it points at, never the id | The booking flow this product is sold through (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save product attributes (primary button) | `setProductAttributes` PUT `/products/{productId}/attributes` | inline | inline | 400 Two axes share a code, or one axis repeats a value code.; 403 Authenticated but not permitted at the requested scope; 409 Regeneration would exceed the variant ceiling for this product … | opens modal first |
| Save product (secondary button) | `updateProduct` PATCH `/products/{productId}` | UpdateProductRequest | Product | 400 `media` with no `isPrimary` item or more than one, or one asset twice.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a … | opens modal first |
| Save ticket type (secondary button) | `updateProductVariant` PATCH `/products/{productId}/variants/{variantId}` | inline | ProductVariant | 400 A `description` value longer than 300 characters.; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `getProduct` (onLoad, Read a product); `listProductVariants` (onLoad, List generated variants)

**Where the user goes next**

- → `BO-007` Product Directory: *Product Directory*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product variants list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product variants untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product variants yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listProductVariants` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `getProduct` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `description` value longer than 300 characters.; 400 Two axes share a code, or one axis repeats a value code.; 400 `media` with no `isPrimary` item or more than one, or one asset twice.; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … |

#### Permissions

- `listBookingFlows` → `TENANT_CONFIGURE` (configure) · staff
- `getProduct` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listProductVariants` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `setProductAttributes` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateProduct` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateProductVariant` → `PRODUCT_CONFIGURE` (configure) · staff
- `searchMedia` → `ASSET_LIBRARY_VIEW` (read) · staff
- `listConsentQuestions` → `GUEST_VIEW` (read) · staff
- `restoreProductVersion` → `PRODUCT_CONFIGURE` (configure) · staff
- `assessProductChange` → `PRODUCT_CONFIGURE` (configure) · staff
- `cloneProduct` → `PRODUCT_CONFIGURE` (configure) · staff
- `listProductVersions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `getProduct` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

37 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.13 | The system should allow combination of multiple properties for all type of tickets. For example, there can be a VIP child ticket and a normal adult ticket. | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.32 | Ability to create and book dynamic performances based on the event start time. Dynamic performance to be chosen by customer 2 - 3 - 4 hour (for pods or Spaces) | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.33 | Book per time slot | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.34 | Book variable amount of minutes per individual 30 minute session. Can be at different times of the day and different times of the week / month. | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.37 | As above, If individuals purchase X number of minutes, they want the ability to book varying time slots on varying dates | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.38 | For example: If a skydiver or first time flyer wishes to “just turn up”.. we need the ability to sell to that individual and enter them onto the system and create a “ There and then” booking. Can be … | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.39 | Pre purchased number of minutes with variable price based on time slots . Peak, Off Peak, Super Prime etc etc etc . We need the ability to change these periods easily ie , if I wanted to make Prime … | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 1.3.40 | Ability for specific profiles to add minutes to their account. | Ticketing Catalogue | CONTRACTED | `listProductVariants` |
| 3.6.29 | Attribute-driven product architecture that lets teams add ticket types, add-ons, and bundles without duplicating SKUs (single definition, multi-variant) | Admission and Access | CONTRACTED | `listProductVariants` |
| 1.1.12 | The system should allow configuration of properties for all type of tickets that define the behavior of the ticket. For example, an open-dated ticket can be available in different tiers such as … | Ticketing Catalogue | CONTRACTED | `setProductAttributes` |
| 1.1.45 | Configure product attributes and metadata | Ticketing Catalogue | CONTRACTED | `setProductAttributes` |
| 1.1.46 | Support multilingual product descriptions | Ticketing Catalogue | CONTRACTED | `updateProduct` |
| … 25 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: all policy types — reschedule, exchange, refund, cancellation, upgrade/downgrade, ownership transfer, membership-to-pass conversion — are managed centrally within the unified product configuration, not separate screens. Each product also maps pricing, GL account code, promotions and channel availability. *(agreed · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies; 5. Key Decisions · DI-466)*
- Decision: special product types — group (min/max size, single or multiple QR codes), family (min/max composition) and corporate/allocation tickets — are configured within the same unified product configuration screen, not separate screens. *(agreed · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships; 5. Key Decisions · DI-465)*
- Quantity/purchase limits can be set per order, per guest, per account category and per sales channel (e.g. maximum 6 tickets per transaction). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-464)*
- Eligibility rules are configurable: residency/nationality/geography (e.g. UAE-resident-only with Emirates ID capture), minimum age (date-of-birth check), guest-profile category (e.g. VIP-only) and minimum loyalty points/spend for a membership tier. *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-463)*
- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)*
- Validity types: fixed date range, rolling (e.g. 90 days from issue) and first-use activation (starts at first scan). Confirmed: first-use tickets need a fallback expiry (e.g. issue date + 30 days) if never scanned. *(agreed · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-451)*
- Products are classified by configurable components (e.g. resident/non-resident → standard/VIP tier → adult/child/youth), not a fixed structure; components can be added and a simple venue may use only guest category. Tickets can be anonymous or require captured guest details. *(client request · MoM 25 Aug 2026, 4.4 Product Combination Matrix & Ownership · DI-450)*
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)*
- Decision (raised by Chinmay): date-change/reschedule is a product-level on/off setting with its own policy rules (e.g. allowed up to 24 hours before the visit, denied within 24 hours), not a separate screen. Typically off for special-day tickets (e.g. New Year, 1 January only), on for standard GA. *(agreed · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive; 5. Key Decisions · DI-446)*
- Open-dated ticket: name, description, price and validity period (e.g. 1 day, 1 month, 6 months), with a configurable reservation rule controlling whether customer details (name, email, phone) are captured at point of sale. *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-445)*
- The preview/publish step shows how the ticket appears on the B2C front end and — at Chinmay's request — also the PDF ticket layout and Apple Wallet / Google Wallet formats, so the reviewer sees every output format. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-444)*
- Ticket attributes such as minimum age, ID-proof requirements (e.g. Emirates ID for UAE-resident tickets, with format validation or photo upload; passport; handicap/PoD documentation) or an embedded ID-reader for on-site verification are configurable per ticket and region, not fixed. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-443)*
- Content localisation: separate content (images, descriptions) per sales channel (POS vs. B2C/B2B) and per language (e.g. English/Arabic). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-442)*
- Identity & classification: product name, product ID, main/sub-category, venue (multi-venue), ticket type. A category hierarchy manager groups and sorts packages and ticket types (e.g. admission > general admission > single-day, multi-day, annual pass, packages, vouchers). *(client request · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference · DI-441)*
- Supporting configuration: ticket variants (adult/child/senior/VIP, configurable), waitlist, on-sale/off-sale timing and cut-offs, entitlement/access rules (single/multi-venue, entries, zones, early entry), fulfilment channels (email, WhatsApp, SMS), after-sales windows (upgrade, reschedule, cancel), dynamic/fixed pricing and promotions. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-437)*
- Guest information capture (name, mobile number, nationality, visit survey, etc.) is configurable per ticket type; even an open-dated admission ticket can optionally collect it. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-434)*
- Six core ticket types: Open-Dated (no fixed date; GA and B2B/travel-agent QR resale), Group & Family (configurable group size, single-scan or multi-scan QR), Membership/Subscription (full details per member; renew/upgrade/cancel), Event (date/time selection, resources, capacity), Gift Voucher, Money Card. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-433)*
- Ticket configuration flow runs basic information → ticket type configuration → validation → publish. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-432)*
- Product master holds price, stock and variant attributes (e.g. size/colour) with a distinct barcode per variant; stock is tracked per variant/size. Decision: size/variant attributes (small/medium/large) are configurable per product type in the admin panel and appear dynamically when products are added. *(agreed · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management; 5. Key Decisions · DI-354)*
- Entitlement settings: re-entry not allowed / once per day / unlimited; expiry end of week, month, year, variable date, from first use, or by performance date/time; group tickets by fixed price or fixed quantity; one ticket may link to several events. *(agreed · MoM 7 Aug 2026, 16. Entitlement Components: Re-entry, Expiration & Sale Restrictions · DI-171)*
- Components/attributes model: a component (e.g. "ticket type") has attributes (adult, youth, senior, infant, child) each priced independently; adding an attribute creates a new sellable variant with no extra setup. Who may sell a product is restricted by site, operating area, workstation or role. *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-164)*
- Product record holds: price (tax inclusive/exclusive), linked print template, system product code, a toggle for capturing reservation details at sale, and entitlements (upgradeable, stored-value load, linked event, re-entry, linked performance). Multiple price lists per channel and season (winter/summer). *(agreed · MoM 7 Aug 2026, 12. Products Configuration: Metric Sheets, Pricing & Components · DI-163)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A120** Build the product creation wizard with four paths (from scratch · save as reusable template · clone · file upload using a standard tenant data-collection template) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'product creation wizard')*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker · keyword 'ticket type')*
- **A229** Build turnstile and handheld scanner configuration (connection details, light and sound feedback by ticket type, custom welcome messaging and branding, compatibility testing and deployment) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S7 (HLD/LLD) · 2 Sep 2026 · workshop tracker · keyword 'ticket type')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-008` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 2.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 2.dc.html#fnb-2d`, `Retail Board 2.dc.html#ret-2c`
- Flow F10 *Partner books, uses and settles*, step 6: Venue reconciles and invoices → Usage becomes money owed
- Flow F85 *Production is planned, costed and released*, step 3: Product Detail & Variants. → **Drawn by the client as FNB-2D.** 4 operations on this step.
- Flow F93 *A recipe changes and its allergen claim is re-verified*, step 3: Product Detail & Variants. → **Drawn by the client as FNB-2D.**
- Flow F10 branch at step 6 (requiresStaff): when Usage disputed at reconciliation, Scan records are the evidence. This is why `scan_event` is retained and why offline scans carry both recordedAt and syncedAt.

#### Acceptance for the design

- [ ] Every input above is drawn (41), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save product attributes, Save product, Save ticket type.
- [ ] Every transition is wired: `BO-007`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`, `GUEST_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 22 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-022` Order Detail

**See everything about one order in one place.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_POST`, `LEDGER_VIEW`, `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`… (9 operate, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `orderId` (deepLink), `documentId` (navigation), `invoiceId` (navigation) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/venue-operations/order-detail` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listOrders`. | `listOrders` ?venueId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listOrders`. | `listOrders` ?principalId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listOrders`. | `listOrders` ?shiftId |
| Status | select | optional | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | — | Sends `?status=` to `listOrders`. | `listOrders` ?status |
| Created from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdFrom=` to `listOrders`. | `listOrders` ?createdFrom |
| Created to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdTo=` to `listOrders`. | `listOrders` ?createdTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |
| Order | picker: choose an order | — | — | `listTaxInvoices` ?orderId |
| Legal entity | picker: choose a legal entity | — | — | `listTaxInvoices` ?legalEntityId |
| Invoice type | segmented control | — | Simplified · Full · Consolidated | `listTaxInvoices` ?invoiceType |
| Status | radio group | — | Issued · Partially credited · Fully credited · Superseded | `listTaxInvoices` ?status |
| Issued from | date picker | — | — | `listTaxInvoices` ?issuedFrom |
| Issued to | date picker | — | — | `listTaxInvoices` ?issuedTo |
| Language | text field | — | pattern `^[a-z]{2}(-[A-Z]{2})?$` | `getTaxDocumentRendition` ?language |

**Form: Create order** (modal, opened by *Create order*; *Create order* calls `createOrder`, *Cancel* sends nothing)

**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `createOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createOrder` body |
| Channel `channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createOrder` body |
| Shift `shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `createOrder` body |
| Guest link `guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `createOrder` body |
| Catalogue bundle version `catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `createOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `createOrder` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createOrder` body |
| Recommendation `lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `createOrder` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Booked window `lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `createOrder` body |
| Starts at `lines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |
| Ends at `lines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `createOrder` body |
| Inventory hold `lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `createOrder` body |
| Seats `lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `createOrder` body |
| Resource hold `lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `createOrder` body |
| Attributes `lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `createOrder` body |
| Transport `lines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `createOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createOrder` body |
| Eligibility declaration `lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `createOrder` body |
| Age band `lines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `createOrder` body |
| Age years `lines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `createOrder` body |
| Height band index `lines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `createOrder` body |
| Confident swimmer `lines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `createOrder` body |
| Guardian signed `lines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `createOrder` body |
| Quoted unit price `lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `createOrder` body |
| Holder name `lines[].holderName` | text field | optional | — | — | — | — | `createOrder` body |
| Data mask values `lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `createOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 422 More seats for one performance than the channel allows (`seatLimitExceeded`, decided 29 September, rev 3 REV3-7). (OrderRefusedProblem)

**Form: Apply manual discount** (modal, opened by *Apply manual discount*; *Apply manual discount* calls `applyManualDiscount`, *Cancel* sends nothing)

**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header. | `applyManualDiscount` body |
| Line `lineId` | picker: choose a line | optional | — | — | shows names, sends the id | Omit to discount the order rather than a line. | `applyManualDiscount` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `applyManualDiscount` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `applyManualDiscount` body |
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything. | `applyManualDiscount` body |
| Reason code `reasonCode` | text field | optional | — | — | — | Optional alongside the free text, where the venue maintains a list. | `applyManualDiscount` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required above the venue threshold. May not be the requester. | `applyManualDiscount` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyManualDiscount` body |

Errors to draw in the form: 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem)

**Form: Create refund** (modal, opened by *Create refund*; *Create refund* calls `createRefund`, *Cancel* sends nothing)

**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header. | `createRefund` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to refund the whole order. | `createRefund` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createRefund` body |
| Secondary authorisation `secondaryAuthorisation` | group | optional | — | — | — | Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. | `createRefund` body |
| Principal `secondaryAuthorisation.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRefund` body |
| Credential `secondaryAuthorisation.credential` | text area | required | — | max length 512 | — | The second person's staff PIN, as they sign in at a till with it. A PIN, never a password (decided 28 September, audit R123 (7)). | `createRefund` body |
| Refund to original tender `refundToOriginalTender` | toggle | optional | on | — | — | — | `createRefund` body |
| Alternate tender `alternateTender` | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createRefund` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRefund` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount exceeds what remains … (RefundPolicyProblem)

**Form: Exchange order lines** (modal, opened by *Exchange order lines*; *Exchange order lines* calls `exchangeOrderLines`, *Cancel* sends nothing)

**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header. | `exchangeOrderLines` body |
| Outgoing lines `outgoingLineIds` | multi-picker: choose outgoing lines | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| Incoming lines `incomingLines` | repeatable rows | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| ID `incomingLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `exchangeOrderLines` body |
| Variant `incomingLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Recommendation `incomingLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `exchangeOrderLines` body |
| Performance `incomingLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Booked window `incomingLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `exchangeOrderLines` body |
| Starts at `incomingLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |
| Ends at `incomingLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `exchangeOrderLines` body |
| Inventory hold `incomingLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `exchangeOrderLines` body |
| Seats `incomingLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `exchangeOrderLines` body |
| Resource hold `incomingLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `exchangeOrderLines` body |
| Attributes `incomingLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `exchangeOrderLines` body |
| Transport `incomingLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `exchangeOrderLines` body |
| Quantity `incomingLines[].quantity` | number field | required | — | min 1 | — | — | `exchangeOrderLines` body |
| Eligibility declaration `incomingLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `exchangeOrderLines` body |
| Age band `incomingLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `exchangeOrderLines` body |
| Age years `incomingLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Height band index `incomingLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Confident swimmer `incomingLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `exchangeOrderLines` body |
| Guardian signed `incomingLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `exchangeOrderLines` body |
| Quoted unit price `incomingLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `exchangeOrderLines` body |
| Holder name `incomingLines[].holderName` | text field | optional | — | — | — | — | `exchangeOrderLines` body |
| Data mask values `incomingLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `exchangeOrderLines` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `exchangeOrderLines` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `exchangeOrderLines` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |

Errors to draw in the form: 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem)

**Form: Hold order** (modal, opened by *Hold order*; *Hold order* calls `holdOrder`, *Cancel* sends nothing)

**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Label `label` | text field | optional | — | max length 60 | — | How the cashier will find it again — a name, a description, a party size. A list of unlabelled parked sales is unusable at a busy counter. | `holdOrder` body |
| Hold until `holdUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |

Errors to draw in the form: 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem)

**Form: Modify order** (modal, opened by *Modify order*; *Modify order* calls `modifyOrder`, *Cancel* sends nothing)

**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this modification, not of the order — the order is the path's `orderId`. | `modifyOrder` body |
| Add lines `addLines` | repeatable rows | optional | — | — | — | — | `modifyOrder` body |
| ID `addLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `modifyOrder` body |
| Variant `addLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `modifyOrder` body |
| Recommendation `addLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `modifyOrder` body |
| Performance `addLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `modifyOrder` body |
| Booked window `addLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `modifyOrder` body |
| Starts at `addLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |
| Ends at `addLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `modifyOrder` body |
| Inventory hold `addLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `modifyOrder` body |
| Seats `addLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `modifyOrder` body |
| Resource hold `addLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `modifyOrder` body |
| Attributes `addLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `modifyOrder` body |
| Transport `addLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `modifyOrder` body |
| Quantity `addLines[].quantity` | number field | required | — | min 1 | — | — | `modifyOrder` body |
| Eligibility declaration `addLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `modifyOrder` body |
| Age band `addLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `modifyOrder` body |
| Age years `addLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `modifyOrder` body |
| Height band index `addLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `modifyOrder` body |
| Confident swimmer `addLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `modifyOrder` body |
| Guardian signed `addLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `modifyOrder` body |
| Quoted unit price `addLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `modifyOrder` body |
| Holder name `addLines[].holderName` | text field | optional | — | — | — | — | `modifyOrder` body |
| Data mask values `addLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `modifyOrder` body |
| Remove lines `removeLineIds` | multi-picker: choose remove lines | optional | — | — | — | — | `modifyOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `modifyOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |

Errors to draw in the form: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem)

**Form: Reprint order** (modal, opened by *Reprint order*; *Reprint order* calls `reprintOrder`, *Cancel* sends nothing)

**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delivery `delivery` | radio group | required | — | Print · Email · SMS · Whatsapp · Wallet | — | — | `reprintOrder` body |
| Destination `destination` | text field | optional | — | — | — | — | `reprintOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to reprint every line. | `reprintOrder` body |
| Reason `reason` | radio group | optional | — | Printer fault · Guest request · Lost ticket · Not received · Other | — | — | `reprintOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the till reprinted — device time, as for every offline-capable write. | `reprintOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Reschedule order** (modal, opened by *Reschedule order*; *Reschedule order* calls `rescheduleOrder`, *Cancel* sends nothing)

**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target performance `targetPerformanceId` | picker: choose a target performance | required | — | — | shows names, sends the id | — | `rescheduleOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to move the whole order. | `rescheduleOrder` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `rescheduleOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `rescheduleOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rescheduleOrder` body |

Errors to draw in the form: 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem)

**Sent by *Void order*** (`voidOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this void, and its idempotency key — it must equal the `Idempotency-Key` header. | `voidOrder` body |
| Reason `reason` | select | required | — | Guest changed mind · Entered in error · Item unavailable · Quality issue · Duplicate · Other | — | The void reason list (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. | `voidOrder` body |
| Note `note` | text area | optional | — | min length 3; max length 500; Required when `reason` is `other` (audit R222); optional otherwise. | — | Required when `reason` is `other` (audit R222); optional otherwise. | `voidOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `voidOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own. |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**The order statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order | the name it points at, never the id | — |
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Entries | list or chips (count when long) | Sequential. What an agent reads to a guest asking about a charge. |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |
| Lines | list or chips (count when long) | — |
| Payments | list or chips (count when long) | — |
| Principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create order (primary button) | `createOrder` POST `/orders` | CreateOrderRequest | Order | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the … | opens modal first |
| Apply manual discount (secondary button) | `applyManualDiscount` POST `/orders/{orderId}/discounts` | ManualDiscountRequest | Order | 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem) | opens modal first |
| Create refund (secondary button) | `createRefund` POST `/orders/{orderId}/refunds` | CreateRefundRequest | Refund | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount … | opens modal first |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Hold order (secondary button) | `holdOrder` POST `/orders/{orderId}/hold` | inline | Order | 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem) | opens modal first |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | opens modal first; produces a document or message: Reprint or resend tickets |
| Reschedule order (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |
| Resume order (secondary button) | `resumeOrder` POST `/orders/{orderId}/resume` | — | OrderResumeResult | 409 Held order expired (`holdExpired`), or already resumed at another till (`alreadyResumed`). (OrderRefusedProblem) | — |
| Void order (destructive button) | `voidOrder` POST `/orders/{orderId}/voids` | inline | Order | 409 Settled — a payment on the order has been `captured`, so the money has moved (`alreadySettled`) — or taken in a shift that is now closed (`shiftClosed`). (OrderRefusedProblem) | — |

**Data it reads**: `listOrders` (onLoad, List orders); `listTaxInvoices` (onLoad, List tax invoices); `getTaxInvoice` (onLoad, Show a tax invoice); `getTaxDocumentRendition` (onLoad, Download the invoice / credit memo PDF)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

**What opens over it**

- confirmDialog *Void order*: **Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A order this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is the void …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order yet. Offers Create order (`createOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the order are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 An order is not paid, is … |

#### Permissions

- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `createOrder` → `ORDER_CREATE` (operate) · staff, guest, partner
- `applyManualDiscount` → `ORDER_DISCOUNT` (operate) · staff, partner
- `createRefund` → `ORDER_REFUND` (operate) · staff, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `holdOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `resumeOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner
- `listTaxInvoices` → `LEDGER_VIEW` (read) · staff, guest
- `issueTaxInvoice` → `LEDGER_POST` (operate) · staff, guest, service
- `getTaxInvoice` → `LEDGER_VIEW` (read) · staff, guest
- `issueCreditMemo` → `LEDGER_POST` (operate) · staff, service
- `getTaxDocumentRendition` → `LEDGER_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

72 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 2.1.6 | This system should provide a Ticketing POS solution that enables the operator to sell all the tickets defined in the system including multi-day and combo tickets. The POS solution must also support … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.29 | The system should be able to offer ticket sales to various outside business entities through the use of the exposed APIs and dedicated modules. Examples of typical clients that would have discounts … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.30 | The system should cater to multiple ways of enabling B2B clients, resellers and partner distribution channels to resell tickets and services offered by the client: - Web-based solution for B2B … | Ticketing Sales | CONTRACTED | `createOrder` |
| … 60 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reservation lookup shows items, customer, payment method, taxes and an optional post-purchase survey, with reprint receipt and regenerate ticket PDF actions. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-179)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-022` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (127), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (53 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create order, Apply manual discount, Create refund, Exchange order lines, Hold order, Modify order, Reprint order, Reschedule order, Resume order, Void order.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `LEDGER_POST`, `LEDGER_VIEW`, `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-023` Refunds & Exchanges

**Give money back, or move the booking.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_POST`, `LEDGER_VIEW`, `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`… (9 operate, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrderRefunds` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `orderId` (deepLink), `venueId` (session), `documentId` (navigation), `invoiceId` (navigation) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/venue-operations/refunds-exchanges` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **`getRefundPolicy` wired 24 August.** **A refunds screen that cannot read the refund policy** judges every request by memory — and F09 was reaching it through `BO-003 Queue Integration Setup`, which held the operation only because of the 18 August bulk attach.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Principal | picker: choose a principal | — | — | `listOrders` ?principalId |
| Shift | picker: choose a shift | — | — | `listOrders` ?shiftId |
| Status | select | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | `listOrders` ?status |
| Created from | date and time picker | — | — | `listOrders` ?createdFrom |
| Created to | date and time picker | — | — | `listOrders` ?createdTo |
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |
| Tax invoice | picker: choose a tax invoice | — | — | `listCreditMemos` ?taxInvoiceId |
| Refund | picker: choose a refund | — | — | `listCreditMemos` ?refundId |
| Legal entity | picker: choose a legal entity | — | — | `listCreditMemos` ?legalEntityId |
| Issued from | date picker | — | — | `listCreditMemos` ?issuedFrom |
| Issued to | date picker | — | — | `listCreditMemos` ?issuedTo |
| Language | text field | — | pattern `^[a-z]{2}(-[A-Z]{2})?$` | `getTaxDocumentRendition` ?language |

**Form: Create refund** (modal, opened by *Create refund*; *Create refund* calls `createRefund`, *Cancel* sends nothing)

**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header. | `createRefund` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to refund the whole order. | `createRefund` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createRefund` body |
| Secondary authorisation `secondaryAuthorisation` | group | optional | — | — | — | Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. | `createRefund` body |
| Principal `secondaryAuthorisation.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRefund` body |
| Credential `secondaryAuthorisation.credential` | text area | required | — | max length 512 | — | The second person's staff PIN, as they sign in at a till with it. A PIN, never a password (decided 28 September, audit R123 (7)). | `createRefund` body |
| Refund to original tender `refundToOriginalTender` | toggle | optional | on | — | — | — | `createRefund` body |
| Alternate tender `alternateTender` | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createRefund` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRefund` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount exceeds what remains … (RefundPolicyProblem)

**Form: Apply manual discount** (modal, opened by *Apply manual discount*; *Apply manual discount* calls `applyManualDiscount`, *Cancel* sends nothing)

**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header. | `applyManualDiscount` body |
| Line `lineId` | picker: choose a line | optional | — | — | shows names, sends the id | Omit to discount the order rather than a line. | `applyManualDiscount` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `applyManualDiscount` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `applyManualDiscount` body |
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything. | `applyManualDiscount` body |
| Reason code `reasonCode` | text field | optional | — | — | — | Optional alongside the free text, where the venue maintains a list. | `applyManualDiscount` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required above the venue threshold. May not be the requester. | `applyManualDiscount` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyManualDiscount` body |

Errors to draw in the form: 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem)

**Form: Create order** (modal, opened by *Create order*; *Create order* calls `createOrder`, *Cancel* sends nothing)

**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `createOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createOrder` body |
| Channel `channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createOrder` body |
| Shift `shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `createOrder` body |
| Guest link `guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `createOrder` body |
| Catalogue bundle version `catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `createOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `createOrder` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createOrder` body |
| Recommendation `lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `createOrder` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Booked window `lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `createOrder` body |
| Starts at `lines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |
| Ends at `lines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `createOrder` body |
| Inventory hold `lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `createOrder` body |
| Seats `lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `createOrder` body |
| Resource hold `lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `createOrder` body |
| Attributes `lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `createOrder` body |
| Transport `lines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `createOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createOrder` body |
| Eligibility declaration `lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `createOrder` body |
| Age band `lines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `createOrder` body |
| Age years `lines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `createOrder` body |
| Height band index `lines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `createOrder` body |
| Confident swimmer `lines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `createOrder` body |
| Guardian signed `lines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `createOrder` body |
| Quoted unit price `lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `createOrder` body |
| Holder name `lines[].holderName` | text field | optional | — | — | — | — | `createOrder` body |
| Data mask values `lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `createOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 422 More seats for one performance than the channel allows (`seatLimitExceeded`, decided 29 September, rev 3 REV3-7). (OrderRefusedProblem)

**Form: Exchange order lines** (modal, opened by *Exchange order lines*; *Exchange order lines* calls `exchangeOrderLines`, *Cancel* sends nothing)

**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header. | `exchangeOrderLines` body |
| Outgoing lines `outgoingLineIds` | multi-picker: choose outgoing lines | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| Incoming lines `incomingLines` | repeatable rows | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| ID `incomingLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `exchangeOrderLines` body |
| Variant `incomingLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Recommendation `incomingLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `exchangeOrderLines` body |
| Performance `incomingLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Booked window `incomingLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `exchangeOrderLines` body |
| Starts at `incomingLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |
| Ends at `incomingLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `exchangeOrderLines` body |
| Inventory hold `incomingLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `exchangeOrderLines` body |
| Seats `incomingLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `exchangeOrderLines` body |
| Resource hold `incomingLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `exchangeOrderLines` body |
| Attributes `incomingLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `exchangeOrderLines` body |
| Transport `incomingLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `exchangeOrderLines` body |
| Quantity `incomingLines[].quantity` | number field | required | — | min 1 | — | — | `exchangeOrderLines` body |
| Eligibility declaration `incomingLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `exchangeOrderLines` body |
| Age band `incomingLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `exchangeOrderLines` body |
| Age years `incomingLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Height band index `incomingLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Confident swimmer `incomingLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `exchangeOrderLines` body |
| Guardian signed `incomingLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `exchangeOrderLines` body |
| Quoted unit price `incomingLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `exchangeOrderLines` body |
| Holder name `incomingLines[].holderName` | text field | optional | — | — | — | — | `exchangeOrderLines` body |
| Data mask values `incomingLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `exchangeOrderLines` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `exchangeOrderLines` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `exchangeOrderLines` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |

Errors to draw in the form: 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem)

**Form: Hold order** (modal, opened by *Hold order*; *Hold order* calls `holdOrder`, *Cancel* sends nothing)

**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Label `label` | text field | optional | — | max length 60 | — | How the cashier will find it again — a name, a description, a party size. A list of unlabelled parked sales is unusable at a busy counter. | `holdOrder` body |
| Hold until `holdUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |

Errors to draw in the form: 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem)

**Form: Modify order** (modal, opened by *Modify order*; *Modify order* calls `modifyOrder`, *Cancel* sends nothing)

**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this modification, not of the order — the order is the path's `orderId`. | `modifyOrder` body |
| Add lines `addLines` | repeatable rows | optional | — | — | — | — | `modifyOrder` body |
| ID `addLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `modifyOrder` body |
| Variant `addLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `modifyOrder` body |
| Recommendation `addLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `modifyOrder` body |
| Performance `addLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `modifyOrder` body |
| Booked window `addLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `modifyOrder` body |
| Starts at `addLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |
| Ends at `addLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `modifyOrder` body |
| Inventory hold `addLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `modifyOrder` body |
| Seats `addLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `modifyOrder` body |
| Resource hold `addLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `modifyOrder` body |
| Attributes `addLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `modifyOrder` body |
| Transport `addLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `modifyOrder` body |
| Quantity `addLines[].quantity` | number field | required | — | min 1 | — | — | `modifyOrder` body |
| Eligibility declaration `addLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `modifyOrder` body |
| Age band `addLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `modifyOrder` body |
| Age years `addLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `modifyOrder` body |
| Height band index `addLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `modifyOrder` body |
| Confident swimmer `addLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `modifyOrder` body |
| Guardian signed `addLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `modifyOrder` body |
| Quoted unit price `addLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `modifyOrder` body |
| Holder name `addLines[].holderName` | text field | optional | — | — | — | — | `modifyOrder` body |
| Data mask values `addLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `modifyOrder` body |
| Remove lines `removeLineIds` | multi-picker: choose remove lines | optional | — | — | — | — | `modifyOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `modifyOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |

Errors to draw in the form: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem)

**Form: Reprint order** (modal, opened by *Reprint order*; *Reprint order* calls `reprintOrder`, *Cancel* sends nothing)

**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delivery `delivery` | radio group | required | — | Print · Email · SMS · Whatsapp · Wallet | — | — | `reprintOrder` body |
| Destination `destination` | text field | optional | — | — | — | — | `reprintOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to reprint every line. | `reprintOrder` body |
| Reason `reason` | radio group | optional | — | Printer fault · Guest request · Lost ticket · Not received · Other | — | — | `reprintOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the till reprinted — device time, as for every offline-capable write. | `reprintOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Reschedule order** (modal, opened by *Reschedule order*; *Reschedule order* calls `rescheduleOrder`, *Cancel* sends nothing)

**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target performance `targetPerformanceId` | picker: choose a target performance | required | — | — | shows names, sends the id | — | `rescheduleOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to move the whole order. | `rescheduleOrder` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `rescheduleOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `rescheduleOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rescheduleOrder` body |

Errors to draw in the form: 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem)

**Sent by *Void order*** (`voidOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this void, and its idempotency key — it must equal the `Idempotency-Key` header. | `voidOrder` body |
| Reason `reason` | select | required | — | Guest changed mind · Entered in error · Item unavailable · Quality issue · Duplicate · Other | — | The void reason list (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. | `voidOrder` body |
| Note `note` | text area | optional | — | min length 3; max length 500; Required when `reason` is `other` (audit R222); optional otherwise. | — | Required when `reason` is `other` (audit R222); optional otherwise. | `voidOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `voidOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |
| Secondary principal | the name it points at, never the id | — |

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**The selected refund** (detail panel, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own. |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |
| Secondary principal | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Ledger entry | the name it points at, never the id | Written before the gateway is called. |
| Gateway reference | text | — |

**The order statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order | the name it points at, never the id | — |
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Entries | list or chips (count when long) | Sequential. What an agent reads to a guest asking about a charge. |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

**The refund policy** (detail panel, from `getRefundPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | The venue in the path. Not taken from a `setRefundPolicy` body. |
| Self authorise limit | AED 1,234.50 | Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser. |
| Requires second user above | AED 1,234.50 | Above this, a second user — cashier OR supervisor — names themselves as audit control. |
| Requires approval above | AED 1,234.50 | Above this, an ORDER_REFUND_APPROVE holder must approve. |
| Time bands | list or chips (count when long) | Refundable percentage by time before the performance. Evaluated most-specific first. |
| Allow partial | yes / no (icon or chip) | — |
| Refund window days | 1,234 | Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 … |
| Variance threshold | AED 1,234.50 | Price variance above this is an exception requiring review rather than a routine posting (CF-38). |

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |
| Lines | list or chips (count when long) | — |
| Payments | list or chips (count when long) | — |
| Principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create refund (primary button) | `createRefund` POST `/orders/{orderId}/refunds` | CreateRefundRequest | Refund | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount … | opens modal first |
| Apply manual discount (secondary button) | `applyManualDiscount` POST `/orders/{orderId}/discounts` | ManualDiscountRequest | Order | 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem) | opens modal first |
| Create order (secondary button) | `createOrder` POST `/orders` | CreateOrderRequest | Order | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the … | opens modal first |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Hold order (secondary button) | `holdOrder` POST `/orders/{orderId}/hold` | inline | Order | 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem) | opens modal first |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | opens modal first; produces a document or message: Reprint or resend tickets |
| Reschedule order (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |
| Resume order (secondary button) | `resumeOrder` POST `/orders/{orderId}/resume` | — | OrderResumeResult | 409 Held order expired (`holdExpired`), or already resumed at another till (`alreadyResumed`). (OrderRefusedProblem) | — |
| Void order (destructive button) | `voidOrder` POST `/orders/{orderId}/voids` | inline | Order | 409 Settled — a payment on the order has been `captured`, so the money has moved (`alreadySettled`) — or taken in a shift that is now closed (`shiftClosed`). (OrderRefusedProblem) | — |

**Data it reads**: `listOrders` (onLoad, List orders); `getRefundPolicy` (onLoad, The policy this refund is judged against); `listCreditMemos` (onLoad, List credit memos); `getTaxDocumentRendition` (onLoad, Download the invoice / credit memo PDF)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `BO-004` Manual Wait Time Entry: *Authorises the bulk refund*; carries `refundId`

**What opens over it**

- confirmDialog *Void order*: **Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A refunds exchanges this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The refunds exchanges list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the refunds exchanges untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No refunds exchanges yet. Offers Create refund (`createRefund`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listOrderRefunds` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listOrderRefunds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 Held order expired … |

#### Permissions

- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `createRefund` → `ORDER_REFUND` (operate) · staff, partner
- `applyManualDiscount` → `ORDER_DISCOUNT` (operate) · staff, partner
- `createOrder` → `ORDER_CREATE` (operate) · staff, guest, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `holdOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `resumeOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner
- `getRefundPolicy` → `ORDER_VIEW` (read) · staff
- `issueCreditMemo` → `LEDGER_POST` (operate) · staff, service
- `listCreditMemos` → `LEDGER_VIEW` (read) · staff, guest
- `getTaxDocumentRendition` → `LEDGER_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listOrderRefunds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

71 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.12.3 | The system provide the ability for cashiers to issue refund up to a certain value with another user (cashier or supervisor) putting in their name as an audit control. | Ticketing Sales | CONTRACTED | `createRefund` |
| 2.12.13 | The system should change ticket status to Refunded after the Refund transaction is posted. Refund transaction should be linked with the ticket identifier to allow for reconciliation. There should be … | Ticketing Sales | CONTRACTED | `createRefund` |
| 4.2.3 | The system should be able to manually adjust the price of items in a transaction and make sure that these are reflected in the promotion discount | Bundles and Promotions | CONTRACTED | `applyManualDiscount` |
| 2.1.6 | This system should provide a Ticketing POS solution that enables the operator to sell all the tickets defined in the system including multi-day and combo tickets. The POS solution must also support … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.29 | The system should be able to offer ticket sales to various outside business entities through the use of the exposed APIs and dedicated modules. Examples of typical clients that would have discounts … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.30 | The system should cater to multiple ways of enabling B2B clients, resellers and partner distribution channels to resell tickets and services offered by the client: - Web-based solution for B2B … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.8.1 | The system should provide an application for call center agents to make new ticket purchases, modify existing ticket purchases and offer refunds for guests. Any modifications done should follow the … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.8.2 | The system should allow call center agents to: - Make ticket sales including individual seat selection. - Look up existing orders after guest verification. - Change demographic data on existing … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.12.25 | Each order has a unique number. | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.11.11 | The system should correctly allocate the upgrade transaction to the sales channel it was processed on. Upgrade sales channel can be different from the purchase sales channel. | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.13.5 | In addition to this, some B2B customers may have direct access via API. | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.14.6 | The Annual pass can be bought at the Guest Service or at front gate. | Ticketing Sales | CONTRACTED | `createOrder` |
| … 59 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Online/app returns: customer submits a return request with a reason (and photo if applicable) → approval team → courier pickup → refund after verified receipt. Confirmed: an item bought at the POS can also be returned via the web portal, subject to approval. *(agreed · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online; 5. Key Decisions · DI-367)*
- Bulk refunds: select and refund at event or date level (e.g. ~5,000 transactions for a cancelled event), online and on-site bookings, with one approval step before processing. *(agreed · MoM 12 Aug 2026, 18. Bulk Refund Processing and Refund Requests · DI-269)*
- Refunds use preset time-banded percentages (e.g. full refund a set number of days before the event, less closer to/after it), support partial refunds, and let an authorised approver apply a custom override percentage. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-252)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-023` · status **notStarted** · provenance generated
- Flow F09 *Event is cancelled and refunded*, step 3: Reviews the refund exposure → How many orders, how much money, how many across other venues
- Flow F09 branch at step 3 (requiresStaff): when Refund exceeds the manager threshold, Requires a second approver. CF-36 put the threshold at venue level.

#### Acceptance for the design

- [ ] Every input above is drawn (121), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (71 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create refund, Apply manual discount, Create order, Exchange order lines, Hold order, Modify order, Reprint order, Reschedule order, Resume order, Void order.
- [ ] Every transition is wired: `BO-008`, `BO-004`.
- [ ] Every gated control is gated: `LEDGER_POST`, `LEDGER_VIEW`, `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-024` Payment Exceptions

**Resolve payments that never resolved themselves.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_POST`, `ORDER_CREATE`, `ORDER_MODIFY`, `SHIFT_CLOSE` (4 operate); in the flows as cashier, finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`createPayment`, `addTip`, `capturePayment`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `paymentId` (deepLink), `depositId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/payment-exceptions` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Payment exceptions across currencies. **The rate shown is the one stored on the payment, not today's** (CF-37) — an exception opened in March and worked in August is worked at March's rate, or the reconciliation will never close.

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

**Form: Settle deposit** (modal, opened by *Settle deposit*; *Settle deposit* calls `settleDeposit`, *Cancel* sends nothing)

**Collects what `settleDeposit` sends before it is called.** Required: `outcome`. Optional: `amount`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Convert to revenue · Return · Forfeit · Partial forfeit | — | — | `settleDeposit` body |
| Amount `amount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | The part kept as income. Required for `partialForfeit`, ignored otherwise. | `settleDeposit` body |
| Reason `reason` | text area | optional | — | — | — | — | `settleDeposit` body |

Errors to draw in the form: 400 `partialForfeit` without an `amount`, or with one that is not above zero and below the deposit, or in another currency.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The deposit is not `held` (it has already been settled), or a forfeit was asked for while the deposit is still refundable.

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

**Sent by *Close deposit boxes*** (`closeDepositBoxes`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Boxs `boxIds` | multi-picker: choose boxs | optional | — | — | — | — | `closeDepositBoxes` body |
| All open at venue `allOpenAtVenue` | toggle | optional | — | — | — | — | `closeDepositBoxes` body |
| Counts `counts` | repeatable rows | required | — | Omitting a box that needs one is refused with 422 `deposit-box-count-missing`. | — | One count per box being closed that has traded (audit R123 (4)). Omitting a box that needs one is refused with 422 `deposit-box-count-missing`. | `closeDepositBoxes` body |
| Box `counts[].boxId` | picker: choose a box | required | — | — | shows names, sends the id | — | `closeDepositBoxes` body |
| Counted total `counts[].countedTotal` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeDepositBoxes` body |
| Counted denominations `counts[].countedDenominations` | repeatable rows | optional | — | at least 1 | — | A count is a list of lines and the line is the row. Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — … | `closeDepositBoxes` body |
| ID `counts[].countedDenominations[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `closeDepositBoxes` body |
| Shift `counts[].countedDenominations[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `closeDepositBoxes` body |
| Deposit box `counts[].countedDenominations[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `closeDepositBoxes` body |
| Count kind `counts[].countedDenominations[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `closeDepositBoxes` body |
| Cash movement `counts[].countedDenominations[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `closeDepositBoxes` body |
| Denomination `counts[].countedDenominations[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `closeDepositBoxes` body |
| Counted quantity `counts[].countedDenominations[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `closeDepositBoxes` body |
| Counted value `counts[].countedDenominations[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `closeDepositBoxes` body |
| Counted by `counts[].countedDenominations[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `closeDepositBoxes` body |
| Counted at `counts[].countedDenominations[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `closeDepositBoxes` body |
| Recount of `counts[].countedDenominations[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `closeDepositBoxes` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create payment (primary button) | `createPayment` POST `/payments` | CreatePaymentRequest | Payment | 402 Declined by the provider (`providerDeclined`). (PaymentProblem); 409 Tender unavailable offline (`tenderUnavailableOffline`), amount exceeds the balance due (`exceedsBalanceDue`), or a guest channel sent a tender … | emits `payment.captured`, `order.paid` |
| Add tip (secondary button) | `addTip` POST `/payments/{paymentId}/tip` | inline | Payment | 409 Payment not settled — not yet `captured` (`notCaptured`) — or a tip is already recorded against it (`tipAlreadyRecorded`). (PaymentProblem) | opens modal first |
| Capture payment (secondary button) | `capturePayment` POST `/payments/{paymentId}/capture` | inline | Payment | 402 Capture refused by the issuer (`providerDeclined`); the payment moves to `declined` (states/payment.yaml). (PaymentProblem); 409 Only an `authorised` payment is captured (`notAuthorised`). The amount may not exceed … | emits `payment.captured`, `order.paid`; opens modal first |
| Inquire payment status (secondary button) | `inquirePaymentStatus` POST `/payments/{paymentId}/inquiry` | — | Payment | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Close deposit boxes (destructive button) | `closeDepositBoxes` POST `/deposit-boxes/close` | inline | DepositBox[] | 422 A box being closed has no entry in `counts`, or its entry has neither a total nor a denomination count (problem type `deposit-box-count-missing`, audit R123 … | — |
| Settle deposit (secondary button) | `settleDeposit` POST `/deposits/{depositId}/settle` | inline | Deposit | 400 `partialForfeit` without an `amount`, or with one that is not above zero and below the deposit, or in another currency.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in … | opens modal first |

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `PTR-014` Settlement & Payment History: *Settlement & Payment History*

**What opens over it**

- confirmDialog *Close deposit boxes*: **Names what `closeDepositBoxes` changes and what it leaves alone**, in the consequence rather than the verb. A payment exceptions this affects should be identified in the dialog, not just counted. **Collects what `closeDepositBoxes` sends before it is called.** Nothing in the body is required. …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved payment exceptions. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment exceptions untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment exceptions configured. The form opens empty and `createPayment` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_CREATE`, which `createPayment` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `partialForfeit` without an `amount`, or with one that is not above zero and below the deposit, or in another currency.; 409 Only an `authorised` payment is captured (`notAuthorised`). The amount may not exceed what was authorised (`aboveAuthorisedAmount`), and less than that is … (PaymentProblem); 409 Payment not settled — not yet `captured` (`notCaptured`) — or a tip is already recorded … |

#### Permissions

- `createPayment` → `ORDER_CREATE` (operate) · staff, guest, partner
- `addTip` → `ORDER_MODIFY` (operate) · staff, partner
- `capturePayment` → `ORDER_CREATE` (operate) · staff, partner
- `inquirePaymentStatus` → `ORDER_CREATE` (operate) · staff, guest, partner
- `closeDepositBoxes` → `SHIFT_CLOSE` (operate) · staff
- `settleDeposit` → `LEDGER_POST` (operate) · staff, service

**A refused user sees:** Shown when the caller lacks `ORDER_CREATE`, which `createPayment` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 5.8.6 | The system should allow automated close out of one or more deposit boxes. | F&B & Guest Management | CONTRACTED | `closeDepositBoxes` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-024` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 3.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 3.dc.html#ret-3k`
- Flow F32 *A till opens, trades and settles*, step 8: The supervisor reviews the shift and the deposit reconciles. → Cash to the safe, shift `closed`, and the ledger posted. **`shift` writes `ledger.posting` here** — a till closing is a ledger act, which is why that cross-contract write is correct.
- Flow F99 *A chargeback arrives and is defended*, step 2: Payment Exceptions. → 6 operations, 0 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (45), with its required mark, default, format and its error state (400, 402, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-024?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create payment, Add tip, Capture payment, Inquire payment status, Close deposit boxes, Settle deposit.
- [ ] Every transition is wired: `BO-008`, `PTR-014`.
- [ ] Every gated control is gated: `LEDGER_POST`, `ORDER_CREATE`, `ORDER_MODIFY`, `SHIFT_CLOSE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-025` Chargebacks & Disputes

**Answer the acquirer with the evidence attached.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_REFUND_APPROVE`, `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW` (2 operate, 1 read); in the flows as finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSettlementExceptions` reads the population and `getSettlement` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `settlementId` (deepLink), `chargebackId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/chargebacks-disputes` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Provider name | text field | — | — | `listSettlements` ?providerName |
| Status | select | — | Ingesting · Parsing · Matching · Matched · Has exceptions · Resolved · Failed | `listSettlements` ?status |
| Period from | date picker | — | — | `getChargebackAnalytics` ?periodFrom |
| Period to | date picker | — | — | `getChargebackAnalytics` ?periodTo |
| Group by | select | Reason | Reason · Provider · Outcome · Venue · Month · Product · Product category · Customer | `getChargebackAnalytics` ?groupBy |
| Min chargebacks | number field | — | min 1 | `getChargebackAnalytics` ?minChargebacks |
| Product | picker: choose a product | — | — | `getChargebackAnalytics` ?productId |
| Provider | picker: choose a provider | — | — | `getChargebackAnalytics` ?providerId |
| Period from | date picker | — | — | `getChargebackAnalytics` ?periodFrom |
| Period to | date picker | — | — | `getChargebackAnalytics` ?periodTo |
| Group by | select | Reason | Reason · Provider · Outcome · Venue · Month · Product · Product category · Customer | `getChargebackAnalytics` ?groupBy |
| Min chargebacks | number field | — | min 1 | `getChargebackAnalytics` ?minChargebacks |
| Product | picker: choose a product | — | — | `getChargebackAnalytics` ?productId |
| Provider | picker: choose a provider | — | — | `getChargebackAnalytics` ?providerId |

**Form: Resolve settlement exception** (modal, opened by *Resolve settlement exception*; *Resolve settlement exception* calls `resolveSettlementException`, *Cancel* sends nothing)

**Collects what `resolveSettlementException` sends before it is called.** Required: `exceptionId`, `resolution`, `note`. Optional: `matchedPaymentId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Exception `exceptionId` | picker: choose an exception | required | — | — | shows names, sends the id | — | `resolveSettlementException` body |
| Resolution `resolution` | radio group | required | — | Matched manually · Write off · Dispute raised · Provider error · Timing difference | — | How a settlement exception was explained. One vocabulary for the request and the stored exception. | `resolveSettlementException` body |
| Matched payment `matchedPaymentId` | picker: choose a matched payment | optional | — | — | shows names, sends the id | — | `resolveSettlementException` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `resolveSettlementException` body |

Errors to draw in the form: 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 404 The settlement, or an exception with this `exceptionId` under it, does not exist or is outside the caller's scope.; 409 The exception is already resolved.

**Form: Ingest settlement file** (modal, opened by *Ingest settlement file*; *Ingest settlement file* calls `ingestSettlementFile`, *Cancel* sends nothing)

**Collects what `ingestSettlementFile` sends before it is called.** Required: `providerName`, `periodStart`, `periodEnd`, `fileReference`. Optional: `format`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Provider name `providerName` | text field | required | — | — | — | — | `ingestSettlementFile` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | The venue this day of settlement is for (audit R110 (b)). | `ingestSettlementFile` body |
| Period start `periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | A day in the region's time zone, local midnight to local midnight. | `ingestSettlementFile` body |
| Period end `periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | A day in the region's time zone, local midnight to local midnight. | `ingestSettlementFile` body |
| File reference `fileReference` | picker: choose a file reference | required | — | That upload route is staff-only and needs `ASSET_LIBRARY_MANAGE`; a partner caller has no upload route yet. | shows names, sends the id | The `id` of the `MediaAsset` holding the file, uploaded first through `assets.createUpload` then `assets.completeUpload` (direct to object storage through a signed URL). | `ingestSettlementFile` body |
| Format `format` | radio group | optional | — | Csv · Fixed width · Xml · Json | — | — | `ingestSettlementFile` body |

Errors to draw in the form: 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)).

#### Outputs: what the screen shows and produces

**Shown**

**Every settlement exception** (data table, from `listSettlementExceptions`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-created when parsing finds the exception, so a UUID (naming-and-style 4). |
| Settlement | the name it points at, never the id | — |
| Kind | chip: Unmatched in provider, Unmatched in ledger, Amount mismatch, Duplicate in provider … | — |
| Provider reference | text | — |
| Payment | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expected amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Resolution | chip: Matched manually, Write off, Dispute raised, Provider error, Timing difference | Null while the exception is open. |
| Resolved by principal | the name it points at, never the id | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**Every settlement** (data table, from `listSettlements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Currency code | text | A settlement has no account, so nothing else denominates it. A posting takes its currency from `ledger.account.currency` and a payment from … |
| Provider name | text | — |
| Period start | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Period end | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| File reference | the name it points at, never the id | The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. Kept on the row because parsing is asynchronous: the job … |
| Format | chip: Csv, Fixed width, Xml, Json | The file format given at ingest. Null when none was given. |
| Status | chip: Ingesting, Parsing, Matching, Matched, Has exceptions, Resolved… | — |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |
| Provider gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**The selected settlement exception** (detail panel, from `listSettlementExceptions`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-created when parsing finds the exception, so a UUID (naming-and-style 4). |
| Settlement | the name it points at, never the id | — |
| Kind | chip: Unmatched in provider, Unmatched in ledger, Amount mismatch, Duplicate in provider … | — |
| Provider reference | text | — |
| Payment | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expected amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Resolution | chip: Matched manually, Write off, Dispute raised, Provider error, Timing difference | Null while the exception is open. |
| Note | text | The `note` given to `resolveSettlementException`, stored with the resolution. |
| Resolved by principal | the name it points at, never the id | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**The settlement** (detail panel, from `getSettlement`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Currency code | text | A settlement has no account, so nothing else denominates it. A posting takes its currency from `ledger.account.currency` and a payment from … |
| Provider name | text | — |
| Period start | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Period end | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| File reference | the name it points at, never the id | The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. Kept on the row because parsing is asynchronous: the job … |
| Format | chip: Csv, Fixed width, Xml, Json | The file format given at ingest. Null when none was given. |
| Status | chip: Ingesting, Parsing, Matching, Matched, Has exceptions, Resolved… | — |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |
| Provider gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Provider fees | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Provider net | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Ledger gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Difference | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Resolve settlement exception (primary button) | `resolveSettlementException` POST `/settlements/{settlementId}/exceptions` | inline | SettlementException | 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 404 The settlement, or an exception with this `exceptionId` under it, does not exist or is outside the … | opens modal first |
| Ingest settlement file (secondary button) | `ingestSettlementFile` POST `/settlements` | inline | Settlement | 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)). | opens modal first |

**Data it reads**: `listSettlements` (onLoad, List settlement batches); `getChargebackAnalytics` (onLoad, Chargeback analytics panel); `getChargebackAnalytics` (onLoad, Chargeback rate by reason, product and customer)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `BO-024` Payment Exceptions: *Payment Exceptions*; carries `paymentId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The chargebacks disputes list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the chargebacks disputes untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No chargebacks disputes yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSettlementExceptions` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SETTLEMENT_VIEW`, which `listSettlementExceptions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)).; 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 409 The case already has an outcome, or was `accepted` by the venue (a conceded case cannot be won), or the fiscal period for the … |

#### Permissions

- `listSettlementExceptions` → `SETTLEMENT_VIEW` (read) · staff, partner
- `resolveSettlementException` → `SETTLEMENT_RECONCILE` (operate) · staff, partner
- `getSettlement` → `SETTLEMENT_VIEW` (read) · staff, partner
- `ingestSettlementFile` → `SETTLEMENT_RECONCILE` (operate) · staff, partner
- `listSettlements` → `SETTLEMENT_VIEW` (read) · staff, partner
- `recordChargeback` → `ORDER_REFUND_APPROVE` (operate) · staff, service
- `assignChargeback` → `ORDER_REFUND_APPROVE` (operate) · staff
- `recordChargebackOutcome` → `ORDER_REFUND_APPROVE` (operate) · staff, service
- `getChargebackAnalytics` → `ORDER_REFUND_APPROVE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `SETTLEMENT_VIEW`, which `listSettlementExceptions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.92 | The system shall support chargeback notification handling, dispute management, evidence collection, investigation workflows, resolution tracking, and financial adjustments. Track chargeback status … | F&B & Guest Management | CONTRACTED | `recordChargeback` |
| 8.3.11 | System shall identify transactions with elevated chargeback risk. | Unified Operations Dashboard | CONTRACTED | `recordChargeback` |
| 4.2.21 | The system shall provide tools for tracking chargebacks, managing disputes, storing evidence, monitoring resolution status, and generating chargeback analytics. | Bundles and Promotions | CONTRACTED | `getChargebackAnalytics` |
| 8.3.12 | System shall identify customers with repeated chargebacks. | Unified Operations Dashboard | CONTRACTED | `getChargebackAnalytics` |
| 8.3.13 | System shall identify products with elevated chargeback rates. | Unified Operations Dashboard | CONTRACTED | `getChargebackAnalytics` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-025` · status **notStarted** · provenance generated
- Flow F99 *A chargeback arrives and is defended*, step 1: Chargebacks & Disputes. → 5 operations, 5 of them previously unwalked.
- Flow F99 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.
- ADR-0033 *Every asynchronous handoff has an outbox and a place to fail* (`docs/adr/0033-outbox-and-dead-letters.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (49 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-025?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Resolve settlement exception, Ingest settlement file.
- [ ] Every transition is wired: `BO-008`, `BO-024`.
- [ ] Every gated control is gated: `ORDER_REFUND_APPROVE`, `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-026` Group Bookings

**Handle a booking that arrives as a school, not a guest.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`… (8 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `orderId` (deepLink), `groupBookingId` (navigation) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/venue-operations/group-bookings` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 31 August** — `Seat Platform Board 7.dc.html` frame `seatp-7e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Group Booking* matched at 0.96. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listOrders`. | `listOrders` ?venueId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listOrders`. | `listOrders` ?principalId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listOrders`. | `listOrders` ?shiftId |
| Status | select | optional | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | — | Sends `?status=` to `listOrders`. | `listOrders` ?status |
| Created from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdFrom=` to `listOrders`. | `listOrders` ?createdFrom |
| Created to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdTo=` to `listOrders`. | `listOrders` ?createdTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

**Form: Create group booking** (modal, opened by *Create group booking*; *Create group booking* calls `createGroupBooking`, *Cancel* sends nothing)

**Collects what `createGroupBooking` sends before it is called.** Required: `orderId`, `leaderSubjectId`, `expectedSize`. Optional: `kind`, `packageProductId`, `yearGroup`, `accessAndDietaryNeeds`, `celebrantName`, `celebrantTurningAge`, `allergiesAndRequests`, `finalHeadcountDueBy`, `organisationName`, `minimumSize`, `attendeeCaptureRequired`, `attendeeCaptureDueBy`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Group quote `groupQuoteId` | picker: choose a group quote | optional | — | — | shows names, sends the id | The quote this booking converts (BO-272). Must be the current version and `sent` or `accepted`; conversion sets its `groupBookingId` and moves a `sent` quote to `accepted` … | `createGroupBooking` body |
| Kind `kind` | radio group | optional | General | General · School · Corporate · Party | — | — | `createGroupBooking` body |
| Package product `packageProductId` | text field | optional | — | — | — | The school-trip format or party package. | `createGroupBooking` body |
| Year group `yearGroup` | text field | optional | — | max length 40 | — | — | `createGroupBooking` body |
| Access and dietary needs `accessAndDietaryNeeds` | text area | optional | — | max length 1000 | — | — | `createGroupBooking` body |
| Celebrant name `celebrantName` | text field | optional | — | max length 120 | — | The birthday child. | `createGroupBooking` body |
| Celebrant turning age `celebrantTurningAge` | stepper or slider | optional | — | min 1; max 18 | — | — | `createGroupBooking` body |
| Allergies and requests `allergiesAndRequests` | text area | optional | — | max length 1000 | — | — | `createGroupBooking` body |
| Final headcount due by `finalHeadcountDueBy` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGroupBooking` body |
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createGroupBooking` body |
| Leader subject `leaderSubjectId` | picker: choose a leader subject | required | — | — | shows names, sends the id | The person who pays, is called if the coach is late, and collects the names. | `createGroupBooking` body |
| Organisation name `organisationName` | text field | optional | — | max length 200 | — | — | `createGroupBooking` body |
| Expected size `expectedSize` | number field | required | — | min 2 | — | — | `createGroupBooking` body |
| Minimum size `minimumSize` | number field | optional | — | min 1 | — | — | `createGroupBooking` body |
| Attendee capture required `attendeeCaptureRequired` | toggle | optional | off | — | — | — | `createGroupBooking` body |
| Attendee capture due by `attendeeCaptureDueBy` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGroupBooking` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The order already has a group booking (`orderAlreadyGrouped`), or is voided (`orderVoided`), or `groupQuoteId` names a quote that cannot be converted … (GroupBookingProblem)

**Form: Save group booking** (modal, opened by *Save group booking*; *Save group booking* calls `updateGroupBooking`, *Cancel* sends nothing)

**Collects what `updateGroupBooking` sends before it is called.** Nothing in the body is required. Optional: `packageProductId`, `yearGroup`, `accessAndDietaryNeeds`, `celebrantName`, `celebrantTurningAge`, `allergiesAndRequests`, `finalHeadcountDueBy`, `leaderSubjectId`, `organisationName`, `expectedSize`, `confirmedSize`, `minimumSize` and 3 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Package product `packageProductId` | text field | optional | — | — | — | The school-trip format or party package. | `updateGroupBooking` body |
| Year group `yearGroup` | text field | optional | — | max length 40 | — | — | `updateGroupBooking` body |
| Access and dietary needs `accessAndDietaryNeeds` | text area | optional | — | max length 1000 | — | — | `updateGroupBooking` body |
| Celebrant name `celebrantName` | text field | optional | — | max length 120 | — | The birthday child. | `updateGroupBooking` body |
| Celebrant turning age `celebrantTurningAge` | stepper or slider | optional | — | min 1; max 18 | — | — | `updateGroupBooking` body |
| Allergies and requests `allergiesAndRequests` | text area | optional | — | max length 1000 | — | — | `updateGroupBooking` body |
| Final headcount due by `finalHeadcountDueBy` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateGroupBooking` body |
| Leader subject `leaderSubjectId` | picker: choose a leader subject | optional | — | — | shows names, sends the id | — | `updateGroupBooking` body |
| Organisation name `organisationName` | text field | optional | — | max length 200 | — | — | `updateGroupBooking` body |
| Expected size `expectedSize` | number field | optional | — | min 2 | — | — | `updateGroupBooking` body |
| Confirmed size `confirmedSize` | number field | optional | — | min 0 | — | — | `updateGroupBooking` body |
| Minimum size `minimumSize` | number field | optional | — | min 1 | — | — | `updateGroupBooking` body |
| Attendee capture required `attendeeCaptureRequired` | toggle | optional | — | — | — | — | `updateGroupBooking` body |
| Attendee capture due by `attendeeCaptureDueBy` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateGroupBooking` body |
| Status `status` | radio group | optional | — | Confirmed · Names pending · Complete · Cancelled | — | — | `updateGroupBooking` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The status change goes backwards (`statusBackwards`), or the group is already cancelled or complete (`groupClosed`). (GroupBookingProblem); 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Create order** (modal, opened by *Create order*; *Create order* calls `createOrder`, *Cancel* sends nothing)

**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `createOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createOrder` body |
| Channel `channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createOrder` body |
| Shift `shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `createOrder` body |
| Guest link `guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `createOrder` body |
| Catalogue bundle version `catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `createOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `createOrder` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createOrder` body |
| Recommendation `lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `createOrder` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Booked window `lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `createOrder` body |
| Starts at `lines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |
| Ends at `lines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `createOrder` body |
| Inventory hold `lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `createOrder` body |
| Seats `lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `createOrder` body |
| Resource hold `lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `createOrder` body |
| Attributes `lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `createOrder` body |
| Transport `lines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `createOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createOrder` body |
| Eligibility declaration `lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `createOrder` body |
| Age band `lines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `createOrder` body |
| Age years `lines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `createOrder` body |
| Height band index `lines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `createOrder` body |
| Confident swimmer `lines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `createOrder` body |
| Guardian signed `lines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `createOrder` body |
| Quoted unit price `lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `createOrder` body |
| Holder name `lines[].holderName` | text field | optional | — | — | — | — | `createOrder` body |
| Data mask values `lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `createOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 422 More seats for one performance than the channel allows (`seatLimitExceeded`, decided 29 September, rev 3 REV3-7). (OrderRefusedProblem)

**Form: Apply manual discount** (modal, opened by *Apply manual discount*; *Apply manual discount* calls `applyManualDiscount`, *Cancel* sends nothing)

**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header. | `applyManualDiscount` body |
| Line `lineId` | picker: choose a line | optional | — | — | shows names, sends the id | Omit to discount the order rather than a line. | `applyManualDiscount` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `applyManualDiscount` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `applyManualDiscount` body |
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything. | `applyManualDiscount` body |
| Reason code `reasonCode` | text field | optional | — | — | — | Optional alongside the free text, where the venue maintains a list. | `applyManualDiscount` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required above the venue threshold. May not be the requester. | `applyManualDiscount` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyManualDiscount` body |

Errors to draw in the form: 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem)

**Form: Create refund** (modal, opened by *Create refund*; *Create refund* calls `createRefund`, *Cancel* sends nothing)

**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header. | `createRefund` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to refund the whole order. | `createRefund` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createRefund` body |
| Secondary authorisation `secondaryAuthorisation` | group | optional | — | — | — | Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. | `createRefund` body |
| Principal `secondaryAuthorisation.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRefund` body |
| Credential `secondaryAuthorisation.credential` | text area | required | — | max length 512 | — | The second person's staff PIN, as they sign in at a till with it. A PIN, never a password (decided 28 September, audit R123 (7)). | `createRefund` body |
| Refund to original tender `refundToOriginalTender` | toggle | optional | on | — | — | — | `createRefund` body |
| Alternate tender `alternateTender` | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createRefund` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRefund` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount exceeds what remains … (RefundPolicyProblem)

**Form: Exchange order lines** (modal, opened by *Exchange order lines*; *Exchange order lines* calls `exchangeOrderLines`, *Cancel* sends nothing)

**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header. | `exchangeOrderLines` body |
| Outgoing lines `outgoingLineIds` | multi-picker: choose outgoing lines | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| Incoming lines `incomingLines` | repeatable rows | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| ID `incomingLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `exchangeOrderLines` body |
| Variant `incomingLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Recommendation `incomingLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `exchangeOrderLines` body |
| Performance `incomingLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Booked window `incomingLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `exchangeOrderLines` body |
| Starts at `incomingLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |
| Ends at `incomingLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `exchangeOrderLines` body |
| Inventory hold `incomingLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `exchangeOrderLines` body |
| Seats `incomingLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `exchangeOrderLines` body |
| Resource hold `incomingLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `exchangeOrderLines` body |
| Attributes `incomingLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `exchangeOrderLines` body |
| Transport `incomingLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `exchangeOrderLines` body |
| Quantity `incomingLines[].quantity` | number field | required | — | min 1 | — | — | `exchangeOrderLines` body |
| Eligibility declaration `incomingLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `exchangeOrderLines` body |
| Age band `incomingLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `exchangeOrderLines` body |
| Age years `incomingLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Height band index `incomingLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Confident swimmer `incomingLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `exchangeOrderLines` body |
| Guardian signed `incomingLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `exchangeOrderLines` body |
| Quoted unit price `incomingLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `exchangeOrderLines` body |
| Holder name `incomingLines[].holderName` | text field | optional | — | — | — | — | `exchangeOrderLines` body |
| Data mask values `incomingLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `exchangeOrderLines` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `exchangeOrderLines` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `exchangeOrderLines` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |

Errors to draw in the form: 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem)

**Form: Hold order** (modal, opened by *Hold order*; *Hold order* calls `holdOrder`, *Cancel* sends nothing)

**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Label `label` | text field | optional | — | max length 60 | — | How the cashier will find it again — a name, a description, a party size. A list of unlabelled parked sales is unusable at a busy counter. | `holdOrder` body |
| Hold until `holdUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |

Errors to draw in the form: 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem)

**Form: Modify order** (modal, opened by *Modify order*; *Modify order* calls `modifyOrder`, *Cancel* sends nothing)

**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this modification, not of the order — the order is the path's `orderId`. | `modifyOrder` body |
| Add lines `addLines` | repeatable rows | optional | — | — | — | — | `modifyOrder` body |
| ID `addLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `modifyOrder` body |
| Variant `addLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `modifyOrder` body |
| Recommendation `addLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `modifyOrder` body |
| Performance `addLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `modifyOrder` body |
| Booked window `addLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `modifyOrder` body |
| Starts at `addLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |
| Ends at `addLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `modifyOrder` body |
| Inventory hold `addLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `modifyOrder` body |
| Seats `addLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `modifyOrder` body |
| Resource hold `addLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `modifyOrder` body |
| Attributes `addLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `modifyOrder` body |
| Transport `addLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `modifyOrder` body |
| Quantity `addLines[].quantity` | number field | required | — | min 1 | — | — | `modifyOrder` body |
| Eligibility declaration `addLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `modifyOrder` body |
| Age band `addLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `modifyOrder` body |
| Age years `addLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `modifyOrder` body |
| Height band index `addLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `modifyOrder` body |
| Confident swimmer `addLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `modifyOrder` body |
| Guardian signed `addLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `modifyOrder` body |
| Quoted unit price `addLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `modifyOrder` body |
| Holder name `addLines[].holderName` | text field | optional | — | — | — | — | `modifyOrder` body |
| Data mask values `addLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `modifyOrder` body |
| Remove lines `removeLineIds` | multi-picker: choose remove lines | optional | — | — | — | — | `modifyOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `modifyOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |

Errors to draw in the form: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem)

**Form: Reprint order** (modal, opened by *Reprint order*; *Reprint order* calls `reprintOrder`, *Cancel* sends nothing)

**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delivery `delivery` | radio group | required | — | Print · Email · SMS · Whatsapp · Wallet | — | — | `reprintOrder` body |
| Destination `destination` | text field | optional | — | — | — | — | `reprintOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to reprint every line. | `reprintOrder` body |
| Reason `reason` | radio group | optional | — | Printer fault · Guest request · Lost ticket · Not received · Other | — | — | `reprintOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the till reprinted — device time, as for every offline-capable write. | `reprintOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Reschedule order** (modal, opened by *Reschedule order*; *Reschedule order* calls `rescheduleOrder`, *Cancel* sends nothing)

**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target performance `targetPerformanceId` | picker: choose a target performance | required | — | — | shows names, sends the id | — | `rescheduleOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to move the whole order. | `rescheduleOrder` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `rescheduleOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `rescheduleOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rescheduleOrder` body |

Errors to draw in the form: 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem)

**Sent by *Void order*** (`voidOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this void, and its idempotency key — it must equal the `Idempotency-Key` header. | `voidOrder` body |
| Reason `reason` | select | required | — | Guest changed mind · Entered in error · Item unavailable · Quality issue · Duplicate · Other | — | The void reason list (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. | `voidOrder` body |
| Note `note` | text area | optional | — | min length 3; max length 500; Required when `reason` is `other` (audit R222); optional otherwise. | — | Required when `reason` is `other` (audit R222); optional otherwise. | `voidOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `voidOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own. |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**The group booking** (detail panel, from `getGroupBooking`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: General, School, Corporate, Party | — |
| Package product | text | The school-trip format or party package. |
| Year group | text | — |
| Access and dietary needs | text | — |
| Celebrant name | text | The birthday child. |
| Celebrant turning age | 1,234 | — |
| Allergies and requests | text | — |
| Final headcount due by | 1 Oct 2026, 14:30 | — |
| Quote sent at | 1 Oct 2026, 14:30 | — |
| Risk assessment sent at | 1 Oct 2026, 14:30 | — |
| Preferred date | 1 Oct 2026 | The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. |
| Order | the name it points at, never the id | — |
| Leader subject | the name it points at, never the id | — |
| Organisation name | text | — |
| Expected size | 1,234 | — |

**The order statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order | the name it points at, never the id | — |
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Entries | list or chips (count when long) | Sequential. What an agent reads to a guest asking about a charge. |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |
| Lines | list or chips (count when long) | — |
| Payments | list or chips (count when long) | — |
| Principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create order (primary button) | `createOrder` POST `/orders` | CreateOrderRequest | Order | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the … | opens modal first |
| Apply manual discount (secondary button) | `applyManualDiscount` POST `/orders/{orderId}/discounts` | ManualDiscountRequest | Order | 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem) | opens modal first |
| Create refund (secondary button) | `createRefund` POST `/orders/{orderId}/refunds` | CreateRefundRequest | Refund | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount … | opens modal first |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Hold order (secondary button) | `holdOrder` POST `/orders/{orderId}/hold` | inline | Order | 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem) | opens modal first |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | opens modal first; produces a document or message: Reprint or resend tickets |
| Reschedule order (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |
| Resume order (secondary button) | `resumeOrder` POST `/orders/{orderId}/resume` | — | OrderResumeResult | 409 Held order expired (`holdExpired`), or already resumed at another till (`alreadyResumed`). (OrderRefusedProblem) | — |
| Void order (destructive button) | `voidOrder` POST `/orders/{orderId}/voids` | inline | Order | 409 Settled — a payment on the order has been `captured`, so the money has moved (`alreadySettled`) — or taken in a shift that is now closed (`shiftClosed`). (OrderRefusedProblem) | — |
| Create group booking (secondary button) | `createGroupBooking` POST `/group-bookings` | CreateGroupBookingRequest | GroupBooking | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The order already has a group booking (`orderAlreadyGrouped`), or is voided (`orderVoided`), or `groupQuoteId` names a quote that … | opens modal first |
| Save group booking (secondary button) | `updateGroupBooking` PATCH `/group-bookings/{groupBookingId}` | UpdateGroupBookingRequest | GroupBooking | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The status change goes backwards … | opens modal first |

**Data it reads**: `listOrders` (onLoad, List orders)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

**What opens over it**

- confirmDialog *Void order*: **Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A group bookings this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is the …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group bookings list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group bookings untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group bookings yet. Offers Create group booking (`createGroupBooking`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the group bookings are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getGroupBooking` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 Held order expired … |

#### Permissions

- `createGroupBooking` → `ORDER_CREATE` (operate) · staff
- `getGroupBooking` → `ORDER_VIEW` (read) · staff, guest
- `updateGroupBooking` → `ORDER_MODIFY` (operate) · staff
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `createOrder` → `ORDER_CREATE` (operate) · staff, guest, partner
- `applyManualDiscount` → `ORDER_DISCOUNT` (operate) · staff, partner
- `createRefund` → `ORDER_REFUND` (operate) · staff, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `holdOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `resumeOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getGroupBooking` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

77 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |
| 2.1.6 | This system should provide a Ticketing POS solution that enables the operator to sell all the tickets defined in the system including multi-day and combo tickets. The POS solution must also support … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.29 | The system should be able to offer ticket sales to various outside business entities through the use of the exposed APIs and dedicated modules. Examples of typical clients that would have discounts … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.30 | The system should cater to multiple ways of enabling B2B clients, resellers and partner distribution channels to resell tickets and services offered by the client: - Web-based solution for B2B … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.8.1 | The system should provide an application for call center agents to make new ticket purchases, modify existing ticket purchases and offer refunds for guests. Any modifications done should follow the … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.8.2 | The system should allow call center agents to: - Make ticket sales including individual seat selection. - Look up existing orders after guest verification. - Change demographic data on existing … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.12.25 | Each order has a unique number. | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.11.11 | The system should correctly allocate the upgrade transaction to the sales channel it was processed on. Upgrade sales channel can be different from the purchase sales channel. | Ticketing Sales | CONTRACTED | `createOrder` |
| … 65 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group bookings: one shared QR for the whole group (redeemed together at the counter) or one QR per person, each of which the guest can link to their own profile in the mobile app. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-289)*
- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-026` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Platform Board 7.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been …
- Derived from `wireframes/reference/Seat Platform Board 7.dc.html`
- Client design-board frames: `Seat Platform Board 7.dc.html#seatp-7e`

#### Acceptance for the design

- [ ] Every input above is drawn (158), with its required mark, default, format and its error state (400, 403, 404, 409, 412, 422).
- [ ] Every output is drawn (69 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-026?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create order, Apply manual discount, Create refund, Exchange order lines, Hold order, Modify order, Reprint order, Reschedule order, Resume order, Void order, Create group booking, Save group booking.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`, `ORDER_RESCHEDULE`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-027` Reissue & Media Replacement

**Replace media a guest has lost or damaged.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_VIEW`, `SCOPE_VIEW` (1 configure, 3 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getMediaEntitlements` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `mediaCode` (deepLink), `mediaId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/reissue-media-replacement` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **8 assets operations removed 18 August (CF-114).** The whole media contract was attached to this screen. **A till adding an item to a ticket does not manage a media library** — it reads the asset it needs and nothing else. Same shape as CF-87, one level up: that attached sibling operations, this attached a whole contract. **Absorbed BO-320 and BO-652 on 28 September (audit R276)**: Ticket Reissue & Fulfillment Regeneration brought `listTicketReissueFulfillment` (the reissue history of an order's tickets) and Credential Replacement & Reissue brought `listCredentialReplacementReissue` (lost, damaged and stolen credentials replaced); both are retired, and their hubs BO-314 and BO-644 open this screen.

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

**Form: Replace media asset** (modal, opened by *Replace media asset*; *Replace media asset* calls `replaceMediaAsset`, *Cancel* sends nothing)

**Collects what `replaceMediaAsset` sends before it is called.** Required: `uploadId`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Upload `uploadId` | picker: choose an upload | required | — | — | shows names, sends the id | — | `replaceMediaAsset` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `replaceMediaAsset` body |

Errors to draw in the form: 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem)

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

**Ticket reissues** (data table): Carried from BO-320 (merged 28 September, audit R276) — tickets and media regenerated after an amendment, correction, loss or delivery failure. **Cursor pagination, never offset.**

**Credential replacements** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows. Carried from BO-652 (merged 28 September, audit R276).

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Append entitlement to media (primary button) | `appendEntitlementToMedia` POST `/media/{mediaCode}/entitlements` | AppendEntitlementRequest | AppendEntitlementResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or … | opens modal first; produces a document or message: Add something to a ticket the guest already holds |
| Replace media asset (secondary button) | `replaceMediaAsset` POST `/media/{mediaId}/replace` | inline | MediaReplaceResult | 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem) | opens modal first |

**Data it reads**: `getMediaEntitlements` (onLoad, What is already on this media); `getMediaAsset` (onLoad, Read an asset with derivatives and usage); `listTicketReissueFulfillment` (onLoad, Ticket reissue and fulfilment regeneration history …); `listCredentialReplacementReissue` (onLoad, Credential replacement, reissue, revocation and recovery …)

**Where the user goes next**

- → `BO-314` Amendment & After-Sales Command Center: *Back to Amendment & After-Sales Command Center*
- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*
- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reissue media replacement, read by `getMediaEntitlements`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reissue media replacement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reissue media replacement yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | The ticket reissue or credential replacement history for this media has nothing matching; the media itself is still shown. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media … (AppendRefusedProblem); 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem) |

#### Permissions

- `getMediaEntitlements` → `ORDER_VIEW` (read) · staff
- `appendEntitlementToMedia` → `ORDER_CREATE` (operate) · staff
- `getMediaAsset` → `ASSET_LIBRARY_VIEW` (read) · staff
- `replaceMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `listTicketReissueFulfillment` → `ORDER_VIEW` (read) · staff
- `listCredentialReplacementReissue` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-027` · status **notStarted** · provenance generated
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 12: Works in Reissue & Media Replacement (Ticket Reissue & Fulfillment Regeneration, merged into it on 28 September, audit … → Manage ticket/media regeneration following an amendment, correction, loss, delivery failure, or other authorized event.
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 16: Works in Reissue & Media Replacement (Credential Replacement & Reissue, merged into it on 28 September, audit R276) → Securely manage lost, damaged, stolen or incorrectly issued credentials.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Append entitlement to media, Replace media asset.
- [ ] Every transition is wired: `BO-314`, `BO-644`, `BO-008`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_VIEW`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-028` Refund Approval Queue

**Approve the refunds a cashier is not allowed to make alone.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`createRefundRequest`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/refund-approval-queue` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Order id | text field | — | — | — | — | Required. | — |
| Reason | text field | — | — | — | — | Required. | — |
| Line ids | multi select | — | — | — | — | — | — |

**Sent by *Create refund request*** (`createRefundRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createRefundRequest` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | — | `createRefundRequest` body |
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `createRefundRequest` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create refund request (primary button) | `createRefundRequest` POST `/refund-requests` | inline | inline | 403 Authenticated but not permitted at the requested scope | — |

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Figures load; the expected total renders last |
| Error (`?state=error`) | **Could not load. Every action that moves money is blocked** — a figure nobody read must not be reconciled against |
| Empty, first run (`?state=emptyFirstRun`) | Nothing in the period — reported as a result, not an empty screen |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createRefundRequest` → no permission · guest

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.15 | Ticket Cancellation - System shall support ticket cancellation. | Guest Mobile App & Branding | CONTRACTED | `createRefundRequest` |
| 19.2.82 | Self-Service Refund Requests - System shall support self-service refund requests. | Guest Mobile App & Branding | CONTRACTED | `createRefundRequest` |
| 2.6.42 | Customer should be able to intiate refund tickets from the online portal | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.12 | The system should allow amendment and refunds (full or partial) based on ticket status (available, expired, etc.). This should be configurable. | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.15 | The system should be able to refund in different and multiple payment methods (example: System to allow refunds in cash for the tickets/bookings purchased through credit card). | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.18 | The system should provide the option to issue refund in the original mode of payment used by the guest or a different method of payment with supervisor override. Refund can also be offered as credits … | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 4.2.2 | The system should be able to refund transactions that contain promotions and ensure discounted amount is not refunded | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| 4.6.10 | The system to be able to refund in different and multiple payment methods. For example, system to allow refunds in cash or original payment methods. | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| 4.6.11 | The system should be able to accept foreign currency and offer refunds/negative sales in local currencies. | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| 5.5.24 | Support partial and full refunds while maintaining financial reconciliation. | F&B & Guest Management | CONTRACTED | `createRefundRequest` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Refund-requests screen lists customer-initiated online requests awaiting a finance/operations decision: accept, request more information, or auto-deny. *(agreed · MoM 12 Aug 2026, 18. Bulk Refund Processing and Refund Requests · DI-270)*
- Bulk refunds: select and refund at event or date level (e.g. ~5,000 transactions for a cancelled event), online and on-site bookings, with one approval step before processing. *(agreed · MoM 12 Aug 2026, 18. Bulk Refund Processing and Refund Requests · DI-269)*
- Guests can request a refund from their account/profile; operations are notified and can approve, reject or ask for more information. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-254)*
- A refund started at the POS is routed for approval before it reaches the bank. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-253)*
- Refunds use preset time-banded percentages (e.g. full refund a set number of days before the event, less closer to/after it), support partial refunds, and let an authorised approver apply a custom override percentage. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-252)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-028` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-028?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Create refund request.
- [ ] Every transition is wired: `BO-008`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-029` Report Builder

**Build the report nobody wrote down, without asking for a release.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `analytics` module |
| Block | Block A · ticket #20785 (APP-SETUP-BO-029) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listReports` reads the population and `getFinancialReport` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `conversationId` (deepLink), `reportId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/venue-operations/report-builder` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Category | select | optional | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | Sends `?category=` to `listReports`. | `listReports` ?category |
| Search | text field | optional | — | — | — | Sends `?search=` to `listReports`. | `listReports` ?search |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Report | select | — | Profit and loss · Balance sheet · Cash flow · Revenue by venue · Revenue by product · Tax summary | `getFinancialReport` ?report |
| Fiscal period | picker: choose a fiscal period | — | — | `getFinancialReport` ?fiscalPeriodId |
| Legal entity | picker: choose a legal entity | — | — | `getFinancialReport` ?legalEntityId |
| Cost center | picker: choose a cost center | — | — | `getFinancialReport` ?costCenterId |

**Form: Create report** (modal, opened by *Create report*; *Create report* calls `createReport`, *Cancel* sends nothing)

**Collects what `createReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createReport` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createReport` body |
| Category `category` | select | required | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `createReport` body |
| Data source `dataSource` | select | required | — | Orders · Order lines · Payments · Refunds · Shifts · Scan events · Entitlements · Products · Inventory · Stock movements · Stock counts · Waste … | — | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over data nobody maintains. | `createReport` body |
| Columns `columns` | repeatable rows | required | — | at least 1 | — | — | `createReport` body |
| Field `columns[].field` | text field | required | — | — | — | — | `createReport` body |
| Label `columns[].label` | text field | optional | — | — | — | — | `createReport` body |
| Aggregation `columns[].aggregation` | select | optional | None | None · Count · Count distinct · Sum · Average · Min · Max | — | — | `createReport` body |
| Sort order `columns[].sortOrder` | number field | optional | — | — | — | — | `createReport` body |
| Sort direction `columns[].sortDirection` | segmented control | optional | — | Asc · Desc | — | — | `createReport` body |
| Format `columns[].format` | text field | optional | — | — | — | — | `createReport` body |
| Filters `filters` | repeatable rows | optional | — | — | — | — | `createReport` body |
| Field `filters[].field` | text field | required | — | — | — | — | `createReport` body |
| Operator `filters[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Contains · Is null · Is not null | — | — | `createReport` body |
| Value `filters[].value` | field | optional | — | — | — | Open on purpose; its type is the field's. One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a … | `createReport` body |
| Values `filters[].values` | list of values (chips) | optional | — | — | — | The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`. | `createReport` body |
| Is parameter `filters[].isParameter` | toggle | optional | off | — | — | Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope. | `createReport` body |
| Group by `groupBy` | list of values (chips) | optional | — | — | — | — | `createReport` body |
| Parameters `parameters` | repeatable rows | optional | — | — | — | — | `createReport` body |
| Key `parameters[].key` | text field | required | — | — | — | — | `createReport` body |
| Label `parameters[].label` | text field | required | — | — | — | — | `createReport` body |
| Type `parameters[].type` | select | required | — | String · Integer · Decimal · Money · Boolean · Date · Date time · Uuid · Enum | — | — | `createReport` body |
| Is required `parameters[].isRequired` | toggle | required | — | — | — | — | `createReport` body |
| Default value `parameters[].defaultValue` | field | optional | — | — | — | Open on purpose. A value of this parameter's `type`, used when a run supplies none. | `createReport` body |
| Required permission `requiredPermission` | select | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a venue user could build themselves a … | `createReport` body |
| Max date range days `maxDateRangeDays` | number field (days) | optional | 366 | min 1 | — | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so `runReport`'s date-range 400 always has a … | `createReport` body |

Errors to draw in the form: 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report

**Form: Ask reporting question** (modal, opened by *Ask reporting question*; *Ask reporting question* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

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

**Form: Save natural language query** (modal, opened by *Save natural language query*; *Save natural language query* calls `saveNaturalLanguageQuery`, *Cancel* sends nothing)

**Collects what `saveNaturalLanguageQuery` sends before it is called.** Required: `name`. Optional: `category`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `saveNaturalLanguageQuery` body |
| Category `category` | select | optional | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `saveNaturalLanguageQuery` body |

**Form: Save report** (modal, opened by *Save report*; *Save report* calls `updateReport`, *Cancel* sends nothing)

**Collects what `updateReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `updateReport` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `updateReport` body |
| Category `category` | select | required | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `updateReport` body |
| Data source `dataSource` | select | required | — | Orders · Order lines · Payments · Refunds · Shifts · Scan events · Entitlements · Products · Inventory · Stock movements · Stock counts · Waste … | — | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over data nobody maintains. | `updateReport` body |
| Columns `columns` | repeatable rows | required | — | at least 1 | — | — | `updateReport` body |
| Field `columns[].field` | text field | required | — | — | — | — | `updateReport` body |
| Label `columns[].label` | text field | optional | — | — | — | — | `updateReport` body |
| Aggregation `columns[].aggregation` | select | optional | None | None · Count · Count distinct · Sum · Average · Min · Max | — | — | `updateReport` body |
| Sort order `columns[].sortOrder` | number field | optional | — | — | — | — | `updateReport` body |
| Sort direction `columns[].sortDirection` | segmented control | optional | — | Asc · Desc | — | — | `updateReport` body |
| Format `columns[].format` | text field | optional | — | — | — | — | `updateReport` body |
| Filters `filters` | repeatable rows | optional | — | — | — | — | `updateReport` body |
| Field `filters[].field` | text field | required | — | — | — | — | `updateReport` body |
| Operator `filters[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Contains · Is null · Is not null | — | — | `updateReport` body |
| Value `filters[].value` | field | optional | — | — | — | Open on purpose; its type is the field's. One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a … | `updateReport` body |
| Values `filters[].values` | list of values (chips) | optional | — | — | — | The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`. | `updateReport` body |
| Is parameter `filters[].isParameter` | toggle | optional | off | — | — | Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope. | `updateReport` body |
| Group by `groupBy` | list of values (chips) | optional | — | — | — | — | `updateReport` body |
| Parameters `parameters` | repeatable rows | optional | — | — | — | — | `updateReport` body |
| Key `parameters[].key` | text field | required | — | — | — | — | `updateReport` body |
| Label `parameters[].label` | text field | required | — | — | — | — | `updateReport` body |
| Type `parameters[].type` | select | required | — | String · Integer · Decimal · Money · Boolean · Date · Date time · Uuid · Enum | — | — | `updateReport` body |
| Is required `parameters[].isRequired` | toggle | required | — | — | — | — | `updateReport` body |
| Default value `parameters[].defaultValue` | field | optional | — | — | — | Open on purpose. A value of this parameter's `type`, used when a run supplies none. | `updateReport` body |
| Required permission `requiredPermission` | select | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a venue user could build themselves a … | `updateReport` body |
| Max date range days `maxDateRangeDays` | number field (days) | optional | 366 | min 1 | — | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so `runReport`'s date-range 400 always has a … | `updateReport` body |

Errors to draw in the form: 409 The report is a system report, which is clone-only (audit R096).

#### Outputs: what the screen shows and produces

**Shown**

**Every report definition** (data table, from `listReports`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| Filters | list or chips (count when long) | — |
| Group by | list or chips (count when long) | — |
| Parameters | list or chips (count when long) | — |
| Required permission | chip: SESSION FORCE LOGOUT, USER MANAGE, ROLE MANAGE, PERMISSION GRANT, PERMISSION VIEW … | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a … |
| Max date range days | 1,234 | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so … |
| ID | the name it points at, never the id | — |
| Is system | yes / no (icon or chip) | Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). Clone-only (decided 28 September, audit R096): `updateReport` … |

**The selected report definition** (detail panel, from `getReport`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| Filters | list or chips (count when long) | — |
| Group by | list or chips (count when long) | — |
| Parameters | list or chips (count when long) | — |
| Required permission | chip: SESSION FORCE LOGOUT, USER MANAGE, ROLE MANAGE, PERMISSION GRANT, PERMISSION VIEW … | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a … |
| Max date range days | 1,234 | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so … |
| ID | the name it points at, never the id | — |
| Is system | yes / no (icon or chip) | Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). Clone-only (decided 28 September, audit R096): `updateReport` … |
| Is retired | yes / no (icon or chip) | — |
| Estimated cost | chip: Low, Medium, High | Informs whether it may run inline or must be queued. |
| Created by principal | the name it points at, never the id | — |
| Last run at | 1 Oct 2026, 14:30 | — |

**The financial report** (detail panel, from `getFinancialReport`)

| Shows | Format | Notes |
|---|---|---|
| Report | chip: Profit and loss, Balance sheet, Cash flow, Revenue by venue, Revenue by product … | The report `getFinancialReport` returns. One vocabulary for the query and the response. |
| Fiscal period | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Currency | text | — |
| Currency scale | 1,234 | — |
| Generated at | 1 Oct 2026, 14:30 | — |
| Sections | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create report (primary button) | `createReport` POST `/reports` | CreateReportRequest | ReportDefinition | 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report | opens modal first |
| Ask reporting question (secondary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Delete report (destructive button) | `deleteReport` DELETE `/reports/{reportId}` | — | — | 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report`, audit R096) | — |
| Run report (secondary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Save natural language query (secondary button) | `saveNaturalLanguageQuery` POST `/reports/ask/{conversationId}/save` | inline | ReportDefinition | — | opens modal first |
| Save report (secondary button) | `updateReport` PUT `/reports/{reportId}` | CreateReportRequest | ReportDefinition | 409 The report is a system report, which is clone-only (audit R096). | opens modal first |

**Data it reads**: `getFinancialReport` (onLoad, P&L, balance sheet or cash flow); `listReports` (onLoad, List available report definitions)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

**What opens over it**

- confirmDialog *Delete report*: **Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A report this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report yet. Offers Create report (`createReport`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on category, search and the report are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem); 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 400 Unknown field, invalid filter, or estimated cost beyond the limit; 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report` … |

#### Permissions

- `getFinancialReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `createReport` → `REPORT_MANAGE` (configure) · staff, partner
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `deleteReport` → `REPORT_MANAGE` (configure) · staff, partner
- `getReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `saveNaturalLanguageQuery` → `REPORT_MANAGE` (configure) · staff, partner
- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

93 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.45 | Support account consolidation. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 5.7.53 | Cross-site financial consolidation. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 5.7.55 | Site-level profit and loss reporting. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 5.7.73 | Profit & Loss reporting. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 5.7.74 | Balance Sheet reporting. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 1.1.40 | System shall provide analytics and dashboards covering ticket sales, attendance, utilization, conversion rates, capacity utilization and revenue performance. | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.104 | Membership analytics | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.135 | Required Reports Operational Reports Donations by Campaign. Donations by Site. Donations by Product. Donations by Sales Channel. Donations by Date. Donations by User/Cashier. Donations by Payment … | Ticketing Catalogue | CONTRACTED | `createReport` |
| 3.2.65 | An Entry or Exit report is expected presenting the readings per outcome (ok/ko), per time and per access point. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.66 | The in park report showing the difference between the Entries and the Exits. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.68 | The length of stay report shall present the difference between the time in scan and the time out scan. | Admission and Access | CONTRACTED | `createReport` |
| 3.5.12 | System shall provide analytics showing bundle sales volume, revenue contribution, conversion rate, redemption rate, average order value impact, profitability, and performance by channel. | Admission and Access | CONTRACTED | `createReport` |
| … 81 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Custom report templates (advanced users, SQL/scripting) exported as PDF or Excel; ticket and receipt layouts built in a drag-and-drop template builder placing dynamic variables (guest name, ticket number, QR) on a background image. *(agreed · MoM 7 Aug 2026, 22. Report & Document Template Design · DI-184)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-029` · status **notStarted** · provenance generated
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (64), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-029?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create report, Ask reporting question, Delete report, Run report, Save natural language query, Save report.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-039` Shift Directory

**See every till, open or closed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASH_LIFT`, `CASH_NO_SALE`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SHIFT_APPROVE_OPEN`, `SHIFT_CLOSE`… (9 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `approveShiftOpen` decides items that `listShifts` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/venue-operations/shift-directory` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listShifts`. | `listShifts` ?workstationId |
| Status | select | optional | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | — | Sends `?status=` to `listShifts`. | `listShifts` ?status |
| Opened from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedFrom=` to `listShifts`. | `listShifts` ?openedFrom |
| Opened to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedTo=` to `listShifts`. | `listShifts` ?openedTo |

**Form: Open shift** (modal, opened by *Open shift*; *Open shift* calls `openShift`, *Cancel* sends nothing)

**Collects what `openShift` sends before it is called.** Required: `workstationId`, `openingFloat`. Optional: `depositBoxCode`, `bagNumber`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Workstation `workstationId` | picker: choose a workstation | required | — | — | shows names, sends the id | — | `openShift` body |
| Opening float `openingFloat` | repeatable rows | required | — | at least 1 | — | A count is a list of lines and the line is the row. Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — … | `openShift` body |
| ID `openingFloat[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `openShift` body |
| Shift `openingFloat[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `openShift` body |
| Deposit box `openingFloat[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `openShift` body |
| Count kind `openingFloat[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `openShift` body |
| Cash movement `openingFloat[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `openShift` body |
| Denomination `openingFloat[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `openShift` body |
| Counted quantity `openingFloat[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `openShift` body |
| Counted value `openingFloat[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `openShift` body |
| Counted by `openingFloat[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `openShift` body |
| Counted at `openingFloat[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `openShift` body |
| Recount of `openingFloat[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `openShift` body |
| Deposit box code `depositBoxCode` | text field | optional | — | max length 64 | — | Physical container assigned to this shift. Required where the venue configures deposit box allocation. | `openShift` body |
| Bag number `bagNumber` | text field | optional | — | max length 64 | — | Required where the venue configures bag numbers as mandatory. | `openShift` body |
| Recorded at `recordedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are … | `openShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent (`required-device-absent`).

**Form: Accept shift variance** (modal, opened by *Accept shift variance*; *Accept shift variance* calls `acceptShiftVariance`, *Cancel* sends nothing)

**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Retained for audit. The accepting principal is recorded. | `acceptShiftVariance` body |

Errors to draw in the form: 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type `shift-not-pending-variance`) — within tolerance, still open, or already accepted.

**Form: Approve shift open** (modal, opened by *Approve shift open*; *Approve shift open* calls `approveShiftOpen`, *Cancel* sends nothing)

**Collects what `approveShiftOpen` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | — | `approveShiftOpen` body |

Errors to draw in the form: 409 Shift is not `pendingApproval` (problem type `shift-not-awaiting-approval`)

**Form: Create cash movement** (modal, opened by *Create cash movement*; *Create cash movement* calls `createCashMovement`, *Cancel* sends nothing)

**Collects what `createCashMovement` sends before it is called.** Required: `id`, `kind`, `amount`, `recordedAt`. Optional: `denominations`, `reference`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. | `createCashMovement` body |
| Kind `kind` | segmented control | required | — | Opening float · Lift · Add | — | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`. | `createCashMovement` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createCashMovement` body |
| Denominations `denominations` | repeatable rows | optional | — | at least 1 | — | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. | `createCashMovement` body |
| ID `denominations[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Shift `denominations[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `createCashMovement` body |
| Deposit box `denominations[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Count kind `denominations[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `createCashMovement` body |
| Cash movement `denominations[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `createCashMovement` body |
| Denomination `denominations[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `createCashMovement` body |
| Counted quantity `denominations[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `createCashMovement` body |
| Counted value `denominations[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `createCashMovement` body |
| Counted by `denominations[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Counted at `denominations[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |
| Recount of `denominations[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `createCashMovement` body |
| Reference `reference` | text field | optional | — | max length 64 | — | Safe drop reference or bag number. | `createCashMovement` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `createCashMovement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 …

**Form: Record no sale** (modal, opened by *Record no sale*; *Record no sale* calls `recordNoSale`, *Cancel* sends nothing)

**Collects what `recordNoSale` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordNoSale` body |
| Reason `reason` | radio group | required | — | Change for guest · Correct float · Retrieve dropped cash · Till check · Other | — | — | `recordNoSale` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `recordNoSale` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordNoSale` body |

Errors to draw in the form: 409 Shift is not open (problem type `shift-not-open`)

**Form: Reopen shift** (modal, opened by *Reopen shift*; *Reopen shift* calls `reopenShift`, *Cancel* sends nothing)

**Collects what `reopenShift` sends before it is called.** Required: `reason` and `supervisorStepUp` — a supervisor who did not close the shift enters their staff PIN on this device (`principalId`, `credential`) (decided 28 September, audit R144). A refusal names which: the supervisor is the closer (403 approver-is-closer) or the PIN was refused (403 supervisor-step-up-refused). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `reopenShift` body |
| Supervisor step up `supervisorStepUp` | group | required | — | — | — | The supervisor signing the reopen on this device (audit R144). Replaces the bare `approverPrincipalId`, which named an approver without proving they were there. | `reopenShift` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `reopenShift` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `reopenShift` body |

Errors to draw in the form: 403 The supervisor is the closing principal (problem type `approver-is-closer`), or the step-up failed: the PIN did not verify, or the principal does not hold …; 409 Shift is not closed (problem type `shift-not-closed`), or the fiscal period has closed over it (`fiscal-period-closed`)

**Form: Resume shift** (modal, opened by *Resume shift*; *Resume shift* calls `resumeShift`, *Cancel* sends nothing)

**Collects what `resumeShift` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `resumeShift` body |

Errors to draw in the form: 403 Not the principal who suspended it, and the caller does not hold SHIFT_CLOSE_OTHER (problem type `not-shift-holder`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this shift is not `suspended` (`shift-not-suspended`)

**Sent by *Close shift*** (`closeShift`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Counted cash `countedCash` | repeatable rows | required | — | at least 1; A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`. | — | The cashier's blind count, one line per denomination counted (decided 29 September, readiness close-out; our build plan). | `closeShift` body |
| Denomination `countedCash[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there. | `closeShift` body |
| Count `countedCash[].count` | number field | required | — | min 0; max 100000 | — | How many of this note or coin were counted. Zero is a line, not an omission: a denomination counted and found empty. | `closeShift` body |
| Total `countedCash[].total` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent. | `closeShift` body |
| Non cash declared `nonCashDeclared` | repeatable rows | optional | — | — | — | Declared totals per non-cash tender, for reconciliation against captured payments. | `closeShift` body |
| Tender `nonCashDeclared[].tender` | text field | required | — | — | — | — | `closeShift` body |
| Amount `nonCashDeclared[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeShift` body |
| Notes `notes` | text area | optional | — | max length 1000 | — | — | `closeShift` body |
| Release held leases `releaseHeldLeases` | toggle | optional | on | — | — | Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak. | `closeShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `closeShift` body |

**Sent by *Suspend shift*** (`suspendShift`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 200 | — | — | `suspendShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `suspendShift` body |

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**Every cash movement** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Deposit box | the name it points at, never the id | The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099). |
| Witness principal | the name it points at, never the id | The cashier who countersigned a withdrawal. Null on other movements. |
| Withdrawal reason | chip: Banking, Safe drop, Change order, Other | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |

**The selected shift** (detail panel, from `getCurrentShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**The shift** (detail panel, from `getShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open shift (primary button) | `openShift` POST `/shifts` | OpenShiftRequest | Shift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent … | opens modal first |
| Accept shift variance (secondary button) | `acceptShiftVariance` POST `/shifts/{shiftId}/accept-variance` | inline | Shift | 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type … | step-up: pin (A supervisor signs off a cashier's over/short at the till, in front of the drawer (audit R080 (e)).); opens modal first |
| Approve shift open (secondary button) | `approveShiftOpen` POST `/shifts/{shiftId}/approve-open` | inline | Shift | 409 Shift is not `pendingApproval` (problem type `shift-not-awaiting-approval`) | opens modal first |
| Close shift (destructive button) | `closeShift` POST `/shifts/{shiftId}/close` | CloseShiftRequest | ShiftCloseResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` or `suspended` — already closing or closed (problem type `shift-not-open`) — or open orders remain … | — |
| Create cash movement (secondary button) | `createCashMovement` POST `/shifts/{shiftId}/cash-movements` | CreateCashMovementRequest | CashMovement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since … | opens modal first |
| Record no sale (secondary button) | `recordNoSale` POST `/shifts/{shiftId}/no-sale` | inline | NoSaleEvent | 409 Shift is not open (problem type `shift-not-open`) | opens modal first |
| Reopen shift (secondary button) | `reopenShift` POST `/shifts/{shiftId}/reopen` | inline | Shift | 403 The supervisor is the closing principal (problem type `approver-is-closer`), or the step-up failed: the PIN did not verify, or the principal does not hold …; 409 Shift is not closed (problem type … | step-up: pin (Reopening a counted shift is a reversal; a supervisor signs it in place (audit R144).); opens modal first |
| Resume shift (secondary button) | `resumeShift` POST `/shifts/{shiftId}/resume` | inline | Shift | 403 Not the principal who suspended it, and the caller does not hold SHIFT_CLOSE_OTHER (problem type `not-shift-holder`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this … | opens modal first |
| Suspend shift (destructive button) | `suspendShift` POST `/shifts/{shiftId}/suspend` | inline | Shift | 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` (problem type `shift-not-open`) | — |

**Data it reads**: `listShifts` (onLoad, List shifts); `getCurrentShift` (onLoad, The open or suspended shift on the session's workstation); `getShift` (onLoad, Read a shift); `listCashMovements` (onLoad, Lifts, adds and the opening float)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

**What opens over it**

- confirmDialog *Close shift*: **Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A shift this affects should be identified in the dialog, not just counted. **Collects what `closeShift` sends before it is called.** Required: `countedCash`, `recordedAt`. Optional …
- confirmDialog *Suspend shift*: **Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A shift this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, status, openedFrom, openedTo and the shift are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent (`required-device-absent`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this shift is not `suspended` (`shift-not-suspended`); 409 Shift is not `open` (problem type `shift-not-open`) |

#### Permissions

- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `getCurrentShift` → `SHIFT_OPEN` (operate) · staff
- `openShift` → `SHIFT_OPEN` (operate) · staff
- `acceptShiftVariance` → `OVERSHORT_ACCEPT` (operate) · staff · step-up pin
- `approveShiftOpen` → `SHIFT_APPROVE_OPEN` (operate) · staff
- `closeShift` → `SHIFT_CLOSE` (operate) · staff
- `createCashMovement` → `CASH_LIFT` (operate) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `recordNoSale` → `CASH_NO_SALE` (operate) · staff
- `reopenShift` → `SHIFT_REOPEN` (operate) · staff · step-up pin
- `resumeShift` → `SHIFT_OPEN` (operate) · staff
- `suspendShift` → `SHIFT_SUSPEND` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.9.8 | The system should allow the option of configuring the requirement of a supervisor's approval for opening and closing a cashier's session. For example, to open a cashier’s session, the cashier details … | F&B & Guest Management | CONTRACTED | `approveShiftOpen` |
| 5.8.3 | The system should allow the cashier to enter a total amount counted, or to count by denomination. For denomination counts, the cashier counts and enters each denomination separately and each count is … | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.1 | The system should be able to manage end of day shift closing and provide the ability to close out each cash register. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.2 | The system should have the ability to do a "blind" cashier close-out. Over-shorts should be captured and recorded. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.5 | The system should allow automatic closing of a cashier's session after a configurable time period. The supervisor should be notified on closing of the session. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*
- Shift/session view shows open and closed sessions per workstation with expected cash and card totals; a live till monitor shows real-time cash status per workstation and open/close codes. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-273)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-039` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (61), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (56 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-039?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Open shift, Accept shift variance, Approve shift open, Close shift, Create cash movement, Record no sale, Reopen shift, Resume shift, Suspend shift.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `CASH_LIFT`, `CASH_NO_SALE`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SHIFT_APPROVE_OPEN`, `SHIFT_CLOSE`, `SHIFT_OPEN`, `SHIFT_REOPEN`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**36 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acceptShiftVariance": {"method":"POST","path":"/shifts/{shiftId}/accept-variance","contract":"shift","summary":"Accept an over/short beyond the threshold","permission":"OVERSHORT_ACCEPT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"addTip": {"method":"POST","path":"/payments/{paymentId}/tip","contract":"orders","summary":"Record a tip against a payment","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"appendEntitlementToMedia": {"method":"POST","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"Add something to a ticket the guest already holds","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AppendEntitlementRequest","responds":"AppendEntitlementResult"},
"applyManualDiscount": {"method":"POST","path":"/orders/{orderId}/discounts","contract":"orders","summary":"Apply a discount a cashier chose","permission":"ORDER_DISCOUNT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ManualDiscountRequest","responds":"Order"},
"approveShiftOpen": {"method":"POST","path":"/shifts/{shiftId}/approve-open","contract":"shift","summary":"Approve a shift opening outside tolerance","permission":"SHIFT_APPROVE_OPEN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"assessProductChange": {"method":"POST","path":"/products/{productId}/change-impact","contract":"catalogue","summary":"What a change would touch, before making it","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductChangeImpact"},
"assignChargeback": {"method":"POST","path":"/chargebacks/{chargebackId}/assign","contract":"orders","summary":"Give a chargeback to an investigator, with a note","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"capturePayment": {"method":"POST","path":"/payments/{paymentId}/capture","contract":"orders","summary":"Capture a previously authorised payment","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"cloneProduct": {"method":"POST","path":"/products/{productId}/clone","contract":"catalogue","summary":"Copy a product as a new draft","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Product"},
"closeDepositBoxes": {"method":"POST","path":"/deposit-boxes/close","contract":"shift","summary":"Close one box or all of them","permission":"SHIFT_CLOSE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DepositBox"},
"closeShift": {"method":"POST","path":"/shifts/{shiftId}/close","contract":"shift","summary":"Blind close-out","permission":"SHIFT_CLOSE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CloseShiftRequest","responds":"ShiftCloseResult"},
"createCashMovement": {"method":"POST","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Record a cash lift or add","permission":"CASH_LIFT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCashMovementRequest","responds":"CashMovement"},
"createGroupBooking": {"method":"POST","path":"/group-bookings","contract":"orders","summary":"Turn an order into a group booking","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGroupBookingRequest","responds":"GroupBooking"},
"createOrder": {"method":"POST","path":"/orders","contract":"orders","summary":"Create an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateOrderRequest","responds":"Order"},
"createPayment": {"method":"POST","path":"/payments","contract":"orders","summary":"Take a payment against an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePaymentRequest","responds":"Payment"},
"createRefund": {"method":"POST","path":"/orders/{orderId}/refunds","contract":"orders","summary":"Refund an order, wholly or in part","permission":"ORDER_REFUND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRefundRequest","responds":null},
"createRefundRequest": {"method":"POST","path":"/refund-requests","contract":"orders","summary":"Guest-initiated refund request","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createReport": {"method":"POST","path":"/reports","contract":"reporting","summary":"Create a custom report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"deleteReport": {"method":"DELETE","path":"/reports/{reportId}","contract":"reporting","summary":"Retire a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"exchangeOrderLines": {"method":"POST","path":"/orders/{orderId}/exchanges","contract":"orders","summary":"Exchange lines for different products or dates","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ExchangeOrderRequest","responds":"OrderExchangeResult"},
"getChargebackAnalytics": {"method":"GET","path":"/chargebacks/analytics","contract":"orders","summary":"Chargeback rate, win and loss, by reason, provider, outcome and period","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"periodFrom","in":"query","required":true},{"name":"periodTo","in":"query","required":true},{"name":"groupBy","in":"query","required":null},{"name":"minChargebacks","in":"query","required":null},{"name":"productId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"providerId","in":"query","required":null}],"requestBody":null,"responds":"OrdChargebackAnalytics"},
"getCurrentShift": {"method":"GET","path":"/shifts/current","contract":"shift","summary":"The open or suspended shift on the session's workstation","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Shift"},
"getFinancialReport": {"method":"GET","path":"/reports/financial","contract":"finance","summary":"Financial statements, revenue and tax summaries","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"report","in":"query","required":true},{"name":"fiscalPeriodId","in":"query","required":true},{"name":"legalEntityId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"costCenterId","in":"query","required":null}],"requestBody":null,"responds":"FinancialReport"},
"getGroupBooking": {"method":"GET","path":"/group-bookings/{groupBookingId}","contract":"orders","summary":"A group, its leader and its name-capture duty","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GroupBooking"},
"getMediaAsset": {"method":"GET","path":"/media/{mediaId}","contract":"assets","summary":"Read an asset with derivatives and usage","permission":"ASSET_LIBRARY_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetDetail"},
"getMediaEntitlements": {"method":"GET","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"What is already on this media","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaEntitlements"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getOrderStatement": {"method":"GET","path":"/orders/{orderId}/statement","contract":"orders","summary":"Full financial history of an order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrderStatement"},
"getProduct": {"method":"GET","path":"/products/{productId}","contract":"catalogue","summary":"Read a product","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Product"},
"getRefundPolicy": {"method":"GET","path":"/venues/{venueId}/refund-policy","contract":"orders","summary":"Read a venue's refund policy","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RefundPolicy"},
"getReport": {"method":"GET","path":"/reports/{reportId}","contract":"reporting","summary":"Read a report definition","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportDefinition"},
"getSettlement": {"method":"GET","path":"/settlements/{settlementId}","contract":"finance","summary":"Settlement detail with match results","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"Settlement"},
"getShift": {"method":"GET","path":"/shifts/{shiftId}","contract":"shift","summary":"Read a shift","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Shift"},
"getTaxDocumentRendition": {"method":"GET","path":"/tax-documents/{documentId}/rendition","contract":"finance","summary":"The PDF of a tax invoice or credit memo, in a language","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"FinTaxDocumentRendition"},
"getTaxInvoice": {"method":"GET","path":"/tax-invoices/{invoiceId}","contract":"finance","summary":"One tax invoice, with its lines, VAT per rate and credit memos","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"FinTaxInvoice"},
"holdOrder": {"method":"POST","path":"/orders/{orderId}/hold","contract":"orders","summary":"Park a sale and free the till","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"ingestSettlementFile": {"method":"POST","path":"/settlements","contract":"finance","summary":"Ingest a provider settlement file","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"inquirePaymentStatus": {"method":"POST","path":"/payments/{paymentId}/inquiry","contract":"orders","summary":"Ask the provider what actually happened","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"issueCreditMemo": {"method":"POST","path":"/tax-invoices/{invoiceId}/credit-memos","contract":"finance","summary":"Credit all or part of a tax invoice","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinIssueCreditMemoRequest","responds":"FinCreditMemo"},
"issueTaxInvoice": {"method":"POST","path":"/tax-invoices","contract":"finance","summary":"Issue a tax invoice for one or more paid orders","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinIssueTaxInvoiceRequest","responds":"FinTaxInvoice"},
"listBookingFlows": {"method":"GET","path":"/venues/{venueId}/booking-flows","contract":"white-label","summary":"A venue's booking flows, in the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"flowTypeKey","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCashMovements": {"method":"GET","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Lifts, adds and the opening float","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConsentQuestions": {"method":"GET","path":"/consent-questions","contract":"marketing-crm","summary":"The consent questions a venue asks at booking","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialReplacementReissue": {"method":"GET","path":"/credential-replacement-reissue","contract":"access","summary":"Credential Replacement, Reissue, Revocation & Recovery","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialReplacementReissueRevocationRecoveryView"},
"listCreditMemos": {"method":"GET","path":"/credit-memos","contract":"finance","summary":"Credit memos issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"taxInvoiceId","in":"query","required":null},{"name":"refundId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrderRefunds": {"method":"GET","path":"/orders/{orderId}/refunds","contract":"orders","summary":"List refunds against an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductVariants": {"method":"GET","path":"/products/{productId}/variants","contract":"catalogue","summary":"List generated variants","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductVersions": {"method":"GET","path":"/products/{productId}/versions","contract":"catalogue","summary":"What this product used to be","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductVersion"},
"listReports": {"method":"GET","path":"/reports","contract":"reporting","summary":"List available report definitions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlementExceptions": {"method":"GET","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Unmatched or mismatched settlement lines","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlements": {"method":"GET","path":"/settlements","contract":"finance","summary":"List settlement batches","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"providerName","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShifts": {"method":"GET","path":"/shifts","contract":"shift","summary":"List shifts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"openedFrom","in":"query","required":null},{"name":"openedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxInvoices": {"method":"GET","path":"/tax-invoices","contract":"finance","summary":"Tax invoices issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"orderId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"invoiceType","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTicketReissueFulfillment": {"method":"GET","path":"/ticket-reissue-fulfillment","contract":"orders","summary":"Ticket Reissue & Fulfillment Regeneration","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TicketReissueFulfillmentRegenerationView"},
"modifyOrder": {"method":"POST","path":"/orders/{orderId}/modify","contract":"orders","summary":"Add or remove lines on an existing order","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifyOrderRequest","responds":"OrderModificationResult"},
"openShift": {"method":"POST","path":"/shifts","contract":"shift","summary":"Open a shift","permission":"SHIFT_OPEN","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OpenShiftRequest","responds":"Shift"},
"recordChargeback": {"method":"POST","path":"/chargebacks/intake","contract":"orders","summary":"Take in a chargeback notified by a provider","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"recordChargebackOutcome": {"method":"POST","path":"/chargebacks/{chargebackId}/outcome","contract":"orders","summary":"Record the bank's decision and adjust the ledger","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"recordNoSale": {"method":"POST","path":"/shifts/{shiftId}/no-sale","contract":"shift","summary":"Open the Deposit Box without a sale","permission":"CASH_NO_SALE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NoSaleEvent"},
"reopenShift": {"method":"POST","path":"/shifts/{shiftId}/reopen","contract":"shift","summary":"Reopen a shift closed in error","permission":"SHIFT_REOPEN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"replaceMediaAsset": {"method":"POST","path":"/media/{mediaId}/replace","contract":"assets","summary":"Replace the file behind an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaReplaceResult"},
"reprintOrder": {"method":"POST","path":"/orders/{orderId}/reprints","contract":"orders","summary":"Reprint or resend tickets","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rescheduleOrder": {"method":"POST","path":"/orders/{orderId}/reschedule","contract":"orders","summary":"Move an order to another performance","permission":"ORDER_RESCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderExchangeResult"},
"resolveSettlementException": {"method":"POST","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Resolve a settlement exception","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SettlementException"},
"restoreProductVersion": {"method":"POST","path":"/products/{productId}/versions/{version}/restore","contract":"catalogue","summary":"Put a previous version back","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Product"},
"resumeOrder": {"method":"POST","path":"/orders/{orderId}/resume","contract":"orders","summary":"Bring a parked sale back to a till","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderResumeResult"},
"resumeShift": {"method":"POST","path":"/shifts/{shiftId}/resume","contract":"shift","summary":"Resume a suspended shift","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"saveNaturalLanguageQuery": {"method":"POST","path":"/reports/ask/{conversationId}/save","contract":"reporting","summary":"Save a natural-language answer as a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportDefinition"},
"searchMedia": {"method":"GET","path":"/media","contract":"assets","summary":"Search the asset library","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"tag","in":"query","required":null},{"name":"collectionId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":"unusedOnly","in":"query","required":null},{"name":"rightsExpiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setProductAttributes": {"method":"PUT","path":"/products/{productId}/attributes","contract":"catalogue","summary":"Set the attribute axes for a product","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"settleDeposit": {"method":"POST","path":"/deposits/{depositId}/settle","contract":"finance","summary":"Convert to revenue, return it, or forfeit it","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Deposit"},
"suspendShift": {"method":"POST","path":"/shifts/{shiftId}/suspend","contract":"shift","summary":"Suspend a shift so another user can log in","permission":"SHIFT_SUSPEND","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"updateGroupBooking": {"method":"PATCH","path":"/group-bookings/{groupBookingId}","contract":"orders","summary":"Confirm numbers, change the leader or cancel a group","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"UpdateGroupBookingRequest","responds":"GroupBooking"},
"updateProduct": {"method":"PATCH","path":"/products/{productId}","contract":"catalogue","summary":"Update a product","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"UpdateProductRequest","responds":"Product"},
"updateProductVariant": {"method":"PATCH","path":"/products/{productId}/variants/{variantId}","contract":"catalogue","summary":"Describe a variant","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProductVariant"},
"updateReport": {"method":"PUT","path":"/reports/{reportId}","contract":"reporting","summary":"Publish a new version of a definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"voidOrder": {"method":"POST","path":"/orders/{orderId}/voids","contract":"orders","summary":"Void an order","permission":"ORDER_VOID","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AppendEntitlementRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header."},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true}}}},"paymentMethod":{"type":"string","enum":["card","cash","wallet","giftCard","chargeToAccount"]},"note":{"type":"string","maxLength":300},"recordedAt":{"type":"string","format":"date-time"}}},
"AppendEntitlementResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","media"],"properties":{"order":{"allOf":[{"$ref":"#/components/schemas/Order"}],"description":"A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"},"media":{"allOf":[{"$ref":"#/components/schemas/MediaEntitlements"}],"description":"The full set now on the media, so the cashier can say what the QR does."},"addedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowLevelSettings": {"x-ticvai-persistence":"none — jsonb column on whitelabel.booking_flow","type":"object","description":"**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n","properties":{"performanceReveal":{"type":"string","enum":["dateTimeTicket","allAtOnce"],"default":"dateTimeTicket","description":"**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"},"signInAt":{"type":"string","enum":["afterAddOns","atPayment"],"default":"afterAddOns","description":"**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"},"seatEventDateMode":{"type":"string","enum":["inlineStep","popupOnSeatMap"],"default":"inlineStep","description":"**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"},"extrasStep":{"type":"string","enum":["auto","always","never"],"default":"auto","description":"`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."},"quickTour":{"type":"boolean","default":false,"description":"**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"default":[],"description":"**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n","items":{"type":"string","format":"uuid"}}}},
"BookingFlowStep": {"x-ticvai-persistence":"whitelabel.booking_flow_step","type":"object","description":"One step of a venue's flow, in the venue's order (decided 29 September, W12).","required":["stepKey","enabled","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bookingFlowId":{"type":"string","format":"uuid","readOnly":true},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"enabled":{"type":"boolean","description":"A `required` step cannot be off; the flow saves and `isValid` turns false."},"sortOrder":{"type":"integer","minimum":0},"requirement":{"type":"string","enum":["required","optional","conditional"],"readOnly":true,"x-ticvai-derived":"onRead","description":"From the flow type, so the CMS can mark the step without a second read."},"settings":{"type":"object","additionalProperties":true,"default":{},"description":"The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."}}},
"BookingFlowTypeKey": {"type":"string","description":"**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n","enum":["datedDayPass","timedEntry","openDated","seatedFixedPerformance","seatedDateTimeSeatMap","experienceWorkshop","surfSession","meetingRoomHourly","cabanaMap","cabanaBySize","guidedTourByLanguage","transport","tableReservation","membership","giftCard","multiLocation"]},
"CashCountLine": {"x-ticvai-persistence":"orders.cash_count_line","type":"object","description":"**One denomination, counted once, against one shift.** Raised in review on 24 August: the table was a stub.\n**The denomination is referenced rather than described** — `platform.denomination` already holds the note and coin definitions per currency, and a count line that repeats the face value is a count line that can disagree with the till it was counted on.\n**`countedQuantity` is a quantity and `expectedQuantity` is derived**, not stored: the expectation is the opening float plus every movement, and a stored expectation that drifts from the movements is a variance nobody can explain.\n","required":["shiftId","denominationId","countedQuantity"],"properties":{"id":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","description":"A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are."},"depositBoxId":{"type":"string","format":"uuid","nullable":true},"countKind":{"type":"string","enum":["openingFloat","close","movement"],"description":"Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). **Until 26 September the three were indistinguishable on one shift** (pull audit R099). Set by the server from the operation that wrote the line.\n"},"cashMovementId":{"type":"string","format":"uuid","nullable":true,"description":"The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`.\n"},"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination` — face value, kind and sort order live there."},"countedQuantity":{"type":"integer","minimum":0,"description":"**How many of this note or coin were in the drawer.**"},"countedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**Quantity times face value, stored.** Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count.\n"},"countedBy":{"type":"string","format":"uuid","nullable":true},"countedAt":{"type":"string","format":"date-time"},"recountOf":{"type":"string","format":"uuid","nullable":true,"description":"**A recount points at what it replaces rather than overwriting it.** `requestRecount` exists because a variance is a question before it is a fact.\n"}}},
"CashMovement": {"x-ticvai-persistence":"orders.cash_movement","allOf":[{"$ref":"#/components/schemas/CreateCashMovementRequest"},{"type":"object","required":["shiftId","authorisedByPrincipalId","sequence"],"properties":{"shiftId":{"type":"string","format":"uuid"},"depositBoxId":{"type":"string","format":"uuid","nullable":true,"description":"The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"},"witnessPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The cashier who countersigned a withdrawal. Null on other movements."},"withdrawalReason":{"allOf":[{"$ref":"#/components/schemas/WithdrawalReason"}],"nullable":true},"authorisedByPrincipalId":{"type":"string","format":"uuid","description":"The principal who authorised the movement, recorded for audit."},"sequence":{"type":"integer","description":"Monotonic within the shift. Preserves order across an offline batch."},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}]},
"CashMovementKind": {"type":"string","enum":["openingFloat","lift","add"],"description":"`openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`.\n"},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"Chargeback": {"type":"object","x-ticvai-persistence":"orders.chargeback + orders.chargeback_evidence + orders.chargeback_investigation_log","description":"BL-118, CF-144. **A chargeback is not a refund**, and treating it as one is how a venue loses them by default.\nA refund is a decision the venue makes. **A chargeback is a decision a bank makes, on a clock the venue does not control** — evidence is due in days, a deadline missed is a case lost regardless of merit, and there is a fee either way.\nThe money is already gone when this record is created. **Representment is an argument, not a reversal.**\n","required":["id","paymentId","amount","reason","status","evidenceDueBy"],"properties":{"id":{"type":"string","format":"uuid"},"paymentId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid"},"providerCaseReference":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"feeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","enum":["fraudulent","productNotReceived","productUnacceptable","duplicate","subscriptionCancelled","creditNotProcessed","unrecognised","other"],"description":"**The scheme's reason code, mapped.** Which evidence wins depends entirely on it — a *product not received* case is answered by a scan record and a *fraudulent* case is not.\n"},"status":{"type":"string","enum":["received","underReview","evidenceSubmitted","won","lost","accepted","expired"]},"evidenceDueBy":{"type":"string","format":"date-time","description":"**The field the whole record exists for.** A deadline missed is a case lost on merit nobody read, and it is the one date that must reach a person rather than a report.\n"},"evidenceSubmittedAt":{"type":"string","format":"date-time","nullable":true},"evidence":{"type":"array","description":"**What the platform can prove**, assembled rather than typed: the order, the scan that admitted them, the delivery, the terms accepted, the IP and device. A venue answering a chargeback by hand is a venue answering it late.\nHeld as rows of `orders.chargeback_evidence`, one per item (29 September, build: a list of objects needs its own table to be stored at all).\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["order","scanRecord","deliveryProof","termsAccepted","communication","deviceFingerprint","other"]},"reference":{"type":"string"}}}},"outcomeAt":{"type":"string","format":"date-time","nullable":true},"schemeReasonCode":{"type":"string","nullable":true,"description":"The card scheme's own reason code as notified, beside the mapped `reason` (5.7.92)."},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"description":"When the provider notified the case; the date its debit posts to (`recordChargeback`)."},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who is investigating (`assignChargeback`)."},"investigationLog":{"type":"array","description":"Notes from `assignChargeback` and `recordChargebackOutcome`, oldest first, with who wrote each and when. Append-only. Held as rows of `orders.chargeback_investigation_log` (29 September, build).","items":{"type":"object","properties":{"note":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}},"debitJournalEntryId":{"type":"string","format":"uuid","nullable":true,"description":"The `chargebackDebit` (and `chargebackFee`) entry posted at intake."},"outcomeJournalEntryId":{"type":"string","format":"uuid","nullable":true,"description":"The `chargebackReversal` entry posted when the case is won, or the additional fee when lost."}}},
"CloseShiftRequest": {"type":"object","required":["countedCash","recordedAt"],"properties":{"countedCash":{"type":"array","minItems":1,"description":"**The cashier's blind count, one line per denomination counted** (decided 29 September, readiness close-out; our build plan). The server writes each line as one `CashCountLine` (`countKind` close) against the shift, taking the face value from `platform.denomination`. A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`.\n","items":{"$ref":"#/components/schemas/CountedDenominationLine"}},"nonCashDeclared":{"type":"array","description":"Declared totals per non-cash tender, for reconciliation against captured payments.\n","items":{"type":"object","required":["tender","amount"],"properties":{"tender":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"notes":{"type":"string","maxLength":1000},"releaseHeldLeases":{"type":"boolean","default":true,"description":"Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"ConsentQuestion": {"type":"object","x-ticvai-persistence":"marketing.consent_question + marketing.consent_question_version","description":"**A venue-defined consent question asked at booking** (decided 29 September, rev 3 REV3-26). Each version's text is kept in `consent_question_version`, so an answer always points at the exact words the guest saw. Attached to products by the catalogue and to booking flows by the white-label flow configuration; one or several per flow, as the venue chooses.\n","required":["id","kind","text","version","scope","required","blockingAnswer","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ConsentQuestionKind"},"text":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"The question as the guest reads it, per locale."},"helpText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"Raised by one each time the question changes (`updateConsentQuestion`)."},"scope":{"type":"string","enum":["perPerson","perBooking"],"default":"perPerson","description":"Asked for each declared person, or once for the whole booking."},"required":{"type":"boolean","default":true,"description":"Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`)."},"blockingAnswer":{"type":"string","enum":["yes","no","none"],"default":"none","description":"The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing."},"status":{"type":"string","enum":["active","retired"],"default":"active"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ConsentQuestionKind": {"type":"string","description":"What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue set them.","enum":["swim","scuba","risk","custom"]},
"CountedDenominationLine": {"type":"object","x-ticvai-persistence":"none — request only; lands as `CashCountLine` rows","description":"**One line of a cash count as the cashier types it: which note or coin, how many, and what they come to** (decided 29 September, readiness close-out; our build plan). The shape of the blind count on close (`closeShift`) and of the count columns on the till screens (POS-007, POS-011). It is the request side of `CashCountLine`, which is the stored row and adds the shift, the count kind, who counted and when.\n**`total` is shown to the cashier and checked, not trusted**: the server recomputes `count` times the denomination's face value and refuses a line whose `total` disagrees with 422 `count-total-mismatch`. An inactive or unknown denomination is refused with 422 `unknown-denomination`.\n","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there."},"count":{"type":"integer","minimum":0,"maximum":100000,"description":"**How many of this note or coin were counted.** Zero is a line, not an omission: a denomination counted and found empty."},"total":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"`count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent.\n"}}},
"CreateCashMovementRequest": {"type":"object","required":["id","kind","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7."},"kind":{"$ref":"#/components/schemas/CashMovementKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"denominations":{"$ref":"#/components/schemas/DenominationCount","x-ticvai-persisted":false,"description":"**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"},"reference":{"type":"string","maxLength":64,"description":"Safe drop reference or bag number."},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateGroupBookingRequest": {"type":"object","description":"Request only. Persisted as `GroupBooking`.","required":["orderId","leaderSubjectId","expectedSize"],"properties":{"groupQuoteId":{"x-ticvai-references":"orders.group_quote","type":"string","format":"uuid","nullable":true,"description":"**The quote this booking converts** (BO-272). Must be the current version and `sent` or `accepted`; conversion sets its `groupBookingId` and moves a `sent` quote to `accepted` (decided 29 September, writers pass)."},"kind":{"type":"string","enum":["general","school","corporate","party"],"default":"general"},"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"orderId":{"type":"string","format":"uuid"},"leaderSubjectId":{"type":"string","format":"uuid","description":"The person who pays, is called if the coach is late, and collects the names."},"organisationName":{"type":"string","maxLength":200,"nullable":true},"expectedSize":{"type":"integer","minimum":2},"minimumSize":{"type":"integer","minimum":1,"nullable":true},"attendeeCaptureRequired":{"type":"boolean","default":false},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true}}},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateRefundRequest": {"type":"object","required":["id","amount","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Omit to refund the whole order."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","minLength":3,"maxLength":500},"secondaryAuthorisation":{"type":"object","description":"Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid"},"credential":{"type":"string","maxLength":512,"description":"The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."}}},"refundToOriginalTender":{"type":"boolean","default":true},"alternateTender":{"$ref":"#/components/schemas/TenderKind"},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"CredentialReplacementReissueRevocationRecoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Replacement, Reissue, Revocation & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"],"description":"Replacement reason this policy covers"},"immediateOldMediaRevocation":{"type":"boolean","description":"Immediate old-media revocation"},"gracePeriod":{"type":"string","description":"ISO 8601 duration, e.g. PT30M"},"maximumReplacements":{"type":"integer","description":"Maximum replacements"},"identityVerification":{"type":"boolean","description":"Identity verification"},"supervisorApproval":{"type":"boolean","description":"Supervisor approval"},"reasonCodes":{"type":"array","items":{"type":"string"},"description":"Reason codes"},"recoveryAllowed":{"type":"boolean","description":"A suspended credential may be restored under this policy"}},"required":["reason"]},
"DataSource": {"type":"string","description":"What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n","enum":["orders","orderLines","payments","refunds","shifts","scanEvents","entitlements","products","inventory","stockMovements","stockCounts","waste","workstations","devices","principals","loyalty","reviews","queueEntries","guests","campaigns","cases","ledgerEntries","workOrders","approvals","purchaseOrders","receipts","requisitions","stockBatches","resourceBookings","delegations","forms","challenges","wallets","resaleListings","accreditationApplications","accreditationHolders","accreditationCredentials","forecastPoints"],"x-ticvai-forecast-points":"**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"},
"DenominationCount": {"type":"array","description":"**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n","items":{"$ref":"#/components/schemas/CashCountLine"},"minItems":1},
"Deposit": {"type":"object","x-ticvai-persistence":"ledger.deposit","description":"**Money taken before the sale is complete.** Not deferred revenue — that is a sold entitlement not yet consumed, and the sale happened.\n","required":["id","amount","reason","status"],"properties":{"id":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","enum":["reservation","rental","event","damageBond","other"]},"status":{"type":"string","enum":["held","convertedToRevenue","returned","forfeited","partiallyForfeited"]},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"bookingId":{"type":"string","format":"uuid","nullable":true},"refundableUntil":{"type":"string","format":"date-time","nullable":true,"description":"**After which a forfeit is permitted rather than a return.** The date is the cancellation term, and a deposit with no date is refundable indefinitely.\n"},"liabilityAccountId":{"type":"string","format":"uuid"},"settledAt":{"type":"string","format":"date-time","nullable":true}}},
"DepositBox": {"type":"object","x-ticvai-persistence":"orders.deposit_box + orders.deposit_box_opening_denomination + orders.deposit_box_foreign_holding","description":"5.8. **Allocated to a cashier, not to a workstation.** A cashier moving between tills takes their float with them, which is what makes a variance attributable to a person.\n**`openingDenominations` and `foreignHoldings` are child rows** (26 September, pull audit R099): `orders.deposit_box_opening_denomination` and `orders.deposit_box_foreign_holding`, one row per item, keyed to the box. Until then the contract carried both and the table had nowhere to put either.\n","required":["cashierPrincipalId","venueId","openingFloat"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"cashierPrincipalId":{"type":"string","format":"uuid"},"cashierName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where it is being used now. **Changes during a shift; the box does not.**"},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The shift trading from this box. A UUIDv7, as `Shift.id` is."},"status":{"$ref":"#/components/schemas/DepositBoxStatus"},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openingDenominations":{"type":"array","description":"5.8.3. **Either this or a total** — a supervisor handing over a counted bag should not have to re-count it into fields. POS-001 offered only denominations until 14 August.\n","items":{"type":"object","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination`, as `CashCountLine.denominationId` does. Until 26 September this was `denomination: number` — a face value as a JSON float, which naming-and-style 5.1 forbids and which could disagree with the note it named (pull audit R122).\n"},"count":{"type":"integer","minimum":0}}}},"withdrawnTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Reduces the expected close figure.** Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier look short.\n"},"foreignHoldings":{"type":"array","description":"4.6.11 and 6.1.10. **Foreign cash accepted at this till, counted separately by currency.** A till taking USD and EUR alongside AED has three counts and three variances — collapsing them into a base-currency total makes a variance unattributable to the currency that caused it.\n**No opening float in a foreign currency and no change given in one.** Foreign cash only ever comes in, which is what keeps this to one number per currency rather than a full reconciliation each.\n","items":{"type":"object","required":["currency","countedAmount"],"properties":{"currency":{"type":"string","pattern":"^[A-Z]{3}$","description":"**Stored, because it is the one thing that is not the region's.** A foreign holding is by definition cash in a currency the till does not trade in, so it cannot resolve from the region (ADR-0018) the way the box's own amounts do; it is the key of the row, one per currency per box. The amounts on this item are in this currency.\n"},"expectedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The sum of tenders taken in this currency during the shift."},"countedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"baseEquivalent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**At the rates on the payments, not today's.** A shift closed on Friday and reviewed on Monday is reviewed at Friday's rates (CF-37).\n"}}}},"expectedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**Flagged where it is not the holder.** A box closed without its holder present is allowed — the cash is counted by somebody, and who counted it is the record.\n"},"allocatedAt":{"type":"string","format":"date-time","description":"When the device recorded the allocation. `allocateDepositBox` is offline-capable, so for a box allocated offline this differs from the server's receipt time.\n"},"closedAt":{"type":"string","format":"date-time","nullable":true}}},
"DepositBoxStatus": {"type":"string","enum":["allocated","open","suspended","closing","closed","reconciled"]},
"EntitlementStatus": {"type":"string","description":"**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n","enum":["issued","partiallyConsumed","fullyConsumed","expired","cancelled","surrendered"]},
"ExchangeOrderRequest": {"type":"object","required":["id","outgoingLineIds","incomingLines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."},"outgoingLineIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"incomingLines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"waiveFee":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"FinCreditMemo": {"x-ticvai-persistence":"ledger.credit_memo + ledger.credit_memo_line","type":"object","description":"5.7.94. **A tax credit note against one tax invoice**, with its own series. Never edited.","required":["id","creditMemoNumber","taxInvoiceId","kind","reason","legalEntityId","issuedAt","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"creditMemoNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's credit memo series, in sequence without gaps."},"taxInvoiceId":{"type":"string","format":"uuid"},"taxInvoiceNumber":{"type":"string","readOnly":true},"kind":{"type":"string","enum":["full","partial"]},"reason":{"type":"string","enum":["refund","cancellation","priceAdjustment","returnOfGoods","billingError","other"]},"refundId":{"type":"string","format":"uuid","nullable":true},"cancelledOrderId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid"},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"note":{"type":"string","nullable":true},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinCreditMemoLine"}},"scopePath":{"type":"string","readOnly":true}}},
"FinCreditMemoLine": {"type":"object","required":["invoiceLineNumber","netAmount","taxAmount","grossAmount"],"properties":{"invoiceLineNumber":{"type":"integer","minimum":1},"description":{"type":"string","maxLength":500},"quantity":{"type":"number","nullable":true},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxRate":{"type":"number"},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FinEInvoiceTransmissionStatus": {"type":"string","description":"6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.","enum":["notRequired","queued","sent","accepted","rejected","failed"]},
"FinIssueCreditMemoRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["kind","reason"],"properties":{"kind":{"type":"string","enum":["full","partial"]},"reason":{"type":"string","enum":["refund","cancellation","priceAdjustment","returnOfGoods","billingError","other"]},"refundId":{"type":"string","format":"uuid","nullable":true},"cancelledOrderId":{"type":"string","format":"uuid","nullable":true},"lines":{"type":"array","description":"Required for `partial`. Each names an invoice line and the quantity or amount credited.","items":{"type":"object","required":["lineNumber"],"properties":{"lineNumber":{"type":"integer","minimum":1},"quantity":{"type":"number","nullable":true},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"note":{"type":"string","maxLength":500,"nullable":true}}},
"FinIssueTaxInvoiceRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["invoiceType","orderIds"],"properties":{"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"orderIds":{"type":"array","minItems":1,"description":"One order for `simplified` and `full`; one or more for `consolidated`. Every order must be paid, of one buyer, one legal entity and one currency.","items":{"type":"string","format":"uuid"}},"recipient":{"$ref":"#/components/schemas/FinTaxInvoiceRecipient"},"languages":{"type":"array","description":"Overrides the template's languages for this document, within those the template offers.","items":{"type":"string","pattern":"^[a-z]{2}(-[A-Z]{2})?$"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true,"description":"A simplified invoice this full invoice replaces for the same supply. Refused unless the law allows it (make-or-break on issueTaxInvoice)."},"deliverToEmail":{"type":"string","format":"email","nullable":true,"description":"Sends the PDF on issue as well as returning it."}}},
"FinTaxCategory": {"type":"string","description":"How a line is treated for VAT. Taken from the tax code the line was posted with.","enum":["standardRated","zeroRated","exempt","outOfScope","reverseCharge"]},
"FinTaxDocumentRendition": {"x-ticvai-persistence":"none — a signed link to the stored PDF","type":"object","required":["documentId","documentKind","url","expiresAt"],"properties":{"documentId":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","creditMemo"]},"documentNumber":{"type":"string"},"language":{"type":"string","nullable":true},"contentType":{"type":"string","default":"application/pdf"},"url":{"type":"string","format":"uri"},"expiresAt":{"type":"string","format":"date-time"}}},
"FinTaxInvoice": {"x-ticvai-persistence":"ledger.tax_invoice + ledger.tax_invoice_line","type":"object","description":"5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.","required":["id","invoiceNumber","invoiceType","status","legalEntityId","issuedAt","supplyDate","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"invoiceNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."},"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"status":{"$ref":"#/components/schemas/FinTaxInvoiceStatus"},"legalEntityId":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"orderIds":{"type":"array","items":{"type":"string","format":"uuid"}},"supplierName":{"type":"string"},"supplierAddress":{"type":"string","nullable":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest the orders belong to; the key a guest's own reads filter on."},"buyerName":{"type":"string","nullable":true},"buyerAddress":{"type":"string","nullable":true},"buyerCountryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true},"customerAccountId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"supplyDate":{"type":"string","format":"date","description":"The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs, at the rate the orders were stored at."},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"languages":{"type":"array","items":{"type":"string"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The PDF rendered at issue; read through getTaxDocumentRendition."},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null where the platform issued it."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinTaxInvoiceLine"}},"taxSummary":{"type":"array","x-ticvai-persisted":false,"description":"VAT per rate and category, summed from the lines for the response.","items":{"type":"object","properties":{"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxRate":{"type":"number"},"taxableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."}}},
"FinTaxInvoiceLine": {"type":"object","description":"One line as it was sold and taxed. Amounts are in the invoice currency.","required":["lineNumber","description","quantity","netAmount","taxAmount","grossAmount","taxCategory"],"properties":{"lineNumber":{"type":"integer","minimum":1},"orderId":{"type":"string","format":"uuid"},"orderLineId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string","maxLength":500},"quantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true},"taxRate":{"type":"number","minimum":0,"maximum":100},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FinTaxInvoiceRecipient": {"x-ticvai-persistence":"none — copied onto the invoice as buyer columns","type":"object","description":"Who the invoice is addressed to. Required for `full` and `consolidated`.","required":["name"],"properties":{"name":{"type":"string","maxLength":300},"address":{"type":"string","maxLength":1000,"nullable":true},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"taxRegistrationNumber":{"type":"string","maxLength":30,"nullable":true,"description":"The recipient's TRN where they are VAT-registered."},"customerAccountId":{"type":"string","format":"uuid","nullable":true,"description":"The B2B credit account (payments `B2bCreditAccount`) where a company is invoiced."}}},
"FinTaxInvoiceStatus": {"type":"string","description":"`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).","enum":["issued","partiallyCredited","fullyCredited","superseded"]},
"FinTaxInvoiceType": {"type":"string","description":"5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.","enum":["simplified","full","consolidated"]},
"FinancialReport": {"x-ticvai-persistence":"none — computed from replica","type":"object","required":["report","fiscalPeriodId","currency","generatedAt","sections"],"properties":{"report":{"$ref":"#/components/schemas/FinancialReportKind"},"fiscalPeriodId":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer"},"generatedAt":{"type":"string","format":"date-time"},"sections":{"type":"array","items":{"type":"object","required":["name","lines","total"],"properties":{"name":{"type":"string"},"lines":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"accountCode":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"priorPeriodAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The same line for **the same period last year** (decided 28 September, audit R127 (3)). Absent where that period did not exist."}}}},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"FinancialReportKind": {"type":"string","description":"The report `getFinancialReport` returns. One vocabulary for the query and the response.","enum":["profitAndLoss","balanceSheet","cashFlow","revenueByVenue","revenueByProduct","taxSummary"]},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"GroupBooking": {"type":"object","x-ticvai-persistence":"orders.group_booking","description":"BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n","required":["id","orderId","leaderSubjectId","expectedSize","status"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["general","school","corporate","party"],"default":"general"},"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"quoteSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"riskAssessmentSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"preferredDate":{"type":"string","format":"date","nullable":true,"description":"The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. Null for a group a member of staff built from an order."},"orderId":{"type":"string","format":"uuid"},"leaderSubjectId":{"type":"string","format":"uuid"},"organisationName":{"type":"string","nullable":true},"expectedSize":{"type":"integer"},"confirmedSize":{"type":"integer","nullable":true},"minimumSize":{"type":"integer","nullable":true,"description":"**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"},"attendeeCaptureRequired":{"type":"boolean","default":false,"description":"**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["provisional","confirmed","namesPending","complete","cancelled"]}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"ManualDiscountRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineId":{"type":"string","format":"uuid","nullable":true,"description":"Omit to discount the order rather than a line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"percentage":{"type":"number","minimum":0,"maximum":100},"reason":{"type":"string","minLength":3,"maxLength":300,"description":"Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything.\n"},"reasonCode":{"type":"string","nullable":true,"description":"Optional alongside the free text, where the venue maintains a list."},"approverPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Required above the venue threshold. May not be the requester."},"recordedAt":{"type":"string","format":"date-time"}}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetDetail": {"x-ticvai-persistence":"assets.media_asset","allOf":[{"$ref":"#/components/schemas/MediaAsset"},{"type":"object","properties":{"derivatives":{"type":"array","description":"Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n","items":{"type":"object","properties":{"label":{"type":"string"},"width":{"type":"integer"},"height":{"type":"integer"},"sizeBytes":{"type":"integer"},"url":{"type":"string"}}}},"usage":{"type":"array","description":"Every place this asset is referenced.","items":{"$ref":"#/components/schemas/MediaUsage"}},"collections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"previousVersions":{"type":"array","items":{"type":"object","properties":{"version":{"type":"integer"},"replacedAt":{"type":"string","format":"date-time"},"replacedByPrincipalId":{"type":"string","format":"uuid"}}}}}}]},
"MediaEntitlements": {"type":"object","x-ticvai-persistence":"none — projection over entitlement and scan history","required":["mediaCode","isValid","entitlements"],"properties":{"mediaCode":{"type":"string"},"mediaKind":{"type":"string","enum":["qr","wristband","card","nfc","mobilePass"]},"subjectId":{"type":"string","format":"uuid","nullable":true},"isValid":{"type":"boolean"},"invalidReason":{"type":"string","nullable":true},"canAcceptMore":{"type":"boolean","description":"False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"},"entitlements":{"type":"array","items":{"type":"object","properties":{"entitlementId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["admission","locker","fnb","retail","parking","rental","experience","membership"]},"orderId":{"type":"string","format":"uuid"},"addedAt":{"type":"string","format":"date-time"},"status":{"allOf":[{"$ref":"#/components/schemas/EntitlementStatus"}],"description":"**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"transferredToSubjectId":{"type":"string","format":"uuid","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true}}}}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MediaReplaceResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","affectedSurfaces"],"properties":{"asset":{"$ref":"#/components/schemas/MediaAsset"},"affectedSurfaces":{"type":"integer","description":"How many surfaces now show the new file."},"liveSurfaces":{"type":"integer","description":"Of those, how many are published to guests right now."},"derivativesRegenerating":{"type":"boolean"}}},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"MediaUsage": {"x-ticvai-persistence":"assets.media_usage","type":"object","description":"One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n","required":["surface","referenceId"],"properties":{"extractedText":{"type":"string","description":"**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"surface":{"type":"string","enum":["tenantBranding","homepageBanner","promoBlock","contentPage","product","event","menuItem","merchandise","workOrder","incident","inspection","campaign"]},"referenceId":{"type":"string"},"label":{"type":"string"},"isLive":{"type":"boolean","description":"True where the referencing surface is published to guests."}}},
"ModifyOrderRequest": {"type":"object","required":["id","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"},"addLines":{"type":"array","items":{"$ref":"#/components/schemas/CreateOrderLine"}},"removeLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"NoSaleEvent": {"type":"object","x-ticvai-persistence":"orders.no_sale_event","required":["id","shiftId","reason","principalId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"reason":{"type":"string"},"note":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"},"countThisShift":{"type":"integer","description":"Running count. Returned so the terminal can show it — a cashier who can see they are on their ninth no-sale behaves differently from one who cannot.\n"}}},
"OpenShiftRequest": {"type":"object","required":["workstationId","openingFloat"],"properties":{"workstationId":{"type":"string","format":"uuid"},"openingFloat":{"$ref":"#/components/schemas/DenominationCount"},"depositBoxCode":{"type":"string","maxLength":64,"description":"Physical container assigned to this shift. Required where the venue configures deposit box allocation.\n"},"bagNumber":{"type":"string","maxLength":64,"description":"Required where the venue configures bag numbers as mandatory."},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are ordered against it.\n"}}},
"OrdChargebackAnalytics": {"x-ticvai-persistence":"none — computed from orders.chargeback and orders.payment on the reporting replica","type":"object","description":"4.2.21. Chargeback measures for a period, in total and per group.","required":["periodFrom","periodTo","groupBy","totals","groups"],"properties":{"periodFrom":{"type":"string","format":"date"},"periodTo":{"type":"string","format":"date"},"groupBy":{"type":"string"},"totals":{"$ref":"#/components/schemas/OrdChargebackMeasures"},"groups":{"type":"array","items":{"allOf":[{"$ref":"#/components/schemas/OrdChargebackMeasures"},{"type":"object","required":["key"],"properties":{"key":{"type":"string","description":"The reason, provider id, outcome, venue id, month (`YYYY-MM`), product id, product category id, or guest `subjectId` (`anonymous` for purchases with no guest) of the group."},"label":{"type":"string","nullable":true,"description":"The display name of the group's key. Null for `customer` unless the caller holds `GUEST_VIEW_PII`."}}}]}}}},
"OrdChargebackMeasures": {"x-ticvai-persistence":"none — computed","type":"object","properties":{"chargebackCount":{"type":"integer"},"chargebackAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"cardPaymentCount":{"type":"integer"},"chargebackRateByCount":{"type":"number","description":"Chargebacks received per card payment captured in the period, as a fraction."},"chargebackRateByValue":{"type":"number"},"decidedCount":{"type":"integer"},"wonCount":{"type":"integer"},"lostCount":{"type":"integer"},"acceptedCount":{"type":"integer"},"expiredCount":{"type":"integer","description":"Lost to a missed evidence deadline."},"winRate":{"type":"number","nullable":true,"description":"Won over decided (won, lost, expired); null with none decided."},"recoveredAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"feeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openCount":{"type":"integer"}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderModificationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["order","balanceDue"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"addedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"removedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest pays; negative means a refund is due."},"refundId":{"type":"string","format":"uuid","nullable":true},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderResumeResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","hasChanged"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"hasChanged":{"type":"boolean","description":"True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"},"changes":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["priceChanged","promotionExpired","promotionNowApplies","soldOut","seatHoldExpired","productWithdrawn"]},"lineId":{"type":"string","format":"uuid"},"detail":{"type":"string"},"wasAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nowAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"OrderStatement": {"x-ticvai-persistence":"none — computed from order, payment, refund and ledger","type":"object","required":["orderId","orderNumber","currency","entries","currentBalance"],"properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"entries":{"type":"array","description":"Sequential. What an agent reads to a guest asking about a charge.","items":{"type":"object","required":["kind","amount","runningBalance","occurredAt"],"properties":{"kind":{"type":"string","enum":["sale","payment","refund","void","modification","exchange","fee","variance","chargeback"]},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"referenceId":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}}},"totalPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRefunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"currentBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest owes; negative means a refund is outstanding."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductChangeImpact": {"type":"object","description":"1.4.4 and 1.4.16. What a proposed change would touch. **Modelled on `PerformanceCancellationResult`**, which does this for a cancellation.\n","required":["entitlementsIssued","ordersAffected","propagates"],"properties":{"entitlementsIssued":{"type":"integer","description":"How many live entitlements came from this product."},"ordersAffected":{"type":"integer"},"futurePerformances":{"type":"integer"},"openCarts":{"type":"integer","description":"**A guest with this product in a cart while its price changes underneath them** is the case nobody thinks about until it happens.\n"},"propagates":{"type":"boolean","description":"Whether the change reaches what has already been sold. **A name correction should; a price change must not**, and the difference is the whole reason this operation exists.\n"},"blockedBy":{"type":"array","description":"Reasons the change would be refused outright.","items":{"type":"string"}}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProductVariant": {"x-ticvai-persistence":"catalogue.variant","type":"object","required":["id","productId","sku","axisValues","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid"},"sku":{"type":"string"},"axisValues":{"type":"object","additionalProperties":{"type":"string"}},"name":{"type":"string","maxLength":150,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}` and no string a guest can read. A menu showing *Large* needs somewhere for the word to live.\n"},"barcode":{"type":"string","maxLength":64,"nullable":true,"description":"**Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a partner's own code for a variant and **requires `partnerId`**, so a manufacturer's EAN had nowhere to go. One per variant against many per variant is a different cardinality and belongs in a different place — and a POS scan should be an indexed column lookup, not a join.\n"},"isDefault":{"type":"boolean","default":false,"description":"Taken from their variant tables. Which variant a product page opens on. Ours had no way to say, so a three-size drink opened on whichever row sorted first.\n"},"isActive":{"type":"boolean","description":"False when retired. Retired variants are never deleted — orders reference them."},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"**Who this ticket type is for and what it includes**, shown behind the (i) on each Adult, Child, Senior or Infant row (decided 29 September, 23SEP-6). Each language value at most 300 characters; longer is a `400`. Set with `updateProductVariant`. Whether the guest screen shows it is `BookingFlowConfig.cardInfo` (white-label).\n"}}},
"ProductVersion": {"type":"object","x-ticvai-persistence":"catalogue.product_version","description":"1.1.47, 1.4.9 to 1.4.11. **Follows `white-label.ConfigVersion`** — the same pattern for the same reason, and the fourth place this mechanism was asked for.\n","required":["version","publishedAt","publishedByPrincipalId"],"properties":{"version":{"type":"integer"},"productId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true},"isCurrent":{"type":"boolean"},"contentHash":{"type":"string","description":"**Lets a diff be cheap and a no-op change be recognised.** Republishing an unchanged product should not create a version.\n"},"restoredFromVersion":{"type":"integer","nullable":true,"description":"Set where this version was created by a restore. **A restore is a new version, not a rewind** — a price that was wrong for three days stays visible, because a finance query run next quarter has to reproduce what was charged.\n"}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RefundPolicy": {"x-ticvai-persistence":"orders.refund_policy + orders.refund_policy_time_band","type":"object","description":"Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n**The three thresholds must ascend** (decided 28 September, audit R123 (6)): `selfAuthoriseLimit` <= `requiresSecondUserAbove` <= `requiresApprovalAbove`, where the second is set. `setRefundPolicy` refuses a policy that does not with 422 `refund-thresholds-not-ascending`.\n","required":["venueId","selfAuthoriseLimit","requiresApprovalAbove"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue in the path. Not taken from a `setRefundPolicy` body."},"selfAuthoriseLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser.\n"},"requiresSecondUserAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, a second user — cashier OR supervisor — names themselves as audit control. Dual-authorisation, not escalation (2.12.3).\n"},"requiresApprovalAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, an ORDER_REFUND_APPROVE holder must approve."},"timeBands":{"type":"array","description":"Refundable percentage by time before the performance. Evaluated most-specific first.\n","items":{"type":"object","required":["hoursBefore","percentage"],"properties":{"hoursBefore":{"type":"integer","minimum":0},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"allowPartial":{"type":"boolean","default":true},"refundWindowDays":{"type":"integer","nullable":true,"minimum":0,"description":"Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6))."},"varianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n**A venue setting with a tenant default** (decided 28 September, audit R094). **Proposed default, client to correct (audit R094): AED 5.00 per order line.**\n"}}},
"ReportCategory": {"type":"string","enum":["sales","admission","financial","inventory","guest","operations","marketing","workforce","compliance","custom"]},
"ReportColumn": {"x-ticvai-persistence":"reporting.report_column","type":"object","required":["field"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"label":{"type":"string"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"default":"none"},"sortOrder":{"type":"integer"},"sortDirection":{"type":"string","enum":["asc","desc"]},"format":{"type":"string","nullable":true}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportFilter": {"x-ticvai-persistence":"reporting.report_filter","type":"object","required":["field","operator"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","contains","isNull","isNotNull"]},"value":{"description":"**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"},"values":{"type":"array","description":"The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.","items":{}},"isParameter":{"type":"boolean","default":false,"description":"Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"}}},
"ReportParameter": {"x-ticvai-persistence":"reporting.report_parameter","type":"object","required":["key","label","type","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"},"isRequired":{"type":"boolean"},"defaultValue":{"description":"Open on purpose. A value of this parameter's `type`, used when a run supplies none."}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"Settlement": {"x-ticvai-persistence":"ledger.settlement","type":"object","required":["id","providerName","periodStart","periodEnd","status","ingestedAt"],"properties":{"id":{"type":"string","format":"uuid"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","description":"**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"},"providerName":{"type":"string"},"venueId":{"type":"string","format":"uuid","description":"The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."},"periodStart":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"periodEnd":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"fileReference":{"type":"string","format":"uuid","description":"The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"},"format":{"type":"string","nullable":true,"enum":["csv","fixedWidth","xml","json"],"description":"The file format given at ingest. Null when none was given."},"status":{"$ref":"#/components/schemas/SettlementStatus"},"lineCount":{"type":"integer"},"matchedCount":{"type":"integer"},"exceptionCount":{"type":"integer"},"providerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerFees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerNet":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ledgerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ingestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"}}},
"SettlementException": {"x-ticvai-persistence":"ledger.settlement_exception","type":"object","required":["id","settlementId","kind","providerReference","amount"],"properties":{"id":{"type":"string","format":"uuid","description":"Server-created when parsing finds the exception, so a UUID (naming-and-style 4)."},"settlementId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["unmatchedInProvider","unmatchedInLedger","amountMismatch","duplicateInProvider","feeUnexplained"]},"providerReference":{"type":"string","nullable":true},"paymentId":{"type":"string","format":"uuid","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expectedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"resolution":{"allOf":[{"$ref":"#/components/schemas/SettlementResolution"}],"nullable":true,"description":"Null while the exception is open."},"note":{"type":"string","nullable":true,"description":"The `note` given to `resolveSettlementException`, stored with the resolution."},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"SettlementResolution": {"type":"string","description":"How a settlement exception was explained. One vocabulary for the request and the stored exception.","enum":["matchedManually","writeOff","disputeRaised","providerError","timingDifference"]},
"SettlementStatus": {"type":"string","enum":["ingesting","parsing","matching","matched","hasExceptions","resolved","failed"]},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included."},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftCloseResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["shift","expectedCash","countedCash","variance","requiresAcceptance"],"properties":{"shift":{"$ref":"#/components/schemas/Shift"},"expectedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Counted minus expected. Negative is short."},"requiresAcceptance":{"type":"boolean","description":"True when the variance exceeds the venue's `shiftVarianceThreshold` (audit R094). The shift is then `pendingVariance` and only `acceptShiftVariance` finalises it (audit R080 (e)).\n"},"nonCashVariances":{"type":"array","items":{"type":"object","required":["tender","declared","captured","variance"],"properties":{"tender":{"type":"string"},"declared":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"captured":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]},
"TicketReissueFulfillmentRegenerationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Ticket Reissue & Fulfillment Regeneration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumReissues":{"type":"string","description":"Maximum Reissues"},"freeReissueCount":{"type":"integer","description":"Free Reissue Count"},"supervisorThreshold":{"type":"integer","description":"Supervisor Threshold"},"reissueReason":{"type":"string","enum":["dateChanged","timeslotChanged","seatChanged","attendeeChanged","lostTicket","damagedCredential","emailNotReceived","walletPassIssue","printingError","credentialCompromised","administrativeCorrection"],"description":"Why the ticket is reissued."},"credentialMedia":{"type":"string","enum":["qr","dynamicQr","barcode","rfid","nfc","printedTicket","wearable"],"description":"Credential media regenerated."},"deliveryMethod":{"type":"string","enum":["email","smsWhatsappLink","mobileApp","walletPass","walletUpdate","posPrint","boxOfficeCollection"],"description":"How the reissue is delivered."},"reissueOption":{"type":"string","enum":["regenerateNew","resendExisting"],"description":"Regenerate a new credential (old one invalidated) or resend the existing one"}}},
"UpdateGroupBookingRequest": {"type":"object","description":"Request only. Every field optional; absent means unchanged.","properties":{"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"leaderSubjectId":{"type":"string","format":"uuid"},"organisationName":{"type":"string","maxLength":200,"nullable":true},"expectedSize":{"type":"integer","minimum":2},"confirmedSize":{"type":"integer","minimum":0},"minimumSize":{"type":"integer","minimum":1,"nullable":true},"attendeeCaptureRequired":{"type":"boolean"},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["confirmed","namesPending","complete","cancelled"]}}},
"UpdateProductRequest": {"type":"object","minProperties":1,"properties":{"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"The product family across the tenant's venues (decided 29 September, rev 3 REV3-18); see `Product.familyKey`. At most one product per venue in a family, else `409 duplicate-code`."},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"dataMaskValues":{"type":"object","additionalProperties":true},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"See `Product.salesContact` (W3, 29 September)."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"See `Product.bookingFlowId` (W8, W12, 29 September)."},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"}},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"}},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"}},"requiresTimeWindow":{"type":"boolean"}}},
"VariantDimension": {"x-ticvai-persistence":"catalogue.variant_dimension","type":"object","description":"**A length is an axis like any other** (decided 29 September, rev 3 REV3-13). A meeting room type sold by the hour has an axis `length` with values `1h`, `2h`, `halfDay`, `fullDay`, each carrying `durationMinutes` (proposed 60, 120, 240 and 480, client to correct), and each generated variant is priced on its own, so a half day need not cost four single hours.\n","required":["code","name","values"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"values":{"type":"array","minItems":1,"items":{"type":"object","required":["code","label"],"properties":{"code":{"type":"string","maxLength":64},"label":{"type":"string","maxLength":200},"priceDelta":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"durationMinutes":{"type":"integer","minimum":15,"maximum":1440,"nullable":true,"description":"How long a variant carrying this value books its space for, on a `length` axis of a product with `requiresTimeWindow` (decided 29 September, rev 3 REV3-13). Null on any other axis. One axis per product at most may carry it; a second is a `400`."}}}}}},
"VoidReason": {"type":"string","description":"**The void reason list** (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. `other` requires a note (audit R222), and the notes are reviewed quarterly to add real reasons. Proposed, client to correct.\n","enum":["guestChangedMind","enteredInError","itemUnavailable","qualityIssue","duplicate","other"]},
"WithdrawalReason": {"type":"string","description":"Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.","enum":["banking","safeDrop","changeOrder","other"]}
}
```
