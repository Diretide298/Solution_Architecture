#!/usr/bin/env bash
# Regenerate every derived artefact, in dependency order.
#
# Run this after any change to contracts, screens, flows, states or events. Everything below is
# derived; nothing in it should ever be edited by hand. The order matters — the domain closure
# reads the lineage, and the status reads the closure.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 tools/derive-schema.py
python3 tools/link-screens-contracts.py

python3 - <<'PY'
import yaml, glob, json
lin = json.load(open('handoff/api-data-lineage.json'))
idx = {}
for f in sorted(glob.glob('screens/P*.yaml')):
    d = yaml.safe_load(open(f)); p = d['platform']
    for s in d['screens']:
        ops = [a.get('operationId') for a in (s.get('apis') or []) if a.get('operationId')]
        reads, writes, svcs, stores = set(), set(), set(), set()
        for o in ops:
            v = lin.get(o)
            if not v: continue
            reads |= set(v['reads']); writes |= set(v['writes'])
            if v.get('service'): svcs.add(v['service'])
            stores |= set(v.get('stores') or [])
        idx[s['id']] = dict(name=s['name'], platform=p['code'], platformName=p['shortName'],
            operator=p.get('operator'), app=p['app'], route=s['implementation']['route'],
            board=(s.get('wireframe') or {}).get('board'), operations=ops, services=sorted(svcs),
            stores=sorted(stores), reads=sorted(reads), writes=sorted(writes), storedProcedures=[],
            wave=s['wave'], offline=bool((s.get('states') or {}).get('offline')), specified=True,
            exits=(s.get('navigation') or {}).get('exitTo') or [])
json.dump(idx, open('handoff/screen-index.json', 'w'), indent=1)
print(f"screen-index: {len(idx)}")
PY

for d in ai; do
  python3 tools/derive-domain.py "$d" --quiet
  python3 tools/build-status.py --domain "$d" >/dev/null
  python3 tools/render-domain.py "$d"
done

python3 tools/build-audience.py
python3 tools/build-status.py
python3 tools/build-status.py --domain ai
python3 tools/sync-counts.py

echo
for t in check-screens check-frontend check-flows check-states check-config-scope check-wireframes check-package; do
  printf "  %-22s" "$t"; python3 "tools/$t.py" 2>&1 | tail -1
done
