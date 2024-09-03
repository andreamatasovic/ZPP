from Container import *
from gui import *
from pars import *
from rules import *

from main_page import *
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()