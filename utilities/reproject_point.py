import pyproj
from fiona.crs import from_epsg, from_string, to_string


def reproject(point, source_epsg_code, target_epsg_code):
    transformer = pyproj.Transformer.from_crs(from_epsg(source_epsg_code), from_epsg(target_epsg_code), always_xy=True)
    target_x, target_y = transformer.transform(point.x, point.y)

    return (target_x, target_y)

