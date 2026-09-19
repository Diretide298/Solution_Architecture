# P09 · Commercial, regenerated — 9 September 2026

**Phase C of the screen regeneration.** 230 screens, the largest single `BP-001` group in the
package, and the case the plan chose because *"if it works there it works everywhere."*

The headline is not that the screens were rewritten. It is what the rewrite found: **the
specification for all 230 of them was parsed on 3 September and never reached them.**

---

## 1 · The finding

`sources/workshop/pack.json` has held, since 3 September, the eleven columns `ADM-145 Promotion
Approval Inbox` needs — Promotion, Request type, Requested by, Requested date, Discount exposure,
Revenue impact estimate, Margin impact, Campaign budget, Risk level, Requested activation date,
Current approval level — and the five decisions a reviewer can take: Approve, Reject, Return for
Change, Request Information, Delegate.

**The screen said `searchField: "Find a record"`.**

Across the module that is **9,474 usable bullets, a median of 36 per screen, against three declared
components**. Nothing was missing. Nothing needed inventing. There was a join nobody had written.

---

## 2 · The pack has a grammar, and reading it properly is most of the work

`ADM-048` is representative:

| Section | Contents | What it is |
|---|---|---|
| `§Display` | Total Price Lists, Active Price Lists, Draft Price Lists … | the metric row |
| `§Each price list should show` | Price List ID, Name, Code, Type, Currency … | the table columns |
| `§Status` | Draft / Configured / Validated / Active / Inactive / Expired | the lifecycle enum |
| `§Filter by` | Venue, Brand, Market, Country, Currency … | the filters |
| `§Quick Actions` | Create, Duplicate, Open, Compare, Validate, Export, Archive | the buttons |
| `§Separate permissions for` | View Pricing, Create Price Lists, Modify Pricing Structure | **component permissions** |

**`Display` and `Each price list should show` are different things** — one is a count across a
population, the other is a field of one row — and the first classifier I wrote read both as
"columns" and put `totalPriceLists` in a table of price lists. Separating them is also what makes
a command centre identifiable *from evidence rather than from its name*: a screen the pack gives
both a metric directory and a per-row directory is a command centre whatever it is called.

`§Separate permissions for` is the answer to a question the package has been failing since August.
**Four components in 3,496 declare a permission**, against a schema rule saying hiding is the
default. The packs have been naming them per screen the whole time.

---

## 3 · The join is exact, and it is not corroboration

The contracts were drafted from the same pack, and every drafted property records the sentence it
came from:

```yaml
CommercialPricingCommandCenterView:
  properties:
    totalPriceLists: { type: integer, description: "Total Price Lists" }
```

So a pack bullet matches a contract property **by its own text**, normalised for case and trailing
punctuation. No similarity scoring, no threshold to tune, no silent near-miss. **871 of 1,111
data-bearing labels bind — 78%.**

**This is naming, not corroboration.** The screen and the contract descend from the same pack
sentence; their agreeing proves nothing about whether the sentence is right. What it buys is that
the frontend and the contract use one name for one field, and `check-bindings.py` now keeps them
that way. Claiming more would repeat the exact mistake this rebuild exists to undo — **two derived
artefacts agreeing is not corroboration when they share a parent.**

---

## 4 · What changed

| | before | after |
|---|---|---|
| Components | 730 | **1,450** |
| Components declaring `bindsTo` | 0 | **289** |
| Declared columns | 0 | **1,719** — 1,381 resolve to a contract field, 338 are a source label, **0 broken** |
| Components citing a source | 0 | **1,450 — every one** |
| Component permissions | 0 | 5 |
| Overlays *(each becomes its own wireframe frame)* | 0 | 15 on 11 screens |
| Recorded gaps | 0 | **199 on 112 screens** |
| Screens declaring `preloaded` | 0 | 59 |
| Mutations declaring what they invalidate | 0 | 47 |
| Screens declaring a pattern | 0 | **230** |
| Components carrying boilerplate | **609** | **0** |
| Distinct layout shapes | 8 | **109** |
| Largest identical group | **137** | **38** |

`check-screens` **PASS, 0 errors.** Package warnings fell 674 → 668.

Patterns assigned: `listDetail` 130, `configEditor` 86, `commandCentre` 13, `approvalInbox` 1.

**Every preserved field is verifiably untouched**, compared against a pre-run copy: ids, names,
modules, waves, `requiresModule`, `source`, `implementation`, `navigation`, every declared
`operationId`, and the `coldEntry` paragraphs — of which **this module has only 3**, against 417
across the package. That is itself worth noting: the 417 hand-written entry paragraphs are almost
entirely elsewhere, and the platform now called **TICVAI Web** — P09, then styled
"Commercial" — was never given them.

---

## 5 · What the rebuild found, which matters more than what it wrote

**70 screens whose pack contains nothing that can be drawn.** Their sections are purpose,
acceptance conditions and worked examples — no directory of metrics, columns or fields anywhere.
They now carry **no content region rather than an empty one**, and a gap saying so. The first run
gave them a `dataTable` and a `detailPanel` with no columns in either; that is an empty box, which
§5 of the plan says the generator must refuse to draw, and it does.

