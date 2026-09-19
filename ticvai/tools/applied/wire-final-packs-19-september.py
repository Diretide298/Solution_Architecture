#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire the last non-AI packs: Licensing, Accreditation, Event Management and the rest.

The closing run of the contract pass. Four bodies of work and a tail:

    Licensing 98    `subscription` had 112 operations and six of ten boards were already
                    covered. Fifteen were missing, and they are the commercial engine:
                    the VSI model that scores a prospect into a tier, the billable unit,
                    the module dependency graph, go-live validation and licence
                    enforcement.
    Accreditation 74  A new contract. Accreditation is the opposite of ticketing — applied
                    for rather than bought, vetted rather than paid for, and granting a set
                    of places and times that differs for every holder.
    Event Mgmt 33   A `catalogue` extension. Event types, schedules that overrun, spaces,
                    capacity profiles, registration, resource plans, lifecycle, session
                    templates and prepaid minutes.
    Resources 20    Boards 3 and 4 were always `workforce`, which had 14 operations and no
                    shift template, no minimum cover, no coverage gap, no leave, no labour
                    cost and no compliance check. Ten added.

**The tail is the interesting part.** Thirty-odd screens across six packs that earlier
runs left behind, and almost every one of them belongs to a contract other than its
pack's: the gaming wallet screens go to `wallet` under the 19 September supersession,
the rental analytics go to `reporting`, the resource AI boards go to `ai`.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

FILES = ('screens/P08-venue-back-office.yaml', 'screens/P09-platform-admin-console.yaml')

S, X, C, W, R, A, G, M, F, I, T, P, Q = ('subscription', 'accreditation', 'catalogue',
                                         'workforce', 'reporting', 'approvals', 'games',
                                         'marketing-crm', 'finance', 'identity',
                                         'tenancy', 'promotions', 'wallet')

