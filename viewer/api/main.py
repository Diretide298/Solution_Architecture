"""The stateful half of the viewer.

The Node server serves the delivery package: contracts, schemas, boards, the
lineage. It reads, and it holds nothing. This service holds the things a person
*writes* — who they are, and what they decided about an artefact — and nothing
else. The split is deliberate: the readers are five thousand lines of working,
tested code, and rewriting them in Python would buy nothing.

    uvicorn api.main:app --port 8787        (from viewer/)

Port 8787, not 8000: on Windows 8000 falls inside a reserved range and
binding it fails with Errno 10013.
"""

from __future__ import annotations

import base64
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import date, timedelta
from typing import List, Optional

from fastapi import (
    Cookie, Depends, FastAPI, File, Form, HTTPException, Query, Response,
    Request, UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import db, decisions, openproject, secrets, security

app = FastAPI(
    title="TICVAI viewer — accounts and validation",
    version="1.0.0",
    description=__doc__,
)

# On a workstation the viewer is served by the Node process on another port, so
# the browser treats calls here as cross-origin. Credentials must be allowed for
# the session cookie to be sent at all, and allowing credentials rules out "*".
#
# The deployment gives the two halves their own names, so the call from the
# reading server to here is cross-origin and its origin has to be named. It is
# named here rather than left to TICVAI_ORIGINS so that a deploy that forgets an
# environment variable still signs people in; the variable stays for any further
# name — a staging host, a second front end — without a code change.
#
# It is never "*". Two reasons, and the first one alone settles it: a browser
# refuses a credentialed response that answers "*", so every call here would
# fail exactly the way a rejected origin does. The second is that if it did work
# it would let any site on the internet read this one using the visitor's own
# session.
_extra = [o.strip() for o in os.environ.get("TICVAI_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4173", "http://127.0.0.1:4173",
        "http://localhost:8787", "http://127.0.0.1:8787",
        # Two spellings of the same front end. The product is Adam, but
        # aster.ainfinite.ai is a live name with a certificate against it,
        # so it stays until DNS and certbot have caught up; both are named
        # here meanwhile. See viewer/handoff/adam-rename-todo.md.
        "https://aster.ainfinite.ai",
        "https://adam.ainfinite.ai",
    ] + _extra,
    allow_credentials=True,
    # PUT is here for the two settings routes. Without it the preflight answers
    # 400 and saving a token or a git identity fails from the deployed page only:
    # same-origin callers (the viewer's proxy, the checks) never send a preflight.
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
    # A cross-origin fetch can read almost none of the response headers unless
    # they are named here — the browser hides the rest even from a call that
    # succeeded. These two are the export's answer about itself: the filename it
    # decided on, and how many rows it found. Without them the page would have to
    # invent its own name for the file, which is how the name on disk and the
    # name in Content-Disposition start disagreeing, and would have to count rows
    # by splitting the CSV on newlines — which is wrong the first time somebody
    # puts a line break in a note.
    expose_headers=["Content-Disposition", "X-Ticvai-Rows"],
)

SESSION_COOKIE = "ticvai_session"

# Who the session cookie belongs to.
#
# Unset on a workstation and in the one-origin deployment: the cookie is
# host-only, which is the tighter default and all either arrangement needs.
#
# It is required the moment the two halves are on different names — the reading
# server on adam.example.com and this service on adamapi.example.com. The
# browser sends a host-only cookie set by adamapi back to adamapi and nowhere
# else, so the node gate, which reads the same cookie off its own requests to
# decide who is asking, would never see one and would bounce every page to the
# sign-in door in a loop. TICVAI_COOKIE_DOMAIN=.example.com is what makes one
# cookie visible to both names.
#
# It must be the shared parent of the two, and no higher: a cookie scoped to a
# domain is sent to every host under it.
COOKIE_DOMAIN = os.environ.get("TICVAI_COOKIE_DOMAIN") or None
# What a *review* can say. Three values: this is somebody judging an artefact.
VERDICTS = ("approved", "rejected", "needs-work")

# How the team answered one — the tracker's "Our verdict" column, kept apart
# from the reviewer's because they are two different statements. "Needs work"
# answered by "Built" is a complete exchange; two verdicts in a row is an
# argument. Recorded when an item is closed, so closing says how and not only
# that it happened.
RESPONSES = ("built", "wired", "answered", "accepted", "approved-no-action")

# The two verdicts that put work in a queue. Everything else is a resolution.
ASKS_FOR_WORK = ("needs-work", "rejected")
TARGET_KINDS = ("operation", "table", "screen", "board", "module", "state", "schema")

# Which layer a verdict was given from. Recorded so the review can be read by
# layer — how much of the frontend has been signed off against how much of the
# backend — which the kind alone answers only while one kind means one layer.
LAYERS = ("frontend", "contracts", "domain", "backend", "modules", "decisions")

# Which side of the house the work lands on. Two values and deliberately only
# two: the question it answers is "whose queue is this in", and a list long
# enough to describe every nuance is a list nobody filters by.
TAGS = ("frontend", "backend")

# What each of those values is *called* in a file somebody opens in Excel.
#
# These are the same words the browser's own export writes, and they are spelled
# out again here for the same reason the vocabulary above is spelled out again in
# validation.js: each half of the viewer holds its own copy of what a value is
# called, because the alternative is a network call in front of a column heading.
#
# The two exports have to read the same. A reader who takes the review activity
# off the reviews page one week and off the admin panel the next must get a file
# that pivots the same way, and "Needs work" in one against "needs-work" in the
# other is two files that will not stack. A change here is a change in
# reviews.js, and the other way round.
KIND_LABEL = {
    "operation": "APIs", "table": "Tables", "screen": "Wireframes",
    "board": "Boards", "module": "Modules",
    "state": "State models", "schema": "Schemas",
}
LAYER_LABEL = {
    "frontend": "Frontend", "contracts": "Contracts", "domain": "Domain",
    "backend": "Backend", "modules": "Modules", "decisions": "Decisions",
}
TAG_LABEL = {"frontend": "Frontend", "backend": "Backend"}
AUDIENCE_LABEL = {"internal": "The team", "client": "Client"}
VERDICT_LABEL = {
    "approved": "Approved", "needs-work": "Needs work", "rejected": "Rejected",
}
RESPONSE_LABEL = {
    "built": "Built", "wired": "Wired", "answered": "Answered",
    "accepted": "Accepted", "approved-no-action": "Approved — no action",
}
# Where a change request stands, as a file opened in Excel spells it. Here with
# the other label maps rather than beside CHANGE_STATUSES, because this is the
# same kind of thing they are — the export's spelling of a stored value — and
# the import reads both spellings of each, exactly as _RESPONSE_OF does.
#
# "Accepted" is also a RESPONSE_LABEL. The two never meet: one is what a
# reviewer's verdict was answered with, the other is where a change request got
# to, and they are in different files with different columns.
CHANGE_STATUS_LABEL = {
    "open": "Open", "accepted": "Accepted",
    "rejected": "Rejected", "done": "Done",
}


@app.on_event("startup")
def _startup() -> None:
    db.init()


# ── shapes ───────────────────────────────────────────────────────────

class Credentials(BaseModel):
    email: str
    password: str


class PasswordReset(BaseModel):
    token: str
    password: str


class Redemption(BaseModel):
    token: str
    name: str = ""
    password: str


class InviteRequest(BaseModel):
    email: str
    role: str = "reviewer"
    days: int = Field(default=security.INVITE_DAYS, ge=1, le=90)
    # The ADAM project the link opens. Blank is the first project, which is
    # what every invite meant before there was a choice.
    project_id: str = ""


class Bootstrap(BaseModel):
    email: str
    name: str = ""
    password: str


class PasswordChange(BaseModel):
    current: str
    replacement: str


class VerdictIn(BaseModel):
    target_kind: str
    target_id: str
    verdict: str
    note: str = ""
    # Optional: an older client does not send it, and the kind says what it
    # would have been.
    layer: str = ""
    # Which side has to act. Chosen in the interface; defaulted from the kind
    # when a caller says nothing.
    tag: str = ""


class Account(BaseModel):
    id: int
    email: str
    name: str
    role: str


class VerdictOut(BaseModel):
    id: int
    target_kind: str
    target_id: str
    layer: str = ""
    tag: str = ""
    audience: str = "internal"
    verdict: str
    note: str
    by: str
    by_email: str
    at: str
    # Null until somebody marks it complete. Both fields or neither.
    done_at: Optional[str] = None
    done_by_name: Optional[str] = None
    done_response: str = ""
    # Set when an admin did not accept the completion. Whether the row counts
    # as done is decided by which of the two timestamps is later.
    sent_back_at: Optional[str] = None
    sent_back_by_name: Optional[str] = None
    sent_back_note: str = ""


class DoneIn(BaseModel):
    done: bool = True
    # How it was answered. Required when closing, meaningless when reopening.
    response: str = ""


class SendBackIn(BaseModel):
    note: str = ""


# ── who is asking ────────────────────────────────────────────────────

def current_account(
    ticvai_session: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE),
) -> Optional[dict]:
    """The signed-in account, or None. Looked up by the hash of the token, so
    an expired or forged cookie simply finds nothing."""
    if not ticvai_session:
        return None
    row = db.one(
        """SELECT s.expires_at, a.id, a.email, a.name, a.role, a.active
             FROM session s JOIN account a ON a.id = s.account_id
            WHERE s.token_hash = ?""",
        (security.token_hash(ticvai_session),),
    )
    if not row or not row["active"] or security.expired(row["expires_at"]):
        return None
    return dict(row)


def require_account(account: Optional[dict] = Depends(current_account)) -> dict:
    if not account:
        raise HTTPException(401, "Sign in to do that.")
    return account


def require_admin(account: dict = Depends(require_account)) -> dict:
    """Anyone who administers: an admin, or the owner above them.

    `security.is_admin` rather than `role == "admin"`, and that is the whole of
    why the predicate exists. Every one of these checks was a string comparison
    while "administers" had exactly one spelling; the moment it had two, each
    one left over would have refused the super admin something an admin can do.
    """
    if not security.is_admin(account["role"]):
        raise HTTPException(403, "Only an admin can do that.")
    return account


def require_owner(account: dict = Depends(require_account)) -> dict:
    """The super admin, and nobody else — not even an admin.

    For the things that are deliberately one person's rather than the
    administrators': granting roles, the IP allowlist, and the Build layer. The
    role cannot be reached through this API at all (see set_role below), so what
    this gates is reachable only by somebody who has had a shell on the machine.
    """
    if not security.is_owner(account["role"]):
        raise HTTPException(
            403, "Only the super admin can do that.")
    return account


def require_reader(account: dict = Depends(require_account)) -> dict:
    """Anyone who reads the delivery whole: an administrator, or a pm.

    **Distinct from require_admin, and the distinction is the pm's whole job.**
    These are the paths that answer "how is the delivery going" rather than
    "who has an account" — the overview of every ticket, the requests nobody has
    taken on, the registers as a file. Asking require_admin on them meant a
    project manager, whose role exists to watch exactly that, was refused all
    four and left with a reviewer's view of one package.

    It gates reading and nothing else. Every write on the same objects still
    asks require_admin or narrower, so a pm sees the whole picture and changes
    no part of it, which is the shape the role was described as having.
    """
    if not security.may_oversee(account["role"]):
        raise HTTPException(403, "Only an admin or a project manager can do that.")
    return account


def require_writer(account: dict = Depends(require_account)) -> dict:
    """Anyone who may act on the team's behalf — admin or reviewer, never a
    client.

    This is what a client still may not do: change the shape of the review
    itself. Closing an item, and anything else that says work has happened, is
    the team's own record of its own queue. Recording a verdict is no longer on
    this list — see require_voice — but everything else that writes still is.

    Hiding a control in the browser is presentation; a hidden button is still a
    POST away for anyone who opens devtools. The rule has to be here or it is
    not a rule.
    """
    if account["role"] not in security.WRITERS:
        raise HTTPException(
            403, "A client account can read the package but cannot do that.")
    return account


def require_voice(account: dict = Depends(require_account)) -> dict:
    """Anyone who may say what they think of an artefact — everybody, client
    included.

    A client reviewing what was built for them is the point of showing it to
    them, and a reader who can find a fault and has no way to say so will say
    it somewhere nobody is reading. What keeps that safe is not refusing the
    write but separating it: see `audience_of`.
    """
    return account


def audience_of(account: dict) -> str:
    """Which review a verdict belongs to, from who is writing it.

    Derived here and never accepted from the request. A caller who could name
    their own audience could file a client's approval as the team's, which is
    the only thing about this that would actually matter.
    """
    return "client" if account["role"] == "client" else "internal"


# ── accounts ─────────────────────────────────────────────────────────

def projects_for(account: dict) -> list:
    """Which packages this account may read, and as what.

    The role here is the *project's* role and not the account's. The same person
    can be a reviewer on one package and a client on another \u2014 that is what
    `account_project` is for \u2014 and reading `account.role` for a package would
    make the table decorative.

    An administrator gets every active project. They register projects and they
    issue grants, so refusing them a package they added a minute ago would be a
    lockout with the key in the same pocket. Everybody else needs a row, and a
    missing row is no access: there is no default that has to be remembered and
    turned off.
    """
    if security.is_admin(account["role"]):
        return [
            {"id": row["id"], "role": "reviewer"}
            for row in db.all_rows(
                "SELECT id FROM project WHERE active = 1 ORDER BY id")
        ]
    return [
        {"id": row["project_id"], "role": row["role"]}
        for row in db.all_rows(
            "SELECT ap.project_id, ap.role FROM account_project ap "
            "JOIN project p ON p.id = ap.project_id "
            "WHERE ap.account_id = ? AND p.active = 1 ORDER BY ap.project_id",
            (account["id"],),
        )
    ]


@app.get("/api/auth/me")
def me(account: Optional[dict] = Depends(current_account)):
    """Who the caller is. Answers rather than refuses when nobody is signed in,
    so the viewer can ask on load without treating 401 as an error."""
    if not account:
        return {"signedIn": False}
    return {
        "signedIn": True,
        "account": Account(
            id=account["id"], email=account["email"],
            name=account["name"], role=account["role"],
        ),
        # Which packages, and as what. The reading server refuses a project that
        # is not on this list, so it is the whole of the access check rather than
        # a hint for drawing a menu.
        "projects": projects_for(account),
    }


def _account_count() -> int:
    return db.one("SELECT COUNT(*) AS n FROM account")["n"]


@app.get("/api/auth/state")
def auth_state(account: Optional[dict] = Depends(current_account)):
    """What the sign-in page needs before it can draw itself: whether anyone
    holds an account yet, and whether this caller is one of them."""
    return {
        "signedIn": bool(account),
        "needsBootstrap": _account_count() == 0,
        "domain": security.ALLOWED_DOMAIN,
        "account": None if not account else Account(
            id=account["id"], email=account["email"],
            name=account["name"], role=account["role"],
        ),
    }


@app.post("/api/auth/bootstrap")
def bootstrap(body: Bootstrap, response: Response, request: Request):
    """Creates the first account, as an admin.

    Open only while no account exists. That is the whole guard, and it is
    enough: the moment this succeeds the door closes behind it, and everyone
    after comes in by invitation. It exists so the first password is chosen by
    the person who will use it, rather than generated by someone else and sent
    to them.
    """
    if _account_count() > 0:
        raise HTTPException(409, "An account already exists. Ask an admin for an invite.")
    try:
        email = security.check_email(body.email)
        security.check_password(body.password)
    except (security.DomainError, ValueError) as exc:
        raise HTTPException(400, str(exc))

    account_id = db.write(
        """INSERT INTO account (email, email_folded, name, password_hash, role, created_at)
           VALUES (?, ?, ?, ?, 'admin', ?)""",
        (email, db.fold(email), body.name.strip(),
         security.hash_password(body.password), security.stamp()),
    )
    token = security.new_token()
    db.write(
        """INSERT INTO session (token_hash, account_id, created_at, expires_at, user_agent)
           VALUES (?, ?, ?, ?, ?)""",
        (security.token_hash(token), account_id, security.stamp(),
         security.session_expiry(), request.headers.get("user-agent", "")[:200]),
    )
    _set_session_cookie(response, token)
    return {"ok": True, "email": email, "role": "admin"}


@app.post("/api/auth/login")
def login(body: Credentials, response: Response, request: Request):
    row = db.one(
        "SELECT id, password_hash, active FROM account WHERE email_folded = ?",
        (db.fold(body.email),),
    )
    # One message for both "no such account" and "wrong password". Telling them
    # apart hands an attacker a list of who holds an account.
    if not row or not security.verify_password(row["password_hash"], body.password):
        raise HTTPException(401, "That email and password do not match.")
    if not row["active"]:
        raise HTTPException(403, "That account has been disabled.")

    token = security.new_token()
    db.write(
        """INSERT INTO session (token_hash, account_id, created_at, expires_at, user_agent)
           VALUES (?, ?, ?, ?, ?)""",
        (
            security.token_hash(token), row["id"], security.stamp(),
            security.session_expiry(), request.headers.get("user-agent", "")[:200],
        ),
    )
    db.write("UPDATE account SET last_seen_at = ? WHERE id = ?",
             (security.stamp(), row["id"]))
    _set_session_cookie(response, token)
    return {"ok": True}


@app.post("/api/auth/logout")
def logout(
    response: Response,
    ticvai_session: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE),
):
    if ticvai_session:
        db.write("DELETE FROM session WHERE token_hash = ?",
                 (security.token_hash(ticvai_session),))
    # Domain and path have to match the ones it was set with, or the browser
    # keeps the cookie and signing out leaves a live one behind.
    response.delete_cookie(SESSION_COOKIE, path="/", domain=COOKIE_DOMAIN)
    return {"ok": True}


@app.post("/api/auth/logout-all")
def logout_all(
    response: Response,
    account: dict = Depends(require_account),
):
    """Drop every session this account holds, on every device.

    Sessions are the only thing touched. Verdicts, invites and the account row
    itself are untouched, so this costs nothing but a sign-in — which is what
    makes it safe to reach for on a shared machine or a lost laptop, where the
    alternative is deactivating the account and losing the audit trail's author.

    Deliberately not admin-gated: the person best placed to know a session has
    escaped is the person it belongs to, and making them ask an admin first is
    how a stolen cookie stays live overnight. An admin revoking *somebody
    else's* sessions is the separate route below.
    """
    dropped = db.change("DELETE FROM session WHERE account_id = ?", (account["id"],))
    # Including the caller's own. Signing out everywhere and staying signed in
    # here would mean the one device you are holding is the one you cannot
    # clear — and that is usually the point of pressing it.
    # Domain and path have to match the ones it was set with, or the browser
    # keeps the cookie and signing out leaves a live one behind.
    response.delete_cookie(SESSION_COOKIE, path="/", domain=COOKIE_DOMAIN)
    return {"ok": True, "dropped": dropped}


@app.post("/api/accounts/{account_id}/logout-all")
def logout_account(account_id: int, admin: dict = Depends(require_admin)):
    """The same, done to somebody else. Admin only.

    The honest tool for "that person has left" or "that laptop is gone": it ends
    their sessions without disabling the account, so every verdict they recorded
    keeps its author and the register still reads correctly.
    """
    if not db.one("SELECT id FROM account WHERE id = ?", (account_id,)):
        raise HTTPException(404, "No such account.")
    dropped = db.change("DELETE FROM session WHERE account_id = ?", (account_id,))
    return {"ok": True, "dropped": dropped}


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        SESSION_COOKIE, token,
        max_age=security.SESSION_DAYS * 24 * 3600,
        httponly=True,   # script cannot read it, so an injection cannot steal it
        samesite="lax",
        path="/",
        # Host-only unless the two halves are on different names under one
        # parent, where both have to see it. "lax" survives that: sibling
        # subdomains are the same *site*, and it is cross-site that lax stops.
        domain=COOKIE_DOMAIN,
        # The viewer runs over http on a workstation. Setting Secure here would
        # stop the cookie being sent at all. Set TICVAI_SECURE_COOKIE=1 when
        # this is ever served over https.
        secure=bool(os.environ.get("TICVAI_SECURE_COOKIE")),
    )


# ── managing accounts ────────────────────────────────────────────────

