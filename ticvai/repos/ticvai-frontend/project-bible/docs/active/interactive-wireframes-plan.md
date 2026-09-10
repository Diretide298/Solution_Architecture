# Plan — navigable wireframes with state, for all fifteen platforms

**9 September 2026.** Written against the audit of `TICVAI POS Terminal (1) 1.html`
(`pos-prototype-audit-9-september.md`) and the package as it stands: **1,231 screens, 2,684
declared navigation edges, 199 overlays, 94 flows, 118 unique operations on P04 alone.**

---

## 0 · The thing the POS file settles

The boards in `wireframes/` answer *what is on a screen*. **Nobody has been able to answer
*what happens when you press it*** — and that is the question a frontend developer and a coding
agent both open with.

The POS file answers it, for one platform, by being a **running application in one artboard**
rather than N static frames. That is the shape. The plan is how to get the other fourteen there
without hand-writing 618 KB of JavaScript fifteen times, and how to make the answer
machine-readable so an agent gets it without executing anything.

**One sentence version:** the transitions already exist in the package as `exitTo` edges and flow
steps — they have never carried a *trigger* or a *payload*, and no renderer has ever drawn them as
links. Fix the vocabulary, then render it twice: once cheaply for all 1,231 screens, once richly for
the seven platforms somebody actually walks end to end.

---

## 1 · Seven things not in the brief

Not objections. Each one changes what gets built.

### 1.1 The transitions are already half-written, in the flows

**94 flows, 275 ordered screen pairs, each with the operations that run on the step.** `F58 — a
ticket is sold at a till` walks POS-002 → POS-003 → POS-002 → POS-005 with `getAvailability`,
`acquireInventoryHold`, `createPayment` named per step. **176 of those 275 pairs are not in any
`exitTo` list** — so the flows and the screens already disagree about what connects to what, and
nothing has ever compared them.

This is the single largest free input to the work. It is also the reason to do the vocabulary change
before any drawing.

### 1.2 `handoff/screen-index.json` is the AI-agent index, and it already exists

1,091 entries, each carrying `operations`, `services`, `stores`, `reads`, `writes`, `route`, `wave`,
`offline` and **`exits`**. This is 80 % of the metadata deliverable, built by `refresh.sh`.

**Do not build a second one.** Extend this: add `transitions`, `machine`, `overlays`, `entryState`,
`guards`, and the board anchor. One file, one generator, and every artefact stamps ids that join
back to it.

It is also **140 screens stale** — the index has 1,091 and `screens/` now has 1,231. `refresh.sh`
has not run since the September screens landed.

### 1.3 140 screens have no exit and 226 cannot be reached

| Platform | No `exitTo` | Unreachable |
|---|---|---|
| P16 Venue Analytics | **60 of 70** | 60 |
| P09 TICVAI Web | 50 | 50 |
| P08 Venue Management | 30 | 87 |
| P05, P06, P07, P13, P01 | 0 | 3–8 each |

A navigable board makes every one of these a visible dead end — which is the point, but it means the
first navigable P16 board is **86 % dead ends** unless the navigation is authored first. **Authoring
navigation is a prerequisite for three platforms, not a by-product.**

### 1.4 Six artefacts already claim to be "the POS board"

`wireframes/P04 Venue POS.dc.html` (generated) · `wireframes/claude-design/Venue POS Board.dc.html` ·
`POS Board 1/3/4/5/6.dc.html` and `POS Frontline Board 2.dc.html` (client packs) · and now the
prototype. **An agent told to "read the POS board" reads the wrong one five times out of six.**

Every platform needs a declared **canonical artefact** in its `platform:` block, and the others
demoted to `boardFrames` with a provenance. Without it the metadata is worthless: it will resolve
to a file nobody meant.

### 1.5 `derive-wireframes.py` will overwrite this work

Its skip rule is per-screen and matches `wireframes/FnB`, `wireframes/POS`, `wireframes/Retail`,
`wireframes/TICVAI Boards v2`. **A new prototype at any other path is regenerated over on the next
`refresh.sh`.** This is the same class of defect as the overlay and gap losses found last week, and
it must be closed in the same change that gives the prototype a home.

### 1.6 Each prototype invents its own seed data

