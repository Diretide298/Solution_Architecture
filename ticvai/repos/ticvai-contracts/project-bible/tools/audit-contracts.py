# -*- coding: utf-8 -*-
"""Audit every contract against the four things that are supposed to agree with it.

**The contracts sit at the top of the chain.** Screens cite operations, the lineage
reads the contracts, the DDL follows the lineage, and the wireframes bind to schemas.
A contract that has drifted does not announce itself — it produces a screen layer that
cannot be bound and a gap list that proposes authoring operations which, under another
name, already exist.

Four sources are joined here, and each answers a different question:

    contracts/*/*.yaml       what the contract declares
    screens/P*.yaml          which of those operations anything actually calls
    handoff/traceability.json   what the requirement matrix expects of it
    sources/workshop/pack.json  what the client's boards describe in its domain

**The signal that matters is not coverage, it is disagreement.** A contract with 60% of
its operations unused *and* 119 board screens in its domain carrying none is not
partly finished — it is modelling something other than what the client drew. Coverage
would report both halves as "work remaining" and miss that they point at each other.

    python tools/audit-contracts.py            report
    python tools/audit-contracts.py --write    write docs/active/contract-audit.md
"""
import collections
import glob
import io
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Packs whose domain is AI. Held back on purpose: the AI boards are not complete, so
# a gap there is not evidence of a stale contract.
AI_PACK = re.compile(r'^AI_|Unified_BI', re.I)


def read(p):
    return io.open(p, encoding='utf8', errors='replace').read()


# ------------------------------------------------------------------ contracts

def contracts():
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'contracts', '*', '*.yaml'))):
        name = os.path.basename(f)[:-5]
        txt = read(f)
        date = subprocess.run(['git', 'log', '-1', '--format=%ad', '--date=short', '--', f],
                              capture_output=True, text=True, cwd=ROOT).stdout.strip()
        out[name] = {
            'path': os.path.relpath(f, ROOT).replace('\\', '/'),
            'ops': set(re.findall(r'^\s*operationId:\s*(\S+)', txt, re.M)),
            'schemas': set(re.findall(r'^    ([A-Z][A-Za-z0-9]*):$', txt, re.M)),
            'changed': date or '?',
        }
    return out


# ------------------------------------------------------------------ screens

def screens():
    """operations anything calls, and per-pack board coverage."""
    used = set()
    op_contract = {}
    packs = collections.defaultdict(lambda: {'screens': 0, 'withops': 0,
                                             'contracts': collections.Counter(),
                                             'module': collections.Counter()})
    for f in sorted(glob.glob(os.path.join(ROOT, 'screens', 'P*.yaml'))):
        d = yaml.safe_load(read(f)) or {}
        for s in d.get('screens') or []:
            apis = s.get('apis') or []
            for a in apis:
                oid = a.get('operationId')
                if oid:
                    used.add(oid)
                    if a.get('contract'):
                        op_contract[oid] = a['contract']
            pack = (s.get('source') or {}).get('pack')
            if not pack:
                continue
            p = packs[pack]
            p['screens'] += 1
            if apis:
                p['withops'] += 1
                for a in apis:
                    if a.get('contract'):
                        p['contracts'][a['contract']] += 1
            if s.get('requiresModule'):
                p['module'][s['requiresModule']] += 1
    return used, op_contract, packs


# ------------------------------------------------------------------ matrix

def matrix():
    f = os.path.join(ROOT, 'handoff', 'traceability.json')
    rows = json.load(io.open(f, encoding='utf8'))
    if isinstance(rows, dict):
        rows = rows.get('rows') or list(rows.values())[0]
    per = collections.defaultdict(collections.Counter)
    for r in rows:
        if isinstance(r, dict) and r.get('contract'):
            per[r['contract']][r.get('verdict', '?')] += 1
    return per


# ------------------------------------------------------------------ verdict

