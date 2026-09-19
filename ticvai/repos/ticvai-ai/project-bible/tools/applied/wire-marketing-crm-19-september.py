#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire the Marketing CRM configuration reference — twelve boards, 107 screens.

**The largest single pack gap in the package, and nine of its twelve boards were
joins.** `marketing-crm` already held 167 operations covering campaigns, journeys,
message templates and delivery, conversations, cases, surveys and reviews, loyalty and
challenges, waivers, consent and privacy operations. Board 11 is the CMS, which is
`white-label`.

Seventeen operations were missing, all of them on boards 1 to 3 — the guest master data
model, identity resolution, retention, and the audience layer:

  - `mergeGuests` existed and nothing said which records were duplicates or which value
    survives a merge.
  - `listDataRetentionExpiry` could read retention outcomes and nothing set a policy.
  - `createSegment` built audiences and nothing activated one, which is where consent
    has to be enforced — a segment built last month contains people who have since
    opted out.

**This pack is also the one that defeated the matcher twice.** It is a prose PDF with no
directories: 120 screens whose only heading is `Purpose`, holding text like *"maintain
standard and custom attributes… define primary and external identifiers, source-system
priority, survivorship rules."* Those are tasks, and `derive-task-linkage.py` skipped
every one of them because the heading said `Purpose`. It reported 107 of 107 screens
with no candidate operation in any contract, against a contract with 167 of them.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

F = 'screens/P08-venue-back-office.yaml'
M, W, A, R, I = 'marketing-crm', 'white-label', 'approvals', 'reporting', 'identity'

