# Sources

> **Purpose:** Client-supplied source documents. The authoritative inputs everything else derives from.
> **Owner:** Chitrangi (MoM) · Qossai / Allam (client documents)
> **Status:** Living — add on receipt

**Read-only.** Nothing in this folder is edited. Corrections to a MoM are raised with
Chitrangi and a revised document is added; the original stays.

---

## Authority

Per [overview](../docs/overview.md) §2, these rank differently. This is the single most
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
| 03 Aug 2026 | `TICVAI_UIUX_MoM_03Aug2026__1_.docx` | Two mobile apps · dedicated venue-scanner · consistent POS across device types |
| 05 Aug 2026 | `TICVAI_Kickoff_MoM_2026-08-05.docx` | Three B2B models · **identity ≠ entitlement** · kiosk channel |
| 07 Aug 2026 | `TICVAI_BackendDeepDive_MoM_07Aug2026.docx` | Five-level permissions · data mask · **ticket ID ≠ media code** · component/attribute variants |
| 10 Aug 2026 | `TICVAI_Kickoff_MoM_2026-08-10.docx` | **Database per tenant** · module licensing · guest-app app scope · queue wait-time via third-party feed |
| 12 Aug 2026 | `TICVAI_Kickoff_MoM_12Aug2026.docx` | **Finance deep-dive** · single session · Sale Board per workstation · conditional role selection |

### Known record defects

| Defect | Detail |
|---|---|
| **Lost subject** | 10 Aug §5.1 — *"agreed this makes more sense and will be adopted"* names nobody. No owner for a decision since partially reversed. CF-23 |
| **Self-contradiction** | 12 Aug decision block — one bullet says front-end selection is role-driven and not device-driven; another says it auto-loads from the workstation. Resolved by [ADR-0002](../docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md) |
| **Party inversion** | 12 Aug §23, §25 — party attribution is inverted relative to every prior MoM. Five action items have ambiguous ownership. CF-25 |

Per [overview](../docs/overview.md) §8, decisions that contradict each other within one record,
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

## `designs/` — Design material

Two different things live here, and they do not carry the same weight.

**Client material. Rank 3, directional.**

| File | Covers |
|---|---|
| `Ticvai_Design_Vision_Book_v1_1.pdf` | Design vision and direction |
| `TICVAI_White_Label_Guest_App_UI_Reference_1.pdf` | Guest B2C app UI reference |
| `TICVAI_Employee_App_UI_Reference_1.pdf` | Employee app UI reference |
| `Park_POS_dc.html`, `Park_POS_v1_dc.html` | Early POS explorations |

Design references are a **starting point, not a specification** (03 Aug §2). Where a design
reference conflicts with a MoM decision, the MoM wins.

**Our own builds, from our own sources.** These were not given to us. They were built by a
teammate's Claude Design session reading this package's MoM transcriptions and screen specs, which
is why they agree with the contracts rather than merely resembling them — and why they outrank the
PDFs above for anything about structure.

| File | Covers | Standing |
|---|---|---|
| `TICVAI_POS_Terminal_client_approved.html` | P04, 30 screens | **Client-approved.** The fidelity reference every other build is measured against |
| `booking-skeletons/` | The guest booking spine | The design system of record for the booking flow |

`booking-skeletons/` is a white-label booking engine, not a mockup. One fixed step spine —
Select, Seats, Extras, Details, Payment, Confirmed — composed from **16 module factories** (chips,
date, note, counters, cards, form, timeline, event, benefits, heights, toggle, spec, sessions,
menu, matrix, expand) and covering **34 flows across five verticals**: theme park, water park, stadium, theatre and
dining. Brand, palette, type, density and layout are configuration; the theme is derived from a
logo by sampling its pixels. Its own claim is that **a new flow is a data entry, not new UI.**

That claim is the reason it matters here. Roughly **55 of the 134 guest screens** across P01, P02
and P05 sit on this spine. Those are to be *mapped* onto the modules — flow, modules in order,
configuration — and not drawn again. A screen that genuinely will not compose from the fourteen is
a missing module and should be reported as one. The remaining guest screens — account, membership,
engagement, in-venue services, support — are not covered and do need drawing.

The pack's own README says fourteen modules and omits `date()` and `toggle()`, both of which are
in use — the count above is read off the code, which is the one that renders.

**A flow is a data entry that renders itself**, not a drawing. The unit looks like this:

```js
{ id: 'day', label: 'Dated day pass', pay: 'full', requires: ['lead', 'consent'],
  modules: () => [date(), expand('tt', 'Choose your ticket', [...]), note('nudge', ...)] }
```

So work against this pack means **adding an entry to `flows: []`**, not authoring HTML that
resembles the output. Anything hand-drawn in its style is a fork of the engine on day one.

Open `TICVAI_Booking_Skeletons.dc.html` directly; `support.js` and `logos/` sit beside it and every
path in it is relative, so it renders from disk with nothing installed.
`TICVAI_White_Label_Booking.earlier.dc.html` is the previous iteration, kept because it shows which
decisions were reversed.

**The POS build is a bundle; the Skeletons pack is source.** That difference decides how each one
can be extended. `TICVAI_POS_Terminal_client_approved.html` is 5.67 MB of which only 20 KB is
reachable text: the build itself is a JSON-escaped string on one line inside
`<script type="__bundler/template">`, with 4.67 MB of base64 assets on another. It cannot be
edited, diffed or read in that form. `tools/extract-design-document.py` unpacks it --

    python3 tools/extract-design-document.py         sources/designs/TICVAI_POS_Terminal_client_approved.html         --out wireframes/design-base/pos-terminal --apply

