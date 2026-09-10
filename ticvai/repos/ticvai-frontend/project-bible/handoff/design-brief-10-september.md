# Claude Design — the whole screen estate, in one pass

**Prompt and brief, 10 September 2026.** Hand this to Claude Design as its instructions.

---

## The situation has changed since your last handoff

When you last worked on this package, the screen definitions were not worth drawing from. 337 of
them were the same three components — `searchField` *"Find a record"*, `dataTable` *"Every record
with its status"*, `detailPanel` *"The selected record"* — and **every frame you drew was richer
than the screen it depicted, 292 of 292**. You said so, and you were right.

**All 1,091 screens have been rebuilt.** Every component now names its source, most name the data
they bind to, and the popups exist.

| | before | now |
|---|---|---|
| Components | 3,496 | **7,388** |
| Components declaring `bindsTo` | 78 (and 19 of them broken) | **1,771**, none broken |
| Declared columns, as contract field paths | 0 | **12,541** — 11,843 resolve, **0 broken** |
| Components citing a source | 0 | **7,372 of 7,388** |
| Overlays (popups, drawers, sheets) | 0 | **195 across 143 screens** |
| Screens declaring a pattern | 0 | **1,091** |
| Screens declaring `preloaded` | 0 | **511** |
| Recorded gaps | 0 | **789 across 564 screens** |
| Components carrying boilerplate | 70% | 9% |

`check-screens` passes with **0 errors**.

---

## Read these four files first. They are the brief.

| File | What it is |
|---|---|
| `screens/_design-tokens.yaml` | **The design system, extracted rather than invented.** Colour by role, the 9.5–16.5px scale, three densities, five overlay sizes. Taken from your own boards *and* the client's `Park_POS_dc.html` independently — they agree, which is what makes it a system rather than a preference. |
| `screens/_patterns.yaml` | Eight patterns on named slots. A screen fills slots; it does not invent a layout. |
| `screens/_components.yaml` | 40 component kinds. Not free text. |
| `screens/P*.yaml` | The 1,091 screens. |

Then open `_review-screens/index.html` — **1,286 frames already generated** from those files by
`tools/render-screens.py`, one per screen plus one per overlay.

---

## What we want from you

**Not 1,091 hand-drawn frames.** The generator produces those, deterministically, in seconds, and
regenerates them whenever a screen changes. Competing with it is the wrong use of your time.

Four things instead, in order:

### 1 · Judge the generated boards and tell us where the derivation is wrong

Sweep `_review-screens/` and report, per platform, where a *derived* decision is a bad one. We
expect to be wrong about: which of a schema's twenty fields belong in a table, when a `listDetail`
should have been a `statusTracker`, and where a metric row is measuring the wrong thing.

**Say it as a finding against a screen id**, the way you did in your last report — the three
mis-stamps, the `provenance` collision and P04/P06 were all correct and our index was wrong on all
three. That register of judgement is the thing we cannot generate.

### 2 · The 203 screens that draw nothing

They render an explicit **"Nothing to draw"** panel. That is deliberate and it is not a bug: their
source contains a purpose, acceptance conditions and worked examples, and **nothing describing a
screen**. Filling them with a plausible layout is the single most damaging thing that could be done
to this package — it is exactly the failure being undone, and nobody downstream would be able to
tell which screens were specified and which were imagined.

**For each, tell us which of three it is:** a screen that should not exist; a screen that exists
elsewhere under another name; or a screen that needs one specific question answered before anyone
can draw it — and name the question.

### 3 · The interaction design a generator cannot do

