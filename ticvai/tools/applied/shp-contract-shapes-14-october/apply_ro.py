"""C-REQUEST-SERVER-FIELDS: mark each flagged server-owned property of the write body `readOnly: true`; a `status` the
caller sets (CLIENT below) is marked `x-ticvai-caller-sets` with the reason instead.
    python -I apply_ro.py <root> <found.json> [--apply]"""
import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc, sq
root = Path(sys.argv[1])
found = json.load(open(sys.argv[2], encoding='utf-8'))
APPLY = '--apply' in sys.argv
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
docs = {s: d for s, _, d in g.contracts()}
CLIENT = {
    'setChannelListing': 'the caller moves a listing between draft, live, paused and delisted',
    'setChannelProvider': 'the caller sets a provider active, standby or suspended',
    'setConfigurationProfile': 'the caller sends draft, or published to publish the version',
    'setConfigurationTemplate': 'the caller saves a template draft, makes it active or retires it',
    'setContactAutomation': 'the caller moves an automation through draft, active, paused and retired',
    'setCurrencyRoundingRule': 'the caller makes a rounding profile active or retires it',
    'setDataProcessingPurpose': 'the caller moves a purpose from draft to active or retired',
    'setFeeDefinition': 'the caller saves a fee draft, makes it active or retires it',
    'setJourneyProfile': 'the caller sets a profile inactive, there being no delete',
    'setPackagePricingDefinition': 'the caller saves a package price draft or makes it active',
    'setPriceCalculationPolicy': 'the caller saves a calculation profile draft or makes it active',
    'setPrivacyNoticePolicyGovernance': 'the caller moves the version forward along its lifecycle',
    'setPrivacyRequestTypes': 'the caller makes a request type active or retires it',
    'setQualityEvaluation': 'the caller advances an evaluation from draft to scored to acknowledged',
    'setSenderIdentityDomain': 'the caller may set active on a verified identity, or suspended',
    'setTenantDomainMapping': 'a domain is detached by setting its status',
    'setTrackingTechnology': 'the caller approves, blocks or retires a technology',
    'setWaiverAssociation': 'the caller removes an association by setting removed',
    'setWaiverException': 'the caller requests, approves, rejects or revokes an exception',
    'setWaiverTriggerRule': 'the caller switches a rule off by setting inactive',
}


def deref_name(node, doc):
    name = None
    while isinstance(node, dict) and '$ref' in node:
        fp, _, fr = node['$ref'].partition('#')
        if fp:
            return None, None
        name = fr.split('/')[-1]
        cur = doc
        for p in [p for p in fr.split('/') if p]:
            cur = cur.get(p)
        node = cur
    return name, node


todo = {}  # (file, schema, prop) -> ('ro'|'caller', reason)
for oid, msg in found['C-REQUEST-SERVER-FIELDS'].items():
    o = ops[oid]
    doc = docs[o['contract']]
    _, rb = deref_name(o['op'].get('requestBody'), doc)
    sch = list(rb['content'].values())[0]['schema']
    name, node = deref_name(sch, doc)
    if not name:
        raise SystemExit(f'{oid}: inline body')
    for fld in msg.split('server-owned ')[1].split(', '):
        if fld == 'status' and oid in CLIENT:
            todo[(o['file'], name, fld)] = ('caller', CLIENT[oid])
        else:
            todo.setdefault((o['file'], name, fld), ('ro', None))
by_file = {}
for (f, s, p), v in todo.items():
    by_file.setdefault(f, []).append((s, p, v))
n, prob = 0, []
for rel, items in sorted(by_file.items()):
    D = Doc(root / rel)
    for s, p, (kind, why) in sorted(items):
        si = D.find_schema(s)
        props = D.child(si, 'properties')
        if props is None:
            prob.append((s, p, 'no properties line')); continue
        pi = D.child(props, p)
        if pi is None:
            prob.append((s, p, 'no property line')); continue
        line = D.text(D.lines[pi])
        if kind != 'ro':
            continue
        add = 'readOnly: true'
        val = line.split(':', 1)[1].strip()
        if val.startswith('{') and val.endswith('}'):
            eol = D.lines[pi][len(line):]
            D.lines[pi] = line[:line.rindex('}')].rstrip() + ', ' + add + ' }' + eol
            D.dirty = True
        elif val == '':
            D.insert(pi + 1, [' ' * D.child_indent(pi) + add])
        else:
            prob.append((s, p, 'unhandled: ' + line.strip()[:60])); continue
        n += 1
    if APPLY:
        D.save()
print(n, 'marked', prob)
