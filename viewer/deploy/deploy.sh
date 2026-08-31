#!/usr/bin/env bash
#
# The whole deployment, in one command.
#
#   sudo ./deploy/deploy.sh --admin you@softlabsgroup.com     # first time
#   git pull && sudo ./deploy/deploy.sh                       # every time after
#
# Two services on two ports, kept alive by PM2.
#
#   :4173  node      the delivery package, and the sign-in gate in front of it
#   :8787  uvicorn   accounts, invites, verdicts, mentions, and /docs
#
# In front of them, nginx terminates TLS for two names and decides which process
# each request belongs to. This script does not install or reload it — the two
# server blocks are kept in deploy/nginx/ and put in place by hand, because a
# deploy that can take the certificates down is a worse trade than a deploy that
# leaves them alone.
#
#   aster.ainfinite.ai      -> :4173, all of it
#   asterapi.ainfinite.ai   -> :8787, except the thirteen package routes the
#                              node process owns, which go to :4173
#
# Two names means one site rather than two only if the session cookie is scoped
# to the parent both sit under, which is what COOKIE_DOMAIN below is for, and
# which the checks at the end assert rather than assume.
#
# PM2 does the job systemd units were doing: start both, restart on crash,
# come back after a reboot, keep the logs. One tool, one command to look at
# them, and nothing that needs `daemon-reload`.
#
# Idempotent. Every step checks before it acts, so running it again is how you
# deploy rather than something to be careful about.

set -euo pipefail

APP_USER="${APP_USER:-ticvai}"
APP_DIR="${APP_DIR:-/srv/ticvai}"
VIEWER_PORT="${VIEWER_PORT:-4173}"
API_PORT="${API_PORT:-8787}"
ADMIN_EMAIL=""

# ── the deployed names ───────────────────────────────────────────────
#
# Three settings that only matter once this is on real names behind TLS, and
# that all three have to agree with each other. They live here rather than being
# typed into ecosystem.config.cjs because this script *generates* that file: a
# value added there by hand survives until the next deploy and then vanishes,
# which is a bug that arrives days later wearing the costume of something else.
#
# PUBLIC_ORIGIN   where a browser loads the front end. The accounts service must
#                 name it to allow a credentialed cross-origin call, and it can
#                 never be "*" — a browser refuses "*" alongside credentials.
#
# COOKIE_DOMAIN   the parent both names sit under, with the leading dot. This is
#                 what lets one session cookie be seen by the front end and the
#                 API alike. Without it the cookie is host-only to whichever
#                 name issued it, the reading server's gate never sees one, and
#                 signing in bounces straight back to the sign-in door in a loop
#                 that looks, from the outside, like the page refreshing itself.
#                 Set it to the shared parent and no higher: a domain cookie is
#                 sent to every host beneath it.
#
# SECURE_COOKIE   1 once there is a certificate. Set it before there is one and
#                 the cookie is never sent at all.
#
# The defaults are this deployment, because this script only ever runs on it and
# a default that is wrong for the only caller is not a default, it is a trap.
# Another one overrides them from the environment, and empty is the no-op in all
# three cases — no extra origin, a host-only cookie, and no Secure:
#
#   PUBLIC_ORIGIN=https://viewer.example.com COOKIE_DOMAIN=.example.com \
#     sudo -E ./deploy/deploy.sh
#
# sudo -E, or sudo drops them and you silently get the defaults below.
PUBLIC_ORIGIN="${PUBLIC_ORIGIN-https://aster.ainfinite.ai}"
COOKIE_DOMAIN="${COOKIE_DOMAIN-.ainfinite.ai}"
SECURE_COOKIE="${SECURE_COOKIE-1}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --admin) ADMIN_EMAIL="${2:-}"; shift 2 ;;
    --dir) APP_DIR="${2:-}"; shift 2 ;;
    --port) VIEWER_PORT="${2:-}"; shift 2 ;;
    --api-port) API_PORT="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done

