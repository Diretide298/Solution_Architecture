# Workshop pack — the contract gap, as named operations

**Derived by `tools/derive-pack-linkage.py`. Regenerate rather than editing.**

| | |
|---|---:|
| Pack screens | 1924 |
| Wired to an operation that exists | **629** |
| Candidate match below the threshold | 198 |
| No operation exists | **1097** |
| Distinct operations to author | **1305** |

## How these were derived

A screen's operations follow from **what entity it acts on and what it does to it**, and this pack titles every screen after both — `Access Point Directory` is a list of access points, `Offline Validation Policy Builder` sets an offline policy. Matched against operation names that is precise: `listAccessPoints`, `setOfflinePolicy`, `enrolFacePass`, `listQueues`, `setBrandIdentity` all came out of it.

**Two weaker signals were tried first and both failed the same way** — the terms they agree on are the generic ones. Bag-of-words over summaries and tables put eight unrelated screens on `listScans` at 0.75. Joining the field lists through the schema resolved only 9% of 4,756 field terms, and the ones that resolved were `status`, `owner` and `channel`, so `Pricing Rule Command Center` came back pointing at `pii.subject`.

**A proposed name is a specification, not a decision.** The verb comes from the archetype and the entity from the title; the shape of the request and response does not follow from either, and neither does the permission, the scope level or the audience. Those are the parts a person writes.

## ACCREDITATION — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Accreditation Command Center | `listAccreditation` |
| Accreditation Application Directory | `listAccreditationApplication` |
| New Accreditation Application | `listNewAccreditationApplication` |
| Accreditation Form Builder | `setAccreditationForm` |
| Accreditation Category Management | `listAccreditationCategory` |
| Accreditation Program Setup | `setAccreditationProgram` |
| Applicant Type Configuration | `setApplicantType` |
| Application Requirements Matrix | `listApplicationRequirementMatrix` |
| Accreditation Intake Monitor | `listAccreditationIntake` |
| Registration Rules & Publication | `publishRegistrationRule` |

## ACCREDITATION — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Accreditation Holder Directory | `listAccreditationHolder` |
| Accreditation Holder Profile | `listAccreditationHolderProfile` |
| Identity Details & Verification | `listIdentityDetailVerification` |
| Photo Management | `listPhoto` |
| Document Repository | `listDocumentRepository` |
| Document Verification Queue | `listDocumentVerificationQueue` |
| Duplicate & Identity Conflict Detection | `listDuplicateIdentityConflict` |
| Organization & Affiliation Management | `listOrganizationAffiliation` |
| Profile Completeness & Compliance Monitor | `listProfileCompletenessCompliance` |
| Profile History & Audit Timeline | `listProfileTimeline` |

## ACCREDITATION — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Accreditation Review Queue | `listAccreditationReviewQueue` |
| Application Review Workspace | `setApplicationReview` |
| Approval Rules & Conditions | `approveRuleCondition` |
| Reviewer Assignment & Delegation | `setReviewerDelegation` |
| Rejection & Resubmission Management | `listRejectionResubmission` |
| Escalation & Exception Management | `listEscalationException` |
| Approval SLA & Workload Monitor | `approveSlaWorkload` |
| Approval SLA & Workload Monitor | `listSlaWorkload` |
| Approval Policy Validation & Publication | `approvePolicyValidation` |
| Approval Policy Validation & Publication | `publishPolicyValidation` |

## ACCREDITATION — board 4

7 screens · 7 operations to author

| Screen | Operation to author |
|---|---|
| Credential Generation Workspace | `setCredentialGeneration` |
| Credential Media Configuration | `setCredentialMedia` |
| Badge Template Designer | `setBadgeTemplate` |
| Badge Printing & Print Queue | `listBadgePrintingPrint` |
| Digital & Mobile Credential Management | `listDigitalMobileCredential` |
| NFC & RFID Credential Encoding | `listNfcRfidCredential` |
| Credential Activation & Delivery | `listCredentialActivationDelivery` |

## ACCREDITATION — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Accreditation Access Command Center | `listAccreditationAccess` |
| Access Profile Management | `listAccessProfile` |
| Venue & Zone Access Matrix | `listVenueZoneAccess` |
| Operational Area Permission Management | `listOperationalAreaPermission` |
| Date & Time Access Rules | `listDateTimeAccess` |
| Access Schedule Management | `listAccessSchedule` |
| Holder Access Assignment | `setHolderAccess` |
| Temporary Access & Exception Management | `listTemporaryAccessException` |
| Access Revocation & Suspension | `listAccessRevocationSuspension` |
| Access Rights Preview, Impact & Synchronization | `listAccessRightPreview` |

## ACCREDITATION — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Accreditation Lifecycle Command Center | `listAccreditationLifecycle` |
| Accreditation Status Workflow | `listAccreditationStatuWorkflow` |
| Validity Period Configuration | `setValidityPeriod` |
| Event & Venue Accreditation Assignment | `setEventVenueAccreditation` |
| Multi-Venue Accreditation Management | `listMultiVenueAccreditation` |
| Temporary & Seasonal Accreditation | `listTemporarySeasonalAccreditation` |
| Suspension & Reactivation Management | `listSuspensionReactivation` |
| Accreditation Revocation Management | `listAccreditationRevocation` |
| Expiry Monitor & Expiration Rules | `listExpiryExpirationRule` |
| Accreditation Renewal Workspace | `setAccreditationRenewal` |

## ACCREDITATION — board 7

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Accreditation Communications Command Center | `listAccreditationCommunication` |
| Notification Rule Management | `listNotificationRule` |
| Expiry & Renewal Notification Scheduler | `listExpiryRenewalNotification` |
| Communication Template Library | `listCommunicationTemplate` |
| Channel, Language & Branding Configuration | `setChannelLanguageBranding` |
| Manual & Bulk Communication Center | `listManualBulkCommunication` |
| Accreditation Bulk Import | `listAccreditationBulkImport` |
| Import Validation & Processing Monitor | `listImportValidationProcessing` |
| Accreditation Export & Data Extract Center | `listAccreditationExportData` |
| Delivery, Batch & Operational History | `listDeliveryBatchOperational` |

## ACCREDITATION — board 8

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Accreditation Executive Dashboard | `listAccreditationExecutive` |
| Accreditation Status & Portfolio Reporting | `listAccreditationStatuPortfolio` |
| Accreditation Utilization Analytics | `listAccreditationUtilization` |
| Accreditation Access Activity Reporting | `listAccreditationAccessActivity` |
| Accreditation Trend & Comparative Analysis | `listAccreditationTrendComparative` |
| Accreditation Audit Reporting | `listAccreditationReporting` |
| Immutable Accreditation Audit Log | `listImmutableAccreditation` |
| Accreditation API Management | `listAccreditationApi` |
| Accreditation Webhook Management | `listAccreditationWebhook` |
| Integration & Data Exchange Monitor | `listIntegrationDataExchange` |

## AI Configuration Assistant — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| AI Configuration Home & Start | `setHomeStart` |
| Setup Type & Business Intent Discovery | `setTypeBusinessIntent` |
| Venue & Business Model Discovery | `listVenueBusinessModel` |
| Guided Question & Answer Workspace | `setGuidedQuestionAnswer` |
| Product & Admission Model Discovery | `listProductAdmissionModel` |
| Operational Requirement Discovery | `listOperationalRequirementDiscovery` |
| Commercial Requirement Discovery | `listCommercialRequirementDiscovery` |
| Required, Recommended & Optional Decisions | `listRequiredRecommendedOptional` |
| Missing Information & Clarification Center | `listMissingInformationClarification` |
| Configuration Blueprint & Dependency Map | `setBlueprintDependencyMap` |

## AI Configuration Assistant — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| AI Configuration Build Command Center | `listBuild` |
| AI Configuration Build Command Center | `setBuild` |
| Venue & Organization Configuration | `setVenueOrganization` |
| Product Configuration Assistant | `setProductAssistant` |
| Schedule, Capacity & Availability Configuration | `setScheduleCapacityAvailability` |
| Promotion, Bundle & Upsell Configuration | `setPromotionBundleUpsell` |
| Seating, Access & Operational Configuration | `setSeatingAccessOperational` |
| Channel, Media & Fulfillment Configuration | `setChannelMediaFulfillment` |
| Cross-Module Conflict & Dependency Validation | `listCrossModuleConflict` |
| Configuration Preview & Impact Analysis | `setPreviewImpactAnalysi` |

## AI Configuration Assistant — board 3

15 screens · 15 operations to author

| Screen | Operation to author |
|---|---|
| AI Configuration Readiness Center | `listReadiness` |
| AI Configuration Readiness Center | `setReadiness` |
| Configuration Validation Results | `setValidationResult` |
| AI Recommendations & Best-Practice Review | `listRecommendationBestPractice` |
| AI Configuration Execution Center | `create` |
| AI Configuration Execution Center | `list` |
| AI Configuration Execution Center | `set` |
| Execution Progress & Dependency Monitor | `createProgressDependency` |
| Execution Progress & Dependency Monitor | `listProgressDependency` |
| Configuration Results & Object Mapping | `setResultObjectMapping` |
| Configuration Change & Modification Assistant | `setChangeModificationAssistant` |
| Configuration History, Versions & Rollback | `listVersionRollback` |
| Configuration History, Versions & Rollback | `setVersionRollback` |
| AI Configuration Audit & Governance | `listGovernance` |
| AI Configuration Audit & Governance | `setGovernance` |

## AI Forecasting and Predictive Intelligence — board 1

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| Forecasting Command Center | `list` |
| Forecast Configuration & Forecasting Strategy | `listForecastStrategy` |
| Forecast Configuration & Forecasting Strategy | `setForecastStrategy` |
| Forecast Data & Signal Configuration | `setForecastDataSignal` |
| Attendance & Visitation Forecast | `listAttendanceVisitationForecast` |
| Ticket, Product & Timeslot Demand Forecast | `listTicketProductTimeslot` |
| Channel & Booking Pace Forecast | `listChannelBookingPace` |
| Revenue & Commercial Forecast | `listRevenueCommercialForecast` |
| Forecast Drivers, Confidence & Explainability | `listForecastDriverConfidence` |
| Forecast Scenario & What-If Simulator | `listForecastScenarioWhat` |
| Forecast Accuracy, Review & Publication Center | `listForecastAccuracyReview` |
| Forecast Accuracy, Review & Publication Center | `publishForecastAccuracyReview` |

## AI Forecasting and Predictive Intelligence — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Operational Forecasting Command Center | `listOperational` |
| Capacity & Occupancy Forecast | `listCapacityOccupancyForecast` |
| Attraction Utilization & Queue Forecast | `listAttractionUtilizationQueue` |
| Entry, Access & Guest Flow Forecast | `listEntryAccessGuest` |
| Workforce Demand & Staffing Forecast | `listWorkforceDemandStaffing` |
| POS, Kiosk & Frontline Service Forecast | `listPosKioskFrontline` |
| F&B, Retail & Inventory Demand Forecast | `listRetailInventoryDemand` |
| Resource, Equipment & Facility Requirement Forecast | `listResourceEquipmentFacility` |
| Operational Scenario & Readiness Simulator | `listOperationalScenarioReadiness` |
| Operational Forecast Review, Recommendations & Handover | `listOperationalForecastReview` |

## AI Governance — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| AI Governance Command Center | `listGovernance` |
| AI Capability Registry & Ownership | `listCapabilityOwnership` |
| AI Risk Classification & Assessment | `listRiskClassificationAssessment` |
| AI Autonomy Level Configuration | `setAutonomyLevel` |
| AI Action & Permission Policy Builder | `setActionPermissionPolicy` |
| AI Data Access & Usage Policy | `listDataAccessUsage` |
| Environment, Tenant & Scope Governance | `listEnvironmentTenantScope` |
| AI Policy Conflict, Exception & Override Management | `listPolicyConflictException` |
| AI Policy Testing & Governance Simulation | `simulatePolicyTestingGovernance` |
| AI Governance Policy Publication & Effective Policy Map | `publishGovernancePolicyEffective` |

## AI Governance — board 2

14 screens · 14 operations to author

| Screen | Operation to author |
|---|---|
| AI Human Oversight Command Center | `listHumanOversight` |
| AI Approval Requirement & Routing Configuration | `approveRequirementRouting` |
| AI Approval Requirement & Routing Configuration | `setRequirementRouting` |
| AI Approval Review Workspace | `approveReview` |
| AI Approval Review Workspace | `setReview` |
| Conditional Approval & Approval Conditions | `approveConditionalCondition` |
| Human Review, Challenge & AI Clarification Workspace | `setHumanReviewChallenge` |
| Escalation, Delegation & Approval SLA Management | `approveEscalationDelegationSla` |
| Escalation, Delegation & Approval SLA Management | `listEscalationDelegationSla` |
| Live AI Execution Oversight & Human Intervention | `createLiveOversightHuman` |
| Human Override & Manual Control Center | `listHumanOverrideManual` |
| Approval & Intervention History / Decision Timeline | `approveInterventionDecisionTimeline` |
| Approval & Intervention History / Decision Timeline | `listInterventionDecisionTimeline` |
| Human Oversight Workflow Simulator & Readiness Center | `listHumanOversightWorkflow` |

## AI Governance — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| AI Explainability & Audit Command Center | `listExplainability` |
| AI Decision Explorer & Search | `listDecisionSearch` |
| AI Decision Explanation Workspace | `setDecisionExplanation` |
| Data, Feature & Evidence Provenance | `listDataFeatureEvidence` |
| Candidate, Rule & Decision Path Trace | `listCandidateRuleDecision` |
| Model, Provider & AI Runtime Trace | `listModelProviderRuntime` |
| Governance, Approval & Human Decision Trace | `approveGovernanceHumanDecision` |
| Execution & Business Outcome Trace | `createBusinessOutcomeTrace` |
| AI Audit Record & Evidence Package | `listRecordEvidencePackage` |
| AI Trace Investigation & Replay Simulator | `listTraceInvestigationReplay` |

