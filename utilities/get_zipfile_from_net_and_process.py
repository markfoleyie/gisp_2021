from io import BytesIO
from zipfile import ZipFile
import requests


def get_zip_from_server(url, return_directory):
    """
    This accepts a  a URL and (ii) retrieves a zipped shapefile from the URL.

    :param url: URL of zip file
    :return: a list of files from th zip file
    """

    try:
        response = requests.get(url)
        if 200 <= response.status_code <= 299:
            if response.headers["Content-Type"] and response.headers["Content-Type"] == "application/zip":
                my_zipfile = ZipFile(BytesIO(response.content))
                my_zipfile.extractall(path=return_directory)
                return my_zipfile.namelist()
            else:
                raise ValueError(
                    f"Doesn't look like  can deal with the content\nContent-Type is '{response.headers['Content-Type']}'"
                )
        else:
            raise ValueError(f"Bad status code: {response.status_code}")
    except Exception as e:
        print(f"{e}")
        quit(1)


