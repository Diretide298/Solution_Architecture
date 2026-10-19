# Miral, UAE cell. Covers the Abu Dhabi and Dubai regions.
tenant_id    = "00000000-0000-0000-0000-000000000000"
tenant_slug  = "miral"
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
