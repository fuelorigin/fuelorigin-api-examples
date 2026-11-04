#!/usr/bin/env python3
"""The event-study window table.

GET /api/events/{slug}/study
Without a key: at most 1,000 rows per read.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/events-slug-study.csv. One request, no retry.

Options:
  --slug: The event's page name, for example hormuz-2026.
  --country: Only this country, by its slug.
  --fuel: The fuel code. Other values are rejected.
  --series: Only this series code, as the answer's rows state it.
  --status: Only rows with this status, as the answer's rows state it.
  --same_observation: false drops offsets that resolve to the same print as the start of the
      event.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python events_slug_study.py --country france --fuel DIESEL
"""

import argparse

import fuelorigin

ROUTE_ID = "events-slug-study"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="hormuz-2026",
        help="The event's page name, for example hormuz-2026.",
    )
    parser.add_argument("--country", default="germany", help="Only this country, by its slug.")
    parser.add_argument(
        "--fuel",
        choices=("EURO_SUPER_95", "DIESEL", "HEATING_GASOIL", "LPG_MOTOR", "FUEL_OIL_1", "FUEL_OIL_2", "RESIDUAL_FUEL_OIL", "OTHER", "REGULAR_GASOLINE_US"),
        help="The fuel code. Other values are rejected.",
    )
    parser.add_argument("--series", help="Only this series code, as the answer's rows state it.")
    parser.add_argument("--status", help="Only rows with this status, as the answer's rows state it.")
    parser.add_argument(
        "--same_observation",
        choices=("true", "false"),
        help="false drops offsets that resolve to the same print as the start of the event.",
    )
    parser.add_argument("--limit", type=int, default=500, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/events/{fuelorigin.path_part(args.slug)}/study", {
        "country": args.country,
        "fuel": args.fuel,
        "series": args.series,
        "status": args.status,
        "same_observation": args.same_observation,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
