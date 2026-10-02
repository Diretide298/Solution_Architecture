#!/usr/bin/env python3
"""Move the workshop-pack console screens to Venue Management and merge the duplicates (2 October 2026).

**Chinmay, 2 October 2026 (batch 1, ADM-049; DEC-100): "They are venue screens."** The 410 screens generated
onto the TICVAI Console (P09) from the client's workshop packs -- Commercial 370 (ADM-048..ADM-317 and
ADM-559..ADM-698), Catalogue lifecycle 20 and Platform rules and workflow 20 -- configure records the venue
owns. They move to Venue Management (P08), appended at the end of its file, and each one that duplicates the
venue's own screen is merged with it, so one surface edits each record. TICVAI staff reach them only through
a platform-staff grant into the tenant (R098). The pre-apply round of the same day: "Duplicate screens: merge
as proposed", ids kept as anchors.

**The ids do not change.** A pushed OpenProject key (APP-SETUP-ADM-049 ...) names the screen id, so the screen
keeps it in its new file and the move is metadata (check-key-stability, C4).

**Two kinds of merge.**
  full     the anchor declares the venue screen's own operations, so two screens on one platform would do
           the same thing (S-DUP-SCREEN). The anchor keeps its id and its place on its board, declares no
           operation of its own and routes to the venue screen (the BO-031 / M24-03 pattern).
  section  the anchor edits the same record as a venue screen through operations the venue screen does not
           declare -- often the slice's setup operation that a pushed ticket names. It becomes a section of
           the venue screen (same component, a route under it) and keeps its operations, so the slice and the
           ticket keep their host; whether its duplicate writer retires is a contract and plan question
           (CHG-MOV-008), not a screen edit.

**Three stay on the console**, because a later decision of the same day says TICVAI staff use them: ADM-068
(DEC-207, TICVAI staff keep the country tax templates) and ADM-619 (DEC-211, a cross-tenant view of TICVAI's
payment operations, which no tenant cell can serve). Their boards' detail screens move; they keep the edge to
the console hub and gain one from Venue Home.

    python3 tools/applied/move-adm049-2-october.py [--apply]

Run once, in worktree screens-move-adm049; a second run finds nothing to move and says so.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCREENS = ROOT / "screens"
P08 = SCREENS / "P08-venue-back-office.yaml"
P09 = SCREENS / "P09-platform-admin-console.yaml"
NOTES = ROOT / "handoff" / "design-notes"
FLOWS = ROOT / "flows"
CONTRACTS = ROOT / "contracts"
DAY = "2 October 2026"

CHG = {
    "move": "CHG-MOV-001", "merge": "CHG-MOV-002", "states": "CHG-MOV-003", "names": "CHG-MOV-004",
    "layout": "CHG-MOV-005", "stepup": "CHG-MOV-006", "bind": "CHG-MOV-007", "gaps": "CHG-MOV-008",
    "canvas": "CHG-MOV-009",
}

KEEP = {
    "ADM-068": "DEC-207 (Chinmay, 2 October, batch 6): TICVAI staff maintain the country tax templates",
    "ADM-619": "DEC-211 (Chinmay, 2 October, batch 6): a cross-tenant view of TICVAI's payment operations",
}
HOME = "BO-100"
CONSOLE_HOME = "ADM-002"

# full merges: the anchor's operations are the venue screen's own (S-DUP-SCREEN on one platform)
FULL = {
    "ADM-097": "BO-441",   # rule priority and conflict: same two operations, "same operation and component"
    "ADM-242": "BO-086",   # approval matrix: same two operations
    "ADM-249": "BO-084",   # unified approval inbox: one queue (design notes), operations a subset of BO-084
    "ADM-252": "BO-391",   # SLA and escalation monitor: same two operations
    "ADM-611": "BO-1146",  # refund policy: the same refund policy record, operations a subset of BO-1146
}
# section merges: the same record as the venue screen, edited through operations it keeps
SECTION = {
    "ADM-049": "BO-009", "ADM-051": "BO-009", "ADM-052": "BO-009",
    "ADM-053": "BO-011", "ADM-178": "BO-011", "ADM-179": "BO-011", "ADM-180": "BO-011", "ADM-181": "BO-011",
    "ADM-119": "BO-007", "ADM-131": "BO-008", "ADM-121": "BO-117",
    "ADM-138": "BO-010", "ADM-140": "BO-010", "ADM-141": "BO-010", "ADM-148": "BO-010", "ADM-157": "BO-010",
    "ADM-158": "BO-010", "ADM-159": "BO-010", "ADM-169": "BO-010", "ADM-172": "BO-010", "ADM-173": "BO-010",
    "ADM-174": "BO-010", "ADM-199": "BO-010", "ADM-210": "BO-010",
    "ADM-145": "BO-084", "ADM-243": "BO-087", "ADM-244": "BO-388",
}
# A/B screens whose emptyFirstRun promised a create action that no operation offers (design-notes corrections)
STATE_FIX = ["ADM-145", "ADM-238", "ADM-240", "ADM-244", "ADM-246", "ADM-247", "ADM-248", "ADM-249", "ADM-250",
             "ADM-251", "ADM-252", "ADM-254", "ADM-255", "ADM-256", "ADM-257", "ADM-584", "ADM-618"]
BOILER = "Carries the create action; distinct from a filter that matched nothing."
BOILER_FIX = ("Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty "
              "list is the good outcome. Distinct from a filter that matched nothing.")
BOILER2 = "Carries the create action and says what the platform does in the meantime."
BOILER2_FIX = ("Offers no create action (nothing on this screen creates one) and says what the platform does in the "
               "meantime.")
# A/B screens whose name carries the pack page number after a tab
# the page number after a real tab, or after the two characters backslash-t the import left in the text
PAGE_NO = re.compile(r"(\t|\\t)\s*\d*\s*$")
NAME_FIX = ["ADM-570", "ADM-581", "ADM-582", "ADM-584", "ADM-587", "ADM-603"]


def in_range(sid: str) -> bool:
    m = re.fullmatch(r"ADM-(\d+)", sid or "")
    return bool(m) and (48 <= int(m.group(1)) <= 317 or 559 <= int(m.group(1)) <= 698)


def read(path: Path):
    raw = path.read_bytes().decode("utf-8")
    return raw, yaml.load(raw.replace("\r\n", "\n"), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


def write(path: Path, raw: str, doc) -> None:
    out = yaml.dump(doc, Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True, width=100)
    path.write_bytes((out.replace("\n", "\r\n") if "\r\n" in raw else out).encode("utf-8"))


def put_after(d: dict, after: str, key: str, value) -> dict:
    """d with key set, placed after `after` when it is new (dump order is the file's order)."""
    if key in d:
        d[key] = value
        return d
    out = {}
    for k, v in d.items():
        out[k] = v
        if k == after:
            out[key] = value
    if key not in out:
        out[key] = value
    d.clear()
    d.update(out)
    return d


def prepend_notes(s: dict, text: str) -> None:
    old = s.get("notes")
    put_after(s, "navigation", "notes", text + ("\n\n" + old if old else ""))


def comps(s):
    for r in ((s.get("layout") or {}).get("regions") or []):
        for c in (r.get("components") or []):
            yield r, c


# ------------------------------------------------------------------------------------------------ screens
def move(s: dict, names: dict, routes: set, log: list) -> None:
    sid = s["id"]
    imp = s.get("implementation") or {}
    imp["app"] = "venue-management-web"
    imp["component"] = str(imp.get("component", "")).replace("apps/ticvai-web/", "apps/venue-management-web/")
    if imp.get("route") in routes:
        imp["route"] = imp["route"].rstrip("/") + "-" + sid.lower()
    routes.add(imp.get("route"))
    wf = s.get("wireframe") or {}
    if str(wf.get("board", "")).startswith("wireframes/P09 TICVAI Web.dc.html"):
        wf["board"] = wf["board"].replace("wireframes/P09 TICVAI Web.dc.html", "wireframes/P08 Venue Management.dc.html")
    for sb in wf.get("stateBoards") or []:
        if str(sb.get("board", "")).startswith("wireframes/P09 TICVAI Web.dc.html"):
            sb["board"] = sb["board"].replace("wireframes/P09 TICVAI Web.dc.html", "wireframes/P08 Venue Management.dc.html")
    nav = s.setdefault("navigation", {})
    entry, exits = nav.get("entryFrom") or [], nav.get("exitTo") or []
    orphan = [p for p in entry if p in KEEP]
    if CONSOLE_HOME in entry or CONSOLE_HOME in exits:
        nav["entryFrom"] = [HOME if x == CONSOLE_HOME else x for x in entry]
        nav["exitTo"] = [HOME if x == CONSOLE_HOME else x for x in exits]
        for t in nav.get("transitions") or []:
            if t.get("to") == CONSOLE_HOME:
                t.clear()
                t.update({"to": HOME, "trigger": "Back to Venue Home",
                          "provenance": f"moved to Venue Management {DAY} ({CHG['move']}); it returned to the "
                                        "console's Platform Dashboard (ADM-002)",
                          "back": True})
    elif orphan:
        nav["entryFrom"] = entry + [HOME]
        nav["exitTo"] = exits + [HOME]
        nav.setdefault("transitions", []).append(
            {"to": HOME, "trigger": "Back to Venue Home",
             "provenance": f"moved to Venue Management {DAY} ({CHG['move']}); its board's hub {orphan[0]} stays on "
                           "the console, so Venue Home is its venue-side way in", "back": True})
    note = (f"**Moved to Venue Management (P08) on {DAY}** (Chinmay, DEC-100: \"they are venue screens\"; "
            f"{CHG['move']}). It configures a record the venue owns, so the venue's own staff use it here, inside "
            "the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), "
            "never from the console directly. The id is kept, so its tickets keep their keys.")
    if orphan:
        note += (f" Its board's hub {orphan[0]} stays on the console ({KEEP[orphan[0]]}); this screen keeps that "
                 f"edge and is also reached from {HOME} Venue Home.")
    prepend_notes(s, note)
    log.append(f"moved {sid}")


def full_merge(s: dict, target: str, names: dict, log: list) -> None:
    sid = s["id"]
    tname = names[target]
    dropped = [a.get("operationId") for a in s.get("apis") or [] if a.get("operationId")]
    s["apis"] = []
    for _, c in comps(s):
        c.pop("operation", None)
    for o in s.get("overlays") or []:
        for k in ("confirm", "dismiss"):
            if isinstance(o.get(k), dict):
                o[k].pop("operation", None)
    nav = s.setdefault("navigation", {})
    for t in nav.get("transitions") or []:
        t.pop("operation", None)
        t.pop("carries", None)
    if target not in (nav.get("exitTo") or []):
        nav["exitTo"] = (nav.get("exitTo") or []) + [target]
    nav.setdefault("transitions", []).append(
        {"to": target, "trigger": f"Open {tname}",
         "provenance": f"merged into {target} {DAY} ({CHG['merge']})"})
    states = s.get("states") or {}
    if "emptyNoAccess" in states:
        states["emptyNoAccess"] = (f"Shown when the caller lacks the permission {target} {tname} requires; this id "
                                   "has no operation of its own since the merge, so it names that screen's.")
    s["apisNote"] = (f"No operations of its own since {DAY} ({CHG['merge']}): merged into {target} {tname}, whose "
                     f"operations it routes to ({', '.join(dropped)}).")
    s["purpose"] = str(s.get("purpose") or "").rstrip() + f" (merged into {target} {tname})."
    prepend_notes(s, f"**Merged into {target} {tname}** (decided {DAY}, Chinmay: DEC-100 and the pre-apply round, "
                     f"\"duplicate screens: merge as proposed\"; {CHG['merge']}). On one platform it declared the "
                     f"same operations as {target} (check-screen-wiring S-DUP-SCREEN). **One implementation, both "
                     f"ids kept**, as the M24-03 merges do: this id stays for traceability and routes to {target}, "
                     "and nothing on it is built separately.")
    log.append(f"full merge {sid} -> {target}: dropped {', '.join(dropped)}")


def section_merge(s: dict, target: dict, log: list) -> None:
    sid, tid, tname = s["id"], target["id"], target["name"]
    imp = s["implementation"]
    timp = target.get("implementation") or {}
    tail = str(imp.get("route", "")).rstrip("/").split("/")[-1]
    imp["route"] = str(timp.get("route", "")).rstrip("/") + "/" + tail
    imp["component"] = timp.get("component", imp.get("component"))
    nav = s.setdefault("navigation", {})
    if tid not in (nav.get("exitTo") or []):
        nav["exitTo"] = (nav.get("exitTo") or []) + [tid]
        nav.setdefault("transitions", []).append(
            {"to": tid, "trigger": f"Open {tname}",
             "provenance": f"a section of {tid} since {DAY} ({CHG['merge']})"})
    s["purpose"] = str(s.get("purpose") or "").rstrip() + f" (a section of {tid} {tname} since {DAY})."
    prepend_notes(s, f"**Merged into {tid} {tname} as a section of it** (decided {DAY}, Chinmay: DEC-100, \"merge "
                     f"them with BO-008 to BO-011 so one surface edits each record\", and the pre-apply round; "
                     f"{CHG['merge']}). It edits the same record as {tid}: it renders inside {tid}'s component, under "
                     f"its route, and keeps its own operations, because the first-release slice and its ticket name "
                     "them. Whether those duplicate writers retire in favour of the venue screen's is a contract and "
                     f"plan question ({CHG['gaps']}).")
    log.append(f"section merge {sid} -> {tid}")


def fix_layouts(S: dict, log: list) -> None:
    """The A/B design-note corrections that are screen edits (CHG-MOV-005, -006, -007)."""
    # ADM-048: the venue hub reads venue-scoped records; listMembershipCommercialPricing needs a platform
    # permission (PLATFORM_TENANT_VIEW) at tenant scope, which nobody holds in Venue Management.
    s = S["ADM-048"]
    s["apis"] = [a for a in s["apis"] if a.get("operationId") != "listMembershipCommercialPricing"]
    log.append("ADM-048 drops listMembershipCommercialPricing")
    # ADM-088: the strategy's state changes on its builder (ADM-089); the command centre lists.
    s = S["ADM-088"]
    s["apis"] = [a for a in s["apis"] if a.get("operationId") != "transitionDynamicPricingStrategy"]
    for r, c in list(comps(s)):
        if c.get("operation") == "transitionDynamicPricingStrategy":
            r["components"].remove(c)
    s["overlays"] = [o for o in s.get("overlays") or []
                     if (o.get("confirm") or {}).get("operation") != "transitionDynamicPricingStrategy"]
    if not s["overlays"]:
        del s["overlays"]
    s["apisNote"] = (str(s.get("apisNote") or "") + f" **{DAY} ({CHG['merge']}):** activating, pausing or retiring a "
                     "strategy happens on ADM-089, the strategy builder, which declares "
                     "transitionDynamicPricingStrategy; the command centre lists, so one surface changes a "
                     "strategy's state (and BO-528, the rental view, is not its twin).").strip()
    log.append("ADM-088 drops transitionDynamicPricingStrategy")
    # ADM-145: delegation is set ahead of time (BO-087); decideApprovalRequest has no delegate.
    s = S["ADM-145"]
    for r, c in list(comps(s)):
        if c.get("label") == "Delegate" and not c.get("operation"):
            r["components"].remove(c)
    s["requiresModule"] = "core"
    log.append("ADM-145 drops Delegate, requiresModule core")
    # ADM-157: its own purpose (the pack text was ADM-187's).
    s = S["ADM-157"]
    s["purpose"] = ("Test a promotion before it goes live: run a sample basket through the promotion engine "
                    "(evaluatePromotions) and replay it against past sales (simulatePromotion), to see which offer "
                    f"applies, what it costs and what it would have done. (A section of BO-010 Promotions & Coupons "
                    f"since {DAY}.)")
    s["purposeNote"] = (f"Purpose rewritten {DAY} ({CHG['layout']}): the pack text was shared word for word with "
                        "ADM-187 and did not describe this screen (design-notes correction ticketing-backoffice ADM-157).")
    # ADM-241: free-text fields drawn as drop-downs.
    s = S["ADM-241"]
    kinds = {"Workflow Name": ("textField", "workflowName"), "Module": ("textField", "module"),
             "Business Process": ("textField", "businessProcess"), "Owner": ("textField", "owner"),
             "Version": ("textField", "version"), "Priority": ("textField", "priority"),
             "Effective Dates": ("datePicker", "effectiveFrom")}
    for _, c in comps(s):
        if c.get("label") in kinds and c.get("kind") == "selectField":
            k, f = kinds[c["label"]]
            c["kind"] = k
            c["bindsTo"] = f"VisualWorkflowDesignerInput.{f}"
            if c["label"] == "Effective Dates":
                c["notes"] = "From and to: effectiveFrom and effectiveTo on VisualWorkflowDesignerInput."
        if c.get("label") == "Save changes" and not c.get("operation"):
            c["operation"] = "setVisualWorkflow"
    # ADM-245: the action types are one choice, not eight buttons that would run them.
    s = S["ADM-245"]
    acts = {"Create Approval", "Create Task", "Update Status", "Apply Hold", "Release Hold", "Create Notification",
            "Generate Document", "Execute Refund"}
    for r in (s.get("layout") or {}).get("regions") or []:
        cs = r.get("components") or []
        if any(c.get("label") in acts for c in cs):
            prov = next(c.get("provenance") for c in cs if c.get("label") in acts)
            r["components"] = [c for c in cs if c.get("label") not in acts]
            r["components"][:0] = [{
                "kind": "multiSelect", "label": "Allowed actions",
                "bindsTo": "TriggerActionCrossModuleOrchestrationConfigurationInput.allowedActions",
                "notes": "The pack's action types (Create Approval, Create Task, Update Status, Apply Hold, Release Hold, "
                         "Create Notification, Generate Document, Execute Refund) are options of allowedActions, not "
                         f"buttons: choosing Execute Refund here refunds nothing ({CHG['layout']}).",
                "provenance": prov},
                {"kind": "primaryButton", "label": "Save orchestration", "operation": "setTriggerActionCross",
                 "provenance": "contract approvals.yaml PUT /trigger-action-cross"}]
    # ADM-251: the error types filter the list.
    s = S["ADM-251"]
    errs = {"Business Rule Failure", "Missing Data", "Permission Failure", "Integration Failure", "Action Failure",
            "Duplicate Event", "Service Unavailable", "Configuration Error"}
    for r in (s.get("layout") or {}).get("regions") or []:
        cs = r.get("components") or []
        if any(c.get("label") in errs for c in cs):
            prov = next(c.get("provenance") for c in cs if c.get("label") in errs)
            r["components"] = [c for c in cs if c.get("label") not in errs]
            body = next(x for x in s["layout"]["regions"] if x.get("name") == "contentBody")
            body["components"].insert(0, {
                "kind": "multiSelect", "label": "Error type",
                "bindsTo": "WorkflowExceptionFailureRecoveryCenterView.errorType",
                "notes": "The pack's error types (Business Rule Failure, Missing Data, Permission Failure, Integration "
                         "Failure, Action Failure, Duplicate Event, Service Unavailable, Configuration Error) filter "
                         f"the list by errorType; they are not actions ({CHG['layout']}).",
                "provenance": prov})
            break
    # ADM-257: the table's columns, from the response schema.
    s = S["ADM-257"]
    cols = [f"AiWorkflowIntelligenceAutonomousGovernanceCenterView.{f}" for f in
            ("useCase", "aiService", "autonomyLevel", "decisionScope", "confidenceThreshold",
             "humanApprovalRequirement", "executionVolume", "exceptionRate", "overrideRate", "lastReview", "owner")]
    for _, c in comps(s):
        if c.get("kind") in ("dataTable", "detailPanel") and not c.get("columns"):
            c["columns"] = list(cols)
    # ADM-247: the publish action raises the step-up its operation demands.
    s = S["ADM-247"]
    for r, c in comps(s):
        if c.get("label") == "Publish Now":
            c["operation"] = "approveVersioningGovernance"
            c["notes"] = ("Publishes the workflow version; approveVersioningGovernance demands step-up (mfa), so the "
                          "confirmation asks for the authentication code in place.")
    for r in s["layout"]["regions"]:
        if r.get("name") == "actionBar":
            r["components"] += [
                {"kind": "textField", "label": "Authentication code", "operation": "verifyMfaChallenge",
                 "notes": "Asked in place inside the Publish confirmation; its result is the stepUpToken "
                          "approveVersioningGovernance needs (audit R126).",
                 "provenance": "contract identity.yaml POST /auth/mfa/challenge/{challengeId}/verify"},
                {"kind": "secondaryButton", "label": "Email me a code instead", "operation": "createMfaChallenge",
                 "notes": "Opens the step-up challenge for Publish; the emailed code is the fallback to the "
                          "authenticator app (audit R126 (5)).",
                 "provenance": "contract identity.yaml POST /auth/mfa/challenge"}]
    s.setdefault("overlays", []).append({
        "id": "confirmPublishVersion", "component": "confirmDialog", "trigger": "Publish Now",
        "body": "**Says which workflow version goes live, where (rolloutScope) and from when.** Collects what "
                "`approveVersioningGovernance` sends and asks for the authentication code in place, because the "
                f"operation demands step-up (mfa) and refuses without a fresh stepUpToken ({CHG['stepup']}). "
                "Dismissing sends nothing.",
        "confirm": {"label": "Publish", "operation": "approveVersioningGovernance"},
        "dismiss": {"label": "Cancel"},
        "provenance": "contract approvals.yaml PUT /versioning-governance"})
    s["apis"] += [
        {"operationId": "createMfaChallenge", "contract": "identity",
         "purpose": "The step-up challenge Publish asks for in place", "trigger": "onAction"},
        {"operationId": "verifyMfaChallenge", "contract": "identity",
         "purpose": "Answers the step-up challenge; its token goes into approveVersioningGovernance",
         "trigger": "onAction"}]
    # ADM-603: the read of a B2B account's payment terms now exists (getB2bPaymentTerms).
    s = S["ADM-603"]
    s["apis"].append({"operationId": "getB2bPaymentTerms", "contract": "payments",
                      "purpose": "Read the account's current payment terms before they are changed",
                      "trigger": "onLoad",
                      "provenance": f"deferred workshop-pack gap closed {DAY} ({CHG['bind']})"})
    for r in s["layout"]["regions"]:
        if r.get("name") == "contentBody":
            r["components"].insert(0, {
                "kind": "detailPanel", "label": "Current payment terms", "bindsTo": "B2bPaymentTerms",
                "columns": [f"B2bPaymentTerms.{f}" for f in ("creditLimit", "paymentTermDays", "billingCycle",
                                                            "purchaseOrderRequired", "depositPercent",
                                                            "balanceDue", "atLimit", "overrideApprovalRole")],
                "operation": "getB2bPaymentTerms",
                "notes": "What setB2bPaymentTerms will replace, read for the picked account, so the form opens "
                         "on the saved terms rather than empty (PR-9).",
                "provenance": "contract payments.yaml GET /b2b-credit-accounts/{accountId}/terms"})
            break
    s["gaps"] = [g for g in s.get("gaps") or [] if "CHG-WIR-027" not in str(g.get("why"))]
    log.append("layout fixes on ADM-145, 157, 241, 245, 247, 251, 257, 603")


def apply_screens(apply: bool) -> dict:
    raw8, d8 = read(P08)
    raw9, d9 = read(P09)
    names = {s["id"]: s["name"] for s in d8["screens"] + d9["screens"]}
    moving = [s for s in d9["screens"] if in_range(s["id"]) and s["id"] not in KEEP]
    if not moving:
        print("nothing to move: the workshop-pack screens are already in P08")
        return {}
    S = {s["id"]: s for s in moving}
    B = {s["id"]: s for s in d8["screens"]}
    log: list = []
    routes = {str((s.get("implementation") or {}).get("route")) for s in d8["screens"]}
    hubs, orphans = [], []
    for s in moving:
        nav = s.get("navigation") or {}
        if CONSOLE_HOME in (nav.get("entryFrom") or []):
            hubs.append(s["id"])
        elif any(p in KEEP for p in nav.get("entryFrom") or []):
            orphans.append(s["id"])
    fix_layouts(S, log)
    for sid in STATE_FIX:
        st = S[sid].get("states") or {}
        if BOILER in str(st.get("emptyFirstRun") or ""):
            st["emptyFirstRun"] = st["emptyFirstRun"].replace(BOILER, BOILER_FIX)
            log.append(f"{sid} emptyFirstRun rewritten")
        elif BOILER2 in str(st.get("emptyFirstRun") or ""):
            st["emptyFirstRun"] = st["emptyFirstRun"].replace(BOILER2, BOILER2_FIX)
            log.append(f"{sid} emptyFirstRun rewritten")
        else:
            log.append(f"{sid} emptyFirstRun already free of the boilerplate: {str(st.get('emptyFirstRun'))[:60]!r}")
    for sid in NAME_FIX:
        new = PAGE_NO.sub("", S[sid]["name"]).rstrip()
        log.append(f"{sid} name {S[sid]['name']!r} -> {new!r}")
        S[sid]["name"] = new
        names[sid] = new
    for s in moving:
        move(s, names, routes, log)
    for sid, tid in FULL.items():
        full_merge(S[sid], tid, names, log)
    for sid, tid in SECTION.items():
        section_merge(S[sid], B[tid], log)
    # Venue Home is the way in for the boards' hubs, and for the detail screens whose hub stays on the console.
    home = B[HOME]
    hn = home["navigation"]
    for sid in hubs + orphans:
        if sid not in hn["exitTo"]:
            hn["exitTo"].append(sid)
            hn.setdefault("transitions", []).append(
                {"to": sid, "trigger": PAGE_NO.sub("", names[sid]).rstrip(),
                 "provenance": f"moved to Venue Management {DAY} ({CHG['move']}); "
                               + ("its workshop board's hub" if sid in hubs else "its board's hub stays on the console")})
    d9["screens"] = [s for s in d9["screens"] if s["id"] not in S]
    d8["screens"] = d8["screens"] + moving
    d8["platform"]["screenCount"] = len(d8["screens"])
    d9["platform"]["screenCount"] = len(d9["screens"])
    for line in log:
        print("  " + line)
    print(f"moved {len(moving)} screens ({len(hubs)} board hubs, {len(orphans)} under a console hub); "
          f"{len(FULL)} full merges, {len(SECTION)} section merges; P08 {len(d8['screens'])}, P09 {len(d9['screens'])}")
    if apply:
        write(P08, raw8, d8)
        write(P09, raw9, d9)
    return {"moved": [s["id"] for s in moving], "names": names, "renamed": {sid: names[sid] for sid in NAME_FIX},
            "declared": {s["id"]: {a.get("operationId") for a in s.get("apis") or []} for s in d8["screens"]}}


# ------------------------------------------------------------------------------------------------ contracts
def op_ranges(lines):
    """[(operationId, start, end)] for every operation block in an OpenAPI file, by indentation."""
    out = []
    verbs = re.compile(r"^(\s+)(get|post|put|patch|delete):\s*$")
    i = 0
    while i < len(lines):
        m = verbs.match(lines[i])
        if not m:
            i += 1
            continue
        ind = len(m.group(1))
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > ind):
            j += 1
        oid = None
        for k in range(i, j):
            mm = re.match(r"^\s+operationId:\s*(\S+)", lines[k])
            if mm:
                oid = mm.group(1).strip("'\"")
                break
        out.append((oid, i, j))
        i = j
    return out