**72 screens where nothing in the pack chooses a pattern.** They fall to `listDetail` and
`patternReason` records the fallback rather than presenting a default as a decision. Being able to
count them is the entire point of the field.

**55 screens naming actions no operation performs.** `ADM-048` offers Create Price List, Duplicate,
Compare, Validate, View Dependencies, Export and Archive, and declares `listCommercialPricing`.
This is Phase 3's reconciliation seen from the screen side rather than the contract side.

**185 of the 230 declare nothing but a `list*` read.** Where the pack named no actions, the button
is taken from the screen's own mutating operation and cited to the contract instead of the pack —
and for most of these screens there is no such verb either.

**352 page-footer artefacts.** `Pag e 15 | 158TICVAI • 15` sits inside `ADM-145`'s list of approval
types, and `6 | Pag e` inside `ADM-048`'s examples, because the footer fell between two list items
and the two packs number pages in opposite orders. They are dropped **and counted** — a generator
that drops silently is one nobody can audit, and one of these reached a table header last time.

---

## 6 · Two defects the run caught in itself

**The verb test.** Reading `§Supports`, `§Allows` and `§Enables` as action directories produced
**722 distinct "actions" across 230 screens**, most of them nouns: `Event`, `B2B`, `Venue`,
`Auditor`, `Per Ticket`. The heading is not what disqualifies them — an action starts with a verb.
The verb lexicon is **read off the packs themselves**, every first word under a heading that is
literally `Actions` or `Quick Actions` across all 590 pack entries, plus the destructive and
publishing verbs added unconditionally so a missing confirmation can never be an accident of
vocabulary.

**The pattern must be chosen on labels, not on headings.** `ADM-150`'s `§Configure whether` heads
six sentences of prose; choosing `configEditor` from the heading gave it a form with no fields.
A metric directory containing no metric is not a metric directory.

---

## 7 · New check: `columns` is now validated

`check-bindings.py` reads `columns` as well as `bindsTo`. A path naming a schema or field that does
not exist now fails the build; a bare source label is legitimate and counted separately.

**A rule nothing reads is a document, not a constraint** — this package has already found that
three times in `_schema.yaml` alone, and 1,719 unvalidated schema paths would have been the fourth.
Current state: **1,381 resolve, 338 are labels awaiting a field, 0 broken.**

`patternReason` is declared in `_schema.yaml` for the same reason.

---

## 8 · What this did **not** fix

  **208 title-stamped operations remain.** The screens are specified; their operations are still
  their own names with `list` in front. That is Phase 3, and specifying the screens proper is what
  makes it answerable — not something this run could settle.

  **338 column labels bind to nothing.** Mostly the screens declaring *real* contract operations —
  `listPromotions`, `listCouponCodes` — whose domain schemas were never drafted from pack text and
  so share no description to join on. Each is a real question about whether the pack and the
  contract name the same thing differently.

  **100 screens require `marketing` and call operations from `ticketing`.** Pre-existing, unchanged,
  and confirmed unchanged: a tenant with one licence and not the other gets a broken page.

  **The wireframes are not regenerated.** That is Phase 5, and `refresh.sh` is reserved to Chinmay.

---

## 9 · The tool

`tools/generate-screens-from-pack.py --platform P09 --module Commercial [--write]`

Written pack-general rather than P09-specific, so **D can reuse it** for every other pack-sourced
module. It reports its own counters on every run — bullets available, carried, bound, dropped —
because the failure mode of a generator against rich sources is not emptiness but mis-assignment,
and a number that moves the wrong way is the only way to see it.

---

## 10 · Known defects in this run, not yet fixed

**Noted 9 September and deliberately left**, so the review folder stays a fixed target rather than
a moving one. All four are in the generator, not in the screens' source material.

**`bindsTo: Page` on the screens with real operations.** `listApprovalRequests` returns a
pagination envelope and `response_schemas()` takes the first `$ref` in the response — which is the
wrapper, not the row type. `ADM-145` therefore binds its queue to `Page` rather than to
`ApprovalRequest`. Affects the handful of screens calling real domain operations; the drafted
`*View` screens are unaffected because their response is the shape itself.

**`invalidates` names the wrong query.** `decideApprovalRequest` records
`invalidates: [listPromotions]` when it should invalidate `listApprovalRequests` — the queue it
actually changes. The code takes `op_ids[0]`, which is declaration order; it should take
`collection_op`, which is already computed two lines above for exactly this reason.

**The unserved-actions gap does not fire on multi-operation screens.** The test is
`len(op_ids) <= 1`, so `ADM-145` — which offers Return for Change, Request Information and Delegate
against a single `decideApprovalRequest` — records no gap. Three real actions with nothing behind
them, invisible.

**Detail-group notes can end mid-phrase.** `ADM-145`'s detail panel reads *"The pack's own detail
groups on this screen: Approval can be required for"*. The heading is accurate and the sentence is
not; the note should read the heading as a label rather than as prose.