## AI Governance — board 4

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| AI Risk Register & Risk Exposure Management | `listRiskExposure` |
| AI Governance Control Library & Control Effectiveness | `listGovernanceEffectiveness` |
| AI Policy Compliance & Violation Monitoring | `listPolicyComplianceViolation` |
| AI Data, Privacy & Usage Compliance Monitoring | `listDataPrivacyUsage` |
| AI Quality, Behavior & Governance Drift Monitoring | `listQualityBehaviorGovernance` |
| AI Governance Alert & Detection Center | `listGovernanceAlertDetection` |
| AI Incident & Remediation Management | `listIncidentRemediation` |
| AI Compliance, Assurance & Governance Reporting | `listComplianceAssuranceGovernance` |
| AI Governance Review, Action Plan & Continuous Improvement | `listGovernanceReviewAction` |

## Access Control Module — board 12

3 screens · 3 operations to author

| Screen | Operation to author |
|---|---|
| Graphical Access Map & Live Gate Performance | `listGraphicalAccessMap` |
| Guest Dwell Time, Length of Stay & Attraction Flow | `listGuestDwellTime` |
| Access Reports, Scheduled Reporting & Data Export | `listAccessReportScheduled` |

## Access Control Module — board 8

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| Special Event, Free View & Alternative Admission | `listSpecialEventFree` |

## Approval Workflows and Governance — board 1

16 screens · 14 operations to author

| Screen | Operation to author |
|---|---|
| Approval Command Center Dashboard | `approve` |
| Approval Command Center Dashboard | `list` |
| My Approval Inbox | `approve` |
| My Approval Inbox | `list` |
| Team / Shared Approval Queue | `approveTeamSharedQueue` |
| Approval Request Detail | `approveRequestDetail` |
| AI Decision Support | `listDecisionSupport` |
| High Priority & Risk Queue | `listHighPriorityRisk` |
| Escalated Approval Center | `approveEscalated` |
| Escalated Approval Center | `listEscalated` |
| Completed Approval History | `approveCompleted` |
| Completed Approval History | `listCompleted` |
| Approval SLA & Workload Monitor | `approveSlaWorkload` |
| Approval SLA & Workload Monitor | `listSlaWorkload` |
| Approval Activity & Notification Center | `approveActivityNotification` |
| Approval Activity & Notification Center | `listActivityNotification` |

## Approval Workflows and Governance — board 2

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Create Approval Workflow | `approveCreateWorkflow` |
| Approval Stage Configuration | `approveStage` |
| Approval Stage Configuration | `setStage` |
| Condition & Decision Rule Builder | `setConditionDecisionRule` |
| Approval Sequence & Parallel Routing | `approveSequenceParallelRouting` |
| Workflow Outcome & Action Configuration | `setWorkflowOutcomeAction` |
| Workflow Validation & Simulation | `simulateWorkflowValidation` |
| Workflow Publication & Lifecycle | `publishWorkflowLifecycle` |
| Workflow Versioning & Change History | `listWorkflowVersioningChange` |

## Approval Workflows and Governance — board 3

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Approval Matrix Command Center | `approveMatrix` |
| Approval Matrix Command Center | `listMatrix` |
| Approval Authority Matrix | `approveAuthorityMatrix` |
| Organizational Hierarchy Routing | `listOrganizationalHierarchyRouting` |
| Department-Based Approval Matrix | `approveDepartmentBasedMatrix` |
| Venue & Tenant Approval Matrix | `approveVenueTenantMatrix` |
| Value & Threshold Routing | `listValueThresholdRouting` |
| Risk-Based & Conditional Routing | `listRiskBasedConditional` |
| Approver Group & Decision Policy | `listApproverGroupDecision` |
| Routing Simulator & Conflict Detection | `listRoutingSimulatorConflict` |
| AI Routing Advisor & Matrix Optimization | `listRoutingAdvisorMatrix` |

## Approval Workflows and Governance — board 4

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Business Context & Evidence Viewer | `listBusinessContextEvidence` |
| Approval Timeline & Decision Chain | `approveTimelineDecisionChain` |
| Approve & Sensitive Action Confirmation | `listApproveSensitiveAction` |
| Reject / Return / Request Information | `listRejectReturnRequest` |
| Requester Modification & Resubmission | `listRequesterModificationResubmission` |
| Withdrawal, Cancellation, Expiration & Reopening | `listWithdrawalCancellationExpiration` |
| Segregation of Duties & Four-Eyes Control | `listSegregationDutyFour` |
| Approved Action Execution & Status | `createApprovedActionStatu` |
| Decision Record & Immutable Audit View | `listDecisionRecordImmutable` |

## Approval Workflows and Governance — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Delegation & Escalation Command Center | `listDelegationEscalation` |
| Temporary Delegation & Availability Calendar | `listTemporaryDelegationAvailability` |
| Out-of-Office & Substitute Routing | `listOutOfficeSubstitute` |
| Approval SLA Policy Configuration | `approveSlaPolicy` |
| Approval SLA Policy Configuration | `setSlaPolicy` |
| Reminder & Breach Notification Rules | `listReminderBreachNotification` |
| Escalation Policy Builder | `setEscalationPolicy` |
| Live Escalation Operations Center | `listLiveEscalation` |
| SLA & Escalation Performance Analytics | `listSlaEscalationPerformance` |
| AI SLA & Escalation Advisor | `listSlaEscalationAdvisor` |

## Approval Workflows and Governance — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Governance & Compliance Command Center | `listGovernanceCompliance` |
| Segregation of Duties Policy Manager | `listSegregationDutyPolicy` |
| Four-Eyes & Dual-Control Policy | `listFourEyeDual` |
| Authentication & MFA Policy Manager | `listAuthenticationMfaPolicy` |
| Sensitive Action Confirmation | `listSensitiveActionConfirmation` |
| Digital Signature Management | `listDigitalSignature` |
| Immutable Approval Record & Tamper Detection | `approveImmutableRecordTamper` |
| Approval Record Retention Policy | `approveRecordRetentionPolicy` |
| Regulatory Audit & Evidence Center | `listRegulatoryEvidence` |
| Governance Risk & AI Compliance Advisor | `listGovernanceRiskCompliance` |

## Approval Workflows and Governance — board 7

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| Approval Integration Command Center | `approveIntegration` |
| Approval Integration Command Center | `listIntegration` |
| Module Integration Registry | `listModuleIntegration` |
| Approval API Management | `approveApi` |
| Approval API Management | `listApi` |
| Workflow Event Framework | `listWorkflowEventFramework` |
| Webhook Configuration & Subscription Manager | `setWebhookSubscriptionManager` |
| External Workflow System Integration | `listExternalWorkflowSystem` |
| Data & Workflow Mapping Studio | `setDataWorkflowMapping` |
| Integration Security & Access Control | `listIntegrationSecurityAccess` |
| Integration Monitoring, Error & Retry Center | `listIntegrationMonitoringError` |
| Integration Analytics & AI Health Advisor | `listIntegrationHealthAdvisor` |

## Approval Workflows and Governance — board 8

14 screens · 14 operations to author

| Screen | Operation to author |
|---|---|
| Approval Executive KPI Dashboard | `approveExecutiveKpi` |
| Approval Executive KPI Dashboard | `listExecutiveKpi` |
| Approval Volume & Outcome Analytics | `approveVolumeOutcome` |
| Approval Volume & Outcome Analytics | `listVolumeOutcome` |
| Approval Processing Time Analytics | `approveProcessingTime` |
| Approval Processing Time Analytics | `listProcessingTime` |
| Bottleneck Analysis & Heatmap | `listBottleneckAnalysiHeatmap` |
| Approval Trend & Comparative Analytics | `approveTrendComparative` |
| Approval Trend & Comparative Analytics | `listTrendComparative` |
| Approver & Team Performance Analytics | `listApproverTeamPerformance` |
| AI Approval Intelligence Center | `approve` |
| AI Approval Intelligence Center | `list` |
| AI Optimization & What-If Simulator | `listWhatSimulator` |
| AI Governance Executive Advisor | `listGovernanceExecutiveAdvisor` |

## Digital Asset Management DAM — board 1

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| Digital Asset Management Command Center | `listDigitalAsset` |
| Central Digital Asset Library | `listCentralDigitalAsset` |
| Upload & Asset Ingestion Workspace | `setUploadAssetIngestion` |
| Folder, Collection & Workspace Management | `listFolderCollection` |
| Folder, Collection & Workspace Management | `setFolderCollection` |
| Metadata & Taxonomy Management | `listMetadataTaxonomy` |
| Tags, Keywords & Classification | `listTagKeywordClassification` |
| Advanced Search & Discovery | `listAdvancedSearchDiscovery` |
| Digital Asset 360° Profile | `listDigitalAssetProfile` |
| Bulk Asset Management Workspace | `listBulkAsset` |
| Bulk Asset Management Workspace | `setBulkAsset` |
| Asset Activity, Recent Assets & Library Health | `listAssetActivityRecent` |

## Digital Asset Management DAM — board 2

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| AI Auto-Tagging & Content Understanding | `listAutoTaggingContent` |
| Semantic & Natural-Language Asset Search | `listSemanticNaturalLanguage` |
| Visual Similarity & Related Asset Discovery | `listVisualSimilarityRelated` |
| Duplicate & Near-Duplicate Management | `listDuplicateNear` |
| Asset Version Control & Revision History | `listAssetVersionRevision` |
| Version Comparison & Replacement Impact | `listVersionComparisonReplacement` |
| Transformation & Rendition Management | `listTransformationRendition` |
| Rendition Processing & Delivery Readiness | `listRenditionProcessingDelivery` |
| AI Quality, Intelligence Review & Recommendations | `listQualityReviewRecommendation` |

## Digital Asset Management DAM — board 3

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| DAM Governance & Rights Command Center | `listDamGovernanceRight` |
| Asset Ownership & Responsibility Management | `listAssetOwnershipResponsibility` |
| Rights, License & Usage Policy Management | `listRightLicenseUsage` |
| Asset Approval Workflow Management | `approveAssetWorkflow` |
| Asset Approval Workflow Management | `listAssetWorkflow` |
| Publication Eligibility & Governance Validation | `publishEligibilityGovernanceValidation` |
| Role-Based Asset Access & Permission Management | `listRoleBasedAsset` |
| Secure Internal & External Sharing | `listSecureInternalExternal` |
| Rights Expiry, Renewal & Usage Impact | `listRightExpiryRenewal` |
| Governance Audit Trail & Compliance Evidence | `listGovernanceTrailCompliance` |
| Governance Risk, Compliance & AI Recommendations | `listGovernanceRiskCompliance` |

## Digital Asset Management DAM — board 4

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Asset Distribution & Delivery Command Center | `listAssetDistributionDelivery` |
| Asset Usage & Distribution Map | `listAssetUsageDistribution` |
| Channel & Distribution Configuration | `setChannelDistribution` |
| Secure Delivery URL, CDN & Rendition Delivery | `listSecureDeliveryUrl` |
| Asset Replacement & Propagation Management | `listAssetReplacementPropagation` |
| Fallback, Expiry & Distribution Continuity | `listFallbackExpiryDistribution` |
| DAM API & Integration Hub | `listDamApiIntegration` |
| Delivery Monitoring & Integration Health | `listDeliveryMonitoringIntegration` |
| Asset Usage & Performance Analytics | `listAssetUsagePerformance` |
| Distribution Intelligence, AI Insights & Optimization | `listDistributionInsight` |

## Event Management Configuration Backend Structure v1.0 — board 1

3 screens · 3 operations to author

| Screen | Operation to author |
|---|---|
| Event Catalogue Command Center | `listEventCatalogue` |
| Event Type & Behaviour Configuration | `setEventTypeBehaviour` |
| Event Duplication & Clone Configuration | `setEventDuplicationClone` |

## Event Management Configuration Backend Structure v1.0 — board 2

3 screens · 3 operations to author

| Screen | Operation to author |
|---|---|
| Event Schedule Command Center | `listEventSchedule` |
| Dynamic Performance Duration Configuration | `setDynamicPerformanceDuration` |
| Schedule Change & Rescheduling Configuration | `setScheduleChangeRescheduling` |

## Event Management Configuration Backend Structure v1.0 — board 3

3 screens · 3 operations to author

| Screen | Operation to author |
|---|---|
| Venue & Space Command Center | `listVenueSpace` |
| Venue Master Configuration | `setVenueMaster` |
| Space Access Rules Configuration | `setSpaceAccessRule` |

## Event Management Configuration Backend Structure v1.0 — board 4

3 screens · 3 operations to author

| Screen | Operation to author |
|---|---|
| Seating & Capacity Command Center | `listSeatingCapacity` |
| Event Capacity Profile Configuration | `setEventCapacityProfile` |
| Seating Mode & Reservation Configuration | `setSeatingModeReservation` |

## Event Management Configuration Backend Structure v1.0 — board 5

4 screens · 4 operations to author

| Screen | Operation to author |
|---|---|
| Registration & Attendance Command Center | `listRegistrationAttendance` |
| Attendee Data & Registration Form Configuration | `setAttendeeDataRegistration` |
| Accreditation & Participant Category Configuration | `setAccreditationParticipantCategory` |
| Event Admission & Entry Policy Configuration | `setEventAdmissionEntry` |

## Event Management Configuration Backend Structure v1.0 — board 6

