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
                   identity.end_principal_sessions, which tools/derive-ddl.py writes; since r12 (ADAM CR-377,
                   CHG-CR377-001) resetPrincipalCredential does too, with end reason credential-reset, which
                   ActiveSession.endReason names.
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
  BR-R13-UPSERT-KEY, BR-R13-WALLET-TRANSFER-ETAG, BR-R13-GUEST-ROWS, BR-R13-REPRINT-GUEST, BR-R13-WRITES-LISTED,
  BR-R13-READS-DECLARED, BR-R13-FIELDS-KEPT, BR-R13-ONE-RULE (r13 root-cause lane v, CHG-R13R20-001 to
                   CHG-R13R41-001): the developer review's roots R20, R24, R28, R27, R21, R39, R40 and R41, for the
                   operations it named: a unique key behind a keyed upsert, the transfer rules' version, row security
                   for the guest an operation names, reprintOrder for a guest-checkout buyer, the tables and reads a
                   text uses, a column for each field kept, and one rule where a text contradicted itself.
  BR-VENUE-LIMIT-DEFAULT, BR-ENROL-FIELDS, BR-CART-ANONYMOUS, BR-TENANT-ROW-READ, BR-TAMPER-DETECTED-AT,
  BR-TRANSFER-GUEST-WRITE, BR-RESEND-THROUGH-ACCESS, BR-HELD-LEASES-NOOP, BR-EXPECTED-CASH, BR-QUEUE-EVENT-READS,
  BR-HOST-IDEMPOTENCY (r13 second CR round, lane w2: ADAM CR-484 to CR-527, CHG-CR484-001 to CHG-CR527-001): a
                   venue limit's proposed default, enrolDevice's field rules, the anonymous cart, the tenant's settings
                   row, a nullable event field, a guest's own transfer and resend, the shift close, the queue event's
                   reads and the device host's idempotency store.
  BR-CELL-TIER-ACTIVE, BR-CELL-TIER-JOB, BR-TENANT-LIMITS-DEFAULT, BR-TENANT-LIMITS-ROUTE, BR-PLAN-VERSIONS,
  BR-MODULE-CATALOGUE-AUDIENCE, BR-MODULE-LISTING-UPSERT, BR-LICENCE-COMBINE, BR-ADDON-MODULE-KEY, BR-DOWNGRADE-CHECK
                   (r13 second CR round, lane w5: ADAM CR-488 to CR-491, CR-510, CR-529 to CR-531, CR-535 and CR-541;
                   CHG-CR488-001 to CHG-CR541-001): the cell tier change, the tenant request limits and their route,
                   plan versions, the module catalogue and listing, the licence position and the downgrade check, as
                   lane_w5_rules_r13 lists them.
  BR-CREDENTIAL-POLICY-PROBLEM, BR-MFA-PRIMARY, BR-ENABLEMENT-SERVICE-CALLER, BR-CELL-CALL-CLIENT,
  BR-CAPACITY-PACK-UNIT, BR-CURRENT-PLAN-READER, BR-PREVIEW-RULES (r14 catch-up, lane b: ADAM CR-548, CR-549, CR-555,
                   CR-560, CR-567 and CR-568; CHG-CR548-001 to CHG-CR568-001): the credential policy refusal, the
                   primary MFA method, the service caller of getModuleEnablement, the cell call and capacity pack unit,
                   the current plan and contract readers and the subscription preview, as lane_b_rules_r14 lists them.
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
  BR-BEACON-GEOFENCE (r12, ADAM CR-389, CHG-CR389-001) a beacon's geofence is access.device_placement.activation_zone,
                   each input field names its column, health and lastDetected are not stored, and both beacon
                   operations ask tenancy#deviceRecords in process and answer 404 for a beaconId with no beacon.
  BR-FACE-TAG-PROFILE (r12, ADAM CR-390, CHG-CR390-001) setFaceTagTemporaryEnrollment creates on its path id (201,
                   no 404), lists both 422 types, stores consentFormId, and reads the venue's settings in process.
  BR-FACE-PASS-REVOKE (r12, ADAM CR-391, CHG-CR391-001) revokeFacePass declares its 404 and reads the enrolment on
                   Identity's service route (listSubjectBiometricRecords), never in process; Identity's consumer
                   deletes the row on revoked.
  BR-POLICY-VERSIONS (r12, ADAM CR-392, CHG-CR392-001) a policy version is the next integer per kind, unique with
                   kind; an effectiveFrom in the past is 400; the current version is the latest in force (UTC).
  BR-CONTENT-PAGE-SWITCH (r12, ADAM CR-393, CHG-CR393-001) a published page takes an isEnabled switch, which
                   invalidates the storefront pages cache.
  BR-GUIDED-CHOICE-TARGETS (r12, ADAM CR-394, CHG-CR394-001) the three guided-choice writes ask Catalogue in process,
                   publish states the on-sale rule per kind, and its 422 is GuidedChoiceAnswerProblem.
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
  BR-DASHBOARD-COST (r12, ADAM CR-372, CHG-CR372-001) Dashboard.aggregateCost states its rule (60 / refreshSeconds per
                   tile, a share of the refresh budget, bands 0.5 and 0.8) and createDashboard and updateDashboard store
                   it on every save.
  BR-DASHBOARD-ENTITLEMENT (r12, ADAM CR-373, CHG-CR373-001) createDashboard, updateDashboard, listDashboards and
                   getCommandCentre ask the three Subscription licence reads in process; the rule is stated on
                   CreateDashboardRequest.module (x-ticvai-permission-modules and the session); both writes refuse 409
                   module-not-licensed or module-permission-not-held, and module-not-entitled is gone.
  BR-TILE-MARKS    (r12, ADAM CR-374, CHG-CR374-001) every DashboardTile.visualisation mark has its row in the mark
                   table, and "as their names" is gone.
  BR-AUDIT-REASON  (r12, ADAM CR-376, CHG-CR376-001) AuditRecord.reason (platform.audit_record.reason, 3 to 500
                   characters) exists, resetPrincipalCredential writes its reason there, and every request field
                   that says it is "recorded in the audit" says it is the audit row's reason.
  BR-PRIVACY-CONSENT (r12, ADAM CR-378, CHG-CR378-001) listPrivacyConsent states every count's source, every warning
                   code's rule, every directory type's source and status map and every filter's reach, and declares
                   the nine Marketing tables it reads; each count on the view says what it counts.
  BR-GUEST-BROADCAST (r12, ADAM CR-379, CHG-CR379-001) broadcastToGuests names its venue, writes
                   workforce.guest_broadcast and emits workforce.guestBroadcastAccepted (critical consumer
                   marketing-crm sendGuestBroadcast), asks access#liveEntitlementSubjects, signs an evacuation with
                   supervisorStepUp (403 supervisor-step-up-refused), and no longer writes through
                   sendTransactionalMessage; the operations host's read of access.entitlement is an XDR entry.
  BR-OPEN-SHIFT-CLAIM (r12, ADAM CR-380, CHG-CR380-001) claimOpenShift reads the training records, staffing rules and
                   rota it checks, asks the role and overlap queries, writes the open shift and the rota assignment, and
                   answers 409 rota-assignment-overlap; OpenShift.requiredQualifications states the courseName match.
  BR-KIOSK-LISTS   (r12, ADAM CR-381, CHG-CR381-001) updateKioskConfig takes attractSlides (at most 40) and startTiles
                   (at most 8), each replacing its whole list when given.
  BR-KIOSK-DELETE  (r12, ADAM CR-382, CHG-CR382-001) KioskConfig.deletedAt; deleteKioskConfig writes only kiosk_config
                   and removes nothing; every kiosk-configuration operation says what a deleted one does.
  BR-KIOSK-COUNT   (r12, ADAM CR-383, CHG-CR383-001) listKioskConfigs, getKioskConfig and listKioskAssignments ask
                   tenancy#workstationRecords in process for the venue's kiosks; KioskAssignment answers a kiosk with
                   no row.
  BR-KIOSK-CHANNEL (r12, ADAM CR-384, CHG-CR384-001) Workstation.channel [pos, kiosk], not null default pos, kept when
                   configureWorkstation leaves it out; listWorkstations filters by it; assignKiosk refuses from it.
  BR-KIOSK-FINDINGS (r12, ADAM CR-385, CHG-CR385-001) every KioskConfigFindingKind has a severity and rule row; the
                   validation and the publish ask the media, products and payment methods in process.
  BR-KIOSK-RESTORE (r12, ADAM CR-386, CHG-CR386-001) a restore of an older version sets hasUnpublishedChanges.
  BR-BANNER-OUTSIDE-DRAFT (r12, ADAM CR-387, CHG-CR387-001; general) a table white-label's header lists outside the
                   draft has no NOT NULL key to whitelabel.tenant_config, and no banner operation reads or writes it.
  BR-BANNER-STATE  (r12, ADAM CR-388, CHG-CR388-001) a banner returns to draft by isActive false, never by clearing
                   startsAt (the promo block's move); updateBanner lists its 400.
  BR-GATE-MODE-POLICY (r12, ADAM CR-396, CHG-CR396-001) whoCanActivate holds identity.role ids (format uuid);
                   setTurnstileMode asks identity#principalHoldsRoleAtVenue in process, answers 403
                   gate-mode-role-required and 400 reason-required, states the policy precedence and the incident's type
                   and team; a scheduled change keeps its turnstile mode (AccessGateModeChange.targetTurnstileMode).
  BR-ACCESS-POINT-ACTIVE (r12, ADAM CR-397, CHG-CR397-001) createAccessPoint says a new access point is created active,
                   and setAccessPointDirection names no device status AccessPoint does not have.
  BR-WHITELIST-APPROVAL (r12, ADAM CR-399, CHG-CR399-001) addBlacklistEntry raises its whitelist request through
                   x-ticvai-write-via createApprovalRequest, passes 422 no-approval-route on, and an access consumer of
                   approval.granted writes access.blacklist.
  BR-ADMISSION-CREATE (r12, ADAM CR-400, CHG-CR400-001) createAdmissionRules answers update's three 422 problem types,
                   asks tenancy#scopeRecords for the working venue's path and answers 403 working-venue-required;
                   updateAdmissionRules asks no scope read.
  BR-PRICING-QUEUE-MEMBERS (r12, ADAM CR-416, CHG-CR416-001) the recommendation queue and explainability reads declare
                   catalogue.pricing_simulation, catalogue.price_category and tenancy#scopeRecords, state each member's
                   rule, answer actualRevenueResultPercent null (nullable, LO-CR416-001) and confidence times 100.
  BR-PRICING-AUTOMATION-LEVEL (r12, ADAM CR-417, CHG-CR417-001) both automation views answer automationLevel and no
                   automationMode; the policy view's scopeLevel and listDynamicPricingAutomation's filter list every
                   level DynamicPricingControl stores; the orchestrator reads pricing_market and sales_channel for
                   market and channel, and channel is nullable.
  BR-PRICING-SCORECARD (r12, ADAM CR-418, CHG-CR418-001) listLearningModelPerformance waits on the price outcome
                   measure and is assembled from three sources, with no catalogue.model_scorecard anywhere.
  BR-PRICE-SIMULATION (r12, ADAM CR-419, CHG-CR419-001) simulatePriceBreakdownCalculation is no singleton, takes productVariantId,
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
                   each figure its rule, answers and filters automationLevel (no automationMode) and offers no testing
                   status (LO-CR423-001).
  BR-PRICE-BAND-ORDER (r12, ADAM CR-424, CHG-CR424-001) listDynamicPriceBand sorts by ladderId only, a member of its
                   view; a sort on `code`, which a price ladder lacks, fails.
  BR-GUARDRAIL-SCOPE (r12, ADAM CR-425, CHG-CR425-001) setDynamicPricingGuardrailPolicy is keyed by [scopeLevel, scopeId],
                   declares 400 validation and 422 scope-id-required / scope-not-found / no-approval-route, keeps a raise
                   in pendingAutomationLevel and pendingApprovalRequestId (readOnly), types its three lists as arrays,
                   and Catalogue consumes the four approval outcomes for subjectType dynamicPricingControl.
  BR-SEAT-MAP-SECTIONS (r12, ADAM CR-402, CHG-CR402-001) Section carries a required, read-only seatMapId referencing
                   seating.seat_map, unique with code (matched exactly); getSeatMap answers the map's sections by it, the
                   five writers say they set it, and editSeatMapStructure and copySeatMapSection answer a taken code 409
                   seat-label-taken.
  BR-SEAT-TEMPLATE-COPY (r12, ADAM CR-403, CHG-CR403-001) SeatMapTemplate keeps its own structure at its region's
                   scope_path, read-beneath, with a read-only sourceSeatMapId; createSeatMapTemplate persists the source;
                   createSeatMap reads the template, writes seating.seat, answers 422 unknown-reference and copies no
                   view photo.
  BR-SEAT-MAP-UPDATE (r12, ADAM CR-404, CHG-CR404-001) updateSeatMap declares no 409 its body cannot cause and does
                   declare the 404 a sectionViews code off the map answers (CR-402).
  BR-FORECAST-CURVE (r12, ADAM CR-405, CHG-CR405-001) listDemandBookingCurve reads the venue currency through
                   tenancy#venueSettingsRecords, nothing from Orders, answers confidence x 100 and a venue with no
                   currency 500, never a left-out revenue.
  BR-ELASTICITY-CONTEXT (r12, ADAM CR-406, CHG-CR406-001) DemandForecast stores the five context columns;
                   listPriceElasticityRevenue reads the venue currency (not Orders) and states the filters, the
                   latest-run rule, the confidence bands, the item and the full order.
  BR-PRICING-PERFORMANCE (r12, ADAM CR-407, CHG-CR407-001) listDynamicPricingPerformance reads the venue currency and
                   the strategies (not Orders), orders by label then key (not a nested `at`), refuses what it cannot
                   compare 400, and keeps every view member with the left-out KPIs on LO-CR407-001.
  BR-REVENUE-ROW   (r12, ADAM CR-408, CHG-CR408-001) listRevenue declares its demand_forecast read, defines the row,
                   the status mappings and the control in force, orders by rankBy and lists the five left-out figures
                   (LO-CR408-001).
  BR-COMPETITOR-OBSERVATION (r12, ADAM CR-409, CHG-CR409-001) a competitor price observation is a row of
                   catalogue.competitor_price_observation (its own currencyCode, keyed to its demand_signal registry
                   row); listCompetitorPricingMarket reads it and states the median, position and movement rules, and
                   the view's computed figures are nullable.
  BR-CONTEXTUAL-RULE (r12, ADAM CR-410, CHG-CR410-001) a contextual rule is a pricing.dynamic_price_rule row with its
                   dimension columns; channelId keys catalogue.sales_channel; setDynamicPriceRule answers 422
                   contextual-rule-incomplete; listChannelCustomerSegment reads the rule table only.
  BR-SALE-SCHEDULE-SUMMARY (r12, ADAM CR-411, CHG-CR411-001) every figure of the schedule summary states its rule,
                   blackouts come from blackoutDates, and listChannelSaleSchedule reads product_channel_assignment for
                   every-product windows.
  BR-CHANNEL-ALLOCATION-COUNTS (r12, ADAM CR-412, CHG-CR412-001) channel_envelope keeps allocationPercent and the
                   released and returned units; setChannelAllocations refuses a percentage with no percent (400
                   validation); relinquishChannelAllocation writes returned_units; the product filter is the event
                   path and the order is total.
  BR-CHANNEL-CODE-UNIQUE (r12, ADAM CR-413, CHG-CR413-001) a channel code is unique per tenant (x-ticvai-unique) and
                   createChannelProfile answers 409 DuplicateCode and 400 for a bad scope; scopeId is a uuid; kiosk
                   maps to kiosk.
  BR-SALE-RULE-INSTANTS (r12, ADAM CR-414, CHG-CR414-001) listChannelSaleRule answers effectiveFrom and effectiveTo as
                   nullable instants, ordered nulls last with id last.
  BR-PRICING-APPROVAL (r12, ADAM CR-415, CHG-CR415-001) sendForApproval always raises an approvals request in process
                   (x-ticvai-writes approvals.request, both in commerce), passes 422 no-approval-route through,
                   writes no outbox or audit_entry, and Catalogue consumes the four approval events for it.
  BR-BOOKING-FLOW-RESOLVE (r12, ADAM CR-426 and CR-427, CHG-CR426-001, CHG-CR427-001) deleteBookingFlow and
                   getPublishedBookingFlow ask catalogue#productRecords and #productCategoryRecords in process (XDR-051);
                   deleteBookingFlow states its two 409 cases and the on-sale rule, getPublishedBookingFlow the four
                   steps, the kind tie rule (productKinds position, then catalogue position), the fall-through and 400.
  BR-FLOW-TYPE-CATALOGUE (r12, ADAM CR-428, CHG-CR428-001) every catalogue type has name and description {en, ar} (the
                   15 English names CMS-103 shows, in catalogue order), every condition is {en, ar}, and
                   listBookingFlowTypes answers in catalogue order (never by name) with the condition and defaultSortOrder
                   rules.
  BR-BOOKING-FLOW-WRITES (r12, ADAM CR-429, CHG-CR429-001) both flow writes read consentQuestionRecords in process (served
                   so), never guestMatchPolicyRecords, name their 400s step-not-in-flow-type, duplicate-flow-step and
                   consent-question-not-active, and add a left-out step at its index; listBookingFlows states one order.
  BR-GUEST-CONTACT-FIELDS (r12, ADAM CR-430, CHG-CR430-001) setBookingFlowConfig checks each active venue (in process,
                   XDR-022) against the marketing-crm GuestMatchPolicy in force there, the default matchBy email with no row.
  BR-GUEST-CODE-UNKNOWN (r12, ADAM CR-431, CHG-CR431-001) an unknown login, passwordReset or stepUp identifier gets a
                   never-sent otp_challenge row, so the 429 answers alike, and verifyGuestOtp refuses any code against it.
  BR-GUEST-CHECKOUT-PROOF (r12, ADAM CR-432, CHG-CR432-001) a guest-checkout code is proved under the cart's anonymous
                   session (security none or guestAuth, 204, no subject, no GuestSession), the session holds
                   verifiedContactRef, checkoutCart writes a subject-less order with it, and no route makes a profile.
  BR-DELEGATION-CYCLE (r12, ADAM CR-433, CHG-CR433-001) identity#delegationReaches is a yes/no rule question under
                   ITenantRootGrant that grantDelegation asks in process, under one transaction advisory lock.
  BR-WEBHOOK-REPLAY-TENANT (r12, ADAM CR-434, CHG-CR434-001) WebhookReplayJob.tenantId states the backfill from the
                   subscription's API client, the stop on rows left, and SET NOT NULL.
  BR-OUTBOX-REPUBLISH-READS (r12, ADAM CR-435, CHG-CR435-001) republishOutbox declares no read of outbox rows (neither
                   read-via nor lineage read) and names its partition-catalogue bound.
  BR-VARIANT-PRICE (r13, ADAM CR-439 and CR-455, CHG-CR439-001, CHG-CR455-001) catalogue#variantPriceRecords states the
                   one price rule (candidates, ranking, the category rate, a null amount); searchCatalogue and
                   variantListingFacts use it; ProductVariant.priceCategoryId; the simulation states the member, dynamic,
                   fee and tax rules and answers 422 promotion-evaluation-unavailable and unsupported-tax-method.
  BR-ELASTICITY-LABELS (r13, ADAM CR-446, CHG-CR446-001) a one-bound proximity reads 'up to {to} days' or '{from}+ days';
                   movementPercent is rounded to one decimal.
  BR-CHANGE-IMPACT (r13, ADAM CR-456, CHG-CR456-001) listPricingChangeImpact is computed at read time with a rule per
                   figure, its reads declared, the five sourceless figures nullable and on LO-CR456-001.
  BR-PRODUCT-WORKFLOW (r13, ADAM CR-460, CHG-CR460-001) listProductApprovalWorkflows reads catalogue.approval_policy rows
                   with subject product; approveWorkflow states the mapping and what a replace keeps.
  BR-FEE-INSTANTS  (r13, ADAM CR-464, CHG-CR464-001) the fee and calculation-sequence views answer nullable instants,
                   asOf is an instant, and status takes CatalogueConfigStatus.
  BR-SEAT-RULE-OVERLAP (r13, ADAM CR-467, CHG-CR467-001) setSeatPricingRule answers invalid-range and defines covered
                   seats and the overlap on its own table.
  BR-TAX-PROFILE-LIST (r13, ADAM CR-468, CHG-CR468-001) listTaxProfiles and getTaxProfileJurisdiction declare their
                   tax-code, legal-entity, venue, tax-rule and product reads; at or beneath; status as stored.
  BR-FORM-LIVE-ACCEPTANCE (r13, ADAM CR-472, CHG-CR472-001) submitForm asks nothing of Identity (no read-via, no
                   lineage read of pii.subject), reads its own waiver_version_control, and states the live-acceptance
                   rule: same form, subject and onBehalfOf, unexpired, the same version or an earlier one under
                   noResign, 200 with nothing written, else 201.
  BR-SEO-METADATA-STORE (r13, ADAM CR-474, CHG-CR474-001) setSeoMetadata asks nothing of Catalogue (no read-via, no
                   lineage read of catalogue.product), does not check the entity, stores a changed slug and leaves
                   the 301 to createUrlRedirect.
  BR-CONFIG-DIFF-PRODUCTS (r13, ADAM CR-475, CHG-CR475-001) diffConfigVersion asks catalogue#productRecords and
                   #productCategoryRecords in process and states the three-step flow rule of CR-427.
  BR-PREVIEW-READS-NOTHING (r13, ADAM CR-476, CHG-CR476-001) createPreview asks no query, the operations role has no
                   grant on orders.ticket_template, ticketTemplateRecords is served in process, and preview.requested's
                   consumer asks both reads in process.
  BR-SHOP-DROP-ORDER-LINES (r13, ADAM CR-477, CHG-CR477-001) createShopAndDrop asks orders#orderLineRecords in process
                   (XDR-071 grants orders.order_line to operations) and states the 422 unknown-order and unknown-line.
  BR-MERCH-LIVE-PRICE (r13, ADAM CR-478, CHG-CR478-001) lookupMerchandise asks tenancy#workstationRecords and
                   promotions#liveEffectivePrice in process; liveEffectivePrice is served in process, reads promotion
                   and promotion_rule, and runs evaluatePromotions' code; XDR-072 grants the two tables.
  r13, lane o (ADAM CR-436 to CR-482, decided 1 and 2 November 2026; channel_rules_r13), each failing on the r12 package
  but the last, which holds a condition r12 already met:
  BR-AUDIT-READ-NULLABLE (CR-436, CHG-CR436-001) AuditRead does not require readAt or target: the SQL adds both nullable
                   and the table record follows the SQL.
  BR-REFUND-POLICY-SCOPE (CR-454, CHG-CR454-001) RefundCalculationPolicyView.scopePath stays required and states the
                   backfill from the tenant root, then SET NOT NULL.
  BR-CHANNEL-RETRY (CR-457, CHG-CR457-001) retryChannelIncident emits catalogue.channelIncidentRetryRequested, whose
                   event names Catalogue's channel retry job (incidentId+retryCount, never resolved without a success).
  BR-CHANNEL-TESTS (CR-458, CHG-CR458-001) ChannelConnection.lastTests is an array of {test, result, testedAt, detail};
                   testChannelConnection states the tests per type, the address guard and the status rule;
                   listChannelConnectionIntegration maps the stored names to the view's.
  BR-VAULT-REFERENCE (CR-459, CHG-CR459-001) the one vault-reference format, checked by the kernel's shared validator,
                   with 422 secret-not-reference that never echoes the value.
  BR-CHANNEL-RULE-CONFLICT (CR-466, CHG-CR466-001) setChannelSalesRule's 409 rule-conflict: same channel, product and
                   kind, overlapping instants (CR-414), never on a switch-off, under an advisory lock.
  BR-R12-DB-STATEMENTS (CR-461, CR-470, CHG-CR461-001) what the r12 [DB] tickets left to the operations and the NOT NULL
                   the package means for seating.section.seat_map_id and seating.seat_map_template.
  BR-MEMBERSHIP-PLAN-PAGE (CR-482, CHG-CR482-001) Product.isFeatured and compareAtPrice (compare_at_amount), set on
                   create and update; WEB-022 sells through the cart and goes on to WEB-011.
  BR-WEB035-PRICE-CARDS (CR-473, CHG-CR473-001) WEB-035 keeps CR-358's Prices in your currency cards on listProducts.
  r13 second CR round, lane w3 (ADAM CR-493 to CR-534, decided 3 November 2026; lane_w3_rules_r13), each failing on
  the r13 candidate before the lane (f599f2c6):
  BR-GST007-AS-BUILT (CR-493, CHG-CR493-001) GST-007's coach-mark cards, the More dates month calendar and the
                   one-question Yes / No consent pop-up with a close (x) that discards the answers.
  BR-GST008-PHOTO-BADGE (CR-494, CHG-CR494-001) GST-008's open photo runs into the white card and the N selected badge
                   sits beside the kind icon, in the record and in the frame.
  BR-BOOKING-FLOW-EVENT (CR-495, CHG-CR495-001) getPublishedBookingFlow resolves from eventId (products where
                   {venueId, eventId}, first that resolves); GST-007 sends productId, else eventId.
  BR-FORM-ROOT-READ (CR-496, CHG-CR496-001) submitForm reads the published form and its resign rule under the root
                   grant, filtered to the caller's paths, then returns to the caller's grant.
  BR-CONFIG-DIFF-SHAPE (CR-500, CHG-CR500-001) diffConfigVersion's areas, paths, values, order, changeScope and 404.
  BR-PERFORMANCE-INTO-TICKETS (CR-503, CHG-CR503-001) WEB-005 takes performanceId from WEB-006 and shows the Date of
                   visit from getPerformance.
  BR-PREVIEW-ADDRESS (CR-507, CHG-CR507-001) createPreview takes the address through getPlatformSubdomain's reads and
                   keeps its entry through IKeyedState (preview:{previewId}).
  BR-SESSION-BATCH-RECORD (CR-511, CHG-CR511-001) the batch is recorded in platform.idempotency_record, the outbox row
                   keyed by batchId, the scope an active venue's path or the tenant root.
  BR-GUEST-DOCUMENT-UPLOAD (CR-521, CHG-CR521-001) createGuestDocumentUpload issues the key; uploadGuestDocument checks
                   it (422) and guest_document takes the grant-holder subject policy.
  BR-KIOSK-CHECK-ROWS (CR-528, CHG-CR528-001) the kiosk checks read payment methods by venueIds and media by venue_id
                   under the root grant, findings only.
  BR-WEB022-STATUS-PILL (CR-534, CHG-CR534-001) WEB-022's Your plan pill maps every GuestMembership.status; the
                   redraw and the Passholders section are on the left-out list.
  BR-SCHEDULED-PUBLISH-RUN (CR-501, CHG-CR501-001) the scheduled-publish job's run (per tenant, SKIP LOCKED, the review
                   filter, latest scheduledFor, the same-run supersede) on top of CR-154's activated_at rule, and the
                   approval consumer leaves a later-scheduled version waiting.
  BR-PUBLISH-REVIEW-DEFAULT (CR-520, CHG-CR520-001) switching the publish review on creates the default rule, reads
                   approvals#ruleRecords in process (XDR-111) and Identity's role permissions over its service route,
                   and answers 409 review-route-unavailable until #31185.
  r13 second CR round, lane w1 (ADAM CR-499 to CR-545, decided 3 November 2026; lane_w1_rules_r13), each failing on
  the r13 candidate before the lane:
  BR-GROUP-PACKAGE-SOURCE (CR-499) setGroupPackageDefinition answers name and unitPrice null and asks no venue
                   settings; listGroupPackages names and prices a package as listProducts does, with channel.
  BR-PRODUCT-BADGE-RATING (CR-504) Product.highlightBadge (per language, 20 characters) on create and update, and
                   Product.rating (readOnly, not stored); WEB-005's cards bind both.
  BR-SHOP-DROP-RULES (CR-508) createShopAndDrop's 409 types per reason, 400 line-ids-required, the dropReference
                   rule, the drop's venue, the order path's merchandise match and the collection point's hours.
  BR-CATEGORY-TREE-PASSES (CR-523) listProductCategories prunes inactive subtrees for guests and lifts a node's
                   kept descendants past a node dropped for its kind.
  BR-WAITING-ROOM-COOKIE (CR-524) getWaitingRoomPosition is built on #29033 and its admitted answer carries the
                   API's Set-Cookie.
  BR-GUIDED-ANSWER-FILTER (CR-532) one guided-answer filter: the overlap, subcategory, swim (consent kind swim or
                   the old swimAbility) and certification rules, and the consent-question read on its three callers.
  BR-SEARCH-CATALOGUE-SOURCES (CR-533) searchCatalogue's summary is the description, with the localised maps,
                   channel, showInfoOnly from the published configuration and fromPrice's reads.
  BR-SIMULATION-CHANNEL-MAP (CR-537) the simulation maps SalesChannel to catalogue Channel; api and backOffice price
                   nothing.
  BR-CHANNEL-RETRY-READINGS (CR-538) a retrying incident is refused; the job's trace, audit entry and shared
                   scrubbing of the excerpt.
  BR-CHANGE-IMPACT-REPRICE (CR-539) projectedRevenue reprices order lines by each line's ratio, the most specific
                   line winning; the revenue figures are nullable.
  BR-CHANNEL-TEST-NOT-SUPPORTED (CR-540) a named test that does not apply is recorded notSupported, and the 422
                   fires only for an order test that applies.
  BR-IMPORT-STAGED-ROWS (CR-542) catalogue.import_job_row stages the parse; the job stores mode, appliedCount and
                   failedCount; the commit's refusals.
  BR-GUEST-MEMBERSHIP-FIELDS (CR-543) the freeze window is stored; GuestMembership's status, benefits and terms by
                   rule; no Marketing read.
  BR-BULK-PRICE-SKIPS (CR-544) bulkChangePrices' selection, skip reasons, escalates, 403 and 400.
  BR-CLONE-PRODUCT-RULES (CR-545) cloneProduct's code and name constraints, 400, and its copy list.
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
    rpc = op("resetPrincipalCredential")[3]
    need("BR-END-SESSIONS", "identity.end_principal_sessions" in text(rpc) and "credential-reset" in text(rpc),
         "resetPrincipalCredential does not end sessions through identity.end_principal_sessions with end reason "
         "credential-reset (CR-377)")
    aser = ((isch.get("ActiveSession") or {}).get("properties") or {}).get("endReason") or {}
    need("BR-END-SESSIONS", "credential-reset" in str(aser.get("description") or ""),
         "ActiveSession.endReason does not name credential-reset (CR-377)")
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

    # BR-KIOSK-* and BR-BANNER-* (r12, ADAM CR-381 to CR-388, decided 31 October 2026, Chinmay; the lead: "for each
    # one actually check if they hold and if not then find out the best way keeping in mind what client needs", and
    # "Include them in r12"). Each fails on the r12 candidate before these CRs (8535bc29) and passes on the decisions.
    def kwords(x):
        return " ".join(str(x or "").split())

    def kvias(o_):
        return {(str(v.get("query")), str(v.get("route"))) for v in o_.get("x-ticvai-read-via") or []
                if isinstance(v, dict)}

    wlk = load("contracts/satellite/white-label.yaml")
    wls = (wlk.get("components") or {}).get("schemas") or {}
    # BR-KIOSK-LISTS (CR-381): updateKioskConfig takes the slides and the tiles as parts of their own.
    ukc = op("updateKioskConfig")[3]
    ukb = props(op("updateKioskConfig")[4], body_schema(ukc))
    for part, mx in (("attractSlides", 40), ("startTiles", 8)):
        need("BR-KIOSK-LISTS", (ukb.get(part) or {}).get("type") == "array" and (ukb.get(part) or {}).get("maxItems") == mx,
             f"updateKioskConfig's body has no {part} array of at most {mx} (CR-381)")
    need("BR-KIOSK-LISTS", "`attractLoop` with its `slides`" not in kwords(ukc.get("description"))
         and "an empty list clears it" in kwords(ukc.get("description")),
         "updateKioskConfig does not name attractSlides and startTiles as parts that replace the whole list (CR-381)")
    # BR-KIOSK-DELETE (CR-382): a removal sets deleted_at and removes nothing.
    kcp = (wls.get("KioskConfig") or {}).get("properties") or {}
    da = kcp.get("deletedAt") or {}
    need("BR-KIOSK-DELETE", da.get("readOnly") is True and da.get("nullable") is True and da.get("format") == "date-time",
         "KioskConfig has no readOnly, nullable deletedAt (whitelabel.kiosk_config.deleted_at; CR-382)")
    dkc = op("deleteKioskConfig")[3]
    dw = {str((w or {}).get("table")) for w in dkc.get("x-ticvai-writes") or [] if isinstance(w, dict)}
    need("BR-KIOSK-DELETE", dw == {"whitelabel.kiosk_config"} and "removes nothing" in kwords(dkc.get("description")),
         f"deleteKioskConfig does not write only whitelabel.kiosk_config and remove nothing ({sorted(dw)}; CR-382)")
    need("BR-KIOSK-DELETE", "`deletedAt` is null" in kwords((kcp.get("name") or {}).get("description")),
         "KioskConfig.name's uniqueness does not leave deleted configurations out (CR-382)")
    for oid_ in ("listKioskConfigs", "getKioskConfig", "updateKioskConfig", "getKioskConfigValidation",
                 "setKioskOutOfService", "restoreKioskConfigVersion", "getPublishedKioskConfig",
                 "publishKioskConfigs", "listKioskConfigVersions", "assignKiosk"):
        need("BR-KIOSK-DELETE", "deletedAt" in kwords(op(oid_)[3].get("description")),
             f"{oid_} does not say what it does with a deleted configuration (deletedAt; CR-382)")
    # BR-KIOSK-COUNT and BR-KIOSK-CHANNEL (CR-383, CR-384): a kiosk is a workstation whose channel is kiosk, read in
    # process; the venue's kiosks are listed and counted from it.
    tsch = (load("contracts/spine/tenancy.yaml").get("components") or {}).get("schemas") or {}
    need("BR-KIOSK-CHANNEL", (tsch.get("WorkstationChannel") or {}).get("enum") == ["pos", "kiosk"],
         "tenancy has no WorkstationChannel [pos, kiosk] (CR-384)")
    wst = tsch.get("Workstation") or {}
    wch = (wst.get("properties") or {}).get("channel") or {}
    need("BR-KIOSK-CHANNEL", "channel" in (wst.get("required") or []) and wch.get("default") == "pos",
         "Workstation.channel is not stored not null with default pos (CR-384)")
    cwr = ((tsch.get("ConfigureWorkstationRequest") or {}).get("properties") or {}).get("channel") or {}
    need("BR-KIOSK-CHANNEL", bool(cwr) and "default" not in cwr and "keeps the stored value" in kwords(cwr.get("description")),
         "ConfigureWorkstationRequest.channel does not keep the stored value when left out (CR-384)")
    need("BR-KIOSK-CHANNEL", any(isinstance(p_, dict) and p_.get("name") == "channel"
                                 for p_ in op("listWorkstations")[3].get("parameters") or []),
         "listWorkstations takes no channel filter (CR-384)")
    ak = op("assignKiosk")[3]
    need("BR-KIOSK-CHANNEL", ("tenancy#workstationRecords", "in-process") in kvias(ak)
         and "kiosk enrolment" not in kwords(ak.get("description")) and "`channel` is" in kwords(ak.get("description")),
         "assignKiosk does not refuse not-a-kiosk from Workstation.channel, read in process (CR-384)")
    for oid_ in ("listKioskConfigs", "getKioskConfig", "listKioskAssignments"):
        need("BR-KIOSK-COUNT", ("tenancy#workstationRecords", "in-process") in kvias(op(oid_)[3]),
             f"{oid_} does not ask tenancy#workstationRecords in process for the venue's kiosks (CR-383)")
    need("BR-KIOSK-COUNT", "`channel` `kiosk`" in kwords((kcp.get("assignedKioskCount") or {}).get("description")),
         "KioskConfig.assignedKioskCount does not count the venue's kiosks by channel (CR-383)")
    kap = (wls.get("KioskAssignment") or {}).get("properties") or {}
    need("BR-KIOSK-COUNT", all((kap.get(f_) or {}).get("nullable") is True
                               for f_ in ("id", "kioskConfigId", "assignedAt", "assignedByPrincipalId")),
         "KioskAssignment cannot answer a kiosk with no row (id, kioskConfigId, assignedAt, assignedByPrincipalId "
         "nullable; CR-383)")
    # BR-KIOSK-FINDINGS (CR-385): a severity and a rule for every kind, and every read declared, in process.
    fk = wls.get("KioskConfigFindingKind") or {}
    fkt = kwords(fk.get("description"))
    for k_ in fk.get("enum") or []:
        need("BR-KIOSK-FINDINGS", f"| {k_} | error" in fkt,
             f"KioskConfigFindingKind has no severity and rule row for {k_} (CR-385)")
    for oid_ in ("getKioskConfigValidation", "publishKioskConfigs"):
        for q_ in ("assets#mediaAssetRecords", "catalogue#productRecords", "payments#paymentMethodRecords"):
            need("BR-KIOSK-FINDINGS", (q_, "in-process") in kvias(op(oid_)[3]),
                 f"{oid_} does not ask {q_} in process (CR-385)")
    need("BR-KIOSK-FINDINGS", "paymentMethodRecords" in (load("contracts/satellite/payments.yaml")
                                                         .get("x-ticvai-queries") or {}),
         "payments declares no paymentMethodRecords query (CR-385)")
    # BR-KIOSK-RESTORE (CR-386): a restore of an older version leaves something to publish.
    need("BR-KIOSK-RESTORE", "after a restore of a version other than the current" in
         kwords((kcp.get("hasUnpublishedChanges") or {}).get("description")),
         "KioskConfig.hasUnpublishedChanges is not set by a restore of an older version (CR-386)")
    need("BR-KIOSK-RESTORE", "is not the configuration's current published version" in
         kwords(op("restoreKioskConfigVersion")[3].get("description")),
         "restoreKioskConfigVersion does not say when it sets hasUnpublishedChanges (CR-386)")
    # BR-BANNER-OUTSIDE-DRAFT (CR-387; general): a table white-label's header lists outside the draft has no NOT NULL
    # key to the draft row (whitelabel.tenant_config), and no banner operation reads or writes the draft. A table named
    # outside the draft joins the list below; the phrase check fails if the header stops naming one.
    outside = kwords((wlk.get("info") or {}).get("description"))
    outside = outside[outside.find("**Outside the draft:**"):][:600]
    sref = json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8")).get("cols") or {}
    for phrase, table in (("banners", "whitelabel.banner"), ("content blocks", "whitelabel.content_block")):
        need("BR-BANNER-OUTSIDE-DRAFT", phrase in outside,
             f"white-label's header no longer lists {phrase} outside the draft; review BR-BANNER-OUTSIDE-DRAFT (CR-387)")
        for c_ in sref.get(table) or []:
            need("BR-BANNER-OUTSIDE-DRAFT", not (c_.get("references") == "whitelabel.tenant_config"
                                                 and c_.get("required") == "yes"),
                 f"{table}.{c_.get('column')} is a NOT NULL key to the working draft, though the table is outside the "
                 f"draft (retire it, x-ticvai-retired-columns; CR-387)")
    need("BR-BANNER-OUTSIDE-DRAFT", "tenant_config_id" in ((wls.get("Banner") or {}).get("x-ticvai-retired-columns") or []),
         "Banner does not retire tenant_config_id (CR-387)")
    lin_ = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    for oid_ in ("createBanner", "updateBanner", "deleteBanner", "listBanners"):
        o_ = op(oid_)[3]
        decl = {str((x or {}).get("table")) for k_ in ("x-ticvai-reads", "x-ticvai-writes")
                for x in o_.get(k_) or [] if isinstance(x, dict)}
        lt = set((lin_.get(oid_) or {}).get("reads") or []) | set((lin_.get(oid_) or {}).get("writes") or [])
        need("BR-BANNER-OUTSIDE-DRAFT", "whitelabel.tenant_config" not in decl | lt,
             f"{oid_} reads or writes whitelabel.tenant_config, though a banner is outside the draft (CR-387)")
    need("BR-BANNER-OUTSIDE-DRAFT", "whitelabel.banner" in {str((x or {}).get("table")) for x in
                                                           op("createBanner")[3].get("x-ticvai-writes") or []
                                                           if isinstance(x, dict)},
         "createBanner declares no write of whitelabel.banner (CR-387)")
    # BR-BANNER-STATE (CR-388): a banner returns to draft by isActive false, never by clearing startsAt.
    sch_ = load("states/schedule.yaml")
    bmoves = {(t.get("from"), t.get("to"), t.get("operation")): kwords(t.get("guard"))
              for t in sch_.get("transitions") or []}
    need("BR-BANNER-STATE", "isActive false" in bmoves.get(("scheduled", "draft", "updateBanner"), "")
         and "isActive not false" in bmoves.get(("draft", "scheduled", "updateBanner"), "")
         and ("scheduled", "draft", "updatePromoBlock") in bmoves,
         "states/schedule.yaml still moves a banner to draft by clearing startsAt (CR-388)")
    bst = kwords((((wls.get("Banner") or {}).get("properties") or {}).get("state") or {}).get("description"))
    need("BR-BANNER-STATE", "sets `draft` again when a later update clears `startsAt`" not in bst
         and "`isActive` false puts a `draft`, `scheduled` or `active` banner in `draft`" in bst,
         "Banner.state does not state the isActive rule of every updateBanner save (CR-388)")
    ub = op("updateBanner")[3]
    need("BR-BANNER-STATE", "validation-failed" in set(((ub.get("responses") or {}).get("400") or {})
                                                       .get("x-ticvai-problem-types") or []),
         "updateBanner lists no 400 validation-failed for startsAt null (CR-388)")

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
    # BR-BEACON-GEOFENCE, BR-FACE-TAG-PROFILE, BR-FACE-PASS-REVOKE, BR-POLICY-VERSIONS, BR-CONTENT-PAGE-SWITCH,
    # BR-GUIDED-CHOICE-TARGETS (r12, ADAM CR-389 to CR-394; the lead's review, 31 October 2026, "for each one actually
    # check if they hold"). Each fails on the r12 candidate (8535bc29) and passes on the decision.
    acc = op("setBleBeaconGeofence")[4]
    asch = (acc.get("components") or {}).get("schemas") or {}

    def inproc(oid, q):
        return any(isinstance(v, dict) and v.get("query") == q and v.get("route") == "in-process"
                   for v in op(oid)[3].get("x-ticvai-read-via") or [])

    az = ((asch.get("AccessDevicePlacement") or {}).get("properties") or {}).get("activationZone") or {}
    need("BR-BEACON-GEOFENCE", az.get("type") == "object" and {"centre", "radiusMeters", "boundary"}
         <= set((az.get("properties") or {})),
         "AccessDevicePlacement has no activationZone {centre, radiusMeters, boundary} for the beacon geofence (CR-389)")
    bin_ = (asch.get("BleBeaconGeofenceConfigurationInput") or {}).get("properties") or {}
    want = {"beaconName": "name", "beaconId": "device_id", "venue": "venue_id", "gate": "access_point_id",
            "park": "access_area_id", "zone": "access_area_id", "attraction": "access_area_id",
            "proximityThreshold": "proximity_threshold_meters", "activeInactive": "is_active",
            "geofenceRadiusMeters": "activation_zone", "geofenceCentre": "activation_zone",
            "geofenceBoundary": "activation_zone"}
    got = {k: str((bin_.get(k) or {}).get("x-ticvai-stored-as") or "").replace("access.device_placement.", "")
           for k in want}
    need("BR-BEACON-GEOFENCE", got == want, f"BleBeaconGeofenceConfigurationInput's columns are not CR-389's: {got}")
    need("BR-BEACON-GEOFENCE", all((bin_.get(k) or {}).get("x-ticvai-persisted") is False
                                   for k in ("health", "lastDetected")),
         "BleBeaconGeofenceConfigurationInput keeps health or lastDetected, which are ignored on input (CR-389)")
    for oid in ("setBleBeaconGeofence", "getBleBeaconGeofence"):
        need("BR-BEACON-GEOFENCE", inproc(oid, "tenancy#deviceRecords"),
             f"{oid} does not ask tenancy#deviceRecords in process (CR-389, XDR-031)")
        need("BR-BEACON-GEOFENCE", "404" in {str(k) for k in op(oid)[3].get("responses") or {}},
             f"{oid} declares no 404 for a beaconId with no beacon (CR-389)")
    need("BR-BEACON-GEOFENCE", any(isinstance(p, dict) and p.get("name") == "beaconId" and p.get("required") is True
                                   for p in op("getBleBeaconGeofence")[3].get("parameters") or []),
         "getBleBeaconGeofence takes no required beaconId (CR-389)")
    need("BR-BEACON-GEOFENCE", "this write does not touch `access.access_point`" in flat(op("setBleBeaconGeofence")[3]),
         "setBleBeaconGeofence does not say it leaves access.access_point to setAccessPointGeofence (CR-389)")

    ft = op("setFaceTagTemporaryEnrollment")[3]
    fcodes = {str(k) for k in ft.get("responses") or {}}
    need("BR-FACE-TAG-PROFILE", "201" in fcodes and "404" not in fcodes,
         "setFaceTagTemporaryEnrollment does not create on the path id (201, no 404; CR-390, CR-245)")
    need("BR-FACE-TAG-PROFILE", ((ft.get("responses") or {}).get("422") or {}).get("x-ticvai-problem-types")
         == ["retention-threshold-required", "consent-form-required"],
         "setFaceTagTemporaryEnrollment's 422 does not list its two types (CR-390)")
    need("BR-FACE-TAG-PROFILE", "consentFormId" in ((asch.get("AccessBiometricProfile") or {}).get("properties") or {}),
         "AccessBiometricProfile has no consentFormId (access.biometric_profile.consent_form_id; CR-390)")
    for oid in ("setFaceTagTemporaryEnrollment", "listFaceTagTemporary"):
        need("BR-FACE-TAG-PROFILE", inproc(oid, "tenancy#venueSettingsRecords"),
             f"{oid} does not ask tenancy#venueSettingsRecords in process (CR-390, XDR-032)")

    rv = op("revokeFacePass")[3]
    need("BR-FACE-PASS-REVOKE", "404" in {str(k) for k in rv.get("responses") or {}},
         "revokeFacePass declares no 404 for an unknown or another guest's enrolment (CR-391)")
    need("BR-FACE-PASS-REVOKE", not inproc("revokeFacePass", "identity#subjectBiometricRecords"),
         "revokeFacePass reads pii.subject_biometric in process: biometric records stay off the access role (CR-391)")
    sv = op("listSubjectBiometricRecords")
    need("BR-FACE-PASS-REVOKE", sv[1] == "/queries/subject-biometric-records" and sv[2] == "post"
         and {"serviceAuth": []} in (sv[3].get("security") or []),
         "identity#subjectBiometricRecords has no service operation (listSubjectBiometricRecords, POST "
         "/queries/subject-biometric-records, serviceAuth; CR-391, CR-438)")
    ev = load("events/biometric-enrolmentChanged.yaml")
    idc = next((c for c in ev.get("consumers") or [] if isinstance(c, dict) and c.get("context") == "identity"), {})
    purpose = " ".join(str(idc.get("purpose") or "").split())
    need("BR-FACE-PASS-REVOKE", "delete the row on revoked" in purpose and "or deactivate the enrolment" not in purpose,
         "biometric.enrolmentChanged: Identity's consumer does not delete the row on revoked (CR-391)")
    xdr = load("docs/active/cross-deployable-writes.yaml")
    need("BR-FACE-PASS-REVOKE", not any(r.get("reader") == "access" and "pii.subject_biometric" in (r.get("tables") or [])
                                        for r in xdr.get("reads") or [] if isinstance(r, dict)),
         "a reads entry grants the access role pii.subject_biometric (CR-391: wait for service sign-in)")

    wls = (op("setPolicy")[4].get("components") or {}).get("schemas") or {}
    need("BR-POLICY-VERSIONS", ["kind", "version"] in ((wls.get("Policy") or {}).get("x-ticvai-unique-together") or []),
         "Policy is not unique on (kind, version) (CR-392)")
    sp = op("setPolicy")[3]
    need("BR-POLICY-VERSIONS", "effective-from-in-past" in problem_types(sp) and "409" in {str(k) for k in sp.get("responses") or {}},
         "setPolicy declares no 400 effective-from-in-past or no 409 for a concurrent version (CR-392)")
    need("BR-POLICY-VERSIONS", "one more than the highest stored for that kind" in flat(sp),
         "setPolicy does not say how a version is numbered (CR-392)")
    for oid in ("listPolicies", "listPublishedPolicies"):
        need("BR-POLICY-VERSIONS", "latest `effectiveFrom` on or before today (UTC)" in flat(op(oid)[3]),
             f"{oid} does not state the current-version rule (CR-392)")
    need("BR-POLICY-VERSIONS", "next scheduled `effectiveFrom`" in flat(op("listPublishedPolicies")[3]),
         "listPublishedPolicies' cache does not expire at the next scheduled effectiveFrom (CR-392)")

    need("BR-CONTENT-PAGE-SWITCH", "a change to `isEnabled`" in flat(op("updateContentPage")[3]),
         "updateContentPage refuses an isEnabled switch on a published page (CR-393)")
    need("BR-CONTENT-PAGE-SWITCH", "by `updateContentPage`" in flat(op("listPublishedContentPages")[3]),
         "listPublishedContentPages' cache is not invalidated by an isEnabled switch (CR-393)")

    for oid in ("createGuidedChoice", "proposeGuidedChoice", "publishGuidedChoice"):
        for q in ("catalogue#productRecords", "catalogue#productCategoryRecords", "catalogue#eventRecords"):
            need("BR-GUIDED-CHOICE-TARGETS", inproc(oid, q), f"{oid} does not ask {q} in process (CR-394, XDR-033)")
    pg = op("publishGuidedChoice")[3]
    need("BR-GUIDED-CHOICE-TARGETS", str(((((pg.get("responses") or {}).get("422") or {}).get("content") or {})
                                          .get("application/problem+json") or {}).get("schema", {}).get("$ref", ""))
         .endswith("/GuidedChoiceAnswerProblem"),
         "publishGuidedChoice's 422 is not GuidedChoiceAnswerProblem (CR-394)")
    gap = props(op("publishGuidedChoice")[4], {"$ref": "#/components/schemas/GuidedChoiceAnswerProblem"})
    need("BR-GUIDED-CHOICE-TARGETS", {"questionId", "answerId"} <= set(gap),
         "GuidedChoiceAnswerProblem carries no questionId and answerId (CR-394)")
    ptext = flat(pg)
    for word in ("`guest_listing` `bookable`", "`lifecycle_state` `onSale` or `live`", "at least one such product",
                 "enabled in the published configuration"):
        need("BR-GUIDED-CHOICE-TARGETS", word in ptext, f"publishGuidedChoice does not state {word!r} (CR-394)")
    need("BR-GUIDED-CHOICE-TARGETS", "questions/i/answers/j/target" in flat(op("createGuidedChoice")[3]),
         "createGuidedChoice's 400 does not name the failing target by its pointer (CR-394)")
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
    access_rules_r12(need, op)
    pricing_rules_r13(need, op)
    lane_q_rules_r13(need, op)
    roots_r13_v(need, op)
    lane_w2_rules_r13(need, op)
    lane_w4_rules_r13(need, op)

    # ---------------------------------------------------------------- r12 CR lane F (31 October 2026; the lead: "for
    # each one actually check if they hold and if not then find out the best way keeping in mind what client needs").
    def writes_of(oid):
        return {str(r.get("table")) for r in op(oid)[3].get("x-ticvai-writes") or [] if isinstance(r, dict)}

    def ptypes_of_id(oid, code):
        return set((((op(oid)[3].get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types")) or [])

    rdoc_ = load("contracts/satellite/reporting.yaml")
    rsch_ = (rdoc_.get("components") or {}).get("schemas") or {}
    # BR-DASHBOARD-COST (ADAM CR-372; CHG-CR372-001)
    acost = flat(props(rdoc_, rsch_.get("Dashboard") or {}).get("aggregateCost") or {})
    for frag in ("60 / `refreshSeconds`", "adds 0", "dashboardRefreshBudgetPerMinute", "below 0.5",
                 "from 0.5 to below 0.8", "from 0.8", "refresh-budget-exceeded", "reporting.dashboard.aggregate_cost"):
        need("BR-DASHBOARD-COST", frag in acost, f"Dashboard.aggregateCost does not state {frag!r} (CR-372)")
    for oid in ("createDashboard", "updateDashboard"):
        need("BR-DASHBOARD-COST", "`aggregateCost` is worked out" in flat(op(oid)[3].get("description") or ""),
             f"{oid} does not say it works out and stores aggregateCost on save (CR-372)")
    # BR-DASHBOARD-ENTITLEMENT (ADAM CR-373; CHG-CR373-001)
    lic = {"subscription#contractRecords", "subscription#licenceAddOnRecords", "subscription#planRecords"}
    for oid in ("createDashboard", "updateDashboard", "listDashboards", "getCommandCentre"):
        miss = lic - vias_of(oid)
        need("BR-DASHBOARD-ENTITLEMENT", not miss, f"{oid} does not ask {', '.join(sorted(miss))} in process (CR-373)")
    for oid in ("createDashboard", "updateDashboard"):
        need("BR-DASHBOARD-ENTITLEMENT", {"module-not-licensed", "module-permission-not-held"} <= ptypes_of_id(oid, "409"),
             f"{oid}'s 409 does not name module-not-licensed and module-permission-not-held (CR-373)")
    for oid_, (f_, _p, _m, o_, _d) in sorted(ops.items()):
        if f_.name == "reporting.yaml":
            need("BR-DASHBOARD-ENTITLEMENT", "module-not-entitled" not in problem_types(o_),
                 f"{oid_} still answers module-not-entitled for the entitlement guard (CR-373)")
    cdr = flat(rsch_.get("CreateDashboardRequest") or {})
    for frag in ("x-ticvai-permission-modules", "permissionsByScope", "`core` is always", "empty list"):
        need("BR-DASHBOARD-ENTITLEMENT", frag in cdr,
             f"CreateDashboardRequest.module's entitlement rule does not state {frag!r} (CR-373)")
    # BR-TILE-MARKS (ADAM CR-374; CHG-CR374-001)
    dtv = props(rdoc_, rsch_.get("DashboardTile") or {}).get("visualisation") or {}
    marks = list(dtv.get("enum") or [])
    if not marks and isinstance(dtv.get("$ref"), str):
        marks = list((rsch_.get(dtv["$ref"].rsplit("/", 1)[1]) or {}).get("enum") or [])
    note = str(dtv.get("x-ticvai-note") or dtv.get("description") or "")
    table_rows = [ln for ln in note.splitlines() if ln.strip().startswith("|")]
    need("BR-TILE-MARKS", bool(marks), "DashboardTile.visualisation lists no marks (CR-374)")
    for m in marks:
        need("BR-TILE-MARKS", any(f"`{m}`" in r for r in table_rows) or f"`{m}` one measure" in note
             or m in ("line", "area", "bar") or m.startswith("stacked"),
             f"DashboardTile.visualisation mark {m} has no row saying what it binds (CR-374)")
    need("BR-TILE-MARKS", "as their names" not in note, "DashboardTile.visualisation still says 'as their names' (CR-374)")
    # BR-AUDIT-REASON (ADAM CR-376; CHG-CR376-001)
    tsch_ = (load("contracts/spine/tenancy.yaml").get("components") or {}).get("schemas") or {}
    arr = ((tsch_.get("AuditRecord") or {}).get("properties") or {}).get("reason") or {}
    need("BR-AUDIT-REASON", arr.get("nullable") is True and arr.get("minLength") == 3 and arr.get("maxLength") == 500,
         "AuditRecord.reason is missing, or not nullable with 3 to 500 characters (CR-376)")
    need("BR-AUDIT-REASON", "audit row's `reason`" in text(rpc),
         "resetPrincipalCredential does not write its reason to the audit row's reason (CR-376)")
    for f in sorted((ROOT / "contracts").rglob("*.yaml")):
        if "frozen" in f.parts:
            continue
        raw = f.read_text(encoding="utf-8")
        for m in re.finditer(r"description: '?(Reason, recorded in the audit[^\n]*(?:\n {12,}[^\n]*)*)", raw):
            need("BR-AUDIT-REASON", "audit row''s `reason`" in m.group(1),
                 f"{f.relative_to(ROOT)}: a reason 'recorded in the audit' does not say it is the audit row's reason (CR-376)")
    # BR-PRIVACY-CONSENT (ADAM CR-378; CHG-CR378-001)
    lpc = op("listPrivacyConsent")[3]
    lpc_t = flat(lpc.get("description") or "")
    # marketing.consent_purpose_channel is no longer read: the channel filter does not narrow consent purposes (ADAM
    # CR-469; CHG-CR469-001).
    miss = {"marketing.consent_purpose", "marketing.communication_preference_type",
            "marketing.consent_capture_point", "marketing.tracking_technology", "marketing.cookie_banner_design",
            "marketing.minor_privacy_rule", "marketing.privacy_notice_governance",
            "marketing.processing_purpose"} - reads_of("listPrivacyConsent")
    need("BR-PRIVACY-CONSENT", not miss, f"listPrivacyConsent does not declare its reads of {', '.join(sorted(miss))} (CR-378)")
    need("BR-PRIVACY-CONSENT", "white-label#policyRecords" in vias_of("listPrivacyConsent"),
         "listPrivacyConsent does not read whitelabel.policy through white-label#policyRecords (CR-378)")
    pv = (op("listPrivacyConsent")[4].get("components") or {}).get("schemas", {}).get(
        "PrivacyConsentConfigurationCommandCenterView") or {}
    pvp = pv.get("properties") or {}
    for k, v in pvp.items():
        if (v or {}).get("type") == "integer":
            need("BR-PRIVACY-CONSENT", bool((v or {}).get("description")), f"PrivacyConsent view count {k} says nothing of what it counts (CR-378)")
            need("BR-PRIVACY-CONSENT", f"`{k}` =" in lpc_t or f"`{k}`" in lpc_t,
                 f"listPrivacyConsent states no rule for {k} (CR-378)")
    codes = ((((pvp.get("configurationWarnings") or {}).get("items") or {}).get("properties") or {}).get("code") or {}).get("enum") or []
    for c in codes:
        need("BR-PRIVACY-CONSENT", (f"`{c}`:" in lpc_t) or (c == "other" and "`other` is not raised" in lpc_t),
             f"listPrivacyConsent states no rule for the warning {c} (CR-378)")
    types_ = (((((pvp.get("configurationDirectory") or {}).get("items") or {}).get("properties") or {})
               .get("configurationType") or {}).get("enum") or [])
    for c in types_:
        need("BR-PRIVACY-CONSENT", f"`{c}` from" in lpc_t, f"listPrivacyConsent states no source for directory type {c} (CR-378)")
    for prm in lpc.get("parameters") or []:
        nm = (prm or {}).get("name")
        if nm and nm not in ("pageSize",):
            need("BR-PRIVACY-CONSENT", f"`{nm}`" in lpc_t.split("**Filters.**", 1)[-1],
                 f"listPrivacyConsent does not say what the {nm} filter narrows (CR-378)")
    need("BR-PRIVACY-CONSENT", "newest `effectiveFrom` first" not in json.dumps(op("listPrivacyConsent")[4], default=str),
         "the privacy command centre still orders its directory by newest effectiveFrom (CR-378)")
    # BR-GUEST-BROADCAST (ADAM CR-379; CHG-CR379-001)
    btg = op("broadcastToGuests")[3]
    bb = schema_of(op("broadcastToGuests")[4], body_schema(btg))
    need("BR-GUEST-BROADCAST", "venueId" in (bb.get("required") or []), "broadcastToGuests' body does not require venueId (CR-379)")
    need("BR-GUEST-BROADCAST", "supervisorStepUp" in (bb.get("properties") or {}) and btg.get("x-ticvai-step-up") == "pin"
         and btg.get("x-ticvai-step-up-carrier") == "body:supervisorStepUp",
         "broadcastToGuests does not sign an evacuation with supervisorStepUp (x-ticvai-step-up pin, CR-379)")
    need("BR-GUEST-BROADCAST", "supervisor-step-up-refused" in ptypes_of_id("broadcastToGuests", "403"),
         "broadcastToGuests' 403 does not name supervisor-step-up-refused (CR-379)")
    need("BR-GUEST-BROADCAST", not any((w or {}).get("operation") == "sendTransactionalMessage"
                                       for w in btg.get("x-ticvai-write-via") or []),
         "broadcastToGuests still writes marketing.message_dispatch through sendTransactionalMessage (CR-379)")
    need("BR-GUEST-BROADCAST", "workforce.guest_broadcast" in writes_of("broadcastToGuests")
         and "workforce.guestBroadcastAccepted" in (btg.get("x-ticvai-emits") or []),
         "broadcastToGuests does not write workforce.guest_broadcast and emit workforce.guestBroadcastAccepted (CR-379)")
    for oid in ("broadcastToGuests", "sendGuestBroadcast"):
        need("BR-GUEST-BROADCAST", "access#liveEntitlementSubjects" in vias_of(oid),
             f"{oid} does not ask access#liveEntitlementSubjects (CR-379)")
    need("BR-GUEST-BROADCAST", "liveEntitlementSubjects" in (load("contracts/spine/access.yaml").get("x-ticvai-queries") or {}),
         "access declares no liveEntitlementSubjects query (CR-379)")
    need("BR-GUEST-BROADCAST", "workforce.guestBroadcastAccepted" in (op("sendGuestBroadcast")[3].get("x-ticvai-consumes") or []),
         "marketing-crm sendGuestBroadcast does not consume workforce.guestBroadcastAccepted (CR-379)")
    ev = ROOT / "events" / "workforce-guestBroadcastAccepted.yaml"
    evd = load("events/workforce-guestBroadcastAccepted.yaml") if ev.exists() else {}
    need("BR-GUEST-BROADCAST", any((c or {}).get("operation") == "marketing-crm.sendGuestBroadcast" and (c or {}).get("isCritical")
                                   for c in evd.get("consumers") or []),
         "workforce.guestBroadcastAccepted has no critical consumer marketing-crm.sendGuestBroadcast (CR-379)")
    xdr = load("docs/active/cross-deployable-writes.yaml").get("reads") or []
    need("BR-GUEST-BROADCAST", any((x or {}).get("reader") == "operations" and "access.entitlement" in (x.get("tables") or [])
                                   and "sendGuestBroadcast" in (x.get("operations") or []) for x in xdr),
         "no XDR entry lets the operations role read access.entitlement for sendGuestBroadcast (CR-379)")
    need("BR-GUEST-BROADCAST", any((x or {}).get("reader") == "commerce" and "broadcastToGuests" in (x.get("operations") or [])
                                   and "access#liveEntitlementSubjects" in (x.get("queries") or []) for x in xdr),
         "commerce's XDR entry does not cover broadcastToGuests' access#liveEntitlementSubjects (CR-379)")
    msd = (((load("contracts/satellite/marketing-crm.yaml").get("components") or {}).get("schemas") or {})
           .get("MessageDispatch") or {})
    need("BR-GUEST-BROADCAST", "sourceRef" in (msd.get("properties") or {}),
         "MessageDispatch has no sourceRef, which listMessageDispatches filters on (CR-379)")
    # BR-OPEN-SHIFT-CLAIM (ADAM CR-380; CHG-CR380-001)
    miss = {"workforce.training_record", "workforce.staffing_rules", "workforce.rota_assignment"} - reads_of("claimOpenShift")
    need("BR-OPEN-SHIFT-CLAIM", not miss, f"claimOpenShift does not declare its reads of {', '.join(sorted(miss))} (CR-380)")
    miss = {"workforce.open_shift", "workforce.rota_assignment"} - writes_of("claimOpenShift")
    need("BR-OPEN-SHIFT-CLAIM", not miss, f"claimOpenShift does not declare its writes of {', '.join(sorted(miss))} (CR-380)")
    miss = {"identity#principalHoldsRoleAtVenue", "workforce#principalHasOverlappingAssignment"} - vias_of("claimOpenShift")
    need("BR-OPEN-SHIFT-CLAIM", not miss, f"claimOpenShift does not ask {', '.join(sorted(miss))} (CR-380)")
    need("BR-OPEN-SHIFT-CLAIM", {"shift-claimant-not-eligible", "working-hour-rule-breach", "rota-assignment-overlap"}
         <= ptypes_of_id("claimOpenShift", "409"), "claimOpenShift's 409 does not name all three refusals (CR-380)")
    wsch_ = (load("contracts/satellite/workforce.yaml").get("components") or {}).get("schemas") or {}
    rq = flat(((wsch_.get("OpenShift") or {}).get("properties") or {}).get("requiredQualifications") or {})
    need("BR-OPEN-SHIFT-CLAIM", "`courseName`" in rq and "ignoring case" in rq and "`passed`" in rq,
         "OpenShift.requiredQualifications does not state the training-record match (CR-380)")

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
    need("BR-PRICE-SIMULATION", "productVariantId" in sprops("PriceBreakdownCalculationSimulationExplainabilityInput"),
         "PriceBreakdownCalculationSimulationExplainabilityInput has no productVariantId (CR-419)")
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
    need("BR-STRATEGY-FIGURES", "automationMode" not in sprops("DynamicPricingStrategyCommandCenterView")
         and "automationLevel" in sprops("DynamicPricingStrategyCommandCenterView")
         and param_enum("listDynamicPricingStrategy", "automationMode") is None
         and param_enum("listDynamicPricingStrategy", "automationLevel"),
         "the strategy row still answers or filters automationMode instead of automationLevel (CR-423, CR-417)")
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

    # ---------------------------------------------------------------- r12 CR lane J, seat maps and revenue reads (ADAM
    # CR-402 to CR-408; the lead, 31 October 2026: "Include them in r12"). Each rule fails on the r12 candidate before
    # the posted decision (28bc5f7b) and passes once the decision is in the package.
    seat_doc = load("contracts/satellite/seating.yaml")
    seat_s = ((seat_doc.get("components") or {}).get("schemas") or {})

    def seat_props(name):
        return (seat_s.get(name) or {}).get("properties") or {}

    def writes_of(oid):
        return {str(r.get("table")) for r in op(oid)[3].get("x-ticvai-writes") or [] if isinstance(r, dict)}

    ov_j = (json.loads((ROOT / "handoff" / "api-data-lineage-overrides.json").read_text(encoding="utf-8"))
            .get("operations") or {})
    lo_j = {str(i.get("id")) for i in (load("docs/active/left-out.yaml").get("items") or []) if isinstance(i, dict)}
    # BR-SEAT-MAP-SECTIONS (ADAM CR-402; CHG-CR402-001)
    sec = seat_s.get("Section") or {}
    smi = seat_props("Section").get("seatMapId") or {}
    need("BR-SEAT-MAP-SECTIONS", smi.get("readOnly") is True and smi.get("x-ticvai-references") == "seating.seat_map"
         and "seatMapId" in (sec.get("required") or []),
         "Section has no required, read-only seatMapId referencing seating.seat_map, so no section belongs to a map (CR-402)")
    need("BR-SEAT-MAP-SECTIONS", ["seatMapId", "code"] in (sec.get("x-ticvai-unique-together") or [])
         and (seat_props("Section").get("code") or {}).get("x-ticvai-unique-compare") == "exact",
         "Section is not unique on (seatMapId, code) with code matched exactly, as Seat's key matches it (CR-402)")
    need("BR-SEAT-MAP-SECTIONS", "`seat_map_id` is `seatMapId`" in descr("getSeatMap"),
         "getSeatMap does not answer the map's sections by seat_map_id (CR-402)")
    for oid in ("createSeatMap", "editSeatMapStructure", "cloneSeatMap", "copySeatMapSection", "commitImportJob"):
        need("BR-SEAT-MAP-SECTIONS", "seat_map_id" in descr(oid),
             f"{oid} does not say the sections it writes take seat_map_id (CR-402)")
    for oid in ("editSeatMapStructure", "copySeatMapSection"):
        need("BR-SEAT-MAP-SECTIONS", "seat-label-taken" in codes_of(oid, "409"),
             f"{oid} does not answer a section code already on the map 409 seat-label-taken (CR-402)")
    # BR-SEAT-TEMPLATE-COPY (ADAM CR-403; CHG-CR403-001)
    tpl = seat_s.get("SeatMapTemplate") or {}
    tp = seat_props("SeatMapTemplate")
    need("BR-SEAT-TEMPLATE-COPY", tpl.get("x-ticvai-rls") == "read-beneath" and "scopePath" in tp
         and {"structure", "scopePath"} <= set(tpl.get("required") or []),
         "SeatMapTemplate keeps no structure, or is not read-beneath at its region's scope_path (CR-403)")
    need("BR-SEAT-TEMPLATE-COPY", (tp.get("sourceSeatMapId") or {}).get("readOnly") is True
         and (tp.get("sourceSeatMapId") or {}).get("x-ticvai-references") == "seating.seat_map",
         "SeatMapTemplate has no read-only sourceSeatMapId for lineage (CR-403)")
    cst = (((((op("createSeatMapTemplate")[3].get("requestBody") or {}).get("content") or {}).get("application/json")
            or {}).get("schema") or {}).get("properties") or {}).get("sourceSeatMapId") or {}
    need("BR-SEAT-TEMPLATE-COPY", cst and cst.get("x-ticvai-persisted") is not False,
         "createSeatMapTemplate's sourceSeatMapId is still not persisted (CR-403)")
    need("BR-SEAT-TEMPLATE-COPY", "seating.seat_map_template" in reads_of("createSeatMap")
         and "seating.seat" in writes_of("createSeatMap")
         and "unknown-reference" in codes_of("createSeatMap", "422"),
         "createSeatMap does not declare the read of seating.seat_map_template, the write of seating.seat, or 422 "
         "unknown-reference for a template it cannot use (CR-403)")
    need("BR-SEAT-TEMPLATE-COPY", "View photos are not copied" in descr("createSeatMap"),
         "createSeatMap does not say a template's copy carries no view photos (CR-403)")
    # BR-SEAT-MAP-UPDATE (ADAM CR-404; CHG-CR404-001)
    usm = op("updateSeatMap")[3]
    need("BR-SEAT-MAP-UPDATE", "409" not in (usm.get("responses") or {})
         and "Structural changes to a published map are rejected" not in descr("updateSeatMap"),
         "updateSeatMap still declares a 409 its body cannot cause, or still says structural changes are rejected (CR-404)")
    need("BR-SEAT-MAP-UPDATE", "404" in (usm.get("responses") or {}),
         "updateSeatMap does not declare the 404 a sectionViews code off the map answers (CR-402)")
    # BR-FORECAST-CURVE (ADAM CR-405; CHG-CR405-001)
    ldc = descr("listDemandBookingCurve")
    need("BR-FORECAST-CURVE", "tenancy#venueSettingsRecords" in vias_of("listDemandBookingCurve")
         and "orders#salesOrderRecords" not in vias_of("listDemandBookingCurve")
         and "orders.sales_order" not in ((ov_j.get("listDemandBookingCurve") or {}).get("reads") or []),
         "listDemandBookingCurve does not read the venue currency through tenancy#venueSettingsRecords, or still reads "
         "Orders (CR-405)")
    for frag in ("stored 0-1 value times 100", "the answer is 500", "`revenue` is never left out"):
        need("BR-FORECAST-CURVE", frag in ldc, f"listDemandBookingCurve does not state {frag!r} (CR-405)")
    # BR-ELASTICITY-CONTEXT (ADAM CR-406; CHG-CR406-001)
    dfp = sprops("DemandForecast")
    miss = {"dayType", "peakPeriod", "season", "eventProximityFromDays", "eventProximityToDays"} - set(dfp)
    need("BR-ELASTICITY-CONTEXT", not miss,
         f"DemandForecast does not store the elasticity context {', '.join(sorted(miss))} (CR-406)")
    need("BR-ELASTICITY-CONTEXT", "tenancy#venueSettingsRecords" in vias_of("listPriceElasticityRevenue")
         and "orders#salesOrderRecords" not in vias_of("listPriceElasticityRevenue")
         and "orders.sales_order" not in ((ov_j.get("listPriceElasticityRevenue") or {}).get("reads") or []),
         "listPriceElasticityRevenue does not read the venue currency through tenancy#venueSettingsRecords, or still "
         "reads Orders (CR-406)")
    lpe = descr("listPriceElasticityRevenue")
    for frag in ("`weekdayWeekend` matches `day_type`", "latest run of each slice", "below 0.5 is `low`",
                 "one point of `response_curve`", "Sorted by `product` ascending with nulls last"):
        need("BR-ELASTICITY-CONTEXT", frag in lpe, f"listPriceElasticityRevenue does not state {frag!r} (CR-406)")
    # BR-PRICING-PERFORMANCE (ADAM CR-407; CHG-CR407-001)
    ldp = descr("listDynamicPricingPerformance")
    need("BR-PRICING-PERFORMANCE", "tenancy#venueSettingsRecords" in vias_of("listDynamicPricingPerformance")
         and "orders#salesOrderRecords" not in vias_of("listDynamicPricingPerformance")
         and "catalogue.dynamic_pricing_strategy" in reads_of("listDynamicPricingPerformance")
         and "orders.sales_order" not in ((ov_j.get("listDynamicPricingPerformance") or {}).get("reads") or []),
         "listDynamicPricingPerformance does not read the venue currency and the strategies, or still reads Orders (CR-407)")
    need("BR-PRICING-PERFORMANCE", "by `at`" not in ldp and "By `label`, then by `key`" in ldp,
         "listDynamicPricingPerformance orders by a member its row does not have, not by label then key (CR-407)")
    need("BR-PRICING-PERFORMANCE", "400" in (op("listDynamicPricingPerformance")[3].get("responses") or {})
         and "`400 validation` naming the parameter" in ldp,
         "listDynamicPricingPerformance does not refuse the comparisons and the market level it cannot answer (CR-407)")
    need("BR-PRICING-PERFORMANCE", "LO-CR407-001" in lo_j and "absent, not zero" in ldp
         and "incrementalRevenue" in sprops("DynamicPricingPerformanceOptimizationAnalyticsView"),
         "the KPIs CR-407 leaves out are not absent and on the left-out list, or the view lost an approved member")
    # BR-REVENUE-ROW (ADAM CR-408; CHG-CR408-001)
    lrv = descr("listRevenue")
    need("BR-REVENUE-ROW", "catalogue.demand_forecast" in reads_of("listRevenue"),
         "listRevenue does not declare its read of catalogue.demand_forecast (CR-408)")
    for frag in ("whose status is not `ignored`", "scheduled is `queued`", "most specific scope that matches",
                 "By `rankBy` (default `revenueOpportunity`)", "LO-CR408-001"):
        need("BR-REVENUE-ROW", frag in lrv, f"listRevenue does not state {frag!r} (CR-408)")
    need("BR-REVENUE-ROW", "Sorted by `optimizationId` descending" not in lrv and "LO-CR408-001" in lo_j,
         "listRevenue still orders by optimizationId against its rankBy, or the left-out figures are not listed (CR-408)")

    # ---------------------------------------------------------------- r12 CR lane K (CR-409 to CR-415; the lead, 31
    # October 2026: "Include them in r12"). Each rule fails on the r12 candidate (8535bc29) and passes on the decision.
    csch = ((op("listCompetitorPricingMarket")[4].get("components") or {}).get("schemas") or {})

    def cprops(name):
        return (csch.get(name) or {}).get("properties") or {}

    def desc(oid):
        return " ".join(str(op(oid)[3].get("description") or "").split())

    # BR-COMPETITOR-OBSERVATION (ADAM CR-409; CHG-CR409-001)
    cpo = csch.get("CompetitorPriceObservation") or {}
    need("BR-COMPETITOR-OBSERVATION", cpo.get("x-ticvai-persistence") == "catalogue.competitor_price_observation"
         and (cprops("CompetitorPriceObservation").get("demandSignalId") or {}).get("x-ticvai-references") == "catalogue.demand_signal"
         and "currencyCode" in (cpo.get("required") or []),
         "no catalogue.competitor_price_observation with its own currencyCode, keyed to catalogue.demand_signal (CR-409)")
    need("BR-COMPETITOR-OBSERVATION", {"catalogue.competitor_price_observation", "catalogue.demand_signal"} <= reads_of("listCompetitorPricingMarket"),
         "listCompetitorPricingMarket does not read the observations and their registry rows (CR-409)")
    lcp = desc("listCompetitorPricingMarket")
    for frag in ("median published price over the latest observation of each mapping", "never converted",
                 "previous observation of the same mapping", "Only observations in the venue's trading currency count"):
        need("BR-COMPETITOR-OBSERVATION", frag in lcp, f"listCompetitorPricingMarket does not state {frag!r} (CR-409)")
    vw = cprops("CompetitorPricingMarketPositionIntelligenceView")
    for p in ("marketMedianPrice", "positionVsMedian", "movementPercent", "historicalCorrelation"):
        need("BR-COMPETITOR-OBSERVATION", (vw.get(p) or {}).get("nullable") is True,
             f"CompetitorPricingMarketPositionIntelligenceView.{p} is not nullable, though it is null when missing (CR-409)")
    # BR-CONTEXTUAL-RULE (ADAM CR-410; CHG-CR410-001)
    dpr = cprops("PricingDynamicPriceRule")
    miss = {"dimension", "salesChannel", "customerSegment", "segmentRef", "locationLevel", "locationId",
            "dynamicPricingEnabled"} - set(dpr)
    need("BR-CONTEXTUAL-RULE", not miss, f"PricingDynamicPriceRule has no {sorted(miss)} (CR-410)")
    need("BR-CONTEXTUAL-RULE", (dpr.get("channelId") or {}).get("x-ticvai-references") == "catalogue.sales_channel",
         "PricingDynamicPriceRule.channelId does not key catalogue.sales_channel (CR-410)")
    need("BR-CONTEXTUAL-RULE", "contextual-rule-incomplete" in problem_types(op("setDynamicPriceRule")[3]),
         "setDynamicPriceRule does not answer 422 contextual-rule-incomplete (CR-410)")
    need("BR-CONTEXTUAL-RULE", reads_of("listChannelCustomerSegment") == {"pricing.dynamic_price_rule"}
         and "`rule_type` `contextual`" in desc("listChannelCustomerSegment"),
         "listChannelCustomerSegment does not list the rule_type contextual rows of pricing.dynamic_price_rule only (CR-410)")
    # BR-SALE-SCHEDULE-SUMMARY (ADAM CR-411; CHG-CR411-001)
    sms = cprops("ChannelSalesScheduleAvailabilityWindowsSummary")
    for p, v in sms.items():
        need("BR-SALE-SCHEDULE-SUMMARY", "CR-411" in str((v or {}).get("description") or ""),
             f"ChannelSalesScheduleAvailabilityWindowsSummary.{p} states no rule (CR-411)")
    need("BR-SALE-SCHEDULE-SUMMARY", "blackoutDates" in str((sms.get("blackouts") or {}).get("description")),
         "the blackouts figure is not counted from blackoutDates (CR-411)")
    need("BR-SALE-SCHEDULE-SUMMARY", "catalogue.product_channel_assignment" in reads_of("listChannelSaleSchedule"),
         "listChannelSaleSchedule does not read catalogue.product_channel_assignment for every-product windows (CR-411)")
    # BR-CHANNEL-ALLOCATION-COUNTS (ADAM CR-412; CHG-CR412-001)
    cal = cprops("ChannelAllocation")
    need("BR-CHANNEL-ALLOCATION-COUNTS", "allocationPercent" in cal and all((cal.get(p) or {}).get("readOnly") is True
         for p in ("releasedUnits", "returnedUnits")),
         "ChannelAllocation has no allocationPercent, or no readOnly releasedUnits and returnedUnits (CR-412)")
    need("BR-CHANNEL-ALLOCATION-COUNTS", "validation" in ((((op("setChannelAllocations")[3].get("responses") or {}).get("400") or {})
         .get("x-ticvai-problem-types")) or []), "setChannelAllocations' 400 does not list validation (CR-412)")
    need("BR-CHANNEL-ALLOCATION-COUNTS", "returned_units" in text(op("relinquishChannelAllocation")[3].get("x-ticvai-writes") or []),
         "relinquishChannelAllocation does not write returned_units (CR-412)")
    lic = desc("listInventoryCapacityChannel")
    need("BR-CHANNEL-ALLOCATION-COUNTS", "gives an empty page, not 400" in lic and "then by `id`" in lic
         and "catalogue.product" in reads_of("listInventoryCapacityChannel"),
         "listInventoryCapacityChannel does not state the product path, the empty page and a total order (CR-412)")
    # BR-CHANNEL-CODE-UNIQUE (ADAM CR-413; CHG-CR413-001)
    need("BR-CHANNEL-CODE-UNIQUE", (cprops("SalesChannelProfile").get("code") or {}).get("x-ticvai-unique") == "tenant",
         "SalesChannelProfile.code is not x-ticvai-unique: tenant (CR-413)")
    ccp = (op("createChannelProfile")[3].get("responses") or {})
    need("BR-CHANNEL-CODE-UNIQUE", "DuplicateCode" in text(ccp.get("409") or {}) and "validation" in text(ccp.get("400") or {}),
         "createChannelProfile does not answer 409 DuplicateCode and 400 validation (CR-413)")
    need("BR-CHANNEL-CODE-UNIQUE", (cprops("ChannelCreationProfileConfigurationInput").get("scopeId") or {}).get("format") == "uuid",
         "ChannelCreationProfileConfigurationInput.scopeId is not a uuid (CR-413)")
    need("BR-CHANNEL-CODE-UNIQUE", "kiosk -> kiosk" in " ".join(str((cprops("SalesChannelCommandCenterView").get("salesChannel") or {}).get("description")).split()),
         "the channelType -> salesChannel mapping has no kiosk -> kiosk (CR-413)")
    # BR-SALE-RULE-INSTANTS (ADAM CR-414; CHG-CR414-001)
    srv = cprops("ChannelSalesRulesLimitsRestrictionsView")
    for p in ("effectiveFrom", "effectiveTo"):
        need("BR-SALE-RULE-INSTANTS", (srv.get(p) or {}).get("format") == "date-time" and (srv.get(p) or {}).get("nullable") is True,
             f"ChannelSalesRulesLimitsRestrictionsView.{p} is not a nullable date-time (CR-414)")
    lsr = desc("listChannelSaleRule")
    need("BR-SALE-RULE-INSTANTS", "NULLS LAST" in lsr and "then by `id`" in lsr,
         "listChannelSaleRule's order puts no place for a null effectiveFrom or has no id last (CR-414)")
    # BR-PRICING-APPROVAL (ADAM CR-415; CHG-CR415-001)
    dpo = op("decidePricingRecommendation")[3]
    need("BR-PRICING-APPROVAL", "approvals.request" in {str(w.get("table")) for w in dpo.get("x-ticvai-writes") or []
                                                         if isinstance(w, dict)}
         and "approvals.createApprovalRequest` in process" in desc("decidePricingRecommendation"),
         "decidePricingRecommendation does not raise the request in process through createApprovalRequest (CR-415)")
    need("BR-PRICING-APPROVAL", "no-approval-route" in problem_types(dpo),
         "decidePricingRecommendation does not pass 422 no-approval-route through (CR-415)")
    dtx = desc("decidePricingRecommendation")
    need("BR-PRICING-APPROVAL", "always opens a request" in dtx and "above the caller" not in dtx
         and "writes no outbox event and no" in dtx,
         "decidePricingRecommendation still makes sendForApproval conditional, or writes an outbox event (CR-415)")
    st = load("states/pricing-recommendation.yaml")
    need("BR-PRICING-APPROVAL", not any("above the caller" in str(t.get("guard")) for t in st.get("transitions") or []),
         "states/pricing-recommendation.yaml still guards sendForApproval on the caller's level (CR-415)")
    for ev in ("approval-granted", "approval-rejected", "approval-expired", "approval-withdrawn"):
        cons = [c for c in load(f"events/{ev}.yaml").get("consumers") or [] if isinstance(c, dict)
                and c.get("context") == "catalogue" and "pricingRecommendation" in str(c.get("purpose"))]
        need("BR-PRICING-APPROVAL", bool(cons) and all("catalogue.pricing_recommendation" in (c.get("writes") or [])
             and c.get("idempotencyKey") == "requestId" for c in cons),
             f"events/{ev}.yaml has no catalogue consumer for subjectType pricingRecommendation (CR-415)")

    # ---------------------------------------------------------------- r12 CR lane M (the lead, 31 October 2026: "for
    # each one actually check if they hold and if not then find out the best way keeping in mind what client needs";
    # "Include them in r12"). Each rule fails on the r12 candidate before the posted decision and passes on it.
    def routes(o_):
        return {(str((v or {}).get("query")), str((v or {}).get("route"))) for v in o_.get("x-ticvai-read-via") or []
                if isinstance(v, dict)}

    xdr = load("docs/active/cross-deployable-writes.yaml")
    xdr_reads = {str((r or {}).get("id")): r for r in xdr.get("reads") or [] if isinstance(r, dict)}
    wsch = (wl.get("components") or {}).get("schemas") or {}

    # BR-BOOKING-FLOW-RESOLVE (ADAM CR-426, CR-427; CHG-CR426-001, CHG-CR427-001)
    dbf, gpb = op("deleteBookingFlow")[3], op("getPublishedBookingFlow")[3]
    for oid_, o_ in (("deleteBookingFlow", dbf), ("getPublishedBookingFlow", gpb)):
        for q in ("catalogue#productRecords", "catalogue#productCategoryRecords"):
            need("BR-BOOKING-FLOW-RESOLVE", (q, "in-process") in routes(o_),
                 f"{oid_} does not ask {q} in process from the operations host (CR-426/CR-427, XDR-051)")
    x51 = xdr_reads.get("XDR-051") or {}
    need("BR-BOOKING-FLOW-RESOLVE", {"deleteBookingFlow", "getPublishedBookingFlow"} <= set(x51.get("operations") or [])
         and {"catalogue#productRecords", "catalogue#productCategoryRecords"} <= set(x51.get("queries") or []),
         "docs/active/cross-deployable-writes.yaml XDR-051 does not grant deleteBookingFlow's and getPublishedBookingFlow's "
         "two Catalogue reads (CR-426/CR-427)")
    dd = words(dbf.get("description"))
    for frag in ("no other enabled default flow of the venue has a type that lists the same kind",
                 "`isSellable` true, `guestListing` `bookable`", "`onSaleFrom` and `onSaleTo` where they are set",
                 "neither it nor its category names a flow"):
        need("BR-BOOKING-FLOW-RESOLVE", frag in dd, f"deleteBookingFlow does not say {frag!r} (CR-426)")
    gd = words(gpb.get("description"))
    for frag in ("lists the kind earliest", "comes first in `x-ticvai-system-catalogue`",
                 "falls through to the next step", "the answer is 400 `validation`", "most recently updated flow decides nothing"):
        need("BR-BOOKING-FLOW-RESOLVE", frag in gd, f"getPublishedBookingFlow does not say {frag!r} (CR-427)")
    need("BR-BOOKING-FLOW-RESOLVE", "400" in {str(k) for k in (gpb.get("responses") or {})},
         "getPublishedBookingFlow declares no 400 for a call with none of productId, productCategoryId and flowTypeKey (CR-427)")

    # BR-FLOW-TYPE-CATALOGUE (ADAM CR-428; CHG-CR428-001)
    bft = wsch.get("BookingFlowType") or {}
    cat = bft.get("x-ticvai-system-catalogue") or {}
    names_en = ["Dated day pass", "Timed entry", "Open-dated", "Seated fixed performance",
                "Seated date, time and seat map", "Experience or workshop", "Surf or session",
                "Meeting room by the hour", "Cabana on a map", "Guided tour by language", "Transport",
                "Table reservation", "Membership", "Gift card", "Several locations"]

    def loc(v):
        return isinstance(v, dict) and bool(str(v.get("en") or "").strip()) and bool(str(v.get("ar") or "").strip())

    types_ = cat.get("types") or []
    need("BR-FLOW-TYPE-CATALOGUE", [(t or {}).get("name", {}).get("en") if isinstance((t or {}).get("name"), dict)
                                    else None for t in types_] == names_en,
         "the system catalogue's type names are not the 15 English names CMS-103 shows, in catalogue order (CR-428)")
    for t in types_:
        k = (t or {}).get("key")
        need("BR-FLOW-TYPE-CATALOGUE", loc(t.get("name")) and loc(t.get("description")),
             f"catalogue type {k} has no name and description as {{en, ar}} (CR-428)")
        for s in t.get("steps") or []:
            if "condition" in (s or {}):
                need("BR-FLOW-TYPE-CATALOGUE", loc(s.get("condition")),
                     f"catalogue type {k} step {s.get('stepKey')}: condition is not {{en, ar}} (CR-428)")
    for k, v in (cat.get("commonConditions") or {}).items():
        need("BR-FLOW-TYPE-CATALOGUE", loc(v), f"commonConditions.{k} is not {{en, ar}} (CR-428)")
    lbt = words(op("listBookingFlowTypes")[3].get("description"))
    need("BR-FLOW-TYPE-CATALOGUE", "Sorted by `name`" not in lbt and "**Order.** Catalogue order" in lbt
         and "`commonConditions[stepKey]`" in lbt and "counting from 0" in lbt,
         "listBookingFlowTypes does not answer in catalogue order with the condition and defaultSortOrder rules (CR-428)")

    # BR-BOOKING-FLOW-WRITES (ADAM CR-429; CHG-CR429-001)
    for oid_ in ("createBookingFlowDefinition", "updateBookingFlowDefinition"):
        o_ = op(oid_)[3]
        need("BR-BOOKING-FLOW-WRITES", ("marketing-crm#consentQuestionRecords", "in-process") in routes(o_)
             and "marketing-crm#guestMatchPolicyRecords" not in {q for q, _r in routes(o_)},
             f"{oid_} does not read consentQuestionRecords in process, or still reads guestMatchPolicyRecords (CR-429)")
        p400 = ptypes(o_, "400")
        need("BR-BOOKING-FLOW-WRITES", {"step-not-in-flow-type", "duplicate-flow-step", "consent-question-not-active"} <= p400
             and not ({"step-not-in-type", "step-given-twice"} & p400),
             f"{oid_}'s 400 does not name step-not-in-flow-type, duplicate-flow-step and consent-question-not-active "
             f"only ({sorted(p400)}; CR-429)")
        need("BR-BOOKING-FLOW-WRITES", "added at its index in the type" in words(o_.get("description")),
             f"{oid_} does not say a step left out is added at its index with the type's defaultEnabled (CR-429)")
    mq = (load("contracts/satellite/marketing-crm.yaml").get("x-ticvai-queries") or {}).get("consentQuestionRecords") or {}
    need("BR-BOOKING-FLOW-WRITES", "in-process" in (mq.get("served") or []),
         "marketing-crm#consentQuestionRecords is not served in process (CR-429)")
    lbf200 = words(((op("listBookingFlows")[3].get("responses") or {}).get("200") or {}).get("description"))
    need("BR-BOOKING-FLOW-WRITES", "defaults first" not in lbf200,
         "listBookingFlows' 200 still says 'defaults first' beside its Order paragraph (CR-429)")

    # BR-GUEST-CONTACT-FIELDS (ADAM CR-430; CHG-CR430-001)
    sbc = op("setBookingFlowConfig")[3]
    need("BR-GUEST-CONTACT-FIELDS", ("tenancy#activeVenues", "in-process") in routes(sbc)
         and ("marketing-crm#guestMatchPolicyRecords", "in-process") in routes(sbc),
         "setBookingFlowConfig does not ask tenancy#activeVenues and guestMatchPolicyRecords in process (CR-430)")
    sbd = words(sbc.get("description"))
    for frag in ("with no row it is the default, `matchBy` `email`", "`email` or `mobile` for `emailOrMobile`",
                 "else the tenant's, else `[email]`"):
        need("BR-GUEST-CONTACT-FIELDS", frag in sbd, f"setBookingFlowConfig does not say {frag!r} (CR-430)")
    gcf = words((((wsch.get("BookingFlowSettings") or {}).get("properties") or {}).get("guestContactFields") or {})
                .get("description"))
    need("BR-GUEST-CONTACT-FIELDS", "identity `GuestMatchPolicy" not in gcf and "marketing-crm `GuestMatchPolicy`" in gcf,
         "BookingFlowSettings.guestContactFields still calls the match policy identity's (it is marketing-crm's; CR-430)")
    need("BR-GUEST-CONTACT-FIELDS", "setBookingFlowConfig" in ((xdr_reads.get("XDR-022") or {}).get("operations") or []),
         "XDR-022 does not list setBookingFlowConfig's in-process tenancy#activeVenues (CR-430)")

    # BR-GUEST-CODE-UNKNOWN (ADAM CR-431, changing one point of CR-370's follow-up; CHG-CR431-001)
    rgo, vgo = op("requestGuestOtp")[3], op("verifyGuestOtp")[3]
    rgd_ = words(rgo.get("description"))
    need("BR-GUEST-CODE-UNKNOWN", "nothing is written for the code" not in rgd_
         and "generated and never sent" in rgd_ and "whether or not the identifier has an account" in rgd_,
         "requestGuestOtp does not write the never-sent otp_challenge row for an unknown login, passwordReset or stepUp "
         "identifier, or does not say the 429 answers alike (CR-431)")
    v401 = words(((vgo.get("responses") or {}).get("401") or {}).get("description"))
    need("BR-GUEST-CODE-UNKNOWN", "subject-null `login`, `passwordReset` or `stepUp` row" in v401,
         "verifyGuestOtp's 401 does not refuse a code against a subject-null login, passwordReset or stepUp row (CR-431)")

    # BR-GUEST-CHECKOUT-PROOF (ADAM CR-432, with the lead's answer of 31 October 2026; CHG-CR432-001)
    sec = vgo.get("security")
    need("BR-GUEST-CHECKOUT-PROOF", isinstance(sec, list) and {} in sec and {"guestAuth": []} in sec,
         "verifyGuestOtp's security is not none beside guestAuth (the cart's anonymous session, CR-432)")
    need("BR-GUEST-CHECKOUT-PROOF", "204" in {str(k) for k in (vgo.get("responses") or {})}
         and "no subject is created and no `GuestSession` is issued" in words(vgo.get("description")),
         "verifyGuestOtp does not answer a guest-checkout code 204 with no subject and no GuestSession (CR-432)")
    oags = words(((load("contracts/spine/identity.yaml").get("x-ticvai-queries") or {}).get("openAnonymousGuestSession")
                  or {}).get("rule"))
    need("BR-GUEST-CHECKOUT-PROOF", "verifiedContactRef" in oags,
         "openAnonymousGuestSession does not say the session holds the proved verifiedContactRef (CR-432)")
    cco = words(op("checkoutCart")[3].get("description"))
    need("BR-GUEST-CHECKOUT-PROOF", "takes `verifiedContactRef` from the session" in cco
         and "`subjectId` null" in cco,
         "checkoutCart does not take verifiedContactRef from the anonymous session and write a subject-less order (CR-432)")
    need("BR-GUEST-CHECKOUT-PROOF", "Both routes produce a guest profile" not in words(op("verifyGuestEmail")[3]
                                                                                       .get("description")),
         "verifyGuestEmail still says both routes produce a guest profile (a profile is made only with an account; "
         "CR-432, the lead's answer)")

    # BR-DELEGATION-CYCLE (ADAM CR-433, item (6) beside CR-362's (1) to (5); CHG-CR433-001)
    drq = (load("contracts/spine/identity.yaml").get("x-ticvai-queries") or {}).get("delegationReaches") or {}
    need("BR-DELEGATION-CYCLE", "ITenantRootGrant" in str(drq.get("rule") or "") and "recursive" in str(drq.get("rule") or "")
         and set(((drq.get("returns") or {}).get("properties") or {})) == {"reaches"}
         and set(drq.get("inputs") or {}) == {"fromSubjectId", "toSubjectId"} and drq.get("served") == ["in-process"],
         "identity#delegationReaches is not a yes/no rule question (fromSubjectId, toSubjectId -> reaches) answered under "
         "ITenantRootGrant in process (CR-433)")
    gdo2 = op("grantDelegation")[3]
    need("BR-DELEGATION-CYCLE", ("identity#delegationReaches", "in-process") in routes(gdo2),
         "grantDelegation does not ask identity#delegationReaches in process (CR-433)")
    need("BR-DELEGATION-CYCLE", "transaction advisory lock" in words(gdo2.get("description")),
         "grantDelegation does not run the cycle check and the insert under one transaction advisory lock (CR-433)")

    # BR-WEBHOOK-REPLAY-TENANT (ADAM CR-434; CHG-CR434-001)
    wrj = ((load("contracts/satellite/public-api.yaml").get("components") or {}).get("schemas") or {}).get("WebhookReplayJob") or {}
    wtd = words(((wrj.get("properties") or {}).get("tenantId") or {}).get("description"))
    need("BR-WEBHOOK-REPLAY-TENANT", "tenantId" in (wrj.get("required") or [])
         and "allowed_tenant_ids holds exactly one tenant" in wtd and "delete nothing" in wtd and "SET NOT NULL" in wtd,
         "WebhookReplayJob.tenantId does not state CR-434's backfill, stop and SET NOT NULL steps")

    # BR-OUTBOX-REPUBLISH-READS (ADAM CR-435; CHG-CR435-001)
    rpo = op("republishOutbox")[3]
    need("BR-OUTBOX-REPUBLISH-READS", not rpo.get("x-ticvai-read-via")
         and "partition catalogue" in words(rpo.get("description")),
         "republishOutbox declares a read it does not make, or does not name the partition-catalogue bound (CR-435)")
    need("BR-OUTBOX-REPUBLISH-READS", "platform.outbox" not in ((lin.get("republishOutbox") or {}).get("reads") or []),
         "the lineage has republishOutbox reading platform.outbox rows (handoff/api-data-lineage-overrides.json; CR-435)")

    # ---------------------------------------------------------------- r13 lane r (ADAM CR-472 to CR-478, decided by
    # Chinmay on 2 November 2026, "approve all as a recommended"). Each rule fails on the r12 contract and passes on
    # the posted decision.
    def via_of(o_):
        return {(str((v or {}).get("query")), str((v or {}).get("route"))) for v in o_.get("x-ticvai-read-via") or []
                if isinstance(v, dict)}

    def asks(o_):
        return {q for q, _ in via_of(o_)}

    xdr13 = {str((r or {}).get("id")): r for r in (load("docs/active/cross-deployable-writes.yaml").get("reads") or [])
             if isinstance(r, dict)}

    def w13(x):
        return " ".join(str(x or "").split())

    # BR-FORM-LIVE-ACCEPTANCE (CR-472)
    sbf = op("submitForm")[3]
    need("BR-FORM-LIVE-ACCEPTANCE", not any(q.startswith("identity#") for q in asks(sbf))
         and "pii.subject" not in ((lin.get("submitForm") or {}).get("reads") or []),
         "submitForm still reads pii.subject (a read-via of Identity or a lineage read; CR-472)")
    need("BR-FORM-LIVE-ACCEPTANCE", any(isinstance(r, dict) and r.get("table") == "marketing.waiver_version_control"
                                        for r in sbf.get("x-ticvai-reads") or []),
         "submitForm does not read marketing.waiver_version_control, its own data, for the resign rule (CR-472)")
    sd = w13(sbf.get("description"))
    for frag in ("both null or both equal", "`expires_at` later than now", "is `noResign`",
                 "`resignAtNextBooking` or `resignBeforeNextVisit`, or the version has no resign rule",
                 "with that submission and nothing is written", "It checks no one''s age".replace("''", "'")):
        need("BR-FORM-LIVE-ACCEPTANCE", frag in sd, f"submitForm does not say {frag!r} (CR-472)")

    # BR-SEO-METADATA-STORE (CR-474)
    ssm = op("setSeoMetadata")[3]
    need("BR-SEO-METADATA-STORE", not any(q.startswith("catalogue#") for q in asks(ssm))
         and "catalogue.product" not in ((lin.get("setSeoMetadata") or {}).get("reads") or []),
         "setSeoMetadata still reads catalogue.product (a read-via of Catalogue or a lineage read; CR-474)")
    smd = w13(ssm.get("description"))
    for frag in ("does not check that the entity exists", "it does not refuse and does not write a redirect",
                 "`createUrlRedirect` (POST /seo-redirects, #33242)"):
        need("BR-SEO-METADATA-STORE", frag in smd, f"setSeoMetadata does not say {frag!r} (CR-474)")

    # BR-CONFIG-DIFF-PRODUCTS (CR-475)
    dcv = op("diffConfigVersion")[3]
    for q in ("catalogue#productRecords", "catalogue#productCategoryRecords"):
        need("BR-CONFIG-DIFF-PRODUCTS", (q, "in-process") in via_of(dcv),
             f"diffConfigVersion does not ask {q} in process from the operations host (CR-475, XDR-051)")
    dcd = w13(dcv.get("description"))
    for frag in ("the product''s own `bookingFlowId`, else its category''s `bookingFlowId`, else the venue''s default "
                 "flow whose type lists the product''s kind".replace("''", "'"), "where {bookingFlowId} or {venueId}"):
        need("BR-CONFIG-DIFF-PRODUCTS", frag in dcd, f"diffConfigVersion does not say {frag!r} (CR-475)")

    # BR-PREVIEW-READS-NOTHING (CR-476)
    cpv = op("createPreview")[3]
    # ADAM CR-507 (3 November 2026): createPreview asks the two address reads getPlatformSubdomain asks, and nothing else
    cpv_q = {str((v or {}).get("query")) for v in cpv.get("x-ticvai-read-via") or [] if isinstance(v, dict)}
    need("BR-PREVIEW-READS-NOTHING", cpv_q <= {"platform-ops#tenantDomainRecords", "subscription#cellRecords"},
         "createPreview asks a query beyond its address reads; the renderer in the workers host reads Catalogue and "
         "Orders, not it (CR-476, CR-507)")
    need("BR-PREVIEW-READS-NOTHING", not any(r.get("reader") == "operations" and "orders.ticket_template"
                                             in (r.get("tables") or []) for r in xdr13.values()),
         "a reads entry grants the operations role orders.ticket_template (CR-476: no grant)")
    ttr = (load("contracts/spine/orders.yaml").get("x-ticvai-queries") or {}).get("ticketTemplateRecords") or {}
    need("BR-PREVIEW-READS-NOTHING", "in-process" in (ttr.get("served") or []),
         "orders#ticketTemplateRecords is not served in process (Orders' in-process query class; CR-476)")
    prq = load("events/preview-requested.yaml")
    pur = w13(" ".join(str((c or {}).get("purpose") or "") for c in prq.get("consumers") or []))
    need("BR-PREVIEW-READS-NOTHING", "catalogue#productRecords (ids [productId]) and orders#ticketTemplateRecords in "
         "process" in pur, "preview.requested's consumer does not ask its two reads in process (CR-476)")

    # BR-SHOP-DROP-ORDER-LINES (CR-477)
    csd = op("createShopAndDrop")[3]
    need("BR-SHOP-DROP-ORDER-LINES", ("orders#orderLineRecords", "in-process") in via_of(csd)
         and ("fnb#deliveryLocationRecords", "in-process") in via_of(csd),
         "createShopAndDrop does not ask orders#orderLineRecords (and fnb#deliveryLocationRecords) in process (CR-477)")
    x71 = xdr13.get("XDR-071") or {}
    need("BR-SHOP-DROP-ORDER-LINES", x71.get("reader") == "operations" and x71.get("tables") == ["orders.order_line"]
         and "orders#orderLineRecords" in (x71.get("queries") or []),
         "XDR-071 does not grant the operations role SELECT on orders.order_line for orderLineRecords (CR-477)")
    cdd = w13(csd.get("description"))
    for frag in ("An `orderId` with no visible line is `422 unknown-order`", "not one of those lines is `422 unknown-line`"):
        need("BR-SHOP-DROP-ORDER-LINES", frag in cdd, f"createShopAndDrop does not say {frag!r} (CR-477)")

    # BR-MERCH-LIVE-PRICE (CR-478)
    lkm = op("lookupMerchandise")[3]
    for q in ("tenancy#workstationRecords", "promotions#liveEffectivePrice", "tenancy#venueSettingsRecords"):
        need("BR-MERCH-LIVE-PRICE", (q, "in-process") in via_of(lkm),
             f"lookupMerchandise does not ask {q} in process (CR-478)")
    lep = (load("contracts/satellite/promotions.yaml").get("x-ticvai-queries") or {}).get("liveEffectivePrice") or {}
    need("BR-MERCH-LIVE-PRICE", "in-process" in (lep.get("served") or [])
         and "promotions.promotion_rule" in (lep.get("reads") or [])
         and "the same evaluation code evaluatePromotions uses (#31714)" in w13(lep.get("rule")),
         "promotions#liveEffectivePrice is not an in-process query class reading promotion_rule and running "
         "evaluatePromotions' code (CR-478)")
    x72 = xdr13.get("XDR-072") or {}
    need("BR-MERCH-LIVE-PRICE", x72.get("reader") == "operations"
         and x72.get("tables") == ["promotions.promotion", "promotions.promotion_rule"],
         "XDR-072 does not grant the operations role SELECT on promotions.promotion and promotion_rule (CR-478)")
    need("BR-MERCH-LIVE-PRICE", "one item per merchandise (`itemRef` the merchandise id, `unitPrice` its list price)"
         in w13(lkm.get("description")), "lookupMerchandise does not state liveEffectivePrice's inputs (CR-478)")
    channel_rules_r13(need, op)
    lane_p_rules_r13(need, op, ops)
    lane_w5_rules_r13(need, op, ops)
    lane_w3_rules_r13(need, op)
    lane_w1_rules_r13(need, op)
    lane_b_rules_r14(need, op)

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
             "BR-KIOSK-LISTS", "BR-KIOSK-DELETE", "BR-KIOSK-COUNT", "BR-KIOSK-CHANNEL", "BR-KIOSK-FINDINGS",
             "BR-KIOSK-RESTORE", "BR-BANNER-OUTSIDE-DRAFT", "BR-BANNER-STATE",
             "BR-UAEPASS-ENDPOINTS", "BR-LINK-CHECKOUT", "BR-DELEGATION-READS", "BR-GUEST-POLICY-CURRENCY",
             "BR-CONTENT-PAGE-KEY", "BR-CONTENT-PUBLISH",
             "BR-CONTENT-BLOCK", "BR-SCOPE-LOOKUP", "BR-ID-RESUBMIT", "BR-DOC-NUMBER-ENC", "BR-REGISTER-SOURCE",
             "BR-GUEST-CODE-DELIVERY", "BR-BEACON-GEOFENCE", "BR-FACE-TAG-PROFILE", "BR-FACE-PASS-REVOKE",
             "BR-POLICY-VERSIONS", "BR-CONTENT-PAGE-SWITCH", "BR-GUIDED-CHOICE-TARGETS",
             "BR-GUEST-SETTINGS", "BR-BILLING-LINES", "BR-SHOP-DROP-COLLECT", "BR-DELEGATION-KEY", "BR-FOREIGN-TENDER",
             "BR-PRODUCT-FROM-PRICE",
             "BR-BOOKING-FLOW-MISSING", "BR-CALL-DISPOSITION", "BR-RESTORE-MISSING-PAGE",
             "BR-DASHBOARD-COST", "BR-DASHBOARD-ENTITLEMENT", "BR-TILE-MARKS", "BR-AUDIT-REASON",
             "BR-PRIVACY-CONSENT", "BR-GUEST-BROADCAST", "BR-OPEN-SHIFT-CLAIM",
             "BR-GATE-MODE-POLICY", "BR-ACCESS-POINT-ACTIVE", "BR-WHITELIST-APPROVAL", "BR-ADMISSION-CREATE",
             "BR-PRICING-QUEUE-MEMBERS", "BR-PRICING-AUTOMATION-LEVEL", "BR-PRICING-SCORECARD", "BR-PRICE-SIMULATION",
             "BR-CALC-PROFILE-VERSION", "BR-ROLLBACK-CANCEL", "BR-LIVE-PRICE", "BR-STRATEGY-FIGURES",
             "BR-PRICE-BAND-ORDER", "BR-GUARDRAIL-SCOPE",
             "BR-SEAT-MAP-SECTIONS", "BR-SEAT-TEMPLATE-COPY", "BR-SEAT-MAP-UPDATE", "BR-FORECAST-CURVE",
             "BR-ELASTICITY-CONTEXT", "BR-PRICING-PERFORMANCE", "BR-REVENUE-ROW",
             "BR-COMPETITOR-OBSERVATION", "BR-CONTEXTUAL-RULE", "BR-SALE-SCHEDULE-SUMMARY",
             "BR-CHANNEL-ALLOCATION-COUNTS", "BR-CHANNEL-CODE-UNIQUE", "BR-SALE-RULE-INSTANTS", "BR-PRICING-APPROVAL",
             "BR-BOOKING-FLOW-RESOLVE", "BR-FLOW-TYPE-CATALOGUE", "BR-BOOKING-FLOW-WRITES", "BR-GUEST-CONTACT-FIELDS",
             "BR-GUEST-CODE-UNKNOWN", "BR-GUEST-CHECKOUT-PROOF", "BR-DELEGATION-CYCLE", "BR-WEBHOOK-REPLAY-TENANT",
             "BR-OUTBOX-REPUBLISH-READS",
             "BR-VARIANT-PRICE", "BR-ELASTICITY-LABELS", "BR-CHANGE-IMPACT", "BR-PRODUCT-WORKFLOW", "BR-FEE-INSTANTS",
             "BR-SEAT-RULE-OVERLAP", "BR-TAX-PROFILE-LIST",
             "BR-FORM-LIVE-ACCEPTANCE", "BR-SEO-METADATA-STORE", "BR-CONFIG-DIFF-PRODUCTS", "BR-PREVIEW-READS-NOTHING",
             "BR-SHOP-DROP-ORDER-LINES", "BR-MERCH-LIVE-PRICE",
             "BR-R13-UPSERT-KEY", "BR-R13-WALLET-TRANSFER-ETAG", "BR-R13-GUEST-ROWS", "BR-R13-REPRINT-GUEST",
             "BR-R13-WRITES-LISTED", "BR-R13-READS-DECLARED", "BR-R13-FIELDS-KEPT", "BR-R13-ONE-RULE"] + LANE_Q_R13_RULES + LANE_W2_R13_RULES + R13_O_RULES + R13_LANE_P_RULES + R13_W5_RULES + R13_W3_RULES + R13_W4_RULES + R13_W1_RULES + R14_B_RULES
    for r in rules:
        print(f"  {r:18} {len(errors.get(r, [])):3d}")
        for m in errors.get(r, [])[:12]:
            print(f"      {m}")
    print(f"  {len(PAIR_EXEMPT)} create/update pair(s) exempt with a reason")
    print(f"\n{'FAIL' if total else 'PASS'} - {total} finding(s) against the 3 October business rules")
    return 1 if total else 0


R13_LANE_P_RULES = ["BR-PRIVACY-CHANGE-SET", "BR-PRIVACY-POLICY-GRANT", "BR-OPEN-SHIFT-COMPLETE",
                    "BR-MESSAGE-DISPATCH-BODY", "BR-LICENCE-IN-FORCE", "BR-DASHBOARD-GET-HIDDEN",
                    "BR-PRIVACY-CONSENT-READINGS", "BR-CONTENT-BLOCK-APPROVAL"]


def lane_p_rules_r13(need, op, ops):
    """r13 lane p (ADAM CR-437, CR-440, CR-441, CR-442, CR-449, CR-450, CR-469, CR-462; the lead, 1 November 2026
    "Approve all", and 2 November 2026 "approve all as a recommended" and, for CR-462, "Yes to both"). Each fails on
    the r12 contract.

      BR-PRIVACY-CHANGE-SET       (CR-437) the change set's items are stored whole (jsonb) and approvalRequestId is a
                                  declared key into approvals.request.
      BR-PRIVACY-POLICY-GRANT     (CR-440) listPrivacyConsent asks white-label#policyRecords under the tenant root
                                  grant, and every other read under the caller's.
      BR-OPEN-SHIFT-COMPLETE      (CR-441) OpenShift requires venueId, positionCode, from and to, from before to; any
                                  other operation that writes workforce.open_shift declares a 400; claimOpenShift's 409
                                  names open-shift-incomplete.
      BR-MESSAGE-DISPATCH-BODY    (CR-442) MessageDispatch carries body and the non-unique (sourceRef, subjectId,
                                  channel) index; sendGuestBroadcast writes in the inbox's transaction after a check
                                  and leaves the sending to Marketing's message sender; guest codes send through it.
      BR-LICENCE-IN-FORCE         (CR-449) LicencePosition states the in-force contract rule, and no contract takes
                                  the licensed modules from control.tenant.plan_id.
      BR-DASHBOARD-GET-HIDDEN     (CR-450) getDashboard asks the licence reads and answers 404 for a hidden dashboard.
      BR-PRIVACY-CONSENT-READINGS (CR-469) listPrivacyConsent ranks the warning codes in their stated order, maps every
                                  ConsentSource value onto the banner channels, keeps a venue's ancestor policies and
                                  sorts undated items last.
      BR-CONTENT-BLOCK-APPROVAL   (CR-462) publishContentBlock keeps the asked-for schedule in the approval request's
                                  attributes and reads it back through approvals#requestRecords; approval.granted,
                                  rejected, withdrawn and expired each have a white-label consumer that writes
                                  whitelabel.content_block.
    """
    def words(x):
        return " ".join(str(x or "").split())

    def vias(o_):
        return {str((v or {}).get("query")): words((v or {}).get("for"))
                for v in o_.get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def schemas(rel):
        return (load(rel).get("components") or {}).get("schemas") or {}

    mkt = schemas("contracts/satellite/marketing-crm.yaml")

    # BR-PRIVACY-CHANGE-SET (CR-437)
    pcs = (mkt.get("PrivacyConfigurationTestingApprovalPublicationView") or {}).get("properties") or {}
    it, ar = pcs.get("items") or {}, pcs.get("approvalRequestId") or {}
    need("BR-PRIVACY-CHANGE-SET", it.get("x-ticvai-persistence-column") == "jsonb" and it.get("x-ticvai-persisted") is not False
         and "written whole on each save" in words(it.get("description")),
         "PrivacyConfigurationTestingApprovalPublicationView.items is not stored whole as jsonb (CR-437)")
    need("BR-PRIVACY-CHANGE-SET", ar.get("x-ticvai-references") == "approvals.request",
         "PrivacyConfigurationTestingApprovalPublicationView.approvalRequestId declares no key into approvals.request "
         "(CR-437)")

    # BR-PRIVACY-POLICY-GRANT (CR-440)
    lpc = op("listPrivacyConsent")[3]
    lpd = words(lpc.get("description"))
    need("BR-PRIVACY-POLICY-GRANT", "ITenantRootGrant" in vias(lpc).get("white-label#policyRecords", ""),
         "listPrivacyConsent does not ask white-label#policyRecords under the tenant root grant (CR-440)")
    need("BR-PRIVACY-POLICY-GRANT", "Every other read is under the caller's grant" in lpd,
         "listPrivacyConsent does not say every other read is under the caller's grant (CR-440)")

    # BR-PRIVACY-CONSENT-READINGS (CR-469)
    order = ["capturePointWithoutNotice", "policyExpired", "purposeWithoutLawfulBasis",
             "purposeWordingDiffersByChannel", "translationMissing"]
    ranked = ", ".join(f"`{c}`" for c in order) + "; within a code, by `configurationId`, nulls last"
    need("BR-PRIVACY-CONSENT-READINGS", ranked in lpd,
         "listPrivacyConsent does not rank its warning codes in CR-378's order, then by configurationId nulls last "
         "(CR-469)")
    need("BR-PRIVACY-CONSENT-READINGS",
         "With no privacy policy in force, every consent purpose raises `policyExpired`" in lpd,
         "listPrivacyConsent does not say what happens with no privacy policy in force (CR-469)")
    need("BR-PRIVACY-CONSENT-READINGS", "sort after every dated item, by id" in lpd,
         "listPrivacyConsent does not sort undated items after every dated item, by id (CR-469)")
    need("BR-PRIVACY-CONSENT-READINGS", "an ancestor's, the tenant root included" in lpd
         and "Venue: `scopePath` at or beneath" not in lpd,
         "listPrivacyConsent's venue filter drops the tenant's policies (CR-469)")
    chan = lpd.split("Channel (ADAM CR-469)", 1)[-1].split("Language:", 1)[0] if "Channel (ADAM CR-469)" in lpd else ""
    for v in (mkt.get("ConsentSource") or {}).get("enum") or []:
        need("BR-PRIVACY-CONSENT-READINGS", f"`{v}`" in chan,
             f"listPrivacyConsent's channel filter does not say what ConsentSource {v} maps to on banners and "
             "tracking technologies (CR-469)")
    need("BR-PRIVACY-CONSENT-READINGS", "channel filter does not narrow them" in chan,
         "listPrivacyConsent narrows consent purposes and preference types (message channels) by a ConsentSource "
         "(CR-469)")

    # BR-OPEN-SHIFT-COMPLETE (CR-441)
    osh = schemas("contracts/satellite/workforce.yaml").get("OpenShift") or {}
    osd = words(osh.get("description"))
    need("BR-OPEN-SHIFT-COMPLETE", {"venueId", "positionCode", "from", "to"} <= set(osh.get("required") or []),
         "OpenShift does not require venueId, positionCode, from and to (CR-441)")
    need("BR-OPEN-SHIFT-COMPLETE", "with `from` before `to`" in osd and "reported, not guessed" in osd,
         "OpenShift does not state from before to and the checked NOT NULL migration (CR-441)")
    need("BR-OPEN-SHIFT-COMPLETE", "open-shift-incomplete" in ptypes(op("claimOpenShift")[3], "409"),
         "claimOpenShift's 409 does not name open-shift-incomplete (CR-441)")
    for oid, (_f, _p, _m, o_, _d) in sorted(ops.items()):
        if oid == "claimOpenShift":
            continue
        if any((w or {}).get("table") == "workforce.open_shift"
               for w in o_.get("x-ticvai-writes") or [] if isinstance(w, dict)):
            need("BR-OPEN-SHIFT-COMPLETE", "400" in (o_.get("responses") or {}),
                 f"{oid} writes an open shift and declares no 400 for a missing venueId, positionCode, from or to "
                 "(CR-441)")

    # BR-MESSAGE-DISPATCH-BODY (CR-442)
    md = mkt.get("MessageDispatch") or {}
    body = (md.get("properties") or {}).get("body") or {}
    need("BR-MESSAGE-DISPATCH-BODY", body.get("type") == "string" and body.get("nullable") is True,
         "MessageDispatch has no nullable body, the resolved message as sent (CR-442)")
    need("BR-MESSAGE-DISPATCH-BODY", ["sourceRef", "subjectId", "channel"] in (md.get("x-ticvai-index") or []),
         "MessageDispatch has no non-unique index on (sourceRef, subjectId, channel) (CR-442)")
    sgb = words(op("sendGuestBroadcast")[3].get("description"))
    for frag in ("written in the inbox's transaction", "after a check that no row", "Marketing's message sender",
                 "dead-letters"):
        need("BR-MESSAGE-DISPATCH-BODY", frag in sgb, f"sendGuestBroadcast does not say {frag!r} (CR-442)")
    need("BR-MESSAGE-DISPATCH-BODY",
         "Marketing's message sender" in words(op("sendGuestOneTimeCode")[3].get("description")),
         "sendGuestOneTimeCode does not send through Marketing's message sender (CR-442)")

    # BR-LICENCE-IN-FORCE (CR-449)
    lp = schemas("contracts/satellite/subscription.yaml").get("LicencePosition") or {}
    lpt = words(lp.get("description"))
    for frag in ("its status is not `expired`", "`startsAt` is on or before today",
                 "`cancelledAt` is null or after today", "`core` always licensed", "not `control.tenant.plan_id`"):
        need("BR-LICENCE-IN-FORCE", frag in lpt, f"LicencePosition does not state {frag!r} of the in-force rule (CR-449)")
    for f in sorted((ROOT / "contracts").rglob("*.yaml")):
        if "frozen" in f.parts:
            continue
        need("BR-LICENCE-IN-FORCE", "control.tenant.plan_id -> control.plan_module" not in words(f.read_text(encoding="utf-8")),
             f"{f.relative_to(ROOT)} still takes the licensed modules from control.tenant.plan_id (CR-449)")

    # BR-CONTENT-BLOCK-APPROVAL (CR-462)
    pcb = op("publishContentBlock")[3]
    pcd = words(pcb.get("description"))
    need("BR-CONTENT-BLOCK-APPROVAL", vias(pcb).get("approvals#requestRecords") is not None
         and any((v or {}).get("query") == "approvals#requestRecords" and (v or {}).get("route") == "in-process"
                 for v in pcb.get("x-ticvai-read-via") or [] if isinstance(v, dict)),
         # in process since the r13 integration (CHG-R13INT-013): the operations host asks Approvals' queries in
         # process under lane r's class rule (CHG-R13INP-001), which CR-462's "service route" predated
         "publishContentBlock's approval.granted consumer does not read approvals#requestRecords in process (CR-462, "
         "CHG-R13INT-013)")
    need("BR-CONTENT-BLOCK-APPROVAL", "with `attributes` set to `publishAt` and `expireAt` exactly as sent" in pcd
         and "the block stays a draft" not in pcd,
         "publishContentBlock does not keep the asked-for schedule in the approval request's attributes, or still "
         "says a rejected block stays a draft (CR-462)")
    for ev in ("granted", "rejected", "withdrawn", "expired"):
        evd = load(f"events/approval-{ev}.yaml")
        need("BR-CONTENT-BLOCK-APPROVAL", any((c or {}).get("context") == "white-label"
                                              and "whitelabel.content_block" in ((c or {}).get("writes") or [])
                                              for c in evd.get("consumers") or []),
             f"approval.{ev} has no white-label consumer that writes whitelabel.content_block (CR-462)")

    # BR-DASHBOARD-GET-HIDDEN (CR-450)
    gd = op("getDashboard")[3]
    miss = {"subscription#contractRecords", "subscription#licenceAddOnRecords", "subscription#planRecords"} - set(vias(gd))
    need("BR-DASHBOARD-GET-HIDDEN", not miss, f"getDashboard does not ask {', '.join(sorted(miss))} in process (CR-450)")
    need("BR-DASHBOARD-GET-HIDDEN", "`404 not-found`" in words(gd.get("description")) and "404" in (gd.get("responses") or {}),
         "getDashboard does not answer 404 not-found for a dashboard whose module fails the rule (CR-450)")


def access_rules_r12(need, op):
    """BR-GATE-MODE-POLICY, BR-ACCESS-POINT-ACTIVE, BR-WHITELIST-APPROVAL, BR-ADMISSION-CREATE (r12; ADAM CR-396, CR-397,
    CR-399, CR-400, decided 31 October 2026, after the lead's review of every CR). Each fails on the r11 contract."""
    def words(x):
        return " ".join(str(x or "").split())

    def vias(o_):
        return {(str((v or {}).get("query")), str((v or {}).get("route")))
                for v in o_.get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    acc = load("contracts/spine/access.yaml")
    sch = (acc.get("components") or {}).get("schemas") or {}

    # BR-GATE-MODE-POLICY (CR-396)
    tsm = op("setTurnstileMode")[3]
    need("BR-GATE-MODE-POLICY", ("identity#principalHoldsRoleAtVenue", "in-process") in vias(tsm),
         "setTurnstileMode does not ask identity#principalHoldsRoleAtVenue in process for whoCanActivate (CR-396)")
    need("BR-GATE-MODE-POLICY", "gate-mode-role-required" in ptypes(tsm, "403")
         and "reason-required" in ptypes(tsm, "400"),
         "setTurnstileMode does not answer 403 gate-mode-role-required and 400 reason-required (CR-396)")
    td = words(tsm.get("description"))
    for frag in ("beats the venue default", "must pass every one of them", "`emergencyAccessEvent` for `dropArm`",
                 "`securityEvent` for `freeFlow`", "`assignedTeam` `accessSupervisor`", "a cancelled one opens none"):
        need("BR-GATE-MODE-POLICY", frag in td, f"setTurnstileMode does not say {frag!r} (CR-396)")
    who = ((sch.get("AccessGateModePolicy") or {}).get("properties") or {}).get("whoCanActivate") or {}
    need("BR-GATE-MODE-POLICY", (who.get("items") or {}).get("format") == "uuid",
         "AccessGateModePolicy.whoCanActivate is not a list of identity.role ids (format uuid; CR-396)")
    need("BR-GATE-MODE-POLICY", "targetTurnstileMode" in ((sch.get("AccessGateModeChange") or {}).get("properties") or {}),
         "AccessGateModeChange has no targetTurnstileMode, so a scheduled turnstile mode has nowhere to wait (CR-396)")

    # BR-ACCESS-POINT-ACTIVE (CR-397)
    need("BR-ACCESS-POINT-ACTIVE", "created active" in words(op("createAccessPoint")[3].get("description")),
         "createAccessPoint does not say a new access point is created active (CR-397)")
    need("BR-ACCESS-POINT-ACTIVE", "device status AccessPoint" not in words(op("setAccessPointDirection")[3].get("description"))
         and "says so through its device status" not in words(op("setAccessPointDirection")[3].get("description")),
         "setAccessPointDirection promises a device status AccessPoint does not have (CR-397)")

    # BR-WHITELIST-APPROVAL (CR-399)
    abe = op("addBlacklistEntry")[3]
    need("BR-WHITELIST-APPROVAL", any((w or {}).get("operation") == "createApprovalRequest"
                                      for w in abe.get("x-ticvai-write-via") or [] if isinstance(w, dict)),
         "addBlacklistEntry raises its whitelist approval request with no x-ticvai-write-via createApprovalRequest (CR-399)")
    need("BR-WHITELIST-APPROVAL", "no-approval-route" in ptypes(abe, "422"),
         "addBlacklistEntry does not pass approvals' 422 no-approval-route on (CR-399)")
    ev = load("events/approval-granted.yaml")
    need("BR-WHITELIST-APPROVAL", any((c or {}).get("context") == "access" and "access.blacklist" in ((c or {}).get("writes") or [])
                                      for c in ev.get("consumers") or []),
         "events/approval-granted.yaml names no access consumer that writes the approved whitelist entry (CR-399)")

    # BR-ADMISSION-CREATE (CR-400)
    car, uar = op("createAdmissionRules")[3], op("updateAdmissionRules")[3]
    need("BR-ADMISSION-CREATE", ptypes(car, "422") >= {"entry-count-required", "validity-days-required",
                                                       "validity-ends-before-start"},
         "createAdmissionRules does not answer updateAdmissionRules' three 422 problem types (CR-400)")
    need("BR-ADMISSION-CREATE", "tenancy#scopeRecords" in {q for q, _ in vias(car)}
         and "working-venue-required" in ptypes(car, "403"),
         "createAdmissionRules does not read the working venue's path (tenancy#scopeRecords) or answer 403 "
         "working-venue-required (CR-400, CR-217)")
    need("BR-ADMISSION-CREATE", "tenancy#scopeRecords" not in {q for q, _ in vias(uar)},
         "updateAdmissionRules re-derives scope_path from the editor's working venue (CR-400)")


def pricing_rules_r13(need, op):
    """r13 lane n, pricing, fees and tax (ADAM CR-439, CR-446, CR-455, CR-456, CR-460, CR-464, CR-467, CR-468; the
    lead's "Approve all", 1 November 2026, and "approve all as a recommended", 2 November 2026). Each rule fails on the
    r12 contract and passes once the posted decision is in the package."""
    cat = load("contracts/spine/catalogue.yaml")
    sch = (cat.get("components") or {}).get("schemas") or {}
    fin = load("contracts/spine/finance.yaml")
    lo = {str(i.get("id")) for i in (load("docs/active/left-out.yaml").get("items") or []) if isinstance(i, dict)}

    def words(x):
        return " ".join(str(x or "").split())

    def d(oid):
        return words(op(oid)[3].get("description"))

    def sp(name):
        return (sch.get(name) or {}).get("properties") or {}

    def reads(oid):
        return {str(r.get("table")) for r in op(oid)[3].get("x-ticvai-reads") or [] if isinstance(r, dict)}

    def vias(oid):
        return {str(v.get("query")) for v in op(oid)[3].get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def codes(oid, code):
        return set(((op(oid)[3].get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def param(oid, name):
        for p_ in op(oid)[3].get("parameters") or []:
            if isinstance(p_, dict) and p_.get("name") == name:
                return p_.get("schema") or {}
        return None

    def is_status(node):
        node = node or {}
        refs = [node.get("$ref")] + [a.get("$ref") for a in node.get("allOf") or [] if isinstance(a, dict)]
        return "#/components/schemas/CatalogueConfigStatus" in refs

    # BR-VARIANT-PRICE (ADAM CR-439, CR-455; CHG-CR439-001, CHG-CR455-001)
    q = (cat.get("x-ticvai-queries") or {}).get("variantPriceRecords") or {}
    qr = words(q.get("rule"))
    need("BR-VARIANT-PRICE", {"variantId", "venueId", "channel", "at", "customerSegment"} <= set(q.get("inputs") or {})
         and "in-process" in (q.get("served") or []),
         "catalogue#variantPriceRecords is not declared with (variantId, venueId, channel, at, customerSegment), served "
         "in process (CR-439)")
    for frag in ("highestPriorityWins", "assignment priority (highest first", "price_category_id equal to the variant's",
                 "base_rate_id", "null amount"):
        need("BR-VARIANT-PRICE", frag in qr, f"variantPriceRecords' rule does not state {frag!r} (CR-439, CR-455)")
    need("BR-VARIANT-PRICE", (sp("ProductVariant").get("priceCategoryId") or {}).get("nullable") is True,
         "ProductVariant has no nullable priceCategoryId (CR-455)")
    body = ((((op("updateProductVariant")[3].get("requestBody") or {}).get("content") or {}).get("application/json") or {})
            .get("schema") or {}).get("properties") or {}
    need("BR-VARIANT-PRICE", "priceCategoryId" in body, "updateProductVariant does not write priceCategoryId (CR-455)")
    sc = ((((((op("searchCatalogue")[3].get("responses") or {}).get("200") or {}).get("content") or {})
            .get("application/json") or {}).get("schema") or {}).get("items") or {}).get("properties") or {}
    need("BR-VARIANT-PRICE", (sc.get("fromPrice") or {}).get("nullable") is True
         and "variantPriceRecords" in words((sc.get("fromPrice") or {}).get("description")),
         "searchCatalogue's fromPrice is not nullable or does not name variantPriceRecords (CR-439, CR-455)")
    lf = words(((cat.get("x-ticvai-queries") or {}).get("variantListingFacts") or {}).get("rule"))
    need("BR-VARIANT-PRICE", "variantPriceRecords" in lf,
         "variantListingFacts' listPrice does not use variantPriceRecords (CR-439)")
    sim = "simulatePriceBreakdownCalculation"
    need("BR-VARIANT-PRICE", {"no-selected-rate", "promotion-evaluation-unavailable", "unsupported-tax-method"}
         <= codes(sim, "422") and "no-price-for-variant" not in codes(sim, "422"),
         "simulatePriceBreakdownCalculation's 422 does not list no-selected-rate, promotion-evaluation-unavailable and "
         "unsupported-tax-method, or lists no-price-for-variant (CR-439, CR-455)")
    need("BR-VARIANT-PRICE", {"pricing.dynamic_price_rule", "pricing.dynamic_price_condition",
                              "pricing.dynamic_price_action", "catalogue.sales_channel", "catalogue.fee_rule",
                              "catalogue.tax_rule"} <= reads(sim),
         "simulatePriceBreakdownCalculation does not declare the member, fee and tax reads (CR-455)")
    ds = d(sim)
    for frag in ("`membershipProgramme`", "The lowest priority number wins", "lower number first",
                 "`channel_deployments`", "one Catalogue calculation component",
                 "rule wins over `ledger.tax_code.is_inclusive`"):
        need("BR-VARIANT-PRICE", frag in ds, f"simulatePriceBreakdownCalculation does not state {frag!r} (CR-439, CR-455)")
    need("BR-VARIANT-PRICE", "LO-CR455-001" in lo,
         "fixedTax and tiered are not on the left-out list as LO-CR455-001 (CR-455)")

    # BR-ELASTICITY-LABELS (ADAM CR-446; CHG-CR446-001)
    need("BR-ELASTICITY-LABELS", "'up to {to} days'" in d("listPriceElasticityRevenue")
         and "'{from}+ days'" in d("listPriceElasticityRevenue"),
         "listPriceElasticityRevenue does not write a one-bound proximity as 'up to {to} days' / '{from}+ days' (CR-446)")
    need("BR-ELASTICITY-LABELS", "rounded to one decimal like `positionVsMedian`" in d("listCompetitorPricingMarket"),
         "listCompetitorPricingMarket does not round movementPercent to one decimal (CR-446)")

    # BR-CHANGE-IMPACT (ADAM CR-456; CHG-CR456-001)
    ci = "listPricingChangeImpact"
    need("BR-CHANGE-IMPACT", {"orders#orderLineRecords", "tenancy#venueSettingsRecords"} <= vias(ci)
         and {"catalogue.rate", "catalogue.price", "catalogue.price_assignment", "catalogue.performance",
              "catalogue.group_package", "catalogue.dynamic_pricing_control"} <= reads(ci),
         "listPricingChangeImpact does not declare the reads CR-456 names")
    vp = sp("PricingChangeImpactAnalysisView")
    for f_ in ("b2bPartners", "apis", "integrations", "promotions", "marginImpact", "averagePriceChange",
               "maximumChange", "minimumChange", "riskLevel"):
        need("BR-CHANGE-IMPACT", (vp.get(f_) or {}).get("nullable") is True,
             f"PricingChangeImpactAnalysisView.{f_} is not nullable (CR-456)")
    need("BR-CHANGE-IMPACT", "LO-CR456-001" in lo and "computed when the row is read" in d(ci)
         and "365 days before the read" in d(ci),
         "listPricingChangeImpact does not compute at read with the 365-day window, or LO-CR456-001 is missing (CR-456)")
    need("BR-CHANGE-IMPACT", not any("change_impact_analysis" in str((s_ or {}).get("x-ticvai-persistence") or "")
                                     for s_ in sch.values() if isinstance(s_, dict)),
         "a schema persists an impact analysis, which CR-456 ruled out (computed at read time)")

    # BR-PRODUCT-WORKFLOW (ADAM CR-460; CHG-CR460-001)
    lpw = d("listProductApprovalWorkflows")
    need("BR-PRODUCT-WORKFLOW", "catalogue.approval_policy" in reads("listProductApprovalWorkflows")
         and "subject product" in lpw and "ordered by `name` then `id`" in lpw,
         "listProductApprovalWorkflows does not read catalogue.approval_policy rows with subject product (CR-460)")
    need("BR-PRODUCT-WORKFLOW", "keep their stored values" in d("approveWorkflow")
         and "`workflowId` is `id`" in d("approveWorkflow"),
         "approveWorkflow does not state the mapping and what a replace keeps (CR-460)")

    # BR-FEE-INSTANTS (ADAM CR-464; CHG-CR464-001)
    for v in ("FeeSurchargeLibraryView", "FeeApplicabilityChargingRuleBuilderView",
              "FeeApplicabilityChargingRuleBuilderInput", "FeeWaiverTaxExemptionExceptionRulesView",
              "PriceCalculationSequenceFormulaEngineView"):
        pr = sp(v)
        for f_ in ("effectiveFrom", "effectiveTo"):
            need("BR-FEE-INSTANTS", (pr.get(f_) or {}).get("format") == "date-time"
                 and (pr.get(f_) or {}).get("nullable") is True, f"{v}.{f_} is not a nullable date-time (CR-464)")
        if "status" in pr:
            need("BR-FEE-INSTANTS", is_status(pr.get("status")),
                 f"{v}.status does not take CatalogueConfigStatus (CR-464)")
    for oid in ("listFeeSurcharge", "listFeeWaiverTax"):
        need("BR-FEE-INSTANTS", is_status(param(oid, "status")),
             f"{oid}'s status filter does not take CatalogueConfigStatus (CR-464)")
    need("BR-FEE-INSTANTS", (param("listPriceCalculationSequence", "asOf") or {}).get("format") == "date-time",
         "listPriceCalculationSequence's asOf is not an instant (CR-464)")

    # BR-SEAT-RULE-OVERLAP (ADAM CR-467; CHG-CR467-001)
    need("BR-SEAT-RULE-OVERLAP", {"invalid-range", "overlapping-rule-same-priority"} <= codes("setSeatPricingRule", "422"),
         "setSeatPricingRule's 422 does not name invalid-range and overlapping-rule-same-priority (CR-467)")
    need("BR-SEAT-RULE-OVERLAP", "they are not apart" in d("setSeatPricingRule")
         and "A selector only one of them sets never makes them apart" in d("setSeatPricingRule")
         and "Covered seats" in words((sch.get("SeatPricingRule") or {}).get("description")),
         "setSeatPricingRule or SeatPricingRule does not define covered seats and the overlap (CR-467)")

    # BR-TAX-PROFILE-LIST (ADAM CR-468; CHG-CR468-001)
    for oid in ("listTaxProfiles", "getTaxProfileJurisdiction"):
        need("BR-TAX-PROFILE-LIST", {"catalogue.tax_rule", "catalogue.product"} <= reads(oid)
             and {"finance#taxCodeRecords", "finance#legalEntityRecords", "tenancy#venueSettingsRecords"} <= vias(oid),
             f"{oid} does not declare the reads CR-468 names")
    need("BR-TAX-PROFILE-LIST", "at or above" not in d("listTaxProfiles") and "at or beneath" in d("listTaxProfiles")
         and is_status(param("listTaxProfiles", "status"))
         and is_status(sp("TaxProfileJurisdictionConfigurationView").get("status")),
         "listTaxProfiles still says at or above, or its status is not CatalogueConfigStatus (CR-468)")
    need("BR-TAX-PROFILE-LIST", "in-process" in (((fin.get("x-ticvai-queries") or {}).get("legalEntityRecords") or {})
                                                 .get("served") or []),
         "finance#legalEntityRecords is not served in process, so Catalogue cannot ask it within commerce (CR-468)")


LANE_Q_R13_RULES = ["BR-CATALOGUE-ANCESTORS", "BR-GUIDED-CHOICE-UPDATE", "BR-FACE-TAG-CONSENT-FALLBACK", "BR-TICKET-LAYOUT",
                    "BR-DEVICE-HOST", "BR-DEVICE-KEY", "BR-SIGNAGE-BOARD", "BR-TEMPERATURE-CHECKPOINT",
                    "BR-SIGNAGE-CALLS-LEFT", "BR-WALLET-TOPUP-GUEST", "BR-DELEGATION-AUTHORITY", "BR-EXCHANGE-QUOTE",
                    "BR-MATRIX-REFUSAL-TYPES", "BR-END-SESSIONS-ROOT", "BR-ORDER-SETTLEMENT"]


def lane_q_rules_r13(need, op):
    """r13 CR lane q (ADAM CR-443 to CR-483, decided 1 and 2 November 2026; CHG-CR443-001 to CHG-CR483-001,
    CHG-R13ORD-001). Each rule fails on the r12 package (e3e4082c) and passes once the posted decision is in."""
    def words(x):
        return " ".join(str(x or "").split())

    def vias(o_):
        return {(str((v or {}).get("query")), str((v or {}).get("route")))
                for v in o_.get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def tables(o_, key):
        return {str((t or {}).get("table")) for t in o_.get(key) or [] if isinstance(t, dict)}

    def query(contract, name):
        return ((load(contract).get("x-ticvai-queries") or {}).get(name)) or {}

    def schemas(contract):
        return (load(contract).get("components") or {}).get("schemas") or {}

    xdr = {str((r or {}).get("id")): r for r in load("docs/active/cross-deployable-writes.yaml").get("reads") or []
           if isinstance(r, dict)}

    # BR-CATALOGUE-ANCESTORS (ADAM CR-443): the guided choice and kiosk checks read rows at the venue and its ancestors
    # getKioskConfigValidation left this loop with ADAM CR-528 (3 November 2026): its checks read the venue's and the
    # tenant's rows by venueIds and venue_id, no scope path (lane w3's BR-KIOSK-CHECK-ROWS)
    need("BR-CATALOGUE-ANCESTORS", "for this check only" in words(op("getKioskConfigValidation")[3].get("description")),
         "getKioskConfigValidation does not read its rows for this check only (CR-443, CR-528)")
    for oid in ("createGuidedChoice", "proposeGuidedChoice", "updateGuidedChoice", "publishGuidedChoice"):
        need("BR-CATALOGUE-ANCESTORS", "at its ancestors" in words(op(oid)[3].get("description"))
             and "for this check only" in words(op(oid)[3].get("description")),
             f"{oid} does not say its check reads the rows at the venue and at its ancestors, for this check only (CR-443)")
    need("BR-CATALOGUE-ANCESTORS", "root grant" in words(op("getKioskConfigValidation")[3].get("description")),
         "getKioskConfigValidation does not read module enablement under the routed tenant's root grant (CR-443)")
    for contract, name in (("contracts/spine/catalogue.yaml", "productCategoryRecords"),
                           ("contracts/satellite/payments.yaml", "paymentMethodRecords"),
                           ("contracts/satellite/assets.yaml", "mediaAssetRecords")):
        need("BR-CATALOGUE-ANCESTORS", "CR-443" in words(query(contract, name).get("rule"))
             and "ITenantRootGrant" in words(query(contract, name).get("rule")),
             f"{name}'s rule does not state the read above the venue for White Label's checks under the routed tenant's "
             "root grant (CR-443; the lead, 2 November 2026)")

    # BR-GUIDED-CHOICE-UPDATE (ADAM CR-444)
    ugc = op("updateGuidedChoice")[3]
    need("BR-GUIDED-CHOICE-UPDATE", "target-not-in-venue" in ptypes(ugc, "400"),
         "updateGuidedChoice's 400 does not answer target-not-in-venue (CR-444)")
    for q in ("catalogue#productRecords", "catalogue#productCategoryRecords", "catalogue#eventRecords"):
        need("BR-GUIDED-CHOICE-UPDATE", (q, "in-process") in vias(ugc),
             f"updateGuidedChoice does not ask {q} in process (CR-444)")
    need("BR-GUIDED-CHOICE-UPDATE", "updateGuidedChoice" in ((xdr.get("XDR-033") or {}).get("operations") or []),
         "XDR-033 does not grant updateGuidedChoice's Catalogue reads (CR-444)")

    # BR-FACE-TAG-CONSENT-FALLBACK (ADAM CR-445)
    sft = words(op("setFaceTagTemporaryEnrollment")[3].get("description"))
    need("BR-FACE-TAG-CONSENT-FALLBACK", "else the tenant default" in sft and "root grant" in sft,
         "setFaceTagTemporaryEnrollment does not fall back to the tenant default under the root grant (CR-445)")
    view = (schemas("contracts/spine/access.yaml").get("FaceTagTemporaryEnrollmentView") or {}).get("properties") or {}
    need("BR-FACE-TAG-CONSENT-FALLBACK", "never the form in effect" in words((view.get("consentFormId") or {}).get("description")),
         "FaceTagTemporaryEnrollmentView.consentFormId does not say it is the stored value (CR-445)")

    # BR-TICKET-LAYOUT (ADAM CR-447, CR-463): the layout model the BOCA driver and the proof share
    osch = schemas("contracts/spine/orders.yaml")
    tl, tle = osch.get("TicketLayout") or {}, osch.get("TicketLayoutElement") or {}
    stock = ((tl.get("properties") or {}).get("stock") or {}).get("properties") or {}
    need("BR-TICKET-LAYOUT", {"widthMm", "heightMm", "dpi"} <= set(stock),
         "orders TicketLayout.stock has no widthMm, heightMm and dpi (CR-447, CR-463)")
    eprops = tle.get("properties") or {}
    need("BR-TICKET-LAYOUT", {"kind", "xMm", "yMm", "rotation", "font", "fontSize", "moduleSizeMm", "content"} <= set(eprops)
         and {"field", "text", "assetRef"} <= set(((eprops.get("content") or {}).get("properties") or {})),
         "orders TicketLayoutElement lacks the names the device host built (CR-463)")
    need("BR-TICKET-LAYOUT", "TicketLayout" in words(((osch.get("TicketTemplateRequest") or {}).get("properties") or {})
                                                     .get("layoutRef", {}).get("description")),
         "TicketTemplateRequest.layoutRef does not name a stored TicketLayout (CR-447)")
    need("BR-TICKET-LAYOUT", "TicketLayout" in words(op("printTicketProof")[3].get("description"))
         and ("access#mediaTemplateRecords", "in-process") in vias(op("printTicketProof")[3])
         and "printTicketProof" in ((xdr.get("XDR-067") or {}).get("operations") or []),
         "printTicketProof does not render the stored TicketLayout read from Access in process (access#mediaTemplateRecords, "
         "XDR-067; CR-447)")
    need("BR-TICKET-LAYOUT", "layout" in ((schemas("contracts/spine/access.yaml").get("PdfPrintablePosTicketDesignerInput")
                                           or {}).get("properties") or {}),
         "the ticket designer's input (BO-346) has no layout to save (CR-447)")
    tp = load("contracts/devices/ticket-printer.yaml") if (ROOT / "contracts/devices/ticket-printer.yaml").exists() else {}
    paths = tp.get("paths") or {}
    need("BR-TICKET-LAYOUT", "/ticket-printer/status" in paths and "/ticket-printer/print-jobs" in paths,
         "contracts/devices/ticket-printer.yaml does not carry the device host's two paths (CR-463)")
    pj = (paths.get("/ticket-printer/print-jobs") or {}).get("post") or {}
    need("BR-TICKET-LAYOUT", any((p or {}).get("name") == "Idempotency-Key" and (p or {}).get("required")
                                 for p in pj.get("parameters") or []),
         "the device host's print job does not require an Idempotency-Key (CR-463)")
    need("BR-TICKET-LAYOUT", {"502", "503", "504", "409", "400", "403"} <= {str(k) for k in (pj.get("responses") or {})},
         "the device host's print job does not answer 400, 403, 409, 502, 503 and 504 (CR-463)")
    td = words((tp.get("info") or {}).get("description"))
    need("BR-TICKET-LAYOUT", "127.0.0.1 only" in td and "refuses any other origin with 403" in td
         and "never prints again" in td and "keeps no secret" in td,
         "contracts/devices/ticket-printer.yaml does not state loopback, the origin allowlist, the idempotent retry "
         "and no secret (CR-463 (2))")

    # BR-DEVICE-HOST (ADAM CR-448)
    adr = (ROOT / "docs/adr/0015-standards-first-device-drivers.md").read_text(encoding="utf-8")
    need("BR-DEVICE-HOST", "CR-448" in adr and "device host" in adr,
         "ADR-0015 does not record where the BOCA driver runs (the Windows device host, CR-448)")

    # BR-DEVICE-KEY (ADAM CR-451)
    dc = (schemas("contracts/spine/tenancy.yaml").get("DeviceCredential") or {}).get("properties") or {}
    need("BR-DEVICE-KEY", "apiKey" in ((dc.get("kind") or {}).get("enum") or []) and "key" in dc,
         "tenancy DeviceCredential has no kind apiKey, or no key shown once at issue (CR-451)")
    for oid in ("getSignageQueueBoard", "getSignageQueueCalls"):
        rs = {str(k) for k in (op(oid)[3].get("responses") or {})}
        need("BR-DEVICE-KEY", {"401", "403"} <= rs and "CR-451" in words(op(oid)[3].get("description")),
             f"{oid} does not sign the display in by its key, with 401 and 403 (CR-451)")
    need("BR-DEVICE-KEY", "CR-451" in words(op("submitQueueReading")[3].get("description")),
         "submitQueueReading does not use the device-key sign-in (CR-451)")
    for oid in ("getSignageQueueBoard", "getSignageQueueCalls", "submitQueueReading"):
        need("BR-DEVICE-KEY", ("tenancy#deviceForApiKey", "in-process") in vias(op(oid)[3])
             and oid in ((xdr.get("XDR-068") or {}).get("operations") or []),
             f"{oid}'s device-key sign-in does not ask tenancy#deviceForApiKey in process under XDR-068 (CR-451)")
    need("BR-DEVICE-KEY", "ITenantRootGrant" in words(query("contracts/spine/tenancy.yaml", "deviceForApiKey").get("rule")),
         "tenancy#deviceForApiKey is not one statement under the routed tenant's root grant (CR-451)")

    # BR-SIGNAGE-BOARD (ADAM CR-452)
    gsb = op("getSignageQueueBoard")[3]
    gd = words(gsb.get("description"))
    need("BR-SIGNAGE-BOARD", "queue.feed" in tables(gsb, "x-ticvai-reads"),
         "getSignageQueueBoard does not read queue.feed for isStale (CR-452)")
    for frag in ("`green` up to 15 minutes, `amber` from 16 to 45, `red` above 45", "English as the fallback",
                 "'Min {n} cm'", "older than twice its feed's", "`refreshSeconds` is 30", "ordered by name"):
        need("BR-SIGNAGE-BOARD", frag in gd, f"getSignageQueueBoard does not say {frag!r} (CR-452)")

    # BR-TEMPERATURE-CHECKPOINT (ADAM CR-453)
    stc = op("setTemperatureCheckpoint")[3]
    need("BR-TEMPERATURE-CHECKPOINT", ("tenancy#outletRecords", "in-process") in vias(stc) and "400" in (stc.get("responses") or {})
         and "setTemperatureCheckpoint" in ((xdr.get("XDR-004") or {}).get("operations") or []),
         "setTemperatureCheckpoint does not check outletId against the venue's outlets in process with a 400 (CR-453)")
    need("BR-TEMPERATURE-CHECKPOINT", "`minCelsius` greater than `maxCelsius` is `400`" in words(stc.get("description"))
         and "0 or less is `400`" in words(stc.get("description")),
         "setTemperatureCheckpoint does not refuse min above max, or a frequency of 0 or less (CR-453)")

    # BR-SIGNAGE-CALLS-LEFT (ADAM CR-453)
    calls = (((((op("getSignageQueueCalls")[3].get("responses") or {}).get("200") or {}).get("content") or {})
              .get("application/json") or {}).get("schema") or {}).get("properties") or {}
    need("BR-SIGNAGE-CALLS-LEFT", "leftCalled" in calls,
         "getSignageQueueCalls does not list the parties that left the called state since the cursor (CR-453)")

    # BR-WALLET-TOPUP-GUEST (ADAM CR-471)
    tuw = op("topUpWallet")[3]
    need("BR-WALLET-TOPUP-GUEST", tuw.get("x-ticvai-self-scoped") == "subject" and "404" in (tuw.get("responses") or {}),
         "topUpWallet does not hold a guest to its own wallet (self-scoped subject, the shared 404) (CR-471)")
    need("BR-WALLET-TOPUP-GUEST", {"wallet.balance", "wallet.credit_lot", "wallet.wallet_transaction", "wallet.wallet",
                                   "platform.outbox"} <= tables(tuw, "x-ticvai-writes"),
         "topUpWallet's x-ticvai-writes does not list its five tables (CR-471)")
    twd = words(tuw.get("description"))
    need("BR-WALLET-TOPUP-GUEST", "ITenantRootGrant" in twd and "Nothing else runs under the root grant" in twd
         and "`orders.order_line.venue_id`" in twd,
         "topUpWallet does not confine a guest's writes to the root grant, or state the lot's scope (CR-471)")

    # BR-DELEGATION-AUTHORITY (ADAM CR-479)
    for oid in ("createApprovalDelegation", "approveRoleAuthorityDelegation"):
        v = vias(op(oid)[3])
        need("BR-DELEGATION-AUTHORITY", ("identity#principalHoldsRoleAtVenue", "in-process") in v
             and ("identity#principalHoldsPermissionAtVenue", "in-process") in v,
             f"{oid} does not ask the two yes/no rule questions in process (CR-479)")
    php = query("contracts/spine/identity.yaml", "principalHoldsPermissionAtVenue")
    need("BR-DELEGATION-AUTHORITY", "ITenantRootGrant" in words(php.get("rule")) and php.get("served") == ["in-process"],
         "identity#principalHoldsPermissionAtVenue is not a yes/no under ITenantRootGrant, served in process (CR-479)")
    cad = words(op("createApprovalDelegation")[3].get("description"))
    need("BR-DELEGATION-AUTHORITY", "makes the limit unlimited" in cad and "is not compared with the matrix" in cad
         and "The `400`s (`invalidWindow`, `delegateIsDelegator`) are checked first" in cad,
         "createApprovalDelegation does not state the limit rule, maxPercentage and the order of refusals (CR-479)")
    need("BR-DELEGATION-AUTHORITY", "which never exceeds what the delegator may approve under the matrix, its own"
         not in words(op("approveRoleAuthorityDelegation")[3].get("description")),
         "approveRoleAuthorityDelegation still compares maxPercentage with the matrix (CR-479)")

    # BR-EXCHANGE-QUOTE (ADAM CR-480)
    eol = op("exchangeOrderLines")[3]
    need("BR-EXCHANGE-QUOTE", ptypes(eol, "409") == {"line-redeemed", "outside-exchange-window", "replacement-unavailable"},
         "exchangeOrderLines' 409 does not name one problem type per reason (CR-480)")
    # access#entitlementRecords in process, as modifyOrder asks it (CR-480's own reason; CHG-R13INT-013)
    for q, r in (("access#entitlementRecords", "in-process"), ("catalogue#performanceRecords", "in-process"),
                 ("catalogue#inventoryReservationRecords", "in-process"), ("catalogue#variantPriceRecords", "in-process")):
        need("BR-EXCHANGE-QUOTE", (q, r) in vias(eol), f"exchangeOrderLines does not ask {q} ({r}) (CR-480)")
    ed = words(eol.get("description"))
    need("BR-EXCHANGE-QUOTE", "`exchangeFee` is zero until the client sets a fee rule" in ed and "writes nothing" in ed,
         "exchangeOrderLines does not state the quote, the zero fee and the write-nothing interim (CR-480)")
    ev = load("events/order-exchanged.yaml")
    need("BR-EXCHANGE-QUOTE", {"catalogue", "seating", "access"} <= {(c or {}).get("context") for c in ev.get("consumers") or []},
         "events/order-exchanged.yaml names no catalogue, seating and access consumers (CR-480)")

    # BR-MATRIX-REFUSAL-TYPES (ADAM CR-481)
    sam = op("setApprovalMatrix")[3]
    need("BR-MATRIX-REFUSAL-TYPES", {"loosens-parent-rule", "unreachable-rule", "matrix-id-mismatch"} <= ptypes(sam, "409"),
         "setApprovalMatrix's 409 does not declare loosens-parent-rule and unreachable-rule (CR-481)")
    for oid in ("setApprovalMatrix", "approveMatrixMultiLevel"):
        sch = (((((op(oid)[3].get("responses") or {}).get("422") or {}).get("content") or {})
                .get("application/problem+json") or {}).get("schema") or {}).get("$ref")
        need("BR-MATRIX-REFUSAL-TYPES", str(sch).endswith("ApprovalConditionInvalidProblem"),
             f"{oid}'s 422 condition-invalid is not ApprovalConditionInvalidProblem (ruleOrder, clause; CR-481)")

    # BR-END-SESSIONS-ROOT (ADAM CR-483)
    ddl = (ROOT / "tools/derive-ddl.py").read_text(encoding="utf-8")
    need("BR-END-SESSIONS-ROOT", "FROM platform.scope s WHERE s.level = 'tenant' LIMIT 1" not in ddl
         and "subpath(hs.path, 0, 1)" in ddl and "no tenant root for principal" in ddl and "'P0001'" in ddl,
         "identity.end_principal_sessions still takes the root from platform.scope's tenant row, or does not raise "
         "when it finds none (CR-483)")

    # BR-ORDER-SETTLEMENT (the lead, 2 November 2026, "Yes to both": CR-480's rule for modifyOrder and rescheduleOrder)
    for oid in ("modifyOrder", "rescheduleOrder"):
        o_ = op(oid)[3]
        d = words(o_.get("description"))
        need("BR-ORDER-SETTLEMENT", "line-redeemed" in ptypes(o_, "409") and "never written by Orders" in d
             and "writes nothing" in d and ("catalogue#variantPriceRecords", "in-process") in vias(o_),
             f"{oid} does not settle as an exchange does: refusals first, quote first, entitlements through the "
             "order event's consumers (CHG-R13ORD-001)")
    need("BR-ORDER-SETTLEMENT", "modifyOrder" in str(ev.get("emittedWhen")) and "rescheduleOrder" in str(ev.get("emittedWhen")),
         "events/order-exchanged.yaml is not emitted by modifyOrder and rescheduleOrder (CHG-R13ORD-001)")

R13_O_RULES = ["BR-AUDIT-READ-NULLABLE", "BR-REFUND-POLICY-SCOPE", "BR-CHANNEL-RETRY", "BR-CHANNEL-TESTS",
               "BR-VAULT-REFERENCE", "BR-CHANNEL-RULE-CONFLICT", "BR-R12-DB-STATEMENTS", "BR-MEMBERSHIP-PLAN-PAGE",
               "BR-WEB035-PRICE-CARDS"]


def channel_rules_r13(need, op):
    """r13 lane o (ADAM CR-436 to CR-482, decided by Chinmay on 1 and 2 November 2026). Each fails on the r12 package but
    BR-WEB035-PRICE-CARDS, which holds CR-473's condition (the CR-358 cards stay)."""
    def words(x):
        return " ".join(str(x or "").split())

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def schemas(rel):
        return (load(rel).get("components") or {}).get("schemas") or {}

    cat = schemas("contracts/spine/catalogue.yaml")

    # BR-AUDIT-READ-NULLABLE (CR-436)
    ar = schemas("contracts/spine/tenancy.yaml").get("AuditRead") or {}
    need("BR-AUDIT-READ-NULLABLE", not ({"readAt", "target"} & set(ar.get("required") or [])),
         "AuditRead requires readAt or target, so the table record says NOT NULL where the SQL adds them nullable (CR-436)")

    # BR-REFUND-POLICY-SCOPE (CR-454)
    rcp = schemas("contracts/spine/orders.yaml").get("RefundCalculationPolicyView") or {}
    rsd = words(((rcp.get("properties") or {}).get("scopePath") or {}).get("description"))
    need("BR-REFUND-POLICY-SCOPE", "scopePath" in (rcp.get("required") or [])
         and "WHERE level = 'tenant'" in rsd and "SET NOT NULL" in rsd,
         "RefundCalculationPolicyView.scopePath does not stay required and state the backfill from the tenant root, then "
         "SET NOT NULL (CR-454)")

    # BR-CHANNEL-RETRY (CR-457)
    rci = op("retryChannelIncident")[3]
    need("BR-CHANNEL-RETRY", "catalogue.channelIncidentRetryRequested" in (rci.get("x-ticvai-emits") or []),
         "retryChannelIncident does not emit catalogue.channelIncidentRetryRequested (CR-457)")
    rcd = words(rci.get("description"))
    for frag in ("id as text", "action `retry`", "never marked `resolved` without"):
        need("BR-CHANNEL-RETRY", frag in rcd, f"retryChannelIncident does not say {frag!r} (CR-457)")
    ev = load("events/catalogue-channelIncidentRetryRequested.yaml")
    cons = [c for c in ev.get("consumers") or [] if (c or {}).get("context") == "catalogue"]
    need("BR-CHANNEL-RETRY", ev.get("emittedBy") == ["retryChannelIncident"] and cons
         and cons[0].get("idempotencyKey") == "incidentId+retryCount"
         and "connectorNotAvailable" in words(cons[0].get("purpose")) and "retryNotDelivered" in words(cons[0].get("purpose"))
         and {"catalogue.channel_incident", "catalogue.audit_entry"} <= set(cons[0].get("writes") or []),
         "events/catalogue-channelIncidentRetryRequested.yaml does not name the channel retry job as CR-457 decided")
    need("BR-CHANNEL-RETRY", {p.get("field") for p in ev.get("payload") or []} >= {
        "incidentId", "salesChannelId", "channelConnectionId", "errorType", "apiRequestReference", "correlationId",
        "retryCount", "requestedByPrincipalId"},
         "catalogue.channelIncidentRetryRequested does not carry CR-457's payload")

    # BR-CHANNEL-TESTS (CR-458)
    lt = ((cat.get("ChannelConnection") or {}).get("properties") or {}).get("lastTests") or {}
    need("BR-CHANNEL-TESTS", lt.get("type") == "array"
         and set(((lt.get("items") or {}).get("properties") or {})) == {"test", "result", "testedAt", "detail"}
         and (((lt.get("items") or {}).get("properties") or {}).get("result") or {}).get("enum") == ["passed", "failed", "notSupported"],
         "ChannelConnection.lastTests is not an array of {test, result, testedAt, detail} with passed, failed, notSupported (CR-458)")
    tcd = words(op("testChannelConnection")[3].get("description"))
    for frag in ("`ticvaiNative` has none", "`authentication` only", "endpoint address not allowed", "no redirects",
                 "10000 ms", "Credential found", "No connector for <connectionType> yet", "`notSupported` counts as neither",
                 "action `test`"):
        need("BR-CHANNEL-TESTS", frag in tcd, f"testChannelConnection does not say {frag!r} (CR-458)")
    lcd = words(op("listChannelConnectionIntegration")[3].get("description"))
    need("BR-CHANNEL-TESTS", "`productSync` answered as `product`" in lcd and "`webhook` entry is left out" in lcd
         and "stored `offline`" in lcd,
         "listChannelConnectionIntegration does not map the stored test names and status to the view's (CR-458)")

    # BR-VAULT-REFERENCE (CR-459)
    rx = "^t-<tenantId>-[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$"
    scc = op("setChannelConnectionConfiguration")[3]
    cr = words(((cat.get("ChannelConnection") or {}).get("properties") or {}).get("credentialsReference", {}).get("description"))
    need("BR-VAULT-REFERENCE", rx in words(scc.get("description")) and rx in cr and "shared validator in the kernel" in cr,
         "the vault-reference format is not stated once for the kernel's shared validator and on "
         "setChannelConnectionConfiguration (CR-459)")
    need("BR-VAULT-REFERENCE", "secret-not-reference" in ptypes(scc, "422") and "never echoed" in words(scc.get("description")),
         "setChannelConnectionConfiguration does not answer 422 secret-not-reference without echoing the value (CR-459)")

    # BR-CHANNEL-RULE-CONFLICT (CR-466)
    csr = op("setChannelSalesRule")[3]
    cd = words(csr.get("description"))
    for frag in ("`ruleLevel` plays no part", "not open to the past (CR-414)", "`isActive` false never conflicts",
                 "pg_advisory_xact_lock", "names the id of the rule it collides with"):
        need("BR-CHANNEL-RULE-CONFLICT", frag in cd, f"setChannelSalesRule does not say {frag!r} (CR-466)")
    need("BR-CHANNEL-RULE-CONFLICT", "rule-conflict" in ptypes(csr, "409"),
         "setChannelSalesRule does not answer 409 rule-conflict (CR-466)")

    # BR-R12-DB-STATEMENTS (CR-461, CR-470)
    seat = schemas("contracts/satellite/seating.yaml")
    smd = words(((seat.get("Section") or {}).get("properties") or {}).get("seatMapId", {}).get("description"))
    order = ["if the table holds any row, stop", "then `SET NOT NULL`", "`section_seat_map_id_fkey`",
             "`section_seat_map_id_idx`", "`section_seat_map_id_code_uniq`"]
    at, pos = [], 0
    for f in order:   # each step after the one before it
        pos = smd.find(f, max(pos, 0))
        at.append(pos)
    need("BR-R12-DB-STATEMENTS", all(i >= 0 for i in at),
         "Section.seatMapId does not give CR-470's guarded migration in its order (guard, NOT NULL, key, index, unique)")
    tpl = seat.get("SeatMapTemplate") or {}
    std = words(((tpl.get("properties") or {}).get("structure") or {}).get("description"))
    need("BR-R12-DB-STATEMENTS", {"structure", "scopePath"} <= set(tpl.get("required") or [])
         and "NOT NULL" in std and "from `region_id` first" in std,
         "SeatMapTemplate does not keep structure and scope_path NOT NULL with CR-461's migration rule")
    dpd = words(op("setDynamicPriceRule")[3].get("description"))
    need("BR-R12-DB-STATEMENTS", "`400 validation` on `salesChannel`" in dpd and "a reader takes a null as true" in dpd,
         "setDynamicPriceRule does not say what pricing.dynamic_price_rule leaves to it (CR-470)")
    ca = (cat.get("ChannelAllocation") or {}).get("properties") or {}
    need("BR-R12-DB-STATEMENTS", all("a reader takes a null count as 0" in words((ca.get(k) or {}).get("description"))
                                     for k in ("releasedUnits", "returnedUnits")),
         "ChannelAllocation's released and returned counts do not say a reader takes a null as 0 (CR-461)")

    # BR-MEMBERSHIP-PLAN-PAGE (CR-482)
    pp = (cat.get("Product") or {}).get("properties") or {}
    need("BR-MEMBERSHIP-PLAN-PAGE", (pp.get("isFeatured") or {}).get("type") == "boolean"
         and (pp.get("isFeatured") or {}).get("default") is False
         and (pp.get("compareAtPrice") or {}).get("x-ticvai-column") == "compare_at_amount"
         and (pp.get("compareAtPrice") or {}).get("nullable") is True,
         "Product has no isFeatured (boolean, default false) or compareAtPrice (Money, nullable, compare_at_amount) (CR-482)")
    for req in ("CreateProductRequest", "UpdateProductRequest"):
        need("BR-MEMBERSHIP-PLAN-PAGE", {"isFeatured", "compareAtPrice"} <= set(((cat.get(req) or {}).get("properties") or {})),
             f"{req} does not take isFeatured and compareAtPrice (CR-482)")
    p01 = load("screens/P01-guest-web-storefront.yaml").get("screens") or []
    scr = next((x for x in p01 if (x or {}).get("id") == "WEB-022"), {})
    apis = {a.get("operationId") for a in scr.get("apis") or []}
    need("BR-MEMBERSHIP-PLAN-PAGE", {"getPlanBenefits", "listMembershipBenefits", "listProductVariants", "createCart",
                                     "addCartLine", "updateCartLine", "removeCartLine", "getCart",
                                     "getPublishedBookingFlow"} <= apis
         and "WEB-011" in ((scr.get("navigation") or {}).get("exitTo") or []),
         "WEB-022 does not sell through the cart and go on into the membership booking flow (CR-482)")

    # BR-WEB035-PRICE-CARDS (CR-473)
    w35 = next((x for x in p01 if (x or {}).get("id") == "WEB-035"), {})
    cards = [c for r in ((w35.get("layout") or {}).get("regions") or []) for c in (r or {}).get("components") or []
             if (c or {}).get("label") == "Prices in your currency"]
    need("BR-WEB035-PRICE-CARDS", bool(cards) and cards[0].get("operation") == "listProducts"
         and "Product.fromPrice" in (cards[0].get("columns") or []),
         "WEB-035 no longer has CR-358's Prices in your currency cards on listProducts (CR-473's condition)")
def roots_r13_v(need, op):
    """r13 root-cause lane v (2 November 2026; the lead: "lets see if we can do something in parallel", "yes"): the
    developer review's roots R20, R21, R24, R27, R28, R39, R40 and R41, each fixed at its source for the operations the
    review named. Every rule fails on the r12 contract (e3e4082c) and passes on the fix (CHG-R13R20-001 ...)."""
    def words(x):
        return " ".join(str(x or "").split())

    def sch(rel, name):
        return ((load(rel).get("components") or {}).get("schemas") or {}).get(name) or {}

    def tables(o, key):
        return {str(x.get("table") if isinstance(x, dict) else x) for x in o.get(key) or []}

    def vias(o):
        return {str((v or {}).get("query")) for v in o.get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def body(o):
        return ((((o.get("requestBody") or {}).get("content") or {}).get("application/json") or {}).get("schema") or {})

    # BR-R13-UPSERT-KEY (R20): a "keyed by" upsert has a unique index behind its key.
    for rel, name, table, cols in (
            ("contracts/satellite/fnb.yaml", "KitchenRoutingRules", "fnb.kitchen_routing_rule", ["outletId"]),
            ("contracts/satellite/fnb.yaml", "CourseRules", "fnb.course_rule", ["outletId"]),
            ("contracts/spine/catalogue.yaml", "DynamicPricingStrategy", "catalogue.dynamic_pricing_strategy",
             ["scopePath", "code"]),
            ("contracts/spine/catalogue.yaml", "ChannelConnection", "catalogue.channel_connection",
             ["salesChannelId", "connectorName", "environment"]),
            ("contracts/spine/catalogue.yaml", "ChannelSync", "catalogue.channel_sync", ["salesChannelId", "domain"]),
            ("contracts/satellite/subscription.yaml", "ModuleListing", "control.module_listing", ["moduleCode"])):
        ut = sch(rel, name).get("x-ticvai-unique-together") or []
        need("BR-R13-UPSERT-KEY", cols in [list(x) for x in ut],
             f"{name} declares no x-ticvai-unique-together {cols}, so {table} has no unique key behind its upsert (R20)")
    need("BR-R13-UPSERT-KEY", op("setChannelSyncSetting")[3].get("x-ticvai-body-key") == ["salesChannelId", "domain"],
         "setChannelSyncSetting is keyed by salesChannelId alone, not by the channel and domain its text says (R20)")

    # BR-R13-WALLET-TRANSFER-ETAG (R24): the version getWalletTransferRules promised, by CR-332's rule.
    wtr = sch("contracts/satellite/wallet.yaml", "WalletTransferRules")
    ver = (wtr.get("properties") or {}).get("version") or {}
    need("BR-R13-WALLET-TRANSFER-ETAG", ver.get("type") == "integer" and ver.get("readOnly") is True
         and "version" in (wtr.get("required") or []),
         "WalletTransferRules has no required, readOnly integer version for setWalletTransferRules' If-Match (R24)")
    for oid in ("getWalletTransferRules", "setWalletTransferRules"):
        hdr = (((op(oid)[3].get("responses") or {}).get("200") or {}).get("headers") or {}).get("ETag") or {}
        need("BR-R13-WALLET-TRANSFER-ETAG", "version" in str(hdr.get("description") or ""),
             f"{oid}'s 200 sends no ETag that is wallet.transfer_rule.version (R24)")
    need("BR-R13-WALLET-TRANSFER-ETAG",
         "`412` and nothing changes" in words(op("setWalletTransferRules")[3].get("description")),
         "setWalletTransferRules does not say a stale If-Match is 412 and nothing changes (R24)")

    # BR-R13-GUEST-ROWS (R28): row security admits the caller the operation names.
    cc = op("claimCart")[3]
    ctext = words(cc.get("description"))
    need("BR-R13-GUEST-ROWS", "ITenantRootGrant" in ctext and "Nothing else runs under the root grant" in ctext
         and "404" in {str(k) for k in (cc.get("responses") or {})},
         "claimCart does not read and attach the anonymous cart under ITenantRootGrant after its token check, with "
         "the shared 404 (R28)")
    need("BR-R13-GUEST-ROWS",
         sch("contracts/satellite/retail.yaml", "ShopAndDrop").get("x-ticvai-rls") == "guest-reads-own",
         "ShopAndDrop is not x-ticvai-rls guest-reads-own, so a guest cannot read its own drops (R28)")
    tt = sch("contracts/spine/orders.yaml", "TicketTransfer")
    need("BR-R13-GUEST-ROWS", tt.get("x-ticvai-rls") == "guest-reads-own"
         and tt.get("x-ticvai-guest-subject") == ["fromSubjectId", "toSubjectId"],
         "TicketTransfer does not let the guest fromSubjectId or toSubjectId names read it (R28)")
    rev = words(op("revokeEntitlementShare")[3].get("description"))
    need("BR-R13-GUEST-ROWS", "over_subject_id" in rev and "the shared `404` before any write" in rev,
         "revokeEntitlementShare does not say what a guest who is not the owner gets (R28)")

    # BR-R13-REPRINT-GUEST (R27): reprintOrder serves a guest-checkout buyer and answers the wallet passes.
    rp = op("reprintOrder")[3]
    pnames = {str((x or {}).get("name") or (x or {}).get("$ref")) for x in rp.get("parameters") or []
              if isinstance(x, dict)}
    need("BR-R13-REPRINT-GUEST", "X-Order-Access-Token" in pnames and any("DeviceId" in n for n in pnames),
         "reprintOrder takes no X-Order-Access-Token and X-Device-Id, so a guest-checkout buyer is refused (R27)")
    props = (((((rp.get("responses") or {}).get("200") or {}).get("content") or {}).get("application/json") or {})
             .get("schema") or {}).get("properties") or {}
    need("BR-R13-REPRINT-GUEST", "WalletPass" in str((props.get("walletPasses") or {}).get("items")),
         "reprintOrder's 200 carries no walletPasses for delivery wallet (R27)")
    # email, sms and whatsapp go through Access as order.ticketsResent since ADAM CR-506 (CHG-CR506-001), which replaced
    # R27's sendTransactionalMessage route; BR-RESEND-THROUGH-ACCESS holds it
    need("BR-R13-REPRINT-GUEST", "order.ticketsResent" in (rp.get("x-ticvai-emits") or []),
         "reprintOrder does not say how email, sms and whatsapp are sent (R27; CR-506)")

    # BR-R13-WRITES-LISTED (R21): the tables the text writes or reads are listed.
    for oid, key, want in (("restoreConfigVersion", "x-ticvai-writes",
                            {"whitelabel.content_page", "whitelabel.booking_flow_step",
                             "whitelabel.footer_config_column", "whitelabel.footer_config_social_link"}),
                           ("cloneProduct", "x-ticvai-writes", {"catalogue.price"}),
                           ("bulkChangePrices", "x-ticvai-writes", {"catalogue.price"}),
                           ("bulkChangePrices", "x-ticvai-reads", {"catalogue.price"}),
                           ("getTenantLicences", "x-ticvai-reads", {"control.plan_module", "control.plan_limit"})):
        got = tables(op(oid)[3], key)
        need("BR-R13-WRITES-LISTED", want <= got, f"{oid}'s {key} omits {sorted(want - got)}, which its text uses (R21)")
    need("BR-R13-WRITES-LISTED", "409" in {str(k) for k in (op("cloneProduct")[3].get("responses") or {})},
         "cloneProduct declares no 409 duplicate-code for a code already used (R21)")

    # BR-R13-READS-DECLARED (R39): the data the text uses has a declared read.
    for oid, q in (("getCurrentSession", "tenancy#outletRecords"), ("setDeviceAssignment", "identity#principalRecords"),
                   ("reserveMerchandise", "tenancy#outletRecords"),
                   ("reserveMerchandise", "tenancy#venueSettingsRecords"),
                   ("reserveMerchandise", "tenancy#regionSettingsRecords"),
                   ("proposeTranslations", "catalogue#productRecords")):
        need("BR-R13-READS-DECLARED", q in vias(op(oid)[3]), f"{oid} declares no read-via {q} (R39)")
    for oid, t in (("getSiteSetupProgress", "whitelabel.booking_flow_step"), ("setSubscription", "control.plan_module"),
                   ("setSubscription", "control.plan_limit")):
        need("BR-R13-READS-DECLARED", t in tables(op(oid)[3], "x-ticvai-reads"), f"{oid} declares no read of {t} (R39)")

    # BR-R13-FIELDS-KEPT (R40): a field an operation takes or promises has a column.
    wg = sch("contracts/satellite/queue.yaml", "WaitingGuest").get("properties") or {}
    need("BR-R13-FIELDS-KEPT", {"callResolvedAt", "callResolutionReason", "callResolvedByPrincipalId"} <= set(wg),
         "WaitingGuest has no column for resolveCalledWaitingGuest's reason and time (R40)")
    need("BR-R13-FIELDS-KEPT", "failureReason" in (sch("contracts/satellite/white-label.yaml", "SitePackage")
                                                   .get("properties") or {}),
         "SitePackage has no failureReason for the job's reason (R40)")
    need("BR-R13-FIELDS-KEPT", "writtenAt" in (body(op("recordSubjectDataExportPart")[3]).get("properties") or {}),
         "recordSubjectDataExportPart's body carries no writtenAt (R40)")

    # BR-R13-ONE-RULE (R41): an operation does not contradict its own schema or another text.
    need("BR-R13-ONE-RULE", "per outlet" in words(op("setKitchenStations")[3].get("x-ticvai-singleton-note")),
         "setKitchenStations' singleton note says one set per venue against its required outletId (R41)")
    cor = (sch("contracts/spine/orders.yaml", "CreateOrderRequest").get("properties") or {}).get("id") or {}
    need("BR-R13-ONE-RULE", "fresh UUIDv7" in words(cor.get("description"))
         and "fresh UUIDv7" in words(op("syncOrders")[3].get("description")),
         "syncOrders and CreateOrderRequest.id do not say the header is a fresh key per batch POST (R41)")
    pf = (sch("contracts/satellite/ai.yaml", "IndexSource").get("properties") or {}).get("payloadFields") or {}
    need("BR-R13-ONE-RULE", "the vectors are in the tenant database" not in words(pf.get("description")).replace("**", ""),
         "IndexSource.payloadFields still says the vectors are in the tenant database, against ADR-0049 (R41)")
    need("BR-R13-ONE-RULE", "the hours rule is CR-104" not in str(op("createShopAndDrop")[3].get("x-ticvai-read-via")),
         "createShopAndDrop's read-via still gives CR-104's outlet hours as the rule the lead replaced (R41)")
    need("BR-R13-ONE-RULE", "stored with `requiresApproval` true" in words(op("setSubstitutionRules")[3].get("description")),
         "setSubstitutionRules does not state when requiresApproval is true (R41)")


LANE_W2_R13_RULES = ["BR-VENUE-LIMIT-DEFAULT", "BR-ENROL-FIELDS", "BR-CART-ANONYMOUS", "BR-TENANT-ROW-READ",
                     "BR-TAMPER-DETECTED-AT", "BR-TRANSFER-GUEST-WRITE", "BR-RESEND-THROUGH-ACCESS",
                     "BR-HELD-LEASES-NOOP", "BR-EXPECTED-CASH", "BR-QUEUE-EVENT-READS", "BR-HOST-IDEMPOTENCY"]


def lane_w2_rules_r13(need, op):
    """r13 second CR round, lane w2 (ADAM CR-484 to CR-527, decided by Chinmay on 3 November 2026; CHG-CR484-001 to
    CHG-CR527-001). Each rule fails on the r13 candidate before the lane (f599f2c6) and passes on its change."""
    def words(x):
        return " ".join(str(x or "").split())

    def vias(o_):
        return {(str((v or {}).get("query")), str((v or {}).get("route")))
                for v in o_.get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def tables(o_, key):
        return {str((t or {}).get("table") if isinstance(t, dict) else t) for t in o_.get(key) or []}

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def codes(o_):
        return {str(k) for k in (o_.get("responses") or {})}

    def schemas(rel):
        return (load(rel).get("components") or {}).get("schemas") or {}

    def body(o_):
        return ((((o_.get("requestBody") or {}).get("content") or {}).get("application/json") or {}).get("schema")
                or {})

    def payload(rel):
        return {str((f or {}).get("field")): f for f in load(rel).get("payload") or [] if isinstance(f, dict)}

    ten = schemas("contracts/spine/tenancy.yaml")
    ords = schemas("contracts/spine/orders.yaml")

    # BR-VENUE-LIMIT-DEFAULT (CR-484): every configured limit a venue inherits carries its proposed tenant default, and
    # no read fills the venue's value from a parameter default before the venue is asked.
    vs = ten.get("VenueSettings") or {}
    for name, pr in (vs.get("properties") or {}).items():
        if (isinstance(pr, dict) and pr.get("type") in ("integer", "number") and pr.get("nullable") is True
                and "inherits the tenant default" in words(pr.get("description"))):
            need("BR-VENUE-LIMIT-DEFAULT", "default" in pr,
                 f"VenueSettings.{name} inherits the tenant default but carries no proposed default, so "
                 "getVenueSettingsDefaults answers null (CR-484)")
    sm = next((x for x in op("listProductStartTimes")[3].get("parameters") or []
               if isinstance(x, dict) and x.get("name") == "stepMinutes"), {})
    need("BR-VENUE-LIMIT-DEFAULT", "default" not in (sm.get("schema") or {}),
         "listProductStartTimes' stepMinutes parameter carries a default that fills it before the venue is asked (CR-484)")

    # BR-ENROL-FIELDS (CR-485)
    edv = op("enrolDevice")[3]
    tr = ((ten.get("DeviceEnrolment") or {}).get("properties") or {}).get("testResult") or {}
    need("BR-ENROL-FIELDS", "validation" in ptypes(edv, "400") and tr.get("required") == ["passed"]
         and "these body checks, then the move check" in words(edv.get("description")),
         "enrolDevice does not require testResult on the move to provisioned and refuse it, and configurationProfileId, "
         "on any other move with 400 validation, checked first (CR-485)")

    # BR-CART-ANONYMOUS (CR-486)
    cc = op("createCart")[3]
    tok = ((ords.get("Cart") or {}).get("properties") or {}).get("token") or {}
    need("BR-CART-ANONYMOUS", ("tenancy#activeVenues", "in-process") in vias(cc) and {"403", "404"} <= codes(cc)
         and "ITenantRootGrant" in words(cc.get("description")),
         "createCart does not check the venue with tenancy#activeVenues (404), refuse a subjectId it may not name "
         "(403), or write the anonymous cart's one insert under ITenantRootGrant (CR-486)")
    need("BR-CART-ANONYMOUS", tok.get("x-ticvai-secret") == "field-encrypted" and tok.get("nullable") is True,
         "Cart.token is not stored field-encrypted, or not null on a signed-in guest's or staff cart (CR-486)")

    # BR-TENANT-ROW-READ (CR-487)
    ddl = (ROOT / "tools/derive-ddl.py").read_text(encoding="utf-8")
    need("BR-TENANT-ROW-READ", vs.get("x-ticvai-tenant-row-read") is True
         and "(venue_id IS NULL AND cardinality(platform.current_scope_paths()) > 0)" in ddl,
         "platform.venue_settings does not let a scoped session read the tenant's own row (CR-487)")

    # BR-TAMPER-DETECTED-AT (CR-492): a field the request may leave out is not published as always there
    det = payload("events/device-tamperDetected.yaml").get("detectedAt") or {}
    tbody = ten.get("DeviceTamperEvent") or {}
    need("BR-TAMPER-DETECTED-AT", "detectedAt" in (tbody.get("required") or []) or det.get("required") is False,
         "device.tamperDetected requires detectedAt, which recordDeviceTamperEvent's body may leave out (CR-492)")
    need("BR-TAMPER-DETECTED-AT", "never filled from `recordedAt`" in words(op("recordDeviceTamperEvent")[3]
                                                                             .get("description")).replace("It is ", ""),
         "recordDeviceTamperEvent does not say detectedAt is stored and published as sent, never filled (CR-492)")

    # BR-TRANSFER-GUEST-WRITE (CR-502)
    need("BR-TRANSFER-GUEST-WRITE", (ords.get("TicketTransfer") or {}).get("x-ticvai-guest-writer") == "fromSubjectId"
         and "ITenantRootGrant" in words(op("claimTicketTransfer")[3].get("description")),
         "orders.ticket_transfer does not admit the sender's own write by subject, or claimTicketTransfer does not "
         "update its one row under ITenantRootGrant once the token is verified (CR-502)")

    # BR-RESEND-THROUGH-ACCESS (CR-506)
    rp = op("reprintOrder")[3]
    rpb = (body(rp).get("properties") or {})
    evp = ROOT / "events/order-ticketsResent.yaml"
    ev = load("events/order-ticketsResent.yaml") if evp.exists() else {}
    need("BR-RESEND-THROUGH-ACCESS", "order.ticketsResent" in (rp.get("x-ticvai-emits") or [])
         and (rpb.get("walletPlatform") or {}).get("enum") == ["apple", "google"]
         and "sendTransactionalMessage" not in words(rp.get("description"))
         and any((c or {}).get("context") == "access" for c in ev.get("consumers") or [])
         and (ords.get("OrderEvent") or {}).get("x-ticvai-guest-insert") == {"eventType": "ticketsResent"}
         and "apply_split_insert_rls" in ddl,
         "reprintOrder does not send email, sms and whatsapp through Access as order.ticketsResent, take walletPlatform, "
         "or let a guest append its ticketsResent row by an insert-only branch (CR-506)")

    # BR-HELD-LEASES-NOOP (CR-517) and BR-EXPECTED-CASH (CR-518)
    for oid in ("closeShift", "submitShiftCount"):
        o_ = op(oid)[3]
        d_ = words(o_.get("description"))
        need("BR-HELD-LEASES-NOOP", not any(q.startswith("catalogue#") for q, _r in vias(o_))
             and "`releaseHeldLeases` changes nothing" in d_ and "400" in codes(o_),
             f"{oid} gives releaseHeldLeases a path to Catalogue, or does not say it changes nothing (CR-517)")
        need("BR-EXPECTED-CASH", ("finance#fxRateRecords", "in-process") not in vias(o_)
             and {"orders.refund", "orders.refund_payment", "orders.cash_movement", "orders.payment"}
             <= tables(o_, "x-ticvai-reads"),
             f"{oid} still reads ledger.fx_rate, or does not read the refunds and cash its expected cash is made of "
             "(CR-518)")
    need("BR-EXPECTED-CASH", "A + B - C + D - E - F" in words(op("submitShiftCount")[3].get("description"))
         and "`pending`, `held` or `partiallyPaid`" in words(op("closeShift")[3].get("description")),
         "submitShiftCount does not state the expected-cash formula, or closeShift what an open order is (CR-518)")

    # BR-QUEUE-EVENT-READS (CR-519)
    for oid in ("redeemWaitingGuest", "overrideWaitingGuest"):
        o_ = op(oid)[3]
        need("BR-QUEUE-EVENT-READS", "queue.queue" in tables(o_, "x-ticvai-reads")
             and ("tenancy#scopeRecords", "in-process") in vias(o_) and "400" in codes(o_)
             and "`party_size`" in words(o_.get("description")),
             f"{oid} writes queueEntry.redeemed with the queue's venue, access point and scope path but declares no "
             "read of them, or does not bound admittedCount by party_size (CR-519)")

    # BR-HOST-IDEMPOTENCY (CR-527)
    tp = load("contracts/devices/ticket-printer.yaml")
    pj = ((tp.get("paths") or {}).get("/ticket-printer/print-jobs") or {}).get("post") or {}
    td = words((tp.get("info") or {}).get("description"))
    need("BR-HOST-IDEMPOTENCY", "idempotency-conflict" in ptypes(pj, "409") and "%ProgramData%" in td
         and "The key is saved before printing" in td and "never sent to the printer again" in td,
         "the device host does not keep its Idempotency-Keys in files saved before printing, with the 409 and the "
         "restart rule (CR-527)")
R13_W5_RULES = ["BR-CELL-TIER-ACTIVE", "BR-CELL-TIER-JOB", "BR-TENANT-LIMITS-DEFAULT", "BR-TENANT-LIMITS-ROUTE",
                "BR-PLAN-VERSIONS", "BR-MODULE-CATALOGUE-AUDIENCE", "BR-MODULE-LISTING-UPSERT", "BR-LICENCE-COMBINE",
                "BR-ADDON-MODULE-KEY", "BR-DOWNGRADE-CHECK"]


def lane_w5_rules_r13(need, op, ops):
    """r13 second CR round, lane w5 (ADAM CR-488, CR-489, CR-490, CR-491, CR-510, CR-529, CR-530, CR-531, CR-535,
    CR-541; posted 3 November 2026 under the lead's "Close the CRs and respond to devs" and "get the NEw CRs in the
    r13"). Each fails on the r13 candidate f599f2c6.

      BR-CELL-TIER-ACTIVE          (CR-488) updateCellTier refuses a cell that is not active, 409 cell-not-active, before
                                   any other check.
      BR-CELL-TIER-JOB             (CR-489) updateCellTier queues a tierMigration job and leaves control.cell alone; a
                                   second one is 409 tier-change-pending; the cell becomes migrating when the job starts
                                   (states/cell.yaml, a job transition the cell job runner makes), and a job whose cell
                                   cannot take it fails from queued.
      BR-TENANT-LIMITS-DEFAULT     (CR-490) the platform default is the configuration key
                                   RequestLimits:Tenant:PlatformDefault, filled audience by audience, not a sizing tier.
      BR-TENANT-LIMITS-ROUTE       (CR-491) tenantRequestLimits is served as getTenantRequestLimits, GET
                                   /internal/tenant-request-limits?tenantId=, serviceAuth, 200 PlanRequestLimits, 400, 401.
      BR-PLAN-VERSIONS             (CR-510) versions numbered 1, 2, 3, the newest active; one currency per version; 400s
                                   for currency, duplicates and a changed code; 404 on createPlanVersion; control.plan
                                   unique on (lower(code), version), plan_module and plan_limit unique per version.
      BR-MODULE-CATALOGUE-AUDIENCE (CR-529) listModuleCatalogue stays public; non-staff see available and beta only;
                                   staff keep PLATFORM_PLAN_MANAGE.
      BR-MODULE-LISTING-UPSERT     (CR-530) setModuleListing is one upsert on lower(module_code) that keeps the row's id,
                                   behind the unique key on ModuleListing.moduleCode.
      BR-LICENCE-COMBINE           (CR-531) LicencePosition states the one combining method (current contract, source,
                                   core, limits, overage row) and its limits are not control.tenant.plan_id's.
      BR-ADDON-MODULE-KEY          (CR-535) addLicenceAddOn accepts a ModuleKey other than core, refuses anything else
                                   400 and reads no control.module_listing.
      BR-DOWNGRADE-CHECK           (CR-541) setSubscription asks white-label getModuleEnablement for the downgrade check,
                                   answers 503 when the cell does not, and previewSubscriptionChange runs the same check.
    """
    def words(x):
        return " ".join(str(x or "").split())

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def tabs(o_, key):
        return {str((r or {}).get("table")) for r in o_.get(key) or [] if isinstance(r, dict)}

    sub = load("contracts/satellite/subscription.yaml")
    sch = (sub.get("components") or {}).get("schemas") or {}

    # BR-CELL-TIER-ACTIVE (CR-488)
    uct = op("updateCellTier")[3]
    ud = words(uct.get("description"))
    need("BR-CELL-TIER-ACTIVE", "cell-not-active" in ptypes(uct, "409"),
         "updateCellTier's 409 does not list cell-not-active (CR-488)")
    need("BR-CELL-TIER-ACTIVE", "before any other check, a cell whose `status` is anything but `active`" in ud,
         "updateCellTier does not refuse a cell that is not active before its other checks (CR-488)")

    # BR-CELL-TIER-JOB (CR-489)
    need("BR-CELL-TIER-JOB", "tier-change-pending" in ptypes(uct, "409"),
         "updateCellTier's 409 does not list tier-change-pending (CR-489)")
    need("BR-CELL-TIER-JOB", "It does not change `control.cell.status`" in ud and "A future `scheduledFor` is accepted" in ud,
         "updateCellTier does not say the cell stays active until its job starts (CR-489)")
    need("BR-CELL-TIER-JOB", tabs(uct, "x-ticvai-writes") == {"control.cell_job"},
         "updateCellTier does not write control.cell_job alone (CR-489)")
    cell = load("states/cell.yaml")
    tier = [t for t in cell.get("transitions") or []
            if t.get("from") == "active" and t.get("to") == "migrating" and "tier" in words(t.get("guard")).lower()]
    need("BR-CELL-TIER-JOB", bool(tier) and all(t.get("trigger") == "job" and not t.get("operation") for t in tier),
         "states/cell.yaml still moves the cell to migrating at updateCellTier, not when its job starts (CR-489)")
    runner = ((sub.get("x-ticvai-jobs") or {}).get("cellJobRunner") or {}).get("moves") or []
    for mv in ({"model": "cell", "from": "active", "to": "migrating"},
               {"model": "cell-job", "from": "queued", "to": "failed"}):
        need("BR-CELL-TIER-JOB", mv in runner, f"the cell job runner does not move {mv} (CR-489)")

    # BR-TENANT-LIMITS-DEFAULT (CR-490)
    trl = (sub.get("x-ticvai-queries") or {}).get("tenantRequestLimits") or {}
    tr = words(trl.get("rule"))
    for frag in ("`RequestLimits:Tenant:PlatformDefault`", "not computed from a sizing tier",
                 "else the platform default's value for that audience", "the contract defaults of 25 and 70",
                 "that audience has no tenant budget"):
        need("BR-TENANT-LIMITS-DEFAULT", frag in tr, f"tenantRequestLimits does not state {frag!r} (CR-490)")
    prl = words((sch.get("PlanRequestLimits") or {}).get("description"))
    need("BR-TENANT-LIMITS-DEFAULT", "RequestLimits:Tenant:PlatformDefault" in prl and "expected peak" not in prl,
         "PlanRequestLimits still takes the platform default from a sizing tier (CR-490)")
    adr = words((ROOT / "docs/adr/0064-per-tenant-limits.md").read_text(encoding="utf-8"))
    need("BR-TENANT-LIMITS-DEFAULT", "RequestLimits:Tenant:PlatformDefault" in adr,
         "ADR-0064 does not name the platform default's configuration key (CR-490)")

    # BR-TENANT-LIMITS-ROUTE (CR-491)
    f_, path_, meth_, gtl, _d = op("getTenantRequestLimits")
    need("BR-TENANT-LIMITS-ROUTE", path_ == "/internal/tenant-request-limits" and meth_ == "get"
         and (gtl.get("security") or []) == [{"serviceAuth": []}] and gtl.get("x-ticvai-permission") is None,
         "getTenantRequestLimits is not GET /internal/tenant-request-limits under serviceAuth alone (CR-491)")
    tid = [p for p in gtl.get("parameters") or [] if isinstance(p, dict) and p.get("name") == "tenantId"]
    need("BR-TENANT-LIMITS-ROUTE", bool(tid) and tid[0].get("in") == "query" and tid[0].get("required") is True
         and (tid[0].get("schema") or {}).get("format") == "uuid",
         "getTenantRequestLimits does not take tenantId as a required uuid query parameter (CR-491)")
    rs = gtl.get("responses") or {}
    need("BR-TENANT-LIMITS-ROUTE", {"200", "400", "401", "429"} <= set(rs) and "404" not in rs
         and str(((((rs.get("200") or {}).get("content") or {}).get("application/json") or {}).get("schema") or {})
                 .get("$ref", "")).endswith("/PlanRequestLimits"),
         "getTenantRequestLimits does not answer 200 PlanRequestLimits, 400, 401 and 429, with no 404 (CR-491)")
    need("BR-TENANT-LIMITS-ROUTE", trl.get("operation") == "getTenantRequestLimits",
         "tenantRequestLimits does not name its operation getTenantRequestLimits (CR-491)")
    need("BR-TENANT-LIMITS-ROUTE", "/queries/tenant-request-limits" not in (sub.get("paths") or {}),
         "Platform still has a POST /queries/tenant-request-limits route (CR-491)")

    # BR-PLAN-VERSIONS (CR-510)
    cp, cpv = op("createPlan")[3], op("createPlanVersion")[3]
    need("BR-PLAN-VERSIONS", {"plan-currency-mismatch", "duplicate-plan-module", "duplicate-limit-metric"}
         <= ptypes(cp, "400"), "createPlan's 400 does not list the currency and duplicate refusals (CR-510)")
    need("BR-PLAN-VERSIONS", {"plan-code-changed", "plan-currency-mismatch", "duplicate-plan-module",
                              "duplicate-limit-metric"} <= ptypes(cpv, "400") and "404" in (cpv.get("responses") or {}),
         "createPlanVersion does not answer 404 and the 400 refusals of CR-510")
    cvd = words(cpv.get("description"))
    for frag in ("FOR UPDATE", "the highest existing version compared as an integer, plus 1",
                 "sets `isActive` false on every earlier version"):
        need("BR-PLAN-VERSIONS", frag in cvd, f"createPlanVersion does not state {frag!r} (CR-510)")
    need("BR-PLAN-VERSIONS", "version `1`" in words(cp.get("description")),
         "createPlan does not write version 1 (CR-510)")
    plan = sch.get("Plan") or {}
    cpr = (sch.get("CreatePlanRequest") or {}).get("properties") or {}
    need("BR-PLAN-VERSIONS", ["code", "version"] in (plan.get("x-ticvai-unique-together") or [])
         and "x-ticvai-unique" not in (cpr.get("code") or {}),
         "control.plan is not unique on (lower(code), version) in place of plan_code_uniq (CR-510)")
    need("BR-PLAN-VERSIONS", ["plan_id", "plan_version", "licensed_module"]
         in ((cpr.get("licensedModules") or {}).get("x-ticvai-unique-together") or [])
         and ["plan_id", "plan_version", "metric"] in ((cpr.get("limits") or {}).get("x-ticvai-unique-together") or []),
         "control.plan_module and control.plan_limit have no unique key per plan version (CR-510)")

    # BR-MODULE-CATALOGUE-AUDIENCE (CR-529)
    lmc = op("listModuleCatalogue")[3]
    ld = words(lmc.get("description"))
    need("BR-MODULE-CATALOGUE-AUDIENCE", lmc.get("x-ticvai-permission") == "PLATFORM_PLAN_MANAGE"
         and lmc.get("x-ticvai-guest-callable") is True and {} in (lmc.get("security") or []),
         "listModuleCatalogue is no longer a public read with PLATFORM_PLAN_MANAGE for staff (CR-529)")
    need("BR-MODULE-CATALOGUE-AUDIENCE", "whose `status` is `available` or `beta`" in ld
         and "with it, the call gets every row with its status" in ld,
         "listModuleCatalogue does not say which listings non-staff and staff callers see (CR-529)")

    # BR-MODULE-LISTING-UPSERT (CR-530)
    sml = words(op("setModuleListing")[3].get("description"))
    need("BR-MODULE-LISTING-UPSERT", "keeps the existing row's id" in sml and "no advisory lock" in sml
         and "lower(module_code)" in sml,
         "setModuleListing does not upsert on lower(module_code) keeping the row's id (CR-530)")
    need("BR-MODULE-LISTING-UPSERT", ["moduleCode"] in ((sch.get("ModuleListing") or {})
                                                        .get("x-ticvai-unique-together") or []),
         "ModuleListing has no unique key on moduleCode (CR-530)")

    # BR-LICENCE-COMBINE (CR-531)
    lp = sch.get("LicencePosition") or {}
    lpd = words(lp.get("description"))
    for frag in ("One combining method", "the in-force contract with the latest start date; on a tie, the greatest id",
                 "even if an add-on also covers it", "`core` is always listed with `source` `plan`",
                 "`displayName` is left empty", "or 0 when the plan does not have the metric",
                 "the row of the add-on with the latest `validFrom`"):
        need("BR-LICENCE-COMBINE", frag in lpd, f"LicencePosition does not state {frag!r} (CR-531)")
    need("BR-LICENCE-COMBINE", "control.tenant.plan_id" not in words(lp.get("x-ticvai-persistence")),
         "LicencePosition's limits still come from control.tenant.plan_id (CR-531)")
    for oid in ("getTenantLicences", "addLicenceAddOn", "removeLicenceAddOn"):
        need("BR-LICENCE-COMBINE", "combining method" in words(op(oid)[3].get("description")),
             f"{oid} does not answer through LicencePosition's one combining method (CR-531)")
    need("BR-LICENCE-COMBINE", "control.tenant.plan_id" not in words(op("removeLicenceAddOn")[3]),
         "removeLicenceAddOn still takes the limits from control.tenant.plan_id (CR-531)")

    # BR-ADDON-MODULE-KEY (CR-535)
    ala = op("addLicenceAddOn")[3]
    ad = words(ala.get("description"))
    need("BR-ADDON-MODULE-KEY", "not in the module listing" not in ad
         and "is not a licence module key (`ModuleKey`; `core` excluded) is 400" in ad
         and "before the lock is taken" in ad,
         "addLicenceAddOn does not refuse a key that is not a licence module key (core excluded) before the lock "
         "(CR-535)")
    need("BR-ADDON-MODULE-KEY", "400" in (ala.get("responses") or {}),
         "addLicenceAddOn declares no 400 (CR-535)")
    need("BR-ADDON-MODULE-KEY", "control.module_listing" not in tabs(ala, "x-ticvai-reads"),
         "addLicenceAddOn reads control.module_listing (CR-535)")

    # BR-DOWNGRADE-CHECK (CR-541)
    ss, psc = op("setSubscription")[3], op("previewSubscriptionChange")[3]
    need("BR-DOWNGRADE-CHECK", "white-label.getModuleEnablement" in (ss.get("x-ticvai-calls") or [])
         and "white-label.getModuleEnablement" in (psc.get("x-ticvai-calls") or []),
         "setSubscription and previewSubscriptionChange do not declare the call to white-label getModuleEnablement "
         "(CR-541)")
    need("BR-DOWNGRADE-CHECK", "503" in (ss.get("responses") or {}),
         "setSubscription declares no 503 for a cell that does not answer (CR-541)")
    sd = words(ss.get("description"))
    for frag in ("every in-force add-on (add-ons survive a plan change) and `core`", "plus every unexpired capacity pack",
                 "as `getEntitlementUsage` works out `current`", "never decides on a guess"):
        need("BR-DOWNGRADE-CHECK", frag in sd, f"setSubscription's downgrade check does not state {frag!r} (CR-541)")
    need("BR-DOWNGRADE-CHECK", "the same check" in words(psc.get("description")),
         "previewSubscriptionChange does not return the conflicts from setSubscription's check (CR-541)")


R13_W3_RULES = ["BR-GST007-AS-BUILT", "BR-GST008-PHOTO-BADGE", "BR-BOOKING-FLOW-EVENT", "BR-FORM-ROOT-READ",
                "BR-CONFIG-DIFF-SHAPE", "BR-PERFORMANCE-INTO-TICKETS", "BR-PREVIEW-ADDRESS", "BR-SESSION-BATCH-RECORD",
                "BR-GUEST-DOCUMENT-UPLOAD", "BR-KIOSK-CHECK-ROWS", "BR-WEB022-STATUS-PILL", "BR-SCHEDULED-PUBLISH-RUN",
                "BR-PUBLISH-REVIEW-DEFAULT"]


def lane_w3_rules_r13(need, op):
    """r13 second CR round, lane w3 (ADAM CR-493 to CR-534, decided by Chinmay on 3 November 2026: "Close the CRs and
    respond to devs", "get the NEw CRs in the r13"; CHG-CR493-001 to CHG-CR534-001). Each rule fails on the r13
    candidate before the lane (f599f2c6) and passes once the posted decision is in."""
    def words(x):
        return " ".join(str(x or "").split())

    def vias(o_):
        return {(str((v or {}).get("query")), str((v or {}).get("route")))
                for v in o_.get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def tables(o_, key):
        return {str((t or {}).get("table")) for t in o_.get(key) or [] if isinstance(t, dict)}

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def schemas(rel):
        return (load(rel).get("components") or {}).get("schemas") or {}

    def screen(rel, sid):
        return next((x for x in load(rel).get("screens") or [] if (x or {}).get("id") == sid), {})

    def components(scr):
        return [c for r in ((scr.get("layout") or {}).get("regions") or []) for c in (r or {}).get("components") or []]

    def overlay(scr, oid):
        return next((o_ for o_ in scr.get("overlays") or [] if (o_ or {}).get("id") == oid), {})

    def params(scr):
        return {str((p or {}).get("name")): p for p in ((scr.get("entryState") or {}).get("params") or [])}

    def query(rel, name):
        return ((load(rel).get("x-ticvai-queries") or {}).get(name)) or {}

    p01, p02 = "screens/P01-guest-web-storefront.yaml", "screens/P02-guest-mobile-app.yaml"
    xdr = {str((r or {}).get("id")): r for r in load("docs/active/cross-deployable-writes.yaml").get("reads") or []
           if isinstance(r, dict)}
    lo = {str((i or {}).get("id")) for i in load("docs/active/left-out.yaml").get("items") or [] if isinstance(i, dict)}

    # BR-GST007-AS-BUILT (CR-493): coach-mark cards, the More dates calendar, the one-question Yes / No pop-up with a close
    g7 = screen(p02, "GST-007")
    cq, mc, qt = overlay(g7, "consentQuestions"), overlay(g7, "monthCalendar"), overlay(g7, "quickTour")
    cqb = words(cq.get("body"))
    need("BR-GST007-AS-BUILT", "one question at a time" in cqb and "on every platform" in cqb
         and "records it on the second tap" in cqb and "after the last question" in cqb
         and "Close" in str((cq.get("dismiss") or {}).get("label")) and (cq.get("dismiss") or {}).get("discards") == ["answers"]
         and (cq.get("confirm") or {}).get("operation") == "recordConsentAnswers",
         "GST-007's consent pop-up is not the one-question Yes / No pop-up with a close (x) that discards the answers (CR-493)")
    need("BR-GST007-AS-BUILT", (mc.get("confirm") or {}).get("label") == "OK" and (mc.get("dismiss") or {}).get("label") == "Cancel"
         and "Sunday-first" in words(mc.get("body")) and "mirror in Arabic" in words(mc.get("body")),
         "GST-007 has no in-app month calendar behind More dates (OK / Cancel, Sunday-first, mirrored in Arabic) (CR-493)")
    need("BR-GST007-AS-BUILT", "260-wide card" in words(qt.get("body"))
         and "the date card, the entry windows, Continue, the selection summary" in words(qt.get("body")),
         "GST-007's quick tour is not the four coach-mark cards in the built order (CR-493)")

    # BR-GST008-PHOTO-BADGE (CR-494)
    g8 = screen(p02, "GST-008")
    tt = next((c for c in components(g8) if (c or {}).get("label") == "Ticket types"), {})
    need("BR-GST008-PHOTO-BADGE", "photoIntoCardGradient" in words(g8.get("notes"))
         and "whether `ticketTags` is on or off" in words(g8.get("notes")) and "photoIntoCardGradient" in words(tt.get("notes")),
         "GST-008 does not state the photo fading into the white card and the N selected badge beside the kind icon (CR-494)")
    fr = (ROOT / "wireframes/frames/gst-008.html").read_text(encoding="utf-8")
    need("BR-GST008-PHOTO-BADGE", '<span class="tag">3 selected</span>' not in fr and 'class="sel">3 selected' in fr
         and ".v4f-gst-008 .tk.open .ph{height:190px" in fr,
         "wireframes/frames/gst-008.html still draws the selected badge as a tag, or the open photo is not 190 high (CR-494)")

    # BR-BOOKING-FLOW-EVENT (CR-495)
    gpb = op("getPublishedBookingFlow")[3]
    gpd = words(gpb.get("description"))
    need("BR-BOOKING-FLOW-EVENT", "eventId" in {(p or {}).get("name") for p in gpb.get("parameters") or []}
         and "where {`venueId`, `eventId`}" in gpd and "`flowTypeKey` and `eventId` the answer is 400" in gpd
         and "The first product that resolves to an enabled flow wins" in gpd
         and ("catalogue#eventRecords", "in-process") in vias(gpb),
         "getPublishedBookingFlow does not resolve the flow from an eventId as CR-495 decided")
    need("BR-BOOKING-FLOW-EVENT", "getPublishedBookingFlow" in ((xdr.get("XDR-110") or {}).get("operations") or []),
         "XDR-110 does not name getPublishedBookingFlow's in-process event read (CR-495)")
    g7api = next((a for a in g7.get("apis") or [] if a.get("operationId") == "getPublishedBookingFlow"), {})
    need("BR-BOOKING-FLOW-EVENT", "`{ eventId }`" in words(g7api.get("purpose")) and "productId" in params(g7),
         "GST-007 does not send { productId } when it has one, else { eventId } (CR-495)")

    # BR-FORM-ROOT-READ (CR-496)
    sf = op("submitForm")[3]
    sfd = words(sf.get("description"))
    need("BR-FORM-ROOT-READ", "`ITenantRootGrant`" in sfd and "`scope_path <@ ANY(paths) OR scope_path @> ANY(paths)`" in sfd
         and "(`SET LOCAL` back)" in sfd and "marketing.form_definition" in tables(sf, "x-ticvai-reads"),
         "submitForm does not read the published form and its resign rule under the root grant, filtered to the "
         "caller's paths, then return to the caller's grant (CR-496)")

    # BR-CONFIG-DIFF-SHAPE (CR-500)
    cd = schemas("contracts/satellite/white-label.yaml").get("ConfigDiff") or {}
    area = ((((cd.get("properties") or {}).get("changes") or {}).get("items") or {}).get("properties") or {}).get("area") or {}
    need("BR-CONFIG-DIFF-SHAPE", "one of brand, appIcons, bookingFlow, bookingFlows, theme, fonts, footer, "
         "notificationBranding, enabledPaymentMethods, accessibility, header, navigation, homepage, modules, features, "
         "languages; entries are ordered by area in this order" in words(area.get("description")),
         "ConfigDiff's area does not name the snapshot's top-level parts, in their order (CR-500)")
    dcv = op("diffConfigVersion")[3]
    dvd = words(dcv.get("description"))
    need("BR-CONFIG-DIFF-SHAPE", "404" in (dcv.get("responses") or {}) and "compact JSON text" in dvd
         and "`features[guestCheckout].isEnabled`" in dvd and "A property that is null counts as absent" in dvd
         and "exactly where the publish''s `pendingBuildTimeChanges` says so".replace("''", "'") in dvd,
         "diffConfigVersion does not state CR-500's one rule for areas, paths, values, order, changeScope and the 404")

    # BR-PERFORMANCE-INTO-TICKETS (CR-503)
    w5 = screen(p01, "WEB-005")
    dov = next((c for c in components(w5) if (c or {}).get("label") == "Date of visit"), {})
    w5api = {a.get("operationId"): a for a in w5.get("apis") or []}
    need("BR-PERFORMANCE-INTO-TICKETS", (params(w5).get("performanceId") or {}).get("optional") is True
         and (w5api.get("getPerformance") or {}).get("trigger") == "onLoad" and dov.get("operation") == "getPerformance"
         and any(t.get("to") == "WEB-006" and t.get("carries") == ["eventId"] and "no longer available" in str(t.get("trigger"))
                 for t in (w5.get("navigation") or {}).get("transitions") or []),
         "WEB-005 does not take performanceId from WEB-006, read getPerformance and show the Date of visit (CR-503)")

    # BR-PREVIEW-ADDRESS (CR-507)
    cpv, gps = op("createPreview")[3], op("getPlatformSubdomain")[3]
    need("BR-PREVIEW-ADDRESS", vias(cpv) == {("platform-ops#tenantDomainRecords", "in-process"),
                                             ("subscription#cellRecords", "in-process")}
         and vias(cpv) <= vias(gps),
         "createPreview does not take the address through getPlatformSubdomain's two in-process reads (CR-507)")
    cpd = words(cpv.get("description"))
    need("BR-PREVIEW-ADDRESS", "`IKeyedState`" in cpd and "`preview:{previewId}`" in cpd and "never a custom domain" in cpd
         and "One reader" in words(gps.get("description")) and "IKeyedState" in words(op("getPreview")[3].get("description")),
         "createPreview, getPreview and getPlatformSubdomain do not state the one reader and the IKeyedState entry (CR-507)")
    prq = load("events/preview-requested.yaml")
    need("BR-PREVIEW-ADDRESS", "IKeyedState" in " ".join(str((c or {}).get("purpose")) for c in prq.get("consumers") or []),
         "preview.requested's renderer does not read and write the entry through IKeyedState (CR-507)")

    # BR-SESSION-BATCH-RECORD (CR-511)
    rse = op("recordStorefrontSessionEvents")[3]
    rsd = words(rse.get("description"))
    need("BR-SESSION-BATCH-RECORD", ("tenancy#activeVenues", "in-process") in vias(rse)
         and "platform.idempotency_record" in tables(rse, "x-ticvai-writes")
         and "`IIdempotencyStore`" in rsd and "`aggregate_id` is `batchId` and its sequence is 1" in rsd
         and "never refused" in rsd,
         "recordStorefrontSessionEvents does not record the batch in the kernel's idempotency record, key the outbox row by "
         "batchId and scope by an active venue (CR-511)")

    # BR-GUEST-DOCUMENT-UPLOAD (CR-521)
    mk = schemas("contracts/satellite/marketing-crm.yaml")
    cgu, ugd = op("createGuestDocumentUpload")[3], op("uploadGuestDocument")[3]
    need("BR-GUEST-DOCUMENT-UPLOAD", cgu.get("x-ticvai-permission") == "GUEST_VIEW_PII"
         and cgu.get("x-ticvai-scope-level") == "venue" and set(cgu.get("x-ticvai-audience") or []) == {"staff", "guest"}
         and "marketing.guest_document_upload" in tables(cgu, "x-ticvai-writes")
         and ptypes(cgu, "400") == {"media-type-not-permitted", "media-too-large"},
         "createGuestDocumentUpload does not issue the key as uploadGuestDocument's twin (CR-521)")
    need("BR-GUEST-DOCUMENT-UPLOAD", "guest-document-upload-invalid" in ptypes(ugd, "422")
         and "marketing.guest_document_upload" in tables(ugd, "x-ticvai-writes"),
         "uploadGuestDocument does not check the issued key (422 guest-document-upload-invalid) and attach it (CR-521)")
    need("BR-GUEST-DOCUMENT-UPLOAD", (mk.get("GuestDocument") or {}).get("x-ticvai-rls") == "grant-holder-write"
         and (mk.get("GuestDocumentUpload") or {}).get("x-ticvai-persistence") == "marketing.guest_document_upload"
         and (mk.get("GuestDocumentUpload") or {}).get("x-ticvai-rls") == "grant-holder-write"
         and "createGuestDocumentUpload" in words((((mk.get("GuestDocument") or {}).get("properties") or {})
                                                   .get("storageRef") or {}).get("description")),
         "marketing.guest_document has not the grant-holder subject policy, or the upload table is missing (CR-521)")

    # BR-KIOSK-CHECK-ROWS (CR-528)
    gkd = words(op("getKioskConfigValidation")[3].get("description"))
    need("BR-KIOSK-CHECK-ROWS", "containing the kiosk''s venue or empty".replace("''", "'") in gkd
         and "no scope path is read" in gkd and "Only findings are returned" in gkd
         and "a row of another venue counts as not held" in gkd,
         "getKioskConfigValidation does not read the venue's and the tenant's rows with today's fields (CR-528)")
    pmr = words(query("contracts/satellite/payments.yaml", "paymentMethodRecords").get("rule"))
    mar = words(query("contracts/satellite/assets.yaml", "mediaAssetRecords").get("rule"))
    need("BR-KIOSK-CHECK-ROWS", "scope_path that is the venue's or an ancestor" not in pmr and "no scope path is read" in pmr
         and "VenueId on its MediaAssetRecord" in mar,
         "paymentMethodRecords still reads scope paths, or mediaAssetRecords' record carries no VenueId (CR-528)")

    # BR-SCHEDULED-PUBLISH-RUN (CR-501, with r13's CR-154 rule kept: activated_at on every activation, newer publish wins)
    wl = load("contracts/satellite/white-label.yaml")
    spj = words(((wl.get("x-ticvai-jobs") or {}).get("scheduledPublish") or {}).get("for"))
    need("BR-SCHEDULED-PUBLISH-RUN", all(f in spj for f in ("FOR UPDATE SKIP LOCKED", "review_status notRequired or approved",
                                                             "the latest scheduledFor (on a tie, the highest version number)",
                                                             "Superseded by version N, which was due at the same time.",
                                                             "superseded: version N was published after this one was scheduled")),
         "white-label#scheduledPublish does not run as CR-501 decided on top of CR-154's rule")
    agr = load("events/approval-granted.yaml")
    agp = words(" ".join(str((c or {}).get("purpose")) for c in agr.get("consumers") or [] if (c or {}).get("context") == "white-label"))
    need("BR-SCHEDULED-PUBLISH-RUN", "is left waiting" in agp and "makes it current when it falls due" in agp,
         "white-label's approval.granted consumer does not leave a version scheduled for later waiting (CR-501)")

    # BR-PUBLISH-REVIEW-DEFAULT (CR-520, the reads on r13's routes: Tenancy's queries in process from operations)
    spr = op("setPublishReviewPolicy")[3]
    spd = words(spr.get("description"))
    need("BR-PUBLISH-REVIEW-DEFAULT", ("approvals#ruleRecords", "in-process") in vias(spr)
         and ("identity#rolePermissionRecords", "service") in vias(spr)
         and "review-route-unavailable" in ptypes(spr, "409")
         and "`approverScopeLevel` `tenant`, `levels` 1" in spd and "approvals never lets a requester approve" in spd
         and "setPublishReviewPolicy" in ((xdr.get("XDR-111") or {}).get("operations") or [])
         and "service" in (query("contracts/spine/identity.yaml", "rolePermissionRecords").get("served") or []),
         "setPublishReviewPolicy does not create CR-520's default rule, or reads it on the wrong route (CR-520)")

    # BR-WEB022-STATUS-PILL (CR-534)
    w22 = screen(p01, "WEB-022")
    yp = next((c for c in components(w22) if (c or {}).get("label") == "Your plan"), {})
    ypn = words(yp.get("notes"))
    need("BR-WEB022-STATUS-PILL", all(f in ypn for f in ("`active` Active (`--status-active`)", "`frozen` Paused",
                                                         "`suspended` Suspended", "`expired` Expired",
                                                         "`cancelled` Cancelled", "Never a raw value or an empty pill"))
         and {"LO-CR534-001", "LO-CR534-002"} <= lo,
         "WEB-022's Your plan pill does not map every GuestMembership.status, or the redraw and Passholders are not on "
         "the left-out list (CR-534)")


R13_W4_RULES = ["BR-DELEGATION-INPUT", "BR-RULE-CODE-KEY", "BR-STEP-UP-CHECK", "BR-MATRIX-LIST-REACH",
                "BR-PRIVACY-VENUE", "BR-SESSION-GRANT", "BR-BREACH-CORPUS", "BR-MFA-VALUES",
                "BR-ROLE-PERMISSIONS-HOME", "BR-PUBLIC-API-CALLER"]


def lane_w4_rules_r13(need, op):
    """r13 second CR round, lane w4: identity, approvals, public API (ADAM CR-497, CR-498, CR-509, CR-512, CR-513,
    CR-514, CR-522, CR-525, CR-526, CR-536, decided 3 November 2026; CHG-CR497-001 ...). Each rule fails on the r13
    candidate (f599f2c6) and passes once the posted decision is in."""
    def words(x):
        return " ".join(str(x or "").split()).replace("**", "")

    def vias(o_):
        return {(str((v or {}).get("query")), str((v or {}).get("route")))
                for v in o_.get("x-ticvai-read-via") or [] if isinstance(v, dict)}

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def tables(o_, key):
        return {str((t or {}).get("table") if isinstance(t, dict) else t) for t in o_.get(key) or []}

    def schemas(rel):
        return (load(rel).get("components") or {}).get("schemas") or {}

    def sprops(rel, name):
        return (schemas(rel).get(name) or {}).get("properties") or {}

    def params(o_):
        return {str((p or {}).get("$ref", "")).rsplit("/", 1)[-1] for p in o_.get("parameters") or []}

    appr, ident = "contracts/spine/approvals.yaml", "contracts/spine/identity.yaml"
    iq = load(ident).get("x-ticvai-queries") or {}

    # BR-DELEGATION-INPUT (ADAM CR-497)
    ard = op("approveRoleAuthorityDelegation")[3]
    for sch in ("RolesAuthorityDelegationApprovalLimitsInput", "RolesAuthorityDelegationApprovalLimitsView"):
        pr = sprops(appr, sch)
        for f in ("delegator", "delegate", "requiredRole", "venue"):
            need("BR-DELEGATION-INPUT", (pr.get(f) or {}).get("format") == "uuid",
                 f"{sch}.{f} is not a uuid (CR-497)")
        need("BR-DELEGATION-INPUT", "ApprovalKind" in str(pr.get("requestKind")),
             f"{sch}.requestKind is not an ApprovalKind (CR-497)")
    need("BR-DELEGATION-INPUT", "validation" in ptypes(ard, "400"),
         "approveRoleAuthorityDelegation's 400 does not answer the shared validation problem (CR-497)")
    need("BR-DELEGATION-INPUT", "always the path of the venue the caller acts at" in words(ard.get("description"))
         and "platform.venue_settings" in tables(ard, "x-ticvai-reads"),
         "approveRoleAuthorityDelegation does not store the caller's venue path or read the venue's money (CR-497)")

    # BR-RULE-CODE-KEY (ADAM CR-498)
    code = words((sprops(appr, "ApprovalRule").get("code") or {}).get("description"))
    need("BR-RULE-CODE-KEY", "rule_matrix_id_matrix_version_code_uniq" in code
         and "unique index on (`matrix_id`, `code`)" not in code,
         "ApprovalRule.code still names the old key (matrix_id, code) rather than the versioned one (CR-498)")
    v119 = (ROOT / "backend" / "tenant" / "V0119__names_after_r1_20261029.sql")
    need("BR-RULE-CODE-KEY", v119.exists() and "DROP INDEX approvals.rule_matrix_id_code_uniq"
         in v119.read_text(encoding="utf-8"),
         "the names migration no longer drops approvals.rule_matrix_id_code_uniq (CR-498)")

    # BR-STEP-UP-CHECK (ADAM CR-509)
    cq = iq.get("consumeMfaStepUp") or {}
    need("BR-STEP-UP-CHECK", cq.get("table") == "identity.mfa_challenge" and "in-process" in (cq.get("served") or [])
         and "consumed" in str(cq.get("returns")) and "expired" in str(cq.get("returns")),
         "identity declares no in-process consumeMfaStepUp over identity.mfa_challenge answering consumed, missing or "
         "expired (CR-509)")
    for oid in ("approveMatrixMultiLevel", "approveRoleAuthorityDelegation"):
        need("BR-STEP-UP-CHECK", ("identity#consumeMfaStepUp", "in-process") in vias(op(oid)[3]),
             f"{oid} does not ask identity#consumeMfaStepUp in process (CR-509, CR-497)")
    amm = op("approveMatrixMultiLevel")[3]
    mi = sprops(appr, "ApprovalMatrixMultiLevelApprovalConfigurationInput")
    need("BR-STEP-UP-CHECK", (mi.get("requiredApproverRole") or {}).get("format") == "uuid"
         and (mi.get("venue") or {}).get("format") == "uuid",
         "approveMatrixMultiLevel's requiredApproverRole or venue is not a uuid (CR-509)")
    need("BR-STEP-UP-CHECK", "copied into it unchanged" in words(amm.get("description"))
         and "keep their stored values" in words(amm.get("description")),
         "approveMatrixMultiLevel does not say how the other rules and the unmapped fields carry into the new version "
         "(CR-509)")

    # BR-MATRIX-LIST-REACH (ADAM CR-526)
    lam = words(op("listApprovalMatrices")[3].get("description"))
    need("BR-MATRIX-LIST-REACH", "deepest listed entry" in lam and "one copy of each matrix id" in lam,
         "listApprovalMatrices does not say which nodes are 'here' for a caller with several, or how they merge (CR-526)")

    # BR-PRIVACY-VENUE (ADAM CR-512)
    for oid in ("exportSubjectData", "deleteGuestAccount"):
        o_ = op(oid)[3]
        need("BR-PRIVACY-VENUE", "GuestVenue" in params(o_) and "venue-required" in ptypes(o_, "400")
             and {("tenancy#scopeRecords", "in-process"), ("tenancy#regionSettingsRecords", "in-process")} <= vias(o_),
             f"{oid} raises its request at no venue: no X-Venue-Id, 400 venue-required or the venue reads (CR-512)")
    esd = op("exportSubjectData")[3]
    need("BR-PRIVACY-VENUE", "identity.subject_data_export" in tables(esd, "x-ticvai-reads")
         and "One open export per guest" in words(esd.get("description")),
         "exportSubjectData does not answer a second export with the open one (CR-512)")
    job = words(((load(ident).get("x-ticvai-jobs") or {}).get("subjectExport") or {}).get("for"))
    need("BR-PRIVACY-VENUE", "72 hours" in job and "storage seam" in job,
         "the export job's declaration does not carry its rules (CR-512)")

    # BR-SESSION-GRANT (ADAM CR-513)
    sg = schemas(ident).get("SessionGrant") or {}
    gid = (sg.get("properties") or {}).get("grantId") or {}
    need("BR-SESSION-GRANT", sg.get("x-ticvai-persistence") == "identity.session"
         and gid.get("x-ticvai-references") == "identity.delegated_access",
         "identity.session has no grant_id referencing identity.delegated_access (CR-513)")
    need("BR-SESSION-GRANT", "does not resolve grants again" in words(op("getCurrentSession")[3].get("description")),
         "getCurrentSession does not answer from the session registry filled at sign-in (CR-513)")
    for oid in ("login", "selectRole"):
        need("BR-SESSION-GRANT", "identity.session" in tables(op(oid)[3], "x-ticvai-writes"),
             f"{oid} does not write the session's grant_id (CR-513)")

    # BR-BREACH-CORPUS (ADAM CR-514)
    rbc = words((sprops(ident, "PasswordPolicy").get("requireBreachCheck") or {}).get("description"))
    for w in ("Pwned Passwords", "Identity:BreachCorpusPath", "readiness check", "SUFFIX:COUNT"):
        need("BR-BREACH-CORPUS", w in rbc, f"PasswordPolicy.requireBreachCheck does not state {w!r} (CR-514)")
    for oid in ("createPrincipal", "resetPrincipalCredential"):
        need("BR-BREACH-CORPUS", "policy-not-met" in ptypes(op(oid)[3], "422"),
             f"{oid} does not answer 422 policy-not-met for a breached password (CR-514)")

    # BR-MFA-VALUES (ADAM CR-522)
    ev = ROOT / "events" / "identity-mfaCodeIssued.yaml"
    need("BR-MFA-VALUES", ev.exists(), "events/identity-mfaCodeIssued.yaml does not exist (CR-522)")
    for oid in ("enrolMfaMethod", "createMfaChallenge"):
        need("BR-MFA-VALUES", "identity.mfaCodeIssued" in (op(oid)[3].get("x-ticvai-emits") or []),
             f"{oid} does not emit identity.mfaCodeIssued (CR-522)")
    me = sprops(ident, "MfaEnrolment")
    need("BR-MFA-VALUES", "period=30" in words((me.get("qrCodeUri") or {}).get("description"))
         and "pattern" in ((me.get("recoveryCodes") or {}).get("items") or {}),
         "MfaEnrolment does not state the otpauth URI or the recovery code format (CR-522)")
    need("BR-MFA-VALUES", "RFC 6238" in words(op("verifyMfaChallenge")[3].get("description"))
         and "RFC 6238" in words(op("verifyMfaEnrolment")[3].get("description")),
         "the MFA verifications do not state the RFC 6238 values (CR-522)")
    need("BR-MFA-VALUES", ptypes(op("removeMfaMethod")[3], "409") == {"last-required-mfa-method"},
         "removeMfaMethod's 409 is not last-required-mfa-method (CR-522)")
    mj = (load("contracts/satellite/marketing-crm.yaml").get("x-ticvai-jobs") or {}).get("mfaCodeSender") or {}
    need("BR-MFA-VALUES", "identity.mfaCodeIssued" in (mj.get("consumes") or []),
         "Marketing declares no consumer of identity.mfaCodeIssued (CR-522)")

    # BR-ROLE-PERMISSIONS-HOME (ADAM CR-525)
    f_, _, _, srp, _ = op("setRolePermissions")
    need("BR-ROLE-PERMISSIONS-HOME", f_ is not None and f_.name == "identity.yaml",
         "setRolePermissions is not built in the Identity module (CR-525)")
    need("BR-ROLE-PERMISSIONS-HOME", {"identity.role", "identity.role_permission", "identity.session",
                                      "identity.refresh_token"} <= tables(srp, "x-ticvai-writes")
         and "identity.delegated_access" in tables(srp, "x-ticvai-reads")
         and not any(q.startswith("identity#") for q, _ in vias(srp)),
         "setRolePermissions does not declare its own tables, or still asks Identity's queries (CR-525)")
    need("BR-ROLE-PERMISSIONS-HOME", "validation" in ptypes(srp, "400"),
         "setRolePermissions does not answer 400 validation for an inheritsFromRoleId it refuses (CR-525)")

    # BR-PUBLIC-API-CALLER (ADAM CR-536)
    pa = load("contracts/satellite/public-api.yaml")
    need("BR-PUBLIC-API-CALLER", "never by its permissions" in words((pa.get("info") or {}).get("description")),
         "public-api does not say how it tells callers apart (CR-536)")
    for oid, want in (("listDeveloperMembers", {"control.developer_account", "control.developer_member"}),
                      ("listIntegrationListings", {"control.integration_listing", "control.developer_member"}),
                      ("listProductionAccessRequests", {"control.production_access_request",
                                                        "control.developer_member"}),
                      ("requestProductionAccess", {"control.api_client", "control.integration_listing",
                                                   "control.developer_account", "control.developer_member",
                                                   "control.production_access_request"})):
        need("BR-PUBLIC-API-CALLER", tables(op(oid)[3], "x-ticvai-reads") == want,
             f"{oid} does not declare exactly the reads CR-536 names")
    need("BR-PUBLIC-API-CALLER", tables(op("requestProductionAccess")[3], "x-ticvai-writes")
         == {"control.production_access_request"},
         "requestProductionAccess does not declare its one write (CR-536)")
    need("BR-PUBLIC-API-CALLER", "partner" in (op("listDeveloperMembers")[3].get("x-ticvai-audience") or []),
         "listDeveloperMembers is still for staff only (CR-536)")
    need("BR-PUBLIC-API-CALLER", "email" in (sprops(ident, "PrincipalVerifiedEmail")),
         "identity.principal has no verified email (CR-536)")


R13_W1_RULES = ["BR-GROUP-PACKAGE-SOURCE", "BR-PRODUCT-BADGE-RATING", "BR-SHOP-DROP-RULES", "BR-CATEGORY-TREE-PASSES",
                "BR-WAITING-ROOM-COOKIE", "BR-GUIDED-ANSWER-FILTER", "BR-SEARCH-CATALOGUE-SOURCES",
                "BR-SIMULATION-CHANNEL-MAP", "BR-CHANNEL-RETRY-READINGS", "BR-CHANGE-IMPACT-REPRICE",
                "BR-CHANNEL-TEST-NOT-SUPPORTED", "BR-IMPORT-STAGED-ROWS", "BR-GUEST-MEMBERSHIP-FIELDS",
                "BR-BULK-PRICE-SKIPS", "BR-CLONE-PRODUCT-RULES"]


def lane_w1_rules_r13(need, op):
    """r13 second CR round, lane w1 (ADAM CR-499 to CR-545, decided by Chinmay on 3 November 2026: "Close the CRs and
    respond to devs", "get the NEw CRs in the r13"). Each rule fails on the r13 candidate before the lane (f599f2c6)."""
    def words(x):
        return " ".join(str(x or "").split())

    def schemas(rel):
        return (load(rel).get("components") or {}).get("schemas") or {}

    def vias(o_):
        return {(str((v or {}).get("query")), str((v or {}).get("route"))) for v in o_.get("x-ticvai-read-via") or []
                if isinstance(v, dict)}

    def tables(o_, key):
        return {str(x.get("table") if isinstance(x, dict) else x) for x in o_.get(key) or []}

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def param(o_, name):
        return next((x for x in o_.get("parameters") or [] if isinstance(x, dict) and x.get("name") == name), {})

    def body(o_):
        return ((((o_.get("requestBody") or {}).get("content") or {}).get("application/json") or {}).get("schema")
                or {})

    cat = schemas("contracts/spine/catalogue.yaml")
    chan = "#/components/schemas/Channel"

    # BR-GROUP-PACKAGE-SOURCE (CR-499)
    sgp, lgp = op("setGroupPackageDefinition")[3], op("listGroupPackages")[3]
    sgv = next((v for v in sgp.get("x-ticvai-read-via") or [] if (v or {}).get("query") == "tenancy#venueSettingsRecords"),
               {})
    need("BR-GROUP-PACKAGE-SOURCE", "the read is not asked until it does" in words(sgv.get("for"))
         and "answers `name` and `unitPrice` as null" in words(sgp.get("description")),
         "setGroupPackageDefinition asks the venue settings, or does not answer name and unitPrice null (CR-499)")
    gpp = (cat.get("GroupPackageDefinition") or {}).get("properties") or {}
    need("BR-GROUP-PACKAGE-SOURCE", (gpp.get("nameLocalised") or {}).get("readOnly") is True
         and (gpp.get("nameLocalised") or {}).get("x-ticvai-persisted") is False
         and "fromPrice" in words((gpp.get("unitPrice") or {}).get("description")),
         "GroupPackageDefinition has no read-only nameLocalised, or unitPrice is not the product's fromPrice (CR-499)")
    need("BR-GROUP-PACKAGE-SOURCE", ((param(lgp, "channel").get("schema") or {}).get("$ref")) == chan
         and "the same price-list function `listProductVariants` uses" in words(lgp.get("description")),
         "listGroupPackages takes no channel, or does not price a package as listProducts does (CR-499)")

    # BR-PRODUCT-BADGE-RATING (CR-504)
    pp = (cat.get("Product") or {}).get("properties") or {}
    hb, rt = pp.get("highlightBadge") or {}, pp.get("rating") or {}
    need("BR-PRODUCT-BADGE-RATING", hb.get("nullable") is True
         and (hb.get("additionalProperties") or {}).get("maxLength") == 20
         and rt.get("readOnly") is True and rt.get("x-ticvai-persisted") is False and rt.get("nullable") is True
         and {"average", "count"} <= set((rt.get("properties") or {})),
         "Product has no highlightBadge (per language, at most 20) or no readOnly, unstored rating {average, count} "
         "(CR-504)")
    for req in ("CreateProductRequest", "UpdateProductRequest"):
        need("BR-PRODUCT-BADGE-RATING", "highlightBadge" in ((cat.get(req) or {}).get("properties") or {}),
             f"{req} does not take highlightBadge (CR-504)")
    p01 = load("screens/P01-guest-web-storefront.yaml").get("screens") or []
    w5 = next((x for x in p01 if (x or {}).get("id") == "WEB-005"), {})
    cards = [c for r in ((w5.get("layout") or {}).get("regions") or []) for c in (r or {}).get("components") or []
             if (c or {}).get("operation") == "listProducts"
             and {"Product.highlightBadge", "Product.rating"} <= set((c or {}).get("columns") or [])]
    need("BR-PRODUCT-BADGE-RATING", bool(cards), "WEB-005's cards do not bind Product.highlightBadge and Product.rating "
         "on listProducts (CR-504)")

    # BR-SHOP-DROP-RULES (CR-508)
    csd = op("createShopAndDrop")[3]
    need("BR-SHOP-DROP-RULES", ptypes(csd, "409") == {"shop-and-drop-already-dropped", "shop-and-drop-item-not-droppable",
                                                      "shop-and-drop-collection-point-closed"}
         and "line-ids-required" in ptypes(csd, "400"),
         "createShopAndDrop's 409 does not declare one problem type per reason, or its 400 has no line-ids-required "
         "(CR-508)")
    need("BR-SHOP-DROP-RULES", any(q == "orders#salesOrderRecords" for q, _ in vias(csd)),
         "createShopAndDrop does not declare its read of the order (orders#salesOrderRecords) (CR-508)")
    cdd = words(csd.get("description"))
    for frag in ("first 22 characters", "`-SD-`", "transaction-scoped lock on that prefix", "Numbering is per prefix",
                 "never the line's own venue", "of kind `collectionPoint`", "the next local midnight",
                 "A null `opensAt` or `closesAt` sets no limit", "collection point's serving outlets"):
        need("BR-SHOP-DROP-RULES", frag in cdd, f"createShopAndDrop does not say {frag!r} (CR-508)")

    # BR-CATEGORY-TREE-PASSES (CR-523)
    lpc = words(op("listProductCategories")[3].get("description"))
    for frag in ("Pass 1, for a guest or visitor only:", "Pass 2, for every caller:", "nearest kept ancestor",
                 "A node never appears under a node it is not filed beneath"):
        need("BR-CATEGORY-TREE-PASSES", frag in lpc, f"listProductCategories does not say {frag!r} (CR-523)")

    # BR-WAITING-ROOM-COOKIE (CR-524)
    gwr = op("getWaitingRoomPosition")[3]
    hdr = ((((gwr.get("responses") or {}).get("200") or {}).get("headers") or {}).get("Set-Cookie") or {})
    gwd = words(gwr.get("description"))
    need("BR-WAITING-ROOM-COOKIE", bool(hdr) and "The API itself sends the cookie" in gwd and "#29033" in gwd
         and "never caches the admitted answer" in gwd,
         "getWaitingRoomPosition does not send the admission cookie itself, or is not built on #29033 (CR-524)")

    # BR-GUIDED-ANSWER-FILTER (CR-532)
    wl = schemas("contracts/satellite/white-label.yaml")
    flt = {}
    for nm, sc in wl.items():
        t = str(sc)
        if "requiresSwimmer" in t and "holdsCertification" in t:
            flt = sc
            break
    ft = words(flt)
    for frag in ("kind `swim`", "`swimAbility` `confident`", "overlap; an empty bound on either side is open",
                 "any category below it", "true or no flag keeps products needing this code or no certification"):
        need("BR-GUIDED-ANSWER-FILTER", frag in ft, f"GuidedChoice answer.filter does not say {frag!r} (CR-532)")
    need("BR-GUIDED-ANSWER-FILTER", ("marketing-crm#consentQuestionRecords", "in-process") in vias(op("previewGuidedChoice")[3])
         and "One guided-answer filter, written once as shared code" in words(op("previewGuidedChoice")[3]
                                                                              .get("description")),
         "previewGuidedChoice does not call the one shared filter with the consent-question read (CR-532)")
    for oid in ("listProducts", "searchCatalogue"):
        o_ = op(oid)[3]
        need("BR-GUIDED-ANSWER-FILTER", ("marketing-crm#consentQuestionRecords", "service") in vias(o_)
             and "One shared guided-answer filter" in words(param(o_, "guidedAnswerIds").get("description")),
             f"{oid} does not declare the consent-question read or state the shared filter's rules (CR-532)")

    # BR-SEARCH-CATALOGUE-SOURCES (CR-533)
    sc_ = op("searchCatalogue")[3]
    item = ((((((sc_.get("responses") or {}).get("200") or {}).get("content") or {}).get("application/json") or {})
             .get("schema") or {}).get("items") or {}).get("properties") or {}
    need("BR-SEARCH-CATALOGUE-SOURCES", {"nameLocalised", "summaryLocalised"} <= set(item)
         and ((param(sc_, "channel").get("schema") or {}).get("$ref")) == chan
         and ("white-label#tenantLanguageRecords", "service") in vias(sc_)
         and {"catalogue.price_list", "catalogue.price"} <= tables(sc_, "x-ticvai-reads")
         and "requested language" not in words(param(sc_, "q").get("description")),
         "searchCatalogue does not answer the localised maps, take channel, read showInfoOnly from the published "
         "configuration or declare fromPrice's reads (CR-533)")
    need("BR-SEARCH-CATALOGUE-SOURCES", ("white-label#tenantLanguageRecords", "service") in vias(op("listProducts")[3]),
         "listProducts does not declare the showInfoOnly read (CR-533)")

    # BR-SIMULATION-CHANNEL-MAP (CR-537)
    sim = op("simulatePriceBreakdownCalculation")[3]
    sd = words(sim.get("description"))
    vw = ((cat.get("PriceBreakdownCalculationSimulationExplainabilityView") or {}).get("properties") or {})
    fp = ((((vw.get("channelComparison") or {}).get("items") or {}).get("properties") or {}).get("finalPayable") or {})
    need("BR-SIMULATION-CHANNEL-MAP", "`guestWeb` becomes `web`" in sd and "`partner` becomes `b2b`" in sd
         and "`api` and `backOffice` have no catalogue channel" in sd and fp.get("nullable") is True,
         "the simulation does not map SalesChannel to catalogue Channel, or a comparison entry cannot omit "
         "finalPayable (CR-537)")

    # BR-CHANNEL-RETRY-READINGS (CR-538)
    rci = op("retryChannelIncident")[3]
    need("BR-CHANNEL-RETRY-READINGS", "`retrying`" in words(((rci.get("responses") or {}).get("409") or {})
                                                             .get("description")),
         "retryChannelIncident does not refuse an incident already retrying (CR-538)")
    ev = load("events/catalogue-channelIncidentRetryRequested.yaml")
    pur = words(" ".join(str((c or {}).get("purpose") or "") for c in ev.get("consumers") or []))
    for frag in ("[removed]", "2,000 characters", "13 to 19 digits", "action retry", "entity_type channelIncident",
                 "no channel_connection_id ends the attempt as connectorNotAvailable", "rebuilds the call from the incident",
                 "A connector may scrub more, never less"):
        need("BR-CHANNEL-RETRY-READINGS", frag in pur,
             f"catalogue.channelIncidentRetryRequested's job does not say {frag!r} (CR-538)")

    # BR-CHANGE-IMPACT-REPRICE (CR-539)
    lci = op("listPricingChangeImpact")[3]
    ld = words(lci.get("description"))
    for frag in ("`proposed_amount` / `current_amount`", "the most specific wins: product, then rate, then priceList",
                 "the mean of their ratios", "half away from zero", "trade in more than one currency"):
        need("BR-CHANGE-IMPACT-REPRICE", frag in ld, f"listPricingChangeImpact does not say {frag!r} (CR-539)")
    iv = None
    for nm, sc in cat.items():
        if {"projectedRevenue", "revenueImpact", "currentRevenue"} <= set((sc or {}).get("properties") or {}):
            iv = sc
            break
    ivp = (iv or {}).get("properties") or {}
    need("BR-CHANGE-IMPACT-REPRICE", all((ivp.get(k) or {}).get("nullable") is True
                                         for k in ("currentRevenue", "projectedRevenue", "revenueImpact")),
         "currentRevenue, projectedRevenue and revenueImpact are not nullable (CR-539)")

    # BR-CHANNEL-TEST-NOT-SUPPORTED (CR-540)
    tcd = words(op("testChannelConnection")[3].get("description"))
    need("BR-CHANNEL-TEST-NOT-SUPPORTED", "A named test that does not apply is recorded as `notSupported`" in tcd
         and "a call where nothing ran leaves `connectionStatus` unchanged" in tcd
         and "a named order test that does not apply is `notSupported`, not `422`" in tcd,
         "testChannelConnection does not record a named test that does not apply as notSupported (CR-540)")

    # BR-IMPORT-STAGED-ROWS (CR-542)
    row = cat.get("CatalogueImportJobRow") or {}
    rp = row.get("properties") or {}
    need("BR-IMPORT-STAGED-ROWS", row.get("x-ticvai-persistence") == "catalogue.import_job_row"
         and ["importJobId", "rowNumber"] in [list(x) for x in row.get("x-ticvai-unique-together") or []]
         and {"importJobId", "scopePath", "rowNumber", "action", "targetProductId", "payload", "isExcluded", "outcome",
              "failure", "productId"} <= set(rp)
         and (rp.get("outcome") or {}).get("enum") == ["pending", "applied", "failed", "excluded"],
         "catalogue.import_job_row does not stage the parse as CR-542 states")
    jp = (cat.get("CatalogueImportJob") or {}).get("properties") or {}
    need("BR-IMPORT-STAGED-ROWS", all((jp.get(k) or {}).get("readOnly") is True for k in ("mode", "appliedCount",
                                                                                          "failedCount")),
         "CatalogueImportJob does not store mode, appliedCount and failedCount, read-only (CR-542)")
    cci = op("commitCatalogueImport")[3]
    need("BR-IMPORT-STAGED-ROWS", {"catalogue-import-wrong-kind", "catalogue-import-not-ready",
                                   "catalogue-import-already-committed", "catalogue-import-found-nothing",
                                   "category-has-live-orders"} <= ptypes(cci, "409")
         and "catalogue.import_job_row" in tables(op("importProductCatalogue")[3], "x-ticvai-writes")
         and "The source file is never read again" in words(cci.get("description")),
         "commitCatalogueImport does not refuse as CR-542 states, or the parse does not write the staged rows")

    # BR-GUEST-MEMBERSHIP-FIELDS (CR-543)
    ent = (schemas("contracts/spine/access.yaml").get("Entitlement") or {}).get("properties") or {}
    need("BR-GUEST-MEMBERSHIP-FIELDS", {"frozenFrom", "frozenUntil"} <= set(ent),
         "access.entitlement does not store frozen_from and frozen_until (CR-543)")
    gmm = op("getMyMemberships")[3]
    need("BR-GUEST-MEMBERSHIP-FIELDS", not any(q.startswith("marketing") for q, _ in vias(gmm))
         and {"catalogue.plan_benefit", "catalogue.membership_benefit"} <= tables(gmm, "x-ticvai-reads")
         and {"catalogue.plan_benefit", "catalogue.membership_benefit"} <= tables(op("listGuestMemberships")[3],
                                                                                  "x-ticvai-reads"),
         "getMyMemberships still reads Marketing, or the two membership reads do not declare the benefit tables (CR-543)")
    gm = words(cat.get("GuestMembership"))
    for frag in ("`suspended_reason` set becomes `suspended`", "`frozen_until` is null or on or after today",
                 "ordered by `plan_benefit.priority` then `code`", "the day after this term's `validTo`"):
        need("BR-GUEST-MEMBERSHIP-FIELDS", frag in gm, f"GuestMembership does not say {frag!r} (CR-543)")

    # BR-BULK-PRICE-SKIPS (CR-544)
    bcp = op("bulkChangePrices")[3]
    sel = ((body(bcp).get("properties") or {}).get("selection") or {}).get("properties") or {}
    bpr = cat.get("BulkPriceResult") or {}
    sk = ((((bpr.get("properties") or {}).get("skipped") or {}).get("items") or {}).get("properties") or {})
    need("BR-BULK-PRICE-SKIPS", chan in str(sel.get("channel")) and "ProductKind" in str(sel.get("productKind"))
         and "escalates" in (bpr.get("required") or [])
         and (sk.get("reason") or {}).get("enum") == ["partnerNetRate", "fixedPriceBundle", "openChangeRequest"]
         and "price-escalation-required" in ptypes(bcp, "403") and "validation" in ptypes(bcp, "400")
         and "catalogue.package_pricing" in tables(bcp, "x-ticvai-reads"),
         "bulkChangePrices does not select, skip, escalate and refuse as CR-544 states")

    # BR-CLONE-PRODUCT-RULES (CR-545)
    clp = op("cloneProduct")[3]
    cb = body(clp).get("properties") or {}
    need("BR-CLONE-PRODUCT-RULES", (cb.get("code") or {}).get("maxLength") == 64
         and (cb.get("code") or {}).get("pattern") == "^[A-Za-z0-9_-]+$"
         and (cb.get("name") or {}).get("maxLength") == 200 and "validation" in ptypes(clp, "400")
         and "What a clone copies:" in words(clp.get("description"))
         and "`nameLocalised` null" in words(clp.get("description")),
         "cloneProduct does not take createProduct's code rules, refuse with 400, or state what a clone copies (CR-545)")


R14_B_RULES = ["BR-CREDENTIAL-POLICY-PROBLEM", "BR-MFA-PRIMARY", "BR-ENABLEMENT-SERVICE-CALLER", "BR-CELL-CALL-CLIENT",
               "BR-CAPACITY-PACK-UNIT", "BR-CURRENT-PLAN-READER", "BR-PREVIEW-RULES"]


def lane_b_rules_r14(need, op):
    """r14 catch-up, lane b: identity and subscriptions (ADAM CR-548, CR-549, CR-555, CR-560, CR-567, CR-568, decided
    and posted 3 November 2026 under the lead's "Dont hold r13. approve them and rever tto the devs"; CHG-CR548-001 to
    CHG-CR568-001). Each rule fails on r13 as released (dffd024e) and passes once the posted decision is in.

      BR-CREDENTIAL-POLICY-PROBLEM (CR-548) the 422 policy-not-met of changeOwnCredential, createPrincipal and
                                   resetPrincipalCredential is CredentialPolicyNotMetProblem (Problem plus rule:
                                   minLength, pinLength, requireBreachCheck), never errors[].
      BR-MFA-PRIMARY               (CR-549) createMfaChallenge with no methodId takes the primary usable method, else
                                   the newest; enrol, verify and remove keep at most one primary; isPrimary never null.
      BR-ENABLEMENT-SERVICE-CALLER (CR-555) getModuleEnablement takes serviceAuth beside bearerAuth, admits Platform
                                   alone as the service caller, and answers 400 tenant-required, 401, 403 and 404.
      BR-CELL-CALL-CLIENT          (CR-560) setSubscription states the seam, the serviceAuth token, the 5-second
                                   timeout and the kernel client's own ticket.
      BR-CAPACITY-PACK-UNIT        (CR-560) CapacityPack.unit is a UsageMetric; addCapacityPack answers 400.
      BR-CURRENT-PLAN-READER       (CR-567) PlanReader.Current (highest active version, compared as an integer) for
                                   getPlan, listPlans (one item per plan) and the default planVersion;
                                   SubscriptionReader.Current for getSubscription.
      BR-PREVIEW-RULES             (CR-568) previewSubscriptionChange states each figure's rule, declares its reads, and
                                   answers 404, 422 preview-currency-mismatch and 503; modulesGained and modulesLost
                                   are always present.
    """
    def words(x):
        return " ".join(str(x or "").split()).replace("**", "")

    def ptypes(o_, code):
        return set(((o_.get("responses") or {}).get(code) or {}).get("x-ticvai-problem-types") or [])

    def tables(o_, key):
        return {str((t or {}).get("table") if isinstance(t, dict) else t) for t in o_.get(key) or []}

    def schema_ref(o_, code):
        sch = (((((o_.get("responses") or {}).get(code) or {}).get("content") or {})
                .get("application/problem+json") or {}).get("schema") or {})
        refs = [str(sch.get("$ref") or "")] + [str((x or {}).get("$ref") or "") for x in sch.get("oneOf") or []]
        return {r.rsplit("/", 1)[-1] for r in refs if r}

    ident = load("contracts/spine/identity.yaml")
    isch = (ident.get("components") or {}).get("schemas") or {}
    sub = load("contracts/satellite/subscription.yaml")
    ssch = (sub.get("components") or {}).get("schemas") or {}

    # BR-CREDENTIAL-POLICY-PROBLEM (CR-548)
    cp = isch.get("CredentialPolicyNotMetProblem") or {}
    ext = [x for x in cp.get("allOf") or [] if isinstance(x, dict) and "properties" in x]
    rule = ((ext[0].get("properties") or {}).get("rule") or {}) if ext else {}
    need("BR-CREDENTIAL-POLICY-PROBLEM", bool(ext) and "rule" in (ext[0].get("required") or [])
         and rule.get("enum") == ["minLength", "pinLength", "requireBreachCheck"]
         and "errors" not in (ext[0].get("properties") or {}),
         "identity has no CredentialPolicyNotMetProblem (Problem plus a required rule of minLength, pinLength, "
         "requireBreachCheck, no errors[]) (CR-548)")
    for oid in ("changeOwnCredential", "createPrincipal", "resetPrincipalCredential"):
        o_ = op(oid)[3]
        need("BR-CREDENTIAL-POLICY-PROBLEM", "CredentialPolicyNotMetProblem" in schema_ref(o_, "422")
             and "policy-not-met" in ptypes(o_, "422"),
             f"{oid}'s 422 policy-not-met is not CredentialPolicyNotMetProblem (CR-548)")
        txt = words(o_.get("description")) + " " + words(((o_.get("responses") or {}).get("422") or {}).get("description"))
        need("BR-CREDENTIAL-POLICY-PROBLEM", "with `errors[]` naming" not in txt and "`errors[]` names `requireBreachCheck`" not in txt,
             f"{oid} still answers policy-not-met with errors[] (CR-548)")
    rbc = words((((isch.get("PasswordPolicy") or {}).get("properties") or {}).get("requireBreachCheck") or {}).get("description"))
    need("BR-CREDENTIAL-POLICY-PROBLEM", "with `errors[]` naming `requireBreachCheck`" not in rbc,
         "PasswordPolicy.requireBreachCheck still refuses with errors[] (CR-548)")

    # BR-MFA-PRIMARY (CR-549)
    cmc = words(op("createMfaChallenge")[3].get("description"))
    for frag in ("if none is marked primary, the newest (highest `id`; ids are UUIDv7)",
                 "every one is left out, the call answers the existing `409 email-otp-not-second-factor`",
                 "no active methods at all, it answers the existing `422 mfa-method-not-usable`",
                 "written to `identity.mfa_challenge.method_id`, never left null"):
        need("BR-MFA-PRIMARY", frag in cmc, f"createMfaChallenge does not state {frag!r} (CR-549)")
    need("BR-MFA-PRIMARY", "no other active method marked primary" in words(op("verifyMfaEnrolment")[3].get("description")),
         "verifyMfaEnrolment does not make the first active method primary (CR-549)")
    need("BR-MFA-PRIMARY", "writes `is_primary` false" in words(op("enrolMfaMethod")[3].get("description")),
         "enrolMfaMethod does not write is_primary false on the pending method (CR-549)")
    need("BR-MFA-PRIMARY", "the newest remaining active method" in words(op("removeMfaMethod")[3].get("description")),
         "removeMfaMethod does not move the primary mark when the primary is removed (CR-549)")
    ip = words((((isch.get("MfaMethod") or {}).get("properties") or {}).get("isPrimary") or {}).get("description"))
    need("BR-MFA-PRIMARY", "At most one primary" in ip and "never null" in ip,
         "MfaMethod.isPrimary does not say at most one primary and never null (CR-549)")
    need("BR-MFA-PRIMARY", "null means the principal's primary method" not in str(isch.get("MfaChallenge")),
         "MfaChallenge.methodId still leaves the method null for the primary one (CR-549)")

    # BR-ENABLEMENT-SERVICE-CALLER (CR-555)
    gme = op("getModuleEnablement")[3]
    need("BR-ENABLEMENT-SERVICE-CALLER", {"bearerAuth": []} in (gme.get("security") or [])
         and {"serviceAuth": []} in (gme.get("security") or []) and "service" in (gme.get("x-ticvai-audience") or []),
         "getModuleEnablement does not take serviceAuth beside bearerAuth (CR-555)")
    rs = gme.get("responses") or {}
    need("BR-ENABLEMENT-SERVICE-CALLER", "tenant-required" in ptypes(gme, "400") and {"401", "403", "404"} <= set(rs),
         "getModuleEnablement does not answer 400 tenant-required, 401, 403 and 404 (CR-555)")
    gd = words(gme.get("description"))
    for frag in ("only Platform (the Control Plane) is admitted", "kernel's ordinary permission check",
                 "no operator-token check, grant lookup or stand-in platform caller"):
        need("BR-ENABLEMENT-SERVICE-CALLER", frag in gd, f"getModuleEnablement does not state {frag!r} (CR-555)")

    # BR-CELL-CALL-CLIENT (CR-560)
    sd = words(op("setSubscription")[3].get("description"))
    for frag in ("`ITenantModuleEnablement`", "'cell unreachable'", "A timeout (5 seconds)",
                 "the control plane's own cell identity", "beside `IServiceClient`", "the cell refuses a mismatch"):
        need("BR-CELL-CALL-CLIENT", frag in sd, f"setSubscription does not state {frag!r} (CR-560)")

    # BR-CAPACITY-PACK-UNIT (CR-560)
    unit = (((ssch.get("CapacityPack") or {}).get("properties") or {}).get("unit") or {})
    need("BR-CAPACITY-PACK-UNIT", "UsageMetric" in str(unit.get("$ref") or unit.get("allOf")),
         "CapacityPack.unit is not a UsageMetric (CR-560)")
    need("BR-CAPACITY-PACK-UNIT", "counts toward no metric" in words(unit.get("description"))
         and "counts toward no metric" in sd,
         "a stored pack whose unit is not a UsageMetric is not said to count toward no metric (CR-560)")
    acp = op("addCapacityPack")[3]
    need("BR-CAPACITY-PACK-UNIT", "400" in (acp.get("responses") or {})
         and "naming the `unit` field" in words(acp.get("description")),
         "addCapacityPack does not refuse another unit with 400 validation naming unit (CR-560)")

    # BR-CURRENT-PLAN-READER (CR-567)
    act = words((((((ssch.get("Plan") or {}).get("allOf") or [{}, {}])[1].get("properties") or {}).get("isActive") or {})
                 .get("description")))
    for frag in ("`PlanReader.Current`", "the highest `version` compared as an integer", "where 9 sorts above 10",
                 "If no row is active", "replaces the `published_at` ordering"):
        need("BR-CURRENT-PLAN-READER", frag in act, f"Plan.isActive does not state {frag!r} (CR-567)")
    need("BR-CURRENT-PLAN-READER", "The current version of `planId`" in words(op("getPlan")[3].get("description")),
         "getPlan does not answer the current version (CR-567)")
    need("BR-CURRENT-PLAN-READER", "One item per plan, its current version" in words(op("listPlans")[3].get("description")),
         "listPlans does not answer one item per plan (CR-567)")
    gs = words(op("getSubscription")[3].get("description"))
    for frag in ("`SubscriptionReader.Current`", "the latest `starts_at`, then the greatest `id`", "Any status counts",
                 "It does not read `control.tenant.subscription_id`"):
        need("BR-CURRENT-PLAN-READER", frag in gs, f"getSubscription does not state {frag!r} (CR-567)")
    pv = words((((ssch.get("SetSubscriptionRequest") or {}).get("properties") or {}).get("planVersion") or {})
               .get("description"))
    need("BR-CURRENT-PLAN-READER", "PlanReader.Current" in pv,
         "SetSubscriptionRequest.planVersion does not default through PlanReader.Current (CR-567)")

    # BR-PREVIEW-RULES (CR-568)
    psc = op("previewSubscriptionChange")[3]
    pd = words(psc.get("description"))
    for frag in ("read by `getSubscription`'s reader", "a module with no listing adds nothing",
                 "rounded half away from zero to the currency's minor unit", "`requiresMigration` true whenever they differ",
                 "written once as one function both call", "`canApply`: false when `conflicts` has entries"):
        need("BR-PREVIEW-RULES", frag in pd, f"previewSubscriptionChange does not state {frag!r} (CR-568)")
    want = {"control.contract", "control.plan", "control.plan_module", "control.plan_limit", "control.licence_add_on",
            "control.licence_add_on_limit", "control.capacity_pack", "control.usage_record", "control.module_listing",
            "control.tenant"}
    need("BR-PREVIEW-RULES", want <= tables(psc, "x-ticvai-reads"),
         f"previewSubscriptionChange does not declare its reads {sorted(want - tables(psc, 'x-ticvai-reads'))} (CR-568)")
    need("BR-PREVIEW-RULES", {"404", "503"} <= set(psc.get("responses") or {})
         and "preview-currency-mismatch" in ptypes(psc, "422"),
         "previewSubscriptionChange does not answer 404, 422 preview-currency-mismatch and 503 (CR-568)")
    sp = ssch.get("SubscriptionPreview") or {}
    spp = sp.get("properties") or {}
    need("BR-PREVIEW-RULES", {"modulesGained", "modulesLost"} <= set(sp.get("required") or [])
         and all("ModuleKey" in str((spp.get(k) or {}).get("items")) for k in ("modulesGained", "modulesLost")),
         "SubscriptionPreview's modulesGained and modulesLost are not always-present ModuleKey lists (CR-568)")


if __name__ == "__main__":
    sys.exit(main())
