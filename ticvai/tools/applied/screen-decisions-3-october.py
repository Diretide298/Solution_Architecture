#!/usr/bin/env python3
"""Apply Chinmay's 3 October answers that change a screen (the Block A audit's business rules).

**Decided by Chinmay on 3 October 2026** in the answers to the Block A audit (`Pattern 4`, `Block A
audit business rules` and the questions answered as recommended). Each is a change entry:

  CHG-SPF-007  GST-001 and WEB-001 stop calling `listAnalyticsProviders` (TENANT_CONFIGURE): a
               guest reads the analytics providers from the published tenant config.
  CHG-SPF-008  KIT-007, the kitchen's guest board, is read-only: order numbers, Preparing and Ready,
               in the order the server returns them, no buttons; handover stays on KIT-006.
  CHG-SPF-009  BO-056: attendance is self clock-in on the staff app; the back office corrects it with
               `amendAttendance` and no longer records it.
  CHG-SPF-010  BO-078: one `approveRequisition` call carries the decision (approve, reject, return);
               the separate reject and return operations leave the screen (and flow F92).
  CHG-SPF-011  ANL-023: the first Save creates the dashboard (`createDashboard`), later saves update
               it; the refresh budget is checked on both.
  CHG-SPF-012  POS-000: session management stays on the till's door behind a supervisor PIN step-up
               (reverses CHG-DOOR-003 for this screen only); GST-055's admission QR rotates every
               30 seconds; GST-053's add-on toggle sends `updateVisitPlan` addAddOn / removeAddOn;
               a signed-out guest builds and changes a plan (GST-053, GST-054).
  CHG-SPF-013  Operations another agent adds, bound here by their agreed names: the guest chat
               screens (GST-031, GST-032, WEB-044) send with `sendGuestConversationMessage` and stream
               the assistant's answers; GST-070 lists the guest's own reservations and waitlist places
               (`listMyTableReservations`) and the restaurants that take bookings
               (`listBookableOutlets`); EMP-026 uploads photos (`uploadIncidentMedia`) and records a
               person involved (`addIncidentPerson`).

Every edit finds its target and does nothing when it is already done, so a second run says there is
nothing to do. Screens are spliced back one at a time by the 3 October pattern fix's writer.

    python tools/applied/screen-decisions-3-october.py [--apply] [--only 007,008,...]
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

WHO = "decided by Chinmay, 3 October 2026"


def prov(chg):
    return f"{WHO} ({chg})"


def drop_api(s, op):
    before = len(s.get("apis") or [])
    s["apis"] = [a for a in s.get("apis") or [] if a.get("operationId") != op]
    return len(s["apis"]) != before


def drop_components(s, pred):
    n = 0
    for r in (s.get("layout") or {}).get("regions") or []:
        keep = [c for c in r.get("components") or [] if not pred(c)]
        n += len(r.get("components") or []) - len(keep)
        r["components"] = keep
    s["layout"]["regions"] = [r for r in s["layout"]["regions"] if r.get("components") or r.get("ref")]
    return n


def drop_overlays(s, ids):
    before = len(s.get("overlays") or [])
    s["overlays"] = [o for o in s.get("overlays") or [] if o.get("id") not in ids]
    return len(s["overlays"]) != before


def add_api(s, entry):
    if any(a.get("operationId") == entry["operationId"] for a in s.get("apis") or []):
        return False
    s.setdefault("apis", []).append(entry)
    return True


def region(s, name):
    for r in s["layout"]["regions"]:
        if r.get("name") == name:
            return r
    r = {"name": name, "components": []}
    s["layout"]["regions"].append(r)
    return r


def add_component(s, rname, comp):
    for _, c in spf.sp.components(s):
        if c.get("label") == comp["label"] and c.get("operation") == comp.get("operation"):
            return False
    region(s, rname)["components"].append(comp)
    return True


def note(obj, key, text):
    v = str(obj.get(key) or "")
    if text in v:
        return False
    obj[key] = (v.rstrip() + "\n\n" + text) if v else text
    return True


def comp_by(s, **kw):
    for _, c in spf.sp.components(s):
        if all(c.get(k) == v for k, v in kw.items()):
            return c
    return None


# ── CHG-SPF-007 ──────────────────────────────────────────────────────────────────────────────────

def d007(S, log):
    hit = False
    for sid in ("GST-001", "WEB-001"):
        s = S[sid]
        if drop_api(s, "listAnalyticsProviders"):
            log.append(f"007 {sid}: listAnalyticsProviders removed")
            hit = True
        for a in s.get("apis") or []:
            if a.get("operationId") == "getPublishedTenantConfig" and note(
                    a, "purpose", "Also the analytics providers to start once their consent category is "
                                  "granted, from the published config (listAnalyticsProviders needs "
                                  "TENANT_CONFIGURE and left the guest screens: " + prov("CHG-SPF-007")
                                  + ")."):
                hit = True
    return hit


# ── CHG-SPF-008 ──────────────────────────────────────────────────────────────────────────────────

def d008(S, log):
    s = S["KIT-007"]
    hit = False
    if drop_api(s, "recordOrderHandover"):
        hit = True
    if drop_components(s, lambda c: c.get("operation") == "recordOrderHandover"
                       or (c.get("kind") == "cardList" and not c.get("label")
                           and c.get("bindsTo") == "KitchenTicket[]")):
        hit = True
    if drop_overlays(s, {"formRecordOrderHandover"}):
        hit = True
    es = s.get("entryState") or {}
    if any(p.get("name") == "orderId" for p in es.get("params") or []):
        es["params"] = [p for p in es["params"] if p.get("name") != "orderId"]
        hit = True
    board = comp_by(s, operation="listKitchenTickets", kind="cardList")
    if board and note(board, "notes", "**Read-only, in the order the server returns** ("
                      + prov("CHG-SPF-008") + "): order numbers, Preparing and Ready for pickup, no "
                      "buttons and no re-sorting on the display. The handover is recorded on KIT-006."):
        hit = True
    if hit:
        note(s, "notes", "**An unattended guest display, read-only** (" + prov("CHG-SPF-008") + "): "
             "`recordOrderHandover`, its button and form left this screen; a handover is recorded "
             "on KIT-006 Expo / Pass.")
        log.append("008 KIT-007: read-only board, handover removed")
    return hit


# ── CHG-SPF-009 ──────────────────────────────────────────────────────────────────────────────────

def d009(S, log):
    s = S["BO-056"]
    hit = drop_api(s, "recordAttendance")
    hit |= bool(drop_components(s, lambda c: c.get("operation") == "recordAttendance"))
    hit |= drop_overlays(s, {"formRecordAttendance"})
    if hit:
        note(s, "notes", "**Attendance is self clock-in only** (" + prov("CHG-SPF-009") + ", not the "
             "recommendation): staff clock in and out themselves on the staff app (`recordAttendance`, "
             "EMP-024 and EMP-025); a supervisor corrects a record afterwards here with Amend attendance "
             "(`amendAttendance`). Record attendance left this screen.")
        log.append("009 BO-056: Record attendance removed")
    return hit


# ── CHG-SPF-010 ──────────────────────────────────────────────────────────────────────────────────

def d010(S, F, log):
    s = S["BO-078"]
    hit = False
    for op in ("rejectRequisition", "returnRequisition"):
        hit |= drop_api(s, op)
    hit |= bool(drop_components(s, lambda c: c.get("operation") in ("rejectRequisition",
                                                                       "returnRequisition")))
    hit |= drop_overlays(s, {"confirmRejectRequisition", "formReturnRequisition"})
    btn = comp_by(s, operation="approveRequisition")
    if btn and btn.get("label") != "Decide requisition":
        btn["label"] = "Decide requisition"
        btn["notes"] = ("**One decision call** (" + prov("CHG-SPF-010") + "): approve, reject or "
                        "return, with the reason a reject or a return needs.")
        hit = True
    for o in s.get("overlays") or []:
        if o.get("id") == "formApproveRequisition" and "approve, reject or return" not in str(o.get("body")):
            o["trigger"] = "Decide requisition"
            o["confirm"]["label"] = "Send decision"
            o["body"] = ("**Collects the decision `approveRequisition` sends** (" + prov("CHG-SPF-010")
                         + "): `decision` is approve, reject or return; a reject or a return names "
                         "its reason in `note`, which the form will not send empty. Optional: "
                         "`amendedLines` (approve only). Dismissing sends nothing; the screen behind is "
                         "unchanged.")
            hit = True
    if hit:
        log.append("010 BO-078: reject and return folded into approveRequisition")
    f92 = ROOT / "flows" / "F92-store-stock-is-watched-replenished-and-reconcile.yaml"
    t = f92.read_text(encoding="utf-8")
    old = "  - rejectRequisition\n  - returnRequisition\n  - updateRequisitionLines\n"
    if old in t:
        F[f92] = t.replace(old, "  - approveRequisition\n  - updateRequisitionLines\n")
        log.append("010 F92: step 3 decides with approveRequisition")
        hit = True
    f15 = next((ROOT / "flows").glob("F15-*.yaml"))
    t = F.get(f15) or f15.read_text(encoding="utf-8")
    old = "is the whole reason `returnRequisition` exists."
    if old in t:
        F[f15] = t.replace(old, "is why `approveRequisition` has a return decision (CHG-SPF-010).")
        log.append("010 F15: branch names the return decision")
        hit = True
    return hit


# ── CHG-SPF-011 ──────────────────────────────────────────────────────────────────────────────────

def d011(S, log):
    s = S["ANL-023"]
    hit = add_api(s, {"operationId": "createDashboard", "contract": "reporting",
                      "purpose": "The first Save of a new dashboard; later saves update it",
                      "trigger": "onAction", "invalidates": ["getDashboard"],
                      "provenance": prov("CHG-SPF-011")})
    btn = comp_by(s, kind="primaryButton", label="Save dashboard")
    if btn and "createDashboard" not in str(btn.get("notes")):
        btn["notes"] = ("**The first Save creates the dashboard (`createDashboard`), every later Save "
                        "updates it (`updateDashboard`)** (" + prov("CHG-SPF-011") + "); the refresh "
                        "budget is checked on both. " + str(btn.get("notes") or ""))
        hit = True
    for p in (s.get("entryState") or {}).get("params") or []:
        if p.get("name") == "dashboardId" and not p.get("optional"):
            p["optional"] = True
            p["notes"] = ("Optional (" + prov("CHG-SPF-011") + "): opened without one, the canvas is a "
                          "new dashboard and its first Save creates it.")
            hit = True
    if not any(o.get("id") == "formCreateDashboard" for o in s.get("overlays") or []):
        s.setdefault("overlays", []).append({
            "id": "formCreateDashboard", "component": "modal", "trigger": "Save dashboard",
            "body": ("**The first Save of a new dashboard** (" + prov("CHG-SPF-011") + "): names it "
                     "and creates it with `createDashboard`, tiles and all; every later Save goes "
                     "straight to `updateDashboard`. The refresh budget is checked here too. "
                     "Dismissing sends nothing; the canvas keeps its tiles."),
            "confirm": {"label": "Create dashboard", "operation": "createDashboard"},
            "dismiss": {"label": "Keep editing", "discards": []},
            "provenance": prov("CHG-SPF-011")})
        hit = True
    st = s.get("states") or {}
    na = ("Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listReports` requires to show this "
          "screen, and names that permission. A caller without `REPORT_MANAGE` sees the dashboard "
          "read-only: Save (`createDashboard`, `updateDashboard`) and Archive (`deleteDashboard`) are "
          "disabled and name that permission (" + prov("CHG-SPF-011") + ").")
    if st.get("emptyNoAccess") != na:
        st["emptyNoAccess"] = na
        hit = True
    if hit:
        log.append("011 ANL-023: first Save creates, later saves update")
    return hit


# ── CHG-SPF-012 ──────────────────────────────────────────────────────────────────────────────────

def d012(S, log):
    hit = False
    s = S["POS-000"]
    for a in s.get("apis") or []:
        if a.get("operationId") == "listActiveSessions" and a.get("trigger") != "onAction":
            a["trigger"] = "onAction"
            a["purpose"] = ("Who holds this till now, read only after a supervisor's PIN step-up: "
                            "nobody is signed in at the door (" + prov("CHG-SPF-012") + ")")
            hit = True
    # The PIN is asked in the step-up prompt the panel opens (no new control: the step-up input
    # itself is the contract's to add, see the CHG-SPF-012 notes).
    panel = comp_by(s, label="Signed in on this till now")
    if panel and note(panel, "notes", "**Opens only after a supervisor's PIN step-up** ("
                      + prov("CHG-SPF-012") + ", not the recommendation; reverses CHG-DOOR-003 for "
                      "this screen). Nobody is signed in at a till's door, so a supervisor's PIN, asked "
                      "in the step-up prompt this panel opens, authorises `listActiveSessions` and "
                      "`forceLogout` here; BO-053 keeps them too. The PIN is masked and never stored "
                      "on the till."):
        hit = True
    if drop_components(s, lambda c: c.get("label") == "Supervisor PIN"):
        hit = True
    s = S["GST-055"]
    code = comp_by(s, label="Your code")
    if code and note(code, "notes", "**Every 30 seconds** (" + prov("CHG-SPF-012") + ": GST-055's "
                     "admission QR rotates every 30 seconds; the answer named GST-069 and meant this "
                     "screen): the default above, which the venue may change."):
        hit = True
    s = S["GST-053"]
    tog = comp_by(s, label="Add Fast Track")
    if tog and note(tog, "notes", "Sends `updateVisitPlan` with the change kind `addAddOn` (on) or "
                    "`removeAddOn` (off); the add-on is priced at booking (" + prov("CHG-SPF-012") + ")."):
        hit = True
    for sid in ("GST-053", "GST-054"):
        s = S[sid]
        if note(s, "notes", "**A signed-out guest builds and changes a plan** (" + prov("CHG-SPF-012")
                + "): the plan lives in an anonymous session; signing in is asked only to save, share "
                "or book, and the plan moves to the account on sign-in."):
            hit = True
    if hit:
        log.append("012 POS-000, GST-055, GST-053, GST-054: decisions noted")
    return hit


# ── CHG-SPF-013 (operations another agent adds) ─────────────────────────────────────────────────

GUEST_SEND = "sendGuestConversationMessage"


def d013(S, log):
    hit = False
    for sid in ("GST-031", "GST-032", "WEB-044"):
        s = S[sid]
        for a in s.get("apis") or []:
            if a.get("operationId") == "sendConversationMessage":
                a["operationId"] = GUEST_SEND
                a["contract"] = "marketing-crm"
                a["purpose"] = ("After a handover, the guest writes to the agent, as the guest: "
                                "sendConversationMessage needs CASE_MANAGE (" + prov("CHG-SPF-013") + ")")
                hit = True
        for _, c in spf.sp.components(s):
            if c.get("operation") == "sendConversationMessage":
                c["operation"] = GUEST_SEND
                if c.get("label") == "Send conversation message":
                    c["label"] = "Send to the agent"
                hit = True
            if c.get("operation") == "sendAiMessage" and c.get("kind") in ("assistantPanel",
                                                                           "secondaryButton"):
                if note(c, "notes", "**Answers stream** (" + prov("CHG-SPF-013") + "): server-sent "
                        "events carry the tokens, then the sources and any proposed action; the full "
                        "message is stored once it ends."):
                    hit = True
        for o in s.get("overlays") or []:
            if (o.get("confirm") or {}).get("operation") == "sendConversationMessage":
                o["confirm"]["operation"] = GUEST_SEND
                o["confirm"]["label"] = "Send to the agent"
                o["trigger"] = "Send to the agent"
                o["id"] = "formSendGuestConversationMessage"
                o["body"] = str(o.get("body")).replace("sendConversationMessage", GUEST_SEND)
                hit = True
            elif "sendConversationMessage" in str(o.get("body")):
                o["body"] = str(o["body"]).replace("sendConversationMessage", GUEST_SEND)
                hit = True
        for _, c in spf.sp.components(s):
            if "`sendConversationMessage`" in str(c.get("notes")):
                c["notes"] = str(c["notes"]).replace("`sendConversationMessage`", f"`{GUEST_SEND}`")
                hit = True
    if hit:
        log.append("013 GST-031, GST-032, WEB-044: guest send, streamed answers")

    s = S["GST-070"]
    h2 = add_api(s, {"operationId": "listMyTableReservations", "contract": "fnb",
                     "purpose": "The guest's own table reservations and waitlist places (self-scoped)",
                     "trigger": "onLoad", "provenance": prov("CHG-SPF-013")})
    h2 |= add_api(s, {"operationId": "listBookableOutlets", "contract": "fnb",
                      "purpose": "The restaurants that take bookings, published data",
                      "trigger": "onLoad", "provenance": prov("CHG-SPF-013")})
    h2 |= add_component(s, "contentBody", {
        "kind": "cardList", "label": "Your reservations and waitlist places",
        "operation": "listMyTableReservations",
        "notes": ("The guest's own, upcoming first; each opens Change or cancel, or Leave the waitlist. "
                  "Empty: *No reservations yet* with Reserve."), "provenance": prov("CHG-SPF-013")})
    h2 |= add_component(s, "contentBody", {
        "kind": "selectField", "label": "Restaurant", "operation": "listBookableOutlets",
        "notes": "Only the restaurants that take bookings, as published; the choice scopes Reserve and "
                 "Join the waitlist.", "provenance": prov("CHG-SPF-013")})
    for p in (s.get("entryState") or {}).get("params") or []:
        if p.get("name") in ("entryId", "reservationId") and not p.get("optional"):
            p["optional"] = True
            p["notes"] = ("Optional (" + prov("CHG-SPF-013") + "): opened without it, the screen lists "
                          "the guest's own with `listMyTableReservations`; a link opens that one.")
            h2 = True
    if h2:
        log.append("013 GST-070: own reservations and bookable restaurants bound")
        hit = True

    s = S["EMP-026"]
    h3 = add_api(s, {"operationId": "uploadIncidentMedia", "contract": "maintenance",
                     "purpose": "Photos of the incident", "trigger": "onAction",
                     "provenance": prov("CHG-SPF-013")})
    h3 |= add_api(s, {"operationId": "addIncidentPerson", "contract": "maintenance",
                      "purpose": "A person involved, stored as a PII subject", "trigger": "onAction",
                      "provenance": prov("CHG-SPF-013")})
    h3 |= add_api(s, {"operationId": "searchGuests", "contract": "marketing-crm",
                      "purpose": "The optional guest lookup for a person involved", "trigger": "onAction",
                      "provenance": prov("CHG-SPF-013")})
    h3 |= add_component(s, "contentBody", {
        "kind": "fileUpload", "label": "Photos", "operation": "uploadIncidentMedia",
        "notes": "From the camera or the gallery, several at once; each uploads as it is added and "
                 "can be removed before the report is sent.", "provenance": prov("CHG-SPF-013")})
    h3 |= add_component(s, "actionBar", {
        "kind": "secondaryButton", "label": "Add a person involved", "operation": "addIncidentPerson",
        "provenance": prov("CHG-SPF-013")})
    h3 |= add_component(s, "contextPanel", {
        "kind": "searchField", "label": "Find the guest involved", "operation": "searchGuests",
        "notes": "Optional, inside Add a person involved: a guest found here fills name and contact "
                 "from the guest's record, so the person is linked rather than typed again.",
        "provenance": prov("CHG-SPF-013")})
    if not any(o.get("id") == "formAddIncidentPerson" for o in s.get("overlays") or []):
        s.setdefault("overlays", []).append({
            "id": "formAddIncidentPerson", "component": "modal", "trigger": "Add a person involved",
            "body": ("**A person involved in the incident** (" + prov("CHG-SPF-013") + "): name, role "
                     "(guest, staff, contractor, other) and contact, with an optional guest lookup "
                     "(`searchGuests`) that fills them from the guest's record. Stored as a PII "
                     "subject; the consent rules apply, so contact details are asked only with the "
                     "purpose shown. Dismissing sends nothing; the screen behind is unchanged."),
            "confirm": {"label": "Add person", "operation": "addIncidentPerson"},
            "dismiss": {"label": "Cancel", "discards": ["name", "role", "contact", "subjectId"]},
            "provenance": prov("CHG-SPF-013")})
        h3 = True
    if h3:
        log.append("013 EMP-026: photos and a person involved bound")
        hit = True
    return hit


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", default="007,008,009,010,011,012,013")
    a = ap.parse_args()
    only = set(a.only.split(","))
    F = spf.ScreenFiles()
    S = F.screens
    flows: dict = {}
    log: list = []
    steps = {"007": (d007, ("GST-001", "WEB-001")), "008": (d008, ("KIT-007",)),
             "009": (d009, ("BO-056",)), "010": (d010, ("BO-078",)), "011": (d011, ("ANL-023",)),
             "012": (d012, ("POS-000", "GST-055", "GST-053", "GST-054")),
             "013": (d013, ("GST-031", "GST-032", "WEB-044", "GST-070", "EMP-026"))}
    for k, (fn, ids) in steps.items():
        if k not in only:
            continue
        hit = fn(S, flows, log) if fn is d010 else fn(S, log)
        if hit:
            F.dirty |= set(ids)
    print("\n".join(log) if log else "nothing to do")
    if a.apply and (F.dirty or flows):
        print("written: " + ", ".join(F.write() + [p.name for p in flows]))
        for p, t in flows.items():
            p.write_text(t, encoding="utf-8")
    elif F.dirty or flows:
        print("nothing written — pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
