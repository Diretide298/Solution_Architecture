# RAG index sources

**Eleven sources declared. The services that own them do not know AI exists.**

Each names a table, the fields carrying retrievable text, the collection it lands in and the
domain event that makes it stale. The AI service consumes the event; the owning service
publishes what it always published.

That direction matters. **Retrieval is downstream of the business**, and an indexing failure
must not become a failure to publish a product.

| Table | Text fields | Collection | Scope | Chunk | Invalidated by |
|---|---|---|---|---|---|
| `whitelabel.content_page` | title, body | knowledge | tenant | section | `whitelabel.contentPublished` |
| `whitelabel.faq_entry` | question, answer | knowledge | tenant | wholeRecord | `whitelabel.contentPublished` |
| `whitelabel.policy` | title, body | knowledge | tenant | section | `whitelabel.contentPublished` |
| `catalogue.product` | name, description | catalogue | venue | wholeRecord | `catalogue.productPublished` |
| `catalogue.entitlement_template` | name, description | catalogue | venue | wholeRecord | `catalogue.productPublished` |
| `fnb.menu_item` | name, description, allergens | catalogue | venue | wholeRecord | `fnb.menuPublished` |
| `retail.merchandise` | name, description | catalogue | venue | wholeRecord | `retail.merchandisePublished` |
| `maintenance.inspection_template` | name, instructions | knowledge | venue | section | `maintenance.templatePublished` |
| `marketing.case` | title, resolutionNote | knowledge | tenant | wholeRecord | `marketing.caseClosed` |
| `reporting.report_definition` | name, description | knowledge | tenant | wholeRecord | `reporting.definitionPublished` |
| `assets.media_asset` | title, extractedText | knowledge | tenant | section | `assets.documentIndexed` |

## Why each

**`whitelabel.content_page`** — **The pages you asked about.** Tenant-authored guest-app content — about us, plan your visit, accessibility. A guest-app asking "is there parking" should be answered from the page that says so.

**`whitelabel.faq_entry`** — Already written as question and answer, which is the shape retrieval wants. The highest-value source per unit of effort.

**`whitelabel.policy`** — Refund, privacy, terms. **Section-chunked** — a refund question should retrieve the refund clause, not the whole document.

**`catalogue.product`** — What is on sale. Drives both guest-app search and the configuration assistant, which needs to know what already exists before proposing something similar.

**`catalogue.entitlement_template`** — Validity, re-entry and transfer rules in prose. "Can I leave and come back" is answered from here.

**`fnb.menu_item`** — **Allergens are indexed deliberately.** 4.8.9 requires them always present, and "does the burger contain nuts" is a question with consequences.

**`retail.merchandise`** — Shop stock, for guest-app search.

**`maintenance.inspection_template`** — Operating and safety procedures. **The staff assistant source that matters most** — a technician asking how to isolate a chiller is asking a safety question.

**`marketing.case`** — Resolved cases. An agent facing a complaint benefits more from how the last one was resolved than from a policy.

**`reporting.report_definition`** — So "which report shows refunds by cashier" is answerable. **Closes part of CF-65** — 52 reports are named in the matrix and nobody can find them.

**`assets.media_asset`** — Uploaded PDFs and documents, after text extraction. The generic path for anything a tenant uploads.

---

## Four rules that apply to all of them

**Only `textFields` are embedded.** Indexing a whole row embeds ids and timestamps as though
they were meaning, and a search for "annual pass" then matches a UUID. Everything else
becomes payload used for filtering.

**`scope_path` always travels in the payload.** The vector store has no row-level security to
fall back on, so scope is carried or it is not enforced. A venue's operating procedure must
not answer a question about another venue.

**Deletion is explicit.** Removing a row from Postgres does not remove its vectors from
Qdrant — nothing cascades between the stores. `removeIndexEntry` removes one record and
`eraseSubject` every entry of an erased subject; `deleteGuestAccount` and an erasure that
arrives another way call them, and so does archiving (ADR-0047). **A knowledge base still
answering from an erased subject is an erasure that did not happen.**

**A rebuild never exposes a half-built index.** A tenant has one collection per embedding model
holding every source (ADR-0049), so a rebuild of one source writes its new points into that
collection under a new index epoch; retrieval filters on the old epoch until the rebuild is
verified, then flips in one step (`reindexSource`, lead decision of 20 October 2026). **The
shadow collection and alias swap are for a change of embedding model only**, which rebuilds every
source. Reindexing in place would leave the assistant answering from a half-built index, which is
worse than a stale one — stale is wrong in a knowable way.

