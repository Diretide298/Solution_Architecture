# Blockers on "guess" tickets: till, kitchen and guest (part of the specs; helpers there).
# flake8: noqa

F("KIT-008", STALE,
  comp_drop=["Bump", None],
  note="Bump and the unbound rail cards left 4 October 2026: the exceptions screen saves no ticket status "
       "(CHG-WIR-008); bumping is the rail's (KIT-002, setKitchenTicketStatus)")

F("POS-021", READ,
  apis_add=[A("getOutlet", "onLoad", "The outlet's paymentTiming (pay first or send first, POS-021 "
                                     "decision), which decides whether Pay or Send to kitchen comes first")],
  entry=[P("workstationId", "session"), P("outletId", "session"), P("cartId", "session"),
         P("itemId", "deepLink", True)],
  add_comps=[("contentBody", c("detailPanel", "How this outlet takes payment", "Outlet", "getOutlet",
                               cols("Outlet", "name", "paymentTiming"),
                               notes="payFirst: Pay opens POS-005, then the order goes to the kitchen. "
                                     "sendFirst: Send to kitchen, payment at the end (POS-022)."))],
  note="Outlet.paymentTiming is read with getOutlet (4 October 2026); the Block A rule 'payment timing "
       "follows POS-021: pay first or send first, both configurations' decides which button leads")

F("POS-025", READ,
  apis_add=[A("listShifts", "onLoad", "This till's last closed shift (query workstationId, status closed), "
                                     "the one a supervisor may reopen")],
  comp_set={"Reopen shift": dict(notes="Shown only when the till has no open shift: reopens the till's last "
                                       "closed shift from listShifts, with the supervisor's PIN (F32).")},
  add_comps=[("contentBody", c("detailPanel", "Last closed shift", "Shift", "listShifts",
                               cols("Shift", "principalDisplayName", "status", "openedAt")))],
  note="Reopen acts on the till's last closed shift, read with listShifts (4 October 2026): the shift on "
       "screen is open or suspended, and reopenShift takes a closed one")

F("POS-007", READ,
  apis_add=[A("listShifts", "onLoad", "Shifts of the venue waiting for a supervisor (status "
                                     "pendingVariance) or a recount, on any till: F32's 'from whichever till "
                                     "they are at'")],
  add_comps=[("contentBody", c("dataTable", "Shifts waiting at any till", "Shift", "listShifts",
                               cols("Shift", "principalDisplayName", "status", "openedAt"),
                               perm="OVERSHORT_ACCEPT",
                               notes="Query status pendingVariance; selecting one gives accept, reject and "
                                     "close its shiftId, and getShiftCountLines its lines."))],
  note="A supervisor finds a shift waiting on another till with listShifts (status pendingVariance), "
       "bound 4 October 2026 (F32: accept or reject from whichever till they are at)")

F("POS-023", READ,
  apis_drop=["createRetailSale"],
  comp_drop=["Create retail sale"],
  note="createRetailSale left 4 October 2026: a merchandise sale at the till is a cart line (addCartLine), "
       "charged with everything else on POS-005 (one cart, one order, one receipt, 14 August)")

F("POS-029", READ,
  apis_add=[A("acceptFnbOrder", "onAction", "Received to preparing: the outlet takes the order"),
            A("setKitchenTicketStatus", "onAction", "Preparing to ready: advance the order's kitchen ticket")],
  comp_set={"Advance stage": dict(notes="Received: acceptFnbOrder. Preparing: setKitchenTicketStatus ready. "
                                        "Dispatch and delivered wait for their operation (asked of contracts, "
                                        "ledger).")},
  add_comps=[("contentBody", c("secondaryButton", "Accept order", op="acceptFnbOrder")),
             ("contentBody", c("secondaryButton", "Mark ready", op="setKitchenTicketStatus"))],
  note="Stage changes bound 4 October 2026: accept (acceptFnbOrder) and ready (setKitchenTicketStatus); "
       "dispatch and delivered are asked of contracts in the ledger")

F("WEB-013", READ,
  apis_add=[A("registerGuest", "onAction", "Create an account for the order's email: sends a code"),
            A("verifyGuestEmail", "onAction", "Prove the code; then linkGuestCheckout moves the order to the "
                                              "account")],
  comp_set={"Set a password": dict(label="Create an account",
                                   notes="Guest accounts are passwordless: registerGuest with the order's "
                                         "email, verifyGuestEmail with the code, then linkGuestCheckout.")},
  add_comps=[("contentBody", c("secondaryButton", "Send me a code", op="registerGuest")),
             ("contentBody", c("secondaryButton", "Verify the code", op="verifyGuestEmail"))],
  note="'Set a password' is 'Create an account' (4 October 2026): registerGuest and verifyGuestEmail "
       "make and prove the account (no password field exists), then linkGuestCheckout")

F("GST-028", READ,
  apis_add=[A("listMyEntitlements", "onLoad", "The guest's parking entitlement from this order"),
            A("getParkingEntitlement", "onLoad", "The plate, car park and pass of that entitlement")],
  add_comps=[("contentBody", c("detailPanel", "Your parking", "ParkingEntitlement", "getParkingEntitlement",
                               cols("ParkingEntitlement", "plateNumber", "plateCountry", "mediaCode"),
                               notes="The entitlement of this order (listMyEntitlements filtered by "
                                     "orderId)."))],
  note="The plate, car park and pass are read from the parking entitlement (listMyEntitlements, then "
       "getParkingEntitlement), bound 4 October 2026")

F("GST-062", READ,
  apis_add=[A("listMyEntitlements", "onLoad", "The guest's tickets; lookupShopAndDrop is called once per "
                                             "entitlementId to find the goods waiting")],
  comp_set={"Waiting for you": dict(bindsTo=None,
                                    notes="One lookupShopAndDrop per ticket the guest carries "
                                          "(listMyEntitlements), merged; a receipt number or drop reference "
                                          "can be typed as well.")},
  add_comps=[("contentBody", c("cardList", "My tickets", "Entitlement", "listMyEntitlements",
                               cols("Entitlement", "productId", "validTo")))],
  note="The guest's drops are found by their own tickets (listMyEntitlements, then lookupShopAndDrop per "
       "entitlementId), bound 4 October 2026")
