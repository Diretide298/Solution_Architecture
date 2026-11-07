# Putting the viewer on a server

Ubuntu or Debian, one command.

The viewer and the delivery package are siblings in one repository, and this
script lives inside the viewer half — so the clone is the repository and the
`cd` is into `viewer`:

```
adam/
|-- viewer/     server.mjs, lib/, public/, api/, and deploy/ within it
`-- ticvai/     the delivery package -- contracts, screens, flows, states
```

```
git clone <this repo> /opt/adam && cd /opt/adam/viewer
sudo ./deploy/deploy.sh --admin you@softlabsgroup.com
```

Run it again whenever you want to deploy. It is idempotent: every step checks
before it acts.

```
cd /opt/adam && git pull && cd viewer && sudo ./deploy/deploy.sh
```

That copies **both** halves: `viewer/` into `/srv/ticvai/viewer`, and every
package registered in `projects.json` to the place its own `root` points at, so
`"root": "../ticvai"` means `/srv/ticvai/ticvai` on the server and `adam/ticvai`
in the checkout without either having to know about the other.

It did not always. The packages were separate repositories placed beside the
viewer by hand, and the script only ever *checked* they were there. Deploying
this layout with that script put a new viewer on an old package and said
nothing, because a package that is merely stale is a package that is present.

The first run pauses once to ask for a password for the admin account. It does
not take one as a flag, because a password given as an argument sits in the
shell history and in `ps` for as long as the command runs.

## Release tags: what the viewer serves

Since 1 October (council C2) ADAM serves each package at its **newest release tag** — `r1`, `r2`,
… in the repository — and not at whatever the checkout's working tree holds, so the spec stops
moving under a developer every time somebody saves a file. A release is a tag:

```
git tag -a r3 -m "r3" && git push origin r3 && git push github r3
```

The deployed viewer has no `.git`, so the deploy exports each tag from the checkout into
`/srv/ticvai/viewer/.releases/<project>/<tag>/` (`deploy/export-releases.mjs`, the same code the
viewer uses on a workstation). A tag is exported once and never rewritten; a file unchanged since
an earlier release is a hard link to it, so a release costs what changed. The mirrors under
`repos/<repo>/` are left out apart from `.github`, `terraform`, `apps` and `openapi`, and
`ticvai-docs/setup` (the starter guides SETUP tickets link; the list is `lib/export-keep.json`) — they are
generated copies of the package, 4 GB of its 4.8, and carry the same tag in their own repositories.
The rsync of the viewer excludes `.releases`, so `--delete` cannot take the exports away.

On start the viewer serves the newest exported tag and writes `served.json` beside the exports; the
deploy prints it (`ticvai is served at release r3 (…)`). While there is no tag it serves the
working-tree copy in `/srv/ticvai/ticvai`, exactly as before. `packageRef` on a project in
`projects.json` (or `ADAM_PACKAGE_REF` in the environment) overrides the choice: `latest` (the
default), `working`, or one tag such as `r2` to roll back. A new tag is a deploy: the viewer decides
at start and does not watch an export.

The accounts service reads `served.json` to record the tag a `/ticket` pull saw, and `index.json`
to date tags for the release notes. See `api/README.md`.

## What ends up running

Two processes, two ports, kept alive by PM2.

```
   :4173   node      the delivery package, and the sign-in gate in front of it
   :8787   uvicorn   accounts, invites, verdicts, mentions, and /docs
```

**A browser only ever talks to :4173.** `server.mjs` forwards everything the
accounts service owns — `/api/auth`, `/api/accounts`, `/api/invites`,
`/api/validation`, `/api/verdicts`, `/api/mentions`, `/docs` — to the other
process and hands the answer back unchanged. That is one origin, which means no
CORS to configure and one session cookie both halves can see.

:8787 is open anyway because `/docs` lives there and talking to the API
directly is useful. Nothing on any page depends on it being reachable.

### Two names instead of one

The arrangement above puts everything on one name and lets `server.mjs` forward
what the accounts service owns. To give the service its own name instead —

```
   adam.ainfinite.ai      →  :4173   the package, and the gate
   adamapi.ainfinite.ai   →  :8787   accounts, invites, verdicts, /docs
```

— the browser has to be told where to call, both halves have to agree the call
is allowed, and, the part that is easy to miss, **one cookie has to be visible
to both names**. Four variables in `/srv/ticvai/ecosystem.config.cjs`:

```
ticvai-viewer:  TICVAI_API_PUBLIC     = https://adamapi.ainfinite.ai
ticvai-api:     TICVAI_ORIGINS        = https://adam.ainfinite.ai,https://aster.ainfinite.ai
                TICVAI_COOKIE_DOMAIN  = .ainfinite.ai
                TICVAI_SECURE_COOKIE  = 1
