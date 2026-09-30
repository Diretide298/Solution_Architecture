# TICVAI — Nomenclature Standard

**Version:** 1.0
**Scope:** All five repositories. Binding.
**Owner:** Architecture (Chinmay)

---

## 1. The Rule

**One concept, one name, everywhere.** A term is chosen once in the glossary and carries
through the contract, the database, the code and the screen label. Only the *casing*
changes between layers. The word never does.

This exists because the platform spans 21 domains, 118 sub-domains and a reference system
that loaded specific meanings onto ordinary words. Without a naming discipline, every
review conversation costs ten minutes of disambiguation for two years, and the same
concept ends up modelled twice under different names.

---

## 2. Case Conventions by Layer

| Layer | Convention | Example |
|---|---|---|
| Glossary (canonical) | Title Case, singular | `Access Point` |
| OpenAPI schema name | PascalCase, singular | `AccessPoint` |
| JSON field | camelCase | `accessPointId` |
| URL path segment | kebab-case, **plural** | `/access-points` |
| Query parameter | camelCase | `?accessPointId=` |
| C# type | PascalCase | `AccessPoint` |
| C# property | PascalCase | `AccessPointId` |
| TypeScript type | PascalCase | `AccessPoint` |
| TypeScript variable | camelCase | `accessPointId` |
| Python class | PascalCase | `AccessPoint` |
| Python variable | snake_case | `access_point_id` |
| SQL table | snake_case, **singular** | `access_point` |
| SQL column | snake_case | `access_point_id` |
| Event type | dot.lower.versioned | `access.scan.recorded.v1` |
| Permission | SCREAMING_SNAKE | `ACCESS_POINT_CONFIGURE` |
| UI label | Sentence case, human | `Access point` |

**Tables are singular, URL collections are plural.** `access_point` the table,
`/access-points` the collection. Both conventions are defensible in isolation; mixing
them arbitrarily within a layer is not.

---

## 3. Canonical Domain Terms

These carry platform-specific meaning. **Never substitute a synonym**, however natural it
sounds.

| Canonical | Means | Never write |
|---|---|---|
| **Event** | A named happening that has one or more Performances | Show, Session, Occasion |
| **Performance** | A dated, timed instance of an Event | Showtime, Session, Slot, Occurrence |
| **Product** | The sellable thing (decided 28 September, audit R131) | Item (bare), Article, Offering |
| **Menu Item** | An F&B Product variant as a menu sells it (`MenuItem`) | Dish, F&B item |
| **Merchandise Item** | A retail Product variant as a shop sells it (`MerchandiseItem`) | Retail item, Article |
| **Inventory Item** | A stock record the venue counts, buys and consumes. **Not a Product** (`InventoryItem`) | Stock item |
| **SKU** | A variant's stock-keeping code. A field (`sku`), never an entity | SKU for the Product |
| **Component** | A part of a Product's definition | Element, Part, Piece |
| **Attribute** | An axis that generates Product variants | Option, Variant, Property, Modifier |
| **Envelope** | A capacity allocation container | Pool, Bucket, Quota, Allocation |
| **Entitlement** | The right a holder has, separate from identity | Permission, Right, Access, Grant |
| **Media** | The physical or digital carrier of a Ticket | Card (except Game Card, Gift Card), Wristband, Pass, Carrier |
| **Media Code** | The identifier on the Media. **≠ Ticket ID** | Barcode, QR (except guest copy), Serial, Card number |
| **Ticket** | The issued instrument granting entitlement | Pass, Admission, Voucher |
| **Order** | A completed commercial transaction | Booking (except guest labels), Sale, Purchase, Basket |
| **Reservation** | A held, not-yet-paid commitment. **≠ Order** | Booking, Hold (except labels, see 3.3), Provisional order |
| **Data Mask** | Configurable custom-field definition set | Custom fields, Extra fields, Metadata |
| **Metric Sheet** | The grid defining product/price relationships | Matrix, Grid, Price table |
| **Operating Area** | A grouping of Workstations by function | Zone, Section |
| **Department** | A functional area within a Venue. **Canonical** (decided 28 September, audit R194) | Section |
| **Zone** | A physical area inside a Venue: dining, access, seating, queue (decided 28 September, audit R194) | Zone for an Operating Area |
| **Access Point** | A physical validation location | Gate, Entry, Turnstile, Door |
| **Workstation** | A configured device instance. Staff copy may say *till* (audit R156) | Terminal, Station, Till or POS in code |
| **Sale Board** | The configured front-end a Workstation loads | Screen, Layout, Menu, Interface |
| **Admission Profile** | Rules governing entry for an entitlement | Access rules, Entry policy |
| **Org Unit** | A node in the tenant hierarchy (`OrgUnit`, renamed from Scope Node 26 August; accepted audit R194). Used for authorisation, it is a scope | Scope Node (retired), Level, Node |
| **Cell** | One tenant in one jurisdiction | Instance, Stamp, Deployment, Region |
| **Deposit Box** | The cash container assigned to a shift. *Till* never means this | Drawer (in code), Float, Till |
| **Kitchen Ticket** | The order slip on the kitchen display (`KitchenTicket`). Not a Ticket (decided 28 September, audit R210) | Chit, Docket, Ticket (bare) |
| **Game Card** | A card loaded with game credits (`GameCard`). Recorded exception to *Card* (audit R220) | Play card |
| **Gift Card** | A stored-value card bought as a gift (`GiftCard`). Recorded exception to *Card* and *Money Card* (audit R220) | Gift voucher |
| **Principal** | An authenticated actor | User, Account, Login |
| **Subject** | A person referenced from the ledger by opaque ID | Customer, Guest, Person |

