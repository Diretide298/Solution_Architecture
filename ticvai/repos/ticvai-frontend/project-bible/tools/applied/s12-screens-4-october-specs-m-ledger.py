# Requests to the screens agent in runs/fix-s12/LEDGER.md, answered here (part of the specs).
# flake8: noqa

F("BO-087", BIND,
  apis_add=[A("listApprovalMatrices", "onLoad", "The approval matrices (ADM-243's section, merged here on "
                                                "2 October): who approves what, up to which amount"),
            A("setApprovalMatrix", "onAction", "Set role authority and approval limits (ADM-243's section)")],
  add_comps=[
      ("contentBody", c("dataTable", "Approval limits", "ApprovalMatrix", "listApprovalMatrices",
                        cols("ApprovalMatrix", "kind", "scopeLevel", "version", "isActive"),
                        notes="ADM-243's section: one matrix per approval kind and scope.")),
      ("contentBody", c("dataTable", "Rules of the selected matrix", "ApprovalMatrix.rules", "listApprovalMatrices",
                        cols("ApprovalRule", "order", "minAmount", "maxAmount", "approverRoleIds", "mode",
                             "requiresMfa"))),
      ("actionBar", c("secondaryButton", "Save approval limits", op="setApprovalMatrix",
                      perm="APPROVAL_CONFIGURE")),
  ],
  overlays_add=[dict(id="formSetApprovalMatrix", component="modal", trigger="Save approval limits",
                     body="**Collects what `setApprovalMatrix` sends before it is called.** Required: `kind`, "
                          "`scopeLevel`, `rules` (each with `order`, `approverRoleIds`, `mode`; optional "
                          "amount band, risk score, levels, MFA). Optional: `isActive`. Dismissing sends nothing.",
                     confirm=dict(label="Save approval limits", operation="setApprovalMatrix"),
                     dismiss=dict(label="Cancel", discards=["kind", "scopeLevel", "rules", "isActive"]),
                     provenance="contract approvals.yaml PUT /approval-matrices (4 October 2026, CHG-FXS-002)")],
  note="ADM-243 (merged into BO-087 as a section on 2 October) brings its bindings: the approval matrices "
       "are read with listApprovalMatrices and saved with setApprovalMatrix (the plan builds them on "
       "APP-SETUP-BO-087; ledger, 4 October 2026)")


def _drawer_step(sid, step, comp, what):
    F(sid, STALE, drop_gaps=("~full-page navigation the 3 August workshop replaced",),
      set=dict(implementation={"app": "venue-pos", "route": f"/sell/sell-ticket-catalogue/{comp.lower()}",
                               "component": "apps/venue-pos/src/routes/sell/SellTicketCatalogueBoard.tsx",
                               "status": "notStarted", "sectionOf": "POS-002"}),
      note=f"Built as step {step} of the POS-002 sale drawer ({what}), not a page of its own: the plan's "
           "default of 4 October 2026, carried by the tickets (block-a-extra-tasks.json screenNotes), "
           "closing the 3 August question 'whether this survives as a screen' (Chinmay to confirm)")


_drawer_step("POS-003", "two", "TimedEntry", "date, session and ticket quantities")
_drawer_step("POS-004", "three", "SeatMap", "section, then seats")

F("KIT-005", BIND,
  comp_drop=["Bump"],
  add_comps=[
      ("contentBody", c("selectField", "Move from station", "KitchenStation.id", "listKitchenStations",
                        notes="moves[].fromStationId.")),
      ("contentBody", c("selectField", "Move to station", "KitchenStation.id", "listKitchenStations",
                        notes="moves[].toStationId.")),
      ("contentBody", c("multiSelect", "Menu categories to move", "StationRebalance.moves", "rebalanceStationLoad",
                        notes="moves[].categoryIds; one move per from/to pair.")),
      ("contentBody", c("datePicker", "Revert at", "StationRebalance.revertAt", "rebalanceStationLoad",
                        notes="The move undoes itself then; end of service by default.")),
      ("actionBar", c("primaryButton", "Move work", op="rebalanceStationLoad",
                      notes="Sends StationRebalance {moves, revertAt}; the rail re-routes at once.")),
  ],
  note="Move work bound 4 October 2026 to rebalanceStationLoad (StationRebalance: moves[] fromStationId, "
       "toStationId, categoryIds; revertAt), as the contract types it (ledger); Bump is the rail's (KIT-002)")

F("BO-230", STALE, drop_gaps=("~No operation switches a gate's direction live",),
  comp_set={"Every live gate mode": dict(columns=cols("LiveGateModeLaneControlView", "currentMode",
                                                      "targetMode", "pendingChangeId")),
            "Cancel gate mode change": dict(notes="Acts on the selected row's pendingChangeId (the "
                                                  "scheduled change cancelGateModeChange takes); hidden "
                                                  "when the row has none.")},
  note="Cancel acts on LiveGateModeLaneControlView.pendingChangeId (contracts, 4 October 2026); the "
       "stale gap about a live direction switch is closed (setAccessPointDirection is bound)")

F("BO-346", BIND, force=True,
  apis_drop=["listTicketTemplates", "createTicketTemplate", "updateTicketTemplate", "printTicketProof"],
  apis_set={"getPdfPrintablePos": dict(purpose="Load the design of the media template being edited "
                                               "(query templateId = access.media_template.id)")},
  comp_set={"Save design": dict(notes="templateId is the access media template the screen was opened "
                                      "for (BO-344's row, access.media_template.id).")},
  note="Template model reconciled 4 October 2026 (contracts, ledger): the design belongs to an access "
       "media template (access.media_template.id, the row BO-344 opens), read and saved with "
       "get/setPdfPrintablePos; the orders ticket-template operations (list, create, update, proof) are "
       "another model and left this screen")

F("POS-026", READ, force=True,
  apis_add=[A("listTaxInvoices", "onAction", "The order's simplified tax invoice when the entry carries no "
                                            "invoiceId (query orderId)")],
  add_comps=[("contentBody", c("dataTable", "Tax invoices", "FinTaxInvoice", "listTaxInvoices",
                               notes="Query orderId; opening one shows it (getTaxInvoice) and offers the PDF."))],
  note="The order's tax invoice is found with listTaxInvoices?orderId when no invoiceId is carried "
       "(contracts, ledger, 4 October 2026)")
