#!/usr/bin/env python3
"""Read every minute in `sources/mom/` and say which open question each one already answers.

**Two false blockers were found in one afternoon and both were minutes nobody had read.** `BO-006`
sat on an open question that the 14 August minute answered three weeks earlier, and `P11`'s eight
screens were recorded as having *zero MoM coverage* for a workshop that had already happened. Both
cost work twice: once to raise, once to withdraw.

Eight minutes were added to the package on 8 September, six of them the most recent sessions on the
project. **Everything reasoned before that date reasoned without them.** This is the sweep.

## What it matches against

  `screens/P*.yaml` -> the 74 `openQuestions`, each on a named screen.
  `docs/registers/conflicts.md` -> the rows under `## Open`, which is the register's own claim
  about what is unresolved.

## How it scores, and why the score is not the answer

Rare-term overlap: a question's distinctive words against each minute's paragraphs, weighted by how
few minutes use the word. `wallet` narrows; `system` does not. **The output is a reading list, not a
verdict** -- the tool says *this minute talks about this*, and a person says whether it settles it.
**A scorer that closed questions by itself would be the same defect it is looking for**: an
assertion nothing checked.

Run: python3 tools/mine-moms.py [--top N]
"""
import json
import math
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MOMS = ROOT / "sources" / "mom"
SCREENS = ROOT / "screens"
CONFLICTS = ROOT / "docs" / "registers" / "conflicts.md"
OUT = ROOT / "sources" / "mom-corpus.json"

PARA = re.compile(r"<w:p[ >].*?</w:p>", re.S)
TEXT = re.compile(r"<w:t[^>]*>(.*?)</w:t>", re.S)
TAG = re.compile(r"<[^>]+>")

# Words in every minute carry no signal. Kept deliberately short: an aggressive stop list is how a
# scorer stops finding the thing nobody thought to ask for.
STOP = set("""a an and are as at be been but by can for from had has have if in into is it its
may no not of on or that the their there they this to was were will with we you your our
shall should would could item action point discussion note noted agreed team meeting
session client softlabs ticvai date time page minutes minute attendees present also
one two three per each other more most such via""".split())

WORD = re.compile(r"[a-z][a-z0-9-]{2,}")
MONTHS = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
          "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}


def paragraphs(path):
    """Paragraph text from a minute, whatever a minute turns out to be.

    **Only 8 of the 22 files in `sources/mom/` are Word documents.** The other 14 carry a `.docx`
    extension over Markdown -- eleven open `**Minutes`, three open with a table row -- and the eight
    real ones are exactly the eight added on 8 September. Reading the extension rather than the
    first four bytes raises `BadZipFile` on two thirds of the corpus, which is how a sweep of
    everything quietly becomes a sweep of the newest third."""
    if path.read_bytes()[:4] != b"PK\x03\x04":
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            # Markdown table rows carry the decisions; the pipes are not words.
            txt = " ".join(re.sub(r"[|*`#>]+", " ", line).split())
            if txt:
                yield txt
        return
    yield from docx_paragraphs(path)


def docx_paragraphs(path):
    """A docx is a zip; the body is `word/document.xml`.

    Table cells are `<w:p>` too, so they arrive as their own paragraphs -- which is what we want,
    because **most decisions in these minutes are recorded in tables**, not prose."""
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist()
                 if re.match(r"word/(document|footnotes|endnotes)\d*\.xml$", n)]
        for n in sorted(names):
            xml = z.read(n).decode("utf-8", errors="replace")
            for p in PARA.findall(xml):
                txt = TAG.sub("", "".join(TEXT.findall(p)))
                for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                             ("&quot;", '"'), ("&apos;", "'"), (" ", " ")):
                    txt = txt.replace(a, b)
                txt = " ".join(txt.split())
                if txt:
                    yield txt


def mom_date(name):
    """Sortable date from the filename. **These are not consistently named**, which is why this
    tries three shapes rather than one."""
    m = re.search(r"(20\d\d)-(\d\d)-(\d\d)", name)
    if m:
        return "-".join(m.groups())
    m = re.search(r"(\d{1,2})(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(20\d\d)", name)
    if m:
        return "%s-%s-%02d" % (m.group(3), MONTHS[m.group(2)], int(m.group(1)))
    m = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)_(\d{1,2})_(20\d\d)", name)
    if m:
        return "%s-%s-%02d" % (m.group(3), MONTHS[m.group(1)], int(m.group(2)))
    return "unknown"


