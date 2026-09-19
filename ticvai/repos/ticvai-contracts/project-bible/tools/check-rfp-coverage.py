# -*- coding: utf-8 -*-
"""The RFP's own capability list against the screens we draw.

`sources/specifications/rfp/` holds the document the whole engagement answers, and
until 19 September nothing in the package had read it. It was filed on intake
next to a proposal *we* wrote - `Ch03_Functional_Domain_Coverage` - which has the
same twelve domains in the same order, because Ch03 was written to answer it.

**That is why this tool exists and `check-spec-coverage.py` is the lesser one.**
Ch03 is our claim about our coverage; the RFP is the client's statement of what
they asked for. Checking our screens against our own proposal tells you the
proposal is self-consistent. Checking them against the RFP tells you whether the
thing we are building is the thing that was requested.

    python tools/check-rfp-coverage.py             report
    python tools/check-rfp-coverage.py --write     write docs/active/rfp-coverage.md
"""
import collections
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RFP = os.path.join(ROOT, 'sources', 'specifications', 'rfp',
                   'TAIS Platform RFP From Miracle Star Trading.pdf')

STOP = set('''and or the a an of for to in with per by on at from into its it this that
management system configuration platform service services support integration integrations
based multi non full new all each every other via using must shall provides provide
allows allow supports supported tracks maintains enables domain'''.split())


def words(s):
    return [w for w in re.findall(r'[a-z]{3,}', s.lower()) if w not in STOP]


# ------------------------------------------------------------------- the RFP

def rfp_lines():
    """Page text with the diagonal watermark removed.

    Every page carries `CONFIDENTIAL` set as a rotated watermark, and pdfplumber
    interleaves its letters into the body one at a time. They arrive two ways:
    as lone lines (`L`, `A`, `I`, `T`), and spliced inside a word - `CrCedit`,
    `WCishlist`, `ManOagement`, `validatioNn`, `transaTctions`, `loyaOlty`.

    Left in, they corrupt the capability names this tool matches on, and
    `Credit Memo Management` silently becomes a capability nothing can match.

    The splices are repaired on a rule that holds in English prose: **an
    uppercase letter with a lowercase letter on both sides is never legitimate
    here**, and neither is one ending a lowercase word. What that rule cannot
    reach is a watermark letter glued to the *front* of a word (`Nfeedback`,
    `Oto`) - there is no lexical way to tell that from a capitalised word - so
    those survive in the descriptions. They do not affect matching, which runs
    on the capability names.
    """
    import pdfplumber
    mark = set('CONFIDENTIAL')
    out = []
    with pdfplumber.open(RFP) as pdf:
        for page in pdf.pages:
            for raw in (page.extract_text() or '').split('\n'):
                line = raw.strip()
                if len(line) <= 1:
                    continue
                # a -> X <- a  : ManOagement, loyaOlty, transaTctions, rCedit
                line = re.sub(r'(?<=[a-z])([A-Z])(?=[a-z])',
                              lambda m: '' if m.group(1) in mark else m.group(1), line)
                # A -> X <- a  : WCishlist
                line = re.sub(r'(?<=[A-Z])([A-Z])(?=[a-z])',
                              lambda m: '' if m.group(1) in mark else m.group(1), line)
                # a -> X <- end: andA, Logging I
                line = re.sub(r'(?<=[a-z])([A-Z])\b',
                              lambda m: '' if m.group(1) in mark else m.group(1), line)
                line = re.sub(r'\s+([A-Z])\s*$',
                              lambda m: '' if m.group(1) in mark else m.group(0), line)
                line = re.sub(r'\s+', ' ', line).strip()
                if len(line) > 1:
                    out.append(line)
    return out


