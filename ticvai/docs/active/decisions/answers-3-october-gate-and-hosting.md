# Chinmay's gate and hosting decision (3 October 2026, evening)

> **The cited copy (3 October 2026, CHG-R1S-001, CHG-R1S-026).** The sections "Gate and hosting" and "Block A size and embeddings" of Chinmay's answers log
> (the lead's working log of batch 1 onward), copied into git so the R1S change entries can cite it
> (`ticvai/CLAUDE.md` rule 12). Verbatim, followed by the lead's clarification relayed the same evening.
> It amends DEC-539 (no in-cell gpt-oss-120b fallback) and DEC-543 (the guard is the provider's safety
> service, not a self-hosted Qwen3Guard); DEC-542 (the offline Presidio scrubber) stands.
> **Corrected 4 October 2026 (CHG-R11-001; the last section):** the embeddings are ours, in the cell, never an LLM.

## Gate and hosting (Chinmay, 3 Oct evening)
- Gate failed (new kinds of problem): fix now, re-gate, cut r1 late; design batches start in parallel.
- Hosting: "We are not hosting anything unless client asks it." No in-cell open model (gpt-oss-120b), no GPU node pool. The AI goes through providers: Core42 Compass by default, OpenAI UAE as fallback, BYOK. The guard model (Qwen3Guard) needs a GPU host, so it becomes the provider-side safety service (e.g. Azure AI Content Safety, UAE North) unless the client asks for self-hosting (default; Chinmay may drop the guard). The Presidio scrubber stays: a CPU library inside our own worker, not a hosted model; scrubbing stays mandatory. On-prem / self-hosted models only when a client asks.

## Clarification relayed by the lead (3 October, evening)
Chinmay confirmed we never host an LLM unless a client asks, and the guard model (Qwen3Guard) is itself an LLM.
The guard becomes the provider's content-safety service (for example Azure AI Content Safety in UAE North for
uaeOnly; the provider's own moderation for BYOK and globalAllowed), still fail-closed: with the scrubber or the
safety service down the call is refused 503 scrubber-unavailable, never sent raw. The offline Presidio scrubber
stays mandatory in every residency class.

## Block A size and embeddings (Chinmay, 3 Oct evening)
- Block A ships in two drops: A1 by 27 Nov (the original Block A core plus the completeness work that fits, incl. the accepted 43 h overtime, prioritised so every A1 app works end to end); A2 = the rest of the pulled-in work, right after, ahead of Block B. Chinmay: "before we were completing in Feb, so work is definitely getting pulled into A from others" - the program end should stay about where it was.
- Keep A2 small: apply lever A (pull in app homes only, not the 42 command centres; section homes link to their setup screens) and lever B (don't pull a service's writers into Block A just because its reads are there).
- Embeddings: provider embeddings on the UAE route (OpenAI UAE text-embedding-3-large / Core42), no embedding model hosted by us; Qdrant stays in our cell for the vectors (ADR-0049). "We have a GPU server" noted, not used for tenant data.

## Correction (Chinmay, 4 October 2026, evening): we host the embedding model, never an LLM

> **Added 4 October 2026 (CHG-R11-001), the 3 October text above left as it was recorded.** The "Embeddings" bullet
> above is a mis-recording: Chinmay's "We have a GPU server" was his answer, and it became "provider embeddings, no
> embedding model hosted by us" (CHG-R1S-026). From the lead's answers log, section "AI hosting correction
> (Chinmay, 4 Oct 2026, evening)", and the two follow-ups relayed the same evening, verbatim where quoted:

- **We host the embedding model and its reranker ourselves, never an LLM.** "Yes I said before we have to host for
  embeddings only not for LLM." LLM calls stay with the providers (Core42 Compass by default, OpenAI UAE as
  fallback, BYOK); the guard stays the provider's content-safety service. Tenant content is embedded in our own
  cell; Qdrant stays in the cell. Hybrid retrieval: our BGE-M3 dense vectors with Qdrant's BM25 sparse index,
  reranked by our reranker.
- **Where: GPU in UAE North, on Azure and on AWS** ("GPu in Azure and aws hosted in UAAE north").
- **Presidio and the Arabic NER run on the same server** ("its a sdk we can host it wihtin our embeddings server
  cant we ? also the arabic NER"; "For embeddings and scrubber we can gpu server"). Scrubbing stays mandatory; if
  the server is down the LLM call is refused (503 scrubber-unavailable), never sent raw.
- **No AI CPU node at all** ("Naaa dont keep AI CPU node at all"): the AI pool is the GPU node pool and carries the
  `ticvai-ai` pods too; the separate Presidio pool and the 2 x D8s v5 AI CPU pool ($700) go.
- **The node** (NV12ads was "a bit costly even for a gpu node"): Azure NV6ads A10 v5 (a sixth of an A10, 4 GB of GPU
  memory, 6 vCPU, 55 GB, UAE North), $0.649 an hour, $473.77 a month; one node without high availability, two with
  it, one per zone. It runs the `ticvai-ai` pods (about 1 vCPU each), Presidio's pattern rules on its CPU, and on
  its GPU at fp16 BGE-M3 (about 1.1 GB), its reranker (about 1.1 GB) and the Arabic NER (about 0.3 GB). The sizing
  is an assumption until the Sprint 2 benchmark; the step up is NV12ads A10 v5 ($947.54) on CPU saturation or GPU
  memory pressure. AWS (me-central-1): a g6.2xlarge-class node (one L4 with 24 GB, 8 vCPU; g6.xlarge's 4 vCPU is
  too few for the AI pods), its price and regional availability to confirm.
- **Cost (Azure, a month):** the 1 October base of $5,553.50 without high availability and $8,047.50 with it, less
  the $700 AI CPU pool, plus the GPU nodes ($473.77 / $947.54): **$5,327.27 without high availability, $8,295.04
  with it.**
- The Presidio link given was github.com/data-privacy-stack/presidio: confirm it is the Microsoft Presidio project
  before pinning a release.
