#!/usr/bin/env python3
"""Sankey nodes and links: origin country -> importing EU member state.

GET /api/flows/eu
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/flows-eu.csv. One request, no retry.

Options:
  --commodity: crude, or a product family: AUTOMOTIVE_DIESEL, GASOIL, MOTOR_GASOLINE,
      JET_KEROSENE, FUEL_OIL, NAPHTHA, LPG.
  --period: YYYY-MM.
  --top: Origins with their own node.
  --limit: Rows in this one read.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python flows_eu.py --commodity AUTOMOTIVE_DIESEL --top 8
"""

import argparse

import fuelorigin

ROUTE_ID = "flows-eu"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--commodity",
        help="crude, or a product family: AUTOMOTIVE_DIESEL, GASOIL, MOTOR_GASOLINE, JET_KEROSENE, FUEL_OIL, NAPHTHA, LPG.",
    )
    parser.add_argument("--period", help="YYYY-MM.")
    parser.add_argument("--top", type=int, help="Origins with their own node.")
    parser.add_argument("--limit", type=int, help="Rows in this one read.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv("/api/flows/eu", {
        "commodity": args.commodity,
        "period": args.period,
        "top": args.top,
        "limit": args.limit,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
