#!/usr/bin/env python3
"""Rebuild the screens no workshop pack describes, from the contracts they already call.

**501 of the package's 1,091 screens have no pack behind them**, and the pack generator has nothing
to say about them. They are not, however, sourceless: **492 of them declare operations — 2,624 in
total, an average of 5.3 each**, against a median of one on the pack-sourced screens. That is the
richest per-screen input in the package and nothing has ever read it.

    EMP-057  getGuest · listGuestVisits · listGuestOrders · matchGuest · mergeGuests
             ...renders `searchField "Find a record"`, `dataTable "Every record with its status"`.

`getGuest` returns a `Guest`. `Guest` has properties. **Those properties are what the screen can
show, and the contract is the authority on their names** — so a column bound to `Guest.loyaltyTier`
cites a contract path, fails the build when the contract renames it, and is exactly as checkable as
a column derived from a pack page.

## What this is not

**It is not derivation from the title.** That is the mistake the whole rebuild exists to undo, and
it is worth being precise about the difference: the *title* is a name somebody typed; a *declared
operation* is a commitment the contract makes and the frontend will call. Reading the second is
reading the specification. The screen's name is never consulted here except to choose a noun for a
state sentence.

**It is not a claim that these columns are the right ones.** A response schema says what a screen
*can* show, not what it *should*. Every component says so — `provenance: contract <file>
#/components/schemas/Guest` — and a person narrowing twenty fields to the six that matter is real
work this does not pretend to have done. What it removes is the situation where nobody can tell
what a screen shows at all.

## Where the pattern comes from

The **verbs of the operations the screen declares**, which is evidence rather than vocabulary:

    a decide/approve operation over a list          -> approvalInbox
    a list and a get of the same subject            -> listDetail
    only writes, no list                            -> configEditor
    three or more independent reads, no single get  -> commandCentre

`patternReason` names the operations that decided it. Where the operations decide nothing, the
screen falls to `listDetail` and **says so**, exactly as in the pack generator.

## Overlays

Every destructive operation a screen declares becomes a `confirmDialog` overlay, and every overlay
becomes a wireframe frame. **No screen in this population declared a single one** — against 2,624
operations including `cancelOrder`, `refundPayment`, `voidTransaction` and `revokeCredential`.

## Since the 27 September pull audit

States are read off the operations (R250), the table and panel show one entity and are labelled
from it, carried placeholders are dropped and same-named regions merged (R253, R256), every write
with a request body opens a form naming its fields (R264), and an operation no component reaches
fails the run instead of becoming a note (R273). **This tool is not on the refresh**: the screens
it built have been maintained since, so `tools/fix-audit-contract-screens.py` carries the same
rules onto them in place, reusing the helpers below.

Run: python tools/generate-screens-from-contracts.py --platform P06 [--write]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001 — a stream without reconfigure prints as it can
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contract_shapes import (load_contracts, path_params,  # noqa: E402
                             response_schemas, schema_fields)
import screen_patterns as SP  # noqa: E402 — the 3 October rules (CHG-SPF-001..004), shared with the check

# **Is the platform being built a phone or a handheld?** Set by `main()` per platform file; it caps
# every list and panel at five columns there (CHG-SPF-002).
SMALL_SCREEN = False
_PACKAGE = None


def package():
    """The contracts as `tools/screen_patterns.py` reads them, once, for the entry-parameter rules."""
    global _PACKAGE
    if _PACKAGE is None:
        _PACKAGE = SP.Package(str(ROOT), screens={})
    return _PACKAGE

# Provenance prefixes this generator owns; anything else on an overlay is somebody's
# decision and is carried through a rebuild.
GAPS_MINE = ("contract ",)
OVERLAYS_MINE = ("contract ", "authored \u2014 ")

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
PACK = ROOT / "sources" / "workshop" / "pack.json"

STAMP = "9 September 2026"

# `(screen id, [operationId])` for every screen whose declared operations reach no component.
UNREACHED: list[tuple[str, list[str]]] = []

# **Destructive is a property of the verb.** Zero screens in this population declare a confirm
# dialog, against operations named `cancelOrder`, `voidTransaction` and `revokeCredential`.
DESTRUCTIVE = re.compile(
    r"^(delete|remove|cancel|void|revoke|refund|reverse|suspend|terminate|deactivate|expire|"
    r"archive|purge|withdraw|reject|refuse|force|override|reset|discard|unpublish|close|stop|"
    r"disable|clear|abandon|merge)[A-Z]")
PUBLISHES = re.compile(r"^(publish|deploy|promote|activate)[A-Z]")
DECIDES = re.compile(r"^(decide|approve|adjudicate|review|endorse)[A-Z]")
READS = ("list", "get", "search", "export")

# A verb, and what a button for it says. **Read off the operation, never off the screen name.**
VERB_LABEL = {
    "create": "Create", "add": "Add", "set": "Save changes", "update": "Save changes",
    "delete": "Delete", "remove": "Remove", "cancel": "Cancel", "void": "Void",
    "refund": "Refund", "revoke": "Revoke", "publish": "Publish", "activate": "Activate",
    "approve": "Approve", "reject": "Reject", "decide": "Decide", "assign": "Assign",
    "merge": "Merge", "import": "Import", "export": "Export", "send": "Send", "issue": "Issue",
    "print": "Print", "scan": "Scan", "redeem": "Redeem", "transfer": "Transfer",
    "reprint": "Reprint", "suspend": "Suspend", "resume": "Resume", "start": "Start",
    "complete": "Complete", "close": "Close", "open": "Open", "reserve": "Reserve",
    "release": "Release", "relinquish": "Release hold", "confirm": "Confirm", "apply": "Apply",
    "search": "Search", "match": "Find matches", "simulate": "Simulate", "validate": "Validate",
    "sync": "Sync", "retry": "Retry", "acknowledge": "Acknowledge", "escalate": "Escalate",
    "resolve": "Resolve", "reassign": "Reassign", "split": "Split", "move": "Move",
}

# Fields that are plumbing on every schema in the package and are not what a screen is *about*.
# **Dropped from columns, never from the contract** — they exist, they are simply not the subject.
PLUMBING = {"createdAt", "updatedAt", "createdBy", "updatedBy", "deletedAt", "version",
            "etag", "tenantId", "cellId", "schemaVersion", "_links", "meta"}

# Boilerplate the last generation left behind. A note matching one of these is discarded rather
# than carried forward — carrying it would preserve the thing being removed.
BOILERPLATE = {
    "find a record", "every record with its status", "the selected record",
    "the records behind the figures", "the configuration being edited",
    "scope this applies at", "active", "the act the screen exists for",
    "structure from the wireframe board. components not yet enumerated.",
}

PRESERVE = ["id", "name", "module", "requiresModule", "wave", "capability", "source",
            "implementation", "navigation", "notes", "openQuestions", "density", "densityReason",
            "resolvedQuestions", "audience", "offline", "boardFrames", "machine",
            # **A note explaining a name or a purpose is not the name or the purpose.** Both were
            # dropped by this whitelist: `nameNote` records why BO-047 stopped being called F&B
            # Order Management, and `purposeNote` carries what a collapsed duplicate said before
            # it was removed — 528 screens hold one. Losing them leaves the decision unexplained
            # and the collapse indistinguishable from a deletion.
            "purposeNote", "nameNote"]

TEMPLATES = {"commandCentre": "dashboard", "listDetail": "split", "approvalInbox": "split",
             "configEditor": "form", "statusTracker": "detail", "credentialView": "detail"}


def norm(t) -> str:
    return " ".join(str(t).lower().split()).strip(" .:;,")


def words(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", " ", str(name)).lower()


def subject(name: str) -> str:
    cleaned = re.sub(r"\b(command cent(er|re)|dashboard|manager|management|monitor|builder|"
                     r"configurator|studio|workspace|explorer|center|centre|configuration|setup|"
                     r"engine|inbox|directory|library|matrix|hub|screen|page|view|detail|details)\b",
                     "", name, flags=re.I)
    cleaned = re.sub(r"[&/,]", " ", cleaned)
    kept = [w for w in cleaned.split() if len(w) > 2][:3]
    return " ".join(kept).lower() or "record"


def choose_pattern(op_ids: list[str]) -> tuple[str, str]:
    """The pattern, and the operations that chose it. **The screen's name is not consulted.**"""
    lists = [o for o in op_ids if o.startswith(("list", "search"))]
    gets = [o for o in op_ids if o.startswith("get")]
    writes = [o for o in op_ids if not o.startswith(READS)]
    decides = [o for o in op_ids if DECIDES.match(o)]

    if decides and lists:
        return "approvalInbox", (f"`{decides[0]}` decides items that `{lists[0]}` queues — every "
                                 f"row is waiting for a person, so the empty state is success")
    if writes and not lists and not gets:
        return "configEditor", (f"the screen declares only writes "
                                f"({', '.join('`' + w + '`' for w in writes[:3])}) and no read of "
                                f"a population — it is settings, not a list")
    if len(lists) >= 3 and not gets:
        return "commandCentre", (f"{len(lists)} independent reads and no read of one record — "
                                 f"the screen watches a population rather than working one")
    if lists and gets:
        return "listDetail", (f"`{lists[0]}` reads the population and `{gets[0]}` reads one of "
                              f"them — list, select, act")
    if gets and not lists:
        return "statusTracker", (f"`{gets[0]}` reads one record and nothing reads a population — "
                                 f"the screen is about that one thing")
    if lists:
        return "listDetail", (f"`{lists[0]}` reads a population and nothing reads one of them; "
                              f"the detail is the row until a `get` exists")
    return "listDetail", ("**the screen's operations choose no pattern** — no list, no get, no "
                          "write that groups. It falls to the default, and the fallback is "
                          "recorded rather than passed off as a decision")


