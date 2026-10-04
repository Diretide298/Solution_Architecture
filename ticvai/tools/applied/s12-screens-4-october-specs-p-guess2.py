# More blockers on "guess" tickets (part of the specs; helpers there).
# flake8: noqa

F("ADM-003", READ,
  apis_add=[A("listCells", "onLoad", "Every cell across tenants with its health summary, to pick one: "
                                    + AGREED, contract="subscription")],
  entry=[P("cellId", "deepLink", True, "From ADM-002 there is none: the operator picks a cell from the list.")],
  add_comps=[("contentBody", c("dataTable", "Cells", "CellDetail", "listCells",
                               cols("CellDetail", "name", "kind", "tier", "status", "isReachable", "lastContactAt"),
                               notes="Every cell, unhealthy first; selecting one loads its health, capacity "
                                     "and jobs."))],
  note="Cross-tenant: the cells are listed with listCells (agreed with contracts in the ledger, 4 October "
       "2026); cellId is optional and comes from the selected row")

F("ADM-021", READ,
  apis_add=[A("listCapabilityTemplates", "onLoad", "The presets (All, Viewer, Mid-level) per module for the "
                                                  "create-role modal (DEC-007)"),
            A("listPermissions", "onLoad", "The per-module permission checklist")],
  add_comps=[("contentBody", c("multiSelect", "Start from presets", "CapabilityTemplate.code", "listCapabilityTemplates",
                               cols("CapabilityTemplate", "name", "module", "presetLevel"))),
             ("contentBody", c("multiSelect", "Permissions by module", "Role.permissions", "listPermissions",
                               notes="Grouped by IdentityPermission.moduleId; a preset ticks its capabilities."))],
  note="The create-role modal's preset picker and checklist read listCapabilityTemplates and "
       "listPermissions (4 October 2026)")

F("CMS-026", BIND,
  comp_set={"Logo": dict(bindsTo="CookieBannerPreferenceCenterDesignerView.logoAssetId",
                         operation="setCookieBannerDesign", notes="A media asset id from the library."),
            "Position": dict(bindsTo="CookieBannerPreferenceCenterDesignerView.position",
                             operation="setCookieBannerDesign"),
            "Theme": dict(kind="textField", bindsTo="CookieBannerPreferenceCenterDesignerView.themeId",
                          operation="setCookieBannerDesign"),
            "Language": dict(kind="multiSelect", bindsTo="CookieBannerPreferenceCenterDesignerView.languages",
                             operation="setCookieBannerDesign")},
  comp_drop=["Branding"],
  add_comps=[("contentBody", c("selectField", "Channel", "CookieBannerPreferenceCenterDesignerView.channel",
                               "setCookieBannerDesign",
                               notes="Required; with the brand, the key the save upserts on.")),
             ("contentBody", c("textField", "Brand", "CookieBannerPreferenceCenterDesignerView.brandId",
                               "setCookieBannerDesign",
                               notes="The brand the design is for; picking a row of the list fills channel "
                                     "and brand and loads that design.")),
             ("contentBody", c("toggle", "Reject in one click", "CookieBannerPreferenceCenterDesignerView.rejectIsOneClick",
                               "setCookieBannerDesign")),
             ("contentBody", c("dataTable", "Designs", "CookieBannerPreferenceCenterDesignerView",
                               "listCookieBannerPreference",
                               cols("CookieBannerPreferenceCenterDesignerView", "channel", "brandId", "position",
                                    "languages")))],
  note="Channel and brand, the upsert key, are fields on the form and choosing a row of the list loads "
       "that design (4 October 2026); the remaining selects are bound to the design's properties")

F("BO-201", BIND,
  add_comps=[("contentBody", c("selectField", "Gate mode", "AccessGateModePolicy.mode", "setGateModePolicy",
                               notes="Free flow or drop arm; required, half of the upsert key with the venue.")),
             ("contentBody", c("toggle", "Open an incident", "AccessGateModePolicy.createsIncident",
                               "setGateModePolicy"))],
  note="Mode (the upsert key) and createsIncident added to the form 4 October 2026")

_VTI = {"ID generation pattern": "idGenerationPattern", "Ticket classification": "ticketClassification",
        "Ticket ownership model": "ticketOwnershipModel",
        "Holder assignment requirements": "holderAssignmentRequirements",
        "Transferability reference": "transferabilityReference", "Validity model": "validityModel",
        "Consumption model": "consumptionModel", "Entitlement model": "entitlementModel"}
_vti = {k: dict(kind="textField", bindsTo=f"VirtualTicketIdentityMasterRecordConfigurationInput.{v}",
                operation="setVirtualTicketIdentity") for k, v in _VTI.items()}
_vti["Media requirements"] = dict(kind="multiSelect",
                                  bindsTo="VirtualTicketIdentityMasterRecordConfigurationInput.mediaRequirements",
                                  operation="setVirtualTicketIdentity", notes="Free entries.")
