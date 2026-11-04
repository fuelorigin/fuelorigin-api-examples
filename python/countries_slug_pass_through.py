#!/usr/bin/env python3
"""How much of a crude price move reaches the pump, and how fast.

GET /api/countries/{slug}/pass-through
Asks for the API's own CSV (format=csv) and writes it unchanged, # lines included. On a 403 it
prints the API's reason and stops.

Writes out/countries-slug-pass-through.csv. One request, no retry.

Options:
  --slug: The page name in the address, for example germany.
  --fuel: The fuel code. Other values are rejected.
  --window: latest-3y (the most recent three-year window), full (the whole sample), or all (both,
      as a list).
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.

Example:
  python countries_slug_pass_through.py --slug france --fuel EURO_SUPER_95
"""

import argparse

import fuelorigin

ROUTE_ID = "countries-slug-pass-through"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--slug",
        default="germany",
        help="The page name in the address, for example germany.",
    )
    parser.add_argument(
        "--fuel",
        choices=("EURO_SUPER_95", "DIESEL", "HEATING_GASOIL", "LPG_MOTOR", "FUEL_OIL_1", "FUEL_OIL_2", "RESIDUAL_FUEL_OIL", "OTHER", "REGULAR_GASOLINE_US"),
        default="DIESEL",
        help="The fuel code. Other values are rejected.",
    )
    parser.add_argument(
        "--window",
        choices=("latest-3y", "full", "all"),
        help="latest-3y (the most recent three-year window), full (the whole sample), or all (both, as a list).",
    )
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    args = parser.parse_args()

    file = fuelorigin.get_csv(f"/api/countries/{fuelorigin.path_part(args.slug)}/pass-through", {"fuel": args.fuel, "window": args.window, "lang": args.lang})
    fuelorigin.save_csv(ROUTE_ID, file)


if __name__ == "__main__":
    main()
