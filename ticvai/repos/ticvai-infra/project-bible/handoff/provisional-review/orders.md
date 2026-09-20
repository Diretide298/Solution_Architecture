# orders — 89 operations awaiting sign-off

> **These are specified, not unfinished.** Each has a request, a response and a citation of
> the pack page it was read from. `x-ticvai-provisional` means **nobody who has to build it
> has agreed it** — so the only thing that closes one is a decision in this column: *agreed*,
> *corrected* (say how), or *not needed*.

**4 pack(s), read in page order.** A session opens a book and walks it.

- Ticket Resale Marketplace — **30**
- Order Reservation Management — **29**
- Group Sales Corporate Booking Management — **20**
- Ticket Upgrade, Exchange & Conversion — **10**


---

## Group Sales Corporate Booking Management

### p4   · `listGroupSale`

`GET /group-sale` · ORDER_VIEW · staff · **Group Sales Command Center**

> Provide the Group Sales team with a centralized commercial workspace showing the entire group-sales pipeline.

**`GroupSalesCommandCenterView`** — `approvalRequests`, `averageGroupValue`, `confirmedGroups`, `confirmedRevenue`, `conversionRate`, `customerResponses`, `depositsPending`, `enquiryId`, `estimatedValue`, `eventAttraction`, `expectedCloseDate`, `expectedGuests`, `expiringQuotes`, `followUpsDue`, `groupType`, `guestCount`, `newEnquiries`, `nextAction`, `organizationCustomer`, `pipelineValue`, `probability`, `quotationsOutstanding`, `quoteStatus`, `quotesAwaitingApproval`, `quotesExpiring`, `salesOwner`, `salesTargetAchievement`, `visitDate`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-264 Group Sales Command Center
- serves P08 BO-283 Group Sales Analytics & AI Intelligence Center

**Decision:** 

### p5   · `listGroupEnquiryOpportunity`

`GET /group-enquiry-opportunity` · ORDER_VIEW · staff · **Group Enquiry & Opportunity Capture**

> Capture a new group-sales enquiry and convert it into a structured sales opportunity.

**`GroupEnquiryOpportunityCaptureView`** — `adults`, `alternativeDate`, `budget`, `campaign`, `children`, `contact`, `crm`, `customerOrganization`, `email`, `enquiryId`, `estimatedGuests`, `existingCustomer`, `expectedCloseDate`, `expectedValue`, `groupType`, `leadSource`, `manualEntry`, `nextAction`, `notes`, `phone`, `preferredDate`, `preferredTime`, `priority`, `probability`, `referral`, `requestedEvent`, `requestedExperience`, `requestedVenue`, `salesOwner`, `salesTeam`, `specialRequirements`, `staffTeachers`, `students`, `walkIn`, `website`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-265 Group Enquiry & Opportunity Capture

**Decision:** 

### p6   · `listGroupCustomerOrganization`

`GET /group-customer-organization` · ORDER_VIEW · staff · **Group Customer & Organization Profile**

> Maintain the customer or organization buying directly from TICVAI.

**`GroupCustomerOrganizationProfileView`** — `accountOwner`, `address`, `association`, `billingDetails`, `bookingContact`, `cancellationHistory`, `charity`, `city`, `company`, `confirmedBookings`, `country`, `customerId`, `decisionMaker`, `eventDayContact`, `eventOrganizer`, `financeContact`, `futureBookings`, `government`, `organizationName`, `organizationType`, `outstandingBalance`, `preferredLanguage`, `previousEnquiries`, `previousQuotations`, `primaryContact`, `privateGroup`, `registrationDetailsWhereApplicable`, `revenue`, `school`, `sportsClub`, `taxVatInformation`, `totalGuests`, `tourGroup`, `university`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-266 Group Customer & Organization Profile

**Decision:** 

### p8   · `listGroupRequirementAvailability`

`GET /group-requirement-availability` · ORDER_VIEW · staff · **Group Requirements, Availability & Capacity Planner**

> Determine whether TICVAI can accommodate the requested group before preparing a quotation.

**`GroupRequirementsAvailabilityCapacityPlannerView`** — `accessibilityRequirements`, `addOns`, `alternativeDates`, `arrivalTime`, `availableCapacity`, `catering`, `cateringCapacity`, `date`, `departureTime`, `equipment`, `eventAttraction`, `eventCapacity`, `existingGroups`, `groupSize`, `guestCategories`, `guides`, `meetingSpaces`, `operationalHolds`, `proposal`, `publicSales`, `resourceAvailability`, `resources`, `rooms`, `seatingRequirement`, `timeslotAvailability`, `transportation`, `vehicles`, `venue`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-267 Group Requirements, Availability & Capacity Planner

**Decision:** 

### p9   · `setGroupPackageExperience`

`PUT /group-package-experience` · ORDER_CREATE · staff · **Group Package & Experience Builder**

> Build a complete commercial package tailored to the group's requirements.

**`GroupPackageExperienceBuilderView`** — `addOnPrice`, `addOns`, `admissionTickets`, `birthdayPackage`, `complimentaryQuantity`, `conferencePackage`, `corporatePackage`, `discount`, `educationProgram`, `educationalWorkshop`, `fB`, `fees`, `groupRate`, `groupTicket`, `guidedTour`, `mealVoucher`, `meetingRoom`, `merchandise`, `packageTotal`, `parking`, `pricePerGuest`, `rentalResources`, `reservedSeating`, `schoolPackage`, `standardPrice`, `tax`, `transportation`, `vipExperience`, `vipGroupPackage`, `workshop`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-268 Group Package & Experience Builder

**Decision:** 

### p11  · `setGroupQuotationProposal`

`PUT /group-quotation-proposal` · ORDER_CREATE · staff · **Group Quotation Builder & Proposal Generation**

> Turn the configured group package into a professional customer quotation.

**`GroupQuotationBuilderProposalGenerationView`** — `amendmentConditions`, `cancellationPolicy`, `contact`, `currency`, `customer`, `customerPortal`, `depositRequirement`, `description`, `discount`, `email`, `fee`, `groupRate`, `guestCount`, `guestCountDeadline`, `operationalTerms`, `opportunity`, `paymentSchedule`, `pdf`, `productService`, `quantity`, `quoteDate`, `quoteNumber`, `quoteValidity`, `salesOwner`, `secureDigitalLink`, `standardRate`, `tax`, `total`, `validUntil`, `visitDate`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-269 Group Quotation Builder & Proposal Generation

**Decision:** 

### p12  · `listQuoteRevisionNegotiation`

`GET /quote-revision-negotiation` · ORDER_VIEW · staff · **Quote Revision, Negotiation & Version Management**

> Manage the commercial negotiation process without losing historical versions.

**`QuoteRevisionNegotiationVersionManagementView`** — `customerRequest`, `date`, `internalResponse`, `nt`, `packageChange`, `priceChange`, `quantityChange`, `termsChange`, `user`, `v1V2V3`, `v2`, `v3Accepted`

- serves P08 BO-270 Quote Revision, Negotiation & Version Management

**Decision:** 

### p13  · `approveGroupDiscountException`

`PUT /group-discount-exception` · ORDER_CREATE · staff · **Group Discount, Exception & Approval Workflow**

> Govern non-standard group pricing and commercial exceptions before a quote is committed.

**`GroupDiscountExceptionApprovalWorkflowView`** — `approvalRequiredCommercialDirector`, `capacityImpact`, `customer`, `customerType`, `discount`, `event`, `historicalCustomerValue`, `margin`, `marginImpact`, `opportunity`, `proposedPrice`, `quote`, `reason`, `requested18`, `risk`, `salesUser`, `standardGroupDiscount10`, `standardPrice`, `transactionValue`, `venue`

- serves P08 BO-271 Group Discount, Exception & Approval Workflow

**Decision:** 

### p15  · `listQuoteBookingConversion`

`GET /quote-booking-conversion` · ORDER_VIEW · staff · **Quote-to-Booking Conversion & Confirmation**

> Convert an accepted quotation into a confirmed TICVAI group booking without re-entering the commercial configuration.

**`QuoteToBookingConversionConfirmationView`** — `agreedPrice`, `applicable`, `approvalRemainsValid`, `bookingConfirmation`, `capacityRemainsAvailable`, `customer`, `customerDetailsComplete`, `customerPortalLinkWhereApplicable`, `depositRequest`, `groupBookingId`, `guestCountValid`, `nextSteps`, `operationalRequirements`, `paymentDepositRuleConfigured`, `paymentInstructions`, `paymentSchedule`, `priceRemainsApproved`, `products`, `quantity`, `quoteRemainsValid`, `resourcesRemainAvailable`, `salesOwner`, `ticvaiOrder`, `visitEvent`

- serves P08 BO-272 Quote-to-Booking Conversion & Confirmation

**Decision:** 

### p16  · `setGroupBookingHandover`

`PUT /group-booking-handover` · ORDER_CREATE · staff · **Group Booking 360° & Handover Workspace**

> Provide a consolidated view of the completed sales journey and hand the confirmed group cleanly from Sales to Operations. 360° Header

**`GroupBooking360HandoverWorkspaceView`** — `accessibility`, `agreedPrice`, `approval`, `arrival`, `attachments`, `balance`, `capacity`, `catering`, `creation`, `dateTime`, `departmentAssignments`, `deposit`, `discount`, `eventDayContact`, `finalQuote`, `financeContact`, `groupCheckIn`, `groupRequirementsAvailabilityCapacity`, `guides`, `handoverAcknowledgment`, `internalMentions`, `mainContact`, `notes`, `opportunity`, `organization`, `originalEnquiry`, `packageComponents`, `parking`, `products`, `reconciliationPerformanceAi`, `resources`, `seatingWhereApplicable`, `servicesTheGroup`, `specialInstructions`, `tasks`, `tickets`, `transport`

> ⚠ **37 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-273 Group Booking 360° & Handover Workspace

**Decision:** 

### p20  · `listGroupBooking`

`GET /group-booking` · ORDER_VIEW · staff · **Group Booking Operations Command Center**

> Provide Operations with a real-time command center for all confirmed and upcoming group bookings.

**`GroupBookingOperationsCommandCenterView`** — `arrivalTime`, `bookingValue`, `checkInsToday`, `completedGroups`, `expectedGuestsToday`, `groupBookingId`, `groupType`, `groupsAwaitingDeposit`, `groupsReady`, `groupsToday`, `groupsWithIssues`, `guestListStatus`, `guestListsPending`, `guests`, `operationalOwner`, `organization`, `outstandingPayments`, `paymentStatus`, `readiness`, `resourceStatus`, `resourcesPending`, `ticketStatus`, `ticketsPending`, `upcomingGroups`, `venueEvent`, `visitDate`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-274 Group Booking Operations Command Center

