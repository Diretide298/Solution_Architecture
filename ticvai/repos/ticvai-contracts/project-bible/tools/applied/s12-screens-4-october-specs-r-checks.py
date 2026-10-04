# What the screen checks asked after the first pass (part of the specs; helpers there).
# flake8: noqa

F("GST-028", READ, force=True,
  entry=[P("orderId", "previousScreen"), P("subjectId", "session"),
         P("entitlementId", "navigation", True, "The parking entitlement of this order, from listMyEntitlements "
                                                "(the one whose orderId is the order's).")],
  add_comps=[("contentBody", c("cardList", "Parking passes", "Entitlement", "listMyEntitlements",
                               cols("Entitlement", "orderId", "validFrom", "status"),
                               notes="Filtered to this order; the parking one gives entitlementId."))],
  note="entitlementId comes from the order's parking entitlement in listMyEntitlements (check-screens)")

F("POS-023", READ, force=True,
  overlays_drop=["formCreateRetailSale"],
  comp_set={"Scan or search": dict(bindsTo=None, operation="lookupMerchandise")},
  note="The createRetailSale form left with the operation; the search scans or looks up by barcode")


def _pos023_edge(S, pk):
    s = S.get("POS-023")
    out = []
    for t in ((s or {}).get("navigation") or {}).get("transitions") or []:
        if isinstance(t, dict) and str(t.get("to")).startswith("POS-002") and "orderId" in (t.get("carries") or []):
            t["carries"] = [x for x in t["carries"] if x != "orderId"]
            if not t["carries"]:
                t.pop("carries")
            out.append(("POS-023", "CHG-FXS-003 POS-023: edge to POS-002 no longer carries orderId (no sale is made here)"))
    return out


EDGES.append(_pos023_edge)

F("POS-029", READ, force=True,
  entry=[P("workstationId", "session"), P("outletId", "session"),
         P("orderId", "navigation", True, "The order selected on the board, for Accept and Hand over."),
         P("ticketId", "navigation", True, "The selected order's kitchen ticket (KitchenTicket for the "
                                           "order), for Mark ready.")],
  add_comps=[("contentBody", c("selectField", "Ticket status", "KitchenTicket.status", "setKitchenTicketStatus",
                               notes="ready by default when Mark ready is pressed."))],
  note="Accept and Mark ready collect their bodies (estimated ready time; ticket status) and Mark ready acts "
       "on the selected order's ticketId (check-screens, check-screen-wiring)")

F("POS-026", READ, force=True,
  comp_drop=["Send the receipt by", "Reissue reason"],
  overlays_add=[
      dict(id="formReprintReceipt", component="modal", trigger="Reprint receipt",
           body="**Collects what `reprintReceipt` sends before it is called.** Required: `delivery` (print, "
                "email, SMS or WhatsApp; print by default). Optional: `destination` (asked for anything but "
                "print). Dismissing sends nothing.",
           confirm=dict(label="Reprint receipt", operation="reprintReceipt"),
           dismiss=dict(label="Cancel", discards=["delivery", "destination"]),
           provenance="contract retail.yaml POST /retail-sales/{saleId}/reprint (4 October 2026, CHG-FXS-003)"),
      dict(id="formReissueEntitlement", component="modal", trigger="Reissue entitlement",
           body="**Collects what `reissueEntitlement` sends before it is called.** Required: `reason` (venue "
                "closure, weather, goodwill, system error, medical issue, bereavement). Optional: `validFrom`, "
                "`note`. Dismissing sends nothing.",
           confirm=dict(label="Reissue entitlement", operation="reissueEntitlement"),
           dismiss=dict(label="Cancel", discards=["reason", "validFrom", "note"]),
           provenance="contract orders.yaml POST /entitlements/{entitlementId}/reissue (4 October 2026, CHG-FXS-003)")],
  note="Reprint and reissue collect their bodies in their own forms (delivery; reason)")

F("POS-027", READ, force=True,
  comp_set={"Name, phone, booking reference or scan a wristband": dict(bindsTo=None)},
  note="The search box is a query input (searchGuests search, identifyGuest token), not a bound field")


def _account(sid):
    F(sid, READ, force=True,
      add_comps=[("contentBody", c("textField", "Email for the account", "RegisterGuestRequest.identifier",
                                   "registerGuest", notes="The order's email, prefilled; channel email.")),
],
      note="Create an account collects the email and the code its two calls send")


_account("WEB-013")

F("BO-346", BIND, force=True,
  states=dict(emptyFirstRun="No design saved for this media template yet: the designer opens on the "
                            "defaults; Save design creates it."),
  note="First-run state names Save design, the screen's own write")

F("BO-669", DEF, force=True,
  add_comps=[("contentBody", c("detailPanel", "Validity as saved", "AccreditationValidity", "getAccreditationValidity",
                               cols("AccreditationValidity", "validityKind", "validityMonths", "onExpiry")))],
  note="The saved validity shows beside the form")

