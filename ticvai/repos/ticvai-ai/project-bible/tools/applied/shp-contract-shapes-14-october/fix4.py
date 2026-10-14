import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc, sq
root, S = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
a = json.load(open(S / 'action409-out.json', encoding='utf-8'))
NEW = {
    'freezeEntitlement': 'Already `frozen`, or `suspended`, or ended as `expired` or `cancelled`; only an `active` one is frozen. Nothing changes.',
    'pushWalletPassUpdate': 'The pass is `voided` or `expired`; nothing is pushed to its devices.',
    'reinstateEntitlement': 'Not `suspended`; only a suspended one is reinstated. Nothing changes.',
    'suspendEntitlement': 'Already ended (`fullyConsumed`, `expired`, `cancelled` or `surrendered`); only a live one is suspended or reinstated. Nothing changes.',
}
for oid, new in NEW.items():
    D = Doc(root / ops[oid]['file'])
    i = D.response(oid, '409')
    j = D.child(i, 'description')
    old = 'description: ' + sq(a[oid]['description'])
    line = D.text(D.lines[j])
    assert line.strip() == old, (oid, line)
    D.lines[j] = line.replace(old, 'description: ' + sq(new)) + D.lines[j][len(line):]
    D.dirty = True
    D.save()
    a[oid]['description'] = new
json.dump(a, open(S / 'action409-out.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('ok')
