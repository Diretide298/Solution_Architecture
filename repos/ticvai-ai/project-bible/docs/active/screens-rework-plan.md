# Screens — the rework, and why

**18 August 2026.** Chinmay: *"the boards are real stupid, they are not built how an actual
frontend or UX would build."*

**That is right, and the numbers say why.** This is the measurement, the diagnosis and the order of
work.

---

## 1. What the audit found

377 screens across 12 platforms. Every one has a purpose, states, navigation, a layout and an
implementation path — **the record is structurally complete, and most of what fills it was
generated.**

| | of 377 | |
|---|---:|---|
| No accessibility note | **375** | The field exists on 2 screens |
| Navigation marked `inferred` | **355** | `entryFrom` and `exitTo` were guessed, not designed |
| Layout has 0 or 1 components | **225** | `GST-021 Interactive Map` has one component: `scanTarget` |
| States copied from a pattern | **172** | Their own notes say *"not individually considered"* |
| Purpose derived from the screen name | **138** | Their own notes say *"not from a requirement"* |
| `module: TODO` | **124** | |
| Carries an unresolved open question | 74 | |

**50 screens share the loading state `"Content loads"`. 47 share `"List skeleton; the count renders
first"`.** Three strings cover a third of the estate.

**The package has been honest about this all along** — each generated field carries a note saying
so. Nobody hid it; it was never revisited.

---

## 2. The diagnosis

**The screen model was built to satisfy the contract, not to describe an interface.**

It answers *which operations does this screen call, which platform builds it, which wave ships it* —
and those are the right questions for traceability. **They are not the questions a designer asks**,
and the fields that would answer those questions exist and are empty.

Three things are missing rather than wrong:

**Composition.** `layout.regions[].components[].kind` is one enum value per component. A designer
needs hierarchy — what is primary, what is secondary, what is progressive disclosure — and
`{kind: scanTarget}` on a map screen is not a layout, it is a placeholder that passed a checker.

**Interaction.** States are per screen: loading, empty, error. **Real interfaces have states per
component** — a list loading while a filter is disabled while a save button spins. And the three
that exist are the wrong three: **`empty` conflates "no data yet", "no results for this filter" and
"you do not have permission to see this"**, which are three different screens.

**Content.** No screen says what a field is called, what its validation message reads, or what the
empty state actually tells a person to do. **`"Nothing here yet, with what to do about it"` does not
say what to do about it.**

---

## 3. What not to do

**Do not redesign 377 screens.** At any honest rate that is weeks, and most of it would be
redesigning screens nobody has questioned.

**Do not start from the boards.** They are the visible symptom. Rebuilding them before the model
underneath can express a design means drawing twice.

**Do not add fields nobody fills.** `accessibility` exists on 375 screens as an absence — a field
added and never populated is worse than no field, because it reads as a considered blank.

---

## 4. The order

### Phase 1 — Fix the model (small, and everything depends on it)

**Split `empty` into three.** `emptyFirstRun`, `emptyNoResults`, `emptyNoAccess`. They are different
screens with different copy and different actions, and one field cannot hold them.

**Add per-component state.** A component may be loading, disabled, readonly or in error
independently of its screen.

**Add `contentSpec`** — field labels, validation messages, the empty-state call to action. **The
copy is a deliverable and it is currently nowhere.**

**Add `density` and `breakpoint` behaviour.** A back-office table and a kiosk button grid are not the
same screen at two widths.

**Make `navigation.inferred` fail a checker after a date.** 355 inferred routes is a navigation
model nobody designed; marking them was honest, leaving them is not.

### Phase 2 — Design the 40 that matter

**Not 377. Forty.** Chosen by three tests, and a screen qualifying on any one is in:

- **A guest sees it.** 109 guest-facing screens; the venue is judged on these.
- **It is in Wave 1.** Anything shipping first.
- **It carries money or a legal act.** Checkout, refund, waiver, consent, gate.

**Each gets a real composition, real states, real copy, and a drawn board.** The other 337 keep the
generated record and are marked as such — **a screen honestly labelled generated is more useful than
one that looks designed and is not.**

### Phase 3 — The boards

**Only after Phase 2.** A board is a rendering of a design; there is nothing to render yet.

And the boards need a different tool. **A `.dc.html` file per platform is a document, and a design
system is a component library** — the same button drawn 377 times is 377 buttons.

### Phase 4 — Reconcile with the contracts

**13 screens call no operation. 315 operations reach no screen.** Both are real and neither is
purely a screen problem:

- Sync, webhook, job and service operations legitimately have no screen — **but not 315 of them.**
- A screen calling nothing is either a navigation shell or a gap.

**This lands last because Phase 2 will change it.** Designing checkout properly will attach
operations that currently float.

---

## 5. What this does not touch

**The contracts are sound.** The API audit run alongside this found four things, all narrow: 291
write operations with no documented error response, 236 operations with no description, 10 session
operations whose caller was unstated — now `x-ticvai-self-service`, with a checker.

**Nothing in the screens work changes an operation's shape.** It changes which screens call it and
what a person sees when they do.

---

## 6. The estimate, honestly

**Phase 1 is a day.** Model change plus a migration of 377 records, mechanical.

**Phase 2 is the real work — 40 screens, and design is not a thing that goes faster when hurried.**
A day per five screens with a designer in the room is eight days, and that assumes the decisions
behind them are made.

**Phase 3 depends on tooling nobody has chosen.**

**Phase 4 is two days once Phase 2 is done**, and would be a week if attempted first.

**The thing to protect:** Phase 1 is cheap and unblocks everything, and it is the phase most likely
to be skipped because it produces nothing visible.
