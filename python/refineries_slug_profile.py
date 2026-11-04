#!/usr/bin/env python3
"""Everything the refinery page shows: site facts, connections, national context.

GET /api/refineries/{slug}/profile
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row: the site facts, capacity and cited pages.
Connections and the national context stay in the JSON.

Writes out/refineries-slug-profile.csv. One request, no retry.

Options:
  --slug: The refinery's page name, for example miro-karlsruhe.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python refineries_slug_profile.py
"""

import argparse

import fuelorigin

ROUTE_ID = "refineries-slug-profile"


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

    answer = fuelorigin.get_json(f"/api/refineries/{fuelorigin.path_part(args.slug)}/profile", {"lang": args.lang})
    data = answer["data"]

    # One row: the site facts, capacity and cited pages. Connections and the national context stay
    # in the JSON.
    rows = [{"refinery": data["refinery"], "capacity": data["capacity"], "citations": data.get("citations")}]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
