#!/usr/bin/env python3
"""Everything the first screen of a country page needs, one period per dataset.

GET /api/countries/{slug}/overview
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per largest crude origin on the country page's
first screen; the rest of the page stays in the JSON.

Writes out/countries-slug-overview.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --fuel: Fuel for the headline and the price link.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_overview.py --slug netherlands --fuel petrol
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-overview"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--fuel",
        choices=("road_diesel", "petrol", "jet"),
        help="Fuel for the headline and the price link.",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/countries/{fuelorigin.path_part(args.slug)}/overview", {"fuel": args.fuel, "lang": args.lang})
    data = answer["data"]

    # One row per largest crude origin on the country page's first screen; the rest of the page
    # stays in the JSON.
    rows = [
        {"country": data["country"]["slug"], "period": data["crude"]["period"], "basis": data["crude"]["basis"],
         "status": data["crude"]["status"], "other_share_pct": data["crude"]["other_share_pct"],
         "unattributed_share_pct": data["crude"]["unattributed_share_pct"], **origin}
        for origin in data["crude"]["top_origins"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
