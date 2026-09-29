#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The four small leftovers the Specification sheet showed on 29 September, applied in one pass.

1. P11 Accreditation Web still called the approvals stubs (`listAccreditationBadges`,
   `listApprovalRequests`) instead of the accreditation operations that now exist. The applicant
   and reviewer screens are rebound to `accreditation.yaml`, and the contract's reference to
   `access.validateEntry` (an operation that does not exist) becomes `validateAccess`.
2. `getResourceQualifications` was the one resources operation on no screen. It joins BO-857,
   the resource profile, where a resource's certifications belong.
3. 19 tables were reached by no operation. Each is a child or join table whose parent's writer
   fills it; the lineage now says so. Two have no writer at all and are recorded as gaps below.
4. The two billing-statement reads had a staff audience and no permission. Staff reading a
   member's statement need `ORDER_VIEW`, the same as any other order read.

Text edits only, so authored formatting survives. Rerunnable: every edit checks before it acts.

    python3 tools/applied/leftovers-29-september.py
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROV = "readiness close-out, 29 September 2026"


def rw(path):
    s = io.open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    return s.replace("\r\n", "\n"), nl


def save(path, s, nl):
    io.open(path, "w", encoding="utf-8", newline="").write(s.replace("\n", nl))


def apis_block(entries):
    out = ["  apis:"]
    for op, contract, purpose, trigger in entries:
        out += [f"  - operationId: {op}", f"    contract: {contract}", f"    purpose: {purpose}" if ": " not in purpose else "    purpose: '" + purpose.replace("'", "''") + "'",
                f"    trigger: {trigger}", f"    provenance: {PROV}"]
    return "\n".join(out) + "\n"


def screen_span(s, sid):
    m = re.search(rf"^- id: {re.escape(sid)}\n", s, re.M)
    if not m:
        raise SystemExit(f"{sid} not found")
    n = re.search(r"^- id: ", s[m.end():], re.M)
    return m.start(), (m.end() + n.start()) if n else len(s)


def set_apis(s, sid, entries):
    a, b = screen_span(s, sid)
    blk = s[a:b]
    m = re.search(r"^  apis:.*\n(?:(?:  - |    ).*\n)*", blk, re.M)
    if not m:
        raise SystemExit(f"{sid}: no apis block")
    if set(re.findall(r"operationId: (\w+)", m.group(0))) == {e[0] for e in entries}:
        return s
    return s[:a] + blk[:m.start()] + apis_block(entries) + blk[m.end():] + s[b:]


def drop_gap(s, sid, op):
    a, b = screen_span(s, sid)
    blk = s[a:b]
    # A gap's `why` is a folded block with blank lines inside it; run to the next gap or key.
    m = re.search(rf"^  - operation: {op}\n(?:(?:    .*)?\n)*?(?=^  - |^  [a-z])", blk, re.M)
    return s if not m else s[:a] + blk[:m.start()] + blk[m.end():] + s[b:]


