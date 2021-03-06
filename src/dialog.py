import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

root = tk.Tk()
root.withdraw()

def open_dialog(caption="Open File",wildcard="All Files|*.*",defaultDir=""):
    return filedialog.askopenfilename(initialdir=defaultDir,title=caption,filetypes=wildcard)

def save_dialog(caption="Save File",wildcard="All Files|*.*",defaultDir=""):
    return filedialog.asksaveasfilename(initialdir=defaultDir,title=caption,filetypes=wildcard)

def info_dialog(message,caption=""):
    return messagebox.showinfo(title=caption,message=message)

def error_dialog(message,caption=""):
    return messagebox.showerror(title=caption,message=message)

def yes_no_dialog(message,caption=""):
    return messagebox.askyesno(title=caption,message=message)

def float_input_dialog(message,caption="",minvalue=None,maxvalue=None):
    return simpledialog.askfloat(title=caption,prompt=message,minvalue=minvalue,maxvalue=maxvalue)