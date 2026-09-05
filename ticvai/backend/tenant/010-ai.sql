-- ai — 16 tables
-- **Derived. Do not hand-edit.**

-- Maps a Qdrant point id back to its document and scope. The join between the two stores Hangs
-- off: reaches ai.index_source through its keys; references ai.knowledge_document. Reached by: 6
-- operations read it and 0 write it
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
    scope_path                        text,
    module                            text NOT NULL,
    locale                            text,
    message_count                     integer,
    started_at                        timestamptz NOT NULL,
    last_message_at                   timestamptz
);

-- Maps a source row to its Qdrant point ids, so a deletion in Postgres can be followed into the
-- vector store. Nothing cascades between the two Hangs off: reaches ai.index_source through its
-- keys; references ai.index_source. Reached by: 1 operations read it and 2 write it
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
    stage                             text,
    error                             text,
    attempts                          integer,
    created_at                        timestamptz
);

-- A build in flight. recordsFailed is the number to watch — a source failing on 3% of rows is a
-- search missing 3% of answers Hangs off: reaches ai.index_source through its keys; references
-- ai.index_source. Reached by: 2 operations read it and 1 write it
CREATE TABLE IF NOT EXISTS ai.index_job (
    id                                uuid PRIMARY KEY NOT NULL,
    source_id                         uuid NOT NULL,
    kind                              text,
    reason                            text,
    status                            text NOT NULL,
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
-- schema; references ai.knowledge_collection. Reached by: 3 operations read it and 1 write it; 5
-- tables reference it
CREATE TABLE IF NOT EXISTS ai.index_source (
    id                                uuid PRIMARY KEY,
    "table"                           text NOT NULL,
    contract                          text,
    text_fields                       text[] NOT NULL,
    payload_fields                    text[],
    collection                        text NOT NULL,
    scope_level                       text NOT NULL,
    invalidated_by                    text[],
    chunk_strategy                    text,
    parent_field                      text,
    is_active                         boolean,
    entry_count                       integer,
    last_indexed_at                   timestamptz,
    stale_count                       integer,
    collection_id                     uuid NOT NULL
);

-- The audit record. Retention is unresolved (CF-64) — a prompt may carry personal data. Analytical
-- store, not the transactional primary (ADR-0020) — append-only with an analytical read pattern,
-- and it must not compete with a gate scan for a connection
CREATE TABLE IF NOT EXISTS ai.interaction (
    id                                uuid PRIMARY KEY NOT NULL,
    conversation_id                   uuid,
    principal_id                      uuid NOT NULL,
    audience                          text,
    subject_id                        uuid,
    billable_to_tenant_id             uuid,
    scope_path                        text,
    capability                        text NOT NULL,
    prompt                            text,
    response                          text,
    outcome                           text NOT NULL,
    refusal_reason                    text,
    provider                          text,
    model                             text,
    prompt_tokens                     integer,
    completion_tokens                 integer,
    cost_minor                        integer,
    latency_ms                        integer,
    masked_field_count                integer,
    trace_id                          text,
    created_at                        timestamptz NOT NULL
);

-- A collection in the vector store. One per embedding model — a collection carries its own vector
-- config and a shard cannot, so two models cannot share one (ADR-0021). Carries the shard key,
-- which is the tenant boundary on shared placement Hangs off: reaches ai.index_source through its
-- keys. Reached by: 4 operations read it and 1 write it; 2 tables reference it
CREATE TABLE IF NOT EXISTS ai.knowledge_collection (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL,
    description                       text,
    scope_level                       text NOT NULL,
    scope_path                        text,
    document_count                    integer,
    shard_key                         text,
    retrieval                         text,
    sparse_model                      text,
    idf_scope                         text,
    embedding_model                   text,
    is_active                         boolean
);

-- Source, status and chunk count. The text and its vectors live in Qdrant Hangs off: reaches
-- ai.index_source through its keys; references ai.knowledge_collection, maintenance.asset. Reached
-- by: 3 operations read it and 1 write it; 1 tables reference it
CREATE TABLE IF NOT EXISTS ai.knowledge_document (
    id                                uuid PRIMARY KEY,
    collection_id                     uuid,
    title                             text NOT NULL,
    source_asset_id                   uuid NOT NULL,
    mime_type                         text,
    status                            text,
    chunk_count                       integer,
    failure_reason                    text,
    indexed_at                        timestamptz
);

-- A generated seat layout awaiting review. Ends at previewReady and writes nothing to the seat map
-- — the draft enters seating.import_job at its existing human commit step (ADR-0020) Hangs off:
-- reaches ai.index_source through its keys; references assets.media_asset, venuemap.import_job.
-- Reached by: 0 operations read it and 1 write it
CREATE TABLE IF NOT EXISTS ai.layout_draft (
    id                                uuid PRIMARY KEY,
    import_job_id                     uuid NOT NULL,
    status                            text NOT NULL,
    seat_count                        integer,
    section_count                     integer,
    categories_proposed               text[],
    unresolved                        text[],
    trace_id                          text,
    scope_path                        text,
    asset_id                          uuid NOT NULL
);

-- Prompt and response with sources, provider, model, tokens and latency. Analytical store, not the
-- transactional primary (ADR-0020) — append-only with an analytical read pattern, and it must not
-- compete with a gate scan for a connection
CREATE TABLE IF NOT EXISTS ai.message (
    id                                uuid PRIMARY KEY NOT NULL,
    conversation_id                   uuid NOT NULL,
    role                              text NOT NULL,
    content                           text NOT NULL,
    confidence                        numeric(18,4),
    rationale                         text,
    proposed_action                   uuid,
    trace_id                          text,
    provider                          text,
    model                             text,
    prompt_tokens                     integer,
    completion_tokens                 integer,
    latency_ms                        integer,
    created_at                        timestamptz NOT NULL
);

-- What the assistant may do, which roles may use it, what is masked. Resolves tenant then venue
-- (ADR-0018) Hangs off: reaches ai.index_source through its keys; references platform.tenant.
-- Reached by: 12 operations read it and 2 write it
CREATE TABLE IF NOT EXISTS ai.policy (
    id                                uuid PRIMARY KEY,
    scope_level                       text NOT NULL,
    enabled_capabilities              text[] NOT NULL,
    allowed_role_ids                  text[],
    masked_fields                     text[],
    requires_approval_for             text[],
    monthly_token_ceiling             integer,
    ceiling_behaviour                 text,
    ceiling_warning_percent           integer,
    guest_capability_scope            text[],
    retrieve_top_k                    integer,
    rerank_top_k                      integer,
    cache_answers                     boolean,
    cache_ttl_minutes                 integer,
    retain_interactions_days          integer,
    semantic_cache_threshold          numeric(18,4),
    negative_cache_ttl_seconds        integer,
    cascade                           jsonb,
    chunking                          jsonb,
    quantisation                      text,
    hnsw                              jsonb,
    per_request_token_ceiling         integer,
    streams_by_capability             text[],
    fallback_provider_id              uuid,
    guardrail_short_circuit           boolean,
    tenant_id                         uuid NOT NULL
);

-- A draft the assistant produced and a person must approve. Nothing executes from here Hangs off:
-- reaches ai.index_source through its keys; references ai.interaction, identity.principal. Reached
-- by: 5 operations read it and 6 write it; 1 tables reference it
CREATE TABLE IF NOT EXISTS ai.proposed_action (
    id                                uuid PRIMARY KEY NOT NULL,
    interaction_id                    uuid,
    kind                              text NOT NULL,
    target_contract                   text NOT NULL,
    target_operation                  text NOT NULL,
    payload                           jsonb NOT NULL,
    summary                           text,
    status                            text NOT NULL,
    approval_level                    integer,
    decided_by_principal_id           uuid,
    decision_reason                   text,
    proposed_at                       timestamptz,
    decided_at                        timestamptz
);

-- Configured providers, models and failover order. Credentials are a vault reference, never a key
-- Hangs off: reaches ai.index_source through its keys; references ai.provider, control.tenant,
-- platform.org_unit. Reached by: 14 operations read it and 3 write it; 5 tables reference it
CREATE TABLE IF NOT EXISTS ai.provider (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL,
    capability                        text NOT NULL,
    model                             text,
    failover_provider_id              uuid,
    degrade_gracefully                boolean,
    priority                          integer NOT NULL,
    scope_level                       text,
    scope_path                        text,
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
-- reference it
CREATE TABLE IF NOT EXISTS ai.suggestion (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL,
    basis                             text NOT NULL,
    scope_path                        text,
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
-- by: 0 operations read it a
CREATE TABLE IF NOT EXISTS ai.suggestion_outcome (
    id                                uuid PRIMARY KEY NOT NULL,
    suggestion_id                     uuid NOT NULL,
    decision                          text NOT NULL,
    actual_value                      jsonb,
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    realised_outcome                  jsonb,
    note                              text
);

