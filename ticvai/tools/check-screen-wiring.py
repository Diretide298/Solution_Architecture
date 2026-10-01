#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What a screen record says against what it can actually do.

**Audit classes A-SCREEN-* (audit/ticvai/ROOT-CLASSES.md).** Screens were generated, then
patched, and the 26 September pull audit found the marks of both: state texts pasted from the list
pattern onto screens with no create operation or filter (R250), a region name used twice
(R253), a declared operation no component reaches (R273), a write fired on load (R268), a button
calling a body-taking operation with nothing to collect the body (R264), no screen permission
while the no-access state promises to name one (R255), a screen that edits a record and reads
nothing (R265), a 202 with nothing to poll (R288), open questions citing endpoints that do not
exist (R266), notes that describe a screen from before a rename (R269), operation purposes that
are the operationId (R260) and offline texts promising writes no operation can queue (R257).
`check-screens.py` validates each record against the schema; this reads the record against itself
and against the contracts.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-screen-wiring.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "S-STATE-BOILERPLATE": "empty-state text promises a create action, filter or permission the screen lacks (R250)",
    "S-DUP-REGION": "a region name used twice on one screen (R253)",
    "S-OP-UNREACHED": "a declared operation no component, overlay or transition reaches (R273)",
    "S-ONLOAD-WRITE": "a write operation triggered onLoad (R268)",
    "S-BUTTON-FORM": "a button calls an operation with a required body and nothing collects it (R264)",
    "S-SCREEN-PERMISSION": "permissioned operations and a no-access state, but no screen permission (R255)",
    "S-NO-READ": "a screen that edits (PUT/PATCH) and reads nothing (R265)",
    "S-ASYNC-POLL": "a 202 operation with no read on the screen to follow it (R288)",
    "S-OPENQ-STALE": "an open question cites an endpoint no operation has (R266)",
    "S-NOTES-STALE": "notes or gaps say an operation was removed or absent while apis hold it (R269)",
    "S-PURPOSE-TEMPLATE": "an api purpose that is the operationId, empty, or template text (R260)",
    "S-OFFLINE-CLAIM": "an offline state promising queued writes no operation is offline-capable for (R257)",
    "S-WORKSTATION-OP": "a workstation-scoped operation on a platform nobody signs a workstation into (R100)",
    "S-GUEST-AUDIENCE": "a guest screen calls an operation whose audience has no guest (R167 R289 R072)",
    "S-UPLOAD": "a write takes a file reference and the screen has no upload (R196)",
    "S-EXPORT": "an Export control with no operation behind it (R293)",
    "S-METRIC-NO-OP": "a metric tile with no operation and no binding (R283)",
    "S-DUP-SCREEN": "two screens on one platform with the same operations and no stated division (R276)",
    "S-CONSUMED-MIRROR": "apis and the contract's x-ticvai-consumed-by disagree (R254 R042)",
    "S-FIELD-BINDING": "a component bound to Schema.field where the schema has no such field (R275)",
    "S-PANEL-ENTITY": "a list and its detail panel bound to different entities (R256)",
    "S-STAFF-AUDIENCE": "a staff screen calls an operation whose audience has no staff: guest-, device-, service- or partner-only (R254, CHG-WIR-001)",
    "S-PURPOSE-BOILERPLATE": "a screen purpose that is a generator template or a pasted board placeholder (CHG-WIR-003)",
}
# **The staff surfaces.** A screen on one of these is operated by venue or platform staff, so every operation
# it calls must accept a staff caller. Added 2 October 2026 with the wiring fixes (CHG-WIR-001): guest-only
# reads (listMyCases, getLoyaltyPosition), device heartbeats and service-only writes had been bulk-attached to
# back-office, till and staff-app screens, where the call is refused or answers for the wrong principal.
# Partner (P10), accreditation-applicant (P11), developer (P14) and sign-up (P17) surfaces are not staff.
STAFF_CODES = ("P04", "P06", "P07", "P08", "P09", "P12", "P13", "P15", "P16")
STAFF_OK = {"staff", "public", "anonymous"}
# **Generator purposes.** The 18 August generator wrote one of these when a screen had no purpose of its own,
# and board imports pasted the board's title with its date. Each reads like a purpose and says nothing a
# designer can act on; several were copied between screens (CHG-WIR-003).
PURPOSE_BOILERPLATE = re.compile(
    r"^(Work with|See|Find|Add) .{2,80} for this venue\.?$"
    r"|Change how .{2,60} behaves here, and see which level the current value came from"
    r"|from the client design board"
    r"|^The screen this app sits on", re.I)
