#!/usr/bin/env python3
"""Crude imports by grade: volume, CIF value and price, quality (key holders only).

GET /api/crude-import-cost
For key holders: without FO_KEY the script says so and stops, without calling the API.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/crude-import-cost.csv. One request, no retry.

Options:
  --country: Reporting country, ISO 3166-1 alpha-2 (GR, GB), or EU_V for the EU aggregate.
  --grade: Eurostat crude code, e.g.
  --indicator: One of the six published indicators.
  --origin: Production country named by the grade's label, ISO 3166-1 alpha-2.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python crude_import_cost.py --country GR --indicator VOL_THS_BBL
"""

import argparse

import fuelorigin

ROUTE_ID = "crude-import-cost"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--country",
        default="DE",
        help="Reporting country, ISO 3166-1 alpha-2 (GR, GB), or EU_V for the EU aggregate.",
    )
    parser.add_argument("--grade", default="TOTAL", help="Eurostat crude code, e.g.")
    parser.add_argument(
        "--indicator",
        choices=("VOL_THS_BBL", "VAL_THS_USD", "AVGPRC_USD_BBL", "API_DEG", "SULPH_PC", "CMPY_NR"),
        default="AVGPRC_USD_BBL",
        help="One of the six published indicators.",
    )
    parser.add_argument("--origin", help="Production country named by the grade's label, ISO 3166-1 alpha-2.")
    parser.add_argument(
        "--from",
        dest="from_",
        default=fuelorigin.months_ago(12),
        help="First day, YYYY-MM-DD.",
    )
    parser.add_argument("--to", help="Last day, YYYY-MM-DD.")
    parser.add_argument("--limit", type=int, default=500, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    fuelorigin.require_key(ROUTE_ID)

    file = fuelorigin.get_csv("/api/crude-import-cost", {
        "country": args.country,
        "grade": args.grade,
        "indicator": args.indicator,
        "origin": args.origin,
        "from": args.from_,
        "to": args.to,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
