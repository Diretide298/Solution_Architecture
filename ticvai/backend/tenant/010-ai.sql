-- ai — 75 tables
-- **Derived. Do not hand-edit.**

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.action_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    origin                            text NOT NULL CONSTRAINT action_plan_origin_chk CHECK (origin IN ('configurationSession', 'generateConfiguration', 'assistant', 'riskCase', 'operationalRequirement', 'rollback')),
    origin_ref                        text,
    summary                           text,
    status                            text NOT NULL CONSTRAINT action_plan_status_chk CHECK (status IN ('draft', 'validated', 'simulated', 'awaitingApproval', 'approved', 'executing', 'paused', 'completed', 'partiallyCompleted', 'failed', 'compensated', 'cancelled', 'rolledBack')),
    autonomy_level                    jsonb,
    approval_tier                     integer,
    approval_request_id               uuid,
    proposed_action_id                uuid,
    change_set_hash                   text,
    governance_outcome                text,
    policy_version_ref                text,
    simulation                        jsonb,
    is_partial_completion_allowed     boolean DEFAULT false,
    rollback_of_plan_id               uuid,
    requested_by_principal_id         uuid,
    created_at                        timestamptz,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 21 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.action_step (
    id                                uuid PRIMARY KEY NOT NULL,
    plan_id                           uuid NOT NULL,
    step_number                       integer NOT NULL,
    depends_on                        integer[],
    tool_key                          text NOT NULL,
    target_contract                   text NOT NULL,
    target_operation                  text NOT NULL,
    contract_version                  text,
    payload                           jsonb,
    provenance                        text CONSTRAINT action_step_provenance_chk CHECK (provenance IN ('confirmed', 'aiRecommended', 'inferred', 'unknown')),
    idempotency_key                   text,
    target_object_ref                 text,
    target_object_version             text,
    is_reversible                     boolean,
    compensation                      jsonb,
    status                            text NOT NULL CONSTRAINT action_step_status_chk CHECK (status IN ('pending', 'validated', 'running', 'succeeded', 'failed', 'compensated', 'skipped', 'paused')),
    attempts                          integer,
    last_error                        text,
    result_ref                        text,
    started_at                        timestamptz,
    completed_at                      timestamptz
);

