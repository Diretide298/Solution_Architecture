#!/usr/bin/env python3
"""Hold the finance decisions of 2 October 2026 (Chinmay) in the package, so they cannot quietly come back.

Change log CHG-FIN-001 to CHG-FIN-011 (changes/entries/CHG-FIN-*.yaml). Each rule below is one decision
that the package used to contradict; each fails on the state before the decision and passes after it.

  F-REVENUE-LABEL  (CHG-FIN-002) No screen component is labelled with a bare "Revenue": "Revenue",
                   "Total revenue", "Gross revenue", "Revenue today", "Revenue by ...", "Revenue vs ...".
                   Takings, Gross sales, Net revenue, Recognised revenue and Deferred revenue are
                   different measures and a label names one of them.
  F-BLIND-CLOSE    (CHG-FIN-003) A cashier's screen (P04 till, P06 staff app) calls `closeShift` only from
                   a supervisor's control (SHIFT_CLOSE_OTHER or OVERSHORT_ACCEPT; CHG-SPO-021) (it returns
                   the expected cash; the cashier counts through `submitShiftCount`) and
                   never shows `Shift.expectedCash`, `Shift.variance` or `ShiftCloseResult.*` unless
                   the component is permissioned OVERSHORT_ACCEPT (the supervisor).
  F-TAX-BASE       (CHG-FIN-004) `CalculateTaxRequest.discountsAreTaxInclusive` stays deprecated: the
                   taxable base has one source, `TaxProfile.taxBase`.
  F-FIN-KPIS       (CHG-FIN-007, CHG-FIN-010) The finance measures stay seeded (`ReportingSystemKpi`) and
                   watchable (`MetricSource`), and `ReportColumn` keeps the encodings the nine marks bind on.
  F-CHARGE-CCY     (CHG-FIN-001) The guest-selected currency stays modelled end to end: the venue setting,
                   the checkout field, the order's locked rate and the refund's currency.
  F-LEDGER         (CHG-FIN-005, CHG-FIN-008) No PUT, PATCH or DELETE on a journal entry (posted entries are
                   only reversed), and `approveJournalEntry` still refuses an approver who is the preparer.
  F-RECON-DAILY    (CHG-FIN-009) `ingestSettlementFile` still refuses a settlement period that is not one day.
  F-TAX-DOCS       (CHG-FIN-011) The tax invoice and the tax credit note keep the fields UAE law requires
                   (amounts in AED with the rate; the credit note's before, after and parties).
  F-VARIANCE-REASON (CHG-R4-019, the client's policy of 6 October 2026, T10.1) A difference within the shift
                   variance threshold closes only with a reason: an operation takes pendingClosure to closed
                   with a required `reason`, the receipt and close result carry `varianceReasonRequired`, and
                   every cashier screen that submits the blind count can give the reason.

    python3 tools/check-finance-rules.py
"""
from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]

BARE_REVENUE = re.compile(
    r"^(total |gross |today'?s |daily )?revenue( today| this hour| vs\b.*| by\b.*)?$", re.I)
CASHIER_PLATFORMS = ("P04", "P06")
HIDDEN_FROM_CASHIER = ("Shift.expectedCash", "Shift.variance", "ShiftCloseResult.")


def load(p):
    return yaml.safe_load(open(ROOT / p, encoding="utf-8"))


SUPERVISOR_CLOSE = {"SHIFT_CLOSE_OTHER", "OVERSHORT_ACCEPT"}


def components(screen):
    for region in (screen.get("layout") or {}).get("regions") or []:
        for c in region.get("components") or []:
            yield c


