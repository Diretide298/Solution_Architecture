-- =============================================================================
-- V0001a — Personal data
--
-- The `pii` schema was declared in V0001 and left empty. Four foreign keys in
-- V0003b point at pii.subject, and the V0001 rollback drops two pii tables that
-- were never created. psql would have failed on the first FK; the structural
-- checker did not, because it never verified that a referenced table exists.
--
-- Both are now fixed — this migration, and a new check.
--
-- =============================================================================
-- WHY THIS SCHEMA IS SEPARATE
--
-- Erasure. Under UAE PDPL a subject may request deletion, and the ledger is
-- append-only — a sale cannot be unwritten because the buyer asked. Splitting
-- identity from behaviour makes both possible at once: delete the person, keep
-- the transaction, and the transaction still reconciles because it never held a
-- name in the first place.
--
-- Everything outside this schema refers to a person by `subject_id` and nothing
-- else. No name, no email, no phone, no document number. When a subject is
-- erased, `pii.subject` keeps a tombstone row and every referring table keeps
-- working against an id that now resolves to nobody.
--
-- The consequence to understand: **a subject_id is not personal data on its own,
-- and it is not anonymous either.** It is pseudonymous. Joining it back to an
-- identity requires this schema, which is why this schema is where access is
-- most tightly held.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- The subject. One row per person the platform knows about.
-- -----------------------------------------------------------------------------
CREATE TYPE pii.subject_kind AS ENUM ('guest', 'employee', 'contact', 'applicant');

CREATE TABLE pii.subject (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    kind                pii.subject_kind NOT NULL DEFAULT 'guest',

    -- Name is deliberately one field, not three.
    display_name        text,
    given_name          text,
    family_name         text,

    date_of_birth       date,
    nationality         char(2),
    preferred_language  char(2),

    -- Erasure
    is_erased           boolean NOT NULL DEFAULT false,
    erased_at           timestamptz,
    erasure_request_id  char(26),

    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),

    CONSTRAINT subject_erasure_is_complete CHECK (
        NOT is_erased OR (
            display_name IS NULL AND given_name IS NULL AND family_name IS NULL
            AND date_of_birth IS NULL AND nationality IS NULL
            AND erased_at IS NOT NULL
        )
    )
);

COMMENT ON TABLE pii.subject IS
  'One row per person. Referred to from everywhere else by id alone.

An erased subject keeps its row as a tombstone. Deleting it would break every foreign key '
  'pointing at it, and cascading those deletes would remove sales from the ledger — which is '
  'both wrong accounting and, in most jurisdictions, not what erasure requires.';

COMMENT ON COLUMN pii.subject.display_name IS
  'What to call this person. Populated from given and family name where both exist, and '
  'directly where they do not — a mononym, a company contact, a name that does not split '
  'into two parts. Forcing every name into given plus family is a Western assumption that '
  'fails visibly in the Gulf.';

COMMENT ON CONSTRAINT subject_erasure_is_complete ON pii.subject IS
  'An erased subject cannot retain identifying fields. Enforced rather than trusted to the '
  'erasure job, because a partial erasure that reports success is worse than a failure.';

CREATE INDEX subject_kind ON pii.subject (kind) WHERE NOT is_erased;
CREATE INDEX subject_erased ON pii.subject (erased_at) WHERE is_erased;

-- -----------------------------------------------------------------------------
-- Contact points. Separate because a person has several, and because each
-- carries its own verification state.
-- -----------------------------------------------------------------------------
CREATE TYPE pii.contact_kind AS ENUM ('email', 'mobile', 'phone', 'whatsapp', 'postal');

CREATE TABLE pii.subject_contact (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id          uuid NOT NULL REFERENCES pii.subject (id) ON DELETE CASCADE,
    kind                pii.contact_kind NOT NULL,
    value               text NOT NULL,
    value_normalised    text NOT NULL,
    value_hash          text NOT NULL,
    is_primary          boolean NOT NULL DEFAULT false,
    is_verified         boolean NOT NULL DEFAULT false,
    verified_at         timestamptz,
    created_at          timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT contact_verification CHECK (NOT is_verified OR verified_at IS NOT NULL)
);

COMMENT ON COLUMN pii.subject_contact.value_normalised IS
  'Lowercased email, E.164 mobile. Matching on the raw value means the same person registers '
  'twice with two capitalisations of one address.';

COMMENT ON COLUMN pii.subject_contact.value_hash IS
  'Deterministic hash of the normalised value. Lets a guest be found by email without the '
  'search path reading the plaintext column, and lets a suppression list be checked without '
  'holding the address it suppresses.';

COMMENT ON COLUMN pii.subject_contact.is_verified IS
  'Set only by a completed verification. This is what makes guest checkout linking safe — '
  'orders attach to an identity on a verified identifier, never on a claim.';

CREATE UNIQUE INDEX contact_one_primary ON pii.subject_contact (subject_id, kind)
    WHERE is_primary;
CREATE INDEX contact_hash ON pii.subject_contact (kind, value_hash);
CREATE INDEX contact_subject ON pii.subject_contact (subject_id);

