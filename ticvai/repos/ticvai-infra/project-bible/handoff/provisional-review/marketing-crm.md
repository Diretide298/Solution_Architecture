# marketing-crm — 68 operations awaiting sign-off

> **These are specified, not unfinished.** Each has a request, a response and a citation of
> the pack page it was read from. `x-ticvai-provisional` means **nobody who has to build it
> has agreed it** — so the only thing that closes one is a decision in this column: *agreed*,
> *corrected* (say how), or *not needed*.

**4 pack(s), read in page order.** A session opens a book and walks it.

- Waiver, Consent & Digital Form Management — **20**
- Customer Service — **19**
- Privacy Consent Preference Management — **19**
- Communication & Notification Platform Services — **10**


---

## Communication & Notification Platform Services

### p4   · `listCommunicationService`

`GET /communication-service` · MARKETING_VIEW · staff · **Communication Service Command Center**

> Provide administrators and technical/operations teams with a centralized view of the health and activity of TICVAI's communication infrastructure. This is not a marketing dashboard.

**`CommunicationServiceCommandCenterView`** — `accessControl`, `averageDeliveryTime`, `crm`, `customerService`, `delivered`, `eSCy`, `emailSent`, `failed`, `finance`, `groupSales`, `inAppNotifications`, `membership`, `messagesProcessedToday`, `otherTicvaiServices`, `pNg`, `pending`, `providerAvailability`, `providerC31k97924s`, `push110k99806s`, `pushNotifications`, `resourceManagement`, `retrying`, `showCommunicationVolumeOriginatingFrom`, `smsSent`, `ticketing`, `waiver`, `wallet`, `whatsappSent`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-784 Communications Center
- serves P09 ADM-038 Communication Service Command Center

**Decision:** 

### p6   · `setChannelProvider`

`PUT /channel-provider` · MARKETING_MANAGE · staff · **Channel & Provider Configuration**

> Configure the external/internal services used by TICVAI to deliver communications.

**`ChannelProviderConfigurationView`** — `account`, `apiConfiguration`, `brand`, `channel`, `country`, `credentialsSecretReference`, `email`, `environment`, `exposedDirectlyInTheUi`, `futureSupportedChannels`, `inAppNotification`, `legalEntity`, `mobilePush`, `priority`, `providerAPrimary`, `providerBFallback`, `providerName`, `rateLimits`, `region`, `sms`, `status`, `testConnection`, `testWebhook`, `timeout`, `webhookConfiguration`, `whatsapp`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-039 Channel & Provider Configuration

**Decision:** 

### p7   · `setSenderIdentityDomain`

`PUT /sender-identity-domain` · MARKETING_MANAGE · staff · **Sender Identity, Domain & Brand Configuration**

> Manage the identities from which TICVAI communications are sent.

**`SenderIdentityDomainBrandConfigurationView`** — `application`, `approvedTemplates`, `approvedUse`, `brand`, `businessAccount`, `country`, `environment`, `fromAddress`, `fromName`, `legalEntity`, `phoneNumber`, `platform`, `provider`, `region`, `replyTo`, `senderId`, `sendingDomain`, `status`, `verificationStatus`

- serves P09 ADM-040 Sender Identity, Domain & Brand Configuration

**Decision:** 

### p9   · `listSystemTransactionalTemplate`

`GET /system-transactional-template` · MARKETING_VIEW · staff · **System Transactional Template Registry**

> Maintain centralized system/transactional communication templates used by TICVAI operational modules. This screen must not replace CRM's marketing template builder.

**`SystemTransactionalTemplateRegistryView`** — `attachmentsWhereApplicable`, `body`, `brand`, `businessEvent`, `channel`, `cta`, `depositDue`, `eventCancelled`, `eventReminder`, `eventRescheduled`, `footer`, `groupBookingConfirmed`, `guardianConsentRequired`, `header`, `language`, `marketingTemplateCrm`, `membershipActivated`, `membershipExpiring`, `paymentFailed`, `paymentSuccessful`, `sourceModule`, `status`, `subject`, `templateId`, `templateName`, `ticketConfirmation`, `ticketResend`, `transactionalTemplatePlatform`, `version`, `waiverReminder`, `waiverRequired`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-789 Transactional Notification Rules
- serves P09 ADM-041 System Transactional Template Registry

**Decision:** 

### p11  · `listBusinessEventNotification`

`GET /business-event-notification` · MARKETING_VIEW · staff · **Business Event & Notification Trigger Mapping**

> Map TICVAI business events to the operational communications they should generate. This is the core of the event-driven communication architecture.

**`BusinessEventNotificationTriggerMappingView`** — `bookingType`, `brand`, `channel`, `customer`, `event`, `eventId`, `eventType`, `membership`, `ownedWithinCrm`, `payload`, `priority`, `product`, `sourceModule`, `status`, `t1Day`, `t30Days`, `t7Days`, `time`, `transactionStatus`, `validEmailEmailPermitted`, `venue`

- serves P09 ADM-042 Business Event & Notification Trigger Mapping

**Decision:** 

### p13  · `listRoutingPriorityThrottling`

`GET /routing-priority-throttling` · MARKETING_VIEW · staff · **Routing, Priority, Throttling & Fallback Rules**

> Determine how TICVAI delivers a message after a communication requirement has been created.

**`RoutingPriorityThrottlingFallbackRulesView`** — `brand`, `brandLimit`, `channel`, `complianceRules`, `cost`, `country`, `eventLimit`, `messageType`, `messagesPerMinute`, `messagesPerSecond`, `nonUrgentHighVolumeCommunication`, `p1Critical`, `p2High`, `p3Normal`, `p4Bulk`, `paymentIssueEventDayNotification`, `primaryProviderA`, `priority`, `provider`, `providerHealth`, `providerLimit`, `recipientType`, `ticketConfirmationWaiverReminder`

- serves P08 BO-790 Scheduling, Priority & Approval
- serves P09 ADM-043 Routing, Priority, Throttling & Fallback Rules

**Decision:** 

### p14  · `listConsentPreferenceCommunication`

`GET /consent-preference-communication` · MARKETING_VIEW · staff · **Consent, Preference & Communication Policy Enforcement**

> Create a central enforcement layer ensuring communications respect the appropriate communication rules.

**`ConsentPreferenceCommunicationPolicyEnforcementView`** — `administrativeSuppression`, `allowed`, `blocked`, `complaint`, `contactRestrictions`, `emailPreference`, `hardBounce`, `invalidEmail`, `invalidMobile`, `language`, `marketing`, `marketingConsent`, `operational`, `optOut`, `pushPreference`, `rerouted`, `service`, `smsPreference`, `suppressed`, `suppression`, `transactional`, `unsubscribed`, `whatsappPreference`

- serves P09 ADM-044 Consent, Preference & Communication Policy Enforcement

**Decision:** 

### p16  · `listDeliveryQueueFailure`

`GET /delivery-queue-failure` · MARKETING_VIEW · staff · **Delivery Queue, Failure & Retry Management**

> Provide technical/operations teams with visibility into communications currently being processed or failing.

**`DeliveryQueueFailureRetryManagementView`** — `attempts`, `businessEvent`, `cancelled`, `changeProvider`, `channel`, `communicationId`, `created`, `deadLettered`, `delivered`, `failed`, `inspectFailure`, `pending`, `priority`, `processing`, `provider`, `recipient`, `replayEventWhereSafe`, `reroute`, `retrying`, `sent`, `sourceModule`, `status`, `template`

- serves P08 BO-791 Delivery, Retry & Failover
- serves P09 ADM-045 Delivery Queue, Failure & Retry Management

**Decision:** 

### p18  · `listProviderHealthUsage`

`GET /provider-health-usage` · MARKETING_VIEW · staff · **Provider Health, Usage & Cost Monitoring**

> Monitor the operational and commercial performance of communication providers.

**`ProviderHealthUsageCostMonitoringView`** — `apiLatency`, `availability`, `businessUnit`, `cost`, `costPerMessage`, `deliveryTime`, `erSDelivery1k`, `event`, `failureRate`, `fallbackUsage`, `ng`, `retries`, `successRate`, `tenant`, `trackContractualProviderTargetsWhereConfigured`, `volume`

- serves P08 BO-792 Deliverability & Analytics
- serves P09 ADM-046 Provider Health, Usage & Cost Monitoring

