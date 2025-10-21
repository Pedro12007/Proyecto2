import tkinter as tk
import sqlite3


class Admin:
    def __init__(self):
        self.ventana_admin = tk.Tk()
        self.ventana_admin.title("Menú de administrador")
        self.ventana_admin.state("zoomed")
        self.ventana_admin.geometry('900x800')

