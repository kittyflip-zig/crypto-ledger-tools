from pathlib import Path

from crypto_ledger_tools.cli import main


def test_cli_report_writes_markdown(tmp_path):
    output = tmp_path / "report.md"

    exit_code = main(["report", "examples/sample_transactions.csv", "--output", str(output)])

    assert exit_code == 0
    text = output.read_text(encoding="utf-8")
    assert "# Crypto Ledger Report" in text
    assert "| COIN | USD |" in text


def test_cli_normalize_writes_csv(tmp_path):
    output = tmp_path / "normalized.csv"

    exit_code = main(["normalize", "examples/sample_transactions.csv", "--output", str(output)])

    assert exit_code == 0
    assert Path(output).read_text(encoding="utf-8").startswith("tx_id,timestamp,asset")
