"""
Assignment 1
Marks available: 35% of Total
This is the first of two assignments. It is designed to test
    Some basic programming skills
    Your understanding of basic shapefile read/write operations using Fiona
    Your ability to implement basic spatial analysis methods using Shapely

Specific tasks
==============
Download and save the counties dataset as a shapefile. You can get this at
https://markfoley.info/geoserver/census2011/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=census2011:counties&outputFormat=SHAPE-ZIP

Merge the Dublin local authorities into one and store in a new shapefile. Don't forget to store the attributes as well
as the geometry.

Calculate the centroid for Dublin merged and store this in a new shapefile.

Geocode the address of this centroid. You will need to convert the CRS to WGS84. This should be stored in the shapefile
you created in the last step.

Suggestions
===========
Store downloaded files like counties in their own directory/folder in your PyCharm project. Give this a sensible name
such as "counties" in this example. By using this scheme you can download it once and use it in different programs.

Store files created such as the merged shapefile and centroid in a separate directory/folder. Name this something like
".cache". The leading "." indicates a hidden directory/folder. This is designed to be sacrificial. You can delete its
contents without losing anything of value.

Testing
=======
If you show the resulting shapefiles in ArcGIS or QGIS you can easily verify whether your output is correct.

Submission
==========
Create a single .py file and submit this. Don't hard code file locations, like "c:\My Documents\Blah\Blah..." as I won't
be able to run your code without amending it. Use relative locations instead.
"""

# Don't forget to import this in every program. I keep it in a directory called 'utilities' but this will vary for you.
import utilities.gdal_workaround

# 'shape' creates a geometry object from a GeoJSON-like structure that Fiona gives you, 'mapping' creates a GeoJSON-like
# structure that Fiona needs rom a Shpely geometry object. They are, therefore opposites -> convert a to b and b to a.
from shapely.geometry import shape, mapping

# This is the shapely operation that actually does the merge computation
from shapely.ops import unary_union

# So that we can read and write shapefiles...
import fiona
from fiona.crs import to_string

# This is like a dictionary but the order of entry of the keys is preserved. This is useful as Fiona's schema needs
# attributes in a predictable order
from collections import OrderedDict

# This is a utility program to geocode an address or reverse geocode a coordinate pair using OSM's Nominatim geocoder.
import utilities.geopy_nominatim as geocode

