#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Documentation that names a table the package no longer has.

**`derive-schema-history.py` declares every rename, dated, with a reason. Nothing read it.**
It was written so a workbook diff would read sixteen renames rather than sixteen deletions and
sixteen additions, and that is worth having — but the same declaration answers a question
nothing was asking: *which documents did that rename just falsify?*

On 20 September sixteen tables were renamed. The applied script swept `tools/*.py`, because a
hardcoded name there is a lookup that silently stops matching. **It did not sweep `docs/`**, and
`docs/` is where the reasoning lives. ADR-0018's own text justified the configuration scope walk
by saying *"`org_unit` is an `ltree`"* — a sentence that stopped being true the moment the table
became `platform.scope`, in the ADR that the rename was argued from.

Ring 4 of `contract-change-runbook.md` lists nine files a contract change breaks that no tool
rebuilds. **Documentation was not one of them**, which is exactly why this went unnoticed.

## What it reports

    error     a `schema.table` that `schema-history.json` declares renamed, with the new name.
              This is a stale document and the fix is mechanical
    warning   a `schema.table` the package has never held. Usually a hypothetical, a quotation
              from somebody else's schema, or a typo - a person has to look

**Two kinds of file are exempt and the reasons differ.** A document *about* a rename must keep
the old name: `schema-merge-*.md` says "rental.category is the asset-category master, so it moves
out of rental", and replacing that produces nonsense. And `sources/` is other people's material,
read-only by convention - `check-package` already excludes it from its own doc scan.

    python3 tools/check-doc-tables.py
    python3 tools/check-doc-tables.py --fix     # rewrite the mechanical ones
"""
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")

# A document whose subject IS the rename keeps the old name; so does anything imported.
EXEMPT_PARTS = ("sources", "_dump", "repos")
EXEMPT_NAMES = ("schema-merge-decision-log.md", "schema-merge-decisions-20-september.md",
                "schema-merge-final-report-20-september.md",
                "schema-merge-response-20-september.md", "rename-worklist-20-september.md",
                "schema-merge-audit-18-september.md", "change-log-validation-18-september.md")

# `word.word` where the left side names a real schema. **A backtick is a boundary, not an
# exclusion** - documentation wraps almost every table name in one, and excluding them found
# three stale names where there were sixty. The schema check is what keeps this narrow:
# `schema-reference.json` and `derive-schema.py` both parse as word.word and neither has a
# schema on the left.
TOKEN = re.compile(r"(?<![\w./-])([a-z][a-z0-9_]{2,})\.([a-z][a-z0-9_]{2,})(?![\w./-])")

# **A schema name is also a contract filename.** `orders.yaml` and `subscription.yaml` parse as
# word.word with a real schema on the left and are files, not tables.
EXTENSIONS = {"yaml", "yml", "json", "md", "py", "mjs", "csv", "xlsx", "html", "sql", "txt",
              "sh", "svg", "png", "pdf", "js", "css", "ini", "cfg", "lock", "log"}

# A quotation is evidence. Provenance blocks record what somebody actually said.
QUOTE = re.compile(r"^\s*>|^\s{4,}\S")


def load():
    hist = json.load(io.open(os.path.join(H, "schema-history.json"), encoding="utf-8"))
    renamed = {r["from"]: r["to"] for r in (hist.get("renames") or [])}
    cols = json.load(io.open(os.path.join(H, "schema-reference.json"), encoding="utf-8"))
    have = {t for t in (cols.get("cols") or {})}
    schemas = {t.split(".")[0] for t in have if "." in t}
    return renamed, have, schemas


def main():
    fix = "--fix" in sys.argv[1:]
    renamed, have, schemas = load()

    stale = collections.defaultdict(list)
    unknown = collections.Counter()
    files = 0
    for dirpath, dirnames, names in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXEMPT_PARTS and not d.startswith(".")]
        rel_dir = os.path.relpath(dirpath, ROOT)
        if not (rel_dir == "docs" or rel_dir.startswith("docs" + os.sep)):
            continue
        for n in sorted(names):
            if not n.endswith(".md") or n in EXEMPT_NAMES:
                continue
            p = os.path.join(dirpath, n)
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            files += 1
            text = io.open(p, encoding="utf-8").read()
            out = text
            for i, line in enumerate(text.split("\n"), 1):
                quoted = bool(QUOTE.match(line))
                for m in TOKEN.finditer(line):
                    tok = m.group(0)
                    if tok in have or m.group(1) not in schemas:
                        continue
                    if m.group(2) in EXTENSIONS:
                        continue
                    if tok in renamed:
                        stale[rel].append((i, tok, renamed[tok], quoted))
                    else:
                        unknown[tok] += 1
            if fix:
                for _, tok, new, quoted in stale.get(rel, []):
                    if quoted:
                        continue
                    out = re.sub(r"(?<![\w./-])" + re.escape(tok) + r"(?![\w./-])", new, out)
                if out != text:
                    io.open(p, "w", encoding="utf-8", newline="\n").write(out)

    n_stale = sum(len(v) for v in stale.values())
    n_quoted = sum(1 for v in stale.values() for x in v if x[3])
    print("  %d document(s) scanned" % files)
    if not stale:
        print("  PASS — no document names a renamed table")
    else:
        print("  %d name(s) in %d document(s) were renamed and the document still says the old "
              "one" % (n_stale, len(stale)))
        for rel in sorted(stale)[:14]:
            names_here = collections.Counter(t for _, t, _, _ in stale[rel])
            print("    %-56s %s" % (rel, ", ".join("%s x%d" % (k, v) if v > 1 else k
                                                   for k, v in names_here.most_common(4))))
        if n_quoted:
            print("  %d of them sit in a quotation or an indented block and are left alone — a "
                  "quotation records what was written, not what is true now" % n_quoted)
    if unknown:
        print("\n  %d name(s) the package has never held — a hypothetical, somebody else's "
              "schema, or a typo:" % len(unknown))
        for tok, k in unknown.most_common(8):
            print("      %-40s x%d" % (tok, k))
    if fix:
        print("\n  --fix applied. Quotations were not touched.")
        return 0
    if stale:
        print("\n  run with --fix, or exempt the file in EXEMPT_NAMES if it is about the rename")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
