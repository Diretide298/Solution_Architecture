#!/usr/bin/env python3
"""
Validate screen definitions.

Four checks, in order of how often they catch something:

  1. Component vocabulary — every `kind` exists in _components.yaml. A screen calling for a
     component that does not exist is either asking for something new (add it deliberately)
     or using a name the design system already has under a different label.

  2. operationIds resolve — every API referenced exists in the contracts. This is the check
     that catches a wireframe drawn against an imagined endpoint, which is the expensive
     failure: it survives design review, survives estimation, and is found at build.

  3. Four states — loading, empty and error on every screen; offline where the platform is
     offline-capable. The empty state is the one that reaches production unconsidered.

  4. Navigation resolves — every entryFrom and exitTo points at a screen that exists.
  5. Platform naming holds together — audience, form factor, surface and runtime must agree,
     and a POS or handheld must be offline-capable.
  5. Platform naming holds together — audience, form factor, surface and runtime must agree,
     and a POS or handheld must be offline-capable.

Run: python3 tools/check-screens.py
"""
import sys
from pathlib import Path

import json
import re
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
# The shipped `contracts/` is authoritative. Until 17 August these pointed at a sibling repo
# outside the package, so every validator passed for whoever had that repo checked out and read
# nothing for anyone working from the zip — which is the worst failure a checker can have, because
# it is silent and it looks like success.
CONTRACTS = ROOT / "contracts"
if not CONTRACTS.exists():
    CONTRACTS = ROOT.parent / "ticvai" / "ticvai-contracts" / "openapi"
if not CONTRACTS.exists():
    CONTRACTS = ROOT / "contracts"

ERRORS: list[str] = []
WARNINGS: list[str] = []


def load_vocabulary() -> tuple[set[str], set[str]]:
    doc = yaml.safe_load((SCREENS / "_components.yaml").read_text(encoding="utf-8"))
    return ({c["kind"] for c in doc.get("components", [])},
            {r["id"] for r in doc.get("regions", [])})


# **A screen whose only operation was read off its own title declares nothing.** 423 screens
# hold exactly one operation, it begins `list`, and every word after `list` comes from the
# screen's own name — `BO-233 Operations Audit, Shift Handover & Summary` declaring only
# `listShiftHandoverSummary`. The title promises a handover; the declaration can only fetch rows.
#
# **The stamp is a property of five files, not of the package.** P08, P09, P10, P12 and P13 carry
# all 423 of them and the other ten platforms carry none — measured 8 September, and the same
# split Claude Design measured independently at a stricter threshold (360). So this ships
# *enforcing* where the count is zero and *warning* where the re-signature work is outstanding.
# **A check that can only warn everywhere is a check nobody fixes.**
STAMP_WARN_ONLY = {"P08", "P09", "P10", "P12", "P13"}

# The publish family, as ADR-less vocabulary: what `publishGate.requiredWhen` actually means.
PUBLISHES = re.compile(r"^(publish|deploy|promote|activate)[A-Z]")
_JOINING = {"and", "or", "the", "a", "an", "of", "for", "to", "with", "in", "on", "by"}


def _singular(word: str) -> str:
    return word[:-1] if len(word) > 3 and word.endswith("s") and not word.endswith("ss") else word


def title_stamped(name: str, ops: list[str]) -> bool:
    """True when the screen's one operation is its own title with `list` in front."""
    if len(ops) != 1 or not ops[0].startswith("list"):
        return False
    stem = {_singular(w.lower())
            for w in re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])", ops[0][4:])}
    title = {_singular(w.lower()) for w in re.split(r"[^A-Za-z0-9]+", name)
             if w and w.lower() not in _JOINING}
    return bool(stem) and stem <= title


def load_wireframe_schema() -> tuple[set[str], dict[str, set[str]]]:
    """Allowed keys and enums for the `wireframe` block, read from `_schema.yaml`.

    **`_schema.yaml` was documentation and nothing read it.** The wireframe block declared four
    fields, carried seven, and every one of the 1,091 `status` values was outside its own enum —
    which is a block nothing validates, so the schema drifted from the files for as long as
    anybody had been writing to it. Reading the schema here is the point: a rule with its own
    hardcoded copy of the vocabulary drifts the same way.
    """
    doc = yaml.safe_load((SCREENS / "_schema.yaml").read_text(encoding="utf-8"))
    node = doc
    for step in ("properties", "screens", "items", "properties", "wireframe"):
        node = (node or {}).get(step) or {}
    props = node.get("properties") or {}
    enums = {k: set(v["enum"]) for k, v in props.items() if isinstance(v, dict) and v.get("enum")}
    closed = node.get("additionalProperties") is False
    return (set(props) if closed else set()), enums


def load_id_pattern() -> "re.Pattern | None":
    """The screen `id` pattern, read from `_schema.yaml`.

    **The second unenforced rule in the same file.** It read `^[A-Z]{3}-[0-9]{3}$` until
    8 September, and all 363 `BO-` screens failed it — on the field `board-data.js`, the
    traceability map and every board anchor join on. Nobody noticed because nothing read the
    schema.
    """
    doc = yaml.safe_load((SCREENS / "_schema.yaml").read_text(encoding="utf-8"))
    node = doc
    for step in ("properties", "screens", "items", "properties", "id"):
        node = (node or {}).get(step) or {}
    pat = node.get("pattern") if isinstance(node, dict) else None
    return re.compile(pat) if pat else None


def load_template_enum() -> set:
    """The `layout.template` enum, read from `_schema.yaml`.

    **The third unenforced rule in the same file, found by Claude Design on 9 September.**
    `BO-096 Resource Calendar` declares `template: calendar`, which is not one of the ten the
    schema allows — the only one of 1,083 templates outside its own enum — and it passed every
    check because **nothing read the enum.** Design reported it as a CI failure; it was the
    opposite, a rule that does not exist.

    Three rules in one file drifted the same way and were found one at a time. The pattern is not
    the field, it is that **`_schema.yaml` describes the format and only the checker enforces it**,
    so anything declared there and unread here is a document rather than a constraint.
    """
    doc = yaml.safe_load((SCREENS / "_schema.yaml").read_text(encoding="utf-8"))
    node = doc
    for step in ("properties", "screens", "items", "properties", "layout",
                 "properties", "template"):
        node = (node or {}).get(step) or {}
    return set(node.get("enum") or []) if isinstance(node, dict) else set()


OP_PATHS: dict = {}
OP_CONTRACT: dict = {}
CONTRACT_MODULE = {
    "orders": "ticketing", "catalogue": "ticketing", "promotions": "ticketing",
    "access": "access", "fnb": "fnb", "retail": "retail", "inventory": "inventory",
    "seating": "seating", "venue-map": "seating", "subscription": "membership",
    "marketing-crm": "marketing", "resources": "resources", "queue": "queue",
    "games": "games", "maintenance": "maintenance", "reporting": "analytics",
    "ai": "ai", "public-api": "developerApi",
}


PERMISSION_KEYS: set = set()
NAV_KEYS: set = set()
TR_KEYS: set = set()
TR_REQUIRED: set = set()
SCREEN_ANCHORS: dict = {}
NAV_SETS: set = set()
_USES_SEEN: set = set()

