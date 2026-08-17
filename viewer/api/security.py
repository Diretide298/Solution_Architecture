"""Passwords, session tokens and invite tokens.

Three rules hold this together:

  A secret is never stored as it was sent. Passwords go through argon2; session
  and invite tokens are random enough that they need no stretching, but are
  stored as SHA-256 so a copy of the database cannot be replayed as a login.

  A token is compared in constant time, or by primary-key lookup on its hash,
  which is the same thing — never by scanning rows and comparing strings.

  Only this domain may hold an account, and that is checked where the invite is
  made rather than where it is redeemed.
"""

from __future__ import annotations

import hashlib
import os
import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash

_hasher = PasswordHasher()

# The only domain that may hold an account. Overridable so the harness does not
# have to own a real company mailbox to prove the rule works.
ALLOWED_DOMAIN = os.environ.get("TICVAI_DOMAIN", "softlabsgroup.com").lower()

SESSION_DAYS = 14
INVITE_DAYS = 7

# Deliberately not a full RFC 5322 parser. It rejects the shapes that are not
# addresses; the invite, not the regex, is what establishes the address is real.
_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def now() -> datetime:
    return datetime.now(timezone.utc)


def stamp(moment: Optional[datetime] = None) -> str:
    return (moment or now()).isoformat(timespec="seconds")


def parse(value: str) -> datetime:
    return datetime.fromisoformat(value)


def expired(value: str) -> bool:
    return parse(value) <= now()


# ── the domain rule ──────────────────────────────────────────────────

class DomainError(ValueError):
    """Raised when an address is malformed or outside the allowed domain."""


def check_email(email: str) -> str:
    """Returns the address, or says exactly why it cannot hold an account."""
    address = email.strip()
    if not _EMAIL.match(address):
        raise DomainError(f"{address!r} is not an email address.")
    domain = address.rsplit("@", 1)[1].lower()
    if domain != ALLOWED_DOMAIN:
        raise DomainError(
            f"Only {ALLOWED_DOMAIN} addresses can hold an account, and "
            f"{address!r} is on {domain}."
        )
    return address


# ── passwords ────────────────────────────────────────────────────────

# Short passwords are the ones that get guessed. This is the only rule, because
# composition rules ("one capital, one digit") push people towards Password1!
# and no further.
MIN_PASSWORD = 12


def check_password(password: str) -> str:
    if len(password) < MIN_PASSWORD:
        raise ValueError(f"A password needs at least {MIN_PASSWORD} characters.")
    return password


def hash_password(password: str) -> str:
    return _hasher.hash(check_password(password))


def verify_password(stored: str, offered: str) -> bool:
    try:
        _hasher.verify(stored, offered)
        return True
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False


# ── tokens ───────────────────────────────────────────────────────────

def new_token() -> str:
    """256 bits from the OS. Not guessable, so it needs no stretching."""
    return secrets.token_urlsafe(32)


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def session_expiry() -> str:
    return stamp(now() + timedelta(days=SESSION_DAYS))


def invite_expiry(days: int = INVITE_DAYS) -> str:
    return stamp(now() + timedelta(days=days))
