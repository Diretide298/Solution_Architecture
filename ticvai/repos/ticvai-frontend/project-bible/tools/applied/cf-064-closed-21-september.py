#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close CF-64, and hand its unbuilt half to CF-165 rather than tracking it twice.

**CF-64 asked two questions and both are now answered.** Retention was decided 20 September by
ADR-0047 — three stages, five years from last activity, floor-aware. The RPO floor was decided
21 September: asynchronous several-minute as the default, synchronous near-zero selectable on a
pinned instance, and `ReplicationMode` is in `subscription.yaml` as of the same morning.

**What remains is contract work, and CF-165 already names it.** ADR-0047 lists six items in order;
two are done (`cell_instance.role`, and `ai.yaml`'s dangling `pii.erase_subject` citation). The
other four sit under CF-165, whose row says in its own words that it stays open because *"the rule
CF-135 set is decided **and** built"*.

**Leaving CF-64 open to carry the same four items would be the pattern this package found twice
yesterday** — BL-155 blocked on a conflict about scheduling workshops, BL-161 blocked on a
conflict about retention. **One conflict per question**, and a second row shadowing the first is
how a blocker goes stale without anybody noticing.

    python3 tools/applied/cf-064-closed-21-september.py --apply
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "docs", "registers", "conflicts.md")

CLOSED_HEAD = ("### By client decision\n\n"
               "| ID | Issue | Closed by | ADR |\n|---|---|---|---|\n")

ISSUE = (
    "**89 retention requirements against two stated periods, and an RPO floor nobody had set.** "
    "Only 4.3.4 (10 years, payment) and 6.1.78 (7 years) named a period; the other 87 said "
    "\"configurable\", which asks the platform to let somebody set a number rather than to pick "
    "one. **Refined 17 Aug by CF-60's count of the DR sheet** — 62 of its requirements are "
    "infrastructure and only RPO and RTO sit in the platform at all."
)

CLOSED_BY = (
    "**Closed 21 September, in two halves decided a day apart.**\n\n"
    "**Retention, 20 September.** Three stages — active, archived, erased — with a base of **five "
    "years from last activity, not from creation**, because retention measured from creation "
    "deletes the most loyal guests on a schedule and does it invisibly until year six. **The "
    "default is floor-aware or it is illegal**: 4.3.4's ten years and 6.1.78's seven override "
    "upward and cannot be configured below, and a ceiling exists because keeping personal data "
    "because nobody chose a number is its own breach. The archive is a separate instance rather "
    "than a tablespace, so archived personal data is not one query mistake from an operational "
    "read.\n\n"
    "**The RPO floor, 21 September — and the recommendation was taken.** `asynchronous` with a "
    "several-minute recovery point is **the default and what every tenant gets**; `synchronous` "
    "with a near-zero point is **selectable**, because DR-11 asks the platform to *support "
    "configurable* objectives and a platform offering exactly one would have answered a different "
    "requirement. **A floor nobody can rise above is not a floor.**\n\n"
    "**`synchronous` requires `pinnedInstance`, and that precondition was not invented for this "
    "decision.** Synchronous replication puts a network round-trip inside every write "
    "transaction; on a shared instance that cost is paid by every tenant on the host, and it "
    "lands on the two paths with the least headroom in the package — `acquireInventoryHold`, "
    "which already serialises on contention, and `access.scan_event`, which runs tens of "
    "thousands of times a day at a gate. ADR-0042 already holds that the pin is what a dedicated "
    "client is buying, and a dedicated client is exactly who asks for near-zero. **One decision "
    "served this and CF-168.** `CellInstance.supportsSynchronousReplication` is the topology fact "
    "underneath: a capability absent is a capability unavailable, not one assumed.\n\n"
    "**RTO is deliberately not modelled.** DR-12 asks for it configurably too, but an RTO is a "
    "promise about how fast an operator restores rather than a property a row can carry — it "
    "belongs in the SOW beside the runbook, and a column claiming it would be a column nothing "
    "enforces.\n\n"
    "**The remaining contract work is CF-165's and is not duplicated here.** ADR-0047 lists six "
    "items; `control.cell_instance.role` and `ai.yaml`'s dangling `pii.erase_subject` citation "
    "are done, and the other four sit under CF-165, which stays open because **decided is not "
    "built.** A second row shadowing the same four items is how a blocker goes stale — this "
    "package found two such blockers yesterday, and will not add a third."
)

ADR_CELL = ("[ADR-0047](../adr/0047-how-long-data-is-kept-and-where-it-goes-next.md), "
            "[ADR-0042](../adr/0042-when-a-region-grows-and-where-a-tenant-lands.md)")

NEW_ROW = "| **CF-64** | %s | %s | %s |\n" % (ISSUE, CLOSED_BY, ADR_CELL)


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(REG, encoding="utf-8").read()

    if "**Closed 21 September, in two halves decided a day apart.**" in s:
        print("  already applied")
        return 0

    lines = s.split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith("| **CF-64** |")]
    if len(hits) != 1:
        print("  !! CF-64 appears on %d lines" % len(hits))
        return 1
    i = hits[0]
    old = lines[i]
    owner = old.rstrip().rstrip("|").rsplit("|", 2)
    print("    CF-64 found at line %d · %d chars · owner/raised%s"
          % (i + 1, len(old), "".join(owner[-2:])))
    del lines[i]
    s = "\n".join(lines)

    if s.count(CLOSED_HEAD) != 1:
        print("  !! closed-table header matched %d times" % s.count(CLOSED_HEAD))
        return 1
    s = s.replace(CLOSED_HEAD, CLOSED_HEAD + NEW_ROW, 1)
    print("    moved to Closed · %d chars of closure text" % len(CLOSED_BY))

    if s.count("| **CF-64** |") != 1:
        print("  !! CF-64 now appears %d times" % s.count("| **CF-64** |"))
        return 1
    if "| **CF-165** |" not in s:
        print("  !! CF-165 is not in the register — the handed-off work has no home")
        return 1
    print("    CF-165 still present and still open — the four unbuilt items have a home")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(REG, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> docs/registers/conflicts.md")
    print("\n  Now run tools/build-cf-index.py to regenerate conflict-status.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
