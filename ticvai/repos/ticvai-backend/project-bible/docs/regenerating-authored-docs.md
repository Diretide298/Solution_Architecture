# Regenerating the hand-authored docs after a contract change

> Companion to [`contract-change-runbook.md`](contract-change-runbook.md). That file says what a
> contract edit sets off; this one says how to rebuild the parts no tool rebuilds — ring 4.

## What feeds what

```
contracts/*.yaml ──┬─> derive-lineage.py --apply ──> api-data-lineage.json   <- FIRST, always
                   ├─> derive-domain.py ──> domain-markers.json
                   ├─> derive-schema.py ──> schema-reference.json
                   ├─> derive-relationships.py ──> relationships.csv
                   └─> build-audience.py ──> audience-index.json

api-data-lineage.json ──> 20+ tools, including build-audience.py
handoff/links.json ──> derive-domain.py            (an INPUT; nothing writes it)
service-decomposition.json ──┬─> derive-diagrams.py
                             ├─> derive-burst-scope.py
                             ├─> derive-service-counts.py (rewrites its arithmetic half)
                             ├─> build-schema-workbook.py
                             ├─> build-services-workbook.py
                             └─> check-package.py

traceability.json ──> build-status.py ──> status.json
contract-backlog.json ──> build-backlog-index.py ──> docs/registers/contract-backlog.md
backlog-clusters.json ──> build-cluster-index.py ──> docs/registers/clusters.md
docs/registers/conflicts.md ──> build-cf-index.py ──> conflict-status.md
```

**Seven files in `handoff/` are authored inputs that look derived**, and
`tools/check-authored-inputs.py` holds each of them: `service-decomposition.json`,
`contract-backlog.json`, `backlog-clusters.json`, `traceability.json`, `artefact-audit.md`,
`schema-viewer-notes.md` and `rag-index-sources.md`. (`handoff/links.json` is an input too and is
outside that check.) **`api-list.md` and `wireframes/LINKAGE.md` were on this list until
19 September and are generated now** by `tools/build-api-list.py` and `tools/build-linkage.py`; a
file that can be generated should be.

---

## How the check holds each file (3 November 2026, r14)

**Until r14 the check compared every file with one hash of the whole contract surface.** Any new
operation anywhere made all seven stale, so they sat in `tools/refresh-safe-baseline.json` for a
month while four of them really were wrong (review E-02). **Now each file has its own test, about
what that file describes**, in two kinds:

- **Computed** — rules the file can be held to mechanically. They can never be blessed away, and
  `--bless` refuses a file that fails one. Every name a file writes in backticks must be an
  operation, schema, schema property or enum value, table or `table.column`, event, event file or
  payload field, contract, or a contract's declared job or query. **Write a historical name that
  no longer exists without backticks, or struck through (~~`old`~~).**
- **Described** — a record of only the part of the package the file is about, taken by `--bless`.
  When that part moves the file is STALE and the check prints what moved (the operations that
  arrived, by name), so the re-read is of those, not of the whole file.

| File | Computed (must pass) | Described (re-read when it moves) |
|---|---|---|
| `service-decomposition.json` | every deployable contract (`contracts/spine`, `contracts/satellite`, not `x-ticvai-tier: device`) in exactly one service; every schema with tables owned by exactly one service; tiers and deployables defined; `operations`, `tables`, `readsFrom`, `writesOutside` and the note's opening as `derive-service-counts.py` derives them; no undated count in prose | each deployable contract and the schemas it persists into; every schema |
| `contract-backlog.json` | every named contract exists; an open entry's `what`, `why` and `blockedNote` name only things that exist; **an open entry's `fix` proposes no operation that exists** (an existing operation is cited dotted, `contract.op`; a bare one is a proposal); an open entry blocked on nothing whose matrix rows are all CONTRACTED fails | the operations and schema shapes of the contracts the open entries name (an entry whose fix delegates to `traceability.json` rows is held by the rows) |
| `backlog-clusters.json` | every backlog entry in a cluster or `unclustered`; every id exists; `entryCount`, `rowCitations`, `lanes` and `contracts` equal what the entries give; cited CFs are in the register | each entry's `what` |
| `traceability.json` | contract and evidence exist (as `check-traceability` also checks); a partial or gap row against a done entry names the decision (`cf`) that keeps it partial; notes name only things that exist | the operations and schema shapes of the contracts the rows that are not CONTRACTED are in |
| `artefact-audit.md` | the verdict table and the domain table equal `traceability.json`; the closed-class list is `closed_classes.json`; no held count is higher than the package holds (counts are dated); names exist | `closed_classes.json` and every CF row it cites |
| `schema-viewer-notes.md` | the three hubs, in order, are the three most-referenced tables; its edge-kind and `how` tables list exactly the values in `relationships.csv`; ambient is exactly lineage; the column-less tables are counted and named; names exist (its counts are a dated measurement) | — (everything it claims is computed) |
| `rag-index-sources.md` | every source's table exists, every text field is a column of it, every invalidating event exists and lists `ai` as a consumer; the declared tables are exactly those `reindexSource` reads; the event table matches `events/`; no undated count | the `IndexSource` model and the indexing operations' descriptions, which its four rules restate |

**A count written into authored prose carries its date** ("on 3 November 2026", "at r13"). An
undated count claims to be current, and that is the claim that goes stale silently. Where a count
is arithmetic, keep it in the field that is derived (`operations`, `tables`) instead of the prose.

