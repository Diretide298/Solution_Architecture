# Miral, Oman cell. Required by jurisdiction, not by load — a venue operating in
# Oman expects its infrastructure in Oman (Project Direction §3.3.1).
#
# BLOCKER: confirm hyperscaler presence in Oman before applying. Where there is
# no in-jurisdiction region, tier = "client_hosted" is the mechanism, not a
# workaround. See CF-20 / Dubai Compliance Authority follow-up.
tenant_id    = "00000000-0000-0000-0000-000000000000"
tenant_slug  = "miral"
jurisdiction = "om"
tier         = "client_hosted"
location     = "TBC"

database_sku       = "GP_Standard_D4ds_v5"
read_replica_count = 1

# OMR carries 3 decimal places against AED's 2. Region settings drive the money
# scale; nothing here needs to change, but the seed data must set it correctly.
