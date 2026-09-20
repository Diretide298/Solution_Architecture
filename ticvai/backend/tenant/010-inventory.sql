-- inventory — 20 tables
-- **Derived. Do not hand-edit.**

-- A stock take. Its lines carry both the counted number and the recount, because two counts that
-- agree is a different fact from one nobody checked
CREATE TABLE IF NOT EXISTS inventory.count (
    id                                text PRIMARY KEY NOT NULL,
    location_id                       uuid NOT NULL,
    location_name                     text,
    kind                              text NOT NULL,
    status                            text NOT NULL,
    is_blind                          boolean NOT NULL,
    line_count                        integer NOT NULL,
    counted_count                     integer NOT NULL,
    variance_line_count               integer,
    variance_value                    numeric(18,4),
    started_by_principal_id           uuid,
    posted_by_principal_id            uuid,
    journal_entry_id                  text,
    started_at                        timestamptz NOT NULL,
    closed_at                         timestamptz,
    posted_at                         timestamptz
);

-- What was actually on the shelf (client board 5, 24 August). A count could be opened and posted
-- and nothing recorded what was counted. The theoretical quantity is snapshotted at entry, not at
-- post — stock moves during a count, and a variance computed at post time measures against a
-- different number from the one the counter was looking at
CREATE TABLE IF NOT EXISTS inventory.count_line (
    id                                uuid PRIMARY KEY NOT NULL,
    count_id                          uuid NOT NULL,
    item_id                           uuid NOT NULL,
    location_id                       uuid,
    batch_id                          uuid,
    counted_quantity                  numeric(18,4) NOT NULL,
    theoretical_quantity              numeric(18,4),
    uom                               text,
    variance                          numeric(18,4),
    variance_percent                  numeric(18,4),
    status                            text,
    counted_by_principal_id           uuid,
    counted_at                        timestamptz,
    note                              text
);

-- Stock arriving against a purchase order. Where a three-way match would begin
CREATE TABLE IF NOT EXISTS inventory.goods_receipt (
    id                                text PRIMARY KEY NOT NULL,
    receipt_number                    text NOT NULL,
    purchase_order_id                 text NOT NULL,
    location_id                       uuid NOT NULL,
    delivery_note_reference           text,
    total_value                       numeric(18,4),
    received_by_principal_id          uuid NOT NULL,
    journal_entry_id                  text,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz,
    synced_at                         timestamptz
);

