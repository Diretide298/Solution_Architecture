# Membership, events, ticket design and resources (part of s12-screens-4-october-specs.py).
# flake8: noqa

F("BO-293", BIND, pattern="configEditor", template="split",
  apis_add=[A("getMembershipProductValidation", "onLoad",
              "The product version's validation checks, issues, impact, publication targets and "
              "approval stage, read by membershipCode and version: " + AGREED, contract="subscription")],
  entry=[P("membershipCode", "BO-284"), P("version", "BO-284"),
         P("challengeId", "navigation", True)],
  regions=[
      ("contentBody", [
          c("detailPanel", "Version", "MembershipProductValidationApprovalPublicationVersioView",
            "getMembershipProductValidation",
            cols("MembershipProductValidationApprovalPublicationVersioView", "membershipCode", "version",
                 "approvalStage", "effectiveFrom", "migrationPolicy")),
          c("dataTable", "Validation checks", "MembershipProductValidationApprovalPublicationVersioView.validationChecks",
            "getMembershipProductValidation"),
          c("dataTable", "Issues", "MembershipProductValidationApprovalPublicationVersioView.validationIssues",
            "getMembershipProductValidation"),
          c("dataTable", "Publication targets", "MembershipProductValidationApprovalPublicationVersioView.publicationTargets",
            "getMembershipProductValidation",
            notes="B2C, POS, mobile app, call centre, B2B, access control, ticketing and other dependent "
                  "services, each with its state (the pack's eight, read, not chosen)."),
          c("detailPanel", "Impact", "MembershipProductValidationApprovalPublicationVersioView",
            "getMembershipProductValidation",
            cols("MembershipProductValidationApprovalPublicationVersioView", "activeMembersAffected",
                 "futureRenewals", "entitlementsAffected", "channels")),
      ]),
      ("contextPanel", [
          c("selectField", "Action", "MembershipProductValidationApprovalPublicationVersioInput.action",
            "approveMembershipProductValidation",
            notes="Only the actions the approval stage allows next are offered."),
          c("datePicker", "Effective from", "MembershipProductValidationApprovalPublicationVersioInput.effectiveFrom",
            "approveMembershipProductValidation", notes="For schedule and publish."),
          c("selectField", "Existing members", "MembershipProductValidationApprovalPublicationVersioInput.migrationPolicy",
            "approveMembershipProductValidation",
            notes="Stay on the current version, move at next renewal, or move on the effective date."),
          c("textField", "Reason", "MembershipProductValidationApprovalPublicationVersioInput.reason",
            "approveMembershipProductValidation", notes="Required for reject and suspend."),
          c("primaryButton", "Submit", op="approveMembershipProductValidation",
            notes="Sends membershipCode and version from the entry, with the step-up token."),
          c("textField", "Authentication code", op="verifyMfaChallenge"),
          c("secondaryButton", "Email me a code instead", op="createMfaChallenge"),
      ]),
  ],
  states=dict(loading="The version's checks and impact load first.",
              error="Could not load. Names the read that failed; no action is offered until it loads.",
              emptyFirstRun="Not used: the screen opens on one product version."),
  note="Bound 4 October 2026: the screen reads the version it works on (getMembershipProductValidation, "
       "agreed in the ledger) by the membershipCode and version BO-284 carries; the eight publication "
       "targets are read, and the action, effective date, migration policy and reason are the inputs "
       "the PUT takes")
carry("BO-284", "BO-293", ["membershipCode", "version"], trigger="Validate and publish")

_PDF = {"Orientation": "orientation", "Margins": "margins", "Header": "header", "Footer": "footer",
        "Background": "background", "Logo": "logo", "Text": "text", "QR/barcode": "qrBarcode",
        "Terms": "terms", "Perforation indicators where applicable": "perforationIndicatorsWhereApplicable",
        "Print-safe zones": "printSafeZones", "Printer profile": "printerProfile",
        "Paper/stock type": "paperStockType", "Thermal layout": "thermalLayout",
        "Cut behavior": "cutBehavior", "Supported printer integration": "supportedPrinterIntegration"}
