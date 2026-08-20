# Handoff

Everything a new person needs, and the answers to the questions they will ask second.

| | |
|---|---|
| `TICVAI_Schema_Reference.xlsx` | **278 tables, 2,025 columns, nine sheets.** Modules with a rationale, relationships, where-used, data lineage |
| **`platforms-and-apps.md`** | Twelve platforms, ten apps, named by who operates them |
| **`build-order.md`** | Which apps can be built, and in what order. The gate is *specified*, not *defined* |
| **`services-and-procedures.md`** | Where each operation gets its data. 23 services, ten stored procedures |
| **`api-data-lineage.json`** | All 689 operations against their tables, service, store and procedure |
| **`screen-index.json`** | Every screen joined to its board, operations, service and tables |
| `rag-index-sources.md` | Eleven sources indexed for retrieval, and the events that invalidate them |
| `storage-design.md` | The 30% of a migration that does not derive from the contracts |
| `page-inventory.md` | All 364 screens, every one defined |
| `platform-deployment.md` | Where each platform runs and how it ships |
| `screen-contract-linkage.md` | Which operations reach a screen, and which do not |
| `requirements-coverage.md` | Coverage by domain, and where the rest sits |
| `artefact-audit.md` | Fifteen artefact classes, five closed |
| `integration-register.md` | 35 named integrations tested against the contracts |
| `relationships.csv` | Table relationships with an edge kind |
| `tooltips.json` | Hover content for the visualizer — every table, contract, platform, ADR and flow |
| `schema-viewer-notes.md` | Why clicking a catalogue table lands in platform |
| `migrations-README.md` | Why no SQL exists, and what resumes it |
| `ai-index.md` | Where every AI artefact lives — contract, ADRs, states, storage, screens, open items |
| `tooltips-README.md` | The shape of `tooltips.json` and how a viewer looks entries up |
| `schema-deriver-note.md` | A defect the deriver had, kept so it is not reintroduced |
| `schema-storage-only.md` | Tables that exist in storage and in no contract, with the reason for each |

## The three to read first

**`platforms-and-apps.md`** if you want to know who owns what.

**`build-order.md`** if you want to know what to start. Two apps clear the bar and both are
offline-mandatory, which is not a coincidence.

**The workbook** if you are building anything that stores data. The **Data lineage** sheet
answers "what breaks if I change this table" and "where does this API get its data" from the
same rows.

## Domain sets — derived, not written

`ai-index.md` was maintained by hand until 17 August and drifted four times in one day. It is now
generated:

    python3 tools/derive-domain.py ai      # closure  → handoff/domain-ai.json + domain-markers.json
    python3 tools/render-domain.py ai      # page     → handoff/ai-index.md

**Membership is derived by closure from a seed contract**, not listed. The seed is the contract's
operations; the closure follows the schemas they touch, the enums those schemas use, the state
models on those enums, the events those states publish, the tables the lineage maps them to, the
screens that call them, the flows they step through, and the documents that name them. Two reverse
hops complete it: a state model that emits an event the domain consumes, and a foreign table
holding a key into a domain table.

**That is how `ai` reaches `conversation.yaml`.** AI never names `ConversationState` — it consumes
`conversation.handedOver`, and the model that emits it is where the handover behaviour is
specified. The hand-written index named none of the six state models the closure finds outside the
contract.

**One definition drives two surfaces.** `domain-markers.json` puts a dot beside each artefact
where it already sits, so `ai.yaml` stays in Contracts and `conversation.yaml` stays under
`marketing-crm` — the artefact-kind organisation survives. `<domain>-index.md` gathers the whole
set across layers for a reader who wants the domain rather than the tree.

**It generalises.** `derive-domain.py finance` and `orders` and `access` all resolve, which is the
answer to why there is no `ai/` folder — there is no `finance/` either, and neither needs one.

## Status — two files, one shape

    python3 tools/build-status.py             → handoff/status.json
    python3 tools/build-status.py --domain ai → handoff/status-ai.json

**Both have the same schema**, so one component renders either. A platform view and a domain view
are the same question at different scopes, and giving them different shapes would mean writing the
dashboard twice.

**Every metric carries `done`, `total` and a `note` saying what the denominator is.** That is not
decoration: on 17 August a read-routing claim reported 63% coverage when the truth was 100%,
because the count was operations and the denominator should have been reads. **A percentage
without its denominator is a defect report waiting to happen.**

Some notes are more useful than the number — `State models` can exceed 100%, because the
denominator is status enums in contracts and a few models describe behaviour that no enum
expresses.

`tools/refresh.sh` regenerates everything in dependency order and runs the validators.

### What the dashboard should not do

**Do not show `design 92%` next to `build 0%` as two bars of equal weight.** They are not
comparable: the first is coverage of a specification and the second is whether anything runs. The
second is the one that decides whether the first is true.
