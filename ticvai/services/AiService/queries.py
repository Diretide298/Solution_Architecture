"""Generated. The declared reads and writes of each operation."""

READS = {
 "createAiConversation": [
  "SELECT * FROM ai.conversation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createKnowledgeCollection": [
  "SELECT * FROM ai.chunk_ref LIMIT 50",
  "SELECT * FROM ai.knowledge_collection WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "decideProposedAction": [
  "SELECT * FROM ai.proposed_action LIMIT 50"
 ],
 "generateConfiguration": [
  "SELECT * FROM ai.chunk_ref LIMIT 50",
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.variant_dimension LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM catalogue.event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.performance LIMIT 50",
  "SELECT * FROM catalogue.price LIMIT 50",
  "SELECT * FROM catalogue.price_list LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM marketing.loyalty_programme LIMIT 50",
  "SELECT * FROM platform.region_settings LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50",
  "SELECT * FROM promotions.promotion LIMIT 50",
  "SELECT * FROM seating.seat LIMIT 50",
  "SELECT * FROM seating.seat_category LIMIT 50",
  "SELECT * FROM seating.seat_map LIMIT 50",
  "SELECT * FROM seating.seating_rules LIMIT 50",
  "SELECT * FROM seating.section WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "generateVenueLayout": [
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM assets.media_asset LIMIT 50"
 ],
 "getAiPolicy": [
  "SELECT * FROM ai.policy LIMIT 50"
 ],
 "getAiUsage": [
  "SELECT * FROM ai.interaction WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "ingestKnowledgeDocument": [
  "SELECT * FROM ai.chunk_ref LIMIT 50",
  "SELECT * FROM ai.knowledge_document LIMIT 50"
 ],
 "listAiConversations": [
  "SELECT * FROM ai.conversation WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listAiInteractions": [
  "SELECT * FROM ai.interaction WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listAiProviders": [
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listIndexFailures": [
  "SELECT * FROM ai.index_failure LIMIT 50"
 ],
 "listIndexJobs": [
  "SELECT * FROM ai.index_job LIMIT 50"
 ],
 "listIndexSources": [
  "SELECT * FROM ai.index_job LIMIT 50",
  "SELECT * FROM ai.index_source LIMIT 50"
 ],
 "listKnowledgeCollections": [
  "SELECT * FROM ai.chunk_ref LIMIT 50",
  "SELECT * FROM ai.knowledge_collection WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listProposedActions": [
  "SELECT * FROM ai.proposed_action LIMIT 50"
 ],
 "proposeTranslations": [
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM control.content_block WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "proposeVenueLabels": [
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM venuemap.import_job LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "proposeWalkways": [
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM assets.media_asset LIMIT 50",
  "SELECT * FROM venuemap.import_job LIMIT 50",
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "recordSuggestionOutcome": [
  "SELECT * FROM ai.suggestion WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "reindexSource": [
  "SELECT * FROM ai.index_source LIMIT 50",
  "SELECT * FROM assets.media_asset LIMIT 50",
  "SELECT * FROM catalogue.entitlement_template WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM fnb.menu_item LIMIT 50",
  "SELECT * FROM maintenance.inspection_template LIMIT 50",
  "SELECT * FROM marketing.case LIMIT 50",
  "SELECT * FROM reporting.report_definition WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM retail.merchandise LIMIT 50",
  "SELECT * FROM whitelabel.content_page WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM whitelabel.faq_entry LIMIT 50",
  "SELECT * FROM whitelabel.policy WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "removeIndexEntry": [
  "SELECT * FROM ai.index_entry LIMIT 50"
 ],
 "requestSuggestion": [
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM ai.suggestion WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "semanticSearch": [
  "SELECT * FROM ai.chunk_ref LIMIT 50",
  "SELECT * FROM ai.knowledge_collection WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM ai.knowledge_document LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "sendAiMessage": [
  "SELECT * FROM ai.chunk_ref LIMIT 50",
  "SELECT * FROM ai.conversation WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM ai.knowledge_document LIMIT 50",
  "SELECT * FROM ai.message LIMIT 50",
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM ai.proposed_action LIMIT 50",
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setAiCredential": [
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setAiPolicy": [
  "SELECT * FROM ai.policy LIMIT 50"
 ],
 "setAiProvider": [
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setIndexSource": [
  "SELECT * FROM ai.index_source LIMIT 50",
  "SELECT * FROM ai.knowledge_collection WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setSuggestionProvider": [
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "testAiProvider": [
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50"
 ]
}

WRITES = {
 "createAiConversation": [
  "SELECT id FROM ai.conversation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createKnowledgeCollection": [
  "SELECT id FROM ai.knowledge_collection WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "decideProposedAction": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.proposed_action ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "generateConfiguration": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.proposed_action ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "generateVenueLayout": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.layout_draft WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "ingestKnowledgeDocument": [
  "SELECT id FROM ai.knowledge_document ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "proposeTranslations": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.proposed_action ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "proposeVenueLabels": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.proposed_action ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "proposeWalkways": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.proposed_action ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordSuggestionOutcome": [
  "SELECT id FROM ai.suggestion_outcome ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reindexSource": [
  "SELECT id FROM ai.index_entry ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.index_job ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "removeIndexEntry": [
  "SELECT id FROM ai.index_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "requestSuggestion": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.suggestion WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "semanticSearch": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "sendAiMessage": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.message ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAiCredential": [
  "SELECT id FROM ai.provider WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAiPolicy": [
  "SELECT id FROM ai.policy ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAiProvider": [
  "SELECT id FROM ai.provider WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setIndexSource": [
  "SELECT id FROM ai.index_source ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setSuggestionProvider": [
  "SELECT id FROM ai.policy ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "testAiProvider": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ai.provider WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "createAiConversation": [
  "cache:idempotency:bench"
 ],
 "createKnowledgeCollection": [
  "cache:idempotency:bench"
 ],
 "decideProposedAction": [
  "cache:idempotency:bench"
 ],
 "generateConfiguration": [
  "cache:idempotency:bench"
 ],
 "generateVenueLayout": [
  "cache:idempotency:bench"
 ],
 "ingestKnowledgeDocument": [
  "cache:embedding:bench",
  "cache:idempotency:bench"
 ],
 "proposeTranslations": [
  "cache:idempotency:bench"
 ],
 "proposeVenueLabels": [
  "cache:idempotency:bench"
 ],
 "proposeWalkways": [
  "cache:idempotency:bench"
 ],
 "recordSuggestionOutcome": [
  "cache:idempotency:bench"
 ],
 "reindexSource": [
  "cache:embedding:bench",
  "cache:idempotency:bench"
 ],
 "removeIndexEntry": [
  "cache:embedding:bench",
  "cache:idempotency:bench"
 ],
 "requestSuggestion": [
  "cache:idempotency:bench"
 ],
 "semanticSearch": [
  "cache:answer:bench",
  "cache:idempotency:bench"
 ],
 "sendAiMessage": [
  "cache:answer:bench",
  "cache:idempotency:bench"
 ],
 "setAiCredential": [
  "cache:idempotency:bench"
 ],
 "setAiPolicy": [
  "cache:idempotency:bench"
 ],
 "setAiProvider": [
  "cache:idempotency:bench"
 ],
 "setIndexSource": [
  "cache:idempotency:bench"
 ],
 "setSuggestionProvider": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "testAiProvider": [
  "cache:idempotency:bench"
 ]
}
