"""Which address a request actually came from, and whether a rule covers it.

Separated from main.py because this is the part that is easy to get wrong and
worth testing on its own: every function here is pure, takes strings, and never
touches the store or a request object.

**The hard problem is not matching addresses, it is believing them.** A request
arriving at this service has travelled nginx → the Node viewer → here, and each
hop can only report what the previous one told it. `X-Real-IP` is a header like
any other: a client that sends its own is lying, and a service that reads it
without asking who handed it over is a service whose allowlist can be walked
past by adding one line to a curl command.

So the rule is: **a forwarded address is believed only when the machine that
handed it over is one we put there.** The immediate peer — `request.client.host`,
which is a TCP fact and not a header — decides. If the peer is a trusted proxy,
`X-Real-IP` is the answer; if it is anybody else, the peer *is* the answer and
whatever they claimed about themselves is discarded.

That makes TICVAI_TRUSTED_PROXIES the security boundary of the whole feature,
which is why it defaults to loopback and nothing else. Loopback is safe to trust
because a process on the machine could talk to the database directly anyway.
"""

from __future__ import annotations

import ipaddress
import os
from typing import Optional

# The machines whose word about the caller we take. nginx and the Node viewer
# both sit on loopback in the deployment, so the default needs no configuration;
# TICVAI_TRUSTED_PROXIES exists for an arrangement where they do not, and it
# takes addresses or networks in the same notation as a rule.
#
# **Widening this is the one change here that can be a mistake.** A proxy named
# in this list can claim any address it likes for any request and be believed,
# so an entry that is not actually a proxy under our control is a way through
# the allowlist rather than an inconvenience.
_DEFAULT_TRUSTED = "127.0.0.1,::1"


def _networks(text: str) -> list:
    out = []
    for part in (text or "").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.append(ipaddress.ip_network(part, strict=False))
        except ValueError:
            # A typo in an environment variable must not stop the service
            # booting, and it must not silently widen trust either. Dropping the
            # entry does neither: the proxy it was meant to name is simply not
            # trusted, which fails towards refusing rather than towards
            # believing.
            continue
    return out


def trusted_proxies() -> list:
    return _networks(os.environ.get("TICVAI_TRUSTED_PROXIES", _DEFAULT_TRUSTED))


def normalise(value: str) -> Optional[str]:
    """One spelling of an address, or None if it is not one.

    IPv6 has many spellings of the same address and ::ffff:127.0.0.1 is IPv4
    wearing a hat — both are folded here, because two spellings of one address
    in the sightings table read as two places somebody has been.
    """
    text = (value or "").strip()
    if not text:
        return None
    # Uvicorn reports an IPv6 peer bare, but a header can carry the bracketed
    # form a URL would use, and ipaddress refuses those.
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    try:
        address = ipaddress.ip_address(text)
    except ValueError:
        return None
    mapped = getattr(address, "ipv4_mapped", None)
    return str(mapped or address)


def as_network(value: str) -> Optional[str]:
    """A rule, normalised to a network — or None if it is not one.

    A bare address becomes a single-address network, so the store holds one
    shape and the matcher has one branch. `strict=False` accepts 10.0.0.5/24 and
    keeps 10.0.0.0/24, which is what somebody who typed that meant rather than
    an error worth refusing them over.
    """
    text = (value or "").strip()
    if not text:
        return None
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    try:
        network = ipaddress.ip_network(text, strict=False)
    except ValueError:
        return None
    return str(network)


def covers(rules, ip: str) -> bool:
    """Whether any of these rules lets this address through.

    Rules are the stored strings. A rule that no longer parses — impossible
    through the API, possible if somebody edits the database by hand — is
    skipped rather than raised on, because a syntax error in one row must not
    turn into a lockout on every row.
    """
    address = normalise(ip)
    if address is None:
        return False
    here = ipaddress.ip_address(address)
    for rule in rules:
        try:
            network = ipaddress.ip_network(rule, strict=False)
        except (ValueError, TypeError):
            continue
        # An IPv4 address is never in an IPv6 network and the comparison raises
        # rather than answering False, which would take the middleware down on
        # the first mixed store.
        if network.version != here.version:
            continue
        if here in network:
            return True
    return False


def is_trusted_peer(peer: str) -> bool:
    address = normalise(peer)
    if address is None:
        return False
    here = ipaddress.ip_address(address)
    for network in trusted_proxies():
        if network.version == here.version and here in network:
            return True
    return False


def client_ip(peer: str, real_ip: str = "", forwarded_for: str = "") -> str:
    """The address to hold this request against.

    `peer` is the TCP fact. The two headers are claims, and they are read only
    when the peer is one of ours.

    When both headers are present, `X-Real-IP` wins. nginx sets it to the one
    address it is confident about; X-Forwarded-For is a list that the client
    contributes the first entry of, and picking from it correctly needs to know
    how many hops to skip — which is one more thing to configure and get wrong.
    The list is read only when X-Real-IP is absent, and then from the **left**,
    because in that case there is exactly one proxy and the client's claim is
    all that is in front of it.

    Returns "" when nothing here is an address, which the caller must treat as
    "unknown" rather than as a value to match rules against.
    """
    direct = normalise(peer)
    if direct is None:
        return ""
    if not is_trusted_peer(direct):
        # Somebody talking to this service directly. Whatever they said about
        # themselves is discarded — this is the branch the whole module is for.
        return direct
    claimed = normalise(real_ip)
    if claimed:
        return claimed
    for part in (forwarded_for or "").split(","):
        found = normalise(part)
        if found:
            return found
    # A trusted proxy that forwarded nothing. That is a misconfiguration rather
    # than an attack, and answering with the proxy's own address is honest about
    # what we know: it will not match an office rule, so it shows up in the dry
    # run as something to fix before arming.
    return direct
