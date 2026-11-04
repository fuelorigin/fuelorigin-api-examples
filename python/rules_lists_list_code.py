#!/usr/bin/env python3
"""One country list as it stood on a date, by its legal dates or by what our runs had read (key
holders only).

GET /api/rules/lists/{list_code}
For key holders: without FO_KEY the script says so and stops, without calling the API.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per country on the list that day.

Writes out/rules-lists-list-code.csv. One request, no retry.

Options:
  --list_code: The list.
  --as_of: The day, YYYY-MM-DD.
  --basis: legal: by the legal dates the texts state or fix (Annex LI only); observed: what our
      runs had read by the end of the day (UTC).
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python rules_lists_list_code.py --as_of 2025-01-01
"""

import argparse

import fuelorigin

ROUTE_ID = "rules-lists-list-code"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--list_code",
        choices=("EU_ANNEX_LI_PARTNER", "EU_FAQ_NET_EXPORTER", "UK_GUIDANCE_PARTNER", "UK_GUIDANCE_NET_EXPORTER"),
        default="EU_ANNEX_LI_PARTNER",
        help="The list.",
    )
    parser.add_argument("--as_of", default="2026-04-24", help="The day, YYYY-MM-DD.")
    parser.add_argument(
        "--basis",
        choices=("legal", "observed"),
        default="legal",
        help="legal: by the legal dates the texts state or fix (Annex LI only); observed: what our runs had read by the end of the day (UTC).",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    fuelorigin.require_key(ROUTE_ID)

    answer = fuelorigin.get_json(f"/api/rules/lists/{fuelorigin.path_part(args.list_code)}", {"as_of": args.as_of, "basis": args.basis, "lang": args.lang})
    data = answer["data"]

    # One row per country on the list that day.
    rows = [
        {"list_code": data["list_code"], "as_of": data["as_of"], "basis": data["basis"],
         "status": data["status"], "licence": data["licence"], **entry}
        for entry in data["entries"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
