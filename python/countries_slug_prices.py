#!/usr/bin/env python3
"""Weekly pump prices from the Weekly Oil Bulletin.

GET /api/countries/{slug}/prices
Without a key: at most 1,500 rows per read.
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/countries-slug-prices.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --fuel: The fuel code. Other values are rejected.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_prices.py --slug france --fuel EURO_SUPER_95
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-prices"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--fuel",
        choices=("EURO_SUPER_95", "DIESEL", "HEATING_GASOIL", "LPG_MOTOR", "FUEL_OIL_1", "FUEL_OIL_2", "RESIDUAL_FUEL_OIL", "OTHER", "REGULAR_GASOLINE_US"),
        default="DIESEL",
        help="The fuel code. Other values are rejected.",
    )
    parser.add_argument(
        "--from",
        dest="from_",
        default=fuelorigin.months_ago(6),
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

    file = fuelorigin.get_csv(f"/api/countries/{fuelorigin.path_part(args.slug)}/prices", {
        "fuel": args.fuel,
        "from": args.from_,
        "to": args.to,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
