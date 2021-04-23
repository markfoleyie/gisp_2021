"""
Spatial Analysis with Python
============================
You are required to write a program that performs basic spatial analysis on a Polygon feature set and Point feature set.
You should get these from Geoserver in GeoJSON format. I haven't specified which layers to use - I'll leave that as a
choice for you. There is a selection of datasets on https://markfoley.info/geoserver/. Look for layers in the census2011,
census2016 and TUDublin workspaces. Consider which point and polygon datasets would match.

Specifically, we want to do the following:

    Create a single polygon from the Union of all the polygons.
    Compute the centroid of the single polygon.
    Extract the points that lie within the single polygon.
    Compute a convex hull and centroid for the extracted points
    Compute the distance between the centroid of the single polygon and the centroid of the points that lie within the
    single polygon.
    Create a representation of the line joining the two centroids
    Geocode both centroids and add their names to the appropriate point as an attribute
    Create shapefiles to store the results of the above. Bear in mind that a shapefile contains a single geometry type
    and is a set of thematically related features. Therefore you will need to create shapefiles as follows:
        Combined polygon from Union
        Points that lie within Combined Polygon
        Convex hull of the points from above
        Both centroids. Each should have an attribute to hold its name returned from the geocoding process.
        Linestring representing the distance between the centroids

You should also create a graphical user interface (GUI) to facilitate interaction with your program. This should
facilitate the selection of the source server and datasets and present a summary of your results.

The user can then use any GIS application such as ArcGIS or QGIS to display the resulting shapefiles.

To get you started, I have created some useful Python modules in the utilities folder on GitHub. Among other things,
these have functions which implement the process of accessing GeoJSON data from Geoserver. Get these and study how they
work. You should be able to import any of these directly into your program.

"""

import tkinter as tk
from tkinter.font import Font, BOLD
from tkinter import ttk
from tkinter import messagebox
from tkinter import TclError
from tkinter import scrolledtext as st

# Don't forget to look in 'utilities' for useful functions that I have given you. If you add these files to your project
# you can import them.

# Constants to be used both in GUI and non-GUI (can be modified).
DEFAULTS = {
    "HOST": "https://markfoley.info/geoserver",
    "TEMP_DIR": ".ca2_temp",
    "WORKSPACE_POLYS": "census2011",
    "DATASET_POLYS": "counties",
    "WORKSPACE_POINTS": "TUDublin",
    "DATASET_POINTS": "geonames_ie",
    "POLYS_CQL_FILTER": "nuts3name = 'Dublin'",
    "POINTS_CQL_FILTER": "featurecode = 'PPL' AND population > 1000",
    "SRS_CODE": 29903
}


def do_analysis(**defaults):
    """
    All 'real work' happens here. We take in any (modified) defaults as our starting parameters.

    :param defaults: The elements we are going to work with such as Geoserver datasets, SRS code, CQL filters etc.
    :return: None
    """
    # Make result log to be printed at the end. Information will be added to this as we proceed.
    result_log = ""

    # Do analysis here.

    # Get data from Geoerver. Note that we use the same SRS for both and the we filter based on required polygons and
    # points with population greater than a specified amount. Take note of 'download_from_geoserver' in 'utilities'.

    # return log of results. This can be printed to the console or written to the scrolledtext element in the GUI.
    return result_log


