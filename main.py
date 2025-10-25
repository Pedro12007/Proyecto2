import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

def validar_campo_lleno(entrada):
    return len(entrada.replace(' ', '')) > 0

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


class Admin:
    def __init__(self):
        global ventana_admin
        ventana_admin = tk.Toplevel(ventana_login)
        ventana_admin.title("Menú de administrador")
        ventana_admin.state("zoomed")
        ventana_admin.geometry('900x800')

        def cerrar_sesion():
            ventana_admin.destroy()
            ventana_login.deiconify()
            ventana_login.state("zoomed")

        def generar_usuario():
            self.nombre_usuario = self.nombres.get()
            self.apellido_usuario = self.apellidos.get()

            usuario_generado = ''

            if validar_campo_lleno(self.nombre_usuario) and validar_campo_lleno(self.apellido_usuario):
                lista_nombres = self.nombre_usuario.split()
                lista_apellidos = self.apellido_usuario.split()
                for i in lista_nombres:
                    usuario_generado += i[0].lower()
                if len(lista_apellidos) == 1:
                    usuario_generado += lista_apellidos[0].lower()
                else:
                    usuario_generado += lista_apellidos.pop(0).lower()
                    for i in lista_apellidos:
                        usuario_generado += i[0].lower()

                self.usuario.config(state='normal')
                self.usuario.delete(0, tk.END)
                self.usuario.insert(0, usuario_generado)
                self.usuario.config(state='readonly')



            else:
                messagebox.showerror('Error', 'El nombre y/o apellido están vacíos.')

        fondo = 'white'


        ventana_admin.protocol('WM_DELETE_WINDOW', cerrar_sesion)

        frame_principal = tk.Frame(ventana_admin, bg='white')
        frame_principal.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame_add_usuario = tk.Frame(ventana_admin, bg='white')
        frame_add_usuario.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame_mostrar_usuarios = tk.Frame(ventana_admin, bg='white')
        frame_mostrar_usuarios.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame_modificar_usuario = tk.Frame(ventana_admin, bg='white')
        frame_modificar_usuario.place(relx=0, rely=0, relwidth=1, relheight=1)


        # Contenido Frame principal
        tk.Label(frame_principal, text='Menú de administrador', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)
        tk.Button(frame_principal, text="Agregar usuario", font=("Arial", 16), bg="white", fg="black", command=lambda: frame_add_usuario.tkraise()).pack(pady=20)
        tk.Button(frame_principal, text="Modificar datos de usuario", font=("Arial", 16), bg="white", fg="black", command=lambda: frame_mostrar_usuarios.tkraise()).pack(pady=20)
        tk.Button(frame_principal, text="Cerrar sesión", font=("Arial", 16), bg="white", fg="black", command=cerrar_sesion).pack(pady=20)


        # Contenido Frame - agregar usuario
        tk.Button(frame_add_usuario, text='Regresar', font=('Arial', 16), bg="white", fg="black", command=lambda: frame_principal.tkraise()).pack(side='left', anchor='n', pady=20)
        tk.Label(frame_add_usuario, text='Agregar usuario', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)
        tk.Label(frame_add_usuario, text='Nombre:', font=("Arial", 14), bg=fondo).pack(anchor='center',pady=20)
        self.nombres = tk.Entry(frame_add_usuario, width=40, bd=1)
        self.nombres.pack(anchor='center', pady=10)

        tk.Label(frame_add_usuario, text='Apellido:', font=("Arial", 14), bg=fondo).pack(anchor='center',pady=20)
        self.apellidos = tk.Entry(frame_add_usuario, width=40, bd=1)
        self.apellidos.pack(anchor='center', pady=10)

        fila_usuario = tk.Frame(frame_add_usuario, width=100, bg=fondo)
        fila_usuario.pack(pady=20)
        tk.Label(fila_usuario, text='Usuario:', font=("Arial", 14), bg=fondo).pack(side='left', padx=10)
        tk.Button(fila_usuario, text='Generar usuario', font=('Arial', 12), bg="white", fg="black", command=generar_usuario).pack(side='right', padx=10)
        self.usuario = tk.Entry(frame_add_usuario, width=40, bd=1, state='readonly')
        self.usuario.pack(anchor='center', pady=10)

        tk.Label(frame_add_usuario, text='Contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center',pady=20)
        self.contrasena = tk.Entry(frame_add_usuario, width=40, bd=1)
        self.contrasena.pack(anchor='center', pady=10)

        tk.Label(frame_add_usuario, text='Confirmar contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center',pady=20)
        self.contrasena_conf = tk.Entry(frame_add_usuario, width=40, bd=1)
        self.contrasena_conf.pack(anchor='center', pady=10)

        tk.Button(frame_add_usuario, text='Guardar', font=('Arial', 16), bg="white", fg="black").pack(anchor='center', pady=10)

        # Contenido Frame - mostrar usuarios
        tk.Button(frame_mostrar_usuarios, text='Regresar', font=('Arial', 16), bg="white", fg="black", command=lambda: frame_principal.tkraise()).pack(side='left', anchor='n', pady=20)
        tk.Label(frame_mostrar_usuarios, text='Mostrar usuarios', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)
        tk.Button(frame_mostrar_usuarios, text='Seleccionar', font=('Arial', 16), bg="white", fg="black", command=lambda: frame_modificar_usuario.tkraise()).pack(side='right', pady=20)


        # Contenido Frame - modificar usuario
        tk.Button(frame_modificar_usuario, text='Regresar', font=('Arial', 16), bg="white", fg="black", command=lambda: frame_mostrar_usuarios.tkraise()).pack(side='left', anchor='n', pady=20)
        tk.Label(frame_modificar_usuario, text='Modificar usuario', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)

        tk.Label(frame_modificar_usuario, text=f'Usuario: pendiente', font=('Arial', 14), bg=fondo).pack(anchor='center',pady=20)

        tk.Label(frame_modificar_usuario, text='Nombre:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.nombres_m = tk.Entry(frame_modificar_usuario, width=40, bd=1)
        self.nombres_m.pack(anchor='center', pady=10)

        tk.Label(frame_modificar_usuario, text='Apellido:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.apellidos_m = tk.Entry(frame_modificar_usuario, width=40, bd=1)
        self.apellidos_m.pack(anchor='center', pady=10)

        tk.Label(frame_modificar_usuario, text='Contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.contrasena_m = tk.Entry(frame_modificar_usuario, width=40, bd=1)
        self.contrasena_m.pack(anchor='center', pady=10)

        tk.Label(frame_modificar_usuario, text='Confirmar contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.contrasena_conf_m = tk.Entry(frame_modificar_usuario, width=40, bd=1)
        self.contrasena_conf_m.pack(anchor='center', pady=10)

        tk.Button(frame_modificar_usuario, text='Guardar', font=('Arial', 16), bg="white", fg="black").pack(anchor='center', pady=10)

        frame_principal.tkraise()

class MenuPrincipal:
    def __init__(self):
        ventana_menu_principal = tk.Toplevel(ventana_login)
        ventana_menu_principal.title('Menu principal')
        ventana_menu_principal.state('zoomed')
        ventana_menu_principal.geometry('900x800')




        ventana_menu_principal.mainloop()



login = Login()