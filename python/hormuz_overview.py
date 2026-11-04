#!/usr/bin/env python3
"""Strait of Hormuz and EU oil: the eight dimensions, EU-wide and per member state.

GET /api/hormuz-overview
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per member state: its crude and product readings
and its sentence. Each range stays a range. The EU-wide block and the eight dimensions stay in the
JSON.

Writes out/hormuz-overview.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python hormuz_overview.py
"""

import argparse

import fuelorigin

ROUTE_ID = "hormuz-overview"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/hormuz-overview", {"lang": args.lang})
    data = answer["data"]

    # One row per member state: its crude and product readings and its sentence. Each range stays a
    # range. The EU-wide block and the eight dimensions stay in the JSON.
    rows = [
        {"period": data["period"], "country": c["country"], "crude": c["crude"], "product": c["product"],
         "inventory_days": c["inventory_days"], "statement": (c.get("statement") or {}).get("text")}
        for c in data["countries"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
