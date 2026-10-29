#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What a screen record says against what it can actually do.

**Audit classes A-SCREEN-* (docs/active/root-classes.md).** Screens were generated, then
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

**Offline writes against frontend-patterns 4.4** (14 October 2026, CHG-SWP-004, the sweep after #27741). In an
offline app a write the contract marks `x-ticvai-offline-capable: true` goes through the one offline store's outbox,
and every other write is disabled offline with the reason on screen; a web app queues nothing. S-OFFLINE-CLAIM
caught a screen whose every write is online-only; these catch the rest of the contradiction:

    S-OFFLINE-REFUSED   on an offline app, the screen refuses offline (`offline: false`, or an offline state that
                        refuses and promises nothing) a write its contract marks offline-capable
    S-OFFLINE-QUEUED    the offline state promises to queue or sync, refuses nothing and does not name a write that
                        is not offline-capable (4.4: disabled offline), on a screen with other offline-capable
                        writes; or a web app's screen (no offline store) promises to queue its writes

**The contract decides, and it may narrow** (14 October 2026, CHG-OFL-001; the lead: "POS createOrder and payments are
offline-capable on the POS", and the client-approved screens are not changed). `x-ticvai-offline-apps` lists the
platform codes a write queues on (createPayment: P04, because only a till takes cash); `x-ticvai-offline-refused-on`
lists the screens where the approved UI refuses it offline (createOrder on the seat map, ADR-0013), with the reason in
`x-ticvai-offline-condition`. On any other platform or on a listed screen the write counts as online-only in all
three rules. `x-ticvai-outbox-replay: true` marks the outbox's own replay call (syncOrders), which a screen never
queues and never has to call disabled. S-OFFLINE-CLAIM, like S-OFFLINE-QUEUED, reads an offline state that also refuses ("Nothing here is
offered offline ... a request queued and never sent is worse") as a refusal, not a promise.

**What the client's prototype already shows** (20 October 2026, r8 integration, CHG-R8INT-003). A client-approved
screen whose layout is the client's prototype (`wireframe.provenance: client-verified`, `prototype.match: exact`) is
built from that view, and its visible YAML is fixed (check-approved-ui). A read it gains to fill what the view already
shows -- GST-067's "Tickets you can act on" rows and "Rules" note, from the guest's own refund requests and listings and
the venue's refund terms -- names that element in the binding: `shownBy: <the element's text in the prototype>`. Such
a read counts as reached, and S-SHOWN-BY fails a `shownBy` whose text the prototype file does not hold (as a quoted
string), or on a screen whose layout is not an exact, client-verified prototype view. **A partial match that names its
view counts too** (CHG-R8INT-008): the guest web's Your orders, Transfer & resale and Reservations are partial matches
whose rows the client approved, and the lead's ruling of 20 October 2026 is that no read a person sees is marked
`background` to escape S-OP-UNREACHED.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-screen-wiring.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
from typed_props import DEVICE_GUEST_PLATFORMS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
_PROTO_TEXT = {}


def prototype_text(rel):
    """The client prototype file's text, read once; empty when the file is absent (a gitignored design file)."""
    if rel not in _PROTO_TEXT:
        f = ROOT / rel
        _PROTO_TEXT[rel] = f.read_text(encoding="utf-8", errors="replace") if f.is_file() else ""
    return _PROTO_TEXT[rel]


def shown_in_prototype(s, shown, text_of=None):
    """None when `shown` is a quoted string of the screen's client-verified prototype file, else why not.

    The prototype is the screen's view when it matches it exactly (`match: exact`), or when it matches in part and
    the screen names the view it is drawn from (`match: partial` with a `prototype.view`; r8 integration,
    CHG-R8INT-008): Your orders, Transfer & resale and Reservations on the guest web are partial matches whose rows
    the client approved, and the reads that fill those rows name them."""
    wf = s.get("wireframe") or {}
    proto = wf.get("prototype") if isinstance(wf.get("prototype"), dict) else {}
    view_named = proto.get("match") == "partial" and str(proto.get("view") or "").strip()
    if wf.get("provenance") != "client-verified" or not (proto.get("match") == "exact" or view_named) \
            or not proto.get("file"):
        return "its layout is not an exact, client-verified prototype view, nor a partial one naming its view"
    text = (text_of or prototype_text)(proto["file"])
    if not text:
        return "its prototype file %s is not present to check against" % proto["file"]
    if not any(q + shown + q in text for q in ("'", '"')):
        return "%s does not hold %r as a quoted string" % (proto["file"], shown)
    return None


RULES = {
    "S-STATE-BOILERPLATE": "empty-state text promises a create action, filter or permission the screen lacks (R250)",
    "S-DUP-REGION": "a region name used twice on one screen (R253)",
    "S-OP-UNREACHED": "a declared operation no component, overlay or transition reaches (R273)",
    "S-SHOWN-BY": "an api's shownBy names text the screen's client-verified prototype (exact, or partial naming its "
                  "view) does not hold, or the screen's layout is no such prototype (CHG-R8INT-003, CHG-R8INT-008)",
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
    "S-MEDIA-LIBRARY": "a screen about the media a guest carries calls the digital-asset library (CF-114, CHG-WIR-025, CHG-R4-013)",
    "S-OFFLINE-REFUSED": "an offline app's screen refuses offline a write its contract marks offline-capable (4.4, CHG-SWP-004)",
    "S-OFFLINE-QUEUED": "a screen promises to queue a write that is not offline-capable, or a web app's screen queues (4.4, CHG-SWP-004)",
    "S-INPUT-SOURCE": "a guest screen's action needs an id nothing on the screen supplies (CR-142, CHG-CRA-008)",
}
# **Two things are called media** (glossary; orders.yaml `getMediaEntitlements`): the QR, wristband or card a
# guest carries, which orders and access read and write, and the images, video and documents of the asset
# library (`assets.yaml`), which shares the `/media` prefix and nothing else. A screen that reads or writes the
# first has no use for the second: BO-027 (2 October, CHG-WIR-025), POS-010 and EMP-036 "Issue media" (6 October,
# CHG-R4-013) each read an image-library asset where the guest's wristband was meant.
GUEST_MEDIA_OPS = {"getMediaEntitlements", "appendEntitlementToMedia", "setMediaBindingActivation",
                   "replaceCredential", "getEntitlementCredential"}
# **The staff surfaces.** A screen on one of these is operated by venue or platform staff, so every operation
# it calls must accept a staff caller. Added 2 October 2026 with the wiring fixes (CHG-WIR-001): guest-only
# reads (listMyCases, getLoyaltyPosition), device heartbeats and service-only writes had been bulk-attached to
# back-office, till and staff-app screens, where the call is refused or answers for the wrong principal.
# Partner (P10), accreditation-applicant (P11), developer (P14) and sign-up (P17) surfaces are not staff.
STAFF_CODES = ("P04", "P06", "P07", "P08", "P09", "P12", "P13", "P15", "P16")
STAFF_OK = {"staff", "public", "anonymous"}
# The TICVAI Console's tenant picker and platform-staff grant (audit R098, CHG-SBO-001): the frame every console
# screen acting in a tenant carries, left out of the duplicate-screen signature (S-DUP-SCREEN).
CONSOLE_FRAME = {"listTenants", "openPlatformStaffGrant", "listOwnPlatformStaffGrants"}
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
# CHG-SWP-004: a narrower promise (no "queue" the noun: "New queue calls arrive") and the words of a refusal.
QUEUE_PROMISE = re.compile(r"\b(queued|queues? (it|them|the|locally|offline|and)|kept and sent|sends? (it )?when|"
                           r"syncs?|on sync|works offline|saved locally|replay|outbox)\b", re.I)
OFFLINE_REFUSAL = re.compile(r"(not offered|not available|nothing here is offered|online only|\bdisabled\b|refused|"
                             r"cannot (be )?(open|done|made)|needs? (a |the )?(connection|network|server|gateway|primary)|"
                             r"requires? (a |the )?(connection|network|primary)|waits? for the connection|"
                             r"with the reason|connect to)", re.I)


def offline_here(op: dict, plat: str, sid: str) -> bool:
    """The write may queue on this screen (frontend-patterns 4.4, CHG-OFL-001): the contract marks it
    `x-ticvai-offline-capable: true`, this platform is in its `x-ticvai-offline-apps` where it lists any, and
    this screen is not in its `x-ticvai-offline-refused-on`."""
    if op.get("x-ticvai-offline-capable") is not True:
        return False
    apps = op.get("x-ticvai-offline-apps")
    if apps and str(plat)[:3] not in {str(a)[:3] for a in apps}:
        return False
    return sid not in set(op.get("x-ticvai-offline-refused-on") or [])


def required_body(op: dict) -> bool:
    rb = op.get("requestBody")
    if not isinstance(rb, dict):
        return False
    return bool(rb.get("required", False)) or "$ref" in rb


def overlay_refs(o: dict) -> set:
    """The operations an overlay reaches: its confirm's and dismiss's, and the reads it names in `reads` (CHG-R10UI-016):
    a picker inside a form is filled by a list read (SV-PICK, check-screen-value-sources), and an overlay has no
    component to carry that read's name, so it names it there and the read counts as reached (S-OP-UNREACHED)."""
    out = set()
    for k in ("confirm", "dismiss"):
        v = o.get(k)
        if isinstance(v, dict) and v.get("operation"):
            out.add(v["operation"])
    out |= {r for r in (o.get("reads") or []) if isinstance(r, str) and r}
    return out


def self_test():
    """shown_in_prototype on made-up screens (CHG-R8INT-008): exact and view-naming partial prototypes accept a
    quoted string they hold; a partial without a view, a generated layout and an absent string are refused."""
    files = {"p.html": "row('r3', '2 Jul', 'AED 675 \u00b7 refunded in full', 'Invoice')"}
    text_of = files.get

    def sc(match, view=None, prov="client-verified"):
        p = {"file": "p.html", "match": match}
        if view:
            p["view"] = view
        return {"wireframe": {"provenance": prov, "prototype": p}}
    cases = [
        ("exact, held", sc("exact"), "AED 675 \u00b7 refunded in full", True),
        ("partial naming its view, held", sc("partial", "Account > Order history"), "AED 675 \u00b7 refunded in full", True),
        ("partial without a view", sc("partial"), "AED 675 \u00b7 refunded in full", False),
        ("partial naming its view, not held", sc("partial", "Account"), "AED 999", False),
        ("generated layout", sc("exact", prov="generated"), "Invoice", False),
        ("none", sc("none", "x"), "Invoice", False),
    ]
    bad = []
    for name, s, shown, ok in cases:
        why = shown_in_prototype(s, shown, text_of)
        if (why is None) != ok:
            bad.append(f"shown_in_prototype: {name}: expected {'accepted' if ok else 'refused'}, got {why!r}")
    # an overlay reaches its confirm's operation and the picker reads it names (CHG-R10UI-016)
    form = {"id": "formConfigure", "confirm": {"operation": "configureWorkstation"}, "reads": ["listSaleBoards"]}
    if overlay_refs(form) != {"configureWorkstation", "listSaleBoards"}:
        bad.append(f"overlay_refs: a form's picker read is not reached: {overlay_refs(form)}")
    if overlay_refs({"id": "x", "confirm": {"label": "OK"}}) != set():
        bad.append("overlay_refs: an overlay with no operation reached something")
    return bad


def main() -> int:
    g.force_utf8()
    tests = self_test()
    for x in tests:
        print(f"  SELF-TEST  {x}")
    if tests:
        print(f"FAIL {len(tests)} self-test(s)")
        return 1
    if "--self-test" in sys.argv:
        print("PASS - the shownBy self-tests")
        return 0
    guard = g.Guard("check-screen-wiring", RULES)
    ops = g.operations()
    path_index = set()
    for f in ops.values():
        path_index.add((f["method"].upper(), re.sub(r"\{[^}]+\}", "{}", f["path"]).rstrip("/")))

    all_screens = g.screens()
    offline_platforms = {stem: bool(p.get("offlineCapable")) for stem, p in g.platforms().items()}
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
        # --- CHG-R4-013 guest media is not the asset library ------------------------------------
        if op_ids & GUEST_MEDIA_OPS:
            for o in sorted(op_ids):
                f = ops.get(o)
                if f and f.get("contract") == "assets":
                    guard.add("S-MEDIA-LIBRARY", f"{sid}:{o}",
                              f"{sid} ({plat}): {o} is the digital-asset library; this screen is about the media "
                              f"a guest carries ({', '.join(sorted(op_ids & GUEST_MEDIA_OPS))})")
        # --- R100 workstation operations off the till ------------------------------------------
        for o in sorted(op_ids):
            f = ops.get(o)
            # A workstation-scoped operation a guest may call in its own session (`x-ticvai-guest-callable`, CHG-GCF-003:
            # createPayment, inquirePaymentStatus) is the guest variant on a guest platform (CHG-SCR-012).
            if f and plat.startswith(GUEST_CODES) and f["op"].get("x-ticvai-guest-callable"):
                continue
            if f and f["op"].get("x-ticvai-scope-level") == "workstation" and plat not in ws_platforms:
                guard.add("S-WORKSTATION-OP", f"{sid}:{o}",
                          f"{sid} ({plat}): {o} is workstation-scoped and nothing on {plat} signs a workstation in")
        # --- R167 R289 guest surfaces ----------------------------------------------------------
        if plat.startswith(GUEST_CODES):
            for o in sorted(op_ids):
                f = ops.get(o)
                aud = (f or {}).get("op", {}).get("x-ticvai-audience") or []
                # The kiosk is a guest surface on a registered device: device operations are its own
                # (typed_props.DEVICE_GUEST_PLATFORMS; CHG-SCR-013).
                ok = {"guest", "public", "anonymous"} | ({"device"} if plat.startswith(DEVICE_GUEST_PLATFORMS) else set())
                if f and aud and not (ok & set(aud)) \
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
        # The console's grant frame is not the screen's job (CHG-SBO-001): it says nothing about whether two
        # screens duplicate each other, so it is left out of the signature.
        own_ops = op_ids - CONSOLE_FRAME
        if len(own_ops) >= 2:
            sigs.setdefault((plat, frozenset(own_ops)), []).append(sid)
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
            refs |= overlay_refs(o)
        for t in ((s.get("navigation") or {}).get("transitions") or []):
            if isinstance(t, dict) and t.get("operation"):
                refs.add(t["operation"])
        for a in apis:
            if a.get("shownBy"):
                why = shown_in_prototype(s, str(a["shownBy"]))
                if why:
                    guard.add("S-SHOWN-BY", f"{sid}:{a['operationId']}",
                              f"{sid}: {a['operationId']} shownBy {a['shownBy']!r}, but {why}")
                    continue
                refs.add(a["operationId"])
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
        # **Not on a guest surface** (2 October 2026, CHG-CLN-007): a guest holds no permission (ADR-0025), so a guest
        # screen has none to declare; its no-access state is "not signed in" or "not yours" (GFIX-4).
        if perms and "emptyNoAccess" in states and not s.get("permission") and not plat.startswith(GUEST_CODES):
            guard.add("S-SCREEN-PERMISSION", sid, f"{sid}: operations need {', '.join(sorted(perms)[:3])}"
                      f"{' ...' if len(perms) > 3 else ''}; the screen declares no permission")
        # --- R265 edits with no read -----------------------------------------------------------
        methods = {f["method"] for f in facts.values() if f}
        if methods & {"put", "patch"} and "get" not in methods \
                and not any(READ_LIKE.match(o) for o in facts):
            guard.add("S-NO-READ", sid, f"{sid}: edits a record ({', '.join(sorted(methods))}) and reads nothing")
        # --- R288 asynchronous operations ------------------------------------------------------
        gets = {o for o, f in facts.items() if f and f["method"] == "get"}
        # A shell beacon sent in the background (an append-only batch of events, `record...Events`) has nothing to
        # follow (Block A audit, 14 October 2026, CHG-SCR-011); every other 202 still needs its read.
        beacons = {a["operationId"] for a in apis if a.get("trigger") == "background"
                   and re.match(r"^record\w*Events$", a["operationId"])}
        for o, f in facts.items():
            if f and o not in beacons and "202" in {str(k) for k in (f["op"].get("responses") or {})}:
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
            # **A related record is not a wrong one** (Block A audit, 14 October 2026, CHG-SCR-014). The panel shows
            # another entity on purpose when its read needs no id the screen does not hold: the id comes from the
            # selected row (the reader's device, a shared wallet's balance) or from the screen itself (the rules
            # beside the performance they produce). It fails when the panel's read needs an id nothing gives it.
            panel_op = next((c.get("operation") for c in comps if c.get("kind") == "detailPanel"
                             and str(c.get("bindsTo") or "").replace("[]", "").split(".")[0] == panels[0]), None)
            table_props = set()
            for (st, n), node in by_schema.items():
                if n == tables[0]:
                    table_props |= set((node.get("properties") or {}).keys())
            held = table_props | {p.get("name") if isinstance(p, dict) else str(p)
                                  for p in ((s.get("entryState") or {}).get("params") or [])}
            needs = set(re.findall(r"\{(\w+)\}", (ops.get(panel_op) or {}).get("path", ""))) if panel_op else {"?"}
            if needs - held - {"id"}:
                guard.add("S-PANEL-ENTITY", sid, f"{sid}: the table shows {tables[0]}, the panel {panels[0]}")
        # --- R257 offline promises -------------------------------------------------------------
        off = str(states.get("offline") or "")
        if off and OFFLINE_PROMISE.search(off) and not OFFLINE_REFUSAL.search(off):
            writes = [o for o, f in facts.items() if f and f["method"] in WRITES]
            if writes and not any(offline_here(facts[o]["op"], plat, sid) for o in writes):
                guard.add("S-OFFLINE-CLAIM", sid,
                          f"{sid}: offline state promises to queue or sync and none of its "
                          f"{len(writes)} write(s) is x-ticvai-offline-capable")
        # --- CHG-SWP-004 offline writes against frontend-patterns 4.4 ---------------------------
        writes = [o for o, f in facts.items() if f and f["method"] in WRITES]
        capable = [o for o in writes if offline_here(facts[o]["op"], plat, sid)]
        offline_app = bool(offline_platforms.get(plat))
        refuses = bool(off and OFFLINE_REFUSAL.search(off))
        promises = bool(off and QUEUE_PROMISE.search(off))
        if offline_app and capable and (s.get("offline") is False or (refuses and not promises)):
            for o in capable:
                guard.add("S-OFFLINE-REFUSED", f"{sid}:{o}",
                          f"{sid} ({plat[:3]}): {o} is offline-capable (outbox, 4.4); the screen refuses it offline: "
                          + ("offline: false" if s.get("offline") is False else off[:100]))
        if promises and not refuses:
            if offline_app and capable:
                for o in writes:
                    # The outbox's own replay call (x-ticvai-outbox-replay: syncOrders) runs when the link is
                    # back; it is never queued and never "disabled offline" (CHG-OFL-002).
                    if o not in capable and o not in off and not facts[o]["op"].get("x-ticvai-outbox-replay"):
                        guard.add("S-OFFLINE-QUEUED", f"{sid}:{o}",
                                  f"{sid} ({plat[:3]}): offline state promises to queue or sync and does not say "
                                  f"{o} (not offline-capable) is disabled offline: {off[:90]}")
            elif not offline_app:
                for o in writes:
                    guard.add("S-OFFLINE-QUEUED", f"{sid}:{o}",
                              f"{sid} ({plat[:3]}): a web app has no offline store, and its offline state queues "
                              f"{o}: {off[:90]}")
    pairs = g.load_yaml(g.SCREENS / "_guest-pairs.yaml") or {}
    division = {s["id"]: bool(str(s.get("division") or "").strip()) for _, s in all_screens}
    for (plat, sig), ids in sorted(sigs.items(), key=lambda kv: kv[1]):
        # **A stated division is the answer** (Block A audit, 14 October 2026, CHG-SCR-009): screens are never merged
        # to clear this (client-approved UI); each member says what it is for (`division`, derive-screen-wiring.py).
        if len(ids) > 1 and not all(division.get(i) for i in ids):
            guard.add("S-DUP-SCREEN", "+".join(sorted(ids)),
                      f"{plat}: {', '.join(sorted(ids))} declare the same {len(sig)} operations")
    input_sources(guard, all_screens, ops, by_schema)
    return guard.finish()


# **A guest action needs every id it sends from somewhere on the screen** (class 14 of the 18 October triage,
# CHG-CRA-008). WEB-021's "Add a card" calls storePaymentToken, which requires providerId and consentPurposeId, and
# nothing on the web screen supplied either: GST-071, its twin in the app, had been bound to getPublishedTenantConfig
# and listConsentPurposes on 4 October (CHG-FXS-003) and the web screen was not (ADAM CR-142). A guest cannot type an
# id, so an id-typed required input of an onAction operation needs a source: an entry parameter of that name, a field
# of that name in what a single-record read on the screen returns, a read on the screen whose response is the thing
# the id names (`consentPurposeId` <- `ConsentPurposeConfig`), or the guest's session.
GUEST_SCREEN = re.compile(r"^(WEB|GST|KSK)-")
SESSION_IDS = {"subjectId", "tenantId", "principalId", "venueId", "workstationId", "sessionId"}


def input_sources(guard, all_screens, ops, by_schema) -> None:
    def deref(node, stem, depth=0):
        while isinstance(node, dict) and "$ref" in node and depth < 8:
            m = re.match(r"^(?:\.\./)?(?:[\w-]+/)?([\w-]+)\.yaml#/components/schemas/(\w+)$", str(node["$ref"]))
            if m:
                stem, node = m.group(1), by_schema.get((m.group(1), m.group(2))) or {}
            else:
                node = by_schema.get((stem, g.ref_name(str(node["$ref"])))) or {}
            depth += 1
        return node, stem

    def walk(node, stem, depth, fields, names):
        if not isinstance(node, dict) or depth > 5:
            return
        if "$ref" in node:
            names.add(g.ref_name(str(node["$ref"])).lower())
            node, stem = deref(node, stem)
        for k in ("allOf", "oneOf", "anyOf"):
            for sub in node.get(k) or []:
                walk(sub, stem, depth + 1, fields, names)
        if isinstance(node.get("items"), dict):
            walk(node["items"], stem, depth + 1, fields, names)
        for p, ps in (node.get("properties") or {}).items():
            fields.add(p)
            walk(ps, stem, depth + 1, fields, names)

    for plat, s in all_screens:
        sid = s.get("id", "")
        if not GUEST_SCREEN.match(sid):
            continue
        apis = [a for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId") in ops]
        have = set(SESSION_IDS) | {p.get("name") for p in ((s.get("entryState") or {}).get("params") or [])
                                   if isinstance(p, dict)}
        kinds: set = set()
        answers: dict = {}   # every operation on the screen -> the fields its 2xx responses carry, list rows included
        for a in apis:
            f = ops[a["operationId"]]
            for code, r in (f["op"].get("responses") or {}).items():
                if not str(code).startswith("2") or not isinstance(r, dict):
                    continue
                for media in (r.get("content") or {}).values():
                    fields, names = set(), set()
                    walk((media or {}).get("schema") or {}, f["contract"], 0, fields, names)
                    answers.setdefault(a["operationId"], set()).update(fields)
                    if f["method"] != "get" and a.get("trigger") != "onLoad":
                        continue
                    kinds |= names
                    if not a["operationId"].startswith("list"):   # a list's fields belong to whichever row is picked
                        have |= fields
        for a in apis:
            if a.get("trigger") != "onAction":
                continue
            f = ops[a["operationId"]]
            need = re.findall(r"\{(\w+)\}", f.get("path") or "")
            rb = ((f["op"].get("requestBody") or {}).get("content") or {}).get("application/json") or {}
            body, bst = deref(rb.get("schema") or {}, f["contract"])
            req = set((body or {}).get("required") or [])
            for b in (body or {}).get("allOf") or []:
                req |= set((deref(b, bst)[0] or {}).get("required") or [])
            need += [r for r in sorted(req) if r.endswith(("Id", "Code")) and r not in need]
            named = a.get("inputSources") if isinstance(a.get("inputSources"), dict) else {}
            for n in need:
                thing = re.sub(r"(Id|Code)$", "", n).lower()
                if n in have or (thing and any(thing in k for k in kinds)):
                    continue
                # The screen names the source (inputSources, 29 October 2026): a list's picked row, or what an earlier
                # write returns. Taken only when that operation is on the screen and its response has the field.
                src = str(named.get(n) or "")
                if src:
                    op_name, _, field = src.partition(".")
                    if field in answers.get(op_name, set()):
                        continue
                    guard.add("S-INPUT-SOURCE", f"{sid}:{a['operationId']}:{n}",
                              f"{sid} ({plat[:3]}): {a['operationId']} names {n}'s source as {src}, but "
                              + (f"{op_name} is not on the screen" if op_name not in answers
                                 else f"no 2xx response of {op_name} has {field}"))
                    continue
                guard.add("S-INPUT-SOURCE", f"{sid}:{a['operationId']}:{n}",
                          f"{sid} ({plat[:3]}): {a['operationId']} needs {n} and nothing on the screen supplies it "
                          f"(an entry parameter, a read's field, or a read of what it names)")


if __name__ == "__main__":
    sys.exit(main())
