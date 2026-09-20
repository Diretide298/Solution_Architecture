# access — 146 operations awaiting sign-off

> **These are specified, not unfinished.** Each has a request, a response and a citation of
> the pack page it was read from. `x-ticvai-provisional` means **nobody who has to build it
> has agreed it** — so the only thing that closes one is a decision in this column: *agreed*,
> *corrected* (say how), or *not needed*.

**2 pack(s), read in page order.** A session opens a book and walks it.

- Access Control Module — **116**
- Ticket Media Credential Management — **30**


---

## Access Control Module

### p6   · `listAccess`

`GET /access` · SCOPE_VIEW · staff · **Access Control Command Center**

> Central operational/configuration landing page for the complete Access Control module.

**`AccessControlCommandCenterView`** — `activeAccessPoints`, `attractionGates`, `currentAdmissionRate`, `currentInVenueOccupancy`, `devicesOffline`, `devicesOnline`, `entryGates`, `exitGates`, `failedScans`, `gatesClosed`, `gatesOpen`, `handheldDevices`, `offlineDevices`, `overrides`, `securityAlerts`, `synchronizationStatus`, `totalVenues`, `turnstiles`

- serves P08 BO-144 Access Control Command Center

**Decision:** 

### p7   · `listVenueParkAccess`

`GET /venue-park-access` · SCOPE_VIEW · staff · **Venue & Park Access Structure**

> Define the highest-level physical access hierarchy.

**`VenueParkAccessStructureView`** — `accessControlEnabled`, `arena`, `building`, `capacity`, `code`, `defaultCredentialRules`, `defaultEntryPolicy`, `defaultExitPolicy`, `emergencyBehavior`, `eventSpace`, `exhibition`, `museum`, `name`, `offlinePolicy`, `operatingCalendar`, `parentEntity`, `park`, `stadium`, `supportMultiParkEnvironments`, `temporaryVenue`, `tenant`, `themePark`, `timeZone`, `venue`, `waterpark`

- serves P08 BO-145 Venue & Park Access Structure

**Decision:** 

### p8   · `setAccessAreaZone`

`PUT /access-area-zone` · ACCESS_POINT_CONFIGURE · staff · **Access Area & Zone Builder**

> Divide a venue into controlled access areas.

**`AccessAreaZoneBuilderView`** — `allowedCredentialClasses`, `capacity`, `entryRequirements`, `exitRequirements`, `operatingSchedule`, `securityClassification`, `zoneType`

- serves P08 BO-146 Access Area & Zone Builder

**Decision:** 

### p9   · `setAttractionAccess`

`PUT /attraction-access` · ACCESS_POINT_CONFIGURE · staff · **Attraction Access Configuration**

> Configure attractions as access-controlled destinations.

**`AttractionAccessConfigurationView`** — `adultCompanionRequirement`, `ageRestriction`, `attractionId`, `biometricRequirement`, `capacity`, `entitlementRequirement`, `entryPoints`, `exitPoints`, `fastPassSupport`, `heightRestriction`, `membershipAccess`, `name`, `operatingCalendar`, `temporaryClosureBehavior`, `venue`, `vipAccess`, `zone`

- serves P08 BO-147 Attraction Access Configuration

**Decision:** 

### p11  · `setGateLane`

`PUT /gate-lane` · ACCESS_POINT_CONFIGURE · staff · **Gate & Lane Configuration**

> Configure individual physical gates/lanes.

**`GateLaneConfigurationView`** — `accessPoint`, `bidirectional`, `closed`, `countOnly`, `crossover`, `emergencyDropArm`, `entry`, `exit`, `freeSpin`, `gateId`, `gateName`, `laneNumber`, `location`, `manual`, `reEntry`, `type`, `validation`

- serves P08 BO-149 Gate & Lane Configuration

**Decision:** 

### p12  · `setAccessGraphicalMap`

`PUT /access-graphical-map` · ACCESS_POINT_CONFIGURE · staff · **Access Control Graphical Map Designer**

> Create a graphical digital twin of the access-control environment.

**`AccessControlGraphicalMapDesignerView`** — `ai`, `architecturalDrawing`, `cad`, `image`, `ontoTheMap`, `pdf`, `venuePlan`

- serves P08 BO-150 Access Control Graphical Map Designer

**Decision:** 

### p13  · `listAccessLocationGrouping`

`GET /access-location-grouping` · SCOPE_VIEW · staff · **Access Location Grouping**

> Group multiple access points for operational and capacity purposes. Allow access topology and operating behavior to change by date/time.

**`AccessLocationGroupingView`** — `adventureHallGate`, `coasterGate`, `dropTowerGate`, `freeEntryDays`, `gate01`, `gate02`, `gate03`, `gate04`, `holidays`, `maintenancePeriods`, `normalOperatingDays`, `privateEvents`, `seasonalSchedules`, `weekends`

- serves P08 BO-151 Access Location Grouping

**Decision:** 

### p13  · `listOperatingCalendarSpecial`

`GET /operating-calendar-special` · SCOPE_VIEW · staff · **Operating Calendar & Special Access Days**

> Allow access topology and operating behavior to change by date/time.

**`OperatingCalendarSpecialAccessDaysView`** — `afterHoursEvents`, `ai`, `freeEntryDays`, `holidays`, `ladiesOnlySessions`, `maintenancePeriods`, `normalOperatingDays`, `privateEvents`, `schoolGroupSessions`, `seasonalSchedules`, `specialEvents`, `weekends`

- serves P08 BO-152 Operating Calendar & Special Access Days

**Decision:** 

### p14  · `publishTopologyValidation`

`PUT /topology-validation` · ACCESS_POINT_CONFIGURE · staff · **Topology Validation & Publication**

> Final validation and controlled deployment of access configuration. Before publication, TICVAI automatically validates: orphan gates devices without access points access points without zones incorrect entry/exit direction missing offline configuration conflicting operating calendars inaccessible zones missing emergency…

**`TopologyValidationPublicationView`** — `accessPoint`, `development`, `entireTenant`, `park`, `scanned`, `selectedDevices`, `selectedGates`, `venue`, `withRollbackToPreviousConfiguration`, `zone`

- serves P08 BO-153 Topology Validation & Publication

**Decision:** 

### p17  · `listAccessRule`

`GET /access-rule` · SCOPE_VIEW · staff · **Access Rule Command Center**

> Central configuration dashboard for all access and entitlement rules.

**`AccessRuleCommandCenterView`** — `activeAccessRules`, `draftRules`, `offlineCompatibleRules`, `productsTicketsCovered`, `recentlyModifiedRules`, `rulesAllowingOverride`, `rulesPendingApproval`, `rulesUsingBiometrics`, `rulesWithConflicts`, `scheduledRules`, `upcomingRuleChanges`, `venuesCovered`

- serves P08 BO-154 Access Rule Command Center

**Decision:** 

### p18  · `setVisualAccessRule`

`PUT /visual-access-rule` · ACCESS_POINT_CONFIGURE · staff · **Visual Access Rule Builder**

> Provide a no-code rule engine. This is where TICVAI should become significantly easier to configure than traditional access-control systems.

**`VisualAccessRuleBuilderView`** — `ai`, `at`, `conditionsAreSatisfied`, `exited`, `logic`

- serves P08 BO-155 Visual Access Rule Builder

**Decision:** 

### p19  · `listEntryExitRule`

`GET /entry-exit-rule` · SCOPE_VIEW · staff · **Entry, Exit & Re-entry Rules**

> Configure admission quantity and journey sequencing. The source matrix explicitly requires configurable quantities for entry, exit and same-day re-entry, anti- passback intervals, required exit before re-entry, and required entry before exit.

**`EntryExitReEntryRulesView`** — `allowedNotAllowed`, `designatedGateRequired`, `entry1`, `exitRequired`, `exitRequiredFirst`, `exitScanOptional`, `exitScanRequired`, `maximumReEntries`, `nExits`, `nPerDay`, `nPerPeriod`, `nTimes`, `once`, `reEntry1`, `reEntryGateDesignatedGateOnly`, `reEntryWindow`, `sameDayOnly`, `unlimited`, `unlimitedExit`

- serves P08 BO-156 Entry, Exit & Re-entry Rules

**Decision:** 

### p20  · `listAntiPassbackJourney`

`GET /anti-passback-journey` · SCOPE_VIEW · staff · **Anti-Passback & Journey Sequence**

> Prevent credential sharing and impossible access sequences.

**`AntiPassbackJourneySequenceView`** — `attraction`, `credential`, `entryExitReEntry`, `gate`, `guest`, `mainEntryAttractionEntry`, `park`, `venue`

- serves P08 BO-157 Anti-Passback & Journey Sequence

**Decision:** 

### p21  · `listAccessValidityTime`

`GET /access-validity-time` · SCOPE_VIEW · staff · **Access Validity & Time Rules**

> Determine when access is permitted.

**`AccessValidityTimeRulesView`** — `blackoutDates`, `endOfDay`, `endOfMonth`, `endOfWeek`, `endOfYear`, `eventDates`, `fromTo`, `holidays`, `nDaysAfterActivation`, `nDaysAfterFirstUse`, `nDaysAfterSale`, `offPeakDates`, `peakDates`, `seasons`, `toItsAdmissionPerformanceTime`, `weekdays`, `weekends`

- serves P08 BO-158 Access Validity & Time Rules

**Decision:** 

### p22  · `listEntitlementConsumption`

`GET /entitlement-consumption` · SCOPE_VIEW · staff · **Entitlement Consumption Engine**

> Determine what gets consumed when access is granted. This is critical because one credential may represent several different entitlements. The matrix specifically describes a single QR capable of carrying park admission, ride entitlement, meal voucher, coupon, photo voucher and re-entry rights.

**`EntitlementConsumptionEngineView`** — `attractionAdmission`, `consumptionPerValidation`, `customEntitlement`, `event`, `exampleSilverFastPass`, `experience`, `fastPass`, `locker`, `meal`, `membershipBenefit`, `oneAccessPerRide`, `parkAdmission`, `photo`, `quantity`, `reEntry`, `ride`, `ride1Remaining2`, `ride2Remaining1`, `ride3Remaining0`, `voucher`

- serves P08 BO-159 Entitlement Consumption Engine

**Decision:** 

### p23  · `listMultiParkCrossover`

`GET /multi-park-crossover` · SCOPE_VIEW · staff · **Multi-Park & Crossover Rules**

> Configure complex access between multiple parks/venues. The matrix specifically requires multi-park access on different days, same-day crossover, park-specific entry quantities and conditional access based on previous park admission.

**`MultiParkCrossoverRulesView`** — `allowedParks`, `crossoverQuantity`, `crossoverTime`, `differentDayAccess`, `numberOfParkEntries`, `parkOrder`, `prerequisitePark`, `reEntryAfterCrossover`, `sameDayCrossover`

- serves P08 BO-160 Multi-Park & Crossover Rules
- serves P08 BO-220 Multi-Park & Crossover Journey Orchestrator

**Decision:** 

### p24  · `listGuestCompanionEligibility`

`GET /guest-companion-eligibility` · SCOPE_VIEW · staff · **Guest, Companion & Eligibility Rules**

> Apply access conditions based on guest characteristics and relationships.

**`GuestCompanionEligibilityRulesView`** — `accreditation`, `adult`, `beforeAdmission`, `beforeExit`, `child`, `childA`, `childB`, `customerSegment`, `journeys`, `junior`, `member`, `nanny`, `pod`, `podCompanion`, `senior`, `staff`, `vip`

- serves P08 BO-161 Guest, Companion & Eligibility Rules

**Decision:** 

### p25  · `listGroupAdmissionQuantity`

`GET /group-admission-quantity` · SCOPE_VIEW · staff · **Group Admission & Quantity Validation**

> Handle B2B groups, school groups, tour groups and family/group tickets efficiently. The matrix specifically calls for faster admission for large B2B groups and the ability for one QR/group ticket to represent multiple admissions.

**`GroupAdmissionQuantityValidationView`** — `attendanceIncrement`, `authorizedGuests50`, `authorizedQuantity50`, `entered42`, `entireGroup`, `guestsEnteringNow42`, `individualChildTicketsUnderGroup`, `leaderGuests`, `multipleWaves`, `partialGroup`, `prevalidatedB2bManifest`, `remaining8`, `singleQrMultiEntry`, `storedOnOneDevice`

- serves P08 BO-162 Group Admission & Quantity Validation

**Decision:** 

### p26  · `publishRuleConflictCheck`

`PUT /rule-conflict-check` · ACCESS_POINT_CONFIGURE · staff · **Rule Simulation, Conflict Check & Publication**

> No access rule should reach a live gate without being tested.

**`RuleSimulationConflictCheckPublicationView`** — `adventureParkEnteredAt1400`, `antiPassbackPassed`, `credentialValid`, `crossoverAllowed`, `denyRuleAc284`, `entitlements`, `entryQuantityAvailable`, `exitedAt1730`, `previousParkRequirementMet`, `ruleV10`, `ruleV11`, `ruleV20`, `validatedOfflineAndInvalidated`, `verificationMethodValid`, `visitDateValid`, `waterParkEntitlement`

- serves P08 BO-163 Rule Simulation, Conflict Check & Publication

**Decision:** 

### p29  · `listDigitalCredentialSecurity`

`GET /digital-credential-security` · SCOPE_VIEW · staff · **Digital Credential Security Command Center**

> Central configuration and monitoring page for all secure digital credentials.

**`DigitalCredentialSecurityCommandCenterView`** — `activeDigitalCredentials`, `annualPasses`, `credentialsRevokedToday`, `deviceBoundCredentials`, `digitalPasses`, `dynamicQrEnabled`, `dynamicQrTickets`, `eventCredentials`, `locationProtectedCredentials`, `loyaltyCredentials`, `membershipCredentials`, `mobileWalletCredentials`, `offlineReadyCredentials`, `securityAlerts`, `suspiciousSessions`

- serves P08 BO-164 Digital Credential Security Command Center
- serves P08 BO-173 Credential Security Simulation, Audit & Publication

**Decision:** 

### p30  · `setDynamicSecurityProfile`

`PUT /dynamic-security-profile` · ACCESS_POINT_CONFIGURE · staff · **Dynamic QR Security Profile Builder**

> Configure how a dynamic QR is generated and protected. 30 | Pag e The matrix requires a unique QR per issued ticket/pass and periodic QR refresh to reduce screenshot and duplication fraud.

