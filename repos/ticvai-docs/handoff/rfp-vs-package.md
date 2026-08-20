# The RFP against the package

**18 August 2026.** `sources/client/TAIS_Platform_RFP.pdf` — 13 pages, 11 domains, 50 bulleted
capabilities. **The document we were asked to bid on, and nothing in this package had read it.**

Every scope argument until now traced to the requirement matrix and the minutes. Neither is the
RFP.

---

## The good news first

**The domain structure matches what was built.** Eleven RFP domains against 25 contracts, and the
mapping is close to one-to-one without anyone having tried to make it so:

| RFP domain | Contracts |
|---|---|
| Identity & Security | `identity`, `approvals` |
| Governance & Multi-Tenant | `tenancy`, `subscription`, `platform-ops` |
| Finance | `finance`, `orders` |
| Ticketing & Entitlement | `catalogue`, `access`, `seating` |
| Events & Experience | `catalogue`, `queue` |
| Sales & Commerce | `orders`, `promotions`, `retail` |
| POS & Frontline Operations | `orders`, `shift`, `fnb` |
| Marketing & Customer Engagement | `marketing-crm` |
| Intelligence & AI | `ai`, `reporting` |
| Operations & Logistics | `inventory`, `maintenance`, `workforce`, `assets` |
| Ecosystem & Platform Infrastructure | `platform-ops`, `sync`, `white-label` |

**41 of 50 capabilities are contracted.** That is the number to lead with.

---

## 🔴 The non-functional requirements exist, and I have been recording them as absent

The RFP states them plainly:

> **Availability — minimum platform uptime of 99.9%.**
> **Performance — ticket validation and POS transactions must process with minimal latency.**
> **Scalability — high transaction volumes and concurrent users during peak events.**

**`performance/SLA (no targets)` has been one of three blocked artefact classes since the audit**,
and `frontend-delivery.md` says *"no screen has a performance budget… a known blocked artefact
class rather than an oversight."*

**It was not blocked. The target was in the RFP.** 99.9% is 8.8 hours a year, which is a
different architecture conversation from the one this package has been having — and it bears
directly on the answer I gave about one database holding all 24 schemas.

---

## Nine capabilities with nothing behind them

| | |
|---|---|
| **Chargeback Management** | Under Finance. **A chargeback is not a refund** — it is a disputed transaction with a bank-imposed timetable, evidence submission and a fee. `createRefund` does not cover it |
| **Ticket Resale Marketplace** | Under Sales & Commerce. Guest-to-guest resale, not `transferOrderTickets` — a marketplace has listings, pricing and a settlement leg |
| **Dynamic Pricing Engine** · **Pricing Optimization** · **Demand Forecasting** · **Recommendation Engine** | Four of the thirteen Intelligence & AI capabilities. **These are the 194 parked AI requirements**, and the RFP asks for them by name |
| **System Telemetry** | Under Intelligence & AI. `observability.md` covers logging and tracing; telemetry as a product capability is not contracted |
| **Hotel Integration** | Under Operations & Logistics. No contract, no conflict, no mention anywhere |
| **Locker & Rental Management** | Under Operations & Logistics. Distinct from shop-and-drop, which is collection of a purchase |
| **Operations Command Center** | Under Operations & Logistics. A live venue-wide operational view. `BO-005 Queue Monitor` is the nearest thing and it is one module |
| **Developer Portal** · **Sandbox Environment** | Under Ecosystem. **These are CF-21's 94 Developer & API requirements**, workshop-blocked since 6 August |
| **SEO Management** · **URL Management** | Under Marketing and Ecosystem. `white-label` has content pages and no SEO surface |

**Four of these are already tracked** — the AI four are the parked 194, and the developer pair is
CF-21. **Five are not tracked anywhere**: chargebacks, resale, hotel, lockers and the command
centre.

---

## What this changes

**Chargeback is the one to act on.** It sits under Finance, it has a bank-imposed timetable, and
a platform that cannot evidence a chargeback loses it by default. Raised as **CF-123**.

**The non-functional requirements should stop being described as blocked.** The class was closed
by the client before the first workshop, and three sweeps recorded it as open because the
document was never read.

**And the RFP asks vendors to state whether each capability is out-of-the-box, configurable, or
custom.** Nothing in this package answers that question in that shape, and it is the shape the
client will evaluate against.
