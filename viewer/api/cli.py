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
import sys

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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
