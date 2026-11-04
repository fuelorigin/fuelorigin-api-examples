#!/usr/bin/env python3
"""One month's EU crude imports: five sentences and a chart's figures.

GET /api/statistics/eu-crude-oil-imports/months/{period}
Without a key the API answers the last 24 months; full history needs a key.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per member state's line, or per headline sentence
with --table facts.

Writes out/statistics-eu-crude-oil-imports-months-period.csv. One request, no retry.

Options:
  --period: The month, YYYY-MM.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.
  --table: Which table of the answer: country_lines, facts.

Example:
  python statistics_eu_crude_oil_imports_months_period.py --period 2026-05 --table facts
"""

import argparse

import fuelorigin

ROUTE_ID = "statistics-eu-crude-oil-imports-months-period"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--period", default="2026-06", help="The month, YYYY-MM.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    parser.add_argument("--table", choices=("country_lines", "facts"), default="country_lines", help="Which table of the answer.")
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/statistics/eu-crude-oil-imports/months/{fuelorigin.path_part(args.period)}", {"lang": args.lang})
    data = answer["data"]

    # One row per member state's line, or per headline sentence with --table facts.
    if args.table == "country_lines":
        rows = data["country_lines"]
    else:
        rows = data["facts"]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
