"""The address logic on its own, with no service and no store.

Here rather than in ip-check.mjs because the two things most worth proving
cannot be reached over a socket from a harness:

  **An untrusted peer's X-Real-IP is discarded.** The harness talks to the
  service over loopback, and loopback is trusted, so every request it can make
  takes the believing branch. The branch that matters — somebody reaching the
  service directly and claiming to be in the office — is unreachable from there
  and is the whole security argument for the feature.

  **A rule and an address of different families do not raise.** `10.0.0.1 in
  2001:db8::/32` is a TypeError, not a False, and one IPv6 rule in the table
  would otherwise take the middleware down on every request.

Run:  python -m api.netaddr_check   — or simply  python api/netaddr-check.py
"""

import os
import sys
from pathlib import Path

# Importable whether this is run as a module or as a file.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("TICVAI_TRUSTED_PROXIES", "127.0.0.1,::1")

from api import netaddr as n  # noqa: E402

CASES = [
    # ── one spelling per address ─────────────────────────────────────
    ("an IPv4-mapped v6 address folds to the v4 one",
     n.normalise("::ffff:203.0.113.7"), "203.0.113.7"),
    ("a bracketed v6 address is still an address",
     n.normalise("[2001:db8::1]"), "2001:db8::1"),
    ("and something that is not an address is not one",
     n.normalise("not-an-ip"), None),

    # ── one shape per rule ───────────────────────────────────────────
    ("a bare address is stored as a single-address network",
     n.as_network("203.0.113.7"), "203.0.113.7/32"),
    ("host bits below the prefix are dropped, not refused",
     n.as_network("10.0.0.5/24"), "10.0.0.0/24"),
    ("a v6 network survives intact",
     n.as_network("2001:db8::/32"), "2001:db8::/32"),
    ("and a label is not a network", n.as_network("the office"), None),

    # ── matching ─────────────────────────────────────────────────────
    ("an address matches its own /32", n.covers(["203.0.113.7/32"], "203.0.113.7"), True),
    ("and anything inside a range", n.covers(["10.0.0.0/24"], "10.0.0.99"), True),
    ("but not one outside it", n.covers(["10.0.0.0/24"], "10.0.1.1"), False),
    ("a v6 rule against a v4 address answers no rather than raising",
     n.covers(["2001:db8::/32"], "10.0.0.1"), False),
    ("a rule that no longer parses is skipped, not fatal",
     n.covers(["nonsense", "10.0.0.0/24"], "10.0.0.5"), True),
    ("nothing covers an address that is not one", n.covers(["0.0.0.0/0"], "nonsense"), False),

    # ── whom to believe ──────────────────────────────────────────────
    #
    # The four lines the feature stands on.
    ("somebody talking to the service directly keeps their own address, "
     "whatever they claim",
     n.client_ip("198.51.100.9", "203.0.113.7"), "198.51.100.9"),
    ("and cannot get in by claiming an allowed one through X-Forwarded-For",
     n.client_ip("198.51.100.9", "", "10.0.0.5"), "198.51.100.9"),
    ("a proxy we put there is believed",
     n.client_ip("127.0.0.1", "203.0.113.7"), "203.0.113.7"),
    ("X-Real-IP wins over the forwarded list, which the client contributes to",
     n.client_ip("127.0.0.1", "203.0.113.7", "10.0.0.1"), "203.0.113.7"),
    ("the forwarded list is read only in its absence, and from the left",
     n.client_ip("127.0.0.1", "", "203.0.113.9, 10.0.0.1"), "203.0.113.9"),
    ("a trusted proxy that forwarded nothing answers as itself, which will not "
     "match an office rule and so shows up in the dry run",
     n.client_ip("127.0.0.1"), "127.0.0.1"),
    ("and no peer is no answer, never a value to match rules against",
     n.client_ip(""), ""),
]


def main() -> int:
    bad = 0
    for name, got, want in CASES:
        ok = got == want
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}"
              + ("" if ok else f" — got {got!r}, wanted {want!r}"))
    print(f"\n{len(CASES) - bad} passed, {bad} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