```

Then `pm2 restart ticvai-viewer ticvai-api --update-env`.

Both blocks in `deploy/nginx/` answer to their `aster` name as well, on the same
certificate, and will until nothing has called it for a while. **Renaming a name
that has traffic on it is an alias first and a removal much later** — the record
and the certificate are the slow parts, and neither moves because a file
changed.

`TICVAI_API_PUBLIC` is written into every page as `<meta name="ticvai-api">` and
read by `validation.js`. **It is one value and not a list**, so it moves with the
DNS and not before — it is the address the browser is told to call, and an
address that can be argued out of being itself fails quietly. `API_DEPLOYED` in
`public/validation.js` is the same value for a workstation and moves in the same
commit. It is a meta tag rather than a line in the eight HTML
files because the address belongs to a deployment and those files are the same
in all of them. `TICVAI_AUTH` is a different question and stays on loopback:
that is this process asking the other one who you are, which never leaves the
box.

**`TICVAI_COOKIE_DOMAIN` is not optional here.** The gate in `lib/session.mjs`
reads the session cookie off requests to :4173 to decide who is asking. A
cookie set by `adamapi` without a domain goes back to `adamapi` and nowhere
else, so :4173 would see no cookie, call everybody a stranger, and redirect
every page to the sign-in door — which then signs you in successfully and
bounces you straight back. Scope it to the shared parent and no higher; a
domain cookie is sent to every host underneath it.

`samesite=lax` is right either way. Sibling subdomains are the same *site*, and
cross-site is what lax stops.

The proxy in `server.mjs` stays in place and simply goes unused by the browser.
Nothing has to be removed, and unsetting `TICVAI_API_PUBLIC` puts the one-origin
arrangement back.

Both names need a certificate — see below — and `adamapi` puts `/docs` on the
public internet, so put a basic-auth or an IP rule in front of it if that is not
wanted.

### nginx: what it does here, and what the deploy will not do to it

There was a period with no nginx at all, and the reasoning was sound while it
lasted: it was doing exactly one job — putting both halves on one origin — and
the node process already does that in the code it had for asking the accounts
service who you are. A reverse proxy earns its place with TLS termination,
caching, or load across several backends.

TLS is now the case that earns it. There are two names with Let's Encrypt
certificates on them, and nginx terminates both and decides which process
answers:

```
   adam.ainfinite.ai  ──▶ :4173   everything, no path split at all
   adamapi.ainfinite.ai ─▶ :8787  everything except /pkg/ and the package
                                  routes, which go to :4173