**Decision:** 

### p19  · `listDeliveryCommunicationPlatform`

`GET /delivery-communication-platform` · MARKETING_VIEW · staff · **AI Delivery Optimization & Communication Platform Diagnostics**

> Provide an AI intelligence layer focused specifically on communication infrastructure performance, not CRM marketing strategy.

**`AiDeliveryOptimizationCommunicationPlatformDiagnostiView`** — `businessEvents`, `channels`, `consentPreferenceCommunicationPolicy`, `cost`, `delivery`, `failures`, `groupArrivals`, `guardianConsentIsIncomplete`, `health`, `historicalPatterns`, `latency`, `majorEvents`, `membershipRenewals`, `operationalAlerting`, `providerFailover`, `providers`, `queueScaling`, `queues`, `recipientPreferences`, `regionalPerformance`, `retries`, `ticketReleases`, `waiverDeadlines`, `whyDidCommunicationCostIncrease`

- serves P09 ADM-047 AI Delivery Optimization & Communication Platform Diagnostics

**Decision:** 


---

## Customer Service

### p3   · `listCustomerService`

`GET /customer-service` · MARKETING_VIEW · staff · **Customer Service Command Center**

> Provide every customer-service agent with a personalized operational workspace showing customers, cases, tasks, SLAs, alerts and workload.

**`CustomerServiceCommandCenterView`** — `assignedAgent`, `averageResolutionTime`, `awaitingCustomer`, `awaitingInternalTeam`, `callCustomer`, `caseId`, `casesDueToday`, `category`, `channel`, `customer`, `escalatedCases`, `findBooking`, `findCustomer`, `findOrder`, `findTicket`, `followUpFinance`, `lastInteraction`, `myOpenCases`, `newCase`, `newCases`, `nextAction`, `priority`, `requestSupervisorApproval`, `resolvedToday`, `respondToComplaint`, `slaAtRisk`, `slaBreached`, `slaRemaining`, `status`, `subject`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P12 SUP-009 Customer Service Command Center
- serves P12 SUP-010 Customer 360° Service Profile

**Decision:** 

### p5   · `listCustomerServiceProfile`

`GET /customer-service-profile` · MARKETING_VIEW · staff · **Customer 360° Service Profile**

> Provide the agent with a complete customer-service view of the customer. This should be one of the most important screens in the entire Customer Service module.

**`Customer360ServiceProfileView`** — `accessibilityRequirementsWhereAppropriatelyAuthorized`, `activeMembership`, `activeReservations`, `communicationRestrictions`, `contactDetails`, `country`, `customerId`, `customerName`, `customerSince`, `customerType`, `customerValue`, `disputesRecorded`, `futureGroupBookingWhereApplicable`, `loyaltyTier`, `marketingConsent`, `maskedWhereAppropriate`, `membershipRenewed`, `membershipStatus`, `preferredCommunicationChannel`, `preferredLanguage`, `riskAttentionIndicator`, `roleRestricted`, `upcomingTickets`, `walletBalance`

- serves P08 BO-737 Customer 360 Profile
- serves P12 SUP-009 Customer Service Command Center
- serves P12 SUP-010 Customer 360° Service Profile

**Decision:** 

### p7   · `listUnifiedInteractionCommunication`

`GET /unified-interaction-communication` · MARKETING_VIEW · staff · **Unified Interaction & Communication History**

> Provide one chronological timeline of customer interactions across supported service channels.

**`UnifiedInteractionCommunicationHistoryView`** — `agentSystem`, `attachments`, `automatedNotifications`, `b2cPortal`, `channel`, `customer`, `dateTime`, `direction`, `email`, `internalNotes`, `liveChat`, `mobileApp`, `phone`, `posFrontDesk`, `relatedCase`, `relatedOrder`, `relatedTicket`, `sentimentWhereEnabled`, `socialChannelWhereIntegrated`, `subject`, `webForm`, `whatsappWhereIntegrated`

- serves P08 BO-803 Chat Analytics & Audit
- serves P12 SUP-011 Unified Interaction & Communication History

**Decision:** 

### p9   · `createCaseClassificationIntelligent`

`POST /case-classification-intelligent` · MARKETING_MANAGE · staff · **Case Creation, Classification & Intelligent Routing**

> Create structured customer-service cases and ensure they reach the correct team.

**`CaseCreationClassificationIntelligentRoutingView`** — `accessProblem`, `agentSkill`, `attachments`, `bookingIssue`, `category`, `complaint`, `customer`, `customerType`, `description`, `event`, `eventProximity`, `exchange`, `generalEnquiry`, `groupBooking`, `language`, `lostTicket`, `loyalty`, `membership`, `payment`, `priority`, `product`, `relatedMembership`, `relatedOrder`, `relatedPayment`, `relatedTicket`, `reschedule`, `source`, `subcategory`, `subject`, `technicalIssue`, `ticketIssue`, `venue`, `wallet`, `workload`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P12 SUP-012 Case Creation, Classification & Intelligent Routing

**Decision:** 

### p11  · `setCaseInvestigationResolution`

`PUT /case-investigation-resolution` · MARKETING_MANAGE · staff · **Case Investigation & Resolution Workspace**

> Provide the primary workspace in which an agent investigates and resolves a case.

**`CaseInvestigationResolutionWorkspaceView`** — `accessEvent`, `actionHistory`, `attachments`, `call`, `caseId`, `category`, `centerCaseTimeline`, `changeStatus`, `conversationNotesActionsAndInvestigation`, `created`, `customer`, `customerProfileAndRelatedProducts`, `departmentNotes`, `groupBooking`, `lastUpdated`, `leftCustomerContext`, `membership`, `mentions`, `order`, `owner`, `payment`, `priority`, `privateNotes`, `queue`, `reply`, `requestApproval`, `rightRecommendedActions`, `sla`, `status`, `subject`, `ticket`, `walletTransaction`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-807 Classification & Workflow
- serves P12 SUP-013 Case Investigation & Resolution Workspace

**Decision:** 

### p13  · `setOrderBookingTicket`

`PUT /order-booking-ticket` · MARKETING_MANAGE · staff · **Order, Booking & Ticket Service Workspace**

> Allow customer-service agents to perform permitted ticket/order servicing without entering the underlying technical modules.

**`OrderBookingTicketServiceWorkspaceView`** — `amount`, `changeName`, `channel`, `dateTime`, `exchange`, `fulfillment`, `inCustomerService`, `order`, `payment`, `products`, `purchaseDate`, `requestRefund`, `reschedule`, `saturday1600`, `sunday1400Aed0`, `sunday1600Aed20Ticket`, `ticketStatus`, `tickets`

- serves P08 BO-801 Sales & Service Actions
- serves P12 SUP-014 Order, Booking & Ticket Service Workspace

**Decision:** 

### p15  · `setRefundCompensationService`

`PUT /refund-compensation-service` · MARKETING_MANAGE · staff · **Refund, Compensation & Service Exception Workspace**

> Manage cases requiring money, compensation, goodwill or policy exceptions.

**`RefundCompensationServiceExceptionWorkspaceView`** — `aed2011000`, `agentPermitted`, `amountPaid`, `amountUsed`, `complimentaryTicket`, `discount`, `feeWaiver`, `fees`, `fullRefund`, `managerFinanceApproval`, `originalTransaction`, `partialRefund`, `policyException`, `previousRefund`, `proposedCompensation`, `proposedRefund`, `refundableAmount`, `serviceCredit`, `supervisorApproval`, `voucher`, `walletCredit`

- serves P08 BO-812 Service Recovery
- serves P08 BO-822 Service Recovery Automation
- serves P12 SUP-015 Refund, Compensation & Service Exception Workspace

**Decision:** 

### p16  · `listEscalationCollaborationInternal`

`GET /escalation-collaboration-internal` · MARKETING_VIEW · staff · **Escalation, Collaboration & Internal Resolution**

> Allow Customer Service to collaborate with other TICVAI departments without losing ownership of the customer case.

**`EscalationCollaborationInternalResolutionView`** — `accessControl`, `assignee`, `attachments`, `confirmRefundTransactionStatus`, `crm`, `department`, `dueDate`, `escalationType`, `fB`, `finance`, `groupSales`, `management`, `membership`, `operations`, `priority`, `relatedCase`, `relatedTransaction`, `request`, `retail`, `technicalSupport`, `ticketing`, `venueManagement`

