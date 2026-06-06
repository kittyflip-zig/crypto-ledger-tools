from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Callable

from .exchange_templates import normalize_report_filename
from .models import NormalizedTransaction, normalize_row


SUPPORTED_TEMPLATE_VERSION = "2026-06"


@dataclass(frozen=True)
class ExchangeAdapter:
    adapter_id: str
    display_name: str
    template_version: str
    filename_markers: tuple[str, ...]
    required_columns: tuple[str, ...]
    converter: Callable[[dict[str, str]], NormalizedTransaction | None]


def list_supported_adapters() -> list[ExchangeAdapter]:
    return [
        ExchangeAdapter(
            adapter_id="coincheck_trade_history",
            display_name="Coincheck trade history",
            template_version=SUPPORTED_TEMPLATE_VERSION,
            filename_markers=("trade_history_様式1_コインチェック株式会社", "trade_history_様式1"),
            required_columns=("取引日時", "増加通貨名", "増加数量", "減少通貨名", "減少数量"),
            converter=_convert_coincheck_row,
        ),
        ExchangeAdapter(
            adapter_id="bitflyer_trade_history",
            display_name="bitFlyer crypto trade history",
            template_version=SUPPORTED_TEMPLATE_VERSION,
            filename_markers=("tradehistory_仮想通貨の取引",),
            required_columns=("取引日時", "通貨1", "通貨1数量", "通貨2", "通貨2数量"),
            converter=_convert_bitflyer_trade_row,
        ),
        ExchangeAdapter(
            adapter_id="sbivc_trade_record",
            display_name="SBI VC Trade record",
            template_version=SUPPORTED_TEMPLATE_VERSION,
            filename_markers=("trade_record_list",),
            required_columns=("約定日時", "銘柄", "売買", "数量"),
            converter=_convert_sbivc_trade_row,
        ),
        ExchangeAdapter(
            adapter_id="gmo_trading_report",
            display_name="GMO trading report",
            template_version=SUPPORTED_TEMPLATE_VERSION,
            filename_markers=("trading_report",),
            required_columns=("日時", "銘柄名", "売買区分", "約定数量"),
            converter=_convert_gmo_trade_row,
        ),
    ]


def detect_adapter(filename: str | Path, headers: list[str]) -> ExchangeAdapter:
    normalized_name = normalize_report_filename(filename)
    normalized_headers = {header.strip() for header in headers}
    for adapter in list_supported_adapters():
        marker_match = any(marker.lower() in normalized_name for marker in adapter.filename_markers)
        header_match = all(column in normalized_headers for column in adapter.required_columns)
        if marker_match or header_match:
            return adapter
    raise ValueError(f"unsupported exchange CSV template: {Path(filename).name}")


def load_exchange_transactions(path: str | Path) -> list[NormalizedTransaction]:
    csv_path = Path(path)
    rows = _read_csv_with_fallback(csv_path)
    if not rows:
        return []

    adapter = detect_adapter(csv_path.name, list(rows[0].keys()))
    transactions: list[NormalizedTransaction] = []
    for row in rows:
        tx = adapter.converter(row)
        if tx is not None:
            transactions.append(tx)
    return transactions


def _read_csv_with_fallback(path: Path) -> list[dict[str, str]]:
    for encoding in ("utf-8-sig", "cp932"):
        try:
            with path.open("r", encoding=encoding, newline="") as handle:
                return list(csv.DictReader(handle))
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("csv", b"", 0, 1, "unsupported encoding")


def _convert_coincheck_row(row: dict[str, str]) -> NormalizedTransaction | None:
    increase_currency = _value(row, "増加通貨名")
    decrease_currency = _value(row, "減少通貨名")
    increase_quantity = _decimal_or_none(_value(row, "増加数量"))
    decrease_quantity = _decimal_or_none(_value(row, "減少数量"))

    if increase_currency and increase_currency != "JPY" and increase_quantity:
        return _make_tx(
            tx_id=_first_value(row, "登録番号", "取引日時"),
            timestamp=_value(row, "取引日時"),
            asset=increase_currency,
            side="buy",
            quantity=increase_quantity,
            total_value=decrease_quantity or Decimal("0"),
            fee=_decimal_or_zero(_value(row, "手数料数量")),
            quote_currency=decrease_currency or "JPY",
            note=_value(row, "取引種別") or "coincheck import",
        )

    if decrease_currency and decrease_currency != "JPY" and decrease_quantity:
        return _make_tx(
            tx_id=_first_value(row, "登録番号", "取引日時"),
            timestamp=_value(row, "取引日時"),
            asset=decrease_currency,
            side="sell",
            quantity=decrease_quantity,
            total_value=increase_quantity or Decimal("0"),
            fee=_decimal_or_zero(_value(row, "手数料数量")),
            quote_currency=increase_currency or "JPY",
            note=_value(row, "取引種別") or "coincheck import",
        )
    return None


