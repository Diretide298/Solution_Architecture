-- V0129 -- tenant database, after r1 (9cec72d) (20261104).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 5 table(s), 36 column(s), 43 index(es), 47 other statement(s), 1 row-level security polic(ies) re-applied.

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL THEN
ALTER TABLE access.entitlement ADD COLUMN IF NOT EXISTS holder_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'accreditation' AND table_name = 'holder' AND column_name = 'full_name' AND is_nullable = 'NO') THEN ALTER TABLE accreditation.holder ALTER COLUMN full_name DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.message') IS NOT NULL THEN
ALTER TABLE ai.message ADD COLUMN IF NOT EXISTS subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.accreditation_badge') IS NOT NULL THEN
ALTER TABLE approvals.accreditation_badge ADD COLUMN IF NOT EXISTS holder_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request') IS NOT NULL THEN
ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS platform_approver_permission text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.request') IS NOT NULL THEN
ALTER TABLE approvals.request ADD COLUMN IF NOT EXISTS platform_minimum_approvals integer;
END IF; END $$;

DO $$ BEGIN IF to_regclass('assets.share') IS NOT NULL THEN
ALTER TABLE assets.share ADD COLUMN IF NOT EXISTS recipient_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.performance') IS NOT NULL THEN
ALTER TABLE catalogue.performance ADD COLUMN IF NOT EXISTS admission_starts_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL THEN
ALTER TABLE catalogue.product ADD COLUMN IF NOT EXISTS display_order integer DEFAULT 100;
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.service_order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'service_order_line' AND column_name = 'status') THEN
ALTER TABLE fnb.service_order_line DROP CONSTRAINT IF EXISTS service_order_line_status_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.service_order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'service_order_line' AND column_name = 'status') THEN
ALTER TABLE fnb.service_order_line ADD CONSTRAINT service_order_line_status_chk CHECK (status IN ('ordered', 'accepted', 'inPreparation', 'ready', 'served', 'collected', 'delivered', 'cancelled', 'refunded')) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.service_order_line') IS NOT NULL THEN
ALTER TABLE fnb.service_order_line ADD COLUMN IF NOT EXISTS comped_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.service_order_line') IS NOT NULL THEN
ALTER TABLE fnb.service_order_line ADD COLUMN IF NOT EXISTS comp_reason text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.service_order_line') IS NOT NULL THEN
ALTER TABLE fnb.service_order_line ADD COLUMN IF NOT EXISTS comped_by_principal_id uuid;
END IF; END $$;

CREATE TABLE IF NOT EXISTS fnb.table_visit_server (
    id                                uuid PRIMARY KEY NOT NULL,
    table_visit_id                    uuid NOT NULL,
    server_principal_id               uuid NOT NULL,
    from_at                           timestamptz NOT NULL,
    is_split_gratuity                 boolean NOT NULL DEFAULT true,
    recorded_by_principal_id          uuid NOT NULL,
    scope_path                        ltree NOT NULL
);

CREATE TABLE IF NOT EXISTS identity.offline_pin_verifier (
    id                                uuid PRIMARY KEY NOT NULL,
    principal_id                      uuid NOT NULL,
    venue_id                          uuid NOT NULL,
    verifier_hash                     text NOT NULL,
    credential_set_at                 timestamptz NOT NULL,
    issued_at                         timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    revoked_at                        timestamptz,
    scope_path                        ltree NOT NULL
);

CREATE TABLE IF NOT EXISTS identity.offline_step_up (
    id                                uuid PRIMARY KEY NOT NULL,
    operation_id                      text NOT NULL CONSTRAINT offline_step_up_operation_id_chk CHECK (char_length(operation_id) <= 100),
    act_id                            uuid NOT NULL,
    workstation_id                    uuid NOT NULL,
    caller_principal_id               uuid NOT NULL,
    signer_principal_id               uuid NOT NULL,
    package_id                        uuid NOT NULL,
    verifier_id                       uuid NOT NULL,
    verified_at                       timestamptz NOT NULL,
    recorded_at                       timestamptz NOT NULL,
    synced_at                         timestamptz NOT NULL,
    failed_attempts_before            integer NOT NULL,
    verdict                           text NOT NULL CONSTRAINT offline_step_up_verdict_chk CHECK (verdict IN ('confirmed', 'refusedAtSync')),
    refusal                           text CONSTRAINT offline_step_up_refusal_chk CHECK (refusal IN ('credentialWrong', 'noPin', 'permissionNotHeld', 'notActiveHere', 'selfApproval', 'verifierInvalid')),
    scope_path                        ltree NOT NULL
);

DO $$ BEGIN IF to_regclass('identity.principal') IS NOT NULL THEN
ALTER TABLE identity.principal ADD COLUMN IF NOT EXISTS subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.session') IS NOT NULL THEN
ALTER TABLE identity.session ADD COLUMN IF NOT EXISTS subject_id uuid;
END IF; END $$;

CREATE TABLE IF NOT EXISTS identity.subject_erasure_part (
    id                                uuid PRIMARY KEY NOT NULL,
    request_id                        uuid NOT NULL,
    subject_id                        uuid NOT NULL,
    owner                             text NOT NULL CONSTRAINT subject_erasure_part_owner_chk CHECK (char_length(owner) <= 40),
    rows_erased                       integer NOT NULL,
    erased_at                         timestamptz NOT NULL
);