- serves P12 SUP-016 Escalation, Collaboration & Internal Resolution

**Decision:** 

### p17  · `listCaseResolutionClosure`

`GET /case-resolution-closure` · MARKETING_VIEW · staff · **Case Resolution, Closure & Customer Feedback**

> Govern how cases are resolved and formally closed.

**`CaseResolutionClosureCustomerFeedbackView`** — `actionTaken`, `compensation`, `content`, `csatSurvey`, `customer`, `customerNotification`, `customerReplies`, `feedbackRequest`, `financialActionCompleteOrTracked`, `financialImpact`, `integration`, `internalTasksCompleted`, `operational`, `payment`, `policy`, `product`, `requiredApprovalsComplete`, `requiredCustomerResponseSent`, `resolutionCategory`, `resolutionDate`, `resolutionDocumented`, `resolutionFails`, `resolutionSummary`, `resolvedBy`, `rootCause`, `serviceRating`, `staff`, `supervisorReopens`, `system`, `unknown`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P12 SUP-017 Case Resolution, Closure & Customer Feedback

**Decision:** 

### p19  · `setCustomerServiceCopilot`

`PUT /customer-service-copilot` · MARKETING_MANAGE · staff · **AI Customer Service Copilot & Knowledge Workspace**

> Create the AI intelligence layer assisting agents throughout the service journey. This should not be a simple chatbot added to the side of the screen. It should understand the customer + transaction + policy + case context.

**`AiCustomerServiceCopilotKnowledgeWorkspaceView`** — `applicablePolicy`, `availability`, `brandTone`, `caseContext`, `caseCreationClassificationIntelligent`, `caseResponse`, `chat`, `collaboration`, `customerBalances`, `customerLanguage`, `email`, `findSundaySAvailableAlternatives`, `internalEscalation`, `paymentFinanceServices`, `paymentStatus`, `takingIntoAccount`, `ticketValidity`, `timeline`, `whatsapp`, `whyCanTThisCustomerReschedule`

- serves P08 BO-797 AI Chatbot Configuration
- serves P08 BO-798 Intent & Knowledge Management
- serves P12 SUP-018 AI Customer Service Copilot & Knowledge Workspace

**Decision:** 

### p24  · `listContact`

`GET /contact` · MARKETING_VIEW · staff · **Contact Center Operations Command Center**

> Provide supervisors and management with a real-time view of customer-service operations across

**`ContactCenterOperationsCommandCenterView`** — `activeAgents`, `agentUtilization`, `averageResolutionTime`, `b2cPortal`, `casesResolvedToday`, `casesToday`, `criticalCases`, `csat`, `customersWaiting`, `email`, `firstContactResolution`, `firstResponseTime`, `frontDesk`, `frontPos`, `liveChat`, `mobileApp`, `nNgRiskTs`, `ng`, `phone`, `slaAtRisk`, `slaBreached`, `socialChannelsWhereIntegrated`, `unassignedCases`, `webForm`, `whatsapp`

- serves P12 SUP-019 Contact Center Operations Command Center

**Decision:** 

### p27  · `setIntelligentRoutingSkill`

`PUT /intelligent-routing-skill` · MARKETING_MANAGE · staff · **Intelligent Routing, Skills & Assignment Engine**

> Determine the best agent or team to handle each customer request.

**`IntelligentRoutingSkillsAssignmentEngineView`** — `agentAvailability`, `agentSkill`, `caseCategory`, `caseTicketReschedule`, `channel`, `currentWorkload`, `customerLanguage`, `customerType`, `event`, `eventProximity`, `languageArabic`, `membershipTier`, `priority`, `priorityHigh`, `product`, `sla`, `subcategory`, `type`, `venue`

- serves P08 BO-800 Routing & Queue Management
- serves P12 SUP-021 Intelligent Routing, Skills & Assignment Engine

**Decision:** 

### p29  · `listSlaPolicyService`

`GET /sla-policy-service` · MARKETING_VIEW · staff · **SLA Policy & Service-Level Management**

> Define and monitor service-level commitments for different customer-service scenarios.

**`SlaPolicyServiceLevelManagementView`** — `atRisk`, `averageResolution`, `averageResponse`, `brand`, `breached`, `businessHours`, `calendarTime`, `caseType`, `channel`, `complaintResolutionSla`, `customerTier`, `event`, `firstResponse4Hours`, `firstResponse5Minutes`, `firstResponseSla`, `groupCustomer`, `holidayCalendars`, `internalEscalationSla`, `market`, `nextResponseSla`, `partner`, `pausedStates`, `priority`, `resolutionSla`, `resolutionTarget24Hours`, `resolutionTarget30Minutes`, `slaCompliance`, `venue`, `venueOperatingHours`, `withinSla`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-809 SLA Policy Configuration
- serves P12 SUP-022 SLA Policy & Service-Level Management

**Decision:** 

### p31  · `listAgentWorkloadAvailability`

`GET /agent-workload-availability` · MARKETING_VIEW · staff · **Agent Workload, Availability & Workforce Control**

> Give supervisors visibility and control over active customer-service resources.

**`AgentWorkloadAvailabilityWorkforceControlView`** — `activeCases`, `afterCallWork`, `agent`, `available`, `averageHandleTime`, `break`, `busy`, `calls`, `changeAvailability`, `chats`, `chatting`, `languages`, `managementWhereApplicable`, `offline`, `onCall`, `queue`, `reassignCases`, `requestAssistance`, `resolutionRate`, `skills`, `slaRiskCases`, `status`, `team`, `training`, `utilization`

- serves P08 BO-800 Routing & Queue Management
- serves P08 BO-808 Assignment & Workload
- serves P12 SUP-023 Agent Workload, Availability & Workforce Control

**Decision:** 

### p32  · `listEscalationCriticalCase`

`GET /escalation-critical-case` · MARKETING_VIEW · staff · **Escalation & Critical Case Monitor**

> Provide supervisors with one workspace for cases requiring elevated attention.

**`EscalationCriticalCaseMonitorView`** — `assignedAgent`, `case`, `criticalCases`, `currentStatus`, `customer`, `escalatedCases`, `escalatedTo`, `escalationTime`, `event`, `eventDayEscalations`, `financialEscalations`, `managementEscalations`, `priority`, `reason`, `sla`, `slaBreaches`, `technicalEscalations`, `transactionValue`, `vipEscalations`

- serves P08 BO-810 Escalation Rules
- serves P12 SUP-024 Escalation & Critical Case Monitor

**Decision:** 

### p34  · `listQualityAgentEvaluation`

`GET /quality-agent-evaluation` · MARKETING_VIEW · staff · **Quality Management & Agent Evaluation**

> Measure whether customer-service interactions meet TICVAI's defined service-quality standards.

**`QualityManagementAgentEvaluationView`** — `accuracy`, `call`, `case`, `chat`, `closing`, `communicationCoaching`, `communicationQuality`, `complaint`, `customerVerification`, `documentation`, `email`, `empathy`, `greeting`, `missingCaseDocumentation`, `policyAdherence`, `policyCompliance`, `policyTraining`, `productTraining`, `requiredStatements`, `resolution`, `resolutionQuality`, `systemTraining`, `tone`, `understanding`, `whatsapp`

- serves P08 BO-802 Sentiment, Quality & Escalation
- serves P12 SUP-025 Quality Management & Agent Evaluation

**Decision:** 

### p35  · `listCustomerSatisfactionFeedback`

`GET /customer-satisfaction-feedback` · MARKETING_VIEW · staff · **Customer Satisfaction, Feedback & Voice of Customer**

> Measure customer perception of TICVAI's support experience and identify recurring service problems.

**`CustomerSatisfactionFeedbackVoiceOfCustomerView`** — `agent`, `appFeedback`, `case`, `caseType`, `channel`, `complaint`, `complaintReview`, `complaints`, `csat`, `customerEffortWhereMeasured`, `customerType`, `directCustomerComment`, `event`, `followUpCase`, `language`, `negative`, `neutral`, `npsWhereUsed`, `positive`, `postCaseSurvey`, `product`, `productEvent`, `rating`, `repeatContactRate`, `sentiment`, `serviceRating`, `supervisorTask`, `surveyResponseRate`, `team`, `topic`, `venue`, `webFeedback`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-814 Voice of Customer Center
- serves P08 BO-818 Survey Responses & Insights
- serves P08 BO-821 AI Sentiment & Topic Analysis

