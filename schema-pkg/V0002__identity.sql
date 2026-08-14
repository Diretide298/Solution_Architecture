-- =============================================================================
-- V0002 — Identity & Authorisation
--
-- Principals, roles, grants, SSO and MFA.
--
-- The authorisation model is documented in project-bible/architecture/specs/
-- permission-resolution.md and enforced by PermissionResolver.cs. This schema
-- stores the inputs to that resolution; it does not attempt to resolve.
--
-- Deliberate absences:
--   * No effective_permissions table. Resolution happens at login and caches in
--     Redis. A materialised permission set is stale the moment a grant changes,
--     and nobody notices until someone keeps access they should have lost.
--   * No sessions table. Sessions live in Redis (SessionRegistry.cs) because
--     single-session enforcement needs an atomic claim, and a database row plus
--     application check is a race.
--
-- ROLLBACK at the foot of the file.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Principals. A person or a service that can authenticate.
-- -----------------------------------------------------------------------------
CREATE TYPE identity.principal_kind AS ENUM ('staff', 'service', 'partner');

CREATE TABLE identity.principal (
    id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    kind                    identity.principal_kind NOT NULL DEFAULT 'staff',
    username                text NOT NULL,
    employee_reference      text,
    display_name            text NOT NULL,
    home_scope_id           uuid NOT NULL REFERENCES platform.scope_node (id),
    home_scope_path         ltree NOT NULL,
    is_active               boolean NOT NULL DEFAULT true,
    deactivated_at          timestamptz,
    deactivated_reason      text,
    must_change_credential  boolean NOT NULL DEFAULT false,
    requires_mfa            boolean NOT NULL DEFAULT false,
    last_login_at           timestamptz,
    failed_login_count      smallint NOT NULL DEFAULT 0,
    locked_until            timestamptz,
    created_at              timestamptz NOT NULL DEFAULT now(),
    updated_at              timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT principal_username_unique UNIQUE (username),
    CONSTRAINT principal_deactivation_reason
        CHECK (is_active OR deactivated_reason IS NOT NULL)
);

COMMENT ON COLUMN identity.principal.home_scope_path IS
  'Denormalised from scope_node for RLS. Kept in step by trigger — a principal '
  'moved between venues must not retain visibility of the old one.';

COMMENT ON CONSTRAINT principal_deactivation_reason ON identity.principal IS
  'Deactivation always carries a reason. "Who disabled this account and why" is '
  'the first question asked after an incident.';

CREATE INDEX principal_scope_gist ON identity.principal USING gist (home_scope_path);
CREATE INDEX principal_active     ON identity.principal (is_active) WHERE is_active;
CREATE INDEX principal_employee   ON identity.principal (employee_reference)
    WHERE employee_reference IS NOT NULL;

ALTER TABLE identity.principal ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity.principal FORCE ROW LEVEL SECURITY;
CREATE POLICY principal_scope ON identity.principal
    USING (platform.in_scope(home_scope_path));

-- Credentials are separate. A principal row is read constantly for display;
-- a credential hash should be read only when authenticating.
CREATE TABLE identity.principal_credential (
    principal_id        uuid PRIMARY KEY REFERENCES identity.principal (id) ON DELETE CASCADE,
    credential_hash     text NOT NULL,
    algorithm           text NOT NULL DEFAULT 'argon2id',
    rotated_at          timestamptz NOT NULL DEFAULT now(),
    expires_at          timestamptz,
    previous_hashes     text[] NOT NULL DEFAULT '{}'
);

COMMENT ON COLUMN identity.principal_credential.previous_hashes IS
  'Bounded history for reuse prevention. Trimmed by the application to the '
  'configured depth; unbounded growth here is a slow leak of hashes.';

ALTER TABLE identity.principal_credential ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity.principal_credential FORCE ROW LEVEL SECURITY;
CREATE POLICY principal_credential_scope ON identity.principal_credential
    USING (EXISTS (
        SELECT 1 FROM identity.principal p
        WHERE p.id = principal_id AND platform.in_scope(p.home_scope_path)
    ));

-- -----------------------------------------------------------------------------
-- Roles. A named set of permissions.
-- -----------------------------------------------------------------------------
CREATE TABLE identity.role (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    code                text NOT NULL,
    name                text NOT NULL,
    description         text,
    is_system           boolean NOT NULL DEFAULT false,
    scope_level         platform.scope_level,
    is_active           boolean NOT NULL DEFAULT true,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT role_code_unique UNIQUE (code)
);

