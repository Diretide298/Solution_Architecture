#!/usr/bin/env bash
# The release push on the OpenProject server (council item C6): the server pulls the release from git and runs
# it; nothing is pasted into its shell but the three commands below. OPENPROJECT-PUSH.md, "The release push".
#
# Host: pms.softlabsgroup.in (Contabo vmi163716), Docker container "openproject" (OpenProject 10.0.2).
# Checkout: /opt/ticvai-release, read-only (a deploy key or deploy token that can only read), sparse: only
# ticvai/tools and ticvai/handoff/service-docs are checked out.
#
# One time (as root; OPENPROJECT-PUSH.md has the read-only deploy key steps):
#   git clone --filter=blob:none --no-checkout <read-only repo url> /opt/ticvai-release
#   git -C /opt/ticvai-release sparse-checkout init --cone
#   git -C /opt/ticvai-release sparse-checkout set ticvai/tools ticvai/handoff/service-docs
#   git -C /opt/ticvai-release checkout main
#   (or, with this script copied over once:  bash op-release-server.sh setup <read-only repo url>)
#
# Per release rN (as root):
#   /opt/ticvai-release/ticvai/tools/op-release-server.sh dry-run r1
#   /opt/ticvai-release/ticvai/tools/op-release-server.sh apply r1
#   /opt/ticvai-release/ticvai/tools/op-release-server.sh apply r1 ONLY=descriptions BATCH=200   (staged pointers)
#
# dry-run  fetches the tags, checks out rN (refuses a dirty checkout), copies tools/op-release.rb and
#          handoff/service-docs/op-release.json into the container and runs the dry run. The log is kept in
#          /opt/ticvai-release/.release-out/ (excluded from git).
# apply    refuses unless a dry run of the same tag and the same bundle was run first (FORCE=1 overrides), backs
#          the database up (NO_BACKUP=1 skips; never on the first apply of a release), runs APPLY=1, then copies
#          /tmp/op-created.json out of the container to .release-out/op-created-rN.json and prints it. The lead
#          scp's it back (or copies the printed JSON) and merges it: python3 tools/op-created-merge.py <file>.
#
# Extra settings after the tag are passed to op-release.rb: ONLY, BATCH, SHOW, LIMIT, AUTHOR, ASSIGN_COMMENT,
# RETITLE (see the header of op-release.rb). Anything else is refused.
set -euo pipefail

CHECKOUT=${CHECKOUT:-/opt/ticvai-release}
CONTAINER=${CONTAINER:-openproject}
BACKUPS=${BACKUPS:-/root/databaseBackup}
PKG="$CHECKOUT/ticvai"
OUT="$CHECKOUT/.release-out"
RB="$PKG/tools/op-release.rb"
BUNDLE="$PKG/handoff/service-docs/op-release.json"
ALLOWED="ONLY BATCH SHOW LIMIT AUTHOR ASSIGN_COMMENT RETITLE"

die() { echo "op-release-server: $*" >&2; exit 1; }

usage() {
  sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
}

setup() {
  local url=${1:-}
  [ -n "$url" ] || die "setup needs the read-only repository url"
  [ -e "$CHECKOUT" ] && die "$CHECKOUT exists already; per release run: $0 dry-run rN"
  if ! git clone --filter=blob:none --no-checkout "$url" "$CHECKOUT"; then
    echo "partial clone refused by the server; cloning in full" >&2
    rm -rf "$CHECKOUT"
    git clone --no-checkout "$url" "$CHECKOUT"
  fi
  git -C "$CHECKOUT" sparse-checkout init --cone
  git -C "$CHECKOUT" sparse-checkout set ticvai/tools ticvai/handoff/service-docs
  git -C "$CHECKOUT" checkout main
  mkdir -p "$OUT"
  grep -qx '.release-out/' "$CHECKOUT/.git/info/exclude" 2>/dev/null || echo '.release-out/' >> "$CHECKOUT/.git/info/exclude"
  echo "checked out $(git -C "$CHECKOUT" rev-parse --short HEAD) into $CHECKOUT; next: $PKG/tools/op-release-server.sh dry-run rN"
}

