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
         ... (<annotation>)                                 each word of the annotation is a field, enum
                                                            value, parameter or response code reachable
                                                            from that operation or schema; `<field>
                                                            default|max|min|minLength|maxLength <n>` is
                                                            that field's constraint; "a quote" is in its text
       F<n> [step <k>], F<n> branch at step <k>             the flow exists (and the step, or a branch at it)
       DI-<n> [(gloss)]                                     in handoff/design-inputs/mom-design-inputs.yaml
       MATRIX <ref>                                         a matrixRef or packageRef in traceability.json
       ADR-<n>                                              docs/adr/<nnnn>-*.md
       screens/<file>.yaml#<screen id> [...]                the file has the screen
       <screen id> [(gloss)]                                the screen exists (WEB-010)
       R<n>, POSV2-<n>, REV3-<n>[a-z] [(gloss)]             in the audit, POS v2 or rev 3 registers
       REV3 <ref>, 23SEP-<n>, DG-<n>, GAP-<x><n>            in the rev 3 register (handoff/rev3-decisions.json)
       <NAME>-<dd>SEP <n>[-<m>]                             a design-round document under sources/designs/
       <NAME>-<dd>SEP (<anchor>[, <n> | detail])            guest-rev3-*/<NAME>.md (the latest round that has
                                                            it): item <n> is a numbered heading or item; the
                                                            anchor is a heading or a phrase in it
                                                            (CLIENT-RESPONSE-30SEP 2, AUDIT-29SEP (Seats))
       TRACKER <sheet> row <n>                              recognised; resolved against the tracker index
       other package paths [(locator)]                      the file exists; a path may contain spaces (the
                                                            longest existing prefix is the path)
       MoM <date> <section>, Vision Book p<n>,             recognised (free text by nature)
       designer default, CF/BL/W/CFG/MOB/M17/M18/SD decision refs

   A source string may hold several, separated by `;` or `|` (not inside parentheses), or be a list.

`designer default` is allowed and counted: the brief asks for it to stay rare.

5. **Decided questions** (2 October 2026, CHG-NOTE-001..010): an answered open question moves from `openQuestions`
   to the screen's `decisions` list. Each decision carries `question`, `decision`, `decidedBy`, `date`
   (YYYY-MM-DD) and `source`: the decision ledger id (`DEC-<n>`) and the change entries that record it
   (`CHG-<BATCH>-<nnn>`, each must exist in `changes/entries/`); `reviewable` (a default Chinmay may still
   overrule) is a boolean; `questionSource` (where the question came from) resolves like any other source. A
   question may not stay in `openQuestions` once it is decided on the same screen.
6. **Correction status**: a correction main has acted on carries `status` (`fixed`: main changed the screen;
   `logged`: the gap is an open change entry, not fixed yet; `withdrawn`: a decision made it moot) and `by`, the
   change entry that did it (it must exist). A correction with no `status` is still open. Any `CHG-` id named in a
   source must exist too.

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
CORRECTION_STATUS = ("fixed", "logged", "withdrawn")
CHG_ID = re.compile(r"\bCHG-[A-Z][A-Z0-9]{1,5}-\d{3}\b")
_ENTRIES: set | None = None


def change_ids() -> set:
    """The change-log entry ids that exist (changes/entries/CHG-<BATCH>-<nnn>-<slug>.yaml)."""
    global _ENTRIES
    if _ENTRIES is None:
        _ENTRIES = {m.group(0) for f in (ROOT / "changes" / "entries").glob("CHG-*.yaml")
                    if (m := CHG_ID.match(f.name))}
    return _ENTRIES


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
        self.flows, self.branches = {}, {}
        for f in sorted((ROOT / "flows").glob("F*.yaml")):
            m = re.match(r"^(F\d+)", f.name)
            if m:
                try:
                    d = _load(f) or {}
                    self.flows[m.group(1)] = {s.get("step") for s in d.get("steps") or []}
                    self.branches[m.group(1)] = {b.get("at") for b in d.get("branches") or [] if isinstance(b, dict)}
                except Exception:
                    self.flows[m.group(1)], self.branches[m.group(1)] = set(), set()
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
        # the design-round documents (CLIENT-RESPONSE-30SEP.md, AUDIT-29SEP.md, ...): the latest round that has each
        self.design_docs = {}
        rounds = sorted((ROOT / "sources" / "designs").glob("guest-rev3-*"),
                        key=lambda d: int((re.search(r"-(\d+)-", d.name + "-") or [0, 0])[1]))
        for d in rounds:
            for f in d.glob("*.md"):
                self.design_docs[f.stem] = f

    def contract(self, rel: str):
        if rel not in self._contracts:
            p = ROOT / rel
            self._contracts[rel] = _load(p) if p.exists() else None
        return self._contracts[rel]

    def contract_path(self, path: pathlib.Path):
        """A contract (or a file it $refs) by absolute path."""
        try:
            rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return None
        return self.contract(rel)


