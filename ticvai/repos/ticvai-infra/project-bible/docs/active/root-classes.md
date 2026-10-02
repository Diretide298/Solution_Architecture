# Root issues by class, and the guard that closes each

> **The cited copy** (2 October 2026, CHG-SEED-012). Built 2026-10-01 by the audit workspace's root-class builder from the 26 September pull audit ledger, the step log and the F6/F8 outcomes (plan item 1F, C12). The builder and the ledger are not in git; this file is the input every document cites. Rebuilding it is a change: log it, and copy the new build here.

**A class is closed when the next instance of it fails something**: a check in `ticvai/tools/` or a rule in `ticvai/docs/active/change-rules.md`. The new checks are baseline-aware. Members still present today are listed in `ticvai/handoff/audit-baseline.json`, and only a new one fails.

- **36 classes** over 293 root issues
- **19** classes lean on an existing check (3 on existing checks alone)
- **24** classes guarded by the **9 new checks** (95 rules)
- **17** classes use one of the **8 change rules**
- **16 root issues not closed** (no guard), 5 false, 272 closed
- Status of the 293: client 72, fixed 82, open 134, won't fix 5

Status comes from the ledger and the step log, latest evidence first: verdict false means won't fix; a closed step (S005-S007) means fixed, or client for a client/both root decided on our default; then the F6 outcome (S004); then S001-S003. The F8 column is the 1 October re-audit sample (gone, reduced, same, grew). *Known today* is how many members of that rule the guard still finds.

## Classes

