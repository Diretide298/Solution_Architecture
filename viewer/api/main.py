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
VERDICTS = ("approved", "rejected", "needs-work")
TARGET_KINDS = ("operation", "table", "screen", "board")


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


class Account(BaseModel):
    id: int
    email: str
    name: str
    role: str


class VerdictOut(BaseModel):
    id: int
    target_kind: str
    target_id: str
    verdict: str
    note: str
    by: str
    by_email: str
    at: str


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
    """Anyone who may record a decision — admin or reviewer, never a guest.

    A guest is read-only, and this is where that is true. Hiding the verdict
    form in the browser is presentation; a hidden form is still a POST away for
    anyone who opens devtools. The rule has to be here or it is not a rule.
    """
    if account["role"] not in security.WRITERS:
        raise HTTPException(
            403, "A guest account can read the package but cannot record a verdict.")
    return account


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
    response.delete_cookie(SESSION_COOKIE, path="/")
    return {"ok": True}


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        SESSION_COOKIE, token,
        max_age=security.SESSION_DAYS * 24 * 3600,
        httponly=True,   # script cannot read it, so an injection cannot steal it
        samesite="lax",
        path="/",
        # The viewer runs over http on a workstation. Setting Secure here would
        # stop the cookie being sent at all. Set TICVAI_SECURE_COOKIE=1 when
        # this is ever served over https.
        secure=bool(__import__("os").environ.get("TICVAI_SECURE_COOKIE")),
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
    # decides whether the domain rule applies. A guest is an outside client and
    # is expected to be on another domain; a reviewer is not.
    if body.role not in security.ROLES:
        raise HTTPException(400, f"A role is one of {', '.join(security.ROLES)}.")

    try:
        email = security.check_email(body.email, body.role)
    except security.DomainError as exc:
        raise HTTPException(400, str(exc))

    # A guest link goes to an address outside the company, so it is worth less
    # for less time. Asking for longer is capped rather than refused.
    days = min(body.days, security.GUEST_INVITE_DAYS) if body.role == "guest" else body.days

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


# ── verdicts ─────────────────────────────────────────────────────────

@app.post("/api/validation")
def record(body: VerdictIn, account: dict = Depends(require_writer)):
    if body.verdict not in VERDICTS:
        raise HTTPException(400, f"A verdict is one of {', '.join(VERDICTS)}.")
    if body.target_kind not in TARGET_KINDS:
        raise HTTPException(400, f"A target is one of {', '.join(TARGET_KINDS)}.")
    if not body.target_id.strip():
        raise HTTPException(400, "A verdict needs something to be about.")

    row_id = db.write(
        """INSERT INTO verdict (target_kind, target_id, verdict, note, account_id, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            body.target_kind, body.target_id.strip(), body.verdict,
            body.note.strip(), account["id"], security.stamp(),
        ),
    )
    return {"id": row_id, "ok": True}


@app.get("/api/validation/{target_kind}/{target_id:path}")
def history(target_kind: str, target_id: str):
    """Every verdict on one artefact, newest first. The newest is the current
    one; the rest are how it got there, which is the part worth keeping."""
    rows = db.all_rows(
        """SELECT v.id, v.target_kind, v.target_id, v.verdict, v.note,
                  v.created_at AS at, a.name AS by, a.email AS by_email
             FROM verdict v JOIN account a ON a.id = v.account_id
            WHERE v.target_kind = ? AND v.target_id = ?
            ORDER BY v.id DESC""",
        (target_kind, target_id),
    )
    items = [VerdictOut(**dict(r)) for r in rows]
    return {"current": items[0] if items else None, "history": items}


@app.get("/api/validation")
def summary(target_kind: Optional[str] = None):
    """The current verdict on everything judged so far — one row per artefact,
    which is what a sign-off report is made of."""
    sql = """
        SELECT v.target_kind, v.target_id, v.verdict, v.note,
               v.created_at AS at, a.name AS by, a.email AS by_email, v.id
          FROM verdict v
          JOIN account a ON a.id = v.account_id
         WHERE v.id IN (SELECT MAX(id) FROM verdict GROUP BY target_kind, target_id)
    """
    args: tuple = ()
    if target_kind:
        sql += " AND v.target_kind = ?"
        args = (target_kind,)
    sql += " ORDER BY v.target_kind, v.target_id"

    rows = db.all_rows(sql, args)
    counts: dict = {}
    for r in rows:
        counts.setdefault(r["target_kind"], {}).setdefault(r["verdict"], 0)
        counts[r["target_kind"]][r["verdict"]] += 1
    return {"counts": counts, "items": [VerdictOut(**dict(r)) for r in rows]}


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
        """SELECT v.id, v.target_kind, v.target_id, v.verdict, v.note,
                  v.created_at AS at, v.account_id,
                  a.name AS by, a.email AS by_email, a.role AS by_role, a.active AS by_active
             FROM verdict v JOIN account a ON a.id = v.account_id
            ORDER BY v.id DESC"""
    )
    people = db.all_rows(
        "SELECT id, email, name, role, active, created_at FROM account ORDER BY id"
    )
    return {
        "verdicts": [dict(r) for r in rows],
        "accounts": [dict(p) for p in people],
    }


@app.get("/api/health")
def health():
    accounts = db.one("SELECT COUNT(*) AS n FROM account")["n"]
    return {"ok": True, "accounts": accounts, "domain": security.ALLOWED_DOMAIN}
