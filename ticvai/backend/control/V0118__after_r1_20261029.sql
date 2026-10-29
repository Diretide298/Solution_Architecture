-- V0118 -- control database, after r1 (9cec72d) (20261029).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 1 table(s), 0 column(s), 0 index(es), 1 other statement(s).

CREATE TABLE IF NOT EXISTS control.platform_approval_rule (
    kind                              text NOT NULL CONSTRAINT platform_approval_rule_kind_chk CHECK (kind IN ('configurationChange')),
    subject_type                      text NOT NULL CONSTRAINT platform_approval_rule_subject_type_chk CHECK (subject_type IN ('tenant')),
    approver_permission               text NOT NULL CONSTRAINT platform_approval_rule_approver_permission_chk CHECK (approver_permission IN ('PLATFORM_TENANT_MANAGE')),
    minimum_approvals                 integer NOT NULL DEFAULT 2,
    is_active                         boolean NOT NULL DEFAULT true,
    CONSTRAINT platform_approval_rule_pkey PRIMARY KEY (kind, subject_type)
);

INSERT INTO control.platform_approval_rule (kind, subject_type, approver_permission, minimum_approvals, is_active) VALUES ('configurationChange', 'tenant', 'PLATFORM_TENANT_MANAGE', 2, true) ON CONFLICT DO NOTHING;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0118', 'after r1 (9cec72d): 1 table(s), 0 column(s), 0 index(es), 1 other statement(s)', '0734fd490afa0778d956476a7e7e5376172830ced0580ddffd834eefa923ffc9')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP TABLE IF EXISTS control.platform_approval_rule;
-- DELETE FROM platform.schema_version WHERE version = 'V0118';
