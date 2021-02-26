"""
Read any shapefile from a Geoserver instance and (i) display its metadata and (ii) hand back its contents in GeoJSON
format.

How it works
1. Constructs a URL formatted to get a resource from Geoserver, from some basic inputs
2. Retrieves a zip file containing the resource (shape-zip)
3. Extracts the contents of the zip file to a temporary directory and identifies the .shp file
4. Reads the shapefile metadata, outputs this and writes the feature collection form the shapefile in GeoJSON format to
a file in the temporary directory.

Mark Foley
Feb 2021
"""

import fiona
import os
import json
from utilities.get_or_create_temporary_directory import get_temporary_directory as get_temp
from utilities.get_zipfile_from_net_and_process import get_zip_from_server as get_zip
from utilities.reproject_point import reproject


DEFAULT_SHAPE_ZIP = {
    "geoserver": "https://markfoley.info/geoserver",
    "workspace": "census2011",
    "dataset": "counties"
}


def get_shp_details(shapefile):
    """
    This accepts the path to shapefile and (i) opens the shapefile, (ii) prints metadata, (iii) creates a GeoJSON-like
    dictionary from the shapefile features and (iv) writes this to a file in GeoJSON format.

    :param shapefile: path to shapefile
    :return: None
    """

    try:
        with fiona.open(shapefile, "r") as source:
            # Open the file and print out some basic info
            print(f"Name: {source.name}")
            print(f"Driver: {source.driver}")
            print(f"Geometry Type: {source.schema['geometry']}")
            print(f"CRS: {source.crs}\n{source.crs_wkt}")
            print(f"Features: {len(source)}")
            print(f"Bounds: {source.bounds}")
            print(f"Num properties: {len(source.schema['properties'])}")

            geojson_shell = {
                "type": "FeatureCollection",
                "features": [],
                "crs": {
                    "type": "name",
                    "properties": {
                        "name": f"urn:ogc:def:crs:EPSG::{source.crs['init'].split(':')[-1]}"
                    }
                }
            }

            for feature in source:
                geojson_shell["features"].append(feature)

            with open(f"{os.path.splitext(shapefile)[0]}.json", "w") as output:
                output.write(json.dumps(geojson_shell))
    except Exception as e:
        print(f"{e}")
        quit(1)


def main():
    """
    Accepts inputs and runs through the process in stages

    :return: None
    """
    geoserver_target = {}
    geoserver_target["geoserver"] = \
        input(f"Input Geoserver URL or press ENTER for {DEFAULT_SHAPE_ZIP['geoserver']} ") or DEFAULT_SHAPE_ZIP['geoserver']
    geoserver_target["workspace"] = \
        input(f"Input Workspace or press ENTER for {DEFAULT_SHAPE_ZIP['workspace']} ") or DEFAULT_SHAPE_ZIP['workspace']
    geoserver_target["dataset"] = \
        input(f"Input Data Set or press ENTER for {DEFAULT_SHAPE_ZIP['dataset']} ") or DEFAULT_SHAPE_ZIP['dataset']

    my_temp_directory = get_temp(__file__)
    url = f"{geoserver_target['geoserver']}/{geoserver_target['workspace']}/ows?service=WFS&version=1.0.0&" \
          f"request=GetFeature&typeName={geoserver_target['workspace']}:{geoserver_target['dataset']}&" \
          f"outputFormat=SHAPE-ZIP"

    my_zipfiles = get_zip(url, my_temp_directory)
    for file in my_zipfiles:
        if file[-4:] == ".shp":
            get_shp_details(os.path.join(my_temp_directory, file))

    print(f"Looks like all went well.")


if __name__ == '__main__':
    main()
