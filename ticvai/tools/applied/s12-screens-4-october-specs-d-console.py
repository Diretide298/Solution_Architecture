# Platform console and sign-up screens (part of s12-screens-4-october-specs.py; helpers there).
# flake8: noqa

GRANT = [  # the tenant picker and the open grant, as the console screens already draw them
    c("selectField", "Tenant", "Tenant.id", "listTenants", cols("Tenant", "code", "name", "status")),
    c("banner", "Open grant into this tenant", "PlatformStaffGrant", "listOwnPlatformStaffGrants",
      cols("PlatformStaffGrant", "operatorDisplayName", "permissions", "reason", "openedAt", "expiresAt")),
    c("primaryButton", "Open access grant", op="openPlatformStaffGrant",
      notes="Shown when no grant into the picked tenant is open (audit R098)."),
]


def registration(sid, operator):
    F(sid, DEF, pattern="wizard", template="form", drop_gaps=("person",),
      patternReason="Three steps on one form: prove the email, then the organisation, then submit "
                    "(defined 4 October 2026 from OnboardingApplication, CHG-FXS-001).",
      regions=[
          ("contentBody", [
              c("textField", "Work email", "StartProspectSignupRequest.email", "startProspectSignup"),
              c("secondaryButton", "Send code", op="startProspectSignup"),
              c("textField", "One-time code", "VerifyProspectSignupCodeRequest.code", "verifyProspectSignupCode",
                notes="Six digits; five attempts, then a new code is needed."),
              c("secondaryButton", "Verify code", op="verifyProspectSignupCode",
                notes="On success the organisation fields unlock; the verified email becomes "
                      "contactEmail and is not editable."),
              c("textField", "Company name", "OnboardingApplication.companyName", "submitOnboardingApplication"),
              c("textField", "Contact email", "OnboardingApplication.contactEmail", "submitOnboardingApplication",
                notes="The verified email, read-only."),
              c("textField", "Contact phone", "OnboardingApplication.contactPhone", "submitOnboardingApplication",
                notes="E.164, +971 by default."),
              c("selectField", "Country", "OnboardingApplication.countryCode", "submitOnboardingApplication",
                notes="ISO 3166-1 alpha-2; AE by default."),
              c("textField", "Legal name", "OnboardingApplication.billingEntity.legalName",
                "submitOnboardingApplication", notes="Optional here; required before the first invoice."),
              c("textField", "Trade licence number", "OnboardingApplication.billingEntity.tradeLicenceNumber",
                "submitOnboardingApplication", notes="Optional here."),
              c("textField", "Tax registration number (TRN)", "OnboardingApplication.billingEntity.trn",
                "submitOnboardingApplication", notes="Optional; 15 digits for a UAE VAT registrant."),
              c("primaryButton", "Submit", op="submitOnboardingApplication",
                notes="Sends a client UUIDv7 id and status submitted. The venue type and the plan are "
                      "chosen in the next steps (venueTypeTemplateId and requestedPlanId are optional "
                      "here)."),
              c("secondaryButton", "Cancel", notes="Leaves without submitting; nothing is sent."),
          ]),
      ],
      states=dict(loading="Not used: the form renders at once.",
                  error="The call that failed is named beside its button (code, verify or submit); "
                        "what was typed stays."),
      note="Defined 4 October 2026 from StartProspectSignupRequest, VerifyProspectSignupCodeRequest and "
           "OnboardingApplication (companyName, contactEmail, contactPhone, countryCode, billingEntity)"
           + ("; the operator-led path of SGN-002" if operator else ""))


registration("SGN-002", False)
registration("ADM-380", True)

