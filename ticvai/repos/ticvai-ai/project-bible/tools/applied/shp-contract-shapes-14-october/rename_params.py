"""Rename new path keys so they match the table the operation's lineage reaches (check-parameter-columns)."""
import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc, sq
root, S = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
R = {  # op: (old, new, description)
    'setChannelProvider': ('channelProviderId', 'communicationProviderId', None),
    'setEInvoicingProvider': ('eInvoicingProviderId', 'providerId', None),
    'setPrepaidMinutePackage': ('packageId', 'prepaidMinutesId', None),
    'setBiometricLifecycleRetention': ('policyId', 'retentionSettingId', "Addresses the retention rule this write creates or replaces. The body's `policyId`, when sent, must equal it."),
    'setCredentialActivationDisplay': ('ruleId', 'credentialPolicyId', "Addresses the activation and display rule this write creates or replaces. The body's `ruleId`, when sent, must equal it."),
    'publishActivationScheduler': ('scheduleId', 'lifecycleActionId', "Addresses the scheduled lifecycle action this write creates or replaces. The body's `scheduleId`, when sent, must equal it."),
    'approveDecision': ('approvalRequestId', 'promotionId', 'The promotion whose pending approval this decision is on (the request is recorded in the approvals engine).'),
    'approveExceptionServiceRecovery': ('approvalRequestId', 'afterSaleRequestId', 'The after-sales request whose policy exception this decision is on.'),
    'approveGroupDiscountException': ('approvalRequestId', 'groupQuoteId', 'The group quote whose discount exception this decision is on, before the quote is committed.'),
}
app = json.load(open(S / 'noaddr-applied.json', encoding='utf-8'))
dec = json.load(open(S / 'noaddr-decisions.json', encoding='utf-8'))
for oid, (old, new, desc) in R.items():
    f = ops[oid]
    D = Doc(root / f['file'])
    path = f['path']
    newpath = path.replace('{%s}' % old, '{%s}' % new)
    pl = D.find_path_item(path)
    assert pl is not None, oid
    D.lines[pl] = D.lines[pl].replace('{%s}' % old, '{%s}' % new)
    m, end = D.find_op(oid)
    hits = [j for j in range(m, end) if re.match(r'^\s*- name: %s\s*$' % old, D.text(D.lines[j]))]
    assert len(hits) == 1, (oid, hits)
    j = hits[0]
    D.lines[j] = D.lines[j].replace(old, new)
    if desc:
        dl = j + 3
        assert D.text(D.lines[dl]).strip().startswith('description:'), (oid, D.lines[dl])
        ind = D.indent(dl)
        D.lines[dl] = ' ' * ind + 'description: ' + sq(desc) + D.eol
    D.dirty = True
    D.save()
    for k in app['K']:
        if k['op'] == oid:
            k['to'] = newpath
            k['params'] = [new]
    dec[oid]['param'] = new
json.dump(app, open(S / 'noaddr-applied.json', 'w', encoding='utf-8'), indent=1)
json.dump(dec, open(S / 'noaddr-decisions.json', 'w', encoding='utf-8'), indent=1)
print('ok')