# A drawer, a sheet and a modal carry ids; a button does not. `control` is `kind#id`, and only
# the overlay kinds can have the id half resolved.
OVERLAY_KINDS = ("drawer", "sheet", "modal", "confirmDialog", "toast")


def load_permission_keys() -> set:
    """Every permission key any role grants, from `roles.yaml`.

    **The registry `transitions[].guard` joins on.** A guard naming a key no role grants is a
    control nobody can ever use, which looks identical to a control everybody can use until
    somebody tries it in production.
    """
    p = ROOT / "roles.yaml"
    if not p.exists():
        return set()
    doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    keys = set()
    for role in (doc.get("roles") or {}).values():
        for g in (role.get("grants") or []):
            keys.add(g if isinstance(g, str) else (g or {}).get("key"))
    return {k for k in keys if k}


def load_navigation_schema():
    """Allowed keys for `navigation` and for one `transitions[]` entry, from `_schema.yaml`.

    **Six of the navigation block's nine keys were undeclared while 1,091 screens used them** —
    `inferred`, `notes`, `fromFlows`, `uses`, `transitions`, `flowDerived`. The block is closed in
    the schema now and this is what reads that. Same shape as `load_wireframe_schema`: the enum
    lives in the schema, the enforcement lives here, and neither is any use without the other.
    """
    doc = yaml.safe_load((SCREENS / "_schema.yaml").read_text(encoding="utf-8"))
    nav = doc["properties"]["screens"]["items"]["properties"]["navigation"]
    tr = (nav.get("properties") or {}).get("transitions", {}).get("items", {})
    nav_keys = set(nav.get("properties") or ()) if nav.get("additionalProperties") is False else set()
    tr_keys = set(tr.get("properties") or ()) if tr.get("additionalProperties") is False else set()
    return nav_keys, tr_keys, set(tr.get("required") or ())


def _target(name: str, where: str, field: str, value: str, all_ids: set) -> None:
    """`SCREEN` or `SCREEN#anchor` — the screen must exist, the anchor should resolve."""
    base, _, anch = str(value).partition("#")
    if base not in all_ids:
        ERRORS.append(f"{name}: {where} {field} points at {base!r}, which is not a screen in the "
                      f"package — a transition to nowhere")
        return
    if anch and anch not in SCREEN_ANCHORS.get(base, set()):
        # **Not an error yet.** `machine` (the process vocabulary) is Phase 0 §2.2 and unbuilt,
        # so a failure path naming `paymentUnknown` is a forward reference rather than a mistake.
        # It becomes an error the day `machine` ships and these can be resolved against it.
        WARNINGS.append(f"{name}: {where} {field} is {value!r} and {anch!r} is neither a declared "
                        f"state nor an overlay on {base} — it lands nowhere until `machine` "
                        f"(plan §2.2) declares it")


def check_machine(name: str, screen: dict, all_ids: set) -> None:
    """The step state a screen holds, and whether it is a machine or just a list of words.

    **A state nothing transitions into is unreachable** — usually a rename that only got done in
    half the places. **A transition naming an undeclared state is a dead edge.** Neither shows up
    in a rendering, which is why both were free to accumulate in the prototype's JavaScript.
    """
    m = screen.get("machine")
    if not m:
        return
    sid = screen["id"]
    states = m.get("states") or {}
    if not states:
        ERRORS.append(f"{name}: {sid} machine {m.get('key')!r} declares no states")
        return

    if m.get("initial") not in states:
        ERRORS.append(f"{name}: {sid} machine initial {m.get('initial')!r} is not one of its own "
                      f"states {sorted(states)}")

    own_ops = {a.get("operationId") for a in (screen.get("apis") or [])}
    for sname, sv in states.items():
        sv = sv or {}
        op = sv.get("operation")
        if op and op not in own_ops:
            ERRORS.append(f"{name}: {sid} machine state {sname!r} runs {op!r}, which is not in "
                          f"the screen's own apis[]")
        for field in ("goes", "retryTo"):
            v = sv.get(field)
            if not v:
                continue
            if field == "retryTo":
                if v not in states:
                    ERRORS.append(f"{name}: {sid} machine state {sname!r} retries to {v!r}, "
                                  f"which is not a declared state")
            else:
                _target(name, f"{sid} machine.{sname}", field, v, all_ids)

    reached = {m.get("initial")}
    for i, t in enumerate(m.get("transitions") or []):
        where = f"{sid} machine.transitions[{i}]"
        for end in ("from", "to"):
            if t.get(end) not in states:
                ERRORS.append(f"{name}: {where} {end} is {t.get(end)!r}, which is not a declared "
                              f"state of {m.get('key')!r}")
        reached.add(t.get("to"))

    # A terminal state is allowed to have no way out; anything else with no way in is a mistake.
    for sname in states:
        if sname not in reached:
            ERRORS.append(f"{name}: {sid} machine state {sname!r} is unreachable — no transition "
                          f"arrives at it and it is not the initial state")


def check_overlay_returns(name: str, screen: dict, all_ids: set) -> None:
    """**What closing an overlay does.** 199 of them said what opens it and none said this."""
    sid = screen["id"]
    own_ops = {a.get("operationId") for a in (screen.get("apis") or [])}
    for o in (screen.get("overlays") or []):
        for half in ("confirm", "dismiss"):
            block = o.get(half)
            if not block:
                continue
            where = f"{sid} overlay {o.get('id')!r} {half}"
            if block.get("to"):
                _target(name, where, "to", block["to"], all_ids)
            op = block.get("operation")
            if op and op not in own_ops:
                ERRORS.append(f"{name}: {where} calls {op!r}, which is not in the screen's own "
                              f"apis[]")


