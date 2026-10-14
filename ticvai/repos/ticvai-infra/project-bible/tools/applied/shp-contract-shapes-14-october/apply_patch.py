"""C-PATCH-FULL-BODY: an Update<X>Request (minProperties 1, no required, no defaults, request only) holding the
resource's caller-sendable properties, copied line for line; the PATCH body points at it.
    python -I apply_patch.py <root> [--apply]"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from yedit import Doc, sq
root = Path(sys.argv[1])
APPLY = '--apply' in sys.argv
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
ops = g.operations()
by, names = g.schemas()
PAIRS = [('updateDonationCampaign', 'DonationCampaign'), ('updatePartnerAgreement', 'PartnerAgreement'),
         ('updateRotaAssignment', 'RotaAssignment'), ('updateTableReservation', 'TableReservation')]
for oid, sname in PAIRS:
    f = ops[oid]
    s = by[(f['contract'], sname)]
    ro = {p for p, v in (s.get('properties') or {}).items() if isinstance(v, dict) and v.get('readOnly')}
    table = str(s.get('x-ticvai-persistence') or '').strip('"')
    new = 'Update' + sname + 'Request'
    assert (f['contract'], new) not in by, new
    D = Doc(root / f['file'])
    si = D.find_schema(sname)
    send = D.end_trim(D.block_end(si))
    pi = D.child(si, 'properties')
    ind = D.indent(si)
    kept, dropped = [], []
    j = pi + 1
    pend = D.block_end(pi)
    ci = D.child_indent(pi)
    out = []
    while j < pend:
        if D.blank(j) or D.indent(j) != ci:
            j += 1
            continue
        name = D.text(D.lines[j]).strip().split(':', 1)[0].strip('\'"')
        e = D.end_trim(D.block_end(j))
        if name in ro:
            dropped.append(name)
        else:
            kept.append(name)
            blk = [D.text(x) for x in D.lines[j:e]]
            # drop a default directly under the property
            k = 1
            while k < len(blk):
                t = blk[k]
                if len(t) - len(t.lstrip(' ')) == ci + 2 and t.strip().startswith('default:'):
                    m = k + 1
                    while m < len(blk) and (not blk[m].strip() or len(blk[m]) - len(blk[m].lstrip(' ')) > ci + 2):
                        m += 1
                    del blk[k:m]
                    continue
                k += 1
            blk = [re.sub(r':\s*&id\d+\s*$', ':', t) for t in blk]
            out += blk
        j = D.block_end(j)
    assert not any('*id' in t for t in out), (oid, 'alias in copy')
    pad = ' ' * ind
    desc = (f"**A partial update of {sname}** (the CR-089 pattern; CHG-SHP-008): `{oid}` sends only what changes, and a "
            f"field left out keeps its stored value. Nothing is required and nothing has a default, so a generated client "
            f"never resends a value it did not mean to change. The server's own fields ({', '.join(sorted(dropped)) or 'none'}) "
            f"are not sendable.")
    lines = [f'{pad}{new}:', f'{pad}  type: object', f'{pad}  x-ticvai-persistence: none — request only; a partial update of {table}',
             f'{pad}  description: {sq(desc)}', f'{pad}  minProperties: 1', f'{pad}  properties:'] + out
    # point the PATCH body at it (requestBody block only)
    m, end = D.find_op(oid)
    rb = D.child(m, 'requestBody', end)
    rbe = D.block_end(rb)
    hits = [x for x in range(rb, rbe) if f"#/components/schemas/{sname}'" in D.lines[x]]
    assert len(hits) == 1, (oid, hits)
    D.lines[hits[0]] = D.lines[hits[0]].replace(f"#/components/schemas/{sname}'", f"#/components/schemas/{new}'")
    D.dirty = True
    si = D.find_schema(sname)
    send = D.end_trim(D.block_end(si))
    D.insert(send, lines)
    print(oid, new, 'kept', len(kept), 'dropped', dropped)
    if APPLY:
        D.save()
