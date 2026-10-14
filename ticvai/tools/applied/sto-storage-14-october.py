#!/usr/bin/env python3
"""One-off, batch STO (Block A storage audit, 14 October 2026): where each persisted array and field is stored.
Already applied; kept as the record of what was changed and why. Idempotent.

* CHG-STO-010 (check-storage-promises SP-ARRAY-NOWHERE, check-contract-storage ST-FIELD-NO-COLUMN): an array of objects
  that no column and no child table held is now one of two things, decided per field:
  - **stored whole with its row** (`x-ticvai-persistence-kind: valueObject`, `x-ticvai-persistence-column: jsonb`,
    the form `AiGovernanceRuleList` and `KitchenRoutingRules.categoryRules` already use): a configuration list read and
    written with the record that owns it (bands, tiers, windows, rules, steps, thresholds), a job's findings, a
    decision's trace, a record's own history of actions. Nothing queries one element on its own, and a child table
    would be rows with no identity a caller ever addresses. A list of Money is `numeric(18,4)[]` (the amounts; the
    currency resolves as every Money column's does).
  - **worked out on read** (`x-ticvai-persisted: false`): a view's list read from the table that holds it (a media
    asset's collections, renditions, versions; a visit plan's days are its `venuemap.visit_plan_item` rows), or
    computed at read time (a cart's conflicts and consent questions, a booking's readiness, a leave request's
    coverage impact, a privacy change set's simulation; the waiver workspace's checklist and AI findings, as its
    persistence note already said).
  `ProductDisplayTag` and `TransportNetworkImportFinding` said "jsonb column on ..." and got none: the field now
  declares it.
* CHG-STO-014 (ST-SECRET-FORM, SR-SECRET-UNHASHED): every stored write-only secret says how it is kept (SECRETS below).
* CHG-STO-015 (ST-ENUM-CHECK): `UrlRedirect.statusCode` is stored as an integer and `CookieScanPolicy.frequency`
  quotes `off`, so derive-ddl gives each its CHECK.
* CHG-STO-011 (ST-FIELD-NO-COLUMN): `orders.EntitlementSummary` is one entitlement as a guest sees it, assembled from
  `access.entitlement` and the product; it is not stored in `catalogue.entitlement_template` (its persistence said
  so, and eight fields had no column there). The marketing campaign's `Invitation` shared its name with Orders'
  complimentary `Invitation`, and derive-schema read Orders' fields into `marketing.invitation` (product_id,
  quantity, offered_by ...), leaving the campaign invitation's own six fields with no column: it is
  `CampaignInvitation` now (a component name; the wire is unchanged).

    python3 tools/applied/sto-storage-14-october.py [--apply]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sto_markers import Contracts  # noqa: E402

# (contract stem, schema, property): stored whole with its row, as jsonb
JSONB = [
    ("accreditation", "AccreditationNotificationRules", "rules"),
    ("accreditation", "AccreditationProgramme", "categories"),
    ("accreditation", "AccreditationRequirements", "rows"),
    ("accreditation", "BadgePrintJob", "failures"),
    ("ai", "AiApprovalRequestScore", "signals"),
    ("ai", "AiDecisionRecord", "annotations"),
    ("ai", "AiForecastScenario", "changes"),
    ("ai", "AiGuidedChoiceSuggestion", "questions"),
    ("ai", "AiHistoryImport", "findings"),
    ("ai", "AiIncident", "containment"),
    ("ai", "AiModel", "taskFitness"),
    ("ai", "AiProvider", "fitnessWarnings"),
    ("ai", "AiRiskCase", "entities"),
    ("ai", "AiRiskStrategy", "outcomeMap"),
    ("ai", "AiVenueSettings", "openingHours"),
    ("approvals", "ApprovalRecord", "policyVersions"),
    ("approvals", "ApprovalSlaPolicy", "reminders"),
    ("assets", "MediaTaxonomy", "categories"),
    ("assets", "MediaTaxonomy", "fields"),
    ("assets", "MediaTaxonomy", "keywordVocabularies"),
    ("catalogue", "CatalogueImportJob", "findings"),
    ("catalogue", "EntitlementTemplate", "validTimeWindows"),
    ("catalogue", "EventRegistration", "participantCategories"),
    ("catalogue", "EventResourcePlan", "contractors"),
    ("catalogue", "EventResourcePlan", "requirements"),
    ("catalogue", "EventSchedule", "performances"),
    ("catalogue", "PerformanceTemplate", "bands"),
    ("catalogue", "Product", "displayTags"),
    ("catalogue", "VariantDimension", "values"),
    ("cross-region", "DsarRequest", "cellResults"),
    ("cross-region", "GuestLink", "linkedCells"),
    ("finance", "EventBudget", "costLines"),
    ("fnb", "FnbReservationPolicy", "turnTimeBands"),
    ("games", "GameOperationalConfig", "operatingHours"),
    ("games", "GamePricing", "calendarExceptions"),
    ("games", "GamePricing", "groupPricing"),
    ("games", "GamePricing", "peakPricing"),
    ("games", "GameplayAuthorisation", "trace"),
    ("games", "RedemptionRules", "earnRules"),
    ("identity", "AccessDecision", "matchedPolicies"),
    ("maintenance", "WorkOrderDetail", "parts"),
    ("maintenance", "WorkOrderDetail", "timeEntries"),
    ("maintenance", "WorkOrderPriorityPolicy", "bands"),
    ("marketing-crm", "ConsentCapturePointCustomerJourneyConfigurationView", "steps"),
    ("marketing-crm", "CookieBannerPreferenceCenterDesignerView", "buttons"),
    ("marketing-crm", "CookieBannerPreferenceCenterDesignerView", "categories"),
    ("marketing-crm", "CookieBannerPreferenceCenterDesignerView", "links"),
    ("marketing-crm", "DataDiscoveryAccessExportCorrectionWorkspaceInput", "corrections"),
    ("marketing-crm", "DataDiscoveryAccessExportCorrectionWorkspaceInput", "identifiers"),
    ("marketing-crm", "DataDiscoveryAccessExportCorrectionWorkspaceView", "corrections"),
    ("marketing-crm", "DataDiscoveryAccessExportCorrectionWorkspaceView", "results"),
    ("marketing-crm", "DeletionAnonymizationRestrictionOperationsView", "systemResults"),
    ("marketing-crm", "DigitalWaiverFormBuilderView", "sections"),
    ("marketing-crm", "DuplicateCandidate", "conflicts"),
    ("marketing-crm", "GuestAttributeModel", "attributes"),
    ("marketing-crm", "GuestAttributeModel", "fieldGroups"),
    ("marketing-crm", "GuestAttributeModel", "identifiers"),
    ("marketing-crm", "IdentityResolutionRules", "matchers"),
    ("marketing-crm", "IdentityResolutionRules", "survivorship"),
    ("marketing-crm", "KioskAssistSession", "actionsTaken"),
    ("marketing-crm", "LocalizationBrandingCustomerExperienceConfigurationView", "languages"),
    ("marketing-crm", "PrivacyConfigurationTestingApprovalPublicationView", "items"),
    ("marketing-crm", "PrivacyRequestTypeConfig", "stages"),
    ("marketing-crm", "QualityManagementAgentEvaluationView", "aiFindings"),
    ("marketing-crm", "QualityManagementAgentEvaluationView", "coachingActions"),
    ("marketing-crm", "QualityManagementAgentEvaluationView", "criteria"),
    ("marketing-crm", "RoutingPriorityThrottlingFallbackRulesView", "providers"),
    ("marketing-crm", "SignatorySignatureGuardianRuleConfigurationView", "guardianThresholdByCountry"),
    ("marketing-crm", "WaiverApprovalTestingPublicationWorkspaceView", "history"),
    ("marketing-crm", "WaiverTriggerEligibilityCompletionRulesView", "eligibility"),
    ("marketing-crm", "WaiverTriggerEligibilityCompletionRulesView", "reminders"),
    ("payments", "ChargebackEvidence", "documents"),
    ("payments", "MixedTenderRules", "allowedCombinations"),
    ("payments", "PaymentRiskRules", "lists"),
    ("payments", "PaymentRiskRules", "rules"),
    ("payments", "PaymentRoutingRule", "targets"),
    ("promotions", "RecommendationExperiment", "variants"),
    ("promotions", "RecommendationSuppression", "hardExclusions"),
    ("public-api", "ApiVersion", "changes"),
    ("rental", "RentalAvailabilityRules", "operatingWindows"),
    ("rental", "RentalFeePolicy", "lateFeeTiers"),
    ("rental", "RentalInspection", "checklist"),
    ("rental", "RentalInventoryModel", "components"),
    ("rental", "RentalPricingProfile", "calendarRules"),
    ("rental", "RentalPricingProfile", "durationTiers"),
    ("reporting", "AnalyticsAnomaly", "candidateCauses"),
    ("reporting", "ReportSubscription", "recipients"),
    ("reporting", "SemanticModel", "domains"),
    ("reporting", "SemanticModel", "relationships"),
    ("resources", "ResourceSchedule", "exceptions"),
    ("resources", "ResourceSchedule", "windows"),
    ("seating", "AccessibleSeating", "spaces"),
    ("seating", "SeatRecommendationRules", "profiles"),
    ("seating", "Section", "boundary"),
    ("subscription", "GoLiveReadiness", "groups"),
    ("subscription", "LicenceEnforcementPolicy", "thresholds"),
    ("subscription", "LicensingModel", "overagePricing"),
    ("subscription", "TenantMigrationPlan", "blockers"),
    ("subscription", "VsiModel", "factors"),
    ("subscription", "VsiModel", "tiers"),
    ("tenancy", "DeviceFirmwareRollout", "waves"),
    ("transport", "TransportNetworkImport", "findings"),
    ("venue-map", "PlacedResource", "boundary"),
    ("venue-map", "VenueMapImportJob", "findings"),
    ("venue-map", "VenuePoint", "media"),
    ("venue-map", "VisitPlan", "excluded"),
    ("wallet", "WalletAccountingMapping", "mappings"),
    ("wallet", "WalletAuthenticationPolicy", "tiers"),
    ("wallet", "WalletConfigurationVersion", "findings"),
    ("wallet", "WalletFundingRules", "bonusRules"),
    ("wallet", "WalletReconciliationSources", "sources"),
    ("white-label", "ConfigVersion", "pendingBuildTimeChanges"),
    ("workforce", "ShiftTemplate", "breaks"),
]
# (contract stem, schema, property): a list of Money, stored as its amounts
MONEY_ARRAYS = [
    ("catalogue", "DonationCampaign", "fixedAmounts"),
    ("wallet", "GiftCardProduct", "denominations"),
    ("wallet", "WalletFundingRules", "presetAmounts"),
]
# (contract stem, schema, property): worked out on read, never stored on the row
NOT_STORED = [
    ("accreditation", "AccreditationApplication", "requirementStatus"),
    ("approvals", "ApprovalRequest", "pendingApprovers"),
    ("assets", "MediaAssetApproval", "eligibility"),
    ("assets", "MediaAssetDetail", "collections"),
    ("assets", "MediaAssetDetail", "derivatives"),
    ("assets", "MediaAssetDetail", "previousVersions"),
    ("assets", "MediaAssetVersion", "usageImpact"),
    ("marketing-crm", "DeletionAnonymizationRestrictionOperationsView", "approvals"),
    ("marketing-crm", "DeletionAnonymizationRestrictionOperationsView", "checks"),
    ("marketing-crm", "DeletionAnonymizationRestrictionOperationsView", "impact"),
    ("marketing-crm", "PrivacyComplianceExceptionInvestigationWorkspaceView", "timeline"),
    ("marketing-crm", "PrivacyConfigurationTestingApprovalPublicationView", "audit"),
    ("marketing-crm", "PrivacyConfigurationTestingApprovalPublicationView", "simulation"),
    ("marketing-crm", "PrivacyConfigurationTestingApprovalPublicationView", "validationIssues"),
    ("marketing-crm", "WaiverApprovalTestingPublicationWorkspaceView", "aiFindings"),
    ("marketing-crm", "WaiverApprovalTestingPublicationWorkspaceView", "checklist"),
    ("orders", "Cart", "conflicts"),
    ("orders", "Cart", "consentQuestions"),
    ("rental", "RentalBooking", "readiness"),
    ("seating", "ImportJob", "findings"),
    ("venue-map", "VisitPlan", "days"),
    ("workforce", "LeaveRequest", "coverageImpact"),
]
# (contract stem, schema, property path, form): how a stored secret is kept (ADR-0063 as amended 14 October 2026,
# ADR-0071; CHG-STO-014, ST-SECRET-FORM). A credential the tenant or we configure for a provider, or a signing
# secret, is a Key Vault secret whose name the row keeps; a per-guest or per-device secret TICVAI must use again is
# field-encrypted; a per-link token TICVAI only ever looks up is its blind index; a password is an Argon2id PHC string.
SECRETS = [
    ("approvals", "ApprovalExternalProvider", "outboundCredential", "vault-reference"),
    ("approvals", "ApprovalExternalProvider", "signingSecret", "vault-reference"),
    ("public-api", "WebhookSubscription", "signingSecret", "vault-reference"),
    ("orders", "PaymentProvider", "credentialRef", "vault-reference"),
    ("payments", "PaymentProviderConnection", "credentialRef", "vault-reference"),
    ("white-label", "StorefrontAnalyticsProvider", "reportingCredentialRef", "vault-reference"),
    ("white-label", "StoreAccount", "apiCredentialSecretRef", "vault-reference"),
    ("white-label", "StoreAccount", "passCertificateSecretRef", "vault-reference"),
    ("identity", "GuestCredential", "passwordHash", "argon2id-phc"),
    ("identity", "PrincipalCredential", "credentialHash", "argon2id-phc"),
    ("identity", "PrincipalCredential", "history[].credentialHash", "argon2id-phc"),
    ("marketing-crm", "MarketingSubscription", "unsubscribeToken", "blind-index"),
    ("orders", "PaymentLink", "token", "blind-index"),
    ("orders", "TicketTransfer", "claimToken", "blind-index"),
    ("orders", "WalletPass", "authenticationToken", "blind-index"),
    ("orders", "PaymentToken", "token", "field-encrypted"),
    ("tenancy", "RegisteredDevice", "pushToken", "field-encrypted"),
]
MARKERS = [
    # CHG-STO-015 (ST-ENUM-CHECK): an HTTP status is a number; stored as one it carries its CHECK (as CHG-CRD-002)
    ("marketing-crm", "UrlRedirect", "statusCode", "x-ticvai-persistence-column", "integer"),
]
SCHEMA_EDITS = [
    # CHG-STO-015 (ST-ENUM-CHECK): YAML read the bare `off` as the boolean false, so the enum was not all strings and
    # derive-ddl gave the column no CHECK; the wire value is the string "off"
    ("marketing-crm", "CookieScanPolicy", "          - monthly\n          - off\n",
     "          - monthly\n          - 'off'\n"),
    # CHG-STO-011: a projection, not a template row
    ("orders", "EntitlementSummary", "      x-ticvai-persistence: catalogue.entitlement_template\n",
     "      x-ticvai-persistence: 'none — projection of access.entitlement and its product, as a guest or a steward "
     "sees it'\n"),
]
# (contract stem, persisted schema, column): Orders' invitation keys the shared name left on marketing.invitation
# through the relationship graph; retired so the graph does not put them back (CHG-STO-011)
RETIRED = [
    ("marketing-crm", "CampaignInvitation", "product_id"),
    ("marketing-crm", "CampaignInvitation", "performance_id"),
    ("marketing-crm", "CampaignInvitation", "offered_by_principal_id"),
    ("marketing-crm", "CampaignInvitation", "issued_by_principal_id"),
    ("marketing-crm", "CampaignInvitation", "cost_center_id"),
]
TEXT_EDITS = [
    # CHG-STO-011: the campaign invitation is not Orders' complimentary Invitation
    ("marketing-crm", "\n    Invitation:\n", "\n    CampaignInvitation:\n"),
    ("marketing-crm", "                $ref: '#/components/schemas/Invitation'\n",
     "                $ref: '#/components/schemas/CampaignInvitation'\n"),
]


def main() -> int:
    apply = "--apply" in sys.argv
    c = Contracts(Path(__file__).resolve().parents[2])
    bad, n = 0, 0
    for stem, schema, prop in JSONB:
        try:
            h1, where = c.set_marker(stem, schema, prop, "x-ticvai-persistence-kind", "valueObject")
            h2, _ = c.set_marker(stem, schema, prop, "x-ticvai-persistence-column", "jsonb")
            n += (h1 != "=") + (h2 != "=")
        except (LookupError, ValueError) as e:
            print("  !", e)
            bad += 1
    for stem, schema, prop in MONEY_ARRAYS:
        try:
            h, where = c.set_marker(stem, schema, prop, "x-ticvai-persistence-column", "'numeric(18,4)[]'")
            n += h != "="
        except (LookupError, ValueError) as e:
            print("  !", e)
            bad += 1
    for stem, schema, prop in NOT_STORED:
        try:
            h, where = c.set_marker(stem, schema, prop, "x-ticvai-persisted", False)
            n += h != "="
        except (LookupError, ValueError) as e:
            print("  !", e)
            bad += 1
    for stem, schema, prop, form in SECRETS:
        try:
            h, where = c.set_marker(stem, schema, prop, "x-ticvai-secret", form)
            n += h != "="
        except (LookupError, ValueError) as e:
            print("  !", e)
            bad += 1
    for stem, schema, prop, key, value in MARKERS:
        try:
            h, where = c.set_marker(stem, schema, prop, key, value)
            n += h != "="
        except (LookupError, ValueError) as e:
            print("  !", e)
            bad += 1
    for stem, schema, old, new in SCHEMA_EDITS:
        try:
            n += c.replace_in_schema(stem, schema, old, new) != "="
        except LookupError as e:
            print("  !", e)
            bad += 1
    for stem, old, new in TEXT_EDITS:
        try:
            n += c.replace_text(stem, old, new) != "="
        except LookupError as e:
            print("  !", e)
            bad += 1
    for stem, schema, col in RETIRED:
        try:
            n += c.add_retired(stem, schema, col) != "="
        except LookupError as e:
            print("  !", e)
            bad += 1
    print(f"  {n} edit(s), {bad} not found")
    if apply and not bad:
        print("  wrote", ", ".join(c.save()) or "nothing")
    elif not apply:
        print("dry run; pass --apply")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