6 screens · 6 operations to author

| Screen | Operation to author |
|---|---|
| Event Resource Command Center | `listEventResource` |
| Event Resource Requirement Configuration | `setEventResourceRequirement` |
| Staff & Role Assignment Configuration | `setStaffRole` |
| Contractor & External Workforce Configuration | `setContractorExternalWorkforce` |
| Event Shift & Roster Configuration | `setEventShiftRoster` |
| Resource Location & Deployment Configuration | `setResourceLocationDeployment` |

## Event Management Configuration Backend Structure v1.0 — board 7

5 screens · 5 operations to author

| Screen | Operation to author |
|---|---|
| Event Lifecycle & Change Command Center | `listEventLifecycleChange` |
| Lifecycle Transition Configuration | `setLifecycleTransition` |
| Event Change Request Configuration | `setEventChangeRequest` |
| Event Cancellation Workflow Configuration | `setEventCancellationWorkflow` |
| Ticket, Reservation & Customer Treatment Configuration | `setTicketReservationCustomer` |

## Event Management Configuration Backend Structure v1.0 — board 8

4 screens · 4 operations to author

| Screen | Operation to author |
|---|---|
| Activity Session & Slot Template Configuration | `setActivitySessionSlot` |
| Prepaid Minute Package & Customer Balance Configuration | `setPrepaidMinutePackage` |
| Peak, Off-Peak & Super Prime Time Configuration | `setPeakOffSuper` |
| Walk-In / There-and-Then Booking Configuration | `setWalkThereThen` |

## Event Management Configuration Backend Structure v1.0 — board 9

2 screens · 2 operations to author

| Screen | Operation to author |
|---|---|
| Session Operations Command Center | `listSession` |
| Participant Photo & Video Assignment | `setParticipantPhotoVideo` |

## F&B Backend Structure Module Sample Reference v1.0 — board 1

8 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| F&B Command Center | `list` |
| Create / Edit Outlet | `listCreateEditOutlet` |
| Outlet Types & Templates | `listOutletTypeTemplate` |
| Operating Hours & Service Periods | `listOperatingHourService` |
| POS & Device Assignment | `setPosDevice` |
| Service Channel Configuration | `setServiceChannel` |
| Order Routing & KDS/Printer Rules | `listOrderRoutingKds` |
| F&B Global Settings & Controls | `listGlobalSetting` |

## F&B Backend Structure Module Sample Reference v1.0 — board 2

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Restaurant Service Command Center | `listRestaurantService` |
| Floor Plan & Table Map | `listFloorPlanTable` |
| Table & Seating Configuration | `setTableSeating` |
| Reservation Calendar & Timeline | `listReservationCalendarTimeline` |
| Create / Edit Reservation | `listCreateEditReservation` |
| Walk-In & Waitlist Management | `listWalkWaitlist` |
| Guest Profile & Dining History | `listGuestProfileDining` |
| Live Table & Service Management | `listLiveTableService` |
| Table Order, Bill & Payment Management | `listTableOrderBill` |

## Game and Ride Module — board 1

10 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Game & Ride Operations Dashboard | `listGameRide` |
| Game & Ride Directory | `listGameRide` |
| Attraction Profile | `listAttractionProfile` |
| Attraction Type Configuration | `setAttractionType` |
| Game & Ride Operational Configuration | `setGameRideOperational` |
| Wallet & Credit Acceptance Mapping | `listWalletCreditAcceptance` |
| Attraction / Reader Mapping | `listAttractionReaderMapping` |
| Game Package & Entitlement Association | `listGamePackageEntitlement` |
| Configuration Health & Validation | `setHealthValidation` |
| Attraction Audit, Dependencies & Governed Actions | `listAttractionDependencyGoverned` |

## Game and Ride Module — board 10

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Self-Service Experience Command Center | `listSelfServiceExperience` |
| Self-Service Kiosk Profile & Channel Configuration | `setSelfServiceKiosk` |
| Customer Card / Wallet Identification | `listCustomerCardWallet` |
| Customer Wallet & Balance Summary | `listCustomerWalletBalance` |
| Self-Service Wallet Top-Up | `listSelfServiceWallet` |
| Bonus, Free Game & Benefit View | `listBonuFreeGame` |
| Game & Ride Eligibility / “What Can I Play?” | `listGameRideEligibility` |
| Redemption Balance & Prize Discovery | `listRedemptionBalancePrize` |
| Customer Game & Wallet Transaction History | `listCustomerGameWallet` |
| Self-Service UI Theme, Language & Journey Configuration | `setSelfServiceTheme` |

## Game and Ride Module — board 2

9 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| Reader Management Dashboard | `listReader` |
| Reader Directory | `listReader` |
| Reader Credit & Payment Configuration | `setReaderCreditPayment` |
| Reader / Attraction Assignment | `setReaderAttraction` |
| Retap Delay & Transaction Protection | `listRetapDelayTransaction` |
| Free Game Glow & Reader Display Rules | `listFreeGameGlow` |
| Reader Theme & Experience Configuration | `setReaderThemeExperience` |
| Real-Time Tap Validation & Reader Response | `listRealTimeTap` |
| Balance Check Reader & Device Test Console | `listBalanceCheckReader` |

## Game and Ride Module — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Wallet & Credit Management Dashboard | `listWalletCredit` |
| Wallet & Credit Type Configuration | `setWalletCreditType` |
| Wallet Account & Balance View | `listWalletAccountBalance` |
| Top-Up Configuration | `setTop` |
| Top-Up Bonus Rule Configuration | `setTopBonuRule` |
| Bonus Usage Restrictions | `listBonuUsageRestriction` |
| Bonus Validity & Expiry Configuration | `setBonuValidityExpiry` |
| Free Game & Ride Credit Management | `listFreeGameRide` |
| Refund, Adjustment & Manual Bonus Control | `listRefundAdjustmentManual` |
| Wallet Credit Transaction Ledger & Audit | `listWalletCreditTransaction` |

## Game and Ride Module — board 4

10 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Gameplay Validation Command Center | `listGameplayValidation` |
| Gameplay Validation Rule Configuration | `setGameplayValidationRule` |
| Deduction Priority & Funding Source Rules | `listDeductionPriorityFunding` |
| All Games & Rides Pass Configuration | `setAllGameRide` |
| Specific Game/Ride Unlimited Entitlement | `listSpecificGameRide` |
| Specific Game/Ride Limited Entitlement | `listSpecificGameRide` |
| Game Package Builder | `setGamePackage` |
| Entitlement Validity & Activation Rules | `listEntitlementValidityActivation` |
| Real-Time Gameplay Authorization | `listRealTimeGameplay` |
| Validation Simulator & Exception Analysis | `listValidationSimulatorException` |

## Game and Ride Module — board 5

8 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| Game & Ride Pricing Command Center | `listGameRidePricing` |
| Standard Game & Ride Price Configuration | `setStandardGameRide` |
| Group Pricing Configuration | `setGroupPricing` |
| Peak / Non-Peak Dynamic Pricing | `listPeakNonDynamic` |
| Pricing Calendar & Exception Dates | `listPricingCalendarException` |
| Normal & VIP Pricing Configuration | `setNormalVipPricing` |
| Retry Price Configuration | `setRetryPrice` |
| Effective Pricing & Reader Price Preview | `listEffectivePricingReader` |

## Game and Ride Module — board 6

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Redemption Credit Rule Configuration | `setRedemptionCreditRule` |
| Ticket-Based Redemption / Ticket-Eater Integration | `listTicketBasedRedemption` |
| Ticketless Redemption Game Integration | `listTicketlessRedemptionGame` |
| Redemption Wallet & Balance View | `listRedemptionWalletBalance` |
| Redemption Counter / Prize Checkout | `listRedemptionCounterPrize` |
| Prize Catalogue & Credit Cost Configuration | `setPrizeCatalogueCredit` |
| Prize Inventory Integration | `listPrizeInventoryIntegration` |
| Direct-Pay / Crane & Prize Machine Configuration | `setDirectPayCrane` |
| Redemption Transaction Ledger, Reconciliation & Audit | `listRedemptionTransactionLedger` |

## Game and Ride Module — board 7

10 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Card Lifecycle Command Center | `listCardLifecycle` |
| Card / Credential Profile | `listCardCredentialProfile` |
| Card Expiry Rule Configuration | `setCardExpiryRule` |
| Last Recharge & Last Activity Tracking | `listLastRechargeActivity` |
| Expiry Monitoring & Upcoming Expiration | `listExpiryMonitoringUpcoming` |
| Card Expiry Runtime Validation | `listCardExpiryRuntime` |
| Card Block, Suspend & Reactivation Control | `listCardBlockSuspend` |
| Card Replacement & Wallet Relinking | `listCardReplacementWallet` |
| Customer Balance & Credential Status View | `listCustomerBalanceCredential` |
| Card Lifecycle Audit & History | `listCardLifecycle` |

## Game and Ride Module — board 8

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Game & Ride Operations Control Center | `listGameRide` |
| Live Gameplay Transaction Monitor | `listLiveGameplayTransaction` |
| Reader & Device Health Monitor | `listReaderDeviceHealth` |
| Tap Validation & Decision Trace | `listTapValidationDecision` |
| Rejected Transaction & Reason Analysis | `listRejectedTransactionReason` |
| Entitlement & Free-Play Consumption Monitor | `listEntitlementFreePlay` |
| Offline, Synchronization & Recovery Monitor | `listOfflineSynchronizationRecovery` |
| Operational Alerts & Exception Center | `listOperationalAlertException` |
| Operational Analytics & Reconciliation Dashboard | `listOperationalReconciliation` |

## Game and Ride Module — board 9

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Reader Integration Command Center | `listReaderIntegration` |
| Reader Manufacturer & Model Profile | `listReaderManufacturerModel` |
| Communication Protocol Configuration | `setCommunicationProtocol` |
| Reader Command & Event Mapping | `listReaderEventMapping` |
| Reader Configuration Deployment & Synchronization | `setReaderDeploymentSynchronization` |
| Game Trigger & I/O Control Mapping | `listGameTriggerMapping` |
| Reader Screen, LED & Sound Output Mapping | `listReaderLedSound` |
| Edge Cache & Offline Rule Package | `listEdgeCacheOffline` |
| Device Diagnostics & Integration Logs | `listDeviceDiagnosticIntegration` |
| Integration Certification & Test Console | `listIntegrationCertificationTest` |

## Marketing CRM Configuration Reference v1.0 — board 1

9 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| CRM Command Center | `listCrm` |
| Guest Directory | `listGuest` |
| Guest Master Configuration | `setGuestMaster` |
| Activity Timeline | `listActivityTimeline` |
| Contact & Preferences | `listContactPreference` |
| Family & Guardians | `listFamilyGuardian` |
| Corporate & Groups | `listCorporateGroup` |
| Commerce & Documents | `listCommerceDocument` |
| AI Guest Intelligence | `listGuest` |

## Marketing CRM Configuration Reference v1.0 — board 10

10 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Gamification Command Center | `listGamification` |
| Challenge Builder | `setChallenge` |
| Achievement & Badge Engine | `listAchievementBadge` |
| Points & Activity Rules | `listPointActivityRule` |
| Milestones & Reward Rules | `listMilestoneRewardRule` |
| Family, Team & Event Challenges | `listFamilyTeamEvent` |
| Referral & Streak Management | `listReferralStreak` |
| Progress, Leaderboards & Hub | `listProgressLeaderboardHub` |
| AI Engagement Optimization | `listEngagement` |
| Gamification Analytics & Audit | `listGamification` |

## Marketing CRM Configuration Reference v1.0 — board 11

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Digital Experience Center | `listDigitalExperience` |
| Site, Brand & Domain Setup | `setSiteBrandDomain` |
| Design System & Components | `listDesignSystemComponent` |
| Page & Landing Builder | `setPageLanding` |
| Content, Media & Forms | `listContentMediaForm` |
| Dynamic Product Pages | `listDynamicProductPage` |
| Mobile App CMS | `listMobileAppCms` |
| Personalization & Localization | `listPersonalizationLocalization` |
| SEO Management | `listSeo` |
| Publishing, Analytics & Audit | `listPublishing` |

## Marketing CRM Configuration Reference v1.0 — board 12

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Waiver Template Builder | `setWaiverTemplate` |
| Assignment Rules | `setRule` |
| Version, Expiry & Renewal | `listVersionExpiryRenewal` |
| Signature Experience Setup | `setSignatureExperience` |
| Guardian & Group Signing | `listGuardianGroupSigning` |
| Pre-Arrival Completion | `listPreArrivalCompletion` |
| Verification & Access Control | `listVerificationAccess` |
| Documents, Search & Retention | `listDocumentSearchRetention` |
| Legal Evidence & Audit | `listLegalEvidence` |

## Marketing CRM Configuration Reference v1.0 — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Data Governance Center | `listDataGovernance` |
| Identity Resolution Rules | `listIdentityResolutionRule` |
| Duplicate Review & Merge | `listDuplicateReviewMerge` |
| Consent Policy Configuration | `setConsentPolicy` |
| Consent Capture & Versions | `listConsentCaptureVersion` |
| Guest Preference Center | `listGuestPreference` |
| Data Subject Requests | `listDataSubjectRequest` |
| Retention & Anonymization | `listRetentionAnonymization` |
| Privacy & AI Governance | `listPrivacyGovernance` |
| Compliance Audit Dashboard | `listCompliance` |