# board -> (first id number, [ops per screen]) for the sequential packs
LICENSING = {
    'ADM-369': [('listTenants', S, 'The commercial portfolio', 'onLoad'),
                ('getSubscription', S, 'One customer', 'onAction')],
    'ADM-370': [('listTenants', S, 'Subscriptions by tier', 'onLoad')],
    'ADM-371': [('getSubscription', S, 'Commercial 360', 'onLoad'),
                ('getEntitlementUsage', S, 'What they consume', 'onLoad')],
    'ADM-372': [('scoreVsiAssessment', S, 'Their VSI and model', 'onAction')],
    'ADM-373': [('getBillingReconciliation', S, 'Revenue against metering', 'onLoad')],
    'ADM-374': [('setTrialConfiguration', S, 'Trial rules', 'onAction'),
                ('listTenants', S, 'Trials running', 'onLoad')],
    'ADM-376': [('listRenewalAuto', S, 'Renewals due', 'onLoad')],
    'ADM-377': [('simulateCommercialPackage', S, 'Expansion options', 'onAction')],
    'ADM-378': [('getLicenceEnforcement', S, 'Exceptions and overage', 'onLoad')],

    'ADM-379': [('scoreVsiAssessment', S, 'Begin the assessment', 'onAction')],
    'ADM-380': [('submitOnboardingApplication', S, 'Register the organisation', 'onAction')],
    'ADM-381': [('scoreVsiAssessment', S, 'Venue type and business profile', 'onAction')],
    'ADM-382': [('scoreVsiAssessment', S, 'Visitors, capacity and scale', 'onAction')],
    'ADM-384': [('scoreVsiAssessment', S, 'Ticketing and product needs', 'onAction')],
    'ADM-385': [('scoreVsiAssessment', S, 'Access, queue and experience', 'onAction')],
    'ADM-386': [('listModuleCatalogue', S, 'Additional modules', 'onLoad'),
                ('scoreVsiAssessment', S, 'Record the answers', 'onAction')],
    'ADM-387': [('scoreVsiAssessment', S, 'Integration and technical needs', 'onAction')],
    'ADM-388': [('scoreVsiAssessment', S, 'Score and recommend', 'onAction')],

    'ADM-389': [('listLicensingModels', S, 'The rules engine', 'onLoad')],
    'ADM-390': [('getVsiModel', S, 'The VSI model', 'onLoad'),
                ('setVsiModel', S, 'Build it', 'onAction')],
    'ADM-391': [('setVsiModel', S, 'Scoring and tier thresholds', 'onAction')],
    'ADM-392': [('createPlan', S, 'Tier configuration', 'onAction'),
                ('listPlans', S, 'Tiers defined', 'onLoad')],
    'ADM-393': [('setLicensingModel', S, 'Tier allowances', 'onAction')],
    'ADM-394': [('setLicensingModel', S, 'Commercial and licensing model', 'onAction')],
    'ADM-395': [('setLicensingModel', S, 'Billable unit and minimum guarantee', 'onAction')],
    'ADM-396': [('setLicensingModel', S, 'Overage pricing', 'onAction'),
                ('addCapacityPack', S, 'Capacity packs', 'onAction')],
    'ADM-397': [('simulateCommercialPackage', S, 'Simulate the model', 'onAction')],
    'ADM-398': [('createPlanVersion', S, 'Publish a version', 'onAction')],

    'ADM-399': [('simulateCommercialPackage', S, 'The recommended package', 'onLoad')],
    'ADM-400': [('listPlans', S, 'Tiers to choose from', 'onLoad'),
                ('simulateCommercialPackage', S, 'Price the choice', 'onAction')],
    'ADM-401': [('listModuleCatalogue', S, 'The marketplace', 'onLoad')],
    'ADM-402': [('listModuleCatalogue', S, 'Recommended modules', 'onLoad')],
    'ADM-403': [('listModuleCatalogue', S, 'One module in detail', 'onLoad')],
    'ADM-404': [('setModuleListing', S, 'Dependencies and compatibility', 'onAction'),
                ('listModuleCatalogue', S, 'What depends on what', 'onLoad')],
    'ADM-405': [('addCapacityPack', S, 'Add-ons and capacity', 'onAction')],
    'ADM-406': [('simulateCommercialPackage', S, 'Simulate the package', 'onAction')],
    'ADM-407': [('simulateCommercialPackage', S, 'Review the summary', 'onLoad')],
    'ADM-408': [('createPartnerQuote', S, 'Confirm the package', 'onAction')],

    'ADM-409': [('setTrialConfiguration', S, 'Purchase or trial', 'onAction')],
    'ADM-410': [('setSubscription', S, 'Contract and billing cycle', 'onAction')],
    'ADM-411': [('createLegalEntity', F, 'Billing and legal entity', 'onAction')],
    'ADM-412': [('setPaymentProvider', 'orders', 'Payment and settlement setup', 'onAction')],
    'ADM-413': [('setTrialConfiguration', S, 'Trial and conversion rules', 'onAction')],
    'ADM-414': [('previewSubscriptionChange', S, 'Order and pricing review', 'onLoad')],
    'ADM-415': [('setAgreementContractTerm', S, 'Agreement and acceptance', 'onAction')],
    'ADM-416': [('simulateCommercialPackage', S, 'Validate before committing', 'onAction')],
    'ADM-417': [('setSubscription', S, 'Create the subscription', 'onAction')],
    'ADM-418': [('getSubscription', S, 'Confirmation', 'onLoad')],

    'BO-594': [('listTenants', S, 'Provisioning in flight', 'onLoad')],
    'ADM-419': [('createTenant', S, 'Provision the tenant', 'onAction')],
    'ADM-420': [('createOrgUnit', T, 'Venue and operational structure', 'onAction')],
    'ADM-421': [('createPrincipal', I, 'The first administrator', 'onAction'),
                ('setPasswordPolicy', I, 'Security initialisation', 'onAction')],
    'ADM-422': [('getTenantLicences', S, 'Licence and entitlement activation', 'onLoad'),
                ('addLicenceAddOn', S, 'Activate an add-on', 'onAction')],
    'ADM-423': [('listModuleCatalogue', S, 'Module activation and dependencies', 'onLoad')],
    'ADM-424': [('listVenueTypeTemplates', S, 'Apply a venue template', 'onAction')],
    'ADM-425': [('updateRegionSettings', T, 'Regional defaults', 'onAction')],
    'ADM-426': [('runGoLiveValidation', S, 'Validate the provisioning', 'onAction')],
    'ADM-427': [('getGoLiveReadiness', S, 'Provisioning outcome', 'onLoad')],

    'BO-595': [('getGoLiveReadiness', S, 'Setup progress', 'onLoad')],
    'BO-596': [('getGoLiveReadiness', S, 'The guided plan', 'onLoad')],
    'BO-597': [('generateConfiguration', 'ai', 'Draft the configuration', 'onAction')],
    'BO-598': [('generateConfiguration', 'ai', 'Review and accept a draft', 'onAction')],
    'BO-599': [('getTenantConfig', 'white-label', 'Manual configuration', 'onLoad')],
    'BO-600': [('setVenueSettings', T, 'Venue and calendar setup', 'onAction')],
    'BO-601': [('setPrices', C, 'Product and pricing setup', 'onAction'),
               ('setChannelListing', S, 'Sales channels', 'onAction')],
    'BO-602': [('configureWorkstation', T, 'POS, payment and access setup', 'onAction')],
    'BO-603': [('runGoLiveValidation', S, 'Configuration health', 'onAction')],
    'BO-604': [('getGoLiveReadiness', S, 'Handoff to go-live', 'onLoad')],

    'BO-605': [('getGoLiveReadiness', S, 'Readiness at a glance', 'onLoad')],
    'BO-606': [('runGoLiveValidation', S, 'Run the plan', 'onAction')],
    'BO-607': [('runGoLiveValidation', S, 'Ticketing and product checks', 'onAction')],
    'BO-608': [('runGoLiveValidation', S, 'Sales channel tests', 'onAction')],
    'BO-609': [('runGoLiveValidation', S, 'Payment and financial checks', 'onAction')],
    'BO-610': [('runGoLiveValidation', S, 'Ticket, QR and access checks', 'onAction')],
    'BO-611': [('runGoLiveValidation', S, 'User, security and integration checks', 'onAction')],
    'BO-612': [('runGoLiveValidation', S, 'Communication and journey checks', 'onAction')],
    'BO-613': [('getGoLiveReadiness', S, 'Blockers and warnings', 'onLoad')],
    'BO-614': [('getGoLiveReadiness', S, 'Final sign-off', 'onAction')],

    'ADM-449': [('getEntitlementUsage', S, 'Usage against licence', 'onLoad')],
    'ADM-450': [('getTenantLicences', S, 'Entitlement inventory', 'onLoad')],
    'ADM-451': [('getUsageMetering', S, 'Billable event metering', 'onLoad')],
    'ADM-452': [('getLicenceEnforcement', S, 'Thresholds and position', 'onLoad')],
    'ADM-453': [('setLicenceEnforcementPolicy', S, 'What happens at each threshold',
                 'onAction')],
    'ADM-454': [('getLicenceEnforcement', S, 'Minimum guarantee and variable consumption',
                 'onLoad')],
    'ADM-455': [('addCapacityPack', S, 'Overage and temporary exceptions', 'onAction')],
    'ADM-456': [('getBillingReconciliation', S, 'Alerts and reconciliation', 'onLoad')],
    'ADM-457': [('getEntitlementUsage', S, 'Consumption trend', 'onLoad')],
    'ADM-458': [('getUsageMetering', S, 'Metering audit', 'onLoad')],

    'ADM-459': [('listSubscriptionInvoices', S, 'Billing at a glance', 'onLoad')],
    'ADM-460': [('generateInvoice', S, 'Calculate the charge', 'onAction')],
    'ADM-461': [('getBillingReconciliation', S, 'Consumption against invoice', 'onLoad')],
    'ADM-462': [('recordInvoicePayment', S, 'Invoice and payment', 'onAction'),
                ('listSubscriptionInvoices', S, 'Invoices raised', 'onLoad')],
    'ADM-463': [('previewSubscriptionChange', S, 'Model a change', 'onAction'),
                ('setSubscription', S, 'Apply it', 'onAction')],
    'ADM-464': [('listRenewalAuto', S, 'Renewals', 'onLoad'),
                ('setRenewalAutoMembership', S, 'Set auto-renewal', 'onAction')],
    'ADM-465': [('simulateCommercialPackage', S, 'Right-sizing options', 'onAction')],
    'ADM-466': [('simulateCommercialPackage', S, 'Scenario simulation', 'onAction')],
    'ADM-467': [('cancelInvoice', S, 'Credit or cancel', 'onAction'),
                ('disputeInvoice', S, 'Raise a dispute', 'onAction')],
    'ADM-468': [('getBillingReconciliation', S, 'Billing audit', 'onLoad')],
}

