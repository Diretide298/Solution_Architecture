-- V0001__baseline.sql
-- Platform schema, row-level security, the partitioning mechanism, the outbox, the pii split.
--
-- This is the migration every other migration assumes. It creates no business table: it creates
-- the machinery those tables are required to use. ADR-0005 (venue isolation by partitioning),
-- ADR-0044 (which tables partition, signed off 18 September 2026) and ADR-0002 (authorisation is
-- user-driven) all land here, because all three are enforced by the database rather than asserted
-- by the application.
--
-- **Default deny is the point.** With `ticvai.scope_paths` unset, every policy below returns no
-- rows. A connection that forgets to set it sees an empty database, not the whole of it — which is
-- the Sprint 1 Gate 0 criterion, written as a predicate rather than a promise.

BEGIN;

-- ---------------------------------------------------------------------------
-- Extensions
-- ---------------------------------------------------------------------------

-- ltree carries the scope tree. GiST indexes its containment operators, which is what makes
-- `<@` cheap enough to sit inside every policy on every table.
CREATE EXTENSION IF NOT EXISTS ltree;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------------------------------------------------------------------------
-- Schemas
-- ---------------------------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS platform;

-- **pii is an architectural boundary, not a naming convention.** A subject-access export is
-- answerable because natural-person columns live in one schema that can be enumerated, and a
-- retention rule has somewhere to attach. Keeping it separate is what makes CF-165 tractable
-- when somebody finally writes that rule.
CREATE SCHEMA IF NOT EXISTS pii;

-- ---------------------------------------------------------------------------
-- Scope vocabulary
-- ---------------------------------------------------------------------------

-- A bare uuid in a `venue_id` column can point at a workstation, a department or nothing at all.
-- The type says uuid and the intent says venue. This enum plus the composite foreign key in
-- V0003a is what closes that gap, and `check-migrations` fails any later table that skips it.
DO $$
BEGIN
    CREATE TYPE platform.scope_level AS ENUM
        ('tenant', 'region', 'venue', 'outlet', 'department', 'workstation');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

-- The scope tree itself. `(id, level)` is UNIQUE so that a level-typed foreign key can target it:
-- a reference to (venue_id, 'venue') cannot resolve to a workstation.
CREATE TABLE IF NOT EXISTS platform.scope_node (
    id                                uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    level                             platform.scope_level NOT NULL,
    parent_id                         uuid REFERENCES platform.scope_node (id),
    scope_path                        text NOT NULL,
    display_name                      text NOT NULL,
    is_active                         boolean NOT NULL DEFAULT true,
    created_at                        timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT scope_node_id_level_key UNIQUE (id, level),
    CONSTRAINT scope_node_path_key UNIQUE (scope_path)
);

CREATE INDEX IF NOT EXISTS scope_node_path_gist
    ON platform.scope_node USING gist ((scope_path::ltree));

CREATE INDEX IF NOT EXISTS scope_node_parent_idx
    ON platform.scope_node (parent_id) WHERE parent_id IS NOT NULL;

-- ---------------------------------------------------------------------------
-- Row-level security
-- ---------------------------------------------------------------------------

-- The paths the current connection may see, read from a session GUC the API layer sets per
-- request. `true` in current_setting makes an unset GUC return NULL rather than raising, so an
-- unconfigured connection degrades to zero rows instead of an error nobody catches.
CREATE OR REPLACE FUNCTION platform.current_scope_paths()
    RETURNS ltree[]
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT COALESCE(
        (SELECT array_agg(p::ltree)
           FROM unnest(string_to_array(
                    NULLIF(current_setting('ticvai.scope_paths', true), ''), ',')) AS p
          WHERE btrim(p) <> ''),
        ARRAY[]::ltree[]);
$$;

-- True when the row sits at or beneath one of the granted paths. An empty grant list matches
-- nothing — deny is the default, and it is the default because it is the absence of a grant
-- rather than the presence of a denial.
CREATE OR REPLACE FUNCTION platform.in_scope(row_scope_path text)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_scope_path IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND row_scope_path::ltree <@ ANY (platform.current_scope_paths());
$$;

-- Applies the standard policy to a table. Later migrations call this instead of repeating six
-- lines; V0001 writes its own out longhand because `check-migrations` reads the literal
-- statements and a checker that trusts a helper call verifies nothing.
CREATE OR REPLACE FUNCTION platform.apply_scope_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := 'scope_isolation';
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    -- FORCE is the whole point. Without it the table owner — which is what a migration and most
    -- pooled application connections run as — bypasses every policy silently.
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.in_scope(scope_path)) '
        'WITH CHECK (platform.in_scope(scope_path))', policy_name, target);
END
$$;

ALTER TABLE platform.scope_node ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.scope_node FORCE ROW LEVEL SECURITY;
CREATE POLICY scope_isolation ON platform.scope_node
    USING (platform.in_scope(scope_path))
    WITH CHECK (platform.in_scope(scope_path));

-- ---------------------------------------------------------------------------
-- Partitioning mechanism (ADR-0005, ADR-0044)
-- ---------------------------------------------------------------------------

