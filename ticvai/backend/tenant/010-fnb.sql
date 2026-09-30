-- fnb — 48 tables
-- **Derived. Do not hand-edit.**

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.allergen_verdict (
    menu_item_id                      uuid NOT NULL,
    matches                           boolean NOT NULL,
    declared                          text[],
    actual                            text[],
    over_declared                     text[],
    checked_at                        timestamptz NOT NULL,
    trigger                           text NOT NULL CONSTRAINT allergen_verdict_trigger_chk CHECK (trigger IN ('manual', 'recipeChanged', 'substitutionChanged', 'modifierChanged')),
    id                                uuid PRIMARY KEY NOT NULL
);

-- How one table’s bill was divided. A party of six paying separately is the ordinary case
CREATE TABLE IF NOT EXISTS fnb.bill_split (
    id                                uuid PRIMARY KEY,
    visit_id                          uuid NOT NULL,
    method                            text NOT NULL CONSTRAINT bill_split_method_chk CHECK (method IN ('byAmount', 'byCovers', 'byCategory', 'byLine', 'bySeat'))
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
    decision                          text NOT NULL CONSTRAINT cold_chain_event_decision_chk CHECK (decision IN ('accepted', 'acceptedWithNote', 'partiallyRejected', 'rejected')),
    corrective_action_id              uuid,
    is_supplier_claim_raised          boolean DEFAULT false
);

-- A meal deal, priced as one thing (client board 2G). A combo is one product with slots, not a
-- bundle of products — a model that prices by summing cannot express a deal
CREATE TABLE IF NOT EXISTS fnb.combo (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid,
    name                              text NOT NULL,
    name_localised                    jsonb,
    list_price                        numeric(18,4) NOT NULL,
    availability                      jsonb,
    is_active                         boolean DEFAULT true
);

-- One choice within a combo. minSelect and maxSelect are what make it a slot rather than a line —
-- a main is exactly one, a sauce might be none or two
CREATE TABLE IF NOT EXISTS fnb.combo_slot (
    id                                uuid PRIMARY KEY NOT NULL,
    combo_id                          uuid,
    name                              text NOT NULL,
    min_select                        integer DEFAULT 1,
    max_select                        integer DEFAULT 1,
    sort_order                        integer DEFAULT 100
);

