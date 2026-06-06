from crypto_ledger_tools.exchange_templates import (
    adjusted_headers_for_actual_csv,
    detect_dynamic_asset_columns,
    normalize_report_filename,
)


def test_normalize_report_filename_allows_company_prefix_to_be_absent():
    template_name = "SBIVC_CASHFLOW_YYYYMM.csv"
    actual_name = "CASHFLOW_202601.csv"

    assert normalize_report_filename(template_name) == normalize_report_filename(actual_name)


def test_detect_dynamic_asset_columns_from_balance_headers():
    headers = ["日時", "入出金の種別", "残高_JPY", "残高_BTC", "残高_SOL"]

    assert detect_dynamic_asset_columns(headers) == ["残高_JPY", "残高_BTC", "残高_SOL"]


def test_adjusted_headers_uses_actual_dynamic_asset_columns():
    template_headers = ["日時", "入出金の種別", "残高_JPY", "残高_BTC", "残高_ETH"]
    actual_headers = ["日時", "入出金の種別", "残高_JPY", "残高_SUI", "残高_XRP"]

    assert adjusted_headers_for_actual_csv(template_headers, actual_headers) == [
        "日時",
        "入出金の種別",
        "残高_JPY",
        "残高_SUI",
        "残高_XRP",
    ]
