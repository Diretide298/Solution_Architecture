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

# The roles. Kept here rather than in main.py because two places held the list
# and the second was always the one that got missed.
#
# Named `client` and not `guest` because this codebase already has a guest: the
# package's own word for a venue visitor, in `x-ticvai-audience` on 96
# operations. Two meanings for one word in one repository is a bug waiting for
# somebody to read the wrong one.
#
# **This is not a ladder, and the sets below are not ranges of one.** It was
# three roles and it reads like a ladder — client, reviewer, admin — but a
# project manager reads everything and administers nothing while an admin does
# the opposite, and neither is "above" the other. So what a role may do is
# stated as membership of a named set, and every check asks a predicate rather
# than comparing to a string.
#
#   owner     the super admin. Everything an admin may do, plus the things that
#             are deliberately one person's: granting roles, the IP allowlist,
#             and the Build layer. Granted from the CLI only — see api/cli.py —
#             so there is no dropdown anywhere that can produce one.
#   admin     invites, resets, the registers, the bulk settles. As it was.
#   pm        delivery oversight. Reads everything an admin can read and writes
#             nothing: not a verdict, not a change request settlement.
#   lead      a team lead. Sees all activity and every change request; is
#             notified about, and acts on, the platforms in `scope`.
#   dev       a developer. Their own work.
#   reviewer  records verdicts on the package. As it was.
#   client    outside the company: reads everything except the decisions, and
#             writes nothing. As it was.
ROLES = ("owner", "admin", "pm", "lead", "dev", "reviewer", "client")

# What each role is *called*, which is not what it is stored as.
#
# `owner` is the System Architect. The stored value stays `owner` in the
# database, in `ROLES`, in every predicate above, in `audience.mjs` and in the
# CLI subcommand, because renaming it would mean migrating live account rows
# and nine checks to change a name while changing no permission — the System
# Architect has exactly the powers the owner had, which is all of them.
#
# `viewer/public/validation.js` holds the same map for the pages. Two copies
# of seven words, rather than an endpoint whose only job is to serve them.
LABELS = {
    "owner": "System Architect",
    "admin": "Admin",
    "pm": "Project Manager",
    "lead": "Team Lead",
    "dev": "Developer",
    "reviewer": "Reviewer",
    "client": "Client",
}


def label(role: str) -> str:
    """The name a person reads. Falls back to the stored value, so a role
    added to ROLES and not to LABELS appears under its own name."""
    return LABELS.get(role, role)


# Who may manage accounts, invites, resets, the exports and the bulk settles.
#
# **Every `role == "admin"` in this codebase meant this set**, back when the set
# had one member. An owner that is not in here is a super admin who can see less
# than an admin, which is the one way this change could go quietly wrong.
ADMINS = ("owner", "admin")

# Who may change the shape of the review itself: close an item, send one back,
# say that work has happened. **Not who may record a verdict** — that is
# `require_voice` in main.py and it is open to everybody including a client, on
# the argument that a reader who finds a fault and cannot say so will say it
# somewhere nobody is reading. Saying what you think is not the same act as
# declaring it dealt with, and only the second one is in here.
#
# A pm is absent because declaring work done is the thing they are overseeing. A
# client is absent because they are outside the company.
WRITERS = ("owner", "admin", "lead", "dev", "reviewer")

# Who may settle a change request — accept it, reject it, mark it done.
#
# Narrower than WRITERS by one: a dev may close a review item that names their
# own work, and does not decide whether the package itself was wrong. That is
# the lead's, and above.
#
# A pm is absent here for the reason they are absent from WRITERS, and it has to
# be said in a set rather than left to the project role: everybody internal gets
# `reviewer` on a project by default, so a check that asked only the project
# role would hand a pm the decision it is their job to watch.
SETTLERS = ("owner", "admin", "lead", "reviewer")

# Who may read the whole of the delivery rather than their own corner of it: the
# overview of every ticket, the overdue list, the registers as files, and the
# bell that says routing has failed.
#
# **This is the set a pm exists for, and it was the one the role did not have.**
# The comment above says a pm "reads everything an admin can read"; every one of
# those four paths asked `require_admin`, so what a pm actually was, in the
# store, was a reviewer who could not settle — the oversight half of the role
# was described and not wired. Separating "reads the whole thing" from
# "administers it" is the only way to have one without the other.
#
# Deliberately not a superset of anything. A lead and a dev are absent because
# their slice is the point of their role; a reviewer is absent because reading
# every ticket in the project is not what reviewing the package is.
READERS = ("owner", "admin", "pm")

# Who a platform can be handed to. A scope row for anybody else is meaningless
# rather than harmful, and refusing it early is how it stays that way.
SCOPED = ("lead", "dev")

# The one role the API will not grant. It is CLI-only, so that becoming the
# super admin takes a shell on the machine rather than a session on the site.
CLI_ONLY = ("owner",)


def is_owner(role: str) -> bool:
    return role == "owner"


def is_admin(role: str) -> bool:
    """Whether this role administers. True for an owner, which is the point."""
    return role in ADMINS


def may_write(role: str) -> bool:
    return role in WRITERS


def may_be_scoped(role: str) -> bool:
    return role in SCOPED


def may_settle(role: str) -> bool:
    return role in SETTLERS


def may_oversee(role: str) -> bool:
    """Whether this role reads the delivery whole. True for a pm, which is the point."""
    return role in READERS

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