**Decision:** 

### p22  · `setGroupOperationalPlanning`

`PUT /group-operational-planning` · ORDER_CREATE · staff · **Group Operational Planning & Task Workspace**

> Convert the commercial booking into a detailed operational execution plan.

**`GroupOperationalPlanningTaskWorkspaceView`** — `accessibility`, `arrivalDate`, `arrivalLocation`, `arrivalTime`, `catering`, `confirmMealQuantities`, `confirmPayment`, `contactPerson`, `department`, `departureTime`, `dependency`, `dueDate`, `dueTime`, `entryGate`, `equipment`, `groupArrivalAwareness`, `groupLeaders`, `groupMeetingPoint`, `groupSize`, `guides`, `notes`, `owner`, `parking`, `prepareCredentials`, `prepareGroupEntry`, `priority`, `seating`, `specialRequirements`, `status`, `task`, `ticketingMethod`, `transportation`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-275 Group Operational Planning & Task Workspace

**Decision:** 

### p23  · `listParticipantGuestList`

`GET /participant-guest-list` · ORDER_VIEW · staff · **Participants, Guest Lists & Group Structure**

> Manage the people participating in the group where individual information is required.

**`ParticipantsGuestListsGroupStructureView`** — `accessibilityRequirement`, `ageDateOfBirthWhereApplicable`, `ageTicketMismatch`, `api`, `credentialStatus`, `csvExcelImport`, `customerUpload`, `dietaryRequirement`, `email`, `firstName`, `groupSubgroup`, `guestCountMismatch`, `guestType`, `individualGuestInformationRequired`, `invalidCategory`, `lastName`, `manualEntry`, `membership`, `missingRequiredField`, `mobile`, `previousGroupTemplate`, `seat`, `ticketCategory`

- serves P08 BO-276 Participants, Guest Lists & Group Structure

**Decision:** 

### p25  · `listGroupPaymentDeposit`

`GET /group-payment-deposit` · ORDER_VIEW · staff · **Group Payment, Deposit & Balance Management**

> Track the complete payment lifecycle of a group booking.

**`GroupPaymentDepositBalanceManagementView`** — `accountCredit`, `amountOutstanding`, `amountPaid`, `balance`, `bankTransfer`, `bookingValue`, `card`, `cashWherePermitted`, `consumeTicvaiPaymentFinanceCapabilities`, `customSchedule`, `deposit`, `depositPaid`, `depositRequired`, `finalBalance`, `installment`, `milestonePayment`, `nextDueDate`, `otherApprovedMethod`, `paymentLink`, `paymentStatus`, `placeBookingOnPaymentHold`, `preventTicketRelease`

- serves P08 BO-277 Group Payment, Deposit & Balance Management

**Decision:** 

### p26  · `listGroupTicketSeat`

`GET /group-ticket-seat` · ORDER_VIEW · staff · **Group Ticket, Seat & Entitlement Allocation**

> Allocate the confirmed group inventory to individual guests, subgroups or quantity blocks.

**`GroupTicketSeatEntitlementAllocationView`** — `accessibleSeats`, `admission`, `bulkTicket`, `companionSeats`, `credentialStatus`, `fastTrack`, `generalAdmission`, `groupCredential`, `guestSubgroup`, `individualTicket`, `keepGroupTogether`, `meal`, `merchandise`, `namedTicket`, `otherPackageComponents`, `parking`, `product`, `quantityAllocated`, `quantityBasedTicket`, `quantityBooked`, `remaining`, `reservedSeat`, `rows1218`, `seatZone`, `sectionA`, `teacherLeaderAdjacentSeating`, `ticketType`, `vipAllocation`, `workshop`, `zoneAllocation`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-278 Group Ticket, Seat & Entitlement Allocation

**Decision:** 

### p27  · `listGroupTicketFulfillment`

`GET /group-ticket-fulfillment` · ORDER_VIEW · staff · **Group Ticket Fulfillment & Distribution**

> Control how tickets and other credentials are delivered to the group.

**`GroupTicketFulfillmentDistributionView`** — `changeDeliveryMethod`, `checkInStatus`, `credential`, `delivered`, `downloaded`, `eachParticipantReceivesTheirCredential`, `email`, `entitlements`, `failed`, `generated`, `groupLeaderWallet`, `guest`, `individualMobileTickets`, `individualQr`, `nfc`, `oneGroupQr`, `opened`, `physicalCollection`, `posPrint`, `reissued`, `rfid`, `seat`, `sent`, `services`, `ticket`, `ticketsDistributedToTeachersTeamLeaders`, `ticketsRequired`, `wristband`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-279 Group Ticket Fulfillment & Distribution

**Decision:** 

### p29  · `listGroupArrivalCheck`

`GET /group-arrival-check` · ORDER_VIEW · staff · **Group Arrival, Check-In & Admission Operations**

> Manage the physical arrival and admission of large groups efficiently.

**`GroupArrivalCheckInAdmissionOperationsView`** — `accessibilityRequirement`, `actualArrival`, `additionalGuests`, `arrivalTime`, `arrived`, `booked`, `checkedIn`, `eachCredentialScannedIndividually`, `expected`, `extraGuest`, `gate`, `groupLeader`, `groupSize`, `groupsExpectedToday`, `invalidTicket`, `issues`, `lateArrival`, `missingCredential`, `missingGuest`, `noShow`, `paymentHold`, `readiness`, `remaining`, `staffLeaders`, `wrongDate`

- serves P08 BO-280 Group Arrival, Check-In & Admission Operations

**Decision:** 

### p30  · `listGroupAmendmentCancellation`

`GET /group-amendment-cancellation` · ORDER_VIEW · staff · **Group Amendments, Cancellation & Refund Operations**

> Manage changes occurring after group confirmation.

**`GroupAmendmentsCancellationRefundOperationsView`** — `additionalCharge`, `capacityOverride`, `catering`, `cateringChange`, `contractException`, `dateChange`, `equipment`, `fees`, `fullCancellation`, `guestLists`, `guides`, `increaseGuestCount`, `largeRefund`, `lateCancellation`, `newValue`, `originalValue`, `packageChange`, `partialCancellation`, `productChange`, `reduceGuestCount`, `refundCredit`, `resourceChange`, `rooms`, `seatChange`, `seatsAffected`, `tasks`, `tickets`, `ticketsAdded`, `ticketsReleased`, `timeChange`, `waivedFee`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-281 Group Amendments, Cancellation & Refund Operations

**Decision:** 

### p31  · `listGroupBookingReconciliation`

`GET /group-booking-reconciliation` · ORDER_VIEW · staff · **Group Booking Reconciliation, Closure & Performance**

> Close the group booking after the visit and reconcile what was sold against what actually occurred.

**`GroupBookingReconciliationClosurePerformanceView`** — `additionalCharges`, `admissionReconciled`, `amountPaid`, `attendance`, `customerFeedbackCapturedWhereApplicable`, `customerSatisfactionWhereAvailable`, `finalBookingValue`, `finalGuest`, `finalRevenue`, `financeReconciled`, `mealsBookedVsRedeemed`, `merchandiseFulfilled`, `noShow`, `operationalIssues`, `outstandingBalance`, `packageAttachment`, `parkingUsed`, `refunds`, `refundsResolved`, `resourcesClosed`, `resourcesConsumed`, `revenuePerGuest`, `tickets`, `ty`, `workshopsBookedVsAttended`

- serves P08 BO-274 Group Booking Operations Command Center
- serves P08 BO-282 Group Booking Reconciliation, Closure & Performance

**Decision:** 

### p33  · `listGroupSale2`

`GET /group-sale-2` · ORDER_VIEW · staff · **Group Sales Analytics & AI Intelligence Center**

> Provide management with intelligence across the complete group-sales lifecycle. This should combine data from Board 1 + Board 2.

**`GroupSalesAnalyticsAiIntelligenceCenterView`** — `additionalGroups`, `affectingB2cDemand`, `afterOneDay`, `area9CompleteArchitecture`, `averageBookingValue`, `averageGroupSize`, `cancellationRate`, `capacity`, `capacityUtilization`, `conversionRate`, `customerTerms`, `discount`, `discountCost`, `discounts`, `enquiries`, `expectedContribution`, `groupBookings`, `guests`, `management`, `noShowRate`, `outstandingReceivables`, `prices`, `quotes`, `reconciliation`, `repeatCustomerRate`, `resourceManagementAndAccessControl`, `revenue`, `revenuePerGuest`, `showConversionAtEachStage`, `toMateriallyIncreaseConversion`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-264 Group Sales Command Center
- serves P08 BO-283 Group Sales Analytics & AI Intelligence Center

**Decision:** 


---

## Order Reservation Management

### p3   · `listOrderReservation`

`GET /order-reservation` · ORDER_VIEW · staff · **Order & Reservation Command Center**

> Provide the central operational workspace for searching, monitoring, opening, and managing every order and reservation across TICVAI.

**`OrderReservationCommandCenterView`** — `activeReservations`, `cancelledOrders`, `channel`, `collectPayment`, `completedOrders`, `confirmedOrders`, `createdDate`, `customer`, `expiringReservations`, `expiry`, `failedOrders`, `fulfillmentStatus`, `grossOrderValue`, `orderId`, `orderValue`, `ordersRequiringAttention`, `ordersToday`, `ownerAgent`, `partiallyFulfilled`, `paymentStatus`, `pendingPayment`, `productEvent`, `reservationId`, `reservationStatus`, `temporaryHolds`, `venue`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-304 Order & Reservation Command Center

**Decision:** 

### p5   · `setOrderDetailTransaction`

`PUT /order-detail-transaction` · ORDER_CREATE · staff · **Order Detail & Transaction Workspace**

> Provide the authoritative 360-degree view of a single order. This should become one of the most important operational screens in TICVAI.

**`OrderDetailTransactionWorkspaceView`** — `cashierAgent`, `channel`, `credentials`, `currency`, `customer`, `date`, `discount`, `event`, `fee`, `fulfillmentStatus`, `invoices`, `membership`, `orderDate`, `orderNumber`, `orderStatus`, `orderTime`, `paymentStatus`, `payments`, `performance`, `personType`, `product`, `quantity`, `refunds`, `relatedOrders`, `reservationStatus`, `reservations`, `salesLocation`, `seat`, `tax`, `ticketStatus`, `ticketType`, `tickets`, `timeslot`, `total`, `unitPrice`, `waivers`