def apply_contracts(apply: bool, moved: list, renamed: dict, declared: dict) -> None:
    moved = set(moved)
    drop = {("listMembershipCommercialPricing", "ADM-048"), ("transitionDynamicPricingStrategy", "ADM-088")}
    add = {"createMfaChallenge": "P08 ADM-247 Versioning, Governance, Approval & Publication",
           "verifyMfaChallenge": "P08 ADM-247 Versioning, Governance, Approval & Publication"}
    entry = re.compile(r"^(\s*-\s+)(['\"]?)P09 (ADM-\d+)\b(.*)$")
    for f in sorted(CONTRACTS.glob("*/*.yaml")):
        text = f.read_bytes().decode("utf-8")
        crlf = "\r\n" in text
        lines = text.replace("\r\n", "\n").split("\n")
        changed = 0
        ranges = op_ranges(lines)
        owner = {}
        for oid, a, b in ranges:
            for k in range(a, b):
                owner[k] = oid
        out = []
        for k, ln in enumerate(lines):
            m = entry.match(ln)
            if m and m.group(3) in moved:
                sid, oid = m.group(3), owner.get(k)
                if (oid, sid) in drop or (oid and oid not in declared.get(sid, set())):
                    changed += 1
                    continue
                rest = m.group(4)
                if sid in renamed:
                    q = m.group(2)
                    rest = " " + (renamed[sid].replace("\\", "\\\\").replace('"', '\\"') if q == '"' else renamed[sid]) + q
                ln = f"{m.group(1)}{m.group(2)}P08 {sid}{rest}"
                changed += 1
            out.append(ln)
        # additions: after the operation's last consumed-by entry
        for oid, line in add.items():
            rs = [(a, b) for o, a, b in op_ranges(out) if o == oid]
            if not rs or any(line in x for x in out[rs[0][0]:rs[0][1]]):
                continue
            a, b = rs[0]
            idx = next((k for k in range(a, b) if re.match(r"^\s+x-ticvai-consumed-by:\s*$", out[k])), None)
            if idx is None:
                continue
            k = idx + 1
            last = None
            while k < b and re.match(r"^\s*-\s", out[k]):
                last = k
                k += 1
            pref = re.match(r"^(\s*-\s+)(['\"]?)", out[last])
            q = pref.group(2)
            new = f"{pref.group(1)}{q}{line}{q}"
            # keep the list in order
            pos = idx + 1
            while pos <= last and out[pos].strip().lstrip("- ").strip("'\"") < line:
                pos += 1
            out.insert(pos, new)
            changed += 1
        if changed:
            print(f"  {f.relative_to(ROOT).as_posix()}: {changed} consumed-by line(s)")
            if apply:
                body = "\n".join(out)
                f.write_bytes((body.replace("\n", "\r\n") if crlf else body).encode("utf-8"))