| Class | What goes wrong | Roots | Status | Guard | Known today |
|---|---|---|---|---|---|
| A01 CONN-SUMMARY | Connector summary drops or misstates what the YAML says | 8 | fixed 8 | ticvai-connector.mjs (+ mcp-check.mjs) |  |
| A02 CONN-FILES | Connector file and table reads fail or mislead | 5 | fixed 5 | ticvai-connector.mjs (+ mcp-check.mjs) |  |
| A03 CONN-SEARCH | Connector search misses whole kinds of artefact | 5 | fixed 5 | ticvai-connector.mjs (+ mcp-check.mjs) |  |
| A04 CONN-LIVE | Connector behaviour only a live OpenProject pull shows | 3 (2 not closed) | fixed 2, open 1 | `CR-5` |  |
| A05 STARTER-APPS | Screens name apps the starter does not have, or tag them another runtime | 3 | fixed 3 | `SF-APP-MISSING`; `SF-APP-RUNTIME`; check-frontend (every app a screen names exists in frontend/) |  |
| A06 STARTER-STANDARDS | Standards describe a different codebase from the starter, or each other | 5 | fixed 5 | `CR-6`; `SF-DOC-TYPES`; `SF-DOCS-MIRROR`; `SF-GLOSSARY`; `SF-ID-RULE`; check-migrations (RLS on scoped tables, FK targets, ids uuid, money numeric) | 4 |
| A07 STARTER-GATES | A gate a ticket demands that the starter cannot run | 6 (1 not closed) | fixed 5, open 1 | `CR-5`; `SF-DONE-GATES`; `SF-EMPTY-STUB`; `SF-OUTBOX-POLICIES` | 4 |
| A08 STARTER-CLAUDE | CLAUDE.md gives no path for a ticket kind, or hides the pulled files | 2 | fixed 2 | `SF-CLAUDE-PATHS` |  |
| A09 TICKET-ACCEPTANCE | A ticket with no checkable acceptance, or Done-when that cannot hold | 6 | fixed 6 | `T-AUTH-TESTS`; `T-DONE-WHEN`; `T-MIG-DONE`; `T-ONBOARD-SOURCE`; `T-REPO-ITEMS`; `T-SETUP-REPO` | 2 |
| A10 TICKET-DRIFT | Ticket text disagrees with the package it was generated from | 10 | fixed 6, open 4 | `S-CONSUMED-MIRROR`; `T-BOILERPLATE`; `T-MIG-DONE`; `T-NONEMPTY-LABEL`; `T-PROVISIONAL`; `T-PURPOSE-CUT`; `T-READ-ROUTING`; `T-SLICE-CALLS`; `T-SPEC-SCREEN`; `T-USED-BY`; `T-WAVE` | 38 |
| A11 TICKET-SETUP | Setup and onboarding tickets name no source, repository or independent reviewer | 3 | fixed 3 | `T-ONBOARD-SOURCE`; `T-REVIEWER`; `T-SETUP-REPO` |  |
| A12 MIGRATION-PLAN | Migration tickets, MIGRATIONS.md and the DDL disagree | 4 | fixed 2, open 2 | `D-MIG-ORDER`; `D-MIG-TABLES` | 1 |
| A13 DERIVED-COUNTS | Counts typed into derived headers and records go stale | 2 | open 2 | `D-HEADER-COUNT`; check-package rule 32 (diagrams derived, not stale) |  |
| A14 TICKET-LINKS | Ticket links leave out the ADRs, state models and events it needs | 1 (1 not closed) | open 1 | **none** |  |
| A15 STORAGE-GAP | A persisted contract field or state has no column or table | 17 | client 1, fixed 1, open 15 | `ST-FIELD-NO-COLUMN` | 192 |
| A16 STORAGE-SHAPE | A table's shape is wrong for its contract: stubs, types, requiredness, enums | 5 | open 5 | `D-STUB-TABLE`; `ST-ENUM-CHECK`; `ST-OFFLINE-RECORDED-AT`; `ST-REQUIRED-MISMATCH`; `ST-TYPE-MISMATCH` | 71 |
| A17 DDL-DERIVATION | The derived DDL breaks its own conventions | 12 (1 not closed) | fixed 6, open 6 | `D-DESC-CUT`; `D-DOUBLE-KEY`; `D-FK-INDEX`; `D-FK-TARGET-NAME`; `D-JSONB-TWIN`; `D-NAMING`; `D-RUN-TOGETHER`; `D-SCOPE-LTREE`; `D-SCOPE-NOTNULL`; check-migrations (RLS on scoped tables, FK targets, ids uuid, money numeric); check-package rule 39 (scoped operations' tables carry a scope column) | 237 |
| A18 API-CONVENTIONS | An operation breaks an api-conventions or naming rule | 15 | fixed 6, open 9 | `C-NO-ADDRESS`; `C-PAGED-ORDER`; `C-REQUEST-SERVER-FIELDS`; `C-SCHEMA-PARAMETERS`; `C-SEARCH-PARAM`; `C-SUCCESS-PROBLEM`; `C-TWO-IDEMPOTENCY`; `C-UNTYPED-BODY`; `CR-1`; check-package rule 46 (Page envelope); check-package rule 47 (one route, one operation); check-package rule 48 (Idempotency-Key); check-package rule 49 (X-Consistency-Token); check-package rule 50 (path naming) | 884 |
| A19 ERRORS-AND-STATES | Refusals, wrong-state calls and error detail left undeclared | 4 | client 1, open 3 | `C-ACTION-409`; `C-ERROR-PROBLEM-TYPE`; `CR-1` | 727 |
| A20 TYPES-AND-VOCAB | One value typed, enumerated or named two ways | 13 | client 1, fixed 4, open 8 | `C-COLOUR-PATTERN`; `C-ENUM-NON-STRING`; `C-ENUM-OTHER`; `C-EVENT-NAME`; `C-FIELD-TYPE-DRIFT`; `C-ID-FORMAT`; `C-MONEY-NUMBER`; `CR-1`; check-migrations (RLS on scoped tables, FK targets, ids uuid, money numeric); check-package rule 33 (a stored currency column earns its place); check-states (models vs enums, transitions vs operations) | 194 |
| A21 STATE-MODELS | State models and operations disagree | 3 | open 3 | `C-APPEND-ONLY`; `CR-1`; check-states (models vs enums, transitions vs operations) |  |
| A22 LINEAGE | Declared reads, writes and emits do not match what the operation does | 5 | open 5 | `CR-1`; `CR-3`; check-lineage (lineage vs contracts) |  |
| A23 AUTH-SCOPE | Permission, audience or scope does not fit the caller | 13 | client 6, open 7 | `C-GUEST-INTERNAL`; `CR-1`; `S-GUEST-AUDIENCE`; `S-WORKSTATION-OP`; check-migrations (RLS on scoped tables, FK targets, ids uuid, money numeric); check-package rule 23/26 (who may call; permission in enum); check-package rule 9 (every operation declares its authentication); check-package permission-escalated rule (audit R197); check-screens guest-surface rule (staff permission on a guest screen) | 133 |
| A24 GLOSSARY | A synonym the glossary bans, or a term it does not define | 15 | client 9, open 6 | `CR-4`; `G-BANNED-NAME` | 198 |
| A25 PROSE-QUALITY | Prose that is corrupted, stale after a rename, or promises what the schema lacks | 6 | fixed 2, open 4 | `C-PROSE-SPLIT`; `CR-1`; `D-RENAME-RESIDUE`; `N-ENTRY-MIRROR`; `S-NOTES-STALE`; `S-OPENQ-STALE`; check-doc-tables (docs naming renamed tables) | 6 |
| A26 BUSINESS-RULES | Behaviour the contract leaves unspecified | 28 | client 21, open 7 | `CR-1`; audit-uncontrolled-values |  |
| A27 CLIENT-DECISIONS | A platform, vendor, law or data decision the package cannot make | 8 | client 8 | `CR-2` |  |
| A28 MISSING-OPERATION | A screen or flow needs an operation or field the contract lacks | 31 | client 7, fixed 3, open 21 | `CR-3`; `S-ASYNC-POLL`; `S-EXPORT`; `S-METRIC-NO-OP`; `S-NO-READ`; `S-UPLOAD`; audit-screenless-operations | 1619 |
| A29 JOURNEY-CONTRACT | A journey contradicts the contract or the screen it runs on | 8 | client 5, fixed 1, open 2 | `CR-1`; `CR-3`; check-flows rule 3 (a step's operations are on its screen) |  |
| A30 SCREEN-GENERATED | Generator boilerplate left on screens | 8 | fixed 5, open 3 | `S-BUTTON-FORM`; `S-DUP-REGION`; `S-ONLOAD-WRITE`; `S-OP-UNREACHED`; `S-PANEL-ENTITY`; `S-PURPOSE-TEMPLATE`; `S-SCREEN-PERMISSION`; `S-STATE-BOILERPLATE` | 8264 |
| A31 SCREEN-WRONG-OP | A screen wires an operation wrong for its platform or purpose | 15 | client 3, fixed 1, open 11 | `CR-3`; `S-CONSUMED-MIRROR`; `S-DUP-SCREEN`; `S-FIELD-BINDING`; `S-OFFLINE-CLAIM`; check-screen-redundancy; check-screens attachment warnings (audit R254); check-screens guard vocabulary (audit R278); check-screens requiresModule rule | 56 |
| A32 NAVIGATION | Navigation inferred, not designed | 3 | fixed 1, open 2 | `N-CARRIES-HELD`; `N-ENTRY-MIRROR`; `N-TWIN-OPS`; `N-TWIN-WAVE`; check-screens entry-param rule (operations needing ids the entryState lacks) | 98 |
| A33 WIREFRAMES | A screen with no wireframe, or a drawn frame nothing links | 3 | client 2, open 1 | `W-DUMP-POINTER`; `W-INCOMING-UNLINKED`; `W-NO-DESIGN` | 313 |
| A34 SCREEN-CONTEXT | A screen does not say where its context comes from or how it behaves | 2 | client 2 | `CR-1`; `CR-2`; check-session-entry (every app that reads a session creates one) |  |
| A35 ONE-OFFS | Single findings with no shared cause | 11 (11 not closed) | client 6, open 5 | **none** |  |
| A36 FALSE | Findings the verdict pass found false | 5 | won't fix 5 | **none** |  |

## Not closed

| Root | Class | Status | Why no guard |
|---|---|---|---|
| R018 | A04 CONN-LIVE | fixed | the gateway retry is in viewer/mcp/client.mjs but no test replays a 502; needs a case in viewer/mcp/mcp-check.mjs (viewer/ is outside this task) |
| R021 | A04 CONN-LIVE | fixed | the setup-ticket hint needs a live OpenProject pull; ticvai-connector.mjs reports it as not covered |
| R036 | A07 STARTER-GATES | open | offline-core has no read cache; there is no mechanical signal for a design gap in a package that does not exist yet |
| R052 | A14 TICKET-LINKS | open | ticket links are built by tools/adam-links.py and ADAM; no rule says which ADRs, states and events a ticket must link (C8/C9 work) |
| R200 | A17 DDL-DERIVATION | open | ADR-0011 makes an undeclared reference a deliberate convention, so which ones should be keys is a judgement; audit-unwired-tables style report needed |
| R073 | A35 ONE-OFFS | client | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R077 | A35 ONE-OFFS | client | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R080 | A35 ONE-OFFS | client | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R085 | A35 ONE-OFFS | open | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R110 | A35 ONE-OFFS | client | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R116 | A35 ONE-OFFS | open | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R120 | A35 ONE-OFFS | client | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R132 | A35 ONE-OFFS | client | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R136 | A35 ONE-OFFS | open | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R150 | A35 ONE-OFFS | open | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |
| R219 | A35 ONE-OFFS | open | mixed one-off findings with no shared mechanism; CR-7 makes a recurrence a new class with its own guard |

## Every root issue

### A01 CONN-SUMMARY: Connector summary drops or misstates what the YAML says

*Mechanism:* the indexer copied a whitelist of fields and flattened allOf/inline bodies.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R003 | Operation summary drops or misstates inline request/response bodies (requestBody [], nested $ref shown as t... | ours | fixed | reduced | connector |
| R006 | Derived operation platforms/consumers metadata is wrong: platforms omit the P-codes x-ticvai-consumed-by na... | ours | fixed | reduced | connector |
| R007 | adam_table summary misstates the DDL: ignores 900/920 (rls null, foreignKeys []), ltree shown as text, prec... | ours | fixed | reduced | connector |
| R008 | adam_contract schema view does not resolve allOf, so composed schemas show 0 properties | ours | fixed | reduced | connector |
| R010 | Operation summary drops path-item-level parameters | ours | fixed | reduced | connector |
| R014 | Schema/operation summaries drop enums, nullable, min/max, pattern, defaults and nested item shapes | ours | fixed | grew | connector |
| R015 | adam_screen / pulled screen JSON drops screen YAML fields (entryState, gaps, pattern, requiresModule, per-c... | ours | fixed | gone | connector |
| R020 | Operation summary / README drops security and x-ticvai extensions (auth null, permission-escalated, step-up... | ours | fixed | grew | connector |

### A02 CONN-FILES: Connector file and table reads fail or mislead

*Mechanism:* server paths, big single-line SQL files and error mapping were never exercised.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R004 | adam_table ddl.file is a root-less path (tenant/010-x.sql, no backend/ prefix) that adam_file cannot open, ... | ours | fixed | gone | connector |
| R009 | Large generated package docs cannot be navigated: adam_file has no in-file search/anchor jump and spec docs... | ours | fixed | reduced | connector |
| R011 | adam_file returns 900-foreign-keys.sql / 910-indexes.sql as a few huge lines that overflow the tool result | ours | fixed | gone | connector |
| R013 | adam_file answers non-contract paths (wireframe boards, directories, typos) with a misleading "may not read... | ours | fixed | gone | connector |
| R024 | adam_file reports a missing file as HTTP 500 exposing the server filesystem path | ours | fixed | gone | connector |

### A03 CONN-SEARCH: Connector search misses whole kinds of artefact

*Mechanism:* the search index covered screens and pages only; tokenisation was whole-string.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R005 | adam_search does not index operations, schemas, contracts or shared components although its description say... | ours | fixed | reduced | connector |
| R012 | adam_search does not index backend SQL/DDL files, migration keys or plan items (MIG-*, SETUP-*, CF-*) | ours | fixed | reduced | connector |
| R016 | one-offs (b09) | ours | fixed | gone | connector |
| R017 | adam_search cannot find permission names (no permission kind) | ours | fixed | gone | connector |
| R022 | adam_search relevance/tokenisation: multi-word queries miss, short queries flood | ours | fixed | grew | connector |

### A04 CONN-LIVE: Connector behaviour only a live OpenProject pull shows

*Mechanism:* gateway retries, next-step hints and predecessor status need a live board; the connector check skips them.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R018 | adam_pull intermittently fails with HTTP 502 on first call | ours | fixed | grew | **not closed** |
| R021 | adam_pull 'next' hint pushes adam_search/adam_link on tooling/onboarding tickets with nothing to link | ours | fixed | gone | **not closed** |
| R050 | Predecessor tickets (MIG-*, SETUP-*, SVC-*) named in Follows are not in the repo and their status is not vi... | ours | open | grew | CR-5 |

### A05 STARTER-APPS: Screens name apps the starter does not have, or tag them another runtime

*Mechanism:* the starter's app list was written by hand beside a package that derives it.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R031 | CLAUDE.md calls apps/backoffice React Native but project.json tags platform:web and screens deploy to brows... | ours | fixed | gone | SF-APP-RUNTIME |
| R037 | CLAUDE.md app table has no home for console (P09), kitchen (P15) or staff web/CMS platforms and no add-an-a... | ours | fixed | reduced | SF-APP-MISSING, frontend |
| R249 | Screen implementation.app names apps not in the starter (guest-app, guest-web, venue-pos, venue-management-... | ours | fixed | gone | SF-APP-MISSING, frontend |

### A06 STARTER-STANDARDS: Standards describe a different codebase from the starter, or each other

*Mechanism:* standards were edited in one copy; the starter code moved without them.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R025 | Starter lacks cross-cutting plumbing: ITenantContext is TenantId-only (no venue/region/workstation scope), ... | ours | fixed | reduced | SF-DOC-TYPES |
| R026 | frontend-patterns 4.4 "every mutation goes through the offline-core outbox" does not fit online-only, web o... | ours | fixed | reduced | CR-6 |
| R028 | Standards docs (backend-patterns, project-bible) describe a different codebase than the starter (Ticvai.Mod... | ours | fixed | reduced | SF-DOC-TYPES, SF-DOCS-MIRROR, CR-6 |
| R030 | Id-generation standards conflict: backend-patterns bans Guid.NewGuid for UlidGenerator while naming-and-sty... | ours | fixed | reduced | SF-ID-RULE, migrations |
| R040 | Starter ICurrentUserService breaks naming (User, bare Service suffix) | ours | fixed | gone | SF-GLOSSARY |

### A07 STARTER-GATES: A gate a ticket demands that the starter cannot run

*Mechanism:* Done-when lines name harnesses, runners, fixtures and packages the starter does not ship.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R027 | Service Done-when requires contract tests / lint and typecheck / RLS tests, but the starter has no harness,... | ours | fixed | reduced | SF-DONE-GATES |
| R029 | packages/api-client and the app shells are empty stubs (export {}); SETUP-CLIENTS has not landed | ours | fixed | grew | SF-EMPTY-STUB |
| R032 | No migration mechanism in the starter: no SQL runner, folder, baseline or CI; raw versioned SQL vs EF Core ... | ours | fixed | grew | SF-DONE-GATES |
| R034 | quality-gates reference fixture (two brands, three regions, AED/OMR) is required but not in the starter | ours | fixed | grew | SF-DONE-GATES, CR-5 |
| R035 | offline-core outbox API mismatches contracts: no lastWriterWins policy, outbox mints its own ULID with no c... | ours | fixed | reduced | SF-OUTBOX-POLICIES |
| R036 | offline-core has no read cache/settings store for "already loaded, marked with its age" offline states; web... | ours | open | grew | **not closed** |

### A08 STARTER-CLAUDE: CLAUDE.md gives no path for a ticket kind, or hides the pulled files

*Mechanism:* the working-a-ticket steps assumed one ticket kind; .adam/ is git-ignored.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R033 | CLAUDE.md "Working a ticket" assumes a contract-backed API ticket; no path for DB migration, DevOps or onbo... | ours | fixed | reduced | SF-CLAUDE-PATHS |
| R039 | Pulled package lives under git-ignored .adam/, so Grep silently finds nothing there | ours | fixed | grew | SF-CLAUDE-PATHS |

### A09 TICKET-ACCEPTANCE: A ticket with no checkable acceptance, or Done-when that cannot hold

*Mechanism:* the generator pasted one Done-when template per ticket kind.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R041 | Screen tickets carry no acceptance criteria beyond "three sub-tasks: build, connect, tests" and boilerplate... | ours | fixed | grew | T-DONE-WHEN |
| R046 | Migration Done-when is boilerplate that cannot hold: CI rollback test, restored snapshot, previous release'... | ours | fixed | reduced | T-MIG-DONE |
| R053 | Onboarding tickets: scope, variant and done state ambiguous; 'pass the connection test' has no defined pass... | ours | fixed | grew | T-ONBOARD-SOURCE, T-DONE-WHEN |
| R054 | Service Done-when demands 401/403 tests on operations with null permission, anonymous or self-scoped access | ours | fixed | grew | T-AUTH-TESTS |
| R059 | DevOps setup tickets are one-line descriptions with no acceptance criteria | ours | fixed | reduced | T-DONE-WHEN, T-SETUP-REPO |
| R069 | Backend Done-when mixes frontend/CI/fixture items (lint/typecheck, tenant fixture) | ours | fixed | reduced | T-REPO-ITEMS |

### A10 TICKET-DRIFT: Ticket text disagrees with the package it was generated from

*Mechanism:* descriptions are generated once and pushed; the package moved after.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R042 | Ticket 'Used by' / linked screens omit consumers named in x-ticvai-consumed-by | ours | fixed | reduced | T-USED-BY, S-CONSUMED-MIRROR |
| R044 | Backend ticket template says "each operation has its own sub-task" and repeats reviewers, but no sub-tasks ... | ours | fixed | reduced | T-BOILERPLATE |
| R045 | Wave disagrees between screen, journey, operation, service doc and the ticket Block A milestone | ours | fixed | grew | T-WAVE |
| R047 | Ticket title / 'In the slice' names fewer operations than the screen's Calls list | ours | fixed | reduced | T-SLICE-CALLS |
| R048 | DB migration ticket names a V-number/file that MIGRATIONS.md and table records give to another module | ours | fixed | grew | T-MIG-DONE |
| R061 | Contract/operations marked provisional or 'confirm before building' yet the ticket asks for them to be built | ours | open | reduced | T-PROVISIONAL |
| R064 | Service doc 'makes table X non-empty' copied onto update/escalate operations | ours | open | reduced | T-NONEMPTY-LABEL |
| R066 | ReportingService ticket routes reads to the primary while contract/service say replica only | ours | fixed | gone | T-READ-ROUTING |
| R067 | Ticket description and screen purpose truncated mid-word | ours | open | grew | T-PURPOSE-CUT |
| R274 | Generated frontend spec (WL.md, MOB.md, POS.md) disagrees with the screen record or contract (template, par... | ours | open | grew | T-SPEC-SCREEN |

### A11 TICKET-SETUP: Setup and onboarding tickets name no source, repository or independent reviewer

*Mechanism:* SETUP-* text was a fixed string with no repo field; the reviewer rota ignored the builder.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R001 | Onboarding tickets name adam-connector-setup.zip / setup.cmd with no location, and neither is in the repo | ours | fixed | reduced | T-ONBOARD-SOURCE |
| R002 | Ticket targets a repo, fixture or command the backend starter does not match (frontend work in backend repo... | ours | fixed | grew | T-SETUP-REPO |
| R058 | Done-when 'reviewed by this week's checker' is outside the repo and the checker is often the builder | ours | fixed | reduced | T-REVIEWER |

### A12 MIGRATION-PLAN: Migration tickets, MIGRATIONS.md and the DDL disagree

*Mechanism:* the ticket's own order and table list were computed apart from MIGRATIONS.md.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R049 | DB ticket covers a subset of a module's DDL tables; ownership of the rest unstated, table counts disagree | ours | open | reduced | D-MIG-TABLES |
| R051 | Migration ordering (Follows, 'keys into schemas created later (N) go in MIG-FOREIGN-KEYS') computed under t... | ours | fixed | reduced | D-MIG-ORDER |
| R056 | Which migration creates module schemas, enum types, the 920 RLS helpers, ltree and FK targets is unstated | ours | open | grew | D-MIG-ORDER |
| R063 | Tables carry migration 'unassigned' / migration ids inconsistent across ADAM and OpenProject | ours | fixed | grew | D-MIG-TABLES |

### A13 DERIVED-COUNTS: Counts typed into derived headers and records go stale

*Mechanism:* a count was written as text instead of computed where it is shown.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R043 | Service/module record metadata stale: 'why' operation/table counts, service tier vs operation tier, adam_mo... | ours | open | reduced | D-HEADER-COUNT, pkg-32 |
| R170 | Package derived headers/docs give contradictory table/schema/RLS counts | ours | open | grew | D-HEADER-COUNT |

### A14 TICKET-LINKS: Ticket links leave out the ADRs, state models and events it needs

*Mechanism:* the link set is operations and screens; nothing adds the rest.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R052 | Ticket links omit related artefacts: nothing linked, ADRs not listed, state models/events found only by search | ours | open | grew | **not closed** |

### A15 STORAGE-GAP: A persisted contract field or state has no column or table

*Mechanism:* x-ticvai-persistence named a table and nothing compared its fields with the DDL.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R086 | Contract request/response fields have no table column (cross-service findings) | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R099 | OrderService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R107 | VenueOpsService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R109 | DDL table columns derived from the wrong contract schema (instance vs template, request body), e.g. entitle... | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R112 | FnbService: contract fields/state have no column or table in its schema | ours | open | grew | ST-FIELD-NO-COLUMN |
| R115 | CatalogueService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R130 | MarketingService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R135 | IdentityService: contract fields/state have no column or table in its schema | both | client | grew | ST-FIELD-NO-COLUMN |
| R159 | AccessService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R172 | InventoryService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R173 | LedgerService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R179 | TenancyService: contract fields/state have no column or table in its schema | ours | open | grew | ST-FIELD-NO-COLUMN |
| R201 | AiService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R216 | PlatformService: contract fields/state have no column or table in its schema | ours | open | gone | ST-FIELD-NO-COLUMN |
| R217 | ReportingService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R218 | RetailService: contract fields/state have no column or table in its schema | ours | open | reduced | ST-FIELD-NO-COLUMN |
| R248 | WhiteLabelService: contract fields/state have no column or table in its schema | ours | fixed | same | ST-FIELD-NO-COLUMN |

### A16 STORAGE-SHAPE: A table's shape is wrong for its contract: stubs, types, requiredness, enums

*Mechanism:* derive-schema took columns from a response shape and never checked them against the fields.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R087 | Synthesised tables are stubs holding only id + one FK, lacking the columns their description promises | ours | open | reduced | D-STUB-TABLE |
| R089 | Column/field requiredness contradicts the contract or its own description (subject_id, principal_id, PK nul... | ours | open | reduced | ST-REQUIRED-MISMATCH |
| R113 | Offline-capable operations have no recorded_at/synced_at storage or client timestamp for conflict policy | ours | open | reduced | ST-OFFLINE-RECORDED-AT |
| R151 | Contract enums, uniqueness, defaults and immutability are not carried into the DDL (no CHECK/unique/DEFAULT) | ours | open | grew | ST-ENUM-CHECK |
| R227 | heightBandsCm integer[] in contract but text[] in product_eligibility_rule | ours | open | same | ST-TYPE-MISMATCH |

### A17 DDL-DERIVATION: The derived DDL breaks its own conventions

*Mechanism:* derive-ddl/derive-relationships guessed keys by name and wrote names and types mechanically.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R019 | Table column descriptions truncated mid-sentence in adam_table / pulled table files | ours | fixed | gone | D-DESC-CUT |
| R070 | Tenant-scoped tables carry no scope_path/venue_id/region_id (rls null), so 920 applies no policy and "row-l... | ours | fixed | reduced | pkg-39, migrations |
| R082 | Name-matched foreign keys / 910 convention references resolve to the wrong table (ai.index_source, fnb.deli... | ours | open | reduced | D-FK-TARGET-NAME |
| R090 | Declared foreign keys have no index; 910-indexes indexes only convention references | ours | fixed | gone | D-FK-INDEX |
| R092 | scope_path typed text (not ltree) in the DDL | ours | fixed | gone | D-SCOPE-LTREE |
| R093 | DDL column names break naming rules (bare money names, non-assertion booleans, FK without _id, reserved words) | ours | open | reduced | D-NAMING |
| R102 | Derivation adds a second key column beside the contract one for the same parent/concept | ours | open | reduced | D-DOUBLE-KEY |
| R111 | Same data modelled in two places with no source of truth (jsonb + child table, two tables, two write paths) | ours | open | grew | D-JSONB-TWIN |
| R119 | Derived DDL object names (ix_/fk_/policy/partition) break naming-and-style 6.1 | ours | open | reduced | D-NAMING |
| R180 | scope_path nullable on FORCE-RLS tables, so rows without a path are invisible | ours | fixed | reduced | D-SCOPE-NOTNULL |
| R200 | References kept as convention-only (indexed, not declared) instead of real foreign keys | ours | open | grew | **not closed** |
| R247 | Derived DDL 010-*.sql has column name and type run together | ours | fixed | gone | D-RUN-TOGETHER |

### A18 API-CONVENTIONS: An operation breaks an api-conventions or naming rule

*Mechanism:* operations were drafted from boards faster than anyone read them against the conventions.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R076 | List operations take PageSize/PageCursor but return a bare array instead of the Page envelope | ours | fixed | reduced | pkg-46 |
| R079 | Create/PUT/PATCH request bodies reuse the full resource schema: client must send server-owned id (uuid vs U... | ours | open | grew | C-REQUEST-SERVER-FIELDS |
| R088 | Request/response bodies typed as free-form objects (additionalProperties:true, object[], no schema) | ours | open | reduced | C-UNTYPED-BODY |
| R103 | PUT set/singleton semantics undefined (replace vs upsert, omitted items, collection PUT with no id) | ours | open | grew | C-NO-ADDRESS, CR-1 |
| R118 | Contract paths break URL rules (singular collections, verb actions, two roots for one resource, e.g. /kitch... | ours | open | same | pkg-50 |
| R142 | Mutating operations declare no Idempotency-Key (or one on a pure computation) | ours | fixed | reduced | pkg-48 |
| R153 | Two idempotency keys (header and body ULID) with no precedence rule | ours | open | grew | C-TWO-IDEMPOTENCY |
| R154 | List sort order / keyset cursor key not specified | ours | open | grew | C-PAGED-ORDER |
| R162 | Operation cannot address the row it acts on (no path key or identifying parameter) | ours | open | grew | C-NO-ADDRESS |
| R176 | Same method+path defined in two contracts with different bodies/permissions (conversation messages, stock-c... | ours | fixed | reduced | pkg-47 |
| R182 | List search/filter parameter semantics undefined | ours | open | grew | C-SEARCH-PARAM |
| R192 | Operations do not declare the X-Consistency-Token header api-conventions requires | ours | fixed | grew | pkg-49 |
| R198 | listAuditRecords returns untyped, unpaged free-form objects | ours | open | gone | C-UNTYPED-BODY, pkg-46 |
| R212 | Stray 'parameters: IdempotencyKey' inside component schemas | ours | fixed | gone | C-SCHEMA-PARAMETERS |
| R235 | shareEntitlement 200 response typed as Problem | ours | fixed | gone | C-SUCCESS-PROBLEM |

### A19 ERRORS-AND-STATES: Refusals, wrong-state calls and error detail left undeclared

*Mechanism:* errors were listed as bare statuses; state guards lived in prose.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R075 | Listed operation errors carry no problem type URI or error code; one status bundles several causes | ours | open | reduced | C-ERROR-PROBLEM-TYPE |
| R078 | Refusals and illegal state transitions have no declared error response, or a listed error cannot occur | ours | open | reduced | C-ACTION-409 |
| R095 | State-dependent behaviour undefined: which statuses allow an action and what a wrong-state call gets | both | client | grew | C-ACTION-409, CR-1 |
| R133 | Errors must return detail (which, candidates, reason code) the shared Problem schema has no field for | ours | open | reduced | C-ERROR-PROBLEM-TYPE |

### A20 TYPES-AND-VOCAB: One value typed, enumerated or named two ways

*Mechanism:* each schema was written on its own; nothing compared the same field across them.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R074 | Same id typed ULID in one place and uuid/text/untyped in another across contracts, tables and events | ours | open | reduced | C-ID-FORMAT, migrations |
| R084 | Money currency/scale source inconsistent (region vs venue trading currency) or unreadable by the operation | ours | open | grew | pkg-33, migrations, CR-1 |
| R104 | Fields that need a closed vocabulary are free strings / untyped object[] | ours | open | reduced | CR-1 |
| R105 | Enum/vocabulary values disagree between description, request, response, screens or duplicate enums | ours | open | reduced | states |
| R122 | Money-like values typed as JSON number or integer minor units | ours | open | gone | C-MONEY-NUMBER |
| R177 | Wire schemas use bare money field names (price, total, value) without x-ticvai-column | ours | open | grew | C-MONEY-NUMBER |
| R186 | Event names do not follow <context>.<entity>.<verb>.v<n> | ours | open | grew | C-EVENT-NAME |
| R222 | Enums use the banned value "other" | both | client | reduced | C-ENUM-OTHER |
| R237 | Queue name LocalisedText on create/read but string on updateQueue | ours | fixed | gone | C-FIELD-TYPE-DRIFT |
| R238 | setAccessPointGeofence enforcement enum contains YAML boolean false | ours | open | gone | C-ENUM-NON-STRING |
| R239 | AI ceiling behaviour: manager decides vs block enum and 429 | ours | fixed | gone | CR-1 |
| R240 | Resource kind enum includes mealPlan 'listed to be refused' | ours | fixed | gone | CR-1 |
| R246 | Theme.darkMode colours lack the hex pattern | ours | fixed | gone | C-COLOUR-PATTERN |

### A21 STATE-MODELS: State models and operations disagree

*Mechanism:* models were written from prose; append-only was declared, not enforced.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R081 | State models disagree with the operations (transition credited to the wrong op, missing states, terminal st... | ours | open | grew | states |
| R185 | LedgerService declared append-only but its operations update rows | ours | open | grew | C-APPEND-ONLY |
| R233 | Parking plate change only allowed from 'active' though the common case is 'pushed' | ours | open | gone | states, CR-1 |

### A22 LINEAGE: Declared reads, writes and emits do not match what the operation does

*Mechanism:* the lineage is derived from request and response shapes, so it misses side effects.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R071 | Operations' declared reads/writes do not match their behaviour: needed tables omitted, wrong or unused tabl... | ours | open | grew | lineage, CR-3 |
| R114 | Operations change another service's data with no defined operation, event or ownership (foreign-writer rule) | ours | open | grew | CR-3 |
| R141 | Operations write cache:resolution with no key, value or invalidation rule | ours | open | grew | CR-1 |
| R157 | Required notification/outbox events not named | ours | open | reduced | CR-3 |
| R189 | Flow needs an operation or writer the contract never defines | ours | open | grew | CR-3 |

### A23 AUTH-SCOPE: Permission, audience or scope does not fit the caller

*Mechanism:* permissions and scope levels were chosen per contract, not per actor and screen.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R072 | Guest-audience operations require staff permissions (PRODUCT_VIEW, ORDER_VIEW, TENANT_CONFIGURE...) with gu... | ours | open | reduced | screens-guest, S-GUEST-AUDIENCE |
| R091 | Permission chosen for an operation does not fit its action, actor or level | both | client | reduced | CR-1, pkg-23 |
| R097 | Venue/region-scoped operations take no venueId; where scope comes from, what an optional or body venueId me... | ours | open | grew | CR-1 |
| R098 | Scope level of operations does not fit where the screen runs: Platform Console calls tenant-cell ops with n... | both | client | grew | CR-1 |
| R100 | Workstation/device-scoped operations are consumed by back-office, partner or guest callers with no workstation | ours | open | grew | S-WORKSTATION-OP |
| R140 | Unauthenticated guest calls (getTenantAppStatus, tenant content): tenant resolution and public auth not dec... | ours | open | grew | pkg-9 |
| R164 | Guest/public/list operations expose internal or secret fields (principal ids, budget caps, draft internals) | ours | open | reduced | C-GUEST-INTERNAL |
| R167 | Guest sign-in screens wired to staff login/SSO/MFA that require a workstation and return a staff session | both | client | same | S-GUEST-AUDIENCE, screens-guest |
| R183 | Scope level of the permission check does not match where the row lives | both | client | grew | migrations |
| R197 | x-ticvai-permission-escalated equals the base permission | both | client | same | pkg-escalated |
| R199 | recordNoSale gated by SHIFT_SUSPEND (copy-paste) | ours | open | gone | CR-1 |
| R209 | Guest screens call requestSuggestion with kinds guests may not ask | both | client | grew | CR-1 |
| R289 | Guest order-history screens still wire staff listOrders instead of listMyOrders | ours | open | grew | S-GUEST-AUDIENCE, screens-guest |

### A24 GLOSSARY: A synonym the glossary bans, or a term it does not define

*Mechanism:* names were taken from the client boards and backend workbook, not the glossary.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R131 | Item/SKU/MerchandiseItem/MenuItem used where the glossary requires Product | both | client | gone | G-BANNED-NAME |
| R145 | Booking/Reservation/Hold used against the glossary | both | client | reduced | G-BANNED-NAME |
| R146 | Domain terms used by contracts/screens that the glossary does not define | client | client | grew | CR-4 |
| R147 | Other glossary drift (one concept two names, misc banned synonyms) | ours | open | reduced | G-BANNED-NAME |
| R155 | Guest/guestId used where the glossary requires Subject | ours | open | gone | G-BANNED-NAME |
| R156 | Till/drawer/float/station/POS/layout used where the glossary requires Workstation, Deposit Box or Sale Board | both | client | reduced | G-BANNED-NAME |
| R165 | Session used where the glossary requires Performance | both | client | reduced | G-BANNED-NAME |
| R190 | 'Bundle' means two things: promotions Bundle vs signed catalogue BundleSummary | ours | open | reduced | CR-4 |
| R193 | Media overloaded: DAM assets vs the ticket carrier | ours | open | same | CR-4 |
| R194 | Zone/Department/Org unit used where the glossary requires Operating Area or Scope Node | both | client | reduced | G-BANNED-NAME |
| R195 | Envelope renamed channel_capacity: two names for one concept | ours | open | reduced | CR-4 |
| R210 | Ticket reused for kitchen tickets / QR against the glossary | both | client | gone | G-BANNED-NAME |
| R211 | Case "subject" collides with canonical Subject | ours | open | gone | CR-4 |
| R220 | Card/cardCode used where the glossary requires Media / Media Code | both | client | reduced | G-BANNED-NAME |
| R221 | AccessPoint mode vs operatingMode overlap; setTurnstileMode title | both | client | reduced | CR-4 |

### A25 PROSE-QUALITY: Prose that is corrupted, stale after a rename, or promises what the schema lacks

*Mechanism:* find-and-replace and renames swept code, not descriptions, notes and comments.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R083 | Operation/schema description promises fields or behaviour its schema cannot express | ours | open | reduced | CR-1 |
| R138 | Contract YAML prose corrupted by line-wrap/find-replace ("s ervice", dropped words) | ours | open | grew | C-PROSE-SPLIT |
| R160 | platform.org_unit -> platform.scope rename left behind in descriptions and DDL comments | ours | fixed | reduced | D-RENAME-RESIDUE, doc-tables |
| R266 | Screen open questions cite inventory endpoints that do not exist, unresolved/stale | ours | fixed | reduced | S-OPENQ-STALE |
| R269 | Screen notes/metadata stale after later renames and rewiring | ours | open | grew | S-NOTES-STALE |
| R287 | BO-104 F&B screens moved to P15 then rolled back; notes and edges disagree | ours | open | reduced | S-NOTES-STALE, N-ENTRY-MIRROR |

### A26 BUSINESS-RULES: Behaviour the contract leaves unspecified

*Mechanism:* operations were drafted from boards with the happy path only.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R094 | 'Configured' limits, windows and thresholds have no named source or value | both | client | reduced | uncontrolled, CR-1 |
| R096 | Contract prose states a rule or behaviour without defining it | client | client | reduced | CR-1 |
| R101 | CatalogueService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R106 | VenueOpsService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R108 | Duplicate codes and unknown/cross-venue/cyclic references on create/update have no defined outcome | both | client | grew | CR-1 |
| R123 | OrderService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R125 | FnbService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R126 | IdentityService: operation-specific business rules, validation and failure cases left unspecified | client | client | reduced | CR-1 |
| R127 | LedgerService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R128 | Stored-vs-derived values: who maintains denormalised counters, flags and time-based status is unstated | ours | open | grew | CR-1 |
| R129 | TenancyService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R134 | Draft vs live tenant config handling inconsistent (which row get/set act on, draft save writes live cache, ... | ours | open | reduced | CR-1 |
| R137 | Versioning/snapshot promised but only one version can be stored | ours | open | reduced | CR-1 |
| R143 | Time zone for dates and day boundaries unstated | ours | open | grew | CR-1 |
| R144 | requiresApproval / approver / step-up semantics undefined | both | client | grew | CR-1 |
| R149 | MarketingService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R152 | Human-readable numbers/codes (caseNumber, orderNumber, receipt, card code) have no generation rule | both | client | reduced | CR-1 |
| R158 | ReportingService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R163 | WhiteLabelService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R169 | Required hold/expiry values (ttlSeconds, expiresAt) have no client default | both | client | reduced | CR-1 |
| R171 | InventoryService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R175 | Unknown or out-of-scope parent id on list/get: 404 vs empty vs defaults | ours | open | grew | CR-1 |
| R181 | Initial status/defaults on create not stated | ours | open | grew | CR-1 |
| R202 | Absence of an optional singleton resource (404 vs empty 200) unstated | ours | open | reduced | CR-1 |
| R213 | AiService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R214 | PlatformService: operation-specific business rules, validation and failure cases left unspecified | client | client | same | CR-1 |
| R215 | RetailService: operation-specific business rules, validation and failure cases left unspecified | client | client | grew | CR-1 |
| R228 | AccessService: operation-specific business rules, validation and failure cases left unspecified | both | client | grew | CR-1 |

### A27 CLIENT-DECISIONS: A platform, vendor, law or data decision the package cannot make

*Mechanism:* the question had no owner, so the package either guessed or stayed silent.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R038 | Project bible has little or no DevOps/CI/IaC guidance | both | client | reduced | CR-2 |
| R057 | DevOps setup tickets leave platform decisions open (CI system, cloud/region, client generator, cell mapping... | both | client | reduced | CR-2 |
| R065 | Acceptance depends on something not yet available (unbuilt backend, sandbox credentials, upstream process) | both | client | grew | CR-2 |
| R117 | External integrations/vendors named with no interface (payment gateway/tokenisation, FX, face-match, parkin... | both | client | grew | CR-2 |
| R191 | Operations that post to the ledger give no account mapping, fiscal period or entry number | client | client | grew | CR-2 |
| R203 | AI provider region scope cannot be expressed and residency owner disagrees | both | client | reduced | CR-2 |
| R205 | Face-pass guest flow lacks id sources and a guardian step | both | client | reduced | CR-2 |
| R229 | Seed data referenced but not in the package (denominations, system roles) | client | client | same | CR-2 |

### A28 MISSING-OPERATION: A screen or flow needs an operation or field the contract lacks

*Mechanism:* screens were designed from boards; nobody walked each datum back to an operation.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R121 | No pricing source for operations/screens that show or compute prices (Product has no price, listPrices not ... | ours | open | reduced | CR-3 |
| R124 | Cart / hold / order lifecycle contradicts between flows and the orders contract, and guest cartId source is... | ours | open | grew | CR-3 |
| R161 | transferOrderTickets needs ticketIds but Order/Entitlement expose no ticket id | ours | open | reduced | CR-3 |
| R166 | Guest parking contract: no pay step, no own-entitlement read, no live availability, 502 drops the entitlement | both | client | grew | CR-3 |
| R168 | No storage of plan licensed modules/limits for licence checks | ours | open | gone | CR-3 |
| R174 | Operations with no consuming screen ('Called by: no screen') | ours | open | reduced | screenless |
| R178 | listPerformances needs eventId but Product has no eventId and screens do not call listEvents | ours | open | grew | CR-3 |
| R187 | No itinerary/plan resource for guest plans | client | client | reduced | CR-3 |
| R188 | getMyMemberships duplicates listGuestMemberships and the tier-benefit source disagrees | ours | open | grew | CR-3 |
| R196 | Operations take a storageRef/fileReference but no upload operation is linked | ours | open | same | S-UPLOAD |
| R204 | Alert schema has no workstation/shift/item fields and listAlerts cannot filter by them | ours | open | gone | CR-3 |
| R206 | No operation lists or reads configuration profiles/deployments | ours | open | gone | CR-3 |
| R207 | Shift close/variance approval has no operation and Shift carries no variance figures | ours | open | reduced | CR-3 |
| R208 | Guest queue entry id has no source after joinQueue | ours | fixed | gone | CR-3 |
| R224 | listModifierGroups used on guest menu though GuestMenu embeds modifierGroups | ours | open | reduced | CR-3 |
| R225 | getAvailability cannot give performances for a date | ours | open | reduced | CR-3 |
| R226 | listContentPages cannot select a page kind or published-only for guests | ours | open | reduced | CR-3 |
| R232 | claimTableSession vs claimLocationSession used inconsistently | ours | open | grew | CR-3 |
| R236 | Shop-and-drop reservation not tied to a cart, order or payment | both | client | reduced | CR-3 |
| R241 | verifyAllergens runs on every recipe change but screens give it a Verify button | both | client | gone | CR-3 |
| R242 | No operation reads guest in-venue notifications | both | client | reduced | CR-3 |
| R243 | No operation lists a guest ticket transfers | ours | fixed | gone | CR-3 |
| R244 | Menu versioning and scheduled publishes have no schema/list support | ours | fixed | reduced | CR-3 |
| R245 | Sync rejections have no resolve operation | ours | open | same | CR-3 |
| R259 | Screen needs data (names, pickers, lookups, period lists) that no linked operation supplies | ours | open | grew | S-NO-READ, CR-3 |
| R265 | Screen has load/error states or edits a resource but links no read | ours | open | grew | S-NO-READ |
| R280 | Screen needs (search, filters, onLoad reads) not met by operations in the first-release slice | ours | open | grew | CR-3 |
| R282 | Report screens bind to generic runReport/getFinancialReport with no named report or parameters | both | client | grew | CR-3 |
| R283 | Hub/dashboard screens promise attention counts or metric tiles with no operation | both | client | grew | S-METRIC-NO-OP |
| R288 | 202/queued operations have no linked poll/result op | ours | open | grew | S-ASYNC-POLL |
| R293 | Export button has no operation behind it | ours | open | reduced | S-EXPORT |

### A29 JOURNEY-CONTRACT: A journey contradicts the contract or the screen it runs on

*Mechanism:* flows were written from the boards and the contracts from the matrix, separately.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R139 | Journey/flow behaviour contradicts the contract (who does what, when, blocked vs warned) | both | client | reduced | CR-3 |
| R148 | Guest case contract: Case has no kind or messages and whether raising a case works offline disagrees | both | client | reduced | CR-3 |
| R184 | IdentityService session model contradicts itself (registry, displacement, refresh storage) | both | client | reduced | CR-1 |
| R223 | Deposit box allocated per cashier (schema) vs per till per shift (F73) | ours | open | reduced | CR-3 |
| R230 | F50 offline rotating QR vs getEntitlementCredential not offline-capable | both | client | same | CR-3 |
| R231 | Journey F52 treats a Reservation as a paid booking; glossary says unpaid hold | ours | open | same | CR-3 |
| R234 | Flow F02 relies on SeatAvailability 'renderMode' the schema lacks | ours | fixed | reduced | CR-3 |
| R261 | Journey step operation lists / branches disagree with the screen apis | both | client | reduced | flows |

### A30 SCREEN-GENERATED: Generator boilerplate left on screens

*Mechanism:* generate-screens pasted list-pattern states, regions and buttons onto every screen.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R250 | Screen UI states are generic list-pattern boilerplate (create action, filter, missing permission) that do n... | ours | fixed | grew | S-STATE-BOILERPLATE |
| R253 | Generated screen regions are placeholders: duplicate contentBody, unbound/duplicate action buttons, "Compon... | ours | fixed | reduced | S-DUP-REGION |
| R255 | Screen permission is null while operations need one or several permissions, so emptyNoAccess cannot name on... | ours | open | reduced | S-SCREEN-PERMISSION |
| R256 | Screen layout regions bound to the wrong schema or the wrong pattern (desktop split on phone, system fields... | ours | fixed | grew | S-PANEL-ENTITY |
| R260 | Generated screen labels, component/route names and api purposes are garbled, truncated or template text ("E... | ours | open | grew | S-PURPOSE-TEMPLATE |
| R264 | Action buttons have no form for the required fields of the operation they call | ours | fixed | reduced | S-BUTTON-FORM |
| R268 | Operations that mutate or need user input are triggered onLoad | ours | fixed | reduced | S-ONLOAD-WRITE |
| R273 | Declared screen operations reach no component | ours | open | reduced | S-OP-UNREACHED |

### A31 SCREEN-WRONG-OP: A screen wires an operation wrong for its platform or purpose

*Mechanism:* operations were attached by name resemblance and bulk passes, not from the screen's purpose.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R254 | Operations attached to screens mechanically (by name resemblance, bulk attach, whole contract families, flo... | ours | fixed | reduced | S-CONSUMED-MIRROR, screens-attach |
| R257 | Screen offlineCapable / offline state contradicts its operations' x-ticvai-offline-capable and the journey | ours | open | reduced | S-OFFLINE-CLAIM |
| R263 | Module label on screen/ticket differs from the contract operation module | ours | open | reduced | screens-module |
| R271 | Web screens not offline-capable yet define an offline state that keeps cached data with no browser store | ours | open | reduced | S-OFFLINE-CLAIM |
| R275 | Screen form fields, filters or actions do not map onto the contract body or enums | both | client | grew | S-FIELD-BINDING |
| R276 | Screens duplicate or overlap another screen with no stated division | both | client | grew | S-DUP-SCREEN, redundancy |
| R277 | Kitchen display screens promise course filter, station load, bump and a ticket read fnb does not provide | both | client | grew | CR-3 |
| R278 | Screen guards use dotted permission names not in the SCREAMING_SNAKE enum | ours | open | reduced | screens-guard |
| R279 | Section/settings screens lean on getVenueSettings for things it does not hold and need TENANT_CONFIGURE | ours | open | grew | CR-3 |
| R284 | Kitchen rail ordering given three ways | ours | open | grew | CR-3 |
| R285 | Till screens call catalogue ops though terminals must read the local catalogue bundle | ours | open | grew | CR-3 |
| R286 | P15 Kitchen Display platform exists although the contract says TICVAI does not build a kitchen display | ours | open | gone | CR-3 |
| R290 | Till screens use server carts though POS never uses carts | ours | open | grew | CR-3 |
| R291 | Guest concierge: createAiConversation module and conversationId source undefined | ours | open | grew | CR-3 |
| R292 | Loyalty screens call evaluatePromotions which needs a cart the screen does not have | ours | open | gone | CR-3 |

### A32 NAVIGATION: Navigation inferred, not designed

*Mechanism:* exits came from module nav-sets and carries were copied from the destination.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R251 | Inferred navigation is wrong: one-sided entry/exit, exits to unrelated screens, params the screen never hol... | ours | fixed | grew | N-ENTRY-MIRROR, N-CARRIES-HELD |
| R262 | Screens declare no entry params for ids every call needs, and inbound transitions carry none | ours | open | grew | screens-params, N-CARRIES-HELD |
| R281 | Web and app twin screens break stated parity (ops, states, wave, journeys) | ours | open | reduced | N-TWIN-WAVE, N-TWIN-OPS |

### A33 WIREFRAMES: A screen with no wireframe, or a drawn frame nothing links

*Mechanism:* drawn frames were archived and screens repointed to generated ones; new frames land unlinked.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R252 | Screens have no wireframe: generated frame notStarted, boardFrames empty, or noted as needing drawing (repo... | both | client | grew | W-NO-DESIGN |
| R258 | Drawn Claude Design / client frames archived to _dump/wireframes-3-september; screens repointed to notStart... | both | client | grew | W-INCOMING-UNLINKED, W-DUMP-POINTER |
| R272 | Wireframe pack frames exist but the screen record does not reference them (APP packs, Park_POS mockup, titl... | ours | open | reduced | W-INCOMING-UNLINKED |

### A34 SCREEN-CONTEXT: A screen does not say where its context comes from or how it behaves

*Mechanism:* screen records hold what is shown, rarely what is assumed.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R267 | Guest app screens do not say where current venue/subject/card/entitlement context comes from | both | client | reduced | session, CR-2 |
| R270 | Screen-specific behaviour left unstated (offline write, validation, error display): individual screen gaps | both | client | grew | CR-1 |

### A35 ONE-OFFS: Single findings with no shared cause

*Mechanism:* none shared: each batch's leftovers, fixed or decided one by one.

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R073 | one-offs (b04) | both | client | gone | **not closed** |
| R077 | one-offs (b06) | both | client | gone | **not closed** |
| R080 | one-offs (b01) | both | client | gone | **not closed** |
| R085 | one-offs (b12) | ours | open | gone | **not closed** |
| R110 | one-offs (b02) | both | client | gone | **not closed** |
| R116 | one-offs (b08) | ours | open | gone | **not closed** |
| R120 | one-offs (b03) | both | client | gone | **not closed** |
| R132 | one-offs (b10) | both | client | gone | **not closed** |
| R136 | one-offs (b13) | ours | open | gone | **not closed** |
| R150 | one-offs (b14) | ours | open | gone | **not closed** |
| R219 | one-offs (b05) | ours | open | gone | **not closed** |

### A36 FALSE: Findings the verdict pass found false

*Mechanism:* the agent misread the package (a platform flag as a screen flag, a tool name, a ticket parent).

| Root | Title | Bucket | Status | F8 | Guard |
|---|---|---|---|---|---|
| R023 | Pull hint / README / CLAUDE.md name tools that are not in the session (adam_link vs adam_links, adam_propos... | none | won't fix | gone | n/a |
| R055 | No comments / no change requests on the ticket (informational) | none | won't fix | reduced | n/a |
| R060 | DB tickets titled/parented 'Venue Management' for tables owned by another service or database | none | won't fix | gone | n/a |
| R062 | Ticket spec link anchor '#group-x' does not exist in the service doc | none | won't fix | grew | n/a |
| R068 | Wireframe check raised on non-UI tickets (DB, DevOps) | none | won't fix | gone | n/a |

## Guards

| Guard | Kind | Where | Gates | Known today | Note |
|---|---|---|---|---|---|
| `C-ACTION-409` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 123 |  |
| `C-APPEND-ONLY` | new check | `ticvai/tools/check-contract-shapes.py` | yes |  |  |
| `C-COLOUR-PATTERN` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 4 |  |
| `C-ENUM-NON-STRING` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 1 |  |
| `C-ENUM-OTHER` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 99 |  |
| `C-ERROR-PROBLEM-TYPE` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 604 |  |
| `C-EVENT-NAME` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 77 |  |
| `C-FIELD-TYPE-DRIFT` | new check | `ticvai/tools/check-contract-shapes.py` | yes |  |  |
| `C-GUEST-INTERNAL` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 2 |  |
| `C-ID-FORMAT` | new check | `ticvai/tools/check-contract-shapes.py` | yes |  |  |
| `C-MONEY-NUMBER` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 13 |  |
| `C-NO-ADDRESS` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 375 |  |
| `C-PAGED-ORDER` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 395 |  |
| `C-PROSE-SPLIT` | new check | `ticvai/tools/check-contract-shapes.py` | yes |  |  |
| `C-REQUEST-SERVER-FIELDS` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 100 |  |
| `C-SCHEMA-PARAMETERS` | new check | `ticvai/tools/check-contract-shapes.py` | yes |  |  |
| `C-SEARCH-PARAM` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 3 |  |
| `C-SUCCESS-PROBLEM` | new check | `ticvai/tools/check-contract-shapes.py` | yes |  |  |
| `C-TWO-IDEMPOTENCY` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 3 |  |
| `C-UNTYPED-BODY` | new check | `ticvai/tools/check-contract-shapes.py` | yes | 8 |  |
| `CR-1` | change rule | `ticvai/docs/active/change-rules.md` | no |  | a CR is written and reviewed against it |
| `CR-2` | change rule | `ticvai/docs/active/change-rules.md` | no |  | a CR is written and reviewed against it |
| `CR-3` | change rule | `ticvai/docs/active/change-rules.md` | no |  | a CR is written and reviewed against it |
| `CR-4` | change rule | `ticvai/docs/active/change-rules.md` | no |  | a CR is written and reviewed against it |
| `CR-5` | change rule | `ticvai/docs/active/change-rules.md` | no |  | a CR is written and reviewed against it |
| `CR-6` | change rule | `ticvai/docs/active/change-rules.md` | no |  | a CR is written and reviewed against it |
| `D-DESC-CUT` | new check | `ticvai/tools/check-ddl-conventions.py` | yes |  |  |
| `D-DOUBLE-KEY` | new check | `ticvai/tools/check-ddl-conventions.py` | yes | 2 |  |
| `D-FK-INDEX` | new check | `ticvai/tools/check-ddl-conventions.py` | yes |  |  |
| `D-FK-TARGET-NAME` | new check | `ticvai/tools/check-ddl-conventions.py` | yes | 14 |  |
| `D-HEADER-COUNT` | new check | `ticvai/tools/check-ddl-conventions.py` | yes |  |  |
| `D-JSONB-TWIN` | new check | `ticvai/tools/check-ddl-conventions.py` | yes |  |  |
| `D-MIG-ORDER` | new check | `ticvai/tools/check-ddl-conventions.py` | yes | 1 |  |
| `D-MIG-TABLES` | new check | `ticvai/tools/check-ddl-conventions.py` | yes |  |  |
| `D-NAMING` | new check | `ticvai/tools/check-ddl-conventions.py` | yes | 221 |  |
| `D-RENAME-RESIDUE` | new check | `ticvai/tools/check-ddl-conventions.py` | yes | 5 |  |
| `D-RUN-TOGETHER` | new check | `ticvai/tools/check-ddl-conventions.py` | yes |  |  |
| `D-SCOPE-LTREE` | new check | `ticvai/tools/check-ddl-conventions.py` | yes |  |  |
| `D-SCOPE-NOTNULL` | new check | `ticvai/tools/check-ddl-conventions.py` | yes |  |  |
| `D-STUB-TABLE` | new check | `ticvai/tools/check-ddl-conventions.py` | yes | 12 |  |
| `G-BANNED-NAME` | new check | `ticvai/tools/check-glossary-terms.py` | yes | 198 |  |
| `N-CARRIES-HELD` | new check | `ticvai/tools/check-navigation.py` | yes | 54 |  |
| `N-ENTRY-MIRROR` | new check | `ticvai/tools/check-navigation.py` | yes |  |  |
| `N-TWIN-OPS` | new check | `ticvai/tools/check-navigation.py` | yes | 33 |  |
| `N-TWIN-WAVE` | new check | `ticvai/tools/check-navigation.py` | yes | 11 |  |
| `S-ASYNC-POLL` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 70 |  |
| `S-BUTTON-FORM` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 92 |  |
| `S-CONSUMED-MIRROR` | new check | `ticvai/tools/check-screen-wiring.py` | yes |  |  |
| `S-DUP-REGION` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 212 |  |
| `S-DUP-SCREEN` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 35 |  |
| `S-EXPORT` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 12 |  |
| `S-FIELD-BINDING` | new check | `ticvai/tools/check-screen-wiring.py` | yes |  |  |
| `S-GUEST-AUDIENCE` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 1 |  |
| `S-METRIC-NO-OP` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 1085 |  |
| `S-NO-READ` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 413 |  |
| `S-NOTES-STALE` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 1 |  |
| `S-OFFLINE-CLAIM` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 21 |  |
| `S-ONLOAD-WRITE` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 5 |  |
| `S-OP-UNREACHED` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 2614 |  |
| `S-OPENQ-STALE` | new check | `ticvai/tools/check-screen-wiring.py` | yes |  |  |
| `S-PANEL-ENTITY` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 7 |  |
| `S-PURPOSE-TEMPLATE` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 54 |  |
| `S-SCREEN-PERMISSION` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 2382 |  |
| `S-STATE-BOILERPLATE` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 2898 |  |
| `S-UPLOAD` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 39 |  |
| `S-WORKSTATION-OP` | new check | `ticvai/tools/check-screen-wiring.py` | yes | 130 |  |
| `SF-APP-MISSING` | new check | `ticvai/tools/check-starter-fit.py` | yes |  |  |
| `SF-APP-RUNTIME` | new check | `ticvai/tools/check-starter-fit.py` | yes |  |  |
| `SF-CLAUDE-PATHS` | new check | `ticvai/tools/check-starter-fit.py` | yes |  |  |
| `SF-DOC-TYPES` | new check | `ticvai/tools/check-starter-fit.py` | yes |  |  |
| `SF-DOCS-MIRROR` | new check | `ticvai/tools/check-starter-fit.py` | yes | 4 |  |
| `SF-DONE-GATES` | new check | `ticvai/tools/check-starter-fit.py` | yes | 1 |  |
| `SF-EMPTY-STUB` | new check | `ticvai/tools/check-starter-fit.py` | yes | 3 |  |
| `SF-GLOSSARY` | new check | `ticvai/tools/check-starter-fit.py` | yes |  |  |
| `SF-ID-RULE` | new check | `ticvai/tools/check-starter-fit.py` | yes |  |  |
| `SF-OUTBOX-POLICIES` | new check | `ticvai/tools/check-starter-fit.py` | yes |  |  |
| `ST-ENUM-CHECK` | new check | `ticvai/tools/check-contract-storage.py` | yes | 2 |  |
| `ST-FIELD-NO-COLUMN` | new check | `ticvai/tools/check-contract-storage.py` | yes | 192 |  |
| `ST-OFFLINE-RECORDED-AT` | new check | `ticvai/tools/check-contract-storage.py` | yes | 9 |  |
| `ST-REQUIRED-MISMATCH` | new check | `ticvai/tools/check-contract-storage.py` | yes | 40 |  |
| `ST-TYPE-MISMATCH` | new check | `ticvai/tools/check-contract-storage.py` | yes | 8 |  |
| `T-AUTH-TESTS` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-BOILERPLATE` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-DONE-WHEN` | new check | `ticvai/tools/check-ticket-text.py` | yes | 2 |  |
| `T-MIG-DONE` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-NONEMPTY-LABEL` | new check | `ticvai/tools/check-ticket-text.py` | yes | 31 |  |
| `T-ONBOARD-SOURCE` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-PROVISIONAL` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-PURPOSE-CUT` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-READ-ROUTING` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-REPO-ITEMS` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-REVIEWER` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-SETUP-REPO` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-SLICE-CALLS` | new check | `ticvai/tools/check-ticket-text.py` | yes | 1 |  |
| `T-SPEC-SCREEN` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `T-USED-BY` | new check | `ticvai/tools/check-ticket-text.py` | yes | 6 |  |
| `T-WAVE` | new check | `ticvai/tools/check-ticket-text.py` | yes |  |  |
| `W-DUMP-POINTER` | new check | `ticvai/tools/check-wireframe-coverage.py` | yes |  |  |
| `W-INCOMING-UNLINKED` | new check | `ticvai/tools/check-wireframe-coverage.py` | yes | 17 |  |
| `W-NO-DESIGN` | new check | `ticvai/tools/check-wireframe-coverage.py` | yes | 296 |  |
| `connector` | existing check | the audit kit's ticvai-connector.mjs (not in git), `viewer/mcp/mcp-check.mjs` | yes |  | replays the connector roots' own cases through the real tools; not in run-checks and audit/ is git-ignored, so it guards only while this machine runs it (S001 step checks) |
| `doc-tables` | existing check | `ticvai/tools/check-doc-tables.py` | yes |  | docs/ only |
| `flows` | existing check | `ticvai/tools/check-flows.py` | yes |  |  |
| `frontend` | existing check | `ticvai/tools/check-frontend.py` | yes |  |  |
| `lineage` | existing check | `ticvai/tools/check-lineage.py` | yes |  | holds the lineage to the contracts, not to behaviour |
| `migrations` | existing check | `ticvai/tools/check-migrations.py` | yes |  |  |
| `pkg-23` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `pkg-32` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `pkg-33` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `pkg-39` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `pkg-46` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `pkg-47` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `pkg-48` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `pkg-49` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `pkg-50` | existing check | `ticvai/tools/check-package.py` | yes |  | kebab-case and one param type gate; plural/POST-on-item warn |
| `pkg-9` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `pkg-escalated` | existing check | `ticvai/tools/check-package.py` | yes |  |  |
| `redundancy` | existing check | `ticvai/tools/check-screen-redundancy.py` | no |  | warnings only |
| `screenless` | existing check | `ticvai/tools/audit-screenless-operations.py` | yes |  |  |
| `screens-attach` | existing check | `ticvai/tools/check-screens.py` | no |  | warnings only |
| `screens-guard` | existing check | `ticvai/tools/check-screens.py` | yes |  |  |
| `screens-guest` | existing check | `ticvai/tools/check-screens.py` | yes |  |  |
| `screens-module` | existing check | `ticvai/tools/check-screens.py` | yes |  |  |
| `screens-params` | existing check | `ticvai/tools/check-screens.py` | yes |  |  |
| `session` | existing check | `ticvai/tools/check-session-entry.py` | yes |  |  |
| `states` | existing check | `ticvai/tools/check-states.py` | yes |  |  |
| `uncontrolled` | existing check | `ticvai/tools/audit-uncontrolled-values.py` | no |  | report-only in run-checks |