@app.get("/api/accounts")
def list_accounts(admin: dict = Depends(require_admin)):
    rows = db.all_rows(
        """SELECT a.id, a.email, a.name, a.role, a.active, a.created_at, a.last_seen_at,
                  (SELECT COUNT(*) FROM verdict v WHERE v.account_id = a.id) AS verdicts
             FROM account a ORDER BY a.id"""
    )
    return {"accounts": [dict(r) for r in rows]}


@app.post("/api/accounts/{account_id}/active")
def set_active(account_id: int, active: bool, admin: dict = Depends(require_admin)):
    """Disables or re-enables an account.

    Disabling rather than deleting, because a verdict points at the person who
    gave it. Deleting the account would either orphan the verdict or take it
    with them, and both lose something worth keeping.
    """
    row = db.one("SELECT id, role, active FROM account WHERE id = ?", (account_id,))
    if not row:
        raise HTTPException(404, "No such account.")
    if account_id == admin["id"]:
        raise HTTPException(409, "You cannot disable your own account.")
    if security.is_owner(row["role"]):
        # The owner is not disableable from here for the same reason the role is
        # not grantable from here: the super admin is arranged on the machine, so
        # that a session on the site is never enough to remove one.
        raise HTTPException(
            409, "The super admin cannot be disabled from here. Use the CLI.")
    if not active and security.is_admin(row["role"]) and _live_admin_count() <= 1:
        raise HTTPException(409, "That is the last active admin. Make another first.")

    db.write("UPDATE account SET active = ? WHERE id = ?", (1 if active else 0, account_id))
    if not active:
        # A disabled account must stop being signed in, not merely stop being
        # able to sign in again.
        db.write("DELETE FROM session WHERE account_id = ?", (account_id,))
    return {"ok": True, "active": active}


@app.post("/api/accounts/{account_id}/role")
def set_role(account_id: int, role: str, admin: dict = Depends(require_admin)):
    """Move an account between roles. Every role but one.

    `owner` is refused in both directions — it cannot be granted here and it
    cannot be taken away here — and that is the point of it: becoming or
    unmaking the super admin takes a shell on the machine, so no session, no
    stolen cookie and no mistake on this page can produce one.
    """
    if role not in security.ROLES:
        raise HTTPException(400, f"A role is one of {', '.join(security.ROLES)}.")
    if role in security.CLI_ONLY:
        raise HTTPException(
            403, f"{role!r} is not granted from here. It is set on the machine, "
                 f"with `python -m api.cli owner <address>`.")
    row = db.one("SELECT id, role FROM account WHERE id = ?", (account_id,))
    if not row:
        raise HTTPException(404, "No such account.")
    if row["role"] in security.CLI_ONLY:
        raise HTTPException(
            403, "The super admin's role is not changed from here. Use the CLI.")
    # "Your own administration" rather than "your own admin role": an owner
    # demoting themselves to reviewer is the same lockout by another name, and
    # the check that named one role would have missed it.
    if account_id == admin["id"] and not security.is_admin(role):
        raise HTTPException(409, "You cannot take administration away from yourself.")
    if (security.is_admin(row["role"]) and not security.is_admin(role)
            and _live_admin_count() <= 1):
        raise HTTPException(409, "That is the last admin.")
    db.write("UPDATE account SET role = ? WHERE id = ?", (role, account_id))
    return {"ok": True, "role": role}


def _live_admin_count() -> int:
    """How many accounts can still administer. **Owners included** — they can do
    everything an admin can, so a store with one owner and one admin does not
    become adminless when the admin is demoted, and saying it did would block a
    change that is perfectly safe."""
    holes = ",".join("?" * len(security.ADMINS))
    return db.one(
        f"SELECT COUNT(*) AS n FROM account WHERE role IN ({holes}) AND active = 1",
        security.ADMINS)["n"]


# ── who owns which slice ─────────────────────────────────────────────
#
# "Super admin assigns team lead a platform", as routes. The table is `scope` in
# db.py, and the reasoning about what it is for — and what it is deliberately
# not for — is there rather than repeated here.
#
# **Reading is an administrator's; writing is the owner's alone.** An admin
# needs to see who owns what to do their job; changing it is how work gets
# routed and who gets paged, so it is arranged by one person on purpose.


class ScopeIn(BaseModel):
    project_id: str = ""
    tag: str
    # Absent or empty means the whole of that side. Kept tellable from a named
    # platform all the way down to the column, because "owns frontend" and "owns
    # P01" are different grants and a lead may hold both.
    platform: str = Field(default="", max_length=20)


# A platform code as the package writes it: P01, P04. **This service cannot
# check that the platform exists** — the packages live on the node side, which
# is the half that reads them, and teaching this one to open them would be a
# second reader of the same files. So the shape is checked and the existence is
# not, and a typo shows up as a scope that matches nothing rather than as a
# refusal. The page offers a list, which is where the real answer comes from.
_PLATFORM = re.compile(r"^P\d{2,3}$")


def _scope_row(row) -> dict:
    return {
        "id": row["id"],
        "project": row["project_id"],
        "tag": row["tag"],
        "platform": row["platform"],
        # What it says out loud, built here so the page and any report agree.
        "says": f"{TAG_LABEL.get(row['tag'], row['tag'])}"
                + (f" · {row['platform']}" if row["platform"] else " · all platforms"),
        "grantedAt": row["granted_at"],
        "grantedBy": row["granted_by_name"] or row["granted_by_email"],
    }


_SCOPE_SELECT = (
    "SELECT s.*, g.name AS granted_by_name, g.email AS granted_by_email "
    "FROM scope s JOIN account g ON g.id = s.granted_by"
)


@app.get("/api/accounts/{account_id}/scopes")
def list_scopes(account_id: int, admin: dict = Depends(require_admin)):
    """Which slices this account owns. An administrator may read it."""
    if not db.one("SELECT id FROM account WHERE id = ?", (account_id,)):
        raise HTTPException(404, "No such account.")
    rows = db.all_rows(
        _SCOPE_SELECT + " WHERE s.account_id = ? ORDER BY s.project_id, s.tag, s.platform",
        (account_id,))
    return {"scopes": [_scope_row(r) for r in rows]}


@app.get("/api/scopes")
def every_scope(project_id: str = Query(default=""),
                admin: dict = Depends(require_admin)):
    """Every grant on a project, so "who owns P04" is one call rather than one
    per account. An administrator may read it."""
    project = _readable_project(admin, project_id)
    rows = db.all_rows(
        _SCOPE_SELECT + " WHERE s.project_id = ? ORDER BY s.tag, s.platform, s.id",
        (project,))
    out = []
    for row in rows:
        who = db.one("SELECT name, email, role FROM account WHERE id = ?",
                     (row["account_id"],))
        out.append({**_scope_row(row), "account": {
            "id": row["account_id"],
            "name": who["name"] if who else "",
            "email": who["email"] if who else "",
            "role": who["role"] if who else "",
        }})
    return {"project": project, "scopes": out}


@app.post("/api/accounts/{account_id}/scopes")
def grant_scope(account_id: int, body: ScopeIn, owner: dict = Depends(require_owner)):
    """Hand somebody a slice of a project. The super admin, and nobody else.

    Refused for a role that cannot hold one. A scope row on an admin is not
    dangerous — nothing reads it for them, because they are whole rather than
    scoped — but it is a second, narrower answer to a question already answered,
    and the person who wrote it would reasonably expect it to mean something.
    """
    row = db.one("SELECT id, role, active FROM account WHERE id = ?", (account_id,))
    if not row:
        raise HTTPException(404, "No such account.")
    if not security.may_be_scoped(row["role"]):
        raise HTTPException(
            409, f"{'An' if row['role'][0] in 'aeiou' else 'A'} {row['role']} "
                 f"is not scoped to a platform. "
                 f"{' or a '.join(security.SCOPED)} can hold one; an owner, an admin "
                 f"and a pm already see the whole project.")

    project = _readable_project(owner, body.project_id)
    tag = body.tag.strip().lower()
    if tag not in TAGS:
        raise HTTPException(400, f"tag is one of {', '.join(TAGS)}.")
    platform = body.platform.strip().upper()
    if platform and not _PLATFORM.match(platform):
        raise HTTPException(
            400, f"A platform is written P01, P04 and so on, not {body.platform!r}. "
                 f"Leave it out to mean the whole of {TAG_LABEL.get(tag, tag)}.")

    # NULL rather than '' for "the whole side", because the unique index has to
    # tell it from a named platform and SQLite compares '' as a value.
    stored = platform or None
    existing = db.one(
        "SELECT id FROM scope WHERE account_id = ? AND project_id = ? AND tag = ? "
        "AND platform IS ?", (account_id, project, tag, stored))
    if existing:
        raise HTTPException(409, "They already hold that one.")

    db.write(
        "INSERT INTO scope (account_id, project_id, tag, platform, granted_by, granted_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (account_id, project, tag, stored, owner["id"], security.stamp()))
    row = db.one(_SCOPE_SELECT + " WHERE s.account_id = ? AND s.project_id = ? "
                 "AND s.tag = ? AND s.platform IS ?",
                 (account_id, project, tag, stored))
    return {"ok": True, "scope": _scope_row(row)}


@app.delete("/api/scopes/{scope_id}")
def revoke_scope(scope_id: int, owner: dict = Depends(require_owner)):
    """Take one back. The super admin, and nobody else."""
    if not db.change("DELETE FROM scope WHERE id = ?", (scope_id,)):
        raise HTTPException(404, "No such grant.")
    return {"ok": True}


@app.post("/api/auth/password")
def change_password(body: PasswordChange, account: dict = Depends(require_account),
                    ticvai_session: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE)):
    row = db.one("SELECT password_hash FROM account WHERE id = ?", (account["id"],))
    if not security.verify_password(row["password_hash"], body.current):
        raise HTTPException(401, "That is not your current password.")
    try:
        security.check_password(body.replacement)
    except ValueError as exc:
        raise HTTPException(400, str(exc))

    db.write("UPDATE account SET password_hash = ? WHERE id = ?",
             (security.hash_password(body.replacement), account["id"]))
    # Every other session belonging to this account ends: changing a password
    # is what someone does when they think one has been taken, and it would be
    # no use if whoever took it stayed signed in.
    keep = security.token_hash(ticvai_session) if ticvai_session else ""
    db.write("DELETE FROM session WHERE account_id = ? AND token_hash != ?",
             (account["id"], keep))
    return {"ok": True}


# ── invites ──────────────────────────────────────────────────────────

@app.post("/api/invites")
def create_invite(body: InviteRequest, admin: dict = Depends(require_admin)):
    """Makes a link for one address.

    The address is fixed here, by an admin, and cannot be changed by whoever
    opens the link. That is what makes an invite count as having verified the
    address: the person who could vouch for it is the person who typed it.
    """
    # The role is settled before the address, because it is the role that
    # decides whether the domain rule applies. A client is outside the company and
    # is expected to be on another domain; a reviewer is not.
    if body.role not in security.ROLES:
        raise HTTPException(400, f"A role is one of {', '.join(security.ROLES)}.")
    if body.role in security.CLI_ONLY:
        # The same rule as set_role, stated again because this is the other door
        # into a role. An invite is a link handed to somebody; a link that makes
        # a super admin is a super admin left in whatever chat it was pasted in.
        raise HTTPException(
            403, f"An invite cannot make a {body.role}. That role is set on the "
                 f"machine, with `python -m api.cli owner <address>`.")

    try:
        email = security.check_email(body.email, body.role)
    except security.DomainError as exc:
        raise HTTPException(400, str(exc))

    # A client link goes to an address outside the company, so it is worth less
    # for less time. Asking for longer is capped rather than refused.
    days = min(body.days, security.CLIENT_INVITE_DAYS) if body.role == "client" else body.days

    project_id = (body.project_id or db.FIRST_PROJECT).strip()
    project = db.one("SELECT id, name, active FROM project WHERE id = ?", (project_id,))
    if not project or not project["active"]:
        raise HTTPException(400, f"There is no open ADAM project called '{project_id}'.")

    folded = db.fold(email)
    if db.one("SELECT id FROM account WHERE email_folded = ?", (folded,)):
        raise HTTPException(409, f"{email} already holds an account.")

    # A second invite to the same address supersedes the first, so a resend
    # cannot leave two live links for one person.
    db.write(
        """UPDATE invite SET revoked_at = ?
            WHERE email_folded = ? AND redeemed_at IS NULL AND revoked_at IS NULL""",
        (security.stamp(), folded),
    )

    token = security.new_token()
    invite_id = db.write(
        """INSERT INTO invite
             (email, email_folded, token_hash, role, project_id, created_by,
              created_at, expires_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            email, folded, security.token_hash(token), body.role, project_id,
            admin["id"], security.stamp(), security.invite_expiry(days),
        ),
    )
    # The only time the token exists in the clear. It is not recoverable later,
    # by us or by anyone who takes a copy of the database.
    return {
        "id": invite_id,
        "email": email,
        "role": body.role,
        "project": {"id": project["id"], "name": project["name"]},
        "link": f"/invite.html#{token}",
        "token": token,
        "expires_at": db.one("SELECT expires_at FROM invite WHERE id = ?",
                             (invite_id,))["expires_at"],
    }


@app.get("/api/invites")
def list_invites(admin: dict = Depends(require_admin)):
    rows = db.all_rows(
        """SELECT i.id, i.email, i.role, i.project_id, p.name AS project_name,
                  i.created_at, i.expires_at, i.redeemed_at, i.revoked_at
             FROM invite i LEFT JOIN project p ON p.id = i.project_id
            ORDER BY i.id DESC"""
    )
    out = []
    for r in rows:
        state = (
            "redeemed" if r["redeemed_at"] else
            "revoked" if r["revoked_at"] else
            "expired" if security.expired(r["expires_at"]) else "open"
        )
        out.append({**dict(r), "state": state})
    return {"invites": out}


@app.delete("/api/invites/{invite_id}")
def revoke_invite(invite_id: int, admin: dict = Depends(require_admin)):
    row = db.one("SELECT redeemed_at FROM invite WHERE id = ?", (invite_id,))
    if not row:
        raise HTTPException(404, "No such invite.")
    if row["redeemed_at"]:
        raise HTTPException(409, "That invite has already been used.")
    db.write("UPDATE invite SET revoked_at = ? WHERE id = ?",
             (security.stamp(), invite_id))
    return {"ok": True}


@app.get("/api/invites/check/{token}")
def check_invite(token: str):
    """What an invite is for, so the page can greet the right person — and
    refuse plainly rather than after they have chosen a password."""
    row = _live_invite(token)
    return {"email": row["email"], "role": row["role"]}


def _live_invite(token: str):
    row = db.one(
        """SELECT id, email, email_folded, role, project_id, expires_at, redeemed_at, revoked_at
             FROM invite WHERE token_hash = ?""",
        (security.token_hash(token),),
    )
    if not row:
        raise HTTPException(404, "That invite link is not valid.")
    if row["redeemed_at"]:
        raise HTTPException(409, "That invite has already been used.")
    if row["revoked_at"]:
        raise HTTPException(409, "That invite was withdrawn.")
    if security.expired(row["expires_at"]):
        raise HTTPException(409, "That invite has expired. Ask for another.")
    return row


@app.post("/api/auth/redeem")
def redeem(body: Redemption, response: Response, request: Request):
    """Turns an invite into an account. The address comes from the invite, not
    from the form, so there is nothing here for a caller to claim."""
    invite = _live_invite(body.token)
    try:
        security.check_password(body.password)
    except ValueError as exc:
        raise HTTPException(400, str(exc))

    if db.one("SELECT id FROM account WHERE email_folded = ?", (invite["email_folded"],)):
        raise HTTPException(409, "That address already holds an account.")

    account_id = db.write(
        """INSERT INTO account (email, email_folded, name, password_hash, role, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            invite["email"], invite["email_folded"], body.name.strip(),
            security.hash_password(body.password), invite["role"], security.stamp(),
        ),
    )
    db.write("UPDATE invite SET redeemed_at = ? WHERE id = ?",
             (security.stamp(), invite["id"]))
    # The project the invite was for. Without this row the new account can open
    # nothing until the next restart, when the startup backfill happens to grant
    # every account the first project. Admin is not a project role (see
    # projects_for), so an admin invite lands as reviewer here.
    db.write(
        "INSERT OR IGNORE INTO account_project (account_id, project_id, role, created_at) "
        "VALUES (?, ?, ?, ?)",
        (account_id, invite["project_id"] or db.FIRST_PROJECT,
         "client" if invite["role"] == "client" else "reviewer", security.stamp()),
    )

    token = security.new_token()
    db.write(
        """INSERT INTO session (token_hash, account_id, created_at, expires_at, user_agent)
           VALUES (?, ?, ?, ?, ?)""",
        (
            security.token_hash(token), account_id, security.stamp(),
            security.session_expiry(), request.headers.get("user-agent", "")[:200],
        ),
    )
    _set_session_cookie(response, token)
    return {"ok": True, "email": invite["email"], "role": invite["role"]}


# ── resetting a password ─────────────────────────────────────────────
#
# There is no self-service reset and this is not one. This package holds a hash
# of a password and no mailer, so there is nothing that can prove an address to
# a stranger who has forgotten theirs — which is what the sign-in page says
# plainly rather than offering a link it cannot honour.
#
# What it can do is let an admin, who already decides who holds an account at
# all, hand out a link. The trust is the same trust an invite runs on: somebody
# who can vouch for the person is the person who made the link, and the link
# goes to them through whatever channel they already use.
#
# Three things this is careful about:
#
#   1. The admin never learns the new password. They mint a link; the person
#      chooses the password behind it. An admin who set passwords directly
#      would be an admin who could sign in as anybody and leave verdicts under
#      their name, and the audit trail's whole value is that it cannot.
#   2. One live link per account. Making a second withdraws the first, so a
#      re-send cannot leave two ways in.
#   3. Using it ends every session that account had. A reset is what somebody
#      reaches for when they have lost control of an account, and one that left
#      the old sessions running would be a reset in name only.


def _live_reset(token: str):
    row = db.one(
        """SELECT r.id, r.account_id, r.expires_at, r.used_at, r.revoked_at,
                  a.email, a.name, a.active
             FROM reset r JOIN account a ON a.id = r.account_id
            WHERE r.token_hash = ?""",
        (security.token_hash(token),),
    )
    if not row:
        raise HTTPException(404, "That reset link is not valid.")
    if row["used_at"]:
        raise HTTPException(409, "That reset link has already been used.")
    if row["revoked_at"]:
        raise HTTPException(409, "That reset link was replaced by a newer one.")
    if security.expired(row["expires_at"]):
        raise HTTPException(409, "That reset link has expired. Ask for another.")
    if not row["active"]:
        raise HTTPException(409, "That account is disabled.")
    return row


@app.post("/api/accounts/{account_id}/reset")
def make_reset(account_id: int, admin: dict = Depends(require_admin)):
    """Mints a link that lets one person set a new password."""
    person = db.one("SELECT id, email, name, active FROM account WHERE id = ?", (account_id,))
    if not person:
        raise HTTPException(404, "No such account.")
    if not person["active"]:
        raise HTTPException(409, "That account is disabled. Enable it first.")

    # A second link supersedes the first, so a resend cannot leave two live.
    db.change(
        "UPDATE reset SET revoked_at = ? WHERE account_id = ? AND used_at IS NULL AND revoked_at IS NULL",
        (security.stamp(), account_id),
    )

    token = security.new_token()
    expires = security.reset_expiry()
    db.write(
        """INSERT INTO reset (account_id, token_hash, created_by, created_at, expires_at)
           VALUES (?, ?, ?, ?, ?)""",
        (account_id, security.token_hash(token), admin["id"], security.stamp(), expires),
    )
    # The path only. The admin's browser knows which address it reached this
    # page on, and it is the one the person being sent the link has to use.
    #
    # The token rides in the fragment for the same reason an invite's does: a
    # fragment is never sent to the server in a request line, so it cannot land
    # in an access log, a proxy trace or a Referer header on the way past.
    return {
        "ok": True,
        "link": f"/invite.html#reset={token}",
        "email": person["email"],
        "name": person["name"],
        "expires_at": expires,
    }