def columns_for(schema: str, schemas: dict, limit: int = 12, kind: str | None = None) -> list[str]:
    """Field paths a component shows, plumbing removed, declaration order kept.

    **With a `kind`, narrowed to the fields the screen is about** (3 October 2026, CHG-SPF-002): the
    Block A audit found phones showing sixteen fields of an incident and panels dumping every
    property of a schema. `screen_patterns.pick_columns` keeps names, states, money and dates, drops
    plumbing and foreign ids, and keeps at most five on a phone or handheld. Without a `kind` (what a
    screen arrives holding, `entryState.preloaded`) nothing is narrowed.
    """
    raw = [f"{schema}.{p}" for p in schema_fields(schema, schemas) if p not in PLUMBING][:limit]
    if kind is None:
        return raw
    return SP.pick_columns(None, {"kind": kind, "columns": raw}, SMALL_SCREEN)


def keep_note(note) -> str | None:
    # **Both sides normalised.** `norm` strips the trailing full stop from the note and the set kept
    # its own, so *"…Components not yet enumerated."* never matched and was carried onto 151
    # screens as a second `contentBody` (audit R253).
    return None if not note or norm(note) in {norm(b) for b in BOILERPLATE} else str(note)


# ── what the 27 September audit found, and the helpers that answer it ─────────────────────────
#
# **R250 — states were a list pattern pasted onto every screen.** 2,299 screens said *"Carries the
# create action"* and 1,981 of them declared nothing that creates; 1,650 described a filter they
# did not have; every one said *"Names the missing permission"* without naming it. The operations
# answer all three, so the states are now read off them: a create action only where a create
# operation exists, a no-results state only where the list operation takes a filter, and the
# permission by name from `x-ticvai-permission`.
#
# **R253 / R256 — layouts were assembled, not composed.** The table and the panel were bound to
# two separately chosen operations and labelled from the screen's name, so `BO-091 "Every policy
# spend"` showed `IndexFailure` rows. Carried components were appended as a second `contentBody`,
# and `derive-wireframes.py` keys regions by name — **the carried placeholder replaced the generated
# table in the wireframe.** Now the panel shows the table's entity, labels come from the bound
# schema, carried placeholders are dropped and same-named regions are merged into one.
#
# **R264 — a button is not a form.** One verb-labelled button per write operation, and nothing that
# collects `transferOrderTickets`'s `recipient` or `joinQueue`'s `partySize`. Every write whose
# request body declares fields now opens a `modal` (or its `confirmDialog`, when destructive) that
# names the fields it collects, required first, inline bodies included.
#
# **R273 — an unreached operation is a failure, not a note.** Every declared read is bound to a
# component where its response has a shape; what still reaches nothing fails the run.

ACRONYMS = {
    "ai": "AI", "api": "API", "fnb": "F&B", "sla": "SLA", "seo": "SEO", "vsi": "VSI",
    "sms": "SMS", "pos": "POS", "kds": "KDS", "qr": "QR", "nfc": "NFC", "pdf": "PDF",
    "csv": "CSV", "url": "URL", "otp": "OTP", "kyc": "KYC", "vat": "VAT", "id": "ID",
    "fx": "FX", "rfid": "RFID", "sso": "SSO", "mfa": "MFA", "crm": "CRM", "cms": "CMS",
}

# Components that show data and so must name it — the same set `check-bindings.py` enforces.
DATA_BEARING = {"dataTable", "detailPanel", "cardList", "chart", "metricTile", "timeline",
                "seatMap", "cartPanel", "consentBlock", "duplicateMatch", "list", "kpiRow"}

# **A create action exists only where an operation makes something.** Read off the verb.
CREATES = re.compile(r"^(create|add|register|import|upload|issue|submit|raise|record|book|"
                     r"enrol|enroll|invite|request|open|log)[A-Z]")

