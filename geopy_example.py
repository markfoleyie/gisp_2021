from geopy.geocoders import Nominatim
from shapely.geometry import Point
from shapely import wkt
GEOCODER = Nominatim(user_agent="myapplication")


def geocode(point=None, address=None, reverse=False):
    if point and isinstance(point, Point):
        pass
    elif point and (isinstance(point, list) or isinstance(point, tuple)):
        point = Point(point[0], point[1])
    elif point and (isinstance(point, str)):
        try:
            point = wkt.loads(point)
        except:
            point = None
    else:
        pass

    if point and reverse:
        return GEOCODER.reverse(f"{point.y}, {point.x}")
    elif address:
        return GEOCODER.geocode(f"{address}")
    else:
        print(f"Call to Geocoder incorrectly formatted")
        return None


def main():
    point = Point(-8.5, 53.5)
    address = "Mullingar, Westmeath, Ireland"
    answer = geocode(point=point, reverse=True)
    print(f"The address of {point} is {answer}")
    answer = geocode(address=address, reverse=False)
    print(f"The location of {address} is {Point(answer.longitude, answer.latitude)}")


if __name__ == "__main__":
    main()