**`DynamicQrSecurityProfileBuilderView`** — `credentialId`, `cryptographicSignatureKeyReference`, `custom`, `deviceBindingReference`, `dynamic`, `dynamicDeviceBound`, `dynamicLocationBound`, `entitlementPayload`, `nonceOtp`, `refreshEvery30Seconds`, `screens`, `static`, `ticketId`, `timestamp`, `venueContext`

- serves P08 BO-165 Dynamic QR Security Profile Builder

**Decision:** 

### p32  · `listCredentialActivationDisplay`

`GET /credential-activation-display` · SCOPE_VIEW · staff · **Credential Activation & Display Rules**

> Configure when the guest is permitted to see/use the credential. The matrix specifies that after registration, a ticket may appear as a blurred QR and only become clear and usable near the park entrance.

**`CredentialActivationDisplayRulesView`** — `blurQr`, `displayActivationTimer`, `displayCredentialStatus`, `displayDynamicQr`, `displayRemainingEntitlements`, `hideQr`, `showAvailableAtVenue`, `showCountdown`, `showVenueDirections`

- serves P08 BO-166 Credential Activation & Display Rules

**Decision:** 

### p33  · `listDeviceBindingSession`

`GET /device-binding-session` · SCOPE_VIEW · staff · **Device Binding & Session Security**

> Prevent one credential from being shared across unauthorized devices. The source explicitly requires tickets to be linked to a specific device/user and suspicious patterns such as device sharing and multiple simultaneous sessions to be detected.

**`DeviceBindingSessionSecurityView`** — `allowedBeforeFirstUse`, `andSimultaneously`, `appInstallation`, `concurrentSessions`, `credential`, `deviceId`, `deviceReference`, `lastActivation`, `lastKnownVenue`, `maximumActiveDevices`, `notAllowed`, `operatorApprovalRequired`, `os`, `otpVerificationRequired`, `registrationDate`, `securityStatus`, `supervisorApprovalRequired`, `user`

- serves P08 BO-167 Device Binding & Session Security

**Decision:** 

### p34  · `setBleBeaconGeofence`

`PUT /ble-beacon-geofence` · ACCESS_POINT_CONFIGURE · staff · **BLE Beacon & Geofence Configuration**

> Configure location-aware credential activation. This is a major requirement under 3.1.9. The matrix requires BLE beacon proximity and geofence boundaries to activate/deactivate credentials at venue, attraction, zone and gate level.

**`BleBeaconGeofenceConfigurationView`** — `activeInactive`, `andDraws`, `attraction`, `beaconId`, `beaconName`, `gate`, `health`, `lastDetected`, `park`, `proximityThreshold`, `venue`, `zone`

- serves P08 BO-168 BLE Beacon & Geofence Configuration

**Decision:** 

### p35  · `listCredentialTransferRebinding`

`GET /credential-transfer-rebinding` · SCOPE_VIEW · staff · **Credential Transfer & Rebinding**

> Securely manage digital-ticket transfers. The matrix requires tickets to be transferable through email/app, with the recipient required to authenticate before accessing and activating the transferred QR.

**`CredentialTransferRebindingView`** — `beforeFirstValidationOnly`, `numberOfTransfers`, `oldCredentialInvalid`, `oldDeviceBindingRemoved`, `recipientCredentialActiveEligible`, `requireAcceptance`, `requireOtp`, `requireRecipientAccount`, `returnToSender`

- serves P08 BO-169 Credential Transfer & Rebinding

**Decision:** 

### p36  · `listCredentialRevocationLifecycle`

`GET /credential-revocation-lifecycle` · SCOPE_VIEW · staff · **Credential Revocation & Lifecycle Events**

> Immediately invalidate credentials when the underlying ticket changes. Requirement 3.1.4 specifically requires dynamic QR invalidation after refunds, cancellations, transfers, exchanges, upgrades or reissues.

**`CredentialRevocationLifecycleEventsView`** — `accountSuspension`, `cancellation`, `centralPlatform`, `exchange`, `fraudLock`, `gateNetwork`, `manualInvalidation`, `mobileApp`, `offlineRevocationPackage`, `ticketExpiration`, `walletCredentialService`

- serves P08 BO-170 Credential Revocation & Lifecycle Events

**Decision:** 

### p37  · `listOfflineCryptographicValidation`

`GET /offline-cryptographic-validation` · SCOPE_VIEW · staff · **Offline Cryptographic Validation Profile**

> Allow access devices to validate secure credentials without continuous backend connectivity. The matrix explicitly requires offline cryptographic validation and embedded entitlement validation without real-time backend connectivity.

**`OfflineCryptographicValidationProfileView`** — `configurableFallback`, `continueRestrictedValidation`, `credentialAuthenticity`, `credentialStatusSnapshot`, `digitalSignature`, `entitlements`, `failClosed`, `guestCategory`, `operatorWarning`, `park`, `reEntryPermissions`, `reservation`, `seat`, `supervisorMode`, `ticketId`, `ticketType`, `timeWindow`, `timeslot`, `validityPeriod`, `venue`, `visitDate`, `zone`

- serves P08 BO-171 Offline Cryptographic Validation Profile

**Decision:** 

### p38  · `setEmbeddedEntitlementPayload`

`PUT /embedded-entitlement-payload` · ACCESS_POINT_CONFIGURE · staff · **Embedded Entitlement Payload Designer**

> Determine what operational information can be securely carried by the credential for offline decisions. The matrix permits embedded information including ticket type, seat assignment, event ID, venue access rights, timeslot, reservations, locker assignments, membership entitlements, guest category and validity.

**`EmbeddedEntitlementPayloadDesignerView`** — `admission`, `ai`, `attractionPermissions`, `credentialId`, `date`, `expiry`, `fastPass`, `guestCategory`, `locker`, `membership`, `otherPermittedOperationalClaims`, `park`, `reservation`, `seat`, `ticketType`, `time`, `timeslot`, `venue`, `zone`

- serves P08 BO-172 Embedded Entitlement Payload Designer

**Decision:** 

### p39  · `listCredentialSecurity`

`GET /credential-security` · SCOPE_VIEW · staff · **Credential Security Simulation, Audit & Publication**

> Test the complete secure credential lifecycle before production deployment.

**`CredentialSecuritySimulationAuditPublicationView`** — `activation`, `credential`, `device`, `deviceValid`, `dynamicDigitalCredentials`, `entitlementValid`, `gate`, `guestAccountReference`, `location`, `operator`, `qrFreshnessFailed`, `refresh`, `resultReasonCode`, `revocation`, `securityApprovePublish`, `signatureValid`, `ticket`, `timestamp`, `validation`, `venueValid`

- serves P08 BO-164 Digital Credential Security Command Center
- serves P08 BO-173 Credential Security Simulation, Audit & Publication

**Decision:** 

### p44  · `listMediaCredential`

`GET /media-credential` · SCOPE_VIEW · staff · **Media & Credential Command Center**

> Central management page for every media and verification technology supported by Access Control.

**`MediaCredentialCommandCenterView`** — `activeMediaProfiles`, `ai`, `biometricCredentials`, `externalCredentials`, `failedMediaReads`, `mediaSwapsToday`, `nfcCredentials`, `qrCredentials`, `rfidCredentials`, `unknownCredentials`, `verificationExceptions`, `walletCredentials`

- serves P08 BO-174 Media & Credential Command Center

**Decision:** 

### p45  · `listMediaTypeTechnology`

`GET /media-type-technology` · SCOPE_VIEW · staff · **Media Type & Technology Library**

> Define reusable media technologies. The matrix expects support for linear barcode, two-dimensional codes, magnetic strips, contact/proximity RFID, NFC and biometric readers.

**`MediaTypeTechnologyLibraryView`** — `appCredential`, `applicableProducts`, `applicableVenues`, `contact`, `encodingFormat`, `externalBarcode`, `facePass`, `faceTag`, `hotelCard`, `iso15693`, `mobileWallet`, `onlineOfflineCapability`, `otherSupportedStandards`, `paperTicket`, `partnerQr`, `plasticCard`, `proximity`, `qr`, `securityClassification`, `supportedReaderTypes`, `technology`, `thirdPartyCredential`, `wristband`, `writableReadOnly`

- serves P08 BO-175 Media Type & Technology Library
- serves P08 BO-337 Media Type & Credential Technology Registry

**Decision:** 

### p46  · `listVirtualCredentialMedia`

`GET /virtual-credential-media` · SCOPE_VIEW · staff · **Virtual Credential & Media Association**

> Associate one virtual ticket identity with its permitted media representations.

**`VirtualCredentialMediaAssociationView`** — `accessHistory`, `andThereforeToTheSame`, `consumptionState`, `entitlements`, `guest`, `qr8x72`, `resolvesTo`, `rfid298173`, `simultaneously`, `ticket`, `walletCredential827`

- serves P08 BO-174 Media & Credential Command Center
- serves P08 BO-176 Virtual Credential & Media Association

**Decision:** 

### p47  · `listVerificationMethodSelection`

`GET /verification-method-selection` · SCOPE_VIEW · staff · **Verification Method Selection & Locking**

> Control which verification method the guest chooses and when it becomes locked. The matrix specifies that although a ticket may technically support physical card, Dynamic QR, Face Pass and Face Tag, the customer should select one verification method. It may be changed before first successful verification, but after tha…

**`VerificationMethodSelectionLockingView`** — `dynamicQr`, `facePass`, `faceTag`, `guestNotAllowed`, `operationsSupervisorApproval`, `physicalCard`, `reason`, `rfid`, `verificationMethodLocked`

- serves P08 BO-177 Verification Method Selection & Locking

**Decision:** 

### p48  · `listMediaIssuanceEncoding`

`GET /media-issuance-encoding` · SCOPE_VIEW · staff · **Media Issuance & Encoding Profile**

> Configure how ticket identity is written or encoded onto each medium. The source requires ticket IDs to be generated as 2D barcode, QR or RFID and requires randomized, always- unique identifiers to reduce fraud.

**`MediaIssuanceEncodingProfileView`** — `checksumSignatureWhereApplicable`, `credentialIdentifier`, `encodingFormat`, `identifierCollisionCheckEnabled`, `insteadAdministratorsSelectAControlled`, `offlinePayloadProfile`, `randomizationEnabled`, `randomizedMediaIdentifier`, `secureReference`, `secureToken`, `ticketIdReference`

- serves P08 BO-178 Media Issuance & Encoding Profile

**Decision:** 

### p49  · `listMediaSwapReplacement`

`GET /media-swap-replacement` · SCOPE_VIEW · staff · **Media Swap & Replacement**

> Transfer a ticket from one medium to another without changing the underlying virtual ticket. This directly covers the matrix requirement to swap RFID to barcode/QR or vice versa while transferring the attached information.

**`MediaSwapReplacementView`** — `entryHistory`, `fastPassBalance`, `guest`, `membershipAssociation`, `reEntryStatus`, `reasonsType`, `remainingEntitlements`, `reservations`, `ticket`, `to`

- serves P08 BO-179 Media Swap & Replacement

**Decision:** 

### p50  · `setRfidNfc`

`PUT /rfid-nfc` · ACCESS_POINT_CONFIGURE · staff · **RFID & NFC Configuration**

> Provide dedicated configuration for proximity credentials. The matrix requires RFID—including ISO 15693—and NFC, as well as multi-range RFID scanning at near, medium and far ranges.

**`RfidNfcConfigurationView`** — `credential`, `encodingProfile`, `frequencyInterfaceProfile`, `gate`, `journey`, `membership`, `mobileDevice`, `nfcTicket`, `offlineCapability`, `readWriteBehavior`, `readerCompatibility`, `rfidStandard`, `securityProfile`, `supportedReaders`, `tagCardType`, `venue`, `walletCredential`, `zone`

- serves P08 BO-180 RFID & NFC Configuration

**Decision:** 

### p51  · `listExternalPartnerCredential`

`GET /external-partner-credential` · SCOPE_VIEW · staff · **External & Partner Credential Mapping**

> Allow TICVAI Access Control to understand credentials generated by other systems. The matrix explicitly requires reading reseller/external partner ticket formats and barcodes generated by other systems.

**`ExternalPartnerCredentialMappingView`** — `apiValidation`, `cachedValidation`, `dependingOnPolicy`, `hybrid`, `localMapping`, `offlineMapping`, `tokenValidation`

- serves P08 BO-181 External & Partner Credential Mapping

**Decision:** 

### p53  · `listHotelWalletExternal`

`GET /hotel-wallet-external` · SCOPE_VIEW · staff · **Hotel, Wallet & External Media Integration**

> Configure specialized external credential ecosystems. The source specifically requires hotel room-card integration at access points and an interface to the hotel's property-management system for room billing.

**`HotelWalletExternalMediaIntegrationView`** — `accessDecisionProceedsNormally`

- serves P08 BO-182 Hotel, Wallet & External Media Integration

**Decision:** 

### p54  · `publishMediaCompatibilityTesting`

`PUT /media-compatibility-testing` · ACCESS_POINT_CONFIGURE · staff · **Media Compatibility, Testing & Publication**

> Ensure that every configured medium works with the intended access-control hardware before deployment. This is particularly important because the matrix says the solution should operate with hardware selected by the venue, while hardware limitations must be highlighted and recommended equipment exposed for procurement …

**`MediaCompatibilityTestingPublicationView`** — `communicate`, `deviceGroup`, `gate`, `nfc`, `park`, `retentionDeletionAudit`, `rfid`, `tenant`, `theTicketIsFullyRedeemed`, `venue`

- serves P08 BO-183 Media Compatibility, Testing & Publication

**Decision:** 

### p56  · `listBiometricAccess`

`GET /biometric-access` · SCOPE_VIEW · staff · **Biometric Access Command Center**

> Central dashboard for biometric access configuration and operational health.

**`BiometricAccessCommandCenterView`** — `activeFacePassProfiles`, `activeFaceTags`, `ai`, `biometricSecurityAlerts`, `blockedFaceChanges`, `cameraReaderHealth`, `enrollmentsToday`, `failedVerifications`, `manualReviews`, `profilesPendingDeletion`, `reEnrollmentRequests`, `successfulFaceVerifications`

- serves P08 BO-184 Biometric Access Command Center

**Decision:** 

### p58  · `setBiometricVerificationProfile`

`PUT /biometric-verification-profile` · ACCESS_POINT_CONFIGURE · staff · **Biometric Verification Profile Builder**

> Configure which ticket/credential types can or must use biometric verification. The matrix specifically requires biometric checks to be configurable by ticket type, including memberships, annual passes, multi-day and multi-attraction products.

**`BiometricVerificationProfileBuilderView`** — `attraction`, `attractionsCredentialOnly`, `facePass`, `faceTag`, `gate`, `mainEntryFaceRequired`, `park`, `selectType`, `supportedFutureBiometricProvider`, `venue`, `vipLoungeFaceRequired`, `zone`

