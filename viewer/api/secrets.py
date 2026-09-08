"""
Credentials this service holds *on behalf of* somebody, and can hand back.

Everything else secret in here is a password hash — argon2, one way, and the
point is that nobody can reverse it. This is the opposite problem. A developer's
OpenProject API token has to be usable later, as a token, so it must be stored
in a form this process can undo.

That is a real change in what the database is worth to an attacker, and it is
worth being plain about: `ticvai.db` already holds e-mail addresses and password
hashes, and it now also holds credentials to a third-party system that a thief
could use directly. Three things follow, and all three are enforced below.

**The key is not in the database.** It comes from `TICVAI_SECRET_KEY` in the
environment, so a stolen database file is ciphertext and nothing else. A copy of
the .db without the key is inert.

**A missing key is a refusal, never a fallback.** There is no "encrypt with a
default", no "store it in the clear for now". A deployment that has not set a
key cannot store a token, and says so in a sentence that names the variable.
The alternative — a hardcoded default key — is the one that ships to production
and turns encryption into decoration.

**Nothing here ever returns a token to a browser.** The API hands back a *hint*
— the last four characters — which is enough for a person to recognise which
token they pasted and useless to anybody else. Decryption happens server-side,
on the way out to OpenProject, and the plaintext does not enter a response body.

Fernet is AES-128-CBC with an HMAC-SHA256 authentication tag and a timestamp,
from `cryptography`. Chosen over rolling anything: it is authenticated, so a
tampered ciphertext raises instead of decrypting to rubbish, and it is one
import.
"""

from __future__ import annotations

import base64
import hashlib
import os
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

ENV_KEY = "TICVAI_SECRET_KEY"

# Enough that a passphrase is not trivially guessable. Not a substitute for
# generating one properly — see `describe_key` for the line that tells an
# operator how.
MIN_PASSPHRASE = 32


class NoKey(RuntimeError):
    """No usable key in the environment. Carries the sentence to show a person."""


class Unreadable(RuntimeError):
    """Ciphertext that will not open — a rotated key, or a tampered row."""


def _key() -> bytes:
    """
    The Fernet key, from the environment.

    Two accepted shapes, because an operator will produce one of them:

    A real Fernet key — 32 bytes, urlsafe-base64, what `Fernet.generate_key()`
    prints — is used as it is. Anything else long enough is treated as a
    passphrase and hashed to 32 bytes with SHA-256. The second is a convenience
    and not an endorsement: a passphrase somebody typed has far less entropy
    than 32 random bytes, which is why there is a length floor under it.
    """
    raw = (os.environ.get(ENV_KEY) or "").strip()
    if not raw:
        raise NoKey(
            f"{ENV_KEY} is not set, so this service cannot store a credential. "
            f"Generate one with:  python -c \"from cryptography.fernet import Fernet; "
            f"print(Fernet.generate_key().decode())\"  and put it in the environment "
            f"of both halves before restarting."
        )

    candidate = raw.encode("utf-8")
    try:
        # Validates length and alphabet. A 32-byte urlsafe-base64 string is a
        # key; anything else raises and falls through to the passphrase path.
        Fernet(candidate)
        return candidate
    except (ValueError, TypeError):
        pass

    if len(raw) < MIN_PASSPHRASE:
        raise NoKey(
            f"{ENV_KEY} is set but too short to use as a passphrase — "
            f"{len(raw)} characters, and {MIN_PASSPHRASE} is the floor. Either "
            f"lengthen it or, better, generate a real key with "
            f"Fernet.generate_key()."
        )
    return base64.urlsafe_b64encode(hashlib.sha256(candidate).digest())


def available() -> bool:
    """Whether a credential can be stored at all. The settings page asks this
    before offering the field, so somebody is told why rather than meeting a
    500 after typing a token in."""
    try:
        _key()
        return True
    except NoKey:
        return False


def describe_key() -> Optional[str]:
    """The sentence explaining what is missing, or None when all is well."""
    try:
        _key()
        return None
    except NoKey as exc:
        return str(exc)


def seal(plaintext: str) -> str:
    """Encrypt. Raises NoKey when the deployment has no key — deliberately
    loud, because the alternative is storing a live credential in the clear."""
    if not plaintext:
        raise ValueError("nothing to store")
    return Fernet(_key()).encrypt(plaintext.encode("utf-8")).decode("ascii")


def open_(ciphertext: str) -> str:
    """
    Decrypt, server-side only.

    An `InvalidToken` here is not corruption in the usual sense — far more often
    it is a key that was rotated or a deployment reading another's database. The
    message says so, because "invalid token" sends somebody looking at the row.
    """
    try:
        return Fernet(_key()).decrypt(ciphertext.encode("ascii")).decode("utf-8")
    except InvalidToken as exc:
        raise Unreadable(
            f"a stored credential will not decrypt with the current {ENV_KEY}. "
            f"The key has probably changed since it was saved — the owner needs "
            f"to paste the credential again."
        ) from exc


def hint(plaintext: str) -> str:
    """
    What a person is shown instead of their token: the last four characters.

    Enough to recognise which of several tokens is stored, and useless to
    anybody else. Short values are masked completely rather than half-revealed —
    the last four of a six-character secret is most of it.
    """
    text = plaintext.strip()
    if len(text) < 12:
        return "•" * 8
    return f"…{text[-4:]}"
