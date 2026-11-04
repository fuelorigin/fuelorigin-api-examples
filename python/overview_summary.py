#!/usr/bin/env python3
"""The country-page headline for every EU member state, in one call.

GET /api/overview-summary
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per member state: its headline and latest price.

Writes out/overview-summary.csv. One request, no retry.

Options:
  --fuel: Fuel for the headline and the price.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python overview_summary.py --fuel petrol
"""

import argparse

import fuelorigin

ROUTE_ID = "overview-summary"

# This answer does not name its datasets, so the file's top lines cite the main one here.
CITE = [("Eurostat", "nrg_ti_oilm", "https://ec.europa.eu/eurostat/databrowser/view/nrg_ti_oilm/default/table?lang=en")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--fuel",
        choices=("road_diesel", "petrol", "jet"),
        help="Fuel for the headline and the price.",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/overview-summary", {"fuel": args.fuel, "lang": args.lang})
    data = answer["data"]

    # One row per member state: its headline and latest price.
    rows = data
    fuelorigin.save_rows(ROUTE_ID, rows, answer, cite=CITE)


if __name__ == "__main__":
    main()