- serves P08 BO-185 Biometric Verification Profile Builder

**Decision:** 

### p59  · `setFacePassEnrollment`

`PUT /face-pass-enrollment` · ACCESS_POINT_CONFIGURE · staff · **Face Pass Enrollment Configuration**

> Configure persistent Face Pass registration. The source specifies that Face Pass may be registered through the App, ticket counters or Annual Pass counter.

**`FacePassEnrollmentConfigurationView`** — `accountLoginRequired`, `alreadyAssociatedWith`, `annualPassCounter`, `enrollmentExpiry`, `identityCheckRequired`, `minimumImageQuality`, `numberOfCaptureAttempts`, `operatorVerification`, `otherAuthorizedChannel`, `selfServiceKiosk`, `ticketCounter`, `ticvaiApp`, `validTicketPassRequired`

- serves P08 BO-186 Face Pass Enrollment Configuration

**Decision:** 

### p60  · `listBiometricConsentGuardian`

`GET /biometric-consent-guardian` · SCOPE_VIEW · staff · **Biometric Consent & Guardian Management**

> Manage consent requirements associated with persistent biometric enrollment. The matrix requires App users to provide consent before Face Pass registration and requires guardian consent for minors. On-site enrollment also requires consent before facial data is captured.

**`BiometricConsentGuardianManagementView`** — `channel`, `consentRecordId`, `consentRecordMayBeRetained`, `countryJurisdiction`, `credential`, `enrollmentChannel`, `from`, `guardianReferenceWhereApplicable`, `guestCategory`, `operatorWhereApplicable`, `policyVersion`, `tenant`, `timestamp`, `venue`, `withdrawalDeletionStatus`

- serves P08 BO-187 Biometric Consent & Guardian Management

**Decision:** 

### p61  · `listFaceTagTemporary`

`GET /face-tag-temporary` · SCOPE_VIEW · staff · **Face Tag Temporary Enrollment**

> Configure the temporary biometric model separately from Face Pass. The matrix describes Face Tag as temporarily stored facial data, enrollable at ticket counters or entry gates, with biometric data permanently deleted once the associated ticket is fully redeemed.

**`FaceTagTemporaryEnrollmentView`** — `alternativeConfigurableTriggersWherePermitted`, `credentialCancellation`, `endOfVisit`, `entryGate`, `operationalRetentionThreshold`, `temporaryCredential`, `ticket`, `ticketCounter`, `ticketExpiration`, `visit`

- serves P08 BO-188 Face Tag Temporary Enrollment

**Decision:** 

### p62  · `listFaceMatchingVerification`

`GET /face-matching-verification` · SCOPE_VIEW · staff · **Face Matching & Verification Thresholds**

> Configure biometric verification behavior. The source requires a configurable Biometric Check Level determining the scoring of biometric comparison.

**`FaceMatchingVerificationThresholdsView`** — `captureTimeout`, `duplicateFaceCheck`, `imageQuality`, `livenessCheck`, `maskObstructionHandling`, `operatorFallback`, `venuePolicy`

- serves P08 BO-189 Face Matching & Verification Thresholds

**Decision:** 

### p63  · `listFaceChangeEnrollment`

`GET /face-change-enrollment` · SCOPE_VIEW · staff · **Face Change, Re-enrollment & Identity Protection**

> Prevent guests from replacing a registered biometric identity with another person's face. The source explicitly states that customers may re-register Face Pass, but the system must compare the new facial data with the previous profile. If the difference exceeds an acceptable threshold, the update is blocked and venue a…

**`FaceChangeReEnrollmentIdentityProtectionView`** — `auditHistory`, `credential`, `existingProfileReference`, `guest`, `matchResult`, `newCaptureReference`, `operator`, `previousChanges`, `reasonForReEnrollment`, `reasonsType`

- serves P08 BO-190 Face Change, Re-enrollment & Identity Protection

**Decision:** 

### p65  · `listBiometricValidationGate`

`GET /biometric-validation-gate` · SCOPE_VIEW · staff · **Biometric Validation at Gate**

> Configure how facial verification interacts with the physical access-control journey.

**`BiometricValidationAtGateView`** — `biometricMatchValidAccess`, `decisionReturned`

- serves P08 BO-191 Biometric Validation at Gate

**Decision:** 

### p66  · `listBiometricLifecycleRetention`

`GET /biometric-lifecycle-retention` · SCOPE_VIEW · staff · **Biometric Lifecycle, Retention & Deletion**

> Manage biometric-data lifecycle and deletion rules.

**`BiometricLifecycleRetentionDeletionView`** — `abandonedRegistrations`, `activeCredential`, `alreadyValidatedUsingFacePass`, `facePass`, `faceTag`, `failedEnrollmentCaptures`, `reasonShown`, `temporaryCaptures`, `verificationMethod`

- serves P08 BO-192 Biometric Lifecycle, Retention & Deletion

**Decision:** 

### p67  · `listBiometric`

`GET /biometric` · SCOPE_VIEW · staff · **Biometric Simulation, Audit & Publication**

> Test biometric configurations before live deployment.

**`BiometricSimulationAuditPublicationView`** — `accessEntitlementValid`, `alternativeVerificationFallback`, `cameraUnavailable`, `childAssignedAdult`, `credentialResolved`, `credentialType`, `faceMismatch`, `faceProfileActive`, `faceTagDeleted`, `faceTagExpired`, `gateGroup`, `hardware`, `livenessFailure`, `lowConfidenceMatch`, `matchPolicySatisfied`, `noBiometricProfile`, `offlineBiometricScenario`, `park`, `reEnrollmentAttempt`, `required`, `tenant`, `ticketValid`, `validFacePass`, `venue`, `verificationPolicySatisfied`, `withAppropriateFallbackRules`

> ⚠ **26 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-193 Biometric Simulation, Audit & Publication

**Decision:** 

### p70  · `listDeviceGate`

`GET /device-gate` · SCOPE_VIEW · staff · **Device & Gate Command Center**

> Provide the central operational/configuration view of the complete access-control hardware estate.

**`DeviceGateCommandCenterView`** — `ai`, `biometricReaders`, `cameraHealthWhereApplicable`, `configurationVersion`, `connectivity`, `controllerHealth`, `credentialSecurityPackageVersion`, `degraded`, `devicesRequiringSync`, `firmwareSoftwareExceptions`, `gatesClosed`, `gatesOpen`, `handhelds`, `hardwareAlerts`, `lastHeartbeat`, `localRuleVersion`, `offline`, `online`, `rfidNfcReaders`, `scannerHealth`, `totalDevices`, `turnstiles`

- serves P08 BO-194 Device & Gate Command Center

**Decision:** 

### p72  · `listDeviceTypeHardware`

`GET /device-type-hardware` · SCOPE_VIEW · staff · **Device Type & Hardware Library**

> Create reusable hardware definitions independently from physical deployed devices.

**`DeviceTypeHardwareLibraryView`** — `accessiblePodGate`, `androidHandheld`, `beacon`, `biometric`, `buggyGate`, `cameraController`, `connectivity`, `counter`, `deviceCategory`, `firmwareSoftwareInformation`, `fullHeight`, `iosDevice`, `lightCapability`, `manufacturer`, `model`, `multiTechnology`, `nfc`, `offlineCapability`, `paymentCapabilityWhereAvailable`, `podium`, `qrBarcode`, `relayControllerSupport`, `rfid`, `screenCapability`, `soundCapability`, `speedGate`, `staffGate`, `standard`, `standardTurnstiles`, `supportedExternalAccessDevice`, `supportedTechnologies`, `tablet`, `tripod`, `vipGate`, `wideLane`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-195 Device Type & Hardware Library

**Decision:** 

### p73  · `listPhysicalDeviceRegistration`

`GET /physical-device-registration` · SCOPE_VIEW · staff · **Physical Device Registration & Provisioning**

> Register actual deployed hardware and connect it to the Board 1 topology.

**`PhysicalDeviceRegistrationProvisioningView`** — `accessPoint`, `accessRules`, `configuration`, `controllerReference`, `deviceId`, `gateAssignment`, `gateLane`, `hardwareModel`, `installationDate`, `ipNetworkReference`, `manufacturer`, `mediaProfiles`, `operatingMode`, `park`, `serialNumber`, `tenant`, `useControlledDeviceCertificates`, `useControlledDeviceCredentials`, `venue`, `whilePreserving`, `zone`

- serves P08 BO-196 Physical Device Registration & Provisioning

**Decision:** 

### p74  · `setTurnstileLaneBehavior`

`PUT /turnstile-lane-behavior` · ACCESS_POINT_CONFIGURE · staff · **Turnstile & Lane Behavior Configuration**

> Configure how each turnstile or lane behaves. The matrix specifically requires software on turnstiles to behave differently according to card/ticket type and supports different operating modes.

**`TurnstileLaneBehaviorConfigurationView`** — `attraction`, `closed`, `countOnly`, `crossover`, `emergency`, `entry`, `entryExit`, `exit`, `fastPass`, `freeSpin`, `group`, `incompletePassageBehavior`, `passThroughTimeout`, `reEntry`, `relockBehavior`

- serves P08 BO-197 Turnstile & Lane Behavior Configuration

**Decision:** 

### p76  · `setValidationOutcomeGuest`

`PUT /validation-outcome-guest` · ACCESS_POINT_CONFIGURE · staff · **Validation Outcome & Guest Feedback Designer**

> Configure what the physical access device does and displays after validation. The matrix explicitly requires valid/non-valid messages, lights, pictograms and sounds, including green/yellow/red behavior.

**`ValidationOutcomeGuestFeedbackDesignerView`** — `alertSound`, `customMessage`, `denialSound`, `gateOpen`, `gateRemainsControlled`, `gateRemainsLocked`, `greenLight`, `operatorPrompt`, `pictogram`, `reasonCode`, `redAccessDenied`, `redLight`, `successTone`, `yellowLight`

- serves P08 BO-198 Validation Outcome & Guest Feedback Designer

**Decision:** 

### p77  · `setReaderScannerPeripheral`

`PUT /reader-scanner-peripheral` · ACCESS_POINT_CONFIGURE · staff · **Reader, Scanner & Peripheral Configuration**

> Configure the technologies attached to a gate/device.

**`ReaderScannerPeripheralConfigurationView`** — `whereSupported`, `yellowOperatorVerification`

- serves P04 POS-016 Till Configuration
- serves P08 BO-199 Reader, Scanner & Peripheral Configuration

**Decision:** 

### p78  · `setHandheldMobileAccess`

`PUT /handheld-mobile-access` · ACCESS_POINT_CONFIGURE · staff · **Handheld & Mobile Access Device Configuration**

> Configure mobile access-control devices used by staff. The matrix explicitly requires handheld devices and Android/iOS dedicated mobile applications.

**`HandheldMobileAccessDeviceConfigurationView`** — `androidIos`, `assignedOperatorGroup`, `assignedVenue`, `assignedZone`, `biometricCapabilityWhereSupported`, `changeDeviceMode`, `crossover`, `deviceType`, `entry`, `exit`, `groupAdmission`, `manualAttendance`, `offlineCapability`, `permittedOperatingModes`, `preventsFurtherTrustedAccessTransactions`, `reEntry`, `scanGroupAdmission`, `scanTicket`, `scannerSource`

- serves P08 BO-200 Handheld & Mobile Access Device Configuration

**Decision:** 

### p79  · `listGateModeFree`

`GET /gate-mode-free` · SCOPE_VIEW · staff · **Gate Modes, Free Spin & Emergency Controls**

> Manage non-standard operational modes. The source specifically requires Free Spin and Drop Arm/Emergency behavior.

**`GateModesFreeSpinEmergencyControlsView`** — `automaticNotification`, `closed`, `credentialReadingOff`, `crossover`, `emergencyCode`, `entry`, `exit`, `gateGroup`, `incidentRecord`, `reEntry`, `reason`, `turnstileRotationCountOn`, `venueScope`, `whoCanActivate`

- serves P08 BO-201 Gate Modes, Free Spin & Emergency Controls

**Decision:** 

### p81  · `setDeviceSoftwareContent`

`PUT /device-software-content` · ACCESS_POINT_CONFIGURE · staff · **Device Software, Content & Remote Configuration**

> Centrally control access-control device software and guest-facing configuration. The source requires the ability to configure/manage software on turnstiles, add external webpages on supported screens, and enable payment technologies where available.

**`DeviceSoftwareContentRemoteConfigurationView`** — `deviceSettings`, `emergencyInformation`, `externalApprovedWebpage`, `gateMode`, `instructions`, `language`, `localRules`, `mediaProfiles`, `offlineSecurityConfiguration`, `outcomeProfiles`, `promotionalInformation`, `readerSettings`, `reasonMessage`, `ticketStatus`, `uiContent`, `welcomePage`

- serves P08 BO-202 Device Software, Content & Remote Configuration

**Decision:** 

### p82  · `listHardwareCompatibilityHealth`

`GET /hardware-compatibility-health` · SCOPE_VIEW · staff · **Hardware Compatibility, Health, Testing & Deployment**

> Provide the final testing and governance layer before hardware is used in production. The matrix says venues may select their hardware, while the provider must expose hardware limitations and recommendations.

**`HardwareCompatibilityHealthTestingDeploymentView`** — `board2AccessRules`, `board6PhysicalExecution`, `deviceGroup`, `disappears`, `distribute`, `issues`, `localValidation`, `nfc`, `offline`, `pilotDeployment`, `rfid`, `rollback`, `scheduledRollout`, `selectedGates`, `sounds`, `synchronize`, `venue`

- serves P08 BO-203 Hardware Compatibility, Health, Testing & Deployment

**Decision:** 

### p86  · `listOfflineEdge`

`GET /offline-edge` · SCOPE_VIEW · staff · **Offline & Edge Operations Command Center**

> Provide a real-time overview of offline readiness across the entire access-control estate.

**`OfflineEdgeOperationsCommandCenterView`** — `credentialDefinitionsAvailable`, `currentlyOffline`, `currentlyOnline`, `deviceStorageHealthy`, `devicesInDegradedMode`, `edgeNodesOnline`, `lastSynchronizationSuccessful`, `offlineReadyDevices`, `offlineSecurityAlerts`, `packagesCurrent`, `packagesExpiring`, `pendingOfflineTransactions`, `revocationDataCurrent`, `rulesCached`, `verificationMaterialCurrent`

- serves P08 BO-204 Offline & Edge Operations Command Center

**Decision:** 

