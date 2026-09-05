# Three unmapped packs — what they draw, and what the package would need

**31 August 2026. 20 boards, 228 frames, and 183 of them draw something the package has no screen
for.**

**Two linked. That is not a mapping failure — it is the honest answer**, and forcing the other 226
onto existing screens would claim a coverage that does not exist.

---

## The shape of it

| Pack | Boards | Frames | Match an existing screen | Draw something new |
|---|---:|---:|---:|---:|
| **Marketing** | 12 | 120 | 24 | **96** |
| **Inventory** | 7 | 68 | 11 | **57** |
| **Guest Mobile** | 8 | 40 | 10 | **30** |
| | **27** | **228** | **45** | **183** |

**Only five of the forty-five matched above 0.80.** The rest are a word in common, not a screen.

---

## 1 · Inventory — a warehouse and procurement suite, not a stockroom

**`inventory` has 50 operations.** They cover a venue stockroom: items, locations, movements,
requisitions, purchase orders, goods receipts, stock counts, transfers, suppliers.

**Boards 2 through 7 draw a different product.**

| The pack draws | Operations today |
|---|---:|
| Warehouse zones, bins, storage rules, put-away | **0** |
| Receiving dock, inbound scheduling, bay clashes | **0** |
| Picking waves, packing, staging, dispatch cut-offs | **0** |
| Warehouse task and workforce management | **0** |
| RFQ, supplier invitation, quote comparison, negotiation, award | **2** |
| Goods receipt note, invoice capture, two- and three-way matching | **2** |
| Match exception and dispute resolution | **0** |
| Demand forecasting and consumption planning | **0** |
| Supplier qualification, performance, risk analytics | **1** |
| Unit-of-measure conversion | **0** |

**Board 1 is the exception.** Item master, categories, UoM, locations, statuses, movement history,
reorder parameters — **that maps onto screens that exist**, and it is the board worth taking now.

**Boards 2–7 are roughly 100 operations and 40 tables of WMS and procurement.** A quarter of work,
and a scope decision rather than a design one.

**Three ways it resolves:**

**Contract it.** The client drew it, so somebody expects it.

**Scope it out.** The venue keeps a stockroom; warehouse management is an ERP integration.
**`inventory` already has adaptor precedent** — the queue contract does exactly this for
third-party queue systems.

**Take Board 1 and defer the rest.** Cheapest, honest, and leaves 57 frames drawn against nothing.

---

## 2 · Marketing — twelve boards, and four are genuinely new domains

**`marketing-crm` has 96 operations**, the largest domain in the package. **Six of the twelve boards
land on it.** Four do not.

**Already contracted, needs screens not operations:**

- **Board 1 CRM** — guest directory, 360 profile, activity timeline, family and guardians
- **Board 2 Data governance** — identity resolution, duplicate merge, consent, DSAR
- **Board 3 Audiences** — dynamic segments, behavioural, predictive
- **Board 5 Journeys** — the Visual Journey Builder. `listJourneys`, `createJourney`,
  `activateJourney` exist
- **Board 7 Omnichannel** — unified inbox, chatbot, agent workspace
- **Board 8 Cases** — twelve case operations exist, and SLA policy does not

**Genuinely new:**

**Board 10 Gamification** — challenges, badges, points liability, milestones, streaks, referrals.
**`createChallenge` exists and nothing else does.** *£96 400 liability · 44% never spent* is a
ledger obligation, not a marketing feature.

**Board 11 Digital experience** — page builder, design system, dynamic product pages, SEO, mobile
app CMS. **`WhiteLabelService` has 50 operations and none is a page builder.**

**Board 12 Waivers** — templates, assignment rules, versioning, guardian signing, pre-arrival
completion, verification at the gate, retention. **`getWaiverStatus` is the only waiver operation in
the package**, and the board draws ten screens of lifecycle behind it.

**Board 9 Voice of customer** — surveys, NPS/CSAT/CES, review moderation. **Partially there.**

**🔴 And Board 2 draws the two things CF-165 says are missing.** *Retention and anonymisation — 8,400
records, runs Sunday.* **There is no retention operation, no anonymisation operation, and no
retention policy table.** The board is the specification for a conflict that has been open since 20
August.

---

## 3 · Guest Mobile — the pack that should reach two platforms

**Forty frames, and the naming is conversational**: *Your Tickets*, *Send a Ticket*, *Best Available
First*. **Four matched a screen by title.**

**But the content maps onto journeys the package has.** `gm-6a` through `gm-6e` is choose a
performance, best available, seat map, ten-minute hold, booked — **that is F43 and F59, already
walked, already contracted.**

**The gap is that P01 Guest Web is 3 of 46 drawn and P02 Guest App is 3 of 63**, while P05 Guest
Kiosk is 17 of 17. **These forty frames almost certainly serve both P01 and P02**, and the pack has
no way to say so.

**Board 8 is genuinely new and worth naming.** *Screen reader on a ticket · type at 200% · one hand
in the sun · nothing announced only aloud · what a tenant cannot switch off.*

**The package has no accessibility operations at all.** `gm-8e` — the platform's own floor, the
things a tenant may not disable — **is a policy surface, not a screen**, and it needs a decision
before it needs a contract.

---

## What we would take now, in order

**1 — Inventory Board 1.** Eight frames onto screens that exist. **No contract change.**

**2 — Marketing Boards 1, 2, 3, 5, 7, 8.** Sixty frames onto the largest contracted domain. **Screen
work, not contract work** — and Board 2 closes the drawing half of CF-165 while proving the
operations behind it are missing.

**3 — Guest Mobile, once a frame can name two screens.** The journeys exist; the link does not.

**4 — Everything else needs a scope decision first.** Inventory 2–7, Marketing 10, 11, 12, Guest
Mobile 8. **Roughly 130 frames, and every one is a product question rather than a drawing.**

---

## The trickle-down, stated once

**A frame does not become a screen. It becomes a screen only after an operation exists to fill it,
and an operation only after a contract says what it does.**

```
board frame  ->  is there a screen?     yes: link it
                 no: is there a contract operation?
                     yes: build the screen, wire it, walk a flow
                     no:  contract first — schema, operation, table, state model
                          then screen, then flow, then diagram
```

**Every step has a checker.** `check-package` refuses an operation missing from the lineage;
`check-screens` refuses a screen naming an operation that does not exist; `check-flows` refuses a
step on a screen that is not there; `check-states` refuses a status enum with no model.

**That is why 183 frames are recorded rather than linked.** Linking them would put a screen in front
of an operation that does not exist, and the checkers would be right to refuse it.
