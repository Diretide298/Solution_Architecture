# Wireframe & vocabulary handoff

**7 September 2026.** Everything from the pattern-board audit, the Phase 4 vocabulary pass and
Phase 1 drawing, in one file. Written to be committed to `atlas/ticvai/` alongside
`conflict-status.md`.

Boards live in the Omelette project *Index board for wireframes*. Nothing in this file has been
applied to the YAMLs — the edits in §2 are the outstanding work.

---

## 1 · Where the drawing stands

**Twenty frames, and every pattern in the package now has one.** Phase 1 is closed.

| Board | Frames | Covers |
|---|---|---|
| `Pattern Boards.dc.html` | 8 | 629 screens across the largest patterns |
| `Queue and Resources Board.dc.html` | 7 | BO-001/002/003/005, BO-095/096/097 |
| `Stray Screens Board.dc.html` | 5 | BO-100, GST-049, GST-055, BO-060, BO-020 |
| client POS pack | 2 | POS-007, POS-009 — indexed, not redrawn |

**Not drawn:** `BO-006 Parking Configuration`, deliberately. Its own note reads *Placeholder* and
its open question asks whether parking is barrier integration, space counting, pre-booking or all
three. Those are three different screens; drawing one invents the answer the 14 August MoM will
give, and a frame is harder to argue with than a placeholder.

**Pattern count: 44 → 41.** BP-010 folds into BP-001 (§2.1); BP-023 and BP-024 dissolve once
`scanTarget` is corrected (§2.6).

---

## 2 · YAML edits outstanding

Ordered so the vocabulary lands before the screens that validate against it. Full reasoning on
`Vocabulary Corrections.dc.html`; the per-screen checklist is `notes/phase4-patch.md`.

### 2.1 — BP-010 template mislabel · 20 screens · P08

`layout.template: list` → `split`, add a `searchField`.

```
BO-074  BO-075  BO-076  BO-077  BO-089  BO-090      orders & money
BO-078  BO-079  BO-080  BO-081  BO-082  BO-083      stock & supply
BO-084  BO-085  BO-086  BO-087  BO-088              people & access rights
BO-020  BO-021  BO-045                              food & beverage
```

A list declaring a `detailPanel` is the `listDetailSplit` pattern the vocabulary already names.
BP-001 goes 314 → 334 and BP-010 ceases to exist. **The original count of seventeen was short.**
Parsing all 363 P08 screens for `template: list` carrying a `detailPanel` returns twenty: the
fourteen finance, stock and approval screens plus `BO-020 F&B Order Management`, `BO-021 Order
Search` and `BO-045 Menu Management`, which sit outside the three modules the first count looked
at. The query is one line and should be the CI check, not a hand list. Add the `searchField` rather than making
BP-001's third component optional — twelve of the seventeen list journal entries, stock movements
or inventory items with no way to find one, and an optional component in a signature is how two
patterns quietly become one name.

### 2.2 — `publishGate`, a new component

Seven publish gates were filed with eleven read-only audit trails because both declare
`searchField · timeline`. Nothing in the vocabulary carries consequence.

```yaml
- kind: publishGate
  description: >
    Making a draft live, with what it will affect named before it happens.
  states: [draft, validating, blocked, publishable, publishing, published, overridden]
  requiredWhen: the screen calls an operation that publishes, deploys or activates
  notes: >
    `blocked` names what is wrong and what to do — a disabled Publish with no reason is the
    state operators escalate. `overridden` is a publish that went past a warning; it is
    recorded, because the person who authorised it is the whole value of the record.
    Saving is not publishing. A gate that shares its button with save will be pressed by
    somebody who meant to save.
```

**A component, not a template.** BO-094 Map Editor is a canvas that publishes and BO-153 is a
dashboard that publishes; a template can only be one of those.

**Scope, measured 8 September** — full working in `notes/ops-review-2026-09-08.md` §5. The
`requiredWhen` as worded fires on **45 screens**, not eight. 34 are real gates and none of them
declares the component today. The other 11 are a naming collision: `releaseInventoryHold`,
`releaseSeatHold`, `releaseSeatBlock`, `releaseStoredValue`, `releaseCustomDomain`,
`releaseChannelAllocation`, `releaseProductionPlan` — `release` there means *let go of a hold*,
which is the opposite of publishing.

