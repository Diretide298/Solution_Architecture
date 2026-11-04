#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The fields of the authored inputs that the refresh owns, declared as data (r14 review finding E-03).

**The package rule is that authored inputs change only with a change entry**: contracts/, screens/, flows/, states/,
events/ and docs/adr/ are written by people, and `tools/refresh.sh` derives everything else. Some refresh steps
nevertheless write *into* those files: r13's derive commit a657374c rewrote 412 `provenance` sentences across
fourteen screen files, and the r10 and r11 derive commits touched 25 and 6 contract and screen files. Nothing said
which of those writes a refresh is allowed to make, so a hand edit committed under "derived" was indistinguishable
from a derivation. The lead (r14): "The derive must stop writing authored files, or declare exactly the derived
fields it owns." This module is that declaration; `tools/check-derived-fields.py` holds a refresh to it.

**Every write below was read off the tool that makes it**, not inferred from a diff (refresh.sh as of r14: steps
19-25 and 34-35 of handoff/refresh-manifest.json, plus `derive-screen-wiring` and `derive-state-views`, which joined
refresh.sh after the manifest was last traced and are missing from it). No refresh step writes states/, events/ or
docs/adr/; `derive-write-decisions` writes docs/active/, which is not authored.

## The path syntax

A field path is dot-separated, matched against a parsed YAML document:

    key        that map key                  *        every map key
    key[]      every item of the list `key`  key[?f]  the items of `key` that filter `f` (FILTERS below) accepts
    (a filter token may only end a path: it declares list items, matched one side at a time)

    contracts/*.yaml   paths.*.*.x-ticvai-consumed-by      every operation's consumed-by list
    screens/P*.yaml    screens[].navigation.transitions[?flow-edge]   the transitions derive-transitions writes

File globs are `fnmatch` patterns on the package-relative path, in which `*` also crosses `/`.

## What a rule allows (`mode`)

    whole    the whole file is derived: any change, its creation and its deletion
    create   the file may be created when `when(doc)` holds (a generator that writes only new files); a change to
             it or its deletion is a hand edit
    strip    every value at the path is derived: removed from both sides before they are compared (`strip`)
    fill     written only where the field is absent (or null): adding it passes, changing or removing it does not;
             `when(value)` narrows what may be added
    replace  may be changed when `when(before, after, parent)` holds (a generator correcting text it recognises)
    grow     a list that may gain items `add(item, ctx)` accepts and lose items `drop(item, ctx)` accepts; its order
             is the generator's (it sorts)

A missing field, a null and an empty map or list are the same thing to the comparison, because the generators
create the containers they fill (`setdefault`): a screen gaining `entryState: {params: [...]}` is judged on the
params, not on `entryState` having appeared.

`strip(path, doc)` removes the strip-mode fields from a parsed document; `compare(path, before, after)` lists the
differences outside every declared field (dotted paths, a few per file); `differences()` is the same, uncapped.
"""
from __future__ import annotations

import copy
import fnmatch
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

import yaml

LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
LIMIT = 5                        # differences compare() returns per file


def base(to) -> str:
    """A transition's target without its `#anchor` (as derive-carries-from-entrystate reads it)."""
    return str(to or "").partition("#")[0]


def _prov(item) -> str:
    return str(item.get("provenance") or "") if isinstance(item, dict) else ""


# ── filters on list items (`key[?name]`) ────────────────────────────────────────────────────────────────────────────

FILTERS: dict[str, Callable] = {
    # derive-transitions-from-flows: "Anything this tool writes leads with `flow `"
    "flow-edge": lambda t: _prov(t).startswith("flow "),
    # label-launcher-edges: f"structural — {id} is {code}'s home screen and its exits are its launcher"
    "launcher-edge": lambda t: _prov(t).startswith("structural — ") and "home screen and its exits are its launcher"
                               in _prov(t),
    # derive-carries-from-entrystate.is_mine: provenance `derived — … declares entryState.params`
    "carries-edge": lambda t: _prov(t).startswith("derived — ") and "declares entryState.params" in _prov(t),
    # derive-components: "Every proposed component is marked `derived: true`"
    "derived-component": lambda c: isinstance(c, dict) and c.get("derived") is True,
    # derive-components makes a `contentBody` region only for what goes into it: a region of that name holding
    # nothing but derived components is the generator's
    "derived-region": lambda r: (isinstance(r, dict) and r.get("name") == "contentBody" and set(r) <= {"name",
                                 "components"} and bool(r.get("components"))
                                 and all(isinstance(c, dict) and c.get("derived") is True for c in r["components"])),
    # derive-screen-wiring S-NO-READ and S-ASYNC-POLL: apis entries stamped with STAMP
    "wiring-api": lambda a: _prov(a).startswith("Block A audit, 14 October 2026: "),
}


# ── predicates the grow, fill and replace rules use ─────────────────────────────────────────────────────────────────

def _screen(doc, sid):
    for s in (doc or {}).get("screens") or []:
        if isinstance(s, dict) and s.get("id") == sid:
            return s
    return None


def _nav(s) -> dict:
    n = (s or {}).get("navigation") if isinstance(s, dict) else None
    return n if isinstance(n, dict) else {}


def _flow_edge(src, dst) -> bool:
    """`src` has a same-platform transition to `dst` that derive-transitions-from-flows wrote (--adopt)."""
    return any(isinstance(t, dict) and base(t.get("to")) == dst and FILTERS["flow-edge"](t)
               and not t.get("crossesDevice") for t in (_nav(src).get("transitions") or []))


def exit_added(item, ctx) -> bool:
    """An exit the refresh adds: --adopt (a flow walked S -> X inside one app) or derive-carries pass 1 (X's
    entryFrom names S, mirrored into S's exitTo)."""
    s = ctx.screen_after
    other = _screen(ctx.after, item)
    return _flow_edge(s, item) or (other is not None and s is not None
                                   and s.get("id") in (_nav(other).get("entryFrom") or []))


def entry_added(item, ctx) -> bool:
    """An entryFrom the refresh adds: --adopt adds S to X's entryFrom when it adopts S -> X."""
    return _flow_edge(_screen(ctx.after, item), (ctx.screen_after or {}).get("id"))


PARAM_KEYS = {"name", "from", "optional", "notes"}


def param_added(item, ctx) -> bool:
    """An entry parameter in the shape `screen_patterns.param_for` (derive-entrystate-params) or derive-screen-wiring
    S-ASYNC-POLL writes: name, from, and an optional flag whose note starts "Optional: "."""
    return (isinstance(item, dict) and set(item) <= PARAM_KEYS and bool(item.get("name"))
            and item.get("from") in ("session", "deepLink", "navigation")
            and (("notes" not in item and "optional" not in item)
                 or (item.get("optional") is True and str(item.get("notes") or "").startswith("Optional: "))))


def param_dropped(item, ctx) -> bool:
    """derive-entrystate-params takes the identity a login mints off the door that mints it."""
    return isinstance(item, dict) and item.get("from") == "session" and item.get("name") in {
        "sessionId", "principalId", "operatorId"}


PURPOSE_BOILERPLATE = re.compile(          # derive-screen-wiring.PURPOSE_BOILERPLATE, verbatim
    r"^(Work with|See|Find|Add) .{2,80} for this venue\.?$"
    r"|Change how .{2,60} behaves here, and see which level the current value came from"
    r"|from the client design board"
    r"|^The screen this app sits on", re.I)


def purpose_rewritten(before, after, parent=None) -> bool:
    return bool(PURPOSE_BOILERPLATE.search(str(before or "")))


def api_purpose_rewritten(before, after, parent=None) -> bool:
    return str(before or "").strip().lower() in ("", "add something", "tbd", "todo") or bool(
        re.fullmatch(r"[a-z][A-Za-z0-9]+", str(before or "").strip()))       # the operationId as its own purpose


READ_LIKE = re.compile(           # derive-screen-wiring.READ_LIKE, verbatim
    r"^(search|evaluate|decide|resolve|preview|calculate|quote|check|validate|estimate|price|lookup|"
    r"identify|find|compute|simulate|match|suggest|run|list|get|query|render|verify|recommend)", re.I)


def trigger_corrected(before, after, parent=None) -> bool:
    """S-ONLOAD-WRITE (a write declared onLoad -> onAction) and the beacon rule (-> background) of
    derive-screen-wiring. A read is never moved off onLoad; which operations are writes is the contract's, so a
    read-like name is the test here."""
    op = str((parent or {}).get("operationId") or "")
    return after == "background" or (before == "onLoad" and after == "onAction" and not READ_LIKE.match(op))


def region_renamed(before, after, parent=None) -> bool:
    """S-DUP-REGION: an earlier region of a duplicated name takes its slot or a number after the name."""
    return isinstance(before, str) and isinstance(after, str) and after.startswith(before) and after != before


def note_linked(before, after, parent=None) -> bool:
    """W-INCOMING-UNLINKED appends "Drawn frame: … (linked by the Block A audit, 14 October 2026)." to the note."""
    b, a = str(before or "").rstrip(), str(after or "")
    return a.startswith(b) and re.fullmatch(r"\s?Drawn frame: \S.* \(linked by the Block A audit, 14 October 2026\)\.",
                                            a[len(b):]) is not None


def derived_flow(doc) -> bool:
    return isinstance(doc, dict) and doc.get("provenance") == "derived-from-board"


# ── the declaration ─────────────────────────────────────────────────────────────────────────────────────────────────

@dataclass
class Rule:
    glob: str
    path: str                    # "" for a whole-file rule
    mode: str
    step: str                    # the refresh step that owns it
    why: str                     # one line: why it is derived
    when: Optional[Callable] = None
    add: Optional[Callable] = None
    drop: Optional[Callable] = None
    tokens: list = field(default_factory=list, repr=False)


SCREENS = "screens/P*.yaml"
SCR = "screens[]."

RULES = [
    # whole files
    Rule("screens/_id-register.yaml", "", "whole", "34 derive-id-register --apply",
         "the high-water mark of every screen id prefix, counted from screens/P*.yaml"),
    Rule("flows/F*.yaml", "", "create", "19 derive-board-flows --apply",
         "one flow per client board, routed through the screens' declared navigation; written only when absent",
         when=derived_flow),

    # contracts
    Rule("contracts/*.yaml", "paths.*.*.x-ticvai-consumed-by", "strip", "35 link-screens-contracts",
         "the screens that call the operation, read from screens/P*.yaml apis"),
    Rule("contracts/*.yaml", "info.x-ticvai-screen-count", "strip", "35 link-screens-contracts",
         "the number of screens calling the contract"),

    # screens: navigation
    Rule(SCREENS, SCR + "navigation.transitions[?flow-edge]", "strip", "20 derive-transitions-from-flows --adopt",
         "an edge a flow walks, labelled from the flow step (provenance 'flow ...')"),
    Rule(SCREENS, SCR + "navigation.transitions[?launcher-edge]", "strip", "21 label-launcher-edges",
         "a home screen's exit, labelled with the destination's name (provenance 'structural — ... launcher')"),
    Rule(SCREENS, SCR + "navigation.transitions[?carries-edge]", "strip", "22 derive-carries-from-entrystate",
         "an edge carrying what the destination declares and the source holds (provenance 'derived — ... "
         "declares entryState.params'); recomputed every run"),
    Rule(SCREENS, SCR + "navigation.transitions[].carries", "fill", "22 derive-carries-from-entrystate (pass 4)",
         "filled on a flow, board or structural edge that says nothing about what it carries"),
    Rule(SCREENS, SCR + "navigation.exitTo", "grow", "20 derive-transitions-from-flows --adopt; 22 "
         "derive-carries-from-entrystate (pass 1)",
         "an exit a flow walks inside one app, or the parent of a child's entryFrom; added and sorted, never "
         "removed", add=exit_added),
    Rule(SCREENS, SCR + "navigation.entryFrom", "grow", "20 derive-transitions-from-flows --adopt",
         "the source of an adopted flow edge; added and sorted, never removed", add=entry_added),

    # screens: entry state
    Rule(SCREENS, SCR + "entryState.params", "grow", "23 derive-entrystate-params; derive-screen-wiring "
         "S-ASYNC-POLL",
         "a path parameter of an operation the screen calls, in screen_patterns.param_for's shape; a session id "
         "is taken off the screen that mints the session", add=param_added, drop=param_dropped),

    # screens: layout
    Rule(SCREENS, SCR + "layout.regions[?derived-region]", "strip", "24 derive-components",
         "the contentBody region made to hold proposed components"),
    Rule(SCREENS, SCR + "layout.regions[].components[?derived-component]", "strip", "24 derive-components",
         "a component the screen's operations imply, marked derived: true"),
    Rule(SCREENS, SCR + "layout.regions[].components[].operation", "fill", "derive-screen-wiring S-OP-UNREACHED, "
         "S-METRIC-NO-OP, S-NO-READ", "the declared operation an unbound control calls (invisible)"),
    Rule(SCREENS, SCR + "layout.regions[].components[].bindsTo", "fill", "derive-screen-wiring S-METRIC-NO-OP",
         "the response field a metric tile reads (invisible)"),
    Rule(SCREENS, SCR + "layout.regions[].name", "replace", "derive-screen-wiring S-DUP-REGION",
         "a duplicated region id made unique by its slot (internal id, never shown)", when=region_renamed),
    Rule(SCREENS, SCR + "overlays[].confirm.operation", "fill", "derive-screen-wiring S-BUTTON-FORM",
         "the write a dialog's confirm calls (invisible)"),

    # screens: apis and spec text
    Rule(SCREENS, SCR + "apis[].contract", "strip", "35 link-screens-contracts",
         "the contract that owns the operationId"),
    Rule(SCREENS, SCR + "apis[?wiring-api]", "strip", "derive-screen-wiring S-NO-READ, S-ASYNC-POLL",
         "a read the screen needs before an edit or after a 202 (provenance 'Block A audit, 14 October 2026')"),
    Rule(SCREENS, SCR + "apis[].purpose", "replace", "derive-screen-wiring S-PURPOSE-TEMPLATE",
         "an empty or placeholder api purpose, from the operation's summary", when=api_purpose_rewritten),
    Rule(SCREENS, SCR + "apis[].trigger", "replace", "derive-screen-wiring S-ONLOAD-WRITE, S-OP-UNREACHED",
         "a write declared onLoad fires on its control; a beacon runs in the background", when=trigger_corrected),
    Rule(SCREENS, SCR + "permission", "fill", "derive-screen-wiring S-SCREEN-PERMISSION",
         "the permission a staff screen's load needs, from x-ticvai-permission"),
    Rule(SCREENS, SCR + "division", "fill", "derive-screen-wiring S-DUP-SCREEN",
         "what a screen sharing its operations with others is for"),
    Rule(SCREENS, SCR + "purpose", "replace", "derive-screen-wiring S-PURPOSE-BOILERPLATE",
         "a generator's boilerplate purpose, rewritten from the operations", when=purpose_rewritten),

    # screens: wireframe
    Rule(SCREENS, SCR + "wireframe.board", "fill", "25 derive-board-anchors",
         "platform.wireframeBoard + '#' + the screen id"),
    Rule(SCREENS, SCR + "wireframe.status", "fill", "25 derive-board-anchors",
         "the block a screen with no wireframe gets", when=lambda v: v == "notStarted"),
    Rule(SCREENS, SCR + "wireframe.provenance", "fill", "25 derive-board-anchors",
         "the block a screen with no wireframe gets", when=lambda v: v == "generated"),
    Rule(SCREENS, SCR + "wireframe.stateViews", "strip", "derive-state-views --apply",
         "each state's pattern in the approved prototype, from screens/_state-patterns.yaml"),
    Rule(SCREENS, SCR + "wireframe.note", "replace", "derive-screen-wiring W-INCOMING-UNLINKED",
         "a link to the frame drawn under wireframes/incoming/, appended", when=note_linked),
]


def _tokens(path: str) -> list:
    """'a[].b.c[?f]' -> [('k','a'),('i',None),('k','b'),('k','c'),('i','f')]."""
    out = []
    for seg in path.split(".") if path else []:
        m = re.fullmatch(r"([^\[\]]+)((?:\[\??[\w-]*\])*)", seg)
        if not m:
            raise ValueError(f"bad path segment {seg!r} in {path!r}")
        out.append(("k", m.group(1)))
        for f in re.findall(r"\[\??([\w-]*)\]", m.group(2)):
            out.append(("i", f or None))
    for i, (k, f) in enumerate(out):
        if k == "i" and f and i != len(out) - 1:
            raise ValueError(f"a filter token may only end a path: {path!r}")
        if k == "i" and f and f not in FILTERS:
            raise ValueError(f"unknown filter {f!r} in {path!r}")
    return out


for _r in RULES:
    _r.tokens = _tokens(_r.path)


def rules_for(path: str) -> list:
    return [r for r in RULES if fnmatch.fnmatchcase(path, r.glob)]


def file_rule(path: str) -> Optional[Rule]:
    return next((r for r in rules_for(path) if r.mode in ("whole", "create")), None)


# ── matching ────────────────────────────────────────────────────────────────────────────────────────────────────────
# A concrete path is a list of steps: ('k', key) or ('i', label, item) where `item` is the list item on the side
# being judged (for a filter) or None.

def _match(tokens: list, steps: list, item=None) -> bool:
    if len(tokens) != len(steps):
        return False
    for i, (t, s) in enumerate(zip(tokens, steps)):
        if t[0] != s[0]:
            return False
        if t[0] == "k" and t[1] != "*" and t[1] != s[1]:
            return False
        if t[0] == "i" and t[1]:
            if i != len(tokens) - 1 or not FILTERS[t[1]](item):
                return False
    return True


def _stripped(rules, steps, item=None) -> bool:
    return any(r.mode == "strip" and _match(r.tokens, steps, item) for r in rules)


def _rule(rules, steps, mode):
    return next((r for r in rules if r.mode == mode and _match(r.tokens, steps)), None)


def strip(path: str, doc):
    """Remove every strip-mode field the declaration names for `path` from `doc` (a deep copy is returned)."""
    rules = [r for r in rules_for(path) if r.mode == "strip"]
    doc = copy.deepcopy(doc)

    def walk(node, steps):
        if isinstance(node, dict):
            for k in list(node):
                st = steps + [("k", k)]
                if _stripped(rules, st):
                    del node[k]
                else:
                    walk(node[k], st)
        elif isinstance(node, list):
            keep = []
            for it in node:
                st = steps + [("i", None)]
                if not _stripped(rules, st, it):
                    walk(it, st)
                    keep.append(it)
            node[:] = keep
    walk(doc, [])
    return doc


# ── comparing ───────────────────────────────────────────────────────────────────────────────────────────────────────

LIST_KEYS = ("id", "operationId", "to", "name", "step", "state")
INDEXED = {("screens", "layout", "regions")}        # renamed by S-DUP-REGION: matched by position, not name


@dataclass
class Ctx:
    before: object
    after: object
    screen_after: Optional[dict] = None


def _empty(v) -> bool:
    return v is None or v == {} or v == []


def _key_of(items: list, steps: list):
    """The field that identifies the items of a list, if one is present and unique on this side."""
    names = tuple(s[1] for s in steps if s[0] == "k")
    if names in INDEXED:
        return None
    if not items or not all(isinstance(x, dict) for x in items):
        return None
    for k in LIST_KEYS:
        vals = [x.get(k) for x in items]
        if all(isinstance(v, (str, int)) for v in vals) and len(set(map(str, vals))) == len(vals):
            return k
    return None


def _label(steps: list) -> str:
    out = ""
    for s in steps:
        if s[0] == "k":
            out += ("." if out else "") + str(s[1])
        else:
            out += f"[{s[1]}]" if s[1] is not None else "[]"
    return out or "(document)"


def differences(path: str, before, after) -> list:
    """Every difference between two parsed documents outside the fields the refresh owns: (dotted path, kind), kind
    one of added, removed, changed, reordered."""
    rules = rules_for(path)
    found: list = []

    def scalar_list(a, b) -> bool:
        return all(not isinstance(x, (dict, list)) for x in (a or []) + (b or []))

    def walk(a, b, steps, screen_after=None, parent=None):
        if _empty(a) and _empty(b):
            return
        if a == b:
            return
        # a declared field: fill (absent before), replace (the generator's own correction)
        r = _rule(rules, steps, "fill")
        if r and _empty(a) and (r.when is None or r.when(b)):
            return
        r = _rule(rules, steps, "replace")
        if r and r.when(a, b, parent):
            return
        if isinstance(a, dict) or isinstance(b, dict):
            if not (isinstance(a, dict) or a is None) or not (isinstance(b, dict) or b is None):
                found.append((_label(steps), "changed"))
                return
            a, b = a or {}, b or {}
            for k in list(a) + [k for k in b if k not in a]:
                st = steps + [("k", k)]
                if _stripped(rules, st):
                    continue
                walk(a.get(k), b.get(k), st, screen_after, b)
            return
        if isinstance(a, list) or isinstance(b, list):
            if not (isinstance(a, list) or a is None) or not (isinstance(b, list) or b is None):
                found.append((_label(steps), "changed"))
                return
            item_steps = steps + [("i", None)]
            a = [x for x in (a or []) if not _stripped(rules, item_steps, x)]
            b = [x for x in (b or []) if not _stripped(rules, item_steps, x)]
            grow = _rule(rules, steps, "grow")
            if scalar_list(a, b):
                sa, sb = list(map(str, a)), list(map(str, b))
                c = Ctx(before, after, screen_after)
                for x in [x for x in b if str(x) not in sa]:
                    if not (grow and grow.add and grow.add(x, c)):
                        found.append((f"{_label(steps)}[{x}]", "added"))
                for x in [x for x in a if str(x) not in sb]:
                    if not (grow and grow.drop and grow.drop(x, c)):
                        found.append((f"{_label(steps)}[{x}]", "removed"))
                if not grow and sorted(sa) == sorted(sb) and sa != sb:
                    found.append((_label(steps), "reordered"))
                return
            ka, kb = _key_of(a, steps), _key_of(b, steps)
            if ka and ka == kb:
                da = {str(x[ka]): x for x in a}
                db = {str(x[ka]): x for x in b}
                c = Ctx(before, after, screen_after)
                for lab, x in db.items():
                    if lab not in da and not (grow and grow.add and grow.add(x, c)):
                        found.append((f"{_label(steps)}[{lab}]", "added"))
                for lab, x in da.items():
                    if lab not in db and not (grow and grow.drop and grow.drop(x, c)):
                        found.append((f"{_label(steps)}[{lab}]", "removed"))
                common_a = [k for k in da if k in db]
                common_b = [k for k in db if k in da]
                if not grow and common_a != common_b:
                    found.append((_label(steps), "reordered"))
                for lab in common_a:
                    sa = db[lab] if steps == [("k", "screens")] else screen_after
                    walk(da[lab], db[lab], steps + [("i", lab)], sa)
                return
            for i in range(max(len(a), len(b))):
                x = a[i] if i < len(a) else None
                y = b[i] if i < len(b) else None
                sa = y if steps == [("k", "screens")] else screen_after
                if x is None or y is None:
                    c = Ctx(before, after, screen_after)
                    if y is not None and grow and grow.add and grow.add(y, c):
                        continue
                    if x is not None and grow and grow.drop and grow.drop(x, c):
                        continue
                    found.append((f"{_label(steps)}[{i}]", "added" if x is None else "removed"))
                    continue
                walk(x, y, steps + [("i", i)], sa)
            return
        found.append((_label(steps), "changed"))

    walk(before, after, [])
    return found


def _load(text: str):
    return yaml.load(text, Loader=LOADER)


def is_yaml(path: str) -> bool:
    return path.endswith((".yaml", ".yml"))


def compare_all(path: str, before_text: Optional[str], after_text: Optional[str]) -> list:
    """Every difference outside the declared fields between two versions of `path` (None: the file is absent), as
    (dotted path, kind); a whole-file finding has the path "(file)"."""
    fr = file_rule(path)
    if fr and fr.mode == "whole":
        return []
    if before_text is None and after_text is None:
        return []
    if before_text is None or after_text is None:
        if fr and fr.mode == "create" and before_text is None and is_yaml(path):
            try:
                if fr.when(_load(after_text)):
                    return []
            except yaml.YAMLError:
                pass
        return [("(file)", "added" if before_text is None else "deleted")]
    if fr and fr.mode == "create":
        # a generator that writes only new files never changes one
        if before_text.replace("\r\n", "\n") == after_text.replace("\r\n", "\n"):
            return []
        try:
            if _load(before_text) == _load(after_text):
                return []
        except yaml.YAMLError:
            pass
        return [("(file)", "changed; the step that writes it only ever creates it")]
    if not is_yaml(path):
        if before_text.replace("\r\n", "\n") == after_text.replace("\r\n", "\n"):
            return []
        return [("(file)", "changed; not YAML, and no step owns it")]
    try:
        a, b = _load(before_text), _load(after_text)
    except yaml.YAMLError as e:
        return [("(file)", f"not parseable YAML: {str(e).splitlines()[0]}")]
    return differences(path, a, b)


def compare(path: str, before_text: Optional[str], after_text: Optional[str]) -> list:
    """The dotted paths of the differences outside the fields the refresh owns, at most LIMIT of them."""
    return [p for p, _k in compare_all(path, before_text, after_text)[:LIMIT]]


def summary() -> list:
    """One line per rule, for --list."""
    return [f"{r.glob:28} {r.mode:8} {r.path or '(whole file)'}  <- {r.step}: {r.why}" for r in RULES]