checkout_tag() {
  local tag=$1
  [[ "$tag" =~ ^r[0-9]+$ ]] || die "a release tag looks like r1, r2 (got '$tag')"
  [ -d "$CHECKOUT/.git" ] || die "no checkout at $CHECKOUT; run the one-time setup first (header of this script)"
  mkdir -p "$OUT"
  grep -qx '.release-out/' "$CHECKOUT/.git/info/exclude" 2>/dev/null || echo '.release-out/' >> "$CHECKOUT/.git/info/exclude"
  if [ -n "$(git -C "$CHECKOUT" status --porcelain --untracked-files=no)" ]; then
    git -C "$CHECKOUT" status --short --untracked-files=no | head -20
    die "the checkout has local changes; it only ever holds a release tag. Inspect, then: git -C $CHECKOUT checkout -- ."
  fi
  git -C "$CHECKOUT" fetch --quiet --depth 1 origin tag "$tag" 2>/dev/null || git -C "$CHECKOUT" fetch --tags --prune --quiet origin
  git -C "$CHECKOUT" rev-parse -q --verify "refs/tags/$tag" >/dev/null || die "tag $tag not found on origin"
  # The two files are read straight from the tag, never by switching the working tree: git before 2.25 cannot
  # move a sparse checkout to another commit ("Sparse checkout leaves no entry", 1 October on git 2.17).
  local from="$OUT/$tag"
  mkdir -p "$from"
  git -C "$CHECKOUT" show "refs/tags/$tag:ticvai/tools/op-release.rb" > "$from/op-release.rb" || die "op-release.rb missing at $tag"
  git -C "$CHECKOUT" show "refs/tags/$tag:ticvai/handoff/service-docs/op-release.json" > "$from/op-release.json"     || die "op-release.json missing at $tag: build it with tools/op-release.py --release $tag and commit it before tagging"
  RB="$from/op-release.rb"
  BUNDLE="$from/op-release.json"
  grep -q "\"release\": \"$tag\"" "$BUNDLE" || die "the bundle at $tag is not for $tag: rebuild it (tools/op-release.py --release $tag)"
  # the bundle records the git blob of each plan file it was built from; at the tag they must be the same files
  local f want have
  for f in tasks.csv pms-map.json block-a-schedule.json; do
    want=$(grep -o "\"$f\": \"[0-9a-f]*\"" "$BUNDLE" | head -1 | cut -d'"' -f4)
    have=$(git -C "$CHECKOUT" rev-parse -q --verify "refs/tags/$tag:ticvai/handoff/service-docs/$f" || true)
    [ -n "$want" ] && [ "$want" = "$have" ] || die "the bundle at $tag was built from a different $f than the one at $tag: rebuild it (tools/op-release.py --release $tag), commit, re-tag"
  done
  echo "== $tag = $(git -C "$CHECKOUT" rev-parse --short "refs/tags/$tag^{commit}"); bundle sha256 $(bundle_sum | cut -c1-12)"
}

bundle_sum() { sha256sum "$BUNDLE" | cut -d' ' -f1; }

env_args() {
  local kv name
  ENV_ARGS=()
  for kv in "$@"; do
    [[ "$kv" == *=* ]] || die "extra settings are NAME=value (got '$kv')"
    name=${kv%%=*}
    [[ " $ALLOWED " == *" $name "* ]] || die "$name is not a setting op-release.rb takes ($ALLOWED)"
    ENV_ARGS+=(-e "$kv")
  done
}

copy_in() {
  docker inspect "$CONTAINER" >/dev/null 2>&1 || die "container $CONTAINER not found"
  docker cp "$RB" "$CONTAINER:/tmp/op-release.rb"
  docker cp "$BUNDLE" "$CONTAINER:/tmp/op-release.json"
}

