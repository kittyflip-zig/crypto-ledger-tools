from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from .calculator import AssetSummary, calculate_average_cost
from .models import NormalizedTransaction


def build_markdown_report(transactions: list[NormalizedTransaction]) -> str:
    summaries = calculate_average_cost(transactions)
    lines = [
        "# Crypto Ledger Report",
        "",
        "This report is generated from user-supplied CSV rows. It is not tax, accounting, investment, or trading advice.",
        "",
        "| Asset | Quote | Acquired | Disposed | Remaining | Remaining Cost | Average Cost | Realized PnL |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries.values():
        lines.append(_summary_row(summary))
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Calculations use a simple moving average cost method.")
    lines.append("- Fees are added to acquisition cost for buys and deducted from proceeds for sells.")
    lines.append("- Review the output before using it in any external workflow.")
    return "\n".join(lines) + "\n"


def _summary_row(summary: AssetSummary) -> str:
    return (
        f"| {summary.asset} | {summary.quote_currency} | "
        f"{_fmt(summary.acquired_quantity)} | {_fmt(summary.disposed_quantity)} | "
        f"{_fmt(summary.remaining_quantity)} | {_fmt(summary.remaining_cost)} | "
        f"{_fmt(summary.average_cost)} | {_fmt(summary.realized_pnl)} |"
    )


def _fmt(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