def verdict(ops, unused, board_gap, gap_rows):
    """One word for what is wrong, chosen so the fix differs for each.

    **`MISMATCHED` is the one to act on first.** Unused operations AND unserved board
    screens in the same domain mean the contract models a different thing, not a
    smaller one — and writing the missing operations without reading the unused ones
    would leave both halves in place.

    **`undersized` must not scale with the contract.** The first cut of this rule asked
    for `board_gap >= 3 × ops`, which meant `orders` needed 504 unserved screens to
    trip it and reported `aligned` on 178. A hundred board screens with nothing to call
    is the same problem whether the contract holds nine operations or a hundred and
    sixty-eight, so the threshold is absolute.
    """
    if not ops:
        return 'empty'
    frac = len(unused) / float(len(ops))
    if frac >= 0.40 and board_gap >= 20:
        # **Two causes, opposite work, and this tool cannot tell them apart.**
        # `seating` was ranked MISMATCHED on 21 unused operations and 119 unserved
        # screens, and the cause was the reverse of drift: its 14 runtime operations
        # were all called, its 21 authoring operations were called by nothing, and the
        # 119 screens were the authoring half — the same thing, never joined. Wiring
        # them took it to 0 unused without a line of contract change.
        #
        # So the verdict names the question rather than answering it. **Sort the
        # operations by runtime versus authoring first**: a clean split means a missing
        # join, a scatter means real drift.
        return 'JOIN OR DRIFT'
    if board_gap >= 50:
        return 'undersized'
    if frac >= 0.25:
        return 'stale'
    if board_gap >= 20 or gap_rows >= 10:
        return 'matrix gaps'
    return 'aligned'


# A pack's domain word, and whether any operation anywhere carries it. This is the
# check that finds a domain with no contract — attributing a pack to whichever
# contract one stray wired screen named does not, and reported Wallet, Rental and
# Accreditation as covered when between them they have three matching operations.
DOMAIN_WORD = {
    'Wallet_Configuration_Backend_Structure_v1.0.pdf': 'wallet',
    'Rental_Management.pdf': 'rental',
    'ACCREDITATION.pdf': 'accreditation',
    'Payment_Payment_Orchestration.pdf': 'payment',
    'Upsell,CrossSellEngine.pdf': 'upsell',
    'Digital Asset Management DAM.pdf': 'asset',
    'Seat_Management_Venue_Mapping_Reference v1.0.pdf': 'seat',
    'Subscription_Licensing_AI_Self_Service.pdf': 'licen',
    'Resource_Management_Configuration_Reference.pdf': 'resource',
    'Marketing_CRM_Configuration_Reference v1.0.pdf': 'campaign',
    'Approval_Workflows_and_Governance_Reference.pdf': 'approval',
    'Event_Management_Configuration_Backend_Structure_v1.0.pdf': 'event',
    'Game_and_Ride_Module.pdf': 'game',
}