**Decision:** 

### p37  · `listServiceRootCause`

`GET /service-root-cause` · MARKETING_VIEW · staff · **Service Analytics & Root-Cause Intelligence**

> Provide comprehensive analytics explaining why customers contact TICVAI and what is driving service demand.

**`ServiceAnalyticsRootCauseIntelligenceView`** — `betterB2cInformation`, `betterTicketDelivery`, `cases`, `complaintRate`, `contactVolume`, `costPerCaseWhereAvailable`, `csat`, `escalationRate`, `eventVsEvent`, `firstContactResolution`, `firstResponseTime`, `improvedNotifications`, `monthVsMonth`, `productConfiguration`, `productVsProduct`, `reopenRate`, `resolutionTime`, `selfService`, `slaCompliance`, `technicalFixes`, `todayVsYesterday`, `venueVsVenue`, `weekVsWeek`

- serves P08 BO-823 VOC Analytics & Audit
- serves P12 SUP-027 Service Analytics & Root-Cause Intelligence

**Decision:** 

### p39  · `listContactAutomation`

`GET /contact-automation` · MARKETING_VIEW · staff · **AI Contact Center Intelligence & Automation Studio**

> Create the management-level AI intelligence layer for Customer Service. This is different from 10.1.10 AI Customer Service Copilot. Board 1 Copilot = helps one agent resolve one case. Board 2 AI Intelligence = improves the entire service operation.

**`AiContactCenterIntelligenceAutomationStudioView`** — `agentPerformance`, `aiPreparesActionAgentApproves`, `aiSuggestsAction`, `allowedActions`, `approval`, `approvedLowRiskWorkflowsExecuteAutomatically`, `auditTrail`, `cases`, `confidenceThreshold`, `contactVolume`, `customerFeedback`, `effectiveDates`, `estimatedAutomationConfidence964`, `eventDaySupportDemand`, `events`, `exceptionHandling`, `expectedComplaints`, `interactions`, `killSwitch`, `level1RecommendOnly`, `level2AgentConfirmation`, `level3SupervisorGovernedAutomation`, `management`, `onlySpecificallyApprovedScenarios`, `orders`, `owner`, `payments`, `products`, `qa`, `queueDemand`, `queues`, `requiredAgents`, `scope`, `sla`, `slaRisk`, `systemIncidents`, `tickets`, `version`

> ⚠ **38 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P12 SUP-028 AI Contact Center Intelligence & Automation Studio

**Decision:** 


---

## Privacy Consent Preference Management

### p4   · `listPrivacyConsent`

`GET /privacy-consent` · MARKETING_VIEW · staff · **Privacy & Consent Configuration Command Center**

> Provide administrators with one central dashboard for configuring and governing TICVAI's privacy framework across tenants, brands, venues and customer channels.

**`PrivacyConsentConfigurationCommandCenterView`** — `activeConsentCapturePoints`, `activeConsentPurposes`, `activePrivacyPolicies`, `communicationPreferenceTypes`, `configurationWarnings`, `consentConfigurationsRequiringReview`, `cookieCategories`, `nFrom`, `pendingPolicyApprovals`, `scheduledPolicyChanges`, `supportedLanguages`, `testConfiguration`, `v3201Sep`

- serves P13 CMS-021 Privacy & Consent Configuration Command Center

**Decision:** 

### p5   · `listDataProcessingPurpose`

`GET /data-processing-purpose` · MARKETING_VIEW · staff · **Data Processing Purpose & Lawful Basis Registry**

> Create a central registry explaining why customer data is being collected or processed. This becomes the foundation used by consent forms, policies, customer journeys and downstream systems.

**`DataProcessingPurposeLawfulBasisRegistryView`** — `administratorConfiguresIt`, `biometrics`, `businessOwner`, `capturePoints`, `childrenSData`, `consent`, `consentDefinitions`, `contractualNecessity`, `countriesJurisdictions`, `dataCategories`, `dataControllerApplicableOrganization`, `dataSubjectCategories`, `description`, `effectiveDates`, `frameworkForExample`, `identityDocuments`, `legalObligation`, `legitimateInterest`, `otherConfiguredBasis`, `otherOrganizationDefinedSensitiveCategories`, `policiesNotices`, `preciseLocation`, `processingActivities`, `purposeId`, `purposeName`, `retentionPolicies`, `retentionReference`, `status`, `systemsModules`, `thirdPartyProcessors`, `thirdPartyProviderReference`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-022 Data Processing Purpose & Lawful Basis Registry

**Decision:** 

### p8   · `setCommunicationPreferenceMarketing`

`PUT /communication-preference-marketing` · MARKETING_MANAGE · staff · **Communication Preference & Marketing Permission Configuration**

> Define how customers control the communications they wish to receive. This screen should integrate strongly with CRM and Marketing but remain governed by the central Privacy Engine.

**`CommunicationPreferenceMarketingPermissionConfiguratView`** — `applicableBrands`, `applicableCountries`, `availableChannels`, `birthdayCampaigns`, `channelPurposeBrand`, `communicationType`, `communications`, `consentDependency`, `customerEditableStatus`, `defaultBehavior`, `directMail`, `email`, `eventChanges`, `loyaltyOffers`, `marketingTransactionalClassification`, `membershipOffers`, `newEvents`, `orderConfirmation`, `otherFutureChannels`, `partnerOffers`, `paymentInformation`, `phone`, `preferenceCategory`, `promotions`, `pushNotification`, `securityMessages`, `sms`, `surveys`, `ticketDelivery`, `treatedAsTheSameThing`, `whatsapp`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-749 Guest Preference Center
- serves P13 CMS-024 Communication Preference & Marketing Permission Configuration

**Decision:** 

### p10  · `listCookieTrackingDigital`

`GET /cookie-tracking-digital` · MARKETING_VIEW · staff · **Cookie, Tracking & Digital Technology Registry**

> Maintain a centralized registry of cookies, SDKs, pixels and other governed tracking technologies used by TICVAI digital channels. This should cover more than traditional browser cookies.

**`CookieTrackingDigitalTechnologyRegistryView`** — `advertisingMarketing`, `advertisingPixel`, `analytics`, `analyticsTracker`, `applicableChannel`, `applicableCountry`, `b2cWebsite`, `category`, `consentRequirement`, `customerPortal`, `dataCollected`, `domainApplication`, `duration`, `embeddedCheckout`, `embeddedService`, `firstPartyCookie`, `firstThirdParty`, `functional`, `mobileApp`, `mobileSdk`, `name`, `otherOrganizationDefinedCategories`, `otherTrackingTechnology`, `partnerMicrosites`, `personalization`, `personalizationTechnology`, `privacyInformation`, `processingPurpose`, `provider`, `purpose`, `sessionTechnology`, `status`, `strictlyNecessary`, `technologyId`, `thirdPartyCookie`, `whiteLabelSites`

> ⚠ **36 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-025 Cookie, Tracking & Digital Technology Registry

**Decision:** 

### p11  · `listCookieBannerPreference`

`GET /cookie-banner-preference` · MARKETING_VIEW · staff · **Cookie Banner & Preference Center Designer**

> Provide a no-code designer for privacy/cookie interfaces displayed on digital channels.

**`CookieBannerPreferenceCenterDesignerView`** — `additionalConfiguredLanguages`, `analyticsOnOff`, `arabicRtl`, `branding`, `buttons`, `categoryDescriptions`, `description`, `desktop`, `english`, `functionalOnOff`, `language`, `links`, `logo`, `marketingOnOff`, `mobile`, `necessaryAlwaysActive`, `personalizationOnOff`, `position`, `tablet`, `theme`, `title`

- serves P13 CMS-026 Cookie Banner & Preference Center Designer

**Decision:** 

### p12  · `setConsentCapturePoint`

`PUT /consent-capture-point` · MARKETING_MANAGE · staff · **Consent Capture Point & Customer Journey Configuration**

> Define where, when and under what circumstances privacy notices and consent requests appear. This prevents each channel from implementing consent independently.

