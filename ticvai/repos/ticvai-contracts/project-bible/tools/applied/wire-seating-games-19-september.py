#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire seating boards 2–13 and the whole Game & Ride module.

**Seating was the contract that taught the join-versus-drift test, and it was only half
answered.** The 19 September wiring took boards 1–4 of the seat pack from 119 unserved
to 22 wired, and left 97 screens across boards 5 to 13 — holds, seat rules, group
bookings, recommendation governance, pricing, reporting, platform and integration.

Boards 6 to 9 needed authoring and got 19 operations. **Boards 10 to 13 needed none:**

    b10  dynamic pricing        -> `catalogue`, which already prices by demand
    b11  occupancy reporting    -> `reporting`, whose KPI and dashboard layer landed
                                   earlier today
    b12  platform configuration -> `tenancy` and `identity`
    b13  API and webhooks       -> `public-api`

**Game & Ride is the reverse case: 14 operations against 100 screens.** It got 23. Its
wallet board is not wired to `games` at all — the 19 September supersession decision put
the five configuration screens behind the wallet pack and kept the five operating ones
here, and `wallet` now exists to receive them.

Readers are `tenancy` devices with a game configuration, exactly as payment terminals
are. Three packs now share that shape, which is the sign it was the right one.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

F = 'screens/P08-venue-back-office.yaml'

S, C, R, T, I, P, A, W, G, M, O = ('seating', 'catalogue', 'reporting', 'tenancy',
                                   'identity', 'public-api', 'approvals', 'wallet',
                                   'games', 'maintenance', 'orders')

