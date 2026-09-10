# Regenerating the screen layer — plan

**Decision, 9 September 2026: rebuild all 1,091 screen definitions from scratch, generate the
wireframes from a design system rather than drawing them, and re-run the derivation chain.**

This document is the plan. It is long because the last generation of this layer failed quietly and
the reason it failed is the thing this plan has to design around.

---

## 1 · What is being rebuilt, and what is not

Two layers live in `screens/P*.yaml` and they are in very different condition.

### Keep — the inventory is sound

| | |
|---|---|
| Screen ids, names, modules, waves, `requiresModule` | 1,091, traceable, and the join every other artefact uses |
| `implementation` — app, route, component path | 1,091 |
| `navigation` entryFrom / exitTo | 1,091, plus 95 flows |
| Hand-written `coldEntry` paragraphs | 417 |
| Hand-written states | 690 |
| Matrix traceability | 2,647 of 3,156 requirements `CONTRACTED`, verified 9 September |

**None of that is regenerated.** It is months of real work and the workbook audit independently
confirmed the matrix side of it.

### Rebuild — the layout, binding and state layer is filler

| | Measured 9 September |
|---|---|
| Annotated components carrying one of **ten** boilerplate strings | **70%** |
| `searchField` components whose note is *"Find a record"* | **335** |
| `dataTable` components whose note is *"Every record with its status"* | **315** |
| `detailPanel` components whose note is *"The selected record"* | **315** |
| Screens that are exactly `searchField + dataTable + detailPanel` | **337** |
| Components declaring which operation fills them (`bindsTo`) | **78 of 3,496** — 2.2% |
| Components declaring a permission | **4 of 3,496** |
| Screens declaring `preloaded` | **0** |
| States written by a deriver rather than a person | **401** |
| Screens declaring exactly one operation | **636 of 1,091** |
| Screens declaring `modal` or `toast` | **0** |
| Operations in the contracts reaching no screen | **245 of 1,626** |

`ADM-145 Promotion Approval Inbox` is the whole failure in one screen. It declares
`listPromotions` and `listApprovalRequests` both `onLoad`, `decideApprovalRequest` `onAction`, and
three components annotated *"Find a record"*, *"Every record with its status"*, *"The selected
record"*. **Nothing says which call fills the table, what the columns are, where the detail panel
gets its data, or what to refetch after a decision.** A frontend developer cannot build it without
guessing, and 336 other screens guess identically.

---

## 2 · Why regenerating now is different from last time

**The first generation ran off screen titles.** That is why 577 operations are named after the
screens that consume them, why 423 screens declare a single `list*` stamped from their own name,
and why 337 screens share three components. **Two derived artefacts agreeing is not corroboration**
— the layout was derived from the title and the operation was derived from the title, and they
agreed because they had the same parent.

Four sources now exist that did not:

| Source | Size | What it gives a screen |
|---|---|---|
| **Claude Design's frames** | 292 frames, median **26 distinct labels** against 3 declared components | The real columns, actions, filters and empty states — already drawn |
| **Client packs** | 44 books; **305 frames** on 39 boards with no package screen at all | Screens nobody has specified, and the client's own layout for them |
| **`api-data-lineage.json`** | all 1,626 operations | verb, path, tables read and written, permission, scope, routing, offline, audience |
| **Contract response schemas** | 26 contracts | The actual fields a component can bind to — which makes `bindsTo` *checkable* |
| **Minutes** | 22, 60,647 words, 86 labelled decisions | Behaviour that is decided and unwritten |

**Every frame in the package is richer than the screen it depicts — 292 of 292.** The
specification has been the poor relation of the drawing this whole time.

---

## 3 · The guardrail, which comes before any generation

**Build the validation first.** If we generate 1,091 screens and only then ask whether they are
any good, we will have produced new filler at ten times the volume and no way to tell. That is
precisely how the current state arose, and it went unnoticed for weeks.

**Every generated field cites its source.** A `provenance` entry per non-trivial field naming one
of: a frame (`board#anchor`), a pack page (`<pack>, page N`), a contract schema path, a minute
(`MoM date §section`), or `authored` where a person wrote it. **A field that can cite nothing does
not get written.** This is the single rule that would have prevented the current mess: *"Find a
record"* cites nothing and would never have been generated.

