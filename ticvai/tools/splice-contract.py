# -*- coding: utf-8 -*-
"""Add paths and schemas to an existing contract without silently overwriting either.

**This exists because of a real, silent failure.** Splicing `/resource-bookings:` into
`resources.yaml` when that path key already existed produced valid YAML in which the
later mapping replaced the earlier one — taking `bookResource` with it. Nothing
complained. `check-package` then reported *"screen WEB-031 calls 'bookResource', which
does not exist"*, three steps away from the cause.

So the splice refuses on a collision instead of producing it, and says which key.

    python tools/splice-contract.py <contract.yaml> <paths.yaml> <schemas.yaml>
"""
import collections
import io
import re
import sys

import yaml


def keys_at(text, indent):
    pat = re.compile(r'^%s([^\s#][^:]*):\s*$' % (' ' * indent), re.M)
    return pat.findall(text)


def main():
    target, paths_file, schemas_file = sys.argv[1], sys.argv[2], sys.argv[3]
    t = io.open(target, encoding='utf8').read()
    paths = io.open(paths_file, encoding='utf8').read().rstrip('\n')
    schemas = io.open(schemas_file, encoding='utf8').read().rstrip('\n')

    marker = '\ncomponents:\n  schemas:\n'
    if marker not in t:
        sys.exit('no "components:/  schemas:" marker in %s' % target)
    head, tail = t.split(marker, 1)

    clash = set(keys_at(head, 2)) & set(keys_at(paths + '\n', 2))
    if clash:
        sys.exit('path key already present, refusing: %s' % ', '.join(sorted(clash)))
    clash = set(keys_at(tail, 4)) & set(keys_at(schemas + '\n', 4))
    if clash:
        sys.exit('schema already present, refusing: %s' % ', '.join(sorted(clash)))

    new = head.rstrip('\n') + '\n' + paths + '\n' + marker + schemas + '\n' + tail
    io.open(target, 'w', encoding='utf8').write(new)

    d = yaml.safe_load(io.open(target, encoding='utf8'))
    ops = [o['operationId'] for p, v in (d.get('paths') or {}).items()
           for m, o in v.items() if isinstance(o, dict) and o.get('operationId')]
    dup = [k for k, c in collections.Counter(ops).items() if c > 1]
    txt = io.open(target, encoding='utf8').read()
    missing = sorted(set(re.findall(r'(?<!yaml)#/components/schemas/(\w+)', txt))
                     - set((d.get('components') or {}).get('schemas') or {}))
    print('%s: %d paths, %d operations, %d schemas' % (
        target, len(d['paths']), len(ops), len(d['components']['schemas'])))
    if dup:
        print('  DUPLICATE operationIds: %s' % ', '.join(dup))
    if missing:
        print('  DANGLING local $refs: %s' % ', '.join(missing))
    if not dup and not missing:
        print('  clean')


if __name__ == '__main__':
    main()