def _deref(node, base: pathlib.Path, ix: Index):
    """Follow $ref (local or to another contract file) to the node it names."""
    for _ in range(20):
        if not (isinstance(node, dict) and "$ref" in node):
            break
        f, _, ptr = str(node["$ref"]).partition("#")
        base = (base.parent / f) if f else base
        n = ix.contract_path(base)
        for part in [x for x in ptr.split("/") if x]:
            n = n.get(part.replace("~1", "/")) if isinstance(n, dict) else None
        node = n
    return node, base


def _reach(node, base, ix, names, fields, texts, depth=0, seen=None):
    """Every property name, enum value and description reachable from a schema node."""
    seen = set() if seen is None else seen
    node, base = _deref(node, base, ix)
    if not isinstance(node, dict) or depth > 8 or id(node) in seen:
        return
    seen.add(id(node))
    if isinstance(node.get("description"), str):
        texts.append(node["description"])
    for e in node.get("enum") or []:
        names.add(str(e))
    if "const" in node:
        names.add(str(node["const"]))
    for pn, ps in (node.get("properties") or {}).items():
        names.add(pn)
        fields[pn].append(_deref(ps, base, ix)[0])
        _reach(ps, base, ix, names, fields, texts, depth + 1, seen)
    for key in ("allOf", "oneOf", "anyOf"):
        for s in node.get(key) or []:
            _reach(s, base, ix, names, fields, texts, depth, seen)
    for key in ("items", "additionalProperties"):
        if isinstance(node.get(key), dict):
            _reach(node[key], base, ix, names, fields, texts, depth + 1, seen)


def _target(rel: str, frag: str, ix: Index):
    """(names, fields, response codes or None, text) reachable from an operation or schema of a contract."""
    doc, base = ix.contract(rel), ROOT / rel
    names, fields, codes, texts = set(), collections.defaultdict(list), None, []
    if frag.startswith("/"):
        _reach({"$ref": "#" + frag}, base, ix, names, fields, texts)
    else:
        for item in (doc.get("paths") or {}).values():
            if not isinstance(item, dict):
                continue
            for op in item.values():
                if isinstance(op, dict) and op.get("operationId") == frag:
                    codes = {str(c) for c in (op.get("responses") or {})}
                    texts += [str(op.get(k)) for k in ("summary", "description") if op.get(k)]
                    for prm in (item.get("parameters") or []) + (op.get("parameters") or []):
                        prm, pb = _deref(prm, base, ix)
                        if isinstance(prm, dict):
                            names.add(str(prm.get("name")))
                            fields[str(prm.get("name"))].append(_deref(prm.get("schema") or {}, pb, ix)[0])
                            texts.append(str(prm.get("description") or ""))
                            _reach(prm.get("schema") or {}, pb, ix, names, fields, texts)
                    rb, rbb = _deref(op.get("requestBody") or {}, base, ix)
                    for c in ((rb or {}).get("content") or {}).values():
                        _reach(c.get("schema") or {}, rbb, ix, names, fields, texts)
                    for r in (op.get("responses") or {}).values():
                        r, rb2 = _deref(r, base, ix)
                        texts.append(str((r or {}).get("description") or ""))
                        for c in ((r or {}).get("content") or {}).values():
                            _reach(c.get("schema") or {}, rb2, ix, names, fields, texts)
                    names |= {k for k in op if k.startswith("x-")}
        if codes is None:
            _reach({"$ref": "#/components/schemas/" + frag}, base, ix, names, fields, texts)
    names |= set(((doc.get("components") or {}).get("schemas") or {}))
    return names, fields, codes, _norm(" ".join(texts))


CONSTRAINT = {"default": ("default",), "max": ("maximum", "maxLength", "maxItems"), "maximum": ("maximum",),
              "min": ("minimum", "minLength", "minItems"), "minimum": ("minimum",), "minLength": ("minLength",),
              "maxLength": ("maxLength",), "minItems": ("minItems",), "maxItems": ("maxItems",)}


