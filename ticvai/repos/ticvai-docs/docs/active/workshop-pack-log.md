# Workshop pack — what was done, and how to re-verify it

**A run log, kept by hand.** The package derives almost everything and can therefore answer "what
is true now" at any moment — but not "what did we do, and when". This file is that second
question. Every entry names the command that produced the change, so any claim here can be
re-checked rather than believed.

**Every number below was re-derived on 4 September against the package as it stands**, not copied
forward from the run that produced it.

---

## Source

`Workshop Docs.zip` — 17 module reference PDFs, 1,058 pages, fully text-extractable.

| | |
|---|---:|
| PDFs in the zip | 17 |
| Copied into `sources/workshop/` | **17** |
| In the zip and missing from the package | 0 |
| In the package and not in the zip | 0 |

## The chain, and where each hop is checked

```
Workshop Docs.zip
  │  tools/parse-workshop-pack.py --check
  ▼
sources/workshop/pack.json          590 screens · 59 boards · 17 sources
  │  tools/derive-pack-screens.py --apply
  ▼
screens/P08,P09,P10,P12,P13.yaml    590 screens carrying source.pack + source.board
  │  tools/derive-wireframes.py         (one board per PLATFORM — how a team builds)
  │  tools/derive-pack-boards.py        (one board per WORKSHOP BOARD — how the client reviews)
  ▼
wireframes/                         5 platform boards · 59 WS boards · 2 indexes
```

**The parse is gated, not trusted.** `parse-workshop-pack.py --check` fails unless it reconciles to
exactly 590 screens across 59 boards; a parse that does not reconcile stops the chain rather than
feeding it.

## Reconciliation, as a multiset

Compared on `(pack, board, number, title)` — **not on `(pack, number)`**, which collapses 590
records to 500 because a screen number repeats across boards within one document. A first pass
here reported a 90-screen gap that did not exist, and the key was the whole of the error.

| | |
|---|---:|
| Records in `pack.json` | 590 |
| Screens in `screens/P*.yaml` with `source.pack` | **590** |
| In the pack and not in `screens/` | **0** |
| In `screens/` and not in the pack | **0** |
| Boards in the pack | 59 |
| Boards present in `screens/` | **59** |
| Screens per board | 10, on all 59 |

## Placement

Each board went to the platform that owns its module. No board is split across platforms.

| Platform | Boards | Screens |
|---|---:|---:|
| P09 TICVAI Web | 28 | 280 |
| P08 Venue Management | 22 | 220 |
| P13 Venue CMS | 4 | 40 |
| P10 Partner Web | 3 | 30 |
| P12 Venue Support | 2 | 20 |
| **Total** | **59** | **590** |

## Wireframes

**Two groupings of the same cards, and they cannot disagree** — `derive-pack-boards.py` imports
`render_screen` from `derive-wireframes.py` rather than reimplementing it, so a card is rendered
once and only regrouped.

- **5 platform boards** — `wireframes/P## <Name>.dc.html`. What a team builds from: a team owns a
  platform, a platform owns a file.
- **59 workshop boards** — `wireframes/WS## <Module> Board <n>.dc.html`. What the client reviews:
  the board is the unit the pack was written in. Each card links back to its platform board.
- **1 new index** — `wireframes/TICVAI Workshop Boards.dc.html`.

`derive-wireframes.py` was taught the `WS##` prefix so its manifest files these as
`workshopBoards` rather than `unrecognised` — that list is what somebody reads to find leftovers
from a rename, and 59 generated files sitting in it would make it useless for its purpose.

**1,680 anchor references checked, 0 broken** — every `wireframe.board` and every
`wireframe.workshopBoard` resolves to an `id=` that exists in the file it names.

## Contract linkage

`tools/derive-pack-linkage.py` — entity from the title × verb from the archetype, matched against
operation *names*.

| | |
|---|---:|
| Wired to an operation that exists | 13 |
| Candidate below the wire threshold | 27 |
| No operation exists | **550** |
| Distinct operations to author | **613** |

Named per screen in [workshop-contract-gap.md](workshop-contract-gap.md). **A proposed name is a
specification, not a decision** — the request and response shape, the permission, the scope level
and the audience are the parts a person writes.

## Checks, 4 September

All eleven pass at 1,090 screens.

