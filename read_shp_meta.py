"""
Program to read basic metadata from any shapefile.

MF, March 2010
"""

import utilities.gdal_workaround
import fiona
from fiona.crs import from_epsg, from_string, to_string
import shapely

# 'mapping' turns a shapely geometry into a GeoJSON-like structure for use by Fiona
# 'shape' turns a GeoJSON-like structure from Fiona into a shapely geometry object. An object needs to be in this format
# to allow shapely to do geometric computations
from shapely.geometry import mapping, shape
import pyproj

if __name__ == "__main__":
    # try/except is ther to catch any errors that occur
    try:
        # Get the incoming file from user. This must, of course, exist and be a valid spatial file
        incoming_file = input("Enter path to shapefile: ")

        with fiona.open(incoming_file, "r") as source:
            # Open the file and print out some basic info
            print(f"Driver: {source.driver}")
            print(f"Geometry Type: {source.schema['geometry']}")
            print(f"CRS: {source.crs}\n{source.crs_wkt}")
            print(f"Features: {len(source)}")
            print(f"Bounds: {source.bounds}")
            print(f"Num properties: {len(source.schema['properties'])}")
            for k, v in source.schema["properties"].items():
                # Describe each 'property' attribute
                print(f"  {k}: {v}")
            print("+-" * 40)

            for feature in source:
                # Now we want to do stuff with the actual data. Each 'feature' represents a spatial 'thing' that we're
                # interested in, such as a county.
                # Suggestions:
                # 1. Loop through the features, printing metadata about each one
                # 2. Use shapely to find out something about each one such as its centroid.
                #    -> this needs to 'map' fiona's internal structure (GeoJSON) to shapely's internal structure
                #    (Geometry object).
                print(f"Id: {feature['id']}")
                print(f"GEOM Type: {feature['geometry']['type']}")
                print(f"Properties")
                for k,v in feature['properties'].items():
                    print(f"... {k}: {v}")

                # Here we make the shapely geometry from the Fiona GeoJSON-like structure
                feature_geom = shape(feature['geometry'])

                # Get the x,y of the centroid, make an appropriate 'transformer' object and use this to convert x,y to
                # lon,lat
                easting, northing = feature_geom.centroid.x, feature_geom.centroid.y
                transformer = pyproj.Transformer.from_crs(source.crs["init"], 4326, always_xy=True)
                lon, lat = transformer.transform(easting, northing)
                # Print the centroid
                print(f"Centroid of Id: {feature['id']} is {feature_geom.centroid}")
                if (lon != feature_geom.centroid.x) or (lat != feature_geom.centroid.y):
                    print(f"(Lon/Lat: {lon}, {lat})")
                print("="*80)

    except Exception as e:
        # Print any error message(s)
        print(f"Something bad happened\n{e}")