### p87  · `setEdgeNodeLocal`

`PUT /edge-node-local` · ACCESS_POINT_CONFIGURE · staff · **Edge Node & Local Processing Configuration**

> Configure where local access decisions are processed when central services cannot be reached.

**`EdgeNodeLocalProcessingConfigurationView`** — `deviceGroup`, `edgeNodeId`, `embeddedDeviceProcessing`, `failure`, `lastHeartbeat`, `localProcessingAtGateLevel`, `mobileOfflineProcessing`, `network`, `processingMode`, `redundancy`, `securityStatus`, `softwareVersion`, `storageAllocation`, `tenant`, `venue`

- serves P08 BO-205 Edge Node & Local Processing Configuration

**Decision:** 

### p89  · `listEdgePackageData`

`GET /edge-package-data` · SCOPE_VIEW · staff · **Edge Package & Data Distribution**

> Define what configuration and operational data is securely distributed to edge devices.

**`EdgePackageDataDistributionView`** — `accessRules`, `calendars`, `credentialSecurityParameters`, `deviceAuthorized`, `devices`, `entitlementDefinitions`, `gateResponses`, `gates`, `languages`, `mediaProfiles`, `operatorPermissions`, `packageComplete`, `reasonCodes`, `revocationInformation`, `signatureValid`, `trustedVerificationMaterial`, `venues`, `verificationProfiles`, `version`, `versionValid`, `zones`

- serves P08 BO-207 Edge Package & Data Distribution

**Decision:** 

### p90  · `listOfflineCredentialRevocation`

`GET /offline-credential-revocation` · SCOPE_VIEW · staff · **Offline Credential & Revocation Cache**

> Manage the local information required to reject credentials that should no longer be usable. This is especially important because Board 3 requires refunded, cancelled, transferred, exchanged, upgraded and reissued credentials to be invalidated.

**`OfflineCredentialRevocationCacheView`** — `canTrigger`, `cancellation`, `continue`, `continueWithWarning`, `denySelectedCredentialClasses`, `failClosed`, `fraudLock`, `lostCredential`, `manualInvalidation`, `restrictedProductsOnly`, `supervisorMode`

- serves P08 BO-208 Offline Credential & Revocation Cache

**Decision:** 

### p91  · `listOfflineEntitlementUsage`

`GET /offline-entitlement-usage` · SCOPE_VIEW · staff · **Offline Entitlement & Usage Ledger**

> Track entitlement consumption while the central system is unavailable. This is necessary for tickets such as: 3 Fast Pass uses 1 park entry 1 meal 1 re-entry where usage can occur during an outage.

**`OfflineEntitlementUsageLedgerView`** — `credential`, `decision`, `device`, `entitlement`, `fastPassRemaining3`, `gate`, `localSequence`, `offlineAllowedMaximum1`, `operator`, `packageVersion`, `quantity`, `rideA1`, `rideB1`, `shareCurrentUsageState`, `timestamp`

- serves P08 BO-209 Offline Entitlement & Usage Ledger

**Decision:** 

### p93  · `listConnectivityFailureDegraded`

`GET /connectivity-failure-degraded` · SCOPE_VIEW · staff · **Connectivity Failure & Degraded Mode Policy**

> Configure how devices transition from normal online operation to offline/degraded operation.

**`ConnectivityFailureDegradedModePolicyView`** — `centralServicesReachable`, `onlyDeviceLocalProcessingAvailable`, `someServicesUnavailable`

- serves P08 BO-210 Connectivity Failure & Degraded Mode Policy

**Decision:** 

### p94  · `listReconnectionSynchronizationConflict`

`GET /reconnection-synchronization-conflict` · SCOPE_VIEW · staff · **Reconnection, Synchronization & Conflict Resolution**

> Synchronize everything that occurred offline when connectivity returns.

**`ReconnectionSynchronizationConflictResolutionView`** — `centralRemainingBalanceBeforeOutage`, `configuredBusinessRule`, `earliestTransactionWins`, `entitlementEvents682`, `entries3240`, `exits1204`, `overrides18`, `pendingScans4821`, `preserveBothFlag`, `returnOnline`, `securityEvents7`, `securityInvestigation`, `supervisorReview`

- serves P08 BO-211 Reconnection, Synchronization & Conflict Resolution

**Decision:** 

### p95  · `simulateOfflineResilienceTesting`

`PUT /offline-resilience-testing` · ACCESS_POINT_CONFIGURE · staff · **Offline Simulation & Resilience Testing**

> Allow venues to prove that their access environment will survive outages before opening to guests.

**`OfflineSimulationResilienceTestingView`** — `antiPassbackEnforced`, `attendanceStoredLocally`, `dynamicQrVerifiedLocally`, `entryEntitlementVerified`, `gateOpens`, `ticketDateVerified`, `transactionQueued`

- serves P08 BO-212 Offline Simulation & Resilience Testing

**Decision:** 

### p96  · `listEdgeSecurityDeployment`

`GET /edge-security-deployment` · SCOPE_VIEW · staff · **Edge Security, Audit & Deployment**

> Govern the complete offline/edge environment.

**`EdgeSecurityAuditDeploymentView`** — `authorizedDevices`, `configurationChanges`, `definesTheUnderlyingRules`, `deviceConfiguration`, `deviceGroup`, `edgeCertificates`, `edgeCluster`, `edgeCredentials`, `edgePackageDefinitions`, `failedPackageValidation`, `gateGroup`, `individualDevice`, `offlineOverrideActivity`, `offlineRules`, `packageSignatures`, `park`, `processesOnSpecialDates`, `revokedDevices`, `rollbackToV47`, `securityPolicy`, `tenant`, `theCloudGoesDown`, `thisTicketAllows3Entries`, `unauthorizedConnectionAttempts`, `v47`, `v48Tonight0200`, `venue`, `venueEdgeActive`, `venueExecutives`, `whereOperationallyAppropriate`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-213 Edge Security, Audit & Deployment

**Decision:** 

### p101 · `listGuestJourney`

`GET /guest-journey` · SCOPE_VIEW · staff · **Guest Journey Command Center**

> Central configuration and monitoring screen for all special and multi-person admission journeys.

**`GuestJourneyCommandCenterView`** — `activeJourneyProfiles`, `companionViolations`, `crossoverExceptions`, `crossoversToday`, `delayedGroups`, `familyJourneys`, `fastPassAnomalies`, `fastPassValidations`, `groupArrivalsToday`, `guestsViaGroupAdmission`, `incompleteGroupEntry`, `journeyExceptions`, `reEntryGuests`, `specialEventAdmissions`, `unusuallyHighManualIntervention`, `vipAdmissions`

- serves P08 BO-214 Guest Journey Command Center
- serves P08 BO-780 Guest Engagement Journeys

**Decision:** 

### p102 · `setGroupAdmissionProfile`

`PUT /group-admission-profile` · ACCESS_POINT_CONFIGURE · staff · **Group & B2B Admission Profile Builder**

> Group & B2B Admission Profile Builder

**`GroupB2bAdmissionProfileBuilderView`** — `camps`, `corporateGroups`, `entireGroup`, `events`, `families`, `groupBarcode`, `groupLeaderCredential`, `groupRfid`, `hybrid`, `individualCredentials`, `individualScan`, `leaderQuantity`, `manifestBased`, `multipleWaves`, `partialGroup`, `purchasedGuests`, `resellers`, `schools`, `singleGroupQr`, `tourOperators`, `travelGroups`

- serves P08 BO-215 Group & B2B Admission Profile Builder

**Decision:** 

### p103 · `listGroupLeaderFast`

`GET /group-leader-fast` · SCOPE_VIEW · staff · **Group Leader & Fast B2B Validation**

> Solve the specific matrix requirement for faster entrance flow when large B2B groups have multiple tickets stored on one device.

**`GroupLeaderFastB2bValidationView`** — `accessRules`, `attendance`, `booking`, `group120Guests`, `groupProduct`, `manifest`, `payment`, `remaining`, `visitDate`

- serves P08 BO-216 Group Leader & Fast B2B Validation

**Decision:** 

### p104 · `listGroupAttendancePartial`

`GET /group-attendance-partial` · SCOPE_VIEW · staff · **Group Attendance & Partial Entry Manager**

> Manage actual attendance when fewer guests arrive than the quantity purchased. The matrix explicitly requires the scanner to show the exact group size and allow the operator to enter actual attendants so daily attendance is updated correctly.

**`GroupAttendancePartialEntryManagerView`** — `device`, `entered43`, `gate`, `group`, `guestsArriving`, `leader`, `operator`, `previouslyEntered0`, `purchased50`, `quantity`, `remaining`, `remaining7`, `time`, `totalEntered`

- serves P08 BO-217 Group Attendance & Partial Entry Manager

**Decision:** 

### p105 · `listFamilyChildPod`

`GET /family-child-pod` · SCOPE_VIEW · staff · **Family, Child, POD & Companion Journey**

> Configure linked-person access journeys. The matrix requires child protection through adult-ticket pairing or biometric validation of the assigned adult. It also requires POD accompanying persons and nannies to be bound to a primary guest and only enter when accompanied by that guest.

**`FamilyChildPodCompanionJourneyView`** — `groupLeaderGroupMember`, `guardianMinor`, `otherAuthorizedRelationships`, `parentChild`, `podCompanion`, `primaryGuestNanny`

- serves P08 BO-218 Family, Child, POD & Companion Journey

**Decision:** 

### p106 · `listEntryTemporaryExit`

`GET /entry-temporary-exit` · SCOPE_VIEW · staff · **Re-entry & Temporary Exit Journey**

> Manage guests temporarily leaving and returning to the venue. 106 | Pa ge The source matrix requires configurable re-entry and also describes a journey using a designated re-entry gate with both ticket verification and a UV stamp.

**`ReEntryTemporaryExitJourneyView`** — `additionalVerification`, `antiPassback`, `correctGate`, `credentialFace`, `credentialOnly`, `credentialOperator`, `credentialUvStamp`, `customSupportedMethod`, `maximum`, `previousEntry`, `reEntryEntitlement`, `reEntryQuantity`, `validExit`

- serves P08 BO-219 Re-entry & Temporary Exit Journey

**Decision:** 

### p108 · `listMultiParkCrossover2`

`GET /multi-park-crossover-2` · SCOPE_VIEW · staff · **Multi-Park & Crossover Journey Orchestrator**

> Operationalize the multi-park rules configured in Board 2. The matrix specifically distinguishes crossover from normal entry and re-entry and requires crossover to be tracked separately.

**`MultiParkCrossoverJourneyOrchestratorView`** — `adventureParkInside`, `crossover`, `maximum`, `normalEntry`, `reEntry`, `waterParkCrossoverAvailable`

- serves P08 BO-160 Multi-Park & Crossover Rules
- serves P08 BO-220 Multi-Park & Crossover Journey Orchestrator

**Decision:** 

### p109 · `listFastPassAttraction`

`GET /fast-pass-attraction` · SCOPE_VIEW · staff · **Fast Pass & Attraction Access Journey**

> Configure the operational experience for limited and unlimited priority-access entitlements. The matrix requires Silver Fast Pass to support three accesses and Gold to support unlimited access with an optional one-access-per-ride restriction.

**`FastPassAttractionAccessJourneyView`** — `eligibleType`, `eligibleYes`, `previousUse1032`, `rideCoaster`, `totalUses`

- serves P08 BO-221 Fast Pass & Attraction Access Journey

**Decision:** 

### p110 · `listSpecialEventFree`

`GET /special-event-free` · SCOPE_VIEW · staff · **Special Event, Free View & Alternative Admission**

> Configure temporary/special admission processes that differ from normal venue access. The matrix requires special-event products capable of capturing attendance without physical admission, N- person attendance entered through a turnstile/tablet/handheld, and Free View days where main gates are open while attraction gat…

**`SpecialEventFreeViewAlternativeAdmissionView`** — `attendance`, `exampleFreeViewDay`, `exampleSpecialEvent`, `on`

- serves P08 BO-222 Special Event, Free View & Alternative Admission

**Decision:** 

### p116 · `listLiveAccess`

`GET /live-access` · SCOPE_VIEW · staff · **Live Access Operations Command Center**

> Provide the venue control room with a real-time view of access operations across all gates, parks, zones, and attractions.

**`LiveAccessOperationsCommandCenterView`** — `activeGates`, `activeOperationalAlerts`, `averageValidationTime`, `groupGate`, `guestsCurrentlyInPark`, `guestsEnteredToday`, `guestsExited`, `guestsMinute`, `lastScan4SecAgo`, `mainGate01`, `mainGate02`, `mainGate03`, `mainGate04`, `modeEntry`, `offlineGates`, `overrides`, `queueModerate`, `reEntryGate`, `rejected3`, `rejectedScans`, `statusOnline`, `throughput31GuestsMin`, `valid92`, `validScans`, `vipGate`, `yellow5`, `yellowInterventionScans`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-224 Live Access Operations Command Center

**Decision:** 

### p117 · `listPodiumConsole`

`GET /podium-console` · SCOPE_VIEW · staff · **Podium Operations Console**

> Provide the operational interface described in the matrix for attendants controlling one or more turnstiles.

**`PodiumOperationsConsoleView`** — `changeGateMode`, `gate01Entry`, `gate02Entry`, `gate03Entry`, `gate04Entry`, `gate05Closed`, `gate06Group`, `gates0106`, `groupAdmission`, `handheld`, `manualValidate`, `otherAuthorizedOperationalInterface`, `physicalKeyboardControlPanel`, `rescan`, `saraM`, `tablet`, `ticketLookup`, `workstation`

- serves P08 BO-225 Podium Operations Console

**Decision:** 

### p118 · `listTicketCredentialInvestigation`

`GET /ticket-credential-investigation` · SCOPE_VIEW · staff · **Ticket & Credential Investigation Console**

> Allow operators to quickly investigate why a guest cannot enter.

**`TicketCredentialInvestigationConsoleView`** — `clerk`, `dynamicQrLocked`, `guestJohnSmith`, `lockerL284`, `mealVoucherAvailable`, `parkEntryUsed`, `paymentMethod`, `paymentReference`, `pos`, `salesChannel`, `transactionTime`, `visitDate01Sep2026`

- serves P08 BO-226 Ticket & Credential Investigation Console

**Decision:** 

### p120 · `listValidationExceptionReason`

`GET /validation-exception-reason` · SCOPE_VIEW · staff · **Validation Exception & Reason Code Manager**

> Standardize what happens when access is not automatically granted. The matrix requires the scanner to display a reason code when a ticket is invalid.

