"""
Program to illustrate GUI programming with Tkinter by showing various widgets in action:

* Menu
* Frame
* Status bar
* ScrolledText
* Canvas
* Image

Mark Foley
March 2021
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
# import PIL.Image as Image
# import PIL.ImageDraw as ImageDraw


class MyGUI(tk.Tk):
    """
    All of the GUI stuff lives here
    """

    def __init__(self, gui_settings):
        """
        All of the GUI 'look' lives here.
        """
        super().__init__()

        # Configure basic window options
        for k, v in gui_settings.items():
            setattr(self, k, v)
        self.title(self.title_text)
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(self.resizable_width, self.resizable_height)

        # Make protocol handler to manage interaction between the application and the window handler
        self.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self.padding = {
            'padx': 5,
            'pady': 5,
            'ipadx': 5,
            'ipady': 5,
        }
        self.chosen_file = tk.StringVar()

        self.create_text_menu()

        self.frame1 = ttk.Frame(
            self,
            width=self.width,
            height=self.height - ((self.padding["pady"] * 2) + (self.padding["ipady"] * 2))
        ).grid(row=0, column=0)

        self.statusbar = ttk.Label(
            self,
            textvariable=self.chosen_file,
            relief=tk.SUNKEN,
            anchor=tk.W,
        ).grid(row=1, column=0, sticky="ew", ipadx=10)

        self.notebook = ttk.Notebook(
            self.frame1,
            width=self.width,
            height=self.height - ((self.padding["pady"] * 6) + (self.padding["ipady"] * 6))
        )
        self.notebook.bind("<ButtonRelease>", self.tab_changed)
        self.notebook.grid(row=0, column=0)

        self.scrolled_text1 = ScrolledText(self.notebook)
        self.scrolled_text1.grid(row=0, column=0, **self.padding, sticky="nwse")

        self.last_x = self.last_y = None
        self.canvas_1 = tk.Canvas(self.notebook, bg="white")
        self.canvas_1.bind("<B1-Motion>", self.draw_canvas)
        self.canvas_1.grid(row=0, column=0, **self.padding, sticky="nwse")

        self.notebook.add(self.scrolled_text1, text="Text Editor")
        self.notebook.add(self.canvas_1, text="Whiteboard")

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.destroy()

    def new_file(self):
        pass

    def open_file(self):
        # Can run file dialogue from anywhere
        chosen_file = filedialog.askopenfilename(filetypes=(("Python files", "*.py"),
                                                            ("Text files", "*.txt"),
                                                            ("Markdown files", "*.md;*.mkd"),
                                                            ("All files", "*.*")))
        self.chosen_file.set(chosen_file)

        with open(chosen_file, 'r') as fh:
            contents = fh.read()

        self.scrolled_text1.insert("1.0", contents)

    def clear_textbox(self):
        self.chosen_file.set("")
        self.scrolled_text1.delete("1.0", tk.END)

    def save_file_as(self):
        with filedialog.asksaveasfile(mode="w", defaultextension=".tksave") as fh:
            if not fh:
                return
            try:
                fh.write(self.scrolled_text1.get("1.0", tk.END))
            except Exception as e:
                self.show_info("Error", f"{e}")

    def show_info(self, title="Info", message="Nothing to show."):
        messagebox.showinfo(title, message)

    def draw_canvas(self, event):
        colour = "black"
        if self.last_x:
            if abs(self.last_x - event.x) > 10:
                self.last_x = None

        if self.last_y:
            if abs(self.last_y - event.y) > 10:
                self.last_y = None

        if self.last_x and self.last_y:
            self.canvas_1.create_line(self.last_x, self.last_y, event.x, event.y, fill=colour, width=5)

        self.last_x = event.x
        self.last_y = event.y

    def tab_changed(self, event):
        nb = self.notebook
        if nb.tab(nb.select(), "text") == "Text Editor":
            self.create_text_menu()

        elif nb.tab(nb.select(), "text") == "Whiteboard":
            self.create_canvas_menu()

        else:
            return

    def create_text_menu(self):
        # set up menu
        self.menubar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label="Open File", command=self.open_file)
        self.file_menu.add_command(label="Clear textbox", command=self.clear_textbox)
        self.file_menu.add_command(label="Save As...", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.catch_destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_command(label="Help",
                                 command=lambda: self.show_info(title="Help text", message=f"{__doc__}"))
        self.config(menu=self.menubar)

    def create_canvas_menu(self):
        # set up menu
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Clear Canvas", command=lambda: self.canvas_1.delete("all"))
        self.menubar.add_command(label="Help",
                                 command=lambda: self.show_info(title="Help text", message=f"{__doc__}"))
        self.config(menu=self.menubar)


def main():
    GUI_SETTINGS = {
        "width": 800,
        "height": 600,
        "status_bar_height": 10,
        "resizable_width": False,
        "resizable_height": False,
        "title_text": "Tk Demo - Various Widgets",
    }

    # root = tk.Tk()
    # root.withdraw()
    # my_file = filedialog.askopenfilename()
    # messagebox.showinfo("Title text", f"You chose {my_file}")
    # # Show window again
    # root.deiconify()

    app = MyGUI(GUI_SETTINGS)
    app.mainloop()


if __name__ == "__main__":
    main()
