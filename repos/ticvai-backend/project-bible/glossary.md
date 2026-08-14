# Glossary

> **Purpose:** Canonical domain vocabulary  
> **Owner:** Chinmay + Allam  
> **Status:** **Draft — needs client sign-off**


**One concept, one name, everywhere.** Only casing changes between layers. The word never does.

Sources: client-supplied reference definitions · MoM decisions 30 Jul – 12 Aug 2026 · the requirement matrix.

---

## Catalogue & product

| Term | Definition | Never say |
|---|---|---|
| **Event** | A named happening that has one or more Performances. Carries the identity a guest recognises | Show, Occasion |
| **Performance** | A dated, timed instance of an Event. The thing capacity attaches to | Showtime, Session, Slot |
| **Product** | A sellable thing. May be a ticket, membership, F&B item, retail item, rental or bundle | Item, SKU, Article |
| **Component** | A constituent part of a Product's definition | Element, Part |
| **Attribute** | An axis that generates Product variants. Adding an attribute value auto-creates sellable variants | Option, Variant, Modifier |
| **Metric Sheet** | The grid defining product-to-price relationships across axes | Matrix, Grid, Price table |
| **Price List** | A named set of prices, scoped by channel, season or calendar | Tariff, Rate card |
| **Envelope** | A capacity allocation container. Combines with Space Structure and Seat Category to form capacity | Pool, Bucket, Quota |
| **Capacity Allocation** | Space Structure + Seat Category + Envelope | Inventory, Availability |

## Sale & entitlement

| Term | Definition | Never say |
|---|---|---|
| **Order** | A completed commercial transaction. Posts to the ledger. Creates entitlement | Booking, Sale, Basket |
| **Reservation** | A held, not-yet-paid commitment. Expires. **Not an Order** | Booking, Hold |
| **Ticket** | The issued instrument granting entitlement. Has a stable Ticket ID | Pass, Admission, Voucher |
| **Entitlement** | The right a holder has. **Separate from identity** — settled 05 Aug 2026 | Permission, Right, Access |
| **Media** | The physical or digital carrier of a Ticket — card, wristband, phone, print | Card, Pass, Carrier |
| **Media Code** | The identifier written on the Media. **≠ Ticket ID** — settled 07 Aug 2026. Media can be re-linked; the Ticket ID does not change | Barcode, QR, Serial |
| **Money Card** | A Ticket used as a stored-value instrument | Gift card, Wallet card |

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

## Organisation & operations

| Term | Definition | Never say |
|---|---|---|
| **Tenant** | Top-level entity owning all Brands. One per commercial client | Client, Customer, Org |
| **Brand / Organisation** | Groups similar business types within a Tenant. May span jurisdictions | Division |
| **Region / Branch** | Geographic grouping. **Owns currency, decimals, date format, time zone, fiscal year** — inherited by all Venues beneath | Area, Territory |
| **Venue** | Isolated configuration and operations unit. Admin access scopes here | Site, Park, Property |
| **Department / Sub-Department** | Functional areas within a Venue — Ticketing, F&B, Retail, B2C, B2B, OTA | Section |
| **Workstation** | A configured device instance. Determines Sale Board, hardware, till identity, Access Point, reporting dimension. **Never authorisation** | Terminal, Till, Station |
| **Operating Area** | A grouping of Workstations by function | Zone, Section |
| **Sale Board** | The configured front-end a Workstation loads — ticketing, F&B or retail | Screen, Layout, Menu |
| **Scope Node** | A node in the seven-level hierarchy, addressed by ltree path | Level, Org unit |
| **Cell** | One Tenant in one jurisdiction. The deployment unit | Instance, Stamp, Region |
| **Deposit Box** | The cash container assigned to a shift | Drawer, Float |
| **Cash Lift** | Mid-shift removal of cash from an open float, traced | Pickup, Drop |
| **Blind Close-Out** | Shift close where the operator counts without seeing the expected figure | — |

## Identity & configuration

| Term | Definition | Never say |
|---|---|---|
| **Principal** | An authenticated actor holding permissions | User, Account, Login |
| **Subject** | A person referenced from the ledger by opaque ID. PII lives separately and is erasable | Customer, Guest, Person |
| **Role** | A named grouping of Principals for permission management. **Fully configurable; nothing predefined** — 12 Aug 2026 | Group, Profile |
| **Data Mask** | Configurable custom-field definition set — typed, validated, multi-language, attachable at account, event, ticket or metric-cell level | Custom fields, Metadata |
| **Cost Center** | Financial dimension for revenue and cost attribution | Department code |

---

## Adding a term

PR to this page, reviewed by Architecture. A term used in code that is not here is a review finding. Update the forbidden-synonym table in [setup/naming-and-style](setup/naming-and-style.md) in the same PR.