ACCREDITATION = {
    'BO-615': [('listAccreditationApplications', X, 'Applications in flight', 'onLoad'),
               ('listAccreditationHolders', X, 'Holders by status', 'onLoad')],
    'BO-616': [('listAccreditationApplications', X, 'The directory', 'onLoad')],
    'BO-617': [('createAccreditationApplication', X, 'Start an application', 'onAction')],
    'BO-618': [('createForm', M, 'Build the application form', 'onAction')],
    'BO-619': [('listAccreditationProgrammes', X, 'Categories within a programme', 'onLoad')],
    'BO-620': [('createAccreditationProgramme', X, 'Set up a programme', 'onAction')],
    'BO-621': [('setAccreditationRequirements', X, 'Applicant types', 'onAction')],
    'BO-622': [('setAccreditationRequirements', X, 'The requirements matrix', 'onAction')],
    'BO-623': [('listAccreditationApplications', X, 'Intake monitor', 'onLoad')],
    'BO-624': [('createAccreditationProgramme', X, 'Publish the rules', 'onAction')],

    'BO-625': [('listAccreditationHolders', X, 'The holder directory', 'onLoad')],
    'BO-626': [('getAccreditationHolder', X, 'One holder', 'onLoad')],
    'BO-627': [('updateAccreditationHolder', X, 'Identity and verification', 'onAction')],
    'BO-628': [('updateAccreditationHolder', X, 'Photo management', 'onAction')],
    'BO-629': [('submitAccreditationDocument', X, 'The document repository', 'onLoad')],
    'BO-630': [('verifyAccreditationDocument', X, 'Verify a document', 'onAction')],
    'BO-631': [('listAccreditationIdentityConflicts', X, 'Possible duplicates', 'onLoad')],
    'BO-632': [('updateAccreditationHolder', X, 'Organisation and affiliation', 'onAction')],
    'BO-633': [('getAccreditationHolder', X, 'Completeness and compliance', 'onLoad')],
    'BO-634': [('listAccreditationAudit', X, 'Profile history', 'onLoad')],

    'BO-635': [('listAccreditationApplications', X, 'The review queue', 'onLoad')],
    'BO-636': [('decideAccreditationApplication', X, 'Decide', 'onAction'),
               ('listAccreditationApplications', X, 'The application', 'onLoad')],
    'BO-638': [('setVisualWorkflow', A, 'Approval rules and conditions', 'onAction')],
    'BO-639': [('setApprovalMatrix', A, 'Reviewer assignment', 'onAction')],
    'BO-640': [('decideAccreditationApplication', X, 'Reject or return', 'onAction')],
    'BO-641': [('escalateApprovalRequest', A, 'Escalate an exception', 'onAction')],
    'BO-643': [('listAccreditationAudit', X, 'Decision history', 'onLoad')],

    'BO-645': [('listAccreditationCredentials', X, 'Credentials issued', 'onLoad')],
    'BO-646': [('issueAccreditationCredential', X, 'Generate a credential', 'onAction')],
    'BO-647': [('setBadgeTemplate', X, 'Credential media', 'onAction')],
    'BO-648': [('listBadgeTemplates', X, 'Badge designs', 'onLoad'),
               ('setBadgeTemplate', X, 'Design one', 'onAction')],
    'BO-649': [('createBadgePrintJob', X, 'Queue for printing', 'onAction'),
               ('listBadgePrintJobs', X, 'The print queue', 'onLoad')],
    'BO-650': [('issueAccreditationCredential', X, 'Digital and mobile credentials', 'onAction')],
    'BO-651': [('issueAccreditationCredential', X, 'NFC and RFID encoding', 'onAction')],

    'BO-654': [('listAccessProfiles', X, 'Access at a glance', 'onLoad')],
    'BO-655': [('listAccessProfiles', X, 'Profiles', 'onLoad'),
               ('setAccessProfile', X, 'Define one', 'onAction')],
    'BO-656': [('setAccessProfile', X, 'Venue and zone matrix', 'onAction')],
    'BO-657': [('setAccessProfile', X, 'Operational area permissions', 'onAction')],
    'BO-658': [('setAccessProfile', X, 'Date and time rules', 'onAction')],
    'BO-659': [('setAccessProfile', X, 'Schedule by event phase', 'onAction')],
    'BO-660': [('setHolderAccess', X, 'Assign profiles to a holder', 'onAction')],
    'BO-661': [('setHolderAccess', X, 'Temporary access and exceptions', 'onAction')],
    'BO-662': [('setAccreditationStatus', X, 'Revoke or suspend', 'onAction')],
    'BO-663': [('previewAccessImpact', X, 'Who this change would affect', 'onAction')],

    'BO-664': [('listAccreditationHolders', X, 'Lifecycle at a glance', 'onLoad')],
    'BO-665': [('setAccreditationStatus', X, 'Move through the workflow', 'onAction')],
    'BO-666': [('setAccreditationValidity', X, 'Validity periods', 'onAction')],
    'BO-667': [('createAccreditationProgramme', X, 'Event and venue assignment', 'onAction')],
    'BO-668': [('setAccessProfile', X, 'Multi-venue accreditation', 'onAction')],
    'BO-669': [('setAccreditationValidity', X, 'Temporary and seasonal', 'onAction')],
    'BO-670': [('setAccreditationStatus', X, 'Suspend and reactivate', 'onAction')],
    'BO-671': [('setAccreditationStatus', X, 'Revoke', 'onAction')],
    'BO-672': [('listAccreditationHolders', X, 'Expiring soon', 'onLoad')],
    'BO-673': [('setAccreditationValidity', X, 'Expiry and renewal rules', 'onAction')],

    'BO-674': [('setAccreditationNotificationRules', X, 'Notifications at a glance', 'onLoad')],
    'BO-675': [('setAccreditationNotificationRules', X, 'Notification rules', 'onAction')],
    'BO-676': [('setAccreditationNotificationRules', X, 'Expiry and renewal scheduling',
                'onAction')],
    'BO-677': [('listMessageTemplates', M, 'Template library', 'onLoad')],
    'BO-678': [('setLocalizationBrandingCustomer', M, 'Channel, language and branding',
                'onAction')],
    'BO-679': [('sendTransactionalMessage', M, 'Bulk communication', 'onAction')],
    'BO-680': [('importAccreditationHolders', X, 'Bulk import a roster', 'onAction')],
    'BO-681': [('importAccreditationHolders', X, 'Validation and processing', 'onLoad')],
    'BO-682': [('listAccreditationHolders', X, 'Export', 'onLoad')],
    'BO-683': [('listAccreditationAudit', X, 'Import and export audit', 'onLoad')],

    'BO-684': [('listAccreditationHolders', X, 'The executive view', 'onLoad')],
    'BO-685': [('listAccreditationHolders', X, 'Status and portfolio', 'onLoad')],
    'BO-686': [('listAccreditationAccessActivity', X, 'Utilisation', 'onLoad')],
    'BO-687': [('listAccreditationAccessActivity', X, 'Access activity', 'onLoad')],
    'BO-688': [('getKpiValues', R, 'Trend and comparison', 'onLoad')],
    'BO-689': [('listAccreditationAudit', X, 'Audit reporting', 'onLoad')],
    'BO-690': [('listAccreditationAudit', X, 'The immutable log', 'onLoad')],
    'BO-691': [('listApiClients', 'public-api', 'API management', 'onLoad')],
    'BO-692': [('listWebhookSubscriptions', 'public-api', 'Webhooks', 'onLoad')],
    'BO-693': [('listAccreditationAudit', X, 'Integration audit', 'onLoad')],
}

