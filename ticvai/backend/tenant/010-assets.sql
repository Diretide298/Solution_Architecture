-- assets — 12 tables
-- **Derived. Do not hand-edit.**

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.approval (
    asset_id                          uuid,
    state                             text,
    approved_by                       uuid,
    comment                           text,
    at                                timestamptz,
    scope_path                        text,
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
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.audit (
    id                                uuid PRIMARY KEY,
    asset_id                          uuid,
    at                                timestamptz,
    action                            text,
    actor_id                          uuid,
    recipient                         text,
    detail                            text,
    scope_path                        text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.distribution_channel (
    code                              text NOT NULL,
    name                              text,
    cdn_base_url                      text,
    signed_urls                       boolean,
    signed_url_ttl_seconds            integer,
    default_rendition                 text,
    fallback_asset_id                 uuid,
    on_rights_expiry                  text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- An image, video or document with a licence and a lifecycle. Referenced everywhere and owned by
-- one service, so a takedown is one delete
CREATE TABLE IF NOT EXISTS assets.media_asset (
    id                                uuid PRIMARY KEY,
    kind                              text,
    status                            text,
    filename                          text,
    content_type                      text,
    size_bytes                        integer,
    title                             jsonb,
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
    reference_count                   integer,
    rights                            jsonb,
    is_rights_expired                 boolean,
    version                           integer,
    uploaded_by_principal_id          uuid,
    created_at                        timestamptz
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

-- An upload in progress, with the ticket a client uses to send bytes directly
CREATE TABLE IF NOT EXISTS assets.media_upload (
    id                                uuid PRIMARY KEY,
    upload_id                         uuid NOT NULL,
    upload_url                        text NOT NULL,
    method                            text NOT NULL,
    headers                           jsonb,
    max_size_bytes                    integer,
    expires_at                        timestamptz NOT NULL
);

-- Where an asset is used. What a takedown has to check before deleting
CREATE TABLE IF NOT EXISTS assets.media_usage (
    id                                uuid PRIMARY KEY,
    surface                           text NOT NULL,
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
    status                            text,
    failure_reason                    text,
    url                               text,
    scope_path                        text
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.share (
    id                                uuid PRIMARY KEY,
    asset_ids                         text[] NOT NULL,
    recipient_email                   text,
    recipient_organisation            text,
    allow_download                    boolean,
    allowed_renditions                text[],
    password_protected                boolean,
    expires_at                        timestamptz NOT NULL,
    revoked_at                        timestamptz,
    url                               text,
    opened_count                      integer,
    scope_path                        text
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.tag (
    value                             text NOT NULL,
    vocabulary                        text,
    source                            text,
    confidence                        numeric(18,4),
    accepted                          boolean,
    added_by                          uuid,
    added_at                          timestamptz,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 2 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS assets.taxonomy (
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