@app.get("/api/reset/check/{token}")
def check_reset(token: str):
    """What the reset page asks before drawing a form. Says who the link is for
    so nobody sets a password on an account they did not mean to."""
    row = _live_reset(token)
    return {"ok": True, "email": row["email"], "name": row["name"]}


@app.post("/api/auth/reset")
def use_reset(body: PasswordReset, response: Response, request: Request):
    """Sets the new password, ends every old session, and signs them in here."""
    row = _live_reset(body.token)
    try:
        security.check_password(body.password)
    except ValueError as exc:
        raise HTTPException(400, str(exc))

    db.write(
        "UPDATE account SET password_hash = ? WHERE id = ?",
        (security.hash_password(body.password), row["account_id"]),
    )
    db.write("UPDATE reset SET used_at = ? WHERE id = ?", (security.stamp(), row["id"]))

    # Every session, including any the old password left open somewhere else.
    dropped = db.change("DELETE FROM session WHERE account_id = ?", (row["account_id"],))

    token = security.new_token()
    db.write(
        """INSERT INTO session (token_hash, account_id, created_at, expires_at, user_agent)
           VALUES (?, ?, ?, ?, ?)""",
        (
            security.token_hash(token), row["account_id"], security.stamp(),
            security.session_expiry(), request.headers.get("user-agent", "")[:200],
        ),
    )
    _set_session_cookie(response, token)
    return {"ok": True, "email": row["email"], "dropped": dropped}


# ── settings: what a developer configures about themselves ───────────
#
# One page, because the configuration stopped being one field. It holds the
# things ADAM needs *per person* rather than per installation: the OpenProject
# credential it will act with, the git identity that ties a commit back to a
# work package, and the line that wires up the MCP bridge.
#
# **The credential is per account and never shared.** A single service token
# would attribute every status change in the PMS to one robot, which destroys
# the audit trail the PMS exists for. Yours moves things as you.

OPENPROJECT = "openproject"

# Where the PMS is. One instance, so it is a default rather than a question —
# but stored per credential, because a token is only meaningful against the host
# that issued it and pointing somewhere new must not silently send the old key.
DEFAULT_PMS = os.environ.get("TICVAI_PMS_URL", "https://pms.softlabsgroup.in").rstrip("/")


class GitIdentityIn(BaseModel):
    git_email: str = ""


class PmsTokenIn(BaseModel):
    token: str
    endpoint: str = ""


def _secret_row(account_id: int, kind: str):
    return db.one(
        "SELECT ciphertext, hint, endpoint, updated_at FROM account_secret "
        "WHERE account_id = ? AND kind = ?",
        (account_id, kind),
    )


@app.get("/api/settings/me")
def my_settings(account: dict = Depends(require_account)):
    """
    What this person has configured. **Never a token** — the hint is the last
    four characters, which is enough to recognise which one is stored.
    """
    row = db.one("SELECT git_email FROM account WHERE id = ?", (account["id"],))
    stored = _secret_row(account["id"], OPENPROJECT)
    return {
        "email": account["email"],
        "name": account["name"],
        "gitEmail": (row["git_email"] if row else "") or "",
        "openproject": {
            "configured": bool(stored),
            "hint": stored["hint"] if stored else "",
            "endpoint": (stored["endpoint"] if stored else "") or DEFAULT_PMS,
            "updatedAt": stored["updated_at"] if stored else None,
        },
        # Said out loud rather than left for a 500 after somebody types a token
        # in. A deployment with no key cannot store one, and the reason names
        # the variable to set.
        "canStoreCredentials": secrets.available(),
        "whyNot": secrets.describe_key(),
    }


@app.put("/api/settings/git-identity")
def set_git_identity(body: GitIdentityIn, account: dict = Depends(require_account)):
    """The address this person's commits carry. Blank clears it."""
    value = body.git_email.strip()
    if value and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
        raise HTTPException(400, "That is not an e-mail address.")
    db.write("UPDATE account SET git_email = ? WHERE id = ?", (value, account["id"]))
    return {"ok": True, "gitEmail": value}


