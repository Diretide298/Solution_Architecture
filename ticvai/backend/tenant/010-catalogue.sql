-- catalogue — 32 tables
-- **Derived. Do not hand-edit.**

-- Another way to name the same product — a barcode, a supplier code, a legacy id
CREATE TABLE IF NOT EXISTS catalogue.alternative_code (
    code                              text NOT NULL CONSTRAINT alternative_code_code_chk CHECK (char_length(code) <= 128),
    partner_id                        uuid NOT NULL,
    partner_name                      text,
    variant_id                        uuid,
    note                              text CONSTRAINT alternative_code_note_chk CHECK (char_length(note) <= 200),
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid
);

-- How much of a capacity each channel may sell. Web cannot consume the counter’s share
CREATE TABLE IF NOT EXISTS catalogue.channel_allocation (
    id                                uuid PRIMARY KEY,
    channel                           text NOT NULL CONSTRAINT channel_allocation_channel_chk CHECK (channel IN ('pos', 'kiosk', 'web', 'mobile', 'b2b', 'ota', 'callCentre')),
    allocated_units                   integer NOT NULL,
    sold_units                        integer,
    leased_units                      integer,
    remaining_units                   integer,
    release_at                        timestamptz,
    envelope_id                       uuid NOT NULL
);

-- How much of a performance each sales channel may sell. Two hundred seats with eighty to the web,
-- eighty to the box office and forty held back. Renamed from envelope, which was unguessable
CREATE TABLE IF NOT EXISTS catalogue.channel_capacity (
    id                                uuid PRIMARY KEY NOT NULL,
    performance_id                    uuid NOT NULL,
    name                              text,
    seat_category_id                  uuid,
    oversell_allowance                integer DEFAULT 0,
    oversell_basis                    text CONSTRAINT channel_capacity_oversell_basis_chk CHECK (oversell_basis IN ('fixedCount', 'historicNoShowRate', 'percentage')),
    capacity                          integer NOT NULL,
    sold                              integer NOT NULL,
    leased                            integer NOT NULL,
    remaining                         integer NOT NULL,
    has_channel_allocations           boolean,
    is_seated                         boolean NOT NULL
);

-- Fixed, free or round-up. Posts to a liability account, not revenue — money collected for a
-- charity is not the venue’s to recognise Hangs off: reaches catalogue.product through its keys;
-- references ledger.account, platform.scope. Reached by: 3 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS catalogue.donation_campaign (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL CONSTRAINT donation_campaign_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT donation_campaign_description_chk CHECK (char_length(description) <= 1000),
    beneficiary                       text,
    venue_ids                         text[],
    amount_mode                       text NOT NULL CONSTRAINT donation_campaign_amount_mode_chk CHECK (amount_mode IN ('fixedChoices', 'freeAmount', 'roundUp')),
    min_amount                        numeric(18,4),
    max_amount                        numeric(18,4),
    liability_account_id              uuid,
    channels                          text[],
    is_active                         boolean NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    raised_total                      numeric(18,4),
    venue_id                          uuid NOT NULL
);