```
check-screens             PASS ·  128 warnings
check-flows               PASS ·   51 warnings
check-states              PASS ·    2 warnings
check-config-scope        PASS ·    0 warnings
check-backlog             PASS ·    1 warning
check-traceability        PASS ·    0 warnings
check-wireframes          PASS ·   36 warnings
check-frontend            PASS ·    1 warning
check-package             PASS ·   17 warnings
check-screen-redundancy   PASS ·   20 warnings
audit-links               every link resolves
```

**`check-package` failed 6 on the first run after the boards were written** — stale mirrors, one
per repo, because 60 new files and 5 edited screen files had not been copied out. `derive-mirrors.py`
cleared it. **The mirror check is the thing that caught it**, and it is worth keeping in mind that
writing files is only half of a change in this package.

## Open, and not started

- **613 operations to author.** The pack specifies what a screen shows, not what serves it.
- **Tables for the new screens**, blocked on the operations — `check-package` flags a table written
  by nothing.
- **Four area-number collisions.** Areas 10, 11, 12 and 13 are each claimed by two documents
  (Customer Service / Pricing, Ticket Upgrade / Waiver, Communication / Order, Membership / Rules).
  **The client should settle these**, not us.
- **56 "Command Center" screens** — an open design question that sizes the contract work.
- **MoM review** for per-board additional input. Never started.
- **`screens/_schema.yaml` is still not enforced.** Nothing imports `jsonschema`. The pack screens
  carry `wireframe.status: generated`, which is not in the schema's enum
  (`notStarted|inProgress|review|approved`), and nothing caught it — because nothing checks.

## Re-verifying any of this

```bash
python tools/parse-workshop-pack.py --check     # zip -> pack.json, gated at 590/59
python tools/derive-pack-screens.py             # dry run: what would land in screens/
python tools/derive-pack-boards.py              # dry run: 59 boards, 10 each, 0 split
python tools/derive-pack-linkage.py             # dry run: 13 / 27 / 550 / 613
python tools/check-package.py                   # includes the mirror check
```

Every one of these is idempotent and safe to run without `--apply`.

---

# 4 September — estate merge and audit

**Run before the next Claude Design drop**, so the drop lands on a package that already knows what
it has.

## Merged

| What | Where |
|---|---|
| `ADM-318 Dead Letters` | P09. `listDeadLetters` + `replayDeadLetter` both existed and **no screen called either** |
| `listIndexFailures` | `contracts/satellite/ai.yaml`. `ai.index_failure` had **no operation at all** |
| Wired onto `BO-091 AI Policy & Spend` | Failure rate beside spend — both answer *is it working, what does it cost* |

**Deliberately not DEV-005 Webhooks.** `replayEvents` is partner-facing redelivery of a customer's
own integration; handling a platform failure as a customer integration question is how it stays
unfixed.

## The ADM-038 collision, and the lock that replaces it

Two workstreams both allocated **ADM-038** — each took `max+1` over the screens it could see,
neither could see the other, nothing held a number. One 'Dead Letters', one 'Communication Service
Command Center'. Silent on both sides.

`screens/_id-register.yaml` is now the issue log: **a number in it is spent.** `check-screens.py`
fails on a screen issued above the recorded high-water mark, and `derive-id-register.py --apply`
runs in `refresh.sh` before that check. A retired id is never reissued — `nextFree` is the
high-water mark plus one, gaps included.

## New checks

- **Failure-table coverage** (`check-screens.py`). The inverse of the guest-coverage rule: one asks
  whether a guest can reach what they may call, this asks whether an operator can see what the
  platform dropped. Caught `ai.index_failure`, and found a third table nobody had named —
  **`fnb.kitchen_exception`, still open.**
- **Readers derived from contracts, not the lineage** — see the structural finding below.
- **Id register** (`check-screens.py`), as above.

## New tools

`derive-pack-boards.py` · `derive-id-register.py` · `audit-screen-estate.py`

## 🔴 Structural finding — two handoff artefacts nothing regenerates

**`handoff/api-data-lineage.json` and `handoff/screen-index.json` are read as authoritative by
twenty-plus tools, and no tool in the package writes either.** They arrive with the dump.

So adding an operation to a contract does not reach the lineage, and adding a screen does not reach
the index — both were maintained by hand this session, which is the wrong answer and is recorded
here as such. `check-package.py` catches the drift (it failed on both), so the gap is visible
rather than silent, but **a `derive-lineage.py` and a `derive-screen-index.py` do not exist and
should.** That is the largest single piece of derivation debt in the package.

