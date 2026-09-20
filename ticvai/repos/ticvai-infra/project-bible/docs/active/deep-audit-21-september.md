# Deep audit — module-wise build clearance

**21 September 2026.** Pinned at commit `87a159c`. Written for the engineering leads deciding
what to staff. **Revision 2** — five findings were corrected after adversarial review; each
correction is marked in place.

> **The one-line state of the package.** 2,068 API operations, 621 database tables and 2,427
> screens are designed. **Nothing has been built** — `implementation.status` reads `notStarted` on
> all 2,427 screens, no server runs, no screen renders. The design is roughly eight weeks old and
> has never been tested against anything outside itself.

Not *"does it validate"* — **which modules can be staffed on Monday, and for the rest, the named
reason.** The bar is adversarial: a module is RED until the audit fails to find a reason it
cannot start.

**The package's own tooling was not run.** Every number below comes from reading
`contracts/`, `screens/`, `states/`, `flows/` and `backend/*.sql` directly, with ad-hoc scripts
written for this audit and thrown away. That is the point: the derived artefacts are written by
the passes under audit. **The trade is explicit — nothing here was independently reproduced by a
second method, so treat a number that matters as one to re-run, not one to cite.** Every claim
names the file it came from.

**Terms used throughout.** *Platform* `P01`–`P17` — one screen file, one surface (P04 is the POS
terminal, P08 the back office). *App* — what a user installs; five of them, each spanning several
platforms. *Contract* — one OpenAPI file per domain; *spine* means other contracts depend on it,
*satellite* means they do not. *Wave 1* — the screens the package marks as needed for opening
day; this report takes the marking as given and does not verify it. *Specified* — a screen whose
YAML declares `loading`, `error`, an `empty*` state and at least one operation. *Gate* `D1`–`D8`
(domains) and `A1`–`A9` (apps) — the clearance tests, listed in §8 and §9. *CF-nn* — an entry in
the conflict register.

---

## 1 — What was measured, and what this method cannot see

Four source-layer sweeps: operation reach (contracts × screens × flows), persistence resolution
(contract schemas × DDL), permission vocabulary (contracts × `roles.yaml`), and screen
specification (all 2,427 screens across 16 platforms).

**What this method cannot see, stated before the findings:**

- **It does not read English.** A screen with every state written and an operation declared
  passes A1 whether or not the prose describes the right screen.
- **It cannot tell an intentional gap from an oversight.** 700 operations reach no screen; this
  audit says which, not whether that is wrong.
- **It trusts the YAML parse.** Where a field carries free text — `x-ticvai-persistence` does —
  a regex decides what counts, and **my first pass got this wrong**: it reported 207 missing
  tables that were 933 deliberate `none — <reason>` values. The corrected result is in §4.
- **`operationId` also appears as a schema property.** Four lines in `marketing-crm`,
  `public-api`, `approvals` and `orders` are fields named `operationId`, not operations. A naive
  grep counts 2,072 declarations against 2,068 real ones.
- **Wave is taken as declared.** If a screen's `wave: 1` is wrong, every Wave-1 number here
  inherits that.

---

## 2 — The baseline, re-derived

`handoff/status.json` reproduced from disk on every count checked. **Use it; do not use the
landing pages.**

| | status.json | disk | |
|---|---:|---:|---|
| operations | 2,068 | **2,068** unique ids, 0 duplicates | ✓ |
| contracts | 32 | **32** (9 spine + 23 satellite) + 2 shared | ✓ |
| tables written | 621 | **621** `CREATE TABLE` (572 tenant + 49 control) | ✓ |
| screens | 2,427 | **2,427** | ✓ |
| state models · events | 125 · 29 | **125 · 29** | ✓ |
| flows | 96 + 192 | **288** files, 192 `derived-from-board` | ✓ |
| ADRs · boards | 48 · 218 | **48 · 218** | ✓ |

