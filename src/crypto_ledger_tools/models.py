from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


VALID_SIDES = {"buy", "sell"}


@dataclass(frozen=True)
class NormalizedTransaction:
    tx_id: str
    timestamp: str
    asset: str
    side: str
    quantity: Decimal
    total_value: Decimal
    fee: Decimal
    quote_currency: str
    note: str = ""

    @property
    def net_quote_value(self) -> Decimal:
        if self.side == "buy":
            return self.total_value + self.fee
        return self.total_value - self.fee

    @property
    def unit_price(self) -> Decimal:
        if self.quantity == 0:
            return Decimal("0")
        return self.total_value / self.quantity


def parse_decimal(value: str, field_name: str) -> Decimal:
    try:
        amount = Decimal(str(value).strip())
    except Exception as exc:
        raise ValueError(f"{field_name} must be a decimal number") from exc
    if amount < 0:
        raise ValueError(f"{field_name} must not be negative")
    return amount


def normalize_row(row: dict[str, str]) -> NormalizedTransaction:
    required = [
        "tx_id",
        "timestamp",
        "asset",
        "side",
        "quantity",
        "total_value",
        "fee",
        "quote_currency",
    ]
    missing = [name for name in required if name not in row or row[name] == ""]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    side = row["side"].strip().lower()
    if side not in VALID_SIDES:
        raise ValueError("side must be buy or sell")

    quantity = parse_decimal(row["quantity"], "quantity")
    if quantity <= 0:
        raise ValueError("quantity must be greater than zero")

    asset = row["asset"].strip().upper()
    quote_currency = row["quote_currency"].strip().upper()
    if not asset:
        raise ValueError("asset must not be empty")
    if not quote_currency:
        raise ValueError("quote_currency must not be empty")

    return NormalizedTransaction(
        tx_id=row["tx_id"].strip(),
        timestamp=row["timestamp"].strip(),
        asset=asset,
        side=side,
        quantity=quantity,
        total_value=parse_decimal(row["total_value"], "total_value"),
        fee=parse_decimal(row["fee"], "fee"),
        quote_currency=quote_currency,
        note=row.get("note", "").strip(),
    )
