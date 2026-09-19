# The wallet cluster was built from the gaming pack

> **Owner:** Chinmay · **Written:** 19 September 2026 · **Status:** open — a decision, not a finding
>
> Found by the step-2 triage on the 814 newly parsed pack screens. It is not a duplication problem
> in the direction the triage reads it.

---

## What is there now

**All nineteen wallet screens on P08 came from `Game_and_Ride_Module.pdf`.** Not one came from a
wallet pack, because the wallet pack had never been parsed until 18 September.

The gaming book carries a board titled ***Wallet & Credit*** — board 3, ten screens — and those
became `BO-414` to `BO-423`. Six more came from its boards 6, 7, 8 and 10.

**Nine of the nineteen have zero components and zero operations.** `BO-417 Top-Up Configuration` is
one sentence — *"Configure the rules governing customer wallet recharges."* — and nothing else.

```
BO-399  Wallet & Credit Acceptance Mapping          0 cmp   0 api
BO-417  Top-Up Configuration                        0       0
BO-418  Top-Up Bonus Rule Configuration             0       0
BO-420  Bonus Validity & Expiry Configuration       0       0
BO-423  Wallet Credit Transaction Ledger & Audit    0       0
BO-448  Redemption Wallet & Balance View            0       0
BO-469  Wallet & Deduction Transaction Monitor      0       0
BO-488  Self-Service Wallet Top-Up                  0       0
```

## What is arriving

`Wallet_Configuration_Backend_Structure_v1.0.pdf` — **100 screens across 10 boards**, from a
workshop dedicated to the domain on 27 August.

**Board 2 is the MoM's §4.5 one screen for one**, and the matrix agrees:

| MoM §4.5, 27 Aug | pack board 2 | matrix |
|---|---|---|
| top-up dashboard | `01 Funding Command Center` | 4.3.33 |
| *"sets minimum and maximum top-up amounts"* | `03 Top-Up Rule Configuration` | 4.3.30 |
| channel & funding-source mapping | `04 Channel & Funding Source Mapping` | — |
| auto-reload on threshold | `05 Auto-Reload Configuration` | **4.3.28** |
| *"distinct from auto-reload"*, calendar-based | `06 Recurring Funding Schedule` | **4.3.29** |
| approval above a threshold | `07 Funding Authorization & Approval Rules` | — |
| full or partial reversal | `08 Funding Reversal & Correction` | — |
| daily/monthly velocity controls | `09 Funding Limits & Velocity Controls` | **4.3.30** |
| funding transaction audit trail | `10 Funding Transaction Audit` | **4.3.35** |

**Three ranks agree**: the MoM (rank 1), the matrix (rank 2, a `Wallet` sub-domain of 33
requirements) and the pack. `BO-417` covers none of it specifically and cites none of it.

## The pack settles it: two vocabularies, and gaming is a value in one of them

**`Wallet Type Library` (board 1, page 4)** — *who owns a wallet*:

```
Guest Wallet · Registered Customer Wallet · Family Wallet · Parent Wallet
Child Wallet · Corporate Wallet · School Wallet · Employee Wallet
```

**`Credit & Balance Type Configuration` (board 1, page 8)** — *what value sits inside one*:

```
Cash Credit · Refund Credit · Bonus Credit · Promotional Credit · Gift Card Credit
Membership Credit · Loyalty Credit · Ride Credit · Attraction Credit
```

**Game credit is a credit type, not a wallet system.** The 27 August MoM records Chinmay saying
*"six wallet types had already been scoped on the Softlabs side (including attraction credit, game
credit, rental credit, parking credit, and other credit types)"* and asking Allam to send the
wallet-configuration documentation so they could be cross-checked. **That documentation is this
pack** — it arrived, and it resolves the six into the second list above. The MoM's open action,
*"cross-check … pending from Chinmay"*, can close.

**The acceptance condition decides the rest:** *"New wallet credit types can be introduced through
configuration without development changes."* A per-module wallet configuration screen contradicts
it — the whole point is one library that gaming, rentals, parking and attractions all draw on.

