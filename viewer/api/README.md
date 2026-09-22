# Accounts and validation

The stateful half of the viewer. The Node server (`server.mjs`, port 4173)
serves the delivery package — contracts, schemas, boards, lineage. It reads,
and holds nothing. This service holds what a person *writes*: who they are, and
what they decided about an artefact.

They are separate because the readers are ~5,400 lines of working, harnessed
code. Porting them to Python would buy nothing and risk plenty.

## Running it

```
pip install -r api/requirements.txt
python -m uvicorn api.main:app --port 8787
```

Port **8787**, not 8000 — on this machine 8000 falls in a range Windows
reserves, and binding it fails with `Errno 10013`.

Interactive API docs at `http://localhost:8787/docs`.

## The first account

Invites are made by an admin, which leaves the question of where the first
admin comes from. From a terminal, deliberately:

```
python -m api.cli admin chinmay.parab@softlabsgroup.com
```

Then everyone else is invited from the viewer, or from here:

```
python -m api.cli invite asha@softlabsgroup.com --role reviewer
python -m api.cli list
```

## Roles

Seven, on three axes that are deliberately not one.

**What you may do anywhere** is `account.role`:

| | |
|---|---|
| `owner` | the super admin. Everything an admin may, plus the Build layer, the IP allowlist and granting roles. |
| `admin` | invites, resets, the registers, the bulk settles. |
| `pm` | delivery oversight. Reads what an admin reads; settles nothing. |
| `lead` | a team lead. Sees all activity and every change request; acts on the platforms they own. |
| `dev` | a developer. Their own work. |
| `reviewer` | records verdicts on the package. |
| `client` | outside the company: reads everything but the decisions, records nothing. |

**Which packages you may open** is `account_project`, and its role is only ever
reviewer or client — the same person can be a reviewer on one package and a
client on another.

**Which slice of a package is yours** is `scope`: a side (frontend or backend)
and a platform within it, or the whole side. Only a `lead` or a `dev` holds one;
an owner, an admin and a pm are whole rather than scoped.

Seeing and acting are separate. A team lead reads every change request on the
project and is notified about, and may settle, the ones in their scope.

Three predicates in `security.py` answer these rather than any string
comparison — `is_admin`, `is_owner`, `may_settle` — and `isAdmin` / `isOwner` in
`public/validation.js` answer the same question for drawing. **A `role == "admin"`
left anywhere is a refusal of the super admin**, which is the one way this model
goes quietly wrong.

`owner` is granted from the machine and nowhere else:

```
python -m api.cli owner chinmay.parab@softlabsgroup.com
python -m api.cli owner chinmay.parab@softlabsgroup.com --revoke --to admin
```

`/api/accounts/{id}/role` refuses it in both directions and an invite cannot
carry it, so becoming or unmaking the super admin takes a shell here. The CLI
refuses to leave nobody able to administer.

## Where a change request goes

A request carries a **slice**: a side of the house (`frontend` or `backend`) and
a platform within it (`P01`…), or no platform meaning the whole side. `scope`
says who owns which slice, and putting the two together is how a request finds
the lead whose queue it is in.

The side is chosen at filing and defaults from the kind — the same `TAG_OF` map
a verdict uses, and for the same reason: a screen blocked on an endpoint is
backend work, and only the person who found it knows. `adr` and `other` have no
honest default, so those arrive **unrouted**, which the page shows as a bucket
rather than hiding.

A grant of one platform does not cover a request that names none. *Frontend,
unspecified* is wider than *Frontend · P01*, so it belongs to whoever owns the
whole side, or to nobody until somebody says.

**Seeing and acting are separate.** A team lead reads every request on the
project — a lead who cannot see what is coming cannot prepare for it. The slice
decides which they may take on, which they may settle, and which are counted
against them. A reviewer still settles anything on the project, as they always
could.

### Taking one on, and the two-day clock

`picked_by` and `picked_at` are columns, **not a status**. Picking says whose a
request is; settling says what was decided; a request sits picked and unsettled
for as long as the work takes, and that is not a contradiction. Keeping it off
`status` also leaves the spreadsheet round trip's four words exactly as they
were.

