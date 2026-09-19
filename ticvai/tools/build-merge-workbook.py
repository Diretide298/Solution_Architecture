#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The schema merge workbook, generated from the verdicts rather than typed.

**The first cut of this sheet said 26 decided when the review had settled 31.** The verdicts
lived in prose and the sheet was written by hand from memory of them, so the two drifted the
moment either moved. `handoff/merge-verdicts.json` is the source of truth and this builds the
workbook from it, which is why the count on the Summary sheet cannot disagree with the review
again.

Five sheets, in the order a reader wants them:

    Summary     the tallies, and the four criteria every call was made on
    Decisions   the eleven structural decisions, scored criterion by criterion
    Our actions what changes on OUR side, which is the half that makes the rest credible
    Tasks       one row per unmatched table, with the verdict and its reason
    Open        only the rows somebody still has to choose

`DECISIONS` and `ACTIONS` are written here rather than derived, because a decision is a
judgement about several tables at once and no per-row verdict can reconstruct it. Everything
else comes from the verdicts file.

    python3 tools/build-merge-workbook.py
"""
import collections
import io
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
OUT = os.path.join(H, "TICVAI_Schema_Merge_Tasks.xlsx")

GROUP = {
    "We take theirs": ["ADDITIVE", "TAKE THEIRS", "TAKE BODY", "MERGE", "EITHER", "TAKE EITHER"],
    "We keep ours": ["DECLINE", "KEEP OURS"],
    "Needs a choice": ["DECIDE", "COLLISION", "PLACEMENT", "SPLIT"],
    "Correction": ["NO MATCH", "RECLASSIFY"],
}
OF = {v: g for g, vs in GROUP.items() for v in vs}
ORDER = ["We take theirs", "We keep ours", "Needs a choice", "Correction"]

INK = "1F3864"
HEAD = PatternFill("solid", fgColor=INK)
SUB = PatternFill("solid", fgColor="D9E2F3")
BAND = {
    "We take theirs": PatternFill("solid", fgColor="E2EFDA"),
    "We keep ours": PatternFill("solid", fgColor="FCE4D6"),
    "Needs a choice": PatternFill("solid", fgColor="FFF2CC"),
    "Correction": PatternFill("solid", fgColor="EDEDED"),
}
THIN = Border(bottom=Side(style="thin", color="BFBFBF"))
WRAP = Alignment(wrap_text=True, vertical="top")
TOP = Alignment(vertical="top")

CRITERIA = [
    ("Maintainability", "how many places a change has to be made, and how many ways to get it wrong"),
    ("Readability", "does the name tell a developer what the rows are, without the schema doc open"),
    ("Optimised access", "does the query a screen actually runs stay inside one schema, on narrow rows"),
    ("DB strain", "contention, row width, update churn, and what shares a hot table with what"),
]

# n, title, call, rows, maintainability, readability, access, strain, the deciding evidence
DECISIONS = [
    (1, "Rental domain", "Keep rental.*, take their agreement", 5,
     "ours", "ours", "ours", "ours",
     "catalogue.rental_rate puts rental pricing inside the hottest table set in the system - the "
     "flash-sale argument that gave F&B and Retail their own price tables. Their layout also "
     "splits rental across CatalogueService and VenueOpsService. But we hold agreement_rules and "
     "agreement_signature and NO agreement: the signature signs a version string, and "
     "rental.participant has no booking reference at all."),
    (2, "Payments domain", "Keep payments for config; fix our own split first", 5,
     "neither today", "ours", "ours", "ours",
     "payments and orders are both OrderService, so the rental argument does not apply. The real "
     "one is DB strain: orders is the highest-churn schema and payment config is read on every "
     "checkout and written monthly. We hold payments in two schemas ourselves - 6 tables in "
     "orders, 16 in payments - and orders.payment_routing duplicates payments.routing_rule."),
    (3, "Subscription domain", "Consolidate into subscription; decline platform", 2,
     "a third option", "against control", "against theirs", "tie",
     "control holds 51 tables and is a junk drawer. Their placement puts billing in "
     "TenancyService and licensing in PlatformService, so a plan lookup becomes a cross-service "
     "call. Ours is split three ways. Moving control.subscription and subscription_plan into the "
     "subscription schema is the only option that puts one domain in one schema in one service."),
    (4, "venue schema", "Their name, our table: platform.scope. Decline all five", 5,
     "ours", "theirs", "tie", "tie",
     "platform.org_unit is one self-referencing hierarchy - level, parent_id, path, child_count. "
     "Their five typed tables flatten it, so adding a level becomes a new table. But scope is the "
     "word 58 of our configuration profiles already address by. All five of their tables are "
     "levels of that hierarchy: ScopeLevel enumerates tenant, brand, region, venue, department, "
     "subDepartment, workstation, outlet and subject, and ADR-0011 makes it binding."),
    (5, "pricing schema", "Take all three; give the schema an owner", 3,
     "theirs", "theirs", "theirs", "theirs",
     "We hold three guardrail columns on rental.pricing_profile - dynamic_enabled and a max "
     "increase and decrease - and no engine under them, and nothing at all on tickets, F&B or "
     "retail. A second pricing behaviour is currently a schema change. The pricing schema has no "
     "service owner; assign it to CatalogueService."),
    (6, "Payroll and HR scope", "CLOSED on their own sources - decline payroll, take HR as a "
        "projection", 14,
     "ours", "-", "-", "-",
     "Answered without asking. Resource_Management_Configuration_Reference.pdf Board 3 p45, "
     "'Workforce Integration & Synchronization Center': connect TICVAI with EXTERNAL HR, "
     "workforce management, payroll, identity and employee systems; its Integration Sources list "
     "names HRMS, Payroll and Time & Attendance, and Board 10 monitors Payroll as an integration. "
     "The requirement matrix has ZERO rows mentioning payroll, payslip, salary, wage, HRMS or HR "
     "system across all five sheets. The nearest, 1.2.84, is labour COSTING by venue and "
     "department, and 1.2.37 says INTEGRATE approved leave requests. So: decline the seven "
     "payroll tables, take the seven HR tables as an externally mastered projection, and add the "
     "field-ownership and sync layer Board 3 requires that neither workbook has."),
    (7, "Where a customer lives", "Keep the three-way split", 4,
     "ours", "ours", "ours", "ours",
     "identity.principal carries 134 inbound foreign keys, the most connected table in the "
     "package. Their proposal adds every guest row to the table every authentication already "
     "reads. The split is also what lets a subject-access export and a deletion request walk one "
     "subtree rather than everything."),
    (8, "Loyalty rules", "Take their split - ours has three faults", 3,
     "theirs", "theirs", "theirs", "theirs",
     "marketing.loyalty_programme holds no rules - it is a header. The only rules table is "
     "marketing.loyalty_tier, which is misnamed (earning triggers and multipliers, not tiers) and "
     "is referenced by nothing: 0 operations, 0 screens, 0 foreign keys. The tier a guest is in "
     "is two denormalised strings on their balance row."),
    (9, "Membership hierarchy", "Take it", 2,
     "theirs", "theirs", "theirs", "theirs",
     "Benefits are columns on catalogue.entitlement_template - fast_track_tier, "
     "can_claim_shop_and_drop, included_value - so a new benefit is a schema change. Its 15 "
     "operations and 34 screens read 34 columns to get three. The array argument in its purest "
     "form."),
    (10, "Cross-cell guest link", "REVERSED - keep it in platform", 1,
     "ours", "theirs", "ours", "tie",
     "We had recommended moving platform.guest_link into sync. dsar_request.guest_link_id points "
     "at it and both are TenancyService; sync is CrossRegionService. Moving the link alone puts a "
     "DSAR fan-out across a service boundary on its hottest path. Either both go or neither does."),
    (11, "The DSAR duplicate", "Drop theirs", 1,
     "ours", "tie", "ours", "tie",
     "A subject-access request spans every service. Ours sits in TenancyService and walks "
     "guest_link; theirs would sit in MarketingService, which owns one of the dozen schemas a "
     "DSAR has to reach."),
]

# area, what we change, why, kind
ACTIONS = [
    ("Loyalty", "Take points_earning_rule, points_redemption_rule and loyalty_rule; retire or "
                "rename marketing.loyalty_tier; add a real tier table",
     "loyalty_programme is a header with no rules. loyalty_tier is misnamed and referenced by "
     "nothing - 0 ops, 0 screens, 0 FKs. Tiers are denormalised strings on the balance row.",
     "Defect"),
    ("Loyalty", "Take marketing.loyalty_points, the ledger",
     "loyalty_position is a balance with no transaction history behind it, so it cannot be "
     "audited or corrected.", "Defect"),
    ("Rental", "Take rental_agreement; merge rental_agreement_item with rental.equipment_assignment",
     "We hold agreement_rules and agreement_signature and no agreement. The signature references "
     "a participant and a version string, and rental.participant has no booking reference.",
     "Defect"),
    ("Payments", "Collapse orders.payment_routing into payments.routing_rule",
     "Both are priority plus conditions deciding a provider. Their single payment_route maps onto "
     "both of ours.", "Duplicate"),
    ("Rental", "Move rental.category out of rental",
     "It is the asset-category master for the whole venue - maintenance.asset, maintenance_plan, "
     "inspection_template, resources.resource_category and resource_requirement all point at it.",
     "Misplacement"),
    ("Payments", "Move orders.payment_provider, payment_token and payment_routing into payments",
     "We hold payments in two schemas - 6 tables in orders, 16 in payments. Config on the wrong "
     "side of our own boundary.", "Inconsistency"),
    ("Subscription", "Move control.subscription and control.subscription_plan into subscription",
     "Subscription lives in three places. control holds 51 tables and is a junk drawer.",
     "Inconsistency"),
    ("Platform", "Rename platform.org_unit to platform.scope",
     "Their name is better: scope is the word 58 of our configuration profiles already address "
     "by. org_unit appears nowhere else in our language.", "Take theirs"),
    ("Naming", "Publish a singular-or-plural rule and apply it to ourselves first",
     "sla_policy, admission_rules, region_settings, seating_rules. We have no rule, so we cannot "
     "argue theirs. access.entry_rule and seating.seat_rule are parked on it.", "Inconsistency"),
    ("Naming", "Take fnb.order, fnb.order_line and orders.discount",
     "fnb.fnb_order repeats its schema - the exact fault we ask them to fix in "
     "approvals.approval_matrix.", "Inconsistency"),
    ("Pricing", "Assign the pricing schema to CatalogueService",
     "It has no service owner. Leaving a schema unowned is how the last fifty unowned tables "
     "happened.", "Ownership"),
    ("Workforce", "Add a field-ownership and synchronisation layer for externally mastered staff "
                  "data",
     "Board 3 requires that for every field administrators determine which system is master, "
     "which is what prevents conflicting updates, and Board 10 specifies a six-state integration "
     "monitor. We hold no field-ownership record, no sync status and no conflict record - and "
     "neither does their workbook. Taking their employee tables without this takes the data and "
     "leaves the governance.", "Gap in both"),
    ("Arrays", "Review the 140 tables carrying an array column that encodes a relationship",
     "Their workbook normalised six and we took all six. "
     "access.admission_rules.allowed_access_point_ids is the proof - their entry_rule_point IS "
     "that array as a table. The other 134 are the same decision, unreviewed.", "Package-wide"),
    ("Tooling", "Fix the *_asset_id convention rule in derive-relationships.py",
     "Five of the twelve rental-to-maintenance edges are icons, images, a PDF and two signature "
     "scans matched to maintenance.asset. They belong to assets.media_asset.", "Defect"),
]


def load(name):
    return json.load(io.open(os.path.join(H, name), encoding="utf-8"))


def header(ws, cols, widths, row=1):
    for c, name in enumerate(cols, 1):
        cell = ws.cell(row=row, column=c, value=name)
        cell.fill = HEAD
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = widths[c - 1]
    ws.row_dimensions[row].height = 26


def sheet(wb, title, cols, rows, widths, band_col=None, wrap_from=0):
    ws = wb.create_sheet(title)
    header(ws, cols, widths)
    for r in rows:
        ws.append(r)
        i = ws.max_row
        fill = BAND.get(r[band_col]) if band_col is not None else None
        for c in range(1, len(cols) + 1):
            cell = ws.cell(row=i, column=c)
            cell.border = THIN
            cell.alignment = WRAP if c > wrap_from else TOP
            if fill:
                cell.fill = fill
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def main():
    verdicts = load("merge-verdicts.json")
    cls = load("mismatch-classification.json")

    rows = []
    for t in sorted(verdicts):
        v, why = verdicts[t]
        d = cls.get(t) or {}
        rows.append([t, OF.get(v, "?"), v, d.get("category", ""), d.get("purpose", ""), why])
    by_group = collections.Counter(r[1] for r in rows)

    wb = Workbook()
    wb.remove(wb.active)

    # ── Summary ──────────────────────────────────────────────────────────────
    ws = wb.create_sheet("Summary")
    ws["A1"] = "TICVAI schema merge — where their 223 unmatched tables landed"
    ws["A1"].font = Font(bold=True, size=14, color=INK)
    ws["A2"] = ("Their workbook holds 323 tables against our 556. 100 already share a name. "
                "These 223 are the rest.")
    ws["A2"].font = Font(size=10, italic=True, color="595959")
    ws.append([])

    ws.append(["Answer", "Tables", "What it means"])
    for c in (1, 2, 3):
        ws.cell(row=ws.max_row, column=c).fill = HEAD
        ws.cell(row=ws.max_row, column=c).font = Font(bold=True, color="FFFFFF")
    meaning = {
        "We take theirs": "their table, their name, or their columns",
        "We keep ours": "same table, we keep ours, with the reason stated per row",
        "Needs a choice": "payroll — a scope question, not a schema one",
        "Correction": "matches we had wrong; no choice involved",
    }
    for g in ORDER:
        ws.append([g, by_group.get(g, 0), meaning[g]])
        for c in (1, 2, 3):
            ws.cell(row=ws.max_row, column=c).fill = BAND[g]
            ws.cell(row=ws.max_row, column=c).border = THIN
    ws.append(["Total", sum(by_group.values()), ""])
    for c in (1, 2):
        ws.cell(row=ws.max_row, column=c).font = Font(bold=True)
    ws.append([])

    ws.append(["How every call was made"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True, size=12, color=INK)
    ws.append(["Not our schema against theirs. Where their shape is better we took it, where ours "
               "is better we kept it, and where each had half we combined. Nothing was decided on "
               "who authored it or on what a rename costs."])
    ws.cell(row=ws.max_row, column=1).font = Font(italic=True, color="595959")
    ws.append(["Criterion", "The question it asks"])
    for c in (1, 2):
        ws.cell(row=ws.max_row, column=c).fill = SUB
        ws.cell(row=ws.max_row, column=c).font = Font(bold=True)
    for name, q in CRITERIA:
        ws.append([name, q])
        ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
        ws.cell(row=ws.max_row, column=2).alignment = WRAP
    ws.append([])
    ws.append(["Re-scoring all 223 against these moved 38 rows, almost all of them in the backend "
               "team's favour."])
    ws.cell(row=ws.max_row, column=1).font = Font(italic=True, color="595959")

    ws.append([])
    ws.append(["Verdict", "Tables", "Answer"])
    for c in (1, 2, 3):
        ws.cell(row=ws.max_row, column=c).fill = HEAD
        ws.cell(row=ws.max_row, column=c).font = Font(bold=True, color="FFFFFF")
    for v, n in collections.Counter(r[2] for r in rows).most_common():
        ws.append([v, n, OF.get(v, "?")])
        ws.cell(row=ws.max_row, column=3).fill = BAND.get(OF.get(v, ""), SUB)
    for col, w in zip("ABC", (26, 10, 86)):
        ws.column_dimensions[col].width = w

    # ── Decisions ────────────────────────────────────────────────────────────
    cols = ["#", "Decision", "The call", "Rows", "Maintainability", "Readability",
            "Optimised access", "DB strain", "What decided it"]
    sheet(wb, "Decisions", cols,
          [list(d) for d in DECISIONS],
          [5, 24, 44, 7, 17, 15, 17, 13, 100], wrap_from=4)

    # ── Our actions ──────────────────────────────────────────────────────────
    sheet(wb, "Our actions", ["Area", "Kind", "What changes on our side", "Why"],
          [[a[0], a[3], a[1], a[2]] for a in ACTIONS],
          [16, 16, 62, 92], wrap_from=2)

    # ── Tasks and Open ───────────────────────────────────────────────────────
    cols = ["Their table", "Answer", "Verdict", "How it was classified",
            "Their stated purpose", "Our reason"]
    widths = [38, 16, 14, 22, 62, 78]
    sheet(wb, "Tasks", cols, rows, widths, band_col=1, wrap_from=3)
    sheet(wb, "Open", cols, [r for r in rows if r[1] == "Needs a choice"], widths,
          band_col=1, wrap_from=3)

    wb.save(OUT)
    print("  %d row(s), %d decision(s), %d action(s) -> handoff/%s"
          % (len(rows), len(DECISIONS), len(ACTIONS), os.path.basename(OUT)))
    for g in ORDER:
        print("    %-16s %3d" % (g, by_group.get(g, 0)))
    missing = sorted(set(cls) - set(verdicts))
    if missing:
        print("  %d table(s) classified with no verdict: %s" % (len(missing), missing[:6]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
