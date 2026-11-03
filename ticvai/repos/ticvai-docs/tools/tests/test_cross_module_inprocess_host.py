"""Tests for XR-INPROCESS-HOST and XR-SERVICE-PATH in tools/check-cross-module-reads.py, and the generator rule in
tools/contract_shapes.py read_route (r13, 2 November 2026; ADAM CR-438, CR-475 to CR-478; CHG-R13INP-001,
CHG-CR438-001).

    python -m pytest ticvai/tools/tests/test_cross_module_inprocess_host.py -q

The synthetic tests give the rules a few grants and operations; the last ones read the real package.
"""
import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
_spec = importlib.util.spec_from_file_location("xr", TOOLS / "check-cross-module-reads.py")
xr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(xr)
import contract_shapes as CS  # noqa: E402

GRANTS = [
    {"id": "XDR-010", "reader": "access", "queries": ["identity#subjectRecords"],
     "operations": ["listDeviceBindingSession"], "narrow": True},
    {"id": "XDR-051", "reader": "operations", "queries": ["catalogue#productRecords"], "operations": ["x"]},
    {"id": "XDR-075", "reader": "operations", "queries": ["orders#paymentRecords"], "composes": "OrderService"},
]


def why(o, rdep, owner, odep, key, consumer=False):
    return xr.asked_in_process_by_host(o, rdep, owner, odep, key, consumer, xr.granted_reads(GRANTS),
                                       xr.narrow_reads(GRANTS), xr.composed_modules(GRANTS))


def test_same_deployable_granted_composed_and_consumer_are_in_process():
    assert why("openShift", "commerce", "TenancyService", "commerce", "tenancy#deviceRecords")
    assert why("diffConfigVersion", "operations", "CatalogueService", "commerce", "catalogue#productRecords")
    assert "composes OrderService" in why("listX", "operations", "OrderService", "commerce", "orders#refundRecords")
    assert why("onPaid", "operations", "LedgerService", "commerce", "finance#journalRecords", consumer=True)


def test_a_narrow_grant_is_its_own_operations_only():
    assert why("listDeviceBindingSession", "access", "IdentityService", "commerce", "identity#subjectRecords")
    assert why("enrolFacePass", "access", "IdentityService", "commerce", "identity#subjectRecords") is None


def test_a_module_no_host_composes_stays_on_the_service_route():
    assert why("listX", "operations", "IdentityService", "commerce", "identity#principalRecords") is None
    assert why("listX", "ticvai-ai", "TenancyService", "commerce", "tenancy#venueSettingsRecords") is None


def test_the_control_plane_is_not_a_cell_host():
    assert xr.control_plane({"writes": ["control.tenant_migration_plan"]}, {})
    assert xr.control_plane({}, {"x-ticvai-scope-level": "platform"})
    assert not xr.control_plane({"reads": ["subscription.membership_product"]}, {"x-ticvai-scope-level": "tenant"})


def test_kebab_names_the_path():
    assert xr.kebab("subjectBiometricRecords") == "subject-biometric-records"
    assert xr.camel("subject-biometric-records") == "subjectBiometricRecords"


def _op(path, method, body, ok, extra=None):
    op = {"operationId": "listThing", "description": "**The `service` route of the `thingRecords` query**",
          "security": [{"serviceAuth": []}],
          "requestBody": {"content": {"application/json": {"schema": {"type": "object", "properties": body}}}},
          "responses": {"200": {"content": {"application/json": {"schema": {"type": ok}}}},
                        "400": {"$ref": "../shared/common.yaml#/components/responses/BadRequest"}, "401": {}}}
    op.update(extra or {})
    return {"listThing": {"contract": "things", "path": path, "method": method, "op": op}}


QUERIES = {"things#thingRecords": ("things", {"inputs": {"ids": {}, "where": {}}, "returns": {"type": "array"},
                                              "served": ["in-process", "service"]})}


def test_a_service_route_built_to_cr438_passes():
    assert xr.service_path_findings(_op("/queries/thing-records", "post", {"ids": {}, "where": {}}, "array"),
                                    QUERIES, {}) == []


def test_a_get_or_another_path_or_body_fails():
    got = xr.service_path_findings(_op("/internal/things", "get", {}, "array"), QUERIES, {})
    assert len(got) == 1 and "not POST /queries/thing-records" in got[0][1] and "declared inputs" in got[0][1]
    got = xr.service_path_findings(_op("/queries/thing-records", "post", {"ids": {}, "where": {}}, "object"),
                                   QUERIES, {})
    assert "JSON array" in got[0][1]


def test_the_package_has_no_service_read_a_host_asks_in_process():
    # the real package: the class is re-routed (CHG-R13INP-001) and subjectBiometricRecords is at its CR-438 path
    assert xr.main() == 0


def test_the_generator_writes_in_process_for_a_composed_module_and_never_a_narrow_grant():
    assert CS.read_route("operations", "commerce", "orders#salesOrderRecords") == "in-process"
    assert CS.read_route("access", "commerce", "catalogue#productRecords") == "in-process"
    assert CS.read_route("access", "commerce", "identity#subjectRecords") == "service"
    assert CS.read_route("operations", "commerce", "identity#principalRecords") == "service"