-- What was done about a finding and who signed it. The signature is the record — *discarded and
-- reset* with nobody against it is not a corrective action
CREATE TABLE IF NOT EXISTS fnb.corrective_action (
    id                                uuid PRIMARY KEY NOT NULL,
    raised_at                         timestamptz NOT NULL,
    raised_by_principal_id            uuid,
    source                            text NOT NULL CONSTRAINT corrective_action_source_chk CHECK (source IN ('temperatureExcursion', 'coldChainBreach', 'expiredStock', 'contamination', 'pestSighting', 'equipmentFailure', 'missedCheck', 'manual')),
    source_ref                        uuid,
    severity                          text CONSTRAINT corrective_action_severity_chk CHECK (severity IN ('observation', 'minor', 'major', 'critical')),
    action_taken                      text,
    disposal                          text CONSTRAINT corrective_action_disposal_chk CHECK (disposal IN ('none', 'discarded', 'reworked', 'quarantined', 'returned')),
    status                            text NOT NULL CONSTRAINT corrective_action_status_chk CHECK (status IN ('open', 'actioned', 'signed', 'escalated', 'closed')),
    signed_by_principal_id            uuid,
    signed_at                         timestamptz,
    escalated_to_principal_id         uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.course_rule (
    outlet_id                         uuid,
    default_coursing                  text CONSTRAINT course_rule_default_coursing_chk CHECK (default_coursing IN ('fireAndForget', 'holdAndFire', 'phased', 'timed', 'delayed')),
    course_names                      text[],
    auto_fire_minutes                 integer,
    service_mode_overrides            jsonb,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Where food goes that is not a table — a lounger, a cabana, a suite, a stand. Served by outlets
-- through a join, because one kitchen serves several
CREATE TABLE IF NOT EXISTS fnb.delivery_location (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT delivery_location_kind_chk CHECK (kind IN ('table', 'seat', 'cabana', 'sunbed', 'poolside', 'box', 'suite', 'lawn', 'collectionPoint', 'namedLocation')),
    label                             text NOT NULL,
    zone                              text,
    table_id                          uuid,
    seat_id                           uuid,
    serving_outlet_ids                text[],
    is_serviceable                    boolean NOT NULL,
    unserviceable_reason              text,
    walk_time_minutes                 integer
);

-- join table. Which outlets serve which locations Hangs off: a child of fnb.delivery_location;
-- reaches fnb.service_order through its keys; references fnb.delivery_location, platform.outlet.
-- Reached by: 2 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS fnb.delivery_location_outlet (
    id                                uuid PRIMARY KEY NOT NULL,
    location_id                       uuid,
    outlet_id                         uuid
);

-- An outlet's takeaway and delivery rules: minimum order, fee, free-above threshold, radius, slot
-- length. Enforced at order time rather than only shown, which is what the design did
CREATE TABLE IF NOT EXISTS fnb.delivery_policy (
    id                                uuid PRIMARY KEY,
    outlet_id                         uuid NOT NULL,
    is_collection_enabled             boolean DEFAULT true,
    is_delivery_enabled               boolean DEFAULT false,
    collection_point                  text CONSTRAINT delivery_policy_collection_point_chk CHECK (char_length(collection_point) <= 200),
    collection_hold_minutes           integer DEFAULT 20,
    asap_collection_minutes           integer DEFAULT 25,
    asap_delivery_minutes             integer DEFAULT 45,
    slot_minutes                      integer DEFAULT 30,
    minimum_order                     numeric(18,4),
    delivery_fee                      numeric(18,4),
    free_delivery_above               numeric(18,4),
    radius_km                         numeric(18,4),
    emirates_served                   text[],
    cutlery_opt_in                    boolean DEFAULT true,
    scope_path                        ltree NOT NULL
);

-- A physical table with a capacity and a position. What may combine with what is declared rather
-- than inferred — a pillar or a service run means two adjacent tables sometimes cannot
CREATE TABLE IF NOT EXISTS fnb.dining_table (
    id                                uuid PRIMARY KEY NOT NULL,
    label                             text NOT NULL CONSTRAINT dining_table_label_chk CHECK (char_length(label) <= 32),
    capacity                          integer NOT NULL,
    zone                              text,
    position                          jsonb,
    shape                             text CONSTRAINT dining_table_shape_chk CHECK (shape IN ('round', 'square', 'rectangle', 'booth', 'bar')),
    is_out_of_service                 boolean DEFAULT false,
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
    kind                              text NOT NULL CONSTRAINT kitchen_exception_kind_chk CHECK (kind IN ('equipmentDown', 'itemRanOut', 'lateDelivery', 'staffShort', 'powerLoss', 'spillage', 'chased', 'other')),
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
    display_workstation_ids           text[],
    display_endpoint                  text,
    is_active                         boolean
);

-- What the pass sees. One order can produce several, routed by station, and the clock on it is the
-- kitchen’s rather than the counter’s
CREATE TABLE IF NOT EXISTS fnb.kitchen_ticket (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
    order_number                      text,
    outlet_id                         uuid NOT NULL,
    table_label                       text,
    service_mode                      text CONSTRAINT kitchen_ticket_service_mode_chk CHECK (service_mode IN ('quickService', 'tableService', 'roomService', 'collection', 'delivery')),
    coursing                          text,
    buzzer_code                       text,
    status                            text NOT NULL CONSTRAINT kitchen_ticket_status_chk CHECK (status IN ('received', 'preparing', 'ready', 'served', 'recalled', 'cancelled')),
    priority                          integer,
    prioritised_by_principal_id       uuid,
    prioritise_reason                 text,
    created_at                        timestamptz NOT NULL,
    target_ready_at                   timestamptz,
    elapsed_seconds                   integer
);

-- One item the kitchen is making, bumped independently
CREATE TABLE IF NOT EXISTS fnb.kitchen_ticket_line (
    kitchen_ticket_id                 uuid NOT NULL,
    line_id                           uuid NOT NULL,
    name                              text NOT NULL,
    quantity                          integer NOT NULL,
    modifiers                         text[],
    note                              text,
    allergens                         text[],
    refire_of_line_id                 uuid,
    refire_reason                     text,
    is_chargeable                     boolean,
    course                            integer,
    station_id                        uuid,
    status                            text NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A guest claim on a delivery location — a lounger, a cabana. The equivalent of a table session
-- away from a table
CREATE TABLE IF NOT EXISTS fnb.location_session (
    id                                uuid PRIMARY KEY NOT NULL,
    location_id                       uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT location_session_kind_chk CHECK (kind IN ('table', 'seat', 'cabana', 'sunbed', 'poolside', 'box', 'suite', 'lawn', 'collectionPoint', 'namedLocation')),
    label                             text NOT NULL,
    outlet_id                         uuid,
    visit_id                          uuid,
    joined_existing_visit             boolean,
    subject_id                        uuid,
    expires_at                        timestamptz NOT NULL,
    venue_id                          uuid
);

-- What an outlet is offering, versioned and published. Outlet-scoped (CF-138)
CREATE TABLE IF NOT EXISTS fnb.menu (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT menu_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT menu_name_chk CHECK (char_length(name) <= 200),
    outlet_id                         uuid NOT NULL,
    availability                      jsonb,
    is_active                         boolean NOT NULL,
    published_version                 integer,
    published_at                      timestamptz
);

-- A product seen through a menu. Catalogue owns whether it can be sold; F&B owns what a kitchen
-- needs to make it — station, prep time, allergens, and the 86 flag
CREATE TABLE IF NOT EXISTS fnb.menu_item (
    id                                uuid PRIMARY KEY NOT NULL,
    product_variant_id                uuid NOT NULL,
    name                              text NOT NULL,
    description                       text,
    list_price                        numeric(18,4) NOT NULL,
    sort_order                        integer,
    modifier_group_ids                text[],
    station_id                        uuid,
    menu_section_id                   uuid,
    is_stock_tracked                  boolean,
    is_available                      boolean NOT NULL,
    unavailable_reason                text,
    restore_at                        timestamptz,
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

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.menu_schedule (
    id                                uuid PRIMARY KEY NOT NULL,
    menu_id                           uuid NOT NULL,
    effective_at                      timestamptz NOT NULL,
    status                            text NOT NULL CONSTRAINT menu_schedule_status_chk CHECK (status IN ('pending', 'applied', 'cancelled')),
    published_version                 integer,
    created_at                        timestamptz,
    created_by_principal_id           uuid,
    cancelled_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- A run of items on a menu, in the order the outlet set. Not alphabetical, or Desserts sits above
-- Mains forever
CREATE TABLE IF NOT EXISTS fnb.menu_section (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    sort_order                        integer NOT NULL,
    menu_id                           uuid NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.menu_version (
    id                                uuid PRIMARY KEY NOT NULL,
    menu_id                           uuid NOT NULL,
    version                           integer NOT NULL,
    status                            text NOT NULL CONSTRAINT menu_version_status_chk CHECK (status IN ('draft', 'scheduled', 'live', 'superseded')),
    effective_at                      timestamptz,
    published_at                      timestamptz,
    published_by_principal_id         uuid,
    restored_from_version             integer,
    channels                          text[],
    note                              text,
    availability                      jsonb,
    scope_path                        ltree NOT NULL
);

-- A choice attached to an item — how it is cooked, what is on it. Attached to the item, not chosen
-- per sale (CF-160)
CREATE TABLE IF NOT EXISTS fnb.modifier_group (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    min_selections                    integer NOT NULL,
    max_selections                    integer NOT NULL,
    scope_path                        ltree NOT NULL
);

-- One choice within a group, with its own price delta
CREATE TABLE IF NOT EXISTS fnb.modifier_option (
    modifier_group_id                 uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    price_delta                       numeric(18,4) NOT NULL,
    is_default                        boolean,
    is_available                      boolean,
    allergens                         text[]
);

-- How a guest's order leaves the kitchen: collected at a time, delivered to an address in a
-- window, or taken to a place in the venue. The address is here and nowhere else
CREATE TABLE IF NOT EXISTS fnb.order_fulfilment (
    id                                uuid PRIMARY KEY,
    service_order_id                  uuid,
    mode                              text NOT NULL CONSTRAINT order_fulfilment_mode_chk CHECK (mode IN ('collection', 'delivery', 'inVenue')),
    collection_at                     timestamptz,
    window_start                      timestamptz,
    window_end                        timestamptz,
    delivery_address                  jsonb,
    delivery_fee                      numeric(18,4),
    is_cutlery                        boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.outlet_template (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT outlet_template_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT outlet_template_name_chk CHECK (char_length(name) <= 200),
    outlet_type                       text NOT NULL CONSTRAINT outlet_template_outlet_type_chk CHECK (outlet_type IN ('restaurant', 'bar', 'cafe', 'kiosk', 'mobile')),
    service_model                     text[] NOT NULL,
    default_menu_ids                  text[],
    course_rules                      jsonb,
    kitchen_sla_minutes               integer,
    delivery_policy_id                uuid,
    is_active                         boolean,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.product_recommendation (
    id                                uuid PRIMARY KEY,
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

-- A forecast turned into a prep list (board 2M). A plan is not a production run — a plan that
-- creates runs as it is drafted creates runs nobody asked for
CREATE TABLE IF NOT EXISTS fnb.production_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid,
    for_date                          date NOT NULL,
    status                            text NOT NULL CONSTRAINT production_plan_status_chk CHECK (status IN ('draft', 'released', 'superseded', 'cancelled')),
    based_on_suggestion_id            uuid,
    released_run_ids                  text[]
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.production_plan_line (
    production_plan_id                uuid NOT NULL,
    item_id                           uuid NOT NULL,
    suggested_quantity                numeric(18,4),
    planned_quantity                  numeric(18,4) NOT NULL,
    uom                               text,
    station_id                        uuid,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A batch made for one outlet or several (BL-129). Production is a stock movement in both
-- directions at once — ingredients out, sellable items in — and theoretical against actual is the
-- whole point of recording it
CREATE TABLE IF NOT EXISTS fnb.production_run (
    id                                uuid PRIMARY KEY NOT NULL,
    recipe_id                         uuid NOT NULL,
    production_plan_id                uuid,
    station_id                        uuid,
    producing_outlet_id               uuid,
    for_outlet_ids                    text[],
    planned_quantity                  numeric(18,4) NOT NULL,
    actual_quantity                   numeric(18,4),
    scheduled_for                     timestamptz,
    status                            text NOT NULL CONSTRAINT production_run_status_chk CHECK (status IN ('planned', 'inProgress', 'completed', 'cancelled')),
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

-- How long a table is held, by party size, and what sits between seatings.
-- fnb.table_reservation.duration_minutes was set per booking with no default behind it, and a turn
-- time is the single most tuned number in a restaurant — a two-top and a table of eight do not
-- turn at the same speed. The booking keeps its own duration as the snapshot, so a turn time
-- revised in March cannot shorten a reservation
CREATE TABLE IF NOT EXISTS fnb.reservation_policy (
    id                                uuid PRIMARY KEY,
    outlet_id                         uuid,
    default_turn_minutes              integer NOT NULL,
    seating_buffer_minutes            integer DEFAULT 0,
    maximum_duration_minutes          integer,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.reservation_table (
    reservation_id                    uuid NOT NULL,
    table_id                          uuid NOT NULL,
    created_at                        timestamptz NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What the service charge on a bill is, and on what. fnb.sub_bill.service_charge was stored with
-- nothing anywhere holding the rate, and F29 recomputes it per bill on a split — so a number was
-- applied twice over a visit from a value that existed only in somebody's head. is_discretionary
-- is the field a regulator reads first: a charge a guest cannot decline is a price, and a price
-- belongs in the displa
CREATE TABLE IF NOT EXISTS fnb.service_charge_policy (
    id                                uuid PRIMARY KEY,
    basis                             text NOT NULL CONSTRAINT service_charge_policy_basis_chk CHECK (basis IN ('none', 'percentOfSubtotal', 'fixedPerCover', 'fixedPerBill')),
    rate_percent                      numeric(18,4),
    amount                            numeric(18,4),
    minimum_party_size                integer,
    service_types                     text[],
    is_taxable                        boolean NOT NULL,
    included_in_display_price         boolean,
    shown_separately                  boolean,
    is_discretionary                  boolean NOT NULL,
    distribution                      text NOT NULL CONSTRAINT service_charge_policy_distribution_chk CHECK (distribution IN ('venueRevenue', 'staffPool', 'split')),
    staff_pool_percent                numeric(18,4),
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Food and drink ordered, wherever from — a counter, a table, a lounger, the app. The kitchen
-- ticket is what the pass sees; this is what the guest bought
CREATE TABLE IF NOT EXISTS fnb.service_order (
    id                                uuid PRIMARY KEY NOT NULL,
    order_number                      text NOT NULL,
    outlet_id                         uuid NOT NULL,
    service_mode                      text NOT NULL CONSTRAINT service_order_service_mode_chk CHECK (service_mode IN ('quickService', 'tableService', 'roomService', 'collection', 'delivery')),
    table_visit_id                    uuid,
    status                            text NOT NULL CONSTRAINT service_order_status_chk CHECK (status IN ('ordered', 'accepted', 'inPreparation', 'ready', 'served', 'collected', 'delivered', 'cancelled', 'refunded')),
    sales_order_id                    uuid,
    updated_at                        timestamptz,
    gross_amount                      numeric(18,4) NOT NULL,
    tax_amount                        numeric(18,4),
    kitchen_ticket_id                 uuid,
    estimated_ready_at                timestamptz,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz,
    synced_at                         timestamptz
);

-- One item on a food order, with its modifiers resolved at the moment of sale
CREATE TABLE IF NOT EXISTS fnb.service_order_line (
    service_order_id                  uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    menu_item_id                      uuid NOT NULL,
    quantity                          integer NOT NULL,
    modifier_option_ids               text[],
    note                              text,
    seat_number                       integer,
    course                            integer,
    redeem_entitlement_id             uuid,
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
    reason                            text CONSTRAINT sold_out_item_reason_chk CHECK (reason IN ('ranOut', 'qualityIssue', 'equipmentDown', 'supplierFailure', 'seasonal', 'other')),
    note                              text CONSTRAINT sold_out_item_note_chk CHECK (char_length(note) <= 500),
    called_by_principal_id            uuid,
    refused_order_count               integer DEFAULT 0
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
    net_amount                        numeric(18,4),
    tax_amount                        numeric(18,4),
    service_charge                    numeric(18,4),
    gross_amount                      numeric(18,4) NOT NULL,
    status                            text CONSTRAINT sub_bill_status_chk CHECK (status IN ('open', 'paid', 'voided'))
);

-- What may replace what, and under what conditions (board 2L, 24 August). The rule exists so
-- verifyAllergens has something to check against — swapping butter for margarine removes dairy and
-- may add soy
CREATE TABLE IF NOT EXISTS fnb.substitution_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    recipe_id                         uuid NOT NULL,
    from_ingredient_id                uuid NOT NULL,
    to_ingredient_id                  uuid NOT NULL,
    ratio                             numeric(18,4) DEFAULT 1,
    allergens_added                   text[],
    allergens_removed                 text[],
    conditions                        text[],
    requires_approval                 boolean DEFAULT false,
    is_active                         boolean DEFAULT true
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS fnb.table_combination (
    id                                uuid PRIMARY KEY,
    outlet_id                         uuid,
    table_ids                         text[] NOT NULL,
    combined_covers                   integer NOT NULL,
    setup_minutes                     integer DEFAULT 5,
    scope_path                        ltree NOT NULL
);

-- A booking with a time and a party size. Distinct from a table session, which is a guest already
-- sitting down Hangs off: reaches fnb.service_order through its keys; references
-- catalogue.variant, fnb.modifier_group, fnb.table_visit. Reached by: 6 operations read it and 4
-- write it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS fnb.table_reservation (
    id                                uuid PRIMARY KEY,
    outlet_id                         uuid NOT NULL,
    subject_id                        uuid,
    guest_name                        text,
    contact_point                     text,
    party_size                        integer NOT NULL,
    starts_at                         timestamptz NOT NULL,
    duration_minutes                  integer,
    status                            text CONSTRAINT table_reservation_status_chk CHECK (status IN ('awaitingDeposit', 'booked', 'confirmed', 'seated', 'completed', 'cancelled', 'noShow')),
    group_id                          uuid,
    notes                             text,
    actual_party_size                 integer,
    table_visit_id                    uuid,
    created_at                        timestamptz,
    amount                            numeric(18,4) NOT NULL,
    basis                             text NOT NULL CONSTRAINT table_reservation_basis_chk CHECK (basis IN ('fixedPerGuest', 'fixedPerTable', 'percentOfMinimumSpend')),
    hold_expires_at                   timestamptz,
    refundable_until                  timestamptz,
    variant_id                        uuid,
    cart_line_id                      uuid,
    deposit_id                        uuid
);

-- A device claim on a table — a QR scanned, an order opened. The hospitality event around it is a
-- table_visit
CREATE TABLE IF NOT EXISTS fnb.table_session (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid NOT NULL,
    outlet_name                       text,
    table_id                          uuid NOT NULL,
    table_label                       text NOT NULL,
    visit_id                          uuid NOT NULL,
    joined_existing_visit             boolean,
    subject_id                        uuid,
    expires_at                        timestamptz NOT NULL
);

-- One party at one table, from seating to settling. Distinct from fnb.table_session, which is the
-- device claim: a QR scanned at the table opens a session, and the visit is the hospitality event
-- around it
CREATE TABLE IF NOT EXISTS fnb.table_visit (
    id                                uuid PRIMARY KEY NOT NULL,
    table_id                          uuid NOT NULL,
    table_label                       text,
    outlet_id                         uuid NOT NULL,
    covers                            integer NOT NULL,
    status                            text NOT NULL CONSTRAINT table_visit_status_chk CHECK (status IN ('open', 'billRequested', 'settled', 'merged', 'cancelled')),
    server_principal_id               uuid,
    subject_id                        uuid,
    merged_into_visit_id              uuid,
    merged_from_visit_ids             text[],
    running_total                     numeric(18,4),
    gratuity                          numeric(18,4),
    opened_at                         timestamptz NOT NULL,
    closed_at                         timestamptz
);

-- A unit that gets read, and the range it must hold. fnb.temperature_log.check_point_id was NOT
-- NULL and referenced no table in the package — every HACCP reading was obliged to name a
-- definition nothing modelled, and the safe range was written onto each reading with no source.
-- TemperatureLog calls HACCP records a UAE regulatory obligation that is inspected, and an
-- inspector asking what range a freez
CREATE TABLE IF NOT EXISTS fnb.temperature_checkpoint (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid,
    kind                              text NOT NULL CONSTRAINT temperature_checkpoint_kind_chk CHECK (kind IN ('fridge', 'freezer', 'holdingCabinet', 'blastChiller', 'coreProbe', 'delivery', 'displayCounter', 'ambient')),
    label                             text NOT NULL,
    min_celsius                       numeric(18,4),
    max_celsius                       numeric(18,4),
    check_frequency_minutes           integer,
    requires_corrective_action_on_breach boolean,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL
);

-- HACCP temperature checks (client board 5J, 20 August). A regulatory obligation nothing in the
-- package touched. An out-of-range reading is kept, not refused — deleting a bad reading is the
-- one thing an inspector looks for. Hangs off: reaches fnb.service_order through its keys;
-- references fnb.corrective_action, identity.principal. Reached by: 2 operations read it and 1
-- write it.
CREATE TABLE IF NOT EXISTS fnb.temperature_log (
    id                                uuid PRIMARY KEY NOT NULL,
    check_point_id                    uuid NOT NULL,
    check_point_kind                  text CONSTRAINT temperature_log_check_point_kind_chk CHECK (check_point_kind IN ('fridge', 'freezer', 'holdingCabinet', 'blastChiller', 'coreProbe', 'delivery', 'displayCounter', 'ambient')),
    recorded_at                       timestamptz NOT NULL,
    recorded_by_principal_id          uuid,
    value_celsius                     numeric(18,4) NOT NULL,
    min_celsius                       numeric(18,4),
    max_celsius                       numeric(18,4),
    outcome                           text NOT NULL CONSTRAINT temperature_log_outcome_chk CHECK (outcome IN ('inRange', 'outOfRange', 'notTaken')),
    is_device_reported                boolean DEFAULT false,
    corrective_action_id              uuid
);

-- A restaurant waitlist party (BL-130). Distinct from queue, which is for rides — this has a party
-- size, a seating preference and a walk-away point
CREATE TABLE IF NOT EXISTS fnb.waitlist_entry (
    id                                uuid PRIMARY KEY NOT NULL,
    outlet_id                         uuid NOT NULL,
    subject_id                        uuid,
    party_size                        integer NOT NULL,
    quoted_wait_minutes               integer,
    seating_preference                text CONSTRAINT waitlist_entry_seating_preference_chk CHECK (seating_preference IN ('any', 'indoor', 'outdoor', 'bar', 'booth', 'highChair')),
    status                            text NOT NULL CONSTRAINT waitlist_entry_status_chk CHECK (status IN ('waiting', 'notified', 'seated', 'walkedAway', 'noShow', 'cancelled')),
    notified_at                       timestamptz,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz,
    hold_expires_at                   timestamptz
);