F("ADM-412", BIND, drop_gaps=("person",),
  comp_drop=["Payment methods", "Save payment provider"],
  add_comps=[
      ("contentBody", c("textField", "Provider name", "SetPaymentProviderRequest.name", "setPaymentProvider")),
      ("contentBody", c("selectField", "Gateway", "SetPaymentProviderRequest.kind", "setPaymentProvider",
                        notes="Network International and Stripe for Phase 1 (CF-131).")),
      ("contentBody", c("multiSelect", "Payment methods", "SetPaymentProviderRequest.supportedMethods",
                        "setPaymentProvider")),
      ("contentBody", c("multiSelect", "Currencies", "SetPaymentProviderRequest.supportedCurrencies",
                        "setPaymentProvider")),
      ("contentBody", c("multiSelect", "Channels", "SetPaymentProviderRequest.acceptedOnChannels",
                        "setPaymentProvider")),
      ("contentBody", c("textField", "Credential reference", "SetPaymentProviderRequest.credentialRef",
                        "setPaymentProvider",
                        notes="The vault reference the operator was given, never the key itself.")),
      ("contentBody", c("selectField", "Applies at", "SetPaymentProviderRequest.scopeLevel",
                        "setPaymentProvider", notes="Venue by default: the venue picked above.")),
      ("contentBody", c("toggle", "Active", "SetPaymentProviderRequest.isActive", "setPaymentProvider")),
      ("contentBody", c("cardList", "Routing", "SetPaymentProviderRequest.routing", "setPaymentProvider",
                        cols("PaymentRouting", "priority", "conditions", "fallbackProviderId"),
                        notes="Ordered rules, first match wins; a fallback provider is required.")),
      ("actionBar", c("primaryButton", "Save payment provider", op="setPaymentProvider",
                      notes="Upsert on id; If-Match carries the version read by listPaymentProviders.")),
  ],
  note="Save form bound 4 October 2026 to SetPaymentProviderRequest: name, kind, methods, currencies, "
       "channels, credential reference, scope, active and routing (the methods multiSelect alone could "
       "not send a provider)")

F("ADM-421", BIND, drop_gaps=("~declares no operation that writes",),
  comp_drop=["Venue Name", "Venue Type", "Address", "Time Zone", "Currency", "Operating Region",
             "Default Language", "Operating Model"],
  apis_add=[A("listOrgUnits", "onLoad", "The picked tenant's brands and regions, to place the venue under")],
  add_comps=[
      ("contentBody", c("selectField", "Place under", "CreateScopeNodeRequest.parentId", "listOrgUnits",
                        cols("OrgUnit", "name", "level", "path"),
                        notes="Brand and region nodes of the picked tenant (listOrgUnits level brand, "
                              "region).")),
      ("contentBody", c("selectField", "Level", "CreateScopeNodeRequest.level", "createOrgUnit",
                        notes="venue by default; zone under a venue.")),
      ("contentBody", c("textField", "Code", "CreateScopeNodeRequest.code", "createOrgUnit",
                        notes="Unique in the tenant; letters, digits and hyphens.")),
      ("contentBody", c("textField", "Venue name", "CreateScopeNodeRequest.name", "createOrgUnit")),
  ],
  overlays_drop=["formCreateOrgUnit"],
  note="Bound 4 October 2026 to CreateScopeNodeRequest (level, parentId, code, name) with the parent "
       "picked from listOrgUnits. Type, address, time zone, currency, region, language and operating "
       "model are not part of createOrgUnit: currency and region come from the parent region "
       "(ADR-0018), the rest are venue settings set on the venue's own screens")

F("ADM-424", BIND, drop_gaps=("person",),
  comp_set={"Dependencies": dict(columns=cols("ModuleListing", "moduleCode", "name", "requiresModules",
                                               "incompatibleWithModules", "status")),
            "Active modules": dict(columns=cols("ModuleEnablement", "moduleKey", "displayName",
                                                 "isLicensed", "isEnabled")),
            "Licensed modules": dict(bindsTo="LicencePosition.licensedModules",
                                     columns=["LicencePosition.licensedModules.moduleKey",
                                              "LicencePosition.licensedModules.source",
                                              "LicencePosition.licensedModules.validTo"])},
  comp_drop=["Tenant"],
  add_comps=[("contentBody", c("selectField", "Tenant", "Tenant.id", "listTenants",
                               cols("Tenant", "code", "name", "status")))],
  note="One vocabulary 4 October 2026: ModuleListing.moduleCode, LicencePosition.licensedModules[]."
       "moduleKey and ModuleEnablement.moduleKey all hold ModuleKey values (the contract is asked to "
       "type the first two as ModuleKey, ledger). Activate is enabled for a module only when it is "
       "licensed and every module in its requiresModules is licensed and enabled or being enabled; one "
       "in incompatibleWithModules blocks it, naming the conflict")

