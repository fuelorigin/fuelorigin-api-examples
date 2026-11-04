#!/usr/bin/env python3
"""Strait of Hormuz exposure rows, by dimension and month.

GET /api/countries/{slug}/hormuz
Without a key: at most 1,000 rows per read.
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/countries-slug-hormuz.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --dimension: Only this dimension, for example DIRECT_CRUDE.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_hormuz.py --slug poland
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-hormuz"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--dimension",
        default="DIRECT_CRUDE",
        help="Only this dimension, for example DIRECT_CRUDE.",
    )
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

    file = fuelorigin.get_csv(f"/api/countries/{fuelorigin.path_part(args.slug)}/hormuz", {
        "dimension": args.dimension,
        "from": args.from_,
        "to": args.to,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