## Marketing CRM Configuration Reference v1.0 — board 3

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Audience Intelligence | `listAudience` |
| Dynamic Segment Builder | `setDynamicSegment` |
| Static Lists & Imports | `listStaticListImport` |
| Behavioral Segmentation | `listBehavioralSegmentation` |
| Membership & Loyalty Segments | `listMembershipLoyaltySegment` |
| Demographic & Geographic | `listDemographicGeographic` |
| Revenue & Engagement Segments | `listRevenueEngagementSegment` |
| Predictive Audiences | `listPredictiveAudience` |
| Activation & Governance | `listActivationGovernance` |

## Marketing CRM Configuration Reference v1.0 — board 4

7 screens · 7 operations to author

| Screen | Operation to author |
|---|---|
| Campaign Builder | `setCampaign` |
| Audience & Offer Selection | `listAudienceOfferSelection` |
| Multichannel Composer | `listMultichannelComposer` |
| Schedule & Trigger Rules | `listScheduleTriggerRule` |
| Budget, Goals & Forecast | `listBudgetGoalForecast` |
| A/B & AI Optimization | `list` |
| Attribution & Audit | `listAttribution` |

## Marketing CRM Configuration Reference v1.0 — board 5

6 screens · 6 operations to author

| Screen | Operation to author |
|---|---|
| Journey Automation Center | `listJourneyAutomation` |
| Visual Journey Builder | `setVisualJourney` |
| Trigger Event Catalog | `listTriggerEventCatalog` |
| Decision Logic & Timing | `listDecisionLogicTiming` |
| Lifecycle Journeys | `listLifecycleJourney` |
| Cross-Sell & Service Recovery | `listCrossSellService` |

## Marketing CRM Configuration Reference v1.0 — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Communications Center | `listCommunication` |
| Template Library | `listTemplate` |
| Newsletter Builder | `setNewsletter` |
| Content Blocks & Product Feed | `listContentBlockProduct` |
| Subscriptions & Preferences | `listSubscriptionPreference` |
| Transactional Notification Rules | `listTransactionalNotificationRule` |
| Scheduling, Priority & Approval | `approveSchedulingPriority` |
| Delivery, Retry & Failover | `listDeliveryRetryFailover` |
| Deliverability & Analytics | `listDeliverability` |
| AI Content, Translation & Audit | `listContentTranslation` |

## Marketing CRM Configuration Reference v1.0 — board 7

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Omnichannel Command Center | `listOmnichannel` |
| Unified Inbox | `listUnified` |
| Guest Conversation 360 | `listGuestConversation` |
| AI Chatbot Configuration | `setChatbot` |
| Intent & Knowledge Management | `listIntentKnowledge` |
| Agent Workspace | `setAgent` |
| Routing & Queue Management | `listRoutingQueue` |
| Sales & Service Actions | `listSaleServiceAction` |
| Sentiment, Quality & Escalation | `listSentimentQualityEscalation` |
| Chat Analytics & Audit | `listChat` |

## Marketing CRM Configuration Reference v1.0 — board 8

7 screens · 7 operations to author

| Screen | Operation to author |
|---|---|
| Case Queue & Search | `listCaseQueueSearch` |
| Classification & Workflow | `listClassificationWorkflow` |
| Assignment & Workload | `setWorkload` |
| SLA Policy Configuration | `setSlaPolicy` |
| Escalation Rules | `listEscalationRule` |
| Case Workspace | `setCase` |
| Service Recovery | `listServiceRecovery` |

## Marketing CRM Configuration Reference v1.0 — board 9

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Voice of Customer Center | `listVoiceCustomer` |
| Survey Builder | `setSurvey` |
| Survey Triggers & Distribution | `listSurveyTriggerDistribution` |
| NPS, CSAT & CES Configuration | `setNpsCsatCes` |
| Survey Responses & Insights | `listSurveyResponseInsight` |
| Review Collection & Rating Rules | `listReviewCollectionRating` |
| Moderation & Publishing | `listModerationPublishing` |
| AI Sentiment & Topic Analysis | `listSentimentTopicAnalysi` |
| Service Recovery Automation | `listServiceRecoveryAutomation` |
| VOC Analytics & Audit | `listVoc` |

## Order   Reservation Management — board 3

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| External Payment, Partner & Settlement Reference Mapping | `listExternalPaymentPartner` |

## Payment Payment Orchestration — board 1

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Payment Command Center\t7 | `listPayment` |
| Payment Method Catalogue\t8 | `listPaymentMethodCatalogue` |
| Payment Method Configuration\t9 | `setPaymentMethod` |
| Channel & Touchpoint Payment Configuration\t10 | `setChannelTouchpointPayment` |
| Venue, Location & Business Unit Payment Assignment\t11 | `setVenueLocationBusiness` |
| Currency & Payment Currency Configuration\t12 | `setCurrencyPayment` |
| Payment Eligibility & Availability Rule Builder\t13 | `setPaymentEligibilityAvailability` |
| Payment Fees, Surcharges & Commercial Rules\t14 | `listPaymentFeeSurcharge` |
| Payment Policy, Governance & Approval Manager\t15 | `approvePaymentPolicyGovernance` |
| Payment Configuration Simulator & Validation Center\t16 | `listPaymentSimulatorValidation` |
| Payment Configuration Simulator & Validation Center\t16 | `setPaymentSimulatorValidation` |

## Payment Payment Orchestration — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Payment Orchestration Command Center\t27 | `listPaymentOrchestration` |
| Gateway, PSP & Acquirer Directory\t28 | `listGatewayPspAcquirer` |
| Provider Connection & Adapter Configuration\t29 | `setProviderConnectionAdapter` |
| Gateway Capability & Payment Method Mapping\t30 | `listGatewayCapabilityPayment` |
| Payment Routing Rule Builder\t31 | `setPaymentRoutingRule` |
| Routing Strategy, Priority & Load Distribution\t33 | `listRoutingStrategyPriority` |
| Failover, Retry & Resilience Manager\t34 | `listFailoverRetryResilience` |
| Provider Health, SLA & Performance Monitor\t35 | `listProviderHealthSla` |
| Provider Cost, Commercial & Routing Economics\t36 | `listProviderCostCommercial` |
| Payment Routing Simulator, Decision Trace & AI Advisor\t37 | `listPaymentRoutingSimulator` |

## Payment Payment Orchestration — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Terminal & Card-Present Command Center\t48 | `listTerminalCardPresent` |
| Payment Terminal & Device Inventory\t49 | `listPaymentTerminalDevice` |
| Terminal Provisioning & Device Configuration\t51 | `setTerminalProvisioningDevice` |
| POS, Kiosk & Terminal Assignment Manager\t52 | `setPosKioskTerminal` |
| EMV & Card-Present Processing Configuration\t53 | `setEmvCardPresent` |
| Payment Server & Terminal Connectivity Manager\t54 | `listPaymentServerTerminal` |
| Card-Present Transaction Monitor & Operations\t55 | `listCardPresentTransaction` |
| Degraded, Offline & Store-and-Forward Manager\t56 | `listDegradedOfflineStore` |
| Terminal Health, Maintenance & Incident Center\t57 | `listTerminalHealthMaintenance` |
| Terminal Simulator, Certification & AI Operations Advisor\t59 | `listTerminalSimulatorCertification` |

## Payment Payment Orchestration — board 4

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Digital Payments Command Center\t71 | `listDigitalPayment` |
| Digital & Alternative Payment Method Manager\t71 | `listDigitalAlternativePayment` |
| Digital Wallet & Mobile Payment Configuration\t72 | `setDigitalWalletMobile` |
| Payment Link Builder & Configuration\t73 | `setPaymentLink` |
| Payment Link Distribution & Customer Journey Manager\t74 | `listPaymentLinkDistribution` |
| Hosted Checkout, Redirect & Return Flow Configuration\t75 | `setHostedCheckoutRedirect` |
| Digital Payment Session & Transaction Monitor\t76 | `listDigitalPaymentSession` |
| Authentication, Tokenization & Recurring Payment Controls\t78 | `listAuthenticationTokenizationRecurring` |
| Digital Payment Exception, Recovery & Expiry Center\t79 | `listDigitalPaymentException` |
| Digital Payment Simulator, Conversion & AI Advisor\t80 | `listDigitalPaymentSimulator` |

## Payment Payment Orchestration — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Mixed Tender & Credit Command Center\t93 | `listMixedTenderCredit` |
| Mixed Tender Rule & Combination Builder\t93 | `setMixedTenderRule` |
| Split Payment & Tender Allocation Manager\t94 | `listSplitPaymentTender` |
| B2B Credit Account & Limit Manager\t95 | `listCreditAccountLimit` |
| B2B Invoice, On-Account & Payment Terms Configuration\t96 | `setInvoiceAccountPayment` |
| Stored Value, Gift Card & Voucher Tender Controls\t97 | `listStoredValueGift` |
| Advanced Payment Eligibility, Sequence & Restriction Rules\t98 | `listAdvancedPaymentEligibility` |
| Partial Payment, Failure & Recovery Manager\t100 | `listPartialPaymentFailure` |
| Mixed Tender Transaction Trace & Allocation Audit\t100 | `listMixedTenderTransaction` |
| Mixed Tender Simulator, Credit Exposure & AI Advisor\t102 | `listMixedTenderSimulator` |

## Payment Payment Orchestration — board 6

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Refund & Payment Adjustment Command Center\t116 | `listRefundPaymentAdjustment` |
| Refund Request & Eligibility Workspace\t117 | `setRefundRequestEligibility` |
| Refund Allocation & Original Tender Manager\t119 | `listRefundAllocationOriginal` |
| Void, Reversal & Cancellation Manager\t120 | `listVoidReversalCancellation` |
| Refund Approval & Exception Workflow\t121 | `approveRefundExceptionWorkflow` |
| Refund Processing, Provider Status & Recovery Center\t122 | `listRefundProcessingProvider` |
| Payment Adjustment & Financial Correction Manager\t123 | `listPaymentAdjustmentFinancial` |
| Refund Transaction Trace & Audit Investigation\t124 | `listRefundTransactionTrace` |
| Refund Simulator, Risk Analysis & AI Advisor\t126 | `listRefundSimulatorRisk` |

## Payment Payment Orchestration — board 7

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Reconciliation & Settlement Command Center\t139 | `listReconciliationSettlement` |
| Reconciliation Source & Import Manager\t141 | `listReconciliationSourceImport` |
| Transaction Matching & Reconciliation Engine\t142 | `listTransactionMatchingReconciliation` |
| Reconciliation Exception & Investigation Center\t143 | `listReconciliationExceptionInvestigation` |
| Settlement & Payout Manager\t144 | `listSettlementPayoutManager` |
| Fees, Commission, FX & Settlement Economics\t145 | `listFeeCommissionSettlement` |
| Merchant Account & Settlement Calendar Manager\t146 | `listMerchantAccountSettlement` |
| Settlement Posting, Finance Handoff & Close Manager\t148 | `listSettlementPostingFinance` |
| Reconciliation Audit, Trace & Evidence Center\t149 | `listReconciliationTraceEvidence` |
| Reconciliation Simulator, Forecast & AI Operations Advisor\t150 | `listReconciliationSimulatorForecast` |

## Payment Payment Orchestration — board 8

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Payment Risk & Fraud Command Center\t166 | `listPaymentRiskFraud` |
| Payment Risk Rule & Decision Engine\t167 | `listPaymentRiskRule` |
| Velocity, Behavioral & Transaction Risk Controls\t168 | `listVelocityBehavioralTransaction` |
| Risk Lists, Signals & Payment Control Center\t169 | `listRiskListSignal` |
| Fraud Alert, Investigation & Case Management\t170 | `listFraudAlertInvestigation` |
| Chargeback & Dispute Command Center\t172 | `listChargebackDispute` |
| Chargeback Evidence & Representment Workspace\t173 | `setChargebackEvidenceRepresentment` |
| Payment Performance & Conversion Analytics\t174 | `listPaymentPerformanceConversion` |
| AI Fraud, Anomaly & Payment Intelligence Center\t175 | `listFraudAnomalyPayment` |
| Payment Executive Intelligence, Risk Simulator & AI Advisor\t176 | `listPaymentExecutiveRisk` |

## Pricing   Revenue Management — board 2

3 screens · 3 operations to author

| Screen | Operation to author |
|---|---|
| Effective Date, Season & Day-Based Pricing Rules | `listEffectiveDateSeason` |
| Timeslot, Performance & Time-of-Day Pricing Rules | `listTimeslotPerformanceTime` |
| Pricing Rule Priority, Conflict Resolution & Testing | `listPricingRulePriority` |

## Pricing   Revenue Management — board 3

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| Fee Waiver, Tax Exemption & Exception Rules | `listFeeWaiverTax` |

## Pricing   Revenue Management — board 4

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| Bulk Pricing Update, Import & Mass Maintenance | `listBulkPricingUpdate` |

## Pricing   Revenue Management — board 5

4 screens · 4 operations to author

| Screen | Operation to author |
|---|---|
| Seasonal, Calendar, Day & Timeslot Dynamic Rules | `listSeasonalCalendarDay` |
| Channel, Customer Segment & Location Dynamic Rules | `listChannelCustomerSegment` |
| Dynamic Price Bands, Ladders & Adjustment Matrix | `listDynamicPriceBand` |
| Rule Priority, Conflict Resolution & Dynamic Pricing Test Console | `listRulePriorityConflict` |

## Pricing   Revenue Management — board 6

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| Market, Tourism, Holiday & Contextual Signal Hub | `listMarketTourismHoliday` |

## Promotions   Bundles Management — board 2

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| Payment Method, Bank & Partner Discount Rules | `listPaymentMethodBank` |

## Promotions   Bundles Management — board 4

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| Gift, Free Product & Added-Value Offer Builder | `setGiftFreeProduct` |

