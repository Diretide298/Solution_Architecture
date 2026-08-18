#!/usr/bin/env bash
#
# Stand the TICVAI viewer up on a fresh Ubuntu or Debian server.
#
#   sudo ./deploy/setup.sh --admin you@softlabsgroup.com
#
# Safe to run again: every step checks before it acts, so a second run upgrades
# the units and the nginx site without touching the database or the accounts.
#
# What it leaves running:
#   nginx        :80        the only port open to the world
#     ├─ /api/auth, /api/accounts, /api/invites, /api/validation, /api/verdicts
#     │                 →  127.0.0.1:8787   accounts and verdicts (FastAPI)
#     └─ everything else  →  127.0.0.1:4173   the delivery package (Node)
#
# Both services bind the loopback address only. Nothing but nginx can be
# reached from outside, which is why there is one place to put a certificate
# when there is a name to put one on.

set -euo pipefail

APP_USER="${APP_USER:-ticvai}"
APP_DIR="${APP_DIR:-/srv/ticvai}"
ADMIN_EMAIL=""
SKIP_NGINX=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --admin) ADMIN_EMAIL="${2:-}"; shift 2 ;;
    --dir) APP_DIR="${2:-}"; shift 2 ;;
    --user) APP_USER="${2:-}"; shift 2 ;;
    --no-nginx) SKIP_NGINX=1; shift ;;
    -h|--help) sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[[ $EUID -eq 0 ]] || { echo "run with sudo — it installs packages and systemd units" >&2; exit 1; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"

say() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }

# ---------------------------------------------------------------- packages --
say "Packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip nginx curl ca-certificates

# Node 22 or newer: server.mjs uses fetch, AbortSignal.timeout and node:sqlite.
NODE_OK=0
if command -v node >/dev/null 2>&1; then
  [[ "$(node -p 'process.versions.node.split(".")[0]')" -ge 22 ]] && NODE_OK=1
fi
if [[ $NODE_OK -eq 0 ]]; then
  say "Node 22 (the packaged one is too old for fetch and node:sqlite)"
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y -qq nodejs
fi
echo "  node $(node -v) · python $(python3 -V | cut -d' ' -f2) · nginx present"

# ------------------------------------------------------------------- user ----
say "Service account"
if ! id -u "$APP_USER" >/dev/null 2>&1; then
  useradd --system --create-home --home-dir "/home/$APP_USER" --shell /usr/sbin/nologin "$APP_USER"
  echo "  created $APP_USER"
else
  echo "  $APP_USER exists"
fi

# ------------------------------------------------------------------ files ----
say "Application at $APP_DIR"
mkdir -p "$APP_DIR"
# The repository is the source of truth; this is a copy the service owns. The
# database is excluded so a redeploy can never overwrite live accounts with
# whatever happened to be in a working tree — the one way to lose real review
# work to a deploy.
rsync -a --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '__pycache__' \
  --exclude '.venv' \
  --exclude 'arabic-embed-eval' \
  --exclude 'repos' \
  --exclude 'viewer/api/ticvai.db*' \
  "$REPO/" "$APP_DIR/"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

# ------------------------------------------------------------ python deps ----
say "Python environment"
if [[ ! -x "$APP_DIR/.venv/bin/python" ]]; then
  python3 -m venv "$APP_DIR/.venv"
fi
"$APP_DIR/.venv/bin/pip" install -q --upgrade pip
"$APP_DIR/.venv/bin/pip" install -q -r "$APP_DIR/viewer/api/requirements.txt" uvicorn
chown -R "$APP_USER:$APP_USER" "$APP_DIR/.venv"

# --------------------------------------------------------------- database ----
say "Database"
DB="$APP_DIR/viewer/api/ticvai.db"
if [[ -f "$DB" ]]; then
  echo "  $DB exists — left alone, accounts and verdicts intact"
