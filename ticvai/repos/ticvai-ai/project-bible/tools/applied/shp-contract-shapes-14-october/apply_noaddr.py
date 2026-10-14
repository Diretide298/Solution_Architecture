"""C-NO-ADDRESS: x-ticvai-singleton (+ note) on S members; a path key on K members (the write moves from the collection
path to the item path). Line-level edits only.

    python -I apply_noaddr.py <ticvai root> <scratch> [--apply]
"""
import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc, sq

root, S = Path(sys.argv[1]), Path(sys.argv[2])
APPLY = '--apply' in sys.argv
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g

dec = json.load(open(S / 'noaddr-decisions.json', encoding='utf-8'))
ops = g.operations()
docs = {stem: doc for stem, _, doc in g.contracts()}


def deref(node, doc):
    while isinstance(node, dict) and '$ref' in node:
        fp, _, frag = node['$ref'].partition('#')
        if fp:
            return None
        cur = doc
        for p in [p for p in frag.split('/') if p]:
            cur = cur.get(p) if isinstance(cur, dict) else None
        node = cur
    return node


def body_props(op, doc):
    rb = deref(op.get('requestBody'), doc) or {}
    for media in (rb.get('content') or {}).values():
        n = deref(media.get('schema'), doc) or {}
        props = dict(n.get('properties') or {})
        for part in n.get('allOf') or []:
            props.update((deref(part, doc) or {}).get('properties') or {})
        return props
    return {}


def path_param_types(doc):
    out = {}
    for p, item in (doc.get('paths') or {}).items():
        for v, op in (item or {}).items():
            if not isinstance(op, dict):
                continue
            for prm in list(item.get('parameters') or []) + list(op.get('parameters') or []):
                prm = deref(prm, doc) if isinstance(prm, dict) else None
                if isinstance(prm, dict) and prm.get('in') == 'path':
                    out.setdefault(prm['name'], prm.get('schema') or {})
    return out


report = {'S': [], 'K': [], 'skipped': []}
by_file = {}
for oid, d in dec.items():
    by_file.setdefault(ops[oid]['file'], []).append(oid)

for rel, oids in sorted(by_file.items()):
    f = ops[oids[0]]
    doc = docs[f['contract']]
    D = Doc(root / rel)
    ptypes = path_param_types(doc)
    all_paths = set((doc.get('paths') or {}).keys())
    # singletons first: two lines after operationId
    for oid in sorted(o for o in oids if dec[o]['kind'] == 'S'):
        m, end = D.find_op(oid)
        idl = next(j for j in range(m, end) if D.text(D.lines[j]).strip().startswith('operationId:'))
        ind = ' ' * D.indent(idl)
        D.insert(idl + 1, [f'{ind}x-ticvai-singleton: true', f'{ind}x-ticvai-singleton-note: {sq(dec[oid]["note"])}'])
        report['S'].append(oid)
    # path keys
    for oid in sorted(o for o in oids if dec[o]['kind'] == 'K'):
        info = ops[oid]
        src = info['path']
        params = dec[oid]['param'].split('/')
        subs = sorted(p for p in all_paths if re.fullmatch(re.escape(src.rstrip('/')) + r'/\{[^}/]+\}', p))
        if subs and len(params) == 1:
            target = subs[0]
            params = [re.search(r'\{([^}]+)\}$', target).group(1)]
        else:
            target = src.rstrip('/') + ''.join('/{%s}' % p for p in params)
        props = body_props(info['op'], doc)
        if info['method'] in ((doc.get('paths') or {}).get(target) or {}):
            report['skipped'].append({'op': oid, 'why': f'{target} already has a {info["method"]}'})
            continue
        m, end = D.find_op(oid)
        e = D.end_trim(end)
        block = D.lines[m:e]
        bind = D.indent(m)
        # parameters to add
        plines = []
        item_level = {str((deref(x, doc) or {}).get('name')) for x in
                      (((doc.get('paths') or {}).get(target) or {}).get('parameters') or [])}
        for p in [p for p in params if p not in item_level]:
            sch = ptypes.get(p)
            if not sch:
                bp = props.get(p) if isinstance(props.get(p), dict) else {}
                if bp.get('type') == 'string' and not bp.get('enum'):
                    sch = {'type': 'string', **({'format': bp['format']} if bp.get('format') else {})}
                elif p.endswith('Id'):
                    sch = {'type': 'string', 'format': 'uuid'}
                else:
                    sch = {'type': 'string'}
            if p in props:
                desc = f"Addresses the item this write creates or replaces. The body's `{p}`, when sent, must equal it."
            elif p == 'approvalRequestId':
                desc = 'The approval request this decision is on (approvals engine).'
            else:
                desc = "Addresses the item this write creates or replaces: its `id`. The body's `id`, when sent, must equal it."
            styp = '{ ' + ', '.join(f'{k}: {v}' for k, v in sch.items() if k in ('type', 'format', 'pattern')) + ' }'
            plines.append((p, desc, styp))
        # find parameters: within the block
        sub = Doc.__new__(Doc)
        sub.lines, sub.eol = block, D.eol
        pi = sub.child(0, 'parameters')
        if pi is not None:
            nxt = next((j for j in range(pi + 1, len(block)) if not sub.blank(j)), None)
            li = sub.indent(nxt) if nxt is not None and sub.text(block[nxt]).lstrip().startswith('- ') else sub.indent(pi) + 2
            at = pi + 1
            new = []
        else:
            idl = next(j for j in range(len(block)) if sub.text(block[j]).strip().startswith('operationId:'))
            at = idl + 1
            li = sub.indent(idl)
            new = [' ' * li + 'parameters:']
        pad = ' ' * li
        for p, desc, styp in plines:
            new += [f'{pad}- name: {p}', f'{pad}  in: path', f'{pad}  required: true', f'{pad}  description: {sq(desc)}',
                    f'{pad}  schema: {styp}']
        if plines:
            block[at:at] = [t + D.eol for t in new]
        # cut the operation out of its collection path
        D.delete(m, e)
        pl = D.find_path_item(src)
        pend = D.block_end(pl)
        if not any(not D.blank(j) for j in range(pl + 1, pend)):
            pend2 = D.end_trim(pend)
            D.delete(pl, max(pend2, pl + 1))
            insert_at = pl
            gone = True
        else:
            insert_at = D.end_trim(D.block_end(pl))
            gone = False
        tl = D.find_path_item(target)
        if tl is not None:
            at2 = D.end_trim(D.block_end(tl))
            D.lines[at2:at2] = block
        else:
            D.lines[insert_at:insert_at] = [f'  {target}:' + D.eol] + block
            all_paths.add(target)
        D.dirty = True
        report['K'].append({'op': oid, 'from': src, 'to': target, 'params': params,
                            'into_existing': tl is not None, 'source_item_removed': gone, 'contract': f['contract']})
    if APPLY:
        D.save()
json.dump(report, open(S / 'noaddr-applied.json', 'w', encoding='utf-8'), indent=1)
print(len(report['S']), 'singletons', len(report['K']), 'path keys', 'applied' if APPLY else '(dry run)')
