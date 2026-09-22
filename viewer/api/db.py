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

import json
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
  created_at TEXT NOT NULL,
  -- Which OpenProject project this package's work is scheduled in. The board,
  -- a work package lookup and a new link all read inside it and nowhere else,
  -- so a developer on TICVAI is not shown somebody else's tickets. The id is
  -- what the API filters on; the identifier and name are what a person reads.
  -- Chosen by an admin on admin.html. Blank is "not chosen yet", and the work
  -- routes refuse rather than guess.
  pms_project_id  INTEGER,
  pms_identifier  TEXT NOT NULL DEFAULT '',
  pms_name        TEXT NOT NULL DEFAULT '',
  pms_set_at      TEXT,
  pms_set_by      INTEGER
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

-- Which slice of a project somebody owns.
--
-- **The third axis, and it is not the other two.** `account.role` says what a
-- person may do anywhere; `account_project` says which packages they may open;
-- this says which part of one is theirs. A team lead has one role and one
-- project and four platforms, and none of the three facts implies another.
--
-- `tag` is frontend or backend — the same two values `verdict.tag` carries, and
-- for the same stated reason: the question it answers is "whose queue is this
-- in", and two values is what makes it answerable. `platform` is P01, P02 and
-- so on, or NULL meaning the whole of that side.
--
-- The package already agrees that this is the unit: `lib/platforms.mjs` opens
-- with "a platform is an application somebody signs into... it is the unit a
-- delivery lead owns". This table is that sentence, stored.
--
-- **Owning a slice is about being notified and acting, never about reading.** A
-- team lead sees every change request and all of the activity on the project;
-- what `scope` decides is which ones reach their queue and which ones they may
-- settle. Two separate questions that one table would happily confuse, so the
-- comment is here rather than nowhere.
--
-- No row for an owner, an admin or a pm. They are not scoped, they are whole —
-- and a scope row for one of them would be a second, narrower answer to a
-- question that has already been answered.
CREATE TABLE IF NOT EXISTS scope (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  project_id TEXT    NOT NULL REFERENCES project(id) ON DELETE CASCADE,
  tag        TEXT    NOT NULL,
  -- NULL is "the whole of that side", which is a different statement from a
  -- row per platform and has to stay tellable from it: platforms get added, and
  -- a lead who owns the side should own the new one without anybody remembering.
  platform   TEXT,
  granted_by INTEGER NOT NULL REFERENCES account(id),
  granted_at TEXT    NOT NULL
);
-- One row per person per slice. The NULL platform does not collide with a named
-- one in SQLite's unique index -- NULLs are distinct -- which is correct here:
-- "the whole side" and "P01" are different grants and a person may hold both.
CREATE UNIQUE INDEX IF NOT EXISTS scope_once
  ON scope(account_id, project_id, tag, platform);
CREATE INDEX IF NOT EXISTS scope_by_slice ON scope(project_id, tag, platform);

-- A change to an OpenProject work package that somebody has been shown and has
-- not yet agreed to. Claude proposes; the person says yes; only then is it sent.
--
-- The token is what the apply has to present, and only its hash is kept, like
-- every other token here. `lock_version` is the version of the work package the
-- person was shown: if it has moved since, the apply is refused rather than
-- landing on top of a change they never saw. One use, fifteen minutes.
CREATE TABLE IF NOT EXISTS wp_proposal (
  id            INTEGER PRIMARY KEY,
  token_hash    TEXT    NOT NULL UNIQUE,
  account_id    INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  project_id    TEXT    NOT NULL,
  -- 'change' alters an existing work package; 'child' creates one under it.
  --
  -- One table for both, and the reason is the column nobody thinks about:
  -- `applied_at`, claimed with `UPDATE ... WHERE applied_at IS NULL`, is what
  -- makes a proposal single-use. A second table would need that mechanism
  -- written a second time, and the failure of the copy is silent — two quick
  -- presses making two tickets, which nobody notices until somebody wonders
  -- why a change request has two.
  kind          TEXT    NOT NULL DEFAULT 'change',
  -- For 'change', the work package being changed. For 'child', the parent it
  -- will hang under — empty when the change request came from no ticket.
  external_key  TEXT    NOT NULL,
  lock_version  INTEGER,
  status_id     INTEGER,
  status_name   TEXT    NOT NULL DEFAULT '',
  -- Whether that status closes the work package, as OpenProject said when the
  -- change was proposed. Recorded rather than re-asked at apply time, for the
  -- same reason `lock_version` is: the answer is part of what the person was
  -- shown. It is what the testing gate counts — a ticket is "closed" when
  -- OpenProject's own isClosed says so, never by a name matched here.
  status_closes INTEGER NOT NULL DEFAULT 0,
  percent_done  INTEGER,
  comment       TEXT    NOT NULL DEFAULT '',
  summary       TEXT    NOT NULL DEFAULT '',
  -- 'child' only. The change request this is for, what the ticket will say,
  -- which type it will be, and the id OpenProject gave it once it existed.
  change_number INTEGER,
  subject       TEXT    NOT NULL DEFAULT '',
  description   TEXT    NOT NULL DEFAULT '',
  type_id       INTEGER,
  type_name     TEXT    NOT NULL DEFAULT '',
  result_key    TEXT    NOT NULL DEFAULT '',
  created_at    TEXT    NOT NULL,
  expires_at    TEXT    NOT NULL,
  applied_at    TEXT
);
CREATE INDEX IF NOT EXISTS wp_proposal_by_account ON wp_proposal(account_id, created_at);

