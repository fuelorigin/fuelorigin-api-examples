#!/usr/bin/env python3
"""One country across the four lists over time, with the texts behind them and its refined-product
tonnes to the EU (key holders only).

GET /api/rules/countries/{iso2}
For key holders: without FO_KEY the script says so and stops, without calling the API.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per list the country was checked against. The
listings and quotes stay as JSON text in their cells.

Writes out/rules-countries-iso2.csv. One request, no retry.

Options:
  --iso2: ISO 3166-1 alpha-2, e.g.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python rules_countries_iso2.py --iso2 TR
"""

import argparse

import fuelorigin

ROUTE_ID = "rules-countries-iso2"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--iso2", default="NO", help="ISO 3166-1 alpha-2, e.g.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    fuelorigin.require_key(ROUTE_ID)

    answer = fuelorigin.get_json(f"/api/rules/countries/{fuelorigin.path_part(args.iso2)}", {"lang": args.lang})
    data = answer["data"]

    # One row per list the country was checked against. The listings and quotes stay as JSON text in
    # their cells.
    rows = [{"iso2": data["iso2"], "country_name": data["country_name"], **entry} for entry in data["lists"]]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
