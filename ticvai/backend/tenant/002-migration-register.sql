-- The migration register.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **The one table this generator cannot derive**, because `handoff/schema-reference.json` carries
-- it with no columns — it is storage the contracts never describe, which is correct: no operation
-- reads or writes it. It came from `V0001__baseline.sql` and would have been lost when that file
-- was deleted on 21 September.
--
-- Migrations fan out per region, not per tenant (ADR-0014). A tenant in three regions is three
-- cells and three applications, and they may legitimately sit at different versions mid-rollout.
-- **Emitted into both databases** because ADR-0039 made `control` a database of its own, and a
-- database that is migrated independently needs its own record of where it got to.
CREATE TABLE IF NOT EXISTS platform.schema_version (
    version                           text PRIMARY KEY NOT NULL,
    description                       text NOT NULL,
    checksum                          text NOT NULL,
    applied_at                        timestamptz NOT NULL DEFAULT now(),
    applied_by                        text NOT NULL DEFAULT current_user,
    execution_ms                      integer,
    rollback_tested_at                timestamptz
);

-- **Deliberately not under RLS**, and it carries no `scope_path` to put one on: the register
-- describes the database rather than anybody's data, and a connection that cannot read it cannot
-- safely migrate.
