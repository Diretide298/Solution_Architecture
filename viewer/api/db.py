"""The store behind accounts, invites and validation verdicts.

Deliberately SQLite and deliberately plain SQL. The viewer reads a delivery
package off disk; this holds the handful of things a reader *writes*, and that
is a few thousand rows at the outside. An ORM would be more machinery than the
problem has.

Everything that could be used to get in — passwords, session tokens, invite
tokens — is stored hashed, never in the clear. A copy of this file must not be
enough to sign in as anyone.
"""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

# Next to the delivery package, not inside it: the package is what the vendor
# shipped and stays as received.
DB_PATH = Path(os.environ.get("TICVAI_DB", Path(__file__).parent / "ticvai.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS account (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  email         TEXT    NOT NULL,
  -- one account per address, case-insensitively: Asha@ and asha@ are the same
  -- person, and letting both exist would split their verdicts in two
  email_folded  TEXT    NOT NULL UNIQUE,
  name          TEXT    NOT NULL DEFAULT '',
  password_hash TEXT    NOT NULL,
  role          TEXT    NOT NULL DEFAULT 'reviewer',
  active        INTEGER NOT NULL DEFAULT 1,
  created_at    TEXT    NOT NULL,
  last_seen_at  TEXT
);

CREATE TABLE IF NOT EXISTS invite (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  -- The address is fixed when the invite is made, not chosen by whoever opens
  -- the link. That is the whole reason an invite counts as verification: the
  -- person who could vouch for the address is the person who typed it.
  email        TEXT    NOT NULL,
  email_folded TEXT    NOT NULL,
  token_hash   TEXT    NOT NULL UNIQUE,
  role         TEXT    NOT NULL DEFAULT 'reviewer',
  created_by   INTEGER REFERENCES account(id),
  created_at   TEXT    NOT NULL,
  expires_at   TEXT    NOT NULL,
  redeemed_at  TEXT,
  revoked_at   TEXT
);
CREATE INDEX IF NOT EXISTS invite_email ON invite(email_folded);

CREATE TABLE IF NOT EXISTS session (
  token_hash  TEXT    PRIMARY KEY,
  account_id  INTEGER NOT NULL REFERENCES account(id),
  created_at  TEXT    NOT NULL,
  expires_at  TEXT    NOT NULL,
  user_agent  TEXT    NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS session_account ON session(account_id);

CREATE TABLE IF NOT EXISTS verdict (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  -- "operation:listProducts", "table:orders.sales_order", "screen:WEB-002",
  -- "board:P07 Staff Scanner". The kind is split out so a view can ask for
  -- every table verdict without parsing strings.
  target_kind TEXT    NOT NULL,
  target_id   TEXT    NOT NULL,
  verdict     TEXT    NOT NULL,
  note        TEXT    NOT NULL DEFAULT '',
  account_id  INTEGER NOT NULL REFERENCES account(id),
  created_at  TEXT    NOT NULL
);
-- Verdicts are append-only: a row is a thing someone said at a time, and
-- rewriting it would lose the fact that they once thought otherwise. The
-- current verdict is the newest row for that target.
CREATE INDEX IF NOT EXISTS verdict_target ON verdict(target_kind, target_id, id DESC);
"""


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    # Without this SQLite does not enforce the REFERENCES above at all.
    conn.execute("PRAGMA foreign_keys = ON")
    # A reader browsing while someone writes should not block or fail.
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


@contextmanager
def cursor(commit: bool = False) -> Iterator[sqlite3.Cursor]:
    conn = connect()
    try:
        cur = conn.cursor()
        yield cur
        if commit:
            conn.commit()
    finally:
        conn.close()


def init() -> None:
    with cursor(commit=True) as cur:
        cur.executescript(SCHEMA)


def fold(email: str) -> str:
    """The form two spellings of one address agree on."""
    return email.strip().lower()


def one(sql: str, args: tuple = ()) -> Optional[sqlite3.Row]:
    with cursor() as cur:
        cur.execute(sql, args)
        return cur.fetchone()


def all_rows(sql: str, args: tuple = ()) -> list:
    with cursor() as cur:
        cur.execute(sql, args)
        return cur.fetchall()


def write(sql: str, args: tuple = ()) -> int:
    with cursor(commit=True) as cur:
        cur.execute(sql, args)
        return cur.lastrowid