def create_merged_shapefile(**inputs):
    """
    takes a dictionary of inputs (search string, search property, source and destination) and based on this creates a
    new merged geometry. It writes this to a new shapefile

    :param inputs: a dictionary of inputs (search string, search property, source and destination)
    :return: Nothing
    """

    # Create an empty list of geometries to merge. As we find one of the searched-for features we'll add it to this
    geometries_to_merge = []

    with fiona.open(inputs["SOURCE"]) as source:
        # Open the source file
        for feature in source:
            # read each 'feature' or spatial 'thing' (record) in the file and...
            if inputs["SEARCH_STRING"] in feature["properties"][inputs["SEARCH_PROPERTY"]]:
                # ... match the search string (data) in the search property (attribute), the property attribute is a
                # name like 'countyname' or 'nuts3name' or whatever
                search_feature = feature
                # Get the geom type - we do this by turning the GeoJSON structure from Fiona into a Shapely geometry
                # using 'shape' and then extracting its 'type'
                search_feature_type = type(shape(search_feature["geometry"]))
                # We then make an instance of this 'type'.
                search_poly = search_feature_type(shape(search_feature["geometry"]))
                # Add this (Multi)Polygon to our properties to merge list
                geometries_to_merge.append(search_poly)

        # We now have a list of polys to be merged, so we merge them...
        merged_polys = unary_union(geometries_to_merge)
        # ... and compute the centroid. We could do any other shapely operation that we wanted here as well.
        # Note that centroid is just one of many attributes of a shapely (multi)polygon. There are lots of others such
        # as area, boundary, bounding box, convex hull etc.
        merged_centroid = merged_polys.centroid

        # Reverse geocode the centroid
        source_epsg = int(to_string(source.crs).split(":")[1])
        geocode_result = geocode.geocode_location(location=f"{merged_centroid.x},{merged_centroid.y}", epsg=source_epsg)
        centroid_address = geocode_result["body"]["result"]["display_name"]

        # A small buffer can clean up geometries where the adjacent boundaries aren't exactly the same. If you take this
        # out and display the resulting shapefile in ArcGIS or QGIS, you'll see some ghost internal boundaries where
        # the different adjacent poly boundaries didn't exactly match.
        merged_polys = merged_polys.buffer(10)

        # Convert the shapely poly to GeoJSON-like structure for Fiona using 'mapping'
        merged_polys_mapping = mapping(merged_polys)
        centroid_mapping = mapping(merged_centroid)

        # Make the features - they're dictionaries. Note that we're only going to end up with one feature in each of
        # the outgoing shapefiles.

        # First the merged polys...
        merged_destination_feature = {}
        # id can be anything as long as it's unique
        merged_destination_feature["id"] = 0
        merged_destination_feature["geometry"] = merged_polys_mapping
        merged_destination_feature["properties"] = OrderedDict()
        merged_destination_feature["properties"]["featurename"] = f"{inputs['SEARCH_STRING']} merged"
        merged_destination_feature["properties"]["centroid_x"] = merged_centroid.x
        merged_destination_feature["properties"]["centroid_y"] = merged_centroid.y

        # Create a new shapefile (the output)
        merged_destination_meta = source.meta
        merged_destination_meta["schema"]["geometry"] = f"{merged_polys_mapping['type']}"
        merged_destination_meta["schema"]["properties"] = OrderedDict()
        merged_destination_meta["schema"]["properties"]["featurename"] = "str:254"
        merged_destination_meta["schema"]["properties"]["centroid_x"] = "float:33.31"
        merged_destination_meta["schema"]["properties"]["centroid_y"] = "float:33.31"

        with fiona.open(inputs["MERGED_DESTINATION"], "w", **merged_destination_meta) as destination:
            # Open the destination file and write out the (only) destination feature
            destination.write(merged_destination_feature)

        # ... then the centroid shapefile
        centroid_feature = {}
        # id can be anything as long as it's unique
        centroid_feature["id"] = 0
        centroid_feature["geometry"] = centroid_mapping
        centroid_feature["properties"] = OrderedDict()
        centroid_feature["properties"]["address"] = f"{centroid_address}"
        centroid_feature["properties"]["centroid_x"] = merged_centroid.x
        centroid_feature["properties"]["centroid_y"] = merged_centroid.y

        # Create a new shapefile (the output)
        centroid_meta = source.meta
        centroid_meta["schema"]["geometry"] = f"{centroid_mapping['type']}"
        centroid_meta["schema"]["properties"] = OrderedDict()
        centroid_meta["schema"]["properties"]["address"] = "str:254"
        centroid_meta["schema"]["properties"]["centroid_x"] = "float:33.31"
        centroid_meta["schema"]["properties"]["centroid_y"] = "float:33.31"

        with fiona.open(inputs["CENTROID_DESTINATION"], "w", **centroid_meta) as destination:
            # Open the destination file and write out the (only) destination feature
            destination.write(centroid_feature)


if __name__ == "__main__":
    # Test it

    inputs = {}
    inputs["SEARCH_STRING"] = "Dublin"

    # This is an example of 'knowing your data'. nuts3name is a property that describes a higher admin unit than county.
    inputs["SEARCH_PROPERTY"] = "nuts3name"

    inputs["SOURCE"] = "counties/counties.shp"

    # We're going to write these files. As they're 'sacrificial' - it can be easily recreated - I'm putting it into a
    # directory that I can afford to lose.
    inputs["MERGED_DESTINATION"] = ".cache/merged_polys.shp"
    inputs["CENTROID_DESTINATION"] = ".cache/merged_polys_centroid.shp"

    # The important bit...
    create_merged_shapefile(**inputs)

    print("Done.")