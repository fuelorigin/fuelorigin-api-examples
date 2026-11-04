#!/usr/bin/env python3
"""One-line facts with citations for one statistics page.

GET /api/statistics/{slug}
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per line, each with its ready-to-paste citation.

Writes out/statistics-slug.csv. One request, no retry.

Options:
  --slug: The statistics page, for example eu-crude-oil-imports.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python statistics_slug.py --slug strait-of-hormuz-europe
"""

import argparse

import fuelorigin

ROUTE_ID = "statistics-slug"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="eu-crude-oil-imports",
        help="The statistics page, for example eu-crude-oil-imports.",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/statistics/{fuelorigin.path_part(args.slug)}", {"lang": args.lang})
    data = answer["data"]

    # One row per line, each with its ready-to-paste citation.
    rows = data["facts"]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
