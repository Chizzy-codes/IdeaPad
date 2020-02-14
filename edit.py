import sqlite3
import tkinter.messagebox
from tkinter import *


class Edit(Toplevel):
    def __init__(self, home, ideatime, name, text):
        self.original = home
        self.name = name
        self.text = text
        self.ideatime = ideatime
        Toplevel.__init__(self)
        self.title("Edit Idea")
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

        name = Label(self.uframe, text="Idea Name : ", font=("verdana", 15, "normal"), anchor=W)
        name.pack(side=LEFT, padx=0, pady=10)

        self.nentry = Entry(self.uframe, width=20, font=("verdana", 15, "normal"))
        self.nentry.pack(side=LEFT, padx=60, pady=10)
        self.nentry.insert(END, self.name)

        textlabel = Label(self.mframe, text="Idea Text : ", font=("verdana", 15, "normal"), anchor=W)
        textlabel.pack(side=TOP, padx=90, pady=10, fill=X)

        self.textentry = Text(self.mframe, height=30)
        self.textentry.pack(fill=X, padx=60, pady=10, side=TOP)
        self.textentry.insert(END, self.text)

        close = Button(self.bframe, text="Close", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                       command=self.on_exit)
        close.pack(side=LEFT, padx=60, pady=5)

        save = Button(self.bframe, text="Save", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                      command=self.submit_edit)
        save.pack(side=RIGHT, padx=60, pady=5)

    def submit_edit(self):
        name = str(self.nentry.get())
        text = str(self.textentry.get("1.0", END))

        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            query = "UPDATE ideas SET ideaname=?, ideatext=? WHERE ideatime=?"

            cursor.execute(query, (name, text, self.ideatime))
            conn.commit()
            conn.close()
        except:
            tkinter.messagebox.showinfo("Failed", "Submission Unsuccessful!!!")
        else:
            tkinter.messagebox.showinfo("Success", "Idea Successfully Updated!!!")
        self.on_exit()

    def on_exit(self):
        self.destroy()
        self.original.deiconify()
