from __future__ import annotations

import argparse
from pathlib import Path

from .exchange_adapters import load_exchange_transactions
from .io import load_transactions, write_normalized_csv
from .jpy import build_jpy_views, write_jpy_csv
from .rates import load_daily_rates
from .report import build_markdown_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="crypto-ledger-tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    normalize_parser = subparsers.add_parser("normalize")
    normalize_parser.add_argument("input_csv")
    normalize_parser.add_argument("--output", required=True)

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("input_csv")
    report_parser.add_argument("--output", required=True)

    jpy_parser = subparsers.add_parser("jpy")
    jpy_parser.add_argument("input_csv")
    jpy_parser.add_argument("--rates", required=True)
    jpy_parser.add_argument("--output", required=True)

    exchange_parser = subparsers.add_parser("exchange-normalize")
    exchange_parser.add_argument("input_csv")
    exchange_parser.add_argument("--output", required=True)

    args = parser.parse_args(argv)
    transactions = (
        load_exchange_transactions(args.input_csv)
        if args.command == "exchange-normalize"
        else load_transactions(args.input_csv)
    )

    if args.command == "normalize":
        write_normalized_csv(transactions, args.output)
        return 0

    if args.command == "report":
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(build_markdown_report(transactions), encoding="utf-8")
        return 0

    if args.command == "jpy":
        rates = load_daily_rates(args.rates)
        write_jpy_csv(build_jpy_views(transactions, rates), args.output)
        return 0

    if args.command == "exchange-normalize":
        write_normalized_csv(transactions, args.output)
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