EVENTS = {
    'BO-694': [('listEvents', C, 'The event catalogue', 'onLoad')],
    'BO-695': [('listEventTypes', C, 'Event types', 'onLoad'),
               ('setEventType', C, 'Define behaviour', 'onAction')],
    'BO-696': [('cloneEvent', C, 'Clone, choosing what comes with it', 'onAction')],
    'BO-697': [('setEventSchedule', C, 'The schedule', 'onAction')],
    'BO-698': [('setEventSchedule', C, 'Dynamic duration and turnaround', 'onAction')],
    'BO-699': [('rescheduleEvent', C, 'Move or cancel, and treat the tickets', 'onAction')],
    'BO-700': [('listSpaces', C, 'Spaces at this venue', 'onLoad')],
    'BO-701': [('setSpace', C, 'Define a space', 'onAction')],
    'BO-702': [('setSpace', C, 'Space access rules', 'onAction')],
    'BO-703': [('setEventCapacityProfile', C, 'Capacity at a glance', 'onLoad')],
    'BO-704': [('setEventCapacityProfile', C, 'The capacity profile', 'onAction')],
    'BO-705': [('setEventCapacityProfile', C, 'Seating mode', 'onAction')],
    'BO-706': [('setEventRegistration', C, 'Registration at a glance', 'onLoad')],
    'BO-707': [('setEventRegistration', C, 'Attendee data and form', 'onAction')],
    'BO-708': [('setEventRegistration', C, 'Participant categories', 'onAction'),
               ('listAccessProfiles', X, 'The passes they map to', 'onLoad')],
    'BO-709': [('setEventRegistration', C, 'Admission and entry policy', 'onAction')],
    'BO-710': [('getEventResourcePlan', C, 'The resource plan', 'onLoad')],
    'BO-711': [('setEventResourcePlan', C, 'What the event needs', 'onAction')],
    'BO-712': [('setEventResourcePlan', C, 'Staff and roles', 'onAction'),
               ('createRotaAssignment', W, 'Roster them', 'onAction')],
    'BO-713': [('setEventResourcePlan', C, 'Contractors and external workforce', 'onAction')],
    'BO-714': [('setShiftTemplate', W, 'Event shifts', 'onAction'),
               ('getStaffingCoverage', W, 'Where it is short', 'onLoad')],
    'BO-715': [('setEventResourcePlan', C, 'Deployment by location', 'onAction')],
    'BO-716': [('setEventLifecycleState', C, 'Lifecycle at a glance', 'onLoad')],
    'BO-717': [('setEventLifecycleState', C, 'Move through the lifecycle', 'onAction')],
    'BO-718': [('createApprovalRequest', A, 'Raise a change request', 'onAction')],
    'BO-719': [('rescheduleEvent', C, 'Cancellation workflow', 'onAction')],
    'BO-720': [('rescheduleEvent', C, 'How tickets and customers are treated', 'onAction')],
    'BO-721': [('setSessionTemplate', C, 'Slot templates', 'onAction'),
               ('listSessionTemplates', C, 'Templates in use', 'onLoad')],
    'BO-722': [('setPrepaidMinutePackage', C, 'Prepaid minute packages', 'onAction'),
               ('listCreditTypes', Q, 'The credit type behind them', 'onLoad')],
    'BO-723': [('setSessionTemplate', C, 'Peak, off-peak and super prime', 'onAction')],
    'BO-724': [('setSessionTemplate', C, 'Walk-in policy', 'onAction')],
    'BO-725': [('listSessionTemplates', C, 'Sessions running', 'onLoad')],
    'BO-726': [('assignSessionMedia', C, 'Attach photos to participants', 'onAction')],
}

