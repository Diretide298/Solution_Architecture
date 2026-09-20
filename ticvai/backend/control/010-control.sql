-- control — 49 tables
-- **Derived. Do not hand-edit.**

-- The one credential model (CF-135a). 2.7.52, 7.1.25 and 7.1.30 each asserted their own. Bound to
-- one environment, because a key that works in both is a key somebody will use in the wrong one
CREATE TABLE IF NOT EXISTS control.api_client (
    id                                uuid PRIMARY KEY NOT NULL,
    developer_id                      uuid NOT NULL,
    name                              text NOT NULL,
    client_id                         text,
    environment                       text NOT NULL,
    scopes                            text[] NOT NULL,
    allowed_tenant_ids                text[],
    ip_allow_list                     text[],
    status                            text NOT NULL,
    last_used_at                      timestamptz
);

-- Which API modules a tenant licensed (13.3.24, D5). Configuration, not code — rates change
-- without a release
CREATE TABLE IF NOT EXISTS control.api_licence (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid NOT NULL,
    licensed_modules                  text[] NOT NULL,
    call_allowance_per_month          integer,
    overage_rate_per_thousand         numeric(18,4),
    revenue_share_percent             numeric(18,4),
    effective_from                    date,
    effective_to                      date
);

-- Rate limits per client (13.1.36). A quota protects the venue, not the developer. Hangs off:
-- reaches control.cell through its keys; references control.api_client. Reached by: 1 operations
-- read it and 1 write it.
CREATE TABLE IF NOT EXISTS control.api_limit (
    id                                uuid PRIMARY KEY,
    client_id                         uuid NOT NULL,
    sustained_per_minute              integer NOT NULL,
    burst_per_second                  integer,
    daily_cap                         integer,
    per_operation_overrides           jsonb,
    on_breach                         text
);

-- API versions and sunset dates (13.1.31–35, ADR-0031). With third parties a breaking change with
-- no window breaks somebody else business. Hangs off: reaches control.cell through its keys.
-- Reached by: 3 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS control.api_version (
    version                           text NOT NULL,
    status                            text NOT NULL,
    released_at                       timestamptz,
    deprecated_at                     timestamptz,
    sunset_at                         timestamptz,
    minimum_notice_months             integer,
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
    state                             text,
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
    scope                             text,
    started_at                        timestamptz,
    completed_at                      timestamptz,
    state                             text,
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
    status                            text NOT NULL,
    performance_id                    uuid NOT NULL,
    cell_name                         text NOT NULL,
    snapshot_taken_at                 timestamptz,
    price_divergence_policy           text,
    sequence_high                     integer,
    orders_taken                      integer,
    orders_reconciled                 integer,
    orders_rejected                   integer,
    provisioned_at                    timestamptz,
    live_at                           timestamptz,
    drained_at                        timestamptz,
    reconciled_at                     timestamptz,
    decommissioned_at                 timestamptz,
    auto_decommission                 boolean,
    grace_minutes                     integer,
    teardown_confirmed_at             timestamptz,
    usage_record_id                   uuid
);

-- A deployment and a legal boundary at once (ADR-0001). One per jurisdiction, carrying its cloud
-- provider, region and endpoint. Only CrossRegionService reaches another one, and it moves a
-- pseudonymous link rather than a guest
CREATE TABLE IF NOT EXISTS control.cell (
    id                                uuid PRIMARY KEY,
    name                              text,
    kind                              text,
    cluster_id                        uuid,
    is_reachable                      boolean,
    last_contact_at                   timestamptz,
    licence_expires_at                timestamptz,
    participates_in_cross_cell        boolean,
    region_id                         uuid,
    region_name                       text,
    country_code                      text,
    tier                              text,
    status                            text,
    cloud_provider                    text,
    cloud_region                      text,
    api_endpoint                      text,
    venue_count                       integer,
    provisioned_at                    timestamptz,
    deployment_ref                    text,
    health                            jsonb
);

