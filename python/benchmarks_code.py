#!/usr/bin/env python3
"""One benchmark's definition and its quotes, at their own granularity.

GET /api/benchmarks/{code}
Without a key: at most 1,000 rows per read.
Without a key the API answers the last 24 months; full history needs a key.
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/benchmarks-code.csv. One request, no retry.

Options:
  --code: The benchmark's code, for example BRENT_SPOT_FOB.
  --from: First day, YYYY-MM-DD.
  --to: Last day, YYYY-MM-DD.
  --limit: Rows in this one read.
  --offset: Rows to skip.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python benchmarks_code.py --code BRENT_SPOT_FOB --from 2026-09-01
"""

import argparse

import fuelorigin

ROUTE_ID = "benchmarks-code"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--code",
        default="BRENT_SPOT_FOB",
        help="The benchmark's code, for example BRENT_SPOT_FOB.",
    )
    parser.add_argument(
        "--from",
        dest="from_",
        default=fuelorigin.months_ago(3),
        help="First day, YYYY-MM-DD.",
    )
    parser.add_argument("--to", help="Last day, YYYY-MM-DD.")
    parser.add_argument("--limit", type=int, default=500, help="Rows in this one read.")
    parser.add_argument("--offset", type=int, help="Rows to skip.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/benchmarks/{fuelorigin.path_part(args.code)}", {
        "from": args.from_,
        "to": args.to,
        "limit": args.limit,
        "offset": args.offset,
        "lang": args.lang,
    })
    fuelorigin.save_csv(ROUTE_ID, file, limit=args.limit)


if __name__ == "__main__":
    main()
