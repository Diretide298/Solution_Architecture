# The reference fixture

Every integration test, the frontend mock server and a developer's local database run against one set of seed
data: the **reference fixture**. Ticket SETUP-SEED builds it here, in `db/seed/`; until it lands this file is the
placeholder that says where it goes.

What it holds (TICVAI quality gates 8, SETUP-SEED's ticket):

- two brands, three regions across two countries, AED and OMR;
- products, prices, events, tills, staff, roles and denominations, so the apps can be built before the Back Office
  setup screens exist (the denominations and roles from `docs/active/seed-data-proposal.md` in the package,
  proposed, for the client to correct).

How it is used:

- it loads on a database the migration runner (`SqlMigrationRunner`, MIG-BASELINE onwards) has migrated;
- `dotnet test` runs the integration tests (`tests/TICVAI.IntegrationTests`) against it;
- the frontend mock server serves the same data.

A ticket whose Done-when says "against the reference fixture" means this data, loaded this way.
