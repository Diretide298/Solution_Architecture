import sys, json, importlib.util
from pathlib import Path
root = Path(sys.argv[1])
out = sys.argv[2]
sys.path.insert(0, str(root / 'tools'))
import audit_guard as g
captured = {}


def fin(self, limit=12):
    captured.update(self.found)
    return 0


g.Guard.finish = fin
spec = importlib.util.spec_from_file_location('ccs', root / 'tools' / 'check-contract-shapes.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
sys.argv = ['x']
m.main()
json.dump(captured, open(out, 'w', encoding='utf-8'), indent=1)
for r, v in captured.items():
    if v:
        print(r, len(v))
