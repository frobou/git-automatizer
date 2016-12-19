# -*- coding: utf-8 -*-
try:
    from Tkinter import *  # for Python2
except ImportError:
    from tkinter import *  # for Python3


class Application(object):
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack()
        self.msg = Label(self.widget1, text="Primeiro widget")
        self.msg.pack()
        self.sair = Button(self.widget1)
        self.sair["text"] = "Sair"
        self.sair["font"] = ("Calibri", "10")
        self.sair["width"] = 5
        self.sair["command"] = self.widget1.quit
        self.sair.pack()


root = Tk()
Application(root)
root.mainloop()
