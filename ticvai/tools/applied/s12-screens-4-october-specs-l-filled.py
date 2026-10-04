# Sprint 1-2 screens whose content was defined or is defined here, with stale person gaps (specs part).
# flake8: noqa

for _sid in ("BO-151", "BO-166", "BO-1065", "ANL-047", "BO-877"):
    F(_sid, STALE, drop_gaps=("person",),
      note="The generator's 'needs a person' gap removed 4 October 2026: the screen's content is "
           "defined (tables, panels and actions bound to its operations)")

F("CMS-025", STALE, drop_gaps=("person", "~names 3 actions"),
  note="The generator's 'needs a person' gaps removed 4 October 2026: the registry is defined, and the "
       "pack's three kinds (analytics tracker, embedded service, other) are values of the technology "
       "type, not separate operations")

F("BO-696", DEF, pattern="configEditor", template="form", drop_gaps=("person",),
  patternReason="One event copied with the parts and date shift chosen (defined 4 October 2026 from "
                "cloneEvent, CHG-FXS-001).",
  regions=[
      ("contentBody", [
          c("detailPanel", "Event to copy", "Event", "getEvent", cols("Event", "name", "code", "performanceCount")),
          c("textField", "New event name", None, "cloneEvent", notes="Body newName; the source name with "
                                                                   "' (copy)' by default."),
          c("multiSelect", "Copy", None, "cloneEvent",
            notes="Body include[]: the parts to copy (performances, prices, capacities, resources, "
                  "content); all ticked by default."),
          c("numberField", "Move dates by (days)", None, "cloneEvent",
            notes="Body shiftDatesByDays; 0 keeps the dates, 7 moves every performance a week on."),
          c("primaryButton", "Copy event", op="cloneEvent",
            notes="On 201 opens the new event (the eventId returned) as a draft."),
          c("secondaryButton", "Cancel", notes="Leaves without copying."),
      ]),
  ],
  states=dict(loading="The event being copied.", error="Could not load the event. Names it; nothing is copied.",
              emptyFirstRun="Not used: the screen opens on one event (eventId)."),
  note="Defined 4 October 2026 from cloneEvent (include, shiftDatesByDays, newName) and getEvent")

F("BO-1062", DEF, pattern="configEditor", template="split", drop_gaps=("person",),
  patternReason="The organisation node in context, with the tenant's venue-setting defaults edited "
                "beside it (defined 4 October 2026, CHG-FXS-001).",
  set=dict(purpose="See where this venue sits in the tenant's hierarchy (tenant, brand, region, venue) "
                   "and set the defaults every venue inherits unless it overrides them."),
  apis_set={"getOrgUnit": dict(trigger="onLoad", purpose="The node opened (orgUnitId), or the venue in "
                                                         "session, with its place in the hierarchy")},
  regions=[
      ("contentBody", [
          c("detailPanel", "Where this sits", "OrgUnit", "getOrgUnit",
            cols("OrgUnit", "name", "code", "level", "path", "isActive", "childCount"),
            notes="path is shown as tenant > brand > region > venue."),
      ]),
      ("contextPanel", [
          c("detailPanel", "Venue setting defaults", "VenueSettings", "getVenueSettingsDefaults",
            cols("VenueSettings", "supportHours", "quietHours", "alerting", "displayCurrencies",
                 "cartLeaseSeconds")),
          c("numberField", "Cart hold (seconds)", "VenueSettings.cartLeaseSeconds", "setVenueSettingsDefaults"),
          c("multiSelect", "Display currencies", "VenueSettings.displayCurrencies", "setVenueSettingsDefaults"),
          c("numberField", "Calendar day starts at (hour)", "VenueSettings.calendarDayStartHour",
            "setVenueSettingsDefaults"),
          c("secondaryButton", "Save venue setting defaults", op="setVenueSettingsDefaults", perm="TENANT_CONFIGURE",
            notes="Sends the defaults read by getVenueSettingsDefaults with these changed (a PUT)."),
      ]),
  ],
  states=dict(loading="The node and the defaults.", error="Could not load. Names the read that failed.",
              emptyFirstRun="Never saved: the platform defaults show."),
  note="Defined 4 October 2026 from OrgUnit (getOrgUnit) and the tenant's venue-setting defaults. Legal "
       "entity, isolation, encryption and residency are set on their own screens (finance, BO-1065)")