RESOURCES_AND_TAIL = {
    # resources b3 — staff as a resource, which is `workforce` plus qualifications
    'BO-873': [('listPrincipals', I, 'The staff directory', 'onLoad')],
    'BO-874': [('getPrincipal', I, 'One person', 'onLoad'),
               ('listResources', 'resources', 'Them as a bookable resource', 'onLoad')],
    'BO-875': [('setResourceQualifications', 'resources', 'Skills and competencies', 'onAction')],
    'BO-876': [('setResourceQualifications', 'resources', 'Certification and expiry', 'onAction'),
               ('validateWorkforceCompliance', W, 'What has lapsed', 'onLoad')],
    'BO-877': [('setResourceQualifications', 'resources', 'Qualification rules', 'onAction'),
               ('suggestResources', 'resources', 'Who qualifies', 'onLoad')],
    'BO-878': [('getResourceSchedule', 'resources', 'Availability and working pattern', 'onLoad'),
               ('setResourceSchedule', 'resources', 'Set it', 'onAction')],
    'BO-879': [('listShiftTemplates', W, 'Shift templates', 'onLoad'),
               ('setShiftTemplate', W, 'Define one', 'onAction')],
    'BO-880': [('listLeaveRequests', W, 'Leave and absence', 'onLoad'),
               ('requestLeave', W, 'Request time off', 'onAction')],
    'BO-881': [('setStaffingRules', W, 'Overtime and working-hour rules', 'onAction')],
    'BO-882': [('listRotaAssignments', W, 'Rota synchronisation', 'onLoad')],

    # resources b4 — the roster
    'BO-883': [('listRotaAssignments', W, 'The roster', 'onLoad'),
               ('getStaffingCoverage', W, 'Where it is short', 'onLoad')],
    'BO-884': [('createRotaAssignment', W, 'Roster a position', 'onAction')],
    'BO-885': [('setStaffingRules', W, 'Minimum staffing and cover', 'onAction')],
    'BO-886': [('getStaffingCoverage', W, 'Gaps, by severity', 'onLoad')],
    'BO-887': [('listOpenShifts', W, 'The shift marketplace', 'onLoad'),
               ('claimOpenShift', W, 'Pick one up', 'onAction')],
    'BO-888': [('listAttendance', W, 'Live attendance', 'onLoad')],
    'BO-889': [('recordAttendance', W, 'Check in or out', 'onAction'),
               ('amendAttendance', W, 'Correct an exception', 'onAction')],
    'BO-890': [('validateWorkforceCompliance', W, 'Where the rota breaks a rule', 'onLoad')],
    'BO-891': [('getLabourCost', W, 'Cost against budget', 'onLoad')],
    'BO-892': [('getStaffingCoverage', W, 'What the planner is optimising', 'onLoad')],

    # resources b7 — event resources, now in `catalogue`
    'BO-913': [('getEventResourcePlan', C, 'Event resource plans', 'onLoad')],
    'BO-914': [('setEventResourcePlan', C, 'What an event needs', 'onAction')],
    'BO-915': [('listSpaces', C, 'Venue and space allocation', 'onLoad'),
               ('bookResource', 'resources', 'Book the space', 'onAction')],
    'BO-916': [('allocateResources', 'resources', 'Equipment allocation', 'onAction')],
    'BO-917': [('createRotaAssignment', W, 'Staff allocation', 'onAction')],
    'BO-918': [('listResourcePackages', 'resources', 'Template library', 'onLoad'),
               ('createResourcePackage', 'resources', 'Save a template', 'onAction')],
    'BO-920': [('getEventResourcePlan', C, 'Cost estimate', 'onLoad')],
    'BO-921': [('getResourceCalendar', 'resources', 'Conflicts across events', 'onLoad')],
    'BO-922': [('getEventResourcePlan', C, 'Readiness gate', 'onLoad'),
               ('createApprovalRequest', A, 'Send for approval', 'onAction')],

    # resources b9 / b10 leftovers
    'BO-938': [('raiseMyCase', M, 'Raise a request', 'onAction')],
    'BO-940': [('listApprovalRequests', A, 'Approvals on mobile', 'onLoad'),
               ('decideApprovalRequest', A, 'Decide', 'onAction')],
    'BO-942': [('getGameplaySyncStatus', G, 'Offline sync state', 'onLoad')],
    'BO-946': [('listDemandBookingCurve', C, 'Forecast accuracy', 'onLoad')],
    'BO-951': [('listAnalyticsPipelines', R, 'Integration and data health', 'onLoad')],
    'BO-952': [('getResourceUtilisation', 'resources', 'Executive resource view', 'onLoad')],

    # gaming wallet screens — superseded to `wallet` on 19 September
    'BO-415': [('listCreditTypes', Q, 'The credit type library', 'onLoad'),
               ('createCreditType', Q, 'Define one', 'onAction')],
    'BO-417': [('setWalletFundingRules', Q, 'Top-up rules', 'onAction')],
    'BO-418': [('setWalletFundingRules', Q, 'Top-up bonus rules', 'onAction')],
    'BO-420': [('updateCreditType', Q, 'Bonus validity and expiry', 'onAction')],
    'BO-483': [('certifyIntegration', 'public-api', 'Integration certification', 'onAction')],
    'BO-486': [('getGameCard', G, 'Identify the customer', 'onLoad')],
    'BO-487': [('getWallet', 'retail', 'Balance summary', 'onLoad')],
    'BO-488': [('topUpWallet', 'retail', 'Self-service top-up', 'onAction')],
    'BO-491': [('listPrizes', G, 'Prize discovery', 'onLoad')],
    'BO-492': [('listGameplayTransactions', G, 'Transaction history', 'onLoad')],

    # rental leftovers
    'BO-523': [('getRentalAvailability', 'rental', 'Availability forecast', 'onLoad')],
    'BO-528': [('listDynamicPricingStrategy', C, 'Dynamic pricing', 'onLoad')],
    'BO-563': [('listOverdueRentals', 'rental', 'Operational alerts', 'onLoad')],
    'BO-583': [('getDueMaintenance', 'maintenance', 'Predictive maintenance', 'onLoad')],
    'BO-585': [('getKpiValues', R, 'Rental revenue', 'onLoad')],
    'BO-590': [('getAnalyticsBenchmark', R, 'Location and channel performance', 'onLoad')],
    'BO-591': [('listDemandBookingCurve', C, 'Demand forecast', 'onLoad')],
    'BO-593': [('askReportingQuestion', R, 'Ask about rentals', 'onAction')],

    # f&b, approvals and wallet tails
    'BO-727': [('listOutlets', T, 'F&B outlets', 'onLoad')],
    'BO-729': [('listMenus', 'fnb', 'Menus', 'onLoad')],
    'BO-730': [('listMenus', 'fnb', 'Menu items', 'onLoad')],
    'BO-731': [('listKitchenTickets', 'fnb', 'Kitchen operations', 'onLoad')],
    'BO-732': [('listOutlets', T, 'Outlet configuration', 'onLoad')],
    'BO-733': [('getKpiValues', R, 'F&B performance', 'onLoad')],
    'ADM-353': [('createWebhookSubscription', 'public-api', 'Webhook subscriptions', 'onAction')],
    'ADM-354': [('listApiClients', 'public-api', 'External workflow systems', 'onLoad')],
    'ADM-356': [('listAccessPolicies', I, 'Integration access control', 'onLoad')],
    'BO-1152': [('listWalletDisputes', Q, 'Operations audit trail', 'onLoad')],
}

