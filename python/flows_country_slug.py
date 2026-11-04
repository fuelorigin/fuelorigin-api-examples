#!/usr/bin/env python3
"""Sankey nodes and links: crude origin -> supplier -> this country's fuel.

GET /api/flows/country/{slug}
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/flows-country-slug.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --product: Fuel.
  --period: YYYY-MM.
  --limit: Rows in this one read.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python flows_country_slug.py --slug estonia --product MOTOR_GASOLINE
"""

import argparse

import fuelorigin

ROUTE_ID = "flows-country-slug"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--product",
        choices=("AUTOMOTIVE_DIESEL", "MOTOR_GASOLINE", "JET_KEROSENE"),
        help="Fuel.",
    )
    parser.add_argument("--period", help="YYYY-MM.")
    parser.add_argument("--limit", type=int, help="Rows in this one read.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/flows/country/{fuelorigin.path_part(args.slug)}", {
        "product": args.product,
        "period": args.period,
        "limit": args.limit,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
