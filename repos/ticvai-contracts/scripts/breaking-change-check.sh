#!/usr/bin/env bash
# Fails the build on an unapproved breaking contract change.
# A break is permitted only when the PR carries the `contract:major` label AND
# the spec version has been majored.
set -euo pipefail

BASE_REF="${BASE_REF:-origin/main}"
FAILED=0

mkdir -p .diff/base .diff/head

for spec in openapi/spine/*.yaml openapi/satellite/*.yaml; do
  [ -e "$spec" ] || continue
  name=$(basename "$spec")

  if ! git show "${BASE_REF}:${spec}" > ".diff/base/${name}" 2>/dev/null; then
    echo "NEW  ${name} — no baseline, skipping diff"
    continue
  fi
  cp "$spec" ".diff/head/${name}"

  if ! npx --yes oasdiff breaking \
        ".diff/base/${name}" ".diff/head/${name}" \
        --fail-on ERR --format text; then
    echo "BREAKING CHANGE in ${name}"
    FAILED=1
  fi
done

if [ "$FAILED" -eq 1 ]; then
  if [ "${PR_LABELS:-}" == *"contract:major"* ]; then
    echo "Breaking changes present but PR is labelled contract:major — allowed."
    exit 0
  fi
  echo
  echo "Breaking changes require:"
  echo "  1. a major version bump in the spec's info.version"
  echo "  2. the 'contract:major' PR label"
  echo "  3. a deprecation window — guest apps lag by store review (Direction §3.4.9)"
  exit 1
fi

echo "No breaking changes."
