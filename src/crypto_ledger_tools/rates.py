from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from .models import parse_decimal


@dataclass(frozen=True)
class DailyRate:
    date: str
    base_currency: str
    quote_currency: str
    close: Decimal


def load_daily_rates(path: str | Path) -> dict[tuple[str, str, str], DailyRate]:
    rates_path = Path(path)
    with rates_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return {_rate_key(rate): rate for rate in (_normalize_rate(row) for row in reader)}


def convert_to_jpy(
    amount: Decimal,
    currency: str,
    date: str,
    rates: dict[tuple[str, str, str], DailyRate],
) -> Decimal:
    normalized_currency = currency.strip().upper()
    if normalized_currency == "JPY":
        return amount
    key = (date, normalized_currency, "JPY")
    if key not in rates:
        raise ValueError(f"missing {normalized_currency}/JPY daily close for {date}")
    return amount * rates[key].close


def _normalize_rate(row: dict[str, str]) -> DailyRate:
    required = ["date", "base_currency", "quote_currency", "close"]
    missing = [name for name in required if name not in row or row[name] == ""]
    if missing:
        raise ValueError(f"missing required rate fields: {', '.join(missing)}")
    return DailyRate(
        date=row["date"].strip(),
        base_currency=row["base_currency"].strip().upper(),
        quote_currency=row["quote_currency"].strip().upper(),
        close=parse_decimal(row["close"], "close"),
    )


def _rate_key(rate: DailyRate) -> tuple[str, str, str]:
    return (rate.date, rate.base_currency, rate.quote_currency)
