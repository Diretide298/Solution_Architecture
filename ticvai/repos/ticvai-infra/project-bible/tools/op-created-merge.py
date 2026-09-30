"""Add the ids tools/op-create.rb made on the server to pms-map.json.

    python tools/op-created-merge.py op-created.json
"""
import json
import sys
from pathlib import Path

MAP = Path(__file__).resolve().parents[1] / "handoff" / "service-docs" / "pms-map.json"
made = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
mp = json.loads(MAP.read_text(encoding="utf-8"))
clash = {k: (mp[k], v) for k, v in made.items() if k in mp and mp[k] != v}
if clash:
    sys.exit(f"already mapped to a different id: {clash}")
new = {k: v for k, v in made.items() if k not in mp}
# op-create.rb finds a ticket by its subject under the same parent. When a task is split, the old ticket can match
# the new half while the map still gives it to the other half (30 September: SVC-WALLET-RETAIL-1/-2). Two keys on
# one ticket put one task's links and text on another's ticket, so stop and repair instead.
owner = {v: k for k, v in mp.items() if isinstance(v, int)}
shared = {k: (v, owner[v]) for k, v in new.items() if v in owner}
if shared:
    sys.exit(f"these new keys were matched to a ticket another key already has (key: (id, other key)): {shared}")
mp.update(new)
MAP.write_text(json.dumps(mp, indent=1), encoding="utf-8")
print(f"{len(new)} added to {MAP.name}, {len(made) - len(new)} were already there")
