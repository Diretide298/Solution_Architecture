# AI scope — for confirmation

**TICVAI · Phase 1**
Prepared by Softlabs Group · 17 August 2026
For confirmation by: Qossai Alqawasmi, Muhamed Allam

---

## Purpose

The requirements matrix carries **288 AI requirements**. This document proposes which are built
in Phase 1, which are deferred, and which are not AI at all and belong to other modules.

It is written for confirmation rather than information. **Section 7 lists five questions** that
change what gets built, and we would like those answered before contracts are finalised.

---

## 1. The principle we propose

**Build anything that needs no trained model. Defer anything that does.**

This was agreed in principle on 14 August. A model that predicts attendance, detects fraud or
sets a price learns from operating history, and TICVAI will have none until the platform has
been live through a season. A model trained on nothing predicts nothing, and a forecasting
feature shipped without data does not fail loudly — **it produces confident numbers that happen
to be wrong**, which is worse than not shipping it.

What remains works on day one because it reads what is already there: the tenant's own
catalogue, configuration, venue plans and documents.

---

## 2. In scope for Phase 1

**80 requirements.**

| | Reqs | What it does |
|---|---|---|
| **Seat map and layout generation** | — | A venue uploads a plan and a schema; the platform proposes the seat map, sections, categories and the ticket configuration that follows |
| **Configuration assistance** | 5 | An admin describes what they want and the platform drafts it — a product, a pass, a price category |
| **Conversational assistant** | 38 | Natural language across modules, multilingual, grounded in the tenant's own data |
| **Knowledge retrieval and semantic search** | — | Across products, memberships, documents and operating procedures |
| **AI governance** | 36 | Prompt and response logging, approval before execution, explainability, audit trail, cost monitoring |

### What "grounded" means here

Every answer is retrieved from data the platform already holds and **returns its sources**. The
assistant does not answer from general knowledge, and where it has nothing to retrieve it says
so rather than inventing something plausible.

### What it may not do

**It drafts. A person applies.** Every configuration the assistant produces is a draft returned
to the screen the admin was already on. They review it, change what they want and save it under
their own permission.

Nothing is created, priced or published by the assistant. Pricing, promotional, financial and
operational proposals additionally require an explicit approval step, recorded with who
approved it and why.

---

## 3. Deferred to a later phase

**194 requirements.** Not cancelled — deferred until there is data to train on.

| | Reqs | Needs |
|---|---|---|
| Demand forecasting | 58 | At least one full season of attendance by venue, attraction and session |
| Fraud detection | 54 | A body of transactions including known-bad ones. Without labelled fraud there is nothing to detect against |
| Dynamic pricing | 46 | Demand and conversion history, plus a commercial willingness to let price move |
| Recommendation engine | 36 | Purchase and attendance history per guest-app |

### What we still build for these in Phase 1

The screens, the contracts, the database tables and the configuration surfaces. **A venue can
configure a pricing rule in Phase 1 and the engine that would drive it automatically arrives
later.** The work is not wasted and the deferral is not visible as a missing feature — it is
visible as a rule that is set manually rather than proposed.

**Our recommendation on timing:** revisit six months after go-live, when there is a season of
data. Fraud detection may justify moving earlier if transaction volume is high, because it is
the one where the cost of waiting is measurable.

---

## 4. Not AI — proposed to move

**59 requirements are filed under AI and are not.** We propose moving them so they are built by
the right team at the right time, rather than deferred with the AI work.

| | Reqs | Belongs in |
|---|---|---|
| No-show revenue recognition, complimentary and invitation tickets | 6 | Ticketing and Finance |
| Future-dated pricing calendars and schedules | 9 | Ticketing Catalogue |
| BI and reporting dashboards | 34 | Already covered by the reporting module |
| Operations command centre | 10 | A live operational dashboard, not a model |

**None of this is a reduction in scope.** It is the same work counted under the module that
will deliver it.

