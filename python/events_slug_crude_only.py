#!/usr/bin/env python3
"""Stored crude-only path around an event (T0-4 to T0+13 bulletin weeks).

GET /api/events/{slug}/crude-only
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per bulletin week around the event.

Writes out/events-slug-crude-only.csv. One request, no retry.

Options:
  --slug: The event's page name, for example hormuz-2026.
  --country: Country slug.
  --fuel: EURO_SUPER_95 or DIESEL.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python events_slug_crude_only.py --country france --fuel DIESEL
"""

import argparse

import fuelorigin

ROUTE_ID = "events-slug-crude-only"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="hormuz-2026",
        help="The event's page name, for example hormuz-2026.",
    )
    parser.add_argument("--country", default="germany", help="Country slug.")
    parser.add_argument("--fuel", choices=("EURO_SUPER_95", "DIESEL"), help="EURO_SUPER_95 or DIESEL.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/events/{fuelorigin.path_part(args.slug)}/crude-only", {"country": args.country, "fuel": args.fuel, "lang": args.lang})
    data = answer["data"]

    # One row per bulletin week around the event.
    rows = [
        {"event": data["event"]["slug"], "country": data["country"]["slug"], "fuel_type": data["fuel_type"],
         "status": data["status"], "data_class": data["data_class"], "confidence": data["confidence"], **point}
        for point in data["points"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
