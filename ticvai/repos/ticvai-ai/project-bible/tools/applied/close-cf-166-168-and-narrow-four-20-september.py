#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two conflicts closed, four narrowed, and one backlog entry that has been four times its size.

Everything here was re-tested against the package this afternoon. **Nothing closes on a reading
of its own row** — that is how BL-160 was closed in August against evidence for a different gap,
and how CF-166 came to sit open for a month with all four of its asks already built.

## CF-166 — closed. Its row was never finished

It reads *"three of four gaps closed, and the fourth was never a gap"*, quotes the 21 August
decision, and **stops.** No owner, no date — the row has two cells where every other row in the
section has four. So it has been reported as open ever since, by a register that is parsed by
section rather than by sentence.

All four asks exist in `contracts/satellite/seating.yaml`:

    full copy-paste between seat maps      cloneSeatMap
    partial, section-level copy-paste      copySeatMapSection
    layout version-comparison view         diffSeatMapVersions
    AI-assisted import, PDF/image/CSV      importSeatMap, getSeatMapImport

## CF-168 — closed. The threshold is taken, and ADR-0047 found what it was missing

ADR-0042 decided placement on 8 September and left one number. **Twelve days and nothing has
contradicted it**, so it is taken: add an instance when peak connections hold at or above **70%
of `max_connections` on three days in a rolling seven, at least two non-consecutive.**

**And ADR-0047 found the defect underneath it.** `control.cell_instance` carries `id`, `cell_id`,
`name`, `status`, `max_connections`, `created_at`, `retired_at` — **and no role.** ADR-0042 places
a new tenant on the *emptiest* instance in the region, and an archive instance is by design the
emptiest thing in the estate, so the first tenant provisioned after an archive server exists would
land on it. The same column is why a burst environment cannot be placed at all: it has no trailing
history, so emptiest-first would put the most violent workload in the estate onto whichever
instance has the least headroom to absorb it.

## Four narrowed, none closed

**CF-64** keeps only the RPO floor, which is Dinesh's and is not ours to take. Retention is
decided by ADR-0047 — three stages, five years from last activity, floor-aware defaults.

**CF-165** is decided and not built. It closes when the five contract changes ADR-0047 names
land, on the rule CF-135 set: *"decided and built 18 August. Closed."*

**CF-162** keeps the reconciliation path, which has no design. The burst environment's shape is
settled by ADR-0047.

**CF-170** goes from seventeen screens to sixteen. **Class D is verified a false positive**:
`ADM-029 Deployment Monitor` declares twelve operations including `startRollout`, `pauseRollout`
and `rollbackRollout`, and is a real deployment actor the rule caught because rollout control is
not named `publish*`. **Class B is verified still broken** — all five still declare an `approve*`
and nothing else.

**CF-171** is re-measured, not fixed: **577 of 2,056, 28%**, where the row says 577 of 1,626, 35%.
Not one has been specified. **The figure was wrong in our favour**, which is the direction that
does not get noticed.

## BL-110 — not 48 things

Its 43 traceability rows carry **one note repeated forty times**. Walked against the package: 17
are already served, 14 are a condition on an existing `Grant`, 11 are a screen or a report, and 6
are new — of which 5 are live venue state that belongs at the gate rather than in `identity`.

    python3 tools/applied/close-cf-166-168-and-narrow-four-20-september.py --apply
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "docs", "registers", "conflicts.md")
BACKLOG = os.path.join(ROOT, "handoff", "contract-backlog.json")

CLOSED_SECTION = "### By research or architecture\n\n| ID | Issue | Closed by | ADR |\n|---|---|---|---|\n"

CF166_ROW = (
    "| **CF-166** | Seat map reuse and comparison — the 21 August decision asked for full and "
    "partial section-level copy-paste between seat maps, a layout version-comparison view, and "
    "AI-assisted import from PDF, image, Excel or CSV | **Closed 20 September.** All four exist "
    "in `contracts/satellite/seating.yaml` and were verified operation by operation: "
    "`cloneSeatMap` (full copy), `copySeatMapSection` (partial), `diffSeatMapVersions` "
    "(comparison), `importSeatMap` with `getSeatMapImport` (import). **This row was never "
    "finished** — it stated the decision, said three of four were closed and the fourth was "
    "never a gap, and stopped, with no owner and no date where every other row has both. **The "
    "register is parsed by section, so an unfinished row reads as an open conflict**, and this "
    "one has read that way for a month while the work was done. | — |\n"
)

