# Venue, seating and settings screens (part of s12-screens-4-october-specs.py; helpers there).
# flake8: noqa

VS_PUT = ("**setVenueSettings replaces the whole settings row** (PUT; an omitted property returns to "
          "its default). The save sends the VenueSettings that getVenueSettings returned, with only "
          "this screen's group changed; nothing else is reset (CHG-FXS-003).")


def _venue_settings_rule(S, pk):
    """Every screen that saves a group of VenueSettings reads the row and sends it back whole."""
    out = []
    for sid, s in S.items():
        ops = {a["operationId"] for a in s.get("apis") or []}
        if "setVenueSettings" not in ops:
            continue
        hit = []
        if "getVenueSettings" not in ops:   # BO-600: a wave-3 screen outside Sprints 1-2 that still
            continue                         # needs a person; it gets its read when it is defined
        for o in s.get("overlays") or []:
            if (o.get("confirm") or {}).get("operation") == "setVenueSettings" and \
                    "replaces the whole settings row" not in str(o.get("body") or ""):
                o["body"] = str(o.get("body") or "").rstrip() + " " + VS_PUT
                hit.append(f"overlay {o.get('id')} sends the row whole")
        if "replaces the whole settings row" not in str(s.get("notes") or ""):
            s["notes"] = (str(s.get("notes") or "").rstrip() + "\n\n" + VS_PUT).strip()
            hit.append("note")
        if hit:
            out.append((sid, f"{READ} {sid}: " + "; ".join(hit)))
    return out


EDGES.append(_venue_settings_rule)

F("BO-1045", DEF, pattern="listDetail", template="split", drop_gaps=("person",),
  patternReason="Seat categories listed with the selected one's price bands edited beside it "
                "(defined 4 October 2026 from SeatCategory and SeatPriceBand, CHG-FXS-001).",
  regions=[
      ("contentBody", [
          c("dataTable", "Seat categories", "SeatCategory", "listSeatCategories",
            cols("SeatCategory", "rank", "code", "name", "displayColour", "seatCount"),
            notes="The venue in session (query venueId), in rank order."),
          c("primaryButton", "New seat category", notes="Opens an empty form in the side panel."),
      ]),
      ("contextPanel", [
          c("textField", "Code", "SeatCategory.code", "createSeatCategory", notes="Set at creation."),
          c("textField", "Name", "SeatCategory.name", "createSeatCategory"),
          c("textField", "Colour", "SeatCategory.displayColour", "createSeatCategory",
            notes="Hex colour shown on the seat map; keeps 3:1 contrast with the map background."),
          c("numberField", "Rank", "SeatCategory.rank", "createSeatCategory"),
          c("dataTable", "Price bands", "SeatCategory.priceBands", "listSeatCategories",
            cols("SeatPriceBand", "code", "displayLabel", "amount", "channel", "effectiveFrom", "effectiveTo")),
          c("textField", "Band code", "SeatPriceBand.code", "updateSeatCategory"),
          c("textField", "Band label", "SeatPriceBand.displayLabel", "updateSeatCategory"),
          c("numberField", "Band price", "SeatPriceBand.amount", "updateSeatCategory",
            notes="In the venue's currency (Money; the currency comes from the region)."),
          c("selectField", "Band channel", "SeatPriceBand.channel", "updateSeatCategory",
            notes="Empty means every channel."),
          c("datePicker", "Effective from", "SeatPriceBand.effectiveFrom", "updateSeatCategory"),
          c("datePicker", "Effective to", "SeatPriceBand.effectiveTo", "updateSeatCategory"),
          c("secondaryButton", "Add band", notes="Adds a row to the category's priceBands."),
          c("primaryButton", "Create seat category", op="createSeatCategory"),
          c("primaryButton", "Save changes", op="updateSeatCategory",
            notes="Sends name, colour, rank and the whole priceBands list."),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No seat categories yet. Carries New seat category."),
  note="Defined 4 October 2026 from SeatCategory and SeatPriceBand (R275 d): categories in rank order, "
       "each with its price bands by channel and effective period. Mapping bands to sections, rows or "
       "seats is the seat map editor's (the remaining gap)")

F("BO-1063", DEF, pattern="configEditor", template="form", drop_gaps=("person",),
  patternReason="One venue's seating defaults in one form (defined 4 October 2026 from "
                "VenueSettings.seating and the cart hold settings, CHG-FXS-001).",
  set=dict(purpose="Set this venue's seating and hold defaults without a separate seat system: how "
                   "long a cart and a seat hold last, how often they extend, and how many seats a "
                   "guest may book in one order."),
  regions=[
      ("contentBody", [
          c("numberField", "Cart hold (seconds)", "VenueSettings.cartLeaseSeconds", "setVenueSettings"),
          c("numberField", "Cart extension (minutes)", "VenueSettings.cartHoldExtensionMinutes",
            "setVenueSettings"),
          c("numberField", "Cart extensions allowed", "VenueSettings.cartMaxExtensions", "setVenueSettings"),
          c("numberField", "Seat hold extension (seconds)", "VenueSettings.seating.seatHoldExtensionSeconds",
            "setVenueSettings"),
          c("numberField", "Seat hold extensions allowed", "VenueSettings.seating.seatHoldMaxExtensions",
            "setVenueSettings"),
          c("numberField", "Seats per guest booking", "VenueSettings.seating.maxSeatsPerGuestOrder",
            "setVenueSettings"),
          c("primaryButton", "Save venue settings", op="setVenueSettings"),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
  ],
  states=dict(loading="The form with the venue's saved values.",
              error="Could not load. Names the read that failed; nothing is editable until it loads.",
              emptyFirstRun="Never saved: the form shows the defaults getVenueSettings returns."),
  note="Defined 4 October 2026 from VenueSettings (cart lease and extensions, seat hold extensions, "
       "seats per order). Default map, naming, approvals and publishing policy are not venue settings "
       "in the contract and left the purpose")

F("BO-674", DEF, pattern="commandCentre", drop_gaps=("~operations return no schema",),
  patternReason="The accreditation communications section's home: links to its screens, with no "
                "dashboard until a read of sends and delivery outcomes exists (4 October 2026, "
                "CHG-FXS-001).",
  set=dict(purpose="The home of accreditation communications: open the notification rules, templates, "
                   "schedules and delivery screens of this section."),
  regions=[
      ("contentBody", [
          c("cardList", "Accreditation communications",
            notes="One card per screen this hub opens (navigation.exitTo), each with its name and "
                  "purpose; no figures until the delivery read exists (contract gap CHG-WIR-004)."),
      ]),
  ],
  states=dict(loading="The cards render at once; nothing is fetched.",
              error="Not used: the hub fetches nothing."),
  note="Defined 4 October 2026 as the section's navigation hub: the five dashboard elements had no "
       "read (contract gap CHG-WIR-004, still open), so the chart left the screen and it links to "
       "BO-675 to BO-683")
