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
from typing import List, Optional

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import db, security

app = FastAPI(
    title="TICVAI viewer — accounts and validation",
    version="1.0.0",
    description=__doc__,
)

# On a workstation the viewer is served by the Node process on another port, so
# the browser treats calls here as cross-origin. Credentials must be allowed for
# the session cookie to be sent at all, and allowing credentials rules out "*".
#
# A deployment puts both behind one address, where there is no cross-origin call
# to permit and this list is simply unused. TICVAI_ORIGINS is for the case in
# between — a server whose two halves are still on separate ports — and takes a
# comma-separated list. It is never "*": that combined with credentials would
# let any site on the internet read this one using the visitor's own session.
_extra = [o.strip() for o in os.environ.get("TICVAI_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4173", "http://127.0.0.1:4173",
        "http://localhost:8787", "http://127.0.0.1:8787",
        
    ] + _extra,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"],
)

SESSION_COOKIE = "ticvai_session"

# Who the session cookie belongs to.
#
# Unset on a workstation and in the one-origin deployment: the cookie is
# host-only, which is the tighter default and all either arrangement needs.
#
# It is required the moment the two halves are on different names — the reading
# server on atlas.example.com and this service on atlasapi.example.com. The
# browser sends a host-only cookie set by atlasapi back to atlasapi and nowhere
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


@app.on_event("startup")
def _startup() -> None:
    db.init()


# ── shapes ───────────────────────────────────────────────────────────

class Credentials(BaseModel):
    email: str
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


@app.get("/api/health")
def health():
    accounts = db.one("SELECT COUNT(*) AS n FROM account")["n"]
    return {"ok": True, "accounts": accounts, "domain": security.ALLOWED_DOMAIN}
