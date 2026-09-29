-- ledger — 20 tables
-- **Derived. Do not hand-edit.**

-- A line in the chart of accounts, denominated in its own currency. One of four tables that
-- genuinely differ from their region — a group consolidating across jurisdictions holds accounts
-- in several
CREATE TABLE IF NOT EXISTS ledger.account (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT account_code_chk CHECK (char_length(code) <= 64),
    external_code                     text,
    is_suspense                       boolean DEFAULT false,
    sub_type                          text,
    tags                              text[],
    notes                             text,
    name                              text NOT NULL CONSTRAINT account_name_chk CHECK (char_length(name) <= 200),
    type                              text NOT NULL CONSTRAINT account_type_chk CHECK (type IN ('asset', 'liability', 'equity', 'revenue', 'expense')),
    parent_id                         uuid,
    legal_entity_id                   uuid NOT NULL,
    currency                          text,
    is_postable                       boolean NOT NULL,
    is_active                         boolean NOT NULL,
    balance                           numeric(18,4)
);

-- Which account a kind of transaction posts to. Configuration, not a posting
CREATE TABLE IF NOT EXISTS ledger.account_mapping (
    event_type                        text NOT NULL CONSTRAINT account_mapping_event_type_chk CHECK (event_type IN ('ticketRevenue', 'fnbRevenue', 'retailRevenue', 'rentalRevenue', 'taxPayable', 'cashReceived', 'cardReceived', 'walletReceived', 'refundIssued', 'voidReversal', 'deferredRevenue', 'recognisedRevenue', 'breakageRevenue', 'priceVariance', 'cashOverShort', 'settlementFee', 'settlementClearing', 'gameCreditLoaded', 'pointsAccrued')),
    debit_account_id                  uuid NOT NULL,
    credit_account_id                 uuid NOT NULL,
    venue_id                          uuid,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Where a cost lands. Referenced by seven tables and operated on by two, because it is written
-- once and read constantly
CREATE TABLE IF NOT EXISTS ledger.cost_center (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    parent_id                         uuid,
    venue_id                          uuid,
    is_active                         boolean
);

-- Money taken before the sale is complete (BL-139). Not deferred revenue — that is a sold
-- entitlement not yet consumed, and the sale happened
CREATE TABLE IF NOT EXISTS ledger.deposit (
    id                                uuid PRIMARY KEY NOT NULL,
    amount                            numeric(18,4) NOT NULL,
    reason                            text NOT NULL CONSTRAINT deposit_reason_chk CHECK (reason IN ('reservation', 'rental', 'event', 'damageBond', 'other')),
    status                            text NOT NULL CONSTRAINT deposit_status_chk CHECK (status IN ('held', 'convertedToRevenue', 'returned', 'forfeited', 'partiallyForfeited')),
    subject_id                        uuid,
    order_id                          text,
    booking_id                        uuid,
    refundable_until                  timestamptz,
    liability_account_id              uuid,
    settled_at                        timestamptz
);

-- What an event cost against what it earned (BL-049). Profitability is revenue minus committed
-- cost — an event three weeks out with purchase orders raised has spent it
CREATE TABLE IF NOT EXISTS ledger.event_budget (
    id                                uuid PRIMARY KEY NOT NULL,
    event_id                          uuid NOT NULL,
    cost_center_id                    uuid,
    budgeted_revenue                  numeric(18,4) NOT NULL,
    budgeted_cost                     numeric(18,4) NOT NULL,
    actual_revenue                    numeric(18,4),
    committed_cost                    numeric(18,4),
    actual_cost                       numeric(18,4)
);

-- A window that closes. Once closed, corrections post to the next one
CREATE TABLE IF NOT EXISTS ledger.fiscal_period (
    id                                uuid PRIMARY KEY NOT NULL,
    legal_entity_id                   uuid NOT NULL,
    name                              text NOT NULL,
    start_date                        date NOT NULL,
    end_date                          date NOT NULL,
    status                            text NOT NULL CONSTRAINT fiscal_period_status_chk CHECK (status IN ('open', 'closing', 'closed')),
    closed_by_principal_id            uuid,
    closed_at                         timestamptz,
    approval_request_id               uuid
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ledger.fiscal_period_event (
    fiscal_period_id                  uuid NOT NULL,
    action                            text NOT NULL,
    reason                            text,
    principal_id                      uuid NOT NULL,
    approver_principal_id             uuid,
    occurred_at                       timestamptz NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS ledger.fx_provider_assignment (
    purpose                           text NOT NULL CONSTRAINT fx_provider_assignment_purpose_chk CHECK (purpose IN ('tender', 'interEntity', 'reporting', 'revaluation')),
    source                            text NOT NULL CONSTRAINT fx_provider_assignment_source_chk CHECK (source IN ('manual', 'uaeCentralBank', 'ecb', 'openExchangeRates', 'cardScheme', 'provider')),
    credential_ref                    text,
    schedule                          text,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- configured rates with effective windows. A rate change is a new row; the old is never edited
-- Hangs off: reaches ledger.account through its keys; references identity.principal,
-- platform.scope. Reached by: 14 operations read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS ledger.fx_rate (
    id                                uuid PRIMARY KEY,
    from_currency                     text NOT NULL,
    to_currency                       text NOT NULL,
    rate                              numeric(18,6) NOT NULL,
    purpose                           text NOT NULL CONSTRAINT fx_rate_purpose_chk CHECK (purpose IN ('tender', 'interEntity', 'reporting', 'revaluation')),
    source                            text,
    effective_from                    timestamptz NOT NULL,
    effective_to                      timestamptz,
    set_by_principal_id               uuid,
    note                              text CONSTRAINT fx_rate_note_chk CHECK (char_length(note) <= 500),
    provider_reference                text,
    fetched_at                        timestamptz,
    region_id                         uuid NOT NULL
);

-- what one legal entity owes another after a cross-region redemption Hangs off: reaches
-- ledger.account through its keys; references access.entitlement, ledger.legal_entity,
-- orders.sales_order. Reached by: 5 operations read it and 3 write it.
CREATE TABLE IF NOT EXISTS ledger.inter_entity_obligation (
    id                                uuid PRIMARY KEY NOT NULL,
    from_legal_entity_id              uuid NOT NULL,
    to_legal_entity_id                uuid NOT NULL,
    entitlement_id                    text,
    order_id                          text,
    arising_amount                    numeric(18,4) NOT NULL,
    rate_applied                      numeric(18,6),
    arising_at                        timestamptz NOT NULL,
    status                            text NOT NULL CONSTRAINT inter_entity_obligation_status_chk CHECK (status IN ('outstanding', 'settled', 'disputed')),
    settled_at                        timestamptz,
    settlement_rate                   numeric(18,6),
    fx_movement                       numeric(18,4)
);

-- A balanced set of postings. Append-only: a correction is another entry, never an edit, which is
-- what makes a period closeable
CREATE TABLE IF NOT EXISTS ledger.journal_entry (
    id                                text PRIMARY KEY NOT NULL,
    entry_number                      text NOT NULL,
    fiscal_period_id                  uuid NOT NULL,
    status                            text NOT NULL CONSTRAINT journal_entry_status_chk CHECK (status IN ('draft', 'pendingApproval', 'posted', 'reversed')),
    source                            text NOT NULL CONSTRAINT journal_entry_source_chk CHECK (source IN ('manual', 'order', 'refund', 'void', 'shift', 'recognition', 'settlement', 'variance', 'reversal', 'writeOff')),
    source_id                         text,
    description                       text NOT NULL,
    reference                         text,
    total_debit                       numeric(18,4) NOT NULL,
    total_credit                      numeric(18,4) NOT NULL,
    posted_by_principal_id            uuid,
    approved_by_principal_id          uuid,
    reversal_of_entry_id              text,
    reversed_by_entry_id              text,
    reversal_reason                   text,
    rejection_reason                  text,
    rejected_by_principal_id          uuid,
    rejected_at                       timestamptz,
    created_at                        timestamptz NOT NULL,
    posted_at                         timestamptz
);

-- One side of a posting. Entries balance; lines do not
CREATE TABLE IF NOT EXISTS ledger.journal_line (
    journal_entry_id                  text NOT NULL,
    account_id                        uuid NOT NULL,
    debit                             numeric(18,4) NOT NULL,
    credit                            numeric(18,4) NOT NULL,
    venue_id                          uuid,
    cost_center_id                    uuid,
    description                       text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Who the money belongs to. A tenant may trade through several, which is why inter-entity rates
-- exist
CREATE TABLE IF NOT EXISTS ledger.legal_entity (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT legal_entity_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT legal_entity_name_chk CHECK (char_length(name) <= 200),
    country_code                      text NOT NULL,
    currency                          text NOT NULL,
    currency_scale                    integer NOT NULL,
    tax_registration_number           text,
    fiscal_year_start_month           integer NOT NULL,
    region_ids                        text[],
    is_active                         boolean,
    scope_path                        ltree NOT NULL
);

-- One side of a double-entry movement. Renamed from entry, which sat beside journal_entry and
-- journal_line — three things called entry in one schema is a schema nobody reads twice. Hangs
-- off: reaches ledger.account through its keys; references ledger.account, ledger.cost_center,
-- ledger.journal_entry. Reached by: 7 operations read it and 10 write it; written by 3 contracts —
-- finance, orders, shift.
CREATE TABLE IF NOT EXISTS ledger.posting (
    id                                text PRIMARY KEY NOT NULL,
    journal_entry_id                  text NOT NULL,
    account_id                        uuid NOT NULL,
    account_code                      text,
    debit                             numeric(18,4) NOT NULL,
    credit                            numeric(18,4) NOT NULL,
    venue_id                          uuid,
    cost_center_id                    uuid,
    source                            text CONSTRAINT posting_source_chk CHECK (source IN ('manual', 'order', 'refund', 'void', 'shift', 'recognition', 'settlement', 'variance', 'reversal', 'writeOff')),
    source_id                         text,
    description                       text,
    posted_at                         timestamptz NOT NULL
);

-- What was expected against what was invoiced. Where a three-way match would post if it existed
CREATE TABLE IF NOT EXISTS ledger.price_variance (
    id                                text PRIMARY KEY NOT NULL,
    order_id                          text NOT NULL,
    order_line_id                     text NOT NULL,
    venue_id                          uuid NOT NULL,
    variant_id                        uuid,
    quoted_price                      numeric(18,4) NOT NULL,
    server_price                      numeric(18,4) NOT NULL,
    variance                          numeric(18,4) NOT NULL,
    catalogue_bundle_version          text,
    is_exception                      boolean NOT NULL,
    review_status                     text CONSTRAINT price_variance_review_status_chk CHECK (review_status IN ('notRequired', 'pendingReview', 'reviewed')),
    review_outcome                    text CONSTRAINT price_variance_review_outcome_chk CHECK (review_outcome IN ('accepted', 'investigated', 'catalogueCorrected')),
    reviewed_by_principal_id          uuid,
    journal_entry_id                  text,
    occurred_at                       timestamptz NOT NULL
);

-- When deferred revenue becomes revenue — a membership sold in March and earned across a year
CREATE TABLE IF NOT EXISTS ledger.recognition_schedule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT recognition_schedule_name_chk CHECK (char_length(name) <= 200),
    method                            text NOT NULL CONSTRAINT recognition_schedule_method_chk CHECK (method IN ('immediate', 'onRedemption', 'straightLine', 'perVisit', 'onExpiry')),
    priority                          integer DEFAULT 100,
    recognition_site                  text DEFAULT 'sale' CONSTRAINT recognition_schedule_recognition_site_chk CHECK (recognition_site IN ('sale', 'admission', 'consumption')),
    frequency                         text DEFAULT 'onPeriodClose' CONSTRAINT recognition_schedule_frequency_chk CHECK (frequency IN ('daily', 'weekly', 'monthly', 'onEvent', 'onPeriodClose')),
    revalidate_on_validity_change     boolean DEFAULT true,
    product_kinds                     text[] NOT NULL,
    deferred_account_id               uuid,
    recognised_account_id             uuid,
    breakage_account_id               uuid,
    no_show_trigger                   text CONSTRAINT recognition_schedule_no_show_trigger_chk CHECK (no_show_trigger IN ('performanceEnd', 'validityEnd', 'none')),
    no_show_account_id                uuid,
    breakage_after_days               integer,
    is_active                         boolean
);

-- Money actually arriving from a provider, matched against what was taken
CREATE TABLE IF NOT EXISTS ledger.settlement (
    id                                uuid PRIMARY KEY NOT NULL,
    currency_code                     text,
    provider_name                     text NOT NULL,
    venue_id                          uuid,
    period_start                      date NOT NULL,
    period_end                        date NOT NULL,
    file_reference                    uuid,
    format                            text CONSTRAINT settlement_format_chk CHECK (format IN ('csv', 'fixedWidth', 'xml', 'json')),
    status                            text NOT NULL CONSTRAINT settlement_status_chk CHECK (status IN ('ingesting', 'parsing', 'matching', 'matched', 'hasExceptions', 'resolved', 'failed')),
    line_count                        integer,
    matched_count                     integer,
    exception_count                   integer,
    provider_gross                    numeric(18,4),
    provider_fees                     numeric(18,4),
    provider_net                      numeric(18,4),
    ledger_gross                      numeric(18,4),
    difference                        numeric(18,4),
    ingested_at                       timestamptz NOT NULL,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- A settlement that did not match. The queue somebody works, not an error log
CREATE TABLE IF NOT EXISTS ledger.settlement_exception (
    id                                uuid PRIMARY KEY NOT NULL,
    settlement_id                     uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT settlement_exception_kind_chk CHECK (kind IN ('unmatchedInProvider', 'unmatchedInLedger', 'amountMismatch', 'duplicateInProvider', 'feeUnexplained')),
    provider_reference                text,
    payment_id                        text,
    amount                            numeric(18,4) NOT NULL,
    expected_amount                   numeric(18,4),
    resolution                        text,
    note                              text,
    resolved_by_principal_id          uuid,
    resolved_at                       timestamptz
);

-- A rate and its rules, scoped to a region
CREATE TABLE IF NOT EXISTS ledger.tax_code (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT tax_code_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT tax_code_name_chk CHECK (char_length(name) <= 200),
    country_code                      text NOT NULL,
    applies_to                        text[],
    rate                              numeric(18,4) NOT NULL,
    compound_on_tax_code_id           uuid,
    is_inclusive                      boolean,
    account_id                        uuid,
    effective_from                    date NOT NULL,
    effective_to                      date,
    is_active                         boolean NOT NULL
);

-- Who does not pay, and on what evidence. Hangs off: reaches ledger.account through its keys;
-- references ledger.tax_code. Reached by: 3 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS ledger.tax_exemption (
    id                                uuid PRIMARY KEY NOT NULL,
    scope                             text NOT NULL CONSTRAINT tax_exemption_scope_chk CHECK (scope IN ('account', 'productKind', 'channel', 'legalEntity')),
    scope_ref                         text,
    tax_code_id                       uuid NOT NULL,
    reason                            text NOT NULL CONSTRAINT tax_exemption_reason_chk CHECK (char_length(reason) <= 500),
    exemption_type                    text CONSTRAINT tax_exemption_exemption_type_chk CHECK (exemption_type IN ('diplomatic', 'export', 'businessToBusiness', 'charity', 'governmentEntity', 'freeZone', 'zeroRated', 'other')),
    certificate_reference             text CONSTRAINT tax_exemption_certificate_reference_chk CHECK (char_length(certificate_reference) <= 100),
    evidence_document_id              uuid,
    verification_status               text DEFAULT 'pending' CONSTRAINT tax_exemption_verification_status_chk CHECK (verification_status IN ('notRequired', 'pending', 'verified', 'rejected', 'expired')),
    verified_by                       uuid,
    verified_at                       timestamptz,
    verification_note                 text CONSTRAINT tax_exemption_verification_note_chk CHECK (char_length(verification_note) <= 500),
    valid_from                        date,
    valid_to                          date
);

