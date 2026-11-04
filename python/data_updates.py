#!/usr/bin/env python3
"""Each new month of a publisher's dataset, with the moment it first reached us.

GET /api/data-updates
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per new month of a publisher's dataset.

Writes out/data-updates.csv. One request, no retry.

Options:
  --limit: Rows in this one read.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python data_updates.py --limit 10
"""

import argparse

import fuelorigin

ROUTE_ID = "data-updates"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--limit", type=int, default=50, help="Rows in this one read.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/data-updates", {"limit": args.limit, "lang": args.lang})
    data = answer["data"]

    # One row per new month of a publisher's dataset.
    rows = data
    fuelorigin.save_rows(ROUTE_ID, rows, answer, own_bookkeeping=True)


if __name__ == "__main__":
    main()
