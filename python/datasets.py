#!/usr/bin/env python3
"""The published versions of the downloadable dataset bundle, with their addresses and DOI.

GET /api/datasets
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per file of each published version of the dataset
bundle.

Writes out/datasets.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python datasets.py
"""

import argparse

import fuelorigin

ROUTE_ID = "datasets"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/datasets", {"lang": args.lang})
    data = answer["data"]

    # One row per file of each published version of the dataset bundle.
    rows = [
        {"version": version["version"], "published_at": version["published_at"], "doi": data["doi"],
         "zenodo_doi": version["zenodo_doi"], **file}
        for version in data["versions"]
        for file in version["files"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer, own_bookkeeping=True)


if __name__ == "__main__":
    main()
