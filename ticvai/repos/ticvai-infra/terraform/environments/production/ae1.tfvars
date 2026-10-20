# Production, UAE cell ae1 (the client hosts production later; the lead, 20 October 2026).
# A cell is a region with a database per tenant (ADR-0038, ADR-0040): Miral is a tenant placed on it,
# a row in the control database (ADR-0039), not an input here (FOUNDATION-AI-C55).
# Miral, UAE cell. Covers the Abu Dhabi and Dubai regions.
environment  = "production"
cell         = "ae1"
jurisdiction = "ae"
tier         = "dedicated"
location     = "uaenorth"

# Sized against TENANT aggregate load, not per-venue. Venue peaks within a tenant
# are correlated — Eid, National Day, school holidays — so the averaging
# assumption behind per-venue sizing does not apply.
database_sku        = "GP_Standard_D16ds_v5"
database_storage_mb = 524288
read_replica_count  = 3

# Verify the Azure paired region for uaenorth sits inside the jurisdiction
# before enabling. Default pairing may move personal data across the boundary.
geo_redundant_backup_enabled = false

workload_min_nodes = 4
workload_max_nodes = 30
