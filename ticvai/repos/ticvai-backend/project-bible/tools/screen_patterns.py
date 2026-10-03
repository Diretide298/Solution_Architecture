#!/usr/bin/env python3
"""The six screen patterns the Block A audit of 3 October found, as rules a check and a fix share.

**Found on live r2 by the Block A audit** (`changes/entries/CHG-AUD-001-block-a-audit-patterns-for-r3.yaml`,
counted across the package by the zero-AI pattern scans): a designer or a developer reading a screen
was told to ask for a field the server sets, shown every field of a schema on a phone, told the wrong
permission, sent to a screen nothing could open, handed another screen's route, and told a Block A
screen was not in the first release. Each pattern is a rule here; `tools/check-screen-patterns.py`
fails on any of them, and `tools/applied/spec-screen-patterns-3-october.py` used the same rules to
find what it fixed (CHG-SPF-001..006).

    P1   a form asks for a field the request schema marks `readOnly`
    P2   a list or panel shows a schema unfiltered: more than five columns on a phone or handheld,
         every property of a schema wider than five, a generated dump wider than the desktop caps,
         or the generator's own "Columns are every field" admission
    P3   the no-access state names a permission no operation on the screen requires, leaves out the
         permission the screen's read needs, or leaves out the one its actions need beyond it
    P5   a required entry parameter that no inbound edge carries and the session does not supply
    P7b  an implementation route or component that belongs to another screen (shared by two
         screens, or named for something else)
    P8   a Block A screen that says it is not in the first release, or carries a wave other than 1

The helpers (`pick_columns`, `no_access_text`, `reads_itself`) are what the generators use so they
cannot write the pattern again.
"""
from __future__ import annotations

import glob
import json
import os
import re
from collections import defaultdict

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOAD_TRIGGERS = {"onLoad", "onInterval", "background", None}
INPUT_KINDS = {"selectField", "textField", "toggle", "numberField", "datePicker", "multiSelect",
               "searchField", "fileUpload", "consentBlock", "scanTarget", "seatMap"}
COLUMN_KINDS = {"dataTable", "detailPanel", "cardList"}
SMALL_FORM_FACTORS = {"mobileApp", "handheld"}

# P2: at most five on a phone or handheld (Chinmay's brief, 3 October); on a desktop a generated
# dump wider than these is narrowed. A workshop pack's own field list is the client's document and
# is not capped.
SMALL_MAX = 5
DESKTOP_CAP = {"dataTable": 8, "detailPanel": 12, "cardList": 6}
# What the picker keeps when it narrows a component.
PICK_SMALL = {"dataTable": 4, "detailPanel": 5, "cardList": 4}
PICK_DESKTOP = {"dataTable": 6, "detailPanel": 8, "cardList": 5}

COLUMNS_NOTE = re.compile(r"Columns are every field")


def _load(path):
    with open(path, encoding="utf-8") as fh:
        txt = fh.read()
    try:
        return yaml.load(txt, Loader=yaml.CSafeLoader)
    except Exception:  # noqa: BLE001 — no libyaml, or an escape only the Python reader accepts
        return yaml.safe_load(txt)


# ── the package ───────────────────────────────────────────────────────────────────────────────