F("BO-1066", DEF, pattern="listDetail", template="split", drop_gaps=("person",),
  patternReason="Access policies listed with the selected one edited, simulated and moved through its "
                "states, and the findings and reviews beside them (defined 4 October 2026, CHG-FXS-001).",
  regions=[
      ("contentBody", [
          c("dataTable", "Access policies", "AuthorisationPolicy", "listAuthorisationPolicies",
            cols("AuthorisationPolicy", "name", "effect", "permissions", "appliesToRoleIds", "priority",
                 "effectiveTo")),
          c("textField", "Policy name", "AuthorisationPolicy.name", "createAuthorisationPolicy"),
          c("textField", "Policy code", "AuthorisationPolicy.code", "createAuthorisationPolicy"),
          c("selectField", "Effect", "AuthorisationPolicy.effect", "createAuthorisationPolicy"),
          c("multiSelect", "Permissions", "AuthorisationPolicy.permissions", "createAuthorisationPolicy"),
          c("selectField", "Combine conditions", "AuthorisationPolicy.combining", "createAuthorisationPolicy"),
          c("primaryButton", "Create access policy", op="createAuthorisationPolicy"),
          c("secondaryButton", "Save as new version", op="updateAuthorisationPolicy"),
          c("secondaryButton", "Simulate", op="simulateAuthorisationPolicy",
            notes="What the policy would decide for sample contexts, before it decides anything."),
          c("secondaryButton", "Submit / approve / activate / retire", op="setAuthorisationPolicyState"),
          c("destructiveButton", "Emergency override", op="createEmergencyAccessOverride",
            notes="Needs a reason and an expiry; loud by design."),
      ]),
      ("contextPanel", [
          c("dataTable", "Permission findings", "IdentityPermissionFinding", "listPermissionFindings",
            cols("IdentityPermissionFinding", "kind", "principalId", "permission", "recommendation", "lastUsedAt")),
          c("dataTable", "Access reviews", "IdentityAccessReviewCampaign", "listAccessReviewCampaigns",
            cols("IdentityAccessReviewCampaign", "name", "dueAt", "status", "itemCount", "decidedCount")),
          c("secondaryButton", "Start access review", op="createAccessReviewCampaign"),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No access policies yet: roles alone decide. Carries Create "
                                         "access policy."),
  note="Defined 4 October 2026 from AuthorisationPolicy, IdentityPermissionFinding and "
       "IdentityAccessReviewCampaign with the screen's bound operations")

F("BO-669", DEF, pattern="configEditor", template="form",
  patternReason="One programme's validity edited as a whole record, with presets for temporary and "
                "seasonal programmes (defined 4 October 2026 from AccreditationValidity, CHG-FXS-001).",
  apis_add=[A("listAccreditationProgrammes", "onLoad", "The programme whose validity is set"),
            A("getAccreditationValidity", "onLoad",
              "The programme's validity as saved, before the whole-record save: " + AGREED,
              contract="accreditation"),
            A("setAccreditationValidity", "onAction", "Save the programme's validity (whole record)")],
  regions=[
      ("contentBody", [
          c("selectField", "Programme", "AccreditationProgramme.id", "listAccreditationProgrammes",
            cols("AccreditationProgramme", "code", "name", "status")),
          c("selectField", "Validity", "AccreditationValidity.validityKind", "setAccreditationValidity",
            notes="Presets: Temporary is fixedPeriod, Seasonal is seasonal, Event-only is eventDuration "
                  "(VO-R14: presets inside the validity editor, same record as BO-666)."),
          c("numberField", "Valid for (months)", "AccreditationValidity.validityMonths", "setAccreditationValidity",
            notes="For fixedPeriod and rolling."),
          c("selectField", "On expiry", "AccreditationValidity.onExpiry", "setAccreditationValidity"),
          c("numberField", "Grace period (days)", "AccreditationValidity.gracePeriodDays", "setAccreditationValidity",
            notes="For gracePeriod."),
          c("numberField", "Renewal window (days)", "AccreditationValidity.renewalWindowDays", "setAccreditationValidity"),
          c("toggle", "Renewal re-verifies the holder", "AccreditationValidity.renewalRequiresReverification",
            "setAccreditationValidity"),
          c("primaryButton", "Save", op="setAccreditationValidity",
            notes="Sends the whole AccreditationValidity read by getAccreditationValidity with the edits."),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
  ],
  states=dict(loading="The programme's validity as saved.",
              error="Could not load. Names the read that failed; the form stays read-only.",
              emptyFirstRun="Never saved: the programme's validity is the platform default (eventDuration)."),
  note="Defined 4 October 2026 from AccreditationValidity: the pack's select fields (type, automatic "
       "expiry, renewal eligibility) are validityKind, onExpiry and the renewal fields; the validity is "
       "read with getAccreditationValidity (agreed with contracts in the ledger) before the whole-record save")
