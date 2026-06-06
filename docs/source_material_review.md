# Source Material Review

## Purpose

This note records how local legacy material was handled while preparing `crypto-ledger-tools` as an OSS candidate.

## Reviewed Location

```text
C:\temp
```

## Handling Decision

The local folder contains legacy scripts and generated working files related to crypto CSV processing, price/rate lookup, spreadsheet reporting, and chain-history export.

These files were treated as reference material only.

No legacy source file, real transaction file, generated spreadsheet, generated PDF, local cache, or chain-history export was copied into the OSS candidate.

## Excluded Material Categories

- Real or semi-real transaction CSV exports
- Generated Excel workbooks
- Generated PDF reports
- Rate cache files
- Legacy one-off Python scripts
- Chain-history export scripts that require user-supplied address values
- API-oriented price/rate lookup scripts
- Local output folders

## Safe Reimplementation Boundary

The OSS candidate keeps only general, reusable behavior:

- CSV schema validation
- Transaction row normalization
- Simple moving average acquisition cost calculation
- Realized profit and loss cross-checking
- Markdown and CSV report output
- Fictional sample data

The candidate does not include:

- Real transaction rows
- Real wallet address values
- Exchange-specific private exports
- API credentials
- Tax filing templates
- Investment or trading recommendations

## Notes for Future Review

- If exchange-specific importers are added later, create fictional fixture files first.
- If API-based rate lookup is added later, read credentials from environment variables only.
- If chain-history export is added later, keep address values out of sample files and tests.
- Keep this candidate publication-blocked until HIDE confirms the source material boundary.