**`ValidationExceptionReasonCodeManagerView`** — `allowWithWarning`, `alreadyUsed`, `deny`, `operatorReview`, `supervisorRequired`, `ticketDate02Sep2026`, `verificationMismatch`

- serves P08 BO-227 Validation Exception & Reason Code Manager

**Decision:** 

### p121 · `approveManualOverrideSupervisor`

`PUT /manual-override-supervisor` · ACCESS_POINT_CONFIGURE · staff · **Manual Override & Supervisor Approval**

> Allow authorized staff to bypass selected access restrictions when operationally justified. The matrix explicitly requires Allow Override and operator-based ticket override.

**`ManualOverrideSupervisorApprovalView`** — `ahmedK`, `gateOpens`, `guestScans`, `originalResultDenied`, `overrideApproved`, `selectType`

- serves P08 BO-228 Manual Override & Supervisor Approval

**Decision:** 

### p122 · `listCredentialDisableBlacklist`

`GET /credential-disable-blacklist` · SCOPE_VIEW · staff · **Credential Disable, Blacklist & Whitelist Operations**

> Provide immediate operational security control over individual credentials.

**`CredentialDisableBlacklistWhitelistOperationsView`** — `attractionAccess`, `blacklistWhitelistCapability`, `centralPlatform`, `dependingOnPolicy`, `entireCredential`, `exceptions`, `fastPass`, `manualTicketInvalidation`, `offlineRevocationPackage`, `onlineGates`, `permanent`, `reEntry`, `reason`, `specificEntitlement`, `to`, `untilDate`, `untilEndOfDay`, `untilManuallyRestored`, `untilTime`, `venueAccess`, `venueEdge`

- serves P08 BO-229 Credential Disable, Blacklist & Whitelist Operations

**Decision:** 

### p124 · `listLiveGateMode`

`GET /live-gate-mode` · SCOPE_VIEW · staff · **Live Gate Mode & Lane Control**

> Allow operations to change access-point modes during live operations without entering the Board 6 engineering configuration. Board 6 defines which modes a device can support. Board 9 controls which permitted mode it is currently running.

**`LiveGateModeLaneControlView`** — `affectedGates`, `closed`, `countOnly`, `crossover`, `currentMode`, `effectiveTime`, `entry`, `exit`, `fastPass`, `freeSpin`, `group`, `operator`, `reEntry`, `reason`, `safetyControls`, `selectType`, `targetMode`

- serves P08 BO-230 Live Gate Mode & Lane Control

**Decision:** 

### p125 · `listQueueThroughputLane`

`GET /queue-throughput-lane` · SCOPE_VIEW · staff · **Queue, Throughput & Lane Optimization**

> Manage entrance flow in real time. This addresses the matrix requirement to improve entrance flow and queuing, particularly for large B2B groups.

**`QueueThroughputLaneOptimizationView`** — `activeLanes`, `family`, `fastPass`, `g01Standard2821Healthy`, `g02Standard3118Healthy`, `g03Group4709Healthy`, `g04Standard12142Investigate`, `groupB2b`, `guestsWaiting`, `podAccessible`, `reEntry`, `standard`, `vip`

- serves P08 BO-231 Queue, Throughput & Lane Optimization

**Decision:** 

### p127 · `setOperationalIncidentException`

`PUT /operational-incident-exception` · ACCESS_POINT_CONFIGURE · staff · **Operational Incident & Exception Workspace**

> Manage access incidents that require more than a simple override.

**`OperationalIncidentExceptionWorkspaceView`** — `accessJourney`, `accessSupervisor`, `credentialHistory`, `gateDevice`, `guestServices`, `operator`, `reasonCodes`, `relevantSecurityAlerts`, `scanHistory`, `security`, `technicalSupport`, `ticketStatus`, `ticketing`, `typesType`

- serves P08 BO-232 Operational Incident & Exception Workspace

**Decision:** 

### p128 · `listShiftHandoverSummary`

`GET /shift-handover-summary` · SCOPE_VIEW · staff · **Operations Audit, Shift Handover & Control Summary**

> Provide full accountability for everything operators and supervisors changed during live access operations.

**`OperationsAuditShiftHandoverControlSummaryView`** — `abnormalRejectionRates`, `blacklistChanges`, `blacklistedCredentials`, `credentialDisables`, `credentialFraudIncidentUnderInvestigation`, `device`, `disabledGates`, `exceptionReport`, `gate08RfidIntermittent`, `gateModeChangeReport`, `grantedRightNow`, `groupAdjustments`, `incidentReport`, `incidents`, `login`, `logout`, `manualOpenings`, `modeChanges`, `offlineDevices`, `operator`, `operatorActivityReport`, `outcomes`, `overrides`, `permissionAware`, `podium`, `reEntryGate02TemporarilyClosed`, `role`, `schoolGroupExpected1615`, `shiftReport`, `ticketLookups`, `unresolvedIncidents`, `unusualOverrideVolumes`

> ⚠ **32 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-233 Operations Audit, Shift Handover & Control Summary

**Decision:** 

### p133 · `listDynamicAccessPolicy`

`GET /dynamic-access-policy` · SCOPE_VIEW · staff · **Dynamic Access Policy Command Center**

> Provide central governance and visibility over all dynamic access policies.

**`DynamicAccessPolicyCommandCenterView`** — `activePolicies`, `aiRecommendations`, `allowDecisions`, `denyDecisions`, `draftPolicies`, `expiringPolicies`, `policiesPendingApproval`, `policiesTriggeredToday`, `policyConflicts`

- serves P08 BO-234 Dynamic Access Policy Command Center

**Decision:** 

### p134 · `listAccessAttributeCatalog`

`GET /access-attribute-catalog` · SCOPE_VIEW · staff · **Access Attribute Catalog**

> Define the attributes available to the TICVAI policy engine. This becomes the reusable data dictionary for dynamic access decisions.

**`AccessAttributeCatalogView`** — `accreditation`, `age`, `attraction`, `capacity`, `companionRelationship`, `countryResidencyWhereApplicable`, `credentialStatus`, `customerSegment`, `date`, `day`, `department`, `employee`, `entitlements`, `event`, `gate`, `genderWhereLegallyBusinessPermitted`, `groupType`, `guestCategory`, `jobFunction`, `loyaltyTier`, `mediaType`, `membership`, `occupancy`, `operatingCalendar`, `park`, `performance`, `podStatus`, `resource`, `restrictedArea`, `role`, `season`, `securityClearance`, `shift`, `specialDay`, `ticketType`, `time`, `venue`, `verificationMethod`, `visitDate`, `zone`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-235 Access Attribute Catalog

**Decision:** 

### p136 · `setVisualDynamicPolicy`

`PUT /visual-dynamic-policy` · ACCESS_POINT_CONFIGURE · staff · **Visual Dynamic Policy Builder**

> Provide a no-code interface for constructing contextual access policies.

**`VisualDynamicPolicyBuilderView`** — `allow`, `deny`, `requireBiometric`, `requireCompanion`, `requireId`, `requireSupervisor`, `review`

- serves P08 BO-236 Visual Dynamic Policy Builder

**Decision:** 

### p137 · `setContextTimeEvent`

`PUT /context-time-event` · ACCESS_POINT_CONFIGURE · staff · **Context, Time, Event & Capacity Policy Builder**

> Configure policies driven by changing venue conditions rather than only guest attributes.

**`ContextTimeEventCapacityPolicyBuilderView`** — `date`, `day`, `event`, `holiday`, `mayEnterSpecifiedZones`, `monitor`, `normal`, `operatingCalendar`, `performance`, `restrict`, `season`, `specialEvent`, `time`

- serves P08 BO-237 Context, Time, Event & Capacity Policy Builder

**Decision:** 

### p139 · `listIdentityMembershipAccreditation`

`GET /identity-membership-accreditation` · SCOPE_VIEW · staff · **Identity, Membership & Accreditation Policies**

> Configure policies based on who the requesting person is.

**`IdentityMembershipAccreditationPoliciesView`** — `annualPassHolder`, `automaticallyExpiresAfterward`, `backstage`, `contractor`, `emergencyServices`, `employee`, `eventStaff`, `financeOffice`, `guest`, `media`, `member`, `memberLounge`, `performer`, `priorityEntrance`, `productionZone`, `security`, `selectedAttractions`, `staffEntrance`, `until`, `vendor`, `vip`, `vipHospitality`

- serves P08 BO-238 Identity, Membership & Accreditation Policies

**Decision:** 

### p140 · `listPolicyScopeHierarchy`

`GET /policy-scope-hierarchy` · SCOPE_VIEW · staff · **Policy Scope, Hierarchy & Inheritance**

> Govern how policies apply across TICVAI's multi-tenant and multi-venue architecture.

**`PolicyScopeHierarchyInheritanceView`** — `applies`, `appliesOnly`, `appliesTo`, `denyOverridesAllow`, `explicitResolution`, `highestPriorityWins`, `mandatoryParentWins`, `mostSpecificWins`

- serves P08 BO-239 Policy Scope, Hierarchy & Inheritance

**Decision:** 

### p142 · `listAuthorizationGovernanceTemporary`

`GET /authorization-governance-temporary` · SCOPE_VIEW · staff · **Authorization Governance & Temporary Access**

> Apply enterprise governance principles to privileged and temporary access.

**`AuthorizationGovernanceTemporaryAccessView`** — `adventureParkPolicies`, `approvalRequirements`, `approver`, `at`, `cannot`, `delegatedAdministration`, `duration`, `expiringGrants`, `fullAudit`, `leastPrivilege`, `reason`, `resortGlobalSecurityPolicy`, `scope`, `segregationOfDuties`, `temporaryAccess`, `with`

- serves P08 BO-240 Authorization Governance & Temporary Access

**Decision:** 

### p143 · `listPolicyEvaluationArchitecture`

`GET /policy-evaluation-architecture` · SCOPE_VIEW · staff · **Policy Evaluation Architecture & Offline Distribution**

> Define where and how policies are evaluated. This screen connects Board 10 with the offline/edge architecture already configured in Board 7.

**`PolicyEvaluationArchitectureOfflineDistributionView`** — `centralUnavailable`, `evaluatedAtVenueEdge`, `evaluatedLocallyWhereSupported`

> ⚠ **1 of 3 property names read as sentences** rather than fields — likely the pack's bullets (triggers, behaviours) taken as a directory: `evaluatedLocallyWhereSupported`

- serves P08 BO-241 Policy Evaluation Architecture & Offline Distribution

**Decision:** 

### p144 · `simulatePolicyConflictImpact`

`PUT /policy-conflict-impact` · ACCESS_POINT_CONFIGURE · staff · **Policy Simulation, Conflict & Impact Analysis**

> Test policies before they affect live guest admission.

**`PolicySimulationConflictImpactAnalysisView`** — `accessAllowed`, `affectedProducts`, `affectedVenues`, `estimatedGuestsImpacted`, `goldMembersAllow`, `hierarchy`, `occupancy`, `pass`, `policiesInvolved`, `priority`, `resultingDecision`

- serves P08 BO-242 Policy Simulation, Conflict & Impact Analysis
- serves P08 BO-981 Conflict & Impact Simulation

**Decision:** 

### p151 · `listAccessSecurityFraud`

`GET /access-security-fraud` · SCOPE_VIEW · staff · **Access Security & Fraud Command Center**

> Provide security teams with a real-time command center for access-related fraud and suspicious activity across all venues.

**`AccessSecurityFraudCommandCenterView`** — `activeInvestigations`, `activeSecurityAlerts`, `biometricAlerts`, `blacklistedCredentials`, `credentialsLockedToday`, `critical`, `deviceSharingAlerts`, `fraudPrevented`, `highRisk`, `highRiskCredentials`, `lowRisk`, `mediumRisk`, `suspiciousQrActivity`, `unusuallyHighReEntryAttemptsDetected`

- serves P08 BO-244 Access Security & Fraud Command Center

**Decision:** 

### p152 · `listFraudDetectionRule`

`GET /fraud-detection-rule` · SCOPE_VIEW · staff · **Fraud Detection Rule & Signal Library**

> Configure the signals TICVAI uses to identify suspicious access behavior.

**`FraudDetectionRuleSignalLibraryView`** — `abnormalDeviceChanges`, `abnormalFastPassConsumption`, `abnormalTransferFrequency`, `antiPassbackViolations`, `applicableCredentialTypes`, `applicableVenues`, `credentialCopied`, `deviceBindingMismatch`, `excessiveAttractionUse`, `excessiveQrActivations`, `excessiveRefreshAttempts`, `expiredCredential`, `faceMismatch`, `gateA1002`, `gateB1003`, `impossibleDeviceMovement`, `invalidSignature`, `multipleActiveSessions`, `multipleDevices`, `multipleIdentitiesLinked`, `newDevice`, `offlineAvailability`, `podNannyRelationshipAnomalies`, `repeatedFailedValidation`, `repeatedWrongGateAttempts`, `response`, `revokedCredential`, `rootedCompromisedDeviceWhereDetectable`, `scope`, `screenshotReplayAttempt`, `severity`, `simultaneousUse`, `suspiciousCompanionChanges`, `suspiciousScannerDeviceActivity`, `threshold`, `timeWindow`, `unusualCrossover`, `unusualFaceChange`, `unusualReEntry`, `weight`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-245 Fraud Detection Rule & Signal Library

**Decision:** 

### p154 · `listCredentialSharingConcurrent`

`GET /credential-sharing-concurrent` · SCOPE_VIEW · staff · **Credential Sharing & Concurrent Usage Detection**

> Detect one of the most important access-control fraud scenarios: One valid ticket being shared by multiple people or devices.

**`CredentialSharingConcurrentUsageDetectionView`** — `additionalDevices`, `increaseRisk`, `iphoneDeviceA`, `maximumActiveDevices`, `requireBiometric`, `requireId`, `requireOperator`, `securityAlert`

- serves P08 BO-246 Credential Sharing & Concurrent Usage Detection

**Decision:** 

### p155 · `listUnifiedIdentityCredential`

`GET /unified-identity-credential` · SCOPE_VIEW · staff · **Unified Identity & Credential Lock Manager**

> Provide the single security lock required by the matrix so suspicious activity can immediately stop all access associated with an identity.

**`UnifiedIdentityCredentialLockManagerView`** — `centralPlatform`, `dynamicQr`, `endOfDay`, `facePass`, `fastPass`, `guestJohnSmith`, `membership`, `mobileDevices`, `nHours`, `offlineRevocationPackage`, `onlineGates`, `permanent`, `rfidWristbandRf8291`, `selectType`, `ticketVc18274`, `untilInvestigationComplete`, `untilManuallyReleased`, `venueEdge`, `walletCredential`

