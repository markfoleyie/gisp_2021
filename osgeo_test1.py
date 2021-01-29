# from gdal import ogr
import osgeo.ogr as ogr
shapefile = ogr.Open(".temp_data/counties.shp")
numLayers = shapefile.GetLayerCount()
print(f"Shapefile contains {numLayers} layers")
print()
for layerNum in range(numLayers):
    layer = shapefile.GetLayer(layerNum)
    spatialRef = layer.GetSpatialRef().ExportToProj4()
    numFeatures = layer.GetFeatureCount()
    print(f"Layer {layerNum} has spatial reference {spatialRef}")
    print(f"Layer {layerNum} has {numFeatures} features")
    print()

    for featureNum in range(numFeatures):
        feature = layer.GetFeature(featureNum)
        featureName = feature.GetField("countyname")
        print(f"Feature {featureNum} has name {featureName}")