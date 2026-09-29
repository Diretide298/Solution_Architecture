# Glossary

> **Purpose:** Canonical domain vocabulary  
> **Owner:** Chinmay + Allam  
> **Status:** **Draft — needs client sign-off**


**One concept, one name, everywhere.** Only casing changes between layers. The word never does.

Sources: client-supplied reference definitions · MoM decisions 30 Jul – 12 Aug 2026 · the requirement matrix · the Block A pull audit decisions of 28 September 2026 (`handoff/audit-decisions.json`).

**Two kinds of entry since 28 September.** Terms marked *decided 28 September* were settled when Chinmay adopted the audit defaults. Terms marked *proposed, client to approve (audit R146)* were drafted from how the contracts already use the noun; each stands until the client corrects it.

---

## Catalogue & product

| Term | Definition | Never say |
|---|---|---|
| **Event** | A named happening that has one or more Performances. Carries the identity a guest-app recognises | Show, Occasion |
| **Performance** | A dated, timed instance of an Event. The thing capacity attaches to. **"Session" in the design** (Session Calendar, Session Template, session time, the resources manifest) **means a Performance** (decided 28 September, audit R165): `PerformanceTemplate`, `/performances/{performanceId}/manifest`. **Guest-facing copy may say "session"** (decided 29 September, rev 3 CFG-10; see Recorded exceptions) | Showtime, Session (except guest-facing copy), Slot |
| **Product** | The sellable thing. May be a ticket, membership, rental or bundle, and it is what a Menu Item or a Merchandise Item sells (decided 28 September, audit R131) | Item (bare), Article |
| **Menu Item** | An F&B Product variant as it appears on a menu: its name, price, station and modifiers. `MenuItem` in `fnb.yaml`, pointing at a `productVariantId` (decided 28 September, audit R131) | Dish, F&B item |
| **Merchandise Item** | A retail Product variant as a shop sells it, with its SKU, barcode and return rules. `MerchandiseItem` in `retail.yaml` (decided 28 September, audit R131) | Retail item, Article |
| **Inventory Item** | A stock-keeping record for something the venue counts, buys and consumes: an ingredient, a consumable or the stock behind a Merchandise Item. **Not a Product**: an ingredient is never sold. `InventoryItem` in `inventory.yaml` (decided 28 September, audit R131) | Stock item, Ingredient (as a type name) |
| **SKU** | A Product variant's stock-keeping code. **A code, never the thing**: `sku` is a field, not an entity (decided 28 September, audit R131) | SKU for the Product itself |
| **Category** | A node in a hierarchy that groups Products for navigation, reporting and defaults: `ProductCategory` in `catalogue.yaml`, with parent and child. Scoped variants (`RentalCategory`, `ReportCategory`) group within their own module. **Not a Seat Category**, which prices a seat. *Proposed, client to approve (audit R146)* | Department (for products), Group |
| **Component** | A constituent part of a Product's definition | Element, Part |
| **Attribute** | An axis that generates Product variants. Adding an attribute value auto-creates sellable variants | Option, Variant, Modifier |
| **Metric Sheet** | The grid defining product-to-price relationships across axes | Matrix, Grid, Price table |
| **Price List** | A named set of prices, scoped by channel, season or calendar | Tariff, Rate card |
| **Envelope** | A capacity allocation container. Combines with Space Structure and Seat Category to form capacity | Pool, Bucket, Quota |
| **Capacity Allocation** | Space Structure + Seat Category + Envelope | Inventory, Availability |
| **Channel** | Where a sale came from: POS, kiosk, web, mobile, B2B, OTA, call centre, guest app, partner, API or back office. The shared `SalesChannel` in `common.yaml` is the reporting dimension used for attribution, promotion eligibility and settlement. *Proposed, client to approve (audit R146)* | Source, Outlet (for the channel) |

## Sale & entitlement

| Term | Definition | Never say |
|---|---|---|
| **Order** | A completed commercial transaction. Posts to the ledger. Creates entitlement | Booking (in code), Sale, Basket |
| **Reservation** | A held, not-yet-paid commitment. Expires. **Not an Order** | Booking (in code), Hold (in code) |
| **Ticket** | The issued instrument granting entitlement. Has a stable Ticket ID | Pass, Admission, Voucher |
| **Entitlement** | The right a holder has. **Separate from identity** — settled 05 Aug 2026 | Permission, Right, Access |
| **Media** | The physical or digital carrier of a Ticket — card, wristband, phone, print | Card (except Game Card and Gift Card), Pass, Carrier |
| **Media Code** | The identifier written on the Media. **≠ Ticket ID** — settled 07 Aug 2026. Media can be re-linked; the Ticket ID does not change | Barcode, QR (in code and staff copy), Serial |
| **Money Card** | A Ticket used as a stored-value instrument | Wallet card |
| **Gift Card** | A stored-value card bought to be given, with a face value and a balance. `GiftCard` in `wallet.yaml`. **A recorded exception** to *never write Card* and to *Money Card*, kept because guests know it by this name (decided 28 September, audit R220) | Gift voucher |
| **Game Card** | The card a guest loads with credits, bonus credits and points to play games and rides. `GameCard` in `games.yaml`. **A recorded exception** to *never write Card* (decided 28 September, audit R220) | Play card, Arcade card |
| **Settlement** | A payment provider's statement for a period, ingested and matched line by line against the ledger: its gross, fees, net and exceptions. `Settlement` in `finance.yaml`. *Proposed, client to approve (audit R146)* | Payout (for the statement), Remittance |
| **Reconciliation** | The act of matching a Settlement's lines to the platform's payments under the configured matching rules, and resolving what does not match. `ReconciliationSource` and `ReconciliationMatchingRules` in `payments.yaml`. *Proposed, client to approve (audit R146)* | Recon, Matching (as a noun) |