run_rb() {   # $1 = log file, rest = docker exec -e arguments
  local log=$1; shift
  echo "== rails runner starts in about 75 s and prints nothing until then; do not interrupt it"
  docker exec "$@" "$CONTAINER" bash -c 'cd /app && bundle exec rails runner /tmp/op-release.rb /tmp/op-release.json' 2>&1 | tee "$log"
}

dry_run() {
  local tag=$1; shift
  env_args "$@"
  checkout_tag "$tag"
  copy_in
  local stamp log
  stamp=$(date +%Y%m%d-%H%M%S)
  log="$OUT/$tag-dryrun-$stamp.log"
  run_rb "$log" -e "EXPECT_RELEASE=$tag" ${ENV_ARGS[@]+"${ENV_ARGS[@]}"}
  bundle_sum > "$OUT/$tag-dryrun.sha256"
  echo "== dry run kept in $log. If the plan is right: $0 apply $tag $*"
}

apply() {
  local tag=$1; shift
  env_args "$@"
  checkout_tag "$tag"
  if [ "${FORCE:-0}" != "1" ]; then
    [ -f "$OUT/$tag-dryrun.sha256" ] || die "no dry run of $tag yet: $0 dry-run $tag first (FORCE=1 overrides)"
    [ "$(cat "$OUT/$tag-dryrun.sha256")" = "$(bundle_sum)" ] || die "the bundle changed since the dry run of $tag; dry-run again"
  fi
  local stamp log
  stamp=$(date +%Y%m%d-%H%M%S)
  if [ "${NO_BACKUP:-0}" = "1" ] && [ -f "$OUT/$tag-applied" ]; then
    echo "== NO_BACKUP=1: no backup (an earlier apply of $tag backed up)"
  else
    mkdir -p "$BACKUPS"
    echo "== database backup -> $BACKUPS/openproject-$stamp-$tag.dump"
    docker exec "$CONTAINER" bash -c 'pg_dump -Fc "$DATABASE_URL"' > "$BACKUPS/openproject-$stamp-$tag.dump"
    [ -s "$BACKUPS/openproject-$stamp-$tag.dump" ] || die "the backup is empty; nothing applied"
  fi
  copy_in
  docker exec "$CONTAINER" rm -f /tmp/op-created.json
  log="$OUT/$tag-apply-$stamp.log"
  local rc=0
  run_rb "$log" -e APPLY=1 -e "EXPECT_RELEASE=$tag" ${ENV_ARGS[@]+"${ENV_ARGS[@]}"} || rc=$?
  touch "$OUT/$tag-applied"
  # copied whatever happened later: the create phase commits on its own, so its ids must never be lost
  if docker exec "$CONTAINER" test -f /tmp/op-created.json; then
    docker cp "$CONTAINER:/tmp/op-created.json" "$OUT/op-created-$tag.json"
    echo "== new ticket ids ($OUT/op-created-$tag.json); merge them into pms-map.json with tools/op-created-merge.py:"
    cat "$OUT/op-created-$tag.json"
  else
    echo "== no op-created.json (the create phase did not run)"
  fi
  echo "== log kept in $log"
  [ "$rc" = "0" ] || die "op-release.rb stopped with status $rc; the phases before the failure are committed (see the log)"
}

status() {
  [ -d "$CHECKOUT/.git" ] || die "no checkout at $CHECKOUT"
  echo "checkout: $(git -C "$CHECKOUT" describe --tags --always) ($(git -C "$CHECKOUT" rev-parse --short HEAD))"
  echo "latest tags: $(git -C "$CHECKOUT" tag --list 'r*' --sort=-v:refname | head -5 | tr '\n' ' ')"
  ls -1t "$OUT" 2>/dev/null | head -10
}

cmd=${1:-}
[ $# -gt 0 ] && shift
case "$cmd" in
  setup)   setup "$@" ;;
  dry-run) [ $# -ge 1 ] || usage; dry_run "$@" ;;
  apply)   [ $# -ge 1 ] || usage; apply "$@" ;;
  status)  status ;;
  *)       usage ;;
esac
