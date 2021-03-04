import pyproj
from fiona.crs import from_epsg, from_string, to_string
from shapely.geometry import Point


def reproject(point, source_epsg_code, target_epsg_code):
    transformer = pyproj.Transformer.from_crs(from_epsg(source_epsg_code), from_epsg(target_epsg_code), always_xy=True)
    target_x, target_y = transformer.transform(point.x, point.y)

    return (target_x, target_y)


def main():
    point_4326 = Point(-6.33, 53.33)
    point_29902 = Point(reproject(point_4326, 4326, 29902))
    point_2157 = Point(reproject(point_4326, 4326, 2157))

    print(f"Source point is {point_4326}\n29902: {point_29902}\n2157: {point_2157}")


if __name__ == "__main__":
    main()
