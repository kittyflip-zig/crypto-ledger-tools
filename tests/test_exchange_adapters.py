from crypto_ledger_tools.exchange_adapters import detect_adapter, load_exchange_transactions


def test_detect_adapter_for_coincheck_template_without_company_prefix():
    headers = ["取引日時", "増加通貨名", "増加数量", "減少通貨名", "減少数量"]

    adapter = detect_adapter("trade_history_20260101-20260131.csv", headers)

    assert adapter.adapter_id == "coincheck_trade_history"
    assert adapter.template_version == "2026-06"


def test_load_exchange_transactions_from_fictional_coincheck_csv():
    transactions = load_exchange_transactions("examples/sample_coincheck_trade_history.csv")

    assert len(transactions) == 2
    assert transactions[0].asset == "BTC"
    assert transactions[0].side == "buy"
    assert transactions[0].quote_currency == "JPY"
    assert transactions[1].asset == "BTC"
    assert transactions[1].side == "sell"
