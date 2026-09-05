"""Generated. The declared reads and writes of each operation."""

READS = {
 "acceptVenueLabelProposals": [
  "SELECT * FROM ai.proposed_action LIMIT 50",
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "acceptWalkwayProposals": [
  "SELECT * FROM ai.proposed_action LIMIT 50",
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "acceptWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "adjustGameCard": [
  "SELECT * FROM games.card LIMIT 50"
 ],
 "attachWorkOrderEvidence": [
  "SELECT * FROM assets.media_asset LIMIT 50",
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "bookResource": [
  "SELECT * FROM resources.booking LIMIT 50",
  "SELECT * FROM resources.resource WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "callNextParties": [
  "SELECT * FROM queue.queue LIMIT 50"
 ],
 "cancelWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "checkInResource": [
  "SELECT * FROM resources.booking LIMIT 50",
  "SELECT * FROM resources.resource WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "checkOutResource": [
  "SELECT * FROM pii.subject LIMIT 50",
  "SELECT * FROM resources.booking LIMIT 50",
  "SELECT * FROM resources.resource WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "closeWorkOrder": [
  "SELECT * FROM maintenance.asset LIMIT 50",
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "completeUpload": [
  "SELECT * FROM assets.media_asset LIMIT 50"
 ],
 "completeWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "configureQueueFeed": [
  "SELECT * FROM queue.feed LIMIT 50"
 ],
 "createAsset": [
  "SELECT * FROM maintenance.asset LIMIT 50"
 ],
 "createCollection": [
  "SELECT * FROM assets.media_collection LIMIT 50"
 ],
 "createGame": [
  "SELECT * FROM games.game LIMIT 50"
 ],
 "createInspectionTemplate": [
  "SELECT * FROM maintenance.inspection_template LIMIT 50"
 ],
 "createMaintenancePlan": [
  "SELECT * FROM maintenance.maintenance_plan LIMIT 50"
 ],
 "createPrize": [
  "SELECT * FROM games.prize LIMIT 50"
 ],
 "createQueue": [
  "SELECT * FROM queue.queue LIMIT 50"
 ],
 "createResource": [
  "SELECT * FROM platform.org_unit LIMIT 50",
  "SELECT * FROM resources.resource WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createUpload": [
  "SELECT * FROM assets.media_upload LIMIT 50"
 ],
 "createVenueMap": [
  "SELECT * FROM assets.media_asset LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50",
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "deleteMediaAsset": [
  "SELECT * FROM assets.media_usage LIMIT 50"
 ],
 "getAsset": [
  "SELECT * FROM maintenance.asset LIMIT 50",
  "SELECT * FROM maintenance.maintenance_plan LIMIT 50",
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "getAssetHistory": [
  "SELECT * FROM maintenance.asset LIMIT 50"
 ],
 "getDueMaintenance": [
  "SELECT * FROM maintenance.asset LIMIT 50",
  "SELECT * FROM maintenance.maintenance_plan LIMIT 50"
 ],
 "getExpiringRights": [
  "SELECT * FROM assets.media_asset LIMIT 50"
 ],
 "getGameCard": [
  "SELECT * FROM games.card LIMIT 50",
  "SELECT * FROM games.credit_ledger LIMIT 50"
 ],
 "getIncident": [
  "SELECT * FROM maintenance.incident LIMIT 50"
 ],
 "getMediaAsset": [
  "SELECT * FROM assets.media_asset LIMIT 50",
  "SELECT * FROM assets.media_usage LIMIT 50"
 ],
 "getQueue": [
  "SELECT * FROM queue.queue LIMIT 50"
 ],
 "getQueueFeedHealth": [
  "SELECT * FROM queue.feed LIMIT 50"
 ],
 "getResourceAvailability": [
  "SELECT * FROM maintenance.work_order LIMIT 50",
  "SELECT * FROM resources.booking LIMIT 50",
  "SELECT * FROM resources.resource WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getSessionManifest": [
  "SELECT * FROM marketing.consent_record LIMIT 50",
  "SELECT * FROM pii.subject LIMIT 50",
  "SELECT * FROM resources.session_participant LIMIT 50"
 ],
 "getSignageQueueBoard": [
  "SELECT * FROM queue.queue LIMIT 50",
  "SELECT * FROM queue.reading LIMIT 50"
 ],
 "getSignageQueueCalls": [
  "SELECT * FROM queue.waiting_guest LIMIT 50"
 ],
 "getVenueMap": [
  "SELECT * FROM assets.media_asset LIMIT 50",
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM venuemap.path LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "getVenueMapGraph": [
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM venuemap.path LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "getVenueMapLive": [
  "SELECT * FROM access.scan_event WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM queue.waiting_guest LIMIT 50",
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "getWaitTimes": [
  "SELECT * FROM queue.waiting_guest LIMIT 50",
  "SELECT * FROM queue.queue LIMIT 50",
  "SELECT * FROM queue.reading LIMIT 50"
 ],
 "getWaitingGuest": [
  "SELECT * FROM queue.waiting_guest LIMIT 50"
 ],
 "getWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "importVenueGeometry": [
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "issueGameCard": [
  "SELECT * FROM games.card LIMIT 50"
 ],
 "joinQueue": [
  "SELECT * FROM queue.waiting_guest LIMIT 50"
 ],
 "leaveQueue": [
  "SELECT * FROM queue.waiting_guest LIMIT 50"
 ],
 "listAssets": [
  "SELECT * FROM maintenance.asset LIMIT 50"
 ],
 "listCollections": [
  "SELECT * FROM assets.media_collection LIMIT 50"
 ],
 "listGames": [
  "SELECT * FROM games.game LIMIT 50"
 ],
 "listIncidents": [
  "SELECT * FROM maintenance.incident LIMIT 50"
 ],
 "listInspectionTemplates": [
  "SELECT * FROM maintenance.inspection_template LIMIT 50"
 ],
 "listInspections": [
  "SELECT * FROM maintenance.inspection LIMIT 50"
 ],
 "listMaintenancePlans": [
  "SELECT * FROM maintenance.maintenance_plan LIMIT 50"
 ],
 "listPrizes": [
  "SELECT * FROM games.prize LIMIT 50"
 ],
 "listQueueEntries": [
  "SELECT * FROM queue.waiting_guest LIMIT 50"
 ],
 "listQueueFeeds": [
  "SELECT * FROM queue.feed LIMIT 50"
 ],
 "listQueues": [
  "SELECT * FROM queue.queue LIMIT 50"
 ],
 "listResources": [
  "SELECT * FROM resources.resource WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listVenueMaps": [
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listWorkOrders": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "loadGameCredits": [
  "SELECT * FROM games.card LIMIT 50"
 ],
 "lookupAsset": [
  "SELECT * FROM maintenance.asset LIMIT 50",
  "SELECT * FROM maintenance.maintenance_plan LIMIT 50",
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "overrideWaitingGuest": [
  "SELECT * FROM queue.waiting_guest LIMIT 50"
 ],
 "pauseWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "publishVenueMap": [
  "SELECT * FROM assets.media_asset LIMIT 50",
  "SELECT * FROM platform.outlet LIMIT 50",
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM venuemap.path LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "recordAuthorityNotification": [
  "SELECT * FROM maintenance.incident LIMIT 50"
 ],
 "recordGamePlay": [
  "SELECT * FROM games.play LIMIT 50"
 ],
 "recordWorkOrderParts": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "recordWorkOrderTime": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "redeemPrize": [
  "SELECT * FROM games.redemption LIMIT 50"
 ],
 "redeemWaitingGuest": [
  "SELECT * FROM queue.waiting_guest LIMIT 50"
 ],
 "rejectWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "reorderSessionManifest": [
  "SELECT * FROM resources.session_participant LIMIT 50"
 ],
 "replaceMediaAsset": [
  "SELECT * FROM assets.media_asset LIMIT 50"
 ],
 "reportIncident": [
  "SELECT * FROM maintenance.incident LIMIT 50"
 ],
 "resumeWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "searchMedia": [
  "SELECT * FROM assets.media_asset LIMIT 50"
 ],
 "setAssetStatus": [
  "SELECT * FROM maintenance.asset LIMIT 50"
 ],
 "setPathClosure": [
  "SELECT * FROM venuemap.path LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "setQueueStatus": [
  "SELECT * FROM queue.queue LIMIT 50"
 ],
 "setReaderProfile": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM games.reader_profile WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setResourceQualifications": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM resources.resource WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setVenuePoint": [
  "SELECT * FROM access.access_point WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM platform.outlet LIMIT 50",
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setWaitTime": [
  "SELECT * FROM queue.queue LIMIT 50"
 ],
 "startWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "submitInspection": [
  "SELECT * FROM maintenance.inspection LIMIT 50"
 ],
 "submitQueueReading": [
  "SELECT * FROM queue.reading LIMIT 50"
 ],
 "syncGamePlays": [
  "SELECT * FROM games.card LIMIT 50",
  "SELECT * FROM games.game LIMIT 50"
 ],
 "testQueueFeed": [
  "SELECT * FROM queue.reading LIMIT 50"
 ],
 "transferGameCard": [
  "SELECT * FROM games.card LIMIT 50"
 ],
 "updateAsset": [
  "SELECT * FROM maintenance.asset LIMIT 50"
 ],
 "updateGame": [
  "SELECT * FROM games.game LIMIT 50"
 ],
 "updateIncident": [
  "SELECT * FROM maintenance.incident LIMIT 50"
 ],
 "updateMaintenancePlan": [
  "SELECT * FROM maintenance.maintenance_plan LIMIT 50"
 ],
 "updateMediaAsset": [
  "SELECT * FROM assets.media_asset LIMIT 50"
 ],
 "updateQueue": [
  "SELECT * FROM queue.queue LIMIT 50"
 ],
 "updateWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ],
 "validateVenueMapGraph": [
  "SELECT * FROM venuemap.map WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM venuemap.path LIMIT 50",
  "SELECT * FROM venuemap.point LIMIT 50"
 ],
 "verifyWorkOrder": [
  "SELECT * FROM maintenance.work_order LIMIT 50"
 ]
}

WRITES = {
 "acceptVenueLabelProposals": [
  "SELECT id FROM venuemap.point ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "acceptWalkwayProposals": [
  "SELECT id FROM venuemap.path ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM venuemap.point ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "acceptWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "adjustGameCard": [
  "SELECT card_code FROM games.card ORDER BY card_code LIMIT 1 FOR UPDATE"
 ],
 "attachWorkOrderEvidence": [
  "SELECT id FROM maintenance.work_order_attachment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "bookResource": [
  "SELECT id FROM resources.booking ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "callNextParties": [
  "SELECT id FROM queue.queue ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "checkInResource": [
  "SELECT id FROM orders.stored_value_authorisation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM resources.booking ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "checkOutResource": [
  "SELECT id FROM orders.stored_value_authorisation WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM resources.booking ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closeWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "completeUpload": [
  "SELECT id FROM assets.media_asset ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "completeWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "configureQueueFeed": [
  "SELECT id FROM queue.feed ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createAsset": [
  "SELECT id FROM maintenance.asset ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createCollection": [
  "SELECT id FROM assets.media_collection ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createGame": [
  "SELECT id FROM games.game ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createInspectionTemplate": [
  "SELECT id FROM maintenance.inspection_template ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createMaintenancePlan": [
  "SELECT id FROM maintenance.maintenance_plan ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPrize": [
  "SELECT id FROM games.prize ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createQueue": [
  "SELECT id FROM queue.queue ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createResource": [
  "SELECT id FROM resources.resource WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createUpload": [
  "SELECT id FROM assets.media_upload ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createVenueMap": [
  "SELECT id FROM venuemap.map WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deleteMediaAsset": [
  "SELECT id FROM assets.media_usage ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "importVenueGeometry": [
  "SELECT id FROM venuemap.import_job ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM venuemap.path ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "issueGameCard": [
  "SELECT card_code FROM games.card ORDER BY card_code LIMIT 1 FOR UPDATE"
 ],
 "joinQueue": [
  "SELECT id FROM queue.waiting_guest ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "leaveQueue": [
  "SELECT id FROM queue.waiting_guest ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "loadGameCredits": [
  "SELECT card_code FROM games.card ORDER BY card_code LIMIT 1 FOR UPDATE"
 ],
 "overrideWaitingGuest": [
  "SELECT id FROM queue.waiting_guest ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "pauseWorkOrder": [
  "SELECT id FROM inventory.requisition ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "publishVenueMap": [
  "SELECT id FROM venuemap.map WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordAuthorityNotification": [
  "SELECT id FROM maintenance.incident ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordGamePlay": [
  "SELECT play_id FROM games.play ORDER BY play_id LIMIT 1 FOR UPDATE"
 ],
 "recordWorkOrderParts": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordWorkOrderTime": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "redeemPrize": [
  "SELECT id FROM games.redemption ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "redeemWaitingGuest": [
  "SELECT id FROM queue.waiting_guest ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rejectWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reorderSessionManifest": [
  "SELECT id FROM resources.session_participant ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "replaceMediaAsset": [
  "SELECT id FROM assets.media_asset ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reportIncident": [
  "SELECT id FROM maintenance.incident ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "resumeWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAssetStatus": [
  "SELECT id FROM maintenance.asset ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setPathClosure": [
  "SELECT id FROM venuemap.map WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM venuemap.path ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setQueueStatus": [
  "SELECT id FROM queue.queue ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setReaderProfile": [
  "SELECT id FROM games.reader_profile WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setResourceQualifications": [
  "SELECT id FROM resources.qualification WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setVenuePoint": [
  "SELECT id FROM venuemap.point ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setWaitTime": [
  "SELECT id FROM queue.queue ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "startWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "submitInspection": [
  "SELECT id FROM maintenance.inspection ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "submitQueueReading": [
  "SELECT id FROM queue.reading ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "syncGamePlays": [
  "SELECT id FROM games.credit_ledger ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT play_id FROM games.play ORDER BY play_id LIMIT 1 FOR UPDATE"
 ],
 "testQueueFeed": [
  "SELECT id FROM queue.reading ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "transferGameCard": [
  "SELECT card_code FROM games.card ORDER BY card_code LIMIT 1 FOR UPDATE"
 ],
 "updateAsset": [
  "SELECT id FROM maintenance.asset ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateGame": [
  "SELECT id FROM games.game ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateIncident": [
  "SELECT id FROM maintenance.incident ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateMaintenancePlan": [
  "SELECT id FROM maintenance.maintenance_plan ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateMediaAsset": [
  "SELECT id FROM assets.media_asset ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateQueue": [
  "SELECT id FROM queue.queue ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "verifyWorkOrder": [
  "SELECT id FROM maintenance.work_order ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "acceptVenueLabelProposals": [
  "cache:idempotency:bench"
 ],
 "acceptWalkwayProposals": [
  "cache:idempotency:bench"
 ],
 "acceptWorkOrder": [
  "cache:idempotency:bench"
 ],
 "adjustGameCard": [
  "cache:idempotency:bench"
 ],
 "attachWorkOrderEvidence": [
  "cache:idempotency:bench"
 ],
 "bookResource": [
  "cache:idempotency:bench"
 ],
 "callNextParties": [
  "cache:idempotency:bench"
 ],
 "cancelWorkOrder": [
  "cache:idempotency:bench"
 ],
 "checkInResource": [
  "cache:idempotency:bench"
 ],
 "checkOutResource": [
  "cache:idempotency:bench"
 ],
 "closeWorkOrder": [
  "cache:idempotency:bench"
 ],
 "completeUpload": [
  "cache:idempotency:bench"
 ],
 "completeWorkOrder": [
  "cache:idempotency:bench"
 ],
 "configureQueueFeed": [
  "cache:idempotency:bench"
 ],
 "createAsset": [
  "cache:idempotency:bench"
 ],
 "createCollection": [
  "cache:idempotency:bench"
 ],
 "createGame": [
  "cache:idempotency:bench"
 ],
 "createInspectionTemplate": [
  "cache:idempotency:bench"
 ],
 "createMaintenancePlan": [
  "cache:idempotency:bench"
 ],
 "createPrize": [
  "cache:idempotency:bench"
 ],
 "createQueue": [
  "cache:idempotency:bench"
 ],
 "createResource": [
  "cache:idempotency:bench"
 ],
 "createUpload": [
  "cache:idempotency:bench"
 ],
 "createVenueMap": [
  "cache:idempotency:bench"
 ],
 "createWorkOrder": [
  "cache:idempotency:bench"
 ],
 "deleteMediaAsset": [
  "cache:idempotency:bench"
 ],
 "getVenueMapGraph": [
  "cache:resolution:bench"
 ],
 "importVenueGeometry": [
  "cache:idempotency:bench"
 ],
 "issueGameCard": [
  "cache:idempotency:bench"
 ],
 "joinQueue": [
  "cache:idempotency:bench"
 ],
 "leaveQueue": [
  "cache:idempotency:bench"
 ],
 "loadGameCredits": [
  "cache:idempotency:bench"
 ],
 "overrideWaitingGuest": [
  "cache:idempotency:bench"
 ],
 "pauseWorkOrder": [
  "cache:idempotency:bench"
 ],
 "publishVenueMap": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "recordAuthorityNotification": [
  "cache:idempotency:bench"
 ],
 "recordGamePlay": [
  "cache:idempotency:bench"
 ],
 "recordWorkOrderParts": [
  "cache:idempotency:bench"
 ],
 "recordWorkOrderTime": [
  "cache:idempotency:bench"
 ],
 "redeemPrize": [
  "cache:idempotency:bench"
 ],
 "redeemWaitingGuest": [
  "cache:idempotency:bench"
 ],
 "rejectWorkOrder": [
  "cache:idempotency:bench"
 ],
 "reorderSessionManifest": [
  "cache:idempotency:bench"
 ],
 "replaceMediaAsset": [
  "cache:idempotency:bench"
 ],
 "reportIncident": [
  "cache:idempotency:bench"
 ],
 "resumeWorkOrder": [
  "cache:idempotency:bench"
 ],
 "setAssetStatus": [
  "cache:idempotency:bench"
 ],
 "setPathClosure": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setQueueStatus": [
  "cache:idempotency:bench"
 ],
 "setReaderProfile": [
  "cache:idempotency:bench"
 ],
 "setResourceQualifications": [
  "cache:idempotency:bench"
 ],
 "setVenuePoint": [
  "cache:idempotency:bench"
 ],
 "setWaitTime": [
  "cache:idempotency:bench"
 ],
 "startWorkOrder": [
  "cache:idempotency:bench"
 ],
 "submitInspection": [
  "cache:idempotency:bench"
 ],
 "submitQueueReading": [
  "cache:idempotency:bench"
 ],
 "testQueueFeed": [
  "cache:idempotency:bench"
 ],
 "transferGameCard": [
  "cache:idempotency:bench"
 ],
 "updateAsset": [
  "cache:idempotency:bench"
 ],
 "updateGame": [
  "cache:idempotency:bench"
 ],
 "updateIncident": [
  "cache:idempotency:bench"
 ],
 "updateMaintenancePlan": [
  "cache:idempotency:bench"
 ],
 "updateMediaAsset": [
  "cache:idempotency:bench"
 ],
 "updateQueue": [
  "cache:idempotency:bench"
 ],
 "updateWorkOrder": [
  "cache:idempotency:bench"
 ],
 "verifyWorkOrder": [
  "cache:idempotency:bench"
 ]
}
