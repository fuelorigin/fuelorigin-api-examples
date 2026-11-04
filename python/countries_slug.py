#!/usr/bin/env python3
"""One country's profile, and what the API holds for each dataset its pages draw.

GET /api/countries/{slug}
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per dataset: what the API holds for this country,
and from which sources.

Writes out/countries-slug.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug.py --slug poland
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/countries/{fuelorigin.path_part(args.slug)}", {"lang": args.lang})
    data = answer["data"]

    # One row per dataset: what the API holds for this country, and from which sources.
    rows = [{"country": data["country"]["slug"], **dataset} for dataset in data["datasets"]]
    fuelorigin.save_rows(ROUTE_ID, rows, answer, own_bookkeeping=True)


if __name__ == "__main__":
    main()