@app.put("/api/settings/openproject")
def set_openproject_token(body: PmsTokenIn, account: dict = Depends(require_account)):
    """
    Store an OpenProject API token for this account, encrypted.

    **The token is checked against the instance before it is kept.** A token
    that does not work is worse than none: it is stored, looks configured, and
    fails later somewhere that reads as a different bug. So this calls
    `/api/v3/users/me` as the token and refuses anything that does not come back
    naming a user.
    """
    token = body.token.strip()
    if not token:
        raise HTTPException(400, "Paste a token.")
    if not secrets.available():
        raise HTTPException(503, secrets.describe_key())

    endpoint = (body.endpoint.strip() or DEFAULT_PMS).rstrip("/")
    if not endpoint.startswith(("http://", "https://")):
        raise HTTPException(400, "The instance must be an http or https address.")
    # **No userinfo.** `https://apikey:SECRET@pms.example.com` is a valid URL and
    # would be stored in `endpoint` — which is a plaintext column, deliberately,
    # because it is meant to hold a hostname. A credential smuggled in there
    # would sit unencrypted beside the encrypted one and appear in any error
    # message naming the endpoint.
    if "@" in endpoint.split("//", 1)[1].split("/", 1)[0]:
        raise HTTPException(
            400,
            "Give the instance address on its own — a username or password in "
            "the URL would be stored unencrypted. The token field is what "
            "carries the credential.",
        )

    # OpenProject takes an API key as HTTP Basic with the literal username
    # `apikey`. Verified here rather than trusted.
    auth = base64.b64encode(f"apikey:{token}".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(
        f"{endpoint}/api/v3/users/me",
        headers={
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
            # **Named, because urllib's default gets us blocked.** The instance
            # sits behind Cloudflare, which refuses `Python-urllib/3.9` outright
            # with a 403 and error 1010 — "blocked based on your browser's
            # signature". That 403 never reaches OpenProject, so reading it as
            # a rejected token accuses the one thing that was fine. The same
            # request from curl succeeds; the only difference is this header.
            "User-Agent": "ADAM-bridge/1.0 (+https://adam.ainfinite.ai)",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as answer:
            who = json.loads(answer.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", "replace")[:400]
        except Exception:  # noqa: BLE001 — a body that will not read is not the story
            pass
        # An edge that refused us never asked OpenProject anything, so the token
        # is not what failed and must not be blamed. Told apart by the body,
        # because the status code alone is a 403 either way.
        if "cloudflare" in body.lower() or "error_code" in body and "1010" in body:
            raise HTTPException(
                502,
                f"{endpoint} is behind a proxy that refused this service before "
                f"OpenProject saw it. Your token was never checked. An "
                f"administrator needs to allow this server through.",
            )
        if exc.code in (401, 403):
            raise HTTPException(400, "OpenProject did not accept that token.")
        raise HTTPException(502, f"OpenProject answered {exc.code} — try again.")
    except Exception as exc:  # noqa: BLE001 — the network, in all its forms
        raise HTTPException(502, f"Could not reach {endpoint}: {exc}")

    who_name = who.get("name") or who.get("login") or "an account"

    now = security.stamp()
    existing = _secret_row(account["id"], OPENPROJECT)
    if existing:
        db.write(
            "UPDATE account_secret SET ciphertext = ?, hint = ?, endpoint = ?, "
            "updated_at = ? WHERE account_id = ? AND kind = ?",
            (secrets.seal(token), secrets.hint(token), endpoint, now,
             account["id"], OPENPROJECT),
        )
    else:
        db.write(
            "INSERT INTO account_secret (account_id, kind, ciphertext, hint, endpoint, "
            "created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (account["id"], OPENPROJECT, secrets.seal(token), secrets.hint(token),
             endpoint, now, now),
        )
    # Who it turned out to be, so somebody who pasted the wrong token sees it
    # immediately rather than discovering it when work is attributed oddly.
    return {"ok": True, "connectedAs": who_name, "hint": secrets.hint(token),
            "endpoint": endpoint}


@app.delete("/api/settings/openproject")
def forget_openproject_token(account: dict = Depends(require_account)):
    """
    Remove it. **This does not revoke it in OpenProject** — only the owner can
    do that, from their account page there — and the answer says so, because
    "removed" reading as "revoked" is how a live credential is left lying about.
    """
    db.write("DELETE FROM account_secret WHERE account_id = ? AND kind = ?",
             (account["id"], OPENPROJECT))
    return {
        "ok": True,
        "note": "Removed from ADAM. The token is still live in OpenProject until "
                "you delete it there, under My account → Access tokens.",
    }


# ── the join: which artefact a work package is about ─────────────────
#
# **The only thing this service stores about scheduled work.** OpenProject holds
# the work packages and is good at it; what it cannot express is that WP #1841 is
# about screen `BO-102` and table `access.entitlement`, because it knows nothing
# about the package. The package knows those names and nothing about the
# schedule. This is the join, and it is deliberately the whole of ADAM's
# ambition here — a second issue tracker would be CF-124 committed on purpose.

# What an artefact can be. Checked rather than free text: a typo'd kind makes a
# row no board will ever look for again, and it fails silently.
LINKABLE = {"screen", "flow", "contract", "operation", "schema", "table",
            "module", "service", "adr", "platform"}


def _work_package_key(raw: str) -> str:
    """An OpenProject work package id, checked before it becomes part of a URL.

    They are integers, always. Without this the value goes straight into
    `work_packages/{key}` — and a key containing a `?` would append a query
    string to the request, while `..` would walk up to the API root and return
    something that is not a work package at all. Neither is dangerous here, but
    both produce an answer that is confidently about the wrong thing, which is
    the failure mode worth spending three lines on.
    """
    key = str(raw).strip().lstrip("#")
    if not key.isdigit():
        raise HTTPException(400, f"'{raw}' is not a work package number.")
    return key


class LinkIn(BaseModel):
    target_kind: str
    target_id: str
    external_key: str
    project_id: str = ""


def _pms_for(account_id: int):
    """This person's OpenProject endpoint and token, decrypted.

    Raises the sentence to show them if they have not configured one — which is
    a thing to fix on a page, not an error to log.
    """
    row = db.one(
        "SELECT ciphertext, endpoint FROM account_secret WHERE account_id = ? AND kind = ?",
        (account_id, OPENPROJECT),
    )
    if not row:
        raise HTTPException(
            428,
            "Connect your OpenProject account first — Settings, then paste an API "
            "token. ADAM reads the PMS as you, never as a shared service account.",
        )
    try:
        return (row["endpoint"] or DEFAULT_PMS), secrets.open_(row["ciphertext"])
    except secrets.Unreadable as exc:
        raise HTTPException(409, str(exc))


def _link_row(row) -> dict:
    return {
        "id": row["id"],
        "target": {"kind": row["target_kind"], "id": row["target_id"]},
        "system": row["external_system"],
        "key": row["external_key"],
        "url": row["url"],
        # Labelled as a cache wherever it is shown. OpenProject is the truth
        # about status; this is what it said at `syncedAt` and may be old.
        "cached": {
            "subject": row["cached_subject"],
            "status": row["cached_status"],
            "type": row["cached_type"],
            "assignee": row["cached_assignee"],
            "syncedAt": row["synced_at"],
        },
    }


def _readable_project(account: dict, project_id: str) -> str:
    """The ADAM project a work call is about, checked against what this account
    may open. Blank means the first project, which is what every caller meant
    before the parameter existed."""
    project = (project_id or db.FIRST_PROJECT).strip()
    if project not in {p["id"] for p in projects_for(account)}:
        raise HTTPException(403, f"You do not have access to the ADAM project '{project}'.")
    return project


def _pms_scope(account: dict, project_id: str) -> dict:
    """
    Which OpenProject project this ADAM project reads, or the sentence to show.

    **Refused rather than widened when nobody has chosen.** Falling back to the
    whole instance is what this replaced: a board of every ticket assigned to
    you anywhere, most of them about other products.
    """
    project = _readable_project(account, project_id)
    row = db.one(
        "SELECT id, name, pms_project_id, pms_identifier, pms_name FROM project WHERE id = ?",
        (project,),
    )
    if not row or row["pms_project_id"] is None:
        raise HTTPException(
            428,
            f"No OpenProject project has been chosen for the ADAM project "
            f"'{(row['name'] if row else '') or project}' yet. An admin sets it on "
            f"the admin page, under Projects.",
        )
    return {
        "project": project,
        "pmsId": row["pms_project_id"],
        "pmsIdentifier": row["pms_identifier"],
        "pmsName": row["pms_name"],
    }


def _in_scope(found: dict, scope: dict, number: str) -> None:
    """A work package from another OpenProject project is not this one's."""
    if found.get("projectId") != scope["pmsId"]:
        raise HTTPException(
            404,
            f"#{number} is in the OpenProject project '{found.get('project') or '?'}', "
            f"not in '{scope['pmsName'] or scope['pmsIdentifier']}', which the ADAM "
            f"project '{scope['project']}' reads.",
        )


@app.get("/api/links")
def list_links(
    target_kind: str = Query(default=""),
    target_id: str = Query(default=""),
    external_key: str = Query(default=""),
    project_id: str = Query(default=""),
    account: dict = Depends(require_account),
):
    """
    Links, read either way round.

    Artefact to work is "what is scheduled against this screen". Work to
    artefact is "what does this ticket touch", which is what an agent asks when
    it opens a branch. Both are one index away, which is why the table carries
    two.
    """
    project = _readable_project(account, project_id)
    where = ["project_id = ?"]
    args = [project]
    if target_kind:
        where.append("target_kind = ?")
        args.append(target_kind)
    if target_id:
        where.append("target_id = ?")
        args.append(target_id)
    if external_key:
        where.append("external_key = ?")
        args.append(external_key.lstrip("#"))

    rows = db.all_rows(
        f"SELECT * FROM artefact_link WHERE {' AND '.join(where)} ORDER BY id DESC",
        tuple(args),
    )
    return {"total": len(rows), "links": [_link_row(r) for r in rows]}


@app.post("/api/links")
def make_link(body: LinkIn, account: dict = Depends(require_account)):
    """
    Say that a work package is about an artefact.

    **The work package is fetched before the row is written.** A link to a
    number nobody can open is worse than no link: it looks like coordination,
    is a dead end, and the board that draws it has no way to tell. Fetching also
    fills the cached columns, so a listing can be drawn without one API call per
    row.
    """
    kind = body.target_kind.strip().lower()
    if kind not in LINKABLE:
        raise HTTPException(
            400,
            f"'{kind}' is not something a work package can be about. "
            f"One of: {', '.join(sorted(LINKABLE))}.",
        )
    target = body.target_id.strip()
    if not target:
        raise HTTPException(400, "Both an artefact and a work package are needed.")
    key = _work_package_key(body.external_key)

    scope = _pms_scope(account, body.project_id)
    endpoint, token = _pms_for(account["id"])
    try:
        found = openproject.work_package(endpoint, token, key)
    except openproject.Blocked as exc:
        raise HTTPException(502, str(exc))
    except openproject.Refused as exc:
        raise HTTPException(400 if exc.status == 404 else 502, str(exc))
    try:
        _in_scope(found, scope, key)
    except HTTPException as exc:
        # A link is a claim about this package; one to another product's
        # ticket is refused like a number that does not exist.
        raise HTTPException(400, exc.detail)

    project = scope["project"]
    now = security.stamp()
    try:
        db.write(
            "INSERT INTO artefact_link (project_id, target_kind, target_id, "
            "external_system, external_key, url, cached_subject, cached_status, "
            "cached_type, cached_assignee, synced_at, created_at, created_by) "
            "VALUES (?, ?, ?, 'openproject', ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (project, kind, target, key, found["url"], found["subject"],
             found["status"], found["type"], found["assignee"], now, now,
             account["id"]),
        )
    except Exception as exc:  # noqa: BLE001 — the UNIQUE is the one that matters
        if "UNIQUE" in str(exc).upper():
            # Already said. The state the caller wanted is the state that
            # exists, so this is a 409 and not a failure worth alarm.
            raise HTTPException(409, f"{kind} {target} is already linked to #{key}.")
        raise

    return {"ok": True, "linked": {"kind": kind, "id": target}, "workPackage": found}


@app.delete("/api/links/{link_id}")
def drop_link(link_id: int, account: dict = Depends(require_account)):
    """Unsay it. Deletes the join and nothing in OpenProject — which is the
    whole point of the join living here."""
    row = db.one("SELECT id FROM artefact_link WHERE id = ?", (link_id,))
    if not row:
        raise HTTPException(404, "No such link.")
    db.write("DELETE FROM artefact_link WHERE id = ?", (link_id,))
    return {"ok": True, "note": "The link is gone. The work package is untouched."}


@app.get("/api/work-packages/{key}")
def read_work_package(
    key: str,
    project_id: str = Query(default=""),
    account: dict = Depends(require_account),
):
    """One work package, read live as the caller, with whatever it is linked to.
    Only from the OpenProject project the ADAM project reads."""
    # The number is checked before the credential is looked up, and the order
    # matters: the other way round, asking for `/api/work-packages/banana`
    # without a stored token answers "connect your OpenProject account", which
    # sends somebody to configure a thing that was never the problem.
    number = _work_package_key(key)
    scope = _pms_scope(account, project_id)
    endpoint, token = _pms_for(account["id"])
    try:
        found = openproject.work_package(endpoint, token, number)
    except openproject.Blocked as exc:
        raise HTTPException(502, str(exc))
    except openproject.Refused as exc:
        raise HTTPException(404 if exc.status == 404 else 502, str(exc))
    _in_scope(found, scope, number)

    rows = db.all_rows(
        "SELECT * FROM artefact_link WHERE external_key = ? "
        "AND external_system = 'openproject' AND project_id = ?",
        (number, scope["project"]),
    )
    return {"workPackage": found, "touches": [_link_row(r)["target"] for r in rows]}


@app.get("/api/board/mine")
def my_board(
    project_id: str = Query(default=""),
    account: dict = Depends(require_account),
):
    """
    What is open and assigned to this person, with the artefacts each touches.

    Live from OpenProject rather than from the cached columns: a board is the
    one place staleness shows, and it is read rarely enough that one API call is
    the right cost. The cached columns exist for listings that hang off an
    artefact, where fanning out would be one call per row.
    """
    scope = _pms_scope(account, project_id)
    endpoint, token = _pms_for(account["id"])
    try:
        items = openproject.mine(endpoint, token, project_id=scope["pmsId"])
    except (openproject.Blocked, openproject.Refused) as exc:
        raise HTTPException(502, str(exc))
    # Checked again here, in case an instance ignores the filter: a board that
    # quietly shows other products' tickets is the thing this scope prevents.
    items = [item for item in items if item.get("projectId") == scope["pmsId"]]

    # One query for every link, joined in memory. The alternative is a query per
    # work package, and this table is small.
    touching: dict = {}
    for row in db.all_rows(
        "SELECT external_key, target_kind, target_id FROM artefact_link "
        "WHERE external_system = 'openproject' AND project_id = ?", (scope["project"],)
    ):
        touching.setdefault(row["external_key"], []).append(
            {"kind": row["target_kind"], "id": row["target_id"]})

    return {
        "total": len(items),
        "endpoint": endpoint,
        "project": scope["project"],
        "openproject": {
            "id": scope["pmsId"],
            "identifier": scope["pmsIdentifier"],
            "name": scope["pmsName"],
            "url": f"{endpoint}/projects/{scope['pmsIdentifier']}" if scope["pmsIdentifier"] else "",
        },
        "items": [{**item, "touches": touching.get(item["key"], [])} for item in items],
        # Said out loud when it is the answer. An empty board reads as "nothing
        # assigned to me", and the truth may be "nothing has been loaded yet".
        "note": None if items else
                f"Nothing open is assigned to you in the OpenProject project "
                f"'{scope['pmsName'] or scope['pmsIdentifier']}'. If its work has not "
                f"been loaded there yet, that is why.",
    }


# ── the delivery overview: every ticket in the project, for an admin ─
#
# `/api/board/mine` answers "what am I holding". This answers "where is the
# delivery", which is a different question with a different cost: every ticket in
# every state, so the closed and the rejected are counted too, paged out of
# OpenProject a few hundred at a time.
#
# That cost is why this one is cached and the board is not. A board is read by
# the person whose work it is, once, and a minute-old board is a wrong board. An
# overview is a page several admins leave open, and the number it exists to show
# — how the project is going — does not change between two reads a minute apart.
# So: one read per project per five minutes, and a Refresh button for the
# impatient, which is `refresh=1` and skips the cache.
#
# Admin-only, unlike the rest of the PMS routes. It carries every assignee's
# workload, which is the one PMS shape that is nobody's business but the team's.

OVERVIEW_TTL_SECONDS = 300
OVERVIEW_LIMIT = 2000
# {(adam project, openproject id): {"at": monotonic, "payload": {...}}}
_overview_cache: dict = {}


def _overview_payload(account: dict, scope: dict) -> dict:
    """One live read of a whole project, with the artefact links joined in."""
    endpoint, token = _pms_for(account["id"])
    try:
        items = openproject.everything(
            endpoint, token, scope["pmsId"], limit=OVERVIEW_LIMIT)
        known = openproject.statuses(endpoint, token)
    except (openproject.Blocked, openproject.Refused) as exc:
        raise HTTPException(502, str(exc))
    # Same belt-and-braces as the board: an instance that ignores the project
    # filter must not turn an overview of one product into an overview of all.
    items = [item for item in items if item.get("projectId") == scope["pmsId"]]

    touching: dict = {}
    for row in db.all_rows(
        "SELECT external_key, target_kind, target_id FROM artefact_link "
        "WHERE external_system = 'openproject' AND project_id = ?", (scope["project"],)
    ):
        touching.setdefault(row["external_key"], []).append(
            {"kind": row["target_kind"], "id": row["target_id"]})

    return {
        "project": scope["project"],
        "endpoint": endpoint,
        "openproject": {
            "id": scope["pmsId"],
            "identifier": scope["pmsIdentifier"],
            "name": scope["pmsName"],
            "url": f"{endpoint}/projects/{scope['pmsIdentifier']}" if scope["pmsIdentifier"] else "",
        },
        # Named by OpenProject, not by ADAM. Which of them count as finished is
        # `isClosed`, which is the instance's own answer and survives a team
        # renaming its columns.
        "statuses": known,
        "total": len(items),
        # Said out loud rather than left to look like a small project.
        "truncated": len(items) >= OVERVIEW_LIMIT,
        "items": [{**item, "touches": touching.get(item["key"], [])} for item in items],
        "note": None if items else
                f"The OpenProject project '{scope['pmsName'] or scope['pmsIdentifier']}' "
                f"has no work packages yet.",
    }


@app.get("/api/board/overview")
def delivery_overview(
    project_id: str = Query(default=""),
    refresh: int = Query(default=0),
    account: dict = Depends(require_reader),
):
    """Every ticket in the project's OpenProject project, cached for five minutes.

    A reader's rather than an administrator's: this is the delivery, and a pm
    who cannot see it is not overseeing anything. Note that it still runs on the
    caller's own OpenProject token, so a pm sees what their own OpenProject
    account can see — ADAM widens who may ask, and does not widen the answer.
    """
    scope = _pms_scope(account, project_id)
    key = (scope["project"], scope["pmsId"])
    now = time.monotonic()
    held = _overview_cache.get(key)
    if held and not refresh and now - held["at"] < OVERVIEW_TTL_SECONDS:
        age = int(now - held["at"])
        return {**held["payload"], "asOf": held["asOf"], "ageSeconds": age,
                "fromCache": True, "cacheSeconds": OVERVIEW_TTL_SECONDS}

    payload = _overview_payload(account, scope)
    asOf = security.stamp()
    _overview_cache[key] = {"at": now, "asOf": asOf, "payload": payload}
    return {**payload, "asOf": asOf, "ageSeconds": 0, "fromCache": False,
            "cacheSeconds": OVERVIEW_TTL_SECONDS}


# ── changing a work package: proposed, shown, then applied ───────────
#
# Claude never changes OpenProject in one step. `propose` reads the work package,
# works out what would change, and keeps that under a one-use token; nothing is
# sent. The person is shown the change. Only `apply`, with the token, sends it —
# as that person, with their own OpenProject token, so OpenProject's history
# names them. The change is refused if the work package has moved since it was
# shown, because what the person agreed to was a change to what they saw.

PROPOSAL_MINUTES = 15


class ProposalIn(BaseModel):
    project_id: str = ""
    status: str = ""
    percent_done: Optional[int] = Field(default=None, ge=0, le=100)
    comment: str = Field(default="", max_length=5000)


class ApplyIn(BaseModel):
    project_id: str = ""


def _pick_status(wanted: str, known: list) -> dict:
    """A status by name, forgiving of case and spacing. Refuses with the names
    there are, so the next attempt can be right."""
    fold = lambda text: re.sub(r"[^a-z0-9]+", "", (text or "").lower())  # noqa: E731
    for status in known:
        if fold(status["name"]) == fold(wanted):
            return status
    names = ", ".join(st["name"] for st in known)
    raise HTTPException(400, f"OpenProject has no status called '{wanted}'. It has: {names}.")


@app.get("/api/board/statuses")
def list_statuses(account: dict = Depends(require_account)):
    """The statuses a work package can be given, by name."""
    endpoint, token = _pms_for(account["id"])
    try:
        found = openproject.statuses(endpoint, token)
    except (openproject.Blocked, openproject.Refused) as exc:
        raise HTTPException(502, str(exc))
    return {"statuses": found}


@app.post("/api/work-packages/{key}/proposals")
def propose_change(key: str, body: ProposalIn, account: dict = Depends(require_account)):
    """
    Work out a change and keep it for the person to agree to. **Sends nothing.**
    """
    number = _work_package_key(key)
    wanted_status = body.status.strip()
    note = body.comment.strip()
    if not wanted_status and body.percent_done is None and not note:
        raise HTTPException(400, "Say what should change: a status, a % done, or a comment.")

    scope = _pms_scope(account, body.project_id)
    endpoint, token = _pms_for(account["id"])
    try:
        found = openproject.work_package(endpoint, token, number)
        status = _pick_status(wanted_status, openproject.statuses(endpoint, token)) \
            if wanted_status else None
    except openproject.Blocked as exc:
        raise HTTPException(502, str(exc))
    except openproject.Refused as exc:
        raise HTTPException(404 if exc.status == 404 else 502, str(exc))
    _in_scope(found, scope, number)

    changes = []
    if status and status["name"] != found["status"]:
        changes.append(f"status: {found['status'] or '(none)'} -> {status['name']}")
    elif status:
        status = None  # already that; nothing to send
    percent = body.percent_done
    if percent is not None and percent != found["percentDone"]:
        changes.append(f"% done: {found['percentDone'] if found['percentDone'] is not None else '(none)'} -> {percent}")
    else:
        percent = None
    if note:
        changes.append(f"comment: {note[:200]}{'...' if len(note) > 200 else ''}")
    if not changes:
        raise HTTPException(409, f"#{number} is already like that. Nothing to change.")

    proposal = security.new_token()
    now = security.now()
    db.write(
        "INSERT INTO wp_proposal (token_hash, account_id, project_id, external_key, "
        "lock_version, status_id, status_name, percent_done, comment, summary, "
        "created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (security.token_hash(proposal), account["id"], scope["project"], number,
         found.get("lockVersion"), status["id"] if status else None,
         status["name"] if status else "", percent, note, "; ".join(changes),
         security.stamp(now), security.stamp(now + timedelta(minutes=PROPOSAL_MINUTES))),
    )
    return {
        "proposal": proposal,
        "workPackage": {k: found[k] for k in ("key", "subject", "status", "percentDone", "url")},
        "changes": changes,
        "expiresInMinutes": PROPOSAL_MINUTES,
        "note": "Nothing has changed yet. Show these changes to the person and apply "
                "only after they say yes.",
    }


@app.post("/api/work-packages/{key}/proposals/{proposal}/apply")
def apply_change(key: str, proposal: str, body: ApplyIn,
                 account: dict = Depends(require_account)):
    """Send a change the person has agreed to. One use; their own token."""
    number = _work_package_key(key)
    row = db.one("SELECT * FROM wp_proposal WHERE token_hash = ?", (security.token_hash(proposal),))
    if not row or row["account_id"] != account["id"] or row["external_key"] != number:
        raise HTTPException(404, "No such proposal for this work package. Propose the change first.")
    if row["applied_at"]:
        raise HTTPException(409, "That change has already been applied.")
    if security.expired(row["expires_at"]):
        raise HTTPException(410, f"That proposal is more than {PROPOSAL_MINUTES} minutes old. Propose it again.")

    scope = _pms_scope(account, body.project_id or row["project_id"])
    if scope["project"] != row["project_id"]:
        raise HTTPException(400, "That proposal was made for another ADAM project.")
    endpoint, token = _pms_for(account["id"])

    # Claimed before it is sent, so two quick presses cannot send it twice.
    if not db.change("UPDATE wp_proposal SET applied_at = ? WHERE id = ? AND applied_at IS NULL",
                     (security.stamp(), row["id"])):
        raise HTTPException(409, "That change has already been applied.")
    try:
        current = openproject.work_package(endpoint, token, number)
        _in_scope(current, scope, number)
        if row["lock_version"] is not None and current.get("lockVersion") != row["lock_version"]:
            raise HTTPException(
                409, f"#{number} was changed in OpenProject after this was proposed. "
                     f"Look at it again and propose the change again.")
        updated = current
        if row["status_id"] is not None or row["percent_done"] is not None:
            updated = openproject.update(
                endpoint, token, number, current["lockVersion"],
                status_id=row["status_id"], percent_done=row["percent_done"])
        if row["comment"]:
            openproject.comment(endpoint, token, number, row["comment"])
    except HTTPException:
        db.change("UPDATE wp_proposal SET applied_at = NULL WHERE id = ?", (row["id"],))
        raise
    except openproject.Blocked as exc:
        db.change("UPDATE wp_proposal SET applied_at = NULL WHERE id = ?", (row["id"],))
        raise HTTPException(502, str(exc))
    except openproject.Refused as exc:
        # Partly sent is possible: the status landed and the comment did not.
        # The proposal stays used so it is not sent twice; the answer says so.
        raise HTTPException(
            409 if exc.status in (409, 422) else 502,
            f"{exc} (Check #{number} in OpenProject before trying again: part of the "
            f"change may already be there.)")

    # The cached columns on its links say what OpenProject said last; now it
    # says something new.
    db.change(
        "UPDATE artefact_link SET cached_status = ?, synced_at = ? "
        "WHERE external_system = 'openproject' AND external_key = ? AND project_id = ?",
        (updated.get("status", ""), security.stamp(), number, row["project_id"]),
    )
    return {
        "ok": True,
        "applied": row["summary"],
        "workPackage": {k: updated.get(k) for k in ("key", "subject", "status", "percentDone", "url")},
    }


# ── change requests ──────────────────────────────────────────────────
#
# Somebody building from the package found it wrong, contradictory or short of
# something the work needs. A developer's Claude drafts one and files it only
# after the developer says yes, the same two steps as an OpenProject change.
# Internal only; resolved by an admin or a reviewer on the project.

CHANGE_KINDS = ("contract", "operation", "schema", "table", "screen", "flow", "module",
                "service", "adr", "platform", "state", "event", "other")
# What each of those is called in a file somebody opens in Excel, and on the
# changes page. **Not KIND_LABEL**, which is the verdict vocabulary: that one has
# seven kinds to this one's thirteen and calls an operation "APIs", so using it
# here would label six of these blank and rename the rest. The same words as
# `KINDS` in changes.js and in public/change-csv.js, which is what makes the
# page's export and this one the same file.
CHANGE_KIND_LABEL = {
    "contract": "Contract", "operation": "Operation", "schema": "Schema",
    "table": "Table", "screen": "Screen", "flow": "Journey", "module": "Module",
    "service": "Service", "adr": "Decision", "platform": "Platform",
    "state": "State model", "event": "Event", "other": "Other",
}
CHANGE_STATUSES = ("open", "accepted", "rejected", "done")
DRAFT_MINUTES = 30


class ChangeIn(BaseModel):
    project_id: str = ""
    target_kind: str
    target_id: str = Field(min_length=1, max_length=300)
    title: str = Field(min_length=5, max_length=200)
    problem: str = Field(min_length=10, max_length=8000)
    evidence: str = Field(default="", max_length=8000)
    options: List[str] = Field(default_factory=list, max_length=8)
    recommendation: str = Field(default="", max_length=2000)
    blocking: bool = False
    ticket: str = Field(default="", max_length=20)
    # Whose queue. Both optional: `tag` falls back to the kind's usual side and
    # `platform` to the whole of it, which is what a filer who does not know
    # means. See _clean_change.
    tag: str = Field(default="", max_length=20)
    platform: str = Field(default="", max_length=20)


class FileIn(BaseModel):
    project_id: str = ""


class ResolveIn(BaseModel):
    project_id: str = ""
    status: str
    resolution: str = Field(default="", max_length=4000)
    ref: str = Field(default="", max_length=300)


def _change_project(account: dict, project_id: str) -> dict:
    """The project, and whether this account may act on its change requests.
    A client account gets nothing: these are the team's own notes."""
    if account["role"] == "client":
        raise HTTPException(403, "Change requests are for the delivery team.")
    project = _readable_project(account, project_id)
    role = next((p["role"] for p in projects_for(account) if p["id"] == project), "")
    if role == "client":
        raise HTTPException(403, "Change requests are for the delivery team.")
    # Both halves, and the account role is the half that was missing. Everybody
    # internal is `reviewer` on a project by default, so the project role alone
    # would let a pm — whose whole job is to watch this decision being made —
    # make it. An administrator settles anything; everybody else needs the
    # account role to permit it *and* a reviewer's standing on this project.
    return {"project": project,
            # Carried out so the per-request check does not have to look it up
            # again — and so the two can never disagree about which project role
            # they are reasoning from.
            "role": role,
            "may_resolve": security.is_admin(account["role"])
                           or (security.may_settle(account["role"]) and role == "reviewer")}


def _clean_change(body: ChangeIn) -> dict:
    kind = body.target_kind.strip().lower()
    if kind not in CHANGE_KINDS:
        raise HTTPException(400, f"target_kind is one of {', '.join(CHANGE_KINDS)}.")
    options = [o.strip() for o in body.options if o and o.strip()]
    if any(len(o) > 1000 for o in options):
        raise HTTPException(400, "Keep each option under 1000 characters.")
    ticket = body.ticket.strip().lstrip("#")
    if ticket and not ticket.isdigit():
        raise HTTPException(400, "ticket is an OpenProject work package number.")

    # The side of the house, chosen if the filer said and defaulted from the
    # kind if not — the same starting position a verdict gets, from the same
    # map, for the same reason: a screen blocked on an endpoint is backend work
    # and only the person who found it knows that.
    #
    # An empty tag survives. `adr` and `other` have no honest default, so those
    # arrive unrouted, which is a state the page shows rather than a hole.
    tag = body.tag.strip().lower() or db.TAG_OF.get(kind, "")
    if tag and tag not in TAGS:
        raise HTTPException(400, f"tag is one of {', '.join(TAGS)}, or left out.")
    platform = body.platform.strip().upper()
    if platform and not _PLATFORM.match(platform):
        raise HTTPException(
            400, f"A platform is written P01, P04 and so on, not {body.platform!r}.")
    if platform and not tag:
        # A platform belongs to a side. Accepting one without the other would
        # make a request that matches a scope on neither half of the pair.
        raise HTTPException(
            400, "A platform needs a side with it — say tag as well.")

    return {
        "target_kind": kind, "target_id": body.target_id.strip(),
        "title": body.title.strip(), "problem": body.problem.strip(),
        "evidence": body.evidence.strip(), "options": options,
        "recommendation": body.recommendation.strip(),
        "blocking": bool(body.blocking), "ticket": ticket,
        "tag": tag, "platform": platform,
    }


_CHANGE_SELECT = (
    "SELECT c.*, r.name AS raised_by_name, r.email AS raised_by_email, "
    "s.name AS resolved_by_name, p.name AS picked_by_name "
    "FROM change_request c "
    "JOIN account r ON r.id = c.raised_by "
    "LEFT JOIN account s ON s.id = c.resolved_by "
    "LEFT JOIN account p ON p.id = c.picked_by"
)


def _change_row(row) -> dict:
    return {
        "id": f"CR-{row['number']:03d}",
        # The store's own id for this row, which is what the CSV round trip
        # matches on. `id` above is the name people say — CR-007 — and it is
        # **counted per project**, so two projects both have one; it cannot
        # identify a row on its own. Carried so the page's export can write the
        # same `id` column the service's does and be applied the same way.
        "rowId": row["id"],
        "number": row["number"],
        "project": row["project_id"],
        "target": {"kind": row["target_kind"], "id": row["target_id"]},
        "title": row["title"],
        "problem": row["problem"],
        "evidence": row["evidence"],
        "options": json.loads(row["options"] or "[]"),
        "recommendation": row["recommendation"],
        "blocking": bool(row["blocking"]),
        "ticket": row["external_key"],
        "status": row["status"],
        "raisedBy": row["raised_by_name"] or row["raised_by_email"],
        # Separately from the fallback above, because the CSV has a column for
        # each: a roster of who raised what is read by name, and the address is
        # what somebody searches when two people share one.
        "raisedByEmail": row["raised_by_email"],
        "raisedAt": row["raised_at"],
        "raisedVia": row["raised_via"],
        "tag": row["tag"],
        "platform": row["platform"],
        # What the pair says out loud, built here so the page, the file and any
        # report agree on the words.
        "slice": (f"{TAG_LABEL.get(row['tag'], row['tag'])}"
                  + (f" · {row['platform']}" if row["platform"] else " · all platforms"))
                 if row["tag"] else "",
        "pickedBy": row["picked_by_name"],
        "pickedAt": row["picked_at"],
        "resolution": row["resolution"],
        "resolvedRef": row["resolved_ref"],
        "resolvedBy": row["resolved_by_name"],
        "resolvedAt": row["resolved_at"],
    }


def _open_on_target(project: str, kind: str, target: str) -> list:
    rows = db.all_rows(
        _CHANGE_SELECT + " WHERE c.project_id = ? AND c.target_kind = ? AND c.target_id = ? "
        "AND c.status IN ('open', 'accepted') ORDER BY c.number",
        (project, kind, target),
    )
    return [_change_row(r) for r in rows]


def _file_change(project: str, fields: dict, account: dict, via: str) -> dict:
    # The number and the row in one statement, so two filings at once cannot
    # take the same number.
    with db.cursor(commit=True) as cur:
        cur.execute(
            "INSERT INTO change_request (project_id, number, target_kind, target_id, title, "
            "problem, evidence, options, recommendation, blocking, external_key, status, "
            "raised_by, raised_at, raised_via, tag, platform) "
            "SELECT ?, COALESCE(MAX(number), 0) + 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'open', ?, ?, ?, ?, ? "
            "FROM change_request WHERE project_id = ?",
            (project, fields["target_kind"], fields["target_id"], fields["title"],
             fields["problem"], fields["evidence"], json.dumps(fields["options"]),
             fields["recommendation"], int(fields["blocking"]), fields["ticket"],
             account["id"], security.stamp(), via,
             fields.get("tag", ""), fields.get("platform", ""), project),
        )
        new_id = cur.lastrowid
    return _change_row(db.one(_CHANGE_SELECT + " WHERE c.id = ?", (new_id,)))


# ── whose change request is it ───────────────────────────────────────
#
# A request carries a slice — a side of the house and a platform within it —
# and `scope` says who owns which slice. Putting the two together is how a
# request finds the lead whose queue it belongs in.
#
# **Seeing is not acting, and the split is the whole point of the role.** A team
# lead reads every request on the project, because a lead who cannot see what is
# happening outside their platform cannot spot the thing that is about to land
# on it. What the slice decides is narrower: which ones they may pick up, which
# ones they may settle, and which ones will be counted against them.

# How long a request may sit with nobody having taken it on. Two days, and the
# escalation is a query rather than a job: "open, unpicked, older than this" is
# answerable at any moment from the rows themselves, so there is no scheduler to
# install, no tick to miss, and no stored notification to go stale when somebody
# picks the request up a minute after it fired.
PICK_SLA_DAYS = 2


def _scopes_of(account_id: int, project: str) -> list:
    return db.all_rows(
        "SELECT tag, platform FROM scope WHERE account_id = ? AND project_id = ?",
        (account_id, project))


def _in_scope(scopes: list, tag: str, platform: str) -> bool:
    """Whether a slice falls inside any of these grants.

    A grant with no platform is the whole of that side, and it covers a platform
    that did not exist when the grant was made — which is the reason the column
    is nullable rather than a row per platform.

    An untagged request is in nobody's scope, and that is correct rather than
    unfortunate: nobody has said whose it is, so nobody is quietly on the hook
    for it. It shows up in the unrouted list instead.
    """
    if not tag:
        return False
    for row in scopes:
        if row["tag"] != tag:
            continue
        if row["platform"] is None or row["platform"] == platform:
            return True
    return False


def _may_pick(account: dict, scopes: list, row) -> bool:
    """Whether this account may take this request on.

    An administrator may pick anything, because somebody has to be able to when
    the lead is away and because they are whole rather than scoped. A lead may
    pick what is theirs. Nobody else picks at all: taking a request on is a
    statement that you are going to deal with it.
    """
    if security.is_admin(account["role"]):
        return True
    if account["role"] != "lead":
        return False
    return _in_scope(scopes, row["tag"], row["platform"])


def _may_settle_change(account: dict, project_role: str, scopes: list, row) -> bool:
    """Whether this account may accept, reject or complete this request.

    An administrator settles anything. A lead settles their own slice — that is
    what "approvals, per platform" means. A reviewer settles anything on the
    project, as they always could: narrowing that would take a capability away
    from the people doing the reviewing today, which is a different decision
    from giving leads one.
    """
    if security.is_admin(account["role"]):
        return True
    if not security.may_settle(account["role"]) or project_role != "reviewer":
        return False
    if account["role"] == "lead":
        return _in_scope(scopes, row["tag"], row["platform"])
    return True


def _overdue_before() -> str:
    """The stamp a request must have been raised before to count as overdue.

    Compared as text, which is exact rather than a shortcut: security.stamp()
    writes one fixed-width ISO 8601 form in UTC, and for that form text order is
    time order.
    """
    return security.stamp(security.now() - timedelta(days=PICK_SLA_DAYS))


@app.post("/api/changes/{number}/pick")
def pick_change(number: str, body: FileIn, account: dict = Depends(require_account)):
    """Take a change request on. Says whose it is; says nothing about the answer.

    Picking and settling are separate acts on purpose, and a request can sit
    picked and unsettled for a fortnight without that being a contradiction —
    that is what being worked on looks like. What picking stops is the two-day
    escalation, because the thing being escalated is that nobody has looked.
    """
    scope = _change_project(account, body.project_id)
    row = db.one("SELECT * FROM change_request WHERE project_id = ? AND number = ?",
                 (scope["project"], _change_number(number)))
    if not row:
        raise HTTPException(404, f"No {number} in this project.")
    if row["status"] != "open":
        raise HTTPException(
            409, f"{number} is {row['status']}, not open. There is nothing left to take on.")

    scopes = _scopes_of(account["id"], scope["project"])
    if not _may_pick(account, scopes, row):
        raise HTTPException(403, (
            f"{number} is not in your platforms."
            if account["role"] == "lead" else
            "Only a team lead on that platform, or an admin, takes a change request on."))

    if row["picked_by"] and row["picked_by"] != account["id"]:
        holder = db.one("SELECT name, email FROM account WHERE id = ?", (row["picked_by"],))
        raise HTTPException(409, (
            f"{number} was taken on by {holder['name'] or holder['email']}. "
            f"They can hand it back, or an admin can."))

    db.write("UPDATE change_request SET picked_by = ?, picked_at = ? WHERE id = ?",
             (account["id"], security.stamp(), row["id"]))
    return {"ok": True, "change": _change_row(db.one(_CHANGE_SELECT + " WHERE c.id = ?", (row["id"],)))}


@app.post("/api/changes/{number}/unpick")
def unpick_change(number: str, body: FileIn, account: dict = Depends(require_account)):
    """Hand one back. The person holding it, or an administrator.

    The clock starts again from where it was — `raised_at` is what the
    escalation measures from and it does not move, so a request handed back
    after three days is overdue the moment it is handed back rather than getting
    another two days of quiet.
    """
    scope = _change_project(account, body.project_id)
    row = db.one("SELECT * FROM change_request WHERE project_id = ? AND number = ?",
                 (scope["project"], _change_number(number)))
    if not row:
        raise HTTPException(404, f"No {number} in this project.")
    if not row["picked_at"]:
        raise HTTPException(409, f"Nobody has taken {number} on.")
    if row["picked_by"] != account["id"] and not security.is_admin(account["role"]):
        raise HTTPException(403, "Only whoever took it on can hand it back, or an admin.")

    db.write("UPDATE change_request SET picked_by = NULL, picked_at = NULL WHERE id = ?",
             (row["id"],))
    return {"ok": True, "change": _change_row(db.one(_CHANGE_SELECT + " WHERE c.id = ?", (row["id"],)))}


@app.get("/api/changes/overdue")
def overdue_changes(project_id: str = Query(default=""),
                    reader: dict = Depends(require_reader)):
    """Every open request nobody has taken on within two days.

    **This is the escalation.** There is no notification to send and none
    stored: the question is answered from the rows every time it is asked, so a
    request picked up a minute after it tipped over stops being on this list
    immediately, and a service that was down for a day does not miss anything.

    A reader's, which is where "the super admin must be told" lands — an owner
    is an administrator, and an admin seeing it too is right rather than a leak:
    they are the ones who can reassign a platform. A pm reads it and can
    reassign nothing, which is oversight working as intended: the list is the
    thing they are meant to be asking about in the stand-up.
    """
    project = _readable_project(reader, project_id)
    rows = db.all_rows(
        _CHANGE_SELECT + " WHERE c.project_id = ? AND c.status = 'open' "
        "AND c.picked_at IS NULL AND c.raised_at < ? ORDER BY c.raised_at",
        (project, _overdue_before()))

    # Who should have taken each one, so the list is actionable rather than a
    # complaint. An unrouted request names nobody, and that is the answer: it is
    # waiting on somebody saying whose it is.
    out = []
    for row in rows:
        holders = db.all_rows(
            "SELECT a.id, a.name, a.email FROM scope s JOIN account a ON a.id = s.account_id "
            "WHERE s.project_id = ? AND s.tag = ? AND (s.platform IS NULL OR s.platform = ?) "
            "AND a.active = 1 AND a.role = 'lead'",
            (project, row["tag"], row["platform"]))
        out.append({
            **_change_row(row),
            "waitingDays": _days_since(row["raised_at"]),
            "shouldBe": [{"id": h["id"], "name": h["name"] or h["email"]} for h in holders],
        })
    return {"project": project, "afterDays": PICK_SLA_DAYS, "total": len(out), "items": out}


def _days_since(stamp: str) -> int:
    try:
        return max(0, (security.now() - security.parse(stamp)).days)
    except (ValueError, TypeError):
        return 0


@app.get("/api/changes")
def list_changes(project_id: str = Query(default=""), status: str = Query(default=""),
                 target_kind: str = Query(default=""), target_id: str = Query(default=""),
                 ticket: str = Query(default=""), account: dict = Depends(require_account)):
    """The project's change requests, newest first, narrowed by what is given."""
    scope = _change_project(account, project_id)
    where, args = ["c.project_id = ?"], [scope["project"]]
    if status:
        wanted = [s.strip() for s in status.split(",") if s.strip()]
        if any(s not in CHANGE_STATUSES for s in wanted):
            raise HTTPException(400, f"status is one or more of {', '.join(CHANGE_STATUSES)}.")
        where.append(f"c.status IN ({', '.join('?' for _ in wanted)})")
        args += wanted
    if target_kind:
        where.append("c.target_kind = ?"); args.append(target_kind.strip().lower())
    if target_id:
        where.append("c.target_id = ?"); args.append(target_id.strip())
    if ticket:
        where.append("c.external_key = ?"); args.append(ticket.strip().lstrip("#"))
    rows = db.all_rows(_CHANGE_SELECT + " WHERE " + " AND ".join(where) + " ORDER BY c.number DESC",
                       tuple(args))

    # Every request, for everybody who may read them — a lead sees the whole
    # project, which is the point of the role. What the slice decides is marked
    # per row rather than filtered out, so "mine" is a lens and never a wall.
    scopes = _scopes_of(account["id"], scope["project"])
    items = []
    for row in rows:
        item = _change_row(row)
        item["mine"] = _in_scope(scopes, row["tag"], row["platform"])
        item["mayPick"] = row["status"] == "open" and _may_pick(account, scopes, row)
        item["maySettle"] = _may_settle_change(account, scope["role"], scopes, row)
        items.append(item)

    counts = {s: 0 for s in CHANGE_STATUSES}
    for row in db.all_rows("SELECT status, COUNT(*) AS n FROM change_request WHERE project_id = ? "
                           "GROUP BY status", (scope["project"],)):
        counts[row["status"]] = row["n"]

    # The two figures the escalation is about, counted over the whole project
    # rather than over what the filters left — a filtered-away overdue request
    # is still overdue.
    waiting = db.one(
        "SELECT COUNT(*) AS n FROM change_request WHERE project_id = ? "
        "AND status = 'open' AND picked_at IS NULL", (scope["project"],))["n"]
    overdue = db.one(
        "SELECT COUNT(*) AS n FROM change_request WHERE project_id = ? "
        "AND status = 'open' AND picked_at IS NULL AND raised_at < ?",
        (scope["project"], _overdue_before()))["n"]
    unrouted = db.one(
        "SELECT COUNT(*) AS n FROM change_request WHERE project_id = ? "
        "AND status = 'open' AND tag = ''", (scope["project"],))["n"]

    return {"project": scope["project"], "mayResolve": scope["may_resolve"],
            "total": len(items), "counts": counts,
            "unpicked": waiting, "overdue": overdue, "unrouted": unrouted,
            "afterDays": PICK_SLA_DAYS, "items": items}


def _change_number(value: str) -> int:
    text = value.strip().upper().removeprefix("CR-").removeprefix("CR")
    if not text.isdigit():
        raise HTTPException(400, "A change request is named CR-<number>.")
    return int(text)


@app.get("/api/changes/{number}")
def read_change(number: str, project_id: str = Query(default=""),
                account: dict = Depends(require_account)):
    scope = _change_project(account, project_id)
    row = db.one(_CHANGE_SELECT + " WHERE c.project_id = ? AND c.number = ?",
                 (scope["project"], _change_number(number)))
    if not row:
        raise HTTPException(404, f"No {number} in this project.")
    return {"found": True, "change": _change_row(row), "mayResolve": scope["may_resolve"]}


@app.post("/api/changes")
def raise_change(body: ChangeIn, account: dict = Depends(require_account)):
    """Raise one from the viewer: the person is the one writing it, so no draft."""
    scope = _change_project(account, body.project_id)
    return {"ok": True, "change": _file_change(scope["project"], _clean_change(body), account, "viewer")}


@app.post("/api/changes/drafts")
def draft_change(body: ChangeIn, account: dict = Depends(require_account)):
    """
    Keep a change request for the person to agree to. **Files nothing.** Says
    which open ones already cover the same artefact, so a duplicate is caught
    before it is filed.
    """
    scope = _change_project(account, body.project_id)
    fields = _clean_change(body)
    code = security.new_token()
    now = security.now()
    db.write(
        "INSERT INTO change_draft (token_hash, account_id, project_id, payload, created_at, expires_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (security.token_hash(code), account["id"], scope["project"], json.dumps(fields),
         security.stamp(now), security.stamp(now + timedelta(minutes=DRAFT_MINUTES))),
    )
    return {
        "draft": code,
        "preview": fields,
        "alreadyOpen": _open_on_target(scope["project"], fields["target_kind"], fields["target_id"]),
        "expiresInMinutes": DRAFT_MINUTES,
        "note": "Nothing has been filed. Show this to the person; file it only after they say yes. "
                "If one of alreadyOpen says the same thing, point to it instead.",
    }