COMMENT ON COLUMN identity.role.is_system IS
  'Shipped with the platform. Cannot be amended or deleted, only cloned. '
  'Prevents a tenant editing the role their own administrator depends on.';

COMMENT ON COLUMN identity.role.scope_level IS
  'The level this role is intended to be granted at. Advisory — a venue manager '
  'role granted at region level is a configuration smell, not an error.';

-- Permissions as text, validated against the contract enum in CI rather than a
-- lookup table. A foreign key here would mean a migration for every new
-- permission, and the enum in shared/permissions.yaml is already the source.
CREATE TABLE identity.role_permission (
    role_id             uuid NOT NULL REFERENCES identity.role (id) ON DELETE CASCADE,
    permission          text NOT NULL,
    effect              text NOT NULL DEFAULT 'allow' CHECK (effect IN ('allow', 'deny')),
    PRIMARY KEY (role_id, permission)
);

COMMENT ON COLUMN identity.role_permission.effect IS
  'Deny wins over allow at every level (permission-resolution.md R2). Stored '
  'per row so a role can carve an exception out of a broader grant.';

CREATE INDEX role_permission_perm ON identity.role_permission (permission);

-- -----------------------------------------------------------------------------
-- Grants. A principal holds a role at a scope.
-- -----------------------------------------------------------------------------
CREATE TABLE identity.grant (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    principal_id        uuid NOT NULL REFERENCES identity.principal (id) ON DELETE CASCADE,
    role_id             uuid NOT NULL REFERENCES identity.role (id),
    scope_id            uuid NOT NULL REFERENCES platform.scope_node (id),
    scope_path          ltree NOT NULL,
    granted_by          uuid REFERENCES identity.principal (id),
    granted_at          timestamptz NOT NULL DEFAULT now(),
    valid_from          timestamptz NOT NULL DEFAULT now(),
    valid_to            timestamptz,
    revoked_at          timestamptz,
    revoked_by          uuid REFERENCES identity.principal (id),
    revoke_reason       text,
    CONSTRAINT grant_validity CHECK (valid_to IS NULL OR valid_to > valid_from),
    CONSTRAINT grant_revocation CHECK (revoked_at IS NULL OR revoke_reason IS NOT NULL)
);

COMMENT ON TABLE identity.grant IS
  'Grants are never deleted, only revoked. "Who had access on the day of the '
  'incident" is unanswerable against a table that deletes rows.';

COMMENT ON COLUMN identity.grant.valid_to IS
  'Temporary elevation — cover for absence, a contractor engagement. Expiry is '
  'evaluated at login (R10), so an expired grant cannot be resolved even if '
  'nobody remembered to revoke it.';

CREATE INDEX grant_principal ON identity.grant (principal_id)
    WHERE revoked_at IS NULL;
CREATE INDEX grant_scope_gist ON identity.grant USING gist (scope_path);
CREATE INDEX grant_expiring   ON identity.grant (valid_to)
    WHERE revoked_at IS NULL AND valid_to IS NOT NULL;

-- One live grant of a role at a scope. A duplicate is a data defect, not a
-- stronger grant.
CREATE UNIQUE INDEX grant_unique_live
    ON identity.grant (principal_id, role_id, scope_id)
    WHERE revoked_at IS NULL;

ALTER TABLE identity.grant ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity.grant FORCE ROW LEVEL SECURITY;
CREATE POLICY grant_scope ON identity.grant
    USING (platform.in_scope(scope_path));

-- -----------------------------------------------------------------------------
-- SSO. Per tenant, because a tenant's Azure AD is theirs, not ours.
-- -----------------------------------------------------------------------------
CREATE TABLE identity.sso_provider (
    id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name            text NOT NULL,
    protocol                text NOT NULL CHECK (protocol IN ('oidc', 'saml2')),
    metadata_url            text,
    issuer                  text,
    client_id               text,
    client_secret_ref       text,
    auto_provision          boolean NOT NULL DEFAULT false,
    is_enforced             boolean NOT NULL DEFAULT false,
    is_active               boolean NOT NULL DEFAULT true,
    created_at              timestamptz NOT NULL DEFAULT now()
);

COMMENT ON COLUMN identity.sso_provider.client_secret_ref IS
  'Key vault reference, never the secret. A secret in a database column ends up '
  'in a backup, a replica and somebody''s laptop.';