- serves P08 BO-247 Unified Identity & Credential Lock Manager

**Decision:** 

### p156 · `listBiometricIdentityIntegrity`

`GET /biometric-identity-integrity` · SCOPE_VIEW · staff · **Biometric & Identity Integrity Monitoring**

> Detect suspicious biometric and identity-related changes without duplicating Board 5's biometric configuration. Board 5 configures biometrics. Board 11 monitors biometric security risk.

**`BiometricIdentityIntegrityMonitoringView`** — `approval`, `changeDate`, `currentVerification`, `faceChanged`, `location`, `newBiometricReference`, `oldBiometricReference`, `operator`, `reEnrollment`, `reason`, `repeatedFaceMismatch`, `successfulVisits`, `suspiciousEnrollmentFrequency`, `unusualVerificationFailures`, `verificationProcess`

- serves P08 BO-248 Biometric & Identity Integrity Monitoring

**Decision:** 

### p158 · `listRelationshipCompanionFraud`

`GET /relationship-companion-fraud` · SCOPE_VIEW · staff · **Relationship & Companion Fraud Monitoring**

> Detect abuse involving linked guests such as: Child + Adult POD + Companion Guest + Nanny Group Leader + Group Membership dependents.

**`RelationshipCompanionFraudMonitoringView`** — `accessDenial`, `biometricVerification`, `childEntersExitsWithUnauthorizedAdult`, `companionChangedDuringVisit`, `differentCompanionBAttemptedEntry`, `excessiveRelationshipChanges`, `idVerification`, `relationshipChangeAttempt`, `securityEscalation`, `supervisorVerification`, `yellowIntervention`

- serves P08 BO-249 Relationship & Companion Fraud Monitoring

**Decision:** 

### p159 · `listAccessRiskScoring`

`GET /access-risk-scoring` · SCOPE_VIEW · staff · **Access Risk Scoring & Decision Engine**

> Convert multiple security signals into a unified access risk score.

**`AccessRiskScoringDecisionEngineView`** — `accessZone`, `credentialType`, `criticalLockSecurityReview`, `event`, `faceMismatch15`, `historicalBehavior`, `impossibleTravel25`, `multipleSessions20`, `newDevice10`, `previousFailedAttempts12`, `product`, `ticketValue`, `time`, `venue`

- serves P08 BO-250 Access Risk Scoring & Decision Engine

**Decision:** 

### p161 · `setRealTimeSecurity`

`PUT /real-time-security` · ACCESS_POINT_CONFIGURE · staff · **Real-Time Security Response & Playbook Builder**

> Configure what TICVAI automatically does when security conditions are detected.

**`RealTimeSecurityResponsePlaybookBuilderView`** — `after`, `alertOnly`, `blacklist`, `fullIdentityLock`, `increaseRiskScore`, `requireAdditionalVerification`, `requireSupervisor`, `temporarilyLock`

- serves P08 BO-251 Real-Time Security Response & Playbook Builder

**Decision:** 

### p162 · `setSecurityInvestigationEvidence`

`PUT /security-investigation-evidence` · ACCESS_POINT_CONFIGURE · staff · **Security Investigation & Evidence Workspace**

> Provide security specialists with a deeper investigation environment than Board 9's operational incident workspace.

**`SecurityInvestigationEvidenceWorkspaceView`** — `biometricEvents`, `blacklist`, `blacklistEvents`, `clearRisk`, `companionRelationships`, `credentialHistory`, `critical91`, `deviceIds`, `gate`, `mediaChanges`, `operatorIntervention`, `overrides`, `posTicketTransactionReference`, `qrActivations`, `scanRecords`, `securityPolicies`

- serves P08 BO-252 Security Investigation & Evidence Workspace

**Decision:** 

### p164 · `listSecurityDetectionGovernance`

`GET /security-detection-governance` · SCOPE_VIEW · staff · **Security Analytics, AI Detection & Governance**

> Provide long-term intelligence on fraud patterns, security controls and effectiveness.

**`SecurityAnalyticsAiDetectionGovernanceView`** — `abusiveCompromisedOrFraudulent`, `aiRecommendations`, `averageInvestigationTime`, `averageResponseTime`, `b2b12`, `biometricAlerts`, `blacklistHits`, `blacklistPolicies`, `board10DynamicPolicy`, `board3CredentialSecurity`, `board5BiometricAccess`, `board9LiveOperations`, `companionViolations`, `contextualConditions`, `credentialSharing`, `detectionRate`, `deviceBindingViolations`, `estimatedFraudPrevented`, `falsePositiveIndicator`, `financialExposure`, `fraudAttempts`, `fraudRules`, `identityLocks`, `operatorOverrideRate`, `patternImproveControls`, `pos3`, `preventedFraud`, `recurringFraudRate`, `resellerX41`, `resellerY7`, `responsePlaybooks`, `riskModels`, `securityOverrides`, `thresholds`, `web8`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-253 Security Analytics, AI Detection & Governance
- serves P16 ANL-070 Analytics Governance, Security & Audit Center

**Decision:** 

### p168 · `listAccessMonitoring`

`GET /access-monitoring` · SCOPE_VIEW · staff · **Access Monitoring & Analytics Command Center**

> Provide a single executive and operational overview of access performance across all TICVAI-controlled venues.

**`AccessMonitoringAnalyticsCommandCenterView`** — `activeGates`, `averageValidationTime`, `avgValidation`, `crossovers`, `currentlyInVenue`, `entries`, `exits`, `fastPassUses`, `groupAdmissions`, `interventionRate`, `offlineDevices`, `reEntries`, `rejectedScans`, `totalAdmissions`, `totalAdmissionsToday`, `validScans`

- serves P08 BO-254 Access Monitoring & Analytics Command Center

**Decision:** 

### p170 · `listLiveVenueOccupancy`

`GET /live-venue-occupancy` · SCOPE_VIEW · staff · **Live Venue Occupancy & People Counting**

> Provide real-time people counting and occupancy using entry and exit events.

**`LiveVenueOccupancyPeopleCountingView`** — `adventureZone`, `capacity`, `critical`, `current`, `exits`, `high`, `kidsZone`, `normal`, `occupancy`, `operationalAdjustments`, `vipZone`, `warning`

- serves P08 BO-255 Live Venue Occupancy & People Counting

**Decision:** 

### p171 · `listGraphicalAccessMap`

`GET /graphical-access-map` · SCOPE_VIEW · staff · **Graphical Access Map & Live Gate Performance**

> Turn the graphical access topology created in Board 1 into a live operational analytics map.

**`GraphicalAccessMapLiveGatePerformanceView`** — `attractionAccess`, `critical`, `crossoverPoints`, `entryPoints`, `exitPoints`, `gates`, `groupGates`, `guests`, `healthy`, `offline`, `reEntryGates`, `reject`, `success`, `turnstiles`, `vipGates`, `warning`, `yellow`

- serves P08 BO-256 Graphical Access Map & Live Gate Performance

**Decision:** 

### p172 · `listAttendanceAdmission`

`GET /attendance-admission` · SCOPE_VIEW · staff · **Attendance & Admission Analytics**

> Provide detailed reporting of who actually attended compared with tickets sold/reserved. This is particularly important because group admission may differ from purchased quantity.

**`AttendanceAdmissionAnalyticsView`** — `actualAttendance`, `attendance`, `attendanceRate`, `attended`, `channel`, `customerSegment`, `dateTime`, `eligible`, `event`, `groupAttendance`, `membershipAttendance`, `noShowRate`, `noShows`, `purchased`, `repeatEntry`, `sold`, `ticketType`, `ticketsEligibleToday`, `ticketsScanned`, `ticketsSold`, `uniqueGuests`

- serves P08 BO-257 Attendance & Admission Analytics

**Decision:** 

### p174 · `listEntryExitCrossover`

`GET /entry-exit-crossover` · SCOPE_VIEW · staff · **Entry, Exit, Re-entry & Crossover Analytics**

> Analyze complete guest movement across the access journey.

**`EntryExitReEntryCrossoverAnalyticsView`** — `averageTimeOutside`, `crossoverProduct`, `crossoverTime`, `crossoverUtilization`, `mostUsedReEntryGates`, `parkAParkB`, `parkBParkA`, `reEntryByProduct`, `reEntryRate`, `rejectedReEntry`, `waterPark`

- serves P08 BO-258 Entry, Exit, Re-entry & Crossover Analytics

**Decision:** 

### p175 · `listThroughputQueueValidation`

`GET /throughput-queue-validation` · SCOPE_VIEW · staff · **Throughput, Queue & Validation Performance Analytics**

> Measure the operational efficiency of gates and validation devices.

**`ThroughputQueueValidationPerformanceAnalyticsView`** — `averageGateCycle`, `averageScanTime`, `downtime`, `g011482039s1208`, `g021391042s1411`, `g03821081s8264`, `gate03Underperforming`, `gateGuestsHrValidationRejectIntervention`, `guestsPerHour`, `guestsPerMinute`, `manualInterventionRate`, `reasonsType`, `successRate`, `yellowRate`

- serves P08 BO-259 Throughput, Queue & Validation Performance Analytics

**Decision:** 

### p176 · `listValidationOutcomeRejection`

`GET /validation-outcome-rejection` · SCOPE_VIEW · staff · **Validation Outcome & Rejection Analytics**

> Analyze why guests are denied or require manual intervention.

**`ValidationOutcomeRejectionAnalyticsView`** — `overrides`, `rejected`

- serves P08 BO-260 Validation Outcome & Rejection Analytics

**Decision:** 

### p177 · `listGuestDwellTime`

`GET /guest-dwell-time` · SCOPE_VIEW · staff · **Guest Dwell Time, Length of Stay & Attraction Flow**

> Use access events to understand how guests move through and use the venue.

**`GuestDwellTimeLengthOfStayAttractionFlowView`** — `attractionVisits`, `averageLengthOfStay`, `fastPass`, `fastPassUsage`, `medianStay`, `peakArrival`, `peakDeparture`, `reEntryBehavior`, `repeatVisits`, `totalValidations`, `uniqueGuests`, `unnecessary`, `zoneDwellTime`

- serves P08 BO-261 Guest Dwell Time, Length of Stay & Attraction Flow

**Decision:** 

### p179 · `listAccessReportScheduled`

`GET /access-report-scheduled` · SCOPE_VIEW · staff · **Access Reports, Scheduled Reporting & Data Export**

> Provide configurable operational and management reports.

**`AccessReportsScheduledReportingDataExportView`** — `apiDataFeed`, `biIntegration`, `channel`, `csv`, `dashboard`, `date`, `device`, `event`, `fieldLevelRestrictions`, `gate`, `park`, `partner`, `pdf`, `product`, `rbac`, `retentionRules`, `tenant`, `tenantIsolation`, `ticketType`, `venue`, `xlsx`, `zone`

- serves P08 BO-262 Access Reports, Scheduled Reporting & Data Export

**Decision:** 

### p180 · `listAccessExecutiveInsight`

`GET /access-executive-insight` · SCOPE_VIEW · staff · **AI Access Intelligence, Forecasting & Executive Insights**

> Turn access-control data into proactive operational intelligence. This should be the final intelligence screen of the entire Access Control module.

**`AiAccessIntelligenceForecastingExecutiveInsightsView`** — `currentPlanned`, `deviceCapacity`, `expectedAttendance`, `forecastAiRecommend`, `gateDemand`, `groupArrivalPressure`, `peakArrivalTime`, `peakExitTime`, `reEntryDemand`, `tomorrowSAttendance`, `venueOccupancy`, `zoneOccupancy`

- serves P08 BO-263 AI Access Intelligence, Forecasting & Executive Insights

**Decision:** 


---

## Ticket Media Credential Management

### p4   · `listVirtualTicket`

`GET /virtual-ticket` · SCOPE_VIEW · staff · **Virtual Ticket Command Center**

> Provide administrators and operations teams with a centralized view of all Virtual Tickets and their associated media across TICVAI. This is the primary administrative entry point into the Virtual Ticket architecture.

**`VirtualTicketCommandCenterView`** — `active`, `bindMedia`, `cancelled`, `credentialSynchronizationIssues`, `customerAhmedHassan`, `diagnoseCredential`, `eventPerformance`, `expired`, `lastCredentialActivity`, `lastModified`, `media4`, `mediaBindingExceptions`, `numberOfLinkedMedia`, `orderReference`, `partiallyConsumed`, `pendingActivation`, `primaryMedia`, `product`, `productVipConcert`, `reactivate`, `revoked`, `seatA18`, `seatResourceWhereApplicable`, `statusActive`, `suspended`, `ticketHolder`, `ticketStatus`, `ticketType`, `totalVirtualTickets`, `usageStatus`, `usedConsumed`, `validFromTo`, `virtualTicketId`, `virtualTicketsWithMultipleMedia`

> ⚠ **34 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-334 Virtual Ticket Command Center

**Decision:** 

### p6   · `setVirtualTicketIdentity`

`PUT /virtual-ticket-identity` · ACCESS_POINT_CONFIGURE · staff · **Virtual Ticket Identity & Master Record Configuration**

> Define the authoritative Virtual Ticket object used throughout TICVAI. This screen is extremely important because the Virtual Ticket—not the QR/RFID/card— is the master ticket record.

**`VirtualTicketIdentityMasterRecordConfigurationView`** — `accessEntitlement`, `consumptionModel`, `customer`, `deviceChanges`, `entitlementModel`, `entitlements`, `event`, `faceEnrollmentChanges`, `fulfillmentStatus`, `holderAssignmentRequirements`, `idGenerationPattern`, `mediaReplacement`, `mediaRequirements`, `membership`, `order`, `orderLine`, `participant`, `performanceTimeslot`, `priceSnapshot`, `product`, `productVersion`, `qrRegeneration`, `reservation`, `resource`, `rfid77812Vt009821`, `rfid99142Vt009821`, `rfidReplacement`, `seat`, `suspended`, `theVirtualTicketRemainsUnchanged`, `ticketClassification`, `ticketHolder`, `ticketOwnershipModel`, `ticketReprint`, `transferabilityReference`, `valid`, `validity`, `validityModel`, `venue`, `walletUpdates`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-335 Virtual Ticket Identity & Master Record Configuration

**Decision:** 

### p8   · `listVirtualTicketStatus`

`GET /virtual-ticket-statu` · SCOPE_VIEW · staff · **Virtual Ticket Status & Lifecycle Model**

> Configure the standardized lifecycle of a Virtual Ticket independently from the lifecycle of individual media.

