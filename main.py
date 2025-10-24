import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

class Login:
    def __init__(self):
        global ventana_login
        ventana_login = tk.Tk()
        ventana_login.title("Login")
        ventana_login.state("zoomed")
        ventana_login.geometry('900x800')

        fondo = 'white'

        self.left_frame = tk.Frame(ventana_login)
        self.left_frame.configure(bg=fondo)
        self.left_frame.pack(expand=True, fill="both", side='left')

        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self.left_frame, bg=fondo)
        content.grid(row=1, column=0)

        tk.Label(content, text="Usuario", font=("Arial", 20), fg="black", bg=fondo).pack(pady=10)
        self.usuario = tk.Entry(content, width=40, bd=1)
        self.usuario.pack(pady=10)

        tk.Label(content, text="Contraseña", font=("Arial", 20), fg="black", bg=fondo).pack(pady=10)
        self.contrasena = tk.Entry(content, width=40, show='*', bd=1)
        self.contrasena.pack(pady=10)

        def acceder():
            self.user = self.usuario.get()
            self.password = self.contrasena.get()


            if self.user and self.password:
                if self.user == 'admin':
                    if self.password == '1234':
                        admin = Admin()
                        ventana_login.withdraw()
                    else:
                        messagebox.showerror('Error', 'Contraseña incorrecta.')
                else:
                    pass
            else:
                messagebox.showerror("Error", "Ingrese su usuario y contraseña.")

        tk.Button(content, text="Iniciar sesión", font=("Arial", 16), bg="white", fg="black", command=acceder).pack(pady=20)

        self.right_frame = tk.Frame(ventana_login, bg= 'black')
        self.right_frame.pack(expand=True, fill="both", side='right')

        self.imagen_original = Image.open("21design2.png")
        self.label_img = tk.Label(self.right_frame, bg="black")
        self.label_img.place(relx=0.5, rely=0.5, anchor="center")

        self.right_frame.bind("<Configure>", self._ajustar_imagen)

        ventana_login.mainloop()

    def _ajustar_imagen(self, event):
        if event.width <= 1 or event.height <= 1:
            return

        img_w, img_h = self.imagen_original.size
        frame_w, frame_h = event.width, event.height

        prop_img = img_w / img_h
        prop_frame = frame_w / frame_h

        if prop_frame > prop_img:
            new_h = frame_h
            new_w = int(new_h * prop_img)
        else:
            new_w = frame_w
            new_h = int(new_w / prop_img)

        img_resized = self.imagen_original.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(img_resized)

        self.label_img.config(image=self.img_tk)
        self.label_img.image = self.img_tk

    def mostrar_ventana(self):
        ventana_login.deiconify()


class Admin:
    def __init__(self):
        global ventana_admin
        ventana_admin = tk.Tk()
        ventana_admin.title("Menú de administrador")
        ventana_admin.state("zoomed")
        ventana_admin.geometry('900x800')

        def cerrar_sesion():
            ventana_admin.destroy()

        tk.Label(ventana_admin, text='Menú de administrador', font=("Arial", 16, 'bold')).pack(pady=20)

        tk.Button(ventana_admin, text="Agregar usuario", font=("Arial", 16), bg="white", fg="black").pack(pady=20)
        tk.Button(ventana_admin, text="Modificar datos de usuario", font=("Arial", 16), bg="white", fg="black").pack(pady=20)
        tk.Button(ventana_admin, text="Cerrar sesión", font=("Arial", 16), bg="white", fg="black", command=cerrar_sesion).pack(pady=20)

login = Login()