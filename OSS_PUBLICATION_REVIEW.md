# OSS Publication Review

## 1. Public Candidate File List

- `README.md`
- `README.ja.md`
- `README.en.md`
- `.gitignore`
- `LICENSE`
- `pyproject.toml`
- `src/crypto_ledger_tools/__init__.py`
- `src/crypto_ledger_tools/models.py`
- `src/crypto_ledger_tools/exchange_adapters.py`
- `src/crypto_ledger_tools/exchange_templates.py`
- `src/crypto_ledger_tools/io.py`
- `src/crypto_ledger_tools/jpy.py`
- `src/crypto_ledger_tools/calculator.py`
- `src/crypto_ledger_tools/rates.py`
- `src/crypto_ledger_tools/report.py`
- `src/crypto_ledger_tools/cli.py`
- `tests/test_calculator.py`
- `tests/test_cli.py`
- `tests/test_exchange_adapters.py`
- `tests/test_exchange_templates.py`
- `tests/test_jpy.py`
- `examples/sample_daily_rates.csv`
- `examples/sample_coincheck_trade_history.csv`
- `examples/sample_transactions.csv`
- `docs/usage.md`
- `docs/data_format.md`
- `docs/csv_template_handling.md`
- `docs/disclaimer.md`
- `docs/github_release_setup.md`
- `docs/ja_overview.md`
- `docs/ja_quickstart.md`
- `docs/japan_roadmap.md`
- `docs/source_material_review.md`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `.github/workflows/ci.yml`
- `OSS_PUBLICATION_REVIEW.md`

Internal management file:

- `INTERNAL_MANAGEMENT_MDA.md` is maintained for HTDESIGNS internal publication control and is not required in the public OSS package.

## 2. Excluded File List

- Existing private repository code: excluded.
- Existing real transaction CSV files: excluded.
- Existing account exports: excluded.
- Existing API integration scripts: excluded.
- Existing local-only notes outside this candidate folder: excluded.
- Media files and generated binary files: excluded.
- Local test cache and generated outputs such as `.pytest_cache/`, `report.md`, `normalized.csv`, `__pycache__/`, and `*.egg-info/`: excluded by `.gitignore`.
- Local legacy material under `C:\temp`: excluded from publication and documented in `docs/source_material_review.md`.
- Original `CSVtemplate.zip`: excluded. Only template behavior notes and fictional fixtures are included.

## 3. Sensitive and Personal Data Check Result

Review target:

```text
software/oss_candidates/crypto-ledger-tools
```

Command required by publication review:

```powershell
rg -i "private|secret|token|api_key|password|wallet|address|exchange|gmail|cookie|webhook|kitty|nas|htdesigns_media" software/oss_candidates/crypto-ledger-tools
```

Publication review result:

- No real transaction history was added.
- No real wallet address value was added.
- No API key, access token, password, cookie, or webhook URL was added.
- No Gmail, NAS, local media path, or user-local path was added.
- Search hits for terms such as `wallet`, `address`, `token`, `password`, `cookie`, `webhook`, and `private` are expected only in documentation, disclaimer, contribution, and security-policy text.
- `TOKEN` appears as a fictional asset symbol in sample and test data.
- `.pytest_cache/` was generated during local test execution and is explicitly excluded from publication by `.gitignore`.
- `C:\temp` source material was reviewed by filename and script structure only; real data files were not imported.

## 4. Test Result

Planned verification commands:

```powershell
cd software/oss_candidates/crypto-ledger-tools
python -m pytest
python -m crypto_ledger_tools.cli report examples/sample_transactions.csv --output report.md
python -m crypto_ledger_tools.cli normalize examples/sample_transactions.csv --output normalized.csv
python -m crypto_ledger_tools.cli jpy examples/sample_transactions.csv --rates examples/sample_daily_rates.csv --output sample_jpy.csv
python -m crypto_ledger_tools.cli exchange-normalize examples/sample_coincheck_trade_history.csv --output normalized_exchange.csv
```

Result:

- `python -m pytest`: passed, 11 tests.
- `python -m crypto_ledger_tools.cli report examples/sample_transactions.csv --output <temp report>`: passed.
- `python -m crypto_ledger_tools.cli normalize examples/sample_transactions.csv --output <temp csv>`: passed.
- `python -m crypto_ledger_tools.cli jpy examples/sample_transactions.csv --rates examples/sample_daily_rates.csv --output <temp csv>`: passed.
- `python -m crypto_ledger_tools.cli exchange-normalize examples/sample_coincheck_trade_history.csv --output <temp csv>`: passed.

GitHub release setup:

- README now routes improvement suggestions to GitHub Issues.
- Sponsor text is added, but the real Sponsor URL still needs the final GitHub account or organization.

Environment note:

- Local verification used an explicit local Python executable because `python` was not available on PATH in this PowerShell session.

## 5. Remaining Risks

- Average-cost calculation rules are intentionally simple and may not match every jurisdiction, accounting policy, or user workflow.
- Only `buy` and `sell` rows are supported in the first candidate.
- Full multi-currency valuation, chain-specific events, staking rewards, fees paid in another asset, and transfers are not fully supported yet.
- Users may misinterpret calculation output unless the disclaimer remains visible.
- Public release should be blocked until HIDE confirms that no private source code or real transaction data was copied in.
- Public release should stay blocked until HIDE confirms the `C:\temp` legacy material boundary.

## 6. Description for OpenAI Codex for Open Source Application

`crypto-ledger-tools` is a small MIT-licensed Python package candidate from HT Designs Software / OSS Lab. It helps users normalize fictional crypto transaction CSV rows, calculate simple moving average acquisition cost, cross-check realized profit and loss, and export Markdown or CSV reports. The project is designed as a safe open source starting point: it contains only fictional sample data, avoids real wallet address values and credentials, includes tests and CI, and clearly states that it is not tax, accounting, investment, legal, or trading advice.

## 7. Items HIDE Should Confirm Next

- Confirm the package name `crypto-ledger-tools`.
- Confirm MIT License is acceptable for this OSS candidate.
- Confirm no prior private code was copied into this candidate.
- Confirm `C:\temp` files should remain excluded and reference-only.
- Confirm no real transaction CSV or account export should be added.
- Confirm whether the first public release should support only `buy` and `sell`.
- Confirm whether generated files such as `report.md` and `normalized.csv` should remain untracked.
- Confirm repository publication timing before any public push.
