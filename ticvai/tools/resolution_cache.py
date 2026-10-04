#!/usr/bin/env python3
"""Which `cache:resolution` entry an operation fills or evicts (4 October 2026, CHG-FXC-001, root class R141).

**The lineage named the store and never the key.** 68 operations read or wrote `cache:resolution`, and the
service documents said, correctly, that "which resolution entry each writer evicts or bumps ... is not recorded
for any operation, so a writer here cannot yet be implemented from the package alone". The Sprint 1-2 judging
of 4 October found that sentence blocking 18 tickets (setRefundPolicy, setNavigation, restoreConfigVersion,
setApiLicensing, setTaxInvoiceTemplate, setPrices, publishVenueMap ...).

**The rule, one for every operation:**

* An entry is keyed `res:{tenantId}:{resolver}:{scopePath}`: the tenant, what is being resolved, and the scope
  node it was resolved for. Its value carries the resolver's `version` at the time it was built.
* A **resolver** is what gets resolved, named after the configuration it is built from: `permissions` (identity
  roles, grants, delegated access and the scope tree), `tenant-config` (white-label configuration and published
  content), `price-list` (price lists and prices), and otherwise the table the configuration lives in
  (`orders.refund_policy`, `platform.region_settings` ...).
* A **reader** (a GET that writes the store) fills the entry on a miss, and serves it stale while it re-resolves
  when its `version` is behind (ADR-0032, stale-while-revalidate).
* A **writer** bumps `resver:{tenantId}:{resolver}` (`INCR`) once its transaction commits, for every resolver whose
  tables it wrote. **Every scope in the tenant is affected**, ancestors and descendants alike: a configuration row at
  a region is inherited by every venue under it, and the bump is one counter per resolver, so no writer enumerates
  child scopes and no child scope is missed. Configuration changes are rare, so the cost is a re-resolution per
  scope on the next read.

The lineage entry records it as `cache`:

    "cache": {"store": "cache:resolution", "role": "evicts" | "fills", "resolvers": [...],
              "key": "res:{tenantId}:{resolver}:{scopePath}", "bump": "INCR resver:{tenantId}:{resolver}",
              "affects": "every scope in the tenant"}

`derive-lineage.py` writes it for a new operation and fills it where it is missing; `check-write-lineage.py`
(W-CACHEKEY) fails an operation that touches the store without it; `derive-diagrams.py` prints it per operation.
"""
from __future__ import annotations

STORE = "cache:resolution"
KEY = "res:{tenantId}:{resolver}:{scopePath}"
BUMP = "INCR resver:{tenantId}:{resolver}"
AFFECTS = ("every scope in the tenant: the bump is one counter per resolver, so the scope written, its "
           "ancestors and every descendant that inherits from it re-resolve on their next read")

# Tables that are bookkeeping around a write, never what a resolver is built from.
_NOT_CONFIG = {"platform.audit_record", "platform.outbox"}

# Grouped resolvers: one entry answers a question built from several tables.
_GROUPS = (
    ("permissions", lambda t: t.startswith("identity.") or t == "platform.scope"),
    ("tenant-config", lambda t: t.startswith("whitelabel.") or t in (
        "control.content_block", "control.seo_metadata", "control.url_redirect")),
    ("price-list", lambda t: t in ("catalogue.price_list", "catalogue.price")),
    ("venue-map", lambda t: t.startswith("venuemap.")),
    ("menu", lambda t: t.startswith("fnb.menu") or t == "catalogue.product_version"),
    ("table-layout", lambda t: t in ("fnb.dining_table", "fnb.table_combination")),
)

# Operations whose resolver is not told by a table they write: they resolve, they do not configure, so they fill
# the entry whatever their verb (resolvePermissions is a POST that computes).
_BY_OPERATION = {
    "resolvePermissions": ["permissions"],
    "getCurrentSession": ["permissions"],
}


def _fold(names: set) -> list:
    """A child table folds into its parent's resolver: `orders.refund_policy_time_band` is part of the refund
    policy, `marketing.consent_purpose_channel` of the consent purposes."""
    return sorted(n for n in names if not any(n != m and n.startswith(m + "_") for m in names))


def resolver_of(table: str) -> str | None:
    """The resolver a configuration table feeds, or None for a store or bookkeeping table."""
    if ":" in table or table in _NOT_CONFIG:
        return None
    for name, test in _GROUPS:
        if test(table):
            return name
    return table


def _strip(path: str) -> str:
    return (path or "").rstrip("/")


def resolution_cache(op_id: str, entry: dict, lineage: dict) -> dict | None:
    """The `cache` record for one lineage entry, or None when it does not touch `cache:resolution`."""
    if STORE not in (entry.get("writes") or []) and STORE not in (entry.get("reads") or []):
        return None
    verb = (entry.get("verb") or "").upper()
    role = "fills" if verb == "GET" or op_id in _BY_OPERATION else "evicts"
    res = list(_BY_OPERATION.get(op_id) or [])
    if not res and role == "evicts":
        res = _fold({r for t in entry.get("writes") or [] if (r := resolver_of(t))})
    if not res and role == "fills":
        # A reader resolves what the writer on the same resource configures: getTheme <- setTheme, listPrices <-
        # setPrices, getVenueMapGraph <- publishVenueMap (an action path is its resource plus a verb).
        mine = _strip(entry.get("path"))
        for o, e in lineage.items():
            if o == op_id or (e.get("verb") or "").upper() == "GET" or STORE not in (e.get("writes") or []):
                continue
            p = _strip(e.get("path"))
            if p == mine or p.rsplit("/", 1)[0] == mine or mine.startswith(p + "/"):
                res += [r for t in e.get("writes") or [] if (r := resolver_of(t))]
        res = _fold(set(res))
    if not res:
        res = _fold({r for t in entry.get("reads") or [] if (r := resolver_of(t))})
    return {
        "store": STORE,
        "role": role,
        "resolvers": res,
        "key": KEY,
        "bump": BUMP if role == "evicts" else None,
        "affects": AFFECTS if role == "evicts" else None,
    }
