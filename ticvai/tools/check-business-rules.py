#!/usr/bin/env python3
"""Hold the Block A business rules of 3 October 2026 (Chinmay) in the contracts, so they cannot quietly come back.

Change log CHG-RUL-001 to CHG-RUL-021 (changes/entries/CHG-RUL-*.yaml); the answers are in
`docs/active/decisions/answers-3-october-business-rules.md` ("Block A audit business rules" and "Asked as
questions instead of defaults"). The r2 Block A audit (CHG-AUD-001 pattern 4) found contract rules that
disagreed with the screens that call them. Each rule below is one decision; each fails on the package before
the decision and passes after it. Two rules are general, because the same gap can open on any operation:

  BR-STREAM        An operation answers with `text/event-stream` exactly when it declares
                   `x-ticvai-streaming: sse`, and then names its events (`x-ticvai-sse-events`) and keeps a
                   JSON answer for a client that does not ask for the stream. `sendAiMessage` streams (CHG-RUL-002).
  BR-PAIR-REFUSAL  An update that takes the same request schema as a create declares every refusal (4xx) the
                   create declares: the same body passes the same rules (`updateDashboard` skipped the refresh
                   budget, CHG-RUL-008). Pairs found before 3 October and not named by a rule are exempt below,
                   each with its reason.

And one rule per decision:

  BR-SPLIT         (CHG-RUL-001) Five split methods; `closeTableVisit` takes a payment without `subBillId` (an
                   unsplit bill is one sub-bill); `splitBill` and `closeTableVisit` state the outlet's payment
                   timing (`paymentTiming`, send first or pay first).
  BR-VISIT-PLAN    (CHG-RUL-003, CHG-RUL-009) `VisitPlanUpdate` has `addAddOn` and `removeAddOn`; the plan is built
                   and changed in an anonymous guest session and moves to the account on sign-in; booking needs a
                   signed-in guest (`sign-in-required`).
  BR-PO            (CHG-RUL-004) A purchase order request requires neither a requisition nor a quotation (blanket
                   and RFQ-award orders), names its `kind`, and refuses a standard order without an approved
                   requisition (`requisition-required`); the order goes through the approval matrix.
  BR-PAY-LINK      (CHG-RUL-005, CHG-RUL-021) `createPaymentLink` answers 200 with the live link it already has
                   and 409 `order-already-paid` for a paid order; `cancelPaymentLink` (ORDER_CREATE) cancels a live
                   link and refuses one that is not live.
  BR-REPORT-RUNS   (CHG-RUL-006) `listReportExecutions`: `mineOnly` is a filter, and seeing other people's runs
                   does not need `REPORT_MANAGE`.
  BR-CONTRAST      (CHG-RUL-007) `Theme` lists its WCAG AA pairs (`x-ticvai-contrast-pairs`): every colour named
                   exists, text pairs need 4.5:1, large text and non-text pairs 3:1.
  BR-WO-CANCEL     (CHG-RUL-010) `cancelWorkOrder` refuses only once labour time or a part is recorded
                   (`work-recorded`).
  BR-INCIDENT      (CHG-RUL-011) Incidents: reported, investigating, escalated (optional), closed; reopen to
                   investigating with a reason; each change logged. Checked in the contract and `states/incident.yaml`.
  BR-FARE          (CHG-RUL-012) Fare tables are versioned by `effectiveFrom`: a future table sits beside the
                   current one (`FareTable.upcoming`) and a quote prices at travel time (`travelAt`).
  BR-SESSIONS-DOOR (CHG-RUL-015) `listActiveSessions` and `forceLogout` admit a call with no session (`{}`) and
                   carry the supervisor's PIN step-up themselves.
  BR-ATTENDANCE    (CHG-RUL-016) `recordAttendance` acts on the caller (`x-ticvai-self-scoped: principal`, no
                   person in the body); `amendAttendance` is the supervisor's correction.
  BR-AI-CURRENCY   (CHG-RUL-017) The AI spend ceiling defaults to the tenant's billing currency, never USD.
  BR-QR            (CHG-RUL-018) The admission QR (`getEntitlementCredential.rotation`) steps every 30 seconds by
                   default (GST-055).
  BR-NEW-OPS       (CHG-RUL-013) `listMyTableReservations` (self-scoped, paged), `listBookableOutlets` (public,
                   published, paged), `uploadIncidentMedia` and `addIncidentPerson` exist.

The step-up rule of `rejectShiftVariance` (CHG-RUL-014), and of `closeShift`, `acceptShiftVariance`,
`withdrawFromDepositBox` and the 20 MFA step-ups (CHG-RUL-019, CHG-RUL-020), is held by `check-step-up.py`
(SU-CARRIER), which asks every step-up operation where it carries the step-up.

    python3 tools/check-business-rules.py
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]

# Operations whose answer streams, by decision. A new streaming operation declares itself and BR-STREAM holds it.
STREAMING_REQUIRED = {"sendAiMessage": "Chinmay, 3 October: stream answers (CHG-RUL-002)"}

# **BR-PAIR-REFUSAL exemptions**: pairs found on 3 October that no business rule named. Each is a judgement
# (an update may not be able to meet the create's refusal, e.g. a reservation already holding its table), so
# each is listed with why it is not fixed here. A new pair is not exempt.
PAIR_EXEMPT = {
    ("createTableReservation", "updateTableReservation"):
        "409 on create is a slot already full; the update re-checks capacity under 422 (not reviewed by a rule)",
    ("createTableReservationForGuest", "updateTableReservation"):
        "the staff create's 400/409 are about naming the guest, which an update does not do (not reviewed)",
    ("createReport", "updateReport"):
        "400 on create is the definition's validation; whether update shares it is open (not reviewed)",
    ("createRotaAssignment", "updateRotaAssignment"):
        "409 on create is a double booking; whether update re-checks it is open (not reviewed)",
    ("createTicketTemplate", "updateTicketTemplate"):
        "400 on create is the template's validation; whether update shares it is open (not reviewed)",
}

PARSE_ERRORS: list = []

WCAG_MIN = {"text": 4.5, "largeText": 3.0, "nonText": 3.0}


def load(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8")) or {}


def operations():
    out = {}
    for f in sorted((ROOT / "contracts").rglob("*.yaml")):
        if "frozen" in f.parts:
            continue
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception as e:  # a contract that does not parse hides every rule in it: fail, never skip
            PARSE_ERRORS.append(f"{f.relative_to(ROOT)} does not parse: {str(e).splitlines()[-1]}")
            continue
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for method, op in item.items():
                if isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = (f, path, method, op, doc)
    return out


def schema_of(doc, node):
    """Resolve a local `#/components/schemas/X` reference once (and allOf members), else the node."""
    if not isinstance(node, dict):
        return {}
    ref = node.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
        return ((doc.get("components") or {}).get("schemas") or {}).get(ref.rsplit("/", 1)[1]) or {}
    return node


def props(doc, node):
    node = schema_of(doc, node)
    out = dict(node.get("properties") or {})
    for part in node.get("allOf") or []:
        out.update(props(doc, part))
    return out


def body_schema(op):
    return (((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {}).get("schema") or {}


def problem_types(op):
    s = json.dumps(op.get("responses") or {}, default=str)
    return set(re.findall(r"[a-z]+(?:-[a-z]+)+", s))


def text(op):
    return json.dumps(op, default=str)


def main() -> int:
    ops = operations()
    errors = collections.defaultdict(list)

    def need(rule, cond, msg):
        if not cond:
            errors[rule].append(msg)

    def op(oid):
        return ops.get(oid, (None, None, None, {}, {}))

    # -------------------------------------------------------------- BR-STREAM (general)
    for oid, (f, path, method, o, doc) in sorted(ops.items()):
        streams = any("text/event-stream" in ((r or {}).get("content") or {})
                      for r in (o.get("responses") or {}).values() if isinstance(r, dict))
        declared = o.get("x-ticvai-streaming")
        if streams and declared != "sse":
            errors["BR-STREAM"].append(f"{oid} ({f.name}): answers text/event-stream without x-ticvai-streaming: sse")
        if declared:
            ok200 = "text/event-stream" in (((o.get("responses") or {}).get("200") or {}).get("content") or {})
            need("BR-STREAM", ok200, f"{oid}: declares streaming and has no 200 text/event-stream response")
            need("BR-STREAM", bool(o.get("x-ticvai-sse-events")), f"{oid}: streams and names no x-ticvai-sse-events")
            json_too = "application/json" in (((o.get("responses") or {}).get("200") or {}).get("content") or {})
            need("BR-STREAM", json_too, f"{oid}: streams and keeps no application/json answer for other clients")
    for oid, why in STREAMING_REQUIRED.items():
        need("BR-STREAM", op(oid)[3].get("x-ticvai-streaming") == "sse", f"{oid} must stream ({why})")

    # -------------------------------------------------------------- BR-PAIR-REFUSAL (general)
    by_schema = collections.defaultdict(list)
    for oid, (f, path, method, o, doc) in ops.items():
        ref = body_schema(o).get("$ref")
        if ref:
            codes = {str(k) for k in (o.get("responses") or {}) if str(k)[0] == "4"} - {"401", "403", "404", "429"}
            by_schema[(f.name, ref)].append((oid, method, codes))
    for (fname, ref), members in sorted(by_schema.items()):
        creates = [m for m in members if m[1] == "post" and m[0].startswith("create")]
        updates = [m for m in members if m[1] in ("put", "patch") and m[0].startswith(("update", "set", "replace"))]
        for c in creates:
            for u in updates:
                missing = c[2] - u[2]
                if missing and (c[0], u[0]) not in PAIR_EXEMPT:
                    errors["BR-PAIR-REFUSAL"].append(
                        f"{u[0]} takes {c[0]}'s body ({ref.rsplit('/', 1)[1]}) and does not declare its "
                        f"{', '.join(sorted(missing))}")

    # -------------------------------------------------------------- BR-SPLIT
    f, _, _, split, doc = op("splitBill")
    methods = set((((doc.get("components") or {}).get("schemas") or {}).get("SplitMethod") or {}).get("enum") or [])
    need("BR-SPLIT", {"byAmount", "byCovers", "byCategory", "byLine", "bySeat"} <= methods,
         f"SplitMethod lacks a method: has {sorted(methods)}")
    _, _, _, close, cdoc = op("closeTableVisit")
    pay = (props(cdoc, body_schema(close)).get("payments") or {}).get("items") or {}
    need("BR-SPLIT", "subBillId" not in (schema_of(cdoc, pay).get("required") or []),
         "closeTableVisit still requires payments[].subBillId (an unsplit bill closes as one sub-bill)")
    for oid in ("splitBill", "closeTableVisit"):
        need("BR-SPLIT", "paymentTiming" in text(op(oid)[3]), f"{oid} does not state the outlet's payment timing")

    # -------------------------------------------------------------- BR-VISIT-PLAN
    _, _, _, upd, vdoc = op("updateVisitPlan")
    change = schema_of(vdoc, ((props(vdoc, body_schema(upd)).get("changes") or {}).get("items") or {}))
    kinds = set(((change.get("properties") or {}).get("op") or {}).get("enum") or [])
    need("BR-VISIT-PLAN", {"addAddOn", "removeAddOn"} <= kinds,
         f"VisitPlanUpdate change kinds lack addAddOn/removeAddOn: {sorted(kinds)}")
    need("BR-VISIT-PLAN", "sign-in-required" in problem_types(op("bookVisitPlan")[3]),
         "bookVisitPlan does not refuse an anonymous session (sign-in-required)")
    need("BR-VISIT-PLAN", "moves to the account" in text(op("generateVisitPlan")[3]),
         "generateVisitPlan does not say the anonymous plan moves to the account on sign-in")

    # -------------------------------------------------------------- BR-PO
    _, _, _, cpo, idoc = op("createPurchaseOrder")
    req = schema_of(idoc, body_schema(cpo))
    need("BR-PO", not ({"requisitionId", "quotationId"} & set(req.get("required") or [])),
         "CreatePurchaseOrderRequest still requires requisitionId or quotationId (blanket and RFQ-award orders)")
    need("BR-PO", "kind" in (req.get("properties") or {}), "CreatePurchaseOrderRequest names no kind")
    need("BR-PO", "requisition-required" in problem_types(cpo),
         "createPurchaseOrder does not refuse a standard order without an approved requisition")
    need("BR-PO", "approval matrix" in text(cpo), "createPurchaseOrder does not route through the approval matrix")

    # -------------------------------------------------------------- BR-PAY-LINK
    _, _, _, pl, _ = op("createPaymentLink")
    need("BR-PAY-LINK", "200" in (pl.get("responses") or {}), "createPaymentLink has no 200 for the live link it returns")
    need("BR-PAY-LINK", "order-already-paid" in problem_types(pl), "createPaymentLink does not refuse a paid order 409")
    cpl = op("cancelPaymentLink")[3]
    need("BR-PAY-LINK", cpl.get("x-ticvai-permission") == "ORDER_CREATE" and "payment-link-not-live" in problem_types(cpl),
         "cancelPaymentLink is missing, not under ORDER_CREATE, or does not refuse a link that is not live (CHG-RUL-021)")

    # -------------------------------------------------------------- BR-REPORT-RUNS
    _, _, _, lr, _ = op("listReportExecutions")
    mine = next((p for p in lr.get("parameters") or [] if isinstance(p, dict) and p.get("name") == "mineOnly"), {})
    d = str(mine.get("description") or "")
    need("BR-REPORT-RUNS", "filter" in d and "REPORT_MANAGE" not in d.split("filter")[0],
         "listReportExecutions.mineOnly is not a filter, or other people's runs still need REPORT_MANAGE")
    need("BR-REPORT-RUNS", lr.get("x-ticvai-permission") == "REPORT_VIEW_VENUE",
         "listReportExecutions is not gated by REPORT_VIEW_VENUE")

    # -------------------------------------------------------------- BR-CONTRAST
    _, _, _, st, wdoc = op("setTheme")
    theme = (((wdoc.get("components") or {}).get("schemas") or {}).get("Theme") or {})
    pairs = theme.get("x-ticvai-contrast-pairs") or []
    need("BR-CONTRAST", bool(pairs), "Theme declares no x-ticvai-contrast-pairs")
    tprops = theme.get("properties") or {}
    comp = set(((tprops.get("componentColours") or {}).get("properties") or {}))
    for p in pairs:
        for side in ("foreground", "background"):
            name = str(p.get(side) or "")
            ok = name in tprops or (name.startswith("componentColours.") and name.split(".")[1] in comp | {"*"})
            need("BR-CONTRAST", ok, f"contrast pair names {name!r}, which Theme does not have")
        use, ratio = p.get("use"), float(p.get("ratio") or 0)
        need("BR-CONTRAST", use in WCAG_MIN and ratio >= WCAG_MIN.get(use, 99),
             f"contrast pair {p.get('foreground')} on {p.get('background')}: {use} at {ratio} is below WCAG AA")
    need("BR-CONTRAST", "4.5:1" in text(st) and "3:1" in text(st), "setTheme does not state the AA ratios")

    # -------------------------------------------------------------- BR-WO-CANCEL
    need("BR-WO-CANCEL", "work-recorded" in problem_types(op("cancelWorkOrder")[3]),
         "cancelWorkOrder does not refuse with work-recorded once labour time or a part is recorded")

    # -------------------------------------------------------------- BR-INCIDENT
    _, _, _, ui, mdoc = op("updateIncident")
    ub = props(mdoc, body_schema(ui))
    need("BR-INCIDENT", "escalate" in ub and "reason" in ub, "updateIncident takes no escalate or reason")
    need("BR-INCIDENT", "incident-transition-not-allowed" in problem_types(ui),
         "updateIncident does not refuse a transition outside the incident flow")
    st_inc = load("states/incident.yaml")
    tr = {(t.get("from"), t.get("to")) for t in st_inc.get("transitions") or []}
    need("BR-INCIDENT", ("closed", "underInvestigation") in tr, "states/incident.yaml has no reopen to investigating")
    need("BR-INCIDENT", ("underInvestigation", "actionRequired") not in tr,
         "states/incident.yaml still enters actionRequired (not in the 3 October flow)")

    # -------------------------------------------------------------- BR-FARE
    _, _, _, q, tdoc = op("quoteTransportFare")
    need("BR-FARE", "travelAt" in props(tdoc, body_schema(q)), "FareQuoteRequest has no travelAt")
    ft = props(tdoc, {"$ref": "#/components/schemas/FareTable"})
    need("BR-FARE", "upcoming" in ft and "effectiveTo" in ft, "FareTable has no upcoming version or effectiveTo")

    # -------------------------------------------------------------- BR-SESSIONS-DOOR
    for oid in ("listActiveSessions", "forceLogout"):
        o = op(oid)[3]
        need("BR-SESSIONS-DOOR", {} in (o.get("security") or []), f"{oid} does not admit a call with no session")
        need("BR-SESSIONS-DOOR", bool(o.get("x-ticvai-step-up-carrier")), f"{oid} carries no supervisor step-up")

    # -------------------------------------------------------------- BR-ATTENDANCE
    _, _, _, ra, adoc = op("recordAttendance")
    need("BR-ATTENDANCE", ra.get("x-ticvai-self-scoped") == "principal", "recordAttendance is not self-scoped")
    need("BR-ATTENDANCE", not ({"principalId", "employeeId", "staffPrincipalId"} & set(props(adoc, body_schema(ra)))),
         "recordAttendance takes a person in its body")
    need("BR-ATTENDANCE", op("amendAttendance")[3].get("x-ticvai-permission") == "WORKFORCE_MANAGE",
         "amendAttendance is not the supervisor's (WORKFORCE_MANAGE)")

    # -------------------------------------------------------------- BR-AI-CURRENCY
    ai = (ROOT / "contracts/satellite/ai.yaml").read_text(encoding="utf-8")
    need("BR-AI-CURRENCY", not re.search(r"USD by default|default USD|, USD by default", ai),
         "ai.yaml still defaults the spend ceiling to USD")
    need("BR-AI-CURRENCY", "billing currency" in text(op("setAiSpendCeiling")[3]),
         "setAiSpendCeiling does not default to the tenant's billing currency")

    # -------------------------------------------------------------- BR-QR
    cred = op("getEntitlementCredential")[3]
    rot = (((((cred.get("responses") or {}).get("200") or {}).get("content") or {}).get("application/json") or {})
           .get("schema") or {}).get("properties", {}).get("rotation") or {}
    step = (rot.get("properties") or {}).get("timeStepSeconds") or {}
    need("BR-QR", step.get("default") == 30 and "30 seconds" in str(step.get("description") or ""),
         "getEntitlementCredential rotation.timeStepSeconds is not 30 seconds by decision (GST-055)")

    # -------------------------------------------------------------- BR-NEW-OPS
    for oid in ("listMyTableReservations", "listBookableOutlets", "uploadIncidentMedia", "addIncidentPerson"):
        need("BR-NEW-OPS", oid in ops, f"{oid} is missing")
    if "listMyTableReservations" in ops:
        o = ops["listMyTableReservations"][3]
        need("BR-NEW-OPS", o.get("x-ticvai-self-scoped") == "subject", "listMyTableReservations is not self-scoped")
    for oid in ("listMyTableReservations", "listBookableOutlets"):
        if oid in ops:
            names = {str(p.get("$ref", "")).rsplit("/", 1)[-1] for p in ops[oid][3].get("parameters") or []}
            need("BR-NEW-OPS", "PageCursor" in names, f"{oid} is a list with no paging")
    if "listBookableOutlets" in ops:
        need("BR-NEW-OPS", {} in (ops["listBookableOutlets"][3].get("security") or []),
             "listBookableOutlets is not readable before sign-in")
    if "addIncidentPerson" in ops:
        need("BR-NEW-OPS", "consent" in text(ops["addIncidentPerson"][3]).lower(),
             "addIncidentPerson does not apply the consent rules")

    errors["BR-PARSE"].extend(PARSE_ERRORS)
    total = sum(len(v) for v in errors.values())
    rules = ["BR-PARSE", "BR-STREAM", "BR-PAIR-REFUSAL", "BR-SPLIT", "BR-VISIT-PLAN", "BR-PO", "BR-PAY-LINK", "BR-REPORT-RUNS",
             "BR-CONTRAST", "BR-WO-CANCEL", "BR-INCIDENT", "BR-FARE", "BR-SESSIONS-DOOR", "BR-ATTENDANCE",
             "BR-AI-CURRENCY", "BR-QR", "BR-NEW-OPS"]
    for r in rules:
        print(f"  {r:18} {len(errors.get(r, [])):3d}")
        for m in errors.get(r, [])[:12]:
            print(f"      {m}")
    print(f"  {len(PAIR_EXEMPT)} create/update pair(s) exempt with a reason")
    print(f"\n{'FAIL' if total else 'PASS'} - {total} finding(s) against the 3 October business rules")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
