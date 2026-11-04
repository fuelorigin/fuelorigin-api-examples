#!/usr/bin/env python3
"""Days of cover by product, our calculation (key holders only).

GET /api/stock-cover-by-product
For key holders: without FO_KEY the script says so and stops, without calling the API.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/stock-cover-by-product.csv. One request, no retry.

Options:
  --country: Member state, ISO 3166-1 alpha-2 (DE, GR), or EU27_2020 for the EU aggregate.
  --product: One product.
  --basis: One stock basis.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python stock_cover_by_product.py --country DE --product PETROL
"""

import argparse

import fuelorigin

ROUTE_ID = "stock-cover-by-product"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--country",
        default="EE",
        help="Member state, ISO 3166-1 alpha-2 (DE, GR), or EU27_2020 for the EU aggregate.",
    )
    parser.add_argument(
        "--product",
        choices=("DIESEL_GASOIL", "ROAD_DIESEL", "JET_KEROSENE", "PETROL"),
        default="ROAD_DIESEL",
        help="One product.",
    )
    parser.add_argument(
        "--basis",
        choices=("EMERGENCY", "ALL_STOCKS"),
        default="EMERGENCY",
        help="One stock basis.",
    )
    parser.add_argument(
        "--from",
        dest="from_",
        default=fuelorigin.months_ago(12),
        help="First day, YYYY-MM-DD.",
    )
    parser.add_argument("--to", help="Last day, YYYY-MM-DD.")
    parser.add_argument("--limit", type=int, default=500, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    fuelorigin.require_key(ROUTE_ID)

    file = fuelorigin.get_csv("/api/stock-cover-by-product", {
        "country": args.country,
        "product": args.product,
        "basis": args.basis,
        "from": args.from_,
        "to": args.to,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