**`VirtualTicketStatusLifecycleModelView`** — `accessUsage`, `api`, `appleWalletActive`, `authorizedOperator`, `blocked`, `cancellation`, `cancelled`, `expiry`, `faceActive`, `from`, `membership`, `orderManagement`, `qrActive`, `refunded`, `reissuedSuperseded`, `rfidLostRevoked`, `scheduledProcess`, `suspended`, `theTicketItselfRemainsValid`, `ticketTransfer`, `transferred`, `voided`, `withGovernedAlternativeStates`

- serves P08 BO-334 Virtual Ticket Command Center
- serves P08 BO-336 Virtual Ticket Status & Lifecycle Model

**Decision:** 

### p9   · `listMediaTypeCredential`

`GET /media-type-credential` · SCOPE_VIEW · staff · **Media Type & Credential Technology Registry**

> Maintain the centralized catalogue of credential technologies supported by TICVAI. This makes the credential architecture extensible rather than hard-coded.

**`MediaTypeCredentialTechnologyRegistryView`** — `appleWallet`, `barcode`, `category`, `customWearable`, `dynamicQr`, `faceRecognitionReference`, `generationMethod`, `googleWallet`, `integrationAdapter`, `mediaTypeId`, `membershipCard`, `mobileTicket`, `name`, `nfcCard`, `nfcWristband`, `pdf`, `printedTicket`, `provider`, `qr`, `rfidCard`, `rfidIsTheTechnologyMediaType`, `rfidWristband`, `supportedChannels`, `supportedDevices`, `supportsDynamicUpdate`, `supportsEncryption`, `supportsExpiration`, `supportsOfflineReference`, `supportsReplacement`, `supportsRevocation`, `supportsSigning`, `supportsVisualDesign`, `technology`, `tenantDefinedIntegrationBasedCredentialTechnology`, `thermalTicket`, `tokenFormat`, `validationMechanism`

> ⚠ **37 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-174 Media & Credential Command Center
- serves P08 BO-337 Media Type & Credential Technology Registry

**Decision:** 

### p11  · `listMultiMediaBinding`

`GET /multi-media-binding` · SCOPE_VIEW · staff · **Multi-Media Binding & Association Rules**

> Configure how one Virtual Ticket can be associated with multiple media simultaneously. This is one of the most important screens in Area 15.

**`MultiMediaBindingAssociationRulesView`** — `accessEnvironment`, `age`, `allowedMedia`, `appleWallet`, `backupMedia`, `channel`, `country`, `customerType`, `dynamicQr`, `event`, `exclusiveActivation`, `face`, `googleWallet`, `mandatoryMedia`, `maximumActiveMedia`, `mediaCombination`, `membership`, `minimumMediaRequired`, `mobileQr`, `mobileQrBeforeWristbandCollection`, `optionalMedia`, `primaryMedia`, `product`, `rfidCard`, `rfidWristband`, `secondaryMedia`, `simultaneousActivation`, `temporaryMedia`, `ticketType`, `venue`

> ⚠ **30 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-338 Multi-Media Binding & Association Rules

**Decision:** 

### p12  · `listCredentialIdentityToken`

`GET /credential-identity-token` · SCOPE_VIEW · staff · **Credential Identity, Token & Reference Mapping**

> Define how individual media identifiers resolve securely back to the authoritative Virtual Ticket.

**`CredentialIdentityTokenReferenceMappingView`** — `activationDate`, `andTheResolverReturns`, `credentialBindingId`, `credentialReference`, `dependingOnCredentialTechnology`, `encryption`, `expiry`, `faceReference`, `hashing`, `issuedDate`, `keyReferences`, `masking`, `mediaType`, `nfcToken`, `providerReference`, `qrToken`, `rfidUid`, `securityProfile`, `signedPayloads`, `status`, `tokenIdentifier`, `tokenization`, `version`, `virtualTicketId`, `walletObject`

- serves P08 BO-339 Credential Identity, Token & Reference Mapping

**Decision:** 

### p14  · `listEntitlementCrossMedia`

`GET /entitlement-cross-media` · SCOPE_VIEW · staff · **Entitlement & Cross-Media Synchronization Rules**

> Ensure all media attached to a Virtual Ticket share the same authoritative ticket and entitlement state.

**`EntitlementCrossMediaSynchronizationRulesView`** — `cancellation`, `conflictingStates`, `delayedUpdates`, `entry`, `exit`, `expiry`, `mainAdmission`, `offlineTransactionsPendingSynchronization`, `partialConsumption`, `providerUpdateFailures`, `reactivation`, `redemption`, `replacement`, `staleWalletCredentials`, `suspension`

- serves P08 BO-340 Entitlement & Cross-Media Synchronization Rules

**Decision:** 

### p15  · `listMediaActivationPriority`

`GET /media-activation-priority` · SCOPE_VIEW · staff · **Media Activation, Priority & Fallback Rules**

> Configure when each credential becomes active and how alternative media behave if the preferred credential cannot be used.

**`MediaActivationPriorityFallbackRulesView`** — `automaticExpiration`, `immediateOnIssuance`, `manualActivation`, `onDownload`, `onEventDate`, `onFaceEnrollment`, `onFirstUse`, `onRfidAssignment`, `onTicketActivation`, `onWalletInstallation`, `oneTimeUse`, `originalMediaImpact`, `replacementBehavior`, `scheduledActivation`, `temporaryMedia`, `ticket`, `validityDuration`

- serves P08 BO-341 Media Activation, Priority & Fallback Rules

**Decision:** 

### p16  · `listMediaReplacementRevocation`

`GET /media-replacement-revocation` · SCOPE_VIEW · staff · **Media Replacement, Revocation & Rebinding Rules**

> Configure controlled handling of lost, stolen, damaged, compromised or replaced credential media.

**`MediaReplacementRevocationRebindingRulesView`** — `approval`, `approvalRequired`, `compromisedQr`, `damagedWristband`, `dateTime`, `faceReEnrollment`, `gracePeriod`, `identityVerification`, `incorrectCredentialAssignment`, `lostRfidCard`, `newBinding`, `newMobileDevice`, `numberOfReplacements`, `oldBinding`, `oldMediaAutomaticallyRevoked`, `printedTicketReplacement`, `reason`, `reasonMandatory`, `relatedTransaction`, `replacementFeeReference`, `rfid88721Revoked`, `rfid99211Active`, `simultaneousMediaPolicy`, `supervisorApproval`, `user`, `vt009821Active`, `walletCredentialReplacement`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-342 Media Replacement, Revocation & Rebinding Rules

**Decision:** 

### p17  · `listVirtualTicketArchitecture`

`GET /virtual-ticket-architecture` · SCOPE_VIEW · staff · **Virtual Ticket Architecture Testing, Governance & Audit**

> Provide the final testing and governance environment for Virtual Ticket and multi-media configurations. 17 | Pag e

**`VirtualTicketArchitectureTestingGovernanceAuditView`** — `activation`, `actor`, `approvals`, `beforeAfter`, `brokenProviderIntegration`, `configurationChanges`, `conflictingActivationRules`, `coreVirtualTicketArchitecture`, `credentialBindingConflict`, `excessiveActiveCredentials`, `expiredWalletToken`, `faceUnavailable`, `invalidLifecycleDependencies`, `invalidMediaCombinations`, `lostRfid`, `mediaBindings`, `missingFallback`, `missingSecurityProfile`, `offlineDevice`, `providerOutage`, `rebindings`, `replacement`, `replacementRebindingTestGovern`, `resolverChanges`, `revocation`, `revokedQr`, `ruleChanges`, `sameAuthoritativeEntitlementEvaluated`, `suspension`, `synchronizationFailure`, `timestamp`

> ⚠ **31 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-334 Virtual Ticket Command Center
- serves P08 BO-343 Virtual Ticket Architecture Testing, Governance & Audit

**Decision:** 

### p23  · `listMediaDesign`

`GET /media-design` · SCOPE_VIEW · staff · **Media Design Studio Command Center**

> Provide administrators with the central workspace for creating and managing all ticket and credential media templates. This should be the entry point for the entire no-code Media Design Studio.

**`MediaDesignStudioCommandCenterView`** — `a4A5`, `appleWallet`, `appleWalletTemplates`, `archived`, `barcodeTicket`, `brand`, `cardWristbandTemplates`, `createMediaTemplate`, `customPrint`, `draft`, `dynamicQrTicket`, `effectiveFrom`, `effectiveTo`, `googleWallet`, `googleWalletTemplates`, `language`, `lastModified`, `mediaType`, `mobileTicket`, `owner`, `pdf`, `pdfPrintTemplates`, `pendingApproval`, `pos`, `productEventAssociation`, `published`, `qrDigitalTemplates`, `qrTicket`, `rfidCard`, `rfidNfcTemplates`, `scheduled`, `status`, `templateId`, `templateName`, `templatesRequiringReview`, `templatesWithValidationErrors`, `thermal`, `totalMediaTemplates`, `venue`, `version`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-344 Media Design Studio Command Center

**Decision:** 

### p24  · `setDigitalBarcodeTicket`

`PUT /digital-barcode-ticket` · ACCESS_POINT_CONFIGURE · staff · **Digital QR & Barcode Ticket Designer**

> Provide a visual no-code designer specifically for digital QR and barcode tickets.

**`DigitalQrBarcodeTicketDesignerView`** — `barcode`, `barcodeType`, `customFields`, `customerName`, `date`, `dynamicQr`, `entrance`, `errorCorrection`, `eventImage`, `eventName`, `expiration`, `hideShowEncodedReference`, `humanReadableValue`, `instructions`, `logo`, `mobileTabletDesktop`, `orderReference`, `orientation`, `participantName`, `position`, `price`, `qr`, `quietZone`, `refreshBehavior`, `rotationBehaviorWhereSupported`, `row`, `seat`, `section`, `showPriceOnOff`, `signedQr`, `size`, `sponsor`, `staticQr`, `terms`, `ticketType`, `time`, `tokenizedQr`, `venue`, `virtualTicketId`, `waiverLinkStatus`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-345 Digital QR & Barcode Ticket Designer

**Decision:** 

### p26  · `setPdfPrintablePos`

`PUT /pdf-printable-pos` · ACCESS_POINT_CONFIGURE · staff · **PDF, Printable & POS Ticket Designer**

> Design tickets intended for printing, PDF generation, POS, box office and other physical/document outputs.

**`PdfPrintablePosTicketDesignerView`** — `a4`, `a5`, `background`, `boxOfficeStock`, `customDimensions`, `cutBehavior`, `dpi`, `dynamicFields`, `footer`, `header`, `images`, `logo`, `margins`, `orientation`, `pageSize`, `paperStockType`, `pdf`, `perforationIndicatorsWhereApplicable`, `posReceipt`, `prePrintedStockWhereRequired`, `printSafeZones`, `printerProfile`, `qrBarcode`, `supportedPrinterIntegration`, `terms`, `text`, `thermalLayout`, `thermalTicket`

> ⚠ **28 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-346 PDF, Printable & POS Ticket Designer

**Decision:** 

### p27  · `setAppleWalletPass`

`PUT /apple-wallet-pass` · ACCESS_POINT_CONFIGURE · staff · **Apple Wallet Pass Designer**

> Provide an Apple Wallet-specific configuration experience for eligible TICVAI credentials. This should not simply be a PDF ticket rendered inside a wallet.

**`AppleWalletPassDesignerView`** — `accordingToTheCredentialProfile`, `auxiliaryFields`, `backFields`, `backgroundAppearance`, `barcode`, `description`, `dynamicUpdates`, `eventChanges`, `expiry`, `foregroundAppearance`, `headerFields`, `icon`, `imagesWhereSupported`, `labelAppearance`, `logo`, `organization`, `passIdentity`, `primaryFields`, `qr`, `relevantNotificationUpdateBehavior`, `revocationInvalidationBehaviorWhereSupported`, `seatChanges`, `secondaryFields`, `ticketStatusChanges`, `tokenReference`

- serves P08 BO-347 Apple Wallet Pass Designer

**Decision:** 

### p29  · `setGoogleWalletPass`

`PUT /google-wallet-pass` · ACCESS_POINT_CONFIGURE · staff · **Google Wallet Pass Designer**

> Provide a dedicated Google Wallet configuration environment.

**`GoogleWalletPassDesignerView`** — `accordingToSupportedWalletFunctionality`, `additionalInformation`, `barcode`, `credentialTokenReference`, `customFields`, `dateTime`, `eventInformation`, `eventTimeChange`, `heroImageAssetsWhereApplicable`, `issuer`, `links`, `logo`, `mapping`, `passClass`, `passTemplate`, `provideDeviceOrientedPreviewBeforePublication`, `qr`, `relevantTicketInformationChanges`, `seat`, `seatReassignment`, `status`, `ticketHolder`, `ticketStatusChange`, `ticketType`, `title`, `venue`, `venueChange`

> ⚠ **27 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-348 Google Wallet Pass Designer

**Decision:** 

### p30  · `setRfidNfcCard`

`PUT /rfid-nfc-card` · ACCESS_POINT_CONFIGURE · staff · **RFID, NFC, Card & Wristband Media Designer**

> Configure both the visual and technical profile of physical electronic credentials. This is important because RFID/NFC media are not merely artwork.

**`RfidNfcCardWristbandMediaDesignerView`** — `activationAtCollection`, `back`, `chipProfile`, `colorCategory`, `credentialBindingVirtualTicket`, `customArtwork`, `customWearable`, `customerName`, `depositReferenceWhereApplicable`, `disposable`, `encoded`, `encodingProfile`, `expiry`, `front`, `logo`, `mediaDimensions`, `membershipCard`, `membershipTier`, `nfcCard`, `nfcWristband`, `photo`, `printableArea`, `printed`, `printerEncoderIntegration`, `provider`, `readerCompatibility`, `reusable`, `rfidCard`, `rfidNfcTechnology`, `rfidWristband`, `serialNumber`, `sizeWhereApplicable`, `sponsorVenueBranding`, `staffGuestCardWhereApplicable`, `uidReferenceHandling`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-180 RFID & NFC Configuration
- serves P08 BO-349 RFID, NFC, Card & Wristband Media Designer

**Decision:** 

### p31  · `setDigitalCardMembership`

`PUT /digital-card-membership` · ACCESS_POINT_CONFIGURE · staff · **Digital Card, Membership & Wearable Designer**

> Provide specialized configuration for persistent credentials that may represent longer-lived relationships rather than a single event ticket.