def _norm(s: str) -> str:
    """Text for a quote to be found in: markdown emphasis and code marks dropped, spaces collapsed, lower case."""
    return re.sub(r"\s+", " ", re.sub(r"[`*]", "", s)).strip().lower()


def _split_top(s: str, seps: str) -> list[str]:
    """Split on any of `seps` outside parentheses and double quotes."""
    out, cur, depth, quote = [], "", 0, False
    for ch in s:
        if ch == '"':
            quote = not quote
        elif not quote and ch == "(":
            depth += 1
        elif not quote and ch == ")":
            depth = max(0, depth - 1)
        if ch in seps and depth == 0 and not quote:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def check_annotation(src: str, rel: str, frag: str, ann: str, ix: Index) -> str | None:
    """`contracts/x.yaml#op (field, field default 480, 422, "a quote")`: every word must be in the contract."""
    names, fields, codes, text = _target(rel, frag, ix)
    last = None
    for item in _split_top(ann, ",;"):
        toks = re.findall(r'"[^"]*"|\S+', item)
        i = 0
        while i < len(toks):
            t = toks[i].strip(".:")
            if t.startswith('"'):
                if _norm(t.strip('"')) not in text:
                    return f"{src}: the quote {t} is not in {frag}"
            elif re.fullmatch(r"\d{3}", t) and codes is not None:
                if t not in codes:
                    return f"{src}: {frag} has no {t} response"
            elif t in CONSTRAINT and i + 1 < len(toks) and re.fullmatch(r"-?\d+(\.\d+)?", toks[i + 1]):
                want = float(toks[i + 1])
                nodes = fields.get(last or "", [])

                def same(v) -> bool:  # 480, or "24" where the field is a string enum
                    try:
                        return not isinstance(v, bool) and float(v) == want
                    except (TypeError, ValueError):
                        return False
                if not any(isinstance(n, dict) and any(k in n and same(n[k]) for k in CONSTRAINT[t]) for n in nodes):
                    return f"{src}: {last} has no {t} {toks[i + 1]} in {frag}"
                i += 1
            elif re.fullmatch(r"[A-Za-z_][\w-]*(\.[A-Za-z_][\w-]*)*", t) and all(p in names for p in t.split(".")):
                last = t.split(".")[-1]
            else:
                return (f"{src}: {t!r} is not a field, value, parameter or response of {frag}; "
                        f"a contract source's parentheses name only what the contract has (prose goes in the rule)")
            i += 1
    return None


LOOSE = re.compile(r"^(MoM\b.*|Vision Book( p\.? ?\d+.*)?|designer default|"
                   r"(CF|BL|CFG|MOB|M17|M18|SD|W|WLB|L)-?\d+[a-z]?(\s*\(.*\))?|"
                   r"W\d+|rev 3 .*|audit .*|decided .*)$", re.I)
PATHLIKE = re.compile(r"^(handoff|docs|sources|wireframes|flows|states|events|screens|contracts|tools|audit)/")
GLOSS = r"(?:\s*\(.*\))?"


def _design_doc(name: str, rest: str, ix: Index) -> str | None:
    """`CLIENT-RESPONSE-30SEP 2`, `AUDIT-29SEP (Seats, seat view box)`, `CLIENT-RESPONSE-REV3-25SEP (Basket, 10)`."""
    f = ix.design_docs.get(name)
    if f is None:
        return f"{name}: no sources/designs/guest-rev3-*/{name}.md"
    body = f.read_text(encoding="utf-8")
    flat = re.sub(r"\s+", " ", re.sub(r"[*_`]", "", body)).lower()
    heads = [re.sub(r"[*_`]", "", h).strip().lower() for h in re.findall(r"^#+\s*(.+)$", body, re.M)]

    def numbered(n: str) -> bool:
        return bool(re.search(rf"^(#+\s*|\*\*){n}\.\s", body, re.M))

    rest = rest.strip()
    if not rest:
        return None
    m = re.fullmatch(r"(\d+)(?:\s*[-–]\s*(\d+))?", rest)
    if m:
        for n in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
            if not numbered(str(n)):
                return f"{name} {rest}: {f.name} has no item {n}"
        return None
    m = re.fullmatch(r"\((.*)\)", rest)
    if not m:
        return f"{name} {rest}: cite an item number or (a heading or phrase in {f.name})"
    parts = _split_top(m.group(1), ",")
    anchor = re.sub(r"[*_`]", "", parts[0]).lower()
    if not any(h.startswith(anchor) or re.sub(r"^\d+\.\s*", "", h).startswith(anchor) for h in heads) \
            and anchor not in flat:
        return f"{name} ({parts[0]}): neither a heading nor a phrase in {f.name}"
    for p in parts[1:]:
        if re.fullmatch(r"\d+", p) and not numbered(p):
            return f"{name} ({m.group(1)}): {f.name} has no item {p}"
    return None