-- A change request: somebody building from the package found it wrong,
-- contradictory or missing something, and says so where the package's owners
-- will see it. Not a decision - a decision is settled; this is open until an
-- admin or a reviewer on the project accepts or rejects it, and done when the
-- package has been fixed (resolved_ref says by what). Internal only: a client
-- account neither reads nor writes these.
CREATE TABLE IF NOT EXISTS change_request (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id     TEXT    NOT NULL,
  -- CR-<number>, counted per project.
  number         INTEGER NOT NULL,
  target_kind    TEXT    NOT NULL,
  target_id      TEXT    NOT NULL,
  title          TEXT    NOT NULL,
  problem        TEXT    NOT NULL,
  -- The passages that show it, quoted - what makes it checkable.
  evidence       TEXT    NOT NULL DEFAULT '',
  -- JSON list of the ways it could be settled.
  options        TEXT    NOT NULL DEFAULT '[]',
  recommendation TEXT    NOT NULL DEFAULT '',
  -- Work cannot go on until it is settled.
  blocking       INTEGER NOT NULL DEFAULT 0,
  -- The OpenProject work package it came up in, when there was one. The
  -- *parent* of anything filed from this request.
  external_key   TEXT    NOT NULL DEFAULT '',
  -- The ticket filed for this request, once one has been. At most one, ever:
  -- this column is the guard, and a second attempt is answered with the key
  -- already here rather than with a second ticket. Set only through the
  -- propose-then-confirm flow, never by an import or a CSV.
  child_key      TEXT    NOT NULL DEFAULT '',
  child_at       TEXT,
  child_by       INTEGER REFERENCES account(id),
  status         TEXT    NOT NULL DEFAULT 'open',
  raised_by      INTEGER NOT NULL REFERENCES account(id),
  raised_at      TEXT    NOT NULL,
  -- 'claude' when filed through the connector, 'viewer' from the page.
  raised_via     TEXT    NOT NULL DEFAULT 'viewer',
  -- Whose queue this is in: a side of the house, and a platform within it.
  -- The pair `scope` grants, so a request finds the lead who owns that slice.
  -- Either may be blank, and blank is not an error — it means nobody has said,
  -- and a request nobody has routed is one for the super admin to triage
  -- rather than one quietly belonging to everybody.
  tag            TEXT    NOT NULL DEFAULT '',
  platform       TEXT    NOT NULL DEFAULT '',
  -- Who has taken it on, and when. **Not a status.** Picking a request up and
  -- settling it are different acts — the first says whose it is, the second
  -- says what was decided — and a request can sit picked and unsettled for a
  -- fortnight without that being a contradiction. Keeping it off `status` also
  -- leaves the spreadsheet round trip's four words exactly as they were.
  --
  -- `picked_at` being null on an open request older than two days is the whole
  -- of the escalation: it is a query, not a job, so there is no tick to miss.
  picked_by      INTEGER REFERENCES account(id),
  picked_at      TEXT,
  resolution     TEXT    NOT NULL DEFAULT '',
  -- What closed it: a commit, an ADR, a contract version.
  resolved_ref   TEXT    NOT NULL DEFAULT '',
  resolved_by    INTEGER REFERENCES account(id),
  resolved_at    TEXT,
  UNIQUE (project_id, number)
);
CREATE INDEX IF NOT EXISTS change_request_by_target
  ON change_request(project_id, target_kind, target_id, status);