## Promotions   Bundles Management — board 5

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| Guest Choice & Build-Your-Own Bundle Designer | `setGuestChoiceBuild` |

## Rental Management — board 1

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Rental Product Command Center | `listRentalProduct` |
| Create Rental Product Wizard | `listCreateRentalProduct` |
| Rental Product Profile | `listRentalProductProfile` |
| Rental Category & Classification Setup | `setRentalCategoryClassification` |
| Inventory Tracking Model | `listInventoryTrackingModel` |
| Rental Location Assignment | `setRentalLocation` |
| Rental Duration & Turnaround Configuration | `setRentalDurationTurnaround` |
| Rental Rules & Operational Policy | `listRentalRuleOperational` |
| Customer Requirements, Agreement & Waiver | `listCustomerRequirementAgreement` |

## Rental Management — board 10

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Rental Executive Command Center | `listRentalExecutive` |
| Rental Revenue & Commercial Analytics | `listRentalRevenueCommercial` |
| Utilization & Capacity Analytics | `listUtilizationCapacity` |
| Inventory & Equipment Performance Analytics | `listInventoryEquipmentPerformance` |
| Rental Duration, Extension & Return Analytics | `listRentalDurationExtension` |
| Damage, Loss, Deposit & Exception Analytics | `listDamageLossDeposit` |
| Location & Channel Performance | `listLocationChannelPerformance` |
| Rental Forecasting & Demand Intelligence | `listRentalDemand` |
| Audit, Governance & Operational Control | `listGovernanceOperational` |
| AI Rental Management Copilot & Action Center | `listRentalCopilotAction` |

## Rental Management — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Rental Inventory Command Center | `listRentalInventory` |
| Serialized Equipment Registry | `listSerializedEquipment` |
| Equipment / Asset Profile | `listEquipmentAssetProfile` |
| Pooled Inventory Management | `listPooledInventory` |
| Equipment Status & Condition Management | `listEquipmentStatuCondition` |
| QR / Barcode Equipment Identification | `listBarcodeEquipmentIdentification` |
| Inventory Location Allocation | `listInventoryLocationAllocation` |
| Inventory Transfer Management | `listInventoryTransfer` |
| Inventory Adjustment & Exception Management | `listInventoryAdjustmentException` |
| Inventory Intelligence & Rebalancing | `listInventoryRebalancing` |

## Rental Management — board 3

9 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| Availability Command Center | `listAvailability` |
| Availability Rule Configuration | `setAvailabilityRule` |
| Operating Hours & Rental Windows | `listOperatingHourRental` |
| Timeslot & Duration Availability Setup | `setTimeslotDurationAvailability` |
| Resource / Equipment Calendar | `listResourceEquipmentCalendar` |
| Blackout, Closure & Capacity Blocking | `listBlackoutClosureCapacity` |
| Overlap & Conflict Engine | `listOverlapConflict` |
| Inventory Holds, Buffers & Release Rules | `listInventoryHoldBuffer` |
| Availability Intelligence & AI Forecasting | `listAvailability` |

## Rental Management — board 4

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Rental Pricing Command Center | `listRentalPricing` |
| Pricing Profile Builder | `setPricingProfile` |
| Duration & Tiered Pricing Configuration | `setDurationTieredPricing` |
| Calendar, Peak & Seasonal Pricing | `listCalendarPeakSeasonal` |
| Dynamic Pricing & AI Recommendation | `listDynamicPricingRecommendation` |
| Deposit & Security Hold Policy | `listDepositSecurityHold` |
| Deposit Lifecycle & Settlement Rules | `listDepositLifecycleSettlement` |
| Late Fee, Grace Period & Extension Pricing | `listLateFeeGrace` |
| Commercial Exceptions, Waivers & Overrides | `listCommercialExceptionWaiver` |

## Rental Management — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Rental Booking Command Center | `listRentalBooking` |
| New Rental Booking Wizard | `listNewRentalBooking` |
| Availability Selection & Alternative Options | `listAvailabilitySelectionAlternative` |
| Customer & Participant Information | `listCustomerParticipantInformation` |
| Group Rental & Participant Management | `listGroupRentalParticipant` |
| Rental Agreement & Waiver Completion | `listRentalAgreementWaiver` |
| Booking Commercial Summary & Payment | `listBookingCommercialSummary` |
| Reservation Confirmation & QR Voucher | `listReservationConfirmationVoucher` |
| Reservation Modification, Cancellation & No-Show | `listReservationModificationCancellation` |
| Reservation Detail, Timeline & Readiness | `listReservationDetailTimeline` |

## Rental Management — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Rental Checkout Command Center | `listRentalCheckout` |
| Voucher Scan & Reservation Retrieval | `listVoucherScanReservation` |
| Checkout Readiness Validation | `listCheckoutReadinessValidation` |
| Equipment Assignment Workspace | `setEquipment` |
| Equipment Scan & Validation | `listEquipmentScanValidation` |
| Pre-Rental Condition Inspection | `listPreRentalCondition` |
| Safety & Handover Checklist | `listSafetyHandoverChecklist` |
| Deposit & Financial Handover Validation | `listDepositFinancialHandover` |
| Group & Multi-Item Checkout | `listGroupMultiItem` |
| Checkout Confirmation & Rental Activation | `listCheckoutConfirmationRental` |

## Rental Management — board 7

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Active Rental Operations Command Center | `listActiveRental` |
| Active Rental Detail & Live Timeline | `listActiveRentalDetail` |
| Rental Extension Request | `listRentalExtensionRequest` |
| Extension Pricing & Confirmation | `listExtensionPricingConfirmation` |
| Equipment Swap / Replacement | `listEquipmentSwapReplacement` |
| Rental Incident & Operational Exception | `listRentalIncidentOperational` |
| Due Soon & Customer Notification Management | `listDueSoonCustomer` |
| Overdue Rental Management | `listOverdueRental` |
| Active Group Rental Management | `listActiveGroupRental` |
| Active Rental Intelligence & Operational Alerts | `listActiveRentalOperational` |

## Rental Management — board 8

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Rental Return Command Center | `listRentalReturn` |
| Return Scan & Rental Retrieval | `listReturnScanRental` |
| Return Summary & Actual Return Time | `listReturnSummaryActual` |
| Post-Rental Condition Inspection | `listPostRentalCondition` |
| Before vs After Condition Comparison | `listBeforeAfterCondition` |
| Damage Assessment & Charge Workflow | `listDamageAssessmentCharge` |
| Partial Return & Missing Equipment | `listPartialReturnMissing` |
| Late Fees, Damage Fees & Final Settlement | `listLateFeeDamage` |
| Deposit Release, Capture & Customer Confirmation | `listDepositReleaseCapture` |
| Return Completion & Equipment Disposition | `listReturnCompletionEquipment` |

## Rental Management — board 9

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Maintenance Command Center | `listMaintenance` |
| Maintenance Rule & Service Plan Configuration | `setMaintenanceRuleService` |
| Maintenance Calendar & Scheduling | `listMaintenanceCalendarScheduling` |
| Technician Repair Workspace | `setTechnicianRepair` |
| Parts, Cost & Maintenance Expense Tracking | `listPartCostMaintenance` |
| Asset Maintenance History & Lifecycle | `listAssetMaintenanceLifecycle` |
| Return-to-Service Inspection & Approval | `approveReturnServiceInspection` |
| Asset Retirement, Write-Off & Replacement Recommendation | `listAssetRetirementWrite` |
| Maintenance Intelligence & Predictive AI | `listMaintenancePredictive` |

## Resource Management Configuration — board 1

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Resource Type Configuration | `setResourceType` |
| Resource Category Management | `listResourceCategory` |
| Resource Creation & Profile | `createResourceProfile` |
| Configurable Attribute Builder | `setConfigurableAttribute` |
| Resource Hierarchy & Parent–Child Relationships | `listResourceHierarchyParent` |
| Resource Dependency Rules | `listResourceDependencyRule` |
| Resource Package & Bundle Configuration | `setResourcePackageBundle` |
| Multi-Venue Resource Assignment | `setMultiVenueResource` |
| Resource Lifecycle, Governance & Audit | `listResourceLifecycleGovernance` |

## Resource Management Configuration — board 10

8 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| Resource Utilization & Capacity Analytics | `listResourceUtilizationCapacity` |
| Resource Cost, Revenue & Efficiency Analytics | `listResourceCostRevenue` |
| Demand Forecast Accuracy & Planning Performance | `listDemandForecastAccuracy` |
| Resource KPI, SLA & Performance Framework | `listResourceKpiSla` |
| Resource Governance & Policy Center | `listResourceGovernancePolicy` |
| Audit Trail & Resource Decision History | `listTrailResourceDecision` |
| Resource Integration & System Health Center | `listResourceIntegrationSystem` |
| Executive Resource Intelligence & AI Improvement Center | `listExecutiveResourceImprovement` |

## Resource Management Configuration — board 2

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Resource Calendar Command Center | `listResourceCalendar` |
| Calendar Filters, Search & Smart Discovery | `listCalendarFilterSearch` |
| Resource Availability Schedule Configuration | `setResourceAvailabilitySchedule` |
| Resource Time-Slot Configuration | `setResourceTimeSlot` |
| Advance Reservation Management | `listAdvanceReservation` |
| Recurring Reservation Configuration | `setRecurringReservation` |
| Operational Time & Resource Blocking | `listOperationalTimeResource` |
| Multi-Event Resource Planning | `listMultiEventResource` |
| Smart Assignment & Drag-and-Drop Reallocation | `setSmartDragDrop` |

## Resource Management Configuration — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Staff Resource Directory | `listStaffResource` |
| Staff Resource Profile | `listStaffResourceProfile` |
| Skills & Competency Management | `listSkillCompetency` |
| Certification & Expiry Management | `listCertificationExpiry` |
| Qualification & Assignment Rule Engine | `setQualificationRule` |
| Staff Availability & Working Pattern | `listStaffAvailabilityWorking` |
| Shift Template & Assignment Configuration | `setShiftTemplate` |
| Break, Leave & Absence Configuration | `setBreakLeaveAbsence` |
| Overtime & Working-Hour Rules | `listOvertimeWorkingHour` |
| Workforce Integration & Synchronization Center | `listWorkforceIntegrationSynchronization` |

## Resource Management Configuration — board 4

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Workforce Roster Command Center | `listWorkforceRoster` |
| Attraction & Operational Staffing Roster | `listAttractionOperationalStaffing` |
| Minimum Staffing & Coverage Rule Configuration | `setMinimumStaffingCoverage` |
| Staffing Gap & Coverage Control Center | `listStaffingGapCoverage` |
| Shift Marketplace & Workforce Requests | `listShiftMarketplaceWorkforce` |
| Attendance & Live Workforce Command Center | `listAttendanceLiveWorkforce` |
| Staff Check-In, Check-Out & Attendance Exceptions | `listStaffCheckOut` |
| Workforce Compliance Validation Center | `listWorkforceComplianceValidation` |
| Labor Cost & Staffing Budget Control | `listLaborCostStaffing` |
| AI Workforce Planner & Roster Optimization | `listWorkforcePlannerRoster` |

## Resource Management Configuration — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Experience Resource Requirement Builder | `setExperienceResourceRequirement` |
| Staff-to-Experience Qualification Mapping | `listStaffExperienceQualification` |
| Resource Combination Builder | `setResourceCombination` |
| Ticket Demand & Resource Capacity Mapping | `listTicketDemandResource` |
| Customer Resource Selection Configuration | `setCustomerResourceSelection` |
| Skill-Based & Smart Resource Selection | `listSkillBasedSmart` |
| Customer / Cashier Resource Assignment Experience | `setCustomerCashierResource` |
| Dynamic Resource Allocation Engine | `listDynamicResourceAllocation` |
| Priority, Scoring & Allocation Policy | `listPriorityScoringAllocation` |
| Automatic Replacement & Assignment Recovery | `setAutomaticReplacementRecovery` |

## Resource Management Configuration — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Equipment & Asset Command Center | `listEquipmentAsset` |
| Rental Resource Configuration | `setRentalResource` |
| Rental Inventory & Availability Control | `listRentalInventoryAvailability` |
| Resource Checkout Workspace | `setResourceCheckout` |
| Guest & Resource Assignment | `setGuestResource` |
| Rental Duration, Extension & Return Management | `listRentalDurationExtension` |
| Deposit & Rental Financial Control | `listDepositRentalFinancial` |
| Maintenance & Resource Blocking | `listMaintenanceResourceBlocking` |
| Inspection, Condition & Compliance Management | `listInspectionConditionCompliance` |
| Asset Lifecycle, Depreciation & Retirement | `listAssetLifecycleDepreciation` |

## Resource Management Configuration — board 7

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Event Resource Planning Command Center | `listEventResourcePlanning` |
| Event Resource Requirement Builder | `setEventResourceRequirement` |
| Venue & Space Allocation | `listVenueSpaceAllocation` |
| Equipment & Asset Allocation | `listEquipmentAssetAllocation` |
| Event Staff & Personnel Allocation | `listEventStaffPersonnel` |
| Event Resource Template Library | `listEventResourceTemplate` |
| AI Event Resource Forecasting | `listEventResource` |
| Event Resource Cost Estimator | `listEventResourceCost` |
| Multi-Event Allocation & Conflict Optimizer | `listMultiEventAllocation` |
| Event Resource Approval & Readiness Gate | `approveEventResourceReadiness` |

