-- orders — 82 tables
-- **Derived. Do not hand-edit.**

-- Holds 33 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.after_sale_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text CONSTRAINT after_sale_policy_name_chk CHECK (char_length(name) <= 150),
    product_id                        uuid,
    event_id                          uuid,
    performance_id                    uuid,
    channel                           text CONSTRAINT after_sale_policy_channel_chk CHECK (char_length(channel) <= 40),
    customer_segment_id               uuid,
    permitted_modifications           text[],
    eligible_ticket_statuses          text[],
    maximum_amendments_per_order      integer,
    maximum_amendments_per_ticket     integer,
    maximum_date_changes              integer,
    cooling_period_hours              integer,
    permitted_cancellation_scopes     text[],
    evaluated_conditions              text[],
    cancellation_reason_codes         text[],
    void_types                        text[],
    void_same_business_day_only       boolean DEFAULT true,
    void_before_settlement_only       boolean DEFAULT true,
    void_before_ticket_use_only       boolean DEFAULT true,
    void_before_fiscal_closure_only   boolean DEFAULT true,
    is_void_supervisor_required       boolean DEFAULT true,
    void_dual_authorisation           boolean DEFAULT false,
    void_channels                     text[],
    void_reason_codes                 text[],
    maximum_reissues                  integer,
    free_reissue_count                integer DEFAULT 0,
    reissue_supervisor_threshold      integer,
    default_reissue_option            text DEFAULT 'regenerateNew' CONSTRAINT after_sale_policy_default_reissue_option_chk CHECK (default_reissue_option IN ('regenerateNew', 'resendExisting')),
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.after_sale_policy_window (
    after_sale_policy_id              uuid NOT NULL,
    min_hours_before                  integer NOT NULL,
    max_hours_before                  integer,
    outcome                           text NOT NULL,
    fee_percent                       numeric(18,4),
    fee_amount                        numeric(18,4),
    is_supervisor_exception_allowed   boolean,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 28 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.after_sale_request (
    id                                uuid PRIMARY KEY NOT NULL,
    number                            text CONSTRAINT after_sale_request_number_chk CHECK (char_length(number) <= 50),
    order_id                          uuid NOT NULL,
    order_line_id                     uuid,
    reservation_id                    uuid,
    group_booking_id                  uuid,
    request_type                      text NOT NULL CONSTRAINT after_sale_request_request_type_chk CHECK (request_type IN ('orderAmendment', 'reservationAmendment', 'dateChange', 'timeslotChange', 'performanceChange', 'quantityChange', 'attendeeChange', 'seatChange', 'deliveryChange', 'cancellation', 'partialCancellation', 'void', 'reissue', 'serviceRecoveryException')),
    channel                           text CONSTRAINT after_sale_request_channel_chk CHECK (char_length(channel) <= 40),
    reason_code                       text CONSTRAINT after_sale_request_reason_code_chk CHECK (char_length(reason_code) <= 40),
    reason                            text CONSTRAINT after_sale_request_reason_chk CHECK (char_length(reason) <= 1000),
    before                            jsonb,
    after                             jsonb,
    after_sale_policy_id              uuid,
    policy_result                     text CONSTRAINT after_sale_request_policy_result_chk CHECK (char_length(policy_result) <= 200),
    requested_exception               text CONSTRAINT after_sale_request_requested_exception_chk CHECK (char_length(requested_exception) <= 1000),
    remedy                            text CONSTRAINT after_sale_request_remedy_chk CHECK (remedy IN ('complimentaryReissue', 'feeWaiver', 'partialRefund', 'voucher', 'walletCredit', 'alternativeDate', 'alternativeEvent', 'complimentaryAddOn')),
    financial_impact                  numeric(18,4),
    refund_id                         uuid,
    status                            text NOT NULL CONSTRAINT after_sale_request_status_chk CHECK (status IN ('requested', 'pendingApproval', 'approved', 'rejected', 'completed', 'failed')),
    escalated_at                      timestamptz,
    requested_by_principal_id         uuid,
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    decision_comment                  text CONSTRAINT after_sale_request_decision_comment_chk CHECK (char_length(decision_comment) <= 1000),
    failure_reason                    text CONSTRAINT after_sale_request_failure_reason_chk CHECK (char_length(failure_reason) <= 500),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- A partner’s credit line, drawn against and settled periodically
CREATE TABLE IF NOT EXISTS orders.b2b_credit (
    id                                uuid PRIMARY KEY NOT NULL,
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
-- platform.scope. Reached by: 24 operations read it and 9 write it; 7 tables reference it; written
-- by 3 contracts — marketing-crm, orders, venue-map.
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
    coupon_codes                      text[],
    expires_at                        timestamptz,
    extensions_used                   integer,
    max_extensions                    integer,
    locale                            text,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- One line, with the lease that holds its capacity. Null lease for a product with no capacity
-- Hangs off: a child of orders.cart; reaches orders.sales_order through its keys; references
-- catalogue.inventory_hold, catalogue.performance, catalogue.variant. Reached by: 12 operations
-- read it and 6 write it; 3 tables reference it; written by 2 contracts — orders, venue-map.
CREATE TABLE IF NOT EXISTS orders.cart_line (
    id                                uuid PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    product_name                      text,
    quantity                          integer NOT NULL,
    performance_id                    uuid,
    booked_window                     jsonb,
    recommendation_id                 uuid,
    table_reservation_id              uuid,
    seat_ids                          text[],
    resource_hold_id                  uuid,
    attributes                        jsonb,
    parent_line_id                    uuid,
    override_price                    numeric(18,4),
    override_reason                   text CONSTRAINT cart_line_override_reason_chk CHECK (override_reason IN ('priceMatch', 'serviceRecovery', 'negotiated', 'damagedGoods', 'staffSale', 'error')),
    fee_kind                          text CONSTRAINT cart_line_fee_kind_chk CHECK (fee_kind IN ('booking', 'transaction', 'service', 'delivery', 'convenience', 'cancellation')),
    unit_price                        numeric(18,4),
    line_total                        numeric(18,4),
    inventory_hold_id                 uuid,
    lease_expires_at                  timestamptz,
    is_available                      boolean,
    cart_id                           uuid NOT NULL
);

-- a denomination and a count from a blind till count Hangs off: reaches orders.sales_order through
-- its keys; references orders.cash_movement, orders.deposit_box, orders.pos_shift. Reached by: 7
-- operations read it and 5 write it.
CREATE TABLE IF NOT EXISTS orders.cash_count_line (
    id                                uuid PRIMARY KEY NOT NULL,
    shift_id                          uuid NOT NULL,
    deposit_box_id                    uuid,
    count_kind                        text CONSTRAINT cash_count_line_count_kind_chk CHECK (count_kind IN ('openingFloat', 'close', 'movement')),
    cash_movement_id                  uuid,
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
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT cash_movement_kind_chk CHECK (kind IN ('openingFloat', 'lift', 'add')),
    amount                            numeric(18,4) NOT NULL,
    reference                         text CONSTRAINT cash_movement_reference_chk CHECK (char_length(reference) <= 64),
    reason                            text CONSTRAINT cash_movement_reason_chk CHECK (char_length(reason) <= 500),
    recorded_at                       timestamptz NOT NULL,
    shift_id                          uuid NOT NULL,
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
    payment_id                        uuid NOT NULL,
    provider_id                       uuid,
    provider_case_reference           text,
    amount                            numeric(18,4) NOT NULL,
    fee_amount                        numeric(18,4),
    reason                            text NOT NULL CONSTRAINT chargeback_reason_chk CHECK (reason IN ('fraudulent', 'productNotReceived', 'productUnacceptable', 'duplicate', 'subscriptionCancelled', 'creditNotProcessed', 'unrecognised', 'other')),
    status                            text NOT NULL CONSTRAINT chargeback_status_chk CHECK (status IN ('received', 'underReview', 'evidenceSubmitted', 'won', 'lost', 'accepted', 'expired')),
    evidence_due_by                   timestamptz NOT NULL,
    evidence_submitted_at             timestamptz,
    outcome_at                        timestamptz,
    scheme_reason_code                text,
    notified_at                       timestamptz,
    assignee_principal_id             uuid,
    debit_journal_entry_id            uuid,
    outcome_journal_entry_id          uuid
);

-- One item of evidence assembled for a chargeback (29 September): the order, the scan that
-- admitted them, the delivery, the terms accepted, a communication or a device fingerprint, each a
-- kind and a reference. Its own rows because a list of objects has nowhere else to be stored, and
-- because which evidence wins depends on the chargeback's reason
CREATE TABLE IF NOT EXISTS orders.chargeback_evidence (
    chargeback_id                     uuid NOT NULL,
    kind                              text,
    reference                         text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- The investigation notes on a chargeback, oldest first (29 September), each with who wrote it and
-- when. Append-only: assignChargeback and recordChargebackOutcome add to it and nothing edits it
CREATE TABLE IF NOT EXISTS orders.chargeback_investigation_log (
    chargeback_id                     uuid NOT NULL,
    note                              text,
    principal_id                      uuid,
    at                                timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- a manual override of a partner credit limit, recorded with who and why. Second table on a marker
-- the deriver only read the first half of Hangs off: a child of orders.b2b_credit; reaches
-- orders.sales_order through its keys; references identity.principal, orders.b2b_credit,
-- orders.sales_order. Reached by: 3 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS orders.credit_override (
    b2b_credit_id                     uuid NOT NULL,
    order_id                          uuid,
    amount                            numeric(18,4),
    authorised_by_principal_id        uuid,
    reason                            text,
    expires_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.deposit (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
    customer_id                       uuid,
    rental_agreement_id               uuid,
    table_reservation_id              uuid,
    currency_code                     text NOT NULL CONSTRAINT deposit_currency_code_chk CHECK (char_length(currency_code) <= 10),
    required_amount                   numeric(18,4) NOT NULL,
    authorized_amount                 numeric(18,4) NOT NULL,
    captured_amount                   numeric(18,4) NOT NULL,
    released_amount                   numeric(18,4) NOT NULL,
    forfeited_amount                  numeric(18,4) NOT NULL,
    status                            text NOT NULL CONSTRAINT deposit_status_chk CHECK (char_length(status) <= 30),
    settled_at                        timestamptz,
    created_at                        timestamptz,
    updated_at                        timestamptz,
    ledger_deposit_id                 uuid
);

-- A cashier’s cash box. Allocated to a person, not a workstation — a cashier moving between tills
-- takes their float, which is what makes a variance attributable. withdrawnTotal reduces the
-- expected close: cash skimmed for banking is not a shortfall Hangs off: reaches
-- orders.sales_order through its keys; references identity.principal, orders.pos_shift,
-- platform.scope. Reached by: 5 operations read it
CREATE TABLE IF NOT EXISTS orders.deposit_box (
    id                                uuid PRIMARY KEY NOT NULL,
    cashier_principal_id              uuid NOT NULL,
    cashier_name                      text,
    venue_id                          uuid NOT NULL,
    workstation_id                    uuid,
    shift_id                          uuid,
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
    id                                uuid PRIMARY KEY NOT NULL,
    applies_to                        text[],
    dining                            jsonb,
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
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
    promotion_id                      uuid,
    coupon_code                       text CONSTRAINT discount_coupon_code_chk CHECK (char_length(coupon_code) <= 100),
    type                              text NOT NULL CONSTRAINT discount_type_chk CHECK (char_length(type) <= 30),
    value                             numeric(18,4),
    applied_amount                    numeric(18,4) NOT NULL,
    reason                            text CONSTRAINT discount_reason_chk CHECK (char_length(reason) <= 500),
    created_at                        timestamptz NOT NULL
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.external_reference_mapping (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
    payment_id                        uuid,
    refund_id                         uuid,
    source_system                     text NOT NULL CONSTRAINT external_reference_mapping_source_system_chk CHECK (source_system IN ('paymentGateways', 'acquirers', 'banks', 'posTerminals', 'b2bPartners', 'resellers', 'otas', 'erp', 'financeSystems', 'walletProviders')),
    provider                          text CONSTRAINT external_reference_mapping_provider_chk CHECK (char_length(provider) <= 60),
    merchant_id                       text CONSTRAINT external_reference_mapping_merchant_id_chk CHECK (char_length(merchant_id) <= 60),
    external_transaction_id           text CONSTRAINT external_reference_mapping_external_transaction_id_chk CHECK (char_length(external_transaction_id) <= 100),
    authorization_code                text CONSTRAINT external_reference_mapping_authorization_code_chk CHECK (char_length(authorization_code) <= 40),
    partner_order_id                  text CONSTRAINT external_reference_mapping_partner_order_id_chk CHECK (char_length(partner_order_id) <= 100),
    settlement_batch                  text CONSTRAINT external_reference_mapping_settlement_batch_chk CHECK (char_length(settlement_batch) <= 100),
    settlement_date                   date,
    erp_reference                     text CONSTRAINT external_reference_mapping_erp_reference_chk CHECK (char_length(erp_reference) <= 100),
    amount                            numeric(18,4),
    is_manual                         boolean DEFAULT false,
    reason                            text CONSTRAINT external_reference_mapping_reason_chk CHECK (char_length(reason) <= 500),
    approval_reference                text CONSTRAINT external_reference_mapping_approval_reference_chk CHECK (char_length(approval_reference) <= 100),
    created_by_principal_id           uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Evaluated before the charge (BL-118). It holds rather than refuses — a rule that declines
-- outright turns a false positive into a lost sale with an angry guest
CREATE TABLE IF NOT EXISTS orders.fraud_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    condition                         jsonb NOT NULL,
    applies_to                        text DEFAULT 'charge' CONSTRAINT fraud_rule_applies_to_chk CHECK (applies_to IN ('charge', 'refund')),
    signal                            text CONSTRAINT fraud_rule_signal_chk CHECK (signal IN ('velocityCount', 'velocityAmount', 'issuerCountry', 'deviceReuse', 'billingMismatch', 'refundCount', 'refundValue', 'refundRatio')),
    subject_key                       text DEFAULT 'guest' CONSTRAINT fraud_rule_subject_key_chk CHECK (subject_key IN ('guest', 'paymentToken', 'device')),
    threshold                         numeric(18,4),
    window_days                       integer,
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
    order_id                          uuid NOT NULL,
    leader_subject_id                 uuid NOT NULL,
    organisation_name                 text,
    expected_size                     integer NOT NULL,
    confirmed_size                    integer,
    minimum_size                      integer,
    is_attendee_capture_required      boolean DEFAULT false,
    attendee_capture_due_by           timestamptz,
    status                            text NOT NULL CONSTRAINT group_booking_status_chk CHECK (status IN ('provisional', 'confirmed', 'namesPending', 'complete', 'cancelled'))
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_customer_organization (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT group_customer_organization_name_chk CHECK (char_length(name) <= 200),
    organisation_type                 text NOT NULL CONSTRAINT group_customer_organization_organisation_type_chk CHECK (organisation_type IN ('school', 'corporate', 'travelAgent', 'eventOrganizer', 'association', 'government', 'other')),
    billing_details                   jsonb,
    tax_details                       jsonb,
    updated_at                        timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_customer_organization_contact (
    group_customer_organization_id    uuid NOT NULL,
    role                              text NOT NULL,
    name                              text NOT NULL,
    email                             text,
    phone                             text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_enquiry (
    id                                uuid PRIMARY KEY NOT NULL,
    source                            text NOT NULL CONSTRAINT group_enquiry_source_chk CHECK (source IN ('website', 'salesTeam', 'campaign', 'existingCustomer', 'partner', 'manualEntry')),
    organisation_id                   uuid,
    contact                           jsonb NOT NULL,
    group_size                        integer NOT NULL,
    preferred_dates                   text[],
    requirements                      text CONSTRAINT group_enquiry_requirements_chk CHECK (char_length(requirements) <= 2000),
    sales_owner_principal_id          uuid,
    priority                          text CONSTRAINT group_enquiry_priority_chk CHECK (priority IN ('low', 'normal', 'high')),
    expected_value                    numeric(18,4),
    probability                       integer,
    expected_close_date               date,
    next_action_at                    timestamptz,
    created_by                        uuid,
    created_at                        timestamptz NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_participant (
    group_participant_list_id         uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    full_name                         text NOT NULL,
    role                              text,
    email                             text,
    phone                             text,
    date_of_birth                     date
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_participant_list (
    group_booking_id                  uuid NOT NULL,
    source                            text NOT NULL CONSTRAINT group_participant_list_source_chk CHECK (source IN ('manualEntry', 'csvExcelImport', 'customerUpload', 'api')),
    file_ref                          uuid,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_payment_milestone (
    group_payment_schedule_id         uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    due_date                          date NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    label                             text,
    status                            text NOT NULL
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_payment_schedule (
    group_booking_id                  uuid NOT NULL,
    schedule_type                     text NOT NULL CONSTRAINT group_payment_schedule_schedule_type_chk CHECK (schedule_type IN ('depositThenBalance', 'milestonePayment', 'finalBalance', 'customSchedule')),
    total                             numeric(18,4),
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 40 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_quote (
    id                                uuid PRIMARY KEY NOT NULL,
    quote_number                      text NOT NULL CONSTRAINT group_quote_quote_number_chk CHECK (char_length(quote_number) <= 50),
    version                           integer NOT NULL,
    enquiry_id                        uuid NOT NULL,
    organisation_id                   uuid,
    contact_id                        uuid,
    sales_owner_principal_id          uuid,
    package_name                      text CONSTRAINT group_quote_package_name_chk CHECK (char_length(package_name) <= 150),
    template                          text CONSTRAINT group_quote_template_chk CHECK (template IN ('schoolPackage', 'corporatePackage', 'birthdayPackage', 'vipGroupPackage', 'conferencePackage')),
    group_package_id                  uuid,
    component_types                   text[],
    quote_date                        date,
    valid_until                       date,
    visit_date                        date,
    guest_count                       integer NOT NULL,
    guest_count_deadline              timestamptz,
    standard_total                    numeric(18,4),
    total                             numeric(18,4),
    deposit_requirement               numeric(18,4),
    payment_schedule_type             text CONSTRAINT group_quote_payment_schedule_type_chk CHECK (payment_schedule_type IN ('depositThenBalance', 'milestonePayment', 'finalBalance', 'customSchedule')),
    cancellation_policy               text CONSTRAINT group_quote_cancellation_policy_chk CHECK (char_length(cancellation_policy) <= 2000),
    amendment_conditions              text CONSTRAINT group_quote_amendment_conditions_chk CHECK (char_length(amendment_conditions) <= 2000),
    operational_terms                 text CONSTRAINT group_quote_operational_terms_chk CHECK (char_length(operational_terms) <= 2000),
    delivery_formats                  text[],
    customer_request                  text CONSTRAINT group_quote_customer_request_chk CHECK (char_length(customer_request) <= 2000),
    internal_response                 text CONSTRAINT group_quote_internal_response_chk CHECK (char_length(internal_response) <= 2000),
    status                            text NOT NULL CONSTRAINT group_quote_status_chk CHECK (status IN ('draft', 'sent', 'superseded', 'accepted', 'rejected', 'expired')),
    discount_approval                 text NOT NULL DEFAULT 'notRequired' CONSTRAINT group_quote_discount_approval_chk CHECK (discount_approval IN ('notRequired', 'pending', 'approved', 'rejected', 'returnedForChange')),
    discount_percent                  numeric(18,4),
    discount_reason                   text CONSTRAINT group_quote_discount_reason_chk CHECK (char_length(discount_reason) <= 1000),
    discount_decided_by_principal_id  uuid,
    discount_decided_at               timestamptz,
    discount_decision_comment         text CONSTRAINT group_quote_discount_decision_comment_chk CHECK (char_length(discount_decision_comment) <= 1000),
    group_booking_id                  uuid,
    sent_at                           timestamptz,
    responded_at                      timestamptz,
    created_by_principal_id           uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_quote_line (
    group_quote_id                    uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid,
    component_type                    text,
    description                       text NOT NULL,
    quantity                          integer NOT NULL,
    is_complimentary                  boolean,
    standard_rate                     numeric(18,4) NOT NULL,
    group_rate                        numeric(18,4) NOT NULL,
    discount                          numeric(18,4),
    tax                               numeric(18,4),
    fee                               numeric(18,4),
    total                             numeric(18,4)
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_task (
    id                                uuid PRIMARY KEY NOT NULL,
    group_booking_id                  uuid NOT NULL,
    department                        text NOT NULL CONSTRAINT group_task_department_chk CHECK (char_length(department) <= 60),
    task                              text NOT NULL CONSTRAINT group_task_task_chk CHECK (char_length(task) <= 300),
    owner_principal_id                uuid,
    due_at                            timestamptz,
    priority                          text DEFAULT 'normal' CONSTRAINT group_task_priority_chk CHECK (priority IN ('low', 'normal', 'high', 'critical')),
    depends_on_task_id                uuid,
    status                            text NOT NULL CONSTRAINT group_task_status_chk CHECK (status IN ('open', 'inProgress', 'done', 'cancelled')),
    notes                             text CONSTRAINT group_task_notes_chk CHECK (char_length(notes) <= 2000),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_ticket_allocation (
    group_booking_id                  uuid NOT NULL,
    allocation_mode                   text NOT NULL CONSTRAINT group_ticket_allocation_allocation_mode_chk CHECK (allocation_mode IN ('individualTicket', 'bulkTicket', 'namedTicket', 'quantityBasedTicket', 'zoneAllocation')),
    keep_group_together               boolean,
    vip_allocation                    boolean,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_ticket_allocation_line (
    group_ticket_allocation_id        uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    quantity                          integer NOT NULL,
    zone_id                           uuid,
    participant_id                    uuid
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_ticket_fulfillment (
    group_booking_id                  uuid NOT NULL,
    method                            text NOT NULL CONSTRAINT group_ticket_fulfillment_method_chk CHECK (method IN ('email', 'sms', 'wallet', 'bulkPdf', 'posPrint', 'physicalCollection')),
    recipients                        text NOT NULL CONSTRAINT group_ticket_fulfillment_recipients_chk CHECK (recipients IN ('organiser', 'eachParticipant')),
    release_at                        timestamptz,
    released_at                       timestamptz,
    updated_at                        timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 27 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.group_visit_plan (
    id                                uuid PRIMARY KEY NOT NULL,
    group_booking_id                  uuid NOT NULL,
    arrival_at                        timestamptz,
    arrival_location                  text CONSTRAINT group_visit_plan_arrival_location_chk CHECK (char_length(arrival_location) <= 200),
    meeting_point                     text CONSTRAINT group_visit_plan_meeting_point_chk CHECK (char_length(meeting_point) <= 200),
    entry_gate_id                     uuid,
    departure_at                      timestamptz,
    group_leaders                     text CONSTRAINT group_visit_plan_group_leaders_chk CHECK (char_length(group_leaders) <= 500),
    contact_id                        uuid,
    ticketing_method                  text CONSTRAINT group_visit_plan_ticketing_method_chk CHECK (char_length(ticketing_method) <= 60),
    requirements                      jsonb,
    operational_owner_principal_id    uuid,
    handover_notes                    text CONSTRAINT group_visit_plan_handover_notes_chk CHECK (char_length(handover_notes) <= 4000),
    handover_attachment_ids           text[],
    handover_acknowledged_by_principal_id uuid,
    handover_acknowledged_at          timestamptz,
    check_in_status                   text NOT NULL DEFAULT 'expected' CONSTRAINT group_visit_plan_check_in_status_chk CHECK (check_in_status IN ('expected', 'partiallyArrived', 'arrived', 'noShow')),
    actual_arrival_at                 timestamptz,
    arrival_gate_id                   uuid,
    arrived_count                     integer DEFAULT 0,
    additional_guests                 integer DEFAULT 0,
    staff_leaders_count               integer DEFAULT 0,
    check_in_issues                   text[],
    checked_in_by_principal_id        uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is. Reached by: 1 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS orders.guest_credit_account (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    credit_limit                      numeric(18,4) NOT NULL,
    settlement_days_before_visit      integer,
    requires_approval                 boolean NOT NULL,
    status                            text NOT NULL CONSTRAINT guest_credit_account_status_chk CHECK (status IN ('pendingApproval', 'active'))
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
    id                                uuid PRIMARY KEY NOT NULL,
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
CREATE TABLE IF NOT EXISTS orders.member_exception (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_id                     uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT member_exception_kind_chk CHECK (kind IN ('eligibilityOverride', 'expiryExtension', 'complimentaryRenewal', 'complimentaryBenefit', 'entitlementAdjustment', 'freezeException', 'suspensionOverride', 'replacementCredential')),
    reason                            text NOT NULL CONSTRAINT member_exception_reason_chk CHECK (char_length(reason) <= 500),
    approval_request_id               uuid,
    extend_days                       integer,
    benefit_id                        uuid,
    quantity                          integer,
    new_expiry_at                     timestamptz,
    recorded_by                       uuid,
    recorded_at                       timestamptz NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.membership_activation_action (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_id                     uuid NOT NULL,
    action                            text NOT NULL CONSTRAINT membership_activation_action_action_chk CHECK (action IN ('activate', 'block', 'review', 'replace', 'link', 'escalate')),
    credential_id                     uuid,
    media_code                        text CONSTRAINT membership_activation_action_media_code_chk CHECK (char_length(media_code) <= 100),
    subject_id                        uuid,
    reason                            text CONSTRAINT membership_activation_action_reason_chk CHECK (char_length(reason) <= 500),
    membership_status                 text CONSTRAINT membership_activation_action_membership_status_chk CHECK (char_length(membership_status) <= 30),
    recorded_by                       uuid,
    recorded_at                       timestamptz NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.membership_migration (
    id                                uuid PRIMARY KEY NOT NULL,
    membership_id                     uuid NOT NULL,
    from_product_id                   uuid NOT NULL,
    target_product_id                 uuid NOT NULL,
    direction                         text NOT NULL CONSTRAINT membership_migration_direction_chk CHECK (direction IN ('upgrade', 'downgrade', 'migration')),
    effective_timing                  text NOT NULL CONSTRAINT membership_migration_effective_timing_chk CHECK (effective_timing IN ('immediate', 'nextVisit', 'nextRenewal', 'endOfCurrentTerm')),
    pro_rata                          boolean,
    pro_rata_amount                   numeric(18,4),
    order_id                          uuid,
    effective_at                      timestamptz,
    status                            text NOT NULL CONSTRAINT membership_migration_status_chk CHECK (status IN ('scheduled', 'applied')),
    created_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.membership_renewal (
    id                                uuid PRIMARY KEY NOT NULL,
    customer_membership_id            uuid NOT NULL,
    entitlement_template_id           uuid NOT NULL,
    order_id                          uuid,
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
    id                                uuid PRIMARY KEY NOT NULL,
    shift_id                          uuid NOT NULL,
    workstation_id                    uuid,
    reason                            text NOT NULL,
    note                              text,
    principal_id                      uuid NOT NULL,
    recorded_at                       timestamptz NOT NULL,
    count_this_shift                  integer
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.order_event (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
    reservation_id                    uuid,
    event_type                        text NOT NULL CONSTRAINT order_event_event_type_chk CHECK (char_length(event_type) <= 60),
    previous_state                    text CONSTRAINT order_event_previous_state_chk CHECK (char_length(previous_state) <= 40),
    new_state                         text CONSTRAINT order_event_new_state_chk CHECK (char_length(new_state) <= 40),
    channel                           text CONSTRAINT order_event_channel_chk CHECK (char_length(channel) <= 40),
    actor_principal_id                uuid,
    actor_system                      text CONSTRAINT order_event_actor_system_chk CHECK (char_length(actor_system) <= 60),
    related_entity_type               text CONSTRAINT order_event_related_entity_type_chk CHECK (char_length(related_entity_type) <= 40),
    related_entity_id                 text CONSTRAINT order_event_related_entity_id_chk CHECK (char_length(related_entity_id) <= 40),
    correlation_id                    text CONSTRAINT order_event_correlation_id_chk CHECK (char_length(correlation_id) <= 100),
    result                            text CONSTRAINT order_event_result_chk CHECK (char_length(result) <= 200),
    exception_type                    text CONSTRAINT order_event_exception_type_chk CHECK (exception_type IN ('stuckOrder', 'orphanReservation', 'paymentOrderMismatch', 'capacityMismatch', 'missingCustomerData', 'fulfillmentFailure', 'externalSynchronizationFailure')),
    scope_path                        ltree NOT NULL,
    occurred_at                       timestamptz NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.order_fee (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
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
    sales_order_id                    uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    recommendation_id                 uuid,
    performance_id                    uuid,
    booked_window                     jsonb,
    inventory_hold_id                 uuid,
    seat_ids                          text[],
    resource_hold_id                  uuid,
    attributes                        jsonb,
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
    reprint_count                     integer DEFAULT 0,
    venue_id                          uuid
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.order_line_discount (
    order_line_id                     uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    promotion_id                      uuid,
    source                            text NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    reason                            text
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.order_line_eligibility (
    order_line_id                     uuid NOT NULL,
    age_band                          text,
    age_years                         integer,
    height_band_index                 integer,
    confident_swimmer                 boolean,
    is_guardian_signed                boolean,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.order_relationship (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
    related_order_id                  uuid NOT NULL,
    relationship_type                 text NOT NULL CONSTRAINT order_relationship_relationship_type_chk CHECK (relationship_type IN ('parentOrder', 'childOrder', 'mergedInto', 'replacementOrder', 'amendedFrom', 'convertedFrom', 'reissuedFrom')),
    split_basis                       text CONSTRAINT order_relationship_split_basis_chk CHECK (split_basis IN ('ticket', 'attendee', 'product', 'orderLine', 'paymentResponsibility', 'department', 'corporateCostCenter', 'customer')),
    amount                            numeric(18,4),
    after_sale_request_id             uuid,
    created_by_principal_id           uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.order_source_channel (
    id                                uuid PRIMARY KEY NOT NULL,
    source                            text NOT NULL CONSTRAINT order_source_channel_source_chk CHECK (source IN ('b2cWeb', 'mobileApp', 'pos', 'mobileFlyingPos', 'kiosk', 'callCenter', 'boxOffice', 'b2bPortal', 'reseller', 'ota', 'api', 'administrativeBackend')),
    sub_channel                       text CONSTRAINT order_source_channel_sub_channel_chk CHECK (char_length(sub_channel) <= 60),
    channel_prefix                    text CONSTRAINT order_source_channel_channel_prefix_chk CHECK (char_length(channel_prefix) <= 10),
    numbering_rule                    text NOT NULL CONSTRAINT order_source_channel_numbering_rule_chk CHECK (numbering_rule IN ('globalSequence', 'tenantSequence', 'venueSequence', 'yearMonthPrefix', 'customPattern')),
    numbering_pattern                 text CONSTRAINT order_source_channel_numbering_pattern_chk CHECK (char_length(numbering_pattern) <= 60),
    partner_reference_type            text CONSTRAINT order_source_channel_partner_reference_type_chk CHECK (partner_reference_type IN ('otaBookingReference', 'resellerOrderId', 'erpReference', 'externalCrmReference')),
    holds_inventory                   boolean DEFAULT true,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- A tender against an order, with the rate it converted at fixed on the row (CF-37). A payment
-- reconciled next month is reconciled at the rate of the day it was taken
CREATE TABLE IF NOT EXISTS orders.payment (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
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
    provider_idempotency_key          text,
    terminal_id                       uuid,
    last_inquiry_at                   timestamptz,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.payment_allocation_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    channel                           text CONSTRAINT payment_allocation_rule_channel_chk CHECK (char_length(channel) <= 40),
    terminal_id                       uuid,
    product_id                        uuid,
    order_type                        text CONSTRAINT payment_allocation_rule_order_type_chk CHECK (char_length(order_type) <= 40),
    customer_type                     text CONSTRAINT payment_allocation_rule_customer_type_chk CHECK (char_length(customer_type) <= 40),
    allocation_level                  text NOT NULL CONSTRAINT payment_allocation_rule_allocation_level_chk CHECK (allocation_level IN ('orderLevel', 'orderLineLevel', 'productLevel', 'taxFeeComponent', 'specificTicket', 'deposit')),
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- A link a guest opens to pay for a booking taken at a till (BL-072). The link is the credential —
-- a guest holding one is anonymous, and a phone booking is exactly the case where they have not
-- registered. The expiry releases the hold, not just the link. Hangs off: reaches
-- orders.sales_order through its keys; references identity.principal, orders.reservation,
-- orders.sales_order. Reached by: 10 operat
CREATE TABLE IF NOT EXISTS orders.payment_link (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
    reservation_id                    uuid,
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
-- orders.sales_order through its keys; references orders.payment. Reached by: 1 operations read it
-- and 0 write it.
CREATE TABLE IF NOT EXISTS orders.payment_tip (
    id                                uuid PRIMARY KEY NOT NULL,
    payment_id                        uuid NOT NULL
);

-- A cash session at a workstation — opened with a float, closed with a count and a variance. Moved
-- to OrderService on 24 August because all its data is in orders
CREATE TABLE IF NOT EXISTS orders.pos_shift (
    id                                uuid PRIMARY KEY NOT NULL,
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
    cashier_reason                    text CONSTRAINT pos_shift_cashier_reason_chk CHECK (cashier_reason IN ('tillError', 'unrecordedRefund', 'miscount', 'other')),
    cashier_note                      text CONSTRAINT pos_shift_cashier_note_chk CHECK (char_length(cashier_note) <= 1000),
    held_lease_count                  integer,
    opened_at                         timestamptz NOT NULL,
    recorded_at                       timestamptz,
    suspended_at                      timestamptz,
    suspend_reason                    text CONSTRAINT pos_shift_suspend_reason_chk CHECK (char_length(suspend_reason) <= 200),
    closed_at                         timestamptz,
    closed_by_principal_id            uuid,
    recount_requested_at              timestamptz,
    recount_requested_by_principal_id uuid,
    recount_reason                    text CONSTRAINT pos_shift_recount_reason_chk CHECK (char_length(recount_reason) <= 500),
    count_number                      integer,
    synced_at                         timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.pos_shift_approval (
    pos_shift_id                      uuid NOT NULL,
    kind                              text NOT NULL,
    principal_id                      uuid NOT NULL,
    at                                timestamptz NOT NULL,
    reason                            text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.pos_shift_incident (
    pos_shift_id                      uuid NOT NULL,
    kind                              text,
    at                                timestamptz,
    principal_id                      uuid,
    note                              text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Money going back, always against a payment and never editing it. The ledger posts both
CREATE TABLE IF NOT EXISTS orders.refund (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
    batch_id                          uuid,
    fx_rate                           numeric(18,6),
    tax_reversal_entry_id             uuid,
    settle_to                         text DEFAULT 'originalTender' CONSTRAINT refund_settle_to_chk CHECK (settle_to IN ('originalTender', 'advanceBalance', 'wireTransfer', 'storeCredit')),
    fx_variance                       numeric(18,4),
    tender_currency                   text,
    tender_amount                     numeric(18,4),
    amount                            numeric(18,4) NOT NULL,
    applied_percentage                numeric(18,4),
    status                            text NOT NULL CONSTRAINT refund_status_chk CHECK (status IN ('pendingApproval', 'pendingGateway', 'completed', 'declined', 'failed')),
    reason                            text,
    requested_by_principal_id         uuid,
    secondary_principal_id            uuid,
    approved_by_principal_id          uuid,
    ledger_entry_id                   uuid,
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

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.refund_calculation_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    refund_types                      text[] NOT NULL,
    refund_destinations               text[] NOT NULL,
    percentage                        numeric(18,4),
    non_refundable_fees               text[],
    scope                             jsonb,
    updated_at                        timestamptz
);

-- When a refund is allowed and what it costs. Scoped, so a venue may be stricter than its tenant
CREATE TABLE IF NOT EXISTS orders.refund_policy (
    id                                uuid PRIMARY KEY NOT NULL,
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

-- Holds 23 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.resale_eligibility_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid,
    event_id                          uuid,
    performance_id                    uuid,
    ticket_type                       text CONSTRAINT resale_eligibility_rule_ticket_type_chk CHECK (char_length(ticket_type) <= 40),
    sales_channel                     text CONSTRAINT resale_eligibility_rule_sales_channel_chk CHECK (char_length(sales_channel) <= 40),
    customer_segment_id               uuid,
    is_resale_allowed                 boolean NOT NULL,
    required_conditions               text[],
    resale_opens_at                   timestamptz,
    resale_closes_at                  timestamptz,
    blackout_from                     timestamptz,
    blackout_to                       timestamptz,
    minimum_ownership_hours           integer,
    resale_immediately_after_purchase boolean DEFAULT false,
    maximum_resale_attempts           integer,
    maximum_listings_per_customer     integer,
    is_identity_verification_required boolean DEFAULT false,
    original_purchaser_only           boolean DEFAULT false,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- What a resale costs and how high it may be priced. orders.resale_listing stored
-- seller_fee_percent, buyer_fee_percent and price_cap_percent on every listing with nothing
-- producing them, so two listings a minute apart could carry different commercials and record no
-- reason. The listing keeps its columns as the snapshot — the same rule-and-record split
-- payments.fee_rule and orders.order_fee already u
CREATE TABLE IF NOT EXISTS orders.resale_fee_policy (
    id                                uuid PRIMARY KEY NOT NULL,
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
    entitlement_id                    uuid NOT NULL,
    seller_subject_id                 uuid NOT NULL,
    ask_price                         numeric(18,4) NOT NULL,
    price_cap_percent                 numeric(18,4),
    seller_fee_percent                numeric(18,4),
    buyer_fee_percent                 numeric(18,4),
    status                            text NOT NULL CONSTRAINT resale_listing_status_chk CHECK (status IN ('pendingReview', 'listed', 'reserved', 'sold', 'withdrawn', 'expired', 'rejected')),
    listed_at                         timestamptz,
    sold_to_subject_id                uuid,
    review_reasons                    text[],
    moderated_by_principal_id         uuid,
    moderated_at                      timestamptz,
    moderation_reason                 text CONSTRAINT resale_listing_moderation_reason_chk CHECK (char_length(moderation_reason) <= 1000),
    payout_status                     text CONSTRAINT resale_listing_payout_status_chk CHECK (payout_status IN ('pending', 'held', 'paid', 'failed')),
    scope_path                        ltree NOT NULL
);

-- Holds 35 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.resale_marketplace_config (
    id                                uuid PRIMARY KEY NOT NULL,
    marketplace_name                  text NOT NULL CONSTRAINT resale_marketplace_config_marketplace_name_chk CHECK (char_length(marketplace_name) <= 150),
    pricing_mode                      text NOT NULL CONSTRAINT resale_marketplace_config_pricing_mode_chk CHECK (pricing_mode IN ('faceValueOnly', 'fixedPrice', 'sellerSelectedPrice', 'cappedPrice', 'operatorControlled', 'aiRecommendedPrice')),
    maximum_discount_percent          numeric(18,4),
    seller_can_edit_price             boolean DEFAULT true,
    maximum_price_changes             integer,
    minimum_minutes_between_price_changes integer,
    moderation_mode                   text NOT NULL DEFAULT 'automatic' CONSTRAINT resale_marketplace_config_moderation_mode_chk CHECK (moderation_mode IN ('automatic', 'riskBased', 'manual')),
    review_triggers                   text[],
    expiry_rule                       text DEFAULT 'atEventStart' CONSTRAINT resale_marketplace_config_expiry_rule_chk CHECK (expiry_rule IN ('xMinutesBeforeEvent', 'xHoursBeforeEvent', 'atEventStart', 'atConfiguredDate')),
    expiry_offset                     integer,
    withdrawal_policy                 text DEFAULT 'sellerCannotWithdrawWhileReserved' CONSTRAINT resale_marketplace_config_withdrawal_policy_chk CHECK (withdrawal_policy IN ('sellerCanWithdrawAnytime', 'sellerCannotWithdrawWhileReserved')),
    maximum_withdrawals               integer,
    cancellation_fee                  numeric(18,4),
    checkout_hold_minutes             integer DEFAULT 10,
    is_buyer_identity_verification_required boolean DEFAULT false,
    settlement_timing                 text DEFAULT 'afterAccessValidation' CONSTRAINT resale_marketplace_config_settlement_timing_chk CHECK (settlement_timing IN ('immediatelyAfterResale', 'xDaysAfterResale', 'afterEventCompletion', 'xDaysAfterEvent', 'afterAccessValidation', 'operatorDefinedSettlementCycle')),
    settlement_delay_days             integer,
    minimum_payout_threshold          numeric(18,4),
    customer_terms                    text CONSTRAINT resale_marketplace_config_customer_terms_chk CHECK (char_length(customer_terms) <= 20000),
    seller_terms                      text CONSTRAINT resale_marketplace_config_seller_terms_chk CHECK (char_length(seller_terms) <= 20000),
    buyer_terms                       text CONSTRAINT resale_marketplace_config_buyer_terms_chk CHECK (char_length(buyer_terms) <= 20000),
    terms_version                     text CONSTRAINT resale_marketplace_config_terms_version_chk CHECK (char_length(terms_version) <= 20),
    disclosures                       text CONSTRAINT resale_marketplace_config_disclosures_chk CHECK (char_length(disclosures) <= 4000),
    resale_ticket_label               text CONSTRAINT resale_marketplace_config_resale_ticket_label_chk CHECK (char_length(resale_ticket_label) <= 60),
    deployment_model                  text DEFAULT 'ticvaiHostedWhiteLabel' CONSTRAINT resale_marketplace_config_deployment_model_chk CHECK (deployment_model IN ('embeddedWhiteLabel', 'ticvaiHostedWhiteLabel', 'headlessApi')),
    navigation                        text[],
    authentication_method             text DEFAULT 'customerAccount' CONSTRAINT resale_marketplace_config_authentication_method_chk CHECK (authentication_method IN ('customerAccount', 'sso', 'passwordlessLogin', 'otp', 'appAuthentication')),
    branding                          jsonb,
    domain                            text CONSTRAINT resale_marketplace_config_domain_chk CHECK (char_length(domain) <= 253),
    languages                         text[],
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.resale_recommendation (
    id                                uuid PRIMARY KEY NOT NULL,
    recommendation_type               text NOT NULL CONSTRAINT resale_recommendation_recommendation_type_chk CHECK (recommendation_type IN ('pricing', 'demandPrediction', 'listing', 'sellerRisk', 'expiry', 'marketplaceOptimisation', 'anomaly')),
    event_id                          uuid,
    resale_listing_id                 uuid,
    recommendation                    text NOT NULL CONSTRAINT resale_recommendation_recommendation_chk CHECK (char_length(recommendation) <= 2000),
    recommended_value                 jsonb,
    decision                          text CONSTRAINT resale_recommendation_decision_chk CHECK (decision IN ('accept', 'modify', 'ignore')),
    applied_value                     jsonb,
    decided_by_principal_id           uuid,
    decided_at                        timestamptz,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.resale_settlement (
    id                                uuid PRIMARY KEY NOT NULL,
    resale_listing_id                 uuid NOT NULL,
    seller_subject_id                 uuid NOT NULL,
    listing_price                     numeric(18,4) NOT NULL,
    seller_fee                        numeric(18,4) NOT NULL,
    processing_fee                    numeric(18,4),
    tax                               numeric(18,4),
    adjustments                       numeric(18,4),
    seller_proceeds                   numeric(18,4) NOT NULL,
    payout_method                     text CONSTRAINT resale_settlement_payout_method_chk CHECK (payout_method IN ('originalPaymentMethod', 'bankTransfer', 'wallet')),
    settlement_batch                  text CONSTRAINT resale_settlement_settlement_batch_chk CHECK (char_length(settlement_batch) <= 100),
    expected_payout_date              date,
    status                            text NOT NULL CONSTRAINT resale_settlement_status_chk CHECK (status IN ('pending', 'scheduled', 'onHold', 'paid', 'failed', 'reversed')),
    hold_reason                       text CONSTRAINT resale_settlement_hold_reason_chk CHECK (hold_reason IN ('manualHold', 'complianceHold', 'refundDisputeHold')),
    paid_at                           timestamptz,
    failure_reason                    text CONSTRAINT resale_settlement_failure_reason_chk CHECK (char_length(failure_reason) <= 500),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- A held place that is not yet a sale — a table, a cabana, a slot
CREATE TABLE IF NOT EXISTS orders.reservation (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    subject_id                        uuid,
    status                            text NOT NULL CONSTRAINT reservation_status_chk CHECK (status IN ('held', 'converted', 'expired', 'cancelled')),
    expires_at                        timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL,
    converted_order_id                uuid
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.reservation_hold_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    hold_type                         text NOT NULL CONSTRAINT reservation_hold_policy_hold_type_chk CHECK (hold_type IN ('cartHold', 'checkoutHold', 'agentReservation', 'groupReservation', 'b2bReservation', 'corporateReservation', 'manualHold', 'paymentHold', 'seatHold', 'inventoryHold')),
    channel                           text CONSTRAINT reservation_hold_policy_channel_chk CHECK (char_length(channel) <= 40),
    product_id                        uuid,
    event_id                          uuid,
    performance_id                    uuid,
    ticket_type                       text CONSTRAINT reservation_hold_policy_ticket_type_chk CHECK (char_length(ticket_type) <= 40),
    customer_segment_id               uuid,
    hold_duration_minutes             integer NOT NULL,
    locked_capacity                   text[],
    on_expiry                         text[],
    is_extension_allowed              boolean DEFAULT false,
    maximum_extensions                integer,
    extension_duration_minutes        integer,
    extension_permission              text CONSTRAINT reservation_hold_policy_extension_permission_chk CHECK (char_length(extension_permission) <= 60),
    extension_requires_approval       boolean DEFAULT false,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.reservation_line (
    reservation_id                    uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    variant_id                        uuid NOT NULL,
    recommendation_id                 uuid,
    performance_id                    uuid,
    booked_window                     jsonb,
    inventory_hold_id                 uuid,
    seat_ids                          text[],
    resource_hold_id                  uuid,
    attributes                        jsonb,
    quantity                          integer NOT NULL,
    quoted_unit_price                 numeric(18,4) NOT NULL,
    holder_name                       text,
    data_mask_values                  jsonb
);

-- The sale. What was bought, by whom, through which channel, at what scope. Every payment, refund,
-- entitlement and ledger posting reaches back to a row here
CREATE TABLE IF NOT EXISTS orders.sales_order (
    id                                uuid PRIMARY KEY NOT NULL,
    order_number                      text,
    channel                           text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    status                            text NOT NULL CONSTRAINT sales_order_status_chk CHECK (status IN ('pending', 'held', 'paid', 'partiallyPaid', 'completed', 'voided', 'refunded', 'partiallyRefunded', 'failed')),
    gross_amount                      numeric(18,4) NOT NULL,
    tax_amount                        numeric(18,4) NOT NULL,
    net_amount                        numeric(18,4) NOT NULL,
    refunded_amount                   numeric(18,4),
    charge_currency                   text,
    charge_fx_rate                    numeric(18,6),
    charge_fx_rate_id                 uuid,
    charge_total                      numeric(18,4),
    charge_rate_locked_until          timestamptz,
    total_price_variance              numeric(18,4),
    principal_id                      uuid,
    workstation_id                    uuid,
    shift_id                          uuid,
    subject_id                        uuid,
    hold_label                        text CONSTRAINT sales_order_hold_label_chk CHECK (char_length(hold_label) <= 60),
    held_until                        timestamptz,
    created_at                        timestamptz NOT NULL,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.status_transition_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    entity                            text NOT NULL CONSTRAINT status_transition_rule_entity_chk CHECK (entity IN ('order', 'reservation')),
    from_status                       text NOT NULL CONSTRAINT status_transition_rule_from_status_chk CHECK (char_length(from_status) <= 40),
    to_status                         text NOT NULL CONSTRAINT status_transition_rule_to_status_chk CHECK (char_length(to_status) <= 40),
    required_conditions               text CONSTRAINT status_transition_rule_required_conditions_chk CHECK (char_length(required_conditions) <= 1000),
    allowed_permission                text CONSTRAINT status_transition_rule_allowed_permission_chk CHECK (char_length(allowed_permission) <= 60),
    is_system_controlled              boolean DEFAULT false,
    integration_requirement           text CONSTRAINT status_transition_rule_integration_requirement_chk CHECK (char_length(integration_requirement) <= 200),
    notification                      text CONSTRAINT status_transition_rule_notification_chk CHECK (char_length(notification) <= 200),
    audit_requirement                 text CONSTRAINT status_transition_rule_audit_requirement_chk CHECK (char_length(audit_requirement) <= 200),
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- A hold against any stored-value instrument (CF-126). Two-phase spend for all six, where only the
-- retail wallet had it — a guest with 200 game credits starting a play the machine then failed had
-- no held balance Hangs off: reaches orders.sales_order through its keys. Reached by: 4 operations
-- read it and 6 write it; written by 3 contracts — marketing-crm, orders, resources.
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
-- not a code change. Hangs off: reaches orders.sales_order through its keys. Reached by: 7
-- operations read it and 4 write it; 1 tables reference it.
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
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid NOT NULL,
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

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.till_shift_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    require_open_approval             boolean DEFAULT false,
    opening_float_tolerance           numeric(18,4),
    is_deposit_box_required           boolean DEFAULT true,
    is_bag_number_required            boolean DEFAULT false,
    require_close_approval            boolean DEFAULT false,
    auto_close_after_hours            integer DEFAULT 14,
    no_sale_alert_count               integer DEFAULT 10,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.upgrade (
    id                                uuid PRIMARY KEY NOT NULL,
    number                            text NOT NULL CONSTRAINT upgrade_number_chk CHECK (char_length(number) <= 50),
    order_id                          uuid NOT NULL,
    original_order_line_id            uuid NOT NULL,
    new_order_line_id                 uuid,
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

-- Holds 47 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS orders.upgrade_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT upgrade_rule_name_chk CHECK (char_length(name) <= 150),
    code                              text NOT NULL CONSTRAINT upgrade_rule_code_chk CHECK (char_length(code) <= 50),
    transaction_type                  text NOT NULL CONSTRAINT upgrade_rule_transaction_type_chk CHECK (transaction_type IN ('upgrade', 'downgrade', 'exchange', 'conversion', 'personTypeConversion', 'productConversion')),
    from_product_id                   uuid NOT NULL,
    from_variant_id                   uuid,
    to_product_id                     uuid NOT NULL,
    to_variant_id                     uuid,
    event_id                          uuid,
    performance_id                    uuid,
    direction                         text NOT NULL CONSTRAINT upgrade_rule_direction_chk CHECK (direction IN ('oneWay', 'bidirectional')),
    is_chained_upgrade_allowed        boolean DEFAULT false,
    allowed_channels                  text[],
    customer_segment_id               uuid,
    priority                          integer DEFAULT 0,
    eligible_ticket_statuses          text[],
    permitted_windows                 text[],
    is_supervisor_exception_allowed   boolean DEFAULT false,
    original_ticket_treatment         text DEFAULT 'supersede' CONSTRAINT upgrade_rule_original_ticket_treatment_chk CHECK (original_ticket_treatment IN ('invalidate', 'supersede', 'retainForHistory', 'partiallyRetainEntitlement')),
    conversion_type                   text CONSTRAINT upgrade_rule_conversion_type_chk CHECK (conversion_type IN ('childAdult', 'juniorAdult', 'seniorAdult', 'residentTourist', 'standardMember', 'customPersonTypes')),
    entitlement_treatment             text CONSTRAINT upgrade_rule_entitlement_treatment_chk CHECK (entitlement_treatment IN ('retained', 'replaced', 'added', 'removed', 'alreadyConsumed')),
    target_requirements               text[],
    financial_method                  text NOT NULL CONSTRAINT upgrade_rule_financial_method_chk CHECK (financial_method IN ('fullDifference', 'fixedUpgradeFee', 'percentageUpgrade', 'proRata', 'creditBased', 'noCredit', 'complimentary')),
    price_source                      text DEFAULT 'currentSellingPrice' CONSTRAINT upgrade_rule_price_source_chk CHECK (price_source IN ('currentSellingPrice', 'originalDatePrice', 'upgradeSpecificRate', 'contractedRate', 'membershipRate', 'fixedUpgradePrice')),
    dynamic_price_treatment           text CONSTRAINT upgrade_rule_dynamic_price_treatment_chk CHECK (dynamic_price_treatment IN ('currentDynamicPrice', 'protectedUpgradeRate', 'configuredRate')),
    upgrade_amount                    numeric(18,4),
    upgrade_percent                   numeric(18,4),
    carry_forward_discounts           text[],
    approval_requirement              text CONSTRAINT upgrade_rule_approval_requirement_chk CHECK (char_length(approval_requirement) <= 200),
    pro_rata_method                   text CONSTRAINT upgrade_rule_pro_rata_method_chk CHECK (pro_rata_method IN ('timeBased', 'usageBased', 'valueBased', 'entitlementBased', 'fixedCredit')),
    fixed_credit_amount               numeric(18,4),
    maximum_credit_percent            numeric(18,4),
    minimum_upgrade_amount            numeric(18,4),
    credit_expiry_days                integer,
    non_creditable_components         text[],
    exclude_fees_from_credit          boolean DEFAULT true,
    tax_treatment                     text CONSTRAINT upgrade_rule_tax_treatment_chk CHECK (char_length(tax_treatment) <= 60),
    negative_difference_treatment     text DEFAULT 'noRefund' CONSTRAINT upgrade_rule_negative_difference_treatment_chk CHECK (negative_difference_treatment IN ('noRefund', 'refundDifference', 'walletCredit', 'voucherCredit', 'supervisorApproval')),
    credential_treatment              text DEFAULT 'regenerateQr' CONSTRAINT upgrade_rule_credential_treatment_chk CHECK (credential_treatment IN ('regenerateQr', 'invalidateOldQr', 'preserveExistingCredential')),
    generated_documents               text[],
    owner_principal_id                uuid,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    is_active                         boolean NOT NULL,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- One reminder per booking, set by the guest. GST-018 Add to Calendar / Reminders had nothing
-- behind its reminders half. A row says how long before each session to remind and on which
-- channels; the sender skips any channel the guest has since withdrawn consent for, because a
-- reminder is not a reason to message somebody who said no
CREATE TABLE IF NOT EXISTS orders.visit_reminder (
    id                                uuid PRIMARY KEY NOT NULL,
    order_id                          uuid,
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
    entitlement_id                    uuid NOT NULL,
    platform                          text NOT NULL CONSTRAINT wallet_pass_platform_chk CHECK (platform IN ('apple', 'google')),
    serial_number                     text NOT NULL,
    authentication_token              text,
    status                            text NOT NULL CONSTRAINT wallet_pass_status_chk CHECK (status IN ('issued', 'updated', 'voided', 'expired')),
    last_pushed_at                    timestamptz,
    device_registrations              integer,
    scope_path                        ltree NOT NULL
);