def main():
    """
    The 'main' part of the program. This runs when a GUI is not used.

    :return: None
    """

    # Some sensible defaults - to pre-populate 'input' statements - saves a lot of typing!
    defaults = {}
    defaults["HOST"] = input(f"Input Geoserver URL or press ENTER for {DEFAULTS['HOST']} ") or DEFAULTS['HOST']
    defaults["TEMP_DIR"] = input(f"Input Temp Directory or press ENTER for {DEFAULTS['TEMP_DIR']} ") or DEFAULTS[
        'TEMP_DIR']
    defaults["WORKSPACE_POLYS"] = input(f"Input Polygon workspace or press ENTER for {DEFAULTS['WORKSPACE_POLYS']} ") or \
                                  DEFAULTS['WORKSPACE_POLYS']
    defaults["DATASET_POLYS"] = input(f"Input Polygon dataset or press ENTER for {DEFAULTS['DATASET_POLYS']} ") or \
                                DEFAULTS['DATASET_POLYS']
    defaults["WORKSPACE_POINTS"] = input(
        f"Input Points workspace or press ENTER for {DEFAULTS['WORKSPACE_POINTS']} ") or DEFAULTS['WORKSPACE_POINTS']
    defaults["DATASET_POINTS"] = input(f"Input Points dataset or press ENTER for {DEFAULTS['DATASET_POINTS']} ") or \
                                 DEFAULTS['DATASET_POINTS']
    defaults["POLYS_CQL_FILTER"] = input(
        f"Input Polygon CQL filter or press ENTER for {DEFAULTS['POLYS_CQL_FILTER']} ") or DEFAULTS['POLYS_CQL_FILTER']
    defaults["POINTS_CQL_FILTER"] = input(
        f"Input Points CQL filter or press ENTER for {DEFAULTS['POINTS_CQL_FILTER']} ") or DEFAULTS['POINTS_CQL_FILTER']
    defaults["SRS_CODE"] = input(f"Input SRS code or press ENTER for {DEFAULTS['SRS_CODE']} ") or DEFAULTS['SRS_CODE']

    # Do the actual spatial work.
    result = do_analysis(**defaults)
    print(result)


def main_gui():
    # Contain top level window usually called root
    root = tk.Tk()

    # Create an instance of the class that defines the GUI and associate it with the top level window..
    GUI(root, **DEFAULTS)

    # Keep listening for events until destroy event occurs.
    root.mainloop()


class GUI:
    """
    This class contains all GUI-related logic in your program.
    """
    def __init__(self, parent, **defaults):
        """
        The design of your GUI is created here.

        :param parent: a 'tk' object usually called root in the main function.
        :param defaults: a set of sensible defaults used to populate adat entry widgets - this saves a lot of typing!
        """

        # the tk object
        self.parent = parent

        # Create a bunch of 'StringVar' elements which can be monitered by Entry widgets. These are populated by
        # defaults.
        try:
            self.defaults = {}
            for k, v in DEFAULTS.items():
                self.defaults[k.lower()] = tk.StringVar()
                self.defaults[k.lower()].set(v)
        except Exception as e:
            print(f"{e}")
            return

        self.parent.title("GIS Programming Assignment 2021")

        # Make protocol handler to manage interaction between the application and the window handler
        parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        # Don't allow 'tear-off' menus
        self.parent.option_add('*tearOff', tk.FALSE)

        # Example of how to set up a menu. This adds 'self.menu' - the menubar with 'file' and 'self.file_menu' - the
        # drop-down choice which only gives 'Exit' as  an option.
        self.menu = tk.Menu(self.parent)

        self.file_menu = tk.Menu(self.menu)
        self.file_menu.add_command(label="Exit", command=self.catch_destroy)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.parent.config(menu=self.menu)

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()

    def run_analysis(self):
        """
        This is the method that is fired when the 'RUN' button is pressed. All it needs to do is call the 'do_analysis'
        function and wiite any results to the scrolledtext widget.

        :return: None
        """

        # Insert any preamble into the scrolledtext widget. Inserting text is a little fiddly so the following
        # (commented out) example illustrates how it works. It assumes the presence of a scrolledtext widget called
        # 'self.text1'. As this doesn't exist yet, I've commented out the example to avoid errors. This just goes
        # through the defaults and adds some text about each one to the widget.
        #
        # Note 'tk.END' means the end-point of any existing text in the widget. It's a bit like placig the cusror at the
        # end of a text document in Notepad and adding from there.

        # self.text1.insert(tk.END, f"{'-' * 60}\n")
        # for k in self.defaults:
        #     DEFAULTS[k.upper()] = self.defaults[k].get()
        #     self.text1.insert(tk.END, f"{k}: {self.defaults[k].get()}\n")

        # Do actual spatial analysis
        result = do_analysis(**self.defaults)

        # Write results to scrolledtext widget


if __name__ == "__main__":
    # main()
    main_gui()
