#!/usr/bin/env python3
"""Latest weekly petrol and diesel prices, tax share and price split, every member state.

GET /api/landing/eu-pump-prices
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per member state and fuel.

Writes out/landing-eu-pump-prices.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python landing_eu_pump_prices.py
"""

import argparse

import fuelorigin

ROUTE_ID = "landing-eu-pump-prices"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/landing/eu-pump-prices", {"lang": args.lang})
    data = answer["data"]

    # One row per member state and fuel.
    rows = [
        {"country": row["country"], **fuel}
        for row in data["rows"]
        for fuel in row["fuels"].values()
        if fuel
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
