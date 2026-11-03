#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""What a natural person's data is, and where it is kept: the vocabulary derive-schema, derive-ddl,
derive-subject-data-register and check-personal-data share.

**Why** (r13 system review, 3 November 2026, findings B-01 and C-11; the lead, 3 November 2026: personal data "Move the
columns" into pii.*; CHG-R14M-001). ADR-0023 says personal data lives in a separate erasable store, referenced by an
opaque subject id. The module tables had grown 57 columns of names, contacts, birth dates, ID numbers and IP addresses
of their own, the contracts could not say which fields were personal, and erasure and export could not be derived. The
rule is now written once, here, as the contract marks it:

  * `x-ticvai-data-class: personal` on a property: the field is a natural person's data. A response that carries it
    is answered under the PII permission (`GUEST_VIEW_PII`), or the operation declares `x-ticvai-personal-data`
    (`gated`: null to a caller without GUEST_VIEW_PII; `self`: the caller's own record). The subject-data export
    includes it and erasure removes it. `business` marks a field of the same name that is an organisation's (a
    sender number, a store account's legal entity); `behavioural` is CR-141's class for what a guest did.
  * `x-ticvai-pii: {store: <store>, subject: <property>}` on a property of a schema persisted outside pii.*: the value
    is kept in pii.* for the subject the named property holds (a uuid property referencing pii.subject, default
    `subjectId`), never as a column of the module's table. derive-schema gives it no column; derive-ddl retires the
    column the databases still hold and writes the copy for the migration owner (migration-review.md). The module
    writes it through Identity's `recordSubjectDetails` and reads it through Identity's subject queries.
  * `x-ticvai-subject-kind: guest|employee|contact|applicant` on that subject property: the kind of the pii.subject
    a row with no subject gets when its value is first written (and when the forward migration backfills it).
"""
from __future__ import annotations

import re

# store -> (pii table, column, contact kind or None)
STORES = {
    "subject.displayName": ("pii.subject", "display_name", None),
    "subject.givenName": ("pii.subject", "given_name", None),
    "subject.familyName": ("pii.subject", "family_name", None),
    "subject.dateOfBirth": ("pii.subject", "date_of_birth", None),
    "subject.nationality": ("pii.subject", "nationality", None),
    "subject.preferredLanguage": ("pii.subject", "preferred_language", None),
    "contact.email": ("pii.subject_contact", "value", "email"),
    "contact.phone": ("pii.subject_contact", "value", "phone"),
    "contact.mobile": ("pii.subject_contact", "value", "mobile"),
    # an email or a number, whichever the guest gave: the contact's kind is read from the value at the write
    "contact.point": ("pii.subject_contact", "value", "email or mobile, from the value"),
    "document.number": ("pii.subject_document", "number_ciphertext", None),
    "identifier.ipAddress": ("pii.subject_network_identifier", "ip_address", None),
}
SUBJECT_KINDS = ("guest", "employee", "contact", "applicant")
DATA_CLASSES = ("personal", "behavioural", "business")
# The permissions under which a response may carry a personal field without declaring x-ticvai-personal-data.
PII_PERMISSIONS = ("GUEST_VIEW_PII", "REPORT_EXPORT_PII", "BIOMETRIC_IMAGE_VIEW")
PERSONAL_DATA_MODES = ("gated", "self")
PII_SCHEMA = "pii"

# **A natural person's identifier, by column name** (the review's B-01 scan, a7_pii.py, less what it caught by accident:
# `face_value`, `*_fingerprint` and the biometric configuration columns are not a person's data, and biometrics live
# in pii.subject_biometric by ADR-0063; plus the person-name roles found on the same rows: signatory, signed, guardian,
# subject and person names, an emergency contact, a contact point). `display_name` is not here: on most tables it is
# a configuration label. `buyer_name` is not here either: it sits on the ledger's tax documents, whose retention is
# the law's (the lead's item, CHG-R14M-001 notes).
COLUMN = re.compile(
    r"(^|_)(email|e_mail|phone|mobile|msisdn|first_name|last_name|full_name|given_name|family_name|surname|"
    r"date_of_birth|dob|birth_date|passport|passport_number|national_id|emirates_id|id_number|document_number|"
    r"home_address|address_line|postcode|postal_code|holder_name|guest_name|customer_name|contact_name|"
    r"recipient_name|ip_address|nationality|signatory_name|signed_name|signer_name|guardian_name|subject_name|"
    r"person_name|emergency_contact|contact_point)(_|$)")
NOT_A_VALUE = re.compile(r"(_id|_ids|_hash|_ref|_blind|_masked|_last4|_verified|_count|_required|_enabled|_policy|"
                         r"_mode|_type|_kind|_at|_on|_ciphertext|_claim|_channel)$")
NOT_A_VALUE_PREFIX = ("is_", "has_", "requires_", "allow", "prefers_", "records_")

# **The same, by property name** (the review's a14 list, and the role names above in camelCase).
PROPERTY = re.compile(
    r"^(email|emailAddress|phone|phoneNumber|mobile|mobileNumber|dateOfBirth|birthDate|passportNumber|nationalId|"
    r"emiratesId|idNumber|documentNumber|homeAddress|address|fullName|firstName|lastName|holderName|guestName|"
    r"customerName|contactName|contactEmail|contactPhone|recipientEmail|recipientName|ipAddress|nationality|"
    r"signatoryName|signedName|signerName|guardianName|subjectName|personName|emergencyContact|contactPoint)$")


def is_identifier_column(name: str) -> bool:
    """A column name that holds a natural person's identifier (not a key, flag, hash or timestamp about one)."""
    n = str(name)
    return bool(COLUMN.search(n)) and not NOT_A_VALUE.search(n) and not n.startswith(NOT_A_VALUE_PREFIX)


def is_identifier_property(name: str) -> bool:
    return bool(PROPERTY.match(str(name)))


def pii_mark(spec) -> dict | None:
    """The property's `x-ticvai-pii` as {store, subject}, or None."""
    if not isinstance(spec, dict):
        return None
    m = spec.get("x-ticvai-pii")
    if isinstance(m, str):
        m = {"store": m}
    if not isinstance(m, dict) or not m.get("store"):
        return None
    return {"store": str(m["store"]), "subject": str(m.get("subject") or "subjectId")}


def data_class(spec) -> str | None:
    return spec.get("x-ticvai-data-class") if isinstance(spec, dict) else None


def copy_steps(table: str, column: str, store: str, subject_column: str, kind: str | None) -> str:
    """What the forward migration does for one moved column, in the order it does it (for migration-review.md)."""
    pt, pc, ck = STORES.get(store, ("pii.?", "?", None))
    k = kind or "guest"
    steps = [
        f"1. add `{table}.{subject_column}` (uuid, a pii.subject id) where the table lacks it (the additive forward "
        "migration does)",
        f"2. backfill: for each row with `{subject_column}` null that holds this or any other field kept for "
        f"`{subject_column}`, insert one `pii.subject` (kind `{k}`, a new UUIDv7, is_erased false, created_at now) and "
        f"set `{subject_column}` to it, once per row for all of that subject's columns",
    ]
    if pt == "pii.subject":
        steps.append(f"3. copy: `UPDATE pii.subject s SET {pc} = coalesce(s.{pc}, x.{column})` from `{table} x` on "
                     f"`s.id = x.{subject_column}` (a value the subject already holds is kept)")
    elif pt == "pii.subject_contact":
        kd = ck if ck in ("email", "phone", "mobile") else "email where the value holds '@', else mobile"
        steps.append(f"3. copy: insert a `pii.subject_contact` (kind {kd}, value, value_normalised, value_hash, "
                     f"is_primary false, is_verified false) for each row's `{column}` against `{subject_column}`, "
                     "skipping a contact the subject already holds (same kind and value_hash)")
    elif pt == "pii.subject_document":
        steps.append(f"3. copy: insert a `pii.subject_document` (kind `other` unless the row says, number_ciphertext "
                     f"encrypted by the application under the tenant's data key, ADR-0063 section 5, number_last4) "
                     f"for each row's `{column}`: run by the application's one-off job, never in SQL, since the "
                     "key is the application's")
    else:
        steps.append(f"3. copy: insert a `pii.subject_network_identifier` (subject_id, source_table `{table}`, "
                     f"source_id the row's id, ip_address, captured_at the row's time) for each row's `{column}`")
    steps.append(f"4. drop: the four-step drop of `{table}.{column}` (its NOT NULL now, stop every read and write, "
                 "then DROP COLUMN in a later forward migration once the copy is verified by count)")
    return "; ".join(steps)