def build_corpus():
    docs = []
    for f in sorted(list(MOMS.glob("*.docx")) + list(MOMS.glob("*.md"))):
        paras = list(paragraphs(f))
        docs.append({"file": f.name, "date": mom_date(f.name), "paragraphs": paras,
                     "format": "docx" if f.read_bytes()[:2] == b"PK" else "markdown",
                     "words": sum(len(p.split()) for p in paras)})
    docs.sort(key=lambda d: (d["date"], d["file"]))
    return docs


def tokens(s):
    return {w for w in WORD.findall(s.lower()) if w not in STOP}


def idf(docs):
    n = len(docs)
    df = Counter()
    for d in docs:
        df.update(tokens(" ".join(d["paragraphs"])))
    return {w: math.log(n / c) for w, c in df.items()}


def open_questions():
    out = []
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = doc["platform"]["code"]
        for s in doc["screens"]:
            for q in (s.get("openQuestions") or []):
                out.append({"kind": "openQuestion", "ref": "%s %s" % (code, s["id"]),
                            "name": s.get("name", ""), "text": q})
    return out


def open_conflicts():
    """Rows under a `## Open` heading -- the register's own statement of what is unresolved."""
    out, live = [], False
    for ln in CONFLICTS.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            live = ln.startswith("## Open")
            continue
        if not live or not ln.startswith("| **CF-"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split(" | ")]
        m = re.match(r"\*\*(CF-[0-9a-z]+)\*\*", cells[0])
        if m:
            out.append({"kind": "conflict", "ref": m.group(1), "name": "",
                        "text": cells[1] if len(cells) > 1 else ""})
    return out


def score(item, docs, weights, top):
    q = tokens(item["text"] + " " + item["name"])
    # The rarest terms in the question are the ones that identify it. A question sharing only
    # `configuration` and `screen` with a minute has not been answered by it.
    q = {w for w in q if weights.get(w, 0) > 0.35}
    hits = []
    for d in docs:
        best, bp = 0.0, None
        for p in d["paragraphs"]:
            if len(p) < 40:
                continue
            ov = q & tokens(p)
            if len(ov) < 3:
                continue
            s = sum(weights.get(w, 0) for w in ov) / (1 + math.log(len(p.split())))
            if s > best:
                best, bp = s, p
        if bp:
            hits.append({"mom": d["file"], "date": d["date"], "score": round(best, 3),
                         "paragraph": bp[:700]})
    hits.sort(key=lambda h: -h["score"])
    return hits[:top]


def main():
    top = 3
    if "--top" in sys.argv:
        top = int(sys.argv[sys.argv.index("--top") + 1])
    if not MOMS.exists():
        print("  no sources/mom -- nothing to mine")
        return 1

    docs = build_corpus()
    weights = idf(docs)
    print("%d minutes | %s words" % (len(docs), format(sum(d["words"] for d in docs), ",")))
    for d in docs:
        print("  %s  %6sw  %4dp  %s" % (d["date"], format(d["words"], ","),
                                        len(d["paragraphs"]), d["file"]))

    items = open_conflicts() + open_questions()
    print("\n%d open items: %d conflicts, %d screen questions"
          % (len(items), sum(1 for i in items if i["kind"] == "conflict"),
             sum(1 for i in items if i["kind"] == "openQuestion")))

    results = [dict(it, hits=score(it, docs, weights, top)) for it in items]
    covered = [r for r in results if r["hits"]]
    print("  %d of %d have at least one minute discussing them" % (len(covered), len(items)))

    OUT.write_text(json.dumps(
        {"generatedBy": "tools/mine-moms.py",
         "note": ("Reading list, not a verdict. A hit means a minute discusses the same rare "
                  "terms as the open item; whether it settles it is a person's call."),
         "minutes": [{k: v for k, v in d.items() if k != "paragraphs"} for d in docs],
         "items": results}, indent=1), encoding="utf-8")
    print("  -> %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
