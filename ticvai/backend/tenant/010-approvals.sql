-- approvals — 30 tables
-- **Derived. Do not hand-edit.**

-- The badge an approved accreditation actually issues, held apart from the request that granted
-- it. zones is the access it carries and state walks issued, expired and revoked — a badge
-- outlives the decision behind it, which is why revoking one is a row here and not an edit to
-- approvals.request. revoked_reason is required in practice for the same reason an empty state is:
-- a badge that stops working w
CREATE TABLE IF NOT EXISTS approvals.accreditation_badge (
    id                                uuid PRIMARY KEY NOT NULL,
    approval_request_id               uuid,
    holder_name                       text,
    zones                             text[],
    state                             text CONSTRAINT accreditation_badge_state_chk CHECK (state IN ('issued', 'collected', 'suspended', 'revoked', 'expired')),
    issued_at                         timestamptz,
    expires_at                        timestamptz,
    revoked_reason                    text
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.approved_action_execution (
    id                                text PRIMARY KEY NOT NULL,
    approval_request_id               text NOT NULL,
    source_module                     text NOT NULL,
    action_type                       text NOT NULL,
    subject_ref                       text,
    status                            text NOT NULL CONSTRAINT approved_action_execution_status_chk CHECK (status IN ('queued', 'executing', 'succeeded', 'failed', 'investigating', 'escalated')),
    attempts                          integer,
    last_attempt_at                   timestamptz,
    failure_reason                    text,
    assignee_id                       text,
    last_action                       text CONSTRAINT approved_action_execution_last_action_chk CHECK (last_action IN ('retry', 'investigate', 'escalate')),
    note                              text,
    updated_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.approver_availability (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid,
    unavailable_from                  timestamptz,
    unavailable_to                    timestamptz,
    substitute_principal_id           uuid,
    delegation_id                     uuid,
    reason                            text,
    applies_to_request_kinds          text[],
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.automation (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT automation_name_chk CHECK (char_length(name) <= 200),
    source_module                     text CONSTRAINT automation_source_module_chk CHECK (source_module IN ('ticketing', 'pricing', 'finance', 'procurement', 'crm', 'resourceManagement', 'fnb', 'retail', 'groupSales', 'customerService', 'membership', 'wallet', 'waiver', 'subscriptionLicensing')),
    business_rule_id                  uuid,
    workflow_definition_id            uuid,
    action                            text NOT NULL CONSTRAINT automation_action_chk CHECK (action IN ('createApproval', 'createTask', 'updateStatus', 'applyHold', 'releaseHold', 'createNotification', 'generateDocument', 'executeRefund', 'updateAllocation', 'activateMembership', 'suspendPartner', 'callApprovedApi', 'callApprovedService', 'startSubWorkflow')),
    is_ai_assisted                    boolean DEFAULT false,
    status                            text NOT NULL CONSTRAINT automation_status_chk CHECK (status IN ('active', 'paused', 'disabled', 'killSwitched')),
    status_reason                     text CONSTRAINT automation_status_reason_chk CHECK (char_length(status_reason) <= 500),
    status_changed_by                 uuid,
    status_changed_at                 timestamptz,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.automation_execution (
    id                                uuid PRIMARY KEY NOT NULL,
    automation_id                     uuid NOT NULL,
    workflow_instance_id              uuid,
    workflow_version_id               uuid,
    business_rule_id                  uuid,
    business_object_type              text CONSTRAINT automation_execution_business_object_type_chk CHECK (char_length(business_object_type) <= 100),
    business_object_id                text,
    action                            text CONSTRAINT automation_execution_action_chk CHECK (action IN ('createApproval', 'createTask', 'updateStatus', 'applyHold', 'releaseHold', 'createNotification', 'generateDocument', 'executeRefund', 'updateAllocation', 'activateMembership', 'suspendPartner', 'callApprovedApi', 'callApprovedService', 'startSubWorkflow')),
    executed_under_principal_id       uuid,
    result                            text NOT NULL CONSTRAINT automation_execution_result_chk CHECK (result IN ('succeeded', 'failed', 'awaitingConfirmation', 'reversed')),
    confidence                        numeric(18,4),
    failure_reason                    text CONSTRAINT automation_execution_failure_reason_chk CHECK (char_length(failure_reason) <= 1000),
    executed_at                       timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.business_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT business_rule_name_chk CHECK (char_length(name) <= 200),
    business_object_field             text NOT NULL CONSTRAINT business_rule_business_object_field_chk CHECK (char_length(business_object_field) <= 200),
    operator                          text NOT NULL CONSTRAINT business_rule_operator_chk CHECK (operator IN ('equals', 'notEquals', 'greaterThan', 'lessThan', 'between', 'contains', 'inList', 'exists', 'doesNotExist', 'beforeAfter', 'percentageThreshold', 'boolean')),
    comparison_value                  text CONSTRAINT business_rule_comparison_value_chk CHECK (char_length(comparison_value) <= 1000),
    outcome                           text NOT NULL CONSTRAINT business_rule_outcome_chk CHECK (outcome IN ('allow', 'reject', 'requireApproval', 'requireAdditionalInformation', 'applyHold', 'createTask', 'generateAlert', 'startWorkflow', 'executeApprovedAction')),
    explanation                       text CONSTRAINT business_rule_explanation_chk CHECK (char_length(explanation) <= 1000),
    status                            text NOT NULL CONSTRAINT business_rule_status_chk CHECK (status IN ('draft', 'testing', 'review', 'pendingApproval', 'approved', 'scheduled', 'active', 'suspended', 'retired')),
    version                           integer,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 13 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.control_policy (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text,
    applies_to_request_kinds          text[],
    applies_above_value               numeric(18,4),
    control                           text NOT NULL CONSTRAINT control_policy_control_chk CHECK (control IN ('fourEyes', 'dualControl', 'separationFromRequester', 'separationFromExecutor')),
    required_approver_group_ids       text[],
    minimum_approvers                 integer DEFAULT 2,
    requires_step_up                  boolean DEFAULT false,
    requires_signature                boolean DEFAULT false,
    is_break_glass_allowed            boolean DEFAULT false,
    scope_path                        ltree NOT NULL,
    is_active                         boolean DEFAULT true
);

-- Every decision at every level. Immutable once the request completes — an approval is evidence
-- Hangs off: reaches approvals.request through its keys; references approvals.request,
-- identity.principal. Reached by: 16 operations read it and 3 write it.
CREATE TABLE IF NOT EXISTS approvals.decision (
    id                                uuid PRIMARY KEY,
    level                             integer NOT NULL,
    principal_id                      uuid NOT NULL,
    display_name                      text,
    is_delegate                       boolean,
    delegated_from                    uuid,
    decision                          text NOT NULL CONSTRAINT decision_decision_chk CHECK (decision IN ('approve', 'reject')),
    comment                           text,
    reason                            text,
    used_mfa                          boolean,
    signature_ref                     text,
    decided_at                        timestamptz NOT NULL,
    request_id                        text NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.decision_record (
    request_id                        uuid,
    sequence                          integer,
    recorded_at                       timestamptz,
    decision                          text,
    decided_by                        uuid,
    comment                           text,
    payload_hash                      text,
    previous_record_hash              text,
    record_hash                       text,
    integrity                         text CONSTRAINT decision_record_integrity_chk CHECK (integrity IN ('intact', 'broken', 'unverifiable')),
    scope_path                        ltree NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.decision_table (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT decision_table_name_chk CHECK (char_length(name) <= 200),
    resolution_strategy               text NOT NULL CONSTRAINT decision_table_resolution_strategy_chk CHECK (resolution_strategy IN ('priority', 'sequence', 'specificity')),
    on_match                          text NOT NULL CONSTRAINT decision_table_on_match_chk CHECK (on_match IN ('stopProcessing', 'continueEvaluation')),
    conflicts                         text[],
    status                            text NOT NULL CONSTRAINT decision_table_status_chk CHECK (status IN ('draft', 'testing', 'review', 'pendingApproval', 'approved', 'scheduled', 'active', 'suspended', 'retired')),
    version                           integer,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 6 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.decision_table_row (
    decision_table_id                 uuid NOT NULL,
    id                                uuid PRIMARY KEY NOT NULL,
    priority                          integer NOT NULL,
    conditions                        jsonb NOT NULL,
    outcome                           text NOT NULL,
    explanation                       text
);

-- Standing in for an approver. Always time-bounded — an open-ended delegation is one nobody
-- remembers Hangs off: reaches approvals.request through its keys; references identity.principal.
-- Reached by: 8 operations read it and 3 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS approvals.delegation (
    id                                uuid PRIMARY KEY,
    delegator_principal_id            uuid NOT NULL,
    delegate_principal_id             uuid NOT NULL,
    kinds                             text[],
    max_amount                        numeric(18,4),
    valid_from                        timestamptz NOT NULL,
    valid_to                          timestamptz NOT NULL,
    reason                            text,
    is_active                         boolean,
    scope_path                        ltree NOT NULL
);

-- Who was asked, when, and why it moved up. The original approver stays in the record Hangs off:
-- reaches approvals.request through its keys; references approvals.request. Reached by: 6
-- operations read it and 1 write it.
CREATE TABLE IF NOT EXISTS approvals.escalation (
    id                                uuid PRIMARY KEY NOT NULL,
    request_id                        text NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.evidence_package (
    id                                uuid PRIMARY KEY,
    requested_by                      uuid,
    requested_at                      timestamptz,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    request_count                     integer,
    integrity_failures                integer,
    status                            text CONSTRAINT evidence_package_status_chk CHECK (status IN ('assembling', 'ready', 'failed')),
    asset_id                          uuid,
    expires_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.external_dispatch (
    id                                uuid PRIMARY KEY NOT NULL,
    request_id                        text NOT NULL,
    provider_id                       uuid NOT NULL,
    level                             integer NOT NULL,
    status                            text NOT NULL CONSTRAINT external_dispatch_status_chk CHECK (status IN ('pending', 'sent', 'failed', 'decided', 'timedOut', 'cancelled')),
    attempt_count                     integer DEFAULT 0,
    external_reference                text,
    last_response_code                integer,
    last_error                        text,
    sent_at                           timestamptz,
    answered_at                       timestamptz,
    external_outcome                  text,
    external_approver_ref             text,
    scope_path                        ltree NOT NULL
);

-- Holds 14 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.external_provider (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    endpoint_url                      text NOT NULL,
    outbound_auth                     text DEFAULT 'oauthClientCredentials' CONSTRAINT external_provider_outbound_auth_chk CHECK (outbound_auth IN ('bearerToken', 'basic', 'oauthClientCredentials', 'mutualTls')),
    outbound_credential               text,
    signing_secret                    text,
    api_client_id                     uuid NOT NULL,
    timeout_minutes                   integer DEFAULT 1440,
    on_timeout                        text DEFAULT 'fallBackToRoles' CONSTRAINT external_provider_on_timeout_chk CHECK (on_timeout IN ('fallBackToRoles', 'escalate', 'reject')),
    max_attempts                      integer DEFAULT 5,
    status                            text DEFAULT 'active' CONSTRAINT external_provider_status_chk CHECK (status IN ('active', 'paused', 'disabled')),
    last_success_at                   timestamptz,
    scope_path                        ltree NOT NULL
);

-- What requires approval where. Versioned, because a request must be decided by the rules it was
-- raised under Hangs off: reaches approvals.request through its keys. Reached by: 8 operations
-- read it and 2 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS approvals.matrix (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL CONSTRAINT matrix_kind_chk CHECK (kind IN ('refund', 'priceOverride', 'discountOverride', 'complimentaryTicket', 'membershipCancellation', 'accessPermissionChange', 'configurationChange', 'aiRecommendation', 'releasePromotion', 'requisition', 'stockWriteOff', 'journalEntry', 'periodClose', 'periodReopen', 'purchaseOrderCancel', 'purchaseOrderShortClose', 'tenantMigration', 'productChange', 'pricingChange')),
    scope_level                       text NOT NULL CONSTRAINT matrix_scope_level_chk CHECK (scope_level IN ('tenant', 'region', 'venue')),
    scope_path                        ltree NOT NULL,
    version                           integer,
    is_active                         boolean
);

-- One request per action needing authorisation. The subject is a reference, never a copy Hangs
-- off: a root — nothing above it in its schema; references identity.principal. Reached by: 31
-- operations read it and 24 write it; 50 tables reference it; written by 3 contracts — approvals,
-- subscription, workforce.
CREATE TABLE IF NOT EXISTS approvals.request (
    id                                text PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT request_kind_chk CHECK (kind IN ('refund', 'priceOverride', 'discountOverride', 'complimentaryTicket', 'membershipCancellation', 'accessPermissionChange', 'configurationChange', 'aiRecommendation', 'releasePromotion', 'requisition', 'stockWriteOff', 'journalEntry', 'periodClose', 'periodReopen', 'purchaseOrderCancel', 'purchaseOrderShortClose', 'tenantMigration', 'productChange', 'pricingChange')),
    reroute_on_no_approver            boolean DEFAULT true,
    out_of_office_delegate_id         uuid,
    allow_email_approval              boolean DEFAULT false,
    reopened_from                     uuid,
    status                            text NOT NULL CONSTRAINT request_status_chk CHECK (status IN ('draft', 'pending', 'escalated', 'returned', 'informationRequested', 'approved', 'rejected', 'withdrawn', 'expired', 'cancelled')),
    subject_contract                  text,
    subject_type                      text,
    subject_id                        text,
    scope_path                        ltree NOT NULL,
    summary                           text,
    amount                            numeric(18,4),
    justification                     text,
    requested_by_principal_id         uuid NOT NULL,
    matrix_version                    integer,
    mode                              text CONSTRAINT request_mode_chk CHECK (mode IN ('sequential', 'parallel', 'consensus', 'majority')),
    current_level                     integer,
    total_levels                      integer,
    resubmitted_from_id               text,
    reopened_from_id                  text,
    sla_due_at                        timestamptz,
    is_sla_breached                   boolean,
    expires_at                        timestamptz,
    requested_at                      timestamptz NOT NULL,
    completed_at                      timestamptz,
    ai_assessment                     jsonb
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.retention_policy (
    id                                uuid PRIMARY KEY,
    applies_to_request_kinds          text[],
    retain_years                      integer,
    retain_signatures                 boolean DEFAULT true,
    retain_attachments                boolean DEFAULT false,
    on_expiry                         text DEFAULT 'archive' CONSTRAINT retention_policy_on_expiry_chk CHECK (on_expiry IN ('delete', 'anonymise', 'archive')),
    overrides_privacy_deletion        boolean DEFAULT true,
    legal_basis                       text,
    scope_path                        ltree NOT NULL
);

-- Ordered within a matrix. First match wins, so adding a rule cannot silently change another Hangs
-- off: reaches approvals.request through its keys; references approvals.external_provider,
-- approvals.matrix. Reached by: 15 operations read it and 2 write it; 3 tables reference it.
CREATE TABLE IF NOT EXISTS approvals.rule (
    id                                uuid PRIMARY KEY,
    sort_order                        integer NOT NULL,
    min_amount                        numeric(18,4),
    max_amount                        numeric(18,4),
    risk_score_above                  numeric(18,4),
    condition                         text,
    approver_role_ids                 text[] NOT NULL,
    approver_scope_level              text CONSTRAINT rule_approver_scope_level_chk CHECK (approver_scope_level IN ('venue', 'department', 'region', 'tenant')),
    mode                              text NOT NULL CONSTRAINT rule_mode_chk CHECK (mode IN ('sequential', 'parallel', 'consensus', 'majority')),
    levels                            integer DEFAULT 1,
    requires_mfa                      boolean DEFAULT false,
    requires_signature                boolean DEFAULT false,
    sla_minutes                       integer,
    escalate_after_minutes            integer,
    escalate_to_role_ids              text[],
    expires_after_minutes             integer,
    external_provider_id              uuid,
    matrix_id                         uuid NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.signature (
    id                                uuid PRIMARY KEY,
    request_id                        uuid,
    signed_by                         uuid,
    signed_at                         timestamptz,
    method                            text CONSTRAINT signature_method_chk CHECK (method IN ('platformKey', 'uaePass', 'externalCertificate', 'drawnSignature')),
    payload_hash                      text,
    signature                         text,
    certificate_subject               text,
    is_step_up_verified               boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.sla_policy (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    applies_to_request_kinds          text[],
    target_minutes                    integer,
    business_hours_only               boolean DEFAULT true,
    calendar_id                       uuid,
    first_reminder_at_percent         integer,
    second_reminder_at_percent        integer,
    escalate_at_percent               integer,
    on_breach                         text DEFAULT 'escalate' CONSTRAINT sla_policy_on_breach_chk CHECK (on_breach IN ('notifyOnly', 'escalate', 'autoApprove', 'autoReject')),
    is_auto_action_allowed            boolean DEFAULT false,
    escalation_group_id               uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.step_up_policy (
    operation_id                      text NOT NULL,
    required                          text NOT NULL,
    contract_floor                    text,
    scope_level                       text CONSTRAINT step_up_policy_scope_level_chk CHECK (scope_level IN ('tenant', 'region', 'venue')),
    reason                            text CONSTRAINT step_up_policy_reason_chk CHECK (char_length(reason) <= 512),
    set_by                            uuid,
    set_at                            timestamptz,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.workflow_definition (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text NOT NULL CONSTRAINT workflow_definition_name_chk CHECK (char_length(name) <= 200),
    kind                              text NOT NULL CONSTRAINT workflow_definition_kind_chk CHECK (kind IN ('approvalWorkflow', 'operationalWorkflow', 'crossModuleWorkflow')),
    source_module                     text NOT NULL CONSTRAINT workflow_definition_source_module_chk CHECK (source_module IN ('ticketing', 'pricing', 'finance', 'procurement', 'crm', 'resourceManagement', 'fnb', 'retail', 'groupSales', 'customerService', 'membership', 'wallet', 'waiver', 'subscriptionLicensing')),
    business_process                  text CONSTRAINT workflow_definition_business_process_chk CHECK (char_length(business_process) <= 200),
    owner_principal_id                uuid,
    priority                          text CONSTRAINT workflow_definition_priority_chk CHECK (char_length(priority) <= 30),
    active_workflow_version_id        uuid,
    status                            text NOT NULL CONSTRAINT workflow_definition_status_chk CHECK (status IN ('draft', 'testing', 'review', 'pendingApproval', 'approved', 'scheduled', 'active', 'suspended', 'retired')),
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 15 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.workflow_exception (
    id                                uuid PRIMARY KEY NOT NULL,
    workflow_instance_id              uuid NOT NULL,
    workflow_step_execution_id        uuid,
    error_type                        text NOT NULL CONSTRAINT workflow_exception_error_type_chk CHECK (error_type IN ('businessRuleFailure', 'missingData', 'missingApprover', 'permissionFailure', 'integrationFailure', 'timeout', 'actionFailure', 'invalidState', 'duplicateEvent', 'serviceUnavailable', 'configurationError')),
    source_module                     text CONSTRAINT workflow_exception_source_module_chk CHECK (source_module IN ('ticketing', 'pricing', 'finance', 'procurement', 'crm', 'resourceManagement', 'fnb', 'retail', 'groupSales', 'customerService', 'membership', 'wallet', 'waiver', 'subscriptionLicensing')),
    detail                            text CONSTRAINT workflow_exception_detail_chk CHECK (char_length(detail) <= 2000),
    business_impact                   text CONSTRAINT workflow_exception_business_impact_chk CHECK (char_length(business_impact) <= 500),
    priority                          text CONSTRAINT workflow_exception_priority_chk CHECK (char_length(priority) <= 30),
    owner_principal_id                uuid,
    retry_count                       integer DEFAULT 0,
    status                            text NOT NULL CONSTRAINT workflow_exception_status_chk CHECK (status IN ('open', 'retrying', 'escalated', 'resolved', 'cancelled')),
    raised_at                         timestamptz NOT NULL,
    resolved_at                       timestamptz,
    resolved_by                       uuid,
    scope_path                        ltree NOT NULL
);

-- Holds 26 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.workflow_instance (
    id                                uuid PRIMARY KEY NOT NULL,
    workflow_definition_id            uuid NOT NULL,
    workflow_version_id               uuid NOT NULL,
    workflow_trigger_id               uuid,
    source_module                     text NOT NULL CONSTRAINT workflow_instance_source_module_chk CHECK (source_module IN ('ticketing', 'pricing', 'finance', 'procurement', 'crm', 'resourceManagement', 'fnb', 'retail', 'groupSales', 'customerService', 'membership', 'wallet', 'waiver', 'subscriptionLicensing')),
    business_object_type              text CONSTRAINT workflow_instance_business_object_type_chk CHECK (char_length(business_object_type) <= 100),
    business_object_id                text,
    initiated_by_principal_id         uuid,
    owner_principal_id                uuid,
    priority                          text CONSTRAINT workflow_instance_priority_chk CHECK (char_length(priority) <= 30),
    current_node_id                   text,
    status                            text NOT NULL CONSTRAINT workflow_instance_status_chk CHECK (status IN ('running', 'waitingApproval', 'waitingTask', 'waitingSystem', 'escalated', 'failed', 'completed', 'cancelled')),
    correlation_id                    text NOT NULL CONSTRAINT workflow_instance_correlation_id_chk CHECK (char_length(correlation_id) <= 100),
    sla_policy_id                     uuid,
    sla_due_at                        timestamptz,
    is_sla_breached                   boolean DEFAULT false,
    escalation_level                  integer DEFAULT 0,
    first_reminder_at                 timestamptz,
    second_reminder_at                timestamptz,
    manager_escalated_at              timestamptz,
    executive_escalated_at            timestamptz,
    sla_outcome                       text CONSTRAINT workflow_instance_sla_outcome_chk CHECK (sla_outcome IN ('metWithinTarget', 'metAfterReminder', 'metAfterEscalation', 'breached')),
    started_at                        timestamptz NOT NULL,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz
);

-- Holds 20 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.workflow_intervention (
    id                                uuid PRIMARY KEY NOT NULL,
    workflow_instance_id              uuid NOT NULL,
    workflow_step_execution_id        uuid,
    workflow_exception_id             uuid,
    action                            text NOT NULL CONSTRAINT workflow_intervention_action_chk CHECK (action IN ('reassign', 'retryStep', 'skipStep', 'resume', 'cancel', 'extendSla', 'addBackupApprover', 'changePriority', 'escalateException')),
    reason                            text NOT NULL CONSTRAINT workflow_intervention_reason_chk CHECK (char_length(reason) <= 500),
    from_status                       text CONSTRAINT workflow_intervention_from_status_chk CHECK (from_status IN ('running', 'waitingApproval', 'waitingTask', 'waitingSystem', 'escalated', 'failed', 'completed', 'cancelled')),
    to_status                         text CONSTRAINT workflow_intervention_to_status_chk CHECK (to_status IN ('running', 'waitingApproval', 'waitingTask', 'waitingSystem', 'escalated', 'failed', 'completed', 'cancelled')),
    assignee_principal_id             uuid,
    previous_assignee_principal_id    uuid,
    alternative_node_id               text,
    previous_input                    jsonb,
    corrected_input                   jsonb,
    sla_due_at_before                 timestamptz,
    sla_due_at_after                  timestamptz,
    previous_priority                 text CONSTRAINT workflow_intervention_previous_priority_chk CHECK (char_length(previous_priority) <= 30),
    priority                          text CONSTRAINT workflow_intervention_priority_chk CHECK (char_length(priority) <= 30),
    actor_principal_id                uuid NOT NULL,
    acted_at                          timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

-- Holds 19 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.workflow_step_execution (
    id                                uuid PRIMARY KEY NOT NULL,
    workflow_instance_id              uuid NOT NULL,
    node_id                           text NOT NULL,
    step_name                         text CONSTRAINT workflow_step_execution_step_name_chk CHECK (char_length(step_name) <= 200),
    node_type                         text NOT NULL CONSTRAINT workflow_step_execution_node_type_chk CHECK (node_type IN ('start', 'trigger', 'task', 'decision', 'approval', 'systemAction', 'notification', 'wait', 'timer', 'parallelBranch', 'merge', 'escalation', 'subWorkflow', 'end')),
    service                           text CONSTRAINT workflow_step_execution_service_chk CHECK (char_length(service) <= 100),
    action                            text CONSTRAINT workflow_step_execution_action_chk CHECK (char_length(action) <= 200),
    assigned_to_principal_id          uuid,
    approval_request_id               text,
    input_payload                     jsonb,
    output_payload                    jsonb,
    decision                          text CONSTRAINT workflow_step_execution_decision_chk CHECK (char_length(decision) <= 100),
    rule_evaluations                  integer DEFAULT 0,
    retries                           integer DEFAULT 0,
    failure_handling                  text CONSTRAINT workflow_step_execution_failure_handling_chk CHECK (failure_handling IN ('waits', 'retries', 'rollsBack', 'continuesPartially', 'requiresHumanIntervention')),
    status                            text NOT NULL CONSTRAINT workflow_step_execution_status_chk CHECK (status IN ('notStarted', 'running', 'waiting', 'successful', 'failed', 'compensated')),
    started_at                        timestamptz,
    completed_at                      timestamptz,
    scope_path                        ltree NOT NULL
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.workflow_trigger (
    id                                uuid PRIMARY KEY NOT NULL,
    workflow_definition_id            uuid NOT NULL,
    trigger_type                      text NOT NULL CONSTRAINT workflow_trigger_trigger_type_chk CHECK (trigger_type IN ('event', 'dataCondition', 'schedule', 'manual')),
    trigger_definition                text CONSTRAINT workflow_trigger_trigger_definition_chk CHECK (char_length(trigger_definition) <= 1000),
    allowed_actions                   text[],
    on_failure                        text CONSTRAINT workflow_trigger_on_failure_chk CHECK (on_failure IN ('retry', 'rollback', 'compensate', 'exceptionQueue', 'humanIntervention')),
    max_retries                       integer,
    is_active                         boolean DEFAULT true,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

-- Holds 26 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.workflow_version (
    id                                uuid PRIMARY KEY NOT NULL,
    workflow_definition_id            uuid NOT NULL,
    version                           integer NOT NULL,
    definition                        jsonb NOT NULL,
    node_types                        text[],
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    status                            text NOT NULL CONSTRAINT workflow_version_status_chk CHECK (status IN ('draft', 'tested', 'businessReview', 'technicalValidation', 'approval', 'scheduled', 'active', 'suspended', 'retired')),
    change_reason                     text CONSTRAINT workflow_version_change_reason_chk CHECK (char_length(change_reason) <= 1000),
    what_changed                      text CONSTRAINT workflow_version_what_changed_chk CHECK (char_length(what_changed) <= 2000),
    changed_areas                     text[],
    risk_classification               text CONSTRAINT workflow_version_risk_classification_chk CHECK (char_length(risk_classification) <= 30),
    test_results                      text CONSTRAINT workflow_version_test_results_chk CHECK (char_length(test_results) <= 2000),
    business_owner_principal_id       uuid,
    technical_owner_principal_id      uuid,
    approval_request_id               text,
    rollout_scope                     text CONSTRAINT workflow_version_rollout_scope_chk CHECK (rollout_scope IN ('allScopes', 'selectedTenant', 'selectedVenue', 'selectedBrand', 'controlledRollout')),
    scope_ids                         text[],
    created_by                        uuid,
    tested_by                         uuid,
    approved_by                       uuid,
    published_by                      uuid,
    published_at                      timestamptz,
    scope_path                        ltree NOT NULL,
    created_at                        timestamptz,
    updated_at                        timestamptz
);