> ⚠ **36 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-305 Order Detail & Transaction Workspace

**Decision:** 

### p7   · `setReservationHoldPolicy`

`PUT /reservation-hold-policy` · ORDER_CREATE · staff · **Reservation & Hold Policy Configuration**

> Configure how TICVAI temporarily reserves inventory before an order is fully confirmed.

**`ReservationHoldPolicyConfigurationView`** — `admissionCapacity`, `agentReservation`, `approvalRequirement`, `authorizedRole`, `b2bReservation`, `cartHold`, `channel`, `checkoutHold`, `corporateReservation`, `customerSegment`, `entitlementCapacity`, `event`, `extensionAllowed`, `extensionDuration`, `groupReservation`, `inventory`, `inventoryHold`, `maintainAuditRecord`, `manualHold`, `maximumExtensions`, `paymentHold`, `performance`, `product`, `reservationType`, `seat`, `seatHold`, `throughTheCentralCapacityInventoryServices`, `ticketType`, `timeslotCapacity`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-306 Reservation & Hold Policy Configuration

**Decision:** 

### p9   · `setOrderReservationStatus`

`PUT /order-reservation-statu` · ORDER_CREATE · staff · **Order & Reservation Status Lifecycle Configuration**

> Define the governed state machine for orders and reservations. SoftLab should not hard-code status transitions independently in every channel.

**`OrderReservationStatusLifecycleConfigurationView`** — `allowedRole`, `auditRequirement`, `fromStatus`, `integrationRequirement`, `notification`, `operationalStatus`, `requiredConditions`, `systemControlledStatus`, `toStatus`, `userEditableStatus`, `userSystemAction`

- serves P08 BO-307 Order & Reservation Status Lifecycle Configuration

**Decision:** 

### p10  · `createOrderSourceChannel`

`POST /order-source-channel` · ORDER_CREATE · staff · **Order Creation & Source/Channel Configuration**

> Configure how orders can originate from different TICVAI sales channels while using one common transaction engine.

**`OrderCreationSourceChannelConfigurationView`** — `administrativeBackend`, `affiliate`, `agent`, `api`, `apiConsumer`, `b2bPortal`, `b2cWeb`, `boxOffice`, `callCenter`, `campaign`, `channel`, `channelPrefix`, `customPattern`, `device`, `erpReference`, `externalCrmReference`, `externalReference`, `globalSequence`, `holdInventory`, `kiosk`, `mobileApp`, `mobileFlyingPos`, `ota`, `otaBookingReference`, `partner`, `pos`, `repeatedRequests`, `reseller`, `resellerOrderId`, `salesLocation`, `subChannel`, `tenantSequence`, `terminal`, `venueSequence`, `yearMonthPrefix`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-308 Order Creation & Source/Channel Configuration

**Decision:** 

### p11  · `setCustomerGuestAccount`

`PUT /customer-guest-account` · ORDER_CREATE · staff · **Customer, Guest & Account Assignment**

> Define how customers are identified and associated with orders/reservations.

**`CustomerGuestAccountAssignmentView`** — `agent`, `anonymousSaleWherePermitted`, `b2bAccount`, `company`, `continueGuest`, `corporateAccount`, `costCenterWhereApplicable`, `country`, `customerId`, `dateOfBirth`, `dependingOnPolicy`, `email`, `from`, `groupOrganizer`, `guestCheckout`, `language`, `member`, `membershipId`, `mobile`, `name`, `partner`, `registeredCustomer`, `reseller`, `taxDetails`

- serves P08 BO-309 Customer, Guest & Account Assignment

**Decision:** 

### p13  · `listOrderLineProduct`

`GET /order-line-product` · ORDER_VIEW · staff · **Order Line, Product & Entitlement Composition**

> Manage the products and commercial components contained within an order.

**`OrderLineProductEntitlementCompositionView`** — `addOns`, `capacity`, `channelLimits`, `customerLimits`, `date`, `discount`, `entitlement`, `event`, `eventLimits`, `experiences`, `fB`, `fee`, `fulfillmentMethod`, `memberships`, `moment`, `otherConfiguredProducts`, `packages`, `parking`, `performance`, `personType`, `price`, `product`, `productLimits`, `quantity`, `rental`, `retail`, `seat`, `tax`, `tickets`, `timeslot`, `variant`, `vouchers`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-310 Order Line, Product & Entitlement Composition

**Decision:** 

### p14  · `listCapacityReservationInventory`

`GET /capacity-reservation-inventory` · ORDER_VIEW · staff · **Capacity Reservation & Inventory Commitment**

> Control when and how order activity consumes real capacity/inventory. This is the transactional bridge between the Order Engine and the Capacity/Inventory Engines.

**`CapacityReservationInventoryCommitmentView`** — `authorizedAmendmentRemovesProduct`, `confirmedInventoryConsumption`, `eventCapacity`, `fBRetailInventoryWhereApplicable`, `generalAdmissionCapacity`, `holdExpires`, `orderFails`, `paymentFailsAccordingToPolicy`, `productInventory`, `rentalInventory`, `reservationCancels`, `returnAControlledException`, `seatInventory`, `temporaryAvailabilityProtection`, `timeslotCapacity`

- serves P08 BO-311 Capacity Reservation & Inventory Commitment

**Decision:** 

### p15  · `listReservationConfirmationExpiry`

`GET /reservation-confirmation-expiry` · ORDER_VIEW · staff · **Reservation Confirmation, Expiry & Fulfillment Readiness**

> Determine when a reservation becomes a confirmed order and when it is ready for ticket/media fulfillment.

**`ReservationConfirmationExpiryFulfillmentReadinessView`** — `capacityConfirmed`, `credentialConfiguration`, `creditApproved`, `customerDataComplete`, `deliveryMethod`, `depositReceived`, `emailDelivery`, `entitlementValid`, `exampleB2b`, `exampleB2c`, `expire`, `orderConfirmed`, `otherCredentialServices`, `partnerAuthorized`, `partnerConfirmationReceived`, `paymentComplete`, `paymentConditionMet`, `preserveHistory`, `requiredApprovalComplete`, `requiredCustomerData`, `requiredWaiverComplete`, `rfidNfc`, `ticketMedia`, `waiverRequirement`, `walletPass`

- serves P08 BO-312 Reservation Confirmation, Expiry & Fulfillment Readiness

**Decision:** 

### p17  · `listOrderLifecycleTimeline`

`GET /order-lifecycle-timeline` · ORDER_VIEW · staff · **Order Lifecycle Timeline, SLA, Exceptions & AI Operations**

> Provide complete lifecycle visibility and proactively identify orders/reservations that require operational intervention.

**`OrderLifecycleTimelineSlaExceptionsAiOperationsView`** — `board2AmendmentsCancellations`, `capacityMismatch`, `channel`, `correlationId`, `created`, `eventType`, `externalSynchronizationFailure`, `fulfillmentFailure`, `governedCommercialTransaction`, `importantArchitectureDecisionsToFreeze`, `missingCustomerData`, `newState`, `orphanReservation`, `paymentOrderMismatch`, `previousState`, `relatedTransaction`, `reprocessFulfillment`, `result`, `revalidate`, `stuckOrder`, `timestamp`, `userSystem`

- serves P08 BO-313 Order Lifecycle Timeline, SLA, Exceptions & AI Operations

**Decision:** 

### p20  · `listAmendmentAfterSale`

`GET /amendment-after-sale` · ORDER_VIEW · staff · **Amendment & After-Sales Command Center**

> Provide one operational workspace for all post-sale activities affecting confirmed orders and reservations.

**`AmendmentAfterSalesCommandCenterView`** — `amendmentsToday`, `approvalStatus`, `attendeeChange`, `cancellation`, `cancellations`, `channel`, `createdTime`, `customer`, `dateChange`, `dateTimeChanges`, `failedActions`, `financialImpact`, `orderAmendment`, `orderNumber`, `originalValue`, `partialCancellation`, `partialCancellations`, `pendingAmendments`, `pendingApprovals`, `performanceChange`, `processingStatus`, `productEvent`, `quantityChange`, `reissues`, `requestId`, `requestType`, `requestedBy`, `reservationAmendment`, `slaBreaches`, `timeslotChange`, `voids`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-314 Amendment & After-Sales Command Center
- serves P08 BO-323 Amendment History, Audit & After-Sales Analytics

**Decision:** 

### p22  · `setOrderAmendment`

`PUT /order-amendment` · ORDER_CREATE · staff · **Order Amendment Workspace**

> Provide agents with a controlled workspace for modifying an existing order without directly editing historical transaction records. The original order must always remain reconstructable.

**`OrderAmendmentWorkspaceView`** — `amendmentPolicy`, `availability`, `calculate`, `capacity`, `credentialImpact`, `currentReservation`, `customer`, `customerDetails`, `customerEligibility`, `deliveryMethod`, `eligibleProductAttributes`, `executeAmendment`, `fulfillmentMethod`, `fulfillmentStatus`, `orderDate`, `orderId`, `originalChannel`, `payment`, `paymentStatus`, `performance`, `pricing`, `productRules`, `quantity`, `seatAvailability`, `seatWhereApplicable`, `ticketHolder`, `tickets`, `timeslot`, `total`, `venue`, `visitDate`, `waiver`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-315 Order Amendment Workspace

**Decision:** 

### p24  · `setAmendmentEligibilityPolicy`

`PUT /amendment-eligibility-policy` · ORDER_CREATE · staff · **Amendment Eligibility & Policy Rule Builder**

> Define when an order or reservation may be amended and which changes are permitted.

**`AmendmentEligibilityPolicyRuleBuilderView`** — `attendeeChange`, `broaderExceptionPermissions`, `cancelled`, `channel`, `coolingPeriod`, `customerSegment`, `dateChange`, `dateTimeAttendeeChanges`, `dateTimeChangeOnly`, `deliveryChange`, `event`, `expired`, `fullyUsed`, `maximumAmendmentsPerOrder`, `maximumAmendmentsPerTicket`, `maximumDateChanges`, `membership`, `orderStatus`, `otherPermittedModifications`, `partiallyUsed`, `performance`, `performanceChange`, `product`, `quantityIncrease`, `quantityReduction`, `seatChange`, `suspended`, `tenant`, `ticketStatus`, `ticketType`, `timeslotChange`, `unused`, `venue`

