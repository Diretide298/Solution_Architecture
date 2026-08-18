# Putting the viewer on a server

Ubuntu or Debian, one command:

```
git clone <this repo> /opt/ticvai-src && cd /opt/ticvai-src
sudo ./deploy/setup.sh --admin you@softlabsgroup.com
```

Run it again whenever you want to deploy. It is idempotent: every step checks
before it acts.

```
git pull && sudo ./deploy/setup.sh
```

## What ends up running

```
   the internet
        │
        ▼
   nginx  :80                    the only port reachable from outside
        ├─ /api/auth · accounts · invites · validation · verdicts · /docs
        │        └──►  127.0.0.1:8787   uvicorn   accounts and verdicts
        └─ everything else
                 └──►  127.0.0.1:4173   node      the delivery package
```

Both application processes bind the loopback address, so 4173 and 8787 do not
exist from outside the machine. One address means one origin: no CORS to
configure, and one session cookie both halves can see.

## Your data survives a redeploy

This is guaranteed in three places, not one, because losing a reviewer's work
to a deploy is the kind of mistake that is only noticed later:

1. **`.gitignore` and `.git/info/exclude`** — `viewer/api/*.db` is never
   committed, so it cannot travel in a `git pull`. The second copy is because a
   package drop overwrites `.gitignore` at the repository root and on 18 August
   silently took the rule with it.
2. **`setup.sh` excludes it from the sync** — `--exclude 'viewer/api/ticvai.db*'`,
   so the copy step cannot overwrite the live file with whatever was in a
   working tree.
3. **`setup.sh` checks before creating** — an existing database is left alone
   and the script says so.

Accounts, invites, verdicts and live sessions all persist. People stay signed
in across a restart.

**Backups** run daily via `ticvai-backup.timer`, keeping the last 14 in
`/srv/ticvai/backups/`. It uses `sqlite3 .backup` rather than `cp`, because a
plain copy of a live database produces a file that opens and is wrong — worse
than one that fails to open. The package can be regenerated from a dump; a
verdict cannot be regenerated from anything.

```
sudo systemctl start ticvai-backup.service     # take one now
ls -l /srv/ticvai/backups/
```

## Inviting a client

A guest is an outside client: they read a restricted view and record nothing.

```
sudo -u ticvai env TICVAI_DB=/srv/ticvai/viewer/api/ticvai.db \
  PYTHONPATH=/srv/ticvai/viewer /srv/ticvai/.venv/bin/python \
  -m api.cli invite them@theircompany.com --role guest --base http://<server>
```

The `@softlabsgroup.com` rule still applies to `admin` and `reviewer`. It is
lifted for `guest` alone, because a client is by definition somewhere else —
and what replaces it is the invite. The address is fixed by the admin who
types it and cannot be changed by whoever opens the link, so the person who
could vouch for the address is the person who typed it. Guest links expire in
three days rather than seven.

**What a guest sees:** Frontend (Screen, Journey, Apps, Waves) and Contracts
(Reader, Structure). **What they do not:** Decisions, Backend, Lineage, every
Audit view, and the verdict history. Not hidden in the browser — a guest's
`/api/index` does not contain the audit at all, and `/api/decisions`,
`/api/backend`, `/api/file` and `/api/tree` answer 403 to them.

Prove it rather than believe it:

```
node viewer/checks/guest-check.mjs
```

26 checks. It creates a guest, asks the server the questions a curious client
would ask from devtools, and removes the account afterwards.

## This address has no certificate

Deliberately, for now. It means the password and the session cookie cross the
internet in clear text and anyone on the path can read both. Treat every
account on it as public knowledge until that changes.

When there is a name to put a certificate on:

```
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d viewer.example.com
```

Then set `TICVAI_SECURE_COOKIE=1` in `/etc/systemd/system/ticvai-api.service`
and `systemctl restart ticvai-api`. Nothing else changes — that is what one
origin buys.

## Day to day

```
journalctl -u ticvai-viewer -u ticvai-api -f      # logs
systemctl restart ticvai-viewer                    # after a package drop
systemctl status ticvai-backup.timer               # when the last snapshot ran
```

A package drop into the repository needs `git pull` then a restart of
`ticvai-viewer` — it reads the package at boot and watches for changes, but a
`git pull` moves too many files at once to rely on the watcher.

## Turning the gate off

`TICVAI_NO_GATE=1` serves the whole package to anyone who asks. It exists for a
workstation and must never be set here. `setup.sh` proves the gate holds before
it finishes, so a stray value fails the deploy rather than quietly publishing
the package.