An open request nobody has taken on within `PICK_SLA_DAYS` (two) is **overdue**.
There is no notification stored and none sent: `GET /api/changes/overdue`
answers it from the rows every time it is asked. So a request picked up a minute
after it tipped over stops being overdue immediately with nothing to retract,
and a service that was down for a day misses nothing. The overdue list names the
leads who should have taken each one — or nobody, for an unrouted request, which
is itself the answer.

Handing one back does not restart the clock: the escalation measures from
`raised_at`, which does not move.

## Why invites rather than signup

Restricting signup to `@softlabsgroup.com` only checks the address a stranger
*claims*. Anyone reaching the page could register as `ceo@softlabsgroup.com`
and start signing artefacts off under that name — which defeats the point of
recording who approved what.

An invite fixes the address at the moment it is created, by someone who already
holds an account. Whoever opens the link cannot change it. So the invite is the
verification: the person who could vouch for the address is the person who
typed it. No mail server is needed — the link is handed over however you
already talk to each other.

An invite is single-use, expires in 7 days, can be revoked, and is superseded
if a second one is made for the same address. The token is stored as a SHA-256
hash, so a copy of the database cannot be used to mint accounts.

## What is stored

`ticvai.db`, SQLite, beside this file. Not inside the delivery package — that
stays as the vendor shipped it.

| table | holds |
|---|---|
| `account` | one row per person. Password hashed with argon2. One account per address, case-insensitively. |
| `invite` | one row per link. Token hashed. Carries the address it is for. |
| `session` | one row per sign-in. Token hashed, 14-day expiry. |
| `verdict` | append-only. One row per thing someone said, about one artefact, at one time. |

Verdicts are never rewritten. A row is a thing a person said at a time, and
editing it would lose the fact that they once thought otherwise. The current
verdict on an artefact is simply its newest row.

## Endpoints

| | |
|---|---|
| `GET /api/auth/me` | who the caller is; answers rather than 401s when nobody is |
| `POST /api/auth/login` | email + password → session cookie |
| `POST /api/auth/logout` | ends the session |
| `POST /api/auth/redeem` | invite token + password → account, signed in |
| `GET /api/invites/check/{token}` | who an invite is for, before a password is chosen |
| `POST /api/invites` | admin only. Makes a link for one address. |
| `GET /api/invites` | admin only. Every invite and its state. |
| `DELETE /api/invites/{id}` | admin only. Withdraws an unused invite. |
| `POST /api/validation` | records a verdict on an artefact |
| `GET /api/validation/{kind}/{id}` | current verdict and how it got there |
| `GET /api/validation` | one row per judged artefact, plus counts |
| `GET /api/export/{dataset}` | admin only. A date range as a CSV. `verdicts`, `changes`, `invites`, `accounts`. |
| `POST /api/decisions/preview` | admin only. What an edited review file would close. Writes nothing. |
| `POST /api/decisions/apply` | admin only. Closes it, on the preview's checksum. |
| `POST /api/changes/{n}/pick` | take a request on. A lead on that platform, or an admin. |
| `POST /api/changes/{n}/unpick` | hand it back. Whoever holds it, or an admin. |
| `GET /api/changes/overdue` | admin only. Open, untaken, older than two days. |
| `POST /api/changes/import/preview` | admin only. What an edited change request file would settle. Writes nothing. |
| `POST /api/changes/import/apply` | admin only. Settles it, on the preview's checksum. |

A target is `operation`, `table`, `screen` or `board`. A verdict is `approved`,
`rejected` or `needs-work`.

Two of the four exports come back. The review file is filled in down its
**our verdict** column and closes items; the change request file is filled in
down **our decision**, **because** and **reference**, and settles them. Both
take the CSV or the same sheet saved as .xlsx, both match rows on the **id**
column, and neither applies without the checksum its own preview answered with
— so a file cannot be applied that nobody read the consequences of.