def check_navigation(name: str, screen: dict, all_ids: set, kinds: set) -> None:
    """The navigation block, and every labelled transition in it.

    **The schema has been caught four times carrying rules nothing read** — `wireframe.status`,
    the `id` pattern, `layout.template`, and now the whole navigation block. Every field the
    transitions vocabulary declares is checked here, in the same change that declared it.
    """
    sid = screen["id"]
    nav = screen.get("navigation") or {}
    if not nav:
        return

    for k in nav:
        if NAV_KEYS and k not in NAV_KEYS:
            ERRORS.append(f"{name}: {sid} navigation declares {k!r}, which the schema does not — "
                          f"the block is closed, so this is a typo or a field somebody forgot to "
                          f"declare, and either way nothing reads it")

    for u in (nav.get("uses") or []):
        if u not in NAV_SETS and u not in _USES_SEEN:
            _USES_SEEN.add(u)
            WARNINGS.append(f"{name}: navigation.uses names the shared set {u!r} and no file in "
                            f"the package defines it — declare the set or drop the key; a pointer "
                            f"to nothing reads like a fact")

    transitions = nav.get("transitions") or []
    if not transitions:
        return

    own_ops = {a.get("operationId") for a in (screen.get("apis") or [])}
    own_overlays = {o.get("id") for o in (screen.get("overlays") or [])}
    own_kinds = {c.get("kind")
                 for r in ((screen.get("layout") or {}).get("regions") or [])
                 for c in (r.get("components") or [])}
    has_denied = bool((screen.get("states") or {}).get("denied"))

    labelled = set()
    for i, t in enumerate(transitions):
        where = f"{sid} transitions[{i}]"
        if not isinstance(t, dict):
            ERRORS.append(f"{name}: {where} is not a mapping")
            continue

        for k in t:
            if TR_KEYS and k not in TR_KEYS:
                ERRORS.append(f"{name}: {where} declares {k!r}, which the transitions vocabulary "
                              f"does not")
        for k in sorted(TR_REQUIRED):
            if not t.get(k):
                ERRORS.append(f"{name}: {where} has no {k!r} — required")

        if t.get("to"):
            labelled.add(str(t["to"]).partition("#")[0])
            _target(name, where, "to", t["to"], all_ids)
        if t.get("returnsTo"):
            _target(name, where, "returnsTo", t["returnsTo"], all_ids)
        for j, f in enumerate(t.get("onFailure") or []):
            if not isinstance(f, dict) or not f.get("to") or not f.get("when"):
                ERRORS.append(f"{name}: {where} onFailure[{j}] needs both 'when' and 'to'")
                continue
            _target(name, where, f"onFailure[{j}].to", f["to"], all_ids)

        op = t.get("operation")
        if op and op not in own_ops:
            ERRORS.append(f"{name}: {where} calls {op!r}, which is not in the screen's own apis[] "
                          f"— a transition cannot invoke an operation the screen does not declare")

        g = t.get("guard")
        if g:
            if PERMISSION_KEYS and g not in PERMISSION_KEYS:
                ERRORS.append(f"{name}: {where} is guarded by {g!r}, which no role in roles.yaml "
                              f"grants — a control nobody can ever use")
            elif not has_denied:
                # **The pairing that is the whole reason roles.yaml exists.** A move that can be
                # refused needs somewhere for the refusal to land.
                WARNINGS.append(f"{name}: {sid} has a {g!r}-gated transition and declares no "
                                f"states.denied — the refusal lands nowhere")

        c = t.get("control")
        if c:
            kind, _, anch = str(c).partition("#")
            if kinds and kind not in kinds:
                ERRORS.append(f"{name}: {where} control {c!r} names the kind {kind!r}, which is "
                              f"not in the component library")
            elif kind in OVERLAY_KINDS:
                if anch and anch not in own_overlays:
                    ERRORS.append(f"{name}: {where} control {c!r} names no overlay on {sid} — "
                                  f"declared overlays are {sorted(own_overlays) or 'none'}")
            elif own_kinds and kind not in own_kinds:
                WARNINGS.append(f"{name}: {where} control {c!r} names a {kind} and {sid} lays out "
                                f"no component of that kind")

    # **Coverage, but only where somebody has started.** A screen with no transitions at all is
    # unwritten, not wrong — 1,080 of 1,091 are in that state and warning about each says nothing.
    # A screen that labels some of its exits and not others is the one worth naming.
    unlabelled = [e for e in (nav.get("exitTo") or []) if e not in labelled]
    if unlabelled:
        WARNINGS.append(f"{name}: {sid} labels {len(labelled)} of "
                        f"{len(nav.get('exitTo') or [])} exits — no transition says how you reach "
                        f"{', '.join(sorted(unlabelled)[:6])}"
                        + (" and others" if len(unlabelled) > 6 else ""))


def load_operation_ids() -> set[str]:
    ops: set[str] = set()
    if not CONTRACTS.exists():
        return ops
    for f in CONTRACTS.rglob("*.yaml"):
        # **An unparseable contract used to be skipped in silence.** Its operations then looked
        # as though they did not exist, so every screen calling one failed and the report pointed
        # at the screens rather than at the one file that was broken. **A checker that misreports
        # where a fault is costs more than one that stops.**
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL  {f.name} does not parse: {exc}")
            raise SystemExit(1)
        for item in (doc.get("paths") or {}).values():
            if not isinstance(item, dict):
                continue
            for verb, op in item.items():
                if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                    if oid := op.get("operationId"):
                        ops.add(oid)
    return ops


# A platform's name should say what the thing is before what it is for: audience and form
# factor lead, purpose follows. "Guest App — Mobile", not "Guest Mobile App". These maps exist
# so the four fields cannot drift apart — surface and runtime are the older vocabulary and
# must keep agreeing with the newer one.
SURFACE_FOR = {"guest": "guestFacing", "staff": "staffFacing",
               "platformAdmin": "platformAdmin", "partner": "partner", "public": "public"}
RUNTIME_FOR = {"web": {"reactWeb"}, "mobileApp": {"reactNative"},
               "kiosk": {"reactWeb", "embedded"},
               "posTerminal": {"reactNativeTablet", "electron"}, "handheld": {"reactNative"}}
OFFLINE_REQUIRED = {"posTerminal", "handheld"}


SHORTNAMES: dict[str, str] = {}

# A guest or public surface may only call operations a guest can call. Enforced because a
# sibling-attachment pass on 17 August put 659 staff operations onto guest screens — including
# `applyManualDiscount` and `exchangeOrderLines` on a guest's own ticket list — and every other
# checker passed, because each operation existed and resolved to a table.
# P11 Accreditation is `public`, not `guest`. An external reviewer signs in from outside the
# organisation and holds a real permission — treating that surface as a guest surface is what
# produced `decideApprovalRequest` marked `x-ticvai-guest-callable` on 17 August, which reads as
# a guest approving their own refund. Public and guest are different audiences and the platform
# declares which it is.
GUEST_PLATFORMS = {"P01", "P02", "P05"}


def check_guest_operations(name: str, code: str, screen: dict, staff_ops: set[str]) -> None:
    if code not in GUEST_PLATFORMS:
        return
    for a in (screen.get("apis") or []):
        if (oid := a.get("operationId")) in staff_ops:
            ERRORS.append(f"{name}: {screen['id']} is a guest surface and declares '{oid}', "
                          "which carries a staff permission")


def check_platform(name: str, p: dict) -> None:
    """Also enforces that a shortName identifies exactly one platform.

    Three platforms were called "Staff Web" until 17 August — P08 back office, P12 support and
    P13 the CMS. A name that identifies three things identifies none, and it is the kind of
    collision that survives because each file is individually correct.
    """
    if sn := p.get("shortName"):
        if sn in SHORTNAMES and SHORTNAMES[sn] != p.get("code"):
            ERRORS.append(f"{name}: shortName '{sn}' is already used by "
                          f"{SHORTNAMES[sn]} — a name identifying two platforms identifies none")
        SHORTNAMES[sn] = p.get("code")

    for k in ("code", "audience", "formFactor", "shortName", "name"):
        if k not in p:
            ERRORS.append(f"{name}: platform is missing '{k}'")
            return

    if not p["name"].startswith(p["shortName"]):
        ERRORS.append(f"{name}: name '{p['name']}' does not lead with shortName "
                      f"'{p['shortName']}' — audience and form factor come first")

    expected = SURFACE_FOR.get(p["audience"])
    if expected and p.get("surface") != expected:
        ERRORS.append(f"{name}: surface '{p.get('surface')}' disagrees with audience "
                      f"'{p['audience']}' (expected '{expected}')")

    allowed = RUNTIME_FOR.get(p["formFactor"], set())
    if allowed and p.get("runtime") not in allowed:
        ERRORS.append(f"{name}: runtime '{p.get('runtime')}' is not valid for formFactor "
                      f"'{p['formFactor']}'")

    if p["formFactor"] in OFFLINE_REQUIRED and not p.get("offlineCapable"):
        ERRORS.append(f"{name}: a {p['formFactor']} must be offlineCapable — a gate that "
                      "cannot validate without a network is a queue (ADR-0013)")

    if p["formFactor"] == "web" and p.get("offlineCapable"):
        WARNINGS.append(f"{name}: a web surface declaring offlineCapable is unusual — confirm")