## Estate audit — `docs/active/screen-estate-audit.md`

| | |
|---|---:|
| Audience declared and never served | **74** operations |
| Single-audience read on an entity several audiences work | **94** operations |
| Authored screens nothing navigates to | **184** |
| Pack screens nothing navigates to | 590 (expected — never wired) |
| Exact functional duplicates | 107 |
| Screens in an identical-signature cluster | 171 (15%) |

**The first version of that tool reported 158 audience gaps and most were noise** — the screens say
`platformAdmin` and the contracts say `staff`, and conflating two vocabularies invented findings.
Mapped explicitly; `device` and `service` excluded, because the absence of a UI for a turnstile is
not a design gap.

## Checks, after

All eleven pass. `check-package` 17 warnings, `audit-links` every link resolves.

---

# 4 September — buckets 1 and 2

Worked from `tools/screen-ledger.py`, which is new and is the accounting nothing in the package had.

**199 → 242 screens done**, and two obligations are now clear on every authored screen.

## Bucket 1 — screens calling no operation: 14 authored → 9

Wired **BO-067**, **PTR-019**, **SUP-006**, **CMS-013**, **CMS-017** to operations that already
existed in the contracts. `CMS-013` closes a `check-package` warning from the other end —
`control.seo_metadata` was *written by `setSeoMetadata` and read by nothing*.

Two judgements: **`setApiQuota` is not on PTR-019** (declared `staff`, and that is a partner
surface), and **PTR-019 moved `requiresModule` from `partner` to `developerApi`** after the drift
check flagged it.

The 9 left are correct or blocked: 5 are presentation surfaces that legitimately call nothing, and
**4 are the P11 accreditation journey — `audience: public` with no public-audience operation in
the contracts.** That is a contract decision.

## Bucket 2 — screens nothing navigates to: 184 → 0 authored

🔴 **The 184 was my own tool being wrong.** It counted only `exitTo` and ignored `entryFrom` — the
same edge declared from the destination, and there are **343 of them** — and it counted the 15
declared entry points as orphans. Corrected, the real number was **78**.

All 78 now have an inbound edge. **P06 was 38 of them and had one shape**: every screen exited to
the hubs, `EMP-003 Home` exited to `EMP-004` and then straight to `EMP-051..070`, and everything
between 005 and 050 fell out of the graph — a contiguous range the inference simply missed.

Edges are declared as `entryFrom` on the destination, with `inferred: false`, and **a follow-on is
parented to what it follows** rather than to a home screen: `KSK-008 Payment unresolved` from
`KSK-007 Payment`, `EMP-027 Incident detail` from `EMP-026`, `GST-071 Payment Methods` from
`GST-039 Profile`.

**Declaring the navigation non-inferred turned one warning into a failure**, correctly: flow F62
*a ticket will not scan* runs scan → manual entry → lookup, and `SCN-008 → SCN-009` was never
declared. Added.

## Viewer

The frames table's **"From"** column said *"a screen"* on nearly every row — true and useless,
because `f.source` records only which artefact supplied the frame's *name*. It now reads
**"Where it came from"** and says who made the board, which is what decides who may change it:
*we generated it, from screens* · *a client workshop board* · *a client pack, drawn* · *an earlier
design drop*.

## Where the ledger stands

| missing | total | pack | authored |
|---|---:|---:|---:|
| `ops` | 586 | 577 | 9 |
| `nav-in` | 590 | 590 | **0** |
| `nav-out` | 677 | 590 | 87 |
| `wire` | **0** | 0 | 0 |
| `impl` | **0** | 0 | 0 |
| `unique` | 175 | 3 | 172 |

Next: `nav-out`, 87 authored screens that go nowhere.

## Bucket 3 — screens that go nowhere: 87 authored → 0

**Whole platforms sat in this shape.** Nine of P15 Kitchen Display's ten screens and nine of P16
Venue Analytics' ten declared `entryFrom: [KIT-001]` / `[ANL-001]` and no `exitTo` at all — a
person landing on *Demand Forecasting* was offered no route anywhere.

All 87 had an `entryFrom` and none had a way back, which made the rule unambiguous: **`exitTo`
gains each screen already named in `entryFrom`.** That is the same edge travelled the other way,
not a guess about the product — and **no forward edges were invented.** Whether `ANL-009 AI
Assistant` should lead to `ANL-010 Suggestions` is a product question and looks like one; a way
back is not.

