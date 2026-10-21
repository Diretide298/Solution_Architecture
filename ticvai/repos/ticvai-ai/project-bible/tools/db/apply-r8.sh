#!/usr/bin/env bash
# Lives in the TICVAI package as ticvai/tools/db/apply-r8.sh (r9, CHG-R9MIG-003); the R8-DB task texts point at it.
# r8 apply for a repository-built database (Hrushikant's apply.sh, 21 Oct, with the two r8 retries made exact).
# usage: apply-r8.sh <host> <user> <tenant_db> <control_db> <logdir>     (PGPASSWORD, and PGPORT if not 5432, in env)
# Files: sql/tenant/*.sql and sql/control/*.sql beside this script (the 13 r8 files, from r8-db-files.zip).
# Each file runs as one transaction. Only tenant V0108 and control V0110 may be retried statement by statement,
# and only these errors are accepted (6 in all; anything else stops the run):
#   tenant V0108:  relation "marketing.privacy_exception" does not exist   (3; a table the repository has not built yet)
#                  column "scope_path" does not exist                       (2; platform.outbox_sequence keeps migration 240's shape, CR-166)
#   control V0110: relation "control.onboarding_application" does not exist (1; a table the repository has not built yet)
set -u
H=$1; U=$2; TDB=$3; CDB=$4; LOG=$5
BIN="${PGBIN:-/c/Program Files/PostgreSQL/18/bin}"; SQL="$(dirname "$0")/sql"
mkdir -p "$LOG"
TEN="V0103a__names_early_after_r1_20261020 V0105a__names_early_after_r1_20261020 V0107__names_after_r1_20261019 V0108__after_r1_20261020 V0109__names_after_r1_20261020 V0110__after_r1_20261020 V0111__names_after_r1_20261020 V0112__after_r1_20261021"
CON="V0107__names_after_r1_20261019 V0108__after_r1_20261020 V0109__names_after_r1_20261020 V0110__after_r1_20261020 V0112__after_r1_20261021"
accepted() { # side/file -> the error texts that file may raise
  case "$1" in
    tenant/V0108__after_r1_20261020) echo 'relation "marketing.privacy_exception" does not exist|column "scope_path" does not exist' ;;
    control/V0110__after_r1_20261020) echo 'relation "control.onboarding_application" does not exist' ;;
    *) echo '' ;;
  esac; }
run() { # db side file pass
  local L="$LOG/$4-$2-$3.log" ok; ok=$(accepted "$2/$3")
  "$BIN/psql" -h "$H" -U "$U" -d "$1" -X -q -1 -v ON_ERROR_STOP=1 -f "$SQL/$2/$3.sql" > "$L" 2>&1 && { echo "pass$4 $2 $3 ok"; return 0; }
  if [ -z "$ok" ]; then echo "pass$4 $2 $3 STOPPED: $(grep -m1 ERROR "$L" | sed 's/.*ERROR: *//')"; return 1; fi
  L="$LOG/$4-$2-$3.retry.log"
  "$BIN/psql" -h "$H" -U "$U" -d "$1" -X -q -v ON_ERROR_STOP=0 -f "$SQL/$2/$3.sql" > "$L" 2>&1
  local n bad; n=$(grep -c ERROR "$L"); bad=$(grep ERROR "$L" | grep -Ecv "$ok")
  echo "pass$4 $2 $3 retried: $n errors, $bad not accepted"
  [ "$bad" -eq 0 ] || { grep ERROR "$L" | grep -Ev "$ok" | head -5; return 1; }
}
for pass in 1 2; do
  for f in $TEN; do run "$TDB" tenant "$f" $pass || exit 1; done
  for f in $CON; do run "$CDB" control "$f" $pass || exit 1; done
done
echo "done: expect tenant V0108 retried with 5 errors and control V0110 with 1, on both passes; every other file ok"