**And six of the seven screens named below declare no publish operation at all.** BO-173, BO-193,
BO-213, BO-223, BO-343 and ADM-227 declare a single `list…`; only BO-153 declares
`publishTopologyValidation`. All seven are BP-006 screens, so **the publish list was read off
their titles** — the same evidence §3's first CI check exists to reject. Either those six publish
and are missing an operation, which is a contract gap like BO-233 and CMS-033, or they do not and
their titles are wrong.

**Decision, recommended:**

1. Reword `requiredWhen` to key off the declaration, not the subject — *"the screen declares an
   operation that publishes, deploys, promotes or activates"* — and exclude `release*`, or rename
   the eleven hold-releasing operations.
2. **Ship it warning.** Enforcing fails 34 undeclared screens on day one and rejects six of the
   seven this patch adds it to.
3. Declare it on **`BO-153` and `BO-094` only** — the two screens with a real publish operation.
   Hold BO-173, BO-193, BO-213, BO-223, BO-343, ADM-227 pending re-signature.
4. Flip to enforcing once the 34 are declared and the six resolved.

### 2.3 — `emptyNoEvents`, a new screen state

All eleven audit trails declare `emptyFirstRun` reading *"the action is to create the first entry"*.
Nobody hand-writes the first row of an immutable audit log, and on `CMS-058 Compliance Evidence`
and `ADM-296 Resale Ownership History` that is a screen offering to author evidence.

```yaml
- key: emptyNoEvents
  required: false
  requiredWhen: the screen renders a timeline it does not write to
  description: >
    The record is complete and nothing has happened yet. No action, and saying so is the
    point: an audit trail that offers to create its first entry is offering to author
    evidence.
```

Replace `emptyFirstRun` on `BO-233` `BO-302` `BO-362` `ADM-136` `ADM-147` `ADM-275` `ADM-296`
`SUP-011` `CMS-033` `CMS-039` `CMS-058`. Name taken from the frame at `Pattern Boards#bp-006`,
which drew the state before the defect was found.

### 2.4 — Missing `template` keys · 4 screens · P08

Not `template: none` — the `layout` block opens straight into `regions` and the key is absent,
which is why these are the only three screens in 1,091 with no derived frame.

| Screen | | Also |
|---|---|---|
| BO-092 Venue Maps | `template: list` | a directory, not a canvas |
| BO-093 Map Import & Labelling | `template: form` | add `fileUpload`, `progressIndicator` |
| BO-094 Map Editor & Publish | `template: canvas` | add `publishGate` |

Filling these does not answer `CF-146`. Raise `graphFinding` separately: BO-094's notes carry two
findings — an unreachable point is a defect, and a point reachable only by steps is a map that
works until a wheelchair user opens it — with no component to declare either.

### 2.5 — BP-006 re-signature · 23 screens · 5 files

All twenty-three carry an identical generated block, captions and error string included, down to
`error: Configuration service unavailable` on `ADM-121`, which uploads a spreadsheet. **BP-006 is
not a pattern; it is the layout a generator writes when nobody wrote one.**

Five need a new signature, each taken from its one declared operation:

| Screen | Operation | Becomes |
|---|---|---|
| BO-235 Access Attribute Catalog | `listAccessAttributeCatalog` | `list` · dataTable · searchField · primaryButton |
| ADM-121 Bulk Product Creation | `createBulkProductCatalogue` | `form` · fileUpload · progressIndicator · dataTable · banner |
| ADM-240 Conditions & Decision Tables | `listConditionDecisionLogic` | `split` · dataTable · detailPanel |
| ADM-260 Product & Catalogue Assignment | `setProductCatalogue` | `split` · treeNav · multiSelect · confirmDialog |
| CMS-044 Dynamic Fields & Conditional Logic | `listDynamicFieldQuestion` | `split` · dataTable · detailPanel · selectField |

The other eighteen: seven gain `publishGate` (§2.2), eleven keep the signature and swap their
empty state (§2.3).

### 2.6 — `scanTarget` on three screens that scan nothing

`scanTarget` is *"camera viewport for barcode, QR or NFC"*. It is the most misapplied component in
the package — **five screens declare it, and only the two scanner-platform ones are plausible.**
The three P08 cases are desktop back-office screens at `compact` density: a report about scans is
not a scanner.