class Package:
    """Screens (with platform), operations and schemas per contract, read once."""

    def __init__(self, root: str = ROOT, screens: dict | None = None):
        self.root = root
        self.platforms, self.screens, self.files = {}, {}, {}
        if screens is None:
            for f in sorted(glob.glob(os.path.join(root, "screens", "P*.yaml"))):
                d = _load(f)
                code = d["platform"]["code"]
                self.platforms[code] = d["platform"]
                self.files[code] = f
                for s in d.get("screens") or []:
                    s["_plat"] = code
                    self.screens[s["id"]] = s
        else:
            self.screens = screens
        self.contracts, self.ops = {}, {}
        for f in sorted(glob.glob(os.path.join(root, "contracts", "*", "*.yaml"))):
            name = os.path.splitext(os.path.basename(f))[0]
            c = _load(f) or {}
            self.contracts[name] = c
            for path, item in (c.get("paths") or {}).items():
                if not isinstance(item, dict):
                    continue
                for method, o in item.items():
                    if isinstance(o, dict) and o.get("operationId"):
                        self.ops[o["operationId"]] = dict(o, _contract=name, _method=method,
                                                          _path=path)
        self._resp = {}

    def small(self, sid: str) -> bool:
        return (self.platforms.get(self.screens[sid]["_plat"]) or {}).get("formFactor") \
            in SMALL_FORM_FACTORS

    # schema resolution, $ref and allOf, after the audit's pattern scans
    def deref(self, contract, node):
        n = 0
        while isinstance(node, dict) and "$ref" in node and n < 8:
            f, _, frag = node["$ref"].partition("#")
            contract = os.path.splitext(os.path.basename(f))[0] if f else contract
            tgt = self.contracts.get(contract, {})
            for part in frag.strip("/").split("/"):
                tgt = tgt.get(part) if isinstance(tgt, dict) else None
            node, n = tgt, n + 1
        return contract, node

    def resolve(self, contract, node, depth=0):
        out = {"properties": {}, "required": set()}
        if not isinstance(node, dict) or depth > 12:
            return out
        if "$ref" in node:
            c2, tgt = self.deref(contract, {"$ref": node["$ref"]})
            return self.resolve(c2, tgt, depth + 1)
        for sub in node.get("allOf") or []:
            r = self.resolve(contract, sub, depth + 1)
            out["properties"].update(r["properties"])
            out["required"] |= r["required"]
        for k, v in (node.get("properties") or {}).items():
            out["properties"][k] = v
        out["required"] |= set(node.get("required") or [])
        return out

    def schema(self, name, prefer=None):
        for c in ([prefer] if prefer else []) + list(self.contracts):
            if c and name in (((self.contracts.get(c) or {}).get("components") or {})
                              .get("schemas") or {}):
                return c, self.resolve(c, {"$ref": "#/components/schemas/" + name})
        return None, None

    def request_schema(self, op_id):
        o = self.ops.get(op_id)
        if not o or not o.get("requestBody"):
            return None
        c, rb = self.deref(o["_contract"], o["requestBody"])
        content = (rb or {}).get("content") or {}
        sch = ((content.get("application/json") or {}).get("schema")
               or next((v.get("schema") for v in content.values() if isinstance(v, dict)), None))
        return self.resolve(c, sch) if sch else None

    def response_props(self, op_id) -> set:
        """Every property name a success response carries, at any depth (rows of a page too)."""
        if op_id in self._resp:
            return self._resp[op_id]
        out: set = set()
        o = self.ops.get(op_id)
        if o:
            for code, r in (o.get("responses") or {}).items():
                if not str(code).startswith("2"):
                    continue
                c, r = self.deref(o["_contract"], r)
                for media in ((r or {}).get("content") or {}).values():
                    if isinstance(media, dict) and media.get("schema"):
                        self._names(c, media["schema"], out, 0, set())
        self._resp[op_id] = out
        return out

    def _names(self, contract, node, out, depth, seen):
        if depth > 6 or not isinstance(node, dict):
            return
        if "$ref" in node:
            if node["$ref"] in seen:
                return
            seen = seen | {node["$ref"]}
            sname = node["$ref"].rsplit("/", 1)[-1]
            c2, tgt = self.deref(contract, node)
            if isinstance(tgt, dict):
                props = self.resolve(c2, tgt)["properties"]
                if "id" in props and sname:
                    out.add(sname[0].lower() + sname[1:] + "Id")
                    out.add("@" + sname)               # the schema whose id this is
                self._names(c2, tgt, out, depth + 1, seen)
            return
        for k in ("allOf", "oneOf", "anyOf"):
            for sub in node.get(k) or []:
                self._names(contract, sub, out, depth + 1, seen)
        if isinstance(node.get("items"), dict):
            self._names(contract, node["items"], out, depth + 1, seen)
        for k, v in (node.get("properties") or {}).items():
            out.add(k)
            self._names(contract, v, out, depth + 1, seen)

    def op_perms(self, op_id) -> set:
        o = self.ops.get(op_id) or {}
        out = set()
        p = o.get("x-ticvai-permission")
        if isinstance(p, str):
            out.add(p)
        elif isinstance(p, list):
            out |= {str(x) for x in p}
        pm = o.get("x-ticvai-permission-by-module")
        if isinstance(pm, dict):
            out |= {str(v) for v in pm.values() if isinstance(v, str)}
        return out


def components(s):
    for r in ((s.get("layout") or {}).get("regions") or []):
        for c in (r.get("components") or []):
            if isinstance(c, dict):
                yield r, c


def apis(s):
    return [a for a in (s.get("apis") or []) if isinstance(a, dict) and a.get("operationId")]


