#!/usr/bin/env python3
"""Events: embargoes, tax changes, disruptions.

GET /api/events
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/events.csv. One request, no retry.

Options:
  --country: Only this country, by its slug.
  --event_type: Only events of this type, as the answer's rows state it.
  --status: Only rows with this status, as the answer's rows state it.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python events.py --country germany
"""

import argparse

import fuelorigin

ROUTE_ID = "events"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--country", help="Only this country, by its slug.")
    parser.add_argument("--event_type", help="Only events of this type, as the answer's rows state it.")
    parser.add_argument("--status", help="Only rows with this status, as the answer's rows state it.")
    parser.add_argument("--from", dest="from_", help="First day, YYYY-MM-DD.")
    parser.add_argument("--to", help="Last day, YYYY-MM-DD.")
    parser.add_argument("--limit", type=int, default=100, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv("/api/events", {
        "country": args.country,
        "event_type": args.event_type,
        "status": args.status,
        "from": args.from_,
        "to": args.to,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