The POS file carries its own `CATALOG`, `TXNS`, `GUESTS`, `TABLES`, `SEATMAPS`, `SYNC_SEED`. If P02
invents `MyOrders` separately, **an order bought on the guest app cannot be the order collected at
the till** — and the cross-device handovers (`crossesDevice` in the flows) become undemonstrable,
which is exactly what the client will ask to see.

**One shared fixture set**, keyed the way the contracts are keyed, referenced by every prototype.
Derivable from the flows: `F60 — an online order is collected at the counter` names both ends.

### 1.7 Zero `aria-*`, and the schema has an `accessibility` block nobody fills

Wireframes are where focus order and announcements get decided cheaply. `accessibility:
{focusOrder, announcements, notes}` exists in `_schema.yaml` and is essentially unpopulated. A
navigable artefact is the first artefact that *can* carry it.

---

## 2 · Phase 0 — the vocabulary *(blocks everything else)*

`screens/_schema.yaml` cannot express a trigger, a payload or a step machine. Three additive blocks.

### 2.1 `navigation.transitions[]`

`exitTo` stays — `check-screens.py`, `screen-index.json`, `board-data.js` and the reachability
check all join on it. `transitions` is the same edge with the answers attached.

```yaml
navigation:
  entryFrom: [POS-002, POS-003, POS-004]
  exitTo:    [POS-001, POS-002, POS-010, POS-021, POS-022, POS-023]
  transitions:
    - to: POS-005#receipt
      trigger: Charge                 # the words on the control
      control: primaryButton          # which component in layout.regions
      operation: createPayment        # one of this screen's own apis[]
      carries: [orderId, paymentId, tenderAmount, tenderCurrency, fxRate]
      guard: payment.capture          # permission key; absent means any principal
      onFailure: POS-005#unknown      # where a failed call lands — not states.error
      back: false                     # can they come back the way they came
      crossesDevice: false            # a handover, not a link (the 24 August rule)
      provenance: flow F58 step 8
```

**`carries` is the field the whole exercise is for.** It is what a frontend developer cannot guess
and currently has to read someone's JavaScript to find.

### 2.2 `machine` — the step state a screen holds

`states` stays as it is: it is a *rendering* vocabulary (`loading`, `empty`, `error`, `offline`,
`denied`) and it is correct. `machine` is the *process* vocabulary, and the package has never had
one.

```yaml
machine:
  key: payStage                       # the variable a developer implements
  initial: idle
  states:
    idle:       {}
    processing: { operation: createPayment,        note: Authorisation in flight }
    checking:   { operation: inquirePaymentStatus }
    unknown:    { note: "The terminal charged a card and never answered. Inquiry, never retry." }
    completed:  { terminal: true, goes: POS-005#receipt }
    failed:     { terminal: true, retryTo: idle }
  transitions:
    - { from: idle,       on: Charge,          to: processing }
    - { from: processing, on: gatewayTimeout,  to: unknown }
    - { from: unknown,    on: Check status,    to: checking }
    - { from: checking,   on: settled,         to: completed }
    - { from: checking,   on: notFound,        to: failed }
```

Six machines are already implemented in the POS file and undeclared — `payStage`, `closeStep`,
`dstep`, `reversalStage`, `netStatus`, and the top-level `screen`. **They are transcribed, not
invented.**

### 2.3 `overlays[].returns`

199 overlays across the package declare `trigger` and `body`. **None declares what closing it
does** — and a drawer that returns a seat selection to the cart is a different thing from one that
discards it.

```yaml
overlays:
  - id: held
    component: modal
    trigger: Held orders
    confirm: { label: Recall, to: POS-002, carries: [cart, cartAt], operation: recallHeldOrder }
    dismiss: { to: POS-002, carries: [] }
```

### 2.4 Enforcement, in the same change

The schema has been caught three times carrying rules nothing read (`wireframe.status`, the `id`
pattern, `layout.template`). **Every field above ships with its check or it does not ship.**
`check-screens.py` gains:

- `transitions[].to` resolves to a real screen or anchor
- `transitions[].operation` is one of the screen's own `apis[]`
- `transitions[].carries` names fields the operation's response schema actually has
- `transitions[].guard` is a permission key that exists
- `machine.transitions` reference only declared `machine.states`, and no state is unreachable
- every `exitTo` has a `transitions` entry, or the screen says in `apisNote` why not