**The four landing pages disagree with this and with each other.** `README.md` (17 Aug) says 92
conflicts, 25 contract files, 364 screens, 23 journeys, 7 validators. `OVERVIEW.md` says *"Tables
written 0 of 623 — build has not started"* in a table, and *"2427 screens cannot be reached"* in
prose two sections below its own *"2426 of 2427 reachable"*. `COVERAGE.md` carries *"Tables
written as DDL 623"* and *"Any SQL — removed deliberately"* on one page. `MANIFEST.md` says 44
ADRs against its own header's 46, 203 flows against 288, and names
`docs/registers/decisions.md`, which does not exist. `docs/RESUME.md` — *"read this first and
nothing else"* — is entirely 18 August.

**Recommended fix.** `sync-counts.py` substitutes a fixed list of noun-phrases and cannot see a
sentence. The missing checker is the sibling of `check-authored-inputs.py`: one that reads a
narrative count and fails the package when it disagrees with `status.json`. Its first five
findings are the five files above. Until it exists, **delete the count from the prose** rather
than maintain it — the principle the package already holds is *derived, not listed*.

---

## 3 — Finding 1: the checker loop cannot fail

`tools/refresh.sh:281`:

    printf "  %-22s" "$t"; python3 "tools/$t.py" 2>&1 | tail -1 || true

**Every exit code of all 32 checkers is discarded, and only the last line of output survives.**
A checker emitting 400 errors contributes one line and does not fail the run.

The comment above it explains why, and the reasoning is sound as far as it goes: under `set -e`
with `pipefail`, one non-zero checker killed the whole script, and *"for most of 9 September this
script died at check-flows and nobody saw the eight checks below it."*

**The fix for "one failure stops the report" was to discard all failures.** The correct fix is to
collect them: run each checker, record its status, print the table, and exit non-zero at the end
if any failed. That preserves the full report and restores the gate.

**This is not theoretical — §5 is the proof.**

**How long the gate has been dark.** `| tail -1 || true` entered at `78d71ba` on **10 September
2026**. **124 commits have been made since, 109 of them touching `ticvai/`** — every one under a
gate that could not fail. That is the date after which no green claim about this package is
supported by anything.

**Status at the time of writing: fixed in the working tree, uncommitted.** `tools/run-checks.py`
(created 21 September, 02:22) runs every checker, keeps each exit code, prints the same table and
exits non-zero if a gating checker failed; `refresh.sh` now calls it, and the tail coverage guard
was widened to grep the new file so the checker list moving did not read as thirty-two unrun
tools. **This is exactly the fix recommended below.** It is not yet committed, and nothing has
verified it against a known-bad package — the eight P11 references in §5 are the obvious test
case.

---

## 4 — What is NOT broken

Stated before the rest, because a clean result on something never tested is new information.

**Persistence resolves completely.** 589 schemas carry a table-shaped `x-ticvai-persistence`
(559 single, 30 of the `a + b` composite form) = **621 table references, and every one resolves
to a `CREATE TABLE` in `backend/`. Zero dangling.** The contract → schema → DDL chain holds end
to end. This was the finding I most expected to break.

**No duplicate operationIds.** 2,068 unique across 34 files.

**Flows never name an operation that does not exist.** 1,118 operation references across 288
flow files, all resolving.

**No operation is unauthenticated by accident.** 94 operations declare no
`x-ticvai-permission`, and **all 94 carry an audience** — guest 47, service 10, anonymous 8,
device 6, and the rest mixed. None has nothing.

**Wave 1 is specified.** **169 of 176 Wave-1 screens (96%)** carry their states and at least one
operation. The estate-wide 43% hides this, and it is the single most decision-relevant number in
this report.

---

## 5 — Finding 2: eight screens call operations that do not exist

`screens/P11-accreditation-portal.yaml` names eight operations that appear **nowhere in
`contracts/`**:

    saveAccreditationDraft                   submitAccreditationApplication
    withdrawAccreditationApplication         addAccreditationDocument
    getAccreditationApplicationByReference   getAccreditationBadge
    revokeAccreditationBadge                 getApprovalRequest

The contract declares `createAccreditationApplication` and `submitAccreditationDocument`; the
screens call `submitAccreditationApplication` and `addAccreditationDocument`. **These are near
misses, which is why nobody saw them by eye.**

`check-screens.py` refuses exactly this — *"references unknown operationId"* — and the package
was committed after a refresh run. **This is Finding 1 with a body.** It is also the only
dangling-reference class found: the other direction (flows) is clean.