> ⚠ **33 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-316 Amendment Eligibility & Policy Rule Builder

**Decision:** 

### p26  · `setCancellationPartialPolicy`

`PUT /cancellation-partial-policy` · ORDER_CREATE · staff · **Cancellation & Partial Cancellation Policy Configuration**

> Configure whether an order, reservation, or selected order lines may be cancelled.

**`CancellationPartialCancellationPolicyConfigurationView`** — `addOnOnly`, `cancellationWindow`, `channel`, `customerSegment`, `entireOrder`, `entireReservation`, `eventDate`, `groupMember`, `individualTicket`, `notPermittedExceptSupervisorException`, `orderStatus`, `packageComponentWherePermitted`, `paymentStatus`, `product`, `selectedOrderLines`, `selectedQuantity`, `ticketStatus`, `usage`

- serves P08 BO-317 Cancellation & Partial Cancellation Policy Configuration

**Decision:** 

### p29  · `listVoidReversalSame`

`GET /void-reversal-same` · ORDER_VIEW · staff · **Void, Reversal & Same-Day Correction Management**

> Separate genuine void/correction operations from normal customer cancellations and refunds. This is important financially and operationally.

**`VoidReversalSameDayCorrectionManagementView`** — `accidentalSaleReversal`, `beforeFiscalClosure`, `beforeSettlement`, `beforeTicketUse`, `failedTransactionCleanup`, `finalAccountingTreatment`, `finance`, `fiscalTaxServiceWhereApplicable`, `insteadOf`, `operatorError`, `optionalDualAuthorization`, `orderVoid`, `paymentGateway`, `paymentVoidRequest`, `pos`, `reason`, `rolePermission`, `sameBusinessDayOnly`, `sameDayCorrection`, `specificChannelsOnly`, `supervisorApproval`, `supervisorRequired`, `technicalFailure`, `ticketVoid`, `wrongPayment`, `wrongProduct`, `wrongQuantity`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-319 Void, Reversal & Same-Day Correction Management

**Decision:** 

### p30  · `listTicketReissueFulfillment`

`GET /ticket-reissue-fulfillment` · ORDER_VIEW · staff · **Ticket Reissue & Fulfillment Regeneration**

> Manage ticket/media regeneration following an amendment, correction, loss, delivery failure, or other authorized event.

**`TicketReissueFulfillmentRegenerationView`** — `active`, `administrativeCorrection`, `attendeeChanged`, `barcode`, `boxOfficeCollection`, `credentialCompromised`, `damagedCredential`, `dateChanged`, `dynamicQr`, `email`, `emailNotReceived`, `freeReissueCount`, `lostTicket`, `maximumReissues`, `mobileApp`, `nfc`, `optionsType`, `posPrint`, `printedTicket`, `printingError`, `qr`, `rfid`, `seatChanged`, `smsWhatsappLink`, `supervisorThreshold`, `timeslotChanged`, `walletPass`, `walletPassIssue`, `walletUpdate`, `wearable`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-320 Ticket Reissue & Fulfillment Regeneration

**Decision:** 

### p32  · `setAfterSaleFinancial`

`PUT /after-sale-financial` · ORDER_CREATE · staff · **After-Sales Financial Settlement & Adjustment Workspace**

> Provide a consolidated view of the financial consequences of amendments, cancellations, refunds, exchanges and corrections. This is not the payment engine; it is the after-sales financial orchestration layer.

**`AfterSalesFinancialSettlementAdjustmentWorkspaceView`** — `additionalCharge`, `alreadyRefunded`, `collectionRequired`, `creditNote`, `credits`, `currentOrderValue`, `failed`, `fees`, `invoiceAdjustment`, `netTransactionImpact`, `noFinancialDifference`, `originalOrderValue`, `outstandingBalance`, `paymentComplete`, `paymentPending`, `reconciliationRequired`, `taxAdjustment`, `throughTheFinanceDocumentServices`, `updatedReceipt`

- serves P08 BO-321 After-Sales Financial Settlement & Adjustment Workspace

**Decision:** 

### p33  · `approveExceptionServiceRecovery`

`PUT /exception-service-recovery` · ORDER_CREATE · staff · **Approval, Exception & Service Recovery Management**

> Govern after-sales actions that fall outside normal policies or exceed financial/operational authority.

**`ApprovalExceptionServiceRecoveryManagementView`** — `alternativeDate`, `alternativeEvent`, `complimentaryAddOn`, `complimentaryReissue`, `customer`, `feeWaiver`, `financialImpact`, `order`, `partialRefund`, `reason`, `requestedAction`, `requestedException`, `requestor`, `standardPolicyResult`, `supportingDocuments`, `voucher`, `walletCredit`

- serves P08 BO-322 Approval, Exception & Service Recovery Management

**Decision:** 

### p35  · `listAmendmentAfterSale2`

`GET /amendment-after-sale-2` · ORDER_VIEW · staff · **Amendment History, Audit & After-Sales Analytics**

> Provide complete traceability and analytical visibility across all changes made after original order creation.

**`AmendmentHistoryAuditAfterSalesAnalyticsView`** — `action`, `afterValue`, `amendmentRate`, `approval`, `approvalRate`, `averageRefund`, `beforeValue`, `board3CompletesArea12`, `cancellationRate`, `channel`, `customer`, `exception`, `exceptionRate`, `excessiveVoids`, `financialImpact`, `frequentFeeWaivers`, `highReissueFrequency`, `neverOverwriteTheOriginalOrder`, `orderId`, `preserveSnapshotsForSignificantAmendments`, `repeatedManualRefunds`, `repeatedOutOfPolicyExceptions`, `requestId`, `result`, `ruleApplied`, `seatB12`, `seatC08`, `serviceRecoveryCost`, `ticketId`, `timestamp`, `to`, `traceability`, `user`, `usersOfMisconduct`, `valueAed250`, `valueAed280`, `visit02Sep1800`, `visit03Sep1900`

> ⚠ **38 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-314 Amendment & After-Sales Command Center
- serves P08 BO-323 Amendment History, Audit & After-Sales Analytics

**Decision:** 

### p40  · `listPaymentOrderFinancial`

`GET /payment-order-financial` · ORDER_VIEW · staff · **Payment & Order Financial Command Center**

> Provide operations and finance teams with a centralized view of the financial status of all

**`PaymentOrderFinancialCommandCenterView`** — `amountPaid`, `authorized`, `by`, `channel`, `currency`, `customer`, `failed`, `failedPayments`, `fullyPaidOrders`, `grossOrderValue`, `notRequired`, `orderId`, `orderStatus`, `orderValue`, `outstanding`, `outstandingBalance`, `overpaid`, `paid`, `partiallyPaid`, `partiallyPaidOrders`, `partiallyRefunded`, `paymentInitiated`, `paymentMethod`, `paymentMethods`, `paymentProvider`, `paymentStatus`, `paymentsToday`, `pendingPayments`, `reconciliationExceptions`, `reconciliationRequired`, `reconciliationStatus`, `refunded`, `refundsPending`, `reversed`, `settlementStatus`, `settlementVariance`, `unallocatedPayments`, `unpaid`, `unpaidOrders`, `venue`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-324 Payment & Order Financial Command Center

**Decision:** 

### p41  · `listOrderPaymentDetail`

`GET /order-payment-detail` · ORDER_VIEW · staff · **Order Payment Detail & Transaction Ledger**

> Provide the complete payment history associated with an individual order.

**`OrderPaymentDetailTransactionLedgerView`** — `additionalCollection`, `adjustment`, `aedComplete`, `authorization`, `authorizationCode`, `capture`, `creditApplied`, `creditNote`, `currency`, `customer`, `deposit`, `externalReference`, `gateway`, `gatewayTransactionId`, `merchant`, `nt100`, `nt300`, `onOdNt`, `orderNumber`, `orderTotal`, `outstanding`, `paid`, `partialRefund`, `payment`, `paymentStatus`, `refunded`, `reversal`, `settlementReference`, `settlementStatus`, `terminal`, `voucher`, `walletCredit`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-325 Order Payment Detail & Transaction Ledger
- serves P09 ADM-607 Mixed Tender Transaction Trace & Allocation Audit 100
- serves P09 ADM-617 Refund Transaction Trace & Audit Investigation 124

**Decision:** 

### p43  · `setMultiPaymentSplit`

`PUT /multi-payment-split` · ORDER_CREATE · staff · **Multi-Payment, Split Tender & Payment Allocation Configuration**

> Support orders paid using multiple payment methods and determine how each payment is allocated.

**`MultiPaymentSplitTenderPaymentAllocationConfiguratioView`** — `channel`, `customerType`, `deposit`, `destination`, `orderLevel`, `orderLineLevel`, `orderType`, `product`, `productLevel`, `specificTicket`, `taxFeeComponent`, `terminal`, `venue`, `visaAed600`, `voucherAed150`, `walletAed250`

- serves P08 BO-326 Multi-Payment, Split Tender & Payment Allocation Configuration
- serves P09 ADM-601 Split Payment & Tender Allocation Manager 94

**Decision:** 

### p44  · `listDepositPartialPayment`

`GET /deposit-partial-payment` · ORDER_VIEW · staff · **Deposit, Partial Payment & Outstanding Balance Management**

> Support commercial scenarios where an order may be confirmed or reserved without full immediate payment.

**`DepositPartialPaymentOutstandingBalanceManagementView`** — `b2b`, `balanceBeforeVisit`, `balanceByFixedDate`, `corporateSales`, `creditAccount`, `daysRemaining`, `depositPaid`, `depositRequired`, `dueDate`, `dueSoon`, `events`, `finalNotice`, `fixedDeposit`, `fullPayment`, `gracePeriod`, `groups`, `largeReservations`, `overdue`, `payOnCollectionWherePermitted`, `paymentReminder`, `percentageDeposit`, `remainingBalance`, `requireApproval`, `requiredDeposit`, `schools`, `stagedPayment`, `status`, `total`, `warning`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-327 Deposit, Partial Payment & Outstanding Balance Management

**Decision:** 

### p46  · `listOrderSplitMerge`

`GET /order-split-merge` · ORDER_VIEW · staff · **Order Split, Merge & Transaction Relationship Management**

> Allow complex orders to be reorganized without destroying transaction history.