---

## 3 · Phase 1 — the metadata spine

**One new tool, `tools/derive-navigation.py`.** Inputs: `screens/P*.yaml`, `flows/F*.yaml`,
`handoff/api-data-lineage.json`. Outputs:

1. **Seeded `transitions` blocks written back into the screen files**, for the 275 pairs the flows
   already walk — trigger and operation come from the flow step, `carries` from the operation's
   path and body parameters. Everything else is stubbed with `provenance: authored` and left for a
   person, in the package's usual style: a derived value that reads like a decision is worse than a
   blank.
2. **The 176 flow/`exitTo` disagreements**, as a report. Each is a flow walking an edge the screen
   does not declare, or the reverse.
3. **`handoff/screen-index.json` extended** with `transitions`, `machine`, `overlays`, `guards`,
   `entryState` and `board`.
4. **`handoff/navigation-graph.json`** — the whole 2,684-edge graph in one file, per platform, so an
   agent asking *"how does a cashier reach a refund"* answers it with one read.

**Also in this phase, because they are cheap and they block the render:**

- Normalise `flows[].platforms`. It holds **29 distinct values for 15 platforms** — `P04` and
  `P04 Venue POS` both appear, so anything joining flows to platforms is silently half-blind.
- Run `refresh.sh` to bring the index from 1,091 to 1,231.
- Author navigation for **P16 (60), P09 (50), P08 (30)**, or accept those boards drawing as dead ends.

---

## 4 · Phase 2 — two tiers, because 1,231 screens will not be hand-built

The brief says *"rebuild all the rest like this"*. **At the POS file's fidelity that is 393 screens
of P08 in one artboard.** It is not the right artefact for a 393-screen configuration console
either — nobody walks those end to end; they arrive at one from a menu and leave.

### Tier A — interactive prototype, one artboard per platform

The POS file's shape. A device frame, a state machine, seeded data, real permission guards.

| Platform | Screens | Why Tier A |
|---|---|---|
| **P04** Venue POS | 24 | Built. Apply the twelve corrections |
| **P05** Guest Kiosk | 17 | A single unattended journey with a failure path (F57, F75) |
| **P07** Venue Scanner | 11 | Scan → admit → offline → reconcile. Three of the eleven are failure states |
| **P15** Kitchen Display | 10 | One board, one machine (`kitchen-ticket.yaml`), no navigation to speak of |
| **P02** Guest App | 71 | The cross-device other half of P04. Needed for the handover demos |
| **P01** Guest Web | 46 | Purchase funnel — the flow the client reviews first |
| **P06** Venue Staff App | 66 | Shift, task, incident, floor plan — all machines, all offline |

**245 screens, 7 platforms.** In that order: the three small ones prove the generator and the
metadata before the two 66/71-screen builds.

### Tier B — navigable generated board, all fifteen

**Corrected 9 September, after reading both renderers.** This section originally named
`derive-wireframes.py`. That is the wrong tool — and the mistake is worth keeping, because it is the
§1.4 defect happening to me: **there are two renderers and the better one's output is the one git
throws away.**

| | `derive-wireframes.py` | `render-screens.py` |
|---|---|---|
| Writes | `wireframes/P## *.dc.html` — **tracked** | `_review-screens/*.html` — **`.gitignore`d as "review scaffolding"** |
| Frames | 1 per screen | 1 per screen **+ 1 per overlay** |
| Overlays | **no concept of one** | 199 rendered, drawer branch included |
| Components drawn | `comps[:3]` main, `comps[3:5]` side — five, where `ADM-048` declares 25 | every region, every component |
| Table headers | invented `Name / Status / Value` | the columns the screen declares, accent-coloured where they bind |
| Stamped | nothing | `data-screen-id` |
| Exits | not drawn | `<a href="#pos-005">`, **capped at 8** |

So Tier B is **`render-screens.py` promoted**, not `derive-wireframes.py` upgraded, and three of the
four changes below are already done. What remains:

1. ~~**Exits become links.**~~ Done — 93 in the P04 file. **But capped at `exits[:8]`**, and POS-002
   declares eleven, so three edges are silently invisible. Remove the cap or say why it is there.
   Still to add: the `trigger` as the link label, which needs Phase 0.
