#!/usr/bin/env python3
"""The AI engine tasks and DB-ROLES in docs/active/block-a-extra-tasks.json say what to build and when it is done.

**3 October 2026, CHG-TBF-006 and CHG-TBF-007** (Chinmay, Block A audit business rules, 3 October: "AI engine
tickets: What and done-when filled from docs/architecture/ai-system-design.md and the 2 Oct AI decisions; gaps
become questions later"). The Block A audit on live r2 found the AI engine tickets a line or two long with no
Done-when (AI-ENGINE-TRANSLATE: "proposeTranslations for CMS content, reviewed by the operator before
publishing"), so a developer pulling one through ADAM had nothing to finish against. Each text below is taken
from the AI system design (sections 3.3 to 3.13, 4.4, 5.8, 7) and the decisions of 2 October: the per-tenant AI
residency class with Core42 Compass the UAE-only default (ADR-0009 amended, DEC-539), the mandatory offline
scrubber and guard (ADR-0020 amended, DEC-542/543), BYOK of any provider (CHG-FUP-008) and the model choices of
docs/active/research/ai-ml-model-selection-2-october.md. DB-ROLES is filled from ADR-0055 and ADR-0020.

Only `detail` changes: subject, days, assignee, dependencies and app-module stay as planned. The engineer-days
come before "Done when", because the ticket's done-when line is everything after it (tools/op-release.py).

Idempotent: a second run says nothing to do. Run from anywhere: python3 tools/applied/ai-engine-tasks-3-october.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "docs" / "active" / "block-a-extra-tasks.json"

DETAIL = {
    "AI-ENGINE-GATEWAY": (
        "In ticvai-ai (Python). One gateway every AI call goes through: capability code calls gateway.run(task, "
        "inputs, schema?) and never names a provider (design 3.3). **Routing, in order:** (1) the allowed set: "
        "TICVAI's curated catalogue, filtered by the tenant's AI residency class (ADR-0009 amended 2 October, "
        "DEC-539): uaeOnly, the default and mandatory for government, bank and health tenants, resolves only to "
        "endpoints inside the UAE (Core42 Compass GPT-4.1 mini for the Small tier, Compass GPT-5 for the Strong "
        "tier, reached through the existing openaiCompatible provider kind); globalAllowed (a private venue under "
        "PDPL Art. 23) resolves to Azure gpt-5-mini / gpt-6-sol Global Standard or the tenant's BYOK provider; "
        "onPrem to the in-site open model; then by the task's data classification and the governance policy; (2) "
        "the task's tier from TICVAI's curated task-to-tier map: a client never picks a model. BYOK accepts any "
        "vendor (CHG-FUP-008), is enabled by TICVAI (PLATFORM_AI_MANAGE) for a globalAllowed tenant only, maps each "
        "task to that vendor's equivalent model, and is activated by setAiProvider only after testAiProvider's "
        "compatibility probes pass (tool calling, structured output, Arabic, context, latency, residency); the key "
        "is a per-tenant write-only Key Vault secret shown only by its last four characters; (3) the cascade, "
        "Small to Strong only on a checkable signal (schema validation failed twice, retrieval partial), never on "
        "a model's self-reported confidence; (4) a circuit breaker per endpoint (opens at 50% errors over 20 calls "
        "or p95 above twice the task budget for 60 s; half-open after 30 s) and the class's fallback chain (uaeOnly: "
        "OpenAI's UAE region, then the in-cell gpt-oss-120b); a residency refusal is returned, never failed over to "
        "another region; (5) degraded mode when nothing answers (search-only, rules-only or 'a person will help'). "
        "**Before each call:** the per-request budget and the capability's ceilingBehaviour, maskedFields (fail "
        "closed), then the scrubber and input guard of AI-ENGINE-SCRUB-GUARD, and a stable-first prompt order for "
        "prefix caching. **After it:** structured-output validation, the output guard and the re-fill, an "
        "ai.activity row and OpenTelemetry spans with no prompt text. evaluateAiGovernance is an in-process "
        "decision point (allow, allow with conditions, prepare only, approval required, escalate, block, with the "
        "policy version; design 3.8); getAiUsage meters tokens and spend per tenant; every governed answer writes "
        "one ai.decision_record (model, prompt template, policy and knowledge versions; design 3.9). About 12 "
        "engineer-days. Done when: a uaeOnly tenant's call reaches the Compass endpoint and, with Compass forced "
        "down, falls back to the OpenAI UAE endpoint and then the in-cell model and never to a Global endpoint (a "
        "test asserts the residency refusal instead of a cross-border call); a BYOK provider that fails a "
        "compatibility probe is refused with 409 compatibility-test-required; a tenant over its ceiling gets the "
        "capability's ceilingBehaviour; and every call in the test run leaves an ai.activity row, and every governed "
        "answer a decision record naming its model, prompt and policy versions."),
    "AI-ENGINE-SCRUB-GUARD": (
        "In ticvai-ai, self-hosted inside the cell for every residency class (ADR-0020 amended 2 October, "
        "DEC-542/543; contracts/satellite/ai.yaml AiPolicy.scrubbing, CHG-CSA-003). Between the gateway's "
        "maskedFields step and the provider: (1) detection with Microsoft Presidio (offline) and custom recognisers "
        "for Emirates ID numbers, UAE phone numbers, passport numbers, IBANs, Luhn-checked card numbers and email "
        "addresses, plus an Arabic named-entity model (CAMeL Tools or an Arabic GLiNER) for Arabic names and places; "
        "(2) reversible placeholders ([GUEST_1], [PHONE_1]) whose map lives in the cell for the life of the request "
        "only, is never logged and never travels with the prompt, and the reply re-filled before the user sees it; "
        "(3) Qwen3Guard on the prompt before it leaves and on the answer before it is shown (Qwen3Guard-Stream for "
        "streamed answers); (4) mandatory whatever the residency class: a uaeOnly tenant is scrubbed as well; (5) "
        "fails closed: scrubber or guard down means 503 scrubber-unavailable and no provider call; a guard refusal "
        "is 422 guard-refused. maskedFields stays the first control; the scrubber is the second, for free text. "
        "About 6 engineer-days. Done when: on a test corpus in Arabic and English, a prompt carrying an Emirates ID, "
        "a UAE phone number, an IBAN, a card number, an email and an Arabic name reaches the provider stub with "
        "placeholders only and no raw value, and the reply comes back re-filled; stopping the scrubber or the guard "
        "refuses the call with 503 and the provider stub receives nothing; a harmful prompt is refused with 422 "
        "guard-refused; and the corpus test runs in CI on every gateway change."),
    "AI-ENGINE-BASELINE": (
        "In ticvai-ai: the baseline-then-learn layer of design 3.13 (ADR-0051, AI-D16/AI-D17). **One estimator "
        "interface per question** (a suggestion kind, a forecast definition, a risk score, a recommendation rank) "
        "with three producers behind the same contract: the Prior (the venue AI profile from setAiVenueSettings, a "
        "starting pattern per venue type - water park, theme park, family entertainment centre, museum, arena, zoo "
        "or aquarium - written by TICVAI from published sources and never from another tenant's data, and the UAE "
        "calendar: Sat-Sun weekend, public holidays, Ramadan and Eid by Hijri date, school holidays, summer heat for "
        "outdoor venues); the Statistical producer, the tenant's own data pulled toward the prior, (k x prior + n x "
        "own mean) / (k + n) with k = coldStart.priorWeightObservations (4 same weekdays by default), re-estimated "
        "nightly as a recorded producer version; and the Learned slot, which only an admin's promotion fills (Block "
        "B). **Maturity on every answer:** AiMaturity (starting, learning, established, learned) on every Suggestion "
        "and AiForecastVersion and one ai.capability_maturity row per question, with the 'Based on' line (your venue "
        "profile, UAE calendar, 23 days of your sales), the share of own data and what the next stage needs. A 422 "
        "only for a missing setting (AiMissingSettingProblem names the setting and the screen that sets it), never "
        "for little history. The weather enters the prior with its Block B adapter. About 15 engineer-days; "
        "historical import, the training job and the learned producers continue in Block B. Done when: a new venue "
        "with no history gets an answer for every Block A suggestion kind on day one, with stage starting and a "
        "Based-on line; after 28 days of seeded sales the stage reads learning and the answer has moved toward the "
        "venue's own mean by the formula; a missing setting returns 422 naming it; and a two-tenant test shows no "
        "producer reads the other tenant's rows."),
    "AI-ENGINE-SUGGESTIONS": (
        "In ticvai-ai: requestSuggestion answers from the baseline (AI-ENGINE-BASELINE) on day one for the kinds the "
        "Block A screens call (BO-005 queueBalancing; GST-031 and WEB-044 waitTime and upsell, from the "
        "conversation only; prepPlan for the kitchen's production plan), with the upsell baseline from the "
        "Promotions relationship map plus business priority (design 3.10, ADR-0052), each answer "
        "carrying its maturity stage and Based-on line and recorded through the gateway's decision point. The "
        "recommendation runtime itself is Block B (ADR-0052). About 8 engineer-days. Done when: each of those "
        "screens gets a suggestion on a freshly seeded venue with no history, none answers 422 for little history, "
        "and every answer has a decision record naming its producer and stage."),
    "AI-ENGINE-CONCIERGE": (
        "In ticvai-ai: the guest concierge profile of the one assistant runtime (design 5.10). Knowledge ingest and "
        "reindex from the venue's published content into the tenant's Qdrant collection (AI-ENGINE-QDRANT), with "
        "embeddings and reranking self-hosted on CPU in the cell (BGE-M3 dense and sparse plus a multilingual "
        "cross-encoder; Qwen3-Embedding-0.6B and Qwen3-Reranker-0.6B are the candidates if they win the Arabic "
        "evaluation); hybrid retrieval through the single retrieval client (the venue filter always added); answers "
        "on the Small tier with sources, the venue's content as the only source, and a reliability category "
        "(grounded, partial, conflicting sources, insufficient evidence; design 5.6); the semantic then exact answer "
        "cache for FAQ-class answers keyed by tenant, scope path, locale and policy version (threshold 0.95, TTL "
        "60 minutes, never for live numbers; ADR-0034); streaming over sendAiMessage (tokens, then sources and any "
        "proposed action; the full message stored); degraded mode: the fallback model, then search-only answers "
        "with links, then 'a person will help' (design 3.7). Index lag over 15 minutes alerts (design 4.4). About 8 "
        "engineer-days. Done when: on the concierge golden set in English and Arabic groundedness and citation "
        "accuracy are each at least 95% (design 3.5); a question about another venue's content returns nothing from "
        "it; editing a source page invalidates its cached answer; and with the provider stubbed down the guest gets "
        "a search-only answer with links, not an error."),
    "AI-ENGINE-QDRANT": (
        "In ticvai-ai, on SETUP-QDRANT's cluster (ADR-0049, design 5.8). Collection-per-tenant provisioning at tenant "
        "onboarding, per embedding model (t_<tenantId>_<model>) behind the alias tenant_<tenantId> (a model change is "
        "a shadow collection, an evaluation and an alias swap); per-tenant HS256 JWT issuance and rotation, scoped to "
        "the tenant's collections and alias, signed with the admin API key that only the issuer reads from Key Vault "
        "(ticvai-ai never does); the single retrieval client with no scope parameter that reads the caller's scope "
        "from the request and always adds the venue filter (points carry venue_id and scope_path, indexed); dense "
        "and sparse named vectors fused by reciprocal rank; erasure by guest or document payload, checked against "
        "the point references in ai.chunk_embedding; offboarding that deletes the collections and alias and revokes "
        "the token; per-collection snapshots copied to UAE North storage by a CronJob (azcopy, workload identity) "
        "and a restore tested per tenant. About 5 engineer-days. Done when: a token for one tenant cannot read "
        "another tenant's collection (the store refuses it); a collection-scoped token works through the alias, or "
        "the token names both; a venue-scoped question never returns another venue's chunk; an erased guest's "
        "points are gone and the check against ai.chunk_embedding proves it; and one tenant's snapshot restores "
        "into a fresh collection."),
    "AI-ENGINE-GUIDED": (
        "In ticvai-ai: Help me choose suggested from the catalogue (design 3.11, decided 29 September; capability "
        "C7 at autonomy 'suggest'). Rules first: read each guest-sellable product's category, subcategory, segment "
        "tags (level, audience), minimum height and age, duration, price band and language through the catalogue "
        "API with the venue's permissions; pick the one or two attributes that split the products most evenly, "
        "dropping any where one answer leaves nothing bookable (deterministic: the same catalogue gives the same "
        "questions); map each answer to a product, a category or a flow. The Small tier writes the question, answer "
        "titles and one-liners in the tenant's languages from the attributes only, never guest data; with the model "
        "unavailable the attribute names are used as they are. The draft is saved through proposeGuidedChoice "
        "(source aiSuggested, suggestionRef) with a decision record of the inputs, the split each question makes and "
        "the model and prompt versions. Publishing is publishGuidedChoice by a person holding TENANT_PUBLISH; "
        "nothing is published automatically. A withdrawn mapped product, or new products no answer reaches, raise a "
        "new suggestion and never rewrite the published version. About 4 engineer-days. Done when: the same "
        "catalogue run twice gives the same questions; the draft lands with source aiSuggested and a decision "
        "record; with the model stubbed down a usable draft still lands with attribute names; nothing is live until "
        "a person publishes; and withdrawing a mapped product raises a new suggestion."),
    "AI-ENGINE-TRANSLATE": (
        "In ticvai-ai: proposeTranslations for CMS content, English to Arabic and Arabic to English (and the other "
        "locales a tenant enables), on the Small tier with the tenant glossary in the cached prompt prefix so brand "
        "terms and register hold (research T03); placeholders, markup and links preserved; scrubbed and guarded like "
        "every call (AI-ENGINE-SCRUB-GUARD). The result is an AI draft on the field until an operator saves it, and "
        "is never published automatically. With the model unavailable the field is left blank and marked missing, "
        "never filled with the source text. About 3 engineer-days. Done when: an English CMS page gets an Arabic "
        "draft that keeps every glossary term and placeholder; the draft stays a draft until an operator saves it; "
        "and with the provider stubbed down the field reads missing, not English."),
    "AI-ENGINE-PLANNER": (
        "In ticvai-ai: the planner agent on top of the rules planner in venue-map (design 2.3 and 7; MOB-6). The "
        "schedule is solved deterministically (OR-Tools CP-SAT over show times, opening hours, walking times and "
        "configured capacity; research T04) and the Small tier reads the guest's intent and writes the why. The "
        "agent works only through the plan operations as the guest (the itinerary kind of requestSuggestion and its "
        "plan tools), never writes venuemap.visit_plan itself, and is grounded in each day's venue: it proposes only "
        "what that day's tools return, and a wish the venue cannot meet is answered from "
        "VisitPlan.unmatchedPreferences. When AI is off or fails it falls back to the rules plan, never to an error. "
        "About 8 engineer-days. Done when: a refinement in chat (add lunch at one, skip the coasters) produces a "
        "valid plan through the plan tools that respects show times and capacity; a request for something at "
        "another venue is answered from unmatchedPreferences and updateVisitPlan refuses the point (422 "
        "point-not-at-day-venue); and with the model stubbed down the guest gets the rules plan."),
    "AI-ENGINE-EVAL": (
        "In ticvai-ai: the evaluation harness and release pipeline of design 3.5. Golden sets per capability in the "
        "repository (Arabic, English and code-mixed cases, plus permission and tenant-isolation cases such as 'show "
        "revenue for another tenant'), run by runAiEvaluation; isolation and permission cases must pass 100% and a "
        "single failure blocks the release. Scores land in AiModel.taskFitness with the task's band; a model bound "
        "outside it returns fitnessWarnings on setAiProvider (warn, never block; AI-D18). The Arabic golden set "
        "decides between Compass GPT-4.1 mini and GPT-4.1 Arabic (Seraj) for the uaeOnly Small tier (ADR-0009 "
        "amended), and a BYOK vendor's model enters the curated map only after passing the task's set. Release "
        "stages draft, offline evaluation, shadow, canary, production, with rollback as a pointer switch; the "
        "backtest runner the learned producers will use; and a shadow producer that passes its promotion gate "
        "raises one ai.governance_alert of kind promotionReady and a P09 tile, and never switches itself (AI-D16). "
        "About 5 engineer-days. Done when: CI runs the harness on every Block A AI answer type (concierge, Help me "
        "choose wording, translations, planner, day-one suggestions) and blocks a merge on any isolation failure or "
        "a regression against the previous release; a model scored outside its band returns fitnessWarnings; and a "
        "seeded shadow producer that passes its gate raises exactly one promotionReady alert and changes nothing "
        "live."),
    "DB-ROLES": (
        "In ticvai-backend, created by the baseline migration (MIG-BASELINE), one PostgreSQL login role per "
        "deployable of ADR-0055: commerce, access, operations, workers and ticvai_ai, each reading its password or "
        "token from the cell's Key Vault. Each role gets USAGE and SELECT, INSERT, UPDATE, DELETE on the schemas its "
        "modules own (the schema owners in handoff/service-decomposition.json; workers runs every module's "
        "consumers, the outbox relay and the scheduled jobs, so it gets the schemas those touch), SELECT on the "
        "published read views of DB-READ-VIEWS, and nothing else: no CREATE, no ownership, no BYPASSRLS, so FORCE "
        "row-level security applies to every host. ticvai_ai writes only the ai schema (and ai.inbox; ADR-0058) and "
        "is read-only on the transactional schemas (ADR-0020). The tables are owned by a separate migration role "
        "that only SqlMigrationRunner uses. Done when: each host connects with its own role from Key Vault; an "
        "INSERT from the ticvai_ai role into a transactional table, and from the commerce role into an operations "
        "schema (fnb), are each refused by PostgreSQL; no host role has BYPASSRLS or owns a table (a query on "
        "pg_roles and pg_tables in CI shows it); and a host role with no scope set on its session reads no rows from "
        "a table under FORCE row-level security."),
}


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    doc = json.loads(text)
    changed = []
    for t in doc["tasks"]:
        new = DETAIL.get(t["key"])
        if new and t.get("detail") != new:
            t["detail"] = new
            changed.append(t["key"])
    missing = sorted(set(DETAIL) - {t["key"] for t in doc["tasks"]})
    if missing:
        print("not in the file:", ", ".join(missing))
        return 1
    if not changed:
        print("nothing to do")
        return 0
    PATH.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(changed)} task text(s) written: {', '.join(changed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