[[ $EUID -eq 0 ]] || { echo "Run this with sudo." >&2; exit 1; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# The viewer repository. This script lives in deploy/ at its root, so one level
# up is the whole of it \u2014 server.mjs, lib/, public/, api/. It used to be the
# tree that *contained* the viewer; the packages are separate repositories now
# and are placed beside it rather than copied with it.
REPO="$(cd "$HERE/.." && pwd)"

say()  { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
note() { printf '    %s\n' "$*"; }
die()  { printf '\n\033[31m!! %s\033[0m\n' "$*" >&2; exit 1; }

# ── packages ────────────────────────────────────────────────────────────────
say "Packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
# sqlite3 is for the nightly snapshot, which uses `.backup` rather than cp —
# a plain copy of a live database opens and is wrong, which is worse than a
# file that fails to open.
apt-get install -y -qq python3 python3-venv python3-pip curl ca-certificates rsync sqlite3

# Node 22 or newer: the viewer uses node:sqlite and getSetCookie(), and neither
# exists on the 18 that Debian ships.
if ! command -v node >/dev/null || [[ "$(node -v | sed 's/v\([0-9]*\).*/\1/')" -lt 22 ]]; then
  note "installing Node 22"
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash - >/dev/null
  apt-get install -y -qq nodejs
fi
note "node $(node -v)"

if ! command -v pm2 >/dev/null; then
  note "installing pm2"
  npm install -g pm2 >/dev/null 2>&1
fi
note "pm2 $(pm2 -v)"

# ── the account the services run as ─────────────────────────────────────────
say "Service account"
if id "$APP_USER" >/dev/null 2>&1; then
  note "$APP_USER exists"
else
  useradd --system --create-home --home-dir "/home/$APP_USER" --shell /usr/sbin/nologin "$APP_USER"
  note "created $APP_USER"
fi

# ── the application ─────────────────────────────────────────────────────────
say "Application at $APP_DIR"
mkdir -p "$APP_DIR"

# The database is excluded from the copy, not merely gitignored. This is the
# step that would otherwise overwrite live accounts and verdicts with whatever
# happened to be in a working tree, and it is the one mistake here that cannot
# be undone.
# Into $APP_DIR/viewer, not $APP_DIR. The deployed layout is the working one:
#
#   /srv/ticvai/
#   \u251c\u2500\u2500 viewer/     this repository
#   \u251c\u2500\u2500 ticvai/     a package repository, checked out beside it
#   \u2514\u2500\u2500 .venv/ ecosystem.config.cjs backups/
#
# so `"root": "../ticvai"` in projects.json means the same thing in both places.
# --delete is scoped to viewer/ for the same reason: the packages beside it are
# not this repository's to remove.
mkdir -p "$APP_DIR/viewer"
rsync -a --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude 'api/ticvai.db' \
  --exclude 'api/ticvai.db-shm' \
  --exclude 'api/ticvai.db-wal' \
  --exclude '.versions' \
  "$REPO/" "$APP_DIR/viewer/"

( cd "$APP_DIR/viewer" && npm install --omit=dev --silent >/dev/null 2>&1 || true )
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

# ── the packages, when they travel with the viewer ──────────────────────────
#
# They used to be separate checkouts placed beside this one by hand, and the
# section below still only *checks* that they are there, because that was the
# whole arrangement. In this tree they are siblings inside one repository:
#
#   adam/
#   ├── viewer/     this, with deploy/deploy.sh inside it
#   └── ticvai/     the delivery package
#
# which is the same shape as the deployed layout, so each registered package is
# copied to the place its own `root` in projects.json already points at and
# `"root": "../ticvai"` goes on meaning one thing in both.
#
# Only roots that are relative and present beside the source checkout are
# copied. An absolute root, or one that is not here, is the old by-hand case and
# is left alone — the check below is what catches those going missing.
#
# --delete is scoped to one package at a time, for the reason the viewer's is
# scoped to viewer/: a drop has to be able to remove a file as well as add one,
# or a board deleted in the repo stays on the server for good.
if [[ -f "$REPO/projects.json" ]]; then
  # Assigned, not piped. `python3 … | while read` puts the failure in a
  # subshell and hands the loop an empty list, so a broken enumeration reads
  # exactly like a registry with nothing in it and the deploy copies no
  # packages, quietly. An assignment fails the script.
  PKG_ROOTS="$(python3 - "$REPO/projects.json" <<'PYROOTS'
import json, os, sys
doc = json.load(open(sys.argv[1], encoding="utf-8"))
for entry in doc.get("projects", []):
    if entry.get("active") is False:
        continue
    root = entry.get("root", "")
    if not root or os.path.isabs(root):
        continue
    # The copy below runs with --delete, so a root that resolves to the viewer
    # directory or anywhere above it would empty the deployment -- and the one
    # thing in there that cannot be got back is api/ticvai.db. "." is all it
    # takes. Refused here rather than guarded there, because this is where the
    # value comes from.
    here = os.path.normpath(os.path.join(os.sep, "viewer"))
    there = os.path.normpath(os.path.join(here, root))
    if there == here or here.startswith(there.rstrip(os.sep) + os.sep):
        sys.exit('root %r is the viewer directory or a parent of it' % root)
    print(root)
PYROOTS
)"
  while IFS= read -r rel; do
    [[ -n "$rel" ]] || continue
    if [[ -d "$REPO/$rel" ]]; then
      mkdir -p "$APP_DIR/viewer/$rel"
      rsync -a --delete --exclude '.git' --exclude 'node_modules' \
        "$REPO/$rel/" "$APP_DIR/viewer/$rel/"
      note "package $rel copied from beside the checkout"
    else
      note "package $rel is not beside the checkout — left as it is"
    fi
  done <<< "$PKG_ROOTS"
  chown -R "$APP_USER:$APP_USER" "$APP_DIR"
fi

# ── the packages ────────────────────────────────────────────────────────────
#
# Whatever was not copied above: a package with an absolute root, or one that
# lives in its own checkout beside the deployed viewer rather than beside the
# source. Those are still not this script's to fetch.
#
# But a package that was never checked out is a viewer that starts, answers every
# route and counts zero, which is the same shape as the bug that had the landing
# page drawing zeroes for weeks. So the roots are resolved here and a missing one
# stops the deploy with its own path in the message.
REGISTRY="$APP_DIR/viewer/projects.json"
if [[ -f "$REGISTRY" ]]; then
  MISSING_PKG="$(python3 - "$REGISTRY" "$APP_DIR/viewer" <<'PYPKG'
import json, os, sys
registry, viewer = sys.argv[1], sys.argv[2]
doc = json.load(open(registry, encoding="utf-8"))
gone = []
for entry in doc.get("projects", []):
    if entry.get("active") is False:
        continue
    root = os.path.normpath(os.path.join(viewer, entry.get("root", "")))
    if not os.path.isdir(root):
        gone.append("%s -> %s" % (entry.get("id", "?"), root))
print("; ".join(gone))
PYPKG
)"
  [[ -z "$MISSING_PKG" ]] || die \
    "a registered package is not on disk: $MISSING_PKG. Check it out beside the
