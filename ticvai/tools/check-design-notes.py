#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The process design notes: every rule sourced, every source real, every screen a screen.

**`handoff/design-notes/<process>.yaml` is authored** (1 October): one file per process -- white-label,
ticketing-guest, ticketing-backoffice, fnb-retail, venue-operations, platform-foundation,
finance-insights, customer-marketing, ai -- written by the owner of that process, holding what a
designer must get right that the contracts do not say. `tools/design_spec.py` renders each screen's
notes into that screen's block in every batch's BUNDLE.md, so **a note that cites nothing, or cites
something that is not there, reaches a design session looking exactly as authoritative as one that
does.** This is what stops that.

Checks, per file:

1. It parses, and it is a mapping with `process` and `screens`.
2. Every screen id under `screens` exists in `screens/P*.yaml`; every `consistency.with` too.
3. **Every rule carries a `source`**: each item of `inputs`, `outputs`, `actions`, `edgeCases`,
   `corrections` and `openQuestions`, and each vocabulary term.
4. **Every source is a recognised form, and the checkable ones resolve:**

       contracts/<file>.yaml[#<pointer or operationId>]   file exists; the operationId or schema too
       F<n> [step <k>]                                      the flow exists (and the step)
       DI-<n>                                               in handoff/design-inputs/mom-design-inputs.yaml
       MATRIX <ref>                                         a matrixRef or packageRef in traceability.json
       ADR-<n>                                              docs/adr/<nnnn>-*.md
       screens/<file>.yaml#<screen id>                      the file has the screen
       R<n>, POSV2-<n>, REV3-<n>                            in the audit, POS v2 or rev 3 registers
       TRACKER <sheet> row <n>                              recognised; resolved against the tracker index
       MoM <date> <section>, Vision Book p<n>,             recognised (free text by nature)
       designer default, other package paths, CF/BL/W/CFG/MOB/DG/M17/23SEP/SD decision refs

   A source string may hold several, separated by `;` or `|`, or be a list.

`designer default` is allowed and counted: the brief asks for it to stay rare.

    python3 tools/check-design-notes.py              # the package's notes; exit 1 on an error
    python3 tools/check-design-notes.py --dir DIR    # another folder (a trial)
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES = ROOT / "handoff" / "design-notes"
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
RULE_LISTS = ("inputs", "outputs", "actions", "edgeCases", "corrections", "openQuestions")


def _load(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")
    try:
        return yaml.load(text, Loader=LOADER)
    except yaml.YAMLError:
        # libyaml rejects escaped surrogate pairs (contracts/satellite/subscription.yaml); the pure-Python loader reads them
        return yaml.load(text, Loader=yaml.SafeLoader)


class Index:
    """What a source can point at, read once."""

    def __init__(self):
        self.screens, self.screen_file = set(), collections.defaultdict(set)
        for f in sorted((ROOT / "screens").glob("P*.yaml")):
            doc = _load(f) or {}
            for s in doc.get("screens") or []:
                self.screens.add(s["id"])
                self.screen_file[f.name].add(s["id"])
        self.flows = {}
        for f in sorted((ROOT / "flows").glob("F*.yaml")):
            m = re.match(r"^(F\d+)", f.name)
            if m:
                try:
                    d = _load(f) or {}
                    self.flows[m.group(1)] = {s.get("step") for s in d.get("steps") or []}
                except Exception:
                    self.flows[m.group(1)] = set()
        di = _load(ROOT / "handoff" / "design-inputs" / "mom-design-inputs.yaml") or {}
        self.di = {e.get("id") for e in di.get("inputs") or []}
        tr = json.loads((ROOT / "handoff" / "traceability.json").read_text(encoding="utf-8"))
        self.matrix = {r.get("matrixRef") for r in tr.get("rows") or []} | {r.get("packageRef") for r in tr.get("rows") or []}
        self.adrs = {re.match(r"^(\d{4})", f.name).group(1) for f in (ROOT / "docs" / "adr").glob("0*.md")}
        reg = ""
        for f in ("audit-decisions.json", "audit-register.md", "audit-decisions.md"):
            for base in (ROOT / "handoff", ROOT / "docs" / "registers"):
                if (base / f).exists():
                    reg += (base / f).read_text(encoding="utf-8")
        self.r = set(re.findall(r"\bR-?[A-Z0-9]*\d+[a-z]?\b", reg))
        self.posv2 = {d.get("ref") for d in json.loads((ROOT / "handoff" / "pos-v2-decisions.json").read_text(encoding="utf-8"))}
        self.rev3 = {d.get("ref") for d in json.loads((ROOT / "handoff" / "rev3-decisions.json").read_text(encoding="utf-8"))}
        ti = ROOT / "handoff" / "design-inputs" / "task-tracker-index.json"
        self.tracker = {r["id"] for r in json.loads(ti.read_text(encoding="utf-8")).get("rows", [])} if ti.exists() else set()
        self._contracts = {}

    def contract(self, rel: str):
        if rel not in self._contracts:
            p = ROOT / rel
            self._contracts[rel] = _load(p) if p.exists() else None
        return self._contracts[rel]


LOOSE = re.compile(r"^(MoM\b.*|Vision Book( p\.? ?\d+.*)?|designer default|"
                   r"(CF|BL|CFG|MOB|DG|M17|M18|23SEP|SD|W|GAP|WLB|L|REV3|POSV2)-?\d+[a-z]?(\s*\(.*\))?|"
                   r"W\d+|rev 3 .*|audit .*|decided .*)$", re.I)
PATHLIKE = re.compile(r"^(handoff|docs|sources|wireframes|flows|states|events|screens|contracts|tools|audit)/")


def check_source(one: str, ix: Index) -> tuple[str | None, str]:
    """(error or None, kind). One source string, already split."""
    s = one.strip().strip(".")
    if not s:
        return "empty source", "?"
    m = re.match(r"^(contracts/[^#\s]+\.ya?ml)(?:#(.+))?$", s)
    if m:
        doc = ix.contract(m.group(1))
        if doc is None:
            return f"{m.group(1)} does not exist", "contract"
        frag = (m.group(2) or "").strip()
        if frag:
            if frag.startswith("/"):
                parts = [p for p in frag.split("/") if p]
                node = doc
                for p in parts:
                    if isinstance(node, dict) and p in node:
                        node = node[p]
                    elif isinstance(node, dict) and p.replace("~1", "/") in node:
                        node = node[p.replace("~1", "/")]
                    else:
                        # a pointer into a schema's property may name a field the schema reaches by $ref
                        if parts[:2] == ["components", "schemas"] and len(parts) >= 3 and parts[2] in \
                                ((doc.get("components") or {}).get("schemas") or {}):
                            return None, "contract"
                        return f"{s}: pointer does not resolve", "contract"
            else:
                ops = {op.get("operationId") for it in (doc.get("paths") or {}).values() if isinstance(it, dict)
                       for op in it.values() if isinstance(op, dict)}
                sch = set(((doc.get("components") or {}).get("schemas") or {}))
                if frag not in ops and frag not in sch:
                    return f"{s}: no operation or schema {frag!r} in {m.group(1)}", "contract"
        return None, "contract"
    m = re.match(r"^(F\d+)(?:\s+step\s+(\d+)(?:\s*[-–→>]+\s*\d+)?)?\b", s)
    if m and (len(s) == len(m.group(0)) or s[len(m.group(0)):].strip().startswith(("(", ",", ":"))):
        if m.group(1) not in ix.flows:
            return f"flow {m.group(1)} does not exist", "flow"
        if m.group(2) and int(m.group(2)) not in ix.flows[m.group(1)]:
            return f"{m.group(1)} has no step {m.group(2)}", "flow"
        return None, "flow"
    m = re.match(r"^DI-(\d+)$", s)
    if m:
        return (None if s in ix.di else f"{s} is not in mom-design-inputs.yaml"), "DI"
    m = re.match(r"^MATRIX\s+([\d.]+)", s)
    if m:
        return (None if m.group(1).rstrip(".") in ix.matrix else f"{s}: no such matrix ref in traceability.json"), "MATRIX"
    m = re.match(r"^ADR-?(\d{1,4})\b", s)
    if m:
        return (None if m.group(1).zfill(4) in ix.adrs else f"{s}: no such ADR"), "ADR"
    m = re.match(r"^screens/([\w.-]+\.yaml)#([A-Z]{2,4}-\d{3})$", s)
    if m:
        return (None if m.group(2) in ix.screen_file.get(m.group(1), set()) else f"{s}: no such screen in that file"), "screen"
    m = re.match(r"^POSV2-\d+$", s)
    if m:
        return (None if s in ix.posv2 else f"{s}: not in pos-v2-decisions.json"), "POSV2"
    m = re.match(r"^REV3-\d+$", s)
    if m:
        return (None if s in ix.rev3 else f"{s}: not in rev3-decisions.json"), "REV3"
    m = re.match(r"^R-?[A-Z0-9-]*\d+[a-z]?(\s*\(.*\))?$", s)
    if m:
        base = re.match(r"^(R-?[A-Z0-9-]*\d+)", s).group(1)
        return (None if base in ix.r or base.rstrip("abcdefg") in ix.r else f"{s}: not in the audit register"), "R"
    m = re.match(r"^TRACKER\b(.*)$", s, re.I)
    if m:
        rest = m.group(1)
        mm = re.search(r"(Actions|Client Inputs|Tracker)\s+row\s+([ACST]?\d+)", rest, re.I)
        if mm and ix.tracker:
            sheet, n = mm.group(1).lower(), mm.group(2)
            rid = n if n[0] in "ACST" else {"actions": "A", "client inputs": "C"}.get(sheet, "") + n
            if sheet == "tracker" and n[0] not in "ST":
                return None, "TRACKER"
            if rid not in ix.tracker:
                return f"{s}: no row {rid} in the tracker index", "TRACKER"
        return None, "TRACKER"
    if PATHLIKE.match(s):
        path = s.split("#", 1)[0].split(" ", 1)[0]
        return (None if (ROOT / path).exists() else f"{s}: {path} does not exist"), "path"
    if LOOSE.match(s):
        return None, "designer default" if s.lower() == "designer default" else "decision"
    return f"unrecognised source form: {s!r}", "?"


def split_sources(src) -> list[str]:
    if src is None:
        return []
    if isinstance(src, (list, tuple)):
        out = []
        for x in src:
            out += split_sources(x)
        return out
    parts = [p.strip() for p in re.split(r"\s*[;|]\s*", str(src)) if p.strip()]
    out = []
    for p in parts:
        # "DI-1093, DI-1094" -> two; "MoM 30 Sep 4.6, Booking" stays one (free text)
        bits = [b.strip() for b in p.split(",")]
        if len(bits) > 1 and all(re.match(r"^(DI-\d+|F\d+|ADR-\d+|R\d+|REV3-\d+|POSV2-\d+|MATRIX [\d.]+)", b) for b in bits):
            out += bits
        else:
            out.append(p)
    return out


def check_file(f: pathlib.Path, ix: Index, errs: list, stats: collections.Counter) -> None:
    rel = f.name
    try:
        doc = _load(f)
    except Exception as e:
        errs.append(f"{rel}: does not parse: {e}")
        return
    if not isinstance(doc, dict):
        errs.append(f"{rel}: not a mapping")
        return
    for k in ("process", "screens"):
        if k not in doc:
            errs.append(f"{rel}: no `{k}`")
    if doc.get("process") and doc["process"] != f.stem:
        errs.append(f"{rel}: process {doc['process']!r} does not match the file name")

    def src_ok(where: str, item, required: bool = True):
        if not isinstance(item, dict):
            errs.append(f"{rel}: {where}: an item must be a mapping with a source")
            return
        srcs = split_sources(item.get("source"))
        if not srcs:
            if required:
                errs.append(f"{rel}: {where}: no source")
            return
        for s in srcs:
            e, kind = check_source(s, ix)
            stats[kind] += 1
            if e:
                errs.append(f"{rel}: {where}: {e}")

    for i, v in enumerate(doc.get("vocabulary") or []):
        src_ok(f"vocabulary[{i}] {((v or {}).get('term') if isinstance(v, dict) else v)!r}", v)
    for i, v in enumerate(doc.get("inputToOutput") or []):
        if isinstance(v, dict) and v.get("source"):
            src_ok(f"inputToOutput[{i}]", v)
    screens = doc.get("screens") or {}
    if not isinstance(screens, dict):
        errs.append(f"{rel}: `screens` must map screen ids to notes")
        return
    for sid, e in screens.items():
        stats["screens"] += 1
        if str(sid) not in ix.screens:
            errs.append(f"{rel}: screen {sid} does not exist in screens/P*.yaml")
        if not isinstance(e, dict):
            errs.append(f"{rel}: {sid}: notes must be a mapping")
            continue
        for key in RULE_LISTS:
            items = e.get(key) or []
            if not isinstance(items, list):
                errs.append(f"{rel}: {sid}.{key} must be a list")
                continue
            for i, it in enumerate(items):
                stats["rules"] += 1
                src_ok(f"{sid}.{key}[{i}]", it)
        for i, c in enumerate(e.get("consistency") or []):
            if isinstance(c, dict):
                w = c.get("with")
                for x in (w if isinstance(w, list) else [w] if w else []):
                    if re.match(r"^[A-Z]{2,4}-\d{3}$", str(x)) and str(x) not in ix.screens:
                        errs.append(f"{rel}: {sid}.consistency[{i}]: screen {x} does not exist")
                if c.get("source"):
                    src_ok(f"{sid}.consistency[{i}]", c)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", help="the notes folder (default handoff/design-notes)")
    a = ap.parse_args()
    d = pathlib.Path(a.dir).resolve() if a.dir else NOTES
    files = sorted(d.glob("*.yaml")) if d.is_dir() else []
    if not files:
        print("design notes: none yet (handoff/design-notes/*.yaml); nothing to check")
        return 0
    ix = Index()
    errs, stats = [], collections.Counter()
    for f in files:
        check_file(f, ix, errs, stats)
    for e in errs[:200]:
        print(f"  {e}")
    if len(errs) > 200:
        print(f"  … {len(errs) - 200} more")
    kinds = ", ".join(f"{k} {v}" for k, v in sorted(stats.items()) if k not in ("screens", "rules"))
    print(f"design notes: {len(files)} file(s), {stats['screens']} screens, {stats['rules']} rules; "
          f"sources: {kinds}; {len(errs)} error(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
