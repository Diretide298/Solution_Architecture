# Handoff

Everything a new person needs, and the answers to the questions they will ask second.

| | |
|---|---|
| `TICVAI_Schema_Reference.xlsx` | **230 tables, 2,026 columns, eight sheets.** Modules with a rationale, relationships, where-used |
| **`services-and-procedures.md`** | 22 services, ten stored procedures, and why only ten |
| **`screen-index.json`** | Every screen joined to its board, operations, service, tables and procedure |
| **`api-data-lineage.json`** | Every operation against its tables, service and procedure — machine-readable |
| `storage-design.md` | The 30% of a migration that does not derive from the contracts |
| `page-inventory.md` | All 347 screens, every one defined |
| `platform-deployment.md` | Twelve platforms, where each runs and how it ships |
| `screen-contract-linkage.md` | Which operations reach a screen, and the 499 that do not |
| `requirements-coverage.md` | 2,842 of 3,184 covered, and where the rest sits |
| `artefact-audit.md` | Fifteen artefact classes, four closed |
| `integration-register.md` | 35 named integrations tested against 642 operations |
| `relationships.csv` | 406 table relationships with an edge kind |
| `tooltips.json` | 340 hover entries for the visualizer |
| `deployment-models.md` | Shared, dedicated, additional region, on-premise |
| `schema-viewer-notes.md` | Why clicking a catalogue table lands in platform |
| `api-list.md` · `schema.md` | The operation and table indexes |
| `migrations-README.md` | Why no SQL exists, and what resumes it |

## The two to read first

**The workbook** if you are building anything that stores data. **`platform-deployment.md`**
if you are building anything a person looks at — it carries the definition-depth table, which
is the difference between 347 screens defined and 27 specified.
