# Renames — 8 September 2026

**`release` meant two opposite things.** Seven operations used it for *give a hold back* and one
used it for *publish*, and the collision was blocking `publishGate`: a `requiredWhen` that keys off
the declared operation could not say "publishes" without either excluding `release*` by pattern or
accepting eleven false positives.

**Renaming beat excluding**, because `releaseProductionPlan` proves the word carries both senses —
`handoff/board-panel-map.json` classifies it `build`, and its own contract summary reads *"Make the
plan real."* A pattern exclusion would have had to make an exception for it, which is a rule with a
hole in the shape of the thing it is trying to catch.

## What changed

`release` → `relinquish` on the seven hold-releasing operations. One new verb, meaning exactly
*give a hold back* and nothing else:

| was | is | contract | verb |
|---|---|---|---|
| `releaseInventoryHold` | `relinquishInventoryHold` | `spine/catalogue` | DELETE |
| `releaseSeatHold` | `relinquishSeatHold` | `satellite/seating` | DELETE |
| `releaseSeatBlock` | `relinquishSeatBlock` | `satellite/seating` | DELETE |
| `releaseCustomDomain` | `relinquishCustomDomain` | `satellite/white-label` | DELETE |
| `releaseStoredValue` | `relinquishStoredValue` | `spine/orders` | POST |
| `releaseChannelAllocation` | `relinquishChannelAllocation` | `spine/catalogue` | POST |
| `releaseWalletAuthorisation` | `relinquishWalletAuthorisation` | `spine/cross-region` | POST |

**`releaseProductionPlan` is untouched.** It is the publish, and after this pass it is the only
operation in the package whose name begins `release`.

**The list was seven, not the six previously circulated.** `releaseWalletAuthorisation` was missing
from it — it is declared in `spine/cross-region.yaml`, called by no screen, and so absent from every
count taken from the screen side. It is renamed with the others: `relinquishStoredValue` and
`relinquishWalletAuthorisation` are deliberately the same shape, because `CF-126` made one lifecycle
out of six balances and **a shared mechanism with two names is six balances again in a year.**

## Scope

40 occurrences across 25 source files — `contracts/` (6), `screens/` (6), `states/` (5), `flows/`
(5), `docs/` (3). Derived artefacts were left alone and regenerate: `diagrams/`, `services/`,
`handoff/` and the `repos/*/project-bible/` mirrors.

**`docs/active/renames-26-august.md` and `docs/active/dump-audit-3-september.md` keep the old names
on purpose.** They record what was true on those dates — `renames-26-august.md` documents
`releaseLease -> releaseInventoryHold`, and rewriting that line would make the file claim a rename
that did not happen.

## What this does not fix

`check-package` fails 14 lineage errors until the derivers run — seven old names the lineage still
holds and seven new ones it does not, plus six mirrors out of sync. **All of it is derived-layer
drift, none of it structural**, and `refresh.sh` clears it.
