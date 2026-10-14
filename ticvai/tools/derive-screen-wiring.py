#!/usr/bin/env python3
"""Derive the invisible wiring of every screen from its operations: the Block A audit's generator rules (14 October 2026).

**The screens' UI is fixed and approved by the client** (Chinmay, 14 October 2026). This deriver never adds, removes,
moves or relabels a visible component, region title, overlay or screen, and never changes copy a person reads. It
writes only what is invisible and follows from the operations a screen declares: the permission the screen is gated
on, which declared operation a control binds to, an api's `purpose`, internal region ids, and the design notes of the
rendering states where a generator's note promises something the approved screen does not have. A member it cannot
fix without a visible change is left as it is and reported as a keep ("client-approved UI").

The rules, one per audit class (`tools/check-screen-wiring.py`; evidence `audit/ticvai/runs/audit-1014/classes.json`;
change entries CHG-SCR-nnn):

  S-STATE-BOILERPLATE   The pack generator (9 September) wrote "Carries the create action", "The filter narrowed
                        it" and "Names the missing permission" on every screen, whatever it had. They are design
                        notes, not copy. Where the screen has no create operation and no visible create control, or no
                        filter, the note says what the screen has. A visible create control with nothing behind it is
                        the UI's promise and is reported, not rewritten.
  S-SCREEN-PERMISSION   A staff screen whose operations need a permission declares the one its load needs
                        (`generate-screens-from-contracts.py::screen_permission`: the read it loads with first, then
                        any read, then its writes), or the one its no-access state already names. Guest surfaces
                        declare none (ADR-0025, CHG-CLN-007).

**On the refresh, among the screen derivers** (after `derive-components`). Fills and corrects only what a generator
wrote, so a person's note or permission survives; idempotent, a second run writes nothing. Files are written as the
other screen derivers write them (PyYAML `safe_dump`, width 100), in the checkout's line endings: every screen file
round-trips byte for byte, so the diff is the change and nothing else.

    python tools/derive-screen-wiring.py [--only S-STATE-BOILERPLATE,...] [--platform P08] [--apply] [--verbose]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
SCREENS = ROOT / "screens"
sys.path.insert(0, str(TOOLS))

_spec = importlib.util.spec_from_file_location("gen_contract_screens", TOOLS / "generate-screens-from-contracts.py")
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
LF, CRLF = chr(10), chr(13) + chr(10)

# The check's own vocabulary (tools/check-screen-wiring.py), so a fix means what the check means.
FILTERS = {"searchField", "selectField", "multiSelect", "datePicker", "toggle"}
CREATE_LIKE = re.compile(r"^(create|add|register|issue|open|start|submit|raise|record|enrol|invite|"
                         r"import|upload|book|reserve|request|schedule|draft|new|clone|copy|"
                         r"generate|publish|assign|allocate|log)", re.I)
WRITES = ("post", "put", "patch", "delete")
GUEST_CODES = ("P01", "P02", "P05")


# ── the package ─────────────────────────────────────────────────────────────────────────────────

def load_ops() -> dict:
    """operationId -> {contract, file, method, path, op}."""
    out = {}
    for f in sorted((ROOT / "contracts").glob("*/*.yaml")):
        text = f.read_text(encoding="utf-8")
        try:
            doc = yaml.load(text, Loader=LOADER) or {}
        except Exception:  # noqa: BLE001
            doc = yaml.safe_load(text) or {}
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for m in ("get", "post", "put", "patch", "delete"):
                op = item.get(m)
                if isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = {"contract": f.stem, "file": f.relative_to(ROOT).as_posix(),
                                              "method": m, "path": path, "op": op}
    return out


def comps(s: dict):
    for r in ((s.get("layout") or {}).get("regions") or []):
        for c in (r.get("components") or []):
            if isinstance(c, dict):
                yield r, c


def apis(s: dict) -> list:
    return [a for a in (s.get("apis") or []) if isinstance(a, dict) and a.get("operationId")]


def put_after(s: dict, key: str, value, after: tuple) -> None:
    """Set `key` on the screen, placed after the first of `after` it has (the order people read the record in)."""
    if key in s:
        s[key] = value
        return
    anchor = next((k for k in after if k in s), None)
    items = list(s.items())
    s.clear()
    placed = False
    for k, v in items:
        s[k] = v
        if k == anchor and not placed:
            s[key] = value
            placed = True
    if not placed:
        s[key] = value


# ── S-STATE-BOILERPLATE ─────────────────────────────────────────────────────────────────────────

FIRST_RUN = re.compile(r"^No (?P<noun>.{1,80}?) (?P<cfg>yet|configured yet)\. Carries the create action"
                       r"(; distinct from a filter that matched nothing| and says what the platform does in "
                       r"the meantime)\.$")
NO_RESULTS = re.compile(r"^The filter narrowed it and the (?P<noun>.{1,80}?) are still there\. ")
NO_ACCESS = "Names the missing permission. **Never an empty table**"
NO_ACCESS_NONE = ("No operation on this screen requires a permission, so no permission can be missing: the state is "
                  "reached only by a caller who is not signed in, or a tenant without the screen's module, and says "
                  "which. **Never an empty table** — that reads as *there is no data* and sends somebody to support "
                  "with the wrong question.")
CREATE_BUTTON = re.compile(r"^\s*(\+\s*)?(create|add|new|register|issue|raise|record|submit|book|enrol|invite|"
                           r"upload|import)\b", re.I)


def first_run_note(noun: str, configured: bool, writer: str | None) -> str:
    """The first-run note of a screen that creates nothing (shared with `generate-screens-from-pack.py`)."""
    if configured:
        return (f"No {noun} configured. `{writer}` saves the first one; the state says what the platform does in the "
                f"meantime." if writer else f"No {noun} configured, and this screen declares nothing that saves one.")
    return (f"No {noun} yet. **Offers no create action** — this screen declares no operation that makes one — and "
            f"says so rather than showing an empty table.")


def no_results_note(lister: str | None) -> str:
    """The no-results note of a screen with no filter (shared with `generate-screens-from-pack.py`)."""
    if lister:
        return f"Never shown: this screen offers no filter, so an empty `{lister}` is always the first-run state above."
    return "Never shown: this screen has no list or filter to narrow, so nothing it shows can be filtered to empty."


def fix_states(s: dict, ops: dict, log: list, keeps: list, **_) -> None:
    sid = s["id"]
    states = s.get("states") or {}
    facts = {a["operationId"]: ops.get(a["operationId"]) for a in apis(s)}
    kinds = {c.get("kind") for _, c in comps(s)}
    creates = [o for o, f in facts.items() if f and f["method"] == "post" and CREATE_LIKE.match(o)]
    m = FIRST_RUN.match(str(states.get("emptyFirstRun") or ""))
    if m and not creates:
        visible = [c.get("label") for _, c in comps(s)
                   if "Button" in str(c.get("kind")) and CREATE_BUTTON.match(str(c.get("label") or ""))]
        if visible:
            keeps.append((sid, "S-STATE-BOILERPLATE", f"emptyFirstRun: the approved screen shows {visible[0]!r} and no "
                          f"operation on it creates; the note is the UI's promise (client-approved UI)"))
        else:
            writer = next((o for o, f in facts.items() if f and f["method"] in ("put", "patch", "post")), None)
            states["emptyFirstRun"] = first_run_note(
                m.group("noun"), m.group("cfg") == "configured yet" or s.get("pattern") == "configEditor", writer)
            log.append(f"{sid}: emptyFirstRun names no create action")
    perms = [f["op"].get("x-ticvai-permission") for f in facts.values() if f and f["op"].get("x-ticvai-permission")]
    if str(states.get("emptyNoAccess") or "").startswith(NO_ACCESS) and not perms:
        states["emptyNoAccess"] = NO_ACCESS_NONE
        log.append(f"{sid}: emptyNoAccess names no permission")
    elif states.get("emptyNoAccess") == NO_ACCESS_NONE and perms:
        # Its own note, gone stale: an operation now needs a permission, so the state names it.
        known = [o for o, f in facts.items() if f]
        new = G.no_access_state(ops, known, {a["operationId"] for a in apis(s) if a.get("trigger") == "onLoad"})
        if new:
            states["emptyNoAccess"] = new
            log.append(f"{sid}: emptyNoAccess names the permission its operations now need")
    if NO_RESULTS.match(str(states.get("emptyNoResults") or "")) and not (kinds & FILTERS):
        lister = next((o for o, f in facts.items() if f and f["method"] == "get" and o.startswith(("list", "search"))),
                      None)
        states["emptyNoResults"] = no_results_note(lister)
        log.append(f"{sid}: emptyNoResults names no filter")


# ── S-SCREEN-PERMISSION ─────────────────────────────────────────────────────────────────────────

def fix_permission(s: dict, ops: dict, log: list, keeps: list, platform: dict | None = None, **_) -> None:
    code = str((platform or {}).get("code") or "")
    if s.get("permission") or code.startswith(GUEST_CODES):
        return
    known = [a["operationId"] for a in apis(s) if a["operationId"] in ops]
    perms = {ops[o]["op"].get("x-ticvai-permission") for o in known}
    perms = {p for p in perms if isinstance(p, str) and p}
    if not perms:
        return
    named = [p for p in re.findall(r"`([A-Z][A-Z0-9_]+)`", str((s.get("states") or {}).get("emptyNoAccess") or ""))
             if p in perms]
    loads = {a["operationId"] for a in apis(s) if a.get("trigger") == "onLoad"}
    got = G.screen_permission(ops, known, loads)
    perm = named[0] if named else (got[0] if got else sorted(perms)[0])
    put_after(s, "permission", perm, ("wave", "requiresModule", "module", "name"))
    log.append(f"{s['id']}: permission {perm}")


# ── S-OP-UNREACHED ──────────────────────────────────────────────────────────────────────────────
# A declared operation no component, overlay or transition reaches. The control or panel that calls it is almost
# always on the screen already, unbound: a `derive-components` proposal that records the operation it was proposed
# for (`impliedBy`) but never said it calls it; a panel bound to the schema the read returns; a form whose fields
# are the write's body; a button labelled with the operation's verb and object; the one table or panel the screen
# has for the one read it loads. Each is bound (`operation`), which is invisible. A shell beacon that no person
# triggers runs in the background. What is left has no control on the approved screen and is reported as a keep.

SCHEMAS: dict = {}
DATA_KINDS = {"dataTable", "cardList", "timeline", "chart", "list", "detailPanel", "kpiRow", "seatMap", "calendar",
              "map", "board"}
LIST_KINDS = {"dataTable", "cardList", "timeline", "chart", "list", "kpiRow", "calendar", "map", "board", "seatMap"}
CHECK_INPUTS = FILTERS | {"textField", "numberField", "fileUpload", "consentBlock", "scanTarget"}
INPUT_KINDS = {"textField", "numberField", "selectField", "multiSelect", "datePicker", "toggle", "searchField",
               "fileUpload", "consentBlock", "scanTarget"}
BEACON = re.compile(r"^record\w*(Events|Beacon|Heartbeat)$|^(send|report)\w*Heartbeat$")
VERBS = {"set": {"save", "set", "update", "apply", "configure", "edit"},
         "update": {"save", "update", "edit", "apply", "change"},
         "create": {"create", "add", "new", "raise", "open"}, "add": {"add", "create", "new", "attach"},
         "delete": {"delete", "remove"}, "remove": {"remove", "delete", "unlink"},
         "decide": {"approve", "reject", "decide"}, "approve": {"approve", "accept"}, "reject": {"reject", "decline"},
         "export": {"export", "download"}, "simulate": {"simulate", "preview", "run", "test"},
         "validate": {"validate", "check", "test", "verify"}, "test": {"test", "check", "run"},
         "publish": {"publish", "activate", "go"}, "relinquish": {"release"}, "revoke": {"revoke", "remove"},
         "cancel": {"cancel"}, "void": {"void"}, "close": {"close"}, "open": {"open", "start"},
         "generate": {"generate", "create"}, "run": {"run", "start"}, "send": {"send", "resend"},
         "submit": {"submit", "send"}, "import": {"import", "upload"}, "upload": {"upload", "import"},
         "assign": {"assign"}, "suspend": {"suspend", "pause", "block"}, "resume": {"resume", "unblock"},
         "pause": {"pause", "suspend"}, "retry": {"retry"}, "deploy": {"deploy", "push"},
         "rollback": {"rollback", "roll"}, "transition": {"move", "change", "transition"}}
STOP = {"the", "a", "an", "to", "of", "for", "and", "&", "on", "in", "by", "with", "or", "all", "this", "new"}


def _schemas() -> dict:
    if not SCHEMAS:
        SCHEMAS.update(G.load_contracts(ROOT)[1])
    return SCHEMAS


def returned(op: dict) -> set:
    """Schema names a 2xx response carries, and the names those schemas refer to one level down."""
    found = set()
    for code, r in (op.get("responses") or {}).items():
        if str(code).startswith("2"):
            found |= set(re.findall(r"#/components/schemas/(\w+)", json.dumps(r, default=str)))
    for n in list(found):
        found |= set(re.findall(r"#/components/schemas/(\w+)", json.dumps(_schemas().get(n) or {}, default=str)))
    return found - {"Page", "Paged", "Cursor", "PageMeta", "Envelope", "Problem"}


def family(name: str) -> str:
    return re.sub(r"(Summary|Detail|Details|View|Row|Item|Line|Record|Response|Page|List)$", "", str(name))


def words(text: str) -> list:
    return [w for w in re.findall(r"[a-z0-9]+", str(text).lower()) if w not in STOP]


def op_words(op: str) -> tuple[str, list]:
    m = re.match(r"^([a-z]+)([A-Z].*)?$", op)
    if not m:
        return op, []
    return m.group(1), [w for w in G.noun_for(m.group(2) or "").lower().split() if w not in STOP]


def label_fits(label: str, op: str) -> int:
    """How well a button label names an operation: 0 when it does not; more when more of the object is named."""
    lw = words(label)
    if not lw:
        return 0
    verb, noun = op_words(op)
    if lw[0] not in VERBS.get(verb, {verb}):
        return 0
    if not noun:
        return 1
    hit = sum(1 for n in noun if any(w[:5] == n[:5] for w in lw[1:]))
    return hit if hit == len(noun) or (hit and len(lw) == 1 + hit) else 0


def reached(s: dict) -> set:
    refs = {c.get("operation") for _, c in comps(s) if c.get("operation")}
    for o in s.get("overlays") or []:
        for k in ("confirm", "dismiss"):
            if isinstance(o, dict) and isinstance(o.get(k), dict) and o[k].get("operation"):
                refs.add(o[k]["operation"])
    for t in ((s.get("navigation") or {}).get("transitions") or []):
        if isinstance(t, dict) and t.get("operation"):
            refs.add(t["operation"])
    return refs


def is_cancel(c: dict) -> bool:
    return str(c.get("label") or "").strip().lower() in ("cancel", "close", "back", "dismiss")


def fix_unreached(s: dict, ops: dict, log: list, keeps: list, **_) -> None:
    sid = s["id"]
    refs = reached(s)
    todo = [a for a in apis(s) if a["operationId"] not in refs and a.get("trigger") not in ("background", "onInterval")
            and a["operationId"] in ops]
    if not todo:
        return
    free = [c for _, c in comps(s) if not c.get("operation")]
    has_inputs = any(c.get("kind") in CHECK_INPUTS for _, c in comps(s))
    collected = {(o.get("confirm") or {}).get("operation") for o in (s.get("overlays") or [])
                 if isinstance(o, dict) and isinstance(o.get("confirm"), dict)}

    def uncollected(c, op):
        """A button for a write whose body nothing on the screen collects (S-BUTTON-FORM): not bound here."""
        f = ops[op]
        rb = f["op"].get("requestBody")
        needs = isinstance(rb, dict) and (bool(rb.get("required")) or "$ref" in rb)
        return ("Button" in str(c.get("kind")) and f["method"] in WRITES and needs and op not in collected
                and not has_inputs)

    blocked: set = set()

    def bind(c, op, why):
        c["operation"] = op
        free.remove(c)
        log.append(f"{sid}: {c.get('kind')} {str(c.get('label') or '')[:40]!r} binds {op} ({why})")

    left = []
    for a in todo:
        op = a["operationId"]
        f = ops[op]
        read = f["method"] == "get" or op.startswith(("list", "get", "search"))
        # 1. the component proposed for it
        mine = [c for c in free if c.get("impliedBy") == op and not is_cancel(c)]
        got = [c for c in mine if not uncollected(c, op)]
        if mine and not got:
            blocked.add(op)
        for c in got:
            bind(c, op, "the component proposed for it")
        if got:
            continue
        # 2. bound to the schema it returns (a read) or collects (a write's form)
        if read:
            names = {family(n) for n in returned(f["op"])}
            got = [c for c in free if c.get("kind") not in ("metricTile",) and "Button" not in str(c.get("kind"))
                   and family(str(c.get("bindsTo") or "").replace("[]", "").split(".")[0]) in names]
        else:
            body = G.body_fields(f, _schemas())[0]
            got = [c for c in free if body and c.get("kind") in INPUT_KINDS
                   and str(c.get("bindsTo") or "").split(".")[0] == body]
        for c in got:
            bind(c, op, "bound to its schema")
        if got:
            continue
        # 3. a button that names it
        scored = sorted(((label_fits(c.get("label"), op), i, c) for i, c in enumerate(free)
                         if "Button" in str(c.get("kind")) and not is_cancel(c)), key=lambda t: (-t[0], t[1]))
        if scored and scored[0][0] > 0 and uncollected(scored[0][2], op):
            blocked.add(op)
            scored = []
        if scored and scored[0][0] > 0 and (len(scored) == 1 or scored[1][0] < scored[0][0]):
            bind(scored[0][2], op, "its label names it")
            continue
        gates = [c for c in free if c.get("kind") == "publishGate"]
        if op.startswith("publish") and len(gates) == 1:
            bind(gates[0], op, "the screen's one publish gate")
            continue
        left.append(a)
    # 4. the one unbound table or panel the screen has, for the one read of its kind that nothing shows
    for kinds, pick in ((LIST_KINDS, lambda o: o.startswith(("list", "search"))),
                        ({"detailPanel"}, lambda o: o.startswith("get"))):
        reads = [a for a in left if pick(a["operationId"]) and ops[a["operationId"]]["method"] == "get"]
        slots = [c for c in free if c.get("kind") in kinds and not c.get("bindsTo")]
        if len(reads) == 1 and len(slots) == 1:
            bind(slots[0], reads[0]["operationId"], "the screen's one unbound panel for its one unshown read")
            left.remove(reads[0])
    for a in left:
        op = a["operationId"]
        if BEACON.match(op) and ops[op]["method"] == "post":
            a["trigger"] = "background"
            log.append(f"{sid}: {op} runs in the background (a beacon no person triggers)")
            continue
        keeps.append((sid, "S-OP-UNREACHED", f"{op} ({a.get('trigger')}): " + (
            "its control on the approved screen collects nothing for the body it needs" if op in blocked else
            "no control on the approved screen reaches it") + " (client-approved UI)"))


# ── S-METRIC-NO-OP ──────────────────────────────────────────────────────────────────────────────
# A metric tile the client's board drew, with no read behind it. The tile stays (client-approved UI); it binds the
# read that computes it: a read the screen declares whose response carries the measure by name (`bindsTo`
# Schema.field), else the scorecard read the screen already calls (`getKpiValues`, by KPI code). A tile no declared
# read computes is reported: binding it needs a read or a KPI the contract does not yet have.

TILE_STOP = STOP | {"total", "count", "number", "no", "avg", "average", "today", "current", "percent", "pct",
                    "of", "per", "%", "#"}


def fields_of(name: str, depth: int = 0) -> dict:
    """`{field path: words}` of a schema, nested one level (rows of a page, a summary's sub-objects)."""
    out = {}
    for p, body in G.schema_fields(name, _schemas()).items():
        out[p] = set(words(G.noun_for(p))) - TILE_STOP
        ref = re.findall(r"#/components/schemas/(\w+)", json.dumps(body, default=str))
        if ref and depth < 1:
            for q, w in fields_of(ref[0], depth + 1).items():
                out[f"{p}.{q}"] = w
    return out


def fix_metrics(s: dict, ops: dict, log: list, keeps: list, **_) -> None:
    sid = s["id"]
    tiles = [c for _, c in comps(s) if c.get("kind") == "metricTile" and not c.get("operation")
             and not c.get("bindsTo") and not c.get("derived")]
    if not tiles:
        return
    reads = [a["operationId"] for a in apis(s) if a["operationId"] in ops
             and (ops[a["operationId"]]["method"] == "get" or a["operationId"].startswith(("get", "list", "search")))]
    shapes = []
    for o in reads:
        for n in G.response_schemas(ops[o]["op"])[:1]:
            # A measure is read off one object (a summary, a view, a health record), never off a row of a list.
            if o.startswith("get") or re.search(r"(View|Analytics|Performance|Health|Insights|Summary|Totals|Kpis?)$", n):
                flds = {p: w for p, w in fields_of(n).items()
                        if not re.search(r"(Id|Ids|Identifier|At|Allowed|Enabled)$", p.split(".")[-1])}
                shapes.append((o, n, flds))
    for c in tiles:
        want = set(words(c.get("label"))) - TILE_STOP
        best = None
        if want:
            for o, n, flds in shapes:
                for path, w in flds.items():
                    if not w:
                        continue
                    hit = len({x for x in want if any(x[:5] == y[:5] for y in w)})
                    score = (hit / len(want), hit / len(w))
                    if hit and score[0] == 1 and score[1] >= 0.66 and (best is None or score > best[0]):
                        best = (score, o, f"{n}.{path}")
        if best:
            c["operation"], c["bindsTo"] = best[1], best[2]
            log.append(f"{sid}: tile {str(c.get('label'))[:40]!r} binds {best[2]} ({best[1]})")
        elif "getKpiValues" in reads:
            c["operation"] = "getKpiValues"
            log.append(f"{sid}: tile {str(c.get('label'))[:40]!r} binds getKpiValues (the screen's scorecard read)")
        else:
            keeps.append((sid, "S-METRIC-NO-OP", f"tile {c.get('label')!r}: no read the screen declares computes it "
                          f"(needs a read or a KPI the contract does not have; the tile stays: client-approved UI)"))


# ── S-NO-READ ───────────────────────────────────────────────────────────────────────────────────
# A screen that edits a record (PUT or PATCH) and reads nothing opens its form blank over saved data. Where the
# contract reads the record on the same path and the approved screen has a panel or table that can show it, the read
# is declared on load and bound there (an invisible change). Otherwise it is reported: the contract has no read of
# the record, or the approved screen has nothing to show it in.

STAMP = "Block A audit, 14 October 2026"


def fix_no_read(s: dict, ops: dict, log: list, keeps: list, **_) -> None:
    sid = s["id"]
    facts = {a["operationId"]: ops.get(a["operationId"]) for a in apis(s)}
    methods = {f["method"] for f in facts.values() if f}
    if not (methods & {"put", "patch"}) or "get" in methods:
        return
    if any(re.match(r"^(search|evaluate|decide|resolve|preview|calculate|quote|check|validate|estimate|price|lookup|"
                    r"identify|find|compute|simulate|match|suggest|run|list|get|query|render|verify|recommend)", o, re.I)
           for o in facts):
        return
    by_path = {(f["path"], f["method"]): o for o, f in ops.items()}
    edits = [o for o, f in facts.items() if f and f["method"] in ("put", "patch")]
    read = next((by_path.get((facts[o]["path"], "get")) for o in edits if by_path.get((facts[o]["path"], "get"))), None)
    if not read:
        keeps.append((sid, "S-NO-READ", f"{edits[0]}: the contract has no read on its path (a contract gap)"))
        return
    names = {family(n) for n in returned(ops[read]["op"])}
    slots = [c for _, c in comps(s) if not c.get("operation") and c.get("kind") in ("detailPanel", "dataTable")
             and (not c.get("bindsTo") or family(str(c.get("bindsTo")).split(".")[0]) in names)]
    if len(slots) != 1:
        keeps.append((sid, "S-NO-READ", f"{read} would read the record, and the approved screen has no panel to show "
                      f"it in (client-approved UI)"))
        return
    entry = {"operationId": read, "contract": ops[read]["contract"],
             "purpose": " ".join(str(ops[read]["op"].get("summary") or read).split()), "trigger": "onLoad",
             "provenance": f"{STAMP}: the record {edits[0]} edits, read before it is edited (CHG-SCR-005)"}
    s.setdefault("apis", []).append(entry)
    slots[0]["operation"] = read
    log.append(f"{sid}: reads {read} on load into its {slots[0].get('kind')}")


# ── S-DUP-REGION ────────────────────────────────────────────────────────────────────────────────
# A region name is the region's internal id, and `derive-wireframes.py` keys regions by it: a second `contentBody`
# replaced the first in every wireframe drawn from the screen. **The last keeps its name**, because it is the one the
# wireframe draws today, so the drawn frame does not change; each earlier one takes its slot (`contentBody` in slot
# `headline` becomes `contentBodyHeadline`), or a number. No title or component moves.

def fix_dup_regions(s: dict, ops: dict, log: list, keeps: list, **_) -> None:
    regions = [r for r in ((s.get("layout") or {}).get("regions") or []) if isinstance(r, dict)]
    taken = {r.get("name") for r in regions}
    last = {r.get("name"): i for i, r in enumerate(regions)}
    for i, r in enumerate(regions):
        n = r.get("name")
        if not n or last.get(n) == i:
            continue
        slot = re.sub(r"[^A-Za-z0-9]", "", str(r.get("slot") or ""))
        cand = n + (slot[:1].upper() + slot[1:] if slot else "2")
        k = 2
        while cand in taken:
            k += 1
            cand = f"{n}{slot[:1].upper() + slot[1:] if slot else ''}{k}"
        r["name"] = cand
        taken.add(cand)
        log.append(f"{s['id']}: region {n} (slot {r.get('slot')}) renamed {cand}")


# ── S-PURPOSE-BOILERPLATE and S-PURPOSE-TEMPLATE ────────────────────────────────────────────────
# A screen's `purpose` and an api's `purpose` are spec prose for the designer and the developer, never shown. The
# 18 August generator wrote "See X for this venue." where a screen had no purpose of its own, and board imports pasted
# the board's title and date; an api purpose was sometimes the operationId or "Add something". Both are rewritten
# from the contract: the screen's from its name and the summaries of what it reads and does, the api's from the
# operation's summary.

PURPOSE_BOILERPLATE = re.compile(
    r"^(Work with|See|Find|Add) .{2,80} for this venue\.?$"
    r"|Change how .{2,60} behaves here, and see which level the current value came from"
    r"|from the client design board"
    r"|^The screen this app sits on", re.I)


def summary(ops: dict, op: str) -> str:
    return " ".join(str(ops[op]["op"].get("summary") or "").split()).rstrip(".")


def fix_screen_purpose(s: dict, ops: dict, log: list, keeps: list, **_) -> None:
    if not PURPOSE_BOILERPLATE.search(str(s.get("purpose") or "")):
        return
    known = [a for a in apis(s) if a["operationId"] in ops]
    reads = [a["operationId"] for a in known if ops[a["operationId"]]["method"] == "get"]
    reads.sort(key=lambda o: next((0 for a in known if a["operationId"] == o and a.get("trigger") == "onLoad"), 1))
    acts = [a["operationId"] for a in known if ops[a["operationId"]]["method"] in WRITES]
    name = str(s.get("name") or s["id"]).strip()
    parts = []
    if reads:
        parts.append("shows " + "; ".join(f"{summary(ops, o)[:1].lower() + summary(ops, o)[1:]} (`{o}`)"
                                         for o in reads[:2] if summary(ops, o)))
    if acts:
        parts.append("acts with " + "; ".join(f"{summary(ops, o)[:1].lower() + summary(ops, o)[1:]} (`{o}`)"
                                             for o in acts[:3] if summary(ops, o)))
    parts = [p for p in parts if not p.endswith(("shows ", "acts with "))]
    merged = re.search(r"\(merged into ([A-Z]+-\d+)[^)]*\)", str(s.get("purpose") or ""))
    if not parts and merged:
        s["purpose"] = (f"{name}: merged into {merged.group(1)}; this id routes there and nothing on it is built "
                        f"separately.")
        log.append(f"{s['id']}: purpose names the screen it was merged into")
        return
    if not parts:
        keeps.append((s["id"], "S-PURPOSE-BOILERPLATE", "the screen declares no operation to say what it does from; "
                      "its purpose needs a person"))
        return
    s["purpose"] = f"{name}: " + ", and ".join(parts) + "."
    log.append(f"{s['id']}: purpose written from its operations")


def fix_api_purpose(s: dict, ops: dict, log: list, keeps: list, **_) -> None:
    for a in apis(s):
        p = str(a.get("purpose") or "").strip()
        o = a["operationId"]
        if (not p or p == o or p.lower() in ("add something", "tbd", "todo")) and o in ops and summary(ops, o):
            a["purpose"] = summary(ops, o)
            log.append(f"{s['id']}: {o} purpose from the contract summary")


# ── S-DUP-SCREEN ────────────────────────────────────────────────────────────────────────────────
# Two screens on one platform calling the same operations are either one screen drawn twice or two facets of one
# record the client's boards drew apart. Screens are never merged here (client-approved UI); each states its
# division (`division`): what it shares, with whom, and which part of the record it is for, from its own purpose
# and source. `check-screen-wiring` accepts a group whose members all state one.

CONSOLE_FRAME = {"listTenants", "openPlatformStaffGrant", "listOwnPlatformStaffGrants"}
_GROUPS: dict = {}


def dup_groups(docs: dict) -> dict:
    """screen id -> the other ids on its platform with the same operation signature (the check's)."""
    key = id(docs)
    if key not in _GROUPS:
        sigs: dict = {}
        for d in docs.values():
            code = (d.get("platform") or {}).get("code")
            for s in d.get("screens") or []:
                own = {a["operationId"] for a in apis(s)} - CONSOLE_FRAME
                if len(own) >= 2:
                    sigs.setdefault((code, frozenset(own)), []).append(s["id"])
        out = {}
        for ids in sigs.values():
            if len(ids) > 1:
                for i in ids:
                    out[i] = [x for x in ids if x != i]
        _GROUPS.clear()
        _GROUPS[key] = out
    return _GROUPS[key]


def fix_division(s: dict, ops: dict, log: list, keeps: list, docs: dict | None = None, **_) -> None:
    others = dup_groups(docs or {}).get(s["id"])
    if not others or s.get("division"):
        return
    shared = sorted({a["operationId"] for a in apis(s)} - CONSOLE_FRAME)
    what = " ".join(str(s.get("purpose") or s.get("name") or "").split()).rstrip(".")
    src = s.get("source") or {}
    where = (f" (pack {src.get('pack')}, board {src.get('board')}.{src.get('number')}, page {src.get('page')})"
             if src.get("pack") else "")
    put_after(s, "division", f"Shares {', '.join(f'`{o}`' for o in shared[:4])}{' and more' if len(shared) > 4 else ''} with "
                     f"{', '.join(sorted(others))}; this screen is {s.get('name')}{where}: "
                     f"{what[:1].lower() + what[1:]}.", ("purposeNote", "purpose", "name"))
    log.append(f"{s['id']}: division stated against {', '.join(sorted(others)[:3])}")


STEPS = {
    "S-PURPOSE-BOILERPLATE": fix_screen_purpose,
    "S-PURPOSE-TEMPLATE": fix_api_purpose,
    "S-STATE-BOILERPLATE": fix_states,
    "S-SCREEN-PERMISSION": fix_permission,
    "S-METRIC-NO-OP": fix_metrics,
    "S-NO-READ": fix_no_read,
    "S-DUP-REGION": fix_dup_regions,
    "S-OP-UNREACHED": fix_unreached,
    "S-DUP-SCREEN": fix_division,
}


# ── files ───────────────────────────────────────────────────────────────────────────────────────

def dump(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated class ids (default: every rule)")
    ap.add_argument("--platform", help="comma-separated platform codes (default: every platform)")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    steps = [x.strip() for x in a.only.split(",")] if a.only else list(STEPS)
    unknown = [x for x in steps if x not in STEPS]
    if unknown:
        print(f"unknown rule(s): {', '.join(unknown)}; known: {', '.join(STEPS)}")
        return 2
    plats = tuple(x.strip() for x in a.platform.split(",")) if a.platform else None

    ops = load_ops()
    files = [f for f in sorted(SCREENS.glob("P*.yaml")) if not plats or f.name.startswith(plats)]
    raws = {f: f.open(encoding="utf-8", newline="").read() for f in files}
    docs = {}
    for f in files:
        d = yaml.load(raws[f], Loader=LOADER)
        if dump(d) != raws[f].replace(CRLF, LF):
            print(f"  {f.name} is not in the derivers' form (safe_dump, width 100); left alone")
            continue
        docs[f] = d

    log: list = []
    keeps: list = []
    changed: set = set()
    for step in steps:
        fn = STEPS[step]
        for f, d in docs.items():
            for s in d.get("screens") or []:
                before = json.dumps(s, sort_keys=False, default=str)
                fn(s, ops, log, keeps, platform=d.get("platform") or {}, docs=docs)
                if json.dumps(s, sort_keys=False, default=str) != before:
                    changed.add(f)
    kinds = Counter(re.sub(r"`[^`]*`|'[^']*'|\b[A-Z][A-Z0-9_]{3,}\b|\d+", "", x.split(": ", 1)[1]).strip() for x in log)
    print(f"derive-screen-wiring: {', '.join(steps)}; {len(log)} change(s) in {len(changed)} file(s)")
    for k, v in kinds.most_common(40):
        print(f"  {v:>5}  {k}")
    for line in (log if a.verbose else log[:15]):
        print("  " + line)
    if keeps:
        print(f"  {len(keeps)} keep(s), left as they are:")
        for sid, rule, why in (keeps if a.verbose else keeps[:40]):
            print(f"    KEEP {rule:<22} {sid:<9} {why}")
    for f in sorted(changed):
        out = dump(docs[f])
        if CRLF in raws[f]:
            out = out.replace(LF, CRLF)      # the checkout's line endings (core.autocrlf)
        if out == raws[f]:
            continue
        if a.apply:
            f.open("w", encoding="utf-8", newline="").write(out)
            print(f"  written  {f.name}")
        else:
            print(f"  would write  {f.name}")
    if not a.apply and changed:
        print("  (dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