**New checks in `check-screens.py`, written before the generator:**

  `bindsTo` resolves to an operation the screen declares, and the named field path exists in that
  operation's response schema. **This is the check that has never existed** and it is why 2.2%
  binding was allowed to look acceptable.

  Every data-bearing component binds. A `dataTable` with no source is not a specification.

  No two screens share a component note verbatim more than *n* times — **a boilerplate detector**,
  because 335 identical strings should have failed a build.

  Every `onAction` operation declares what it invalidates.

  A screen whose pattern declares a slot leaves no slot unfilled and unexplained.

---

## 4 · Phase 0 — the design system

**This is what replaces Claude Design, and it already exists undeclared.** Extracted 9 September
from two independent sources that turn out to agree:

| | Claude Design's boards | Client's own `Park_POS_dc.html` |
|---|---|---|
| Font | `Manrope, system-ui, sans-serif` | **the same** |
| Size scale | 9.5 · 10 · 11 · 11.5 · 12 · 12.5 · 13 px | **the same** |
| Weights | 600 · 700 · 800 | **the same** |
| Ground | `#0B1324` | `#0B1324` |
| Radii | 5 · 9 · 10 · 11 · 12 px | 8 · 9 · 10 · 12 · 16 px |

Two designers who never coordinated produced the same vocabulary, **so it is a system rather than
a preference.** Also available: `Ticvai_Design_Vision_Book_v1_1.pdf`, and the client's Employee App
and White-Label Guest App UI references.

**Deliverable: `screens/_design-tokens.yaml`** — colour roles (not raw hexes: `ground`, `surface`,
`textPrimary`, `textMuted`, `accent`, `danger`, `warning`, `success`), the type scale, spacing,
radii, elevation, and per-density overrides for `compact` / `comfortable` / `touchLarge`.

**Density is already a screen field** — 892 compact, 148 comfortable, 51 touchLarge — and it is a
hardware fact, not a taste: `touchLarge` is a screen operated with a wet or gloved finger. The
tokens must carry all three or the generator will render a POS like a back office.

---

## 5 · Phase 1 — the pattern library, built on slots

Claude Design found six patterns empirically, and `BP-001` alone covers **337 screens** as
`split` + `searchField` + `dataTable` + `detailPanel`. **Six patterns is what you get from thin
input**, not the real number. Expect 12–18 once the input is rich: list-detail workspaces separate
from approval inboxes separate from configuration editors separate from monitors.

**The structural idea is the slot.** A pattern declares named slots; a screen fills them. That is
what turns 337 duplicates into 337 configurations, and it is what lets one React component serve
all of them.

A pattern declares:

  **When to use it**, and when not to — the part that stops everything collapsing into `BP-001`.
  **Regions**, from the seven already in `_components.yaml` (`appHeader`, `sideNav`, `contentBody`,
  `actionBar`, `contextPanel`, `statusStrip`, `bottomNav`).
  **Slots** with roles: `collection`, `selection`, `filters`, `primaryAction`, `bulkActions`,
  `overlays`.
  **Required states**, including which of `emptyFirstRun` / `emptyNoResults` / `emptyNoAccess` /
  `emptyNoEvents` apply — a distinction the package already draws and mostly does not use.
  **Overlays it owns** — confirm dialogs, drawers, side panels. `modal` and `toast` are declared by
  **zero screens today**, which cannot be true of a platform with destructive actions.
  **Its fetch shape** — list→select→detail, single fetch, wizard steps, or polling.
  **Its overlay states**, each of which becomes a frame — see below.
  **Responsive and density behaviour**, from the tokens.

`contentBody` is annotated in `_components.yaml` as *"the only region most screens define"*. That
annotation is the diagnosis: 1,083 screens define one region because nothing made them think about
the others.

### An overlay is a frame, not a footnote

**Decided 9 September: every overlay renders as its own wireframe frame — the screen with that
popup open.** A spec that merely lists *"confirmDialog: Merge these two records"* tells a reviewer
nothing about the flow. A frame showing the underlying screen with the dialog over it shows what
the user was looking at when they were asked, what stays visible behind it, and what they lose by
cancelling. **That is the difference between a wireframe you can review a flow on and a wireframe
you can only count.**

The generator emits **one frame per screen plus one per overlay state**. `EMP-057 Guest Profile &
Dining History` becomes three: the profile, the profile with duplicate candidates proposed, and
the profile with the merge confirmation open — which is the sequence somebody has to see to say
whether the merge flow is right, and precisely the sequence that is invisible today.