def block_a_screens(root: str = ROOT) -> set | None:
    """The screens Block A tasks build, from the release the tickets were cut from; None if absent."""
    p = os.path.join(root, "handoff", "service-docs", "op-release.json")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        rel = json.load(fh)
    T = {t["key"]: t for t in rel["tickets"]}

    def root_of(k):
        n = 0
        while T.get(k) and T[k].get("parent") and n < 20:
            k, n = T[k]["parent"], n + 1
        return k
    out = set()
    for t in rel["tickets"]:
        if t.get("type") == "Task" and root_of(t["key"]) in ("BLOCK-A", "BLOCK-A2"):    # both drops (CHG-RONEP-007)
            for b in t.get("builds") or []:
                kind, _, val = b.partition(" ")
                if kind == "screen":
                    out.add(val)
    return out


# ── P1: forms that ask for a readOnly field ─────────────────────────────────────────────────────

def read_only(sch, field) -> bool:
    p = (sch or {}).get("properties", {}).get(field)
    return isinstance(p, dict) and p.get("readOnly") is True


def overlay_asked(o) -> set:
    asked = set((o.get("dismiss") or {}).get("discards") or [])
    body = str(o.get("body") or "")
    m = re.search(r"Required:(.*?)(Optional:|Dismissing|$)", body, re.S)
    if m:
        asked |= set(re.findall(r"`([A-Za-z0-9_]+)`", m.group(1)))
    m = re.search(r"Optional:(.*?)(Dismissing|$)", body, re.S)
    if m:
        asked |= set(re.findall(r"`([A-Za-z0-9_]+)`", m.group(1)))
    return asked


def p1(pk: Package, sid: str, s: dict) -> list:
    out = []
    for _, c in components(s):
        if c.get("kind") not in INPUT_KINDS or "." not in str(c.get("bindsTo") or ""):
            continue
        field = str(c["bindsTo"]).split(".", 1)[1]
        sch = pk.request_schema(c.get("operation")) if c.get("operation") else None
        if sch and field in sch["properties"] and read_only(sch, field):
            out.append(("P1", sid, f"input '{c.get('label')}' asks for {field}, which "
                                   f"{c.get('operation')} marks readOnly"))
    for o in s.get("overlays") or []:
        if not isinstance(o, dict):
            continue
        op = (o.get("confirm") or {}).get("operation")
        sch = pk.request_schema(op) if op else None
        if not sch:
            continue
        for f in sorted(overlay_asked(o)):
            if read_only(sch, f):
                out.append(("P1", sid, f"overlay {o.get('id')} asks for {f}, which {op} marks "
                                       f"readOnly (the server sets it)"))
    return out


# ── P2: unfiltered columns ──────────────────────────────────────────────────────────────────────

def column_schema(pk: Package, c: dict):
    cols = [str(x) for x in (c.get("columns") or [])]
    names = {x.split(".", 1)[0] for x in cols if "." in x}
    b = str(c.get("bindsTo") or "").split(".", 1)[0].rstrip("[]")
    name = b or (sorted(names)[0] if len(names) == 1 else "")
    if not name:
        return "", None
    _, sch = pk.schema(name, (pk.ops.get(c.get("operation")) or {}).get("_contract"))
    return name, sch


def generated(c: dict) -> bool:
    return str(c.get("provenance") or "").startswith("contract ")


def p2(pk: Package, sid: str, s: dict) -> list:
    out = []
    small = pk.small(sid)
    for _, c in components(s):
        cols = [str(x) for x in (c.get("columns") or [])]
        kind = c.get("kind")
        if not cols or kind not in COLUMN_KINDS:
            continue
        label = c.get("label") or kind
        if small and len(cols) > SMALL_MAX:
            out.append(("P2", sid, f"{kind} '{label}' shows {len(cols)} columns on a "
                                   f"{'phone or handheld'}; at most {SMALL_MAX}"))
            continue
        name, sch = column_schema(pk, c)
        props = set((sch or {}).get("properties") or {})
        fields = {x.split(".", 1)[1].split(".")[0] for x in cols if x.startswith(name + ".")}
        if props and len(props) >= 4 and props <= fields and                 len(cols) > (PICK_SMALL if small else PICK_DESKTOP)[kind]:
            out.append(("P2", sid, f"{kind} '{label}' shows every one of {name}'s "
                                   f"{len(props)} properties"))
        elif not small and generated(c) and len(cols) > DESKTOP_CAP[kind]:
            out.append(("P2", sid, f"generated {kind} '{label}' shows {len(cols)} columns "
                                   f"(cap {DESKTOP_CAP[kind]})"))
    if COLUMNS_NOTE.search(str(s.get("apisNote") or "")):
        out.append(("P2", sid, "apisNote still says the columns are every field"))
    return out