# Query parameters that page a list rather than narrow it. Everything else a list operation
# accepts in the query is a filter a person can set.
PAGING = {"cursor", "limit", "pageSize", "pageCursor", "page", "offset", "sort", "order"}

# The verb half of a button label. **The label names the operation** — three buttons all reading
# `Create` (ADM-008) are three buttons nobody can tell apart.
LABEL_VERB = dict(VERB_LABEL, set="Save", update="Save", match="Find matches for",
                  relinquish="Release")

ONLOAD_ERROR = "Could not load. Names which read failed and leaves the {noun} untouched."
NO_ACCESS_TAIL = ("**Never an empty table** — that reads as *there is no data* and sends "
                  "somebody to support with the wrong question.")


def noun_for(camel: str) -> str:
    """`FnbOrderLine` -> `F&B order line`."""
    ws = re.sub(r"(?<!^)(?=[A-Z])", " ", str(camel)).strip().lower().split()
    return " ".join(ACRONYMS.get(w, w) for w in ws)


def schema_noun(schema: str | None) -> str:
    return noun_for(re.sub(r"(Summary|Detail|View|Record|Row|Item|Response)$", "", schema or "")
                    or schema or "record")


def button_label(oid: str) -> str:
    """`createPlanVersion` -> `Create plan version`; `updatePrincipal` -> `Save principal`."""
    m = re.match(r"^([a-z]+)([A-Z].*)?$", oid)
    if not m:
        return oid
    verb, rest = m.group(1), m.group(2) or ""
    base = LABEL_VERB.get(verb) or verb.capitalize()
    obj = noun_for(rest)
    if obj and not set(obj.split()) <= set(base.lower().split()):
        return f"{base} {obj}"
    return base


def cite(ops: dict, oid: str) -> str:
    return f"contract {ops[oid]['file']} {ops[oid]['method'].upper()} {ops[oid]['path']}"


def shape_of(ops: dict, oid: str | None) -> str | None:
    got = response_schemas(ops[oid]["op"]) if oid and oid in ops else []
    return got[0] if got else None


def _required_of(name: str, schemas: dict, seen=frozenset()) -> set:
    body = schemas.get(name) or {}
    req = set(body.get("required") or [])
    for branch in body.get("allOf") or []:
        if isinstance(branch, dict):
            req |= set(branch.get("required") or [])
            for ref in re.findall(r"#/components/schemas/(\w+)", str(branch.get("$ref") or "")):
                if ref not in seen:
                    req |= _required_of(ref, schemas, seen | {name})
    return req


def body_fields(entry: dict, schemas: dict) -> tuple[str | None, list[tuple[str, dict, bool]]]:
    """`(schema name or None, [(field, field schema, required)])` of an operation's request body.

    **Inline bodies count.** `createMfaChallenge` declares `{action, methodId}` inline and was
    reported as *"declares no request body shape"*, because only a `$ref` was read.
    """
    content = ((entry["op"].get("requestBody") or {}).get("content") or {})
    for media in content.values():
        schema = (media or {}).get("schema") or {}
        ref = re.findall(r"#/components/schemas/(\w+)", str(schema.get("$ref") or ""))
        if ref:
            props = schema_fields(ref[0], schemas)
            req = _required_of(ref[0], schemas)
            name = ref[0]
        else:
            props = dict(schema.get("properties") or {})
            req = set(schema.get("required") or [])
            for branch in schema.get("allOf") or []:
                if not isinstance(branch, dict):
                    continue
                props.update(branch.get("properties") or {})
                req |= set(branch.get("required") or [])
                for r in re.findall(r"#/components/schemas/(\w+)", str(branch.get("$ref") or "")):
                    props.update(schema_fields(r, schemas))
                    req |= _required_of(r, schemas)
            name = None
        # **A readOnly field is the server's to set, never the form's to ask** (3 October 2026,
        # CHG-SPF-001): the Block A audit found BO-094's form asking for `id` and `mapId`.
        fields = [(f, b if isinstance(b, dict) else {}, f in req)
                  for f, b in props.items() if f not in PLUMBING
                  and not (isinstance(b, dict) and b.get("readOnly") is True)]
        if fields:
            fields.sort(key=lambda t: not t[2])      # required first, declaration order kept
            return name, fields
    return None, []


def field_kind(name: str, body: dict) -> str:
    t, fmt = body.get("type"), body.get("format")
    if body.get("enum"):
        return "selectField"
    if t == "boolean":
        return "toggle"
    if t in ("integer", "number"):
        return "numberField"
    if fmt in ("date", "date-time"):
        return "datePicker"
    if t == "array":
        return "multiSelect"
    if name.lower() in ("search", "q", "query"):
        return "searchField"
    return "textField"


def filter_params(entry: dict | None) -> list[tuple[str, dict]]:
    """The query parameters a list operation narrows by. Shared `$ref` parameters are paging."""
    if not entry:
        return []
    out = []
    for p in entry["op"].get("parameters") or []:
        if isinstance(p, dict) and p.get("in") == "query" and p.get("name") \
                and p["name"] not in PAGING:
            out.append((p["name"], p.get("schema") or {}))
    return out


def filter_components(ops: dict, oid: str) -> list[dict]:
    return [{"kind": field_kind(n, b), "label": noun_for(n).capitalize(), "operation": oid,
             "notes": f"Sends `?{n}=` to `{oid}`.", "provenance": cite(ops, oid)}
            for n, b in filter_params(ops.get(oid))]


def screen_permission(ops: dict, known: list[str],
                      loads: set | None = None) -> tuple[str, str] | None:
    """`(permission, operation)` the screen's reads require — its writes where it has none.

    **The read the screen loads with comes first** (`loads`, the operations triggered on load):
    a picker read on a button is not what the no-access state is about (CHG-SPF-003).
    """
    loads = loads or set()
    ordered = ([o for o in known if o.startswith(READS) and o in loads]
               + [o for o in known if o.startswith(READS) and o not in loads]
               + [o for o in known if not o.startswith(READS)])
    for o in ordered:
        perm = ops[o]["op"].get("x-ticvai-permission")
        if isinstance(perm, str) and perm:
            return perm, o
    return None


def fields_sentence(oid: str, fields: list) -> str:
    req = [f for f, _, r in fields if r]
    opt = [f for f, _, r in fields if not r]

    def some(xs):
        shown = ", ".join(f"`{x}`" for x in xs[:12])
        return shown + (f" and {len(xs) - 12} more" if len(xs) > 12 else "")
    parts = [f"**Collects what `{oid}` sends before it is called.**"]
    parts.append(f"Required: {some(req)}." if req else "Nothing in the body is required.")
    if opt:
        parts.append(f"Optional: {some(opt)}.")
    return " ".join(parts)


