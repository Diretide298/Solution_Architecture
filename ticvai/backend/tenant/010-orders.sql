-- orders — 34 tables
-- **Derived. Do not hand-edit.**

-- A partner’s credit line, drawn against and settled periodically
CREATE TABLE IF NOT EXISTS orders.b2b_credit (
    id                                uuid PRIMARY KEY,
    account_id                        uuid NOT NULL,
    account_name                      text,
    credit_limit                      numeric(18,4) NOT NULL,
    used                              numeric(18,4) NOT NULL,
    available                         numeric(18,4) NOT NULL,
    is_over_limit                     boolean,
    is_suspended                      boolean NOT NULL,
    payment_terms_days                integer,
    oldest_unpaid_invoice_at          timestamptz,
    days_overdue                      integer,
    scope_path                        text
);

-- A cart holds leases; an order holds money. Retained after expiry so a recovery link lands on
-- something Hangs off: reaches orders.sales_order through its keys; references pii.subject,
-- platform.scope. Reached by: 9 operations read it and 6 write it; 2 tables reference it.
CREATE TABLE IF NOT EXISTS orders.cart (
    id                                uuid PRIMARY KEY NOT NULL,
    token                             text,
    venue_id                          uuid NOT NULL,
    channel                           text NOT NULL,
    subject_id                        uuid,
    status                            text NOT NULL,
    subtotal                          numeric(18,4),
    discount_total                    numeric(18,4),
    tax_total                         numeric(18,4),
    total                             numeric(18,4),
    applied_promotion_ids             text[],
    expires_at                        timestamptz,
    extensions_used                   integer,
    max_extensions                    integer,
    locale                            text,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- One line, with the lease that holds its capacity. Null lease for a product with no capacity
-- Hangs off: a child of orders.cart; reaches orders.sales_order through its keys; references
-- catalogue.inventory_hold, catalogue.performance, catalogue.variant. Reached by: 5 operations
-- read it and 4 write it.
CREATE TABLE IF NOT EXISTS orders.cart_line (
    id                                uuid PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    product_name                      text,
    quantity                          integer NOT NULL,
    performance_id                    uuid,
    seat_ids                          text[],
    override_price                    numeric(18,4),
    override_reason                   text,
    fee_kind                          text,
    unit_price                        numeric(18,4),
    line_total                        numeric(18,4),
    inventory_hold_id                 uuid,
    lease_expires_at                  timestamptz,
    is_available                      boolean,
    cart_id                           uuid NOT NULL,
    lease_id                          text NOT NULL
);

-- a denomination and a count from a blind till count Hangs off: reaches orders.sales_order through
-- its keys; references orders.deposit_box, orders.pos_shift, platform.denomination. Reached by: 5
-- operations read it and 3 write it.
CREATE TABLE IF NOT EXISTS orders.cash_count_line (
    id                                uuid PRIMARY KEY,
    shift_id                          text NOT NULL,
    deposit_box_id                    uuid,
    denomination_id                   uuid NOT NULL,
    counted_quantity                  integer NOT NULL,
    counted_value                     numeric(18,4),
    counted_by                        uuid,
    counted_at                        timestamptz,
    recount_of                        uuid
);

-- Cash in or out of a drawer — a float, a pickup, a drop, a payout. Denominated, and the audit
-- trail behind a shift variance
CREATE TABLE IF NOT EXISTS orders.cash_movement (
    id                                text PRIMARY KEY,
    kind                              text,
    amount                            numeric(18,4),
    denominations                     jsonb,
    reference                         text,
    reason                            text,
    recorded_at                       timestamptz,
    shift_id                          text,
    authorised_by_principal_id        uuid,
    sequence                          integer,
    synced_at                         timestamptz
);

-- A disputed transaction (BL-118, CF-144). Not a refund — a bank decides, on a clock the venue
-- does not control, and a deadline missed is a case lost regardless of merit
CREATE TABLE IF NOT EXISTS orders.chargeback (
    id                                uuid PRIMARY KEY NOT NULL,
    payment_id                        text NOT NULL,
    provider_id                       uuid,
    provider_case_reference           text,
    amount                            numeric(18,4) NOT NULL,
    fee_amount                        numeric(18,4),
    reason                            text NOT NULL,
    status                            text NOT NULL,
    evidence_due_by                   timestamptz NOT NULL,
    evidence_submitted_at             timestamptz,
    outcome_at                        timestamptz
);

-- a manual override of a partner credit limit, recorded with who and why. Second table on a marker
-- the deriver only read the first half of Hangs off: a child of orders.b2b_credit; reaches
-- orders.sales_order through its keys; references identity.principal, orders.b2b_credit,
-- orders.sales_order. Reached by: 1 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS orders.credit_override (
    b2b_credit_id                     uuid NOT NULL,
    order_id                          text,
    amount                            numeric(18,4),
    authorised_by_principal_id        uuid,
    reason                            text,
    expires_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.deposit (
    id                                uuid PRIMARY KEY,
    order_id                          text NOT NULL,
    customer_id                       uuid,
    rental_agreement_id               uuid,
    currency_code                     text NOT NULL,
    required_amount                   numeric(18,4) NOT NULL,
    authorized_amount                 numeric(18,4) NOT NULL,
    captured_amount                   numeric(18,4) NOT NULL,
    released_amount                   numeric(18,4) NOT NULL,
    forfeited_amount                  numeric(18,4) NOT NULL,
    status                            text NOT NULL,
    settled_at                        timestamptz,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- A cashier’s cash box. Allocated to a person, not a workstation — a cashier moving between tills
-- takes their float, which is what makes a variance attributable. withdrawnTotal reduces the
-- expected close: cash skimmed for banking is not a shortfall Hangs off: reaches
-- orders.sales_order through its keys; references identity.principal, orders.pos_shift,
-- platform.scope. Reached by: 4 operations read it
CREATE TABLE IF NOT EXISTS orders.deposit_box (
    id                                uuid PRIMARY KEY,
    cashier_principal_id              uuid NOT NULL,
    cashier_name                      text,
    venue_id                          uuid NOT NULL,
    workstation_id                    uuid,
    shift_id                          text,
    status                            text,
    opening_float                     numeric(18,4) NOT NULL,
    withdrawn_total                   numeric(18,4),
    expected_total                    numeric(18,4),
    counted_total                     numeric(18,4),
    variance                          numeric(18,4),
    closed_by_principal_id            uuid,
    allocated_at                      timestamptz,
    closed_at                         timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.discount (
    id                                uuid PRIMARY KEY,
    order_id                          text NOT NULL,
    promotion_id                      uuid,
    coupon_code                       text,
    type                              text NOT NULL,
    value                             numeric(18,4),
    applied_amount                    numeric(18,4) NOT NULL,
    reason                            text,
    created_at                        timestamptz NOT NULL
);

-- A donation within a transaction. A line, not a flag, because one transaction may give to several
-- campaigns Hangs off: reaches orders.sales_order through its keys; references
-- catalogue.donation_campaign, orders.sales_order.
CREATE TABLE IF NOT EXISTS orders.donation_line (
    id                                uuid PRIMARY KEY NOT NULL,
    campaign_id                       uuid NOT NULL,
    order_id                          text NOT NULL
);

-- Evaluated before the charge (BL-118). It holds rather than refuses — a rule that declines
-- outright turns a false positive into a lost sale with an angry guest
CREATE TABLE IF NOT EXISTS orders.fraud_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    condition                         jsonb NOT NULL,
    action                            text NOT NULL,
    risk_weight                       integer,
    is_active                         boolean NOT NULL,
    scope_path                        text
);

-- A group with a leader and an attendee manifest (BL-028). A school booking forty places has one
-- person who pays and forty who need names collecting, and a generic order has one guest
CREATE TABLE IF NOT EXISTS orders.group_booking (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    leader_subject_id                 uuid NOT NULL,
    organisation_name                 text,
    expected_size                     integer NOT NULL,
    confirmed_size                    integer,
    minimum_size                      integer,
    attendee_capture_required         boolean,
    attendee_capture_due_by           timestamptz,
    status                            text NOT NULL
);

-- A complimentary entitlement issued outside the order path (8.1.3–8.1.5). No payment is expected,
-- so nothing waits for one. Hangs off: reaches orders.sales_order through its keys; references
-- catalogue.performance, catalogue.product, identity.principal. Reached by: 0 operations read it
-- and 1 write it.
CREATE TABLE IF NOT EXISTS orders.invitation (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    performance_id                    uuid,
    quantity                          integer NOT NULL,
    reason                            text NOT NULL,
    offered_by_principal_id           uuid NOT NULL,
    issued_by_principal_id            uuid,
    recipient_name                    text,
    recipient_email                   text,
    cost_center_id                    uuid,
    entitlement_ids                   text[],
    issued_at                         timestamptz NOT NULL
);

-- What a profile may give away and over what period (8.1.5). An unbounded comp right is how a
-- venue gives away a season. Hangs off: reaches orders.sales_order through its keys; references
-- identity.principal, identity.role. Reached by: 2 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS orders.invitation_allowance (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid NOT NULL,
    role_id                           uuid,
    period_kind                       text NOT NULL,
    allowance                         integer NOT NULL,
    used                              integer NOT NULL,
    remaining                         integer,
    requires_approval_above           integer
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.membership_renewal (
    id                                uuid PRIMARY KEY,
    customer_membership_id            uuid NOT NULL,
    plan_id                           uuid NOT NULL,
    order_id                          text,
    type                              text NOT NULL,
    status                            text NOT NULL,
    previous_expiry_at                timestamptz,
    new_expiry_at                     timestamptz,
    attempted_at                      timestamptz NOT NULL,
    completed_at                      timestamptz,
    failure_reason                    text
);

-- drawer opened without a sale. Recorded because it is the classic cover for theft Hangs off:
-- reaches orders.sales_order through its keys; references identity.principal, orders.pos_shift,
-- platform.workstation. Reached by: 1 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS orders.no_sale_event (
    id                                text PRIMARY KEY NOT NULL,
    shift_id                          text NOT NULL,
    workstation_id                    uuid,
    reason                            text NOT NULL,
    note                              text,
    principal_id                      uuid NOT NULL,
    recorded_at                       timestamptz NOT NULL,
    count_this_shift                  integer
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.order_fee (
    id                                uuid PRIMARY KEY,
    order_id                          text NOT NULL,
    rule_id                           uuid,
    payment_method_id                 uuid,
    name                              text NOT NULL,
    category                          text NOT NULL,
    calculation_type                  text,
    rate_value                        numeric(18,4),
    amount                            numeric(18,4) NOT NULL,
    tax_amount                        numeric(18,4) NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- One thing bought on one order, priced at the moment of sale. A price list changing afterwards
-- does not change what somebody paid
CREATE TABLE IF NOT EXISTS orders.order_line (
    sales_order_id                    text NOT NULL,
    id                                text PRIMARY KEY,
    variant_id                        uuid,
    performance_id                    uuid,
    inventory_hold_id                 text,
    seat_ids                          text[],
    quantity                          integer,
    quoted_unit_price                 numeric(18,4),
    holder_name                       text,
    data_mask_values                  jsonb,
    server_unit_price                 numeric(18,4),
    price_variance                    numeric(18,4),
    tax_amount                        numeric(18,4),
    net_amount                        numeric(18,4),
    gross_amount                      numeric(18,4),
    entitlement_ids                   text[],
    cross_region_right_ids            text[],
    lease_id                          text NOT NULL
);

-- links an order to the media its entitlements were issued onto. What makes append-to-existing
-- possible without editing a paid order Hangs off: reaches orders.sales_order through its keys;
-- references orders.sales_order.
CREATE TABLE IF NOT EXISTS orders.order_media_link (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL
);

-- A tender against an order, with the rate it converted at fixed on the row (CF-37). A payment
-- reconciled next month is reconciled at the rate of the day it was taken
CREATE TABLE IF NOT EXISTS orders.payment (
    id                                text PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    tender                            text NOT NULL,
    tender_currency                   text,
    tender_amount                     numeric(18,4),
    fx_rate                           numeric(18,4),
    fx_rate_source                    text,
    change_currency                   text,
    amount                            numeric(18,4) NOT NULL,
    change_amount                     numeric(18,4),
    status                            text NOT NULL,
    provider_name                     text,
    provider_reference                text,
    last_inquiry_at                   timestamptz,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

-- A link a guest opens to pay for a booking taken at a till (BL-072). The link is the credential —
-- a guest holding one is anonymous, and a phone booking is exactly the case where they have not
-- registered. The expiry releases the hold, not just the link. Hangs off: reaches
-- orders.sales_order through its keys; references identity.principal, orders.sales_order,
-- retail.reservation. Reached by: 3 operati
CREATE TABLE IF NOT EXISTS orders.payment_link (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    reservation_id                    uuid,
    token                             text NOT NULL,
    status                            text NOT NULL,
    channel                           text,
    sent_to                           text,
    expires_at                        timestamptz NOT NULL,
    release_hold_on_expiry            boolean,
    viewed_at                         timestamptz,
    paid_at                           timestamptz,
    resend_count                      integer,
    issued_by_principal_id            uuid,
    scope_path                        text
);

-- tips post to a liability, not to sales Hangs off: a child of orders.payment; reaches
-- orders.sales_order through its keys; references orders.payment.
CREATE TABLE IF NOT EXISTS orders.payment_tip (
    id                                uuid PRIMARY KEY NOT NULL,
    payment_id                        text NOT NULL
);

-- A cash session at a workstation — opened with a float, closed with a count and a variance. Moved
-- to OrderService on 24 August because all its data is in orders
CREATE TABLE IF NOT EXISTS orders.pos_shift (
    id                                text PRIMARY KEY NOT NULL,
    workstation_id                    uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        text NOT NULL,
    principal_id                      uuid NOT NULL,
    principal_display_name            text,
    status                            text NOT NULL,
    deposit_box_code                  text,
    bag_number                        text,
    opening_float                     numeric(18,4),
    sales_total                       numeric(18,4),
    refunds_total                     numeric(18,4),
    lifts_total                       numeric(18,4),
    held_lease_count                  integer,
    opened_at                         timestamptz NOT NULL,
    recorded_at                       timestamptz,
    suspended_at                      timestamptz,
    closed_at                         timestamptz,
    synced_at                         timestamptz
);

-- Money going back, always against a payment and never editing it. The ledger posts both
CREATE TABLE IF NOT EXISTS orders.refund (
    id                                text PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    fx_rate                           numeric(18,4),
    tax_reversal_entry_id             uuid,
    settle_to                         text,
    fx_variance                       numeric(18,4),
    amount                            numeric(18,4) NOT NULL,
    applied_percentage                numeric(18,4),
    status                            text NOT NULL,
    reason                            text,
    requested_by_principal_id         uuid,
    secondary_principal_id            uuid,
    approved_by_principal_id          uuid,
    ledger_entry_id                   text,
    gateway_reference                 text,
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- When a refund is allowed and what it costs. Scoped, so a venue may be stricter than its tenant
CREATE TABLE IF NOT EXISTS orders.refund_policy (
    id                                uuid PRIMARY KEY,
    venue_id                          uuid NOT NULL,
    self_authorise_limit              numeric(18,4) NOT NULL,
    requires_second_user_above        numeric(18,4),
    requires_approval_above           numeric(18,4) NOT NULL,
    allow_partial                     boolean,
    refund_window_days                integer,
    variance_threshold                numeric(18,4)
);

-- An entitlement listed for resale (BL-060). A resale is a transfer with money attached and the
-- venue stays in the middle — the seller entitlement is voided and a new one issued, so the ticket
-- that admits is always one the venue issued
CREATE TABLE IF NOT EXISTS orders.resale_listing (
    id                                uuid PRIMARY KEY NOT NULL,
    entitlement_id                    uuid NOT NULL,
    seller_subject_id                 uuid NOT NULL,
    ask_price                         numeric(18,4) NOT NULL,
    price_cap_percent                 numeric(18,4),
    seller_fee_percent                numeric(18,4),
    buyer_fee_percent                 numeric(18,4),
    status                            text NOT NULL,
    listed_at                         timestamptz,
    sold_to_subject_id                uuid,
    payout_status                     text,
    scope_path                        text
);

-- A held place that is not yet a sale — a table, a cabana, a slot
CREATE TABLE IF NOT EXISTS orders.reservation (
    id                                text PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    status                            text NOT NULL,
    expires_at                        timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL,
    converted_order_id                text
);

-- The sale. What was bought, by whom, through which channel, at what scope. Every payment, refund,
-- entitlement and ledger posting reaches back to a row here
CREATE TABLE IF NOT EXISTS orders.sales_order (
    id                                text PRIMARY KEY NOT NULL,
    order_number                      text,
    channel                           text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        text NOT NULL,
    status                            text NOT NULL,
    gross_amount                      numeric(18,4) NOT NULL,
    tax_amount                        numeric(18,4) NOT NULL,
    net_amount                        numeric(18,4) NOT NULL,
    refunded_amount                   numeric(18,4),
    total_price_variance              numeric(18,4),
    principal_id                      uuid,
    workstation_id                    uuid,
    shift_id                          text,
    subject_id                        uuid,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

-- A hold against any stored-value instrument (CF-126). Two-phase spend for all six, where only the
-- retail wallet had it — a guest with 200 game credits starting a play the machine then failed had
-- no held balance Hangs off: reaches orders.sales_order through its keys. Reached by: 2 operations
-- read it and 5 write it; written by 3 contracts — marketing-crm, orders, resources.
CREATE TABLE IF NOT EXISTS orders.stored_value_authorisation (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL,
    instrument_id                     uuid NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    status                            text NOT NULL,
    captured_amount                   numeric(18,4),
    expires_at                        timestamptz,
    reference                         text,
    scope_path                        text
);

-- Ticket artwork and media selection (BL-102). A venue changing its artwork had no path that was
-- not a code change. Hangs off: reaches orders.sales_order through its keys. Reached by: 2
-- operations read it and 0 write it.
CREATE TABLE IF NOT EXISTS orders.ticket_template (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    is_recyclable                     boolean,
    recycle_after_days                integer,
    media_type                        text NOT NULL,
    applies_to_product_kinds          text[],
    selection_priority                integer,
    layout_ref                        text,
    locale_variants                   jsonb,
    is_active                         boolean NOT NULL
);

-- A ticket moving between people. Claimed by whoever holds the link, which is why it expires
CREATE TABLE IF NOT EXISTS orders.ticket_transfer (
    id                                text PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    ticket_ids                        text[] NOT NULL,
    from_subject_id                   uuid,
    to_subject_id                     uuid,
    recipient_address_masked          text,
    status                            text NOT NULL,
    claim_url                         text,
    offered_at                        timestamptz NOT NULL,
    claimed_at                        timestamptz,
    expires_at                        timestamptz NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.upgrade (
    id                                uuid PRIMARY KEY,
    number                            text NOT NULL,
    order_id                          text NOT NULL,
    original_order_line_id            uuid NOT NULL,
    new_order_line_id                 uuid,
    rule_id                           uuid,
    original_amount                   numeric(18,4) NOT NULL,
    new_amount                        numeric(18,4) NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    status                            text NOT NULL,
    requested_by_user_id              uuid,
    reason                            text,
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz,
    cancelled_at                      timestamptz
);

-- An Apple or Google wallet pass (BL-029). A live object, not a download — a pass that cannot be
-- pushed to is a screenshot with better rounding
CREATE TABLE IF NOT EXISTS orders.wallet_pass (
    id                                uuid PRIMARY KEY NOT NULL,
    entitlement_id                    uuid NOT NULL,
    platform                          text NOT NULL,
    serial_number                     text NOT NULL,
    authentication_token              text,
    status                            text NOT NULL,
    last_pushed_at                    timestamptz,
    device_registrations              integer,
    scope_path                        text
);

