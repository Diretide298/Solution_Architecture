"""Append one sentence, as its own paragraph, to an operation's description (adding a description where there is none).
Line-level: the description's own quoting style is kept. Verified by re-parsing every touched operation.

    python -I apply_desc.py <ticvai root> <decisions.json> [--apply]
"""
import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc, sq
import yaml

root = Path(sys.argv[1])
dec = json.load(open(sys.argv[2], encoding='utf-8'))
APPLY = '--apply' in sys.argv
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
by_file = {}
for oid in dec:
    by_file.setdefault(ops[oid]['file'], []).append(oid)
problems, n = [], 0
for rel, oids in sorted(by_file.items()):
    D = Doc(root / rel)
    for oid in sorted(oids):
        text = dec[oid]
        m, end = D.find_op(oid)
        di = D.child(m, 'description', end)
        if di is None:
            idl = next(j for j in range(m, end) if D.text(D.lines[j]).strip().startswith('operationId:'))
            D.insert(idl + 1, [' ' * D.indent(idl) + 'description: ' + sq(text)])
            n += 1
            continue
        line = D.text(D.lines[di])
        val = line.split('description:', 1)[1].strip()
        dend = D.end_trim(D.block_end(di))
        last = dend - 1
        ind = D.indent(di)
        if val[:1] in ('|', '>'):
            ci = D.child_indent(di, D.block_end(di)) if dend > di + 1 else ind + 2
            D.insert(dend, ['', ' ' * ci + text])
        elif val[:1] == "'":
            lt = D.text(D.lines[last])
            if not lt.rstrip().endswith("'") or (last == di and len(val) < 2):
                problems.append((oid, 'single-quoted end not found'))
                continue
            stripped = lt.rstrip()
            ci = ind + 2
            eol = D.lines[last][len(lt):]
            D.lines[last] = stripped[:-1] + eol
            D.insert(last + 1, ['', ' ' * ci + text.replace("'", "''") + "'"])
        elif val[:1] == '"':
            lt = D.text(D.lines[last])
            if not lt.rstrip().endswith('"'):
                problems.append((oid, 'double-quoted end not found'))
                continue
            stripped = lt.rstrip()
            eol = D.lines[last][len(lt):]
            D.lines[last] = stripped[:-1] + eol
            D.insert(last + 1, ['', ' ' * (ind + 2) + text.replace('\\', '\\\\').replace('"', '\\"') + '"'])
        else:
            # plain scalar: rewrite nothing; append as a continuation paragraph only when the text is plain-safe
            if ': ' in text or ' #' in text or text.startswith(('*', '`', '!', '&', '[', '{', '>', '|', "'", '"', '%', '@')):
                # make it a paragraph that cannot start a token: prefix is the existing scalar, so a leading '*' is
                # fine inside a continuation line; only ': ' and ' #' are unsafe
                if ': ' in text or ' #' in text:
                    problems.append((oid, 'plain scalar and unsafe text'))
                    continue
            D.insert(dend, ['', ' ' * (ind + 2) + text])
        D.dirty = True
        n += 1
    if APPLY:
        D.save()
# verify
bad = []
if APPLY:
    for rel, oids in sorted(by_file.items()):
        d = yaml.load((root / rel).read_text(encoding='utf-8'), Loader=yaml.CSafeLoader)
        found = {}
        for p, item in (d.get('paths') or {}).items():
            for v, op in (item or {}).items():
                if isinstance(op, dict) and op.get('operationId') in oids:
                    found[op['operationId']] = str(op.get('description') or '')
        for oid in oids:
            want = dec[oid]
            got = found.get(oid, '')
            if not got.rstrip().endswith(want.rstrip()):
                bad.append((oid, got[-120:]))
print(n, 'appended', 'problems', problems, 'bad', bad[:10], len(bad))
