"""
This example takes a set of polys (the Dublin counties) from Geoserver, merges the polys into one and totals the
populations. The result is written to a new shapefile. Note the use of utility programs here. These are available in the
utilities directory on the GitHub site.
"""
import os
import fiona
from fiona.crs import from_epsg

from shapely.ops import cascaded_union
from shapely.geometry import shape, mapping

from utilities.download_from_geoserver import download_wfs_data as get_geoserver
from utilities.get_or_create_temporary_directory import get_temporary_directory as get_temp

DEFAULTS = {
    "HOST": "https://markfoley.info/geoserver",
    "TEMP_DIR": ".wk12example_temp",
    "WORKSPACE_POLYS": "census2011",
    "DATASET_POLYS": "counties",
    "POLYS_CQL_FILTER": "nuts3name = 'Dublin'",
    "POLYS_PROPERTY_FILTER": ["nuts3name", "countyname", "total2011"],
    "SRS_CODE": 29903
}


def do_analysis(**defaults):
    try:
        # Get data from Geoserver
        local_polys = get_geoserver(
            host=defaults["HOST"],
            workspace=defaults["WORKSPACE_POLYS"],
            dataset=defaults["DATASET_POLYS"],
            filter_expression=defaults["POLYS_CQL_FILTER"],
            property_list=defaults["POLYS_PROPERTY_FILTER"],
            srs=defaults["SRS_CODE"])

        # For each county, convert its geometry to shapely-friendly format/
        feature_polys = []
        population = 0
        for feature in local_polys["geojson_data"]["features"]:
            feature_polys.append(shape(feature["geometry"]))
            population += feature["properties"]["total2011"]

        # Merge the polys
        merged_polys = cascaded_union(feature_polys)

        # Make outgoing schema for the new shapefile
        outgoing_schema = {
            "geometry": merged_polys.geom_type,
            "properties": {
                "name": "str",
                "population": "int"
            }
        }

        # Construct the outgoing feature - there will be only one.
        outgoing_feature = {
            "id": 0,
            "geometry": mapping(merged_polys),
            "properties": {
                "name": "Greater Dublin",
                "population": population
            }
        }

        # Make a temp directory if necessary
        tmp_dir = get_temp(__file__, defaults['TEMP_DIR'])

        # Make the filename for the new shapefile
        target_file = os.path.join(tmp_dir, f"{defaults['WORKSPACE_POLYS']}_{defaults['DATASET_POLYS']}.shp")

        # Write out the new shapefile
        with fiona.open(target_file, "w", driver="ESRI Shapefile", crs=from_epsg(f"{defaults['SRS_CODE']}"),
                        schema=outgoing_schema) as fh:
            fh.write(outgoing_feature)


    except Exception as e:
        print(f"{e}")
        quit(1)


def main():
    # Pass the defaults to the analysis process.
    do_analysis(**DEFAULTS)


if __name__ == "__main__":
    main()
