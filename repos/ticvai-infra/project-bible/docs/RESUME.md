# Resume here

**Written 18 August 2026 at the end of the requirement walk.** If you are picking this up in a
new session with no conversation history, read this file first and nothing else.

---

## Where things stand

| | |
|---|---|
| **Requirement walk** | **Complete. 3,184 of 3,184 matrix rows, 142 of 146 sections.** |
| Overall gap rate | **21%** — steady between 20% and 24% from section fifteen onward |
| Package | 27 contracts, 376 screens, 26 ADRs, ~1,960 files |
| Backlog | **178 entries, 175 open** — 132 deferred, 24 decision, 19 settled |
| Clusters | **22 clusters covering 136 entries; 42 singletons** |
| Conflict register | **143 conflicts, 40 open** — CF-120 to CF-140 raised by this walk |
| Validators | **All nine green.** `bash tools/refresh.sh` |

**Verdict split:** CONTRACTED 1,544 · CONTRACTED_PARTIAL 585 · GAP_CONTRACT 650 ·
GAP_DECISION 27 · PARKED 378.

The four "missing" sections are label artefacts — 2.2, 2.3, 2.4 and the phantom Payment row
at 1171. Nothing is unwalked.

---

## Read these, in this order

| File | Why |
|---|---|
| `docs/registers/clusters.md` | **Start here.** 175 open entries grouped into 22 clusters by what one decision closes |
| `docs/registers/conflicts.md` | 143 conflicts. CF-120 to CF-140 are this walk's |
| `docs/registers/contract-backlog.md` | Every entry with lane, blockers and reasoning |
| `handoff/traceability.json` | Every matrix row, its verdict, its evidence and why |
| `sources/README.md` | What client documents exist, which were missing, and what they changed |

---

## What the walk found, in one page

**The package is stronger than the gap rate suggests, and unevenly so.**
`maintenance` (8%), `workforce` (4%), `finance` (18% across 219 rows), `access` (9% across 77),
`seating` (10% across 112) and `approvals` (9% across 80) are close to complete.
`catalogue` is a spine contract at 31%, and Developer & API (50%) and Device Management (35%)
are two of CF-21's three uncontracted domains.

**Six structural questions came out of it**, each absorbing a dozen entries:

- **CF-125 / CL-01 resource management** — 98 row citations, no bookable-resource model. 7.6.15 says so in the client's own words. **The delivery plan puts it at P3.**
- **CF-132 / CL-05 portfolio and family** — eleven appearances across ten sections
- **CF-134 / CL-03 alerting** — six contracts detect their own trouble and none tells a person
- **CF-129 / CL-04 waivers, capture and surveys** — one form mechanism serving three needs
- **CF-131 / CL-06 payments** — tokenisation blocks recurring billing, auto-reload and payment links
- **CF-135 / CF-136** — the two uncontracted domains, each with a security dimension

**Three findings came from documents, not the matrix:**

- **CF-138** — the client decided outlet-level F&B configuration on 18 August, and **ADR-0018 records them confirming venue-level on 14 August** and names outlet as a rejected alternative. `check-config-scope.py` enforces the old rule as a build gate.
- **CF-139** — the RFP weights **AI at 15% of the evaluation** and names the four capabilities CF-73 parked (194 requirements).
- **CF-140** — the delivery plan prices 7,552 person-days and its priorities invert the dependency order.

---

---

## Two things about the matrix you must know before touching it

**A reference number does not uniquely identify a requirement.** `handoff/matrix-analysis/`
records **28 reference collision pairs (CF-120)** — two different requirements sharing one
number, across 5.5, 5.6, 8.1, 8.3 and 22.3. The walk suffixed the second block in
`traceability.json` (`5.5.1b`, `8.3.55b`, `22.3.1b`) while keeping `matrixRef` unsuffixed.
**Any analysis keyed on the raw reference silently merges two requirements** — that is how
sixteen journey-automation requirements at 22.3b share numbers with case management.

**The section labels do not describe their contents.** 2.6 labelled *Call Center Sales* is the
B2C website; 4.2 labelled *Promotions* is payments; 4.4 labelled *Upsell* is retail POS and
inventory; 7.1 labelled *Retail POS* is RBAC and audit; 12.1 labelled *Reporting and
Dashboards* is accreditation. Use `TICVAI_canonical_section_map.csv`, not the labels.

