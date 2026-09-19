#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire the 191 unserved rental and resource board screens.

Two packs, 199 screens, 191 of them calling nothing. `tools/scope-pack-to-contracts.py`
scored every one against every operation in all thirty contracts and found **150 with no
candidate anywhere** — the verdict survived three successive repairs to the matcher, so
it is the contracts that were absent rather than the matcher that was blind.

**But not every board here was a gap, and that is the part worth getting right.**

    rental board 9   maintenance   36 operations already exist — work orders,
                                   inspections, parts, return-to-service. A join.
    rental board 2   inventory     serialised registry, pooled stock, transfers,
                                   adjustments. Mostly a join.
    resource b3/b4   workforce     rotas, attendance, shift marketplace, labour cost.
                                   Partly a join; `workforce` is thin and the rest is
                                   left open rather than invented here.
    resource b7      catalogue     event resource planning — waits for Phase 4.4.
    resource b8      ai            held back; the AI boards are not complete.

So this wires three kinds of thing: new `resources` operations to the resource master and
calendar boards, new `rental` operations to the rental lifecycle boards, and **existing
operations in other contracts to the boards that were always theirs.**

Idempotent — a screen that already declares an operation keeps it.
Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

F = 'screens/P08-venue-back-office.yaml'

# screen -> [(operationId, contract, purpose, trigger)]
WIRING = {
    # ---------------------------------------------- resources, board 1: the master
    'BO-854': [('listResourceTypes', 'resources', 'Resources by type', 'onLoad'),
               ('getResourceUtilisation', 'resources', 'Utilisation across the estate', 'onLoad')],
    'BO-855': [('listResourceTypes', 'resources', 'The classes defined so far', 'onLoad'),
               ('createResourceType', 'resources', 'Define a class', 'onAction'),
               ('updateResourceType', 'resources', 'Change a class', 'onAction')],
    'BO-856': [('listResourceCategories', 'resources', 'The classification tree', 'onLoad'),
               ('createResourceCategory', 'resources', 'Add a category', 'onAction'),
               ('updateResourceCategory', 'resources', 'Change a category', 'onAction')],
    'BO-857': [('getResource', 'resources', 'The resource being edited', 'onLoad'),
               ('createResource', 'resources', 'Create it', 'onAction'),
               ('updateResource', 'resources', 'Save the profile', 'onAction'),
               ('setResourceLifecycleState', 'resources', 'Submit, activate, suspend or retire',
                'onAction'),
               ('cloneResource', 'resources', 'Copy it', 'onAction')],
    'BO-858': [('listResourceAttributes', 'resources', 'Attributes defined so far', 'onLoad'),
               ('createResourceAttribute', 'resources', 'Define an attribute', 'onAction')],
    'BO-859': [('getResourceHierarchy', 'resources', 'The tree', 'onLoad'),
               ('setResourceHierarchy', 'resources', 'Re-parent or attach', 'onAction')],
    'BO-860': [('getResourceDependencies', 'resources', 'Rules in force', 'onLoad'),
               ('setResourceDependencies', 'resources', 'Define what must come with it', 'onAction')],
    'BO-861': [('listResourcePackages', 'resources', 'The packages', 'onLoad'),
               ('createResourcePackage', 'resources', 'Define one', 'onAction'),
               ('updateResourcePackage', 'resources', 'Change one', 'onAction')],
    'BO-862': [('setResourceVenueAssignment', 'resources', 'Where it may operate', 'onAction'),
               ('getResource', 'resources', 'The resource being assigned', 'onLoad')],
    'BO-863': [('getResourceAuditTrail', 'resources', 'The immutable timeline', 'onLoad'),
               ('setResourceLifecycleState', 'resources', 'Move it through its lifecycle', 'onAction')],

    # ---------------------------------------------- resources, board 2: the calendar
    'BO-864': [('getResourceCalendar', 'resources', 'Every resource against time', 'onLoad'),
               ('bookResource', 'resources', 'Create a reservation from a free slot', 'onAction'),
               ('createResourceBlock', 'resources', 'Block a period', 'onAction')],
    'BO-865': [('getResourceCalendar', 'resources', 'The filtered grid', 'onLoad'),
               ('suggestResources', 'resources', 'Find one that matches', 'onAction')],
    'BO-866': [('getResourceSchedule', 'resources', 'The pattern as configured', 'onLoad'),
               ('setResourceSchedule', 'resources', 'Operating hours and working pattern', 'onAction')],
    'BO-867': [('setResourceSchedule', 'resources', 'Slot length and booking limits', 'onAction'),
               ('getResourceSchedule', 'resources', 'The current slots', 'onLoad')],
    'BO-868': [('listResourceBookings', 'resources', 'Reservations ahead', 'onLoad'),
               ('bookResource', 'resources', 'Reserve in advance', 'onAction'),
               ('updateResourceBooking', 'resources', 'Move or resize it', 'onAction')],
    'BO-869': [('bookResource', 'resources', 'Create the series', 'onAction'),
               ('cancelResourceBooking', 'resources', 'Cancel an occurrence or the series',
                'onAction')],
    'BO-870': [('listResourceBlocks', 'resources', 'Blocks in force', 'onLoad'),
               ('createResourceBlock', 'resources', 'Block a window', 'onAction'),
               ('releaseResourceBlock', 'resources', 'Put it back into service', 'onAction')],
    'BO-871': [('getResourceCalendar', 'resources', 'Several events at once', 'onLoad'),
               ('allocateResources', 'resources', 'Fill each requirement', 'onAction')],
    'BO-872': [('updateResourceBooking', 'resources', 'Drag to reassign, extend or shorten',
                'onAction'),
               ('getResourceCalendar', 'resources', 'The grid being dragged on', 'onLoad')],

    # ---------------------------------------------- resources, board 5: allocation
    'BO-893': [('getExperienceResourceRequirements', 'resources', 'What the experience needs',
                'onLoad'),
               ('setExperienceResourceRequirements', 'resources', 'Bind the requirements',
                'onAction')],
    'BO-894': [('setResourceQualifications', 'resources', 'What a person is certified to do',
                'onAction'),
               ('suggestResources', 'resources', 'Staff who qualify', 'onLoad')],
    'BO-895': [('listResourcePackages', 'resources', 'Existing combinations', 'onLoad'),
               ('createResourcePackage', 'resources', 'Build a combination', 'onAction')],
    'BO-896': [('getResourceUtilisation', 'resources', 'Capacity against demand', 'onLoad')],
    'BO-897': [('setResourceSelectionPolicy', 'resources',
                'Whether the guest may choose, per ticket type', 'onAction')],
    'BO-898': [('suggestResources', 'resources', 'Attribute matching, not a model', 'onLoad')],
    'BO-899': [('allocateResources', 'resources', 'Assign at the counter', 'onAction'),
               ('suggestResources', 'resources', 'What is free and suitable', 'onLoad')],
    'BO-900': [('allocateResources', 'resources', 'Allocate against the requirement', 'onAction'),
               ('getResourceAllocationPolicy', 'resources', 'The strategy in force', 'onLoad')],
    'BO-901': [('getResourceAllocationPolicy', 'resources', 'Rotation, priority and scoring',
                'onLoad'),
               ('setResourceAllocationPolicy', 'resources', 'Change the strategy', 'onAction')],
    'BO-902': [('replaceResourceAllocation', 'resources', 'Swap in an approved substitute',
                'onAction')],

    # ------------------------- resources, board 6: equipment — rental and maintenance
    'BO-903': [('listResources', 'resources', 'Equipment and assets', 'onLoad'),
               ('listAssets', 'maintenance', 'The asset register', 'onLoad')],
    'BO-904': [('getRentalProduct', 'rental', 'The rental product behind the resource', 'onLoad'),
               ('setRentalInventoryModel', 'rental', 'Pooled, serialised or hybrid', 'onAction')],
    'BO-905': [('getRentalAvailability', 'rental', 'What is free, with turnaround subtracted',
                'onLoad'),
               ('setRentalAvailabilityRules', 'rental', 'Buffers and release rules', 'onAction')],
    'BO-906': [('checkOutRental', 'rental', 'Hand it over', 'onAction'),
               ('getRentalBooking', 'rental', 'The booking being checked out', 'onLoad')],
    'BO-907': [('assignRentalEquipment', 'rental', 'Bind assets to the booking', 'onAction'),
               ('checkOutResource', 'resources', 'Hand the resource over', 'onAction')],
    'BO-908': [('extendRental', 'rental', 'Keep it longer', 'onAction'),
               ('returnRental', 'rental', 'Take it back and settle', 'onAction')],
    'BO-909': [('setRentalDepositPolicy', 'rental', 'How much is held, and how', 'onAction'),
               ('setRentalFeePolicy', 'rental', 'Grace period and late fees', 'onAction')],
    'BO-910': [('createResourceBlock', 'resources', 'Take it out of service', 'onAction'),
               ('createWorkOrder', 'maintenance', 'Raise the repair', 'onAction'),
               ('getDueMaintenance', 'maintenance', 'What is due', 'onLoad')],
    'BO-911': [('recordRentalInspection', 'rental', 'Condition, with evidence', 'onAction'),
               ('submitInspection', 'maintenance', 'The maintenance inspection', 'onAction'),
               ('listInspections', 'maintenance', 'Inspections so far', 'onLoad')],
    'BO-912': [('setResourceLifecycleState', 'resources', 'Retire or archive it', 'onAction'),
               ('getAssetHistory', 'maintenance', 'Its life so far', 'onLoad')],

    # ---------------------------------------------- resources, board 9: mobile staff
    'BO-933': [('listResourceBookings', 'resources', "Today's assignments", 'onLoad')],
    'BO-934': [('getResourceCalendar', 'resources', 'My schedule', 'onLoad')],
    'BO-935': [('getResource', 'resources', 'The resource for this assignment', 'onLoad'),
               ('listResourceBookings', 'resources', 'The assignment itself', 'onLoad')],
    'BO-936': [('recordAttendance', 'workforce', 'Check in or out', 'onAction')],
    'BO-937': [('checkOutResource', 'resources', 'Hand it over', 'onAction'),
               ('checkInResource', 'resources', 'Take it back', 'onAction')],
    'BO-939': [('requestShiftSwap', 'workforce', 'Swap, pick up or release', 'onAction'),
               ('listShiftSwapRequests', 'workforce', 'Requests outstanding', 'onLoad')],
    'BO-941': [('listAnnouncements', 'workforce', 'Live alerts and notices', 'onLoad')],

    # ---------------------------------------------- resources, board 10: analytics
    'BO-943': [('getResourceUtilisation', 'resources', 'Utilisation across the estate', 'onLoad')],
    'BO-944': [('getResourceUtilisation', 'resources', 'Utilisation and capacity', 'onLoad')],
    'BO-945': [('getResourceUtilisation', 'resources', 'Cost and efficiency against use', 'onLoad')],
    'BO-947': [('getResourceUtilisation', 'resources', 'The KPI base', 'onLoad')],
    'BO-948': [('getResourceAllocationPolicy', 'resources', 'Policy in force', 'onLoad'),
               ('setResourceAllocationPolicy', 'resources', 'Change it', 'onAction')],
    'BO-950': [('getResourceAuditTrail', 'resources', 'Decision history', 'onLoad')],

    # ---------------------------------------------- rental, board 1: the product
    'BO-494': [('listRentalProducts', 'rental', 'Products across venues', 'onLoad'),
               ('publishRentalProduct', 'rental', 'Activate, suspend or archive', 'onAction')],
    'BO-495': [('createRentalProduct', 'rental', 'Create the draft', 'onAction'),
               ('validateRentalProduct', 'rental', 'What is still missing', 'onAction')],
    'BO-496': [('getRentalProduct', 'rental', 'The master configuration', 'onLoad'),
               ('updateRentalProduct', 'rental', 'Save it', 'onAction')],
    'BO-497': [('listRentalCategories', 'rental', 'Categories and their defaults', 'onLoad'),
               ('createRentalCategory', 'rental', 'Define a category', 'onAction')],
    'BO-498': [('setRentalInventoryModel', 'rental', 'Pooled, serialised or hybrid', 'onAction')],
    'BO-499': [('setRentalProductLocations', 'rental', 'Where it is collected and returned',
                'onAction')],
    'BO-500': [('setRentalDurationRules', 'rental', 'Duration, increment and turnaround',
                'onAction')],
    'BO-501': [('setRentalOperationalRules', 'rental', 'Who may rent it, and what must happen',
                'onAction')],
    'BO-502': [('setRentalAgreementRequirements', 'rental', 'Agreement, waiver and signature',
                'onAction')],
    'BO-503': [('validateRentalProduct', 'rental', 'The readiness checklist', 'onLoad'),
               ('publishRentalProduct', 'rental', 'Submit, approve and publish', 'onAction')],

    # --------------------------- rental, board 2: serialised inventory — mostly inventory
    'BO-504': [('listInventoryItems', 'inventory', 'Stock across locations', 'onLoad'),
               ('getStockPositions', 'inventory', 'What is where', 'onLoad')],
    'BO-505': [('listSerialisedItems', 'inventory', 'Individually identified assets', 'onLoad'),
               ('listAssets', 'maintenance', 'The asset register behind them', 'onLoad')],
    'BO-506': [('getAsset', 'maintenance', 'The asset profile', 'onLoad'),
               ('updateAsset', 'maintenance', 'Change it', 'onAction')],
    'BO-507': [('getStockPositions', 'inventory', 'Pooled quantities', 'onLoad'),
               ('createStockMovement', 'inventory', 'Adjust the pool', 'onAction')],
    'BO-508': [('setAssetStatus', 'maintenance', 'Available, rented or faulty', 'onAction'),
               ('getAsset', 'maintenance', 'Current condition', 'onLoad')],
    'BO-509': [('lookupAsset', 'maintenance', 'Scan a QR or barcode', 'onAction')],
    'BO-510': [('listStockLocations', 'inventory', 'Where stock may sit', 'onLoad'),
               ('createStockLocation', 'inventory', 'Add a location', 'onAction')],
    'BO-511': [('listStockTransfers', 'inventory', 'Transfers in flight', 'onLoad'),
               ('createStockTransfer', 'inventory', 'Move stock between stations', 'onAction'),
               ('receiveStockTransfer', 'inventory', 'Receive it', 'onAction')],
    'BO-512': [('createStockMovement', 'inventory', 'Adjust with a reason', 'onAction'),
               ('listStockMovements', 'inventory', 'Adjustments so far', 'onLoad')],
    'BO-513': [('getStockPositions', 'inventory', 'Imbalance across locations', 'onLoad'),
               ('getSuggestedRequisitions', 'inventory', 'What to move, and where', 'onLoad')],

    # ---------------------------------------------- rental, board 3: availability
    'BO-514': [('getRentalAvailability', 'rental', 'What is free, across products', 'onLoad')],
    'BO-515': [('setRentalAvailabilityRules', 'rental', 'Windows, slots and holds', 'onAction')],
    'BO-516': [('setRentalAvailabilityRules', 'rental', 'Operating hours and rental windows',
                'onAction')],
    'BO-517': [('setRentalDurationRules', 'rental', 'Slot and duration setup', 'onAction')],
    'BO-518': [('getRentalAvailability', 'rental', 'Live availability', 'onLoad')],
    'BO-519': [('getResourceCalendar', 'resources', 'Equipment against time', 'onLoad')],
    'BO-520': [('createRentalBlackout', 'rental', 'Close or reduce capacity', 'onAction')],
    'BO-521': [('getRentalAvailability', 'rental', 'Where bookings overlap', 'onLoad')],
    'BO-522': [('setRentalAvailabilityRules', 'rental', 'Buffers and hold release', 'onAction')],

    # ---------------------------------------------- rental, board 4: pricing
    'BO-524': [('listRentalPricingProfiles', 'rental', 'Profiles, and products without one',
                'onLoad')],
    'BO-525': [('createRentalPricingProfile', 'rental', 'Build a profile', 'onAction'),
               ('updateRentalPricingProfile', 'rental', 'Change it', 'onAction')],
    'BO-526': [('updateRentalPricingProfile', 'rental', 'Duration and tiered rates', 'onAction')],
    'BO-527': [('updateRentalPricingProfile', 'rental', 'Peak, weekend and seasonal rules',
                'onAction')],
    'BO-529': [('setRentalDepositPolicy', 'rental', 'Deposit basis, limits and instruments',
                'onAction')],
    'BO-530': [('setRentalDepositPolicy', 'rental', 'Release, capture and approval thresholds',
                'onAction')],
    'BO-531': [('setRentalFeePolicy', 'rental', 'Grace, late fee and extension pricing',
                'onAction')],
    'BO-532': [('requestRentalCommercialOverride', 'rental', 'Waive or adjust, with approval',
                'onAction')],
    'BO-533': [('simulateRentalPricing', 'rental', 'Test the configuration', 'onAction'),
               ('explainRentalPrice', 'rental', 'Why the price is what it is', 'onAction')],

    # ---------------------------------------------- rental, board 5: booking
    'BO-534': [('listRentalBookings', 'rental', 'Reservations across locations', 'onLoad')],
    'BO-535': [('createRentalBooking', 'rental', 'Reserve it', 'onAction'),
               ('quoteRentalPrice', 'rental', 'What it will cost', 'onAction')],
    'BO-536': [('getRentalAvailability', 'rental', 'Alternatives when the first choice is gone',
                'onLoad')],
    'BO-537': [('updateRentalBooking', 'rental', 'Capture customer details', 'onAction')],
    'BO-538': [('createRentalBooking', 'rental', 'One booking, many participants', 'onAction')],
    'BO-539': [('signRentalAgreement', 'rental', 'Capture the signature against a version',
                'onAction')],
    'BO-540': [('quoteRentalPrice', 'rental', 'Rental amount and deposit, apart', 'onLoad')],
    'BO-541': [('getRentalBooking', 'rental', 'The confirmed reservation', 'onLoad')],
    'BO-542': [('updateRentalBooking', 'rental', 'Modify, cancel or mark a no-show', 'onAction')],
    'BO-543': [('getRentalBooking', 'rental', 'Timeline and readiness', 'onLoad')],

    # ---------------------------------------------- rental, board 6: checkout
    'BO-544': [('listRentalBookings', 'rental', 'Awaiting arrival', 'onLoad')],
    'BO-545': [('getRentalBooking', 'rental', 'Retrieve by voucher scan', 'onLoad')],
    'BO-546': [('getRentalBooking', 'rental', 'What is still outstanding', 'onLoad')],
    'BO-547': [('assignRentalEquipment', 'rental', 'Bind the assets', 'onAction')],
    'BO-548': [('assignRentalEquipment', 'rental', 'Scan to assign', 'onAction'),
               ('lookupAsset', 'maintenance', 'Resolve the scanned code', 'onAction')],
    'BO-549': [('recordRentalInspection', 'rental', 'Condition before it goes out', 'onAction')],
    'BO-550': [('checkOutRental', 'rental', 'Safety briefing and handover', 'onAction')],
    'BO-551': [('checkOutRental', 'rental', 'Hold the deposit', 'onAction')],
    'BO-552': [('assignRentalEquipment', 'rental', 'Several items at once', 'onAction')],
    'BO-553': [('checkOutRental', 'rental', 'Activate the rental', 'onAction')],

    # ---------------------------------------------- rental, board 7: active rentals
    'BO-554': [('listRentalBookings', 'rental', 'Rentals out right now', 'onLoad'),
               ('listOverdueRentals', 'rental', 'Due soon and late', 'onLoad')],
    'BO-555': [('getRentalBooking', 'rental', 'The live rental', 'onLoad')],
    'BO-556': [('getRentalAvailability', 'rental', 'Can it be extended', 'onLoad')],
    'BO-557': [('quoteRentalPrice', 'rental', 'Price the extension', 'onAction'),
               ('extendRental', 'rental', 'Extend it', 'onAction')],
    'BO-558': [('swapRentalEquipment', 'rental', 'Replace a faulty item', 'onAction')],
    'BO-559': [('reportRentalIncident', 'rental', 'Record what happened', 'onAction')],
    'BO-560': [('listOverdueRentals', 'rental', 'Due soon', 'onLoad')],
    'BO-561': [('listOverdueRentals', 'rental', 'Late, and what it is accruing', 'onLoad')],
    'BO-562': [('getRentalBooking', 'rental', 'The group rental', 'onLoad')],

    # ---------------------------------------------- rental, board 8: return
    'BO-564': [('listRentalBookings', 'rental', 'Expected back', 'onLoad')],
    'BO-565': [('getRentalBooking', 'rental', 'Retrieve by scan', 'onLoad')],
    'BO-566': [('returnRental', 'rental', 'Record the actual return time', 'onAction')],
    'BO-567': [('recordRentalInspection', 'rental', 'Condition on the way back', 'onAction')],
    'BO-568': [('recordRentalInspection', 'rental', 'Before against after', 'onLoad')],
    'BO-569': [('assessRentalDamage', 'rental', 'Price the damage', 'onAction')],
    'BO-570': [('returnRental', 'rental', 'Partial return, with what is missing', 'onAction')],
    'BO-571': [('returnRental', 'rental', 'Late fee, damage and settlement', 'onAction')],
    'BO-572': [('returnRental', 'rental', 'Capture or release the deposit', 'onAction')],
    'BO-573': [('returnRental', 'rental', 'Complete, and dispose of the equipment', 'onAction'),
               ('setAssetStatus', 'maintenance', 'Back into the pool, or not', 'onAction')],

    # ------------------------------ rental, board 9: maintenance — a join, not a gap
    'BO-574': [('listWorkOrders', 'maintenance', 'Open work orders', 'onLoad'),
               ('getDueMaintenance', 'maintenance', 'What is due', 'onLoad')],
    'BO-575': [('listMaintenancePlans', 'maintenance', 'Service plans', 'onLoad'),
               ('createMaintenancePlan', 'maintenance', 'Define a plan', 'onAction'),
               ('updateMaintenancePlan', 'maintenance', 'Change it', 'onAction')],
    'BO-576': [('getDueMaintenance', 'maintenance', 'The maintenance calendar', 'onLoad'),
               ('createWorkOrder', 'maintenance', 'Schedule a job', 'onAction')],
    'BO-577': [('getWorkOrder', 'maintenance', 'The job', 'onLoad'),
               ('createWorkOrder', 'maintenance', 'Raise one', 'onAction'),
               ('updateWorkOrder', 'maintenance', 'Change it', 'onAction'),
               ('attachWorkOrderEvidence', 'maintenance', 'Photos and documents', 'onAction')],
    'BO-578': [('startWorkOrder', 'maintenance', 'Begin the repair', 'onAction'),
               ('recordWorkOrderTime', 'maintenance', 'Time on the job', 'onAction'),
               ('completeWorkOrder', 'maintenance', 'Finish it', 'onAction')],
    'BO-579': [('recordWorkOrderParts', 'maintenance', 'Parts and cost', 'onAction')],
    'BO-580': [('getAssetHistory', 'maintenance', 'Its life so far', 'onLoad')],
    'BO-581': [('submitInspection', 'maintenance', 'Return-to-service inspection', 'onAction'),
               ('verifyWorkOrder', 'maintenance', 'Approve the return to service', 'onAction')],
    'BO-582': [('setAssetStatus', 'maintenance', 'Retire or write off', 'onAction'),
               ('getAssetHistory', 'maintenance', 'The case for retiring it', 'onLoad')],

    # ---------------------------------------------- rental, board 10: analytics
    'BO-584': [('listRentalBookings', 'rental', 'The commercial picture', 'onLoad')],
    'BO-586': [('getResourceUtilisation', 'resources', 'Utilisation and capacity', 'onLoad')],
    'BO-587': [('getAssetHistory', 'maintenance', 'Equipment performance', 'onLoad')],
    'BO-588': [('listRentalBookings', 'rental', 'Duration, extension and return', 'onLoad')],
    'BO-589': [('listRentalBookings', 'rental', 'Damage, loss and deposit exceptions', 'onLoad')],
    'BO-592': [('getResourceAuditTrail', 'resources', 'Governance and audit', 'onLoad')],
}