F("ADM-460", DEF, pattern="configEditor", template="split", drop_gaps=("person",),
  patternReason="Pick a tenant and a period, calculate the charge as a dry run, read the lines, "
                "then issue (defined 4 October 2026 from generateInvoice, CHG-FXS-001).",
  apis_add=[A("listTenants", "onLoad", "The tenant picker (audit R098)"),
            A("listSubscriptionInvoices", "onLoad", "The tenant's invoices already issued, to show a "
                                                    "period that is billed")],
  entry=[P("tenantId", "navigation", True, "Opened without it, the operator picks a tenant.")],
  regions=[
      ("contentBody", [
          c("selectField", "Tenant", "Tenant.id", "listTenants", cols("Tenant", "code", "name", "status")),
          c("datePicker", "Period start", "SubscriptionInvoice.periodStart", "generateInvoice"),
          c("datePicker", "Period end", "SubscriptionInvoice.periodEnd", "generateInvoice"),
          c("primaryButton", "Calculate", op="generateInvoice",
            notes="dryRun true: prices the period and changes nothing."),
          c("dataTable", "Charge lines", "SubscriptionInvoice.lines", "generateInvoice",
            ["SubscriptionInvoice.lines.kind", "SubscriptionInvoice.lines.moduleCode",
             "SubscriptionInvoice.lines.description", "SubscriptionInvoice.lines.quantity",
             "SubscriptionInvoice.lines.unitPrice", "SubscriptionInvoice.lines.amount"],
            notes="One line per licensed module at its listed price, the package's base line, and "
                  "metered usage lines; the commercial model decides which lines appear."),
          c("metricTile", "Subtotal", "SubscriptionInvoice.subtotal", "generateInvoice"),
          c("metricTile", "Tax", "SubscriptionInvoice.taxAmount", "generateInvoice"),
          c("metricTile", "Total", "SubscriptionInvoice.total", "generateInvoice"),
          c("secondaryButton", "Issue invoice", op="generateInvoice",
            notes="dryRun false; idempotent per tenant and period, so a second issue returns the "
                  "same invoice."),
      ]),
      ("contextPanel", [
          c("dataTable", "Invoices issued", "SubscriptionInvoice", "listSubscriptionInvoices",
            cols("SubscriptionInvoice", "periodStart", "periodEnd", "status", "total")),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="Nothing calculated yet: pick a tenant and a period."),
  note="Defined 4 October 2026 from generateInvoice: the dry run (dryRun true) is the calculation and "
       "its lines are the charge breakdown; the same call without dryRun issues it")

# ── Forecasts: the screen picks its forecast definition (getForecast needs definitionKey) ─────────


def forecast(sid, subject, what, extra_regions=(), dim=None, drop=("person",), more_apis=()):
    F(sid, FCST, pattern="listDetail", template="split", drop_gaps=drop,
      patternReason=f"Forecast values of one {what} definition, picked on the screen (4 October "
                    f"2026, CHG-FXS-004).",
      apis_add=[A("listForecastDefinitions", "onLoad",
                  f"The {what} forecast definitions (subject {subject}); the picked one's "
                  "definitionKey is what getForecast reads")] + list(more_apis),
      regions=[
          ("contentBody", GRANT + [
              c("selectField", "Forecast", "AiForecastDefinition.definitionKey", "listForecastDefinitions",
                cols("AiForecastDefinition", "name", "grain", "horizonDays"),
                notes=f"Query subject {subject}; the first active definition is picked by default."),
              c("datePicker", "From", "AiForecastPoint.targetStart", "getForecast", notes="Query from; today by default."),
              c("datePicker", "To", "AiForecastPoint.targetEnd", "getForecast", notes="Query to; the definition's horizon by default."),
              c("dataTable", "Forecast", "AiForecastPoint", "getForecast",
                cols("AiForecastPoint", "targetStart", "dimensionKey", "p10", "p50", "p90", "unit"),
                notes=(f"dimensionKey is the {dim}; " if dim else "") +
                      "a range, never a bare number (design 5.6)."),
          ]),
          ("contextPanel", [
              c("detailPanel", "The selected value", "AiForecastPoint", "getForecast",
                cols("AiForecastPoint", "targetStart", "targetEnd", "p10", "p50", "p90", "drivers")),
              c("detailPanel", "Version", "AiForecastVersion", "getForecast",
                cols("AiForecastVersion", "versionNumber", "status", "basis", "maturity", "dataCutoffAt")),
          ] + list(extra_regions)),
      ],
      states=dict(LIST_STATES, emptyFirstRun=f"No {what} forecast defined for this tenant yet.",
                  emptyNoResults="No values in this window. Names the window and offers the "
                                 "definition's horizon."),
      note=f"Forecast definition picked on the screen 4 October 2026: listForecastDefinitions (subject "
           f"{subject}) supplies the definitionKey getForecast requires; columns are AiForecastPoint's "
           "(p10, p50, p90). Pack labels with no contract field left the screen")


forecast("ADM-503", "productDemand or timeslotDemand", "product and timeslot demand",
         drop=("person", "~operations return no schema"),
         more_apis=[A("getForecastAccuracy", "onLoad", "How accurate the picked demand forecast has been, "
                                                     "by horizon, so a planner knows how far to trust it")],
         extra_regions=[c("dataTable", "Accuracy by horizon", "AiForecastAccuracy", "getForecastAccuracy",
                          cols("AiForecastAccuracy", "horizonDays", "wape", "bias", "intervalCoverage"))])
forecast("ADM-504", "channelPace", "channel booking pace", dim="sales channel",
         drop=("person", "~operations return no schema"))
forecast("ADM-505", "revenue", "revenue", dim="revenue stream (ticket, membership, add-on, F&B, retail)",
         drop=("person", "~operations return no schema"),
         more_apis=[A("explainMetricChange", "onAction", "Why the revenue forecast moved against the "
                                                       "previous period, by driver")],
         extra_regions=[c("secondaryButton", "Why did it change", op="explainMetricChange",
                          notes="metricKey the definition's, period the selected value's, comparison "
                                "previousPeriod."),
                        c("detailPanel", "Explanation", "AiMetricChangeExplanation", "explainMetricChange",
                          cols("AiMetricChangeExplanation", "change", "changePercent", "drivers", "narrative"))])
forecast("ADM-506", "any", "any", drop=("person", "~operations return no schema"),
         extra_regions=[
             c("dataTable", "Accuracy by horizon", "AiForecastAccuracy", "getForecastAccuracy",
               cols("AiForecastAccuracy", "horizonDays", "periodStart", "wape", "bias", "intervalCoverage")),
             c("dataTable", "Versions", "AiForecastVersion", "listForecastVersions",
               cols("AiForecastVersion", "versionNumber", "status", "basis", "dataCutoffAt")),
             c("secondaryButton", "Why did it change", op="explainMetricChange",
               notes="metricKey the definition's, period the selected value's, comparison forecast."),
             c("detailPanel", "Explanation", "AiMetricChangeExplanation", "explainMetricChange",
               cols("AiMetricChangeExplanation", "change", "changePercent", "drivers", "narrative", "reliability")),
         ])
