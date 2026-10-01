-- control — 81 tables
-- **Derived. Do not hand-edit.**

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.api_anomaly (
    id                                uuid PRIMARY KEY NOT NULL,
    rule_key                          text NOT NULL,
    client_id                         uuid NOT NULL,
    measure                           text,
    observed                          numeric(18,4),
    baseline                          numeric(18,4),
    action_taken                      text CONSTRAINT api_anomaly_action_taken_chk CHECK (action_taken IN ('flag', 'throttle', 'suspend')),
    detected_at                       timestamptz NOT NULL,
    resolved_at                       timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.api_anomaly_rule (
    id                                uuid PRIMARY KEY,
    rule_key                          text NOT NULL,
    client_id                         uuid,
    measure                           text NOT NULL CONSTRAINT api_anomaly_rule_measure_chk CHECK (measure IN ('callsPerMinute', 'clientErrorShare', 'allowListRefusals', 'unusualOperations', 'authFailures')),
    comparison                        text NOT NULL CONSTRAINT api_anomaly_rule_comparison_chk CHECK (comparison IN ('aboveBaselineMultiple', 'aboveFixed')),
    threshold                         numeric(18,4) NOT NULL,
    window_minutes                    integer DEFAULT 5,
    action                            text NOT NULL DEFAULT 'flag' CONSTRAINT api_anomaly_rule_action_chk CHECK (action IN ('flag', 'throttle', 'suspend')),
    is_active                         boolean DEFAULT true
);

-- The one credential model (CF-135a). 2.7.52, 7.1.25 and 7.1.30 each asserted their own. Bound to
-- one environment, because a key that works in both is a key somebody will use in the wrong one
CREATE TABLE IF NOT EXISTS control.api_client (
    id                                uuid PRIMARY KEY NOT NULL,
    developer_id                      uuid NOT NULL,
    name                              text NOT NULL,
    client_id                         text,
    environment                       text NOT NULL CONSTRAINT api_client_environment_chk CHECK (environment IN ('sandbox', 'production')),
    scopes                            text[] NOT NULL,
    issued_by                         text CONSTRAINT api_client_issued_by_chk CHECK (issued_by IN ('partner', 'ticvai')),
    certification_listing_id          uuid,
    credential_ttl_days               integer,
    expires_at                        timestamptz,
    allowed_tenant_ids                text[],
    ip_allow_list                     text[],
    status                            text NOT NULL CONSTRAINT api_client_status_chk CHECK (status IN ('active', 'suspended', 'revoked')),
    last_used_at                      timestamptz
);

-- Which API modules a tenant licensed (13.3.24, D5). Configuration, not code — rates change
-- without a release
CREATE TABLE IF NOT EXISTS control.api_licence (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    licensed_modules                  text[] NOT NULL,
    call_allowance_per_month          integer,
    catalogue_write_exception         jsonb,
    overage_rate_per_thousand         numeric(18,4),
    revenue_share_percent             numeric(18,4),
    effective_from                    date,
    effective_to                      date
);

-- Rate limits per client (13.1.36). A quota protects the venue, not the developer. Hangs off:
-- reaches control.partner through its keys; references control.api_client. Reached by: 1
-- operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS control.api_limit (
    id                                uuid PRIMARY KEY,
    client_id                         uuid NOT NULL,
    sustained_per_minute              integer NOT NULL,
    burst_per_second                  integer,
    daily_cap                         integer,
    per_operation_overrides           jsonb,
    on_breach                         text DEFAULT 'throttle' CONSTRAINT api_limit_on_breach_chk CHECK (on_breach IN ('throttle', 'reject', 'queue'))
);

-- API versions and sunset dates (13.1.31–35, ADR-0031). With third parties a breaking change with
-- no window breaks somebody else business. Hangs off: reaches control.partner through its keys.
-- Reached by: 3 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS control.api_version (
    version                           text NOT NULL,
    status                            text NOT NULL CONSTRAINT api_version_status_chk CHECK (status IN ('preview', 'current', 'deprecated', 'sunset')),
    released_at                       timestamptz,
    deprecated_at                     timestamptz,
    sunset_at                         timestamptz,
    minimum_notice_months             integer DEFAULT 12,
    migration_guide_url               text,
    active_client_count               integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- One archival run against one table in one cell, with what it moved and what it destroyed counted
-- separately. rows_archived and rows_purged are two numbers because they are two different
-- consequences — copying rows out is reversible and deleting them is not, and a single
-- rows_processed would hide which of the two happened. error holds the failure text, because an
-- archival job that fails silently is
CREATE TABLE IF NOT EXISTS control.archival_job (
    id                                uuid PRIMARY KEY NOT NULL,
    cell_id                           uuid,
    policy_name                       text,
    target_table                      text,
    rows_archived                     integer,
    rows_purged                       integer,
    state                             text CONSTRAINT archival_job_state_chk CHECK (state IN ('scheduled', 'running', 'succeeded', 'failed')),
    run_at                            timestamptz,
    error                             text
);

-- One backup, and whether anyone has proved it restores. restore_tested_at is the column that
-- matters: a backup nobody has restored from is a belief, not a backup, and it is null far more
-- often than state being completed suggests. scope names what was taken — a cell, a tenant
-- database — because ADR-0038 makes those different sizes of loss
CREATE TABLE IF NOT EXISTS control.backup_run (
    id                                uuid PRIMARY KEY NOT NULL,
    cell_id                           uuid,
    scope                             text CONSTRAINT backup_run_scope_chk CHECK (scope IN ('cell', 'tenant')),
    started_at                        timestamptz,
    completed_at                      timestamptz,
    state                             text CONSTRAINT backup_run_state_chk CHECK (state IN ('running', 'succeeded', 'failed')),
    size_bytes                        integer,
    restore_tested_at                 timestamptz,
    error                             text
);

-- One flash sale's own environment, from provisioning to teardown (ADR-0035). A cell stood up for
-- a single performance, holding a catalogue snapshot taken at snapshot_taken_at, and it cannot be
-- decommissioned until orders_taken equals orders_reconciled plus orders_rejected — which is what
-- reconciled_at records and why auto_decommission has a grace_minutes rather than a timer. The
-- five timestamps are
CREATE TABLE IF NOT EXISTS control.burst_environment (
    id                                uuid PRIMARY KEY NOT NULL,
    status                            text NOT NULL CONSTRAINT burst_environment_status_chk CHECK (status IN ('requested', 'provisioning', 'warming', 'live', 'draining', 'reconciling', 'reconciled', 'decommissioned', 'failed')),
    performance_id                    uuid NOT NULL,
    cell_name                         text NOT NULL,
    snapshot_taken_at                 timestamptz,
    price_divergence_policy           text CONSTRAINT burst_environment_price_divergence_policy_chk CHECK (price_divergence_policy IN ('honourSnapshot', 'honourCurrent', 'reject')),
    sequence_high                     integer,
    orders_taken                      integer,
    orders_reconciled                 integer,
    orders_rejected                   integer,
    provisioned_at                    timestamptz,
    live_at                           timestamptz,
    drained_at                        timestamptz,
    reconciled_at                     timestamptz,
    decommissioned_at                 timestamptz,
    is_auto_decommission              boolean DEFAULT true,
    grace_minutes                     integer DEFAULT 30,
    teardown_confirmed_at             timestamptz,
    usage_record_id                   uuid
);

-- A deployment and a legal boundary at once (ADR-0001). One per jurisdiction, carrying its cloud
-- provider, region and endpoint. Only CrossRegionService reaches another one, and it moves a
-- pseudonymous link rather than a guest
CREATE TABLE IF NOT EXISTS control.cell (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    kind                              text CONSTRAINT cell_kind_chk CHECK (kind IN ('shared', 'dedicated', 'onPremiseIsolated', 'onPremiseConnected', 'controlPlane', 'burst')),
    cluster_id                        uuid,
    is_reachable                      boolean DEFAULT true,
    last_contact_at                   timestamptz,
    licence_expires_at                timestamptz,
    participates_in_cross_cell        boolean DEFAULT true,
    region_id                         uuid NOT NULL,
    region_name                       text,
    country_code                      text NOT NULL,
    tier                              text NOT NULL CONSTRAINT cell_tier_chk CHECK (tier IN ('shared', 'dedicated', 'isolated', 'clientHosted')),
    status                            text NOT NULL CONSTRAINT cell_status_chk CHECK (status IN ('provisioning', 'active', 'migrating', 'suspended', 'decommissioning', 'failed')),
    cloud_provider                    text,
    cloud_region                      text,
    api_endpoint                      text,
    venue_count                       integer,
    provisioned_at                    timestamptz,
    deployment_ref                    text,
    health                            jsonb
);

-- identical cells serving a region. Scaling out is launching another, not growing one Hangs off: a
-- child of control.cell; reaches control.partner through its keys; references control.cell,
-- platform.scope. Reached by: 2 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS control.cell_cluster (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text,
    region_id                         uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT cell_cluster_kind_chk CHECK (kind IN ('shared', 'dedicated', 'onPremiseIsolated', 'onPremiseConnected', 'controlPlane', 'burst')),
    cell_ids                          text[] NOT NULL,
    schema_version                    text,
    modelled_on_cell_id               uuid,
    status                            text NOT NULL CONSTRAINT cell_cluster_status_chk CHECK (status IN ('provisioning', 'active', 'draining', 'retired')),
    accepting_new_tenants             boolean,
    tenant_count                      integer,
    provisioned_at                    timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.cell_instance (
    id                                uuid PRIMARY KEY NOT NULL,
    cell_id                           uuid NOT NULL,
    name                              text NOT NULL,
    status                            text NOT NULL CONSTRAINT cell_instance_status_chk CHECK (status IN ('provisioning', 'live', 'draining', 'retired')),
    role                              text DEFAULT 'primary' CONSTRAINT cell_instance_role_chk CHECK (role IN ('primary', 'archive', 'burst')),
    supports_synchronous_replication  boolean DEFAULT false,
    max_connections                   integer,
    created_at                        timestamptz,
    retired_at                        timestamptz
);

-- Work running against a cell — provisioning, migration, decommission
CREATE TABLE IF NOT EXISTS control.cell_job (
    id                                uuid PRIMARY KEY NOT NULL,
    cell_id                           uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT cell_job_kind_chk CHECK (kind IN ('provision', 'tierMigration', 'schemaMigration', 'backup', 'restore', 'decommission')),
    status                            text NOT NULL CONSTRAINT cell_job_status_chk CHECK (status IN ('queued', 'running', 'completed', 'failed', 'rolledBack')),
    progress_percent                  integer,
    message                           text,
    error                             text,
    scheduled_for                     timestamptz,
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- Which tenants live in which cell, and under what database name (ADR-0038). The relation that
-- replaced control.cell.tenant_id: a cell is a region and holds many tenants, so a tenant with
-- venues in two regions has two rows, two cells and two databases. database_name does not encode
-- the region — the instance already is the region, and a name that repeats it is a name that can
-- contradict it. status wa
CREATE TABLE IF NOT EXISTS control.cell_tenant (
    id                                uuid PRIMARY KEY NOT NULL,
    cell_id                           uuid NOT NULL,
    tenant_id                         uuid NOT NULL,
    instance_id                       uuid NOT NULL,
    replication_mode                  text,
    pinned_instance                   boolean DEFAULT false,
    database_name                     text NOT NULL,
    status                            text NOT NULL CONSTRAINT cell_tenant_status_chk CHECK (status IN ('provisioning', 'live', 'suspended', 'draining', 'dropped')),
    provisioned_at                    timestamptz,
    dropped_at                        timestamptz
);

-- What is published to an OTA (BL-076). An OTA pulls a feed, caches it and sells against the cache
-- — so the gap between pushes is the oversell window, and the allocation bounds it
CREATE TABLE IF NOT EXISTS control.channel_listing (
    id                                uuid PRIMARY KEY NOT NULL,
    channel_name                      text NOT NULL CONSTRAINT channel_listing_channel_name_chk CHECK (channel_name IN ('viator', 'klook', 'headout', 'getYourGuide', 'tiqets', 'expedia', 'other')),
    product_id                        uuid NOT NULL,
    external_product_ref              text,
    status                            text NOT NULL CONSTRAINT channel_listing_status_chk CHECK (status IN ('draft', 'live', 'paused', 'delisted')),
    allocation_units                  integer,
    price_list_id                     uuid,
    adapter                           text CONSTRAINT channel_listing_adapter_chk CHECK (adapter IN ('viatorApi', 'klookApi', 'headoutApi', 'getYourGuideApi', 'tiqetsApi', 'octoStandard', 'generic')),
    adapter_credential_ref            text,
    push_interval_minutes             integer DEFAULT 15,
    guest_data_scope                  text DEFAULT 'nameOnly' CONSTRAINT channel_listing_guest_data_scope_chk CHECK (guest_data_scope IN ('none', 'nameOnly', 'nameAndContact', 'full')),
    last_pushed_at                    timestamptz,
    scope_path                        ltree NOT NULL
);

-- Authored content with a schedule (BL-172). The CMS modelled configuration and not authoring — a
-- marketer could choose between things a developer had built and could not write something new
CREATE TABLE IF NOT EXISTS control.content_block (
    id                                uuid PRIMARY KEY NOT NULL,
    page_id                           uuid,
    kind                              text NOT NULL CONSTRAINT content_block_kind_chk CHECK (kind IN ('richText', 'image', 'video', 'gallery', 'cta', 'faq', 'form', 'embed', 'productGrid', 'countdown', 'testimonial')),
    position                          integer,
    body                              jsonb,
    locale_variants                   jsonb,
    status                            text NOT NULL CONSTRAINT content_block_status_chk CHECK (status IN ('draft', 'scheduled', 'published', 'expired', 'archived')),
    publish_at                        timestamptz,
    expire_at                         timestamptz,
    audience_segment_id               uuid,
    approved_by_principal_id          uuid,
    scope_path                        ltree NOT NULL
);

-- A credit note against a tenant invoice — TICVAI crediting its own customer, not a venue
-- crediting a guest. Points at the invoice it corrects; an invoice is never edited, it is credited
-- and reissued
CREATE TABLE IF NOT EXISTS control.credit_note (
    id                                uuid PRIMARY KEY NOT NULL,
    credit_note_number                text NOT NULL,
    invoice_id                        text NOT NULL,
    tenant_id                         uuid NOT NULL,
    reason_code                       text NOT NULL CONSTRAINT credit_note_reason_code_chk CHECK (reason_code IN ('billingError', 'serviceCredit', 'disputeResolution', 'goodwill', 'other')),
    reason                            text CONSTRAINT credit_note_reason_chk CHECK (char_length(reason) <= 500),
    settlement                        text NOT NULL CONSTRAINT credit_note_settlement_chk CHECK (settlement IN ('offsetNextInvoice', 'refund')),
    settlement_status                 text CONSTRAINT credit_note_settlement_status_chk CHECK (settlement_status IN ('pending', 'offset', 'refunded')),
    net_amount                        numeric(18,4),
    tax_amount                        numeric(18,4),
    gross_amount                      numeric(18,4) NOT NULL,
    issued_at                         timestamptz NOT NULL,
    issued_by_principal_id            uuid
);

-- One line of a control.credit_note: what is credited, against which invoice line, and for how
-- much
CREATE TABLE IF NOT EXISTS control.credit_note_line (
    credit_note_id                    uuid NOT NULL,
    invoice_line_index                integer,
    description                       text,
    quantity                          numeric(18,4),
    unit_price                        numeric(18,4),
    amount                            numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- A developer organisation (13.1.6–13.1.9). An organisation, because an integration outlives the
-- engineer who built it — and not a tenant or a partner
CREATE TABLE IF NOT EXISTS control.developer_account (
    id                                uuid PRIMARY KEY NOT NULL,
    organisation_name                 text NOT NULL,
    contact_email                     text NOT NULL,
    website_url                       text,
    country_code                      text,
    partner_id                        uuid,
    status                            text NOT NULL CONSTRAINT developer_account_status_chk CHECK (status IN ('pending', 'verified', 'suspended', 'closed')),
    verified_at                       timestamptz
);

-- Dev, staging, production — and which cells are in each. Promotion may require approval and a
-- soak period
CREATE TABLE IF NOT EXISTS control.environment (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT environment_kind_chk CHECK (kind IN ('dev', 'staging', 'production')),
    name                              text NOT NULL,
    cell_ids                          text[],
    requires_approval_to_promote      boolean,
    soak_hours                        integer,
    current_release_version           text,
    is_active                         boolean,
    cell_id                           uuid NOT NULL
);

-- A published third-party integration (13.1.50). A listing, not an installation — the code runs on
-- the developer own infrastructure
CREATE TABLE IF NOT EXISTS control.integration_listing (
    id                                uuid PRIMARY KEY NOT NULL,
    developer_id                      uuid NOT NULL,
    name                              text NOT NULL,
    category                          text NOT NULL CONSTRAINT integration_listing_category_chk CHECK (category IN ('crm', 'marketing', 'accounting', 'hotel', 'transport', 'analytics', 'accessibility', 'other')),
    description                       text,
    integration_url                   text,
    required_scopes                   text[],
    status                            text NOT NULL CONSTRAINT integration_listing_status_chk CHECK (status IN ('draft', 'submitted', 'inReview', 'certified', 'rejected', 'revoked', 'delisted')),
    certified_until                   date,
    certified_against_version         text,
    listing_fee_model                 text CONSTRAINT integration_listing_listing_fee_model_chk CHECK (listing_fee_model IN ('none', 'flat', 'revenueShare')),
    visibility                        text DEFAULT 'public' CONSTRAINT integration_listing_visibility_chk CHECK (visibility IN ('public', 'private'))
);

-- A bill to a tenant. Lines are children
CREATE TABLE IF NOT EXISTS control.invoice (
    id                                uuid PRIMARY KEY NOT NULL,
    invoice_number                    text NOT NULL,
    tenant_id                         uuid NOT NULL,
    period_start                      date NOT NULL,
    period_end                        date NOT NULL,
    status                            text NOT NULL CONSTRAINT invoice_status_chk CHECK (status IN ('draft', 'issued', 'paid', 'overdue', 'disputed', 'cancelled')),
    net_amount                        numeric(18,4),
    tax_amount                        numeric(18,4),
    gross_amount                      numeric(18,4) NOT NULL,
    plan_version_used                 text,
    credited_total                    numeric(18,4),
    issued_at                         timestamptz,
    due_at                            date,
    paid_at                           timestamptz
);

-- One charge on a tenant invoice, traced to the usage that produced it
CREATE TABLE IF NOT EXISTS control.invoice_line (
    invoice_id                        uuid NOT NULL,
    description                       text,
    kind                              text,
    module_code                       text,
    audience                          text,
    metric                            text,
    quantity                          numeric(18,4),
    unit_price                        numeric(18,4),
    amount                            numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Something bought beyond the plan. Hangs off: a child of control.tenant; reaches control.partner
-- through its keys; references control.tenant. Reached by: 8 operations read it and 2 write it; 1
-- tables reference it.
CREATE TABLE IF NOT EXISTS control.licence_add_on (
    tenant_id                         uuid,
    module_key                        text NOT NULL,
    list_price                        numeric(18,4),
    valid_from                        date,
    valid_to                          date,
    note                              text CONSTRAINT licence_add_on_note_chk CHECK (char_length(note) <= 500),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.licence_add_on_limit (
    licence_add_on_id                 uuid NOT NULL,
    metric                            text NOT NULL,
    limit_value                       integer,
    is_overage_allowed                boolean,
    overage_unit_price                numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- A schema change with a version. Plans group them; runs record what happened per cell
CREATE TABLE IF NOT EXISTS control.migration (
    version                           text NOT NULL,
    module                            text NOT NULL,
    description                       text,
    is_reversible                     boolean NOT NULL,
    rollback_tested_at                timestamptz,
    checksum                          text NOT NULL,
    estimated_lock_ms                 integer,
    touches_partitioned_table         boolean,
    applied_cell_count                integer,
    pending_cell_count                integer,
    id                                uuid PRIMARY KEY NOT NULL,
    release_id                        uuid NOT NULL
);

-- A set of migrations to apply together, with the cells they target
CREATE TABLE IF NOT EXISTS control.migration_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    target_version                    text NOT NULL,
    computed_at                       timestamptz NOT NULL,
    expires_at                        timestamptz,
    is_all_reversible                 boolean NOT NULL,
    irreversible                      text[],
    total_estimated_lock_ms           integer,
    scope_path                        ltree NOT NULL
);

-- One cell in a plan, and its own readiness
CREATE TABLE IF NOT EXISTS control.migration_plan_cell (
    migration_plan_id                 uuid NOT NULL,
    cell_id                           uuid,
    cell_name                         text,
    tenant_selection                  text,
    tenant_ids                        text[],
    current_version                   text,
    migrations_to_apply               text[],
    estimated_lock_ms                 integer,
    warnings                          text[],
    id                                uuid PRIMARY KEY NOT NULL
);

-- One execution of a plan. Runs are append-only; a retry is a new run
CREATE TABLE IF NOT EXISTS control.migration_run (
    id                                uuid PRIMARY KEY NOT NULL,
    plan_id                           uuid NOT NULL,
    status                            text NOT NULL CONSTRAINT migration_run_status_chk CHECK (status IN ('queued', 'canary', 'running', 'paused', 'complete', 'failed', 'rolledBack')),
    canary_cell_id                    uuid,
    canary_tenant_id                  uuid,
    tenants_total                     integer,
    tenants_complete                  integer,
    tenants_failed                    integer,
    cells_total                       integer,
    cells_complete                    integer,
    cells_failed                      integer,
    started_by_principal_id           uuid,
    started_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- What happened in one cell during one run. Where a partial failure is named rather than counted
CREATE TABLE IF NOT EXISTS control.migration_run_cell (
    migration_run_id                  uuid NOT NULL,
    cell_id                           uuid NOT NULL,
    cell_name                         text,
    region_name                       text,
    country_code                      text,
    is_canary                         boolean,
    wave                              integer,
    status                            text NOT NULL,
    from_version                      text,
    to_version                        text,
    error                             text,
    started_at                        timestamptz,
    completed_at                      timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What one migration did to one tenant database (ADR-0039). migration_run_cell exists so a partial
-- failure is *named rather than counted*, and once a cell held two hundred tenants it counted: a
-- run that succeeded for 180 and failed for 20 had one row saying failed. This is that row, one
-- level down. database_name is denormalised deliberately — after a drop, the run record still has
-- to say what it tou
CREATE TABLE IF NOT EXISTS control.migration_run_tenant (
    migration_run_id                  uuid NOT NULL,
    tenant_id                         uuid NOT NULL,
    cell_id                           uuid NOT NULL,
    database_name                     text,
    is_canary                         boolean,
    wave                              integer,
    status                            text NOT NULL,
    from_version                      text,
    to_version                        text,
    error                             text,
    started_at                        timestamptz,
    completed_at                      timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A prospect signing themselves up (BL-165). Nothing is provisioned until verification passes — an
-- unverified application that provisions a cell is a cell somebody has to clean up
CREATE TABLE IF NOT EXISTS control.onboarding_application (
    id                                uuid PRIMARY KEY NOT NULL,
    company_name                      text NOT NULL,
    contact_email                     text NOT NULL,
    contact_phone                     text,
    country_code                      text,
    venue_type_template_id            uuid,
    requested_plan_id                 uuid,
    status                            text NOT NULL CONSTRAINT onboarding_application_status_chk CHECK (status IN ('submitted', 'verifying', 'approved', 'provisioning', 'active', 'rejected', 'abandoned')),
    trial_ends_at                     timestamptz,
    rejection_reason                  text,
    provisioned_tenant_id             uuid
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.outbox_relay (
    cell_tenant_id                    uuid PRIMARY KEY NOT NULL,
    holder                            text NOT NULL CONSTRAINT outbox_relay_holder_chk CHECK (char_length(holder) <= 200),
    lease_expires_at                  timestamptz NOT NULL,
    acquired_at                       timestamptz,
    renewed_at                        timestamptz,
    last_polled_at                    timestamptz
);

CREATE TABLE IF NOT EXISTS control.outbox_republish (
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid NOT NULL,
    range_starts_at                   timestamptz NOT NULL,
    range_ends_at                     timestamptz NOT NULL,
    event_names                       text[],
    reason                            text NOT NULL CONSTRAINT outbox_republish_reason_chk CHECK (char_length(reason) <= 500),
    status                            text NOT NULL CONSTRAINT outbox_republish_status_chk CHECK (status IN ('queued', 'running', 'completed', 'failed', 'cancelled')),
    cursor_at                         timestamptz,
    rows_published                    integer NOT NULL DEFAULT 0,
    last_error                        text,
    requested_by_principal_id         uuid NOT NULL,
    requested_at                      timestamptz NOT NULL,
    started_at                        timestamptz,
    finished_at                       timestamptz
);

-- Holds 28 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner (
    id                                uuid PRIMARY KEY NOT NULL,
    legal_entity_name                 text NOT NULL,
    trading_name                      text NOT NULL,
    partner_type                      text NOT NULL,
    registration_number               text,
    tax_vat_number                    text,
    country                           text NOT NULL,
    city                              text,
    registered_address                text,
    business_address                  text,
    website                           text,
    main_telephone                    text,
    general_email                     text,
    preferred_language                text,
    default_currency                  text,
    time_zone                         text,
    account_manager_principal_id      uuid,
    commercial_manager_principal_id   uuid,
    finance_owner_principal_id        uuid,
    operational_owner_principal_id    uuid,
    technical_owner_principal_id      uuid,
    parent_partner_id                 uuid,
    classification_tags               text[],
    status                            text NOT NULL CONSTRAINT partner_status_chk CHECK (status IN ('lead', 'applicant', 'underReview', 'approved', 'configuration', 'active', 'restricted', 'suspended', 'terminated', 'archived')),
    risk_rating                       text CONSTRAINT partner_risk_rating_chk CHECK (risk_rating IN ('low', 'medium', 'high', 'critical')),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Net rate or commission, credit terms, validity. Versioned — an order placed last week used last
-- week’s rate Hangs off: a child of control.partner; reaches control.partner through its keys;
-- references approvals.request, assets.media_asset, control.partner. Reached by: 42 operations
-- read it and 7 write it; 10 tables reference it; written by 2 contracts — approvals,
-- subscription.
CREATE TABLE IF NOT EXISTS control.partner_agreement (
    id                                uuid PRIMARY KEY,
    partner_id                        uuid NOT NULL,
    version                           integer,
    status                            text CONSTRAINT partner_agreement_status_chk CHECK (status IN ('pendingApproval', 'active', 'expiringSoon', 'expired', 'suspended', 'terminated')),
    rate_mode                         text NOT NULL CONSTRAINT partner_agreement_rate_mode_chk CHECK (rate_mode IN ('netRate', 'commission')),
    commission_percent                numeric(18,4),
    volume_window                     text CONSTRAINT partner_agreement_volume_window_chk CHECK (volume_window IN ('calendarMonth', 'calendarQuarter', 'calendarYear', 'agreementYear', 'rolling12Months')),
    segment_tier                      text,
    branding_asset_id                 uuid,
    storefront_subdomain              text,
    sponsorship                       jsonb,
    credit_term_days                  integer,
    accepted_by_principal_id          uuid,
    accepted_version                  integer,
    accepted_at                       timestamptz,
    signature_ref                     text,
    settlement_currency               text,
    fx_policy                         text DEFAULT 'rateAtSale' CONSTRAINT partner_agreement_fx_policy_chk CHECK (fx_policy IN ('rateAtSale', 'rateAtInvoice', 'fixedRate')),
    fixed_rate                        numeric(18,4),
    credit_limit                      numeric(18,4),
    allowed_channels                  text[],
    allowed_venue_ids                 text[],
    requires_approval_above_value     numeric(18,4),
    valid_from                        date NOT NULL,
    valid_to                          date,
    expiry_alert_days                 integer DEFAULT 30,
    approval_request_id               uuid,
    notes                             text,
    agreement_name                    text,
    agreement_type                    text,
    contract_reference                text,
    legal_entity_id                   uuid,
    brand_id                          uuid,
    territory                         text,
    commercial_owner_principal_id     uuid,
    finance_owner_principal_id        uuid,
    pricing_basis                     text CONSTRAINT partner_agreement_pricing_basis_chk CHECK (pricing_basis IN ('retailPrice', 'netRate', 'discountFromRetail', 'markup', 'derivedRate')),
    payment_model                     text CONSTRAINT partner_agreement_payment_model_chk CHECK (payment_model IN ('creditAccount', 'prepaid', 'payPerTransaction')),
    renewal_type                      text CONSTRAINT partner_agreement_renewal_type_chk CHECK (renewal_type IN ('manual', 'auto')),
    renewal_notice_days               integer,
    is_renegotiation_required         boolean DEFAULT false,
    renewal_requires_approval         boolean,
    minimum_commitment                integer,
    sales_target                      numeric(18,4),
    agreement_value                   numeric(18,4),
    commission_terms                  text,
    credit_terms                      text,
    allocation_terms                  text,
    cancellation_conditions           text,
    refund_conditions                 text,
    booking_restrictions              text,
    settlement_terms                  text,
    scope_path                        ltree NOT NULL
);

-- Holds 23 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_allocation (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    agreement_id                      uuid NOT NULL,
    venue_id                          uuid,
    event_id                          uuid,
    product_id                        uuid,
    ticket_type                       text,
    allocation_model                  text NOT NULL CONSTRAINT partner_allocation_allocation_model_chk CHECK (allocation_model IN ('guaranteed', 'onRequest', 'shared', 'fixedQuantity', 'percentage', 'rolling', 'seasonal')),
    quantity                          integer,
    allocation_percent                numeric(18,4),
    minimum_commitment                integer,
    maximum_allocation                integer,
    commitment_rule                   text CONSTRAINT partner_allocation_commitment_rule_chk CHECK (commitment_rule IN ('useItOrRelease', 'takeOrPay', 'guaranteedMinimum')),
    sell_through_target               numeric(18,4),
    return_rule                       text,
    release_mode                      text NOT NULL CONSTRAINT partner_allocation_release_mode_chk CHECK (release_mode IN ('automatic', 'manual')),
    release_hours_before_event        integer,
    release_date                      timestamptz,
    per_member_limit                  integer,
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 31 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_application (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid,
    company_name                      text NOT NULL,
    trading_name                      text,
    country                           text,
    requested_partner_type            text,
    markets                           text[],
    expected_sales_volume             integer,
    requested_products                text[],
    requested_venues                  text[],
    preferred_distribution_method     text CONSTRAINT partner_application_preferred_distribution_method_chk CHECK (preferred_distribution_method IN ('b2bPortal', 'api', 'otaConnection', 'agentPortal', 'affiliateLink', 'voucherDistribution', 'bulkTicketExport', 'other')),
    estimated_annual_business         numeric(18,4),
    contact_name                      text,
    contact_email                     text,
    billing_requirements              text,
    business_case                     text,
    territory                         text,
    credit_request                    numeric(18,4),
    payment_terms                     text,
    tax_registration_number           text,
    product_requirements              text,
    fulfillment_requirements          text,
    api_integration_requirements      text,
    stage                             text NOT NULL DEFAULT 'application' CONSTRAINT partner_application_stage_chk CHECK (stage IN ('application', 'businessVerification', 'documentation', 'commercialReview', 'financeReview', 'technicalReview', 'approval', 'configuration', 'activation')),
    status                            text NOT NULL DEFAULT 'submitted' CONSTRAINT partner_application_status_chk CHECK (status IN ('submitted', 'inReview', 'moreInformationRequested', 'approved', 'rejected', 'withdrawn')),
    submitted_at                      timestamptz NOT NULL,
    sla_due_at                        timestamptz,
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_application_review_task (
    partner_application_id            uuid NOT NULL,
    department                        text NOT NULL,
    assignee_principal_id             uuid,
    due_at                            timestamptz,
    is_completed                      boolean NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_billing_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    agreement_id                      uuid NOT NULL,
    consolidated_billing              boolean DEFAULT false,
    billing_entity_name               text,
    invoice_frequency                 text NOT NULL CONSTRAINT partner_billing_profile_invoice_frequency_chk CHECK (invoice_frequency IN ('perTransaction', 'weekly', 'monthly')),
    invoice_grouping                  text CONSTRAINT partner_billing_profile_invoice_grouping_chk CHECK (invoice_grouping IN ('perPartner', 'perBranch', 'perVenue', 'perEvent', 'perPurchaseOrder')),
    statement_frequency               text CONSTRAINT partner_billing_profile_statement_frequency_chk CHECK (statement_frequency IN ('weekly', 'monthly')),
    tax_profile_id                    text,
    is_purchase_order_required        boolean DEFAULT false,
    billing_contact_id                uuid,
    finance_email                     text,
    allowed_payment_methods           text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_booking_limit (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid,
    agreement_id                      uuid,
    maximum_tickets_per_booking       integer,
    maximum_booking_value             numeric(18,4),
    daily_booking_limit               integer,
    monthly_booking_limit             integer,
    event_limit                       integer,
    product_limit                     integer,
    hold_limit                        integer,
    hold_duration_minutes             integer,
    cancellation_limit_percent        numeric(18,4),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_capability_grant (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    capability                        text NOT NULL CONSTRAINT partner_capability_grant_capability_chk CHECK (capability IN ('searchAvailability', 'createBooking', 'holdInventory', 'confirmBooking', 'cancelBooking', 'modifyBooking', 'rescheduleBooking', 'downloadTicket', 'printTicket', 'sendTicket', 'accessCustomerDetails', 'useCredit', 'usePaymentCard', 'viewCommission', 'viewNetRates', 'accessReports', 'exportData', 'useApi', 'createSubAgents', 'refund', 'manualPriceOverride', 'creditAdjustment', 'highValueBooking', 'customerDataExport')),
    is_allowed                        boolean NOT NULL,
    requires_internal_approval        boolean DEFAULT false,
    grant_type                        text NOT NULL CONSTRAINT partner_capability_grant_grant_type_chk CHECK (grant_type IN ('permanent', 'temporary', 'seasonal', 'eventSpecific')),
    effective_from                    date,
    effective_to                      date,
    event_id                          uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_case (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    contact_id                        uuid,
    category                          text NOT NULL CONSTRAINT partner_case_category_chk CHECK (category IN ('bookingDispute', 'pricingDispute', 'commissionDispute', 'creditDispute', 'invoiceDispute', 'cancellationDispute', 'ticketIssue', 'allocationIssue', 'apiIssue', 'settlementDispute')),
    priority                          text NOT NULL CONSTRAINT partner_case_priority_chk CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    order_id                          uuid,
    invoice_reference                 text,
    settlement_batch_id               uuid,
    amount_in_dispute                 numeric(18,4),
    description                       text NOT NULL,
    evidence                          text[],
    owner_principal_id                uuid,
    sla_policy_id                     uuid,
    status                            text NOT NULL DEFAULT 'open' CONSTRAINT partner_case_status_chk CHECK (status IN ('open', 'assigned', 'investigating', 'waitingPartner', 'waitingInternal', 'resolutionProposed', 'resolved', 'closed')),
    first_response_at                 timestamptz,
    resolution_target_at              timestamptz NOT NULL,
    resolved_at                       timestamptz,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 28 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_change_request (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    order_id                          uuid NOT NULL,
    request_type                      text NOT NULL CONSTRAINT partner_change_request_request_type_chk CHECK (request_type IN ('fullCancellation', 'partialCancellation', 'dateChange', 'performanceChange', 'quantityReduction', 'productChange', 'ticketReissue', 'customerNameChange', 'refundRequest')),
    quantity                          integer,
    reason                            text,
    original_state                    text,
    new_state                         text,
    original_value                    numeric(18,4),
    is_cancellation_allowed           boolean,
    cancellation_fee                  numeric(18,4),
    refund_or_credit                  numeric(18,4),
    financial_impact                  numeric(18,4),
    allocation_impact                 integer,
    commission_adjustment             numeric(18,4),
    approval_reasons                  text[],
    status                            text NOT NULL DEFAULT 'requested' CONSTRAINT partner_change_request_status_chk CHECK (status IN ('requested', 'pendingApproval', 'approved', 'rejected', 'processed')),
    requested_by_principal_id         uuid,
    approved_by_principal_id          uuid,
    approval_request_id               uuid,
    refund_id                         uuid,
    requested_at                      timestamptz NOT NULL,
    target_performance_id             uuid,
    target_product_id                 uuid,
    new_customer_name                 text,
    is_fee_waiver_requested           boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_commercial_exception (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    agreement_id                      uuid,
    request_type                      text NOT NULL CONSTRAINT partner_commercial_exception_request_type_chk CHECK (request_type IN ('priceException', 'creditException', 'allocationException', 'commissionException', 'bookingLimitException', 'paymentTermException', 'cancellationException')),
    current_rule                      text,
    requested_exception               text NOT NULL,
    amount_impact                     numeric(18,4),
    reason                            text,
    effective_from                    date,
    effective_to                      date,
    requested_by_principal_id         uuid,
    status                            text NOT NULL DEFAULT 'pendingApproval' CONSTRAINT partner_commercial_exception_status_chk CHECK (status IN ('pendingApproval', 'approved', 'rejected', 'returned', 'expired')),
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 23 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_commission_line (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    agreement_id                      uuid NOT NULL,
    agreement_version                 integer NOT NULL,
    order_id                          uuid NOT NULL,
    product_id                        uuid,
    gross_value                       numeric(18,4),
    net_rate                          numeric(18,4),
    commission_basis                  numeric(18,4),
    commission_percent                numeric(18,4),
    commission_amount                 numeric(18,4),
    incentive                         numeric(18,4),
    adjustment                        numeric(18,4),
    adjustment_reason                 text CONSTRAINT partner_commission_line_adjustment_reason_chk CHECK (adjustment_reason IN ('cancellation', 'refund', 'chargeback', 'partialFulfillment', 'commissionCorrection', 'incentiveQualification')),
    payable_amount                    numeric(18,4),
    settlement_period                 text CONSTRAINT partner_commission_line_settlement_period_chk CHECK (settlement_period IN ('perTransaction', 'weekly', 'monthly', 'eventBased', 'customCycle')),
    period                            text,
    legal_entity_id                   uuid,
    status                            text NOT NULL DEFAULT 'calculated' CONSTRAINT partner_commission_line_status_chk CHECK (status IN ('calculated', 'reconciled', 'financeReview', 'approved', 'scheduled', 'paid', 'onHold', 'disputed', 'reversed')),
    settlement_batch_id               uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_commission_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    agreement_id                      uuid NOT NULL,
    commission_model                  text NOT NULL CONSTRAINT partner_commission_rule_commission_model_chk CHECK (commission_model IN ('fixedPercentage', 'fixedAmount', 'productSpecific', 'tiered', 'volumeBased', 'revenueBased', 'performanceIncentive', 'campaignIncentive')),
    product_id                        uuid,
    product_category                  text,
    venue_id                          uuid,
    event_id                          uuid,
    market                            text,
    sales_channel                     text,
    commission_percent                numeric(18,4),
    commission_amount                 numeric(18,4),
    volume_window                     text CONSTRAINT partner_commission_rule_volume_window_chk CHECK (volume_window IN ('calendarMonth', 'calendarQuarter', 'calendarYear', 'agreementYear', 'rolling12Months')),
    incentive_type                    text CONSTRAINT partner_commission_rule_incentive_type_chk CHECK (incentive_type IN ('volumeBonus', 'growthBonus', 'targetAchievement', 'seasonalIncentive', 'newProductIncentive', 'strategicPartnerBonus')),
    effective_from                    date NOT NULL,
    effective_to                      date,
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_commission_rule_tier (
    partner_commission_rule_id        uuid NOT NULL,
    from_units                        integer NOT NULL,
    commission_percent                numeric(18,4) NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_contact (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    name                              text NOT NULL,
    position                          text,
    department                        text,
    email                             text,
    mobile                            text,
    telephone                         text,
    language                          text,
    time_zone                         text,
    contact_type                      text NOT NULL CONSTRAINT partner_contact_contact_type_chk CHECK (contact_type IN ('primary', 'commercial', 'reservations', 'finance', 'technical', 'operations', 'management', 'emergency')),
    principal_id                      uuid,
    status                            text NOT NULL DEFAULT 'active' CONSTRAINT partner_contact_status_chk CHECK (status IN ('invited', 'active', 'disabled', 'revoked', 'expired')),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_credit_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    agreement_id                      uuid NOT NULL,
    is_credit_enabled                 boolean NOT NULL DEFAULT false,
    temporary_credit_limit            numeric(18,4),
    temporary_limit_until             date,
    credit_owner_principal_id         uuid,
    approval_authority                text,
    risk_classification               text CONSTRAINT partner_credit_profile_risk_classification_chk CHECK (risk_classification IN ('low', 'medium', 'high', 'critical')),
    warning_threshold_percent         numeric(18,4) DEFAULT 70,
    high_risk_threshold_percent       numeric(18,4) DEFAULT 90,
    block_threshold_percent           numeric(18,4) DEFAULT 100,
    credit_status                     text NOT NULL DEFAULT 'notEnabled' CONSTRAINT partner_credit_profile_credit_status_chk CHECK (credit_status IN ('notEnabled', 'withinLimit', 'warning', 'highRisk', 'onHold', 'blocked')),
    effective_from                    date,
    effective_to                      date,
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 21 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_distribution_right (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    country                           text,
    region                            text,
    city                              text,
    market                            text,
    brand_id                          uuid,
    venue_id                          uuid,
    attraction_id                     uuid,
    event_id                          uuid,
    is_allowed                        boolean NOT NULL,
    distribution_methods              text[],
    exclusivity                       text NOT NULL CONSTRAINT partner_distribution_right_exclusivity_chk CHECK (exclusivity IN ('nonExclusive', 'exclusive', 'preferred', 'restricted')),
    sub_agent_rule                    text CONSTRAINT partner_distribution_right_sub_agent_rule_chk CHECK (sub_agent_rule IN ('allowed', 'prohibited', 'approvalRequired')),
    maximum_hierarchy_depth           integer,
    effective_from                    date NOT NULL,
    effective_to                      date,
    review_date                       date,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_document (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    agreement_id                      uuid,
    document_type                     text NOT NULL,
    document_number                   text,
    issue_date                        date,
    expiry_date                       date,
    issuing_authority                 text,
    file_ref                          text,
    verification_status               text NOT NULL DEFAULT 'missing' CONSTRAINT partner_document_verification_status_chk CHECK (verification_status IN ('missing', 'uploaded', 'underReview', 'verified', 'rejected', 'expiring', 'expired')),
    verified_by_principal_id          uuid,
    verified_at                       timestamptz,
    is_mandatory                      boolean DEFAULT false,
    expiry_action                     text CONSTRAINT partner_document_expiry_action_chk CHECK (expiry_action IN ('warnOnly', 'blockNewBookings', 'blockCreditTransactions', 'suspendPartner', 'requireManualReview')),
    notes                             text,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 30 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_rate (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    agreement_id                      uuid NOT NULL,
    product_id                        uuid,
    product_family                    text,
    venue_id                          uuid,
    event_id                          uuid,
    ticket_type                       text,
    price_category                    text,
    market                            text,
    channel                           text,
    pricing_model                     text NOT NULL CONSTRAINT partner_rate_pricing_model_chk CHECK (pricing_model IN ('retailPrice', 'netRate', 'discountFromRetail', 'markup', 'derivedRate')),
    net_rate                          numeric(18,4),
    discount_percent                  numeric(18,4),
    max_markup_percent                numeric(18,4),
    pricing_profile_id                text,
    seasonal_rate                     boolean DEFAULT false,
    effective_from                    date NOT NULL,
    effective_to                      date,
    blackout_dates                    text[],
    event_exceptions                  text[],
    minimum_permitted_rate            numeric(18,4),
    max_discount_percent              numeric(18,4),
    margin_floor                      numeric(18,4),
    is_manual_override_allowed        boolean DEFAULT false,
    approval_threshold                numeric(18,4),
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_rate_volume_band (
    partner_rate_id                   uuid NOT NULL,
    from_units                        integer NOT NULL,
    discount_percent                  numeric(18,4) NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_reconciliation_exception (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    order_id                          uuid,
    partner_reference                 text,
    compared_source                   text NOT NULL CONSTRAINT partner_reconciliation_exception_compared_source_chk CHECK (compared_source IN ('ticvaiOrders', 'ticketsIssued', 'partnerRates', 'paymentsCredit', 'commission', 'invoices', 'cancellationsRefunds')),
    mismatch_type                     text NOT NULL CONSTRAINT partner_reconciliation_exception_mismatch_type_chk CHECK (mismatch_type IN ('missingTransaction', 'duplicateTransaction', 'price', 'quantity', 'tax', 'commission', 'payment', 'cancellation', 'settlement')),
    partner_amount                    numeric(18,4),
    ticvai_amount                     numeric(18,4),
    status                            text NOT NULL DEFAULT 'open' CONSTRAINT partner_reconciliation_exception_status_chk CHECK (status IN ('open', 'investigating', 'matched', 'corrected', 'differenceAccepted', 'adjusted', 'disputed', 'escalated')),
    assignee_principal_id             uuid,
    root_cause_group                  text,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_scope_assignment (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    brand_id                          uuid,
    venue_id                          uuid,
    attraction_id                     uuid,
    business_unit                     text,
    event_portfolio                   text,
    market                            text,
    is_authorized                     boolean NOT NULL,
    start_date                        date NOT NULL,
    end_date                          date,
    seasonal_scope                    boolean DEFAULT false,
    scope_exclusions                  text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_security (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    agreement_id                      uuid,
    security_type                     text NOT NULL CONSTRAINT partner_security_security_type_chk CHECK (security_type IN ('cashDeposit', 'bankGuarantee', 'securityDeposit', 'letterOfCredit', 'prepaymentBalance', 'corporateGuarantee', 'other')),
    amount                            numeric(18,4) NOT NULL,
    currency                          text NOT NULL,
    issuing_institution               text,
    reference                         text,
    effective_date                    date NOT NULL,
    expiry_date                       date,
    document_id                       uuid,
    verification_status               text NOT NULL DEFAULT 'pending' CONSTRAINT partner_security_verification_status_chk CHECK (verification_status IN ('pending', 'verified', 'rejected', 'expired')),
    expiry_action                     text CONSTRAINT partner_security_expiry_action_chk CHECK (expiry_action IN ('generateWarning', 'reduceCredit', 'blockNewCreditSales', 'placePartnerOnHold', 'requireFinanceReview')),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_settlement_batch (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    legal_entity_id                   uuid,
    currency                          text NOT NULL,
    period                            text NOT NULL,
    settlement_period                 text CONSTRAINT partner_settlement_batch_settlement_period_chk CHECK (settlement_period IN ('perTransaction', 'weekly', 'monthly', 'eventBased', 'customCycle')),
    status                            text NOT NULL DEFAULT 'calculated' CONSTRAINT partner_settlement_batch_status_chk CHECK (status IN ('calculated', 'reconciled', 'financeReview', 'approved', 'scheduled', 'paid', 'onHold', 'disputed', 'reversed')),
    scheduled_date                    date,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.partner_status_history (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    action                            text NOT NULL CONSTRAINT partner_status_history_action_chk CHECK (action IN ('approve', 'activate', 'restrict', 'suspend', 'reactivate', 'terminate', 'archive')),
    from_status                       text CONSTRAINT partner_status_history_from_status_chk CHECK (from_status IN ('lead', 'applicant', 'underReview', 'approved', 'configuration', 'active', 'restricted', 'suspended', 'terminated', 'archived')),
    to_status                         text NOT NULL CONSTRAINT partner_status_history_to_status_chk CHECK (to_status IN ('lead', 'applicant', 'underReview', 'approved', 'configuration', 'active', 'restricted', 'suspended', 'terminated', 'archived')),
    reason_category                   text NOT NULL CONSTRAINT partner_status_history_reason_category_chk CHECK (reason_category IN ('commercial', 'compliance', 'credit', 'fraud', 'contractExpiry', 'performance', 'technical', 'managementDecision')),
    reason_note                       text,
    suspension_scope                  text CONSTRAINT partner_status_history_suspension_scope_chk CHECK (suspension_scope IN ('full', 'selected')),
    restrictions                      text[],
    restricted_venue_ids              text[],
    restricted_markets                text[],
    effective_from                    timestamptz NOT NULL,
    requested_by_principal_id         uuid,
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz
);

-- A principal on a partner branch (2.7.51, BL-075). A partner was a flat account. Quota and credit
-- resolve nearest-ancestor-wins, like configuration
CREATE TABLE IF NOT EXISTS control.partner_user (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    principal_id                      uuid NOT NULL,
    role                              text,
    sales_location                    text,
    currency                          text,
    account_expires_at                timestamptz,
    branch_scope_path                 ltree NOT NULL,
    allocation_quota                  integer,
    credit_limit_override             numeric(18,4),
    can_manage_users                  boolean DEFAULT false
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.production_access_request (
    id                                uuid PRIMARY KEY NOT NULL,
    developer_id                      uuid NOT NULL,
    sandbox_client_id                 uuid NOT NULL,
    listing_id                        uuid NOT NULL,
    scopes                            text[],
    allowed_tenant_ids                text[],
    ip_allow_list                     text[],
    note                              text,
    status                            text NOT NULL CONSTRAINT production_access_request_status_chk CHECK (status IN ('pending', 'approved', 'rejected', 'withdrawn')),
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    reason                            text,
    production_client_id              uuid,
    requested_at                      timestamptz
);

-- a shipped version. Promoted through dev, staging and production; superseded by a later one Hangs
-- off: reaches control.partner through its keys; references identity.principal. Reached by: 5
-- operations read it and 3 write it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS control.release (
    version                           text NOT NULL,
    required_migrations               text[],
    note                              text NOT NULL CONSTRAINT release_note_chk CHECK (char_length(note) <= 2000),
    guest_release_notes               jsonb,
    breaking_changes                  text[],
    id                                uuid PRIMARY KEY NOT NULL,
    status                            text NOT NULL CONSTRAINT release_status_chk CHECK (status IN ('draft', 'inDev', 'inStaging', 'inProduction', 'superseded', 'withdrawn')),
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL,
    promoted_to_staging_at            timestamptz,
    promoted_to_production_at         timestamptz,
    plan_id                           uuid NOT NULL
);

-- One service and version inside a release. A release is not a single artefact
CREATE TABLE IF NOT EXISTS control.release_component (
    release_id                        uuid NOT NULL,
    component                         text NOT NULL,
    version                           text NOT NULL,
    image_digest                      text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- One release reaching cells, in waves, with a canary first
CREATE TABLE IF NOT EXISTS control.rollout (
    id                                uuid PRIMARY KEY NOT NULL,
    release_id                        uuid NOT NULL,
    environment                       text NOT NULL CONSTRAINT rollout_environment_chk CHECK (environment IN ('dev', 'staging', 'production')),
    status                            text NOT NULL CONSTRAINT rollout_status_chk CHECK (status IN ('queued', 'canary', 'rolling', 'paused', 'complete', 'failed', 'rolledBack')),
    cells_total                       integer,
    cells_complete                    integer,
    cells_failed                      integer,
    started_by_principal_id           uuid,
    approved_by_principal_id          uuid,
    paused_reason                     text,
    started_at                        timestamptz NOT NULL,
    completed_at                      timestamptz,
    reinventory_hold_id               uuid
);

-- One cell in a rollout — its wave, whether it is the canary, and what version it moved between
CREATE TABLE IF NOT EXISTS control.rollout_cell (
    rollout_id                        uuid NOT NULL,
    cell_id                           uuid NOT NULL,
    cell_name                         text,
    region_name                       text,
    country_code                      text,
    is_canary                         boolean,
    wave                              integer,
    status                            text NOT NULL CONSTRAINT rollout_cell_status_chk CHECK (status IN ('pending', 'running', 'complete', 'failed', 'skipped', 'rolledBack')),
    from_version                      text,
    to_version                        text,
    error                             text,
    started_at                        timestamptz,
    completed_at                      timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- How far a release has reached into one tenant database (ADR-0039). The per-tenant sibling of
-- control.rollout_cell, which stays as the regional rollup. The canary is a tenant, not a cell —
-- the point of a canary is that its failure is cheap, and a first cell holding two hundred
-- databases is not a cheap failure. wave is therefore a set of tenants, and it may be a subset of
-- one cell
CREATE TABLE IF NOT EXISTS control.rollout_tenant (
    tenant_id                         uuid NOT NULL,
    cell_id                           uuid NOT NULL,
    database_name                     text,
    is_canary                         boolean,
    wave                              integer,
    status                            text NOT NULL CONSTRAINT rollout_tenant_status_chk CHECK (status IN ('pending', 'running', 'complete', 'failed', 'skipped', 'rolledBack')),
    from_version                      text,
    to_version                        text,
    error                             text,
    started_at                        timestamptz,
    completed_at                      timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A developer sandbox (13.2.1, D2/D3). Synthetic data only — no cloning, no masking, which removes
-- the PDPL and DESC exposure entirely
CREATE TABLE IF NOT EXISTS control.sandbox (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    developer_id                      uuid,
    status                            text NOT NULL CONSTRAINT sandbox_status_chk CHECK (status IN ('provisioning', 'active', 'resetting', 'expired', 'deleted')),
    data_profile                      jsonb NOT NULL,
    contains_production_data          boolean DEFAULT false,
    expires_at                        timestamptz,
    last_reset_at                     timestamptz
);

-- The bounds a service scales within inside one cell, not the scaling itself. replica_floor and
-- replica_ceiling are the decision; target_utilisation_pct and scale_step_pct are how fast it
-- moves between them. A ceiling is a cost limit and a floor is an availability one, and a cell
-- that hits its ceiling under load is a capacity decision someone has to take rather than a fault
-- to page on
CREATE TABLE IF NOT EXISTS control.scaling_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    cell_id                           uuid,
    service                           text,
    replica_floor                     integer,
    replica_ceiling                   integer,
    target_utilisation_pct            integer,
    scale_step_pct                    integer,
    updated_at                        timestamptz
);

-- Titles, canonicals, hreflang and schema markup (22.11). An attraction that does not appear in
-- search sells through OTAs at OTA commission. Hangs off: reaches control.partner through its
-- keys. Reached by: 2 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS control.seo_metadata (
    id                                uuid PRIMARY KEY NOT NULL,
    entity_kind                       text NOT NULL CONSTRAINT seo_metadata_entity_kind_chk CHECK (entity_kind IN ('contentPage', 'product', 'event', 'performance', 'membership', 'promotion', 'venue')),
    entity_id                         uuid NOT NULL,
    locale                            text,
    title                             text,
    meta_description                  text,
    keywords                          text[],
    canonical_url                     text,
    slug                              text,
    hreflang                          jsonb,
    schema_org_type                   text,
    open_graph                        jsonb,
    is_auto_generated                 boolean DEFAULT true,
    no_index                          boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- Something the platform is telling tenants, scheduled or in progress
CREATE TABLE IF NOT EXISTS control.support_notice (
    id                                uuid PRIMARY KEY NOT NULL,
    version                           text NOT NULL,
    support_ends_at                   date NOT NULL,
    message                           jsonb,
    affected_tenant_ids               text[],
    published_by_principal_id         uuid,
    published_at                      timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- A customer of the platform — the root of the org tree. platform.tenant is a one-column
-- projection of this, so a cell can resolve its own tenant without reaching across a residency
-- boundary
CREATE TABLE IF NOT EXISTS control.tenant (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    status                            text NOT NULL CONSTRAINT tenant_status_chk CHECK (status IN ('onboarding', 'active', 'suspended', 'terminating', 'terminated')),
    suspension_mode                   text CONSTRAINT tenant_suspension_mode_chk CHECK (suspension_mode IN ('readOnly', 'noNewSales', 'fullLockout')),
    suspension_reason                 text,
    suspension_effective_at           timestamptz,
    suspension_notice_message         jsonb,
    termination_scheduled_at          timestamptz,
    termination_retention_until       timestamptz,
    termination_reason                text CONSTRAINT tenant_termination_reason_chk CHECK (char_length(termination_reason) <= 1000),
    termination_requested_by_principal_id uuid,
    plan_id                           uuid,
    plan_name                         text,
    cell_count                        integer,
    venue_count                       integer,
    region_id                         uuid,
    billing_email                     text,
    billing_address                   text CONSTRAINT tenant_billing_address_chk CHECK (char_length(billing_address) <= 500),
    account_manager_principal_id      uuid,
    created_at                        timestamptz NOT NULL,
    activated_at                      timestamptz,
    subscription_id                   uuid
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.tenant_domain (
    id                                uuid PRIMARY KEY,
    hostname                          text NOT NULL CONSTRAINT tenant_domain_hostname_chk CHECK (char_length(hostname) <= 253),
    tenant_id                         uuid NOT NULL,
    cell_id                           uuid,
    database_name                     text CONSTRAINT tenant_domain_database_name_chk CHECK (char_length(database_name) <= 63),
    kind                              text NOT NULL CONSTRAINT tenant_domain_kind_chk CHECK (kind IN ('platformSubdomain', 'customDomain')),
    channel                           text CONSTRAINT tenant_domain_channel_chk CHECK (channel IN ('guestWeb', 'backOffice', 'partnerPortal', 'developerPortal')),
    status                            text NOT NULL CONSTRAINT tenant_domain_status_chk CHECK (status IN ('active', 'detached')),
    verified_at                       timestamptz
);

-- a tenant moving between cells — shared to dedicated, or rebalancing Hangs off: a child of
-- control.tenant; reaches control.partner through its keys; references control.cell,
-- control.tenant, control.tenant_migration_plan. Reached by: 3 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS control.tenant_migration (
    id                                uuid PRIMARY KEY NOT NULL,
    plan_id                           uuid NOT NULL,
    tenant_id                         uuid NOT NULL,
    from_cell_id                      uuid,
    to_cell_id                        uuid,
    reason                            text,
    status                            text NOT NULL CONSTRAINT tenant_migration_status_chk CHECK (status IN ('planned', 'copying', 'verifying', 'awaitingCutover', 'cuttingOver', 'complete', 'failed', 'rolledBack')),
    rows_copied                       integer,
    rows_expected                     integer,
    is_verification_passed            boolean,
    cutover_at                        timestamptz,
    source_retained_until             timestamptz,
    started_at                        timestamptz NOT NULL,
    completed_at                      timestamptz,
    error                             text
);

-- computed against cell state; expires, because a plan made for a different world is not a plan
-- Hangs off: a child of control.tenant; reaches control.partner through its keys; references
-- control.cell, control.tenant. Reached by: 1 operations read it and 1 write it; 1 tables
-- reference it.
CREATE TABLE IF NOT EXISTS control.tenant_migration_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid NOT NULL,
    from_cell_id                      uuid NOT NULL,
    to_cell_id                        uuid NOT NULL,
    from_kind                         text CONSTRAINT tenant_migration_plan_from_kind_chk CHECK (from_kind IN ('shared', 'dedicated', 'onPremiseIsolated', 'onPremiseConnected', 'controlPlane', 'burst')),
    to_kind                           text CONSTRAINT tenant_migration_plan_to_kind_chk CHECK (to_kind IN ('shared', 'dedicated', 'onPremiseIsolated', 'onPremiseConnected', 'controlPlane', 'burst')),
    can_proceed                       boolean NOT NULL,
    row_counts                        jsonb,
    estimated_copy_minutes            integer,
    estimated_cutover_seconds         integer,
    cross_region_links_to_repoint     integer,
    computed_at                       timestamptz NOT NULL,
    expires_at                        timestamptz
);

-- When a tenant has agreed to be upgraded. Not every tenant takes a release the day it ships
CREATE TABLE IF NOT EXISTS control.upgrade_schedule (
    tenant_id                         uuid NOT NULL,
    tenant_name                       text,
    release_version                   text NOT NULL,
    scheduled_for                     timestamptz NOT NULL,
    deferred_by_tenant                boolean,
    deferral_reason                   text,
    max_deferral_until                timestamptz,
    notified_at                       timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- 301s and 302s for retired content (22.11.7). A redirect chain loses ranking at every hop, so a
-- new one pointing at a redirect is collapsed
CREATE TABLE IF NOT EXISTS control.url_redirect (
    id                                uuid PRIMARY KEY NOT NULL,
    from_path                         text NOT NULL,
    to_path                           text NOT NULL,
    status_code                       text NOT NULL,
    reason                            text CONSTRAINT url_redirect_reason_chk CHECK (reason IN ('contentMigrated', 'pageRetired', 'campaignExpired', 'restructure', 'slugChanged')),
    created_at                        timestamptz,
    hit_count                         integer,
    is_active                         boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- What a tenant consumed, which is what an invoice is computed from
CREATE TABLE IF NOT EXISTS control.usage_record (
    id                                uuid PRIMARY KEY NOT NULL,
    metric                            text NOT NULL CONSTRAINT usage_record_metric_chk CHECK (metric IN ('venues', 'workstations', 'activeUsers', 'devices', 'brandedApps', 'aiTokens', 'apiCalls', 'storageGb', 'transactions', 'guestProfiles')),
    quantity                          numeric(18,4) NOT NULL,
    venue_id                          uuid,
    capability                        text,
    audience                          text CONSTRAINT usage_record_audience_chk CHECK (audience IN ('staff', 'guest')),
    recorded_at                       timestamptz NOT NULL
);

-- What a venue of this kind starts with (BL-165). A water park and a theatre need different
-- defaults, and configuring 300 settings from empty is asking a prospect to leave
CREATE TABLE IF NOT EXISTS control.venue_type_template (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    venue_kind                        text NOT NULL CONSTRAINT venue_type_template_venue_kind_chk CHECK (venue_kind IN ('themePark', 'waterPark', 'museum', 'theatre', 'stadium', 'arena', 'zoo', 'aquarium', 'cinema', 'attraction', 'mixed')),
    seeds_product_kinds               text[],
    seeds_roles                       text[],
    seeds_admission_profiles          text[],
    seeds_reports                     text[]
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS control.waf_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    cell_id                           uuid,
    name                              text,
    action                            text CONSTRAINT waf_rule_action_chk CHECK (action IN ('allow', 'block', 'rateLimit', 'challenge')),
    match_on                          text,
    pattern                           text,
    is_enabled                        boolean,
    hit_count24h                      integer,
    updated_at                        timestamptz
);

-- What was sent and what failed (13.1.30). The log a developer needs most — without it every
-- question is a support ticket
CREATE TABLE IF NOT EXISTS control.webhook_delivery (
    id                                uuid PRIMARY KEY NOT NULL,
    subscription_id                   uuid NOT NULL,
    event_id                          uuid,
    event_type                        text NOT NULL,
    status                            text NOT NULL CONSTRAINT webhook_delivery_status_chk CHECK (status IN ('pending', 'delivered', 'failed', 'retrying', 'abandoned')),
    attempt_count                     integer,
    response_code                     integer,
    response_body_excerpt             text,
    is_replay                         boolean DEFAULT false,
    is_test                           boolean DEFAULT false,
    delivered_at                      timestamptz
);

-- An external subscriber to business events (13.1.26, 13.3.18). The 29 events existed and nothing
-- outside could receive one. Hangs off: reaches control.partner through its keys; references
-- control.api_client. Reached by: 3 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS control.webhook_subscription (
    id                                uuid PRIMARY KEY NOT NULL,
    client_id                         uuid NOT NULL,
    endpoint_url                      text NOT NULL,
    event_types                       text[] NOT NULL,
    filters                           jsonb,
    signing_secret                    text,
    status                            text NOT NULL CONSTRAINT webhook_subscription_status_chk CHECK (status IN ('pendingVerification', 'active', 'paused', 'failing', 'disabled')),
    consecutive_failures              integer,
    disabled_reason                   text
);

