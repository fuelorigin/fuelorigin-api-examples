#!/usr/bin/env python3
"""Map layers as GeoJSON: refineries, ports, pipelines, export points, chokepoints.

GET /api/map/layers
This route has no format=csv, and every source behind it allows redistribution, so the script
writes rows of the JSON answer as CSV. One row per drawn feature: its layer, its geometry as text,
its properties.

Writes out/map-layers.csv. One request, no retry.

Options:
  --lang: Language of the reader-facing text, for example en, de or fr. Numbers and codes do not
      change.
  --layer: Only this layer: refineries, ports, crude_pipelines, product_pipelines, other_pipelines,
      export_points or chokepoints.

Example:
  python map_layers.py --layer ports
"""

import argparse
import json

import fuelorigin

ROUTE_ID = "map-layers"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--lang",
        help="Language of the reader-facing text, for example en, de or fr. Numbers and codes do not change.",
    )
    parser.add_argument("--layer", help="Only this layer, for example ports.")
    args = parser.parse_args()

    answer = fuelorigin.get_json("/api/map/layers", {"lang": args.lang})
    data = answer["data"]

    # One row per drawn feature: its layer, its geometry as text, its properties.
    rows = [
        {"layer": layer["id"], "schematic": layer["schematic"], "geometry_type": feature["geometry"]["type"],
         "coordinates": json.dumps(feature["geometry"]["coordinates"]), **feature["properties"]}
        for layer in data["layers"]
        if args.layer in (None, layer["id"])
        for feature in layer["features"]["features"]
    ]
    fuelorigin.save_rows(ROUTE_ID, rows, answer)


if __name__ == "__main__":
    main()