INVALIDATES = {
    'createResourceType': ['listResourceTypes'],
    'updateResourceType': ['listResourceTypes'],
    'createResourceCategory': ['listResourceCategories'],
    'updateResourceCategory': ['listResourceCategories'],
    'createResourceAttribute': ['listResourceAttributes'],
    'createResource': ['listResources'],
    'updateResource': ['getResource', 'listResources'],
    'cloneResource': ['listResources'],
    'setResourceLifecycleState': ['getResource', 'listResources', 'getResourceAuditTrail'],
    'setResourceHierarchy': ['getResourceHierarchy'],
    'setResourceDependencies': ['getResourceDependencies'],
    'createResourcePackage': ['listResourcePackages'],
    'updateResourcePackage': ['listResourcePackages'],
    'setResourceVenueAssignment': ['getResource'],
    'setResourceSchedule': ['getResourceSchedule', 'getResourceAvailability'],
    'bookResource': ['getResourceCalendar', 'listResourceBookings', 'getResourceAvailability'],
    'updateResourceBooking': ['getResourceCalendar', 'listResourceBookings'],
    'cancelResourceBooking': ['getResourceCalendar', 'listResourceBookings'],
    'createResourceBlock': ['listResourceBlocks', 'getResourceCalendar'],
    'releaseResourceBlock': ['listResourceBlocks', 'getResourceCalendar'],
    'allocateResources': ['getResourceCalendar', 'listResourceBookings'],
    'replaceResourceAllocation': ['getResourceCalendar', 'listResourceBookings'],
    'setResourceAllocationPolicy': ['getResourceAllocationPolicy'],
    'setExperienceResourceRequirements': ['getExperienceResourceRequirements'],
    'createRentalProduct': ['listRentalProducts'],
    'updateRentalProduct': ['getRentalProduct', 'listRentalProducts'],
    'publishRentalProduct': ['getRentalProduct', 'listRentalProducts'],
    'createRentalCategory': ['listRentalCategories'],
    'setRentalProductLocations': ['getRentalProduct'],
    'setRentalDurationRules': ['getRentalProduct', 'getRentalAvailability'],
    'setRentalOperationalRules': ['getRentalProduct'],
    'setRentalAgreementRequirements': ['getRentalProduct'],
    'setRentalInventoryModel': ['getRentalProduct', 'getRentalAvailability'],
    'setRentalAvailabilityRules': ['getRentalAvailability'],
    'createRentalBlackout': ['getRentalAvailability'],
    'createRentalPricingProfile': ['listRentalPricingProfiles'],
    'updateRentalPricingProfile': ['listRentalPricingProfiles'],
    'setRentalDepositPolicy': ['listRentalPricingProfiles'],
    'setRentalFeePolicy': ['listRentalPricingProfiles'],
    'createRentalBooking': ['listRentalBookings', 'getRentalAvailability'],
    'updateRentalBooking': ['getRentalBooking', 'listRentalBookings'],
    'signRentalAgreement': ['getRentalBooking'],
    'checkOutRental': ['getRentalBooking', 'listRentalBookings', 'getRentalAvailability'],
    'assignRentalEquipment': ['getRentalBooking'],
    'extendRental': ['getRentalBooking', 'getRentalAvailability'],
    'swapRentalEquipment': ['getRentalBooking'],
    'returnRental': ['getRentalBooking', 'listRentalBookings', 'getRentalAvailability',
                     'listOverdueRentals'],
    'recordRentalInspection': ['getRentalBooking'],
    'assessRentalDamage': ['getRentalBooking'],
    'reportRentalIncident': ['getRentalBooking'],
    'createWorkOrder': ['listWorkOrders', 'getDueMaintenance'],
    'updateWorkOrder': ['getWorkOrder', 'listWorkOrders'],
    'startWorkOrder': ['getWorkOrder', 'listWorkOrders'],
    'completeWorkOrder': ['getWorkOrder', 'listWorkOrders'],
    'verifyWorkOrder': ['getWorkOrder', 'listWorkOrders'],
    'setAssetStatus': ['getAsset', 'listAssets'],
    'updateAsset': ['getAsset', 'listAssets'],
    'createStockTransfer': ['listStockTransfers', 'getStockPositions'],
    'receiveStockTransfer': ['listStockTransfers', 'getStockPositions'],
    'createStockMovement': ['getStockPositions', 'listStockMovements'],
    'createStockLocation': ['listStockLocations'],
}


def main():
    apply = '--apply' in sys.argv
    d = yaml.safe_load(io.open(F, encoding='utf8'))
    by_id = {s['id']: s for s in d['screens']}

    added = 0
    touched = []
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
            touched.append((sid, s['name'], [n['operationId'] for n in new]))

    for sid, name, ops in touched:
        print('  %-9s %-46s %s' % (sid, name[:46], ', '.join(ops)))
    if missing:
        print('\n  NOT FOUND: %s' % ', '.join(missing))
    print('\n%d reference(s) across %d screen(s)' % (added, len(touched)))

    per = {}
    for s in d['screens']:
        src = (s.get('source') or {}).get('pack') or ''
        if 'Rental_Manage' in src or 'Resource_Manage' in src:
            k = src.split('.')[0]
            tot, served = per.get(k, (0, 0))
            per[k] = (tot + 1, served + (1 if s.get('apis') else 0))
    for k, (tot, served) in sorted(per.items()):
        print('  %-46s %d of %d screens now call something' % (k[:46], served, tot))

    if not apply:
        print('\n  nothing written — pass --apply')
        return
    io.open(F, 'w', encoding='utf8').write(
        yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
    print('  -> %s' % F)


if __name__ == '__main__':
    main()