viewer, or set \"active\": false in $REGISTRY. A viewer that starts without its
packages answers every route and counts zero."
  note "every registered package is on disk"
fi

# ── python ──────────────────────────────────────────────────────────────────
say "Python environment"
if [[ ! -x "$APP_DIR/.venv/bin/python" ]]; then
  python3 -m venv "$APP_DIR/.venv"
fi
"$APP_DIR/.venv/bin/pip" install -q --upgrade pip
# Named here rather than installed from viewer/api/requirements.txt, to keep the
# habit this script already has of every version being visible in the file that
# does the installing. The two lists have to agree; requirements.txt says the
# same four and the same two below it.
#
# openpyxl and python-multipart are the decisions upload. python-multipart is
# the one worth spelling out: FastAPI does not need it to start, so a venv
# without it comes up perfectly healthy and then raises the first time somebody
# posts the spreadsheet — a feature that 500s on a machine where nobody changed
# anything, which is the failure this line exists to prevent.
"$APP_DIR/.venv/bin/pip" install -q fastapi "uvicorn[standard]" argon2-cffi \
  openpyxl python-multipart
chown -R "$APP_USER:$APP_USER" "$APP_DIR/.venv"

# Asserted rather than assumed, for the same reason the gate and the cookie
# domain are asserted further down: a missing import here is invisible until an
# admin uploads a file, and by then the deploy has been declared done.
"$APP_DIR/.venv/bin/python" - <<'PYCHECK' || die "the venv is missing openpyxl or python-multipart — the decisions upload would fail at request time"
import importlib.util, sys
# "multipart" and not "python-multipart": the distribution is named one thing
# and the module it installs another, and find_spec asks about the module.
missing = [m for m in ("openpyxl", "multipart") if not importlib.util.find_spec(m)]
sys.exit(1 if missing else 0)
PYCHECK
note "openpyxl and python-multipart are in the venv"