**It is also the check on whether an overlay was specified at all.** A frame that cannot be drawn
because the spec does not say what the dialog contains is a spec with a hole in it, and the
generator fails rather than rendering an empty box. **The overlay frame count is derived, never
estimated** — it is exactly the number of overlay states the screens declare, which is zero today.

---

## 5b · Modules compose, and the command centre is the composition

**Stated 9 September: licensing a functional module brings two more with it.** A tenant who buys
F&B, Ticketing and Retail also gets **the central Command Centre for dashboards** and **AI
Analytics, Reporting and Custom Dashboards** — and the command centre shows *the modules that
tenant actually licensed*, with the boards belonging to them.

**The package has the decision and not the mechanism.**

  **ADR-0041 is titled *"a command centre is a saved dashboard"***, and 61 screens in the package
  are named as one — `BO-144 Access Control Command Center`, `EMP-051 Restaurant Service Command
  Center`, `EMP-061 Retail Inventory Command Center`. **Each is scoped to a single module.**

  `reporting.dashboard` exists with `listDashboards`, `createDashboard`, `getDashboard` and
  `updateDashboard`. **There is no `deleteDashboard`** — CF-169's open question about soft or hard
  delete where `is_shared` is true.

  **No authoring screen exists.** Searching all 1,091 names for `widget`, `saved view`, `tile` or
  `custom dashboard` returns `BO-029 Report Builder` and nothing else. **These are the screens not
  yet received**, and CF-169 already sizes them: a dashboard list separating mine from shared, an
  editor that binds a tile to a `report_definition`, a tile configuration panel, and a viewer.

  **`requiresModule` cannot express any of this.** It is an 18-value enum saying which single
  licence a screen needs — `analytics` on 20 screens, `ai` on 13 — and **nothing anywhere says
  those two are implied by owning any functional module.** A tenant with F&B and no `analytics`
  row is served no command centre, which is the opposite of what was just decided.

### What this adds to the plan

**A module bundle in the licence model.** `analytics` and `ai` become *implied* by any functional
module rather than separately bought. That is a contract change on `LicencePosition` and it needs
your sign-off, because it decides what a tenant is entitled to without buying it.

**A `commandCentre` pattern whose slots are filled by licence, not by the screen.** This is the
first pattern in the library that is *composed at runtime*: its tiles are the licensed modules'
boards, so the same screen renders differently for two tenants. Every other pattern has static
slots; this one has a slot list derived from `LicencePosition`. **Designing that first is worth
doing precisely because it is the hardest case** — if the slot model survives it, the other
patterns are straightforward.

**The 61 per-module command centres become instances, not screens.** They are one pattern with a
module parameter, which is the same 337-duplicates problem seen a second time and caught earlier.

**Four authoring screens get written** — CF-169's list, editor, tile panel and viewer — with two
decisions attached that the entry already names: the editor must surface
`dashboard.aggregate_cost` and `report_definition.estimated_cost`, because **24 tiles on a short
refresh is a performance incident nobody was warned about**; and the delete question has to be
settled before the list screen can offer the action.

---

## 6 · Phase 2 — the screen specifications

Per screen, generated from the sources in §2 and carrying provenance per §3:

  **What it does** — purpose, and the decision it exists to support.
  **Its pattern**, and only its *differences* from that pattern.
  **Slot bindings** — each slot to an operation and, for collections, to named columns as schema
  field paths. `listApprovalRequests` → columns, not "every record with its status".
  **Actions** — each with its operation, its permission, its confirmation copy where destructive,
  and **what it invalidates**.
  **Overlays** — popups, drawers, side sheets, with their trigger and their consequence text.
  **Navigation and chrome** — sidebar entries, breadcrumb, where this sits.
  **States** — the four, plus the empty variants that actually apply. **401 are currently derived**
  and must be rewritten or explicitly re-derived with provenance.
  **`entryState`** — params, `coldEntry` (keep the 417 already written), and **`preloaded`, which
  no screen declares today**. It is the difference between a detail screen that flashes a skeleton
  and one that shows the row you just tapped.
  **Permissions at component level** — 4 of 3,496 today, against a schema rule that says hiding is
  the default.

**The fetch plan is the deliverable a frontend team actually wants**: which operations load in
parallel, which wait on another's result, what each fills, cache policy, and invalidation on
mutation. That is the object React Query or RTK Query is configured from. Today the only signal is
`trigger: onLoad` on several operations at once, with no order and no dependency.

