try:
    import fiona
    from fiona.crs import from_epsg
    import utilities.fiona_supported_drivers as fsd
    import os
except Exception as e:
    print(f"{e}")
    quit(1)


def write_spatial(file=None, directory=None, data=None, **meta):
    try:
        if not data:
            raise ValueError(f"No data to write.")
        if not os.path.exists(directory):
            raise ValueError(f"Target directory doesn't exist.")
        if "driver" not in meta:
            raise ValueError(f"Missing driver.")
        if "crs" not in meta:
            raise ValueError(f"Missing CRS.")
        if "schema" not in meta:
            raise ValueError(f"Missing schema.")
        if meta["driver"] not in fsd.file_extensions:
            raise ValueError(f"Invalid driver.")

        target = os.path.join(directory, f"{file}.{fsd.file_extensions[meta['driver']]}")
        meta["crs"] = from_epsg(meta["crs"])
        for k, v in meta["schema"]["properties"].items():
            if v == "string":
                meta["schema"]["properties"][k] = "str"
            elif v == "double":
                meta["schema"]["properties"][k] = "float"

        with fiona.open(target, "w", **meta) as fh:
            for feature in data:
                fh.write(feature)

    except Exception as e:
        print(f"{e}")
        quit(1)