-- identical cells serving a region. Scaling out is launching another, not growing one Hangs off: a
-- child of control.cell; reaches control.cell through its keys; references control.cell,
-- platform.scope. Reached by: 2 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS control.cell_cluster (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text,
    region_id                         uuid NOT NULL,
    kind                              text NOT NULL,
    cell_ids                          text[] NOT NULL,
    schema_version                    text,
    modelled_on_cell_id               uuid,
    status                            text NOT NULL,
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
    status                            text NOT NULL,
    role                              text,
    supports_synchronous_replication  boolean,
    max_connections                   integer,
    created_at                        timestamptz,
    retired_at                        timestamptz
);

-- Work running against a cell — provisioning, migration, decommission
CREATE TABLE IF NOT EXISTS control.cell_job (
    id                                uuid PRIMARY KEY NOT NULL,
    cell_id                           uuid NOT NULL,
    kind                              text NOT NULL,
    status                            text NOT NULL,
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
    pinned_instance                   boolean,
    database_name                     text NOT NULL,
    status                            text NOT NULL,
    provisioned_at                    timestamptz,
    dropped_at                        timestamptz
);

-- What is published to an OTA (BL-076). An OTA pulls a feed, caches it and sells against the cache
-- — so the gap between pushes is the oversell window, and the allocation bounds it
CREATE TABLE IF NOT EXISTS control.channel_listing (
    id                                uuid PRIMARY KEY NOT NULL,
    channel_name                      text NOT NULL,
    product_id                        uuid NOT NULL,
    external_product_ref              text,
    status                            text NOT NULL,
    allocation_units                  integer,
    price_list_id                     uuid,
    adapter                           text,
    adapter_credential_ref            text,
    push_interval_minutes             integer,
    guest_data_scope                  text,
    last_pushed_at                    timestamptz,
    scope_path                        text
);

-- Authored content with a schedule (BL-172). The CMS modelled configuration and not authoring — a
-- marketer could choose between things a developer had built and could not write something new
CREATE TABLE IF NOT EXISTS control.content_block (
    id                                uuid PRIMARY KEY NOT NULL,
    page_id                           uuid,
    kind                              text NOT NULL,
    position                          integer,
    body                              jsonb,
    locale_variants                   jsonb,
    status                            text NOT NULL,
    publish_at                        timestamptz,
    expire_at                         timestamptz,
    audience_segment_id               uuid,
    approved_by_principal_id          uuid,
    scope_path                        text
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
    status                            text NOT NULL,
    verified_at                       timestamptz
);

-- Dev, staging, production — and which cells are in each. Promotion may require approval and a
-- soak period
CREATE TABLE IF NOT EXISTS control.environment (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL,
    name                              text NOT NULL,
    cell_ids                          text[],
    requires_approval_to_promote      boolean,
    soak_hours                        integer,
    current_release_version           text,
    is_active                         boolean,
    cell_id                           uuid NOT NULL
);

-- Footer columns and legal links (BL-002). A header is chrome and a footer is a link surface —
-- legal links are held separately so a tenant cannot remove the privacy notice by accident
CREATE TABLE IF NOT EXISTS control.footer_config (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        text NOT NULL,
    legal_links                       jsonb,
    copyright_text                    text
);

-- A published third-party integration (13.1.50). A listing, not an installation — the code runs on
-- the developer own infrastructure
CREATE TABLE IF NOT EXISTS control.integration_listing (
    id                                uuid PRIMARY KEY NOT NULL,
    developer_id                      uuid NOT NULL,
    name                              text NOT NULL,
    category                          text NOT NULL,
    description                       text,
    integration_url                   text,
    required_scopes                   text[],
    status                            text NOT NULL,
    certified_until                   date,
    certified_against_version         text,
    listing_fee_model                 text
);

-- A bill to a tenant. Lines are children
CREATE TABLE IF NOT EXISTS control.invoice (
    id                                uuid PRIMARY KEY NOT NULL,
    invoice_number                    text NOT NULL,
    tenant_id                         uuid NOT NULL,
    period_start                      date NOT NULL,
    period_end                        date NOT NULL,
    status                            text NOT NULL,
    subtotal                          numeric(18,4),
    tax_amount                        numeric(18,4),
    total                             numeric(18,4) NOT NULL,
    plan_version_used                 text,
    issued_at                         timestamptz,
    due_at                            date,
    paid_at                           timestamptz
);

