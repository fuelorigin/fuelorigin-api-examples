#!/usr/bin/env python3
"""Crude imports into EU member states by producing country (country to country).

GET /api/map/flows
Without a key the API answers the last 24 months; full history needs a key.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per origin and destination. Country to country: not
a shipping route.

Writes out/map-flows.csv. One request, no retry.

Options:
  --commodity: The value of commodity.
  --period: YYYY-MM.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python map_flows.py --period 2026-03
"""

import argparse

import fuelorigin

ROUTE_ID = "map-flows"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--commodity", choices=("crude",), help="The value of commodity.")
    parser.add_argument("--period", help="YYYY-MM.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/map/flows", {"commodity": args.commodity, "period": args.period, "lang": args.lang})
    data = answer["data"]

    # One row per origin and destination. Country to country: not a shipping route.
    rows = [
        {"commodity": data["commodity"], "period": data["period"], "basis": data["basis"],
         "unit": data["unit"], **flow}
        for flow in data["flows"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
