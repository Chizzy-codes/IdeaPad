from tkinter import *


class View(Toplevel):
    def __init__(self, home, name, text):
        self.original = home
        self.name = name
        self.text = text
        Toplevel.__init__(self)
        self.title("View Idea")
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

        self.ideaname = Label(self.uframe, text=f"{self.name}", font=("verdana", 15, "normal"), anchor=W)
        self.ideaname.pack(side=LEFT, fill=X, padx=60, pady=10)

        textview = Message(self.mframe, text=f"{self.text}", font=("verdana", 15, "normal"))
        textview.pack(side=TOP, fill=X, padx=60, pady=60)

        close = Button(self.bframe, width=10, text="Close", font=("normal", 15, "normal"), bg="grey", fg="white",
                       command=self.on_exit)
        close.pack(side=LEFT, padx=60, pady=10)

    def on_exit(self):
        self.destroy()
        self.original.deiconify()
