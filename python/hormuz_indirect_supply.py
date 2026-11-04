#!/usr/bin/env python3
"""Hormuz dimension D3 (estimate): crude that may have passed the strait inside fuel imported from
refineries outside the Gulf.

GET /api/hormuz/indirect-supply
Without a key the API answers the last 24 months; full history needs a key.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per member state and product family. Each range
stays a range.

Writes out/hormuz-indirect-supply.csv. One request, no retry.

Options:
  --period: YYYY-MM.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python hormuz_indirect_supply.py --period 2026-03
"""

import argparse

import fuelorigin

ROUTE_ID = "hormuz-indirect-supply"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--period", help="YYYY-MM.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/hormuz/indirect-supply", {"period": args.period, "lang": args.lang})
    data = answer["data"]

    # One row per member state and product family. Each range stays a range.
    rows = [
        {"period": data["period"], "country": c["country"], **family}
        for c in data["countries"]
        for family in c["families"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