def check(path: Path, kinds: set[str], regions: set[str], ops: set[str], all_ids: set[str],
          wf_keys: set[str], wf_enums: dict[str, set[str]], id_pat, templates: set) -> None:
    name = path.name
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    check_platform(name, doc["platform"])
    offline_capable = doc["platform"].get("offlineCapable", False)

    seen: set[str] = set()
    for s in doc["screens"]:
        check_guest_operations(name, doc["platform"]["code"], s, STAFF_OPS)
        check_navigation(name, s, all_ids, kinds)
        check_machine(name, s, all_ids)
        check_overlay_returns(name, s, all_ids)
        sid = s["id"]
        if sid in seen:
            ERRORS.append(f"{name}: duplicate screen id {sid}")
        seen.add(sid)

        if id_pat and not id_pat.match(sid):
            ERRORS.append(f"{name}: screen id {sid!r} does not match the schema's own pattern "
                          f"{id_pat.pattern!r} — the id is what every other artefact joins on")

        # **A template outside the enum is a layout nothing knows how to render.** The deriver,
        # the viewer and every board generator switch on this value; an unknown one falls through
        # to whatever the default branch happens to be, silently.
        tmpl = (s.get("layout") or {}).get("template")
        if templates and tmpl and tmpl not in templates:
            ERRORS.append(f"{name}: {sid} declares layout.template {tmpl!r}, which _schema.yaml "
                          f"does not allow — one of {sorted(templates)}")

        # **The wireframe block, against its own schema.** Nothing validated this until
        # 8 September, and by then every screen in the package held an illegal `status`.
        wf = s.get("wireframe") or {}
        if wf_keys:
            for k in sorted(set(wf) - wf_keys):
                ERRORS.append(f"{name}: {sid} wireframe declares '{k}', which _schema.yaml "
                              f"does not — a field nothing declares is a field nothing reads")
        for k, allowed in wf_enums.items():
            if k in wf and wf[k] not in allowed:
                ERRORS.append(f"{name}: {sid} wireframe.{k} is '{wf[k]}', not one of "
                              f"{', '.join(sorted(allowed))}")
        # **A recorded gap is the thinking this rule demands.** The rule catches screens where the
        # single operation was read off the title and nobody noticed. A screen that names the
        # operation which *should* exist — `ACC-005` asking for `getAccreditationBadge` against a
        # list it is forced to use — has noticed, and failing it would teach people to delete the
        # gap rather than fix it.
        declared_gap = any(g.get("operation") for g in (s.get("gaps") or []))
        if not declared_gap and title_stamped(
                s["name"], [a.get("operationId") for a in (s.get("apis") or [])]):
            msg = (f"{name}: {sid} declares one operation and it is its own title with 'list' "
                   f"in front — the declaration was read off the name, so it is evidence of "
                   f"nothing about what the screen does")
            (WARNINGS if doc["platform"]["code"] in STAMP_WARN_ONLY else ERRORS).append(msg)

        # **A screen that publishes declares the gate.** `publishGate`'s `requiredWhen` keys off
        # the declared operation, not the screen's subject, which is what makes it checkable at
        # all — and it needs no `release*` exclusion since the seven hold-releasing operations
        # became `relinquish*` on 8 September. 35 screens declare a publish-family operation.
        #
        # **Enforcing since 8 September, and it took removing a screen's operations to get there.**
        # The last holdout was `PTR-010 Cart & Quote`, which declared `publishPromotion` and five
        # other promotion authoring verbs on a partner cart screen — the only P10 screen with any,
        # against a platform median of one operation per screen. **That was operation residue, not
        # a missing gate**, so the six `onAction` verbs were removed rather than the component
        # added: a reseller building a quote evaluates promotions, it does not author them. The
        # reads stayed. Every screen that publishes now declares the gate.
        gate_ops = [a.get("operationId") for a in (s.get("apis") or [])]
        if any(o and (PUBLISHES.match(o) or o == "releaseProductionPlan") for o in gate_ops):
            kinds_here = [c.get("kind")
                          for r in ((s.get("layout") or {}).get("regions") or [])
                          for c in (r.get("components") or [])]
            if "publishGate" not in kinds_here:
                ERRORS.append(f"{name}: {sid} declares an operation that publishes and has no "
                              f"publishGate — a publish with no stated consequence is one "
                              f"somebody presses meaning to save")

        if wf.get("status") in ("inProgress", "review", "approved") and not wf.get("board"):
            WARNINGS.append(f"{name}: {sid} claims design status '{wf['status']}' with no board "
                            f"— intent without a frame is a claim nothing backs")

        for region in (s.get("layout") or {}).get("regions", []):
            if (ref := region.get("ref")) and ref not in regions:
                ERRORS.append(f"{name}: {sid} references unknown region '{ref}'")
            for c in region.get("components", []):
                if (k := c.get("kind")) not in kinds:
                    ERRORS.append(f"{name}: {sid} uses unknown component '{k}'")

        for api in s.get("apis", []):
            oid = api.get("operationId")
            if oid == "TODO":
                WARNINGS.append(f"{name}: {sid} has a TODO operationId")
            elif ops and oid not in ops:
                ERRORS.append(f"{name}: {sid} references unknown operationId '{oid}'")

        # **`empty` became three states on 18 August.** One field held "nothing exists yet",
        # "your filter matched nothing" and "you may not see this", and they are three different
        # screens with three different actions. The permission case is the one that mattered —
        # **an empty list where the truth is a permission is a lie a person will act on.**
        #
        # **`emptyNoEvents` satisfies the same obligation, added 8 September.** The rule asked
        # for `emptyFirstRun` by name, so eleven audit trails declared *"the action is to create
        # the first entry"* — a screen offering to author its own evidence. The obligation is
        # that a screen says what an empty one means, not that it invites a first row.
        states = s.get("states") or {}
        empty_first = {"emptyFirstRun", "emptyNoEvents"}
        for required in ("loading", "emptyFirstRun", "error"):
            if required == "emptyFirstRun":
                if not (empty_first & set(states)):
                    ERRORS.append(f"{name}: {sid} declares neither emptyFirstRun nor "
                                  f"emptyNoEvents — an empty screen has to say which it is")
            elif required not in states:
                ERRORS.append(f"{name}: {sid} is missing the '{required}' state")
        if "empty" in states:
            ERRORS.append(f"{name}: {sid} still declares 'empty' — split it into emptyFirstRun, "
                          "emptyNoResults and emptyNoAccess")
        # A screen that filters must say what no-results looks like. A list with a search box and
        # one empty state tells a person their data is gone when their filter is just narrow.
        # Named \, not \ — the parameter is the vocabulary, and shadowing it
        # here made every component on every screen after the first read as unknown. 218 false
        # failures from one variable name.
        screen_kinds = {c.get("kind")
                        for region in (s.get("layout") or {}).get("regions", [])
                        for c in region.get("components", [])}
        if screen_kinds & {"dataTable", "cardList", "searchField", "timeline"} and "emptyNoResults" not in states:
            WARNINGS.append(f"{name}: {sid} lists or filters and declares no emptyNoResults")
        if offline_capable and "offline" not in states:
            ERRORS.append(f"{name}: {sid} is offline-capable but declares no offline state")
        # **Density follows formFactor, not the platform number.** Assigned by platform code on
        # 18 August, which put the handheld scanner on `compact` — a gate device held in one hand
        # while the other takes a ticket is not a desktop, and `formFactor` said so all along.
        want = {"web": "compact", "posTerminal": "touchLarge", "kiosk": "touchLarge",
                "mobileApp": "comfortable", "handheld": "comfortable",
                "wearable": "comfortable"}.get(doc["platform"].get("formFactor"))
        # **A platform's form factor sets the default, not the rule.** P15 is a web back office
        # and four of its sixty screens run on a kitchen display — a KDS bumped by somebody with
        # flour on their hands is `touchLarge` however it is served. A screen may override with a
        # reason; a screen that overrides silently may not.
        if s.get("densityReason"):
            want = None
        if want and s.get("density") != want:
            ERRORS.append(f"{name}: {sid} is density '{s.get('density')}' on a "
                          f"{doc['platform']['formFactor']} platform — expected '{want}'")
        if s.get("density") not in ("compact", "comfortable", "touchLarge"):
            ERRORS.append(f"{name}: {sid} declares no density — a back-office table and a kiosk "
                          "button grid are not one screen at two widths")
        # **A screen that needs a parameter must say where it comes from.** 280 screens called an
        # operation with a path parameter on 20 August and not one route declared it — raised as
        # *screens start abruptly, and what is already loaded is unstated*. `GST-013 Ticket
        # Details` called `getEntitlement(entitlementId)` on `/general/ticket-details`, so **the
        # screen could not know which ticket it was showing.**
        # **A screen that lists a collection may act on a member of it.** `ADM-001`, `PTR-001` and
        # `SUP-001` call `listActiveSessions` (`GET /auth/sessions`) and `forceLogout`
        # (`POST /auth/sessions/{sessionId}/force-logout`): the operator picks the session to
        # terminate off the list in front of them, and `SessionStatus` says why — one principal,
        # one active session per workstation, so signing in takes the till over. That `sessionId`
        # is **the other session's**, discovered on the screen, and was never an entry parameter.
        #
        # Requiring it as one forced a sign-in screen to be handed a session before it could
        # create one. The parameter is satisfied when the screen also calls the collection the
        # member hangs off — the path up to the `{param}` segment.
        screen_paths = {OP_PATHS.get(a.get("operationId"), "")
                        for a in (s.get("apis") or []) if isinstance(a, dict)}
        needed: set = set()
        for api in (s.get("apis") or []):
            path = OP_PATHS.get(api.get("operationId"), "")
            for param in re.findall(r"\{([a-zA-Z]+)\}", path):
                collection = path.split("/{" + param + "}")[0]
                if collection and collection in screen_paths:
                    continue
                needed.add(param)
        entry = s.get("entryState") or {}
        declared = {p.get("name") for p in (entry.get("params") or [])}
        if missing := sorted(needed - declared):
            ERRORS.append(f"{name}: {sid} calls operations needing {', '.join(missing)} and its "
                          "entryState declares none — the screen cannot know what it is showing")
        # A parameter arriving by deep link means the screen is reachable cold, and every one of
        # those can be opened three weeks late against something expired.
        if any(p.get("from") == "deepLink" for p in (entry.get("params") or [])):
            if not entry.get("coldEntry") or str(entry["coldEntry"]).startswith("TODO"):
                WARNINGS.append(f"{name}: {sid} can be reached cold by deep link and says nothing "
                                "about what it shows when the target is gone")

        # **A screen must not depend on a module its tenant did not buy.** Declared 24 August:
        # `requiresModule` joins a screen to `LicencePosition.licensedModules`, and until then a
        # tenant without an F&B licence was still served every F&B screen.
        #
        # **The failure this catches is not the declaration, it is the drift.** A screen declared
        # `ticketing` that quietly starts calling an F&B operation is a page that breaks for every
        # tenant who did not buy F&B — and it breaks in production, months later, for one customer.
        req_mod = s.get("requiresModule")
        if not req_mod:
            ERRORS.append(f"{name}: {sid} declares no requiresModule — a screen that cannot say "
                          "which module it belongs to cannot be hidden from a tenant who did not "
                          "buy it")
        elif req_mod != "core":
            reached = {CONTRACT_MODULE.get(OP_CONTRACT.get(a.get("operationId")), "core")
                       for a in (s.get("apis") or [])}
            foreign = sorted(m for m in reached if m not in ("core", req_mod))
            if foreign:
                WARNINGS.append(f"{name}: {sid} requires '{req_mod}' and calls operations from "
                                f"{', '.join(foreign)} — a tenant with one licence and not the "
                                "other gets a broken page")

        if todo := [k for k, v in states.items() if str(v).startswith("TODO")]:
            WARNINGS.append(f"{name}: {sid} has TODO states — {', '.join(todo)}")
        if (s.get("purpose") or "").startswith("TODO"):
            WARNINGS.append(f"{name}: {sid} has no purpose written")

    for s in doc["screens"]:
        nav = s.get("navigation") or {}
        for direction in ("entryFrom", "exitTo"):
            for target in nav.get(direction, []):
                if target not in all_ids:
                    ERRORS.append(f"{name}: {s['id']} {direction} points at unknown screen {target}")

    declared = doc["platform"].get("screenCount")
    if declared is not None and declared != len(doc["screens"]):
        ERRORS.append(f"{name}: screenCount says {declared}, file has {len(doc['screens'])}")


