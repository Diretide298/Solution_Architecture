"""C-PAGED-ORDER: pick the order field for each member. -> order-decisions.json {op: sentence}"""
import sys, json, re, importlib.util
from pathlib import Path
from collections import Counter
root, S = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
spec = importlib.util.spec_from_file_location('ccs', root / 'tools' / 'check-contract-shapes.py')
ccs = importlib.util.module_from_spec(spec); spec.loader.exec_module(ccs)
found = json.load(open(S / sys.argv[3], encoding='utf-8'))
ops = g.operations()
docs = {stem: doc for stem, _, doc in g.contracts()}
TIME = ['createdAt', 'occurredAt', 'recordedAt', 'raisedAt', 'requestedAt', 'submittedAt', 'issuedAt', 'openedAt',
        'receivedAt', 'scannedAt', 'loggedAt', 'detectedAt', 'sentAt', 'startedAt', 'generatedAt', 'capturedAt',
        'postedAt', 'updatedAt', 'changedAt', 'publishedAt', 'at', 'timestamp']
SCHED = ['startsAt', 'startAt', 'scheduledAt', 'scheduledFor', 'dueAt', 'visitDate', 'dateTime', 'presentationTimestamp', 'start', 'businessDate', 'periodStart',
         'effectiveFrom', 'validFrom', 'expiresAt', 'expiryDate']
NAMED = ['sortOrder', 'displayOrder', 'position', 'sequence', 'rank', 'priority', 'name', 'displayName', 'label', 'title', 'code', 'product', 'channel', 'credential']
out, c = {}, Counter()
for oid in sorted(found['C-PAGED-ORDER']):
    f = ops[oid]
    props = ccs.response_props(f['op'], docs[f['contract']])
    pick = None
    for t in TIME:
        if t in props:
            pick = ('desc', t); break
    if not pick:
        for t in SCHED:
            if t in props:
                pick = ('asc', t); break
    if not pick:
        for t in NAMED:
            if t in props:
                pick = ('asc', t); break
    keys = [p for p in sorted(props) if p.endswith('Id')]
    stem = oid.lower()
    own = 'id' if 'id' in props else next((p for p in keys if p[:-2].lower() in stem), None) or (keys[0] if keys else None)
    then = f', then by `{own}`' if own and (not pick or own != pick[1]) else ''
    if not pick and not own:
        at = sorted(p for p in props if re.search(r'[a-z]At$', p))
        if at:
            pick = ('desc', at[0])
    if pick and pick[0] == 'desc':
        s = f'**Order.** Newest first, by `{pick[1]}` descending{then}.'
    elif pick and pick[1] in SCHED:
        s = f'**Order.** Soonest first, by `{pick[1]}` ascending{then}.'
    elif pick:
        s = f'**Order.** Sorted by `{pick[1]}` ascending{then}.'
    elif own:
        pick = ('desc', own)
        s = f'**Order.** Sorted by `{own}` descending (a UUIDv7, so newest first).'
    else:
        pick = ('none', None)
        s = None
        print('NOKEY', oid, sorted(props)[:15])
    if s:
        assert ccs.order_names_field(s, props), (oid, s)
    if s:
        out[oid] = s
    c[pick[1]] += 1
MANUAL = {'listMembershipCommercialPricing': ('asc', 'membershipCode'), 'listMembershipUsageVisit': ('asc', 'membershipCode'),
          'listPartnerStatementAccount': ('asc', 'dueDate'), 'listPricingDistributionSynchronization': ('asc', 'targetName'),
          'listPricingVersionBaseline': ('desc', 'createdDate'), 'listProcessAutomationOpportunity': ('asc', 'process'),
          'listSlaEscalationBottleneck': ('asc', 'instance'), 'listWorkflowInstanceProcess': ('asc', 'businessObject')}
for oid, (d, fld) in MANUAL.items():
    out[oid] = (f'**Order.** Newest first, by `{fld}` descending.' if d == 'desc' else f'**Order.** Sorted by `{fld}` ascending.')
    f = ops[oid]
    assert ccs.order_names_field(out[oid], ccs.response_props(f['op'], docs[f['contract']])), oid
json.dump(out, open(S / 'order-decisions.json', 'w', encoding='utf-8'), indent=1)
print(c.most_common())
