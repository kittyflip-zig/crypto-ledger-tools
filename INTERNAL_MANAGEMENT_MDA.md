# Crypto Ledger Tools Internal Management MDA

MDA means `Management Document Archive` in this repository.

> 日本語注釈：
> この文書での `MDA` は `Management Document Archive` の略です。
> OSS実体ファイルとは別に、内部管理、発行判断、テンプレート改版、確認履歴を残すための管理文書という意味で使います。

## Document Metadata / 文書メタ情報

| Field | Value |
|---|---|
| Doc ID | `HTD-05DOP-DOP08-D01` |
| Title | Crypto Ledger Tools Internal Management MDA |
| Status | draft |
| Owner | DevOps / GitHub |
| Maintainer | HIDE / Codex |
| Public Revision | D01 |
| Change Class | initial |
| Last Updated | 2026-06-06 |
| QR Code | TBD |

---

## Purpose

This internal management MDA, or Management Document Archive, tracks the OSS publication preparation of `crypto-ledger-tools`.

This file is separate from the public package files. It records internal scope, template-version assumptions, review gates, and revision history for publication control.

> 日本語注釈：
> このMDAは、OSS実体ファイルとは別に、内部管理・発行判断・テンプレート改版チェックを残すための管理MDです。

---

## Current OSS Positioning

`crypto-ledger-tools` is a Japan-focused crypto ledger toolkit candidate.

Primary language:

- Japanese

Secondary language:

- English for OSS publication and developer readability

Current target users:

- Japanese crypto users who need CSV normalization, acquisition-cost checks, JPY conversion, and exchange CSV conversion support.

---

## Template Version Baseline

Current baseline:

```text
CSV template set reviewed: 2026-06
```

Reviewed template families:

| Family | Status | Notes |
|---|---|---|
| SBI VC Trade | adapter entry added | Company prefix may be absent in actual file name |
| GMO Coin | adapter entry added | Trade report mapping is initial |
| Coincheck | adapter entry added | Strong first practical adapter candidate |
| bitFlyer trade history | adapter entry added | Trade history mapping is initial |
| bitFlyer balance history | template-aware only | Balance rows require separate design |
| BitPoint spot | template-aware only | Header structure needs adapter design |
| SBI VC cashflow | template-aware only | Dynamic `残高_` columns supported |

---

## Conversion Policy

Rules:

- Do not copy real exchange CSV files into the OSS candidate.
- Do not publish the original template ZIP.
- Use fictional fixtures only.
- Treat company-name prefixes in template file names as optional.
- Treat crypto-specific columns such as `残高_BTC` and `残高_SUI` as dynamic.
- Keep tax treatment, accounting treatment, and investment judgment outside the adapter.

---

## Current Implementation Records

| Area | File | Status |
|---|---|---|
| Generic ledger schema | `src/crypto_ledger_tools/models.py` | implemented |
| JPY daily-rate conversion | `src/crypto_ledger_tools/jpy.py` | implemented |
| Daily rate loading | `src/crypto_ledger_tools/rates.py` | implemented |
| Template name / dynamic column handling | `src/crypto_ledger_tools/exchange_templates.py` | implemented |
| Exchange adapter entry points | `src/crypto_ledger_tools/exchange_adapters.py` | initial |
| CLI exchange normalization | `exchange-normalize` | initial |

---

## Publication Gates

Before public release:

- [ ] HIDE confirms Japan-focused positioning.
- [ ] HIDE confirms MIT License.
- [ ] HIDE confirms template baseline `2026-06`.
- [ ] HIDE confirms no real exchange CSV is included.
- [ ] HIDE confirms no template ZIP is included.
- [ ] HIDE confirms adapter descriptions do not imply tax advice.
- [ ] HIDE confirms GitHub Issues notification settings.
- [ ] HIDE confirms GitHub Sponsors account or support URL.
- [ ] Tests pass.
- [ ] Sensitive-data `rg` check passes.

---

## Current Document ID / 現行文書番号

```text
HTD-05DOP-DOP08-D01
```

---

## Revision History / 改版履歴

| Doc ID | Date | Change Class | Author / Role | Summary | Reason |
|---|---|---|---|---|---|
| `HTD-05DOP-DOP08-D01` | 2026-06-06 | initial | Codex / DevOps | Created internal management MDA for crypto-ledger-tools OSS publication. | HIDE requested internal management MDA before Git publication. |
