import turtle as t
from shapely.wkt import loads
import csv


def calc_ratios(screen_width,screen_height,data):
    """
    dist_x = max easting - min easting
    dist_y = max northing - min northing

    # Scaling ratio each axis
    # to map points from world to screen
    x_ratio = screen width / dist_x
    y_ratio = screen height / dist_y

    :param data: List of rows representing query result set.
    :return: x and y screen ratios, bounding box for collection (result set)
    """
    bbox = [9999999, 9999999, 0, 0]

    for row in data:
        coords = loads(row['geom_str'])
        bbox[0] = min(coords.bounds[0], bbox[0])
        bbox[1] = min(coords.bounds[1], bbox[1])
        bbox[2] = max(coords.bounds[2], bbox[2])
        bbox[3] = max(coords.bounds[3], bbox[3])

    dist_x = bbox[2] - bbox[0]
    dist_y = bbox[3] - bbox[1]

    return screen_width / dist_x, screen_height / dist_y, bbox


def convert_point(screen_width, screen_height,ratios, point):
    """
    Function to convert easting/northing to screen coordinates.
    Remember screen coordinates are necessary for rendering.
    :param point: The point in easting/northing to convert
    :return: x,y pair in screen coordinates
    """

    # ratios[2] is the bounding box. Its elements 2 & 3 are max x and y
    x = screen_width - ((ratios[2][2] - point[0]) * ratios[0])
    y = screen_height - ((ratios[2][3] - point[1]) * ratios[1])

    # Python turtle graphics start in the middle of the screen so we must offset the points so they are centered
    x = x - (screen_width / 2)
    y = y - (screen_height / 2)

    return x, y


def draw_data(screen_Width, screen_height, data, ratios):
    """
    Draw map based on coordinates from query result set. 'World' coordinates must be converted to screen (pixel)
    coordinates.

    :param data: List of rows representing query result set.
    :return: None. Function draws map in window.
    """

    # ratios = calc_ratios(screen_Width,screen_height,data)

    for row in data:
        t.up()

        # Convert WKT representation to geometry object.
        coords = loads(row['geom_str'])

        centroid = (coords.centroid.bounds[0], coords.centroid.bounds[1])

        # Make 'World' point into screen coordinate pair.
        t.goto(convert_point(screen_Width,screen_height,ratios, centroid))

        # Write row name and population at geometry centroid (approximates to the 'middle' of the row multipolygon..
        legend = "{} (pop: {})".format(row['countyname'], row['total2011'])
        t.write(legend, align="center", font=("Arial", 10))

        # For each polygon in Multpolygon geometry, get each point in polygon, convert it to screen point and draw it.
        for geom in coords.geoms:
            for point in list(geom.exterior.coords):
                t.goto(convert_point(screen_Width,screen_height,ratios, point))
                t.down()
            t.up()

    t.hideturtle()
    t.exitonclick()


def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    INPUT_FILE = "Data/data-ky-wkt2.csv"

    csv.field_size_limit(1000000)
    with open(INPUT_FILE, "r", newline='') as fh:
        my_data = csv.DictReader(fh, delimiter='|',)
        if my_data:
            ratios = calc_ratios(SCREEN_WIDTH, SCREEN_HEIGHT, my_data)

    with open(INPUT_FILE, "r", newline='') as fh:
        my_data = csv.DictReader(fh, delimiter='|', )
        if my_data:
            draw_data(SCREEN_WIDTH, SCREEN_HEIGHT, my_data, ratios)
        else:
            print("Nothing to draw.")


if __name__ == "__main__":
    main()