-- The audit record. Retention is unresolved (CF-64) — a prompt may carry personal data. Analytical
-- store, not the transactional primary (ADR-0020) — append-only with an analytical read pattern,
-- and it must not compete with a gate scan for a connection
CREATE TABLE IF NOT EXISTS ai.activity (
    scrub_audit                       jsonb,
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
    provider                          text CONSTRAINT activity_provider_chk CHECK (provider IN ('openai', 'gemini', 'anthropic', 'azureOpenai', 'localLlm', 'openaiCompatible')),
    model                             text,
    prompt_tokens                     integer,
    completion_tokens                 integer,
    cost_amount                       numeric(18,4),
    latency_ms                        integer,
    masked_field_count                integer,
    trace_id                          text,
    decision_record_id                uuid,
    cache_layer                       text CONSTRAINT activity_cache_layer_chk CHECK (cache_layer IN ('guardrail', 'semantic', 'exact', 'negative', 'analytics')),
    created_at                        timestamptz NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.anomaly_detector (
    id                                uuid PRIMARY KEY NOT NULL,
    detector_key                      text NOT NULL,
    source                            text DEFAULT 'metric' CONSTRAINT anomaly_detector_source_chk CHECK (source IN ('metric', 'forecast', 'deviceHealth')),
    metric_key                        text,
    forecast_source                   jsonb,
    device_health_source              jsonb,
    method                            text NOT NULL CONSTRAINT anomaly_detector_method_chk CHECK (method IN ('threshold', 'seasonalRobustZ', 'peerComparison', 'model')),
    thresholds                        jsonb,
    sensitivity                       text DEFAULT 'medium' CONSTRAINT anomaly_detector_sensitivity_chk CHECK (sensitivity IN ('low', 'medium', 'high')),
    dimensions                        text[],
    cadence                           text CONSTRAINT anomaly_detector_cadence_chk CHECK (cadence IN ('hourly', 'daily')),
    is_active                         boolean DEFAULT true,
    false_alarm_rate                  numeric(18,4),
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.answer_feedback (
    id                                uuid PRIMARY KEY NOT NULL,
    message_id                        uuid NOT NULL,
    conversation_id                   uuid,
    rating                            text NOT NULL CONSTRAINT answer_feedback_rating_chk CHECK (rating IN ('helpful', 'notHelpful')),
    reason                            text CONSTRAINT answer_feedback_reason_chk CHECK (reason IN ('wrong', 'outdated', 'incomplete', 'notGrounded', 'unsafe', 'other')),
    comment                           text CONSTRAINT answer_feedback_comment_chk CHECK (char_length(comment) <= 1000),
    audience                          text CONSTRAINT answer_feedback_audience_chk CHECK (audience IN ('staff', 'guest')),
    principal_id                      uuid,
    subject_id                        uuid,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.approval_request_score (
    id                                uuid PRIMARY KEY NOT NULL,
    approval_request_id               uuid NOT NULL,
    trigger                           text CONSTRAINT approval_request_score_trigger_chk CHECK (trigger IN ('submitted', 'resubmitted', 'slaTick', 'escalated')),
    risk_score                        integer NOT NULL,
    risk_band                         text NOT NULL CONSTRAINT approval_request_score_risk_band_chk CHECK (risk_band IN ('low', 'medium', 'high', 'critical')),
    priority_score                    integer NOT NULL,
    escalation_suggestion             jsonb NOT NULL,
    basis                             text CONSTRAINT approval_request_score_basis_chk CHECK (basis IN ('heuristic', 'statistical', 'model', 'hybrid', 'manual')),
    decision_record_id                uuid,
    scored_at                         timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.assistant_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    profile_key                       text NOT NULL,
    name                              text,
    audience                          text NOT NULL CONSTRAINT assistant_profile_audience_chk CHECK (audience IN ('staff', 'guest', 'support')),
    role_ids                          text[],
    module                            text,
    collection_ids                    text[],
    tool_keys                         text[],
    model_task                        text,
    guest_capability_scope            text[],
    locales                           text[],
    handover_target                   text,
    is_active                         boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.blueprint (
    id                                uuid PRIMARY KEY NOT NULL,
    session_id                        uuid NOT NULL,
    version                           integer NOT NULL,
    readiness                         text NOT NULL CONSTRAINT blueprint_readiness_chk CHECK (readiness IN ('notReady', 'readyWithWarnings', 'ready')),
    required_open                     integer,
    issues                            jsonb,
    dependency_map                    jsonb,
    summary                           text,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.blueprint_decision (
    id                                uuid PRIMARY KEY NOT NULL,
    blueprint_id                      uuid NOT NULL,
    decision_key                      text NOT NULL,
    module                            text,
    decision_class                    text NOT NULL CONSTRAINT blueprint_decision_decision_class_chk CHECK (decision_class IN ('required', 'recommended', 'optional')),
    question                          text,
    value                             jsonb,
    provenance                        text CONSTRAINT blueprint_decision_provenance_chk CHECK (provenance IN ('confirmed', 'aiRecommended', 'inferred', 'unknown')),
    source_id                         uuid,
    source_citation                   text CONSTRAINT blueprint_decision_source_citation_chk CHECK (char_length(source_citation) <= 200),
    recommendation                    jsonb,
    status                            text NOT NULL CONSTRAINT blueprint_decision_status_chk CHECK (status IN ('open', 'accepted', 'modified', 'rejected', 'deferred')),
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    note                              text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.byok_enablement (
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid NOT NULL,
    is_enabled                        boolean NOT NULL,
    coverage                          text DEFAULT 'perTask' CONSTRAINT byok_enablement_coverage_chk CHECK (coverage IN ('perTask', 'allTasks')),
    allowed_tasks                     text[],
    task_model_map                    jsonb,
    reason                            text CONSTRAINT byok_enablement_reason_chk CHECK (char_length(reason) <= 1000),
    platform_staff_grant_id           uuid,
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.capability (
    id                                uuid PRIMARY KEY NOT NULL,
    capability_key                    text NOT NULL,
    family                            text NOT NULL CONSTRAINT capability_family_chk CHECK (family IN ('gatewayAndModels', 'governance', 'actionPipeline', 'knowledgeRetrieval', 'assistants', 'analyticsInsights', 'configurationAssistant', 'forecasting', 'anomalyDetection', 'riskIntelligence', 'recommendations', 'decisionRecords', 'operationsEvaluation', 'residencyPrivacy')),
    name                              text,
    description                       text,
    owner_principal_id                uuid,
    business_function                 text,
    risk_class                        text NOT NULL CONSTRAINT capability_risk_class_chk CHECK (risk_class IN ('low', 'medium', 'high', 'critical')),
    autonomy_ceiling                  jsonb,
    autonomy_level                    jsonb NOT NULL,
    data_categories                   text[],
    lifecycle                         jsonb,
    degradation_mode                  text CONSTRAINT capability_degradation_mode_chk CHECK (degradation_mode IN ('rulesOnly', 'searchOnly', 'humanHandoff', 'hidden', 'failOpen', 'lastPublished')),
    status                            text CONSTRAINT capability_status_chk CHECK (status IN ('active', 'paused')),
    paused_reason                     text,
    paused_at                         timestamptz,
    updated_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.capability_maturity (
    id                                uuid PRIMARY KEY NOT NULL,
    capability_key                    text NOT NULL,
    suggestion_kind                   text,
    forecast_definition_key           text,
    stage                             text NOT NULL CONSTRAINT capability_maturity_stage_chk CHECK (stage IN ('starting', 'learning', 'established', 'learned')),
    maturity                          jsonb,
    producer_ref                      text,
    since                             timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.case_action (
    id                                uuid PRIMARY KEY NOT NULL,
    case_id                           uuid NOT NULL,
    action                            text NOT NULL CONSTRAINT case_action_action_chk CHECK (action IN ('blockPaymentToken', 'suspendAccount', 'restrictWallet', 'revokeEntitlement', 'flagCustomer', 'requireStepUp', 'holdRefunds', 'lockIdentity')),
    target_contract                   text NOT NULL,
    target_operation                  text,
    target_ref                        text,
    rationale                         text,
    status                            text CONSTRAINT case_action_status_chk CHECK (status IN ('recommended', 'planned', 'awaitingApproval', 'applied', 'rejected', 'failed')),
    plan_id                           uuid,
    proposed_by_principal_id          uuid,
    proposed_at                       timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.case_evidence (
    id                                uuid PRIMARY KEY NOT NULL,
    case_id                           uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT case_evidence_kind_chk CHECK (kind IN ('assessment', 'alert', 'transaction', 'networkSnapshot', 'note', 'document')),
    ref                               text,
    content                           jsonb,
    blob_ref                          text,
    label                             text NOT NULL CONSTRAINT case_evidence_label_chk CHECK (label IN ('source', 'derived', 'modelInferred')),
    content_hash                      text,
    added_by_principal_id             uuid,
    added_at                          timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.chunk_embedding (
    id                                uuid PRIMARY KEY NOT NULL,
    document_id                       uuid NOT NULL,
    chunk_index                       integer NOT NULL,
    parent_chunk_id                   uuid,
    content                           text,
    embedding_model                   text NOT NULL,
    collection_alias                  text NOT NULL CONSTRAINT chunk_embedding_collection_alias_chk CHECK (char_length(collection_alias) <= 200),
    point_id                          uuid NOT NULL,
    token_count                       integer,
    content_hash                      text,
    indexed_at                        timestamptz,
    created_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.config_session (
    id                                uuid PRIMARY KEY NOT NULL,
    intent                            text NOT NULL CONSTRAINT config_session_intent_chk CHECK (intent IN ('create', 'modify', 'extend', 'clone')),
    venue_type                        text,
    source_scope_path                 ltree,
    status                            text NOT NULL CONSTRAINT config_session_status_chk CHECK (status IN ('discovering', 'blueprintReady', 'planned', 'executing', 'completed', 'abandoned')),
    progress_percent                  integer,
    next_question                     jsonb,
    conversation_id                   uuid,
    plan_id                           uuid,
    locale                            text,
    requested_by_principal_id         uuid,
    started_at                        timestamptz,
    last_activity_at                  timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.config_source (
    id                                uuid PRIMARY KEY NOT NULL,
    session_id                        uuid NOT NULL,
    asset_id                          uuid NOT NULL,
    source_kind                       text NOT NULL CONSTRAINT config_source_source_kind_chk CHECK (source_kind IN ('brief', 'brochure', 'catalogue', 'priceList', 'spreadsheet', 'brandAsset')),
    note                              text,
    status                            text NOT NULL CONSTRAINT config_source_status_chk CHECK (status IN ('extracting', 'extracted', 'partial', 'failed')),
    page_count                        integer,
    values_extracted                  integer,
    unread_regions                    text[],
    attached_by_principal_id          uuid,
    attached_at                       timestamptz,
    completed_at                      timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.control (
    id                                uuid PRIMARY KEY NOT NULL,
    control_key                       text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    kind                              text NOT NULL CONSTRAINT control_kind_chk CHECK (kind IN ('deterministic', 'manual')),
    check_ref                         text,
    frequency                         text CONSTRAINT control_frequency_chk CHECK (frequency IN ('nightly', 'weekly', 'monthly', 'onDemand')),
    capability_keys                   text[],
    owner_principal_id                uuid,
    effectiveness                     text CONSTRAINT control_effectiveness_chk CHECK (effectiveness IN ('effective', 'partiallyEffective', 'ineffective', 'untested')),
    last_tested_at                    timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.control_test (
    id                                uuid PRIMARY KEY NOT NULL,
    control_id                        uuid NOT NULL,
    result                            text NOT NULL CONSTRAINT control_test_result_chk CHECK (result IN ('pass', 'fail', 'error')),
    exceptions_found                  integer,
    evidence                          jsonb,
    run_by_principal_id               uuid,
    run_at                            timestamptz,
    scope_path                        ltree NOT NULL
);

-- A thread, scoped to a principal and a module. Analytical store, not the transactional primary
-- (ADR-0020) — append-only with an analytical read pattern, and it must not compete with a gate
-- scan for a connection
CREATE TABLE IF NOT EXISTS ai.conversation (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    module                            text NOT NULL CONSTRAINT conversation_module_chk CHECK (module IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai')),
    locale                            text,
    message_count                     integer,
    started_at                        timestamptz NOT NULL,
    last_message_at                   timestamptz
);

-- Holds 25 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.decision_record (
    id                                uuid PRIMARY KEY NOT NULL,
    trace_id                          text NOT NULL,
    capability_key                    text NOT NULL,
    task                              text,
    subject_kind                      text,
    subject_ref                       text,
    inputs_ref                        text,
    evidence                          jsonb,
    producer                          text,
    model_version                     text,
    prompt_template_version           text,
    feature_set_version               text,
    knowledge_version                 text,
    rule_versions                     jsonb,
    governance_outcome                text,
    policy_version                    text,
    approvals                         jsonb,
    human_decision                    jsonb,
    execution_result                  jsonb,
    outcome_ref                       text,
    outcome                           text NOT NULL CONSTRAINT decision_record_outcome_chk CHECK (outcome IN ('answered', 'refused', 'allowed', 'blocked', 'executed', 'failed', 'approvedThenFailed', 'published', 'suggested')),
    previous_hash                     text,
    record_hash                       text NOT NULL,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.entity_risk (
    id                                uuid PRIMARY KEY NOT NULL,
    entity_type                       text NOT NULL CONSTRAINT entity_risk_entity_type_chk CHECK (entity_type IN ('customer', 'account', 'device', 'paymentToken', 'credential', 'cluster', 'staff', 'ipAddress')),
    entity_ref                        text NOT NULL,
    score                             integer NOT NULL,
    band                              text NOT NULL CONSTRAINT entity_risk_band_chk CHECK (band IN ('low', 'medium', 'high', 'critical')),
    signals                           jsonb,
    last_event_at                     timestamptz,
    updated_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.eval_run (
    id                                uuid PRIMARY KEY NOT NULL,
    suite_id                          uuid NOT NULL,
    release_id                        uuid,
    kind                              text NOT NULL CONSTRAINT eval_run_kind_chk CHECK (kind IN ('offline', 'backtest', 'shadow')),
    candidate_ref                     text,
    baseline_ref                      text,
    status                            text NOT NULL CONSTRAINT eval_run_status_chk CHECK (status IN ('queued', 'running', 'passed', 'failed', 'error')),
    metrics                           jsonb,
    gate                              jsonb,
    is_isolation_cases_passed         boolean,
    requested_by_principal_id         uuid,
    started_at                        timestamptz,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.eval_suite (
    id                                uuid PRIMARY KEY NOT NULL,
    suite_key                         text NOT NULL,
    capability_key                    text NOT NULL,
    layer                             text NOT NULL CONSTRAINT eval_suite_layer_chk CHECK (layer IN ('platform', 'tenant')),
    version                           integer,
    case_count                        integer,
    includes_isolation_cases          boolean,
    blob_ref                          text,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.evidence_package (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_kind                        text NOT NULL CONSTRAINT evidence_package_scope_kind_chk CHECK (scope_kind IN ('singleDecision', 'customerJourney', 'capability', 'incident', 'modelVersion', 'governancePolicy')),
    scope_ref                         text,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    format                            text NOT NULL CONSTRAINT evidence_package_format_chk CHECK (format IN ('pdf', 'csv', 'json')),
    status                            text CONSTRAINT evidence_package_status_chk CHECK (status IN ('building', 'ready', 'failed')),
    decision_count                    integer,
    blob_ref                          text,
    manifest_hash                     text,
    requested_by_principal_id         uuid,
    requested_at                      timestamptz,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.forecast_accuracy (
    id                                uuid PRIMARY KEY NOT NULL,
    definition_id                     uuid NOT NULL,
    version_id                        uuid,
    producer_ref                      text,
    horizon_days                      integer NOT NULL,
    period_start                      timestamptz NOT NULL,
    period_end                        timestamptz,
    wape                              numeric(18,4),
    bias                              numeric(18,4),
    interval_coverage                 numeric(18,4),
    baseline_wape                     numeric(18,4),
    measured_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.forecast_definition (
    id                                uuid PRIMARY KEY NOT NULL,
    definition_key                    text NOT NULL,
    name                              text,
    subject                           text NOT NULL CONSTRAINT forecast_definition_subject_chk CHECK (subject IN ('attendance', 'arrivalPattern', 'productDemand', 'timeslotDemand', 'channelPace', 'revenue', 'occupancy', 'attractionUtilisation', 'queue', 'entryFlow', 'staffing', 'posDemand', 'fnbDemand', 'retailDemand', 'stockDemand', 'resourceDemand', 'refunds', 'cashCollection', 'membershipRenewals', 'churn')),
    module                            text,
    grain                             text NOT NULL CONSTRAINT forecast_definition_grain_chk CHECK (grain IN ('hour', 'day', 'week', 'month')),
    dimensions                        text[],
    segment_ids                       text[],
    horizon_days                      integer NOT NULL,
    refresh_cadence                   text CONSTRAINT forecast_definition_refresh_cadence_chk CHECK (refresh_cadence IN ('hourly', 'daily', 'weekly')),
    producer                          text NOT NULL CONSTRAINT forecast_definition_producer_chk CHECK (producer IN ('rule', 'statistical', 'model', 'ensemble')),
    history_window_months             integer DEFAULT 36,
    cold_start                        jsonb,
    producer_ref                      text,
    shadow_producer_ref               text,
    is_auto_publish                   boolean DEFAULT false,
    quality_gates                     jsonb,
    signal_keys                       text[],
    is_active                         boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.forecast_export (
    id                                uuid PRIMARY KEY NOT NULL,
    version_id                        uuid NOT NULL,
    scenario_id                       uuid,
    format                            text NOT NULL CONSTRAINT forecast_export_format_chk CHECK (format IN ('csv', 'xlsx', 'json')),
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    dimension_key                     text,
    include_drivers                   boolean DEFAULT false,
    status                            text NOT NULL CONSTRAINT forecast_export_status_chk CHECK (status IN ('building', 'ready', 'failed')),
    point_count                       integer,
    blob_ref                          text,
    download_url                      text,
    requested_by_principal_id         uuid,
    requested_at                      timestamptz,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.forecast_point (
    id                                uuid PRIMARY KEY NOT NULL,
    version_id                        uuid NOT NULL,
    scenario_id                       uuid,
    target_start                      timestamptz NOT NULL,
    target_end                        timestamptz,
    dimension_key                     text,
    p10                               numeric(18,4),
    p50                               numeric(18,4) NOT NULL,
    p90                               numeric(18,4),
    unit                              text,
    drivers                           jsonb,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.forecast_scenario (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text,
    base_version_id                   uuid NOT NULL,
    status                            text CONSTRAINT forecast_scenario_status_chk CHECK (status IN ('computing', 'ready', 'failed')),
    result                            jsonb,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.forecast_version (
    id                                uuid PRIMARY KEY NOT NULL,
    definition_id                     uuid NOT NULL,
    version_number                    integer NOT NULL,
    module                            text,
    status                            text NOT NULL CONSTRAINT forecast_version_status_chk CHECK (status IN ('running', 'draft', 'awaitingApproval', 'published', 'superseded', 'rejected', 'failed')),
    basis                             text NOT NULL CONSTRAINT forecast_version_basis_chk CHECK (basis IN ('heuristic', 'statistical', 'model', 'hybrid', 'manual')),
    maturity                          jsonb,
    producer_ref                      text,
    model_version                     text,
    data_cutoff_at                    timestamptz,
    horizon_start                     timestamptz,
    horizon_end                       timestamptz,
    quality_checks                    jsonb,
    published_by_principal_id         uuid,
    published_at                      timestamptz,
    decision_record_id                uuid,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.governance_alert (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT governance_alert_kind_chk CHECK (kind IN ('policyViolation', 'crossScopeAttempt', 'maskingDefect', 'dataUsage', 'behaviourDrift', 'inputDrift', 'bias', 'overrideRateShift', 'controlFailed', 'spend', 'providerBreaker', 'evaluationRegression', 'forecastNotPublished', 'indexLag', 'promotionReady')),
    severity                          text NOT NULL CONSTRAINT governance_alert_severity_chk CHECK (severity IN ('info', 'low', 'medium', 'high', 'critical')),
    capability_key                    text,
    release_id                        uuid,
    subject_ref                       text,
    evidence                          jsonb,
    status                            text NOT NULL CONSTRAINT governance_alert_status_chk CHECK (status IN ('open', 'acknowledged', 'dismissed', 'resolved', 'incidentOpened')),
    incident_id                       uuid,
    raised_at                         timestamptz,
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    note                              text,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.governance_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    policy_key                        text NOT NULL,
    name                              text,
    kind                              text NOT NULL CONSTRAINT governance_policy_kind_chk CHECK (kind IN ('action', 'data', 'scope', 'autonomy', 'approval', 'environment')),
    capability_keys                   text[],
    current_version                   integer,
    status                            text CONSTRAINT governance_policy_status_chk CHECK (status IN ('draft', 'active', 'retired')),
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.governance_policy_version (
    id                                uuid PRIMARY KEY NOT NULL,
    policy_id                         uuid NOT NULL,
    version                           integer NOT NULL,
    status                            text NOT NULL CONSTRAINT governance_policy_version_status_chk CHECK (status IN ('draft', 'simulated', 'published', 'superseded')),
    rules                             jsonb,
    change_note                       text,
    simulation_summary                jsonb,
    drafted_by_principal_id           uuid,
    published_by_principal_id         uuid,
    published_at                      timestamptz,
    superseded_at                     timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.guided_choice_suggestion (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    trigger                           text NOT NULL CONSTRAINT guided_choice_suggestion_trigger_chk CHECK (trigger IN ('productsUploaded', 'mappedProductWithdrawn', 'productsUncovered', 'manual')),
    status                            text NOT NULL CONSTRAINT guided_choice_suggestion_status_chk CHECK (status IN ('running', 'proposed', 'noSuggestion', 'failed', 'superseded')),
    product_count                     integer,
    wording_source                    text CONSTRAINT guided_choice_suggestion_wording_source_chk CHECK (wording_source IN ('model', 'attributeNames')),
    model_version                     text,
    prompt_template_version           text,
    guided_choice_id                  uuid,
    decision_record_id                uuid,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.history_import (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    data_kind                         text NOT NULL CONSTRAINT history_import_data_kind_chk CHECK (data_kind IN ('attendance', 'admissions', 'ticketSales', 'fnbSales', 'retailSales', 'queueReadings', 'staffShifts')),
    asset_id                          uuid,
    source_system                     text,
    column_mapping                    jsonb,
    dry_run                           boolean DEFAULT false,
    status                            text NOT NULL CONSTRAINT history_import_status_chk CHECK (status IN ('queued', 'validating', 'loading', 'completed', 'completedWithRejections', 'failed')),
    period_from                       date,
    period_to                         date,
    months_covered                    integer,
    rows_read                         integer,
    rows_loaded                       integer,
    rows_rejected                     integer,
    requested_by_principal_id         uuid,
    created_at                        timestamptz,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.history_observation (
    id                                uuid PRIMARY KEY NOT NULL,
    import_id                         uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    data_kind                         text NOT NULL,
    observed_on                       date NOT NULL,
    hour                              integer,
    dimension_key                     text,
    value                             numeric(18,4) NOT NULL,
    unit                              text,
    scope_path                        ltree NOT NULL
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.inbox (
    consumer                          text NOT NULL CONSTRAINT inbox_consumer_chk CHECK (char_length(consumer) <= 200),
    event_id                          uuid NOT NULL,
    processed_at                      timestamptz NOT NULL,
    CONSTRAINT inbox_pkey PRIMARY KEY (consumer, event_id)
) PARTITION BY RANGE (event_id);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.incident (
    id                                uuid PRIMARY KEY NOT NULL,
    reference                         text NOT NULL,
    title                             text NOT NULL,
    kind                              text CONSTRAINT incident_kind_chk CHECK (kind IN ('governance', 'operational', 'both')),
    severity                          text NOT NULL CONSTRAINT incident_severity_chk CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    status                            text NOT NULL CONSTRAINT incident_status_chk CHECK (status IN ('open', 'contained', 'investigating', 'remediating', 'closed')),
    capability_keys                   text[],
    alert_ids                         text[],
    operational_incident_ref          text,
    root_cause                        text,
    remediation                       text,
    impact                            text,
    control_failure                   text,
    lessons_learned                   text,
    owner_principal_id                uuid,
    opened_at                         timestamptz,
    contained_at                      timestamptz,
    closed_at                         timestamptz,
    scope_path                        ltree NOT NULL
);

-- Maps a source row to its Qdrant point ids, so a deletion in Postgres can be followed into the
-- vector store. Nothing cascades between the two Hangs off: reaches ai.decision_record through its
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
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- A build in flight. recordsFailed is the number to watch — a source failing on 3% of rows is a
-- search missing 3% of answers Hangs off: reaches ai.decision_record through its keys; references
-- ai.index_source. Reached by: 3 operations read it and 1 write it; 2 tables reference it.
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
-- consumes the event that service already publishes Hangs off: reaches ai.decision_record through
-- its keys; references ai.knowledge_collection. Reached by: 3 operations read it and 1 write it; 3
-- tables reference it.
CREATE TABLE IF NOT EXISTS ai.index_source (
    id                                uuid PRIMARY KEY NOT NULL,
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

-- Holds 22 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.insight (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT insight_kind_chk CHECK (kind IN ('anomaly', 'forecastDeviation', 'trend', 'opportunity', 'executiveSummary', 'rootCause', 'forecastThreshold', 'marketingRecommendation')),
    detector_id                       uuid,
    metric_key                        text,
    subject_kind                      text CONSTRAINT insight_subject_kind_chk CHECK (subject_kind IN ('campaign', 'journey', 'forecastDefinition', 'venue')),
    subject_ref                       text,
    recommended_action                jsonb,
    expected_impact                   jsonb,
    title                             text NOT NULL,
    narrative                         text,
    evidence                          jsonb,
    magnitude                         numeric(18,4),
    priority                          text CONSTRAINT insight_priority_chk CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    correlation_key                   text,
    status                            text NOT NULL CONSTRAINT insight_status_chk CHECK (status IN ('new', 'reviewed', 'accepted', 'rejected', 'actioned', 'measured')),
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    action_ref                        text,
    measured_impact                   jsonb,
    decision_record_id                uuid,
    detected_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.intervention (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT intervention_kind_chk CHECK (kind IN ('override', 'pause', 'resume', 'cancel', 'retry', 'rollback', 'capabilityPause', 'capabilityResume')),
    target_kind                       text NOT NULL CONSTRAINT intervention_target_kind_chk CHECK (target_kind IN ('plan', 'step', 'decision', 'capability')),
    target_ref                        text NOT NULL,
    decision_record_id                uuid,
    original_decision                 jsonb,
    human_decision                    jsonb,
    reason                            text CONSTRAINT intervention_reason_chk CHECK (char_length(reason) <= 2000),
    principal_id                      uuid,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- A collection in the vector store. One per embedding model — a collection carries its own vector
-- config and a shard cannot, so two models cannot share one (ADR-0021). Carries the shard key,
-- which is the tenant boundary on shared placement Hangs off: reaches ai.decision_record through
-- its keys. Reached by: 5 operations read it and 1 write it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS ai.knowledge_collection (
    id                                uuid PRIMARY KEY NOT NULL,
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
-- ai.decision_record through its keys; references ai.knowledge_collection, ai.knowledge_document.
-- Reached by: 4 operations read it and 1 write it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS ai.knowledge_document (
    id                                uuid PRIMARY KEY NOT NULL,
    collection_id                     uuid,
    title                             text NOT NULL,
    source_asset_id                   uuid NOT NULL,
    mime_type                         text,
    supersedes_document_id            uuid,
    status                            text CONSTRAINT knowledge_document_status_chk CHECK (status IN ('processing', 'indexed', 'failed', 'superseded')),
    chunk_count                       integer,
    failure_reason                    text,
    indexed_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.knowledge_gap (
    id                                uuid PRIMARY KEY NOT NULL,
    question                          text NOT NULL,
    examples                          text[],
    occurrences                       integer,
    audience                          text CONSTRAINT knowledge_gap_audience_chk CHECK (audience IN ('staff', 'guest')),
    locale                            text,
    kind                              text CONSTRAINT knowledge_gap_kind_chk CHECK (kind IN ('knowledge', 'analytics')),
    suggested_collection_id           uuid,
    owner_principal_id                uuid,
    status                            text NOT NULL CONSTRAINT knowledge_gap_status_chk CHECK (status IN ('open', 'assigned', 'answered', 'dismissed')),
    resolved_document_id              uuid,
    last_asked_at                     timestamptz,
    scope_path                        ltree NOT NULL
);

-- A generated seat layout awaiting review. Ends at previewReady and writes nothing to the seat map
-- — the draft enters seating.import_job at its existing human commit step (ADR-0020) Hangs off:
-- reaches ai.decision_record through its keys; references assets.media_asset. Reached by: 1
-- operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS ai.layout_draft (
    id                                uuid PRIMARY KEY NOT NULL,
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
    provider                          text CONSTRAINT message_provider_chk CHECK (provider IN ('openai', 'gemini', 'anthropic', 'azureOpenai', 'localLlm', 'openaiCompatible')),
    model                             text,
    prompt_tokens                     integer,
    completion_tokens                 integer,
    latency_ms                        integer,
    created_at                        timestamptz NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.model (
    id                                uuid PRIMARY KEY NOT NULL,
    layer                             text NOT NULL CONSTRAINT model_layer_chk CHECK (layer IN ('platform', 'tenant')),
    provider_kind                     text,
    vendor                            text,
    producer_type                     text NOT NULL CONSTRAINT model_producer_type_chk CHECK (producer_type IN ('llm', 'embedding', 'reranker', 'classical', 'rule')),
    model_name                        text NOT NULL,
    capabilities                      text[],
    context_tokens                    integer,
    tool_calling                      boolean DEFAULT false,
    structured_output                 boolean DEFAULT false,
    languages                         text[],
    residency                         text,
    input_cost_per_million_tokens     numeric(18,4),
    output_cost_per_million_tokens    numeric(18,4),
    lifecycle                         jsonb,
    is_default_for_tasks              text[],
    curated_range                     jsonb,
    residency_classes                 text[],
    scope_path                        ltree NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.operational_requirement (
    id                                uuid PRIMARY KEY NOT NULL,
    version_id                        uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT operational_requirement_kind_chk CHECK (kind IN ('staff', 'pos', 'kiosk', 'gates', 'fnb', 'retail', 'stock', 'resource', 'equipment', 'facility')),
    target_contract                   text,
    subject_ref                       text,
    period_start                      timestamptz NOT NULL,
    period_end                        timestamptz,
    quantity                          numeric(18,4) NOT NULL,
    quantity_p90                      numeric(18,4),
    unit                              text,
    productivity_standard             jsonb,
    status                            text CONSTRAINT operational_requirement_status_chk CHECK (status IN ('issued', 'accepted', 'modified', 'rejected', 'handedOver', 'expired')),
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    decision_note                     text,
    handover_ref                      text,
    scope_path                        ltree NOT NULL
);

-- What the assistant may do, which roles may use it, what is masked. Resolves tenant then venue
-- (ADR-0018) Hangs off: reaches ai.decision_record through its keys; references ai.provider,
-- platform.tenant. Reached by: 22 operations read it and 4 write it.
CREATE TABLE IF NOT EXISTS ai.policy (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_level                       text NOT NULL CONSTRAINT policy_scope_level_chk CHECK (scope_level IN ('tenant', 'venue')),
    scope_path                        ltree NOT NULL,
    enabled_capabilities              text[] NOT NULL,
    allowed_role_ids                  text[],
    masked_fields                     text[],
    requires_approval_for             text[],
    scrubbing                         jsonb,
    global_endpoint_exclusions        jsonb,
    monthly_token_ceiling             integer,
    ceiling_behaviour                 text DEFAULT 'warn' CONSTRAINT policy_ceiling_behaviour_chk CHECK (ceiling_behaviour IN ('warn', 'warnThenDisable', 'block')),
    ceiling_behaviour_by_capability   jsonb,
    autonomy_overrides                jsonb,
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

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.policy_exception (
    id                                uuid PRIMARY KEY NOT NULL,
    policy_id                         uuid NOT NULL,
    capability_key                    text,
    reason                            text NOT NULL CONSTRAINT policy_exception_reason_chk CHECK (char_length(reason) <= 2000),
    compensating_controls             text[],
    starts_at                         timestamptz,
    expires_at                        timestamptz NOT NULL,
    status                            text CONSTRAINT policy_exception_status_chk CHECK (status IN ('active', 'expired', 'revoked')),
    approved_by_principal_id          uuid,
    revoked_by_principal_id           uuid,
    revoked_at                        timestamptz,
    revoke_reason                     text,
    scope_path                        ltree NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.prompt_template (
    id                                uuid PRIMARY KEY NOT NULL,
    template_key                      text NOT NULL,
    version                           integer NOT NULL,
    layer                             text NOT NULL CONSTRAINT prompt_template_layer_chk CHECK (layer IN ('platform', 'tenant')),
    task                              text NOT NULL,
    body                              text,
    variables                         text[],
    output_schema                     jsonb,
    status                            text NOT NULL CONSTRAINT prompt_template_status_chk CHECK (status IN ('draft', 'published', 'retired')),
    content_hash                      text,
    published_by_principal_id         uuid,
    published_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- A draft the assistant produced and a person must approve. Nothing executes from here Hangs off:
-- reaches ai.decision_record through its keys; references ai.action_plan, ai.activity,
-- approvals.request. Reached by: 7 operations read it and 11 write it; 2 tables reference it.
CREATE TABLE IF NOT EXISTS ai.proposed_action (
    id                                uuid PRIMARY KEY NOT NULL,
    interaction_id                    uuid,
    translation_job_id                uuid,
    kind                              text NOT NULL CONSTRAINT proposed_action_kind_chk CHECK (kind IN ('pricing', 'promotion', 'operational', 'financial', 'configuration', 'content', 'audience')),
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
    decided_at                        timestamptz,
    scope_path                        ltree NOT NULL,
    plan_id                           uuid,
    approval_request_id               uuid,
    change_set_hash                   text
);

-- Configured providers, models and failover order. Credentials are a vault reference, never a key
-- Hangs off: reaches ai.decision_record through its keys; references ai.model, ai.provider,
-- platform.scope. Reached by: 18 operations read it and 3 write it; 2 tables reference it.
CREATE TABLE IF NOT EXISTS ai.provider (
    is_stateless_only                 boolean,
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT provider_kind_chk CHECK (kind IN ('openai', 'gemini', 'anthropic', 'azureOpenai', 'localLlm', 'openaiCompatible')),
    vendor                            text,
    capability                        text NOT NULL CONSTRAINT provider_capability_chk CHECK (capability IN ('chat', 'embedding', 'vision', 'rerank', 'speechToText', 'textToSpeech')),
    model                             text,
    failover_provider_id              uuid,
    degrade_gracefully                boolean DEFAULT true,
    priority                          integer NOT NULL,
    scope_level                       text CONSTRAINT provider_scope_level_chk CHECK (scope_level IN ('platform', 'tenant', 'venue')),
    scope_path                        ltree NOT NULL,
    tenant_id                         uuid,
    credential_ref                    text,
    credential_hint                   text CONSTRAINT provider_credential_hint_chk CHECK (char_length(credential_hint) <= 4),
    credential_rotated_at             timestamptz,
    credential_expires_at             timestamptz,
    last_verified_at                  timestamptz,
    compatibility                     jsonb,
    endpoint                          text,
    residency                         text,
    residency_classes                 text[],
    max_tokens                        integer,
    is_active                         boolean NOT NULL,
    managed_by                        text DEFAULT 'ticvai' CONSTRAINT provider_managed_by_chk CHECK (managed_by IN ('ticvai', 'tenant')),
    model_id                          uuid,
    task_keys                         text[],
    region_id                         uuid NOT NULL
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.rec_decision (
    id                                uuid PRIMARY KEY NOT NULL,
    placement                         text NOT NULL CONSTRAINT rec_decision_placement_chk CHECK (placement IN ('productPage', 'cart', 'checkout', 'postPurchase', 'preVisit', 'inVenue', 'posBasket', 'kioskBasket', 'fnbMenu', 'retailBasket', 'seatUpgrade', 'membership', 'email', 'homepage', 'loyalty')),
    channel                           text,
    cart_id                           uuid,
    session_ref                       text,
    subject_id                        uuid,
    mode                              text NOT NULL CONSTRAINT rec_decision_mode_chk CHECK (mode IN ('personalised', 'contextual', 'rulesOnly', 'fallback')),
    strategy_ref                      text,
    strategy_version                  integer,
    model_version                     text,
    feature_set_version               text,
    funnel                            jsonb,
    exclusions                        jsonb,
    items                             jsonb NOT NULL,
    experiment_arm                    text,
    latency_ms                        integer,
    expires_at                        timestamptz,
    decided_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.rec_decline (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid,
    session_ref                       text,
    product_id                        uuid,
    item_ref                          text,
    placement                         text CONSTRAINT rec_decline_placement_chk CHECK (placement IN ('productPage', 'cart', 'checkout', 'postPurchase', 'preVisit', 'inVenue', 'posBasket', 'kioskBasket', 'fnbMenu', 'retailBasket', 'seatUpgrade', 'membership', 'email', 'homepage', 'loyalty')),
    channel                           text,
    declined_at                       timestamptz NOT NULL,
    expires_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.rec_event (
    id                                uuid PRIMARY KEY NOT NULL,
    decision_id                       uuid,
    tracking_id                       uuid NOT NULL,
    event_type                        text NOT NULL CONSTRAINT rec_event_event_type_chk CHECK (event_type IN ('impression', 'click', 'addToCart', 'purchase', 'dismiss', 'decline')),
    product_id                        uuid,
    order_id                          uuid,
    channel                           text,
    session_ref                       text,
    subject_id                        uuid,
    occurred_at                       timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.release (
    id                                uuid PRIMARY KEY NOT NULL,
    capability_key                    text NOT NULL,
    artefact_kind                     text NOT NULL CONSTRAINT release_artefact_kind_chk CHECK (artefact_kind IN ('model', 'prompt', 'routing', 'embedding', 'retrieval', 'rule')),
    candidate_ref                     text NOT NULL,
    current_ref                       text,
    previous_ref                      text,
    layer                             text NOT NULL CONSTRAINT release_layer_chk CHECK (layer IN ('platform', 'tenant')),
    module                            text,
    suggestion_kind                   text,
    stage                             text NOT NULL CONSTRAINT release_stage_chk CHECK (stage IN ('draft', 'offlineEval', 'shadow', 'canary', 'production', 'monitored', 'rolledBack', 'rejected')),
    shadow_started_at                 timestamptz,
    gate_passed_at                    timestamptz,
    canary_scope                      jsonb,
    promoted_by_principal_id          uuid,
    promoted_at                       timestamptz,
    rolled_back_by_principal_id       uuid,
    rolled_back_at                    timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.risk_alert (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT risk_alert_kind_chk CHECK (kind IN ('transaction', 'velocity', 'entity', 'network', 'staffLeakage', 'scanAbuse', 'accountTakeover', 'chargeback')),
    entity_type                       text NOT NULL CONSTRAINT risk_alert_entity_type_chk CHECK (entity_type IN ('customer', 'account', 'device', 'paymentToken', 'credential', 'cluster', 'staff', 'wallet', 'ipAddress')),
    entity_ref                        text NOT NULL,
    score                             integer,
    band                              text NOT NULL CONSTRAINT risk_alert_band_chk CHECK (band IN ('low', 'medium', 'high', 'critical')),
    reason_codes                      text[],
    correlation_key                   text,
    assessment_id                     uuid,
    status                            text NOT NULL CONSTRAINT risk_alert_status_chk CHECK (status IN ('open', 'monitoring', 'dismissed', 'falsePositive', 'escalated')),
    case_id                           uuid,
    raised_at                         timestamptz,
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    decision_note                     text,
    scope_path                        ltree NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.risk_assessment (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_kind                      text NOT NULL CONSTRAINT risk_assessment_subject_kind_chk CHECK (subject_kind IN ('payment', 'login', 'scan', 'refund', 'walletTransfer', 'entitlementTransfer')),
    order_id                          uuid,
    payment_attempt_ref               text,
    score                             integer NOT NULL,
    band                              text NOT NULL CONSTRAINT risk_assessment_band_chk CHECK (band IN ('low', 'medium', 'high', 'critical')),
    outcome                           text NOT NULL CONSTRAINT risk_assessment_outcome_chk CHECK (outcome IN ('allow', 'monitor', 'stepUp', 'holdForReview', 'decline')),
    reason_codes                      text[],
    strategy_version                  integer,
    model_version                     text,
    latency_ms                        integer,
    fell_back                         boolean,
    decision_record_id                uuid,
    assessed_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.risk_case (
    id                                uuid PRIMARY KEY NOT NULL,
    reference                         text NOT NULL,
    title                             text,
    status                            text NOT NULL CONSTRAINT risk_case_status_chk CHECK (status IN ('open', 'investigating', 'pendingAction', 'closed')),
    priority                          text CONSTRAINT risk_case_priority_chk CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    alert_ids                         text[],
    assignee_principal_id             uuid,
    summary                           text,
    outcome                           text CONSTRAINT risk_case_outcome_chk CHECK (outcome IN ('confirmedFraud', 'notFraud', 'inconclusive')),
    closure_note                      text,
    opened_by_principal_id            uuid,
    opened_at                         timestamptz,
    closed_by_principal_id            uuid,
    closed_at                         timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.risk_edge (
    id                                uuid PRIMARY KEY NOT NULL,
    from_entity_type                  text NOT NULL CONSTRAINT risk_edge_from_entity_type_chk CHECK (from_entity_type IN ('customer', 'account', 'device', 'paymentToken', 'credential', 'cluster', 'staff', 'ipAddress')),
    from_entity_ref                   text NOT NULL,
    to_entity_type                    text NOT NULL CONSTRAINT risk_edge_to_entity_type_chk CHECK (to_entity_type IN ('customer', 'account', 'device', 'paymentToken', 'credential', 'cluster', 'staff', 'ipAddress')),
    to_entity_ref                     text NOT NULL,
    relation                          text NOT NULL CONSTRAINT risk_edge_relation_chk CHECK (relation IN ('sharedDevice', 'sharedToken', 'sharedAccount', 'sharedContact', 'sharedIp', 'transfer', 'companion', 'staffCustomer')),
    strength                          numeric(18,4),
    first_seen_at                     timestamptz,
    last_seen_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.risk_register (
    id                                uuid PRIMARY KEY NOT NULL,
    title                             text NOT NULL,
    category                          text NOT NULL CONSTRAINT risk_register_category_chk CHECK (category IN ('customer', 'commercial', 'financial', 'operational', 'security', 'modelQuality', 'privacy', 'compliance')),
    capability_keys                   text[],
    likelihood                        integer NOT NULL,
    impact                            integer NOT NULL,
    inherent_rating                   text CONSTRAINT risk_register_inherent_rating_chk CHECK (inherent_rating IN ('low', 'medium', 'high', 'critical')),
    control_keys                      text[],
    residual_rating                   text CONSTRAINT risk_register_residual_rating_chk CHECK (residual_rating IN ('low', 'medium', 'high', 'critical')),
    treatment                         text CONSTRAINT risk_register_treatment_chk CHECK (treatment IN ('accept', 'mitigate', 'transfer', 'avoid')),
    owner_principal_id                uuid,
    status                            text CONSTRAINT risk_register_status_chk CHECK (status IN ('open', 'mitigating', 'accepted', 'closed')),
    review_due_at                     timestamptz,
    updated_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.risk_strategy (
    id                                uuid PRIMARY KEY NOT NULL,
    version                           integer NOT NULL,
    mode                              text NOT NULL CONSTRAINT risk_strategy_mode_chk CHECK (mode IN ('monitor', 'enforce')),
    weights                           jsonb,
    thresholds                        jsonb NOT NULL,
    fail_mode                         text DEFAULT 'open' CONSTRAINT risk_strategy_fail_mode_chk CHECK (fail_mode IN ('open', 'holdForReview')),
    is_decline_governed               boolean DEFAULT false,
    is_model_enabled                  boolean DEFAULT false,
    status                            text CONSTRAINT risk_strategy_status_chk CHECK (status IN ('draft', 'active', 'superseded')),
    published_by_principal_id         uuid,
    published_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.signal_observation (
    id                                uuid PRIMARY KEY NOT NULL,
    source_id                         uuid NOT NULL,
    observed_for                      timestamptz NOT NULL,
    value                             jsonb,
    availability                      text NOT NULL CONSTRAINT signal_observation_availability_chk CHECK (availability IN ('available', 'unavailable')),
    received_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.signal_source (
    id                                uuid PRIMARY KEY NOT NULL,
    signal_key                        text NOT NULL,
    kind                              text NOT NULL CONSTRAINT signal_source_kind_chk CHECK (kind IN ('weather', 'publicHoliday', 'schoolCalendar', 'religiousCalendar', 'event', 'marketing', 'internal')),
    provider                          text,
    credential_ref                    text,
    refresh_cadence                   text CONSTRAINT signal_source_refresh_cadence_chk CHECK (refresh_cadence IN ('hourly', 'daily', 'weekly', 'manual')),
    coverage                          numeric(18,4),
    fresh_at                          timestamptz,
    is_active                         boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.spend_ceiling (
    scope_path                        ltree NOT NULL,
    spend                             numeric(18,4) NOT NULL,
    token_equivalent                  integer,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- One answer to one question, with its basis and its reasoning (24 August). Built so machine
-- learning can be swapped in without touching a screen — a heuristic today, a model when there is
-- data, and the frontend never changes. A suggestion is never an action. Hangs off: reaches
-- ai.decision_record through its keys. Reached by: 3 operations read it and 1 write it; 2 tables
-- reference it.
CREATE TABLE IF NOT EXISTS ai.suggestion (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT suggestion_kind_chk CHECK (kind IN ('price', 'replenishment', 'requisition', 'demandForecast', 'prepPlan', 'menuEngineering', 'staffing', 'slaTarget', 'waitTime', 'upsell', 'segmentation', 'anomaly', 'scenario', 'sendTime', 'wasteRisk', 'queueBalancing', 'itinerary')),
    basis                             text NOT NULL CONSTRAINT suggestion_basis_chk CHECK (basis IN ('heuristic', 'statistical', 'model', 'hybrid', 'manual')),
    scope_path                        ltree NOT NULL,
    subject_ref                       text,
    value                             jsonb,
    confidence                        numeric(18,4),
    explanation                       text,
    inputs                            jsonb,
    producer_ref                      text,
    maturity                          jsonb NOT NULL,
    produced_at                       timestamptz NOT NULL,
    expires_at                        timestamptz
);

-- What the venue actually did. The table that makes the swap possible at all — a model needs
-- labelled data and the only source of labels is whether the advice was taken and whether it
-- worked. A rejected suggestion is the more valuable record. Hangs off: a child of ai.suggestion;
-- reaches ai.decision_record through its keys; references ai.suggestion, identity.principal.
-- Reached by: 1 operations read i
CREATE TABLE IF NOT EXISTS ai.suggestion_outcome (
    id                                uuid PRIMARY KEY NOT NULL,
    suggestion_id                     uuid NOT NULL,
    decision                          text NOT NULL CONSTRAINT suggestion_outcome_decision_chk CHECK (decision IN ('accepted', 'modified', 'rejected', 'ignored', 'expired')),
    actual_value                      jsonb,
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    realised_outcome                  jsonb,
    note                              text,
    scope_path                        ltree NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.tool (
    id                                uuid PRIMARY KEY NOT NULL,
    tool_key                          text NOT NULL,
    target_contract                   text NOT NULL,
    target_operation                  text NOT NULL,
    contract_version                  text,
    effect                            text NOT NULL CONSTRAINT tool_effect_chk CHECK (effect IN ('read', 'write', 'destructive')),
    risk_class                        text CONSTRAINT tool_risk_class_chk CHECK (risk_class IN ('low', 'medium', 'high', 'critical')),
    permission                        text,
    is_reversible                     boolean,
    compensation_operation            text,
    timeout_ms                        integer,
    is_idempotent                     boolean DEFAULT true,
    validate_only                     boolean DEFAULT false,
    status                            text CONSTRAINT tool_status_chk CHECK (status IN ('active', 'disabled')),
    scope_path                        ltree NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.training_run (
    id                                uuid PRIMARY KEY NOT NULL,
    capability_key                    text NOT NULL,
    suggestion_kind                   text,
    forecast_definition_key           text,
    training_window_from              date,
    training_window_to                date,
    data_cutoff_at                    timestamptz,
    includes_imported_history         boolean DEFAULT false,
    feature_set_version               text,
    artefact_ref                      text,
    backtest_run_id                   uuid,
    release_id                        uuid,
    status                            text NOT NULL CONSTRAINT training_run_status_chk CHECK (status IN ('queued', 'training', 'backtesting', 'shadow', 'gatePassed', 'gateFailed', 'failed')),
    metrics                           jsonb,
    started_at                        timestamptz,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ai.venue_settings (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    venue_type                        text NOT NULL CONSTRAINT venue_settings_venue_type_chk CHECK (venue_type IN ('waterPark', 'themePark', 'familyEntertainmentCentre', 'museum', 'arena', 'zooAquarium', 'other')),
    is_outdoor                        boolean DEFAULT true,
    capacity                          integer,
    typical_weekday_attendance        integer,
    typical_weekend_attendance        integer,
    peak_months                       integer[],
    average_spend                     numeric(18,4),
    fnb_attach_rate                   numeric(18,4),
    staff_productivity                jsonb,
    starting_pattern_key              text,
    updated_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

