"""Add a response to operations: {op: {"code": "409", "lines": [...relative lines, indented from the code key...]}}.
Inserted before the op's '429' (or at the end of its responses).   python -I apply_resp.py <root> <file.json> [--apply]"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc
root = Path(sys.argv[1])
dec = json.load(open(sys.argv[2], encoding='utf-8'))
APPLY = '--apply' in sys.argv
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
by_file = {}
for oid in dec:
    by_file.setdefault(ops[oid]['file'], []).append(oid)
n, prob = 0, []
for rel, oids in sorted(by_file.items()):
    D = Doc(root / rel)
    for oid in sorted(oids):
        m, end = D.find_op(oid)
        r = D.child(m, 'responses', end)
        if r is None:
            prob.append((oid, 'no responses')); continue
        code = dec[oid]['code']
        if D.child(r, code) is not None:
            prob.append((oid, 'has ' + code)); continue
        ci = D.child_indent(r)
        at = D.child(r, '429')
        if at is None:
            at = D.end_trim(D.block_end(r))
        D.insert(at, [' ' * ci + f"'{code}':"] + [' ' * (ci + 2) + l for l in dec[oid]['lines']])
        n += 1
    if APPLY:
        D.save()
print(n, 'added', prob)