-- The rules a ticket carries before anybody buys one — validity, entries allowed, transferability,
-- what a gate does with it. access.entitlement is the issued instance
CREATE TABLE IF NOT EXISTS catalogue.entitlement_template (
    description                       text,
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT entitlement_template_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT entitlement_template_name_chk CHECK (char_length(name) <= 200),
    validity_kind                     text NOT NULL CONSTRAINT entitlement_template_validity_kind_chk CHECK (validity_kind IN ('singleUse', 'dated', 'dateRange', 'rolling', 'unlimited', 'countLimited')),
    valid_from_offset_days            integer,
    valid_for_days                    integer,
    days_of_week                      text[],
    expiry_anchor                     text CONSTRAINT entitlement_template_expiry_anchor_chk CHECK (expiry_anchor IN ('offsetDays', 'endOfMonth', 'endOfQuarter', 'endOfYear', 'fixedDate', 'seasonEnd')),
    expiry_date                       date,
    carries_stored_value              boolean DEFAULT false,
    included_value                    numeric(18,4),
    blackout_dates                    text[],
    fast_track_tier                   text CONSTRAINT entitlement_template_fast_track_tier_chk CHECK (fast_track_tier IN ('none', 'priority', 'express', 'unlimited')),
    entries_allowed                   integer,
    is_reentry_allowed                boolean DEFAULT false,
    purchase_eligibility              jsonb,
    person_type                       text CONSTRAINT entitlement_template_person_type_chk CHECK (person_type IN ('adult', 'child', 'infant', 'senior', 'student', 'resident', 'staff')),
    admission_rules_id                uuid,
    is_transferable                   boolean DEFAULT true,
    can_share_media                   boolean DEFAULT true,
    can_claim_shop_and_drop           boolean DEFAULT false,
    is_name_bound                     boolean DEFAULT false,
    is_auto_renew_default             boolean DEFAULT false,
    renewal_term_days                 integer,
    renewal_grace_days                integer DEFAULT 0,
    renewal_variant_id                uuid,
    crosses_cells                     boolean DEFAULT false,
    is_active                         boolean,
    scope_path                        ltree NOT NULL
);

