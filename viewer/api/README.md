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

A target is `operation`, `table`, `screen` or `board`. A verdict is `approved`,
`rejected` or `needs-work`.

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
python -m api.cli adopt you@softlabsgroup.com --source other.db --yes
python -m api.cli forget harness@softlabsgroup.com --yes
```

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