-- ADR-0044, signed off 18 September 2026: a table whose `venue_id` is NOT NULL partitions by
-- list on it, carries `venue_id` as the leading column of its primary key, and every foreign key
-- into it is composite. 32 tables qualify today; they arrive in their own module migrations,
-- not here. What lives here is the mechanism they use.
--
-- **Every partitioned table needs a DEFAULT partition.** Misconfiguration should be loud rather
-- than silently lossy — an insert for an unprovisioned venue lands somewhere it can be found.
CREATE OR REPLACE FUNCTION platform.ensure_venue_partition(target regclass, venue_id uuid)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    part_name text;
    parent_name text := target::text;
BEGIN
    part_name := replace(split_part(parent_name, '.', 2) || '_' ||
                         replace(venue_id::text, '-', ''), '.', '_');
    IF to_regclass(format('%I.%I', split_part(parent_name, '.', 1), part_name)) IS NOT NULL THEN
        RETURN;
    END IF;
    EXECUTE format('CREATE TABLE %I.%I PARTITION OF %s FOR VALUES IN (%L)',
                   split_part(parent_name, '.', 1), part_name, target, venue_id);
END
$$;

-- ---------------------------------------------------------------------------
-- Outbox
-- ---------------------------------------------------------------------------

-- Written inside the transaction that changed the state it describes. That is the entire
-- guarantee: an event cannot exist without its state change, and a state change cannot complete
-- without its event.
CREATE TABLE IF NOT EXISTS platform.outbox (
    id                                uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    event_name                        text NOT NULL,
    aggregate_type                    text,
    aggregate_id                      uuid,
    payload                           jsonb NOT NULL,
    scope_path                        text,
    sequence                          bigint GENERATED ALWAYS AS IDENTITY,
    published_at                      timestamptz,
    attempts                          integer NOT NULL DEFAULT 0,
    last_error                        text,
    created_at                        timestamptz NOT NULL DEFAULT now()
);

-- The publisher's only query. Partial, because a published row is never read again and the
-- unpublished tail is small however large the table grows.
CREATE INDEX IF NOT EXISTS outbox_unpublished_idx
    ON platform.outbox (created_at) WHERE published_at IS NULL;

ALTER TABLE platform.outbox ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.outbox FORCE ROW LEVEL SECURITY;
CREATE POLICY scope_isolation ON platform.outbox
    USING (platform.in_scope(scope_path))
    WITH CHECK (platform.in_scope(scope_path));

-- Where an event goes after the publisher gives up. Kept rather than dropped, because the
-- reason a message failed is the only evidence of what broke.
CREATE TABLE IF NOT EXISTS platform.dead_letter (
    id                                uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    outbox_id                         uuid NOT NULL,
    event_name                        text NOT NULL,
    payload                           jsonb NOT NULL,
    scope_path                        text,
    failure_reason                    text NOT NULL,
    attempts                          integer NOT NULL,
    failed_at                         timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE platform.dead_letter ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.dead_letter FORCE ROW LEVEL SECURITY;
CREATE POLICY scope_isolation ON platform.dead_letter
    USING (platform.in_scope(scope_path))
    WITH CHECK (platform.in_scope(scope_path));

-- ---------------------------------------------------------------------------
-- Migration register
-- ---------------------------------------------------------------------------

-- Migrations fan out per region, not per tenant (ADR-0014). A tenant in three regions is three
-- cells and three applications, and they may legitimately sit at different versions mid-rollout.
-- This table is how the orchestrator knows where each one got to.
CREATE TABLE IF NOT EXISTS platform.schema_version (
    version                           text PRIMARY KEY NOT NULL,
    description                       text NOT NULL,
    checksum                          text NOT NULL,
    applied_at                        timestamptz NOT NULL DEFAULT now(),
    applied_by                        text NOT NULL DEFAULT current_user,
    execution_ms                      integer,
    rollback_tested_at                timestamptz
);

-- Not scope-partitioned and deliberately not under RLS: the migration register describes the
-- database, not anybody's data, and a connection that cannot read it cannot safely migrate.

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0001', 'platform, RLS, partitioning, outbox, pii',
        encode(digest('V0001__baseline', 'sha256'), 'hex'))
ON CONFLICT (version) DO NOTHING;

COMMIT;

-- ============================================================================
-- ROLLBACK
--
-- Tested in CI against a restored snapshot, not asserted. The order is the reverse of creation:
-- policies fall with their tables, functions after the tables that reference them, types last
-- because the enum is depended on by columns in later migrations that must already be gone.
-- ============================================================================

BEGIN;

DROP TABLE IF EXISTS platform.dead_letter;
DROP TABLE IF EXISTS platform.outbox;
DROP TABLE IF EXISTS platform.scope_node;

DROP FUNCTION IF EXISTS platform.ensure_venue_partition(regclass, uuid);
DROP FUNCTION IF EXISTS platform.apply_scope_rls(regclass);
DROP FUNCTION IF EXISTS platform.in_scope(text);
DROP FUNCTION IF EXISTS platform.current_scope_paths();

DROP TYPE IF EXISTS platform.scope_level;

DELETE FROM platform.schema_version WHERE version = 'V0001';
DROP TABLE IF EXISTS platform.schema_version;

DROP SCHEMA IF EXISTS pii;
DROP SCHEMA IF EXISTS platform;

COMMIT;