---

## 7 · Phase 3 — the API reconciliation

Specifying the screens properly is what makes this answerable, so it comes after.

  **245 operations reach no screen.** Each is then either wired, or revealed as genuinely unused
  and removed, or a missing screen.
  **577 provisional operations** whose summary is the title of the screen that consumes them. The
  citations are sound — 577 of 577 resolve to a real pack and page — but *provisional* means not
  agreed with whoever builds it, and a properly specified screen is the conversation that settles
  it.
  **636 one-operation screens** should mostly gain operations; where they do not, the screen is
  probably not a screen.
  **CF-170 Class A and C** — 11 title-only re-signatures and `ADM-115` — fall out of this naturally.

---

## 8 · Phase 4 — journeys and linking

95 flows exist. With `preloaded` populated and slot bindings declared, the navigation graph becomes
checkable rather than descriptive: a screen that requires a param must be reachable from a screen
that can supply it, and **141 screens currently have neither a param source nor an `entryFrom`**.

---

## 9 · Phase 5 — generating the wireframes

`tools/derive-wireframes.py` already generates a board per platform. It is thin because its input
is thin — it has a `TEMPLATE_SHAPE` fallback that invents two components when a screen declares
fewer than two, labelled *"implied by template"*. **With rich screens plus tokens plus patterns,
the generator produces boards at the fidelity Claude Design draws by hand.**

**It emits one frame per screen and one per overlay state**, so a reviewer sees the dialog over
the screen that raised it rather than a list of dialog names. The frame count is therefore larger
than the screen count by exactly the number of overlay states declared — a number that is **zero
today** and is one of the clearest measures of whether the regeneration actually specified the
interactions.

**Where this replaces Design, and where it does not.** For the 337 list-detail screens, generation
is strictly better: consistent, complete, regenerating on every change, and never drifting from the
spec. **For genuinely novel interaction design — the seat-map canvas, the venue map, the kitchen
display, the queue board — a person still decides the interaction**, and the generator renders it
once the pattern is written. Claiming otherwise would be the same overreach as the pattern that
put 337 screens into one shape.

---

## 10 · Phase 6 — the chain

`tools/refresh.sh`, unchanged, in its existing order:

`derive-schema` → `relationships` → `ddl` → `burst-scope` → `sizing` → `table-notes` →
`schema-roots` → `frontend` → `board-panel-map` → `diagrams` → both workbooks → `wireframes` →
`pack-boards` → `id-register` → `link-screens-contracts` → per-domain → `backlog` → `clusters` →
`sync-project-bible` → `platform` → `platform-deployment` → `audience` → `status` → `overview` →
`mirrors` → `sync-counts`.

**`screens/` is an input to this chain, not an output** — which is exactly why rebuilding it makes
everything downstream regenerate correctly, and why nothing downstream can be fixed while it stays
as it is.

**Running `refresh.sh` is reserved to Chinmay** under the package-edit protocol.

---

## 11 · Scale, and where to start

1,091 screens is not a single pass. The order that de-risks it:

**A · Tokens and the checks** — `_design-tokens.yaml` plus the `bindsTo` and boilerplate rules,
which must exist before anything is generated.

**A2 · The `commandCentre` pattern, first.** It is the only pattern composed at runtime from a
tenant's licence, it governs 61 existing screens plus the four CF-169 authoring screens, and it
carries a contract change (`analytics` and `ai` implied by any functional module) that needs
sign-off. **Doing the hardest pattern first is what stops the slot model being designed around the
easy case** — which is how six patterns came to cover 625 screens last time.

**B · Pilot on `P11 Accreditation`** — 8 screens, fully drawn by Claude Design, and its workshop
was on 7 September so the material is current. Small enough to finish, real enough to prove the
shape. **Four of its eight screens declare no operations at all**, so it also exercises the API
reconciliation.

**C · Then `P09 · Commercial`** — 137 screens, the largest single `BP-001` group, and the hardest
case for slot-based patterns. If it works there it works everywhere.

**D · Then the rest, platform by platform**, with the drawn platforms first because their frames
are the richest input.

**The honest risk** is that a generator run against thin sources reproduces the original failure at
greater volume. The provenance rule in §3 is the whole defence: **a field that cannot cite where it
came from does not get written**, and a boilerplate check fails the build when 335 components say
the same thing.
