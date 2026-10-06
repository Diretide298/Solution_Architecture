#!/usr/bin/env python3
"""After `r1`, the baseline migrations do not change. A table change after r1 is a new forward migration.

**Plan item 1C (C3), council of 1 October.** Until the first release, `backend/` is a template that
`tools/derive-ddl.py` rewrites whenever the schema reference changes, and that is right: nothing has
been applied anywhere. From `r1` on, the files under `backend/control/` and `backend/tenant/` are what
databases were built from, and a database cannot be re-run from an edited file. A change after r1 has
to reach a running database as a migration of its own, applied after the ones it already has.

**What fails**, once the git tag `r1` exists:

  changed    a `.sql` file under `backend/` that existed at r1 differs from r1 (forward migrations
             included: a forward migration merged after r1 is as frozen as the baseline)
  deleted    a `.sql` file that existed at r1 is gone
  new        a new baseline file (`NNN-*.sql`) after r1 -- a new schema is a forward migration too

A new forward migration (`backend/<area>/V<nnnn>__*.sql`) is what a change is supposed to become, and
passes. `derive-ddl.py` writes those itself in frozen mode; the changes it cannot write (drops,
renames, type changes) it lists for a person in `handoff/migration-review.md`, which this reports but
does not fail on.

Before r1 this passes and says the baseline is not frozen yet.

    python3 tools/check-migration-freeze.py                  # against the tag r1
    python3 tools/check-migration-freeze.py --baseline HEAD  # testing: any commit-ish as the baseline
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from release_baseline import ROOT, baseline_commit, changed_since, describe  # noqa: E402

FORWARD = re.compile(r"^backend/(?:control|tenant)/V\d+__[\w.-]+\.sql$")
REVIEW = ROOT / "handoff" / "migration-review.md"

# Deleted on purpose after r1, decided by the lead (CHG-SQL-001, Chinmay, 6 October 2026): the forward
# migrations derive-ddl wrote against the OLD r1 (a1ba956) before the fresh start. The fresh r1 (9cec72d)
# regenerated the baselines with all of their changes (five columns since renamed or moved), so they only
# re-applied columns with IF NOT EXISTS. These six paths, and nothing else, may be absent.
RETIRED = {
    "backend/control/V0100__after_r1_20261002.sql",
    "backend/control/V0101__after_r1_20261002.sql",
    "backend/control/V0102__after_r1_20261003.sql",
    "backend/tenant/V0100__after_r1_20261002.sql",
    "backend/tenant/V0101__after_r1_20261002.sql",
    "backend/tenant/V0102__after_r1_20261003.sql",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default=None, help="commit-ish to freeze against (default: the tag r1)")
    a = ap.parse_args()

    commit = baseline_commit(a.baseline)
    if not commit:
        print(f"PASS - not frozen yet: no {a.baseline or 'r1'} tag, so derive-ddl.py still regenerates "
              "the baseline migrations")
        return 0

    errors, forward = [], []
    for status, path in changed_since(commit, "backend"):
        if not path.endswith(".sql"):
            continue
        if status == "M":
            errors.append(f"changed   {path} differs from {describe(a.baseline, commit)}")
        elif status == "D" and path in RETIRED:
            print(f"  retired   {path} (CHG-SQL-001)")
        elif status == "D":
            errors.append(f"deleted   {path} existed at {describe(a.baseline, commit)}")
        elif FORWARD.match(path):
            forward.append(path)
        else:
            errors.append(f"new       {path} is a baseline file added after {describe(a.baseline, commit)}; "
                          "a new schema or table is a forward migration (backend/<area>/V<nnnn>__*.sql)")

    print(f"baseline frozen at {describe(a.baseline, commit)}; {len(forward)} forward migration(s) since")
    for f in sorted(forward):
        print(f"  forward   {f}")
    if REVIEW.exists():
        pending = [l for l in REVIEW.read_text(encoding="utf-8").splitlines() if l.startswith("| ") and
                   not l.startswith(("| Kind", "|---", "| ---"))]
        if pending:
            print(f"  note      {len(pending)} change(s) derive-ddl.py would not generate wait for a person "
                  f"in {REVIEW.relative_to(ROOT).as_posix()}")
    for e in errors:
        print(f"  {e}")
    if errors:
        print(f"FAIL - {len(errors)} baseline migration file(s) changed since "
              f"{describe(a.baseline, commit)}; revert them and let derive-ddl.py write the change as a "
              "forward migration")
        return 1
    print(f"PASS - every baseline migration is byte-identical to {describe(a.baseline, commit)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