2. **State pills become state toggles.** *Not done in either renderer* — both print the state
   *names* on a line (`render-screens.py` line 670: `states_html = " · ".join(...)`). The offline
   state is the most important line in the POS and scanner definitions and it is currently a word.
3. ~~**Overlays get their own frames.**~~ Done, and the drawer branch with it — `.drw` reads
   `drawer: {width: 480px, edge: right}` from the tokens, and the three POS-002 drawers render as
   *step 1/2/3 of 3 · stays on Sell — Ticket Catalogue*.
4. **Every frame stamped.** Partly — `data-screen-id` only. Still needs `data-op`, `data-to`,
   `data-carries`, `data-guard`, `data-machine`.

**And one thing not in the original list, which now outranks all four:** decide which renderer's
output is the package. Today the tracked boards cannot draw an overlay and the untracked ones can.

### Where the two meet

Both tiers stamp the same `data-*` vocabulary and both join to `screen-index.json` by screen id.
**A platform with a Tier A prototype keeps its Tier B board** as the fallback that covers the screens
the prototype skipped — nine of them on P04 today.

---

## 5 · Order of work

| # | Phase | Output | Blocks |
|---|---|---|---|
| 0 | Vocabulary | `_schema.yaml` + `check-screens.py` | everything |
| 1 | **Pick the renderer**; canonical artefact + skip rule | `platform.canonicalBoard`; `render-screens.py` output stops being `.gitignore`d, or `derive-wireframes.py` gains overlays | §1.4, §1.5, Tier B |
| 2 | Spine | `derive-navigation.py`, extended `screen-index.json`, `navigation-graph.json` | both tiers |
| 3 | Nav backfill | P16/P09/P08 navigation authored; flow `platforms` normalised | Tier B usefulness |
| 4 | **Tier B for all 15** | navigable generated boards, 1,231 screens | — |
| 5 | P04 corrections | the twelve, C-01/02/03 first | Tier A template |
| 6 | Shared fixtures | one seed set, cross-device consistent | P02 ↔ P04 handover |
| 7 | Tier A ×6 | P15, P07, P05, then P01, P02, P06 | — |
| 8 | Checks | `check-wireframes.py`: every declared transition has a rendered link | CI |

**Phases 0–4 deliver navigable boards for every screen in the package.** Everything after that is
fidelity on seven platforms. If the work stops after phase 4, the brief's core ask — *navigation
links and state transitions, in the metadata* — is met for 1,231 screens.

---

## 6 · What "the agent has everything" means, concretely

After phase 2, an agent asked to build `POS-005` reads one object:

```
route              /payment/payment
component          apps/venue-pos/src/routes/payment/PaymentForm.tsx
operations         11, each with contract, trigger and invalidates
reads / writes     8 tables in / 10 out, including ledger.fx_rate
entryState         paymentId, saleId — both deepLink; coldEntry prose
machine            payStage: idle→processing→checking→unknown|completed|failed
transitions        6 exits, each with trigger, operation, carries, guard, onFailure
overlays           confirm/dismiss targets and payloads
states             loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline
guards             payment.capture, payment.reversal, payment.comp.approve
board              wireframes/P04 Venue POS Terminal.dc.html#POS-005
```

**Nothing in that list is new information.** All of it exists in the package today, in five files,
joined by nothing. The work is the join and the two fields — `carries` and `machine` — that were
never written down.

---

## 7 · Three decisions — **taken 9 September**

All three settled as recommended. Recorded here rather than in a minute, because they are the
premises the phases above rest on.

1. **Tier split — seven, as listed.** P04, P05, P07, P15, then P01, P02, P06. The three small
   device surfaces first, to prove the pattern before the 66- and 71-screen builds.
2. **Tables and Guests are declared on P04.** A table-service till *is* the floor plan; the
   24 August rule is about a till not opening the **back office**, which this is not. P04 gains
   roughly twelve screens and the prototype becomes contract-complete.
3. **The 140 orphans are drawn as dead ends first.** Phase 4 renders them and that becomes the
   worklist. A board showing 60 unreachable screens on P16 is the most persuasive argument for
   fixing them this package can produce, and it costs nothing extra.

**A fourth is now open, raised by Tier B above:** which renderer's output is the package. Today the
tracked boards cannot draw an overlay and the untracked ones can.

---
