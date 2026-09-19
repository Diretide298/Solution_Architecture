# The contract run — what it found

> **Owner:** Chinmay · **Written:** 19 September 2026 · **Status:** authoring complete, AI held back
>
> Result of the plan in [contract-run-plan-19-september](contract-run-plan-19-september.md).
> Governed by [source-precedence-19-september](source-precedence-19-september.md) —
> **MoM > boards > specifications, matrix where all three are silent.**

---

## The headline

**Unserved board screens: 1,059 → 99**, and 97 of the 99 are the AI packs, held back on purpose
because those boards are not complete.

| | |
|---|---:|
| operations authored | **~260** |
| new contracts | **5** — `rental`, `wallet`, `payments`, `accreditation`, plus the `resources` rebuild |
| contracts extended | **13** |
| references wired | **1,590** |
| board screens now calling something | **1,767 of 1,866** |

## The plan was wrong about where the work was, and the audit is why

The plan ordered the run by the audit's `board screens unserved` column. That column comes from a
rule that attributes a pack to **the contract its already-wired screens name most often** — and when
almost nothing in a pack is wired, one stray screen decides.

**`orders` showed 178 unserved screens and owned none of them.** They were `Wallet` (99) and
`Payment Orchestration` (79), each attributed to `orders` on the strength of a single reference.
`catalogue`'s 162 were Game & Ride and two AI packs.

> **Rule for the next run:** a pack with fewer than five wired screens has no reliable contract
> attribution. Read the boards before believing the column.

## What the packs actually needed

Nine of nineteen packs needed **almost no authoring at all.** The recurring shape is not a missing
domain — it is **an operation that acts without the rule that governs it.**

| pack | screens | operations authored | what was missing |
|---|---:|---:|---|
| Approvals | 74 | 8 | dual control, signature, tamper-evident record, SLA *policy* |
| Unified BI | 57 | 13 | KPI library, semantic model, pipeline freshness, subscriptions |
| Marketing CRM | 107 | 17 | identity resolution, retention policy, audience activation |
| DAM | 39 | 16 | taxonomy, renditions, rights terms, distribution fallback |
| Upsell / Cross-Sell | 59 | 15 | strategies, relationships, outcomes, experiments |
| Seating b5–13 | 97 | 19 | hold types, seat rules, groups, recommendation scoring |
| Licensing | 98 | 15 | VSI model, billable unit, module graph, go-live validation |
| Event Management | 33 | 16 | event types, spaces, capacity profile, resource plan |
| Resources b3–4 | 20 | 10 | shift templates, minimum cover, coverage gap, labour cost |

Worked examples of the shape:

- **`mergeGuests`** merged and nothing said which records were duplicates, or which value survives.
- **`createSeatBlock`** took seats out of sale and nothing said what a block meant or when it returns.
- **`recommendSeats`** ranked seats with no rules to rank by — though the 21 August minute says
  best-seat ranking *"must be configurable per seat map/event."*
- **`listDataRetentionExpiry`** read retention outcomes and nothing set a policy.
- **`issueGiftCard`** issued and nothing said what a gift card *is*.
- **`registerDevice`** created a row and nothing turned it into a device you could trust.
- **`createRotaAssignment`** placed one person in one slot and nothing described the slot.
- **`getEntitlementUsage`** reported consumption and nothing said what to do about it.

## Five domains genuinely had nothing

| contract | why it could not live where it was |
|---|---|
| `rental` | Price is not known at checkout. *Expected 14:00, actual 15:12, grace 15 minutes* — a context whose total is fixed at order time cannot express it, and `orders` is such a context. |
| `wallet` | A balance is a number. It cannot hold consumption order, credit lots with their own expiry, or ownership distributed across a family. |
| `payments` | A declined card and a broken gateway need opposite responses. Routing, health and failover are platform state, not transaction state. |
| `accreditation` | Applied for rather than bought, vetted rather than paid for, granting places and times that differ per holder. |
| `resources` | Nine operations against 95 screens with **zero unused** — no idle half existed to find. |

## Three MoM decisions the package had never absorbed

All from 26 August, all found by reading the minutes during this run:

1. **`bookResource` is no longer guest-callable.** *"A guest always books a product or package —
   never a resource directly."* This closes the open question on `F25-a-guest-rents-a-cabana`, which
   was open because nothing read the minutes, **not because the venue had not decided.**
2. **Allocation rotates across the pool by default**, so one cabana is not worn out while others sit
   empty.
3. **Skill matching is attribute matching, explicitly not AI** — *"to avoid unnecessary
   complexity."*

## The matcher was blind five ways, and every repair changed the answer

`derive-task-linkage.py` is the tool that decides whether an operation already exists. It reported
**107 of 107 Marketing CRM screens with no candidate in any contract — against a contract holding
167 of them.**

| defect | consequence |
|---|---|
| a whitelist of ten section headings | the pack uses **7,092**; two packs' tasks were skipped entirely |
| prose headings excluded outright | two packs are prose PDFs whose only heading is `Purpose` |
| `maintenance.work_order` → `work`, `order` | the schema name — the domain — was discarded |
| structural nouns (`information`) | rare in operations *and* meaningless: the one combination rarity weighting cannot defend against |
| ratio with no absolute floor | a one-token task scored **1.00** against anything containing it |

Fixed, plus a corroboration guard and a learned module-affinity check. **The authoring verdict
survived every repair**, which is the only reason it can be trusted.

## Tooling that came out of it

| tool | what it is for |
|---|---|
| `tools/scope-pack-to-contracts.py` | scores every unserved screen against every operation in all contracts, board by board — join or author, before anything is written |
| `tools/check-contract-split.py` | the `seating` test: is an unused half a missing join or real drift |
| `tools/splice-contract.py` | adds paths and schemas without silently overwriting either, **and verifies the new operations landed inside `paths`** |

**`splice-contract.py` had the bug it exists to catch.** Its first cut appended paths to "everything
before `schemas:`" — which is *inside* `components:` when `securitySchemes:` comes first. Valid YAML,
every reference resolving, no duplicates, and thirteen operations vanished from `paths`. It reported
**"clean"**. It now checks by presence in the parsed document rather than by the file looking
plausible.

## What is open

- **The AI packs — 97 screens across three books.** Held back on purpose: the boards are
  incomplete, and a gap there is not evidence of a missing contract.
- **Ten unused operations across `white-label`, `retail` and `cross-region`**, flagged `stale` by
  the audit. These are decisions — superseded, renamed or still wanted — not authoring, and nothing
  has been deleted.
- **The seven section-type seat screens** (`BO-955`/`957`–`961`), which the 21 August minute
  collapses into one builder. Six ids retire; all seven carry zero components.
- **Three operations dropped earlier to clear checker errors** (`listSaleChannel` ×2,
  `listNextBestAction`) that do exist in the contracts. Restoring them was offered and not taken.
