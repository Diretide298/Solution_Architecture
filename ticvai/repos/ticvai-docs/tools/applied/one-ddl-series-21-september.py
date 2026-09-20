#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Point the five documents that name a deleted file at the series that replaced it.

**Decided 21 September, Chinmay: delete both DDL generations and generate one fresh.** Done — but
*"delete both"* was the right instinct against a wrong description. The deep audit called them two
generations of the same thing. They were not:

    src/Ticvai.Migrations/Scripts/V0001__baseline.sql   extensions, scope vocabulary,
                                                        RLS, partition helper, outbox
    backend/tenant/*.sql, backend/control/*.sql         621 business tables, keys, indexes

**`backend/` had no row-level security at all** — zero `CREATE POLICY`, zero `ENABLE ROW LEVEL
SECURITY`, zero `CREATE EXTENSION` — and `V0001` was the only place it existed. Deleting both
without carrying it would have deleted the security model, and the default-deny with it.

**So the machinery moved into `tools/derive-ddl.py` and became part of the numbered series**,
which is what the file was kept out of `backend/` to avoid in the first place: a `V*.sql` sorts
after `010-` and would have applied last. Numbered `001-extensions.sql` and
`920-row-level-security.sql`, the order is the apply order, and it regenerates like everything
else.

**The estate gained security it never had.** The hand-written baseline protected three tables.
The generated series protects **242 by `scope_path` and 58 by `venue_id`** — the second family
written because `check-migrations` had been saying since it was written that *"checking only
scope_path missed 41 tables that carry venue_id instead; they would have passed with no policy at
all."*

**The second series was real and was somewhere else.** `repos/ticvai-backend/src/Ticvai.Migrations/
Scripts/` held `V0001`–`V0003b` dated 25 August — 39 tables, the exact set `backend/README.md`
records from the 31 August incident where *"the August definition won every time"*. That is the
one the README meant by *"if you hold an older series, delete it"*, and it is gone.

    python3 tools/applied/one-ddl-series-21-september.py --apply
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EDITS = [
    ("backend/MIGRATIONS.md",
     "    V0001__baseline.sql              platform, RLS, partitioning, outbox, pii   [DONE]",
     "    001-extensions.sql               ltree, btree_gist, pgcrypto                [DERIVED]\n"
     "    002-migration-register.sql       platform.schema_version                    [DERIVED]\n"
     "    010-<schema>.sql                 621 tables across 32 schemas               [DERIVED]\n"
     "    900-foreign-keys.sql             632 declared references                    [DERIVED]\n"
     "    910-indexes.sql                  conventions and scope paths                [DERIVED]\n"
     "    920-row-level-security.sql       242 by scope_path, 58 by venue_id          [DERIVED]\n"
     "    930-partitioning.sql             the venue partition helper (ADR-0044)      [DERIVED]"),

    ("docs/active/current-work.md",
     "- [x] **V0001__baseline.sql written** — RLS with `FORCE`, scope tree, partition helper, "
     "outbox,",
     "- [x] **The machinery layer is generated** (21 September) — RLS with `FORCE`, scope tree, "
     "partition helper, outbox,"),

    ("docs/active/current-work.md",
     "`V0001__baseline.sql` survives. It lives in `src/Ticvai.Migrations/Scripts/` regardless, "
     "because a",
     "**Superseded 21 September.** The machinery moved into `derive-ddl.py` and is emitted as "
     "`001-extensions.sql` and `920-row-level-security.sql`, so the whole series regenerates "
     "together. It used to live in `src/Ticvai.Migrations/Scripts/` because a"),

    ("handoff/schema.md",
     "## Applied — `V0001__baseline.sql`",
     "## Applied — the generated template under `backend/`"),

    ("handoff/schema.md",
     "`ticvai-backend/src/Ticvai.Migrations/Scripts/` — `V0001__baseline.sql` applied.",
     "`backend/tenant/` and `backend/control/`, applied in numeric order by "
     "`backend/provision-tenant.sh`. **Both `V*` series were deleted on 21 September** — the root "
     "baseline because its content is generated now, and the August `V0001`-`V0003b` set in the "
     "backend repo because it was the superseded generation."),

    ("docs/adr/0044-which-tables-partition-by-venue.md",
     "primary key, and composite foreign keys into it. The 74 columns are in scope. "
     "`V0001__baseline.sql`",
     "primary key, and composite foreign keys into it. The 74 columns are in scope. "
     "`backend/tenant/930-partitioning.sql`"),
]


def main():
    apply = "--apply" in sys.argv[1:]
    done = skipped = 0
    for rel, old, new in EDITS:
        path = os.path.join(ROOT, rel)
        s = io.open(path, encoding="utf-8").read()
        if new.split("\n")[0][:40] in s and old not in s:
            print("    %-46s already applied" % rel)
            skipped += 1
            continue
        if s.count(old) != 1:
            print("  !! %s: anchor matched %d times" % (rel, s.count(old)))
            return 1
        if apply:
            io.open(path, "w", encoding="utf-8", newline="\n").write(s.replace(old, new, 1))
        print("    %-46s %s" % (rel, old.strip()[:58]))
        done += 1

    # The thing this change is really about, asserted rather than assumed.
    for name, want in (("backend/tenant/920-row-level-security.sql", "apply_scope_rls"),
                       ("backend/tenant/001-extensions.sql", "CREATE EXTENSION"),
                       ("backend/tenant/930-partitioning.sql", "ensure_venue_partition")):
        if want not in io.open(os.path.join(ROOT, name), encoding="utf-8").read():
            print("  !! %s does not contain %s" % (name, want))
            return 1
    if os.path.exists(os.path.join(ROOT, "src", "Ticvai.Migrations")):
        print("  !! src/Ticvai.Migrations still exists")
        return 1
    print("\n    the machinery is in the numbered series · no V* series remains")

    if not apply:
        print("\n  %d edit(s) - pass --apply" % done)
        return 0
    print("  -> %d file(s) updated, %d already current" % (done, skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
