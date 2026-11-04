-- V0128a -- control database, r14, before V0129 (20261104).
-- **Written by hand at the r14 integration (4 November 2026), from the lanes' posted decisions; not derived.**
-- The databases have rows, so this file does what tools/derive-ddl.py cannot: it counts the rows a new rule would
-- refuse and stops with a message naming the table and the count (never deleting or rewriting such a row: decided
-- overnight under the lead's 4 November instruction, "take the recommended decision unless its very very important"),
-- fills what can be filled from the rows' own data, and only then makes the column NOT NULL or validates the CHECK.
-- Every block is guarded on its table and columns, so the file applies as one transaction, twice, on any database.
-- It sorts before V0129 (as derive-ddl's early names files do), so a duplicate stops here, by name and
-- count, before V0129's unique indexes fail on it. It changes nothing; its rollback has nothing to undo.
-- 3 count(s), 0 change(s).

-- control.api_client: client_id unique (api_client_client_id_uniq, ADAM CR-571; CHG-CR571-001)
DO $data$ DECLARE n bigint; BEGIN IF to_regclass('control.api_client') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_client' AND column_name = 'client_id') THEN
  SELECT count(*) INTO n FROM (SELECT client_id FROM control.api_client WHERE client_id IS NOT NULL GROUP BY client_id HAVING count(*) > 1) q;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: control.api_client has % client_id value(s) held by more than one row; the unique index cannot be built (CR-571). Nothing was changed.', n; END IF;
END IF; END $data$;

-- control.api_version: version unique (api_version_version_uniq, ADAM CR-570; CHG-CR570-001)
DO $data$ DECLARE n bigint; BEGIN IF to_regclass('control.api_version') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_version' AND column_name = 'version') THEN
  SELECT count(*) INTO n FROM (SELECT version FROM control.api_version GROUP BY version HAVING count(*) > 1) q;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: control.api_version has % version value(s) held by more than one row; the unique index cannot be built (CR-570). Nothing was changed.', n; END IF;
END IF; END $data$;

-- control.developer_member: one active member per email (developer_member_email_uniq, ADAM CR-569; CHG-CR569-002)
DO $data$ DECLARE n bigint; BEGIN IF to_regclass('control.developer_member') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'developer_member' AND column_name = 'email') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'developer_member' AND column_name = 'status') THEN
  SELECT count(*) INTO n FROM (SELECT lower(email) FROM control.developer_member WHERE status = 'active' GROUP BY lower(email) HAVING count(*) > 1) q;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: control.developer_member has % email(s) active in more than one developer account; the unique index cannot be built and the decision does not say which gives way (CR-569). Nothing was changed.', n; END IF;
END IF; END $data$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0128a', 'r14 checks before V0129: duplicate client_id, version and active developer email counted, nothing changed', 'd756287d965fd108cb98ba493d7a2c6f95fc87fe8fa3d8af7e5435b6deff5c20')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DELETE FROM platform.schema_version WHERE version = 'V0128a';
