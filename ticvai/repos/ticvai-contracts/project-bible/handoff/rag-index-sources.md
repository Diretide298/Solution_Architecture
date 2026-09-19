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
| `marketing.case` | subject, resolution | knowledge | tenant | wholeRecord | `marketing.caseClosed` |
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
owning service should publish anyway, and other consumers want them. 29 events are now declared.

## What is still missing: six of the eleven text fields

**The tables all exist. Six of them do not have the column this file says to embed.** Checked
against `handoff/schema-reference.json`:

| Source | Declared | Present | Absent |
|---|---|---|---|
| `whitelabel.policy` | title, body | `body` | **`title`** |
| `catalogue.entitlement_template` | name, description | `name` | **`description`** |
| `retail.merchandise` | name, description | `name` | **`description`** |
| `maintenance.inspection_template` | name, instructions | `name` | **`instructions`** |
| `marketing.case` | subject, resolution | `subject` | **`resolution`** |
| `assets.media_asset` | title, extractedText | `title` | **`extractedText`** |

**These are contract gaps, not errors in this file, and two of them are load-bearing.**
`marketing.case` has no `resolution` column, so the source whose whole value is "how was the
last one resolved" can only embed the subject line. `assets.media_asset` has no
`extractedText`, so the generic path for anything a tenant uploads has nothing to index until
extraction has somewhere to write.

The other four are prose the contract describes but never gave a field:
`maintenance.inspection_template.instructions` is the staff-assistant source that matters most
and is the clearest of the four.

**Indexing a column that does not exist is not a silent failure — it is a missing source.**
Until the contracts declare these six, those sources index their name and nothing else.
