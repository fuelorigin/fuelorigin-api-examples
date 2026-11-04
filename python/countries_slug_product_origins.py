#!/usr/bin/env python3
"""Refined-product imports by partner country, monthly tonnes and shares.

GET /api/countries/{slug}/product-origins
Without a key: at most 1,500 rows per read.
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/countries-slug-product-origins.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --basis: Default: energy; for a covered country outside the EU, the basis of its own rows
      (Switzerland: customs_origin).
  --family: One product family: AUTOMOTIVE_DIESEL, BITUMEN, FUEL_OIL, GASOIL, JET_KEROSENE, LPG,
      LUBRICANTS, MOTOR_GASOLINE, NAPHTHA, OTHER.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --include_zero: false (default): only rows with a reported quantity or share above zero.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_product_origins.py --slug netherlands --family MOTOR_GASOLINE
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-product-origins"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--basis",
        choices=("energy", "customs", "customs_value_estimated", "customs_origin", "unknown"),
        help="Default: energy; for a covered country outside the EU, the basis of its own rows (Switzerland: customs_origin).",
    )
    parser.add_argument(
        "--family",
        default="AUTOMOTIVE_DIESEL",
        help="One product family: AUTOMOTIVE_DIESEL, BITUMEN, FUEL_OIL, GASOIL, JET_KEROSENE, LPG, LUBRICANTS, MOTOR_GASOLINE, NAPHTHA, OTHER.",
    )
    parser.add_argument(
        "--from",
        dest="from_",
        default=fuelorigin.months_ago(12),
        help="First day, YYYY-MM-DD.",
    )
    parser.add_argument("--to", help="Last day, YYYY-MM-DD.")
    parser.add_argument(
        "--include_zero",
        choices=("true", "false"),
        help="false (default): only rows with a reported quantity or share above zero.",
    )
    parser.add_argument("--limit", type=int, default=1000, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/countries/{fuelorigin.path_part(args.slug)}/product-origins", {
        "basis": args.basis,
        "family": args.family,
        "from": args.from_,
        "to": args.to,
        "include_zero": args.include_zero,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
