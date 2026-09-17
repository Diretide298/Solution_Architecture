"""Generated. The declared reads and writes of each operation."""

READS = {
 "completeSsoAuthorization": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM identity.sso_provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createDelegatedAccess": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createMfaChallenge": [
  "SELECT * FROM identity.mfa_method LIMIT 50"
 ],
 "createPrincipal": [
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "createRole": [
  "SELECT * FROM identity.role LIMIT 50"
 ],
 "deleteDelegatedAccess": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "deleteGuestAccount": [
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "enrolMfaMethod": [
  "SELECT * FROM identity.mfa_recovery_code LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "exportSubjectData": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.consent_record LIMIT 50",
  "SELECT * FROM marketing.form_submission LIMIT 50",
  "SELECT * FROM marketing.guest_document LIMIT 50",
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "getCurrentSession": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM identity.role LIMIT 50"
 ],
 "getGuestSession": [
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "getPrincipal": [
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "getSsoConfig": [
  "SELECT * FROM identity.sso_group_mapping WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.sso_provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "grantDelegation": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "guestSocialLogin": [
  "SELECT * FROM pii.subject_contact LIMIT 50"
 ],
 "guestUaePassLogin": [
  "SELECT * FROM pii.subject_contact LIMIT 50"
 ],
 "linkGuestCheckout": [
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM pii.subject_contact LIMIT 50"
 ],
 "listActiveSessions": [
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "listDelegatedAccess": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listDelegations": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "listMfaMethods": [
  "SELECT * FROM identity.mfa_method LIMIT 50"
 ],
 "listPrincipals": [
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "listRoles": [
  "SELECT * FROM identity.role LIMIT 50"
 ],
 "listSsoProviders": [
  "SELECT * FROM identity.sso_provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "login": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM identity.principal_credential LIMIT 50",
  "SELECT * FROM identity.role LIMIT 50"
 ],
 "registerGuest": [
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "removeMfaMethod": [
  "SELECT * FROM identity.mfa_method LIMIT 50"
 ],
 "requestGuestOtp": [
  "SELECT * FROM pii.subject_contact LIMIT 50"
 ],
 "resolvePermissions": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM identity.role LIMIT 50",
  "SELECT * FROM identity.role_permission LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "selectRole": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.role LIMIT 50"
 ],
 "setPasswordPolicy": [
  "SELECT * FROM identity.password_policy WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setSegregationRules": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.segregation_rule WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setSsoConfig": [
  "SELECT * FROM identity.sso_group_mapping WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.sso_provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "startSsoAuthorization": [
  "SELECT * FROM identity.sso_provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "updatePrincipal": [
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "verifyGuestEmail": [
  "SELECT * FROM identity.otp_challenge LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "verifyGuestOtp": [
  "SELECT * FROM identity.otp_challenge LIMIT 50",
  "SELECT * FROM pii.subject_contact LIMIT 50"
 ],
 "verifyMfaChallenge": [
  "SELECT * FROM identity.mfa_challenge LIMIT 50",
  "SELECT * FROM identity.mfa_recovery_code LIMIT 50"
 ],
 "verifyMfaEnrolment": [
  "SELECT * FROM identity.mfa_method LIMIT 50"
 ]
}

WRITES = {
 "createDelegatedAccess": [
  "SELECT id FROM identity.delegated_access WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createMfaChallenge": [
  "SELECT id FROM identity.mfa_challenge ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPrincipal": [
  "SELECT id FROM identity.principal ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRole": [
  "SELECT id FROM identity.role ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deleteDelegatedAccess": [
  "SELECT id FROM identity.delegated_access WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deleteGuestAccount": [
  "SELECT id FROM pii.subject ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.dsar_request ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "enrolMfaMethod": [
  "SELECT id FROM identity.mfa_method ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM identity.mfa_recovery_code ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "grantDelegation": [
  "SELECT id FROM identity.delegated_access WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "guestSocialLogin": [
  "SELECT id FROM pii.subject ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "guestUaePassLogin": [
  "SELECT id FROM pii.subject ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM pii.subject_document ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "linkGuestCheckout": [
  "SELECT id FROM orders.sales_order WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM pii.subject ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "registerGuest": [
  "SELECT id FROM pii.subject ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM pii.subject_contact ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "removeMfaMethod": [
  "SELECT id FROM identity.mfa_method ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "requestGuestOtp": [
  "SELECT id FROM identity.otp_challenge ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setPasswordPolicy": [
  "SELECT id FROM identity.password_policy WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setSegregationRules": [
  "SELECT id FROM identity.segregation_rule WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setSsoConfig": [
  "SELECT id FROM identity.sso_group_mapping WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM identity.sso_provider WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updatePrincipal": [
  "SELECT id FROM identity.principal ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "verifyGuestEmail": [
  "SELECT id FROM identity.otp_challenge ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "verifyGuestOtp": [
  "SELECT id FROM pii.subject_contact ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "verifyMfaChallenge": [
  "SELECT id FROM identity.mfa_challenge ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM identity.mfa_recovery_code ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "verifyMfaEnrolment": [
  "SELECT id FROM identity.mfa_method ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "completeSsoAuthorization": [
  "cache:idempotency:bench",
  "cache:identity.session:bench"
 ],
 "createDelegatedAccess": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "createMfaChallenge": [
  "cache:idempotency:bench"
 ],
 "createPrincipal": [
  "cache:idempotency:bench"
 ],
 "createRole": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "deleteDelegatedAccess": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "deleteGuestAccount": [
  "cache:idempotency:bench"
 ],
 "enrolMfaMethod": [
  "cache:idempotency:bench"
 ],
 "exportSubjectData": [
  "cache:idempotency:bench"
 ],
 "forceLogout": [
  "cache:idempotency:bench",
  "cache:identity.session:bench"
 ],
 "getCurrentSession": [
  "cache:resolution:bench",
  "cache:identity.session:bench"
 ],
 "getGuestSession": [
  "cache:identity.guest_session:bench"
 ],
 "grantDelegation": [
  "cache:idempotency:bench"
 ],
 "guestLogout": [
  "cache:identity.guest_session:bench"
 ],
 "guestSocialLogin": [
  "cache:idempotency:bench",
  "cache:identity.guest_session:bench"
 ],
 "guestUaePassLogin": [
  "cache:idempotency:bench",
  "cache:identity.guest_session:bench"
 ],
 "linkGuestCheckout": [
  "cache:idempotency:bench"
 ],
 "listActiveSessions": [
  "cache:identity.session:bench"
 ],
 "login": [
  "cache:idempotency:bench",
  "cache:identity.session:bench"
 ],
 "logout": [
  "cache:idempotency:bench",
  "cache:identity.session:bench"
 ],
 "refreshToken": [
  "cache:idempotency:bench",
  "cache:identity.session:bench"
 ],
 "registerGuest": [
  "cache:idempotency:bench",
  "cache:identity.guest_session:bench"
 ],
 "removeMfaMethod": [
  "cache:idempotency:bench"
 ],
 "requestGuestOtp": [
  "cache:idempotency:bench"
 ],
 "resolvePermissions": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "revokeAllSessions": [
  "cache:idempotency:bench",
  "cache:identity.session:bench"
 ],
 "selectRole": [
  "cache:idempotency:bench",
  "cache:identity.session:bench"
 ],
 "setPasswordPolicy": [
  "cache:idempotency:bench"
 ],
 "setSegregationRules": [
  "cache:idempotency:bench"
 ],
 "setSsoConfig": [
  "cache:idempotency:bench"
 ],
 "updatePrincipal": [
  "cache:idempotency:bench"
 ],
 "verifyGuestEmail": [
  "cache:idempotency:bench"
 ],
 "verifyGuestOtp": [
  "cache:idempotency:bench",
  "cache:identity.guest_session:bench"
 ],
 "verifyMfaChallenge": [
  "cache:idempotency:bench",
  "cache:identity.session:bench"
 ],
 "verifyMfaEnrolment": [
  "cache:idempotency:bench"
 ]
}
