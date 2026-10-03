-- whitelabel — 27 tables
-- **Derived. Do not hand-edit.**

-- An analytics platform a storefront or app reports to, per venue: which provider, its property or
-- container id and which consent category gates it. The banner's consent-mode signals are what
-- switch it on, so a provider with no category never loads
CREATE TABLE IF NOT EXISTS whitelabel.analytics_provider (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    provider                          text NOT NULL CONSTRAINT analytics_provider_provider_chk CHECK (provider IN ('googleAnalytics4', 'googleTagManager', 'adobeAnalytics', 'metaPixel', 'matomo', 'other')),
    provider_label                    text CONSTRAINT analytics_provider_provider_label_chk CHECK (char_length(provider_label) <= 100),
    measurement_id                    text NOT NULL CONSTRAINT analytics_provider_measurement_id_chk CHECK (char_length(measurement_id) <= 100),
    surfaces                          text[] NOT NULL,
    consent_category                  text NOT NULL DEFAULT 'analytics' CONSTRAINT analytics_provider_consent_category_chk CHECK (consent_category IN ('functional', 'analytics', 'personalisation', 'marketing')),
    is_enabled                        boolean NOT NULL DEFAULT true,
    reporting_property_id             text CONSTRAINT analytics_provider_reporting_property_id_chk CHECK (char_length(reporting_property_id) <= 100),
    reporting_credential_ref          text CONSTRAINT analytics_provider_reporting_credential_ref_chk CHECK (char_length(reporting_credential_ref) <= 200),
    has_reporting_credential          boolean,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.app_build (
    id                                uuid PRIMARY KEY NOT NULL,
    platform                          text NOT NULL CONSTRAINT app_build_platform_chk CHECK (platform IN ('ios', 'android')),
    config_version                    text NOT NULL,
    store_account_id                  uuid,
    version_name                      text,
    build_number                      integer,
    status                            text NOT NULL CONSTRAINT app_build_status_chk CHECK (status IN ('queued', 'building', 'built', 'failed', 'submitted', 'inReview', 'approved', 'rejected', 'released')),
    failure_reason                    text,
    package_asset_ref                 uuid,
    release_notes                     jsonb,
    submit_to_store                   boolean DEFAULT false,
    requested_at                      timestamptz NOT NULL,
    requested_by_principal_id         uuid,
    finished_at                       timestamptz,
    scope_path                        ltree NOT NULL
);

-- A notice on a tenant storefront, scheduled
CREATE TABLE IF NOT EXISTS whitelabel.banner (
    id                                uuid PRIMARY KEY NOT NULL,
    title                             jsonb NOT NULL,
    subtitle                          jsonb,
    image_asset_ref                   uuid NOT NULL,
    placement                         text CONSTRAINT banner_placement_chk CHECK (placement IN ('homepageHero', 'homepageBlock', 'explore', 'checkout')),
    link_target                       jsonb,
    starts_at                         timestamptz NOT NULL,
    ends_at                           timestamptz,
    state                             text,
    sort_order                        integer,
    is_active                         boolean,
    tenant_config_id                  uuid NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.booking_flow (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    flow_type_key                     text NOT NULL CONSTRAINT booking_flow_flow_type_key_chk CHECK (flow_type_key IN ('datedDayPass', 'timedEntry', 'openDated', 'seatedFixedPerformance', 'seatedDateTimeSeatMap', 'experienceWorkshop', 'surfSession', 'meetingRoomHourly', 'cabanaMap', 'cabanaBySize', 'guidedTourByLanguage', 'transport', 'tableReservation', 'membership', 'giftCard', 'multiLocation')),
    name                              text NOT NULL CONSTRAINT booking_flow_name_chk CHECK (char_length(name) <= 80),
    is_default_for_type               boolean DEFAULT false,
    is_enabled                        boolean DEFAULT true,
    settings                          jsonb,
    is_valid                          boolean,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.booking_flow_step (
    id                                uuid PRIMARY KEY NOT NULL,
    booking_flow_id                   uuid,
    step_key                          text NOT NULL CONSTRAINT booking_flow_step_step_key_chk CHECK (step_key IN ('location', 'helpMeChoose', 'product', 'date', 'time', 'performance', 'level', 'language', 'duration', 'route', 'partySize', 'resourceMap', 'resourceSize', 'seatMap', 'tickets', 'attendees', 'membershipPlan', 'giftCardValue', 'recipient', 'consent', 'extras', 'review', 'payment')),
    is_enabled                        boolean NOT NULL,
    sort_order                        integer NOT NULL,
    requirement                       text CONSTRAINT booking_flow_step_requirement_chk CHECK (requirement IN ('required', 'optional', 'conditional')),
    settings                          jsonb
);

-- One published version of a tenant’s configuration. Rolling back is selecting an earlier one
CREATE TABLE IF NOT EXISTS whitelabel.config_version (
    version                           text NOT NULL,
    published_at                      timestamptz NOT NULL,
    published_by_principal_id         uuid NOT NULL,
    published_by_name                 text,
    note                              text NOT NULL,
    review_status                     text DEFAULT 'notRequired' CONSTRAINT config_version_review_status_chk CHECK (review_status IN ('notRequired', 'pending', 'approved', 'rejected')),
    approval_request_id               uuid,
    is_current                        boolean NOT NULL,
    scheduled_for                     timestamptz,
    content_hash                      text,
    snapshot                          jsonb,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A page a tenant writes — about, directions, accessibility
CREATE TABLE IF NOT EXISTS whitelabel.content_page (
    id                                uuid PRIMARY KEY NOT NULL,
    slug                              text NOT NULL,
    title                             jsonb NOT NULL,
    body                              jsonb NOT NULL,
    is_enabled                        boolean DEFAULT true,
    status                            text NOT NULL,
    icon_asset_ref                    uuid,
    category_code                     text,
    sort_order                        integer,
    is_referenced                     boolean,
    scope_path                        ltree NOT NULL
);

-- A tenant's own hostname and its certificate (24 August). No domain or certificate operation
-- existed anywhere in 1,010 — and ADM-017 Domain & Certificate Management declared 41 operations,
-- none of them about a domain. Verification before issuance, always. Hangs off: reaches
-- whitelabel.footer_config through its keys; references platform.tenant. Reached by: 6 operations
-- read it and 3 write it.
CREATE TABLE IF NOT EXISTS whitelabel.custom_domain (
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid NOT NULL,
    hostname                          text NOT NULL,
    kind                              text CONSTRAINT custom_domain_kind_chk CHECK (kind IN ('guestWeb', 'guestApp', 'partnerPortal', 'developerPortal')),
    status                            text NOT NULL CONSTRAINT custom_domain_status_chk CHECK (status IN ('pending', 'verifying', 'verified', 'issuing', 'active', 'failed', 'expired', 'revoked')),
    verification_method               text CONSTRAINT custom_domain_verification_method_chk CHECK (verification_method IN ('dnsTxt', 'cname', 'httpFile')),
    verification_token                text,
    verification_record               jsonb,
    certificate_expires_at            timestamptz,
    last_checked_at                   timestamptz,
    failure_reason                    text,
    routing                           text DEFAULT 'cname' CONSTRAINT custom_domain_routing_chk CHECK (routing IN ('cname', 'delegatedSubdomain', 'apex')),
    dns_records                       jsonb,
    revalidation                      text DEFAULT 'none' CONSTRAINT custom_domain_revalidation_chk CHECK (revalidation IN ('none', 'pendingRevalidation', 'timedOut')),
    is_cname_lost                     boolean,
    is_primary                        boolean,
    readiness                         jsonb
);

-- A grouping of FAQ entries. Hangs off: reaches whitelabel.footer_config through its keys. Reached
-- by: 2 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS whitelabel.faq_category (
    code                              text NOT NULL,
    name                              jsonb NOT NULL,
    sort_order                        integer,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- One question and answer, localised
CREATE TABLE IF NOT EXISTS whitelabel.faq_entry (
    faq_category_id                   uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    question                          jsonb NOT NULL,
    answer                            jsonb NOT NULL,
    sort_order                        integer,
    is_published                      boolean
);

-- A switch a tenant may throw, distinct from a module they have licensed
CREATE TABLE IF NOT EXISTS whitelabel.feature_toggle (
    feature_key                       text NOT NULL,
    display_name                      text,
    is_enabled                        boolean NOT NULL,
    change_scope                      text NOT NULL,
    requires_configuration            boolean,
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_config_id                  uuid NOT NULL
);

-- Footer columns and legal links (BL-002). A header is chrome and a footer is a link surface —
-- legal links are held separately so a tenant cannot remove the privacy notice by accident
CREATE TABLE IF NOT EXISTS whitelabel.footer_config (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    legal_links                       jsonb,
    copyright_text                    text
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.footer_config_column (
    footer_config_id                  uuid NOT NULL,
    heading                           text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.footer_config_social_link (
    footer_config_id                  uuid NOT NULL,
    platform                          text,
    url                               text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.guided_choice (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    name                              text NOT NULL CONSTRAINT guided_choice_name_chk CHECK (char_length(name) <= 80),
    mode                              text NOT NULL DEFAULT 'button' CONSTRAINT guided_choice_mode_chk CHECK (mode IN ('button', 'popupOnArrival', 'off')),
    show_banner                       boolean DEFAULT true,
    behaviour                         text DEFAULT 'filter' CONSTRAINT guided_choice_behaviour_chk CHECK (behaviour IN ('filter', 'recommend')),
    show_everything                   boolean DEFAULT true,
    status                            text NOT NULL,
    source                            text NOT NULL CONSTRAINT guided_choice_source_chk CHECK (source IN ('manual', 'aiSuggested')),
    suggestion_ref                    text,
    published_at                      timestamptz,
    published_by                      uuid,
    updated_at                        timestamptz
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.guided_choice_answer (
    guided_choice_question_id         uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    title                             jsonb NOT NULL,
    body                              jsonb,
    icon                              text,
    badge                             jsonb,
    sort_order                        integer NOT NULL,
    target                            jsonb,
    filter                            jsonb,
    consent_prefill                   jsonb,
    result                            jsonb,
    guided_choice_id                  uuid NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.guided_choice_question (
    guided_choice_id                  uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    title                             jsonb NOT NULL,
    kind                              text,
    sort_order                        integer NOT NULL
);

-- A block on a tenant homepage, ordered. A section naming a disabled module must not render at all
CREATE TABLE IF NOT EXISTS whitelabel.homepage_section (
    template_key                      text,
    landing_source                    text DEFAULT 'storefront' CONSTRAINT homepage_section_landing_source_chk CHECK (landing_source IN ('storefront', 'ownSite')),
    id                                uuid PRIMARY KEY NOT NULL,
    content_page_id                   uuid,
    homepage_section_id               uuid NOT NULL
);

-- Which modules a tenant has on. The gate every requiresModule screen resolves against
CREATE TABLE IF NOT EXISTS whitelabel.module_enablement (
    module_key                        text NOT NULL CONSTRAINT module_enablement_module_key_chk CHECK (module_key IN ('ticketsAndBooking', 'membership', 'events', 'attractions', 'virtualQueue', 'diningAndFnb', 'shop', 'parking', 'gamification', 'photoGallery', 'wallet', 'loyalty', 'lostAndFound', 'map', 'visitPlanner')),
    display_name                      text,
    is_licensed                       boolean NOT NULL,
    is_enabled                        boolean NOT NULL,
    referenced_by                     text[],
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_config_id                  uuid NOT NULL
);

-- One entry in a tenant’s own navigation. Hangs off: reaches whitelabel.footer_config through its
-- keys. Reached by: 5 operations read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS whitelabel.navigation_item (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT navigation_item_kind_chk CHECK (kind IN ('bottomNavigation', 'drawer', 'tabs')),
    buy_button                        jsonb,
    navigation_item_id                uuid NOT NULL
);

-- A tenant’s own terms, privacy and cookie text, versioned because agreeing to one version is not
-- agreeing to the next
CREATE TABLE IF NOT EXISTS whitelabel.policy (
    kind                              text NOT NULL CONSTRAINT policy_kind_chk CHECK (kind IN ('privacy', 'termsAndConditions', 'refund', 'cookie', 'accessibility')),
    title                             text,
    version                           text NOT NULL,
    body                              jsonb NOT NULL,
    requires_reconsent                boolean,
    effective_from                    date NOT NULL,
    published_by_principal_id         uuid,
    published_at                      timestamptz NOT NULL,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A merchandising slot, targeted and scheduled
CREATE TABLE IF NOT EXISTS whitelabel.promo_block (
    id                                uuid PRIMARY KEY NOT NULL,
    title                             jsonb NOT NULL,
    description                       jsonb,
    icon_asset_ref                    uuid,
    promotion_id                      uuid,
    link_target                       jsonb,
    starts_at                         timestamptz,
    ends_at                           timestamptz,
    state                             text,
    sort_order                        integer,
    scope_path                        ltree NOT NULL
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.publish_review_policy (
    is_enabled                        boolean NOT NULL DEFAULT false,
    requires_reviewer_other_than_author boolean DEFAULT true,
    applies_to                        text[],
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.site_package (
    id                                uuid PRIMARY KEY NOT NULL,
    version                           text,
    status                            text NOT NULL CONSTRAINT site_package_status_chk CHECK (status IN ('building', 'ready', 'failed')),
    download_url                      text,
    expires_at                        timestamptz,
    requested_by_principal_id         uuid,
    platform_staff_grant_id           uuid,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.site_setup_progress (
    id                                uuid PRIMARY KEY NOT NULL,
    preset_key                        text CONSTRAINT site_setup_progress_preset_key_chk CHECK (preset_key IN ('themePark', 'waterPark', 'museum', 'theatreAndArena', 'singleAttraction', 'playCentre', 'multiVenue')),
    current_step                      text,
    steps                             jsonb,
    minimum_path_done                 boolean,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.store_account (
    id                                uuid PRIMARY KEY NOT NULL,
    store                             text NOT NULL CONSTRAINT store_account_store_chk CHECK (store IN ('appleAppStore', 'googlePlay')),
    account_holder_name               text NOT NULL CONSTRAINT store_account_account_holder_name_chk CHECK (char_length(account_holder_name) <= 200),
    duns_number                       text,
    developer_account_id              text NOT NULL CONSTRAINT store_account_developer_account_id_chk CHECK (char_length(developer_account_id) <= 64),
    app_identifier                    text NOT NULL CONSTRAINT store_account_app_identifier_chk CHECK (char_length(app_identifier) <= 155),
    api_credential_secret_ref         text,
    has_api_credential                boolean,
    listing                           jsonb,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Everything a tenant has branded or switched on. Versioned, published, and the reason a guest
-- storefront looks like the venue rather than like TICVAI
CREATE TABLE IF NOT EXISTS whitelabel.tenant_config (
    tenant_id                         uuid NOT NULL,
    version                           text NOT NULL,
    is_draft                          boolean,
    brand                             jsonb,
    app_icons                         jsonb,
    booking_flow                      jsonb,
    theme                             jsonb,
    fonts                             jsonb,
    footer_config_id                  uuid,
    notification_branding             jsonb,
    enabled_payment_methods           text[],
    accessibility                     jsonb,
    header                            jsonb,
    navigation_item_id                uuid,
    homepage_section_id               uuid,
    languages                         jsonb,
    updated_at                        timestamptz,
    is_in_maintenance                 boolean DEFAULT false,
    maintenance_message               jsonb,
    expected_back_at                  timestamptz,
    minimum_app_version               jsonb,
    contact                           jsonb,
    availability                      text,
    availability_message              jsonb,
    id                                uuid PRIMARY KEY NOT NULL
);

