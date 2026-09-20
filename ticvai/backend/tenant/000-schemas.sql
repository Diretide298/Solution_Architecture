-- TICVAI — the tenant template.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- 32 schemas. The boundary is the service boundary (ADR-0028): no
-- service spans a schema it does not own, and no schema is written by two services.
-- **ADR-0038 left that decomposition untouched** — what changed is that this set now
-- exists once per tenant rather than once for everybody.
--
-- 572 tables. Applied to every tenant database by provision-tenant.sh.
--
-- **`control` is not here.** It left the template in ADR-0039 and the count went 26 to 25.

CREATE SCHEMA IF NOT EXISTS access;
CREATE SCHEMA IF NOT EXISTS accreditation;
CREATE SCHEMA IF NOT EXISTS ai;
CREATE SCHEMA IF NOT EXISTS approvals;
CREATE SCHEMA IF NOT EXISTS assets;
CREATE SCHEMA IF NOT EXISTS catalogue;
CREATE SCHEMA IF NOT EXISTS fnb;
CREATE SCHEMA IF NOT EXISTS games;
CREATE SCHEMA IF NOT EXISTS identity;
CREATE SCHEMA IF NOT EXISTS inventory;
CREATE SCHEMA IF NOT EXISTS ledger;
CREATE SCHEMA IF NOT EXISTS maintenance;
CREATE SCHEMA IF NOT EXISTS marketing;
CREATE SCHEMA IF NOT EXISTS orders;
CREATE SCHEMA IF NOT EXISTS payments;
CREATE SCHEMA IF NOT EXISTS pii;
CREATE SCHEMA IF NOT EXISTS platform;
CREATE SCHEMA IF NOT EXISTS pricing;
CREATE SCHEMA IF NOT EXISTS promotions;
CREATE SCHEMA IF NOT EXISTS queue;
CREATE SCHEMA IF NOT EXISTS rental;
CREATE SCHEMA IF NOT EXISTS reporting;
CREATE SCHEMA IF NOT EXISTS resources;
CREATE SCHEMA IF NOT EXISTS retail;
CREATE SCHEMA IF NOT EXISTS seating;
CREATE SCHEMA IF NOT EXISTS subscription;
CREATE SCHEMA IF NOT EXISTS sync;
CREATE SCHEMA IF NOT EXISTS tenancy;
CREATE SCHEMA IF NOT EXISTS venuemap;
CREATE SCHEMA IF NOT EXISTS wallet;
CREATE SCHEMA IF NOT EXISTS whitelabel;
CREATE SCHEMA IF NOT EXISTS workforce;
