#!/usr/bin/env python3
"""What one partner country supplies to the EU.

GET /api/origins/{slug}
Without a key: --months at most 60.
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/origins-slug.csv. One request, no retry.

Options:
  --slug: The partner country's page name, for example norway.
  --months: Chart window in months.
  --limit: Rows in this one read.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python origins_slug.py --slug kazakhstan --months 24
"""

import argparse

import fuelorigin

ROUTE_ID = "origins-slug"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="norway",
        help="The partner country's page name, for example norway.",
    )
    parser.add_argument("--months", type=int, default=12, help="Chart window in months.")
    parser.add_argument("--limit", type=int, help="Rows in this one read.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/origins/{fuelorigin.path_part(args.slug)}", {"months": args.months, "limit": args.limit, "lang": args.lang})
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
