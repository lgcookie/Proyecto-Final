from tkinter import messagebox
import peewee

def report_callback_exception(self,exc, val, tb):
    messagebox.showerror("Error", message=val)