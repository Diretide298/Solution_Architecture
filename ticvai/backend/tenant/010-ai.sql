-- ai — 16 tables
-- **Derived. Do not hand-edit.**

-- The audit record. Retention is unresolved (CF-64) — a prompt may carry personal data. Analytical
-- store, not the transactional primary (ADR-0020) — append-only with an analytical read pattern,
-- and it must not compete with a gate scan for a connection
CREATE TABLE IF NOT EXISTS ai.activity (
    id                                uuid PRIMARY KEY NOT NULL,
    conversation_id                   uuid,
    principal_id                      uuid NOT NULL,
    audience                          text CONSTRAINT activity_audience_chk CHECK (audience IN ('staff', 'guest')),
    subject_id                        uuid,
    billable_to_tenant_id             uuid,
    scope_path                        ltree NOT NULL,
    capability                        text NOT NULL,
    prompt                            text,
    response                          text,
    sources                           jsonb,
    outcome                           text NOT NULL CONSTRAINT activity_outcome_chk CHECK (outcome IN ('answered', 'refused', 'applied', 'rejected', 'failed')),
    refusal_reason                    text,
    provider                          text CONSTRAINT activity_provider_chk CHECK (provider IN ('openai', 'gemini', 'anthropic', 'azureOpenai', 'localLlm')),
    model                             text,
    prompt_tokens                     integer,
    completion_tokens                 integer,
    cost_amount                       numeric(18,4),
    latency_ms                        integer,
    masked_field_count                integer,
    trace_id                          text,
    created_at                        timestamptz NOT NULL
);

-- Maps a Qdrant point id back to its document and scope. The join between the two stores Hangs
-- off: reaches ai.index_source through its keys; references ai.knowledge_document. Reached by: 6
-- operations read it and 0 write it.
CREATE TABLE IF NOT EXISTS ai.chunk_ref (
    id                                uuid PRIMARY KEY NOT NULL,
    document_id                       uuid NOT NULL
);

