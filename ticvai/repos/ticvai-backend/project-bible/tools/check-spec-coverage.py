# -*- coding: utf-8 -*-
"""Read the specification chapters against what the package actually draws.

`sources/specifications/technical/Ch03_Functional_Domain_Coverage` is the client's
own coverage map: twelve domains, and under each a table of capabilities with a
delivery phase and an implementation approach. It is the one document in the drop
that enumerates scope in the client's vocabulary rather than ours.

Nothing had read it. This matches every capability row against the screens and
contracts we have built, and sorts the result three ways:

    drawn     a screen names it
    thin      the module exists but no screen carries the capability's own words
    absent    neither

**Thin is the interesting bucket, not absent.** Absent usually means a module we
have not reached yet, which is known. Thin means we built the module and missed
a capability the client listed inside it - the Emirates ID reader sitting inside
POS, the seatmap importer sitting inside seating. Those are the ones that look
finished and are not.

A word of warning about the matching: it is lexical. A capability whose client
name differs from ours reads as thin when it is drawn. The output is a review
queue in the same sense the redundancy triage is - it ranks a shortlist for a
person and settles nothing by itself.

    python tools/check-spec-coverage.py            report
    python tools/check-spec-coverage.py --write    write docs/active/spec-coverage.md
"""
import collections
import glob
import io
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Retired to `sources/legacy/` on 19 September: the chapters are a proposal we
# wrote, not scope the client handed us, so they do not sit with the ranked
# material. The coverage check still reads Ch03 from there - retiring a document
# stops it being cited as scope, it does not stop it being useful as a checklist.
CH03 = os.path.join(ROOT, 'sources', 'legacy',
                    'Ch03_Functional_Domain_Coverage_v1_4.docx')

# Ch03's twelve domains against the ModuleKey vocabulary in contracts/subscription.yaml.
# A domain maps to several modules; a module answers to several domains.
DOMAIN_MODULES = {
    1:  ['core', 'accreditation'],
    2:  ['core'],
    3:  ['core', 'ticketing'],
    4:  ['ticketing', 'seating', 'access'],
    5:  ['resources', 'queue', 'ticketing'],
    6:  ['ticketing', 'retail', 'fnb', 'membership', 'partner'],
    7:  ['core', 'fnb', 'retail'],
    8:  ['marketing', 'membership'],
    9:  ['ai', 'analytics'],
    10: ['resources', 'inventory', 'maintenance', 'fnb', 'games'],
    11: ['developerApi', 'partner', 'core'],
    12: [],
}

STOP = set('''and or the a an of for to in with per by on at from into its it this that
management system configuration platform service services support integration integrations
based multi non full new all each every other via using'''.split())


def words(s):
    return [w for w in re.findall(r'[a-z]{3,}', s.lower()) if w not in STOP]


# ------------------------------------------------------------------ the chapter

def paragraphs(path):
    xml = zipfile.ZipFile(path).read('word/document.xml').decode('utf8', errors='replace')
    out = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', xml, re.S):
        t = ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', p, re.S))
        t = (t.replace('&amp;', '&').replace('&#8217;', "'").replace('&quot;', '"')
              .replace('&lt;', '<').replace('&gt;', '>')).strip()
        if t:
            out.append(t)
    return out


def capabilities():
    """[(domain no, domain name, capability, phase, notes)] from Ch03's tables.

    A capability row is a cell followed by a `Phase 1` / `Phase 2` cell. The
    header row says `Delivery` in that position, so it is skipped by name.
    """
    ps = paragraphs(CH03)
    rows, dom_no, dom_name = [], None, None
    for i, line in enumerate(ps):
        m = re.match(r'^Domain (\d+)\s*[-–—]\s*(.+)$', line)
        if m:
            dom_no, dom_name = int(m.group(1)), m.group(2).strip()
            continue
        if dom_no is None or i + 1 >= len(ps):
            continue
        if not re.match(r'^Phase [12]$', ps[i + 1]):
            continue
        if line in ('Delivery', 'Capability', 'Implementation', 'Notes') or len(line) > 90:
            continue
        notes = ''
        for j in (i + 2, i + 3):
            if j < len(ps) and not re.match(r'^Phase [12]$', ps[j]):
                if ps[j] not in ('OOTB', 'Configurable', 'Custom'):
                    notes = ps[j]
                    break
        rows.append((dom_no, dom_name, line.lstrip('⚠️ ').strip(),
                     ps[i + 1], notes))
    # the same capability can repeat across a domain's continuation tables
    seen, out = set(), []
    for r in rows:
        if (r[0], r[2]) in seen:
            continue
        seen.add((r[0], r[2]))
        out.append(r)
    return out


# ------------------------------------------------------------------ the package