DROP_ALWAYS = {"id", "scopePath", "tenantId", "cellId", "etag", "version", "schemaVersion",
               "_links", "meta", "createdBy", "updatedBy", "deletedAt", "contentHash",
               "signatureKeyId", "rowVersion", "draftVersion"}
NAMEISH = re.compile(r"(^|[a-z])(name|title|label|code|reference|number|displayName|subject|"
                     r"description|headline)$", re.I)
STATUSISH = re.compile(r"(status|state|health|severity|priority|stage|outcome|result|decision)$",
                       re.I)
KINDISH = re.compile(r"(kind|type|category|channel|method|role|mode|tier|level)$", re.I)
MONEYISH = re.compile(r"(amount|total|price|balance|quantity|qty|count|value|cost|fee|rate|"
                      r"capacity|remaining|sold|points|score|percent|minutes|seconds|duration)",
                      re.I)
DATEISH = re.compile(r"(At|Date|On|From|Until|Time|Day)$")


def column_score(col: str, prop: dict | None, kind: str, hints: str) -> int:
    f = col.split(".", 1)[1] if "." in col else col
    head = f.split(".")[0]
    leaf = f.rsplit(".", 1)[-1]
    if head in DROP_ALWAYS or leaf in DROP_ALWAYS:
        return -100
    score = 10
    if re.search(r"(Id|Ids)$", leaf):
        score = -20
    elif NAMEISH.search(leaf):
        score = 50
    elif STATUSISH.search(leaf):
        score = 40
    elif MONEYISH.search(leaf):
        score = 30
    elif KINDISH.search(leaf):
        score = 25
    elif DATEISH.search(leaf):
        score = 5 if leaf in ("createdAt", "updatedAt") else 20
    elif re.match(r"(is|has|can|requires)[A-Z]", leaf):
        score = 8
    t = (prop or {}).get("type")
    if (t in ("array", "object") or (prop or {}).get("$ref")) and kind != "detailPanel":
        score -= 15
    if hints and re.search(r"\b" + re.escape(leaf) + r"\b", hints):
        score += 35
    return score


def pick_columns(pk: Package | None, c: dict, small: bool, hints: str = "",
                 drop: set | frozenset = frozenset()) -> list:
    """The columns a component keeps: the most telling fields, plumbing and foreign ids out (and
    `drop`, the fields a guest never sees on a guest screen), original order kept."""
    cols = [str(x) for x in (c.get("columns") or [])]
    kind = c.get("kind") if c.get("kind") in COLUMN_KINDS else "dataTable"
    limit = (PICK_SMALL if small else PICK_DESKTOP)[kind]
    props = {}
    if pk is not None:
        _, sch = column_schema(pk, c)
        props = (sch or {}).get("properties") or {}
    scored = []
    for i, col in enumerate(cols):
        head = (col.split(".", 1)[1] if "." in col else col).split(".")[0]
        p = props.get(head)
        score = column_score(col, p if isinstance(p, dict) else None, kind, hints)
        if head in drop:
            score = -100
        scored.append((score, i, col))
    ranked = sorted(scored, key=lambda t: (-t[0], t[1]))
    keep = [x for x in ranked if x[0] > 0][:limit]
    if len(keep) < min(2, len(cols)):            # never leave a panel with nothing to show
        keep = [x for x in ranked if x[0] > -100][:min(2, len(cols))] or ranked[:min(2, len(cols))]
    return [col for _, _, col in sorted(keep, key=lambda t: t[1])]


# ── P3: the no-access state names the right permission ─────────────────────────────────────────

def named_permissions(txt: str) -> set:
    return (set(re.findall(r"`([A-Z][A-Z0-9_]{3,})`", txt))
            or set(re.findall(r"\b([A-Z]+_[A-Z0-9_]+)\b", txt)))


