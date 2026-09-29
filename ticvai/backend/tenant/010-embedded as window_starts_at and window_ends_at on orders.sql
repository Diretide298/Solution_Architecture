-- embedded as window_starts_at and window_ends_at on orders — 1 tables
-- **Derived. Do not hand-edit.**

-- Holds 3 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line (
    id                                uuid PRIMARY KEY NOT NULL,
    starts_at                         timestamptz NOT NULL,
    ends_at                           timestamptz NOT NULL
);