### 3.1 The three that get confused most

| | Order | Reservation | Ticket |
|---|---|---|---|
| Paid | Yes | Not necessarily | N/A |
| Creates entitlement | Yes | No | Is the instrument |
| Can expire | No | Yes | Yes |
| Posts to ledger | Yes | No | No |

Conflating these is the single most common modelling failure in ticketing systems. They
are three entities with three lifecycles.

### 3.2 Ticket ID ≠ Media Code

Settled 07 Aug 2026. A Ticket may be re-linked to different Media over its life; the
Media Code changes, the Ticket ID does not. Any code that treats them as one field is
wrong.


### 3.3 Recorded exceptions (decided 28 September)

A banned word may appear only where this list allows it. **Code, contracts and DDL never take one unless the row says so.** The full glossary, including the domain nouns proposed under audit R146 (Attraction, Queue, Wait Time, Itinerary, Accreditation, Form, Settlement, Reconciliation, Report, Channel, Work Order, Segment, Campaign, Journey, Category, Tile), is `docs/glossary.md`.

| Word | Allowed in | Audit |
|---|---|---|
| Booking | Guest-facing labels only (*Booking Confirmation*, *Group Booking*) | R145 |
| Release hold | Labels. Code says Reservation | R145 |
| Till | Staff-facing copy, meaning the Workstation only | R156 |
| POS, drawer | Staff-facing copy. Never code, contracts or DDL | R156 |
| QR | Guest-facing copy only (GST-055 *Dynamic QR Ticket*) | R210 |
| Game Card, Gift Card | Everywhere, code included (`GameCard`, `GiftCard`, `cardCode`) | R220 |

---

## 4. Identifiers

| Use | Type | Why |
|---|---|---|
| Every entity, wherever it is created | **`uuid`**, new values **UUIDv7** | One id type (ADR-0056). Minted by the application, `Id.New()` on the server or `newId()` on a device; offline devices generate IDs before the server sees them, and the id doubles as the idempotency key; time-ordered so index locality is preserved without a central allocator |
| Human code (order number, ticket code) | **text**, its own column | People read and type it; it is not the id and never stands in for one |
| Scope node addressing | **ltree path** | Ancestor queries without recursive CTEs |
| Outbox sequence | `bigserial` | Single-writer, ordering is the point |
| **Anything on a partitioned table** | **Never `bigserial`** | A shared sequence is a contention point |

Suffix `Id` / `_id` always. Never bare `id` on a foreign key column.

---

## 5. Money, Time and Scope

### 5.1 Money

Always the `Money` type — `{ amount, currency, scale }`.

- **Never** a float, in any language, at any layer
- **Never** a fixed `decimal(18,2)` — OMR uses 3 decimal places, AED uses 2
- SQL columns are `numeric(18,4)` and hold the amount only. **Currency and scale are not stored per row; they resolve** from what denominates the amount (ADR-0018): a ledger posting from `ledger.account.currency`, a payment from its `tender_currency`, a wallet from `wallet.wallet.currency`, everything else from the venue's frozen trading currency. Only tables whose currency genuinely differs from their venue store one (`orders.payment`, `inventory.supplier`, `ledger.account`, `control.partner_agreement`, `ledger.settlement`). They stay on the wire, so a client never walks a hierarchy to read a figure (24 September)
- Wire format is a decimal **string**

Column naming: `gross_amount`, `net_amount`, `tax_amount`, `refunded_amount`. Never
`price`, `value`, `total` alone — they don't say gross or net.

A price somebody enters (a menu item, a merchandise item, a bundle, a licence) is `list_price`: whether it includes tax is set by the tax rule's `taxInclusive`, not by the column, so gross or net would be wrong for some venues. A calculated `subtotal` is `net_amount` and a `total` is `gross_amount`. When the contract's field keeps its wire name, `x-ticvai-column` on the field names the column (24 September: 27 columns renamed this way, listed in `handoff/money-column-names.md`).

### 5.2 Time

All instants are `timestamptz` in UTC, rendered at the edge in the Region's zone.
`DateTime.Now` is banned at compile time.

| Column | Means |
|---|---|
| `created_at` | Row written to this database |
| `recorded_at` | The device recorded the business event. **Differs from `created_at` for offline operations** |
| `synced_at` | Reached the server. Null while pending |
| `occurred_at` | Domain event happened |
| `valid_from` / `valid_to` | Business validity window |
| `effective_at` | When a configuration change takes effect |

