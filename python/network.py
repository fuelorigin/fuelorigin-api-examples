#!/usr/bin/env python3
"""Infrastructure network: which ports, terminals and pipelines each refinery is connected to
(CONNECTED_TO only, never a flow).

GET /api/network
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per cited connection (never a flow), or per node or
country with --table.

Writes out/network.csv. One request, no retry.

Options:
  --country: Slug of a covered country (an EU member state, or a country covered outside the EU
      such as Switzerland); omit for the EU view.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.
  --table: Which table of the answer: edges, nodes, countries.

Example:
  python network.py --country germany --table nodes
"""

import argparse

import fuelorigin

ROUTE_ID = "network"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--country",
        help="Slug of a covered country (an EU member state, or a country covered outside the EU such as Switzerland); omit for the EU view.",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    parser.add_argument("--table", choices=("edges", "nodes", "countries"), default="edges", help="Which table of the answer.")
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/network", {"country": args.country, "lang": args.lang})
    data = answer["data"]

    # One row per cited connection (never a flow), or per node or country with --table.
    if args.table == "edges":
        rows = data["edges"]
    elif args.table == "nodes":
        rows = data["nodes"]
    else:
        rows = data["countries"]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
