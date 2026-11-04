#!/usr/bin/env python3
"""One event, and which countries and series have a study.

GET /api/events/{slug}
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per series of the event study, or per country's run
with --table runs.

Writes out/events-slug.csv. One request, no retry.

Options:
  --slug: The event's page name, for example hormuz-2026.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.
  --table: Which table of the answer: series, runs.

Example:
  python events_slug.py --slug hormuz-2026 --table runs
"""

import argparse

import fuelorigin

ROUTE_ID = "events-slug"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="hormuz-2026",
        help="The event's page name, for example hormuz-2026.",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    parser.add_argument("--table", choices=("series", "runs"), default="series", help="Which table of the answer.")
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/events/{fuelorigin.path_part(args.slug)}", {"lang": args.lang})
    data = answer["data"]

    # One row per series of the event study, or per country's run with --table runs.
    if args.table == "series":
        rows = data["series"]
    else:
        rows = data["runs"]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
