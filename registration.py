import tkinter.messagebox
import tkinter.simpledialog
import sqlite3
from datetime import datetime
from tkinter import *
from homepage import HomePage


class Registration(Toplevel):
    def __init__(self, reg):
        self.reg = reg
        Toplevel.__init__(self)

        self.title("Registration Form")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.frame = Frame(self)
        self.frame.pack()

        upperframe = Frame(self.frame)
        upperframe.pack(side=TOP, padx=10, pady=10)

        lbl1 = Label(upperframe, text="IdeaPad", font=("Verdana", 20, "bold"))
        lbl1.pack(pady=5)
        lbl2 = Label(upperframe, text="Welcome, please enter your username and password.")
        lbl2.pack(side=TOP, padx=10, pady=10)

        # Adding a frame that occupies the bottom half of the window and its content

        lowerframe = Frame(self.frame)
        lowerframe.pack(side=TOP, padx=10, pady=10)

        un = Label(lowerframe, text="Username :", font=("Verdana", 15, "normal"), anchor=W)
        un.grid(row=0, column=0, sticky=E, padx=60, pady=10)

        self.usernamer = Entry(lowerframe, width=20, font=("normal", 15, "normal"))
        self.usernamer.grid(row=0, column=1, sticky=E, padx=60, pady=10, ipadx=10, ipady=2)

        ps = Label(lowerframe, text="Password :", font=("Verdana", 15, "normal"), anchor=W)
        ps.grid(row=1, column=0, sticky=E, padx=60, pady=10)

        self.passwordr = Entry(lowerframe, width=20, font=("normal", 15, "normal"), show="*")
        self.passwordr.grid(row=1, column=1, sticky=E, padx=60, pady=10, ipadx=10, ipady=2)

        ps2 = Label(lowerframe, text="Password :", font=("Verdana", 15, "normal"), anchor=W)
        ps2.grid(row=2, column=0, sticky=E, padx=60, pady=10)

        self.password2 = Entry(lowerframe, width=20, font=("normal", 15, "normal"), show="*")
        self.password2.grid(row=2, column=1, sticky=E, padx=60, pady=10, ipadx=10, ipady=2)

        submit = Button(lowerframe, text="Submit", bg="green", fg="white", width=10, font=("Verdana", 12, "bold"),
                        command=self.submit)
        submit.grid(row=3, column=1, sticky=W, padx=60, pady=60)

    def fetchdata(self, user):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT id FROM users WHERE username=?"
        details = cursor.execute(query, (user,))
        data = details.fetchone()
        result = (int(data[0]), user)
        connection.close()
        return result

    def submit(self):
        one = str(self.passwordr.get())
        two = str(self.password2.get())

        if one == two:

            if tkinter.messagebox.askyesno("Register", "Are you sure you want to register this account"):
                username = str((self.usernamer.get()).lower())
                password = str((self.passwordr.get()).lower())
                time = str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

                connection = sqlite3.connect("data.db")
                cursor = connection.cursor()

                cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (username, password, time))
                connection.commit()
                connection.close()

                tkinter.messagebox.showinfo("Success", "Registration Successful!")
                result = self.fetchdata(username)
                self.destroy()
                HomePage(self.reg, *result)

        else:
            tkinter.messagebox.showinfo("Incorrect" "The two passwords did not match, please enter matching passwords")
            pass

    def on_exit(self):
        self.destroy()
        self.reg.show()
