# P09 TICVAI Web — operations per screen (from screens/P09-platform-admin-console.yaml)

37 declared; YAML runs ADM-001 … ADM-102+ (65+ extra, no operations).
110 operations, 9 contracts, 9 modules. Waves: w1 11 · w2 16 · w3 10.

## Repeated blocks

CELL-BLOCK (7, `subscription`): getCell, getCellHealth, getCellCapacity, listCellJobs,
updateCellTier, decommissionCell, cancelDecommission.
Declared identically on: ADM-013, ADM-014, ADM-030, ADM-032, ADM-033, ADM-034 (7 each),
and inside ADM-003 (+3 cross-region) and ADM-029 (+5 platform-ops rollout).
→ A WAF policy view, a backup status page and an archival monitor can each decommission a cell.

TENANT-READ (6): listTenants, getTenant, getTenantLicences, getEntitlementUsage,
listTenantCells (`subscription`) + getSsoConfig (`identity`).
Declared on ADM-002, 005, 006, 007, 008, 009, 010, 011, 012, 015 — ten screens.
getSsoConfig is residue on all of them except ADM-005 (which also has setSsoConfig).

## Per screen

- ADM-001 Login (Access, w1, 8) identity: login, getCurrentSession, listSsoProviders,
  listMfaMethods, listActiveSessions, forceLogout, revokeAllSessions, getGuestSession (flag —
  4th login screen with the identical set, after SUP-001, PTR-001).
- ADM-002 Platform Dashboard (Overview, w1, 6): TENANT-READ.
- ADM-003 Cross-Tenant Health (Overview, w2, 10): CELL-BLOCK + cross-region
  propagateCrossRegionEntitlement, getCrossRegionEntitlement, reconcileRedemptions.
- ADM-004 Platform Audit Log (Overview, w2, 1): listAiInteractions (`ai`) ONLY — an audit log
  that can only list AI interactions. Needs a platform audit read; none exists.
- ADM-005 Tenant Directory (Tenants, w1, 15): TENANT-READ + createTenant, updateTenant,
  suspendTenant, terminateTenant, reactivateTenant, provisionCell, addLicenceAddOn,
  removeLicenceAddOn, setSsoConfig. (cancelSubscription unreached — see gap list.)
- ADM-006 Tenant Hierarchy Explorer (Tenants, w1, 9): TENANT-READ + updateTenant +
  tenancy listOrgUnits, createOrgUnit.
- ADM-007 Module & Feature Entitlement (Tenants, w1, 9): TENANT-READ + getSubscription,
  addLicenceAddOn, removeLicenceAddOn.
- ADM-008 Subscription & Plan Management (Tenants, w1, 19): listPlans, getPlan, createPlan,
  createPlanVersion, getSubscription, setSubscription, previewSubscriptionChange,
  generateInvoice, listSubscriptionInvoices, getUsageMetering, listPartnerAgreements,
  createPartnerAgreement, updatePartnerAgreement + TENANT-READ.
- ADM-009 Tenant Billing & Invoicing (Tenants, w2, 9): listSubscriptionInvoices, generateInvoice,
  getSubscription + TENANT-READ. (cancelInvoice, disputeInvoice unreached.)
- ADM-010 Usage Metering (Tenants, w2, 7): getUsageMetering + TENANT-READ.
- ADM-011 Licence & Seat Management (Tenants, w2, 11): addLicenceAddOn, removeLicenceAddOn,
  getSubscription, setSubscription, previewSubscriptionChange + TENANT-READ.
- ADM-012 Tenant Isolation & Resource Pool (Tenants, w1, 8): provisionCell, getCellCapacity + TENANT-READ.
- ADM-013 Tenant Performance Monitor (Overview, w2, 7): CELL-BLOCK.
- ADM-014 Auto-Scaling Configuration (Infra, w3, 7): CELL-BLOCK.
- ADM-015 API Rate Limit & Quota (Tenants, w3, 9): TENANT-READ (minus listTenantCells? incl) +
  public-api setApiQuota, getApiUsage, listApiClients → duplicates P14 DEV-006/DEV-008.
