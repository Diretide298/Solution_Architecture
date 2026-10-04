# Blockers on "guess" tickets that an existing operation answers (part of the specs; helpers there).
# flake8: noqa

F("BO-093", READ,
  apis_add=[A("decideProposedAction", "onAction",
              "Close each walkway or label proposal once accepted or rejected (approve / reject), so no "
              "open proposal blocks the publish")],
  comp_set={"Accept or reject segment": dict(notes="acceptWalkwayProposals applies the segment, then "
                                                   "decideProposedAction closes its proposal (approve or "
                                                   "reject with a reason).")},
  add_comps=[("contentBody", c("secondaryButton", "Close proposal", op="decideProposedAction",
                               notes="Fired with the accept or reject of each proposal; a rejected one "
                                     "needs a reason."))],
  note="decideProposedAction bound 4 October 2026: accepting or rejecting a proposal closes it, so the "
       "open proposals that block the publish clear")

F("BO-133", READ,
  apis_add=[A("listReports", "onLoad", "The seeded voidsAndDiscounts report's definition, whose id "
                                      "runReport takes (query search voidsAndDiscounts)")],
  add_comps=[("contentBody", c("selectField", "Report", "ReportDefinition.id", "listReports",
                               notes="The seeded report voidsAndDiscounts by default; its id is runReport's "
                                     "reportId."))],
  note="runReport's reportId comes from listReports (the seeded report's definition, provisioned with "
       "isSystem true), bound 4 October 2026")

F("DEV-008", READ,
  apis_add=[A("listIntegrationListings", "onLoad", "The certification queue: listings waiting for a "
                                                  "decision, whose id certifyIntegration takes")],
  entry=[P("listingId", "deepLink", True, "Otherwise picked from the certification queue."),
         P("version", "deepLink", True), P("requestId", "navigation", True)],
  add_comps=[("contentBody", c("dataTable", "Certification queue", "IntegrationListing", "listIntegrationListings",
                               cols("IntegrationListing", "name", "category", "developerId", "visibility"),
                               notes="Pending certifications first; selecting one gives Certify its listingId."))],
  note="The certification queue is read with listIntegrationListings (4 October 2026); certifyIntegration "
       "acts on the selected listing")

F("POS-020", READ,
  apis_add=[A("listApprovalRequests", "onLoad", "The approval requests waiting for this supervisor "
                                               "(assignedToMe, status pending); each row's id is what "
                                               "decideApprovalRequest takes")],
  add_comps=[("contentBody", c("dataTable", "Approval requests", "ApprovalRequest", "listApprovalRequests",
                               notes="Query assignedToMe and status pending; selecting one gives Decide its "
                                     "requestId. Alerts stay in their own table."))],
  note="The approval inbox lists approval requests with listApprovalRequests (4 October 2026); alerts carry "
       "no requestId, so decisions come from this list")

F("WEB-017", READ,
  apis_add=[A("listLoyaltyProgrammes", "onLoad", "The venue's loyalty programme, whose id "
                                                "getLoyaltyPosition takes (guest-callable, Pattern 4 group 1)")],
  comp_set={"Loyalty": dict(bindsTo="LoyaltyPosition", notes="The guest's position in the programme from "
                                                             "listLoyaltyProgrammes (the first active one).")},
  note="The loyalty tile's programmeId comes from listLoyaltyProgrammes (4 October 2026)")

F("WEB-024", READ,
  apis_add=[A("listMyEntitlements", "onLoad", "The guest's passes, each with its facePassEnrolmentId for "
                                             "getFacePassEnrolment and revokeFacePass")],
  add_comps=[("contentBody", c("cardList", "Passes with a face", "Entitlement", "listMyEntitlements",
                               cols("Entitlement", "productId", "validTo", "facePassEnrolmentId"),
                               notes="Only passes with a facePassEnrolmentId; selecting one reads it."))],
  note="The Face Pass enrolmentId comes from the guest's passes (listMyEntitlements, "
       "Entitlement.facePassEnrolmentId), bound 4 October 2026")