COMMENT ON COLUMN identity.sso_provider.is_enforced IS
  'Disables password login for principals covered by this provider. Set only '
  'after at least one break-glass account is confirmed outside it.';

CREATE TABLE identity.sso_group_mapping (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id         uuid NOT NULL REFERENCES identity.sso_provider (id) ON DELETE CASCADE,
    external_group      text NOT NULL,
    role_id             uuid NOT NULL REFERENCES identity.role (id),
    scope_id            uuid NOT NULL REFERENCES platform.scope_node (id),
    CONSTRAINT sso_group_mapping_unique UNIQUE (provider_id, external_group, role_id, scope_id)
);

COMMENT ON TABLE identity.sso_group_mapping IS
  'An unmapped group grants nothing. There is deliberately no default-role '
  'column: without that rule the identity provider becomes a way to mint access '
  'nobody configured.';

-- -----------------------------------------------------------------------------
-- MFA.
-- -----------------------------------------------------------------------------
CREATE TABLE identity.mfa_method (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    principal_id        uuid NOT NULL REFERENCES identity.principal (id) ON DELETE CASCADE,
    kind                text NOT NULL CHECK (kind IN ('totp','smsOtp','emailOtp','biometric','hardwareToken')),
    label               text,
    secret_ref          text,
    masked_target       text,
    is_active           boolean NOT NULL DEFAULT false,
    is_primary          boolean NOT NULL DEFAULT false,
    enrolled_at         timestamptz NOT NULL DEFAULT now(),
    verified_at         timestamptz,
    last_used_at        timestamptz,
    CONSTRAINT mfa_active_requires_verification
        CHECK (NOT is_active OR verified_at IS NOT NULL)
);

COMMENT ON CONSTRAINT mfa_active_requires_verification ON identity.mfa_method IS
  'A method cannot be active before it is verified. Enrolling without verifying '
  'and then enforcing MFA locks the principal out of their own account.';

CREATE UNIQUE INDEX mfa_one_primary ON identity.mfa_method (principal_id)
    WHERE is_primary AND is_active;
CREATE INDEX mfa_principal ON identity.mfa_method (principal_id) WHERE is_active;

CREATE TABLE identity.mfa_recovery_code (
    principal_id        uuid NOT NULL REFERENCES identity.principal (id) ON DELETE CASCADE,
    code_hash           text NOT NULL,
    used_at             timestamptz,
    PRIMARY KEY (principal_id, code_hash)
);

COMMENT ON TABLE identity.mfa_recovery_code IS
  'Hashed, single-use. Returned once at enrolment and never retrievable — a '
  'recovery code that can be re-read is a second password.';

ALTER TABLE identity.mfa_method ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity.mfa_method FORCE ROW LEVEL SECURITY;
CREATE POLICY mfa_method_scope ON identity.mfa_method
    USING (EXISTS (
        SELECT 1 FROM identity.principal p
        WHERE p.id = principal_id AND platform.in_scope(p.home_scope_path)
    ));

-- -----------------------------------------------------------------------------
-- Authorisation audit. Separate from the general audit log because access
-- changes are asked about far more often and by different people.
-- -----------------------------------------------------------------------------
CREATE TABLE identity.authz_audit (
    id                  char(26) PRIMARY KEY,
    occurred_at         timestamptz NOT NULL DEFAULT now(),
    actor_principal_id  uuid REFERENCES identity.principal (id),
    subject_principal_id uuid REFERENCES identity.principal (id),
    action              text NOT NULL,
    role_id             uuid,
    scope_path          ltree,
    detail              jsonb NOT NULL DEFAULT '{}'::jsonb,
    ip_address          inet
);

CREATE INDEX authz_audit_subject  ON identity.authz_audit (subject_principal_id, occurred_at DESC);
CREATE INDEX authz_audit_occurred ON identity.authz_audit (occurred_at DESC);
CREATE INDEX authz_audit_gist     ON identity.authz_audit USING gist (scope_path)
    WHERE scope_path IS NOT NULL;

