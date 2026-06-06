# Data Format

The input file must be UTF-8 CSV with a header row.

## Columns

| Column | Required | Example | Notes |
|---|---:|---|---|
| `tx_id` | Yes | `demo-001` | Fictional row identifier |
| `timestamp` | Yes | `2026-01-05T10:00:00` | Used for chronological sorting |
| `asset` | Yes | `COIN` | Normalized to uppercase |
| `side` | Yes | `buy` | Supported values: `buy`, `sell` |
| `quantity` | Yes | `2.0` | Must be greater than zero |
| `total_value` | Yes | `200.00` | Quote amount before fee |
| `fee` | Yes | `1.00` | Quote-currency fee |
| `quote_currency` | Yes | `USD` | Normalized to uppercase |
| `note` | No | `fictional first buy` | Optional memo |

## Fee Handling

- Buy rows: `total_value + fee` becomes acquisition cost.
- Sell rows: `total_value - fee` becomes disposal proceeds.

## Sample Data Policy

Sample files must use fictional identifiers and fictional amounts only.

Do not add real transaction history, real account exports, real wallet address values, personal identifiers, or credentials.