`recorded_at` vs `synced_at` is not pedantry — the 31 Jul offline architecture requires
both, and reporting that uses the wrong one misstates revenue by trading day.

### 5.3 Scope

Every tenant-scoped table carries `scope_path ltree` plus the denormalised
`venue_id`, `region_id`, `brand_id` needed for partitioning and reporting.

`scope_path` (and any `*_scope_path`) is typed `ltree` in the DDL, indexed with GiST, and row-level security compares it with `<@`. So a row is visible to a grant at or above it. **A venue-scoped user sees its venue's rows and not tenant-level ones** (`venue_id` null, path at the tenant), which sit above the venue: a venue's list excludes head-office records unless the operation says otherwise. Head-office users see everything beneath them (decided 24 September).

---

## 6. Structural Naming

### 6.1 Database

| Object | Pattern | Example |
|---|---|---|
| Table | `<singular_noun>` | `sales_order` |
| Join table | `<a>_<b>` alphabetical | `order_entitlement` |
| Primary key | `id` | — |
| Foreign key | `<referenced_table>_id` | `venue_id` |
| Index | `<table>_<columns>_idx` | `sales_order_venue_created_idx` |
| Unique index | `<table>_<columns>_uniq` | `sales_order_idempotency_uniq` |
| Check constraint | `<table>_<column>_chk` | `sales_order_amount_chk` |
| Partition | `<table>_v<venue_number>` | `sales_order_v003` |
| RLS policy | `<table>_scope` | `sales_order_scope` |
| Enum type | `<concept>` singular | `scope_level` |

Boolean columns read as assertions: `is_active`, `has_refund`, `can_reenter`,
`requires_approval`. Never `active`, `flag`, `status_bool`.

### 6.2 API

| Object | Pattern | Example |
|---|---|---|
| Collection | `/<plural-kebab>` | `/sales-orders` |
| Item | `/<plural>/{id}` | `/sales-orders/{orderId}` |
| Sub-resource | `/<plural>/{id}/<plural>` | `/sales-orders/{orderId}/refunds` |
| Action *(only when not a resource)* | `/<plural>/{id}/<verb>` | `/sessions/{id}/force-logout` |
| operationId | camelCase verbNoun | `createSalesOrder` |

Prefer resources over actions. `POST /orders/{id}/refunds` beats
`POST /orders/{id}/refund` — the refund is a thing, not only an act.

### 6.3 Events

`<aggregate>.<pastTenseVerb>`, the version in the event's `version` field

`access.validated` · `device.enrolmentChanged` · `order.paid` · `ledger.entryPosted`

Past tense, always. Events are facts, not commands. **The version is in the payload, not the name**
(`events/_schema.yaml`: `version: 1`): adding a field is a minor, safe change; removing or reshaping one
means a new version published alongside the old one until every consumer has moved, never a silent
reshape. Decided 1 October 2026 (Chinmay): the rule follows the 77 events the package already has,
rather than renaming them and every consumer.

### 6.4 Permissions

`<DOMAIN>_<ACTION>[_<QUALIFIER>]`

`ORDER_CREATE` · `ORDER_REFUND` · `ORDER_REFUND_APPROVE` · `SHIFT_CLOSE_OTHER` ·
`SESSION_FORCE_LOGOUT` · `ACCESS_POINT_CONFIGURE`

**Generated from one enum in `ticvai-contracts`** and consumed by backend authorisation,
frontend navigation filtering and AI scoping. If the frontend spells a permission
differently from the backend, a supervisor sees a button that returns 403 — a bug that is
invisible in code review and obvious in production.

---

## 7. Banned Words

Words that describe nothing. If one is the clearest name available, the abstraction is
wrong.

| Banned | Why | Instead |
|---|---|---|
| `Manager`, `Helper`, `Util`, `Service` *(bare)* | Says nothing about responsibility | `OrderPricingCalculator`, `RefundAuthoriser` |
| `Data`, `Info`, `Details` | Every object holds data | `OrderSummary`, `GuestProfile` |
| `Process`, `Handle`, `Do` | No semantics | `PostToLedger`, `ValidateEntitlement` |
| `temp`, `tmp`, `foo`, `test1` | Ship in production, always | Name the thing |
| `flag` | Doesn't say what is true | `is_refundable` |
| `misc`, `other`, `extra` | A design gap wearing a name | Model it properly |
| `new`, `old`, `v2` in a type name | Meaningless in six months | Name by behaviour |

---

## 8. Enforcement

| Layer | Mechanism | Blocking |
|---|---|---|
| Canonical terms | Review checklist + glossary in `ticvai-contracts` | Gate 1 contract review |
| C# banned symbols | `BannedSymbols.txt` + `BannedApiAnalyzers` | **Compile error** |
| Permission strings | Generated enum, single source | **Compile error on drift** |
| SQL naming | Migration review checklist | PR review |
| API naming | Redocly ruleset | **CI** |
| Case conventions | `.editorconfig`, ESLint, Ruff | **CI** |

New canonical terms are added by PR to the glossary, reviewed by Architecture. A term in
code that is not in the glossary is a review finding.
