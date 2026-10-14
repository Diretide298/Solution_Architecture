"""The DuplicateCode 409 a create now declares (C-CODE-409) needs its uniqueness on the property (SP-DUPLICATE-409):
`x-ticvai-unique` on the `code` the create takes, on the persisted schema derive-ddl reads (the Create<X>Request's
resource, or the body itself when it persists). Scope per common.yaml (decided 28 September, R108): configuration codes
per tenant; things placed at a venue per venue.   python -I apply_unique.py <root> <scratch> [--apply]"""
import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc
root, S = Path(sys.argv[1]), Path(sys.argv[2])
APPLY = '--apply' in sys.argv
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
by, names = g.schemas()
VENUE = {'createAccessPoint', 'createStockLocation', 'createQueue', 'createMenu', 'createModifierGroup', 'createResource', 'createGame'}
mine = json.load(open(S / 'code409.json'))


def ref_of(op):
    rb = op.get('requestBody') or {}
    for m in (rb.get('content') or {}).values():
        return g.ref_name(str((m.get('schema') or {}).get('$ref') or ''))


todo = {}
for oid in sorted(mine):
    f = ops[oid]
    st = f['contract']
    req = ref_of(f['op'])
    cands = []
    if req:
        cands.append(req)
        res = re.sub(r'^(Create|Update)(\w+)Request$', r'\2', req)
        if res != req:
            cands.append(res)
    have = any(isinstance(((by.get((st, c)) or {}).get('properties') or {}).get('code'), dict)
               and by[(st, c)]['properties']['code'].get('x-ticvai-unique') for c in cands)
    if have:
        continue
    target = None
    for c in reversed(cands):  # the persisted resource first
        s = by.get((st, c)) or {}
        if 'code' in (s.get('properties') or {}) and not str(s.get('x-ticvai-persistence') or 'none').startswith('none'):
            target = c
            break
    if not target:
        target = next((c for c in cands if 'code' in ((by.get((st, c)) or {}).get('properties') or {})), None)
    if not target:
        print('NO TARGET', oid, cands)
        continue
    todo[(f['file'], target)] = 'venue' if oid in VENUE else 'tenant'
    print(oid, target, todo[(f['file'], target)])
for (rel, sname), lvl in sorted(todo.items()):
    D = Doc(root / rel)
    si = D.find_schema(sname)
    pi = D.child(D.child(si, 'properties'), 'code')
    line = D.text(D.lines[pi])
    val = line.split(':', 1)[1].strip()
    if val.startswith('{'):
        D.lines[pi] = line[:line.rindex('}')].rstrip() + f', x-ticvai-unique: {lvl} }}' + D.lines[pi][len(line):]
        D.dirty = True
    else:
        D.insert(pi + 1, [' ' * D.child_indent(pi) + f'x-ticvai-unique: {lvl}'])
    if APPLY:
        D.save()
print(len(todo))
