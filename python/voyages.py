#!/usr/bin/env python3
"""Observed tanker voyages: a departure from a Norwegian oil terminal linked to the ship's next
recorded port call in Finland (estimate; no cargo).

GET /api/voyages
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per observed voyage: an estimate, with no cargo
known.

Writes out/voyages.csv. One request, no retry.

Options:
  --destination_country: Country slug, e.g.
  --origin_country: Country slug, e.g.
  --limit: Rows in this one read.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python voyages.py --destination_country finland
"""

import argparse

import fuelorigin

ROUTE_ID = "voyages"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--destination_country", help="Country slug, e.g.")
    parser.add_argument("--origin_country", help="Country slug, e.g.")
    parser.add_argument("--limit", type=int, default=50, help="Rows in this one read.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/voyages", {
        "destination_country": args.destination_country,
        "origin_country": args.origin_country,
        "limit": args.limit,
        "lang": args.lang,
    })
    data = answer["data"]

    # One row per observed voyage: an estimate, with no cargo known.
    rows = data["voyages"]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
