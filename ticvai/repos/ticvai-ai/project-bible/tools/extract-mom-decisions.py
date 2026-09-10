#!/usr/bin/env python3
"""Pull every decision, action and confirmation out of the minutes, and say which are unabsorbed.

**A decision taken in a room and not written into the package costs the work twice** — once to make
it, once to make it again. `BO-006` waited three weeks on a question the 14 August minute had
already answered, and `P11`'s eight screens were recorded as having no workshop coverage on the day
after the workshop.

Eight minutes were added on 8 September, six of them the most recent sessions on the project.
**Everything the package concluded before that date concluded without them.**

## What counts as a decision

The minutes are written to a house style and label their own outcomes. Four openers carry the
weight -- `Decision:`, `Action:`, `Confirmed:`, `Agreed` -- and a fifth, `Open item`, marks the
ones that were deliberately left. Anything else is discussion.

## What *unabsorbed* means, and what it does not

Each decision is searched for in the package's own prose: the conflict register, the ADRs, the
active notes. **A miss is not proof of a gap** -- a decision can be absorbed as a contract
operation or a schema column with none of the minute's words surviving. It means *nobody wrote this
sentence down*, which is where to look, not what to conclude.

Run: python3 tools/extract-mom-decisions.py [--unabsorbed]
"""
import importlib.util
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOMS = ROOT / "sources" / "mom"
OUT = ROOT / "sources" / "mom-decisions.json"

# Where an absorbed decision would have left a trace. Derived directories are deliberately absent:
# finding a decision in `handoff/` proves only that a deriver copied it out of one of these.
CORPUS = [ROOT / "docs" / "registers", ROOT / "docs" / "adr", ROOT / "docs" / "active",
          ROOT / "docs" / "architecture", ROOT / "notes"]

# **Most of these lines are bullets**, and the bullet is not always the same character: the docx
# minutes render list items as a leading `-`, the Markdown ones use `-` or a number, and a few
# outcomes are labelled mid-sentence after a dash. Anchoring on the label alone found 35 outcomes
# in 6 of 22 minutes; allowing the bullet in front of it is the difference between sweeping the
# corpus and sweeping the files that happened to be formatted one way.
LABEL = re.compile(r"^\s*(?:[-–—•*·]+\s*|\d+[.)]\s*)?"
                   r"(Decision|Action|Confirmed|Agreed|Open item|Next step|Requested)s?\b"
                   r"\s*(?:\([^)]{0,40}\))?\s*[:—-]\s*", re.I)
WORD = re.compile(r"[a-z][a-z0-9-]{3,}")

# Words that would match anything in a package this size.
STOP = set("""this that with from will would could should have been they their there which what
when where whether tied both same each other more most such than then also into over under
about after before during team client venue tenant system platform screen module data user
users configurable configuration support supports supported provide provides using used
across within between per allow allows allowed""".split())


def load_miner():
    spec = importlib.util.spec_from_file_location("mine", ROOT / "tools" / "mine-moms.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def package_text():
    parts = []
    for d in CORPUS:
        if not d.exists():
            continue
        for f in d.rglob("*.md"):
            parts.append(f.read_text(encoding="utf-8", errors="replace").lower())
    return "\n".join(parts)


def key_terms(s):
    return [w for w in WORD.findall(s.lower()) if w not in STOP]


def main():
    only_unabsorbed = "--unabsorbed" in sys.argv
    mine = load_miner()
    pkg = package_text()

    rows = []
    for f in sorted(MOMS.glob("*.docx")):
        d = mine.mom_date(f.name)
        for para in mine.paragraphs(f):
            m = LABEL.match(para)
            if not m or len(para) < 60:
                continue
            body = para[m.end():].strip()
            terms = key_terms(body)
            if len(terms) < 6:
                continue
            # Rarest-first: the distinctive words are the ones that would survive being written
            # into the package in somebody else's sentence.
            rare = sorted(set(terms), key=lambda w: (pkg.count(w), -len(w)))[:8]
            present = sum(1 for w in rare if w in pkg)
            rows.append({
                "date": d, "mom": f.name, "label": m.group(1).title(),
                "text": body[:500], "terms": rare,
                "termsFoundInPackage": present,
                # Two of eight distinctive terms is the floor at which a decision is plausibly
                # written down somewhere. Below it, nothing in the package uses this vocabulary.
                "absorbed": present >= 4,
            })

    rows.sort(key=lambda r: (r["date"], r["mom"], r["termsFoundInPackage"]))
    doc = {
        "generatedBy": "tools/extract-mom-decisions.py",
        "generated": date.today().isoformat(),
        "note": ("`absorbed` is a vocabulary match against the package's own prose, not a "
                 "verdict. **A decision can be absorbed as a contract operation or a schema "
                 "column with none of the minute's words surviving** -- an unabsorbed row is "
                 "where to look, not what to conclude."),
        "counts": {
            "decisions": len(rows),
            "byLabel": dict(Counter(r["label"] for r in rows).most_common()),
            "byMinute": dict(Counter(r["mom"] for r in rows).most_common()),
            "unabsorbed": sum(1 for r in rows if not r["absorbed"]),
        },
        "decisions": rows,
    }
    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")

    c = doc["counts"]
    print("%d labelled outcomes across %d minutes" % (c["decisions"], len(set(r["mom"] for r in rows))))
    print("  by label: %s" % c["byLabel"])
    print("  vocabulary absent from the package: %d" % c["unabsorbed"])
    for r in rows:
        if only_unabsorbed and r["absorbed"]:
            continue
        print("\n  %s  %s  [%d/8 terms in package]" % (r["date"], r["label"], r["termsFoundInPackage"]))
        print("    %s" % r["text"][:300])
    print("\n  -> %s" % OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
