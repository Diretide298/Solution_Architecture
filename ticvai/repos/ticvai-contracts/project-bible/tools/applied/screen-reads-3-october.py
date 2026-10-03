#!/usr/bin/env python3
"""Give every Block A screen that shows or edits data a read that returns it (the r1 gate's G3, CHG-R1S-004).

**Found by the r1 gate on 3 October 2026** (the judge's findings on ADM-069, POS-024, GST-077 and WEB-033):
a screen that edits saved data with a PUT and reads nothing back opens empty and overwrites what was
there; a picker with no operation has nothing to list. `tools/screen_patterns.py` rule READ found 47 such
Block A instances (34 edits with no read, 13 screens with no read at all); this applies the fix:

* **A read that exists is bound** on the screen (`apis`, purpose and provenance), on load when the screen
  already holds the read's parameters, otherwise when the user acts.
* **Where no read exists, one is added** beside its write, on the same path and returning the write's own
  schema: the read the write was always missing (18 operations, below). Each follows the new-operation
  gates: a permission in the vocabulary (the VIEW counterpart where one exists, otherwise the write's own),
  paging on a list, `x-ticvai-read-routing`, a 429.
* **Three contract facts the gate found** are corrected additively: `GuestMerchandiseItem` carries the
  `variantId` that `addCartLine` needs (WEB-033); `GuestMenu` names the tables it projects (POS-021,
  POS-024); POS-024's "86 an item" picker lists the outlet's menu (`getGuestMenu`).

Idempotent: an operation already present, a binding already made, is left alone.

    python tools/applied/screen-reads-3-october.py [--apply]
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_spec = importlib.util.spec_from_file_location("spf", HERE / "spec-screen-patterns-3-october.py")
spf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(spf)

CHG = "CHG-R1S-004"
PROV = f"r1 gate, 3 October 2026 ({CHG})"
PAGE = ["../shared/common.yaml#/components/parameters/PageSize",
        "../shared/common.yaml#/components/parameters/PageCursor"]

# ── the reads that did not exist ──────────────────────────────────────────────────────────────────
# (contract file, path, operationId, permission, scope, audience, schema, list?, summary, why, extra)
NEW_OPS = [
    ("contracts/satellite/fnb.yaml", "/combos", "listCombos", "PRODUCT_VIEW", "venue", ["staff"],
     "Combo", True, "The combos defined at the venue, with their slots",
     "BO-011 sets a combo's slots with `setComboSlots` and `createCombo` makes one; nothing listed them, "
     "so the screen could not show the slots it was about to replace.", {}),
    ("contracts/satellite/marketing-crm.yaml", "/customer-service-copilot", "getCustomerServiceCopilot",
     "AI_CONFIGURE", "venue", ["staff"], "AiCustomerServiceCopilotKnowledgeWorkspaceView", False,
     "The customer-service copilot configuration as saved",
     "BO-798 saves the copilot's configuration with `setCustomerServiceCopilot` and had no way to read it "
     "back. Gated by `AI_CONFIGURE`, as the write is: the vocabulary has no AI view permission for "
     "configuration.", {}),
    ("contracts/satellite/public-api.yaml", "/api-quotas", "listApiQuotas", "DEVELOPER_ADMIN", "tenant",
     ["staff"], "ApiQuota", True, "The rate limits and quotas set per client",
     "DEV-008 and ADM-015 set quotas with `setApiQuota` and nothing read them. `DEVELOPER_ADMIN`, as the "
     "write: `DEVELOPER_VIEW` is held by developers themselves, who must not read other clients' limits.", {}),
    ("contracts/satellite/public-api.yaml", "/api-anomaly-rules", "listApiAnomalyRules", "DEVELOPER_ADMIN",
     "tenant", ["staff"], "ApiAnomalyRule", True, "The rules that flag abnormal API traffic",
     "DEV-008 and ADM-015 set anomaly rules with `setApiAnomalyRule` and nothing read them.", {}),
    ("contracts/satellite/public-api.yaml", "/api-licensing", "listApiLicences", "DEVELOPER_ADMIN", "tenant",
     ["staff"], "ApiLicence", True, "The API licences granted, per client",
     "DEV-008 sets licences with `setApiLicensing`; `listApiScopes` lists the scopes a licence may grant, "
     "not the licences.", {}),
    ("contracts/satellite/public-api.yaml", "/developers/{developerId}", "getDeveloperAccount",
     "DEVELOPER_VIEW", "tenant", ["partner", "staff"], "DeveloperAccount", False,
     "A registered developer organisation",
     "DEV-002 registers an organisation (`registerDeveloper`) and sets its members; it had no read of the "
     "organisation it then shows. A partner reads only its own (`x-ticvai-self-scoped`).",
     {"new_path_after": "/developers", "path_param": "developerId", "self": "principal"}),
    ("contracts/spine/access.yaml", "/parking-entitlements/{entitlementId}", "getParkingEntitlement", None,
     "venue", ["guest"], "ParkingEntitlement", False, "One of the guest's parking entitlements",
     "WEB-041 and GST-027 change a parking entitlement with `updateParkingEntitlement` and never read it, "
     "so the plate and the dates they edit came from nowhere. Self-scoped, as the update is.",
     {"self": "subject"}),
    ("contracts/spine/access.yaml", "/virtual-ticket-identity", "getVirtualTicketIdentity",
     "ACCESS_POINT_CONFIGURE", "venue", ["staff"], "VirtualTicketIdentityMasterRecordConfigurationView", False,
     "The virtual ticket identity configuration as saved",
     "BO-335 saves it with `setVirtualTicketIdentity` and read nothing back. The vocabulary has no access "
     "view permission, so the write's own gates the read.", {}),
    ("contracts/spine/access.yaml", "/pdf-printable-pos", "getPdfPrintablePos", "ACCESS_POINT_CONFIGURE",
     "venue", ["staff"], "PdfPrintablePosTicketDesignerView", False,
     "The printable ticket design as saved",
     "BO-346 saves the design with `setPdfPrintablePos` and read nothing back.", {}),
    ("contracts/spine/access.yaml", "/ble-beacon-geofence", "getBleBeaconGeofence", "ACCESS_POINT_CONFIGURE",
     "venue", ["staff"], "BleBeaconGeofenceConfigurationView", False,
     "The BLE beacon and geofence configuration as saved",
     "BO-168 saves it with `setBleBeaconGeofence` and read nothing back.", {}),
    ("contracts/spine/access.yaml", "/biometric-verification-profile", "getBiometricVerificationProfile",
     "ACCESS_POINT_CONFIGURE", "venue", ["staff"], "BiometricVerificationProfileBuilderView", False,
     "The biometric verification profile as saved",
     "BO-185 saves it with `setBiometricVerificationProfile` and read nothing back.", {}),
    ("contracts/spine/access.yaml", "/face-pass-enrollment", "getFacePassEnrollmentConfiguration",
     "ACCESS_POINT_CONFIGURE", "venue", ["staff"], "FacePassEnrollmentConfigurationView", False,
     "The FacePass enrolment configuration as saved",
     "BO-186 saves it with `setFacePassEnrollment` and read nothing back. Not `getFacePassEnrolment`, "
     "which is a guest's own enrolment.", {}),
    ("contracts/spine/catalogue.yaml", "/products/{productId}/attributes", "getProductAttributes",
     "PRODUCT_VIEW", "venue", ["staff"], None, False, "A product's attribute axes",
     "BO-007, BO-008 and BO-012 replace a product's axes with `setProductAttributes`, whose body is the "
     "whole set, and had no way to read the set they were replacing.",
     {"inline": "axes"}),
    ("contracts/spine/catalogue.yaml", "/tax-profile-jurisdiction", "getTaxProfileJurisdiction",
     "PRODUCT_VIEW", "venue", ["staff"], "TaxProfileJurisdictionConfigurationView", False,
     "The tax profile and jurisdiction configuration as saved",
     "ADM-069 saves it with `setTaxProfileJurisdiction`, which is PUT-only; the r1 gate found the screen "
     "shows a profile it cannot read.", {}),
    ("contracts/spine/catalogue.yaml", "/package-pricing", "getPackagePricingDefinition", "PRICE_VIEW",
     "venue", ["staff"], "PackagePricing", False, "The package pricing definition as saved",
     "BO-011 saves it with `setPackagePricingDefinition` and read nothing back.", {}),
    ("contracts/spine/tenancy.yaml", "/devices/{deviceId}/assignment", "getDeviceAssignment", "DEVICE_VIEW",
     "venue", ["staff"], "DeviceAssignment", False, "Where a device is assigned",
     "POS-016 assigns a device with `setDeviceAssignment` and could not show where it was assigned.", {}),
    ("contracts/satellite/fnb.yaml", "/substitution-rules", "listSubstitutionRules", "PRODUCT_VIEW", "venue",
     ["staff"], "SubstitutionRule", True, "What may replace what, as saved",
     "BO-111 replaces the substitution rules with `setSubstitutionRules` (a whole-set PUT under `If-Match`) and "
     "could not read the set, or its ETag, before replacing it.", {}),
    ("contracts/satellite/transport.yaml", "/transport/departures/{departureId}", "getTransportDeparture",
     None, "venue", ["guest", "public"], "DepartureOffer", False, "One departure, as a guest books it",
     "GST-077 is opened on a departure (`departureId` from GST-076) and never read it: the r1 gate found "
     "the trip page showing a departure it had no read of. Published network data, as "
     "`getNextTransportDeparture` is.", {"guest_public": True}),
]

# ── the bindings ──────────────────────────────────────────────────────────────────────────────────
# screen -> [(operationId, contract, purpose)]
BIND = {
    "WEB-031": [("listMyTableReservations", "fnb", "Show the guest's own reservations, the one being changed among them")],
    "WEB-036": [("listMyTableReservations", "fnb", "Show the guest's own reservations, the one being changed among them")],
    "WEB-041": [("getParkingEntitlement", "access", "Load the parking entitlement being changed")],
    "GST-027": [("getParkingEntitlement", "access", "Load the parking entitlement being changed")],
    "GST-033": [("listAiConversations", "ai", "Show the guest's earlier conversations with the assistant")],
    "GST-045": [("listTicketTransfers", "orders", "Show the tickets the guest has sent and received")],
    "GST-048": [("getCart", "orders", "Show the cart the suggestions are for")],
    "GST-067": [("getOrder", "orders", "Load the order a refund or resale is asked for")],
    "POS-014": [("getOrder", "orders", "Load the order the exception applies to")],
    "POS-016": [("getDeviceAssignment", "tenancy", "Show where the selected device is assigned")],
    "POS-017": [("listCashMovements", "shift", "Show the shift's cash in and cash out so far")],
    "POS-024": [("getGuestMenu", "fnb", "List the outlet's menu items for the '86 an item' picker")],
    "BO-007": [("getProductAttributes", "catalogue", "Load the product's attribute axes before they are replaced")],
    "BO-008": [("getProductAttributes", "catalogue", "Load the product's attribute axes before they are replaced")],
    "BO-012": [("getProductAttributes", "catalogue", "Load the product's attribute axes before they are replaced")],
    "BO-011": [("listCombos", "fnb", "List the combos and their slots"),
               ("getBundle", "promotions", "Load the bundle being edited"),
               ("getPackagePricingDefinition", "catalogue", "Load the package pricing as saved")],
    "BO-032": [("listEntryRulePoints", "access", "Show the rule's entry points before they are replaced")],
    "BO-044": [("listDeliveryLocations", "fnb", "Show the delivery locations and the outlets mapped to them")],
    "BO-065": [("listDeliveryLocations", "fnb", "Show the delivery locations and the outlets mapped to them")],
    "BO-111": [("listIngredientSubstitutes", "fnb", "Show the recipe's approved substitutions"),
               ("listSubstitutionRules", "fnb", "Show the substitution rules before they are replaced")],
    "BO-117": [("getCatalogueImportJob", "catalogue", "Show the import's progress and its findings")],
    "BO-130": [("getOfflinePolicy", "tenancy", "Load the offline policy saved at this scope")],
    "BO-136": [("getCourseRules", "fnb", "Load the outlet's course rules as saved")],
    "BO-168": [("getBleBeaconGeofence", "access", "Load the configuration as saved")],
    "BO-185": [("getBiometricVerificationProfile", "access", "Load the profile as saved")],
    "BO-186": [("getFacePassEnrollmentConfiguration", "access", "Load the configuration as saved")],
    "BO-335": [("getVirtualTicketIdentity", "access", "Load the configuration as saved")],
    "BO-346": [("getPdfPrintablePos", "access", "Load the design as saved")],
    "BO-618": [("listAccreditationProgrammes", "accreditation", "Show the programmes, the one being changed among them")],
    "BO-798": [("getCustomerServiceCopilot", "marketing-crm", "Load the copilot configuration as saved")],
    "BO-827": [("listLoyaltyCampaigns", "marketing-crm", "Show the loyalty campaigns")],
    "BO-828": [("listLoyaltyProgrammes", "marketing-crm", "Show the programmes and their milestones"),
               ("listRewards", "marketing-crm", "Show the rewards a milestone can give")],
    "BO-877": [("getExperienceResourceRequirements", "resources", "Load the experience's resource requirements"),
               ("listResources", "resources", "List the resources the assignment rules choose from")],
    "ADM-069": [("getTaxProfileJurisdiction", "catalogue", "Load the tax profile and jurisdiction as saved")],
    "ADM-243": [("listApprovalMatrices", "approvals", "Show the approval matrices, the one being changed among them")],
    "ADM-412": [("listPaymentProviders", "orders", "Show the payment providers as configured")],
    "SUP-002": [("listAgentWorkloadAvailability", "marketing-crm", "Show the agents' availability as saved")],
    "CMS-009": [("getTenantConfig", "white-label", "Load the working header and footer")],
    "DEV-002": [("getDeveloperAccount", "public-api", "Show the registered organisation and its members")],
    "DEV-008": [("listApiQuotas", "public-api", "Show the quotas per client"),
                ("listApiAnomalyRules", "public-api", "Show the anomaly rules"),
                ("listApiLicences", "public-api", "Show the licences per client")],
    "GST-077": [("getTransportDeparture", "transport", "Load the departure the trip was opened on")],
}


def _block(lines, indent):
    pad = " " * indent
    return [pad + l if l else "" for l in lines]


def op_yaml(op, path_params) -> list:
    (cfile, path, oid, perm, scope, aud, schema, is_list, summary, why, extra) = op
    L = [f"get:", f"  operationId: {oid}"]
    L.append(f"  x-ticvai-audience: [{', '.join(aud)}]")
    L.append("  x-ticvai-read-routing: replica")
    L.append(f"  summary: {summary}")
    L.append("  description: >")
    txt = (f"**Added by the r1 gate fix of 3 October 2026 ({CHG}): the read this write was missing.** {why} "
           f"Returns what the write stores, in the write's own shape."
           + (" Ordered by creation (`id`, a UUIDv7), oldest first." if is_list else ""))
    words, line = txt.split(), ""
    for w in words:
        if len(line) + len(w) + 1 > 100:
            L.append("    " + line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        L.append("    " + line)
    if perm:
        L.append(f"  x-ticvai-permission: {perm}")
    else:
        L.append("  x-ticvai-permission: null")
    if extra.get("self"):
        L.append(f"  x-ticvai-self-scoped: {extra['self']}")
    L.append(f"  x-ticvai-scope-level: {scope}")
    L.append("  x-ticvai-offline-capable: false")
    L.append("  x-ticvai-conflict-policy: serverWins")
    if extra.get("guest_public"):
        L += ["  security:", "    - guestAuth: []", "    - bearerAuth: []"]
    params = []
    for p in path_params:
        params += [f"    - name: {p}", "      in: path", "      required: true",
                   "      schema: { type: string, format: uuid }"]
    if is_list:
        params += [f"    - $ref: '{r}'" for r in PAGE]
    if params:
        L += ["  parameters:"] + params
    L += ["  responses:", "    '200':", f"      description: {summary}", "      content:",
          "        application/json:", "          schema:"]
    if extra.get("inline") == "axes":
        L += ["            type: object", "            required: [axes]", "            properties:",
              "              axes:", "                type: array",
              "                items: { $ref: '#/components/schemas/VariantDimension' }"]
    elif is_list:
        L += ["            allOf:", "              - $ref: '../shared/common.yaml#/components/schemas/Page'",
              "              - type: object", "                properties:", "                  items:",
              "                    type: array", "                    items:",
              f"                      $ref: '#/components/schemas/{schema}'"]
    else:
        L += [f"            $ref: '#/components/schemas/{schema}'"]
    L += ["    '403': { $ref: '../shared/common.yaml#/components/responses/Forbidden' }"]
    if not is_list:
        L += ["    '404': { $ref: '../shared/common.yaml#/components/responses/NotFound' }"]
    L += ["    '429':", "      $ref: '../shared/common.yaml#/components/responses/TooManyRequests'"]
    return L


def add_ops(apply: bool) -> list:
    done = []
    for op in NEW_OPS:
        cfile, path, oid, extra = op[0], op[1], op[2], op[10]
        f = ROOT / cfile
        raw = f.read_text(encoding="utf-8")
        crlf = "\r\n" in raw
        t = raw.replace("\r\n", "\n")
        if re.search(rf"^\s+operationId: {oid}\s*$", t, re.M):
            continue
        lines = t.split("\n")
        key = f"  {path}:"
        if "new_path_after" in extra:
            anchor = f"  {extra['new_path_after']}:"
            i = lines.index(anchor)
            j = i + 1
            while j < len(lines) and not re.match(r"^  /", lines[j]) and not re.match(r"^\S", lines[j]):
                j += 1
            block = [key] + _block(op_yaml(op, [extra["path_param"]]), 4)
            lines[j:j] = block
        else:
            i = lines.index(key)
            j = i + 1
            # before the item's first method, so a path-level `parameters:` block stays above it
            while j < len(lines) and not re.match(r"^    (get|put|post|patch|delete):", lines[j]) \
                    and not re.match(r"^  \S|^\S", lines[j]):
                j += 1
            lines[j:j] = _block(op_yaml(op, []), 4)
        t = "\n".join(lines)
        if crlf:
            t = t.replace("\n", "\r\n")
        if apply:
            open(f, "w", encoding="utf-8", newline="").write(t)
        done.append(oid)
    return done


def contract_facts(apply: bool) -> list:
    out = []
    f = ROOT / "contracts/satellite/retail.yaml"
    raw = f.read_text(encoding="utf-8")
    t = raw.replace("\r\n", "\n")
    old = ("        isReturnable: { type: boolean }\n        returnWindowDays: { type: integer, nullable: true }\n"
           "        imageAssetRef: { type: string, nullable: true }\n\n    MerchandiseConflictProblem:")
    if "variantId:" not in t.split("    GuestMerchandiseItem:")[1].split("    MerchandiseConflictProblem:")[0]:
        assert t.count(old) == 1
        new = old.replace("        imageAssetRef: { type: string, nullable: true }\n",
                          "        imageAssetRef: { type: string, nullable: true }\n"
                          "        variantId:\n"
                          "          type: string\n"
                          "          format: uuid\n"
                          "          description: >\n"
                          "            The catalogue variant the item sells, which `addCartLine` takes (added 3 October\n"
                          f"            2026, {CHG}: the r1 gate found WEB-033 could not add to the cart from the guest\n"
                          "            projection). An id, not the variant record: price and tax still come from the server.\n")
        t = t.replace(old, new)
        if "\r\n" in raw:
            t = t.replace("\n", "\r\n")
        if apply:
            open(f, "w", encoding="utf-8", newline="").write(t)
        out.append("GuestMerchandiseItem.variantId")
    f = ROOT / "contracts/satellite/fnb.yaml"
    raw = f.read_text(encoding="utf-8")
    old = "x-ticvai-persistence: none — projection over menu, item and availability"
    if old in raw:
        raw = raw.replace(old, "x-ticvai-persistence: none — projection over fnb.menu, fnb.menu_item and availability")
        if apply:
            open(f, "w", encoding="utf-8", newline="").write(raw)
        out.append("GuestMenu names its tables")
    return out


def bind(apply: bool) -> list:
    F = spf.ScreenFiles()
    log = []
    for sid, entries in BIND.items():
        s = F.screens[sid]
        params = {p.get("name") if isinstance(p, dict) else p for p in ((s.get("entryState") or {}).get("params") or [])}
        for oid, contract, purpose in entries:
            if any(a.get("operationId") == oid for a in s.get("apis") or []):
                continue
            s.setdefault("apis", []).append({"operationId": oid, "contract": contract, "purpose": purpose,
                                             "trigger": "onLoad", "provenance": PROV})
            F.dirty.add(sid)
            log.append(f"{sid} + {oid}")
        if sid == "POS-024":
            for r in (s.get("layout") or {}).get("regions") or []:
                for c in r.get("components") or []:
                    if c.get("kind") == "multiSelect" and c.get("label") == "86 an item" and not c.get("operation"):
                        c["operation"] = "getGuestMenu"
                        c["bindsTo"] = "GuestMenu.sections"
                        c["notes"] = ("Lists the outlet's menu items; ticking one sends `setItemAvailability` "
                                      f"(r1 gate, {CHG}).")
                        F.dirty.add(sid)
                        log.append("POS-024 picker reads getGuestMenu")
    reach(F, log)
    settle(F, log)
    if apply and F.dirty:
        F.write()
    return log


def settle(F, log):
    """The reads added before the card-list rule above, moved to it where they paired a table with a panel
    of another entity (S-PANEL-ENTITY)."""
    import re as _re
    fam = lambda n: _re.sub(r"(Summary|Detail|View|Row|Item|Line)$", "", n or "")
    for sid in BIND:
        s = F.screens[sid]
        comps = [c for r in (s.get("layout") or {}).get("regions") or [] for c in r.get("components") or []]
        mine = [c for c in comps if c.get("provenance") == PROV and c.get("kind") in ("dataTable", "detailPanel")]
        for c in mine:
            others = [x for x in comps if x is not c and x.get("kind") in ("dataTable", "detailPanel")]
            if any(fam(str(x.get("bindsTo") or "").split(".")[0]) != fam(str(c.get("bindsTo") or "").split(".")[0])
                   for x in others):
                c["kind"] = "cardList"
                F.dirty.add(sid)
                log.append(f"{sid}: {c.get('operation')} shown as a card list")


def reach(F, log):
    """**Every read bound here is reached by a component** (check-screen-wiring S-OP-UNREACHED, R273): a list
    read gets a table and a single read a panel, with the columns the pattern rules pick (P2)."""
    sys.path.insert(0, str(ROOT / "tools"))
    import screen_patterns as sp
    pk = sp.Package(str(ROOT), screens=F.screens)
    for code, f in ((d["platform"]["code"], f) for f, d in F.doc.items()):
        pk.platforms[code] = F.doc[f]["platform"]
    for sid, entries in BIND.items():
        s = F.screens[sid]
        used = {c.get("operation") for _, c in sp.components(s)}
        used |= {(o.get("confirm") or {}).get("operation") for o in s.get("overlays") or []}
        for oid, contract, purpose in entries:
            if oid in used or oid not in pk.ops:
                continue
            names = sorted(sp._resp_schemas(pk, oid, deep=False) - {"Page"})
            name = names[0] if names else ""
            kind = "dataTable" if oid.startswith("list") else "detailPanel"
            # a screen that already lists or details another entity keeps one table and one panel
            # (check-screen-wiring S-PANEL-ENTITY): the added read is a card list beside them
            if any(x.get("kind") in ("dataTable", "detailPanel") for _, x in sp.components(s)):
                kind = "cardList"
            c = {"kind": kind, "label": purpose, "operation": oid}
            if name:
                _, sch = pk.schema(name, pk.ops[oid]["_contract"])
                props = list(((sch or {}).get("properties") or {}).keys())
                c["bindsTo"] = name
                c["columns"] = [f"{name}.{p}" for p in props]
                c["columns"] = sp.pick_columns(pk, c, pk.small(sid))
            c["provenance"] = PROV
            regs = (s.get("layout") or {}).get("regions") or []
            reg = next((r for r in regs if r.get("name") == "contentBody"), regs[0] if regs else None)
            if reg is None:
                s.setdefault("layout", {"template": "detail", "regions": []})["regions"].append(
                    {"name": "contentBody", "slot": "record", "components": []})
                reg = s["layout"]["regions"][-1]
            reg.setdefault("components", []).insert(0, c)
            F.dirty.add(sid)
            log.append(f"{sid} reaches {oid} ({kind} {name})")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    ops = add_ops(a.apply)
    facts = contract_facts(a.apply)
    log = bind(a.apply)
    print(f"{len(ops)} read(s) added: {', '.join(ops)}")
    print(f"{len(facts)} contract fact(s): {', '.join(facts)}")
    print(f"{len(log)} binding(s):\n  " + "\n  ".join(log))
    if not a.apply:
        print("nothing written: pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