@app.post("/api/changes/drafts/{code}/file")
def file_draft(code: str, body: FileIn, account: dict = Depends(require_account)):
    """File a draft the person agreed to. One use."""
    row = db.one("SELECT * FROM change_draft WHERE token_hash = ?", (security.token_hash(code),))
    if not row or row["account_id"] != account["id"]:
        raise HTTPException(404, "No such draft. Draft the change request first.")
    if row["filed_at"]:
        raise HTTPException(409, "That draft has already been filed.")
    if security.expired(row["expires_at"]):
        raise HTTPException(410, f"That draft is more than {DRAFT_MINUTES} minutes old. Draft it again.")
    scope = _change_project(account, body.project_id or row["project_id"])
    if scope["project"] != row["project_id"]:
        raise HTTPException(400, "That draft was made for another ADAM project.")
    if not db.change("UPDATE change_draft SET filed_at = ? WHERE id = ? AND filed_at IS NULL",
                     (security.stamp(), row["id"])):
        raise HTTPException(409, "That draft has already been filed.")
    return {"ok": True, "change": _file_change(row["project_id"], json.loads(row["payload"]), account, "claude")}


@app.post("/api/changes/{number}/resolve")
def resolve_change(number: str, body: ResolveIn, account: dict = Depends(require_account)):
    """
    Accept, reject, mark done, or reopen. An admin or a reviewer on the
    project, or the team lead whose platform it is; not the person who raised
    it, unless they are an admin - somebody else has to agree the package is
    wrong.

    **Two checks, and they answer different questions.** `may_resolve` on the
    project says whether this account settles anything here at all, and it is
    what the page draws its controls from. `_may_settle_change` says whether
    they settle *this one*, which for a lead depends on the slice it carries —
    and only the second can be the rule, because the first cannot see the
    request.
    """
    scope = _change_project(account, body.project_id)
    if not scope["may_resolve"]:
        raise HTTPException(403, "Only an admin or a reviewer on this project can settle a change request.")
    status = body.status.strip().lower()
    if status not in CHANGE_STATUSES:
        raise HTTPException(400, f"status is one of {', '.join(CHANGE_STATUSES)}.")
    row = db.one("SELECT * FROM change_request WHERE project_id = ? AND number = ?",
                 (scope["project"], _change_number(number)))
    if not row:
        raise HTTPException(404, f"No {number} in this project.")
    scopes = _scopes_of(account["id"], scope["project"])
    if not _may_settle_change(account, scope["role"], scopes, row):
        where = (f"{TAG_LABEL.get(row['tag'], row['tag'])}"
                 + (f" · {row['platform']}" if row["platform"] else "")) if row["tag"]             else "not routed to a platform yet"
        raise HTTPException(403, (
            f"{number} is {where}, which is not one of yours. A team lead "
            f"settles their own platforms; an admin settles anything."))
    if (row["raised_by"] == account["id"] and not security.is_admin(account["role"])
            and status in ("accepted", "rejected")):
        raise HTTPException(403, "Somebody other than the person who raised it has to accept or reject it.")
    note = body.resolution.strip()
    if status == "rejected" and not note:
        raise HTTPException(400, "Say why it is rejected - that is what the person who raised it reads.")
    if status == "open":
        db.write("UPDATE change_request SET status = 'open', resolution = ?, resolved_ref = '', "
                 "resolved_by = NULL, resolved_at = NULL WHERE id = ?", (note, row["id"]))
    else:
        db.write("UPDATE change_request SET status = ?, resolution = ?, resolved_ref = ?, "
                 "resolved_by = ?, resolved_at = ? WHERE id = ?",
                 (status, note or row["resolution"], body.ref.strip() or row["resolved_ref"],
                  account["id"], security.stamp(), row["id"]))
    return {"ok": True, "change": _change_row(db.one(_CHANGE_SELECT + " WHERE c.id = ?", (row["id"],)))}


# ── which OpenProject project each ADAM project reads ────────────────

class PmsProjectIn(BaseModel):
    pms_project_id: int


_PROJECT_SELECT = (
    "SELECT p.id, p.name, p.active, p.pms_project_id, p.pms_identifier, p.pms_name, "
    "p.pms_set_at, a.email AS set_by_email FROM project p "
    "LEFT JOIN account a ON a.id = p.pms_set_by"
)


def _project_row(row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "active": bool(row["active"]),
        "openproject": None if row["pms_project_id"] is None else {
            "id": row["pms_project_id"],
            "identifier": row["pms_identifier"],
            "name": row["pms_name"],
            "url": f"{DEFAULT_PMS}/projects/{row['pms_identifier']}" if row["pms_identifier"] else "",
        },
        "setAt": row["pms_set_at"],
        "setBy": row["set_by_email"],
    }


@app.get("/api/pms/projects")
def list_pms_projects(admin: dict = Depends(require_admin)):
    """Every ADAM project and the OpenProject project each one reads."""
    rows = db.all_rows(f"{_PROJECT_SELECT} ORDER BY p.id")
    return {"endpoint": DEFAULT_PMS, "projects": [_project_row(r) for r in rows]}


@app.get("/api/pms/available")
def available_pms_projects(admin: dict = Depends(require_admin)):
    """
    The OpenProject projects there are to choose from, read with the admin's
    own token, so the list is what that admin can see there.
    """
    endpoint, token = _pms_for(admin["id"])
    try:
        found = openproject.projects(endpoint, token)
    except (openproject.Blocked, openproject.Refused) as exc:
        raise HTTPException(502, str(exc))
    return {"endpoint": endpoint, "projects": found}


@app.put("/api/pms/projects/{project_id}")
def set_pms_project(project_id: str, body: PmsProjectIn,
                    admin: dict = Depends(require_admin)):
    """
    Choose the OpenProject project an ADAM project reads.

    **Looked up before it is kept**, with the admin's token: the number must be
    a project that exists and the admin can see, and the identifier and name
    stored beside it are the ones OpenProject gave, not ones typed in.
    """
    if not db.one("SELECT id FROM project WHERE id = ?", (project_id,)):
        raise HTTPException(404, f"No ADAM project called '{project_id}'.")
    endpoint, token = _pms_for(admin["id"])
    try:
        found = {p["id"]: p for p in openproject.projects(endpoint, token)}
    except (openproject.Blocked, openproject.Refused) as exc:
        raise HTTPException(502, str(exc))
    chosen = found.get(body.pms_project_id)
    if not chosen:
        raise HTTPException(
            400, f"OpenProject has no project #{body.pms_project_id} that your token can see.")
    db.change(
        "UPDATE project SET pms_project_id = ?, pms_identifier = ?, pms_name = ?, "
        "pms_set_at = ?, pms_set_by = ? WHERE id = ?",
        (chosen["id"], chosen["identifier"], chosen["name"], security.stamp(),
         admin["id"], project_id),
    )
    row = db.one(f"{_PROJECT_SELECT} WHERE p.id = ?", (project_id,))
    return {"ok": True, "project": _project_row(row)}


@app.delete("/api/pms/projects/{project_id}")
def clear_pms_project(project_id: str, admin: dict = Depends(require_admin)):
    """
    Unchoose it. The work routes then refuse for this project until somebody
    chooses again. `pms_set_at` is kept, so the startup migration knows a
    person made this choice and does not fill the default back in.
    """
    moved = db.change(
        "UPDATE project SET pms_project_id = NULL, pms_identifier = '', pms_name = '', "
        "pms_set_at = ?, pms_set_by = ? WHERE id = ?",
        (security.stamp(), admin["id"], project_id),
    )
    if not moved:
        raise HTTPException(404, f"No ADAM project called '{project_id}'.")
    return {"ok": True}


# ── mentions ────────────────────────────────────────────

# @ followed by the local part of an address, or a whole address. The local
# part is the handle because `email_folded` is unique, so it identifies exactly
# one person and needs no second namespace that could drift out of step with
# the roster. Names are not matched: two people called Chris is normal, and a
# notification that goes to the wrong Chris is worse than one that does not go.
MENTION = re.compile(r"@([A-Za-z0-9._%+-]+(?:@[A-Za-z0-9.-]+\.[A-Za-z]{2,})?)")