INVALIDATES = {
    'setVsiModel': ['getVsiModel'],
    'setLicensingModel': ['listLicensingModels'],
    'setModuleListing': ['listModuleCatalogue'],
    'runGoLiveValidation': ['getGoLiveReadiness'],
    'setLicenceEnforcementPolicy': ['getLicenceEnforcement'],
    'addCapacityPack': ['getLicenceEnforcement', 'getEntitlementUsage'],
    'createAccreditationProgramme': ['listAccreditationProgrammes'],
    'setAccreditationRequirements': ['listAccreditationProgrammes'],
    'createAccreditationApplication': ['listAccreditationApplications'],
    'decideAccreditationApplication': ['listAccreditationApplications',
                                       'listAccreditationHolders'],
    'updateAccreditationHolder': ['getAccreditationHolder', 'listAccreditationHolders'],
    'submitAccreditationDocument': ['getAccreditationHolder'],
    'verifyAccreditationDocument': ['getAccreditationHolder'],
    'issueAccreditationCredential': ['listAccreditationCredentials'],
    'replaceAccreditationCredential': ['listAccreditationCredentials'],
    'setBadgeTemplate': ['listBadgeTemplates'],
    'createBadgePrintJob': ['listBadgePrintJobs'],
    'setAccessProfile': ['listAccessProfiles'],
    'setHolderAccess': ['getAccreditationHolder'],
    'setAccreditationStatus': ['listAccreditationHolders', 'listAccreditationAudit'],
    'setAccreditationValidity': ['listAccreditationHolders'],
    'importAccreditationHolders': ['listAccreditationHolders'],
    'setEventType': ['listEventTypes'],
    'cloneEvent': ['listEvents'],
    'setEventSchedule': ['listEvents'],
    'rescheduleEvent': ['listEvents', 'getSeatInventory'],
    'setSpace': ['listSpaces'],
    'setEventCapacityProfile': ['getSeatInventory'],
    'setEventResourcePlan': ['getEventResourcePlan'],
    'setEventLifecycleState': ['listEvents'],
    'setSessionTemplate': ['listSessionTemplates'],
    'setShiftTemplate': ['listShiftTemplates'],
    'setStaffingRules': ['getStaffingCoverage', 'validateWorkforceCompliance'],
    'requestLeave': ['listLeaveRequests', 'getStaffingCoverage'],
    'claimOpenShift': ['listOpenShifts', 'getStaffingCoverage'],
    'createRotaAssignment': ['listRotaAssignments', 'getStaffingCoverage'],
    'recordAttendance': ['listAttendance', 'getLabourCost'],
    'amendAttendance': ['listAttendance', 'getLabourCost'],
}


