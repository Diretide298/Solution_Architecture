# Guest app and guest web screens (part of s12-screens-4-october-specs.py; helpers there).
# flake8: noqa

F("GST-011", READ,
  apis_add=[A("listPaymentTokens", "onLoad", "The guest's saved cards: the auto top-up card and a stored-"
                                            "card exit settlement pick one (paymentTokenId)")],
  entry=[P("subjectId", "session"), P("cardCode", "deepLink", True),
         P("walletId", "navigation", True, "Read from the wallet itself (Wallet.id, agreed field) when "
                                           "not carried.")],
  add_comps=[
      ("contextPanel", c("toggle", "Auto top-up", "WalletAutoReloadSetting.enabled", "setWalletAutoReloadSetting")),
      ("contextPanel", c("numberField", "When the balance falls below", "WalletAutoReloadSetting.thresholdAmount",
                         "setWalletAutoReloadSetting")),
      ("contextPanel", c("numberField", "Top up by", "WalletAutoReloadSetting.reloadAmount", "setWalletAutoReloadSetting")),
      ("contextPanel", c("selectField", "Card", "WalletAutoReloadSetting.paymentTokenId", "listPaymentTokens",
                         cols("PaymentToken", "maskedIdentifier", "expiresAt", "isDefault"),
                         notes="Options from listPaymentTokens; none saved shows Add a card (GST-071).")),
  ],
  note="The guest's saved cards are read with listPaymentTokens (4 October 2026) so the auto top-up and "
       "a stored-card exit settlement have a paymentTokenId to send; the walletId is the wallet's own "
       "id (Wallet.id, agreed with contracts in the ledger)")


def _parking(sid):
    F(sid, READ,
      comp_set={"Car parks": dict(columns=cols("ParkingFacility", "name", "capacity", "productVariantId"),
                                  notes="Choosing one puts its parking product (productVariantId, agreed "
                                        "field) in the basket with addCartLine.")},
      note="The car park's parking product is ParkingFacility.productVariantId (agreed with contracts in "
           "the ledger 4 October 2026): Add parking to my cart sends it as addCartLine's variantId")


_parking("GST-027")
_parking("WEB-041")

F("GST-045", READ,
  apis_add=[A("listMyEntitlements", "onLoad", "The guest's own tickets to choose from; each carries its "
                                             "orderId, which transferOrderTickets takes in its path")],
  entry=[P("orderId", "deepLink", True, "From Home there is none: the guest picks tickets from "
                                        "listMyEntitlements and the order is the tickets' orderId.")],
  comp_set={"Tickets to send": dict(bindsTo="Entitlement", operation="listMyEntitlements",
                                    columns=cols("Entitlement", "productId", "validFrom", "status"),
                                    notes="Valid, unused tickets of one order at a time (a transfer is per "
                                          "order); opened from a link, the link's order is preselected.")},
  note="The tickets to send are read with listMyEntitlements (4 October 2026); orderId is optional "
       "and comes from the chosen tickets' orderId when the screen opens from Home")

F("GST-058", READ,
  apis_drop=["getAvailability", "listProducts"],
  apis_add=[A("listBookableVenueMaps", "onLoad", "The venue's published map with bookable cabanas (kind "
                                                 "cabana)"),
            A("getMapResourceAvailability", "onLoad", "Every cabana's status for the chosen date, by zone")],
  regions=[
      ("contentBody", [
          c("selectField", "Map", "BookableVenueMaps.maps", "listBookableVenueMaps",
            notes="The venue's published map with cabanas (query kind cabana); picked by itself when there "
                  "is one, shown when there are several."),
          c("datePicker", "Date", "MapResourceAvailability.from", "getMapResourceAvailability",
            notes="from and to are the chosen day; today by default."),
          c("selectField", "Area", "MapResourceAvailability.resources", "getMapResourceAvailability",
            notes="The zones the spots are in; All by default."),
          c("cardList", "Cabanas", "MapResourceAvailability.resources", "getMapResourceAvailability",
            notes="Each cabana with its label, zone, capacity and status (free, held, booked); a free one "
                  "opens the map booking (GST-074) on it."),
      ]),
  ],
  note="Availability is the map's (4 October 2026): listBookableVenueMaps gives the mapId and "
       "getMapResourceAvailability every cabana's status for the day, as GST-074 books them; getAvailability "
       "needs a performance, event or capacity id no cabana product has, and left the screen")
