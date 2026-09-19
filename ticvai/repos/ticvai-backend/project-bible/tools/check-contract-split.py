# -*- coding: utf-8 -*-
"""Is a contract's unused half a missing join, or real drift?

**This is the test `seating` taught.** The audit ranks a contract `JOIN OR DRIFT` when
many of its operations reach no screen *and* many board screens in its domain call
nothing. Those two facts have two possible causes and they need opposite work:

    a missing join   the contract is right and nothing points at half of it
    real drift       the contract models something the boards do not describe

`seating` looked like the second and was the first. Its 14 runtime operations were all
called and its 21 authoring operations were called by nothing — a clean split along one
line, with the unserved screens sitting exactly on the idle side. Wiring them took it to
zero unused without a line of contract change, and writing the 21 operations the gap list
proposed would have produced 21 duplicates.

So the test is **concentration**. Bucket every operation by what it does, then ask where
the unused ones fell:

    concentrated in one or two buckets  -> a missing join. Wire, do not author.
    spread across every bucket          -> drift. Read the contract against the boards.

**It reports, it never writes**, and it settles nothing on its own — a bucket is a guess
from a verb, and two contracts can split the same way for different reasons.

    python tools/check-contract-split.py                  every contract the audit flagged
    python tools/check-contract-split.py orders catalogue  named ones
"""
import collections
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# What an operation does, by the verb it leads with. The buckets matter more than the
# names: `authoring` and `import` are the two that a board fills and a runtime screen
# never touches, which is why an unused set concentrated there means an unwired board.
BUCKET = {
    'authoring': ('create', 'update', 'set', 'configure', 'define', 'clone', 'copy',
                  'publish', 'unpublish', 'validate', 'simulate', 'preview', 'draft',
                  'activate', 'deactivate', 'archive', 'restore', 'rename', 'reorder'),
    'import':    ('import', 'upload', 'commit', 'ingest', 'parse', 'map', 'sync'),
    'read':      ('list', 'get', 'search', 'find', 'lookup', 'export', 'download',
                  'diff', 'compare', 'recommend', 'suggest', 'preview'),
    'lifecycle': ('approve', 'reject', 'submit', 'withdraw', 'cancel', 'void', 'revoke',
                  'issue', 'reissue', 'extend', 'renew', 'suspend', 'resume', 'close'),
    'money':     ('charge', 'refund', 'settle', 'reconcile', 'capture', 'authorise',
                  'authorize', 'payout', 'invoice', 'credit', 'debit', 'topup', 'top'),
    'runtime':   ('hold', 'release', 'relinquish', 'allocate', 'assign', 'unassign',
                  'scan', 'validate', 'redeem', 'check', 'record', 'log', 'notify',
                  'send', 'trigger', 'run', 'replay', 'retry', 'start', 'stop', 'pause'),
    'delete':    ('delete', 'remove', 'purge'),
}
VERB_BUCKET = {}
for b, verbs in BUCKET.items():
    for v in verbs:
        VERB_BUCKET.setdefault(v, b)


def bucket_of(oid):
    parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', oid)
    if not parts:
        return 'other'
    return VERB_BUCKET.get(parts[0].lower(), 'other')


def main():
    want = [a for a in sys.argv[1:] if not a.startswith('-')]

    used = set()
    for f in glob.glob(os.path.join(ROOT, 'screens', 'P*.yaml')):
        used |= set(re.findall(r'operationId:\s*(\S+)',
                               io.open(f, encoding='utf8', errors='replace').read()))

    for path in sorted(glob.glob(os.path.join(ROOT, 'contracts', '*', '*.yaml'))):
        name = os.path.basename(path)[:-5]
        if want and name not in want:
            continue
        ops = sorted(set(re.findall(r'^\s*operationId:\s*(\S+)',
                                    io.open(path, encoding='utf8', errors='replace').read(), re.M)))
        if not ops:
            continue
        unused = [o for o in ops if o not in used]
        if not unused:
            continue

        per = collections.defaultdict(lambda: [0, 0])      # bucket -> [total, unused]
        for o in ops:
            b = bucket_of(o)
            per[b][0] += 1
            if o in unused:
                per[b][1] += 1

        # concentration: what share of the unused sits in the two biggest buckets, and
        # how many buckets are wholly idle
        ranked = sorted(per.items(), key=lambda kv: -kv[1][1])
        top2 = sum(v[1] for _k, v in ranked[:2])
        conc = top2 / float(len(unused))
        dead = [k for k, v in per.items() if v[0] and v[1] == v[0]]

        call = 'MISSING JOIN' if conc >= 0.75 and dead else 'drift — read it'
        print('\n%-16s %d ops, %d unused   concentration %.0f%%   -> %s'
              % (name, len(ops), len(unused), 100 * conc, call))
        for b, (tot, un) in ranked:
            if not tot:
                continue
            flag = '   <- wholly idle' if un == tot else ''
            print('     %-10s %3d ops  %3d unused%s' % (b, tot, un, flag))
        if dead:
            print('     wholly idle bucket(s): %s' % ', '.join(sorted(dead)))
        print('     e.g. %s' % ', '.join(unused[:6]))


if __name__ == '__main__':
    main()