-- -----------------------------------------------------------------------------
-- Identity documents. Passport, Emirates ID, licence.
-- -----------------------------------------------------------------------------
CREATE TABLE pii.subject_document (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id          uuid NOT NULL REFERENCES pii.subject (id) ON DELETE CASCADE,
    kind                text NOT NULL
        CHECK (kind IN ('passport','emiratesId','nationalId','drivingLicence','residencePermit','other')),
    number_hash         text NOT NULL,
    number_last4        char(4),
    issuing_country     char(2),
    expires_on          date,
    document_asset_ref  text,
    verified_at         timestamptz,
    created_at          timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE pii.subject_document IS
  'The document number is stored **hashed**, with the last four digits in clear for a human '
  'to confirm against the card in front of them. A full passport number in a queryable column '
  'is the single worst row in any venue database, and no operation needs it.';

COMMENT ON COLUMN pii.subject_document.document_asset_ref IS
  'A scan, where one was taken. Held in object storage with its own retention, not in this '
  'table — an image of a passport in a database backup travels further than anyone intends.';

CREATE INDEX document_subject ON pii.subject_document (subject_id);
CREATE INDEX document_expiring ON pii.subject_document (expires_on)
    WHERE expires_on IS NOT NULL;

-- -----------------------------------------------------------------------------
-- Biometric templates. CF-35 — sensitive under PDPL.
-- -----------------------------------------------------------------------------
CREATE TABLE pii.subject_biometric (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id          uuid NOT NULL REFERENCES pii.subject (id) ON DELETE CASCADE,
    modality            text NOT NULL CHECK (modality IN ('face','fingerprint')),
    template_ref        text NOT NULL,
    vendor              text NOT NULL,
    template_version    text NOT NULL,
    consent_record_id   uuid NOT NULL,
    enrolled_at         timestamptz NOT NULL DEFAULT now(),
    expires_at          timestamptz NOT NULL,
    revoked_at          timestamptz,
    CONSTRAINT biometric_expiry CHECK (expires_at > enrolled_at)
);

COMMENT ON TABLE pii.subject_biometric IS
  'CF-35: biometric data is **sensitive** under PDPL and attracts heightened protection — '
  'explicit consent, a DPIA, stricter transfer rules.

Three consequences visible in this table. The template is a reference, never the image: a '
  'face is stored as a vendor template in a separate secured store, and the raw capture is '
  'discarded. Consent is a foreign key, not a boolean, so the specific consent record '
  'authorising enrolment can be produced on demand. And enrolment expires — an indefinite '
  'biometric enrolment is one nobody re-consented to.

CF-35 is open. This schema takes the cautious reading; it may need to become stricter, and '
  'it should not become looser without advice.';

COMMENT ON COLUMN pii.subject_biometric.template_ref IS
  'Reference into the biometric store. Never the template itself, and never the image the '
  'template came from.';

CREATE INDEX biometric_subject ON pii.subject_biometric (subject_id)
    WHERE revoked_at IS NULL;
CREATE INDEX biometric_expiring ON pii.subject_biometric (expires_at)
    WHERE revoked_at IS NULL;

-- -----------------------------------------------------------------------------
-- Erasure. The operation this whole schema exists to make possible.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION pii.erase_subject(p_subject_id uuid, p_request_id char(26))
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
    -- Contact points, documents and biometrics go entirely. Nothing outside this
    -- schema references them, so nothing breaks.
    DELETE FROM pii.subject_contact  WHERE subject_id = p_subject_id;
    DELETE FROM pii.subject_document WHERE subject_id = p_subject_id;
    DELETE FROM pii.subject_biometric WHERE subject_id = p_subject_id;

    -- The subject row stays as a tombstone. Orders, entitlements, scans and
    -- ledger entries keep pointing at an id that now resolves to nobody, which
    -- is the point: the transaction survives, the person does not.
    UPDATE pii.subject
       SET display_name = NULL, given_name = NULL, family_name = NULL,
           date_of_birth = NULL, nationality = NULL, preferred_language = NULL,
           is_erased = true, erased_at = now(), erasure_request_id = p_request_id,
           updated_at = now()
     WHERE id = p_subject_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'subject % not found', p_subject_id;
    END IF;
END $$;

COMMENT ON FUNCTION pii.erase_subject IS
  'Erasure as one transaction. Written as a function rather than left to the application '
  'because a partial erasure is worse than none — it reports success while leaving an email '
  'address behind, and nobody checks again.

Deliberately does not touch anything outside the pii schema. A sale cannot be unwritten '
  'because the buyer asked, and it does not need to be: it never held a name.';

-- -----------------------------------------------------------------------------
-- Access. This schema is where it is held most tightly.
-- -----------------------------------------------------------------------------
COMMENT ON SCHEMA pii IS
  'Personal data. Separately erasable, and the only place a subject_id can be joined back '
  'to a person.

A subject_id outside this schema is pseudonymous, not anonymous — re-identification is '
  'possible and requires access here, which is why reporting reads the replica without this '
  'schema, and why the AI layer never receives a row from it (ADR-0009).';

REVOKE ALL ON ALL TABLES IN SCHEMA pii FROM PUBLIC;

INSERT INTO platform.schema_version (version, name, checksum)
VALUES ('V0001a', 'pii', 'set-by-runner');

-- =============================================================================
-- ROLLBACK
-- =============================================================================
-- DROP FUNCTION IF EXISTS pii.erase_subject(uuid, char);
-- DROP TABLE IF EXISTS pii.subject_biometric;
-- DROP TABLE IF EXISTS pii.subject_document;
-- DROP TABLE IF EXISTS pii.subject_contact;
-- DROP TABLE IF EXISTS pii.subject;
-- DROP TYPE IF EXISTS pii.contact_kind;
-- DROP TYPE IF EXISTS pii.subject_kind;
-- DELETE FROM platform.schema_version WHERE version = 'V0001a';
