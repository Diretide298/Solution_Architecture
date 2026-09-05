"""Generated. The declared reads and writes of each operation."""

READS = {
 "addBlacklistEntry": [
  "SELECT * FROM access.blacklist WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createAccessPoint": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createAdmissionRules": [
  "SELECT * FROM access.admission_rules WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createParkingEntitlement": [
  "SELECT * FROM access.parking_facility LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "enrolFacePass": [
  "SELECT * FROM marketing.consent_record LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "getAccessPoint": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getEntitlement": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getEntitlementCredential": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getEntitlementHistory": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.scan_event WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getFacePassEnrolment": [
  "SELECT * FROM pii.subject_biometric LIMIT 50"
 ],
 "getOfflinePackage": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.admission_rules WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.blacklist WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM venuemap.path LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "listAccessPoints": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listAdmissionRules": [
  "SELECT * FROM access.admission_rules WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listBlacklist": [
  "SELECT * FROM access.blacklist WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listEntitlements": [
  "SELECT * FROM access.admission_rules WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listMyEntitlements": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listParkingFacilities": [
  "SELECT * FROM access.parking_facility LIMIT 50"
 ],
 "listScans": [
  "SELECT * FROM access.scan_event WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "lookupTicket": [
  "SELECT * FROM access.scan_event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "overrideAccess": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.scan_event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "removeBlacklistEntry": [
  "SELECT * FROM access.blacklist WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "revokeFacePass": [
  "SELECT * FROM pii.subject_biometric LIMIT 50"
 ],
 "setAccessPointGeofence": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setParkingFacility": [
  "SELECT * FROM access.parking_facility LIMIT 50"
 ],
 "setTurnstileMode": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "syncScans": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "updateAccessPoint": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "updateAdmissionRules": [
  "SELECT * FROM access.admission_rules WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "updateParkingEntitlement": [
  "SELECT * FROM access.parking_entitlement LIMIT 50"
 ],
 "validateAccess": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.admission_rules WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.blacklist WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "validateGroupAccess": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.admission_rules WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50"
 ]
}

WRITES = {
 "addBlacklistEntry": [
  "SELECT id FROM access.blacklist WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createAccessPoint": [
  "SELECT id FROM access.access_point WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createAdmissionRules": [
  "SELECT id FROM access.admission_rules WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createParkingEntitlement": [
  "SELECT id FROM access.parking_entitlement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "enrolFacePass": [
  "SELECT id FROM marketing.consent_record ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM pii.subject_biometric ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "getEntitlementCredential": [
  "SELECT id FROM access.entitlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "overrideAccess": [
  "SELECT id FROM access.scan_event WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "removeBlacklistEntry": [
  "SELECT id FROM access.blacklist WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "revokeFacePass": [
  "SELECT id FROM pii.subject_biometric ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAccessPointGeofence": [
  "SELECT id FROM access.access_point WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setParkingFacility": [
  "SELECT id FROM access.parking_facility ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setTurnstileMode": [
  "SELECT id FROM access.access_point WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "syncScans": [
  "SELECT id FROM access.scan_event WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM sync.rejection ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateAccessPoint": [
  "SELECT id FROM access.access_point WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateAdmissionRules": [
  "SELECT id FROM access.admission_rules WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateParkingEntitlement": [
  "SELECT id FROM access.parking_entitlement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "validateAccess": [
  "SELECT id FROM access.scan_event WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "validateGroupAccess": [
  "SELECT id FROM access.scan_event WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "addBlacklistEntry": [
  "cache:idempotency:bench"
 ],
 "createAccessPoint": [
  "cache:idempotency:bench"
 ],
 "createAdmissionRules": [
  "cache:idempotency:bench"
 ],
 "createParkingEntitlement": [
  "cache:idempotency:bench"
 ],
 "enrolFacePass": [
  "cache:idempotency:bench"
 ],
 "getOfflinePackage": [
  "cache:resolution:bench"
 ],
 "overrideAccess": [
  "cache:idempotency:bench"
 ],
 "removeBlacklistEntry": [
  "cache:idempotency:bench"
 ],
 "revokeFacePass": [
  "cache:idempotency:bench"
 ],
 "setAccessPointGeofence": [
  "cache:idempotency:bench"
 ],
 "setParkingFacility": [
  "cache:idempotency:bench"
 ],
 "setTurnstileMode": [
  "cache:idempotency:bench"
 ],
 "updateAccessPoint": [
  "cache:idempotency:bench"
 ],
 "updateAdmissionRules": [
  "cache:idempotency:bench"
 ],
 "updateParkingEntitlement": [
  "cache:idempotency:bench"
 ],
 "validateAccess": [
  "cache:idempotency:bench"
 ],
 "validateGroupAccess": [
  "cache:idempotency:bench"
 ]
}