def confirm_body(oid: str, noun: str) -> str:
    return (f"**Names what `{oid}` changes and what it leaves alone**, in the consequence rather "
            f"than the verb. A {noun} this affects should be identified in the dialog, not just "
            f"counted.")


def action_overlay(ops: dict, schemas: dict, oid: str, label: str, noun: str) -> dict | None:
    """The overlay a write's button opens: its confirmation, its form, or nothing."""
    name, fields = body_fields(ops[oid], schemas)
    if DESTRUCTIVE.match(oid):
        o = {"id": "confirm" + oid[0].upper() + oid[1:], "component": "confirmDialog",
             "trigger": label, "body": confirm_body(oid, noun)}
        if fields:
            o["body"] += " " + fields_sentence(oid, fields)
            if name:
                o["bindsTo"] = name
        o["provenance"] = cite(ops, oid)
        return o
    if not fields:
        return None
    o = {"id": "form" + oid[0].upper() + oid[1:], "component": "modal", "trigger": label,
         "body": fields_sentence(oid, fields)
         + " Dismissing sends nothing; the screen behind is unchanged."}
    if name:
        o["bindsTo"] = name
    o["confirm"] = {"label": label, "operation": oid}
    o["dismiss"] = {"label": "Cancel", "discards": [f for f, _, _ in fields][:18]}
    o["provenance"] = cite(ops, oid)
    return o


def form_components(ops: dict, schemas: dict, oid: str) -> list[dict]:
    name, fields = body_fields(ops[oid], schemas)
    out = []
    for f, b, req in fields[:18]:
        c = {"kind": field_kind(f, b), "label": noun_for(f).capitalize()}
        if name:
            c["bindsTo"] = f"{name}.{f}"
        c["operation"] = oid
        if req:
            c["notes"] = "Required."
        c["provenance"] = cite(ops, oid)
        out.append(c)
    return out


def inline_response(entry: dict) -> tuple[bool, list[str]]:
    """`(is a list, field names)` of a success response declared in place rather than by `$ref`."""
    for code in ("200", "201"):
        for media in (((entry["op"].get("responses") or {}).get(code) or {}).get("content")
                      or {}).values():
            schema = (media or {}).get("schema") or {}
            many = schema.get("type") == "array"
            body = (schema.get("items") or {}) if many else schema
            props = [p for p in (body.get("properties") or {}) if p not in PLUMBING]
            if props:
                return many, props
    return False, []


def inline_response_gap(ops: dict, oid: str) -> dict:
    return {"operation": oid,
            "why": (f"**`{oid}` declares its response inline**, so the component that shows it "
                    f"names fields but binds to no schema. The contract should name the shape."),
            "source": cite(ops, oid)}


def bind_read(ops: dict, schemas: dict, oid: str, pattern: str) -> tuple[str, dict] | None:
    """A component for a declared read nothing else binds: `(region name, component)`."""
    if oid.startswith("export"):
        return "actionBar", {"kind": "secondaryButton", "label": button_label(oid),
                             "operation": oid, "provenance": cite(ops, oid)}
    media = [m for code in ("200", "201")
             for m in ((((ops[oid]["op"].get("responses") or {}).get(code) or {})
                        .get("content")) or {})]
    if media and not any("json" in m for m in media):
        # `getOrderCalendarEvent` answers `text/calendar`: a file the guest saves, not data a
        # panel shows. It is reached by the button that downloads it.
        rest = re.sub(r"^(get|list)", "", oid)
        return "actionBar", {"kind": "secondaryButton", "label": f"Download {noun_for(rest)}",
                             "operation": oid, "notes": f"Downloads `{media[0]}`.",
                             "provenance": cite(ops, oid)}
    sch = shape_of(ops, oid)
    cols = columns_for(sch, schemas, limit=16,
                       kind="dataTable" if oid.startswith(("list", "search")) else "detailPanel") \
        if sch else []
    region = "contextPanel" if TEMPLATES.get(pattern) == "split" else "contentBody"
    if not cols:
        # **An inline response still says what the screen shows.** `getAvailability` returns an
        # array of `{performanceId, capacity, sold, remaining}` declared in place; the component
        # calls it and names those fields, and stays unbound (`check-bindings`) until the contract
        # names the shape — which the gap `inline_response_gap` records says it must.
        many, names = inline_response(ops[oid])
        if not names:
            return None
        shown = ", ".join(f"`{n}`" for n in names[:12])
        return ("contentBody" if many else region), {
            "kind": "dataTable" if many else "detailPanel",
            "label": noun_for(re.sub(r"^(list|get|search)", "", oid)).capitalize(),
            "operation": oid,
            "notes": (f"Shows {shown} from `{oid}`'s inline response. **The response has no "
                      f"named schema**, so this cannot bind until the contract names one."),
            "provenance": cite(ops, oid)}
    if oid.startswith(("list", "search")):
        return "contentBody", {"kind": "dataTable", "label": f"Every {schema_noun(sch)}",
                               "bindsTo": sch, "columns": cols, "operation": oid,
                               "provenance": cite(ops, oid)}
    return region, {"kind": "detailPanel", "label": f"The {schema_noun(sch)}", "bindsTo": sch,
                    "columns": cols, "operation": oid, "provenance": cite(ops, oid)}


def reached_ops(regions: list, overlays: list) -> set:
    got = {c.get("operation") for r in regions for c in (r.get("components") or [])}
    got |= {(o.get("confirm") or {}).get("operation") for o in overlays or []}
    return {g for g in got if g}


def reaching_kinds(regions: list, overlays: list) -> dict:
    """`{operationId: {component kinds that call it}}`; an overlay's confirm counts as `overlay`."""
    out: dict = {}
    for r in regions:
        for c in r.get("components") or []:
            if c.get("operation"):
                out.setdefault(c["operation"], set()).add(str(c.get("kind", "")))
    for o in overlays or []:
        op = (o.get("confirm") or {}).get("operation")
        if op:
            out.setdefault(op, set()).add("overlay")
    return out


# What a `derive-components` proposal is standing in for. It is dropped only when the operation it
# was proposed for is now reached by a component of the same family — **a scan target proposed for
# `validateAccess` is not replaced by a button that calls it.**
FAMILY = {"dataTable": {"dataTable", "cardList"}, "cardList": {"dataTable", "cardList"},
          "detailPanel": {"detailPanel", "metricTile"},
          "searchField": {"searchField", "textField", "selectField", "toggle", "datePicker",
                          "numberField", "multiSelect"}}