| Screen | | Correction |
|---|---|---|
| GST-049 Interactive Seat Selection | hand-typed, no `impliedBy` | → `seatMap`, already in the library and used by nothing |
| GST-055 Dynamic QR Ticket | hand-typed, no `impliedBy` | → `credentialDisplay`, new (§2.7) |
| BO-060 Attendance & Footfall | derived from `listScans` | remove; also remove `destructiveButton` and `confirmDialog` |
| BO-034 Scan Activity | derived | verify — a back-office report of scans has no camera |
| BO-035 Override Audit | derived | verify — same |

On both guest screens `scanTarget` is the **only** component not marked `derived: true` — the one
thing somebody typed by hand is the one that does not belong. `seatMap`'s `noGeometry` state is
exactly GST-049's hard case: a map imported from a manifest can be sold from a list but not drawn.

### 2.7 — `credentialDisplay`, a new component

A ticket a guest holds up to a gate reader is the opposite of a camera viewport — the guest is
the thing being scanned, and nothing in the library shows a credential. Needs states the
vocabulary has nowhere else: `live`, `refreshing`, `expired`, `revoked`, `notYetValid`,
`transferred`. Six screens across P02 and P05 would use it.

### 2.8 — `calendar` is not in the template enum

`BO-096 Resource Calendar` declares `template: calendar`. The enum is `list, detail, form,
dashboard, wizard, split, canvas, modal, fullscreen, board`, so the screen fails CI as written.
Either add `calendar` or retemplate to `board`.

### 2.9 — Operation residue · 3 screens · 24 operations

`BO-003` was cleaned on 24 August: fifteen order operations removed — create an order, apply a
discount, exchange lines, hold, refund — *attached by module resemblance, not by what this screen
does*. **The check was never re-run.**

| Screen | Declared | Foreign |
|---|---|---|
| BO-001 Queue Directory | 19 | 6 catalogue, incl. `createEvent`, `createPerformances` |
| BO-002 Queue Configuration | 14 | 4 catalogue + 2 seating, incl. `recommendSeats` |
| BO-005 Queue Monitor | 19 | 12 marketing-crm, incl. `launchCampaign`, `stopCampaign` |

`BO-003`'s `entryState` also still declares `orderId` from `deepLink` and a `coldEntry` about
refunded orders — residue of the removed fifteen.

### 2.10 — `offline` on a platform not marked `offlineCapable`

`BO-097 Check Out & Check In` declares an `offline` state. P08 is not flagged `offlineCapable`.
The screen is right — a poolside kiosk at the far end of a park is where connectivity goes — so
the platform flag is what needs revisiting.

---

## 2b · What parsing all 363 P08 screens showed

`P08 Assembly Board.dc.html` routes every screen to the frame it reuses, generated from the
platform file rather than from the pattern summary. Three numbers came out different from the
plan:

- **Access & Venue is 175 screens, not 114.** Orders & Money is 59, not 15.
- **The BP-010 mislabel is 20, not 17** (§2.1).
- **127 of 363 carry `statesDerived: true`** — a third of the platform's empty, error and
  no-access copy was generated from screen names and operations. Every defect on the earlier
  boards came out of that flag.

Template distribution: `split` 172 · `list` 68 · `detail` 65 · `dashboard` 50 · `form` 4 ·
`calendar` 1 · absent 3. **Half the platform is one pattern**, and 192 once the mislabels are
corrected — so P08 is assembly against `BP-001`, not 363 designs.

Only `BO-235` cannot be routed, because its re-signature (§2.5) has not landed yet.

**Operation-side re-run, 8 September** (`notes/ops-review-2026-09-08.md`). P08 declares 1,114
operations, 666 distinct, and carries **five repeated identical operation sets across 14 screens** —
the P08 counterpart of P09's cell block, and in the modules where money is counted:
BO-039/040/041/042 each declare the full thirteen-operation shift block (open, close, cash
movement, variance); BO-022/026/047 each declare the full fourteen-operation order block including
refunds and exchanges; BO-029/059/061 each declare the nine report operations. Four screens can
each close a shift. Not recorded in any earlier note.

