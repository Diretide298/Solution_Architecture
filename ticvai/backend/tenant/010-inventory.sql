-- inventory — 22 tables
-- **Derived. Do not hand-edit.**

-- A stock take. Its lines carry both the counted number and the recount, because two counts that
-- agree is a different fact from one nobody checked
CREATE TABLE IF NOT EXISTS inventory.count (
    id                                uuid PRIMARY KEY NOT NULL,
    location_id                       uuid NOT NULL,
    location_name                     text,
    kind                              text NOT NULL,
    status                            text NOT NULL CONSTRAINT count_status_chk CHECK (status IN ('open', 'counting', 'closed', 'variancePending', 'posted', 'cancelled')),
    is_blind                          boolean NOT NULL,
    line_count                        integer NOT NULL,
    counted_count                     integer NOT NULL,
    variance_line_count               integer,
    variance_value                    numeric(18,4),
    started_by_principal_id           uuid,
    posted_by_principal_id            uuid,
    journal_entry_id                  uuid,
    started_at                        timestamptz NOT NULL,
    closed_at                         timestamptz,
    posted_at                         timestamptz,
    recount_reason                    text,
    recount_signed_by_principal_id    uuid,
    cancel_reason                     text
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
    status                            text CONSTRAINT count_line_status_chk CHECK (status IN ('entered', 'recountRequested', 'recounted', 'accepted', 'rejected')),
    counted_by_principal_id           uuid,
    counted_at                        timestamptz,
    note                              text
);