_pdf_set = {lab: dict(kind="textField", bindsTo=f"PdfPrintablePosTicketDesignerInput.{prop}",
                      operation="setPdfPrintablePos") for lab, prop in _PDF.items()}
_pdf_set.update({
    "Images": dict(kind="multiSelect", bindsTo="PdfPrintablePosTicketDesignerInput.images", operation="setPdfPrintablePos"),
    "Dynamic fields": dict(kind="multiSelect", bindsTo="PdfPrintablePosTicketDesignerInput.dynamicFields",
                           operation="setPdfPrintablePos"),
    "DPI": dict(kind="numberField", bindsTo="PdfPrintablePosTicketDesignerInput.dpi", operation="setPdfPrintablePos"),
})
F("BO-346", BIND,
  comp_drop=["Print margins", "POS receipt", "Thermal ticket"],
  comp_set=_pdf_set,
  apis_set={"getPdfPrintablePos": dict(purpose="Load the design of the template being edited (query "
                                               "templateId, agreed with contracts in the ledger)")},
  add_comps=[
      ("contentBody", c("selectField", "Output", "PdfPrintablePosTicketDesignerInput.outputFormat",
                        "setPdfPrintablePos", notes="PDF, A4, A5, custom, POS receipt, thermal ticket, box "
                                                    "office stock, pre-printed stock.")),
      ("contentBody", c("textField", "Page size", "PdfPrintablePosTicketDesignerInput.pageSize", "setPdfPrintablePos")),
      ("actionBar", c("primaryButton", "Save design", op="setPdfPrintablePos",
                      notes="templateId is the ticket template the screen was opened for "
                            "(orders.ticket_template, listTicketTemplates).")),
  ],
  note="Bound 4 October 2026 to PdfPrintablePosTicketDesignerInput: one design per ticket template, "
       "keyed by templateId (the orders ticket template from listTicketTemplates); getPdfPrintablePos "
       "reads it by templateId (query parameter agreed in the ledger); the output is the outputFormat "
       "enum, not two buttons; free-text properties are text inputs")

F("BO-716", DEF, pattern="detail", template="split", drop_gaps=("person",),
  patternReason="One event's lifecycle state with the change to its next state beside it (defined 4 "
                "October 2026 from setEventLifecycleState, CHG-FXS-001).",
  regions=[
      ("contentBody", [
          c("detailPanel", "Event", "Event", "getEvent",
            cols("Event", "name", "code", "lifecycleState", "performanceCount", "isActive"),
            notes="lifecycleState is readOnly on Event (agreed with contracts in the ledger)."),
          c("selectField", "Move to", "Event.lifecycleState", "setEventLifecycleState",
            notes="Draft, planned, on sale, live, closed, cancelled, archived; only the next states the "
                  "current one allows. On sale needs a price, a capacity and a schedule; live needs a "
                  "resource plan; cancelled needs a treatment for every buyer (the server refuses "
                  "otherwise, naming what is missing)."),
          c("textField", "Reason", None, "setEventLifecycleState", notes="Body reason; required for cancelled."),
          c("datePicker", "Effective from", None, "setEventLifecycleState", notes="Body effectiveFrom; now by default."),
          c("primaryButton", "Save event lifecycle state", op="setEventLifecycleState",
            notes="A change above the configured impact goes to approvals and shows Waiting for approval; "
                  "getEvent is read again after the 200."),
          c("secondaryButton", "Cancel", notes="Leaves without changing the state."),
      ]),
  ],
  states=dict(loading="The event and its state.", error="Could not load the event. Names it; nothing changes.",
              emptyFirstRun="Not used: the screen opens on one event (eventId)."),
  note="Defined 4 October 2026: the current state is Event.lifecycleState (readOnly, agreed with "
       "contracts in the ledger; setEventLifecycleState's 200 has no body, so the screen reads the "
       "event again), the target state, reason and effective date are the call's body")