-- The audit trail is scoped like everything else. A venue manager reading the
-- access log should see their venue's grants, not the region's.
--
-- scope_path is nullable here — a login or an MFA enrolment has no scope. Those
-- rows are visible to anyone who can read the log at all, which is correct:
-- there is no venue to restrict them to.
ALTER TABLE identity.authz_audit ENABLE ROW LEVEL SECURITY;
ALTER TABLE identity.authz_audit FORCE ROW LEVEL SECURITY;
CREATE POLICY authz_audit_scope ON identity.authz_audit
    USING (scope_path IS NULL OR platform.in_scope(scope_path));

-- -----------------------------------------------------------------------------
-- Keep denormalised scope paths honest.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION identity.sync_principal_scope_path()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    SELECT path INTO NEW.home_scope_path
    FROM platform.scope_node WHERE id = NEW.home_scope_id;
    IF NEW.home_scope_path IS NULL THEN
        RAISE EXCEPTION 'scope_node % not found', NEW.home_scope_id;
    END IF;
    NEW.updated_at := now();
    RETURN NEW;
END $$;

CREATE TRIGGER principal_scope_path
    BEFORE INSERT OR UPDATE OF home_scope_id ON identity.principal
    FOR EACH ROW EXECUTE FUNCTION identity.sync_principal_scope_path();

CREATE OR REPLACE FUNCTION identity.sync_grant_scope_path()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    SELECT path INTO NEW.scope_path
    FROM platform.scope_node WHERE id = NEW.scope_id;
    IF NEW.scope_path IS NULL THEN
        RAISE EXCEPTION 'scope_node % not found', NEW.scope_id;
    END IF;
    RETURN NEW;
END $$;

CREATE TRIGGER grant_scope_path
    BEFORE INSERT OR UPDATE OF scope_id ON identity.grant
    FOR EACH ROW EXECUTE FUNCTION identity.sync_grant_scope_path();

-- A scope node moving in the tree must drag its dependants with it, or RLS
-- silently evaluates against a path that no longer exists.
CREATE OR REPLACE FUNCTION platform.cascade_scope_path()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.path IS DISTINCT FROM OLD.path THEN
        UPDATE platform.scope_node
           SET path = NEW.path || subpath(path, nlevel(OLD.path))
         WHERE path <@ OLD.path AND id <> NEW.id;

        UPDATE identity.principal
           SET home_scope_path = (SELECT path FROM platform.scope_node WHERE id = home_scope_id)
         WHERE home_scope_path <@ OLD.path;

        UPDATE identity.grant
           SET scope_path = (SELECT path FROM platform.scope_node WHERE id = scope_id)
         WHERE scope_path <@ OLD.path;
    END IF;
    RETURN NEW;
END $$;

CREATE TRIGGER scope_node_cascade
    AFTER UPDATE OF path ON platform.scope_node
    FOR EACH ROW EXECUTE FUNCTION platform.cascade_scope_path();

COMMENT ON FUNCTION platform.cascade_scope_path IS
  'Reparenting is rare but it happens — a venue moves region, a department is '
  'restructured. Without this, every denormalised path beneath it goes stale and '
  'RLS starts answering the wrong question.';

INSERT INTO platform.schema_version (version, name, checksum)
VALUES ('V0002', 'identity', 'set-by-runner');

-- =============================================================================
-- ROLLBACK
-- =============================================================================
-- DROP TRIGGER IF EXISTS scope_node_cascade ON platform.scope_node;
-- DROP FUNCTION IF EXISTS platform.cascade_scope_path();
-- DROP TRIGGER IF EXISTS grant_scope_path ON identity.grant;
-- DROP FUNCTION IF EXISTS identity.sync_grant_scope_path();
-- DROP TRIGGER IF EXISTS principal_scope_path ON identity.principal;
-- DROP FUNCTION IF EXISTS identity.sync_principal_scope_path();
-- DROP TABLE IF EXISTS identity.authz_audit;
-- DROP TABLE IF EXISTS identity.mfa_recovery_code;
-- DROP TABLE IF EXISTS identity.mfa_method;
-- DROP TABLE IF EXISTS identity.sso_group_mapping;
-- DROP TABLE IF EXISTS identity.sso_provider;
-- DROP TABLE IF EXISTS identity.grant;
-- DROP TABLE IF EXISTS identity.role_permission;
-- DROP TABLE IF EXISTS identity.role;
-- DROP TABLE IF EXISTS identity.principal_credential;
-- DROP TABLE IF EXISTS identity.principal;
-- DROP TYPE IF EXISTS identity.principal_kind;
-- DELETE FROM platform.schema_version WHERE version = 'V0002';