WIRING = {
    # ------------------------------------------------ b1: the guest master
    'BO-734': [('searchGuests', M, 'Find a guest', 'onLoad'),
               ('listSegments', M, 'Segment indicators', 'onLoad')],
    'BO-735': [('searchGuests', M, 'The directory', 'onLoad'),
               ('getGuestProfile', M, 'Open one', 'onAction')],
    'BO-736': [('getGuestAttributeModel', M, 'The shared data model', 'onLoad'),
               ('setGuestAttributeModel', M, 'Change it, as a version', 'onAction')],
    'BO-738': [('getGuestProfile', M, 'The consolidated record', 'onLoad'),
               ('getGuestIntelligence', M, 'Value, engagement and risk', 'onLoad'),
               ('getGuestRelationships', M, 'Household and organisation', 'onLoad')],
    'BO-739': [('getGuestTimeline', M, 'Everything they did, in order', 'onLoad')],
    'BO-740': [('updateGuestPreferences', M, 'Contact and service preferences', 'onAction'),
               ('getGuestProfile', M, 'Verified contacts', 'onLoad')],
    'BO-741': [('getGuestRelationships', M, 'Family and guardians', 'onLoad'),
               ('setGuestRelationships', M, 'Link without merging', 'onAction')],
    'BO-742': [('setGuestRelationships', M, 'Corporate, school and group links', 'onAction')],
    'BO-743': [('getGuestTimeline', M, 'Commercial and document history', 'onLoad'),
               ('uploadGuestDocument', M, 'Attach a document', 'onAction')],

    # ------------------------------------------- b2: governance and privacy
    'BO-744': [('listPrivacyCompliance', M, 'Data quality and consent coverage', 'onLoad'),
               ('listDuplicateCandidates', M, 'Pending merges', 'onLoad')],
    'BO-745': [('getIdentityResolutionRules', M, 'Matching rules', 'onLoad'),
               ('setIdentityResolutionRules', M, 'Weights, thresholds, survivorship', 'onAction')],
    'BO-746': [('listDuplicateCandidates', M, 'Side by side', 'onLoad'),
               ('decideDuplicateCandidate', M, 'Merge, reject or split', 'onAction'),
               ('mergeGuests', M, 'Perform the merge', 'onAction')],
    'BO-747': [('listConsentPurposes', M, 'Purposes and lawful bases', 'onLoad'),
               ('setConsentPurposes', M, 'Configure them', 'onAction')],
    'BO-748': [('listVersioningEffectiveDate', M, 'Consent versions', 'onLoad'),
               ('recordConsent', M, 'Capture a decision', 'onAction')],
    'BO-749': [('setCommunicationPreferenceMarketing', M, 'The preference centre', 'onAction'),
               ('getGuestConsents', M, 'What a guest has chosen', 'onLoad')],
    'BO-750': [('listDataSubjectCustomer', M, 'Privacy requests', 'onLoad'),
               ('setDataDiscoveryAccess', M, 'Assemble and respond', 'onAction')],
    'BO-751': [('setDataRetentionPolicy', M, 'Retention by category and jurisdiction',
                'onAction'),
               ('runDataRetention', M, 'Preview or execute', 'onAction')],
    'BO-752': [('recordPrivacyIncident', M, 'Record an incident', 'onAction'),
               ('listPrivacy', M, 'Approved AI uses and limits', 'onLoad')],
    'BO-753': [('listPrivacyEvidenceCompliance', M, 'Evidence for an audit', 'onLoad')],

    # ------------------------------------------------- b3: audiences
    'BO-754': [('getAudienceOverlap', M, 'Reachability and overlap', 'onLoad'),
               ('listSegments', M, 'Active segments', 'onLoad')],
    'BO-755': [('createSegment', M, 'Build a rule-based audience', 'onAction'),
               ('previewSegment', M, 'Live count while editing', 'onAction')],
    'BO-756': [('importAudienceList', M, 'Import a supplied list', 'onAction'),
               ('listAudienceLists', M, 'Lists held', 'onLoad')],
    'BO-757': [('createSegment', M, 'Behavioural conditions', 'onAction')],
    'BO-758': [('createSegment', M, 'Membership, loyalty and wallet conditions', 'onAction')],
    'BO-759': [('createSegment', M, 'Demographic and geographic conditions', 'onAction')],
    'BO-760': [('createSegment', M, 'Value and engagement bands', 'onAction')],
    'BO-762': [('createSegment', M, 'Convert a predictive audience into a segment', 'onAction'),
               ('previewSegment', M, 'Threshold simulation', 'onAction')],
    'BO-763': [('activateAudience', M, 'Push it somewhere, with consent enforced', 'onAction'),
               ('listAudienceActivations', M, 'Where audiences are in use', 'onLoad')],

    # ------------------------------------------------- b4: campaigns
    'BO-766': [('listCampaigns', M, 'The library and calendar', 'onLoad')],
    'BO-767': [('createCampaign', M, 'Build a campaign', 'onAction'),
               ('updateCampaign', M, 'Change it', 'onAction')],
    'BO-768': [('listSegments', M, 'Choose an audience', 'onLoad'),
               ('updateCampaign', M, 'Attach it', 'onAction')],
    'BO-769': [('listMessageTemplates', M, 'Compose across channels', 'onLoad'),
               ('updateCampaign', M, 'Save the content', 'onAction')],
    'BO-771': [('createApprovalRequest', A, 'Send for approval', 'onAction'),
               ('getCampaign', M, 'What is being approved', 'onLoad')],
    'BO-772': [('getCampaignPerformance', M, 'Budget, goals and pacing', 'onLoad')],
    'BO-773': [('getCampaignPerformance', M, 'Attribution', 'onLoad')],

    # ------------------------------------------------- b5: journeys
    'BO-774': [('listJourneys', M, 'Journeys running', 'onLoad')],
    'BO-775': [('createJourney', M, 'Build a journey', 'onAction'),
               ('activateJourney', M, 'Activate it', 'onAction')],
    'BO-776': [('listMessageTriggers', M, 'The trigger catalogue', 'onLoad'),
               ('setMessageTrigger', M, 'Define one', 'onAction')],
    'BO-777': [('createJourney', M, 'Decision logic and timing', 'onAction')],
    'BO-779': [('createJourney', M, 'Lifecycle journeys', 'onAction')],
    'BO-781': [('getJourneyPerformance', M, 'Journey analytics', 'onLoad')],

    # ------------------------------------------------- b6: communications
    'BO-784': [('listCommunicationService', M, 'Channel health and volume', 'onLoad')],
    'BO-785': [('listMessageTemplates', M, 'The template library', 'onLoad'),
               ('createMessageTemplate', M, 'Create one', 'onAction')],
    'BO-786': [('createMessageTemplate', M, 'Build a newsletter', 'onAction')],
    'BO-787': [('createMessageTemplate', M, 'Content blocks and product feed', 'onAction')],
    'BO-788': [('setMarketingSubscription', M, 'Subscriptions and preferences', 'onAction'),
               ('getMarketingSubscription', M, 'What a guest is subscribed to', 'onLoad')],
    'BO-789': [('listSystemTransactionalTemplate', M, 'Transactional templates', 'onLoad'),
               ('setMessageTrigger', M, 'Notification rules', 'onAction')],
    'BO-790': [('listRoutingPriorityThrottling', M, 'Scheduling, priority and throttling',
                'onLoad')],
    'BO-791': [('listDeliveryQueueFailure', M, 'Failures and retries', 'onLoad'),
               ('retryMessageDispatch', M, 'Retry', 'onAction')],
    'BO-792': [('listProviderHealthUsage', M, 'Deliverability and cost', 'onLoad')],
    'BO-793': [('setLocalizationBrandingCustomer', M, 'Content, translation and branding',
                'onAction')],

    # ------------------------------------------------- b7: omnichannel
    'BO-794': [('listConversations', M, 'Conversations across channels', 'onLoad')],
    'BO-795': [('listConversations', M, 'The unified inbox', 'onLoad'),
               ('claimConversation', M, 'Take one', 'onAction')],
    'BO-796': [('getConversation', M, 'The conversation', 'onLoad'),
               ('getGuestTimeline', M, 'What else they have done', 'onLoad')],
    'BO-797': [('setCustomerServiceCopilot', M, 'Chatbot configuration', 'onAction')],
    'BO-798': [('setCustomerServiceCopilot', M, 'Intent and knowledge', 'onAction')],
    'BO-799': [('sendConversationMessage', M, 'Reply', 'onAction'),
               ('handoverToAgent', M, 'Take it from the bot', 'onAction')],
    'BO-800': [('setIntelligentRoutingSkill', M, 'Routing and queues', 'onAction'),
               ('listAgentWorkloadAvailability', M, 'Who is free', 'onLoad')],
    'BO-801': [('setOrderBookingTicket', M, 'Act on the order from the conversation',
                'onAction')],
    'BO-802': [('listQualityAgentEvaluation', M, 'Sentiment, quality and escalation', 'onLoad'),
               ('escalateCase', M, 'Escalate', 'onAction')],
    'BO-803': [('listUnifiedInteractionCommunication', M, 'Chat analytics and audit', 'onLoad')],

    # ------------------------------------------------- b8: cases
    'BO-805': [('listCases', M, 'The queue', 'onLoad')],
    'BO-807': [('setCaseInvestigationResolution', M, 'Classification and workflow', 'onAction')],
    'BO-808': [('listAgentWorkloadAvailability', M, 'Assignment and workload', 'onLoad')],
    'BO-809': [('listSlaPolicyService', M, 'SLA policies', 'onLoad'),
               ('setApprovalSlaPolicy', A, 'Configure a target and its consequence', 'onAction')],
    'BO-810': [('listEscalationCriticalCase', M, 'Escalation rules in force', 'onLoad')],
    'BO-811': [('getCase', M, 'The case workspace', 'onLoad'),
               ('addCaseMessage', M, 'Reply', 'onAction'),
               ('updateCase', M, 'Update it', 'onAction')],
    'BO-812': [('setRefundCompensationService', M, 'Service recovery', 'onAction')],

    # ------------------------------------------------- b9: voice of customer
    'BO-814': [('listCustomerSatisfactionFeedback', M, 'Feedback at a glance', 'onLoad')],
    'BO-815': [('createForm', M, 'Build a survey', 'onAction')],
    'BO-816': [('setMessageTrigger', M, 'Survey triggers and distribution', 'onAction')],
    'BO-817': [('createForm', M, 'NPS, CSAT and CES configuration', 'onAction')],
    'BO-818': [('listCustomerSatisfactionFeedback', M, 'Responses and insight', 'onLoad')],
    'BO-819': [('listReviews', M, 'Reviews collected', 'onLoad')],
    'BO-820': [('respondToReview', M, 'Moderate and publish', 'onAction')],
    'BO-821': [('listCustomerSatisfactionFeedback', M, 'Sentiment and topics', 'onLoad')],
    'BO-822': [('setRefundCompensationService', M, 'Automated service recovery', 'onAction')],
    'BO-823': [('listServiceRootCause', M, 'Analytics and root cause', 'onLoad')],

    # ------------------------------------------------- b10: gamification
    'BO-824': [('getMyChallenges', M, 'Challenges running', 'onLoad')],
    'BO-825': [('createChallenge', M, 'Build a challenge', 'onAction')],
    'BO-826': [('createChallenge', M, 'Achievements and badges', 'onAction')],
    'BO-827': [('createLoyaltyProgramme', M, 'Points and activity rules', 'onAction')],
    'BO-828': [('createLoyaltyProgramme', M, 'Milestones and rewards', 'onAction')],
    'BO-829': [('createChallenge', M, 'Family, team and event challenges', 'onAction')],
    'BO-830': [('createReferral', M, 'Referral and streak mechanics', 'onAction')],
    'BO-831': [('getLoyaltyPosition', M, 'Progress and leaderboards', 'onLoad')],
    'BO-832': [('getGuestIntelligence', M, 'Who to nudge, and why', 'onLoad')],
    'BO-833': [('listLoyaltyProgrammes', M, 'Gamification analytics', 'onLoad')],

    # ---------------------------- b11: digital experience — this is the CMS
    'BO-834': [('getTenantConfig', W, 'Site and tenant configuration', 'onLoad')],
    'BO-835': [('claimCustomDomain', W, 'Site, brand and domain', 'onAction')],
    'BO-836': [('setBrandIdentity', W, 'Design system and components', 'onAction')],
    'BO-837': [('createContentPage', W, 'Build a page', 'onAction'),
               ('listContentPages', W, 'Pages published', 'onLoad')],
    'BO-838': [('createForm', M, 'Forms on a page', 'onAction'),
               ('searchMedia', 'assets', 'Media to place', 'onLoad')],
    'BO-839': [('createContentBlock', W, 'Dynamic product blocks', 'onAction')],
    'BO-840': [('setHomepageLayout', W, 'Mobile app content', 'onAction')],
    'BO-841': [('setLocalizationBrandingCustomer', M, 'Personalisation and localisation',
                'onAction')],
    'BO-842': [('setSeoMetadata', M, 'SEO metadata', 'onAction'),
               ('createUrlRedirect', M, 'Redirects', 'onAction')],
    'BO-843': [('publishTenantConfig', W, 'Publish', 'onAction')],

    # ------------------------------------------------- b12: waivers
    'BO-845': [('listWaiver', M, 'Waivers and their state', 'onLoad')],
    'BO-846': [('listWaiverTemplateMaster', M, 'Templates', 'onLoad'),
               ('setDigitalWaiverForm', M, 'Build one', 'onAction')],
    'BO-847': [('listWaiverTriggerEligibility', M, 'Assignment rules', 'onLoad')],
    'BO-848': [('listVersioningEffectiveDate', M, 'Version, expiry and renewal', 'onLoad')],
    'BO-849': [('setSignatorySignatureGuardian', M, 'Signature experience', 'onAction')],
    'BO-850': [('listMinorGuardianGroup', M, 'Guardian and group signing', 'onLoad')],
    'BO-851': [('listParticipantWaiverStatus', M, 'Pre-arrival completion', 'onLoad')],
    'BO-852': [('setWaiverVerificationValidation', M, 'Verification and access control',
                'onAction'),
               ('getWaiverStatus', M, 'Whether this guest may enter', 'onLoad')],
    'BO-853': [('listComplianceEvidenceWaiver', M, 'Documents, search and retention', 'onLoad')],
}

