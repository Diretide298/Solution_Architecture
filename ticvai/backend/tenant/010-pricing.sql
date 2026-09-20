-- pricing — 3 tables
-- **Derived. Do not hand-edit.**

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS pricing.dynamic_price_action (
    id                                uuid PRIMARY KEY,
    rule_id                           uuid NOT NULL,
    type                              text NOT NULL,
    value                             numeric(18,4) NOT NULL,
    min_price                         numeric(18,4),
    max_price                         numeric(18,4)
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS pricing.dynamic_price_condition (
    action_id                         uuid NOT NULL,
    rule_id                           uuid NOT NULL,
    type                              text NOT NULL,
    rule_operator                     text NOT NULL,
    value_json                        text NOT NULL,
    sequence_no                       integer NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS pricing.dynamic_price_rule (
    id                                uuid PRIMARY KEY,
    pricing_rule_code                 text NOT NULL,
    name                              text NOT NULL,
    product_id                        uuid,
    price_list_id                     uuid,
    scope_path                        text,
    channel_id                        uuid,
    priority                          integer NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    is_active                         boolean NOT NULL
);