WIRING = {
    # ---------------------------------------------- seating b2: AI import review
    'BO-967': [('getSeatMapImport', S, 'What the import recognised', 'onLoad'),
               ('validateSeatMap', S, 'Correct and confirm', 'onAction')],
    'BO-968': [('getSeatMapImport', S, 'Rows and seats recognised', 'onLoad'),
               ('updateSeats', S, 'Correct them', 'onAction')],
    'BO-969': [('getSeatMapImport', S, 'Aisles, VIP and accessible areas', 'onLoad'),
               ('setMapZones', S, 'Correct the zones', 'onAction')],
    'BO-970': [('updateSeats', S, 'Numbering and labelling', 'onAction')],

    # ---------------------------------------------- seating b3: layouts
    'BO-973': [('listSeatMaps', S, 'Layouts in use', 'onLoad')],
    'BO-975': [('getSeatMap', S, 'The layout for this event', 'onLoad'),
               ('publishSeatMap', S, 'Publish it', 'onAction')],
    'BO-978': [('listSeatMaps', S, 'Maps available', 'onLoad'),
               ('publishSeatMap', S, 'Assign to performances', 'onAction')],
    'BO-979': [('createSeatHoldPool', S, 'Block seats temporarily', 'onAction'),
               ('listSeatHoldPools', S, 'What is blocked', 'onLoad')],
    'BO-980': [('releaseSeatHoldPool', S, 'Scheduled release', 'onAction'),
               ('listSeatHoldTypes', S, 'The release rules', 'onLoad')],

    # ---------------------------------------------- seating b4: inventory
    'BO-983': [('getSeatInventory', S, 'Every seat state', 'onLoad')],
    'BO-984': [('getSeatInventory', S, 'The live map', 'onLoad')],
    'BO-986': [('getSeatAvailability', S, 'What is free', 'onLoad')],
    'BO-987': [('listSeatBlocks', S, 'Holds in force', 'onLoad'),
               ('getSeatHold', S, 'One hold', 'onLoad')],
    'BO-988': [('getSeatInventory', S, 'Reserved against sold', 'onLoad')],
    'BO-989': [('getSeatInventory', S, 'Sales and allocation', 'onLoad'),
               ('listSeatHoldPools', S, 'Allocation pools', 'onLoad')],
    'BO-990': [('createSeatBlock', S, 'Take a seat out of service', 'onAction'),
               ('createWorkOrder', M, 'Raise the repair', 'onAction')],
    'BO-992': [('getSeatReconciliation', S, 'The map against the orders', 'onLoad')],

    # ---------------------------------------------- seating b5: guest selection
    'BO-994': [('getSeatAvailability', S, 'What the guest can choose', 'onLoad'),
               ('createSeatHold', S, 'Hold the selection', 'onAction')],
    'BO-996': [('getSeatAvailability', S, 'Filtered availability', 'onLoad')],
    'BO-998': [('extendSeatHold', S, 'Extend before it lapses', 'onAction'),
               ('relinquishSeatHold', S, 'Release on abandonment', 'onAction')],
    'BO-999': [('getSeatHold', S, 'What is in the cart', 'onLoad'),
               ('relinquishSeatHold', S, 'Remove one', 'onAction')],
    'BO-1000': [('getSeatAvailability', S, 'Accessible and mobile selection', 'onLoad'),
                ('getAccessibleSeating', S, 'Which seats and routes', 'onLoad')],
    'BO-1001': [('recommendSeats', S, 'Compare and preview', 'onAction')],
    'BO-1002': [('recommendSeats', S, 'What the assistant proposes', 'onAction')],

    # ---------------------------------------------- seating b6: holds
    'BO-1003': [('listSeatHoldPools', S, 'Pools and their utilisation', 'onLoad')],
    'BO-1004': [('listSeatHoldTypes', S, 'Hold kinds', 'onLoad'),
                ('setSeatHoldType', S, 'Define one', 'onAction')],
    'BO-1005': [('createSeatHoldPool', S, 'Create a pool', 'onAction')],
    'BO-1006': [('setSeatHoldType', S, 'Which rule applies where', 'onAction')],
    'BO-1007': [('setSeatHoldType', S, 'Expiration rules', 'onAction')],
    'BO-1008': [('releaseSeatHoldPool', S, 'Automatic release', 'onAction')],
    'BO-1009': [('releaseSeatHoldPool', S, 'Release, convert or reassign', 'onAction')],
    'BO-1010': [('createApprovalRequest', A, 'Send a hold for approval', 'onAction'),
                ('listSeatHoldPools', S, 'What is being requested', 'onLoad')],
    'BO-1011': [('listSeatHoldPools', S, 'Competing holds', 'onLoad'),
                ('setSeatHoldType', S, 'Priority between kinds', 'onAction')],
    'BO-1012': [('listSeatHoldPools', S, 'Utilisation and audit', 'onLoad')],

    # ---------------------------------------------- seating b7: seat rules
    'BO-1013': [('getSeatRules', S, 'Rules in force', 'onLoad')],
    'BO-1014': [('setSeatRules', S, 'Kill a seat, with a reason', 'onAction')],
    'BO-1015': [('setSeatRules', S, 'Buffer seats around a sale', 'onAction')],
    'BO-1016': [('setSeatRules', S, 'Companion pairing', 'onAction')],
    'BO-1017': [('setSeatRules', S, 'Wheelchair companion rules', 'onAction'),
                ('getAccessibleSeating', S, 'The spaces being paired', 'onLoad')],
    'BO-1018': [('getAccessibleSeating', S, 'The accessible inventory', 'onLoad'),
                ('setAccessibleSeating', S, 'Define it', 'onAction')],
    'BO-1019': [('setAccessibleSeating', S, 'Routes to each space', 'onAction')],
    'BO-1020': [('setAccessibleSeating', S, 'Who may buy them', 'onAction')],
    'BO-1021': [('setSeatRules', S, 'Flexible spacing and density', 'onAction')],
    'BO-1022': [('validateSeatCompliance', S, 'Whether the map still complies', 'onLoad')],

    # ---------------------------------------------- seating b8: groups
    'BO-1023': [('listGroupSeatRequests', S, 'Group bookings', 'onLoad')],
    'BO-1024': [('listGroupSeatRequests', S, 'By group type', 'onLoad')],
    'BO-1025': [('createGroupSeatRequest', S, 'Record an enquiry', 'onAction')],
    'BO-1026': [('allocateGroupSeats', S, 'Find the best block', 'onAction')],
    'BO-1027': [('allocateGroupSeats', S, 'Allocate in bulk', 'onAction')],
    'BO-1028': [('setGroupSeatRoster', S, 'Names to seats', 'onAction')],
    'BO-1029': [('listGroupSeatRequests', S, 'The quote', 'onLoad'),
                ('recordDeposit', 'finance', 'Take the deposit', 'onAction')],
    'BO-1030': [('releaseSeatHoldPool', S, 'Release on cancellation', 'onAction'),
                ('listGroupSeatRequests', S, 'The booking being changed', 'onLoad')],
    'BO-1031': [('createApprovalRequest', A, 'Contract approval', 'onAction')],
    'BO-1032': [('listGroupSeatRequests', S, 'Group reporting', 'onLoad')],

    # ---------------------------------------------- seating b9: recommendations
    'BO-1033': [('getSeatRecommendationRules', S, 'Scoring in force', 'onLoad')],
    'BO-1034': [('setSeatRecommendationRules', S, 'What "best seat" means here', 'onAction')],
    'BO-1035': [('setSeatRecommendationRules', S, 'Best value weighting', 'onAction')],
    'BO-1036': [('setSeatRecommendationRules', S, 'Closest to stage', 'onAction')],
    'BO-1037': [('setSeatRecommendationRules', S, 'Family together', 'onAction')],
    'BO-1038': [('setSeatRecommendationRules', S, 'Accessible recommendations', 'onAction'),
                ('getAccessibleSeating', S, 'The accessible inventory', 'onLoad')],
    'BO-1039': [('recommendSeats', S, 'Upgrade options', 'onAction')],
    'BO-1040': [('reassignSeats', S, 'Move a party, and tell them', 'onAction')],
    'BO-1041': [('setSeatRecommendationRules', S, 'Scoring and governance', 'onAction')],
    'BO-1042': [('getSeatRecommendationRules', S, 'Performance and feedback', 'onLoad')],

    # ------------------------------- seating b10: pricing — a join to catalogue
    'BO-1044': [('listDynamicPricingStrategy', C, 'Dynamic pricing in force', 'onLoad')],
    'BO-1045': [('listSeatCategories', S, 'Price bands against categories', 'onLoad'),
                ('createSeatCategory', S, 'Add a band', 'onAction')],
    'BO-1046': [('listDemandBookingCurve', C, 'Forecast against the curve', 'onLoad')],
    'BO-1047': [('listDemandBookingCurve', C, 'By section', 'onLoad')],
    'BO-1048': [('getRecommendations', 'promotions', 'Seat upsell offers', 'onAction')],
    'BO-1049': [('simulatePriceBreakdownCalculation', C, 'What-if on price', 'onAction')],

    # ------------------------------ seating b11: reporting — a join to reporting
    'BO-1052': [('getKpiValues', R, 'Occupancy KPIs', 'onLoad')],
    'BO-1053': [('getKpiValues', R, 'By zone', 'onLoad')],
    'BO-1054': [('getKpiValues', R, 'Revenue by section', 'onLoad')],
    'BO-1056': [('getKpiValues', R, 'Seat utilisation', 'onLoad')],
    'BO-1058': [('listDemandBookingCurve', C, 'Sales pace and pick curve', 'onLoad')],
    'BO-1059': [('getSeatInventory', S, 'The map behind the heat', 'onLoad'),
                ('runReport', R, 'Drill down', 'onAction')],
    'BO-1060': [('createReport', R, 'Build a seat report', 'onAction'),
                ('exportReportResult', R, 'Export it', 'onAction')],

    # --------------------- seating b12: platform — a join to tenancy and identity
    'BO-1061': [('listVenueMaps', 'venue-map', 'Venues and their maps', 'onLoad'),
                ('listSeatMaps', S, 'Seat maps across them', 'onLoad')],
    'BO-1062': [('getOrgUnit', T, 'Tenant and brand context', 'onLoad')],
    'BO-1063': [('getVenueSettings', T, 'Venue configuration', 'onLoad'),
                ('setVenueSettings', T, 'Change it', 'onAction')],
    'BO-1064': [('updateSeats', S, 'Naming and numbering', 'onAction'),
                ('getRegionSettings', T, 'Localisation', 'onLoad')],
    'BO-1065': [('updateRegionSettings', T, 'Currency, timezone and channels', 'onAction')],
    'BO-1066': [('listAccessPolicies', I, 'Who may see and change what', 'onLoad'),
                ('createAccessPolicy', I, 'Write a policy', 'onAction')],
    'BO-1067': [('setVisualWorkflow', A, 'Seat approval workflows', 'onAction')],
    'BO-1068': [('deployConfigurationProfile', T, 'Promote configuration', 'onAction')],
    'BO-1069': [('getWorkstationHealth', T, 'Platform health', 'onLoad')],
    'BO-1070': [('cloneSeatMap', S, 'Clone a map into a new venue', 'onAction'),
                ('setConfigurationProfile', T, 'Inherited settings', 'onAction')],

    # ------------------------- seating b13: integration — a join to public-api
    'BO-1071': [('listApiClients', P, 'Integrations connected', 'onLoad')],
    'BO-1072': [('listSeatMaps', S, 'What the seat API exposes', 'onLoad')],
    'BO-1073': [('listApiClients', P, 'Access and OAuth', 'onLoad'),
                ('createApiClient', P, 'Issue credentials', 'onAction')],
    'BO-1074': [('listWebhookSubscriptions', P, 'Webhooks configured', 'onLoad'),
                ('createWebhookSubscription', P, 'Subscribe', 'onAction')],
    'BO-1075': [('listApiVersions', P, 'The seat event catalogue', 'onLoad')],
    'BO-1076': [('listApiClients', P, 'Limits and idempotency', 'onLoad')],
    'BO-1077': [('listWebhookSubscriptions', P, 'Mapping and transformation', 'onLoad')],
    'BO-1078': [('listWebhookDeliveries', P, 'Delivery, retry and reconciliation', 'onLoad')],
    'BO-1079': [('getSeatReconciliation', S, 'Seat audit', 'onLoad')],
    'BO-1080': [('createApprovalRequest', A, 'Integration approval', 'onAction')],

    # ================================================== Game & Ride, board 1
    'BO-394': [('listGames', G, 'Games and rides today', 'onLoad'),
               ('listGameplayTransactions', G, 'Live taps', 'onLoad')],
    'BO-395': [('listGames', G, 'The directory', 'onLoad')],
    'BO-396': [('getGameCard', G, 'The attraction profile', 'onLoad'),
               ('updateGame', G, 'Change it', 'onAction')],
    'BO-397': [('listAttractionTypes', G, 'Types defined', 'onLoad'),
               ('setAttractionType', G, 'Define one', 'onAction')],
    'BO-398': [('setGameOperationalConfiguration', G, 'Cycle, capacity and restrictions',
                'onAction')],
    'BO-399': [('setCreditEligibilityRules', W, 'Where credit may be spent', 'onAction')],
    'BO-400': [('listReaders', G, 'Readers on this attraction', 'onLoad'),
               ('setReaderConfiguration', G, 'Assign one', 'onAction')],
    'BO-401': [('listGameEntitlements', G, 'Packages and entitlements', 'onLoad'),
               ('createGameEntitlement', G, 'Associate one', 'onAction')],
    'BO-402': [('simulateGameplayAuthorisation', G, 'Would a tap work here', 'onAction')],
    'BO-403': [('listGameplayTransactions', G, 'Audit and governed actions', 'onLoad')],

    # ------------------------------------------------- Game & Ride, board 2
    'BO-404': [('listReaders', G, 'Readers and their health', 'onLoad')],
    'BO-405': [('listReaders', G, 'The directory', 'onLoad')],
    'BO-407': [('setReaderConfiguration', G, 'Profile and device setup', 'onAction'),
               ('enrolDevice', T, 'Enrol the device behind it', 'onAction')],
    'BO-408': [('setReaderConfiguration', G, 'Credit and payment acceptance', 'onAction')],
    'BO-409': [('setReaderConfiguration', G, 'Which attraction it opens', 'onAction')],
    'BO-410': [('setReaderConfiguration', G, 'Retap delay', 'onAction')],
    'BO-411': [('setReaderConfiguration', G, 'Free-game glow and display', 'onAction')],
    'BO-412': [('setReaderConfiguration', G, 'Theme and experience', 'onAction')],
    'BO-413': [('testReader', G, 'Balance check and device test', 'onAction')],

    # ----------------------- Game & Ride, board 3: wallet, per the supersession
    'BO-414': [('getWallet', 'retail', 'The game credit balance', 'onLoad'),
               ('listWalletTransactions', 'retail', 'Recent movement', 'onLoad')],
    'BO-416': [('getWallet', 'retail', 'Account and balance', 'onLoad'),
               ('listCreditLots', W, 'The lots behind it', 'onLoad')],
    'BO-419': [('setCreditEligibilityRules', W, 'Bonus usage restrictions', 'onAction')],
    'BO-421': [('listGameEntitlements', G, 'Free game and ride credit', 'onLoad'),
               ('createGameEntitlement', G, 'Grant free play', 'onAction')],
    'BO-422': [('adjustWallet', 'retail', 'Refund, adjust or grant bonus', 'onAction')],
    'BO-423': [('listWalletTransactions', 'retail', 'The credit ledger', 'onLoad')],

    # ------------------------------------------------- Game & Ride, board 4
    'BO-424': [('getGameplayValidationRules', G, 'Rules in force', 'onLoad'),
               ('listGameplayTransactions', G, 'What they produced', 'onLoad')],
    'BO-425': [('setGameplayValidationRules', G, 'What a tap is checked against', 'onAction')],
    'BO-426': [('setGameplayValidationRules', G, 'Deduction priority', 'onAction')],
    'BO-427': [('createGameEntitlement', G, 'An all-games pass', 'onAction')],
    'BO-428': [('createGameEntitlement', G, 'Unlimited on one game', 'onAction')],
    'BO-429': [('createGameEntitlement', G, 'A limited number of plays', 'onAction')],
    'BO-430': [('createGameEntitlement', G, 'Build a package', 'onAction'),
               ('listGameEntitlements', G, 'Existing packages', 'onLoad')],
    'BO-431': [('createGameEntitlement', G, 'Validity and activation', 'onAction')],
    'BO-432': [('authoriseGameplay', G, 'Authorise a tap', 'onAction')],
    'BO-433': [('simulateGameplayAuthorisation', G, 'Simulate and analyse exceptions', 'onAction')],

    # ------------------------------------------------- Game & Ride, board 5
    'BO-434': [('getGamePricing', G, 'Effective prices', 'onLoad')],
    'BO-435': [('setGamePricing', G, 'Standard price', 'onAction')],
    'BO-436': [('setGamePricing', G, 'Group pricing', 'onAction')],
    'BO-437': [('setGamePricing', G, 'Peak and off-peak', 'onAction')],
    'BO-438': [('setGamePricing', G, 'Calendar and exception dates', 'onAction')],
    'BO-439': [('setGamePricing', G, 'Normal and VIP', 'onAction')],
    'BO-440': [('setGamePricing', G, 'Retry price', 'onAction')],
    'BO-442': [('getGamePricing', G, 'What the reader will charge', 'onLoad')],

    # ------------------------------------------------- Game & Ride, board 6
    'BO-445': [('listPrizes', G, 'Redemption operations', 'onLoad')],
    'BO-446': [('setRedemptionRules', G, 'How tickets are earned', 'onAction')],
    'BO-447': [('setRedemptionRules', G, 'Ticket-eater integration', 'onAction')],
    'BO-448': [('getWallet', 'retail', 'Redemption balance', 'onLoad')],
    'BO-449': [('setRedemptionRules', G, 'Ticketless redemption', 'onAction')],
    'BO-450': [('redeemPrize', G, 'Hand over a prize', 'onAction'),
               ('listPrizes', G, 'The prize catalogue', 'onLoad')],
    'BO-451': [('setPrizeCost', G, 'Ticket price and unit cost', 'onAction'),
               ('createPrize', G, 'Add a prize', 'onAction')],
    'BO-452': [('getStockPositions', 'inventory', 'Prize stock', 'onLoad')],
    'BO-453': [('setPrizeCost', G, 'Direct-pay price', 'onAction')],

    # ------------------------------------------------- Game & Ride, board 7
    'BO-454': [('getGameCard', G, 'Cards in circulation', 'onLoad')],
    'BO-455': [('getGameCard', G, 'The card profile', 'onLoad')],
    'BO-456': [('setGameCardExpiryRules', G, 'When a card lapses', 'onAction')],
    'BO-457': [('getGameCard', G, 'Last recharge and activity', 'onLoad')],
    'BO-458': [('setGameCardExpiryRules', G, 'Warnings before expiry', 'onAction')],
    'BO-459': [('authoriseGameplay', G, 'Expiry checked at the reader', 'onAction')],
    'BO-460': [('setGameCardLifecycle', G, 'Block, suspend or reactivate', 'onAction')],
    'BO-461': [('setGameCardLifecycle', G, 'Replace and relink', 'onAction'),
               ('linkWalletCredential', W, 'Bind the new credential', 'onAction')],
    'BO-462': [('getGameCard', G, 'Balance and credential status', 'onLoad')],
    'BO-463': [('listGameplayTransactions', G, 'Card lifecycle history', 'onLoad')],

    # ------------------------------------------------- Game & Ride, board 8
    'BO-464': [('listGameplayTransactions', G, 'Live operations', 'onLoad')],
    'BO-465': [('listGameplayTransactions', G, 'Every tap', 'onLoad')],
    'BO-466': [('listReaders', G, 'Reader and device health', 'onLoad'),
               ('getDeviceTelemetry', T, 'Telemetry behind it', 'onLoad')],
    'BO-467': [('simulateGameplayAuthorisation', G, 'Trace a decision', 'onAction')],
    'BO-468': [('listGameplayTransactions', G, 'Refusals, by reason', 'onLoad')],
    'BO-470': [('listGameEntitlements', G, 'Entitlement consumption', 'onLoad')],
    'BO-471': [('getGameplaySyncStatus', G, 'What is held offline', 'onLoad')],
    'BO-472': [('listAlerts', R, 'Operational alerts', 'onLoad')],
    'BO-473': [('getGameplaySyncStatus', G, 'Reconciliation', 'onLoad')],

    # ------------------------------------------------- Game & Ride, board 9
    'BO-474': [('listReaders', G, 'Integrations by reader', 'onLoad')],
    'BO-475': [('setReaderProfile', G, 'Manufacturer and model', 'onAction')],
    'BO-476': [('setReaderProfile', G, 'Communication protocol', 'onAction')],
    'BO-477': [('setReaderConfiguration', G, 'Command and event mapping', 'onAction')],
    'BO-478': [('deployReaderConfiguration', G, 'Deploy and synchronise', 'onAction')],
    'BO-479': [('setReaderConfiguration', G, 'Trigger and I/O mapping', 'onAction')],
    'BO-480': [('setReaderConfiguration', G, 'Screen, LED and sound', 'onAction')],
    'BO-481': [('deployReaderConfiguration', G, 'Edge cache and offline package', 'onAction')],
    'BO-482': [('testReader', G, 'Diagnostics', 'onAction')],

    # ------------------------------------------------ Game & Ride, board 10
    'BO-484': [('getGameEligibility', G, 'Self-service overview', 'onLoad')],
    'BO-485': [('setGameKioskConfiguration', G, 'Kiosk profile and channel', 'onAction')],
    'BO-489': [('getGameEligibility', G, 'Bonus, free game and benefits', 'onLoad')],
    'BO-490': [('getGameEligibility', G, 'What can I play', 'onLoad')],
    'BO-493': [('setGameKioskConfiguration', G, 'Theme, language and journey', 'onAction')],
}