**`nav-out` was checked both ways before acting**, after `nav-in` had been counted wrongly the
round before: if B declares `entryFrom: [A]` then A goes to B whether or not A's `exitTo` says so.
Both counts gave 87. The tool now counts the reverse edge anyway, so it cannot drift.

**Three more real flow gaps surfaced**, again because `inferred: false` turns a warning into a
failure. Flow F31 *a menu is drafted, scheduled and rolled back* asserts `BO-045 -> BO-111`,
`BO-111 -> BO-045` and `POS-002 -> BO-045`, and none of the three was declared. The flow is the
authority on the journey and the navigation has to agree with it, so the edges were added.

## Where the ledger stands after three buckets

**1,091 screens · 320 done · 771 outstanding** (was 151 done when the ledger was first built).

| missing | total | pack | authored |
|---|---:|---:|---:|
| `ops` | 586 | 577 | 9 |
| `nav-in` | 590 | 590 | **0** |
| `nav-out` | 590 | 590 | **0** |
| `wire` | **0** | 0 | 0 |
| `impl` | **0** | 0 | 0 |
| `unique` | 175 | 3 | 172 |

**Four of the six obligations are now clear on every authored screen.** What remains on the
authored side is `unique` — and per the duplicate triage, only 42 of those are a real problem and
the action for them is to specify, not to delete. Everything else outstanding is the 590 pack
screens, which are blocked on the 613 operations nobody has authored yet.

## Bucket 4 — the under-specified clusters: 42 screens → 28

**These looked like duplicates and were empty.** Sixteen of the 42 had operations sitting unused in
the contracts the whole time; 19 references were wired across `BO-102 Sell`, `BO-104 Food &
Beverage`, `BO-105 Stock & Supply`, `BO-106 People & Access Rights`, `BO-107 Guests & Marketing`,
`BO-019 Closures`, `BO-065 Venue Configuration`, `ADM-024 Release Notification`, `ADM-026
End-of-Support`, `ADM-036 Platform Broadcast`, `ADM-145 Promotion Approval` and `EMP-022 My rota`.

**Two candidates were false friends and were deliberately left alone.** `fireCourse` /
`holdCourse` / `setCourseRules` are F&B MEAL courses — `fireCourse(ticketId)`,
`setCourseRules(outletId)` — not training, so `EMP-041 Training` keeps nothing. `recordQuotation` /
`compareQuotations` are supplier procurement against a `requisitionId`, not partner sales quotes,
so `PTR-011 Quote Management` keeps nothing. Both would have wired a plausible NAME onto the wrong
capability, which is worse than leaving the screen empty.

### 🔴 One removal was wrong and the flow caught it

`setTurnstileMode` was taken off `SCN-002 Access point & direction` on the reasoning that a config
write does not belong on a screen that reads. **Flow F06 *guest enters the venue* step 2 is
"confirms access point and direction" — and confirming the direction IS setting the mode.** The
screen was right and the tidy-up was wrong; restored, with the reasoning recorded on the screen so
it is not re-tidied.

### And one collision was created

Wiring `listRoles` onto `BO-106 People & Access Rights` made it identical to `BO-142 Store Rules,
Controls & Permissions` — both now `{getVenueSettings, listRoles}`. **That is a real new duplicate
and the cause is the same absence**: store-rule operations do not exist, so BO-142 has nothing of
its own to hold.

## What is left, and it is contract work

**28 screens across 11 clusters, and no more of it can be closed from operations that exist.**
The distinguishing operations have to be authored:

| Screens | Operation that does not exist |
|---|---|
| ADM-032 WAF & Security Policy View | a WAF rule/policy read |
| ADM-033 Backup & DR Status | a backup/restore status read |
| ADM-034 Archival Job Monitor | an archival job list |
| ADM-014 · ADM-030 scaling | a scaling-policy read and write |
| WEB-027 Newsletter Subscription | a marketing subscription |
| EMP-041 Training | a training/course record — the F&B `*Course` operations are not it |
| EMP-023 Swap request | a swap request of its own, distinct from listing the rota |
| PTR-011 Quote Management | a partner sales quote |
| ACC-005 Accreditation Badge | a badge issue/read |
| BO-142 Store Rules | store rules and controls |
| BO-101 · BO-103 · BO-108 | section summaries, or these stay hubs by design |

