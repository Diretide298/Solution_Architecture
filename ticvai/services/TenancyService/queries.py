"""Generated. The declared reads and writes of each operation."""

READS = {
 "acknowledgeAnnouncement": [
  "SELECT * FROM workforce.announcement LIMIT 50"
 ],
 "amendAttendance": [
  "SELECT * FROM workforce.attendance LIMIT 50"
 ],
 "broadcastToGuests": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "configureWorkstation": [
  "SELECT * FROM platform.device LIMIT 50",
  "SELECT * FROM platform.workstation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createApprovalDelegation": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "createApprovalRequest": [
  "SELECT * FROM approvals.delegation WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM approvals.matrix WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM approvals.rule LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "createOrgUnit": [
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "createOutlet": [
  "SELECT * FROM platform.outlet LIMIT 50"
 ],
 "createRotaAssignment": [
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM platform.workstation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createSaleBoard": [
  "SELECT * FROM platform.sale_board LIMIT 50"
 ],
 "decideApprovalRequest": [
  "SELECT * FROM approvals.request WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM approvals.rule LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "deployConfigurationProfile": [
  "SELECT * FROM platform.configuration_profile WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM platform.workstation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "escalateApprovalRequest": [
  "SELECT * FROM approvals.request WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM approvals.rule LIMIT 50"
 ],
 "evaluateApprovalRequirement": [
  "SELECT * FROM approvals.delegation WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM approvals.matrix WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM approvals.rule LIMIT 50",
  "SELECT * FROM identity.delegated_access WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "getAnnouncementReach": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM workforce.announcement_receipt LIMIT 50",
  "SELECT * FROM workforce.rota_assignment LIMIT 50"
 ],
 "getApprovalAnalytics": [
  "SELECT * FROM approvals.decision LIMIT 50",
  "SELECT * FROM approvals.escalation LIMIT 50",
  "SELECT * FROM approvals.request WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getOrgUnit": [
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "getRegionSettings": [
  "SELECT * FROM platform.region_settings LIMIT 50"
 ],
 "getVenueSettings": [
  "SELECT * FROM platform.venue_settings LIMIT 50"
 ],
 "getWorkstation": [
  "SELECT * FROM platform.device LIMIT 50",
  "SELECT * FROM platform.workstation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getWorkstationHealth": [
  "SELECT * FROM platform.device LIMIT 50",
  "SELECT * FROM platform.device_heartbeat LIMIT 50",
  "SELECT * FROM platform.workstation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "issueAccreditationBadge": [
  "SELECT * FROM approvals.accreditation_badge LIMIT 50"
 ],
 "listAccreditationBadges": [
  "SELECT * FROM approvals.accreditation_badge LIMIT 50"
 ],
 "listAnnouncements": [
  "SELECT * FROM workforce.announcement LIMIT 50",
  "SELECT * FROM workforce.announcement_receipt LIMIT 50"
 ],
 "listApprovalDelegations": [
  "SELECT * FROM approvals.delegation WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "listApprovalMatrices": [
  "SELECT * FROM approvals.matrix WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM approvals.rule LIMIT 50"
 ],
 "listApprovalRequests": [
  "SELECT * FROM approvals.decision LIMIT 50",
  "SELECT * FROM approvals.request WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listAttendance": [
  "SELECT * FROM workforce.attendance LIMIT 50",
  "SELECT * FROM workforce.rota_assignment LIMIT 50"
 ],
 "listAuditRecords": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM platform.audit_record LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "listDevices": [
  "SELECT * FROM platform.device LIMIT 50"
 ],
 "listOrgUnits": [
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "listOutlets": [
  "SELECT * FROM platform.outlet LIMIT 50"
 ],
 "listRotaAssignments": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM workforce.rota_assignment LIMIT 50"
 ],
 "listSaleBoards": [
  "SELECT * FROM platform.sale_board LIMIT 50"
 ],
 "listShiftSwapRequests": [
  "SELECT * FROM workforce.shift_swap LIMIT 50"
 ],
 "listStepUpPolicies": [
  "SELECT * FROM approvals.step_up_policy LIMIT 50"
 ],
 "listTrainingRecords": [
  "SELECT * FROM workforce.training_record LIMIT 50"
 ],
 "listWorkstations": [
  "SELECT * FROM platform.device LIMIT 50",
  "SELECT * FROM platform.workstation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "publishAnnouncement": [
  "SELECT * FROM identity.role LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "recordAttendance": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM workforce.rota_assignment LIMIT 50"
 ],
 "recordDeviceHeartbeat": [
  "SELECT * FROM platform.device LIMIT 50"
 ],
 "registerDevice": [
  "SELECT * FROM platform.device LIMIT 50"
 ],
 "requestShiftSwap": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM workforce.rota_assignment LIMIT 50"
 ],
 "resubmitApprovalRequest": [
  "SELECT * FROM approvals.request WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "revokeApprovalDelegation": [
  "SELECT * FROM approvals.delegation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setApprovalMatrix": [
  "SELECT * FROM approvals.matrix WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setConfigurationProfile": [
  "SELECT * FROM platform.configuration_profile WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setConnectivityThresholds": [
  "SELECT * FROM platform.connectivity_policy WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setOfflinePolicy": [
  "SELECT * FROM platform.offline_policy WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setRolePermissions": [
  "SELECT * FROM identity.role LIMIT 50",
  "SELECT * FROM identity.role_permission LIMIT 50",
  "SELECT * FROM identity.segregation_rule WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setStepUpPolicy": [
  "SELECT * FROM approvals.step_up_policy LIMIT 50"
 ],
 "setVenueSettings": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM platform.venue_settings LIMIT 50"
 ],
 "updateOrgUnit": [
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "updateOutlet": [
  "SELECT * FROM platform.outlet LIMIT 50"
 ],
 "updateRegionSettings": [
  "SELECT * FROM platform.region_settings LIMIT 50"
 ],
 "updateRotaAssignment": [
  "SELECT * FROM workforce.rota_assignment LIMIT 50"
 ],
 "updateSaleBoard": [
  "SELECT * FROM platform.sale_board LIMIT 50"
 ],
 "withdrawApprovalRequest": [
  "SELECT * FROM approvals.request WHERE scope_path LIKE $1 LIMIT 50"
 ]
}

WRITES = {
 "acknowledgeAnnouncement": [
  "SELECT id FROM workforce.announcement_receipt ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "amendAttendance": [
  "SELECT id FROM workforce.attendance ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "broadcastToGuests": [
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM workforce.announcement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "configureWorkstation": [
  "SELECT id FROM platform.device ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.workstation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createApprovalDelegation": [
  "SELECT id FROM approvals.delegation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createApprovalRequest": [
  "SELECT id FROM approvals.request WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createOrgUnit": [
  "SELECT id FROM platform.org_unit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createOutlet": [
  "SELECT id FROM platform.outlet ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRotaAssignment": [
  "SELECT id FROM workforce.rota_assignment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createSaleBoard": [
  "SELECT id FROM platform.sale_board ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "decideApprovalRequest": [
  "SELECT id FROM approvals.decision ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM approvals.request WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deployConfigurationProfile": [
  "SELECT id FROM platform.profile_deployment ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.workstation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "escalateApprovalRequest": [
  "SELECT id FROM approvals.escalation ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM approvals.request WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "issueAccreditationBadge": [
  "SELECT id FROM approvals.accreditation_badge ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "listAuditRecords": [
  "SELECT id FROM platform.audit_read ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "publishAnnouncement": [
  "SELECT id FROM workforce.announcement ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM workforce.announcement_receipt ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordAttendance": [
  "SELECT id FROM workforce.attendance ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordDeviceHeartbeat": [
  "SELECT id FROM platform.device ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "registerDevice": [
  "SELECT id FROM platform.device ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "requestShiftSwap": [
  "SELECT id FROM approvals.request WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM workforce.shift_swap ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "resubmitApprovalRequest": [
  "SELECT id FROM approvals.request WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "revokeApprovalDelegation": [
  "SELECT id FROM approvals.delegation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setApprovalMatrix": [
  "SELECT id FROM approvals.matrix WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM approvals.rule ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setConfigurationProfile": [
  "SELECT id FROM platform.configuration_profile WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setConnectivityThresholds": [
  "SELECT id FROM platform.connectivity_policy WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setOfflinePolicy": [
  "SELECT id FROM platform.offline_policy WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setRolePermissions": [
  "SELECT id FROM identity.role_permission ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.audit_record ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setStepUpPolicy": [
  "SELECT id FROM approvals.step_up_policy ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setVenueSettings": [
  "SELECT id FROM platform.venue_settings ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateOrgUnit": [
  "SELECT id FROM platform.org_unit ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateOutlet": [
  "SELECT id FROM platform.outlet ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateRegionSettings": [
  "SELECT id FROM platform.region_settings ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateRotaAssignment": [
  "SELECT id FROM workforce.rota_assignment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateSaleBoard": [
  "SELECT id FROM platform.sale_board ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "withdrawApprovalRequest": [
  "SELECT id FROM approvals.request WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "acknowledgeAnnouncement": [
  "cache:idempotency:bench"
 ],
 "amendAttendance": [
  "cache:idempotency:bench"
 ],
 "broadcastToGuests": [
  "cache:idempotency:bench"
 ],
 "configureWorkstation": [
  "cache:idempotency:bench"
 ],
 "createApprovalDelegation": [
  "cache:idempotency:bench"
 ],
 "createApprovalRequest": [
  "cache:idempotency:bench"
 ],
 "createOrgUnit": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "createOutlet": [
  "cache:idempotency:bench"
 ],
 "createRotaAssignment": [
  "cache:idempotency:bench"
 ],
 "createSaleBoard": [
  "cache:idempotency:bench"
 ],
 "decideApprovalRequest": [
  "cache:idempotency:bench"
 ],
 "deployConfigurationProfile": [
  "cache:idempotency:bench"
 ],
 "escalateApprovalRequest": [
  "cache:idempotency:bench"
 ],
 "evaluateApprovalRequirement": [
  "cache:idempotency:bench"
 ],
 "getOrgUnit": [
  "cache:resolution:bench"
 ],
 "getRegionSettings": [
  "cache:resolution:bench"
 ],
 "getVenueSettings": [
  "cache:resolution:bench"
 ],
 "listAuditRecords": [
  "cache:idempotency:bench"
 ],
 "listOrgUnits": [
  "cache:resolution:bench"
 ],
 "publishAnnouncement": [
  "cache:idempotency:bench"
 ],
 "recordAttendance": [
  "cache:idempotency:bench"
 ],
 "registerDevice": [
  "cache:idempotency:bench"
 ],
 "requestShiftSwap": [
  "cache:idempotency:bench"
 ],
 "resubmitApprovalRequest": [
  "cache:idempotency:bench"
 ],
 "revokeApprovalDelegation": [
  "cache:idempotency:bench"
 ],
 "setApprovalMatrix": [
  "cache:idempotency:bench"
 ],
 "setConfigurationProfile": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setConnectivityThresholds": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setOfflinePolicy": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setRolePermissions": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setVenueSettings": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "updateOrgUnit": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "updateOutlet": [
  "cache:idempotency:bench"
 ],
 "updateRegionSettings": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "updateRotaAssignment": [
  "cache:idempotency:bench"
 ],
 "updateSaleBoard": [
  "cache:idempotency:bench"
 ],
 "withdrawApprovalRequest": [
  "cache:idempotency:bench"
 ]
}
