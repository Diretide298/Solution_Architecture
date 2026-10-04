# Finance, payments and promotions setup screens (part of s12-screens-4-october-specs.py).
# flake8: noqa

F("ADM-570", DEF, pattern="listDetail", template="split", drop_gaps=("person", "~names 3 actions"),
  patternReason="The provider directory with the selected or new connection beside it (defined 4 "
                "October 2026 from PaymentProviderConnection, CHG-FXS-001).",
  regions=[
      ("contentBody", [
          c("dataTable", "Connected providers", "PaymentProviderConnection", "listPaymentProviderConnections",
            cols("PaymentProviderConnection", "code", "name", "providerKind", "environment", "status",
                 "lastTestedAt")),
          c("primaryButton", "Connect a provider", notes="Opens an empty form; the kind picks gateway, "
                                                         "PSP, acquirer, wallet or BNPL provider."),
      ]),
      ("contextPanel", [
          c("textField", "Code", "PaymentProviderConnection.code", "createPaymentProviderConnection"),
          c("textField", "Name", "PaymentProviderConnection.name", "createPaymentProviderConnection"),
          c("selectField", "Kind", "PaymentProviderConnection.providerKind", "createPaymentProviderConnection",
            notes="Gateway, PSP, acquirer, wallet provider or BNPL provider (the pack's three buttons)."),
          c("selectField", "Environment", "PaymentProviderConnection.environment", "createPaymentProviderConnection",
            notes="Sandbox first; production after a passing test."),
          c("textField", "Merchant account", "PaymentProviderConnection.merchantAccountId",
            "createPaymentProviderConnection"),
          c("textField", "Credential reference", "PaymentProviderConnection.credentialRef",
            "createPaymentProviderConnection",
            notes="The vault reference of the key, write-only; the key itself never passes through a "
                  "screen (ADR-0020 as applied to payments). Agreed field, ledger."),
          c("detailPanel", "Key in use", "PaymentProviderConnection.credentialFingerprint",
            "listPaymentProviderConnections", notes="The fingerprint, so a person can confirm which key "
                                                    "is in use without reading it."),
          c("detailPanel", "Capabilities", "PaymentProviderConnection.capabilities",
            "listPaymentProviderConnections"),
          c("primaryButton", "Connect", op="createPaymentProviderConnection"),
          c("secondaryButton", "Cancel", notes="Discards the form; nothing is sent."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No providers connected yet. Carries Connect a provider."),
  note="Defined 4 October 2026 from PaymentProviderConnection. The credential is written as a vault "
       "reference (credentialRef, write-only; agreed with contracts in the ledger), as setPaymentProvider "
       "already does, and read back only as its fingerprint")

F("ADM-077", DEF, pattern="listDetail", template="split", drop_gaps=("person",),
  patternReason="Validation findings and test results listed and filtered, with the e-invoicing "
                "connection and its transmission log beside them (defined 4 October 2026, CHG-FXS-001).",
  apis_add=[A("listLegalEntities", "onLoad", "The legal entities whose documents are transmitted")],
  regions=[
      ("contentBody", [
          c("selectField", "Area", "CalculationValidationReconciliationServiceInterfaceView.area",
            "listCalculationValidationReconciliation", notes="Filter: tax, fees, formula, currency, "
                                                             "reconciliation, test suite."),
          c("selectField", "Severity", "CalculationValidationReconciliationServiceInterfaceView.severity",
            "listCalculationValidationReconciliation"),
          c("dataTable", "Findings and test results", "CalculationValidationReconciliationServiceInterfaceView",
            "listCalculationValidationReconciliation",
            cols("CalculationValidationReconciliationServiceInterfaceView", "resultKind", "area", "code",
                 "severity", "message", "scenarioName", "passed", "calculationVersion"),
            notes="Critical first. A test scenario row shows passed or failed with its reconciliation."),
          c("detailPanel", "The selected result", "CalculationValidationReconciliationServiceInterfaceView",
            "listCalculationValidationReconciliation",
            cols("CalculationValidationReconciliationServiceInterfaceView", "message", "subjectId",
                 "scenarioType", "reconciliation")),
      ]),
      ("contextPanel", [
          c("dataTable", "E-invoicing connection", "FinEInvoicingProvider", "listEInvoicingProviders",
            cols("FinEInvoicingProvider", "legalEntityId", "providerName", "mode", "documentFormat",
                 "lastAcceptedTestAt")),
          c("selectField", "Legal entity", "LegalEntity.id", "listLegalEntities", cols("LegalEntity", "code", "name")),
          c("selectField", "Status", "FinEInvoiceTransmission.status", "listEInvoiceTransmissions"),
          c("dataTable", "Transmissions", "FinEInvoiceTransmission", "listEInvoiceTransmissions",
            cols("FinEInvoiceTransmission", "documentNumber", "documentKind", "mode", "status", "attempt",
                 "errorMessage", "sentAt")),
          c("datePicker", "Issued from", None, "transmitEInvoices",
            notes="Body issuedFrom; with Issued to, resends every document of the legal entity in the window."),
          c("datePicker", "Issued to", None, "transmitEInvoices",
            notes="Body issuedTo."),
          c("primaryButton", "Send to e-invoicing", op="transmitEInvoices",
            notes="legalEntityId the picked one; documentIds the selected failed rows, or the window. "
                  "Accepted documents are skipped and counted."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No findings: every check passed.",
              emptyNoResults="Nothing matches the filters. Names them and offers to clear them."),
  note="Defined 4 October 2026 from CalculationValidationReconciliationServiceInterfaceView, "
       "FinEInvoicingProvider and FinEInvoiceTransmission, with the legal entity picked from "
       "listLegalEntities for the transmission log and a resend")

F("ADM-069", DEF, pattern="configEditor", template="split",
  drop_gaps=("person", "~names 5 actions"),
  patternReason="The venue's tax profile in one form, with the picked legal entity's invoice "
                "templates and e-invoicing beside it (defined 4 October 2026, CHG-FXS-001).",
  set=dict(purpose="Set this venue's tax profile (one per venue: tax type, jurisdiction, rate, base, "
                   "legal entity and registration, effective dates) and, for the legal entity it "
                   "invoices under, the invoice templates and the e-invoicing connection."),
  apis_add=[A("listLegalEntities", "onLoad", "The legal entities: the tax profile's entity, and the one "
                                             "whose invoice templates and e-invoicing are edited")],
  regions=[
      ("contentBody", [
          c("detailPanel", "Tax profile in force", "TaxProfileJurisdictionConfigurationView",
            "getTaxProfileJurisdiction",
            cols("TaxProfileJurisdictionConfigurationView", "taxProfileName", "taxType", "ratePercent",
                 "jurisdiction", "effectiveFrom", "consumingProductCount")),
          c("textField", "Tax profile name", "TaxProfileJurisdictionConfigurationInput.taxProfileName",
            "setTaxProfileJurisdiction"),
          c("textField", "Tax profile code", "TaxProfileJurisdictionConfigurationInput.taxProfileCode",
            "setTaxProfileJurisdiction"),
          c("selectField", "Tax type", "TaxProfileJurisdictionConfigurationInput.taxType",
            "setTaxProfileJurisdiction", notes="VAT, sales, entertainment, tourism, municipality, "
                                               "service or another regulatory tax."),
          c("numberField", "Rate (%)", "TaxProfileJurisdictionConfigurationInput.ratePercent",
            "setTaxProfileJurisdiction"),
          c("selectField", "Country", "TaxProfileJurisdictionConfigurationInput.country", "setTaxProfileJurisdiction"),
          c("selectField", "Jurisdiction level", "TaxProfileJurisdictionConfigurationInput.jurisdictionLevel",
            "setTaxProfileJurisdiction"),
          c("textField", "Jurisdiction", "TaxProfileJurisdictionConfigurationInput.jurisdiction",
            "setTaxProfileJurisdiction"),
          c("selectField", "Legal entity", "TaxProfileJurisdictionConfigurationInput.legalEntity",
            "setTaxProfileJurisdiction", notes="Options from listLegalEntities."),
          c("textField", "Tax registration number", "TaxProfileJurisdictionConfigurationInput.taxRegistrationNumber",
            "setTaxProfileJurisdiction", notes="Prefilled from the legal entity's TRN."),
          c("selectField", "Taxable base", "TaxProfileJurisdictionConfigurationInput.taxBase",
            "setTaxProfileJurisdiction"),
          c("datePicker", "Effective from", "TaxProfileJurisdictionConfigurationInput.effectiveFrom",
            "setTaxProfileJurisdiction"),
          c("datePicker", "Effective to", "TaxProfileJurisdictionConfigurationInput.effectiveTo",
            "setTaxProfileJurisdiction"),
          c("primaryButton", "Save tax profile", op="setTaxProfileJurisdiction"),
      ]),
      ("contextPanel", [
          c("selectField", "Invoicing legal entity", "LegalEntity.id", "listLegalEntities",
            cols("LegalEntity", "code", "name", "countryCode", "taxRegistrationNumber"),
            notes="A UAE VAT registrant is a legal entity with countryCode AE and a taxRegistrationNumber."),
          c("dataTable", "Invoice templates", "FinTaxInvoiceTemplate", "listTaxInvoiceTemplates",
            cols("FinTaxInvoiceTemplate", "documentKind", "numberPrefix", "nextNumber", "languages",
                 "autoIssueOnPayment", "isActive"), notes="Query legalEntityId the picked one."),
          c("textField", "Document title", "FinTaxInvoiceTemplate.title", "setTaxInvoiceTemplate",
            notes="Per language. In the UAE fixed by law: Tax Invoice, Simplified Tax Invoice."),
          c("textField", "Number prefix", "FinTaxInvoiceTemplate.numberPrefix", "setTaxInvoiceTemplate"),
          c("toggle", "Issue a tax invoice on every paid order", "FinTaxInvoiceTemplate.autoIssueOnPayment",
            "setTaxInvoiceTemplate", notes="On and locked for a UAE VAT-registered legal entity."),
          c("secondaryButton", "Save template", op="setTaxInvoiceTemplate"),
          c("detailPanel", "E-invoicing", "FinEInvoicingProvider", "listEInvoicingProviders",
            cols("FinEInvoicingProvider", "providerName", "mode", "participantId", "lastAcceptedTestAt")),
          c("selectField", "E-invoicing mode", "FinEInvoicingProvider.mode", "setEInvoicingProvider"),
          c("textField", "Provider name", "FinEInvoicingProvider.providerName", "setEInvoicingProvider"),
          c("textField", "Participant id", "FinEInvoicingProvider.participantId", "setEInvoicingProvider"),
          c("textField", "Credential reference", "FinEInvoicingProvider.credentialRef", "setEInvoicingProvider"),
          c("secondaryButton", "Save e-invoicing", op="setEInvoicingProvider",
            notes="legalEntityId the picked one."),
      ]),
  ],
  states=dict(loading="The form with the venue's saved tax profile.",
              error="Could not load. Names the read that failed; the form stays read-only until it loads.",
              emptyFirstRun="No tax profile saved yet: the form is empty and Save creates it."),
  note="Defined 4 October 2026: one tax profile per venue, read and saved as one record (Chinmay's "
       "default of 3 October: one tax-profile read, a list only if the design needs it); the legal "
       "entities come from listLegalEntities, which fills the invoice-template and e-invoicing calls "
       "and tells whether the entity is UAE VAT-registered")

F("ADM-164", DEF, pattern="listDetail", template="split", drop_gaps=("person",),
  patternReason="The campaign's codes listed with a distribution form beside them; the form's "
                "answer is the distribution's counts (defined 4 October 2026, CHG-FXS-001).",
  regions=[
      ("contentBody", [
          c("selectField", "Status", "CouponCode.status", "listCouponCodes", notes="Filter."),
          c("textField", "Batch", "CouponCode.batchId", "listCouponCodes", notes="Filter (query batchId)."),
          c("dataTable", "Codes", "CouponCode", "listCouponCodes",
            cols("CouponCode", "code", "batchId", "status", "assignedSubjectId", "redemptionCount", "validTo")),
      ]),
      ("contextPanel", [
          c("selectField", "Batch to distribute", "CodeDistributionAssignmentManagerInput.batchId",
            "setCodeDistributionManager", notes="Options are the batch ids of the listed codes."),
          c("selectField", "Assign to", "CodeDistributionAssignmentManagerInput.assigneeType",
            "setCodeDistributionManager"),
          c("textField", "Assignee", "CodeDistributionAssignmentManagerInput.assigneeReference",
            "setCodeDistributionManager", notes="The guest, segment, company or partner reference the "
                                                "assignee type names."),
          c("selectField", "Channel", "CodeDistributionAssignmentManagerInput.channelsType",
            "setCodeDistributionManager"),
          c("numberField", "Quantity", "CodeDistributionAssignmentManagerInput.quantity",
            "setCodeDistributionManager"),
          c("primaryButton", "Distribute", op="setCodeDistributionManager"),
          c("metricTile", "Generated", "CodeDistributionAssignmentManagerView.generated", "setCodeDistributionManager"),
          c("metricTile", "Assigned", "CodeDistributionAssignmentManagerView.assigned", "setCodeDistributionManager"),
          c("metricTile", "Sent", "CodeDistributionAssignmentManagerView.sent", "setCodeDistributionManager"),
          c("metricTile", "Redeemed", "CodeDistributionAssignmentManagerView.redeemed", "setCodeDistributionManager"),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No codes generated for this campaign yet."),
  note="Defined 4 October 2026: the codes come from listCouponCodes (the campaign's, by status and "
       "batch); a distribution is one setCodeDistributionManager call whose answer is the counts. The "
       "'every code distribution' table bound to the PUT is gone (the view is one answer, not a list)")
