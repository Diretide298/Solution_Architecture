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
  -- Which layer the reviewer was standing in when they said it. Derivable from
  -- the kind today, and recorded anyway: it is what the reviewer was actually
  -- looking at, and a kind that later appears in two layers would make the
  -- derivation quietly wrong rather than absent.
  layer       TEXT    NOT NULL DEFAULT '',
  -- Which side of the house the work lands on, chosen by the reviewer rather
  -- than derived. Separate from `layer` on purpose: the layer is where they
  -- were standing, and the tag is who has to do something about it. A screen
  -- that renders correctly against an endpoint that returns the wrong total is
  -- seen in the frontend and fixed in the backend, and one column cannot say
  -- both.
  tag         TEXT    NOT NULL DEFAULT '',
  verdict     TEXT    NOT NULL,
  note        TEXT    NOT NULL DEFAULT '',
  account_id  INTEGER NOT NULL REFERENCES account(id),
  created_at  TEXT    NOT NULL,
  -- Marked complete by a reviewer once the thing they asked for is done. Not a
  -- verdict and not a replacement for one: the verdict stays as said, and this
  -- records that it has been dealt with. Nullable because "not done" is the
  -- absence of a date rather than a flag that could disagree with one.
  done_at     TEXT,
  done_by     INTEGER REFERENCES account(id)
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


# kind -> the layer it is reviewed from. Used to fill the column in for rows
# recorded before it existed, and as the fallback when a caller does not say.
LAYER_OF = {
    "screen": "frontend",
    "board": "frontend",
    "operation": "contracts",
    "table": "backend",
    "module": "modules",
}

# kind -> which side of the house it lands on by default. Only a starting
# position for the control: a screen blocked on an endpoint is tagged backend
# by the person who found it, which is the whole reason the tag is chosen and
# not derived. An operation defaults to backend because somebody builds the
# endpoint before anybody calls it.
TAG_OF = {
    "screen": "frontend",
    "board": "frontend",
    "operation": "backend",
    "table": "backend",
    "module": "backend",
}


def init() -> None:
    with cursor(commit=True) as cur:
        cur.executescript(SCHEMA)
        # CREATE TABLE IF NOT EXISTS does nothing to a table that is already
        # there, so a store made before `layer` existed keeps its old shape and
        # every insert naming the column fails. Add it, then fill it in from the
        # kind, which is what it would have said at the time.
        have = {row[1] for row in cur.execute("PRAGMA table_info(verdict)")}
        if "layer" not in have:
            cur.execute("ALTER TABLE verdict ADD COLUMN layer TEXT NOT NULL DEFAULT ''")
            for kind, layer in LAYER_OF.items():
                cur.execute(
                    "UPDATE verdict SET layer = ? WHERE target_kind = ? AND layer = ''",
                    (layer, kind),
                )
        if "tag" not in have:
            cur.execute("ALTER TABLE verdict ADD COLUMN tag TEXT NOT NULL DEFAULT ''")
            # Backfilled from the kind, which is what it would have defaulted to
            # had the column existed. A row left blank would drop out of every
            # tag filter and read as untagged work rather than old work.
            for kind, tag in TAG_OF.items():
                cur.execute(
                    "UPDATE verdict SET tag = ? WHERE target_kind = ? AND tag = ''",
                    (tag, kind),
                )
        # Two columns, added together, checked separately: a store that got one
        # and not the other is a store an interrupted migration left behind.
        if "done_at" not in have:
            cur.execute("ALTER TABLE verdict ADD COLUMN done_at TEXT")
        if "done_by" not in have:
            # No REFERENCES here: SQLite cannot add a column with a foreign key
            # to an existing table, and the constraint on the fresh schema above
            # is the one that matters for a store made from now on.
            cur.execute("ALTER TABLE verdict ADD COLUMN done_by INTEGER")


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
