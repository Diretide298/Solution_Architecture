"""The delivery slice's setup rule: a writer that trades is never setup (tools/derive-delivery-slice.py is_setup).

    python -m pytest ticvai/tools/tests/test_delivery_slice_verbs.py -q
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("derive_delivery_slice", TOOLS / "derive-delivery-slice.py")
dds = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dds)


def test_answering_a_chargeback_is_trading_not_setup():
    # r8 gate residue, CHG-R8RES-004: respondToChargeback made ADM-634 a Block A setup screen (C-REACH)
    for op in ("respondToChargeback", "recordChargeback", "assignChargeback", "recordChargebackOutcome"):
        assert not dds.is_setup(op, {"perm": "ORDER_REFUND_APPROVE"}), op


def test_configuring_writers_stay_setup():
    for op in ("createCreditType", "setWalletTransferRules", "createProduct", "setFxRate"):
        assert dds.is_setup(op, {"perm": "WALLET_CONFIGURE"}), op
