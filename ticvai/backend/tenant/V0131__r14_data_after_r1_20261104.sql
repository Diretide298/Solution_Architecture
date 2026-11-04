-- V0131 -- tenant database, r14, after V0129 (20261104).
-- **Written by hand at the r14 integration (4 November 2026), from the lanes' posted decisions; not derived.**
-- The databases have rows, so this file does what tools/derive-ddl.py cannot: it counts the rows a new rule would
-- refuse and stops with a message naming the table and the count (never deleting or rewriting such a row: decided
-- overnight under the lead's 4 November instruction, "take the recommended decision unless its very very important"),
-- fills what can be filled from the rows' own data, and only then makes the column NOT NULL or validates the CHECK.
-- Every block is guarded on its table and columns, so the file applies as one transaction, twice, on any database.
-- order_line.product_id filled; the service_order_line status CHECK validated; personal data: 52 moved
-- field(s) on 24 table(s): 29 copied into pii.subject, 4 into pii.subject_network_identifier, 19 counted for the application's copy job.

-- A UUIDv7 for the rows this file creates (ADR-0056), and a column test, in this session only.
CREATE OR REPLACE FUNCTION pg_temp.r14_uuidv7() RETURNS uuid LANGUAGE sql VOLATILE AS $f$
  SELECT encode(set_bit(set_bit(overlay(uuid_send(gen_random_uuid()) PLACING
         substring(int8send(floor(extract(epoch FROM clock_timestamp()) * 1000)::bigint) FROM 3) FROM 1 FOR 6),
         52, 1), 53, 1), 'hex')::uuid
$f$;
CREATE OR REPLACE FUNCTION pg_temp.r14_has(t text, c text) RETURNS boolean LANGUAGE sql STABLE AS $f$
  SELECT to_regclass(t) IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns
    WHERE table_schema = split_part(t, '.', 1) AND table_name = split_part(t, '.', 2) AND column_name = c)
$f$;

-- orders.order_line.product_id: filled from the line's variant's product (ADAM CR-590, CHG-CR590-001)
DO $data$ DECLARE n bigint; BEGIN IF to_regclass('orders.order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'product_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'variant_id') AND to_regclass('catalogue.variant') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'variant' AND column_name = 'product_id') THEN
  UPDATE orders.order_line l SET product_id = v.product_id FROM catalogue.variant v
   WHERE l.product_id IS NULL AND l.variant_id = v.id;
  SELECT count(*) INTO n FROM (SELECT 1 FROM orders.order_line l WHERE l.product_id IS NULL AND l.variant_id IS NOT NULL) q;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.order_line has % line(s) whose variant names no product (CR-590).', n; END IF;
END IF; END $data$;

