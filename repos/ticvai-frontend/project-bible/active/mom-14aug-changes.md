# Changes from the 14 August kick-off

Source: `RE TICVAI Kick-off meeting-20260814_110459` — 1h 33m. Present: Qossai Alqawasmi,
Muhamed Allam, Chinmay Parab, Dinesh Jadhav, Pradnya Yeram, Aishwarya More, Chitrangi Mestry.

**Three conflicts close. One ADR needs amending. Eleven behaviours are newly specified.**

---

## Closed

### CF-52 — Parking. Closed.

Three modes, and the platform builds for all three because a venue will have whichever its
existing barrier vendor supports.

| Mode | What TICVAI does |
|---|---|
| **No integration** | Issues a parking QR; security scans it at the barrier. Nothing to integrate |
| **Plate number → whitelist** | Guest enters a plate at purchase; **we push it to the parking system's whitelist API**. ANPR opens the barrier. *"Mostly we will go for that direction"* |
| **QR → barrier** | Where there is no ANPR. We push the QR to the parking system |

**Out of scope:** hourly parking charged on exit. *"They can use the parking point of sale and
complete the transaction without connecting to the ticketing, because they don't need us."*

**Direction matters and was settled explicitly.** We **consume their API and push to it** — we
do not publish an API for parking vendors to call. That inverts what the platform-ops contract
would otherwise have assumed.

Qossai set the bar: *"I don't want to arrive in a project and we have parking integration and
then you will tell me that we need three weeks."* Chinmay committed to three or four days,
which is only true if the adaptor pattern is in place before the first vendor appears.

### CF-33a — Queue vendor. Confirmed closed.

Wait times come from **sensors or counting cameras at the ride entrance**, or are entered
manually. Two shapes to consume: a live wait-time API, or a people count that we convert using
a per-person service rate. Warner Bros Abu Dhabi named as the reference implementation.

Downstream: AI recommends which attraction to visit next from live waits. That is a Phase 1
use of live data, not a forecast, so it does not depend on operating history.

### CF-37 — FX. **Partially closed.**

**Settled — foreign currency tender.** All transactions store the **base currency of the
region**. A guest paying USD 100 has the dirham equivalent stored at the configured rate.
Change and refunds are **always in base currency** — never in the tendered currency. A separate
foreign-currency report shows what each cashier took in which currency.

Allam's framing removes the question Chinmay asked: *"the value of the currency doesn't matter
whether it goes high or down. They are purchasing a product equivalent to that currency… at
the end they are paying that base currency value, and they get a refund for the base currency
value."* There is no rate to lock at redemption or expiry, because the stored amount was never
in a foreign currency.

**Still open — cross-region revenue split.** A pass sold in one region and redeemed in another
involves two legal entities with two base currencies. Yesterday's question was about tender;
this one is about settlement between entities, and it was not asked. **CF-37 stays open for
that part**, and the recommendation already drafted still needs Finance.

---

## Needs an ADR amendment

### ADR-0014 — Cell = Tenant × Region. **Contradicted.**

Two hosting models were confirmed, and only one of them is what the ADR describes:

**Dedicated tenant.** Own infrastructure, own domain — `ticketing.dubairacingclub.com`. This
is ADR-0014 as written.

**Shared TICVAI infrastructure.** Small tenants share a database, isolated logically.
`ticvai.com/miraclegarden` or a subdomain. Sold as a cheaper package; a tenant wanting
isolation *"can pay extra and have his own database."*

Dinesh confirmed the isolation model: *"logically isolated, the data will still stay in the
same database, managed centrally."* Allam: isolation *"based on that venue site ID."*

**This is a third cell kind, not a variation.** The scope tree and RLS already support several
tenant roots in one database — that part is not new work. What is new is that **ADR-0014's
claim that a cell holds exactly one tenant is now false**, and two things depend on it:
`platform.tenant` was written as a single-row projection with no RLS, on the stated grounds
that a cell holds one tenant. On a shared cell that is wrong and becomes a cross-tenant leak.

Qossai also named the load case: a two-week event with 30,000 attendees a day is a small tenant
by contract value and a large one by volume. Shared-cell sizing cannot be driven by tenant count.

**Action: amend ADR-0014, add RLS to `platform.tenant`, and revisit the migration
orchestrator's fan-out — a shared cell has many tenants on one schema version.**

---

## Newly specified

### AI — configuration assistant moves to Wave 1

Qossai: *"one of the most important item for the AI is basically the configuration
assistance… it's supposed to be from beginning because this is one of the most important
element in our software."*

An administrator types "I want to configure a new product" and the assistant asks which kind —
admission, timed slot — and walks the configuration. **Forecasting is explicitly not required
in Phase 1**, which confirms the phasing paper's cold-start argument.

Two further Phase 1 candidates named, both independent of operating data: **map layout
generation** from an uploaded schema plus a plan image, and **ticket artwork** generation with
fixed fields held constant.

The AI phasing paper needs revising: configuration assistance was not among the fifteen Phase 1
applications, and it is now the most important one.

### Guest web and app — same CMS, per-surface override

One CMS, one publish. Same branding and look and feel across both, *"so that if a customer
purchases a ticket on the website or on the mobile app they should have the same look and feel."*

**But per-surface override is required.** Qossai: *"if he would like to put a different header
for the mobile application than the website, he can do it."* Base structure is fixed — header,
footer, logo, colour, font — and **module enablement is per surface**: a tenant without dining
disables it and it disappears from the app.

The white-label contract has module enablement and feature toggles. It does **not** have a
per-surface override on either. That is a contract change.

