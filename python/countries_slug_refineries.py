#!/usr/bin/env python3
"""Refineries in one country, with cited capacity and status.

GET /api/countries/{slug}/refineries
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/countries-slug-refineries.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --status: Only rows with this status, as the answer's rows state it.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_refineries.py --slug italy
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-refineries"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument("--status", help="Only rows with this status, as the answer's rows state it.")
    parser.add_argument("--limit", type=int, default=100, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/countries/{fuelorigin.path_part(args.slug)}/refineries", {
        "status": args.status,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
