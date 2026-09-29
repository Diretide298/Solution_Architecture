-- whitelabel — 19 tables
-- **Derived. Do not hand-edit.**

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

-- One published version of a tenant’s configuration. Rolling back is selecting an earlier one
CREATE TABLE IF NOT EXISTS whitelabel.config_version (
    version                           text NOT NULL,
    published_at                      timestamptz NOT NULL,
    published_by_principal_id         uuid NOT NULL,
    published_by_name                 text,
    note                              text NOT NULL,
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
-- whitelabel.footer_config through its keys; references platform.tenant. Reached by: 4 operations
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
    failure_reason                    text
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
-- saying what it is. Reached by: 7 operations read it and 2 write it; 2 tables reference it.
CREATE TABLE IF NOT EXISTS whitelabel.guided_choice (
    id                                text PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    name                              text NOT NULL CONSTRAINT guided_choice_name_chk CHECK (char_length(name) <= 80),
    mode                              text NOT NULL DEFAULT 'button' CONSTRAINT guided_choice_mode_chk CHECK (mode IN ('button', 'popupOnArrival', 'off')),
    show_banner                       boolean DEFAULT true,
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
    guided_choice_id                  text NOT NULL,
    id                                text PRIMARY KEY,
    title                             jsonb NOT NULL,
    sort_order                        integer NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS whitelabel.guided_choice_question (
    guided_choice_id                  text NOT NULL,
    id                                text PRIMARY KEY,
    title                             jsonb NOT NULL,
    sort_order                        integer NOT NULL
);

-- A block on a tenant homepage, ordered. A section naming a disabled module must not render at all
CREATE TABLE IF NOT EXISTS whitelabel.homepage_section (
    id                                uuid PRIMARY KEY,
    content_page_id                   uuid,
    homepage_section_id               uuid NOT NULL
);

-- Which modules a tenant has on. The gate every requiresModule screen resolves against
CREATE TABLE IF NOT EXISTS whitelabel.module_enablement (
    module_key                        text NOT NULL CONSTRAINT module_enablement_module_key_chk CHECK (module_key IN ('ticketsAndBooking', 'membership', 'events', 'attractions', 'virtualQueue', 'diningAndFnb', 'shop', 'parking', 'gamification', 'photoGallery', 'wallet', 'loyalty', 'lostAndFound', 'map')),
    display_name                      text,
    is_licensed                       boolean NOT NULL,
    is_enabled                        boolean NOT NULL,
    referenced_by                     text[],
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_config_id                  uuid NOT NULL
);

-- One entry in a tenant’s own navigation. Hangs off: reaches whitelabel.footer_config through its
-- keys. Reached by: 4 operations read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS whitelabel.navigation_item (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL CONSTRAINT navigation_item_kind_chk CHECK (kind IN ('bottomNavigation', 'drawer', 'tabs')),
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