**Recommended fix:** rename four, write four. One session. P11 is workshop-blocked anyway
(CF-21), so the cost of leaving it is low — **the cost of leaving Finding 1 is not.**

---

## 6 — Finding 3: 485 operations assert a screen that does not call them

| | |
|---|---:|
| operations declared | 2,068 |
| **asserting a consumer** (`x-ticvai-consumed-by`) | **1,798** |
| `sum(info.x-ticvai-screen-count)` | 1,798 |
| operations a screen actually names | **1,313** |
| operations a flow actually names | 1,118 |
| named by screen **or** flow | 1,368 |
| **named by neither** | **700 (34%)** |
| **assert a screen, no screen names them** | **485** |
| named by a screen but assert nothing | **0** |

**The asymmetry is perfectly one-directional**, which names the mechanism: the annotation is
written *from* the screens and never retracted when a screen stops calling the operation. The
same additive-only shape as `derive-lineage`.

**So the published metric — "operations reaching a screen: 1798 of 2068, 87%" — is computed from
the contract's own assertion, not from the screens.** The screen-side figure is **1,313 (63%)**.

**Recommended fix:** derive `x-ticvai-consumed-by` destructively rather than additively, or drop
it and compute reach from `screens/` at read time. The annotation currently measures history.

**This one has left the building.** 87% is a coverage figure of the kind that goes into status
reports and client decks. **Someone needs to establish whether it was ever quoted externally, and
if so, correct it** — the defensible number is 63%, and it is better corrected by us than
discovered by them. The same question applies to any figure derived from an additive-only pass,
which is most of them.

---

## 7 — Finding 4: two permission vocabularies with zero keys in common

| | |
|---|---:|
| keys in `contracts/shared/permissions.yaml` | **167** |
| keys in `roles.yaml` | **44** |
| **shared** | **0** |

`roles.yaml` grants lowercase action keys (`refund.large`) lifted from the POS board; the
contracts carry `SCREAMING_SNAKE` (`ORDER_CANCEL`). `check-screens` validates a screen's `guard`
against `roles.yaml`, **so the only guards anyone could write were POS ones.**

**But the estate is far emptier than a vocabulary clash implies.** Grepped across all 2,427
screens:

| | |
|---|---:|
| `guard:` declarations in the entire estate | **12** |
| of which in P04 (Point of Sale) | **12** |
| in P08, P09, P12, P13, P16 | **0** |

Six of the twelve are `payment.take`; the rest are `sale.resume` ×2, `sale.create`,
`shift.reopen`, `cash.variance.approve`, `inventory.conflict.resolve`.

**So nothing is being "gated" — authorisation is absent almost everywhere, including in
`venue-pos`**, which this report clears for Monday on 12 guards across 40 screens. *"The only app
whose guards resolve"* means *"the only app with any guards at all."* An earlier draft had this
backwards.

**This resizes the fix.** It is not reconciling 167 keys against 44; it is **authoring
authorisation for 2,415 screens that express none**. That is weeks of work, not a decision —
though the decision still has to come first.

**Recommended fix:** `roles-by-app.yaml` (derived, regenerated 21 September) already crosses every
app against the permissions its operations declare, tiered read/operate/configure, and states the
same zero-overlap itself. **The evidence table for this decision is already written** — what is
missing is the decision and then the authoring.

---

## 8 — Domain clearance (backend)

Gates run: **D1** contract well-formed · **D2** persistence resolves · **D3** permissions ·
**D5** operations reach a surface. D4 (lifecycle), D6 (write-only tables), D7 (principles) and
D8 (conflicts) are **not yet run** — see §13.

Ranked by unreached share, which is the discriminator that survived.

| Verdict | Domains |
|---|---|
| **Reach is not the blocker** (≤20% unreached) | `maintenance` 2% · `access` 3% · `inventory` 3% · `public-api` 4% · `venue-map` 8% · `platform-ops` 15% · `promotions` 17% · `orders` 18% · `catalogue` 19% · `fnb` 20% |
| **A third or more strands** | `finance` 23% · `queue` 23% · `approvals` 24% · `ai` 32% · `retail` 32% · `marketing-crm` 32% · `identity` 33% · `subscription` 33% · `tenancy` 38% · `white-label` 40% · `reporting` 58% |
| **Mostly or wholly unreached** | `assets` 65% · `workforce` 69% · `cross-region` 77% · `seating` 81% · `resources` 81% · `games` 82% · `wallet` 90% · `accreditation` 96% · **`payments` 100% (39/39)** · **`rental` 100% (43/43)** |