CF168_ROW = (
    "| **CF-168** | A region may hold more than one Postgres instance, and nothing decided when "
    "to add one or which instance a new tenant lands on | **Closed 20 September.** Placement was "
    "decided 8 September by ADR-0042 — emptiest-first with a pin, where *emptiest* is peak "
    "concurrent connections over the trailing 7 days as a fraction of that instance's own "
    "`max_connections`. **The threshold it left open is taken: 70% on three days in a rolling "
    "seven, at least two non-consecutive.** Twelve days and nothing has contradicted the "
    "recommendation. **ADR-0047 then found what the model was missing**: `control.cell_instance` "
    "has no role, so the placement rule would put a new tenant on the archive server — by design "
    "the emptiest thing in the estate — and could not describe a burst environment at all, which "
    "has no trailing history to be measured on. `role: primary \\| archive \\| burst`, and only "
    "`primary` is placed onto. | [ADR-0042](../adr/0042-when-a-region-grows-and-where-a-tenant-lands.md), "
    "[ADR-0047](../adr/0047-how-long-data-is-kept-and-where-it-goes-next.md) |\n"
)

# Text appended to the Issue cell of a row that stays open.
NARROW = {
    "CF-64": (
        " **Narrowed 20 September to the RPO floor alone, by "
        "[ADR-0047](../adr/0047-how-long-data-is-kept-and-where-it-goes-next.md).** Retention is "
        "decided: three stages — active, archived, erased — with a base of **five years from "
        "last activity, not from creation**, because retention measured from creation deletes "
        "the most loyal guests on a schedule and does it invisibly until year six. The default "
        "is floor-aware or it is illegal: 4.3.4's ten years and 6.1.78's seven override upward "
        "and cannot be configured below, and a ceiling exists because keeping personal data "
        "because nobody chose a number is its own breach. **What remains is one number and it is "
        "Dinesh's**: the tightest RPO any tenant may ever buy, since near-zero requires "
        "synchronous replication and a second site. Recommendation is to tie it to ADR-0042's "
        "pin, so one decision serves this and CF-168."),
    "CF-165": (
        " **Decided 20 September by "
        "[ADR-0047](../adr/0047-how-long-data-is-kept-and-where-it-goes-next.md) and not yet "
        "built**, which is why it stays open — the rule CF-135 set is decided *and* built. The "
        "archive is a separate instance rather than a tablespace, so archived personal data is "
        "not one query mistake from an operational read. **Derived stores purge at archive, not "
        "at erasure**: a knowledge base still answering from an archived profile is an archive "
        "that did not happen, and nothing cascades between Postgres and Qdrant. Five contract "
        "changes are named and ordered; `pii.subject` already carries `is_erased`, `erased_at` "
        "and `erasure_request_id`, so erasure is already a tombstone — **but no erase operation "
        "exists**, and `ai.yaml` names `pii.erase_subject` as the erasure path."),
    "CF-162": (
        " **Narrowed 20 September to the reconciliation path, which still has no design.** The "
        "environment's shape is settled by "
        "[ADR-0047](../adr/0047-how-long-data-is-kept-and-where-it-goes-next.md): a burst "
        "environment is a pinned `control.cell_instance` with `role: burst`, no `cell_tenant` of "
        "its own and a read-only catalogue replica. **It is never placed onto and never enters "
        "another instance's placement metric** — a flash sale that joined the trailing average "
        "would poison a region's placement for a week after it ended. Its data retention is "
        "`reconciled + 30 days` rather than a lifetime, so it is auditable like every other "
        "retention in the package."),
    "CF-170": (
        " **Narrowed 20 September from seventeen screens to sixteen, by re-testing all of them "
        "against the current screen definitions.** **Class D is confirmed a false positive and "
        "is withdrawn**: `ADM-029 Deployment Monitor` declares twelve operations including "
        "`startRollout`, `pauseRollout` and `rollbackRollout`, and is a real deployment actor "
        "the rule caught only because rollout control is not named `publish*`. **Class B is "
        "confirmed still broken** — `BO-293`, `BO-353`, `ADM-247`, `CMS-030` and `CMS-050` each "
        "still declare exactly one operation and it is an `approve*`, so somebody signs off and "
        "the thing they signed off cannot go live. Five need contract work; the eleven of "
        "Class A need a title-or-operation decision, not an operation each."),
    "CF-171": (
        " **Re-measured 20 September: 577 of 2,056 operations, 28%** — the figures above are 577 "
        "of 1,626 and 35%. **The absolute number has not moved by one, and all 577 still have a "
        "`summary` that is verbatim the title of a screen in their own "
        "`x-ticvai-consumed-by`.** It reads better only because the denominator grew by 430 "
        "operations that were specified properly. **A measurement that drifts in our own favour "
        "is the one nobody re-runs**, which is the whole argument of this row restated against "
        "itself. Concentrated in `access` (146), `catalogue` (108), `promotions` (96), "
        "`orders` (89), `marketing-crm` (68), `subscription` (50) and `approvals` (20)."),
}