-- fnb.service_order_line.status CHECK (ADAM CR-594, CHG-CR594-001): V0129 added it NOT VALID; count the rows it
-- refuses, stop on any, then VALIDATE.
DO $data$ DECLARE n bigint; BEGIN IF to_regclass('fnb.service_order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'service_order_line' AND column_name = 'status') AND EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'service_order_line_status_chk' AND conrelid = to_regclass('fnb.service_order_line') AND NOT convalidated) THEN
  SELECT count(*) INTO n FROM (SELECT 1 FROM fnb.service_order_line WHERE status IS NOT NULL AND status NOT IN ('ordered', 'accepted', 'inPreparation', 'ready', 'served', 'collected', 'delivered', 'cancelled', 'refunded')) q;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: fnb.service_order_line has % row(s) whose status is not one of the nine (CR-594); nothing was rewritten.', n; END IF;
END IF; END $data$;
DO $$ BEGIN IF to_regclass('fnb.service_order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'service_order_line' AND column_name = 'status') AND EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'service_order_line_status_chk' AND conrelid = to_regclass('fnb.service_order_line')) THEN
ALTER TABLE fnb.service_order_line VALIDATE CONSTRAINT service_order_line_status_chk;
END IF; END $$;

-- **Personal data into pii.*** (r13 review B-01; the lead, 3 November 2026, "Move the columns"; ADR-0023 as
-- amended; CHG-R14M-001). For each table and subject column: a row that holds any moved field and no subject gets
-- a new pii.subject (of the kind its contract says), then each field is copied into the subject (a value the
-- subject already holds is kept) or into pii.subject_network_identifier, and the copy is verified by count in this
-- same transaction: any row whose value did not arrive stops the migration, naming the table, column and count.
-- **The old columns are NOT dropped and NOT emptied in r14**: they keep every value, so nothing is lost and a
-- rerun costs nothing. Retiring them (the DROP COLUMN of the four-step drop) waits for the lead: personal data on
-- a live database. V0129's guarded DROP NOT NULL only lets a new row leave them empty.
-- **Contacts (email, phone, mobile, contact point) and the document number are counted here, not copied**: a
-- pii.subject_contact needs Identity's deterministic value hash and a pii.subject_document the application's
-- encryption (ADR-0063), neither of which SQL holds; the application's one-off copy job writes them through
-- Identity and verifies its own counts. This file makes sure each such row has its subject first.

-- access.entitlement: subject in holder_subject_id (kind guest): holder_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('access.entitlement', 'holder_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['holder_name']) c WHERE pg_temp.r14_has('access.entitlement', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE access.entitlement SET holder_subject_id = pg_temp.r14_uuidv7() WHERE holder_subject_id IS NULL AND (%s) RETURNING holder_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT holder_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM access.entitlement WHERE holder_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: access.entitlement has % row(s) holding personal data with no holder_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM access.entitlement x WHERE x.holder_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.holder_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: access.entitlement has % row(s) whose holder_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('access.entitlement', 'holder_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.holder_name), updated_at = now() FROM access.entitlement x WHERE p.id = x.holder_subject_id AND x.holder_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM access.entitlement x JOIN pii.subject p ON p.id = x.holder_subject_id WHERE x.holder_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: access.entitlement.holder_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- accreditation.holder: subject in subject_id (kind applicant): date_of_birth -> subject.dateOfBirth, email -> contact.email, full_name -> subject.displayName, nationality -> subject.nationality, phone -> contact.phone
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('accreditation.holder', 'subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['date_of_birth', 'email', 'full_name', 'nationality', 'phone']) c WHERE pg_temp.r14_has('accreditation.holder', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE accreditation.holder SET subject_id = pg_temp.r14_uuidv7() WHERE subject_id IS NULL AND (%s) RETURNING subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT subject_id, %L, false, now(), now() FROM m', cond, 'applicant');
  EXECUTE format('SELECT count(*) FROM accreditation.holder WHERE subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: accreditation.holder has % row(s) holding personal data with no subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM accreditation.holder x WHERE x.subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: accreditation.holder has % row(s) whose subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('accreditation.holder', 'date_of_birth') THEN
    EXECUTE 'UPDATE pii.subject p SET date_of_birth = coalesce(p.date_of_birth, x.date_of_birth), updated_at = now() FROM accreditation.holder x WHERE p.id = x.subject_id AND x.date_of_birth IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM accreditation.holder x JOIN pii.subject p ON p.id = x.subject_id WHERE x.date_of_birth IS NOT NULL AND p.date_of_birth IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: accreditation.holder.date_of_birth: % value(s) did not reach pii.subject.date_of_birth', n; END IF;
  END IF;
  IF pg_temp.r14_has('accreditation.holder', 'email') THEN
    EXECUTE 'SELECT count(*) FROM accreditation.holder WHERE email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: accreditation.holder.email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('accreditation.holder', 'full_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.full_name), updated_at = now() FROM accreditation.holder x WHERE p.id = x.subject_id AND x.full_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM accreditation.holder x JOIN pii.subject p ON p.id = x.subject_id WHERE x.full_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: accreditation.holder.full_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
  IF pg_temp.r14_has('accreditation.holder', 'nationality') THEN
    EXECUTE 'UPDATE pii.subject p SET nationality = coalesce(p.nationality, x.nationality), updated_at = now() FROM accreditation.holder x WHERE p.id = x.subject_id AND x.nationality IS NOT NULL AND char_length(x.nationality) <= 2';
    EXECUTE 'SELECT count(*) FROM accreditation.holder x JOIN pii.subject p ON p.id = x.subject_id WHERE x.nationality IS NOT NULL AND p.nationality IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: accreditation.holder.nationality: % value(s) did not reach pii.subject.nationality', n; END IF;
  END IF;
  IF pg_temp.r14_has('accreditation.holder', 'phone') THEN
    EXECUTE 'SELECT count(*) FROM accreditation.holder WHERE phone IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: accreditation.holder.phone: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
END $data$;

-- approvals.accreditation_badge: subject in holder_subject_id (kind applicant): holder_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('approvals.accreditation_badge', 'holder_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['holder_name']) c WHERE pg_temp.r14_has('approvals.accreditation_badge', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE approvals.accreditation_badge SET holder_subject_id = pg_temp.r14_uuidv7() WHERE holder_subject_id IS NULL AND (%s) RETURNING holder_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT holder_subject_id, %L, false, now(), now() FROM m', cond, 'applicant');
  EXECUTE format('SELECT count(*) FROM approvals.accreditation_badge WHERE holder_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: approvals.accreditation_badge has % row(s) holding personal data with no holder_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM approvals.accreditation_badge x WHERE x.holder_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.holder_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: approvals.accreditation_badge has % row(s) whose holder_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('approvals.accreditation_badge', 'holder_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.holder_name), updated_at = now() FROM approvals.accreditation_badge x WHERE p.id = x.holder_subject_id AND x.holder_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM approvals.accreditation_badge x JOIN pii.subject p ON p.id = x.holder_subject_id WHERE x.holder_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: approvals.accreditation_badge.holder_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- assets.share: subject in recipient_subject_id (kind contact): recipient_email -> contact.email
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('assets.share', 'recipient_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['recipient_email']) c WHERE pg_temp.r14_has('assets.share', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE assets.share SET recipient_subject_id = pg_temp.r14_uuidv7() WHERE recipient_subject_id IS NULL AND (%s) RETURNING recipient_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT recipient_subject_id, %L, false, now(), now() FROM m', cond, 'contact');
  EXECUTE format('SELECT count(*) FROM assets.share WHERE recipient_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: assets.share has % row(s) holding personal data with no recipient_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM assets.share x WHERE x.recipient_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.recipient_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: assets.share has % row(s) whose recipient_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('assets.share', 'recipient_email') THEN
    EXECUTE 'SELECT count(*) FROM assets.share WHERE recipient_email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: assets.share.recipient_email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
END $data$;

-- catalogue.waitlist_entry: subject in subject_id (kind guest): contact_point -> contact.point
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('catalogue.waitlist_entry', 'subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['contact_point']) c WHERE pg_temp.r14_has('catalogue.waitlist_entry', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE catalogue.waitlist_entry SET subject_id = pg_temp.r14_uuidv7() WHERE subject_id IS NULL AND (%s) RETURNING subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM catalogue.waitlist_entry WHERE subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: catalogue.waitlist_entry has % row(s) holding personal data with no subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM catalogue.waitlist_entry x WHERE x.subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: catalogue.waitlist_entry has % row(s) whose subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('catalogue.waitlist_entry', 'contact_point') THEN
    EXECUTE 'SELECT count(*) FROM catalogue.waitlist_entry WHERE contact_point IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: catalogue.waitlist_entry.contact_point: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
END $data$;

-- fnb.table_reservation: subject in subject_id (kind guest): contact_point -> contact.point, guest_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('fnb.table_reservation', 'subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['contact_point', 'guest_name']) c WHERE pg_temp.r14_has('fnb.table_reservation', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE fnb.table_reservation SET subject_id = pg_temp.r14_uuidv7() WHERE subject_id IS NULL AND (%s) RETURNING subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM fnb.table_reservation WHERE subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: fnb.table_reservation has % row(s) holding personal data with no subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM fnb.table_reservation x WHERE x.subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: fnb.table_reservation has % row(s) whose subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('fnb.table_reservation', 'contact_point') THEN
    EXECUTE 'SELECT count(*) FROM fnb.table_reservation WHERE contact_point IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: fnb.table_reservation.contact_point: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('fnb.table_reservation', 'guest_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.guest_name), updated_at = now() FROM fnb.table_reservation x WHERE p.id = x.subject_id AND x.guest_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM fnb.table_reservation x JOIN pii.subject p ON p.id = x.subject_id WHERE x.guest_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: fnb.table_reservation.guest_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- identity.principal: subject in subject_id (kind employee): email -> contact.email
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('identity.principal', 'subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['email']) c WHERE pg_temp.r14_has('identity.principal', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE identity.principal SET subject_id = pg_temp.r14_uuidv7() WHERE subject_id IS NULL AND (%s) RETURNING subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT subject_id, %L, false, now(), now() FROM m', cond, 'employee');
  EXECUTE format('SELECT count(*) FROM identity.principal WHERE subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: identity.principal has % row(s) holding personal data with no subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM identity.principal x WHERE x.subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: identity.principal has % row(s) whose subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('identity.principal', 'email') THEN
    EXECUTE 'SELECT count(*) FROM identity.principal WHERE email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: identity.principal.email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
END $data$;

-- identity.session: subject in subject_id (kind employee): ip_address -> identifier.ipAddress
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('identity.session', 'subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['ip_address']) c WHERE pg_temp.r14_has('identity.session', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE identity.session SET subject_id = pg_temp.r14_uuidv7() WHERE subject_id IS NULL AND (%s) RETURNING subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT subject_id, %L, false, now(), now() FROM m', cond, 'employee');
  EXECUTE format('SELECT count(*) FROM identity.session WHERE subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: identity.session has % row(s) holding personal data with no subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM identity.session x WHERE x.subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: identity.session has % row(s) whose subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('identity.session', 'ip_address') THEN
    EXECUTE 'INSERT INTO pii.subject_network_identifier (id, subject_id, record_table, record_id, ip_address, captured_at) SELECT pg_temp.r14_uuidv7(), x.subject_id, ''identity.session'', x.id, x.ip_address::text, coalesce(x.started_at, now()) FROM identity.session x WHERE x.ip_address IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject_network_identifier i WHERE i.record_table = ''identity.session'' AND i.record_id = x.id)';
    EXECUTE 'SELECT count(*) FROM identity.session x WHERE x.ip_address IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject_network_identifier i WHERE i.record_table = ''identity.session'' AND i.record_id = x.id)' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: identity.session.ip_address: % value(s) did not reach pii.subject_network_identifier', n; END IF;
  END IF;
END $data$;

-- inventory.supplier: subject in contact_subject_id (kind contact): contact_email -> contact.email, contact_name -> subject.displayName, contact_phone -> contact.phone
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('inventory.supplier', 'contact_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['contact_email', 'contact_name', 'contact_phone']) c WHERE pg_temp.r14_has('inventory.supplier', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE inventory.supplier SET contact_subject_id = pg_temp.r14_uuidv7() WHERE contact_subject_id IS NULL AND (%s) RETURNING contact_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT contact_subject_id, %L, false, now(), now() FROM m', cond, 'contact');
  EXECUTE format('SELECT count(*) FROM inventory.supplier WHERE contact_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: inventory.supplier has % row(s) holding personal data with no contact_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM inventory.supplier x WHERE x.contact_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.contact_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: inventory.supplier has % row(s) whose contact_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('inventory.supplier', 'contact_email') THEN
    EXECUTE 'SELECT count(*) FROM inventory.supplier WHERE contact_email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: inventory.supplier.contact_email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('inventory.supplier', 'contact_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.contact_name), updated_at = now() FROM inventory.supplier x WHERE p.id = x.contact_subject_id AND x.contact_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM inventory.supplier x JOIN pii.subject p ON p.id = x.contact_subject_id WHERE x.contact_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: inventory.supplier.contact_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
  IF pg_temp.r14_has('inventory.supplier', 'contact_phone') THEN
    EXECUTE 'SELECT count(*) FROM inventory.supplier WHERE contact_phone IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: inventory.supplier.contact_phone: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
END $data$;

-- marketing.booking_consent_record: subject in person_subject_id (kind guest): person_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('marketing.booking_consent_record', 'person_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['person_name']) c WHERE pg_temp.r14_has('marketing.booking_consent_record', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE marketing.booking_consent_record SET person_subject_id = pg_temp.r14_uuidv7() WHERE person_subject_id IS NULL AND (%s) RETURNING person_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT person_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM marketing.booking_consent_record WHERE person_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.booking_consent_record has % row(s) holding personal data with no person_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM marketing.booking_consent_record x WHERE x.person_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.person_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.booking_consent_record has % row(s) whose person_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('marketing.booking_consent_record', 'person_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.person_name), updated_at = now() FROM marketing.booking_consent_record x WHERE p.id = x.person_subject_id AND x.person_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM marketing.booking_consent_record x JOIN pii.subject p ON p.id = x.person_subject_id WHERE x.person_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.booking_consent_record.person_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- marketing.form_submission: subject in subject_id (kind guest): ip_address -> identifier.ipAddress
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('marketing.form_submission', 'subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['ip_address']) c WHERE pg_temp.r14_has('marketing.form_submission', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE marketing.form_submission SET subject_id = pg_temp.r14_uuidv7() WHERE subject_id IS NULL AND (%s) RETURNING subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM marketing.form_submission WHERE subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.form_submission has % row(s) holding personal data with no subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM marketing.form_submission x WHERE x.subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.form_submission has % row(s) whose subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('marketing.form_submission', 'ip_address') THEN
    EXECUTE 'INSERT INTO pii.subject_network_identifier (id, subject_id, record_table, record_id, ip_address, captured_at) SELECT pg_temp.r14_uuidv7(), x.subject_id, ''marketing.form_submission'', x.id, x.ip_address::text, coalesce(x.submitted_at, now()) FROM marketing.form_submission x WHERE x.ip_address IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject_network_identifier i WHERE i.record_table = ''marketing.form_submission'' AND i.record_id = x.id)';
    EXECUTE 'SELECT count(*) FROM marketing.form_submission x WHERE x.ip_address IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject_network_identifier i WHERE i.record_table = ''marketing.form_submission'' AND i.record_id = x.id)' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.form_submission.ip_address: % value(s) did not reach pii.subject_network_identifier', n; END IF;
  END IF;
END $data$;

-- marketing.guest_profile: subject in subject_id (kind guest): display_name -> subject.displayName, email -> contact.email, phone -> contact.phone, preferred_language -> subject.preferredLanguage
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('marketing.guest_profile', 'subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['display_name', 'email', 'phone', 'preferred_language']) c WHERE pg_temp.r14_has('marketing.guest_profile', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE marketing.guest_profile SET subject_id = pg_temp.r14_uuidv7() WHERE subject_id IS NULL AND (%s) RETURNING subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM marketing.guest_profile WHERE subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.guest_profile has % row(s) holding personal data with no subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM marketing.guest_profile x WHERE x.subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.guest_profile has % row(s) whose subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('marketing.guest_profile', 'display_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.display_name), updated_at = now() FROM marketing.guest_profile x WHERE p.id = x.subject_id AND x.display_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM marketing.guest_profile x JOIN pii.subject p ON p.id = x.subject_id WHERE x.display_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.guest_profile.display_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
  IF pg_temp.r14_has('marketing.guest_profile', 'email') THEN
    EXECUTE 'SELECT count(*) FROM marketing.guest_profile WHERE email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: marketing.guest_profile.email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('marketing.guest_profile', 'phone') THEN
    EXECUTE 'SELECT count(*) FROM marketing.guest_profile WHERE phone IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: marketing.guest_profile.phone: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('marketing.guest_profile', 'preferred_language') THEN
    EXECUTE 'UPDATE pii.subject p SET preferred_language = coalesce(p.preferred_language, x.preferred_language), updated_at = now() FROM marketing.guest_profile x WHERE p.id = x.subject_id AND x.preferred_language IS NOT NULL AND char_length(x.preferred_language) <= 2';
    EXECUTE 'SELECT count(*) FROM marketing.guest_profile x JOIN pii.subject p ON p.id = x.subject_id WHERE x.preferred_language IS NOT NULL AND p.preferred_language IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.guest_profile.preferred_language: % value(s) did not reach pii.subject.preferred_language', n; END IF;
  END IF;
END $data$;

-- marketing.invitation: subject in subject_id (kind guest): recipient_email -> contact.email
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('marketing.invitation', 'subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['recipient_email']) c WHERE pg_temp.r14_has('marketing.invitation', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE marketing.invitation SET subject_id = pg_temp.r14_uuidv7() WHERE subject_id IS NULL AND (%s) RETURNING subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM marketing.invitation WHERE subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.invitation has % row(s) holding personal data with no subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM marketing.invitation x WHERE x.subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.invitation has % row(s) whose subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('marketing.invitation', 'recipient_email') THEN
    EXECUTE 'SELECT count(*) FROM marketing.invitation WHERE recipient_email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: marketing.invitation.recipient_email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
END $data$;

-- marketing.waiver_signature: subject in guardian_subject_id (kind guest): guardian_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('marketing.waiver_signature', 'guardian_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['guardian_name']) c WHERE pg_temp.r14_has('marketing.waiver_signature', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE marketing.waiver_signature SET guardian_subject_id = pg_temp.r14_uuidv7() WHERE guardian_subject_id IS NULL AND (%s) RETURNING guardian_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT guardian_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM marketing.waiver_signature WHERE guardian_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature has % row(s) holding personal data with no guardian_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM marketing.waiver_signature x WHERE x.guardian_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.guardian_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature has % row(s) whose guardian_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('marketing.waiver_signature', 'guardian_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.guardian_name), updated_at = now() FROM marketing.waiver_signature x WHERE p.id = x.guardian_subject_id AND x.guardian_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM marketing.waiver_signature x JOIN pii.subject p ON p.id = x.guardian_subject_id WHERE x.guardian_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature.guardian_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- marketing.waiver_signature: subject in signer_subject_id (kind guest): ip_address -> identifier.ipAddress, signed_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('marketing.waiver_signature', 'signer_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['ip_address', 'signed_name']) c WHERE pg_temp.r14_has('marketing.waiver_signature', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE marketing.waiver_signature SET signer_subject_id = pg_temp.r14_uuidv7() WHERE signer_subject_id IS NULL AND (%s) RETURNING signer_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT signer_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM marketing.waiver_signature WHERE signer_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature has % row(s) holding personal data with no signer_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM marketing.waiver_signature x WHERE x.signer_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.signer_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature has % row(s) whose signer_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('marketing.waiver_signature', 'ip_address') THEN
    EXECUTE 'INSERT INTO pii.subject_network_identifier (id, subject_id, record_table, record_id, ip_address, captured_at) SELECT pg_temp.r14_uuidv7(), x.signer_subject_id, ''marketing.waiver_signature'', x.id, x.ip_address::text, coalesce(x.signed_at, now()) FROM marketing.waiver_signature x WHERE x.ip_address IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject_network_identifier i WHERE i.record_table = ''marketing.waiver_signature'' AND i.record_id = x.id)';
    EXECUTE 'SELECT count(*) FROM marketing.waiver_signature x WHERE x.ip_address IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject_network_identifier i WHERE i.record_table = ''marketing.waiver_signature'' AND i.record_id = x.id)' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature.ip_address: % value(s) did not reach pii.subject_network_identifier', n; END IF;
  END IF;
  IF pg_temp.r14_has('marketing.waiver_signature', 'signed_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.signed_name), updated_at = now() FROM marketing.waiver_signature x WHERE p.id = x.signer_subject_id AND x.signed_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM marketing.waiver_signature x JOIN pii.subject p ON p.id = x.signer_subject_id WHERE x.signed_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature.signed_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- marketing.waiver_signature: subject in participant_subject_id (kind guest): subject_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('marketing.waiver_signature', 'participant_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['subject_name']) c WHERE pg_temp.r14_has('marketing.waiver_signature', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE marketing.waiver_signature SET participant_subject_id = pg_temp.r14_uuidv7() WHERE participant_subject_id IS NULL AND (%s) RETURNING participant_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT participant_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM marketing.waiver_signature WHERE participant_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature has % row(s) holding personal data with no participant_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM marketing.waiver_signature x WHERE x.participant_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.participant_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature has % row(s) whose participant_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('marketing.waiver_signature', 'subject_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.subject_name), updated_at = now() FROM marketing.waiver_signature x WHERE p.id = x.participant_subject_id AND x.subject_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM marketing.waiver_signature x JOIN pii.subject p ON p.id = x.participant_subject_id WHERE x.subject_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: marketing.waiver_signature.subject_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- orders.group_customer_organisation_contact: subject in contact_subject_id (kind contact): email -> contact.email, name -> subject.displayName, phone -> contact.phone
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('orders.group_customer_organisation_contact', 'contact_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['email', 'name', 'phone']) c WHERE pg_temp.r14_has('orders.group_customer_organisation_contact', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE orders.group_customer_organisation_contact SET contact_subject_id = pg_temp.r14_uuidv7() WHERE contact_subject_id IS NULL AND (%s) RETURNING contact_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT contact_subject_id, %L, false, now(), now() FROM m', cond, 'contact');
  EXECUTE format('SELECT count(*) FROM orders.group_customer_organisation_contact WHERE contact_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.group_customer_organisation_contact has % row(s) holding personal data with no contact_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM orders.group_customer_organisation_contact x WHERE x.contact_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.contact_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.group_customer_organisation_contact has % row(s) whose contact_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('orders.group_customer_organisation_contact', 'email') THEN
    EXECUTE 'SELECT count(*) FROM orders.group_customer_organisation_contact WHERE email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: orders.group_customer_organisation_contact.email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('orders.group_customer_organisation_contact', 'name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.name), updated_at = now() FROM orders.group_customer_organisation_contact x WHERE p.id = x.contact_subject_id AND x.name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM orders.group_customer_organisation_contact x JOIN pii.subject p ON p.id = x.contact_subject_id WHERE x.name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.group_customer_organisation_contact.name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
  IF pg_temp.r14_has('orders.group_customer_organisation_contact', 'phone') THEN
    EXECUTE 'SELECT count(*) FROM orders.group_customer_organisation_contact WHERE phone IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: orders.group_customer_organisation_contact.phone: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
END $data$;

-- orders.group_participant: subject in subject_id (kind guest): date_of_birth -> subject.dateOfBirth, email -> contact.email, full_name -> subject.displayName, phone -> contact.phone
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('orders.group_participant', 'subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['date_of_birth', 'email', 'full_name', 'phone']) c WHERE pg_temp.r14_has('orders.group_participant', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE orders.group_participant SET subject_id = pg_temp.r14_uuidv7() WHERE subject_id IS NULL AND (%s) RETURNING subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM orders.group_participant WHERE subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.group_participant has % row(s) holding personal data with no subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM orders.group_participant x WHERE x.subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.group_participant has % row(s) whose subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('orders.group_participant', 'date_of_birth') THEN
    EXECUTE 'UPDATE pii.subject p SET date_of_birth = coalesce(p.date_of_birth, x.date_of_birth), updated_at = now() FROM orders.group_participant x WHERE p.id = x.subject_id AND x.date_of_birth IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM orders.group_participant x JOIN pii.subject p ON p.id = x.subject_id WHERE x.date_of_birth IS NOT NULL AND p.date_of_birth IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.group_participant.date_of_birth: % value(s) did not reach pii.subject.date_of_birth', n; END IF;
  END IF;
  IF pg_temp.r14_has('orders.group_participant', 'email') THEN
    EXECUTE 'SELECT count(*) FROM orders.group_participant WHERE email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: orders.group_participant.email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('orders.group_participant', 'full_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.full_name), updated_at = now() FROM orders.group_participant x WHERE p.id = x.subject_id AND x.full_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM orders.group_participant x JOIN pii.subject p ON p.id = x.subject_id WHERE x.full_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.group_participant.full_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
  IF pg_temp.r14_has('orders.group_participant', 'phone') THEN
    EXECUTE 'SELECT count(*) FROM orders.group_participant WHERE phone IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: orders.group_participant.phone: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
END $data$;

-- orders.invitation: subject in recipient_subject_id (kind guest): recipient_email -> contact.email, recipient_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('orders.invitation', 'recipient_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['recipient_email', 'recipient_name']) c WHERE pg_temp.r14_has('orders.invitation', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE orders.invitation SET recipient_subject_id = pg_temp.r14_uuidv7() WHERE recipient_subject_id IS NULL AND (%s) RETURNING recipient_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT recipient_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM orders.invitation WHERE recipient_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.invitation has % row(s) holding personal data with no recipient_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM orders.invitation x WHERE x.recipient_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.recipient_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.invitation has % row(s) whose recipient_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('orders.invitation', 'recipient_email') THEN
    EXECUTE 'SELECT count(*) FROM orders.invitation WHERE recipient_email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: orders.invitation.recipient_email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('orders.invitation', 'recipient_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.recipient_name), updated_at = now() FROM orders.invitation x WHERE p.id = x.recipient_subject_id AND x.recipient_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM orders.invitation x JOIN pii.subject p ON p.id = x.recipient_subject_id WHERE x.recipient_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.invitation.recipient_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- orders.order_line: subject in holder_subject_id (kind guest): holder_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('orders.order_line', 'holder_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['holder_name']) c WHERE pg_temp.r14_has('orders.order_line', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE orders.order_line SET holder_subject_id = pg_temp.r14_uuidv7() WHERE holder_subject_id IS NULL AND (%s) RETURNING holder_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT holder_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM orders.order_line WHERE holder_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.order_line has % row(s) holding personal data with no holder_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM orders.order_line x WHERE x.holder_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.holder_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.order_line has % row(s) whose holder_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('orders.order_line', 'holder_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.holder_name), updated_at = now() FROM orders.order_line x WHERE p.id = x.holder_subject_id AND x.holder_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM orders.order_line x JOIN pii.subject p ON p.id = x.holder_subject_id WHERE x.holder_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.order_line.holder_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- orders.reservation_line: subject in holder_subject_id (kind guest): holder_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('orders.reservation_line', 'holder_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['holder_name']) c WHERE pg_temp.r14_has('orders.reservation_line', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE orders.reservation_line SET holder_subject_id = pg_temp.r14_uuidv7() WHERE holder_subject_id IS NULL AND (%s) RETURNING holder_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT holder_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM orders.reservation_line WHERE holder_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.reservation_line has % row(s) holding personal data with no holder_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM orders.reservation_line x WHERE x.holder_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.holder_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.reservation_line has % row(s) whose holder_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('orders.reservation_line', 'holder_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.holder_name), updated_at = now() FROM orders.reservation_line x WHERE p.id = x.holder_subject_id AND x.holder_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM orders.reservation_line x JOIN pii.subject p ON p.id = x.holder_subject_id WHERE x.holder_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: orders.reservation_line.holder_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- rental.agreement_signature: subject in signatory_subject_id (kind guest): ip_address -> identifier.ipAddress, signatory_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('rental.agreement_signature', 'signatory_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['ip_address', 'signatory_name']) c WHERE pg_temp.r14_has('rental.agreement_signature', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE rental.agreement_signature SET signatory_subject_id = pg_temp.r14_uuidv7() WHERE signatory_subject_id IS NULL AND (%s) RETURNING signatory_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT signatory_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM rental.agreement_signature WHERE signatory_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.agreement_signature has % row(s) holding personal data with no signatory_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM rental.agreement_signature x WHERE x.signatory_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.signatory_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.agreement_signature has % row(s) whose signatory_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('rental.agreement_signature', 'ip_address') THEN
    EXECUTE 'INSERT INTO pii.subject_network_identifier (id, subject_id, record_table, record_id, ip_address, captured_at) SELECT pg_temp.r14_uuidv7(), x.signatory_subject_id, ''rental.agreement_signature'', x.id, x.ip_address::text, coalesce(x.signed_at, now()) FROM rental.agreement_signature x WHERE x.ip_address IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject_network_identifier i WHERE i.record_table = ''rental.agreement_signature'' AND i.record_id = x.id)';
    EXECUTE 'SELECT count(*) FROM rental.agreement_signature x WHERE x.ip_address IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject_network_identifier i WHERE i.record_table = ''rental.agreement_signature'' AND i.record_id = x.id)' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.agreement_signature.ip_address: % value(s) did not reach pii.subject_network_identifier', n; END IF;
  END IF;
  IF pg_temp.r14_has('rental.agreement_signature', 'signatory_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.signatory_name), updated_at = now() FROM rental.agreement_signature x WHERE p.id = x.signatory_subject_id AND x.signatory_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM rental.agreement_signature x JOIN pii.subject p ON p.id = x.signatory_subject_id WHERE x.signatory_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.agreement_signature.signatory_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- rental.participant: subject in participant_subject_id (kind guest): date_of_birth -> subject.dateOfBirth, id_number -> document.number, name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('rental.participant', 'participant_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['date_of_birth', 'id_number', 'name']) c WHERE pg_temp.r14_has('rental.participant', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE rental.participant SET participant_subject_id = pg_temp.r14_uuidv7() WHERE participant_subject_id IS NULL AND (%s) RETURNING participant_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT participant_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM rental.participant WHERE participant_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant has % row(s) holding personal data with no participant_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM rental.participant x WHERE x.participant_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.participant_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant has % row(s) whose participant_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('rental.participant', 'date_of_birth') THEN
    EXECUTE 'UPDATE pii.subject p SET date_of_birth = coalesce(p.date_of_birth, x.date_of_birth), updated_at = now() FROM rental.participant x WHERE p.id = x.participant_subject_id AND x.date_of_birth IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM rental.participant x JOIN pii.subject p ON p.id = x.participant_subject_id WHERE x.date_of_birth IS NOT NULL AND p.date_of_birth IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant.date_of_birth: % value(s) did not reach pii.subject.date_of_birth', n; END IF;
  END IF;
  IF pg_temp.r14_has('rental.participant', 'id_number') THEN
    EXECUTE 'SELECT count(*) FROM rental.participant WHERE id_number IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: rental.participant.id_number: % value(s) for pii.subject_document, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('rental.participant', 'name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.name), updated_at = now() FROM rental.participant x WHERE p.id = x.participant_subject_id AND x.name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM rental.participant x JOIN pii.subject p ON p.id = x.participant_subject_id WHERE x.name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant.name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- rental.participant: subject in emergency_contact_subject_id (kind contact): emergency_contact -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('rental.participant', 'emergency_contact_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['emergency_contact']) c WHERE pg_temp.r14_has('rental.participant', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE rental.participant SET emergency_contact_subject_id = pg_temp.r14_uuidv7() WHERE emergency_contact_subject_id IS NULL AND (%s) RETURNING emergency_contact_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT emergency_contact_subject_id, %L, false, now(), now() FROM m', cond, 'contact');
  EXECUTE format('SELECT count(*) FROM rental.participant WHERE emergency_contact_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant has % row(s) holding personal data with no emergency_contact_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM rental.participant x WHERE x.emergency_contact_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.emergency_contact_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant has % row(s) whose emergency_contact_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('rental.participant', 'emergency_contact') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.emergency_contact), updated_at = now() FROM rental.participant x WHERE p.id = x.emergency_contact_subject_id AND x.emergency_contact IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM rental.participant x JOIN pii.subject p ON p.id = x.emergency_contact_subject_id WHERE x.emergency_contact IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant.emergency_contact: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- rental.participant: subject in guardian_subject_id (kind guest): guardian_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('rental.participant', 'guardian_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['guardian_name']) c WHERE pg_temp.r14_has('rental.participant', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE rental.participant SET guardian_subject_id = pg_temp.r14_uuidv7() WHERE guardian_subject_id IS NULL AND (%s) RETURNING guardian_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT guardian_subject_id, %L, false, now(), now() FROM m', cond, 'guest');
  EXECUTE format('SELECT count(*) FROM rental.participant WHERE guardian_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant has % row(s) holding personal data with no guardian_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM rental.participant x WHERE x.guardian_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.guardian_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant has % row(s) whose guardian_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('rental.participant', 'guardian_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.guardian_name), updated_at = now() FROM rental.participant x WHERE p.id = x.guardian_subject_id AND x.guardian_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM rental.participant x JOIN pii.subject p ON p.id = x.guardian_subject_id WHERE x.guardian_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: rental.participant.guardian_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- seating.group_request: subject in contact_subject_id (kind contact): contact_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('seating.group_request', 'contact_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['contact_name']) c WHERE pg_temp.r14_has('seating.group_request', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE seating.group_request SET contact_subject_id = pg_temp.r14_uuidv7() WHERE contact_subject_id IS NULL AND (%s) RETURNING contact_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT contact_subject_id, %L, false, now(), now() FROM m', cond, 'contact');
  EXECUTE format('SELECT count(*) FROM seating.group_request WHERE contact_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: seating.group_request has % row(s) holding personal data with no contact_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM seating.group_request x WHERE x.contact_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.contact_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: seating.group_request has % row(s) whose contact_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('seating.group_request', 'contact_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.contact_name), updated_at = now() FROM seating.group_request x WHERE p.id = x.contact_subject_id AND x.contact_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM seating.group_request x JOIN pii.subject p ON p.id = x.contact_subject_id WHERE x.contact_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: seating.group_request.contact_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- seating.hold_pool: subject in holder_subject_id (kind contact): holder_name -> subject.displayName
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('seating.hold_pool', 'holder_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['holder_name']) c WHERE pg_temp.r14_has('seating.hold_pool', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE seating.hold_pool SET holder_subject_id = pg_temp.r14_uuidv7() WHERE holder_subject_id IS NULL AND (%s) RETURNING holder_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT holder_subject_id, %L, false, now(), now() FROM m', cond, 'contact');
  EXECUTE format('SELECT count(*) FROM seating.hold_pool WHERE holder_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: seating.hold_pool has % row(s) holding personal data with no holder_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM seating.hold_pool x WHERE x.holder_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.holder_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: seating.hold_pool has % row(s) whose holder_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('seating.hold_pool', 'holder_name') THEN
    EXECUTE 'UPDATE pii.subject p SET display_name = coalesce(p.display_name, x.holder_name), updated_at = now() FROM seating.hold_pool x WHERE p.id = x.holder_subject_id AND x.holder_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM seating.hold_pool x JOIN pii.subject p ON p.id = x.holder_subject_id WHERE x.holder_name IS NOT NULL AND p.display_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: seating.hold_pool.holder_name: % value(s) did not reach pii.subject.display_name', n; END IF;
  END IF;
END $data$;

-- workforce.employee: subject in employee_subject_id (kind employee): date_of_birth -> subject.dateOfBirth, email -> contact.email, first_name -> subject.givenName, last_name -> subject.familyName, mobile -> contact.mobile
DO $data$ DECLARE n bigint; have text[]; cond text; BEGIN
  IF NOT pg_temp.r14_has('workforce.employee', 'employee_subject_id') OR to_regclass('pii.subject') IS NULL THEN RETURN; END IF;
  SELECT array_agg(c) INTO have FROM unnest(ARRAY['date_of_birth', 'email', 'first_name', 'last_name', 'mobile']) c WHERE pg_temp.r14_has('workforce.employee', c);
  IF have IS NULL THEN RETURN; END IF;
  SELECT string_agg(format('%I IS NOT NULL', c), ' OR ') INTO cond FROM unnest(have) c;
  -- a subject for every row that holds a moved field and has none
  EXECUTE format('WITH m AS (UPDATE workforce.employee SET employee_subject_id = pg_temp.r14_uuidv7() WHERE employee_subject_id IS NULL AND (%s) RETURNING employee_subject_id) INSERT INTO pii.subject (id, kind, is_erased, created_at, updated_at) SELECT employee_subject_id, %L, false, now(), now() FROM m', cond, 'employee');
  EXECUTE format('SELECT count(*) FROM workforce.employee WHERE employee_subject_id IS NULL AND (%s)', cond) INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: workforce.employee has % row(s) holding personal data with no employee_subject_id', n; END IF;
  EXECUTE 'SELECT count(*) FROM workforce.employee x WHERE x.employee_subject_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pii.subject p WHERE p.id = x.employee_subject_id)' INTO n;
  IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: workforce.employee has % row(s) whose employee_subject_id names no pii.subject', n; END IF;
  IF pg_temp.r14_has('workforce.employee', 'date_of_birth') THEN
    EXECUTE 'UPDATE pii.subject p SET date_of_birth = coalesce(p.date_of_birth, x.date_of_birth), updated_at = now() FROM workforce.employee x WHERE p.id = x.employee_subject_id AND x.date_of_birth IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM workforce.employee x JOIN pii.subject p ON p.id = x.employee_subject_id WHERE x.date_of_birth IS NOT NULL AND p.date_of_birth IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: workforce.employee.date_of_birth: % value(s) did not reach pii.subject.date_of_birth', n; END IF;
  END IF;
  IF pg_temp.r14_has('workforce.employee', 'email') THEN
    EXECUTE 'SELECT count(*) FROM workforce.employee WHERE email IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: workforce.employee.email: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
  IF pg_temp.r14_has('workforce.employee', 'first_name') THEN
    EXECUTE 'UPDATE pii.subject p SET given_name = coalesce(p.given_name, x.first_name), updated_at = now() FROM workforce.employee x WHERE p.id = x.employee_subject_id AND x.first_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM workforce.employee x JOIN pii.subject p ON p.id = x.employee_subject_id WHERE x.first_name IS NOT NULL AND p.given_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: workforce.employee.first_name: % value(s) did not reach pii.subject.given_name', n; END IF;
  END IF;
  IF pg_temp.r14_has('workforce.employee', 'last_name') THEN
    EXECUTE 'UPDATE pii.subject p SET family_name = coalesce(p.family_name, x.last_name), updated_at = now() FROM workforce.employee x WHERE p.id = x.employee_subject_id AND x.last_name IS NOT NULL';
    EXECUTE 'SELECT count(*) FROM workforce.employee x JOIN pii.subject p ON p.id = x.employee_subject_id WHERE x.last_name IS NOT NULL AND p.family_name IS NULL' INTO n;
    IF n > 0 THEN RAISE EXCEPTION 'r14 migration stopped: workforce.employee.last_name: % value(s) did not reach pii.subject.family_name', n; END IF;
  END IF;
  IF pg_temp.r14_has('workforce.employee', 'mobile') THEN
    EXECUTE 'SELECT count(*) FROM workforce.employee WHERE mobile IS NOT NULL' INTO n;
    RAISE NOTICE 'r14: workforce.employee.mobile: % value(s) for pii.subject_contact, left on the row for the application''s one-off copy job', n;
  END IF;
END $data$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0131', 'r14 data steps: order_line.product_id, the service_order_line status CHECK, 52 personal fields copied or counted', '6f8d640bb914e57e52f4f11648605c4295452c2faee8ec27866d3eeb43afcdc0')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE fnb.service_order_line DROP CONSTRAINT IF EXISTS service_order_line_status_chk;
-- -- (the data this file wrote stays: order_line.product_id is what the line's variant says, and the pii.* copies
-- -- sit beside the old columns, which still hold every value)
-- DELETE FROM platform.schema_version WHERE version = 'V0131';
