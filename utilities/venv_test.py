"""
You can use this file to test if your standard GIS-related imports work.
"""

try:
    import os
    import gdal_workaround
    import turtle as t
    from shapely.geometry import mapping
    from shapely.wkt import loads
    import psycopg2
    import psycopg2.extras
    import fiona
    from fiona.crs import from_epsg
    import pyproj

    try:
        from osgeo import ogr
        from osgeo import gdal
    except ImportError as e:
        print(f"Bad Import: {e}\nCould be a problem with GDAL or PyGDAL")
    except Exception as e:
        print(f"Something bad happened: {e}")

    print("Didn't see any import errors")

except Exception as e:
    print(f"{e}")
