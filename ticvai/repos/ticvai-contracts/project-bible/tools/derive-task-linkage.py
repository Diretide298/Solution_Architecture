# -*- coding: utf-8 -*-
"""Link screens to operations by what they DO, not by what they are called.

`derive-pack-linkage.py` matches a screen title against an operation name. That is
a real signal and it wired 629 screens, but it has two ceilings it cannot pass:

**It reads the title and nothing else.** Every pack screen also carries `Actions`,
`Configure`, `Capture`, `Show` and `Display` sections — 250, 234, 58, 137 and 226
screens respectively — and those say what the screen does. `Approve or reject the
application` is a task. The title never mentions it.

**A title is one thing, so it yields one operation.** A screen that lists, filters,
approves and exports gets a single `list*` and the other three are lost. Real screens
call four or five operations; the title-matched ones average one.

So this matches **task by task**. A screen's tasks come from its action-bearing
sections; an operation's identity comes from its verb, its path, the tables it reads
and writes, and its summary — not just its name. Each task that matches wires its own
operation, so one screen can gain several.

**What it will not do is invent an operation.** A task with no operation behind it is
left for `workshop-contract-gap.md`, exactly as before. The point is to stop authoring
an operation that already exists under a name the title did not guess.

    python tools/derive-task-linkage.py              measure the lift, write nothing
    python tools/derive-task-linkage.py --apply      wire the matches into screens/
"""
import collections
import glob
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, 'sources', 'workshop', 'pack.json')
LINEAGE = os.path.join(ROOT, 'handoff', 'api-data-lineage.json')

# Sections whose lines describe something the screen DOES. `Purpose` is prose about
# why it exists and `Example` is sample data; neither names a task.
TASK_SECTIONS = ('Actions', 'Configure', 'Capture', 'Show', 'Display', 'Support',
                 'Filters', 'Result', 'Scope of Work', 'Acceptance Condition')

# A task phrase leads with a verb. These map the client's vocabulary onto the verb
# an operationId would use.
TASK_VERB = {
    'list': 'list', 'view': 'list', 'show': 'list', 'display': 'list', 'browse': 'list',
    'see': 'list', 'monitor': 'list', 'track': 'list', 'search': 'search', 'filter': 'list',
    'find': 'search', 'look': 'list', 'report': 'list', 'audit': 'list', 'review': 'list',
    'create': 'create', 'add': 'create', 'new': 'create', 'define': 'create', 'issue': 'issue',
    'generate': 'create', 'raise': 'create', 'register': 'register', 'enrol': 'enrol',
    'enroll': 'enrol', 'record': 'record', 'capture': 'record', 'submit': 'submit',
    'edit': 'update', 'update': 'update', 'change': 'update', 'modify': 'update',
    'configure': 'set', 'set': 'set', 'manage': 'update', 'maintain': 'update',
    'assign': 'assign', 'map': 'assign', 'link': 'assign', 'allocate': 'assign',
    'approve': 'approve', 'reject': 'reject', 'decline': 'reject', 'authorise': 'approve',
    'authorize': 'approve', 'publish': 'publish', 'activate': 'activate',
    'deactivate': 'deactivate', 'suspend': 'deactivate', 'cancel': 'cancel', 'void': 'void',
    'delete': 'delete', 'remove': 'remove', 'revoke': 'revoke', 'release': 'release',
    'export': 'export', 'download': 'export', 'import': 'import', 'upload': 'import',
    'validate': 'validate', 'verify': 'validate', 'check': 'validate', 'simulate': 'simulate',
    'preview': 'simulate', 'test': 'validate', 'reconcile': 'reconcile', 'resolve': 'resolve',
    'override': 'override', 'refund': 'refund', 'transfer': 'transfer', 'extend': 'update',
}

STOP = set('''a an the of for to in with per by on at from into its it this that and or is are
be can may must should all any each every other via using their its when where which what who
new same only more most less least such than then also not no yes if while during after before
screen page view tab section panel list item items data record records value values field fields
system user users staff guest venue tenant across within based over under between'''.split())


def singular(w):
    if w.endswith('ies') and len(w) > 4:
        return w[:-3] + 'y'
    if w.endswith('s') and not w.endswith('ss') and len(w) > 3:
        return w[:-1]
    return w


def nouns(text):
    out = set()
    for w in re.findall(r'[A-Za-z]{3,}', text.lower()):
        if w in STOP or w in TASK_VERB:
            continue
        out.add(singular(w))
    return out


# ---------------------------------------------------------------- operations