def mentioned_in(note: str) -> list:
    """The accounts a note names, as ids. Unknown handles are ignored rather
    than refused: a note is prose, and an address in it that happens not to be
    an account is a sentence, not a mistake to reject a verdict over."""
    handles = {h.lower() for h in MENTION.findall(note or "")}
    if not handles:
        return []
    rows = db.all_rows("SELECT id, email_folded FROM account WHERE active = 1")
    hit = []
    for row in rows:
        folded = row["email_folded"]
        if folded in handles or folded.split("@")[0] in handles:
            hit.append(row["id"])
    return hit


# ── what is standing against you right now ───────────────────────────
#
# The bell's other half. A mention is an **event**: somebody named you at a
# moment, it is stored, and marking it read is meaningful because the moment has
# passed. What is below is not that. These are **conditions** — things that are
# true of the store as it is, this second — and they are computed on every read
# rather than written down.
#
# That difference decides everything about how they behave, and it is worth
# being explicit because a table would have been the obvious thing to build:
#
#   Nothing is sent, so nothing has to be retracted. A change request picked up
#   a minute after it tipped over stops being overdue on the next read, and no
#   row anywhere has to be found and cleared.
#
#   Nothing is scheduled, so nothing can be missed. A service that was down for
#   a day comes back knowing exactly what is overdue; a job that should have run
#   at midnight does not.
#
#   **They cannot be marked read**, and that is the point rather than a
#   limitation. An escalation you can dismiss is one that gets dismissed. The
#   only way to clear "nobody has taken this on" is for somebody to take it on.
#
# The cost is that there is no record of having been told, which matters for an
# event and not for a condition: "you were notified on Tuesday" is not a thing
# anybody needs to know about a request that is still sitting there today.


def _alert(kind: str, severity: str, title: str, detail: str, href: str, items: list) -> dict:
    return {
        "kind": kind,
        "severity": severity,
        "title": title,
        "detail": detail,
        "href": href,
        "count": len(items),
        # A handful, named. The count above is always the true one; this is so
        # the panel can say *which* rather than only how many, and a bell that
        # lists two hundred rows is a bell nobody opens twice.
        "items": items[:5],
    }


def _change_brief(row) -> dict:
    return {
        "id": f"CR-{row['number']:03d}",
        "title": row["title"],
        "days": _days_since(row["raised_at"]),
        "slice": (f"{TAG_LABEL.get(row['tag'], row['tag'])}"
                  + (f" · {row['platform']}" if row["platform"] else "")) if row["tag"] else "",
    }


@app.get("/api/alerts")
def alerts(account: dict = Depends(require_account)):
    """Conditions standing against this account, across every project they read.

    Who is told what follows the role, and the two are different questions:

      An **administrator or a pm** — which includes the owner — is told when a
      request has waited more than the window with nobody taking it on, and when
      one has no side of the house at all. Both are failures of routing
      rather than of work. **This is where "the super admin must be notified"
      lands.** An admin seeing it too is right rather than a leak: they are the
      other people who can reassign a platform. A pm is told and can reassign
      nothing — being told is the point of the role, and a bell that rang only
      for people who could fix it would never reach the person whose job is to
      ask why it is still ringing.

      A **team lead** is told about their own platforms only — open requests in
      their slices that nobody has taken. They can read every request on the
      project, and being *told* about all of them would make the bell useless
      inside a week. Seeing and being notified are separate, and this is the
      half that is narrow.

    Everybody else gets nothing here, which is not the same as being shut out:
    the changes page shows all of this to anybody who may read it. A bell is for
    what is yours to do something about.
    """
    out = []
    projects = [p["id"] for p in projects_for(account)]
    if not projects:
        return {"alerts": [], "total": 0}

    holes = ",".join("?" * len(projects))
    cutoff = _overdue_before()

    if security.may_oversee(account["role"]):
        late = db.all_rows(
            f"SELECT * FROM change_request WHERE project_id IN ({holes}) "
            f"AND status = 'open' AND picked_at IS NULL AND raised_at < ? "
            f"ORDER BY raised_at",
            (*projects, cutoff))
        if late:
            out.append(_alert(
                "overdue-change", "high",
                f"{len(late)} change request{'' if len(late) == 1 else 's'} "
                f"nobody has taken on",
                f"Open for more than {PICK_SLA_DAYS} days with no team lead on "
                f"{'it' if len(late) == 1 else 'them'}. Reassign the platform, or "
                f"take {'it' if len(late) == 1 else 'them'} on.",
                "/changes.html?status=open",
                [_change_brief(r) for r in late]))

        loose = db.all_rows(
            f"SELECT * FROM change_request WHERE project_id IN ({holes}) "
            f"AND status = 'open' AND tag = '' ORDER BY raised_at",
            tuple(projects))
        if loose:
            out.append(_alert(
                "unrouted-change", "warn",
                f"{len(loose)} change request{'' if len(loose) == 1 else 's'} "
                f"with no side of the house",
                "Nobody owns these, because nothing says whether they are "
                "frontend or backend. They will never reach a team lead until "
                "somebody says.",
                "/changes.html?status=open",
                [_change_brief(r) for r in loose]))

    elif account["role"] == "lead":
        # Their slices, in one pass per project, because `scope` is per project
        # and a lead may hold platforms on more than one.
        mine = []
        for project in projects:
            scopes = _scopes_of(account["id"], project)
            if not scopes:
                continue
            for row in db.all_rows(
                "SELECT * FROM change_request WHERE project_id = ? "
                "AND status = 'open' AND picked_at IS NULL ORDER BY raised_at",
                    (project,)):
                if _in_scope(scopes, row["tag"], row["platform"]):
                    mine.append(row)
        if mine:
            overdue = [r for r in mine if r["raised_at"] < cutoff]
            out.append(_alert(
                "unpicked-in-scope", "high" if overdue else "warn",
                f"{len(mine)} change request{'' if len(mine) == 1 else 's'} "
                f"on your platforms",
                (f"{len(overdue)} of them {'has' if len(overdue) == 1 else 'have'} "
                 f"waited more than {PICK_SLA_DAYS} days. "
                 if overdue else "")
                + "Nobody has taken them on yet.",
                "/changes.html?status=open",
                [_change_brief(r) for r in mine]))

    return {"alerts": out, "total": sum(a["count"] for a in out)}


@app.get("/api/mentions")
def mentions(account: dict = Depends(require_account)):
    """Every time somebody named you, newest first.

    Carries the note and the artefact rather than an id to go and fetch,
    because a notification that requires a second request to become legible is
    one that gets rendered as "you have 3 notifications" and never read.
    """
    rows = db.all_rows(
        """SELECT m.id, m.created_at AS at, m.seen_at,
                  v.id AS verdict_id, v.target_kind, v.target_id, v.verdict,
                  v.note, v.audience,
                  a.name AS by, a.email AS by_email
             FROM mention m
             JOIN verdict v ON v.id = m.verdict_id
             JOIN account a ON a.id = v.account_id
            WHERE m.account_id = ?
            ORDER BY m.id DESC
            LIMIT 200""",
        (account["id"],),
    )
    items = [dict(r) for r in rows]
    return {"mentions": items, "unseen": sum(1 for i in items if not i["seen_at"])}


@app.post("/api/mentions/seen")
def mentions_seen(account: dict = Depends(require_account)):
    """Mark everything addressed to you as read. All of it, rather than one at
    a time: the list is short and the gesture people actually make is closing
    the panel, not ticking rows."""
    db.write(
        "UPDATE mention SET seen_at = ? WHERE account_id = ? AND seen_at IS NULL",
        (security.stamp(), account["id"]),
    )
    return {"ok": True, "unseen": 0}


@app.get("/api/mentionable")
def mentionable(account: dict = Depends(require_account)):
    """Who can be named, for the picker. Active accounts only — offering
    somebody who has been disabled invites a note addressed to nobody."""
    rows = db.all_rows(
        "SELECT id, name, email, role FROM account WHERE active = 1 ORDER BY name, email"
    )
    return {"people": [
        {**dict(r), "handle": r["email"].split("@")[0].lower()} for r in rows
    ]}


# ── verdicts ─────────────────────────────────────────────────────────

