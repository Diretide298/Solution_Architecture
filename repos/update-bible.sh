#!/usr/bin/env bash
# Copies ticvai-docs into every repo as project-bible/.
#
# project-bible/ is a copy, not a source. Edit ticvai-docs and re-run this.
# Anything edited inside a repo's project-bible/ is overwritten here.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Source resolution -------------------------------------------------------
# The docs may live either as a sibling of this workspace or inside it. Editing
# one location and syncing from the other silently drops changes — that has
# happened once, so resolution is explicit and the in-tree copy is refreshed
# from the sibling whenever both exist.
SIBLING="$(cd "$ROOT/.." 2>/dev/null && pwd)/ticvai-docs"
INTREE="$ROOT/ticvai-docs"

if [[ -d "$SIBLING" && "$SIBLING" != "$INTREE" ]]; then
  # Refuse to destroy work. Anything present in the in-tree copy but absent from the
  # sibling was authored in the wrong place — overwriting it silently loses it, which
  # has happened once and cost a directory of screen definitions.
  if [[ -d "$INTREE" ]]; then
    ONLY_IN_TREE=$(diff -rq "$SIBLING" "$INTREE" 2>/dev/null | grep "^Only in $INTREE" || true)
    if [[ -n "$ONLY_IN_TREE" ]]; then
      echo "REFUSING TO SYNC — these exist only in the in-tree copy and would be destroyed:" >&2
      echo "$ONLY_IN_TREE" >&2
      echo >&2
      echo "They were authored in the wrong place. Move them to $SIBLING and re-run." >&2
      exit 1
    fi
    if ! diff -rq "$SIBLING" "$INTREE" >/dev/null 2>&1; then
      echo "refreshing in-tree ticvai-docs from $SIBLING"
    fi
  fi
  rm -rf "$INTREE"
  cp -r "$SIBLING" "$INTREE"
  SRC="$SIBLING"
elif [[ -d "$INTREE" ]]; then
  SRC="$INTREE"
else
  echo "ticvai-docs not found at $SIBLING or $INTREE" >&2
  exit 1
fi

echo "source: $SRC"

REPOS=(ticvai-contracts ticvai-backend ticvai-frontend ticvai-ai ticvai-infra)

for repo in "${REPOS[@]}"; do
  target="$ROOT/$repo"
  [[ -d "$target" ]] || { echo "skip: $repo"; continue; }

  rm -rf "$target/project-bible"
  cp -r "$INTREE" "$target/project-bible"

  # The docs repo's own CI and agent files do not belong in a consumer.
  rm -rf "$target/project-bible/.github" \
         "$target/project-bible/CLAUDE.md" \
         "$target/project-bible/AGENTS.md"

  date -u +"%Y-%m-%dT%H:%M:%SZ" > "$target/project-bible/.synced-at"
  echo "updated: $repo ($(find "$target/project-bible" -name '*.md' | wc -l | tr -d ' ') pages)"
done

echo
echo "Commit the project-bible/ change in each repo."
