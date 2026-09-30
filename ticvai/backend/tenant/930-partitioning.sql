-- Partitioning (ADR-0056, accepted 30 September 2026; amends ADR-0044).
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **Release 1 partitions by time, not by venue.** The tables that grow, grow with time: scans,
-- the outbox and its dead letters, the audit trail, journal lines, message dispatches and the
-- consumer inboxes. The rule is read from the schema, like every other rule in this generator: a
-- contract schema marked `x-ticvai-append-only: <time property>`, whose table has that column and
-- no inbound foreign key, is created `PARTITION BY RANGE` on the column, with the column in its
-- primary key. **Those tables declare their partitioning where they are created** (`010-<schema>.sql`);
-- what lives here is each one's DEFAULT partition and the monthly partitions ahead of today.
--
-- **Nothing points at a partitioned table**, which is part of the rule rather than a coincidence:
-- a foreign key into it would have to carry the time column too. Retention (ADR-0047) detaches
-- and archives a whole month instead of deleting rows.
--
-- **The inboxes partition on `event_id`, not on `processed_at`.** Their key is `(consumer,
-- event_id)` because that pair is the de-duplication rule (ADR-0058), and Postgres requires the
-- partition column in every unique key; a key that also carried `processed_at` would let a
-- redelivery insert a second row. The event id is a UUIDv7 (ADR-0056), whose first 48 bits are its
-- millisecond timestamp, so a month is the range between two UUIDv7 floors.
--
-- **Every partitioned table has a DEFAULT partition.** Misconfiguration should be loud rather than
-- silently lossy: a row for a month nobody created (an offline scan from before the first
-- partition, a clock years out) lands somewhere it can be found, and the job that creates the next
-- month fails on it instead of dropping it.
--
-- **Venue list partitioning is deferred, not cancelled** (ADR-0056 section 3). `venue_id NOT NULL`
-- stays where it is and no table gains a `venue_id` column for it. Where a child and its parent both
-- carry a NOT NULL `venue_id`, the foreign key between them is composite `(venue_id, <key>)` against a
-- parent `UNIQUE (venue_id, id)` (900-foreign-keys.sql), which keeps most of ADR-0044's cross-venue
-- guarantee; venue isolation on reads is row-level security (920-row-level-security.sql). Revisit:
-- a tenant with more than 100 venues, or one venue that needs its own vacuum or archive.

-- The smallest UUIDv7 minted at or after `ts`: its 48-bit millisecond timestamp and zeros after.
-- uuid comparison is bytewise, so every UUIDv7 from that millisecond on sorts at or above it.
CREATE OR REPLACE FUNCTION platform.uuidv7_floor(ts timestamptz)
    RETURNS uuid
    LANGUAGE sql
    IMMUTABLE
    PARALLEL SAFE
AS $$
    SELECT (substr(h, 1, 8) || '-' || substr(h, 9, 4) || '-0000-0000-000000000000')::uuid
      FROM (SELECT lpad(to_hex(floor(extract(epoch FROM ts) * 1000)::bigint), 12, '0') AS h) x;
$$;

-- Creates `<table>_p<YYYYMM>` for the month containing `month_start`, if it is missing. The bounds
-- follow the partition column's type: timestamps for a time column, UUIDv7 floors for a uuid.
CREATE OR REPLACE FUNCTION platform.ensure_month_partition(target regclass, month_start date)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    schema_name text := split_part(target::text, '.', 1);
    part_name text := split_part(replace(target::text, '"', ''), '.', 2) || '_p'
                      || to_char(date_trunc('month', month_start), 'YYYYMM');
    key_type text;
    lo timestamptz := date_trunc('month', month_start);
    hi timestamptz := date_trunc('month', month_start) + interval '1 month';
BEGIN
    IF to_regclass(format('%I.%I', schema_name, part_name)) IS NOT NULL THEN
        RETURN;
    END IF;
    SELECT format_type(a.atttypid, a.atttypmod) INTO key_type
      FROM pg_partitioned_table p
      JOIN pg_attribute a ON a.attrelid = p.partrelid AND a.attnum = p.partattrs[0]
     WHERE p.partrelid = target;
    IF key_type = 'uuid' THEN
        EXECUTE format('CREATE TABLE %I.%I PARTITION OF %s FOR VALUES FROM (%L) TO (%L)',
                       schema_name, part_name, target,
                       platform.uuidv7_floor(lo), platform.uuidv7_floor(hi));
    ELSE
        EXECUTE format('CREATE TABLE %I.%I PARTITION OF %s FOR VALUES FROM (%L) TO (%L)',
                       schema_name, part_name, target, lo, hi);
    END IF;
END
$$;

-- This month and `months_ahead` after it. The kernel's partition job (MIG-PARTITIONS) calls this
-- daily with 3; the calls at the end of this file give a new tenant database the same horizon.
CREATE OR REPLACE FUNCTION platform.ensure_month_partitions(target regclass, months_ahead integer)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    FOR i IN 0..months_ahead LOOP
        PERFORM platform.ensure_month_partition(
            target, (date_trunc('month', now()) + make_interval(months => i))::date);
    END LOOP;
END
$$;

-- **8 tables are range-partitioned by month** — append-only in their contract,
-- with the time column present and no inbound foreign key. Listed rather than counted, because
-- the rule is checkable and the list is how.

--   access.scan_event                  on recorded_at
--   ai.inbox                           on event_id
--   kernel.inbox                       on event_id
--   ledger.journal_line                on posted_at
--   marketing.message_dispatch         on queued_at
--   platform.audit_record              on occurred_at
--   platform.dead_letter               on created_at
--   platform.outbox                    on created_at

-- DEFAULT partitions: a row for a month nobody created is kept, and found.
CREATE TABLE IF NOT EXISTS access.scan_event_default PARTITION OF access.scan_event DEFAULT;
CREATE TABLE IF NOT EXISTS ai.inbox_default PARTITION OF ai.inbox DEFAULT;
CREATE TABLE IF NOT EXISTS kernel.inbox_default PARTITION OF kernel.inbox DEFAULT;
CREATE TABLE IF NOT EXISTS ledger.journal_line_default PARTITION OF ledger.journal_line DEFAULT;
CREATE TABLE IF NOT EXISTS marketing.message_dispatch_default PARTITION OF marketing.message_dispatch DEFAULT;
CREATE TABLE IF NOT EXISTS platform.audit_record_default PARTITION OF platform.audit_record DEFAULT;
CREATE TABLE IF NOT EXISTS platform.dead_letter_default PARTITION OF platform.dead_letter DEFAULT;
CREATE TABLE IF NOT EXISTS platform.outbox_default PARTITION OF platform.outbox DEFAULT;

-- This month and the next three (ADR-0056); the partition job keeps the horizon.
SELECT platform.ensure_month_partitions('access.scan_event'::regclass, 3);
SELECT platform.ensure_month_partitions('ai.inbox'::regclass, 3);
SELECT platform.ensure_month_partitions('kernel.inbox'::regclass, 3);
SELECT platform.ensure_month_partitions('ledger.journal_line'::regclass, 3);
SELECT platform.ensure_month_partitions('marketing.message_dispatch'::regclass, 3);
SELECT platform.ensure_month_partitions('platform.audit_record'::regclass, 3);
SELECT platform.ensure_month_partitions('platform.dead_letter'::regclass, 3);
SELECT platform.ensure_month_partitions('platform.outbox'::regclass, 3);
