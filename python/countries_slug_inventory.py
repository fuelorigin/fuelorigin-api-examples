#!/usr/bin/env python3
"""Monthly oil stocks and the published days of cover.

GET /api/countries/{slug}/inventory
Without a key: at most 500 rows per read.
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/countries-slug-inventory.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --siec: Only this product code, as the answer's rows state it.
  --holder: Only this stock holder code, as the answer's rows state it.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_inventory.py --slug estonia
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-inventory"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--from",
        dest="from_",
        default=fuelorigin.months_ago(12),
        help="First day, YYYY-MM-DD.",
    )
    parser.add_argument("--to", help="Last day, YYYY-MM-DD.")
    parser.add_argument("--siec", help="Only this product code, as the answer's rows state it.")
    parser.add_argument("--holder", help="Only this stock holder code, as the answer's rows state it.")
    parser.add_argument("--limit", type=int, default=500, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/countries/{fuelorigin.path_part(args.slug)}/inventory", {
        "from": args.from_,
        "to": args.to,
        "siec": args.siec,
        "holder": args.holder,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
