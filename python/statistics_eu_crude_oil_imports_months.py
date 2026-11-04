#!/usr/bin/env python3
"""The months that have a monthly crude import post.

GET /api/statistics/eu-crude-oil-imports/months
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per month with a post.

Writes out/statistics-eu-crude-oil-imports-months.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python statistics_eu_crude_oil_imports_months.py
"""

import argparse

import fuelorigin

ROUTE_ID = "statistics-eu-crude-oil-imports-months"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/statistics/eu-crude-oil-imports/months", {"lang": args.lang})
    data = answer["data"]

    # One row per month with a post.
    rows = data
    fuelorigin.save_rows(ROUTE_ID, rows, answer, own_bookkeeping=True)


if __name__ == "__main__":
    main()