def is_placeholder(c: dict, reached: set, labels: set, kinds: dict | None = None) -> bool:
    """A carried component that says nothing the generated layout does not already say."""
    kind = str(c.get("kind", ""))
    if c.get("derived") and c.get("impliedBy") in reached:
        have = (kinds or {}).get(c["impliedBy"], set())
        fam = FAMILY.get(kind)
        if fam and have & fam:
            return True      # a derive-components proposal for an operation now bound
        if kind.endswith("Button") and any(k.endswith("Button") for k in have):
            return True      # its button, or the "Cancel" beside it — the form's dismiss now
    if not (c.get("label") or c.get("bindsTo") or c.get("operation")
            or keep_note(c.get("notes"))):
        return True          # "Structure from the wireframe board. Components not yet enumerated."
    if kind.endswith("Button") and not c.get("operation") and norm(c.get("label", "")) in labels:
        return True          # "Create principal" beside the bound `createPrincipal` button
    return False


def merge_regions(regions: list) -> list:
    """One region per name. **`derive-wireframes.py` keys regions by name**, so a second
    `contentBody` silently replaced the first in every wireframe drawn from it."""
    out, by = [], {}
    for r in regions:
        name = r.get("name", "contentBody")
        if name in by:
            by[name].setdefault("components", []).extend(r.get("components") or [])
        else:
            r = dict(r, components=list(r.get("components") or []))
            by[name] = r
            out.append(r)
    return [r for r in out if r.get("components")]


# The texts this generator writes, old and new. **A state it wrote is not a state somebody
# decided**, and treating the last run's boilerplate as a person's words is how 2,299 copies of
# "Carries the create action" survived every rebuild.
_N = r"[^.\n*`]{1,60}"          # a noun from `subject()`: three words at most, never a sentence
OWN_STATES = [re.compile(p.replace("{N}", _N)) for p in (
    r"^The {N} list\.$",
    r"^The saved {N}\.$",
    r"^The {N}, read by `\w+`\.$",
    r"^The {N} figures; each tile loads on its own\.$",
    r"^Could not load\. Names which read failed and leaves the {N} untouched\.$",
    r"^No {N} yet\. Carries the create action; distinct from a filter that matched nothing\.$",
    r"^No {N} configured\. Carries the create action and says what the platform does in the "
    r"meantime\.$",
    r"^The filter narrowed it and the {N} are still there\. Names the active filter and offers to "
    r"clear it\.$",
    r"^Names the missing permission\. \*\*Never an empty table\*\* — that reads as \*there is no "
    r"data\* and sends somebody to support with the wrong question\.$",
    r"^\*\*Nothing is waiting, which is the good outcome\.\*\* An empty queue means every item "
    r"has been decided; it offers no create action, because creating work is not what it needs\.$",
    r"^No {N} yet\. Offers {N} \(`\w+`\)(; distinct from a filter that matched nothing)?\.$",
    r"^No {N} yet\. \*\*Offers no create action\*\* — this screen declares no operation that "
    r"makes one — and says so rather than showing an empty table\.$",
    r"^No {N} configured\. The form opens empty and `\w+` saves the first one; it says what the "
    r"platform does in the meantime\.$",
    r"^No {N} configured, and this screen declares nothing that saves one\.$",
    r"^Nothing matches the filter on [\w, ]{1,200} and the {N} are still there\. Names the active "
    r"filter and offers to clear it\.$",
    r"^Never shown: `\w+` takes no filter, so an empty list is always the first-run state above\.$",
    r"^Shown when the caller lacks `[A-Za-z0-9_.:-]+`, which `\w+` requires( to show this "
    r"screen)?, and names that permission\. \*\*Never an empty table\*\* — that reads as \*there "
    r"is no data\* and sends somebody to support with the wrong question\.( A caller who can see "
    r"the screen but lacks what an action needs sees that action disabled, naming its permission: "
    r"[^\n]*)?$",
)]
OWNED_STATES = ("loading", "error", "emptyFirstRun", "emptyNoResults", "emptyNoAccess")


def is_own_state(v) -> bool:
    return isinstance(v, str) and any(p.match(v.strip()) for p in OWN_STATES)


def no_access_state(ops: dict, known: list[str], loads: set | None = None) -> str | None:
    """**The read's permission for viewing, and each action's where the actions need more**
    (3 October 2026, CHG-SPF-003). The Block A audit found BO-094 naming `VENUE_MAP_VIEW` while its
    every button needs `VENUE_MAP_MANAGE` or `VENUE_MAP_PUBLISH`: a caller told the first is
    missing gets it and still cannot work. `tools/check-screen-patterns.py` holds the rule."""
    perm = screen_permission(ops, known, loads)
    if not perm:
        return None
    loads = loads or set()
    acts: dict = {}
    for o in known:
        if o in loads:
            continue
        p = ops[o]["op"].get("x-ticvai-permission")
        if isinstance(p, str) and p and p != perm[0]:
            acts.setdefault(p, []).append(o)
    text = (f"Shown when the caller lacks `{perm[0]}`, which `{perm[1]}` requires to show this "
            f"screen, and names that permission. " + NO_ACCESS_TAIL)
    if acts:
        text += (" A caller who can see the screen but lacks what an action needs sees that action "
                 "disabled, naming its permission: "
                 + "; ".join(f"`{p}` for " + ", ".join(f"`{o}`" for o in os_[:4])
                             for p, os_ in sorted(acts.items())[:6]) + ".")
    return text


def derived_states(pattern: str, noun: str, known: list[str], ops: dict,
                   collection_op: str | None, detail_op: str | None,
                   loads: set | None = None) -> dict:
    """The rendering states the screen's operations justify, and no others."""
    if pattern == "configEditor":
        loading = f"The saved {noun}."
    elif pattern == "statusTracker" and detail_op:
        loading = f"The {noun}, read by `{detail_op}`."
    elif pattern == "commandCentre":
        loading = f"The {noun} figures; each tile loads on its own."
    else:
        loading = f"The {noun} list."
    states = {"loading": loading, "error": ONLOAD_ERROR.format(noun=noun)}
    filters = [n for n, _ in filter_params(ops.get(collection_op))] if collection_op else []
    creates = [o for o in known if CREATES.match(o)]
    writer = next((o for o in known if not o.startswith(READS)), None)
    if pattern == "approvalInbox":
        states["emptyFirstRun"] = ("**Nothing is waiting, which is the good outcome.** An empty "
                                   "queue means every item has been decided; it offers no create "
                                   "action, because creating work is not what it needs.")
    elif pattern == "configEditor":
        states["emptyFirstRun"] = (
            f"No {noun} configured. The form opens empty and `{writer}` saves the first one; it "
            f"says what the platform does in the meantime." if writer else
            f"No {noun} configured, and this screen declares nothing that saves one.")
    elif creates:
        states["emptyFirstRun"] = (f"No {noun} yet. Offers {button_label(creates[0])} "
                                   f"(`{creates[0]}`)"
                                   + ("; distinct from a filter that matched nothing."
                                      if filters else "."))
    else:
        states["emptyFirstRun"] = (f"No {noun} yet. **Offers no create action** — this screen "
                                   f"declares no operation that makes one — and says so rather "
                                   f"than showing an empty table.")
    if filters and pattern != "configEditor":
        states["emptyNoResults"] = (f"Nothing matches the filter on {', '.join(filters[:6])} and "
                                    f"the {noun} are still there. Names the active filter and "
                                    f"offers to clear it.")
    elif collection_op and pattern != "configEditor":
        # Said rather than left out: `check-screens` asks every list for this state, and the true
        # answer for a list that cannot be narrowed is that it never happens.
        states["emptyNoResults"] = (f"Never shown: `{collection_op}` takes no filter, so an empty "
                                    f"list is always the first-run state above.")
    na = no_access_state(ops, known, loads)
    if na:
        states["emptyNoAccess"] = na
    return states


