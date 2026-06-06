# CSV Template Handling

## Purpose

This note records how exchange CSV templates are handled safely.

The local template ZIP is reference material only. It is not copied into this OSS candidate.

## Template ZIP Review

Reviewed file:

```text
CSVtemplate.zip
```

Review result:

- Seven CSV template files were found.
- File names use a company/report naming convention such as `SBIVC_...`, `GMO_...`, `BitFlyer_...`, and `BitPoint_...`.
- Actual exported data files may omit the company prefix.
- No obvious real transaction rows were detected in the template files.
- One template row contained a date-like value in a date column only; no amount, identifier, transaction ID, or address-like value was detected in that row.

## File Name Matching Rule

Template file names may include a company prefix, while actual data file names may not.

Example:

```text
Template: SBIVC_CASHFLOW_YYYYMM.csv
Actual:   CASHFLOW_202601.csv
```

The program normalizes report names by:

1. Removing known company prefixes.
2. Removing date placeholders such as `YYYYMM`.
3. Removing actual date digits.
4. Comparing the remaining report name.

## Dynamic Crypto Columns

Some templates contain columns such as:

```text
残高_JPY
残高_USDC
残高_BTC
残高_ETH
残高_XRP
```

These columns must not be treated as a fixed list.

If a user stops trading one asset or starts holding another asset, the actual CSV may add or remove asset columns.

The program should:

- Detect dynamic asset columns by prefix, such as `残高_`.
- Preserve the stable non-asset columns from the template.
- Use the actual CSV's asset columns when they differ from the template.
- Avoid failing just because a crypto asset column was added or removed.

## Current Implementation

Implemented helper module:

```text
src/crypto_ledger_tools/exchange_templates.py
```

Supported helper behavior:

- Normalize template and actual CSV file names.
- Detect dynamic asset balance columns.
- Adjust template headers using actual CSV asset columns.

## 2026-06 Adapter Assumption

The OSS source assumes that users may pass CSV files based on the template set reviewed in June 2026.

Current adapter entry points:

```text
src/crypto_ledger_tools/exchange_adapters.py
```

Supported initial adapter families:

| Adapter | Template assumption |
|---|---|
| `coincheck_trade_history` | Coincheck trade history format |
| `bitflyer_trade_history` | bitFlyer crypto trade history format |
| `sbivc_trade_record` | SBI VC trade record format |
| `gmo_trading_report` | GMO trading report format |

The first implementation provides a safe conversion entry point and fictional tests.
When template files change, update the adapter mapping and record the change in the internal management MDA revision history.

## Safety Boundary

Do not commit:

- The original ZIP file.
- Real exchange exports.
- Real transaction rows.
- Real wallet address values.
- API keys, cookies, tokens, or webhook URLs.
