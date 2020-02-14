import tkinter.messagebox
import tkinter.simpledialog
import os
import sqlite3

from tkinter import *
from view import View
from edit import Edit
from add import Add


class HomePage(Toplevel):
    def __init__(self, login, _id, user):
        self.id = _id
        self.username = user
        self.login = login
        Toplevel.__init__(self)
        self.title("IdealPad")
        self.geometry("720x720")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.value = ""
        self.two = ""
        self.ideaname = ""
        self.ideatime = ""

        ##############################################################################################################

        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.frame = Frame(self)
        self.frame.pack()

        self.uframe = Frame(self.frame)
        self.uframe.pack(side=TOP, padx=10, pady=10)

        self.mframe = Frame(self.frame)
        self.mframe.pack(side=TOP, padx=10, pady=10)

        self.bframe = Frame(self.frame)
        self.bframe.pack(side=TOP, padx=10, pady=10)

        ###############################################################################################################

        self.filetab = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filetab)
        self.filetab.add_command(label="New", command=self.addnew)
        self.filetab.add_separator()
        self.filetab.add_command(label="Exit", command=self.exit)

        self.helptab = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helptab)
        self.helptab.add_command(label="About", command=self.about)

        ##############################################################################################################

        self.wlabel = Label(self.uframe, text=f"Welcome {self.username}", font=("Verdana", 20, "normal"),
                            fg="green", anchor=W)
        self.wlabel.pack(side=TOP, padx=60, pady=10, fill=X)

        self.new_entry = Button(self.uframe, text="New", width=10, font=("normal", 15, "normal"), fg="white",
                                bg="grey", command=self.addnew)
        self.new_entry.pack(side=LEFT, padx=60, pady=30)

        self.refresh = Button(self.uframe, text="Refresh", width=10, font=("normal", 15, "normal"), fg="white",
                                bg="green", command=self.update_listbox)
        self.refresh.pack(side=LEFT, padx=60, pady=30)

        self.logoutbtn = Button(self.uframe, text="Logout", width=10, font=("normal", 15, "normal"), fg="white",
                                bg="red", command=self.logout)
        self.logoutbtn.pack(side=LEFT, padx=60, pady=30)

        ################################################################################################################

        self.text = Label(self.mframe, text="Idea List : ", font=("normal", 15, "normal"), anchor=W, width=70)
        self.text.pack(side=TOP, padx=60, pady=10, fill=X)

        self.idealist = Listbox(self.mframe, height=20)
        self.idealist.bind('<<ListboxSelect>>', self.cursorselect)
        self.idealist.pack(fill=X, pady=10, padx=60, side=TOP)

        ###############################################################################################################

        self.editbtn = Button(self.bframe, text="Edit", width=10, font=("normal", 15, "normal"), fg="white", bg="grey",
                              command=self.insertedit)
        self.editbtn.pack(side=LEFT, padx=60, pady=5)

        self.deletebtn = Button(self.bframe, text="Delete", width=10, font=("normal", 15, "normal"), fg="white",
                                bg="grey", command=self.deleteit)
        self.deletebtn.pack(side=LEFT, padx=60, pady=5)

        self.viewbtn = Button(self.bframe, text="View", width=10, font=("normal", 15, "normal"), fg="white", bg="grey",
                              command=self.insertview)
        self.viewbtn.pack(side=LEFT, padx=60, pady=5)

    ###################################################################################################################

    def cursorselect(self, event):
        try:
            self.value = self.idealist.get(self.idealist.curselection())
            self.two = self.value.split("|")
            self.ideaname = self.two[0]
            self.ideatime = self.two[1]
        except:
            pass

    def update_listbox(self):
        self.idealist.delete(0, END)
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT ideaname, ideatime FROM ideas WHERE id=?"
        data = cursor.execute(query, (self.id,))

        for row in data:
            self.idealist.insert(END, f"{row[0]}|{row[1]}")
        connection.close()

    ###################################################################################################################

    def fetchdet(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT ideatext FROM ideas WHERE ideatime=?"
        data = cursor.execute(query, (self.ideatime,))
        details = data.fetchone()
        result = (self.ideaname, details[0])
        connection.close()
        return result

    def insertview(self):
        data = self.fetchdet()
        self.withdraw()
        try:
            View(self, *data)
        except:
            pass

    def insertedit(self):
        data = self.fetchdet()
        self.withdraw()
        try:
            Edit(self, self.ideatime, *data)
        except:
            pass

    def addnew(self):
        self.withdraw()
        Add(self, self.id)

    ####################################################################################################################

    def on_exit(self):
        if tkinter.messagebox.askyesno("Exit", "Do you want to quit the application?"):
            self.quit()

    ###################################################################################################################

    """def viewidea(self):
        view = Toplevel()
        view.title("View Idea")
        view.geometry("720x720")
        view.protocol("WM_DELETE_WINDOW", self.on_exit)

        view.frame = Frame(view)
        view.frame.pack()

        view.uframe = Frame(view.frame)
        view.uframe.pack(side=TOP, padx=10, pady=10)

        view.mframe = Frame(view.frame)
        view.mframe.pack(side=TOP, padx=10, pady=10)

        view.bframe = Frame(view.frame)
        view.bframe.pack(side=TOP, padx=10, pady=10)

        name = Label(view.uframe, text=f"{self.ideaname}", font=("verdana", 15, "normal"), anchor=W)
        name.pack(side=LEFT, fill=X, padx=60, pady=10)

        textview = Message(view.mframe, text=f"{view.text}", font=("verdana", 15, "normal"))
        textview.pack(side=TOP, fill=X, padx=60, pady=60)

        self.value = ""
        self.two = ""
        self.ideaname = ""
        self.ideatime = ""

        close = Button(view.bframe, width=10, text="Close", font=("normal", 15, "normal"), bg="grey", fg="white",
                       command=lambda: view.destroy())
        close.pack(side=LEFT, padx=60, pady=10)"""

    ###################################################################################################################

    """def editidea(self):
        edit = Toplevel()
        edit.title("Edit Idea")
        edit.geometry("720x720")
        edit.protocol("WM_DELETE_WINDOW", self.on_exit_top)

        edit.frame = Frame(edit)
        edit.frame.pack()

        edit.uframe = Frame(edit.frame)
        edit.uframe.pack(side=TOP, padx=10, pady=10)

        edit.mframe = Frame(edit.frame)
        edit.mframe.pack(side=TOP, padx=10, pady=10)

        edit.bframe = Frame(edit.frame)
        edit.bframe.pack(side=TOP, padx=10, pady=10)

        name = Label(edit.uframe, text="Idea Name : ", font=("verdana", 15, "normal"), anchor=W)
        name.pack(side=LEFT, padx=0, pady=10)

        self.nentry = Entry(edit.uframe, width=20, font=("verdana", 15, "normal"))
        self.nentry.pack(side=LEFT, padx=60, pady=10)
        self.nentry.insert(END, self.ideaname)

        textlabel = Label(edit.mframe, text="Idea Text : ", font=("verdana", 15, "normal"), anchor=W)
        textlabel.pack(side=TOP, padx=90, pady=10, fill=X)

        self.textentry = Text(edit.mframe, height=30)
        self.textentry.pack(fill=X, padx=60, pady=10, side=TOP)

        close = Button(edit.bframe, text="Close", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                       command=lambda: edit.destroy())
        close.pack(side=LEFT, padx=60, pady=5)

        save = Button(edit.bframe, text="Save", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                      command=self.submit_edit)
        save.pack(side=RIGHT, padx=60, pady=5)"""

    ###################################################################################################################

    """def addnew(self):
        add = Toplevel()

        add.title("New Idea")
        add.geometry("720x720")
        add.protocol("WM_DELETE_WINDOW", self.on_exit_top)

        add.frame = Frame(add)
        add.frame.pack()

        add.uframe = Frame(add.frame)
        add.uframe.pack(side=TOP, padx=10, pady=10)

        add.mframe = Frame(add.frame)
        add.mframe.pack(side=TOP, padx=10, pady=10)

        add.bframe = Frame(add.frame)
        add.bframe.pack(side=TOP, padx=10, pady=10)

        name = Label(add.uframe, text="Idea Name : ", font=("verdana", 15, "normal"), anchor=W)
        name.pack(side=LEFT, padx=0, pady=10)

        self.anentry = Entry(add.uframe, width=20, font=("verdana", 15, "normal"))
        self.anentry.pack(side=LEFT, padx=60, pady=10)

        textlabel = Label(add.mframe, text="Idea Text : ", font=("verdana", 15, "normal"), anchor=W)
        textlabel.pack(side=TOP, padx=90, pady=10, fill=X)

        self.atextentry = Text(add.mframe, height=30)
        self.atextentry.pack(fill=X, padx=60, pady=10, side=TOP)

        save = Button(add.bframe, text="Save", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                      command=self.submit_new)
        save.pack(side=RIGHT, padx=60, pady=5)

        close = Button(add.bframe, text="Close", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                       command=lambda: add.destroy())
        close.pack(side=LEFT, padx=60, pady=5)"""

    ###################################################################################################################

    def deleteit(self):

        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            query = "DELETE FROM ideas WHERE ideatime=?"

            cursor.execute(query, (self.ideatime,))
            connection.commit()
            connection.close()
        except:
            tkinter.messagebox.showinfo("Failed", "Unsuccessful!!!")
        else:
            tkinter.messagebox.showinfo("Deleted", "Your selected idea has been successfully deleted")
            self.update_listbox()

    ###################################################################################################################

    def logout(self):
        answer = tkinter.messagebox.askquestion(title="Logout", message="Are you sure you want to log out?")
        if answer == "yes":
            self.destroy()
            self.login.show()

    ####################################################################################################################

    @staticmethod
    def about():
        os.system("start about.txt")

    ###################################################################################################################

    def exit(self):
        answer = tkinter.messagebox.askquestion("Exit", "Do you want to exit this program?")
        if answer == "yes":
            self.quit()
        else:
            pass