**Each needs a request and response shape, a permission, a scope level and an audience** — the four
things a derivation cannot supply. That is the same wall the 613 pack operations sit behind.

## Ledger after four buckets

**1,091 screens · 331 done · 760 outstanding** (151 when the ledger was built).

| missing | total | pack | authored |
|---|---:|---:|---:|
| `ops` | 586 | 577 | 9 |
| `nav-in` | 590 | 590 | **0** |
| `nav-out` | 590 | 590 | **0** |
| `wire` | **0** | 0 | 0 |
| `impl` | **0** | 0 | 0 |
| `unique` | 163 | 2 | 161 |

---

# 4 September — 16 operations drafted, and the derivation chain re-run

## The operations

Drafted as **stubs with the decisions stated**, because the four things a new operation needs — a
request and response shape, a permission, a scope level, an audience — are decisions rather than
deductions. **Every permission reused an existing one** (134 exist) rather than inventing one to
fit, and every scope level matches the neighbouring operations in the same contract.

| Contract | Operations | New table |
|---|---|---|
| platform-ops | `listWafRules` `setWafPolicy` | `control.waf_rule` |
| platform-ops | `listBackupRuns` | `control.backup_run` |
| platform-ops | `listArchivalJobs` | `control.archival_job` |
| platform-ops | `getScalingPolicy` `setScalingPolicy` | `control.scaling_policy` |
| marketing-crm | `getMarketingSubscription` `setMarketingSubscription` | `marketing.subscription` |
| workforce | `listTrainingRecords` | `workforce.training_record` |
| workforce | `listShiftSwapRequests` | — reuses `workforce.shift_swap` |
| subscription | `listPartnerQuotes` `createPartnerQuote` | `subscription.partner_quote` |
| approvals | `listAccreditationBadges` `issueAccreditationBadge` | `approvals.accreditation_badge` |
| retail | `listStoreRules` `setStoreRules` | `retail.store_rule` |

**374 → 386 tables.** All 16 wired to the screens that needed them.

### Four mistakes the checks caught, and one they did not

- **A duplicate table.** The first draft added a `ShiftSwapRequest` schema and derived
  `workforce.shift_swap_request` — a second table for rows `workforce.shift_swap` already held.
  Removed; the operation returns the existing `ShiftSwap`.
- **`derive-schema` prunes columns, not tables.** Removing the schema left the orphan table behind:
  `retired_of()` documents this exact failure for a *column* — *"a contract-side deletion can never
  reach the table"* — and the same hole exists one level up for a whole table. Removed by hand and
  **the tool still has no answer for it.**
- **YAML apostrophes.** `roster's` inside a single-quoted scalar broke `workforce.yaml`; a
  description is prose and prose has apostrophes in it.
- **`x-ticvai-config-scope`** missing on three `set*` operations — ADR-0018 requires it.
- **Unbounded list.** `listStoreRules` read a high-volume table with no page size. Paginated.

## 🔴 `derive-lineage.py` — the artefact nothing regenerated

`handoff/api-data-lineage.json` is read by twenty-plus tools and **no tool wrote it.** The 16 new
operations were invisible to every consumer, and `check-package` failed the package for a gap
nothing could close.

**The new tool is additive on purpose, and `--audit` is why.** Run against the stored file, nearly
every one of the 1,033 existing entries differs from what a schema-`$ref` walk produces —
their `reads`/`writes` are richer than the contracts alone can support. **A full rebuild would
destroy real information**, so an entry that exists is left exactly as it is and only missing
operations are added. `--audit` reports the disagreement without changing anything; somebody should
read it before anyone writes the rebuild this file eventually needs.

`service` and `stores` cannot be read off OpenAPI at all — a service assignment is a deployment
decision — so they are taken from what the contract's neighbours already use. `derive-diagrams.py`
raises `KeyError: 'service'` without it, which is how this was found.

## `build-services-workbook.py` had never run

`ROOT = Path("/home/claude/ticvai-pkg")` and an output path under `/mnt/user-data/outputs` — a
path that exists on no machine this package has been checked out on, so every run raised
`FileNotFoundError` before writing a byte. **`build-schema-workbook.py` carried the same line and
globbed nothing silently; the loud failure was the better of the two.** Repointed at the repo, and
its output now lands in `handoff/` beside the schema workbook.

## Full chain re-run

