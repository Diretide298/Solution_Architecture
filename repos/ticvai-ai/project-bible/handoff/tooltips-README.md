# tooltips.json

Hover content for the visualizer, keyed so a component can look itself up without knowing
where the text came from. **Generated** from the contracts, the schema reference and the ADRs —
regenerate rather than edit, or the next contract change silently contradicts it.

## Shape

    {
      "contracts":  { "catalogue":   { tier, operations, module, title, tip } },
      "modules":    { "platform":    { tables, tip } },
      "tables":     { "orders.sales_order": { columns, tip } },
      "platforms":  { "P04":         { name, short, audience, formFactor, app, screens, offline, tip } },
      "adrs":       { "0013":        { title, tip } },
      "validators": { "check-states":{ tip } },
      "artefacts":  { "storage-design": { tip } },
      "terms":      { "lease":       { tip } }
    }

Every entry has `tip`. Everything else is metadata you may want in the same hover card —
operation counts, column counts, whether a platform is offline-capable.

## Lookup keys

| Hovering | Look up | Key |
|---|---|---|
| A schema in the sidebar | `modules` | `platform`, `fnb`, `pii` |
| A table node | `tables` | `orders.sales_order` — schema-qualified |
| A contract file | `contracts` | `catalogue`, `marketing-crm` |
| A platform or app badge | `platforms` | `P04` |
| An ADR reference | `adrs` | `0013` — four digits, zero-padded |
| A validator in the status panel | `validators` | `check-states` |
| Jargon in any prose | `terms` | `lease`, `blind count`, `RLS FORCE` |

## Two things worth honouring

**Table tips say why, not what.** `platform.outbox` reads *"events written in the same
transaction as the state change, so a crash cannot leave an event unpublished for a change that
happened"* — not *"outbox table"*. The column list is already on screen; the hover should carry
what the diagram cannot.

**A missing key means no tooltip, not an empty one.** All 278 tables have one. An empty hover
card is worse than none, because it invites a second hover — and a tip reading "Derived from
fnb.Menu" is the same failure wearing text.

## Regenerating

Tooltips derive from `x-ticvai-module`, contract `info.description`, the storage reasons in the
schema reference, and ADR decision sections. When those change, regenerate — a hover card
asserting something the contract no longer says is worse than a stale document, because nobody
reads a hover card sceptically.

## Coverage

| | |
|---|---|
| Contracts | 22 |
| Schema modules | 21 |
| Tables | 230 of 230 |
| Platforms | 8 |
| ADRs | 18 |
| Validators | 8 |
| Artefacts | 9 |
| Vocabulary terms | 12 |

**328 hover entries, 50 KB.**
