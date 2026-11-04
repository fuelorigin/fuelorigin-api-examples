#!/usr/bin/env python3
"""Crude oil imports by partner country, monthly tonnes and shares.

GET /api/countries/{slug}/crude-origins
Without a key: at most 1,000 rows per read.
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/countries-slug-crude-origins.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --basis: energy = true origin as energy statistics report it; customs = country of consignment
      or dispatch.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --include_zero: false (default): only rows with a reported quantity or share above zero.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_crude_origins.py --slug france --from 2026-01-01
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-crude-origins"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--basis",
        choices=("energy", "customs", "customs_value_estimated", "customs_origin", "unknown"),
        help="energy = true origin as energy statistics report it; customs = country of consignment or dispatch.",
    )
    parser.add_argument(
        "--from",
        dest="from_",
        default=fuelorigin.months_ago(12),
        help="First day, YYYY-MM-DD.",
    )
    parser.add_argument("--to", help="Last day, YYYY-MM-DD.")
    parser.add_argument(
        "--include_zero",
        choices=("true", "false"),
        help="false (default): only rows with a reported quantity or share above zero.",
    )
    parser.add_argument("--limit", type=int, default=1000, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/countries/{fuelorigin.path_part(args.slug)}/crude-origins", {
        "basis": args.basis,
        "from": args.from_,
        "to": args.to,
        "include_zero": args.include_zero,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
