#!/usr/bin/env python3
"""Every published change of the EU and UK rules on fuel refined from Russian crude oil, with
before/after, versions and hashes (key holders only).

GET /api/rules/changes
For key holders: without FO_KEY the script says so and stops, without calling the API.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/rules-changes.csv. One request, no retry.

Options:
  --since: First UTC day of published_at (inclusive), YYYY-MM-DD.
  --until: Last UTC day of published_at (inclusive), YYYY-MM-DD.
  --list: One country list.
  --document: One document: its document_key, e.g.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python rules_changes.py --since 2026-01-01
"""

import argparse

import fuelorigin

ROUTE_ID = "rules-changes"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--since", help="First UTC day of published_at (inclusive), YYYY-MM-DD.")
    parser.add_argument("--until", help="Last UTC day of published_at (inclusive), YYYY-MM-DD.")
    parser.add_argument(
        "--list",
        choices=("EU_ANNEX_LI_PARTNER", "EU_FAQ_NET_EXPORTER", "UK_GUIDANCE_PARTNER", "UK_GUIDANCE_NET_EXPORTER"),
        default="EU_ANNEX_LI_PARTNER",
        help="One country list.",
    )
    parser.add_argument("--document", help="One document: its document_key, e.g.")
    parser.add_argument("--limit", type=int, default=100, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    fuelorigin.require_key(ROUTE_ID)

    file = fuelorigin.get_csv("/api/rules/changes", {
        "since": args.since,
        "until": args.until,
        "list": args.list,
        "document": args.document,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
