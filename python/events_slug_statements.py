#!/usr/bin/env python3
"""The fixed-template sentences for one event.

GET /api/events/{slug}/statements
Without a key: at most 1,000 rows per read.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/events-slug-statements.csv. One request, no retry.

Options:
  --slug: The event's page name, for example hormuz-2026.
  --country: Only this country, by its slug.
  --topic: Only sentences on this topic, as the answer's rows state it.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python events_slug_statements.py --country france
"""

import argparse

import fuelorigin

ROUTE_ID = "events-slug-statements"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="hormuz-2026",
        help="The event's page name, for example hormuz-2026.",
    )
    parser.add_argument("--country", default="germany", help="Only this country, by its slug.")
    parser.add_argument("--topic", help="Only sentences on this topic, as the answer's rows state it.")
    parser.add_argument("--limit", type=int, default=500, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/events/{fuelorigin.path_part(args.slug)}/statements", {
        "country": args.country,
        "topic": args.topic,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
