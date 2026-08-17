"""Command line for the things that cannot be done from the web.

Invites are created by an admin — which leaves the question of where the first
admin comes from. Here: at a terminal, by whoever runs the service. That is the
one account not vouched for by another account, and it should be made
deliberately rather than by whoever reaches the signup page first.

    python -m api.cli admin chinmay.parab@softlabsgroup.com
    python -m api.cli invite asha@softlabsgroup.com --role reviewer
    python -m api.cli list
"""

from __future__ import annotations

import argparse
import getpass
import sqlite3
import sys
from pathlib import Path

from . import db, security


def _read_password() -> str:
    first = getpass.getpass("Password (12+ characters): ")
    if first != getpass.getpass("Again: "):
        sys.exit("Those did not match.")
    try:
        security.check_password(first)
    except ValueError as exc:
        sys.exit(str(exc))
    return first


def add_admin(args) -> None:
    db.init()
    try:
        email = security.check_email(args.email)
    except security.DomainError as exc:
        sys.exit(str(exc))

    folded = db.fold(email)
    if db.one("SELECT id FROM account WHERE email_folded = ?", (folded,)):
        sys.exit(f"{email} already holds an account.")

    password = _read_password()
    db.write(
        """INSERT INTO account (email, email_folded, name, password_hash, role, created_at)
           VALUES (?, ?, ?, ?, 'admin', ?)""",
        (email, folded, args.name or "", security.hash_password(password), security.stamp()),
    )
    print(f"admin {email} created. Sign in at the viewer and invite the rest.")


