"""Put the three drafted decision workspaces back on their original path (they stay C-NO-ADDRESS keeps)."""
import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc
root, S = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
app = json.load(open(S / 'noaddr-applied.json', encoding='utf-8'))
dec = json.load(open(S / 'noaddr-decisions.json', encoding='utf-8'))
for oid in ('approveDecision', 'approveExceptionServiceRecovery', 'approveGroupDiscountException'):
    k = next(x for x in app['K'] if x['op'] == oid)
    f = ops[oid]
    assert f['path'] == k['to'], (oid, f['path'])
    D = Doc(root / f['file'])
    pl = D.find_path_item(k['to'])
    m, end = D.find_op(oid)
    # the path item holds only this operation
    pend = D.block_end(pl)
    others = [j for j in range(pl + 1, pend) if not D.blank(j) and D.indent(j) == 4 and j != m]
    assert not others, (oid, others)
    D.lines[pl] = D.lines[pl].replace(k['to'], k['from'])
    p = k['params'][0]
    j = next(j for j in range(m, end) if re.match(r'^\s*- name: %s\s*$' % p, D.text(D.lines[j])))
    e = j + 1
    while e < end and D.indent(e) > D.indent(j):
        e += 1
    D.delete(j, e)
    D.save()
    app['K'] = [x for x in app['K'] if x['op'] != oid]
    app.setdefault('kept', []).append(oid)
    dec[oid] = {'kind': 'keep', 'why': 'a drafted decision workspace whose body names no record to decide'}
json.dump(app, open(S / 'noaddr-applied.json', 'w', encoding='utf-8'), indent=1)
json.dump(dec, open(S / 'noaddr-decisions.json', 'w', encoding='utf-8'), indent=1)
print('ok')
