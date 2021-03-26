__author__ = 'mark'

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class MyGUI:
    def __init__(self, parent):
        self.parent = parent

        self.parent.title("Tk in-class demo: Display text file contents")

        # Make protocol handler to manage interaction between the application and the window handler
        parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self.frame1 = Frame(self.parent, padx="5m", pady="5m")
        self.frame1.grid(row=0, column=0, sticky=NW+SE)

        self.label1 = Label(self.frame1, text="0/0 A first attempt at a GUI")
        self.label1.grid(row=0, column=0, sticky=W)

        self.label2 = Label(self.frame1, text="0/1 Stuff in row 0 col 1")
        self.label2.grid(row=0, column=1, sticky=W)
        self.label3 = Label(self.frame1, text="1/0 Stuff in row 1 col 0\nincluding a new line char")
        self.label3.grid(row=1, column=0, sticky=W)
        self.label4 = Label(self.frame1, text="2/0 A big long load of text that sapns two columns, etc. etc. .......... and even more")
        self.label4.grid(row=2, column=0, columnspan=2, sticky=W+E)

        # set up menu
        self.menu = Menu(self.parent)

        self.file_menu = Menu(self.menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.catch_destroy)

        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.parent.config(menu=self.menu)

        self.chosen_file = StringVar()

        self.frame2 = ttk.Frame(self.parent, padding=5, borderwidth=2, relief="sunken", height=50, width=50 )
        self.frame2.grid(row=1, column=0, sticky=NW+SE)

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()

    def open_file(self):
        # Can run file dialogue from anywhere
        chosen_file = filedialog.askopenfilename(filetypes=(("Python files", "*.py"),
                                                            ("Text files", "*.txt"),
                                                            ("Markdown files", "*.md;*.mkd"),
                                                            ("All files", "*.*") ))
        self.chosen_file.set(chosen_file)

        print("You pressed File->Open\n{}".format(chosen_file))




def main():
    root = Tk()
    MyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()