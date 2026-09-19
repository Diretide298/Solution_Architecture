# -*- coding: utf-8 -*-
"""What the client sent, and whether anything in the package has read it.

Three categories arrive in every client drop and only one of them was ever
ingested:

    Design Books   -> parsed by parse-workshop-pack.py into sources/workshop/pack.json
    MoMs           -> mined by mine-moms.py into sources/mom-corpus.json
    Specifications -> read by nothing at all

The third category is the reason this tool exists. On 19 September the twelve
technical chapters, the hardware integration sheet and the seating manifest had
zero citations anywhere in contracts/, screens/ or docs/ - they were filed on
intake and never opened. A drop is not ingested when its boards are parsed; it
is ingested when all three categories are.

Read status is deliberately cheap to compute and impossible to fake: a document
counts as read when something outside sources/ names it. Writing this index does
not make anything read.

    python tools/index-sources.py              report to stdout
    python tools/index-sources.py --write      also write sources/SOURCES-INDEX.md
"""
import collections
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'sources')


def read(path):
    try:
        return io.open(path, encoding='utf8', errors='replace').read()
    except Exception:
        return ''


def stem(name):
    """Compare documents by shape, not by the copy that happens to be on disk.

    The same book reaches us as `F&B Dashboard Screens v1.0.pdf`,
    `FB_Dashboard_Screens_v1_0.pdf` and `... (1).pdf` in three folders. Matching
    on the raw filename reports one document as three, two of them unread.
    """
    n = os.path.basename(name)
    n = re.sub(r'\.(pdf|docx|xlsx|jpeg|jpg|png)$', '', n, flags=re.I)
    n = re.sub(r'\s*\(\d+\)', '', n)
    n = re.sub(r'[^a-z0-9]+', '', n.lower())
    n = n.replace('fandb', 'fb').replace('foodandbeverage', 'fb')
    return n


# ---------------------------------------------------------------- the package

def built_screens():
    """pack stem -> [screen count, module counter] for what is drawn today."""
    per = collections.defaultdict(lambda: [0, collections.Counter()])
    for f in glob.glob(os.path.join(ROOT, 'screens', 'P*.yaml')):
        txt = read(f)
        # a screen block runs from its id to the next id; source.pack and
        # requiresModule both sit inside it
        for block in re.split(r'(?m)^(?=(?:  )?- id: [A-Z]{2,3}-[0-9]{3,4}$)', txt):
            mp = re.search(r'^\s*pack: (.+)$', block, re.M)
            mm = re.search(r'^\s*requiresModule: (\S+)$', block, re.M)
            if not mp:
                continue
            s = stem(mp.group(1).strip())
            per[s][0] += 1
            if mm:
                per[s][1][mm.group(1)] += 1
    return per


def normalise(text):
    """Squash text to the same shape `stem` produces, for substring matching.

    **Not `stem` itself.** `stem` begins with `os.path.basename`, which is right
    for a filename and catastrophic for a corpus: on a blob of every doc in the
    package it returns only whatever follows the last slash, throwing away
    essentially all of it. The first run of this tool reported 0 of 24 documents
    cited for exactly that reason, on the same day two of them were cited in a
    document written to cite them.
    """
    n = re.sub(r'[^a-z0-9]+', '', text.lower())
    return n.replace('fandb', 'fb').replace('foodandbeverage', 'fb')


def cited(stems):
    """stem -> True when anything outside sources/ names the document."""
    hay = []
    for sub in ('contracts', 'screens', 'docs', 'flows', 'tools'):
        d = os.path.join(ROOT, sub)
        for dirpath, _, files in os.walk(d):
            for fn in files:
                if fn.rsplit('.', 1)[-1].lower() in ('yaml', 'yml', 'md', 'json', 'py'):
                    hay.append(read(os.path.join(dirpath, fn)))
    blob = normalise(' '.join(hay))
    return dict((s, s in blob) for s in stems)


# ---------------------------------------------------------------- categories