**`OrderSplitMergeTransactionRelationshipManagementView`** — `amendedFrom`, `attendee`, `basePrice`, `childOrder`, `convertedFrom`, `corporateCostCenter`, `correctlyAcrossDerivedOrders`, `credits`, `currency`, `customer`, `department`, `discount`, `fees`, `legalEntity`, `mergedInto`, `neverEraseTheOriginalRelationship`, `orderA4Tickets`, `orderB2Tickets`, `orderLine`, `parentOrder`, `paymentResponsibility`, `paymentStatus`, `payments`, `product`, `productCompatibility`, `refunds`, `reissuedFrom`, `replacementOrder`, `tax`, `taxContext`, `ticket`, `venue`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-328 Order Split, Merge & Transaction Relationship Management

**Decision:** 

### p47  · `listRelatedOrderTransaction`

`GET /related-order-transaction` · ORDER_VIEW · staff · **Related Order & Transaction Relationship Explorer**

> Provide a visual relationship map for complex transaction histories. This becomes especially useful after amendments, upgrades, exchanges, reissues, splits and refunds.

**`RelatedOrderTransactionRelationshipExplorerView`** — `additionalPayment`, `amendment`, `cancellation`, `chargebackWhereIntegrated`, `conversion`, `exchange`, `externalTransaction`, `original`, `partialCancellation`, `payment`, `refund`, `ticketUpgrade`

- serves P08 BO-329 Related Order & Transaction Relationship Explorer

**Decision:** 

### p49  · `listExternalPaymentPartner`

`GET /external-payment-partner` · ORDER_VIEW · staff · **External Payment, Partner & Settlement Reference Mapping**

> Maintain the relationship between TICVAI transactions and external financial/channel references.

**`ExternalPaymentPartnerSettlementReferenceMappingView`** — `acquirers`, `amount`, `approvalWhereRequired`, `authorizationCode`, `b2bPartners`, `banks`, `currency`, `erp`, `erpReference`, `externalTransactionId`, `financeSystems`, `merchantId`, `multipleGatewayTransactions`, `multiplePartnerReferences`, `multiplePayments`, `multipleRefunds`, `otas`, `partnerOrderId`, `paymentGateways`, `posTerminals`, `provider`, `reason`, `resellers`, `settlementBatch`, `settlementDate`, `ticvaiOrderId`, `ticvaiPaymentId`, `timestamp`, `user`, `walletProviders`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-330 External Payment, Partner & Settlement Reference Mapping

**Decision:** 

### p50  · `listPaymentReconciliationException`

`GET /payment-reconciliation-exception` · ORDER_VIEW · staff · **Payment Reconciliation & Exception Management**

> Automatically compare TICVAI payment records with external payment and settlement records.

**`PaymentReconciliationExceptionManagementView`** — `acquirer`, `aed250`, `amount`, `authorizationCode`, `bank`, `currency`, `date`, `erp`, `externalReference`, `investigate`, `markPending`, `match`, `merchant`, `mismatch500480`, `order`, `ota`, `paymentGateway`, `pos`, `remap`, `reseller`, `settlement250`, `transactionId`, `wallet`

- serves P08 BO-331 Payment Reconciliation & Exception Management

**Decision:** 

### p51  · `listFinancialTraceability`

`GET /financial-traceability` · ORDER_VIEW · staff · **Financial Traceability, Control & Audit Explorer**

> Provide a complete financial audit trail across the order lifecycle.

**`FinancialTraceabilityControlAuditExplorerView`** — `amount`, `channel`, `compliance`, `creditOverride`, `currency`, `discount`, `externalAudit`, `fee`, `feeWaiver`, `finance`, `internalAudit`, `management`, `manualAllocation`, `manualPaymentAdjustment`, `manualReconciliation`, `manualRefund`, `manualSettlementMapping`, `paymentMethod`, `priceVersion`, `provider`, `tax`, `timestamp`, `user`

- serves P08 BO-332 Financial Traceability, Control & Audit Explorer

**Decision:** 

### p53  · `listOrderFinancialReconciliation`

`GET /order-financial-reconciliation` · ORDER_VIEW · staff · **Order Financial Analytics & AI Reconciliation Intelligence**

> Provide management-level analytics across order payment performance, balances, settlement and reconciliation.

**`OrderFinancialAnalyticsAiReconciliationIntelligenceView`** — `approvalRate`, `area12FinalArchitecture`, `averagePaymentMethodsPerOrder`, `backendScreenCoreResponsibility`, `collectionRate`, `current`, `depositExposure`, `failureRate`, `grossOrderValue`, `netCollected`, `orderReservation`, `outstandingBalance`, `overdueBalance`, `paymentFailureRate`, `paymentGatewayModules`, `reconciliationExceptions`, `reconciliationRate`, `settlementDelay`, `settlementVariance`, `sow`

- serves P08 BO-333 Order Financial Analytics & AI Reconciliation Intelligence

**Decision:** 


---

## Ticket Resale Marketplace

### p4   · `listResaleMarketplace`

`GET /resale-marketplace` · ORDER_VIEW · staff · **Resale Marketplace Command Center**

> Provide administrators with a centralized operational view of the TICVAI resale marketplace.

**`ResaleMarketplaceCommandCenterView`** — `activeListings`, `andExceptionStates`, `averageResalePrice`, `conversionRate`, `eventDate`, `eventProduct`, `expiringListings`, `expiry`, `grossResaleValue`, `listedPrice`, `listingDate`, `listingId`, `listingsSoldToday`, `marketplaceFee`, `marketplaceFees`, `originalOrderTicketId`, `originalPrice`, `pendingApproval`, `priceVariance`, `rejectedListings`, `riskIndicator`, `sectionRowSeat`, `seller`, `sellerProceeds`, `status`, `suspendedListings`, `ticketsAvailableForResale`, `venue`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-278 Resale Marketplace Command Center

**Decision:** 

### p5   · `setResaleEligibilityRule`

`PUT /resale-eligibility-rule` · ORDER_CREATE · staff · **Resale Eligibility Rule Configuration**

> Define whether a ticket is allowed to enter the resale marketplace. Not every TICVAI ticket should automatically be resellable.

**`ResaleEligibilityRuleConfigurationView`** — `allowResaleImmediatelyAfterPurchase`, `blackoutPeriod`, `customerSegment`, `event`, `eventHasNotStarted`, `identityVerificationRequirement`, `maximumListingsPerCustomer`, `maximumResaleAttempts`, `membershipRestriction`, `membershipType`, `minimumOwnershipPeriod`, `originalPurchaserOnly`, `paymentStatus`, `performance`, `priceCategory`, `product`, `promotion`, `salesChannel`, `specificResaleStartEndDate`, `ticketHasNotBeenScanned`, `ticketHasNotExpired`, `ticketIsFullyPaid`, `ticketIsNotBlocked`, `ticketIsNotComplimentary`, `ticketIsNotInternal`, `ticketIsNotRefunded`, `ticketIsNotStaff`, `ticketIsNotUnderDispute`, `ticketOwnershipStatus`, `ticketStatus`, `ticketType`, `venue`

> ⚠ **8 of 32 property names read as sentences** rather than fields — likely the pack's bullets (triggers, behaviours) taken as a directory: `allowResaleImmediatelyAfterPurchase`, `ticketIsFullyPaid`, `ticketIsNotBlocked`, `ticketIsNotComplimentary`, `ticketIsNotInternal` **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-199 Eligibility Rule Builder
- serves P09 ADM-279 Resale Eligibility Rule Configuration

**Decision:** 

### p7   · `listResalePolicyMarketplace`

`GET /resale-policy-marketplace` · ORDER_VIEW · staff · **Resale Policy & Marketplace Settings**

> Configure the overall business policies governing a resale marketplace.

**`ResalePolicyMarketplaceSettingsView`** — `applicableOrganization`, `bankPayoutInformation`, `brand`, `buyerTerms`, `currency`, `customerTerms`, `identityRequirements`, `listingConfirmation`, `marketplaceDisclosures`, `marketplaceName`, `marketplaceSalesChannel`, `marketplaceStatus`, `operatorDeterminesResalePrice`, `purchaseLimits`, `resaleTicketLabeling`, `sellerNotifications`, `sellerSelectsAPermittedPrice`, `sellerTerms`, `sellerTermsAcceptance`, `sellerVerification`, `serviceFees`, `supportedLanguage`, `timeZone`, `venue`

- serves P09 ADM-278 Resale Marketplace Command Center
- serves P09 ADM-280 Resale Policy & Marketplace Settings

**Decision:** 

### p9   · `createListingSeller`

`POST /listing-seller` · ORDER_CREATE · staff · **Listing Creation & Seller Configuration**

> Define how eligible ticket holders create resale listings.

**`ListingCreationSellerConfigurationView`** — `acceptRecommendedPrice`, `acceptTermsSubmitListing`, `adjacentSeatGroup`, `changePrice`, `chooseSellingPrice`, `dateTime`, `estimatedProceeds`, `event`, `existingListing`, `expiration`, `fee`, `listingDate`, `listingId`, `listingPrice`, `multipleTicketListing`, `originalPrice`, `paymentStatus`, `relistExpiredListing`, `resaleEligibility`, `row`, `seat`, `section`, `seller`, `sellerTermsAcceptance`, `singleTicketListing`, `ticketId`, `ticketOwnership`, `ticketScanStatus`, `ticketStatus`, `ticketType`, `ticketValidity`, `venue`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-281 Listing Creation & Seller Configuration

**Decision:** 

### p10  · `listResalePricingPrice`

`GET /resale-pricing-price` · ORDER_VIEW · staff · **Resale Pricing & Price Guardrails**

> Control the permitted resale price while protecting the operator, seller and buyer.

**`ResalePricingPriceGuardrailsView`** — `automaticPriceReduction`, `currentDynamicPrice`, `currentSellingPrice`, `dynamicPermittedRange`, `eventPrice`, `eventSpecificRange`, `faceValueOnly`, `fixedResalePrice`, `maximumAed240`, `maximumDiscount`, `maximumMarkup`, `maximumResalePrice`, `minimumAed160`, `minimumIntervalBetweenChanges`, `minimumResalePrice`, `numberOfPriceChanges`, `originalFaceValue`, `originalPaidPrice`, `priceAdjustmentCutoff`, `priceCategory`, `productSpecificRange`, `sellerCanEditPrice`

- serves P09 ADM-282 Resale Pricing & Price Guardrails

**Decision:** 

### p12  · `listResaleFeeCommission`

`GET /resale-fee-commission` · ORDER_VIEW · staff · **Resale Fees, Commission & Seller Proceeds**

> Configure the commercial model of the resale marketplace.

