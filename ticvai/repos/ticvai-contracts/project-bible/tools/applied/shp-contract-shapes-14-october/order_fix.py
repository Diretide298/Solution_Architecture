"""Replace the appended order sentence where the description already stated an order the default contradicted."""
import sys, json, importlib.util
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc
root, S = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
spec = importlib.util.spec_from_file_location('ccs', root / 'tools' / 'check-contract-shapes.py')
ccs = importlib.util.module_from_spec(spec); spec.loader.exec_module(ccs)
dec = json.load(open(S / 'order-decisions.json', encoding='utf-8'))
NEW = {
    'getOutletStock': 'Low stock first, by `available` ascending, then by `name`.',
    'listAccreditationDocuments': 'Newest first, by `submittedAt` descending, then by `id`; with `status=submitted` (the verification queue) oldest first, by `submittedAt` ascending.',
    'listDunningCases': 'Fewest attempts remaining first, by `attemptsMade` descending, then by `nextAttemptAt` ascending, then by `id`.',
    'listExpiringBatches': 'Soonest expiry first, by `expiresAt` ascending, then by `id`.',
    'listGuestIdentityVerifications': 'Oldest first, by `submittedAt` ascending, then by `id`.',
    'listInstalmentPlans': 'Soonest first, by `nextDueDate` ascending, then by `id`.',
    'listKnowledgeGaps': 'Newest first, by `lastAskedAt` descending, then by `id`.',
    'listMyTableReservations': 'Soonest first, by `startsAt` ascending (a waitlist entry by `recordedAt`), then by `id`.',
    'listProductTrailChange': 'Newest first, by `dateTime` descending, then by `auditId`.',
    'listProductionAccessRequests': 'Pending first (by `status`), then newest first, by `requestedAt` descending, then by `id`.',
    'listQueueEntries': 'Sorted by `positionInQueue` ascending, then by `joinedAt`.',
    'listSiteNormalisationBases': 'Newest period first, by `periodStart` descending, then by `id`.',
    'listStaffConversations': 'Newest activity first, by `lastMessageAt` descending, then by `id`.',
    'listStaffMessages': 'Newest first, by `sentAt` descending, then by `id`.',
    'listStockCountLines': 'Sorted by `itemId` ascending, then by `id`.',
    'listVisitPlanAlternatives': 'Best first, by `matchedInterests` descending, then by `walkMinutes` ascending.',
}
ops = g.operations()
docs = {s: d for s, _, d in g.contracts()}
for oid, new in NEW.items():
    new = '**Order.** ' + new
    assert ccs.order_names_field(new, ccs.response_props(ops[oid]['op'], docs[ops[oid]['contract']])), oid
    D = Doc(root / ops[oid]['file'])
    m, end = D.find_op(oid)
    old = dec[oid]
    hits = [j for j in range(m, end) if old in D.lines[j] or old.replace("'", "''") in D.lines[j]]
    assert len(hits) == 1, (oid, hits)
    D.lines[hits[0]] = D.lines[hits[0]].replace(old, new)
    D.dirty = True
    D.save()
    dec[oid] = new
json.dump(dec, open(S / 'order-decisions.json', 'w', encoding='utf-8'), indent=1)
print('fixed', len(NEW))
