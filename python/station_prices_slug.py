#!/usr/bin/env python3
"""Pump prices at stations: latest-day distribution, regions, national median vs the bulletin.

GET /api/station-prices/{slug}
Without a key: --days at most 500.
Without a key the API answers the last 24 months; full history needs a key.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per region for the selected fuel, or per fuel with
--table fuels.

Writes out/station-prices-slug.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --fuel: Fuel for regions and series.
  --service: Service mode (Italy).
  --days: Series window in days.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.
  --table: Which table of the answer: regions, fuels.

Example:
  python station_prices_slug.py --slug italy --table fuels
"""

import argparse

import fuelorigin

ROUTE_ID = "station-prices-slug"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--slug", default="france", help="The page name in the address, for example germany.")
    parser.add_argument(
        "--fuel",
        choices=("PETROL_95_E5", "PETROL_95_E10", "PETROL_UNLEADED", "DIESEL", "LPG"),
        help="Fuel for regions and series.",
    )
    parser.add_argument("--service", choices=("self", "served", "not_stated"), help="Service mode (Italy).")
    parser.add_argument("--days", type=int, help="Series window in days.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    parser.add_argument("--table", choices=("regions", "fuels"), default="regions", help="Which table of the answer.")
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/station-prices/{fuelorigin.path_part(args.slug)}", {
        "fuel": args.fuel,
        "service": args.service,
        "days": args.days,
        "lang": args.lang,
    })
    data = answer["data"]

    # One row per region for the selected fuel, or per fuel with --table fuels.
    if args.table == "regions":
        rows = [{"latest_day": data["latest_day"], "selected": data["selected"], **region} for region in data["regions"]]
    else:
        rows = data["fuels"]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
