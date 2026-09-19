# -*- coding: utf-8 -*-
"""Before authoring a contract, ask which contracts the board actually belongs to.

**The audit attributes a pack to one contract — the one its wired screens name most
often — and that is wrong for a large board.** `Resource_Management_Configuration_
Reference.pdf` has ten boards, and two of them are rotas, attendance, overtime and
labour cost, which is `workforce`. `Rental_Management.pdf` has a maintenance board
sitting on top of a 36-operation `maintenance` contract that serves one screen of it.

Attributing all 199 screens to `resources` and authoring against them would have
written work orders, inspections, stock transfers and rota assignments that already
exist. **That is the seating mistake at pack scale.**

So this scores every unserved screen against every operation in every contract, board
by board, using the rare-term matcher from `derive-task-linkage.py`, and reports:

    a board where one existing contract wins most screens   -> a missing join
    a board where nothing scores anywhere                   -> real authoring

**It reports, it never writes.** A match here is a candidate, not a wiring — the
threshold is deliberately lower than `WIRE_AT` because the question is "does anything
plausibly cover this", not "wire it".

    python tools/scope-pack-to-contracts.py Resource_Management Rental_Management
"""
import collections
import glob
import io
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
_spec = importlib.util.spec_from_file_location(
    'dtl', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'derive-task-linkage.py'))
dtl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dtl)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, 'sources', 'workshop', 'pack.json')

CANDIDATE_AT = 0.35


def op_contract():
    out = {}
    for f in glob.glob(os.path.join(ROOT, 'contracts', '*', '*.yaml')):
        name = os.path.basename(f)[:-5]
        for oid in re.findall(r'^\s*operationId:\s*(\S+)',
                              io.open(f, encoding='utf8', errors='replace').read(), re.M):
            out[oid] = name
    return out


def main():
    want = [a for a in sys.argv[1:] if not a.startswith('-')]
    ops = dtl.operations()
    df = dtl.build_df(ops)
    nops = float(len(ops))
    owner = op_contract()

    declared = {}
    for f in glob.glob(os.path.join(ROOT, 'screens', 'P*.yaml')):
        d = yaml.safe_load(io.open(f, encoding='utf8')) or {}
        for s in d.get('screens') or []:
            src = s.get('source') or {}
            if src.get('pack'):
                declared[(src['pack'], str(src.get('board')), str(src.get('number')))] = s

    pack = json.load(io.open(PACK, encoding='utf8'))
    boards = collections.defaultdict(lambda: {'n': 0, 'served': 0, 'nomatch': [],
                                              'hits': collections.Counter(),
                                              'best': []})

    for sc in pack:
        src = sc.get('source') or ''
        if want and not any(w in src for w in want):
            continue
        s = declared.get((src, str(sc.get('board')), str(sc.get('number'))))
        if not s:
            continue
        b = boards[(src, str(sc.get('board')))]
        b['n'] += 1
        if s.get('apis'):
            b['served'] += 1
            continue
        title_ent = dtl.nouns(sc.get('title', ''))
        found = {}
        for verb, ent in dtl.tasks(sc):
            for oid, (overb, oent, _r) in ops.items():
                if overb and overb != verb:
                    continue
                v = dtl.score(ent | title_ent, oent, df, nops)
                if v >= CANDIDATE_AT and v > found.get(oid, 0):
                    found[oid] = v
        if not found:
            b['nomatch'].append((s['id'], s['name']))
            continue
        top = sorted(found.items(), key=lambda x: -x[1])[:5]
        for oid, _v in top:
            b['hits'][owner.get(oid, '?')] += 1
        b['best'].append((s['id'], s['name'], top[0][0], owner.get(top[0][0], '?'), top[0][1]))

    for (src, bno), b in sorted(boards.items(), key=lambda kv: (kv[0][0], int(kv[0][1]))):
        unserved = b['n'] - b['served']
        win = b['hits'].most_common(3)
        share = (100.0 * win[0][1] / sum(b['hits'].values())) if b['hits'] else 0
        call = ('AUTHOR — nothing covers it' if len(b['nomatch']) >= 0.6 * max(unserved, 1)
                else 'JOIN to `%s`' % win[0][0] if win and share >= 45
                else 'MIXED — read it')
        print('\n%-46s board %-3s  %2d screens, %2d unserved   -> %s'
              % (os.path.splitext(src)[0][:46], bno, b['n'], unserved, call))
        print('     no candidate anywhere: %d' % len(b['nomatch']))
        if win:
            print('     candidates by contract: %s'
                  % ', '.join('%s %d' % (k, v) for k, v in win))
        for sid, name, oid, c, v in b['best'][:4]:
            print('       %-8s %-40s %s.%s (%.2f)' % (sid, name[:40], c, oid, v))


if __name__ == '__main__':
    main()