else
  sudo -u "$APP_USER" env TICVAI_DB="$DB" "$APP_DIR/.venv/bin/python" \
    -c 'import sys; sys.path.insert(0, "'"$APP_DIR/viewer"'"); from api import db; db.init(); print("  created", db.DB_PATH)'
fi

# ----------------------------------------------------------------- units -----
say "systemd units"
for unit in ticvai-api.service ticvai-viewer.service ticvai-backup.service ticvai-backup.timer; do
  install -m 644 "$HERE/$unit" "/etc/systemd/system/$unit"
  sed -i "s#@APP_DIR@#$APP_DIR#g; s#@APP_USER@#$APP_USER#g" "/etc/systemd/system/$unit"
done
systemctl daemon-reload
systemctl enable --now ticvai-api.service ticvai-viewer.service
systemctl restart ticvai-api.service ticvai-viewer.service
# The verdicts are the only thing here nobody can regenerate.
apt-get install -y -qq sqlite3
systemctl enable --now ticvai-backup.timer

# ----------------------------------------------------------------- nginx -----
if [[ $SKIP_NGINX -eq 0 ]]; then
  say "nginx"
  install -m 644 "$HERE/nginx.conf" /etc/nginx/sites-available/ticvai
  ln -sf /etc/nginx/sites-available/ticvai /etc/nginx/sites-enabled/ticvai
  rm -f /etc/nginx/sites-enabled/default
  nginx -t
  systemctl reload nginx
fi

# ----------------------------------------------------------------- checks ----
say "Waiting for both services"
for i in $(seq 1 30); do
  if curl -fsS http://127.0.0.1:8787/api/health >/dev/null 2>&1; then break; fi
  sleep 1
done
curl -fsS http://127.0.0.1:8787/api/health >/dev/null \
  && echo "  accounts service answering on 8787" \
  || { echo "  accounts service is not answering — journalctl -u ticvai-api" >&2; exit 1; }

# The gate is the thing most worth proving, so prove it rather than assume it:
# an unauthenticated call must not return the package.
CODE="$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:4173/api/index)"
if [[ "$CODE" == "401" ]]; then
  echo "  gate holding — /api/index answers 401 without a session"
else
  echo "  GATE NOT HOLDING — /api/index answered $CODE, expected 401" >&2
  echo "  is TICVAI_OPEN=1 set? it must not be on a public address" >&2
  exit 1
fi

# ------------------------------------------------------------ first admin ----
if [[ -n "$ADMIN_EMAIL" ]]; then
  say "First admin"
  if sudo -u "$APP_USER" env TICVAI_DB="$DB" PYTHONPATH="$APP_DIR/viewer" \
       "$APP_DIR/.venv/bin/python" -m api.cli list 2>/dev/null | grep -qi "$ADMIN_EMAIL"; then
    echo "  $ADMIN_EMAIL already has an account"
  else
    sudo -u "$APP_USER" env TICVAI_DB="$DB" PYTHONPATH="$APP_DIR/viewer" \
      "$APP_DIR/.venv/bin/python" -m api.cli admin "$ADMIN_EMAIL"
  fi
fi

IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
cat <<EOF

  Ready.  http://${IP:-<this-server>}/

  Sign in, then invite the rest:
    sudo -u $APP_USER env TICVAI_DB=$DB PYTHONPATH=$APP_DIR/viewer \\
      $APP_DIR/.venv/bin/python -m api.cli invite them@example.com --role reviewer \\
      --base http://${IP:-<this-server>}

  Logs:     journalctl -u ticvai-viewer -u ticvai-api -f
  Redeploy: git pull && sudo ./deploy/setup.sh

  This address has no certificate, so the password and the session cookie
  cross the internet in clear text. Anyone on the path can read both. Put a
  name and a cert in front before this holds anything you would mind losing —
  nginx.conf is the one file that needs to change, and setup.sh will then set
  TICVAI_SECURE_COOKIE=1 for you.
EOF
