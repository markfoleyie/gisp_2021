from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class GUI:
    def __init__(self, parent):
        self.parent = parent

        self.parent.title("Tk in-class demo: Display text file contents")

        # Make protocol handler to manage interaction between the application and the window handler
        self.parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        # Don't allow 'tear-off' menus
        self.parent.option_add('*tearOff', FALSE)

        # set up menu
        self.menu = Menu(self.parent)

        self.file_menu = Menu(self.menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.catch_destroy)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.parent.config(menu=self.menu)

        # make a frame to hold everything, initially at least
        self.frame1 = ttk.Frame(parent, padding=5, border=1)
        self.frame1.grid(row=0, column=0)

        # String variable to hold contents to be displayed. StringVar() has the logic to monitor changes in content and
        # thus is useful when we want to dynamically update widget contents.
        self.chosen_file = StringVar()

        self.label1 = ttk.Label(self.frame1, textvariable=self.chosen_file)
        self.label1.grid(row=0, column=0, sticky=W + E)

        self.frame2 = ttk.Frame(parent, padding=5, border=1)
        self.frame2.grid(row=1, column=0)

        # Make a text widget and two scrollbars
        # To associate a scrollbar with a text widget, place the scrollbar carefully with
        # respect to the text widget and set the scrollbar's command to textwidget.{x/y}view
        # as appropriate. Then set the text widget's {x/y}scroolcommand to
        # scrollbal.set as below

        self.text1 = Text(self.frame2, width=100, wrap=NONE)
        self.yscrollbar = ttk.Scrollbar(self.frame2, orient=VERTICAL, command=self.text1.yview)
        self.yscrollbar.grid(column=1, row=1, sticky=NS)

        self.xscrollbar = ttk.Scrollbar(self.frame2, orient=HORIZONTAL, command=self.text1.xview)
        self.xscrollbar.grid(column=0, row=2, sticky=EW)

        self.text1['yscrollcommand'] = self.yscrollbar.set
        self.text1['xscrollcommand'] = self.xscrollbar.set
        self.text1.grid(row=1, column=0)

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()

    def open_file(self):
        # Can run file dialogue from anywhere
        chosen_file = filedialog.askopenfilename(filetypes=(("Python files", "*.py"),
                                                            ("Text files", "*.txt"),
                                                            ("Markdown files", "*.md;*.mkd"),
                                                            ("All files", "*.*")))
        self.chosen_file.set(chosen_file)

        print("Selected: {}".format(self.chosen_file.get()))

        with open(self.chosen_file.get(), "r") as input:
            file_contents = input.read()

        self.text1.insert(INSERT, file_contents)
        self.text1['state'] = 'disabled'


def main():
    # Contain top level window usually called root
    root = Tk()

    # Create an instance of the class that defines the GUI and associate it with the top level window..
    GUI(root)

    # Keep listening for events until destroy event occurs.
    root.mainloop()


if __name__ == "__main__":
    main()