GUEST_CODES = ("P01", "P02", "P05")
FILE_REF = re.compile(r"^(storageRef|fileRef|fileReference|documentRef|imageRef|assetRef|attachmentRef|"
                      r"uploadRef|storageKey|fileKey|blobRef|mediaAssetId|photoRef)s?$")

WRITES = ("post", "put", "patch", "delete")
# POSTs that compute rather than change state; on load they are reads.
READ_LIKE = re.compile(r"^(search|evaluate|decide|resolve|preview|calculate|quote|check|validate|"
                       r"estimate|price|lookup|identify|find|compute|simulate|match|suggest|run|"
                       r"list|get|query|render|verify|recommend)", re.I)
CREATE_LIKE = re.compile(r"^(create|add|register|issue|open|start|submit|raise|record|enrol|invite|"
                         r"import|upload|book|reserve|request|schedule|draft|new|clone|copy|"
                         r"generate|publish|assign|allocate|log)", re.I)
FILTERS = {"searchField", "selectField", "multiSelect", "datePicker", "toggle"}
INPUTS = FILTERS | {"textField", "numberField", "fileUpload", "consentBlock", "scanTarget"}
OFFLINE_PROMISE = re.compile(r"\b(queue[sd]?|queued|kept and sent|sends? (it )?when|syncs?|"
                             r"works offline|saved locally|replay)", re.I)


