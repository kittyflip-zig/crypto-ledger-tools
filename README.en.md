# crypto-ledger-tools

Japanese README: [README.md](README.md)

`crypto-ledger-tools` is a Japan-focused OSS candidate from HT Designs Software / OSS Lab.

It provides reusable Python utilities for normalizing crypto transaction CSV files, calculating average acquisition cost, converting values to JPY using daily close rates, checking realized profit and loss, and exporting simple reports.

This project is designed for publication review. It does not include real transaction records, real wallet address values, API credentials, or personal data.

## Scope

Included:

- CSV formatting and validation
- Transaction normalization
- Average acquisition cost calculation
- Realized profit and loss cross-checks
- Daily close rate loading and JPY conversion
- Japanese exchange CSV normalization entry points
- Markdown and CSV report output
- CLI and importable Python functions
- Tests and CI

Not included:

- Tax advice
- Investment advice
- Buy or sell recommendations
- Real wallet address handling
- API credential storage

## Quick Start

```powershell
cd software/oss_candidates/crypto-ledger-tools
python -m pip install -e ".[dev]"
python -m pytest
python -m crypto_ledger_tools.cli report examples/sample_transactions.csv --output work/output/sample_report.md
```

## Safety Position

This repository is a tooling candidate, not a financial, investment, accounting, legal, or tax advisory product.

See [docs/disclaimer.md](docs/disclaimer.md) and [SECURITY.md](SECURITY.md).

## Feedback and Support

Bug reports, feature requests, CSV template changes, and documentation improvements are welcome via GitHub Issues.

Do not post real transaction CSV files, wallet address values, API keys, personal data, or security vulnerabilities in public Issues.

If this project helps you, GitHub Stars, Issues, CSV template reports, and GitHub Sponsors support are welcome.

## License

MIT License. See [LICENSE](LICENSE).