A change request file may answer an open request and may complete an accepted
one. It may not reopen a settled request or overrule how one was already
answered: both throw away who settled it and when, which re-uploading the right
file afterwards cannot restore. Those rows are listed by the preview and left
alone.

## Configuration

| variable | default | |
|---|---|---|
| `TICVAI_DB` | `api/ticvai.db` | where the store lives |

| `TICVAI_DOMAIN` | `softlabsgroup.com` | the only domain that may hold an account |
| `TICVAI_SECURE_COOKIE` | unset | set to `1` when served over https |

The session cookie is `HttpOnly` and `SameSite=Lax`. It is deliberately *not*
`Secure` by default, because the viewer runs over plain http on a workstation
and the cookie would never be sent. Set `TICVAI_SECURE_COOKIE=1` the moment
this is served over https.

**`TICVAI_DB` is the one to watch.** It is read at import, so a value left set
in a shell silently sends every account and verdict somewhere else, and the
service gives no sign of it — `/api/health` will happily report five accounts
while `api/ticvai.db` has none. It has already happened once here: a test run
set it to a temp file, and the admin account made against that service went
into the temp file rather than the store. `adopt` below is what got it back.

## Housekeeping

```
python -m api.cli list                          # accounts and open invites
python -m api.cli admin you@softlabsgroup.com   # the first account, if there is none
python -m api.cli owner you@softlabsgroup.com   # make an existing account the super admin
python -m api.cli passwd you@softlabsgroup.com  # a new password, without the old one
python -m api.cli adopt you@softlabsgroup.com --source other.db --yes
python -m api.cli forget harness@softlabsgroup.com --yes
```

`passwd` asks for nothing but the new password. The web route demands the
current one, which is no use when the current one is the problem — forgotten,
or set by something other than the person it belongs to. Standing at the
machine the store is on is the proof. Every session is dropped.

`adopt` copies one account out of another store — the stored hash moves across
unchanged, so the password stays the one they chose. Sessions and verdicts are
left behind on purpose.

`forget` deletes every verdict by one account. Verdicts are append-only
otherwise, and this is the deliberate exception: it takes an **account**, not
an artefact, so it can undo a harness run against a real store and cannot be
used to tidy away an inconvenient opinion.

## Tested

`api-check.mjs` — 29 assertions, most of them attempts to get in the ways that
should not work: forged cookies, a reviewer minting invites, redeeming an
invite twice, claiming an address the invite was not for, and telling an
unknown account apart from a wrong password.

`roles-check.mjs` — 43 assertions over the role model, most of them the super
admin doing ordinary administrative things and being allowed to. That is the
hazard: every guard here was `role == "admin"` while "administers" had one
spelling, and each one left behind refuses the owner one route at a time. The
rest is the other direction — what is the owner's alone, and the three doors the
role must not be reachable through. It needs `TICVAI_DB` as well as `API`,
because making an owner is deliberately not something the API can do:

```bash
TICVAI_DB=/tmp/roles.db python -m uvicorn api.main:app --port 8799
TICVAI_DB=/tmp/roles.db API=http://localhost:8799 node api/roles-check.mjs
```

`cr-routing-check.mjs` — 42 assertions over where a request belongs and who
takes it on. Most of them are a team lead being *shown* a request they may not
touch and then refused when they touch it: a check that only tested the refusal
would pass equally against a lead who could not see it at all, which is the
wrong product. It needs `TICVAI_DB` as well as `API`, because making a request
older than it is takes the store directly — the alternative is a check that
sleeps for two days.

`changes-import-check.mjs` — 52 assertions over the change request round trip,
most of them about the half that does not write: a rejection with no reason, a
decision outside the four, an id no request has, a reopen, a stale checksum,
and the same file applied twice. It also asserts that the file the changes page
writes and the file this service writes are **the same file**, row for row —
they share their column list in `public/change-csv.js`, and either one can be
filled in and uploaded back.

It wants an empty store, so give it one of its own:

```bash
TICVAI_DB=/tmp/check.db python -m uvicorn api.main:app --port 8799
API=http://localhost:8799 node api/changes-import-check.mjs
```
