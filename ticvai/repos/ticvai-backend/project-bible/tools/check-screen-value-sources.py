#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every value a screen shows, offers or saves comes from an operation the screen declares (r10, CHG-R10GEN-003).

**What it found.** Between 21 and 24 October 2026 five change requests were raised on screens that every build had
passed, because each named a value that none of its declared operations (`apis`) carries, or a save it never calls:

  * GST-051 Plan (ADAM CR-220): the lunch and shop questions offer `VenuePoint.cuisineTags` and the shops'
    `retailTags`, but the screen's one load read (getVisitPlannerOptions) answers interest tags only, and the plan
    (generateVisitPlan) reports what it could not match only after it is made;
  * WEB-003 Search Results (CR-221): the suggestion cards show `Product.media`, whose `ProductMedia` holds an asset id
    and no address, and no declared operation turns the id into one;
  * WEB-023 Membership Management (CR-233): the retry form sends the `paymentTokenId` of another saved card, and
    nothing the screen declares lists the guest's saved cards;
  * WEB-007 Interactive Seat Selection (CR-187): the banner counts down to `Cart.expiresAt` and the seat cap is
    `VenueSettings.seating.maxSeatsPerGuestOrder`, and the screen reads neither a cart nor the venue settings;
  * GST-043 Arabic / RTL Experience (CR-186): the language is saved "as the profile's language", and the screen
    declares only a public read.