-- One charge on a tenant invoice, traced to the usage that produced it
CREATE TABLE IF NOT EXISTS control.invoice_line (
    invoice_id                        uuid NOT NULL,
    description                       text,
    kind                              text,
    metric                            text,
    quantity                          numeric(18,4),
    unit_price                        numeric(18,4),
    amount                            numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Something bought beyond the plan. Hangs off: reaches control.cell through its keys; references
-- subscription.plan. Reached by: 4 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS control.licence_add_on (
    module_key                        text NOT NULL,
    price                             numeric(18,4),
    valid_from                        date,
    valid_to                          date,
    note                              text,
    id                                uuid PRIMARY KEY NOT NULL,
    plan_id                           uuid NOT NULL
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
    all_reversible                    boolean NOT NULL,
    irreversible                      text[],
    total_estimated_lock_ms           integer,
    scope_path                        text
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
    status                            text NOT NULL,
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
    status                            text NOT NULL,
    trial_ends_at                     timestamptz,
    rejection_reason                  text,
    provisioned_tenant_id             uuid
);

-- Net rate or commission, credit terms, validity. Versioned — an order placed last week used last
-- week’s rate Hangs off: reaches control.cell through its keys; references approvals.request,
-- assets.media_asset, identity.principal. Reached by: 8 operations read it and 3 write it; 1
-- tables reference it.
CREATE TABLE IF NOT EXISTS control.partner_agreement (
    id                                uuid PRIMARY KEY,
    partner_id                        uuid NOT NULL,
    partner_name                      text,
    version                           integer,
    status                            text,
    rate_mode                         text NOT NULL,
    commission_percent                numeric(18,4),
    volume_window                     text,
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
    fx_policy                         text,
    fixed_rate                        numeric(18,4),
    credit_limit                      numeric(18,4),
    allowed_venue_ids                 text[],
    requires_approval_above_value     numeric(18,4),
    valid_from                        date NOT NULL,
    valid_to                          date,
    expiry_alert_days                 integer,
    approval_request_id               text,
    notes                             text
);

-- A principal on a partner branch (2.7.51, BL-075). A partner was a flat account. Quota and credit
-- resolve nearest-ancestor-wins, like configuration
CREATE TABLE IF NOT EXISTS control.partner_user (
    id                                uuid PRIMARY KEY NOT NULL,
    partner_id                        uuid NOT NULL,
    principal_id                      uuid NOT NULL,
    branch_scope_path                 text NOT NULL,
    allocation_quota                  integer,
    credit_limit_override             numeric(18,4),
    can_manage_users                  boolean
);

-- a shipped version. Promoted through dev, staging and production; superseded by a later one Hangs
-- off: reaches control.cell through its keys; references identity.principal, subscription.plan.
-- Reached by: 5 operations read it and 3 write it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS control.release (
    version                           text,
    required_migrations               text[],
    note                              text,
    breaking_changes                  text[],
    id                                uuid PRIMARY KEY,
    status                            text,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
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
    reinventory_hold_id               uuid NOT NULL,
    environment                       text NOT NULL,
    status                            text NOT NULL,
    cells_total                       integer,
    cells_complete                    integer,
    cells_failed                      integer,
    started_by_principal_id           uuid,
    approved_by_principal_id          uuid,
    paused_reason                     text,
    started_at                        timestamptz NOT NULL,
    completed_at                      timestamptz,
    release_id                        uuid NOT NULL
);

-- One cell in a rollout — its wave, whether it is the canary, and what version it moved between
CREATE TABLE IF NOT EXISTS control.rollout_cell (
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
    status                            text NOT NULL,
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
    status                            text NOT NULL,
    data_profile                      jsonb NOT NULL,
    contains_production_data          boolean,
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
-- search sells through OTAs at OTA commission. Hangs off: reaches control.cell through its keys;
-- references ledger.legal_entity. Reached by: 1 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS control.seo_metadata (
    id                                uuid PRIMARY KEY NOT NULL,
    entity_kind                       text NOT NULL,
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
    is_auto_generated                 boolean,
    no_index                          boolean,
    scope_path                        text
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
    scope_path                        text
);

-- A customer of the platform — the root of the org tree. platform.tenant is a one-column
-- projection of this, so a cell can resolve its own tenant without reaching across a residency
-- boundary
CREATE TABLE IF NOT EXISTS control.tenant (
    id                                uuid PRIMARY KEY,
    code                              text,
    name                              text,
    status                            text,
    suspension_mode                   text,
    suspension_reason                 text,
    plan_id                           uuid,
    plan_name                         text,
    cell_count                        integer,
    venue_count                       integer,
    billing_email                     text,
    account_manager_principal_id      uuid,
    created_at                        timestamptz,
    activated_at                      timestamptz,
    subscription                      uuid,
    licences                          jsonb
);

-- a tenant moving between cells — shared to dedicated, or rebalancing Hangs off: a child of
-- control.tenant; reaches control.cell through its keys; references control.cell, control.tenant,
-- control.tenant_migration_plan. Reached by: 3 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS control.tenant_migration (
    id                                uuid PRIMARY KEY NOT NULL,
    plan_id                           uuid NOT NULL,
    tenant_id                         uuid NOT NULL,
    from_cell_id                      uuid,
    to_cell_id                        uuid,
    reason                            text,
    status                            text NOT NULL,
    rows_copied                       integer,
    rows_expected                     integer,
    verification_passed               boolean,
    cutover_at                        timestamptz,
    source_retained_until             timestamptz,
    started_at                        timestamptz NOT NULL,
    completed_at                      timestamptz,
    error                             text
);

-- computed against cell state; expires, because a plan made for a different world is not a plan
-- Hangs off: a child of control.tenant; reaches control.cell through its keys; references
-- control.cell, control.tenant. Reached by: 1 operations read it and 1 write it; 1 tables
-- reference it.
CREATE TABLE IF NOT EXISTS control.tenant_migration_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid NOT NULL,
    from_cell_id                      uuid NOT NULL,
    to_cell_id                        uuid NOT NULL,
    from_kind                         text,
    to_kind                           text,
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
    reason                            text,
    created_at                        timestamptz,
    hit_count                         integer,
    is_active                         boolean,
    scope_path                        text
);

-- What a tenant consumed, which is what an invoice is computed from
CREATE TABLE IF NOT EXISTS control.usage_record (
    id                                text PRIMARY KEY NOT NULL,
    metric                            text NOT NULL,
    quantity                          numeric(18,4) NOT NULL,
    venue_id                          uuid,
    capability                        text,
    recorded_at                       timestamptz NOT NULL
);

-- What a venue of this kind starts with (BL-165). A water park and a theatre need different
-- defaults, and configuring 300 settings from empty is asking a prospect to leave
CREATE TABLE IF NOT EXISTS control.venue_type_template (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    venue_kind                        text NOT NULL,
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
    action                            text,
    match_on                          text,
    pattern                           text,
    enabled                           boolean,
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
    status                            text NOT NULL,
    attempt_count                     integer,
    response_code                     integer,
    response_body_excerpt             text,
    is_replay                         boolean,
    delivered_at                      timestamptz
);

-- An external subscriber to business events (13.1.26, 13.3.18). The 29 events existed and nothing
-- outside could receive one. Hangs off: reaches control.cell through its keys; references
-- control.api_client. Reached by: 3 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS control.webhook_subscription (
    id                                uuid PRIMARY KEY NOT NULL,
    client_id                         uuid NOT NULL,
    endpoint_url                      text NOT NULL,
    event_types                       text[] NOT NULL,
    filters                           jsonb,
    signing_secret                    text,
    status                            text NOT NULL,
    consecutive_failures              integer,
    disabled_reason                   text
);

