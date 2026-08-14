# Cell module

One instance = one tenant in one jurisdiction.

Miral runs **two** cells minimum — `miral-ae` and `miral-om` — because Theme Park
Brand spans UAE and Oman and a venue operating in a jurisdiction expects its
infrastructure there.

## Before applying

1. **Verify the hyperscaler has a region in the jurisdiction.** Gulf coverage is
   uneven. Where there is no region, `tier = "client_hosted"` is the mechanism,
   not a workaround.
2. **Check `geo_redundant_backup_enabled` against the paired region.** Azure's
   default pairing may sit outside the jurisdiction, which would move personal
   data across the boundary via the backup path.
3. Size `database_sku` against **tenant aggregate** load. Venue peaks within a
   tenant are correlated — Eid, National Day, school holidays — so the averaging
   assumption that makes per-venue sizing comfortable does not apply.

## What is not in this module

Cross-tenant analytics. The warehouse is fed by per-cell event export of
**aggregated, pseudonymised** data only. Cells are never queried directly.
Anything above Venue level is aggregate and may cross borders; anything at Venue
level or below stays in-cell.
