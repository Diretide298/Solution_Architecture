#!/usr/bin/env python3
"""Hold the Block A business rules of 3 October 2026 (Chinmay) in the contracts, so they cannot quietly come back.

Change log CHG-RUL-001 to CHG-RUL-021 (changes/entries/CHG-RUL-*.yaml); the answers are in
`docs/active/decisions/answers-3-october-business-rules.md` ("Block A audit business rules" and "Asked as
questions instead of defaults"). The r2 Block A audit (CHG-AUD-001 pattern 4) found contract rules that
disagreed with the screens that call them. Each rule below is one decision; each fails on the package before
the decision and passes after it. Two rules are general, because the same gap can open on any operation:

  BR-STREAM        An operation answers with `text/event-stream` exactly when it declares
                   `x-ticvai-streaming: sse`, and then names its events (`x-ticvai-sse-events`) and keeps a
                   JSON answer for a client that does not ask for the stream. `sendAiMessage` streams (CHG-RUL-002).
  BR-PAIR-REFUSAL  An update that takes the same request schema as a create declares every refusal (4xx) the
                   create declares: the same body passes the same rules (`updateDashboard` skipped the refresh
                   budget, CHG-RUL-008). Pairs found before 3 October and not named by a rule are exempt below,
                   each with its reason. A partial-update request schema (`a partial update of <table>`) counts as
                   the body of the create that persists to that table (ADAM CR-315, CHG-CR315-001).

And one rule per decision:

  BR-APPROVAL-ROUTE  (r8, CHG-R8SPN-016, CHG-R8GEN-013; r10, ADAM CR-102, CHG-R10ID-015) setApprovalMatrix and
                   approveMatrixMultiLevel refuse a condition the engine cannot evaluate (422 condition-invalid, since
                   the condition language exists); submitApprovalRequest's 409 lists approval-no-longer-required and
                   approval-no-approver-available.
  BR-APPROVAL-ENGINE (r10, ADAM CR-102, CHG-R10ID-015) the engine's rules have storage: ApprovalRule.condition
                   defines its language (AND-joined comparisons) and the unreachableRule comparison; a rule's code is
                   unique per rule set (x-ticvai-unique-together [matrix_id, matrixVersion, code], per version since
                   CR-300, CHG-CR300-001); a matrix's version is required; the
                   approver chain is stored (ApprovalRequest.approvers, approvals.request_approver); a decision can be
                   return or requestInformation; the composite operations declare 400, 403 exceedsDelegatorAuthority
                   and 409.
  BR-APPROVAL-VERSIONS (r11, ADAM CR-300, CHG-CR300-001) a matrix keeps one stable id across versions: its versions
                   are approvals.matrix_version rows keyed (approvalMatrixId, version), each rule names its matrixVersion, and
                   ApprovalMatrix is unique on (kind, scopePath); setApprovalMatrix writes the version table.
  BR-BILLING-STATEMENT (r11, ADAM CR-303, CHG-CR303-001) a statement is a completed renewal row or the first period,
                   its charges the cycle's order, its guest customer_id, its dates in the venue's time zone; the id's v5
                   namespace and name are stated on BillingStatement.id, which both statement operations use.
  BR-STORE-CHECKLIST (r11, ADAM CR-304, CHG-CR304-001) every StorePublishingChecklist item has a done-rule and fixed
                   copy, setStoreAccounts names the languages a listing is checked against, and the Pass Type ID is
                   one per tenant.
  BR-PLANNER-QUESTIONS (r11, ADAM CR-321, CHG-CR321-001) the planner's questions are a closed list a venue switches on,
                   orders, relabels and makes required (venuemap.visit_planner_question, each key's default stated),
                   VisitPlannerOptions answers them, setVisitPlannerQuestions writes them and keeps party and dates
                   required, and generateVisitPlan refuses a missing required answer (422 planner-answer-missing).
  BR-ROTA-HOUR-LIMIT (r11, ADAM CR-334, CHG-CR334-001) breachesWorkingHourLimit names the venue's rule (staffing_rules'
                   day, rolling 7-day and rest limits), and both rota writes declare the read.
  BR-ROTA-CROSS-VENUE (r11, ADAM CR-336, CHG-CR336-001) both rota writes ask the overlap and the role as yes/no queries
                   answered under the tenant root grant (never delegatedAccessRecords under the caller's venue), and
                   RotaAssignment's overlap rule is an exclusion constraint (x-ticvai-exclude).
  BR-PRIVACY-REQUEST (r10, ADAM CR-101, CHG-R10ID-016) a guest's privacy request records a subject, not a principal
                   (ApprovalRequest exactly one of requestedByPrincipalId and requestedBySubjectId); exportSubjectData
                   answers an erased subject 410 subject-erased and emits identity.privacyRequestRaised (as
                   deleteGuestAccount does), which Marketing consumes; getSubjectDataExport reads the status and link.
  BR-SCOPE-AUTHZ   (r10, ADAM CR-189, CHG-R10ID-001) the per-scope rule is stated once (Session.permissionsByScope and
                   permission-resolution 7.2): x-ticvai-permission is evaluated at the scope acted on, from the per-scope
                   set; listPrincipals reads its reach from it and createRole needs ROLE_MANAGE at the root (403).
  BR-SSO-ACTIVE    (r10, ADAM CR-190, CHG-R10ID-002) listSsoProviders lists active providers only (a null is_active is not
                   active), ordered by displayName then id.
  BR-PERMISSION-FINDINGS (r10, ADAM CR-210, CHG-R10ID-003) listPermissionFindings states the 50% and 25% peer
                   thresholds and that every authorisation check writes access_decision; listCapabilityTemplates and
                   listAccessReviewItems state full orders.
  BR-ENTITLEMENT-SHARE (r10, ADAM CR-209, CHG-R10ID-004) a share is a delegated_access row of kind sharedEntitlement
                   with ENTITLEMENT_USE; a guest's revoke is recorded (revokedByKind, revokedBySubjectId);
                   revokeEntitlementShare answers 404 for a share of another entitlement.
  BR-PRESET-READONLY (r10, ADAM CR-176, CHG-R10ID-005) setCapabilityTemplate refuses a preset's id with 409
                   capability-template-is-preset.
  BR-END-SESSIONS  (r10, ADAM CR-180, CHG-R10ID-006) updatePrincipal ends a principal's sessions and refresh tokens through
                   identity.end_principal_sessions, which tools/derive-ddl.py writes.
  BR-PLATFORM-TOKEN (r10, ADAM CR-175, CHG-R10ID-007) ADR-0072 defines the platform token; the Control Plane holds the
                   operator, its platform session and its second factors; openPlatformStaffGrant cites the ADR.
  BR-GUEST-TOKENS  (r10, ADAM CR-100, CHG-R10ID-009) getGuestSession answers GuestSessionView, which has no tokens;
                   a refresh token belongs to exactly one of a principal and a guest subject.
  BR-PLATFORM-INVOICE (r10 round 3, ADAM CR-202, CHG-R10ID-023) the contract names the issuing legal entity, the
                   platform tax-rate table exists, and the exact-period unique index skips cancelled invoices.
  BR-GUEST-VENUE   (r10, ADAM CR-198, CHG-R10ID-010, general; 400 venue-required since round 3, CHG-R10ID-022) every venue-level read callable without a session by a
                   guest, a visitor or the public names its venue: a path {venueId}, a required venueId query
                   parameter or the shared GuestVenue header (X-Venue-Id); the rule is stated on guestAuth. Exempt:
                   reads addressed by their own token, and the waiting room's own store (GUEST_VENUE_EXEMPT).
  BR-ANALYTICS-PROVIDER (r11, ADAM CR-323, CHG-CR323-001) one analytics provider row per venueId + provider is a
                   unique key with nulls not distinct, its violation named in setAnalyticsProvider's 409; a PUT that
                   leaves the write-only reportingCredentialRef out keeps the credential and an explicit null clears it.
  BR-MEDIA-COVER-USE (r11, ADAM CR-326 option A, CHG-CR326-001) MediaUsage.surface can name a collection cover
                   (mediaCollectionCover) and deleteMediaAsset reads assets.media_collection to list it with every use.
  BR-AGENT-LAPSE   (r11, ADAM CR-333 option C, CHG-CR333-001) setAgentAvailability sets expiresAt to the earlier of the
                   session's expiry and a heartbeat lapse each PUT refreshes, and a lapsed state reads as offline.
  BR-MEDIA-REPLACE-UPLOAD (r11, ADAM CR-337 option A, CHG-CR337-001) replaceMediaAsset takes the replaced file's key
                   from the asset's current upload (reading assets.asset_version), answers a retry with the current
                   upload 200 unchanged, and refuses an upload already used 409 upload-already-used.
  BR-WALLET-TOPUP-ONCE (r11, ADAM CR-310, CHG-R11CR310-001) a top-up line is credited once: CreditLot.orderLineId
                   carries x-ticvai-unique (derive-ddl writes credit_lot_order_line_id_uniq, partial), and topUpWallet's
                   409 payment-already-used says a unique violation on that index is the refusal.
  BR-WALLET-PUBLISH-CHECKS (r11, ADAM CR-311 option B, CHG-R11CR311-001) publishWalletConfiguration lists its
                   validation checks, credit-type-without-accounting-mapping and consumption-policy-names-retired-type,
                   both blocking, and WalletConfigurationVersion keeps (scopePath, version) unique.
  BR-WALLET-RESTORE-DRAFT (r11, ADAM CR-312 option A, CHG-R11CR312-001) restoreWalletConfigurationVersion writes no
                   configuration_version row and answers the draft with version null; its 409 unpublished-changes
                   compares the area tables with the latest published snapshot as diffWalletConfigurationVersion does;
                   listWalletConfigurationVersions lists no restored draft.
  BR-WALLET-RESTORE-FINDINGS (r12, ADAM CR-355, CHG-CR355-001) restoreWalletConfigurationVersion lists its own two
                   codes, restore-credit-type-retired-since-version and restore-left-newer-rows, both warnings, and never
                   sets a credit type's is_active from false to true.
  BR-WALLET-TOPUP-CREDIT-TYPE (r12, ADAM CR-357, CHG-CR357-001) topUpWallet names each lot's credit type (the one
                   active cash type for the paid lot, the applying bonus rule's bonusCreditTypeId for the bonus), reads
                   wallet.credit_type and wallet.funding_rule, and refuses a bonus the venue did not set (422
                   bonus-not-applicable).
  BR-COOKIE-STRICTLY-NECESSARY (r12, ADAM CR-347, CHG-CR347-001) setCookieBannerDesign's 422 names
                   strictly-necessary-description-missing: no strictlyNecessary category, or its description missing
                   in a language of `languages`.
  BR-ROTA-ROLE-DENY (r12, ADAM CR-344, CHG-CR344-001) identity#principalHoldsRoleAtVenue answers false on a live DENY
                   of the role at or above the venue (deny-overrides-allow), and names #32338 as its builder.
  BR-FORM-VERSION-KEY (r12, ADAM CR-359, CHG-CR359-001) FormDefinition is keyed (id, version), id the form, and the
                   field, requirement and signature rows reference the version row by (form id, version);
                   MarketingWaiverSignature records formVersion; createForm's optional formId makes the next version
                   of an existing form (highest version + 1, 404 when there is none).
  BR-CREDIT-ACCOUNT-CURRENCY (r11, ADAM CR-322 option A, CHG-CR322-001) a B2B credit account stores the currency
                   its limit is agreed in: B2bCreditAccount.currencyCode (required, readOnly; payments.credit_account.
                   currency_code), set by createB2bCreditAccount from creditLimit.currency and never changed after, and
                   neither credit-account operation resolves it from a venue.
  BR-PLATFORM-APPROVAL-RULE (r11, ADAM CR-330 option A, CHG-CR330-001) the platform rule for a tenant subject is a
                   control.platform_approval_rule row seeded by the control migration (x-ticvai-seed-rows:
                   configurationChange, tenant, PLATFORM_TENANT_MANAGE, 2 approvals, active), and createApprovalRequest
                   asks platform-ops#platformApprovalRuleFor over the service route.
  BR-WALLET-ETAG-VERSION (r11, ADAM CR-332 option A, CHG-CR332-001) WalletFundingRules and WalletRefundPolicy carry a
                   version (wallet.funding_rule.version, wallet.refund_policy.version); their GET and PUT send it as
                   ETag, and the PUT refuses a stale If-Match 412, the rule CR-257 chose for group bookings.
  BR-UAEPASS-ENDPOINTS (r12, ADAM CR-360, CHG-CR360-001) guestUaePassLogin builds the token and userinfo endpoints
                   from the row's issuer (UAE Pass publishes no discovery document), uses HTTP Basic, reads sub and
                   the idn claim from userinfo, and never matches an account on the UAE Pass email; setSsoConfig does
                   not refuse a guest uaePass row for its metadataUrl.
  BR-LINK-CHECKOUT (r12, ADAM CR-361, CHG-CR361-001) linkGuestCheckout's verificationCode is optional and ignored; one
                   403 contact-mismatch covers unknown, mismatched and attached-elsewhere; a booking already the
                   caller's answers 200.
  BR-DELEGATION-READS (r12, ADAM CR-362, CHG-CR362-001) grantDelegation and listDelegations ask
                   identity#subjectMinorStatus (one statement under ITenantRootGrant, no date of birth returned) and
                   grantDelegation the tenant root by tenancy#scopeRecords; both are tenant-level; the linked adult's
                   write over a minor is stated on DelegatedAccess and grantDelegation.
  BR-GUEST-POLICY-CURRENCY (r12, ADAM CR-363, CHG-CR363-001) IdentityGuestVerificationPolicy stores currencyCode
                   (identity.guest_verification_policy.currency_code) and neither policy operation resolves the
                   wallet top-up limit's currency from a venue; the set answers 400 on a scale that does not fit.
  BR-CONTENT-PAGE-KEY (r12, ADAM CR-364, CHG-CR364-001) listContentBlocks' pageKey is a uuid (a content page's id),
                   refused 400 otherwise; a homepage section is asked by its contentPageId.
  BR-CONTENT-PUBLISH (r12, ADAM CR-365, CHG-CR365-001) the content block state model publishes a scheduled block now,
                   reschedules it and publishes an expired one by operation; publishContentBlock lists 400 on expireAt
                   and passes approvals' 422 no-approval-route on, and its identity read names approvedByPrincipalId.
  BR-CONTENT-BLOCK (r12, ADAM CR-366, CHG-CR366-001) createContentBlock and updateContentBlock ask
                   marketing-crm#segmentRecords in process for audienceSegmentId and refuse it 422 unknown-reference,
                   and check the body only as far as ContentBlock.body defines it (400 validation); the full per-kind
                   schema is left out (LO-CR366-001), never "validated against the block's own schema".
  BR-SCOPE-LOOKUP  (r12, ADAM CR-367, CHG-CR367-001) permissionsByScope has an entry per grant path, allow or deny, each
                   the full section 2 result, and a node takes the deepest listed entry containing it: every vector of
                   docs/architecture/specs/permission-vectors.json run through that lookup gives the vector's answer, and
                   neither the spec nor Session.permissionsByScope says "the node acted on or one of its ancestors".
  BR-ID-RESUBMIT   (r12, ADAM CR-368, CHG-CR368-001) submitGuestIdentityDocument applies the policy's maxResubmissions
                   (refusals since the latest verified one, 422 resubmission-limit-reached) and reads the count's table.
  BR-DOC-NUMBER-ENC (r12, ADAM CR-369, CHG-CR369-001) a document number is field-encrypted into
                   pii.subject_document.number_ciphertext (ADR-0063 section 5), never hashed, and number_hash is
                   nullable.
  BR-REGISTER-SOURCE (r12, ADAM CR-371, CHG-CR371-001) RegisterGuestRequest.source (guestWeb, guestApp, kiosk) is what
                   identity.guestRegistered carries as channel, and its Marketing consumer maps it to a ConsentSource
                   (never registration).
  BR-GUEST-CODE-DELIVERY (r12, ADAM CR-370 and its follow-up of 31 October, CHG-CR370-001; general) every operation
                   that writes identity.otp_challenge either mints a code and emits identity.guestCodeIssued, or is named
                   in GUEST_CODE_NON_ISSUERS with why it mints none; the event carries destination and code
                   field-encrypted, never in clear, to Marketing's relay-invoked sendGuestOneTimeCode; no issuer writes
                   marketing.message_dispatch across deployables; the lifetime and resend interval are venue settings
                   (600 s and 60 s) answered as expiresInSeconds and resendAfterSeconds; and requestGuestOtp states who
                   with no account still gets a code (register, verify).
  BR-GUEST-SETTINGS (r12, ADAM CR-341 option B for the settings tables, CHG-CR341-001) listMyOrders names no venue and
                   reads each order's venue settings through tenancy#venueSettingsRecords (an order whose settings are not
                   visible is a fault, never a default currency); guestAuth and the venue and region settings queries
                   state the guest read branch of platform.venue_settings and platform.region_settings.
  BR-BILLING-LINES (r12, ADAM CR-342 option A with refunds from orders.refund, CHG-CR342-001) both statement
                   operations read orders.sales_order, orders.order_line_discount, orders.refund and payments.dunning_case
                   and ask tenancy#venueSettingsRecords and finance#taxInvoiceLineRecords; listBillingStatements states the
                   line, total and listing rules (completed refunds, overdue_amount, no adjustment, a cycle with no order or
                   an open-ended first period not listed) and getBillingStatement its 404; BillingStatement is computed
                   from no orders.payment; payments.dunning_case is guest-reads-own (the CR-295 pattern).
  BR-SHOP-DROP-COLLECT (r12, ADAM CR-345 as recommended, CHG-CR345-001) ShopAndDropProblem.refusedReason has
                   disposed; collectShopAndDrop's 409 declares shop-and-drop-already-collected, -past-collect-by and
                   -disposed, and states that a partial take from uncollected stays uncollected and that pastCollectBy is
                   judged on the server's clock (recordedAt decides nothing).
  BR-DELEGATION-KEY (r12, ADAM CR-352, CHG-CR352-001) approveRoleAuthorityDelegation is no singleton: it is keyed by
                   x-ticvai-body-key [delegator, delegate] at the caller's venue, touches no other delegation, and its
                   200 stays RolesAuthorityDelegationApprovalLimitsView.
  BR-FOREIGN-TENDER (r12, ADAM CR-353, CHG-CR353-001) getForeignTenderReport counts cash payments captured or refunded
                   in a currency other than the shift venue's, one line per (shift, tender_currency, fx_rate), filters
                   recorded_at, and asks tenancy#venueSettingsRecords, orders#salesOrderRecords and identity#principalRecords.
  BR-PRODUCT-FROM-PRICE (r12, ADAM CR-358 option (a), CHG-CR358-001) Product.fromPrice is a nullable, readOnly,
                   unstored Money; listProducts takes channel and asks tenancy#venueSettingsRecords; WEB-035's and
                   GST-044's price cards bind Product.fromPrice.
  BR-BOOKING-FLOW-MISSING (r12, ADAM CR-343, CHG-CR343-001) bookingFlowMissing counts a venue's sellable bookable
                   products of a kind some flow type books, against that venue's own enabled flows (no tenant-wide
                   flow), and validateTenantConfig and publishTenantConfig ask catalogue#productRecords and
                   tenancy#activeVenues in process.
  BR-CALL-DISPOSITION (r12, ADAM CR-346, CHG-CR346-001) CallDisposition is stored on marketing.conversation in its
                   four columns, and setCallDisposition ends a conversation an agent holds (withAgent or waitingOnGuest
                   to resolved in states/conversation.yaml) and answers 400 for a callback without callbackAt.
  BR-RESTORE-MISSING-PAGE (r12, ADAM CR-350, CHG-CR350-001) restoreConfigVersion restores a section or navigation item
                   whose content page is gone hidden (contentPageId null, isVisible false), never refuses for it, and
                   keeps content_page.is_referenced.
  BR-PRICING-QUEUE-MEMBERS (r12, ADAM CR-416, CHG-CR416-001) the recommendation queue and explainability reads declare
                   catalogue.pricing_simulation, catalogue.price_category and tenancy#scopeRecords, state each member's
                   rule, answer actualRevenueResultPercent null (nullable, LO-CR416-001) and confidence times 100.
  BR-PRICING-AUTOMATION-LEVEL (r12, ADAM CR-417, CHG-CR417-001) both automation views answer automationLevel and no
                   automationMode; the policy view's scopeLevel and listDynamicPricingAutomation's filter list every
                   level DynamicPricingControl stores; the orchestrator reads pricing_market and sales_channel for
                   market and channel, and channel is nullable.
  BR-PRICING-SCORECARD (r12, ADAM CR-418, CHG-CR418-001) listLearningModelPerformance waits on the price outcome
                   measure and is assembled from three sources, with no catalogue.model_scorecard anywhere.
  BR-PRICE-SIMULATION (r12, ADAM CR-419, CHG-CR419-001) simulatePriceBreakdownCalculation is no singleton, takes variantId,
                   reads tax through finance#taxCodeRecords and the live price from price_execution, declares 400
                   validation and 422 no-selected-rate / no-calculation-profile, and answers aiInsights empty.
  BR-CALC-PROFILE-VERSION (r12, ADAM CR-420, CHG-CR420-001) CalculationProfile is unique on (scopePath, code, version),
                   setPriceCalculationPolicy finds its record by the path id, numbers versions on the server and
                   answers a second active default 409 default-profile-exists; dependsOn names sequence numbers.
  BR-ROLLBACK-CANCEL (r12, ADAM CR-421, CHG-CR421-001) cancelPricingRollback cancels its waiting approval request in
                   process (IApprovalRequests.CancelAsync), writes no outbox row, and cancelApprovalRequest names the
                   in-process move.
  BR-LIVE-PRICE    (r12, ADAM CR-422, CHG-CR422-001) createLiveDynamicPrice never writes catalogue.price, emits
                   catalogue.priceExecuted (an event file with a consumer), reads its approval through
                   approvals#requestRecords, and declares 400 validation and 422 approval-required / guardrail-breached.
  BR-STRATEGY-FIGURES (r12, ADAM CR-423, CHG-CR423-001) listDynamicPricingStrategy reads price_execution and
                   price_ladder, names venue and owner through tenancy#scopeRecords and identity#principalRecords, gives
                   each figure its rule and offers no testing status (LO-CR423-001).
  BR-PRICE-BAND-ORDER (r12, ADAM CR-424, CHG-CR424-001) listDynamicPriceBand sorts by ladderId only, a member of its
                   view; a sort on `code`, which a price ladder lacks, fails.
  BR-GUARDRAIL-SCOPE (r12, ADAM CR-425, CHG-CR425-001) setDynamicPricingGuardrailPolicy is keyed by [scopeLevel, scopeId],
                   declares 400 validation and 422 scope-id-required / scope-not-found / no-approval-route, keeps a raise
                   in pendingAutomationLevel and pendingApprovalRequestId (readOnly), types its three lists as arrays,
                   and Catalogue consumes the four approval outcomes for subjectType dynamicPricingControl.
  BR-GUEST-SELF-403  (r8, CHG-R8SPN-018) a guest operation scoped to the caller's subject answers another subject's
                   record 404, not 403: a ratchet (GUEST_SELF_403_CEILING). BR-ALERT-RECIPIENT (CHG-R8SPN-020) is a
                   warning until reporting's listAlerts states its recipient filter.

  BR-SPLIT         (CHG-RUL-001) Five split methods; `closeTableVisit` takes a payment without `subBillId` (an
                   unsplit bill is one sub-bill); `splitBill` and `closeTableVisit` state the outlet's payment
                   timing (`paymentTiming`, send first or pay first).
  BR-VISIT-PLAN    (CHG-RUL-003, CHG-RUL-009) `VisitPlanUpdate` has `addAddOn` and `removeAddOn`; the plan is built
                   and changed in an anonymous guest session and moves to the account on sign-in; booking needs a
                   signed-in guest (`sign-in-required`).
  BR-PO            (CHG-RUL-004) A purchase order request requires neither a requisition nor a quotation (blanket
                   and RFQ-award orders), names its `kind`, and refuses a standard order without an approved
                   requisition (`requisition-required`); the order goes through the approval matrix.
  BR-PAY-LINK      (CHG-RUL-005, CHG-RUL-021) `createPaymentLink` answers 200 with the live link it already has
                   and 409 `order-already-paid` for a paid order; `cancelPaymentLink` (ORDER_CREATE) cancels a live
                   link and refuses one that is not live.
  BR-REPORT-RUNS   (CHG-RUL-006) `listReportExecutions`: `mineOnly` is a filter, and seeing other people's runs
                   does not need `REPORT_MANAGE`.
  BR-CONTRAST      (CHG-RUL-007) `Theme` lists its WCAG AA pairs (`x-ticvai-contrast-pairs`): every colour named
                   exists, text pairs need 4.5:1, large text and non-text pairs 3:1.
  BR-WO-CANCEL     (CHG-RUL-010) `cancelWorkOrder` refuses only once labour time or a part is recorded
                   (`work-recorded`).
  BR-INCIDENT      (CHG-RUL-011) Incidents: reported, investigating, escalated (optional), closed; reopen to
                   investigating with a reason; each change logged. Checked in the contract and `states/incident.yaml`.
  BR-FARE          (CHG-RUL-012) Fare tables are versioned by `effectiveFrom`: a future table sits beside the
                   current one (`FareTable.upcoming`) and a quote prices at travel time (`travelAt`).
  BR-SESSIONS-DOOR (CHG-RUL-015) `listActiveSessions` and `forceLogout` admit a call with no session (`{}`) and
                   carry the supervisor's PIN step-up themselves.
  BR-ATTENDANCE    (CHG-RUL-016) `recordAttendance` acts on the caller (`x-ticvai-self-scoped: principal`, no
                   person in the body); `amendAttendance` is the supervisor's correction.
  BR-AI-CURRENCY   (CHG-RUL-017) The AI spend ceiling defaults to the tenant's billing currency, never USD.
  BR-QR            (CHG-RUL-018) The admission QR (`getEntitlementCredential.rotation`) steps every 30 seconds by
                   default (GST-055).
  BR-NEW-OPS       (CHG-RUL-013) `listMyTableReservations` (self-scoped, paged), `listBookableOutlets` (public,
                   published, paged), `uploadIncidentMedia` and `addIncidentPerson` exist.

And one rule per decision for the CRs of 18 October 2026 (class 9, "rules nobody has decided yet"; CHG-CRA-007):

  BR-GUEST-PII     (ADAM CR-141) every GuestProfile property is marked personal or behavioural
                   (`x-ticvai-data-class`), the six personal fields among them; `searchGuests` states the consent rule,
                   the id order without GUEST_VIEW_PII and leaves out lifetimeValue until it has a currency.
  BR-HOST-ROUTING  (CR-162) `resolveTenantHost` states 308, terminated is 404, which databases are opened, a
                   platform subdomain verified at provisioning, and `database_name` informational.
  BR-CASH-RECEIPT  (CR-168) a `payment` journal source, a region's account mapping by scope path, entry numbers unique
                   per legal entity, the next open period, and createPayment's two settings reads.
  BR-HOLD-LAPSE    (CR-169) a seat reservation names its hold and can be `sold`; `convertInventoryHold` moves the
                   envelope's units and states the lapsed-hold rule (unitsGone, nothing refunded automatically).
  BR-LOGIN-ATTEMPTS (CR-170, 19 October 2026; CHG-CRA-009) every wrong-credentials 401 of login carries
                   attemptsRemaining, counted per submitted username known or not and per sign-in method, and
                   sso-sign-in-required does not; verifyMfaChallenge carries it on its wrong-code 422 and not on its
                   401, a missing or expired challenge session (narrowed, 20 October 2026, CHG-R8DEC-001); login's 409
                   says since when and on what.
  BR-GATE-CANCEL   (CR-171, 19 October 2026; CHG-CRA-010) a cancelled gate mode change records who, when and why in
                   its own columns, leaving the scheduler's untouched.
  BR-APPROVED-OUTCOME (20 October 2026, option A; CHG-R8DEC-002) an approved action's outcome has a writer:
                   approvals' recordApprovedActionOutcome, service-only, takes applied, notApplied or noOp and returns
                   the execution; the lineage has it write approvals.approved_action_execution; suspendTenant's and
                   reactivateTenant's grant consumers call it.

The step-up rule of `rejectShiftVariance` (CHG-RUL-014), and of `closeShift`, `acceptShiftVariance`,
`withdrawFromDepositBox` and the 20 MFA step-ups (CHG-RUL-019, CHG-RUL-020), is held by `check-step-up.py`
(SU-CARRIER), which asks every step-up operation where it carries the step-up.

    python3 tools/check-business-rules.py
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]

# Operations whose answer streams, by decision. A new streaming operation declares itself and BR-STREAM holds it.
STREAMING_REQUIRED = {"sendAiMessage": "Chinmay, 3 October: stream answers (CHG-RUL-002)"}

# **BR-PAIR-REFUSAL exemptions**: pairs found on 3 October that no business rule named. Each is a judgement
# (an update may not be able to meet the create's refusal, e.g. a reservation already holding its table), so
# each is listed with why it is not fixed here. A new pair is not exempt.
PAIR_EXEMPT = {
    ("createTableReservation", "updateTableReservation"):
        "409 on create is a slot already full; the update re-checks capacity under 422 (not reviewed by a rule)",
    ("createTableReservationForGuest", "updateTableReservation"):
        "the staff create's 400/409 are about naming the guest, which an update does not do (not reviewed)",
    ("createReport", "updateReport"):
        "400 on create is the definition's validation; whether update shares it is open (not reviewed)",
    ("createTicketTemplate", "updateTicketTemplate"):
        "400 on create is the template's validation; whether update shares it is open (not reviewed)",
}

PARSE_ERRORS: list = []

WCAG_MIN = {"text": 4.5, "largeText": 3.0, "nonText": 3.0}


def load(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8")) or {}


def operations():
    out = {}
    for f in sorted((ROOT / "contracts").rglob("*.yaml")):
        if "frozen" in f.parts:
            continue
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception as e:  # a contract that does not parse hides every rule in it: fail, never skip
            PARSE_ERRORS.append(f"{f.relative_to(ROOT)} does not parse: {str(e).splitlines()[-1]}")
            continue
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for method, op in item.items():
                if isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = (f, path, method, op, doc)
    return out


def schema_of(doc, node):
    """Resolve a local `#/components/schemas/X` reference once (and allOf members), else the node."""
    if not isinstance(node, dict):
        return {}
    ref = node.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
        return ((doc.get("components") or {}).get("schemas") or {}).get(ref.rsplit("/", 1)[1]) or {}
    return node


def props(doc, node):
    node = schema_of(doc, node)
    out = dict(node.get("properties") or {})
    for part in node.get("allOf") or []:
        out.update(props(doc, part))
    return out


def body_schema(op):
    return (((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {}).get("schema") or {}


# BR-GUEST-CODE-DELIVERY (ADAM CR-370): writers of identity.otp_challenge that mint no code, each with why. A new writer
# either emits identity.guestCodeIssued or is listed here.
GUEST_CODE_ISSUERS = ("requestGuestOtp", "registerGuest", "verifyGuestEmail")
GUEST_CODE_NON_ISSUERS = {
    "verifyGuestOtp": "checks a code and counts wrong entries or consumes it; it mints none",
}


# BR-GUEST-SELF-403: guest operations scoped to the caller's subject that declared 403 on 20 October 2026 (13 on the
# generators branch before the core lane's CHG-R8SPN-018 merged). Lower it as they are fixed; never raise it.
GUEST_SELF_403_CEILING = 13


# BR-GUEST-VENUE (ADAM CR-198, CHG-R10ID-010): public guest reads that need no venue scope, each with its reason.
GUEST_VENUE_EXEMPT = {
    "getOrder": "addressed by the order access token, which gives its one order's reach (CHG-R9CR-004)",
    "getPaymentLink": "addressed by the payment link's own token",
    "getWaitingRoomPosition": "reads the on-sale waiting room's own store (ADR-0066), no venue table",
}


def problem_types(op):
    s = json.dumps(op.get("responses") or {}, default=str)
    return set(re.findall(r"[a-z]+(?:-[a-z]+)+", s))


def text(op):
    return json.dumps(op, default=str)


def main() -> int:
    ops = operations()
    errors = collections.defaultdict(list)

    def need(rule, cond, msg):
        if not cond:
            errors[rule].append(msg)

    def op(oid):
        return ops.get(oid, (None, None, None, {}, {}))

    # -------------------------------------------------------------- BR-STREAM (general)
    for oid, (f, path, method, o, doc) in sorted(ops.items()):
        streams = any("text/event-stream" in ((r or {}).get("content") or {})
                      for r in (o.get("responses") or {}).values() if isinstance(r, dict))
        declared = o.get("x-ticvai-streaming")
        if streams and declared != "sse":
            errors["BR-STREAM"].append(f"{oid} ({f.name}): answers text/event-stream without x-ticvai-streaming: sse")
        if declared:
            ok200 = "text/event-stream" in (((o.get("responses") or {}).get("200") or {}).get("content") or {})
            need("BR-STREAM", ok200, f"{oid}: declares streaming and has no 200 text/event-stream response")
            need("BR-STREAM", bool(o.get("x-ticvai-sse-events")), f"{oid}: streams and names no x-ticvai-sse-events")
            json_too = "application/json" in (((o.get("responses") or {}).get("200") or {}).get("content") or {})
            need("BR-STREAM", json_too, f"{oid}: streams and keeps no application/json answer for other clients")
    for oid, why in STREAMING_REQUIRED.items():
        need("BR-STREAM", op(oid)[3].get("x-ticvai-streaming") == "sse", f"{oid} must stream ({why})")

    # -------------------------------------------------------------- BR-PAIR-REFUSAL (general)
    # **A partial update is the create's body too** (ADAM CR-315, option A, 29 October 2026; CHG-CR315-001). Since the
    # CR-089 pattern (CHG-SHP-008) an update may take its own `...Request` schema marked `x-ticvai-persistence: none —
    # request only; a partial update of <table>`, so it no longer shared the create's `$ref` and the pair went unread:
    # updateRotaAssignment ("Move or cancel") declared no 409 while createRotaAssignment refuses an overlap and a
    # missing role. Such a schema is keyed here as the create's body that persists to the same table.
    by_table = {}
    for oid, (f, path, method, o, doc) in ops.items():
        ref = body_schema(o).get("$ref")
        if ref and method == "post" and oid.startswith("create"):
            tbl = str(schema_of(doc, body_schema(o)).get("x-ticvai-persistence") or "").strip().strip('"')
            if tbl and not tbl.startswith("none"):
                by_table.setdefault((f.name, tbl), ref)
    by_schema = collections.defaultdict(list)
    for oid, (f, path, method, o, doc) in ops.items():
        ref = body_schema(o).get("$ref")
        if ref:
            pers = str(schema_of(doc, body_schema(o)).get("x-ticvai-persistence") or "")
            m_ = re.search(r"a partial update of ([a-z_]+\.[a-z_]+)", pers)
            if m_ and (f.name, m_.group(1)) in by_table:
                ref = by_table[(f.name, m_.group(1))]
            codes = {str(k) for k in (o.get("responses") or {}) if str(k)[0] == "4"} - {"401", "403", "404", "429"}
            by_schema[(f.name, ref)].append((oid, method, codes))
    for (fname, ref), members in sorted(by_schema.items()):
        creates = [m for m in members if m[1] == "post" and m[0].startswith("create")]
        updates = [m for m in members if m[1] in ("put", "patch") and m[0].startswith(("update", "set", "replace"))]
        for c in creates:
            for u in updates:
                missing = c[2] - u[2]
                if missing and (c[0], u[0]) not in PAIR_EXEMPT:
                    errors["BR-PAIR-REFUSAL"].append(
                        f"{u[0]} takes {c[0]}'s body ({ref.rsplit('/', 1)[1]}) and does not declare its "
                        f"{', '.join(sorted(missing))}")

    # -------------------------------------------------------------- BR-SPLIT
    f, _, _, split, doc = op("splitBill")
    methods = set((((doc.get("components") or {}).get("schemas") or {}).get("SplitMethod") or {}).get("enum") or [])
    need("BR-SPLIT", {"byAmount", "byCovers", "byCategory", "byLine", "bySeat"} <= methods,
         f"SplitMethod lacks a method: has {sorted(methods)}")
    _, _, _, close, cdoc = op("closeTableVisit")
    pay = (props(cdoc, body_schema(close)).get("payments") or {}).get("items") or {}
    need("BR-SPLIT", "subBillId" not in (schema_of(cdoc, pay).get("required") or []),
         "closeTableVisit still requires payments[].subBillId (an unsplit bill closes as one sub-bill)")
    for oid in ("splitBill", "closeTableVisit"):
        need("BR-SPLIT", "paymentTiming" in text(op(oid)[3]), f"{oid} does not state the outlet's payment timing")

    # -------------------------------------------------------------- BR-VISIT-PLAN
    _, _, _, upd, vdoc = op("updateVisitPlan")
    change = schema_of(vdoc, ((props(vdoc, body_schema(upd)).get("changes") or {}).get("items") or {}))
    kinds = set(((change.get("properties") or {}).get("op") or {}).get("enum") or [])
    need("BR-VISIT-PLAN", {"addAddOn", "removeAddOn"} <= kinds,
         f"VisitPlanUpdate change kinds lack addAddOn/removeAddOn: {sorted(kinds)}")
    need("BR-VISIT-PLAN", "sign-in-required" in problem_types(op("bookVisitPlan")[3]),
         "bookVisitPlan does not refuse an anonymous session (sign-in-required)")
    need("BR-VISIT-PLAN", "moves to the account" in text(op("generateVisitPlan")[3]),
         "generateVisitPlan does not say the anonymous plan moves to the account on sign-in")

    # -------------------------------------------------------------- BR-PO
    _, _, _, cpo, idoc = op("createPurchaseOrder")
    req = schema_of(idoc, body_schema(cpo))
    need("BR-PO", not ({"requisitionId", "quotationId"} & set(req.get("required") or [])),
         "CreatePurchaseOrderRequest still requires requisitionId or quotationId (blanket and RFQ-award orders)")
    need("BR-PO", "kind" in (req.get("properties") or {}), "CreatePurchaseOrderRequest names no kind")
    need("BR-PO", "requisition-required" in problem_types(cpo),
         "createPurchaseOrder does not refuse a standard order without an approved requisition")
    need("BR-PO", "approval matrix" in text(cpo), "createPurchaseOrder does not route through the approval matrix")

    # -------------------------------------------------------------- BR-PAY-LINK
    _, _, _, pl, _ = op("createPaymentLink")
    need("BR-PAY-LINK", "200" in (pl.get("responses") or {}), "createPaymentLink has no 200 for the live link it returns")
    need("BR-PAY-LINK", "order-already-paid" in problem_types(pl), "createPaymentLink does not refuse a paid order 409")
    cpl = op("cancelPaymentLink")[3]
    need("BR-PAY-LINK", cpl.get("x-ticvai-permission") == "ORDER_CREATE" and "payment-link-not-live" in problem_types(cpl),
         "cancelPaymentLink is missing, not under ORDER_CREATE, or does not refuse a link that is not live (CHG-RUL-021)")

    # -------------------------------------------------------------- BR-REPORT-RUNS
    _, _, _, lr, _ = op("listReportExecutions")
    mine = next((p for p in lr.get("parameters") or [] if isinstance(p, dict) and p.get("name") == "mineOnly"), {})
    d = str(mine.get("description") or "")
    need("BR-REPORT-RUNS", "filter" in d and "REPORT_MANAGE" not in d.split("filter")[0],
         "listReportExecutions.mineOnly is not a filter, or other people's runs still need REPORT_MANAGE")
    need("BR-REPORT-RUNS", lr.get("x-ticvai-permission") == "REPORT_VIEW_VENUE",
         "listReportExecutions is not gated by REPORT_VIEW_VENUE")

    # -------------------------------------------------------------- BR-CONTRAST
    _, _, _, st, wdoc = op("setTheme")
    theme = (((wdoc.get("components") or {}).get("schemas") or {}).get("Theme") or {})
    pairs = theme.get("x-ticvai-contrast-pairs") or []
    need("BR-CONTRAST", bool(pairs), "Theme declares no x-ticvai-contrast-pairs")
    tprops = theme.get("properties") or {}
    comp = set(((tprops.get("componentColours") or {}).get("properties") or {}))
    for p in pairs:
        for side in ("foreground", "background"):
            name = str(p.get(side) or "")
            ok = name in tprops or (name.startswith("componentColours.") and name.split(".")[1] in comp | {"*"})
            need("BR-CONTRAST", ok, f"contrast pair names {name!r}, which Theme does not have")
        use, ratio = p.get("use"), float(p.get("ratio") or 0)
        need("BR-CONTRAST", use in WCAG_MIN and ratio >= WCAG_MIN.get(use, 99),
             f"contrast pair {p.get('foreground')} on {p.get('background')}: {use} at {ratio} is below WCAG AA")
    need("BR-CONTRAST", "4.5:1" in text(st) and "3:1" in text(st), "setTheme does not state the AA ratios")

    # -------------------------------------------------------------- BR-WO-CANCEL
    need("BR-WO-CANCEL", "work-recorded" in problem_types(op("cancelWorkOrder")[3]),
         "cancelWorkOrder does not refuse with work-recorded once labour time or a part is recorded")

    # -------------------------------------------------------------- BR-INCIDENT
    _, _, _, ui, mdoc = op("updateIncident")
    ub = props(mdoc, body_schema(ui))
    need("BR-INCIDENT", "escalate" in ub and "reason" in ub, "updateIncident takes no escalate or reason")
    need("BR-INCIDENT", "incident-transition-not-allowed" in problem_types(ui),
         "updateIncident does not refuse a transition outside the incident flow")
    st_inc = load("states/incident.yaml")
    tr = {(t.get("from"), t.get("to")) for t in st_inc.get("transitions") or []}
    need("BR-INCIDENT", ("closed", "underInvestigation") in tr, "states/incident.yaml has no reopen to investigating")
    need("BR-INCIDENT", ("underInvestigation", "actionRequired") not in tr,
         "states/incident.yaml still enters actionRequired (not in the 3 October flow)")

    # -------------------------------------------------------------- BR-FARE
    _, _, _, q, tdoc = op("quoteTransportFare")
    need("BR-FARE", "travelAt" in props(tdoc, body_schema(q)), "FareQuoteRequest has no travelAt")
    ft = props(tdoc, {"$ref": "#/components/schemas/FareTable"})
    need("BR-FARE", "upcoming" in ft and "effectiveTo" in ft, "FareTable has no upcoming version or effectiveTo")

    # -------------------------------------------------------------- BR-SESSIONS-DOOR
    for oid in ("listActiveSessions", "forceLogout"):
        o = op(oid)[3]
        need("BR-SESSIONS-DOOR", {} in (o.get("security") or []), f"{oid} does not admit a call with no session")
        need("BR-SESSIONS-DOOR", bool(o.get("x-ticvai-step-up-carrier")), f"{oid} carries no supervisor step-up")

    # -------------------------------------------------------------- BR-ATTENDANCE
    _, _, _, ra, adoc = op("recordAttendance")
    need("BR-ATTENDANCE", ra.get("x-ticvai-self-scoped") == "principal", "recordAttendance is not self-scoped")
    need("BR-ATTENDANCE", not ({"principalId", "employeeId", "staffPrincipalId"} & set(props(adoc, body_schema(ra)))),
         "recordAttendance takes a person in its body")
    need("BR-ATTENDANCE", op("amendAttendance")[3].get("x-ticvai-permission") == "WORKFORCE_MANAGE",
         "amendAttendance is not the supervisor's (WORKFORCE_MANAGE)")

    # -------------------------------------------------------------- BR-AI-CURRENCY
    ai = (ROOT / "contracts/satellite/ai.yaml").read_text(encoding="utf-8")
    need("BR-AI-CURRENCY", not re.search(r"USD by default|default USD|, USD by default", ai),
         "ai.yaml still defaults the spend ceiling to USD")
    need("BR-AI-CURRENCY", "billing currency" in text(op("setAiSpendCeiling")[3]),
         "setAiSpendCeiling does not default to the tenant's billing currency")

    # BR-ANALYTICS-PROVIDER, BR-MEDIA-COVER-USE, BR-AGENT-LAPSE, BR-MEDIA-REPLACE-UPLOAD (r11, ADAM CR-323, CR-326,
    # CR-333, CR-337; the lead, 29 October 2026, "As recommended"). Each fails on the r10 contract and passes on the
    # decision.
    _, _, _, sap, wl = op("setAnalyticsProvider")
    sap_s = (((wl.get("components") or {}).get("schemas") or {}).get("StorefrontAnalyticsProvider") or {})
    need("BR-ANALYTICS-PROVIDER", ["venueId", "provider"] in (sap_s.get("x-ticvai-unique-together") or [])
         and str(sap_s.get("x-ticvai-unique-nulls") or "") == "not-distinct",
         "StorefrontAnalyticsProvider is not unique on (venueId, provider) with nulls not distinct (CR-323 (1))")
    sap_d = " ".join(str(sap.get("description") or "").split())
    need("BR-ANALYTICS-PROVIDER", "leaves `reportingCredentialRef` out keeps" in sap_d and "explicit `null` clears" in sap_d,
         "setAnalyticsProvider does not say a PUT leaving reportingCredentialRef out keeps it and null clears it "
         "(CR-323 (2))")
    need("BR-ANALYTICS-PROVIDER", "analytics_provider_venue_id_provider_uniq" in
         json.dumps(((sap.get("responses") or {}).get("409") or {}), default=str),
         "setAnalyticsProvider's 409 does not name the unique index analytics_provider_venue_id_provider_uniq (CR-323 (1))")
    _, _, _, dma, adoc = op("deleteMediaAsset")
    asch = (adoc.get("components") or {}).get("schemas") or {}
    surf = set((((asch.get("MediaUsage") or {}).get("properties") or {}).get("surface") or {}).get("enum") or [])
    need("BR-MEDIA-COVER-USE", "mediaCollectionCover" in surf,
         "MediaUsage.surface cannot name a collection cover (mediaCollectionCover; CR-326)")
    need("BR-MEDIA-COVER-USE", "assets.media_collection" in text(dma.get("x-ticvai-reads") or [])
         and "mediaCollectionCover" in str(dma.get("description") or ""),
         "deleteMediaAsset does not read assets.media_collection and name a cover as mediaCollectionCover (CR-326)")
    saa = " ".join(str(op("setAgentAvailability")[3].get("description") or "").split())
    need("BR-AGENT-LAPSE", "Session.expiresAt" in saa and "heartbeat lapse" in saa and "reads as `offline`" in saa,
         "setAgentAvailability does not say expiresAt is the earlier of the session's expiry and a heartbeat lapse, "
         "and that a lapsed state reads as offline (CR-333)")
    rma = op("replaceMediaAsset")[3]
    rma_d = " ".join(str(rma.get("description") or "").split())
    refused = set(((props(adoc, {"$ref": "#/components/schemas/UploadRefusedProblem"}).get("refusedReason") or {})
                   .get("enum") or []))
    need("BR-MEDIA-REPLACE-UPLOAD", "uploadAlreadyUsed" in refused and "upload-already-used" in problem_types(rma),
         "replaceMediaAsset does not refuse an upload already used (409 upload-already-used, refusedReason "
         "uploadAlreadyUsed; CR-337)")
    need("BR-MEDIA-REPLACE-UPLOAD", "assets.asset_version" in text(rma.get("x-ticvai-reads") or [])
         and "answers `200` with the asset unchanged" in rma_d and "whose key no `asset_version` row names" in rma_d,
         "replaceMediaAsset does not say where the replaced file's storageKey comes from, or that a retry with the "
         "current upload answers 200 unchanged (CR-337)")

    # -------------------------------------------------------------- BR-QR
    cred = op("getEntitlementCredential")[3]
    rot = (((((cred.get("responses") or {}).get("200") or {}).get("content") or {}).get("application/json") or {})
           .get("schema") or {}).get("properties", {}).get("rotation") or {}
    step = (rot.get("properties") or {}).get("timeStepSeconds") or {}
    need("BR-QR", step.get("default") == 30 and "30 seconds" in str(step.get("description") or ""),
         "getEntitlementCredential rotation.timeStepSeconds is not 30 seconds by decision (GST-055)")

    # -------------------------------------------------------------- BR-NEW-OPS
    for oid in ("listMyTableReservations", "listBookableOutlets", "uploadIncidentMedia", "addIncidentPerson"):
        need("BR-NEW-OPS", oid in ops, f"{oid} is missing")
    if "listMyTableReservations" in ops:
        o = ops["listMyTableReservations"][3]
        need("BR-NEW-OPS", o.get("x-ticvai-self-scoped") == "subject", "listMyTableReservations is not self-scoped")
    for oid in ("listMyTableReservations", "listBookableOutlets"):
        if oid in ops:
            names = {str(p.get("$ref", "")).rsplit("/", 1)[-1] for p in ops[oid][3].get("parameters") or []}
            need("BR-NEW-OPS", "PageCursor" in names, f"{oid} is a list with no paging")
    if "listBookableOutlets" in ops:
        need("BR-NEW-OPS", {} in (ops["listBookableOutlets"][3].get("security") or []),
             "listBookableOutlets is not readable before sign-in")
    if "addIncidentPerson" in ops:
        need("BR-NEW-OPS", "consent" in text(ops["addIncidentPerson"][3]).lower(),
             "addIncidentPerson does not apply the consent rules")

    # ============================================== the rules decided for the CRs of 18 October 2026 (CHG-CRA-007)
    # Class 9 of the 18 October triage, "rules nobody has decided yet": each operation depended on a rule the package
    # never stated, so a developer could not build it. The lead decided each; the contract now states it, with any
    # proposed default marked for the client to correct. One rule per decision, as above.

    # -------------------------------------------------------------- BR-GUEST-PII (ADAM CR-141)
    f, _, _, sg, doc = op("searchGuests")
    gp = ((doc.get("components") or {}).get("schemas") or {}).get("GuestProfile") or {}
    personal = {"displayName", "email", "phone", "preferredLanguage", "preferredChannel", "guestLinkId"}
    for p, ps in (gp.get("properties") or {}).items():
        cls = (ps or {}).get("x-ticvai-data-class")
        need("BR-GUEST-PII", cls in ("personal", "behavioural"),
             f"GuestProfile.{p} is not marked personal or behavioural (x-ticvai-data-class)")
        if p in personal:
            need("BR-GUEST-PII", cls == "personal", f"GuestProfile.{p} is personal data (CR-141) and not marked so")
    st = text(sg)
    need("BR-GUEST-PII", "superseded_at" in st and "granted" in st,
         "searchGuests does not state hasConsentFor's rule (the current consent record, decision granted)")
    need("BR-GUEST-PII", "ordered by `id`" in st or "ordered by id" in st,
         "searchGuests does not order by id for a caller without GUEST_VIEW_PII")
    need("BR-GUEST-PII", "lifetimeValue" in st and "currency" in st,
         "searchGuests does not say lifetimeValue is left out until it has a currency (CR-094's rule)")

    # -------------------------------------------------------------- BR-HOST-ROUTING (ADAM CR-162)
    rt = text(op("resolveTenantHost")[3])
    for frag, why in (("308", "the redirect status"), ("terminated", "a terminated tenant answers 404"),
                      ("draining", "which cell_tenant databases are opened"),
                      ("verifiedAt", "a platform subdomain is written verified at provisioning"),
                      ("informational", "tenant_domain.database_name is informational")):
        need("BR-HOST-ROUTING", frag in rt, f"resolveTenantHost does not state {why} ({frag!r})")

    # -------------------------------------------------------------- BR-CASH-RECEIPT (ADAM CR-168)
    fin = load("contracts/spine/finance.yaml")
    fs = (fin.get("components") or {}).get("schemas") or {}
    need("BR-CASH-RECEIPT", "payment" in ((fs.get("JournalSource") or {}).get("enum") or []),
         "JournalSource has no `payment`: a cash receipt would read as revenue")
    need("BR-CASH-RECEIPT", "scopePath" in ((fs.get("AccountMapping") or {}).get("properties") or {}),
         "AccountMapping has no scopePath: a region's mapping cannot be found")
    je = fs.get("JournalEntry") or {}
    need("BR-CASH-RECEIPT", ["legalEntityId", "entryNumber"] in (je.get("x-ticvai-unique-together") or [])
         and not (((je.get("properties") or {}).get("entryNumber") or {}).get("x-ticvai-unique")),
         "JournalEntry.entryNumber is not unique per legal entity (x-ticvai-unique-together legalEntityId, entryNumber)")
    cp = op("createPayment")[3]
    need("BR-CASH-RECEIPT", "next open period" in text(cp),
         "createPayment does not post a capture to the legal entity's next open period")
    vias = {str(v.get("query")) for v in cp.get("x-ticvai-read-via") or [] if isinstance(v, dict)}
    need("BR-CASH-RECEIPT", {"tenancy#venueSettingsRecords", "tenancy#regionSettingsRecords"} <= vias,
         "createPayment does not declare its reads of venue and region settings")

    # -------------------------------------------------------------- BR-HOLD-LAPSE (ADAM CR-169)
    seat = load("contracts/satellite/seating.yaml")
    sh = ((seat.get("components") or {}).get("schemas") or {}).get("SeatHold") or {}
    shp = sh.get("properties") or {}
    need("BR-HOLD-LAPSE", "sold" in ((shp.get("status") or {}).get("enum") or []),
         "SeatHold.status has no `sold`")
    need("BR-HOLD-LAPSE", "inventoryReservationId" in shp, "SeatHold names no inventory reservation")
    ct = text(op("convertInventoryHold")[3])
    need("BR-HOLD-LAPSE", "unitsGone" in ct and "refunded automatically" in ct,
         "convertInventoryHold does not state the lapsed-hold rule (units retaken, else unitsGone; no automatic refund)")
    need("BR-HOLD-LAPSE", "channel_envelope" in ct, "convertInventoryHold does not move the envelope's leased units")

    # -------------------------------------------------------------- BR-LOGIN-ATTEMPTS (ADAM CR-170; CHG-CRA-009)
    # Decided by Chinmay Parab on 19 October 2026, option D: the door says how many attempts are left on every 401,
    # counted per submitted username so nothing reveals which usernames exist; the 409 says since when and on what.
    idoc = load("contracts/spine/identity.yaml")
    ids = (idoc.get("components") or {}).get("schemas") or {}

    def ext(name, field):
        sch = ids.get(name) or {}
        return any(field in ((part or {}).get("properties") or {}) for part in sch.get("allOf") or [])

    lg = op("login")[3]
    r401 = text((lg.get("responses") or {}).get("401") or {})
    need("BR-LOGIN-ATTEMPTS", "LoginDeniedProblem" in r401 and ext("LoginDeniedProblem", "attemptsRemaining"),
         "login's 401 does not carry attemptsRemaining (LoginDeniedProblem)")
    need("BR-LOGIN-ATTEMPTS", "whether or not a principal has it" in r401,
         "login's 401 does not count attempts per submitted username, known or not")
    # Fix round 3 (lane-H review 2 M-5): "every 401" is every 401 login and verifyMfaChallenge return, and the
    # unknown username's counter is per sign-in method as a known one's lock is.
    # Narrowed by the lead on 20 October 2026 (CHG-R8DEC-001): every wrong-credentials 401, never sso-sign-in-required,
    # which checks no credential. LoginDeniedProblem serves both problem types, so the field is not `required` there and
    # the contract says where it is present and where it is not.
    ldp = text(ids.get("LoginDeniedProblem") or {})
    need("BR-LOGIN-ATTEMPTS", "`unauthenticated`" in ldp and "Not on `sso-sign-in-required`" in ldp,
         "LoginDeniedProblem does not say attemptsRemaining is on every unauthenticated 401 and not on "
         "sso-sign-in-required (CHG-R8DEC-001)")
    need("BR-LOGIN-ATTEMPTS", "does not carry `attemptsRemaining`" in r401 and "carries the count as it stands" not in r401,
         "login's 401 does not say sso-sign-in-required leaves attemptsRemaining out (CHG-R8DEC-001)")
    need("BR-LOGIN-ATTEMPTS", "per sign-in method" in r401,
         "login's 401 does not count attempts per sign-in method as well as per username")
    need("BR-LOGIN-ATTEMPTS", "SessionHeldProblem" in text((lg.get("responses") or {}).get("409") or {})
         and ext("SessionHeldProblem", "openedAt") and ext("SessionHeldProblem", "deviceLabel"),
         "login's 409 does not say since when and on what (SessionHeldProblem openedAt, deviceLabel)")
    need("BR-LOGIN-ATTEMPTS", "credential-locked" in text((lg.get("responses") or {}).get("429") or {}),
         "login's lock is not 429 credential-locked")
    vm = op("verifyMfaChallenge")[3]
    need("BR-LOGIN-ATTEMPTS", "MfaCodeInvalidProblem" in text((vm.get("responses") or {}).get("422") or {})
         and ext("MfaCodeInvalidProblem", "attemptsRemaining"),
         "verifyMfaChallenge's 422 does not carry attemptsRemaining")
    # Narrowed on 20 October 2026 (CHG-R8DEC-001): a missing or expired challenge session is not a wrong credential.
    vm401 = text((vm.get("responses") or {}).get("401") or {})
    need("BR-LOGIN-ATTEMPTS", "MfaCodeInvalidProblem" not in vm401 and "does not carry `attemptsRemaining`" in vm401,
         "verifyMfaChallenge's 401 carries attemptsRemaining or does not say it does not (a missing or expired challenge "
         "session is not a wrong credential, CHG-R8DEC-001)")

    # -------------------------------------------------------------- BR-GATE-CANCEL (ADAM CR-171; CHG-CRA-010)
    # Decided by Chinmay Parab on 19 October 2026, option B: a cancelled gate mode change records who, when and why
    # in its own columns, and the scheduler's changedBy, changedAt and reason are left untouched.
    adoc = load("contracts/spine/access.yaml")
    gm = (((adoc.get("components") or {}).get("schemas") or {}).get("AccessGateModeChange") or {}).get("properties") or {}
    for fld in ("cancelledByPrincipalId", "cancelledAt", "cancelReason"):
        need("BR-GATE-CANCEL", fld in gm, f"AccessGateModeChange has no {fld}")
    need("BR-GATE-CANCEL", (gm.get("cancelReason") or {}).get("maxLength") == 200,
         "AccessGateModeChange.cancelReason is not at most 200 characters")
    need("BR-GATE-CANCEL", "left as they were" in text(op("cancelGateModeChange")[3]),
         "cancelGateModeChange does not leave the scheduler's columns untouched")

    # -------------------------------------------------------------- BR-APPROVED-OUTCOME (CHG-R8DEC-002)
    # Decided by Chinmay Parab on 20 October 2026, option A: approvals.approved_action_execution was "updated by the
    # requesting contract as it executes" with no operation or event able to write it. One internal operation is that
    # writer, and the contracts that apply a grant say they call it.
    ro = op("recordApprovedActionOutcome")
    need("BR-APPROVED-OUTCOME", ro[0] is not None and ro[0].stem == "approvals",
         "approvals has no recordApprovedActionOutcome (the writer of an approved action's outcome)")
    if ro[0] is not None:
        o = ro[3]
        need("BR-APPROVED-OUTCOME", o.get("x-ticvai-audience") == ["service"] and o.get("x-ticvai-auth") == "service"
             and {"serviceAuth": []} in (o.get("security") or []),
             "recordApprovedActionOutcome is not service-only (audience service, x-ticvai-auth service, serviceAuth)")
        oc = props(ro[4], body_schema(o)).get("outcome") or {}
        need("BR-APPROVED-OUTCOME", set(oc.get("enum") or []) == {"applied", "notApplied", "noOp"},
             "recordApprovedActionOutcome's outcome is not applied, notApplied or noOp")
        need("BR-APPROVED-OUTCOME", "ApprovedActionExecutionView" in text((o.get("responses") or {}).get("200") or {}),
             "recordApprovedActionOutcome does not return the execution (ApprovedActionExecutionView)")
    lin_ = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    need("BR-APPROVED-OUTCOME", "approvals.approved_action_execution"
         in ((lin_.get("recordApprovedActionOutcome") or {}).get("writes") or []),
         "the lineage does not have recordApprovedActionOutcome write approvals.approved_action_execution")
    for oid in ("suspendTenant", "reactivateTenant"):
        need("BR-APPROVED-OUTCOME", "recordApprovedActionOutcome" in text(op(oid)[3]),
             f"{oid}'s grant consumer does not record its outcome through recordApprovedActionOutcome")

    # -------------------------------------------------------------- r8 second round (core lane's requests, CHG-R8GEN-013)
    # BR-APPROVAL-ROUTE (CHG-R8SPN-016): a matrix condition the engine cannot evaluate is refused when it is saved, and a
    # submission that no longer needs approval, or finds no approver, says so with its own problem type.
    for oid in ("setApprovalMatrix", "approveMatrixMultiLevel"):
        need("BR-APPROVAL-ROUTE", "condition-invalid" in problem_types(op(oid)[3]),
             f"{oid} does not refuse a condition the engine cannot evaluate (422 condition-invalid)")
    sub409 = text(((op("submitApprovalRequest")[3].get("responses") or {}).get("409")) or {})
    for pt in ("approval-no-longer-required", "approval-no-approver-available"):
        need("BR-APPROVAL-ROUTE", pt in sub409, f"submitApprovalRequest's 409 does not list {pt}")
    # BR-APPROVAL-ENGINE (ADAM CR-102, CHG-R10ID-015): every engine rule the CR named has a place to live.
    adoc = op("decideApprovalRequest")[4]
    asch = ((adoc.get("components") or {}).get("schemas") or {})
    rule_s = asch.get("ApprovalRule") or {}
    cond = text((rule_s.get("properties") or {}).get("condition") or {})
    need("BR-APPROVAL-ENGINE", " AND " in cond and "notIn" in cond and "unreachableRule" in cond,
         "ApprovalRule.condition does not define the condition language (AND-joined clauses, operators) and the "
         "unreachableRule comparison")
    # Per version since ADAM CR-300, option B (CHG-CR300-001): a version repeats its rules' codes, so CR-102's "no
    # duplicate code within one rule set" is (matrix_id, matrix_version, code).
    need("BR-APPROVAL-ENGINE", ["matrix_id", "matrixVersion", "code"] in (rule_s.get("x-ticvai-unique-together") or []),
         "ApprovalRule has no unique (matrix_id, matrix_version, code)")
    need("BR-APPROVAL-ENGINE", "version" in ((asch.get("ApprovalMatrix") or {}).get("required") or []),
         "ApprovalMatrix.version is not required (a matrix version may be null)")
    req_s = asch.get("ApprovalRequest") or {}
    need("BR-APPROVAL-ENGINE", "approvals.request_approver" in str(req_s.get("x-ticvai-persistence") or "")
         and "approvers" in (req_s.get("properties") or {}),
         "ApprovalRequest does not store its approver chain (approvers[], approvals.request_approver)")
    dec = (((asch.get("ApprovalDecision") or {}).get("properties") or {}).get("decision") or {}).get("enum") or []
    need("BR-APPROVAL-ENGINE", {"return", "requestInformation"} <= set(dec),
         "ApprovalDecision.decision cannot store return and requestInformation")
    for oid in ("approveMatrixMultiLevel", "approveRoleAuthorityDelegation"):
        codes = {str(k) for k in (op(oid)[3].get("responses") or {})}
        need("BR-APPROVAL-ENGINE", {"400", "409"} <= codes, f"{oid} does not declare its 400 and 409 refusals")
    for oid in ("createApprovalDelegation", "approveRoleAuthorityDelegation"):
        r403 = text(((op(oid)[3].get("responses") or {}).get("403")) or {})
        need("BR-APPROVAL-ENGINE", "exceeds-delegator-authority" in r403,
             f"{oid} does not refuse exceedsDelegatorAuthority with 403")
    # BR-APPROVAL-VERSIONS (ADAM CR-300, option B; CHG-CR300-001): one matrix row with a stable id, its versions in a
    # table of their own, each rule naming its version, and the two unique keys.
    mv = asch.get("ApprovalMatrixVersion") or {}
    need("BR-APPROVAL-VERSIONS", str(mv.get("x-ticvai-persistence") or "") == "approvals.matrix_version"
         and (mv.get("x-ticvai-primary-key") or []) == ["approvalMatrixId", "version"]
         and ((mv.get("properties") or {}).get("approvalMatrixId") or {}).get("x-ticvai-references") == "approvals.matrix",
         "no approvals.matrix_version keyed (approvalMatrixId, version) and referencing approvals.matrix (ApprovalMatrixVersion)")
    need("BR-APPROVAL-VERSIONS", "matrixVersion" in (rule_s.get("properties") or {})
         and "matrixVersion" in (rule_s.get("required") or []),
         "ApprovalRule does not name its matrix version (a required matrixVersion, approvals.rule.matrix_version)")
    need("BR-APPROVAL-VERSIONS", ["kind", "scopePath"] in ((asch.get("ApprovalMatrix") or {}).get("x-ticvai-unique-together")
                                                          or []),
         "ApprovalMatrix has no unique (kind, scopePath): two first saves can make two matrices for one kind and scope")
    need("BR-APPROVAL-VERSIONS", "approvals.matrix_version" in text(op("setApprovalMatrix")[3].get("x-ticvai-writes") or []),
         "setApprovalMatrix does not write approvals.matrix_version (x-ticvai-writes)")
    # BR-BILLING-STATEMENT (ADAM CR-303, option A; CHG-CR303-001): the cycle, its charges, the v5 namespace and name,
    # and the subject are stated, and both statement operations mint the id by the one rule.
    odoc = op("listBillingStatements")[4]
    bs_id = text((((((odoc.get("components") or {}).get("schemas") or {}).get("BillingStatement") or {})
                   .get("properties") or {}).get("id")) or {})
    need("BR-BILLING-STATEMENT", bool(re.search(r"namespace `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}`",
                                                bs_id)) and "<agreementId>|<periodStart>|<periodEnd>" in bs_id,
         "BillingStatement.id does not state its v5 namespace uuid and the name <agreementId>|<periodStart>|<periodEnd>")
    lbs = text(op("listBillingStatements")[3])
    for word in ("orders.membership_renewal", "completed", "source_order_id", "customer_id", "regionSettingsRecords"):
        need("BR-BILLING-STATEMENT", word in lbs, f"listBillingStatements does not state the cycle rule ({word})")
    for oid in ("listBillingStatements", "getBillingStatement"):
        need("BR-BILLING-STATEMENT", "BillingStatement.id" in text(op(oid)[3]),
             f"{oid} does not mint the statement id by BillingStatement.id's rule")
    # BR-STORE-CHECKLIST (ADAM CR-304, option A; CHG-CR304-001): every checklist item has its done-rule and its copy,
    # the listing languages are named, and the Pass Type ID is one per tenant.
    wdoc = op("setStoreAccounts")[4]
    wsch = ((wdoc.get("components") or {}).get("schemas") or {})
    chk = wsch.get("StorePublishingChecklist") or {}
    item_p = ((((chk.get("properties") or {}).get("items") or {}).get("items") or {}).get("properties") or {})
    items_ = (item_p.get("item") or {}).get("enum") or []
    rules_t = str(chk.get("description") or "")
    copy_t = str((item_p.get("guidance") or {}).get("description") or "")
    for it in items_:
        need("BR-STORE-CHECKLIST", f"- `{it}`:" in rules_t, f"StorePublishingChecklist states no done-rule for {it}")
        need("BR-STORE-CHECKLIST", f"`{it}`: \"" in copy_t, f"StorePublishingChecklist.guidance lists no copy for {it}")
    need("BR-STORE-CHECKLIST", "is_draft" in text(op("setStoreAccounts")[3]),
         "setStoreAccounts does not say which tenant languages a listing is checked against (the working draft's)")
    ptid = text(((wsch.get("StoreAccount") or {}).get("properties") or {}).get("passTypeIdentifier") or {})
    need("BR-STORE-CHECKLIST", "one per tenant" in ptid and "one per brand" not in ptid,
         "StoreAccount.passTypeIdentifier is not one per tenant (CR-304)")
    # BR-PRIVACY-REQUEST (ADAM CR-101, CHG-R10ID-016): a guest's privacy request is recorded, clocked and readable.
    need("BR-PRIVACY-REQUEST", ["requestedByPrincipalId", "requestedBySubjectId"]
         in (req_s.get("x-ticvai-exactly-one-of") or []),
         "ApprovalRequest does not record a guest requester (exactly one of requestedByPrincipalId, requestedBySubjectId)")
    for oid in ("exportSubjectData", "deleteGuestAccount"):
        need("BR-PRIVACY-REQUEST", "identity.privacyRequestRaised" in (op(oid)[3].get("x-ticvai-emits") or []),
             f"{oid} does not put the request into the privacy queue (x-ticvai-emits identity.privacyRequestRaised)")
    need("BR-PRIVACY-REQUEST", "subject-erased" in problem_types(op("exportSubjectData")[3]),
         "exportSubjectData does not answer an erased subject (410 subject-erased)")
    need("BR-PRIVACY-REQUEST", bool(op("getSubjectDataExport")[3]),
         "no status and download read of a data export (getSubjectDataExport)")
    ev = ROOT / "events" / "identity-privacyRequestRaised.yaml"
    evd = yaml.safe_load(ev.read_text(encoding="utf-8")) if ev.exists() else {}
    need("BR-PRIVACY-REQUEST", any((c or {}).get("context") == "marketing" for c in (evd or {}).get("consumers") or []),
         "identity.privacyRequestRaised has no Marketing consumer (the privacy queue)")
    # r10 round 3 (CHG-R10ID-024): the jurisdiction travels, the case carries the request id, the file expires.
    need("BR-PRIVACY-REQUEST", any((x or {}).get("field") == "jurisdiction" for x in (evd or {}).get("payload") or []),
         "identity.privacyRequestRaised carries no jurisdiction (the venue's country)")
    mdoc = load("contracts/satellite/marketing-crm.yaml")
    pr = ((mdoc.get("components") or {}).get("schemas") or {}).get("DataSubjectCustomerPrivacyRequestManagementView") or {}
    need("BR-PRIVACY-REQUEST", "approvalRequestId" in (pr.get("properties") or {}),
         "the privacy case does not carry the request id (approvalRequestId)")
    sde = ((load("contracts/spine/identity.yaml").get("components") or {}).get("schemas") or {}).get("SubjectDataExport") or {}
    need("BR-PRIVACY-REQUEST", "expired" in (((sde.get("properties") or {}).get("status") or {}).get("enum") or [])
         and "7 days" in str(sde.get("description")), "a data export file has no stated keeping period (7 days)")
    # BR-PLATFORM-INVOICE (r10 round 3, ADAM CR-202; CHG-R10ID-023): who issues, at what tax rate, and a cancelled
    # invoice frees its period.
    sub = load("contracts/satellite/subscription.yaml")
    ssch = (sub.get("components") or {}).get("schemas") or {}
    need("BR-PLATFORM-INVOICE", "issuingLegalEntity" in ((ssch.get("Subscription") or {}).get("properties") or {}),
         "the contract names no issuing legal entity")
    need("BR-PLATFORM-INVOICE", (ssch.get("PlatformTaxRate") or {}).get("x-ticvai-persistence") == "control.platform_tax_rate",
         "no platform tax-rate table")
    uw = (ssch.get("SubscriptionInvoice") or {}).get("x-ticvai-unique-when") or []
    need("BR-PLATFORM-INVOICE", any("cancelled" in str(u.get("when")) for u in uw if isinstance(u, dict)),
         "the exact-period unique index does not skip cancelled invoices")
    # BR-SCOPE-AUTHZ (ADAM CR-189, CHG-R10ID-001): the per-scope rule, stated once, and its two first users.
    idoc = load("contracts/spine/identity.yaml")
    isch = (idoc.get("components") or {}).get("schemas") or {}
    pbs = json.dumps(((isch.get("Session") or {}).get("properties") or {}).get("permissionsByScope") or {})
    need("BR-SCOPE-AUTHZ", "CR-189" in pbs and "scope the operation acts on" in pbs,
         "Session.permissionsByScope does not state the per-scope rule (CR-189)")
    spec = (ROOT / "docs" / "architecture" / "specs" / "permission-resolution.md").read_text(encoding="utf-8")
    need("BR-SCOPE-AUTHZ", "CR-189" in spec and "#27692" in spec and "#27666" in spec,
         "permission-resolution 7.2 does not state the per-scope rule with its seam (#27692) and fill (#27666)")
    need("BR-SCOPE-AUTHZ", "per-scope set" in text(op("listPrincipals")[3]),
         "listPrincipals does not read its reach from the per-scope set")
    cr = op("createRole")[3]
    need("BR-SCOPE-AUTHZ", "tenant root" in text(cr) and "403" in {str(k) for k in (cr.get("responses") or {})},
         "createRole does not need ROLE_MANAGE at the tenant root with a 403")
    # BR-SSO-ACTIVE (ADAM CR-190, CHG-R10ID-002)
    sso = text(op("listSsoProviders")[3])
    need("BR-SSO-ACTIVE", "is_active" in sso and "null" in sso and "displayName" in sso,
         "listSsoProviders does not state the active-only filter (null is not active) and its order")
    # BR-PERMISSION-FINDINGS (ADAM CR-210, CHG-R10ID-003)
    pf = text(op("listPermissionFindings")[3])
    need("BR-PERMISSION-FINDINGS", "50%" in pf and "25%" in pf and "access_decision" in pf,
         "listPermissionFindings does not state the peer thresholds and the usage source")
    need("BR-PERMISSION-FINDINGS", "then `name`" in text(op("listCapabilityTemplates")[3]),
         "listCapabilityTemplates states no full order")
    need("BR-PERMISSION-FINDINGS", "`certify`" in text(op("listAccessReviewItems")[3]),
         "listAccessReviewItems does not place review and certify in its order")
    # BR-ENTITLEMENT-SHARE (ADAM CR-209, CHG-R10ID-004)
    da = (isch.get("DelegatedAccess") or {}).get("properties") or {}
    need("BR-ENTITLEMENT-SHARE", "sharedEntitlement" in ((da.get("delegationKind") or {}).get("enum") or []),
         "DelegatedAccess.delegationKind has no sharedEntitlement")
    need("BR-ENTITLEMENT-SHARE", "ENTITLEMENT_USE" in ((load("contracts/shared/permissions.yaml")
                                                        .get("x-ticvai-share-only") or {}).get("permissions") or []),
         "ENTITLEMENT_USE is not kept off role checklists (x-ticvai-share-only; r10 round 3)")
    need("BR-ENTITLEMENT-SHARE", "revokedBySubjectId" in da and "revokedByKind" in da,
         "DelegatedAccess cannot record a guest's revoke (revokedByKind, revokedBySubjectId)")
    res = op("revokeEntitlementShare")[3]
    need("BR-ENTITLEMENT-SHARE", "404" in {str(k) for k in (res.get("responses") or {})} and "over_object_ref" in text(res),
         "revokeEntitlementShare does not match the share to its entitlement (404)")
    # BR-PRESET-READONLY (ADAM CR-176, CHG-R10ID-005)
    need("BR-PRESET-READONLY", "capability-template-is-preset" in problem_types(op("setCapabilityTemplate")[3]),
         "setCapabilityTemplate does not refuse a preset's id")
    # BR-END-SESSIONS (ADAM CR-180, CHG-R10ID-006)
    need("BR-END-SESSIONS", "identity.end_principal_sessions" in text(op("updatePrincipal")[3]),
         "updatePrincipal does not end sessions through identity.end_principal_sessions")
    need("BR-END-SESSIONS", "FUNCTION identity.end_principal_sessions" in
         (ROOT / "tools" / "derive-ddl.py").read_text(encoding="utf-8"),
         "tools/derive-ddl.py does not write identity.end_principal_sessions")
    # BR-PLATFORM-TOKEN (ADAM CR-175, CHG-R10ID-007)
    need("BR-PLATFORM-TOKEN", any((ROOT / "docs" / "adr").glob("0072-*.md")), "ADR-0072 (the platform token) is missing")
    need("BR-PLATFORM-TOKEN", "ADR-0072" in text(op("openPlatformStaffGrant")[3]),
         "openPlatformStaffGrant does not cite ADR-0072")
    sdoc = load("contracts/satellite/subscription.yaml")
    persisted = {str(v.get("x-ticvai-persistence")) for v in ((sdoc.get("components") or {}).get("schemas") or {}).values()
                 if isinstance(v, dict)}
    for t in ("control.platform_operator", "control.platform_session", "control.platform_operator_mfa"):
        need("BR-PLATFORM-TOKEN", t in persisted, f"no schema persists {t} (ADR-0072)")
    # BR-GUEST-TOKENS (ADAM CR-100, CHG-R10ID-009)
    ggs = json.dumps(((op("getGuestSession")[3].get("responses") or {}).get("200") or {}))
    view = (isch.get("GuestSessionView") or {})
    need("BR-GUEST-TOKENS", "GuestSessionView" in ggs and "tokens" not in (view.get("properties") or {}),
         "getGuestSession answers a session with tokens, so a read must issue them")
    need("BR-GUEST-TOKENS", ["principalId", "subjectId"] in ((isch.get("IdentityRefreshToken") or {})
                                                              .get("x-ticvai-exactly-one-of") or []),
         "IdentityRefreshToken is not a principal's or a guest's (exactly one of principalId, subjectId)")
    # BR-GUEST-VENUE (ADAM CR-198, CHG-R10ID-010, general): a public guest read of venue data names its venue.
    cdoc = load("contracts/shared/common.yaml")
    ga = json.dumps(((cdoc.get("components") or {}).get("securitySchemes") or {}).get("guestAuth") or {})
    need("BR-GUEST-VENUE", "CR-198" in ga and "X-Venue-Id" in ga, "guestAuth does not state the venue rule (CR-198)")
    for oid, (f, path, method, o, d) in sorted(ops.items()):
        sec = o.get("security")
        if method != "get" or sec is None or not (sec == [] or any(x == {} for x in sec)):
            continue
        if not set(o.get("x-ticvai-audience") or []) & {"guest", "anonymous", "public"}:
            continue
        if o.get("x-ticvai-scope-level") != "venue" or oid in GUEST_VENUE_EXEMPT or "{venueId}" in path:
            continue
        item = ((d.get("paths") or {}).get(path) or {})
        params = (o.get("parameters") or []) + (item.get("parameters") or [])
        named = False
        for pp in params:
            if not isinstance(pp, dict):
                continue
            if str(pp.get("$ref", "")).endswith("/parameters/GuestVenue"):
                named = True
            if pp.get("name") == "venueId" and pp.get("in") == "query" and pp.get("required"):
                named = True
        need("BR-GUEST-VENUE", named, f"{oid} ({f.name}): a public guest read of venue data names no venue "
             "(declare common GuestVenue)")
        if any(str((pp or {}).get("$ref", "")).endswith("/parameters/GuestVenue") for pp in params if isinstance(pp, dict)):
            r400 = (o.get("responses") or {}).get("400") or {}
            need("BR-GUEST-VENUE", "venue-required" in str(r400) or "VenueRequired" in str(r400),
                 f"{oid} ({f.name}): declares GuestVenue but no 400 venue-required (r10 round 3, CHG-R10ID-022)")
    # BR-ALERT-RECIPIENT (CHG-R8SPN-020): reporting's listAlerts says whose alerts come back (the recipient role; an
    # over/short alert only to a holder of OVERSHORT_ACCEPT).
    la = next((o for oid, (f, _p, _m, o, _d) in ops.items() if oid == "listAlerts" and f.stem == "reporting"),
              op("listAlerts")[3])
    # Printed, not failed, until the surface lane's listAlerts text lands (r8 cause APPROVALS-TENANCY-C36): then move
    # it into `need` so the filter cannot be dropped again.
    if not ("OVERSHORT_ACCEPT" in text(la) and "recipient" in text(la).lower()):
        print("  WARN  BR-ALERT-RECIPIENT listAlerts does not yet state the recipient-role filter (OVERSHORT_ACCEPT for "
              "over/short alerts); surface lane, r8 cause APPROVALS-TENANCY-C36")
    # BR-GUEST-SELF-403 (CHG-R8SPN-018): a guest operation scoped to the caller's own subject answers someone else's
    # record with 404, never 403 (which would confirm it exists). A ratchet over the operations found on 20 October.
    self403 = sorted(oid for oid, (_f, _p, _m, o, _d) in ops.items()
                     if o.get("x-ticvai-self-scoped") == "subject" and "guest" in (o.get("x-ticvai-audience") or [])
                     and "403" in {str(k) for k in (o.get("responses") or {})})
    if len(self403) > GUEST_SELF_403_CEILING:
        need("BR-GUEST-SELF-403", False, f"{len(self403)} guest self-scoped operations declare 403, above the ceiling "
             f"of {GUEST_SELF_403_CEILING}: answer another subject's record 404 ({', '.join(self403[:8])})")

    # BR-WALLET-TOPUP-ONCE, BR-WALLET-PUBLISH-CHECKS, BR-WALLET-RESTORE-DRAFT (r11, ADAM CR-310, CR-311, CR-312; the
    # lead, 29 October 2026, "All as recommended"). Each fails on the r10 contract and passes on the decision.
    wdoc = load("contracts/satellite/wallet.yaml")
    wsch = (wdoc.get("components") or {}).get("schemas") or {}
    lot_line = ((wsch.get("CreditLot") or {}).get("properties") or {}).get("orderLineId") or {}
    need("BR-WALLET-TOPUP-ONCE", lot_line.get("x-ticvai-unique") == "tenant",
         "CreditLot.orderLineId carries no x-ticvai-unique: tenant, so no unique index stops two tills crediting one "
         "top-up line (CR-310)")
    top = op("topUpWallet")[3]
    t409 = json.dumps(((top.get("responses") or {}).get("409") or {}), default=str)
    need("BR-WALLET-TOPUP-ONCE", "payment-already-used" in t409 and "credit_lot_order_line_id_uniq" in t409,
         "topUpWallet's 409 does not say a unique violation on credit_lot_order_line_id_uniq is payment-already-used")
    pub = str(op("publishWalletConfiguration")[3].get("description") or "")
    for code in ("credit-type-without-accounting-mapping", "consumption-policy-names-retired-type"):
        need("BR-WALLET-PUBLISH-CHECKS", re.search(r"`" + code + r"` \(blocking\)", pub) is not None,
             f"publishWalletConfiguration does not list the check `{code}` as blocking (CR-311)")
    need("BR-WALLET-PUBLISH-CHECKS", "no warning" in " ".join(pub.split()),
         "publishWalletConfiguration does not say this release has no warning checks (CR-311, option B)")
    wcv = wsch.get("WalletConfigurationVersion") or {}
    need("BR-WALLET-PUBLISH-CHECKS", ["scopePath", "version"] in (wcv.get("x-ticvai-unique-together") or []),
         "WalletConfigurationVersion does not keep (scopePath, version) unique (CR-311)")
    res = op("restoreWalletConfigurationVersion")[3]
    rdesc = " ".join(str(res.get("description") or "").split())
    need("BR-WALLET-RESTORE-DRAFT", "writes no `wallet.configuration_version` row" in rdesc,
         "restoreWalletConfigurationVersion does not say it writes no configuration_version row (CR-312)")
    r409 = " ".join(str(((res.get("responses") or {}).get("409") or {}).get("description") or "").split())
    need("BR-WALLET-RESTORE-DRAFT", "latest published version" in r409 and "diffWalletConfigurationVersion" in r409,
         "restore's 409 unpublished-changes does not compare with the latest published snapshot as the diff does")
    need("BR-WALLET-RESTORE-DRAFT", ((wcv.get("properties") or {}).get("version") or {}).get("nullable") is True,
         "WalletConfigurationVersion.version is not nullable, so restore's draft answer cannot carry version null")
    lst = " ".join(str(op("listWalletConfigurationVersions")[3].get("description") or "").split())
    need("BR-WALLET-RESTORE-DRAFT", "drafts created by" not in lst,
         "listWalletConfigurationVersions still lists drafts created by the restore (CR-312: no draft row)")

    # BR-WALLET-RESTORE-FINDINGS, BR-WALLET-TOPUP-CREDIT-TYPE, BR-COOKIE-STRICTLY-NECESSARY, BR-ROTA-ROLE-DENY,
    # BR-FORM-VERSION-KEY (r12; the lead, 30 October 2026, "for each one actually check if they hold"; ADAM CR-355,
    # CR-357, CR-347, CR-344, CR-359). Each fails on the r11 contract and passes on the posted decision.
    for code in ("restore-credit-type-retired-since-version", "restore-left-newer-rows"):
        need("BR-WALLET-RESTORE-FINDINGS", re.search(r"`" + code + r"` \(warning", rdesc) is not None,
             f"restoreWalletConfigurationVersion does not list its finding `{code}` as a warning (CR-355)")
    need("BR-WALLET-RESTORE-FINDINGS", "never sets a credit type's `is_active` from false to true" in rdesc
         and "rather than silently revived" not in rdesc,
         "restoreWalletConfigurationVersion does not say a retired credit type stays retired (CR-355)")
    fcode = " ".join(str((((((wcv.get("properties") or {}).get("findings") or {}).get("items") or {})
                           .get("properties") or {}).get("code") or {}).get("description") or "").split())
    need("BR-WALLET-RESTORE-FINDINGS", "restoreWalletConfigurationVersion" in fcode,
         "WalletConfigurationVersion.findings[].code does not say where the restore's own codes are listed (CR-355)")
    tdesc = " ".join(str(top.get("description") or "").split())
    need("BR-WALLET-TOPUP-CREDIT-TYPE", "category `cash`" in tdesc and "bonusCreditTypeId" in tdesc
         and "`bonusAmount` is not paid for and is not compared" not in tdesc,
         "topUpWallet does not name each lot's credit type (the cash type, the bonus rule's bonusCreditTypeId) or "
         "still credits an unchecked bonusAmount (CR-357)")
    treads = text(top.get("x-ticvai-reads") or [])
    need("BR-WALLET-TOPUP-CREDIT-TYPE", "wallet.credit_type" in treads and "wallet.funding_rule" in treads,
         "topUpWallet does not declare its reads of wallet.credit_type and wallet.funding_rule (CR-357)")
    need("BR-WALLET-TOPUP-CREDIT-TYPE", "bonus-not-applicable" in str(((top.get("responses") or {}).get("422") or {})
                                                                     .get("x-ticvai-problem-types") or []),
         "topUpWallet's 422 does not name bonus-not-applicable (CR-357)")
    mdoc = load("contracts/satellite/marketing-crm.yaml")
    c422 = ((op("setCookieBannerDesign")[3].get("responses") or {}).get("422") or {})
    need("BR-COOKIE-STRICTLY-NECESSARY", "strictly-necessary-description-missing"
         in (c422.get("x-ticvai-problem-types") or []) and "`languages`" in str(c422.get("description") or ""),
         "setCookieBannerDesign's 422 does not name strictly-necessary-description-missing for a missing "
         "strictlyNecessary category or description in a language of `languages` (CR-347)")
    hq = (load("contracts/spine/identity.yaml").get("x-ticvai-queries") or {}).get("principalHoldsRoleAtVenue") or {}
    hrule = " ".join(str(hq.get("rule") or "").split())
    need("BR-ROTA-ROLE-DENY", "effect `DENY`" in hrule and "makes `holds` false" in hrule and "#32338" in hrule,
         "identity#principalHoldsRoleAtVenue does not let a live DENY of the role at or above the venue make holds "
         "false, or does not name #32338 as its builder (CR-344)")
    msch = (mdoc.get("components") or {}).get("schemas") or {}
    need("BR-FORM-VERSION-KEY", (msch.get("FormDefinition") or {}).get("x-ticvai-primary-key") == ["id", "version"],
         "FormDefinition is not keyed (id, version), so (formId, formVersion) names no row (CR-359)")
    for sname, prop, vprop in (("DynamicFieldsQuestionsConditionalLogicView", "formId", "formVersion"),
                               ("WaiverRequirement", "formDefinitionId", "formVersion"),
                               ("MarketingWaiverSignature", "templateId", "formVersion")):
        pp = (msch.get(sname) or {}).get("properties") or {}
        need("BR-FORM-VERSION-KEY", (pp.get(prop) or {}).get("x-ticvai-references") == "marketing.form_definition"
             and (pp.get(prop) or {}).get("x-ticvai-references-version") == vprop and vprop in pp,
             f"{sname}.{prop} does not reference marketing.form_definition by ({prop}, {vprop}) (CR-359)")
    cf = op("createForm")[3]
    cfq = [x for x in cf.get("parameters") or [] if isinstance(x, dict) and x.get("name") == "formId"]
    need("BR-FORM-VERSION-KEY", len(cfq) == 1 and cfq[0].get("in") == "query" and not cfq[0].get("required")
         and "404" in {str(k) for k in (cf.get("responses") or {})}
         and "highest version + 1" in " ".join(str(cf.get("description") or "").split()),
         "createForm takes no optional formId making the next version of an existing form (highest version + 1, "
         "404 when no form has that id) (CR-359, decided 31 October 2026)")

    # BR-PLANNER-QUESTIONS, BR-ROTA-HOUR-LIMIT, BR-ROTA-CROSS-VENUE (r11, ADAM CR-321, CR-334, CR-336; the lead, 29
    # October 2026, "As recommended", then "Include those in today as well"). Each fails on the r10 contract.
    vdoc = load("contracts/satellite/venue-map.yaml")
    vsch = (vdoc.get("components") or {}).get("schemas") or {}
    qkeys = (vsch.get("VisitPlannerQuestionKey") or {}).get("enum") or []
    need("BR-PLANNER-QUESTIONS", set(qkeys) == {"party", "heights", "dates", "dayVenues", "pace", "interests",
                                                 "retail", "cuisine"},
         "VisitPlannerQuestionKey is not the closed list of the questions the rules planner understands (CR-321)")
    vq = vsch.get("VisitPlannerQuestion") or {}
    need("BR-PLANNER-QUESTIONS", str(vq.get("x-ticvai-persistence") or "") == "venuemap.visit_planner_question"
         and {"isEnabled", "isRequired", "sortOrder", "label"} <= set(vq.get("properties") or {}),
         "no venuemap.visit_planner_question with isEnabled, isRequired, sortOrder and label (VisitPlannerQuestion)")
    for k in qkeys:
        need("BR-PLANNER-QUESTIONS", f"| `{k}` |" in str(vq.get("description") or ""),
             f"VisitPlannerQuestion states no default for {k}")
    need("BR-PLANNER-QUESTIONS", "questions" in ((vsch.get("VisitPlannerOptions") or {}).get("required") or []),
         "VisitPlannerOptions does not answer the venue's questions (questions), so the guest screens cannot read them")
    need("BR-PLANNER-QUESTIONS", "planner-question-fixed" in problem_types(op("setVisitPlannerQuestions")[3])
         and op("setVisitPlannerQuestions")[3].get("x-ticvai-permission") == "PRODUCT_CONFIGURE",
         "no staff write of the planner questions refusing party and dates switched off (setVisitPlannerQuestions)")
    gvp = op("generateVisitPlan")[3]
    need("BR-PLANNER-QUESTIONS", "planner-answer-missing" in problem_types(gvp)
         and "venuemap.visit_planner_question" in text(gvp.get("x-ticvai-reads") or []),
         "generateVisitPlan does not check the venue's required questions (422 planner-answer-missing, x-ticvai-reads)")
    wsch2 = (load("contracts/satellite/workforce.yaml").get("components") or {}).get("schemas") or {}
    bwl = " ".join(str((((wsch2.get("RotaAssignment") or {}).get("properties") or {})
                        .get("breachesWorkingHourLimit") or {}).get("description") or "").split())
    for word in ("workforce.staffing_rules", "maximumHoursPerDay", "maximumHoursPerWeek", "minimumRestHours",
                 "rolling"):
        need("BR-ROTA-HOUR-LIMIT", word in bwl, f"RotaAssignment.breachesWorkingHourLimit does not name its rule ({word})")
    for oid in ("createRotaAssignment", "updateRotaAssignment"):
        o_ = op(oid)[3]
        need("BR-ROTA-HOUR-LIMIT", "workforce.staffing_rules" in text(o_.get("x-ticvai-reads") or []),
             f"{oid} does not declare its read of the venue's working-hour limits (x-ticvai-reads workforce.staffing_rules)")
        rv = {str((r or {}).get("query")) for r in o_.get("x-ticvai-read-via") or []}
        for qn in ("workforce#principalHasOverlappingAssignment", "identity#principalHoldsRoleAtVenue"):
            need("BR-ROTA-CROSS-VENUE", qn in rv, f"{oid} does not ask {qn} (a yes or no beyond the caller's venue)")
        need("BR-ROTA-CROSS-VENUE", "identity#delegatedAccessRecords" not in rv,
             f"{oid} still reads identity.delegated_access under the caller's venue grant (delegatedAccessRecords)")
    for f_, qn, field in (("contracts/satellite/workforce.yaml", "principalHasOverlappingAssignment", "overlaps"),
                          ("contracts/spine/identity.yaml", "principalHoldsRoleAtVenue", "holds")):
        qd = (load(f_).get("x-ticvai-queries") or {}).get(qn) or {}
        rp = ((qd.get("returns") or {}).get("properties") or {})
        need("BR-ROTA-CROSS-VENUE", list(rp) == [field] and (rp.get(field) or {}).get("type") == "boolean"
             and "ITenantRootGrant" in str(qd.get("rule") or ""),
             f"{qn} does not answer only a boolean ({field}) under the tenant root grant (CR-336)")
    exc = (wsch2.get("RotaAssignment") or {}).get("x-ticvai-exclude") or []
    need("BR-ROTA-CROSS-VENUE", any((e or {}).get("equal") == ["principalId"]
                                    and (e or {}).get("during") == ["startsAt", "endsAt"] for e in exc),
         "RotaAssignment declares no exclusion constraint over principalId and [startsAt, endsAt) (x-ticvai-exclude)")
    # BR-CREDIT-ACCOUNT-CURRENCY, BR-PLATFORM-APPROVAL-RULE, BR-WALLET-ETAG-VERSION (r11, ADAM CR-322, CR-330, CR-332;
    # the lead, 29 October 2026, "As recommended", "Include those in today as well"). Each fails on the r10 contract.
    pdoc = load("contracts/satellite/payments.yaml")
    bca = ((pdoc.get("components") or {}).get("schemas") or {}).get("B2bCreditAccount") or {}
    bcur = (bca.get("properties") or {}).get("currencyCode") or {}
    need("BR-CREDIT-ACCOUNT-CURRENCY", bcur.get("readOnly") is True and "currencyCode" in (bca.get("required") or []),
         "B2bCreditAccount has no required, readOnly currencyCode, so payments.credit_account stores no currency and "
         "a tenant-wide account's Money has none (CR-322)")
    cdesc = " ".join(str(op("createB2bCreditAccount")[3].get("description") or "").split())
    need("BR-CREDIT-ACCOUNT-CURRENCY", "creditLimit.currency" in cdesc and "never changed after" in cdesc,
         "createB2bCreditAccount does not say it sets the account's currency from creditLimit.currency, never changed "
         "after (CR-322)")
    for oid in ("createB2bCreditAccount", "listB2bCreditAccounts"):
        vias = [str(v.get("query")) for v in op(oid)[3].get("x-ticvai-read-via") or [] if isinstance(v, dict)]
        need("BR-CREDIT-ACCOUNT-CURRENCY", not {"tenancy#scopeRecords", "tenancy#venueSettingsRecords"} & set(vias),
             f"{oid} still resolves the account's currency from a venue (tenancy#scopeRecords/venueSettingsRecords); "
             "it is the account's own currencyCode (CR-322)")
    podoc = load("contracts/satellite/platform-ops.yaml")
    par = ((podoc.get("components") or {}).get("schemas") or {}).get("PlatformApprovalRule") or {}
    seed = [r for r in par.get("x-ticvai-seed-rows") or [] if isinstance(r, dict)]
    need("BR-PLATFORM-APPROVAL-RULE", par.get("x-ticvai-persistence") == "control.platform_approval_rule" and any(
         r.get("kind") == "configurationChange" and r.get("subjectType") == "tenant"
         and r.get("approverPermission") == "PLATFORM_TENANT_MANAGE" and r.get("minimumApprovals") == 2
         and r.get("isActive") is True for r in seed),
         "no control.platform_approval_rule schema seeded with the platform rule (configurationChange, tenant, "
         "PLATFORM_TENANT_MANAGE, 2 approvals, active), so suspend and reactivate are always 422 (CR-330)")
    q = ((podoc.get("x-ticvai-queries") or {}).get("platformApprovalRuleFor") or {})
    need("BR-PLATFORM-APPROVAL-RULE", q.get("table") == "control.platform_approval_rule" and "service" in (q.get("served") or []),
         "platform-ops declares no platformApprovalRuleFor query over control.platform_approval_rule served over the "
         "service route (CR-330)")
    vias = {(str(v.get("query")), str(v.get("route"))) for v in op("createApprovalRequest")[3].get("x-ticvai-read-via") or []
            if isinstance(v, dict)}
    need("BR-PLATFORM-APPROVAL-RULE", ("platform-ops#platformApprovalRuleFor", "service") in vias,
         "createApprovalRequest does not ask platform-ops#platformApprovalRuleFor over the service route for a request of "
         "subject type tenant (CR-330)")
    for get_id, put_id, sname in (("getWalletFundingRules", "setWalletFundingRules", "WalletFundingRules"),
                                  ("getWalletRefundPolicy", "setWalletRefundPolicy", "WalletRefundPolicy")):
        ver = ((wsch.get(sname) or {}).get("properties") or {}).get("version") or {}
        need("BR-WALLET-ETAG-VERSION", ver.get("type") == "integer" and ver.get("readOnly") is True
             and "version" in ((wsch.get(sname) or {}).get("required") or []),
             f"{sname} has no required, readOnly integer version, so {put_id}'s If-Match has nothing to compare (CR-332)")
        for oid in (get_id, put_id):
            hdr = ((((op(oid)[3].get("responses") or {}).get("200") or {}).get("headers") or {}).get("ETag") or {})
            need("BR-WALLET-ETAG-VERSION", "version" in str(hdr.get("description") or ""),
                 f"{oid}'s 200 sends no ETag that is the row's version (CR-332)")
        need("BR-WALLET-ETAG-VERSION", "412" in {str(k) for k in (op(put_id)[3].get("responses") or {})}
             and "`412` and nothing changes" in " ".join(str(op(put_id)[3].get("description") or "").split()),
             f"{put_id} does not say a stale If-Match is 412 and nothing changes (CR-332)")

    errors["BR-PARSE"].extend(PARSE_ERRORS)
    # BR-GUEST-SSO (r11, CHG-CR327-002; the lead, 29 October 2026: "Get those 2 gaps sorted as well"): a guest
    # sign-in provider stores its authorization URL and carries no staff group mapping. Fails on CR-327's first cut.
    isch = (load("contracts/spine/identity.yaml").get("components") or {}).get("schemas") or {}
    spc = (isch.get("SsoProviderConfig") or {}).get("properties") or {}
    need("BR-GUEST-SSO", (spc.get("authorizationUrl") or {}).get("format") == "uri"
         and "uaePass" in str((spc.get("authorizationUrl") or {}).get("description") or ""),
         "SsoProviderConfig stores no authorizationUrl for a guest uaePass row (CHG-CR327-002)")
    gm = spc.get("groupMappings") or {}
    need("BR-GUEST-SSO", "minItems" not in gm and "guest" in str(gm.get("description") or ""),
         "SsoProviderConfig.groupMappings still requires a mapping on a guest row (CHG-CR327-002)")

    # BR-UAEPASS-ENDPOINTS .. BR-CONTENT-PUBLISH (r12, ADAM CR-360 to CR-365, decided 30 October 2026, Chinmay; the
    # lead: "for each one actually check if they hold and if not then find out the best way keeping in mind what client
    # needs"). Each fails on the r11 contract.
    def words(x):
        return " ".join(str(x or "").split())

    def vias(o_):
        return {str((v or {}).get("query")) for v in o_.get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    uae = op("guestUaePassLogin")[3]
    ud = words(uae.get("description"))
    for frag in ("`issuer` followed by `/token`", "`issuer` followed by `/userinfo`", "HTTP Basic",
                 "`providerSubject` is the userinfo `sub`", "defaults to `idn`",
                 "never matches or links an existing account", "only when that claim is present"):
        need("BR-UAEPASS-ENDPOINTS", frag in ud, f"guestUaePassLogin does not say: {frag} (CR-360)")
    need("BR-UAEPASS-ENDPOINTS", "uaePass" in str((spc.get("metadataUrl") or {}).get("description") or ""),
         "SsoProviderConfig.metadataUrl does not say it is not used for a guest uaePass row (CR-360)")
    s400 = words(((op("setSsoConfig")[3].get("responses") or {}).get("400") or {}).get("description"))
    need("BR-UAEPASS-ENDPOINTS", "uaePass" in s400 and "not refused" in s400,
         "setSsoConfig's 400 sso-metadata-unreachable still reaches a guest uaePass row (CR-360)")

    lgc = op("linkGuestCheckout")[3]
    vc = (props({}, body_schema(lgc)).get("verificationCode") or {})
    need("BR-LINK-CHECKOUT", "ignored" in str(vc.get("description") or "") and "verificationCode" not in
         (body_schema(lgc).get("required") or []),
         "linkGuestCheckout's verificationCode is not optional and ignored (CR-361)")
    l403 = words(((lgc.get("responses") or {}).get("403") or {}).get("description"))
    need("BR-LINK-CHECKOUT", "subject_holding" in l403 and "another account" in l403 and "same time" in l403,
         "linkGuestCheckout's 403 does not cover unknown, mismatched and attached-elsewhere alike (CR-361)")
    need("BR-LINK-CHECKOUT", "already attached to the caller is not refused" in words(lgc.get("description")),
         "linkGuestCheckout does not answer 200 for a booking already the caller's (CR-361)")

    iq = (load("contracts/spine/identity.yaml").get("x-ticvai-queries") or {}).get("subjectMinorStatus") or {}
    iqp = (((iq.get("returns") or {}).get("items") or {}).get("properties") or {})
    need("BR-DELEGATION-READS", "ITenantRootGrant" in str(iq.get("rule") or "")
         and (iqp.get("minorStatus") or {}).get("enum") == ["minor", "adult", "unknown"]
         and set(iqp) == {"subjectId", "displayName", "minorStatus"},
         "identity#subjectMinorStatus does not answer only displayName and minorStatus under the tenant root grant "
         "(CR-362)")
    gdo, ldo = op("grantDelegation")[3], op("listDelegations")[3]
    need("BR-DELEGATION-READS", {"identity#subjectMinorStatus", "tenancy#scopeRecords"} <= vias(gdo),
         "grantDelegation does not ask identity#subjectMinorStatus and tenancy#scopeRecords (CR-362)")
    need("BR-DELEGATION-READS", "identity#subjectMinorStatus" in vias(ldo),
         "listDelegations does not ask identity#subjectMinorStatus for overSubjectName/IsMinor (CR-362)")
    for oid_, o_ in (("grantDelegation", gdo), ("listDelegations", ldo)):
        need("BR-DELEGATION-READS", o_.get("x-ticvai-scope-level") == "tenant",
             f"{oid_} is not x-ticvai-scope-level tenant (staff at the tenant root only, CR-362)")
    gdd = words(gdo.get("description"))
    need("BR-DELEGATION-READS", "`familyMember` or `primaryHolder` grant over `over_subject_id`" in gdd
         and "highest threshold among the tenant's regions" in gdd,
         "grantDelegation does not state the linked adult's write check and the minor-age region rule (CR-362)")

    gvp = (isch.get("IdentityGuestVerificationPolicy") or {}).get("properties") or {}
    need("BR-GUEST-POLICY-CURRENCY", (gvp.get("currencyCode") or {}).get("readOnly") is True,
         "IdentityGuestVerificationPolicy stores no currencyCode, so a tenant-root limit has no currency (CR-363)")
    for oid_ in ("getGuestVerificationPolicy", "setGuestVerificationPolicy"):
        need("BR-GUEST-POLICY-CURRENCY",
             not {"tenancy#scopeRecords", "tenancy#venueSettingsRecords"} & vias(op(oid_)[3]),
             f"{oid_} still resolves walletTopUpLimit's currency from a venue (CR-363)")
    need("BR-GUEST-POLICY-CURRENCY", "validation" in ptypes(op("setGuestVerificationPolicy")[3], "400"),
         "setGuestVerificationPolicy lists no 400 for a walletTopUpLimit that does not fit its currency (CR-363)")

    lcb = op("listContentBlocks")[3]
    pk = next((p for p in lcb.get("parameters") or [] if isinstance(p, dict) and p.get("name") == "pageKey"), {})
    need("BR-CONTENT-PAGE-KEY", (pk.get("schema") or {}).get("format") == "uuid"
         and "validation" in ptypes(lcb, "400") and "or a homepage section key" not in words(lcb.get("description")),
         "listContentBlocks' pageKey is not a content page's uuid only, refused 400 otherwise (CR-364)")

    cbs = load("states/content-block.yaml")
    edges = {(t.get("from"), t.get("to"), t.get("trigger")) for t in cbs.get("transitions") or []}
    for e in (("scheduled", "published", "operation"), ("scheduled", "scheduled", "operation"),
              ("expired", "published", "operation")):
        need("BR-CONTENT-PUBLISH", e in edges, f"states/content-block.yaml has no {e[0]} -> {e[1]} by operation (CR-365)")
    pcb = op("publishContentBlock")[3]
    need("BR-CONTENT-PUBLISH", "validation" in ptypes(pcb, "400") and "no-approval-route" in ptypes(pcb, "422"),
         "publishContentBlock lists no 400 on expireAt or 422 no-approval-route (CR-365)")
    need("BR-CONTENT-PUBLISH", "must be after the moment it goes live" in words(pcb.get("description")),
         "publishContentBlock does not say expireAt must be after the moment the block goes live (CR-365)")
    need("BR-CONTENT-PUBLISH", any("approvedByPrincipalId" in str((v or {}).get("for") or "")
                                   for v in pcb.get("x-ticvai-read-via") or [] if isinstance(v, dict)),
         "publishContentBlock's identity read gives no purpose (approvedByPrincipalId, CR-365)")
    # BR-CONTENT-BLOCK (r12, ADAM CR-366; the lead's review, 30 October 2026). Fails on the r11 contract.
    wl = load("contracts/satellite/white-label.yaml")
    for oid in ("createContentBlock", "updateContentBlock"):
        o = op(oid)[3]
        vias = {(str(v.get("query")), str(v.get("route"))) for v in o.get("x-ticvai-read-via") or [] if isinstance(v, dict)}
        need("BR-CONTENT-BLOCK", ("marketing-crm#segmentRecords", "in-process") in vias,
             f"{oid} does not ask marketing-crm#segmentRecords in process for audienceSegmentId (CR-366)")
        rs = o.get("responses") or {}
        need("BR-CONTENT-BLOCK", "unknown-reference" in ((rs.get("422") or {}).get("x-ticvai-problem-types") or []),
             f"{oid} does not refuse an unusable audienceSegmentId 422 unknown-reference (CR-366, CR-103)")
        need("BR-CONTENT-BLOCK", "validation" in ((rs.get("400") or {}).get("x-ticvai-problem-types") or []),
             f"{oid} does not answer a failed body check 400 validation (CR-366)")
    cbody = ((((wl.get("components") or {}).get("schemas") or {}).get("ContentBlock") or {}).get("properties") or {}).get("body") or {}
    cbd = " ".join(str(cbody.get("description") or "").split())
    need("BR-CONTENT-BLOCK", "own schema" not in cbd and "CR-366" in cbd and "LO-CR366-001" in cbd,
         "ContentBlock.body still promises a schema per kind no file defines, or does not name the left-out item (CR-366)")
    lo = load("docs/active/left-out.yaml")
    need("BR-CONTENT-BLOCK", any((i or {}).get("id") == "LO-CR366-001" for i in lo.get("items") or []),
         "docs/active/left-out.yaml has no LO-CR366-001 for the per-kind body schemas (CR-366)")

    # BR-SCOPE-LOOKUP (r12, ADAM CR-367). The published set and its lookup give section 2's answer for every vector.
    def contains(a, b):
        return b == a or b.startswith(a + ".")

    def resolve(grants, perm, node):
        if any(g["effect"] == "DENY" and g["permission"] in (perm, "*") and contains(g["scope"], node) for g in grants):
            return "DENY"
        return "PERMIT" if any(g["effect"] == "ALLOW" and g["permission"] == perm and contains(g["scope"], node)
                               for g in grants) else "DENY"

    def published(grants):
        perms = {g["permission"] for g in grants if g["permission"] != "*"}
        return {p: {x for x in perms if resolve(grants, x, p) == "PERMIT"} for p in {g["scope"] for g in grants}}

    def lookup(pub, perm, node):
        listed = [p for p in pub if contains(p, node)]
        if not listed:
            return "DENY"
        return "PERMIT" if perm in pub[max(listed, key=lambda p: p.count(".") + 1)] else "DENY"

    vec = json.loads((ROOT / "docs" / "architecture" / "specs" / "permission-vectors.json").read_text(encoding="utf-8"))
    for v in vec.get("vectors") or []:
        q = v["query"]
        got = lookup(published(v["grants"]), q["permission"], q["scope"])
        need("BR-SCOPE-LOOKUP", got == v["expect"],
             f"{v['id']}: the published-set lookup answers {got}, the vector expects {v['expect']} (CR-367)")
    spec_s = " ".join(spec.split())
    pbs_s = " ".join(" ".join(json.loads(pbs).get("description", "").split()).split()) if pbs else ""
    for where, t in (("permission-resolution.md 7.2", spec_s), ("Session.permissionsByScope", pbs_s)):
        need("BR-SCOPE-LOOKUP", "deepest listed path" in t and "allow or deny" in t and "CR-367" in t,
             f"{where} does not state the entry per grant path (allow or deny) and the deepest-listed-path lookup (CR-367)")
        need("BR-SCOPE-LOOKUP", "it is in the set of the node acted on or of one of its ancestors" not in t
             and "(the node acted on or one of its ancestors);" not in t,
             f"{where} still says a permission holds when held at the node or any ancestor, which V07, V08 and V12 deny "
             "(CR-367)")
    sp = " ".join(str((((load("contracts/shared/permissions.yaml").get("components") or {}).get("schemas") or {})
                       .get("ScopedPermissions") or {}).get("description") or "").split())
    need("BR-SCOPE-LOOKUP", "deepest listed path" in sp, "ScopedPermissions does not state the lookup rule (CR-367)")

    # BR-ID-RESUBMIT (r12, ADAM CR-368)
    sg = op("submitGuestIdentityDocument")[3]
    need("BR-ID-RESUBMIT", "resubmission-limit-reached" in (((sg.get("responses") or {}).get("422") or {})
                                                            .get("x-ticvai-problem-types") or []),
         "submitGuestIdentityDocument does not refuse a guest past maxResubmissions 422 resubmission-limit-reached")
    rd = {str((r or {}).get("table")): " ".join(str((r or {}).get("for") or "").split()) for r in sg.get("x-ticvai-reads") or []}
    need("BR-ID-RESUBMIT", "maxResubmissions" in rd.get("identity.guest_verification_policy", "")
         and "identity.guest_identity_verification" in rd,
         "submitGuestIdentityDocument does not read maxResubmissions and the guest's verifications it counts (CR-368)")
    mr = ((isch.get("IdentityGuestVerificationPolicy") or {}).get("properties") or {}).get("maxResubmissions") or {}
    mrd = " ".join(str(mr.get("description") or "").split())
    need("BR-ID-RESUBMIT", "latest `verified`" in mrd and "greater than" in mrd,
         "IdentityGuestVerificationPolicy.maxResubmissions does not say what counts and from when (CR-368)")

    # BR-DOC-NUMBER-ENC (r12, ADAM CR-369; ADR-0063 section 5)
    dn = ((isch.get("IdentityGuestDocumentSubmission") or {}).get("properties") or {}).get("documentNumber") or {}
    need("BR-DOC-NUMBER-ENC", dn.get("x-ticvai-secret") == "field-encrypted"
         and dn.get("x-ticvai-stored-as") == "pii.subject_document.number_ciphertext",
         "documentNumber is not field-encrypted into pii.subject_document.number_ciphertext (CR-369, ADR-0063 section 5)")
    for oid in ("submitGuestIdentityDocument", "guestUaePassLogin"):
        need("BR-DOC-NUMBER-ENC", "hashed on arrival" not in text(op(oid)[3]).lower()
             and "number_ciphertext" in text(op(oid)[3]),
             f"{oid} does not store the document number encrypted in number_ciphertext (CR-369)")
    sref = json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8"))
    sdc = {c.get("column"): c for c in (sref.get("cols") or {}).get("pii.subject_document") or []}
    need("BR-DOC-NUMBER-ENC", "number_ciphertext" in sdc and (sdc.get("number_hash") or {}).get("required") != "yes",
         "pii.subject_document has no number_ciphertext, or number_hash is still NOT NULL (CR-369)")

    # BR-REGISTER-SOURCE (r12, ADAM CR-371)
    rsrc = ((isch.get("RegisterGuestRequest") or {}).get("properties") or {}).get("source") or {}
    need("BR-REGISTER-SOURCE", rsrc.get("enum") == ["guestWeb", "guestApp", "kiosk"] and rsrc.get("default") == "guestWeb",
         "RegisterGuestRequest has no source (guestWeb, guestApp, kiosk; default guestWeb) for the event's channel (CR-371)")
    gr = load("events/identity-guestRegistered.yaml")
    ch = next((p for p in gr.get("payload") or [] if (p or {}).get("field") == "channel"), {})
    need("BR-REGISTER-SOURCE", "RegisterGuestRequest.source" in str(ch.get("notes") or ""),
         "identity.guestRegistered's channel does not say it is RegisterGuestRequest.source (CR-371)")
    mk = [c for c in gr.get("consumers") or [] if (c or {}).get("context") == "marketing"]
    mkp = " ".join(str((mk[0] if mk else {}).get("purpose") or "").split())
    need("BR-REGISTER-SOURCE", "guestWeb is website" in mkp and "source registration" not in mkp,
         "identity.guestRegistered's Marketing consumer does not map channel to a ConsentSource (CR-371)")
    msch = ((load("contracts/satellite/marketing-crm.yaml").get("components") or {}).get("schemas") or {})
    need("BR-REGISTER-SOURCE", "registration" not in ((msch.get("ConsentSource") or {}).get("enum") or [])
         and "source `registration`" not in text(op("recordConsent")[3]),
         "recordConsent still records registration consents with source registration, which ConsentSource lacks (CR-371)")

    # BR-GUEST-CODE-DELIVERY (r12, ADAM CR-370 and its follow-up of 31 October 2026). Fails on the r11 contract.
    lin = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    otp_writers = {o for o, e in lin.items() if isinstance(e, dict) and "identity.otp_challenge" in (e.get("writes") or [])}
    otp_writers |= {oid for oid, (_f, _p, _m, o, _d) in ops.items()
                    if any((w or {}).get("table") == "identity.otp_challenge" for w in o.get("x-ticvai-writes") or [])}
    for oid in sorted(otp_writers | set(GUEST_CODE_ISSUERS)):
        o = op(oid)[3]
        if oid in GUEST_CODE_NON_ISSUERS:
            continue
        need("BR-GUEST-CODE-DELIVERY", "identity.guestCodeIssued" in (o.get("x-ticvai-emits") or []),
             f"{oid} writes identity.otp_challenge (a guest code) and does not emit identity.guestCodeIssued, so nothing "
             "carries the code to the guest; or name it in GUEST_CODE_NON_ISSUERS with why it mints none (CR-370)")
        need("BR-GUEST-CODE-DELIVERY", not any((w or {}).get("table") == "marketing.message_dispatch"
                                               for w in o.get("x-ticvai-write-via") or []),
             f"{oid} still writes marketing.message_dispatch through Marketing across deployables (CR-370)")
    gci_path = ROOT / "events" / "identity-guestCodeIssued.yaml"
    gci = load("events/identity-guestCodeIssued.yaml") if gci_path.exists() else {}
    gpay = {(p or {}).get("field"): p for p in gci.get("payload") or []}
    for fld in ("destination", "code"):
        need("BR-GUEST-CODE-DELIVERY", (gpay.get(fld) or {}).get("x-ticvai-secret") == "field-encrypted",
             f"identity.guestCodeIssued does not carry {fld} field-encrypted (never in clear; CR-370, ADR-0063)")
    need("BR-GUEST-CODE-DELIVERY", (gpay.get("subjectId") or {}).get("required") is False,
         "identity.guestCodeIssued's subjectId is required, but a register or verify code to an identifier with no "
         "account has none (the CR-370 follow-up)")
    need("BR-GUEST-CODE-DELIVERY", any((c or {}).get("operation") == "marketing-crm.sendGuestOneTimeCode"
                                       and (c or {}).get("idempotencyKey") == "challengeId" for c in gci.get("consumers") or []),
         "identity.guestCodeIssued has no Marketing consumer sendGuestOneTimeCode idempotent on challengeId (CR-370)")
    sg1 = op("sendGuestOneTimeCode")[3]
    need("BR-GUEST-CODE-DELIVERY", "identity.guestCodeIssued" in (sg1.get("x-ticvai-consumes") or [])
         and "guestOneTimeCode" in text(sg1) and "expiresAt" in text(sg1),
         "marketing-crm declares no relay-invoked sendGuestOneTimeCode consuming identity.guestCodeIssued with the system "
         "template guestOneTimeCode and the expiry rule (CR-370)")
    vsi = (((((load("contracts/spine/tenancy.yaml").get("components") or {}).get("schemas") or {}).get("VenueSettings") or {})
            .get("properties") or {}).get("identity") or {}).get("properties") or {}
    for key, dflt, lo_, hi in (("guestOtpLifetimeSeconds", 600, 60, 900), ("guestOtpResendSeconds", 60, 30, 300)):
        s_ = vsi.get(key) or {}
        need("BR-GUEST-CODE-DELIVERY", (s_.get("default"), s_.get("minimum"), s_.get("maximum")) == (dflt, lo_, hi),
             f"VenueSettings.identity.{key} is not default {dflt}, {lo_} to {hi} (CR-370)")
    rg = op("requestGuestOtp")[3]
    rp = (((((rg.get("responses") or {}).get("202") or {}).get("content") or {}).get("application/json") or {})
          .get("schema") or {}).get("properties") or {}
    need("BR-GUEST-CODE-DELIVERY", "guestOtpLifetimeSeconds" in str((rp.get("expiresInSeconds") or {}).get("description"))
         and "guestOtpResendSeconds" in str((rp.get("resendAfterSeconds") or {}).get("description")),
         "requestGuestOtp's expiresInSeconds and resendAfterSeconds do not say which settings they answer (CR-370)")
    rgd = " ".join(str(rg.get("description") or "").split())
    need("BR-GUEST-CODE-DELIVERY", "`register` or `verify` an identifier with no account still gets a code" in rgd,
         "requestGuestOtp does not say that a register or verify code to an identifier with no account is still sent "
         "(the CR-370 follow-up of 31 October 2026)")
    # ---------------------------------------------------------------- r12 CR lane D (the lead, 30 October 2026: "for
    # each one actually check if they hold and if not then find out the best way keeping in mind what client needs").
    # Each rule fails on the r11 package and passes once the posted decision is in it.
    def vias_of(oid):
        return {str(v.get("query")) for v in op(oid)[3].get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def reads_of(oid):
        return {str(r.get("table")) for r in op(oid)[3].get("x-ticvai-reads") or [] if isinstance(r, dict)}

    def flat(o):
        return " ".join(text(o).replace("\\n", " ").split())

    # BR-GUEST-SETTINGS (ADAM CR-341, option B for the settings tables; CHG-CR341-001)
    lmo = op("listMyOrders")[3]
    need("BR-GUEST-SETTINGS", "tenancy#venueSettingsRecords" in vias_of("listMyOrders"),
         "listMyOrders does not read each order's venue settings through tenancy#venueSettingsRecords (CR-341)")
    lmo_t = flat(lmo.get("description") or "")
    need("BR-GUEST-SETTINGS", "names no venue" in lmo_t and "a fault to log, never a silent default currency" in lmo_t,
         "listMyOrders does not say it names no venue and that an order whose settings are not visible is a fault (CR-341)")
    cdoc_s = load("contracts/shared/common.yaml")
    ga = " ".join(str((((cdoc_s.get("components") or {}).get("securitySchemes") or {}).get("guestAuth") or {})
                      .get("description") or "").split())
    need("BR-GUEST-SETTINGS", "platform.venue_settings" in ga and "platform.region_settings" in ga and "CR-341" in ga,
         "guestAuth does not state the guest read branch of platform.venue_settings and platform.region_settings (CR-341)")
    tq_ = load("contracts/spine/tenancy.yaml").get("x-ticvai-queries") or {}
    for qn in ("venueSettingsRecords", "regionSettingsRecords"):
        need("BR-GUEST-SETTINGS", "CR-341" in str((tq_.get(qn) or {}).get("rule") or ""),
             f"tenancy#{qn} does not state the guest read branch (CR-341)")
    # BR-BILLING-LINES (ADAM CR-342, option A with refunds from orders.refund; CHG-CR342-001)
    for oid in ("listBillingStatements", "getBillingStatement"):
        miss = {"orders.sales_order", "orders.order_line_discount", "orders.refund", "payments.dunning_case"} - reads_of(oid)
        need("BR-BILLING-LINES", not miss, f"{oid} does not declare its reads of {', '.join(sorted(miss))} (CR-342)")
        missq = {"tenancy#venueSettingsRecords", "finance#taxInvoiceLineRecords"} - vias_of(oid)
        need("BR-BILLING-LINES", not missq, f"{oid} does not ask {', '.join(sorted(missq))} (CR-342)")
    lbs_t = flat(op("listBillingStatements")[3].get("description") or "")
    for frag in ("`orders.refund` row of the order with `status` `completed`", "`overdue_amount`",
                 "`adjustment`: none", "A payment's status is not a line", "**Not listed**", "open-ended first period"):
        need("BR-BILLING-LINES", frag in lbs_t,
             f"listBillingStatements does not state the line rule ({frag!r}; CR-342)")
    need("BR-BILLING-LINES", "`404`" in flat(op("getBillingStatement")[3].get("description") or ""),
         "getBillingStatement does not answer 404 for a cycle listBillingStatements does not list (CR-342)")
    osch = (op("listBillingStatements")[4].get("components") or {}).get("schemas") or {}
    bsp = str((osch.get("BillingStatement") or {}).get("x-ticvai-persistence") or "")
    need("BR-BILLING-LINES", "orders.refund" in bsp and "orders.payment" not in bsp,
         "BillingStatement is still computed from orders.payment, not orders.refund (CR-342)")
    dc = ((load("contracts/satellite/payments.yaml").get("components") or {}).get("schemas") or {}).get("DunningCase") or {}
    need("BR-BILLING-LINES", dc.get("x-ticvai-rls") == "guest-reads-own",
         "DunningCase (payments.dunning_case) is not x-ticvai-rls guest-reads-own, so a guest's statement shows no "
         "failed attempt, or another guest's under a venue scope (CR-342, the CR-295 pattern)")
    # BR-SHOP-DROP-COLLECT (ADAM CR-345, as recommended; CHG-CR345-001)
    rdoc = op("collectShopAndDrop")[4]
    sdp = (((rdoc.get("components") or {}).get("schemas") or {}).get("ShopAndDropProblem") or {})
    rr = {}
    for part in sdp.get("allOf") or []:
        rr = ((part or {}).get("properties") or {}).get("refusedReason") or rr
    need("BR-SHOP-DROP-COLLECT", "disposed" in (rr.get("enum") or []),
         "ShopAndDropProblem.refusedReason has no disposed (CR-345)")
    csd = op("collectShopAndDrop")[3]
    r409 = ((csd.get("responses") or {}).get("409") or {})
    need("BR-SHOP-DROP-COLLECT", set(r409.get("x-ticvai-problem-types") or []) == {
         "shop-and-drop-already-collected", "shop-and-drop-past-collect-by", "shop-and-drop-disposed"},
         "collectShopAndDrop's 409 does not declare one problem type per reason (CR-345)")
    csd_t = flat(csd.get("description") or "")
    need("BR-SHOP-DROP-COLLECT", "keeps the drop `uncollected`" in csd_t and "server's clock" in csd_t,
         "collectShopAndDrop does not say a partial take from uncollected stays uncollected, or whose clock "
         "pastCollectBy reads (CR-345)")
    # BR-DELEGATION-KEY (ADAM CR-352; CHG-CR352-001)
    ard = op("approveRoleAuthorityDelegation")[3]
    need("BR-DELEGATION-KEY", not ard.get("x-ticvai-singleton") and ard.get("x-ticvai-body-key") == ["delegator", "delegate"],
         "approveRoleAuthorityDelegation is still a singleton, or not keyed by x-ticvai-body-key [delegator, delegate] (CR-352)")
    need("BR-DELEGATION-KEY", "No other delegation at the venue is touched" in flat(ard.get("x-ticvai-body-key-note") or ""),
         "approveRoleAuthorityDelegation's body-key note does not state the upsert rule (CR-352)")
    need("BR-DELEGATION-KEY", "RolesAuthorityDelegationApprovalLimitsView" in text(((ard.get("responses") or {}).get("200") or {})),
         "approveRoleAuthorityDelegation's 200 is no longer RolesAuthorityDelegationApprovalLimitsView (CR-352)")
    # BR-FOREIGN-TENDER (ADAM CR-353; CHG-CR353-001)
    missq = {"tenancy#venueSettingsRecords", "orders#salesOrderRecords", "identity#principalRecords"} - vias_of("getForeignTenderReport")
    need("BR-FOREIGN-TENDER", not missq, f"getForeignTenderReport does not ask {', '.join(sorted(missq))} (CR-353)")
    ftr = flat(op("getForeignTenderReport")[3].get("description") or "")
    for frag in ("(`tender` `cash`)", "`captured` or `refunded`", "One line per (shift, `tender_currency`, `fx_rate`)",
                 "`recorded_at`", "`opened_at`"):
        need("BR-FOREIGN-TENDER", frag in ftr, f"getForeignTenderReport does not state {frag!r} (CR-353)")
    # BR-PRODUCT-FROM-PRICE (ADAM CR-358, option (a); CHG-CR358-001)
    cat = op("listProducts")[4]
    fp = ((((cat.get("components") or {}).get("schemas") or {}).get("Product") or {}).get("properties") or {}).get("fromPrice") or {}
    need("BR-PRODUCT-FROM-PRICE", fp.get("readOnly") is True and fp.get("nullable") is True
         and fp.get("x-ticvai-persisted") is False and "Money" in text(fp),
         "Product has no nullable, readOnly, unstored fromPrice Money (CR-358)")
    lp = op("listProducts")[3]
    need("BR-PRODUCT-FROM-PRICE", any(isinstance(p, dict) and p.get("name") == "channel" for p in lp.get("parameters") or []),
         "listProducts takes no channel parameter for a visitor (CR-358)")
    need("BR-PRODUCT-FROM-PRICE", "tenancy#venueSettingsRecords" in vias_of("listProducts"),
         "listProducts does not read the currency through tenancy#venueSettingsRecords (CR-358)")
    for sf, sid in (("screens/P01-guest-web-storefront.yaml", "WEB-035"), ("screens/P02-guest-mobile-app.yaml", "GST-044")):
        scr = load(sf)
        scr = scr if isinstance(scr, list) else (scr.get("screens") or [])
        s_ = next((x for x in scr if isinstance(x, dict) and x.get("id") == sid), {})
        cards = [c for r in (s_.get("layout") or {}).get("regions") or [] for c in (r.get("components") or [])
                 if isinstance(c, dict) and c.get("label") == "Prices in your currency"]
        need("BR-PRODUCT-FROM-PRICE", bool(cards) and all("Product.fromPrice" in (c.get("columns") or []) for c in cards),
             f"{sid}'s price card does not bind Product.fromPrice (CR-358)")
    # BR-BOOKING-FLOW-MISSING, BR-CALL-DISPOSITION, BR-RESTORE-MISSING-PAGE (r12, ADAM CR-343, CR-346, CR-350; the
    # lead, 30 October 2026). Each fails on the r11 package and passes on the decision.
    wl = load("contracts/satellite/white-label.yaml")
    kind_text = " ".join(str((((wl.get("components") or {}).get("schemas") or {}).get("ConfigFindingKind") or {})
                             .get("description") or "").split())
    row = kind_text[kind_text.find("| bookingFlowMissing |"):]
    for word in ("`isSellable` true", "`guestListing` `bookable`", "There is no tenant-wide flow", "`walletTopUp`"):
        need("BR-BOOKING-FLOW-MISSING", word in row,
             f"ConfigFindingKind's bookingFlowMissing row does not say {word!r} (CR-343)")
    for oid in ("validateTenantConfig", "publishTenantConfig"):
        vias = {(str(v.get("query")), str(v.get("route"))) for v in op(oid)[3].get("x-ticvai-read-via") or []
                if isinstance(v, dict)}
        for q in ("catalogue#productRecords", "tenancy#activeVenues"):
            need("BR-BOOKING-FLOW-MISSING", (q, "in-process") in vias,
                 f"{oid} does not ask {q} in process for bookingFlowMissing (CR-343, XDR-022)")
    msch = (load("contracts/satellite/marketing-crm.yaml").get("components") or {}).get("schemas") or {}
    cd = msch.get("CallDisposition") or {}
    need("BR-CALL-DISPOSITION", cd.get("x-ticvai-persistence") == "marketing.conversation",
         "CallDisposition is stored nowhere (x-ticvai-persistence marketing.conversation; CR-346)")
    cols = {k: (v or {}).get("x-ticvai-column") for k, v in (cd.get("properties") or {}).items()}
    need("BR-CALL-DISPOSITION", cols == {"outcome": "disposition_outcome", "callbackAt": "callback_at",
                                         "callbackAssignedToPrincipalId": "callback_assigned_to_principal_id",
                                         "note": "disposition_note"},
         f"CallDisposition's columns are not the four CR-346 named: {cols}")
    scd = op("setCallDisposition")[3]
    need("BR-CALL-DISPOSITION", "400" in {str(k) for k in (scd.get("responses") or {})}
         and "`callbackScheduled` without `callbackAt`" in " ".join(str(scd.get("description") or "").split()),
         "setCallDisposition does not answer 400 for a callbackScheduled without callbackAt (CR-346)")
    conv = load("states/conversation.yaml")
    moves = {(t.get("from"), t.get("to")) for t in conv.get("transitions") or [] if t.get("operation") == "setCallDisposition"}
    need("BR-CALL-DISPOSITION", moves == {("withAgent", "resolved"), ("waitingOnGuest", "resolved")},
         f"states/conversation.yaml: setCallDisposition does not end a conversation an agent holds ({sorted(moves)}; CR-346)")
    rcv = op("restoreConfigVersion")[3]
    rtext = " ".join(str(rcv.get("description") or "").split())
    for word in ("`contentPageId` null and `isVisible` false", "never causes a refusal", "`content_page.is_referenced`"):
        need("BR-RESTORE-MISSING-PAGE", word in rtext,
             f"restoreConfigVersion does not say {word!r} for a page deleted since the version (CR-350)")

    # ---------------------------------------------------------------- r12 CR lane L, pricing (ADAM CR-416 to CR-425;
    # the lead, 31 October 2026: "Include them in r12"). Each rule fails on the r12 candidate before the posted decision
    # (8535bc29) and passes once the decision is in the package.
    cat_s = ((load("contracts/spine/catalogue.yaml").get("components") or {}).get("schemas") or {})

    def sprops(name):
        return (cat_s.get(name) or {}).get("properties") or {}

    def descr(oid):
        return " ".join(str(op(oid)[3].get("description") or "").split())

    def codes_of(oid, code):
        return set(((op(oid)[3].get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def param_enum(oid, name):
        for p_ in op(oid)[3].get("parameters") or []:
            if isinstance(p_, dict) and p_.get("name") == name:
                return list((p_.get("schema") or {}).get("enum") or [])
        return None

    lo_ids = {str(i.get("id")) for i in (load("docs/active/left-out.yaml").get("items") or []) if isinstance(i, dict)}
    # BR-PRICING-QUEUE-MEMBERS (ADAM CR-416; CHG-CR416-001)
    for oid in ("listRecommendationReviewDecision", "listPricingRecommendationExplainability"):
        miss = {"catalogue.pricing_simulation", "catalogue.price_category"} - reads_of(oid)
        need("BR-PRICING-QUEUE-MEMBERS", not miss, f"{oid} does not declare the read of {', '.join(sorted(miss))} (CR-416)")
        need("BR-PRICING-QUEUE-MEMBERS", "tenancy#scopeRecords" in vias_of(oid),
             f"{oid} does not read the venue's name through tenancy#scopeRecords (CR-416)")
        d_ = descr(oid)
        for frag in ("`expected_revenue` minus `baseline_revenue`", "newest by `created_at`, ties broken by `id`",
                     "no title column is stored", "multiplied by 100", "`catalogue.price_category.name`"):
            need("BR-PRICING-QUEUE-MEMBERS", frag in d_, f"{oid} does not state {frag!r} (CR-416)")
    arr = sprops("AiRecommendationReviewDecisionQueueView").get("actualRevenueResultPercent") or {}
    need("BR-PRICING-QUEUE-MEMBERS", arr.get("nullable") is True and "LO-CR416-001" in lo_ids,
         "actualRevenueResultPercent is not nullable, or not on the left-out list as LO-CR416-001 (CR-416)")
    # BR-PRICING-AUTOMATION-LEVEL (ADAM CR-417; CHG-CR417-001)
    levels = (sprops("DynamicPricingControl").get("scopeLevel") or {}).get("enum") or []
    for vn in ("DynamicPricingAutomationPolicyControlView", "AutomationPolicyAutonomousPricingOrchestratorView"):
        pr = sprops(vn)
        need("BR-PRICING-AUTOMATION-LEVEL", "automationMode" not in pr and "automationLevel" in pr,
             f"{vn} answers automationMode, or no automationLevel (CR-417)")
    need("BR-PRICING-AUTOMATION-LEVEL", set((sprops("DynamicPricingAutomationPolicyControlView").get("scopeLevel") or {})
                                            .get("enum") or []) == set(levels),
         "DynamicPricingAutomationPolicyControlView.scopeLevel does not list every level dynamic_pricing_control stores (CR-417)")
    need("BR-PRICING-AUTOMATION-LEVEL", set(param_enum("listDynamicPricingAutomation", "scopeLevel") or []) == set(levels)
         and param_enum("listDynamicPricingAutomation", "automationMode") is None
         and param_enum("listDynamicPricingAutomation", "automationLevel"),
         "listDynamicPricingAutomation does not filter all eight scope levels and automationLevel, or still filters "
         "automationMode (CR-417)")
    need("BR-PRICING-AUTOMATION-LEVEL", {"catalogue.pricing_market", "catalogue.sales_channel"}
         <= reads_of("listAutomationPolicyAutonomous")
         and (sprops("AutomationPolicyAutonomousPricingOrchestratorView").get("channel") or {}).get("nullable") is True,
         "listAutomationPolicyAutonomous does not read pricing_market and sales_channel, or channel is not nullable (CR-417)")
    need("BR-PRICING-AUTOMATION-LEVEL", "effectiveFrom" in descr("listDynamicPricingAutomation")
         and "`start`" not in descr("listDynamicPricingAutomation"),
         "listDynamicPricingAutomation still orders by `start` (CR-417)")
    # BR-PRICING-SCORECARD (ADAM CR-418; CHG-CR418-001)
    lmp = descr("listLearningModelPerformance")
    for frag in ("price outcome measure", "No `catalogue.model_scorecard` table", "`getForecastAccuracy`",
                 "capability maturity stages", "modified decisions divided by all decisions"):
        need("BR-PRICING-SCORECARD", frag in lmp, f"listLearningModelPerformance does not state {frag!r} (CR-418)")
    need("BR-PRICING-SCORECARD", not any(str((s or {}).get("x-ticvai-persistence") or "").startswith("catalogue.model_scorecard")
                                         for s in cat_s.values() if isinstance(s, dict)),
         "a schema persists to catalogue.model_scorecard, which CR-418 ruled out")
    # BR-PRICE-SIMULATION (ADAM CR-419; CHG-CR419-001)
    sim = op("simulatePriceBreakdownCalculation")[3]
    need("BR-PRICE-SIMULATION", not sim.get("x-ticvai-singleton") and not sim.get("x-ticvai-singleton-note"),
         "simulatePriceBreakdownCalculation is still flagged a singleton though it stores nothing (CR-419)")
    need("BR-PRICE-SIMULATION", "variantId" in sprops("PriceBreakdownCalculationSimulationExplainabilityInput"),
         "PriceBreakdownCalculationSimulationExplainabilityInput has no variantId (CR-419)")
    need("BR-PRICE-SIMULATION", "finance#taxCodeRecords" in vias_of("simulatePriceBreakdownCalculation")
         and {"catalogue.price_execution", "catalogue.membership_programme"} <= reads_of("simulatePriceBreakdownCalculation"),
         "simulatePriceBreakdownCalculation does not read tax through finance#taxCodeRecords, or the live price and the "
         "membership programme (CR-419)")
    need("BR-PRICE-SIMULATION", "validation" in codes_of("simulatePriceBreakdownCalculation", "400")
         and {"no-selected-rate", "no-calculation-profile"} <= codes_of("simulatePriceBreakdownCalculation", "422"),
         "simulatePriceBreakdownCalculation does not declare 400 validation and 422 no-selected-rate / "
         "no-calculation-profile (CR-419)")
    need("BR-PRICE-SIMULATION", "evaluatePromotions" in descr("simulatePriceBreakdownCalculation")
         and "LO-CR419-001" in lo_ids,
         "simulatePriceBreakdownCalculation names no promotion rule, or aiInsights is not on the left-out list (CR-419)")
    # BR-CALC-PROFILE-VERSION (ADAM CR-420; CHG-CR420-001)
    cp = cat_s.get("CalculationProfile") or {}
    need("BR-CALC-PROFILE-VERSION", ["scopePath", "code", "version"] in (cp.get("x-ticvai-unique-together") or []),
         "CalculationProfile is not unique on (scopePath, code, version), so two saves can take one number (CR-420)")
    need("BR-CALC-PROFILE-VERSION", "default-profile-exists" in codes_of("setPriceCalculationPolicy", "409")
         and "validation" in codes_of("setPriceCalculationPolicy", "400"),
         "setPriceCalculationPolicy does not answer a second default 409 default-profile-exists, or a step's profile id "
         "400 validation (CR-420)")
    spc = descr("setPriceCalculationPolicy")
    need("BR-CALC-PROFILE-VERSION", "keyed by `code`" not in spc and "numbered by the server" in spc
         and "`sequence` number" in spc,
         "setPriceCalculationPolicy still keys on code and version, or does not say the server numbers versions and "
         "dependsOn names sequence numbers (CR-420)")
    # BR-ROLLBACK-CANCEL (ADAM CR-421; CHG-CR421-001)
    cpr = descr("cancelPricingRollback")
    need("BR-ROLLBACK-CANCEL", "IApprovalRequests.CancelAsync" in cpr and "is withdrawn" not in cpr
         and "no outbox row is written" in cpr,
         "cancelPricingRollback does not cancel its waiting request in process through IApprovalRequests.CancelAsync, "
         "or still withdraws it (CR-421)")
    ov = (json.loads((ROOT / "handoff" / "api-data-lineage-overrides.json").read_text(encoding="utf-8"))
          .get("operations") or {})
    need("BR-ROLLBACK-CANCEL", "platform.outbox" not in ((ov.get("cancelPricingRollback") or {}).get("writes") or []),
         "the lineage still has cancelPricingRollback write platform.outbox (CR-421)")
    need("BR-ROLLBACK-CANCEL", "CancelAsync" in descr("cancelApprovalRequest"),
         "cancelApprovalRequest does not name the in-process move IApprovalRequests.CancelAsync (CR-421)")
    # BR-LIVE-PRICE (ADAM CR-422; CHG-CR422-001)
    clp = op("createLiveDynamicPrice")[3]
    need("BR-LIVE-PRICE", "catalogue.price" not in ((ov.get("createLiveDynamicPrice") or {}).get("writes") or []),
         "the lineage still has createLiveDynamicPrice write catalogue.price, the base (CR-422)")
    lin_in = sprops("LiveDynamicPriceExecutionDeploymentMonitorInput")
    need("BR-LIVE-PRICE", "applied to `catalogue.price`" not in str((cat_s.get("LiveDynamicPriceExecutionDeploymentMonitorInput")
                                                                       or {}).get("x-ticvai-persistence") or "")
         and "strategy" in lin_in,
         "LiveDynamicPriceExecutionDeploymentMonitorInput is still applied to catalogue.price (CR-422)")
    ev = ROOT / "events" / "catalogue-priceExecuted.yaml"
    evd = load("events/catalogue-priceExecuted.yaml") if ev.exists() else {}
    need("BR-LIVE-PRICE", "catalogue.priceExecuted" in (clp.get("x-ticvai-emits") or [])
         and "createLiveDynamicPrice" in (evd.get("emittedBy") or []) and bool(evd.get("consumers")),
         "createLiveDynamicPrice does not emit catalogue.priceExecuted, or the event has no file or consumer (CR-422)")
    need("BR-LIVE-PRICE", "approvals#requestRecords" in vias_of("createLiveDynamicPrice")
         and "validation" in codes_of("createLiveDynamicPrice", "400")
         and {"approval-required", "guardrail-breached"} <= codes_of("createLiveDynamicPrice", "422"),
         "createLiveDynamicPrice does not read its approval through approvals#requestRecords, or declare 400 validation "
         "and 422 approval-required / guardrail-breached (CR-422)")
    # BR-STRATEGY-FIGURES (ADAM CR-423; CHG-CR423-001)
    need("BR-STRATEGY-FIGURES", {"catalogue.price_execution", "catalogue.price_ladder"} <= reads_of("listDynamicPricingStrategy")
         and {"tenancy#scopeRecords", "identity#principalRecords"} <= vias_of("listDynamicPricingStrategy"),
         "listDynamicPricingStrategy does not read price_execution and price_ladder, or the venue and owner names (CR-423)")
    need("BR-STRATEGY-FIGURES", "testing" not in (param_enum("listDynamicPricingStrategy", "status") or [])
         and "LO-CR423-001" in lo_ids,
         "listDynamicPricingStrategy still offers testing, or it is not on the left-out list (CR-423)")
    lds = descr("listDynamicPricingStrategy")
    for frag in ("`currentPriceAdjustments` counts", "`pricesAtMaximumGuardrail` counts", "seven open-conflict counts",
                 "`pricesAtUpperBand`", "a draft with a ladder and at least one rule"):
        need("BR-STRATEGY-FIGURES", frag in lds, f"listDynamicPricingStrategy does not state {frag!r} (CR-423)")
    # BR-PRICE-BAND-ORDER (ADAM CR-424; CHG-CR424-001)
    ldb = descr("listDynamicPriceBand")
    need("BR-PRICE-BAND-ORDER", "Sorted by `ladderId` ascending" in ldb and "Sorted by `code`" not in ldb
         and "ladderId" in sprops("DynamicPriceBandsLaddersAdjustmentMatrixView"),
         "listDynamicPriceBand does not sort by ladderId alone, a member of its view (CR-424)")
    # BR-GUARDRAIL-SCOPE (ADAM CR-425; CHG-CR425-001)
    gp = op("setDynamicPricingGuardrailPolicy")[3]
    need("BR-GUARDRAIL-SCOPE", gp.get("x-ticvai-body-key") == ["scopeLevel", "scopeId"]
         and "400 validation" in str(gp.get("x-ticvai-body-key-note") or "")
         and "is refused `400 validation`" not in str(gp.get("x-ticvai-body-key-note") or ""),
         "setDynamicPricingGuardrailPolicy is not keyed by [scopeLevel, scopeId], or still answers a missing scopeId "
         "400 (CR-425)")
    need("BR-GUARDRAIL-SCOPE", "validation" in codes_of("setDynamicPricingGuardrailPolicy", "400")
         and {"scope-id-required", "scope-not-found", "no-approval-route"} <= codes_of("setDynamicPricingGuardrailPolicy", "422"),
         "setDynamicPricingGuardrailPolicy does not declare 400 validation and 422 scope-id-required / scope-not-found / "
         "no-approval-route (CR-425)")
    dpc = sprops("DynamicPricingControl")
    need("BR-GUARDRAIL-SCOPE", all((dpc.get(k) or {}).get("readOnly") is True
                                   for k in ("pendingAutomationLevel", "pendingApprovalRequestId")),
         "DynamicPricingControl has no readOnly pendingAutomationLevel and pendingApprovalRequestId (CR-425)")
    for k in ("authorityTiers", "noChangeWindows", "circuitBreakers"):
        need("BR-GUARDRAIL-SCOPE", (dpc.get(k) or {}).get("type") == "array",
             f"DynamicPricingControl.{k} is not an array of the objects its description lists (CR-425)")
    for evn in ("granted", "rejected", "withdrawn", "expired"):
        cons = load(f"events/approval-{evn}.yaml").get("consumers") or []
        need("BR-GUARDRAIL-SCOPE", any(isinstance(c, dict) and c.get("context") == "catalogue"
                                       and "dynamicPricingControl" in str(c.get("purpose") or "") for c in cons),
             f"events/approval-{evn}.yaml has no catalogue consumer for subjectType dynamicPricingControl (CR-425)")

    total = sum(len(v) for v in errors.values())
    rules = ["BR-PARSE", "BR-STREAM", "BR-PAIR-REFUSAL", "BR-SPLIT", "BR-VISIT-PLAN", "BR-PO", "BR-PAY-LINK", "BR-REPORT-RUNS",
             "BR-CONTRAST", "BR-WO-CANCEL", "BR-INCIDENT", "BR-FARE", "BR-SESSIONS-DOOR", "BR-ATTENDANCE",
             "BR-AI-CURRENCY", "BR-QR", "BR-NEW-OPS", "BR-GUEST-PII", "BR-HOST-ROUTING", "BR-CASH-RECEIPT",
             "BR-HOLD-LAPSE", "BR-LOGIN-ATTEMPTS", "BR-GATE-CANCEL", "BR-APPROVAL-ROUTE", "BR-GUEST-SELF-403",
             "BR-APPROVED-OUTCOME", "BR-APPROVAL-ENGINE", "BR-APPROVAL-VERSIONS", "BR-BILLING-STATEMENT",
             "BR-STORE-CHECKLIST", "BR-PRIVACY-REQUEST",
             "BR-ANALYTICS-PROVIDER", "BR-MEDIA-COVER-USE", "BR-AGENT-LAPSE", "BR-MEDIA-REPLACE-UPLOAD",
             "BR-SCOPE-AUTHZ", "BR-SSO-ACTIVE", "BR-PERMISSION-FINDINGS", "BR-ENTITLEMENT-SHARE",
             "BR-PRESET-READONLY", "BR-END-SESSIONS", "BR-PLATFORM-TOKEN", "BR-GUEST-TOKENS", "BR-GUEST-VENUE",
             "BR-PLATFORM-INVOICE", "BR-WALLET-TOPUP-ONCE", "BR-WALLET-PUBLISH-CHECKS", "BR-WALLET-RESTORE-DRAFT",
             "BR-WALLET-RESTORE-FINDINGS", "BR-WALLET-TOPUP-CREDIT-TYPE", "BR-COOKIE-STRICTLY-NECESSARY",
             "BR-ROTA-ROLE-DENY", "BR-FORM-VERSION-KEY",
             "BR-PLANNER-QUESTIONS", "BR-ROTA-HOUR-LIMIT", "BR-ROTA-CROSS-VENUE",
             "BR-CREDIT-ACCOUNT-CURRENCY", "BR-PLATFORM-APPROVAL-RULE", "BR-WALLET-ETAG-VERSION", "BR-GUEST-SSO",
             "BR-UAEPASS-ENDPOINTS", "BR-LINK-CHECKOUT", "BR-DELEGATION-READS", "BR-GUEST-POLICY-CURRENCY",
             "BR-CONTENT-PAGE-KEY", "BR-CONTENT-PUBLISH",
             "BR-CONTENT-BLOCK", "BR-SCOPE-LOOKUP", "BR-ID-RESUBMIT", "BR-DOC-NUMBER-ENC", "BR-REGISTER-SOURCE",
             "BR-GUEST-CODE-DELIVERY",
             "BR-GUEST-SETTINGS", "BR-BILLING-LINES", "BR-SHOP-DROP-COLLECT", "BR-DELEGATION-KEY", "BR-FOREIGN-TENDER",
             "BR-PRODUCT-FROM-PRICE",
             "BR-BOOKING-FLOW-MISSING", "BR-CALL-DISPOSITION", "BR-RESTORE-MISSING-PAGE",
             "BR-PRICING-QUEUE-MEMBERS", "BR-PRICING-AUTOMATION-LEVEL", "BR-PRICING-SCORECARD", "BR-PRICE-SIMULATION",
             "BR-CALC-PROFILE-VERSION", "BR-ROLLBACK-CANCEL", "BR-LIVE-PRICE", "BR-STRATEGY-FIGURES",
             "BR-PRICE-BAND-ORDER", "BR-GUARDRAIL-SCOPE"]
    for r in rules:
        print(f"  {r:18} {len(errors.get(r, [])):3d}")
        for m in errors.get(r, [])[:12]:
            print(f"      {m}")
    print(f"  {len(PAIR_EXEMPT)} create/update pair(s) exempt with a reason")
    print(f"\n{'FAIL' if total else 'PASS'} - {total} finding(s) against the 3 October business rules")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
