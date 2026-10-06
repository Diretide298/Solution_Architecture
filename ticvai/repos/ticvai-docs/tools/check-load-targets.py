#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The client's sizing benchmarks are the package's load-acceptance targets, and no document tests below them.

**6 October 2026, CHG-R4-017.** The client's tracker answer T9 (sources/client/2026-10-06-tracker-answers.md) gave
the numbers the package had sized without: 1,000-2,000 concurrent B2C users the expected peak of a major event,
**3,000 the initial performance acceptance benchmark** (not a hard limit), **50,000+ simultaneous on-sale arrivals**
absorbed by the edge waiting room, and load tests for **both small-site and major-event scenarios**. The package
sized in RPS and tested the waiting room at 30,000 arrivals (ADR-0066 action item 4, the Bahrain figure); nothing held
a document to the client's figures once they existed.

**What fails:**

  L-TARGET-MISSING   a document that holds the acceptance targets does not state one of them (TARGETS below:
                     the block test strategy's load scenarios, the development plan's go-live load test, ADR-0066)
  L-TARGET-BELOW     a document in docs/adr or docs/active plans a waiting-room or on-sale load test at fewer
                     arrivals than the client's 50,000 ("load test at N arrivals"), unless the line says what it
                     was amended from ("was N")

Read-only. Exit 1 on any finding.

    python3 tools/check-load-targets.py
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "sources/client/2026-10-06-tracker-answers.md"
ARRIVALS = 50_000      # T9: "50,000+ simultaneous incoming visitors"
BENCHMARK = 3_000      # T9: "3,000 as the initial performance acceptance benchmark"

# (file, what it must state, pattern)
TARGETS = [
    ("docs/active/block-test-strategy.md", "a small-site load scenario", r"\*\*Small site\*\*"),
    ("docs/active/block-test-strategy.md", "a major-event load scenario", r"\*\*Major event"),
    ("docs/active/block-test-strategy.md", "the 3,000-concurrent B2C run", r"3,000 active concurrent B2C users"),
    ("docs/active/block-test-strategy.md", "a run above the benchmark (3,000 is not a limit)", r"\*\*Above the benchmark\*\*"),
    ("docs/active/block-test-strategy.md", "the 50,000-arrival waiting-room run", r"50,000 simultaneous arrivals"),
    ("docs/active/development-plan.md", "the go-live load test at 3,000 concurrent", r"Load test at .*3,000 concurrent"),
    ("docs/active/development-plan.md", "the go-live load test at 50,000 arrivals", r"Load test at .*50,000 simultaneous"),
    ("docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md",
     "the waiting-room load test at 50,000 arrivals", r"Load test at 50,000 simultaneous arrivals"),
]

BELOW = re.compile(r"[Ll]oad[- ]test(?:ed)? at ([\d,]+)(?: simultaneous)? arrivals")


def main() -> int:
    if not (ROOT / SOURCE).exists():
        print(f"check-load-targets: FAIL - the source {SOURCE} is missing")
        return 1
    bad = []
    for rel, what, pat in TARGETS:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8") if p.exists() else ""
        if not re.search(pat, text):
            bad.append(f"L-TARGET-MISSING  {rel} does not state {what} (the client's T9, {SOURCE})")
    for folder in ("docs/adr", "docs/active"):
        for p in sorted((ROOT / folder).glob("*.md")):
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                for m in BELOW.finditer(line):
                    if int(m.group(1).replace(",", "")) < ARRIVALS and not re.search(r"\bwas [\d,]+", line):
                        bad.append(f"L-TARGET-BELOW    {p.relative_to(ROOT).as_posix()}:{n} plans a load test at "
                                   f"{m.group(1)} arrivals; the client's figure is {ARRIVALS:,}+")
    print(f"check-load-targets: {len(TARGETS)} target statement(s); arrivals {ARRIVALS:,}+, "
          f"acceptance benchmark {BENCHMARK:,} concurrent")
    for b in bad:
        print(f"  FAIL {b}")
    if bad:
        print(f"FAIL - {len(bad)} finding(s)")
        return 1
    print("PASS - the client's sizing benchmarks are the load-acceptance targets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
