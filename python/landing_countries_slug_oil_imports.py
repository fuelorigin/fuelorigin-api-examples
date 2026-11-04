#!/usr/bin/env python3
"""A country's crude and refined-product imports by year and origin, since 2015.

GET /api/landing/countries/{slug}/oil-imports
Without a key the API answers the last 24 months; full history needs a key.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per crude origin in the year. Refined products and
the monthly series stay in the JSON.

Writes out/landing-countries-slug-oil-imports.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --basis: energy = energy statistics (default): crude by country of production, refined products
      by country of last consignment; customs = country of consignment; customs_origin = customs
      statistics by country of origin (covered countries outside the EU: Switzerland).
  --year: The value of year.
  --family: Product family for the monthly share series.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python landing_countries_slug_oil_imports.py --slug poland --year 2025
"""

import argparse

import fuelorigin

ROUTE_ID = "landing-countries-slug-oil-imports"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--basis",
        choices=("energy", "customs", "customs_origin"),
        help="energy = energy statistics (default): crude by country of production, refined products by country of last consignment; customs = country of consignment; customs_origin = customs statistics by country of origin (covered countries outside the EU: Switzerland).",
    )
    parser.add_argument("--year", type=int, help="The value of year.")
    parser.add_argument("--family", help="Product family for the monthly share series.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/landing/countries/{fuelorigin.path_part(args.slug)}/oil-imports", {
        "basis": args.basis,
        "year": args.year,
        "family": args.family,
        "lang": args.lang,
    })
    data = answer["data"]

    # One row per crude origin in the year. Refined products and the monthly series stay in the
    # JSON.
    rows = [
        {"country": data["country"]["slug"], "year": data["year"], "basis": data["basis"],
         "months_reported": data["crude"]["months_reported"],
         "months_not_published": data["crude"]["months_not_published"], **origin}
        for origin in data["crude"]["origins"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