-- A thread, scoped to a principal and a module. Analytical store, not the transactional primary
-- (ADR-0020) — append-only with an analytical read pattern, and it must not compete with a gate
-- scan for a connection
CREATE TABLE IF NOT EXISTS ai.conversation (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    module                            text NOT NULL CONSTRAINT conversation_module_chk CHECK (module IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai')),
    locale                            text,
    message_count                     integer,
    started_at                        timestamptz NOT NULL,
    last_message_at                   timestamptz
);

-- Maps a source row to its Qdrant point ids, so a deletion in Postgres can be followed into the
-- vector store. Nothing cascades between the two Hangs off: reaches ai.index_source through its
-- keys; references ai.index_source. Reached by: 1 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS ai.index_entry (
    id                                uuid PRIMARY KEY NOT NULL,
    source_id                         uuid NOT NULL
);

-- A document that would not chunk, embed or parse. ai.index_job counts records_failed and holds a
-- failure_sample; this is where the other 4,999 go. stage decides who fixes it — a parse failure
-- is a document problem, an embed failure is a provider one
CREATE TABLE IF NOT EXISTS ai.index_failure (
    id                                uuid PRIMARY KEY NOT NULL,
    job_id                            uuid,
    source_id                         uuid,
    document_ref                      text,
    stage                             text CONSTRAINT index_failure_stage_chk CHECK (stage IN ('fetch', 'parse', 'chunk', 'embed', 'upsert')),
    error                             text,
    attempts                          integer,
    created_at                        timestamptz
);

-- A build in flight. recordsFailed is the number to watch — a source failing on 3% of rows is a
-- search missing 3% of answers Hangs off: reaches ai.index_source through its keys; references
-- ai.index_source. Reached by: 3 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS ai.index_job (
    id                                uuid PRIMARY KEY NOT NULL,
    source_id                         uuid NOT NULL,
    kind                              text CONSTRAINT index_job_kind_chk CHECK (kind IN ('full', 'incremental', 'removal')),
    reason                            text,
    status                            text NOT NULL CONSTRAINT index_job_status_chk CHECK (status IN ('queued', 'building', 'verifying', 'swapping', 'complete', 'failed')),
    records_total                     integer,
    records_embedded                  integer,
    records_failed                    integer,
    failure_sample                    text[],
    shadow_collection                 text,
    shard_key                         text,
    embedding_model                   text,
    started_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- One declaration per indexed table. The owning service does not know it exists — the AI service
-- consumes the event that service already publishes Hangs off: a root — nothing above it in its
-- schema; references ai.knowledge_collection. Reached by: 3 operations read it and 1 write it; 3
-- tables reference it.
CREATE TABLE IF NOT EXISTS ai.index_source (
    id                                uuid PRIMARY KEY,
    table_name                        text NOT NULL,
    contract                          text,
    text_fields                       text[] NOT NULL,
    payload_fields                    text[],
    collection                        text NOT NULL,
    scope_level                       text NOT NULL CONSTRAINT index_source_scope_level_chk CHECK (scope_level IN ('tenant', 'region', 'venue')),
    invalidated_by                    text[],
    chunk_strategy                    text CONSTRAINT index_source_chunk_strategy_chk CHECK (chunk_strategy IN ('wholeRecord', 'paragraph', 'fixedTokens', 'section', 'semanticSection', 'parentChild')),
    parent_field                      text,
    is_active                         boolean,
    entry_count                       integer,
    last_indexed_at                   timestamptz,
    stale_count                       integer,
    collection_id                     uuid NOT NULL
);

-- A collection in the vector store. One per embedding model — a collection carries its own vector
-- config and a shard cannot, so two models cannot share one (ADR-0021). Carries the shard key,
-- which is the tenant boundary on shared placement Hangs off: reaches ai.index_source through its
-- keys. Reached by: 4 operations read it and 1 write it; 2 tables reference it.
CREATE TABLE IF NOT EXISTS ai.knowledge_collection (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL,
    description                       text,
    scope_level                       text NOT NULL CONSTRAINT knowledge_collection_scope_level_chk CHECK (scope_level IN ('tenant', 'region', 'venue')),
    scope_path                        ltree NOT NULL,
    document_count                    integer,
    shard_key                         text,
    retrieval                         text DEFAULT 'hybrid' CONSTRAINT knowledge_collection_retrieval_chk CHECK (retrieval IN ('dense', 'hybrid')),
    sparse_model                      text,
    idf_scope                         text DEFAULT 'tenant' CONSTRAINT knowledge_collection_idf_scope_chk CHECK (idf_scope IN ('shard', 'tenant', 'venue')),
    embedding_model                   text,
    is_active                         boolean
);

-- Source, status and chunk count. The text and its vectors live in Qdrant Hangs off: reaches
-- ai.index_source through its keys; references ai.knowledge_collection, ai.knowledge_document.
-- Reached by: 3 operations read it and 1 write it; 2 tables reference it.
CREATE TABLE IF NOT EXISTS ai.knowledge_document (
    id                                uuid PRIMARY KEY,
    collection_id                     uuid,
    title                             text NOT NULL,
    source_asset_id                   uuid NOT NULL,
    mime_type                         text,
    supersedes_document_id            uuid,
    status                            text CONSTRAINT knowledge_document_status_chk CHECK (status IN ('processing', 'indexed', 'failed', 'superseded')),
    chunk_count                       integer,
    failure_reason                    text,
    indexed_at                        timestamptz
);

-- A generated seat layout awaiting review. Ends at previewReady and writes nothing to the seat map
-- — the draft enters seating.import_job at its existing human commit step (ADR-0020) Hangs off:
-- reaches ai.index_source through its keys; references assets.media_asset. Reached by: 1
-- operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS ai.layout_draft (
    id                                uuid PRIMARY KEY,
    import_job_id                     uuid NOT NULL,
    status                            text NOT NULL CONSTRAINT layout_draft_status_chk CHECK (status IN ('parsing', 'previewReady', 'failed')),
    seat_count                        integer,
    section_count                     integer,
    categories_proposed               text[],
    unresolved                        text[],
    trace_id                          text,
    scope_path                        ltree NOT NULL,
    asset_id                          uuid NOT NULL
);

-- Prompt and response with sources, provider, model, tokens and latency. Analytical store, not the
-- transactional primary (ADR-0020) — append-only with an analytical read pattern, and it must not
-- compete with a gate scan for a connection
CREATE TABLE IF NOT EXISTS ai.message (
    id                                uuid PRIMARY KEY NOT NULL,
    conversation_id                   uuid NOT NULL,
    role                              text NOT NULL CONSTRAINT message_role_chk CHECK (role IN ('user', 'assistant', 'system')),
    content                           text NOT NULL,
    sources                           jsonb,
    confidence                        numeric(18,4),
    rationale                         text,
    proposed_action_id                uuid,
    trace_id                          text,
    provider                          text CONSTRAINT message_provider_chk CHECK (provider IN ('openai', 'gemini', 'anthropic', 'azureOpenai', 'localLlm')),
    model                             text,
    prompt_tokens                     integer,
    completion_tokens                 integer,
    latency_ms                        integer,
    created_at                        timestamptz NOT NULL
);

-- What the assistant may do, which roles may use it, what is masked. Resolves tenant then venue
-- (ADR-0018) Hangs off: reaches ai.index_source through its keys; references ai.provider,
-- platform.tenant. Reached by: 12 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS ai.policy (
    id                                uuid PRIMARY KEY,
    scope_level                       text NOT NULL CONSTRAINT policy_scope_level_chk CHECK (scope_level IN ('tenant', 'venue')),
    scope_path                        ltree NOT NULL,
    enabled_capabilities              text[] NOT NULL,
    allowed_role_ids                  text[],
    masked_fields                     text[],
    requires_approval_for             text[],
    monthly_token_ceiling             integer,
    ceiling_behaviour                 text DEFAULT 'warn' CONSTRAINT policy_ceiling_behaviour_chk CHECK (ceiling_behaviour IN ('warn', 'warnThenDisable', 'block')),
    ceiling_warning_percent           integer DEFAULT 80,
    guest_capability_scope            text[],
    retrieve_top_k                    integer DEFAULT 30,
    rerank_top_k                      integer DEFAULT 5,
    cache_answers                     boolean DEFAULT true,
    cache_ttl_minutes                 integer DEFAULT 60,
    retain_interactions_days          integer,
    semantic_cache_threshold          numeric(18,4) DEFAULT 0.95,
    negative_cache_ttl_seconds        integer DEFAULT 300,
    cascade                           jsonb,
    chunking                          jsonb,
    quantisation                      text DEFAULT 'none' CONSTRAINT policy_quantisation_chk CHECK (quantisation IN ('none', 'scalar', 'binary')),
    hnsw                              jsonb,
    per_request_token_ceiling         integer,
    streams_by_capability             text[],
    fallback_provider_id              uuid,
    guardrail_short_circuit           boolean DEFAULT true,
    suggestion_providers              jsonb,
    tenant_id                         uuid NOT NULL
);

-- A draft the assistant produced and a person must approve. Nothing executes from here Hangs off:
-- reaches ai.index_source through its keys; references ai.activity, identity.principal. Reached
-- by: 5 operations read it and 6 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS ai.proposed_action (
    id                                uuid PRIMARY KEY NOT NULL,
    interaction_id                    uuid,
    kind                              text NOT NULL CONSTRAINT proposed_action_kind_chk CHECK (kind IN ('pricing', 'promotion', 'operational', 'financial', 'configuration')),
    target_contract                   text NOT NULL,
    target_operation                  text NOT NULL,
    payload                           jsonb NOT NULL,
    summary                           text,
    status                            text NOT NULL CONSTRAINT proposed_action_status_chk CHECK (status IN ('proposed', 'approved', 'rejected', 'applied', 'expired')),
    expires_at                        timestamptz,
    approval_level                    integer,
    decided_by_principal_id           uuid,
    decision_reason                   text,
    proposed_at                       timestamptz,
    decided_at                        timestamptz
);

-- Configured providers, models and failover order. Credentials are a vault reference, never a key
-- Hangs off: reaches ai.index_source through its keys; references ai.provider, platform.scope,
-- platform.tenant. Reached by: 14 operations read it and 3 write it; 2 tables reference it.
CREATE TABLE IF NOT EXISTS ai.provider (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL CONSTRAINT provider_kind_chk CHECK (kind IN ('openai', 'gemini', 'anthropic', 'azureOpenai', 'localLlm')),
    capability                        text NOT NULL CONSTRAINT provider_capability_chk CHECK (capability IN ('chat', 'embedding', 'vision', 'rerank', 'speechToText', 'textToSpeech')),
    model                             text,
    failover_provider_id              uuid,
    degrade_gracefully                boolean DEFAULT true,
    priority                          integer NOT NULL,
    scope_level                       text CONSTRAINT provider_scope_level_chk CHECK (scope_level IN ('platform', 'tenant', 'venue')),
    scope_path                        ltree NOT NULL,
    tenant_id                         uuid,
    credential_ref                    text,
    credential_rotated_at             timestamptz,
    credential_expires_at             timestamptz,
    last_verified_at                  timestamptz,
    endpoint                          text,
    residency                         text,
    max_tokens                        integer,
    is_active                         boolean NOT NULL,
    region_id                         uuid NOT NULL
);

-- One answer to one question, with its basis and its reasoning (24 August). Built so machine
-- learning can be swapped in without touching a screen — a heuristic today, a model when there is
-- data, and the frontend never changes. A suggestion is never an action. Hangs off: reaches
-- ai.index_source through its keys. Reached by: 3 operations read it and 1 write it; 2 tables
-- reference it.
CREATE TABLE IF NOT EXISTS ai.suggestion (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT suggestion_kind_chk CHECK (kind IN ('price', 'replenishment', 'requisition', 'demandForecast', 'prepPlan', 'menuEngineering', 'staffing', 'slaTarget', 'waitTime', 'upsell', 'segmentation', 'anomaly', 'scenario')),
    basis                             text NOT NULL CONSTRAINT suggestion_basis_chk CHECK (basis IN ('heuristic', 'statistical', 'model', 'hybrid', 'manual')),
    scope_path                        ltree NOT NULL,
    subject_ref                       text,
    value                             jsonb,
    confidence                        numeric(18,4),
    explanation                       text,
    inputs                            jsonb,
    producer_ref                      text,
    produced_at                       timestamptz NOT NULL,
    expires_at                        timestamptz
);

-- What the venue actually did. The table that makes the swap possible at all — a model needs
-- labelled data and the only source of labels is whether the advice was taken and whether it
-- worked. A rejected suggestion is the more valuable record. Hangs off: a child of ai.suggestion;
-- reaches ai.index_source through its keys; references ai.suggestion, identity.principal. Reached
-- by: 1 operations read it a
CREATE TABLE IF NOT EXISTS ai.suggestion_outcome (
    id                                uuid PRIMARY KEY NOT NULL,
    suggestion_id                     uuid NOT NULL,
    decision                          text NOT NULL CONSTRAINT suggestion_outcome_decision_chk CHECK (decision IN ('accepted', 'modified', 'rejected', 'ignored', 'expired')),
    actual_value                      jsonb,
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    realised_outcome                  jsonb,
    note                              text
);

