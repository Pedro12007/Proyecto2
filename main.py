import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from manejo_db import *

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
            pass

        ventana_admin.protocol('WM_DELETE_WINDOW', cerrar_sesion)

        frame_principal = tk.Frame(ventana_admin, bg='white')
        frame_principal.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame_add_usuario = tk.Frame(ventana_admin, bg='white')
        frame_add_usuario.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame_modificar_usuario = tk.Frame(ventana_admin, bg='white')
        frame_modificar_usuario.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Contenido Frame principal
        tk.Label(frame_principal, text='Menú de administrador', font=("Arial", 16, 'bold')).pack(pady=20)
        tk.Button(frame_principal, text="Agregar usuario", font=("Arial", 16), bg="white", fg="black", command=lambda: frame_add_usuario.tkraise()).pack(pady=20)
        tk.Button(frame_principal, text="Modificar datos de usuario", font=("Arial", 16), bg="white", fg="black", command=lambda: frame_modificar_usuario.tkraise()).pack(pady=20)
        tk.Button(frame_principal, text="Cerrar sesión", font=("Arial", 16), bg="white", fg="black", command=cerrar_sesion).pack(pady=20)

        # Contenido Frame - agregar usuario
        tk.Button(frame_add_usuario, text='Regresar', font=('Arial', 16), bg="white", fg="black", command=lambda: frame_principal.tkraise()).pack(side='left', anchor='n', pady=20)
        tk.Label(frame_add_usuario, text='Agregar usuario', font=("Arial", 16, 'bold')).pack(pady=20)
        tk.Label(frame_add_usuario, text='Nombre:', font=("Arial", 14), ).pack(anchor='center',pady=20)
        self.nombres = tk.Entry(frame_add_usuario, width=40, bd=1)
        self.nombres.pack(anchor='center', pady=10)

        tk.Label(frame_add_usuario, text='Apellido:', font=("Arial", 14)).pack(anchor='center',pady=20)
        self.apellidos = tk.Entry(frame_add_usuario, width=40, bd=1)
        self.apellidos.pack(anchor='center', pady=10)

        fila_usuario = tk.Frame(frame_add_usuario, width=100)
        fila_usuario.pack(pady=20)
        tk.Label(fila_usuario, text='Usuario:', font=("Arial", 14)).pack(side='left', padx=10)
        tk.Button(fila_usuario, text='Generar usuario', font=('Arial', 16), bg="white", fg="black", command=generar_usuario).pack(side='right', padx=10)
        self.usuario = tk.Entry(frame_add_usuario, width=40, bd=1, state='readonly')
        self.usuario.pack(anchor='center', pady=10)

        tk.Label(frame_add_usuario, text='Contraseña:', font=("Arial", 14)).pack(anchor='center',pady=20)
        self.contrasena = tk.Entry(frame_add_usuario, width=40, bd=1)
        self.contrasena.pack(anchor='center', pady=10)

        tk.Label(frame_add_usuario, text='Confirmar contraseña:', font=("Arial", 14)).pack(anchor='center',pady=20)
        self.contrasena_conf = tk.Entry(frame_add_usuario, width=40, bd=1)
        self.contrasena_conf.pack(anchor='center', pady=10)

        tk.Button(frame_add_usuario, text='Guardar', font=('Arial', 16), bg="white", fg="black").pack(anchor='center', pady=10)

        # Contenido Frame - modificar usuario
        tk.Button(frame_modificar_usuario, text='Regresar', font=('Arial', 16), bg="white", fg="black", command=lambda: frame_principal.tkraise()).pack(side='left', anchor='n', pady=20)



        frame_principal.tkraise()