-- The two questions the changes page asks that are not about one artefact:
-- "what is in my slice" and "what has nobody taken".
CREATE INDEX IF NOT EXISTS change_request_by_slice
  ON change_request(project_id, tag, platform, status);
CREATE INDEX IF NOT EXISTS change_request_unpicked
  ON change_request(project_id, status, picked_at);

-- A change request drafted by Claude and waiting for the person to agree.
-- Filing takes the one-use code; the draft expires like a work package
-- proposal does.
CREATE TABLE IF NOT EXISTS change_draft (
  id          INTEGER PRIMARY KEY,
  token_hash  TEXT    NOT NULL UNIQUE,
  account_id  INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  project_id  TEXT    NOT NULL,
  payload     TEXT    NOT NULL,
  created_at  TEXT    NOT NULL,
  expires_at  TEXT    NOT NULL,
  filed_at    TEXT
);

-- A credential this service holds on somebody's behalf, encrypted.
--
-- **Its own table, not a column on `account`.** Every other secret here is a
-- one-way hash; this one has to be usable later, as a token, so it is stored
-- reversibly. Keeping it out of the account row means the many places that read
-- an account — sign-in, the roster, `/auth/me`, every JOIN above — cannot carry
-- it out by accident. Reaching it takes naming this table on purpose.
--
-- `ciphertext` is Fernet, and the key is in the environment and never in here:
-- a stolen copy of this file is inert without it. See api/secrets.py.
--
-- `hint` is the last four characters in the clear, which is what a person is
-- shown so they can recognise which token they pasted. Never the token.
--
-- `kind` rather than a column per system, because the second credential is
-- coming — this is the shape that does not need another migration for it.
-- Which artefact a piece of scheduled work is about.
--
-- **This is the only thing the bridge stores about work, and it is the only
-- thing nothing else can say.** OpenProject holds the work packages — 23 epics,
-- 444 features, 2,173 tasks — and it is perfectly good at that. What it cannot
-- express is that WP #1841 is about screen `BO-102`, table `access.entitlement`
-- and `AccessService`, because it knows nothing about the package. The package
-- knows those names and nothing about the schedule. This table is the join, and
-- building anything else here would be recommitting CF-124: two independent
-- plans over the same work, neither referencing the other.
--
-- No id of our own for the work: `external_key` is OpenProject's number and
-- stays OpenProject's. Minting a second identifier is how the third plan starts.
--
-- Many-to-many on purpose. One work package usually touches several artefacts,
-- and one artefact is usually touched by several work packages over time.
--
-- `project_id` from the first row, though there is one package today. It is a
-- column now and a migration later, and the later one has to touch every row.
--
-- The `cached_*` columns are a copy of what OpenProject said at `synced_at`,
-- kept so a board can be drawn without fanning out one API call per row. They
-- are a cache and are labelled as one wherever they are shown: OpenProject is
-- the truth about status, always.
CREATE TABLE IF NOT EXISTS artefact_link (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id      TEXT    NOT NULL REFERENCES project(id) ON DELETE CASCADE,
  target_kind     TEXT    NOT NULL,
  target_id       TEXT    NOT NULL,
  external_system TEXT    NOT NULL DEFAULT 'openproject',
  external_key    TEXT    NOT NULL,
  url             TEXT    NOT NULL DEFAULT '',
  cached_subject  TEXT    NOT NULL DEFAULT '',
  cached_status   TEXT    NOT NULL DEFAULT '',
  cached_type     TEXT    NOT NULL DEFAULT '',
  cached_assignee TEXT    NOT NULL DEFAULT '',
  synced_at       TEXT    NOT NULL DEFAULT '',
  created_at      TEXT    NOT NULL,
  created_by      INTEGER REFERENCES account(id) ON DELETE SET NULL,
  -- The same artefact linked to the same work package twice is a duplicate row
  -- and a board that counts it twice, so the store refuses it rather than the
  -- three callers each remembering to check.
  UNIQUE (project_id, target_kind, target_id, external_system, external_key)
);
-- The two directions this is read from. Artefact → work is "what is scheduled
-- against this screen"; work → artefact is "what does this ticket touch", which
-- is the question an agent asks when it opens a branch.
CREATE INDEX IF NOT EXISTS artefact_link_by_target
  ON artefact_link(project_id, target_kind, target_id);
CREATE INDEX IF NOT EXISTS artefact_link_by_external
  ON artefact_link(project_id, external_system, external_key);