CREATE TABLE IF NOT EXISTS inventory.daily_count_list (
    id                                uuid PRIMARY KEY NOT NULL,
    item_ids                          text[] NOT NULL,
    location_id                       uuid,
    due_by                            text,
    does_post_adjustment              boolean NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Stock arriving against a purchase order. Where a three-way match would begin
CREATE TABLE IF NOT EXISTS inventory.goods_receipt (
    id                                uuid PRIMARY KEY NOT NULL,
    receipt_number                    text NOT NULL,
    purchase_order_id                 uuid NOT NULL,
    location_id                       uuid NOT NULL,
    delivery_note_reference           text,
    net_value_amount                  numeric(18,4),
    received_by_principal_id          uuid NOT NULL,
    journal_entry_id                  uuid,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz,
    synced_at                         timestamptz
);

-- One line received, which may differ from what was ordered
CREATE TABLE IF NOT EXISTS inventory.goods_receipt_line (
    goods_receipt_id                  uuid NOT NULL,
    line_id                           uuid,
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
    sku                               text NOT NULL CONSTRAINT item_sku_chk CHECK (char_length(sku) <= 64),
    barcode                           text CONSTRAINT item_barcode_chk CHECK (char_length(barcode) <= 128),
    name                              text NOT NULL CONSTRAINT item_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    category_id                       uuid,
    base_unit                         text NOT NULL,
    purchase_unit                     text,
    purchase_unit_factor              numeric(18,4) DEFAULT 1,
    costing_method                    text NOT NULL CONSTRAINT item_costing_method_chk CHECK (costing_method IN ('weightedAverage', 'fifo', 'standardCost', 'lastPurchasePrice')),
    reorder_point                     numeric(18,4),
    reorder_quantity                  numeric(18,4),
    par_level                         numeric(18,4),
    preferred_supplier_id             uuid,
    allow_negative_stock              boolean DEFAULT false,
    is_perishable                     boolean DEFAULT false,
    shelf_life_days                   integer,
    id                                uuid PRIMARY KEY NOT NULL,
    on_hand                           numeric(18,4) NOT NULL,
    on_order                          numeric(18,4),
    in_transit                        numeric(18,4),
    available                         numeric(18,4),
    average_cost                      numeric(18,4),
    last_purchase_price               numeric(18,4),
    is_below_reorder_point            boolean,
    has_movements                     boolean,
    is_active                         boolean NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS inventory.kit_component (
    kit_item_id                       uuid,
    component_item_id                 uuid NOT NULL,
    quantity                          numeric(18,4) NOT NULL,
    unit                              text,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Where stock physically is — a stockroom, a bar, a cellar
CREATE TABLE IF NOT EXISTS inventory.location (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT location_kind_chk CHECK (kind IN ('mainStore', 'subStore', 'kitchen', 'bar', 'retailFloor', 'cellar', 'transit')),
    parent_location_id                uuid,
    is_active                         boolean
);

-- Every change in stock, and the only truth about a level — stock_level is computed from these and
-- never stored
CREATE TABLE IF NOT EXISTS inventory.movement (
    id                                uuid PRIMARY KEY NOT NULL,
    item_id                           uuid NOT NULL,
    location_id                       uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT movement_kind_chk CHECK (kind IN ('receipt', 'issue', 'saleDepletion', 'waste', 'adjustmentIn', 'adjustmentOut', 'transferOut', 'transferIn', 'countGain', 'countLoss', 'supplierReturn', 'production')),
    quantity                          numeric(18,4) NOT NULL,
    unit                              text,
    reason                            text CONSTRAINT movement_reason_chk CHECK (char_length(reason) <= 500),
    cost_center_id                    uuid,
    recorded_at                       timestamptz NOT NULL,
    balance_after                     numeric(18,4) NOT NULL,
    unit_cost                         numeric(18,4),
    net_cost_amount                   numeric(18,4),
    principal_id                      uuid NOT NULL,
    source_type                       text,
    source_id                         text,
    journal_entry_id                  uuid,
    created_at                        timestamptz NOT NULL
);

-- A commitment to buy, priced in the supplier’s currency
CREATE TABLE IF NOT EXISTS inventory.purchase_order (
    id                                uuid PRIMARY KEY NOT NULL,
    purchase_order_number             text NOT NULL,
    requisition_id                    uuid,
    quotation_id                      uuid,
    supplier_id                       uuid NOT NULL,
    supplier_name                     text,
    kind                              text DEFAULT 'standard' CONSTRAINT purchase_order_kind_chk CHECK (kind IN ('standard', 'blanket', 'release', 'rfqAward')),
    blanket_parent_id                 uuid,
    contract_price_valid_until        date,
    rfq_id                            uuid,
    supplier_invoice_ref              text,
    match_status                      text CONSTRAINT purchase_order_match_status_chk CHECK (match_status IN ('unmatched', 'matched', 'priceVariance', 'quantityVariance', 'bothVariance')),
    status                            text NOT NULL CONSTRAINT purchase_order_status_chk CHECK (status IN ('raised', 'sent', 'acknowledged', 'partiallyReceived', 'received', 'closedShort', 'cancelled')),
    deliver_to_location_id            uuid,
    net_amount                        numeric(18,4),
    tax_amount                        numeric(18,4),
    gross_amount                      numeric(18,4) NOT NULL,
    expected_delivery                 date,
    raised_by_principal_id            uuid,
    created_at                        timestamptz NOT NULL,
    closed_at                         timestamptz,
    supplier_reference                text,
    acknowledged_at                   timestamptz,
    close_short_reason                text,
    cancel_reason                     text,
    approval_request_id               uuid,
    cancelled_at                      timestamptz,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL
);

-- One item ordered, at a unit price
CREATE TABLE IF NOT EXISTS inventory.purchase_order_line (
    purchase_order_id                 uuid NOT NULL,
    line_id                           text,
    item_id                           uuid,
    item_name                         text,
    ordered_quantity                  numeric(18,4),
    received_quantity                 numeric(18,4),
    outstanding_quantity              numeric(18,4),
    unit_price                        numeric(18,4),
    quoted_unit_price                 numeric(18,4),
    price_override_reason             text,
    line_total                        numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- A supplier’s price, comparable against others
CREATE TABLE IF NOT EXISTS inventory.quotation (
    requisition_id                    uuid NOT NULL,
    reference                         text CONSTRAINT quotation_reference_chk CHECK (char_length(reference) <= 128),
    lead_time_days                    integer,
    valid_until                       date NOT NULL,
    note                              text CONSTRAINT quotation_note_chk CHECK (char_length(note) <= 1000),
    id                                uuid PRIMARY KEY NOT NULL,
    supplier_id                       uuid NOT NULL,
    supplier_name                     text,
    gross_amount                      numeric(18,4) NOT NULL,
    is_selected                       boolean,
    received_at                       timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- One item quoted. Hangs off: a child of inventory.quotation; reaches inventory.item through its
-- keys; references inventory.item, inventory.quotation. Reached by: 2 operations read it and 1
-- write it.
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
    id                                uuid PRIMARY KEY NOT NULL,
    requisition_number                text NOT NULL,
    venue_id                          uuid NOT NULL,
    department_id                     uuid,
    cost_center_id                    uuid,
    justification                     text,
    status                            text NOT NULL CONSTRAINT requisition_status_chk CHECK (status IN ('draft', 'pendingApproval', 'approved', 'rejected', 'returnedForInfo', 'ordered', 'closed', 'cancelled')),
    estimated_total                   numeric(18,4),
    raised_by_principal_id            uuid NOT NULL,
    approved_by_principal_id          uuid,
    approval_note                     text,
    required_by                       date,
    created_at                        timestamptz NOT NULL,
    approved_at                       timestamptz,
    rejection_reason                  text,
    rejected_at                       timestamptz,
    return_question                   text,
    returned_at                       timestamptz,
    cancel_reason                     text,
    cancelled_at                      timestamptz
);

-- One item asked for. Hangs off: a child of inventory.requisition; reaches inventory.item through
-- its keys; references inventory.item, inventory.requisition. Reached by: 7 operations read it and
-- 2 write it.
CREATE TABLE IF NOT EXISTS inventory.requisition_line (
    requisition_id                    uuid NOT NULL,
    line_id                           text,
    item_id                           uuid,
    item_name                         text,
    requested_quantity                numeric(18,4),
    suggested_quantity                numeric(18,4),
    approved_quantity                 numeric(18,4),
    ordered_quantity                  numeric(18,4),
    unit                              text,
    reason                            text,
    note                              text,
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
    status                            text NOT NULL CONSTRAINT serialised_item_status_chk CHECK (status IN ('inStock', 'reserved', 'sold', 'returned', 'damaged', 'lost', 'inTransit', 'warranty')),
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
    status                            text CONSTRAINT stock_batch_status_chk CHECK (status IN ('available', 'quarantined', 'expired', 'recalled', 'consumed', 'written-off'))
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS inventory.stock_reservation (
    id                                uuid PRIMARY KEY NOT NULL,
    item_id                           uuid NOT NULL,
    location_id                       uuid NOT NULL,
    quantity                          numeric(18,4) NOT NULL,
    source_type                       text NOT NULL CONSTRAINT stock_reservation_source_type_chk CHECK (source_type IN ('workOrder', 'rentalAgreement', 'order', 'transfer', 'other')),
    source_id                         uuid NOT NULL,
    status                            text NOT NULL CONSTRAINT stock_reservation_status_chk CHECK (status IN ('active', 'consumed', 'released', 'expired')),
    expires_at                        timestamptz,
    created_at                        timestamptz NOT NULL,
    released_at                       timestamptz
);

-- Who a venue buys from, invoicing in their own currency
CREATE TABLE IF NOT EXISTS inventory.supplier (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT supplier_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT supplier_name_chk CHECK (char_length(name) <= 200),
    contact_name                      text,
    contact_email                     text,
    contact_phone                     text,
    tax_registration_number           text,
    payment_terms_days                integer,
    lead_time_days                    integer,
    currency                          text,
    account_id                        uuid,
    is_active                         boolean,
    status                            text CONSTRAINT supplier_status_chk CHECK (status IN ('active', 'onHold', 'suspended', 'terminated')),
    status_reason                     text,
    minimum_order_value               numeric(18,4),
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS inventory.supplier_contract (
    id                                uuid PRIMARY KEY NOT NULL,
    supplier_id                       uuid NOT NULL,
    number                            text NOT NULL CONSTRAINT supplier_contract_number_chk CHECK (char_length(number) <= 100),
    name                              text NOT NULL CONSTRAINT supplier_contract_name_chk CHECK (char_length(name) <= 200),
    valid_from                        date NOT NULL,
    valid_to                          date,
    currency_code                     text CONSTRAINT supplier_contract_currency_code_chk CHECK (char_length(currency_code) <= 10),
    payment_terms_days                integer,
    document_reference                text CONSTRAINT supplier_contract_document_reference_chk CHECK (char_length(document_reference) <= 500),
    status                            text NOT NULL CONSTRAINT supplier_contract_status_chk CHECK (status IN ('draft', 'active', 'expired', 'terminated') AND char_length(status) <= 30),
    status_reason                     text CONSTRAINT supplier_contract_status_reason_chk CHECK (char_length(status_reason) <= 500),
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL
);

-- Stock moving between locations. In transit is a state, not a gap
CREATE TABLE IF NOT EXISTS inventory.transfer (
    id                                uuid PRIMARY KEY NOT NULL,
    transfer_number                   text,
    from_location_id                  uuid NOT NULL,
    to_location_id                    uuid NOT NULL,
    status                            text NOT NULL CONSTRAINT transfer_status_chk CHECK (status IN ('dispatched', 'inTransit', 'received', 'partiallyReceived', 'cancelled')),
    dispatched_by_principal_id        uuid,
    received_by_principal_id          uuid,
    dispatched_at                     timestamptz NOT NULL,
    received_at                       timestamptz,
    close_short_reason                text,
    close_short_signed_by_principal_id uuid,
    from_venue_id                     uuid,
    to_venue_id                       uuid,
    scope_path                        ltree NOT NULL,
    to_scope_path                     ltree
);

-- One item moving, which is in neither location until it arrives
CREATE TABLE IF NOT EXISTS inventory.transfer_line (
    transfer_id                       uuid NOT NULL,
    item_id                           uuid,
    item_name                         text,
    dispatched_quantity               numeric(18,4),
    received_quantity                 numeric(18,4),
    discrepancy                       numeric(18,4),
    discrepancy_reason                text,
    id                                uuid PRIMARY KEY NOT NULL
);

