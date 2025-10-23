import tkinter as tk
import sqlite3

class Admin:
    def __init__(self):
        self.ventana_admin = tk.Tk()
        self.ventana_admin.title("Menú de administrador")
        self.ventana_admin.state("zoomed")
        self.ventana_admin.geometry('900x800')

        tk.Button(self.ventana_admin, text="Agregar usuario", font=("Arial", 16), bg="white", fg="black").pack(pady=20)
        tk.Button(self.ventana_admin, text="Modificar datos de usuario", font=("Arial", 16), bg="white", fg="black").pack(pady=20)
        tk.Button(self.ventana_admin, text="Cerrar sesión", font=("Arial", 16), bg="white", fg="black").pack(pady=20)