-- Row-level security, control database.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **Default deny is the point.** With `ticvai.scope_paths` unset, every policy below returns no
-- rows. A connection that forgets to set it sees an empty database, not the whole of it — which
-- is the Sprint 1 Gate 0 criterion, written as a predicate rather than a promise.
--
-- **Applied to every table that carries `scope_path`, which is what changed on 21 September.**
-- The hand-written baseline enabled RLS on three tables. The partition key is a column this
-- generator already knows about on every table that has one, so the policy set is derived rather
-- than remembered — and a new table with a `scope_path` is protected by existing, not by somebody
-- noticing.

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

-- Applies the standard policy to a table.
-- **FORCE is the whole point.** Without it the table owner — which is what a migration and most
-- pooled application connections run as — bypasses every policy silently.
CREATE OR REPLACE FUNCTION platform.apply_scope_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := 'scope_isolation';
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.in_scope(scope_path)) '
        'WITH CHECK (platform.in_scope(scope_path))', policy_name, target);
END
$$;

-- **59 tables carry `venue_id` and no `scope_path`, and a policy set built on `scope_path` alone
-- leaves every one of them open.** `check-migrations` has said so since it was written — *"checking
-- only scope_path missed 41 tables that carry venue_id instead; they would have passed with no
-- policy at all"* — and the hand-written baseline never closed it because it protected three
-- tables in total.
--
-- A venue id is resolved to its path through the scope tree rather than assumed. **The subquery is
-- the price of not carrying a redundant `scope_path` column on sixty tables**, and `platform.scope`
-- is small, cached and indexed on `id`.
CREATE OR REPLACE FUNCTION platform.venue_in_scope(row_venue_id uuid)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_venue_id IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND EXISTS (
            SELECT 1 FROM platform.scope s
             WHERE s.id = row_venue_id
               AND s.path::ltree <@ ANY (platform.current_scope_paths()));
$$;

CREATE OR REPLACE FUNCTION platform.apply_venue_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := 'venue_isolation';
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.venue_in_scope(venue_id)) '
        'WITH CHECK (platform.venue_in_scope(venue_id))', policy_name, target);
END
$$;

-- **7 tables carry `scope_path` and 1 carry `venue_id` instead, out of 49.**
-- Both are protected. A table with neither is not scoped -- it is reference data, a
-- registry, or the migration log itself, and a policy on it would deny every row to
-- everybody.


-- Scoped by path.
SELECT platform.apply_scope_rls('control.channel_listing'::regclass);
SELECT platform.apply_scope_rls('control.content_block'::regclass);
SELECT platform.apply_scope_rls('control.footer_config'::regclass);
SELECT platform.apply_scope_rls('control.migration_plan'::regclass);
SELECT platform.apply_scope_rls('control.seo_metadata'::regclass);
SELECT platform.apply_scope_rls('control.support_notice'::regclass);
SELECT platform.apply_scope_rls('control.url_redirect'::regclass);

-- Scoped by venue, resolved through the scope tree.
SELECT platform.apply_venue_rls('control.usage_record'::regclass);