### The three that get confused

| | Order | Reservation | Ticket |
|---|---|---|---|
| Paid | Yes | Not necessarily | n/a |
| Creates entitlement | Yes | No | Is the instrument |
| Can expire | No | Yes | Yes |
| Posts to ledger | Yes | No | No |

Conflating these is the most common modelling failure in ticketing systems.

## Access

| Term | Definition | Never say |
|---|---|---|
| **Access Point** | A physical validation location. Inherited by a Workstation, never selected by the operator | Gate, Entry, Door |
| **Admission Profile** | The rules governing entry for an entitlement — times, re-entry, deny rules | Access rules, Entry policy |
| **Anti-Passback** | Prevention of the same Media being used to enter twice without an exit | — |
| **Rotation** | A turnstile pass event. Modes: entry, re-entry, crossover, exit, free rotation, closed | Turn, Pass |
| **Fast Pass** | An **entitlement with a consumption counter**, spanning access, F&B and queue. Not a queue feature | Skip-the-line, Express |
| **Accreditation** | The approved right of a named person, usually applying through an organisation, to be at an event or venue in a given category, with a validity and the access it grants. The programme, the application, the holder and the credential are separate things: reissuing a credential re-vets nobody. `accreditation.yaml`. *Proposed, client to approve (audit R146)* | Badge (for the accreditation itself), Pass |

## Attractions & queues

| Term | Definition | Never say |
|---|---|---|
| **Attraction** | A ride, game or experience a guest queues for or enters: a Product with an Attraction Type that decides which settings apply (height restriction, cycle time, payout). *Proposed, client to approve (audit R146)* | Ride (as the type name), Experience |
| **Queue** | The line for one Attraction, physical or virtual, with a status (open, paused, closed, at capacity), its waiting parties and the entries it calls. `Queue` in `queue.yaml`. *Proposed, client to approve (audit R146)* | Line, Lane (for the queue) |
| **Wait Time** | The current estimated wait for a Queue in minutes, with its source (measured feed, statistical, manual) and the time it was true. A stale figure says so. `WaitTime` in `queue.yaml`. *Proposed, client to approve (audit R146)* | Queue time, ETA |
| **Itinerary** | A guest's ordered plan for a visit: Attractions, shows and meals with times, built by the guest or suggested by the AI. Not a Reservation and not an Order: it holds no capacity. *Proposed, client to approve (audit R146)* | Day plan (in code), Schedule |

## F&B & kitchen

| Term | Definition | Never say |
|---|---|---|
| **Kitchen Ticket** | The order slip for one Order's F&B lines at one kitchen station, as the kitchen display shows it, with its status, priority and coursing. `KitchenTicket` in `fnb.yaml`. **Its own term, not a Ticket**: it grants no entitlement (decided 28 September, audit R210) | Chit, Docket, Ticket (bare) |

## Organisation & operations

| Term | Definition | Never say |
|---|---|---|
| **Tenant** | Top-level entity owning all Brands. One per commercial client | Client, Customer, Org |
| **Brand / Organisation** | Groups similar business types within a Tenant. May span jurisdictions | Division |
| **Region / Branch** | Geographic grouping. **Owns currency, decimals, date format, time zone, fiscal year** — inherited by all Venues beneath | Area, Territory |
| **Venue** | Isolated configuration and operations unit. Admin access scopes here | Site, Park, Property |
| **Department / Sub-Department** | Functional areas within a Venue — Ticketing, F&B, Retail, B2C, B2B, OTA. **Canonical** (decided 28 September, audit R194): `departmentId` in workforce, tenancy and inventory is correct | Section |
| **Zone** | A physical area inside a Venue: a dining zone, an access zone, a seating zone, a queue zone. **A place, not a grouping of Workstations** (decided 28 September, audit R194) | Zone for an Operating Area |
| **Workstation** | A configured device instance. Determines Sale Board, hardware, till identity, Access Point, reporting dimension. **Never authorisation**. Staff-facing copy may call it a *till* (decided 28 September, audit R156) | Terminal, Station, POS or Till (in code) |
| **Operating Area** | A grouping of Workstations by function | Zone, Section |
| **Sale Board** | The configured front-end a Workstation loads — ticketing, F&B or retail | Screen, Layout, Menu |
| **Org Unit** | A node in the seven-level hierarchy, addressed by ltree path. Renamed from *Scope Node* on 26 August: **the org unit is the thing; a scope is what you get when you use one for authorisation** (`OrgUnit`, `orgUnitId` in `tenancy.yaml`; accepted 28 September, audit R194) | Scope Node (retired), Level, Node |
| **Cell** | One Tenant in one jurisdiction. The deployment unit | Instance, Stamp, Region |
| **Deposit Box** | The cash container assigned to a shift. **"Till" never means the Deposit Box** (decided 28 September, audit R156) | Drawer (in code), Float, Till |
| **Cash Lift** | Mid-shift removal of cash from an open float, traced | Pickup, Drop |
| **Blind Close-Out** | Shift close where the operator counts without seeing the expected figure | — |
| **Work Order** | A unit of maintenance work on an Asset or a location: raised, assigned, timed, completed and, where required, verified by someone other than the technician. `WorkOrder` in `maintenance.yaml`. *Proposed, client to approve (audit R146)* | Job, Ticket (for the work), Task |
| **Form** | A configured set of fields a guest completes and the platform keeps as evidence: a waiver is a Form with a signature, a survey a Form with a scale, a data capture a Form at the point of sale. Versioned; a submission is bound to the version accepted. `FormDefinition` in `marketing-crm.yaml`. *Proposed, client to approve (audit R146)* | Questionnaire, Template (for the form) |