```

The blocks live in `deploy/nginx/`, one file per name, and **`deploy.sh` never
installs, edits or reloads them.** A deploy that can take a certificate down is
a worse trade than a deploy that leaves it alone. What the script does instead
is *read* the API block and refuse to finish if the routes named there disagree
with the routes `server.mjs` actually owns — that list is kept in two files, and
it drifted once: `summary` and `diagrams` were added to the reading server and
not to nginx, so they fell through to the accounts service and 404ed for weeks,
and the landing page drew zeroes rather than an error, because a count that
failed to load and a count of nothing look the same.

So installing a block is by hand, and the install lines are in the header
comment of each file.

### Why PM2 and not systemd units

They do the same job here: start both, restart on crash, come back after a
reboot, keep the logs. PM2 does it with one file and one command, and the file
is generated by the deploy script rather than being four unit files that have
to agree with it. `pm2 startup` still installs a systemd hook underneath, so a
reboot works the same way.

```
pm2 status                     what is running
pm2 logs ticvai-viewer         follow one of them
pm2 restart ticvai-viewer      after a package drop
```

A package drop needs a **deploy**, not a restart: the package is a separate
tree on the server and `git pull` in the checkout does not move it. The deploy
copies it and restarts the viewer, which reads the package at boot and watches
for changes — but a drop moves too many files at once to rely on the watcher.

## Your data survives a redeploy

This is guaranteed in three places, not one, because losing a reviewer's work
to a deploy is the kind of mistake that is only noticed later:

1. **`.gitignore` and `.git/info/exclude`** — `viewer/api/*.db` is never
   committed, so it cannot travel in a `git pull`. The second copy is because a
   package drop overwrites `.gitignore` at the repository root and on 18 August
   silently took the rule with it.
2. **The copy step excludes it** — `api/ticvai.db` and its `-shm`/`-wal`
   companions are named exclusions on the viewer sync, so it cannot overwrite
   the live file with whatever was in a working tree. The package sync cannot
   reach it at all: it writes a sibling tree, and a `root` that resolved to the
   viewer directory or above is refused rather than copied, because that sync
   runs with `--delete` and `"root": "."` is all it would take.
3. **The script checks before creating** — an existing database is left alone
   and the script says so.

Accounts, invites, verdicts, mentions and live sessions all persist. People
stay signed in across a restart.

**Backups** run nightly at 03:17 via `/etc/cron.d/ticvai-backup`, keeping the
last 14 in `/srv/ticvai/backups/`. It uses `sqlite3 .backup` rather than `cp`,
because a plain copy of a live database produces a file that opens and is wrong
— worse than one that fails to open. The package can be regenerated from a
dump; a verdict cannot be regenerated from anything.

```
ticvai-backup                  # take one now
ls -l /srv/ticvai/backups/
```

## The change-request watcher

ADAM on the phone (`viewer/PHONE-SPEC.md`). The watcher that drafted answers to
developers' change requests on the lead's laptop runs here instead, as the PM2
job `ticvai-cr-watch`: hourly, as `ticvai`, from its own clone. It drafts and
lists; it never settles (the job runs `run` without `--auto`). The lead decides
and settles from the decide page, which reads the watcher's folder through the
accounts service (`api/watcher.py`).

```
/var/lib/ticvai/cr-watch-mirror.git   refreshed from this checkout by every deploy;
                                      root's, read-only to ticvai
/srv/ticvai/cr-watch/
|-- repo/         the watcher's clone of the mirror, at what was deployed
|-- release/      its worktree at the newest release tag (made by the watcher)
`-- out/          state.json, drafts/, REVIEW.md, runs.log, spend.jsonl
/etc/ticvai/cr-watch.env   its credentials: 0600, owned by ticvai, never in git
```

Every deploy refreshes the mirror and the clone. The mirror is root's and sits
outside `/srv/ticvai` (which the deploy hands to `ticvai`): root runs git in it,
so `ticvai` must not be able to write a hook or a config line there. Root's git
also runs with hooks, the file-system monitor and automatic gc off. A mirror an
earlier deploy left under `/srv/ticvai/cr-watch/` is removed, and one with
anything in it that is not root's is made again. `ticvai`'s own git config names
the mirror as safe to read. If git refuses to read this checkout as root (it
belongs to whoever pulled it), the deploy stops with git's words rather than
skipping the watcher. The job starts only when the env file, Claude Code and a
seeded `out/` are all there. Until then the deploy
says which one is missing and the decide page answers "The watcher is not set up
on this server."

### Once, by the lead

1. **Deploy once**, so `/srv/ticvai/cr-watch/` exists.
2. **Install Claude Code** for every account, then check `ticvai` can run it:

   ```
   sudo npm install -g @anthropic-ai/claude-code
   sudo -u ticvai -H claude --version
   ```

   It signs in with the API key from the env file. Nothing logs in interactively.
3. **Write the env file** in an editor. Do not `echo` the values: they would
   stay in the shell history.

   ```
   sudo install -m 600 -o ticvai -g ticvai /dev/null /etc/ticvai/cr-watch.env
   sudo nano /etc/ticvai/cr-watch.env
   sudo chown ticvai:ticvai /etc/ticvai/cr-watch.env && sudo chmod 600 /etc/ticvai/cr-watch.env
   sudo -u ticvai test -r /etc/ticvai/cr-watch.env && echo "ticvai can read it"
   ```

   As root: ticvai cannot write in `/etc/ticvai`, so its own editor cannot save
   there ("Error writing ... Permission denied", the first server deploy).

   ```
   ANTHROPIC_API_KEY=...        # the key the drafting and ask-back turns spend
   ADAM_EMAIL=...               # the ADAM account that reads the requests and settles them
   ADAM_PASSWORD=...
   TICVAI_OP_TOKEN=...          # that person's OpenProject API token, for the ticket comments
   # optional
   CR_WATCH_DAILY_USD=50        # the day's cap: at it drafting stops, and the summary says so
   CR_WATCH_ASK_USD=2           # one question from the phone
   ```

   Each Claude turn is started with an allowlisted environment: PATH, HOME, the
   locale, the temporary folder, `ANTHROPIC_API_KEY` and `CLAUDE_*`, nothing
   else. It loads no settings file and can read nothing outside the release
   worktree (`/etc/ticvai` and the out folder are denied by name). The deploy
   fixes the file's owner and mode if they are wrong, refuses the file if it is
   a symbolic link or a hard link (the watcher is then not started), checks that
   the four names are set, and never prints a value. To change a value, edit the
   file. Each run, settle and question reads it afresh, so nothing restarts.
4. **Stop the laptop's schedule** first. Two watchers would draft every request
   twice and both write REVIEW.md. Then **seed** the server's folder, in one of
   two ways:

   - carry the laptop's list over. On the server first, a folder only you can
     read (not `/tmp`, which every account on the box can list and read):

     ```
     install -d -m 700 ~/cr-watch-seed
     ```

     From the checkout on the laptop:

     ```
     scp -r audit/ticvai/cr-watch/state.json audit/ticvai/cr-watch/REVIEW.md \
       audit/ticvai/cr-watch/drafts <server>:cr-watch-seed/
     ```

     then on the server:

     ```
     sudo cp -r ~/cr-watch-seed/. /srv/ticvai/cr-watch/out/
     sudo chown -R ticvai:ticvai /srv/ticvai/cr-watch/out
     rm -r ~/cr-watch-seed
     ```

   - or start fresh after every request ADAM has now:

     ```
     sudo -u ticvai -H /srv/ticvai/.venv/bin/python \
       /srv/ticvai/cr-watch/repo/ticvai/tools/cr-watch.py run --seed \
       --env-file /etc/ticvai/cr-watch.env --out /srv/ticvai/cr-watch/out \
       --release-dir /srv/ticvai/cr-watch/release
     ```
5. **Deploy again.** The deploy now says "the watcher job runs hourly". Check it:

   ```
   sudo -u ticvai -H pm2 status                      # ticvai-cr-watch is listed
   sudo -u ticvai -H pm2 restart ticvai-cr-watch     # run it now rather than at :07
   sudo -u ticvai -H pm2 logs ticvai-cr-watch --lines 30
   ```

   Then open the decide page signed in as the System Architect. Only the System
   Architect can read or decide there; a Team Lead, like everybody else, is
   refused (403) and is not shown the page.

   A request whose drafting failed twice waits for Draft again on the page, or,
   from a shell, as the watcher's account:

   ```
   sudo -u ticvai -H /srv/ticvai/.venv/bin/python /srv/ticvai/cr-watch/repo/ticvai/tools/cr-watch.py \
     redraft --all-failed --out /srv/ticvai/cr-watch/out
   ```

   Neither starts a Claude turn: the next hourly run drafts them.

To stop the watcher, move the env file away and deploy. The job is removed, and
the list in `out/` stays as it was. The decide page then says "The watcher is not
running on this server", with no error and no stale pause; Draft again and Ask
are off, and History still lists what was settled from it.

## Inviting a client

A client is somebody outside the company: they read everything except the
decisions, and they can sign off on what they read — into their own review,
kept apart from the team's.

```
sudo -u ticvai env TICVAI_DB=/srv/ticvai/viewer/api/ticvai.db \
  PYTHONPATH=/srv/ticvai/viewer /srv/ticvai/.venv/bin/python \
  -m api.cli invite them@theircompany.com --role client --base http://<server>:4173
```

The `@softlabsgroup.com` rule still applies to `admin` and `reviewer`. It is
lifted for `client` alone, because a client is by definition somewhere else —
and what replaces it is the invite. The address is fixed by the admin who types
it and cannot be changed by whoever opens the link, so the person who could
vouch for the address is the person who typed it. Client links expire in three
days rather than seven.

**What a client sees:** everything — Frontend, Contracts, Domain and Backend,
every mode of each, the audit included. **What they do not:** the Decisions
layer. The ADRs, the registers and the conflict log record the options that
were rejected, what they would have cost and what has since been superseded,
and a reader who takes a rejected option for a current one is reading something
that was never meant to be a statement.

Not hidden in the browser. `/api/decisions` answers 403, and so does `/api/file`
for anything the Decisions layer serves — which is the one that matters,
because an ADR is a `.md` file and blocking only the endpoint would leave every
decision readable one path at a time.

**Their review is their own.** A client can record a verdict on anything they
can see, and it is filed under its own audience — taken from the role on their
session, never from the request, so it cannot be sent in as the team's. The
sign-off summary answers with the team's review unless asked for
`?audience=client`, which means a client approving something the team rejected
changes nothing about where the team stands. Closing an item stays the team's:
it is a record of the team's own queue.

Prove it rather than believe it:

```
node viewer/checks/client-check.mjs
```

It creates a client, asks the server the questions a curious reader would ask
from devtools, and removes the account afterwards.

## This address has no certificate

Deliberately, for now. It means the password and the session cookie cross the
network in clear text and anyone on the path can read both. Treat every account
on it as public knowledge until that changes.

When there is a name to put a certificate on, put nginx in front of :4173:

```
sudo apt install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d viewer.example.com
```

Then set `TICVAI_SECURE_COOKIE=1` in the `ticvai-api` block of
`/srv/ticvai/ecosystem.config.cjs` and `pm2 restart ticvai-api --update-env`.
Nothing else changes — that is what one origin buys.

## Turning the gate off

`TICVAI_NO_GATE=1` serves the whole package to anyone who asks. It exists for a
workstation and must never be set here. The deploy script proves the gate holds
before it finishes — it asserts that `/api/index` answers 401 to a stranger — so
a stray value fails the deploy rather than quietly publishing the package.
