from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from .models import parse_decimal


@dataclass(frozen=True)
class DailyAssetRate:
    date: str
    asset: str
    quote_currency: str
    close: Decimal
    provider: str = ""
    provider_symbol: str = ""
    session_timestamp: str = ""
    source_retrieved_at: str = ""
    is_final: bool = True


def load_asset_daily_rates(path: str | Path) -> dict[tuple[str, str, str], DailyAssetRate]:
    rates_path = Path(path)
    with rates_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rates = [_normalize(row) for row in reader]
    return {(r.date, r.asset, r.quote_currency): r for r in rates}


def find_rate_on_or_before(
    rates: dict[tuple[str, str, str], DailyAssetRate],
    rate_date: str,
    asset: str,
    quote_currency: str,
    *,
    max_lookback_days: int = 0,
) -> DailyAssetRate | None:
    target = date.fromisoformat(rate_date)
    asset = asset.strip().upper()
    quote_currency = quote_currency.strip().upper()
    for offset in range(max_lookback_days + 1):
        candidate = (target - timedelta(days=offset)).isoformat()
        rate = rates.get((candidate, asset, quote_currency))
        if rate is not None:
            return rate
    return None


def _normalize(row: dict[str, str]) -> DailyAssetRate:
    required = ["date", "asset", "quote_currency", "close"]
    missing = [name for name in required if not (row.get(name) or "").strip()]
    if missing:
        raise ValueError(f"missing required asset-rate fields: {', '.join(missing)}")
    final_text = (row.get("is_final") or "1").strip().lower()
    return DailyAssetRate(
        date=row["date"].strip(),
        asset=row["asset"].strip().upper(),
        quote_currency=row["quote_currency"].strip().upper(),
        close=parse_decimal(row["close"], "close"),
        provider=(row.get("provider") or "").strip(),
        provider_symbol=(row.get("provider_symbol") or "").strip(),
        session_timestamp=(row.get("session_timestamp") or "").strip(),
        source_retrieved_at=(row.get("source_retrieved_at") or "").strip(),
        is_final=final_text not in {"0", "false", "no"},
    )
