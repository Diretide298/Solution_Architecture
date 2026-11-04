#!/usr/bin/env bash
# Fails the build on an unapproved breaking contract change.
# A break is permitted only when the merge request carries the `contract:major` label AND
# every spec with a break has had its info.version majored against the base.
#
# r13 system review D-10 (CHG-R14J-003): the label test was `[ "$PR_LABELS" == *"contract:major"* ]`, and `[` does
# no pattern matching, so a labelled break could never pass; the version-bump rule was printed and never checked; and
# only spine/ and satellite/ were compared (devices/ was left out). Now `[[ ]]` matches, the major is compared, and
# every folder of openapi/ except shared/ (components only) is read.
set -euo pipefail

BASE_REF="${BASE_REF:-origin/main}"
FAILED=0
UNBUMPED=()

mkdir -p .diff/base .diff/head

# The major of info.version: the first `  version:` line under `info:`.
major() {
  awk '/^info:/ {in_info = 1; next} /^[^ ]/ {in_info = 0}
       in_info && /^  version:/ {v = $2; gsub(/["\047]/, "", v); split(v, p, "."); print p[1]; exit}' "$1"
}

for spec in openapi/*/*.yaml; do
  [ -e "$spec" ] || continue
  case "$spec" in openapi/shared/*) continue ;; esac
  name="$(basename "$(dirname "$spec")")-$(basename "$spec")"

  if ! git show "${BASE_REF}:${spec}" > ".diff/base/${name}" 2>/dev/null; then
    echo "NEW  ${spec}: no baseline, skipping diff"
    continue
  fi
  cp "$spec" ".diff/head/${name}"

  if ! npx --yes oasdiff breaking \
        ".diff/base/${name}" ".diff/head/${name}" \
        --fail-on ERR --format text; then
    echo "BREAKING CHANGE in ${spec}"
    FAILED=1
    b="$(major ".diff/base/${name}")"
    h="$(major ".diff/head/${name}")"
    if [ -z "$b" ] || [ -z "$h" ] || [ "$h" -le "$b" ]; then
      UNBUMPED+=("${spec} (info.version major ${b:-?} -> ${h:-?})")
    fi
  fi
done

if [ "$FAILED" -eq 1 ]; then
  if [[ "${PR_LABELS:-}" == *contract:major* ]] && [ "${#UNBUMPED[@]}" -eq 0 ]; then
    echo "Breaking changes present, the merge request is labelled contract:major and every broken spec is majored: allowed."
    exit 0
  fi
  echo
  echo "Breaking changes require:"
  echo "  1. a major version bump in the spec's info.version"
  if [ "${#UNBUMPED[@]}" -gt 0 ]; then printf '     not bumped: %s\n' "${UNBUMPED[@]}"; fi
  echo "  2. the 'contract:major' merge request label"
  if [[ "${PR_LABELS:-}" != *contract:major* ]]; then echo "     not labelled"; fi
  echo "  3. a deprecation window: guest apps lag by store review (Direction §3.4.9)"
  exit 1
fi

echo "No breaking changes."