def capabilities():
    """[(domain no, domain name, capability, description)].

    Two shapes in one document. Domains 1-8 name a capability on its own line
    and describe it in the paragraph beneath. Domains 9-11 give a bare bullet
    list with no descriptions at all - which is itself worth knowing, because a
    bulleted capability is one the client did not trouble to define.
    """
    lines = rfp_lines()
    rows, dom_no, dom_name = [], None, None
    i = 0
    while i < len(lines):
        line = lines[i]
        # `2. Governance & Multi-Tenant Domain` - the hyphen has to be in the
        # class or domain 2 never matches and its rows are filed under domain 1
        m = re.match(r'^(\d{1,2})\.\s+([A-Z][A-Za-z&,/\-\s]+?)\s*(?:Domain)?$', line)
        if m and int(m.group(1)) <= 12 and len(m.group(2)) < 60:
            dom_no, dom_name = int(m.group(1)), m.group(2).strip()
            i += 1
            continue
        if dom_no is None:
            i += 1
            continue
        if line.startswith('•'):
            rows.append((dom_no, dom_name, line.lstrip('• ').strip(), ''))
            i += 1
            continue
        # a capability heading: short, title-cased, no terminal full stop, and
        # followed by a sentence rather than by another heading
        is_head = (len(line) < 70 and '.' not in line and len(line.split()) <= 8
                   and re.match(r'^[A-Z]', line)
                   and len(re.findall(r'[a-z]', line)) > 3
                   and not line.startswith(('The ', 'This ', 'Both ', 'Vendors ',
                                            'Responses ', 'All ')))
        if is_head:
            desc = []
            j = i + 1
            while j < len(lines) and (lines[j].endswith('.') or len(lines[j]) > 70
                                      or lines[j].startswith(('The ', 'This ', 'Supports',
                                                              'Allows', 'Provides'))):
                desc.append(lines[j])
                j += 1
                if len(desc) >= 4:
                    break
            if desc:
                rows.append((dom_no, dom_name, line, ' '.join(desc)))
                i = j
                continue
        i += 1
    seen, out = set(), []
    for r in rows:
        if (r[0], r[2].lower()) in seen:
            continue
        seen.add((r[0], r[2].lower()))
        out.append(r)
    return out


# --------------------------------------------------------------- the package

def package():
    per, everywhere = collections.defaultdict(list), []
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
        everywhere += [m.strip() for m in re.findall(r'^\s*module: (.+)$', txt, re.M)]
    return per, [n.lower() for n in everywhere if n.strip()]


def covered(cap_words, names, df):
    """The capability's rarest word has to appear in one name. See
    `check-spec-coverage.py` for why a pooled match and a strict match both lie.
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
    near, near_hit = None, 0
    for n in names:
        hit = sum(1 for w in cap_words if w in n)
        if hit > near_hit:
            near, near_hit = n, hit
    return False, near


def main():
    caps = capabilities()
    per, everywhere = package()
    df = collections.Counter()
    for n in everywhere:
        for w in set(words(n)):
            df[w] += 1

    drawn, thin = [], []
    for dom, dname, cap, desc in caps:
        cw = words(cap)
        ok, near = covered(cw, everywhere, df)
        (drawn if ok else thin).append((dom, dname, cap, desc, near))

    out = []
    w = out.append
    w('# RFP coverage - what was asked for, against what we draw')
    w('')
    w('> Generated by `tools/check-rfp-coverage.py` from')
    w('> `sources/specifications/rfp/TAIS Platform RFP From Miracle Star Trading.pdf`.')
    w('>')
    w('> **This is the rank 2 check.** `check-spec-coverage.py` reads Ch03, which is a')
    w('> proposal we wrote to answer this document - useful as a checklist, never as scope.')
    w('')
    w('| | count |')
    w('|---|---:|')
    w('| capabilities named in the RFP | **%d** |' % len(caps))
    w('| a screen carries it | %d |' % len(drawn))
    w('| **no screen names it** | **%d** |' % len(thin))
    w('')
    w('## Not named by any screen')
    w('')
    w('| domain | capability | closest screen | what the RFP says |')
    w('|---|---|---|---|')
    for dom, dname, cap, desc, near in sorted(thin, key=lambda r: (r[0], r[2])):
        w('| %d %s | **%s** | %s | %s |' % (
            dom, dname, cap, ('`%s`' % near) if near else '**nothing**',
            (desc[:170] or '*bulleted, undefined in the RFP*').replace('|', '/')))
    w('')
    w('## Carried by a screen')
    w('')
    for dom, dname, cap, desc, near in sorted(drawn, key=lambda r: (r[0], r[2])):
        w('- %d %s - %s' % (dom, dname, cap))
    w('')

    text = '\n'.join(out) + '\n'
    sys.stdout.write(text)
    if '--write' in sys.argv:
        dst = os.path.join(ROOT, 'docs', 'active', 'rfp-coverage-19-september.md')
        io.open(dst, 'w', encoding='utf8').write(text)
        sys.stderr.write('wrote %s\n' % dst)


if __name__ == '__main__':
    main()