def main():
    # 1. P11 rebinding
    p = os.path.join(ROOT, "screens", "P11-accreditation-portal.yaml")
    s, nl = rw(p)
    A = "accreditation"
    s = set_apis(s, "ACC-002", [
        ("createAccreditationApplication", A, "Register the applicant, the organisation and the coverage requested", "onAction"),
        ("submitAccreditationDocument", A, "Each supporting document, against the requirement it satisfies", "onAction")])
    s = drop_gap(s, "ACC-002", "createAccreditationApplication")
    s = set_apis(s, "ACC-003", [
        ("createAccreditationApplication", A, "Submit the reviewed application", "onAction")])
    s = set_apis(s, "ACC-004", [
        ("listAccreditationApplications", A, "The applicant's own applications and where each one stands", "onLoad")])
    s = set_apis(s, "ACC-005", [
        ("listAccreditationCredentials", A, "The credentials issued against this application", "onLoad"),
        ("issueAccreditationCredential", A, "Issue the badge or mobile credential", "onAction")])
    s = set_apis(s, "ACC-006", [
        ("listAccreditationApplications", A, "Applications awaiting review, oldest first", "onLoad")])
    # Document verification waits for a read of an application's documents (BL-180): without one the
    # reviewer has no documentId to act on, and inventing an entry parameter would hide the gap.
    s = set_apis(s, "ACC-007", [
        ("listAccreditationApplications", A, "The application under review", "onLoad"),
        ("decideAccreditationApplication", A, "Approve, reject or return for information", "onAction")])
    s = set_apis(s, "ACC-008", [
        ("listAccreditationCredentials", A, "Every credential issued, with its validity", "onLoad")])
    a, b = screen_span(s, "ACC-007")
    blk = s[a:b].replace("    - name: requestId\n      from: ACC-006\n", "    - name: applicationId\n      from: ACC-006\n")
    if "operation: listAccreditationDocuments" not in blk:
        gap = ("  - operation: listAccreditationDocuments\n"
               "    why: 'The reviewer verifies each document, and nothing reads an application''s documents back,\n"
               "      so there is no documentId to act on. `verifyAccreditationDocument` joins this screen when the read\n"
               "      exists (BL-180).\n\n      '\n"
               "    source: re-trace of 29 September, contract-backlog BL-180\n")
        if re.search(r"^  gaps:\n", blk, re.M):
            blk = re.sub(r"^  gaps:\n", "  gaps:\n" + gap, blk, count=1, flags=re.M)
        else:
            blk = re.sub(r"^  layout:", "  gaps:\n" + gap + "  layout:", blk, count=1, flags=re.M)
    s = s[:a] + blk + s[b:]
    a, b = screen_span(s, "ACC-005")
    s = s[:a] + s[a:b].replace("operation: issueAccreditationBadge\n", "operation: issueAccreditationCredential\n") + s[b:]
    save(p, s, nl)
    print("P11 rebound to accreditation")

    p = os.path.join(ROOT, "contracts", "satellite", "accreditation.yaml")
    s, nl = rw(p)
    if "access.validateEntry" in s:
        save(p, s.replace("access.validateEntry", "access.validateAccess"), nl)
        print("accreditation: validateEntry -> validateAccess")

    # 2. getResourceQualifications on the resource profile
    p = os.path.join(ROOT, "screens", "P08-venue-back-office.yaml")
    s, nl = rw(p)
    if "operationId: getResourceQualifications" not in s:
        a, b = screen_span(s, "BO-857")
        blk = s[a:b]
        m = re.search(r"^  - operationId: getResource\n(?:    .*\n)*", blk, re.M)
        add = ("  - operationId: getResourceQualifications\n    contract: resources\n"
               "    purpose: What the resource is certified to do, and until when\n    trigger: onLoad\n"
               f"    provenance: {PROV}\n")
        s = s[:a] + blk[:m.end()] + add + blk[m.end():] + s[b:]
        save(p, s, nl)
        print("BO-857: getResourceQualifications bound")

    # 3. Lineage: child and join tables written by their parent's writer
    p = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    raw = io.open(p, encoding="utf-8", newline="").read()
    L = json.loads(raw)
    adds = {  # table: (writers, readers)
        "assets.media_collection_member": (["createCollection"], ["listCollections"]),
        "control.cell_instance": (["provisionCell"], ["getCell", "getCellHealth"]),
        "control.cell_tenant": (["provisionCell"], ["getCell", "getTenant"]),
        "control.migration_plan_cell": (["planMigration"], ["planMigration"]),
        "control.release_component": (["createRelease"], ["listReleases", "getReleaseReadiness"]),
        "fnb.delivery_location_outlet": ([], ["listDeliveryLocations", "recordOrderHandover"]),  # gap: no writer
        "fnb.menu_item_modifier": (["attachModifierGroup"], ["createGuestFnbOrder", "buildProductionPlan"]),
        "identity.authz_audit": (["evaluateAccess"], ["listAccessDecisions"]),
        "identity.refresh_token": (["login", "refreshToken", "logout"], ["refreshToken"]),
        "inventory.supplier_contract": (["updateSupplier"], ["listSuppliers", "getSupplierPerformance"]),  # gap: no contract op
        "maintenance.asset_status_change": (["setAssetStatus"], ["getAssetHistory"]),
        "marketing.campaign_target": (["createCampaign", "updateCampaign"], ["getCampaign"]),
        "marketing.review_response": (["respondToReview"], ["listReviews"]),
        "platform.sale_board_page": (["createSaleBoard", "updateSaleBoard"], ["listSaleBoards"]),
        "platform.sale_board_tile": (["createSaleBoard", "updateSaleBoard"], ["listSaleBoards"]),
        "rental.inspection_item": (["recordRentalInspection"], []),
        "reporting.natural_language_query": (["askReportingQuestion", "saveNaturalLanguageQuery"], []),
        "reporting.report_definition_version": (["createReport", "updateReport"], ["getReport"]),
        "seating.section_row": (["createSeatMap", "updateSeatMap", "importSeatMap"], ["allocateGroupSeats"]),
    }
    n = 0
    for t, (ws, rs) in adds.items():
        for op in ws:
            e = L.get(op)
            if e is not None and t not in (e.get("writes") or []):
                e.setdefault("writes", []).append(t); n += 1
        for op in rs:
            e = L.get(op)
            if e is not None and t not in (e.get("reads") or []):
                e.setdefault("reads", []).append(t); n += 1
    if n:
        out = json.dumps(L, indent=1, ensure_ascii=False)
        io.open(p, "w", encoding="utf-8", newline="").write(out + ("\n" if raw.endswith("\n") else ""))
    print(f"lineage: {n} table references added")

    # 4. ORDER_VIEW on the billing-statement reads
    p = os.path.join(ROOT, "contracts", "spine", "orders.yaml")
    s, nl = rw(p)
    lines = s.split("\n")
    n = 0
    for op in ("getBillingStatement", "listBillingStatements"):
        i = lines.index(f"      operationId: {op}")
        for j in range(i + 1, len(lines)):           # the operation's own keys, until the next operation
            if lines[j].startswith("      operationId:") or (lines[j].strip() and not lines[j].startswith("      ")):
                lines.insert(i + 1, "      x-ticvai-permission: ORDER_VIEW"); n += 1
                break
            if lines[j].startswith("      x-ticvai-permission:"):
                if lines[j].strip() != "x-ticvai-permission: ORDER_VIEW":
                    lines[j] = "      x-ticvai-permission: ORDER_VIEW"; n += 1
                break
    if n:
        save(p, "\n".join(lines), nl)
    print(f"orders: ORDER_VIEW on {n} billing-statement read(s)")

    # derive-lineage --apply adds entries and never updates them, so the lineage carries the new
    # permission by hand, as every other hand-set lineage field does.
    p = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    raw = io.open(p, encoding="utf-8", newline="").read()
    L = json.loads(raw)
    k = [op for op in ("getBillingStatement", "listBillingStatements") if L[op].get("perm") != "ORDER_VIEW"]
    for op in k:
        L[op]["perm"] = "ORDER_VIEW"
    if k:
        io.open(p, "w", encoding="utf-8", newline="").write(
            json.dumps(L, indent=1, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))
    print(f"lineage: ORDER_VIEW on {len(k)} billing-statement read(s)")


if __name__ == "__main__":
    main()
