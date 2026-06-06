# Crypto Ledger Tools Program Asset Ledger

## Document Metadata / 文書メタ情報

| Field | Value |
|---|---|
| Doc ID | `HTD-05DOP-DOP09-D01` |
| Title | Crypto Ledger Tools Program Asset Ledger |
| Status | draft |
| Owner | DevOps / GitHub |
| Maintainer | HIDE / Codex |
| Public Revision | D01 |
| Change Class | initial |
| Last Updated | 2026-06-06 |
| QR Code | TBD |

---

## Purpose

This ledger tracks program assets for `crypto-ledger-tools`.

> 日本語注釈：
> この台帳は、OSS本体のソースコード、ドキュメント、サンプル、GitHub表示用バナーなどを管理するためのプログラム資産管理台帳です。

---

## Program CAT Definition

In this project, `Program CAT` means:

```text
Program Catalog / Asset Tracking
```

It is a lightweight category label for program-related assets such as source code, tests, docs, examples, CI, and repository branding files.

---

## Asset Inventory

| Asset ID | Category | Path | Status | Notes |
|---|---|---|---|---|
| `CLT-ASSET-001` | Source | `src/crypto_ledger_tools/` | active | Python package source |
| `CLT-ASSET-002` | Tests | `tests/` | active | pytest coverage |
| `CLT-ASSET-003` | Examples | `examples/` | active | Fictional sample CSV only |
| `CLT-ASSET-004` | Docs | `docs/` | active | Usage, data format, roadmap, release setup |
| `CLT-ASSET-005` | GitHub CI | `.github/workflows/ci.yml` | active | GitHub Actions test workflow |
| `CLT-ASSET-006` | GitHub Issues | `.github/ISSUE_TEMPLATE/` | active | Bug report and feature request templates |
| `CLT-ASSET-007` | Funding | `.github/FUNDING.yml` | active | GitHub Sponsors account: `kittyflip-zig` |
| `CLT-ASSET-008` | Branding | `assets/repository-open-graph.png` | active | GitHub Open Graph / social preview banner |
| `CLT-ASSET-009` | Internal control | `INTERNAL_MANAGEMENT_MDA.md` | active | Internal publication control MDA |
| `CLT-ASSET-010` | Publication review | `OSS_PUBLICATION_REVIEW.md` | active | Public release review record |

---

## Branding Asset Record

| Field | Value |
|---|---|
| File | `assets/repository-open-graph.png` |
| Size | `1280 x 640 px` |
| Purpose | GitHub repository Open Graph / social preview image |
| Title | `crypto-ledger-tools` |
| Creator Credit | `Program CAT / 制作者: HT Designs` |
| Logo Placement | Top-right |
| Logo Source | HTDESIGNS company logo source, embedded into banner image |
| Template Reference | GitHub repository Open Graph template from local Downloads, reference only |

Rules:

- Do not add raw design working files unless needed.
- Keep final public banner in `assets/`.
- If logo or brand color changes, update this ledger and regenerate the banner.
- Do not include private source paths in public README.

---

## GitHub Upload Use

To use the banner on GitHub:

1. Open the repository.
2. Go to `Settings`.
3. Open `Social preview`.
4. Upload `assets/repository-open-graph.png`.
5. Save.

---

## Current Document ID / 現行文書番号

```text
HTD-05DOP-DOP09-D01
```

---

## Revision History / 改版履歴

| Doc ID | Date | Change Class | Author / Role | Summary | Reason |
|---|---|---|---|---|---|
| `HTD-05DOP-DOP09-D01` | 2026-06-06 | initial | Codex / DevOps | Created program asset ledger and registered Open Graph banner. | HIDE requested branding banner and program asset ledger. |