class Materiales:
    def __init__(self):
        self.root = Tk()
        self.root.title("21° Design")
        self.root.configure(background='lightblue')
        self.root.geometry("650x400")

        self.miID = StringVar()
        self.miDescripcion = StringVar()
        self.miUnidad = StringVar()
        self.miPrec_unitario = StringVar()

        self.imagen_buscar = PhotoImage(file="imagenes/buscar.png")
        self.imagen_crear = PhotoImage(file="imagenes/crear.png")
        self.imagen_mostrar = PhotoImage(file="imagenes/mostrar.png")
        self.imagen_actualizar = PhotoImage(file="imagenes/actualizar.png")
        self.imagen_eliminar = PhotoImage(file="imagenes/eliminar.png")

        self.cabecera = ["ID", "Descripción", "Unidad", "Precio Unitario"]

        self.tree = ttk.Treeview(self.root, height=10, columns=("#1", "#2", "#3"))
        self.tree.place(x=0, y=150)

        self.tree.column("#0", width=100)
        self.tree.heading("#0", text=self.cabecera[0], anchor=CENTER)
        self.tree.column("#1", width=250)
        self.tree.heading("#1", text=self.cabecera[1], anchor=CENTER)
        self.tree.column("#2", width=150)
        self.tree.heading("#2", text=self.cabecera[2], anchor=CENTER)
        self.tree.column("#3", width=120)
        self.tree.heading("#3", text=self.cabecera[3], anchor=CENTER)
        self.tree.bind("<Button-1>", self.seleccionarUsandoClick)

        self.menubar = Menu(self.root)

        self.menubasedat = Menu(self.menubar, tearoff=0)
        self.menubasedat.add_command(label="Crear/Conectar Base de Datos", command=self.conexionBBDD)
        self.menubasedat.add_command(label="Eliminar Base de Datos", command=self.eliminarBBDD)
        self.menubasedat.add_command(label="Salir", command=self.salirAplicacion)
        self.menubar.add_cascade(label="Inicio", menu=self.menubasedat)

        self.ayudamenu = Menu(self.menubar, tearoff=0)
        self.ayudamenu.add_command(label="Resetear Campos", command=self.limpiarCampos)
        self.ayudamenu.add_command(label="Acerca", command=Gestor.mensaje)
        self.menubar.add_cascade(label="Ayuda", menu=self.ayudamenu)

        self.root.config(menu=self.menubar)

        Label(self.root, text="ID", background='lightblue').place(x=50, y=10)
        self.e1 = Entry(self.root, textvariable=self.miID, state="readonly")
        self.e1.place(x=120, y=10)

        Label(self.root, text="Descripción", background='lightblue').place(x=50, y=40)
        self.e2 = Entry(self.root, textvariable=self.miDescripcion, width=50)
        self.e2.place(x=150, y=40)

        Label(self.root, text="Unidad", background='lightblue').place(x=50, y=70)
        self.e3 = Entry(self.root, textvariable=self.miUnidad)
        self.e3.place(x=150, y=70)

        Label(self.root, text="Precio Unitario", background='lightblue').place(x=300, y=70)
        self.e4 = Entry(self.root, textvariable=self.miPrec_unitario, width=10)
        self.e4.place(x=420, y=70)

        Label(self.root, text="Q.", background='lightblue').place(x=490, y=70)

        Button(self.root, text="", image=self.imagen_buscar, bg="orange", compound="left", command=self.buscar).place(x=520, y=10)
        Button(self.root, text="", image=self.imagen_crear, bg="green", compound="left", command=self.crear).place(x=50, y=110)
        Button(self.root, text="", image=self.imagen_actualizar, bg="orange", compound="left", command=self.actualizar).place(x=180, y=110)
        Button(self.root, text="", image=self.imagen_mostrar, bg="orange", compound="left", command=self.mostrar).place(x=320, y=110)
        Button(self.root, text="", image=self.imagen_eliminar, bg="red", compound="left", command=self.borrar).place(x=460, y=110)

        self.mostrar()
        self.root.mainloop()

    def conexionBBDD(self):
        Gestor.conexionBBDD()

    def eliminarBBDD(self):
        Gestor.eliminarBBDD()
        self.limpiarMostrar()

    def limpiarMostrar(self):
        self.limpiarCampos()
        self.mostrar()

    def limpiarCampos(self):
        self.e1.config(state="normal")
        self.miID.set("")
        self.e1.config(state="readonly")
        self.miDescripcion.set("")
        self.miUnidad.set("")
        self.miPrec_unitario.set("")

    def mostrar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        Gestor.mostrar(self.tree)

    def salirAplicacion(self):
        valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir del programa?")
        if valor == "yes":
            self.root.destroy()

    def crear(self):
        Gestor.crear(
            self.miDescripcion.get(),
            self.miUnidad.get(),
            self.miPrec_unitario.get()
        )
        self.limpiarMostrar()

    def actualizar(self):
        Gestor.actualizar(
            self.miDescripcion.get(),
            self.miUnidad.get(),
            self.miPrec_unitario.get(),
            self.miID.get()
        )
        self.limpiarMostrar()

    def borrar(self):
        if not self.miID.get():
            messagebox.showerror("Error", "Seleccione un material primero.")
            return

        confirmar = messagebox.askyesno("Confirmar eliminación",f"¿Seguro que desea eliminar el material con ID {self.miID.get()}?")

        if not confirmar:
            return

        Gestor.borrar(self.miID.get())
        self.limpiarMostrar()

    def buscar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        Gestor.buscar(self.tree, self.miDescripcion.get())

    def seleccionarUsandoClick(self, event):
        item_id = self.tree.identify('item', event.x, event.y)
        if not item_id:
            return
        datos_item = self.tree.item(item_id, "values")
        id_texto = self.tree.item(item_id, "text")
        self.e1.config(state="normal")
        self.miID.set(id_texto)
        self.e1.config(state="readonly")
        if len(datos_item) >= 1:
            self.miDescripcion.set(datos_item[0])
        if len(datos_item) >= 2:
            self.miUnidad.set(datos_item[1])
        if len(datos_item) >= 3:
            self.miPrec_unitario.set(datos_item[2])

if __name__ == "__main__":
    app = Materiales()
login = Login()