## Resource Management Configuration — board 8

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Optimal Resource Recommendation Engine | `listOptimalResourceRecommendation` |
| AI Staff Recommendation & Workforce Matching | `listStaffRecommendationWorkforce` |
| Resource Demand Forecasting | `listResourceDemand` |
| AI Staffing Requirement Forecast | `listStaffingRequirementForecast` |
| AI Conflict Resolution Assistant | `listConflictResolutionAssistant` |
| Automatic Schedule Optimization | `listAutomaticSchedule` |
| Alternative & Replacement Resource | `listAlternativeReplacementResource` |
| Operational Scenario Simulator & Digital Twin | `listOperationalScenarioSimulator` |
| Conversational AI Resource Copilot | `listConversationalResourceCopilot` |

## Resource Management Configuration — board 9

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| My Resource Operations Home | `listResourceHome` |
| My Schedule & Assignment Calendar | `setScheduleCalendar` |
| Assignment Detail & Operational Brief | `setDetailOperationalBrief` |
| Mobile Staff Check-In & Check-Out | `listMobileStaffCheck` |
| Resource Collection, Handover & Return | `listResourceCollectionHandover` |
| Employee Requests & Resource Support | `listEmployeeRequestResource` |
| Shift Change, Swap, Pickup & Release | `listShiftChangeSwap` |
| Manager Mobile Approval Center | `approveManagerMobile` |
| Manager Mobile Approval Center | `listManagerMobile` |
| Operational Notifications & Live Alerts | `listOperationalNotificationLive` |
| Mobile Operations Control & Offline Sync | `listMobileOfflineSync` |

## Seat Management Venue Mapping Reference v1.0 — board 1

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Venue Canvas | `listVenueCanva` |
| Sections & Zones | `listSectionZone` |
| Rows & Seats | `listRowSeat` |
| Standing Zones | `listStandingZone` |
| Suites & Boxes | `listSuiteBoxe` |
| Stage & Focal Point | `listStageFocalPoint` |
| Entrances, Exits & Aisles | `listEntranceExitAisle` |
| Amenities & Obstructions | `listAmenityObstruction` |
| Templates, Validation & Publish | `listTemplateValidationPublish` |

## Seat Management Venue Mapping Reference v1.0 — board 10

7 screens · 7 operations to author

| Screen | Operation to author |
|---|---|
| Dynamic Seat Pricing | `listDynamicSeatPricing` |
| Price Bands & Categories | `listPriceBandCategory` |
| Demand Forecasting | `listDemand` |
| Inventory Forecasting | `listInventory` |
| Section Revenue Forecast | `listSectionRevenueForecast` |
| Seat Upsell Recommendations | `listSeatUpsellRecommendation` |
| Scenario & What-If Planning | `listScenarioWhatPlanning` |

## Seat Management Venue Mapping Reference v1.0 — board 11

8 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| Occupancy Reporting | `listOccupancyReporting` |
| Zone Performance Reporting | `listZonePerformanceReporting` |
| Revenue by Section | `listRevenueSection` |
| Seat Utilization Analytics | `listSeatUtilization` |
| Sales Pace & Pick Curves | `listSalePacePick` |
| Heat Maps & Drill-Down | `listHeatMapDrill` |
| Report Builder, Export & Audit | `listReportExport` |
| Report Builder, Export & Audit | `setReportExport` |

## Seat Management Venue Mapping Reference v1.0 — board 12

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Platform Command Center | `listPlatform` |
| Tenant & Brand Context | `listTenantBrandContext` |
| Venue-Specific Configuration | `setVenueSpecific` |
| Naming, Numbering & Localization | `listNamingNumberingLocalization` |
| Currency, Timezone & Channels | `listCurrencyTimezoneChannel` |
| Roles, Permissions & Masking | `listRolePermissionMasking` |
| Seat Approval Workflows | `approveSeatWorkflow` |
| Lifecycle & Environment Promotion | `listLifecycleEnvironmentPromotion` |
| Platform Health & Observability | `listPlatformHealthObservability` |
| Setup, Clone & Inheritance | `setCloneInheritance` |

## Seat Management Venue Mapping Reference v1.0 — board 13

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Integration Command Center | `listIntegration` |
| Seat Management APIs | `listSeatApi` |
| API Access & OAuth | `listApiAccessOauth` |
| Webhook Configuration | `setWebhook` |
| Seat Event Catalog | `listSeatEventCatalog` |
| Concurrency, Idempotency & Limits | `listConcurrencyIdempotencyLimit` |
| Mapping & Transformation | `listMappingTransformation` |
| Monitoring, Retry & Reconciliation | `listMonitoringRetryReconciliation` |
| Immutable Seat Audit Logs | `listImmutableSeatLog` |
| Integration Approval & Compliance | `approveIntegrationCompliance` |

## Seat Management Venue Mapping Reference v1.0 — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Import Command Center | `listImport` |
| PDF & Image Import | `listPdfImageImport` |
| SVG & CAD Import | `listSvgCadImport` |
| CSV & Excel Import | `listCsvExcelImport` |
| AI Section Recognition | `listSectionRecognition` |
| AI Row & Seat Recognition | `listRowSeatRecognition` |
| AI Aisle, VIP & Accessibility | `listAisleVipAccessibility` |
| AI Numbering & Labeling | `listNumberingLabeling` |
| Validation & Correction | `listValidationCorrection` |
| AI Venue Designer & Publish | `setVenuePublish` |

## Seat Management Venue Mapping Reference v1.0 — board 3

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Layout Command Center | `listLayout` |
| Template Library | `listTemplate` |
| Event-Specific Layout | `listEventSpecificLayout` |
| Clone & Inheritance | `listCloneInheritance` |
| Version Compare | `listVersionCompare` |
| Multi-Performance Assignment | `setMultiPerformance` |
| Temporary Seat Blocking | `listTemporarySeatBlocking` |
| Scheduled Seat Release | `listScheduledSeatRelease` |
| Approval, Publish & Rollback | `approvePublishRollback` |

## Seat Management Venue Mapping Reference v1.0 — board 4

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Inventory Command Center | `listInventory` |
| Real-Time Seat Map | `listRealTimeSeat` |
| Status Model Configuration | `setStatuModel` |
| Availability Tracker | `listAvailabilityTracker` |
| Hold Tracker | `listHoldTracker` |
| Reservation Tracker | `listReservationTracker` |
| Sales & Allocation Tracker | `listSaleAllocationTracker` |
| Maintenance & Out of Service | `listMaintenanceOutService` |
| Audit & Reconciliation | `listReconciliation` |

## Seat Management Venue Mapping Reference v1.0 — board 5

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Experience Command Center | `listExperience` |
| Choose My Seats | `listChooseSeat` |
| Find Seats For Me | `listFindSeat` |
| Filters & Interactive Legend | `listFilterInteractiveLegend` |
| Lock Timeout & Concurrency | `listLockTimeoutConcurrency` |
| Cart & Multi-Seat Management | `listCartMultiSeat` |
| Mobile & Accessible Selection | `listMobileAccessibleSelection` |
| View Preview, Compare & Heat Map | `listViewPreviewCompare` |
| AI Conversational Seat Assistant | `listConversationalSeatAssistant` |

## Seat Management Venue Mapping Reference v1.0 — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Hold Command Center | `listHold` |
| Hold Type Master | `listHoldTypeMaster` |
| Hold Pool Creation | `createHoldPool` |
| Hold Rule Assignment | `setHoldRule` |
| Expiration Rules | `listExpirationRule` |
| Automatic Hold Release | `listAutomaticHoldRelease` |
| Release, Convert & Reassign | `listReleaseConvertReassign` |
| Hold Approval Workflow | `approveHoldWorkflow` |
| Priority & Conflict Resolution | `listPriorityConflictResolution` |
| Hold Utilization & Audit | `listHoldUtilization` |

## Seat Management Venue Mapping Reference v1.0 — board 7

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Rules Command Center | `listRule` |
| Seat Kill Rules | `listSeatKillRule` |
| Buffer Seat Rules | `listBufferSeatRule` |
| Companion Seat Rules | `listCompanionSeatRule` |
| Wheelchair Companion Rules | `listWheelchairCompanionRule` |
| Accessible Seating Master | `listAccessibleSeatingMaster` |
| Accessible Route Mapping | `listAccessibleRouteMapping` |
| Accessible Filters & Eligibility | `listAccessibleFilterEligibility` |
| Flexible Spacing Rules | `listFlexibleSpacingRule` |
| Compliance Validation & Audit | `listComplianceValidation` |

## Seat Management Venue Mapping Reference v1.0 — board 8

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Group Reservation Center | `listGroupReservation` |
| Group Type Configuration | `setGroupType` |
| Group Request Intake | `listGroupRequestIntake` |
| Availability & Best-Fit Search | `listAvailabilityBestFit` |
| Bulk Seat Allocation | `listBulkSeatAllocation` |
| Roster & Participant Assignment | `setRosterParticipant` |
| Quote, Deposit & Payment | `listQuoteDepositPayment` |
| Modify, Release & Cancel | `listModifyReleaseCancel` |
| Contracts & Approval Workflow | `approveContractWorkflow` |
| Group Reporting & Audit | `listGroupReporting` |

## Seat Management Venue Mapping Reference v1.0 — board 9

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Recommendation Command Center | `listRecommendation` |
| Best Seat Recommendations | `listBestSeatRecommendation` |
| Best Value Recommendations | `listBestValueRecommendation` |
| Closest-to-Stage Recommendations | `listClosestStageRecommendation` |
| Family Seating Recommendations | `listFamilySeatingRecommendation` |
| Accessibility Recommendations | `listAccessibilityRecommendation` |
| Seat Upgrade Recommendations | `listSeatUpgradeRecommendation` |
| Alternatives & Reseating | `listAlternativeReseating` |
| Scoring Rules & Model Governance | `listScoringRuleModel` |
| Performance, Feedback & Audit | `listPerformanceFeedback` |

## Subscription Licensing AI Self Service — board 1

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Commercial Command Center | `listCommercial` |
| Customer Subscription & Commercial Portfolio | `listCustomerSubscriptionCommercial` |
| Customer Commercial 360° | `listCustomerCommercial` |
| Operational Profile, VSI & Commercial Model Intelligence | `listOperationalProfileVsi` |
| Revenue & Commercial Model Analytics | `listRevenueCommercialModel` |
| Trial & Conversion Monitor | `listTrialConversion` |
| Commercial Optimization & Expansion Opportunities | `listCommercialExpansionOpportunity` |
| Subscription Exceptions & Commercial Alerts | `listSubscriptionExceptionCommercial` |
| Executive AI Commercial Intelligence | `listExecutiveCommercial` |

## Subscription Licensing AI Self Service — board 10

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Billing & Commercial Command Center | `listBillingCommercial` |
| Billing Calculation & Charge Breakdown | `listBillingCalculationCharge` |
| Consumption Reconciliation & Billing Approval | `approveConsumptionReconciliationBilling` |
| Invoice & Payment Management | `listInvoicePayment` |
| Subscription & Commercial Change Management | `listSubscriptionCommercialChange` |
| Renewal Management Center | `listRenewal` |
| AI Upgrade, Downgrade & Commercial Right-Sizing | `listUpgradeDowngradeCommercial` |
| Commercial Scenario Simulator | `listCommercialScenarioSimulator` |
| Discount, Credit & Commercial Override Management | `listDiscountCreditCommercial` |
| Renewal Approval, Activation & Commercial Handoff | `approveRenewalActivationCommercial` |

## Subscription Licensing AI Self Service — board 2

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Welcome & Start Your TICVAI Journey | `listWelcomeStartYour` |
| Customer & Organization Registration | `listCustomerOrganizationRegistration` |
| Venue Type & Business Profile | `listVenueTypeBusiness` |
| Visitor, Capacity & Operational Scale | `listVisitorCapacityOperational` |
| Ticketing & Product Requirements | `listTicketingProductRequirement` |
| Access, Queue & Visitor Experience Assessment | `listAccessQueueVisitor` |
| Additional Business Module Assessment | `listAdditionalBusinessModule` |
| Integration, Payment & Technical Readiness | `listIntegrationPaymentTechnical` |
| AI Assessment Summary & Handoff | `listAssessmentSummaryHandoff` |

## Subscription Licensing AI Self Service — board 3

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Commercial Rules Engine Overview | `listCommercialRule` |
| VSI Model Builder | `setVsiModel` |
| VSI Scoring & Tier Threshold Configuration | `setVsiScoringTier` |
| Subscription Tier Configuration | `setSubscriptionTier` |
| Tier Included Allowances | `listTierIncludedAllowance` |
| Commercial & Licensing Model Configuration | `setCommercialLicensingModel` |
| Billable Unit, Minimum Guarantee & Enforcement Rules | `listBillableUnitMinimum` |
| Overage Pricing & Capacity Packs | `listOveragePricingCapacity` |
| Commercial Model & Rule Simulation | `simulateCommercialModelRule` |
| Rule Versioning, Approval & Publication | `approveRuleVersioning` |
| Rule Versioning, Approval & Publication | `publishRuleVersioning` |

## Subscription Licensing AI Self Service — board 4

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Recommended Package Overview | `listRecommendedPackage` |
| Commercial Model & Tier Selection | `listCommercialModelTier` |
| Module Marketplace | `listModuleMarketplace` |
| AI Module & Package Recommendations | `listModulePackageRecommendation` |
| Module Detail & Commercial Treatment | `listModuleDetailCommercial` |
| Module Dependency & Compatibility Manager | `listModuleDependencyCompatibility` |
| Add-Ons, Capacity & Commercial Options | `listAddOnsCapacity` |
| Commercial Package Simulator | `listCommercialPackageSimulator` |
| Package Review & Commercial Summary | `listPackageReviewCommercial` |
| Final Package Approval & Handoff | `approveFinalPackageHandoff` |

