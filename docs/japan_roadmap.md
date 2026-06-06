# Japan-Focused Roadmap / 日本人向けロードマップ

## Purpose

`crypto-ledger-tools` is now positioned as a Japan-focused crypto ledger toolkit.

The main language should be Japanese, with English as a secondary language for OSS publication and international developer readability.

## Why Japan-Focused?

Japanese crypto users often need to:

- Convert USD-denominated values into JPY.
- Align calculations to daily close rates.
- Compare exchange CSV exports with their own ledger.
- Check acquisition cost and realized profit/loss without exposing real transaction data.
- Handle chain activity such as Sui transfers or staking-related rows.

This project should support those practical workflows while avoiding tax advice and investment advice.

## Current Candidate Scope

Implemented in the OSS candidate:

- Generic transaction CSV schema
- CSV template file name normalization
- Dynamic crypto balance-column detection
- CSV normalization
- Simple moving average acquisition cost calculation
- Realized profit/loss cross-checks
- Daily close rate CSV loading
- JPY conversion CSV output
- Markdown and CSV reporting
- Fictional sample data only

## Planned Adapter Scope

Future adapters should be added in this order:

1. Coincheck CSV adapter hardening
2. Sui activity CSV adapter
3. Additional Japanese exchange CSV adapters
4. Optional daily price/rate provider modules

## Sui Activity Direction

Legacy local material showed two useful Sui-related CSV shapes:

```text
type,details,activity_with,gasFee,age,timestamp_readable,txDigest
txDigest,timestamp,timestamp_readable,status,sender,gasUsed,gasBudget,kind
```

Future Sui support should:

- Convert chain activity rows into neutral ledger rows.
- Keep address values out of samples and tests.
- Treat gas fees as review fields first.
- Avoid deciding tax category automatically.
- Use fictional transaction digests in fixtures.

## Daily Rate Direction

The first supported rate format is:

```csv
date,base_currency,quote_currency,close
2026-01-05,USD,JPY,150.00
```

Future rate providers may support:

- USD/JPY daily close
- USDT/JPY daily close
- Crypto asset JPY daily close

Provider modules must not require credentials for basic tests.

If an API key is supported, it must be read from environment variables or CLI arguments and must never be stored in repository files.

## Exchange CSV Direction

Exchange CSV support should be adapter-based.

Each adapter should:

- Read one exchange export format.
- Match template names even when actual exports omit the company prefix.
- Treat asset-specific balance columns as dynamic columns.
- Map it into the neutral transaction schema.
- Include only fictional fixtures.
- Document unsupported columns.
- Keep raw real exports out of Git.

Coincheck support is a strong candidate for the first exchange adapter, but the current legacy file should remain excluded from publication.

## Non-Goals

This project must not:

- Decide tax treatment.
- Recommend buying, selling, holding, or transferring assets.
- Publish real transaction CSV files.
- Publish real wallet address values.
- Store API keys, cookies, tokens, or webhook URLs.

## Next HIDE Review Points

- Confirm Japan-focused positioning.
- Confirm Japanese-first documentation policy.
- Confirm whether Sui support should be the next implementation item.
- Confirm which exchange CSV adapter should be implemented first.
- Prepare fictional CSV fixtures based on real export column names only.