# ------------------------------------------------------------------------------------------------ flows
def apply_flows(apply: bool, moved: list) -> None:
    moved = set(moved)
    for f in sorted(FLOWS.glob("F*.yaml")):
        text = f.read_bytes().decode("utf-8")
        doc = yaml.load(text.replace("\r\n", "\n"), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
        steps = {st.get("screen") for st in doc.get("steps") or []}
        if not steps & moved:
            continue
        p09 = {x for x in steps if str(x).startswith("ADM-")}
        allmoved = p09 <= moved and steps <= (moved | {x for x in steps if str(x).startswith("BO-")})
        crlf = "\r\n" in text
        lines = text.replace("\r\n", "\n").split("\n")
        out = []
        for ln in lines:
            if ln == "- P09 TICVAI Web":
                out.append("- P08 Venue Management" if allmoved else ln)
                if not allmoved:
                    out.append("- P08 Venue Management")
                continue
            if allmoved and ln == "actor: platformAdmin":
                ln = "actor: venueManager"
            out.append(ln)
        if out != lines:
            print(f"  {f.name}: platform {'renamed' if allmoved else 'P08 added'}")
            if apply:
                body = "\n".join(out)
                f.write_bytes((body.replace("\n", "\r\n") if crlf else body).encode("utf-8"))


OLD_PATH = re.compile(r"screens/P09-platform-admin-console\.yaml#(ADM-\d+)")


def repoint_paths(apply: bool) -> None:
    """A source that cites a moved screen by its old file names the file it is in now. check-design-notes
    resolves `screens/<file>#<id>`, so a stale path is a broken source. Idempotent: run after the move."""
    raw8, d8 = read(P08)
    moved = {s["id"] for s in d8["screens"] if in_range(s["id"])}
    fix = lambda t: OLD_PATH.sub(lambda m: ("screens/P08-venue-back-office.yaml#" if m.group(1) in moved
                                            else "screens/P09-platform-admin-console.yaml#") + m.group(1), t)

    def walk(x):
        if isinstance(x, str):
            return fix(x)
        if isinstance(x, list):
            return [walk(v) for v in x]
        if isinstance(x, dict):
            return {k: walk(v) for k, v in x.items()}
        return x

    n = 0
    for i, s in enumerate(d8["screens"]):
        if s["id"] in moved:
            new = walk(s)
            if new != s:
                d8["screens"][i] = new
                n += 1
    print(f"  P08: {n} moved screen(s) cite their own old path; repointed")
    if apply and n:
        write(P08, raw8, d8)
    for f in sorted(NOTES.glob("*.yaml")):
        raw = f.read_bytes().decode("utf-8")
        new = fix(raw)
        if new != raw:
            print(f"  {f.relative_to(ROOT).as_posix()}: {len(OLD_PATH.findall(raw)) - len(OLD_PATH.findall(new))} "
                  "source(s) repointed")
            if apply:
                f.write_bytes(new.encode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    r = apply_screens(a.apply)
    if r:
        apply_contracts(a.apply, r["moved"], r["renamed"], r["declared"])
        apply_flows(a.apply, r["moved"])
    repoint_paths(a.apply)
    print("applied" if a.apply else "dry run: --apply writes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