def entry_param(screen: dict, name: str, ops: dict, known: list[str]) -> dict:
    """**Required only when nothing else can supply it** (3 October 2026, CHG-SPF-004). The audit
    found 784 required parameters no inbound edge carried: `WEB-044` needing a `conversationId` it
    creates itself, list screens needing the id of the row the user has not picked yet. A screen
    that lists or reads the id itself, makes it, or only acts on it, opens without it
    (`screen_patterns.param_for`, the rule `check-screen-patterns` P5 holds the screens to)."""
    return SP.param_for(package(), screen, name, "navigation")


def build(screen: dict, ops: dict, schemas: dict, report: Counter) -> dict:
    op_ids = [a.get("operationId") for a in (screen.get("apis") or []) if a.get("operationId")]
    known = [o for o in op_ids if o in ops]
    pattern, reason = choose_pattern(known)
    noun = subject(screen["name"])

    reads = [o for o in known if o.startswith(READS)]
    collection_op = next((o for o in reads if o.startswith(("list", "search"))), None)

    def shape(oid):
        return shape_of(ops, oid)

    coll_schema = shape(collection_op) if collection_op else None
    gets = [o for o in reads if o.startswith("get")]
    # **R256: the panel shows the table's entity.** Picking the list and the get separately bound
    # `GST-026`'s table to one thing and its panel to `GameCard`. The selection reads through a
    # `get` that returns the row's own schema, or from the row itself until one exists; any other
    # `get` is its own panel further down, labelled for what it actually returns.
    if coll_schema:
        detail_op = next((g for g in gets if shape(g) == coll_schema), None)
        det_schema = coll_schema
    else:
        detail_op = gets[0] if gets else None
        det_schema = shape(detail_op) if detail_op else None

    def cite_(oid):
        return cite(ops, oid)

    regions, overlays, gaps = [], [], []
    counts = Counter()

    # --- the collection ------------------------------------------------------------------------
    if pattern in ("listDetail", "approvalInbox", "commandCentre") and coll_schema:
        cols = columns_for(coll_schema, schemas, kind="dataTable")
        if cols:
            counts["bound"] += 1
            # **R250: a filter exists where the operation takes one.** The no-results state below
            # is written only when these components are.
            regions.append({"name": "contentBody",
                            "slot": "queue" if pattern == "approvalInbox" else "collection",
                            "components": filter_components(ops, collection_op) + [{
                                "kind": "dataTable",
                                "label": ("Waiting for a decision" if pattern == "approvalInbox"
                                          else f"Every {schema_noun(coll_schema)}"),
                                "bindsTo": coll_schema,
                                "columns": cols,
                                "operation": collection_op,
                                "provenance": cite_(collection_op)}]})
        else:
            gaps.append({"operation": collection_op,
                         "why": (f"**`{collection_op}` returns `{coll_schema}` and that schema "
                                 f"declares no properties**, so the table has nothing to show. "
                                 f"The response shape needs writing before this screen can be "
                                 f"built."),
                         "source": cite_(collection_op)})

    # --- the reads that fill a command centre's tiles ------------------------------------------
    if pattern == "commandCentre":
        tiles = []
        for oid in [o for o in reads if not o.startswith("export")]:
            sch = shape(oid)
            tiles.append({"kind": "metricTile",
                          "label": words(re.sub(r"^(list|get|search)", "", oid)).strip().capitalize(),
                          "bindsTo": sch, "operation": oid,
                          "provenance": cite_(oid)})
            if sch:
                counts["bound"] += 1
        if tiles:
            regions.insert(0, {"name": "contentBody", "slot": "headline", "components": tiles})

    # --- the selection --------------------------------------------------------------------------
    if pattern in ("listDetail", "approvalInbox", "statusTracker") and det_schema:
        cols = columns_for(det_schema, schemas, limit=16, kind="detailPanel")
        if cols:
            counts["bound"] += 1
            # **A status tracker's record is the screen, not a side panel.** `_patterns.yaml` gives
            # it `appHeader` and `contentBody` and nothing else; putting its one record in a
            # context panel left 20 screens — `GST-032 AI Concierge`, `GST-009 Review & Payment` —
            # with no content region at all and counted as undrawable, while their operations
            # offered 114 and 70 fields respectively.
            regions.append({"name": ("contentBody" if pattern == "statusTracker"
                                     else "contextPanel"),
                            "slot": "item" if pattern == "approvalInbox" else
                                    "record" if pattern == "statusTracker" else "selection",
                            "components": [{
                                "kind": "detailPanel",
                                "label": (f"The {schema_noun(det_schema)}"
                                          if pattern == "statusTracker"
                                          else f"The selected {schema_noun(det_schema)}"),
                                "bindsTo": det_schema,
                                "columns": cols,
                                "operation": detail_op or collection_op,
                                "provenance": cite_(detail_op or collection_op)}]})

    # --- the form --------------------------------------------------------------------------------
    form_writer = None
    if pattern == "configEditor":
        writer = next((o for o in known if not o.startswith(READS)), None)
        fields = form_components(ops, schemas, writer) if writer else []
        if fields:
            counts["bound"] += 1
            form_writer = writer
            regions.append({"name": "contentBody", "slot": "fields", "components": fields})
        else:
            gaps.append({"operation": writer,
                         "why": (f"**`{writer}` declares no request body**, so nothing says what "
                                 f"this editor edits. The fields cannot be derived and the screen "
                                 f"needs the contract before it needs a designer."),
                         "source": cite_(writer) if writer else "the screen's own operations"})

    # --- actions, and the overlays they raise -----------------------------------------------------
    # **R253 / R264: a button names its operation and opens what collects its body.** `Create` x3
    # on ADM-008 could not be told apart, and `Transfer` on GST-010 had nowhere to put the
    # recipient `transferOrderTickets` requires.
    action_components = []
    for oid in known:
        if oid.startswith(READS):
            continue
        label = button_label(oid)
        destructive = bool(DESTRUCTIVE.match(oid))
        kind = ("destructiveButton" if destructive
                else "primaryButton"
                if not any(c["kind"] == "primaryButton" for c in action_components)
                else "secondaryButton")
        action_components.append({"kind": kind, "label": label, "operation": oid,
                                  "provenance": cite_(oid)})
        if oid != form_writer:
            ov = action_overlay(ops, schemas, oid, label, noun)
            if ov:
                overlays.append(ov)
    if any(PUBLISHES.match(o) for o in known):
        action_components.append({
            "kind": "publishGate", "label": "What publishing changes",
            "notes": "**Names what goes live, where, and from when.** A publish with no stated "
                     "consequence is one somebody presses meaning to save.",
            "provenance": "authored — required by check-screens"})
    if action_components:
        regions.append({"name": "actionBar",
                        "slot": {"approvalInbox": "decision", "configEditor": "publish"}
                                .get(pattern, "rowActions"),
                        "components": action_components})

    # --- every other declared read gets a component (R273) ----------------------------------------
    for oid in known:
        if oid in reached_ops(regions, overlays) or not oid.startswith(READS):
            continue
        bound = bind_read(ops, schemas, oid, pattern)
        if bound:
            name, comp = bound
            regions.append({"name": name, "slot": "rowActions" if name == "actionBar" else "reads",
                            "components": [comp]})
            if comp.get("bindsTo"):
                counts["bound"] += 1
            elif comp.get("kind") in DATA_BEARING:
                gaps.append(inline_response_gap(ops, oid))

    # --- what the old screen said that is worth keeping --------------------------------------------
    # **Labels and notes a person wrote are kept; the ten boilerplate strings are not.** Carrying
    # `"Find a record"` forward would preserve exactly the thing being removed.
    # **What this generator did not write, it keeps; what it wrote, it rewrites.**
    #
    # The first attempt read the screen's current layout and carried anything that was not a
    # `dataTable` or a button — which after one run is *this tool's own output*, so a second run
    # carried the fields it had just generated and the file grew: 5,390 components became 6,954
    # and then 8,636 across three runs before anyone looked. **A generator that is not a function
    # of its input is not a generator**, and file size was the only thing that showed it.
    #
    # `provenance` is what distinguishes the two. Everything written here cites `contract …` or
    # `authored — …`; everything a person wrote cites something else, or nothing at all.
    #
    # **Carried components join the region of the same name** rather than a second one (R253), and
    # a carried component that only restates the generated layout — a `derive-components`
    # proposal for an operation now bound, a `"Components not yet enumerated"` panel, a
    # `Create principal` button with no operation beside the bound one — is dropped.
    MINE = ("contract ", "authored — ")
    reached = reached_ops(regions, overlays)
    labels = {norm(c.get("label", "")) for r in regions for c in r["components"]
              if str(c.get("kind", "")).endswith("Button")}
    labels |= {norm(words(o)) for o in reached}
    carried = 0
    for region in (screen.get("layout") or {}).get("regions") or []:
        comps = []
        for c in region.get("components") or []:
            if str(c.get("provenance", "")).startswith(MINE):
                continue
            if not (keep_note(c.get("notes")) or c.get("label")):
                continue
            body = {k: v for k, v in c.items() if k != "notes" or keep_note(v)}
            if is_placeholder(body, reached, labels, reaching_kinds(regions, overlays)):
                report["carried placeholders dropped"] += 1
                continue
            body["provenance"] = c.get("provenance") or "carried from the previous definition"
            comps.append(body)
        if comps:
            regions.append({"name": region.get("name", "contentBody"), "slot": "carried",
                            "components": comps})
            carried += len(comps)
    regions = merge_regions(regions)
    report["carried components"] += carried

    # --- gaps ----------------------------------------------------------------------------------
    if not known:
        gaps.append({"operation": None,
                     "why": ("**This screen declares no operation the contracts recognise.** "
                             "Nothing fills it, nothing it does is committed anywhere, and its "
                             "shape below is a default rather than a reading."),
                     "source": "the screen's own declarations"})
        report["no known operations"] += 1
    reached = reached_ops(regions, overlays)
    unreached = [o for o in known if o not in reached]
    if unreached:
        gaps.append({"operation": unreached[0],
                     "why": (f"**{len(unreached)} declared operation"
                             f"{'s' if len(unreached) > 1 else ''} reach no component on this "
                             f"screen**: {', '.join(unreached[:8])}. Either the screen is missing "
                             f"what calls them, or the declaration is residue."),
                     "source": "the screen's own declarations"})
        report["operations reaching nothing"] += len(unreached)
        UNREACHED.append((screen["id"], unreached))
    if reason.startswith("**the screen's operations choose no pattern"):
        report["no pattern evidence"] += 1

    # --- states ---------------------------------------------------------------------------------
    tabled = any(c.get("operation") == collection_op and c.get("kind") == "dataTable"
                 for r in regions for c in r["components"])
    loads = {a.get("operationId") for a in (screen.get("apis") or [])
             if a.get("trigger") in SP.LOAD_TRIGGERS}
    states = derived_states(pattern, noun, known, ops, collection_op if tabled else None,
                            detail_op, loads)
    prior = screen.get("states") or {}
    for k, v in prior.items():
        if not v or is_own_state(v):
            continue
        if k in OWNED_STATES:
            # A state a person wrote outranks a derived one. `statesDerived` marks the ones that
            # were not written, and 393 of this population carry it.
            if not screen.get("statesDerived"):
                states[k] = v
        elif k != "offline":
            # **A state this generator does not write is not a state it may delete.** `denied`
            # is written by the permission work, and the failure states that
            # `navigation.transitions[].onFailure` anchors point at are written by hand.
            states[k] = v
    if screen.get("offline") or "offline" in prior:
        states["offline"] = prior.get(
            "offline", "Served from the local journal. Says what is stale and since when.")

    # --- assemble --------------------------------------------------------------------------------
    out = {k: screen[k] for k in PRESERVE if k in screen}
    out["pattern"] = pattern
    out["patternReason"] = reason
    out["purpose"] = screen.get("purpose")
    # **A gap this generator did not raise is carried, as overlays and components are.** Both
    # generators rebuild `gaps` from what they can see in a pack page or a contract, and assigning
    # that list wholesale deleted every question any other source had recorded on the screen —
    # including the ones the schema calls "a real question" and the brief says never to draw over.
    # `POS-003` and `POS-004` lost theirs on the first rebuild after they were written, which is
    # how this was found.
    kept_gaps = [g for g in (screen.get("gaps") or [])
                 if not str(g.get("source", "")).startswith(GAPS_MINE)
                 and str(g.get("source", "")) != "the screen's own declarations"]
    if gaps or kept_gaps:
        out["gaps"] = gaps + kept_gaps
    out["layout"] = {"template": TEMPLATES[pattern], "regions": regions}
    # **An overlay this generator did not write is carried, exactly as a component is.** Both
    # generators build `overlays` fresh from the destructive actions they find, and assigning that
    # list wholesale deleted every popup any other source had put on the screen. It went unnoticed
    # because until the 3 August UI/UX decisions were applied, nothing else had ever written one —
    # so the first drawer added to the POS would have survived until the next rebuild and then
    # vanished, with no check able to say what had been lost.
    # **A rebuilt overlay keeps what another source said about closing it.** This generator owns
    # the dialog's existence, its trigger and its body. It does not own `confirm` and `dismiss`,
    # which say where accepting and dismissing land and what each carries or throws away — those
    # come from §2.3 and from the minutes. Rebuilding the dict wholesale dropped them from 13 of
    # P04's 16 overlays the first time it ran after they were written, and the three that survived
    # did so only because their provenance kept them out of this generator's hands entirely.
    # **The form modals (R264) write a default `confirm` and `dismiss`**, so the rule is now that a
    # prior half wins unless it is only this generator's own default — one saying nothing beyond
    # the label, the operation and the discarded fields.
    _prior = {o.get("id"): o for o in (screen.get("overlays") or [])}
    _defaults = {"confirm": {"label", "operation"}, "dismiss": {"label", "discards"}}
    for _o in overlays:
        _was = _prior.get(_o.get("id")) or {}
        for _half in ("confirm", "dismiss"):
            if _was.get(_half) and (_half not in _o
                                    or not set(_was[_half]) <= _defaults[_half]):
                _o[_half] = _was[_half]

    kept_overlays = [o for o in (screen.get("overlays") or [])
                     if not str(o.get("provenance", "")).startswith(OVERLAYS_MINE)
                     and o.get("id") not in {x.get("id") for x in overlays}]
    if overlays or kept_overlays:
        out["overlays"] = overlays + kept_overlays
    out["states"] = states
    out["apis"] = [dict(a, **({"invalidates": [collection_op]}
                              if a.get("trigger") == "onAction" and collection_op else {}))
                   for a in (screen.get("apis") or [])]

    entry = dict(screen.get("entryState") or {})
    needed = sorted({p for o in known for p in path_params(ops[o])})
    if needed and not entry.get("params"):
        entry["params"] = [entry_param(screen, p, ops, known) for p in needed]
    if pattern in ("listDetail", "approvalInbox") and det_schema:
        entry["preloaded"] = columns_for(det_schema, schemas, limit=5)
    if entry:
        out["entryState"] = entry
    if screen.get("wireframe"):
        out["wireframe"] = screen["wireframe"]
    out["apisNote"] = (
        f"Rebuilt {STAMP} from the {len(known)} operation"
        f"{'s' if len(known) != 1 else ''} this screen declares, not from a workshop pack — it has "
        f"none. Columns are the fields the screen is about, chosen by "
        f"`screen_patterns.pick_columns`: plumbing and foreign ids out, at most five on a phone or "
        f"handheld (CHG-SPF-002).")

    report[f"pattern:{pattern}"] += 1
    report["overlays"] += len(overlays)
    report["gaps"] += len(gaps)
    report["bound components"] += counts["bound"]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--sample", default="")
    args = ap.parse_args()

    pack = set()
    if PACK.exists():
        pack = {(e["source"], str(e["number"]), str(e["page"]))
                for e in json.loads(PACK.read_text(encoding="utf-8"))}
    ops, schemas = load_contracts(ROOT)
    report, done = Counter(), 0

    files = sorted(SCREENS.glob(f"{args.platform}-*.yaml")) if args.platform \
        else sorted(SCREENS.glob("P*.yaml"))
    pending = []
    for path in files:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        global SMALL_SCREEN
        SMALL_SCREEN = doc["platform"].get("formFactor") in SP.SMALL_FORM_FACTORS
        touched = 0
        for i, screen in enumerate(doc["screens"]):
            src = screen.get("source") or {}
            # **Only the screens the pack generator cannot reach.** A screen with a pack entry is
            # already rebuilt from a richer source and must not be overwritten from a thinner one.
            # **A pack entry is not the same as being served by one.** 203 screens came out of the
            # pack rebuild with no content region at all — their pages carry a purpose, acceptance
            # conditions and worked examples and no directory of anything — and this tool skipped
            # every one of them because a pack entry existed. **197 of the 203 declare operations
            # that would give them 3,959 fields.** The hand-off between the two generators had a
            # hole in it exactly where the pack was thinnest.
            drawn = any(r.get("name") == "contentBody" and r.get("components")
                        for r in (screen.get("layout") or {}).get("regions") or [])
            if drawn and (src.get("pack"), str(src.get("number")),
                          str(src.get("page"))) in pack:
                continue
            if not drawn and (src.get("pack"), str(src.get("number")),
                              str(src.get("page"))) in pack:
                report["pack gave nothing — filled from the contracts"] += 1
            # **A screen drawn by a person outranks one derived from a response schema.** P11's
            # eight screens were rebuilt from Claude Design's frames, which carry the columns, the
            # copy and the reasoning; the contracts carry field names. Overwriting the first with
            # the second is a regression, and the frames say so themselves in `provenance`.
            if any(str(c.get("provenance", "")).startswith("frame ")
                   for r in (screen.get("layout") or {}).get("regions") or []
                   for c in r.get("components") or []):
                report["left alone — drawn from a frame"] += 1
                continue
            doc["screens"][i] = build(screen, ops, schemas, report)
            touched += 1
        if touched:
            pending.append((path, doc))
            print(f"  {doc['platform']['code']}  {touched:>4} screens rebuilt from contracts")
        done += touched

        if args.sample:
            for s in doc["screens"]:
                if s["id"] in set(args.sample.split(",")):
                    print(yaml.safe_dump(s, sort_keys=False, allow_unicode=True, width=100))

    print(f"\n{done} screens rebuilt\n")
    for k in sorted(report):
        print(f"  {k:<28} {report[k]}")

    # **R273: an operation that reaches nothing fails the run.** Until 27 September this wrote a
    # gap saying *"either the screen is missing what calls them, or the declaration is residue"*
    # and shipped the screen anyway, and ticket generation then listed every declared operation as
    # a call to build. Nothing is written while one remains: bind it (a response shape, a button)
    # or take it out of `apis[]`, which is a decision about the screen and not this tool's to make.
    if UNREACHED:
        print(f"\nFAIL  {len(UNREACHED)} screen(s) declare operations no component reaches:")
        for sid, oids in UNREACHED:
            print(f"  {sid:<10} {', '.join(oids)}")
        if args.write:
            print("\nnothing written — bind or remove these first")
        return 1

    if args.write:
        for path, doc in pending:
            # The comment header is the file's own history; keep it, as derive-components does.
            head = "".join(x for x in path.read_text(encoding="utf-8").splitlines(keepends=True)
                           if x.startswith("#"))
            path.write_text(head + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                                                  width=100), encoding="utf-8")
            print(f"  written  {path.name}")
    else:
        print("\n(dry run — pass --write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