def operations():
    """operationId -> (verb, entity tokens, raw record).

    **The entity comes from four places, not one.** `setBrandIdentity` is obvious from
    its name; `POST /venues/{id}/zones/{zid}/close` is not, and its tables say
    `access.zone` while its summary says *Close a zone*. Pooling all four is what lets
    a task phrase reach an operation whose name does not contain the word.
    """
    lin = json.load(io.open(LINEAGE, encoding='utf8'))
    out = {}
    for oid, r in lin.items():
        parts = [p.lower() for p in re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', oid)]
        verb = parts[0] if parts and parts[0] in set(TASK_VERB.values()) else None
        ent = {singular(p) for p in parts[1:] if len(p) > 2 and p not in STOP}
        for seg in re.findall(r'[a-z]+', r.get('path', '').lower()):
            if len(seg) > 2 and seg not in STOP:
                ent.add(singular(seg))
        for tbl in (r.get('reads') or []) + (r.get('writes') or []):
            for seg in re.findall(r'[a-z]+', tbl.split('.')[-1].lower()):
                if len(seg) > 2:
                    ent.add(singular(seg))
        ent |= nouns(r.get('summary') or '')
        out[oid] = (verb, ent, r)
    return out


# ---------------------------------------------------------------- screens

def tasks(screen):
    """[(verb, entity tokens)] — one per action phrase the screen declares."""
    found = []
    for name, lines in (screen.get('sections') or {}).items():
        if name not in TASK_SECTIONS:
            continue
        for line in lines:
            for phrase in re.split(r'[;|•]|\s{2,}', line):
                words = re.findall(r'[A-Za-z]{2,}', phrase.lower())
                if not words:
                    continue
                verb = next((TASK_VERB[w] for w in words[:3] if w in TASK_VERB), None)
                if not verb:
                    continue
                ent = nouns(phrase)
                if ent:
                    found.append((verb, ent))
    return found


def build_df(ops):
    """How many operations use each entity token. `scan` is common; `chargeback` is not."""
    df = collections.Counter()
    for _oid, (_v, ent, _r) in ops.items():
        for w in ent:
            df[w] += 1
    return df


def score(task_ent, op_ent, df, nops):
    """Rare-term overlap, not Jaccard and not containment.

    **Jaccard punishes the operation for being well described.** The entity set here
    pools the operationId, the path, every table read or written and the summary, so a
    well-specified operation carries twenty tokens and a three-word task can never
    reach 0.5 against it. The first run of this tool scored that way and lifted
    coverage by one point.

    **Containment fails the other way, and `derive-pack-linkage.py` already paid for
    it**: an operation with a tiny vocabulary wins every containment measure, which is
    how eight unrelated screens all matched `listScans` at 0.75.

    So weight by rarity. A token shared by half the operations says nothing; a token
    two operations use says almost everything. The task's rarest token must be one the
    operation has, or there is no match at all.
    """
    if not task_ent or not op_ent:
        return 0.0
    shared = task_ent & op_ent
    if not shared:
        return 0.0
    rarest = min(task_ent, key=lambda w: df.get(w, 0))
    if rarest not in op_ent:
        return 0.0
    import math
    got = sum(math.log(nops / float(1 + df.get(w, 0))) for w in shared)
    want = sum(math.log(nops / float(1 + df.get(w, 0))) for w in task_ent)
    return got / want if want else 0.0


WIRE_AT = 0.45


def main():
    ops = operations()
    df = build_df(ops)
    nops = float(len(ops))
    pack = json.load(io.open(PACK, encoding='utf8'))

    # what the screens already declare, so the lift is measured against reality
    declared = {}
    for f in glob.glob(os.path.join(ROOT, 'screens', 'P*.yaml')):
        d = yaml.safe_load(io.open(f, encoding='utf8')) or {}
        for s in d.get('screens') or []:
            src = s.get('source') or {}
            key = (src.get('pack'), str(src.get('board')), str(src.get('number')))
            if src.get('pack'):
                declared[key] = (f, s)

    gained = collections.Counter()
    new_refs = 0
    screens_lifted = 0
    per_screen = {}

    for sc in pack:
        key = (sc.get('source'), str(sc.get('board')), str(sc.get('number')))
        hit = declared.get(key)
        if not hit:
            continue
        f, s = hit
        have = {a.get('operationId') for a in (s.get('apis') or [])}
        title_ent = nouns(sc.get('title', ''))
        picks = {}
        for verb, ent in tasks(sc):
            best, best_s = None, 0.0
            for oid, (overb, oent, _r) in ops.items():
                if overb and overb != verb:
                    continue
                sc_ = score(ent | title_ent, oent, df, nops)
                if sc_ > best_s:
                    best, best_s = oid, sc_
            if best and best_s >= WIRE_AT and best not in have:
                picks[best] = max(best_s, picks.get(best, 0))
        if picks:
            per_screen[s['id']] = picks
            new_refs += len(picks)
            if not have:
                screens_lifted += 1
            gained[f] += 1

    total = len(declared)
    withops = sum(1 for _f, s in declared.values() if (s.get('apis') or []))
    print('pack screens in the package      : %d' % total)
    print('  already declare an operation   : %d  (%.0f%%)' % (withops, 100.0 * withops / total))
    print('  gain at least one from tasks   : %d' % len(per_screen))
    print('  of those, had NONE before      : %d' % screens_lifted)
    print('  new operation references       : %d' % new_refs)
    print()
    print('coverage %.0f%% -> %.0f%%'
          % (100.0 * withops / total, 100.0 * (withops + screens_lifted) / total))
    print()
    for sid, picks in list(per_screen.items())[:8]:
        print('  %-9s %s' % (sid, ', '.join('%s (%.2f)' % (k, v) for k, v in
                                            sorted(picks.items(), key=lambda x: -x[1])[:4])))
    if '--apply' not in sys.argv:
        print('\n  nothing written — pass --apply')
        return
    # wiring deferred: see the report first
    print('\n  --apply is not implemented until the sample above is reviewed')


if __name__ == '__main__':
    main()