@app.post("/api/validation")
def record(body: VerdictIn, account: dict = Depends(require_voice)):
    if body.verdict not in VERDICTS:
        raise HTTPException(400, f"A verdict is one of {', '.join(VERDICTS)}.")
    if body.target_kind not in TARGET_KINDS:
        raise HTTPException(400, f"A target is one of {', '.join(TARGET_KINDS)}.")
    if not body.target_id.strip():
        raise HTTPException(400, "A verdict needs something to be about.")
    # A caller that says nothing gets the layer its kind implies, so a row is
    # never left without one — an unlabelled verdict would be invisible to every
    # per-layer count and look like it had never happened.
    layer = body.layer.strip() or db.LAYER_OF.get(body.target_kind, "")
    if layer and layer not in LAYERS:
        raise HTTPException(400, f"A layer is one of {', '.join(LAYERS)}.")
    tag = body.tag.strip() or db.TAG_OF.get(body.target_kind, "")
    if tag and tag not in TAGS:
        raise HTTPException(400, f"A tag is one of {', '.join(TAGS)}.")

    audience = audience_of(account)
    row_id = db.write(
        """INSERT INTO verdict
             (target_kind, target_id, layer, tag, audience, verdict, note,
              account_id, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            body.target_kind, body.target_id.strip(), layer, tag, audience,
            body.verdict, body.note.strip(), account["id"], security.stamp(),
        ),
    )
    # Who the note names. Written as rows now rather than parsed on every read:
    # the note is prose, people get renamed, and a mention that stopped
    # resolving later would be a notification that silently never arrives.
    #
    # Naming yourself is dropped. It is usually a sentence about your own
    # address rather than a note to yourself, and either way a notification
    # about something you just typed is noise.
    named = [i for i in mentioned_in(body.note) if i != account["id"]]
    for who in named:
        db.write(
            "INSERT INTO mention (verdict_id, account_id, created_at) VALUES (?, ?, ?)",
            (row_id, who, security.stamp()),
        )

    return {"id": row_id, "ok": True, "audience": audience, "mentioned": len(named)}


@app.get("/api/validation/{target_kind}/{target_id:path}")
def history(target_kind: str, target_id: str):
    """Every verdict on one artefact, newest first, and the current one for
    each audience.

    `current` stays the team's, because everything that already reads this key
    means the team's — and a field that quietly changed meaning the first time
    a client reviewed something would be worse than a new one. The client's own
    standing verdict is `client_current`, and the history holds both, marked.
    """
    rows = db.all_rows(
        """SELECT v.id, v.target_kind, v.target_id, v.layer, v.tag, v.audience,
                  v.verdict, v.note,
                  v.created_at AS at, a.name AS by, a.email AS by_email,
                  v.done_at, v.done_response, d.name AS done_by_name,
                  v.sent_back_at, v.sent_back_note, k.name AS sent_back_by_name
             FROM verdict v
             JOIN account a ON a.id = v.account_id
             LEFT JOIN account d ON d.id = v.done_by
             LEFT JOIN account k ON k.id = v.sent_back_by
            WHERE v.target_kind = ? AND v.target_id = ?
            ORDER BY v.id DESC""",
        (target_kind, target_id),
    )
    items = [VerdictOut(**dict(r)) for r in rows]
    newest = lambda who: next((i for i in items if i.audience == who), None)
    return {
        "current": newest("internal"),
        "client_current": newest("client"),
        "history": items,
    }


@app.get("/api/validation")
def summary(target_kind: Optional[str] = None, audience: str = "internal"):
    """The current verdict on everything judged so far — one row per artefact,
    which is what a sign-off report is made of."""
    # One row per artefact *per audience*. Grouping by the artefact alone was
    # right while only the team could write: it is the newest row that stands,
    # and there was only ever one review. With a client reviewing too, that
    # query would hand back whichever of the two happened to be typed last and
    # call it the verdict — a client's approval standing in for the team's on
    # something the team had rejected. Two rows, and the caller says which it
    # wants.
    sql = """
        SELECT v.target_kind, v.target_id, v.layer, v.tag, v.audience, v.verdict, v.note,
               v.created_at AS at, a.name AS by, a.email AS by_email, v.id,
               v.done_at, v.done_response, d.name AS done_by_name,
               v.sent_back_at, v.sent_back_note, k.name AS sent_back_by_name
          FROM verdict v
          JOIN account a ON a.id = v.account_id
          LEFT JOIN account d ON d.id = v.done_by
          LEFT JOIN account k ON k.id = v.sent_back_by
         WHERE v.id IN (
                 SELECT MAX(id) FROM verdict GROUP BY target_kind, target_id, audience)
    """
    args: list = []
    if target_kind:
        sql += " AND v.target_kind = ?"
        args.append(target_kind)
    # "all" is spelled out rather than being what an empty value happens to
    # mean, so a caller that forgets the parameter gets the team's review —
    # which is what every existing caller meant by asking at all.
    if audience != "all":
        sql += " AND v.audience = ?"
        args.append(audience)
    sql += " ORDER BY v.target_kind, v.target_id"

    rows = db.all_rows(sql, tuple(args))
    counts: dict = {}
    for r in rows:
        counts.setdefault(r["target_kind"], {}).setdefault(r["verdict"], 0)
        counts[r["target_kind"]][r["verdict"]] += 1
    return {"audience": audience, "counts": counts,
            "items": [VerdictOut(**dict(r)) for r in rows]}


@app.get("/api/verdicts")
def verdicts(account: dict = Depends(require_account)):
    """Every verdict ever recorded, newest first — not one row per artefact.

    The summary above answers "where does this stand", which is what a sign-off
    report needs. This answers "what has everyone been doing", which is a
    different question and cannot be derived from the first: a summary of
    current verdicts has already thrown away the disagreement, the revisions and
    the pace, and those are most of what tells you whether a review is going
    well.

    Signed in only. Who reviewed what, and how fast, is not public.
    """
    rows = db.all_rows(
        """SELECT v.id, v.target_kind, v.target_id, v.layer, v.tag, v.audience,
                  v.verdict, v.note,
                  v.created_at AS at, v.account_id,
                  a.name AS by, a.email AS by_email, a.role AS by_role, a.active AS by_active,
                  v.done_at, v.done_by, v.done_response, d.name AS done_by_name,
                  v.sent_back_at, v.sent_back_note, k.name AS sent_back_by_name
             FROM verdict v
             JOIN account a ON a.id = v.account_id
             LEFT JOIN account d ON d.id = v.done_by
             LEFT JOIN account k ON k.id = v.sent_back_by
            ORDER BY v.id DESC"""
    )
    people = db.all_rows(
        "SELECT id, email, name, role, active, created_at FROM account ORDER BY id"
    )
    return {
        "verdicts": [dict(r) for r in rows],
        "accounts": [dict(p) for p in people],
    }


@app.post("/api/verdicts/{verdict_id}/done")
def mark_done(verdict_id: int, body: DoneIn, account: dict = Depends(require_writer)):
    """Mark one verdict complete, or put it back.

    Not a new verdict and not an edit of the old one. A verdict is a thing
    somebody said at a time and stays as said; this records that the thing they
    asked for has since been done. Keeping them apart is what lets the review
    read as a worklist — "needs work, and it has been dealt with" is a different
    state from "approved", and collapsing the two would lose the fact that
    somebody had to go and fix it.

    Anybody who can record a verdict can mark one complete, including on
    somebody else's row: the person who fixes a thing is usually not the person
    who found it, and requiring the finder to come back and tick it is how a
    worklist stops being kept.
    """
    row = db.one("SELECT id, done_at FROM verdict WHERE id = ?", (verdict_id,))
    if not row:
        raise HTTPException(404, "No such verdict.")

    if body.done:
        # Closing says how. A bare "done" was the thing the tracker's own sheet
        # had already outgrown: five different answers all arriving as one word
        # tells nobody whether a thing was built, wired, answered or simply
        # agreed with.
        response = body.response.strip()
        if response and response not in RESPONSES:
            raise HTTPException(400, f"A response is one of {', '.join(RESPONSES)}.")
        db.write(
            "UPDATE verdict SET done_at = ?, done_by = ?, done_response = ? WHERE id = ?",
            (security.stamp(), account["id"], response, verdict_id),
        )
    else:
        db.write(
            "UPDATE verdict SET done_at = NULL, done_by = NULL, done_response = '' "
            "WHERE id = ?",
            (verdict_id,),
        )

    fresh = db.one(
        """SELECT v.done_at, v.done_response, d.name AS done_by_name
             FROM verdict v LEFT JOIN account d ON d.id = v.done_by
            WHERE v.id = ?""",
        (verdict_id,),
    )
    return {"id": verdict_id, **dict(fresh)}


@app.post("/api/verdicts/{verdict_id}/send-back")
def send_back(verdict_id: int, body: SendBackIn, account: dict = Depends(require_admin)):
    """Reject a completion, with a reason. Admin only.

    Somebody marked an item done; this says it is not. It is the other half of
    marking done, and without it the only answer to work that was not really
    finished is to reopen it silently — which tells whoever did it nothing, and
    so tends to produce the same thing again.

    **The note is required.** Everywhere else in this store a reason is
    encouraged and optional, because a verdict with no reason is still a
    verdict. This one is different: it is addressed to a specific person about
    a specific piece of work, and it is the only field that tells them what to
    do next.

    Admin only, unlike marking done, which anyone who can review may do. Anyone
    can say a thing is finished; deciding it is not is a call about somebody
    else's work, and that is narrower.

    Nothing is cleared. `done_at` stays where it was and this is written beside
    it, so the row keeps both the claim and the answer to it, and which one
    stands is whichever is later.
    """
    note = body.note.strip()
    if not note:
        raise HTTPException(400, "Say why it is being sent back — that is the whole of it.")

    row = db.one("SELECT id, done_at FROM verdict WHERE id = ?", (verdict_id,))
    if not row:
        raise HTTPException(404, "No such verdict.")
    if not row["done_at"]:
        raise HTTPException(
            400, "That has not been marked done, so there is no completion to reject.")

    db.write(
        "UPDATE verdict SET sent_back_at = ?, sent_back_by = ?, sent_back_note = ? WHERE id = ?",
        (security.stamp(), account["id"], note, verdict_id),
    )
    fresh = db.one(
        """SELECT v.sent_back_at, v.sent_back_note, k.name AS sent_back_by_name
             FROM verdict v LEFT JOIN account k ON k.id = v.sent_back_by
            WHERE v.id = ?""",
        (verdict_id,),
    )
    return {"id": verdict_id, **dict(fresh)}


@app.delete("/api/verdicts/{verdict_id}")
def discard(verdict_id: int, account: dict = Depends(require_account)):
    """Discard your own verdict.

    Verdicts are otherwise append-only, and that is deliberate: a row is a
    thing somebody said at a time, and rewriting it would lose the fact that
    they once thought otherwise. Changing your mind is a second row, not an
    edit of the first.

    This is the one exception, and it is narrow on purpose. It is not for
    withdrawing an opinion — that is what a later verdict is for — it is for a
    row that should never have existed: a mis-click, a test, a note typed into
    the wrong artefact. Those are not disagreements worth keeping, and leaving
    them in makes the register harder to read than the history is worth.

    **Your own only, and no exception for an admin.** An admin can disable an
    account and can read everything, and still cannot delete what somebody else
    said — because the moment that is possible, a register of who signed off on
    what stops being evidence of anything. A junk row from somebody who has
    left stays, and that is the cheaper of the two problems.
    """
    row = db.one("SELECT id, account_id FROM verdict WHERE id = ?", (verdict_id,))
    if not row:
        raise HTTPException(404, "No such verdict.")
    if row["account_id"] != account["id"]:
        raise HTTPException(403, "You can only discard a verdict you recorded yourself.")

    db.write("DELETE FROM verdict WHERE id = ?", (verdict_id,))
    return {"id": verdict_id, "discarded": True}


# ── taking a date range away as a file ───────────────────────────────

def _cell(value) -> str:
    """One CSV field, quoted the way the browser's export quotes one.

    Every field is quoted whether it needs to be or not, and an inner quote is
    doubled. That is not the shortest CSV that would parse — it is the same
    CSV the reviews page writes, and two exports in one product that disagree
    about what happens to a comma inside a note is a defect a reader finds
    halfway down a spreadsheet with the columns already shifted.
    """
    return '"' + ("" if value is None else str(value)).replace('"', '""') + '"'


def _day(value: Optional[str]) -> str:
    """The date half of a stored stamp.

    A slice rather than a parse: every stamp this store writes comes from
    security.stamp(), which is ISO 8601 in UTC, so the first ten characters are
    the date and nothing about a timezone can make them something else.
    """
    return (value or "")[:10]


def _settled(row) -> bool:
    """Whether a verdict counts as finished right now — the same reading
    validation.js exports as isSettled(), because the file and the screen
    disagreeing about what is done would be worse than either being wrong.

    Both stamps are kept rather than one being cleared, so this is a comparison
    and not a flag: marked done, sent back, marked done again. The comparison is
    on the strings, which is safe only because they are the one fixed-width ISO
    form security.stamp() writes — sortable as text is a property of that
    format, not of dates in general.
    """
    if not row["done_at"]:
        return False
    if not row["sent_back_at"]:
        return True
    return row["done_at"] > row["sent_back_at"]


# The columns, in order, and how a row of each table becomes one. Every header
# below matches the browser's export where the two overlap — see the label maps
# at the top of this file.

def _export_verdicts(clause: str, args: tuple):
    rows = db.all_rows(
        f"""SELECT v.id, v.target_kind, v.target_id, v.layer, v.tag, v.audience,
                   v.verdict, v.note, v.created_at,
                   a.name AS by, a.email AS by_email,
                   v.done_at, v.done_response, d.name AS done_by_name,
                   v.sent_back_at, v.sent_back_note
              FROM verdict v
              JOIN account a ON a.id = v.account_id
              LEFT JOIN account d ON d.id = v.done_by
             WHERE 1 = 1{clause}
             ORDER BY v.id""",
        args,
    )
    # `id` first, and it is not decoration. This file goes out, somebody fills
    # in the "our verdict" column and sends it back to be applied in bulk, and
    # without the id there is nothing in a row that identifies which verdict it
    # came from: (kind, artefact) has a row per audience and another row every
    # time somebody changed their mind, since the current verdict is the newest
    # one per target. Matching on the pair would either close the wrong row or
    # close several, and both are unrecoverable by re-uploading the right file.
    # First rather than last so it survives a reader deleting the columns they
    # do not care about from the right-hand end.
    header = [
        "id",
        "when", "date", "review", "layer", "lands on", "kind", "artefact",
        "verdict", "reviewer", "email", "status", "our verdict", "done on",
        "done by", "sent back because", "note",
    ]
    body = [
        [
            r["id"],
            r["created_at"], _day(r["created_at"]),
            AUDIENCE_LABEL.get(r["audience"], r["audience"]),
            LAYER_LABEL.get(r["layer"], r["layer"]),
            TAG_LABEL.get(r["tag"], r["tag"]),
            KIND_LABEL.get(r["target_kind"], r["target_kind"]),
            r["target_id"],
            VERDICT_LABEL.get(r["verdict"], r["verdict"]),
            r["by"], r["by_email"],
            "Done" if _settled(r) else "Sent back" if r["sent_back_at"] else "Open",
            RESPONSE_LABEL.get(r["done_response"], r["done_response"]),
            _day(r["done_at"]), r["done_by_name"] or "",
            r["sent_back_note"], r["note"],
        ]
        for r in rows
    ]
    return header, body


def _export_invites(clause: str, args: tuple):
    rows = db.all_rows(
        f"""SELECT i.email, i.role, i.created_at, i.expires_at,
                   i.redeemed_at, i.revoked_at, c.email AS invited_by
              FROM invite i
              LEFT JOIN account c ON c.id = i.created_by
             WHERE 1 = 1{clause}
             ORDER BY i.id""",
        args,
    )
    header = [
        "when", "date", "address", "role", "state", "expires on",
        "used on", "withdrawn on", "invited by",
    ]
    body = [
        [
            r["created_at"], _day(r["created_at"]), r["email"], r["role"],
            # The same four-way reading /api/invites gives the screen. Derived
            # in both places rather than stored, because it is three dates and a
            # clock, and a stored copy would be wrong the moment one expired.
            "redeemed" if r["redeemed_at"] else
            "revoked" if r["revoked_at"] else
            "expired" if security.expired(r["expires_at"]) else "open",
            _day(r["expires_at"]), _day(r["redeemed_at"]), _day(r["revoked_at"]),
            r["invited_by"] or "",
        ]
        for r in rows
    ]
    return header, body


def _export_accounts(clause: str, args: tuple):
    rows = db.all_rows(
        f"""SELECT a.name, a.email, a.role, a.active, a.created_at, a.last_seen_at,
                   (SELECT COUNT(*) FROM verdict v WHERE v.account_id = a.id) AS verdicts
              FROM account a
             WHERE 1 = 1{clause}
             ORDER BY a.id""",
        args,
    )
    header = [
        "when", "date", "name", "address", "role", "status", "verdicts",
        "last seen",
    ]
    body = [
        [
            r["created_at"], _day(r["created_at"]), r["name"], r["email"], r["role"],
            "active" if r["active"] else "disabled",
            r["verdicts"], _day(r["last_seen_at"]),
        ]
        for r in rows
    ]
    return header, body


def _export_changes(clause: str, args: tuple):
    """Every change request raised, with the three columns that settle one
    blank for somebody to fill in and send back. See /api/changes/import.

    Ordered by project then number, so the file reads the way CR-001, CR-002
    does on the page. Not by `c.id`, which is the matching key and interleaves
    two projects by whoever happened to file first.
    """
    rows = db.all_rows(
        f"""SELECT c.id, c.number, c.project_id, c.target_kind, c.target_id,
                   c.title, c.problem, c.evidence, c.options, c.recommendation,
                   c.blocking, c.external_key, c.status, c.raised_at,
                   c.raised_via, c.resolution, c.resolved_ref, c.resolved_at,
                   c.tag, c.platform, c.picked_at,
                   r.name AS raised_by_name, r.email AS raised_by_email,
                   s.name AS resolved_by_name, p.name AS picked_by_name
              FROM change_request c
              JOIN account r ON r.id = c.raised_by
              LEFT JOIN account s ON s.id = c.resolved_by
              LEFT JOIN account p ON p.id = c.picked_by
             WHERE 1 = 1{clause}
             ORDER BY c.project_id, c.number""",
        args,
    )
    # `id` first and `ref` second, and the pair is the whole of why this file
    # can be applied. `id` is the key — the database's own, unique across every
    # project — and it is what the import matches on. `ref` is CR-007, which is
    # what a person says out loud and what the page shows, and it is **counted
    # per project**: two projects both have a CR-007. Matching on it would settle
    # the wrong request about the wrong package, so it is carried for reading and
    # never read back.
    #
    # The three editable columns sit in the middle, ahead of `problem`. That is
    # deliberate and it is the one layout decision here: `problem` runs to eight
    # thousand characters, and a reader who has to scroll past it to reach the
    # cell they came to fill in is a reader who fills in the wrong row.
    header = [
        "id", "ref", "raised", "date", "project", "status", "blocking",
        "side", "platform",
        "kind", "artefact", "title", "raised by", "email", "via", "ticket",
        "picked by", "picked on",
        "our decision", "because", "reference", "settled on", "settled by",
        "problem", "evidence", "options", "recommendation",
    ]
    body = [
        [
            r["id"],
            f"CR-{r['number']:03d}",
            r["raised_at"], _day(r["raised_at"]),
            r["project_id"],
            CHANGE_STATUS_LABEL.get(r["status"], r["status"]),
            "yes" if r["blocking"] else "",
            # Whose queue it is in. Blank means nobody has said, which the
            # changes page shows as a bucket of its own rather than hiding.
            TAG_LABEL.get(r["tag"], r["tag"]),
            r["platform"],
            CHANGE_KIND_LABEL.get(r["target_kind"], r["target_kind"]),
            r["target_id"],
            r["title"],
            # Name or address, the same fallback _change_row makes, because an
            # account that never set a name would otherwise leave this column
            # blank here and filled on the page's own export of the same row.
            r["raised_by_name"] or r["raised_by_email"], r["raised_by_email"],
            r["raised_via"],
            r["external_key"],
            # Taken on, which is not settled. A blank here on an open request
            # older than two days is what the escalation is counting.
            r["picked_by_name"] or "",
            _day(r["picked_at"]),
            # The three the import reads, and the first of them is **blank
            # while the request is open**. That is the same rule the verdict
            # file follows for "our verdict": the column holds the answer, and
            # an open request has not been answered, so there is nothing to put
            # there. It is what makes a blank cell mean "leave this one alone"
            # on the way back — and since most of any range is open, most of the
            # column is blank and the reader fills in only what they settled.
            #
            # `status` above carries the current state for every row including
            # the open ones, so nothing is hidden by this being empty.
            "" if r["status"] == "open"
            else CHANGE_STATUS_LABEL.get(r["status"], r["status"]),
            r["resolution"],
            r["resolved_ref"],
            _day(r["resolved_at"]),
            r["resolved_by_name"] or "",
            r["problem"], r["evidence"],
            # A JSON list on the way out. Pipes rather than commas because this
            # is one cell in a comma-separated file, and a reader who opens it
            # in a text editor should not have to count quotation marks to see
            # where the options end.
            " | ".join(_options_of(r["options"])),
            r["recommendation"],
        ]
        for r in rows
    ]
    return header, body


def _options_of(value) -> list:
    """The ways a change request could be settled, as stored. `[]` for anything
    that will not parse: a malformed cell in one row of an export is not worth
    failing the other four hundred over, and it shows as an empty cell."""
    try:
        parsed = json.loads(value or "[]")
    except ValueError:
        return []
    return [str(item) for item in parsed] if isinstance(parsed, list) else []


# What may be exported, and what the file is called. Four, because four tables
# hold a record that accumulates and that somebody would sensibly ask a month of.
#
# `verdicts` is the default and the reason this exists: it is the register the
# whole product is for, one row per thing somebody said at a time.
#
# `changes` is the other one that grows with the work rather than with the
# payroll, and it is the other one that comes back: both files have columns a
# person fills in and re-uploads. The other two are read-only registers.
#
# `session` is deliberately absent although it is the fastest-growing table here.
# A session is deleted on sign-out, on a password change and on an account being
# disabled, so a range over it is not a record of anything — it would answer "who
# was signed in during July" with whoever happens not to have signed out since,
# which is a worse answer than none. `mention` is absent because it is derived
# from `verdict` and carries nothing the verdict export does not, and `reset` is
# absent because a reset link is a thing that lives for a day, not a register.
#
# The middle value is the column the range is read against, qualified by the
# alias its own query uses: `verdict` is joined to `account` twice over, and an
# unqualified `created_at` in that WHERE is ambiguous — SQLite refuses it rather
# than guessing, which is the good outcome, but only once. Naming the column
# here keeps the range one piece of code across three different shapes of query.
EXPORTS = {
    "verdicts": ("review-activity", "v.created_at", _export_verdicts),
    "changes": ("change-requests", "c.raised_at", _export_changes),
    "invites": ("invites", "i.created_at", _export_invites),
    "accounts": ("accounts", "a.created_at", _export_accounts),
}

# Of those, the ones about the installation rather than the delivery. A pm is
# refused these two and allowed the rest; an administrator takes any of them.
ADMIN_EXPORTS = {"invites", "accounts"}


def _bound(value: Optional[str], which: str) -> Optional[date]:
    """One end of the range, or None for "no end that way"."""
    text = (value or "").strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise HTTPException(
            400, f"The {which} date should look like 2026-08-01, not {text!r}.")


@app.get("/api/export/{dataset}")
def export_csv(
    dataset: str,
    # `from` is a Python keyword, so the parameter cannot be called that and the
    # query string can be nothing else — a date range whose parameter is named
    # `frm` in a URL is a thing nobody guesses right twice.
    since: Optional[str] = Query(default=None, alias="from"),
    until: Optional[str] = Query(default=None, alias="to"),
    reader: dict = Depends(require_reader),
) -> Response:
    """A date range of one register, as a CSV file.

    **Both ends are inclusive, and the `to` day is included whole.** That is the
    one thing about a range picker worth being explicit about: every stamp in
    this store carries a time, so `created_at <= '2026-08-25'` would compare a
    bare date against '2026-08-25T09:14:02+00:00' and quietly drop everything
    recorded on the last day of the range — the classic version of this bug, and
    one nobody notices because the file is not empty, only short. The upper bound
    is therefore the day after, exclusive.

    The comparison is lexicographic on the stored text rather than on parsed
    dates. That is exact, not a shortcut: security.stamp() writes one fixed-width
    ISO 8601 form in UTC, and for that form text order is time order. It also
    means the range is read in UTC, which is the only timezone any stamp here has
    ever been written in.

    An empty range is answered with the header row and nothing under it, and says
    so in X-Ticvai-Rows. Refusing to send a file would leave the reader unable to
    tell "nothing happened that week" from "the export is broken", which are the
    two things they are actually choosing between.

    **Who may take which file is decided per dataset, not at the door.** The
    review activity and the change requests are the delivery, and a pm reads the
    delivery; the account register and the invite log are the installation, and
    those stay an administrator's. One door for both would have meant either
    refusing a pm the delivery or handing them every address and open invite in
    the store, and neither is the role.

    That the review activity is signed-in reading on /api/verdicts does not make
    the file the same object: a whole-history CSV of who reviewed what and how
    fast is a different thing from the same rows on a screen behind a filter,
    which is why it is here at all rather than open to everybody.
    """
    if dataset not in EXPORTS:
        raise HTTPException(
            404, f"There is nothing to export called {dataset!r}. "
                 f"Try one of {', '.join(EXPORTS)}.")

    first, last = _bound(since, "from"), _bound(until, "to")
    if first and last and last < first:
        raise HTTPException(
            400, f"The range runs backwards: {first.isoformat()} is after "
                 f"{last.isoformat()}. Swap them.")

    if dataset in ADMIN_EXPORTS and not security.is_admin(reader["role"]):
        raise HTTPException(
            403, f"The {dataset} register is an administrator's. "
                 f"The delivery ones are {', '.join(sorted(set(EXPORTS) - ADMIN_EXPORTS))}.")

    stem, column, build = EXPORTS[dataset]
    clause, args = "", []
    if first:
        clause += f" AND {column} >= ?"
        args.append(first.isoformat())
    if last:
        clause += f" AND {column} < ?"
        args.append((last + timedelta(days=1)).isoformat())

    header, body = build(clause, tuple(args))

    # The header row goes out bare and the rows go out quoted, which is what the
    # browser's export does and is valid CSV either way: no column name here
    # holds a comma or a quote, and a reader who opens the file in a text editor
    # sees the headings rather than a row of quotation marks.
    lines = [",".join(header)]
    lines += [",".join(_cell(v) for v in row) for row in body]

    # utf-8-sig, for the byte order mark. Excel on Windows reads a UTF-8 CSV as
    # the system codepage without one, and these notes are full of the em dashes
    # and curly quotes this package is written in, which would arrive as
    # mojibake. The browser's export prepends the same mark by hand.
    payload = "\r\n".join(lines).encode("utf-8-sig")

    # An open end is named rather than left out, so the filename still says what
    # the range was. "beginning" because that is what an empty `from` means, and
    # today for an empty `to` because that is when the file was taken.
    span = (first.isoformat() if first else "beginning")
    span += "-to-" + (last.isoformat() if last else security.now().date().isoformat())
    return Response(
        content=payload,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="ticvai-{stem}-{span}.csv"',
            # How many rows are under the header. The page needs it to say "that
            # range is empty" out loud, and counting newlines in the body would
            # be wrong the first time somebody puts a line break in a note.
            "X-Ticvai-Rows": str(len(body)),
        },
    )


# ── bringing the file back ───────────────────────────────────────────
#
# The other half of the export. A month of the register goes out as a CSV,
# somebody works down the "Our verdict" column in Excel saying how each thing
# was answered, and this reads it back and closes those items in one go.
#
# It closes rows exactly the way /api/verdicts/{id}/done does — done_at, done_by
# and done_response, nothing cleared, the verdict itself untouched — because a
# bulk path that closes rows differently from the single path is two behaviours
# wearing one name, and the difference would only ever be found in a report six
# weeks later.

# What a decision cell may say, and what it means. Both spellings of each of the
# five: the key the store holds, and the label the export writes — a file that
# has been through Excel says "Approved — no action", never
# `approved-no-action`, and it is the same decision. Folded on both sides so
# case, spacing and the shape of the dash stop mattering.
_RESPONSE_OF = {
    decisions.fold(spelling): key
    for key in RESPONSES
    for spelling in (key, RESPONSE_LABEL[key])
}

# The two columns this needs, folded the way the parser folds a heading. Every
# other column in the file is read by a person and ignored here: matching by
# name rather than by position means a reader may reorder columns, or delete the
# ones they do not care about, and the file still applies.
_ID_COLUMN = "id"
_DECISION_COLUMN = "our-verdict"

# SQLite takes 999 bound parameters on the builds this is likely to meet, so the
# lookup of "everything this file names" goes in chunks. A limit that is only
# reached by a big file is the worst kind, because the small file it was tested
# with works.
_CHUNK = 400


def _current(ids: List[int]) -> dict:
    """Where each of those verdicts stands right now, by id."""
    found = {}
    for start in range(0, len(ids), _CHUNK):
        batch = ids[start:start + _CHUNK]
        holes = ",".join("?" * len(batch))
        for row in db.all_rows(
            f"""SELECT v.id, v.target_kind, v.target_id, v.audience, v.verdict,
                       v.done_at, v.done_response, v.sent_back_at,
                       d.name AS done_by_name
                  FROM verdict v
                  LEFT JOIN account d ON d.id = v.done_by
                 WHERE v.id IN ({holes})""",
            tuple(batch),
        ):
            found[row["id"]] = row
    return found


def _describe(row) -> dict:
    """The bit of a verdict a message about it has to say out loud."""
    return {
        "id": row["id"],
        "kind": KIND_LABEL.get(row["target_kind"], row["target_kind"]),
        "artefact": row["target_id"],
        "verdict": VERDICT_LABEL.get(row["verdict"], row["verdict"]),
        "audience": AUDIENCE_LABEL.get(row["audience"], row["audience"]),
    }


def _plan(payload: bytes, filename: str) -> dict:
    """What this file would do, without doing any of it.

    Every row lands in exactly one bucket, and the buckets are the whole of the
    reasoning:

    `close`    — a decision, and a row that is not currently finished. Written.
                 `was` says whether it was never closed or had been closed and
                 sent back; the second is the schema's own sequence, mark done,
                 sent back, marked done again, and closing it now is what makes
                 the completion stand again. The send-back is left where it is:
                 clearing it would lose the reason the work came back.

    `already`  — a decision that agrees with a row already finished. **Not
                 written.** Re-closing it would move done_at to today and done_by
                 to whoever uploaded the file, throwing away who actually closed
                 it and when, in exchange for no change of meaning at all.

    `differs`  — a decision that disagrees with a row already finished. Also not
                 written, and this is the case worth showing rather than
                 counting: the file says Built, the row says Wired, and one of
                 the two is wrong. A bulk upload is the wrong instrument for
                 settling that — it is a single deliberate act on one row, which
                 is what the control on the reviews page is.

    `blank`    — no decision on that row. Counted, never listed. A sheet that
                 has been round-tripped through Excel is mostly blank cells, and
                 an empty cell is the absence of an answer, not an instruction.

    `problems` — a row naming something this cannot act on: an id that is not a
                 number, an id no verdict has, a decision outside the vocabulary,
                 or a decision with no id beside it. Reported one by one with the
                 row number the person sees in Excel, because "400 Bad Request"
                 about a file of four hundred rows is not an answer.
    """
    try:
        sheet = decisions.read(payload)
    except decisions.FileError as bad:
        raise HTTPException(400, str(bad))

    # First wins, so a sheet with two columns called the same thing reads the
    # left one rather than raising about a case nobody meant to create.
    where: dict = {}
    for index, name in enumerate(sheet.header):
        where.setdefault(name, index)

    if _ID_COLUMN not in where:
        # Worth telling apart from a file that was never an export at all. Every
        # file taken before the id column was added has exactly this shape, and
        # there is nothing wrong with it except that nothing in it says which
        # verdict a row is: (kind, artefact) has a row per audience and another
        # every time somebody changed their mind. Guessing would close the wrong
        # item, which re-uploading the right file cannot undo.
        looks_exported = "artefact" in where and _DECISION_COLUMN in where
        raise HTTPException(400, (
            "That file has no id column, so there is no way to tell which "
            "verdict each row is about. " + (
                "It was exported before the id column existed — download the "
                "range again and fill in the new file."
                if looks_exported else
                "Upload a file taken from Download a date range, or exported "
                "off the reviews page.")))
    if _DECISION_COLUMN not in where:
        raise HTTPException(400, (
            "That file has no 'our verdict' column, which is the one this "
            "reads. The headings found were: "
            + (", ".join(sheet.header) or "none") + "."))

    wanted: List[int] = []
    parsed = []
    problems = []
    blank = 0

    for number, cells in sheet.rows:
        said = decisions.cell(cells, where[_DECISION_COLUMN])
        raw_id = decisions.cell(cells, where[_ID_COLUMN])
        if not said:
            blank += 1
            continue
        if not raw_id:
            problems.append({"row": number, "message": (
                f"Row {number}: {said!r} with no id beside it, so there is "
                f"nothing to close.")})
            continue
        try:
            # int(float(...)) as well, because Excel is entirely capable of
            # handing an integer column back as 812.0 once somebody has sorted
            # the sheet.
            verdict_id = int(float(raw_id))
        except ValueError:
            problems.append({"row": number, "message": (
                f"Row {number}: {raw_id!r} is not a verdict id.")})
            continue
        response = _RESPONSE_OF.get(decisions.fold(said))
        if response is None:
            # Reported, never written. done_response is a reporting column with
            # five values and a label for each; a sixth arrives as a blank in
            # every report and matches no filter, and it is the one field the
            # file exists to carry — so a typo in it is exactly the thing worth
            # stopping at. Per row rather than for the file, so the other three
            # hundred rows still apply. The single-row route refuses the same
            # value in the same words, which is the point.
            problems.append({"row": number, "message": (
                f"Row {number}: {said!r} is not one of "
                f"{', '.join(RESPONSE_LABEL[k] for k in RESPONSES)}.")})
            continue
        parsed.append((number, verdict_id, response))
        wanted.append(verdict_id)

    live = _current(wanted)
    close, already, differs = [], [], []

    for number, verdict_id, response in parsed:
        row = live.get(verdict_id)
        if row is None:
            problems.append({"row": number, "message": (
                f"Row {number}: no verdict with id {verdict_id}.")})
            continue
        entry = {"row": number, **_describe(row),
                 "response": response,
                 "response_label": RESPONSE_LABEL[response]}
        if not _settled(row):
            entry["was"] = "sent back" if row["sent_back_at"] else "open"
            close.append(entry)
            continue
        entry["done_on"] = _day(row["done_at"])
        entry["done_by"] = row["done_by_name"] or ""
        entry["current"] = row["done_response"]
        entry["current_label"] = RESPONSE_LABEL.get(
            row["done_response"], row["done_response"])
        (already if row["done_response"] == response else differs).append(entry)

    # Back into file order. Two passes produce them — the ones a cell is wrong
    # about, then the ones the store has never heard of — and a list that runs 18,
    # 19, 17 reads as a second mistake to somebody checking it against the sheet.
    problems.sort(key=lambda p: p["row"])

    return {
        "file": filename or "the upload",
        "format": sheet.kind,
        "tab": sheet.tab,
        "digest": decisions.digest(payload),
        "applied": False,
        "rows": len(sheet.rows),
        "blank": blank,
        "counts": {
            "close": len(close), "already": len(already),
            "differs": len(differs), "problems": len(problems), "blank": blank,
        },
        "close": close,
        "already": already,
        "differs": differs,
        "problems": problems,
    }


def _uploaded(file: UploadFile) -> bytes:
    """The bytes that arrived.

    `file.file` rather than `await file.read()`, so this route stays the plain
    `def` every other route here is. FastAPI runs a sync route in a worker
    thread, where a blocking read off the spooled temporary file is exactly
    right; making one route async to read a form would leave two idioms in one
    module for no gain.

    One byte more than the cap is read on purpose: it is how the size is refused
    without the whole file being in memory first.
    """
    return file.file.read(decisions.MAX_BYTES + 1)


@app.post("/api/decisions/preview")
def preview_decisions(
    file: UploadFile = File(...),
    admin: dict = Depends(require_admin),
):
    """What this spreadsheet would close, and what it would not. Writes nothing.

    The default and the only way to reach the apply below, which will not act on
    a file it has not been told the checksum of. That ordering is the whole
    design: closing two hundred items because somebody uploaded last month's
    file is not recoverable by uploading the right one afterwards, since the
    completions it overwrote no longer say who made them or when.

    Admin only, unlike marking one item done, which any reviewer may do. Closing
    one row is a statement about one piece of work; closing whatever a file
    happens to name is a statement about the queue, and it is the same call as
    sending work back — narrower than the row control on purpose.
    """
    return _plan(_uploaded(file), file.filename or "")


@app.post("/api/decisions/apply")
def apply_decisions(
    file: UploadFile = File(...),
    # The digest the preview answered with, sent back. A plain `confirm=true`
    # would confirm the *press*, which is not the thing in doubt: what has to be
    # established is that the file about to be applied is the file whose
    # consequences were read. Anything else — a second file picked between the
    # two presses, a sheet re-saved in the meantime — hashes differently and is
    # refused rather than applied on the strength of a preview of something else.
    confirm: str = Form(default=""),
    admin: dict = Depends(require_admin),
):
    """Close everything the preview said would close. Admin only.

    The plan is built again from the file rather than carried over from the
    preview, so what is written is derived from the bytes in hand and from the
    store as it is now — not from a summary made a minute ago, during which
    somebody may have closed one of these rows by hand.

    One timestamp for the whole file, because it is one act. All of it in one
    transaction, because a bulk close that half happened is the worst answer
    available: the counts in the response would be right and the store would not.
    """
    payload = _uploaded(file)
    plan = _plan(payload, file.filename or "")

    if not confirm:
        raise HTTPException(400, (
            "Nothing was applied: this needs the checksum the preview answered "
            "with, so that what is closed is what was read."))
    if confirm.strip() != plan["digest"]:
        raise HTTPException(400, (
            "That confirmation belongs to a different file than the one just "
            "uploaded. Preview this file and apply the result of that."))

    at = security.stamp()
    with db.cursor(commit=True) as cur:
        for item in plan["close"]:
            # Character for character the update /api/verdicts/{id}/done makes.
            # Nothing is cleared: the verdict stays as it was said, and a
            # send-back stays where it is — a done_at later than it is what makes
            # the completion stand again, which is the sequence the table was
            # shaped for.
            cur.execute(
                "UPDATE verdict SET done_at = ?, done_by = ?, done_response = ? "
                "WHERE id = ?",
                (at, admin["id"], item["response"], item["id"]),
            )

    plan["applied"] = True
    plan["closed_at"] = at
    plan["closed_by"] = admin["name"] or admin["email"]
    return plan


# ── change requests, out and back ────────────────────────────────────
#
# The same round trip as the verdict file above, over the other register that
# grows with the work. A range of change requests goes out as a CSV, somebody
# works down the "our decision" column saying how each was settled, and this
# reads it back and settles them in one go.
#
# **Every rule /api/changes/{number}/resolve enforces is enforced here, per
# row**, because a bulk path that settles differently from the single path is
# two behaviours wearing one name, and the difference would only ever be found
# in a report six weeks later. Where that route refuses outright, this one
# reports the row and carries on with the rest of the file.
#
# One of those rules is satisfied by where this route sits rather than by any
# code below: "somebody other than the person who raised it has to accept or
# reject it" holds because **this is admin only, and an admin is that route's
# own stated exception**. If this is ever opened to a reviewer, that check has
# to be written in here, because nothing else would then be making it.

# What a decision cell may say, and what it means. Both spellings of each of the
# four: the key the store holds and the label the export writes. Folded on both
# sides so case, spacing and the shape of a dash stop mattering — the same trick
# _RESPONSE_OF plays for the verdict file.
_DECISION_OF = {
    decisions.fold(spelling): key
    for key in CHANGE_STATUSES
    for spelling in (key, CHANGE_STATUS_LABEL[key])
}

# The columns this reads, folded the way the parser folds a heading. `id` and
# `our decision` are required; the other two are optional, because a reader who
# is only moving things to Done has no reason to keep them and the file still
# applies without them. Every other column in the export is there to be read.
_CHANGE_ID_COLUMN = "id"
_CHANGE_DECISION_COLUMN = "our-decision"
_CHANGE_BECAUSE_COLUMN = "because"
_CHANGE_REFERENCE_COLUMN = "reference"


def _change_current(ids: List[int]) -> dict:
    """Where each of those change requests stands right now, by database id."""
    found = {}
    for start in range(0, len(ids), _CHUNK):
        batch = ids[start:start + _CHUNK]
        holes = ",".join("?" * len(batch))
        for row in db.all_rows(
            f"""SELECT c.id, c.number, c.project_id, c.target_kind, c.target_id,
                       c.title, c.status, c.resolution, c.resolved_ref,
                       c.resolved_at, s.name AS resolved_by_name
                  FROM change_request c
                  LEFT JOIN account s ON s.id = c.resolved_by
                 WHERE c.id IN ({holes})""",
            tuple(batch),
        ):
            found[row["id"]] = row
    return found


def _change_describe(row) -> dict:
    """The bit of a change request a message about it has to say out loud."""
    return {
        "id": row["id"],
        "ref": f"CR-{row['number']:03d}",
        "project": row["project_id"],
        "kind": CHANGE_KIND_LABEL.get(row["target_kind"], row["target_kind"]),
        "artefact": row["target_id"],
        "title": row["title"],
    }


def _change_plan(payload: bytes, filename: str) -> dict:
    """What this spreadsheet would settle, without settling any of it.

    Every row lands in exactly one bucket, and the buckets are the reasoning:

    `settle`   — a decision on a request that is open. Written. The ordinary
                 case, and most of any file that does anything.

    `advance`  — `Done` on a request that is already `accepted`. Written, and it
                 is the only move onto an already-settled row this will make:
                 accepting a change and then completing it is the lifecycle
                 rather than a disagreement, and it is exactly what the control
                 on the changes page does. `from` says what it was, so the
                 preview shows it as a move rather than a fresh settlement.

    `already`  — a decision that agrees with where the request already is. **Not
                 written**, including when the file's `because` differs from the
                 stored one: writing it would move resolved_by and resolved_at to
                 whoever uploaded the file, throwing away who actually settled it
                 and when, in exchange for a changed note. Rewording a settled
                 request is a single deliberate act, and the changes page is
                 where it is made.

    `differs`  — any other move off a settled request, **including reopening**.
                 Not written, and listed rather than counted. Reopening clears
                 resolved_by, resolved_at and resolved_ref, so a file applied by
                 accident would not leave the previous answer behind to be
                 restored — the same irreversibility that stops the verdict file
                 re-closing a closed row.

    `blank`    — no decision on that row. Counted, never listed. The export
                 leaves this column empty for every open request, so most of a
                 file is blank cells, and a blank one is the absence of an answer
                 rather than an instruction.

    `problems` — a row naming something this cannot act on: an id that is not a
                 number, an id no request has, a decision outside the four, a
                 decision with no id beside it, or a rejection with nothing
                 saying why. Reported one by one with the row number the person
                 sees in Excel, because "400 Bad Request" about a file of four
                 hundred rows is not an answer.
    """
    try:
        sheet = decisions.read(payload)
    except decisions.FileError as bad:
        raise HTTPException(400, str(bad))

    # First wins, so a sheet with two columns called the same thing reads the
    # left one rather than raising about a case nobody meant to create.
    where: dict = {}
    for index, name in enumerate(sheet.header):
        where.setdefault(name, index)

    if _CHANGE_ID_COLUMN not in where:
        raise HTTPException(400, (
            "That file has no id column, so there is no way to tell which "
            "change request each row is about. Upload a file taken from "
            "Download a date range with Change requests selected."))
    if _CHANGE_DECISION_COLUMN not in where:
        # Worth telling apart from the verdict file, which is the other thing an
        # admin has on disk with an id column and a very similar shape. Applying
        # one as the other cannot happen — the ids would name unrelated rows —
        # so the message names the mistake rather than listing the headings.
        looks_like_verdicts = _DECISION_COLUMN in where
        raise HTTPException(400, (
            "That file has no 'our decision' column, which is the one this "
            "reads. " + (
                "It looks like the review activity file, which has 'our "
                "verdict' and belongs in Close items from a spreadsheet above."
                if looks_like_verdicts else
                "The headings found were: "
                + (", ".join(sheet.header) or "none") + ".")))

    wanted: List[int] = []
    parsed = []
    problems = []
    blank = 0

    for number, cells in sheet.rows:
        said = decisions.cell(cells, where[_CHANGE_DECISION_COLUMN])
        raw_id = decisions.cell(cells, where[_CHANGE_ID_COLUMN])
        if not said:
            blank += 1
            continue
        if not raw_id:
            problems.append({"row": number, "message": (
                f"Row {number}: {said!r} with no id beside it, so there is "
                f"nothing to settle.")})
            continue
        try:
            # int(float(...)) as well, because Excel is entirely capable of
            # handing an integer column back as 812.0 once somebody has sorted
            # the sheet.
            change_id = int(float(raw_id))
        except ValueError:
            problems.append({"row": number, "message": (
                f"Row {number}: {raw_id!r} is not a change request id.")})
            continue
        status = _DECISION_OF.get(decisions.fold(said))
        if status is None:
            problems.append({"row": number, "message": (
                f"Row {number}: {said!r} is not one of "
                f"{', '.join(CHANGE_STATUS_LABEL[k] for k in CHANGE_STATUSES)}."
            )})
            continue
        parsed.append((
            number, change_id, status,
            decisions.cell(cells, where.get(_CHANGE_BECAUSE_COLUMN)),
            decisions.cell(cells, where.get(_CHANGE_REFERENCE_COLUMN)),
        ))
        wanted.append(change_id)

    live = _change_current(wanted)
    settle, advance, already, differs = [], [], [], []

    for number, change_id, status, because, reference in parsed:
        row = live.get(change_id)
        if row is None:
            problems.append({"row": number, "message": (
                f"Row {number}: no change request with id {change_id}.")})
            continue

        # A blank cell leaves what is stored, exactly as the single-row route
        # does with `body.resolution or row["resolution"]`. So the reason a
        # rejection needs is either one typed into this file or one already
        # there from a previous answer.
        note = because or row["resolution"]
        if status == "rejected" and not note.strip():
            problems.append({"row": number, "message": (
                f"Row {number}: CR-{row['number']:03d} is rejected with nothing "
                f"in the 'because' column. Say why it is rejected - that is "
                f"what the person who raised it reads.")})
            continue

        entry = {
            "row": number, **_change_describe(row),
            "decision": status,
            "decision_label": CHANGE_STATUS_LABEL[status],
            "because": note,
            "reference": reference or row["resolved_ref"],
        }
        current = row["status"]

        if current == status:
            entry["settled_on"] = _day(row["resolved_at"])
            entry["settled_by"] = row["resolved_by_name"] or ""
            already.append(entry)
        elif current == "open":
            settle.append(entry)
        elif current == "accepted" and status == "done":
            entry["from"] = CHANGE_STATUS_LABEL[current]
            advance.append(entry)
        else:
            entry["current"] = current
            entry["current_label"] = CHANGE_STATUS_LABEL.get(current, current)
            entry["settled_on"] = _day(row["resolved_at"])
            entry["settled_by"] = row["resolved_by_name"] or ""
            differs.append(entry)

    # Back into file order. Several passes produce them, and a list that runs
    # 18, 19, 17 reads as a second mistake to somebody checking it against the
    # sheet.
    problems.sort(key=lambda p: p["row"])

    return {
        "file": filename or "the upload",
        "format": sheet.kind,
        "tab": sheet.tab,
        "digest": decisions.digest(payload),
        "applied": False,
        "rows": len(sheet.rows),
        "blank": blank,
        "counts": {
            "settle": len(settle), "advance": len(advance),
            "already": len(already), "differs": len(differs),
            "problems": len(problems), "blank": blank,
        },
        "settle": settle,
        "advance": advance,
        "already": already,
        "differs": differs,
        "problems": problems,
    }


def _written_rows(plan: dict) -> list:
    """The rows an apply writes: the ones that answer an open request, and the
    ones that complete an accepted one.

    Two buckets in the preview because they read differently to a person; one
    list here because the statement is identical, and writing it twice would be
    two places for the next change to have to find. Nothing else in the plan is
    written — that is what `already`, `differs` and `problems` mean.
    """
    return plan["settle"] + plan["advance"]


@app.post("/api/changes/import/preview")
def preview_changes(
    file: UploadFile = File(...),
    admin: dict = Depends(require_admin),
):
    """What this spreadsheet would settle, and what it would not. Writes nothing.

    The default, and the only way to reach the apply below, which will not act
    on a file it has not been told the checksum of. Same ordering and the same
    reason as the verdict importer: settling a request overwrites who settled it
    and when, so a file applied by accident does not leave the previous answer
    behind to be restored by uploading the right one afterwards.
    """
    return _change_plan(_uploaded(file), file.filename or "")


@app.post("/api/changes/import/apply")
def apply_changes(
    file: UploadFile = File(...),
    # The digest the preview answered with, sent back. A plain `confirm=true`
    # would confirm the *press*, which is not the thing in doubt: what has to be
    # established is that the file about to be applied is the file whose
    # consequences were read.
    confirm: str = Form(default=""),
    admin: dict = Depends(require_admin),
):
    """Settle everything the preview said would settle. Admin only.

    The plan is built again from the file rather than carried over from the
    preview, so what is written is derived from the bytes in hand and from the
    store as it is now — not from a summary made a minute ago, during which
    somebody may have settled one of these on the changes page.

    One timestamp for the whole file, because it is one act. All of it in one
    transaction, because a bulk settle that half happened is the worst answer
    available: the counts in the response would be right and the store would not.
    """
    payload = _uploaded(file)
    plan = _change_plan(payload, file.filename or "")

    if not confirm:
        raise HTTPException(400, (
            "Nothing was applied: this needs the checksum the preview answered "
            "with, so that what is settled is what was read."))
    if confirm.strip() != plan["digest"]:
        raise HTTPException(400, (
            "That confirmation belongs to a different file than the one just "
            "uploaded. Preview this file and apply the result of that."))

    at = security.stamp()
    with db.cursor(commit=True) as cur:
        for item in _written_rows(plan):
            # Character for character the update /api/changes/{number}/resolve
            # makes for a settled status. `because` and `reference` have already
            # fallen back to what is stored, in _change_plan, so a blank cell
            # leaves the stored note and ref exactly as that route does.
            cur.execute(
                "UPDATE change_request SET status = ?, resolution = ?, "
                "resolved_ref = ?, resolved_by = ?, resolved_at = ? "
                "WHERE id = ?",
                (item["decision"], item["because"], item["reference"],
                 admin["id"], at, item["id"]),
            )

    plan["applied"] = True
    plan["settled_at"] = at
    plan["settled_by"] = admin["name"] or admin["email"]
    return plan


@app.get("/api/health")
def health():
    """Whether the service is answering. That is the whole answer.

    It used to report the number of accounts and the allowed domain. This route
    is unauthenticated by design — `lib/session.mjs` lists it among the paths the
    gate lets through — so once this was on a public name that was the company's
    headcount handed to anyone who asked, from a URL that looks like plumbing.

    Nothing is lost by removing it. `/api/auth/state` already answers the one
    question a caller legitimately has before it can sign in — whether the store
    is empty — as `needsBootstrap`, and carries `domain` because the sign-in page
    has to say which addresses can hold an account. The count itself had no
    reader anywhere but three harnesses, and what each of them wanted was
    "is this store empty", which is the field next door.
    """
    return {"ok": True}
