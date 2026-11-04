#!/usr/bin/env python3
"""Crack spread proxy: US product spot minus Brent (NOT a European margin).

GET /api/margins/proxy
Without a key: at most 1,000 rows per read.
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/margins-proxy.csv. One request, no retry.

Options:
  --product: diesel (NYH ULSD), gasoline (NYH), jet (USGC).
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --freq: day, or week = Weekly Oil Bulletin week (Mon-Sun).
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python margins_proxy.py --product gasoline --freq day
"""

import argparse

import fuelorigin

ROUTE_ID = "margins-proxy"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--product",
        choices=("diesel", "gasoline", "jet"),
        default="diesel",
        help="diesel (NYH ULSD), gasoline (NYH), jet (USGC).",
    )
    parser.add_argument(
        "--from",
        dest="from_",
        default=fuelorigin.months_ago(6),
        help="First day, YYYY-MM-DD.",
    )
    parser.add_argument("--to", help="Last day, YYYY-MM-DD.")
    parser.add_argument(
        "--freq",
        choices=("day", "week"),
        default="week",
        help="day, or week = Weekly Oil Bulletin week (Mon-Sun).",
    )
    parser.add_argument("--limit", type=int, default=500, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv("/api/margins/proxy", {
        "product": args.product,
        "from": args.from_,
        "to": args.to,
        "freq": args.freq,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
