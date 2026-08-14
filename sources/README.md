# Sources

> **Purpose:** Client-supplied source documents. The authoritative inputs everything else derives from.
> **Owner:** Chitrangi (MoM) · Qossai / Allam (client documents)
> **Status:** Living — add on receipt

**Read-only.** Nothing in this folder is edited. Corrections to a MoM are raised with
Chitrangi and a revised document is added; the original stays.

---

## Authority

Per [overview](../overview.md) §2, these rank differently. This is the single most
important thing to understand about this folder:

| Rank | Folder | Authority |
|---|---|---|
| **1** | `mom/` | **Scope + binding.** Later decisions supersede earlier ones |
| **2** | `requirements/` | **Scope.** The contracted requirement baseline |
| **3** | `designs/`, `diagrams/` | Directional. Enhance, do not copy |
| 4 | *(not held here)* | Reference-system material is **not scope** and is deliberately not stored in this repo — see below |

A capability, page or endpoint that cannot be traced to rank 1 or rank 2 **is not scope**.

---

## `mom/` — Minutes of Meeting (7 documents)

Rank 1. Highest authority in the project.

| Date | File | Key decisions |
|---|---|---|
| 30 Jul 2026 | `TICVAI_Kickoff_MoM_30Jul2026__2_.docx` | Programme setup; HLD/LLD ownership |
| 31 Jul 2026 | `TICVAI_MoM_31Jul2026__1_.docx` | Offline-first POS · in-house traffic throttling · 7-year audit trail · KDS integration only |
| 03 Aug 2026 | `TICVAI_UIUX_MoM_03Aug2026__1_.docx` | Two mobile apps · dedicated scanner · consistent POS across device types |
| 05 Aug 2026 | `TICVAI_Kickoff_MoM_2026-08-05.docx` | Three B2B models · **identity ≠ entitlement** · kiosk channel |
| 07 Aug 2026 | `TICVAI_BackendDeepDive_MoM_07Aug2026.docx` | Five-level permissions · data mask · **ticket ID ≠ media code** · component/attribute variants |
| 10 Aug 2026 | `TICVAI_Kickoff_MoM_2026-08-10.docx` | **Database per tenant** · module licensing · guest app scope · queue wait-time via third-party feed |
| 12 Aug 2026 | `TICVAI_Kickoff_MoM_12Aug2026.docx` | **Finance deep-dive** · single session · Sale Board per workstation · conditional role selection |

### Known record defects

| Defect | Detail |
|---|---|
| **Lost subject** | 10 Aug §5.1 — *"agreed this makes more sense and will be adopted"* names nobody. No owner for a decision since partially reversed. CF-23 |
| **Self-contradiction** | 12 Aug decision block — one bullet says front-end selection is role-driven and not device-driven; another says it auto-loads from the workstation. Resolved by [ADR-0002](../adr/0002-authorisation-is-user-driven-not-workstation-driven.md) |
| **Party inversion** | 12 Aug §23, §25 — party attribution is inverted relative to every prior MoM. Five action items have ambiguous ownership. CF-25 |

Per [overview](../overview.md) §8, decisions that contradict each other within one record,
or omit the deciding party, are returned for correction before being treated as binding.

---

## `requirements/` — Requirement matrix

Rank 2. `Ticvai_matrix_20260621_2.xlsx`

| | |
|---|---|
| Requirements | **3,184** |
| Domains | 21 |
| Sub-domains | 118 |
| Sheets | Functionality · Integrations · Compliance & Security · Disaster Recovery & BCP · Training |

### Reading it programmatically

```python
import openpyxl
wb = openpyxl.load_workbook('Ticvai_matrix_20260621_2.xlsx', data_only=True)
ws = wb['Funactionality ']          # note the trailing space
for r in range(2, ws.max_row + 1):
    domain     = ws.cell(r, 2).value
    sub_domain = ws.cell(r, 4).value
    req_id     = ws.cell(r, 5).value
    text       = ' '.join(str(ws.cell(r, c).value or '') for c in (6, 7))
```

### Known defects

| Defect | Detail |
|---|---|
| **Sheet name** | `'Funactionality '` — misspelled, with a trailing space |
| **Duplicate IDs** | 5.6.1 → 5.6.8 appear **twice** with entirely different text. 46 rows, 38 unique IDs. Citations to those IDs are ambiguous — quote the text |
| **Split text** | Requirement text spans columns 6 and 7 and must be joined |
| **Naming mismatch** | The "Retail POS" domain's only sub-domain is "Wallet" (78 reqs) |
| **9.2% actor coverage** | Only 292 of 3,184 requirements name a human actor. The rest is written system-centric — actor assignment is a **decision to be taken**, not a fact to extract. CF-24 |

