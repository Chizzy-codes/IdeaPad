import sqlite3
import tkinter.messagebox
from tkinter import *
from datetime import datetime


class Add(Toplevel):
    def __init__(self, home, _id):
        self.original = home
        self.id = _id
        Toplevel.__init__(self)
        self.title("New Idea")
        self.geometry("720x720")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.frame = Frame(self)
        self.frame.pack()

        self.uframe = Frame(self.frame)
        self.uframe.pack(side=TOP, padx=10, pady=10)

        self.mframe = Frame(self.frame)
        self.mframe.pack(side=TOP, padx=10, pady=10)

        self.bframe = Frame(self.frame)
        self.bframe.pack(side=TOP, padx=10, pady=10)

        self.lbname = Label(self.uframe, text="Idea Name : ", font=("verdana", 15, "normal"), anchor=W)
        self.lbname.pack(side=LEFT, padx=0, pady=10)

        self.anentry = Entry(self.uframe, width=20, font=("verdana", 15, "normal"))
        self.anentry.pack(side=LEFT, padx=60, pady=10)

        self.textlabel = Label(self.mframe, text="Idea Text : ", font=("verdana", 15, "normal"), anchor=W)
        self.textlabel.pack(side=TOP, padx=90, pady=10, fill=X)

        self.atextentry = Text(self.mframe, height=30)
        self.atextentry.pack(fill=X, padx=60, pady=10, side=TOP)

        save = Button(self.bframe, text="Save", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                      command=self.submit_new)
        save.pack(side=RIGHT, padx=60, pady=5)

        close = Button(self.bframe, text="Close", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                       command=self.on_exit)
        close.pack(side=LEFT, padx=60, pady=5)

    def on_exit(self):
        self.destroy()
        self.original.deiconify()

    def submit_new(self):
        name = str(self.anentry.get())
        text = str(self.atextentry.get("1.0", END))
        time = str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            query = "INSERT INTO ideas VALUES(?, ?, ?, ?)"

            cursor.execute(query, (self.id, name, text, time))
            connection.commit()
            connection.close()
        except:
            tkinter.messagebox.showinfo("Failed", "Submission Unsuccessful!!!")
        else:
            tkinter.messagebox.showinfo("Success", "Idea Successfully Saved!!!")
        self.on_exit()
