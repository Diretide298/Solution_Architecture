#!/usr/bin/env python3
"""Refresh the project-bible mirrors under repos/ from the canonical docs/ and handoff/.

The mirrors exist so a developer working inside one code repo has the design context
without cloning the docs repo. Copying without a sync step guarantees drift, and it drifted
78% in a single day of work. This makes the copies true on every refresh.
"""
import hashlib, pathlib, sys

def digest(p): return hashlib.md5(p.read_bytes()).hexdigest()

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    src = {}
    for d in ('docs', 'handoff'):
        for f in (root/d).rglob('*'):
            if f.is_file() and f.suffix in ('.md', '.json'):
                src.setdefault(f.name, f)          # first wins; docs/ before handoff/
    updated = orphaned = checked = 0
    for f in (root/'repos').rglob('*'):
        if not f.is_file() or f.suffix not in ('.md', '.json'):
            continue
        s = src.get(f.name)
        if s is None:
            orphaned += 1
            continue
        checked += 1
        if digest(f) != digest(s):
            f.write_bytes(s.read_bytes())
            updated += 1
    print(f"  project-bible: {checked} mirrored, {updated} refreshed, {orphaned} repo-local")
    return 0

if __name__ == '__main__':
    sys.exit(main())
