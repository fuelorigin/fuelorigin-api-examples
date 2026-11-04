#!/usr/bin/env python3
"""Where the crude oil EU member states import comes from (energy basis).

GET /api/landing/eu-crude-sources
Without a key the API answers the last 24 months; full history needs a key.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per origin country in the latest month every member
state reported.

Writes out/landing-eu-crude-sources.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python landing_eu_crude_sources.py
"""

import argparse

import fuelorigin

ROUTE_ID = "landing-eu-crude-sources"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/landing/eu-crude-sources", {"lang": args.lang})
    data = answer["data"]

    # One row per origin country in the latest month every member state reported.
    rows = [
        {"period": data["period"], "eu_total_tonnes": data["eu_total_tonnes"],
         "untraceable_pct": data["untraceable_pct"], **origin}
        for origin in data["origins"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
