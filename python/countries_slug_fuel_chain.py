#!/usr/bin/env python3
"""The crude behind this country's fuel (one-level look-through).

GET /api/countries/{slug}/fuel-chain
Without a key the API answers the last 24 months; full history needs a key.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per crude origin behind the fuel. Each origin's
Hormuz figures come as a range; none is a midpoint unless the API states a point.

Writes out/countries-slug-fuel-chain.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --product: Product family.
  --period: YYYY-MM.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_fuel_chain.py --slug estonia --product MOTOR_GASOLINE
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-fuel-chain"


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
        help="Product family.",
    )
    parser.add_argument("--period", help="YYYY-MM.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/countries/{fuelorigin.path_part(args.slug)}/fuel-chain", {"product": args.product, "period": args.period, "lang": args.lang})
    data = answer["data"]

    # One row per crude origin behind the fuel. Each origin's Hormuz figures come as a range; none
    # is a midpoint unless the API states a point.
    rows = [
        {"country": data["country"]["slug"], "product_family": data["product_family"], "period": data["period"],
         "status": data["status"], **origin}
        for origin in data["embedded_crude"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