def check_source(one: str, ix: Index) -> tuple[str | None, str]:
    """(error or None, kind). One source string, already split."""
    s = one.strip().strip(".")
    if not s:
        return "empty source", "?"
    m = re.match(r"^(contracts/[^#\s]+\.ya?ml)(?:#(\S+))?(?:\s+\((.*)\))?$", s)
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
                            break
                        return f"{s}: pointer does not resolve", "contract"
            else:
                ops = {op.get("operationId") for it in (doc.get("paths") or {}).values() if isinstance(it, dict)
                       for op in it.values() if isinstance(op, dict)}
                sch = set(((doc.get("components") or {}).get("schemas") or {}))
                if frag not in ops and frag not in sch:
                    return f"{s}: no operation or schema {frag!r} in {m.group(1)}", "contract"
            if m.group(3) is not None:
                return check_annotation(s, m.group(1), frag, m.group(3), ix), "contract"
        elif m.group(3) is not None:
            return f"{s}: name the operation or schema (#...) the parentheses refer to", "contract"
        return None, "contract"
    m = re.match(r"^(F\d+)\s+branch\s+at\s+step\s+(\d+)" + GLOSS + "$", s)
    if m:
        if m.group(1) not in ix.flows:
            return f"flow {m.group(1)} does not exist", "flow"
        if int(m.group(2)) not in ix.branches.get(m.group(1), set()):
            return f"{m.group(1)} has no branch at step {m.group(2)}", "flow"
        return None, "flow"
    m = re.match(r"^(F\d+)(?:\s+step\s+(\d+)(?:\s*[-–→>]+\s*\d+)?)?\b", s)
    if m and (len(s) == len(m.group(0)) or s[len(m.group(0)):].strip().startswith(("(", ",", ":"))):
        if m.group(1) not in ix.flows:
            return f"flow {m.group(1)} does not exist", "flow"
        if m.group(2) and int(m.group(2)) not in ix.flows[m.group(1)]:
            return f"{m.group(1)} has no step {m.group(2)}", "flow"
        return None, "flow"
    m = re.match(r"^(DI-\d+)" + GLOSS + "$", s)
    if m:
        return (None if m.group(1) in ix.di else f"{m.group(1)} is not in mom-design-inputs.yaml"), "DI"
    m = re.match(r"^MATRIX\s+([\d.]+)", s)
    if m:
        return (None if m.group(1).rstrip(".") in ix.matrix else f"{s}: no such matrix ref in traceability.json"), "MATRIX"
    m = re.match(r"^ADR-?(\d{1,4})\b", s)
    if m:
        return (None if m.group(1).zfill(4) in ix.adrs else f"{s}: no such ADR"), "ADR"
    m = re.match(r"^screens/([\w.-]+\.yaml)#([A-Z]{2,4}-\d{3})(?=$|[\s(])", s)
    if m:
        return (None if m.group(2) in ix.screen_file.get(m.group(1), set()) else f"{s}: no such screen in that file"), "screen"
    m = re.match(r"^(POSV2-\d+[a-z]?)" + GLOSS + "$", s)
    if m:
        return (None if m.group(1) in ix.posv2 else f"{s}: not in pos-v2-decisions.json"), "POSV2"
    # the rev 3 register: REV3-8b, REV3-2 (gloss), "REV3 23SEP-3", "REV3 DG-4", DG-3, 23SEP-19, GAP-D2
    m = re.match(r"^(REV3-\d+[a-z]?|(?:REV3\s+)?(?:23SEP-\d+|DG-\d+|GAP-[A-Z]\d+|CFG-\d+|M17-\d+))" + GLOSS + "$", s)
    if m and (s.startswith("REV3") or not s.startswith(("CFG", "M17"))):
        ref = re.sub(r"^REV3\s+", "", m.group(1))
        return (None if ref in ix.rev3 else f"{s}: {ref} is not in rev3-decisions.json"), "REV3"
    m = re.match(r"^R-?[A-Z0-9-]*\d+[a-z]?(\s*\(.*\))?$", s)
    if m:
        base = re.match(r"^(R-?[A-Z0-9-]*\d+)", s).group(1)
        return (None if base in ix.r or base.rstrip("abcdefg") in ix.r else f"{s}: not in the audit register"), "R"
    m = re.match(r"^([A-Z]{2,4}-\d{3})" + GLOSS + "$", s)
    if m:
        return (None if m.group(1) in ix.screens else f"{s}: screen {m.group(1)} does not exist"), "screen"
    m = re.match(r"^([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{1,2}SEP)(?=$|[\s(])(.*)$", s)
    if m:
        return _design_doc(m.group(1), m.group(2), ix), "design round"
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
        # a path may contain spaces ("sources/designs/.../TICVAI Mobile App v4.dc.html (Booking group)"):
        # the longest prefix that exists is the path, what follows it is a locator
        words = s.split("#", 1)[0].split(" ")
        for k in range(len(words), 0, -1):
            if (ROOT / " ".join(words[:k])).exists():
                return None, "path"
        return f"{s}: {s.split('#', 1)[0].split(' (', 1)[0]} does not exist", "path"
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
    parts = _split_top(str(src), ";|")
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
            for cid in CHG_ID.findall(s):
                if cid not in change_ids():
                    errs.append(f"{rel}: {where}: {cid} is not a change entry in changes/entries/")

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
        for i, c in enumerate(e.get("corrections") or []):
            if not isinstance(c, dict) or ("status" not in c and "by" not in c):
                continue
            stats["corrections " + str(c.get("status"))] += 1
            if c.get("status") not in CORRECTION_STATUS:
                errs.append(f"{rel}: {sid}.corrections[{i}]: status {c.get('status')!r} is not one of {CORRECTION_STATUS}")
            if not CHG_ID.fullmatch(str(c.get("by") or "")):
                errs.append(f"{rel}: {sid}.corrections[{i}]: `by` must name the change entry (CHG-<BATCH>-<nnn>)")
            elif c["by"] not in change_ids():
                errs.append(f"{rel}: {sid}.corrections[{i}]: {c['by']} is not a change entry in changes/entries/")
        decided_qs = set()
        for i, d in enumerate(e.get("decisions") or []):
            where = f"{sid}.decisions[{i}]"
            stats["decisions"] += 1
            if not isinstance(d, dict):
                errs.append(f"{rel}: {where}: a decision must be a mapping")
                continue
            for k in ("question", "decision", "decidedBy", "date", "source"):
                if not d.get(k):
                    errs.append(f"{rel}: {where}: no `{k}`")
            if d.get("date") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(d["date"])):
                errs.append(f"{rel}: {where}: date {d['date']!r} is not YYYY-MM-DD")
            if "reviewable" in d and not isinstance(d["reviewable"], bool):
                errs.append(f"{rel}: {where}: reviewable must be true or false")
            stats["decisions reviewable"] += bool(d.get("reviewable"))
            parts = [p.strip() for p in str(d.get("source") or "").split("|") if p.strip()]
            if parts and not any(CHG_ID.fullmatch(p) for p in parts):
                errs.append(f"{rel}: {where}: source names no change entry (CHG-<BATCH>-<nnn>) recording the decision")
            for p in parts:
                if CHG_ID.fullmatch(p):
                    if p not in change_ids():
                        errs.append(f"{rel}: {where}: {p} is not a change entry in changes/entries/")
                elif not re.fullmatch(r"DEC-\d{3}", p):
                    errs.append(f"{rel}: {where}: source {p!r} is neither a DEC-<nnn> ledger id nor a CHG id")
            if d.get("questionSource"):
                src_ok(where + ".questionSource", {"source": d["questionSource"]})
            decided_qs.add(str(d.get("question") or "").strip())
        for i, q in enumerate(e.get("openQuestions") or []):
            if isinstance(q, dict) and str(q.get("question") or "").strip() in decided_qs:
                errs.append(f"{rel}: {sid}.openQuestions[{i}]: already decided on this screen; it belongs in `decisions` only")
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
    kinds = ", ".join(f"{k} {v}" for k, v in sorted(stats.items())
                      if k not in ("screens", "rules") and not k.startswith(("decisions", "corrections ")))
    decided = ", ".join(f"{k} {v}" for k, v in sorted(stats.items()) if k.startswith(("decisions", "corrections ")))
    print(f"design notes: {len(files)} file(s), {stats['screens']} screens, {stats['rules']} rules; "
          f"sources: {kinds}; {decided or 'no decisions'}; {len(errs)} error(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