## Subscription Licensing AI Self Service — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Purchase / Trial Journey Selection | `listPurchaseTrialJourney` |
| Contract & Billing Cycle Selection | `listContractBillingCycle` |
| Billing & Legal Entity Information | `listBillingLegalEntity` |
| Payment Method & Settlement Setup | `setPaymentMethodSettlement` |
| Trial Configuration & Conversion Rules | `setTrialConversionRule` |
| Order & Commercial Pricing Review | `listOrderCommercialPricing` |
| Commercial Agreement, Billable Definition & Customer Acceptance | `listCommercialAgreementBillable` |
| Payment, Contract & Commercial Validation | `listPaymentContractCommercial` |
| Subscription Confirmation & Commercial Activation | `listSubscriptionConfirmationCommercial` |
| Subscription Lifecycle & Trial-to-Paid Handoff | `listSubscriptionLifecycleTrial` |

## Subscription Licensing AI Self Service — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Provisioning Command Center | `listProvisioning` |
| Tenant & Organization Provisioning | `listTenantOrganizationProvisioning` |
| Venue & Operational Structure Creation | `createVenueOperationalStructure` |
| Administrator & Security Initialization | `listAdministratorSecurityInitialization` |
| License & Entitlement Activation | `listLicenseEntitlementActivation` |
| Module Activation & Dependency Validation | `listModuleActivationDependency` |
| Venue Template Application | `listVenueTemplateApplication` |
| Initial Configuration & Regional Defaults | `setInitialRegionalDefault` |
| Provisioning Validation & Exception Management | `listProvisioningValidationException` |
| Environment Ready & Handoff to AI Setup | `setEnvironmentReadyHandoff` |

## Subscription Licensing AI Self Service — board 7

12 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| AI Setup Command Center | `list` |
| AI Setup Command Center | `set` |
| Guided Setup Plan | `setGuidedPlan` |
| AI Configuration Workspace | `set` |
| AI Draft Review & Approval | `approveDraftReview` |
| Manual Configuration Center | `listManual` |
| Manual Configuration Center | `setManual` |
| Venue, Calendar & Operational Setup | `setVenueCalendarOperational` |
| Product, Pricing & Sales Channel Setup | `setProductPricingSale` |
| POS, Payment & Access Setup | `setPosPaymentAccess` |
| Configuration Health & AI Review | `setHealthReview` |
| Setup Completion & Handoff to Go-Live | `setCompletionHandoffLive` |

## Subscription Licensing AI Self Service — board 8

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Go-Live Readiness Command Center | `listLiveReadiness` |
| Automated Validation Plan | `listAutomatedValidationPlan` |
| Ticketing & Product Validation | `listTicketingProductValidation` |
| End-to-End Sales Channel Testing | `listEndSaleChannel` |
| Payment & Financial Validation | `listPaymentFinancialValidation` |
| Ticket, QR & Access Validation | `listTicketAccessValidation` |
| User, Security & Integration Validation | `listUserSecurityIntegration` |
| Communication & Customer Journey Validation | `listCommunicationCustomerJourney` |
| Blocker, Warning & AI Resolution Center | `listBlockerWarningResolution` |
| Final Go-Live Approval & Production Launch | `approveFinalLiveProduction` |

## Subscription Licensing AI Self Service — board 9

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Usage & License Command Center | `listUsageLicense` |
| Entitlement & License Inventory | `listEntitlementLicenseInventory` |
| Commercial Consumption & Billable Event Metering | `listCommercialConsumptionBillable` |
| Operational Usage & Threshold Monitor | `listOperationalUsageThreshold` |
| License Enforcement & Decision Engine | `listLicenseEnforcementDecision` |
| Minimum Guarantee & Variable Consumption Monitor | `listMinimumGuaranteeVariable` |
| Overage, Capacity & Temporary Exception Management | `listOverageCapacityTemporary` |
| Usage Alerts, Reconciliation & Exception Center | `listUsageAlertReconciliation` |
| AI Usage Forecast & Commercial Optimization | `listUsageForecastCommercial` |
| License, Metering & Commercial Synchronization Audit | `listLicenseMeteringCommercial` |

## TICVAI Finance Backend Structure Reference v1.0 — board 1

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| Finance Dashboard | `listFinance` |

## TICVAI Finance Backend Structure Reference v1.0 — board 2

1 screens · 1 operations to author

| Screen | Operation to author |
|---|---|
| Admissions Revenue | `listAdmissionRevenue` |

## Ticket Resale Marketplace — board 3

4 screens · 4 operations to author

| Screen | Operation to author |
|---|---|
| Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience | `listResaleTicketDetail` |
| Buyer Checkout, Inventory Hold & Secure Payment | `listBuyerCheckoutInventory` |
| Resale Confirmation, Ownership Transfer & Ticket Delivery | `listResaleConfirmationOwnership` |
| White-Label Marketplace Deployment & Experience Architecture | `listWhiteLabelMarketplace` |

## Ticket Upgrade, Exchange & Conversion — board 1

4 screens · 4 operations to author

| Screen | Operation to author |
|---|---|
| Upgrade Timing, Usage & Ticket Status Rules | `listUpgradeTimingUsage` |
| Upgrade Financial Treatment & Price Difference Rules | `listUpgradeFinancialTreatment` |
| Pro-Rata, Residual Value & Entitlement Credit Configuration | `setProRataResidual` |
| Person-Type, Product & Entitlement Conversion Rules | `listPersonTypeProduct` |

## Unified BI Reporting and AI Analytics Platform — board 1

8 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| Executive Command Center | `listExecutive` |
| Live Operations Dashboard | `listLive` |
| Revenue Pulse | `listRevenuePulse` |
| Attendance & Footfall Intelligence | `listAttendanceFootfall` |
| Capacity & Utilization Monitor | `listCapacityUtilization` |
| Customer, Membership & Loyalty Pulse | `listCustomerMembershipLoyalty` |
| AI Management Insights | `listInsight` |
| Multi-Site & Performance Comparison | `listMultiSitePerformance` |

## Unified BI Reporting and AI Analytics Platform — board 10

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| BI & Analytics Administration Command Center | `listAdministration` |
| Enterprise KPI Library | `listEnterpriseKpi` |
| KPI Targets, Thresholds & Scorecards | `listKpiTargetThreshold` |
| Benchmark & Comparative Analytics Configuration | `listBenchmarkComparative` |
| Benchmark & Comparative Analytics Configuration | `setBenchmarkComparative` |
| Data Source & Integration Registry | `listDataSourceIntegration` |
| Semantic Model & Business Data Catalogue | `listSemanticModelBusiness` |
| Data Refresh, Pipeline & Data Health Monitor | `listDataRefreshPipeline` |
| Embedded BI, Workspace & Tenant Administration | `setEmbeddedTenantAdministration` |
| Analytics Performance, Usage & Cost Monitor | `listPerformanceUsageCost` |

## Unified BI Reporting and AI Analytics Platform — board 2

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Dashboard Library | `list` |
| Dashboard Creation Wizard | `createWizard` |
| Dashboard Creation Wizard | `listWizard` |
| Drag-and-Drop Dashboard Canvas | `listDragDropCanva` |
| Widget & Visualization Library | `listWidgetVisualization` |
| KPI Builder | `setKpi` |
| Targets, Thresholds & KPI Status Rules | `listTargetThresholdKpi` |
| Data & Filter Configuration | `setDataFilter` |
| Drill-Down & Interaction Designer | `setDrillDownInteraction` |
| Dashboard Access, Publishing & Versioning | `listAccessPublishingVersioning` |
| Dashboard Preview, Validation & Health | `listPreviewValidationHealth` |

## Unified BI Reporting and AI Analytics Platform — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Report Catalogue & Library | `listReportCatalogue` |
| Report Creation Wizard | `createReportWizard` |
| Data Domain & Dataset Selector | `listDataDomainDataset` |
| Field & Column Selector | `listFieldColumnSelector` |
| Filter & Parameter Builder | `setFilterParameter` |
| Grouping, Aggregation & Calculation Builder | `setGroupingAggregationCalculation` |
| Cross-Domain Report Composer | `listCrossDomainReport` |
| Report Layout & Formatting Designer | `setReportLayoutFormatting` |
| Report Preview, Test & Validation | `listReportPreviewTest` |
| Save, Run & Report Results Viewer | `listSaveRunReport` |

## Unified BI Reporting and AI Analytics Platform — board 4

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Reporting Governance Command Center | `listReportingGovernance` |
| Report Scheduler | `listReportScheduler` |
| Subscription Manager | `listSubscriptionManager` |
| Distribution & Delivery Configuration | `setDistributionDelivery` |
| Export & Download Center | `listExportDownload` |
| Report API & Data Delivery Manager | `listReportApiData` |
| Report Access & Sharing Control | `listReportAccessSharing` |
| Delivery Monitoring & Failure Management | `listDeliveryMonitoringFailure` |
| Report Audit Trail & Compliance | `listReportTrailCompliance` |
| Retention, Archive & Governance Policy | `listRetentionArchiveGovernance` |

## Unified BI Reporting and AI Analytics Platform — board 5

8 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| Sales & Revenue Command Center | `listSaleRevenue` |
| Ticket Sales Analytics | `listTicketSale` |
| Product & Attraction Performance | `listProductAttractionPerformance` |
| Promotion & Discount Analytics | `listPromotionDiscount` |
| Refund, Cancellation & Revenue Leakage Analytics | `listRefundCancellationRevenue` |
| Reservation & Advance Sales Analytics | `listReservationAdvanceSale` |
| Revenue Recognition & Commercial Allocation | `listRevenueRecognitionCommercial` |
| Sales Forecast, Targets & AI Commercial Intelligence | `listSaleForecastTarget` |

## Unified BI Reporting and AI Analytics Platform — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Finance Analytics Command Center | `listFinance` |
| Payment & Tender Analytics | `listPaymentTender` |
| Payment Gateway Reconciliation | `listPaymentGatewayReconciliation` |
| ERP & Financial System Reconciliation | `listErpFinancialSystem` |
| Accounts Receivable & Aging Analytics | `listAccountReceivableAging` |
| Revenue Recognition & Deferred Revenue Analytics | `listRevenueRecognitionDeferred` |
| Tax, Cost Center & Profit Center Analytics | `listTaxCostProfit` |
| Cashier, POS & Shift Reconciliation Analytics | `listCashierPosShift` |
| Financial Exception & Control Center | `listFinancialException` |
| AI Finance Intelligence & Forecast | `listFinanceForecast` |

## Unified BI Reporting and AI Analytics Platform — board 7

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Live Operations Command Center | `listLive` |
| Attendance & People Count Analytics | `listAttendancePeopleCount` |
| Gate & Access Performance | `listGateAccessPerformance` |
| Occupancy & Capacity Intelligence | `listOccupancyCapacity` |
| Queue & Guest Flow Analytics | `listQueueGuestFlow` |
| Session, Timeslot & Resource Utilization | `listSessionTimeslotResource` |
| Operational Performance & Service Levels | `listOperationalPerformanceService` |
| Operational Exception & Incident Intelligence | `listOperationalExceptionIncident` |
| Site, Attraction & Operational Benchmarking | `listSiteAttractionOperational` |
| AI Operations Intelligence & Predictive Control | `listPredictive` |

## Unified BI Reporting and AI Analytics Platform — board 8

9 screens · 8 operations to author

| Screen | Operation to author |
|---|---|
| Customer Intelligence Command Center | `listCustomer` |
| Customer 360 Analytics | `listCustomer` |
| Customer Segmentation & Behavioral Analytics | `listCustomerSegmentationBehavioral` |
| Customer Acquisition & Conversion Analytics | `listCustomerAcquisitionConversion` |
| Retention, Visit Frequency & Churn Intelligence | `listRetentionVisitFrequency` |
| Membership Performance & Renewal Analytics | `listMembershipPerformanceRenewal` |
| Loyalty Earn, Burn & Engagement Analytics | `listLoyaltyEarnBurn` |
| Campaign & Marketing Performance Analytics | `listCampaignMarketingPerformance` |
| Customer Value & Commercial Behavior Analytics | `listCustomerValueCommercial` |

## Unified BI Reporting and AI Analytics Platform — board 9

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| AI Analytics Command Center | `list` |
| Ask TICVAI — Natural Language Analytics | `listAskTicvaiNatural` |
| AI-Generated Dashboard Studio | `listGenerated` |
| AI-Generated Dashboard Studio | `setGenerated` |
| AI Report Generator | `listReportGenerator` |
| Anomaly Detection Center | `listAnomalyDetection` |
| Root-Cause Analysis Explorer | `listRootCauseAnalysi` |
| Forecasting & Predictive Analytics Studio | `listPredictive` |
| Forecasting & Predictive Analytics Studio | `setPredictive` |
| AI Insight History, Evidence & Explainability | `listInsightEvidenceExplainability` |
| AI Analytics Governance & Model Control | `listGovernanceModel` |

## Upsell,CrossSellEngine — board 1

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Recommendation Command Center | `listRecommendation` |
| Recommendation Strategy Manager | `listRecommendationStrategyManager` |
| Recommendation Objective & KPI Configuration | `setRecommendationObjectiveKpi` |
| Recommendation Type & Product Relationship Manager | `listRecommendationTypeProduct` |
| Recommendation Placement & Touchpoint Manager | `listRecommendationPlacementTouchpoint` |
| Channel & Journey Strategy Manager | `listChannelJourneyStrategy` |
| Recommendation Priority, Ranking & Suppression Manager17 | `listRecommendationPriorityRanking` |
| Recommendation Guardrails & Business Controls | `listRecommendationGuardrailBusiness` |
| Recommendation Policy, AI Control & Governance | `listRecommendationPolicyGovernance` |
| Recommendation Strategy Simulator & AI Advisor | `listRecommendationStrategySimulator` |