def main():
    apply = '--apply' in sys.argv
    wiring = {}
    for d in (LICENSING, ACCREDITATION, EVENTS, RESOURCES_AND_TAIL):
        wiring.update(d)
    added = 0
    touched = 0
    missing = set(wiring)
    for f in FILES:
        doc = yaml.safe_load(io.open(f, encoding='utf8'))
        by_id = {s['id']: s for s in doc['screens']}
        changed = False
        for sid, ops in sorted(wiring.items()):
            s = by_id.get(sid)
            if not s:
                continue
            missing.discard(sid)
            have = {a.get('operationId') for a in (s.get('apis') or [])}
            new = []
            for oid, contract, purpose, trigger in ops:
                if oid in have:
                    continue
                entry = {'operationId': oid, 'contract': contract,
                         'purpose': purpose, 'trigger': trigger,
                         'provenance': 'board reading, 19 September 2026'}
                if INVALIDATES.get(oid):
                    entry['invalidates'] = INVALIDATES[oid]
                new.append(entry)
            if new:
                s.setdefault('apis', []).extend(new)
                added += len(new)
                touched += 1
                changed = True
        if changed and apply:
            io.open(f, 'w', encoding='utf8').write(
                yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100))
            print('  -> %s' % f)

    if missing:
        print('  NOT FOUND (%d): %s' % (len(missing), ', '.join(sorted(missing)[:12])))
    print('%d reference(s) across %d screen(s)' % (added, touched))
    if not apply:
        print('\n  nothing written — pass --apply')


if __name__ == '__main__':
    main()
