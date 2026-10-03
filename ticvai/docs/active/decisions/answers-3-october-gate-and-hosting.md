# Chinmay's gate and hosting decision (3 October 2026, evening)

> **The cited copy (3 October 2026, CHG-R1S-001, CHG-R1S-026).** The sections "Gate and hosting" and "Block A size and embeddings" of Chinmay's answers log
> (the lead's working log of batch 1 onward), copied into git so the R1S change entries can cite it
> (`ticvai/CLAUDE.md` rule 12). Verbatim, followed by the lead's clarification relayed the same evening.
> It amends DEC-539 (no in-cell gpt-oss-120b fallback) and DEC-543 (the guard is the provider's safety
> service, not a self-hosted Qwen3Guard); DEC-542 (the offline Presidio scrubber) stands.

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