F("BO-857", BIND,
  apis_set={"getResource": dict(trigger="onLoad", purpose="The resource being edited (when opened with "
                                                          "resourceId); a PUT sends it back whole")},
  entry=[P("resourceId", "navigation", True, "Opened without it, the form creates a new resource.")],
  comp_drop=["Capacity", "Unit of measure", "Customer selectable", "Priority", "Availability mode",
             "Scheduling mode", "Default duration", "Minimum booking duration", "Maximum booking duration"],
  add_comps=[
      ("contentBody", c("textField", "Code", "Resource.code", "createResource")),
      ("contentBody", c("textField", "Name", "Resource.name", "createResource")),
      ("contentBody", c("selectField", "Kind", "Resource.kind", "createResource")),
      ("contentBody", c("selectField", "Part of", "Resource.parentResourceId", "listResources",
                        notes="Options from listResources; empty for a top-level resource.")),
      ("contentBody", c("numberField", "Setup (minutes)", "Resource.setupMinutes", "createResource")),
      ("contentBody", c("numberField", "Teardown (minutes)", "Resource.teardownMinutes", "createResource")),
      ("contentBody", c("numberField", "Deposit", "Resource.depositAmount", "createResource")),
      ("contentBody", c("multiSelect", "Requires qualification", "Resource.requiresQualification", "createResource")),
      ("contentBody", c("numberField", "Capacity", "Resource.attributes", "createResource",
                        notes="attributes.capacity, with attributes.unitOfMeasure beside it.")),
      ("contentBody", c("numberField", "Default duration (minutes)", "Resource.attributes", "createResource",
                        notes="attributes.defaultDurationMinutes; min and max booking duration are "
                              "attributes.minBookingMinutes and attributes.maxBookingMinutes.")),
      ("contentBody", c("toggle", "Guests can pick it", "Resource.attributes", "createResource",
                        notes="attributes.customerSelectable.")),
      ("actionBar", c("primaryButton", "Create resource", op="createResource",
                      notes="id is a client UUIDv7; venueId from the session.")),
      ("actionBar", c("primaryButton", "Save resource", op="updateResource",
                      notes="Sends the whole Resource read by getResource with the edits (PUT).")),
  ],
  apis_add=[A("listResources", "onLoad", "The resources this one can be part of (parentResourceId)")],
  note="Bound 4 October 2026 to Resource: code, name, kind, venue (session), parent, setup, teardown, "
       "deposit and qualifications; capacity, durations and guest-selectable go into Resource.attributes "
       "(the keys named on each field), as the contract keeps kind-specific settings there. Priority, "
       "availability mode and scheduling mode left the screen (no property)")

F("BO-877", READ,
  apis_add=[A("listProducts", "onLoad", "The experiences to pick from: experienceId is the catalogue "
                                       "product's id (agreed with contracts in the ledger)")],
  add_comps=[("contentBody", c("selectField", "Experience", "Product.id", "listProducts",
                               cols("Product", "name", "kind"),
                               notes="Opened without experienceId, the user picks one here."))],
  note="The experience is picked on the screen 4 October 2026 (listProducts; experienceId is the "
       "product's id), so a cold entry has a list to pick from")

F("BO-866", READ,
  add_comps=[("contentBody", c("detailPanel", "Resource", "Resource", "getResource",
                               cols("Resource", "code", "name", "kind", "status")))],
  apis_add=[A("getResource", "onLoad", "The resource whose cleaning policy is edited; the PUT sends it "
                                       "back whole with the policy changed")],
  note="getResource bound 4 October 2026: updateResource is a full PUT of Resource (id, code, name, kind, "
       "venueId required), so the screen reads the resource and sends it back with only the cleaning "
       "policy changed")