## The seven events they need now all exist

**Closed since this file was written.** Every invalidating event named in the table above is
declared in `events/`, and `catalogue.productPublished` is no longer the only model:

| Event | File | Publisher |
|---|---|---|
| `whitelabel.contentPublished` | `events/whitelabel-contentPublished.yaml` | white-label |
| `fnb.menuPublished` | `events/fnb-menuPublished.yaml` | fnb |
| `retail.merchandisePublished` | `events/retail-merchandisePublished.yaml` | retail |
| `maintenance.templatePublished` | `events/maintenance-templatePublished.yaml` | maintenance |
| `marketing.caseClosed` | `events/marketing-caseClosed.yaml` | marketing-crm |
| `reporting.definitionPublished` | `events/reporting-definitionPublished.yaml` | reporting |
| `assets.documentIndexed` | `events/assets-documentIndexed.yaml` | assets |

**None of them is AI-specific and that was the argument for writing them** — each is a fact the
owning service should publish anyway, and other consumers want them. Each lists `ai` as a consumer,
which is what makes it an invalidation and not only a notification. 113 events were declared on
3 November 2026.

## The six text fields added on 19 September: all present now

**Re-verified column by column on 3 November 2026 against `handoff/schema-reference.json`**
(earlier checks on 20 and 21 September). `tools/check-authored-inputs.py` now holds every text
field in the table above to a column of its table, every invalidating event to `events/`, and the
eleven tables to the ones `reindexSource` reads, so this section records history rather than
being the check.

| Source | Column | State |
|---|---|---|
| `whitelabel.policy` | `title` | present |
| `catalogue.entitlement_template` | `description` | present |
| `retail.merchandise` | `description` | present |
| `maintenance.inspection_template` | `instructions` | present |
| `marketing.case` | `resolution_note` | present; the register said `resolution` until 20 September |
| `assets.media_asset` | `extracted_text` | **present since r8** (blocker ORDERS-MONEY-C19); `MediaUsage.extractedText` is kept on the wire and never written |

**`marketing.case` named a column it never had.** Until 3 November its text fields read
*subject, resolutionNote*; the case has no subject column — `subject_id` is the guest — and the
text a person reads is `title`. Corrected to `title`. The same check also found the sentence that
named pii.erase_subject as the erasure path, which was never a table or an operation.

**`extractedText` moved to the asset.** On 20 September it sat on `MediaUsage`, the row
recording where an asset is used, so the generic upload path indexed a column that did not exist.
`MediaAsset.extractedText` now holds it, written by the upload's processing job, and
`ingestKnowledgeDocument` reads it through Assets' `mediaAssetRecords`.

**No source was added on 21 September**: the two tables that arrived that day —
`payments.dunning_policy` and `payments.dunning_case` — carry no retrievable text, and a dunning
queue is transactional rather than knowledge. `resolveDunningCase` accepted a `note` that
`DunningCase` had nowhere to store; `resolutionNote` now exists, modelled on
`marketing.case.resolution_note`, **and it is deliberately not a source**, because a note about
somebody's failed payment is not knowledge anybody should be able to retrieve by asking.

## What the contract now says that this register does not

**Two statements in `contracts/satellite/ai.yaml` post-date this register and are not reconciled
with it.** Both are recorded here rather than resolved, because which kind a source feeds is a
declaration a tenant makes through `setIndexSource`, and the defaults are the AI lead's call.

- **Every declaration now carries a search kind** (`IndexSource.kind`: product, entitlement,
  knowledge, faq, report or media; R8 blocker ORDERS-MONEY-C37, the lead's answer of 20 October
  2026). A source with no kind is indexed and searched by nothing. The *Collection* column above
  names the knowledge collection a source lands in (`collectionId`), which is not the kind.
- **`assets.media_asset` is described twice.** `semanticSearch` (23.1.6, 29 September) says the
  `media` kind's source over `assets.media_asset` embeds the asset's title, description and tags;
  this register's row embeds title and extracted text into `knowledge`. A table has at most one
  declaration (`IndexSource.table` is unique), so one of the two is the default and the other is
  served elsewhere — uploaded documents' text already reaches `knowledge` through
  `ingestKnowledgeDocument`.