## Marketing & reporting

| Term | Definition | Never say |
|---|---|---|
| **Segment** | A named, rule-defined set of guests (Subjects), re-evaluated from criteria rather than listed by hand, used to target Campaigns and Journeys. `Segment` in `marketing-crm.yaml`. *Proposed, client to approve (audit R146)* | Audience (as the entity), List |
| **Campaign** | One marketing send to a Segment — one-off, scheduled, triggered or recurring — with its content, budget and performance. `Campaign` in `marketing-crm.yaml`. *Proposed, client to approve (audit R146)* | Blast, Mailing |
| **Journey** | A sequence of messages with branches, where the next step depends on what the guest did about the last one; entered on an event and checked for consent at every send. `Journey` in `marketing-crm.yaml`. *Proposed, client to approve (audit R146)* | Flow, Workflow (for marketing), Automation |
| **Report** | A saved definition of a question over platform data — its fields, filters, grouping and parameters — which is run, scheduled and exported. The definition is versioned so a past result stays reproducible. `ReportDefinition` in `reporting.yaml`. *Proposed, client to approve (audit R146)* | Query, Extract |
| **Tile** | One visual on a dashboard, bound to one Report with its parameters, visualisation and refresh interval. `DashboardTile` in `reporting.yaml`. *Proposed, client to approve (audit R146)* | Widget, Card, Panel |

## Identity & configuration

| Term | Definition | Never say |
|---|---|---|
| **Principal** | An authenticated actor holding permissions | User, Account, Login |
| **Subject** | A person referenced from the ledger by opaque ID. PII lives separately and is erasable | Customer, Guest, Person |
| **Role** | A named grouping of Principals for permission management. **Fully configurable; nothing predefined** — 12 Aug 2026. The seeded role templates proposed in `docs/active/seed-data-proposal.md` are a starting point a tenant edits, not fixed roles | Group, Profile |
| **Data Mask** | Configurable custom-field definition set — typed, validated, multi-language, attachable at account, event, ticket or metric-cell level | Custom fields, Metadata |
| **Cost Center** | Financial dimension for revenue and cost attribution | Department code |

---

## Recorded exceptions

A word the table above bans may appear only where this list allows it. Each exception names where it applies, and **code, contracts and DDL never take one unless the row says so.**

| Word | Allowed in | Means | Decided |
|---|---|---|---|
| **Booking** | Guest-facing labels only: *Booking Confirmation*, *Group Booking* | An Order (or a Reservation) as a guest reads it. Code and contracts use Order and Reservation | 28 September, audit R145 |
| **Release hold** | Guest-facing and staff-facing labels | Releasing a Reservation. Code says Reservation | 28 September, audit R145 |
| **Session** | Guest-facing copy only, e.g. *Pick a session*, *Surf sessions*, *Sunset swim session* | A Performance as the guest reads it. **Code, contracts and DDL keep Performance** (`Performance`, `performanceId`, `createPerformances`), and staff screens keep Performance as R165 decided | 29 September, rev 3 CFG-10 |
| **Till** | Staff-facing copy | The Workstation. Never the Deposit Box | 28 September, audit R156 |
| **POS**, **drawer** | Staff-facing copy (the POS app, the cash drawer) | The Workstation's app; the Deposit Box. **Out of code, contracts and DDL** | 28 September, audit R156 |
| **QR** | Guest-facing copy only, e.g. GST-055 *Dynamic QR Ticket* | The Media Code as the guest sees it | 28 September, audit R210 |
| **Game Card**, **Gift Card** | Everywhere, code included (`GameCard`, `GiftCard`, `cardCode`) | See the terms above | 28 September, audit R220 |

---

## Adding a term

PR to this page, reviewed by Architecture. A term used in code that is not here is a review finding. Update the forbidden-synonym table in setup/naming-and-style in the same PR.
