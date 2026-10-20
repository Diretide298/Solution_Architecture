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

  BR-APPROVAL-ROUTE  (r8, CHG-R8SPN-016, CHG-R8GEN-013) setApprovalMatrix and approveMatrixMultiLevel refuse a
                   condition the engine cannot evaluate (422 condition-not-supported); submitApprovalRequest's 409
                   lists approval-no-longer-required and approval-no-approver-available.
  BR-GUEST-SELF-403  (r8, CHG-R8SPN-018) a guest operation scoped to the caller's subject answers another subject's
                   record 404, not 403: a ratchet (GUEST_SELF_403_CEILING). BR-ALERT-RECIPIENT (CHG-R8SPN-020) is a
                   warning until reporting's listAlerts states its recipient filter.

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

And one rule per decision for the CRs of 18 October 2026 (class 9, "rules nobody has decided yet"; CHG-CRA-007):

  BR-GUEST-PII     (ADAM CR-141) every GuestProfile property is marked personal or behavioural
                   (`x-ticvai-data-class`), the six personal fields among them; `searchGuests` states the consent rule,
                   the id order without GUEST_VIEW_PII and leaves out lifetimeValue until it has a currency.
  BR-HOST-ROUTING  (CR-162) `resolveTenantHost` states 308, terminated is 404, which databases are opened, a
                   platform subdomain verified at provisioning, and `database_name` informational.
  BR-CASH-RECEIPT  (CR-168) a `payment` journal source, a region's account mapping by scope path, entry numbers unique
                   per legal entity, the next open period, and createPayment's two settings reads.
  BR-HOLD-LAPSE    (CR-169) a seat reservation names its hold and can be `sold`; `convertInventoryHold` moves the
                   envelope's units and states the lapsed-hold rule (unitsGone, nothing refunded automatically).
  BR-LOGIN-ATTEMPTS (CR-170, 19 October 2026; CHG-CRA-009) every wrong-credentials 401 of login carries
                   attemptsRemaining, counted per submitted username known or not and per sign-in method, and
                   sso-sign-in-required does not; verifyMfaChallenge carries it on its wrong-code 422 and not on its
                   401, a missing or expired challenge session (narrowed, 20 October 2026, CHG-R8DEC-001); login's 409
                   says since when and on what.
  BR-GATE-CANCEL   (CR-171, 19 October 2026; CHG-CRA-010) a cancelled gate mode change records who, when and why in
                   its own columns, leaving the scheduler's untouched.
  BR-APPROVED-OUTCOME (20 October 2026, option A; CHG-R8DEC-002) an approved action's outcome has a writer:
                   approvals' recordApprovedActionOutcome, service-only, takes applied, notApplied or noOp and returns
                   the execution; the lineage has it write approvals.approved_action_execution; suspendTenant's and
                   reactivateTenant's grant consumers call it.

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