**`ConsentCapturePointCustomerJourneyConfigurationView`** — `accountRegistration`, `annualPassEnrollment`, `apiPartnerJourney`, `brand`, `channel`, `competitionPromotion`, `consentWording`, `country`, `crmCustomerCreation`, `customerPortal`, `customerType`, `displayOrder`, `faceEnrollment`, `guestCheckout`, `kiosk`, `language`, `mandatoryOptionalBehavior`, `membershipEnrollment`, `mobileAppRegistration`, `newsletterSignup`, `optionalPreferences`, `policyVersion`, `posCustomerCreation`, `processingPurpose`, `requiredConsent`, `requiredNotice`, `ticketPurchase`, `walletEnrollment`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-027 Consent Capture Point & Customer Journey Configuration

**Decision:** 

### p14  · `listPrivacyNoticePolicy`

`GET /privacy-notice-policy` · MARKETING_VIEW · staff · **Privacy Notice, Policy & Terms Version Management**

> Manage customer-facing privacy notices and related governed documents with complete version control.

**`PrivacyNoticePolicyTermsVersionManagementView`** — `approvedBy`, `biometricPrivacyNotice`, `childrenSPrivacyNotice`, `cookieNotice`, `determinedByAi`, `documentId`, `effectiveFrom`, `effectiveTo`, `elsewhere`, `language`, `locationServicesNotice`, `marketingNotice`, `material`, `minor`, `noCustomerAction`, `otherOrganizationDefinedPrivacyDocuments`, `owner`, `privacyNotice`, `privacyPolicy`, `publishedAt`, `record`, `requiresNotification`, `requiresReAcceptance`, `status`, `version`

- serves P13 CMS-028 Privacy Notice, Policy & Terms Version Management

**Decision:** 

### p15  · `setMinorGuardianAge`

`PUT /minor-guardian-age` · MARKETING_MANAGE · staff · **Minor, Guardian & Age-Based Privacy Configuration**

> Provide specialized privacy configuration for journeys involving children and guardians. This is especially important for TICVAI customers operating: Theme parks Attractions Camps Academies Family entertainment Children's events

**`MinorGuardianAgeBasedPrivacyConfigurationView`** — `accountAuthentication`, `ageVerificationMethod`, `andSeparately`, `consentRequirements`, `consentStatus`, `consentVersion`, `dateTime`, `email`, `emailOtp`, `guardianName`, `guardianRequiredThreshold`, `minorThreshold`, `mobile`, `otherApprovedMethod`, `participationWaiverWaiverEngine`, `privacyConsentArea17`, `relationship`, `remainDistinctLegalOperationalObjects`, `restrictedMarketing`, `restrictedPersonalization`, `restrictedProcessing`, `restrictedTracking`, `smsOtp`, `staffVerification`, `thisDistinctionIsCritical`, `verificationStatus`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-029 Minor, Guardian & Age-Based Privacy Configuration

**Decision:** 

### p16  · `approvePrivacyTesting`

`PUT /privacy-testing` · MARKETING_MANAGE · staff · **Privacy Configuration Testing, Approval & Publication**

> Act as the final governance gate before privacy configurations are deployed into production. No major privacy configuration should move directly from editing to production without validation.

**`PrivacyConfigurationTestingApprovalPublicationView`** — `approval`, `backendScreenCoreResponsibility`, `beforeAfter`, `biometricConsentNotApplicable`, `board1Configure`, `brand`, `channel`, `circularConfigurationDependency`, `conflictingConsentRules`, `controlledRollout`, `cookiePreferencesDisplay`, `country`, `customerAge`, `customerStatus`, `emailMarketingOptional`, `existingConsents`, `existingPolicyAcceptance`, `guardianFlowNotRequired`, `invalidEffectiveDates`, `language`, `membership`, `missingConsentMapping`, `missingGuardianRule`, `missingLanguage`, `missingPolicy`, `missingProcessingPurpose`, `privacyNoticeV51Display`, `product`, `publication`, `reason`, `requestedProcessing`, `rollback`, `selectedBrand`, `selectedChannel`, `selectedCountry`, `selectedTenant`, `testResult`, `unmappedTrackingTechnology`, `unpublishedDependency`, `whoChangedConfiguration`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-030 Privacy Configuration Testing, Approval & Publication

**Decision:** 

### p21  · `listPrivacy`

`GET /privacy` · MARKETING_VIEW · staff · **Privacy Operations Command Center**

> Provide Privacy, Compliance and authorized operational teams with a centralized real-time overview of privacy operations across TICVAI.

**`PrivacyOperationsCommandCenterView`** — `activeConsentRecords`, `analytics`, `biometrics`, `consentEvidenceExceptions`, `emailMarketing`, `investigateEvidence`, `location`, `marketingOptIns`, `marketingOptOuts`, `otherConfiguredPurposes`, `overdueRequests`, `pendingAnonymization`, `pendingDataRightsRequests`, `pendingDeletionActions`, `personalization`, `policyReAcceptancePending`, `privacyIncidentsExceptions`, `push`, `retentionActionsDue`, `smsMarketing`, `totalCustomerPrivacyProfiles`, `whatsappMarketing`, `withdrawnConsents`

- serves P08 BO-752 Privacy & AI Governance
- serves P13 CMS-031 Privacy Operations Command Center

**Decision:** 

### p22  · `listCustomerPrivacyConsent`

`GET /customer-privacy-consent` · MARKETING_VIEW · staff · **Customer Privacy, Consent & Preference 360°**

> Provide one authoritative privacy view for an individual customer or participant. This becomes the privacy equivalent of the customer 360° workspace.

**`CustomerPrivacyConsentPreference360View`** — `access`, `account`, `accountStatus`, `ageCategory`, `biometricNotice`, `biometricsV4015AugApp`, `brandPreferences`, `childrenSPrivacyNotice`, `choices`, `cookieNoticeVersion`, `correction`, `country`, `customerId`, `declinedV1412AugB2c`, `deletion`, `emailPreference`, `guardianRelationshipWhereApplicable`, `informationExists`, `marketingCategories`, `name`, `objection`, `otherApplicablePrivacyDocuments`, `otherConfiguredRequests`, `personalizationPreferences`, `preferredLanguage`, `privacyPolicyVersion`, `privacyRiskExceptionIndicator`, `pushPreference`, `restriction`, `smsPreference`, `v2820AugPortal`, `v3212AugB2c`, `whatsappPreference`, `whatsappV2112AugApp`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-021 Privacy & Consent Configuration Command Center
- serves P13 CMS-032 Customer Privacy, Consent & Preference 360°

**Decision:** 

### p24  · `listConsentEvidenceWithdrawal`

`GET /consent-evidence-withdrawal` · MARKETING_VIEW · staff · **Consent Evidence, History & Withdrawal Management**

> Maintain legally and operationally useful evidence of every consent event and manage subsequent withdrawals.

**`ConsentEvidenceHistoryWithdrawalManagementView`** — `acknowledged`, `action`, `api`, `authorizedStaff`, `brand`, `channel`, `consentPurpose`, `consentVersion`, `country`, `customerParticipant`, `customerPortal`, `customerService`, `dateTime`, `deviceSessionReferenceWherePermitted`, `evidenceId`, `exactApplicableWordingVersionReference`, `failed`, `guardianReferenceWhereApplicable`, `journeyCapturePoint`, `mobileApp`, `preferenceCenter`, `processed`, `propagated`, `requested`, `sourceSystem`, `status`, `userCustomerActor`, `yesterdaySHistoricalConsentEvidenceRemains`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-033 Consent Evidence, History & Withdrawal Management

**Decision:** 

### p26  · `listDataSubjectCustomer`

`GET /data-subject-customer` · MARKETING_VIEW · staff · **Data Subject / Customer Privacy Request Management**

> Provide a governed case-management workflow for customer privacy requests.

**`DataSubjectCustomerPrivacyRequestManagementView`** — `access`, `accountLogin`, `anonymization`, `api`, `atRisk`, `authorizedRepresentative`, `b2c`, `consentWithdrawal`, `correction`, `customer`, `customerPortal`, `customerService`, `dataCopyExport`, `daysRemaining`, `deletion`, `dueDate`, `emailManualEntry`, `emailVerification`, `guardian`, `idReviewWherePermitted`, `jurisdiction`, `manualVerification`, `marketingOptOut`, `mobileApp`, `mobileVerification`, `notes`, `objection`, `otherOrganizationDefinedPrivacyRequests`, `otp`, `owner`, `pos`, `priority`, `requestId`, `requestType`, `restriction`, `sla`, `source`, `status`, `submittedAt`, `verificationStatus`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-750 Data Subject Requests
- serves P13 CMS-034 Data Subject / Customer Privacy Request Management

