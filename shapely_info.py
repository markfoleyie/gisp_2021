"""
This program returns a bunch of characteristics of up to two geometric objects and the relationships between them.

Mark Foley,
March 2019.
"""
try:
    # import gdal_workaround
    import fiona
    import shapely.geometry as geo
    import shapely
    from collections import OrderedDict
    import os
    from utilities.get_or_create_temporary_directory import get_temporary_directory as get_temp
    from utilities.get_any_file_from_net import get_file_from_server as get_zip
except ImportError as e:
    print("{}".format(e))
    quit(1)

# We sset up some input efaults to save on typing. These can be changed at RUN TIME.
DEFAULT_SHAPE_ZIP = {
    "geoserver": "https://markfoley.info/geoserver",
    "workspace": "census2011",
    "dataset": "counties",
    "filter1": "countyname:carlow",
    "filter2": "countyname:kilkenny",
}


def geom_info(g1, g2=None):
    """

    :param g1: A 'feature' such as you'd get when you use 'fiona' to iterate through a spatial data file
    :param g2: As above.
    :return: A tuple containing up to 3 dictionaries with info on the first feature, the second feature and the
    relationships between them.

    """
    try:
        if not (g1):
            raise ValueError("1st argument must be present.")
        if "geometry" not in g1:
            raise TypeError("1st argument doesn't look like a feature")
        if not isinstance(geo.shape(g1["geometry"]), shapely.geometry.base.BaseGeometry):
            raise TypeError("1st argument is not a spatial feature")
            quit(1)
        if g2 and "geometry" not in g2:
            raise TypeError("2nd argument doesn't look like a feature")
        if g2 and (not isinstance(geo.shape(g2["geometry"]), shapely.geometry.base.BaseGeometry)):
            raise TypeError("2nd argument is not a spatial feature")
            quit(1)

        g1_data = OrderedDict()
        g2_data = OrderedDict()
        relationship = OrderedDict()

        g1 = geo.shape(g1["geometry"])
        g1_data["area"] = g1.area
        g1_data["bounds"] = g1.bounds
        g1_data["length"] = g1.length
        g1_data["geom_type"] = g1.geom_type
        g1_data["has_z"] = g1.has_z
        # g1_data["is_ccw"] = g1.is_ccw
        g1_data["is_empty"] = g1.is_empty
        g1_data["is_ring"] = g1.is_ring
        g1_data["is_closed"] = g1.is_closed
        g1_data["is_valid"] = g1.is_valid
        g1_data["is_empty"] = g1.is_empty
        g1_data["is_simple"] = g1.is_simple

        if g2:
            g2 = geo.shape(g2["geometry"])
            g2_data["area"] = g2.area
            g2_data["bounds"] = g2.bounds
            g2_data["length"] = g2.length
            g2_data["geom_type"] = g2.geom_type
            g2_data["has_z"] = g2.has_z
            # g2_data["is_ccw"] = g2.is_ccw
            g2_data["is_empty"] = g2.is_empty
            g2_data["is_ring"] = g2.is_ring
            g2_data["is_closed"] = g2.is_closed
            g2_data["is_valid"] = g2.is_valid
            g2_data["is_empty"] = g2.is_empty
            g2_data["is_simple"] = g2.is_simple

            relationship["equals"] = g1.equals(g2)
            relationship["contains"] = g1.contains(g2)
            relationship["crosses"] = g1.crosses(g2)
            relationship["disjoint"] = g1.disjoint(g2)
            relationship["intersects"] = g1.intersects(g2)
            relationship["overlaps"] = g1.overlaps(g2)
            relationship["touches"] = g1.touches(g2)
            relationship["within"] = g1.within(g2)

            relationship["de9im"] = g1.relate(g2)

        return g1_data, g2_data, relationship

    except Exception as e:
        print("{}".format(e))
        quit(1)


def read_shp(shapefile, filter1, filter2):
    """
    We read in a shapefile, the argument gives us a string with the FULL PATH to the required file.

    :param shapefile: The file we're going to open
    :param filter1: Filters in the format key:value where key is in the shapefile properties, e.g. countyname:carlow
    :param filter2:
    :return:
    """
    try:
        filter1 = filter1.split(":")
        filter1[1] = filter1[1].title()
        filter2 = filter2.split(":")
        filter2[1] = filter2[1].title()
    except Exception as e:
        print("f{e}")
        quit(1)

    features = []
    with fiona.Env():
        with fiona.open(shapefile, "r") as fh:
            for feature in fh:
                if filter1[1] in feature["properties"]["countyname"] or \
                        filter2[1] in feature["properties"]["countyname"]:
                    features.append(feature)

    print(f"Feature properties\n{'-' * 20}")
    for feature in features:
        for k, v in feature["properties"].items():
            print(f"k: {k}, v: {v}")
        print(f"{'-' * 20}")

    # Do spatial analysis - comparison of the two features
    result = geom_info(features[0], features[1])
    print("g1 Info\n" + "-" * 20)
    for k, v in result[0].items():
        print("{}: {}".format(k, v))

    if result[1]:
        print("\ng2 Info\n" + "-" * 20)
        for k, v in result[1].items():
            print("{}: {}".format(k, v))

    if result[2]:
        print("\nRelationship Info\n" + "-" * 20)
        for k, v in result[2].items():
            print("{}: {}".format(k, v))
        print(" |i|b|e\n +-+-+-\ni|{0[0]}|{0[1]}|{0[2]}\nb|{0[3]}|{0[4]}|{0[5]}\ne|{0[6]}|{0[7]}|{0[8]}"
            .format(
            tuple([i for i in result[2]["de9im"]])
        ))


if __name__ == "__main__":
    geoserver_target = {}
    geoserver_target["geoserver"] = \
        input(f"Input Geoserver URL or press ENTER for {DEFAULT_SHAPE_ZIP['geoserver']} ") or DEFAULT_SHAPE_ZIP[
            'geoserver']
    geoserver_target["workspace"] = \
        input(f"Input Workspace or press ENTER for {DEFAULT_SHAPE_ZIP['workspace']} ") or DEFAULT_SHAPE_ZIP['workspace']
    geoserver_target["dataset"] = \
        input(f"Input Data Set or press ENTER for {DEFAULT_SHAPE_ZIP['dataset']} ") or DEFAULT_SHAPE_ZIP['dataset']
    geoserver_target["filter1"] = \
        input(f"Input filter 1 or press ENTER for {DEFAULT_SHAPE_ZIP['filter1']} ") or DEFAULT_SHAPE_ZIP['filter1']
    geoserver_target["filter2"] = \
        input(f"Input filter 2 or press ENTER for {DEFAULT_SHAPE_ZIP['filter2']} ") or DEFAULT_SHAPE_ZIP['filter2']

    my_temp_directory = get_temp(__file__)
    url = f"{geoserver_target['geoserver']}/{geoserver_target['workspace']}/ows?service=WFS&version=1.0.0&" \
          f"request=GetFeature&typeName={geoserver_target['workspace']}:{geoserver_target['dataset']}&" \
          f"outputFormat=SHAPE-ZIP"
    get_zip(url, my_temp_directory)
    read_shp(f'{os.path.join(my_temp_directory, geoserver_target["dataset"])}.shp', filter1=geoserver_target["filter1"],
             filter2=geoserver_target["filter2"])