def design_books():
    parsed = collections.Counter()
    pj = os.path.join(SRC, 'workshop', 'pack.json')
    if os.path.exists(pj):
        for s in json.load(io.open(pj, encoding='utf8')):
            parsed[stem(s['source'])] += 1
    on_disk = {}
    for sub in ('packs', 'workshop', 'boards', 'requirements', 'designs'):
        for p in glob.glob(os.path.join(SRC, sub, '*')):
            if os.path.isfile(p) and not p.endswith(('.md', '.json', '.url')):
                on_disk.setdefault(stem(p), []).append(
                    os.path.relpath(p, SRC).replace('\\', '/'))
    built = built_screens()
    rows = []
    for s, paths in sorted(on_disk.items()):
        b = built.get(s, [0, collections.Counter()])
        rows.append({
            'stem': s,
            'files': paths,
            'name': os.path.basename(paths[0]),
            'parsed': parsed.get(s, 0),
            'built': b[0],
            'modules': b[1],
        })
    return rows


def moms():
    corpus = os.path.join(SRC, 'mom-corpus.json')
    seen = set()
    if os.path.exists(corpus):
        d = json.load(io.open(corpus, encoding='utf8'))
        for m in d.get('minutes', []):
            k = m.get('file') or m.get('source') or m.get('path') or ''
            if k:
                seen.add(stem(k))
    rows = []
    for p in sorted(glob.glob(os.path.join(SRC, 'mom', '*.docx'))):
        rows.append({'name': os.path.basename(p), 'mined': stem(p) in seen})
    return rows


def specifications():
    rows = []
    base = os.path.join(SRC, 'specifications')
    for dirpath, _, files in os.walk(base):
        for fn in sorted(files):
            if fn.startswith('.') or fn.endswith('.md'):
                continue
            rows.append({'name': fn,
                         'section': os.path.relpath(dirpath, base).replace('\\', '/'),
                         'stem': stem(fn)})
    marks = cited([r['stem'] for r in rows])
    for r in rows:
        r['cited'] = marks.get(r['stem'], False)
    return rows


# ---------------------------------------------------------------- report

def main():
    books, mo, spec = design_books(), moms(), specifications()

    out = []
    w = out.append
    w('# Sources index - what arrived, and what has been read')
    w('')
    w('> Generated by `tools/index-sources.py`. **Read status is not a plan, it is a fact:**')
    w('> a document counts as read when something outside `sources/` names it.')
    w('')

    nb = sum(1 for b in books if b['parsed'])
    w('## Design books - %d of %d parsed' % (nb, len(books)))
    w('')
    w('| document | parsed | screens built | modules |')
    w('|---|---:|---:|---|')
    for b in sorted(books, key=lambda x: (-x['parsed'], x['name'])):
        mods = ', '.join('%s (%d)' % (k, v) for k, v in b['modules'].most_common(3)) or '-'
        w('| `%s` | %s | %s | %s |' % (
            b['name'], b['parsed'] or '**no**', b['built'] or '-', mods))
    w('')

    nm = sum(1 for m in mo if m['mined'])
    w('## MoMs - %d of %d mined' % (nm, len(mo)))
    w('')
    for m in mo:
        w('- %s`%s`' % ('' if m['mined'] else '**UNMINED** ', m['name']))
    w('')

    nc = sum(1 for s in spec if s['cited'])
    w('## Specification documents - %d of %d cited anywhere' % (nc, len(spec)))
    w('')
    w('| document | section | read |')
    w('|---|---|---|')
    for s in spec:
        w('| `%s` | %s | %s |' % (s['name'], s['section'], 'yes' if s['cited'] else '**no**'))
    w('')

    text = '\n'.join(out) + '\n'
    sys.stdout.write(text)
    if '--write' in sys.argv:
        dst = os.path.join(SRC, 'SOURCES-INDEX.md')
        io.open(dst, 'w', encoding='utf8').write(text)
        sys.stderr.write('wrote %s\n' % dst)


if __name__ == '__main__':
    main()
