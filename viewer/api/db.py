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
from datetime import datetime, timezone
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

CREATE TABLE IF NOT EXISTS reset (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  -- Bound to the account, not to an address. An invite fixes an address that
  -- has no account yet; this one starts from the account that already exists,
  -- so nothing about who it is for can be argued over later — and changing
  -- somebody's address does not strand a live reset link on the old one.
  account_id   INTEGER NOT NULL REFERENCES account(id),
  token_hash   TEXT    NOT NULL UNIQUE,
  created_by   INTEGER REFERENCES account(id),
  created_at   TEXT    NOT NULL,
  expires_at   TEXT    NOT NULL,
  used_at      TEXT,
  revoked_at   TEXT
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
  -- Whose review this is: 'internal' or 'client'. Taken from the account's
  -- role at the moment of writing and never from the request, because it is
  -- the one field a caller would have a reason to lie about.
  --
  -- It exists so the two reviews can be read apart. A client signing off is
  -- worth having and is not the same act as the team signing off: the current
  -- verdict is the newest row per artefact, so without this a client's
  -- approval would silently become the standing verdict on something the team
  -- had rejected. Two tracks on one artefact, neither overwriting the other.
  audience    TEXT    NOT NULL DEFAULT 'internal',
  verdict     TEXT    NOT NULL,
  note        TEXT    NOT NULL DEFAULT '',
  account_id  INTEGER NOT NULL REFERENCES account(id),
  created_at  TEXT    NOT NULL,
  -- Marked complete by a reviewer once the thing they asked for is done. Not a
  -- verdict and not a replacement for one: the verdict stays as said, and this
  -- records that it has been dealt with. Nullable because "not done" is the
  -- absence of a date rather than a flag that could disagree with one.
  done_at     TEXT,
  done_by     INTEGER REFERENCES account(id),
  -- An admin looked at what was marked done and did not accept it. Kept beside
  -- the completion rather than undoing it, so which one stands is decided by
  -- which happened last: mark done, sent back, marked done again. Clearing the
  -- completion instead would lose the fact that somebody had thought it
  -- finished, and clearing the rejection on the next attempt would lose the
  -- reason it was not.
  --
  -- The note is not optional. Sending work back without saying why is how it
  -- comes back the same.
  -- How it was answered when it was closed: built, wired, answered, accepted,
  -- or approved with nothing to do. The tracker's "Our verdict" column. Kept
  -- beside done_at rather than replacing it, because "when" and "how" are two
  -- questions and a report asks them separately.
  done_response  TEXT NOT NULL DEFAULT '',
  sent_back_at   TEXT,
  sent_back_by   INTEGER REFERENCES account(id),
  sent_back_note TEXT NOT NULL DEFAULT ''
);
-- Verdicts are append-only: a row is a thing someone said at a time, and
-- rewriting it would lose the fact that they once thought otherwise. The
-- current verdict is the newest row for that target.
CREATE INDEX IF NOT EXISTS verdict_target ON verdict(target_kind, target_id, audience, id DESC);

-- Somebody named in a note. A row per person per verdict, rather than parsing
-- the note again on every read: the note is prose and people get renamed, and
-- a mention that stopped resolving because somebody changed their display name
-- would be a notification that silently never arrives.
--
-- ON DELETE CASCADE because a discarded verdict must take its mentions with
-- it. Without it, discarding a note would leave somebody with a notification
-- pointing at a row that no longer exists.
CREATE TABLE IF NOT EXISTS mention (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  verdict_id INTEGER NOT NULL REFERENCES verdict(id) ON DELETE CASCADE,
  account_id INTEGER NOT NULL REFERENCES account(id),
  created_at TEXT    NOT NULL,
  -- When they looked at it. Null is unread; a date is what makes the count
  -- go down rather than a flag that could disagree with one.
  seen_at    TEXT
);
CREATE INDEX IF NOT EXISTS mention_for ON mention(account_id, seen_at, id DESC);
CREATE INDEX IF NOT EXISTS mention_verdict ON mention(verdict_id);

-- One delivery package. The viewer's projects.json says where each one is on
-- disk; this says who may read it and what its verdicts belong to, which are
-- questions about people rather than about paths.
--
-- The id is the same string the viewer uses in `/pkg/<id>/`, so a permission
-- and a URL cannot drift apart into two spellings of one project.
CREATE TABLE IF NOT EXISTS project (
  id         TEXT PRIMARY KEY,
  name       TEXT NOT NULL DEFAULT '',
  -- Off rather than deleted. A closed project still owns its verdicts, and the
  -- people who wrote them are still entitled to read what they wrote.
  active     INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL
);

