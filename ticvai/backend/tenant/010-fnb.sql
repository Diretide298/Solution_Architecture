-- fnb — 42 tables
-- **Derived. Do not hand-edit.**

-- How one table’s bill was divided. A party of six paying separately is the ordinary case
CREATE TABLE IF NOT EXISTS fnb.bill_split (
    id                                uuid PRIMARY KEY,
    visit_id                          text NOT NULL,
    method                            text NOT NULL
);

-- The temperature a delivery arrived at (board 5G). Taken before the receipt is posted — a claim
-- against a supplier needs the reading that refused it
CREATE TABLE IF NOT EXISTS fnb.cold_chain_event (
    id                                uuid PRIMARY KEY NOT NULL,
    goods_receipt_id                  uuid,
    transfer_id                       uuid,
    recorded_at                       timestamptz NOT NULL,
    value_celsius                     numeric(18,4) NOT NULL,
    threshold_celsius                 numeric(18,4),
    decision                          text NOT NULL,
    corrective_action_id              uuid,
    supplier_claim_raised             boolean
);

-- A meal deal, priced as one thing (client board 2G). A combo is one product with slots, not a
-- bundle of products — a model that prices by summing cannot express a deal
CREATE TABLE IF NOT EXISTS fnb.combo (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid,
    name                              text NOT NULL,
    name_localised                    jsonb,
    price                             numeric(18,4) NOT NULL,
    availability                      jsonb,
    is_active                         boolean
);

-- One choice within a combo. minSelect and maxSelect are what make it a slot rather than a line —
-- a main is exactly one, a sauce might be none or two
CREATE TABLE IF NOT EXISTS fnb.combo_slot (
    id                                uuid PRIMARY KEY NOT NULL,
    combo_id                          uuid,
    name                              text NOT NULL,
    min_select                        integer,
    max_select                        integer,
    sort_order                        integer
);

-- What was done about a finding and who signed it. The signature is the record — *discarded and
-- reset* with nobody against it is not a corrective action
CREATE TABLE IF NOT EXISTS fnb.corrective_action (
    id                                uuid PRIMARY KEY NOT NULL,
    raised_at                         timestamptz NOT NULL,
    source                            text NOT NULL,
    source_ref                        uuid,
    severity                          text,
    action_taken                      text,
    disposal                          text,
    status                            text NOT NULL,
    signed_by_principal_id            uuid,
    signed_at                         timestamptz,
    escalated_to_principal_id         uuid,
    scope_path                        text
);

-- Where food goes that is not a table — a lounger, a cabana, a suite, a stand. Served by outlets
-- through a join, because one kitchen serves several
CREATE TABLE IF NOT EXISTS fnb.delivery_location (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL,
    label                             text NOT NULL,
    zone                              text,
    table_id                          uuid,
    seat_id                           text,
    serving_outlet_ids                text[],
    is_serviceable                    boolean NOT NULL,
    unserviceable_reason              text,
    walk_time_minutes                 integer
);

-- join table. Which outlets serve which locations Hangs off: a child of fnb.delivery_location;
-- reaches fnb.service_order through its keys; references fnb.delivery_location, platform.outlet.
CREATE TABLE IF NOT EXISTS fnb.delivery_location_outlet (
    id                                uuid PRIMARY KEY NOT NULL,
    location_id                       uuid,
    outlet_id                         uuid
);

