#!/usr/bin/env python3
"""One refinery.

GET /api/refineries/{slug}
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row: the refinery.

Writes out/refineries-slug.csv. One request, no retry.

Options:
  --slug: The refinery's page name, for example miro-karlsruhe.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python refineries_slug.py
"""

import argparse

import fuelorigin

ROUTE_ID = "refineries-slug"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="miro-karlsruhe",
        help="The refinery's page name, for example miro-karlsruhe.",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/refineries/{fuelorigin.path_part(args.slug)}", {"lang": args.lang})
    data = answer["data"]

    # One row: the refinery.
    rows = [data]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