## What to do next

**1. The cheapest work with the widest reach, not the biggest.**
**CL-02 is 115 row citations of settled-lane work** — `DataSource` has fourteen values and the
matrix asks reports about twelve more things that already persist. One enum extension.
**CL-10 versioning** has a working precedent in `white-label` (`listConfigVersions`,
`restoreConfigVersion`, `diffConfigVersion` with a `contentHash`) and covers eight entities.
The 19 settled-lane entries are one contract each with precedent in place.

**2. The six decision clusters go to Qossai together** — CL-01, CL-04, CL-05, CL-06, CL-11, CL-12.
They are scope questions rather than design ones, and CL-01's priority contradiction with the
delivery plan belongs in the same conversation.

**3. Three client documents have never been read.** The tracker's own source sheet lists them:
a **3.66 MB TICVAI Finance Backend Structure Reference**, an FnB POS visual reference, and a
`technical documents/` folder of 13 items dated 11 August. **The finance one matters most** —
219 finance rows were just walked and CF-133 raised on tax invoices with that document unread.
Ask Allam before reconciliation starts.

**4. Reconciliation is the larger half and has not begun.** No contract edits were made during
the walk by design — discovery first, clustering second, reconciliation third. **Do not
reconcile the spine until orders, access, finance, shift and approvals are taken together.**

---

## How this package works

**Contract-first.** ADR-0024: nothing is built until the contract describing it exists.
The 27 OpenAPI files are the deliverable; `check-package.py` refuses any screen naming an
operation no contract defines. There is no SQL and no application code — deliberately.

**Registers are generated, never hand-edited.** Edit the JSON, run the generator:

| Edit this | Run this | Produces |
|---|---|---|
| `handoff/contract-backlog.json` | `tools/build-backlog-index.py` | `docs/registers/contract-backlog.md` |
| `handoff/backlog-clusters.json` | `tools/build-cluster-index.py` | `docs/registers/clusters.md` |
| `docs/registers/conflicts.md` | `tools/build-cf-index.py` | `docs/registers/conflict-status.md` |

`bash tools/refresh.sh` regenerates everything and runs all nine validators. **Run it before
every export.** It has caught real errors — including one where a backlog entry was deleted
rather than withdrawn, and one where withdrawing an entry left ten verdicts asserting a gap
the client had declined.

**Verdict taxonomy:** CONTRACTED, CONTRACTED_PARTIAL, GAP_CONTRACT, GAP_DECISION, ROUTED,
PARKED, SUPERSEDED. **Backlog lanes:** settled (one contract, precedent exists), deferred
(cross-contract or no precedent), decision (needs a client or commercial answer — raise a CF).

**The project-bible mirrors under `repos/` are generated.** Each code repo carries a copy of
the design context so a developer inside it need not clone the docs repo. **They drifted 78% —
352 of 449 files — in a single day**, because copying without a sync step always does.
`tools/sync-project-bible.py` now refreshes them and runs inside `refresh.sh`. Never edit a
file under `repos/*/project-bible/`; edit the canonical one under `docs/` or `handoff/`.

**`tools/find-capability.py` searches contracts, screens, states, events and flows.** Use it
before writing any gap verdict. It has two known blind spots: it misses enum *values* under an
unfamiliar field name — that is how `CostingMethod` was wrongly called a gap and BL-124 had to
be withdrawn — and escaped pipes in markdown tables, which it now warns about.

**Before writing a gap verdict, check the inverse.** The systematic error in this walk was
treating *the specific thing is absent* as *nothing exists*, and missing generic machinery that
already covered it. `approvals` is generic over subject; `promotions` conditions on fifteen
fields; `reporting` is a builder. Two verdicts were reversed by exactly this challenge.

---

## Conventions

Terse and direct. Chinmay pushes back in short phrases and expects the error to be
self-identified and corrected without ceremony. Do not hedge, do not pad, do not ask
permission to do obvious work. Documents follow the 31 July MoM pattern: Word, landscape where
appropriate, alternating row shading, reference-numbered rows.