# BR-GUEST-SELF-403: guest operations scoped to the caller's subject that declared 403 on 20 October 2026 (13 on the
# generators branch before the core lane's CHG-R8SPN-018 merged). Lower it as they are fixed; never raise it.
GUEST_SELF_403_CEILING = 13


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

    # ============================================== the rules decided for the CRs of 18 October 2026 (CHG-CRA-007)
    # Class 9 of the 18 October triage, "rules nobody has decided yet": each operation depended on a rule the package
    # never stated, so a developer could not build it. The lead decided each; the contract now states it, with any
    # proposed default marked for the client to correct. One rule per decision, as above.

    # -------------------------------------------------------------- BR-GUEST-PII (ADAM CR-141)
    f, _, _, sg, doc = op("searchGuests")
    gp = ((doc.get("components") or {}).get("schemas") or {}).get("GuestProfile") or {}
    personal = {"displayName", "email", "phone", "preferredLanguage", "preferredChannel", "guestLinkId"}
    for p, ps in (gp.get("properties") or {}).items():
        cls = (ps or {}).get("x-ticvai-data-class")
        need("BR-GUEST-PII", cls in ("personal", "behavioural"),
             f"GuestProfile.{p} is not marked personal or behavioural (x-ticvai-data-class)")
        if p in personal:
            need("BR-GUEST-PII", cls == "personal", f"GuestProfile.{p} is personal data (CR-141) and not marked so")
    st = text(sg)
    need("BR-GUEST-PII", "superseded_at" in st and "granted" in st,
         "searchGuests does not state hasConsentFor's rule (the current consent record, decision granted)")
    need("BR-GUEST-PII", "ordered by `id`" in st or "ordered by id" in st,
         "searchGuests does not order by id for a caller without GUEST_VIEW_PII")
    need("BR-GUEST-PII", "lifetimeValue" in st and "currency" in st,
         "searchGuests does not say lifetimeValue is left out until it has a currency (CR-094's rule)")

    # -------------------------------------------------------------- BR-HOST-ROUTING (ADAM CR-162)
    rt = text(op("resolveTenantHost")[3])
    for frag, why in (("308", "the redirect status"), ("terminated", "a terminated tenant answers 404"),
                      ("draining", "which cell_tenant databases are opened"),
                      ("verifiedAt", "a platform subdomain is written verified at provisioning"),
                      ("informational", "tenant_domain.database_name is informational")):
        need("BR-HOST-ROUTING", frag in rt, f"resolveTenantHost does not state {why} ({frag!r})")

    # -------------------------------------------------------------- BR-CASH-RECEIPT (ADAM CR-168)
    fin = load("contracts/spine/finance.yaml")
    fs = (fin.get("components") or {}).get("schemas") or {}
    need("BR-CASH-RECEIPT", "payment" in ((fs.get("JournalSource") or {}).get("enum") or []),
         "JournalSource has no `payment`: a cash receipt would read as revenue")
    need("BR-CASH-RECEIPT", "scopePath" in ((fs.get("AccountMapping") or {}).get("properties") or {}),
         "AccountMapping has no scopePath: a region's mapping cannot be found")
    je = fs.get("JournalEntry") or {}
    need("BR-CASH-RECEIPT", ["legalEntityId", "entryNumber"] in (je.get("x-ticvai-unique-together") or [])
         and not (((je.get("properties") or {}).get("entryNumber") or {}).get("x-ticvai-unique")),
         "JournalEntry.entryNumber is not unique per legal entity (x-ticvai-unique-together legalEntityId, entryNumber)")
    cp = op("createPayment")[3]
    need("BR-CASH-RECEIPT", "next open period" in text(cp),
         "createPayment does not post a capture to the legal entity's next open period")
    vias = {str(v.get("query")) for v in cp.get("x-ticvai-read-via") or [] if isinstance(v, dict)}
    need("BR-CASH-RECEIPT", {"tenancy#venueSettingsRecords", "tenancy#regionSettingsRecords"} <= vias,
         "createPayment does not declare its reads of venue and region settings")

    # -------------------------------------------------------------- BR-HOLD-LAPSE (ADAM CR-169)
    seat = load("contracts/satellite/seating.yaml")
    sh = ((seat.get("components") or {}).get("schemas") or {}).get("SeatHold") or {}
    shp = sh.get("properties") or {}
    need("BR-HOLD-LAPSE", "sold" in ((shp.get("status") or {}).get("enum") or []),
         "SeatHold.status has no `sold`")
    need("BR-HOLD-LAPSE", "inventoryReservationId" in shp, "SeatHold names no inventory reservation")
    ct = text(op("convertInventoryHold")[3])
    need("BR-HOLD-LAPSE", "unitsGone" in ct and "refunded automatically" in ct,
         "convertInventoryHold does not state the lapsed-hold rule (units retaken, else unitsGone; no automatic refund)")
    need("BR-HOLD-LAPSE", "channel_envelope" in ct, "convertInventoryHold does not move the envelope's leased units")

    # -------------------------------------------------------------- BR-LOGIN-ATTEMPTS (ADAM CR-170; CHG-CRA-009)
    # Decided by Chinmay Parab on 19 October 2026, option D: the door says how many attempts are left on every 401,
    # counted per submitted username so nothing reveals which usernames exist; the 409 says since when and on what.
    idoc = load("contracts/spine/identity.yaml")
    ids = (idoc.get("components") or {}).get("schemas") or {}

    def ext(name, field):
        sch = ids.get(name) or {}
        return any(field in ((part or {}).get("properties") or {}) for part in sch.get("allOf") or [])

    lg = op("login")[3]
    r401 = text((lg.get("responses") or {}).get("401") or {})
    need("BR-LOGIN-ATTEMPTS", "LoginDeniedProblem" in r401 and ext("LoginDeniedProblem", "attemptsRemaining"),
         "login's 401 does not carry attemptsRemaining (LoginDeniedProblem)")
    need("BR-LOGIN-ATTEMPTS", "whether or not a principal has it" in r401,
         "login's 401 does not count attempts per submitted username, known or not")
    # Fix round 3 (lane-H review 2 M-5): "every 401" is every 401 login and verifyMfaChallenge return, and the
    # unknown username's counter is per sign-in method as a known one's lock is.
    # Narrowed by the lead on 20 October 2026 (CHG-R8DEC-001): every wrong-credentials 401, never sso-sign-in-required,
    # which checks no credential. LoginDeniedProblem serves both problem types, so the field is not `required` there and
    # the contract says where it is present and where it is not.
    ldp = text(ids.get("LoginDeniedProblem") or {})
    need("BR-LOGIN-ATTEMPTS", "`unauthenticated`" in ldp and "Not on `sso-sign-in-required`" in ldp,
         "LoginDeniedProblem does not say attemptsRemaining is on every unauthenticated 401 and not on "
         "sso-sign-in-required (CHG-R8DEC-001)")
    need("BR-LOGIN-ATTEMPTS", "does not carry `attemptsRemaining`" in r401 and "carries the count as it stands" not in r401,
         "login's 401 does not say sso-sign-in-required leaves attemptsRemaining out (CHG-R8DEC-001)")
    need("BR-LOGIN-ATTEMPTS", "per sign-in method" in r401,
         "login's 401 does not count attempts per sign-in method as well as per username")
    need("BR-LOGIN-ATTEMPTS", "SessionHeldProblem" in text((lg.get("responses") or {}).get("409") or {})
         and ext("SessionHeldProblem", "openedAt") and ext("SessionHeldProblem", "deviceLabel"),
         "login's 409 does not say since when and on what (SessionHeldProblem openedAt, deviceLabel)")
    need("BR-LOGIN-ATTEMPTS", "credential-locked" in text((lg.get("responses") or {}).get("429") or {}),
         "login's lock is not 429 credential-locked")
    vm = op("verifyMfaChallenge")[3]
    need("BR-LOGIN-ATTEMPTS", "MfaCodeInvalidProblem" in text((vm.get("responses") or {}).get("422") or {})
         and ext("MfaCodeInvalidProblem", "attemptsRemaining"),
         "verifyMfaChallenge's 422 does not carry attemptsRemaining")
    # Narrowed on 20 October 2026 (CHG-R8DEC-001): a missing or expired challenge session is not a wrong credential.
    vm401 = text((vm.get("responses") or {}).get("401") or {})
    need("BR-LOGIN-ATTEMPTS", "MfaCodeInvalidProblem" not in vm401 and "does not carry `attemptsRemaining`" in vm401,
         "verifyMfaChallenge's 401 carries attemptsRemaining or does not say it does not (a missing or expired challenge "
         "session is not a wrong credential, CHG-R8DEC-001)")

    # -------------------------------------------------------------- BR-GATE-CANCEL (ADAM CR-171; CHG-CRA-010)
    # Decided by Chinmay Parab on 19 October 2026, option B: a cancelled gate mode change records who, when and why
    # in its own columns, and the scheduler's changedBy, changedAt and reason are left untouched.
    adoc = load("contracts/spine/access.yaml")
    gm = (((adoc.get("components") or {}).get("schemas") or {}).get("AccessGateModeChange") or {}).get("properties") or {}
    for fld in ("cancelledByPrincipalId", "cancelledAt", "cancelReason"):
        need("BR-GATE-CANCEL", fld in gm, f"AccessGateModeChange has no {fld}")
    need("BR-GATE-CANCEL", (gm.get("cancelReason") or {}).get("maxLength") == 200,
         "AccessGateModeChange.cancelReason is not at most 200 characters")
    need("BR-GATE-CANCEL", "left as they were" in text(op("cancelGateModeChange")[3]),
         "cancelGateModeChange does not leave the scheduler's columns untouched")

    # -------------------------------------------------------------- BR-APPROVED-OUTCOME (CHG-R8DEC-002)
    # Decided by Chinmay Parab on 20 October 2026, option A: approvals.approved_action_execution was "updated by the
    # requesting contract as it executes" with no operation or event able to write it. One internal operation is that
    # writer, and the contracts that apply a grant say they call it.
    ro = op("recordApprovedActionOutcome")
    need("BR-APPROVED-OUTCOME", ro[0] is not None and ro[0].stem == "approvals",
         "approvals has no recordApprovedActionOutcome (the writer of an approved action's outcome)")
    if ro[0] is not None:
        o = ro[3]
        need("BR-APPROVED-OUTCOME", o.get("x-ticvai-audience") == ["service"] and o.get("x-ticvai-auth") == "service"
             and {"serviceAuth": []} in (o.get("security") or []),
             "recordApprovedActionOutcome is not service-only (audience service, x-ticvai-auth service, serviceAuth)")
        oc = props(ro[4], body_schema(o)).get("outcome") or {}
        need("BR-APPROVED-OUTCOME", set(oc.get("enum") or []) == {"applied", "notApplied", "noOp"},
             "recordApprovedActionOutcome's outcome is not applied, notApplied or noOp")
        need("BR-APPROVED-OUTCOME", "ApprovedActionExecutionView" in text((o.get("responses") or {}).get("200") or {}),
             "recordApprovedActionOutcome does not return the execution (ApprovedActionExecutionView)")
    lin_ = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    need("BR-APPROVED-OUTCOME", "approvals.approved_action_execution"
         in ((lin_.get("recordApprovedActionOutcome") or {}).get("writes") or []),
         "the lineage does not have recordApprovedActionOutcome write approvals.approved_action_execution")
    for oid in ("suspendTenant", "reactivateTenant"):
        need("BR-APPROVED-OUTCOME", "recordApprovedActionOutcome" in text(op(oid)[3]),
             f"{oid}'s grant consumer does not record its outcome through recordApprovedActionOutcome")

    # -------------------------------------------------------------- r8 second round (core lane's requests, CHG-R8GEN-013)
    # BR-APPROVAL-ROUTE (CHG-R8SPN-016): a matrix condition the engine cannot evaluate is refused when it is saved, and a
    # submission that no longer needs approval, or finds no approver, says so with its own problem type.
    for oid in ("setApprovalMatrix", "approveMatrixMultiLevel"):
        need("BR-APPROVAL-ROUTE", "condition-not-supported" in problem_types(op(oid)[3]),
             f"{oid} does not refuse a condition the engine cannot evaluate (422 condition-not-supported)")
    sub409 = text(((op("submitApprovalRequest")[3].get("responses") or {}).get("409")) or {})
    for pt in ("approval-no-longer-required", "approval-no-approver-available"):
        need("BR-APPROVAL-ROUTE", pt in sub409, f"submitApprovalRequest's 409 does not list {pt}")
    # BR-ALERT-RECIPIENT (CHG-R8SPN-020): reporting's listAlerts says whose alerts come back (the recipient role; an
    # over/short alert only to a holder of OVERSHORT_ACCEPT).
    la = next((o for oid, (f, _p, _m, o, _d) in ops.items() if oid == "listAlerts" and f.stem == "reporting"),
              op("listAlerts")[3])
    # Printed, not failed, until the surface lane's listAlerts text lands (r8 cause APPROVALS-TENANCY-C36): then move
    # it into `need` so the filter cannot be dropped again.
    if not ("OVERSHORT_ACCEPT" in text(la) and "recipient" in text(la).lower()):
        print("  WARN  BR-ALERT-RECIPIENT listAlerts does not yet state the recipient-role filter (OVERSHORT_ACCEPT for "
              "over/short alerts); surface lane, r8 cause APPROVALS-TENANCY-C36")
    # BR-GUEST-SELF-403 (CHG-R8SPN-018): a guest operation scoped to the caller's own subject answers someone else's
    # record with 404, never 403 (which would confirm it exists). A ratchet over the operations found on 20 October.
    self403 = sorted(oid for oid, (_f, _p, _m, o, _d) in ops.items()
                     if o.get("x-ticvai-self-scoped") == "subject" and "guest" in (o.get("x-ticvai-audience") or [])
                     and "403" in {str(k) for k in (o.get("responses") or {})})
    if len(self403) > GUEST_SELF_403_CEILING:
        need("BR-GUEST-SELF-403", False, f"{len(self403)} guest self-scoped operations declare 403, above the ceiling "
             f"of {GUEST_SELF_403_CEILING}: answer another subject's record 404 ({', '.join(self403[:8])})")

    errors["BR-PARSE"].extend(PARSE_ERRORS)
    total = sum(len(v) for v in errors.values())
    rules = ["BR-PARSE", "BR-STREAM", "BR-PAIR-REFUSAL", "BR-SPLIT", "BR-VISIT-PLAN", "BR-PO", "BR-PAY-LINK", "BR-REPORT-RUNS",
             "BR-CONTRAST", "BR-WO-CANCEL", "BR-INCIDENT", "BR-FARE", "BR-SESSIONS-DOOR", "BR-ATTENDANCE",
             "BR-AI-CURRENCY", "BR-QR", "BR-NEW-OPS", "BR-GUEST-PII", "BR-HOST-ROUTING", "BR-CASH-RECEIPT",
             "BR-HOLD-LAPSE", "BR-LOGIN-ATTEMPTS", "BR-GATE-CANCEL", "BR-APPROVAL-ROUTE", "BR-GUEST-SELF-403",
             "BR-APPROVED-OUTCOME"]
    for r in rules:
        print(f"  {r:18} {len(errors.get(r, [])):3d}")
        for m in errors.get(r, [])[:12]:
            print(f"      {m}")
    print(f"  {len(PAIR_EXEMPT)} create/update pair(s) exempt with a reason")
    print(f"\n{'FAIL' if total else 'PASS'} - {total} finding(s) against the 3 October business rules")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