## 3 · Two CI checks worth adding

Both would have caught most of the above before any drawing.

**A screen whose only operation is `list…` cannot claim a verb in its title.** `BO-233 Shift
Handover` declares only `listShiftHandoverSummary`; `CMS-033 Withdrawal Management` declares only
`listConsentEvidenceWithdrawal`. The screens their titles promise cannot be built from what they
declare — missing operations, not layout defects. Raise against the contracts.

**A layout nobody authored should fail, not default.** Twenty-three screens got the same stamped
`dashboard · timeline · searchField` and the same generator wrote the other 793. Re-signaturing
these does not stop the next unsigned screen becoming a dashboard with a timeline on it.

**Both checks are now sized** (`notes/ops-review-2026-09-08.md` §4). **360 of 1,091 screens declare
exactly one operation, and it is `list` + the screen's own title camel-cased** — P09 55%, P08 38%,
P10 37%, P13 35%, P12 29%, and **zero on the other ten platforms**. The stamp is a property of five
files, not of the package, so check one can ship *enforcing* on P01, P02, P04–P07, P11, P14–P16
today and warning on the five until re-signature. A check that can only warn everywhere is a check
nobody fixes.

A caution on method: the operation names are the screen titles camel-cased with the joining words
dropped — `listShiftHandoverSummary`, `listConsentEvidenceWithdrawal`, `listChannelLogTransaction`.
**The operations came off the same titles as the layouts, so checking one against the other proves
nothing.** Two derived artefacts agreeing is not corroboration.

---

## 4 · Findings that are decisions, not defects

**The queue vendor question is one screen, not four.** `ADR-0012` is adaptor-first: a named vendor
is a driver behind a stable inbound shape, and *vendor poll* is one of seven sources in BO-003's
select. `CF-33` and `CF-33a` therefore cannot touch BO-001, BO-002 or BO-003. **`CF-33a` decides
whether `BO-005 Queue Monitor` exists at all** — and that is the screen whose declaration is 63%
campaign management.

**Resource management: five screens are missing, and every one is already referenced.** `CF-125`
says 47 requirements need a bounded context the platform does not have, and BO-095/096/097 are the
whole surface. Named with what references them:

1. **Resource Types & Deposit Policy** — the `Kind` filter on BO-095 and every deposit figure on BO-097 read from a taxonomy no screen creates.
2. **Availability Rules** — setup/teardown durations, opening hours, blackout dates. Three of the five bands on BO-096 render from rules nothing sets.
3. **Maintenance & Damage** — BO-097 routes damage *straight to maintenance* and BO-095 shows *under repair* with a reason; nothing puts a resource in that state or takes it out.
4. **Damage Assessment & Deposit Capture** — the deposit is held on check-out and released on a clean check-in. Nothing decides to charge it.
5. **Waitlist & Reassignment** — a cabana goes under repair with two bookings on it; BO-096 shows the conflict and nothing moves those guests.

`CF-149` records that the register called this a client decision while the position note called it
ours. Unresolved — the five are named so the decision can be taken on evidence rather than on a
count of requirements.

**BO-020 overlaps P15 Kitchen Display.** BO-020 declares `listKitchenTickets`,
`setKitchenTicketStatus` and `prioritiseKitchenTicket` — what the Kitchen Display exists to do,
in a different platform, with its own board drawn. Neither references the other. A back office
that advances tickets and a kitchen screen that advances tickets will disagree.

**`confirmDialog` and `modal` were used zero times across 492 screens** while `destructiveButton`
was used 39 times and its own entry reads *always requires confirmation*. Fixed on BO-060 on 31
August; the other 39 are still unpaired.

**BO-100 Venue Home is the entry point, and it is the one stray with no defect.** Until 20 August
the declared entry to the back office was BO-001 Queue Directory, which is why 93 screens were
unreachable. Two operations, four tiles, a `partial` state, and an `emptyNoAccess` that hides
sections rather than greying them out.

---

## 5 · One sentence on all of it

A generator applied a small vocabulary faithfully to 816 screens, and every failure has the same
shape: a component derived from an operation that happened to be attached, a state derived from a
screen name, a permission sentence derived from a module nobody checked. The drawing found them
because **a frame has to decide what a component is for, and the YAML never had to.**
