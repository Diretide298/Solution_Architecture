#!/usr/bin/env bash
# The rehearsal pull in one command: the last gate step before a release is tagged (release runbook section 4;
# CHG-GRD-003, CHG-RHS-001), and the live re-pull after it (section 7).
#
#   bash tools/rehearse/rehearse.sh r<N>-rc --base <last live pull> [--op-snapshot <file>] [--block A]
#        [--work <folder>] [--ports 8998,8987,4373] [--jobs 4] [--keep]
#   bash tools/rehearse/rehearse.sh live-repull r<N> --rehearsal <work folder> --created <op-created-r<N>.json>
#        [--out <folder>] [--jobs 4]
#
# r<N>-rc: clones this repository into <work>/rc (objects shared, no remote, the mirrors only as ADAM's release
# export keeps them) at the candidate and tags it r<N> there only; takes r<N>'s bundle (committed, or built at the
# candidate with tools/op-release.py); replays the apply on OpenProject as it is now (simulate.py: the snapshot from
# `prepare.py snapshot`, else the last live pull) into the stand-in OpenProject; merges the created tickets' stand-in
# ids and builds and loads ADAM's ticket links as production does (tools/op-created-merge.py, tools/adam-links.py,
# viewer/api/load_links.py --prune, dry run then --apply); boots ADAM on the clone with a scratch database; pins every
# ticket at r<N-1>; pulls every ticket of the block with the shipped connector; judges the five criteria and writes
# the impact list (<work>/rehearsal-summary.md, rehearsal-report.json). Exit 0 pass, 1 fail, 2 not judged or refused.
# Nothing live: no remote, a scratch database, TICVAI_OP_TOKEN removed from every step, 127.0.0.1 only, never the
# ports 4173, 8787 or 8798 (another session's local ADAM and its fake OpenProject).
#
# live-repull: the rehearsal's list on the live ADAM after the release, each created ticket by its real id (the
# apply's op-created-r<N>.json); release, links, dead links and what each ticket touches must match the rehearsal.
# Needs ADAM_URL, ADAM_EMAIL and ADAM_PASSWORD (the audit account); it only reads. <out>/direct is the next
# rehearsal's --base.
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOP=$(git -C "$HERE" rev-parse --show-toplevel)
COMMON=$(git -C "$TOP" rev-parse --path-format=absolute --git-common-dir)
MAIN=$(cd "$COMMON/.." && pwd)
FORBIDDEN="4173 8787 8798"
if [ -n "${PYTHON:-}" ]; then PY=$PYTHON; elif python3 -c '' >/dev/null 2>&1; then PY=python3; else PY=python; fi