---

## 5. What Qossai confirmed on 17 August

> *AI configuration is mostly for UI maps for seating and the ticket configuration.*

We have taken this as the priority order, and it narrows what we had drafted.

**We would like to confirm whether it also narrows the boundary.** The contract as written
allows the assistant to draft products, memberships, promotions, discount rules, pricing
calendars, seating zones and operating hours. Qossai's confirmation names **seating maps and
ticket configuration**.

Two readings, and they build differently:

**Reading A — seating and ticketing only.** The assistant is a focused tool: upload a plan, get
a seat map, get the ticket types that go with it. Smaller, faster, and the thing a venue does
once per space.

**Reading B — seating and ticketing first, the rest to follow.** The assistant is general and
those two are simply the first capabilities delivered.

**We propose Reading B**, on the grounds that the difference in build cost is small once the
retrieval and approval machinery exists, and the same machinery serves promotions and pricing
later without a second project. **But A is a legitimate choice** and would let us deliver
sooner.

---

## 6. What this means for the venue in practice

**Setting up a new theatre or arena.** Today: someone builds a seat map by hand, section by
section, then creates ticket types and price categories against it. With this: they upload the
architect's plan, the platform proposes the map, and they correct what it got wrong. **The plan
is never applied automatically** — it enters the existing seat-map preview step, which exists
because a seat manifest is always wrong the first time in a way only a person looking at it
will notice.

**Creating a product.** An admin types what they want in plain language. The platform asks the
questions that narrow it — admission or timed entry, which venue, which price list — and
produces a draft with **a list of what it had to guess**. They review the guesses, not just the
result.

**Asking a question.** *"Which annual passes include parking?"* Answered from the tenant's own
catalogue, with links to the products it read.

---

## 7. Questions we need answered

These change what is built. We have proposed an answer to each.

| | Question | Our proposal |
|---|---|---|
| **1** | **Seating and ticketing only, or general assistant starting there?** (Section 5) | General, delivered seating-first |
| **2** | **Which AI providers may process data in each region?** A prompt reaching a provider hosted outside the UAE is a cross-border transfer under PDPL | UAE-hosted inference for anything touching guest-app data; other providers permitted for configuration assistance, which touches none |
| **3** | **How long are prompts and responses retained?** They may contain personal data, and no retention period exists anywhere in the matrix | 90 days for prompts and responses, indefinite for the action audit trail |
| **4** | **Who approves an AI proposal?** Pricing and financial proposals require approval — at what level, and may the person who prompted it also approve it? | Venue manager for operational, finance controller for pricing and financial. **Never the person who prompted it** |
| **5** | **Is the conversational assistant available to guests, or staff only?** The matrix implies both; the guest-app app has an AI tab | **Staff only in Phase 1.** A guest-facing assistant needs a different safety posture and a different cost model |

---

## 8. What exists today

| | |
|---|---|
| Contract | `ai.yaml`, **17 operations**, validated against the platform's 671 |
| Permissions | Four — use, configure, approve, audit |
| Architecture rules | Written and enforced: no provider SDK in capability code, partition-level tenant isolation, read-only against the transactional core, every response carrying trace id, model, token count and sources |
| Screens | The AI tab exists on the venue-staff-app app board and has no defined behaviour |
| **Engineer assigned** | **None.** This is the largest single resourcing gap in the project |

---

## 9. What we need to proceed

| | | From |
|---|---|---|
| 1 | Confirmation of the scope split in sections 2, 3 and 4 | Qossai, Allam |
| 2 | Answers to the five questions in section 7 | Qossai, Allam |
| 3 | Agreement to move the 59 non-AI requirements to their proper modules | Qossai |
| 4 | An AI engineer assigned | Softlabs |

**Item 4 is ours and it is the one that determines the date.** The scope above is
approximately four weeks of work for one engineer who has done retrieval systems before, and
nobody is currently assigned to it.
