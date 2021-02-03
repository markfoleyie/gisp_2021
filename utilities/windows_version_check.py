"""
Check to see what type of Python/Windows you are running (32/64-bit), Python 3.x and, therefore, which GIS-related
binaries (wheel files) you need.

Relevant to MS Windows users only.

Mark Foley
Feb 2020, modified Jan 2021
"""

import os, sys, struct
import getpass
import requests
import pip

# Where we go to get the required libraries
WIN_BINARIES_DIR = "https://www.lfd.uci.edu/~gohlke/pythonlibs/"

# Where we store the full local path to each library
TEMP_FILE = "required_spatial_libraries.txt"

# The current user (you)
USER = getpass.getuser()


def run_check():
    # MS Windows only.
    if os.name != "nt":
        print("You are not running MS Windows. This check is relevant to MS Windows machines only.")
        quit(0)

    # Current libraries and their versions
    LIBRARIES = {
        "GDAL": "3.0.4",
        "Fiona": "1.8.13",
        "Shapely": "1.7.1",
        "pyproj": "3.0.0.post1"
    }
    OTHER_PACKAGES = (
        "requests",
        "psycopg2"
    )

    try:
        # Find out where your Downloads directory is
        DOWNLOADS_DIRECTORY = get_downloads_folder()

        # Make/set a temporary directory to store TEMP_FILE. This can be thrown away when finisshed.
        temp_dir = make_temp_dir("temp")
        temp_file = f"{temp_dir}/{TEMP_FILE}"

        # Create (open and close) temp file. Also include "standard" packages
        with open(temp_file, "w") as fh:
            for package in OTHER_PACKAGES:
                fh.write(f"{package}\n")

        # Figure out your Python version
        print(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        if sys.version_info.minor != 6:
            print(f"You should make sure that you are running Python 3.6.x where x is anything.\n")
            quit(0)
        python_ver = f"cp{sys.version_info.major}{sys.version_info.minor}"
        python_ver_modifier = "" if sys.version_info.minor > 7 else "m"

        # Figure out whether this is a 32- or 64-bit system
        if struct.calcsize("P") * 8 == 32:
            win_bit = "win32"
        elif struct.calcsize("P") * 8 == 64:
            win_bit = "win_amd64"
        else:
            win_bit = ""

        # Show instructions
        print(f"Looks like you're running {struct.calcsize('P') * 8}-bit MS Windows\n"
              f"Go to {WIN_BINARIES_DIR} and download:")
        for k, v in LIBRARIES.items():
            item = f"{k}-{v}-{python_ver}-{python_ver}{python_ver_modifier}-{win_bit}.whl"
            print(f"   {item}")

            # # These are not working at the moment due to limitations on the UCI site.
            # download_library(DOWNLOADS_DIRECTORY, item)
            # install_package(f"{DOWNLOADS_DIRECTORY}/{item}")

            # Update the temp file with customised locations for the libraries. Use this to feed 'pip install'.
            with open(temp_file, "a+") as fh:
                fh.write(f"{DOWNLOADS_DIRECTORY}\{item}\n")

        # # Instructions for each library
        # print("\nRun the following commands in Terminal (assuming that you have downloaded the files in a standard "
        #       "way and they exist in your Downloads directory):\n")
        # with open(temp_file, "r") as fh:
        #     for line in fh:
        #         print(f"pip install {line}", end="")

        # Check file existence
        print("\nI'm now going to check whether the libraries exist on this computer...", end="\n")
        with open(temp_file, "r") as fh:
            for line in fh:
                if line[1] == ":":
                    if os.path.exists(line.strip()):
                        print(f"{line.strip()} exists.")
                    else:
                        print(f"{line.strip()} does NOT exist (at least not in {DOWNLOADS_DIRECTORY}).")

        # Installation instructions
        print(f"Make sure that you have downloaded the libraries indicated above.\n"
              f"Run this command in Terminal...\n"
              f"pip install -r {temp_file}")



    except Exception as e:
        print(f"Something bad happened!\n{e}")
        quit(1)


def get_downloads_folder():
    """
    Returns the default downloads path for linux or windows
    """

    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


def download_library(downloads_folder, library):
    """
    Downloads a library file from the Net

    :param downloads_folder: Your local Downloads folder
    :param library: The required library
    :return: None
    """

    url = f"{WIN_BINARIES_DIR}{library}"
    try:
        lib = requests.get(url, allow_redirects=True)

        if lib.status_code > 399:
            raise Exception(f"Bad http status code: {lib.status_code}")

        with open(f"{downloads_folder}{library}", "wb") as fh:
            fh.write(lib.content)
    except Exception as e:
        print(f"Something bad happened!\n{e}")
        quit(2)


def install_package(package):
    """
    Installs a library (package) using Pip

    :param package: The library file (usually a wheel) to install
    :return: None
    """

    print(f"Installing {package}")
    try:
        if hasattr(pip, 'main'):
            pip.main(['install', package])
        else:
            pip._internal.main(['install', package])
    except Exception as e:
        print(f"Couldn't install {package}: {e}")


def make_temp_dir(temp_name):
    """
    Creates a temporary directory in the current directory (where this Python program is located). This is prepended
    with a dot to indicate that it is temporary and can be deleted without loss.

    :param temp_name: Name of temp directory (without dot)
    :return: Path to temp directory
    """

    script_dir = os.path.dirname(__file__)
    cache_dir = os.path.join(script_dir, f".{temp_name}")
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    return cache_dir


if __name__ == "__main__":
    # Start point
    run_check()