die() { echo "rehearse: $*" >&2; exit 2; }
native() { if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else printf '%s\n' "$1"; fi; }
py() { "$PY" "$@" | tr -d '\r'; }
json_get() { py -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get(sys.argv[2], ""))' "$(native "$1")" "$2"; }
usage() { sed -n '2,24p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 2; }

port_free() {  # nothing answers on 127.0.0.1:<port>, and it can be bound
  "$PY" - "$1" <<'EOF'
import socket, sys
p = int(sys.argv[1])
c = socket.socket()
c.settimeout(1)
try:
    c.connect(("127.0.0.1", p))
    sys.exit(1)
except OSError:
    pass
finally:
    c.close()
s = socket.socket()
try:
    s.bind(("127.0.0.1", p))
except OSError:
    sys.exit(1)
finally:
    s.close()
EOF
}

wait_url() {  # wait_url <url> <seconds> <what>: any HTTP answer counts
  "$PY" - "$1" "$2" <<'EOF' || die "$3 did not answer at $1 (see $W/run/*.log)"
import sys, time, urllib.error, urllib.request
url, until = sys.argv[1], time.time() + float(sys.argv[2])
while time.time() < until:
    try:
        urllib.request.urlopen(url, timeout=5)
        sys.exit(0)
    except urllib.error.HTTPError:
        sys.exit(0)
    except Exception:
        time.sleep(2)
sys.exit(1)
EOF
}

selftests() {
  local m
  for m in judge simulate prepare; do
    "$PY" "$HERE/$m.py" --self-test >/dev/null || die "$m.py self-tests fail: python tools/rehearse/$m.py --self-test"
  done
  node "$HERE/stand-in-openproject.mjs" --self-test >/dev/null \
    || die "the stand-in's self-tests fail: node tools/rehearse/stand-in-openproject.mjs --self-test"
}

PIDS=()
KEEP=0
stop() {
  if [ "$KEEP" = 1 ]; then echo "left running (--keep): ${PIDS[*]:-}"; return; fi
  local p
  for p in "${PIDS[@]:-}"; do [ -n "$p" ] && kill "$p" 2>/dev/null || true; done
}

rehearse() {
  local REF=$1; shift
  local BASE='' SNAP='' BLOCK=A WORK='' PORTS=8998,8987,4373 JOBS=4
  while [ $# -gt 0 ]; do
    case "$1" in
      --base) BASE=$2; shift 2;;
      --op-snapshot) SNAP=$2; shift 2;;
      --block) BLOCK=$2; shift 2;;
      --work) WORK=$2; shift 2;;
      --ports) PORTS=$2; shift 2;;
      --jobs) JOBS=$2; shift 2;;
      --keep) KEEP=1; shift;;
      *) die "unknown option $1";;
    esac
  done
  [[ "$REF" =~ ^r([1-9][0-9]*)-rc$ ]] || die "$REF is not r<N>-rc"
  local N=${BASH_REMATCH[1]}
  local REL=r$N PREV=r$((N - 1))
  local P_OP P_API P_VIEW p f
  IFS=, read -r P_OP P_API P_VIEW <<<"$PORTS"
  for p in $P_OP $P_API $P_VIEW; do
    for f in $FORBIDDEN; do
      [ "$p" != "$f" ] || die "port $p belongs to another session's local ADAM or its fake OpenProject: pass --ports"
    done
    port_free "$p" || die "port $p is in use: pass --ports"
  done
  [ -n "$BASE" ] && [ -f "$BASE/pull-log.jsonl" ] \
    || die "--base is the last live pull's folder (pull-log.jsonl and workspace/), e.g. the last release's live re-pull"
  [ -z "$SNAP" ] || [ -f "$SNAP" ] || die "no OpenProject snapshot at $SNAP"
  selftests

  local RC_COMMIT
  RC_COMMIT=$(git -C "$TOP" rev-parse --verify -q "$REF^{commit}") || die "no tag $REF here: tag the candidate first"
  git -C "$TOP" rev-parse --verify -q "$PREV^{commit}" >/dev/null || die "no tag $PREV here: the release before"
  local real
  if real=$(git -C "$TOP" rev-parse --verify -q "$REL^{commit}"); then
    [ "$real" = "$RC_COMMIT" ] \
      || echo "note: $REL exists here at ${real:0:8}; the rehearsal serves $REF (${RC_COMMIT:0:8}) as $REL in its own clone"
  fi
  W=${WORK:-${TMPDIR:-/tmp}/ticvai-rehearse-$REL}
  [ ! -e "$W/rc" ] || die "$W/rc exists from an earlier run: remove $W or pass --work <new folder>"
  mkdir -p "$W/run"
  trap stop EXIT
  echo "== candidate $REF = ${RC_COMMIT:0:8}, served as $REL; work folder $W"

  # 1. the candidate, in a clone of its own: shared objects, no remote, r<N> tagged there only
  git clone -q --shared --no-checkout "$COMMON" "$W/rc"
  git -C "$W/rc" remote remove origin
  git -C "$W/rc" show "$RC_COMMIT:viewer/lib/export-keep.json" > "$W/export-keep.json"
  local PATTERNS_TXT
  PATTERNS_TXT=$(py "$HERE/prepare.py" sparse --keep "$(native "$W/export-keep.json")") || die "prepare.py sparse failed"
  local -a PATTERNS
  mapfile -t PATTERNS <<<"$PATTERNS_TXT"
  MSYS_NO_PATHCONV=1 git -C "$W/rc" sparse-checkout set --no-cone "${PATTERNS[@]}"
  git -C "$W/rc" checkout -q --detach "$RC_COMMIT"
  local t
  for t in $(git -C "$W/rc" tag -l); do
    if [[ "$t" =~ ^r([0-9]+)$ ]] && [ "${BASH_REMATCH[1]}" -lt "$N" ]; then continue; fi
    git -C "$W/rc" tag -d "$t" >/dev/null
  done
  git -C "$W/rc" tag "$REL" "$RC_COMMIT"
  if [ -d "$TOP/viewer/node_modules" ]; then cp -r "$TOP/viewer/node_modules" "$W/rc/viewer/"
  elif [ -d "$MAIN/viewer/node_modules" ]; then cp -r "$MAIN/viewer/node_modules" "$W/rc/viewer/"
  else (cd "$W/rc/viewer" && npm ci --omit=dev --no-audit --no-fund); fi

  # 2. the bundles: r<N>'s (committed, or built at the candidate) and the one the last apply ran
  local CB="$W/rc/ticvai/handoff/service-docs/op-release.json" CREL BUNDLE_FROM
  CREL=$(json_get "$CB" release)
  if [ "$CREL" = "$REL" ]; then
    cp "$CB" "$W/op-release-$REL.json"; BUNDLE_FROM=committed
  else
    (cd "$W/rc/ticvai" && env -u TICVAI_OP_TOKEN "$PY" tools/op-release.py --release "$REL" \
      --out "$(native "$W/op-release-$REL.json")") || die "op-release.py could not build $REL's bundle at the candidate"
    BUNDLE_FROM="built at the candidate; the committed one is $CREL"
  fi
  if [ "$CREL" = "$PREV" ]; then cp "$CB" "$W/op-release-$PREV.json"
  else git -C "$W/rc" show "$PREV:ticvai/handoff/service-docs/op-release.json" > "$W/op-release-$PREV.json"; fi

  # 3. the stand-in OpenProject: the apply replayed on OpenProject as it is now
  echo "== the apply replayed for the stand-in OpenProject"
  "$PY" "$HERE/simulate.py" --bundle "$(native "$W/op-release-$REL.json")" --release "$REL" \
    --prev "$(native "$W/op-release-$PREV.json")" --base "$(native "$BASE")" \
    ${SNAP:+--op-snapshot "$(native "$SNAP")"} --rules "$(native "$W/rc/ticvai/tools/op-release.rb")" \
    --out "$(native "$W/op-state.json")" --created-out "$(native "$W/op-created-$REL.json")" \
    || die "simulate.py stopped (above)"

  # 4. ticket links, built as production builds them after the apply (never by this kit's own setup: P-22)
  echo "== ticket links: op-created-merge.py, adam-links.py"
  (cd "$W/rc/ticvai" && "$PY" tools/op-created-merge.py "$(native "$W/op-created-$REL.json")")
  (cd "$W/rc/ticvai" && env -u TICVAI_OP_TOKEN "$PY" tools/adam-links.py)

  # 5. ADAM on the candidate: the stand-in, the accounts service on a scratch database, the viewer serving r<N>
  echo "== ADAM on $REL: ports $P_OP (stand-in OpenProject), $P_API (accounts), $P_VIEW (viewer)"
  local REG DB OP_TOKEN KEY
  REG=$(native "$W/run/projects.json"); DB=$(native "$W/run/rehearsal.db")
  "$PY" "$HERE/prepare.py" registry --clone "$(native "$W/rc/ticvai")" --releases "$(native "$W/run/releases")" --out "$REG"
  OP_TOKEN=$(py -c 'import secrets; print(secrets.token_urlsafe(24))')
  KEY=$(py -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
  PORT=$P_OP TOKEN=$OP_TOKEN node "$HERE/stand-in-openproject.mjs" "$(native "$W/op-state.json")" >"$W/run/op.log" 2>&1 &
  PIDS+=($!)
  (cd "$W/rc/viewer" && exec env -u TICVAI_OP_TOKEN TICVAI_DB="$DB" TICVAI_SECRET_KEY="$KEY" \
    TICVAI_PMS_URL="http://127.0.0.1:$P_OP" TICVAI_PROJECTS="$REG" TICVAI_ORIGINS="http://localhost:$P_VIEW" \
    "$PY" -m uvicorn api.main:app --host 127.0.0.1 --port "$P_API") >"$W/run/api.log" 2>&1 &
  PIDS+=($!)
  (cd "$W/rc/viewer" && exec env -u TICVAI_OP_TOKEN TICVAI_AUTH="http://127.0.0.1:$P_API" \
    TICVAI_ORIGINS="http://localhost:$P_VIEW" TICVAI_PROJECTS="$REG" ADAM_PACKAGE_REF="$REL" \
    node server.mjs --port "$P_VIEW") >"$W/run/viewer.log" 2>&1 &
  PIDS+=($!)
  wait_url "http://127.0.0.1:$P_OP/__rehearsal/stats" 60 "the stand-in OpenProject"
  wait_url "http://127.0.0.1:$P_API/api/health" 120 "ADAM's accounts service"
  wait_url "http://127.0.0.1:$P_VIEW/pkg/projects" 1800 "ADAM's viewer (it exports $REL before it listens)"
  "$PY" "$HERE/prepare.py" served --releases "$(native "$W/run/releases")" --tag "$REL" --commit "$RC_COMMIT" \
    || die "ADAM is not serving $REL at ${RC_COMMIT:0:8}: see $W/run/viewer.log"

  # 6. the account, the links loaded the production way, the ticket list, the pins
  local PROJECT EMAIL LINKS
  PROJECT=$(json_get "$W/op-release-$REL.json" project)
  "$PY" "$HERE/prepare.py" account --api "http://127.0.0.1:$P_API" --origin "http://localhost:$P_VIEW" \
    --op "http://127.0.0.1:$P_OP" --op-token "$OP_TOKEN" --project "$PROJECT" --env-out "$(native "$W/run/account.env")" \
    || die "the rehearsal account could not be set up (above; $W/run/api.log)"
  EMAIL=$(sed -n 's/^ADAM_EMAIL=//p' "$W/run/account.env")
  LINKS=$(native "$W/rc/ticvai/handoff/service-docs/adam-links.json")
  echo "== ticket links: load_links.py --prune, dry run then --apply (production's command)"
  "$PY" "$W/rc/viewer/api/load_links.py" "$LINKS" --email "$EMAIL" --prune --db "$DB"
  "$PY" "$W/rc/viewer/api/load_links.py" "$LINKS" --email "$EMAIL" --prune --db "$DB" --apply
  "$PY" "$HERE/prepare.py" tickets --clone "$(native "$W/rc/ticvai")" --bundle "$(native "$W/op-release-$REL.json")" \
    --block "$BLOCK" --created "$(native "$W/op-created-$REL.json")" --base "$(native "$BASE")" \
    --out "$(native "$W/tickets.json")" || die "the ticket list could not be built (above)"
  "$PY" "$HERE/prepare.py" pins --db "$DB" --email "$EMAIL" --tickets "$(native "$W/tickets.json")" --tag "$PREV" \
    --commit "$(git -C "$W/rc" rev-parse "$PREV^{commit}")"
  py -c 'import json,sys; json.dump(dict(zip(sys.argv[2::2], sys.argv[3::2])), open(sys.argv[1], "w"), indent=1)' \
    "$(native "$W/rehearsal.json")" candidate "$REF" commit "$RC_COMMIT" release "$REL" previous "$PREV" \
    base "$(native "$BASE")" snapshot "${SNAP:+$(native "$SNAP")}" block "$BLOCK" bundle "$BUNDLE_FROM" ports "$PORTS"

  # 7. every ticket of the block, with the shipped connector
  echo "== pulling every Block $BLOCK ticket with the candidate's connector"
  ( set -a; . "$W/run/account.env"; set +a
    export ADAM_URL="http://127.0.0.1:$P_VIEW" ADAM_PROJECT=ticvai
    node "$HERE/pull-direct.mjs" --connector "$(native "$W/rc/viewer/mcp")" --tickets "$(native "$W/tickets.json")" \
      --out "$(native "$W/direct")" --jobs "$JOBS" ) | tee "$W/run/pull.out"

  # 8. judge
  py -c 'import sys,urllib.request; open(sys.argv[2], "wb").write(urllib.request.urlopen(sys.argv[1]).read())' \
    "http://127.0.0.1:$P_OP/__rehearsal/stats" "$(native "$W/run/op-stats.json")"
  local code=0
  "$PY" "$HERE/judge.py" rehearsal --work "$(native "$W")" --release "$REL" --base "$(native "$BASE")" || code=$?
  echo "== summary: $W/rehearsal-summary.md; impact list: $W/rehearsal-report.json"
  exit "$code"
}