CREATE TABLE IF NOT EXISTS account_secret (
  account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  kind       TEXT    NOT NULL,
  ciphertext TEXT    NOT NULL,
  hint       TEXT    NOT NULL DEFAULT '',
  -- Which instance the credential is for. A token is only meaningful against
  -- the host it was issued by, and storing that with it is what lets somebody
  -- point at a different OpenProject without silently sending the old key.
  endpoint   TEXT    NOT NULL DEFAULT '',
  created_at TEXT    NOT NULL,
  updated_at TEXT    NOT NULL,
  PRIMARY KEY (account_id, kind)
);

-- ── where people sign in from ───────────────────────────────────────
--
-- Three tables and they answer three different questions, which is why this is
-- not one table with a flag on it:
--
--   ip_policy    is the allowlist switched on at all
--   ip_rule      which addresses it lets through
--   ip_sighting  where each account has actually been seen
--   ip_refusal   who was turned away, or would have been
--
-- **The whole thing ships off.** An allowlist installed armed is an allowlist
-- that locks its owner out of the machine they installed it from, and the only
-- honest way to choose the rules is to have watched the traffic first. So the
-- policy row starts armed = 0, every address is allowed, and the sightings
-- accumulate from the first request — the list of rules writes itself out of
-- what is in this table by the time anybody wants to switch it on.

CREATE TABLE IF NOT EXISTS ip_policy (
  -- One row, forever. The CHECK is the whole mechanism: a second row would be a
  -- second answer to "is this on", and the reader would have to pick.
  id         INTEGER PRIMARY KEY CHECK (id = 1),
  armed      INTEGER NOT NULL DEFAULT 0,
  changed_by INTEGER REFERENCES account(id),
  changed_at TEXT
);

