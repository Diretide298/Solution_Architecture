-- pricing — 3 tables
-- **Derived. Do not hand-edit.**

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS pricing.dynamic_price_action (
    id                                uuid PRIMARY KEY NOT NULL,
    dynamic_price_rule_id             uuid NOT NULL,
    type                              text NOT NULL CONSTRAINT dynamic_price_action_type_chk CHECK (char_length(type) <= 30),
    value                             numeric(18,4) NOT NULL,
    min_price                         numeric(18,4),
    max_price                         numeric(18,4),
    rule_id                           uuid
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS pricing.dynamic_price_condition (
    action_id                         uuid NOT NULL,
    dynamic_price_rule_id             uuid NOT NULL,
    type                              text NOT NULL CONSTRAINT dynamic_price_condition_type_chk CHECK (char_length(type) <= 50),
    rule_operator                     text NOT NULL CONSTRAINT dynamic_price_condition_rule_operator_chk CHECK (char_length(rule_operator) <= 20),
    value_json                        text NOT NULL,
    sequence_no                       integer NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    rule_id                           uuid
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS pricing.dynamic_price_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    pricing_rule_code                 text NOT NULL CONSTRAINT dynamic_price_rule_pricing_rule_code_chk CHECK (char_length(pricing_rule_code) <= 100),
    name                              text NOT NULL CONSTRAINT dynamic_price_rule_name_chk CHECK (char_length(name) <= 200),
    product_id                        uuid,
    price_list_id                     uuid,
    scope_path                        ltree NOT NULL,
    channel_id                        uuid,
    priority                          integer NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    is_active                         boolean NOT NULL,
    dynamic_pricing_strategy_id       uuid,
    rule_type                         text CONSTRAINT dynamic_price_rule_rule_type_chk CHECK (char_length(rule_type) <= 40),
    input_metric                      text CONSTRAINT dynamic_price_rule_input_metric_chk CHECK (char_length(input_metric) <= 40),
    condition_logic                   text DEFAULT 'all' CONSTRAINT dynamic_price_rule_condition_logic_chk CHECK (condition_logic IN ('all', 'any')),
    cooldown_minutes                  integer,
    minimum_duration_minutes          integer,
    exit_threshold_offset             numeric(18,4),
    range_min_percent                 numeric(18,4),
    range_max_percent                 numeric(18,4),
    is_protected                      boolean DEFAULT false
);

