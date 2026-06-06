from dataclasses import replace
from decimal import Decimal

from crypto_ledger_tools import calculate_average_cost, load_transactions


def test_calculate_average_cost_from_sample():
    transactions = load_transactions("examples/sample_transactions.csv")

    summaries = calculate_average_cost(transactions)

    coin = summaries["COIN"]
    assert coin.acquired_quantity == Decimal("3.0")
    assert coin.disposed_quantity == Decimal("1.5")
    assert coin.remaining_quantity == Decimal("1.5")
    assert coin.realized_pnl == Decimal("48.300")


def test_calculate_average_cost_rejects_oversell():
    transactions = load_transactions("examples/sample_transactions.csv")
    oversell = transactions[:1] + [replace(transactions[2], quantity=Decimal("2.5"))]

    try:
        calculate_average_cost(oversell)
    except ValueError as exc:
        assert "sell quantity exceeds" in str(exc)
    else:
        raise AssertionError("expected oversell to fail")
