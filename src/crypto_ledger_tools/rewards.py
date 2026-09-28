from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from .asset_rates import DailyAssetRate, find_rate_on_or_before
from .models import parse_decimal


@dataclass(frozen=True)
class RewardEvent:
    reward_id: str
    received_at: str
    asset: str
    quantity: Decimal
    source: str = ""
    note: str = ""


@dataclass(frozen=True)
class RewardValuation:
    event: RewardEvent
    rate_date: str
    asset_close: Decimal | None
    asset_quote_currency: str | None
    asset_rate_provider: str | None
    fx_rate: Decimal | None
    fx_rate_date: str | None
    fair_value_jpy: Decimal | None
    valuation_method: str
    status: str


def load_reward_events(path: str | Path) -> list[RewardEvent]:
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [_normalize_reward(row) for row in reader]


def value_reward_events(
    events: list[RewardEvent],
    rates: dict[tuple[str, str, str], DailyAssetRate],
    *,
    max_fx_lookback_days: int = 3,
) -> list[RewardValuation]:
    return [
        _value_reward(event, rates, max_fx_lookback_days=max_fx_lookback_days)
        for event in events
    ]


def write_reward_valuations(valuations: list[RewardValuation], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "reward_id",
        "received_at",
        "asset",
        "quantity",
        "source",
        "rate_date",
        "asset_close",
        "asset_quote_currency",
        "asset_rate_provider",
        "fx_rate",
        "fx_rate_date",
        "fair_value_jpy",
        "valuation_method",
        "status",
        "note",
    ]
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for value in valuations:
            writer.writerow(
                {
                    "reward_id": value.event.reward_id,
                    "received_at": value.event.received_at,
                    "asset": value.event.asset,
                    "quantity": str(value.event.quantity),
                    "source": value.event.source,
                    "rate_date": value.rate_date,
                    "asset_close": _text(value.asset_close),
                    "asset_quote_currency": value.asset_quote_currency or "",
                    "asset_rate_provider": value.asset_rate_provider or "",
                    "fx_rate": _text(value.fx_rate),
                    "fx_rate_date": value.fx_rate_date or "",
                    "fair_value_jpy": _text(value.fair_value_jpy),
                    "valuation_method": value.valuation_method,
                    "status": value.status,
                    "note": value.event.note,
                }
            )


def _value_reward(
    event: RewardEvent,
    rates: dict[tuple[str, str, str], DailyAssetRate],
    *,
    max_fx_lookback_days: int,
) -> RewardValuation:
    rate_date = event.received_at[:10]

    direct_jpy = find_rate_on_or_before(
        rates, rate_date, event.asset, "JPY", max_lookback_days=0
    )
    if direct_jpy is not None:
        fair = (event.quantity * direct_jpy.close).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        return RewardValuation(
            event=event,
            rate_date=rate_date,
            asset_close=direct_jpy.close,
            asset_quote_currency="JPY",
            asset_rate_provider=direct_jpy.provider,
            fx_rate=Decimal("1"),
            fx_rate_date=rate_date,
            fair_value_jpy=fair,
            valuation_method="daily_close_direct_jpy",
            status="provisional_daily_close",
        )

    usd_rate = find_rate_on_or_before(
        rates, rate_date, event.asset, "USD", max_lookback_days=0
    )
    if usd_rate is None:
        return RewardValuation(
            event=event,
            rate_date=rate_date,
            asset_close=None,
            asset_quote_currency=None,
            asset_rate_provider=None,
            fx_rate=None,
            fx_rate_date=None,
            fair_value_jpy=None,
            valuation_method="unavailable",
            status="missing_asset_rate",
        )

    fx = find_rate_on_or_before(
        rates,
        rate_date,
        "USD",
        "JPY",
        max_lookback_days=max_fx_lookback_days,
    )
    if fx is None:
        return RewardValuation(
            event=event,
            rate_date=rate_date,
            asset_close=usd_rate.close,
            asset_quote_currency="USD",
            asset_rate_provider=usd_rate.provider,
            fx_rate=None,
            fx_rate_date=None,
            fair_value_jpy=None,
            valuation_method="unavailable",
            status="missing_fx_rate",
        )

    fair = (event.quantity * usd_rate.close * fx.close).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    method = (
        "daily_close_usd_x_same_day_fx"
        if fx.date == rate_date
        else "daily_close_usd_x_prior_available_fx"
    )
    return RewardValuation(
        event=event,
        rate_date=rate_date,
        asset_close=usd_rate.close,
        asset_quote_currency="USD",
        asset_rate_provider=usd_rate.provider,
        fx_rate=fx.close,
        fx_rate_date=fx.date,
        fair_value_jpy=fair,
        valuation_method=method,
        status="provisional_daily_close",
    )


def _normalize_reward(row: dict[str, str]) -> RewardEvent:
    required = ["reward_id", "received_at", "asset", "quantity"]
    missing = [name for name in required if not (row.get(name) or "").strip()]
    if missing:
        raise ValueError(f"missing required reward fields: {', '.join(missing)}")
    return RewardEvent(
        reward_id=row["reward_id"].strip(),
        received_at=row["received_at"].strip(),
        asset=row["asset"].strip().upper(),
        quantity=parse_decimal(row["quantity"], "quantity"),
        source=(row.get("source") or "").strip(),
        note=(row.get("note") or "").strip(),
    )


def _text(value: Decimal | None) -> str:
    return "" if value is None else str(value)