**`ResaleFeesCommissionSellerProceedsView`** — `administrativeFee`, `buyerFee`, `buyerServiceFeeAed12`, `buyerType`, `channel`, `currency`, `event`, `flatTransactionFee`, `listingPriceAed250`, `marketplaceCommission`, `paymentProcessingFee`, `percentageFee`, `product`, `sellerFee`, `sellerProceedsAed225`, `sellerType`, `taxOnFee`, `tenant`, `ticketAed250`, `totalAed262`, `venue`, `venueFee`

- serves P09 ADM-283 Resale Fees, Commission & Seller Proceeds

**Decision:** 

### p13  · `approveListingModeration`

`PUT /listing-moderation` · ORDER_CREATE · staff · **Listing Approval & Moderation**

> Determine whether listings are published automatically or require operator review.

**`ListingApprovalModerationView`** — `event`, `fraudIndicator`, `highResalePrice`, `highValueTicket`, `identityIssue`, `listing`, `listingPrice`, `multipleListings`, `newSeller`, `originalPrice`, `paymentIssue`, `priceVariance`, `requestInformation`, `riskScore`, `seller`, `sellerRisk`, `submittedDate`, `ticket`, `ticketOwnershipConcern`, `unusualDiscount`, `vipTicket`

- serves P09 ADM-284 Listing Approval & Moderation

**Decision:** 

### p15  · `listResaleInventoryAvailability`

`GET /resale-inventory-availability` · ORDER_VIEW · staff · **Resale Inventory & Availability Management**

> Maintain an accurate, synchronized view of tickets currently available through resale.

**`ResaleInventoryAvailabilityManagementView`** — `event`, `listingStatus`, `performance`, `price`, `product`, `row`, `seat`, `section`, `unsoldOriginalTicketInventory`

- serves P09 ADM-285 Resale Inventory & Availability Management

**Decision:** 

### p16  · `listListingLifecycleExpiry`

`GET /listing-lifecycle-expiry` · ORDER_VIEW · staff · **Listing Lifecycle, Expiry & Cancellation**

> Control the full lifecycle of a resale listing from creation until sale, withdrawal or expiry.

**`ListingLifecycleExpiryCancellationView`** — `atConfiguredDate`, `atConfiguredTime`, `atEventStart`, `cancellationCutoff`, `cancellationFee`, `cancelled`, `eligibilityChanges`, `eventChangesMaterially`, `eventIsCancelled`, `expired`, `fraudIsDetected`, `listingApproved`, `listingExpired`, `listingExpiring`, `listingRejected`, `listingSold`, `listingSuspended`, `listingWithdrawn`, `maximumWithdrawals`, `paymentIsReversed`, `priceChanged`, `rejected`, `requiresOperatorAction`, `sellerCanWithdrawAnytime`, `sellerCannotWithdrawWhileReserved`, `suspended`, `ticketBecomesInvalid`, `ticketIsRefunded`, `ticketIsTransferred`, `withdrawn`, `xHoursBeforeEvent`, `xMinutesBeforeEvent`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-286 Listing Lifecycle, Expiry & Cancellation

**Decision:** 

### p18  · `setResaleMarketplaceRecommendation`

`PUT /resale-marketplace-recommendation` · ORDER_CREATE · staff · **AI Resale Configuration & Marketplace Recommendations**

> Provide TICVAI's AI intelligence layer for optimizing resale configuration while keeping commercial control with the operator.

**`AiResaleConfigurationMarketplaceRecommendationsView`** — `accept`, `anomalyDetection`, `category`, `demandPrediction`, `expiryRecommendations`, `financialTransaction`, `highDemand`, `ignore`, `listingRecommendations`, `marketplaceOptimization`, `model`, `modify`, `pricingRecommendations`, `sellerRiskRecommendations`, `synchronization`

- serves P09 ADM-287 AI Resale Configuration & Marketplace Recommendations

**Decision:** 

### p21  · `listResale`

`GET /resale` · ORDER_VIEW · staff · **Resale Operations Command Center**

> Provide operations teams with a real-time control center for all resale transactions after listings move into purchase/fulfillment.

**`ResaleOperationsCommandCenterView`** — `buyer`, `buyerTotal`, `completedTransfers`, `credentialReissues`, `credentialStatus`, `disputes`, `event`, `failedTransfers`, `fraudAlerts`, `grossResaleValue`, `holdTransaction`, `listingId`, `originalOrderId`, `originalTicketId`, `ownershipStatus`, `pendingSellerSettlements`, `pendingTransfers`, `purchaseStatus`, `refunds`, `resalePrice`, `resaleTransactionId`, `resaleTransactionsToday`, `riskScore`, `sectionRowSeat`, `seller`, `sellerProceeds`, `settlementStatus`, `settlementValue`, `statusesType`, `transactionDate`, `transactionsUnderReview`, `venue`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-288 Resale Operations Command Center
- serves P09 ADM-297 Resale Analytics & AI Intelligence

**Decision:** 

### p23  · `listBuyerPurchaseResale`

`GET /buyer-purchase-resale` · ORDER_VIEW · staff · **Buyer Purchase & Resale Order Management**

> Manage the buyer-side purchase transaction and ensure that a resale ticket is temporarily protected while checkout occurs.

**`BuyerPurchaseResaleOrderManagementView`** — `automaticRelease`, `billingInformation`, `buyerServiceFee`, `card`, `concurrentBuyerHandling`, `confirmationTransfer`, `customerId`, `email`, `failureHandling`, `holdDuration`, `holdExtensionRules`, `identityVerificationWhereRequired`, `loyaltyProfile`, `membership`, `mobile`, `name`, `otherPermittedCharges`, `paymentAuthorization`, `paymentCapture`, `paymentTimeout`, `resaleTicketPrice`, `supportedAlternativePaymentMethods`, `taxes`, `totalPayable`, `wallet`

- serves P09 ADM-289 Buyer Purchase & Resale Order Management

**Decision:** 

### p25  · `listTicketOwnershipTransfer`

`GET /ticket-ownership-transfer` · ORDER_VIEW · staff · **Ticket Ownership Transfer Management**

> Securely transfer the ticket entitlement from the original seller to the resale buyer.

**`TicketOwnershipTransferManagementView`** — `accessRights`, `addOnsWherePermitted`, `admissionEntitlement`, `associatedBenefits`, `buyerOwnershipActive`, `buyerPaymentCompleted`, `capacityRemainsValid`, `customer`, `entitlements`, `event`, `eventRemainsActive`, `identity`, `listingRemainsValid`, `membershipAccount`, `newResaleOrder`, `noFraudHoldExists`, `originalOrder`, `ownershipStatus`, `product`, `seat`, `seatAssignment`, `sellerOwnershipHistoricalTransferred`, `sellerStillOwnsTicket`, `ticket`, `ticketHasNotBeenRefunded`, `ticketHasNotBeenScanned`, `validity`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-290 Ticket Ownership Transfer Management

**Decision:** 

### p26  · `listCredentialRevocationRegeneration`

`GET /credential-revocation-regeneration` · ORDER_VIEW · staff · **Credential Revocation & Regeneration**

> Ensure the seller's old ticket credential cannot continue to provide access after resale. This is one of the most important security functions in the module.

**`CredentialRevocationRegenerationView`** — `barcode`, `buyerAssociation`, `digitalTicket`, `dynamicQr`, `email`, `mobileApp`, `mobileWalletPass`, `newCredentialId`, `newQr`, `newSecurityKeysTokenWhereApplicable`, `newToken`, `newWalletPassWhereApplicable`, `nfc`, `oldCredentialRevoke`, `originalTicketRelationship`, `otherConfiguredDeliveryMethods`, `revokedResold`, `rfid`, `staticQr`, `ticvaiAccount`, `wallet`, `wearableCredential`

- serves P09 ADM-291 Credential Revocation & Regeneration

**Decision:** 

### p28  · `listResaleFraudDuplicate`

`GET /resale-fraud-duplicate` · ORDER_VIEW · staff · **Resale Fraud & Duplicate Sale Protection**

> Protect TICVAI, venues, sellers and buyers from resale abuse and fraudulent ticket activity.

**`ResaleFraudDuplicateSaleProtectionView`** — `accountDeviceAnomaliesWherePermitted`, `allow`, `credentialReuse`, `duplicatedCredentials`, `highFrequencyResale`, `holdTransaction`, `identityMismatch`, `invalidatedTickets`, `multipleAccounts`, `multipleResaleAttempts`, `paymentAnomalies`, `repeatedFailedTransactions`, `requireManualReview`, `requireVerification`, `revokedSellerCredential`, `sameTicketListedSimultaneously`, `suspiciousPricing`, `unusualSellerVolume`, `withExplainableContributingFactors`

- serves P09 ADM-292 Resale Fraud & Duplicate Sale Protection

**Decision:** 

### p29  · `listCapacityInventoryReconciliation`

`GET /capacity-inventory-reconciliation` · ORDER_VIEW · staff · **Capacity & Inventory Reconciliation**

> Ensure resale activity never creates additional venue capacity or corrupts primary ticket inventory.

**`CapacityInventoryReconciliationView`** — `activeEntitlements`, `cancelledTickets`, `capacityDiscrepancy`, `correctMapping`, `credentialMismatch`, `holdTicket`, `holds`, `investigate`, `ownershipMismatch`, `primaryInventoryRemaining`, `primaryTicketsSold`, `processExplicitlyReturnsIt`, `reSync`, `refundedTickets`, `resaleTicketsSold`, `sellableCapacity`, `soldResaleListingStillActive`, `ticketsListedForResale`, `venueCapacity`

- serves P09 ADM-293 Capacity & Inventory Reconciliation

**Decision:** 

### p30  · `listSellerSettlementPayout`

`GET /seller-settlement-payout` · ORDER_VIEW · staff · **Seller Settlement & Payout Management**

> Manage the financial amount owed to sellers following successful resale.

**`SellerSettlementPayoutManagementView`** — `adjustments`, `afterAccessValidation`, `afterEventCompletion`, `applicableTax`, `commission`, `complianceHold`, `currency`, `expectedPayoutDate`, `immediatelyAfterResale`, `listingPrice`, `manualHold`, `minimumPayoutThreshold`, `operatorDefinedSettlementCycle`, `paymentAccountVerification`, `payoutMethod`, `processingFee`, `refundDisputeHold`, `resaleTransaction`, `seller`, `sellerFee`, `sellerProceeds`, `sellerVerification`, `settlementBatches`, `settlementId`, `settlementStatus`, `statusesType`, `xDaysAfterEvent`, `xDaysAfterResale`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-294 Seller Settlement & Payout Management

