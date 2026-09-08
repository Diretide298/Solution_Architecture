# Deploying the ADAM bridge

**Every command, in order.** Hand this to whoever has root on the box.

Target commit: **`a387a7a`** — on both remotes (`github` and `origin`) as of 8 September 2026.

| | |
|---|---|
| Server | the one already running `adam.ainfinite.ai` / `adamapi.ainfinite.ai` |
| App directory | `/srv/ticvai` |
| Service account | `ticvai` |
| Ports | `4173` viewer (node), `8787` accounts (uvicorn) |
| Process manager | pm2 |
| Downtime | a few seconds, while pm2 restarts both |

This is a **routine redeploy of an existing install**. Section 7 covers a first-time box.

---

## 0. What is new in this deploy

Three commits since `cfa4f90`. Two things need an operator's attention; everything else
is ordinary.

1. **A credential-encryption key is generated on this deploy** — `/etc/ticvai/secret.key`.
   It is created once and never overwritten. **It must be backed up** (§3). Losing it makes
   every stored OpenProject token unreadable.
2. **`cryptography` is added to the Python venv.** If it fails to install, uvicorn will not
   start at all. The script asserts it and stops rather than restarting into a broken service.

Also: two new tables and one new column, migrated automatically at startup; a settings page
at `/settings.html`; an MCP server under `viewer/mcp/` that developers run on their own
machines, not on this box.

**No nginx change is required.** Verified against the running config — the `location /pkg/`
rule at line 48 of `deploy/nginx/adamapi.ainfinite.ai` already covers every package route.

---

## 1. Before you start

```bash
# who you are and where you are
whoami                                   # need sudo from here
hostname
```

```bash
# find the source checkout — it is the directory containing viewer/ and ticvai/
ls -d /srv/ticvai /opt/adam ~/adam ~/ticvai_architecture 2>/dev/null
```

If none of those exist, find it:

```bash
find / -maxdepth 5 -type d -name viewer -path '*adam*' 2>/dev/null
find / -maxdepth 5 -name deploy.sh -path '*viewer/deploy*' 2>/dev/null
```

> `/srv/ticvai` is where the app **runs**. The **source checkout** is a separate
> directory that you `git pull` in and run `deploy.sh` from. They are not the same
> place. `deploy.sh` copies from the checkout into `/srv/ticvai`.

Set it once so the rest of this document copy-pastes:

```bash
export SRC=/path/to/the/checkout        # the directory that contains viewer/ and ticvai/
ls "$SRC"                               # expect: viewer  ticvai  .gitignore  ...
```

### Take a database snapshot first

```bash
sudo -u ticvai /usr/local/bin/ticvai-backup
ls -lt /srv/ticvai/backups/ | head -3
```

Expect a fresh `ticvai-YYYYMMDD-HHMMSS.db`. This holds real accounts, e-mail addresses,
password hashes and every recorded verdict. **Do not copy it off the server.**

---

## 2. Get the code

```bash
cd "$SRC"
git status --porcelain | head          # expect no output; stop and ask if there is any
git pull
git log -1 --oneline
```

Expect exactly:

```
a387a7a The September board work, and five decisions the two databases forced
```

If you get a different hash, you are on a remote that has not received the push, or on a
different branch. Check with `git branch -vv` and `git remote -v` before going further.

```bash
# confirm all three commits arrived
git log --oneline -4
```

```
a387a7a The September board work, and five decisions the two databases forced
80ccf7d The ADAM bridge: a developer's Claude reads the package and the board
4cf5098 Flatten the page ground so it stops arguing with the scene
cfa4f90 Build the two databases ADR-0038 and ADR-0039 decided
```

---

## 3. Run the deploy

```bash
cd "$SRC/viewer"
sudo ./deploy/deploy.sh
```

That is the whole command. It is idempotent — running it twice is how you deploy, not
something to be careful about. It takes two to four minutes, most of it `apt-get` and `npm`.

### What you will see, and what each section means

