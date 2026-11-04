"""Tests for check-contract-shapes' access rules of the r13 system review (lane h of r14): C-GUEST-OWNER and the owned
half of C-SELF-404 (C-03, CHG-R14H-003), C-SECRET-PARAM (C-13, CHG-R14H-005).

    python -m pytest ticvai/tools/tests/test_check_contract_shapes_access.py -q
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("cs", TOOLS / "check-contract-shapes.py")
cs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cs)


def rules(found):
    return sorted(r for r, _k, _m in found)


def test_a_guest_object_with_no_owner_fails():
    # the r13 getEntitlementCredential: a guest names an entitlement id, nothing says whose
    op = {"x-ticvai-audience": ["staff", "guest"], "x-ticvai-guest-callable": True}
    assert rules(cs.guest_owner_problems("getEntitlementCredential", op, "/entitlements/{entitlementId}/credential",
                                         {"200", "429"})) == ["C-GUEST-OWNER"]


def test_an_owned_object_needs_the_shared_404():
    op = {"x-ticvai-audience": ["guest"], "x-ticvai-object-owner": ["subject", "share"]}
    assert rules(cs.guest_owner_problems("x", op, "/entitlements/{entitlementId}", {"200"})) == ["C-SELF-404"]
    assert rules(cs.guest_owner_problems("x", op, "/entitlements/{entitlementId}", {"200", "404"})) == []


def test_published_session_and_bearer_ids_are_nobodys():
    op = {"x-ticvai-audience": ["guest", "anonymous"]}
    for path in ("/venues/{venueId}/outlets", "/carts/{cartId}/lines/{lineId}", "/payment-links/{token}",
                 "/performances/{performanceId}"):
        assert rules(cs.guest_owner_problems("x", op, path, {"200"})) == [], path


def test_an_owner_outside_the_vocabulary_fails():
    op = {"x-ticvai-audience": ["guest"], "x-ticvai-object-owner": ["household"]}
    assert rules(cs.guest_owner_problems("x", op, "/wallets/{walletId}", {"200", "404"})) == ["C-GUEST-OWNER"]


def test_a_credential_in_the_path_or_a_header_is_marked():
    plain = [{"name": "token", "in": "path"}, {"name": "X-Supervisor-Pin", "in": "header"},
             {"name": "Idempotency-Key", "in": "header"}, {"name": "venueId", "in": "path"}]
    assert rules(cs.secret_param_problems("x", plain, "/payment-links/{token}")) == ["C-SECRET-PARAM"] * 2
    marked = [{"name": "token", "in": "path", "x-ticvai-secret": "bearer"},
              {"name": "X-Supervisor-Pin", "in": "header", "x-ticvai-secret": "bearer"}]
    assert rules(cs.secret_param_problems("x", marked, "/payment-links/{token}")) == []
    assert rules(cs.secret_param_problems("x", [{"name": "t", "in": "query", "x-ticvai-secret": "bearer"}], "")) \
        == ["C-SECRET-PARAM"]