def variance_reason_rule() -> list[str]:
    """F-VARIANCE-REASON (CHG-R4-019): the client's policy of 6 October 2026 (T10.1,
    sources/client/2026-10-06-tracker-answers.md): a difference within the threshold closes only with a reason.
    states/shift.yaml must have an operation (not a job) taking a shift from pendingClosure to closed whose body
    requires `reason`; the cashier's receipt and the supervisor's close result must say when a reason is needed
    (`varianceReasonRequired`); and every cashier screen (P04, P06) that submits the blind count must also call
    that operation, or the till has no way to give the reason."""
    errs: list[str] = []
    sdoc = load("contracts/spine/shift.yaml")
    schemas = sdoc["components"]["schemas"]
    ops = {op.get("operationId"): op for item in sdoc["paths"].values() for op in item.values()
           if isinstance(op, dict) and op.get("operationId")}

    def body_required(op):
        sch = (((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {}).get("schema") or {}
        ref = sch.get("$ref", "")
        if ref.startswith("#/components/schemas/"):
            sch = schemas.get(ref.rsplit("/", 1)[1], {})
        return set(sch.get("required") or [])

    states = load("states/shift.yaml")
    reason_ops = [t["operation"] for t in states.get("transitions") or []
                  if t.get("from") == "pendingClosure" and t.get("to") == "closed" and t.get("trigger") == "operation"
                  and t.get("operation") in ops and "reason" in body_required(ops[t["operation"]])]
    if not reason_ops:
        errs.append("F-VARIANCE-REASON states/shift.yaml has no operation taking a shift from pendingClosure to "
                    "closed with a required reason: a difference within the threshold closes with no reason "
                    "(the client's T10.1; CHG-R4-019)")
    for name in ("ShiftCountReceipt", "ShiftCloseResult"):
        if "varianceReasonRequired" not in (schemas.get(name, {}).get("properties") or {}):
            errs.append(f"F-VARIANCE-REASON {name}.varianceReasonRequired is missing: the caller cannot tell the "
                        "shift waits for a reason (CHG-R4-019)")
    for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml"))):
        doc = yaml.safe_load(open(f, encoding="utf-8"))
        if doc["platform"]["code"] not in CASHIER_PLATFORMS:
            continue
        for s in doc["screens"]:
            apis = {a.get("operationId") for a in s.get("apis") or []}
            if "submitShiftCount" in apis and reason_ops and not apis & set(reason_ops):
                errs.append(f"F-VARIANCE-REASON {s['id']}: submits the blind count but never calls "
                            f"{' or '.join(reason_ops)}, so the cashier cannot give the reason (CHG-R4-019)")
    return errs


def main() -> int:
    errors: list[str] = []

    for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml"))):
        doc = yaml.safe_load(open(f, encoding="utf-8"))
        code = doc["platform"]["code"]
        for s in doc["screens"]:
            for c in components(s):
                label = (c.get("label") or "").strip()
                if label and BARE_REVENUE.match(label):
                    errors.append(f"F-REVENUE-LABEL {s['id']}: component labelled '{label}' "
                                  "(name the measure: Takings, Gross sales, Net revenue, ...; CHG-FIN-002)")
            if code in CASHIER_PLATFORMS:
                ops = [a.get("operationId") for a in s.get("apis") or []]
                if "closeShift" in ops:
                    # **The supervisor's close is allowed on the till** (decided 2 October 2026, Chinmay,
                    # pre-apply round: "closeShift is declared on POS-007 (supervisor PIN, any till)";
                    # CHG-CSP-012, CHG-SPO-021). It stays blind for the cashier: every control and form
                    # that calls closeShift must be a supervisor's (SUPERVISOR_CLOSE), never the cashier's.
                    callers = [c for c in components(s) if c.get("operation") == "closeShift"]
                    sup = {c.get("label") for c in callers if c.get("permission") in SUPERVISOR_CLOSE}
                    forms = [o for o in s.get("overlays") or []
                             if (o.get("confirm") or {}).get("operation") == "closeShift"]
                    if not callers or len(sup) != len(callers) or any(o.get("trigger") not in sup for o in forms):
                        errors.append(f"F-BLIND-CLOSE {s['id']}: a cashier screen declares closeShift, which "
                                      "returns the expected cash, outside a supervisor's control "
                                      f"({' or '.join(sorted(SUPERVISOR_CLOSE))}); the cashier uses "
                                      "submitShiftCount (CHG-FIN-003)")
                for c in components(s):
                    if c.get("permission") == "OVERSHORT_ACCEPT":
                        continue
                    shown = [c.get("bindsTo") or ""] + list(c.get("columns") or [])
                    leak = [x for x in shown if any(x.startswith(h) for h in HIDDEN_FROM_CASHIER)]
                    if leak:
                        errors.append(f"F-BLIND-CLOSE {s['id']}: '{c.get('label') or c.get('kind')}' shows "
                                      f"{', '.join(leak)} to the cashier (CHG-FIN-003)")

    fin = load("contracts/spine/finance.yaml")["components"]["schemas"]
    flag = fin["CalculateTaxRequest"]["properties"].get("discountsAreTaxInclusive")
    if flag is not None and not flag.get("deprecated"):
        errors.append("F-TAX-BASE CalculateTaxRequest.discountsAreTaxInclusive is not deprecated: the taxable "
                      "base has one source, TaxProfile.taxBase (CHG-FIN-004)")

    rep = load("contracts/satellite/reporting.yaml")["components"]["schemas"]
    finance = {"takings", "grossSales", "discounts", "refunds", "netRevenue", "recognisedRevenue",
               "deferredRevenue", "taxCollected"}
    for name in ("ReportingSystemKpi", "MetricSource"):
        missing = finance - set(rep[name]["enum"])
        if missing:
            errors.append(f"F-FIN-KPIS {name} lacks {', '.join(sorted(missing))} (CHG-FIN-007, CHG-FIN-010)")
    enc = {"role", "encoding", "axis", "seriesType", "hierarchyLevel", "unitLabel"}
    missing = enc - set(rep["ReportColumn"]["properties"])
    if missing:
        errors.append(f"F-FIN-KPIS ReportColumn lacks {', '.join(sorted(missing))}: the nine marks cannot "
                      "bind (CHG-FIN-007)")

    orders = load("contracts/spine/orders.yaml")["components"]["schemas"]
    tenancy = load("contracts/spine/tenancy.yaml")
    need = [
        ("Order", orders["Order"]["properties"], ("chargeCurrency", "chargeFxRate", "chargeTotal")),
        ("Refund", orders["Refund"]["properties"], ("tenderCurrency", "tenderAmount")),
    ]
    for name, props, fields in need:
        for fld in fields:
            if fld not in props:
                errors.append(f"F-CHARGE-CCY {name}.{fld} is missing (CHG-FIN-001)")
    if "chargeCurrencies:" not in (ROOT / "contracts/spine/tenancy.yaml").read_text(encoding="utf-8"):
        errors.append("F-CHARGE-CCY VenueSettings.chargeCurrencies is missing (CHG-FIN-001)")
    del tenancy

    fdoc = load("contracts/spine/finance.yaml")
    for path, item in fdoc["paths"].items():
        if path.startswith("/journal-entries"):
            for verb in ("put", "patch", "delete"):
                if verb in item:
                    errors.append(f"F-LEDGER {verb.upper()} {path}: a journal entry is never edited or deleted, "
                                  "only reversed (CHG-FIN-005)")
    ops = {op.get("operationId"): op for item in fdoc["paths"].values() for op in item.values()
           if isinstance(op, dict) and op.get("operationId")}
    text = yaml.safe_dump(ops.get("approveJournalEntry", {}))
    if "approver-is-preparer" not in text:
        errors.append("F-LEDGER approveJournalEntry no longer refuses approver-is-preparer (CHG-FIN-005, CHG-FIN-008)")
    if "settlement-period-not-a-day" not in yaml.safe_dump(ops.get("ingestSettlementFile", {})):
        errors.append("F-RECON-DAILY ingestSettlementFile no longer refuses a period that is not one day (CHG-FIN-009)")
    tax_need = {"FinTaxInvoice": ("taxAmountInLegalCurrency", "grossAmountInLegalCurrency", "legalFxRate", "legalCurrency"),
                "FinTaxInvoiceLine": ("grossAmountInLegalCurrency",),
                "FinCreditMemo": ("invoiceSupplyValue", "correctedSupplyValue", "supplierTaxRegistrationNumber",
                                  "buyerTaxRegistrationNumber", "taxAmountInLegalCurrency")}
    for name, fields in tax_need.items():
        for fld in fields:
            if fld not in fin[name]["properties"]:
                errors.append(f"F-TAX-DOCS {name}.{fld} is missing (Executive Regulation Art. 59-60; CHG-FIN-011)")

    errors += variance_reason_rule()

    for e in errors:
        print("  FAIL", e)
    if errors:
        print(f"FAIL - {len(errors)} finance rule breach(es)")
        return 1
    print("PASS - the finance decisions of 2 October hold (revenue labels, blind close, tax base, finance KPIs, "
          "guest-selected currency, ledger reversal and approval, daily reconciliation, UAE tax documents)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
