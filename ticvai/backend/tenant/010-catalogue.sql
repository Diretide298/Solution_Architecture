-- catalogue — 30 tables
-- **Derived. Do not hand-edit.**

-- Another way to name the same product — a barcode, a supplier code, a legacy id
CREATE TABLE IF NOT EXISTS catalogue.alternative_code (
    code                              text NOT NULL,
    partner_id                        uuid NOT NULL,
    partner_name                      text,
    variant_id                        uuid,
    note                              text,
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid
);

-- How much of a capacity each channel may sell. Web cannot consume the counter’s share
CREATE TABLE IF NOT EXISTS catalogue.channel_allocation (
    id                                uuid PRIMARY KEY,
    channel                           text NOT NULL,
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
    oversell_allowance                integer,
    oversell_basis                    text,
    capacity                          integer NOT NULL,
    sold                              integer NOT NULL,
    leased                            integer NOT NULL,
    remaining                         integer NOT NULL,
    has_channel_allocations           boolean,
    is_seated                         boolean NOT NULL
);

-- Fixed, free or round-up. Posts to a liability account, not revenue — money collected for a
-- charity is not the venue’s to recognise Hangs off: reaches catalogue.event through its keys;
-- references ledger.account, platform.scope. Reached by: 3 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS catalogue.donation_campaign (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL,
    description                       text,
    beneficiary                       text,
    venue_ids                         text[],
    amount_mode                       text NOT NULL,
    min_amount                        numeric(18,4),
    max_amount                        numeric(18,4),
    liability_account_id              uuid,
    is_active                         boolean NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    raised_total                      numeric(18,4),
    venue_id                          uuid NOT NULL
);

-- The rules a ticket carries before anybody buys one — validity, entries allowed, transferability,
-- what a gate does with it. access.entitlement is the issued instance
CREATE TABLE IF NOT EXISTS catalogue.entitlement_template (
    entitlement_id                    text NOT NULL,
    product_name                      text,
    status                            text NOT NULL,
    entries_used                      integer,
    last_used_at                      timestamptz,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    transferred_to_subject_id         uuid,
    description                       text,
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    validity_kind                     text NOT NULL,
    valid_from_offset_days            integer,
    valid_for_days                    integer,
    days_of_week                      text[],
    expiry_anchor                     text,
    expiry_date                       date,
    carries_stored_value              boolean,
    included_value                    numeric(18,4),
    blackout_dates                    text[],
    fast_track_tier                   text,
    entries_allowed                   integer,
    reentry_allowed                   boolean,
    purchase_eligibility              jsonb,
    person_type                       text,
    admission_rules_id                uuid,
    is_transferable                   boolean,
    can_share_media                   boolean,
    can_claim_shop_and_drop           boolean,
    is_name_bound                     boolean,
    auto_renew_default                boolean,
    renewal_term_days                 integer,
    renewal_grace_days                integer,
    renewal_variant_id                uuid,
    crosses_cells                     boolean,
    is_active                         boolean,
    scope_path                        text,
    admission_profile_id              uuid NOT NULL
);

