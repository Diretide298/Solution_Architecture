#!/usr/bin/env python3
"""Write a contract back to disk without duplicating keys.

**`yaml.safe_dump` on a file that already contains a duplicate key emits both copies.** It has
happened three times in two days — `fnb.yaml` 80 blocks, `seating.yaml` 10, `finance.yaml` and
`cross-cell.yaml` 47 between them, every one on `x-ticvai-consumed-by`.

**The loader is where it starts.** `yaml.safe_load` keeps the last of two identical keys and says
nothing, so a round-trip reads one value and writes two — and the second write is what a person
sees in a diff they did not expect to be looking at.

**Every edit to a contract should go through `write_contract`.** It dumps, then strips consecutive
duplicate blocks, then re-parses to prove the result still loads. **A tool that produces the defect
it is meant to prevent is worse than no tool**, so the verification is not optional.

    from tools.contract_io import write_contract
    write_contract(path, doc)
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

# Keys observed to duplicate. They are all list-valued `x-ticvai-*` extensions, which is not a
# coincidence: pandoc-style block sequences under a repeated key are what `safe_dump` reproduces
# faithfully rather than collapsing.
DUP_PRONE = ("x-ticvai-consumed-by", "x-ticvai-audience", "x-ticvai-emits")


def strip_duplicate_blocks(text: str) -> tuple[str, int]:
    """Remove the second of two consecutive identical keys at the same indent.

    **Keeps the first, not the last.** The first is the one written by hand with its original
    quoting; the second is `safe_dump`'s reconstruction. A reviewer reading a diff should see the
    file they wrote.
    """
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    removed = 0
    while i < len(lines):
        m = re.match(r"^(\s+)(" + "|".join(DUP_PRONE) + r"):\s*$", lines[i])
        if m:
            ind, key = m.group(1), m.group(2)
            j = i + 1
            while j < len(lines) and re.match(r"^" + ind + r"\s*- ", lines[j]):
                j += 1
            if j < len(lines) and re.match(r"^" + ind + re.escape(key) + r":\s*$", lines[j]):
                k = j + 1
                while k < len(lines) and re.match(r"^" + ind + r"\s*- ", lines[k]):
                    k += 1
                out.extend(lines[i:j])
                removed += 1
                i = k
                continue
        out.append(lines[i])
        i += 1
    return "\n".join(out), removed


def write_contract(path: str | Path, doc: dict, *, width: int = 100) -> int:
    """Dump, de-duplicate, verify. Returns how many duplicate blocks were removed.

    **Preserves the leading comment header**, which `safe_dump` drops — several contracts open with
    a paragraph explaining what the file is for, and losing it on every edit is how a package ends
    up with no prose at the top of anything.
    """
    p = Path(path)
    original = p.read_text(encoding="utf-8") if p.exists() else ""
    head = "".join(x for x in original.splitlines(keepends=True) if x.startswith("#"))

    body = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=width)
    body, removed = strip_duplicate_blocks(body)

    p.write_text(head + body, encoding="utf-8")

    # **Prove it loads before returning.** Writing a file that does not parse and reporting success
    # is the failure this module exists to stop.
    yaml.safe_load(p.read_text(encoding="utf-8"))
    return removed


def check_all(root: str | Path = ".") -> list[tuple[str, int]]:
    """Report contracts that currently hold a duplicate block. Writes nothing."""
    found = []
    for f in sorted(Path(root).glob("contracts/*/*.yaml")):
        _, n = strip_duplicate_blocks(f.read_text(encoding="utf-8"))
        if n:
            found.append((f.name, n))
    return found


if __name__ == "__main__":
    import sys
    bad = check_all(Path(__file__).resolve().parents[1])
    if bad:
        for name, n in bad:
            print(f"  {name}: {n} duplicate block(s)")
        sys.exit(1)
    print("  no duplicate keys in any contract")
