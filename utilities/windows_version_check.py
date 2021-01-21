"""
Check to see what type of Python/Windows you are running (32/64-bit), Python 3.x.
Relevant to MS Windows users only.

MF
Feb 2020, modified Jan 2021
"""
import os, sys, struct

WIN_BINARIES_DIR = "https://www.lfd.uci.edu/~gohlke/pythonlibs/"


def run_check():
    if os.name != "nt":
        print("You are not running MS Windows. This check is relevant to MS Windows machines only.")
        return

    LIBRARIES = {
        "GDAL": "3.2.1",
        "Fiona": "1.8.18",
        "Shapely": "1.7.1",
        "pyproj": "3.0.0.post1"
    }
    required_packages = []

    python_ver = f"cp{sys.version_info.major}{sys.version_info.minor}"
    python_ver_modifier = "" if sys.version_info.minor > 7 else "m"
    if struct.calcsize("P") * 8 == 32:
        win_bit = "win32"
    elif struct.calcsize("P") * 8 == 64:
        win_bit = "win_amd64"
    else:
        win_bit = ""

    print(f"Looks like you're running {struct.calcsize('P') * 8}-bit MS Windows\n"
          f"Go to {WIN_BINARIES_DIR} and download:")
    for k, v in LIBRARIES.items():
        item = f"{k}-{v}-{python_ver}{python_ver_modifier}-{win_bit}.whl"
        print(f"   {item}")
        required_packages.append(item)

    print("install these using... pip install <full/path/to/filename>\n"
          "e.g  pip install c:\\users\\fred\\Downloads\\GDAL-3.0.4-cp37m-win_amd64.whl")

    return tuple(required_packages)


if __name__ == "__main__":
    run_check()