INVALIDATES = {
    'setSeatHoldType': ['listSeatHoldTypes'],
    'createSeatHoldPool': ['listSeatHoldPools', 'getSeatInventory', 'getSeatAvailability'],
    'releaseSeatHoldPool': ['listSeatHoldPools', 'getSeatInventory', 'getSeatAvailability'],
    'setSeatRules': ['getSeatRules', 'getSeatInventory'],
    'setAccessibleSeating': ['getAccessibleSeating', 'validateSeatCompliance'],
    'createGroupSeatRequest': ['listGroupSeatRequests'],
    'allocateGroupSeats': ['listGroupSeatRequests', 'getSeatInventory'],
    'setGroupSeatRoster': ['listGroupSeatRequests'],
    'setSeatRecommendationRules': ['getSeatRecommendationRules'],
    'reassignSeats': ['getSeatInventory', 'getSeatReconciliation'],
    'createSeatBlock': ['getSeatInventory', 'listSeatBlocks'],
    'setAttractionType': ['listAttractionTypes'],
    'setGameOperationalConfiguration': ['listGames'],
    'setReaderConfiguration': ['listReaders'],
    'deployReaderConfiguration': ['listReaders', 'getGameplaySyncStatus'],
    'createGameEntitlement': ['listGameEntitlements'],
    'setGameplayValidationRules': ['getGameplayValidationRules'],
    'authoriseGameplay': ['listGameplayTransactions', 'getGameCard'],
    'setGamePricing': ['getGamePricing'],
    'setRedemptionRules': ['listPrizes'],
    'setPrizeCost': ['listPrizes'],
    'setGameCardLifecycle': ['getGameCard'],
    'setGameCardExpiryRules': ['getGameCard'],
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