def screen_perms(pk: Package, s: dict):
    """`(load ops with their permissions, every op's permissions, action-only permissions)`."""
    a = apis(s)
    load = [x["operationId"] for x in a if x.get("trigger") in LOAD_TRIGGERS]
    lp = set().union(*[pk.op_perms(o) for o in load]) if load else set()
    ap = set().union(*[pk.op_perms(x["operationId"]) for x in a]) if a else set()
    return load, lp, ap, ap - lp


def p3(pk: Package, sid: str, s: dict) -> list:
    txt = str((s.get("states") or {}).get("emptyNoAccess") or "")
    named = named_permissions(txt)
    if not named:
        return []
    _, lp, ap, act = screen_perms(pk, s)
    out = []
    wrong = sorted(named - ap)
    if wrong:
        out.append(("P3", sid, f"no-access names {', '.join(wrong)}, which no operation on the "
                               f"screen requires"))
    if lp and not (named & lp):
        out.append(("P3", sid, f"no-access does not name the read's permission "
                               f"({', '.join(sorted(lp))})"))
    if act and not (named & act):
        out.append(("P3", sid, f"no-access names no permission the actions need beyond the read "
                               f"({', '.join(sorted(act))})"))
    return out


def no_access_text(pk: Package, s: dict) -> str | None:
    """The state, read off the operations: the read's permission, then what each action adds."""
    a = apis(s)
    load, lp, ap, act = screen_perms(pk, s)
    if not ap:
        return None
    reads = sorted([o for o in load if pk.op_perms(o)],
                   key=lambda o: not o.startswith(("list", "get", "search"))) or \
            [x["operationId"] for x in a if x["operationId"].startswith(("list", "get", "search"))
             and pk.op_perms(x["operationId"])] or [x["operationId"] for x in a
                                                     if pk.op_perms(x["operationId"])]
    rop = reads[0]
    rperm = sorted(pk.op_perms(rop))[0]
    others = sorted((lp or pk.op_perms(rop)) - {rperm})
    txt = (f"Shown when the caller lacks `{rperm}`, which `{rop}` requires to show this screen, "
           f"and names that permission")
    if others:
        txt += (" (the screen's other reads need " + ", ".join(f"`{p}`" for p in others[:4])
                + " and say so in their own panels)")
    txt += (". **Never an empty table** — that reads as *there is no data* and sends somebody to "
            "support with the wrong question.")
    need = act - {rperm} if lp else ap - pk.op_perms(rop)
    if need:
        by = defaultdict(list)
        for x in a:
            if x.get("trigger") in LOAD_TRIGGERS and lp:
                continue
            for p in sorted(pk.op_perms(x["operationId"]) & need):
                if x["operationId"] not in by[p]:
                    by[p].append(x["operationId"])
        parts = [f"`{p}` for " + ", ".join(f"`{o}`" for o in ops[:4])
                 + (f" and {len(ops) - 4} more" if len(ops) > 4 else "")
                 for p, ops in sorted(by.items())]
        txt += (" A caller who can see the screen but lacks what an action needs sees that action "
                "disabled, naming its permission: " + "; ".join(parts[:6]) + ".")
    return txt


# ── P5: required entry parameters nothing supplies ──────────────────────────────────────────────

def entry_params(s: dict) -> list:
    out = []
    for p in ((s.get("entryState") or {}).get("params") or []):
        if isinstance(p, dict) and p.get("name"):
            out.append(p)
        elif isinstance(p, str) and p:
            out.append({"name": p, "from": "navigation"})
    return out


def inbound(screens: dict) -> dict:
    out = defaultdict(list)
    for sid, s in screens.items():
        for t in ((s.get("navigation") or {}).get("transitions") or []):
            if isinstance(t, dict) and t.get("to"):
                out[str(t["to"]).partition("#")[0]].append((sid, set(t.get("carries") or [])))
    return out


def p5(pk: Package, sid: str, s: dict, inb: dict) -> list:
    out = []
    for p in entry_params(s):
        if p.get("optional") or p.get("from") in ("session", "previousScreen"):
            continue
        if any(p["name"] in c for _, c in inb.get(sid, [])):
            continue
        out.append(("P5", sid, f"requires {p['name']} (from {p.get('from')}) and none of its "
                               f"{len(inb.get(sid, []))} inbound edge(s) carries it"))
    return out


def stem_of(param: str) -> str:
    return param[:-2] if param.endswith("Id") else param


READ_VERBS = ("list", "search", "get")
MAKE_VERBS = re.compile(r"(create|start|open|request|begin|add|issue|register|submit|ask|send|join|"
                        r"run|import|generate|book|enrol|build|place|raise|log|report)[A-Z]")


