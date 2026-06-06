from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .models import NormalizedTransaction


@dataclass(frozen=True)
class AssetSummary:
    asset: str
    quote_currency: str
    acquired_quantity: Decimal
    disposed_quantity: Decimal
    remaining_quantity: Decimal
    remaining_cost: Decimal
    average_cost: Decimal
    realized_pnl: Decimal


def calculate_average_cost(
    transactions: list[NormalizedTransaction],
) -> dict[str, AssetSummary]:
    state: dict[str, dict[str, Decimal | str]] = {}

    for tx in sorted(transactions, key=lambda item: (item.timestamp, item.tx_id)):
        current = state.setdefault(
            tx.asset,
            {
                "quote_currency": tx.quote_currency,
                "quantity": Decimal("0"),
                "cost": Decimal("0"),
                "acquired": Decimal("0"),
                "disposed": Decimal("0"),
                "realized_pnl": Decimal("0"),
            },
        )
        if current["quote_currency"] != tx.quote_currency:
            raise ValueError(f"mixed quote_currency values for {tx.asset}")

        quantity = current["quantity"]
        cost = current["cost"]
        if not isinstance(quantity, Decimal) or not isinstance(cost, Decimal):
            raise TypeError("internal calculator state is invalid")

        if tx.side == "buy":
            current["quantity"] = quantity + tx.quantity
            current["cost"] = cost + tx.net_quote_value
            current["acquired"] = current["acquired"] + tx.quantity
            continue

        if tx.quantity > quantity:
            raise ValueError(f"sell quantity exceeds remaining quantity for {tx.asset}")

        average_cost = Decimal("0") if quantity == 0 else cost / quantity
        basis = average_cost * tx.quantity
        current["quantity"] = quantity - tx.quantity
        current["cost"] = cost - basis
        current["disposed"] = current["disposed"] + tx.quantity
        current["realized_pnl"] = current["realized_pnl"] + (tx.net_quote_value - basis)

    summaries: dict[str, AssetSummary] = {}
    for asset, values in state.items():
        remaining_quantity = values["quantity"]
        remaining_cost = values["cost"]
        if not isinstance(remaining_quantity, Decimal) or not isinstance(remaining_cost, Decimal):
            raise TypeError("internal calculator state is invalid")
        average_cost = (
            Decimal("0")
            if remaining_quantity == 0
            else remaining_cost / remaining_quantity
        )
        summaries[asset] = AssetSummary(
            asset=asset,
            quote_currency=str(values["quote_currency"]),
            acquired_quantity=_decimal(values["acquired"]),
            disposed_quantity=_decimal(values["disposed"]),
            remaining_quantity=remaining_quantity,
            remaining_cost=remaining_cost,
            average_cost=average_cost,
            realized_pnl=_decimal(values["realized_pnl"]),
        )
    return summaries


def _decimal(value: Decimal | str) -> Decimal:
    if not isinstance(value, Decimal):
        raise TypeError("internal calculator state is invalid")
    return value