**`payments` at 100% unreached is not a gap, and an earlier draft of this report was wrong to
call it one.** All 39 operations in `contracts/satellite/payments.yaml` are administration —
`setDunningPolicy`, `setPaymentRoutingRules`, `setMerchantAccount`, `listPaymentTerminals`,
`setReconciliationMatchingRules`. **Every tender operation lives in `contracts/spine/orders.yaml`**
— `createPayment`, `capturePayment`, `voidPayment`, `createRefund`, `captureStoredValue` — and
`orders` measures 18% unreached. `payments` is a merchant-admin surface whose screens sit in the
red apps, and its own `x-ticvai-consumed-by` names P09 screens. **Nothing on the POS or guest
payment path is blocked.** The question was closable by reading operation names, and this audit
parsed that exact field for Finding 3 without reading it for meaning.

**`rental` at 100% is consistent with the story** — the Rental book arrived on 11 September and
its boards are drawn twice on purpose.

**A caution on this whole table.** §8 and §9 are **not independent evidence**. Domain unreach is
largely a restatement of app unspecification: `accreditation` 96% *is* P11; `wallet`, `seating`
and `resources` are P08/P09 holding 1,343 screens with zero operations. Two gates that look like
corroboration are one measurement wearing two hats. The app × domain crossing (§13) is what would
separate them, and it was not run.

---

## 9 — App clearance (frontend)

**Specified** = `loading` + `error` + an `empty*` state (+ `offline` where the app is
offline-capable) **and at least one operation declared.**

| App | Screens | Specified | Wave 1 | W1 spec | 0 ops | <4 comp | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| **`venue-pos`** P04 P15 | 40 | **35 (87%)** | 27 | **22** | 5 | 1 | **closest** |
| **`guest`** P01 P02 P05 | 134 | **131 (97%)** | 41 | **40** | 3 | 69 | amber |
| **`venue-staff-mobile`** P06 P07 | 107 | 75 (70%) | 36 | **35** | 32 | 31 | amber |
| **`ticvai-control`** P09–P11 P14 P17 | 767 | 357 (46%) | 12 | 12 | 410 | 365 | **red** |
| **`venue-management`** P08 P12 P13 P16 | 1,379 | 446 (32%) | 60 | **60** | 933 | 775 | **red** |
| | **2,427** | **1,044 (43%)** | **176** | **169 (96%)** | 1,383 | 1,241 | |

**Every screen in the estate has `loading`, `error` and an empty state.** The four-states gate is
satisfied mechanically. **The binding constraint is operations: 1,383 screens (57%) declare
none**, and a screen with no operation is a picture.

Per-platform, the outliers:

| | | |
|---|---|---|
| **P17 TICVAI Sign-up** | **0 of 24 specified, 0 components bound, no screen declares an operation** | newest platform, entirely unwired |
| **P16 Venue Analytics** | 10 of 69 specified; **204 data-bearing components, 16 bound** | charts with no data behind them |
| **P08 Venue Management** | 352 of 1,182 (29%); 620 of 1,471 data-bearing components bound | 49% of the whole estate |
| **P07 Venue Scanner · P14 · P15 · P01** | **100%** | the scanner remains the cleanest surface in the package |

**`build-order.md` must not be cited.** It is dated 17 August, counts 347 screens against today's
2,427, names ten apps against today's five, and reports `guest-web` at 34% specified where the
current estate measures **97%**. It is wrong in the optimistic direction on structure and the
pessimistic direction on readiness.

**Zero screens are built.** `implementation.status` is `notStarted` on all 2,427.

**Two criteria that look like signal and are not.** `route:` is present on **all 2,427 screens**,
including all 1,182 in P08 — so "every screen is routed" distinguishes nothing and should not be
read as readiness. Likewise `loading`/`error`/`empty*` are present estate-wide. **The only
discriminating fields in this table are the operation count and the component count.**