## Upsell,CrossSellEngine — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Upsell & Upgrade Command Center | `listUpsellUpgrade` |
| Upgrade Path & Product Ladder Builder | `setUpgradePathProduct` |
| Upsell Eligibility & Qualification Rules | `listUpsellEligibilityQualification` |
| Upgrade Price Difference & Value Proposition Manager | `listUpgradePriceDifference` |
| Ticket, Experience & Bundle Upgrade Manager | `listTicketExperienceBundle` |
| Membership & Pass Upgrade Engine | `listMembershipPassUpgrade` |
| Pre-Purchase, Cart & Checkout Upsell Manager | `listPrePurchaseCart` |
| Post-Purchase & In-Journey Upgrade Manager | `listPostPurchaseJourney` |
| Upsell Ranking, Propensity & AI Opportunity Engine | `listUpsellRankingPropensity` |
| Upgrade Simulator, Comparison & AI Advisor | `listUpgradeSimulatorComparison` |

## Upsell,CrossSellEngine — board 3

9 screens · 9 operations to author

| Screen | Operation to author |
|---|---|
| Cross-Sell Relationship Builder | `setCrossSellRelationship` |
| Product Affinity Matrix & Relationship Map | `listProductAffinityMatrix` |
| Frequently Bought Together & Basket Pattern Engine | `listFrequentlyBoughtTogether` |
| Cross-Category Recommendation Manager | `listCrossCategoryRecommendation` |
| Multi-Attraction, Destination & Partner Cross-Sell | `listMultiAttractionDestination` |
| Basket-Aware Cross-Sell & Duplicate Prevention | `listBasketAwareCross` |
| Availability, Inventory & Capacity-Aware Cross-Sell | `listAvailabilityInventoryCapacity` |
| AI Cross-Sell Discovery, Scoring & Ranking Engine | `listCrossSellDiscovery` |
| Cross-Sell Simulator & AI Opportunity Advisor | `listCrossSellSimulator` |

## Upsell,CrossSellEngine — board 4

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Journey & Context Command Center | `listJourneyContext` |
| Customer Journey Map & Touchpoint Designer | `setCustomerJourneyMap` |
| Real-Time Context Rule Engine | `listRealTimeContext` |
| Pre-Purchase & Booking Journey Recommendation Manager | `listPrePurchaseBooking` |
| Post-Purchase & Pre-Visit Recommendation Manager | `listPostPurchasePre` |
| In-Venue & Location-Aware Recommendation Engine | `listVenueLocationAware` |
| Visit State, Itinerary & Time-Aware Recommendation | `listVisitStateItinerary` |
| Omnichannel Recommendation Synchronization | `listOmnichannelRecommendationSynchronization` |
| Contextual Trigger, Frequency & Experience Controls | `listContextualTriggerFrequency` |
| Journey Simulator, Decision Trace & AI Optimization | `listJourneySimulatorDecision` |

## Upsell,CrossSellEngine — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Personalization & NBO Command Center | `listPersonalizationNbo` |
| Customer Recommendation Profile | `listCustomerRecommendationProfile` |
| Customer Feature & Signal Configuration | `setCustomerFeatureSignal` |
| Propensity Model & Customer Intent Manager | `listPropensityModelCustomer` |
| Next-Best-Offer Decision Studio | `setNextBestOffer` |
| Personalized Ranking & Decision Policy Builder | `setPersonalizedRankingDecision` |
| Customer Preference, Fatigue & Suppression Intelligence | `listCustomerPreferenceFatigue` |
| Anonymous, Known & Identity-Transition Personalization.123 | `listAnonymouKnownIdentity` |
| AI Explainability, Confidence & Model Governance | `listExplainabilityConfidenceModel` |
| Personalization Simulator & Next-Best-Offer Lab | `listPersonalizationSimulatorNext` |

## Upsell,CrossSellEngine — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Recommendation Performance Command Center | `listRecommendationPerformance` |
| Recommendation Strategy & Placement Analytics | `listRecommendationStrategyPlacement` |
| Recommendation Experiment & A/B Test Studio | `setRecommendationExperimentTest` |
| Experiment Results & Winner Decision Workspace | `setExperimentResultWinner` |
| Recommendation Attribution & Incrementality Analytics | `listRecommendationAttributionIncrementality` |
| AI Model Performance & Drift Monitor | `listModelPerformanceDrift` |
| Recommendation Governance & Deployment Control | `listRecommendationGovernanceDeployment` |
| AI Risk, Fairness, Explainability & Safety Center | `listRiskFairnessExplainability` |
| Recommendation Audit, Decision Trace & Investigation | `listRecommendationDecisionTrace` |
| AI Optimization & Recommendation Intelligence Lab | `listRecommendationLab` |

## Wallet Configuration Backend Structure v1.0 — board 1

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Wallet Command Center | `listWallet` |
| Wallet Type Library | `listWalletType` |
| Wallet Creation & Provisioning Rules | `createWalletProvisioningRule` |
| Wallet Ownership & Account Association | `listWalletOwnershipAccount` |
| Wallet Currency & Monetary Configuration | `setWalletCurrencyMonetary` |
| Credit & Balance Type Configuration | `setCreditBalanceType` |
| Wallet Feature Profile | `listWalletFeatureProfile` |
| Wallet Lifecycle Configuration | `setWalletLifecycle` |
| Wallet Numbering, Identity & Digital Credentials | `listWalletNumberingIdentity` |
| Wallet Configuration Preview, Validation & Publication | `publishWalletPreviewValidation` |
| Wallet Configuration Preview, Validation & Publication | `setWalletPreviewValidation` |

## Wallet Configuration Backend Structure v1.0 — board 10

12 screens · 12 operations to author

| Screen | Operation to author |
|---|---|
| Wallet Integration Command Center | `listWalletIntegration` |
| Wallet API Catalogue & Endpoint Configuration | `setWalletApiCatalogue` |
| Integration Profile & System Mapping | `listIntegrationProfileSystem` |
| Wallet Events, Webhooks & Notification Orchestration | `listWalletEventWebhook` |
| API Security, Access & Integration Permissions | `listApiSecurityAccess` |
| Synchronization, Retry & Resilience Configuration | `setSynchronizationRetryResilience` |
| Integration Monitoring & Exception Workbench | `listIntegrationMonitoringException` |
| Wallet Configuration Governance & Version Control | `setWalletGovernanceVersion` |
| Approval, Publication & Change Management | `approveChange` |
| Approval, Publication & Change Management | `listChange` |
| Approval, Publication & Change Management | `publishChange` |
| Wallet Platform Health, Audit & Administration Center | `listWalletPlatformHealth` |

## Wallet Configuration Backend Structure v1.0 — board 2

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Funding Command Center | `listFunding` |
| Funding Method Configuration | `setFundingMethod` |
| Top-Up Rule Configuration | `setTopRule` |
| Channel & Funding Source Mapping | `listChannelFundingSource` |
| Auto-Reload Configuration | `setAutoReload` |
| Recurring Funding Schedule | `listRecurringFundingSchedule` |
| Funding Authorization & Approval Rules | `approveFundingAuthorizationRule` |
| Funding Reversal & Correction Management | `listFundingReversalCorrection` |
| Funding Limits & Velocity Controls | `listFundingLimitVelocity` |
| Funding Transaction Audit & Reconciliation | `listFundingTransactionReconciliation` |

## Wallet Configuration Backend Structure v1.0 — board 3

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Stored Value & Credit Command Center | `listStoredValueCredit` |
| Credit Type Definition Studio | `setCreditTypeDefinition` |
| Credit Issuance Rule Configuration | `setCreditIssuanceRule` |
| Credit Usage & Eligibility Rules | `listCreditUsageEligibility` |
| Consumption Priority Engine | `listConsumptionPriority` |
| Expiry & Validity Policy Configuration | `setExpiryValidityPolicy` |
| FEFO & Credit Lot Management | `listFefoCreditLot` |
| Split Tender & Multi-Credit Consumption | `listSplitTenderMulti` |
| Credit Expiry, Extension & Forfeiture Operations | `listCreditExpiryExtension` |
| Consumption Simulator, Validation & Rule Publication | `publishConsumptionSimulatorValidation` |

## Wallet Configuration Backend Structure v1.0 — board 4

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Shared Wallet Command Center | `listSharedWallet` |
| Shared Wallet Model Configuration | `setSharedWalletModel` |
| Family & Household Structure Configuration | `setFamilyHouseholdStructure` |
| Parent–Child Stored Value Distribution | `listParentChildStored` |
| Allowance & Budget Allocation Engine | `listAllowanceBudgetAllocation` |
| Member Spending Controls & Permissions | `listMemberSpendingPermission` |
| Corporate Wallet & Organizational Hierarchy | `listCorporateWalletOrganizational` |
| Corporate Budget, Policy & Approval Rules | `approveCorporateBudgetPolicy` |
| Shared Wallet Transfers & Balance Reallocation | `listSharedWalletTransfer` |
| Shared Wallet Simulator, Monitoring & Audit | `listSharedWalletSimulator` |

## Wallet Configuration Backend Structure v1.0 — board 5

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Gift Card & Digital Benefit Command Center | `listGiftCardDigital` |
| Gift Card Product Configuration | `setGiftCardProduct` |
| Gift Card Issuance, Activation & Distribution | `listGiftCardIssuance` |
| Voucher & Coupon Type Configuration | `setVoucherCouponType` |
| Voucher Eligibility & Redemption Rule Studio | `setVoucherEligibilityRedemption` |
| Membership Benefits & Entitlement Mapping | `listMembershipBenefitEntitlement` |
| Benefit Packaging & Digital Wallet Presentation | `listBenefitPackagingDigital` |
| Gift Card & Voucher Expiry Management | `listGiftCardVoucher` |
| Gift Card Balance, Liability & Breakage Control | `listGiftCardBalance` |
| Gift Card & Voucher Simulator, Validation & Publication | `publishGiftCardVoucher` |

## Wallet Configuration Backend Structure v1.0 — board 6

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Wallet Usage & Channel Command Center | `listWalletUsageChannel` |
| Wallet Channel Configuration | `setWalletChannel` |
| Wallet Payment & Redemption Policy | `listWalletPaymentRedemption` |
| Wearable & Credential Type Configuration | `setWearableCredentialType` |
| Wearable Linking & Wallet Association Rules | `listWearableLinkingWallet` |
| NFC, RFID & QR Interaction Rules | `listNfcRfidInteraction` |
| Digital Key & Wallet Authentication Policy | `listDigitalKeyWallet` |
| Offline Wallet & Degraded Mode Configuration | `setOfflineWalletDegraded` |
| Device, Terminal & Acceptance Point Mapping | `listDeviceTerminalAcceptance` |
| Wallet Transaction Simulator, Monitoring & Channel Audit | `listWalletTransactionSimulator` |

## Wallet Configuration Backend Structure v1.0 — board 7

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Wallet Operations Command Center | `listWallet` |
| Peer-to-Peer Transfer Configuration | `setPeerTransfer` |
| Transfer Eligibility, Limits & Approval Rules | `approveTransferEligibilityLimit` |
| Refund Routing & Credit Restoration Engine | `listRefundRoutingCredit` |
| Reversal & Transaction Correction Management | `listReversalTransactionCorrection` |
| Administrative Balance Adjustment Studio | `setAdministrativeBalanceAdjustment` |
| Wallet Block, Freeze & Restriction Management | `listWalletBlockFreeze` |
| Wallet Disputes & Operational Exception Queue | `listWalletDisputeOperational` |
| Operations Simulator, Approval & Audit Trail | `approveSimulatorTrail` |
| Operations Simulator, Approval & Audit Trail | `listSimulatorTrail` |

## Wallet Configuration Backend Structure v1.0 — board 8

11 screens · 11 operations to author

| Screen | Operation to author |
|---|---|
| Wallet Security & Risk Command Center | `listWalletSecurityRisk` |
| Wallet Risk Policy Configuration | `setWalletRiskPolicy` |
| Transaction Risk Scoring Engine | `listTransactionRiskScoring` |
| Velocity & Behavioral Rule Configuration | `setVelocityBehavioralRule` |
| Device, Credential & Account Security | `listDeviceCredentialAccount` |
| AI Fraud & Anomaly Detection Studio | `setFraudAnomalyDetection` |
| Automated Security Action Orchestration | `listAutomatedSecurityAction` |
| Fraud Alert & Investigation Case Management | `listFraudAlertInvestigation` |
| Security Rules Testing, Simulation & AI Sandbox | `simulateSecurityRuleTesting` |
| Security Governance, Audit & Rule Publication | `listSecurityGovernanceRule` |
| Security Governance, Audit & Rule Publication | `publishSecurityGovernanceRule` |

## Wallet Configuration Backend Structure v1.0 — board 9

10 screens · 10 operations to author

| Screen | Operation to author |
|---|---|
| Wallet Finance & Liability Command Center | `listWalletFinanceLiability` |
| Wallet Financial Classification & Accounting Mapping | `listWalletFinancialClassification` |
| Wallet Sub-Ledger & Balance Control | `listWalletSubLedger` |
| Multi-Source Reconciliation Configuration | `setMultiSourceReconciliation` |
| Reconciliation Exception & Resolution Workbench | `listReconciliationExceptionResolution` |
| Gift Card Liability Management | `listGiftCardLiability` |
| Breakage & Revenue Recognition Policy | `listBreakageRevenueRecognition` |
| Wallet Financial Period & Closing Controls | `listWalletFinancialPeriod` |
| Wallet Analytics & Management Reporting | `listWalletReporting` |
| Finance Validation, Reporting & Audit Center | `listFinanceValidationReporting` |
