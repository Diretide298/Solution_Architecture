# ADR-0023 — Personal data lives apart from the append-only ledger

**Status:** Accepted · 17 August 2026, recording a decision already implemented
**Relates to:** ADR-0013 (local-first POS), CF-35 (biometrics under PDPL), CF-64 (retention)

---

## Why this is written late

**The separation is built and complete.** Four `pii.*` tables, ten operations touching
`ledger.entry`, fifteen touching `pii.*`, and — verified 17 August — **zero operations touching
both.**

It was never written down, so it survived as a discipline nobody had stated. **A boundary that
holds because everyone happens to respect it is a boundary one careless join away from not
existing.**

---

## Context

Two requirements point in opposite directions and both are non-negotiable.

**The ledger must be immutable.** A financial record that can be edited is not a record. Every
posting stands, corrections are reversals rather than rewrites, and an auditor must be able to
read a period and know it has not moved since it closed.

**Personal data must be erasable.** Under PDPL a subject may request erasure, and the answer is
yes or it is not an answer. <cite index="10-1">The UAE Personal Data Protection Law applies to controllers and processors established in the UAE and extraterritorially to entities processing personal data of UAE residents.</cite>

**A guest's name inside an immutable ledger entry makes both impossible at once.** Either the
ledger is mutable, or erasure is a lie.

---

## Decision

**Personal data is never a value in the ledger. It is a reference the ledger holds and the
subject store resolves.**

    ledger.entry            subject_id: uuid    ← a pointer, never a name
    pii.subject             the person
    pii.subject_contact     email, phone, address
    pii.subject_document    passport, ID, visa
    pii.subject_biometric   face, fingerprint — CF-35

**Erasure empties the subject record. The ledger entry is untouched and still balances**, because
what it holds is an identifier, not an identity. The money is still accounted for; the person is
gone.

### The four PII tables are separate from each other for the same reason

A contact point is erased routinely — a guest unsubscribing, a bounced address suppressed. **A
passport number under CF-35 is a different class of data with a different retention period and a
different legal basis**, and biometrics are stricter again. Holding them in one table would give
them one lifetime, and they do not have one.

### What replaces the name in a report

A financial report that needs a guest name **joins at read time, under permission**, and
`REPORT_EXPORT_PII` is a distinct permission from `REPORT_VIEW` for exactly this reason. A report
run after erasure shows the transaction and no name — **which is the correct output, not a
defect**, and a reader who does not know that will file a bug.

---

## What this does not solve

**Erasure has more than two homes.** `pii.*` and the ledger were the hard pair, but a subject
also appears in `ai.interaction` if they typed their own name into a prompt, in
`marketing.message_delivery`, in the Qdrant payload of any indexed case, and in an export sitting
on a signed URL.

**ADR-0020 named the AI half. `removeIndexEntry` exists for the vector half.** The rest is
`createDsarRequest` fanning out, and its state model is explicit that **`partiallyFailed` is not
a synonym for completed** — under PDPL a cell that did not answer means the honest answer is no.

**Retention is still unanswered.** CF-64: two periods stated of eighty-nine requirements. **The
separation makes erasure possible; it does not say when it happens**, and a subject record with
no retention period is one that lives forever by default.

---

## Consequences

**No operation may join `pii.*` to `ledger.*` in one query.** Currently true and now stated. The
lineage makes it checkable — an operation reading from both is the signal, and it is worth
adding to `check-package.py` before someone writes a convenient reporting query.

**A guest name cannot be searched from a financial screen.** Deliberate friction: finding a
person from a transaction is a PII read and should look like one.

**Anonymous transactions are structurally normal.** `subject_id` is nullable throughout, so a
cash sale at a kiosk with no guest is not a special case, and neither is a transaction whose
subject was later erased. **The same shape covers both**, which is why erasure needs no
compensating logic anywhere in finance.
