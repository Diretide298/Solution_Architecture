-- orders — 44 tables
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
    scope_path                        ltree NOT NULL
);

-- A cart holds leases; an order holds money. Retained after expiry so a recovery link lands on
-- something Hangs off: reaches orders.sales_order through its keys; references pii.subject,
-- platform.scope. Reached by: 15 operations read it and 7 write it; 3 tables reference it; written
-- by 2 contracts — marketing-crm, orders.
CREATE TABLE IF NOT EXISTS orders.cart (
    id                                uuid PRIMARY KEY NOT NULL,
    token                             text,
    venue_id                          uuid NOT NULL,
    channel                           text NOT NULL CONSTRAINT cart_channel_chk CHECK (channel IN ('pos', 'kiosk', 'guestApp', 'guestWeb', 'callCentre', 'partner', 'api', 'backOffice', 'b2b', 'ota')),
    subject_id                        uuid,
    status                            text NOT NULL CONSTRAINT cart_status_chk CHECK (status IN ('active', 'expiring', 'expired', 'abandoned', 'checkedOut')),
    net_amount                        numeric(18,4),
    discount_total                    numeric(18,4),
    tax_total                         numeric(18,4),
    gross_amount                      numeric(18,4),
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
-- catalogue.inventory_hold, catalogue.performance, catalogue.variant. Reached by: 9 operations
-- read it and 4 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS orders.cart_line (
    id                                uuid PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    product_name                      text,
    quantity                          integer NOT NULL,
    performance_id                    uuid,
    seat_ids                          text[],
    parent_line_id                    uuid,
    override_price                    numeric(18,4),
    override_reason                   text CONSTRAINT cart_line_override_reason_chk CHECK (override_reason IN ('priceMatch', 'serviceRecovery', 'negotiated', 'damagedGoods', 'staffSale', 'error')),
    fee_kind                          text CONSTRAINT cart_line_fee_kind_chk CHECK (fee_kind IN ('booking', 'transaction', 'service', 'delivery', 'convenience', 'cancellation')),
    unit_price                        numeric(18,4),
    line_total                        numeric(18,4),
    inventory_hold_id                 text,
    lease_expires_at                  timestamptz,
    is_available                      boolean,
    cart_id                           uuid NOT NULL
);

-- a denomination and a count from a blind till count Hangs off: reaches orders.sales_order through
-- its keys; references orders.cash_movement, orders.deposit_box, orders.pos_shift. Reached by: 5
-- operations read it and 3 write it.
CREATE TABLE IF NOT EXISTS orders.cash_count_line (
    id                                uuid PRIMARY KEY,
    shift_id                          text NOT NULL,
    deposit_box_id                    uuid,
    count_kind                        text CONSTRAINT cash_count_line_count_kind_chk CHECK (count_kind IN ('openingFloat', 'close', 'movement')),
    cash_movement_id                  text,
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
    id                                text PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT cash_movement_kind_chk CHECK (kind IN ('openingFloat', 'lift', 'add')),
    amount                            numeric(18,4) NOT NULL,
    reference                         text CONSTRAINT cash_movement_reference_chk CHECK (char_length(reference) <= 64),
    reason                            text CONSTRAINT cash_movement_reason_chk CHECK (char_length(reason) <= 500),
    recorded_at                       timestamptz NOT NULL,
    shift_id                          text NOT NULL,
    deposit_box_id                    uuid,
    witness_principal_id              uuid,
    withdrawal_reason                 text,
    authorised_by_principal_id        uuid NOT NULL,
    sequence                          integer NOT NULL,
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
    reason                            text NOT NULL CONSTRAINT chargeback_reason_chk CHECK (reason IN ('fraudulent', 'productNotReceived', 'productUnacceptable', 'duplicate', 'subscriptionCancelled', 'creditNotProcessed', 'unrecognised', 'other')),
    status                            text NOT NULL CONSTRAINT chargeback_status_chk CHECK (status IN ('received', 'underReview', 'evidenceSubmitted', 'won', 'lost', 'accepted', 'expired')),
    evidence_due_by                   timestamptz NOT NULL,
    evidence_submitted_at             timestamptz,
    outcome_at                        timestamptz
);

-- a manual override of a partner credit limit, recorded with who and why. Second table on a marker
-- the deriver only read the first half of Hangs off: a child of orders.b2b_credit; reaches
-- orders.sales_order through its keys; references identity.principal, orders.b2b_credit,
-- orders.sales_order. Reached by: 3 operations read it and 1 write it.
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
    currency_code                     text NOT NULL CONSTRAINT deposit_currency_code_chk CHECK (char_length(currency_code) <= 10),
    required_amount                   numeric(18,4) NOT NULL,
    authorized_amount                 numeric(18,4) NOT NULL,
    captured_amount                   numeric(18,4) NOT NULL,
    released_amount                   numeric(18,4) NOT NULL,
    forfeited_amount                  numeric(18,4) NOT NULL,
    status                            text NOT NULL CONSTRAINT deposit_status_chk CHECK (char_length(status) <= 30),
    settled_at                        timestamptz,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- A cashier’s cash box. Allocated to a person, not a workstation — a cashier moving between tills
-- takes their float, which is what makes a variance attributable. withdrawnTotal reduces the
-- expected close: cash skimmed for banking is not a shortfall Hangs off: reaches
-- orders.sales_order through its keys; references identity.principal, orders.pos_shift,
-- platform.scope. Reached by: 5 operations read it
CREATE TABLE IF NOT EXISTS orders.deposit_box (
    id                                uuid PRIMARY KEY,
    cashier_principal_id              uuid NOT NULL,
    cashier_name                      text,
    venue_id                          uuid NOT NULL,
    workstation_id                    uuid,
    shift_id                          text,
    status                            text CONSTRAINT deposit_box_status_chk CHECK (status IN ('allocated', 'open', 'suspended', 'closing', 'closed', 'reconciled')),
    opening_float                     numeric(18,4) NOT NULL,
    withdrawn_total                   numeric(18,4),
    expected_total                    numeric(18,4),
    counted_total                     numeric(18,4),
    variance                          numeric(18,4),
    closed_by_principal_id            uuid,
    allocated_at                      timestamptz,
    closed_at                         timestamptz
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.deposit_box_foreign_holding (
    deposit_box_id                    uuid NOT NULL,
    currency                          text NOT NULL,
    expected_amount                   numeric(18,4),
    counted_amount                    numeric(18,4) NOT NULL,
    variance                          numeric(18,4),
    base_equivalent                   numeric(18,4),
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.deposit_box_opening_denomination (
    deposit_box_id                    uuid NOT NULL,
    denomination_id                   uuid NOT NULL,
    count                             integer NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What a deposit booking takes now and when the balance is due, with the refund cut-off. Parties
-- and some dining bookings; nothing said how much or when before this
CREATE TABLE IF NOT EXISTS orders.deposit_policy (
    id                                uuid PRIMARY KEY,
    applies_to                        text[],
    basis                             text NOT NULL CONSTRAINT deposit_policy_basis_chk CHECK (basis IN ('fixedPerBooking', 'fixedPerGuest', 'percentOfTotal', 'perBand')),
    amount                            numeric(18,4),
    percent                           numeric(18,4),
    band_size                         numeric(18,4),
    balance_due                       text DEFAULT 'onTheDay' CONSTRAINT deposit_policy_balance_due_chk CHECK (balance_due IN ('onTheDay', 'daysBefore')),
    balance_due_days_before           integer,
    refundable_until_hours            integer DEFAULT 24,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.discount (
    id                                uuid PRIMARY KEY,
    order_id                          text NOT NULL,
    promotion_id                      uuid,
    coupon_code                       text CONSTRAINT discount_coupon_code_chk CHECK (char_length(coupon_code) <= 100),
    type                              text NOT NULL CONSTRAINT discount_type_chk CHECK (char_length(type) <= 30),
    value                             numeric(18,4),
    applied_amount                    numeric(18,4) NOT NULL,
    reason                            text CONSTRAINT discount_reason_chk CHECK (char_length(reason) <= 500),
    created_at                        timestamptz NOT NULL
);

-- Evaluated before the charge (BL-118). It holds rather than refuses — a rule that declines
-- outright turns a false positive into a lost sale with an angry guest
CREATE TABLE IF NOT EXISTS orders.fraud_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    condition                         jsonb NOT NULL,
    action                            text NOT NULL CONSTRAINT fraud_rule_action_chk CHECK (action IN ('allow', 'flagForReview', 'requireStepUp', 'hold', 'decline')),
    risk_weight                       integer,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL
);

-- A group with a leader and an attendee manifest (BL-028). A school booking forty places has one
-- person who pays and forty who need names collecting, and a generic order has one guest
CREATE TABLE IF NOT EXISTS orders.group_booking (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text DEFAULT 'general' CONSTRAINT group_booking_kind_chk CHECK (kind IN ('general', 'school', 'corporate', 'party')),
    package_product_id                text,
    year_group                        text CONSTRAINT group_booking_year_group_chk CHECK (char_length(year_group) <= 40),
    access_and_dietary_needs          text CONSTRAINT group_booking_access_and_dietary_needs_chk CHECK (char_length(access_and_dietary_needs) <= 1000),
    celebrant_name                    text CONSTRAINT group_booking_celebrant_name_chk CHECK (char_length(celebrant_name) <= 120),
    celebrant_turning_age             integer,
    allergies_and_requests            text CONSTRAINT group_booking_allergies_and_requests_chk CHECK (char_length(allergies_and_requests) <= 1000),
    final_headcount_due_by            timestamptz,
    quote_sent_at                     timestamptz,
    risk_assessment_sent_at           timestamptz,
    preferred_date                    date,
    order_id                          text NOT NULL,
    leader_subject_id                 uuid NOT NULL,
    organisation_name                 text,
    expected_size                     integer NOT NULL,
    confirmed_size                    integer,
    minimum_size                      integer,
    is_attendee_capture_required      boolean DEFAULT false,
    attendee_capture_due_by           timestamptz,
    status                            text NOT NULL CONSTRAINT group_booking_status_chk CHECK (status IN ('provisional', 'confirmed', 'namesPending', 'complete', 'cancelled'))
);

-- A complimentary entitlement issued outside the order path (8.1.3–8.1.5). No payment is expected,
-- so nothing waits for one. Hangs off: reaches orders.sales_order through its keys; references
-- catalogue.performance, catalogue.product, identity.principal. Reached by: 2 operations read it
-- and 1 write it.
CREATE TABLE IF NOT EXISTS orders.invitation (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    performance_id                    uuid,
    quantity                          integer NOT NULL,
    reason                            text NOT NULL CONSTRAINT invitation_reason_chk CHECK (reason IN ('hosting', 'media', 'sponsor', 'staff', 'compensation', 'community', 'trade')),
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
    period_kind                       text NOT NULL CONSTRAINT invitation_allowance_period_kind_chk CHECK (period_kind IN ('perPerformance', 'monthly', 'quarterly', 'annual', 'unlimited')),
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
    entitlement_template_id           uuid NOT NULL,
    order_id                          text,
    type                              text NOT NULL CONSTRAINT membership_renewal_type_chk CHECK (char_length(type) <= 30),
    status                            text NOT NULL CONSTRAINT membership_renewal_status_chk CHECK (char_length(status) <= 30),
    previous_expiry_at                timestamptz,
    new_expiry_at                     timestamptz,
    attempted_at                      timestamptz NOT NULL,
    completed_at                      timestamptz,
    failure_reason                    text CONSTRAINT membership_renewal_failure_reason_chk CHECK (char_length(failure_reason) <= 500)
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
    name                              text NOT NULL CONSTRAINT order_fee_name_chk CHECK (char_length(name) <= 150),
    category                          text NOT NULL CONSTRAINT order_fee_category_chk CHECK (char_length(category) <= 20),
    calculation_type                  text CONSTRAINT order_fee_calculation_type_chk CHECK (char_length(calculation_type) <= 20),
    rate_value                        numeric(18,4),
    amount                            numeric(18,4) NOT NULL,
    tax_amount                        numeric(18,4) NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- One thing bought on one order, priced at the moment of sale. A price list changing afterwards
-- does not change what somebody paid
CREATE TABLE IF NOT EXISTS orders.order_line (
    sales_order_id                    text NOT NULL,
    id                                text PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    performance_id                    uuid,
    inventory_hold_id                 text,
    seat_ids                          text[],
    quantity                          integer NOT NULL,
    quoted_unit_price                 numeric(18,4) NOT NULL,
    holder_name                       text,
    data_mask_values                  jsonb,
    server_unit_price                 numeric(18,4) NOT NULL,
    price_variance                    numeric(18,4),
    tax_amount                        numeric(18,4) NOT NULL,
    net_amount                        numeric(18,4) NOT NULL,
    gross_amount                      numeric(18,4) NOT NULL,
    entitlement_ids                   text[],
    cross_region_right_ids            text[],
    reprint_count                     integer DEFAULT 0
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.order_line_eligibility (
    order_line_id                     text NOT NULL,
    age_band                          text,
    age_years                         integer,
    height_band_index                 integer,
    confident_swimmer                 boolean,
    is_guardian_signed                boolean,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A tender against an order, with the rate it converted at fixed on the row (CF-37). A payment
-- reconciled next month is reconciled at the rate of the day it was taken
CREATE TABLE IF NOT EXISTS orders.payment (
    id                                text PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    tender                            text NOT NULL CONSTRAINT payment_tender_chk CHECK (tender IN ('cash', 'card', 'wallet', 'voucher', 'bankTransfer', 'hotelCharge', 'installment', 'giftCard', 'complimentary')),
    tender_currency                   text,
    tender_amount                     numeric(18,4),
    fx_rate                           numeric(18,6),
    fx_rate_source                    text CONSTRAINT payment_fx_rate_source_chk CHECK (fx_rate_source IN ('manual', 'feed', 'cardScheme')),
    change_currency                   text,
    amount                            numeric(18,4) NOT NULL,
    change_amount                     numeric(18,4),
    status                            text NOT NULL CONSTRAINT payment_status_chk CHECK (status IN ('authorised', 'captured', 'pendingConfirmation', 'declined', 'failed', 'voided', 'refunded')),
    provider_name                     text,
    provider_reference                text,
    last_inquiry_at                   timestamptz,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

-- A link a guest opens to pay for a booking taken at a till (BL-072). The link is the credential —
-- a guest holding one is anonymous, and a phone booking is exactly the case where they have not
-- registered. The expiry releases the hold, not just the link. Hangs off: reaches
-- orders.sales_order through its keys; references identity.principal, orders.reservation,
-- orders.sales_order. Reached by: 4 operati
CREATE TABLE IF NOT EXISTS orders.payment_link (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    reservation_id                    text,
    token                             text NOT NULL,
    status                            text NOT NULL CONSTRAINT payment_link_status_chk CHECK (status IN ('issued', 'viewed', 'paid', 'expired', 'cancelled', 'superseded')),
    channel                           text CONSTRAINT payment_link_channel_chk CHECK (channel IN ('email', 'sms', 'whatsapp', 'printed')),
    sent_to                           text,
    expires_at                        timestamptz NOT NULL,
    release_hold_on_expiry            boolean DEFAULT true,
    viewed_at                         timestamptz,
    paid_at                           timestamptz,
    resend_count                      integer DEFAULT 0,
    issued_by_principal_id            uuid,
    scope_path                        ltree NOT NULL
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
    scope_path                        ltree NOT NULL,
    principal_id                      uuid NOT NULL,
    principal_display_name            text,
    status                            text NOT NULL CONSTRAINT pos_shift_status_chk CHECK (status IN ('pendingApproval', 'open', 'suspended', 'pendingVariance', 'pendingClosure', 'closed', 'autoClosed')),
    deposit_box_code                  text,
    bag_number                        text,
    opening_float                     numeric(18,4),
    gross_sales_amount                numeric(18,4),
    gross_refunded_amount             numeric(18,4),
    lifted_amount                     numeric(18,4),
    expected_cash_amount              numeric(18,4),
    counted_cash_amount               numeric(18,4),
    variance_amount                   numeric(18,4),
    held_lease_count                  integer,
    opened_at                         timestamptz NOT NULL,
    recorded_at                       timestamptz,
    suspended_at                      timestamptz,
    suspend_reason                    text CONSTRAINT pos_shift_suspend_reason_chk CHECK (char_length(suspend_reason) <= 200),
    closed_at                         timestamptz,
    closed_by_principal_id            uuid,
    synced_at                         timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.pos_shift_approval (
    pos_shift_id                      text NOT NULL,
    kind                              text NOT NULL,
    principal_id                      uuid NOT NULL,
    at                                timestamptz NOT NULL,
    reason                            text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.pos_shift_incident (
    pos_shift_id                      text NOT NULL,
    kind                              text,
    at                                timestamptz,
    principal_id                      uuid,
    note                              text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Money going back, always against a payment and never editing it. The ledger posts both
CREATE TABLE IF NOT EXISTS orders.refund (
    id                                text PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    batch_id                          uuid,
    fx_rate                           numeric(18,6),
    tax_reversal_entry_id             uuid,
    settle_to                         text DEFAULT 'originalTender' CONSTRAINT refund_settle_to_chk CHECK (settle_to IN ('originalTender', 'advanceBalance', 'wireTransfer', 'storeCredit')),
    fx_variance                       numeric(18,4),
    amount                            numeric(18,4) NOT NULL,
    applied_percentage                numeric(18,4),
    status                            text NOT NULL CONSTRAINT refund_status_chk CHECK (status IN ('pendingApproval', 'pendingGateway', 'completed', 'declined', 'failed')),
    reason                            text,
    requested_by_principal_id         uuid,
    secondary_principal_id            uuid,
    approved_by_principal_id          uuid,
    ledger_entry_id                   text,
    gateway_reference                 text,
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.refund_batch (
    id                                uuid PRIMARY KEY NOT NULL,
    performance_id                    uuid,
    event_id                          uuid,
    venue_id                          uuid,
    date_from                         date,
    date_to                           date,
    percentage                        numeric(18,4),
    reason                            text NOT NULL,
    affected_orders                   integer NOT NULL,
    estimated_total                   numeric(18,4) NOT NULL,
    status                            text NOT NULL CONSTRAINT refund_batch_status_chk CHECK (status IN ('pendingApproval', 'processing', 'completed', 'failed')),
    requested_by_principal_id         uuid,
    created_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- When a refund is allowed and what it costs. Scoped, so a venue may be stricter than its tenant
CREATE TABLE IF NOT EXISTS orders.refund_policy (
    id                                uuid PRIMARY KEY,
    venue_id                          uuid NOT NULL,
    self_authorise_limit              numeric(18,4) NOT NULL,
    requires_second_user_above        numeric(18,4),
    requires_approval_above           numeric(18,4) NOT NULL,
    allow_partial                     boolean DEFAULT true,
    refund_window_days                integer,
    variance_threshold                numeric(18,4)
);

-- Holds 4 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.refund_policy_time_band (
    refund_policy_id                  uuid NOT NULL,
    hours_before                      integer NOT NULL,
    percentage                        numeric(18,4) NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- What a resale costs and how high it may be priced. orders.resale_listing stored
-- seller_fee_percent, buyer_fee_percent and price_cap_percent on every listing with nothing
-- producing them, so two listings a minute apart could carry different commercials and record no
-- reason. The listing keeps its columns as the snapshot — the same rule-and-record split
-- payments.fee_rule and orders.order_fee already u
CREATE TABLE IF NOT EXISTS orders.resale_fee_policy (
    id                                uuid PRIMARY KEY,
    event_id                          uuid,
    product_id                        uuid,
    seller_fee_percent                numeric(18,4) NOT NULL,
    buyer_fee_percent                 numeric(18,4) NOT NULL,
    price_cap_percent                 numeric(18,4),
    minimum_ask_price                 numeric(18,4),
    fees_shown_to_seller              boolean,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL
);

-- An entitlement listed for resale (BL-060). A resale is a transfer with money attached and the
-- venue stays in the middle — the seller entitlement is voided and a new one issued, so the ticket
-- that admits is always one the venue issued
CREATE TABLE IF NOT EXISTS orders.resale_listing (
    id                                uuid PRIMARY KEY NOT NULL,
    entitlement_id                    text NOT NULL,
    seller_subject_id                 uuid NOT NULL,
    ask_price                         numeric(18,4) NOT NULL,
    price_cap_percent                 numeric(18,4),
    seller_fee_percent                numeric(18,4),
    buyer_fee_percent                 numeric(18,4),
    status                            text NOT NULL CONSTRAINT resale_listing_status_chk CHECK (status IN ('listed', 'reserved', 'sold', 'withdrawn', 'expired')),
    listed_at                         timestamptz,
    sold_to_subject_id                uuid,
    payout_status                     text CONSTRAINT resale_listing_payout_status_chk CHECK (payout_status IN ('pending', 'held', 'paid', 'failed')),
    scope_path                        ltree NOT NULL
);

-- A held place that is not yet a sale — a table, a cabana, a slot
CREATE TABLE IF NOT EXISTS orders.reservation (
    id                                text PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    subject_id                        uuid,
    status                            text NOT NULL CONSTRAINT reservation_status_chk CHECK (status IN ('held', 'converted', 'expired', 'cancelled')),
    expires_at                        timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL,
    converted_order_id                text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.reservation_line (
    reservation_id                    text NOT NULL,
    id                                text PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    performance_id                    uuid,
    inventory_hold_id                 text,
    seat_ids                          text[],
    quantity                          integer NOT NULL,
    quoted_unit_price                 numeric(18,4) NOT NULL,
    holder_name                       text,
    data_mask_values                  jsonb
);

-- The sale. What was bought, by whom, through which channel, at what scope. Every payment, refund,
-- entitlement and ledger posting reaches back to a row here
CREATE TABLE IF NOT EXISTS orders.sales_order (
    id                                text PRIMARY KEY NOT NULL,
    order_number                      text,
    channel                           text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    status                            text NOT NULL CONSTRAINT sales_order_status_chk CHECK (status IN ('pending', 'held', 'paid', 'partiallyPaid', 'completed', 'voided', 'refunded', 'partiallyRefunded', 'failed')),
    gross_amount                      numeric(18,4) NOT NULL,
    tax_amount                        numeric(18,4) NOT NULL,
    net_amount                        numeric(18,4) NOT NULL,
    refunded_amount                   numeric(18,4),
    total_price_variance              numeric(18,4),
    principal_id                      uuid,
    workstation_id                    uuid,
    shift_id                          text,
    subject_id                        uuid,
    hold_label                        text CONSTRAINT sales_order_hold_label_chk CHECK (char_length(hold_label) <= 60),
    held_until                        timestamptz,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

-- A hold against any stored-value instrument (CF-126). Two-phase spend for all six, where only the
-- retail wallet had it — a guest with 200 game credits starting a play the machine then failed had
-- no held balance Hangs off: reaches orders.sales_order through its keys. Reached by: 3 operations
-- read it and 5 write it; written by 3 contracts — marketing-crm, orders, resources.
CREATE TABLE IF NOT EXISTS orders.stored_value_authorisation (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT stored_value_authorisation_kind_chk CHECK (kind IN ('wallet', 'giftCard', 'gameCard', 'voucher', 'loyalty', 'prepaidEntitlement')),
    instrument_id                     uuid NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    status                            text NOT NULL CONSTRAINT stored_value_authorisation_status_chk CHECK (status IN ('held', 'partiallyCaptured', 'captured', 'released', 'expired')),
    captured_amount                   numeric(18,4),
    expires_at                        timestamptz,
    reference                         text,
    scope_path                        ltree NOT NULL
);

-- Ticket artwork and media selection (BL-102). A venue changing its artwork had no path that was
-- not a code change. Hangs off: reaches orders.sales_order through its keys. Reached by: 5
-- operations read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS orders.ticket_template (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    is_recyclable                     boolean DEFAULT false,
    recycle_after_days                integer,
    media_type                        text NOT NULL CONSTRAINT ticket_template_media_type_chk CHECK (media_type IN ('thermalTicket', 'a4Pdf', 'wristband', 'rfidCard', 'walletPass', 'qrOnly', 'sms')),
    applies_to_product_kinds          text[],
    selection_priority                integer DEFAULT 100,
    layout_ref                        text,
    locale_variants                   jsonb,
    is_active                         boolean NOT NULL
);

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.ticket_template_channel (
    ticket_template_id                uuid NOT NULL,
    applies_to_channel                text NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- A ticket moving between people. Claimed by whoever holds the link, which is why it expires
CREATE TABLE IF NOT EXISTS orders.ticket_transfer (
    id                                text PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    ticket_ids                        text[] NOT NULL,
    from_subject_id                   uuid,
    to_subject_id                     uuid,
    recipient_address_masked          text,
    status                            text NOT NULL CONSTRAINT ticket_transfer_status_chk CHECK (status IN ('offered', 'claimed', 'expired', 'cancelled')),
    claim_url                         text,
    claim_token                       text,
    offered_at                        timestamptz NOT NULL,
    claimed_at                        timestamptz,
    expires_at                        timestamptz NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.upgrade (
    id                                uuid PRIMARY KEY,
    number                            text NOT NULL CONSTRAINT upgrade_number_chk CHECK (char_length(number) <= 50),
    order_id                          text NOT NULL,
    original_order_line_id            text NOT NULL,
    new_order_line_id                 text,
    rule_id                           uuid,
    original_amount                   numeric(18,4) NOT NULL,
    new_amount                        numeric(18,4) NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    status                            text NOT NULL CONSTRAINT upgrade_status_chk CHECK (char_length(status) <= 30),
    requested_by_principal_id         uuid,
    reason                            text CONSTRAINT upgrade_reason_chk CHECK (char_length(reason) <= 500),
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz,
    cancelled_at                      timestamptz
);

-- One reminder per booking, set by the guest. GST-018 Add to Calendar / Reminders had nothing
-- behind its reminders half. A row says how long before each session to remind and on which
-- channels; the sender skips any channel the guest has since withdrawn consent for, because a
-- reminder is not a reason to message somebody who said no
CREATE TABLE IF NOT EXISTS orders.visit_reminder (
    id                                uuid PRIMARY KEY,
    order_id                          text,
    subject_id                        uuid,
    is_enabled                        boolean NOT NULL,
    lead_time_minutes                 integer DEFAULT 1440,
    channels                          text[],
    scope_path                        ltree NOT NULL
);

-- An Apple or Google wallet pass (BL-029). A live object, not a download — a pass that cannot be
-- pushed to is a screenshot with better rounding
CREATE TABLE IF NOT EXISTS orders.wallet_pass (
    id                                uuid PRIMARY KEY NOT NULL,
    entitlement_id                    text NOT NULL,
    platform                          text NOT NULL CONSTRAINT wallet_pass_platform_chk CHECK (platform IN ('apple', 'google')),
    serial_number                     text NOT NULL,
    authentication_token              text,
    status                            text NOT NULL CONSTRAINT wallet_pass_status_chk CHECK (status IN ('issued', 'updated', 'voided', 'expired')),
    last_pushed_at                    timestamptz,
    device_registrations              integer,
    scope_path                        ltree NOT NULL
);

