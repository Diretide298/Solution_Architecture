#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The typed properties of an operation, read once for the three checks that use them. Imported, no main.

**Council of 2 October 2026:** the "semantic" findings of the process agents were mostly missing types.
Three properties are declared on every operation, and a screen that binds the operation is checked
against them:

    audience       x-ticvai-audience: who may call it (guest, anonymous, public, staff, partner, device,
                   service). A guest screen binding a staff-only operation shows a guest staff data, or
                   fails; a till binding a guest-only operation is refused.     -> check-audience-match
    needs-session  the operation's effective `security` (its own, else its contract's): `[]` is public,
                   an alternative `{}` makes the credential optional, anything else needs one. A screen a
                   guest reaches before signing in cannot load with an operation that needs a session
                   (the storefront's theme read, 2 October).                    -> check-preauth-session
    subject        whether it acts on the caller (x-ticvai-self-scoped, or a null permission with no
                   parameter naming whom) or on a named customer. A till that calls the caller's own
                   loyalty read shows the cashier's loyalty (getLoyaltyPosition on POS-002). -> check-subject

Screens and contracts are read through `audit_guard` (the audit-class guards' plumbing), so these checks
see the package exactly as the other guards do.
"""
from __future__ import annotations

import re

import audit_guard as g

# A platform's audience, from its declared `operator` (the same mapping as tools/build-audience.py).
OPERATOR_AUDIENCE = {"guest": "guest", "venue": "staff", "ticvai": "staff", "partner": "partner",
                     "public": "public"}
# What a screen on a platform of that audience may call. A till is a device as well as a staff session.
CALLABLE_BY = {
    "guest": {"guest", "anonymous", "public"},
    "staff": {"staff", "device", "service", "anonymous", "public"},
}
# The kiosk (P05) is a guest surface running on a registered device: device operations are its own.
DEVICE_GUEST_PLATFORMS = ("P05",)


def callable_by(aud: str, code: str) -> set:
    ok = set(CALLABLE_BY.get(aud) or ())
    if aud == "guest" and code in DEVICE_GUEST_PLATFORMS:
        ok.add("device")
    return ok
GUEST_PLATFORMS = ("P01", "P02", "P05")          # the guest web, the guest app, the kiosk (design_spec.py)

# The identity a session issues. A screen that takes one of these from the session is behind sign-in.
SESSION_IDENTITY = {"subjectId", "sessionId", "principalId", "operatorId"}
# Operations that turn an anonymous caller into a known one (tools/check-session-entry.py).
SESSION_CREATORS = {"login", "verifyGuestOtp", "guestSocialLogin", "guestUaePassLogin"}
LOAD_TRIGGERS = {"onLoad", "onInterval", "background", None}
# A parameter that names whose record it is: the operation then acts on a named customer, not the caller.
# Resources owned by the session that opened them, whoever the caller is (decided 2 October 2026, CHG-SEED-013).
SESSION_OWNED = re.compile(r"^/carts(/|$)")
GUEST_PARAM = re.compile(r"^(subject|guest|customer|member)Id$")
SUBJECT_PARAM = re.compile(r"^(subject|guest|customer|member|account|holder|principal|person|profile)Id$")
INPUT_KINDS = {"selectField", "textField", "toggle", "numberField", "datePicker", "multiSelect",
               "searchField", "fileUpload", "consentBlock", "scanTarget", "seatMap"}
ACTION_KINDS = {"primaryButton", "secondaryButton", "destructiveButton", "iconButton", "publishGate",
                "confirmDialog"}


def operations() -> dict:
    return g.operations()


def audience(op_id: str) -> set:
    o = operations().get(op_id)
    if not o:
        return set()
    a = o["op"].get("x-ticvai-audience")
    if isinstance(a, str):
        a = [a]
    return {str(x) for x in (a or [])}


_DOC_SECURITY: dict = {}


def security(op_id: str):
    """The effective security requirement: the operation's own, else its contract's; None if neither says."""
    o = operations().get(op_id)
    if not o:
        return None
    if "security" in o["op"]:
        return o["op"]["security"]
    if not _DOC_SECURITY:
        for _stem, rel, doc in g.contracts():
            _DOC_SECURITY[rel] = doc.get("security")
    return _DOC_SECURITY.get(o["file"])


def needs_session(op_id: str) -> tuple[bool, str]:
    """(needs a credential, the schemes). Public (`[]`) and optional (an alternative `{}`) do not."""
    s = security(op_id)
    if s is None:
        return True, "no security declared (defaults to a credential)"
    if s == []:
        return False, "public"
    if any(isinstance(x, dict) and not x for x in s):
        return False, "optional"
    schemes = sorted({k for x in s if isinstance(x, dict) for k in x})
    return True, " or ".join(schemes)


def params(op_id: str) -> list[dict]:
    o = operations().get(op_id)
    if not o:
        return []
    out = []
    for p in list(o["item"].get("parameters") or []) + list(o["op"].get("parameters") or []):
        if not isinstance(p, dict):
            continue
        if "$ref" in p:
            # a shared parameter: its component name stands for it (`SubjectId` -> subjectId)
            n = g.ref_name(p["$ref"])
            p = {"name": n[:1].lower() + n[1:], "in": "ref"}
        out.append(p)
    return out


# The words an operation uses when it returns the caller's own record without declaring it.
OWN_WORDS = re.compile(r"caller'?s own|their own|guest'?s own|own (position|record|account|balance|"
                       r"profile|orders?|tickets?|bookings?|wallet|cases?)", re.I)
OWN_NAME = re.compile(r"^(list|get|update|delete|create|cancel)My[A-Z]|Mine$")


def acts_on(op_id: str) -> str:
    """'caller-declared'   x-ticvai-self-scoped subject with no permission: the caller's own record only;
    'caller-undeclared'    no permission, no self-scope, a user session (bearer or guest), nobody named by a
                           parameter or path segment, and the operation calls itself the caller's own (its
                           name says My, or its summary or description says "the caller's own" / "their own");
    'named'                anything else (a permission, a named subject, public, a service, the caller's own
                           session as principal)."""
    o = operations().get(op_id)
    if not o:
        return "named"
    x = o["op"]
    ss = x.get("x-ticvai-self-scoped")
    if SESSION_OWNED.match(o["path"]):
        # **A cart is the session's own** (decided 2 October 2026, CHG-SEED-013): a till's cart belongs to the
        # workstation session and a guest is attached to it, so a till calling its cart acts on its own cart.
        return "named"
    if ss == "subject" and x.get("x-ticvai-permission") is None:
        return "caller-declared"
    if ss or x.get("x-ticvai-permission") is not None or x.get("x-ticvai-auth") == "service":
        return "named"
    need, schemes = needs_session(op_id)
    if not need or not re.search(r"bearerAuth|guestAuth", schemes):
        return "named"
    if audience(op_id) & {"public", "anonymous"}:
        return "named"
    if any(SUBJECT_PARAM.match(str(p.get("name") or "")) for p in params(op_id)):
        return "named"
    if "{" in o["path"] and re.search(r"\{(subject|guest|customer|member|account|holder)Id\}", o["path"]):
        return "named"
    text = f"{x.get('summary') or ''} {x.get('description') or ''}"
    if OWN_NAME.search(op_id) or OWN_WORDS.search(text):
        return "caller-undeclared"
    return "named"


def names_a_guest(s: dict) -> bool:
    """The screen acts for a named guest: it is opened with one (an entry parameter naming a guest, not from
    the session), or it binds an operation that takes one (a parameter or path segment naming whose)."""
    for p in ((s.get("entryState") or {}).get("params") or []):
        if isinstance(p, dict) and p.get("from") != "session" and GUEST_PARAM.match(str(p.get("name") or "")):
            return True
    for op, *_ in bindings(s):
        o = operations().get(op)
        if not o:
            continue
        if any(GUEST_PARAM.match(str(p.get("name") or "")) for p in params(op)):
            return True
        if re.search(r"\{(subject|guest|customer|member)Id\}", o["path"]):
            return True
    return False


# ------------------------------------------------------------------------------------------- screens
def screens():
    """[(code, platform audience, screen)] for every screen."""
    plats = g.platforms()
    out = []
    for stem, s in g.screens():
        p = plats.get(stem) or {}
        code = p.get("code") or stem.split("-")[0]
        out.append((code, OPERATOR_AUDIENCE.get(p.get("operator")), s))
    return out


def components(s: dict) -> list[dict]:
    out = []
    for r in ((s.get("layout") or {}).get("regions") or []):
        for c in (r.get("components") or []):
            if isinstance(c, dict):
                out.append(c)
    return out


def bindings(s: dict) -> list[tuple[str, str, str | None, str]]:
    """[(operationId, where, trigger, purpose)]: apis, component actions, form confirms, transitions."""
    out = []
    for a in s.get("apis") or []:
        if isinstance(a, dict) and a.get("operationId"):
            out.append((a["operationId"], "apis", a.get("trigger"), str(a.get("purpose") or "")))
    for c in components(s):
        if c.get("operation"):
            out.append((c["operation"], "component", "onAction", str(c.get("label") or "")))
    for o in s.get("overlays") or []:
        op = ((o or {}).get("confirm") or {}).get("operation")
        if op:
            out.append((op, "overlay", "onAction", str(o.get("trigger") or "")))
    for t in ((s.get("navigation") or {}).get("transitions") or []):
        if isinstance(t, dict) and t.get("operation"):
            out.append((t["operation"], "transition", "onAction", str(t.get("to") or "")))
    return out


def session_params(s: dict) -> set:
    es = s.get("entryState") or {}
    return {p.get("name") for p in (es.get("params") or [])
            if isinstance(p, dict) and p.get("from") == "session"}


def is_preauth(s: dict) -> bool:
    """A guest reaches it without signing in: it takes no session-issued identity, or it is the door."""
    if {op for op, *_ in bindings(s)} & SESSION_CREATORS:
        return True
    return not (session_params(s) & SESSION_IDENTITY)


def displayed_schemas(s: dict) -> set:
    """Schemas whose fields the screen shows (bindsTo and columns of the non-input, non-action components)."""
    out = set()
    for c in components(s):
        if c.get("kind") in INPUT_KINDS or c.get("kind") in ACTION_KINDS:
            continue
        b = str(c.get("bindsTo") or "")
        if b:
            out.add(b.split(".", 1)[0])
        for col in c.get("columns") or []:
            col = str(col)
            if "." in col and col[:1].isupper():
                out.add(col.split(".", 1)[0])
    return {x for x in out if re.match(r"^[A-Z][A-Za-z0-9]+$", x)}


_SCHEMA_AUD: dict = {}


def schema_audience() -> dict:
    """schema name -> the audiences of the operations that send or return it (through $refs, three deep)."""
    if _SCHEMA_AUD:
        return _SCHEMA_AUD
    by, _names = g.schemas()
    flat = {}
    for (_stem, n), sch in by.items():
        flat.setdefault(n, sch)

    def refs(node, acc):
        if isinstance(node, dict):
            r = node.get("$ref")
            if isinstance(r, str) and "/schemas/" in r:
                acc.add(g.ref_name(r))
            for v in node.values():
                refs(v, acc)
        elif isinstance(node, list):
            for v in node:
                refs(v, acc)
        return acc

    for op_id, o in operations().items():
        aud = audience(op_id)
        if not aud:
            continue
        seen = refs({"r": o["op"].get("responses"), "b": o["op"].get("requestBody")}, set())
        frontier = set(seen)
        for _ in range(3):
            nxt = set()
            for n in frontier:
                nxt |= refs(flat.get(n) or {}, set()) - seen
            seen |= nxt
            frontier = nxt
        for n in seen:
            _SCHEMA_AUD.setdefault(n, set()).update(aud)
    return _SCHEMA_AUD
