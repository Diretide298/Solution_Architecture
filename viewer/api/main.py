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

import os
import re
from datetime import date, timedelta
from typing import List, Optional

from fastapi import (
    Cookie, Depends, FastAPI, File, Form, HTTPException, Query, Response,
    Request, UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import db, decisions, security

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
    allow_methods=["GET", "POST", "DELETE"],
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
# server on aster.example.com and this service on asterapi.example.com. The
# browser sends a host-only cookie set by asterapi back to asterapi and nowhere
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
    if account["role"] != "admin":
        raise HTTPException(403, "Only an admin can do that.")
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

    An admin gets every active project. They register projects and they issue
    grants, so refusing them a package they added a minute ago would be a lockout
    with the key in the same pocket. Everybody else needs a row, and a missing
    row is no access: there is no default that has to be remembered and turned
    off.
    """
    if account["role"] == "admin":
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
    if not active and row["role"] == "admin" and _live_admin_count() <= 1:
        raise HTTPException(409, "That is the last active admin. Make another first.")

    db.write("UPDATE account SET active = ? WHERE id = ?", (1 if active else 0, account_id))
    if not active:
        # A disabled account must stop being signed in, not merely stop being
        # able to sign in again.
        db.write("DELETE FROM session WHERE account_id = ?", (account_id,))
    return {"ok": True, "active": active}


@app.post("/api/accounts/{account_id}/role")
def set_role(account_id: int, role: str, admin: dict = Depends(require_admin)):
    if role not in security.ROLES:
        raise HTTPException(400, f"A role is one of {', '.join(security.ROLES)}.")
    row = db.one("SELECT id, role FROM account WHERE id = ?", (account_id,))
    if not row:
        raise HTTPException(404, "No such account.")
    if account_id == admin["id"] and role != "admin":
        raise HTTPException(409, "You cannot take admin away from yourself.")
    if row["role"] == "admin" and role != "admin" and _live_admin_count() <= 1:
        raise HTTPException(409, "That is the last admin.")
    db.write("UPDATE account SET role = ? WHERE id = ?", (role, account_id))
    return {"ok": True, "role": role}


def _live_admin_count() -> int:
    return db.one(
        "SELECT COUNT(*) AS n FROM account WHERE role = 'admin' AND active = 1")["n"]


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

    try:
        email = security.check_email(body.email, body.role)
    except security.DomainError as exc:
        raise HTTPException(400, str(exc))

    # A client link goes to an address outside the company, so it is worth less
    # for less time. Asking for longer is capped rather than refused.
    days = min(body.days, security.CLIENT_INVITE_DAYS) if body.role == "client" else body.days

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
             (email, email_folded, token_hash, role, created_by, created_at, expires_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            email, folded, security.token_hash(token), body.role,
            admin["id"], security.stamp(), security.invite_expiry(days),
        ),
    )
    # The only time the token exists in the clear. It is not recoverable later,
    # by us or by anyone who takes a copy of the database.
    return {
        "id": invite_id,
        "email": email,
        "role": body.role,
        "link": f"/invite.html#{token}",
        "token": token,
        "expires_at": db.one("SELECT expires_at FROM invite WHERE id = ?",
                             (invite_id,))["expires_at"],
    }


@app.get("/api/invites")
def list_invites(admin: dict = Depends(require_admin)):
    rows = db.all_rows(
        """SELECT id, email, role, created_at, expires_at, redeemed_at, revoked_at
             FROM invite ORDER BY id DESC"""
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
        """SELECT id, email, email_folded, role, expires_at, redeemed_at, revoked_at
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


# What may be exported, and what the file is called. Three, because three tables
# hold a record that accumulates and that somebody would sensibly ask a month of.
#
# `verdicts` is the default and the reason this exists: it is the register the
# whole product is for, one row per thing somebody said at a time, and it is the
# only one of the three that grows with the work rather than with the payroll.
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
    "invites": ("invites", "i.created_at", _export_invites),
    "accounts": ("accounts", "a.created_at", _export_accounts),
}


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
    admin: dict = Depends(require_admin),
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

    Admin only. The account register and the invite log are plainly an admin's;
    the review activity is signed-in reading on /api/verdicts and is admin here
    anyway, because a whole-history file of who reviewed what and how fast is a
    different object from the same rows on a screen behind a filter.
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


@app.get("/api/health")
def health():
    accounts = db.one("SELECT COUNT(*) AS n FROM account")["n"]
    return {"ok": True, "accounts": accounts, "domain": security.ALLOWED_DOMAIN}
