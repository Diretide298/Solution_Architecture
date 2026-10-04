# Till, kitchen and web checkout screens (part of s12-screens-4-october-specs.py; helpers there).
# flake8: noqa

F("POS-026", READ,
  apis_add=[A("getOrder", "onLoad", "The order as it was sold, with each line's entitlementIds")],
  comp_set={"The order, as it was sold": dict(operation="getOrder",
                                              columns=cols("Order", "orderNumber", "status", "grossAmount", "createdAt")),
            "What was issued against it": dict(bindsTo="Order.lines", operation="getOrder",
                                               columns=["OrderLine.variantId", "OrderLine.holderName", "OrderLine.quantity",
                                                        "OrderLine.entitlementIds"],
                                               notes="Each line with the entitlements issued for it; "
                                                     "choosing one gives Reissue its entitlementId."),
            "Reprint receipt": dict(operation="reprintReceipt"),
            "Reissue entitlement": dict(operation="reissueEntitlement")},
  add_comps=[
      ("contentBody", c("selectField", "Send the receipt by", None, "reprintReceipt",
                        notes="Body delivery: print (default), email, SMS or WhatsApp; destination asked for "
                              "anything but print.")),
      ("contentBody", c("selectField", "Reissue reason", None, "reissueEntitlement",
                        notes="Body reason (required): venue closure, weather, goodwill, system error, "
                              "medical issue, bereavement.")),
  ],
  note="The order and what was issued against it are read with getOrder (4 October 2026): Order.lines[] "
       "carries each line's entitlementIds, which Reissue entitlement acts on")

F("POS-027", READ, drop_gaps=(),
  comp_set={"Name, phone, booking reference or scan a wristband": dict(
                bindsTo="GuestProfile", operation="searchGuests",
                notes="Typed text searches searchGuests (query search); a scanned wristband, card or "
                      "QR goes to identifyGuest, which answers with the guest and their live "
                      "entitlements in one call."),
            "Matching guests": dict(operation="searchGuests"),
            "Wallet, passes and open reservations": dict(bindsTo="GuestIdentification", operation="identifyGuest",
                                                         columns=cols("GuestIdentification", "subjectId",
                                                                      "entitlements", "matchedOn")),
            "Attach to sale": dict(notes="Returns to the sale (POS-002) carrying the guest's subjectId; "
                                         "the order is then created with that subjectId. No call of its "
                                         "own: the sale carries the guest.")},
  note="Attach to sale is the edge to POS-002 carrying subjectId (4 October 2026): the sale screen "
       "takes subjectId and the order it creates carries it; search and scan are bound to searchGuests "
       "and identifyGuest")
carry("POS-027", "POS-002", ["subjectId"], trigger="Attach to sale")

F("WEB-011", READ,
  comp_set={"Ticket holder details": dict(notes="One holder name per cart line that needs one; handed to "
                                                "WEB-012, which sends them as checkoutCart attendees[] "
                                                "(lineId, holderName)."),
            "Continue to payment": dict(notes="Records the consent answers (recordConsentAnswers), then "
                                              "opens WEB-012 with the holder names and the ticked opt-ins; "
                                              "nothing else is sent here."),
            "Send me offers and news": dict(notes="Unticked by default; the ticked purposes go to WEB-012 "
                                                  "and into checkoutCart marketingConsents (DEC-275).")},
  note="The holder details are written by checkoutCart on WEB-012 (attendees), which turns the cart into "
       "the order (4 October 2026): this step collects them and hands them over, because a verified or "
       "signed-in guest whose cart needs no forms skips this step (W1) and WEB-012 must make the order "
       "either way. recordConsentAnswers' answers are typed in the contract (questionId, "
       "questionVersion, answer, cartLineId, personIndex); the pull cut them (ledger)")

F("WEB-012", READ,
  apis_drop=["createOrder"],
  apis_add=[A("checkoutCart", "onAction",
              "Pay now, first step: turn the session's cart into the order pending payment, with the "
              "holder names (attendees) and opt-ins (marketingConsents) from WEB-011 when it ran")],
  entry=[P("cartId", "session"),
         P("orderId", "deepLink", True, "A link to an order already pending payment opens it; otherwise "
                                        "checkoutCart makes the order from the cart."),
         P("paymentId", "navigation", True), P("venueId", "session")],
  entry_set={"preloaded": ["the holder names and marketing opt-ins typed on WEB-011, when it ran"]},
  comp_set={"Pay now": dict(notes="checkoutCart (once; its idempotency key is the cart's), then "
                                  "createPayment against the order it returns; an unknown payment outcome "
                                  "has the order to attach to."),
            "Terms and conditions": dict(operation=None,
                                         notes="Pay now is enabled only when ticked; the version shown is "
                                               "the one in force (listPublishedPolicies)."),
            "Send me offers and news": dict(operation="checkoutCart",
                                            notes="Unticked by default; sent as checkoutCart "
                                                  "marketingConsents. Prefilled from WEB-011 when it ran.")},
  note="createOrder left 4 October 2026: the order is made from the cart by checkoutCart (the cart's "
       "lines, holder names and opt-ins), then paid with createPayment; F01 step 7 and F02 step 5 say "
       "the same")


F("KIT-010", READ,
  apis_add=[A("listDashboards", "onLoad", "The venue's kitchen dashboard (module fnb, shared): its id "
                                         "is what getDashboard reads")],
  entry=[P("venueId", "session"), P("stationId", "session"),
         P("dashboardId", "navigation", True, "Otherwise the first shared fnb dashboard listDashboards "
                                               "returns (the kitchen's).")],
  comp_drop=[None],
  add_comps=[("contentBody", c("selectField", "Dashboard", "Dashboard.id", "listDashboards",
                               cols("Dashboard", "name", "isShared"),
                               notes="Query module fnb; the kitchen's shared dashboard by default."))],
  note="The dashboard is found with listDashboards (module fnb) 4 October 2026, so the screen no longer "
       "needs a dashboardId from KIT-002 (SPF-2's station-dashboard read); its tiles are the dashboard's "
       "reports (tileData). The rail cards and the unbound tile left: the rail is KIT-002")
