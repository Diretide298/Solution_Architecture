# ADR-0071: Passwords and PINs are stored as Argon2id PHC strings; a PIN also takes a Key Vault pepper

**Status:** Accepted · 14 October 2026 · Chinmay Parab (the r6 settlement of ADAM CR-078: "fix all nine, plus the class each belongs to") · **amended 3 November 2026**: the offline step-up verifier ([below](#amendment--3-november-2026-the-offline-step-up-verifier-the-one-unpeppered-pin-hash-and-why-it-is-allowed-chinmay-chg-r14v-001))
**Date:** 2026-10-14 · **Deciders:** Chinmay Parab
**Source:** ADAM CR-078 (ticket 27750, `identity.principal_credential` held only `id` and `principal_id`); change entries CHG-CRD-001 (the staff credential), CHG-CRD-002 (the tenant's PIN settings), CHG-CRD-003 (this ADR); CHG-FXC-003 (the guest credential of 4 October, which said "Argon2id, with its parameters" and had no ADR behind it)
**Related:** ADR-0004 (IdentityService issues the JWT; one session per user) · ADR-0063 (encryption and keys; Key Vault) · ADR-0047 (retention and erasure) · ADR-0055 (as amended 14 October 2026: a rule question is asked of its owner by a declared query) · audit R126 (password floor, lockout), R132 (reuse prevention), R123 (7) (a supervisor step-up is a PIN, never a password)

---

## Context

**TICVAI signs its own users in.** IdentityService checks the credential and issues the JWT (ADR-0004); a
tenant's single sign-on is optional (`identity.sso_provider`). So the package holds secrets of three kinds:
a guest's password (`identity.guest_credential`, CHG-FXC-003), a member of staff's or a partner's password,
and a member of staff's PIN for a till, a handheld or a scanner (`identity.principal_credential`, CHG-CRD-001).

**Nothing said how they are stored.** `GuestCredential.passwordHash` said "Argon2id, with its parameters"
on 4 October and no decision stood behind it; `identity.principal_credential` was two key columns until
ADAM CR-078 (14 October), so a developer building `login` had to choose an algorithm, a format, a reuse
check and a lockout alone. A PIN adds a problem a password does not have: **a 4-digit PIN has 10,000
values**, so its hash, however slow, is reversed offline in seconds by anyone who has the table. Salting
does not help when the whole space is that small.

---

## Decision

1. **Argon2id for every stored credential**: guest passwords, staff and partner passwords, staff PINs, MFA
   recovery codes and one-time codes (`identity.mfa_recovery_code`, `identity.otp_challenge`,
   `identity.mfa_challenge` where a code is sent). Parameters at r6: **memory 19 MiB (`m=19456`), 2 passes
   (`t=2`), 1 lane (`p=1`)**, a 16-byte random salt and a 32-byte tag, the OWASP baseline for Argon2id. They
   are raised in configuration, never in code, when a sign-in costs less than about 50 ms on the production
   replicas.
2. **A self-describing PHC string**, `$argon2id$v=19$m=19456,t=2,p=1$<salt>$<hash>`, in one text column
   (`credential_hash`, `password_hash`, `code_hash`). The algorithm and its parameters travel with the hash,
   so raising them never strands a row: a successful sign-in whose stored parameters are below the current
   ones re-hashes in the same transaction.
3. **A PIN is peppered as well as salted.** Before hashing, the PIN is combined with a per-tenant pepper by
   HMAC-SHA-256, and the pepper is a Key Vault secret in the tenant's region (ADR-0063), read by
   IdentityService only and never stored in the database. A stolen table without the pepper cannot be
   brute-forced offline. The pepper's version is recorded as one more PHC parameter
   (`$argon2id$v=19$m=19456,t=2,p=1,kv=<version>$...`), never the pepper itself, so a pepper is rotated by
   re-hashing at each holder's next sign-in. Passwords are not peppered: their space is large enough, and
   the pepper is what makes a short PIN safe to store at all.
4. **One current credential per principal and method, history apart.** `identity.principal_credential` holds
   the current `password` and the current `pin` (unique on principal and method); every replaced hash moves
   to `identity.principal_credential_history`. **The reuse check reads the history**: a password against the
   last `PasswordPolicy.reusePreventionCount` (audit R132), a PIN as the tenant's `pinReusePrevention` says
   (none, last 3, last 5; CHG-CRD-002). A new credential is hashed once per history row it is compared with,
   so the history is kept to the larger of the two settings and older rows are deleted.
5. **Lockout is per credential and temporary.** `failedAttempts` counts consecutive wrong attempts on the row
   (at sign-in, in `changeOwnCredential`, and as a supervisor's step-up PIN); at the tenant's threshold
   (`lockoutAfterAttempts` for a password, `pinLockoutAfterAttempts` for a PIN: 3, 5 or 10) the row is locked
   until `lockedUntil`, now plus `lockoutMinutes`. A locked credential is refused 429 `credential-locked`
   without the hash being computed, which also stops the lock being used to burn CPU. A correct credential or
   a reset clears the count. The guest password does the same on `identity.guest_credential`.
6. **The tenant chooses the PIN rule; the package fixes the storage.** PIN length (4, 6 or 8), PIN reuse and
   PIN lockout are the tenant's drop-downs in its password policy (Chinmay, 14 October 2026: "Give those as
   options that they select as a drop down"). The password floor (R126: never below 8 characters, the breach
   check) is a password rule and never applies to a PIN, which is valid only on a registered workstation.
7. **A credential is never stored as sent, logged or returned.** A request field that carries one is either
   compared and dropped (`x-ticvai-persisted: false`) or stored as its hash (`x-ticvai-stored-as` a `*_hash`
   column); `check-stored-request-fields` (SR-SECRET-UNHASHED) fails anything else.
8. **Other modules never read a credential.** A supervisor's PIN step-up in Orders, Catalogue or Inventory is
   checked by asking Identity's `verifySupervisorStepUp` query, in-process in `commerce` and over the
   serviceAuth operation from `operations` (ADR-0055, as amended for declared queries; CHG-CRD-004).

---

## Options considered

| Option | Verdict |
|---|---|
| **A. Argon2id PHC strings for all; Key Vault pepper for PINs (chosen)** | Memory-hard, parameters travel with the hash, and the pepper is what makes a 4- to 8-digit PIN survive a stolen table |
| B. bcrypt | Sound for passwords, but a 72-byte input limit, no memory hardness, and the same weakness for PINs without a pepper |
| C. PBKDF2-SHA-256 | Acceptable under FIPS; GPU-cheap, so it needs very high iteration counts for the same cost to an attacker |
| D. Encrypt PINs with a Key Vault key instead of hashing | Reversible: anyone who can call the key can read every PIN, and the database then holds secrets rather than verifiers |
| E. No pepper, rely on lockout | Lockout protects the online path only; a database copy is offline and has no lockout |

---

## Consequences

**Easier:** a developer building `login`, `changeOwnCredential`, `resetPrincipalCredential`,
`guestPasswordLogin` or the step-up check has one rule; algorithm upgrades are a configuration change; a
leaked database copy does not leak PINs.

**Harder:** a PIN check needs Key Vault reachable (the pepper is cached in IdentityService memory for the
process's life and refreshed on rotation, so a Key Vault outage does not stop sign-in); rotating a pepper
takes until each holder signs in again, and holders who never do keep a PIN that no longer verifies and are
reset (`resetPrincipalCredential`). Argon2id at 19 MiB per hash bounds concurrent sign-ins per replica; the
replica floors (ADR-0061) already size for the morning sign-in burst.

**What it asks of the package:** the storage is in the contracts (`PrincipalCredential`, `GuestCredential`,
`MfaRecoveryCode`, `OtpChallenge`, `MfaChallenge`, CHG-CRD-001 and CHG-CRD-005) and derived into the DDL;
the pepper is a Key Vault secret per tenant beside the others of ADR-0063; the prevention is
`tools/check-stored-request-fields.py`.

**A second factor's secret is not a credential hash** (R8 blocker IDENTITY-C34, CHG-R8MIG-007; r8 integration,
CHG-R8INT-024). A `totp` shared secret has to be read back to compute the expected code, and an `smsOtp` or `emailOtp`
destination has to be read to send it, so neither can be a one-way Argon2id hash: `MfaMethod.secret` and
`MfaMethod.destination` are stored encrypted with the tenant's field key (`x-ticvai-secret: field-encrypted`,
ADR-0063), write-only and never returned (`maskedTarget` is the only form of a destination a client sees). The one-time
codes themselves stay hashes under this ADR: an enrolment code is an `identity.mfa_challenge` row with `action` `enrol`
and its `codeHash`, so `identity.mfa_method` holds no code.
---

## Amendment — 3 November 2026: the offline step-up verifier, the one unpeppered PIN hash, and why it is allowed (Chinmay, CHG-R14V-001)

**Decided by Chinmay, 3 November 2026, on system review finding F-01: "Offline verifier" (the till keeps a verifier,
re-checked at sync); ADR-0013 amendment of the same date.** A till with no connection must check a supervisor's PIN
itself, and point 3 above (a PIN is peppered with a Key Vault secret the database never holds) cannot hold on a
device: the device would need the pepper. **The exception, and its limits:**

1. **The offline verifier is an Argon2id PHC string over the PIN with its own 16-byte salt and point 1's parameters,
   with no pepper.** It is a second hash of the PIN, never the PIN and never the peppered `credential_hash`.
2. **On the server it is never stored in the clear**: `identity.offline_pin_verifier.verifier_hash` is encrypted
   with the tenant's field key (`x-ticvai-secret: field-encrypted`, ADR-0063), as an MFA secret is (the section
   above), so a copy of the table without the key yields nothing, which is what point 3 protects.
3. **It is minted only where Identity has just checked the PIN** (a correct `pin` sign-in, a correct online
   step-up, a new PIN), so the PIN is never kept to mint one later; it expires 30 days after minting and stops
   counting at once when the PIN is changed, reset or locked.
4. **It reaches only a registered device of the venue** (`getOfflineStepUpPackage` under `deviceAuth`), for at most
   24 hours, held in the device's encrypted local store and replaced whole at each sync.
5. **It never decides alone**: every step-up checked offline is checked again by the server at sync against the
   peppered credential in force at the act's time (ADR-0013 amendment, point 4).

The residual risk is the one ADR-0013's amendment states: a stolen, unlocked till's verifiers can be brute-forced,
for that venue's signers, within their 24 hours. **Open: a security review of the device store and the package**
(the one CHG-R8SPN-027 named for offline sign-in), before the first venue trades offline with it.

## Amendment, 3 November 2026: a registered workstation is proven by its device credential

**Decided by Chinmay, 3 November 2026** ("All four, one release", on the r13 system review's triage; review
finding C-04; CHG-R14H-001). Point 6 says a PIN "is valid only on a registered workstation", and `login` said the
device is what bounds a PIN; but the workstation was a `workstationId` the caller typed into the body, and the
session-less supervisor step-up on the till (`listActiveSessions`, `forceLogout`) admitted a call with no credential
at all. Anyone who learned a workstation id could try PINs from the internet, list who was signed in, end sessions
and lock every supervisor's PIN at will (point 5's lockout used as denial of service).

**The workstation is proven, never named.** A device door (the till, the shared handheld, the scanner) calls with
`deviceAuth` (`contracts/shared/common.yaml`): the credential `enrolDevice` issued to the device it runs on, a
`workstationTerminal` for a till or kiosk computer and the device's own `handheldScanner` credential for a handheld.
The workstation is the one that device is bound to; a `workstationId` in the request that is not it is `403
workstation-mismatch`, and one sent without `deviceAuth` is `401 device-unauthenticated`. Both are answered before any
PIN or password is checked, so neither spends an attempt nor moves a lockout. A device-bound method (`pin`, `card`,
`rfid`) without `deviceAuth` is `400 workstation-required`. An operation that takes its workstation this way says so
with `x-ticvai-workstation-from: device`, and lists the device kinds it accepts in `x-ticvai-device-kinds`; a session-less
step-up is never admitted by `{}`. `tools/check-doors.py` (D-DEVICE-DOOR, D-DEVICE-KINDS) fails an operation that names a
workstation with no session and does not authenticate the device, or a device-reachable operation that lists no kinds.