| section | what it does | what "wrong" looks like |
|---|---|---|
| `==> Packages` | apt, Node 22 check, pm2 | a Node older than 22 gets replaced |
| `==> Service account` | `ticvai` user | already exists — normal |
| `==> Application` | rsync into `/srv/ticvai/viewer`, `npm install` | the live database is **excluded** from the copy |
| `==> the packages` | rsync `ticvai/` into place | dies naming a path if a registered package is missing |
| `==> Python environment` | venv + pip, then **asserts** `cryptography` | **new this deploy** — see below |
| `==> Database` | migrations run at service startup | nothing to do by hand |
| `==> Credential key` | **generates `/etc/ticvai/secret.key`** | **new this deploy** — back it up |
| `==> Processes` | writes `ecosystem.config.cjs` (0600), restarts pm2 | |
| `==> Backups` | nightly `sqlite3 .backup` at 03:17 | |
| `==> Checking` | six assertions | any failure stops with a sentence saying which |
| `==> Done` | the summary | |

### The one line you must not scroll past

```
    generated /etc/ticvai/secret.key — back it up; losing it makes every stored
    credential unreadable
```

**Back it up now, before anyone stores a token.**

```bash
sudo cat /etc/ticvai/secret.key
```

Copy that value into the team password manager as `TICVAI_SECRET_KEY (adam production)`.
It is one line, 44 characters.

```bash
# confirm the permissions are right
sudo ls -l /etc/ticvai/secret.key                    # expect -rw------- root root
sudo ls -l /srv/ticvai/ecosystem.config.cjs          # expect -rw------- (it carries the key)
```

If you see `-rw-r--r--` on either, stop and fix it:

```bash
sudo chmod 600 /etc/ticvai/secret.key /srv/ticvai/ecosystem.config.cjs
```

> **Why the key is not in the database.** It encrypts the OpenProject tokens that are
> stored *in* that database. Put the key in the same file and a copy of the database is a
> copy of every developer's live PMS credential. Outside it, a leaked database is
> ciphertext and nothing else. This is the whole reason the encryption is worth anything.

If the deploy stops at `the venv is missing openpyxl, python-multipart or cryptography`:

```bash
sudo /srv/ticvai/.venv/bin/pip install cryptography
sudo ./deploy/deploy.sh        # then run it again
```

---

## 4. Verify

The deploy runs six assertions itself and stops on any failure, so reaching `==> Done`
already means a lot. These confirm the new parts specifically.

> **pm2 runs as the `ticvai` user, not as root.** A bare `pm2 status` as root talks to
> root's own empty pm2 daemon and shows nothing, which reads exactly like "both services are
> gone". Every pm2 command must be run as `ticvai`. Set this up once per shell:
>
> ```bash
> pm2() { sudo -u ticvai HOME=/home/ticvai $(command -v pm2) "$@"; }
> ```
>
> Then `pm2 status` works as written below. Without the function, spell it out in full:
> `sudo -u ticvai HOME=/home/ticvai pm2 status`.

```bash
# both processes up
pm2 status
```

Expect `ticvai-viewer` and `ticvai-api`, both `online`, restart counts not climbing.

```bash
# the accounts service answers
curl -sf http://127.0.0.1:8787/api/health && echo OK
```

```bash
# the gate still holds — a stranger gets 401, not data
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:4173/api/index
```

Expect `401`. Anything else means the package is being served to the public.

```bash
# the new tables exist
sudo -u ticvai sqlite3 /srv/ticvai/viewer/api/ticvai.db \
  "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('artefact_link','account_secret');"
```

Expect both names. If either is missing the migration did not run — check `pm2 logs ticvai-api`.

```bash
# the new column exists
sudo -u ticvai sqlite3 /srv/ticvai/viewer/api/ticvai.db \
  "SELECT COUNT(*) FROM pragma_table_info('account') WHERE name='git_email';"
```

Expect `1`.

```bash
# the service can encrypt — this is the key actually being read by the process
curl -s http://127.0.0.1:8787/api/settings/me | head -c 200; echo
```

Expect `{"detail":"Sign in to do that."}` — a 401 body. That is correct: it proves the route
exists. A `404` means the code did not deploy; a `500` means something is wrong with the key.

Then in a browser, signed in as yourself:

```
https://adam.ainfinite.ai/settings.html
```

The OpenProject panel should say it *can* store credentials. If it says it cannot and names
`TICVAI_SECRET_KEY`, the process is running without the key — `pm2 restart ticvai-api --update-env`.

> **Do not run the `*-check.mjs` harnesses against this server.** They sign in as
> `harness.admin@softlabsgroup.com` with a password that is written in the repository.
> That account is for a workstation and **must never exist on the live box**.

---

## 5. If it goes wrong

The migrations are additive — new tables and one new column. Older code ignores them, so
rolling the code back is safe and needs no database work.

