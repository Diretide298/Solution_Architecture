import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc
root = Path(sys.argv[1])
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
by, _ = g.schemas()
for oid, lvl in (('createCostCenter', 'tenant'), ('createStockLocation', 'venue')):
    f = ops[oid]
    r = f['op']['responses']
    ref = None
    for c in ('201', '200', 201, 200):
        if c in r:
            rr = r[c]
            for m in (rr.get('content') or {}).values():
                ref = g.ref_name(str((m.get('schema') or {}).get('$ref') or ''))
            break
    s = by[(f['contract'], ref)]
    print(oid, ref, s.get('x-ticvai-persistence'), (s.get('properties') or {}).get('code'))
    D = Doc(root / f['file'])
    si = D.find_schema(ref)
    pi = D.child(D.child(si, 'properties'), 'code')
    line = D.text(D.lines[pi])
    if line.split(':', 1)[1].strip().startswith('{'):
        D.lines[pi] = line[:line.rindex('}')].rstrip() + f', x-ticvai-unique: {lvl} }}' + D.lines[pi][len(line):]
        D.dirty = True
    else:
        D.insert(pi + 1, [' ' * D.child_indent(pi) + f'x-ticvai-unique: {lvl}'])
    D.save()
