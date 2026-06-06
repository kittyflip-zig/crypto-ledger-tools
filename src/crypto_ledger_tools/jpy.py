from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from .io import FIELD_NAMES
from .models import NormalizedTransaction
from .rates import DailyRate, convert_to_jpy


JPY_FIELD_NAMES = FIELD_NAMES + [
    "rate_date",
    "total_value_jpy",
    "fee_jpy",
    "net_quote_value_jpy",
]


@dataclass(frozen=True)
class JpyTransactionView:
    transaction: NormalizedTransaction
    rate_date: str
    total_value_jpy: Decimal
    fee_jpy: Decimal
    net_quote_value_jpy: Decimal


def build_jpy_views(
    transactions: list[NormalizedTransaction],
    rates: dict[tuple[str, str, str], DailyRate],
) -> list[JpyTransactionView]:
    return [_build_jpy_view(tx, rates) for tx in transactions]


def write_jpy_csv(views: list[JpyTransactionView], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=JPY_FIELD_NAMES)
        writer.writeheader()
        for view in views:
            tx = view.transaction
            writer.writerow(
                {
                    "tx_id": tx.tx_id,
                    "timestamp": tx.timestamp,
                    "asset": tx.asset,
                    "side": tx.side,
                    "quantity": str(tx.quantity),
                    "total_value": str(tx.total_value),
                    "fee": str(tx.fee),
                    "quote_currency": tx.quote_currency,
                    "note": tx.note,
                    "rate_date": view.rate_date,
                    "total_value_jpy": _fmt_jpy(view.total_value_jpy),
                    "fee_jpy": _fmt_jpy(view.fee_jpy),
                    "net_quote_value_jpy": _fmt_jpy(view.net_quote_value_jpy),
                }
            )


def _build_jpy_view(
    tx: NormalizedTransaction,
    rates: dict[tuple[str, str, str], DailyRate],
) -> JpyTransactionView:
    rate_date = tx.timestamp[:10]
    return JpyTransactionView(
        transaction=tx,
        rate_date=rate_date,
        total_value_jpy=convert_to_jpy(tx.total_value, tx.quote_currency, rate_date, rates),
        fee_jpy=convert_to_jpy(tx.fee, tx.quote_currency, rate_date, rates),
        net_quote_value_jpy=convert_to_jpy(tx.net_quote_value, tx.quote_currency, rate_date, rates),
    )


def _fmt_jpy(value: Decimal) -> str:
    return str(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
