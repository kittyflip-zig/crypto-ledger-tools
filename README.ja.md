# crypto-ledger-tools

`crypto-ledger-tools` は、日本人向けに暗号資産のCSV整理、取得単価の検算、日本円換算、取引所CSVの共通形式化を行うためのPythonツールです。

HT Designs Software / OSS Lab のOSS候補として準備しています。

このツールは、税務判断、投資助言、売買判断を行うものではありません。

---

## 何ができる？

主な機能:

- 取引CSVを共通形式にそろえる
- `buy` / `sell` の取引データを正規化する
- 平均取得単価を計算する
- 売却済み分の損益を検算する
- USDなどの金額を日次終値レートで日本円換算する
- Coincheckなど日本向け取引所CSVを共通形式へ変換する入口を提供する
- Markdown / CSVで確認用レポートを出す

やらないこと:

- 税務判断
- 投資助言
- 売買推奨
- 実ウォレット管理
- 実取引CSVの同梱
- APIキーや秘密情報の保存

---

## 最初に試す手順

PowerShellでこのフォルダへ移動します。

```powershell
cd software/oss_candidates/crypto-ledger-tools
```

インストールします。

```powershell
python -m pip install -e ".[dev]"
```

テストを実行します。

```powershell
python -m pytest
```

成功すると、次のような結果になります。

```text
11 passed
```

---

## サンプルCSVでレポートを作る

同梱の架空サンプルCSVを使います。

```powershell
python -m crypto_ledger_tools.cli report examples/sample_transactions.csv --output work/output/sample_report.md
```

出力先:

```text
work/output/sample_report.md
```

---

## CSVを正規化する

```powershell
python -m crypto_ledger_tools.cli normalize examples/sample_transactions.csv --output work/output/sample_normalized.csv
```

出力先:

```text
work/output/sample_normalized.csv
```

---

## 日本円換算CSVを作る

取引CSVと日次終値レートCSVを使って、日本円換算列を追加します。

```powershell
python -m crypto_ledger_tools.cli jpy examples/sample_transactions.csv --rates examples/sample_daily_rates.csv --output work/output/sample_jpy.csv
```

出力先:

```text
work/output/sample_jpy.csv
```

追加される主な列:

| 列名 | 内容 |
|---|---|
| `rate_date` | 換算に使った日付 |
| `total_value_jpy` | 取引金額の日本円換算 |
| `fee_jpy` | 手数料の日本円換算 |
| `net_quote_value_jpy` | 手数料反映後の日本円換算 |

---

## 取引所CSVを共通形式へ変換する

取引所別CSVを、ツール内部の共通CSV形式へ寄せます。

```powershell
python -m crypto_ledger_tools.cli exchange-normalize examples/sample_coincheck_trade_history.csv --output work/output/normalized_exchange.csv
```

出力先:

```text
work/output/normalized_exchange.csv
```

現時点では、2026年6月時点のCSVテンプレートを前提に、次の会社・帳票への対応を進めています。

| 対応候補 | 状態 |
|---|---|
| Coincheck 取引履歴 | 初期アダプタあり |
| bitFlyer 取引履歴 | 初期アダプタ入口あり |
| SBI VC Trade | 初期アダプタ入口あり |
| GMO Coin | 初期アダプタ入口あり |
| BitPoint | テンプレート認識・設計対象 |
| 残高履歴 / Cashflow系 | 動的な暗号通貨列に対応する方針 |

会社名がファイル名の先頭に付くテンプレートと、実データ側で会社名が付かないファイル名の両方を想定しています。

例:

```text
SBIVC_CASHFLOW_YYYYMM.csv
CASHFLOW_202601.csv
```

---

## 自分のCSVを置く場所

自分用のCSVは、次のフォルダに置く想定です。

```text
work/input/
```

出力は次のフォルダに置きます。

```text
work/output/
```

フォルダ作成:

```powershell
New-Item -ItemType Directory -Force -Path work/input, work/output
```

`work/` は `.gitignore` に入れてあります。
実取引CSVや生成物をGitに入れないためです。

---

## 入力CSVの共通形式

基本の共通CSVは次の列を使います。

| 列名 | 内容 |
|---|---|
| `tx_id` | 取引ID |
| `timestamp` | 取引日時 |
| `asset` | 暗号資産名 |
| `side` | `buy` または `sell` |
| `quantity` | 数量 |
| `total_value` | 手数料を除いた合計金額 |
| `fee` | 手数料 |
| `quote_currency` | 評価通貨 |
| `note` | 任意メモ |

---

## 注意

- 実取引CSVをOSSリポジトリにコミットしない。
- 実ウォレットアドレスをサンプルやテストに入れない。
- APIキー、トークン、Cookie、Webhook URLを入れない。
- 出力結果は検算用であり、税務判断や投資判断ではない。
- 取引所CSVテンプレートが変わった場合は、アダプタと内部管理MDAの改版履歴を更新する。

---

## 関連ドキュメント

- [docs/ja_quickstart.md](docs/ja_quickstart.md)
- [docs/ja_overview.md](docs/ja_overview.md)
- [docs/japan_roadmap.md](docs/japan_roadmap.md)
- [docs/csv_template_handling.md](docs/csv_template_handling.md)
- [docs/disclaimer.md](docs/disclaimer.md)
