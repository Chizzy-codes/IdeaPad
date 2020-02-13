import tkinter.messagebox
import tkinter.simpledialog
import sqlite3

from homepage import HomePage
from registration import Registration
from tkinter import *
from data import create_tables


class Application:
    def __init__(self, parent):
        # Initialising the login page
        self.master = parent
        self.master.title("IdeaPad")
        self.frame = Frame(self.master)
        self.frame.pack()

        # packing the frame which covers the entire window
        # Adding a frame that occupies the top half of the window and its content

        ###############################################################################################################

        self.upperframe = Frame(self.frame)
        self.upperframe.pack(side=TOP, padx=10, pady=10)

        ###############################################################################################################

        self.lbl1 = Label(self.upperframe, text="IdeaPad", font=("Verdana", 20, "bold"))
        self.lbl1.pack(pady=5)
        self.lbl2 = Label(self.upperframe,
                          text="Welcome, please enter your username and password. If new click 'Register'.")
        self.lbl2.pack(side=TOP, padx=10, pady=10)

        # Adding a frame that occupies the bottom half of the window and its content

        self.lowerframe = Frame(self.frame)
        self.lowerframe.pack(side=TOP, padx=10, pady=10)

        ###############################################################################################################

        self.un = Label(self.lowerframe, text="Username :", font=("Verdana", 15, "normal"), anchor=W)
        self.un.grid(row=0, column=0, sticky=E, padx=60, pady=10)

        self.username = Entry(self.lowerframe, width=20, font=("normal", 15, "normal"))
        self.username.grid(row=0, column=1, sticky=E, padx=60, pady=10, ipadx=10, ipady=2)

        self.ps = Label(self.lowerframe, text="Password :", font=("Verdana", 15, "normal"), anchor=W)
        self.ps.grid(row=1, column=0, sticky=E, padx=60, pady=10)

        self.password = Entry(self.lowerframe, width=20, font=("normal", 15, "normal"), show="*")
        self.password.grid(row=1, column=1, sticky=E, padx=60, pady=10, ipadx=10, ipady=2)

        ###############################################################################################################

        self.login = Button(self.lowerframe, text="Login", bg="blue", fg="white", width=10,
                            font=("Verdana", 12, "bold"),
                            command=self.start_app)
        self.login.grid(row=2, column=1, sticky=W, padx=60, pady=60)

        self.register = Button(self.lowerframe, text="Register", bg="green", fg="white", width=10,
                               font=("Verdana", 12, "bold"),
                               command=self.reg)
        self.register.grid(row=2, column=0, sticky=E, padx=0, pady=60)

    ####################################################################################################################
    def fetch(self, user):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT id FROM users WHERE username=?"
        details = cursor.execute(query, (user,))
        data = details.fetchone()
        result = (int(data[0]), user)
        connection.close()
        return result

    def start_app(self):
        # this function initialises the homepage window
        username = str((self.username.get()).lower())
        password = str((self.password.get()).lower())
        check = (username, password)

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        data = cursor.execute("SELECT username, password FROM users")
        for row in data:
            if check == row:
                tkinter.messagebox.showinfo("Success", "Login Successful!!!")
                result = self.fetch(username)
                self.master.withdraw()
                home = HomePage(*result)
                HomePage.update_listbox(home)
                break

            else:
                tkinter.messagebox.showinfo("Failed", "Username or password entered is incorrect. Try again")

        connection.close()

    def reg(self):
        self.master.withdraw()
        create_tables()
        Registration()

    def show(self):
        # this function updates and runs the first window(the login window...i think)
        self.master.update()
        self.username.delete(0, END)
        self.password.delete(0, END)
        self.master.deiconify()


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