**Decision:** 

### p32  · `listRefundDisputeResale`

`GET /refund-dispute-resale` · ORDER_VIEW · staff · **Refunds, Disputes & Resale Exceptions**

> Handle exceptional scenarios that occur after a resale transaction.

**`RefundsDisputesResaleExceptionsView`** — `buyer`, `buyerDispute`, `buyerRefund`, `caseId`, `caseOwner`, `credentialStatus`, `event`, `eventCancellation`, `eventPostponement`, `evidence`, `failedCredentialIssuance`, `failedOwnershipTransfer`, `financialAmount`, `holdSettlement`, `incorrectTicket`, `notes`, `originalOrder`, `paymentChargeback`, `provideReplacementTicket`, `resaleTransaction`, `resolution`, `returnOwnership`, `seatChange`, `seller`, `sellerDispute`, `sellerPayoutDispute`, `settlementStatus`, `sla`, `ticketAccessIssue`, `venueChange`, `whoReceivesTheRefund`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-295 Refunds, Disputes & Resale Exceptions

**Decision:** 

### p34  · `listResaleOwnership`

`GET /resale-ownership` · ORDER_VIEW · staff · **Resale Audit & Ownership History**

> Provide complete end-to-end traceability of every ticket that enters the resale ecosystem.

**`ResaleAuditOwnershipHistoryView`** — `action`, `approval`, `buyer`, `compliance`, `credential`, `customerDispute`, `deviceChannelWhereApplicable`, `event`, `fee`, `finance`, `fraudInvestigation`, `listing`, `order`, `originalOrder`, `ownership`, `payment`, `paymentReference`, `price`, `resaleOrder`, `resaleTransaction`, `seat`, `seller`, `settlement`, `subjectToRolePermissions`, `ticket`, `ticketId`, `timestamp`, `userSystem`, `venueOperations`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-296 Resale Audit & Ownership History

**Decision:** 

### p35  · `listResale2`

`GET /resale-2` · ORDER_VIEW · staff · **Resale Analytics & AI Intelligence**

> Provide management with commercial, operational and predictive intelligence about the resale marketplace.

**`ResaleAnalyticsAiIntelligenceView`** — `andCommercialPolicies`, `averageDiscount`, `averageListingPrice`, `averageMarkup`, `averageResalePrice`, `averageSalePrice`, `averageTimeToSell`, `conversion`, `customerProposition`, `demand`, `engine`, `exceptionsAuditAnalytics`, `expectedConversion`, `expectedListingVolume`, `expectedMarketplaceRevenue`, `expectedResaleDemand`, `expectedResalePrice`, `fraudRate`, `grossResaleValue`, `including`, `listingsToSalesRatio`, `marketplaceRevenue`, `modelAEmbeddedWhiteLabel`, `modelBTicvaiHostedWhiteLabel`, `modelCHeadlessApi`, `monitoring`, `policyPermitsIt`, `primaryAvailability`, `primaryPrice`, `primaryPriceForWeekendPerformances`, `refundDisputeRate`, `resaleAvailability`, `resaleConversionRate`, `resaleTransactions`, `sellThrough`, `sellerProceeds`

> ⚠ **36 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-288 Resale Operations Command Center
- serves P09 ADM-297 Resale Analytics & AI Intelligence

**Decision:** 

### p40  · `listTicketResaleMarketplace`

`GET /ticket-resale-marketplace` · ORDER_VIEW · staff · **My Tickets & Resale Marketplace Entry**

> Provide the authenticated ticket holder with a simple and secure entry point into the official resale journey. The preferred starting point should be the customer's existing: My Account → My Tickets rather than asking customers to manually enter ticket numbers or upload ticket PDFs.

**`MyTicketsResaleMarketplaceEntryView`** — `appAuthentication`, `availableActions`, `brand`, `clientLogo`, `colors`, `customerAccount`, `dateTime`, `eventProduct`, `exchange`, `language`, `marketplaceName`, `otp`, `passwordlessLogin`, `requestRefund`, `resaleStatus`, `resellTicket`, `sectionRowSeat`, `sso`, `supportDetails`, `ticketHolder`, `ticketStatus`, `ticketType`, `typography`, `venue`, `virtualTicketIdReference`

- serves P09 ADM-278 Resale Marketplace Command Center
- serves P09 ADM-298 My Tickets & Resale Marketplace Entry

**Decision:** 

### p42  · `listResaleEligibilityTicket`

`GET /resale-eligibility-ticket` · ORDER_VIEW · staff · **Resale Eligibility & Ticket Selection**

> Explain whether the selected ticket can be resold before allowing a listing to be created.

**`ResaleEligibilityTicketSelectionView`** — `a14`, `a15`, `a16`, `a17`, `adjacentSeatGroup`, `applicableMarketplaceConditions`, `date`, `error5042`, `event`, `eventStatus`, `existingListing`, `fraudSecurityHold`, `membershipRestrictions`, `originalPrice`, `paymentStatus`, `product`, `promotionRestrictions`, `resaleClosingTime`, `resaleWindow`, `scanUseStatus`, `seat`, `sellIndividually`, `sellSelectedTickets`, `sellTogetherOnly`, `ticketOwnership`, `ticketType`, `ticketValidity`, `venue`, `with`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-299 Resale Eligibility & Ticket Selection

**Decision:** 

### p43  · `listCreateListingResale`

`GET /create-listing-resale` · ORDER_VIEW · staff · **Create Listing & Resale Price Selection**

> Allow an eligible seller to select a resale price within the client's approved marketplace rules.

**`CreateListingResalePriceSelectionView`** — `aiRecommendedPrice`, `cappedPrice`, `faceValueOnly`, `fixedPrice`, `operatorControlled`, `recommendedPriceAed215`, `sellerSelectedPrice`

- serves P09 ADM-300 Create Listing & Resale Price Selection

**Decision:** 

### p45  · `listFeeSellerProceed`

`GET /fee-seller-proceed` · ORDER_VIEW · staff · **Fees, Seller Proceeds & Listing Confirmation**

> Provide complete financial transparency before the seller commits to publishing the listing. This is essential to prevent later disputes.

**`FeesSellerProceedsListingConfirmationView`** — `aed000`, `aed2200`, `applicablePrivacyNotice`, `cancellationPolicy`, `clearlyExplainApplicableSettlementRules`, `estimatedProceedsAed198`, `eventCancellationTreatment`, `eventMuseumNight`, `feeAed22`, `marketplaceTerms`, `originalPriceAed200`, `resalePriceAed220`, `seatA18`, `sellerTerms`, `settlementConditions`, `storeTheApplicableTermsVersionAcceptance`, `youWillReceiveAed19800`, `yourSellingPrice`

- serves P09 ADM-283 Resale Fees, Commission & Seller Proceeds
- serves P09 ADM-301 Fees, Seller Proceeds & Listing Confirmation

**Decision:** 

### p46  · `listResaleListingSeller`

`GET /resale-listing-seller` · ORDER_VIEW · staff · **My Resale Listings & Seller Dashboard**

> Give sellers a dedicated self-service workspace to manage their resale activity after publishing.

**`MyResaleListingsSellerDashboardView`** — `acceptAiPriceRecommendation`, `activeListings`, `contactSupport`, `date`, `estimatedProceedsAed198`, `event`, `expiringSoon`, `expiry`, `listingDate`, `listingPrice`, `marketplaceStatus`, `originalPrice`, `paidSettlements`, `pendingApproval`, `pendingSettlement`, `relist`, `seat`, `sellerProceeds`, `sellingPriceAed220`, `settlementScheduledAfterEvent`, `settlementStatus`, `sold`, `viewsWhereApplicable`

- serves P09 ADM-302 My Resale Listings & Seller Dashboard

**Decision:** 

### p48  · `listOfficialResaleMarketplace`

`GET /official-resale-marketplace` · ORDER_VIEW · staff · **Official Resale Marketplace & Buyer Discovery**

> Provide buyers with a trusted client-branded marketplace for discovering authentic resale inventory.

**`OfficialResaleMarketplaceBuyerDiscoveryView`** — `accessibility`, `address`, `andWhereAppropriate`, `asASeparateMarketplacePage`, `date`, `email`, `event`, `mobile`, `name`, `officialTicketsOfficialResale`, `paymentInformation`, `performance`, `price`, `primaryOnly`, `quantity`, `resaleOnly`, `section`, `ticketType`, `venue`

- serves P09 ADM-278 Resale Marketplace Command Center
- serves P09 ADM-303 Official Resale Marketplace & Buyer Discovery

**Decision:** 

### p49  · `listResaleTicketDetail`

`GET /resale-ticket-detail` · ORDER_VIEW · staff · **Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience**

> Allow customers to understand exactly what they are purchasing and distinguish resale inventory from primary inventory.

**`ResaleTicketDetailSeatSelectionPrimaryVsResaleExperiView`** — `accessibilityAttributes`, `applicableBenefits`, `applicableRestrictions`, `event`, `fees`, `integrateWithTicvaiSeatMap`, `officialResalePriceAed220`, `originalFaceValueAed200`, `performance`, `primaryInventoryResaleInventory`, `resalePrice`, `row`, `seat`, `section`, `theCustomerCanChoose`, `ticketType`, `venue`, `whileMaintainingTheirBackendDistinction`

- serves P09 ADM-304 Resale Ticket Detail, Seat Selection & Primary-vs-Resale Experience

**Decision:** 

### p51  · `listBuyerCheckoutInventory`

`GET /buyer-checkout-inventory` · ORDER_VIEW · staff · **Buyer Checkout, Inventory Hold & Secure Payment**

> Provide a normal, secure TICVAI checkout while protecting the resale listing from simultaneous purchase.

**`BuyerCheckoutInventoryHoldSecurePaymentView`** — `architecture`, `billingDetails`, `email`, `mobile`, `name`, `requiredParticipantInformation`

- serves P09 ADM-305 Buyer Checkout, Inventory Hold & Secure Payment

**Decision:** 

### p52  · `listResaleConfirmationOwnership`

`GET /resale-confirmation-ownership` · ORDER_VIEW · staff · **Resale Confirmation, Ownership Transfer & Ticket Delivery**

> Provide the customer-facing completion experience after successful payment while the backend performs the secure entitlement transfer.

