"""
Download any dataset from a Geoserver installation.
* The dataset can be filtered before download.
* You can choose any CRS.
* Valid formats are "text/csv", "application/zip", "application/json"

To use just import 'download_wfs_data' into your program. You can run this program stand-alone as well for testing
purposes.

Mark Foley,
April 2021
"""

# If any of these imports fail, it's likely to be because you haven't installed the appropriate library.
try:
    from io import BytesIO
    from zipfile import ZipFile
    import urllib
    import requests
    from owslib.wfs import WebFeatureService
except Exception as e:
    print(f"{e}")
    quit(1)

# Default host, it's unlikely that you'll need to change this.
HOST = "https://markfoley.info/geoserver"


def download_wfs_data(host=HOST, workspace=None, dataset=None, output_format="application/json", srs=None,
                      filter_expression=None, return_directory=None):
    """
    This is the main 'active ingredient' in this process. You import this into your program and provide the necessary
    parameters. Note that some have defaults (which can be None).

    :param host: Geoserver host and port. usually defaults to our current instance.
    :param workspace: WS on Geoserver. In our case it's usually TUDublin, census2011 or census2016.
    :param dataset: Any WFS dataset on Geoserver. You must supply this.
    :param output_format: Defaults to 'application/json' but can be any valid format (see above).
    :param srs: Supply any desired EPSG code otherwise ignore ant you'll get the native CRS of the dataset.
    :param filter_expression: You can filter records from the response using any valid ECQL or CQL expression.
    :param return_directory: Only relevant to Zip files. This is where the contents of a zipfile will be stored. Used
    when you wnat to get shapefiles.

    :return: The result. Content depends on output format.
    * Zip returns a tuple of directory (location) and a list of files.
    * CSV returns data in text format
    * Json returns a dictionary with schema and GeoJSON data. (This is the default.
    """

    valid_formats = ["text/csv", "application/zip", "application/json"]

    try:
        wfs11 = WebFeatureService(url=f"{HOST}/wfs", version='1.1.0')

        # Strings to supply to URL. Note that (E)CQL expressions  must be URL-encoded.
        cql_string = f"&cql_filter={urllib.parse.quote(filter_expression)}" if filter_expression else ""
        srs_string = f"&srsName=EPSG:{srs}" if srs else ""
        format_string = f"&outputFormat={output_format}" if output_format else ""

        url = f"{host}/{workspace}/ows?service=WFS&version=1.0.0&request=GetFeature" \
              f"&typeName={workspace}:{dataset}{cql_string}{srs_string}{format_string}"

        response = requests.get(url)
        if 200 <= response.status_code <= 299:
            if not response.headers["Content-Type"]:
                raise ValueError("Couldn't figure out what type this is, sorry.")
            content_type = [item.strip().split("=") for item in
                            response.headers["Content-Type"].split(";")]
            if content_type[0][0] not in valid_formats:
                raise ValueError(f"Looks like an invalid content type: {response.headers['Content-Type']}")
            if content_type[0][0] == "application/zip":
                if not return_directory:
                    raise ValueError("No return directory supplied.")
                my_zipfile = ZipFile(BytesIO(response.content))
                my_zipfile.extractall(path=return_directory)
                return return_directory, my_zipfile.namelist()
            if content_type[0][0] == "application/json":
                return {
                    "schema": wfs11.get_schema(f"{workspace}:{dataset}"),
                    "geojson_data": response.json()
                }
            if content_type[0][0] == "text/csv":
                return response.text
            else:
                pass
    except Exception as e:
        print(f"{e}")
        quit(1)


def main():
    """
    Test the Geoserver download process.

    :return: None
    """
    WORKSPACE_POLYS = "census2011"
    DATASET_POLYS = "counties"
    WORKSPACE_POINTS = "TUDublin"
    DATASET_POINTS = "geonames_ie"
    POLYS_CQL_FILTER = "nuts3name = 'Dublin'"
    POLYS_SRS_NAME = 29903
    POINTS_CQL_FILTER = "featurecode = 'PPL' AND population > 5000"

    polys_result = download_wfs_data(workspace=WORKSPACE_POLYS, dataset=DATASET_POLYS, srs=POLYS_SRS_NAME,
                                     filter_expression=POLYS_CQL_FILTER)
    points_result = download_wfs_data(workspace=WORKSPACE_POINTS, dataset=DATASET_POINTS,
                                      filter_expression=POINTS_CQL_FILTER)
    pass


if __name__ == "__main__":
    main()