-- A physical table with a capacity and a position. What may combine with what is declared rather
-- than inferred — a pillar or a service run means two adjacent tables sometimes cannot
CREATE TABLE IF NOT EXISTS fnb.dining_table (
    id                                uuid PRIMARY KEY NOT NULL,
    label                             text NOT NULL,
    capacity                          integer NOT NULL,
    zone                              text,
    position                          jsonb,
    shape                             text,
    outlet_id                         uuid
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.ingredient_substitute (
    id                                uuid PRIMARY KEY,
    from_inventory_item_id            uuid NOT NULL,
    to_inventory_item_id              uuid NOT NULL,
    substitution_ratio                numeric(18,4) NOT NULL,
    conditions_json                   text,
    allergens_added_json              text,
    allergens_removed_json            text,
    requires_approval                 boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Something that cost the kitchen a service and left no other trace — equipment down, an item run
-- out, a late delivery (client board 3, 24 August). The reasons are the value: a venue looking at
-- a bad Saturday needs to know the fryer was down for forty minutes
CREATE TABLE IF NOT EXISTS fnb.kitchen_exception (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid,
    station_id                        uuid,
    ticket_id                         uuid,
    kind                              text NOT NULL,
    duration_minutes                  integer,
    raised_at                         timestamptz NOT NULL,
    raised_by_principal_id            uuid,
    note                              text
);

-- Where a ticket is routed — grill, cold, bar, pass
CREATE TABLE IF NOT EXISTS fnb.kitchen_station (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    outlet_id                         uuid,
    menu_item_ids                     text[],
    display_endpoint                  text,
    is_active                         boolean
);

-- What the pass sees. One order can produce several, routed by station, and the clock on it is the
-- kitchen’s rather than the counter’s
CREATE TABLE IF NOT EXISTS fnb.kitchen_ticket (
    id                                text PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    order_number                      text,
    outlet_id                         uuid NOT NULL,
    table_label                       text,
    service_mode                      text,
    coursing                          text,
    buzzer_code                       text,
    status                            text NOT NULL,
    priority                          integer,
    prioritised_by_principal_id       uuid,
    prioritise_reason                 text,
    created_at                        timestamptz NOT NULL,
    target_ready_at                   timestamptz,
    elapsed_seconds                   integer
);

-- One item the kitchen is making, bumped independently
CREATE TABLE IF NOT EXISTS fnb.kitchen_ticket_line (
    kitchen_ticket_id                 text NOT NULL,
    line_id                           text NOT NULL,
    name                              text NOT NULL,
    quantity                          integer NOT NULL,
    modifiers                         text[],
    note                              text,
    allergens                         text[],
    course                            integer,
    station_id                        uuid,
    status                            text NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Rotating, hashed, time-bounded. Generated by a job, resolved at claim — never directly created
-- or listed Hangs off: reaches fnb.service_order through its keys; references
-- fnb.delivery_location.
CREATE TABLE IF NOT EXISTS fnb.location_code (
    id                                uuid PRIMARY KEY NOT NULL,
    location_id                       uuid
);

-- A guest claim on a delivery location — a lounger, a cabana. The equivalent of a table session
-- away from a table
CREATE TABLE IF NOT EXISTS fnb.location_session (
    id                                text PRIMARY KEY NOT NULL,
    location_id                       uuid NOT NULL,
    kind                              text NOT NULL,
    label                             text NOT NULL,
    outlet_id                         uuid,
    visit_id                          text,
    joined_existing_visit             boolean,
    subject_id                        uuid,
    expires_at                        timestamptz NOT NULL,
    venue_id                          uuid
);

-- What an outlet is offering, versioned and published. Outlet-scoped (CF-138)
CREATE TABLE IF NOT EXISTS fnb.menu (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    outlet_id                         uuid NOT NULL,
    availability                      jsonb,
    is_active                         boolean NOT NULL
);

-- A product seen through a menu. Catalogue owns whether it can be sold; F&B owns what a kitchen
-- needs to make it — station, prep time, allergens, and the 86 flag
CREATE TABLE IF NOT EXISTS fnb.menu_item (
    id                                uuid PRIMARY KEY NOT NULL,
    product_variant_id                uuid NOT NULL,
    name                              text NOT NULL,
    description                       text,
    price                             numeric(18,4) NOT NULL,
    sort_order                        integer,
    modifier_group_ids                text[],
    station_id                        uuid,
    is_stock_tracked                  boolean,
    is_available                      boolean NOT NULL,
    unavailable_reason                text,
    preparation_minutes               integer,
    allergens                         text[]
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.menu_item_modifier (
    item_id                           uuid NOT NULL,
    group_id                          uuid NOT NULL,
    sort_order                        integer NOT NULL,
    is_active                         boolean NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A run of items on a menu, in the order the outlet set. Not alphabetical, or Desserts sits above
-- Mains forever
CREATE TABLE IF NOT EXISTS fnb.menu_section (
    code                              text NOT NULL,
    name                              text NOT NULL,
    sort_order                        integer NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    menu_id                           uuid NOT NULL
);

-- A choice attached to an item — how it is cooked, what is on it. Attached to the item, not chosen
-- per sale (CF-160)
CREATE TABLE IF NOT EXISTS fnb.modifier_group (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    min_selections                    integer NOT NULL,
    max_selections                    integer NOT NULL,
    scope_path                        text
);

-- One choice within a group, with its own price delta
CREATE TABLE IF NOT EXISTS fnb.modifier_option (
    modifier_group_id                 uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    price_delta                       numeric(18,4) NOT NULL,
    is_default                        boolean,
    is_available                      boolean
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.price (
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
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.price_list (
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

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.product (
    id                                uuid PRIMARY KEY,
    scope_path                        text,
    category_id                       uuid NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    type                              text NOT NULL,
    tax_code                          text,
    is_stock_tracked                  boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.product_category (
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
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.product_recommendation (
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

-- A forecast turned into a prep list (board 2M). A plan is not a production run — a plan that
-- creates runs as it is drafted creates runs nobody asked for
CREATE TABLE IF NOT EXISTS fnb.production_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid,
    for_date                          date NOT NULL,
    status                            text NOT NULL,
    based_on_suggestion_id            uuid,
    released_run_ids                  text[]
);

-- A batch made for one outlet or several (BL-129). Production is a stock movement in both
-- directions at once — ingredients out, sellable items in — and theoretical against actual is the
-- whole point of recording it
CREATE TABLE IF NOT EXISTS fnb.production_run (
    id                                uuid PRIMARY KEY NOT NULL,
    recipe_id                         uuid NOT NULL,
    producing_outlet_id               uuid,
    for_outlet_ids                    text[],
    planned_quantity                  numeric(18,4) NOT NULL,
    actual_quantity                   numeric(18,4),
    scheduled_for                     timestamptz,
    status                            text NOT NULL,
    variance_reason                   text
);

-- What an item is made of, which is how a sale becomes a stock movement
CREATE TABLE IF NOT EXISTS fnb.recipe (
    menu_item_id                      uuid NOT NULL,
    yield                             numeric(18,4),
    cost_per_portion                  numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- One component of a recipe, in its own unit
CREATE TABLE IF NOT EXISTS fnb.recipe_ingredient (
    recipe_id                         uuid NOT NULL,
    inventory_item_id                 uuid NOT NULL,
    quantity                          numeric(18,4) NOT NULL,
    unit                              text NOT NULL,
    is_optional                       boolean,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.reservation_table (
    reservation_id                    uuid NOT NULL,
    table_id                          uuid NOT NULL,
    created_at                        timestamptz NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Food and drink ordered, wherever from — a counter, a table, a lounger, the app. The kitchen
-- ticket is what the pass sees; this is what the guest bought
CREATE TABLE IF NOT EXISTS fnb.service_order (
    id                                text PRIMARY KEY NOT NULL,
    order_number                      text NOT NULL,
    outlet_id                         uuid NOT NULL,
    service_mode                      text NOT NULL,
    table_visit_id                    text,
    status                            text NOT NULL,
    lines                             text[] NOT NULL,
    sales_order_id                    uuid,
    updated_at                        timestamptz,
    gross_amount                      numeric(18,4) NOT NULL,
    tax_amount                        numeric(18,4),
    kitchen_ticket_id                 text,
    estimated_ready_at                timestamptz,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz,
    synced_at                         timestamptz
);

-- One item on a food order, with its modifiers resolved at the moment of sale
CREATE TABLE IF NOT EXISTS fnb.service_order_line (
    service_order_id                  text NOT NULL,
    id                                text PRIMARY KEY NOT NULL,
    menu_item_id                      uuid NOT NULL,
    quantity                          integer NOT NULL,
    modifier_option_ids               text[],
    note                              text,
    seat_number                       integer,
    course                            integer,
    status                            text,
    unit_price                        numeric(18,4),
    line_total                        numeric(18,4)
);

-- An item off the menu and back on (board 5J). setItemAvailability kept the flag and not the
-- history — time off, time back, who called it, and what it cost in refused orders
CREATE TABLE IF NOT EXISTS fnb.sold_out_item (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid,
    menu_item_id                      uuid NOT NULL,
    off_at                            timestamptz NOT NULL,
    back_at                           timestamptz,
    reason                            text,
    called_by_principal_id            uuid,
    refused_order_count               integer
);

-- One bill from a split (client board 4, 24 August). Tax and service charge recompute per bill
-- rather than apportioning pro rata — a split that divides VAT by percentage produces bills that
-- do not sum to the original
CREATE TABLE IF NOT EXISTS fnb.sub_bill (
    sub_bill_id                       text NOT NULL,
    bill_split_id                     uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    visit_id                          uuid NOT NULL,
    label                             text,
    line_ids                          text[],
    subtotal                          numeric(18,4),
    tax_amount                        numeric(18,4),
    service_charge                    numeric(18,4),
    total                             numeric(18,4) NOT NULL,
    status                            text
);

-- What may replace what, and under what conditions (board 2L, 24 August). The rule exists so
-- verifyAllergens has something to check against — swapping butter for margarine removes dairy and
-- may add soy
CREATE TABLE IF NOT EXISTS fnb.substitution_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    from_ingredient_id                uuid NOT NULL,
    to_ingredient_id                  uuid NOT NULL,
    ratio                             numeric(18,4),
    allergens_added                   text[],
    allergens_removed                 text[],
    conditions                        text[],
    requires_approval                 boolean,
    is_active                         boolean
);

-- A booking with a time and a party size. Distinct from a table session, which is a guest already
-- sitting down Hangs off: reaches fnb.service_order through its keys; references fnb.table_visit,
-- orders.group_booking, pii.subject. Reached by: 6 operations read it and 4 write it.
CREATE TABLE IF NOT EXISTS fnb.table_reservation (
    id                                uuid PRIMARY KEY,
    outlet_id                         uuid NOT NULL,
    subject_id                        uuid,
    guest_name                        text,
    contact_point                     text,
    party_size                        integer NOT NULL,
    starts_at                         timestamptz NOT NULL,
    duration_minutes                  integer,
    table_ids                         text[],
    status                            text,
    group_id                          uuid,
    notes                             text,
    actual_party_size                 integer,
    table_visit_id                    text,
    created_at                        timestamptz
);

-- A device claim on a table — a QR scanned, an order opened. The hospitality event around it is a
-- table_visit
CREATE TABLE IF NOT EXISTS fnb.table_session (
    id                                text PRIMARY KEY NOT NULL,
    outlet_id                         uuid NOT NULL,
    outlet_name                       text,
    table_id                          uuid NOT NULL,
    table_label                       text NOT NULL,
    visit_id                          text NOT NULL,
    joined_existing_visit             boolean,
    subject_id                        uuid,
    expires_at                        timestamptz NOT NULL
);

-- One party at one table, from seating to settling. Distinct from fnb.table_session, which is the
-- device claim: a QR scanned at the table opens a session, and the visit is the hospitality event
-- around it
CREATE TABLE IF NOT EXISTS fnb.table_visit (
    id                                text PRIMARY KEY NOT NULL,
    table_id                          uuid NOT NULL,
    table_label                       text,
    outlet_id                         uuid NOT NULL,
    covers                            integer NOT NULL,
    status                            text NOT NULL,
    server_principal_id               uuid,
    subject_id                        uuid,
    merged_into_visit_id              text,
    merged_from_visit_ids             text[],
    running_total                     numeric(18,4),
    opened_at                         timestamptz NOT NULL,
    closed_at                         timestamptz
);

-- HACCP temperature checks (client board 5J, 20 August). A regulatory obligation nothing in the
-- package touched. An out-of-range reading is kept, not refused — deleting a bad reading is the
-- one thing an inspector looks for. Hangs off: reaches fnb.service_order through its keys;
-- references fnb.corrective_action, identity.principal, venuemap.point. Reached by: 2 operations
-- read it and 1 write it.
CREATE TABLE IF NOT EXISTS fnb.temperature_log (
    id                                uuid PRIMARY KEY NOT NULL,
    check_point_id                    uuid NOT NULL,
    check_point_kind                  text,
    recorded_at                       timestamptz NOT NULL,
    recorded_by_principal_id          uuid,
    value_celsius                     numeric(18,4) NOT NULL,
    min_celsius                       numeric(18,4),
    max_celsius                       numeric(18,4),
    outcome                           text NOT NULL,
    device_reported                   boolean,
    corrective_action_id              uuid
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.variant (
    id                                uuid PRIMARY KEY,
    product_id                        uuid NOT NULL,
    sku                               text NOT NULL,
    name                              text NOT NULL,
    barcode                           text,
    is_default                        boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- A restaurant waitlist party (BL-130). Distinct from queue, which is for rides — this has a party
-- size, a seating preference and a walk-away point
CREATE TABLE IF NOT EXISTS fnb.waitlist_entry (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid NOT NULL,
    subject_id                        uuid,
    party_size                        integer NOT NULL,
    quoted_wait_minutes               integer,
    seating_preference                text,
    status                            text NOT NULL,
    notified_at                       timestamptz,
    hold_expires_at                   timestamptz
);