-- into a 0.95 MB document plus 48 assets, with every `src="<uuid>"` rewritten and
`window.__resources` injected so the 29 images reached through `_P('ph20', ...)` resolve instead of
silently falling back to paths that do not exist. **The output lives under `wireframes/`, which is
not mirrored**, because it is derived from a file already in the package and copying 4.6 MB into
six bibles buys nothing. It is not committed as the source of truth; the bundle is.

**The palette trick does not survive being copied out.** It reads logo pixels through a canvas,
which needs a same-origin image. A frame that points at `logos/` works here and comes out blank on
a board. Frames drawn from this pack must leave logo and photo slots empty, naming the source file.

**What was left in the zip.** 16MB of pasted conversation screenshots, a rendered export of the
earlier build, and a copy of the POS terminal that is byte-identical to the one above
(`ab1b7d3b559a8a14ea36c86d13eb3ee2`) — checked, not assumed. The zip is at
`adam/Venue ticketing platform design.zip` if any of that is ever wanted.

---

## `diagrams/`

| File | Covers |
|---|---|
| `MultiTenant_Hierarchy_Diagram.png` | Tenant → Brand → Region → Venue → Department → Sub-Department → Workstation |

Rank 3, but load-bearing. It is the source for:

- The seven-level hierarchy ([architecture/hierarchy-and-authz](../docs/architecture/hierarchy-and-authz.md))
- Region owning currency, decimals, date format and time zone — inherited by all venues
- Venue-level configuration isolation
- **"No cross-venue data access unless explicitly permitted"** — the assertion driving row-level security
- Unified reporting at all seven levels, which forces the central warehouse

The client's own example spans **two jurisdictions** — AED at 2 decimal places, OMR at 3 —
which is the origin of [ADR-0001](../docs/adr/0001-cell-architecture-one-tenant-per-jurisdiction.md)
and [ADR-0008](../docs/adr/0008-money-carries-per-region-scale.md).

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
3. **Domain vocabulary.** Sourced into the [glossary](../docs/glossary.md), which is the durable
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
3. If it is a MoM, add it to history/timeline.
4. If it changes a settled position, raise a CF item in
   [registers/conflicts](../docs/registers/conflicts.md) — a new document does not silently
   supersede a decision.

## What arrived on 18 August, and what it changed

**Five client documents had never entered this package**, and the requirement walk had verified
the matrix against the contracts without ever checking the other direction. They are now filed.

| | Was missing | What it settled |
|---|---|---|
| `rfp/` | **The RFP itself** | Evaluation criteria — **AI at 15%, naming the four capabilities CF-73 parked.** CF-139 |
| `planning/` | **The delivery plan** | 23 epics, 7,552 person-days, and priorities that contradict the dependency order. CF-140 |
| `planning/` | Task tracker from workshops | Workshop actions, not yet swept |
| `mom/` | 14 August MoM | Referenced 29 times in the package and never filed |
| `mom/` | **18 August MoM** | Ten backlog entries settled, one ADR contradicted. CF-138 |
| `requirements/` | Seating manifest and amphitheatre plan | The CF-17 sample, used on 18 August and never filed |

**The lesson is the filing, not the reading.** The 14 August minute was cited twenty-nine times
across the package by people who had read it, and it was never put where the next person would
find it. A source consulted and not filed is a source the package cannot be checked against.

**The 18 August workshop is the sharpest instance of why this matters.** It records a client
decision that F&B configuration moves to outlet level — reversing a decision ADR-0018 names,
dates and gives as its worked example — and it settles ten open backlog entries, including one
the walk had explicitly flagged as *worth asking whether it is wanted* on the same day the
client answered no.

---

## Added 24 August — the folders that were missing

**`boards/` is new.** The client's design-board PDFs — F&B, POS, Retail and Inventory dashboards —
were in the project context and not in this folder. **They are the source the `*.dc.html` packs in
`wireframes/` were drawn from**, and what 84 screens carrying `wireframe.status: designed`
ultimately cite. Having the derived boards without the originals meant a disagreement about a frame
had nowhere to be settled.

Also filed: three backend structure references into `requirements/`, the second requirement matrix,
the technical product sheet, two email attachment registers into `planning/`, and the client's
multi-tenant hierarchy diagram into `diagrams/`.

### Two things to know before reading the latest minutes

**Three MoMs are named `.docx` and are markdown inside.** `TICVAI_MoM_2026-08-20`, `-08-21` and
`-08-24` will not open in Word and will not parse with `python-docx` — **open them as text.** Kept
exactly as received; worth correcting upstream.

**The 20 August minute says so in its own header**: the session was filed as *F&B, Retail,
Procurement & Inventory* and covered none of it — it was CRM, marketing, loyalty, RBAC and CMS.
**That workshop is still outstanding** and is an open action in all three latest minutes.

### What the latest three changed

**24 August.** Dinesh recommended **segregating databases per service from the start**, arguing that
splitting a centralised database after two or three years is harder than merging isolated ones
later. **That is in tension with ADR-0005 and ADR-0028**, which specify one Postgres per cell with
schema-level segregation — the tension is live, not settled. Also: 100–200 tenants centralised,
**plus dedicated infrastructure for flash sales reaching tens of thousands concurrent within
hours**, which the package does not yet model. Access-control vendor narrowed to HID or Suprema
(CF-35).

**21 August.** Seat-map copy/paste at full-map and section level, and layout version comparison.
`createSeatMapTemplate` exists; **copy/paste and version diff do not.**

**20 August.** Duplicate detection, identity resolution and merge rules are covered by `mergeGuests`
and CF-160. **Consent retention and archival policy is not**, and it was discussed.
