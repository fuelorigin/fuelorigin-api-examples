#!/usr/bin/env python3
"""One source, with its licence and health.

GET /api/sources/{source_id}
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row: the source, its licence and its health.

Writes out/sources-source-id.csv. One request, no retry.

Options:
  --source_id: A source's id, as GET /api/sources lists it.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python sources_source_id.py --source_id ec_weekly_oil_bulletin
"""

import argparse

import fuelorigin

ROUTE_ID = "sources-source-id"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--source_id",
        default="eurostat_nrg_ti_oilm",
        help="A source's id, as GET /api/sources lists it.",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json(f"/api/sources/{fuelorigin.path_part(args.source_id)}", {"lang": args.lang})
    data = answer["data"]

    # One row: the source, its licence and its health.
    rows = [data]
    fuelorigin.save_rows(ROUTE_ID, rows, answer, own_bookkeeping=True)


if __name__ == "__main__":
    main()