def reads_itself(pk: Package, s: dict, name: str) -> str | None:
    """A read on the screen that returns `name` without taking it: the screen can show a list and let
    the user choose (or read the one in force), so it can open without being handed the id."""
    ops = [x["operationId"] for x in apis(s)]
    paths = {o: (pk.ops.get(o) or {}).get("_path", "") for o in ops}
    stem = stem_of(name).lower()
    for o in ops:
        if not o.startswith(READ_VERBS) or "{" + name + "}" in paths[o]:
            continue
        got = pk.response_props(o)
        if name in got:
            return o
        # `mapId` is the id of a `VenueMap` row: the schema name ends with the parameter's stem
        if o.startswith(("list", "search")) and any(
                g.startswith("@") and g[1:].lower().endswith(stem) for g in got):
            return o
    collections = set()
    for o in ops:
        m = re.search(r"/([^/{}]+)/\{" + re.escape(name) + r"\}", paths[o])
        if m:
            collections.add(((pk.ops.get(o) or {}).get("_contract"), m.group(1)))
    for o in ops:
        po = pk.ops.get(o) or {}
        if o.startswith(READ_VERBS) and po.get("_method") == "get" and                 "{" + name + "}" not in paths[o] and                 (po.get("_contract"), paths[o].rstrip("/").rsplit("/", 1)[-1]) in collections:
            return o
    return None


def creates(pk: Package, s: dict, name: str) -> str | None:
    """A write on the screen that makes the record `name` identifies (and so can open without it)."""
    stem = stem_of(name).lower()
    for x in apis(s):
        o = x["operationId"]
        po = pk.ops.get(o) or {}
        if po.get("_method") != "post" or not MAKE_VERBS.match(o) or "{" + name + "}" in po.get("_path", ""):
            continue
        got = pk.response_props(o)
        if stem in o.lower() or name in got or any(
                g.startswith("@") and g[1:].lower().endswith(stem) for g in got):
            return o
    return None


def param_for(pk: Package, s: dict, name: str, source: str = "navigation") -> dict:
    """The entry parameter a generator writes for `name`: required only when nothing else supplies
    it (CHG-SPF-004). Found by a read on the screen, made by a write on it, or taken only by an
    action from the row it acts on, it is optional and says why."""
    if source == "session":
        return {"name": name, "from": "session"}
    own = reads_itself(pk, s, name)
    if own:
        return {"name": name, "from": source, "optional": True,
                "notes": f"Optional: opened without it, the screen finds it with `{own}`."}
    made = creates(pk, s, name)
    if made:
        return {"name": name, "from": source, "optional": True,
                "notes": f"Optional: opened without it, the screen makes one with `{made}`."}
    users = [x for x in apis(s) if "{" + name + "}" in (pk.ops.get(x["operationId"]) or {})
             .get("_path", "")]
    if users and not any(x.get("trigger") in LOAD_TRIGGERS for x in users):
        return {"name": name, "from": source, "optional": True,
                "notes": f"Optional: only `{users[0]['operationId']}` takes it, from the record the "
                         f"user acts on."}
    return {"name": name, "from": source}


# ── P7b: a route or component that belongs to another screen ──────────────────────────────────

STOP = {"the", "and", "detail", "details", "list", "form", "directory", "screen", "page", "view",
        "board", "canvas", "general", "for", "with", "your", "my"}


def _words(x: str) -> set:
    out = set()
    for w in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|[0-9]+", x or ""):
        w = w.lower()
        if len(w) > 2 and w not in STOP:
            out.add(w[:-1] if w.endswith("s") and len(w) > 3 else w)
    return out


def _overlap(a: set, b: set) -> bool:
    return any(x == y or (min(len(x), len(y)) >= 4 and (x.startswith(y) or y.startswith(x)))
               for x in a for y in b)


def route_words(route: str, sid: str) -> set:
    segs = [g for g in str(route).strip("/").split("/") if g and not g.startswith((":", "{"))]
    return _words(" ".join(re.sub(r"-?" + re.escape(sid.lower()) + r"$", "", g).replace("-", " ")
                           for g in segs))