**Nothing should be collapsed into the gaming screens**, which is what the similarity score
implies. The question is the reverse, and it splits the nineteen in two.

**Genuinely gaming, and they stay** — a wallet is incidental to what the screen is for:

```
BO-404  Reader Management Dashboard              BO-413  Balance Check Reader & Device Test
BO-448  Redemption Wallet & Balance View         BO-461  Card Replacement & Wallet Relinking
BO-486  Customer Card / Wallet Identification    BO-491  Redemption Balance & Prize Discovery
BO-492  Customer Game & Wallet Transaction History
```

**Generic wallet, and the new pack covers them properly** — this is the set to decide:

```
BO-414  Wallet & Credit Management Dashboard     BO-415  Wallet & Credit Type Configuration
BO-416  Wallet Account & Balance View            BO-417  Top-Up Configuration
BO-418  Top-Up Bonus Rule Configuration          BO-420  Bonus Validity & Expiry Configuration
BO-423  Wallet Credit Transaction Ledger & Audit BO-469  Wallet & Deduction Transaction Monitor
BO-487  Customer Wallet & Balance Summary        BO-488  Self-Service Wallet Top-Up
```

Three ways to take it:

**Supersede.** The wallet pack's screens are authored and the ten gaming ones point at them with
`source.sameAs`, the mechanism already used for Rental boards 6–8 across P06 and P08. Keeps both
navigations working and does not renumber anything.

**Keep both.** A gaming wallet and a platform wallet are different contexts, and a gaming operator
should not have to learn the full wallet module. Cheapest, and it leaves ten screens that the next
triage will flag again.

**Retire the eight empties.** `BO-417`, `BO-418`, `BO-420`, `BO-423`, `BO-448`, `BO-469`, `BO-488`,
`BO-399` have nothing in them. An id is never reissued, so retiring costs only the rows.

**The pack's acceptance condition chooses for us, and it splits the ten differently than substance
would.** The line is not *how much is in the screen* but *is this configuring the wallet system, or
operating one credit type*:

| gaming screen | verdict |
|---|---|
| `BO-415` Wallet & Credit Type Configuration | **superseded** — this *is* the type library, and there must be one |
| `BO-417` Top-Up Configuration | **superseded** — funding rules are the library's, board 2 |
| `BO-418` Top-Up Bonus Rule Configuration | **superseded** — Bonus Credit is a credit type |
| `BO-420` Bonus Validity & Expiry Configuration | **superseded** — expiry is a per-credit-type field |
| `BO-399` Wallet & Credit Acceptance Mapping | **superseded** by `BO-1106` Credit Usage & Eligibility Rules — *acceptance* is where credit may be **spent**, not where it is loaded from, so board 3 rather than board 2 |
| `BO-414` Wallet & Credit Management Dashboard | **keep** — operating the game credit, 12 components, hub of 19 edges |
| `BO-416` Wallet Account & Balance View | **keep** — a view of an account, not configuration |
| `BO-423` Wallet Credit Transaction Ledger & Audit | **keep** — gaming's own ledger view |
| `BO-469` Wallet & Deduction Transaction Monitor | **keep** — gameplay deduction is gaming |
| `BO-487` / `BO-488` | **keep** — customer-facing at a gaming counter |

**Five superseded, five kept**, and every one of the five superseded has **zero components** — so
nothing rendered is lost. The five kept include the hub, so no navigation is re-pointed.

That the substance and the principle agree is worth noting: **the screens that configure the system
were never built, and the screens that operate it were.**

## Why this was nearly missed

The triage scored `Top-Up Rule Configuration` against `BO-417` at **0.26** and put it in the
middle band with 37 others. Read as a duplicate list, the obvious action is to collapse the new
screen into the built one — **which would have deleted the only screen in the package traceable to
matrix 4.3.30 in favour of an empty stub.**

A similarity score says two screens are alike. **It does not say which should survive**, and that
is not a thing the score can know. Recorded in
[`docs/ingestion-runbook.md`](../ingestion-runbook.md) under step 2.