_vti["Save changes"] = dict(operation="setVirtualTicketIdentity", notes="venueId from the session.")
F("BO-335", BIND, comp_set=_vti,
  note="The nine inputs are text inputs bound to VirtualTicketIdentityMasterRecordConfigurationInput "
       "(free strings in the contract, so no invented options), 4 October 2026")


def _media(sid, fields):
    F(sid, READ,
      apis_add=[A("searchMedia", "onLoad", "The media library, to pick an existing asset by name"),
                A("createUpload", "onAction", "Upload a new asset"),
                A("completeUpload", "background", "Finish the upload once the file PUT succeeds; the asset "
                                                  "id fills the field")],
      add_comps=[("contentBody", c("cardList", "Media library", "MediaAsset", "searchMedia",
                                   cols("MediaAsset", "filename", "kind", "contentType"),
                                   notes=f"Picking one fills {fields} with its id.")),
                 ("contentBody", c("fileUpload", "Upload new", "MediaAsset.id", "createUpload",
                                   notes="createUpload, the file PUT, completeUpload; the asset id fills the "
                                         "field being edited."))],
      note=f"Asset ids ({fields}) come from the media library (searchMedia) or an upload "
           "(createUpload, completeUpload), bound 4 October 2026")


_media("CMS-004", "the logo, icon source, splash and video")
_media("ADM-016", "the brand identity and app icon fields")

F("BO-044", READ,
  apis_add=[A("listCorrectiveActions", "onLoad", "The corrective actions, open first, whose id record, sign, "
                                                "escalate and close take: " + AGREED, contract="fnb")],
  add_comps=[("contentBody", c("dataTable", "Corrective actions", "CorrectiveAction", "listCorrectiveActions",
                               cols("CorrectiveAction", "raisedAt", "source", "status"),
                               notes="Open and overdue first; selecting one gives the actions its actionId."))],
  note="Corrective actions are listed with listCorrectiveActions (agreed with contracts in the ledger, 4 "
       "October 2026)")

F("EMP-067", READ,
  apis_add=[A("listCorrectiveActions", "onLoad", "The actions waiting for this supervisor's signature: "
                                                + AGREED, contract="fnb")],
  add_comps=[("contentBody", c("cardList", "Waiting for my signature", "CorrectiveAction", "listCorrectiveActions",
                               cols("CorrectiveAction", "raisedAt", "source", "status"),
                               notes="Query status recorded; tapping one gives Sign its actionId."))],
  note="The action to sign is picked from listCorrectiveActions (agreed, ledger), 4 October 2026")

F("BO-112", READ,
  apis_add=[A("listProductionPlans", "onLoad", "The production plans by date and status, to reopen one "
                                              "(planId): " + AGREED, contract="fnb")],
  add_comps=[("contentBody", c("dataTable", "Production plans", "ProductionPlan", "listProductionPlans",
                               cols("ProductionPlan", "forDate", "status"),
                               notes="Opening the screen lists plans; Build plan makes a new draft only when "
                                     "pressed, never on load."))],
  note="Plans are listed with listProductionPlans (agreed, ledger) 4 October 2026; a draft is built only "
       "by the Build plan action")

F("BO-1162", READ,
  apis_add=[A("getWalletRiskRules", "onLoad", "The risk rules in force, each with the ruleCode "
                                             "setWalletRiskRuleStatus takes: " + AGREED, contract="wallet")],
  add_comps=[("contentBody", c("dataTable", "Risk rules", "WalletRiskRules.rules", "getWalletRiskRules",
                               notes="Each rule with its code and status; Emergency disable and Suspend act "
                                     "on the selected rule's ruleCode."))],
  note="The risk rules are read with getWalletRiskRules (agreed, ledger) 4 October 2026, so the status "
       "actions have a ruleCode")

F("CMS-007", READ,
  apis_add=[A("listContentBlocks", "onLoad", "The page's existing blocks, in order: " + AGREED,
              contract="white-label"),
            A("updateContentBlock", "onAction", "Edit or reorder a block (position): " + AGREED,
              contract="white-label")],
  add_comps=[("contentBody", c("cardList", "Blocks on this page", "ContentBlock", "listContentBlocks",
                               notes="In page order; drag to reorder (updateContentBlock position)."))],
  note="The builder loads and edits existing blocks with listContentBlocks and updateContentBlock (agreed, "
       "ledger) 4 October 2026")

F("BO-085", READ,
  apis_add=[A("getApprovalRequest", "onLoad", "The one request the screen opens on (requestId): " + AGREED,
              contract="approvals")],
  add_comps=[("contentBody", c("detailPanel", "The request", "ApprovalRequest", "getApprovalRequest",
                               cols("ApprovalRequest", "kind", "status", "requestedByPrincipalId", "requestedAt")))],
  note="The single request is read with getApprovalRequest (agreed, ledger) 4 October 2026; listApprovalRequests "
       "has no id filter")
