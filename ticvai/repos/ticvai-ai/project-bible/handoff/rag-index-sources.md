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
| `marketing.case` | subject, resolutionNote | knowledge | tenant | wholeRecord | `marketing.caseClosed` |
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
Qdrant — nothing cascades between the stores. `removeIndexEntry` exists for that, and it is
the path `pii.erase_subject` must call. **A knowledge base still answering from an erased
subject is an erasure that did not happen.**

**A full rebuild builds into a shadow collection and swaps.** Reindexing in place leaves the
assistant answering from a half-built index, which is worse than a stale one — stale is wrong
in a knowable way.

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
owning service should publish anyway, and other consumers want them. 30 events are now declared.

## The six missing text fields: four closed, two not

**Verified column by column on 20 September against `handoff/schema-reference.json`.** All
eleven tables exist and every one is read by an AI operation in the lineage, which is what
`check-package` enforces. **Two of the six fields added on 19 September are not where this
register says they are**, and both are sources whose whole value is the missing field.

| Source | Column | State |
|---|---|---|
| `whitelabel.policy` | `title` | present |
| `catalogue.entitlement_template` | `description` | present |
| `retail.merchandise` | `description` | present |
| `maintenance.inspection_template` | `instructions` | present |
| `marketing.case` | `resolution` | **landed as `resolution_note`.** Register corrected to `resolutionNote`; the column is right and the name here was wrong |
| `assets.media_asset` | `extractedText` | **on the wrong schema — open** |

### `extractedText` is on `MediaUsage`, not `MediaAsset`

`contracts/satellite/assets.yaml` carries `extractedText` on **`MediaUsage`**, whose
`x-ticvai-persistence` is `assets.media_usage` — the row recording *where an asset is used*,
required fields `surface` and `referenceId`. The asset itself, `MediaAsset` on
`assets.media_asset`, does not have it.

**So the generic upload path indexes a column that does not exist**, which this register's own
rule calls out: an index built on a missing column embeds a title and nothing else, and a PDF
nobody can search is a PDF nobody reads. It is also inserted above `id:` at the top of
`MediaUsage`'s properties rather than in place, which is the signature of an insertion that
matched the wrong anchor.

**This is a contract change and contracts are frozen**, so it is recorded rather than made. The
fix is to move the property to `MediaAsset`; nothing reads it yet, so nothing breaks in the
meantime except the source it was written for.