*(Two unrelated 933s appear in this report — 933 `venue-management` screens with zero operations
here, and 933 `none — <reason>` persistence values in §11. They were produced by separate scripts
and are a coincidence, flagged so it does not read as a copy error.)*

---

## 10 — What can start, and what cannot

**Can start now:**

1. **`venue-pos`** — 87% specified and P04's 30 screens are the client-approved locked build.
   **Unblocked: the `payments` concern in an earlier draft was wrong (§8).** Note the screen count
   is disputed — this report measures 40, `frontend/venue-pos.yaml` says 10 (§11).
2. **`guest` (134 screens)** — 97% specified, 40 of 41 Wave-1 screens ready. Its 69 thin screens
   are a design problem, not a build blocker.
3. **`venue-scanner` / P07 (11 screens, 100% specified)** — one contract, one table set,
   offline-mandatory, one flow with eight branches. **It is the smallest surface that exercises
   the whole chain**: contract → schema → DDL → screen → flow → offline sync. As a first slice its
   value is not the feature; it is that **nothing in this package has ever been falsified by
   running.** 2,068 operations, 621 tables and 2,427 screens have produced zero running servers
   and zero rendered screens. A fortnight on P07 settles whether the method produces code, which
   no further design pass can.

**On "scope by wave, not by app" — weaker than an earlier draft claimed.** The arithmetic holds
(169 of 176), but Wave 1 spans seven platforms, and a platform is a deployable. That is seven app
skeletons, seven pipelines and seven auth integrations before one screen renders — and §7 says
2,415 screens express no authorisation at all. **Scope by wave is a scheduling answer to a
readiness question.** It remains the right way to *sequence* work inside an app; it is the wrong
way to choose the first slice.

**A caveat that applies to every row above.** "Specified" means the YAML keys are present —
`loading`, `error`, an `empty*` state, one `operationId`. It does not mean a screen can be built,
and §1 says this method does not read English. **Every readiness number here is a presence check
inside a closed corpus that has never been tested against anything outside itself.**

**Cannot start, and the reason is not ours:** Device Management (60 requirements, **no contract
file at all**), Developer & API (94), Accreditation (58) — workshops not held. Accreditation
carries a sting: the portal can wait, but **accreditation validation appears on the Wave-1
scanner**, so the credential kind it issues cannot.

**Cannot start, and the reason is ours:** anything needing a non-POS permission (§7); **P17**,
which is 24 screens with nothing behind any of them; **P16**, whose analytics surface is 204
data-bearing components against 16 bindings.

---

## 11 — Structural, and not any one module's

- **Three DDL generations coexist at HEAD**, not two as an earlier draft said:
  `backend/tenant/*.sql` (621 tables), `src/Ticvai.Migrations/Scripts/V0001__baseline.sql`
  (1 script, 4 tables), and **`repos/ticvai-backend/src/Ticvai.Migrations/Scripts/` (6 Flyway
  scripts** — `V0001__baseline`, `V0001a__pii`, `V0002__identity`, `V0003__tenancy`,
  `V0003a__scope-typing`, `V0003b__guest-facing`). `backend/README.md` documents this exact
  failure mode as a past incident — *"thirty-three tables existed in both… 632 foreign keys went
  with them"* — and says *"If you hold an older series, delete it."* **`V000N__*.sql` sorts after
  `010-*.sql` and silently wins.** Live risk; decide and delete two.

- **No stack has been chosen, and two are half-built.** `services/` holds **16 FastAPI skeletons**
  (~27k lines of Python); `repos/ticvai-backend/` holds **13 `.csproj` .NET projects**
  (`Ticvai.Api`, `Ticvai.ControlPlane`, `Ticvai.Modules.*`). These are not a prototype and its
  successor — they are two live answers to the same question, and the DDL generations above line
  up with them. **Nothing in the package records which one the build uses.** This is not named in
  any ADR reviewed here and it precedes every other decision in §12.

- **17 services in the map, 16 on disk.** `handoff/service-decomposition.json` names seventeen;
  `services/` scaffolds sixteen. The missing one is **`WalletService`** — and `wallet` is not a
  stub domain: 50 operations, 25 tables in `backend/tenant/010-wallet.sql`, an LLD at
  `diagrams/lld/contracts/wallet.yaml`, and a place on five platform diagrams (P01, P02, P04, P08,
  P09). **It also scores 90% unreached (§8).** A domain designed to completion, placed on five
  platforms, and then given no service and almost no screens.

