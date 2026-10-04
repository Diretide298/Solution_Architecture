# Bindings to what the contracts agent answered in the ledger (part of the specs; helpers there).
# flake8: noqa

DONE = "added by the contracts agent, runs/fix-s12/LEDGER.md (CHG-FXC-011), 4 October 2026"

F("BO-1111", READ,
  apis_set={"listCreditLots": dict(purpose="Every wallet's credit lots at this venue (no walletId), filtered by "
                                           "expiringWithinDays (" + DONE + ")")},
  comp_drop=["Every credit expiry extension", "The selected credit expiry extension"],
  add_comps=[("contentBody", c("selectField", "Expiring within", None, "listCreditLots",
                               notes="Query expiringWithinDays: today, 7 or 30 days."))],
  comp_set={"The tranches behind a balance, with their expiry": dict(
      label="Credit lots", notes="Across the venue's wallets when no wallet is picked; selecting lots gives "
                                 "expireCreditLots its lots to expire, extend or forfeit.")},
  note="Credit lots are listed across the venue by expiry window (listCreditLots without walletId, "
       "expiringWithinDays), 4 October 2026; the pack-label tables left")

F("EMP-066", READ,
  apis_add=[A("listStockCountLines", "onLoad", "The pre-filled lines of the count being entered (countId): "
                                              + DONE, contract="inventory")],
  comp_set={"kind:cardList": dict(label="Lines to count", bindsTo="CountLine", operation="listStockCountLines",
                       notes="One card per line (item, counted); the expected quantity stays hidden while a blind "
                             "count is open. Each card's itemId is what enterCountLine sends.")},
  note="The count lines are read with listStockCountLines (" + DONE + ")")

F("DEV-002", READ,
  apis_add=[A("listDeveloperMembers", "onLoad", "The organisation's members: " + DONE, contract="public-api")],
  comp_set={"kind:dataTable": dict(label="Members", bindsTo="DeveloperMember", operation="listDeveloperMembers")},
  note="The members table reads listDeveloperMembers (" + DONE + ")")

F("BO-167", READ,
  comp_set={"Device bindings": dict(columns=cols("DeviceBindingSessionSecurityView", "user", "credential",
                                                 "appInstallation", "registrationDate", "lastActivation",
                                                 "lastKnownVenue", "deviceId"),
                                    notes="Each row carries its bindingId (DeviceBindingSessionSecurityView."
                                          "bindingId), which Release takes and the optional entry bindingId "
                                          "selects.")},
  note="Release acts on the row's bindingId (" + DONE + ")")

F("BO-097", READ,
  apis_add=[A("getResourceBooking", "onLoad", "The resource booking the check-out and check-in act on: status, "
                                             "conditionOut, conditionIn, depositAuthorisationId (" + DONE + ")",
              contract="resources")],
  add_comps=[("contentBody", c("detailPanel", "Resource booking", "ResourceBooking", "getResourceBooking",
                               notes="status, condition out and in, deposit authorisation."))],
  note="The writes act on the resource booking, read with getResourceBooking (" + DONE + "); the rental "
       "booking panel stays for its timeline")

F("POS-024", READ,
  apis_add=[A("listTableCombinations", "onLoad", "The combinations already declared, read before the whole-set "
                                                "save (" + DONE + ")", contract="fnb")],
  comp_set={"Combinations": dict(bindsTo="TableCombination", operation="listTableCombinations",
                                 notes="Saved with setTableCombinations as the whole set read here.")},
  note="The combinations are read with listTableCombinations before the whole-set PUT (" + DONE + ")")

F("KIT-002", READ,
  comp_set={"Notify server": dict(notes="Takes the selected ticket's visitId (KitchenTicket.visitId); hidden for "
                                        "a counter or delivery ticket, which has none.")},
  note="Notify server reads the ticket's own visitId (" + DONE + ")")

F("POS-031", READ,
  comp_set={"Groups due today": dict(notes="Each row carries groupBookingId; selecting one loads getGroupBooking "
                                           "and gives recordGroupCheckIn its id.")},
  note="The group rows carry groupBookingId (" + DONE + ")")

F("POS-029", READ, force=True,
  apis_add=[A("recordOrderHandover", "onAction", "Hand the order over: served, collected or delivered "
                                                "(contracts, ledger: these are the stages after ready)")],
  comp_set={"Advance stage": dict(notes="Received: acceptFnbOrder. Preparing: setKitchenTicketStatus ready. "
                                        "Ready: recordOrderHandover (served, collected or delivered).")},
  add_comps=[("contentBody", c("secondaryButton", "Hand over", op="recordOrderHandover"))],
  overlays_add=[dict(id="formRecordOrderHandover", component="modal", trigger="Hand over",
                     body="**Collects what `recordOrderHandover` sends before it is called.** Required: "
                          "`outcome` (served, collected or delivered), `recordedAt` (now). Dismissing sends nothing.",
                     confirm=dict(label="Hand over", operation="recordOrderHandover"),
                     dismiss=dict(label="Cancel", discards=["outcome"]),
                     provenance="contract fnb.yaml recordOrderHandover (4 October 2026, CHG-FXS-003)")],
  note="After ready the order is handed over with recordOrderHandover (contracts: FnbOrderStatus served, "
       "collected, delivered; no dispatched stage)")

F("GST-074", READ,
  note="addCartLine's variantId is the placed spot's PlacedResource.variantId (it exists in venue-map; the "
       "pull did not carry it), 4 October 2026")

F("GST-078", READ,
  note="Choose sends the PassOffer's variants[] variantId for the passenger type (" + DONE + ")")

for _sid in ("WEB-002", "WEB-004"):
    F(_sid, READ,
      note="A product's event is Product.eventId (" + DONE + "): the date filter and the product page read "
           "listPerformances for it")

for _sid in ("WEB-039", "GST-021"):
    F(_sid, READ,
      apis_add=[A("listBookableVenueMaps", "onLoad", "The venue's published map (query venueId), whose mapId "
                                                    "getVenueMap and getVenueMapGraph take")],
      entry=[P("mapId", "deepLink", True, "Otherwise the venue's published map from listBookableVenueMaps."),
             P("venueId", "session")],
      add_comps=[("contentBody", c("selectField", "Map", "BookableVenueMaps.maps", "listBookableVenueMaps",
                                   notes="Picked by itself when the venue has one published map."))],
      note="The map comes from listBookableVenueMaps?venueId (contracts, ledger: the venue -> map read exists), "
           "so a normal visit has a map to load")
