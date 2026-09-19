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

    # **`schemas:` is not always the first key under `components:`.** `approvals.yaml`
    # opens with `securitySchemes:`, and assuming the order sent the splice looking for
    # a marker that was never going to be there.
    ci = t.find('\ncomponents:\n')
    if ci < 0:
        sys.exit('no "components:" block in %s' % target)
    si = t.find('\n  schemas:\n', ci)
    if si < 0:
        sys.exit('no "  schemas:" under components: in %s' % target)
    marker = '\n  schemas:\n'
    # **Three regions, and the paths go in the first of them.** `paths:` ends where
    # `components:` begins, so appending to "everything before `schemas:`" appends
    # *inside* `components:` — which is what the first cut of this did. The YAML stayed
    # valid, the file looked right, and thirteen operations vanished from `paths`.
    before_components = t[:ci]
    components_head = t[ci:si]
    after_schemas_key = t[si + len(marker):]

    clash = set(keys_at(before_components, 2)) & set(keys_at(paths + '\n', 2))
    if clash:
        sys.exit('path key already present, refusing: %s' % ', '.join(sorted(clash)))
    clash = set(keys_at(after_schemas_key, 4)) & set(keys_at(schemas + '\n', 4))
    if clash:
        sys.exit('schema already present, refusing: %s' % ', '.join(sorted(clash)))

    expected = set(re.findall(r'^\s*operationId:\s*(\S+)', paths, re.M))
    new = (before_components.rstrip('\n') + '\n' + paths + '\n'
           + components_head + marker + schemas + '\n' + after_schemas_key)
    io.open(target, 'w', encoding='utf8').write(new)

    d = yaml.safe_load(io.open(target, encoding='utf8'))
    ops = [o['operationId'] for p, v in (d.get('paths') or {}).items()
           for m, o in v.items() if isinstance(o, dict) and o.get('operationId')]
    dup = [k for k, c in collections.Counter(ops).items() if c > 1]
    txt = io.open(target, encoding='utf8').read()
    missing = sorted(set(re.findall(r'(?<!yaml)#/components/schemas/(\w+)', txt))
                     - set((d.get('components') or {}).get('schemas') or {}))
    # **The check that the first cut lacked, and it is the important one.** A splice can
    # produce a file that parses, resolves every reference and has no duplicates, while
    # putting the new operations somewhere nothing will ever read them. Verify by
    # presence in the parsed `paths`, not by the file looking plausible.
    landed = sorted(expected - set(ops))
    print('%s: %d paths, %d operations, %d schemas' % (
        target, len(d['paths']), len(ops), len(d['components']['schemas'])))
    if dup:
        print('  DUPLICATE operationIds: %s' % ', '.join(dup))
    if missing:
        print('  DANGLING local $refs: %s' % ', '.join(missing))
    if landed:
        print('  NOT IN paths (%d): %s' % (len(landed), ', '.join(landed[:8])))
    if not dup and not missing and not landed:
        print('  clean — %d new operation(s) landed in paths' % len(expected))


if __name__ == '__main__':
    main()