CREATE TABLE IF NOT EXISTS ip_rule (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  -- Always stored as a network, never as a bare address: a single address is
  -- written 203.0.113.7/32 on the way in. One shape to compare means the
  -- matcher has one branch, and "is 203.0.113.7 already covered" is answerable
  -- without knowing which of the two spellings somebody used last time.
  cidr     TEXT    NOT NULL UNIQUE,
  -- "The Bombay office", "Chinmay at home". A rule nobody can attribute is a
  -- rule nobody dares delete, and an allowlist that only grows is one that
  -- stops meaning anything.
  label    TEXT    NOT NULL DEFAULT '',
  added_by INTEGER NOT NULL REFERENCES account(id),
  added_at TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS ip_sighting (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  ip         TEXT    NOT NULL,
  first_seen TEXT    NOT NULL,
  last_seen  TEXT    NOT NULL,
  hits       INTEGER NOT NULL DEFAULT 1,
  last_agent TEXT    NOT NULL DEFAULT '',
  last_path  TEXT    NOT NULL DEFAULT ''
);
-- Rolled up per account and address rather than a row per request, and that is
-- the difference between a table somebody reads and a table somebody archives.
-- A row per request would be tens of thousands a week to say the one thing
-- anybody wants from it: this person, this address, since when, how often,
-- most recently when. The cost is that you cannot reconstruct a session from
-- it — which is what ip_refusal is for, and refusals are rare enough to keep
-- whole.
CREATE UNIQUE INDEX IF NOT EXISTS ip_sighting_once ON ip_sighting(account_id, ip);
CREATE INDEX IF NOT EXISTS ip_sighting_recent ON ip_sighting(last_seen DESC);

CREATE TABLE IF NOT EXISTS ip_refusal (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  -- Null when nobody was signed in: a refusal at the door is still worth
  -- keeping, and it is the one that tells you somebody is knocking.
  account_id INTEGER REFERENCES account(id) ON DELETE SET NULL,
  -- Copied rather than joined, so the row still says who it was after the
  -- account is deleted. A security log that empties itself when an account
  -- goes is a security log that is useful for everything except the case it
  -- exists for.
  email      TEXT    NOT NULL DEFAULT '',
  ip         TEXT    NOT NULL,
  path       TEXT    NOT NULL DEFAULT '',
  at         TEXT    NOT NULL,
  -- 1: turned away. 0: **would have been** turned away, recorded while the
  -- policy is off. The second is the dry run, and it is the reason arming this
  -- is not a leap of faith — the list of people it is about to lock out is a
  -- query against rows that were written by real traffic, not a guess from a
  -- list of rules.
  armed      INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ip_refusal_recent ON ip_refusal(at DESC);

-- ── tested in batches, and checked by somebody else ─────────────────
--
-- Every so many tickets a developer closes, they stop and test what they have
-- built, and **a teammate confirms they did**. Two rules, and they are the same
-- mechanism seen from either end:
--
--   The gate: closing the next ticket is refused once the open batch is full.
--   Not a reminder — the service owns the write path that closes a ticket, so
--   this is the one place the rule can be a rule rather than a convention.
--
--   The checker: the person who did the testing cannot be the person who says
--   it was done. Otherwise the gate is a box somebody ticks on the way past,
--   which is a slower way of not testing.
--
-- A batch is per person and per project. It opens on the first close after the
-- last one passed, fills as tickets close, and is spent when a teammate passes
-- it. Nothing here schedules or reminds: whether a batch is full is a count of
-- its rows, asked at the moment somebody tries to close the next ticket.

CREATE TABLE IF NOT EXISTS test_batch (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id   TEXT    NOT NULL REFERENCES project(id) ON DELETE CASCADE,
  -- Whose. The gate is personal: one developer closing ten tickets has to test,
  -- and it is not held up by what anybody else has closed.
  account_id   INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  opened_at    TEXT    NOT NULL,
  -- The maker's half: what they tested and what it showed.
  submitted_at TEXT,
  notes        TEXT    NOT NULL DEFAULT '',
  evidence     TEXT    NOT NULL DEFAULT '',
  -- The checker's. `verdict` is '' until somebody has looked, then 'passed' or
  -- 'failed'. A failed batch is not reopened for editing: it stays as it was
  -- said, and the maker submits it again — so the record keeps the fact that it
  -- was sent back, which is the part worth having.
  checker_id   INTEGER REFERENCES account(id),
  checked_at   TEXT,
  verdict      TEXT    NOT NULL DEFAULT '',
  checker_note TEXT    NOT NULL DEFAULT ''
);
-- "The open batch for this person on this project" is asked on every close, so
-- it is an index rather than a scan. Open means no passing verdict yet.
CREATE INDEX IF NOT EXISTS test_batch_open
  ON test_batch(account_id, project_id, verdict, opened_at);

-- ── a diagram somebody arranged by hand ────────────────────────────
--
-- The package is what the vendor shipped and stays as received — that rule is
-- at the top of this file and this does not break it. A saved arrangement
-- lives here and is laid over the generated diagram when it is drawn; the
-- YAML on disk is never written to.
--
-- **What is saved is the arrangement, not the content.** Where each box was
-- dropped, what was hidden, what was annotated. The nodes and the edges still
-- come from the package every time, so a diagram cannot quietly disagree with
-- the contracts about what exists — only about where it sits on the page.
--
-- Versions are kept and never deleted. Saving a new one retires the one before
-- it; retired versions stay readable to whoever can publish, because "we just
-- do not show it" is a different thing from "it is gone", and the second one is
-- how a rearrangement nobody liked becomes unrecoverable.
CREATE TABLE IF NOT EXISTS diagram_version (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id  TEXT    NOT NULL REFERENCES project(id) ON DELETE CASCADE,
  -- Which diagram: `graph:spine`, `data:orders`, `states:WorkOrder`. The view
  -- and its scope, because the same view at two scopes is two pictures.
  diagram     TEXT    NOT NULL,
  -- Counted per diagram, from 1. Not a timestamp: people say "go back to v2".
  version     INTEGER NOT NULL,
  -- {"nodes": {id: {x, y}}, "hidden": [id], "notes": [{x, y, text}]}
  layout      TEXT    NOT NULL,
  -- What the generated diagram looked like when this was arranged, as a hash
  -- the page computes from the node ids it drew. **This is the whole mitigation
  -- for the thing that makes hand-editing dangerous**: the package moves on,
  -- and an arrangement made against an older shape is still displayed as if it
  -- were current. Comparing hashes lets the page say so instead.
  source_hash TEXT    NOT NULL DEFAULT '',
  note        TEXT    NOT NULL DEFAULT '',
  -- 'current' or 'retired'. One current per diagram per project, enforced by
  -- the route rather than by a constraint, because the swap is two writes and
  -- a unique index would refuse the moment between them.
  status      TEXT    NOT NULL DEFAULT 'current',
  created_by  INTEGER NOT NULL REFERENCES account(id),
  created_at  TEXT    NOT NULL,
  retired_by  INTEGER REFERENCES account(id),
  retired_at  TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS diagram_version_once
  ON diagram_version(project_id, diagram, version);
CREATE INDEX IF NOT EXISTS diagram_version_current
  ON diagram_version(project_id, diagram, status);

-- ── what an hour of somebody's time costs ──────────────────────────
--
-- **ADAM holds the rate and nothing else.** The hours come from the work
-- packages, the cost is multiplied on read, and no total is ever stored — so
-- there is no second number to go stale when somebody logs time on Friday, and
-- no figure in this file that anybody could mistake for an invoice.
--
-- Keyed on the OpenProject assignee's display name rather than on an ADAM
-- account, because that is what the hours actually arrive attached to. A join
-- through an account would need a mapping nobody maintains, and a rate that
-- silently matched nobody would read as somebody working for free. `account_id`
-- is carried when the two are known to be the same person, for display only.
CREATE TABLE IF NOT EXISTS rate (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id TEXT    NOT NULL REFERENCES project(id) ON DELETE CASCADE,
  -- Exactly as OpenProject spells it. Compared case-insensitively on read.
  person     TEXT    NOT NULL,
  account_id INTEGER REFERENCES account(id) ON DELETE SET NULL,
  -- Stored in the smallest unit, so no total is ever the sum of floats: a rate
  -- of 4,500.50 is 450050. Divided once, at the edge, for display.
  hourly     INTEGER NOT NULL,
  currency   TEXT    NOT NULL DEFAULT 'INR',
  note       TEXT    NOT NULL DEFAULT '',
  set_by     INTEGER NOT NULL REFERENCES account(id),
  set_at     TEXT    NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS rate_once ON rate(project_id, person);

-- ── what the agent did, and what went wrong ─────────────────────────
--
-- Claude Code runs on the developer's machine and ADAM does not, so the only
-- way to see how much the agent is being used — and where it keeps failing —
-- is for the machine to say. Hooks write locally and flush here in one post
-- when a session ends.
--
-- **Narrow on purpose, and the narrowness is the design.** What is kept is
-- which tool ran, whether it worked, how long it took, and which ticket was
-- open. What is *not* kept is prompts, file contents, diffs, commands or tool
-- arguments. Those would answer richer questions and would put every secret
-- anybody ever pasted into a prompt into this file — which is exported as CSV,
-- backed up, and read by more people than would ever be told. A log that is
-- uncomfortable to keep is a log that gets turned off.
--
-- The cost is real and worth naming: you can see that Edit failed eleven times
-- on one ticket and not what it was trying to edit. The answer to that is to
-- open the ticket, not to widen this.

CREATE TABLE IF NOT EXISTS agent_session (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  -- The agent's own session id, so a flush that arrives twice — a retry, a
  -- second SessionEnd — updates one row instead of making a second.
  key          TEXT    NOT NULL UNIQUE,
  account_id   INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  project_id   TEXT    NOT NULL,
  -- The ticket that was open, when the folder said so. This is what turns
  -- "the agent ran for three hours" into "the agent ran for three hours on
  -- #6046", which is the only form of it anybody can act on.
  external_key TEXT    NOT NULL DEFAULT '',
  -- The repository's folder name, never its path. A path carries the person's
  -- machine, their home directory and sometimes a client's name in it.
  repo         TEXT    NOT NULL DEFAULT '',
  host         TEXT    NOT NULL DEFAULT '',
  agent        TEXT    NOT NULL DEFAULT '',
  started_at   TEXT    NOT NULL,
  ended_at     TEXT,
  -- Time with something actually happening, as against wall clock. A session
  -- left open over lunch is not two hours of agent use, so gaps longer than
  -- the idle threshold are not counted. Computed where the events are, and
  -- stored because it cannot be recovered once the events are trimmed.
  active_ms    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS agent_session_who
  ON agent_session(account_id, started_at DESC);
CREATE INDEX IF NOT EXISTS agent_session_ticket
  ON agent_session(project_id, external_key);

CREATE TABLE IF NOT EXISTS agent_event (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES agent_session(id) ON DELETE CASCADE,
  at         TEXT    NOT NULL,
  -- 'tool', 'prompt', 'stop', 'notify'. A prompt event records that there was
  -- one and when — never a word of it.
  kind       TEXT    NOT NULL,
  tool       TEXT    NOT NULL DEFAULT '',
  ok         INTEGER NOT NULL DEFAULT 1,
  -- A classified word, not a message: 'refused', 'not-found', 'timeout',
  -- 'conflict', 'error'. A message would carry paths and snippets, which is
  -- exactly what this table is for not carrying.
  error_kind TEXT    NOT NULL DEFAULT '',
  ms         INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS agent_event_session ON agent_event(session_id, at);
CREATE INDEX IF NOT EXISTS agent_event_tool ON agent_event(tool, ok);

CREATE TABLE IF NOT EXISTS test_batch_item (
  batch_id     INTEGER NOT NULL REFERENCES test_batch(id) ON DELETE CASCADE,
  external_key TEXT    NOT NULL,
  subject      TEXT    NOT NULL DEFAULT '',
  status_name  TEXT    NOT NULL DEFAULT '',
  closed_at    TEXT    NOT NULL,
  -- What the working tree was at, if the connector could tell us. Nothing here
  -- is enforceable — ADAM cannot see anybody's repository, and a developer who
  -- does not use the connector sends nothing — so this is evidence and a nudge,
  -- never a gate. See the commit note in main.py.
  head_sha     TEXT    NOT NULL DEFAULT '',
  dirty        INTEGER NOT NULL DEFAULT 0,
  -- One row per ticket per batch: closing the same ticket twice is one closure
  -- as far as the gate is concerned, or reopening and reclosing would be a way
  -- to fill a batch without doing any work.
  PRIMARY KEY (batch_id, external_key)
);
"""

# The project every row that predates projects belongs to.
#
# There was one package and it was this one, so every verdict, every mention and
# every invite in an existing store is about it. Named once here rather than
# spelled into six statements below, and used as the column default so the
# backfill for `verdict` is "the column now exists" rather than an UPDATE.
FIRST_PROJECT = "ticvai"
# (OpenProject id, identifier, name) for FIRST_PROJECT. See the migration.
FIRST_PMS_PROJECT = (153, "ticvai", "TICVAI")


# The viewer's package registry. TICVAI_PROJECTS points somewhere else, for a harness.
PROJECTS_PATH = Path(os.environ.get(
    "TICVAI_PROJECTS", Path(__file__).parent.parent / "projects.json"))


def registered_projects() -> list:
    """(id, name) for each active entry in projects.json. Empty when the file is
    missing or unreadable: the accounts service does not need it to run."""
    try:
        entries = json.loads(PROJECTS_PATH.read_text(encoding="utf-8")).get("projects") or []
    except (OSError, ValueError):
        return []
    return [
        (entry["id"], entry.get("name") or entry["id"])
        for entry in entries
        if isinstance(entry, dict) and entry.get("id") and entry.get("active", True)
    ]


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
    # The six below are change request kinds only — a verdict is never given on
    # one. They are here rather than in a second map because "which side of the
    # house is this" is one question, and two maps answering it is how a flow
    # comes to be frontend in one place and backend in another.
    "flow": "frontend",
    "platform": "frontend",
    "contract": "backend",
    "service": "backend",
    "event": "backend",
    # `adr` and `other` are deliberately absent. A decision is not a side of the
    # house and neither is "other", so guessing would route them somewhere on no
    # evidence. They arrive untagged, which is a state the page shows and
    # somebody answers — a worse default is worse than none.
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

        # Which git identity an account commits under. Not a secret, so it sits
        # on the account row rather than in `account_secret` — and it is what
        # lets a commit be matched to the person who owns a work package.
        account_columns = {row[1] for row in cur.execute("PRAGMA table_info(account)")}
        if "git_email" not in account_columns:
            # Blank rather than a copy of `email`: they are the same for most
            # people and guessing would produce a value nobody chose, which then
            # reads as confirmed. Blank is honestly "not stated yet".
            cur.execute("ALTER TABLE account ADD COLUMN git_email TEXT NOT NULL DEFAULT ''")

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
        # Every other package the viewer serves gets a row too, so registering
        # one in projects.json and restarting is all it takes for an admin to
        # see it. Existing rows are left alone, name and active flag included.
        for project_id, name in registered_projects():
            cur.execute(
                "INSERT OR IGNORE INTO project (id, name, active, created_at) VALUES (?, ?, 1, ?)",
                (project_id, name, _stamp()),
            )

        # Where a change request belongs, and who has taken it on. Added to
        # stores made before the columns existed; the fresh schema above already
        # has them.
        change_columns = {row[1] for row in cur.execute("PRAGMA table_info(change_request)")}
        for column, ddl in (
            ("tag", "TEXT NOT NULL DEFAULT ''"),
            ("platform", "TEXT NOT NULL DEFAULT ''"),
            ("picked_by", "INTEGER"),
            ("picked_at", "TEXT"),
        ):
            if column not in change_columns:
                cur.execute(f"ALTER TABLE change_request ADD COLUMN {column} {ddl}")
        # Backfilled from the kind, the same starting position a new one gets,
        # and only where nobody has said otherwise. Leaving them blank would put
        # every request that predates routing into the "nobody has said" bucket
        # the page asks the super admin to clear — which would be true of the
        # column and false of the work.
        #
        # `platform` is not backfilled and cannot be: this service does not read
        # the packages, so it has no way to know that POS-002 is P04. They arrive
        # as "the whole of that side", which is the honest reading of a request
        # filed before anybody was asked.
        for kind, tag in TAG_OF.items():
            cur.execute(
                "UPDATE change_request SET tag = ? WHERE target_kind = ? AND tag = ''",
                (tag, kind),
            )

        # Which OpenProject project each package reads. Added to stores made
        # before the columns existed; the fresh schema above already has them.
        project_columns = {row[1] for row in cur.execute("PRAGMA table_info(project)")}
        for column, ddl in (
            ("pms_project_id", "INTEGER"),
            ("pms_identifier", "TEXT NOT NULL DEFAULT ''"),
            ("pms_name", "TEXT NOT NULL DEFAULT ''"),
            ("pms_set_at", "TEXT"),
            ("pms_set_by", "INTEGER"),
        ):
            if column not in project_columns:
                cur.execute(f"ALTER TABLE project ADD COLUMN {column} {ddl}")
        # TICVAI's work lives in the `ticvai` project on pms.softlabsgroup.in
        # (id 153). Filled in only while nobody has chosen, so an admin's later
        # choice is never put back.
        cur.execute(
            "UPDATE project SET pms_project_id = ?, pms_identifier = ?, pms_name = ?, "
            "pms_set_at = ? WHERE id = ? AND pms_project_id IS NULL AND pms_set_at IS NULL",
            (FIRST_PMS_PROJECT[0], FIRST_PMS_PROJECT[1], FIRST_PMS_PROJECT[2],
             _stamp(), FIRST_PROJECT),
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

        # ---- a change request can become a ticket --------------------------
        #
        # Two tables and the same reason: the columns are new, the stores are
        # not. `child_key` is the guard that stops one request making two
        # tickets, so a store where it silently did not exist would answer
        # "already filed" never and file forever.
        have = {row[1] for row in cur.execute("PRAGMA table_info(change_request)")}
        if "child_key" not in have:
            cur.execute(
                "ALTER TABLE change_request ADD COLUMN child_key TEXT NOT NULL DEFAULT ''")
            cur.execute("ALTER TABLE change_request ADD COLUMN child_at TEXT")
            # No REFERENCES: SQLite cannot add a column with a foreign key to an
            # existing table. The constraint on the fresh schema above is the
            # one that matters from here on.
            cur.execute("ALTER TABLE change_request ADD COLUMN child_by INTEGER")

        have = {row[1] for row in cur.execute("PRAGMA table_info(wp_proposal)")}
        if "status_closes" not in have:
            # 0 is right for every row that already exists: whether a status
            # closed was not asked when they were written, and a proposal older
            # than this deploy has either been applied or lapsed.
            cur.execute(
                "ALTER TABLE wp_proposal ADD COLUMN status_closes INTEGER NOT NULL DEFAULT 0")
        if "kind" not in have:
            # 'change' is right for every row that already exists — creating was
            # not possible when they were written — so the default does the
            # backfill and there is nothing to update.
            cur.execute(
                "ALTER TABLE wp_proposal ADD COLUMN kind TEXT NOT NULL DEFAULT 'change'")
            cur.execute("ALTER TABLE wp_proposal ADD COLUMN change_number INTEGER")
            cur.execute("ALTER TABLE wp_proposal ADD COLUMN subject TEXT NOT NULL DEFAULT ''")
            cur.execute("ALTER TABLE wp_proposal ADD COLUMN description TEXT NOT NULL DEFAULT ''")
            cur.execute("ALTER TABLE wp_proposal ADD COLUMN type_id INTEGER")
            cur.execute("ALTER TABLE wp_proposal ADD COLUMN type_name TEXT NOT NULL DEFAULT ''")
            cur.execute("ALTER TABLE wp_proposal ADD COLUMN result_key TEXT NOT NULL DEFAULT ''")

        # ---- the allowlist, off -------------------------------------------
        #
        # The row exists from the first boot so that reading the policy is a
        # SELECT rather than a SELECT-or-default, and every reader agrees about
        # what "not configured" means. `armed = 0` is the shipped state and the
        # one an existing store lands in: turning it on is a decision somebody
        # makes on the page, never something a deploy does on their behalf.
        cur.execute(
            "INSERT OR IGNORE INTO ip_policy (id, armed) VALUES (1, 0)")


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
