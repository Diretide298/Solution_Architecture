"""Tests for XR-FACT and per-table coverage in tools/check-cross-module-reads.py (ADAM CR-096, CR-135; CHG-RTE-001).

    python -m pytest ticvai/tools/tests/test_cross_module_facts.py -q

The synthetic tests give the detectors a few lines of text; the last one reads the real package and checks that
every fact the two CRs named is found in its operation's text (true before and after the fix: the text stays).
"""
import importlib.util
import json
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
_spec = importlib.util.spec_from_file_location("xr", TOOLS / "check-cross-module-reads.py")
xr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(xr)

OWNER = {"platform": "TenancyService", "orders": "OrderService", "control": "PlatformService",
         "ledger": "LedgerService", "fnb": "FnbService", "promotions": "CatalogueService",
         "retail": "RetailService", "payments": "OrderService"}
TABLES = {"platform.region_settings", "platform.venue_settings", "platform.denomination", "platform.scope",
          "control.tenant_domain", "control.cell", "ledger.fx_rate", "fnb.delivery_location",
          "orders.ticket_template", "promotions.promotion", "retail.merchandise", "payments.provider"}


def named(text, reader="RetailService"):
    return xr.facts_named(text, reader, OWNER, TABLES)


def test_a_phrase_of_the_vocabulary_names_the_owners_table():
    got = named("**Read in the region's time zone**: daysOfWeek are the region's calendar days", "CatalogueService")
    assert set(got) == {"platform.region_settings"}
    assert got["platform.region_settings"][0][0] == "fact"


def test_a_table_name_in_the_text_is_a_fact():
    got = named("409 collectionPointClosed when `fnb.delivery_location` is closed")
    assert got["fnb.delivery_location"][0][0] == "table"


def test_the_readers_own_module_is_not_a_cross_read():
    assert named("Returns price after any live promotion", "CatalogueService") == {}


def test_an_unknown_schema_or_table_is_ignored():
    assert named("reads `nosuch.table` and `kernel.thing`") == {}


def test_a_kernel_table_by_name_is_not_a_fact_but_active_venues_is():
    assert named("written to platform.scope") == {}
    assert set(named("a venueId not among the tenant's active venues", "WhiteLabelService")) == {"platform.scope"}


def test_coverage_is_per_table():
    queries = {"tenancy#workstationRecords": ("TenancyService", {"platform.workstation"}),
               "catalogue#variantsSellableAt": ("CatalogueService", set())}
    tables, owners = xr.covered_by([{"query": "tenancy#workstationRecords"},
                                    {"query": "catalogue#variantsSellableAt"}], queries)
    assert tables == {"platform.workstation"} and owners == {"CatalogueService"}
    assert not xr.is_covered("platform.denomination", "TenancyService", tables, owners)   # the CR-135 shape
    assert xr.is_covered("platform.workstation", "TenancyService", tables, owners)
    assert xr.is_covered("catalogue.product", "CatalogueService", tables, owners)         # a rule query, no table


def test_a_query_covers_its_table_its_projection_source_and_its_reads():
    q = {"table": "a.b", "projection": {"source": "c.d + e.f"}, "reads": ["g.h"]}
    assert xr.query_tables(q) == {"a.b", "c.d", "e.f", "g.h"}


def test_the_facts_the_crs_named_are_found_in_their_operations_text():
    import audit_guard as g   # importable: the check put tools/ on sys.path
    dec = json.loads((ROOT / "handoff" / "service-decomposition.json").read_text(encoding="utf-8"))["services"]
    owner_of_schema = {sc: s for s, v in dec.items() for sc in v.get("schemas") or []}
    svc_of_contract = {c: s for s, v in dec.items() for c in v.get("contracts") or []}
    tables = set(json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8"))["cols"])
    by, names = g.schemas()
    persist = xr.persisted(by, tables)
    ops = g.operations()
    missed = []
    for op, table in sorted(xr.MUST_FIX_FACTS):
        f = ops[op]
        reader = svc_of_contract[f["contract"]]
        text = xr.op_text(f["contract"], f["op"], f["item"], by)
        if table not in xr.facts_named(text, reader, owner_of_schema, tables, persist, names, svc_of_contract):
            missed.append((op, table))
    assert missed == []