BL110_WHAT = (
    "Attribute-based access control, walked requirement by requirement on 20 September: **17 of "
    "the 48 are already served, 14 are a condition on an existing `Grant`, 11 are a screen or a "
    "report, and 6 are new** — of which 5 are live venue state belonging at the gate rather than "
    "in `identity`. The one real authorisation gap is segregation of duties."
)
BL110_WHY = (
    "\n\n**Narrowed 20 September — see "
    "[the walk](../../docs/active/bl-110-abac-walk-20-september.md).** Its 43 traceability rows "
    "carry **one note repeated forty times**, which is a verdict stamped across a section rather "
    "than forty-eight judgements. It is not wrong; it is just not an answer to *how much of this "
    "must be built*.\n\n"
    "**Eleven of the seventeen already-served requirements are the scope tree and the audit "
    "tables** — location, venue, tenant, inheritance, least privilege, caching and offline "
    "evaluation — which is the whole reason the role-based model was chosen deliberately. Plus "
    "`identity.delegated_access`, the `approvals` contract and `identity.authz_audit`.\n\n"
    "**Every attribute the fourteen conditions name already exists as a modelled thing**: shifts "
    "in `workforce`, tiers in `membership`, profiles in `accreditation`, segments in "
    "`marketing`, classifications in `catalogue`. They need referencing from a grant condition, "
    "not inventing.\n\n"
    "**Capacity and occupancy are not permissions.** They are live venue state and they belong "
    "in `access`, at the gate, where the state already is — treating *\"the park is full\"* as an "
    "authorisation decision is what would force a policy engine onto the hot path of all 2,056 "
    "operations and reverse `Session.scope`'s stated design.\n\n"
    "**One question for the client before any of it**: 3.3.27 asks for *\"real-time "
    "authorization\"*. Read literally it contradicts resolving permissions once at login; read "
    "as *\"a revoked permission takes effect promptly\"* it is session invalidation, which "
    "`forceLogout` already answers. One sentence, and it decides whether the hot path changes."
)


def cut_row(lines, cf):
    for i, ln in enumerate(lines):
        if ln.startswith("| **%s**" % cf):
            return i, lines.pop(i)
    return None, None


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(REG, encoding="utf-8").read()

    if "**Closed 20 September.** All four exist" in s:
        print("  already applied")
        return 0

    lines = s.split("\n")
    lines = [l + "\n" for l in lines[:-1]] + [lines[-1]]

    for cf in ("CF-166", "CF-168"):
        i, row = cut_row(lines, cf)
        if i is None:
            print("  !! %s row not found" % cf)
            return 1
        print("    %s  lifted from the open section (line %d)" % (cf, i + 1))

    j = "".join(lines).find(CLOSED_SECTION)
    if j < 0:
        print("  !! closed section header not found")
        return 1
    s = "".join(lines)
    s = s[:j + len(CLOSED_SECTION)] + CF166_ROW + CF168_ROW + s[j + len(CLOSED_SECTION):]
    print("    CF-166, CF-168 -> Closed / By research or architecture")

    # Rows that stay open gain their narrowing before the owner column.
    for cf, text in NARROW.items():
        m = re.search(r"^\| \*\*%s\*\* \|.*$" % cf, s, re.M)
        if not m:
            print("  !! %s row not found" % cf)
            return 1
        row = m.group(0)
        k = row.rfind(" | ", 0, row.rfind(" | "))     # before ` | owner | date |`
        if k < 0:
            print("  !! %s row has no owner column" % cf)
            return 1
        s = s[:m.start()] + row[:k] + text + row[k:] + s[m.end():]
        print("    %s  narrowed in place" % cf)

    B = json.load(io.open(BACKLOG, encoding="utf-8"))
    e = next(x for x in B["entries"] if x["id"] == "BL-110")
    e["narrowed"] = "2026-09-20"
    e["whatBefore"] = e["what"]
    e["what"] = BL110_WHAT
    e["why"] = (e.get("why") or "") + BL110_WHY
    print("    BL-110  narrowed, stays open")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(REG, "w", encoding="utf-8", newline="\n").write(s)
    io.open(BACKLOG, "w", encoding="utf-8", newline="\n").write(
        json.dumps(B, indent=1, ensure_ascii=False))
    print("  -> docs/registers/conflicts.md, handoff/contract-backlog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
