-- V0131 -- control database, r14, after V0129 (20261104).
-- **Written by hand at the r14 integration (4 November 2026), from the lanes' posted decisions; not derived.**
-- The databases have rows, so this file does what tools/derive-ddl.py cannot: it counts the rows a new rule would
-- refuse and stops with a message naming the table and the count (never deleting or rewriting such a row: decided
-- overnight under the lead's 4 November instruction, "take the recommended decision unless its very very important"),
-- fills what can be filled from the rows' own data, and only then makes the column NOT NULL or validates the CHECK.
-- Every block is guarded on its table and columns, so the file applies as one transaction, twice, on any database.
-- 3 column(s) made NOT NULL after a fill or a count.

-- control.api_client.client_id: fill then NOT NULL (ADAM CR-571, CHG-CR571-001; MIG-CONTROL #27647). A row with
-- none gets one made the server's way: tvc_live_ for production, tvc_test_ for sandbox, then 32 lowercase hex
-- characters (letters and digits) from pgcrypto's secure random source; a value already held is drawn again.
DO $data$ DECLARE n bigint; r record; v text; BEGIN IF to_regclass('control.api_client') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_client' AND column_name = 'client_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_client' AND column_name = 'environment') THEN
  FOR r IN SELECT id, environment FROM control.api_client WHERE client_id IS NULL LOOP
    LOOP
      v := CASE WHEN r.environment = 'production' THEN 'tvc_live_' ELSE 'tvc_test_' END || encode(gen_random_bytes(16), 'hex');
      EXIT WHEN NOT EXISTS (SELECT 1 FROM control.api_client WHERE client_id = v);
    END LOOP;
    UPDATE control.api_client SET client_id = v WHERE id = r.id;
  END LOOP;
  SELECT count(*) INTO n FROM (SELECT 1 FROM control.api_client WHERE client_id IS NULL) q;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: control.api_client still has % row(s) with no client_id (CR-571).', n; END IF;
END IF; END $data$;
DO $$ BEGIN IF to_regclass('control.api_client') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_client' AND column_name = 'client_id') THEN
ALTER TABLE control.api_client ALTER COLUMN client_id SET NOT NULL;
END IF; END $$;

-- control.api_anomaly_rule.tenant_id NOT NULL (ADAM CR-566, CHG-CR566-001; MIG-CONTROL-13 #28006). Platform
-- defaults are configuration, never rows: a row with no tenant is counted and stops the migration, never deleted.
DO $data$ DECLARE n bigint; BEGIN IF to_regclass('control.api_anomaly_rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_anomaly_rule' AND column_name = 'tenant_id') THEN
  SELECT count(*) INTO n FROM (SELECT 1 FROM control.api_anomaly_rule WHERE tenant_id IS NULL) q;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: control.api_anomaly_rule has % row(s) with no tenant_id; platform defaults are configuration now (CR-566). Tell the lead; nothing was deleted.', n; END IF;
END IF; END $data$;
DO $$ BEGIN IF to_regclass('control.api_anomaly_rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_anomaly_rule' AND column_name = 'tenant_id') THEN
ALTER TABLE control.api_anomaly_rule ALTER COLUMN tenant_id SET NOT NULL;
END IF; END $$;

-- control.webhook_replay.tenant_id NOT NULL in three steps (ADAM CR-434, CHG-CR434-001; #36203): (1) set it from
-- the subscription's API client where that client's allowed_tenant_ids holds exactly one tenant; (2) stop with
-- the count of rows still without a tenant, deleting nothing; (3) SET NOT NULL.
DO $data$ DECLARE n bigint; BEGIN IF to_regclass('control.webhook_replay') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'webhook_replay' AND column_name = 'tenant_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'webhook_replay' AND column_name = 'subscription_id') AND to_regclass('control.webhook_subscription') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'webhook_subscription' AND column_name = 'client_id') AND to_regclass('control.api_client') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_client' AND column_name = 'allowed_tenant_ids') THEN
  UPDATE control.webhook_replay r SET tenant_id = c.allowed_tenant_ids[1]::uuid
    FROM control.webhook_subscription s JOIN control.api_client c ON c.id = s.client_id
   WHERE r.tenant_id IS NULL AND s.id = r.subscription_id AND cardinality(c.allowed_tenant_ids) = 1;
  SELECT count(*) INTO n FROM (SELECT 1 FROM control.webhook_replay WHERE tenant_id IS NULL) q;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: control.webhook_replay has % row(s) whose tenant cannot be found from its subscription''s client (CR-434). Tell the lead; nothing was deleted.', n; END IF;
END IF; END $data$;
DO $$ BEGIN IF to_regclass('control.webhook_replay') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'webhook_replay' AND column_name = 'tenant_id') THEN
ALTER TABLE control.webhook_replay ALTER COLUMN tenant_id SET NOT NULL;
END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0131', 'r14 data steps: api_client.client_id filled, api_anomaly_rule and webhook_replay tenant_id NOT NULL after a count', '3a253398f5029c0e6eed4795708d70ab3894a87c3b0058da8bd8bee62b1993df')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE control.webhook_replay ALTER COLUMN tenant_id DROP NOT NULL;
-- ALTER TABLE control.api_anomaly_rule ALTER COLUMN tenant_id DROP NOT NULL;
-- ALTER TABLE control.api_client ALTER COLUMN client_id DROP NOT NULL;
-- -- (the client_id and webhook_replay tenant_id values filled are kept: they are what the rows mean)
-- DELETE FROM platform.schema_version WHERE version = 'V0131';
