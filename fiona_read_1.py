"""
Sample to read CRS from shapefile and transform coordinates of bounding box.

Mark Foley
Feb. 2019
"""
import utilities.gdal_workaround
import fiona
from fiona.crs import from_string, from_epsg, to_string
import pyproj
# import pyproj_transformation as pt
# import utilities.generic_useful_parameters as gup

# file = ".cache/geonames_pop5000.shp"
# file = ".cache/geonames_pop_5000.shp"
# file = "gageom/gageom_itm.shp"
# file = "data/landuse2.gpkg"

file = input("Enter a shapefile name in the format of path/to/file.shp ")


with fiona.open(file, 'r') as source:
    # for feature in source:
    #     print("{} {}"
    #           .format(feature["properties"]["countyname"],
    #                   feature["properties"]["total2011"]))

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

    # print("SW: {}".format(pt.transform_coordinates(source.crs, target_crs, in_pair_sw)))
    # print("NE: {}".format(pt.transform_coordinates(source.crs, target_crs, in_pair_ne)))
    # bbox = source.bounds
