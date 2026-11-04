#!/usr/bin/env python3
"""EU and UK rules on fuel refined from Russian crude oil: the official texts quoted verbatim, the
partner and net-exporter country lists, the dates, and the changes recorded.

GET /api/rules/refined-from-russian-crude
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per quoted provision, or per document with --table
documents. The official texts are authoritative; this is information, not legal advice.

Writes out/rules-refined-from-russian-crude.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.
  --table: Which table of the answer: provisions, documents.

Example:
  python rules_refined_from_russian_crude.py --table documents
"""

import argparse

import fuelorigin

ROUTE_ID = "rules-refined-from-russian-crude"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    parser.add_argument("--table", choices=("provisions", "documents"), default="provisions", help="Which table of the answer.")
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/rules/refined-from-russian-crude", {"lang": args.lang})
    data = answer["data"]

    # One row per quoted provision, or per document with --table documents. The official texts are
    # authoritative; this is information, not legal advice.
    if args.table == "provisions":
        rows = data["provisions"]
    else:
        rows = data["documents"]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