```bash
cd "$SRC"
git log --oneline -5                    # find the commit you came from
git checkout cfa4f90                    # the commit before this deploy
cd viewer && sudo ./deploy/deploy.sh
```

To get back:

```bash
cd "$SRC" && git checkout main && cd viewer && sudo ./deploy/deploy.sh
```

**Leave `/etc/ticvai/secret.key` alone during a rollback.** Deleting it does not undo
anything; it strands every credential stored since the deploy.

Logs:

```bash
sudo -u ticvai HOME=/home/ticvai pm2 logs ticvai-api --lines 100
sudo -u ticvai HOME=/home/ticvai pm2 logs ticvai-viewer --lines 100
```

(As root without `sudo -u ticvai`, pm2 reports no processes at all — see §4.)

| symptom | cause | fix |
|---|---|---|
| `ticvai-api` restart-looping | `cryptography` missing from the venv | `sudo /srv/ticvai/.venv/bin/pip install cryptography` then redeploy |
| settings page says credentials cannot be stored | process has no `TICVAI_SECRET_KEY` | `pm2 restart ticvai-api --update-env` |
| sign-in returns to the sign-in page | cookie `Domain` wrong | the deploy asserts this — read what it printed |
| `/api/settings/me` is 404 | code did not copy | check `git log -1` in `$SRC`, redeploy |
| a package route 404s on `adamapi` | old `/api/*` spelling; `cicd` is not in the per-name list | use `adam.ainfinite.ai`, or add `cicd` to the regex in `deploy/nginx/adamapi.ainfinite.ai` |

---

## 6. After the deploy — what each developer does

Two steps, both self-service. Nothing further is needed on the server.

**One.** Create an OpenProject API token: `https://pms.softlabsgroup.in` → My account →
Access tokens → API. It is shown once.

**Two.** Paste it at `https://adam.ainfinite.ai/settings.html`. It is checked against
OpenProject before it is stored, and encrypted at rest. Only the last four characters ever
come back.

Then, to connect their local Claude:

```bash
claude mcp add adam -- node /path/to/adam/viewer/mcp/server.mjs \
  -e ADAM_VIEWER_URL=https://adam.ainfinite.ai \
  -e ADAM_EMAIL=you@softlabsgroup.com \
  -e ADAM_PASSWORD=...
```

They need a checkout of this repository for `server.mjs`; everything it reads comes over
HTTPS from the deployed viewer. Thirteen tools — see `viewer/mcp/README.md`.

**Each developer uses their own account.** The bridge sees exactly what that person can see
in the viewer, and every OpenProject call is made as them. There is no service account, by
decision: a shared login hands every reader the widest role in the building, and attributes
every change to a robot.

---

## 7. First time on a fresh box only

Skip this entirely on the existing server.

```bash
sudo ./deploy/deploy.sh --admin you@softlabsgroup.com
```

It will prompt for that account's password. Then place the two nginx server blocks by hand —
the deploy deliberately does not touch nginx, because a deploy that can take the certificates
down is a worse trade than one that leaves them alone:

```bash
sudo cp deploy/nginx/adam.ainfinite.ai    /etc/nginx/sites-available/
sudo cp deploy/nginx/adamapi.ainfinite.ai /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/adam.ainfinite.ai    /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/adamapi.ainfinite.ai /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Certificates are Certbot's, on `aster.ainfinite.ai`, and both names are on them.

Surviving a reboot needs no step here — `deploy.sh` runs `pm2 save` and installs the systemd
boot hook itself, as the `ticvai` user. If it could not, it says so in a `note` rather than
failing.

---

## Everyday commands

All of these run as `ticvai`, for the reason in §4:

```bash
sudo -u ticvai HOME=/home/ticvai pm2 status                     # what is running
sudo -u ticvai HOME=/home/ticvai pm2 logs ticvai-viewer         # follow one
sudo -u ticvai HOME=/home/ticvai pm2 restart ticvai-viewer      # after a package drop
sudo -u ticvai HOME=/home/ticvai pm2 restart ticvai-api --update-env   # after an env change
sudo -u ticvai /usr/local/bin/ticvai-backup                     # snapshot now
```

---

## One open item

The OpenProject token generated during development (`00c7…babe`, shown in a chat transcript)
**should be revoked** at `https://pms.softlabsgroup.in` → My account → Access tokens. It works
today. Tracked as V-50 in `viewer/TODO.md`.