```
python3 tools/check-authored-inputs.py                 # the check; its self-tests run first
python3 tools/check-authored-inputs.py --self-test     # 20 sabotaged inputs, each must be caught
python3 tools/check-authored-inputs.py --bless handoff/<file>   # after re-reading it
```

**A contract or event that does not parse is an ISSUE**, not a skipped file (review E-07), and so
is a missing input any test reads.

---

**These five are authored narrative and read the contracts.** When a contract changes they can go
stale; the check now says which, and why.

Paste one prompt per session into Claude Code from the repo root. **Do them one at a time** —
each needs the contracts read carefully, and batching produces summaries rather than documents.

---

## House style — prepend to any of these

```
House style for this repo: terse and evidence-first. State what is true and name the operation,
schema or ADR that proves it. No hedging, no marketing language, no "it is worth noting".
Bold the claim, not the label. Where a design choice looks odd, give the reason in one line —
the existing docs do this well, e.g. "a deposit box is allocated to a cashier, not a till".
Never restate a heading in its first sentence. Do not invent counts: derive every number from
the files, say how you derived it, and date it.
```

---

## 1. `handoff/api-list.md` — generated since 19 September

`python3 tools/build-api-list.py`. Do not edit it by hand.

## 2. `handoff/rag-index-sources.md` — check the sources still exist

```
Verify and update handoff/rag-index-sources.md against the current contracts.

It declares eleven RAG index sources, each naming a table, the fields carrying retrievable
text, the collection it lands in, and the domain event that invalidates it. check-package.py
reads this file, so an error here fails a validator.

Run python3 tools/check-authored-inputs.py first: it reports any source whose table, text
field or event does not exist, and any table reindexSource reads that the register omits. If
only the IndexSource model or the indexing operations moved (STALE), re-read the "Four rules"
and "What the contract now says" sections against contracts/satellite/ai.yaml. Report what
changed before writing, then write, then --bless.
```

## 3. `handoff/artefact-audit.md` — re-derive, do not patch

```
Re-derive handoff/artefact-audit.md from handoff/traceability.json, handoff/closed_classes.json
and the current package. The verdict and domain tables must equal traceability (the check
fails them otherwise); recount and date every "What we hold" figure; re-read the Retention and
Device sections against the CFs they cite (the check reports STALE when one of those CF rows
changes). Keep the table shapes: viewer lib/decisions.mjs reads the class table by its Reqs,
Class, What we hold and Artefact columns and the 🔴/🟡/✅ marks. Mark the file's date.
```

## 4. `wireframes/LINKAGE.md` — generated since 19 September

`python3 tools/build-linkage.py`. Do not edit it by hand.

## 5. `handoff/schema-viewer-notes.md` — only if the shape changed

```
Check whether handoff/schema-viewer-notes.md is still accurate.

It explains why the schema graph mis-navigates — clicking a catalogue table takes you to
platform — and what the edge kinds mean. Run tools/derive-relationships.py. The check already
fails it if the hubs, the edge kinds, the how values, the ambient=lineage rule or the column-less
tables changed; if it passes, its dated numbers are history and the file can stay. Rewrite only
if the shape changed, and re-measure and re-date every number when you do.
```

---

## After any of them

```
bash tools/refresh.sh
```

All checkers in the refresh's closing block must pass. `check-package.py` reads
`rag-index-sources.md` and `service-decomposition.json`; `check-traceability.py` reads
`traceability.json` and `contract-backlog.json`; `check-authored-inputs.py` reads all seven.

## If you also changed x-ticvai-persistence

```
python3 tools/derive-schema.py && python3 tools/derive-domain.py && bash tools/refresh.sh
```

## 6. `handoff/service-decomposition.json` — a decision, not a prompt

**Its arithmetic half is derived and its boundary half is a decision.** `derive-service-counts.py
--apply` rewrites `operations`, `tables`, `readsFrom`, `writesOutside` and the note's opening
sentence; the check fails the file until it has been run. `tier`, `contracts`, `schemas`, `why`,
`scale` and `risk` are authored.

**Assigning a contract to a deployable service is a deployment decision, not a contract fact** —
the same reason `derive-lineage` is additive-only. When the check reports a deployable contract
assigned to no service, or a schema with no owner, a person answers "where does this deploy?" and
then `derive-service-counts.py --apply`, `derive-diagrams`, `derive-burst-scope` and both
workbooks re-run. `derive-lineage`'s `NEW_CONTRACT_SERVICE` map carries the working assumption for
contracts added since the decomposition was drawn: rental -> VenueOpsService, wallet ->
WalletService, payments -> OrderService, accreditation -> TenancyService, transport ->
VenueOpsService; all five are in the file. **A contract with no entry there and no assignment in
the file is the lead's decision**, not something to infer from its neighbours.

The device host's contract (`contracts/devices/`, `x-ticvai-tier: device`, ADAM CR-463) is a
localhost API with no tenant and no table, and is deliberately in no service. A contract in a
folder the check does not know is an ISSUE until somebody says which of the three it is.

## Worth knowing

**On 19 September `service-decomposition.json` still described 28 contracts and 378 tables when
there were 32 and 556**, with `rental` and `accreditation` absent, while every checker passed.
That is why this check exists. Its first form compared mtimes (wrong within a minute, because
`link-screens-contracts.py` back-annotates every contract on each refresh); its second compared
one whole-surface hash (always red, so allowlisted, so blind). The third tests what each file
claims and records only what each file is about.
