# Twelve technical documents nobody reads

> **Owner:** Chinmay · **Written:** 19 September 2026 · **Status:** open
>
> Raised by Chinmay while settling the wallet question: *"the attached files that come with
> [MoMs] with detailed documentation — are we reading those?"*
>
> **No.**

---

## What is there

`sources/documents/` holds twelve `.docx` chapters of a technical proposal for the TAIS platform,
plus the RFP they answer.

```
Ch01_Executive_Overview_v1_4          Ch06_Integrations_and_Infrastructure_v1_4
Ch02_Technical_Architecture_v1_4      Ch07_Security_Offline_Mobile_v1_4
Ch03_Functional_Domain_Coverage_v1_4  Ch08_Implementation_and_Delivery_v1_4
Ch04_Finance_and_Commerce_v1_4        Ch09_Platform_Vision_v1_4
Ch05_AI_and_Intelligence_v1_4         Dev01_Engineering_Handbook_v1_0
                                      Dev02_Repository_Structure_and_Contract_Pipeline_v1_0
                                      Dev03_Local_Development_Environment_v1_0
```

**Ch04 alone is 185 paragraphs**, and it is specification rather than prose:

> *"Every financial event in the platform — a ticket sale, a refund, a wallet top-up, a fee charge,
> a discount applied, a settlement received, a chargeback lost — produces a corresponding
> double-entry ledger record… There is no separate 'accounting table'."*

with worked journal entries — `DR Accounts Receivable (Stripe) AED 150.00 / CR Ticket Revenue —
General Admission AED 142.86` — a hard technology commitment (*"the Finance Service uses .NET (C#)
with PostgreSQL exclusively… the only domain in the TAIS stack with a hard language constraint"*),
and a section **4.9 Gift Cards and Stored Value Wallets**.

## Nothing reads them

| check | result |
|---|---|
| Cited anywhere in `contracts/`, `docs/`, `screens/` | **0** |
| Tools reading `sources/documents/` | **none** |
| Covered by the ingestion runbook | **no** |

`sources/README.md` ranks `mom/` and `requirements/` and says nothing about `documents/`, so these
have no authority rank either. They are filed and invisible.

## Why it matters, on today's evidence

The wallet question was settled from three sources — the 27 August MoM, matrix 4.3.28–4.3.35, and
the wallet pack. **Ch04 §4.9 is a fourth, and it was not consulted**, because nothing in the
package knows it exists.

Ch04 also carries a claim that would change ADR-level decisions if it holds: **Finance is committed
to .NET and PostgreSQL exclusively, described as the only domain with a hard language constraint.**
That belongs in the architecture record, not in an unread chapter.

## What is owed

- [ ] **Decide their rank.** Are these ours (a proposal we wrote) or the client's (a specification
      we must meet)? The wording — *"TAIS provides all of this"* — reads as a proposal **we** wrote,
      which makes them rank 3 at most. **Confirm before citing them as scope.**
- [ ] **Read Ch04 §4.9 against the wallet cluster**, and Ch03 *Gift Cards & Stored Value Wallet*
- [ ] **Extract the technology commitments from Ch02 and Ch04** and check them against the ADRs
- [ ] **Add `documents/` to `sources/README.md`'s rank table**, so the next reader knows what they
      are holding
- [ ] **Add a step 0 note to the ingestion runbook** — a client drop carries specifications
      alongside the boards, and only the boards are parsed today
