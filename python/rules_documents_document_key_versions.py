#!/usr/bin/env python3
"""Every version of a followed legal document we fetched: the publisher's version and date, our
retrieval time, sha256, size and official URL (key holders only).

GET /api/rules/documents/{document_key}/versions
For key holders: without FO_KEY the script says so and stops, without calling the API.
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per version of the document.

Writes out/rules-documents-document-key-versions.csv. One request, no retry.

Options:
  --document_key: e.g.
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python rules_documents_document_key_versions.py --document_key ec:faq-art3ma
"""

import argparse

import fuelorigin

ROUTE_ID = "rules-documents-document-key-versions"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--document_key", default="eu:32014R0833", help="e.g.")
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    fuelorigin.require_key(ROUTE_ID)

    answer = fuelorigin.get_json(f"/api/rules/documents/{fuelorigin.path_part(args.document_key, safe=':/')}/versions", {"lang": args.lang})
    data = answer["data"]

    # One row per version of the document.
    rows = [
        {"document_key": data["document_key"], "title": data["title"], "publisher": data["publisher"],
         "licence": data["licence"], "attribution": data["attribution"], **version}
        for version in data["versions"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
