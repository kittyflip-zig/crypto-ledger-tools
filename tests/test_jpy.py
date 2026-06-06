from decimal import Decimal

from crypto_ledger_tools import build_jpy_views, load_daily_rates, load_transactions
from crypto_ledger_tools.cli import main


def test_build_jpy_views_from_sample_rates():
    transactions = load_transactions("examples/sample_transactions.csv")
    rates = load_daily_rates("examples/sample_daily_rates.csv")

    views = build_jpy_views(transactions, rates)

    assert views[0].rate_date == "2026-01-05"
    assert views[0].total_value_jpy == 30000
    assert views[0].fee_jpy == 150
    assert views[2].net_quote_value_jpy == Decimal("31323.1800")


def test_cli_jpy_writes_csv(tmp_path):
    output = tmp_path / "sample_jpy.csv"

    exit_code = main(
        [
            "jpy",
            "examples/sample_transactions.csv",
            "--rates",
            "examples/sample_daily_rates.csv",
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    text = output.read_text(encoding="utf-8")
    assert "total_value_jpy" in text
    assert "30000" in text
