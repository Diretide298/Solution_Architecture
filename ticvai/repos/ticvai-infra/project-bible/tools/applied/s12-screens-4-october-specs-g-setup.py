# Venue Management setup screens: payments, retail, wallet, F&B, access (part of the specs).
# flake8: noqa

F("BO-024", BIND,
  overlays_add=[dict(id="confirmCloseDepositBoxes", component="confirmDialog", trigger="Close deposit boxes",
                     body="**Names what `closeDepositBoxes` changes and what it leaves alone**, in the "
                          "consequence rather than the verb. **Collects what `closeDepositBoxes` sends "
                          "before it is called.** Required: `counts` (each box's counted cash, per "
                          "denomination). Optional: `boxIds`, `allOpenAtVenue`. Dismissing sends nothing.",
                     confirm=dict(label="Close deposit boxes", operation="closeDepositBoxes"),
                     dismiss=dict(label="Cancel", discards=["counts", "boxIds", "allOpenAtVenue"]),
                     provenance="contract shift.yaml POST /deposit-boxes/close (4 October 2026, CHG-FXS-002)")],
  comp_drop=["id", "orderId", "tender", "amount", "tenderedAmount", "walletAuthorisationId", "deviceId",
             "recordedAt"],
  comp_set={"Deposits": dict(bindsTo="OrdersDeposit", operation="listDeposits",
                             columns=cols("OrdersDeposit", "orderId", "requiredAmount", "authorizedAmount",
                                          "capturedAmount", "status", "ledgerDepositId"),
                             notes="Settle deposit acts on the row's ledgerDepositId (the finance "
                                   "Deposit holding the liability; agreed field, ledger). A row "
                                   "without one has nothing to settle yet.")},
  note="The eight CreatePaymentRequest fields left 4 October 2026: createPayment was removed from this "
       "screen on 2 October (CHG-WIR-025). Settle deposit reads OrdersDeposit.ledgerDepositId, the "
       "finance Deposit settleDeposit takes (orders.deposit and ledger.deposit are two records)")

F("BO-048", READ,
  apis_add=[A("listProducts", "onLoad", "The catalogue's merchandise products (kind merchandise), to pick "
                                       "the one a shop item sells"),
            A("listProductVariants", "onAction", "The picked product's variants; the chosen one is the "
                                                 "item's variantId"),
            A("listProductCategories", "onLoad", "The category pick list, by name"),
            A("listInventoryItems", "onLoad", "The stock item pick list, by name")],
  add_comps=[
      ("contextPanel", c("selectField", "Catalogue product", "Product.id", "listProducts",
                         cols("Product", "name", "kind"), notes="Query kind merchandise; picked by name.")),
      ("contextPanel", c("selectField", "Variant", "CreateMerchandiseRequest.variantId", "listProductVariants",
                         notes="Options from listProductVariants of the picked product, by name; required.")),
      ("contextPanel", c("selectField", "Category", "CreateMerchandiseRequest.categoryId", "listProductCategories",
                         notes="Options from listProductCategories, by name.")),
      ("contextPanel", c("selectField", "Stock item", "CreateMerchandiseRequest.inventoryItemId",
                         "listInventoryItems", notes="Options from listInventoryItems, by name; optional.")),
  ],
  note="Pick lists bound 4 October 2026: the variant comes from listProducts (kind merchandise) then "
       "listProductVariants, the category from listProductCategories and the stock item from "
       "listInventoryItems, each picked by name")

