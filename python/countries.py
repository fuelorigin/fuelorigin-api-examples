#!/usr/bin/env python3
"""The list of countries the API knows, with the slugs other routes take.

GET /api/countries
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/countries.csv. One request, no retry.

Options:
  --eu_only: true: only EU member states.
  --covered_only: true: only the countries the site covers. On 2026-11-04 the API refused this file
      (403): it holds the United States row, whose population's licence is not established yet.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries.py --limit 50
"""

import argparse

import fuelorigin

ROUTE_ID = "countries"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--eu_only",
        choices=("true", "false"),
        help="true: only EU member states.",
    )
    parser.add_argument(
        "--covered_only",
        choices=("true", "false"),
        help="true: only the countries the site covers. On 2026-11-04 the API refused this file (403).",
    )
    parser.add_argument("--limit", type=int, default=100, help="Rows in this one read. A read reaching the United States row was refused on 2026-11-04 (403).")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv("/api/countries", {
        "eu_only": args.eu_only,
        "covered_only": args.covered_only,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
