-- approvals — 15 tables
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
-- identity.principal. Reached by: 7 operations read it and 1 write it.
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

-- Standing in for an approver. Always time-bounded — an open-ended delegation is one nobody
-- remembers Hangs off: reaches approvals.request through its keys; references identity.principal.
-- Reached by: 5 operations read it and 2 write it; 1 tables reference it.
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
-- reaches approvals.request through its keys; references approvals.request. Reached by: 1
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

-- What requires approval where. Versioned, because a request must be decided by the rules it was
-- raised under Hangs off: reaches approvals.request through its keys. Reached by: 4 operations
-- read it and 1 write it; 1 tables reference it.
CREATE TABLE IF NOT EXISTS approvals.matrix (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL CONSTRAINT matrix_kind_chk CHECK (kind IN ('refund', 'priceOverride', 'discountOverride', 'complimentaryTicket', 'membershipCancellation', 'accessPermissionChange', 'configurationChange', 'aiRecommendation', 'shiftVariance', 'releasePromotion', 'requisition', 'stockWriteOff', 'journalEntry', 'periodReopen', 'tenantMigration')),
    scope_level                       text NOT NULL CONSTRAINT matrix_scope_level_chk CHECK (scope_level IN ('tenant', 'region', 'venue')),
    scope_path                        ltree NOT NULL,
    version                           integer,
    is_active                         boolean
);

-- One request per action needing authorisation. The subject is a reference, never a copy Hangs
-- off: a root — nothing above it in its schema; references identity.principal. Reached by: 7
-- operations read it and 8 write it; 16 tables reference it; written by 3 contracts — approvals,
-- subscription, workforce.
CREATE TABLE IF NOT EXISTS approvals.request (
    id                                text PRIMARY KEY NOT NULL,
    kind                              text NOT NULL CONSTRAINT request_kind_chk CHECK (kind IN ('refund', 'priceOverride', 'discountOverride', 'complimentaryTicket', 'membershipCancellation', 'accessPermissionChange', 'configurationChange', 'aiRecommendation', 'shiftVariance', 'releasePromotion', 'requisition', 'stockWriteOff', 'journalEntry', 'periodReopen', 'tenantMigration')),
    reroute_on_no_approver            boolean DEFAULT true,
    out_of_office_delegate_id         uuid,
    allow_email_approval              boolean DEFAULT false,
    reopened_from                     uuid,
    status                            text NOT NULL CONSTRAINT request_status_chk CHECK (status IN ('draft', 'pending', 'escalated', 'approved', 'rejected', 'withdrawn', 'expired', 'cancelled')),
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
    completed_at                      timestamptz
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
-- off: reaches approvals.request through its keys; references approvals.matrix. Reached by: 6
-- operations read it and 1 write it; 2 tables reference it.
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