check-bindings asks whether a bound schema exists, check-screen-wiring whether a declared operation is reached; none
asked whether the value is in the answer of an operation the screen declares. What a screen has, here: the answers
of its declared operations (every response body, refusals included, `$ref`s followed at every level), what they are
sent, and what the app shell preloads (`entryState.preloaded`). Rules:

    SV-SCHEMA    a component's binding (`bindsTo`, `columns`), an overlay's, or a `Schema.field` named in prose,
                 belongs to a schema the screen has nowhere; one finding per screen and schema, the fields listed.
                 A field of that name in the answer of the component's own `operation` (or in the request its own
                 write sends) is its source, whichever schema the binding names: check-bindings judges the name.
                 A bare name in a form's body that is a stored field of a schema the screen has nowhere counts too
                 (WEB-007's stepper "at most `maxSeatsPerGuestOrder`")
    SV-FIELD     the schema is answered, but has no such field and no declared answer carries one of that name
    SV-OPTIONS   a choice (selectField, multiSelect, ...) offers values the screen only sends: a field named in its
                 text is in a declared request and is a stored field of a schema, and no read the screen makes
                 before the choice (onLoad, background) answers a field of that name (CR-220). A path parameter is
                 the record the screen is on, not a choice
    SV-MEDIA     a shown field is a media reference (`x-ticvai-references: assets.media_asset`) whose schema has no
                 address (`url`, `href`, `src`), and no declared operation answers MediaAsset's url (CR-221)
    SV-PICK      a form sends a `...Id` field of the request it binds, named in its body, that the screen has
                 nowhere (answer, entry state, an edge, a path parameter), while the package has a read that lists
                 them to the app's audience (guest, partner, staff): the read exists and the screen does not
                 declare it (CR-233). Context ids (venueId, subjectId, deviceId, ...) are never picked
    SV-WRITE     a component's notes say a value is stored, saved or written as or to the user's profile or
                 account, and the screen declares no operation that writes (CR-186)

**Precision first.** Prose is a weak signal, so a `Schema.field` in notes, states, entry params or a form's body
counts only when (a) the component has no operation of its own, or the form no confirm operation (otherwise the
sentence explains that operation's rule: "shown only when the sign-in comes back requiresMfa: the person holds a
permission in `PasswordPolicy.mfaRequiredForPermissions`"); (b) it is not inside parentheses, which cite the rule
a sentence states; and (c) it follows, within a few words, a word that shows or limits it ("One countdown:
`Cart.expiresAt`", "at most", "Shown only when", "lists", "offers"). A name the screen holds itself is never a gap:
an operationId, an enum value, a state, an entry or path parameter, what an edge carries in or a form discards, a
request's own schema. No baseline: every finding is a real gap for the lead's ruling or a fix. Keys are
`<screen>:<schema>` (SV-SCHEMA), `<screen>:<Schema.path>`, `<screen>:<overlay or control>:<field>`.

    python tools/check-screen-value-sources.py [--all] [--list]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "SV-SCHEMA": "a value a screen binds or shows belongs to a schema no declared operation answers or sends, and "
                 "the app shell does not preload it (CR-187)",
    "SV-FIELD": "the schema is answered, but the named field is in no declared answer",
    "SV-OPTIONS": "a choice offers stored values the screen only sends; no read before the choice answers them "
                  "(CR-220)",
    "SV-MEDIA": "a shown media reference holds an asset id and no address, and no declared operation answers one "
                "(CR-221)",
    "SV-PICK": "a form sends an id the user picks from a list the package has and the screen does not declare "
               "(CR-233)",
    "SV-WRITE": "the text saves a value to the user's record and the screen declares no write (CR-186)",
}
OK_STATUS = re.compile(r"^2\d\d$")
CHOICE = {"selectField", "multiSelect", "radioGroup", "chipGroup", "segmentedControl", "checkboxGroup", "chips",
          "filterChips", "toggleGroup", "combobox"}
REF_PATH = re.compile(r"`([A-Z][A-Za-z0-9]+)((?:\.[a-z][A-Za-z0-9]*(?:\[\])?)+)`")
BARE = re.compile(r"`([a-z][a-z0-9]*[A-Z][A-Za-z0-9]*)`")
URLISH = re.compile(r"(?i)(url|href|uri|src|address)$")
WRITE_SAID = re.compile(
    r"\b(?:stored|saved|written|kept|recorded)\b[^.;]{0,80}?\b(?:as|to|on|in)\s+(?:the|their|your|his|her)\s+"
    r"(?:guest'?s?\s+|user'?s?\s+|own\s+)?(?:profile|account)\b", re.I)
READS = {"get"}
BEFORE = {"onLoad", "background", "onEntry", "onFocus", "poll", "onOpen"}


# ----------------------------------------------------------------------------------------------- schema walking
def _ref_target(stem: str, ref: str):
    """(stem, name) of a `$ref` to a component schema, or None."""
    if "#/components/schemas/" not in ref:
        return None
    file, name = ref.split("#/components/schemas/", 1)
    s = Path(file).stem if file else stem
    return s, name


class Schemas:
    def __init__(self, by: dict, names: dict):
        self.by, self.names = by, names
        self._closure: dict = {}

    def find(self, name: str, prefer=()):
        for s in list(prefer) + list(self.names.get(name) or []):
            if (s, name) in self.by:
                return s, self.by[(s, name)]
        return None

    def props(self, stem: str, node, depth: int = 0) -> dict:
        """field -> (stem, node) of an object node: `$ref`, allOf, oneOf, anyOf merged; an array's items."""
        out: dict = {}
        if depth > 12 or not isinstance(node, dict):
            return out
        if isinstance(node.get("$ref"), str):
            t = _ref_target(stem, node["$ref"])
            if t and t in self.by:
                return self.props(t[0], self.by[t], depth + 1)
            return out
        if node.get("type") == "array" or "items" in node and "properties" not in node:
            return self.props(stem, node.get("items"), depth + 1)
        for k in ("allOf", "oneOf", "anyOf"):
            for b in node.get(k) or []:
                out.update(self.props(stem, b, depth + 1))
        for pn, pv in (node.get("properties") or {}).items():
            out[str(pn)] = (stem, pv)
        ap = node.get("additionalProperties")
        if isinstance(ap, dict):
            out.update(self.props(stem, ap, depth + 1))
        return out

    def closure(self, stem: str, node) -> tuple:
        """(named schemas reached, field names reached) from a node, `$ref`s followed at every level."""
        names, fields, seen = set(), set(), set()

        def walk(st, n, d):
            if d > 40 or not isinstance(n, dict):
                return
            if isinstance(n.get("$ref"), str):
                t = _ref_target(st, n["$ref"])
                if t and t in self.by and t not in seen:
                    seen.add(t)
                    names.add(t[1])
                    walk(t[0], self.by[t], d + 1)
                return
            for k in ("allOf", "oneOf", "anyOf"):
                for b in n.get(k) or []:
                    walk(st, b, d + 1)
            if isinstance(n.get("items"), dict):
                walk(st, n["items"], d + 1)
            if isinstance(n.get("additionalProperties"), dict):
                walk(st, n["additionalProperties"], d + 1)
            for pn, pv in (n.get("properties") or {}).items():
                fields.add(str(pn))
                walk(st, pv, d + 1)

        walk(stem, node, 0)
        return names, fields

    def named_closure(self, name: str):
        if name not in self._closure:
            f = self.find(name)
            if not f:
                self._closure[name] = (set(), set())
            else:
                n, fl = self.closure(f[0], {"$ref": f"#/components/schemas/{name}"})
                n.add(name)
                self._closure[name] = (n, fl)
        return self._closure[name]

    def has_path(self, name: str, path: list) -> bool:
        f = self.find(name)
        if not f:
            return False
        stem, node = f
        for step in path:
            p = self.props(stem, node)
            if step not in p:
                return False
            stem, node = p[step]
        return True


def op_io(sch: Schemas, f: dict) -> tuple:
    """(response names, response fields, request names, request fields, refusal names, refusal fields) of an
    operation: its 2xx answers, what it is sent, and the bodies of its other answers (a refusal a screen shows)."""
    stem, op = f["contract"], f["op"]
    rn, rf, qn, qf, en, ef = set(), set(), set(), set(), set(), set()
    for code, r in (op.get("responses") or {}).items():
        if not isinstance(r, dict):
            continue
        ok = bool(OK_STATUS.match(str(code)))
        for c in (r.get("content") or {}).values():
            n, fl = sch.closure(stem, (c or {}).get("schema") or {})
            (rn if ok else en).update(n)
            (rf if ok else ef).update(fl)
    rb = op.get("requestBody") or {}
    for c in (rb.get("content") or {}).values() if isinstance(rb, dict) else []:
        n, fl = sch.closure(stem, (c or {}).get("schema") or {})
        qn |= n
        qf |= fl
    for p in list(op.get("parameters") or []) + list((f.get("item") or {}).get("parameters") or []):
        if isinstance(p, dict) and p.get("name"):
            qf.add(str(p["name"]))
    return rn, rf, qn, qf, en, ef


def media_without_address(sch: Schemas, name: str) -> bool:
    """A schema that references a media asset by id and carries no address of its own."""
    f = sch.find(name)
    if not f:
        return False
    props = sch.props(*f)
    refs = [k for k, (_s, v) in props.items() if isinstance(v, dict) and (
        str(v.get("x-ticvai-references") or "") == "assets.media_asset")]
    return bool(refs) and not any(URLISH.search(k) for k in props)


# ----------------------------------------------------------------------------------------------- screen reading
def _texts(node) -> list:
    out = []
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for v in node.values():
            out += _texts(v)
    elif isinstance(node, list):
        for v in node:
            out += _texts(v)
    return out


def components(screen: dict) -> list:
    out = []
    for r in ((screen.get("layout") or {}).get("regions") or []):
        for c in (r or {}).get("components") or []:
            if isinstance(c, dict):
                out.append(c)
    return out


def parse_binding(b: str):
    m = re.match(r"^([A-Z][A-Za-z0-9]*)(?:\[\])?((?:\.[A-Za-z][A-Za-z0-9]*(?:\[\])?)*)$", str(b or "").strip())
    if not m:
        return None
    return m.group(1), [p.replace("[]", "") for p in m.group(2).split(".") if p]


class Package:
    """The contracts and screens a run judges: the package's own, or the given ones (the tests)."""

    def __init__(self, contracts: list = None, screens: list = None):
        if contracts is None:
            by, names = g.schemas()
            ops = g.operations()
            contracts = g.contracts()
        else:
            by, names, ops = {}, {}, {}
            for stem, rel, doc in contracts:
                for n, sc in (((doc.get("components") or {}).get("schemas")) or {}).items():
                    if isinstance(sc, dict):
                        by[(stem, n)] = sc
                        names.setdefault(n, []).append(stem)
                for path, item in (doc.get("paths") or {}).items():
                    for m in g.VERBS:
                        op = (item or {}).get(m)
                        if isinstance(op, dict) and op.get("operationId"):
                            ops[op["operationId"]] = {"contract": stem, "file": rel, "method": m, "path": path,
                                                      "op": op, "item": item}
        self.screen_list = g.screens() if screens is None else screens
        self.sch = Schemas(by, names)
        self.ops = ops
        self.io = {}
        self.enums, self.all_fields = set(), set()
        self.field_owner: dict = {}
        for (stem, name), s in by.items():
            stored = bool(s.get("x-ticvai-persistence"))
            todo = [(stem, s, 0)]
            while todo:   # the schema's own fields, and those of objects written inline in it (VenueSettings.seating)
                st, node, d = todo.pop()
                for k, (_st, v) in self.sch.props(st, node).items():
                    self.all_fields.add(k)
                    if isinstance(v, dict) and (v.get("x-ticvai-stored-as") or stored):
                        self.field_owner.setdefault(k, set()).add(name)
                    if d < 3 and isinstance(v, dict) and "$ref" not in v and v.get("properties"):
                        todo.append((st, v, d + 1))
        for stem, rel, doc in contracts:
            for t in _texts_enums(doc):
                self.enums.add(t)
        self.screens = {s["id"]: s for _p, s in self.screen_list}

    def op(self, o):
        if o not in self.io:
            self.io[o] = op_io(self.sch, self.ops[o]) if o in self.ops else (set(),) * 6
        return self.io[o]


def _texts_enums(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "enum" and isinstance(v, list):
                for x in v:
                    if isinstance(x, str):
                        yield x
            else:
                yield from _texts_enums(v)
    elif isinstance(node, list):
        for x in node:
            yield from _texts_enums(x)


# In prose, a value named right after one of these words is one the screen shows or works with ("One countdown:
# `Cart.expiresAt`", "at most `maxSeatsPerGuestOrder`", "Shown only when `BookingFlowConfig.quickTour` is on"); a name
# in any other sentence explains a rule the server keeps ("the denied state counts against `PasswordPolicy...`").
SHOWN_BEFORE = re.compile(r"(?i)\b(?:shown?|shows|displays?|displayed|countdown|counts? down|at most|up to|no more "
                          r"than|lists?|listed|offers?|options?|choices|capped)\b[^`.;]{0,24}$")


def shown(text: str, at: int) -> bool:
    """True when the name at `at` follows, within a few words, a word that shows or limits it on the screen."""
    return bool(SHOWN_BEFORE.search(text[max(0, at - 40):at]))


def in_parens(text: str, at: int) -> bool:
    """True when position `at` of `text` sits inside an unclosed parenthesis."""
    depth = 0
    for ch in text[:at]:
        if ch == "(":
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
    return depth > 0


# Ids a screen holds from its context (the session, the device, the app shell), never picked from a list.
CONTEXT_IDS = {"venueId", "subjectId", "principalId", "tenantId", "deviceId", "workstationId", "regionId",
               "outletId", "sessionId", "scopeId"}
GUEST_APPS, PARTNER_APPS = ("P01", "P02", "P05"), ("P10",)


def audience_of(platform: str) -> set:
    if platform.startswith(GUEST_APPS):
        return {"guest"}
    if platform.startswith(PARTNER_APPS):
        return {"partner"}
    if platform.startswith("P11"):
        return {"guest", "partner", "staff"}
    return {"staff"}


def list_ops(pk, name: str, audience: set) -> list:
    """The reads of the package that answer a list of `name` to this audience (operation ids, sorted)."""
    out = []
    for o, f in pk.ops.items():
        if f["method"] != "get" or "{" in f["path"].rsplit("/", 1)[-1]:
            continue
        aud = set(f["op"].get("x-ticvai-audience") or ["staff"])
        if not aud & audience:
            continue
        for code, r in (f["op"].get("responses") or {}).items():
            if OK_STATUS.match(str(code)) and isinstance(r, dict):
                for c in (r.get("content") or {}).values():
                    sc = (c or {}).get("schema") or {}
                    txt = repr(sc)
                    if (f"schemas/{name}'" in txt) and ("'items'" in txt or "array" in txt):
                        out.append(o)
    return sorted(set(out))


# ----------------------------------------------------------------------------------------------- the judgement
def screen_findings(pk: Package, screen: dict, platform: str = "") -> list:
    """[(rule, key, message)] for one screen of the app `platform` (the screens file's stem)."""
    sid = screen["id"]
    out = []
    apis = [a for a in screen.get("apis") or [] if isinstance(a, dict) and a.get("operationId")]
    rn, rf, qn, qf = set(), set(), set(), set()
    before_f = set()
    writes = False
    for a in apis:
        o = a["operationId"]
        a_rn, a_rf, a_qn, a_qf, a_en, a_ef = pk.op(o)
        rn |= a_rn | a_en
        rf |= a_rf | a_ef
        qn |= a_qn
        qf |= a_qf
        if str(a.get("trigger") or "") in BEFORE or (o in pk.ops and pk.ops[o]["method"] in READS
                                                      and str(a.get("trigger") or "") != "onAction"):
            before_f |= a_rf
        if o in pk.ops and pk.ops[o]["method"] not in READS:
            writes = True
    es = screen.get("entryState") or {}
    held = {str(p.get("name")) for p in es.get("params") or [] if isinstance(p, dict)}
    # a path parameter of a declared operation is the record the screen is on, not a value offered to choose
    path_params: set = set()
    for a in apis:
        f = pk.ops.get(a["operationId"])
        if f:
            path_params |= {str(p.get("name")) for p in list(f["op"].get("parameters") or [])
                     + list((f.get("item") or {}).get("parameters") or []) if isinstance(p, dict)
                     and p.get("in") == "path"}
    for pre in es.get("preloaded") or []:
        m = re.match(r"\s*([A-Z][A-Za-z0-9]+)", str(pre))
        if m and pk.sch.find(m.group(1)):
            n, fl = pk.sch.named_closure(m.group(1))
            rn |= n
            rf |= fl
            before_f |= fl
        m2 = re.match(r"\s*[A-Z][A-Za-z0-9]+\.([a-z][A-Za-z0-9]*)", str(pre))
        if m2:
            held.add(m2.group(1))
    nav = screen.get("navigation") or {}
    for t in nav.get("transitions") or []:
        held |= {str(x) for x in (t or {}).get("carries") or []}
    for s2 in pk.screens.values():  # what an edge into this screen carries
        for t in ((s2.get("navigation") or {}).get("transitions") or []):
            if isinstance(t, dict) and t.get("to") == sid:
                held |= {str(x) for x in t.get("carries") or []}
    overlays = [o for o in screen.get("overlays") or [] if isinstance(o, dict)]
    for ov in overlays:
        held |= {str(x) for x in ((ov.get("dismiss") or {}).get("discards") or [])}
        held |= {str(x) for x in ((ov.get("confirm") or {}).get("carries") or [])}
    states = set((screen.get("states") or {}).keys())
    skip_bare = held | states | pk.enums | set(pk.ops) | {c.get("kind") for c in components(screen)}

    def answered(name: str) -> bool:
        return name in rn

    unanswered: dict = {}

    def judge_ref(where: str, name: str, path: list, how: str, own_op=None):
        """A `Schema.field...` or a binding. `own_op`: the operation the component itself names; a field of that
        name in its answer is the value's source, whichever schema the binding names (check-bindings judges that)."""
        if not pk.sch.find(name) or name in qn:
            return
        last = path[-1] if path else None
        if own_op and own_op in pk.ops:
            o_rn, o_rf, _qn, o_qf, o_en, o_ef = pk.op(own_op)
            # an input bound to a field its own write sends is the value the user enters
            sent = o_qf if pk.ops[own_op]["method"] not in READS else set()
            if (last and last in o_rf | o_ef | sent) or (not last and (o_rn or o_rf)):
                return
        if answered(name):
            if path and not pk.sch.has_path(name, path):
                out.append(("SV-FIELD", f"{sid}:{name}.{'.'.join(path)}",
                            f"{sid} {where} names {name}.{'.'.join(path)} ({how}); {name} is answered, but has no "
                            f"such field and no declared answer carries {last!r}"))
            return
        if not path and name in held:
            return
        # one finding per screen and schema: the fix (declare the read, or rebind) is one decision
        unanswered.setdefault(name, {"where": [], "fields": []})
        if where not in unanswered[name]["where"]:
            unanswered[name]["where"].append(where)
        if path and ".".join(path) not in unanswered[name]["fields"]:
            unanswered[name]["fields"].append(".".join(path))

    def judge_media(where: str, name: str, path: list):
        f = pk.sch.find(name)
        if not f or not path or not pk.sch.has_path(name, path):
            return
        stem, node = f
        for step in path:
            stem, node = pk.sch.props(stem, node)[step]
        tgt = None
        n = node.get("items") if isinstance(node, dict) and isinstance(node.get("items"), dict) else node
        if isinstance(n, dict) and isinstance(n.get("$ref"), str):
            t = _ref_target(stem, n["$ref"])
            tgt = t[1] if t else None
        if tgt and media_without_address(pk.sch, tgt) and not ({"url", "thumbnailUrl"} & rf and "MediaAsset" in rn):
            out.append(("SV-MEDIA", f"{sid}:{name}.{'.'.join(path)}",
                        f"{sid} {where} shows {name}.{'.'.join(path)}, a {tgt} that holds an asset id and no "
                        f"address, and no operation the screen declares answers the asset's url: the client holds an "
                        f"id it cannot render (add the address to the answer, or declare a read that gives it)"))

    def refs_in(text: str, prose: bool = True):
        """`Schema.field` names in a text. In prose, a name inside parentheses is a citation of the rule the
        sentence states (`the limit is set per country (`RegionSettings.minorAgeThreshold`)`), not a value shown."""
        for m in REF_PATH.finditer(text or ""):
            if prose and (in_parens(text, m.start()) or not shown(text, m.start())):
                continue
            yield m.group(1), [p.replace("[]", "") for p in m.group(2).split(".") if p]

    # 1. components: bindings, columns, notes
    for i, c in enumerate(components(screen)):
        label = c.get("label") or c.get("kind")
        where = f"component {label!r}"
        b = parse_binding(c.get("bindsTo")) if c.get("bindsTo") else None
        if b:
            judge_ref(where, b[0], b[1], "bindsTo", c.get("operation"))
            if b[1]:
                judge_media(where, b[0], b[1])
        for col in c.get("columns") or []:
            pb = parse_binding(col) if "." in str(col) else None   # a bare label ('Product') is a heading
            if pb:
                judge_ref(where, pb[0], pb[1], "column", c.get("operation"))
                if pb[1]:
                    judge_media(where, pb[0], pb[1])
        text = " ".join(str(c.get(k) or "") for k in ("label", "notes"))
        # a component that calls an operation explains that operation's rule in its notes ("shown only when the
        # sign-in comes back requiresMfa: the person holds a permission in `PasswordPolicy...`"); only the notes of
        # a component with no operation of its own name a value it must show (WEB-007's countdown, CR-187)
        for name, path in ([] if c.get("operation") else refs_in(text)):
            judge_ref(where, name, path, "its notes")
        if c.get("kind") in CHOICE and not c.get("bindsTo"):
            named = [p[-1] for _n, p in refs_in(text, prose=False)] + [m.group(1) for m in BARE.finditer(text)]
            for fld in dict.fromkeys(named):
                if fld in skip_bare - qf or fld in before_f or fld in path_params:
                    continue
                stored = pk.field_owner.get(fld)
                if fld in qf and stored:
                    out.append(("SV-OPTIONS", f"{sid}:{label}:{fld}",
                                f"{sid} {where} offers {fld} (a stored field of {', '.join(sorted(stored)[:3])}), "
                                f"which the screen sends, but no read it makes before the choice (onLoad) answers "
                                f"{fld}: the choices have no source until the action that takes them"))
    # 2. states, entry state, overlays: `Schema.field`
    for st, txt in (screen.get("states") or {}).items():
        for name, path in refs_in(str(txt)):
            judge_ref(f"state {st!r}", name, path, "its text")
    for p in es.get("params") or []:
        if isinstance(p, dict):
            for name, path in refs_in(str(p.get("notes") or "")):
                judge_ref(f"entry param {p.get('name')!r}", name, path, "its notes")
    for ov in overlays:
        where = f"overlay {ov.get('id')!r}"
        body = str(ov.get("body") or "")
        for name, path in ([] if (ov.get("confirm") or {}).get("operation") else refs_in(body)):
            judge_ref(where, name, path, "its body")
        bind = parse_binding(ov.get("bindsTo")) if ov.get("bindsTo") else None
        if bind and not bind[1]:
            judge_ref(where, bind[0], [], "bindsTo")
        # a form's bare names: a field of the form's own schema is what it collects; an id the user must pick
        # from a list needs the list
        own = set(pk.sch.props(*pk.sch.find(bind[0]))) if bind and pk.sch.find(bind[0]) else set()
        discards = {str(x) for x in ((ov.get("dismiss") or {}).get("discards") or [])}
        for m in BARE.finditer(body):
            fld = m.group(1)
            if fld in own and fld.endswith("Id") and fld not in CONTEXT_IDS and fld not in held - discards                     and fld not in rf:
                x = fld[0].upper() + fld[1:-2]
                if x in rn or not pk.sch.find(x):
                    continue
                lists = list_ops(pk, x, audience_of(platform))
                if not lists:
                    continue
                out.append(("SV-PICK", f"{sid}:{ov.get('id')}:{fld}",
                            f"{sid} {where} sends {bind[0]}.{fld}, a {x} the user chooses, but no operation the "
                            f"screen declares lists one, the entry state does not carry it and no edge brings it: "
                            f"declare {' or '.join(lists[:3])} (the read that lists them)"))
            elif fld in skip_bare or fld in own or not shown(body, m.start()):
                continue
            elif fld not in qf and fld not in rf and pk.field_owner.get(fld):
                owners = sorted(pk.field_owner[fld])
                if any(answered(o) for o in owners):
                    continue
                out.append(("SV-SCHEMA", f"{sid}:{ov.get('id')}:{fld}",
                            f"{sid} {where} uses {fld!r} (a field of {', '.join(owners[:3])}), which no operation "
                            f"the screen declares answers or sends and the app shell does not preload"))
    # 3. a save the text promises, with no write declared
    if not writes:
        for i, c in enumerate(components(screen)):
            m = WRITE_SAID.search(str(c.get("notes") or ""))
            if m:
                out.append(("SV-WRITE", f"{sid}:{c.get('label') or c.get('kind')}",
                            f"{sid} component {c.get('label') or c.get('kind')!r} says the value is "
                            f"{m.group(0)!r}, and the screen declares no operation that writes: declare the write "
                            f"(the operation the other screen uses), or say the value stays on the device"))
    for name, u in unanswered.items():
        fl = u["fields"]
        out.insert(0, ("SV-SCHEMA", f"{sid}:{name}",
                       f"{sid} names {name}" + (f" ({', '.join(fl[:6])}{' ...' if len(fl) > 6 else ''})" if fl else "")
                       + f" in {', '.join(u['where'][:3])}{' ...' if len(u['where']) > 3 else ''}; no operation the "
                       f"screen declares answers {name} and the app shell does not preload it: declare the read that "
                       "returns it, or bind the field of an answer the screen already reads"))
    # one finding per key
    seen, uniq = set(), []
    for r, k, msg in out:
        if k not in seen:
            seen.add(k)
            uniq.append((r, k, msg))
    return uniq


def merged_into(screen: dict):
    """The screen this one was merged into, or None (CHG-MOV-002, 2 October 2026; CHG-R10UI-016). A merged screen gets no
    build task: its target's ticket builds it and declares the reads (ticket_done.screen_hold, the test
    check-binding-ratchet's not-built screens use), so its values are judged on the target, never on the merged id."""
    from ticket_done import MERGED_NOTE
    m = MERGED_NOTE.search(str(screen.get("notes") or ""))
    return m.group(1) if m else None


def findings(pk: Package = None) -> list:
    """[(rule, key, message)] over every screen that is built: a screen merged into another is skipped."""
    pk = pk or Package()
    out = []
    for p, s in pk.screen_list:
        if merged_into(s):
            continue
        out += screen_findings(pk, s, p)
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-screen-value-sources", RULES)
    rows = findings()
    if "--list" in sys.argv[1:]:
        for r, k, m in rows:
            print(f"{r}\t{k}\t{m}")
        return 0
    for r, k, m in rows:
        guard.add(r, k, m)
    guard.note(f"{len(rows)} value(s) with no source on {len({k.split(':')[0] for _r, k, _m in rows})} screen(s)")
    if rows:
        guard.note("no mechanical fixer (CHG-R10GEN-006): each fix adds to the screen's `apis` the operation that "
                   "answers the value, wired to the component that shows it, or rebinds it to an answer the screen "
                   "already declares; the screen generators keep generated screens to their declared answers "
                   "(contract_shapes.drop_unsourced, CHG-R10GEN-007)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
