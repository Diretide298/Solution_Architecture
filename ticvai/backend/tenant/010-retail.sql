-- retail — 13 tables
-- **Derived. Do not hand-edit.**

-- Goods swapped rather than returned, which settles differently
CREATE TABLE IF NOT EXISTS retail.exchange (
    id                                uuid PRIMARY KEY NOT NULL,
    sale_id                           uuid NOT NULL,
    return_id                         uuid NOT NULL,
    new_sale_id                       uuid NOT NULL,
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
    list_price                        numeric(18,4) NOT NULL,
    on_hand                           numeric(18,4) NOT NULL,
    is_returnable                     boolean DEFAULT true,
    return_window_days                integer,
    requires_serial_number            boolean DEFAULT false,
    image_asset_ref                   text,
    is_active                         boolean NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS retail.product_recommendation (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    source_product_id                 uuid NOT NULL,
    source_variant_id                 uuid,
    type                              text NOT NULL CONSTRAINT product_recommendation_type_chk CHECK (char_length(type) <= 30),
    target_service                    text NOT NULL CONSTRAINT product_recommendation_target_service_chk CHECK (char_length(target_service) <= 30),
    target_product_id                 uuid NOT NULL,
    target_variant_id                 uuid,
    display_message                   text CONSTRAINT product_recommendation_display_message_chk CHECK (char_length(display_message) <= 300),
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
-- pii.subject, platform.outlet. Reached by: 1 operations read it and 1 write it; 1 tables
-- reference it.
CREATE TABLE IF NOT EXISTS retail.reservation (
    id                                uuid PRIMARY KEY NOT NULL,
    reservation_number                text,
    outlet_id                         uuid NOT NULL,
    subject_id                        uuid,
    status                            text NOT NULL CONSTRAINT reservation_status_chk CHECK (status IN ('reserved', 'collected', 'expired', 'cancelled')),
    collection_note                   text,
    expires_at                        timestamptz NOT NULL,
    collected_at                      timestamptz
);

-- One item reserved. Hangs off: a child of retail.reservation; reaches retail.sale through its
-- keys; references retail.merchandise, retail.reservation. Reached by: 1 operations read it and 1
-- write it.
CREATE TABLE IF NOT EXISTS retail.reservation_line (
    reservation_id                    uuid NOT NULL,
    merchandise_id                    uuid,
    name                              text,
    quantity                          integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Goods coming back, against the sale that produced them
CREATE TABLE IF NOT EXISTS retail."return" (
    id                                uuid PRIMARY KEY NOT NULL,
    return_number                     text,
    sale_id                           uuid NOT NULL,
    refund_id                         uuid,
    reason                            text CONSTRAINT return_reason_chk CHECK (reason IN ('changedMind', 'wrongSize', 'wrongItem', 'faulty', 'damagedInTransit', 'duplicatePurchase', 'giftReturn', 'other')),
    refund_amount                     numeric(18,4) NOT NULL,
    refund_tender                     text,
    restocked_quantity                integer NOT NULL,
    written_off_quantity              integer NOT NULL,
    status                            text NOT NULL,
    refused_reason                    text,
    accepted_by_principal_id          uuid,
    secondary_principal_id            uuid,
    created_at                        timestamptz NOT NULL
);

-- One item returned, with its condition
CREATE TABLE IF NOT EXISTS retail.return_line (
    return_id                         uuid NOT NULL,
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
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid NOT NULL,
    default_window_days               integer NOT NULL,
    requires_receipt                  boolean NOT NULL DEFAULT true,
    allow_cash_refund_on_card_sale    boolean DEFAULT false,
    self_authorise_limit              numeric(18,4),
    requires_second_user_above        numeric(18,4),
    requires_approval_above           numeric(18,4),
    restockable_conditions            text[],
    non_returnable_category_ids       text[]
);

-- A retail transaction, distinct from an admission sale because it moves stock
CREATE TABLE IF NOT EXISTS retail.sale (
    id                                uuid PRIMARY KEY NOT NULL,
    receipt_number                    text NOT NULL,
    order_id                          uuid NOT NULL,
    outlet_id                         uuid NOT NULL,
    shift_id                          uuid,
    subject_id                        uuid,
    net_amount                        numeric(18,4),
    discount_amount                   numeric(18,4),
    tax_amount                        numeric(18,4),
    gross_amount                      numeric(18,4) NOT NULL,
    reprint_count                     integer,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz
);

-- One item sold, which produces a stock movement
CREATE TABLE IF NOT EXISTS retail.sale_line (
    sale_id                           uuid NOT NULL,
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
    id                                uuid PRIMARY KEY NOT NULL,
    drop_reference                    text NOT NULL,
    sale_id                           uuid,
    order_id                          uuid,
    entitlement_id                    uuid,
    subject_id                        uuid,
    collection_point_id               uuid NOT NULL,
    collection_point_name             text,
    status                            text NOT NULL CONSTRAINT shop_and_drop_status_chk CHECK (status IN ('awaitingCollection', 'partiallyCollected', 'collected', 'uncollected', 'disposed')),
    dropped_at                        timestamptz,
    collect_by                        timestamptz NOT NULL,
    collected_at                      timestamptz,
    collected_by_principal_id         uuid,
    verified_by                       text,
    venue_id                          uuid
);

-- One item bought for later collection. Hangs off: a child of retail.shop_and_drop; reaches
-- retail.sale through its keys; references retail.merchandise, retail.shop_and_drop. Reached by: 3
-- operations read it and 0 write it.
CREATE TABLE IF NOT EXISTS retail.shop_and_drop_line (
    shop_and_drop_id                  uuid NOT NULL,
    line_id                           text,
    merchandise_id                    uuid,
    name                              text,
    quantity                          integer,
    collected_quantity                integer,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS retail.store_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    outlet_id                         uuid,
    kind                              text CONSTRAINT store_rule_kind_chk CHECK (kind IN ('discountLimit', 'refundThreshold', 'ageCheck', 'managerOverride', 'priceOverride')),
    threshold_amount                  numeric(18,4),
    limit_kind                        text CONSTRAINT store_rule_limit_kind_chk CHECK (limit_kind IN ('percent', 'amount')),
    threshold_percent                 numeric(18,4),
    minimum_age_years                 integer,
    requires_permission               text,
    is_enabled                        boolean,
    updated_at                        timestamptz,
    updated_by_principal_id           uuid
);

