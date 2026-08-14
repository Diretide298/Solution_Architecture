# Configuration scope — decision sheet

**321 configuration requirements. 263 do not say at what level.**

Four categories are already settled and are not open to preference — currency and money to
region, ledger and settlement to region, brand and guest app to tenant, identity and consent
and licensing to tenant. Those are law, store rules and contract.

The twenty below are the rest. **Recommended by Softlabs, accepted by the client on 14 August.** Two were corrected in that conversation — see the provenance note at the foot.

The default rule underneath all of it: **configuration resolves up the scope tree, nearest
ancestor wins.** A tenant sets a default, a region overrides for its jurisdiction, a venue
overrides for itself. That is the same mechanism RLS already uses, so it costs nothing new.

| | Category | Reqs | **Decided** | Why |
|---|---|---|---|---|
| 1 | **Ticket & entitlement rules** | 104 | `venue` | Validity, re-entry, expiry and transfer rules differ by attraction. A water park re-entry rule is not a museum re-entry rule, and both sit under one tenant |
| 2 | **Pricing & discounts** | 66 | `venue` | A price list is per venue and per channel. **Tax rate is the exception and is regional** — a venue cannot choose its VAT |
| 3 | **Cash & shift** | 52 | `venue` | Float amounts, variance tolerance and count method are operational. **Denominations and decimal places are regional** (ADR-0008) |
| 4 | **Loyalty & membership** | 51 | `tenant` | A membership sold at one venue is honoured at all of them (CF-31). Earning and tier rules must be one scheme or the guest has several |
| 5 | **Capacity & availability** | 50 | `venue` | Capacity is physical. Nothing above venue level knows how many people fit |
| 6 | **Approval thresholds** | 48 | `venue` | Already settled twice — CF-36 refunds, CF-38 price variance. A flagship venue and a kiosk have different tolerances |
| 7 | **Promotions & bundles** | 44 | `region` | Commercial campaigns usually run across venues, and a promotion configured per venue is one somebody has to configure per venue. **Override at venue** where a single site runs its own offer |
| 8 | **Notifications & messaging** | 35 | `tenant` | Templates and sender identity are brand. **Which events trigger a send is venue** — a venue with no F&B does not send order-ready messages |
| 9 | **Workstation & devices** | 24 | `venue` | **Client correction 14 Aug.** The venue defines profiles — type, layout, sellable products, attached devices — and a workstation is assigned one. Forty workstations configured individually is forty things that drift |
| 10 | **Seating** | 21 | `venue` | A seat map belongs to a physical space. **Templates are regional** so a chain reuses a layout |
| 11 | **Refund & cancellation** | 21 | `venue` | Policy differs by product and site. **The approval threshold on top of it is also venue** — same as CF-36 |
| 12 | **Guest profile & CRM** | 21 | `tenant` | **Consent is a controller-level legal act**, and the controller is the tenant. Segments and preferences follow the profile, which is one per guest per tenant |
| 13 | **B2B & partner** | 15 | `tenant` | A contract, a credit limit and a net rate are agreed with the tenant. **Allocation per venue** — a partner gets so many for this site |
| 14 | **Access & gates** | 14 | `venue` | Access points are physical. Anti-passback windows and geofences are per gate |
| 15 | **Security & session** | 14 | `tenant` | Password policy, MFA requirement, session timeout and lockout are one security posture. A venue relaxing MFA is a hole in the tenant |
| 16 | **Reporting & dashboards** | 13 | `tenant` | Definitions are shared so figures are comparable. **Scheduling and recipients are venue** — a duty manager wants their own site at 6am |
| 17 | **F&B & kitchen** | 9 | `venue` | **Client correction 14 Aug.** Menus, stations and course timing are defined at venue and an outlet is assigned them |
| 18 | **Inventory & stock** | 7 | `venue` | Par levels and reorder points are per location. **Suppliers and purchase approval are tenant** — one commercial relationship |
| 19 | **Localisation** | 5 | `tenant` | Languages offered are brand. **Date and number format is regional** and follows currency |
| 20 | **Queue** | 4 | `venue` | Wait-time source, service rate and redemption window are per attraction |

## Provenance

All twenty accepted 14 August. Two corrected in that conversation — rows 9 and 17 above, both
moved to venue. Those corrections produced the rule underneath everything: **venue is the
floor, and below it you are assigned a profile rather than configuring one.**

The 60 previously uncategorised requirements are assigned at the foot of this document.
**All 321 configuration requirements now have a level.**

## The ones put to the client with the case against

**Promotions at region (44).** The argument for venue is that a site running its own offer
should not need a region-level change. The argument for region is that most campaigns are
commercial and cross-venue, and per-venue configuration means configuring it per venue. With
inheritance both work — the question is which is the default and which is the override.

**Loyalty at tenant (51).** Firm, and worth stating plainly: a membership sold at one venue
and honoured at another (CF-31) cannot have per-venue earning rules without the guest holding
several balances. If venues genuinely need their own schemes, they are separate programmes
rather than one programme configured differently.

**Security at tenant (14).** Also firm. A venue that can lower its own MFA requirement is a
hole in the tenant's security posture, and the first audit will say so.

