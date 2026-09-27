#!/usr/bin/env python3
"""Correct the button labels and destructive notes derive-components.py already wrote (audit R260).

derive-components.py only fills screens that declare fewer than two components, so once a screen
has been enriched it is never looked at again. Fixing the generator therefore leaves every label
and note it wrote on 10 September exactly as it was. This corrects those, in place:

* a derived button label whose acronym was lower-cased (*Save ai policy*, *Cancel fnb order*)
  becomes the label the generator now writes (*Save AI policy*, *Cancel F&B order*);
* a derived destructiveButton whose note is the fixed *cancel 3 orders worth AED 480* example
  gets the note the generator now writes, naming what that operation removes.

Only components marked `derived: true` whose label or note is still exactly what the old
generator produced are touched: anything a person has since edited is left alone. Edits are made
line by line, so comments, key order and the rest of the file are unchanged. Idempotent.

Run: `python3 tools/fix-audit-derived-labels.py [--apply]`
Without `--apply` it prints what it would change and writes nothing.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_spec = importlib.util.spec_from_file_location("derive_components",
                                               ROOT / "tools" / "derive-components.py")
dc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dc)

OLD_DESTRUCTIVE_NOTE = (
    "**Always confirms, never the default focus.** The consequence goes in the body — *cancel 3 "
    "orders worth AED 480* is a confirmation, *are you sure* is not.")


def old_label_for(op: str) -> str | None:
    """What derive-components.py wrote before acronyms kept their capitals."""
    m = re.match(r"^([a-z]+)([A-Z].*)$", op)
    if not m or m.group(1) not in dc.VERB_LABEL:
        return None
    noun = re.sub(r"(?<!^)(?=[A-Z])", " ", m.group(2)).strip().lower()
    verb = dc.VERB_LABEL[m.group(1)]
    return f"{verb} {noun}" if len(noun) < 22 else verb


def scalar(key: str, value: str, indent: str) -> list[str]:
    """One `key: value` line with YAML-correct quoting, never folded."""
    out = yaml.safe_dump({key: value}, allow_unicode=True, width=10**6).rstrip("\n")
    return [indent + out + "\n"]


def block_value(lines: list[str], i: int, key_indent: int) -> tuple[str, int]:
    """Parse the scalar starting at line i (a `key:` line) and return (value, end index)."""
    j = i + 1
    while j < len(lines):
        ln = lines[j]
        if ln.strip() == "" or len(ln) - len(ln.lstrip(" ")) > key_indent:
            j += 1
            continue
        break
    # trailing blank lines belong to whatever follows
    while j > i + 1 and lines[j - 1].strip() == "":
        j -= 1
    text = "".join(lines[i:j])
    try:
        dedented = "\n".join(ln[key_indent:] for ln in text.splitlines())
        val = next(iter(yaml.safe_load(dedented).values()))
    except Exception:
        val = None
    return val, j


def fix_file(path: Path) -> tuple[list[str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    report: list[str] = []
    out: list[str] = []
    i = 0
    item = re.compile(r"^(\s*)- kind: (\S+)\s*$")
    while i < len(lines):
        m = item.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        dash = len(m.group(1))
        kind = m.group(2)
        key_indent = dash + 2
        # the component block: until a line at or left of the dash that is not blank
        j = i + 1
        while j < len(lines):
            ln = lines[j]
            if ln.strip() and len(ln) - len(ln.lstrip(" ")) <= dash:
                break
            j += 1
        block = lines[i:j]
        keys: dict[str, int] = {}
        for k, ln in enumerate(block):
            if k == 0:
                continue
            km = re.match(r"^ {%d}([A-Za-z_][\w-]*):" % key_indent, ln)
            if km:
                keys.setdefault(km.group(1), k)
        derived = "derived" in keys and block[keys["derived"]].split(":", 1)[1].strip() == "true"
        op = (block[keys["impliedBy"]].split(":", 1)[1].strip()
              if "impliedBy" in keys else "")
        if not (derived and op and kind.endswith("Button")):
            out.extend(block)
            i = j
            continue

        new_block = list(block)
        pad = " " * key_indent
        # notes first (it may span lines), so the label index stays valid when notes follow it
        if kind == "destructiveButton" and "notes" in keys:
            k = keys["notes"]
            val, end = block_value(new_block, k, key_indent)
            if val == OLD_DESTRUCTIVE_NOTE:
                want = dc.destructive_note(op)
                new_block[k:end] = scalar("notes", want, pad)
                report.append(f"{path.name}:{i + k + 1} {op} notes -> {want}")
                keys = {kk: (vv if vv <= k else vv - (end - k - 1)) for kk, vv in keys.items()}
        if "label" in keys:
            k = keys["label"]
            val, end = block_value(new_block, k, key_indent)
            old, want = old_label_for(op), dc.label_for(op)
            if val is not None and val == old and want and want != old:
                new_block[k:end] = scalar("label", want, pad)
                report.append(f"{path.name}:{i + k + 1} {op} label '{val}' -> '{want}'")
        out.extend(new_block)
        i = j
    return out, report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    total = 0
    for f in sorted(SCREENS.glob("P*.yaml")):
        new, report = fix_file(f)
        for r in report:
            print("  " + r)
        total += len(report)
        if report and a.apply:
            text = "".join(new)
            yaml.safe_load(text)  # never write a file that no longer parses
            with open(f, "w", encoding="utf-8", newline="\n") as out:  # Path.write_text(newline=) is 3.10+
                out.write(text)
    print(f"  {total} change(s) {'written' if a.apply else 'would be made'}")
    if not a.apply and total:
        print("  nothing written — pass --apply, then run tools/refresh.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
