"""
Sample to read CRS from shapefile and transform coordinates of bounding box.

Mark Foley
Feb. 2019
"""
import utilities.gdal_workaround
import fiona
from fiona.crs import from_string, from_epsg, to_string
import pyproj

# file = "data/landuse2.gpkg"
DEFAULT_FILE = ".temp_data/counties.shp"

file = input(f"Enter a shapefile name in the format of path/to/file.shp (blank to use default - {DEFAULT_FILE}) ")
if not file:
    file = DEFAULT_FILE

with fiona.open(file, 'r') as source:
    source_crs = pyproj.CRS.from_dict(source.crs)
    target_crs = pyproj.CRS.from_epsg(4326)
    crs_transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)

    print(f"\n{'=' * 20}\n")
    print(f"There are {len(source)} features in source.")
    print(f"The SRID of source is {to_string(source.crs)}")
    print(f"The bounding box of source is \n{source.bounds}")

    in_pair_sw = source.bounds[0], source.bounds[1]
    in_pair_ne = source.bounds[2], source.bounds[3]

    print(f"The bounding box is converted from {to_string(source.crs)} to {target_crs}.\n")
    print(f"SW: {crs_transformer.transform(*in_pair_sw)}")
    print(f"NE: {crs_transformer.transform(*in_pair_ne)}")