**Decision:** 

### p28  · `setDataDiscoveryAccess`

`PUT /data-discovery-access` · MARKETING_MANAGE · staff · **Data Discovery, Access, Export & Correction Workspace**

> Allow authorized privacy teams to locate customer data across TICVAI and connected systems when fulfilling access, export or correction requests.

**`DataDiscoveryAccessExportCorrectionWorkspaceView`** — `connectedApplications`, `consent17Records`, `consentRecords`, `credentialReferences`, `crm`, `crm14Records`, `customerProfile`, `encryptionSecurity`, `eventRegistrations`, `exclusions`, `expiry`, `format`, `includedCategories`, `includedSystems`, `language`, `loyalty`, `marketing`, `membership`, `membership1Record`, `orders`, `orders26Records`, `paymentsReferences`, `resourceBookings`, `sensitiveFieldHandling`, `ticketing82Records`, `tickets`, `waiverRecords`, `wallet`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-750 Data Subject Requests
- serves P13 CMS-035 Data Discovery, Access, Export & Correction Workspace

**Decision:** 

### p29  · `listDeletionAnonymizationRestriction`

`GET /deletion-anonymization-restriction` · MARKETING_VIEW · staff · **Deletion, Anonymization & Restriction Operations**

> Govern privacy requests or policies requiring personal data to be deleted, anonymized or restricted. This screen requires strong controls because deletion may affect financial, ticketing, fraud, legal and operational records.

**`DeletionAnonymizationRestrictionOperationsView`** — `activeTransactions`, `anonymize`, `biometricReferenceDelete`, `completed`, `configuredJurisdictionRules`, `contractualObligations`, `disconnectThirdPartyProfile`, `failed`, `financialRecords`, `fraudInvestigationHold`, `legalHolds`, `manualActionRequired`, `marketingProfileDelete`, `otherConfiguredAction`, `pending`, `processing`, `pseudonymizeWhereConfigured`, `restrictProcessing`, `retainedWithReason`, `retentionRequirements`, `securityFraudRequirements`, `suppressMarketing`

- serves P13 CMS-036 Deletion, Anonymization & Restriction Operations

**Decision:** 

### p30  · `listDataRetentionExpiry`

`GET /data-retention-expiry` · MARKETING_VIEW · staff · **Data Retention, Expiry & Legal Hold Operations**

> Operationalize retention policies associated with Board 1 processing purposes and data categories.

**`DataRetentionExpiryLegalHoldOperationsView`** — `anonymize`, `approval`, `daily`, `eligibleForAnonymization`, `eligibleForDeletion`, `holdId`, `monthly`, `onConfiguredSchedules`, `owner`, `placeHold`, `processingFailures`, `reason`, `recordsApproachingExpiry`, `retentionExceptions`, `scope`, `start`, `status`, `underLegalHold`, `weekly`

- serves P13 CMS-037 Data Retention, Expiry & Legal Hold Operations

**Decision:** 

### p32  · `setPrivacyComplianceException`

`PUT /privacy-compliance-exception` · MARKETING_MANAGE · staff · **Privacy Compliance, Exception & Investigation Workspace**

> Provide a centralized workspace for privacy configuration and operational exceptions requiring investigation.

**`PrivacyComplianceExceptionInvestigationWorkspaceView`** — `attachmentsReferenceEvidence`, `brand`, `correctiveAction`, `country`, `customer`, `customerPrivacyProfile`, `dataOwner`, `detectedAt`, `exception`, `exceptionSummary`, `fullEnterpriseCybersecurityIncidentManagementPlatform`, `it`, `legal`, `marketing`, `notes`, `operations`, `owner`, `policyConfiguration`, `privacy`, `relatedEvidence`, `rootCause`, `security`, `severity`, `sla`, `status`, `system`, `systemEvents`, `timeline`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-038 Privacy Compliance, Exception & Investigation Workspace

**Decision:** 

### p33  · `listPrivacyEvidenceCompliance`

`GET /privacy-evidence-compliance` · MARKETING_VIEW · staff · **Privacy Audit, Evidence & Compliance Reporting**

> Provide immutable auditability and management/compliance reporting across privacy operations.

**`PrivacyAuditEvidenceComplianceReportingView`** — `action`, `actor`, `administrativeOverride`, `after`, `anonymizationExecuted`, `approval`, `before`, `biometricPrivacyReport`, `channel`, `configurationChange`, `consentGranted`, `consentStatusReport`, `consentWithdrawalReport`, `consentWithdrawn`, `cookieTrackingComplianceReport`, `correctionRequested`, `customer`, `dataExportGenerated`, `dateTime`, `deletionAnonymizationReport`, `deletionApproved`, `eventId`, `evidenceReference`, `exceptionReport`, `identityVerified`, `legalHold`, `marketingPermissionReport`, `minorGuardianPrivacyReport`, `policyAcceptanceReport`, `policyAccepted`, `preferenceChanged`, `privacyRequestCreated`, `privacyRequestSlaReport`, `reason`, `relatedCase`, `retentionAction`, `retentionReport`, `role`, `selected`, `source`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-753 Compliance Audit Dashboard
- serves P13 CMS-039 Privacy Audit, Evidence & Compliance Reporting
- serves P13 CMS-040 Privacy Analytics & AI Compliance Intelligence

**Decision:** 

### p35  · `listPrivacyCompliance`

`GET /privacy-compliance` · MARKETING_VIEW · staff · **Privacy Analytics & AI Compliance Intelligence**

> Provide executives, Privacy Officers and Compliance teams with actionable privacy analytics and AI-assisted risk detection. This should be the intelligence layer across both Privacy Boards.

**`PrivacyAnalyticsAiComplianceIntelligenceView`** — `averageResolutionTime`, `backendScreenCoreResponsibility`, `board1Configure`, `board2Operate`, `consentPropagationFailures`, `consentRate`, `consentStates`, `cookieAcceptanceByCategory`, `deletionCompletionRate`, `guardianConsentCompletion`, `marketingOptInRate`, `policyAcceptance`, `privacyExceptions`, `privacyRequests`, `retentionCompliance`, `showOverdueDeletionRequests`, `slaCompliance`, `withdrawalRate`

- serves P08 BO-744 Data Governance Center
- serves P13 CMS-040 Privacy Analytics & AI Compliance Intelligence

**Decision:** 


---

## Waiver, Consent & Digital Form Management

### p6   · `listWaiverConsent`

`GET /waiver-consent` · MARKETING_VIEW · staff · **Waiver & Consent Command Center**

> Provide administrators with a centralized workspace for managing every waiver, consent form and digital declaration configured across TICVAI.

**`WaiverConsentCommandCenterView`** — `activeWaiverVersions`, `archived`, `associatedProducts`, `customForm`, `draft`, `effectiveFrom`, `effectiveTo`, `expiring`, `language`, `lastModified`, `liabilityWaiver`, `mediaConsent`, `medicalDeclaration`, `membershipDeclaration`, `owner`, `parentGuardianConsent`, `participationConsent`, `pendingApproval`, `preview`, `productsRequiringWaiver`, `published`, `rentalAgreement`, `safetyAcknowledgement`, `scheduled`, `signatoryType`, `status`, `termsAcceptance`, `test`, `totalTemplates`, `type`, `version`, `waiverId`, `waiverName`, `waiversRequiringReview`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-041 Waiver & Consent Command Center

**Decision:** 

### p8   · `listWaiverTemplateMaster`

`GET /waiver-template-master` · MARKETING_VIEW · staff · **Waiver Template Library & Master Setup**

> Create the master definition of a waiver or consent form before individual content and questions are configured.

**`WaiverTemplateLibraryMasterSetupView`** — `applicableCountry`, `applicableJurisdiction`, `brand`, `businessOwner`, `complianceOwner`, `defaultLanguage`, `department`, `internalDescription`, `legalEntity`, `legalReviewer`, `operationalOwner`, `owner`, `status`, `useMasterTemplate`, `waiverId`, `waiverName`, `waiverType`

