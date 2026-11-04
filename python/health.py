#!/usr/bin/env python3
"""Is the API up: a database round trip and the number of views. Not rate limited.

GET /health
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per checked component, with the API's overall
status.

Writes out/health.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python health.py
"""

import argparse

import fuelorigin

ROUTE_ID = "health"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    answer = fuelorigin.get_json("/health", {"lang": args.lang})

    # One row per checked component, with the API's overall status.
    rows = [
        {"status": answer["status"], "version": answer["version"], "checked_at": answer["checked_at"],
         "component": component["name"], "component_status": component["status"],
         "detail": component.get("detail")}
        for component in answer["components"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer, own_bookkeeping=True)


if __name__ == "__main__":
    main()