def required_body(op: dict) -> bool:
    rb = op.get("requestBody")
    if not isinstance(rb, dict):
        return False
    return bool(rb.get("required", False)) or "$ref" in rb


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-screen-wiring", RULES)
    ops = g.operations()
    path_index = set()
    for f in ops.values():
        path_index.add((f["method"].upper(), re.sub(r"\{[^}]+\}", "{}", f["path"]).rstrip("/")))

    all_screens = g.screens()
    by_schema, _ = g.schemas()
    # Platforms that sign a workstation in: some screen takes workstationId from the session.
    ws_platforms = {plat for plat, s in all_screens
                    if any(isinstance(p, dict) and p.get("name") == "workstationId"
                           for p in ((s.get("entryState") or {}).get("params") or []))}
    consumed = {}
    for oid, f in ops.items():
        for entry in f["op"].get("x-ticvai-consumed-by") or []:
            parts = str(entry).split()
            if len(parts) > 1:
                consumed.setdefault(parts[1], set()).add(oid)
    sigs = {}

    def body_props(f):
        rb = f["op"].get("requestBody") or {}
        for media in (rb.get("content") or {}).values():
            sch = (media or {}).get("schema") or {}
            name = g.ref_name(sch.get("$ref", "")) if isinstance(sch, dict) else ""
            node = by_schema.get((f["contract"], name)) or (sch if isinstance(sch, dict) else {})
            return set((node.get("properties") or {}).keys())
        return set()

    for plat, s in all_screens:
        sid = s["id"]
        apis = [a for a in (s.get("apis") or []) if isinstance(a, dict) and a.get("operationId")]
        op_ids = {a["operationId"] for a in apis}
        # --- R100 workstation operations off the till ------------------------------------------
        for o in sorted(op_ids):
            f = ops.get(o)
            if f and f["op"].get("x-ticvai-scope-level") == "workstation" and plat not in ws_platforms:
                guard.add("S-WORKSTATION-OP", f"{sid}:{o}",
                          f"{sid} ({plat}): {o} is workstation-scoped and nothing on {plat} signs a workstation in")
        # --- R167 R289 guest surfaces ----------------------------------------------------------
        if plat.startswith(GUEST_CODES):
            for o in sorted(op_ids):
                f = ops.get(o)
                aud = (f or {}).get("op", {}).get("x-ticvai-audience") or []
                if f and aud and not ({"guest", "public", "anonymous"} & set(aud)) \
                        and not f["op"].get("x-ticvai-guest-callable") and f["op"].get("x-ticvai-auth") != "none":
                    guard.add("S-GUEST-AUDIENCE", f"{sid}:{o}",
                              f"{sid}: a guest screen calls {o}, audience {', '.join(aud)}")
        # --- CHG-WIR-001 staff surfaces call staff operations -----------------------------------
        if plat.startswith(STAFF_CODES) and s.get("audience") in (None, "staff", "platform"):
            for o in sorted(op_ids):
                f = ops.get(o)
                aud = set((f or {}).get("op", {}).get("x-ticvai-audience") or [])
                if f and aud and not (aud & STAFF_OK):
                    guard.add("S-STAFF-AUDIENCE", f"{sid}:{o}",
                              f"{sid} ({plat}): a staff screen calls {o}, audience {', '.join(sorted(aud))}")
        # --- CHG-WIR-003 template purposes ---------------------------------------------------------
        if PURPOSE_BOILERPLATE.search(str(s.get("purpose") or "")):
            guard.add("S-PURPOSE-BOILERPLATE", sid, f"{sid}: purpose is a template: {str(s.get('purpose'))[:80]!r}")
        # --- R196 file references --------------------------------------------------------------
        needs_file = sorted(o for o in op_ids if ops.get(o) and any(FILE_REF.match(p) for p in body_props(ops[o])))
        if needs_file and not any(re.search(r"(upload|presign|createMediaAsset|createAsset)", o, re.I) for o in op_ids):
            guard.add("S-UPLOAD", sid, f"{sid}: {needs_file[0]} takes a file reference and the screen uploads nothing")
        # --- R276 duplicate screens ------------------------------------------------------------
        if len(op_ids) >= 2:
            sigs.setdefault((plat, frozenset(op_ids)), []).append(sid)
        # --- R254 R042 the consumed-by mirror --------------------------------------------------
        for o in sorted(op_ids):
            f = ops.get(o)
            if f and f["op"].get("x-ticvai-consumed-by") is not None and o not in consumed.get(sid, set()):
                guard.add("S-CONSUMED-MIRROR", f"{sid}:{o}", f"{sid} declares {o}; its x-ticvai-consumed-by does not name {sid}")
        for o in sorted(consumed.get(sid, set()) - op_ids):
            guard.add("S-CONSUMED-MIRROR", f"{o}->{sid}", f"{o}'s x-ticvai-consumed-by names {sid}, which does not declare it")
        facts = {a["operationId"]: ops.get(a["operationId"]) for a in apis}
        regions = ((s.get("layout") or {}).get("regions")) or []
        comps = [c for r in regions for c in (r.get("components") or []) if isinstance(c, dict)]
        kinds = {c.get("kind") for c in comps}
        states = s.get("states") or {}
        overlays = [o for o in (s.get("overlays") or []) if isinstance(o, dict)]

        # --- R250 state boilerplate ------------------------------------------------------------
        creates = [o for o, f in facts.items() if f and f["method"] == "post" and CREATE_LIKE.match(o)]
        perms = {str(f["op"].get("x-ticvai-permission")) for f in facts.values()
                 if f and f["op"].get("x-ticvai-permission")}
        if "Carries the create action" in str(states.get("emptyFirstRun") or "") and not creates:
            guard.add("S-STATE-BOILERPLATE", f"{sid}:emptyFirstRun",
                      f"{sid}: emptyFirstRun 'carries the create action' and no create operation")
        if "The filter narrowed" in str(states.get("emptyNoResults") or "") and not (kinds & FILTERS):
            guard.add("S-STATE-BOILERPLATE", f"{sid}:emptyNoResults",
                      f"{sid}: emptyNoResults names a filter and the screen has no filter or search")
        if "Names the missing permission" in str(states.get("emptyNoAccess") or "") and not perms:
            guard.add("S-STATE-BOILERPLATE", f"{sid}:emptyNoAccess",
                      f"{sid}: emptyNoAccess names a permission and no operation has one")
        # --- R253 duplicate regions ------------------------------------------------------------
        names = [r.get("name") for r in regions if r.get("name")]
        for n in sorted({n for n in names if names.count(n) > 1}):
            guard.add("S-DUP-REGION", f"{sid}:{n}", f"{sid}: region {n!r} appears {names.count(n)} times")
        # --- R273 unreached operations ---------------------------------------------------------
        refs = {c.get("operation") for c in comps if c.get("operation")}
        for o in overlays:
            for k in ("confirm", "dismiss"):
                v = o.get(k)
                if isinstance(v, dict) and v.get("operation"):
                    refs.add(v["operation"])
        for t in ((s.get("navigation") or {}).get("transitions") or []):
            if isinstance(t, dict) and t.get("operation"):
                refs.add(t["operation"])
        for a in apis:
            if a["operationId"] not in refs and a.get("trigger") not in ("background", "onInterval"):
                guard.add("S-OP-UNREACHED", f"{sid}:{a['operationId']}",
                          f"{sid}: declares {a['operationId']} ({a.get('trigger')}) and no component reaches it")
        # --- R268 writes on load ---------------------------------------------------------------
        for a in apis:
            f = facts.get(a["operationId"])
            if f and a.get("trigger") == "onLoad" and f["method"] in WRITES \
                    and not READ_LIKE.match(a["operationId"]):
                guard.add("S-ONLOAD-WRITE", f"{sid}:{a['operationId']}",
                          f"{sid}: {a['operationId']} ({f['method'].upper()}) fires onLoad")
        # --- R264 a button is not a form -------------------------------------------------------
        collected = {((o.get("confirm") or {}).get("operation")) for o in overlays
                     if isinstance(o.get("confirm"), dict)}
        has_inputs = bool(kinds & INPUTS)
        for c in comps:
            op_id = c.get("operation")
            f = ops.get(op_id) if op_id else None
            if f and "Button" in str(c.get("kind")) and f["method"] in WRITES \
                    and required_body(f["op"]) and op_id not in collected and not has_inputs:
                guard.add("S-BUTTON-FORM", f"{sid}:{op_id}",
                          f"{sid}: button {c.get('label')!r} calls {op_id}, which takes a body, and "
                          f"nothing on the screen collects it")
        # --- R255 screen permission ------------------------------------------------------------
        if perms and "emptyNoAccess" in states and not s.get("permission"):
            guard.add("S-SCREEN-PERMISSION", sid, f"{sid}: operations need {', '.join(sorted(perms)[:3])}"
                      f"{' ...' if len(perms) > 3 else ''}; the screen declares no permission")
        # --- R265 edits with no read -----------------------------------------------------------
        methods = {f["method"] for f in facts.values() if f}
        if methods & {"put", "patch"} and "get" not in methods \
                and not any(READ_LIKE.match(o) for o in facts):
            guard.add("S-NO-READ", sid, f"{sid}: edits a record ({', '.join(sorted(methods))}) and reads nothing")
        # --- R288 asynchronous operations ------------------------------------------------------
        gets = {o for o, f in facts.items() if f and f["method"] == "get"}
        for o, f in facts.items():
            if f and "202" in {str(k) for k in (f["op"].get("responses") or {})}:
                same = {x for x in gets if ops[x]["contract"] == f["contract"]}
                if not same:
                    guard.add("S-ASYNC-POLL", f"{sid}:{o}",
                              f"{sid}: {o} answers 202 and the screen reads nothing from {f['contract']} to follow it")
        # --- R266 open questions citing endpoints ----------------------------------------------
        for q in (s.get("openQuestions") or []):
            text = q if isinstance(q, str) else " ".join(str(v) for v in (q or {}).values()) \
                if isinstance(q, dict) else str(q)
            for m, p in re.findall(r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[\w/{}.-]+)", text):
                norm = re.sub(r"\{[^}]+\}", "{}", p).rstrip("/")
                if (m, norm) not in path_index:
                    guard.add("S-OPENQ-STALE", f"{sid}:{m} {p}",
                              f"{sid}: open question cites {m} {p}, which no operation declares")
        # --- R269 stale notes ------------------------------------------------------------------
        prose = " ".join(str(s.get(k) or "") for k in ("notes", "apisNote", "purposeNote"))
        prose += " " + " ".join(str(x) for x in (s.get("gaps") or []))
        for o in facts:
            if re.search(r"`?%s`? (was |is |has been )?(removed|dropped|retired)|(removed|dropped) `?%s`?"
                         % (re.escape(o), re.escape(o)), prose):
                guard.add("S-NOTES-STALE", f"{sid}:{o}",
                          f"{sid}: notes say {o} was removed and apis still declare it")
        if apis and re.search(r"\bNo contract\b", prose):
            guard.add("S-NOTES-STALE", f"{sid}:no-contract",
                      f"{sid}: notes say 'No contract' beside {len(apis)} operation(s)")
        # --- R260 template purposes ------------------------------------------------------------
        for a in apis:
            p = str(a.get("purpose") or "").strip()
            if not p or p == a["operationId"] or p.lower() in ("add something", "tbd", "todo"):
                guard.add("S-PURPOSE-TEMPLATE", f"{sid}:{a['operationId']}",
                          f"{sid}: {a['operationId']} has purpose {p!r}")
        # --- R293 R283 controls with nothing behind them ---------------------------------------
        for c in comps:
            if "Button" in str(c.get("kind")) and re.search(r"\bexport\b", str(c.get("label") or ""), re.I) \
                    and not c.get("operation"):
                guard.add("S-EXPORT", f"{sid}:{c.get('label')}", f"{sid}: {c.get('label')!r} has no operation")
            if c.get("kind") == "metricTile" and not c.get("operation") and not c.get("bindsTo") \
                    and not c.get("derived"):
                guard.add("S-METRIC-NO-OP", f"{sid}:{c.get('label')}",
                          f"{sid}: metric tile {c.get('label')!r} names no operation and binds nothing")
        # --- R275 R256 bindings ----------------------------------------------------------------
        bound = {}
        for c in comps:
            b = str(c.get("bindsTo") or "").replace("[]", "")
            if not b:
                continue
            name, _, field = b.partition(".")
            stems = [st for (st, n) in by_schema if n == name]
            if field and stems:
                props = set()
                for st in stems:
                    node = by_schema[(st, name)]
                    props |= set((node.get("properties") or {}).keys())
                    for sub in node.get("allOf") or []:
                        ref = by_schema.get((st, g.ref_name((sub or {}).get("$ref", "")))) or sub or {}
                        props |= set((ref.get("properties") or {}).keys())
                head = field.split(".")[0]
                if props and head not in props:
                    guard.add("S-FIELD-BINDING", f"{sid}:{b}", f"{sid}: {c.get('kind')} binds {b}; {name} has no {head}")
            bound.setdefault(c.get("kind"), []).append(name)
        tables = bound.get("dataTable") or []
        panels = bound.get("detailPanel") or []
        fam = lambda n: re.sub(r"(Summary|Detail|View|Row|Item|Line)$", "", n)
        if len(tables) == 1 and len(panels) == 1 and fam(tables[0]) != fam(panels[0]) \
                and not fam(panels[0]).startswith(fam(tables[0])) and not fam(tables[0]).startswith(fam(panels[0])):
            guard.add("S-PANEL-ENTITY", sid, f"{sid}: the table shows {tables[0]}, the panel {panels[0]}")
        # --- R257 offline promises -------------------------------------------------------------
        off = str(states.get("offline") or "")
        if off and OFFLINE_PROMISE.search(off):
            writes = [o for o, f in facts.items() if f and f["method"] in WRITES]
            if writes and not any(facts[o]["op"].get("x-ticvai-offline-capable") for o in writes):
                guard.add("S-OFFLINE-CLAIM", sid,
                          f"{sid}: offline state promises to queue or sync and none of its "
                          f"{len(writes)} write(s) is x-ticvai-offline-capable")
    pairs = g.load_yaml(g.SCREENS / "_guest-pairs.yaml") or {}
    for (plat, sig), ids in sorted(sigs.items(), key=lambda kv: kv[1]):
        if len(ids) > 1:
            guard.add("S-DUP-SCREEN", "+".join(sorted(ids)),
                      f"{plat}: {', '.join(sorted(ids))} declare the same {len(sig)} operations")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
