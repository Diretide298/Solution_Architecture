-- ledger — 18 tables
-- **Derived. Do not hand-edit.**

-- A line in the chart of accounts, denominated in its own currency. One of four tables that
-- genuinely differ from their region — a group consolidating across jurisdictions holds accounts
-- in several
CREATE TABLE IF NOT EXISTS ledger.account (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    external_code                     text,
    is_suspense                       boolean,
    sub_type                          text,
    tags                              text[],
    notes                             text,
    name                              text NOT NULL,
    type                              text NOT NULL,
    parent_id                         uuid,
    legal_entity_id                   uuid NOT NULL,
    currency                          text,
    is_postable                       boolean NOT NULL,
    is_active                         boolean NOT NULL,
    balance                           numeric(18,4)
);

-- Which account a kind of transaction posts to. Configuration, not a posting
CREATE TABLE IF NOT EXISTS ledger.account_mapping (
    event_type                        text NOT NULL,
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
    reason                            text NOT NULL,
    status                            text NOT NULL,
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
    status                            text NOT NULL,
    closed_by_principal_id            uuid,
    closed_at                         timestamptz
);

-- configured rates with effective windows. A rate change is a new row; the old is never edited
-- Hangs off: reaches ledger.account through its keys; references identity.principal,
-- platform.scope. Reached by: 14 operations read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS ledger.fx_rate (
    id                                uuid PRIMARY KEY,
    from_currency                     text NOT NULL,
    to_currency                       text NOT NULL,
    rate                              numeric(18,4) NOT NULL,
    purpose                           text NOT NULL,
    source                            text,
    effective_from                    timestamptz NOT NULL,
    effective_to                      timestamptz,
    set_by_principal_id               uuid,
    provider_reference                text,
    fetched_at                        timestamptz,
    region_id                         uuid NOT NULL
);

-- what one legal entity owes another after a cross-region redemption Hangs off: reaches
-- ledger.account through its keys; references access.entitlement, ledger.legal_entity,
-- orders.sales_order. Reached by: 5 operations read it and 3 write it.
CREATE TABLE IF NOT EXISTS ledger.inter_entity_obligation (
    id                                text PRIMARY KEY NOT NULL,
    from_legal_entity_id              uuid NOT NULL,
    to_legal_entity_id                uuid NOT NULL,
    entitlement_id                    text,
    order_id                          text,
    arising_amount                    numeric(18,4) NOT NULL,
    rate_applied                      numeric(18,4),
    arising_at                        timestamptz NOT NULL,
    status                            text NOT NULL,
    settled_at                        timestamptz,
    settlement_rate                   numeric(18,4),
    fx_movement                       numeric(18,4)
);

-- A balanced set of postings. Append-only: a correction is another entry, never an edit, which is
-- what makes a period closeable
CREATE TABLE IF NOT EXISTS ledger.journal_entry (
    id                                text PRIMARY KEY NOT NULL,
    entry_number                      text NOT NULL,
    fiscal_period_id                  uuid NOT NULL,
    status                            text NOT NULL,
    source                            text NOT NULL,
    source_id                         text,
    description                       text NOT NULL,
    reference                         text,
    total_debit                       numeric(18,4) NOT NULL,
    total_credit                      numeric(18,4) NOT NULL,
    posted_by_principal_id            uuid,
    approved_by_principal_id          uuid,
    reversal_of_entry_id              text,
    reversed_by_entry_id              text,
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
    code                              text NOT NULL,
    name                              text NOT NULL,
    country_code                      text NOT NULL,
    currency                          text NOT NULL,
    currency_scale                    integer NOT NULL,
    tax_registration_number           text,
    fiscal_year_start_month           integer NOT NULL,
    region_ids                        text[],
    is_active                         boolean,
    scope_path                        text
);

-- One side of a double-entry movement. Renamed from entry, which sat beside journal_entry and
-- journal_line — three things called entry in one schema is a schema nobody reads twice. Hangs
-- off: reaches ledger.account through its keys; references ai.index_source, ledger.account,
-- ledger.cost_center. Reached by: 7 operations read it and 10 write it; 3 tables reference it;
-- written by 3 contracts — finance
CREATE TABLE IF NOT EXISTS ledger.posting (
    id                                text PRIMARY KEY NOT NULL,
    journal_entry_id                  text NOT NULL,
    account_id                        uuid NOT NULL,
    account_code                      text,
    debit                             numeric(18,4) NOT NULL,
    credit                            numeric(18,4) NOT NULL,
    venue_id                          uuid,
    cost_center_id                    uuid,
    source                            text,
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
    review_status                     text,
    review_outcome                    text,
    reviewed_by_principal_id          uuid,
    journal_entry_id                  text,
    occurred_at                       timestamptz NOT NULL
);

-- When deferred revenue becomes revenue — a membership sold in March and earned across a year
CREATE TABLE IF NOT EXISTS ledger.recognition_schedule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL,
    method                            text NOT NULL,
    priority                          integer,
    recognition_site                  text,
    frequency                         text,
    revalidate_on_validity_change     boolean,
    product_kinds                     text[] NOT NULL,
    deferred_account_id               uuid,
    recognised_account_id             uuid,
    breakage_account_id               uuid,
    no_show_trigger                   text,
    no_show_account_id                uuid,
    breakage_after_days               integer,
    is_active                         boolean
);

-- Money actually arriving from a provider, matched against what was taken
CREATE TABLE IF NOT EXISTS ledger.settlement (
    id                                uuid PRIMARY KEY NOT NULL,
    currency_code                     text,
    provider_name                     text NOT NULL,
    period_start                      date NOT NULL,
    period_end                        date NOT NULL,
    status                            text NOT NULL,
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
    scope_path                        text
);

-- A settlement that did not match. The queue somebody works, not an error log
CREATE TABLE IF NOT EXISTS ledger.settlement_exception (
    id                                text PRIMARY KEY NOT NULL,
    settlement_id                     uuid NOT NULL,
    kind                              text NOT NULL,
    provider_reference                text NOT NULL,
    payment_id                        text,
    amount                            numeric(18,4) NOT NULL,
    expected_amount                   numeric(18,4),
    resolution                        text,
    resolved_by_principal_id          uuid,
    resolved_at                       timestamptz
);

-- A rate and its rules, scoped to a region
CREATE TABLE IF NOT EXISTS ledger.tax_code (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
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
-- references ledger.tax_code. Reached by: 2 operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS ledger.tax_exemption (
    id                                uuid PRIMARY KEY NOT NULL,
    scope                             text NOT NULL,
    scope_ref                         text,
    tax_code_id                       uuid NOT NULL,
    reason                            text NOT NULL,
    certificate_reference             text,
    valid_from                        date,
    valid_to                          date
);

