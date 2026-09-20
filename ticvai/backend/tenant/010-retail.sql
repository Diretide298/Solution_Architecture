-- retail — 18 tables
-- **Derived. Do not hand-edit.**

-- Goods swapped rather than returned, which settles differently
CREATE TABLE IF NOT EXISTS retail.exchange (
    id                                text PRIMARY KEY NOT NULL,
    sale_id                           text NOT NULL,
    return_id                         text NOT NULL,
    new_sale_id                       text NOT NULL,
    returned_value                    numeric(18,4),
    replacement_value                 numeric(18,4),
    difference                        numeric(18,4) NOT NULL,
    created_at                        timestamptz
);

-- A product a venue sells as goods, joined to the catalogue rather than duplicating it
CREATE TABLE IF NOT EXISTS retail.merchandise (
    description                       text,
    id                                uuid PRIMARY KEY NOT NULL,
    sku                               text NOT NULL,
    barcode                           text,
    name                              text NOT NULL,
    outlet_id                         uuid NOT NULL,
    category_id                       uuid,
    variant_id                        uuid NOT NULL,
    inventory_item_id                 uuid,
    price                             numeric(18,4) NOT NULL,
    on_hand                           numeric(18,4) NOT NULL,
    is_returnable                     boolean,
    return_window_days                integer,
    requires_serial_number            boolean,
    image_asset_ref                   text,
    is_active                         boolean NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is.
CREATE TABLE IF NOT EXISTS retail.price (
    id                                uuid PRIMARY KEY,
    list_id                           uuid NOT NULL,
    product_id                        uuid NOT NULL,
    variant_id                        uuid,
    amount                            numeric(18,4) NOT NULL,
    tax_code                          text,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is.
CREATE TABLE IF NOT EXISTS retail.price_list (
    id                                uuid PRIMARY KEY,
    scope_path                        text,
    code                              text NOT NULL,
    name                              text NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    channels_json                     text,
    priority                          integer NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is.
CREATE TABLE IF NOT EXISTS retail.product (
    id                                uuid PRIMARY KEY,
    scope_path                        text,
    category_id                       uuid NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    brand                             text,
    tax_code                          text,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is.
CREATE TABLE IF NOT EXISTS retail.product_category (
    id                                uuid PRIMARY KEY,
    scope_path                        text,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is.
CREATE TABLE IF NOT EXISTS retail.product_recommendation (
    id                                uuid PRIMARY KEY,
    scope_path                        text,
    source_product_id                 uuid NOT NULL,
    source_variant_id                 uuid,
    type                              text NOT NULL,
    target_service                    text NOT NULL,
    target_product_id                 uuid NOT NULL,
    target_variant_id                 uuid,
    display_message                   text,
    default_quantity                  numeric(18,4) NOT NULL,
    max_quantity                      numeric(18,4),
    priority                          integer NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Merchandise held for collection. Hangs off: reaches retail.sale through its keys; references
-- pii.subject, platform.outlet. Reached by: 1 operations read it and 1 write it; 3 tables
-- reference it.
CREATE TABLE IF NOT EXISTS retail.reservation (
    id                                text PRIMARY KEY NOT NULL,
    reservation_number                text,
    outlet_id                         uuid NOT NULL,
    subject_id                        uuid,
    status                            text NOT NULL,
    collection_note                   text,
    expires_at                        timestamptz NOT NULL,
    collected_at                      timestamptz
);

-- One item reserved. Hangs off: a child of retail.reservation; reaches retail.sale through its
-- keys; references retail.merchandise, retail.reservation.
CREATE TABLE IF NOT EXISTS retail.reservation_line (
    reservation_id                    text NOT NULL,
    merchandise_id                    uuid,
    name                              text,
    quantity                          integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Goods coming back, against the sale that produced them
CREATE TABLE IF NOT EXISTS retail."return" (
    id                                text PRIMARY KEY NOT NULL,
    return_number                     text,
    sale_id                           text NOT NULL,
    refund_id                         text,
    reason                            text,
    refund_amount                     numeric(18,4) NOT NULL,
    refund_tender                     text,
    restocked_quantity                integer NOT NULL,
    written_off_quantity              integer NOT NULL,
    accepted_by_principal_id          uuid,
    secondary_principal_id            uuid,
    created_at                        timestamptz NOT NULL
);

-- One item returned, with its condition
CREATE TABLE IF NOT EXISTS retail.return_line (
    return_id                         text NOT NULL,
    line_id                           text,
    merchandise_id                    uuid,
    name                              text,
    quantity                          integer,
    condition                         text,
    was_restocked                     boolean,
    refund_amount                     numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- When goods may come back and in what state. Outlet-scoped
CREATE TABLE IF NOT EXISTS retail.return_policy (
    id                                uuid PRIMARY KEY,
    outlet_id                         uuid NOT NULL,
    default_window_days               integer NOT NULL,
    requires_receipt                  boolean NOT NULL,
    allow_cash_refund_on_card_sale    boolean,
    self_authorise_limit              numeric(18,4),
    requires_second_user_above        numeric(18,4),
    requires_approval_above           numeric(18,4),
    non_returnable_category_ids       text[]
);

-- A retail transaction, distinct from an admission sale because it moves stock
CREATE TABLE IF NOT EXISTS retail.sale (
    id                                text PRIMARY KEY NOT NULL,
    receipt_number                    text NOT NULL,
    order_id                          text NOT NULL,
    outlet_id                         uuid NOT NULL,
    shift_id                          text,
    subject_id                        uuid,
    subtotal                          numeric(18,4),
    discount_amount                   numeric(18,4),
    tax_amount                        numeric(18,4),
    gross_amount                      numeric(18,4) NOT NULL,
    reprint_count                     integer,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz
);

-- One item sold, which produces a stock movement
CREATE TABLE IF NOT EXISTS retail.sale_line (
    sale_id                           text NOT NULL,
    line_id                           text,
    merchandise_id                    uuid,
    name                              text,
    quantity                          integer,
    unit_price                        numeric(18,4),
    discount                          numeric(18,4),
    line_total                        numeric(18,4),
    serial_numbers                    text[],
    returned_quantity                 integer,
    is_returnable                     boolean,
    not_returnable_reason             text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Bought now, collected later. The reason a guest is not carrying it round the park
CREATE TABLE IF NOT EXISTS retail.shop_and_drop (
    id                                text PRIMARY KEY NOT NULL,
    drop_reference                    text NOT NULL,
    sale_id                           text NOT NULL,
    entitlement_id                    text,
    subject_id                        uuid,
    collection_point_id               uuid NOT NULL,
    collection_point_name             text,
    status                            text NOT NULL,
    dropped_at                        timestamptz,
    collect_by                        timestamptz NOT NULL,
    collected_at                      timestamptz,
    collected_by_principal_id         uuid,
    verified_by                       text,
    collected_by                      uuid,
    venue_id                          uuid
);

-- One item bought for later collection. Hangs off: a child of retail.shop_and_drop; reaches
-- retail.sale through its keys; references retail.merchandise, retail.shop_and_drop.
CREATE TABLE IF NOT EXISTS retail.shop_and_drop_line (
    shop_and_drop_id                  text NOT NULL,
    line_id                           text,
    merchandise_id                    uuid,
    name                              text,
    quantity                          integer,
    collected_quantity                integer,
    id                                uuid PRIMARY KEY NOT NULL,
    drop_id                           text
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS retail.store_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    outlet_id                         uuid,
    kind                              text,
    threshold_minor                   integer,
    requires_permission               text,
    enabled                           boolean,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is.
CREATE TABLE IF NOT EXISTS retail.variant (
    id                                uuid PRIMARY KEY,
    product_id                        uuid NOT NULL,
    sku                               text NOT NULL,
    name                              text NOT NULL,
    barcode                           text,
    attributes_json                   text,
    is_default                        boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