-- A named thing on at a venue, grouping performances. A concert is an event; each showing is a
-- performance
CREATE TABLE IF NOT EXISTS catalogue.event (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    parent_event_id                   uuid,
    performance_count                 integer,
    is_active                         boolean
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_capacity_profile (
    event_id                          uuid,
    performance_id                    uuid,
    mode                              text CONSTRAINT event_capacity_profile_mode_chk CHECK (mode IN ('reservedSeating', 'unreservedSeating', 'standing', 'mixed', 'capacityOnly')),
    safe_maximum                      integer,
    sellable                          integer,
    held                              integer DEFAULT 0,
    accessible_provision              integer DEFAULT 0,
    companion_seats                   integer DEFAULT 0,
    overbook_percent                  numeric(18,4) DEFAULT 0,
    seat_map_id                       uuid,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_registration (
    event_id                          uuid,
    is_required                       boolean DEFAULT false,
    form_id                           uuid,
    capture_per_attendee              boolean DEFAULT true,
    admission_policy                  jsonb,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_reschedule (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL CONSTRAINT event_reschedule_kind_chk CHECK (kind IN ('moveTime', 'moveDate', 'moveVenue', 'cancel', 'abandon')),
    performance_ids                   text[],
    new_starts_at                     timestamptz,
    new_space_id                      uuid,
    reason                            text NOT NULL,
    ticket_treatment                  text CONSTRAINT event_reschedule_ticket_treatment_chk CHECK (ticket_treatment IN ('moveAutomatically', 'offerChoice', 'refund', 'creditToWallet', 'honourAtAnyPerformance')),
    refund_fees                       boolean DEFAULT true,
    notify_guests                     boolean DEFAULT true,
    notification_template_id          uuid,
    affected_orders                   integer,
    affected_guests                   integer,
    approval_request_id               uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_resource_plan (
    event_id                          uuid,
    readiness                         text CONSTRAINT event_resource_plan_readiness_chk CHECK (readiness IN ('notPlanned', 'planning', 'atRisk', 'ready')),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_schedule (
    event_id                          uuid,
    duration_is_dynamic               boolean DEFAULT false,
    maximum_overrun_minutes           integer,
    cascade_overrun                   boolean DEFAULT true,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    has_performances                  boolean DEFAULT true,
    capacity_basis                    text CONSTRAINT event_type_capacity_basis_chk CHECK (capacity_basis IN ('perPerformance', 'perDay', 'perSession', 'unlimited')),
    ticket_names_date                 boolean DEFAULT true,
    multi_day                         boolean DEFAULT false,
    requires_registration             boolean DEFAULT false,
    requires_accreditation            boolean DEFAULT false,
    seating_modes_allowed             text[],
    default_lifecycle                 text[],
    scope_path                        ltree NOT NULL
);

-- What makes a product a school-trip format or a party package: participants, duration, hosts,
-- free leaders per pupils and how it is paid. The product row still carries the price
CREATE TABLE IF NOT EXISTS catalogue.group_package (
    id                                uuid PRIMARY KEY,
    product_id                        text,
    kind                              text NOT NULL CONSTRAINT group_package_kind_chk CHECK (kind IN ('school', 'party')),
    max_participants                  integer NOT NULL,
    duration_minutes                  integer NOT NULL,
    host_count                        integer DEFAULT 1,
    pricing_basis                     text CONSTRAINT group_package_pricing_basis_chk CHECK (pricing_basis IN ('perParticipant', 'perPackage')),
    free_leader_ratio                 integer DEFAULT 10,
    payment_mode                      text CONSTRAINT group_package_payment_mode_chk CHECK (payment_mode IN ('invoice', 'deposit', 'full')),
    includes                          text[],
    scope_path                        ltree NOT NULL
);

-- Two-phase catalogue import (BL-057), following seating.ImportJob. A job that parses zero
-- products is not a parsed job. Hangs off: reaches catalogue.product through its keys. Reached by:
-- 3 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS catalogue.import_job (
    id                                uuid PRIMARY KEY NOT NULL,
    status                            text NOT NULL CONSTRAINT import_job_status_chk CHECK (status IN ('parsing', 'previewReady', 'committing', 'committed', 'failed')),
    outcome                           text CONSTRAINT import_job_outcome_chk CHECK (outcome IN ('parsed', 'parsedWithFindings', 'nothingFound', 'unreadable')),
    parsed_count                      integer NOT NULL,
    create_count                      integer,
    update_count                      integer,
    scope_path                        ltree NOT NULL
);

-- A short-lived claim on contended stock while somebody decides. A seat in a basket is held, not
-- sold — CF-115 settled that contended inventory is leased rather than reserved, and the hold
-- expires on its own. Renamed from lease, which read as a rental agreement
CREATE TABLE IF NOT EXISTS catalogue.inventory_hold (
    id                                text PRIMARY KEY NOT NULL,
    channel_capacity_id               uuid NOT NULL,
    holder_workstation_id             uuid NOT NULL,
    parent_lease_id                   text,
    requested_units                   integer,
    channel                           text,
    granted_units                     integer NOT NULL,
    consumed_units                    integer NOT NULL,
    status                            text NOT NULL CONSTRAINT inventory_hold_status_chk CHECK (status IN ('active', 'expired', 'released', 'forceReleased')),
    acquired_at                       timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    released_at                       timestamptz,
    force_released_by_principal_id    uuid,
    force_release_reason              text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.membership_benefit (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL CONSTRAINT membership_benefit_code_chk CHECK (char_length(code) <= 100),
    name                              text NOT NULL CONSTRAINT membership_benefit_name_chk CHECK (char_length(name) <= 150),
    type                              text NOT NULL CONSTRAINT membership_benefit_type_chk CHECK (char_length(type) <= 30),
    description                       text CONSTRAINT membership_benefit_description_chk CHECK (char_length(description) <= 500),
    value                             numeric(18,4),
    unit                              text CONSTRAINT membership_benefit_unit_chk CHECK (char_length(unit) <= 30),
    entitlement_template_id           uuid,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.membership_programme (
    program_id                        uuid NOT NULL,
    program_code                      text NOT NULL CONSTRAINT membership_programme_program_code_chk CHECK (char_length(program_code) <= 100),
    program_name                      text NOT NULL CONSTRAINT membership_programme_program_name_chk CHECK (char_length(program_name) <= 150),
    description                       text CONSTRAINT membership_programme_description_chk CHECK (char_length(description) <= 500),
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- When a product happens — a session, a showing, a timed entry slot. Capacity lives here and in
-- catalogue.channel_capacity, never on the product
CREATE TABLE IF NOT EXISTS catalogue.performance (
    id                                uuid PRIMARY KEY NOT NULL,
    event_id                          uuid NOT NULL,
    starts_at                         timestamptz NOT NULL,
    ends_at                           timestamptz NOT NULL,
    approval_request_id               uuid,
    requires_approval_to_cancel       boolean DEFAULT true,
    status                            text NOT NULL CONSTRAINT performance_status_chk CHECK (status IN ('scheduled', 'onSale', 'soldOut', 'suspended', 'cancelled', 'completed')),
    admission_rules_id                uuid,
    seat_map_id                       uuid
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.plan_benefit (
    entitlement_template_id           uuid NOT NULL,
    membership_benefit_id             uuid NOT NULL,
    usage_limit                       numeric(18,4),
    usage_period                      text CONSTRAINT plan_benefit_usage_period_chk CHECK (char_length(usage_period) <= 30),
    priority                          integer NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.prepaid_minutes (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    minutes                           integer NOT NULL,
    list_price                        numeric(18,4),
    credit_type_id                    uuid,
    rounding_minutes                  integer DEFAULT 1,
    minimum_draw_minutes              integer DEFAULT 0,
    band_multipliers_apply            boolean DEFAULT true,
    validity_months                   integer,
    transferable_within_household     boolean DEFAULT false,
    applicable_space_ids              text[],
    scope_path                        ltree NOT NULL
);

-- What something costs on one price list. A change here never rewrites what somebody already paid
CREATE TABLE IF NOT EXISTS catalogue.price (
    id                                uuid PRIMARY KEY,
    price_list_id                     uuid NOT NULL,
    variant_id                        uuid NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    tax_code_id                       uuid
);

-- A named set of prices for a region and channel. Region-scoped, because currency is (ADR-0018)
CREATE TABLE IF NOT EXISTS catalogue.price_list (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    channels                          text[] NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    priority                          integer
);

-- What a venue sells — admission, a session, a bundle, a membership, a locker. Not the instance: a
-- product is the offer and catalogue.performance is the occasion
CREATE TABLE IF NOT EXISTS catalogue.product (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT product_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT product_name_chk CHECK (char_length(name) <= 200),
    description                       text,
    kind                              text NOT NULL CONSTRAINT product_kind_chk CHECK (kind IN ('admission', 'timedAdmission', 'datedAdmission', 'openDated', 'seated', 'membership', 'bundle', 'fnb', 'retail', 'rental', 'addOn', 'giftCard')),
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    created_by_principal_id           uuid,
    approved_by_principal_id          uuid,
    responsible_department_id         uuid,
    on_sale_from                      timestamptz,
    on_sale_to                        timestamptz,
    category_id                       uuid,
    lifecycle_state                   text CONSTRAINT product_lifecycle_state_chk CHECK (lifecycle_state IN ('draft', 'inReview', 'approved', 'live', 'withdrawn', 'archived')),
    is_sellable                       boolean NOT NULL,
    is_stock_tracked                  boolean DEFAULT false,
    has_variants                      boolean NOT NULL,
    variant_count                     integer,
    segment_tags                      text[],
    code_schema                       text,
    channels                          text[],
    entitlement_template_id           uuid,
    blocked_offline                   boolean,
    data_mask_values                  jsonb
);

-- The merchandise hierarchy — categories, brands, collections (Retail Board 2, 20 August).
-- listSeatCategories existed and a product category did not. One tree rather than four tables,
-- because a brand under a department under a category is how a real hierarchy runs
CREATE TABLE IF NOT EXISTS catalogue.product_category (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    code                              text CONSTRAINT product_category_code_chk CHECK (char_length(code) <= 64),
    name_localised                    jsonb,
    kind                              text NOT NULL CONSTRAINT product_category_kind_chk CHECK (kind IN ('category', 'brand', 'collection', 'season', 'department')),
    parent_id                         uuid,
    scope_path                        ltree NOT NULL,
    display_order                     integer DEFAULT 100,
    image_asset_id                    uuid,
    is_active                         boolean DEFAULT true
);

-- Who may take part in a product: age, height, supervision, swim ability. Declared by the guest at
-- booking, checked by staff at the gate; whether a guest who fails there is refunded is a column,
-- because the design says they are not
CREATE TABLE IF NOT EXISTS catalogue.product_eligibility_rule (
    id                                uuid PRIMARY KEY,
    product_id                        text,
    min_age_years                     integer,
    max_age_years                     integer,
    min_height_cm                     integer,
    max_height_cm                     integer,
    height_bands_cm                   text[],
    accompanied_below_age             integer,
    guardian_signature_age_from       integer,
    guardian_signature_age_to         integer,
    is_waiver_required                boolean DEFAULT false,
    swim_ability                      text DEFAULT 'notRequired' CONSTRAINT product_eligibility_rule_swim_ability_chk CHECK (swim_ability IN ('notRequired', 'confident')),
    refundable_if_ineligible_at_gate  boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- Version history for a product (BL-030, BL-047, BL-058). A restore creates a new version rather
-- than rewinding, so a price that was wrong for three days stays reproducible
CREATE TABLE IF NOT EXISTS catalogue.product_version (
    version                           integer NOT NULL,
    product_id                        uuid,
    published_at                      timestamptz NOT NULL,
    published_by_principal_id         uuid NOT NULL,
    note                              text,
    is_current                        boolean,
    content_hash                      text,
    restored_from_version             integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A catalogue snapshot a till can trade from offline (ADR-0013). Published, versioned, and the
-- reason a counter works with no network
CREATE TABLE IF NOT EXISTS catalogue.published_bundle (
    version                           text NOT NULL,
    venue_id                          uuid NOT NULL,
    is_delta                          boolean NOT NULL,
    base_version                      text,
    signature                         text NOT NULL,
    signature_key_id                  text NOT NULL,
    content_hash                      text NOT NULL,
    stale_after                       timestamptz NOT NULL,
    payload                           jsonb NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.session_template (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    space_id                          uuid,
    slot_minutes                      integer,
    turnaround_minutes                integer DEFAULT 0,
    concurrent_capacity               integer,
    walk_in                           jsonb,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.space (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid,
    venue_map_zone_id                 uuid,
    resource_id                       uuid,
    parent_space_id                   uuid,
    maximum_capacity                  integer,
    safe_capacity                     integer,
    setup_minutes                     integer DEFAULT 0,
    teardown_minutes                  integer DEFAULT 0,
    access_rules                      jsonb,
    is_bookable                       boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- One sellable configuration of a product — a size, a colour, a tier. Varies along the dimensions
-- in catalogue.variant_dimension
CREATE TABLE IF NOT EXISTS catalogue.variant (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    sku                               text NOT NULL,
    axis_values                       jsonb NOT NULL,
    name                              text CONSTRAINT variant_name_chk CHECK (char_length(name) <= 150),
    barcode                           text CONSTRAINT variant_barcode_chk CHECK (char_length(barcode) <= 64),
    is_default                        boolean DEFAULT false,
    is_active                         boolean NOT NULL
);

-- The axis a product varies along — size, colour, session length. A t-shirt has one; a timed
-- ticket has none. Renamed from variant_dimension
CREATE TABLE IF NOT EXISTS catalogue.variant_dimension (
    code                              text NOT NULL CONSTRAINT variant_dimension_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT variant_dimension_name_chk CHECK (char_length(name) <= 200),
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL
);

-- Who asked to be told when a sold-out session frees up. Not a queue — a queue is people standing
-- at a ride Hangs off: reaches catalogue.product through its keys; references
-- catalogue.performance, catalogue.variant, pii.subject. Reached by: 4 operations read it and 3
-- write it.
CREATE TABLE IF NOT EXISTS catalogue.waitlist_entry (
    id                                uuid PRIMARY KEY,
    performance_id                    uuid NOT NULL,
    variant_id                        uuid,
    subject_id                        uuid,
    contact_point                     text,
    party_size                        integer NOT NULL,
    status                            text,
    position                          integer,
    offered_at                        timestamptz,
    offer_expires_at                  timestamptz,
    joined_at                         timestamptz
);

