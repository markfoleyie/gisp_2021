"""
Example to illustrate reading from a shapefile, taking a subset of the features , doing some basic coordinate geometry
and writing out the result to a new shapefile.

Mark Foley
March 2021
"""

# import utilities.gdal_workaround
import fiona
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
import os
from utilities.get_or_create_temporary_directory import get_temporary_directory as get_temp
from utilities.get_any_file_from_net import get_file_from_server as get_zip

DEFAULT_SHAPE_ZIP = {
    "geoserver": "https://markfoley.info/geoserver",
    "workspace1": "census2011",
    "dataset1": "counties",
    "workspace2": "TUDublin",
    "dataset2": "geonames_ie",
}


def process_shp(shp, output_dir, region_key, region_value):
    region_features = []

    output_crs = None
    output_schema = {
        "geometry": "",
        "properties": {
            "nuts3name": "str",
            "total2011": "float"
        }
    }

    with fiona.open(shp, "r") as source:
        output_crs = source.crs
        output_driver = source.driver
        output_schema["geometry"] = source.schema["geometry"]
        shp_epsg = source.crs['init'].split(':')[-1]
        for feature in source:
            if feature["properties"][region_key] == region_value:
                region_features.append(feature)

    region_geoms = []
    total_population = 0
    for feature in region_features:
        total_population += feature["properties"]["total2011"]
        region_geoms.append(shape(feature["geometry"]))

    merged_geoms = unary_union(region_geoms)

    new_feature = {
        "type": "Feature",
        "id": 0,
        "properties": {
            "nuts3name": region_value,
            "total2011": total_population
        },
        "geometry": mapping(merged_geoms)
    }

    with fiona.open(
            os.path.join(output_dir, f"{region_key}_{region_value}.shp"),
            "w",
            schema=output_schema,
            driver=output_driver,
            crs=output_crs,
            encoding="utf-8"
    ) as out_file:
        out_file.write(new_feature)


def main():
    geoserver_target = {}
    geoserver_target["geoserver"] = \
        input(f"Input Geoserver URL or press ENTER for {DEFAULT_SHAPE_ZIP['geoserver']} ") or DEFAULT_SHAPE_ZIP[
            'geoserver']
    geoserver_target["workspace1"] = \
        input(f"Input Workspace 1 or press ENTER for {DEFAULT_SHAPE_ZIP['workspace1']} ") or DEFAULT_SHAPE_ZIP[
            'workspace1']
    geoserver_target["dataset1"] = \
        input(f"Input Data Set 1 or press ENTER for {DEFAULT_SHAPE_ZIP['dataset1']} ") or DEFAULT_SHAPE_ZIP['dataset1']

    my_temp_directory = get_temp(__file__)
    counties_url = f"{geoserver_target['geoserver']}/{geoserver_target['workspace1']}/ows?service=WFS&version=1.0.0&" \
                   f"request=GetFeature&typeName={geoserver_target['workspace1']}:{geoserver_target['dataset1']}&" \
                   f"outputFormat=SHAPE-ZIP"

    get_zip(counties_url, my_temp_directory)

    polys_file = f"{os.path.join(my_temp_directory, geoserver_target['dataset1'])}.shp"

    region_key = "nuts3name"
    region_value = "Dublin"

    process_shp(polys_file, my_temp_directory, region_key=region_key, region_value=region_value)


if __name__ == "__main__":
    main()
