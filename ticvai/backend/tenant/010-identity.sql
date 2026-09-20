-- identity — 24 tables
-- **Derived. Do not hand-edit.**

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_decision (
    id                                uuid PRIMARY KEY,
    effect                            text,
    decided_at                        timestamptz,
    decided_by                        text,
    principal_id                      uuid,
    permission                        text,
    scope_path                        text,
    observed_attributes               jsonb,
    override_id                       uuid,
    latency_ms                        integer,
    scope_path_index                  text
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_override (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid,
    scope_path                        text,
    permissions                       text[],
    reason                            text,
    created_by                        uuid,
    created_at                        timestamptz,
    expires_at                        timestamptz,
    revoked_at                        timestamptz,
    alerted_to                        text[]
);

-- Holds 16 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_policy (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    is_template                       boolean,
    permissions                       text[],
    combining                         text,
    effect                            text NOT NULL,
    priority                          integer,
    scope_path                        text,
    applies_to_role_ids               text[],
    status                            text,
    version                           integer,
    effective_from                    timestamptz,
    effective_to                      timestamptz,
    delegated_admin_role_ids          text[]
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.access_policy_version (
    policy_id                         uuid,
    version                           integer,
    changed_by                        uuid,
    changed_at                        timestamptz,
    reason                            text,
    approved_by                       uuid,
    previous                          uuid,
    current                           uuid,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Written by the authorisation layer on every call, not by an operation Hangs off: reaches
-- identity.principal through its keys; references identity.principal.
CREATE TABLE IF NOT EXISTS identity.authz_audit (
    id                                uuid PRIMARY KEY NOT NULL,
    actor_principal_id                uuid,
    subject_principal_id              uuid
);

-- Holds 9 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.benefit_usage (
    id                                uuid PRIMARY KEY,
    customer_membership_id            uuid NOT NULL,
    membership_benefit_id             uuid NOT NULL,
    quantity                          numeric(18,4) NOT NULL,
    source_type                       text,
    source_order_id                   uuid,
    used_at                           timestamptz NOT NULL,
    remaining_quantity                numeric(18,4),
    notes                             text
);

-- Holds 12 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.customer_membership (
    id                                uuid PRIMARY KEY,
    customer_id                       uuid NOT NULL,
    entitlement_template_id           uuid NOT NULL,
    number                            text NOT NULL,
    source_order_id                   uuid,
    start_at                          timestamptz NOT NULL,
    expires_at                        timestamptz,
    status                            text NOT NULL,
    auto_renew                        boolean NOT NULL,
    cancelled_at                      timestamptz,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- One person acting for another, or for a scope they do not own. A parent managing a child's
-- membership, a manager covering another venue for a week. Renamed from grant, which is a verb, a
-- subsidy and a permission depending on who reads it
CREATE TABLE IF NOT EXISTS identity.delegated_access (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid,
    role_id                           uuid,
    permission                        text NOT NULL,
    subject_id                        uuid,
    over_subject_id                   uuid,
    over_object_ref                   text,
    delegation_kind                   text,
    quota                             integer,
    is_revocable_by_subject           boolean,
    scope_path                        text NOT NULL,
    effect                            text NOT NULL,
    permission_id                     uuid,
    revoked_at                        timestamptz,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    created_by_principal_id           uuid,
    created_at                        timestamptz,
    granted_by                        uuid NOT NULL,
    revoked_by                        uuid NOT NULL,
    scope_id                          uuid NOT NULL
);

-- Holds 7 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.membership_history (
    id                                uuid PRIMARY KEY,
    customer_membership_id            uuid NOT NULL,
    from_status                       text,
    to_status                         text NOT NULL,
    reason                            text,
    changed_by_principal_id           uuid,
    changed_at                        timestamptz NOT NULL
);

-- an issued MFA challenge and its outcome Hangs off: reaches identity.principal through its keys;
-- references identity.principal. Reached by: 1 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS identity.mfa_challenge (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL
);

-- A second factor a principal has enrolled. Guests may enrol too, from 26 August
CREATE TABLE IF NOT EXISTS identity.mfa_method (
    id                                uuid PRIMARY KEY NOT NULL,
    kind                              text NOT NULL,
    label                             text,
    masked_target                     text,
    is_active                         boolean NOT NULL,
    is_primary                        boolean,
    enrolled_at                       timestamptz NOT NULL,
    last_used_at                      timestamptz,
    principal_id                      uuid
);

-- hashed, single-use, never retrievable Hangs off: reaches identity.principal through its keys;
-- references identity.principal. Reached by: 2 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS identity.mfa_recovery_code (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid
);

-- Holds 11 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.module (
    id                                uuid PRIMARY KEY,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    parent_module_id                  uuid,
    type                              text NOT NULL,
    sort_order                        integer NOT NULL,
    is_system_module                  boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- a one-time code sent to a guest contact point Hangs off: reaches identity.principal through its
-- keys; references pii.subject. Reached by: 2 operations read it and 2 write it.
CREATE TABLE IF NOT EXISTS identity.otp_challenge (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL
);

-- Length, breach check, lockout and step-up (BL-144). Modelled on NIST SP 800-63B rather than
-- habit — length beats composition, and forced rotation makes passwords worse
CREATE TABLE IF NOT EXISTS identity.password_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    scope_path                        text NOT NULL,
    min_length                        integer NOT NULL,
    require_breach_check              boolean,
    max_age_days                      integer,
    recovery_methods                  text[],
    max_concurrent_sessions           integer,
    device_restriction                jsonb,
    lockout_after_attempts            integer,
    lockout_minutes                   integer,
    force_change_on_first_logon       boolean,
    reuse_prevention_count            integer,
    mfa_required_for_permissions      text[]
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.permission (
    id                                uuid PRIMARY KEY,
    module_id                         uuid NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    action                            text NOT NULL,
    description                       text,
    is_system                         boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

-- A person who can be authorised — staff, partner, platform operator. The most referenced table in
-- the package at 122 incoming columns, because almost everything records who did it. Not a guest:
-- a guest is a pii.subject, and ADR-0023 keeps them apart so a data-subject request has one place
-- to answer from
CREATE TABLE IF NOT EXISTS identity.principal (
    id                                uuid PRIMARY KEY NOT NULL,
    username                          text NOT NULL,
    display_name                      text NOT NULL,
    is_active                         boolean NOT NULL,
    valid_from                        timestamptz,
    valid_to                          timestamptz,
    primary_role_id                   uuid,
    last_login_at                     timestamptz,
    home_scope_id                     uuid
);

-- a credential hash has no response it belongs in Hangs off: a child of identity.principal;
-- reaches identity.principal through its keys; references identity.principal. Reached by: 1
-- operations read it and 0 write it.
CREATE TABLE IF NOT EXISTS identity.principal_credential (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid
);

-- Holds 10 columns. No description has been written for this table — the name is the only thing
-- saying what it is
CREATE TABLE IF NOT EXISTS identity.refresh_token (
    id                                uuid PRIMARY KEY,
    principal_id                      uuid NOT NULL,
    hash                              text NOT NULL,
    expires_at                        timestamptz NOT NULL,
    created_at                        timestamptz NOT NULL,
    created_by_ip                     text,
    revoked_at                        timestamptz,
    revoked_by_ip                     text,
    revocation_reason                 text,
    replaced_by_token_id              uuid
);

-- A named set of permissions, inheritable. A principal holds roles at scopes; the resolution walks
-- the org tree upward until something answers
CREATE TABLE IF NOT EXISTS identity.role (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text NOT NULL,
    description                       text,
    inherits_from_role_id             uuid,
    is_system                         boolean,
    principal_count                   integer,
    grant_count                       integer
);

-- child of role, returned nested Hangs off: a child of identity.role; reaches identity.principal
-- through its keys; references identity.principal, identity.role. Reached by: 2 operations read it
-- and 1 write it.
CREATE TABLE IF NOT EXISTS identity.role_permission (
    role_id                           uuid NOT NULL,
    permission                        text NOT NULL,
    granted_at                        timestamptz,
    granted_by_principal_id           uuid,
    is_active                         boolean,
    id                                uuid PRIMARY KEY NOT NULL
);

-- Which permissions may not be held together (BL-147, 3.3.31). Checked at grant time, not use time
-- — discovering the conflict when somebody exercises it means it already existed
CREATE TABLE IF NOT EXISTS identity.segregation_rule (
    id                                uuid PRIMARY KEY NOT NULL,
    name                              text,
    permission_a                      text NOT NULL,
    permission_b                      text NOT NULL,
    severity                          text NOT NULL,
    rationale                         text,
    scope_sensitive                   boolean,
    allow_with_compensating_control   boolean,
    scope_path                        text
);

-- Which provider group becomes which role. The join that stops SSO meaning manual role assignment
CREATE TABLE IF NOT EXISTS identity.sso_group_mapping (
    id                                uuid PRIMARY KEY,
    external_group                    text NOT NULL,
    role_id                           uuid NOT NULL,
    scope_path                        text,
    provider_id                       uuid,
    scope_id                          uuid
);

-- A tenant’s own identity provider. A guest arriving through UAE Pass is verified in a way an
-- email never is
CREATE TABLE IF NOT EXISTS identity.sso_provider (
    icon_asset_ref                    text,
    scope_path                        text,
    id                                uuid PRIMARY KEY NOT NULL,
    display_name                      text NOT NULL,
    protocol                          text NOT NULL,
    metadata_url                      text,
    issuer                            text,
    client_id                         text,
    client_secret_ref                 text,
    auto_provision_principals         boolean,
    is_enforced                       boolean,
    is_active                         boolean
);

