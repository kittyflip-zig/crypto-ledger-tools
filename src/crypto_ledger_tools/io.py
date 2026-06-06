from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from .models import NormalizedTransaction, normalize_row


FIELD_NAMES = [
    "tx_id",
    "timestamp",
    "asset",
    "side",
    "quantity",
    "total_value",
    "fee",
    "quote_currency",
    "note",
]


def load_transactions(path: str | Path) -> list[NormalizedTransaction]:
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [normalize_row(row) for row in reader]


def write_normalized_csv(
    transactions: Iterable[NormalizedTransaction],
    path: str | Path,
) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for tx in transactions:
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
                }
            )