def package():
    """module -> screen names, and everything-everywhere as a second chance.

    Scoping a capability to its domain's modules is right for a capability that
    lives inside a module, and wrong for one that *is* a platform. `Developer
    Portal`, `Online Storefront`, `Partner & Reseller Portal` and `White-Label
    CMS` are each a whole `P*` file, so a module-scoped match reports four
    delivered platforms as missing. The package-wide blob catches those.
    """
    per = collections.defaultdict(list)
    everywhere = []
    for f in glob.glob(os.path.join(ROOT, 'screens', 'P*.yaml')):
        txt = io.open(f, encoding='utf8', errors='replace').read()
        mp = re.search(r'^  name: (.+)$', txt, re.M)
        if mp:
            everywhere.append(mp.group(1).strip())
        for block in re.split(r'(?m)^(?=(?:  )?- id: [A-Z]{2,3}-[0-9]{3,4}$)', txt):
            mn = re.search(r'^\s*name: (.+)$', block, re.M)
            mm = re.search(r'^\s*requiresModule: (\S+)$', block, re.M)
            if mn and mm:
                per[mm.group(1)].append(mn.group(1).strip())
                everywhere.append(mn.group(1).strip())
    # nav sections carry the client's words more often than screen titles do
    for f in glob.glob(os.path.join(ROOT, 'screens', 'P*.yaml')):
        txt = io.open(f, encoding='utf8', errors='replace').read()
        everywhere += re.findall(r'^\s*module: (.+)$', txt, re.M)
    return per, [n.strip().lower() for n in everywhere if n.strip()]


def document_frequency(names):
    """How many screen names use each word. `reader` is common; `emirates` is not."""
    df = collections.Counter()
    for n in names:
        for w in set(words(n)):
            df[w] += 1
    return df


def covered(cap_words, names, df):
    """True when ONE name carries the capability, and the best name it matched.

    Two ways to get this wrong, and both were run before this rule settled.

    Matching against the pooled text of every name says `Emirates ID Reader` is
    delivered, because some unrelated gaming screen supplies the word `reader`.
    Requiring every word in one name says `Audit Trail & Logging` is missing,
    because our screen is called `Governance Audit Trail & Compliance Evidence`
    and never says `logging`.

    So the test is per name and weighted: the capability's **rarest** word has
    to be in the name. That word is what the capability is about - `emirates`,
    `seatmap`, `gamification` - while the common ones (`management`, `reader`,
    `control`) are shared by half the package and settle nothing.
    """
    if not cap_words:
        return False, None
    rare = min(cap_words, key=lambda w: df.get(w, 0))
    best, best_hit = None, -1
    for n in names:
        if rare not in n:
            continue
        hit = sum(1 for w in cap_words if w in n)
        if hit > best_hit:
            best, best_hit = n, hit
    if best is not None:
        return True, best
    # nothing carried the rare word - report the nearest miss so a person can judge
    near, near_hit = None, 0
    for n in names:
        hit = sum(1 for w in cap_words if w in n)
        if hit > near_hit:
            near, near_hit = n, hit
    return False, near


def main():
    caps = capabilities()
    per, everywhere = package()
    have = set(per)
    df = document_frequency(everywhere)

    drawn, thin, absent = [], [], []
    for dom, dname, cap, phase, notes in caps:
        mods = [m for m in DOMAIN_MODULES.get(dom, []) if m in have]
        scoped = [n.lower() for m in mods for n in per[m]]
        cw = words(cap)
        ok_s, hit_s = covered(cw, scoped, df)
        ok_a, hit_a = covered(cw, everywhere, df)
        row = (dom, dname, cap, phase, mods, notes, hit_s or hit_a)
        if not mods:
            absent.append(row)
        elif ok_s or ok_a:
            drawn.append(row)
        else:
            thin.append(row)

    out = []
    w = out.append
    w('# Ch03 capability coverage - the client\'s list against our screens')
    w('')
    w('> Generated by `tools/check-spec-coverage.py` from')
    w('> `sources/specifications/technical/Ch03_Functional_Domain_Coverage_v1_4.docx`.')
    w('> **A review queue, not a verdict** - the match is lexical, so a capability we')
    w('> named differently reads as thin when it is drawn.')
    w('')
    w('| | count |')
    w('|---|---:|')
    w('| capabilities in Ch03 | **%d** |' % len(caps))
    w('| drawn - a screen carries the capability\'s own words | %d |' % len(drawn))
    w('| **thin - the module exists, no screen names it** | **%d** |' % len(thin))
    w('| absent - no module for it yet | %d |' % len(absent))
    w('')
    w('## Thin - built the module, missed the capability')
    w('')
    w('These are the ones that look finished and are not.')
    w('')
    w('| domain | capability | phase | closest screen we have | notes from Ch03 |')
    w('|---|---|---|---|---|')
    for dom, dname, cap, phase, mods, notes, near in sorted(thin, key=lambda r: (r[0], r[2])):
        w('| D%d %s | **%s** | %s | %s | %s |' % (
            dom, dname, cap, phase, ('`%s`' % near) if near else '**nothing**',
            notes[:150].replace('|', '/')))
    w('')
    w('## Absent - no module carries the domain')
    w('')
    for dom, dname, cap, phase, mods, notes, near in sorted(absent, key=lambda r: (r[0], r[2])):
        w('- D%d %s - **%s** (%s)' % (dom, dname, cap, phase))
    w('')
    w('## Drawn')
    w('')
    for dom, dname, cap, phase, mods, notes, near in sorted(drawn, key=lambda r: (r[0], r[2])):
        w('- D%d %s - %s' % (dom, dname, cap))
    w('')

    text = '\n'.join(out) + '\n'
    sys.stdout.write(text)
    if '--write' in sys.argv:
        dst = os.path.join(ROOT, 'docs', 'active', 'spec-coverage-19-september.md')
        io.open(dst, 'w', encoding='utf8').write(text)
        sys.stderr.write('wrote %s\n' % dst)


if __name__ == '__main__':
    main()