- ADM-016 White-Label Branding (Branding, w2, 11) white-label: getBrandIdentity, setBrandIdentity,
  getTheme, setTheme, getAppIcons, setAppIcons, createPreview, diffConfigVersion,
  listConfigVersions, publishTenantConfig, restoreConfigVersion → duplicates P13 CMS-002/005/006/014.
- ADM-017 Domain & Certificate (Branding, w2, 4) white-label: listCustomDomains, claimCustomDomain,
  verifyCustomDomain, releaseCustomDomain → these are exactly what CMS-017 lacks (it declares none).
- ADM-018 Localisation & Language Pack (Branding, w2, 5) white-label: setLanguages, listFaqs,
  setFaqs, listPolicies, setPolicy.
- ADM-019 Global Configuration & Defaults (Branding, w2, 4) subscription: listPlans, getPlan,
  createPlan, createPlanVersion → plan CRUD on a defaults screen; ADM-008 owns plans.
- ADM-020 Platform User Directory (Access, w1, 4) identity: listPrincipals, getPrincipal,
  createPrincipal, updatePrincipal.
- ADM-021 Platform Role Management (Access, w1, 2) identity: listRoles, createRole — no update,
  no delete, no assignment. (setSegregationRules, setPasswordPolicy unreached.)
- ADM-022 Release & Version Management (Releases, w2, 7) platform-ops: listReleases, getRelease,
  getReleaseReadiness, createRelease, promoteRelease, rejectRelease, withdrawRelease.
- ADM-023 Staging Promotion & Approval (Releases, w2, 7): the identical seven as ADM-022.
- ADM-024 Release Notification Composer (Releases, w3, 2→3): publishSupportNotice,
  listSupportNotices, listReleases.
- ADM-025 Tenant Upgrade Scheduler (Releases, w2, 2): listUpgradeSchedules, scheduleTenantUpgrade.
- ADM-026 End-of-Support Notice (Releases, w3, 2→3): listSupportNotices, publishSupportNotice,
  deprecateApiVersion (public-api) → also on DEV-008.
- ADM-027 Database Migration Console (Releases, w1, 6) platform-ops: listMigrations, planMigration,
  applyMigration, getMigrationRun, rollbackMigrationRun, getVersionSkew.
- ADM-028 Environment Registry (Releases, w2, 2): listEnvironments, registerEnvironment.
- ADM-029 Deployment Monitor (Overview, w2, 12): platform-ops listRollouts, getRollout, startRollout,
  pauseRollout, rollbackRollout + CELL-BLOCK (minus cancelDecommission? incl) + listCellJobs.
  (skipRolloutCell, listDeadLetters, replayDeadLetter unreached.)
- ADM-030 Infrastructure Sizing & Scaling Policy (Infra, w3, 7): CELL-BLOCK.
- ADM-031 Security & Compliance Dashboard (Security, w3, 4) reporting: listDashboards, getDashboard,
  createDashboard, updateDashboard → generic dashboard CRUD, nothing compliance-specific.
- ADM-032 WAF & Security Policy View (Security, w3, 7): CELL-BLOCK — no WAF operation exists.
- ADM-033 Backup & DR Status (Infra, w2, 7): CELL-BLOCK — no backup operation exists. (CF-64 open.)
- ADM-034 Archival Job Monitor (Infra, w3, 7): CELL-BLOCK — no archival operation exists.
- ADM-035 Support & Escalation Console (Support, w3, 2): listSupportNotices, publishSupportNotice.
- ADM-036 Platform Notification Broadcast (Support, w3, 2→4): publishSupportNotice,
  listSupportNotices + workforce listAnnouncements, publishAnnouncement (flag — staff-app
  announcements on a platform broadcast screen).
- ADM-037 AI Provider & Credentials (AI, w1, 4) ai: listAiProviders, setAiProvider, setAiCredential,
  testAiProvider.

## Gap list highlights (77 with no screen)
ai: 11 knowledge/index/translation ops. cross-region: 5 wallet ops (authoriseWalletSpend etc).
identity: setPasswordPolicy, setSegregationRules. platform-ops: listDeadLetters, replayDeadLetter,
skipRolloutCell. reporting: 12 (report execution/schedule/export, listAlertRules).
subscription: cancelInvoice, cancelSubscription, disputeInvoice, createPartnerUser,
executeTenantMigration, exportPartnerInvoice, drain/decommissionBurstEnvironment … +37 more.
