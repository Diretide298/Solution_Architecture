-- assets — 13 tables
-- **Derived. Do not hand-edit.**

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.approval (
    asset_id                          uuid,
    state                             text CONSTRAINT approval_state_chk CHECK (state IN ('draft', 'pendingApproval', 'approved', 'rejected', 'published', 'archived')),
    approved_by                       uuid,
    comment                           text,
    at                                timestamptz,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.asset_version (
    asset_id                          uuid,
    version                           integer,
    file_name                         text,
    size_bytes                        integer,
    checksum                          text,
    created_by                        uuid,
    created_at                        timestamptz,
    note                              text,
    is_current                        boolean,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.audit (
    id                                uuid PRIMARY KEY,
    asset_id                          uuid,
    at                                timestamptz,
    action                            text CONSTRAINT audit_action_chk CHECK (action IN ('uploaded', 'updated', 'retagged', 'versioned', 'approved', 'published', 'shared', 'downloaded', 'delivered', 'archived', 'deleted')),
    actor_id                          uuid,
    recipient                         text,
    detail                            text,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.distribution_channel (
    code                              text NOT NULL,
    name                              text,
    cdn_base_url                      text,
    signed_urls                       boolean DEFAULT false,
    signed_url_ttl_seconds            integer,
    default_rendition                 text,
    fallback_asset_id                 uuid,
    on_rights_expiry                  text DEFAULT 'serveFallback' CONSTRAINT distribution_channel_on_rights_expiry_chk CHECK (on_rights_expiry IN ('serveFallback', 'serveNothing', 'continueServing')),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- An image, video or document with a licence and a lifecycle. Referenced everywhere and owned by
-- one service, so a takedown is one delete
CREATE TABLE IF NOT EXISTS assets.media_asset (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT media_asset_kind_chk CHECK (kind IN ('image', 'video', 'audio', 'document', 'vector', 'font', 'archive')),
    status                            text NOT NULL CONSTRAINT media_asset_status_chk CHECK (status IN ('processing', 'ready', 'quarantined', 'failed', 'archived')),
    filename                          text NOT NULL,
    content_type                      text NOT NULL,
    size_bytes                        integer NOT NULL,
    title                             jsonb,
    description                       jsonb,
    alt_text                          jsonb,
    width                             integer,
    height                            integer,
    duration_seconds                  numeric(18,4),
    custom_metadata                   jsonb,
    shared_with_tenant_ids            text[],
    tags                              text[],
    venue_id                          uuid,
    url                               text,
    thumbnail_url                     text,
    reference_count                   integer NOT NULL,
    rights                            jsonb,
    is_rights_expired                 boolean,
    version                           integer,
    uploaded_by_principal_id          uuid,
    created_at                        timestamptz NOT NULL
);

-- A named group of assets, so a gallery is one reference rather than forty
CREATE TABLE IF NOT EXISTS assets.media_collection (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    description                       text,
    venue_id                          uuid,
    parent_collection_id              uuid,
    asset_count                       integer NOT NULL,
    cover_asset_id                    uuid
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.media_collection_member (
    id                                uuid PRIMARY KEY NOT NULL,
    collection_id                     uuid NOT NULL,
    asset_id                          uuid NOT NULL,
    added_by_principal_id             uuid,
    added_at                          timestamptz
);

-- An upload in progress, with the ticket a client uses to send bytes directly
CREATE TABLE IF NOT EXISTS assets.media_upload (
    id                                uuid PRIMARY KEY,
    upload_id                         uuid NOT NULL,
    upload_url                        text NOT NULL,
    method                            text NOT NULL CONSTRAINT media_upload_method_chk CHECK (method IN ('PUT', 'POST')),
    headers                           jsonb,
    max_size_bytes                    integer,
    expires_at                        timestamptz NOT NULL,
    filename                          text,
    content_type                      text,
    size_bytes                        integer,
    venue_id                          uuid,
    asset_id                          uuid
);

-- Where an asset is used. What a takedown has to check before deleting
CREATE TABLE IF NOT EXISTS assets.media_usage (
    extracted_text                    text,
    id                                uuid PRIMARY KEY,
    surface                           text NOT NULL CONSTRAINT media_usage_surface_chk CHECK (surface IN ('tenantBranding', 'homepageBanner', 'promoBlock', 'contentPage', 'product', 'event', 'menuItem', 'merchandise', 'workOrder', 'incident', 'inspection', 'campaign')),
    reference_id                      text NOT NULL,
    label                             text,
    is_live                           boolean,
    asset_id                          uuid NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.rendition (
    id                                uuid PRIMARY KEY,
    preset                            text NOT NULL,
    format                            text,
    width                             integer,
    height                            integer,
    size_bytes                        integer,
    status                            text CONSTRAINT rendition_status_chk CHECK (status IN ('queued', 'processing', 'ready', 'failed')),
    failure_reason                    text,
    url                               text,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.share (
    id                                uuid PRIMARY KEY,
    asset_ids                         text[] NOT NULL,
    recipient_email                   text,
    recipient_organisation            text,
    allow_download                    boolean DEFAULT false,
    allowed_renditions                text[],
    is_password_protected             boolean DEFAULT false,
    expires_at                        timestamptz NOT NULL,
    revoked_at                        timestamptz,
    url                               text,
    opened_count                      integer,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.tag (
    value                             text NOT NULL,
    vocabulary                        text,
    source                            text DEFAULT 'human' CONSTRAINT tag_source_chk CHECK (source IN ('human', 'autoTag', 'import', 'inherited')),
    confidence                        numeric(18,4),
    is_accepted                       boolean DEFAULT true,
    added_by                          uuid,
    added_at                          timestamptz,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 2 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.taxonomy (
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

