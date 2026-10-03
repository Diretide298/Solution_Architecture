#!/usr/bin/env python3
"""Every write operation writes a table or says why not, and every event emitter writes the outbox (CHG-R1S-005).

**Found by the HLD/LLD cross-check of 3 October** (`handoff-out/r1/HLD-LLD/CROSSCHECK.md`, the PKG rows under
`lineage`): `createOrder` emits `order.created` and `publishTenantConfig` emits `whitelabel.contentPublished`, yet
neither listed `platform.outbox` in its writes, though an event is written to the outbox in the same transaction;
and `exportSitePackage`, `sendGuestConversationMessage`, `rejectShiftVariance`, `enterWaitingRoom`,
`validateVenueMapGraph` and `resolveSyncRejection` were POSTs that wrote no table. Scripted across the package:
10 emitters without the outbox and 163 write operations writing no table.

**The cause.** `derive-lineage.py` derives `writes` from the schema a request body accepts. A state change whose
body is a reason or a step-up (`rejectShiftVariance`), or whose shape is the response's (`exportSitePackage`), got
none; and nothing added the outbox for an operation that emits. The generator now adds `platform.outbox` for every
emitter (a rule, so a new emitter gets it), and this one-off gives the existing entries their tables:

* **writes**: the table the operation changes, read off its response schema's persistence or named below;
* **pure**: an operation that computes and returns (a simulation, a quote, a validation, a print, a lookup) says so
  with its reason, so a developer knows writing nothing is the design;
* **storageUndecided**: the generated workspace writes whose fields no table covers (the request says "no new table
  has been decided"): an explicit exemption with its reason, a question for the lead, never a silent gap.

`tools/check-write-lineage.py` holds all three from now on.

    python tools/applied/lineage-writes-3-october.py [--apply]
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIN = os.path.join(ROOT, "handoff", "api-data-lineage.json")
CHG = "CHG-R1S-005"

SIM = "a simulation: computes what would happen and stores nothing"
EXPLAIN = "an explanation: computes and returns, stores nothing"
VALIDATE = "a validation: reports what it finds, stores nothing"
PRINT = "renders a document from data already stored; nothing is written"
LOOKUP = "a lookup: resolves and returns, nothing is created or merged"
QUOTE = "a quote: priced on request and returned, not stored"

PURE = {
    "compareForecastScenarios": "compares stored scenarios; nothing is written",
    "simulateRecommendationDecision": SIM, "simulateGameplayAuthorisation": SIM, "simulatePaymentRouting": SIM,
    "simulatePaymentConfiguration": SIM, "simulatePromotion": SIM, "simulateRentalPricing": SIM,
    "simulateCreditConsumption": SIM, "simulateCommercialPackage": SIM, "simulateGuestJourney": SIM,
    "simulateRefund": SIM, "simulateOfflineResilienceTesting": SIM, "simulatePolicyConflictImpact": SIM,
    "simulatePriceBreakdownCalculation": SIM, "simulateBundlePreviewRecommendation": SIM,
    "explainRecommendation": EXPLAIN, "explainRentalPrice": EXPLAIN,
    "validateGameConfiguration": VALIDATE, "validateRentalProduct": VALIDATE, "validateTenantConfig": VALIDATE,
    "validateVenueMapGraph": VALIDATE + " (reachability over the map's points and paths)",
    "validateRecognitionSchedules": VALIDATE, "testPricingRule": "a dry run: the request says it stores nothing",
    "testReader": "sends a test to the reader and returns its answer; the reader's own heartbeat records health",
    "printOrderLabel": PRINT, "printPrepSheet": PRINT, "printTicketProof": PRINT,
    "checkGuestCheckoutMatch": LOOKUP, "matchGuest": LOOKUP, "identifyGuest": LOOKUP,
    "resolvePermissions": "computes effective permissions; nothing is granted",
    "evaluateApprovalRequirement": "says whether approval is needed and from whom; no request is raised",
    "checkBookingEligibility": "computed per request; nothing is held",
    "calculateTax": "computes tax for the lines sent; the order's own write stores it",
    "getRecommendations": "computed suggestions; the decision record is written by the AI engine, not here",
    "getUpsellSuggestions": "computed suggestions; nothing is stored",
    "recommendSeats": "computed; seats are held only by createSeatHold",
    "quoteTransportFare": QUOTE, "quoteUpgrade": QUOTE,
    "runSemanticQuery": "runs a query on the analytical replica and returns the result",
    "previewSubscriptionChange": "a preview of a plan change; setSubscription makes it",
    "buildDeepLink": "builds and signs a URL; nothing is stored",
    "exportPartnerInvoice": "renders the settlement in an ERP format from stored data",
    "exportSubjectData": "assembles the subject's data for download; the request is audited by the platform's "
                         "audit trail, not a table of this operation",
    "issueApiToken": "a signed, short-lived token; nothing is stored per issue",
    "startProspectSignup": "the one-time challenge is held in Identity's challenge store (Redis), not a table",
    "verifyProspectSignupCode": "returns a prospect session token held in Redis, not a table",
    "enterWaitingRoom": "a transient place held in the waiting room's Redis counters, never a table (ADR-0066)",
}

UNDECIDED = {
    "setRuleTestRecommendation": "generated workspace write: no table covers its fields and none has been decided",
    "approveCampaignWorkflow": "generated workspace write: no table covers its fields and none has been decided",
    "approveDecision": "generated workspace write: no table covers its fields and none has been decided",
    "setMemberMembershipAccount": "generated workspace write: no table covers its fields and none has been decided",
    "setVirtualTicketCredential": "generated workspace write: no table covers its fields and none has been decided",
    "setOrderDetailTransaction": "generated workspace write on a Block A screen: no table covers its fields and none "
                                 "has been decided (a question for the lead, R1S report)",
    "setAfterSaleFinancial": "generated workspace write on a Block A screen: no table covers its fields and none has "
                             "been decided (a question for the lead, R1S report)",
}

# where the response schema does not say it, or says more than the operation changes
WRITES = {
    "quoteWaitTime": ["fnb.waitlist_entry"],
    "enterCountLine": ["inventory.count_line"],
    "requestRecount": ["inventory.count_line"],
    "setDailyCount": ["inventory.item"],
    "setKitchenSla": ["fnb.kitchen_sla"],
    "sendGuestConversationMessage": ["marketing.conversation_message"],
    "createCaseClassificationIntelligent": ["marketing.case"],
    "setBiometricLifecycleRetention": ["tenancy.data_retention_setting"],
    "setTransportRouteStatus": ["transport.route"],
    "withdrawTransportTimetable": ["transport.timetable"],
    "unpublishGuidedChoice": ["whitelabel.guided_choice"],
    "rejectShiftVariance": ["orders.pos_shift", "orders.pos_shift_incident"],
    "approveShiftClose": ["orders.pos_shift", "orders.pos_shift_approval"],
    "importTicketTemplate": ["orders.ticket_template", "orders.ticket_template_channel"],
    "cloneTicketTemplate": ["orders.ticket_template", "orders.ticket_template_channel"],
    "relinquishChannelAllocation": ["catalogue.channel_allocation"],
    "bulkUpdateCatalogueProducts": ["catalogue.product"],
    "endOwnSession": ["identity.session"],
    "openGuestCreditAccount": ["orders.guest_credit_account"],
    "quoteRentalPrice": ["rental.quote"],
    "recordConsentAnswers": ["marketing.booking_consent_record"],
    "matchGuest": None,  # pure, above
}

STORE_WORDS = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")


def load_contracts():
    schemas, ops = {}, {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        d = yaml.load(io.open(f, encoding="utf-8"), Loader=yaml.CSafeLoader) or {}
        for n, s in ((d.get("components") or {}).get("schemas") or {}).items():
            schemas.setdefault(n, s)
        for p, item in (d.get("paths") or {}).items():
            for v, op in (item or {}).items():
                if isinstance(op, dict) and op.get("operationId"):
                    ops[op["operationId"]] = (v, op)
    return schemas, ops


def emitters(ops) -> dict:
    out = {}
    for f in glob.glob(os.path.join(ROOT, "events", "*.yaml")):
        if f.endswith("_schema.yaml"):
            continue
        e = yaml.load(io.open(f, encoding="utf-8"), Loader=yaml.CSafeLoader) or {}
        for o in e.get("emittedBy") or []:
            out.setdefault(str(o).split(".")[-1], set()).add(e.get("name"))
    for oid, (_, op) in ops.items():
        for e in op.get("x-ticvai-emits") or []:
            out.setdefault(oid, set()).add(e)
    return out


def response_tables(schemas, op) -> list:
    for c in ("200", "201", "202"):
        r = (op.get("responses") or {}).get(c)
        if not r:
            continue
        sch = (((r.get("content") or {}).get("application/json") or {}).get("schema")) or {}
        ref = sch.get("$ref") or ((sch.get("items") or {}).get("$ref") if isinstance(sch, dict) else None)
        if not ref:
            for sub in sch.get("allOf") or []:
                it = ((sub.get("properties") or {}).get("items") or {}).get("items") or {}
                ref = ref or it.get("$ref")
        if ref:
            p = str((schemas.get(ref.split("/")[-1]) or {}).get("x-ticvai-persistence") or "").strip("\"'")
            if p and not p.lower().startswith("none"):
                return [t.strip() for t in re.split(r"\s*\+\s*", p) if STORE_WORDS.match(t.strip())]
        return []
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    raw = io.open(LIN, encoding="utf-8").read()
    lin = json.loads(raw)
    schemas, ops = load_contracts()
    em = emitters(ops)
    outbox, wrote, pure, undecided, left = [], [], [], [], []
    for oid in sorted(em):
        e = lin.get(oid)
        if e is not None and e.get("contract") == "ai":
            continue  # AI writes only AI stores (ADR-0020); its publish path is a question (check-write-lineage)
        if e is not None and "platform.outbox" not in e.get("writes", []):
            e["writes"] = sorted(set(e.get("writes", [])) | {"platform.outbox"})
            outbox.append(oid)
    for oid, (verb, op) in sorted(ops.items()):
        e = lin.get(oid)
        if e is None or verb == "get":
            continue
        real = [w for w in e.get("writes", []) if ":" not in w]
        if real:
            continue
        if oid in PURE:
            if e.get("pure") != PURE[oid]:
                e["pure"] = PURE[oid]
                pure.append(oid)
            continue
        if oid in UNDECIDED:
            if e.get("storageUndecided") != UNDECIDED[oid]:
                e["storageUndecided"] = UNDECIDED[oid]
                undecided.append(oid)
            continue
        tabs = WRITES.get(oid) or response_tables(schemas, op)
        if not tabs:
            left.append(oid)
            continue
        e["writes"] = sorted(set(e.get("writes", [])) | set(tabs))
        e.setdefault("writesNote", f"writes added 3 October 2026 ({CHG}): the HLD/LLD cross-check found it wrote no table")
        wrote.append((oid, tabs))
    print(f"outbox added to {len(outbox)} emitter(s): {', '.join(outbox)}")
    print(f"writes given to {len(wrote)} operation(s)")
    for oid, t in wrote:
        print(f"   {oid}: {', '.join(t)}")
    print(f"marked pure: {len(pure)}; storage undecided: {len(undecided)}; left without an answer: {len(left)} {left}")
    if a.apply:
        ensure = not any(ord(ch) > 127 for ch in raw[:20000]) and "\\u" in raw
        out = json.dumps(lin, indent=1, ensure_ascii=False)
        io.open(LIN, "w", encoding="utf-8", newline="\n").write(out + ("\n" if raw.endswith("\n") else ""))
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main())
