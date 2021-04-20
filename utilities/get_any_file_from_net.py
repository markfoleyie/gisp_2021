from io import BytesIO
from zipfile import ZipFile
import requests
import os
from utilities.get_or_create_temporary_directory import get_temporary_directory as get_temp


def get_file_from_server(url, return_directory, **kwargs):
    """
    This accepts a  a URL and (ii) retrieves a zipped shapefile from the URL.

    :param return_directory:
    :param url: URL of zip file
    :return: a list of files from th zip file
    """

    valid_formats = {
        "CSV": "text/csv",
        "SHAPE-ZIP": "application/zip",
        "JSON": "application/json"
    }

    try:
        response = requests.get(url)
        if 200 <= response.status_code <= 299:
            if not response.headers["Content-Type"]:
                raise ValueError("Couldn't figure out what type this is, sorry.")
            content_type = [item.strip().split("=") for item in
                            response.headers["Content-Type"].split(";")]
            if content_type[0][0] not in valid_formats.values():
                raise ValueError(f"Looks like an invalid content type: {response.headers['Content-Type']}")
            if content_type[0][0] == "application/zip":
                my_zipfile = ZipFile(BytesIO(response.content))
                my_zipfile.extractall(path=return_directory)
                return return_directory, my_zipfile.namelist()
            else:
                content_disposition = [item.strip().split("=") for item in
                                       response.headers["Content-Disposition"].split(";")]
                for item in content_type + content_disposition:
                    if len(item) == 2:
                        locals()[item[0]] = item[1]
                if "filename" in kwargs:
                    locals()["filename"] = kwargs["filename"]
                if not locals()["filename"]:
                    raise ValueError("Got data but couldn't find a filename for it.")
                with open(os.path.join(return_directory, locals()["filename"]),
                          mode="w", encoding=locals().get("charset", "utf-8")) as fh:
                    fh.write(response.text)
                    return return_directory, locals()["filename"]
        else:
            raise ValueError(f"Bad status code: {response.status_code}")
    except Exception as e:
        print(f"{e}")
        quit(1)


def main():
    DEFAULT_FORMAT = {
        "geoserver": "https://markfoley.info/geoserver",
        "workspace": "census2011",
        "dataset": "counties",
        "output_format": "SHAPE-ZIP"
    }

    geoserver_target = {}
    geoserver_target["geoserver"] = \
        input(f"Input Geoserver URL or press ENTER for {DEFAULT_FORMAT['geoserver']} ") or DEFAULT_FORMAT[
            'geoserver']
    geoserver_target["workspace"] = \
        input(f"Input Workspace or press ENTER for {DEFAULT_FORMAT['workspace']} ") or DEFAULT_FORMAT['workspace']
    geoserver_target["dataset"] = \
        input(f"Input Data Set or press ENTER for {DEFAULT_FORMAT['dataset']} ") or DEFAULT_FORMAT['dataset']
    geoserver_target["output_format"] = \
        input(f"Output Format or press ENTER for {DEFAULT_FORMAT['output_format']} ") or DEFAULT_FORMAT['output_format']
    geoserver_target["output_format"] = geoserver_target["output_format"].upper()

    my_temp_directory = get_temp(__file__)
    url = f"{geoserver_target['geoserver']}/{geoserver_target['workspace']}/ows?service=WFS&version=1.0.0&" \
          f"request=GetFeature&typeName={geoserver_target['workspace']}:{geoserver_target['dataset']}&" \
          f"outputFormat={geoserver_target['output_format']}"

    my_files = get_file_from_server(url, my_temp_directory)
    print(my_files)


if __name__ == '__main__':
    main()