-- One line received, which may differ from what was ordered
CREATE TABLE IF NOT EXISTS inventory.goods_receipt_line (
    goods_receipt_id                  text NOT NULL,
    item_id                           uuid,
    item_name                         text,
    ordered_quantity                  numeric(18,4),
    received_quantity                 numeric(18,4),
    rejected_quantity                 numeric(18,4),
    batch_number                      text,
    expiry_date                       date,
    unit_cost                         numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Something a venue stocks, distinct from something it sells. A bottle of syrup is an item and
-- never a product; a t-shirt is both, joined through retail.merchandise
CREATE TABLE IF NOT EXISTS inventory.item (
    sku                               text,
    barcode                           text,
    name                              text,
    venue_id                          uuid,
    category_id                       uuid,
    base_unit                         text,
    purchase_unit                     text,
    purchase_unit_factor              numeric(18,4),
    costing_method                    text,
    reorder_point                     numeric(18,4),
    reorder_quantity                  numeric(18,4),
    par_level                         numeric(18,4),
    preferred_supplier_id             uuid,
    allow_negative_stock              boolean,
    is_perishable                     boolean,
    shelf_life_days                   integer,
    id                                uuid PRIMARY KEY,
    on_hand                           numeric(18,4),
    on_order                          numeric(18,4),
    in_transit                        numeric(18,4),
    available                         numeric(18,4),
    average_cost                      numeric(18,4),
    last_purchase_price               numeric(18,4),
    is_below_reorder_point            boolean,
    has_movements                     boolean,
    is_active                         boolean
);

-- Where stock physically is — a stockroom, a bar, a cellar
CREATE TABLE IF NOT EXISTS inventory.location (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL,
    parent_location_id                uuid,
    is_active                         boolean
);

-- Every change in stock, and the only truth about a level — stock_level is computed from these and
-- never stored
CREATE TABLE IF NOT EXISTS inventory.movement (
    id                                text PRIMARY KEY,
    item_id                           uuid,
    location_id                       uuid,
    kind                              text,
    quantity                          numeric(18,4),
    unit                              text,
    reason                            text,
    cost_center_id                    uuid,
    recorded_at                       timestamptz,
    balance_after                     numeric(18,4),
    unit_cost                         numeric(18,4),
    total_cost                        numeric(18,4),
    principal_id                      uuid,
    source_type                       text,
    source_id                         text,
    journal_entry_id                  text,
    created_at                        timestamptz
);

-- A commitment to buy, priced in the supplier’s currency
CREATE TABLE IF NOT EXISTS inventory.purchase_order (
    id                                text PRIMARY KEY NOT NULL,
    purchase_order_number             text NOT NULL,
    requisition_id                    text,
    supplier_id                       uuid NOT NULL,
    supplier_name                     text,
    kind                              text,
    blanket_parent_id                 uuid,
    contract_price_valid_until        date,
    rfq_id                            uuid,
    supplier_invoice_ref              text,
    match_status                      text,
    status                            text NOT NULL,
    deliver_to_location_id            uuid,
    subtotal                          numeric(18,4),
    tax_amount                        numeric(18,4),
    total                             numeric(18,4) NOT NULL,
    expected_delivery                 date,
    raised_by_principal_id            uuid,
    created_at                        timestamptz NOT NULL,
    closed_at                         timestamptz,
    venue_id                          uuid,
    scope_path                        text
);

-- One item ordered, at a unit price
CREATE TABLE IF NOT EXISTS inventory.purchase_order_line (
    purchase_order_id                 text NOT NULL,
    line_id                           text,
    item_id                           uuid,
    item_name                         text,
    ordered_quantity                  numeric(18,4),
    received_quantity                 numeric(18,4),
    outstanding_quantity              numeric(18,4),
    unit_price                        numeric(18,4),
    line_total                        numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- A supplier’s price, comparable against others
CREATE TABLE IF NOT EXISTS inventory.quotation (
    requisition_id                    text,
    reference                         text,
    lead_time_days                    integer,
    valid_until                       date,
    note                              text,
    id                                uuid PRIMARY KEY,
    supplier_id                       uuid,
    supplier_name                     text,
    total                             numeric(18,4),
    is_selected                       boolean,
    received_at                       timestamptz,
    scope_path                        text
);

-- One item quoted. Hangs off: a child of inventory.quotation; reaches inventory.item through its
-- keys; references inventory.item, inventory.quotation.
CREATE TABLE IF NOT EXISTS inventory.quotation_line (
    quotation_id                      uuid NOT NULL,
    item_id                           uuid NOT NULL,
    quantity                          numeric(18,4) NOT NULL,
    unit_price                        numeric(18,4) NOT NULL,
    unit                              text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A department asking for stock, which becomes a movement when fulfilled. The line items are
-- children
CREATE TABLE IF NOT EXISTS inventory.requisition (
    id                                text PRIMARY KEY NOT NULL,
    requisition_number                text NOT NULL,
    venue_id                          uuid NOT NULL,
    department_id                     uuid,
    status                            text NOT NULL,
    estimated_total                   numeric(18,4),
    raised_by_principal_id            uuid NOT NULL,
    approved_by_principal_id          uuid,
    approval_note                     text,
    required_by                       date,
    created_at                        timestamptz NOT NULL,
    approved_at                       timestamptz
);

-- One item asked for. Hangs off: a child of inventory.requisition; reaches inventory.item through
-- its keys; references inventory.item, inventory.requisition.
CREATE TABLE IF NOT EXISTS inventory.requisition_line (
    requisition_id                    text NOT NULL,
    line_id                           text,
    item_id                           uuid,
    item_name                         text,
    requested_quantity                numeric(18,4),
    approved_quantity                 numeric(18,4),
    ordered_quantity                  numeric(18,4),
    unit                              text,
    estimated_cost                    numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Where an individual item is (Retail Board 4). A lot number answers which delivery; a serial
-- answers which one — a warranty claim, a recall and a proof of purchase all start there
CREATE TABLE IF NOT EXISTS inventory.serialised_item (
    id                                uuid PRIMARY KEY NOT NULL,
    item_id                           uuid NOT NULL,
    batch_id                          uuid,
    serial                            text NOT NULL,
    location_id                       uuid,
    status                            text NOT NULL,
    sold_on_order_line_id             uuid,
    warranty_until                    date,
    received_at                       timestamptz
);

-- The instance that actually expires (BL-122). isPerishable and shelfLifeDays are on the item, so
-- a shelf life was declared and never instantiated — two deliveries a week apart were one stock
-- level with one implied expiry
CREATE TABLE IF NOT EXISTS inventory.stock_batch (
    id                                uuid PRIMARY KEY NOT NULL,
    item_id                           uuid NOT NULL,
    location_id                       uuid NOT NULL,
    batch_code                        text,
    lot_number                        text,
    quantity                          numeric(18,4) NOT NULL,
    received_at                       timestamptz NOT NULL,
    expires_at                        date,
    supplier_id                       uuid,
    status                            text
);

CREATE TABLE IF NOT EXISTS inventory.stock_reservation (
    id                                uuid PRIMARY KEY,
    item_id                           uuid NOT NULL,
    location_id                       uuid NOT NULL,
    quantity                          numeric(18,4) NOT NULL,
    source_type                       text NOT NULL,
    source_id                         uuid NOT NULL,
    status                            text NOT NULL,
    expires_at                        timestamptz,
    created_at                        timestamptz NOT NULL,
    released_at                       timestamptz
);

-- Who a venue buys from, invoicing in their own currency
CREATE TABLE IF NOT EXISTS inventory.supplier (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    contact_name                      text,
    contact_email                     text,
    contact_phone                     text,
    tax_registration_number           text,
    payment_terms_days                integer,
    lead_time_days                    integer,
    currency                          text,
    account_id                        uuid,
    is_active                         boolean,
    scope_path                        text
);

CREATE TABLE IF NOT EXISTS inventory.supplier_contract (
    id                                uuid PRIMARY KEY,
    supplier_id                       uuid NOT NULL,
    number                            text NOT NULL,
    name                              text NOT NULL,
    valid_from                        date NOT NULL,
    valid_to                          date,
    currency_code                     text,
    payment_terms_days                integer,
    document_reference                text,
    status                            text NOT NULL,
    created_by_user_id                uuid,
    created_at                        timestamptz NOT NULL
);

-- Stock moving between locations. In transit is a state, not a gap
CREATE TABLE IF NOT EXISTS inventory.transfer (
    id                                text PRIMARY KEY NOT NULL,
    transfer_number                   text,
    from_location_id                  uuid NOT NULL,
    to_location_id                    uuid NOT NULL,
    status                            text NOT NULL,
    dispatched_by_principal_id        uuid,
    received_by_principal_id          uuid,
    dispatched_at                     timestamptz NOT NULL,
    received_at                       timestamptz,
    scope_path                        text
);

-- One item moving, which is in neither location until it arrives
CREATE TABLE IF NOT EXISTS inventory.transfer_line (
    transfer_id                       text NOT NULL,
    item_id                           uuid,
    item_name                         text,
    dispatched_quantity               numeric(18,4),
    received_quantity                 numeric(18,4),
    discrepancy                       numeric(18,4),
    discrepancy_reason                text,
    id                                uuid PRIMARY KEY NOT NULL
);

