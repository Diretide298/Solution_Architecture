import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'docs/active/breaking-changes.yaml'
raw = p.read_bytes().decode('utf-8')
i = raw.index('  # BC-340 to BC-367')
p.write_bytes(raw[:i].encode('utf-8'))
print('stripped', len(raw) - i)
