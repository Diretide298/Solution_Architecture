-- approvals — 7 tables
-- **Derived. Do not hand-edit.**

-- Holds 8 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS approvals.accreditation_badge (
    id                                uuid PRIMARY KEY NOT NULL,
    approval_request_id               uuid,
    holder_name                       text,
    zones                             text[],
    state                             text,
    issued_at                         timestamptz,
    expires_at                        timestamptz,
    revoked_reason                    text
);

-- Every decision at every level. Immutable once the request completes — an approval is evidence
-- Hangs off: reaches approvals.request through its keys; references approvals.request,
-- identity.principal. Reached by: 2 operations read it and 1 write it
CREATE TABLE IF NOT EXISTS approvals.decision (
    id                                uuid PRIMARY KEY,
    level                             integer NOT NULL,
    principal_id                      uuid NOT NULL,
    display_name                      text,
    is_delegate                       boolean,
    delegated_from                    uuid,
    decision                          text NOT NULL,
    comment                           text,
    reason                            text,
    used_mfa                          boolean,
    signature_ref                     text,
    decided_at                        timestamptz NOT NULL,
    request_id                        text NOT NULL
);

-- Standing in for an approver. Always time-bounded — an open-ended delegation is one nobody
-- remembers Hangs off: reaches approvals.request through its keys; references identity.principal.
-- Reached by: 4 operations read it and 2 write it
CREATE TABLE IF NOT EXISTS approvals.delegation (
    id                                uuid PRIMARY KEY,
    delegator_principal_id            uuid NOT NULL,
    delegate_principal_id             uuid NOT NULL,
    max_amount                        numeric(18,4),
    "from"                            timestamptz NOT NULL,
    "to"                              timestamptz NOT NULL,
    reason                            text,
    is_active                         boolean,
    scope_path                        text
);

-- Who was asked, when, and why it moved up. The original approver stays in the record Hangs off: a
-- child of approvals.request; reaches approvals.request through its keys; references
-- approvals.request. Reached by: 1 operations read it and 1 write it
CREATE TABLE IF NOT EXISTS approvals.escalation (
    id                                uuid PRIMARY KEY NOT NULL,
    request_id                        text NOT NULL
);

-- What requires approval where. Versioned, because a request must be decided by the rules it was
-- raised under Hangs off: reaches approvals.request through its keys. Reached by: 4 operations
-- read it and 1 write it; 1 tables reference it
CREATE TABLE IF NOT EXISTS approvals.matrix (
    id                                uuid PRIMARY KEY,
    kind                              text NOT NULL,
    scope_level                       text NOT NULL,
    scope_path                        text,
    version                           integer,
    is_active                         boolean
);

-- One request per action needing authorisation. The subject is a reference, never a copy Hangs
-- off: a root — nothing above it in its schema; references identity.principal, pii.subject.
-- Reached by: 6 operations read it and 8 write it; 7 tables reference it; written by 3 contracts —
-- approvals, subscription, workforce
CREATE TABLE IF NOT EXISTS approvals.request (
    id                                text PRIMARY KEY NOT NULL,
    kind                              text NOT NULL,
    reroute_on_no_approver            boolean,
    out_of_office_delegate_id         uuid,
    allow_email_approval              boolean,
    reopened_from                     uuid,
    status                            text NOT NULL,
    subject_contract                  text,
    subject_type                      text,
    subject_id                        uuid,
    scope_path                        text,
    summary                           text,
    amount                            numeric(18,4),
    justification                     text,
    requested_by_principal_id         uuid NOT NULL,
    matrix_version                    integer,
    mode                              text,
    current_level                     integer,
    total_levels                      integer,
    resubmitted_from_id               text,
    reopened_from_id                  text,
    sla_due_at                        timestamptz,
    sla_breached                      boolean,
    expires_at                        timestamptz,
    requested_at                      timestamptz NOT NULL,
    completed_at                      timestamptz
);

-- Ordered within a matrix. First match wins, so adding a rule cannot silently change another Hangs
-- off: reaches approvals.request through its keys; references approvals.matrix. Reached by: 5
-- operations read it and 1 write it; 1 tables reference it
CREATE TABLE IF NOT EXISTS approvals.rule (
    id                                uuid PRIMARY KEY,
    "order"                           integer NOT NULL,
    min_amount                        numeric(18,4),
    max_amount                        numeric(18,4),
    risk_score_above                  numeric(18,4),
    condition                         text,
    approver_role_ids                 text[] NOT NULL,
    approver_scope_level              text,
    mode                              text NOT NULL,
    levels                            integer,
    requires_mfa                      boolean,
    requires_signature                boolean,
    sla_minutes                       integer,
    escalate_after_minutes            integer,
    escalate_to_role_ids              text[],
    expires_after_minutes             integer,
    matrix_id                         uuid NOT NULL
);