**`ResaleConfirmationOwnershipTransferTicketDeliveryView`** — `appleWallet`, `currentOwnerBuyerB`, `currentOwnerSellerA`, `dynamicQr`, `followedBy`, `googleWallet`, `mobileTicket`, `otherSupportedCredentialMedia`, `previousOwnerSellerA`, `rfidNfcAssignmentWhereApplicable`, `settlementStatusPending`, `yourTicketHasBeenSold`, `yourTicketIsReady`

- serves P09 ADM-296 Resale Audit & Ownership History
- serves P09 ADM-306 Resale Confirmation, Ownership Transfer & Ticket Delivery

**Decision:** 

### p54  · `listWhiteLabelMarketplace`

`GET /white-label-marketplace` · ORDER_VIEW · staff · **White-Label Marketplace Deployment & Experience Architecture**

> This is the key architecture/configuration screen It defines how each TICVAI client chooses to expose the resale marketplace to its customers. Deployment Model A — Embedded White-Label

**`WhiteLabelMarketplaceDeploymentExperienceArchitecturView`** — `additionalClientLanguages`, `analytics`, `arabicRtl`, `auditLogging`, `authentication`, `authenticationMethod`, `authorization`, `botProtectionWhereApplicable`, `brandColors`, `buy`, `buyerTerms`, `clientAuthentication`, `clientBranding`, `clientLogo`, `clientNavigation`, `dataProtection`, `deepLinking`, `domainConfiguration`, `domainSubdomain`, `embeddedComponents`, `embeddedPages`, `english`, `fraudIntegration`, `languages`, `legalLinks`, `localization`, `marketplaceName`, `mobileResponsiveBehavior`, `myListings`, `myTickets`, `privacy`, `rateLimiting`, `secureSessions`, `sell`, `sellerTerms`, `sessionExpiry`, `ssoSessionPassing`, `supportContact`, `transactions`, `typography`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-307 White-Label Marketplace Deployment & Experience Architecture

**Decision:** 


---

## Ticket Upgrade, Exchange & Conversion

### p3   · `listUpgradeConversion`

`GET /upgrade-conversion` · ORDER_VIEW · staff · **Upgrade & Conversion Command Center**

> Provide administrators and operations teams with one centralized view of all ticket upgrade, exchange and conversion configurations and operational activity.

**`UpgradeConversionCommandCenterView`** — `activeConversionRules`, `activeUpgradePaths`, `approvalRequirement`, `channel`, `childAdult`, `configurationConflicts`, `conversionsToday`, `dayTicketAnnualPass`, `effectivePeriod`, `eventAEventB`, `expiringRules`, `failedConversions`, `financialMethod`, `generalAdmissionCombinationTicket`, `manualOverrides`, `owner`, `pendingExceptions`, `premiumStandard`, `productsEligibleForUpgrade`, `productsExcluded`, `ruleId`, `ruleName`, `sourceProduct`, `standardPremium`, `status`, `targetProduct`, `transactionType`, `upgradesToday`, `venue`

> ⚠ **29 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-308 Upgrade & Conversion Command Center

**Decision:** 

### p5   · `setUpgradeConversionPath`

`PUT /upgrade-conversion-path` · ORDER_CREATE · staff · **Upgrade & Conversion Path Builder**

> Define exactly which products/tickets may be converted into which other products. This becomes the central conversion relationship engine.

**`UpgradeConversionPathBuilderView`** — `note`

- serves P09 ADM-309 Upgrade & Conversion Path Builder

**Decision:** 

### p7   · `listUpgradeEligibilityQualification`

`GET /upgrade-eligibility-qualification` · ORDER_VIEW · staff · **Upgrade Eligibility & Qualification Rules**

> Determine whether a particular ticket/customer/transaction qualifies for a configured upgrade or conversion path. A path existing does not automatically mean every ticket can use it.

**`UpgradeEligibilityQualificationRulesView`** — `cancelled`, `channel`, `customerSegment`, `customerType`, `event`, `expired`, `location`, `loyaltyTier`, `membership`, `originalPrice`, `partiallyUsed`, `performance`, `previousConversion`, `previousUpgrade`, `product`, `promotionUsed`, `purchaseChannel`, `purchaseDate`, `redemptionHistory`, `suspended`, `ticketStatus`, `ticketType`, `timeslot`, `unused`, `usageStatus`, `used`, `valid`, `venue`, `vipUpgradeEligible`, `vipUpgradeNotAvailable`, `visitDate`, `withReason`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-310 Upgrade Eligibility & Qualification Rules

**Decision:** 

### p9   · `listUpgradeTimingUsage`

`GET /upgrade-timing-usage` · ORDER_VIEW · staff · **Upgrade Timing, Usage & Ticket Status Rules**

> Define how ticket lifecycle state affects upgrade and conversion behavior. This deserves its own screen because a ticket may already have been partially consumed.

**`UpgradeTimingUsageTicketStatusRulesView`** — `afterFirstUse`, `afterVisit`, `andAlreadyVisitedAttractionA`, `beforeExpiry`, `beforeFirstUse`, `beforeVisit`, `duringVisit`, `eligibleWithinGracePeriod`, `exampleAttractionUpgrade`, `gracePeriod`, `invalidate`, `neverEligible`, `partiallyConsumed`, `partiallyRetainEntitlement`, `product`, `remainingBenefits`, `remainingDays`, `remainingStoredValue`, `retainForHistory`, `supersede`, `supervisorExceptionAllowed`, `unusedAdmissions`, `usedAdmissions`

- serves P09 ADM-311 Upgrade Timing, Usage & Ticket Status Rules

**Decision:** 

### p10  · `listUpgradeFinancialTreatment`

`GET /upgrade-financial-treatment` · ORDER_VIEW · staff · **Upgrade Financial Treatment & Price Difference Rules**

> Define how the financial relationship between the old and new product should be treated.

**`UpgradeFinancialTreatmentPriceDifferenceRulesView`** — `basedOnRemainingEntitlement`, `basedOnRemainingValidity`, `configuredRate`, `contractedRate`, `corporateDiscount`, `credit`, `currentSellingPrice`, `customerPaysFullTargetPrice`, `discount`, `fees`, `finalAmount`, `fixedUpgradePrice`, `membershipDiscount`, `membershipRate`, `originalDatePrice`, `priceDifference`, `promotion`, `rounding`, `targetPrice`, `tax`, `thisIsImportant`, `upgradeSpecificRate`, `voucher`

- serves P09 ADM-312 Upgrade Financial Treatment & Price Difference Rules

**Decision:** 

### p12  · `setProRataResidual`

`PUT /pro-rata-residual` · ORDER_CREATE · staff · **Pro-Rata, Residual Value & Entitlement Credit Configuration**

> Handle complex upgrades where part of the original product has already been consumed.

**`ProRataResidualValueEntitlementCreditConfigurationView`** — `annualPasses`, `configuredCommercialAmount`, `memberships`, `multiAttractionProducts`, `multiDayPasses`, `packages`, `remainingCommercialValue`, `remainingDaysOriginalDays`, `remainingUsesTotalUses`, `storedEntitlements`, `valueOfUnconsumedBenefits`

- serves P09 ADM-313 Pro-Rata, Residual Value & Entitlement Credit Configuration

**Decision:** 

### p14  · `listPersonTypeProduct`

`GET /person-type-product` · ORDER_VIEW · staff · **Person-Type, Product & Entitlement Conversion Rules**

> Handle conversions that change more than simply the commercial level of a ticket.

**`PersonTypeProductEntitlementConversionRulesView`** — `added`, `age`, `alreadyConsumed`, `andIdentify`, `childAdult`, `corporateAssociation`, `customPersonTypes`, `differenceCalculatedThroughArea10`, `identityVerification`, `juniorAdult`, `membership`, `otherEligibilityRules`, `removed`, `replaced`, `residency`, `residentTourist`, `retained`, `seniorAdult`, `standardMember`

- serves P09 ADM-314 Person-Type, Product & Entitlement Conversion Rules

**Decision:** 

### p16  · `listBulkGroupAssisted`

`GET /bulk-group-assisted` · ORDER_VIEW · staff · **Bulk, Group & Assisted Upgrade Operations**

> Support operational upgrades involving multiple tickets rather than requiring staff to process each individually.

**`BulkGroupAssistedUpgradeOperationsView`** — `byType`, `changePersonType`, `eligible142`, `notEligible8`, `selected150Tickets`

- serves P09 ADM-315 Bulk, Group & Assisted Upgrade Operations

**Decision:** 

### p18  · `createUpgradeCredentialRegeneration`

`POST /upgrade-credential-regeneration` · ORDER_CREATE · staff · **Upgrade Execution, Credential Regeneration & Channel Controls**

> Control what happens operationally once an upgrade or conversion is approved and financially completed.

**`UpgradeExecutionCredentialRegenerationChannelControlView`** — `allAuthorizedPaths`, `api`, `b2b`, `b2cSelfService`, `boxOffice`, `callCenter`, `confirmationEmail`, `entitlementStatesInconsistent`, `invalidateOldQr`, `kiosk`, `mobileApp`, `newAccessRights`, `newDate`, `newEntitlement`, `newPerformance`, `newZone`, `oldCredentialInvalidation`, `pos`, `preserveExistingCredential`, `regenerateQr`, `reseller`, `smsWhatsappWhereConfigured`, `standardPremiumOnly`, `updatedInvoice`, `updatedReceipt`, `updatedTicket`, `walletPassUpdate`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-316 Upgrade Execution, Credential Regeneration & Channel Controls

**Decision:** 

### p20  · `listUpgradeException`

`GET /upgrade-exception` · ORDER_VIEW · staff · **Upgrade History, Exception Management & Audit Explorer**

> Provide complete operational and financial traceability for every upgrade, downgrade, exchange and conversion.

**`UpgradeHistoryExceptionManagementAuditExplorerView`** — `agent`, `approval`, `architectureForExample`, `channel`, `channelSynchronizationFailure`, `complimentaryUpgrade`, `controls`, `customer`, `dateTime`, `eligibilityOverride`, `eligibleCredit`, `eventAEventB`, `expiredTicketException`, `failedCredentialUpdate`, `failedPaymentReconciliation`, `fees`, `financialOverride`, `manualCredit`, `newTicket`, `order`, `originalTicket`, `originalValue`, `paymentRefund`, `priceDifference`, `reason`, `relationships`, `role`, `rule`, `sourceProduct`, `status`, `supportingNote`, `targetProduct`, `tax`, `timestamp`, `transactionId`, `transactionType`, `user`, `withEachTransactionLinked`

> ⚠ **38 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P09 ADM-317 Upgrade History, Exception Management & Audit Explorer

**Decision:** 