def p7b(pk: Package, sid: str, s: dict, comp_owner: dict) -> list:
    im = s.get("implementation") or {}
    comp = str(im.get("component") or "")
    route = str(im.get("route") or "")
    out = []
    if not comp:
        return out
    owners = comp_owner.get((im.get("app"), comp), [])
    # A section of another screen renders inside its host's component (`implementation.sectionOf`,
    # CHG-MOV-002): sharing with the host, or with the host's other sections, is the design.
    host = im.get("sectionOf") or sid
    hosted = all(o == host or ((pk.screens.get(o) or {}).get("implementation") or {})
                 .get("sectionOf") == host for o in owners)
    if im.get("sectionOf"):
        if host not in owners:
            out.append(("P7b", sid, f"a section of {host}, which does not render in "
                                    f"{comp.rsplit('/', 1)[-1]}"))
        return out
    if len(owners) > 1 and not hosted:
        out.append(("P7b", sid, f"component {comp.rsplit('/', 1)[-1]} is also "
                                f"{', '.join(o for o in owners if o != sid)}'s"))
    stem = comp.rsplit("/", 1)[-1].split(".")[0]
    name = _words(str(s.get("name")))
    if not _overlap(_words(stem), name):
        out.append(("P7b", sid, f"component {stem} does not name '{s.get('name')}'"))
    if route and not _overlap(route_words(route, sid), name):
        out.append(("P7b", sid, f"route {route} does not name '{s.get('name')}'"))
    return out


def component_owners(screens: dict) -> dict:
    out = defaultdict(list)
    for sid, s in screens.items():
        im = s.get("implementation") or {}
        if im.get("component"):
            out[(im.get("app"), im["component"])].append(sid)
    return out


# ── P8: a Block A screen that says it is not in the first release ───────────────────────────────

STALE = re.compile(r"\b(wave\s*[2-9]|out of (the )?first release|not in (the )?first release|"
                   r"outside (the )?first release|on hold|later wave|"
                   r"deferred to (wave|phase|block) ?\w*|post-launch|phase 2)\b", re.I)
STALE_KEYS = ("notes", "purpose", "purposeNote", "apisNote", "gaps", "openQuestions",
              "patternReason", "wireframe", "implementation", "states", "layout", "navigation")
# A path through the client prototype's own menu, whose groups are named "Wave 2" and "Wave 3":
# a pointer to where the client drew the screen, not a statement about the plan.
PROTOTYPE_PATH = re.compile(r"All screens → (Wave \d)")


def p8(pk: Package, sid: str, s: dict, block_a: set, exempt: dict) -> list:
    if sid not in block_a:
        return []
    out = []
    if str(s.get("wave")) != "1":
        out.append(("P8", sid, f"a Block A screen with wave {s.get('wave')} (Block A is wave 1)"))
    if s.get("deferred"):
        out.append(("P8", sid, "a Block A screen with a deferred block"))
    for k in STALE_KEYS:
        if k not in s:
            continue
        t = json.dumps(s[k], ensure_ascii=False, default=str)
        for m in STALE.finditer(t):
            if PROTOTYPE_PATH.search(t[max(0, m.start() - 16):m.end()]):
                continue
            ctx = t[max(0, m.start() - 50):m.end() + 30]
            if any(e in ctx for e in exempt.get(sid, ())):
                continue
            out.append(("P8", sid, f"{k} says '{m.group(0)}': …{ctx}…"))
            break
    return out


# ── G3 (READ): a screen that shows or edits data but binds no read that returns it ──────────────
#
# **Found by the r1 gate on 3 October** (CHG-R1S-004): ADM-069 edits a tax profile with a PUT and
# nothing on the screen reads one back; POS-024's "86 an item" picker had no operation returning the
# outlet's menu; GST-077 never read the departure it was opened on. A developer handed such a screen
# builds a form that opens empty and overwrites what was saved. Two rules:
#
#   READ  no-read    the screen has a loading state (every screen does) or a data pattern, and binds
#                    no read at all (a GET, or a POST the lineage says writes nothing)
#   READ  edit       the screen binds a PUT or PATCH (it edits existing data) and no bound read returns
#                    that data: the write's response schema by name, or a table the write stores to
#
# A read covers a table when its response schemas persist to it, when a projection names it
# (`none — projection of fnb.menu_item`), or when its lineage entry reads it.

READ_PATTERNS = {"listDetail", "configEditor", "statusTracker", "commandCentre", "approvalInbox",
                 "detail", "dashboard"}
_TABLE = re.compile(r"\b([a-z][a-z0-9_]*\.[a-z][a-z0-9_]*)\b")
_LINEAGE: dict | None = None