Website scope was also clarified: **the tenant keeps their own marketing site.** We host the
booking flow they link to. The mobile app is the full tenant experience — park times, services,
profile, purchase.

### POS branding — TICVAI, not white-label

Staff-facing surfaces carry **TICVAI branding**: POS, tablets. *"If the application is used by
the venue employee, then it's supposed to be TICVAI branding."*

**The kiosk is the exception** — guest-facing, so white-label with the client's logo and
colours, styled like the website rather than like the POS.

*"Powered by TICVAI"* appears everywhere including guest surfaces.

This contradicts nothing already built, but the White Label Builder currently offers branding
per tenant with no notion of which surfaces it may reach. It needs a surface scope.

### Cinema is in scope

*"We have a seat management module dedicated for this."* A museum in Kuwait with an
educational cinema was the example — assigned seats, a film, a time slot. Seating already
covers it; worth recording because it was previously assumed out of scope.

### F&B — nine behaviours specified

1. **Combo on a ticket.** One QR carries admission and a meal. Scan at the gate to enter, scan
   at the restaurant to redeem the burger. Second redemption is refused.
2. **Per-ticket assignment.** Buying three tickets: ticket 1 combo, ticket 2 nothing, ticket 3
   popcorn. The entitlement attaches to the ticket, not the order.
3. **Pickup or deliver-to-seat**, chosen at purchase. Pickup needs no seat; delivery does.
4. **Seated events deliver to the seat number**, which the platform already knows from the booking.
5. **Group bookings are configurable**: one QR for twenty, or twenty QRs. For seated events
   *"it's better to have 15 QR codes because I may come ten minutes before, one person can come later."*
6. **Individual QRs can be claimed to a profile**, which is what makes per-person delivery possible.
7. **Cashier can assign a specific meal to a specific ticket** — practical for small groups,
   and explicitly impractical for large ones, where the venue issues one QR and the group
   redeems at the counter.
8. **QR at a lounger or beach seat** — scan, order, delivered to that location. Already built
   today as `claimLocationSession`; the MoM confirms the design.
9. **Ordering F&B from outside the venue with no ticket is out of scope.** *"It comes under the
   category of a food ordering application."* Ordering **inside** without a prior F&B purchase
   is in scope.

### One cart, one receipt, one QR

A single cart spans tickets, F&B and retail. **One receipt** on site — *"we don't need multiple
receipts."* One unified guest id, one QR that admits, opens a locker and redeems a meal.

**Entitlements can be appended to an existing ticket.** Buying a locker after arrival: scan the
existing QR, the locker attaches to it, no second QR. This is a real gap — the contract issues
entitlements at order creation and has no append path.

Cross-venue redemption on one QR was confirmed for tenants running several venues.

### Inventory — outlet-level enforcement

Stock is centralised per venue, and **an outlet with no stock cannot sell even when the
warehouse has it**. Allam: *"physically the stock is there, but on the system there is no stock.
It should not allow to buy."* Inter-venue transfer exists as an operational remedy, not an
automatic fallback.

The retail contract has outlet stock; it does not currently refuse a sale on outlet stock alone.

### Cash — float entry by amount or by denomination

Denominations are configurable per region, *"in UAE we have 500, 200, 100, 50, 20… in Bahrain
you will not have 1000."*

**Float entry must support both a total and a denomination breakdown**, configurable per venue.
The POS screens written today assume denomination entry only.

**Decimals confirmed at two or three by region.** *"An item price can be 2.013 and we should
save exactly 2.013, not 2.015."* This is ADR-0008 restated by the client, which is a useful
confirmation rather than a change.

### Workstations — type, layout, and a park map

**Workstation type** is a configuration attribute: POS, kiosk, mobile POS. Layout follows type
— *"a ticketing workstation will have a different layout, a food and beverage workstation a
different layout"* — and **which products a workstation may sell is configured per workstation**.
One workstation sells general admission, another only memberships.

The sale board already carries layout per workstation. **What is missing is the workstation
type as a first-class attribute**, and the product-scope rule.

Also specified: workstations grouped by department and sub-department, a health monitor by
department, and a **park map with drag-and-drop workstation placement** over an uploaded plan.
Chinmay offered AI placement from a map schema, with manual drag-and-drop as the fallback.

---

## Actions

| | | Owner |
|---|---|---|
| 1 | **Amend ADR-0014** — shared-tenant cell, and add RLS to `platform.tenant` | Chinmay |
| 2 | Revise the AI phasing paper — configuration assistance to Wave 1 | Chinmay |
| 3 | Per-surface override on white-label module enablement and branding | Contracts |
| 4 | Append-entitlement-to-existing-ticket operation | Contracts |
| 5 | Workstation type as a configured attribute, plus product scope | Contracts |
| 6 | Float entry by amount as well as denomination | Contracts + POS screens |
| 7 | Outlet stock refusal on sale | Contracts |
| 8 | Parking adaptor — outbound push to a vendor whitelist | Contracts |
| 9 | Update the matrix with the AI column discussed | Chinmay |
| 10 | Tracker meeting, 15 minutes, early next week | Allam + Chinmay |
| 11 | Next workshop: F&B, retail, procurement and inventory together | Qossai |

**The delivered wireframes are reference, not specification.** Allam: *"what we are giving is
just for your reference, you don't need to replicate the same… check the matrix and see if
there are components which we need to show."* Qossai added that the designs came from ChatGPT
and *"there is some error in this one."*

That inverts how the POS mockups were read this morning. They remain a useful source for
**what a screen must do** — four missing operations came out of them — but not for what it
should look like.
