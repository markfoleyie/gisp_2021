"""
Added a docstring
"""

# Don't forget to import this in every program. I keep it in a directory called 'utilities' but this will vary for you.
import utilities.gdal_workaround

import shapely

# We may need to create or manipulate 'Polygon' or 'MultiPolygon' object types. As it's greyed out we haven't used these
# here. 'shape' creates a geometry object from a GeoJSON-like structure that Fiona gives you,
from shapely.geometry import Polygon, MultiPolygon, shape

import fiona

SEARCH_STRING = "ongford"
SEARCH_PROPERTY = "countyname"
SOURCE = ".temp_data/counties.shp"

with fiona.open(SOURCE) as source:
    # Open the source file
    for feature in source:
        # read each 'feature', in this case each county and...
        if SEARCH_STRING in feature["properties"][SEARCH_PROPERTY]:
            # ... match the search string in the 'countyname' property
            search_feature = feature
            # Get the geom type - we do this by turning the GeoJSON structure from Fiona into a Shapely geometry using
            # 'shape' and then extracting its 'type'
            search_feature_type = type(shape(search_feature["geometry"]))
            # We then make an instance of this 'type'.
            # We now have a (multi)polygon type so we can bail out
            search_poly = search_feature_type(shape(search_feature["geometry"]))
            break

with fiona.open(SOURCE) as source:
    # We read the source file again from the top
    for feature in source:
        # For each feature we make a geometry type as we did above.
        feature_type = type(shape(feature["geometry"]))
        feature_poly = feature_type(shape(feature["geometry"]))
        if feature_poly.touches(search_poly):
            # We can then compare the feature we've just made with the 'search feature' that we got from the earlier
            # process/ We do a shapely 'touches' computation and if we get a hit (True) then we print its name.
            print(feature["properties"][SEARCH_PROPERTY])
