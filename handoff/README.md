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