DO $$ BEGIN IF to_regclass('inventory.supplier') IS NOT NULL THEN
ALTER TABLE inventory.supplier ADD COLUMN IF NOT EXISTS contact_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.suppression') IS NOT NULL THEN
ALTER TABLE marketing.suppression ADD COLUMN IF NOT EXISTS address_hash text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL THEN
ALTER TABLE marketing.waiver_signature ADD COLUMN IF NOT EXISTS guardian_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL THEN
ALTER TABLE marketing.waiver_signature ADD COLUMN IF NOT EXISTS signer_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL THEN
ALTER TABLE marketing.waiver_signature ADD COLUMN IF NOT EXISTS participant_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'subject_name' AND is_nullable = 'NO') THEN ALTER TABLE marketing.waiver_signature ALTER COLUMN subject_name DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'signed_name' AND is_nullable = 'NO') THEN ALTER TABLE marketing.waiver_signature ALTER COLUMN signed_name DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart_line') IS NOT NULL THEN
ALTER TABLE orders.cart_line ADD COLUMN IF NOT EXISTS product_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_customer_organisation_contact') IS NOT NULL THEN
ALTER TABLE orders.group_customer_organisation_contact ADD COLUMN IF NOT EXISTS contact_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_customer_organisation_contact' AND column_name = 'name' AND is_nullable = 'NO') THEN ALTER TABLE orders.group_customer_organisation_contact ALTER COLUMN name DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_participant') IS NOT NULL THEN
ALTER TABLE orders.group_participant ADD COLUMN IF NOT EXISTS subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_participant' AND column_name = 'full_name' AND is_nullable = 'NO') THEN ALTER TABLE orders.group_participant ALTER COLUMN full_name DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.invitation') IS NOT NULL THEN
ALTER TABLE orders.invitation ADD COLUMN IF NOT EXISTS recipient_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL THEN
ALTER TABLE orders.order_line ADD COLUMN IF NOT EXISTS holder_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL THEN
ALTER TABLE orders.order_line ADD COLUMN IF NOT EXISTS product_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.reservation_line') IS NOT NULL THEN
ALTER TABLE orders.reservation_line ADD COLUMN IF NOT EXISTS holder_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.sales_order') IS NOT NULL THEN
ALTER TABLE orders.sales_order ADD COLUMN IF NOT EXISTS terms_version text CONSTRAINT sales_order_terms_version_chk CHECK (char_length(terms_version) <= 40);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.sales_order') IS NOT NULL THEN
ALTER TABLE orders.sales_order ADD COLUMN IF NOT EXISTS terms_accepted_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.ticket_transfer') IS NOT NULL THEN
ALTER TABLE orders.ticket_transfer ADD COLUMN IF NOT EXISTS recipient_channel text CONSTRAINT ticket_transfer_recipient_channel_chk CHECK (recipient_channel IN ('email', 'sms', 'whatsapp'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('pii.consent_identifier') IS NOT NULL THEN
ALTER TABLE pii.consent_identifier ADD COLUMN IF NOT EXISTS subject_id uuid;
END IF; END $$;

CREATE TABLE IF NOT EXISTS pii.subject_network_identifier (
    id                                uuid PRIMARY KEY NOT NULL,
    subject_id                        uuid NOT NULL,
    record_table                      text NOT NULL CONSTRAINT subject_network_identifier_record_table_chk CHECK (char_length(record_table) <= 63),
    record_id                         uuid NOT NULL,
    ip_address                        text NOT NULL CONSTRAINT subject_network_identifier_ip_address_chk CHECK (char_length(ip_address) <= 45),
    captured_at                       timestamptz NOT NULL
);

DO $$ BEGIN IF to_regclass('platform.device') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'device' AND column_name = 'kind') THEN
ALTER TABLE platform.device DROP CONSTRAINT IF EXISTS device_kind_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.device') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'device' AND column_name = 'kind') THEN
ALTER TABLE platform.device ADD CONSTRAINT device_kind_chk CHECK (kind IN ('receiptPrinter', 'ticketPrinter', 'labelPrinter', 'cashDrawer', 'barcodeScanner', 'rfidReader', 'nfcReader', 'cardReader', 'idReader', 'biometricReader', 'accessReader', 'paymentTerminal', 'customerDisplay', 'signageDisplay', 'kitchenDisplay', 'turnstileController', 'wristbandEncoder', 'signaturePad', 'scale', 'camera', 'mobileHandset', 'handheldScanner', 'accessPodium', 'bleBeacon', 'workstationTerminal')) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.device') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'device' AND column_name = 'kind') THEN
ALTER TABLE platform.device VALIDATE CONSTRAINT device_kind_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.agreement_signature') IS NOT NULL THEN
ALTER TABLE rental.agreement_signature ADD COLUMN IF NOT EXISTS signatory_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.participant') IS NOT NULL THEN
ALTER TABLE rental.participant ADD COLUMN IF NOT EXISTS emergency_contact_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.participant') IS NOT NULL THEN
ALTER TABLE rental.participant ADD COLUMN IF NOT EXISTS guardian_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.participant') IS NOT NULL THEN
ALTER TABLE rental.participant ADD COLUMN IF NOT EXISTS participant_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.group_request') IS NOT NULL THEN
ALTER TABLE seating.group_request ADD COLUMN IF NOT EXISTS contact_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.hold_pool') IS NOT NULL THEN
ALTER TABLE seating.hold_pool ADD COLUMN IF NOT EXISTS holder_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.employee') IS NOT NULL THEN
ALTER TABLE workforce.employee ADD COLUMN IF NOT EXISTS employee_subject_id uuid;
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'employee' AND column_name = 'first_name' AND is_nullable = 'NO') THEN ALTER TABLE workforce.employee ALTER COLUMN first_name DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'employee' AND column_name = 'last_name' AND is_nullable = 'NO') THEN ALTER TABLE workforce.employee ALTER COLUMN last_name DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'entitlement' AND column_name = 'holder_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'entitlement_holder_subject_id_fkey' AND conrelid = to_regclass('access.entitlement')) THEN
ALTER TABLE access.entitlement ADD CONSTRAINT entitlement_holder_subject_id_fkey FOREIGN KEY (holder_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.accreditation_badge') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'accreditation_badge' AND column_name = 'holder_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'accreditation_badge_holder_subject_id_fkey' AND conrelid = to_regclass('approvals.accreditation_badge')) THEN
ALTER TABLE approvals.accreditation_badge ADD CONSTRAINT accreditation_badge_holder_subject_id_fkey FOREIGN KEY (holder_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('assets.share') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'assets' AND table_name = 'share' AND column_name = 'recipient_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'share_recipient_subject_id_fkey' AND conrelid = to_regclass('assets.share')) THEN
ALTER TABLE assets.share ADD CONSTRAINT share_recipient_subject_id_fkey FOREIGN KEY (recipient_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.table_visit_server') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'recorded_by_principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'table_visit_server_recorded_by_principal_id_fkey' AND conrelid = to_regclass('fnb.table_visit_server')) THEN
ALTER TABLE fnb.table_visit_server ADD CONSTRAINT table_visit_server_recorded_by_principal_id_fkey FOREIGN KEY (recorded_by_principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.table_visit_server') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'server_principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'table_visit_server_server_principal_id_fkey' AND conrelid = to_regclass('fnb.table_visit_server')) THEN
ALTER TABLE fnb.table_visit_server ADD CONSTRAINT table_visit_server_server_principal_id_fkey FOREIGN KEY (server_principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.table_visit_server') IS NOT NULL AND to_regclass('fnb.table_visit') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'table_visit_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'table_visit_server_table_visit_id_fkey' AND conrelid = to_regclass('fnb.table_visit_server')) THEN
ALTER TABLE fnb.table_visit_server ADD CONSTRAINT table_visit_server_table_visit_id_fkey FOREIGN KEY (table_visit_id) REFERENCES fnb.table_visit(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity."session"') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'session_subject_id_fkey' AND conrelid = to_regclass('identity."session"')) THEN
ALTER TABLE identity."session" ADD CONSTRAINT session_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_pin_verifier') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_pin_verifier' AND column_name = 'principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'offline_pin_verifier_principal_id_fkey' AND conrelid = to_regclass('identity.offline_pin_verifier')) THEN
ALTER TABLE identity.offline_pin_verifier ADD CONSTRAINT offline_pin_verifier_principal_id_fkey FOREIGN KEY (principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_step_up') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_step_up' AND column_name = 'caller_principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'offline_step_up_caller_principal_id_fkey' AND conrelid = to_regclass('identity.offline_step_up')) THEN
ALTER TABLE identity.offline_step_up ADD CONSTRAINT offline_step_up_caller_principal_id_fkey FOREIGN KEY (caller_principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_step_up') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_step_up' AND column_name = 'signer_principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'offline_step_up_signer_principal_id_fkey' AND conrelid = to_regclass('identity.offline_step_up')) THEN
ALTER TABLE identity.offline_step_up ADD CONSTRAINT offline_step_up_signer_principal_id_fkey FOREIGN KEY (signer_principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.principal') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'principal' AND column_name = 'subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'principal_subject_id_fkey' AND conrelid = to_regclass('identity.principal')) THEN
ALTER TABLE identity.principal ADD CONSTRAINT principal_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_erasure_part') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_erasure_part' AND column_name = 'subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'subject_erasure_part_subject_id_fkey' AND conrelid = to_regclass('identity.subject_erasure_part')) THEN
ALTER TABLE identity.subject_erasure_part ADD CONSTRAINT subject_erasure_part_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('inventory.supplier') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'inventory' AND table_name = 'supplier' AND column_name = 'contact_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'supplier_contact_subject_id_fkey' AND conrelid = to_regclass('inventory.supplier')) THEN
ALTER TABLE inventory.supplier ADD CONSTRAINT supplier_contact_subject_id_fkey FOREIGN KEY (contact_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'guardian_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'waiver_signature_guardian_subject_id_fkey' AND conrelid = to_regclass('marketing.waiver_signature')) THEN
ALTER TABLE marketing.waiver_signature ADD CONSTRAINT waiver_signature_guardian_subject_id_fkey FOREIGN KEY (guardian_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'participant_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'waiver_signature_participant_subject_id_fkey' AND conrelid = to_regclass('marketing.waiver_signature')) THEN
ALTER TABLE marketing.waiver_signature ADD CONSTRAINT waiver_signature_participant_subject_id_fkey FOREIGN KEY (participant_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'signer_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'waiver_signature_signer_subject_id_fkey' AND conrelid = to_regclass('marketing.waiver_signature')) THEN
ALTER TABLE marketing.waiver_signature ADD CONSTRAINT waiver_signature_signer_subject_id_fkey FOREIGN KEY (signer_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart_line') IS NOT NULL AND to_regclass('catalogue.product') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart_line' AND column_name = 'product_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cart_line_product_id_fkey' AND conrelid = to_regclass('orders.cart_line')) THEN
ALTER TABLE orders.cart_line ADD CONSTRAINT cart_line_product_id_fkey FOREIGN KEY (product_id) REFERENCES catalogue.product(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_customer_organisation_contact') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_customer_organisation_contact' AND column_name = 'contact_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_customer_organisation_contact_contact_subject_id_fkey' AND conrelid = to_regclass('orders.group_customer_organisation_contact')) THEN
ALTER TABLE orders.group_customer_organisation_contact ADD CONSTRAINT group_customer_organisation_contact_contact_subject_id_fkey FOREIGN KEY (contact_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_participant') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_participant' AND column_name = 'subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_participant_subject_id_fkey' AND conrelid = to_regclass('orders.group_participant')) THEN
ALTER TABLE orders.group_participant ADD CONSTRAINT group_participant_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.invitation') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'invitation' AND column_name = 'recipient_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'invitation_recipient_subject_id_fkey' AND conrelid = to_regclass('orders.invitation')) THEN
ALTER TABLE orders.invitation ADD CONSTRAINT invitation_recipient_subject_id_fkey FOREIGN KEY (recipient_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'holder_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'order_line_holder_subject_id_fkey' AND conrelid = to_regclass('orders.order_line')) THEN
ALTER TABLE orders.order_line ADD CONSTRAINT order_line_holder_subject_id_fkey FOREIGN KEY (holder_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL AND to_regclass('catalogue.product') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'product_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'order_line_product_id_fkey' AND conrelid = to_regclass('orders.order_line')) THEN
ALTER TABLE orders.order_line ADD CONSTRAINT order_line_product_id_fkey FOREIGN KEY (product_id) REFERENCES catalogue.product(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.reservation_line') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'reservation_line' AND column_name = 'holder_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'reservation_line_holder_subject_id_fkey' AND conrelid = to_regclass('orders.reservation_line')) THEN
ALTER TABLE orders.reservation_line ADD CONSTRAINT reservation_line_holder_subject_id_fkey FOREIGN KEY (holder_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('pii.subject_network_identifier') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pii' AND table_name = 'subject_network_identifier' AND column_name = 'subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'subject_network_identifier_subject_id_fkey' AND conrelid = to_regclass('pii.subject_network_identifier')) THEN
ALTER TABLE pii.subject_network_identifier ADD CONSTRAINT subject_network_identifier_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.agreement_signature') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'rental' AND table_name = 'agreement_signature' AND column_name = 'signatory_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'agreement_signature_signatory_subject_id_fkey' AND conrelid = to_regclass('rental.agreement_signature')) THEN
ALTER TABLE rental.agreement_signature ADD CONSTRAINT agreement_signature_signatory_subject_id_fkey FOREIGN KEY (signatory_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.participant') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'rental' AND table_name = 'participant' AND column_name = 'emergency_contact_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'participant_emergency_contact_subject_id_fkey' AND conrelid = to_regclass('rental.participant')) THEN
ALTER TABLE rental.participant ADD CONSTRAINT participant_emergency_contact_subject_id_fkey FOREIGN KEY (emergency_contact_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.participant') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'rental' AND table_name = 'participant' AND column_name = 'guardian_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'participant_guardian_subject_id_fkey' AND conrelid = to_regclass('rental.participant')) THEN
ALTER TABLE rental.participant ADD CONSTRAINT participant_guardian_subject_id_fkey FOREIGN KEY (guardian_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.participant') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'rental' AND table_name = 'participant' AND column_name = 'participant_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'participant_participant_subject_id_fkey' AND conrelid = to_regclass('rental.participant')) THEN
ALTER TABLE rental.participant ADD CONSTRAINT participant_participant_subject_id_fkey FOREIGN KEY (participant_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.group_request') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'group_request' AND column_name = 'contact_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'group_request_contact_subject_id_fkey' AND conrelid = to_regclass('seating.group_request')) THEN
ALTER TABLE seating.group_request ADD CONSTRAINT group_request_contact_subject_id_fkey FOREIGN KEY (contact_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.hold_pool') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'hold_pool' AND column_name = 'holder_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'hold_pool_holder_subject_id_fkey' AND conrelid = to_regclass('seating.hold_pool')) THEN
ALTER TABLE seating.hold_pool ADD CONSTRAINT hold_pool_holder_subject_id_fkey FOREIGN KEY (holder_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.employee') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'employee' AND column_name = 'employee_subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'employee_employee_subject_id_fkey' AND conrelid = to_regclass('workforce.employee')) THEN
ALTER TABLE workforce.employee ADD CONSTRAINT employee_employee_subject_id_fkey FOREIGN KEY (employee_subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.message') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ai' AND table_name = 'message' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS message_subject_id_idx ON ai.message (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.service_order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'service_order_line' AND column_name = 'comped_by_principal_id') THEN
CREATE INDEX IF NOT EXISTS service_order_line_comped_by_principal_id_idx ON fnb.service_order_line (comped_by_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('pii.consent_identifier') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pii' AND table_name = 'consent_identifier' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS consent_identifier_subject_id_idx ON pii.consent_identifier (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('catalogue.product') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'product' AND column_name = 'display_order') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'product' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'catalogue' AND table_name = 'product' AND column_name = 'venue_id') THEN
CREATE INDEX IF NOT EXISTS product_venue_id_display_order_id_idx ON catalogue.product (venue_id, display_order, id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.table_visit_server') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'from_at') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'table_visit_id') THEN
CREATE INDEX IF NOT EXISTS table_visit_server_table_visit_id_from_at_idx ON fnb.table_visit_server (table_visit_id, from_at);
END IF; END $$;

DO $$ BEGIN IF to_regclass('pii.subject_network_identifier') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pii' AND table_name = 'subject_network_identifier' AND column_name = 'record_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pii' AND table_name = 'subject_network_identifier' AND column_name = 'record_table') THEN
CREATE INDEX IF NOT EXISTS subject_network_identifier_record_table_record_id_idx ON pii.subject_network_identifier (record_table, record_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('access.entitlement') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'access' AND table_name = 'entitlement' AND column_name = 'holder_subject_id') THEN
CREATE INDEX IF NOT EXISTS entitlement_holder_subject_id_idx ON access.entitlement (holder_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.accreditation_badge') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'accreditation_badge' AND column_name = 'holder_subject_id') THEN
CREATE INDEX IF NOT EXISTS accreditation_badge_holder_subject_id_idx ON approvals.accreditation_badge (holder_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('assets.share') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'assets' AND table_name = 'share' AND column_name = 'recipient_subject_id') THEN
CREATE INDEX IF NOT EXISTS share_recipient_subject_id_idx ON assets.share (recipient_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.table_visit_server') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'recorded_by_principal_id') THEN
CREATE INDEX IF NOT EXISTS table_visit_server_recorded_by_principal_id_idx ON fnb.table_visit_server (recorded_by_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.table_visit_server') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'server_principal_id') THEN
CREATE INDEX IF NOT EXISTS table_visit_server_server_principal_id_idx ON fnb.table_visit_server (server_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.table_visit_server') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'table_visit_id') THEN
CREATE INDEX IF NOT EXISTS table_visit_server_table_visit_id_idx ON fnb.table_visit_server (table_visit_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_pin_verifier') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_pin_verifier' AND column_name = 'principal_id') THEN
CREATE INDEX IF NOT EXISTS offline_pin_verifier_principal_id_idx ON identity.offline_pin_verifier (principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_step_up') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_step_up' AND column_name = 'caller_principal_id') THEN
CREATE INDEX IF NOT EXISTS offline_step_up_caller_principal_id_idx ON identity.offline_step_up (caller_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_step_up') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_step_up' AND column_name = 'signer_principal_id') THEN
CREATE INDEX IF NOT EXISTS offline_step_up_signer_principal_id_idx ON identity.offline_step_up (signer_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'principal' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS principal_subject_id_idx ON identity.principal (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity."session"') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'session' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS session_subject_id_idx ON identity."session" (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_erasure_part') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_erasure_part' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS subject_erasure_part_subject_id_idx ON identity.subject_erasure_part (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('inventory.supplier') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'inventory' AND table_name = 'supplier' AND column_name = 'contact_subject_id') THEN
CREATE INDEX IF NOT EXISTS supplier_contact_subject_id_idx ON inventory.supplier (contact_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'guardian_subject_id') THEN
CREATE INDEX IF NOT EXISTS waiver_signature_guardian_subject_id_idx ON marketing.waiver_signature (guardian_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'participant_subject_id') THEN
CREATE INDEX IF NOT EXISTS waiver_signature_participant_subject_id_idx ON marketing.waiver_signature (participant_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'signer_subject_id') THEN
CREATE INDEX IF NOT EXISTS waiver_signature_signer_subject_id_idx ON marketing.waiver_signature (signer_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart_line' AND column_name = 'product_id') THEN
CREATE INDEX IF NOT EXISTS cart_line_product_id_idx ON orders.cart_line (product_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_customer_organisation_contact') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_customer_organisation_contact' AND column_name = 'contact_subject_id') THEN
CREATE INDEX IF NOT EXISTS group_customer_organisation_contact_contact_subject_id_idx ON orders.group_customer_organisation_contact (contact_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.group_participant') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'group_participant' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS group_participant_subject_id_idx ON orders.group_participant (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.invitation') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'invitation' AND column_name = 'recipient_subject_id') THEN
CREATE INDEX IF NOT EXISTS invitation_recipient_subject_id_idx ON orders.invitation (recipient_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'holder_subject_id') THEN
CREATE INDEX IF NOT EXISTS order_line_holder_subject_id_idx ON orders.order_line (holder_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'product_id') THEN
CREATE INDEX IF NOT EXISTS order_line_product_id_idx ON orders.order_line (product_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.reservation_line') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'reservation_line' AND column_name = 'holder_subject_id') THEN
CREATE INDEX IF NOT EXISTS reservation_line_holder_subject_id_idx ON orders.reservation_line (holder_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('pii.subject_network_identifier') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pii' AND table_name = 'subject_network_identifier' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS subject_network_identifier_subject_id_idx ON pii.subject_network_identifier (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.agreement_signature') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'rental' AND table_name = 'agreement_signature' AND column_name = 'signatory_subject_id') THEN
CREATE INDEX IF NOT EXISTS agreement_signature_signatory_subject_id_idx ON rental.agreement_signature (signatory_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.participant') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'rental' AND table_name = 'participant' AND column_name = 'emergency_contact_subject_id') THEN
CREATE INDEX IF NOT EXISTS participant_emergency_contact_subject_id_idx ON rental.participant (emergency_contact_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.participant') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'rental' AND table_name = 'participant' AND column_name = 'guardian_subject_id') THEN
CREATE INDEX IF NOT EXISTS participant_guardian_subject_id_idx ON rental.participant (guardian_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('rental.participant') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'rental' AND table_name = 'participant' AND column_name = 'participant_subject_id') THEN
CREATE INDEX IF NOT EXISTS participant_participant_subject_id_idx ON rental.participant (participant_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.group_request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'group_request' AND column_name = 'contact_subject_id') THEN
CREATE INDEX IF NOT EXISTS group_request_contact_subject_id_idx ON seating.group_request (contact_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('seating.hold_pool') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'seating' AND table_name = 'hold_pool' AND column_name = 'holder_subject_id') THEN
CREATE INDEX IF NOT EXISTS hold_pool_holder_subject_id_idx ON seating.hold_pool (holder_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.employee') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'employee' AND column_name = 'employee_subject_id') THEN
CREATE INDEX IF NOT EXISTS employee_employee_subject_id_idx ON workforce.employee (employee_subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_pin_verifier') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_pin_verifier' AND column_name = 'principal_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_pin_verifier' AND column_name = 'venue_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS offline_pin_verifier_principal_id_venue_id_uniq ON identity.offline_pin_verifier (principal_id, venue_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_step_up') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_step_up' AND column_name = 'act_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_step_up' AND column_name = 'operation_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS offline_step_up_operation_id_act_id_uniq ON identity.offline_step_up (lower(operation_id), act_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_erasure_part') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_erasure_part' AND column_name = 'owner') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_erasure_part' AND column_name = 'request_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS subject_erasure_part_request_id_owner_uniq ON identity.subject_erasure_part (request_id, lower(owner));
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_pin_verifier') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_pin_verifier' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS offline_pin_verifier_scope_path_idx ON identity.offline_pin_verifier USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_step_up') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_step_up' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS offline_step_up_scope_path_idx ON identity.offline_step_up USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.table_visit_server') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS table_visit_server_scope_path_idx ON fnb.table_visit_server USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('fnb.table_visit_server') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'fnb' AND table_name = 'table_visit_server' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('fnb.table_visit_server'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_pin_verifier') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_pin_verifier' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('identity.offline_pin_verifier'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.offline_step_up') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'offline_step_up' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('identity.offline_step_up'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.message_dispatch') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'message_dispatch' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.message_dispatch'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('marketing.message_dispatch'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_erasure_part') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_erasure_part' AND column_name = 'subject_id') THEN
PERFORM platform.apply_subject_rls('identity.subject_erasure_part'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('pii.subject_network_identifier') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pii' AND table_name = 'subject_network_identifier' AND column_name = 'subject_id') THEN
PERFORM platform.apply_subject_rls('pii.subject_network_identifier'::regclass);
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('identity.principal') IS NOT NULL THEN GRANT SELECT (id, is_active, valid_from, valid_to) ON identity.principal TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('identity.principal') IS NOT NULL THEN GRANT SELECT (id, is_active, subject_id) ON identity.principal TO operations; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0129', 'after r1 (9cec72d): 5 table(s), 36 column(s), 43 index(es), 47 other statement(s), 1 row-level security polic(ies) re-applied', 'dcb9e9ebb4501e610a2701f35dffc1d32339e415cd8b03f175ab5e65fd05d9e6')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- REVOKE SELECT (id, is_active, subject_id) ON identity.principal FROM operations;
-- REVOKE SELECT (id, is_active, valid_from, valid_to) ON identity.principal FROM operations;
-- SELECT platform.drop_rls_policies('marketing.message_dispatch'::regclass); SELECT platform.apply_subject_rls('marketing.message_dispatch'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('marketing.message_dispatch'::regclass);
-- DROP INDEX IF EXISTS fnb.table_visit_server_scope_path_idx;
-- DROP INDEX IF EXISTS identity.offline_step_up_scope_path_idx;
-- DROP INDEX IF EXISTS identity.offline_pin_verifier_scope_path_idx;
-- DROP INDEX IF EXISTS identity.subject_erasure_part_request_id_owner_uniq;
-- DROP INDEX IF EXISTS identity.offline_step_up_operation_id_act_id_uniq;
-- DROP INDEX IF EXISTS identity.offline_pin_verifier_principal_id_venue_id_uniq;
-- DROP INDEX IF EXISTS workforce.employee_employee_subject_id_idx;
-- DROP INDEX IF EXISTS seating.hold_pool_holder_subject_id_idx;
-- DROP INDEX IF EXISTS seating.group_request_contact_subject_id_idx;
-- DROP INDEX IF EXISTS rental.participant_participant_subject_id_idx;
-- DROP INDEX IF EXISTS rental.participant_guardian_subject_id_idx;
-- DROP INDEX IF EXISTS rental.participant_emergency_contact_subject_id_idx;
-- DROP INDEX IF EXISTS rental.agreement_signature_signatory_subject_id_idx;
-- DROP INDEX IF EXISTS pii.subject_network_identifier_subject_id_idx;
-- DROP INDEX IF EXISTS orders.reservation_line_holder_subject_id_idx;
-- DROP INDEX IF EXISTS orders.order_line_product_id_idx;
-- DROP INDEX IF EXISTS orders.order_line_holder_subject_id_idx;
-- DROP INDEX IF EXISTS orders.invitation_recipient_subject_id_idx;
-- DROP INDEX IF EXISTS orders.group_participant_subject_id_idx;
-- DROP INDEX IF EXISTS orders.group_customer_organisation_contact_contact_subject_id_idx;
-- DROP INDEX IF EXISTS orders.cart_line_product_id_idx;
-- DROP INDEX IF EXISTS marketing.waiver_signature_signer_subject_id_idx;
-- DROP INDEX IF EXISTS marketing.waiver_signature_participant_subject_id_idx;
-- DROP INDEX IF EXISTS marketing.waiver_signature_guardian_subject_id_idx;
-- DROP INDEX IF EXISTS inventory.supplier_contact_subject_id_idx;
-- DROP INDEX IF EXISTS identity.subject_erasure_part_subject_id_idx;
-- DROP INDEX IF EXISTS identity.session_subject_id_idx;
-- DROP INDEX IF EXISTS identity.principal_subject_id_idx;
-- DROP INDEX IF EXISTS identity.offline_step_up_signer_principal_id_idx;
-- DROP INDEX IF EXISTS identity.offline_step_up_caller_principal_id_idx;
-- DROP INDEX IF EXISTS identity.offline_pin_verifier_principal_id_idx;
-- DROP INDEX IF EXISTS fnb.table_visit_server_table_visit_id_idx;
-- DROP INDEX IF EXISTS fnb.table_visit_server_server_principal_id_idx;
-- DROP INDEX IF EXISTS fnb.table_visit_server_recorded_by_principal_id_idx;
-- DROP INDEX IF EXISTS assets.share_recipient_subject_id_idx;
-- DROP INDEX IF EXISTS approvals.accreditation_badge_holder_subject_id_idx;
-- DROP INDEX IF EXISTS access.entitlement_holder_subject_id_idx;
-- DROP INDEX IF EXISTS pii.subject_network_identifier_record_table_record_id_idx;
-- DROP INDEX IF EXISTS fnb.table_visit_server_table_visit_id_from_at_idx;
-- DROP INDEX IF EXISTS catalogue.product_venue_id_display_order_id_idx;
-- DROP INDEX IF EXISTS pii.consent_identifier_subject_id_idx;
-- DROP INDEX IF EXISTS fnb.service_order_line_comped_by_principal_id_idx;
-- DROP INDEX IF EXISTS ai.message_subject_id_idx;
-- ALTER TABLE workforce.employee DROP CONSTRAINT IF EXISTS employee_employee_subject_id_fkey;
-- ALTER TABLE seating.hold_pool DROP CONSTRAINT IF EXISTS hold_pool_holder_subject_id_fkey;
-- ALTER TABLE seating.group_request DROP CONSTRAINT IF EXISTS group_request_contact_subject_id_fkey;
-- ALTER TABLE rental.participant DROP CONSTRAINT IF EXISTS participant_participant_subject_id_fkey;
-- ALTER TABLE rental.participant DROP CONSTRAINT IF EXISTS participant_guardian_subject_id_fkey;
-- ALTER TABLE rental.participant DROP CONSTRAINT IF EXISTS participant_emergency_contact_subject_id_fkey;
-- ALTER TABLE rental.agreement_signature DROP CONSTRAINT IF EXISTS agreement_signature_signatory_subject_id_fkey;
-- ALTER TABLE orders.reservation_line DROP CONSTRAINT IF EXISTS reservation_line_holder_subject_id_fkey;
-- ALTER TABLE orders.order_line DROP CONSTRAINT IF EXISTS order_line_product_id_fkey;
-- ALTER TABLE orders.order_line DROP CONSTRAINT IF EXISTS order_line_holder_subject_id_fkey;
-- ALTER TABLE orders.invitation DROP CONSTRAINT IF EXISTS invitation_recipient_subject_id_fkey;
-- ALTER TABLE orders.group_participant DROP CONSTRAINT IF EXISTS group_participant_subject_id_fkey;
-- ALTER TABLE orders.group_customer_organisation_contact DROP CONSTRAINT IF EXISTS group_customer_organisation_contact_contact_subject_id_fkey;
-- ALTER TABLE orders.cart_line DROP CONSTRAINT IF EXISTS cart_line_product_id_fkey;
-- ALTER TABLE marketing.waiver_signature DROP CONSTRAINT IF EXISTS waiver_signature_signer_subject_id_fkey;
-- ALTER TABLE marketing.waiver_signature DROP CONSTRAINT IF EXISTS waiver_signature_participant_subject_id_fkey;
-- ALTER TABLE marketing.waiver_signature DROP CONSTRAINT IF EXISTS waiver_signature_guardian_subject_id_fkey;
-- ALTER TABLE inventory.supplier DROP CONSTRAINT IF EXISTS supplier_contact_subject_id_fkey;
-- ALTER TABLE identity.principal DROP CONSTRAINT IF EXISTS principal_subject_id_fkey;
-- ALTER TABLE identity.session DROP CONSTRAINT IF EXISTS session_subject_id_fkey;
-- ALTER TABLE assets.share DROP CONSTRAINT IF EXISTS share_recipient_subject_id_fkey;
-- ALTER TABLE approvals.accreditation_badge DROP CONSTRAINT IF EXISTS accreditation_badge_holder_subject_id_fkey;
-- ALTER TABLE access.entitlement DROP CONSTRAINT IF EXISTS entitlement_holder_subject_id_fkey;
-- ALTER TABLE workforce.employee ALTER COLUMN last_name SET NOT NULL;
-- ALTER TABLE workforce.employee ALTER COLUMN first_name SET NOT NULL;
-- ALTER TABLE workforce.employee DROP COLUMN IF EXISTS employee_subject_id;
-- ALTER TABLE seating.hold_pool DROP COLUMN IF EXISTS holder_subject_id;
-- ALTER TABLE seating.group_request DROP COLUMN IF EXISTS contact_subject_id;
-- ALTER TABLE rental.participant DROP COLUMN IF EXISTS participant_subject_id;
-- ALTER TABLE rental.participant DROP COLUMN IF EXISTS guardian_subject_id;
-- ALTER TABLE rental.participant DROP COLUMN IF EXISTS emergency_contact_subject_id;
-- ALTER TABLE rental.agreement_signature DROP COLUMN IF EXISTS signatory_subject_id;
-- ALTER TABLE platform.device DROP CONSTRAINT IF EXISTS device_kind_chk; ALTER TABLE platform.device ADD CONSTRAINT device_kind_chk CHECK (kind IN ('receiptPrinter', 'ticketPrinter', 'labelPrinter', 'cashDrawer', 'barcodeScanner', 'rfidReader', 'nfcReader', 'cardReader', 'idReader', 'biometricReader', 'accessReader', 'paymentTerminal', 'customerDisplay', 'signageDisplay', 'kitchenDisplay', 'turnstileController', 'wristbandEncoder', 'signaturePad', 'scale', 'camera', 'mobileHandset', 'handheldScanner', 'accessPodium', 'bleBeacon')) NOT VALID;
-- DROP TABLE IF EXISTS pii.subject_network_identifier;
-- ALTER TABLE pii.consent_identifier DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE orders.ticket_transfer DROP COLUMN IF EXISTS recipient_channel;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS terms_accepted_at;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS terms_version;
-- ALTER TABLE orders.reservation_line DROP COLUMN IF EXISTS holder_subject_id;
-- ALTER TABLE orders.order_line DROP COLUMN IF EXISTS product_id;
-- ALTER TABLE orders.order_line DROP COLUMN IF EXISTS holder_subject_id;
-- ALTER TABLE orders.invitation DROP COLUMN IF EXISTS recipient_subject_id;
-- ALTER TABLE orders.group_participant ALTER COLUMN full_name SET NOT NULL;
-- ALTER TABLE orders.group_participant DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE orders.group_customer_organisation_contact ALTER COLUMN name SET NOT NULL;
-- ALTER TABLE orders.group_customer_organisation_contact DROP COLUMN IF EXISTS contact_subject_id;
-- ALTER TABLE orders.cart_line DROP COLUMN IF EXISTS product_id;
-- ALTER TABLE marketing.waiver_signature ALTER COLUMN signed_name SET NOT NULL;
-- ALTER TABLE marketing.waiver_signature ALTER COLUMN subject_name SET NOT NULL;
-- ALTER TABLE marketing.waiver_signature DROP COLUMN IF EXISTS participant_subject_id;
-- ALTER TABLE marketing.waiver_signature DROP COLUMN IF EXISTS signer_subject_id;
-- ALTER TABLE marketing.waiver_signature DROP COLUMN IF EXISTS guardian_subject_id;
-- ALTER TABLE marketing.suppression DROP COLUMN IF EXISTS address_hash;
-- ALTER TABLE inventory.supplier DROP COLUMN IF EXISTS contact_subject_id;
-- DROP TABLE IF EXISTS identity.subject_erasure_part;
-- ALTER TABLE identity.session DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE identity.principal DROP COLUMN IF EXISTS subject_id;
-- DROP TABLE IF EXISTS identity.offline_step_up;
-- DROP TABLE IF EXISTS identity.offline_pin_verifier;
-- DROP TABLE IF EXISTS fnb.table_visit_server;
-- ALTER TABLE fnb.service_order_line DROP COLUMN IF EXISTS comped_by_principal_id;
-- ALTER TABLE fnb.service_order_line DROP COLUMN IF EXISTS comp_reason;
-- ALTER TABLE fnb.service_order_line DROP COLUMN IF EXISTS comped_at;
-- ALTER TABLE fnb.service_order_line DROP CONSTRAINT IF EXISTS service_order_line_status_chk;
-- ALTER TABLE catalogue.product DROP COLUMN IF EXISTS display_order;
-- ALTER TABLE catalogue.performance DROP COLUMN IF EXISTS admission_starts_at;
-- ALTER TABLE assets.share DROP COLUMN IF EXISTS recipient_subject_id;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS platform_minimum_approvals;
-- ALTER TABLE approvals.request DROP COLUMN IF EXISTS platform_approver_permission;
-- ALTER TABLE approvals.accreditation_badge DROP COLUMN IF EXISTS holder_subject_id;
-- ALTER TABLE ai.message DROP COLUMN IF EXISTS subject_id;
-- ALTER TABLE accreditation.holder ALTER COLUMN full_name SET NOT NULL;
-- ALTER TABLE access.entitlement DROP COLUMN IF EXISTS holder_subject_id;
-- DELETE FROM platform.schema_version WHERE version = 'V0129';