def load_staff_operations() -> set[str]:
    """Operations carrying a staff permission. A guest surface may declare none of them."""
    out: set[str] = set()
    for tier in ("spine", "satellite"):
        d = CONTRACTS / tier
        if not d.exists():
            continue
        for f in d.glob("*.yaml"):
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
            for item in (doc.get("paths") or {}).values():
                if not isinstance(item, dict):
                    continue
                for verb, op in item.items():
                    if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                        # `x-ticvai-guest-callable` marks an operation a guest performs on
                        # their own data — createOrder, createPayment, acquireInventoryHold. The
                        # permission is for staff doing it on a guest's behalf at a till.
                        if op.get("x-ticvai-permission") and not "guest" in (op.get("x-ticvai-audience") or []):
                            out.add(op["operationId"])
    return out


STAFF_OPS: set[str] = set()


def check_reachability(files) -> None:
    """Every screen must be reachable from its platform's entry point.

    **1,421 navigation edges and 110 screens that cannot be reached** — asked about on 20 August,
    and nothing had checked it. Flows were counted at 45% while the graph they walk was never
    verified as a graph.

    `P08` is the case: **`BO-001 Queue Directory` is the declared entry point to a 99-screen back
    office**, it exits to four queue screens, and 93 screens hang off nothing. The back office has
    no home screen at all — the entry point was inferred, like 91 of its 99 navigation blocks, and
    inference picked the lowest-numbered screen.

    **`P14` declares no entry point, so all 8 of its screens are unreachable.**

    A warning rather than an error while `navigation.inferred` is still true across the estate:
    failing here would fail the package for a gap the screens plan already schedules as Phase 2.
    """
    scr: dict = {}
    by_plat: dict = {}
    for f in files:
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = doc["platform"]["code"]
        by_plat[code] = set()
        for s in doc["screens"]:
            scr[s["id"]] = s
            by_plat[code].add(s["id"])

    out: dict = {}
    for sid, s in scr.items():
        nav = s.get("navigation") or {}
        for t in (nav.get("exitTo") or []):
            if t in scr:
                out.setdefault(sid, set()).add(t)
        for t in (nav.get("entryFrom") or []):
            if t in scr:
                out.setdefault(t, set()).add(sid)

    # **Two screens on one platform with the same name.** Not an error — `F&B Order Management`
    # is BO-020 and BO-047 and has been since before the packs arrived, and which of the two
    # should survive is a question for a person. But it needs saying: a navigation menu with the
    # same entry twice is indistinguishable from a bug, and after the 9 September books landed
    # 140 pack screens this became the only way a collision would surface — the redundancy pass
    # compares operation sets, and a screen with no operations collides with nothing.
    for code, ids in sorted(by_plat.items()):
        same: dict[str, list[str]] = {}
        for i in sorted(ids):
            key = re.sub(r"[^a-z0-9]+", " ", scr[i]["name"].lower()).strip()
            same.setdefault(key, []).append(i)
        for key, dupes in sorted(same.items()):
            if len(dupes) > 1:
                WARNINGS.append(
                    f"{code}: {' and '.join(dupes)} are both named "
                    f"'{scr[dupes[0]]['name']}' — one of them is the other under a second id, "
                    f"or the name is wrong on one")

    for code, ids in sorted(by_plat.items()):
        entries = {i for i in ids
                   if (scr[i].get("navigation") or {}).get("isEntryPoint")}
        if not entries:
            WARNINGS.append(f"{code}: no screen declares isEntryPoint — every one of its "
                            f"{len(ids)} screens is unreachable")
            continue
        seen, frontier = set(entries), list(entries)
        while frontier:
            nxt = []
            for t in frontier:
                for u in out.get(t, set()) & ids:
                    if u not in seen:
                        seen.add(u)
                        nxt.append(u)
            frontier = nxt
        stranded = sorted(ids - seen)
        if stranded:
            WARNINGS.append(
                f"{code}: {len(stranded)} screen(s) cannot be reached from "
                f"{', '.join(sorted(entries))} — {', '.join(stranded[:5])}"
                + (" …" if len(stranded) > 5 else ""))