- **A third screen-count taxonomy, and the manifests are as stale as `build-order.md`.**
  `screens/P*.yaml` holds 2,427; the 13 `frontend/*.yaml` manifests hold **376** between them
  (`venue-pos.yaml` says `screenCount: 10` against this report's 40); `repos/ticvai-frontend/apps/`
  holds 6 apps against the package's 5. The manifests are marked derived. **A team's first
  question on Monday is which count is real, and nothing in the package answers it.**
- **`x-ticvai-persistence` has no closed vocabulary.** Four grammars in one field: a table,
  `a + b`, `none — <reason>` (933 of them), and prose paragraphs carrying markdown emphasis. It
  resolves correctly today (§4) and it violates the package's own rule that *a vocabulary with no
  written definition drifts*. It cost this audit one wrong result before it was caught.
- **Four analyses produce no artefact** — RFP coverage, spec coverage, contract audit and screen
  estate all write only behind a `--write` flag `refresh.sh` never passes. Their findings exist
  as one `tail -1` line in a terminal that has scrolled.
- **Three copies of the requirements matrix** with no statement of which is canonical.

---

## 12 — Decisions, in this order

Each names an owner-shaped action, not a topic. Items 1–3 are days; 4–5 are weeks.

1. **Pick the stack.** FastAPI (`services/`, 16 skeletons) or .NET (`repos/ticvai-backend/`,
   13 projects). Everything below is unschedulable until this is answered, and the three DDL
   generations resolve with it. **Day one.** (§11)
2. **Commit the checker-loop fix and test it against a known-bad package.** `run-checks.py` is
   written and uncommitted; the eight P11 references are the test that proves it gates. Until it
   lands, no green claim about this package is supported. **Day one.** (§3, §5)
3. **Pick one screen-count taxonomy and regenerate the rest.** 2,427 vs 376 vs 6 apps. A team
   cannot be staffed against three numbers. **Day two.** (§11)
4. **Build P07 Venue Scanner end to end** — 11 screens, one contract, offline-mandatory. Not for the
   feature: to falsify the method. **A fortnight, and it reprices everything else here.** (§10)
5. **Decide the permission model, then author it.** The vocabulary decision is small; authoring
   authorisation for 2,415 screens that declare none is not. `roles-by-app.yaml` already holds the
   evidence table. **Let P07 and P04 define the mapping before authoring the rest.** (§7)
6. **Stop `x-ticvai-consumed-by` measuring history** — derive it destructively or drop it. The
   wider point is that **every additive-only derivation in this package is monotonically
   optimistic**; four were checked and the rest inherit the shape. (§6)
7. **Give `WalletService` a service or a reason** — 50 operations, 25 tables, five platform
   diagrams, no skeleton, 90% unreached. (§11)
8. **Rename four operations and write four** for P11. (§5)

**Dropped from an earlier draft:** *"answer the payments question"* (it is answered — §8) and
*"scope the first slice by wave"* (weaker than claimed — §10).

---

## 13 — What this audit has not yet run

Named so the report cannot be read as complete.

**Domain gates not run:** D4 lifecycle (status enums with no state model — `status.json` implies
a gap of 51 against a denominator this audit did not reproduce), D6 write-only tables (the
24 August finding of 21, at 621-table scale), D7 principle conformance (money scale,
preview-computes-never-mutates, approve→gateway→cancel, degrade-never-stop, PII as reference),
D8 open conflicts per domain.

**App gates not run:** A3 scaffolding labels (1,650 of 14,488 component labels measured, not yet
attributed per app), A6 flow quality (the 192 derived flows carry `operations: []` and no
branches), A7 guard resolution, A8 the offline claim (the 24 August finding that
`x-ticvai-offline-capable` means two different things), A9 design fidelity.

**Not run at all:** the app × domain crossing, which is what turns §8 and §9 into one answer.

*No `tools/*.py` was executed for this audit. Scripts written for it are disposable; every number
above is reproducible from the source layers at `87a159c`.*