# ── the store ───────────────────────────────────────────────────────────────
say "Database"
DB="$APP_DIR/viewer/api/ticvai.db"
if [[ -f "$DB" ]]; then
  note "$DB exists — left alone, accounts and verdicts intact"
else
  if [[ -z "$ADMIN_EMAIL" ]]; then
    die "No database yet and no --admin given. Re-run with --admin you@softlabsgroup.com"
  fi
  # This asks for a password on the terminal and does not take one as a flag,
  # which is deliberate: a password given as an argument sits in the shell
  # history and in `ps` for as long as the command runs. So the deploy pauses
  # here once, on the first run only.
  note "about to ask for a password for $ADMIN_EMAIL"
  sudo -u "$APP_USER" env TICVAI_DB="$DB" PYTHONPATH="$APP_DIR/viewer" \
    "$APP_DIR/.venv/bin/python" -m api.cli admin "$ADMIN_EMAIL"
  note "created, with $ADMIN_EMAIL as the first admin"
fi
chown "$APP_USER:$APP_USER" "$DB"

# ── pm2 ─────────────────────────────────────────────────────────────────────
say "Processes"

# Written here rather than committed, because it carries this machine's paths
# and ports. The file is the record of what is running; pm2's own dump is a
# cache of it.
cat > "$APP_DIR/ecosystem.config.cjs" <<CONFIG
// Generated by deploy/deploy.sh. Edit the script, not this.
module.exports = {
  apps: [
    {
      name: 'ticvai-api',
      cwd: '$APP_DIR/viewer',
      script: '$APP_DIR/.venv/bin/python',
      args: '-m uvicorn api.main:app --host 127.0.0.1 --port $API_PORT',
      interpreter: 'none',
      env: {
        TICVAI_DB: '$DB',
        PYTHONPATH: '$APP_DIR/viewer',
        PYTHONUNBUFFERED: '1',
        // The three that make two deployed names behave as one site. Set at the
        // top of deploy.sh, and written from there rather than added to this
        // file by hand — this file is regenerated on every deploy, so a
        // hand-edit survives exactly until the next one.
        TICVAI_ORIGINS: '$PUBLIC_ORIGIN',
        TICVAI_COOKIE_DOMAIN: '$COOKIE_DOMAIN',
        TICVAI_SECURE_COOKIE: '$SECURE_COOKIE',
      },
      autorestart: true,
      max_restarts: 20,
    },
    {
      name: 'ticvai-viewer',
      cwd: '$APP_DIR/viewer',
      script: 'server.mjs',
      args: '--host 127.0.0.1 --port $VIEWER_PORT',
      interpreter: 'node',
      env: {
        // Where the viewer forwards everything the accounts service owns.
        // Loopback: the two processes are on the same machine, and this is not
        // the address a browser uses.
        TICVAI_AUTH: 'http://127.0.0.1:$API_PORT',
      },
      autorestart: true,
      max_restarts: 20,
    },
  ],
};
CONFIG
chown "$APP_USER:$APP_USER" "$APP_DIR/ecosystem.config.cjs"

# startOrRestart, not start. `pm2 start` on an app that is already online is a
# no-op — it says "already launched" and returns 0 — so a redeploy would copy
# every new file into place and then leave the old processes running against
# them. The failure is silent and reads as "the deploy did nothing", which is
# exactly what it did: new code on disk, old code in memory, and an environment
# variable added to the config that never reaches the process.
#
# --update-env as well, because even on a restart pm2 otherwise reuses the
# environment a process was first started with.
sudo -u "$APP_USER" HOME="/home/$APP_USER" \
  pm2 startOrRestart "$APP_DIR/ecosystem.config.cjs" --update-env >/dev/null
sudo -u "$APP_USER" HOME="/home/$APP_USER" pm2 save >/dev/null

# Survive a reboot. pm2 startup prints a command to run as root rather than
# doing it, so this runs what it prints.
STARTUP="$(sudo -u "$APP_USER" HOME="/home/$APP_USER" pm2 startup systemd -u "$APP_USER" --hp "/home/$APP_USER" | tail -1)"
if [[ "$STARTUP" == sudo* || "$STARTUP" == env* ]]; then
  eval "$STARTUP" >/dev/null 2>&1 || note "could not install the boot hook automatically"
