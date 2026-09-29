-- embedded as attributes (jsonb) on orders — 1 tables
-- **Derived. Do not hand-edit.**

-- Holds 2 columns. No description has been written for this table — the name is the only thing
-- saying what it is. Reached by: 25 operations read it and 6 write it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS embedded as attributes (jsonb) on orders.cart_line and orders.order_line (
    id                                uuid PRIMARY KEY NOT NULL,
    transport                         jsonb
);

