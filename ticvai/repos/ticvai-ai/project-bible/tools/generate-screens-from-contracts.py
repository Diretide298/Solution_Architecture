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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contract_shapes import (load_contracts, path_params,  # noqa: E402
                             response_schemas, schema_fields)

# Provenance prefixes this generator owns; anything else on an overlay is somebody's
# decision and is carried through a rebuild.
GAPS_MINE = ("contract ",)
OVERLAYS_MINE = ("contract ", "authored \u2014 ")

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
PACK = ROOT / "sources" / "workshop" / "pack.json"

STAMP = "9 September 2026"

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


def columns_for(schema: str, schemas: dict, limit: int = 12) -> list[str]:
    """Field paths a component can bind, plumbing removed, declaration order kept."""
    return [f"{schema}.{p}" for p in schema_fields(schema, schemas)
            if p not in PLUMBING][:limit]


def keep_note(note) -> str | None:
    return None if not note or norm(note) in BOILERPLATE else str(note)


def build(screen: dict, ops: dict, schemas: dict, report: Counter) -> dict:
    op_ids = [a.get("operationId") for a in (screen.get("apis") or []) if a.get("operationId")]
    known = [o for o in op_ids if o in ops]
    pattern, reason = choose_pattern(known)
    noun = subject(screen["name"])

    reads = [o for o in known if o.startswith(READS)]
    collection_op = next((o for o in reads if o.startswith(("list", "search"))), None)
    detail_op = next((o for o in reads if o.startswith("get")), None)

    def shape(oid):
        got = response_schemas(ops[oid]["op"]) if oid in ops else []
        return got[0] if got else None

    coll_schema = shape(collection_op) if collection_op else None
    det_schema = shape(detail_op) if detail_op else coll_schema

    def cite(oid):
        return f"contract {ops[oid]['file']} {ops[oid]['method'].upper()} {ops[oid]['path']}"

    regions, overlays, gaps = [], [], []
    counts = Counter()

    # --- the collection ------------------------------------------------------------------------
    if pattern in ("listDetail", "approvalInbox", "commandCentre") and coll_schema:
        cols = columns_for(coll_schema, schemas)
        if cols:
            counts["bound"] += 1
            regions.append({"name": "contentBody",
                            "slot": "queue" if pattern == "approvalInbox" else "collection",
                            "components": [{
                                "kind": "dataTable",
                                "label": ("Waiting for a decision" if pattern == "approvalInbox"
                                          else f"Every {noun}"),
                                "bindsTo": coll_schema,
                                "columns": cols,
                                "operation": collection_op,
                                "provenance": cite(collection_op)}]})
        else:
            gaps.append({"operation": collection_op,
                         "why": (f"**`{collection_op}` returns `{coll_schema}` and that schema "
                                 f"declares no properties**, so the table has nothing to show. "
                                 f"The response shape needs writing before this screen can be "
                                 f"built."),
                         "source": cite(collection_op)})
    elif pattern in ("commandCentre",) and not coll_schema:
        pass

    # --- the reads that fill a command centre's tiles ------------------------------------------
    if pattern == "commandCentre":
        tiles = []
        for oid in reads[:8]:
            sch = shape(oid)
            tiles.append({"kind": "metricTile",
                          "label": words(re.sub(r"^(list|get|search)", "", oid)).strip().capitalize(),
                          "bindsTo": sch, "operation": oid,
                          "provenance": cite(oid)})
            if sch:
                counts["bound"] += 1
        if tiles:
            regions.insert(0, {"name": "contentBody", "slot": "headline", "components": tiles})

    # --- the selection --------------------------------------------------------------------------
    if pattern in ("listDetail", "approvalInbox", "statusTracker") and det_schema:
        cols = columns_for(det_schema, schemas, limit=16)
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
                                "label": f"The selected {noun}",
                                "bindsTo": det_schema,
                                "columns": cols,
                                "operation": detail_op or collection_op,
                                "provenance": cite(detail_op or collection_op)}]})

    # --- the form --------------------------------------------------------------------------------
    if pattern == "configEditor":
        writer = next((o for o in known if not o.startswith(READS)), None)
        body_schema = None
        if writer:
            rb = ((ops[writer]["op"].get("requestBody") or {}).get("content") or {})
            for b in rb.values():
                found = re.findall(r"#/components/schemas/(\w+)", json.dumps(b.get("schema") or {}))
                if found:
                    body_schema = found[0]
                    break
        fields = columns_for(body_schema, schemas, limit=18) if body_schema else []
        if fields:
            counts["bound"] += 1
            regions.append({"name": "contentBody", "slot": "fields", "components": [
                {"kind": "textField", "label": f.split(".")[-1], "bindsTo": f,
                 "provenance": cite(writer)} for f in fields]})
        else:
            gaps.append({"operation": writer,
                         "why": (f"**`{writer}` declares no request body shape**, so nothing says "
                                 f"what this editor edits. The fields cannot be derived and the "
                                 f"screen needs the contract before it needs a designer."),
                         "source": cite(writer) if writer else "the screen's own operations"})

    # --- actions, and the overlays they raise -----------------------------------------------------
    action_components = []
    for oid in known:
        if oid.startswith(READS):
            continue
        stem = re.match(r"^([a-z]+)", oid)
        label = VERB_LABEL.get(stem.group(1) if stem else "", None)
        if not label:
            label = words(oid).split()[0].capitalize()
        destructive = bool(DESTRUCTIVE.match(oid))
        kind = ("destructiveButton" if destructive
                else "primaryButton" if not action_components else "secondaryButton")
        action_components.append({"kind": kind, "label": label, "operation": oid,
                                  "provenance": cite(oid)})
        if destructive:
            overlays.append({
                "id": "confirm" + oid[0].upper() + oid[1:],
                "component": "confirmDialog",
                "trigger": label,
                "body": (f"**Names what `{oid}` changes and what it leaves alone**, in the "
                         f"consequence rather than the verb. A {noun} this affects should be "
                         f"identified in the dialog, not just counted."),
                "provenance": cite(oid)})
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
    # `authored — …`; everything a person wrote cites something else, or nothing at all. Carried
    # components are grouped into one region per region name, so re-carrying them is a fixed point
    # rather than a fresh region each time.
    MINE = ("contract ", "authored — ")
    keep: dict[str, list] = {}
    for region in (screen.get("layout") or {}).get("regions") or []:
        for c in region.get("components") or []:
            if str(c.get("provenance", "")).startswith(MINE):
                continue
            if not (keep_note(c.get("notes")) or c.get("label")):
                continue
            body = {k: v for k, v in c.items() if k != "notes" or keep_note(v)}
            body["provenance"] = c.get("provenance") or "carried from the previous definition"
            keep.setdefault(region.get("name", "contentBody"), []).append(body)
    carried = sum(len(v) for v in keep.values())
    for name, comps in keep.items():
        regions.append({"name": name, "slot": "carried", "components": comps})
    report["carried components"] += carried

    # --- gaps ----------------------------------------------------------------------------------
    if not known:
        gaps.append({"operation": None,
                     "why": ("**This screen declares no operation the contracts recognise.** "
                             "Nothing fills it, nothing it does is committed anywhere, and its "
                             "shape below is a default rather than a reading."),
                     "source": "the screen's own declarations"})
        report["no known operations"] += 1
    unreached = [o for o in known if not any(
        c.get("operation") == o for r in regions for c in r["components"])]
    if unreached:
        gaps.append({"operation": unreached[0],
                     "why": (f"**{len(unreached)} declared operation"
                             f"{'s' if len(unreached) > 1 else ''} reach no component on this "
                             f"screen**: {', '.join(unreached[:8])}. Either the screen is missing "
                             f"what calls them, or the declaration is residue."),
                     "source": "the screen's own declarations"})
        report["operations reaching nothing"] += len(unreached)
    if reason.startswith("**the screen's operations choose no pattern"):
        report["no pattern evidence"] += 1

    # --- states ---------------------------------------------------------------------------------
    states = {
        "loading": (f"The saved {noun}." if pattern == "configEditor" else f"The {noun} list."),
        "error": f"Could not load. Names which read failed and leaves the {noun} untouched.",
    }
    if pattern == "approvalInbox":
        states["emptyFirstRun"] = ("**Nothing is waiting, which is the good outcome.** An empty "
                                   "queue means every item has been decided; it offers no create "
                                   "action, because creating work is not what it needs.")
    elif pattern == "configEditor":
        states["emptyFirstRun"] = (f"No {noun} configured. Carries the create action and says what "
                                   f"the platform does in the meantime.")
    else:
        states["emptyFirstRun"] = (f"No {noun} yet. Carries the create action; distinct from a "
                                   f"filter that matched nothing.")
    if pattern != "configEditor":
        states["emptyNoResults"] = (f"The filter narrowed it and the {noun} are still there. "
                                    f"Names the active filter and offers to clear it.")
    states["emptyNoAccess"] = ("Names the missing permission. **Never an empty table** — that "
                               "reads as *there is no data* and sends somebody to support with "
                               "the wrong question.")
    for k, v in (screen.get("states") or {}).items():
        # A state a person wrote outranks a derived one. `statesDerived` marks the ones that were
        # not written, and 393 of this population carry it.
        if not screen.get("statesDerived") and k in states and v:
            states[k] = v
    # **A state this generator does not write is not a state it may delete.** It owns six names
    # — loading, error, the three empties, offline — and owning six names does not make it the
    # owner of the block. `denied` is written by the permission work, and the failure states that
    # `navigation.transitions[].onFailure` anchors point at are written by hand; assigning this
    # dict wholesale deleted all of them. Same rule as overlays and gaps, for the same reason.
    for k, v in (screen.get("states") or {}).items():
        if k not in states and v:
            states[k] = v
    if screen.get("offline") or "offline" in (screen.get("states") or {}):
        states["offline"] = (screen.get("states") or {}).get(
            "offline", f"Served from the local journal. Says what is stale and since when.")

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
    _prior = {o.get("id"): o for o in (screen.get("overlays") or [])}
    for _o in overlays:
        _was = _prior.get(_o.get("id")) or {}
        for _half in ("confirm", "dismiss"):
            if _was.get(_half) and _half not in _o:
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
        entry["params"] = [{"name": p, "from": "navigation"} for p in needed]
    if pattern in ("listDetail", "approvalInbox") and det_schema:
        entry["preloaded"] = columns_for(det_schema, schemas, limit=5)
    if entry:
        out["entryState"] = entry
    if screen.get("wireframe"):
        out["wireframe"] = screen["wireframe"]
    out["apisNote"] = (
        f"Rebuilt {STAMP} from the {len(known)} operation"
        f"{'s' if len(known) != 1 else ''} this screen declares, not from a workshop pack — it has "
        f"none. Columns are every field the response schema declares, plumbing aside — narrowing "
        f"them to the ones that matter is work a person still owes this screen.")

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
    for path in files:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
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
        if touched and args.write:
            path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                            encoding="utf-8")
        if touched:
            print(f"  {doc['platform']['code']}  {touched:>4} screens rebuilt from contracts"
                  f"{'  → written' if args.write else ''}")
        done += touched

        if args.sample:
            for s in doc["screens"]:
                if s["id"] in set(args.sample.split(",")):
                    print(yaml.safe_dump(s, sort_keys=False, allow_unicode=True, width=100))

    print(f"\n{done} screens rebuilt\n")
    for k in sorted(report):
        print(f"  {k:<28} {report[k]}")
    if not args.write:
        print("\n(dry run — pass --write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