live_repull() {
  local REL=${1:-}
  [ $# -gt 0 ] && shift
  [[ "$REL" =~ ^r[1-9][0-9]*$ ]] || die "live-repull takes the release, r<N>"
  local REH='' CREATED='' OUT='' JOBS=4 f
  while [ $# -gt 0 ]; do
    case "$1" in
      --rehearsal) REH=$2; shift 2;;
      --created) CREATED=$2; shift 2;;
      --out) OUT=$2; shift 2;;
      --jobs) JOBS=$2; shift 2;;
      *) die "unknown option $1";;
    esac
  done
  [ -n "${ADAM_URL:-}" ] && [ -n "${ADAM_EMAIL:-}" ] && [ -n "${ADAM_PASSWORD:-}" ] \
    || die "set ADAM_URL, ADAM_EMAIL and ADAM_PASSWORD (the audit account); the re-pull only reads"
  for f in $FORBIDDEN; do
    case "$ADAM_URL" in *:$f|*:$f/*) die "ADAM_URL names port $f, another session's local ADAM";; esac
  done
  [ -f "$REH/tickets.json" ] && [ -f "$REH/op-created-$REL.json" ] && [ -d "$REH/rc/viewer/mcp" ] \
    || die "--rehearsal is the rehearsal's work folder (tickets.json, op-created-$REL.json, rc/)"
  [ -f "$CREATED" ] || die "--created is the apply's op-created-$REL.json (.release-out/ on the OpenProject server)"
  OUT=${OUT:-$REH/live}
  mkdir -p "$OUT"
  "$PY" "$HERE/prepare.py" live --tickets "$(native "$REH/tickets.json")" \
    --stand-in "$(native "$REH/op-created-$REL.json")" --created "$(native "$CREATED")" \
    --out "$(native "$OUT/tickets-live.json")" || die "the live list could not be built (above)"
  node "$HERE/pull-direct.mjs" --connector "$(native "$REH/rc/viewer/mcp")" --tickets "$(native "$OUT/tickets-live.json")" \
    --out "$(native "$OUT/direct")" --jobs "$JOBS" | tee "$OUT/pull.out"
  local code=0
  "$PY" "$HERE/judge.py" live --rehearsal "$(native "$REH")" --live "$(native "$OUT")" --release "$REL" || code=$?
  echo "== $OUT/live-repull-summary.md; the next rehearsal's --base is $OUT/direct"
  exit "$code"
}

[ $# -ge 1 ] || usage
case "$1" in
  -h|--help) usage;;
  live-repull) shift; live_repull "$@";;
  r[0-9]*-rc) rehearse "$@";;
  *) die "the first argument is r<N>-rc (the candidate tag) or live-repull";;
esac