carry("GST-058", "GST-074", ["mapId"], trigger="Book a free cabana")


def _gst058_edge(S, pk):
    """GST-058 no longer holds a product (it reads the map), so its edge to GST-074 stops carrying one."""
    s = S.get("GST-058")
    out = []
    for t in ((s or {}).get("navigation") or {}).get("transitions") or []:
        if isinstance(t, dict) and str(t.get("to")).startswith("GST-074") and "productId" in (t.get("carries") or []):
            t["carries"] = [x for x in t["carries"] if x != "productId"]
            out.append(("GST-058", "CHG-FXS-003 GST-058: edge to GST-074 no longer carries productId"))
    return out


EDGES.append(_gst058_edge)

F("GST-069", READ,
  apis_add=[A("listMyEntitlements", "onLoad", "The passes a face can be registered on (entitlementId), "
                                             "each with its facePassEnrolmentId")],
  entry=[P("subjectId", "session"),
         P("enrolmentId", "deepLink", True, "Otherwise the selected pass's Entitlement.facePassEnrolmentId.")],
  add_comps=[
      ("contentBody", c("cardList", "Passes", "Entitlement", "listMyEntitlements",
                        cols("Entitlement", "productId", "validTo", "facePassEnrolmentId", "status"),
                        notes="Passes of the selected person (self or a linked child). A pass with a "
                              "facePassEnrolmentId shows its enrolment (getFacePassEnrolment); one without "
                              "offers Enrol.")),
      ("contentBody", c("scanTarget", "Face capture", None, "enrolFacePass",
                        notes="Captured by the facial-reader vendor's SDK behind a FaceCapture interface; "
                              "the SDK returns the template the body sends (write-only). Until the client "
                              "names the vendor (ADR-0063, a client question), the app builds against a "
                              "stub that returns a fixed test template.")),
  ],
  note="The passes come from listMyEntitlements (4 October 2026): entitlementId for enrolFacePass, "
       "facePassEnrolmentId for getFacePassEnrolment. The template comes from the facial-reader vendor's "
       "SDK, a client choice still open (ADR-0063); the build uses a stub until it is named")

F("GST-071", READ,
  add_comps=[
      ("contentBody", c("detailPanel", "My wallet", "Wallet", "getWallet",
                        cols("Wallet", "balance", "status"))),
      ("contentBody", c("textField", "Card details", None, "getPublishedTenantConfig",
                        notes="The tokenising provider's secure card fields, for the provider the "
                              "published config names (paymentTokenisation); the card never reaches "
                              "the platform.")),
      ("contentBody", c("consentBlock", "Save this card for future payments", "ConsentPurposeConfig",
                        "listConsentPurposes",
                        notes="The purpose for stored cards; its id is storePaymentToken's consentPurposeId.")),
  ],
  apis_add=[A("listConsentPurposes", "onLoad", "The consent purpose a saved card is stored under "
                                               "(consentPurposeId: storing a card for future payments)"),
            A("getPublishedTenantConfig", "onLoad", "The provider the app tokenises cards with "
                                                    "(paymentTokenisation.providerId, agreed field)"),
            A("getWallet", "onLoad", "The guest's wallet and its id, for a balance transfer")],
  note="storePaymentToken's providerId comes from the published tenant config (paymentTokenisation, "
       "agreed with contracts in the ledger) and its consentPurposeId from listConsentPurposes; the "
       "transfer's walletId is the guest's wallet id from getWallet (Wallet.id, agreed). Bound 4 October "
       "2026")
