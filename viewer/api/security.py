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

# The three roles. A client is outside the company: it reads everything except
# the decisions and writes nothing. Kept here rather than in main.py because two
# places held the list and the second was always the one that got missed.
#
# Named `client` and not `guest` because this codebase already has a guest: the
# package's own word for a venue visitor, in `x-ticvai-audience` on 96
# operations. Two meanings for one word in one repository is a bug waiting for
# somebody to read the wrong one.
ROLES = ("admin", "reviewer", "client")
WRITERS = ("admin", "reviewer")

# A client invite is a link to an address we do not control, handed to somebody
# outside the company. A shorter window is the cheapest thing that limits what
# a forwarded or leaked link is worth.
CLIENT_INVITE_DAYS = 3

# A reset link is shorter still, and for a sharper reason than an invite. An
# invite is worth an account that does not exist yet; a reset link is worth an
# account that does — one already carrying somebody's verdicts and whatever
# their role can reach. It is made on request, used within the hour it is
# handed over, and expiring quickly is what keeps a link left in a chat log
# from being a way in a week later.
RESET_DAYS = 1

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


def check_email(email: str, role: str = "reviewer") -> str:
    """Returns the address, or says exactly why it cannot hold an account.

    The domain rule is what stops a stranger self-registering as somebody at
    this company and signing artefacts off in their name. It stays exactly as
    it was for `admin` and `reviewer`.

    A client is outside the company, so the rule cannot apply — the address is
    meant to be elsewhere. What replaces it is the invite: an admin types the
    address, the token fixes it, and whoever opens the link cannot change it.
    The person who could vouch for the address is the person who typed it.

    That reasoning only holds while a client cannot be created any other way, so
    `/api/auth/bootstrap` refuses the role and there is no self-signup path.
    """
    address = email.strip()
    if not _EMAIL.match(address):
        raise DomainError(f"{address!r} is not an email address.")
    if role == "client":
        return address
    domain = address.rsplit("@", 1)[1].lower()
    if domain != ALLOWED_DOMAIN:
        raise DomainError(
            f"Only {ALLOWED_DOMAIN} addresses can hold an account, and "
            f"{address!r} is on {domain}. An outside address can be invited "
            f"as a client, which reads but records nothing."
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


def reset_expiry(days: int = RESET_DAYS) -> str:
    return stamp(now() + timedelta(days=days))
