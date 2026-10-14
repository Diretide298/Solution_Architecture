"""Write the SHP breaking-change block (BC-340..) into docs/active/breaking-changes.yaml: one entry per contract for the
path keys, one per PATCH body."""
import sys, json
from pathlib import Path
from collections import defaultdict
root, S = Path(sys.argv[1]), Path(sys.argv[2])
applied = json.load(open(S / 'noaddr-applied.json', encoding='utf-8'))
impact = json.load(open(S / 'impact.json', encoding='utf-8'))
APPROVER = 'Chinmay Parab, 14 October 2026 (Block A audit: "go with your recommendation")'


def base(keys):
    return sorted({k.split('#')[0] for k in keys})


def flow(xs):
    return '[' + ', '.join(xs) + ']'


def q(s):
    return "'" + s.replace("'", "''") + "'"


by = defaultdict(list)
for k in applied['K']:
    by[k['contract']].append(k)
lines = ['  # BC-340 to BC-367 (CHG-SHP-003, CHG-SHP-008): batch SHP of the 14 October Block A audit, block 340-379. One entry',
         '  # per contract where one reason covers several operations: `operation` names the first and `operations` lists',
         '  # them all (tools/check-contract-compat.py reads both). check-contract-shapes C-NO-ADDRESS: a write that replaces one',
         '  # item of a collection names it in the path; the item moved from the collection path to `<collection>/{key}`.']
n = 340
for contract in sorted(by):
    ks = sorted(by[contract], key=lambda k: k['op'])
    opsl = [k['op'] for k in ks]
    prod = base(p for o in opsl for p in impact.get(o, {}).get('producers', []))
    cons = base(c for o in opsl for c in impact.get(o, {}).get('consumers', []))
    moves = '; '.join(f"{k['op']} {k['from']} -> {k['to']}" for k in ks)
    reason = ('check-contract-shapes C-NO-ADDRESS (R162, R103; audit of 14 October 2026, '
              'audit/ticvai/runs/audit-1014/classes.json): each of these PUTs created or replaced one item of a '
              'collection that the body named, on the collection path, so neither the route nor the contract said '
              'which row it addressed or whether it replaced or upserted. The item is now addressed in the path, '
              'and a body key, when sent, must equal it' + ('; ' + ', '.join(o for o in opsl if o.startswith('approve') and 'approvalRequestId' in str(o) ) if False else '') + (' (approveDecision, approveExceptionServiceRecovery and approveGroupDiscountException now name the record they decide, which their bodies never carried)' if any(o in ('approveDecision', 'approveExceptionServiceRecovery', 'approveGroupDiscountException') for o in opsl) else '') + '. Moves: ' + moves + '. A path cannot change additively.')
    lines += [f'  - id: BC-{n}', f'    contract: {contract}', f'    operation: {opsl[0]}']
    if len(opsl) > 1:
        lines += [f'    operations: {flow(opsl)}']
    lines += [f'    reason: {q(reason)}', f'    approved-by: {q(APPROVER)}', '    tag: r6',
              f'    producer-tickets: {flow(prod) if prod else "[none-linked]"}',
              f'    consumer-tickets: {flow(cons) if cons else "[none-linked]"}']
    n += 1
PATCH = {'updateDonationCampaign': ('catalogue', 'DonationCampaign', 'id, raisedTotal'),
         'updatePartnerAgreement': ('subscription', 'PartnerAgreement', 'id, partnerName, version, approvalRequestId'),
         'updateRotaAssignment': ('workforce', 'RotaAssignment', 'overtimeMinutes, breachesWorkingHourLimit, id, displayName'),
         'updateTableReservation': ('fnb', 'TableReservation', 'id, takenByPrincipalId, actualPartySize, tableVisitId, createdAt')}
for o, (contract, s, gone) in PATCH.items():
    prod = base(impact[o]['producers'])
    cons = base(impact[o]['consumers'])
    reason = (f'check-contract-shapes C-PATCH-FULL-BODY (the ADAM CR-089 pattern; audit of 14 October 2026, '
              f'audit/ticvai/runs/audit-1014/classes.json): the PATCH body was the persisted {s} with its required '
              f'list, so a partial update had to resend the whole resource. The body is now Update{s}Request '
              f'(minProperties 1, no required, no defaults). The server-owned fields ({gone}) leave the request; '
              f'breaking in declaration only, as BC-089: there is no additionalProperties false, so a full body is '
              f'still accepted and those fields ignored.')
    lines += [f'  - id: BC-{n}', f'    contract: {contract}', f'    operation: {o}', '    change: "removed"',
              f'    reason: {q(reason)}', f'    approved-by: {q(APPROVER)}', '    tag: r6',
              f'    producer-tickets: {flow(prod) if prod else "[none-linked]"}',
              f'    consumer-tickets: {flow(cons) if cons else "[none-linked]"}']
    n += 1
assert n <= 380
p = root / 'docs/active/breaking-changes.yaml'
raw = p.read_bytes().decode('utf-8')
eol = '\r\n' if '\r\n' in raw else '\n'
if not raw.endswith(eol):
    raw += eol
raw += eol.join(lines) + eol
p.write_bytes(raw.encode('utf-8'))
print('entries', n - 340, 'last', n - 1)
