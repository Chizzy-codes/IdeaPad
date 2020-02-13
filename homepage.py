import tkinter.messagebox
import tkinter.simpledialog
import os
import sqlite3
from datetime import datetime
from tkinter import *


class HomePage(Toplevel):
    def __init__(self, _id, user):
        self.id = _id
        self.username = user
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
        self.filetab.add_command(label="Edit", command=self.edit)
        self.filetab.add_separator()
        self.filetab.add_command(label="Exit", command=self.exit)

        self.edittab = Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edittab)
        self.edittab.add_command(label="Find", command=self.find)

        self.helptab = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helptab)
        self.helptab.add_command(label="About", command=self.about)

        ##############################################################################################################

        self.wlabel = Label(self.uframe, text=f"Welcome {self.username}", font=("Verdana", 20, "normal"),
                            fg="green", anchor=W)
        self.wlabel.pack(side=TOP, padx=60, pady=10, fill=X)

        self.new_entry = Button(self.uframe, text="New", width=20, font=("normal", 15, "normal"), fg="white",
                                bg="grey", command=self.addnew)
        self.new_entry.pack(side=LEFT, padx=60, pady=30)

        self.logoutbtn = Button(self.uframe, text="Logout", width=20, font=("normal", 15, "normal"), fg="white",
                                bg="red", command=self.logout)
        self.logoutbtn.pack(side=RIGHT, padx=60, pady=30)

        ################################################################################################################

        self.text = Label(self.mframe, text="Idea List : ", font=("normal", 15, "normal"), anchor=W, width=70)
        self.text.pack(side=TOP, padx=60, pady=10, fill=X)

        self.idealist = Listbox(self.mframe, height=20)
        self.idealist.bind('<<ListboxSelect>>', self.cursorselect)
        self.idealist.pack(fill=X, pady=10, padx=60, side=TOP)

        ###############################################################################################################

        self.editbtn = Button(self.bframe, text="Edit", width=10, font=("normal", 15, "normal"), fg="white", bg="grey",
                              command=self.editidea)
        self.editbtn.pack(side=LEFT, padx=60, pady=5)

        self.deletebtn = Button(self.bframe, text="Delete", width=10, font=("normal", 15, "normal"), fg="white",
                                bg="grey", command=self.deleteit)
        self.deletebtn.pack(side=LEFT, padx=60, pady=5)

        self.viewbtn = Button(self.bframe, text="View", width=10, font=("normal", 15, "normal"), fg="white", bg="grey",
                              command=self.viewidea)
        self.viewbtn.pack(side=LEFT, padx=60, pady=5)

    ###################################################################################################################

    def update_listbox(self):
        self.idealist.delete(0, END)
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        data = cursor.execute(f"SELECT ideaname, ideatime FROM ideas WHERE id='{self.id}'")

        for row in data:
            self.idealist.insert(END, f"{row[0]} | {row[1]}")
        connection.close()

    def upgrade(self):
        # this function updates and runs the home window
        self.update()

    ###################################################################################################################

    def on_exit_top(self):
        if tkinter.messagebox.askyesno("Exit", "Do you want to save your changes before you exit?"):
            self.upgrade()
            self.quit()
        else:
            self.quit()

    def tbinsert(self):
        con = sqlite3.connect("data.db")
        cur = con.cursor()

        cur.execute(f"SELECT ideatext FROM ideas WHERE user='{self.username}' AND ideatime='{self.ideatime}'")
        data = cur.fetchall()
        for row in data:
            self.tbinput = row[0]
            print(self.tbinput)
            self.textentry.insert(END, self.tbinput)
        con.commit()
        con.close()

    ####################################################################################################################

    def on_exit(self):
        if tkinter.messagebox.askyesno("Exit", "Do you want to quit the application?"):
            self.quit()

    ####################################################################################################################

    def submit_new(self):
        time = str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        name = self.anentry.get()
        text = self.atextentry.get("1.0", END)
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO ideas VALUES(?, ?, ?, ?)", (self.username, name, text, time))
            connection.commit()
            connection.close()
        except:
            tkinter.messagebox.showinfo("Failed", "Not successful!!!")
        finally:
            self.update_listbox()

    def submit_edit(self):
        name = self.nentry.get()
        text = self.textentry.get("1.0", END)
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        try:
            cursor.execute(f"UPDATE ideas SET ideaname='{name}' WHERE ideatime='{self.ideatime}'")
            cursor.execute(f"UPDATE ideas SET ideatext='{text}' WHERE ideatime='{self.ideatime}'")

        except:
            tkinter.messagebox.showinfo("Failed", "Not successful!!!")
            connection.commit()
            connection.close()
        finally:
            self.update_listbox()

    def cursorselect(self, event):
        self.value = self.idealist.get(self.idealist.curselection())
        self.two = self.value.split("|")
        self.ideaname = self.two[0]
        self.ideatime = self.two[1]

    ###################################################################################################################

    def viewidea(self):
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

        connect = sqlite3.connect("data.")
        curs = connect.cursor()

        data = curs.execute(f"SELECT ideatext FROM ideas WHERE user='{self.username}' AND ideatime='{self.ideatime}'")

        name = Label(view.uframe, text=f"{self.ideaname}", font=("verdana", 15, "normal"), anchor=W)
        name.pack(side=LEFT, fill=X, padx=60, pady=10)

        for row in data:
            view.text = row[0]
        textview = Message(view.mframe, text=f"{view.text}", font=("verdana", 15, "normal"))
        textview.pack(side=TOP, fill=X, padx=60, pady=60)
        connect.commit()
        connect.close()

        self.value = ""
        self.two = ""
        self.ideaname = ""
        self.ideatime = ""

        close = Button(view.bframe, width=10, text="Close", font=("normal", 15, "normal"), bg="grey", fg="white",
                       command=lambda: view.destroy())
        close.pack(side=LEFT, padx=60, pady=10)

    ###################################################################################################################

    def editidea(self):
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
        self.tbinsert()

        close = Button(edit.bframe, text="Close", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                       command=lambda: edit.destroy())
        close.pack(side=LEFT, padx=60, pady=5)

        save = Button(edit.bframe, text="Save", width=10, font=("normal", 15, "normal"), bg="grey", fg="white",
                      command=self.submit_edit)
        save.pack(side=RIGHT, padx=60, pady=5)

    ###################################################################################################################

    def addnew(self):
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
        close.pack(side=LEFT, padx=60, pady=5)

    ###################################################################################################################

    def deleteit(self):
        time = self.ideatime
        print(time)
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        try:
            cursor.execute(f"DELETE FROM ideas WHERE ideatime = '{time}'' and user='{self.username}'")
            connection.commit()
            connection.close()
        except:
            pass
        else:
            tkinter.messagebox.showinfo("Deleted", "Your selected idea has been successfully deleted")
            self.update_listbox()

    ###################################################################################################################

    def logout(self):
        answer = tkinter.messagebox.askquestion(title="Logout", message="Are you sure you want to log out?")
        if answer == "yes":
            self.destroy()

    ####################################################################################################################

    @staticmethod
    def about():
        os.system("start about.txt")

    ####################################################################################################################

    def find(self):

        answer = str(tkinter.simpledialog.askstring(title="Find",
                                                    prompt="Enter the name of the idea that you want to view",
                                                    parent=self))
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        try:
            data = cursor.execute(f"SELECT * FROM ideas WHERE user='{self.username}' AND ideaname='{answer}'")
            for row in data:
                self.ideaname = row[0]
                self.ideatime = row[2]
        except:
            tkinter.messagebox.showinfo("Not Found", "Sorry, no idea with the name you entered exist")

        connection.commit()
        connection.close()

        self.viewidea()

    ###################################################################################################################

    def edit(self):
        answer = tkinter.simpledialog.askstring(title="Edit",
                                                prompt="Enter the name of the idea that you want to edit",
                                                parent=self)

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        try:
            data = cursor.execute(f"SELECT * FROM ideas WHERE user='{self.username}' AND ideaname='{answer}'")
            for row in data:
                self.ideaname = row[0]
                self.ideatime = row[2]
        except:
            tkinter.messagebox.showinfo("Not Found", "Sorry, no idea with the name you entered exists")

        connection.commit()
        connection.close()

        self.editidea()

    ###################################################################################################################

    def exit(self):
        answer = tkinter.messagebox.askquestion("Exit", "Do you want to exit this program?")
        if answer == "yes":
            self.quit()
        else:
            pass