def main():
    con = contracts()
    used, op_contract, packs = screens()
    mat = matrix()

    # a pack's contract is the one its own wired screens name most often
    pack_contract = {}
    for pack, p in packs.items():
        if p['contracts']:
            pack_contract[pack] = p['contracts'].most_common(1)[0][0]

    all_ops = set()
    for c in con.values():
        all_ops |= c['ops']

    board_gap = collections.Counter()
    orphan_packs = []
    for pack, p in packs.items():
        gap = p['screens'] - p['withops']
        if not gap:
            continue
        word = DOMAIN_WORD.get(pack)
        if word:
            hits = [o for o in all_ops if word in o.lower()]
            if len(hits) < 5:
                orphan_packs.append((gap, p['screens'], pack,
                                     p['module'].most_common(1)[0][0] if p['module'] else '?',
                                     len(hits)))
                continue
        c = pack_contract.get(pack)
        if c:
            board_gap[c] += gap
        else:
            orphan_packs.append((gap, p['screens'], pack,
                                 p['module'].most_common(1)[0][0] if p['module'] else '?', 0))

    rows = []
    for name, c in con.items():
        unused = c['ops'] - used
        m = mat.get(name, collections.Counter())
        gaps = m.get('GAP_CONTRACT', 0) + m.get('CONTRACTED_PARTIAL', 0)
        rows.append({
            'name': name, 'ops': len(c['ops']), 'unused': len(unused),
            'schemas': len(c['schemas']), 'changed': c['changed'],
            'contracted': m.get('CONTRACTED', 0), 'gaps': gaps,
            'parked': m.get('PARKED', 0), 'board_gap': board_gap.get(name, 0),
            'verdict': verdict(c['ops'], unused, board_gap.get(name, 0), gaps),
            'unused_names': sorted(unused)[:6],
        })

    order = {'JOIN OR DRIFT': 0, 'undersized': 1, 'stale': 2, 'matrix gaps': 3,
             'aligned': 4, 'empty': 5}
    rows.sort(key=lambda r: (order[r['verdict']], -r['board_gap'], -r['unused']))

    out = []
    w = out.append
    w('# Contract audit — every contract against the four things that must agree with it')
    w('')
    w('> Generated by `tools/audit-contracts.py`. **Contracts sit at the top of the chain**, so a')
    w('> contract that has drifted produces a screen layer that cannot be bound and a gap list')
    w('> proposing operations that already exist under another name.')
    w('')
    w('| verdict | meaning | what to do |')
    w('|---|---|---|')
    w('| **JOIN OR DRIFT** | many unused operations **and** many unserved board screens | **sort its operations runtime vs authoring.** A clean split means a missing join and no contract work; a scatter means real drift |')
    w('| undersized | far fewer operations than the boards describe | author, guided by the matrix |')
    w('| stale | a quarter or more of its operations reach no screen | decide each: superseded, renamed, or still wanted |')
    w('| matrix gaps | the matrix expects more than it carries | close against the requirement |')
    w('| aligned | none of the above | leave it |')
    w('')
    w('| contract | ops | unused | schemas | board screens unserved | matrix ok | matrix gaps | changed | verdict |')
    w('|---|---:|---:|---:|---:|---:|---:|---|---|')
    for r in rows:
        w('| `%s` | %d | %d | %d | %d | %d | %d | %s | **%s** |' % (
            r['name'], r['ops'], r['unused'], r['schemas'], r['board_gap'],
            r['contracted'], r['gaps'], r['changed'], r['verdict']))
    w('')

    w('## Domains with boards and no contract at all')
    w('')
    if orphan_packs:
        w('**These are new files, not edits.** No screen in them names an operation, so nothing')
        w('identifies a contract for them.')
        w('')
        w('| board screens with no operation | screens | module | operations naming it | pack |')
        w('|---:|---:|---|---:|---|')
        for gap, n, pack, mod, hits in sorted(orphan_packs, reverse=True):
            flag = ' *(AI — held back)*' if AI_PACK.search(pack) else ''
            w('| **%d** | %d | `%s` | **%d** | `%s`%s |' % (gap, n, mod, hits, pack, flag))
    else:
        w('None.')
    w('')

    w('## The unused operations, per contract')
    w('')
    w('**An unused operation is not automatically wrong.** It may serve a flow, a job or a')
    w('partner integration rather than a screen. It is a question, and the question is worth')
    w('asking where the same domain also has board screens with nothing to call.')
    w('')
    for r in rows:
        if r['unused']:
            w('- **`%s`** — %d unused, e.g. %s' % (
                r['name'], r['unused'], ', '.join('`%s`' % x for x in r['unused_names'])))
    w('')

    text = '\n'.join(out) + '\n'
    sys.stdout.write(text)
    if '--write' in sys.argv:
        dst = os.path.join(ROOT, 'docs', 'active', 'contract-audit-19-september.md')
        io.open(dst, 'w', encoding='utf8').write(text)
        sys.stderr.write('wrote %s\n' % dst)


if __name__ == '__main__':
    main()