`derive-schema` → `derive-lineage` → `derive-relationships` → `derive-ddl` → `derive-burst-scope` →
`derive-sizing` → `derive-table-notes` → `derive-schema-roots` → `derive-frontend` →
`derive-board-panel-map` → `derive-diagrams` → both workbooks → `derive-wireframes` →
`derive-pack-boards` → `derive-id-register` → `link-screens-contracts` → `derive-platform` →
`derive-platform-deployment` → `build-audience` → `build-backlog-index` → `build-cluster-index` →
`derive-overview` → `sync-counts` → `derive-mirrors`.

**All eleven checks pass. 1,049 operations · 386 tables · 1,091 screens.**

| | |
|---|---:|
| Screens done | **348** (was 151 when the ledger was built) |
| `unique` outstanding, authored | 144 (was 172) |

## Closing the authored estate

Wired the last three section hubs and the promotion dashboard:

| Screen | Given |
|---|---|
| BO-101 Orders & Money | `listOrders` `listSettlements` |
| BO-103 Access & Venue | `listAccessPoints` `listScans` |
| BO-108 Venue Operations | `listWorkOrders` `listIncidents` `listAssets` |
| ADM-138 Promotion Command Center | `getPromotionUsage` |

**A hub that shows nothing of its section is a menu item, not a screen** — all four sat on
`getVenueSettings` or `listPromotions` alone, which is what made them identical to their
neighbours.

### 🔴 Two measurement fixes, and the second changed the headline

**`under-specified` was over-reporting.** A two-screen cluster on one platform is a pair — a list
and its detail, an assistant's home and its answer, a view and the act it offers. Under-specification
is THREE OR MORE screens on a thin generic set, which is what `BO-101..BO-108` on `getVenueSettings`
actually was. Widened; **under-specified is now 0 clusters.**

**`unique` was failing 141 screens the triage calls correct.** A Guest Web screen and its Guest App
twin share an operation set because they are one product on two devices — counting that as
unfinished means a screen can never be done for a reason nobody would ever act on. The column now
counts only membership of an under-specified cluster, which is the same rule `--duplicates` reports.

**That moved the ledger from 351 done to 492**, and none of the 141 was work.

## The authored estate is finished

| missing | total | pack | authored |
|---|---:|---:|---:|
| `ops` | 586 | 577 | **9** |
| `nav-in` | 590 | 590 | **0** |
| `nav-out` | 590 | 590 | **0** |
| `wire` | **0** | 0 | 0 |
| `impl` | **0** | 0 | 0 |
| `unique` | **0** | 0 | 0 |

**Five platforms are complete** — P01 Guest Web 46/46, P04 Venue POS 24/24, P07 Venue Scanner
11/11, P14 Developer 8/8, P15 Kitchen Display 10/10, P16 Venue Analytics 10/10.

**Nine authored screens remain and none is a defect this package can fix:**

- **Five are correct as they are** — `KSK-001 Attract Loop`, `KSK-014 Out of service`,
  `GST-043 Arabic / RTL`, `EMP-044 Accessibility`, `EMP-045 Arabic / RTL`. A presentation surface
  calls nothing because there is nothing to call.
- **Four are the P11 accreditation journey**, which is `audience: public` while the only candidate
  operation is `staff`-only. **An entire public applicant journey with no public-audience
  operation** — a contract decision, and the client's.

Everything else outstanding is the 590 pack screens, and re-running the linkage against the 17 new
operations moved none of them: still **13 wired · 27 candidates · 550 with no operation · 613 to
author.** The new operations are platform and back-office; the pack is product surface, and they do
not overlap.

---

# 4 September — the 613 operations, drafted

## `tools/draft-pack-operations.py`, one module at a time

**577 pack screens called no operation.** The plan's Stage 5 said *one module at a time, so a
failure names the module that caused it* — and it was right twice over.

