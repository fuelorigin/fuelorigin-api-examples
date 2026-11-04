#!/usr/bin/env python3
"""Our public log of revisions and corrections.

GET /api/corrections
Without a key: at most 50,000 rows per read.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/corrections.csv. One request, no retry.

Options:
  --kind: publisher_revision, publisher_completion, publisher_withdrawal, method_change,
      our_correction, withheld_zero or unclassified.
  --source_id: Only this dataset, by its id in GET /api/sources.
  --country: ISO two-letter code of the record's country.
  --from: Corrected on or after this day, YYYY-MM-DD.
  --to: Corrected on or before this day, YYYY-MM-DD.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python corrections.py --country DE --kind publisher_revision
"""

import argparse

import fuelorigin

ROUTE_ID = "corrections"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--kind",
        choices=("publisher_revision", "publisher_completion", "publisher_withdrawal", "method_change", "our_correction", "withheld_zero", "unclassified"),
        help="publisher_revision, publisher_completion, publisher_withdrawal, method_change, our_correction, withheld_zero or unclassified.",
    )
    parser.add_argument("--source_id", help="Only this dataset, by its id in GET /api/sources.")
    parser.add_argument("--country", help="ISO two-letter code of the record's country.")
    parser.add_argument("--from", dest="from_", help="Corrected on or after this day, YYYY-MM-DD.")
    parser.add_argument("--to", help="Corrected on or before this day, YYYY-MM-DD.")
    parser.add_argument("--limit", type=int, default=100, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv("/api/corrections", {
        "kind": args.kind,
        "source_id": args.source_id,
        "country": args.country,
        "from": args.from_,
        "to": args.to,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
