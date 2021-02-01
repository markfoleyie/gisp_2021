import osgeo.ogr
import utilities.gdal_workaround

shapefile = osgeo.ogr.Open(".temp_data/counties.shp")
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(2)
print("Feature 2 has the following attributes:\n")
attributes = feature.items()
for key, value in attributes.items():
    print(f" {key} = {value}")

geometry = feature.GetGeometryRef()
geometryName = geometry.GetGeometryName()

print(f"\nFeature's geometry data consists of a {geometryName}")
