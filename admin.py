import tkinter as tk
import login
import sqlite3

class Admin:
    def __init__(self):
        global ventana_admin
        ventana_admin = tk.Tk()
        ventana_admin.title("Menú de administrador")
        ventana_admin.state("zoomed")
        ventana_admin.geometry('900x800')

        def cerrar_sesion():
            ventana_admin.destroy()
            #login.Login.ventana_login.deiconify()


        tk.Label(ventana_admin, text='Menú de administrador', font=("Arial", 16, 'bold')).pack(pady=20)

        tk.Button(ventana_admin, text="Agregar usuario", font=("Arial", 16), bg="white", fg="black").pack(pady=20)
        tk.Button(ventana_admin, text="Modificar datos de usuario", font=("Arial", 16), bg="white", fg="black").pack(pady=20)
        tk.Button(ventana_admin, text="Cerrar sesión", font=("Arial", 16), bg="white", fg="black", command=cerrar_sesion).pack(pady=20)
