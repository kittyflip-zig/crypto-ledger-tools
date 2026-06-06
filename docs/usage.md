# Usage

## Install for Local Development

```powershell
cd software/oss_candidates/crypto-ledger-tools
python -m pip install -e ".[dev]"
```

## Run Tests

```powershell
python -m pytest
```

## Normalize CSV

```powershell
crypto-ledger-tools normalize examples/sample_transactions.csv --output normalized.csv
```

The normalize command validates required columns, standardizes side values and symbols, and writes a clean CSV.

## Generate Report

```powershell
crypto-ledger-tools report examples/sample_transactions.csv --output report.md
```

The report command calculates simple moving average cost and realized profit and loss from fictional sample rows.

## Convert Quote Values to JPY

```powershell
crypto-ledger-tools jpy examples/sample_transactions.csv --rates examples/sample_daily_rates.csv --output sample_jpy.csv
```

The JPY command reads a daily close rate CSV and adds JPY columns for transaction value, fee, and net value.

## Normalize Exchange CSV

```powershell
crypto-ledger-tools exchange-normalize examples/sample_coincheck_trade_history.csv --output normalized_exchange.csv
```

The exchange-normalize command detects supported Japanese exchange CSV layouts and writes the neutral ledger CSV schema.

## Import as Python

```python
from crypto_ledger_tools import build_markdown_report, load_transactions

transactions = load_transactions("examples/sample_transactions.csv")
report = build_markdown_report(transactions)
```

## Limitations

- Only `buy` and `sell` rows are supported in this first candidate.
- Multi-currency conversion is not included.
- The calculation method is intentionally simple and should be reviewed before any practical use.