**What is derived:** the `operationId` (entity from the title crossed with the archetype's verb),
the `audience` (the platform's own), the `scope-level` and the `permission` (the contract's own
convention, split by read and write). **No new permission was invented** — 134 exist, and a 135th
that nothing grants is a permission nobody can hold.

**What is deliberately not derived: the response shape.** The pack lists what a screen DISPLAYS —
*"17 conversions rejected by eligibility rules"*, *"Active Upgrade Paths"* — and those are
captions, not fields. Thirty-seven captions turned into thirty-seven properties would produce a
schema that looks authoritative and describes nothing. Each operation returns a **provisional
envelope** marked `x-ticvai-provisional: true`.

**And no `x-ticvai-persistence`, which is the half that mattered.** Six hundred speculative tables
would have reached `derive-ddl`, the workbook and the ER model, and every one would be a storage
decision nobody made. **An operation can exist before its storage is decided; a table cannot.**

Tables before: **386.** Tables after: **386.**

| Module | Screens | Contract |
|---|---:|---|
| Access Control | 116 | `access` |
| Promotions & Bundles | 96 | `promotions` |
| Pricing & Revenue | 70 | `catalogue` |
| Ticket Media & Credential · Ticket Resale · B2B | 30 each | `access` · `orders` · `subscription` |
| Order & Reservation | 29 | `orders` |
| Group Sales · Membership · Rules · Sales Channel · Waiver | 20 each | — |
| Customer Service · Privacy | 19 each | `marketing-crm` |
| Product Lifecycle | 18 | `catalogue` |
| Communication · Ticket Upgrade | 10 each | — |

## Three defects, and the checks found all three

**🔴 Nine operations vanished into duplicate YAML keys.** Two screens whose first three title
tokens agreed produced the same path *and* the same verb — YAML keeps the last key, so one block's
operation disappeared from the parsed document while its text stayed in the file and its screen
stayed wired to it. `check-screens` reported nine unknown operationIds; the raw text had them and
the parsed contract did not. Routes are now made unique, and the nine written before that were
renamed in place.

**🔴 A blanket `x-ticvai-config-scope` made things worse, not better.** 17 writes were missing it,
so I added it to every drafted write — and the error count went to **136**. `check-config-scope`
only examines operations its `IS_CONFIG` naming rule reaches, and *"an unexamined tag is worse
than an absent one"*. Removed 136 tags the checker never reads, using the checker's own regex
rather than a guess at it.

**`build-schema-workbook.py` read three files with no encoding** and died on cp1252 — the same
class as its `/home/claude` path, and it had been masked by that path bug until this session fixed
it. One of the fixes then duplicated an `encoding=` keyword; both repaired.

## Navigation, from the pack's own structure

**57 of the 59 boards open with a Command Center**, and the other nine screens are that board's
detail. So the first screen of each board is its hub — reached from the platform's entry point —
and the rest are reached from it and return to it. **59 hubs and 531 leaves wired**, and none of
it is a guess: the grouping is what the workshop wrote.

## Where the estate stands

**1,091 screens · 1,082 done · 9 outstanding.** All eleven checks pass.

| | |
|---|---:|
| Operations | **1,626** (was 1,032 on 3 September) |
| Tables | **386** |
| Screens | 1,091 |
| `ops` outstanding | 9, all authored |
| `nav-in` · `nav-out` · `wire` · `impl` · `unique` | **0** |

**The nine are the same nine and none is fixable here:** five presentation surfaces that correctly
call nothing, and the four P11 accreditation screens that are `audience: public` with no
public-audience operation in the contracts.

## What a drafted operation is not

**594 of the 1,626 operations are stubs.** Every one carries `x-ticvai-provisional: true`, returns
an envelope rather than a schema, and says in its own description that the shape is the part a
person writes. They make the estate navigable and countable and they are **not buildable**. The
request and response shapes, and whether each deserves a table of its own, are the client's
decisions — and they are now 594 small questions with names attached rather than one unanswerable
one.


---

# 4 September — the shapes, read out of the pack

**The previous section said the shape was "the part a person writes". That was wrong, and this
section is the correction.** The pack had not been read closely enough. Its bullets are not
captions: *"Each zone receives capacity, operating schedule, security classification, entry
requirements, exit requirements, allowed credential classes"* is a field directory written by the
people who own the requirement. **13,312 such bullets survive a strict reading** across the 590
screens — a median of 22 per screen.

So the envelope is gone. Every one of the **577** drafted operations now carries a request and a
response derived from its own screen's words.

| | before | after |
|---|---:|---:|
| Operations | 1,626 | 1,626 |
| Component schemas | 766 | **1,496** |
| Properties on drafted schemas | 0 | **15,686** |
| Tables | 386 | **386** |

## How a bullet becomes a property

`tools/packshape.py` reads the section HEADING to decide what its bullets are, because the pack is
consistent about it — `For each attraction` is a record, `Dashboard should show` is a metric list,
`Filter by` is a query, `Purpose` is prose. **Every property keeps the sentence it came from in its
`description`**, so the reading can be checked against the PDF in one step and corrected without
re-deriving anything.

**7,611 bullets were dropped rather than bent into fields** — sentences, examples, comparisons
(`Height ≥ 130 cm`), hierarchy illustrations (`→ Public Plaza`) and page footers. The count is
reported per operation so the loss is visible instead of silent.

Four readings were wrong on the first pass and were fixed before anything was applied:

- **`Support` is not a verb heading.** It sits over *Minimum Quantity / Quantity Bands / Group
  Size* as often as over *Suspend / Escalate / Publish*. Reading it as actions threw away a whole
  pricing directory. The bullet's own first word decides now, not the heading.
- **An enum list is one property, not ten.** *Public Zone / Ticketed Zone / VIP Zone / Staff
  Zone …* was becoming ten boolean-ish fields; it is `zoneType` with ten values, and the shared
  trailing noun is what says so.
- **`Scheduled Changes` on a dashboard is a count, not a timestamp.** The date rule matched
  "scheduled"; the metrics rule now outranks it.
- **A rule builder lists its operators.** `PromotionRuleBuilderInput` came out with properties
  called `and`, `or` and `not`. They are the grammar of the rule, not columns of it.

## The table question, answered with evidence

**No table was created, and this time there is a measurement behind that rather than caution.**

Every drafted write's request fields were compared against the real columns of every table its
contract owns, read out of `backend/*/0*.sql`:

| | writes |
|---|---:|
| Look like an update to a table that exists (≥50% field overlap) | **0** |
| Share a few fields with something (1–24%) | 50 |
| Share **not one field** with any table the package has | **103** |
| | **153** |

**A name match would have said the opposite.** Fuzzy-matching screen titles against table names
claimed 77 of the 153 already had a home — it paired `setMinorGuardianAge` with
`marketing.privacy_incident` on a score of 100, and `setDataDiscoveryAccess` with
`control.seo_metadata`. The fields disagree with the names, and a table is made of fields.

So **the pack is not a data model**: it specifies screens, and what those screens configure is
vocabulary this package does not store today. **13 of the 153** come closest to specifying a
record — the client wrote *"For each attraction: Attraction ID, Name, Venue, Zone, Capacity …"* —
and those carry `x-ticvai-record-definition` naming the client's own heading. They are where the
conversation starts. `docs/active/workshop-pack-write-decisions.md` is the sheet, derived by
`tools/derive-write-decisions.py`.

The evidence lives in each schema's own persistence tag, not only in the report:

```
x-ticvai-persistence: none — request only; **no existing table covers these fields** — the
  closest is access.parking_facility at 6%, so this is not an update to anything the package
  stores today and no new table has been decided
```

## Four defects the checks caught

- **The em dash is load-bearing.** `derive-schema` treats a persistence value containing `—` as
  "not a table". My evidence strings name a real table inside them and used a plain hyphen, so
  `access.parking_facility at 6%` would have been registered as a table of its own. Caught before
  it was written; the table count is 386 before and after.
- **577 duplicate `x-ticvai-consumed-by` keys.** PyYAML writes list items at the parent's indent
  and the rest of the package indents them, so `link-screens-contracts.py` did not recognise its
  own annotation and re-added it to every drafted operation — which YAML resolves by silently
  keeping the last. The emitter now writes the package's way.
- **YAML anchors.** Two schemas sharing a property object made `safe_dump` emit `&id001`, a name
  the contracts already use. The whole file stopped loading. Aliases are off.
- **Six operation names had lost a letter.** `listVirtualTicketStatu`, `listChangeImpactAnalysi`,
  `setOrderReservationStatu` — a singulariser stripping the last `s` from words that were already
  singular. Renamed across contracts, screens and the lineage; the generator has a stop-list now.

## Where it stands

**1,091 screens · 1,082 done · 9 outstanding.** All eleven checks pass; every link resolves. The
nine are the same nine: five presentation surfaces that correctly call nothing, and the four P11
accreditation screens that are `audience: public` with no public-audience operation.

**The 577 are still `x-ticvai-provisional: true`, and should stay that way.** A shape read out of a
PDF has not been agreed with anyone who has to build it. What changed is what a reviewer is looking
at: an operation with named, typed fields each carrying the client's own sentence, instead of an
envelope nobody could argue with.