A full audit for duplicate IDs across the matrix is outstanding before it is used as the
acceptance baseline.

---

## `designs/` — Client design material

Rank 3. Directional.

| File | Covers |
|---|---|
| `Ticvai_Design_Vision_Book_v1_1.pdf` | Design vision and direction |
| `TICVAI_White_Label_Guest_App_UI_Reference_1.pdf` | Guest B2C app UI reference |
| `TICVAI_Employee_App_UI_Reference_1.pdf` | Employee app UI reference |

Design references are a **starting point, not a specification** (03 Aug §2). Where a design
reference conflicts with a MoM decision, the MoM wins.

---

## `diagrams/`

| File | Covers |
|---|---|
| `MultiTenant_Hierarchy_Diagram.png` | Tenant → Brand → Region → Venue → Department → Sub-Department → Workstation |

Rank 3, but load-bearing. It is the source for:

- The seven-level hierarchy ([architecture/hierarchy-and-authz](../architecture/hierarchy-and-authz.md))
- Region owning currency, decimals, date format and time zone — inherited by all venues
- Venue-level configuration isolation
- **"No cross-venue data access unless explicitly permitted"** — the assertion driving row-level security
- Unified reporting at all seven levels, which forces the central warehouse

The client's own example spans **two jurisdictions** — AED at 2 decimal places, OMR at 3 —
which is the origin of [ADR-0001](../adr/0001-cell-architecture-one-tenant-per-jurisdiction.md)
and [ADR-0008](../adr/0008-money-carries-per-region-scale.md).

---

## Reference-system material — deliberately not held here

The VivaTicket BOS manuals (62 documents, build 7.4.31.187) are **not** stored in this
repository.

They are rank 4 — inspiration and de-risking only, never scope — and keeping them
alongside rank 1 and rank 2 material invites exactly the failure this folder structure
exists to prevent: reference behaviour quietly becoming an expectation.

> *"This system serves as a functional reference to learn from, not a design to copy."*
> — 07 Aug 2026 session close

They remain available from the client-supplied set. Retrieve them when needed for the
three permitted uses; do not copy them back in.

### Permitted uses — three only

1. **Gap-hunting.** If the reference system needed a capability and the matrix is silent,
   raise it as a question. It becomes scope only once it appears in the matrix or a MoM.
2. **Edge-case discovery.** Anti-passback, re-entry rules, overshort thresholds, failure
   modes. Cheaper than discovering them at UAT.
3. **Domain vocabulary.** Sourced into the [glossary](../glossary.md), which is the durable
   artefact — the manuals themselves are not needed once the glossary is agreed.

### Never used for

Scope · feature inclusion · API, interface or protocol design · architecture, session or
authorisation design · data model structure · justifying work not traceable to rank 1 or 2.

### Documented exception

**Revenue recognition rules.** Allam explicitly directed that the manuals contain
recognition rules beyond the requirement matrix and are to be cross-checked (12 Aug §8).
This exception is **narrow and applies to revenue recognition only**. Extending it requires
a new MoM decision.

Anything drawn from the manuals under this exception must be **written into the matrix or
a MoM** before it is built. A capability whose only provenance is a reference manual is
tagged `REF` and is not a build item.

### What was already learned from them

Recorded here so the manuals do not need re-reading:

| Finding | Consequence |
|---|---|
| Web services are **SOAP over ISAPI, session-based** | Structurally incompatible with the stateless JWT design agreed 31 Jul. **Zero reusable API design.** Any uplift estimate must separate domain knowledge from interface design |
| Hierarchy is **three levels** — Site → Operating Area → Workstation | TICVAI has seven-plus. Rights cascade and override semantics are original work. CF-27 |
| **Roles are groupings, not permission sets** | Role = Code + Name + Description; rights attach separately. Corroborates 12 Aug §9 |
| Sale Board can act as an access-control screen | Confirms POS-embedded scanning is feasible. CF-04 |
| Supervisor Override is a first-class subsystem with authoriser storage | Corroborates the dual-authorisation model in 2.12.3. CF-07 |
| Staff resources are structurally separate from users | Corroborates the `User` / `StaffResource` split. CF-06 |

## Adding a document

1. Drop it in the correct rank folder. **Never edit an existing file.**
   Reference-system material does not belong here — see above.
2. Add a row to the table above with date and what it decides or supplies.
3. If it is a MoM, add it to [history/timeline](../history/timeline.md).
4. If it changes a settled position, raise a CF item in
   [registers/conflicts](../registers/conflicts.md) — a new document does not silently
   supersede a decision.