F("BO-1094", BIND, pattern="configEditor", template="form",
  set=dict(purpose="Configure how wallets at this venue may be funded: which funding sources and "
                   "channels are accepted, the minimum, maximum and preset top-ups, the amount above "
                   "which a top-up needs approval, and automatic reload."),
  apis_add=[A("listWalletTypes", "onLoad", "The wallet type the rules apply to (walletTypeId)")],
  regions=[
      ("contentBody", [
          c("selectField", "Wallet type", "WalletFundingRules.walletTypeId", "listWalletTypes",
            notes="Options from listWalletTypes."),
          c("multiSelect", "Funding sources", "WalletFundingRules.allowedFundingSources", "setWalletFundingRules",
            notes="Card, cash, bank transfer, voucher, corporate account, loyalty conversion."),
          c("multiSelect", "Channels", "WalletFundingRules.allowedChannels", "setWalletFundingRules"),
          c("numberField", "Minimum top-up", "WalletFundingRules.minimumTopUp", "setWalletFundingRules"),
          c("numberField", "Maximum top-up", "WalletFundingRules.maximumTopUp", "setWalletFundingRules"),
          c("multiSelect", "Preset amounts", "WalletFundingRules.presetAmounts", "setWalletFundingRules"),
          c("numberField", "Approval above", "WalletFundingRules.approvalAboveAmount", "setWalletFundingRules"),
          c("detailPanel", "Automatic reload", "WalletFundingRules.autoReload", "getWalletFundingRules"),
          c("primaryButton", "Save funding rules", op="setWalletFundingRules",
            notes="If-Match carries the version getWalletFundingRules returned."),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
  ],
  states=dict(loading="The form with the saved rules.",
              error="Could not load. Names the read that failed; the form stays read-only.",
              emptyFirstRun="Never saved: the defaults getWalletFundingRules returns."),
  note="Bound 4 October 2026 to WalletFundingRules, one rules object per venue: funding sources are a "
       "fixed list in the contract, not records, so the screen edits which are allowed rather than "
       "creating methods. Per-method fees and provider choice are not in the contract and left the "
       "screen")

F("BO-111", READ,
  comp_set={"Recipes": dict(columns=cols("Recipe", "id", "menuItemId", "yield", "costPerPortion"),
                            notes="Selecting a row sets the recipeId (Recipe.id, agreed field) for the "
                                  "substitutes and substitution rules.")},
  note="The recipeId listIngredientSubstitutes and setIngredientSubstitutes need is Recipe.id (readOnly, "
       "agreed with contracts in the ledger 4 October 2026); the selected recipe row carries it")

F("BO-1146", BIND, pattern="configEditor", template="split", drop_gaps=("~A per-source refund destination",),
  apis_add=[A("getWalletRefundPolicy", "onLoad",
              "The wallet refund policy as saved, with its version for If-Match: " + AGREED,
              contract="wallet")],
  regions=[
      ("contentBody", [
          c("detailPanel", "Venue refund policy", "RefundPolicy", "getRefundPolicy",
            cols("RefundPolicy", "selfAuthoriseLimit", "requiresApprovalAbove", "allowPartial", "refundWindowDays")),
          c("numberField", "Self-authorise up to", "RefundPolicy.selfAuthoriseLimit", "setRefundPolicy"),
          c("numberField", "Second user above", "RefundPolicy.requiresSecondUserAbove", "setRefundPolicy"),
          c("numberField", "Approval above", "RefundPolicy.requiresApprovalAbove", "setRefundPolicy"),
          c("toggle", "Partial refunds", "RefundPolicy.allowPartial", "setRefundPolicy"),
          c("numberField", "Refund window (days)", "RefundPolicy.refundWindowDays", "setRefundPolicy"),
          c("primaryButton", "Save refund policy", op="setRefundPolicy"),
      ]),
      ("contextPanel", [
          c("selectField", "Refund goes to", "WalletRefundPolicy.defaultDestination", "setWalletRefundPolicy",
            notes="Original tender, wallet (instant, with the guest notified) or the guest's choice."),
          c("textField", "Refund credit type", "WalletRefundPolicy.walletRefundCreditTypeId", "setWalletRefundPolicy"),
          c("toggle", "Restore to the original lots", "WalletRefundPolicy.restoreToOriginalLots", "setWalletRefundPolicy"),
          c("toggle", "Keep the original expiry", "WalletRefundPolicy.restoreOriginalExpiry", "setWalletRefundPolicy"),
          c("numberField", "Bonus for choosing the wallet (%)", "WalletRefundPolicy.walletRefundBonusPercent",
            "setWalletRefundPolicy"),
          c("detailPanel", "Wallet refund policy in force", "WalletRefundPolicy", "getWalletRefundPolicy",
            cols("WalletRefundPolicy", "defaultDestination", "restoreToOriginalLots", "walletRefundBonusPercent")),
          c("dataTable", "Destination by source", "WalletRefundPolicy.destinationsBySource", "getWalletRefundPolicy",
            ["WalletRefundPolicy.destinationsBySource.source", "WalletRefundPolicy.destinationsBySource.destination"]),
          c("primaryButton", "Save wallet refund policy", op="setWalletRefundPolicy",
            notes="If-Match carries the version getWalletRefundPolicy returned; a 412 reloads the form."),
      ]),
  ],
  states=dict(loading="Both policies load together.",
              error="Could not load. Names the policy whose read failed; the other stays editable.",
              emptyFirstRun="Never saved: each section shows its defaults."),
  note="Bound 4 October 2026 to RefundPolicy and WalletRefundPolicy, each read before it is saved "
       "(getWalletRefundPolicy agreed with contracts in the ledger). The 21 pack labels with no "
       "contract property left the screen")

F("BO-155", DEF, pattern="listDetail", template="split", drop_gaps=("person",),
  patternReason="Visual access rules listed with the selected rule edited beside it (defined 4 "
                "October 2026 from VisualAccessRuleBuilderInput, CHG-FXS-001).",
  apis_drop=["listAdmissionRules"],
  apis_add=[A("listVisualAccessRules", "onLoad", "The venue's visual access rules: " + AGREED,
              contract="access")],
  regions=[
      ("contentBody", [
          c("dataTable", "Rules", "VisualAccessRuleBuilderView", "listVisualAccessRules",
            cols("VisualAccessRuleBuilderView", "name", "decision", "appliesTo", "locationIds")),
          c("primaryButton", "New rule", notes="Opens an empty rule; ruleId is a client UUIDv7."),
      ]),
      ("contextPanel", [
          c("textField", "Rule name", "VisualAccessRuleBuilderInput.name", "setVisualAccessRule"),
          c("multiSelect", "Applies to", "VisualAccessRuleBuilderInput.appliesTo", "setVisualAccessRule",
            notes="The credential or ticket kinds the rule covers (WHEN)."),
          c("multiSelect", "Locations", "VisualAccessRuleBuilderInput.locationIds", "setVisualAccessRule",
            notes="Gates and zones (AT)."),
          c("multiSelect", "Conditions", "VisualAccessRuleBuilderInput.conditions", "setVisualAccessRule",
            notes="IF clauses, each one line."),
          c("selectField", "Combine conditions", "VisualAccessRuleBuilderInput.logic", "setVisualAccessRule",
            notes="all or any."),
          c("selectField", "Decision", "VisualAccessRuleBuilderInput.decision", "setVisualAccessRule"),
          c("multiSelect", "Consequences", "VisualAccessRuleBuilderInput.consequences", "setVisualAccessRule"),
          c("primaryButton", "Save rule", op="setVisualAccessRule", notes="Upsert on ruleId."),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No rules yet. Carries New rule."),
  note="Defined 4 October 2026 from VisualAccessRuleBuilderInput: the rules are read with "
       "listVisualAccessRules (agreed in the ledger) and saved one at a time by ruleId; the admission "
       "profiles (listAdmissionRules) share no fields with a rule and left the screen")

F("BO-185", BIND, drop_gaps=("~No read of biometric verification profiles",),
  comp_drop=["Ticket Product", "Ticket Type", "Membership", "Annual Pass", "Multi-Day Ticket",
             "Multi-Attraction Ticket", "VIP Credential", "Accreditation"],
  add_comps=[
      ("contentBody", c("textField", "Profile name", "BiometricVerificationProfileBuilderInput.name",
                        "setBiometricVerificationProfile")),
      ("contentBody", c("selectField", "Applies to", "BiometricVerificationProfileBuilderInput.selectType",
                        "setBiometricVerificationProfile",
                        notes="One of ticket product, ticket type, membership, annual pass, multi-day, "
                              "multi-attraction, VIP credential, accreditation (the pack's eight).")),
      ("contentBody", c("selectField", "Biometric", "BiometricVerificationProfileBuilderInput.biometricType",
                        "setBiometricVerificationProfile")),
      ("contentBody", c("selectField", "Face check", "BiometricVerificationProfileBuilderInput.faceRequirement",
                        "setBiometricVerificationProfile", notes="Not used, optional or required.")),
      ("contentBody", c("selectField", "Status", "BiometricVerificationProfileBuilderInput.status",
                        "setBiometricVerificationProfile")),
  ],
  comp_set={"Save changes": dict(operation="setBiometricVerificationProfile",
                                 notes="Sends profileId (the loaded one, or a new UUIDv7) and venueId "
                                       "from the session; park, zone, attraction and gate stay empty, "
                                       "so the profile applies venue-wide.")},
  note="Bound 4 October 2026 to BiometricVerificationProfileBuilderInput: the eight pack labels are the "
       "values of one selectType, not eight fields; venueId comes from the session. The read gap is "
       "closed (getBiometricVerificationProfile is bound)")
