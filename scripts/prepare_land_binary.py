#!/usr/bin/env python3
"""Convert Natural Earth GeoJSON polygons to a compact C-friendly binary file."""
import json
import struct
import sys

src = sys.argv[1] if len(sys.argv) > 1 else "ne_110m_land.geojson"
dst = sys.argv[2] if len(sys.argv) > 2 else "land_polygons.bin"
with open(src, encoding="utf-8") as f:
    data = json.load(f)
polys = []
for feature in data["features"]:
    geom = feature["geometry"]
    if geom["type"] == "Polygon":
        polys.append(geom["coordinates"])
    elif geom["type"] == "MultiPolygon":
        polys.extend(geom["coordinates"])
with open(dst, "wb") as f:
    f.write(b"LANDv1\0\0")
    f.write(struct.pack("<I", len(polys)))
    for poly in polys:
        f.write(struct.pack("<I", len(poly)))
        for ring in poly:
            f.write(struct.pack("<I", len(ring)))
            for lon, lat, *_ in ring:
                f.write(struct.pack("<dd", lon, lat))
print(f"Wrote {len(polys)} polygons to {dst}")