def _lineage(pk: Package) -> dict:
    global _LINEAGE
    if _LINEAGE is None:
        p = os.path.join(pk.root, "handoff", "api-data-lineage.json")
        _LINEAGE = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return _LINEAGE


def _schema_tables(pk: Package, name: str, projections: bool) -> set:
    _, node = pk.schema(name)
    c = next((c for c in pk.contracts if name in (((pk.contracts[c].get("components") or {})
                                                   .get("schemas") or {}))), None)
    raw = ((((pk.contracts.get(c) or {}).get("components") or {}).get("schemas") or {}).get(name)
           or {}) if c else {}
    p = str(raw.get("x-ticvai-persistence") or "").strip("\"'")
    if not p:
        return set()
    if p.lower().startswith("none"):
        return set(_TABLE.findall(p)) if projections else set()
    return {t.strip() for t in re.split(r"\s*\+\s*", p) if _TABLE.fullmatch(t.strip())}


def _resp_schemas(pk: Package, op_id: str, deep: bool) -> set:
    o = pk.ops.get(op_id) or {}
    out: set = set()

    def walk(c, node, depth):
        if depth > (4 if deep else 1) or not isinstance(node, dict):
            return
        if "$ref" in node:
            n = node["$ref"].rsplit("/", 1)[-1]
            if "/schemas/" in node["$ref"] and n not in out:
                out.add(n)
                c2, tgt = pk.deref(c, node)
                if deep:
                    walk(c2, tgt, depth + 1)
            return
        for k in ("allOf", "oneOf", "anyOf"):
            for sub in node.get(k) or []:
                walk(c, sub, depth + (1 if deep else 0))
        if isinstance(node.get("items"), dict):
            walk(c, node["items"], depth)
        for v in (node.get("properties") or {}).values():
            if deep:
                walk(c, v, depth + 1)
            elif isinstance(v, dict) and isinstance(v.get("items"), dict):
                walk(c, v["items"], depth)

    for code, r in (o.get("responses") or {}).items():
        if not str(code).startswith("2"):
            continue
        c, r = pk.deref(o.get("_contract"), r)
        for media in ((r or {}).get("content") or {}).values():
            if isinstance(media, dict) and media.get("schema"):
                walk(c, media["schema"], 0)
        if not deep:
            break
    return out


def is_read(pk: Package, op_id: str) -> bool:
    o = pk.ops.get(op_id)
    if not o:
        return False
    if o["_method"] == "get":
        return True
    e = _lineage(pk).get(op_id) or {}
    real = [w for w in e.get("writes") or [] if ":" not in w]
    return o["_method"] == "post" and not real and bool(e.get("reads"))


def read_covers(pk: Package, op_id: str):
    names = _resp_schemas(pk, op_id, deep=True)
    tabs = set()
    for n in names:
        tabs |= _schema_tables(pk, n, projections=True)
    tabs |= {t for t in (_lineage(pk).get(op_id) or {}).get("reads") or [] if ":" not in t}
    return names, tabs


def write_targets(pk: Package, op_id: str):
    names = _resp_schemas(pk, op_id, deep=False)
    tabs = set()
    for n in names:
        tabs |= _schema_tables(pk, n, projections=False)
    tabs |= {t for t in (_lineage(pk).get(op_id) or {}).get("writes") or []
             if ":" not in t and t not in ("platform.outbox", "platform.idempotency_record")}
    return names, tabs


def p_read(pk: Package, sid: str, s: dict) -> list:
    bound = [a["operationId"] for a in apis(s) if a["operationId"] in pk.ops]
    reads = [o for o in bound if is_read(pk, o)]
    shows = bool((s.get("states") or {}).get("loading")) or s.get("pattern") in READ_PATTERNS
    if shows and not reads:
        return [("READ", sid, "no-read: the screen shows data (a loading state) and binds no read")]
    cn, ct = set(), set()
    for o in reads:
        n, t = read_covers(pk, o)
        cn |= n
        ct |= t
    out = []
    for o in bound:
        if pk.ops[o]["_method"] not in ("put", "patch"):
            continue
        n, t = write_targets(pk, o)
        if (not n and not t) or n & cn or t & ct:
            continue
        out.append(("READ", sid, f"edit: {o} edits {', '.join(sorted(n)) or '-'} "
                                 f"({', '.join(sorted(t)) or '-'}) and no bound read returns it"))
    return out