F("CMS-007", READ, force=True,
  add_comps=[("contentBody", c("secondaryButton", "Save block", op="updateContentBlock",
                               notes="Saves the selected block's content or its new position."))],
  note="Save block edits an existing block (updateContentBlock)")

F("WEB-017", READ, force=True,
  add_comps=[("contentBody", c("selectField", "Programme", "LoyaltyProgramme.id", "listLoyaltyProgrammes",
                               notes="Shown only when the venue runs more than one; the first active one "
                                     "otherwise."))],
  note="The loyalty programme is picked from listLoyaltyProgrammes when there are several")

F("GST-010", READ,
  apis_add=[A("registerGuest", "onAction", "Create an account for the order's email: sends a code"),
            A("verifyGuestEmail", "onAction", "Prove the code; then linkGuestCheckout moves the order to the "
                                              "account")],
  comp_set={"Set a password": dict(label="Create an account",
                                   notes="Guest accounts are passwordless: registerGuest with the order's "
                                         "email, verifyGuestEmail with the code, then linkGuestCheckout.")},
  add_comps=[("contentBody", c("secondaryButton", "Send me a code", op="registerGuest")),
             ("contentBody", c("secondaryButton", "Verify the code", op="verifyGuestEmail"))],
  note="'Set a password' is 'Create an account' (4 October 2026), the same as its web twin WEB-013: "
       "registerGuest and verifyGuestEmail make and prove the account, then linkGuestCheckout")
_account("GST-010")


def _signed_in(S, pk):
    """Screens that now load the guest's own tickets are behind sign-in: they say so (subjectId from session)."""
    out = []
    for sid in ("GST-028", "GST-045", "GST-062"):
        s = S.get(sid)
        if not s:
            continue
        params = s.setdefault("entryState", {}).setdefault("params", [])
        if not any(isinstance(p, dict) and p.get("name") == "subjectId" for p in params):
            params.append({"name": "subjectId", "from": "session",
                           "notes": "The signed-in guest: the screen reads their own tickets (4 October 2026)."})
            out.append((sid, f"CHG-FXS-003 {sid}: behind sign-in (subjectId from session)"))
    return out


EDGES.append(_signed_in)


def _verify_form(sid):
    return dict(id="formVerifyGuestEmail", component="modal", trigger="Verify the code",
                body="**Collects what `verifyGuestEmail` sends before it is called.** Required: `mode` (code), "
                     "the six-digit `code` sent to the order's email. Dismissing sends nothing.",
                confirm=dict(label="Verify the code", operation="verifyGuestEmail"),
                dismiss=dict(label="Cancel", discards=["code"]),
                provenance=f"contract identity.yaml POST /auth/guest/verify-email (4 October 2026, CHG-FXS-003)")


for _sid in ("WEB-013", "GST-010"):
    F(_sid, READ, force=True, comp_drop=["Code"], overlays_add=[_verify_form(_sid)],
      note="The code is collected by the verify form (formVerifyGuestEmail)")

F("POS-029", READ, force=True, comp_drop=["Ready at"],
  overlays_add=[dict(id="formAcceptFnbOrder", component="modal", trigger="Accept order",
                     body="**Collects what `acceptFnbOrder` sends before it is called.** Required: `recordedAt` "
                          "(now, set by the till). Optional: `estimatedReadyAt` (now plus the outlet's target "
                          "prep time by default), `stationId`. Dismissing sends nothing.",
                     confirm=dict(label="Accept order", operation="acceptFnbOrder"),
                     dismiss=dict(label="Cancel", discards=["estimatedReadyAt", "stationId"]),
                     provenance="contract fnb.yaml acceptFnbOrder (4 October 2026, CHG-FXS-003)")],
  note="Accept collects its body in its own form (formAcceptFnbOrder)")

F("GST-071", READ, force=True, comp_drop=["Card details"],
  comp_set={"Save this card for future payments": dict(bindsTo="ConsentPurposeConfig.purpose")},
  add_comps=[("contentBody", c("detailPanel", "Card provider", "PublishedTenantConfig", "getPublishedTenantConfig",
                               ["PublishedTenantConfig.paymentTokenisation"],
                               notes="The tokenising provider; its secure card fields take the card, which "
                                     "never reaches the platform."))],
  note="The card is entered in the provider's secure fields, named by the published config")

F("GST-069", READ, force=True, comp_drop=["Face capture"],
  note="The face is captured inside the enrol form (formEnrolFacePass) by the vendor SDK")


def _gst069_capture(S, pk):
    s = S.get("GST-069")
    out = []
    for o in (s or {}).get("overlays") or []:
        if o.get("id") == "formEnrolFacePass" and "FaceCapture interface" not in str(o.get("body") or ""):
            o["body"] = (str(o.get("body") or "").rstrip() + " The face is captured by the facial-reader vendor's "
                         "SDK behind a FaceCapture interface, which returns the write-only `template`; until "
                         "the client names the vendor (ADR-0063) the build uses a stub returning a fixed test "
                         "template (CHG-FXS-003).")
            out.append(("GST-069", "CHG-FXS-003 GST-069: enrol form names the capture SDK"))
    return out


EDGES.append(_gst069_capture)