Six things are genuinely novel and the generator has no opinion worth having:

  **The POS drawer pattern.** Confirmed at the 3 August UI/UX workshop as the primary POS
  interaction — a right-to-left slide-in for ticket detail, date/time and seat selection, *in place
  of full-page navigation*. **`drawer` is declared in `_components.yaml` and used by zero screens.**
  This is the largest single miss in the package.

  **The POS "hot function" hybrid.** Also 3 August: always-visible buttons for refund, check
  transaction, print last receipt, alongside the search-driven "magic banner". Softlabs was asked
  for the recommendation on the balance. **Nothing in the package reflects it.**

  **The graphical table map.** Distinct two-seat and four-seat tables, select a table then enter
  covers; quick-service versus fine-dining service models; bill splitting by amount, covers or
  category.

  **Seat selection.** `seatMap` appears on **one screen in 1,091**, against four confirmed ticket
  flow variants — admission (no date), dated, timed, seated.

  **The venue map, the kitchen display and the queue board.**

  **The command centre.** `_patterns.yaml` has it, and it is the only pattern composed at runtime
  from a tenant's licence — its tiles are the modules that tenant actually bought. 35 screens use
  it and the composition has never been drawn.

### 4 · Ten component kinds nothing uses

`assetTag`, `drawer`, `duplicateMatch`, `emptyState`, `livePreview`, `modal`, `paymentTerminal`,
`queuePosition`, `signaturePad`, `toast`. **A component nothing uses is either a missing screen or
a component that should not exist**, and we do not know which. `paymentTerminal` unused on a
platform with a POS is the clearest of them.

---

## How overlays work now, because it changed

**Every popup is drawn as its own frame: the screen behind it, dimmed, with the dialog over it.**
Not a separate drawing of a dialog — *the same screen*, and this is verified: all 61 overlay frames
on P08 have their underlying screen byte-identical to that screen's own base frame.

A reviewer cannot judge a flow from a list of dialog names. They need to see what the user was
looking at when they were asked, what stays visible behind the dialog, and what they lose by
cancelling.

**The frame count is derived, never estimated** — screens plus exactly the number of declared
overlays. If you think a screen needs a popup it does not declare, that is a finding on the screen,
not a drawing.

---

## Rules that are not negotiable

**Cite everything.** Every field carries `provenance` naming a frame, a pack page, a contract
schema path, a minute, or `authored`. **A field that can cite nothing does not get written.**
*"Find a record"* cited nothing and appeared 335 times.

**Never fill a gap by drawing over it.** 789 gaps are recorded across 564 screens. Each is a real
question. Making a screen look finished is not the same as finishing it.

**Do not restyle.** `_design-tokens.yaml` is the system and it came from your own work. If a token
is wrong, say which and why; do not fork it.

**Semantic colour pairs stay paired.** A tenant who recolours `danger` to their brand green has
made a destructive confirmation look like a success message. Only `accentSolid`, `surfaceRaised`
and `typography.family.ui` are white-label overridable — plus, from 3 August, a *"powered by"*
footer credit that is fixed and not client-editable, which the tokens do not yet record.

**Two derived artefacts agreeing is not corroboration when they share a parent.** Half this
package's history is that mistake.

---

## Where the content came from, so you can weigh it

| Source | Components | What it is worth |
|---|---:|---|
| Workshop packs | 3,662 | The client's own words: columns, actions, filters, permissions, per screen |
| Contracts | 2,552 | Real field names the frontend will call. Authoritative on naming, silent on which fields matter |
| Carried from the previous definitions | 1,095 | Things a person wrote and the rebuild kept |
| Your frames | 30 | P11 only, and **protected** — the contracts generator refuses to overwrite anything citing a frame |
| Nothing | 16 | Screens declaring no operation the contracts recognise |

The contract-derived columns are **every field the response schema declares, plumbing aside**. A
response says what a screen *can* show, not what it *should*. **Narrowing twenty fields to the six
that matter is the work we are asking you for**, and it is the difference between a screen a
developer can build and a screen a developer can only guess at.

---

## The one-line version

> Read `screens/_design-tokens.yaml`, `_patterns.yaml`, `_components.yaml` and the 1,091 screens in
> `screens/P*.yaml`. Open the 1,286 generated frames in `_review-screens/`. Do not redraw them —
> judge them. Report, per screen id: where a derived decision is wrong, which of the 203 "nothing
> to draw" screens should exist and what question each needs answered, and design the six
> interactions a generator cannot: the POS drawer, the hot-function hybrid, the table map, seat
> selection, the venue map and the command centre composition. Cite every field. Never fill a gap
> by drawing over it.
