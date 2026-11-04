#!/usr/bin/env python3
"""Actual pre-tax price vs what crude alone would have done (computed on demand).

GET /api/countries/{slug}/crude-only
Without a key the API answers the last 24 months; full history needs a key.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per bulletin week.

Writes out/countries-slug-crude-only.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --fuel: EURO_SUPER_95 or DIESEL.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_crude_only.py --slug france --fuel DIESEL
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-crude-only"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument("--fuel", choices=("EURO_SUPER_95", "DIESEL"), help="EURO_SUPER_95 or DIESEL.")
    parser.add_argument("--from", dest="from_", help="First day, YYYY-MM-DD.")
    parser.add_argument("--to", help="Last day, YYYY-MM-DD.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/countries/{fuelorigin.path_part(args.slug)}/crude-only", {"fuel": args.fuel, "from": args.from_, "to": args.to, "lang": args.lang})
    data = answer["data"]

    # One row per bulletin week.
    rows = [
        {"country": data["country"]["slug"], "fuel_type": data["fuel_type"], "status": data["status"],
         "data_class": data["data_class"], "confidence": data["confidence"], **point}
        for point in data["points"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
