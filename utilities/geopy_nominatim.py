# If any of these imports fail, it's likely to be because you haven't installed the appropriate library.
try:
    import datetime
    from geopy.geocoders import Nominatim
    import pyproj
    from shapely.geometry import Point
except Exception as e:
    print(f"{e}")
    quit(1)

geolocator = Nominatim(user_agent="gisp-agent")

def geocode_address(address=""):
    """
    Address geocoder using OSM Nominatim. Accepts 'address' string and returns a dictionary response containing
    everything that the geocoder provides.

    :param address: Address to be geocoded
    :return: response as dict
    """
    body = {}

    try:
        if not address:
            raise Exception("No address supplied")

        # This object gives us everything the the geocoder can tell us about the address supplied
        loc = geolocator.geocode(address, addressdetails=True)

        if not loc:
            raise Exception(f"No result found for '{address}'")

        body["message"] = f"Called 'geocode_address'. OK! {datetime.datetime.now()}"
        body["input_address"] = address
        body["result"] = loc.raw

        # We return a dictionary with everything that the geocoder gave us
        response = {
            "body": body
        }
    except Exception as e:
        body["error"] = f"{e} - {datetime.datetime.now()}"
        response = {
            "body": body
        }

    return response


def geocode_location(location="", epsg=4326):
    """
    Address geocoder using OSM Nominatim. Accepts 'location' string in lat, lon format and returns a
    dictionary response containing everything that the geocoder provides.

    :param location: string in lon, lat
    :param epsg: EPSG code of input coordinates, these will be converted to EPSG:4326 if not already 4326
    :return: dict response
    """
    body = {}

    try:
        if not location:
            raise Exception("No location supplied")

        # The reverse geocoder takes a coordinate pair and attempts to give us the address (and more besides) but the
        # incoming coordinates must be in 4326 (WGS84). If they're not, we need to convert them. The input comes as a
        # string so must be split into its components and these must be converted to floating point numbers.

        if isinstance(location, Point):
            x = location.x
            y = location.y
        elif isinstance(location, str):
            x = float(location.strip().split(",")[0])
            y = float(location.strip().split(",")[1])

        if epsg != 4326:
            input_transformer = pyproj.Transformer.from_crs(int(epsg), 4326, always_xy=True)
            lon, lat = input_transformer.transform(x, y)
        else:
            lon, lat = x, y

        # This object gives us everything the the geocoder can tell us about the coordinates supplied
        loc = geolocator.reverse(f"{lat}, {lon}")

        if not loc:
            raise Exception(f"No result found for '{location}'")

        body["message"] = f"Called 'geocode_location'. OK! {datetime.datetime.now()}"
        body["input_location"] = location
        body["result"] = loc.raw

        # As above, we return a dictionary with everything that the geocoder gave us
        response = {
            "body": body
        }
    except Exception as e:
        body["error"] = f"{e} - {datetime.datetime.now()}"
        response = {
            "body": body
        }

    return response


if __name__ == "__main__":
    # Test some samples
    my_address = "Drumcondra, Dublin, Ireland"
    result = geocode_address(my_address)
    print(result)
    my_location = "-6.33, 53.33"
    result = geocode_location(my_location)
    print(result)
    my_location = "200000.0, 250000"
    result = geocode_location(my_location, 29902)
    print(result)
