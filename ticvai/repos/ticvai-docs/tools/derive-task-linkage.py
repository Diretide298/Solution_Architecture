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

# **A whitelist of section names cannot work, and the measurement is unambiguous: the
# pack uses 7,092 distinct section headings.** The ten this tool started with are the
# head of that distribution and nothing else — past rank twelve every heading is the
# author's own words. `Rental_Management.pdf` calls its directories `Work Order
# Information`, `Expected Return` and `Attachments`; `Resource_Management_
# Configuration_Reference.pdf` uses `Backend Configuration` and `Administrators shall
# configure`. Across those two packs, 199 screens, the whitelist reached **15 `Actions`
# sections and 14 `Configure`** and skipped the rest — and the tool then reported that
# nothing in any contract covered them. **That was the whitelist, not the contracts.**
#
# So the rule is inverted. A section is prose unless proven otherwise is the wrong
# default; a section is a task directory unless it is *named* as prose.
PROSE_SECTION = re.compile(
    r'^\s*(purpose|examples?|for example|worked examples?|reason|rationale|note|notes|'
    r'important|important boundary|boundary|board objective|board \d+ owns|'
    r'ai recommendation|ai capability|recommendations?|recommended|overview|context|'
    r'background|description|summary|definition|why|scenario|outcome|benefit)\b', re.I)

# The verb a heading implies when its lines carry none. **`Work Order Information` is a
# directory of fields, which is a read; `Deposit & Security Hold Policy` is settings.**
SECTION_VERB = (
    (re.compile(r'config|set-?up|rule|polic|setting|parameter|threshold|template|'
                r'builder|model|structure|govern', re.I), 'set'),
    (re.compile(r'captur|record|log\b|intake', re.I), 'record'),
    (re.compile(r'approv|sign.?off|authoris|authoriz', re.I), 'approve'),
    (re.compile(r'validat|verif|inspect|check', re.I), 'validate'),
)