INVALIDATES = {
    'setGuestAttributeModel': ['getGuestAttributeModel'],
    'setGuestRelationships': ['getGuestRelationships', 'getGuestProfile'],
    'setIdentityResolutionRules': ['getIdentityResolutionRules', 'listDuplicateCandidates'],
    'decideDuplicateCandidate': ['listDuplicateCandidates'],
    'mergeGuests': ['listDuplicateCandidates', 'searchGuests', 'getGuestProfile'],
    'setDataRetentionPolicy': ['listDataRetentionExpiry'],
    'runDataRetention': ['listDataRetentionExpiry', 'searchGuests'],
    'importAudienceList': ['listAudienceLists', 'listSegments'],
    'activateAudience': ['listAudienceActivations'],
    'createSegment': ['listSegments', 'getAudienceOverlap'],
    'recordConsent': ['getGuestConsents', 'getAudienceOverlap'],
    'updateGuestPreferences': ['getGuestConsents'],
}


def main():
    apply = '--apply' in sys.argv
    d = yaml.safe_load(io.open(F, encoding='utf8'))
    by_id = {s['id']: s for s in d['screens']}
    added = 0
    touched = 0
    missing = []
    for sid, ops in sorted(WIRING.items()):
        s = by_id.get(sid)
        if not s:
            missing.append(sid)
            continue
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
    if missing:
        print('  NOT FOUND (%d): %s' % (len(missing), ', '.join(missing[:10])))
    print('%d reference(s) across %d screen(s)' % (added, touched))
    if not apply:
        print('\n  nothing written — pass --apply')
        return
    io.open(F, 'w', encoding='utf8').write(
        yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
    print('  -> %s' % F)


if __name__ == '__main__':
    main()