- serves P08 BO-846 Assignment Rules
- serves P13 CMS-042 Waiver Template Library & Master Setup

**Decision:** 

### p9   · `setDigitalWaiverForm`

`PUT /digital-waiver-form` · MARKETING_MANAGE · staff · **Digital Waiver & Form Builder**

> Provide a no-code visual builder for creating the actual customer-facing waiver or digital form.

**`DigitalWaiverFormBuilderView`** — `acknowledgement`, `b2c`, `boldEmphasis`, `checkbox`, `customerDetails`, `date`, `desktop`, `divider`, `guardianDetails`, `heading`, `headings`, `hyperlinks`, `imageLogo`, `informationBox`, `initials`, `instructions`, `kioskOnSite`, `legalText`, `lists`, `mandatoryNotices`, `mobile`, `paragraph`, `paragraphs`, `question`, `sectionNumbering`, `signature`, `tablet`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-846 Assignment Rules
- serves P13 CMS-043 Digital Waiver & Form Builder

**Decision:** 

### p11  · `listDynamicFieldQuestion`

`GET /dynamic-field-question` · MARKETING_VIEW · staff · **Dynamic Fields, Questions & Conditional Logic**

> Configure the information that must be collected from the participant or signatory.

**`DynamicFieldsQuestionsConditionalLogicView`** — `address`, `allowedValues`, `autoPopulated`, `bookingReference`, `characterLimit`, `checkbox`, `conditional`, `customerId`, `customerLookup`, `date`, `dateOfBirth`, `dateRange`, `dropdown`, `duplicatingData`, `email`, `emergencyContact`, `format`, `guardianName`, `initials`, `longText`, `minimumMaximum`, `mobile`, `multiSelect`, `number`, `optional`, `participantLookup`, `participantName`, `readOnly`, `relationship`, `required`, `shortText`, `signature`, `singleSelect`, `ticketNumber`, `yesNo`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-044 Dynamic Fields, Questions & Conditional Logic

**Decision:** 

### p13  · `setSignatorySignatureGuardian`

`PUT /signatory-signature-guardian` · MARKETING_MANAGE · staff · **Signatory, Signature & Guardian Rule Configuration**

> Define who is legally or operationally required to complete and sign the waiver.

**`SignatorySignatureGuardianRuleConfigurationView`** — `authenticationMethod`, `checkboxAcceptance`, `consentEvidence`, `corporateRepresentative`, `customerAuthorizedRepresentative`, `dateTime`, `digitalSignature`, `eachParticipantSignsIndividually`, `groupLeader`, `guardianSignsForEachMinor`, `identityVerificationWhereRequired`, `initialsRequired`, `legalGuardian`, `member`, `organizationSLegalComplianceApproval`, `otherAuthorizedSignatory`, `parent`, `participant`, `participantGuardian`, `purchaser`, `relationship`, `relevantTransactionCustomerReference`, `rentalCustomer`, `signatory`, `signatoryName`, `signatureRequired`, `ticketHolder`, `timestamp`, `typedAcceptance`, `waiverVersion`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-849 Guardian & Group Signing
- serves P13 CMS-045 Signatory, Signature & Guardian Rule Configuration

**Decision:** 

### p14  · `listProductEventExperience`

`GET /product-event-experience` · MARKETING_VIEW · staff · **Product, Event & Experience Association**

> Determine which TICVAI products or activities require each waiver.

**`ProductEventExperienceAssociationView`** — `activity`, `activityLiabilityWaiver`, `addOn`, `attraction`, `automaticallyInheritedByApplicableActivities`, `camp`, `conditional`, `event`, `events`, `futureBookings`, `informational`, `mandatory`, `membership`, `optional`, `package`, `parentGuardianConsent`, `participants`, `performance`, `product`, `products`, `rental`, `resource`, `safetyAcknowledgement`, `ticketType`, `tickets`, `venue`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-046 Product, Event & Experience Association

**Decision:** 

### p16  · `listWaiverTriggerEligibility`

`GET /waiver-trigger-eligibility` · MARKETING_VIEW · staff · **Waiver Trigger, Eligibility & Completion Rules**

> Define when a waiver is required, when it must be completed and what happens if it is not completed.

**`WaiverTriggerEligibilityCompletionRulesView`** — `activity`, `afterPurchase`, `age`, `beforeAccess`, `beforeActivityStart`, `beforeArrival`, `beforeCheckIn`, `beforeEquipmentCollection`, `beforeEvent`, `beforeMembershipActivation`, `beforeTicketDownload`, `beforeTicketIssuance`, `beforeTicketRelease`, `blocksAccess`, `blocksCheckIn`, `blocksTicketActivation`, `blocksTicketDownload`, `bookingType`, `channel`, `country`, `customerType`, `duringCheckout`, `event`, `immediately`, `membership`, `participantType`, `product`, `requiresStaffOverride`, `t24Hours`, `t3Days`, `t7Days`, `venue`, `warnsOnly`, `xDaysBeforeVisit`, `xHoursBeforeEvent`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-847 Version, Expiry & Renewal
- serves P13 CMS-047 Waiver Trigger, Eligibility & Completion Rules

**Decision:** 

### p18  · `listVersioningEffectiveDate`

`GET /versioning-effective-date` · MARKETING_VIEW · staff · **Versioning, Effective Dates & Legal Change Control**

> Ensure TICVAI maintains a complete historical record of exactly which waiver wording each participant accepted.

**`VersioningEffectiveDatesLegalChangeControlView`** — `addedText`, `approval`, `changeReason`, `changedAssociations`, `changedQuestions`, `changedSignatoryRules`, `createdBy`, `createdDate`, `effectiveFrom`, `effectiveTo`, `legalReviewer`, `previousVersionNewVersion`, `removedText`, `v10`, `v11`, `v20`, `versionNumber`

- serves P08 BO-748 Consent Capture & Versions
- serves P08 BO-848 Signature Experience Setup
- serves P09 ADM-328 Workflow Versioning & Change History

**Decision:** 

### p19  · `setLocalizationBrandingCustomer`

`PUT /localization-branding-customer` · MARKETING_MANAGE · staff · **Localization, Branding & Customer Experience Configuration**

> Configure how the waiver appears across different brands, languages and customer channels.

**`LocalizationBrandingCustomerExperienceConfigurationView`** — `additionalLanguagesAsConfigured`, `appropriateContrast`, `approvalStatus`, `arabic`, `b2cWeb`, `brandLogo`, `clearValidationMessages`, `confirmationMessage`, `customerInstructions`, `emailLink`, `english`, `footer`, `groupPortal`, `header`, `keyboardNavigation`, `kiosk`, `lastUpdated`, `mobileApp`, `posFrontDesk`, `qrLink`, `responsiveLayouts`, `screenReaderCompatibleLabels`, `sourceLanguage`, `supportContact`, `translatedContent`, `translationStatus`, `translatorReviewer`, `typography`, `venueLogo`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-678 Channel, Language & Branding Configuration
- serves P08 BO-793 AI Content, Translation & Audit
- serves P08 BO-841 Personalization & Localization

**Decision:** 

### p21  · `approveWaiverTesting`

`PUT /waiver-testing` · MARKETING_MANAGE · staff · **Waiver Approval, Testing & Publication Workspace**

> Provide the final governance gate before a waiver becomes operational.

**`WaiverApprovalTestingPublicationWorkspaceView`** — `activityWaiver`, `adultDeclaration`, `ai`, `approvedBy`, `comments`, `completionRulesConfigured`, `conditionalRulesValid`, `configuration`, `controlledRollout`, `dates`, `effectiveDatesValid`, `enforced`, `guardianConsent`, `guardianSignature`, `insideTicketingOrTicketMedia`, `multipleInconsistentWaiverImplementations`, `productsEventsAssigned`, `publishedBy`, `requiredFieldsConfigured`, `requiredLegalTextPresent`, `requiredTranslationsApproved`, `reviewedBy`, `signatureRulesConfigured`, `submittedBy`, `version`

- serves P13 CMS-050 Waiver Approval, Testing & Publication Workspace

**Decision:** 

### p26  · `listWaiver`

`GET /waiver` · MARKETING_VIEW · staff · **Waiver Operations Command Center**

> Provide Operations, Customer Service, Compliance and venue teams with a real-time overview of waiver completion across upcoming and active activities.

