-- assets — 4 tables
-- **Derived. Do not hand-edit.**

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