def add_invite(args) -> None:
    db.init()
    try:
        email = security.check_email(args.email)
    except security.DomainError as exc:
        sys.exit(str(exc))

    folded = db.fold(email)
    if db.one("SELECT id FROM account WHERE email_folded = ?", (folded,)):
        sys.exit(f"{email} already holds an account.")

    db.write(
        """UPDATE invite SET revoked_at = ?
            WHERE email_folded = ? AND redeemed_at IS NULL AND revoked_at IS NULL""",
        (security.stamp(), folded),
    )
    token = security.new_token()
    db.write(
        """INSERT INTO invite (email, email_folded, token_hash, role, created_at, expires_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (email, folded, security.token_hash(token), args.role,
         security.stamp(), security.invite_expiry(args.days)),
    )
    print(f"invite for {email} ({args.role}), good for {args.days} days:\n")
    print(f"  {args.base}/invite.html#{token}\n")
    print("Send that link to them. It works once, and only for that address.")
    print("It is not stored and cannot be shown again — make another if it is lost.")


def show(args) -> None:
    db.init()
    accounts = db.all_rows(
        "SELECT email, name, role, active, created_at FROM account ORDER BY id")
    print(f"{len(accounts)} account(s)")
    for a in accounts:
        flag = "" if a["active"] else "  (disabled)"
        print(f"  {a['role']:<9} {a['email']}{flag}")

    invites = db.all_rows(
        """SELECT email, role, expires_at, redeemed_at, revoked_at
             FROM invite ORDER BY id DESC""")
    live = [i for i in invites
            if not i["redeemed_at"] and not i["revoked_at"]
            and not security.expired(i["expires_at"])]
    print(f"\n{len(live)} open invite(s) of {len(invites)}")
    for i in live:
        print(f"  {i['role']:<9} {i['email']}  expires {i['expires_at']}")


def forget(args) -> None:
    """Remove every verdict recorded by one account.

    Verdicts are append-only on purpose: a sign-off you can quietly revise is
    not a sign-off, and the history of how something got to `approved` is the
    part worth keeping. This is the one exception, and it is deliberately
    narrow — it takes an account, not an artefact, so it can undo a harness run
    and cannot be used to tidy away an inconvenient opinion. A person's
    verdicts stay until the person is removed.
    """
    db.init()
    account = db.one("SELECT id, email FROM account WHERE email = ?", (args.email,))
    if not account:
        print(f"No account for {args.email}.")
        return
    rows = db.one(
        "SELECT COUNT(*) AS n FROM verdict WHERE account_id = ?", (account["id"],))["n"]
    if not rows:
        print(f"{args.email} has recorded no verdicts.")
        return
    if not args.yes:
        print(f"{rows} verdict(s) by {args.email} would be deleted. Pass --yes to do it.")
        return
    db.write("DELETE FROM verdict WHERE account_id = ?", (account["id"],))
    print(f"Deleted {rows} verdict(s) by {args.email}.")


def passwd(args) -> None:
    """Set a new password on an account, at this terminal.

    The web route deliberately demands the current password, which is no use
    when the current one is the problem — forgotten, or set by something other
    than the person it belongs to. This asks for nothing but the new one,
    because standing at the machine with the store on it is already the whole
    proof. Every session is dropped, so anything signed in with the old
    password stops being signed in.
    """
    db.init()
    account = db.one(
        "SELECT id, email, role FROM account WHERE email_folded = ?", (db.fold(args.email),))
    if not account:
        print(f"No account for {args.email}.")
        return

    replacement = _read_password()
    db.write(
        "UPDATE account SET password_hash = ? WHERE id = ?",
        (security.hash_password(replacement), account["id"]),
    )
    dropped = db.one(
        "SELECT COUNT(*) AS n FROM session WHERE account_id = ?", (account["id"],))["n"]
    db.write("DELETE FROM session WHERE account_id = ?", (account["id"],))
    print(f"Set a new password for {account['email']} ({account['role']}).")
    if dropped:
        print(f"{dropped} session(s) signed out.")


def adopt(args) -> None:
    """Copy one account out of another store, password and all.

    For the case where the service was started against a throwaway database —
    a test run, a `TICVAI_DB` left set in a shell — and the account somebody
    actually made ended up in it. The stored hash moves across unchanged, so
    the password stays the one they chose and is never seen by anything here.

    Nothing else comes with it. Sessions are left behind deliberately: a
    session is a claim about a browser, and it should be made again against
    the store that is now answering. Verdicts are left behind because a verdict
    recorded against a test store was almost certainly a test.
    """
    src_path = Path(args.source)
    if not src_path.exists():
        print(f"No database at {src_path}.")
        return

    src = sqlite3.connect(src_path)
    src.row_factory = sqlite3.Row
    row = src.execute(
        "SELECT * FROM account WHERE email_folded = ?", (db.fold(args.email),)).fetchone()
    if row is None:
        print(f"{args.email} is not in {src_path}.")
        return

    db.init()
    if db.one("SELECT id FROM account WHERE email_folded = ?", (db.fold(args.email),)):
        print(f"{args.email} is already here. Nothing to do.")
        return

    if not args.yes:
        print(f"Would copy {row['email']} ({row['role']}) from {src_path}. Pass --yes to do it.")
        return

    columns = ["email", "email_folded", "name", "password_hash", "role", "active", "created_at"]
    db.write(
        f"INSERT INTO account ({','.join(columns)}) VALUES ({','.join('?' * len(columns))})",
        tuple(row[c] for c in columns),
    )
    print(f"Copied {row['email']} ({row['role']}). Their password is unchanged; sign in again.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="api.cli", description=__doc__)
    subs = parser.add_subparsers(required=True, dest="command")

    p = subs.add_parser("admin", help="create the first admin account")
    p.add_argument("email")
    p.add_argument("--name", default="")
    p.set_defaults(func=add_admin)

    p = subs.add_parser("invite", help="make an invite link for one address")
    p.add_argument("email")
    p.add_argument("--role", default="reviewer", choices=["reviewer", "admin"])
    p.add_argument("--days", type=int, default=security.INVITE_DAYS)
    p.add_argument("--base", default="http://localhost:4173")
    p.set_defaults(func=add_invite)

    p = subs.add_parser("list", help="show accounts and open invites")
    p.set_defaults(func=show)

    p = subs.add_parser("forget", help="delete every verdict by one account — for undoing a harness run")
    p.add_argument("email")
    p.add_argument("--yes", action="store_true", help="actually delete them")
    p.set_defaults(func=forget)

    p = subs.add_parser("passwd", help="set a new password on an account, without the old one")
    p.add_argument("email")
    p.set_defaults(func=passwd)

    p = subs.add_parser("adopt", help="copy one account out of another store, password and all")
    p.add_argument("email")
    p.add_argument("--source", required=True, help="path to the other .db")
    p.add_argument("--yes", action="store_true", help="actually copy it")
    p.set_defaults(func=adopt)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