def main() -> int:
    global STAFF_OPS, PERMISSION_KEYS, NAV_KEYS, TR_KEYS, TR_REQUIRED
    STAFF_OPS = load_staff_operations()
    PERMISSION_KEYS = load_permission_keys()
    NAV_KEYS, TR_KEYS, TR_REQUIRED = load_navigation_schema()
    files = sorted(SCREENS.glob("P*.yaml"))
    if not files:
        print("no platform files found", file=sys.stderr)
        return 1

    kinds, regions = load_vocabulary()
    wf_keys, wf_enums = load_wireframe_schema()
    id_pat = load_id_pattern()
    templates = load_template_enum()
    ops = load_operation_ids()
    lin_path = ROOT / "handoff" / "api-data-lineage.json"
    if lin_path.exists():
        for oid, v in json.loads(lin_path.read_text(encoding="utf-8")).items():
            OP_PATHS[oid] = v.get("path", "")
            OP_CONTRACT[oid] = v.get("contract", "")
    all_ids = {s["id"] for f in files for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]}
    # Anchors a `to` may point into: the rendering states a screen declares, and its overlays.
    for f in files:
        for sc in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            SCREEN_ANCHORS[sc["id"]] = (set(sc.get("states") or {})
                                        | {o.get("id") for o in (sc.get("overlays") or [])}
                                        | set(((sc.get("machine") or {}).get("states") or {})))

    print(f"checking {len(files)} platform(s)")
    print(f"  {len(kinds)} component kinds, {len(regions)} regions, {len(ops)} operationIds\n")
    if not ops:
        WARNINGS.append("contracts not found alongside — operationId checking skipped")

    check_reachability(files)

    total = 0
    for f in files:
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        total += len(doc["screens"])
        check(f, kinds, regions, ops, all_ids, wf_keys, wf_enums, id_pat, templates)
        print(f"  {doc['platform']['code']}  {doc['platform']['name']:30} {len(doc['screens']):>3} screens")

    print(f"\n  {'':36} {total:>3} total\n")
    # **A region that declares itself and puts nothing in it says nothing about being empty.**
    # Two of 511 are like this and both are correct — `POS-001 statusStrip` renders from
    # `getCurrentShift`, `POS-002 sideNav` from the catalogue bundle. **Declaring components in
    # either would be declaring the same thing twice, and the second copy is the one that goes
    # stale.**
    #
    # **So the warning is about the silence, not the emptiness.** A plain "region is empty" gets
    # answered with filler components; this one is closed by a sentence saying what fills it, and
    # the screen view prints that note where the doubt used to be.
    #
    # `notes` rather than a new keyword — a component already has one, and no region in the package
    # carried one before 24 August, so nothing is silenced by accident.
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for sc in doc.get("screens") or []:
            layout = sc.get("layout") or {}
            for reg in layout.get("regions") or []:
                if (reg.get("components") or []) or reg.get("notes"):
                    continue
                WARNINGS.append(
                    f"{sc['id']} declares region {reg.get('name')} and puts nothing in it on the "
                    f"{layout.get('template')} template, and says nothing about why — add "
                    "components, or a note saying what fills it")

    # **A platform's audience and its operations' audiences have to agree.** `WEB-016 Login /
    # Register` — a guest surface — was calling six staff-only MFA operations, `selectRole` (ADR-0002
    # staff authorisation) and the staff session. **Nothing checked it**, because every existing
    # check ran from the operation outward: does it exist, does it resolve, is it permitted. None
    # ran from the platform inward asking whether this surface should be calling it at all.
    #
    # **The permission check does not cover this.** An operation with no permission passes it, and
    # `createParkingEntitlement` is `service` audience with no permission — a guest screen calling
    # a service-to-service operation looks clean to every other rule here.
    OPEN = {"public", "anonymous", "service"}
    _lin = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8")) \
        if (ROOT / "handoff" / "api-data-lineage.json").exists() else {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        _pa = (doc.get("platform") or {}).get("audience")
        for sc in doc.get("screens") or []:
            # **A screen may declare its own audience and override the platform.** DEV-008 is
            # Softlabs administering the developer programme on a partner portal; KSK-013 is the
            # kiosk raising a staff call on a guest surface. Both are correct and both looked like
            # violations until the screen could say so.
            pa = sc.get("audience") or _pa
            if pa not in ("guest", "partner"):
                continue
            for api in (sc.get("apis") or []):
                oid = api.get("operationId")
                oa = set((_lin.get(oid) or {}).get("audience") or [])
                if not oa or (oa & ({pa} | OPEN)):
                    continue
                WARNINGS.append(
                    f"{sc['id']} is a {pa} surface and calls '{oid}', which is declared "
                    f"{sorted(oa)} — either the audience is wrong or this surface should not "
                    "reach that operation")

    # **The offline model was prose on one side and a flag on the other, and nothing compared
    # them.** 190 screens describe offline behaviour; 173 operations declared the flag. A screen
    # said *"Selling continues from the cached menu"* while every operation it loaded was
    # `offline: false` — **and both statements passed every check in this suite**, because none had
    # ever read one against the other.
    #
    # **What breaks: a till goes offline on a Saturday, the screen renders empty, and the cashier
    # reads a design document that promised it would work.**
    #
    # The check is deliberately narrow. It fires only when the prose *claims continued function* —
    # a screen saying "not available offline" is correct and silent. **The flag now means two
    # things and both are legitimate**: servable from cache on a read, callable while offline on a
    # write.
    CLAIMS = re.compile(
        r"keeps working|continues|works from|from the (cached|local)|still (works|takes|sells)|"
        r"local journal|sells from|selling continues", re.I)
    DENIES = re.compile(r"not available|refused|requires the primary|cannot|does not work", re.I)
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for sc in doc.get("screens") or []:
            text = str((sc.get("states") or {}).get("offline") or "")
            if not text or DENIES.search(text[:80]) or not CLAIMS.search(text):
                continue
            loads = [a.get("operationId") for a in (sc.get("apis") or [])
                     if a.get("trigger") == "onLoad" and a.get("operationId") in _lin]
            if loads and not any(_lin[o].get("offline") for o in loads):
                WARNINGS.append(
                    f"{sc['id']} says it keeps working offline and not one of its onLoad "
                    f"operations is offline-capable ({', '.join(loads[:3])}) — the screen renders "
                    "empty on the day the prose is about")

    # **Two guest surfaces drawing one journey must not diverge silently.** P01 Guest Web and P02
    # Guest App had thirteen identically-named screen pairs, and `Loyalty & Rewards` shared *zero*
    # of nine operations across them — the same name, the same journey, and one side could not do
    # what the other could.
    #
    # **A guest does not know which surface they are on.** They opened a link, or they installed an
    # app, and the ticket is the same ticket. A divergence is either a defect or a decision, and
    # only one of those should be silent.
    #
    # Guest-callable operations only: a web screen legitimately lacks a device-audience operation,
    # and demanding parity on those would report the platform working correctly.
    _guest = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        if (doc.get("platform") or {}).get("audience") != "guest":
            continue
        code = doc["platform"]["code"]
        for sc in doc.get("screens") or []:
            ops = {a.get("operationId") for a in (sc.get("apis") or [])
                   if a.get("operationId") in _lin
                   and ({"guest", "public", "anonymous"} & set(_lin[a["operationId"]].get("audience") or []))}
            _guest.setdefault(sc["name"].strip().lower(), []).append((code, sc["id"], ops, sc))
    for name, group in sorted(_guest.items()):
        if len(group) < 2:
            continue
        base = set.union(*[g[2] for g in group])
        for code, sid, ops, sc in group:
            missing = sorted(base - ops)
            if not missing:
                continue
            if "parity" in str(sc.get("notes") or "").lower():
                continue
            WARNINGS.append(
                f"{sid} ({code}) and its counterpart share the name '{sc['name']}' and it cannot "
                f"call {', '.join(missing[:3])} — a guest does not know which surface they are on, "
                "so a divergence needs a note saying it is deliberate")

    # **A placeholder that renders is a placeholder that ships.** 124 screens carried
    # `module: TODO` — 59 of the 63 on P02 Guest App, every one on P10 Partner Web — and the
    # frontend drew them under a group heading reading *TODO* while P01 Guest Web beside it read
    # *Discovery & Browse* and *Booking & Selection*.
    #
    # **No checker looked at `module`.** It is a grouping label, not a join, so nothing resolved it
    # against anything and nothing complained. It was found by a person looking at two boards side
    # by side.
    #
    # `module` groups screens for a reader; `requiresModule` gates them by licence. **Two different
    # fields, and only the second had a check.**
    PLACEHOLDER = {"todo", "tbd", "fixme", "xxx", "none", "n/a", "", "-", "?"}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = (doc.get("platform") or {}).get("code", "")
        for sc in doc.get("screens") or []:
            grp = str(sc.get("module") or "").strip()
            if grp.lower() in PLACEHOLDER:
                WARNINGS.append(
                    f"{sc['id']} ({code}) has module group '{grp or 'unset'}' — a placeholder that "
                    "renders is a placeholder that ships, and this is the heading a reviewer reads "
                    "above the screen")

    # **A destructive button with no confirmation and no label is a button nobody can undo.**
    # `confirmDialog` and `modal` were both in the component library and used **zero times across
    # 492 screens**, while `destructiveButton` was used 39 times and its own library entry reads
    # *always requires confirmation*. **Seven of the 39 had a `null` label** — a red button that
    # cannot say what it destroys, and on `BO-033 Blacklist Management` and `ADM-007 Module &
    # Feature Entitlement` it was the only way to remove a record.
    #
    # **Found by a design review on 31 August, not by anything here** — the components derived
    # correctly from the operations and nobody asked what a destructive act needs beyond a button.
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = (doc.get("platform") or {}).get("code", "")
        for sc in doc.get("screens") or []:
            regions = (sc.get("layout") or {}).get("regions") or []
            comps = [c for r in regions for c in (r.get("components") or [])]
            kinds = {c.get("kind") for c in comps}
            if "destructiveButton" not in kinds:
                continue
            # **An overlay declared in `overlays` counts.** From 9 September a screen declares
            # its popups in a block of their own rather than as components in the layout, because
            # each one renders as its own wireframe frame — the screen with the dialog over it.
            # A rule that only reads `layout` would report every properly specified screen as
            # missing the confirmation it declares two lines further down.
            overlay_kinds = {o.get("component") for o in (sc.get("overlays") or [])}
            if not ({"confirmDialog", "modal"} & (kinds | overlay_kinds)):
                WARNINGS.append(
                    f"{sc['id']} ({code}) has a destructive button and no confirmDialog — the "
                    "component library says one always requires confirmation")
            for c in comps:
                if c.get("kind") == "destructiveButton" and not str(c.get("label") or "").strip():
                    WARNINGS.append(
                        f"{sc['id']} ({code}) has a destructive button with no label — a red "
                        "button that cannot say what it destroys")

    # **Coverage was only ever measured from the screen side.** Every check here asks whether a
    # screen's operations exist and whether the audiences agree. **None asked the inverse: is there
    # a screen for every operation a guest is allowed to call?**
    #
    # 51 were found by hand on 31 August, including `deleteGuestAccount` and `exportSubjectData` —
    # **two things a guest can legally demand under UAE data protection, with nowhere to demand
    # them from.** Also `createRefundRequest`, `createResaleListing` and `createCase`: a guest may
    # request a refund, resell a ticket and raise a complaint, and all three were back-office only.
    #
    # **A contract that says a guest may do something, and no surface where they can, is a promise
    # the package makes and the product does not keep.**
    #
    # Service-to-service operations are excluded by `x-ticvai-service-only`, which is a declaration
    # rather than an inference — an operation tagged `guest` and reachable from nowhere should have
    # to say so.
    _guest_ops = {o for o, v in _lin.items()
                  if {"guest", "public", "anonymous"} & set(v.get("audience") or [])
                  and not v.get("serviceOnly")}
    _on_guest_screen: set = set()
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        if (doc.get("platform") or {}).get("audience") != "guest":
            continue
        for sc in doc.get("screens") or []:
            _on_guest_screen |= {a.get("operationId") for a in (sc.get("apis") or [])}
    for _o in sorted(_guest_ops - _on_guest_screen):
        WARNINGS.append(
            f"{_o}: a guest may call it and no guest screen does — either a surface is missing or "
            "the audience is wrong")

    # ── a failure the platform recorded and nobody can see ──────────────────────────────────
    #
    # **The inverse of the guest-coverage check above.** That one asks whether a guest can reach
    # what a guest may call; this asks whether an operator can see what the platform dropped.
    #
    # Two tables failed it on the first run and they failed it differently, which is why the rule
    # tests the table rather than the operation. `platform.dead_letter` had `listDeadLetters` and
    # `replayDeadLetter` and no screen calling either. `ai.index_failure` had **no operation at
    # all** — a table specified, written up as "failure is a row somebody works, not a log line",
    # and unreachable from anywhere in the package.
    #
    # `events/_schema.yaml` is what makes this an obligation rather than a preference: **"a
    # dead-lettered critical event is a page, not a dashboard."** A page nobody built is the same
    # as no page.
    try:
        _lin = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        _lin = {}
    _failure_tables: set = set()
    for _c in sorted((ROOT / "contracts").rglob("*.yaml")):
        try:
            _doc = yaml.safe_load(_c.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        for _n, _sch in ((_doc.get("components") or {}).get("schemas") or {}).items():
            _t = (_sch or {}).get("x-ticvai-persistence")
            # Named for what it holds: a failure, a dead letter, a rejection, an exception.
            if _t and re.search(r"(failure|dead_letter|rejection|exception|error)s?$", str(_t)):
                _failure_tables.add(str(_t))
    _screen_ops: set = set()
    for f in files:
        _d = yaml.safe_load(f.read_text(encoding="utf-8"))
        for sc in _d.get("screens") or []:
            _screen_ops |= {a.get("operationId") for a in (sc.get("apis") or [])}
    # **Readers come from the contracts, not from the lineage.** `api-data-lineage.json` is read
    # by twenty tools as authoritative and NOTHING IN THIS PACKAGE REGENERATES IT — it arrives
    # with the dump. So an operation added to a contract is invisible to every lineage consumer
    # until the next drop, and this rule would report a table as unreachable while the operation
    # that reads it sits in the file next door. Derived here instead: an operation reads a table
    # if any schema it returns declares that table as its persistence.
    _persist_of: dict = {}
    _op_reads: dict = {}
    for _c in sorted((ROOT / "contracts").rglob("*.yaml")):
        try:
            _doc = yaml.safe_load(_c.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        _schemas = (_doc.get("components") or {}).get("schemas") or {}
        for _n, _sch in _schemas.items():
            _t = (_sch or {}).get("x-ticvai-persistence")
            if _t:
                _persist_of[_n] = str(_t)
        for _path, _item in (_doc.get("paths") or {}).items():
            for _verb, _op in (_item or {}).items():
                if not isinstance(_op, dict) or not _op.get("operationId"):
                    continue
                _refs = set(re.findall(r"#/components/schemas/([A-Za-z0-9_]+)",
                                       json.dumps(_op.get("responses") or {})))
                _tabs = {_persist_of[r] for r in _refs if r in _persist_of}
                if _tabs:
                    _op_reads.setdefault(_op["operationId"], set()).update(_tabs)
    for _t in sorted(_failure_tables):
        _readers = sorted({o for o, ts in _op_reads.items() if _t in ts}
                          | {o for o, v in _lin.items() if _t in (v.get("reads") or [])})
        if not _readers:
            WARNINGS.append(
                f"{_t}: a failure table no operation reads — the platform records it and nothing "
                "in the package can reach a single row")
        elif not (set(_readers) & _screen_ops):
            WARNINGS.append(
                f"{_t}: read by {sorted(_readers)} and no screen calls any of them — "
                "events/_schema.yaml says a dead-lettered critical event is a page, not a dashboard")

    # ── screen ids are issued, not calculated ───────────────────────────────────────────────
    #
    # **Two workstreams both took ADM-038 on 4 September.** Each computed max+1 over the screens
    # it could see, neither could see the other, and nothing held a number — so one 'Dead Letters'
    # and one 'Communication Service Command Center' were both correct and both wrong.
    #
    # `screens/_id-register.yaml` is the issue log that fixes it: **a number in that file is
    # spent.** An allocator starts above the highest number RECORDED rather than above the highest
    # it happens to have loaded, which is the difference between the two workstreams agreeing and
    # merely not overlapping yet.
    #
    # **A retired id is never reissued** — `nextFree` is the high-water mark plus one, gaps and
    # all. Reusing a deleted screen's number is how a link in a document opens the wrong screen.
    _reg_p = ROOT / "screens" / "_id-register.yaml"
    if _reg_p.exists():
        _reg = (yaml.safe_load(_reg_p.read_text(encoding="utf-8")) or {}).get("prefixes") or {}
        _live: dict = {}
        for f in files:
            _d = yaml.safe_load(f.read_text(encoding="utf-8"))
            for sc in _d.get("screens") or []:
                _live.setdefault(sc["id"].rsplit("-", 1)[0], []).append(int(sc["id"].rsplit("-", 1)[1]))
        for _pre, _nums in sorted(_live.items()):
            _rec = _reg.get(_pre)
            if not _rec:
                ERRORS.append(f"{_pre}-: prefix is not in screens/_id-register.yaml — register it "
                              "before issuing ids under it, or two workstreams will both claim the "
                              "same numbers")
                continue
            _over = sorted(n for n in _nums if n > _rec.get("highWaterMark", 0))
            if _over:
                ERRORS.append(
                    f"{_pre}-{_over[0]:03d}: issued above the register's high-water mark of "
                    f"{_rec.get('highWaterMark')} — run tools/derive-id-register.py --apply and "
                    "commit it in the same change, so the next allocator can see the number is spent")

    for w in WARNINGS:
        print(f"  WARN  {w}")
    for e in ERRORS:
        print(f"  FAIL  {e}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