-- A named thing on at a venue, grouping performances. A concert is an event; each showing is a
-- performance
CREATE TABLE IF NOT EXISTS catalogue.event (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        text NOT NULL,
    parent_event_id                   uuid,
    performance_count                 integer,
    is_active                         boolean
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_capacity_profile (
    event_id                          uuid,
    performance_id                    uuid,
    mode                              text,
    safe_maximum                      integer,
    sellable                          integer,
    held                              integer,
    accessible_provision              integer,
    companion_seats                   integer,
    overbook_percent                  numeric(18,4),
    seat_map_id                       uuid,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_registration (
    event_id                          uuid,
    required                          boolean,
    form_id                           uuid,
    capture_per_attendee              boolean,
    admission_policy                  jsonb,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_reschedule (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL,
    performance_ids                   text[],
    new_starts_at                     timestamptz,
    new_space_id                      uuid,
    reason                            text NOT NULL,
    ticket_treatment                  text,
    refund_fees                       boolean,
    notify_guests                     boolean,
    notification_template_id          uuid,
    affected_orders                   integer,
    affected_guests                   integer,
    approval_request_id               uuid,
    scope_path                        text
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_resource_plan (
    event_id                          uuid,
    readiness                         text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_schedule (
    event_id                          uuid,
    duration_is_dynamic               boolean,
    maximum_overrun_minutes           integer,
    cascade_overrun                   boolean,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.event_type (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    has_performances                  boolean,
    capacity_basis                    text,
    ticket_names_date                 boolean,
    multi_day                         boolean,
    requires_registration             boolean,
    requires_accreditation            boolean,
    seating_modes_allowed             text[],
    default_lifecycle                 text[],
    scope_path                        text
);

-- Two-phase catalogue import (BL-057), following seating.ImportJob. A job that parses zero
-- products is not a parsed job. Hangs off: reaches catalogue.event through its keys. Reached by: 2
-- operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS catalogue.import_job (
    id                                uuid PRIMARY KEY NOT NULL,
    status                            text NOT NULL,
    outcome                           text,
    parsed_count                      integer NOT NULL,
    create_count                      integer,
    update_count                      integer,
    scope_path                        text
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
    status                            text NOT NULL,
    acquired_at                       timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    released_at                       timestamptz,
    force_released_by_principal_id    uuid,
    force_release_reason              text,
    envelope_id                       uuid NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.membership_benefit (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    type                              text NOT NULL,
    description                       text,
    value                             numeric(18,4),
    unit                              text,
    entitlement_template_id           uuid,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.membership_programme (
    program_id                        uuid NOT NULL,
    program_code                      text NOT NULL,
    program_name                      text NOT NULL,
    description                       text,
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
    requires_approval_to_cancel       boolean,
    status                            text NOT NULL,
    admission_rules_id                uuid,
    seat_map_id                       uuid,
    admission_profile_id              uuid NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS catalogue.plan_benefit (
    entitlement_template_id           uuid NOT NULL,
    membership_benefit_id             uuid NOT NULL,
    usage_limit                       numeric(18,4),
    usage_period                      text,
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
    price                             numeric(18,4),
    credit_type_id                    uuid,
    rounding_minutes                  integer,
    minimum_draw_minutes              integer,
    band_multipliers_apply            boolean,
    validity_months                   integer,
    transferable_within_household     boolean,
    applicable_space_ids              text[],
    scope_path                        text
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
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    priority                          integer
);

-- What a venue sells — admission, a session, a bundle, a membership, a locker. Not the instance: a
-- product is the offer and catalogue.performance is the occasion
CREATE TABLE IF NOT EXISTS catalogue.product (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    kind                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        text NOT NULL,
    created_by_principal_id           uuid,
    approved_by_principal_id          uuid,
    responsible_department_id         uuid,
    on_sale_from                      timestamptz,
    on_sale_to                        timestamptz,
    category_id                       uuid,
    lifecycle_state                   text,
    is_sellable                       boolean NOT NULL,
    is_stock_tracked                  boolean,
    has_variants                      boolean NOT NULL,
    variant_count                     integer,
    segment_tags                      text[],
    code_schema                       text,
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
    code                              text,
    name_localised                    jsonb,
    kind                              text NOT NULL,
    parent_id                         uuid,
    scope_path                        text,
    display_order                     integer,
    image_asset_id                    uuid,
    is_active                         boolean
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
    turnaround_minutes                integer,
    concurrent_capacity               integer,
    walk_in                           jsonb,
    scope_path                        text
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
    setup_minutes                     integer,
    teardown_minutes                  integer,
    access_rules                      jsonb,
    bookable                          boolean,
    scope_path                        text
);

-- One sellable configuration of a product — a size, a colour, a tier. Varies along the dimensions
-- in catalogue.variant_dimension
CREATE TABLE IF NOT EXISTS catalogue.variant (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    sku                               text NOT NULL,
    axis_values                       jsonb NOT NULL,
    name                              text,
    barcode                           text,
    is_default                        boolean,
    is_active                         boolean NOT NULL
);

-- The axis a product varies along — size, colour, session length. A t-shirt has one; a timed
-- ticket has none. Renamed from variant_dimension
CREATE TABLE IF NOT EXISTS catalogue.variant_dimension (
    code                              text NOT NULL,
    name                              text NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL
);

-- Who asked to be told when a sold-out session frees up. Not a queue — a queue is people standing
-- at a ride Hangs off: reaches catalogue.event through its keys; references catalogue.performance,
-- catalogue.variant, pii.subject. Reached by: 4 operations read it and 3 write it.
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

