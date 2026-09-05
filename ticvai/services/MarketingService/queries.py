"""Generated. The declared reads and writes of each operation."""

READS = {
 "accrueLoyaltyPoints": [
  "SELECT * FROM marketing.loyalty_position LIMIT 50",
  "SELECT * FROM marketing.loyalty_programme LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "activateJourney": [
  "SELECT * FROM marketing.journey WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "addCaseMessage": [
  "SELECT * FROM marketing.case_message LIMIT 50"
 ],
 "addGuestNote": [
  "SELECT * FROM marketing.guest_profile LIMIT 50"
 ],
 "addSuppression": [
  "SELECT * FROM marketing.suppression WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "addToWishlist": [
  "SELECT * FROM marketing.wishlist_item LIMIT 50"
 ],
 "adjustLoyaltyPoints": [
  "SELECT * FROM marketing.loyalty_position LIMIT 50"
 ],
 "claimConversation": [
  "SELECT * FROM marketing.agent_availability LIMIT 50",
  "SELECT * FROM marketing.conversation LIMIT 50"
 ],
 "closeConversation": [
  "SELECT * FROM marketing.conversation LIMIT 50"
 ],
 "createCampaign": [
  "SELECT * FROM marketing.campaign LIMIT 50",
  "SELECT * FROM marketing.segment_criterion LIMIT 50"
 ],
 "createCase": [
  "SELECT * FROM marketing.case LIMIT 50"
 ],
 "createChallenge": [
  "SELECT * FROM catalogue.event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.loyalty_programme LIMIT 50"
 ],
 "createForm": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.form_definition WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createInvitationCampaign": [
  "SELECT * FROM catalogue.event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createJourney": [
  "SELECT * FROM marketing.journey WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.message_template LIMIT 50"
 ],
 "createLoyaltyProgramme": [
  "SELECT * FROM marketing.loyalty_programme LIMIT 50"
 ],
 "createMessageTemplate": [
  "SELECT * FROM marketing.message_template LIMIT 50"
 ],
 "createReferral": [
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM promotions.promotion LIMIT 50"
 ],
 "createSegment": [
  "SELECT * FROM marketing.segment LIMIT 50",
  "SELECT * FROM marketing.segment_criterion LIMIT 50"
 ],
 "createUrlRedirect": [
  "SELECT * FROM control.url_redirect WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "endKioskAssist": [
  "SELECT * FROM marketing.kiosk_assist_session LIMIT 50"
 ],
 "escalateCase": [
  "SELECT * FROM marketing.case LIMIT 50"
 ],
 "getCampaign": [
  "SELECT * FROM marketing.campaign LIMIT 50"
 ],
 "getCampaignPerformance": [
  "SELECT * FROM marketing.attribution_touch LIMIT 50",
  "SELECT * FROM marketing.campaign LIMIT 50",
  "SELECT * FROM marketing.message_delivery LIMIT 50"
 ],
 "getCase": [
  "SELECT * FROM marketing.case LIMIT 50",
  "SELECT * FROM marketing.case_message LIMIT 50"
 ],
 "getConsentHistory": [
  "SELECT * FROM marketing.consent_record LIMIT 50"
 ],
 "getConversation": [
  "SELECT * FROM marketing.conversation LIMIT 50",
  "SELECT * FROM marketing.conversation_message LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "getGuestConsents": [
  "SELECT * FROM marketing.consent_purpose LIMIT 50",
  "SELECT * FROM marketing.consent_record LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "getGuestLoyalty": [
  "SELECT * FROM marketing.loyalty_position LIMIT 50"
 ],
 "getGuestProfile": [
  "SELECT * FROM marketing.consent_record LIMIT 50",
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM marketing.loyalty_position LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50",
  "SELECT * FROM pii.subject_contact LIMIT 50"
 ],
 "getJourneyPerformance": [
  "SELECT * FROM marketing.attribution_touch LIMIT 50",
  "SELECT * FROM marketing.journey WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.journey_entrant WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.message_dispatch LIMIT 50"
 ],
 "getLostItemMatches": [
  "SELECT * FROM marketing.lost_item LIMIT 50"
 ],
 "getLoyaltyPosition": [
  "SELECT * FROM marketing.loyalty_programme LIMIT 50"
 ],
 "getMessageStatus": [
  "SELECT * FROM marketing.message_dispatch LIMIT 50"
 ],
 "getMyChallenges": [
  "SELECT * FROM marketing.challenge WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.challenge_progress LIMIT 50"
 ],
 "getSuppressionList": [
  "SELECT * FROM marketing.suppression WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getWaiverStatus": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.form_definition WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.form_submission LIMIT 50"
 ],
 "getWishlist": [
  "SELECT * FROM marketing.wishlist_item LIMIT 50"
 ],
 "handoverToAgent": [
  "SELECT * FROM marketing.agent_availability LIMIT 50",
  "SELECT * FROM marketing.conversation LIMIT 50"
 ],
 "identifyGuest": [
  "SELECT * FROM access.blacklist WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM marketing.loyalty_position LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "launchCampaign": [
  "SELECT * FROM marketing.campaign LIMIT 50"
 ],
 "listCampaigns": [
  "SELECT * FROM marketing.campaign LIMIT 50"
 ],
 "listCases": [
  "SELECT * FROM marketing.case LIMIT 50"
 ],
 "listConsentPurposes": [
  "SELECT * FROM marketing.consent_purpose LIMIT 50"
 ],
 "listConversations": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM marketing.conversation LIMIT 50"
 ],
 "listGuestDevices": [
  "SELECT * FROM marketing.guest_device LIMIT 50"
 ],
 "listJourneys": [
  "SELECT * FROM marketing.journey WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listLostItems": [
  "SELECT * FROM marketing.lost_item LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "listLoyaltyProgrammes": [
  "SELECT * FROM marketing.loyalty_programme LIMIT 50"
 ],
 "listMessageTemplates": [
  "SELECT * FROM marketing.message_template LIMIT 50"
 ],
 "listMessageTriggers": [
  "SELECT * FROM marketing.message_trigger WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listMyCases": [
  "SELECT * FROM marketing.case LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "listReviews": [
  "SELECT * FROM marketing.review LIMIT 50"
 ],
 "listSegmentMembers": [
  "SELECT * FROM marketing.guest_profile LIMIT 50"
 ],
 "listSegments": [
  "SELECT * FROM marketing.segment LIMIT 50"
 ],
 "matchGuest": [
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "matchLostItem": [
  "SELECT * FROM marketing.lost_item LIMIT 50"
 ],
 "mergeGuestProfiles": [
  "SELECT * FROM marketing.guest_profile LIMIT 50"
 ],
 "mergeGuests": [
  "SELECT * FROM marketing.consent_record LIMIT 50",
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "pauseCampaign": [
  "SELECT * FROM marketing.campaign LIMIT 50"
 ],
 "previewSegment": [
  "SELECT * FROM marketing.segment LIMIT 50"
 ],
 "raiseMyCase": [
  "SELECT * FROM marketing.case LIMIT 50"
 ],
 "recordConsent": [
  "SELECT * FROM marketing.guest_profile LIMIT 50"
 ],
 "recordLostItem": [
  "SELECT * FROM marketing.lost_item LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "recordPrivacyIncident": [
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "recordTouchPoint": [
  "SELECT * FROM marketing.campaign LIMIT 50",
  "SELECT * FROM marketing.journey WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "redeemLoyaltyPoints": [
  "SELECT * FROM marketing.loyalty_position LIMIT 50",
  "SELECT * FROM marketing.loyalty_programme LIMIT 50"
 ],
 "registerGuestDevice": [
  "SELECT * FROM marketing.guest_device LIMIT 50"
 ],
 "removeFromWishlist": [
  "SELECT * FROM marketing.guest_profile LIMIT 50"
 ],
 "reopenCase": [
  "SELECT * FROM marketing.case LIMIT 50"
 ],
 "replyToMyCase": [
  "SELECT * FROM marketing.case LIMIT 50"
 ],
 "respondToInvitation": [
  "SELECT * FROM marketing.invitation WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.invitation_campaign WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "respondToReview": [
  "SELECT * FROM marketing.review LIMIT 50"
 ],
 "retryMessageDispatch": [
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM marketing.message_dispatch LIMIT 50",
  "SELECT * FROM marketing.suppression WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "revokeGuestDevice": [
  "SELECT * FROM marketing.guest_profile LIMIT 50"
 ],
 "searchGuests": [
  "SELECT * FROM marketing.guest_profile LIMIT 50"
 ],
 "sendConversationMessage": [
  "SELECT * FROM marketing.conversation LIMIT 50"
 ],
 "sendTransactionalMessage": [
  "SELECT * FROM marketing.message_dispatch LIMIT 50"
 ],
 "setAgentAvailability": [
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "setCallDisposition": [
  "SELECT * FROM marketing.case LIMIT 50",
  "SELECT * FROM marketing.conversation LIMIT 50"
 ],
 "setConsentPurposes": [
  "SELECT * FROM marketing.consent_purpose LIMIT 50"
 ],
 "setMessageTrigger": [
  "SELECT * FROM marketing.message_template LIMIT 50",
  "SELECT * FROM marketing.message_trigger WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setSeoMetadata": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "startKioskAssist": [
  "SELECT * FROM orders.cart LIMIT 50",
  "SELECT * FROM platform.device LIMIT 50"
 ],
 "stopCampaign": [
  "SELECT * FROM marketing.campaign LIMIT 50",
  "SELECT * FROM marketing.segment_criterion LIMIT 50"
 ],
 "submitForm": [
  "SELECT * FROM marketing.consent_record LIMIT 50",
  "SELECT * FROM marketing.form_definition WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ],
 "submitReview": [
  "SELECT * FROM marketing.review LIMIT 50"
 ],
 "testSendCampaign": [
  "SELECT * FROM marketing.campaign LIMIT 50"
 ],
 "transferConversation": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM marketing.conversation LIMIT 50"
 ],
 "unscheduleCampaign": [
  "SELECT * FROM marketing.campaign LIMIT 50"
 ],
 "updateCampaign": [
  "SELECT * FROM marketing.campaign LIMIT 50",
  "SELECT * FROM marketing.segment_criterion LIMIT 50"
 ],
 "updateCase": [
  "SELECT * FROM marketing.case LIMIT 50"
 ],
 "updateGuestPreferences": [
  "SELECT * FROM marketing.guest_profile LIMIT 50"
 ],
 "updateGuestProfile": [
  "SELECT * FROM marketing.guest_profile LIMIT 50",
  "SELECT * FROM marketing.loyalty_position LIMIT 50"
 ],
 "updateMyProfile": [
  "SELECT * FROM marketing.guest_profile LIMIT 50"
 ],
 "uploadGuestDocument": [
  "SELECT * FROM marketing.consent_record LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50"
 ]
}

WRITES = {
 "accrueLoyaltyPoints": [
  "SELECT id FROM marketing.loyalty_position ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "activateJourney": [
  "SELECT id FROM marketing.journey WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "addCaseMessage": [
  "SELECT id FROM marketing.case_message ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "addSuppression": [
  "SELECT id FROM marketing.suppression WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "addToWishlist": [
  "SELECT id FROM marketing.wishlist_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "adjustLoyaltyPoints": [
  "SELECT id FROM marketing.loyalty_position ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "claimConversation": [
  "SELECT id FROM marketing.conversation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closeConversation": [
  "SELECT id FROM marketing.case ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.conversation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createCampaign": [
  "SELECT id FROM marketing.campaign ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.segment_criterion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createCase": [
  "SELECT id FROM marketing.case ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createChallenge": [
  "SELECT id FROM marketing.challenge WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createForm": [
  "SELECT id FROM marketing.form_definition WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createInvitationCampaign": [
  "SELECT id FROM marketing.invitation_campaign WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createJourney": [
  "SELECT id FROM marketing.journey WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createLoyaltyProgramme": [
  "SELECT id FROM marketing.loyalty_programme ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createMessageTemplate": [
  "SELECT id FROM marketing.message_template ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createReferral": [
  "SELECT id FROM marketing.referral WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createSegment": [
  "SELECT id FROM marketing.segment ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.segment_criterion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createUrlRedirect": [
  "SELECT id FROM control.url_redirect WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "endKioskAssist": [
  "SELECT id FROM marketing.kiosk_assist_session ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "escalateCase": [
  "SELECT id FROM marketing.case ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "handoverToAgent": [
  "SELECT id FROM marketing.conversation ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "launchCampaign": [
  "SELECT id FROM marketing.campaign ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "matchLostItem": [
  "SELECT id FROM marketing.case ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.lost_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "mergeGuestProfiles": [
  "SELECT id FROM marketing.guest_profile ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "mergeGuests": [
  "SELECT id FROM marketing.guest_profile ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM pii.subject ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "pauseCampaign": [
  "SELECT id FROM marketing.campaign ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "previewSegment": [
  "SELECT id FROM marketing.segment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "raiseMyCase": [
  "SELECT id FROM marketing.case ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordConsent": [
  "SELECT id FROM marketing.guest_profile ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordLostItem": [
  "SELECT id FROM marketing.lost_item ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordPrivacyIncident": [
  "SELECT id FROM marketing.privacy_incident WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordTouchPoint": [
  "SELECT id FROM marketing.touch_point ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "redeemLoyaltyPoints": [
  "SELECT id FROM marketing.loyalty_position ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.stored_value_authorisation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "registerGuestDevice": [
  "SELECT id FROM marketing.guest_device ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "removeFromWishlist": [
  "SELECT id FROM marketing.guest_profile ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reopenCase": [
  "SELECT id FROM marketing.case ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "replyToMyCase": [
  "SELECT id FROM marketing.case_message ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "respondToInvitation": [
  "SELECT id FROM marketing.invitation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "respondToReview": [
  "SELECT id FROM marketing.review ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "retryMessageDispatch": [
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "revokeGuestDevice": [
  "SELECT id FROM marketing.guest_profile ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "sendConversationMessage": [
  "SELECT id FROM marketing.conversation ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.conversation_message ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "sendTransactionalMessage": [
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAgentAvailability": [
  "SELECT id FROM marketing.agent_availability ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setCallDisposition": [
  "SELECT id FROM marketing.case ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.conversation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setConsentPurposes": [
  "SELECT id FROM marketing.consent_purpose ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setMessageTrigger": [
  "SELECT id FROM marketing.message_trigger WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setSeoMetadata": [
  "SELECT id FROM control.seo_metadata WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "startKioskAssist": [
  "SELECT id FROM marketing.kiosk_assist_session ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "stopCampaign": [
  "SELECT id FROM marketing.campaign ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.segment_criterion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "submitForm": [
  "SELECT id FROM marketing.consent_record ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.form_submission ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "submitReview": [
  "SELECT id FROM marketing.review ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "testSendCampaign": [
  "SELECT id FROM marketing.campaign ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "transferConversation": [
  "SELECT id FROM marketing.conversation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "unscheduleCampaign": [
  "SELECT id FROM marketing.campaign ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateCampaign": [
  "SELECT id FROM marketing.campaign ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.segment_criterion ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateCase": [
  "SELECT id FROM marketing.case ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateGuestPreferences": [
  "SELECT id FROM marketing.guest_profile ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateGuestProfile": [
  "SELECT id FROM marketing.guest_profile ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.loyalty_position ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateMyProfile": [
  "SELECT id FROM marketing.guest_profile ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM pii.subject ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "uploadGuestDocument": [
  "SELECT id FROM marketing.guest_document ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "accrueLoyaltyPoints": [
  "cache:idempotency:bench"
 ],
 "activateJourney": [
  "cache:idempotency:bench"
 ],
 "addCaseMessage": [
  "cache:idempotency:bench"
 ],
 "addGuestNote": [
  "cache:idempotency:bench"
 ],
 "addSuppression": [
  "cache:idempotency:bench"
 ],
 "addToWishlist": [
  "cache:idempotency:bench"
 ],
 "adjustLoyaltyPoints": [
  "cache:idempotency:bench"
 ],
 "claimConversation": [
  "cache:idempotency:bench"
 ],
 "closeConversation": [
  "cache:idempotency:bench"
 ],
 "createCampaign": [
  "cache:idempotency:bench"
 ],
 "createCase": [
  "cache:idempotency:bench"
 ],
 "createChallenge": [
  "cache:idempotency:bench"
 ],
 "createForm": [
  "cache:idempotency:bench"
 ],
 "createInvitationCampaign": [
  "cache:idempotency:bench"
 ],
 "createJourney": [
  "cache:idempotency:bench"
 ],
 "createLoyaltyProgramme": [
  "cache:idempotency:bench"
 ],
 "createMessageTemplate": [
  "cache:idempotency:bench"
 ],
 "createReferral": [
  "cache:idempotency:bench"
 ],
 "createSegment": [
  "cache:idempotency:bench"
 ],
 "createUrlRedirect": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "endKioskAssist": [
  "cache:idempotency:bench"
 ],
 "escalateCase": [
  "cache:idempotency:bench"
 ],
 "handoverToAgent": [
  "cache:idempotency:bench"
 ],
 "launchCampaign": [
  "cache:idempotency:bench"
 ],
 "listConsentPurposes": [
  "cache:resolution:bench"
 ],
 "matchLostItem": [
  "cache:idempotency:bench"
 ],
 "mergeGuestProfiles": [
  "cache:idempotency:bench"
 ],
 "mergeGuests": [
  "cache:idempotency:bench"
 ],
 "pauseCampaign": [
  "cache:idempotency:bench"
 ],
 "previewSegment": [
  "cache:idempotency:bench"
 ],
 "raiseMyCase": [
  "cache:idempotency:bench"
 ],
 "recordConsent": [
  "cache:idempotency:bench"
 ],
 "recordLostItem": [
  "cache:idempotency:bench"
 ],
 "recordPrivacyIncident": [
  "cache:idempotency:bench"
 ],
 "recordTouchPoint": [
  "cache:idempotency:bench"
 ],
 "redeemLoyaltyPoints": [
  "cache:idempotency:bench"
 ],
 "registerGuestDevice": [
  "cache:idempotency:bench"
 ],
 "removeFromWishlist": [
  "cache:idempotency:bench"
 ],
 "reopenCase": [
  "cache:idempotency:bench"
 ],
 "replyToMyCase": [
  "cache:idempotency:bench"
 ],
 "respondToInvitation": [
  "cache:idempotency:bench"
 ],
 "respondToReview": [
  "cache:idempotency:bench"
 ],
 "retryMessageDispatch": [
  "cache:idempotency:bench"
 ],
 "revokeGuestDevice": [
  "cache:idempotency:bench"
 ],
 "sendConversationMessage": [
  "cache:idempotency:bench"
 ],
 "sendTransactionalMessage": [
  "cache:idempotency:bench"
 ],
 "setAgentAvailability": [
  "cache:idempotency:bench"
 ],
 "setCallDisposition": [
  "cache:idempotency:bench"
 ],
 "setConsentPurposes": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setMessageTrigger": [
  "cache:idempotency:bench"
 ],
 "setSeoMetadata": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "startKioskAssist": [
  "cache:idempotency:bench"
 ],
 "stopCampaign": [
  "cache:idempotency:bench"
 ],
 "submitForm": [
  "cache:idempotency:bench"
 ],
 "submitReview": [
  "cache:idempotency:bench"
 ],
 "testSendCampaign": [
  "cache:idempotency:bench"
 ],
 "transferConversation": [
  "cache:idempotency:bench"
 ],
 "unscheduleCampaign": [
  "cache:idempotency:bench"
 ],
 "updateCampaign": [
  "cache:idempotency:bench"
 ],
 "updateCase": [
  "cache:idempotency:bench"
 ],
 "updateGuestPreferences": [
  "cache:idempotency:bench"
 ],
 "updateGuestProfile": [
  "cache:idempotency:bench"
 ],
 "updateMyProfile": [
  "cache:idempotency:bench"
 ],
 "uploadGuestDocument": [
  "cache:idempotency:bench"
 ]
}
