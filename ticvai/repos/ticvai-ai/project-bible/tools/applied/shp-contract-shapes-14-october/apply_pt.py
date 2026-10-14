"""C-ERROR-PROBLEM-TYPE: write each drafted slug list as the response's x-ticvai-problem-types (one line, after the
response's code line).   python -I apply_pt.py <ticvai root> <scratch> [--apply]"""
import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc

root, S = Path(sys.argv[1]), Path(sys.argv[2])
APPLY = '--apply' in sys.argv
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
slugs = {}
for i in range(1, 5):
    slugs.update(json.load(open(S / f'errs-out-{i}.json', encoding='utf-8')))
excl = set(open(S / 'mod-excl.txt').read().split())
SLUG = re.compile(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$')
by_file = {}
for k, v in slugs.items():
    assert k not in excl, k
    assert v and all(SLUG.match(s) for s in v), (k, v)
    by_file.setdefault(ops[k.rsplit(':', 1)[0]]['file'], []).append(k)
done, skipped = [], []
for rel, keys in sorted(by_file.items()):
    D = Doc(root / rel)
    for k in sorted(keys):
        oid, code = k.rsplit(':', 1)
        i = D.response(oid, code)
        if i is None:
            skipped.append((k, 'no response line'))
            continue
        s = D.text(D.lines[i])
        if not re.match(r"""^\s*['"]?\d{3}['"]?\s*:\s*$""", s):
            skipped.append((k, 'flow style: ' + s.strip()[:60]))
            continue
        ci = D.child_indent(i)
        if D.child(i, 'x-ticvai-problem-types') is not None:
            skipped.append((k, 'already has types'))
            continue
        D.insert(i + 1, [' ' * ci + 'x-ticvai-problem-types: [' + ', '.join(slugs[k]) + ']'])
        done.append(k)
    if APPLY:
        D.save()
print(len(done), 'written', len(skipped), 'skipped', skipped)