**`DigitalCardMembershipWearableDesignerView`** — `ageCategories`, `benefitStatus`, `benefitsSummary`, `brand`, `brands`, `cardArtwork`, `dynamicMessaging`, `expiry`, `memberName`, `memberPhotograph`, `membershipNumber`, `membershipRenewal`, `membershipTypes`, `qrBarcode`, `status`, `suspension`, `tier`, `tierChange`, `tierDesigns`, `validity`, `venues`

- serves P08 BO-350 Digital Card, Membership & Wearable Designer

**Decision:** 

### p32  · `setDynamicFieldData`

`PUT /dynamic-field-data` · ACCESS_POINT_CONFIGURE · staff · **Dynamic Fields, Data Mapping & Content Builder**

> Create a centralized reusable field library so development team does not hard-code ticket fields separately into every media designer. This is another important architecture screen.

**`DynamicFieldsDataMappingContentBuilderView`** — `barcode`, `bookingReference`, `channel`, `credentialReference`, `currency`, `customerId`, `customerName`, `date`, `dateFormats`, `discount`, `dobAgeCategory`, `email`, `entrance`, `event`, `expiry`, `faceValue`, `membershipId`, `mobile`, `orderId`, `paidPrice`, `participantId`, `participantName`, `performance`, `photo`, `product`, `purchaseDate`, `qr`, `row`, `seat`, `section`, `status`, `ticketType`, `tier`, `time`, `usageStatus`, `validity`, `venue`, `virtualTicketId`, `waiverLinkWherePermitted`, `waiverStatus`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-351 Dynamic Fields, Data Mapping & Content Builder

**Decision:** 

### p34  · `listBrandingLocalizationTemplate`

`GET /branding-localization-template` · SCOPE_VIEW · staff · **Branding, Localization & Template Inheritance**

> Allow TICVAI's multi-tenant clients to control branding and localization without rebuilding every ticket template.

**`BrandingLocalizationTemplateInheritanceView`** — `additionalConfiguredLanguages`, `approval`, `arabic`, `backgrounds`, `colors`, `english`, `headerFooter`, `images`, `legalFooter`, `logo`, `reviewer`, `sourceLanguage`, `sponsorPlacement`, `supportInformation`, `translation`, `translationStatus`, `typography`, `version`

- serves P08 BO-352 Branding, Localization & Template Inheritance

**Decision:** 

### p36  · `approveMultiMediaPreview`

`PUT /multi-media-preview` · ACCESS_POINT_CONFIGURE · staff · **Multi-Media Preview, Testing, Approval & Publication**

> Provide the final quality and governance gate before any media template becomes operational. This should be a particularly visual screen.

**`MultiMediaPreviewTestingApprovalPublicationView`** — `aTemplateChanges`, `approvalPublishedMediaTemplate`, `arabicLayoutExceedsPrintableArea`, `barcodeReadability`, `branding`, `controlledRollout`, `credentialPayload`, `date15Sep2026`, `desktop`, `dynamicFields`, `eachTemplate`, `encoder`, `imageResolution`, `localization`, `missingFields`, `missingMandatoryField`, `mobile`, `pos`, `printer`, `productVipConcert`, `providerConfiguration`, `qrOverlapsCustomerName`, `qrReadability`, `redesigningTheVirtualTicketCore`, `row3`, `rtl`, `seat18`, `sectionA`, `selectedBrands`, `selectedChannels`, `selectedProducts`, `selectedVenues`, `sideBySideWherePractical`, `tablet`, `time1930`, `venueArena`, `virtualTicketResolution`, `virtualTicketVt2026009821`, `wallet`, `walletConfiguration`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-353 Multi-Media Preview, Testing, Approval & Publication

**Decision:** 

### p41  · `listCredential`

`GET /credential` · SCOPE_VIEW · staff · **Credential Operations Command Center**

> Provide Operations, Ticketing, Customer Service and Technical teams with a real-time command center covering all issued credential media. This is the operational starting point for Area 15.

**`CredentialOperationsCommandCenterView`** — `activationStatus`, `activeCredentials`, `appleWallet`, `barcode`, `bindingStatus`, `card`, `credentialId`, `credentialStatus`, `credentialsGenerated`, `customerParticipant`, `deliveryStatus`, `dynamicQr`, `event`, `exception`, `expired`, `faceRecognitionReference`, `failedDelivery`, `failedGeneration`, `googleWallet`, `lastActivity`, `mediaType`, `multiMediaVirtualTickets`, `nfc`, `owner`, `pdf`, `pendingActivation`, `pendingBinding`, `pendingDelivery`, `pendingGeneration`, `product`, `provider`, `qrGeneration9998Healthy`, `revoked`, `rfid`, `rfidEncoding987Healthy`, `suspended`, `synchronizationExceptions`, `virtualTicketId`, `virtualTicketsIssued`, `wristband`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-354 Credential Operations Command Center
- serves P08 BO-653 Credential Registry & Credential History

**Decision:** 

### p43  · `setVirtualTicketCredential`

`PUT /virtual-ticket-credential` · ACCESS_POINT_CONFIGURE · staff · **Virtual Ticket & Credential 360° Workspace**

> Provide a complete operational view of one Virtual Ticket and every media credential currently or historically associated with it. This is one of the most important operational screens.

**`VirtualTicketCredential360WorkspaceView`** — `activated`, `al`, `appleWalletActive`, `bindRfid`, `bindingId`, `delivered`, `deviceReferenceWhereAppropriate`, `diagnose`, `dynamicQrActive`, `entitlements`, `event`, `fallback`, `initiateFaceEnrollment`, `issued`, `lastPresentation`, `lastUpdate`, `lastUse`, `mediaType`, `order`, `participant`, `performance`, `primary`, `product`, `provider`, `refresh`, `revokedHistoricalMedia`, `seat`, `secondary`, `showAllAssociatedCredentials`, `status`, `temporary`, `ticketHolder`, `ticketStatus`, `usageStatus`, `validFrom`, `validTo`, `validity`, `venue`, `virtualTicketId`

> ⚠ **39 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-355 Virtual Ticket & Credential 360° Workspace

**Decision:** 

### p45  · `listCredentialGenerationIssuance`

`GET /credential-generation-issuance` · SCOPE_VIEW · staff · **Credential Generation & Issuance Monitor**

> Manage and monitor generation of credential instances from approved Board 2 media templates.

**`CredentialGenerationIssuanceMonitorView`** — `api`, `automaticRetry`, `brand`, `bulkOperation`, `channel`, `customer`, `customerContext`, `customerRequest`, `encoderUnavailable`, `error`, `event`, `faceEnrollment`, `generatedAt`, `invalidPayload`, `language`, `manualRetry`, `media`, `membershipActivation`, `orderConfirmation`, `product`, `provider`, `providerUnavailable`, `requestId`, `requestedAt`, `requiredDataMissing`, `rfidCollection`, `scheduledProcess`, `staffAction`, `status`, `supportControlledBulkOperations`, `template`, `templateMissing`, `templateVersion`, `ticketIssuance`, `tokenGenerationFailure`, `venue`, `virtualTicket`, `walletGenerationFailure`, `walletRequest`

> ⚠ **39 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-356 Credential Generation & Issuance Monitor
- serves P08 BO-644 Credential Issuance Command Center

**Decision:** 

### p47  · `listCredentialDeliveryDistribution`

`GET /credential-delivery-distribution` · SCOPE_VIEW · staff · **Credential Delivery & Distribution Operations**

> Manage how generated ticket media are delivered or made available to customers, participants and operational staff.

**`CredentialDeliveryDistributionOperationsView`** — `api`, `appleWallet`, `attempt`, `authentication`, `authorizedRecipient`, `b2cAccount`, `boxOffice`, `channel`, `customerIdentity`, `dataMasking`, `deliveredAt`, `destination`, `email`, `googleWallet`, `groupLeader`, `groupPortal`, `guardian`, `kiosk`, `media`, `mobileApp`, `openedDownloaded`, `participant`, `physicalCollection`, `pos`, `purchaser`, `recipient`, `sentAt`, `singleMultipleUse`, `smsLink`, `statesType`, `status`, `ticketHolder`, `tokenSecurity`, `virtualTicket`, `whatsappIntegration`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-357 Credential Delivery & Distribution Operations

**Decision:** 

### p48  · `setMediaBindingActivation`

`PUT /media-binding-activation` · ACCESS_POINT_CONFIGURE · staff · **Media Binding, Activation & Assignment Operations**

> Manage credentials that require operational assignment or activation after ticket issuance.

**`MediaBindingActivationAssignmentOperationsView`** — `activation`, `batchAssignment`, `bindingRule`, `credentialIdUid`, `customer`, `encoderAssignment`, `existingMedia`, `faceRecognition`, `manualLookupWhereAuthorized`, `newMediaType`, `nfc`, `physicalCards`, `product`, `provider`, `rawBiometricData`, `rfid`, `scan`, `tap`, `temporaryActivation`, `temporaryCredentials`, `validity`, `virtualTicket`, `wristbands`

- serves P08 BO-358 Media Binding, Activation & Assignment Operations

**Decision:** 

### p50  · `listCredentialReplacementReissue`

`GET /credential-replacement-reissue` · SCOPE_VIEW · staff · **Credential Replacement, Reissue, Revocation & Recovery**

> Manage operational credential changes while preserving the underlying Virtual Ticket.

**`CredentialReplacementReissueRevocationRecoveryView`** — `calculationsHere`, `compromised`, `customerChangedPhone`, `damaged`, `faceReEnrollment`, `gracePeriod`, `identityVerification`, `immediateOldMediaRevocation`, `incorrectAssignment`, `lost`, `maximumReplacements`, `qr`, `qr55128Active`, `qrCompromise`, `reasonCodes`, `rf88721Revoked`, `rf99211Active`, `rfidFailure`, `stolen`, `supervisorApproval`, `theVirtualTicketRemainsUnchanged`, `vt009821Active`, `walletReplacement`, `wristbandReplacement`

- serves P08 BO-359 Credential Replacement, Reissue, Revocation & Recovery
- serves P08 BO-652 Credential Replacement & Reissue

**Decision:** 

### p51  · `listFailedGenerationDelivery`

`GET /failed-generation-delivery` · SCOPE_VIEW · staff · **Failed Generation, Delivery & Credential Exception Management**

> Provide one dedicated operational queue for credential-related failures.

**`FailedGenerationDeliveryCredentialExceptionManagemenView`** — `accessImpact`, `activationFailed`, `bindingFailed`, `credential`, `customer`, `customerArrivalTime`, `deliveryFailed`, `event`, `eventProximity`, `expiredCredential`, `failure`, `generationFailed`, `invalidToken`, `mappingFailure`, `media`, `missingRequiredData`, `missingTemplate`, `noAlternativeMedia`, `numberOfAffectedTickets`, `operationalImpact`, `owner`, `providerFailure`, `providerOutage`, `rebind`, `regenerate`, `rfidEncodingFailure`, `severity`, `switchMedia`, `synchronizationFailure`, `time`, `unknownCredential`, `useFallback`, `vipCustomerServiceImpact`, `virtualTicket`, `walletFailure`

> ⚠ **35 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-360 Failed Generation, Delivery & Credential Exception Management

**Decision:** 

### p53  · `listCredentialUsageCross`

`GET /credential-usage-cross` · SCOPE_VIEW · staff · **Credential Usage & Cross-Media Traceability**

> Provide end-to-end visibility into how the different media attached to one Virtual Ticket have been presented or used. This screen is for credential traceability, while Area 16 remains responsible for the actual access-control decision.

**`CredentialUsageCrossMediaTraceabilityView`** — `area16DecidesAdmission`, `credential`, `device`, `entitlementImpact`, `externalSystem`, `location`, `media`, `presentationTimestamp`, `result`, `rfidRf10028Vt009821`, `synchronizationStatus`, `transactionType`, `virtualTicket`, `where`

- serves P08 BO-361 Credential Usage & Cross-Media Traceability

**Decision:** 

### p54  · `listCredentialSecurityOperational`

`GET /credential-security-operational` · SCOPE_VIEW · staff · **Credential Security, Audit & Operational Evidence**

> Maintain complete evidence of credential creation and lifecycle activity.

**`CredentialSecurityAuditOperationalEvidenceView`** — `action`, `activated`, `actor`, `after`, `approval`, `before`, `bound`, `credential`, `credentialRequested`, `dateTime`, `deletedWhereLegallyPermissiblyApplicable`, `delivered`, `device`, `excessiveRegeneration`, `expired`, `generated`, `lost`, `media`, `multipleCredentialAssignments`, `presented`, `providerReference`, `reactivated`, `reason`, `rebound`, `regenerated`, `relatedTransaction`, `repeatedReplacement`, `replaced`, `replacement`, `revoked`, `rfid1001Revoked`, `rfid1057Active`, `role`, `source`, `suspended`, `suspiciousRebinding`, `unauthorizedAdministrativeActions`, `unexpectedProviderTokenChanges`, `updated`, `virtualTicket`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-173 Credential Security Simulation, Audit & Publication
- serves P08 BO-362 Credential Security, Audit & Operational Evidence

**Decision:** 

### p56  · `listTicketMedia`

`GET /ticket-media` · SCOPE_VIEW · staff · **Ticket Media Analytics & AI Operations Intelligence**

> Provide management and operations with analytics and AI intelligence across Virtual Tickets and credential media. This should be a serious operational intelligence layer—not simply a chatbot.

**`TicketMediaAnalyticsAiOperationsIntelligenceView`** — `activation`, `appleWallet`, `appleWallet31`, `averageGenerationTime`, `averageResolutionTime`, `cardWristband`, `credentialFailureRisk`, `credentialsGenerated`, `deliveryFailure`, `deliveryFailureProbability`, `deliveryFailures`, `deliverySuccess`, `encodingFailures`, `face12`, `faceCredentialAdoption`, `faceRecognitionReference`, `futureMedia`, `generationFailure`, `generationFailures`, `generationSuccess`, `googleWallet`, `googleWallet22`, `likelyOnSiteReplacementVolumes`, `mediaDemandForUpcomingEvents`, `mediaUsageDistribution`, `mobileQr78`, `multiMediaAdoption`, `operationalWorkload`, `providerUptime`, `qrDynamicQr`, `replacementFrequency`, `replacementRate`, `revocationRate`, `rfid18`, `rfidAdoption`, `rfidNfc`, `rfidWristbandStockRequirements`, `sameTicket`, `synchronizationDelay`, `walletAdoption`

> ⚠ **40 properties.** A response this wide, read off a directory screen, is usually the screen's *filter set* rather than one record's fields.

- serves P08 BO-363 Ticket Media Analytics & AI Operations Intelligence

**Decision:** 