# Headings where a line without a verb is a label rather than a task, so the phrase
# must supply the verb itself. `Actions` was always this; acceptance text is prose
# with verbs in it, and reading a verbless acceptance line as a read invents work.
NO_IMPLIED_VERB = re.compile(r'^\s*(actions?|quick actions?|acceptance)', re.I)

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
system user users staff guest venue tenant across within based over under between
information detail details overview summary management center centre command control console
workspace dashboard home main general profile engine builder wizard configuration setup settings
requirement requirements capability capabilities module option options type types kind status
idempotency cache key header token request response payload'''.split())
# **The last two lines are the ones that were silently breaking matches.** `Work Order
# Information` contributes `information`, which appears in almost no operation — so the
# rarest-token guard picked it, found it absent from `createWorkOrder`, and scored zero.
# A structural noun is rare *and* meaningless, which is the one combination the rarity
# weighting cannot defend against. `idempotency` and `cache` leak in from the shared
# parameter `$ref` on every write operation and do the same damage from the other side.


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
            # **The whole qualified name, not the part after the last dot.**
            # `maintenance.work_order` was yielding `work` and `order` and throwing
            # away `maintenance` — the one token that says which domain the operation
            # belongs to. `createWorkOrder` was therefore invisible to any task phrase
            # mentioning maintenance, while `lookupAsset` matched at 1.00 because its
            # summary happened to contain the word.
            for seg in re.findall(r'[a-z]+', tbl.lower()):
                if len(seg) > 2 and seg not in STOP:
                    ent.add(singular(seg))
        ent |= nouns(r.get('summary') or '')
        out[oid] = (verb, ent, r)
    return out


# ---------------------------------------------------------------- screens

def implied_verb(name):
    """The verb a heading implies for its verbless lines — `list` unless it says otherwise."""
    if NO_IMPLIED_VERB.match(name):
        return None
    for rx, verb in SECTION_VERB:
        if rx.search(name):
            return verb
    return 'list'


def tasks(screen):
    """[(verb, entity tokens)] — one per task the screen states.

    **The verb-led phrase is the minority case and assuming otherwise caps this tool
    at a quarter of the pack.** 65% of screens carry a task-bearing section and only
    25% contain a phrase that leads with a verb, because `Display` and `Support` are
    column lists — `Tenant | Venue | Asset Type | Status | Owner` — and a column list
    is a read, stated in nouns.

    So a phrase with a verb uses that verb, and a phrase without one inherits the
    verb its section implies. `Actions` has no implied verb on purpose: a line there
    with no verb is a label, not a task.
    """
    found = []
    for name, lines in (screen.get('sections') or {}).items():
        prose = bool(PROSE_SECTION.match(name))
        # **Skipping a prose heading outright loses whole packs.**
        # `Marketing_CRM_Configuration_Reference` and `Seat_Management_Venue_Mapping`
        # are prose PDFs with no directories at all — 120 and 129 screens whose only
        # heading is `Purpose`, holding text like *"Maintain standard and custom
        # attributes… Define primary and external identifiers, source-system priority,
        # survivorship rules… Version and audit schema changes."* Those are tasks. The
        # tool reported 107 of 107 and 97 of 97 screens with no candidate operation in
        # any contract, against a `marketing-crm` that has 167 of them.
        #
        # What prose actually justifies is refusing to *infer* a verb, not refusing to
        # read the line. A verbless sentence under `Purpose` is background; one that
        # leads with `Maintain` or `Configure` is a task wherever it is written.
        implied = None if prose else implied_verb(name)
        # **The heading is part of the entity, not just the verb.** `Created Date`
        # under `Work Order Information` reaches nothing on its own; the same line
        # under that heading carries `work` and `order` and reaches
        # `maintenance.createWorkOrder`. This is the signal the whitelist threw away
        # even for the sections it did read.
        head_ent = set() if prose else nouns(name)
        for line in lines:
            for phrase in re.split(r'[;|•]|\s{2,}|(?<=[a-z])\.\s+', line):
                words = re.findall(r'[A-Za-z]{2,}', phrase.lower())
                if not words:
                    continue
                verb = next((TASK_VERB[w] for w in words[:3] if w in TASK_VERB), implied)
                if not verb:
                    continue
                ent = nouns(phrase) | head_ent
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
    # **A ratio alone lets a one-token task score 1.00 against anything.** `Export &
    # Download Center` matched `openShift`, `getCurrentSession` and `getEntitlementUsage`
    # at a perfect score, because a task carrying a single common token is wholly
    # contained by every operation that happens to use it. The ratio was right — all of
    # the task's evidence was present — and the evidence was worth nothing.
    #
    # So the shared evidence has to clear an absolute floor as well as a relative one.
    # `MIN_EVIDENCE` is roughly one term used by 2% of operations; a task whose overlap
    # is only common words never reaches it however complete the overlap is.
    if got < MIN_EVIDENCE:
        return 0.0
    return got / want if want else 0.0


MIN_EVIDENCE = 5.0


WIRE_AT = 0.45

# **One weak cross-domain hit is noise; two tasks agreeing on a contract is signal.**
# A CMS screen with an `Attachments` heading reaches `maintenance.attachWorkOrderEvidence`
# at 0.67, because attaching a document is genuinely what both do — the phrase is right
# and the domain is wrong, and no threshold separates those. What separates them is
# corroboration: a screen that really belongs to a contract matches several of its
# operations, not one.
CORROBORATE_AT = 0.60   # a single match this strong stands on its own


STRONG_ENOUGH_ALONE = 0.80   # clears the affinity guard on its own


def confirm(picks, owner, module=None, affinity=None):
    """Drop contracts a screen touched only once, only weakly, or out of its domain.

    `picks` is {operationId: score}; `owner` maps operationId -> contract. Returns the
    same shape with the unsupported contracts removed.

    **The second guard is the one that matters, and it is learned rather than written
    down.** Thresholds could not separate `Export & Download Center` from
    `identity.getCurrentSession` at 1.00, because the phrase really did match and only
    the domain was wrong. `affinity` is the set of contracts each `requiresModule`
    already calls across the 669 screens wired before this tool ran — `access` screens
    call `access` 94% of the time, `membership` screens call `subscription`. A proposal
    outside that set has to be very strong to stand.

    **It is deliberately a guard and not a filter.** A thin module like `resources`
    has only 19 existing references, so treating its affinity as complete would freeze
    today's bias in place and block the very wiring this run exists to find.
    """
    by_contract = collections.defaultdict(list)
    for oid, sc in picks.items():
        by_contract[owner.get(oid, '?')].append((oid, sc))
    keep = {}
    for c, items in by_contract.items():
        top = max(s for _o, s in items)
        if not (len(items) >= 2 or top >= CORROBORATE_AT):
            continue
        if affinity is not None and module and c not in affinity.get(module, ()):
            if top < STRONG_ENOUGH_ALONE:
                continue
        keep.update(dict(items))
    return keep


def module_affinity():
    """{requiresModule: {contracts it already calls}} — learned from what is wired."""
    lin = json.load(io.open(LINEAGE, encoding='utf8'))
    out = collections.defaultdict(set)
    for f in glob.glob(os.path.join(ROOT, 'screens', 'P*.yaml')):
        d = yaml.safe_load(io.open(f, encoding='utf8')) or {}
        for s in d.get('screens') or []:
            m = s.get('requiresModule')
            if not m:
                continue
            for a in (s.get('apis') or []):
                c = a.get('contract') or lin.get(a.get('operationId'), {}).get('contract')
                if c:
                    out[m].add(c)
    return out


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

    owner = {oid: (r.get('contract') or '?') for oid, (_v, _e, r) in ops.items()}
    affinity = module_affinity()
    only = None
    for a in sys.argv[1:]:
        if a.startswith('--only='):
            only = a.split('=', 1)[1]

    gained = collections.Counter()
    new_refs = 0
    screens_lifted = 0
    per_screen = {}
    per_file = collections.defaultdict(dict)

    for sc in pack:
        if only and only not in (sc.get('source') or ''):
            continue
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
        picks = confirm(picks, owner, s.get('requiresModule'), affinity)
        if picks:
            per_screen[s['id']] = picks
            per_file[f][s['id']] = picks
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
    by_contract = collections.Counter()
    for picks in per_screen.values():
        for oid in picks:
            by_contract[owner.get(oid, '?')] += 1
    print('references by contract:')
    for c, k in by_contract.most_common(12):
        print('    %-16s %d' % (c, k))
    print()
    for sid, picks in list(per_screen.items())[:8]:
        print('  %-9s %s' % (sid, ', '.join('%s (%.2f)' % (k, v) for k, v in
                                            sorted(picks.items(), key=lambda x: -x[1])[:4])))
    if '--apply' not in sys.argv:
        print('\n  nothing written — pass --apply')
        return

    # **A read is `onLoad`, anything else is `onAction`.** The verb already decided
    # this when the operation was named, so it is read back rather than guessed again.
    READ_VERB = ('list', 'get', 'search', 'lookup', 'find', 'export')
    written = 0
    for f, screens_ in sorted(per_file.items()):
        d = yaml.safe_load(io.open(f, encoding='utf8'))
        by_id = {s['id']: s for s in d['screens']}
        for sid, picks in screens_.items():
            s = by_id.get(sid)
            if not s:
                continue
            have = {a.get('operationId') for a in (s.get('apis') or [])}
            for oid, _sc in sorted(picks.items(), key=lambda x: -x[1]):
                if oid in have:
                    continue
                r = ops[oid][2]
                verb = re.match(r'[a-z]+', oid).group(0)
                s.setdefault('apis', []).append({
                    'operationId': oid,
                    'contract': owner.get(oid, '?'),
                    'purpose': (r.get('summary') or '').strip() or 'Derived from the screen tasks',
                    'trigger': 'onLoad' if verb in READ_VERB else 'onAction',
                    'provenance': 'derived — task linkage, 19 September 2026',
                })
                written += 1
        io.open(f, 'w', encoding='utf8').write(
            yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
        print('  -> %s' % f)
    print('\n%d reference(s) written' % written)


if __name__ == '__main__':
    main()
