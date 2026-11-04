#!/usr/bin/env python3
"""Every non-EU supplier with a supplier page: crude to the EU, largest EU importers, Hormuz route.

GET /api/suppliers-summary
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per supplier.

Writes out/suppliers-summary.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python suppliers_summary.py
"""

import argparse

import fuelorigin

ROUTE_ID = "suppliers-summary"

# This answer does not name its datasets, so the file's top lines cite the main one here.
CITE = [("Eurostat", "nrg_ti_oilm", "https://ec.europa.eu/eurostat/databrowser/view/nrg_ti_oilm/default/table?lang=en")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/suppliers-summary", {"lang": args.lang})
    data = answer["data"]

    # One row per supplier.
    rows = data
    fuelorigin.save_rows(ROUTE_ID, rows, answer, cite=CITE)


if __name__ == "__main__":
    main()