**`WaiverOperationsCommandCenterView`** — `accessBlocked`, `activity`, `booking`, `completed`, `completion`, `completionRate`, `dateTime`, `event`, `eventActivity`, `exceptions`, `expiring`, `group`, `guardianConsentPending`, `guardianPending`, `invalid`, `manualExceptions`, `missing`, `operationalRisk`, `partiallyCompleted`, `participants`, `pending`, `product`, `rejected`, `sEG`, `thisWeek`, `today`, `tomorrow`, `upcomingParticipantsMissingWaiver`, `venue`, `waiverType`, `waiversRequired`, `youthAttentio`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-844 Waiver Command Center
- serves P08 BO-845 Waiver Template Builder
- serves P13 CMS-051 Waiver Operations Command Center

**Decision:** 

### p28  · `listParticipantWaiverStatus`

`GET /participant-waiver-statu` · MARKETING_VIEW · staff · **Participant Waiver Status & Tracking**

> Provide a detailed operational record of the waiver requirements for each participant.

**`ParticipantWaiverStatusTrackingView`** — `ageCategory`, `booking`, `completionStatus`, `customerPurchaser`, `event`, `group`, `participant`, `participantId`, `product`, `recordException`, `requestCorrection`, `ticket`, `visitDate`, `waiverRequirements`

- serves P08 BO-851 Verification & Access Control
- serves P13 CMS-052 Participant Waiver Status & Tracking

**Decision:** 

### p29  · `listDigitalSigningCollection`

`GET /digital-signing-collection` · MARKETING_VIEW · staff · **Digital Signing & Collection Operations**

> Manage the actual distribution and completion of digital waivers. 29 | Pag e

**`DigitalSigningCollectionOperationsView`** — `activityWaiverV32`, `authentication`, `b2cAccount`, `booking`, `completed`, `delivered`, `emailLink`, `expiredLinks`, `failed`, `groupPortal`, `kiosk`, `mobileApp`, `opened`, `participant`, `participantOmarAhmed`, `pos`, `qrCode`, `sent`, `singleMultiUse`, `smsLink`, `staffAssistedDevice`, `started`, `waiverVersion`, `whatsappWhereIntegrated`

- serves P13 CMS-053 Digital Signing & Collection Operations

**Decision:** 

### p31  · `listMinorGuardianGroup`

`GET /minor-guardian-group` · MARKETING_VIEW · staff · **Minor, Guardian & Group Consent Management**

> Manage complex consent relationships for minors and organized groups. This screen is particularly important for camps, academies, schools, family attractions and youth activities.

**`MinorGuardianGroupConsentManagementView`** — `consentStatus`, `contact`, `groupBooking`, `groupLeader`, `guardian`, `minor`, `oneGuardianMultipleMinors`, `oneGuardianOneMinor`, `organization`, `permittedActions`, `relationship`, `responsibility`, `signatureStatus`, `verificationStatus`

- serves P08 BO-850 Pre-Arrival Completion
- serves P13 CMS-054 Minor, Guardian & Group Consent Management

**Decision:** 

### p33  · `setWaiverVerificationValidation`

`PUT /waiver-verification-validation` · MARKETING_MANAGE · staff · **Waiver Verification & Validation Workspace**

> Provide authorized staff with a controlled process for reviewing waiver submissions that require verification.

**`WaiverVerificationValidationWorkspaceView`** — `booking`, `bookingMatch`, `correctWaiverVersion`, `effectiveDateValid`, `guardianRelationshipPresent`, `participant`, `participantMatch`, `requestCorrection`, `requiredAcknowledgementsAccepted`, `requiredEvidencePresent`, `requiredFieldsComplete`, `requiredQuestionsAnswered`, `risk`, `signatory`, `signaturePresent`, `status`, `submissionId`, `submitted`, `verificationReason`, `version`, `waiver`

- serves P08 BO-852 Documents, Search & Retention
- serves P13 CMS-055 Waiver Verification & Validation Workspace

**Decision:** 

### p34  · `listMissingExpiredInvalid`

`GET /missing-expired-invalid` · MARKETING_VIEW · staff · **Missing, Expired & Invalid Waiver Management**

> Provide a dedicated exception workspace for waiver requirements preventing operational readiness.

**`MissingExpiredInvalidWaiverManagementView`** — `accessBlocking`, `accessImpact`, `booking`, `contactCustomer`, `contactGuardian`, `event`, `eventProximity`, `expired`, `groupSize`, `guardianMissing`, `incomplete`, `mandatoryWaiver`, `minorGuardianIssue`, `missingSignature`, `missingWaiver`, `operationalImpact`, `owner`, `participant`, `participantMismatch`, `problem`, `rejected`, `requestReSign`, `requestVerification`, `requiredCorrection`, `startExceptionWorkflow`, `status`, `timeRemaining`, `verificationFailed`, `visitTime`, `waiver`, `wrongVersion`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P13 CMS-056 Missing, Expired & Invalid Waiver Management

**Decision:** 

### p36  · `listSiteWaiverException`

`GET /site-waiver-exception` · MARKETING_VIEW · staff · **On-Site Waiver & Exception Handling**

> Support customers who arrive at the venue without completing required waivers.

**`OnSiteWaiverExceptionHandlingView`** — `accessControlReceivesUpdatedEligibility`, `activitySpecific`, `booking`, `completeOnKiosk`, `completeOnStaffTablet`, `contactGuardian`, `customer`, `displayQrForCustomer`, `group`, `membership`, `oneTime`, `participant`, `qr`, `reSignUpdatedWaiver`, `requestSupervisorException`, `signatureEvidenceExists`, `ticket`, `ticketSpecific`, `timeLimited`, `waiverStatusVerified`

- serves P13 CMS-057 On-Site Waiver & Exception Handling

**Decision:** 

### p38  · `listComplianceEvidenceWaiver`

`GET /compliance-evidence-waiver` · MARKETING_VIEW · staff · **Compliance Evidence, Audit & Waiver Repository**

> Maintain the complete evidentiary record of every waiver and consent transaction.

**`ComplianceEvidenceAuditWaiverRepositoryView`** — `acknowledgements`, `applicableEvent`, `applicableProduct`, `auditEvents`, `businessUnit`, `dataSensitivity`, `exactVersion`, `legalEntity`, `legalWording`, `questions`, `relatedBooking`, `relatedTicket`, `requirements`, `responses`, `role`, `signatoryEvidence`, `signatoryType`, `signatureEvidence`, `submissionDate`, `submissionTime`, `verification`, `waiverId`, `waiverVersion`

- serves P08 BO-853 Legal Evidence & Audit
- serves P13 CMS-058 Compliance Evidence, Audit & Waiver Repository

**Decision:** 

### p39  · `listWaiverComplianceOperational`

`GET /waiver-compliance-operational` · MARKETING_VIEW · staff · **Waiver Analytics, Compliance & Operational Insights**

> Analyze waiver completion, customer behavior and operational effectiveness.

**`WaiverAnalyticsComplianceOperationalInsightsView`** — `accessBlocks`, `averageCompletionTime`, `checkInDelays`, `completionRate`, `exceptionRate`, `exceptions`, `guardianCompletionRate`, `onSiteCompletion`, `onSiteCompletions`, `preArrivalCompletion`, `rejectionRate`, `reminderEffectiveness`, `staffInterventions`, `waiversAssigned`

- serves P13 CMS-059 Waiver Analytics, Compliance & Operational Insights

**Decision:** 

### p41  · `listWaiverComplianceRisk`

`GET /waiver-compliance-risk` · MARKETING_VIEW · staff · **AI Waiver Compliance & Risk Intelligence Center**

> Provide an AI intelligence layer across the complete waiver lifecycle. This should combine Board 1 configuration data + Board 2 operational data.

**`AiWaiverComplianceRiskIntelligenceCenterView`** — `aWaiverIssue`, `accessBlocks`, `area11CompleteStructure`, `completion`, `customerInteractions`, `exceptions`, `missing`, `nextWeek`, `operationalTrends`, `participants`, `productAssociations`, `questions`, `relationships`, `requirements`, `signatoryRules`, `templates`, `verification`, `versions`

- serves P13 CMS-060 AI Waiver Compliance & Risk Intelligence Center

**Decision:** 

