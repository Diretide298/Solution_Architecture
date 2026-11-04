# ADR-0023 — Personal data lives apart from the append-only ledger

**Status:** Accepted · 17 August 2026, recording a decision already implemented
**Relates to:** ADR-0013 (local-first POS), CF-35 (biometrics under PDPL), CF-64 (retention), ADR-0020 (as amended 2 October 2026: personal data typed into an AI prompt is scrubbed offline in the cell before any model reads it)

---

## Why this is written late

**The separation is built and complete.** Four `pii.*` tables, ten operations touching
`ledger.posting`, fifteen touching `pii.*`, and — verified 17 August — **zero operations touching
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

    ledger.posting            subject_id: uuid    ← a pointer, never a name
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

**ADR-0020 (amended by ADR-0049: vectors live in a Qdrant collection per tenant) named the AI half. `removeIndexEntry` exists for the vector half.** The rest is
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


---

## Amended 3 November 2026: the module tables' personal columns move into pii.*

**The lead, 3 November 2026, on the r13 system review's findings B-01 and C-11: personal data, "Move the columns".**
The invariant above held for `pii.*` and the ledger and nowhere else. The review found the names, contacts, birth
dates, ID numbers and IP addresses of guests, participants, holders, recipients, employees and contacts held as
columns of the module tables (52 columns in 24 tenant tables once read with the person-name roles), the contract
fields with those names unmarked (two of 96 carried a data class), lists returning them to anyone with ORDER_VIEW,
RENTAL_VIEW or the like, an export that asked one module of eleven, and an AI erasure that left prompts, answers and
messages. The rules are now:

1. **A natural person's identifier is kept in `pii.*`, never as a column of a module's table.** A contract field
   that holds one is marked `x-ticvai-data-class: personal` and `x-ticvai-pii: {store, subject}`: the store is the
   `pii.*` field it lives in (`subject.displayName`, `subject.givenName`, `subject.familyName`,
   `subject.dateOfBirth`, `subject.nationality`, `subject.preferredLanguage`, `contact.email`, `contact.phone`,
   `contact.mobile`, `contact.point`, `document.number`, `identifier.ipAddress`; `tools/personal_data.py`), and the
   subject is the property of the same row that holds the person's `pii.subject` id. That property says the kind of a
   subject created for the row (`x-ticvai-subject-kind`: guest, employee, contact or applicant). **The row keeps only
   the id**, so erasure is a delete in `pii.*` and a pseudonym everywhere else, as the decision above already said.
   The field stays on the wire: a client reading a holder's name still gets it, from the store.
2. **The module writes and reads the field through Identity**, the owner of `pii.*` (ADR-0055 rule 4):
   `recordSubjectDetails` in the request that writes its row (creating the subject when the row has none), and the
   `subjectDetails` query to answer it. The IP address a row was made from lives in `pii.subject_network_identifier`,
   against the subject and the module's row.
3. **Every personal field is marked** (`x-ticvai-data-class: personal`; `business` for an organisation's contact
   under the same name), in every contract, request, response and view.
4. **A response that carries a personal field is answered under the PII permission.** The operation's permission
   is `GUEST_VIEW_PII` (or `REPORT_EXPORT_PII`, `BIOMETRIC_IMAGE_VIEW`), or it declares `x-ticvai-personal-data`:
   `gated`, each personal field is answered only to a caller holding `GUEST_VIEW_PII` at the row's scope and is null
   to any other caller (a guest reading their own record gets their own fields), the CR-141 rule of the guest
   profile made general; or `self`, the operation answers only the caller's own record.
5. **Erasure and export reach every module.** `handoff/subject-data-register.json` lists, by contract, every table
   holding a subject's data (a subject column of any name, a field kept in `pii.*` for its rows, or a personal field
   kept on the row). Each of those contracts answers `identity.privacyRequestRaised` from a job of its own: its part
   of the export for `access`, the erasure of the personal fields it keeps outside `pii.*` for `deletion`, recorded
   with Identity's `submitSubjectDataPart` (Marketing through its existing consumer). Identity's erasure job empties
   the subject's `pii.*` rows and holds the erasure done only when every owner has answered and `ai.eraseSubject` has
   nothing left; **partiallyFailed is still not a synonym for completed**. A suppression outlives the erasure by its
   address hash, so a guest who asked not to be contacted stays uncontacted.
6. **The AI side is a module like the others.** `ai.conversation` and `ai.message` carry the guest's subject id,
   and `eraseSubject` deletes the guest's conversations, messages, feedback, recommendation rows and the memory
   metadata, and clears the prompt and response of their activity rows. `ai.decision_record` holds personal content
   only by reference, so its hash chain stays whole.

`tools/check-personal-data.py` holds them (PD-COLUMN, PD-UNMARKED, PD-NOT-MOVED, PD-STORE, PD-RESPONSE,
PD-MODULE-PART, PD-MODULE-ERASE); `tools/derive-schema.py` gives a marked field no column, and `tools/derive-ddl.py`
retires the column the databases hold and writes its copy into `pii.*` for the migration owner
(`handoff/migration-review.md`, "personal data moved"). CHG-R14M-001.

**What this does not settle.** The control database holds its own people (prospects, partner contacts, developers):
it has no `pii` schema and no PII permission, and ADR-0043's regional control database is the lead's open
control-plane decision (review finding B-02), so the check does not judge it yet; its fields are marked all the same.
The ledger's tax documents carry a buyer's name under the tax law's retention, which outlives an erasure request:
that is the lead's to decide, and it is not moved here.
