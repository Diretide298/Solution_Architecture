-- access — 76 tables
-- **Derived. Do not hand-edit.**

-- Holds 27 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.access_area (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    parent_area_id                    uuid,
    entity_type                       text NOT NULL CONSTRAINT access_area_entity_type_chk CHECK (entity_type IN ('venue', 'park', 'building', 'eventSpace', 'waterpark', 'themePark', 'museum', 'arena', 'stadium', 'exhibition', 'temporaryVenue', 'zone', 'attraction', 'controlledArea')),
    zone_type                         text CONSTRAINT access_area_zone_type_chk CHECK (zone_type IN ('public', 'ticketed', 'vip', 'staff', 'backOfHouse', 'attraction', 'restricted', 'fastPass', 'event', 'temporary')),
    name                              text NOT NULL,
    code                              text NOT NULL,
    time_zone                         text,
    operating_calendar                text,
    operating_schedule                text,
    capacity                          integer,
    security_classification           text,
    entry_requirements                text,
    exit_requirements                 text,
    allowed_credential_classes        text[],
    is_access_control_enabled         boolean DEFAULT true,
    default_entry_policy              text,
    default_exit_policy               text,
    default_credential_rules          text,
    offline_policy_id                 uuid,
    emergency_behavior                text,
    support_multi_park_environments   boolean DEFAULT false,
    operational_adjustment            integer DEFAULT 0,
    occupancy_thresholds              jsonb,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.access_attribute (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    attribute_key                     text NOT NULL CONSTRAINT access_attribute_attribute_key_chk CHECK (char_length(attribute_key) <= 100),
    category                          text NOT NULL CONSTRAINT access_attribute_category_chk CHECK (category IN ('guest', 'credential', 'employee', 'location', 'time', 'operational', 'device', 'risk')),
    label                             text NOT NULL CONSTRAINT access_attribute_label_chk CHECK (char_length(label) <= 200),
    data_type                         text NOT NULL CONSTRAINT access_attribute_data_type_chk CHECK (data_type IN ('string', 'integer', 'number', 'boolean', 'date', 'dateTime', 'enum')),
    allowed_values                    text[],
    is_enabled                        boolean NOT NULL DEFAULT true,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.access_change (
    id                                uuid PRIMARY KEY,
    old_access_id                     uuid NOT NULL,
    new_access_id                     uuid,
    type                              text NOT NULL CONSTRAINT access_change_type_chk CHECK (char_length(type) <= 30),
    order_id                          text,
    upgrade_id                        uuid,
    reason                            text CONSTRAINT access_change_reason_chk CHECK (char_length(reason) <= 500),
    changed_by_principal_id           uuid,
    changed_at                        timestamptz NOT NULL
);

-- Holds 30 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.access_device (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    hardware_model_id                 uuid,
    hardware_type                     text NOT NULL CONSTRAINT access_device_hardware_type_chk CHECK (hardware_type IN ('standardTurnstile', 'fullHeightTurnstile', 'tripodTurnstile', 'speedGate', 'wideLane', 'accessiblePodGate', 'buggyGate', 'vipGate', 'staffGate', 'androidHandheld', 'iosDevice', 'tablet', 'qrBarcodeReader', 'rfidReader', 'nfcReader', 'multiTechnologyReader', 'biometricReader', 'podium', 'counter', 'beacon', 'cameraController', 'externalAccessDevice')),
    name                              text,
    serial_number                     text,
    access_area_id                    uuid,
    access_point_id                   uuid,
    gate_lane_id                      uuid,
    device_group_id                   text,
    ip_network_reference              text,
    controller_reference              text,
    installation_date                 date,
    provisioning_stage                text NOT NULL DEFAULT 'registered' CONSTRAINT access_device_provisioning_stage_chk CHECK (provisioning_stage IN ('registered', 'hardwareProfileAssigned', 'locationAssigned', 'authenticated', 'configurationDownloaded', 'securityPackageDownloaded', 'connectivityTested', 'active')),
    lifecycle_status                  text DEFAULT 'registered' CONSTRAINT access_device_lifecycle_status_chk CHECK (lifecycle_status IN ('registered', 'configured', 'tested', 'approved', 'production')),
    capabilities                      text[],
    proximity_threshold_meters        integer,
    is_active                         boolean NOT NULL DEFAULT true,
    status                            text CONSTRAINT access_device_status_chk CHECK (status IN ('healthy', 'active', 'degraded', 'offline', 'localMode')),
    connectivity                      text,
    scanner_health                    text,
    controller_health                 text,
    camera_health                     text,
    configuration_version             text,
    local_rule_version                text,
    credential_security_package_version text,
    last_heartbeat_at                 timestamptz,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.access_incident (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    incident_type                     text NOT NULL CONSTRAINT access_incident_incident_type_chk CHECK (incident_type IN ('credentialFraud', 'duplicateUse', 'biometricMismatch', 'lostWristband', 'gateFailure', 'guestDispute', 'childGuardianIssue', 'groupAdmissionIssue', 'securityEvent', 'offlineConflict', 'partnerTicketFailure', 'emergencyAccessEvent')),
    assigned_team                     text CONSTRAINT access_incident_assigned_team_chk CHECK (assigned_team IN ('accessSupervisor', 'guestServices', 'security', 'ticketing', 'technicalSupport')),
    ticket_id                         text,
    description                       text,
    status                            text NOT NULL DEFAULT 'open' CONSTRAINT access_incident_status_chk CHECK (status IN ('open', 'investigating', 'resolved', 'closed')),
    scan_event_ids                    text[],
    created_by_principal_id           uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.access_map (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    map_id                            text NOT NULL,
    source_file_type                  text CONSTRAINT access_map_source_file_type_chk CHECK (source_file_type IN ('cad', 'pdf', 'image', 'venuePlan', 'architecturalDrawing')),
    source_file                       text,
    proposed_topology                 jsonb,
    proposal_status                   text CONSTRAINT access_map_proposal_status_chk CHECK (proposal_status IN ('pending', 'accepted', 'rejected')),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- A place a credential is presented — a gate, a turnstile, a door, a scanner position. Carries the
-- rules it applies through access.admission_rules
CREATE TABLE IF NOT EXISTS access.access_point (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    external_credential_sources       jsonb,
    scan_anomaly_rules                jsonb,
    operating_mode                    text NOT NULL DEFAULT 'normal',
    vehicle_location_capture          boolean DEFAULT false,
    mode                              text,
    direction                         text,
    is_anti_passback_enabled          boolean,
    requires_exit_before_reentry      boolean DEFAULT false,
    driver                            text,
    geofence                          jsonb,
    is_active                         boolean NOT NULL,
    last_heartbeat_at                 timestamptz
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.access_point_configuration (
    id                                uuid PRIMARY KEY NOT NULL,
    access_point_id                   uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    pass_through_timeout_seconds      integer,
    relock_behavior                   text,
    incomplete_passage_behavior       text,
    unlock_duration_seconds           integer,
    readers                           text[],
    verification_priority             text[],
    rfid_range                        text CONSTRAINT access_point_configuration_rfid_range_chk CHECK (rfid_range IN ('near', 'medium', 'far')),
    is_height_verification_enabled    boolean DEFAULT false,
    biometric_outcome_rules           jsonb,
    is_exit_capture_enabled           boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.access_point_group (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    name                              text NOT NULL,
    parent_group_id                   uuid,
    access_point_ids                  text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- What a gate needs to admit an accredited person, kept by access (29 September, BL-181). Written
-- only by the consumers of accreditation.credentialIssued and accreditation.holderStatusChanged;
-- admits goes false when a credential is replaced or its holder is suspended, revoked, expired or
-- archived. Read by validateAccess and shipped in the offline package, so a revoked badge stops
-- opening doors on a
CREATE TABLE IF NOT EXISTS access.accreditation_credential (
    id                                uuid PRIMARY KEY NOT NULL,
    holder_id                         uuid NOT NULL,
    programme_id                      uuid,
    kind                              text,
    encoded_identifier                text NOT NULL,
    valid_from                        date,
    valid_to                          date,
    zone_ids                          text[],
    holder_status                     text CONSTRAINT accreditation_credential_holder_status_chk CHECK (holder_status IN ('active', 'suspended', 'revoked', 'expired', 'archived')),
    admits                            boolean NOT NULL,
    source_changed_at                 timestamptz,
    scope_path                        ltree NOT NULL
);

-- What a gate checks before it opens — how early, how late, how many times, and which credentials
-- count. Renamed from admission_rules, because *profile* reads as a person
CREATE TABLE IF NOT EXISTS access.admission_rules (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT admission_rules_code_chk CHECK (char_length(code) <= 64),
    per_product_rules                 jsonb,
    name                              text NOT NULL CONSTRAINT admission_rules_name_chk CHECK (char_length(name) <= 200),
    open_minutes_before               integer NOT NULL,
    close_minutes_after               integer NOT NULL,
    max_duration_minutes              integer,
    requires_exit_before_reentry      boolean DEFAULT false,
    max_reentries                     integer,
    entry_limit                       jsonb,
    exit_scan                         text DEFAULT 'optional' CONSTRAINT admission_rules_exit_scan_chk CHECK (exit_scan IN ('required', 'optional', 'none')),
    max_exits                         integer,
    re_entry_window_minutes           integer,
    same_day_only                     boolean DEFAULT true,
    designated_access_point_ids       text[],
    validity                          jsonb,
    crossover                         jsonb,
    allowed_access_point_ids          text[],
    re_entry_verification             text DEFAULT 'credentialOnly' CONSTRAINT admission_rules_re_entry_verification_chk CHECK (re_entry_verification IN ('credentialOnly', 'credentialUvStamp', 'credentialFace', 'credentialOperator', 'custom')),
    rule_conditions                   jsonb,
    scope_path                        ltree NOT NULL
);

-- Holds 21 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.attraction_access (
    id                                uuid PRIMARY KEY NOT NULL,
    attraction_id                     uuid NOT NULL,
    name                              text NOT NULL CONSTRAINT attraction_access_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    zone_id                           uuid,
    capacity                          integer,
    entry_access_point_ids            text[],
    exit_access_point_ids             text[],
    fast_pass_support                 boolean DEFAULT false,
    height_restriction                integer,
    age_restriction                   integer,
    adult_companion_requirement       boolean DEFAULT false,
    membership_access                 boolean DEFAULT false,
    vip_access                        boolean DEFAULT false,
    entitlement_requirement           text,
    biometric_requirement             boolean DEFAULT false,
    operating_calendar                text,
    temporary_closure_behavior        text,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.biometric_audit_event (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    occurred_at                       timestamptz NOT NULL,
    is_simulation                     boolean NOT NULL DEFAULT false,
    scenario                          text CONSTRAINT biometric_audit_event_scenario_chk CHECK (scenario IN ('validFacePass', 'faceMismatch', 'noBiometricProfile', 'lowConfidenceMatch', 'livenessFailure', 'duplicateProfile', 'reEnrollmentAttempt', 'childAssignedAdult', 'faceTagExpired', 'faceTagDeleted', 'offlineBiometric', 'cameraUnavailable', 'alternativeVerificationFallback')),
    biometric_profile_id              text,
    subject_id                        uuid,
    entitlement_id                    text,
    credential_type                   text CONSTRAINT biometric_audit_event_credential_type_chk CHECK (char_length(credential_type) <= 100),
    face_profile_reference            text CONSTRAINT biometric_audit_event_face_profile_reference_chk CHECK (char_length(face_profile_reference) <= 200),
    access_point_id                   uuid,
    gate_group_id                     uuid,
    device_id                         uuid,
    operator_principal_id             uuid,
    result                            text NOT NULL CONSTRAINT biometric_audit_event_result_chk CHECK (result IN ('allowed', 'review', 'denied')),
    reason_code                       text CONSTRAINT biometric_audit_event_reason_code_chk CHECK (char_length(reason_code) <= 60),
    decision_trace                    text[]
);

-- Holds 36 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.biometric_profile (
    id                                text PRIMARY KEY NOT NULL,
    profile_kind                      text NOT NULL CONSTRAINT biometric_profile_profile_kind_chk CHECK (profile_kind IN ('verification', 'facePassEnrolment', 'faceTagEnrolment', 'faceMatch')),
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    name                              text CONSTRAINT biometric_profile_name_chk CHECK (char_length(name) <= 200),
    status                            text NOT NULL DEFAULT 'active' CONSTRAINT biometric_profile_status_chk CHECK (status IN ('active', 'inactive')),
    biometric_type                    text CONSTRAINT biometric_profile_biometric_type_chk CHECK (biometric_type IN ('facePass', 'faceTag', 'otherProvider')),
    select_type                       text CONSTRAINT biometric_profile_select_type_chk CHECK (select_type IN ('ticketProduct', 'ticketType', 'membership', 'annualPass', 'multiDayTicket', 'multiAttractionTicket', 'vipCredential', 'accreditation', 'selectedCustomerSegments')),
    face_requirement                  text CONSTRAINT biometric_profile_face_requirement_chk CHECK (face_requirement IN ('notUsed', 'optional', 'required')),
    park_id                           uuid,
    zone_id                           uuid,
    attraction_id                     uuid,
    access_point_id                   uuid,
    enrollment_channels               text[],
    is_account_login_required         boolean,
    is_valid_ticket_pass_required     boolean,
    is_identity_check_required        boolean,
    number_of_capture_attempts        integer,
    minimum_image_quality             text,
    operator_verification             boolean,
    enrollment_expiry_days            integer,
    duplicate_face_check              boolean,
    bind_to                           text CONSTRAINT biometric_profile_bind_to_chk CHECK (bind_to IN ('ticket', 'visit', 'temporaryCredential')),
    deletion_trigger                  text CONSTRAINT biometric_profile_deletion_trigger_chk CHECK (deletion_trigger IN ('ticketFullyRedeemed', 'endOfVisit', 'ticketExpiration', 'credentialCancellation', 'operationalRetentionThreshold')),
    retention_threshold_hours         integer,
    consent_capture                   text CONSTRAINT biometric_profile_consent_capture_chk CHECK (consent_capture IN ('onScreenAcknowledgement', 'signedForm')),
    access_context                    text CONSTRAINT biometric_profile_access_context_chk CHECK (char_length(access_context) <= 100),
    high_confidence_min               numeric(18,4),
    review_range_min                  numeric(18,4),
    retry_quantity                    integer,
    liveness_check                    boolean,
    image_quality                     text CONSTRAINT biometric_profile_image_quality_chk CHECK (image_quality IN ('low', 'medium', 'high')),
    capture_timeout_seconds           integer,
    mask_obstruction_handling         text CONSTRAINT biometric_profile_mask_obstruction_handling_chk CHECK (mask_obstruction_handling IN ('deny', 'operatorReview', 'fallbackMethod')),
    operator_fallback                 boolean,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Who may not be admitted, and by whose authority
CREATE TABLE IF NOT EXISTS access.blacklist (
    media_code                        text NOT NULL,
    reason                            text NOT NULL,
    added_at                          timestamptz NOT NULL,
    added_by_principal_id             uuid NOT NULL,
    expires_at                        timestamptz,
    list_type                         text DEFAULT 'blacklist' CONSTRAINT blacklist_list_type_chk CHECK (list_type IN ('blacklist', 'whitelist')),
    disable_scope                     text DEFAULT 'entireCredential' CONSTRAINT blacklist_disable_scope_chk CHECK (disable_scope IN ('entireCredential', 'venueAccess', 'attractionAccess', 'reEntry', 'fastPass', 'specificEntitlement')),
    distributed_to                    text[],
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 24 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.branding_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    level                             text NOT NULL CONSTRAINT branding_profile_level_chk CHECK (level IN ('tenant', 'brand', 'venue', 'event', 'product', 'mediaTemplate')),
    scope_id                          text NOT NULL,
    parent_scope_id                   text,
    logo                              text,
    colors                            text[],
    typography                        text,
    backgrounds                       text,
    header_footer                     text,
    legal_footer                      text,
    support_information               text,
    sponsor_placement                 text,
    images                            text[],
    source_language                   text NOT NULL CONSTRAINT branding_profile_source_language_chk CHECK (char_length(source_language) <= 35),
    languages                         text[],
    is_rtl                            boolean NOT NULL DEFAULT false,
    field_overrides                   jsonb,
    translation_status                text DEFAULT 'notStarted' CONSTRAINT branding_profile_translation_status_chk CHECK (translation_status IN ('notStarted', 'inProgress', 'inReview', 'approved')),
    reviewer_principal_id             uuid,
    approval_request_id               text,
    version                           integer DEFAULT 1,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.companion_rule (
    id                                text PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    name                              text NOT NULL CONSTRAINT companion_rule_name_chk CHECK (char_length(name) <= 200),
    guest_category                    text NOT NULL CONSTRAINT companion_rule_guest_category_chk CHECK (guest_category IN ('adult', 'child', 'junior', 'senior', 'pod', 'podCompanion', 'nanny', 'vip', 'member', 'staff', 'accreditation', 'customerSegment')),
    required_companion_category       text NOT NULL CONSTRAINT companion_rule_required_companion_category_chk CHECK (required_companion_category IN ('adult', 'podCompanion', 'nanny', 'guardian')),
    relationship_type                 text CONSTRAINT companion_rule_relationship_type_chk CHECK (relationship_type IN ('parentChild', 'guardianMinor', 'podCompanion', 'primaryGuestNanny', 'groupLeaderGroupMember', 'other')),
    companion_verification            text NOT NULL DEFAULT 'linkedTicket' CONSTRAINT companion_rule_companion_verification_chk CHECK (companion_verification IN ('linkedTicket', 'companionBiometric')),
    verify_at                         text[] NOT NULL,
    attraction_ids                    text[],
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.configuration_change (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    change_type                       text NOT NULL CONSTRAINT configuration_change_change_type_chk CHECK (change_type IN ('configurationChange', 'mediaBinding', 'rebinding', 'activation', 'suspension', 'revocation', 'replacement', 'resolverChange', 'ruleChange', 'approval')),
    subject_type                      text CONSTRAINT configuration_change_subject_type_chk CHECK (char_length(subject_type) <= 63),
    subject_id                        text,
    configuration_version_id          uuid,
    before                            jsonb,
    after                             jsonb,
    changed_by_principal_id           uuid NOT NULL,
    changed_at                        timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.configuration_version (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    configuration_kind                text NOT NULL CONSTRAINT configuration_version_configuration_kind_chk CHECK (configuration_kind IN ('topology', 'ruleSet')),
    version                           text NOT NULL,
    snapshot                          jsonb,
    status                            text NOT NULL DEFAULT 'draft' CONSTRAINT configuration_version_status_chk CHECK (status IN ('draft', 'validated', 'pendingApproval', 'scheduled', 'active', 'inactive', 'rolledBack')),
    last_step                         text CONSTRAINT configuration_version_last_step_chk CHECK (last_step IN ('simulate', 'validate', 'schedule', 'publish', 'rollBack')),
    target_scope                      text CONSTRAINT configuration_version_target_scope_chk CHECK (target_scope IN ('tenant', 'venue', 'park', 'zone', 'accessPoint', 'selectedGates', 'selectedDevices')),
    target_ids                        text[],
    publish_mode                      text CONSTRAINT configuration_version_publish_mode_chk CHECK (publish_mode IN ('now', 'scheduled')),
    scheduled_at                      timestamptz,
    published_at                      timestamptz,
    validation_issues                 text[],
    conflicts                         text[],
    previous_version_id               uuid,
    approval_request_id               uuid,
    created_by_principal_id           uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.consumption_rule (
    id                                text PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT consumption_rule_name_chk CHECK (char_length(name) <= 200),
    credential_type                   text,
    entitlement_type                  text NOT NULL CONSTRAINT consumption_rule_entitlement_type_chk CHECK (entitlement_type IN ('parkAdmission', 'attractionAdmission', 'ride', 'fastPass', 'meal', 'voucher', 'photo', 'locker', 'event', 'experience', 'reEntry', 'membershipBenefit', 'custom')),
    consumption_order                 integer NOT NULL DEFAULT 1,
    consumption_per_validation        integer NOT NULL DEFAULT 1,
    quantity                          integer,
    is_unlimited                      boolean NOT NULL DEFAULT false,
    one_per_attraction                boolean NOT NULL DEFAULT false,
    attraction_ids                    text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 24 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_binding (
    id                                text PRIMARY KEY NOT NULL,
    entitlement_id                    text NOT NULL,
    media_type_id                     text NOT NULL,
    credential_reference              text NOT NULL CONSTRAINT credential_binding_credential_reference_chk CHECK (char_length(credential_reference) <= 200),
    token_reference                   text CONSTRAINT credential_binding_token_reference_chk CHECK (char_length(token_reference) <= 500),
    provider                          text CONSTRAINT credential_binding_provider_chk CHECK (char_length(provider) <= 100),
    provider_reference                text CONSTRAINT credential_binding_provider_reference_chk CHECK (char_length(provider_reference) <= 200),
    credential_security_profile_id    uuid,
    protection_methods                text[],
    role                              text NOT NULL DEFAULT 'primary' CONSTRAINT credential_binding_role_chk CHECK (role IN ('primary', 'secondary', 'fallback', 'temporary', 'revokedHistorical')),
    capture_method                    text CONSTRAINT credential_binding_capture_method_chk CHECK (capture_method IN ('scan', 'tap', 'manualLookup', 'batchAssignment', 'encoderAssignment')),
    activation_mode                   text CONSTRAINT credential_binding_activation_mode_chk CHECK (activation_mode IN ('activateNow', 'schedule', 'activateOnFirstUse', 'activateOnCollection', 'temporaryActivation')),
    scheduled_activation_at           timestamptz,
    status                            text NOT NULL CONSTRAINT credential_binding_status_chk CHECK (status IN ('pending', 'active', 'suspended', 'revoked', 'expired')),
    issued_at                         timestamptz,
    delivered_at                      timestamptz,
    activated_at                      timestamptz,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    version                           integer NOT NULL DEFAULT 1,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_delivery (
    id                                text PRIMARY KEY NOT NULL,
    entitlement_id                    text NOT NULL,
    credential_binding_id             text,
    channel                           text NOT NULL CONSTRAINT credential_delivery_channel_chk CHECK (channel IN ('email', 'smsLink', 'whatsapp', 'b2cAccount', 'mobileApp', 'download', 'appleWallet', 'googleWallet', 'pos', 'boxOffice', 'kiosk', 'groupPortal', 'api', 'physicalCollection')),
    recipient_role                    text NOT NULL DEFAULT 'ticketHolder' CONSTRAINT credential_delivery_recipient_role_chk CHECK (recipient_role IN ('purchaser', 'ticketHolder', 'participant', 'guardian', 'groupLeader', 'authorizedRecipient')),
    destination                       text CONSTRAINT credential_delivery_destination_chk CHECK (char_length(destination) <= 320),
    attempt                           integer NOT NULL,
    status                            text NOT NULL CONSTRAINT credential_delivery_status_chk CHECK (status IN ('notRequired', 'pending', 'sent', 'delivered', 'openedDownloaded', 'completed', 'failed', 'bounced', 'expired', 'cancelled')),
    failure_reason                    text CONSTRAINT credential_delivery_failure_reason_chk CHECK (char_length(failure_reason) <= 500),
    note                              text CONSTRAINT credential_delivery_note_chk CHECK (char_length(note) <= 300),
    sent_at                           timestamptz,
    delivered_at                      timestamptz,
    opened_at                         timestamptz,
    requested_at                      timestamptz NOT NULL,
    requested_by_principal_id         uuid,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 25 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_event (
    id                                uuid PRIMARY KEY NOT NULL,
    entitlement_id                    text NOT NULL,
    credential_binding_id             text,
    media_type_id                     text,
    action                            text NOT NULL CONSTRAINT credential_event_action_chk CHECK (action IN ('credentialRequested', 'generated', 'bound', 'delivered', 'activated', 'refreshed', 'updated', 'presented', 'transferred', 'suspended', 'reactivated', 'replaced', 'swapped', 'revoked', 'expired', 'rebound', 'regenerated', 'deleted')),
    before                            jsonb,
    after                             jsonb,
    source                            text CONSTRAINT credential_event_source_chk CHECK (char_length(source) <= 50),
    device_id                         text CONSTRAINT credential_event_device_id_chk CHECK (char_length(device_id) <= 200),
    access_point_id                   uuid,
    reason                            text CONSTRAINT credential_event_reason_chk CHECK (char_length(reason) <= 500),
    result_reason_code                text CONSTRAINT credential_event_result_reason_code_chk CHECK (char_length(result_reason_code) <= 50),
    swap_reason                       text CONSTRAINT credential_event_swap_reason_chk CHECK (swap_reason IN ('lost', 'damaged', 'deviceChange', 'upgrade', 'guestRequest', 'operationalReplacement', 'fraudSecurity', 'accessibility')),
    from_media_type_id                text,
    from_media_reference              text CONSTRAINT credential_event_from_media_reference_chk CHECK (char_length(from_media_reference) <= 200),
    to_media_type_id                  text,
    to_media_reference                text CONSTRAINT credential_event_to_media_reference_chk CHECK (char_length(to_media_reference) <= 200),
    approval_request_id               text,
    provider_reference                text CONSTRAINT credential_event_provider_reference_chk CHECK (char_length(provider_reference) <= 200),
    related_transaction_id            text CONSTRAINT credential_event_related_transaction_id_chk CHECK (char_length(related_transaction_id) <= 100),
    anomaly_flags                     text[],
    occurred_at                       timestamptz NOT NULL,
    actor_principal_id                uuid,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_event_propagation_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    trigger_event                     text NOT NULL CONSTRAINT credential_event_propagation_rule_trigger_event_chk CHECK (trigger_event IN ('entry', 'exit', 'redemption', 'partialConsumption', 'cancellation', 'refund', 'suspension', 'reactivation', 'transfer', 'exchange', 'upgrade', 'reissue', 'expiry', 'replacement', 'manualInvalidation', 'fraudLock', 'accountSuspension')),
    revocation_action                 text CONSTRAINT credential_event_propagation_rule_revocation_action_chk CHECK (revocation_action IN ('invalidate', 'suspend', 'replace')),
    propagation_targets               text[],
    monitored_conditions              text[],
    propagation                       text CONSTRAINT credential_event_propagation_rule_propagation_chk CHECK (char_length(propagation) <= 500),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 21 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_exception (
    id                                text PRIMARY KEY NOT NULL,
    failure_type                      text NOT NULL CONSTRAINT credential_exception_failure_type_chk CHECK (failure_type IN ('generationFailed', 'bindingFailed', 'activationFailed', 'deliveryFailed', 'walletFailure', 'rfidEncodingFailure', 'duplicateCredential', 'invalidToken', 'providerFailure', 'synchronizationFailure', 'missingTemplate', 'missingRequiredData', 'expiredCredential', 'mappingFailure', 'unknownCredential')),
    severity                          text NOT NULL CONSTRAINT credential_exception_severity_chk CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    entitlement_id                    text,
    credential_binding_id             text,
    credential_issuance_id            uuid,
    credential_delivery_id            text,
    media_type_id                     text,
    failure                           text CONSTRAINT credential_exception_failure_chk CHECK (char_length(failure) <= 1000),
    operational_impact                text CONSTRAINT credential_exception_operational_impact_chk CHECK (char_length(operational_impact) <= 500),
    status                            text NOT NULL DEFAULT 'open' CONSTRAINT credential_exception_status_chk CHECK (status IN ('open', 'inProgress', 'escalated', 'resolved')),
    owner_principal_id                uuid,
    last_action                       text CONSTRAINT credential_exception_last_action_chk CHECK (last_action IN ('retry', 'regenerate', 'useFallback', 'escalate', 'assignOwner', 'openTechnicalCase')),
    retry_status                      text CONSTRAINT credential_exception_retry_status_chk CHECK (char_length(retry_status) <= 30),
    technical_case_reference          text CONSTRAINT credential_exception_technical_case_reference_chk CHECK (char_length(technical_case_reference) <= 100),
    action_history                    jsonb,
    occurred_at                       timestamptz NOT NULL,
    resolved_at                       timestamptz,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 21 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_issuance (
    id                                uuid PRIMARY KEY NOT NULL,
    trigger                           text NOT NULL CONSTRAINT credential_issuance_trigger_chk CHECK (trigger IN ('orderConfirmation', 'ticketIssuance', 'membershipActivation', 'customerRequest', 'staffAction', 'rfidCollection', 'walletRequest', 'faceEnrollment', 'api', 'bulkOperation', 'scheduledProcess')),
    entitlement_id                    text NOT NULL,
    credential_binding_id             text,
    media_type_id                     text NOT NULL,
    media_template_id                 uuid,
    media_template_version_id         uuid,
    provider                          text CONSTRAINT credential_issuance_provider_chk CHECK (char_length(provider) <= 100),
    channel                           text CONSTRAINT credential_issuance_channel_chk CHECK (char_length(channel) <= 50),
    language                          text CONSTRAINT credential_issuance_language_chk CHECK (char_length(language) <= 35),
    status                            text NOT NULL CONSTRAINT credential_issuance_status_chk CHECK (status IN ('requested', 'queued', 'templateResolved', 'dataMapped', 'credentialGenerated', 'bound', 'ready', 'delivered', 'failed')),
    failure_reason                    text CONSTRAINT credential_issuance_failure_reason_chk CHECK (failure_reason IN ('templateMissing', 'requiredDataMissing', 'providerUnavailable', 'invalidPayload', 'tokenGenerationFailure', 'walletGenerationFailure', 'encoderUnavailable')),
    error                             text CONSTRAINT credential_issuance_error_chk CHECK (char_length(error) <= 1000),
    attempt_count                     integer NOT NULL DEFAULT 0,
    next_retry_at                     timestamptz,
    requested_at                      timestamptz NOT NULL,
    generated_at                      timestamptz,
    requested_by_principal_id         uuid,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_issuance_retry_policy (
    venue_id                          text NOT NULL,
    automatic_retry                   boolean NOT NULL DEFAULT true,
    max_attempts                      integer NOT NULL DEFAULT 3,
    backoff_minutes                   integer NOT NULL DEFAULT 5,
    escalate_after_attempts           integer NOT NULL DEFAULT 3,
    updated_at                        timestamptz,
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 32 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_policy (
    id                                text PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT credential_policy_kind_chk CHECK (kind IN ('activationDisplay', 'transfer', 'virtualTicketIdentity', 'deviceBinding')),
    name                              text CONSTRAINT credential_policy_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid,
    before_activation_display         text[],
    active_display                    text[],
    activation_triggers               text[],
    is_transfer_allowed               boolean,
    number_of_transfers               integer,
    before_first_validation_only      boolean,
    require_recipient_account         boolean,
    require_otp                       boolean,
    require_acceptance                boolean,
    return_to_sender                  boolean,
    transfer_deadline_hours           integer,
    is_cancel_pending_allowed         boolean,
    is_transfer_audit_required        boolean,
    id_generation_pattern             text,
    ticket_classification             text,
    ticket_ownership_model            text,
    holder_assignment_requirements    text,
    transferability_reference         text,
    validity_model                    text,
    consumption_model                 text,
    entitlement_model                 text,
    media_requirements                text[],
    maximum_active_devices            integer,
    concurrent_sessions               integer,
    device_change_policy              text CONSTRAINT credential_policy_device_change_policy_chk CHECK (device_change_policy IN ('notAllowed', 'allowedBeforeFirstUse', 'otpVerificationRequired', 'operatorApprovalRequired', 'supervisorApprovalRequired')),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_security_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL CONSTRAINT credential_security_profile_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT credential_security_profile_name_chk CHECK (char_length(name) <= 200),
    venue_id                          uuid,
    credential_type                   text CONSTRAINT credential_security_profile_credential_type_chk CHECK (credential_type IN ('dynamicQrTicket', 'membership', 'annualPass', 'mobileWallet', 'loyalty', 'digitalPass', 'event')),
    qr_mode                           text NOT NULL CONSTRAINT credential_security_profile_qr_mode_chk CHECK (qr_mode IN ('static', 'dynamic', 'dynamicDeviceBound', 'dynamicLocationBound', 'dynamicDeviceLocationBound')),
    payload_components                text[],
    refresh_interval_seconds          integer,
    device_bound                      text DEFAULT 'off' CONSTRAINT credential_security_profile_device_bound_chk CHECK (device_bound IN ('required', 'optional', 'off')),
    location_scope                    text DEFAULT 'none' CONSTRAINT credential_security_profile_location_scope_chk CHECK (location_scope IN ('gate', 'venue', 'event', 'none')),
    offline_ready                     boolean DEFAULT false,
    security_level                    text DEFAULT 'standard' CONSTRAINT credential_security_profile_security_level_chk CHECK (security_level IN ('strong', 'standard')),
    signing_key_reference             text CONSTRAINT credential_security_profile_signing_key_reference_chk CHECK (char_length(signing_key_reference) <= 200),
    embedded_claims                   text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.credential_sharing_case (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    entitlement_id                    text NOT NULL,
    primary_device_id                 uuid,
    additional_device_ids             text[],
    maximum_active_devices            integer,
    maximum_device_changes_per_visit  integer,
    response_actions                  text[],
    detected_at                       timestamptz NOT NULL
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.device_binding (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid,
    entitlement_id                    text NOT NULL,
    credential_binding_id             text,
    device_id                         text NOT NULL CONSTRAINT device_binding_device_id_chk CHECK (char_length(device_id) <= 200),
    device_reference                  text CONSTRAINT device_binding_device_reference_chk CHECK (char_length(device_reference) <= 200),
    app_installation_id               text CONSTRAINT device_binding_app_installation_id_chk CHECK (char_length(app_installation_id) <= 200),
    os                                text CONSTRAINT device_binding_os_chk CHECK (char_length(os) <= 50),
    registered_at                     timestamptz NOT NULL,
    last_activated_at                 timestamptz,
    last_known_venue_id               uuid,
    security_status                   text NOT NULL DEFAULT 'normal' CONSTRAINT device_binding_security_status_chk CHECK (security_status IN ('normal', 'suspicious', 'blocked')),
    deactivated_at                    timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 27 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.device_configuration (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    configuration_kind                text NOT NULL CONSTRAINT device_configuration_configuration_kind_chk CHECK (configuration_kind IN ('handheldProfile', 'deviceGroup')),
    name                              text,
    device_group_id                   text,
    version                           text,
    deployment_stage                  text NOT NULL DEFAULT 'draft' CONSTRAINT device_configuration_deployment_stage_chk CHECK (deployment_stage IN ('draft', 'testDevice', 'deviceGroup', 'venueRollout')),
    device_type                       text,
    platform                          text CONSTRAINT device_configuration_platform_chk CHECK (platform IN ('android', 'ios')),
    access_area_id                    uuid,
    operator_group                    text,
    permitted_operating_modes         text[],
    offline_capability                boolean,
    scanner_source                    text,
    biometric_capability              boolean,
    enabled_functions                 text[],
    device_settings                   text,
    gate_mode                         text,
    reader_settings                   text,
    media_profiles                    text[],
    outcome_profile_ids               text[],
    local_rules                       text,
    edge_package_id                   uuid,
    guest_content                     jsonb,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.dynamic_field (
    id                                uuid PRIMARY KEY NOT NULL,
    field_key                         text NOT NULL CONSTRAINT dynamic_field_field_key_chk CHECK (char_length(field_key) <= 100),
    category                          text NOT NULL CONSTRAINT dynamic_field_category_chk CHECK (category IN ('customer', 'participant', 'order', 'virtualTicket', 'productEvent', 'seating', 'commercial', 'membership', 'compliance', 'credential', 'custom')),
    standard_field                    text CONSTRAINT dynamic_field_standard_field_chk CHECK (standard_field IN ('customerName', 'customerId', 'mobile', 'email', 'photo', 'participantName', 'dobAgeCategory', 'participantId', 'orderId', 'bookingReference', 'purchaseDate', 'channel', 'virtualTicketId', 'ticketType', 'status', 'validity', 'usageStatus', 'product', 'event', 'performance', 'date', 'time', 'venue', 'entrance', 'section', 'block', 'row', 'seat', 'faceValue', 'paidPrice', 'discount', 'currency', 'membershipId', 'tier', 'expiry', 'waiverStatus', 'waiverLink', 'qr', 'barcode', 'credentialReference')),
    date_format                       text CONSTRAINT dynamic_field_date_format_chk CHECK (char_length(date_format) <= 50),
    time_format                       text CONSTRAINT dynamic_field_time_format_chk CHECK (char_length(time_format) <= 50),
    number_format                     text CONSTRAINT dynamic_field_number_format_chk CHECK (char_length(number_format) <= 50),
    text_transformation               text CONSTRAINT dynamic_field_text_transformation_chk CHECK (char_length(text_transformation) <= 50),
    character_limit                   integer,
    conditional_visibility            text CONSTRAINT dynamic_field_conditional_visibility_chk CHECK (char_length(conditional_visibility) <= 500),
    allowed_media                     text[],
    is_sensitive                      boolean NOT NULL DEFAULT false,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.dynamic_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    name                              text NOT NULL CONSTRAINT dynamic_policy_name_chk CHECK (char_length(name) <= 200),
    policy_type                       text NOT NULL CONSTRAINT dynamic_policy_policy_type_chk CHECK (policy_type IN ('guestAttribute', 'accreditation', 'occupancy', 'employee', 'risk', 'membership', 'timeEvent')),
    context_type                      text CONSTRAINT dynamic_policy_context_type_chk CHECK (context_type IN ('date', 'day', 'time', 'season', 'event', 'performance', 'specialEvent', 'holiday', 'operatingCalendar', 'occupancy', 'attractionStatus')),
    identity_type                     text CONSTRAINT dynamic_policy_identity_type_chk CHECK (identity_type IN ('guest', 'member', 'annualPassHolder', 'employee', 'contractor', 'vendor', 'performer', 'media', 'vip', 'security', 'emergencyServices', 'eventStaff')),
    condition_expression              text NOT NULL,
    result                            text NOT NULL CONSTRAINT dynamic_policy_result_chk CHECK (result IN ('allow', 'deny', 'review', 'requireId', 'requireBiometric', 'requireCompanion', 'requireSupervisor')),
    priority                          integer,
    allowed_zone_ids                  text[],
    denied_zone_ids                   text[],
    monitor_threshold_percent         integer,
    restrict_threshold_percent        integer,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    status                            text NOT NULL DEFAULT 'draft' CONSTRAINT dynamic_policy_status_chk CHECK (status IN ('draft', 'pendingApproval', 'active', 'inactive', 'expired')),
    current_version                   integer NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.dynamic_policy_version (
    id                                uuid PRIMARY KEY NOT NULL,
    dynamic_policy_id                 uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    version                           integer NOT NULL,
    status                            text NOT NULL CONSTRAINT dynamic_policy_version_status_chk CHECK (status IN ('pendingApproval', 'active', 'superseded', 'rejected')),
    definition                        jsonb NOT NULL,
    restored_from_version             integer,
    reason                            text CONSTRAINT dynamic_policy_version_reason_chk CHECK (char_length(reason) <= 300),
    created_by_principal_id           uuid,
    created_at                        timestamptz NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.edge_node (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    node_type                         text NOT NULL CONSTRAINT edge_node_node_type_chk CHECK (node_type IN ('venueEdgeNode', 'gateController', 'turnstileLocalEngine', 'handheldLocalEngine')),
    network                           text,
    device_group_id                   text,
    processing_mode                   text,
    storage_allocation                text,
    redundancy                        text,
    last_heartbeat_at                 timestamptz,
    software_version                  text,
    security_status                   text,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.edge_package (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    version                           text NOT NULL,
    contents                          text[],
    device_ids                        text[],
    size_bytes                        integer,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    signature_valid                   boolean,
    package_complete                  boolean,
    version_valid                     boolean,
    is_device_authorized              boolean,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- What a guest actually holds — found missing 18 August. The package sold products, defined
-- EntitlementTemplate, recorded ScanEvent.ticketId, transferred ticket_ids and issued wallet
-- passes against entitlementId: five artefacts referring to a thing that did not exist.
-- validateAccess read the template and suspendEntitlement suspended it, which would have suspended
-- it for every guest who held one. Han
CREATE TABLE IF NOT EXISTS access.entitlement (
    id                                text PRIMARY KEY NOT NULL,
    template_id                       uuid NOT NULL,
    product_id                        uuid NOT NULL,
    order_id                          text NOT NULL,
    order_line_id                     uuid,
    subject_id                        uuid,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    media_code                        text,
    status                            text NOT NULL CONSTRAINT entitlement_status_chk CHECK (status IN ('issued', 'partiallyConsumed', 'fullyConsumed', 'expired', 'cancelled', 'surrendered')),
    status_note                       text,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    entries_used                      integer DEFAULT 0,
    entries_allowed                   integer,
    last_entry_at                     timestamptz,
    frozen_days                       integer DEFAULT 0,
    suspended_reason                  text,
    freeze_reason                     text CONSTRAINT entitlement_freeze_reason_chk CHECK (freeze_reason IN ('travelling', 'injury', 'personal', 'seasonal', 'other')),
    freeze_note                       text CONSTRAINT entitlement_freeze_note_chk CHECK (char_length(freeze_note) <= 500),
    is_name_bound                     boolean DEFAULT false,
    holder_name                       text,
    shared_with_subject_ids           text[],
    issued_via                        text CONSTRAINT entitlement_issued_via_chk CHECK (issued_via IN ('sale', 'invitation', 'reissue', 'transfer', 'resale', 'membership', 'groupBooking')),
    supersedes_entitlement_id         text,
    wallet_value_id                   uuid
);

-- Holds 5 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.entry_rule_point (
    admission_profile_id              uuid NOT NULL,
    access_point_id                   uuid NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    id                                uuid PRIMARY KEY
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.external_credential_integration (
    id                                text PRIMARY KEY NOT NULL,
    integration_type                  text NOT NULL CONSTRAINT external_credential_integration_integration_type_chk CHECK (integration_type IN ('hotelRoomCard', 'hotelPms', 'digitalWallet', 'otherExternal', 'partnerCredential')),
    name                              text NOT NULL CONSTRAINT external_credential_integration_name_chk CHECK (char_length(name) <= 200),
    external_system                   text NOT NULL CONSTRAINT external_credential_integration_external_system_chk CHECK (char_length(external_system) <= 200),
    connection_secret_ref             text CONSTRAINT external_credential_integration_connection_secret_ref_chk CHECK (char_length(connection_secret_ref) <= 200),
    is_room_charge_enabled            boolean DEFAULT false,
    maps_to_virtual_credential        boolean DEFAULT true,
    credential_format                 text CONSTRAINT external_credential_integration_credential_format_chk CHECK (char_length(credential_format) <= 100),
    validation_mode                   text CONSTRAINT external_credential_integration_validation_mode_chk CHECK (validation_mode IN ('localMapping', 'apiValidation', 'tokenValidation', 'cachedValidation', 'offlineMapping', 'hybrid')),
    field_mappings                    text[],
    unrecognised_outcome              text CONSTRAINT external_credential_integration_unrecognised_outcome_chk CHECK (unrecognised_outcome IN ('deny', 'referToOperator')),
    status                            text NOT NULL DEFAULT 'draft' CONSTRAINT external_credential_integration_status_chk CHECK (status IN ('draft', 'active', 'inactive')),
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.face_reenrolment_attempt (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    subject_id                        uuid NOT NULL,
    entitlement_id                    text,
    existing_profile_reference        text NOT NULL CONSTRAINT face_reenrolment_attempt_existing_profile_reference_chk CHECK (char_length(existing_profile_reference) <= 200),
    new_capture_reference             text NOT NULL CONSTRAINT face_reenrolment_attempt_new_capture_reference_chk CHECK (char_length(new_capture_reference) <= 200),
    match_result                      text NOT NULL CONSTRAINT face_reenrolment_attempt_match_result_chk CHECK (match_result IN ('withinPolicy', 'significantDifference')),
    reason_for_re_enrollment          text CONSTRAINT face_reenrolment_attempt_reason_for_re_enrollment_chk CHECK (reason_for_re_enrollment IN ('appearanceChange', 'poorOriginalCapture', 'technicalIssue', 'guestRequest', 'recovery', 'other')),
    verification_process              text CONSTRAINT face_reenrolment_attempt_verification_process_chk CHECK (char_length(verification_process) <= 200),
    operator_principal_id             uuid,
    outcome                           text NOT NULL CONSTRAINT face_reenrolment_attempt_outcome_chk CHECK (outcome IN ('updated', 'blocked', 'pendingReview')),
    reviewed_by_principal_id          uuid,
    reviewed_at                       timestamptz,
    attempted_at                      timestamptz NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.fast_pass_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    name                              text NOT NULL CONSTRAINT fast_pass_profile_name_chk CHECK (char_length(name) <= 200),
    is_unlimited                      boolean NOT NULL DEFAULT false,
    total_uses                        integer,
    consumption_per_validation        integer DEFAULT 1,
    one_per_ride                      boolean DEFAULT false,
    eligible_attraction_categories    text[],
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.fraud_rule (
    id                                text PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    rule_kind                         text NOT NULL CONSTRAINT fraud_rule_rule_kind_chk CHECK (rule_kind IN ('signal', 'relationship')),
    signal                            text CONSTRAINT fraud_rule_signal_chk CHECK (signal IN ('excessiveQrActivations', 'multipleActiveSessions', 'credentialCopied', 'excessiveRefreshAttempts', 'invalidSignature', 'expiredCredential', 'revokedCredential', 'screenshotReplayAttempt', 'abnormalTransferFrequency', 'repeatedFailedValidation', 'newDevice', 'multipleDevices', 'deviceBindingMismatch', 'rootedCompromisedDevice', 'abnormalDeviceChanges', 'impossibleDeviceMovement', 'suspiciousScannerDeviceActivity', 'duplicateEntry', 'simultaneousUse', 'antiPassbackViolations', 'unusualReEntry', 'unusualCrossover', 'excessiveAttractionUse', 'repeatedWrongGateAttempts', 'abnormalFastPassConsumption', 'faceMismatch', 'unusualFaceChange', 'multipleIdentitiesLinked', 'suspiciousCompanionChanges', 'podNannyRelationshipAnomalies', 'excessiveRefunds')),
    signal_category                   text CONSTRAINT fraud_rule_signal_category_chk CHECK (signal_category IN ('credential', 'device', 'access', 'identity')),
    relationship_rule_type            text CONSTRAINT fraud_rule_relationship_rule_type_chk CHECK (relationship_rule_type IN ('companionChangedDuringVisit', 'nannyCredentialWithoutPrimaryGuest', 'childWithUnauthorizedAdult', 'companionLinkedToMultiplePrimaries', 'excessiveRelationshipChanges', 'groupLeaderAcrossUnrelatedGroups')),
    relationship_type                 text CONSTRAINT fraud_rule_relationship_type_chk CHECK (relationship_type IN ('childAdult', 'podCompanion', 'guestNanny', 'groupLeaderGroup', 'membershipDependent')),
    severity                          text NOT NULL CONSTRAINT fraud_rule_severity_chk CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    weight                            integer,
    threshold                         integer,
    time_window                       integer,
    applicable_credential_types       text[],
    applicable_venue_ids              text[],
    offline_availability              boolean DEFAULT false,
    response                          text CONSTRAINT fraud_rule_response_chk CHECK (response IN ('alertOnly', 'increaseRiskScore', 'requireAdditionalVerification', 'requireSupervisor', 'temporarilyLock', 'fullIdentityLock', 'blacklist')),
    relationship_responses            text[],
    is_enabled                        boolean NOT NULL DEFAULT true,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.gate_lane (
    id                                uuid PRIMARY KEY NOT NULL,
    access_point_id                   uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    name                              text,
    location                          text,
    lane_number                       text,
    direction                         text CONSTRAINT gate_lane_direction_chk CHECK (direction IN ('entry', 'exit', 'bidirectional')),
    re_entry                          boolean DEFAULT false,
    is_crossover                      boolean DEFAULT false,
    lane_type                         text CONSTRAINT gate_lane_lane_type_chk CHECK (lane_type IN ('standard', 'vip', 'fastPass', 'accessible', 'group', 'staff', 'attraction')),
    operational_mode                  text,
    lane_size                         text DEFAULT 'standard' CONSTRAINT gate_lane_lane_size_chk CHECK (lane_size IN ('standard', 'wide')),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.gate_mode_change (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    access_point_id                   uuid NOT NULL,
    from_mode                         text,
    target_mode                       text NOT NULL,
    status                            text NOT NULL CONSTRAINT gate_mode_change_status_chk CHECK (status IN ('pending', 'applied', 'cancelled')),
    reason                            text CONSTRAINT gate_mode_change_reason_chk CHECK (char_length(reason) <= 500),
    effective_at                      timestamptz,
    changed_by_principal_id           uuid NOT NULL,
    changed_at                        timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.gate_mode_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    mode                              text NOT NULL CONSTRAINT gate_mode_policy_mode_chk CHECK (mode IN ('freeFlow', 'dropArm')),
    who_can_activate                  text[],
    access_point_group_id             uuid,
    is_reason_required                boolean DEFAULT true,
    emergency_code                    text,
    automatic_notification            boolean DEFAULT false,
    creates_incident                  boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.gate_outcome_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    outcome                           text NOT NULL CONSTRAINT gate_outcome_profile_outcome_chk CHECK (outcome IN ('granted', 'operatorAction', 'denied')),
    applies_to                        text NOT NULL CONSTRAINT gate_outcome_profile_applies_to_chk CHECK (applies_to IN ('adult', 'child', 'vip', 'pod', 'membership', 'invalidCredential', 'wrongVerificationMethod', 'biometricReview', 'reEntryException')),
    light_colour                      text CONSTRAINT gate_outcome_profile_light_colour_chk CHECK (light_colour IN ('green', 'yellow', 'red')),
    gate_action                       text CONSTRAINT gate_outcome_profile_gate_action_chk CHECK (gate_action IN ('open', 'remainsControlled', 'remainsLocked')),
    sound                             text CONSTRAINT gate_outcome_profile_sound_chk CHECK (sound IN ('successTone', 'alertSound', 'denialSound')),
    pictogram                         text,
    messages                          jsonb,
    operator_prompt                   text,
    reason_code                       text,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.group_admission_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    name                              text NOT NULL CONSTRAINT group_admission_rule_name_chk CHECK (char_length(name) <= 200),
    group_segments                    text[],
    allowed_group_modes               text[],
    product_ids                       text[],
    max_group_size                    integer,
    credential_mode                   text CONSTRAINT group_admission_rule_credential_mode_chk CHECK (credential_mode IN ('singleGroupQr', 'groupBarcode', 'groupRfid', 'groupLeaderCredential', 'individualCredentials', 'hybrid')),
    admission_method                  text CONSTRAINT group_admission_rule_admission_method_chk CHECK (admission_method IN ('entireGroup', 'partialGroup', 'multipleWaves', 'individualScan', 'leaderQuantity', 'manifestBased')),
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.hardware_deployment (
    id                                text PRIMARY KEY NOT NULL,
    configuration_version             text NOT NULL,
    target_scope                      text NOT NULL CONSTRAINT hardware_deployment_target_scope_chk CHECK (target_scope IN ('pilot', 'selectedGates', 'deviceGroup', 'venue')),
    venue_id                          text,
    gate_ids                          text[],
    device_group_id                   text,
    status                            text NOT NULL CONSTRAINT hardware_deployment_status_chk CHECK (status IN ('queued', 'inProgress', 'completed', 'partiallyFailed', 'rolledBack')),
    devices_targeted                  integer,
    devices_acknowledged              integer,
    failed_device_ids                 text[],
    requested_by_principal_id         text,
    requested_at                      timestamptz,
    scheduled_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.hardware_model (
    id                                uuid PRIMARY KEY NOT NULL,
    manufacturer                      text NOT NULL,
    model                             text NOT NULL,
    device_category                   text NOT NULL CONSTRAINT hardware_model_device_category_chk CHECK (device_category IN ('turnstile', 'specialGate', 'mobile', 'reader', 'other')),
    hardware_type                     text NOT NULL CONSTRAINT hardware_model_hardware_type_chk CHECK (hardware_type IN ('standardTurnstile', 'fullHeightTurnstile', 'tripodTurnstile', 'speedGate', 'wideLane', 'accessiblePodGate', 'buggyGate', 'vipGate', 'staffGate', 'androidHandheld', 'iosDevice', 'tablet', 'qrBarcodeReader', 'rfidReader', 'nfcReader', 'multiTechnologyReader', 'biometricReader', 'podium', 'counter', 'beacon', 'cameraController', 'externalAccessDevice')),
    supported_technologies            text[],
    connectivity                      text[],
    offline_capability                boolean DEFAULT false,
    screen_capability                 boolean DEFAULT false,
    sound_capability                  boolean DEFAULT false,
    light_capability                  boolean DEFAULT false,
    relay_controller_support          boolean DEFAULT false,
    payment_capability                boolean DEFAULT false,
    firmware_software_information     text,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 17 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.identity_lock (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    subject_id                        uuid NOT NULL,
    lock_scope                        text NOT NULL CONSTRAINT identity_lock_lock_scope_chk CHECK (lock_scope IN ('credentialOnly', 'mediaOnly', 'entitlement', 'venue', 'allVenueAccess', 'fullIdentity')),
    lock_duration                     text NOT NULL CONSTRAINT identity_lock_lock_duration_chk CHECK (lock_duration IN ('untilManuallyReleased', 'endOfDay', 'nHours', 'untilInvestigationComplete', 'permanent')),
    lock_hours                        integer,
    lock_reason                       text NOT NULL CONSTRAINT identity_lock_lock_reason_chk CHECK (lock_reason IN ('credentialSharing', 'fraudSuspected', 'securityIncident', 'identityMismatch', 'stolenCredential', 'guestRemoval')),
    associated_entitlement_ids        text[],
    associated_credential_types       text[],
    propagated_to                     text[],
    security_investigation_id         uuid,
    status                            text NOT NULL DEFAULT 'active' CONSTRAINT identity_lock_status_chk CHECK (status IN ('active', 'released')),
    locked_at                         timestamptz NOT NULL,
    locked_by_principal_id            uuid,
    released_at                       timestamptz,
    released_by_principal_id          uuid
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.journey_profile (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    name                              text NOT NULL CONSTRAINT journey_profile_name_chk CHECK (char_length(name) <= 200),
    journey_type                      text CONSTRAINT journey_profile_journey_type_chk CHECK (char_length(journey_type) <= 60),
    credential_type                   text CONSTRAINT journey_profile_credential_type_chk CHECK (char_length(credential_type) <= 100),
    status                            text NOT NULL DEFAULT 'active' CONSTRAINT journey_profile_status_chk CHECK (status IN ('active', 'inactive')),
    steps                             jsonb,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.journey_sequence_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    name                              text CONSTRAINT journey_sequence_rule_name_chk CHECK (char_length(name) <= 200),
    scope                             text NOT NULL CONSTRAINT journey_sequence_rule_scope_chk CHECK (scope IN ('credential', 'guest', 'gate', 'attraction', 'park', 'venue')),
    window_minutes                    integer,
    required_sequence                 text[],
    violation_responses               text[],
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 26 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.media_binding_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    allowed_media_type_ids            text[],
    mandatory_media_type_ids          text[],
    optional_media_type_ids           text[],
    primary_media_type_id             text,
    secondary_media_type_ids          text[],
    backup_media_type_ids             text[],
    temporary_media_type_ids          text[],
    minimum_media_required            integer DEFAULT 0,
    maximum_active_media              integer,
    media_combinations                text[],
    simultaneous_activation           text[],
    exclusive_activation              text[],
    product_id                        uuid,
    ticket_type                       text CONSTRAINT media_binding_rule_ticket_type_chk CHECK (char_length(ticket_type) <= 100),
    event_id                          text,
    venue_id                          uuid,
    customer_type                     text CONSTRAINT media_binding_rule_customer_type_chk CHECK (char_length(customer_type) <= 100),
    membership                        text CONSTRAINT media_binding_rule_membership_chk CHECK (char_length(membership) <= 100),
    channel                           text CONSTRAINT media_binding_rule_channel_chk CHECK (char_length(channel) <= 50),
    age_category                      text CONSTRAINT media_binding_rule_age_category_chk CHECK (char_length(age_category) <= 50),
    country                           text CONSTRAINT media_binding_rule_country_chk CHECK (char_length(country) <= 2),
    access_environment                text CONSTRAINT media_binding_rule_access_environment_chk CHECK (char_length(access_environment) <= 100),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.media_compatibility_test (
    id                                uuid PRIMARY KEY NOT NULL,
    media_type_id                     text NOT NULL,
    venue_id                          uuid NOT NULL,
    park_id                           text,
    access_point_id                   uuid,
    device_group_id                   text,
    stage                             text NOT NULL CONSTRAINT media_compatibility_test_stage_chk CHECK (stage IN ('draft', 'compatibilityTest', 'validate', 'approval', 'published')),
    compatibility_warnings            text[],
    exception_reason                  text CONSTRAINT media_compatibility_test_exception_reason_chk CHECK (char_length(exception_reason) <= 500),
    approval_request_id               text,
    published_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 28 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.media_encoding_profile (
    id                                text PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT media_encoding_profile_name_chk CHECK (char_length(name) <= 200),
    media_type_id                     text,
    encoding_format                   text CONSTRAINT media_encoding_profile_encoding_format_chk CHECK (char_length(encoding_format) <= 100),
    offline_payload_profile           text CONSTRAINT media_encoding_profile_offline_payload_profile_chk CHECK (char_length(offline_payload_profile) <= 200),
    checksum_signature_reference      text CONSTRAINT media_encoding_profile_checksum_signature_reference_chk CHECK (char_length(checksum_signature_reference) <= 200),
    credential_security_profile_id    uuid,
    is_randomization_enabled          boolean DEFAULT true,
    is_identifier_collision_check_enabled boolean DEFAULT true,
    is_duplicate_prevention_enabled   boolean DEFAULT true,
    rfid_standard                     text CONSTRAINT media_encoding_profile_rfid_standard_chk CHECK (char_length(rfid_standard) <= 100),
    tag_card_type                     text CONSTRAINT media_encoding_profile_tag_card_type_chk CHECK (char_length(tag_card_type) <= 100),
    frequency_interface_profile       text CONSTRAINT media_encoding_profile_frequency_interface_profile_chk CHECK (char_length(frequency_interface_profile) <= 100),
    read_write_behavior               text CONSTRAINT media_encoding_profile_read_write_behavior_chk CHECK (char_length(read_write_behavior) <= 100),
    reader_compatibility              text[],
    supported_readers                 text[],
    nfc_uses                          text[],
    offline_capability                boolean,
    read_range                        text CONSTRAINT media_encoding_profile_read_range_chk CHECK (read_range IN ('near', 'medium', 'far')),
    venue_id                          uuid,
    zone_id                           text,
    access_point_id                   uuid,
    credential_type                   text CONSTRAINT media_encoding_profile_credential_type_chk CHECK (char_length(credential_type) <= 100),
    journey                           text CONSTRAINT media_encoding_profile_journey_chk CHECK (char_length(journey) <= 100),
    is_active                         boolean NOT NULL DEFAULT true,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.media_replacement_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    replacement_reason                text NOT NULL CONSTRAINT media_replacement_policy_replacement_reason_chk CHECK (replacement_reason IN ('lost', 'stolen', 'damaged', 'compromised', 'customerChangedPhone', 'rfidFailure', 'wristbandReplacement', 'qrCompromise', 'walletReplacement', 'faceReEnrollment', 'incorrectAssignment')),
    outcome                           text NOT NULL CONSTRAINT media_replacement_policy_outcome_chk CHECK (outcome IN ('replace', 'rebind', 'suspendMedia', 'revokeMedia')),
    maximum_replacements              integer,
    replacement_fee_product_id        uuid,
    is_approval_required              boolean DEFAULT false,
    supervisor_approval               boolean DEFAULT false,
    identity_verification             boolean DEFAULT true,
    reason_mandatory                  boolean DEFAULT true,
    is_old_media_automatically_revoked boolean DEFAULT true,
    grace_period                      text,
    simultaneous_media_policy         text DEFAULT 'oneActive' CONSTRAINT media_replacement_policy_simultaneous_media_policy_chk CHECK (simultaneous_media_policy IN ('oneActive', 'allowBothDuringGrace')),
    is_reissue_allowed                boolean DEFAULT true,
    is_recovery_allowed               boolean DEFAULT false,
    reason_codes                      text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 18 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.media_template (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT media_template_name_chk CHECK (char_length(name) <= 200),
    designer                          text NOT NULL CONSTRAINT media_template_designer_chk CHECK (designer IN ('digitalBarcode', 'pdfPrintablePos', 'appleWallet', 'googleWallet', 'rfidNfcCard', 'digitalCardMembership')),
    media_type                        text NOT NULL CONSTRAINT media_template_media_type_chk CHECK (media_type IN ('qrTicket', 'dynamicQrTicket', 'barcodeTicket', 'mobileTicket', 'pdf', 'a4A5', 'thermal', 'pos', 'customPrint', 'appleWallet', 'googleWallet', 'rfidCard', 'rfidWristband', 'nfcCard', 'nfcWristband', 'membershipCard', 'customWearable')),
    brand_id                          text,
    venue_id                          uuid,
    product_id                        uuid,
    event_id                          text,
    language                          text CONSTRAINT media_template_language_chk CHECK (char_length(language) <= 35),
    design                            jsonb,
    status                            text NOT NULL DEFAULT 'draft' CONSTRAINT media_template_status_chk CHECK (status IN ('draft', 'pendingApproval', 'scheduled', 'published', 'archived')),
    current_version                   integer,
    owner_principal_id                uuid,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.media_template_version (
    id                                uuid PRIMARY KEY NOT NULL,
    media_template_id                 uuid NOT NULL,
    version                           integer NOT NULL,
    design                            jsonb NOT NULL,
    publish_mode                      text NOT NULL CONSTRAINT media_template_version_publish_mode_chk CHECK (publish_mode IN ('publishNow', 'schedule')),
    scheduled_at                      timestamptz,
    controlled_rollout                boolean DEFAULT false,
    brand_ids                         text[],
    venue_ids                         text[],
    product_ids                       text[],
    channels                          text[],
    validation_checks                 text[],
    preview_targets                   text[],
    approval_request_id               text,
    status                            text NOT NULL CONSTRAINT media_template_version_status_chk CHECK (status IN ('pendingApproval', 'scheduled', 'published', 'superseded', 'rejected')),
    published_at                      timestamptz,
    created_at                        timestamptz NOT NULL,
    created_by_principal_id           uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 39 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.media_type (
    id                                text PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT media_type_name_chk CHECK (char_length(name) <= 200),
    media_type                        text NOT NULL CONSTRAINT media_type_media_type_chk CHECK (media_type IN ('linearBarcode', 'twoDimensionalBarcode', 'qr', 'rfidContact', 'rfidProximity', 'rfidIso15693', 'rfidOtherStandard', 'appCredential', 'mobileWallet', 'paperTicket', 'wristband', 'plasticCard', 'hotelCard', 'facePass', 'faceTag', 'partnerQr', 'externalBarcode', 'thirdPartyCredential')),
    category                          text CONSTRAINT media_type_category_chk CHECK (category IN ('digital', 'physical', 'biometric', 'future')),
    technology                        text NOT NULL CONSTRAINT media_type_technology_chk CHECK (technology IN ('barcode', 'rfid', 'nfc', 'magneticStripe', 'mobile', 'physical', 'biometric', 'external')),
    credential_type                   text CONSTRAINT media_type_credential_type_chk CHECK (char_length(credential_type) <= 100),
    encoding_format                   text CONSTRAINT media_type_encoding_format_chk CHECK (char_length(encoding_format) <= 100),
    generation_method                 text CONSTRAINT media_type_generation_method_chk CHECK (char_length(generation_method) <= 200),
    validation_mechanism              text CONSTRAINT media_type_validation_mechanism_chk CHECK (char_length(validation_mechanism) <= 200),
    supported_reader_types            text[],
    supported_devices                 text[],
    supported_channels                text[],
    providers                         text[],
    integration_adapter               text CONSTRAINT media_type_integration_adapter_chk CHECK (char_length(integration_adapter) <= 100),
    online_offline_capability         text NOT NULL CONSTRAINT media_type_online_offline_capability_chk CHECK (online_offline_capability IN ('onlineOnly', 'offlineOnly', 'onlineAndOffline')),
    writable_read_only                text CONSTRAINT media_type_writable_read_only_chk CHECK (writable_read_only IN ('writable', 'readOnly')),
    security_classification           text CONSTRAINT media_type_security_classification_chk CHECK (char_length(security_classification) <= 100),
    supports_visual_design            boolean DEFAULT false,
    supports_dynamic_update           boolean DEFAULT false,
    supports_revocation               boolean DEFAULT false,
    supports_expiration               boolean DEFAULT false,
    supports_offline_reference        boolean DEFAULT false,
    supports_replacement              boolean DEFAULT false,
    supports_encryption               boolean DEFAULT false,
    supports_signing                  boolean DEFAULT false,
    applicable_venue_ids              text[],
    applicable_product_ids            text[],
    activation_trigger                text CONSTRAINT media_type_activation_trigger_chk CHECK (activation_trigger IN ('immediateOnIssuance', 'onTicketActivation', 'onDownload', 'onWalletInstallation', 'onRfidAssignment', 'onFaceEnrollment', 'onFirstUse', 'onEventDate', 'manualActivation', 'scheduledActivation')),
    temporary_media                   boolean DEFAULT false,
    validity_duration                 text,
    one_time_use                      boolean DEFAULT false,
    automatic_expiration              boolean DEFAULT false,
    replacement_behavior              text CONSTRAINT media_type_replacement_behavior_chk CHECK (char_length(replacement_behavior) <= 200),
    original_media_impact             text CONSTRAINT media_type_original_media_impact_chk CHECK (char_length(original_media_impact) <= 200),
    fallback_media_type_ids           text[],
    is_active                         boolean NOT NULL DEFAULT true,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.offline_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    max_offline_duration_hours        integer,
    offline_checks                    text[],
    after_threshold_behavior          text CONSTRAINT offline_policy_after_threshold_behavior_chk CHECK (after_threshold_behavior IN ('continueRestrictedValidation', 'operatorWarning', 'supervisorMode', 'failClosed', 'fallback')),
    revocation_trigger_events         text[],
    revocation_max_allowed_age_minutes integer,
    revocation_staleness_action       text CONSTRAINT offline_policy_revocation_staleness_action_chk CHECK (revocation_staleness_action IN ('continue', 'continueWithWarning', 'restrictedProductsOnly', 'supervisorMode', 'denySelectedCredentialClasses', 'failClosed')),
    operating_modes                   text[],
    central_unavailable_after_seconds integer,
    edge_unavailable_after_seconds    integer,
    automatic_switch                  boolean DEFAULT true,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.operating_calendar_entry (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    day_type                          text NOT NULL CONSTRAINT operating_calendar_entry_day_type_chk CHECK (day_type IN ('normalOperatingDay', 'weekend', 'holiday', 'seasonalSchedule', 'privateEvent', 'freeEntryDay', 'maintenancePeriod', 'specialEvent', 'ladiesOnlySession', 'schoolGroupSession', 'afterHoursEvent')),
    name                              text,
    starts_at                         timestamptz NOT NULL,
    ends_at                           timestamptz NOT NULL,
    is_ticket_validation_required     boolean DEFAULT true,
    admission_type                    text CONSTRAINT operating_calendar_entry_admission_type_chk CHECK (admission_type IN ('freeViewDay', 'specialEvent')),
    attraction_validation             boolean,
    is_manual_attendance_required     boolean,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- A guest bought parking. Carries the plate where the mode is plateWhitelist — personal data,
-- since a plate identifies a person Hangs off: reaches access.entitlement through its keys;
-- references access.parking_facility, orders.sales_order, pii.subject. Reached by: 2 operations
-- read it and 2 write it.
CREATE TABLE IF NOT EXISTS access.parking_entitlement (
    id                                uuid PRIMARY KEY,
    facility_id                       uuid NOT NULL,
    order_id                          text NOT NULL,
    subject_id                        uuid,
    plate_number                      text,
    plate_country                     text,
    media_code                        text,
    status                            text,
    pushed_at                         timestamptz,
    push_failure_reason               text,
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL
);

-- A car park and its integration mode. Three modes, and the mode decides what happens at sale
-- (CF-52) Hangs off: reaches access.entitlement through its keys; references platform.scope.
-- Reached by: 3 operations read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS access.parking_facility (
    id                                uuid PRIMARY KEY,
    name                              text NOT NULL,
    venue_id                          uuid NOT NULL,
    mode                              text NOT NULL CONSTRAINT parking_facility_mode_chk CHECK (mode IN ('none', 'plateWhitelist', 'qrHandoff')),
    capacity                          integer,
    takes_payment                     boolean DEFAULT false,
    vendor_swap_target_days           integer DEFAULT 5,
    vendor_name                       text,
    endpoint                          text,
    credential_ref                    text,
    push_lead_minutes                 integer,
    access_point_ids                  text[],
    is_active                         boolean
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.podium (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    podium_type                       text NOT NULL CONSTRAINT podium_podium_type_chk CHECK (podium_type IN ('physicalControlPanel', 'tablet', 'workstation', 'handheld', 'other')),
    name                              text NOT NULL,
    access_point_ids                  text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.podium_shift (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid NOT NULL,
    operator_principal_id             uuid NOT NULL,
    role                              text,
    podium_id                         uuid,
    access_device_id                  uuid,
    login_at                          timestamptz NOT NULL,
    logout_at                         timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.policy_evaluation_setting (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    policy_category                   text NOT NULL CONSTRAINT policy_evaluation_setting_policy_category_chk CHECK (char_length(policy_category) <= 100),
    evaluation_mode                   text NOT NULL CONSTRAINT policy_evaluation_setting_evaluation_mode_chk CHECK (evaluation_mode IN ('central', 'edge', 'device', 'hybrid')),
    supported_locations               text[],
    offline_behaviour                 text CONSTRAINT policy_evaluation_setting_offline_behaviour_chk CHECK (offline_behaviour IN ('available', 'conditional', 'unavailable')),
    max_data_age_minutes              integer,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.policy_scope_assignment (
    id                                uuid PRIMARY KEY NOT NULL,
    dynamic_policy_id                 uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    scope_level                       text NOT NULL CONSTRAINT policy_scope_assignment_scope_level_chk CHECK (scope_level IN ('tenant', 'venue', 'park', 'zone', 'attraction', 'accessPoint')),
    scope_id                          uuid NOT NULL,
    policy_category                   text NOT NULL CONSTRAINT policy_scope_assignment_policy_category_chk CHECK (policy_category IN ('emergency', 'securityFraud', 'regulatorySafety', 'venueRestriction', 'accreditation', 'membership', 'standardAccess')),
    category_rank                     integer,
    conflict_resolution               text NOT NULL DEFAULT 'denyOverridesAllow' CONSTRAINT policy_scope_assignment_conflict_resolution_chk CHECK (conflict_resolution IN ('highestPriorityWins', 'denyOverridesAllow', 'mostSpecificWins', 'mandatoryParentWins', 'explicitResolution')),
    is_mandatory                      boolean NOT NULL DEFAULT false,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.reason_code (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    code                              text NOT NULL CONSTRAINT reason_code_code_chk CHECK (char_length(code) <= 32),
    name                              text NOT NULL,
    guest_message                     text,
    operator_message                  text,
    operational_response              text NOT NULL CONSTRAINT reason_code_operational_response_chk CHECK (operational_response IN ('deny', 'operatorReview', 'supervisorRequired', 'allowWithWarning')),
    follow_up_action                  text,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.risk_scoring_config (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        ltree NOT NULL,
    medium_threshold                  integer NOT NULL,
    high_threshold                    integer NOT NULL,
    critical_threshold                integer NOT NULL,
    risk_factors                      text[],
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Every presentation of a credential, admitted or not. The highest-volume table in the platform
CREATE TABLE IF NOT EXISTS access.scan_event (
    id                                text PRIMARY KEY NOT NULL,
    access_point_id                   uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    scope_path                        ltree NOT NULL,
    ticket_id                         text,
    media_code                        text,
    outcome                           text NOT NULL CONSTRAINT scan_event_outcome_chk CHECK (outcome IN ('admitted', 'denied', 'overridden')),
    deny_reason                       text CONSTRAINT scan_event_deny_reason_chk CHECK (deny_reason IN ('notFound', 'notYetValid', 'expired', 'alreadyUsed', 'reentryLimitReached', 'exitRequiredBeforeReentry', 'wrongAccessPoint', 'wrongPerformance', 'outsideAdmissionWindow', 'entitlementSuspended', 'blacklisted', 'capacityReached', 'waiverRequired', 'accompanimentRequired', 'mediaDeactivated', 'unpaid', 'delegatedRightExhausted', 'delegatedRightRevoked', 'journeyNotCovered')),
    direction                         text NOT NULL CONSTRAINT scan_event_direction_chk CHECK (direction IN ('entry', 'exit', 'reentry', 'crossover')),
    operator_principal_id             uuid,
    device_id                         uuid,
    overrides_scan_id                 text,
    override_reason                   text,
    dynamic_policy_id                 uuid,
    dynamic_policy_version            integer,
    dynamic_policy_result             text CONSTRAINT scan_event_dynamic_policy_result_chk CHECK (dynamic_policy_result IN ('allow', 'deny', 'review', 'requireId', 'requireBiometric', 'requireCompanion', 'requireSupervisor')),
    quantity                          integer DEFAULT 1,
    local_sequence                    integer,
    package_version                   text,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz,
    overridden_by_principal_id        uuid
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.security_alert (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    category                          text NOT NULL CONSTRAINT security_alert_category_chk CHECK (category IN ('fraudSignal', 'credentialSharing', 'duplicateAccess', 'blacklist', 'biometric', 'companion', 'edgeSecurity')),
    alert_type                        text CONSTRAINT security_alert_alert_type_chk CHECK (char_length(alert_type) <= 60),
    severity                          text NOT NULL CONSTRAINT security_alert_severity_chk CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    description                       text CONSTRAINT security_alert_description_chk CHECK (char_length(description) <= 500),
    fraud_rule_id                     text,
    entitlement_id                    text,
    subject_id                        uuid,
    zone_id                           uuid,
    access_point_id                   uuid,
    device_id                         uuid,
    face_reenrolment_attempt_id       uuid,
    face_profile_reference            text CONSTRAINT security_alert_face_profile_reference_chk CHECK (char_length(face_profile_reference) <= 200),
    security_investigation_id         uuid,
    status                            text NOT NULL DEFAULT 'open' CONSTRAINT security_alert_status_chk CHECK (status IN ('open', 'acknowledged', 'resolved', 'dismissed')),
    detected_at                       timestamptz NOT NULL,
    acknowledged_at                   timestamptz,
    acknowledged_by_principal_id      uuid
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.security_investigation (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    subject_entitlement_id            text,
    evidence_sources                  text[],
    status                            text NOT NULL DEFAULT 'open' CONSTRAINT security_investigation_status_chk CHECK (status IN ('open', 'investigating', 'actionTaken', 'resolved', 'closed')),
    risk_score                        integer,
    risk_level                        text CONSTRAINT security_investigation_risk_level_chk CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    notes                             text,
    linked_incident_id                uuid,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.security_playbook (
    id                                uuid PRIMARY KEY NOT NULL,
    venue_id                          uuid,
    scope_path                        ltree NOT NULL,
    name                              text NOT NULL CONSTRAINT security_playbook_name_chk CHECK (char_length(name) <= 200),
    trigger_condition                 text NOT NULL,
    response_actions                  text[] NOT NULL,
    acknowledge_within_minutes        integer,
    escalate_to_role                  text CONSTRAINT security_playbook_escalate_to_role_chk CHECK (char_length(escalate_to_role) <= 100),
    escalate_after_minutes            integer,
    is_enabled                        boolean NOT NULL DEFAULT true,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.ticket_status_transition (
    id                                uuid PRIMARY KEY NOT NULL,
    from_status                       text NOT NULL CONSTRAINT ticket_status_transition_from_status_chk CHECK (from_status IN ('created', 'pendingFulfillment', 'active', 'partiallyUsed', 'used', 'expired', 'suspended', 'cancelled', 'voided', 'reissuedSuperseded', 'refunded', 'transferred', 'blocked')),
    to_status                         text NOT NULL CONSTRAINT ticket_status_transition_to_status_chk CHECK (to_status IN ('created', 'pendingFulfillment', 'active', 'partiallyUsed', 'used', 'expired', 'suspended', 'cancelled', 'voided', 'reissuedSuperseded', 'refunded', 'transferred', 'blocked')),
    is_allowed                        boolean NOT NULL,
    requires_authorized_exception     boolean NOT NULL DEFAULT false,
    originating_sources               text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS access.verification_method_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    product_id                        uuid NOT NULL,
    available_methods                 text[] NOT NULL,
    lock_on_first_successful_access   boolean NOT NULL DEFAULT true,
    change_after_lock                 text NOT NULL DEFAULT 'supervisorApproval' CONSTRAINT verification_method_policy_change_after_lock_chk CHECK (change_after_lock IN ('notAllowed', 'supervisorApproval')),
    reason_codes                      text[],
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

