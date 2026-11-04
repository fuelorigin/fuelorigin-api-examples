#!/usr/bin/env python3
"""Country comparison: overviews, monthly Hormuz exposure and the latest price week.

GET /api/compare
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per country: its status, latest price week and
headline. The monthly Hormuz series and the rest of each overview stay in the JSON (overview:
countries_slug_overview.py).

Writes out/compare.csv. One request, no retry.

Options:
  --countries: 1 to 6 country slugs, comma separated, in the order to show them.
  --fuel: Fuel for the headline and the price.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python compare.py --countries spain,italy --fuel petrol
"""

import argparse

import fuelorigin

ROUTE_ID = "compare"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--countries",
        default="germany,france,poland",
        help="1 to 6 country slugs, comma separated, in the order to show them.",
    )
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

    answer = fuelorigin.get_json("/api/compare", {"countries": args.countries, "fuel": args.fuel, "lang": args.lang})
    data = answer["data"]

    # One row per country: its status, latest price week and headline. The monthly Hormuz series and
    # the rest of each overview stay in the JSON (overview: countries_slug_overview.py).
    rows = [
        {"country": c["country"], "status": c["status"], "price": c.get("price"),
         "headline": (c.get("overview") or {}).get("headline")}
        for c in data["countries"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
