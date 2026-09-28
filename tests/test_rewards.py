from decimal import Decimal

from crypto_ledger_tools import (
    DailyAssetRate,
    RewardEvent,
    load_asset_daily_rates,
    load_reward_events,
    value_reward_events,
)
from crypto_ledger_tools.cli import main


def _rate(date, asset, quote, close, provider="test"):
    return DailyAssetRate(
        date=date,
        asset=asset,
        quote_currency=quote,
        close=Decimal(close),
        provider=provider,
    )


def test_value_reward_with_same_day_usd_and_fx():
    event = RewardEvent("r1", "2026-07-11T09:00:00+09:00", "COIN", Decimal("10"), "Example")
    rates = {
        ("2026-07-11", "COIN", "USD"): _rate("2026-07-11", "COIN", "USD", "2.50"),
        ("2026-07-11", "USD", "JPY"): _rate("2026-07-11", "USD", "JPY", "151"),
    }

    value = value_reward_events([event], rates)[0]

    assert value.fair_value_jpy == Decimal("3775")
    assert value.fx_rate_date == "2026-07-11"
    assert value.valuation_method == "daily_close_usd_x_same_day_fx"
    assert value.status == "provisional_daily_close"


def test_weekend_fx_uses_prior_available_rate_and_records_date():
    event = RewardEvent("r2", "2026-07-12T09:00:00+09:00", "COIN", Decimal("4"))
    rates = {
        ("2026-07-12", "COIN", "USD"): _rate("2026-07-12", "COIN", "USD", "3"),
        ("2026-07-10", "USD", "JPY"): _rate("2026-07-10", "USD", "JPY", "150"),
    }

    value = value_reward_events([event], rates, max_fx_lookback_days=3)[0]

    assert value.fair_value_jpy == Decimal("1800")
    assert value.fx_rate_date == "2026-07-10"
    assert value.valuation_method == "daily_close_usd_x_prior_available_fx"


def test_direct_jpy_rate_has_priority():
    event = RewardEvent("r3", "2026-07-11", "COIN", Decimal("2"))
    rates = {
        ("2026-07-11", "COIN", "JPY"): _rate("2026-07-11", "COIN", "JPY", "400"),
        ("2026-07-11", "COIN", "USD"): _rate("2026-07-11", "COIN", "USD", "2.5"),
        ("2026-07-11", "USD", "JPY"): _rate("2026-07-11", "USD", "JPY", "151"),
    }

    value = value_reward_events([event], rates)[0]

    assert value.fair_value_jpy == Decimal("800")
    assert value.valuation_method == "daily_close_direct_jpy"


def test_missing_asset_rate_is_explicit():
    event = RewardEvent("r4", "2026-07-11", "UNKNOWN", Decimal("1"))
    value = value_reward_events([event], {})[0]

    assert value.fair_value_jpy is None
    assert value.status == "missing_asset_rate"


def test_cli_value_rewards(tmp_path):
    output = tmp_path / "valued_rewards.csv"

    exit_code = main(
        [
            "value-rewards",
            "examples/sample_reward_events.csv",
            "--asset-rates",
            "examples/sample_asset_daily_rates.csv",
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    text = output.read_text(encoding="utf-8-sig")
    assert "fair_value_jpy" in text
    assert "3775" in text
    assert "provisional_daily_close" in text


def test_sample_loaders():
    events = load_reward_events("examples/sample_reward_events.csv")
    rates = load_asset_daily_rates("examples/sample_asset_daily_rates.csv")

    assert events[0].asset == "COIN"
    assert rates[("2026-07-11", "COIN", "USD")].close == Decimal("2.50")