**F&B at outlet (9).** Put forward as outlet and **corrected to venue.** It would have added a
fifth level to the resolution chain for nine requirements, and an outlet inventing its own menu
structure independently of the park is not how a venue is run.

## What happens once you decide

Each answer becomes a `x-ticvai-config-scope` on the operations that set it, checked in CI the
same way permissions are. A configuration operation declaring a level it is not entitled to
then fails the build rather than shipping.

**60 requirements did not match any category.** They are in the audit output and worth a read
before this is locked — a category nobody named is usually a category nobody owns.

---

## The 60 uncategorised — assigned

The keyword pass missed these because none of them uses the word my patterns looked for.
Assigned below. **Nothing here contradicts the settled four**, and two of them argue for the
inheritance rule explicitly.

| Group | Reqs | Level | Reasoning |
|---|---|---|---|
| **White-label branding** | 11 | `tenant` | Logo, icons, palette, fonts, header, footer, nav labels, FAQs, policies, T&Cs, self-service portal. **Already settled** — the keyword pass simply missed them because none says "brand" |
| **AI configuration** | 6 | `tenant → venue` | **8.4.4 says tenant-specific and 8.4.5 says venue-specific, in adjacent rows.** The matrix is asking for inheritance in so many words. Tenant sets the default, venue overrides |
| **Revenue recognition** | 5 | `region` | Recognition schedules and frequencies are accounting policy, and the books are regional. Already settled under ledger |
| **Seat map builder** | 5 | `venue` | Standing zones, suites, stage, entrances. Physical. 21.13.2 says "venue-specific configuration" outright |
| **Product attributes & taxonomy** | 6 | `tenant` | **Attribute and category definitions are tenant; values are per product.** A taxonomy that differs by venue makes the catalogue incomparable and every cross-venue report a reconciliation |
| **Booking and purchase minimums** | 7 | `venue` | Minimum booking minutes, repeat-customer minimums, rental deposits, donation amounts, publication scheduling, cross-attraction queue rules, **and 1.3.30 — physical, virtual and hybrid events with configurable attendance rules and access methods.** All operational |
| **Access policy engine** | 2 | `venue` | A visual policy builder configuring access rules without code. Access points are physical, so the policies are |
| **Device configuration versioning** | 2 | `venue` | Versioning and rollback of device configuration. Sits inside the venue workstation profile, per your correction |
| **Case, journey and rating frameworks** | 3 | `tenant` | Case categories and severities, journey wait rules, rating scales. CRM is tenant so figures are comparable |
| **Accreditation programme** | 3 | `tenant` | Application forms, categories, access schedules. **Workshop-blocked (CF-21)** — recorded, not decided |
| **Subscription and licensing** | 3 | `tenant` | Plans, grace periods, onboarding auto-configuration. Already settled |
| **Event delivery and retention** | 2 | `tenant → venue` | **13.3.22 names the levels itself** — routing by event type, tenant, venue and business unit. Retention policy is tenant; routing filters resolve down. Developer & API is workshop-blocked |
| **Payment methods per channel** | 1 | `venue` | Which methods a channel accepts. A kiosk taking cash and a web page not is a venue decision |
| **Guest data validation** | 1 | `tenant` | Rules on the guest data collected. One profile schema per tenant, or the same guest validates differently by venue |
| **F&B modifiers** | 1 | `venue` | Per your correction — F&B configuration is venue, and an outlet is assigned it |
| **Reader types** | 1 | `venue` | At least three reader types with configurable properties. Device configuration, so venue |
| **Safety checklists** | 1 | `tenant → venue` | **Templates tenant, instances venue.** A safety standard that varies by site is not a standard; the hazards it checks for do vary |
| | **60** | | |

## The two that argue for ADR-0018

**8.4.4 and 8.4.5 are adjacent rows.** One says the system shall support tenant-specific AI
configuration; the next says venue-specific. Not a contradiction — the matrix is asking for
inheritance, and had we answered them one at a time we would have built two mechanisms.

**13.3.22** names four levels in one line: routing by event type, tenant, venue and business
unit. Same shape. A single configuration value resolved up a tree handles both; a level per
requirement handles neither.

## Three worth a second look before this is final

**Product attributes and taxonomy at tenant (6).** The alternative is venue, and it is
tempting — a water park and a museum categorise differently. But a taxonomy that differs by
venue makes every cross-venue report a reconciliation, and consolidated reporting is in the
brief. Recommend tenant with venue-specific *values*, not venue-specific *attributes*.

**Safety checklists at tenant with venue override (1).** Only one requirement, and it is the
kind that matters after an incident. A safety standard that varies by site is not a standard;
the hazards it checks for genuinely do vary. Templates tenant, instances venue.

**1.3.30 is worth flagging separately.** Virtual and hybrid events appear once in 3,184
requirements and nowhere else in the platform — no streaming, no virtual access method, no
online attendance. Either it is a stray line or it is a product capability nobody has costed.
Raised as CF-67 rather than silently assigned.

**Accreditation (3) and event delivery (2) are workshop-blocked.** Recorded so they are not
lost, and not decided — Developer & API and Accreditation are two of the three domains in
CF-21.

## Everything else takes the recommendation

The eighteen categories above this section stand as recommended. Promotions at region and
loyalty at tenant remain the two most arguable, and both are cheap to move until something is
built against them.