-- Who may read which project, and as what.
--
-- `account.role` used to answer this on its own, which was honest while there
-- was one package to have a role on. Reviewer-or-client is a fact about a person
-- *on a project* \u2014 the same person can be a reviewer on one and a client on
-- another \u2014 so it lives here. `account.role` keeps only the part that was never
-- per-project: admin, meaning who may invite, reset and manage.
--
-- A missing row is no access. That is the whole check: there is no "everyone
-- can read everything" flag to forget to turn off.
CREATE TABLE IF NOT EXISTS account_project (
  account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  project_id TEXT    NOT NULL REFERENCES project(id) ON DELETE CASCADE,
  role       TEXT    NOT NULL DEFAULT 'reviewer',
  created_at TEXT    NOT NULL,
  PRIMARY KEY (account_id, project_id)
);
CREATE INDEX IF NOT EXISTS account_project_by_project ON account_project(project_id, role);
"""

# The project every row that predates projects belongs to.
#
# There was one package and it was this one, so every verdict, every mention and
# every invite in an existing store is about it. Named once here rather than
# spelled into six statements below, and used as the column default so the
# backfill for `verdict` is "the column now exists" rather than an UPDATE.
FIRST_PROJECT = "ticvai"


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
    # A state model is the rules a status may move by, and a schema is a group
    # of tables. Both are somebody's build before they are anybody's screen.
    "state": "backend",
    "schema": "backend",
}


def _stamp() -> str:
    """The same shape security.stamp() writes.

    Spelled here rather than imported: db.py has no other use for security, and
    pulling argon2 into it to write two timestamps at boot is a dependency for
    the sake of one line.
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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
        if "audience" not in have:
            cur.execute(
                "ALTER TABLE verdict ADD COLUMN audience TEXT NOT NULL DEFAULT 'internal'")
            # Every existing row is internal by construction — a client could
            # not write one until now — so the default is already right and
            # there is nothing to backfill.
            #
            # The index has to be rebuilt by hand: CREATE INDEX IF NOT EXISTS
            # above leaves the old two-column one in place, and "the newest row
            # for this artefact and this audience" is a different lookup.
            cur.execute("DROP INDEX IF EXISTS verdict_target")
            cur.execute(
                "CREATE INDEX verdict_target "
                "ON verdict(target_kind, target_id, audience, id DESC)")
        if "done_by" not in have:
            # No REFERENCES here: SQLite cannot add a column with a foreign key
            # to an existing table, and the constraint on the fresh schema above
            # is the one that matters for a store made from now on.
            cur.execute("ALTER TABLE verdict ADD COLUMN done_by INTEGER")
        if "done_response" not in have:
            cur.execute(
                "ALTER TABLE verdict ADD COLUMN done_response TEXT NOT NULL DEFAULT ''")
        if "sent_back_at" not in have:
            cur.execute("ALTER TABLE verdict ADD COLUMN sent_back_at TEXT")
            cur.execute("ALTER TABLE verdict ADD COLUMN sent_back_by INTEGER")
            cur.execute(
                "ALTER TABLE verdict ADD COLUMN sent_back_note TEXT NOT NULL DEFAULT ''")

        # ---- projects ------------------------------------------------------
        #
        # A verdict is about an artefact in a package, and until now there was
        # one package, so it did not have to say which. The default does the
        # backfill: every row that exists was written about TICVAI because there
        # was nothing else to write about, so the column is correct for all of
        # them the moment it exists. No UPDATE, and none of the risk one carries
        # over a store with live data in it.
        if "project_id" not in have:
            # SQLite will not take a bound parameter in a DEFAULT clause, so this
            # is interpolated \u2014 from the constant above rather than a literal,
            # so the project still has one spelling in this file. FIRST_PROJECT
            # is a module constant and not input; nothing here comes off a
            # request.
            cur.execute(
                f"ALTER TABLE verdict ADD COLUMN project_id TEXT NOT NULL "
                f"DEFAULT '{FIRST_PROJECT}'"
            )
            # "The newest verdict for this artefact" is now a question within a
            # project: two packages may both have a `table:orders.sales_order`,
            # and they are not the same artefact. Rebuilt by hand for the same
            # reason the audience column rebuilt it \u2014 CREATE INDEX IF NOT EXISTS
            # leaves the narrower one in place.
            cur.execute("DROP INDEX IF EXISTS verdict_target")
            cur.execute(
                "CREATE INDEX verdict_target "
                "ON verdict(project_id, target_kind, target_id, audience, id DESC)")

        invite_columns = {row[1] for row in cur.execute("PRAGMA table_info(invite)")}
        if "project_id" not in invite_columns:
            # An invite grants access to a project, so it has to name one. Live
            # invites were issued when there was one, and that is what they meant.
            cur.execute(
                f"ALTER TABLE invite ADD COLUMN project_id TEXT NOT NULL "
                f"DEFAULT '{FIRST_PROJECT}'"
            )

        # The project row itself, so the foreign keys above have something to
        # point at. INSERT OR IGNORE: a store that already has it is left alone,
        # including a name somebody has since edited.
        cur.execute(
            "INSERT OR IGNORE INTO project (id, name, active, created_at) VALUES (?, ?, 1, ?)",
            (FIRST_PROJECT, "TICVAI", _stamp()),
        )

        # The one backfill in the whole migration: everybody keeps exactly the
        # access they have today, on the one project that exists today. Without
        # it, the first deploy would sign everybody out of everything \u2014 an
        # empty account_project is no access, by design.
        #
        # `role` comes off the account, so a client stays a client. Admin is not
        # a project role, so an admin lands here as a reviewer and keeps being an
        # admin through account.role, which is where that has always lived.
        cur.execute(
            "INSERT OR IGNORE INTO account_project (account_id, project_id, role, created_at) "
            "SELECT id, ?, CASE WHEN role = 'client' THEN 'client' ELSE 'reviewer' END, ? "
            "FROM account",
            (FIRST_PROJECT, _stamp()),
        )


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


def change(sql: str, args: tuple = ()) -> int:
    """A write whose answer is *how many rows moved*, not what id was made.

    `write` returns lastrowid, which is the right answer for an INSERT and a
    meaningless one for a DELETE or an UPDATE — SQLite leaves it holding
    whatever the connection inserted last, so a caller counting deletions with
    it gets a number that looks plausible and is unrelated.
    """
    with cursor(commit=True) as cur:
        cur.execute(sql, args)
        return cur.rowcount
