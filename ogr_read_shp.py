import osgeo.ogr
shp = osgeo.ogr.Open(".temp_data/counties.shp")
num_layers = shp.GetLayerCount()

print(f"Shapefile contains {num_layers} layers")

for lyr_num in range(num_layers):
    lyr = shp.GetLayer(lyr_num)
    srs = lyr.GetSpatialRef().ExportToProj4()
    num_features = lyr.GetFeatureCount()

    print(f"Layer {lyr_num} has SRS {srs} and {num_features} features.")

    for feature_num in range(num_features):
        feature = lyr.GetFeature(feature_num)
        feature_name = feature.GetField("COUNTYNAME")
        print(f"\nFeature Id {feature_num} has name {feature_name}")

        attributes = feature.items()
        for key, value in attributes.items():
            try:
                print(f"    Key {key} has value {value}")
            except Exception as e:
                print(f"Error {e}")
                pass
