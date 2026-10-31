#!/usr/bin/env python3
"""Write handoff/screen-index.json: per screen, its operations and what they read, write and call (from the lineage).

**Run twice by refresh.sh** (31 October 2026, r12 integration, CHG-R12INT-001). It was an inline block late in the
refresh, but derive-relationships reads it early (the screens each table is used by), so a screen's new operation, or
a lineage change to what an operation writes, reached relationship-graph.json one refresh late and
check-regenerate-twice --chain failed on it. It reads only the screens and the lineage, so it now also runs after
derive-lineage, before derive-relationships; the run at the end gives the index the screens the derivers finished."""

import glob, json, os
import yaml
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the package root, as refresh.sh runs it
# **Every open in this block names its encoding.** Windows defaults to cp1252, and the moment a
# note in the lineage carried a curly quote the whole refresh died here — after the screens had
# been rewritten and before anything downstream ran, which is the worst place to stop.
lin = json.load(open('handoff/api-data-lineage.json', encoding='utf-8'))
idx = {}
for f in sorted(glob.glob('screens/P*.yaml')):
    d = yaml.safe_load(open(f, encoding='utf-8')); p = d['platform']
    for s in d['screens']:
        ops = [a.get('operationId') for a in (s.get('apis') or []) if a.get('operationId')]
        reads, writes, svcs, stores = set(), set(), set(), set()
        for o in ops:
            v = lin.get(o)
            if not v: continue
            reads |= set(v['reads']); writes |= set(v['writes'])
            if v.get('service'): svcs.add(v['service'])
            stores |= set(v.get('stores') or [])
        nav = s.get('navigation') or {}
        # **A destination id is not a transition.** Until 9 September this index carried `exits`
        # and nothing else about behaviour, so whoever built from it got a list of screen ids and
        # had to invent every trigger, every carried value and every drawer for themselves. The
        # fields below are the ones a builder cannot guess: how the move is made, what state
        # travels with it, what the screen holds mid-process, and what closing an overlay does.
        idx[s['id']] = dict(name=s['name'], platform=p['code'], platformName=p['shortName'],
            operator=p.get('operator'), app=p['app'], route=s['implementation']['route'],
            operations=ops, services=sorted(svcs),
            stores=sorted(stores), reads=sorted(reads), writes=sorted(writes), storedProcedures=[],
            wave=s['wave'], offline=bool((s.get('states') or {}).get('offline')), specified=True,
            exits=nav.get('exitTo') or [],
            pattern=s.get('pattern'), entryFrom=nav.get('entryFrom') or [],
            transitions=nav.get('transitions') or [],
            machine=s.get('machine') or None,
            states=s.get('states') or {},
            overlays=s.get('overlays') or [])
json.dump(idx, open('handoff/screen-index.json', 'w', encoding='utf-8'), indent=1)
print(f"screen-index: {len(idx)}")
