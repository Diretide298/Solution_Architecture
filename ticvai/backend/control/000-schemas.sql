-- TICVAI — the control database.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **One schema, and a database of its own** (ADR-0039). Every table here is *about*
-- tenants rather than *inside* one: the cell registry, placement, licences, subscriptions,
-- releases, rollouts, migration runs, onboarding, and the tenant registry itself.
--
-- A cell registry that exists two hundred times is two hundred registries that can
-- disagree, and the first thing that disagrees is which of them is authoritative.
--
-- 49 tables. Applied once per region, to the instance.

CREATE SCHEMA IF NOT EXISTS control;