fi

# ── the nightly snapshot ────────────────────────────────────────────────────
say "Backups"
mkdir -p "$APP_DIR/backups"
chown "$APP_USER:$APP_USER" "$APP_DIR/backups"
cat > /usr/local/bin/ticvai-backup <<BACKUP
#!/usr/bin/env bash
# sqlite3 .backup rather than cp: a plain copy of a live database produces a
# file that opens and is wrong, which is worse than one that fails to open.
set -euo pipefail
sqlite3 "$DB" ".backup '$APP_DIR/backups/ticvai-\$(date +%Y%m%d-%H%M%S).db'"
ls -1t "$APP_DIR"/backups/ticvai-*.db | tail -n +15 | xargs -r rm --
BACKUP
chmod +x /usr/local/bin/ticvai-backup
cat > /etc/cron.d/ticvai-backup <<CRON
# The package can be regenerated from a dump. A verdict cannot be regenerated
# from anything.
17 3 * * * $APP_USER /usr/local/bin/ticvai-backup
CRON

# ── prove it ────────────────────────────────────────────────────────────────
say "Checking"
for i in $(seq 1 30); do
  curl -sf "http://127.0.0.1:$API_PORT/api/health" >/dev/null 2>&1 && break
  sleep 1
  [[ $i -eq 30 ]] && die "the accounts service never answered — pm2 logs ticvai-api"
done
note "accounts service up on $API_PORT"

for i in $(seq 1 30); do
  curl -so /dev/null "http://127.0.0.1:$VIEWER_PORT/login.html" && break
  sleep 1
  [[ $i -eq 30 ]] && die "the viewer never answered — pm2 logs ticvai-viewer"
done
note "viewer up on $VIEWER_PORT"

# Every package route the reading server owns has to be named in the API host's
# nginx block, because everything not named there goes to the accounts service,
# which has no code for any of them and answers 404. That is a list of routes
# kept in two files, and it drifted: `summary` and `diagrams` were added to
# server.mjs and not here, so the landing page drew zeroes for weeks — a count
# that fails to load and a count of nothing look the same.
#
# server.mjs is the authority, because that is where a route comes into
# existence. A new one now fails the deploy with its own name in the message
# rather than 404ing in somebody's browser later.
NGINX_SITE="$REPO/deploy/nginx/asterapi.ainfinite.ai"
if [[ -f "$NGINX_SITE" ]]; then
  # server.mjs spells a route as `route === 'index'` since the reads moved to
  # /pkg/<project>/. Matched on that form: the old pattern looked for
  # `url.pathname === '/api/index'`, which now finds nothing at all, and a
  # check comparing an empty list against an empty list passes every time.
  # It read `$REPO/viewer/server.mjs` for a while after $REPO stopped being
  # the tree that contained the viewer, which under `set -e` is not a check
  # that passes vacuously but a deploy that dies here — after pm2 has already
  # restarted both processes, so the services come up and the assertions
  # below them never run.
  #
  # `diagrams/detail` is trimmed to `diagrams`, because the nginx names are
  # matched with `(/|$)` and a parent already forwards its children. Left
  # whole it is reported as missing forever, and a check that cries wolf is
  # a check that gets ignored.
  # Two spellings, because server.mjs has two. Most routes arrive as
  # `route === 'index'` after the project prefix is parsed off, but a route
  # that exists *before* a project is known cannot -- so /pkg/projects, the
  # registry, is matched on the whole path instead. It was missed for exactly
  # that reason: nginx never forwarded it, every page 404ed on the first read
  # it makes, and this check had no idea the route existed.
  OWNED="$( {
      grep -oE "route === '[a-z-]+(/[a-z-]+)?'" "$REPO/server.mjs" \
        | grep -oE "'[a-z-]+(/[a-z-]+)?" | tr -d "'" || true
      grep -oE "url\.pathname === '/(api|pkg)/[a-z-]+'" "$REPO/server.mjs" \
        | sed -E "s|.*/(api\|pkg)/([a-z-]+)'|\2|" || true
    } | sed 's|/.*||' | sort -u)"
  # An empty list compared against anything passes, which is the failure this
  # check was rewritten once to escape. server.mjs always owns routes; a list
  # with none in it means the extraction broke, not that the drift is gone.
  [[ -n "${OWNED// /}" ]] || die \
    "no package routes found in $REPO/server.mjs -- the nginx drift check
