"""Generated. The declared reads and writes of each operation."""

READS = {
 "authoriseWalletSpend": [
  "SELECT * FROM platform.wallet_authorisation LIMIT 50"
 ],
 "captureWalletAuthorisation": [
  "SELECT * FROM platform.wallet_authorisation LIMIT 50"
 ],
 "consumeCrossRegionEntitlement": [
  "SELECT * FROM platform.cross_region_entitlement LIMIT 50"
 ],
 "createDsarRequest": [
  "SELECT * FROM platform.dsar_request LIMIT 50"
 ],
 "createGuestLink": [
  "SELECT * FROM platform.guest_link LIMIT 50"
 ],
 "getCrossRegionEntitlement": [
  "SELECT * FROM platform.cross_region_entitlement LIMIT 50"
 ],
 "getDsarRequest": [
  "SELECT * FROM platform.dsar_request LIMIT 50"
 ],
 "getGuestLink": [
  "SELECT * FROM platform.guest_link LIMIT 50"
 ],
 "getWalletAllocation": [
  "SELECT * FROM platform.wallet_authorisation LIMIT 50"
 ],
 "propagateCrossRegionEntitlement": [
  "SELECT * FROM platform.cross_region_entitlement LIMIT 50"
 ],
 "reconcileRedemptions": [
  "SELECT * FROM access.scan_event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM platform.cross_region_entitlement LIMIT 50"
 ],
 "releaseWalletAuthorisation": [
  "SELECT * FROM platform.wallet_authorisation LIMIT 50"
 ],
 "relinquishWalletAuthorisation": [
  "SELECT * FROM platform.wallet_authorisation LIMIT 50"
 ],
 "resolveGuestLink": [
  "SELECT * FROM platform.guest_link LIMIT 50"
 ],
 "revokeCrossRegionEntitlement": [
  "SELECT * FROM platform.cross_region_entitlement LIMIT 50"
 ],
 "revokeGuestLink": [
  "SELECT * FROM platform.guest_link LIMIT 50"
 ],
 "setWalletAllocationPolicy": [
  "SELECT * FROM platform.wallet_authorisation LIMIT 50"
 ]
}

WRITES = {
 "authoriseWalletSpend": [
  "SELECT id FROM platform.wallet_authorisation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "captureWalletAuthorisation": [
  "SELECT id FROM platform.wallet_authorisation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "consumeCrossRegionEntitlement": [
  "SELECT id FROM platform.cross_region_entitlement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createDsarRequest": [
  "SELECT id FROM platform.dsar_request ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createGuestLink": [
  "SELECT guest_link_id FROM platform.guest_link ORDER BY guest_link_id LIMIT 1 FOR UPDATE"
 ],
 "propagateCrossRegionEntitlement": [
  "SELECT id FROM platform.cross_region_entitlement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reconcileRedemptions": [
  "SELECT id FROM platform.cross_region_entitlement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "releaseWalletAuthorisation": [
  "SELECT id FROM platform.wallet_authorisation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "revokeCrossRegionEntitlement": [
  "SELECT id FROM platform.cross_region_entitlement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "revokeGuestLink": [
  "SELECT guest_link_id FROM platform.guest_link ORDER BY guest_link_id LIMIT 1 FOR UPDATE"
 ],
 "setWalletAllocationPolicy": [
  "SELECT id FROM platform.wallet_authorisation ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "authoriseWalletSpend": [
  "cache:idempotency:bench"
 ],
 "captureWalletAuthorisation": [
  "cache:idempotency:bench"
 ],
 "consumeCrossRegionEntitlement": [
  "cache:idempotency:bench"
 ],
 "createDsarRequest": [
  "cache:idempotency:bench"
 ],
 "createGuestLink": [
  "cache:idempotency:bench"
 ],
 "propagateCrossRegionEntitlement": [
  "cache:idempotency:bench"
 ],
 "reconcileRedemptions": [
  "cache:idempotency:bench"
 ],
 "releaseWalletAuthorisation": [
  "cache:idempotency:bench"
 ],
 "revokeCrossRegionEntitlement": [
  "cache:idempotency:bench"
 ],
 "revokeGuestLink": [
  "cache:idempotency:bench"
 ],
 "setWalletAllocationPolicy": [
  "cache:idempotency:bench"
 ]
}
