#!/usr/bin/env python3
"""Your key's usage this month (key holders only).

GET /api/account/usage
For key holders: without FO_KEY the script says so and stops, without calling the API.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row: your key's use this month.

Writes out/account-usage.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python account_usage.py
"""

import argparse

import fuelorigin

ROUTE_ID = "account-usage"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    fuelorigin.require_key(ROUTE_ID)

    answer = fuelorigin.get_json("/api/account/usage", {"lang": args.lang})
    data = answer["data"]

    # One row: your key's use this month.
    rows = [answer["data"]]
    fuelorigin.save_rows(ROUTE_ID, rows, answer, own_bookkeeping=True)


if __name__ == "__main__":
    main()
