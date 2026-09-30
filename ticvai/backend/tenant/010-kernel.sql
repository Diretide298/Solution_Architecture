-- kernel — 1 tables
-- **Derived. Do not hand-edit.**

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS kernel.inbox (
    consumer                          text NOT NULL CONSTRAINT inbox_consumer_chk CHECK (char_length(consumer) <= 200),
    event_id                          uuid NOT NULL,
    processed_at                      timestamptz NOT NULL,
    CONSTRAINT inbox_pkey PRIMARY KEY (consumer, event_id)
) PARTITION BY RANGE (event_id);