cannot run, and an empty list would pass it silently."
  FORWARDED="$(grep -oE '\^/api/\([a-z|-]+\)' "$NGINX_SITE" \
                | tr -d '^()' | sed 's|/api/||' | tr '|' '\n' | sort -u)"
  # A `location /pkg/` covers every route of every project at once, so the
  # per-name list is only load-bearing while the old `/api/*` spelling is still
  # what the client calls. Where the prefix rule is present the names are
  # belt-and-braces; where it is absent a missing name is still a 404.
  if grep -qE '^[[:space:]]*location[[:space:]]+/pkg/' "$NGINX_SITE"; then
    note "nginx forwards /pkg/ — every package route, every project, one rule"
    MISSING=""
  else
    MISSING="$(comm -23 <(echo "$OWNED") <(echo "$FORWARDED") | tr '\n' ' ')"
  fi
  [[ -z "${MISSING// /}" ]] || die \
    "nginx does not forward $(echo "$MISSING" | sed 's|[a-z-][a-z-]*|/api/&|g')\
 — the accounts service will answer them 404. Add them to the location regex in\
 deploy/nginx/asterapi.ainfinite.ai."
  note "nginx forwards every package route server.mjs owns"
fi

# The gate, asserted rather than assumed. TICVAI_NO_GATE serves the whole
# package to anyone who asks; it exists for a workstation and must never be set
# here, so a stray value fails the deploy rather than quietly publishing
# everything.
CODE="$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$VIEWER_PORT/api/index")"
[[ "$CODE" == "401" ]] || die "the gate is open: /api/index answered $CODE to a stranger, wanted 401"
note "the gate holds — /api/index answers 401 without a session"

# The proxy is what makes one origin work, so it is checked too rather than
# assumed from the fact that both processes are running.
CODE="$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$VIEWER_PORT/api/health")"
[[ "$CODE" == "200" ]] || die "the viewer is not forwarding to the accounts service (got $CODE)"
note "the viewer forwards /api/* to the accounts service"

# The session cookie's domain, asserted for the same reason as the gate: it is
# invisible when it is wrong. A cookie missing its Domain is host-only to the
# name that issued it, so on a two-name deployment the reading server's gate
# never sees one — and the symptom is not an error anywhere but a sign-in that
# succeeds and returns you to the sign-in page, over and over, which reads to
# everyone involved as "the login page keeps refreshing".
#
# Checked against the running process rather than the config file, because the
# thing that goes wrong is precisely a config the process never picked up.
# /api/auth/logout sets the cookie's deletion with the same attributes it is
# created with, and needs no credentials to answer.
if [[ -n "$COOKIE_DOMAIN" ]]; then
  SET_COOKIE="$(curl -s -i -X POST "http://127.0.0.1:$API_PORT/api/auth/logout" | grep -i '^set-cookie' || true)"
  case "$SET_COOKIE" in
    *"Domain=$COOKIE_DOMAIN"*)
      note "the session cookie carries Domain=$COOKIE_DOMAIN" ;;
    *)
      die "the accounts service is not setting Domain=$COOKIE_DOMAIN on the session cookie.
       It answered: ${SET_COOKIE:-<no set-cookie at all>}
       The process is running without TICVAI_COOKIE_DOMAIN. Signing in will loop
       back to the sign-in page for anybody whose browser does not already hold
       a cookie for the front end's own name." ;;
  esac
fi

IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
say "Done"
cat <<DONE

    The viewer      http://${IP:-<this-server>}:$VIEWER_PORT
    The API docs    http://${IP:-<this-server>}:$API_PORT/docs

    pm2 status                     what is running
    pm2 logs ticvai-viewer         follow one of them
    pm2 restart ticvai-viewer      after a package drop
    ticvai-backup                  take a snapshot now

    This address has no certificate, deliberately for now. The password and the
    session cookie cross the network in clear text, so treat every account on it
    as public knowledge until that changes.

DONE
