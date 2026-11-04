#!/usr/bin/env python3
"""Trace one value to the publisher's record and the file we downloaded.

GET /api/provenance/{observation_id}
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row: the trace of one value.

Writes out/provenance-observation-id.csv. One request, no retry.

Options:
  --observation_id: The id of one value, as a row's provenance_id states it.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python provenance_observation_id.py
"""

import argparse

import fuelorigin

ROUTE_ID = "provenance-observation-id"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--observation_id",
        default="core.trade_flow:81873",
        help="The id of one value, as a row's provenance_id states it.",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/provenance/{fuelorigin.path_part(args.observation_id, safe=':/')}", {"lang": args.lang})
    data = answer["data"]

    # One row: the trace of one value.
    rows = [data]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