def _convert_bitflyer_trade_row(row: dict[str, str]) -> NormalizedTransaction | None:
    asset = _value(row, "通貨1")
    quote = _value(row, "通貨2") or "JPY"
    quantity = _decimal_or_none(_value(row, "通貨1数量"))
    total_value = _decimal_or_none(_value(row, "通貨2数量")) or _decimal_or_none(_value(row, "取引価格"))
    if not asset or not quantity or not total_value:
        return None
    side = "sell" if quantity < 0 else "buy"
    return _make_tx(
        tx_id=_first_value(row, "注文 ID", "取引日時"),
        timestamp=_value(row, "取引日時"),
        asset=asset,
        side=side,
        quantity=abs(quantity),
        total_value=abs(total_value),
        fee=abs(_decimal_or_zero(_first_value(row, "手数料(JPY)", "手数料"))),
        quote_currency=quote,
        note=_value(row, "取引種別") or "bitflyer import",
    )


def _convert_sbivc_trade_row(row: dict[str, str]) -> NormalizedTransaction | None:
    asset = _value(row, "銘柄")
    quantity = _decimal_or_none(_value(row, "数量"))
    rate = _decimal_or_none(_value(row, "約定レート"))
    if not asset or not quantity or not rate:
        return None
    side = "sell" if "売" in _value(row, "売買") else "buy"
    return _make_tx(
        tx_id=_first_value(row, "取引番号", "約定日時"),
        timestamp=_value(row, "約定日時"),
        asset=asset,
        side=side,
        quantity=quantity,
        total_value=quantity * rate,
        fee=_decimal_or_zero(_value(row, "取引手数料")),
        quote_currency="JPY",
        note=_value(row, "取引区分") or "sbivc import",
    )


def _convert_gmo_trade_row(row: dict[str, str]) -> NormalizedTransaction | None:
    asset = _value(row, "銘柄名")
    quantity = _decimal_or_none(_value(row, "約定数量"))
    total_value = _decimal_or_none(_value(row, "約定金額"))
    if not asset or not quantity or not total_value:
        return None
    side = "sell" if "売" in _value(row, "売買区分") else "buy"
    return _make_tx(
        tx_id=_first_value(row, "約定ID", "注文ID", "日時"),
        timestamp=_value(row, "日時"),
        asset=asset,
        side=side,
        quantity=quantity,
        total_value=total_value,
        fee=_decimal_or_zero(_value(row, "注文手数料")),
        quote_currency="JPY",
        note=_value(row, "精算区分") or "gmo import",
    )


def _make_tx(
    *,
    tx_id: str,
    timestamp: str,
    asset: str,
    side: str,
    quantity: Decimal,
    total_value: Decimal,
    fee: Decimal,
    quote_currency: str,
    note: str,
) -> NormalizedTransaction:
    return normalize_row(
        {
            "tx_id": tx_id or timestamp,
            "timestamp": timestamp,
            "asset": asset,
            "side": side,
            "quantity": str(quantity),
            "total_value": str(total_value),
            "fee": str(fee),
            "quote_currency": quote_currency or "JPY",
            "note": note,
        }
    )


def _value(row: dict[str, str], column: str) -> str:
    return (row.get(column) or "").strip()


def _first_value(row: dict[str, str], *columns: str) -> str:
    for column in columns:
        value = _value(row, column)
        if value:
            return value
    return ""


def _decimal_or_none(value: str) -> Decimal | None:
    clean = value.replace(",", "").strip()
    if not clean:
        return None
    try:
        return Decimal(clean)
    except Exception:
        return None


def _decimal_or_zero(value: str) -> Decimal:
    return _decimal_or_none(value) or Decimal("0")
