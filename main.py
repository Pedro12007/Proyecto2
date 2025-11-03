from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from manejo_db import *
import os
from datetime import datetime

def seleccionar_haciendo_click(tree, event, id_var, campos_vars, readonly_widget=None):
    item_id = tree.identify('item', event.x, event.y)
    if not item_id:
        return None

    datos_item = tree.item(item_id, "values")
    id_texto = tree.item(item_id, "text")

    if readonly_widget:
        readonly_widget.config(state="normal")
    id_var.set(id_texto)
    if readonly_widget:
        readonly_widget.config(state="readonly")

    for i, variable in enumerate(campos_vars):
        if i < len(datos_item):
            variable.set(datos_item[i])

    return id_texto

class VistaLogin:
    def __init__(self):
        global ventana_login

        self.ventana_login = Tk()
        ventana_login = self.ventana_login

        self.ventana_login.title("Login")
        self.ventana_login.state("zoomed")
        self.ventana_login.geometry('900x800')

        fondo = 'white'

        self.left_frame = Frame(self.ventana_login)
        self.left_frame.configure(bg=fondo)
        self.left_frame.pack(expand=True, fill="both", side='left')

        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        content = Frame(self.left_frame, bg=fondo)
        content.grid(row=1, column=0)

        Label(content, text="Usuario", font=("Arial", 20), fg="black", bg=fondo).pack(pady=10)
        self.usuario_entry = Entry(content, width=40, bd=1)
        self.usuario_entry.pack(pady=10)

        Label(content, text="Contraseña", font=("Arial", 20), fg="black", bg=fondo).pack(pady=10)
        self.contrasena_entry = Entry(content, width=40, show='*', bd=1)
        self.contrasena_entry.pack(pady=10)

        self.login_button = Button(content, text="Iniciar sesión", font=("Arial", 16), bg="white", fg="black")
        self.login_button.pack(pady=20)

        self.right_frame = Frame(self.ventana_login, bg='black')
        self.right_frame.pack(expand=True, fill="both", side='right')

        self.imagen_original = Image.open("21design2.png")
        self.label_img = Label(self.right_frame, bg="black")
        self.label_img.place(relx=0.5, rely=0.5, anchor="center")

        self.right_frame.bind("<Configure>", self._ajustar_imagen)

    def set_login_command(self, command):
        #Metodo para que el controlador asigne la función al botón.
        self.login_button.config(command=command)

    def get_usuario(self):
        #Devuelve el texto del campo usuario.
        return self.usuario_entry.get()

    def get_contrasena(self):
        #Devuelve el texto del campo contraseña.
        return self.contrasena_entry.get()

    def mostrar_error(self, titulo, mensaje):
        #Muestra un mensaje de error.
        messagebox.showerror(titulo, mensaje)

    def ocultar_ventana(self):
        #Oculta la ventana de login.
        self.ventana_login.withdraw()

    def iniciar_mainloop(self):
        #Inicia el bucle principal de la aplicación.
        self.ventana_login.mainloop()

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

class ControladorLogin:
    def __init__(self, view):
        self.view = view

    def acceder(self):
        user = self.view.get_usuario()
        password = self.view.get_contrasena()

        if user and password:
            if user == 'admin':
                if password == '1234':
                    self.view.ocultar_ventana()
                    Admin()
                else:
                    self.view.mostrar_error('Error', 'Contraseña incorrecta.')
            else:
                usuario_encontrado = ServicioUsuarios.buscar_usuario_password(user, password)

                if usuario_encontrado:
                    self.view.ocultar_ventana()
                    MenuPrincipal(usuario_encontrado[0])
                else:
                    self.view.mostrar_error('Error', 'Usuario o contraseña incorrectos.')
        else:
            self.view.mostrar_error("Error", "Ingrese su usuario y contraseña.")

    @staticmethod
    def iniciar_app():
        vista_app = VistaLogin()
        controlador_app = ControladorLogin(vista_app)
        vista_app.set_login_command(controlador_app.acceder)

        return vista_app


class VistaAdmin:
    def __init__(self, ventana_login):
        global ventana_admin
        ventana_admin = Toplevel(ventana_login)
        self.ventana_admin = ventana_admin
        ventana_admin.title("Menú de administrador")
        ventana_admin.state("zoomed")
        ventana_admin.geometry('900x800')

        fondo = 'white'

        self.miID_usuario = StringVar()
        self.miNombres = StringVar()
        self.miApellidos = StringVar()
        self.miUsuario = StringVar()

        # Frames
        self.frame_principal = Frame(ventana_admin, bg='white')
        self.frame_principal.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_add_usuario = Frame(ventana_admin, bg='white')
        self.frame_add_usuario.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_mostrar_usuarios = Frame(ventana_admin, bg='white')
        self.frame_mostrar_usuarios.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_modificar_usuario = Frame(ventana_admin, bg='white')
        self.frame_modificar_usuario.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.crear_frame_principal(fondo)
        self.crear_frame_agregar(fondo)
        self.crear_frame_mostrar(fondo)
        self.crear_frame_modificar(fondo)

        self.frame_principal.tkraise()

    def crear_frame_principal(self, fondo):
        Label(self.frame_principal, text='Menú de administrador', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)
        self.btn_agregar = Button(self.frame_principal, text="Agregar usuario", font=("Arial", 16), bg="white", fg="black")
        self.btn_agregar.pack(pady=20)
        self.btn_modificar = Button(self.frame_principal, text="Modificar datos de usuario", font=("Arial", 16), bg="white", fg="black")
        self.btn_modificar.pack(pady=20)
        self.btn_cerrar = Button(self.frame_principal, text="Cerrar sesión", font=("Arial", 16), bg="white", fg="black")
        self.btn_cerrar.pack(pady=20)

    def crear_frame_agregar(self, fondo):
        self.btn_regresar_agregar = Button(self.frame_add_usuario, text='Regresar', font=('Arial', 16), bg="white", fg="black")
        self.btn_regresar_agregar.pack(side='left', anchor='n', pady=20)

        Label(self.frame_add_usuario, text='Agregar usuario', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)
        Label(self.frame_add_usuario, text='Nombre:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.nombres = Entry(self.frame_add_usuario, width=40, bd=1)
        self.nombres.pack(anchor='center', pady=10)

        Label(self.frame_add_usuario, text='Apellido:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.apellidos = Entry(self.frame_add_usuario, width=40, bd=1)
        self.apellidos.pack(anchor='center', pady=10)

        fila_usuario = Frame(self.frame_add_usuario, width=100, bg=fondo)
        fila_usuario.pack(pady=20)
        Label(fila_usuario, text='Usuario:', font=("Arial", 14), bg=fondo).pack(side='left', padx=10)
        self.btn_generar_usuario = Button(fila_usuario, text='Generar usuario', font=('Arial', 12), bg="white", fg="black")
        self.btn_generar_usuario.pack(side='right', padx=10)

        self.usuario = Entry(self.frame_add_usuario, width=40, bd=1, state='readonly')
        self.usuario.pack(anchor='center', pady=10)

        Label(self.frame_add_usuario, text='Contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.contrasena = Entry(self.frame_add_usuario, width=40, bd=1)
        self.contrasena.pack(anchor='center', pady=10)

        Label(self.frame_add_usuario, text='Confirmar contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.contrasena_conf = Entry(self.frame_add_usuario, width=40, bd=1)
        self.contrasena_conf.pack(anchor='center', pady=10)

        self.btn_guardar = Button(self.frame_add_usuario, text='Guardar', font=('Arial', 16), bg="white", fg="black")
        self.btn_guardar.pack(anchor='center', pady=10)

    def crear_frame_mostrar(self, fondo):
        self.btn_regresar_mostrar = Button(self.frame_mostrar_usuarios, text='Regresar', font=('Arial', 16), bg="white", fg="black")
        self.btn_regresar_mostrar.pack(side='left', anchor='n', pady=20)

        Label(self.frame_mostrar_usuarios, text='Mostrar usuarios', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)

        self.cabecera = ["ID", "Nombres", "Apellidos", "Usuario"]
        self.tree = ttk.Treeview(self.frame_mostrar_usuarios, height=10, columns=("#1", "#2", "#3"))
        self.tree.place(x=0, y=150)

        self.tree.column("#0", width=100)
        self.tree.heading("#0", text=self.cabecera[0], anchor=CENTER)
        self.tree.column("#1", width=250)
        self.tree.heading("#1", text=self.cabecera[1], anchor=CENTER)
        self.tree.column("#2", width=150)
        self.tree.heading("#2", text=self.cabecera[2], anchor=CENTER)
        self.tree.column("#3", width=120)
        self.tree.heading("#3", text=self.cabecera[3], anchor=CENTER)

        self.btn_eliminar = Button(self.frame_mostrar_usuarios, text='Eliminar', font=('Arial', 16), bg="white",
                                   fg="black")
        self.btn_eliminar.pack(side='left', pady=20)

        self.btn_modificar_sel = Button(self.frame_mostrar_usuarios, text='Modificar', font=('Arial', 16), bg="white",
                                        fg="black")
        self.btn_modificar_sel.pack(side='right', pady=20)

    def crear_frame_modificar(self, fondo):
        self.btn_regresar_modificar = Button(self.frame_modificar_usuario, text='Regresar', font=('Arial', 16),
                                             bg="white", fg="black")
        self.btn_regresar_modificar.pack(side='left', anchor='n', pady=20)

        Label(self.frame_modificar_usuario, text='Modificar usuario', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)

        Label(self.frame_modificar_usuario, textvariable=self.miUsuario, font=('Arial', 14), bg=fondo).pack(anchor='center', pady=20)

        Label(self.frame_modificar_usuario, text='Nombre:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.nombres_m = Entry(self.frame_modificar_usuario, width=40, bd=1)
        self.nombres_m.pack(anchor='center', pady=10)

        Label(self.frame_modificar_usuario, text='Apellido:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.apellidos_m = Entry(self.frame_modificar_usuario, width=40, bd=1)
        self.apellidos_m.pack(anchor='center', pady=10)

        Label(self.frame_modificar_usuario, text='Contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.contrasena_m = Entry(self.frame_modificar_usuario, width=40, bd=1)
        self.contrasena_m.pack(anchor='center', pady=10)

        Label(self.frame_modificar_usuario, text='Confirmar contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.contrasena_conf_m = Entry(self.frame_modificar_usuario, width=40, bd=1)
        self.contrasena_conf_m.pack(anchor='center', pady=10)

        self.btn_guardar_modificar = Button(self.frame_modificar_usuario, text='Guardar', font=('Arial', 16), bg="white", fg="black")
        self.btn_guardar_modificar.pack(anchor='center', pady=10)

    def set_commands(self, commands):
        #Asigna los comandos del controlador a los botones
        self.ventana_admin.protocol('WM_DELETE_WINDOW', commands['cerrar_ventana'])
        self.btn_agregar.config(command=lambda: self.frame_add_usuario.tkraise())
        self.btn_modificar.config(command=commands['mostrar_usuarios'])
        self.btn_cerrar.config(command=commands['cerrar_sesion'])
        self.btn_regresar_agregar.config(command=lambda: self.frame_principal.tkraise())
        self.btn_generar_usuario.config(command=commands['generar_usuario'])
        self.btn_guardar.config(command=commands['guardar_usuario'])
        self.btn_regresar_mostrar.config(command=lambda: self.frame_principal.tkraise())
        self.btn_eliminar.config(command=commands['eliminar_usuario'])
        self.btn_modificar_sel.config(command=commands['seleccionar_usuario'])
        self.btn_regresar_modificar.config(command=lambda: self.frame_mostrar_usuarios.tkraise())
        self.btn_guardar_modificar.config(command=commands['modificar_usuario'])
        self.tree.bind("<Button-1>", commands['seleccionar_click'])

    def get_datos_agregar(self):
        #Obtiene los datos del formulario de agregar
        return {
            'nombre': self.nombres.get(),
            'apellido': self.apellidos.get(),
            'usuario': self.usuario.get(),
            'contrasena': self.contrasena.get(),
            'contrasena_conf': self.contrasena_conf.get()
        }

    def get_datos_modificar(self):
        #Obtiene los datos del formulario de modificar
        return {
            'id': self.miID_usuario.get(),
            'nombre': self.nombres_m.get(),
            'apellido': self.apellidos_m.get(),
            'usuario': self.miUsuario.get().replace('Usuario: ', ''),
            'contrasena': self.contrasena_m.get(),
            'contrasena_conf': self.contrasena_conf_m.get()
        }

    def set_usuario_generado(self, usuario):
        #Establece el usuario generado
        self.usuario.config(state='normal')
        self.usuario.delete(0, END)
        self.usuario.insert(0, usuario)
        self.usuario.config(state='readonly')

    def cargar_datos_modificar(self, datos):
        #Carga los datos del usuario seleccionado
        self.nombres_m.delete(0, END)
        self.nombres_m.insert(0, datos[1])
        self.apellidos_m.delete(0, END)
        self.apellidos_m.insert(0, datos[2])
        self.miUsuario.set(f'Usuario: {datos[3]}')
        self.contrasena_m.delete(0, END)
        self.contrasena_m.insert(0, datos[4])
        self.contrasena_conf_m.delete(0, END)
        self.contrasena_conf_m.insert(0, datos[4])

    def limpiar_seleccion(self):
        self.miID_usuario.set('')
        self.miNombres.set('')
        self.miApellidos.set('')
        self.miUsuario.set('')

    def mostrar_frame_modificar(self):
        self.frame_modificar_usuario.tkraise()

    def mostrar_frame_mostrar(self):
        #Muestra el frame de mostrar usuarios
        self.frame_mostrar_usuarios.tkraise()


class ControladorAdmin:
    def __init__(self, view):
        self.view = view
        self.configurar_comandos()

    def configurar_comandos(self):
        #Configura los comandos de la vista
        commands = {
            'cerrar_ventana': self.cerrar_sesion,
            'mostrar_usuarios': self.mostrar_usuarios,
            'cerrar_sesion': self.cerrar_sesion,
            'generar_usuario': self.generar_usuario,
            'guardar_usuario': self.guardar_usuario,
            'eliminar_usuario': self.eliminar_usuario,
            'seleccionar_usuario': self.seleccionar_usuario,
            'modificar_usuario': self.modificar_usuario,
            'seleccionar_click': self.seleccionarUsandoClick
        }
        self.view.set_commands(commands)

    def cerrar_sesion(self):
        ventana_admin.destroy()
        ventana_login.deiconify()
        ventana_login.state("zoomed")

    def generar_usuario(self):
        datos = self.view.get_datos_agregar()
        nombre_usuario = datos['nombre']
        apellido_usuario = datos['apellido']

        usuario_generado = ''

        if validar_campo_lleno(nombre_usuario) and validar_campo_lleno(apellido_usuario):
            lista_nombres = nombre_usuario.split()
            lista_apellidos = apellido_usuario.split()
            for i in lista_nombres:
                usuario_generado += i[0].lower()
            if len(lista_apellidos) == 1:
                usuario_generado += lista_apellidos[0].lower()
            else:
                usuario_generado += lista_apellidos.pop(0).lower()
                for i in lista_apellidos:
                    usuario_generado += i[0].lower()

            self.view.set_usuario_generado(usuario_generado)
        else:
            messagebox.showerror('Error', 'El nombre y/o apellido están vacíos.')

    def guardar_usuario(self):
        datos = self.view.get_datos_agregar()

        if validar_campo_lleno(datos['nombre']) and validar_campo_lleno(datos['apellido']) and \
                validar_campo_lleno(datos['usuario']) and validar_campo_lleno(datos['contrasena']) and \
                validar_campo_lleno(datos['contrasena_conf']):
            if datos['contrasena'] == datos['contrasena_conf']:
                ServicioUsuarios.crear(datos['nombre'], datos['apellido'], datos['usuario'], datos['contrasena'])
                messagebox.showinfo('Usuario creado', 'Usuario creado satisfactoriamente.')
            else:
                messagebox.showerror('Error', 'La contraseña debe coincidir.')
        else:
            messagebox.showerror('Error', 'Todos los campos deben estar llenos.')

    def mostrar_usuarios(self):
        GestorUsuarios.mostrar(self.view.tree)
        self.view.mostrar_frame_mostrar()

    def seleccionar_usuario(self):
        if not self.view.miID_usuario.get():
            messagebox.showerror('Error', 'Seleccione un usuario primero.')
            return

        datos = ServicioUsuarios.buscar_id(self.view.miID_usuario.get())
        if datos:
            self.view.cargar_datos_modificar(datos)
            self.view.mostrar_frame_modificar()
        else:
            messagebox.showerror('Error', 'Usuario no encontrado.')

    def modificar_usuario(self):
        datos = self.view.get_datos_modificar()

        if validar_campo_lleno(datos['nombre']) and validar_campo_lleno(datos['apellido']) and \
                validar_campo_lleno(datos['contrasena']) and validar_campo_lleno(datos['contrasena_conf']):
            if datos['contrasena'] == datos['contrasena_conf']:
                ServicioUsuarios.actualizar(datos['nombre'], datos['apellido'], datos['usuario'],
                                            datos['contrasena'], datos['id'])
                messagebox.showinfo('Usuario actualizado', 'Usuario actualizado satisfactoriamente.')
                GestorUsuarios.mostrar(self.view.tree)
                self.view.mostrar_frame_mostrar()
            else:
                messagebox.showerror('Error', 'La contraseña debe coincidir.')
        else:
            messagebox.showerror('Error', 'Todos los campos deben estar llenos.')

    def eliminar_usuario(self):
        if not self.view.miID_usuario.get():
            messagebox.showerror('Error', 'Seleccione un usuario primero.')
            return

        confirmar = messagebox.askyesno('Confirmar',
                                        f'¿Está seguro de eliminar el usuario con ID {self.view.miID_usuario.get()}?')

        if confirmar:
            try:
                ServicioUsuarios.borrar(self.view.miID_usuario.get())
                messagebox.showinfo('Éxito', 'Usuario eliminado correctamente.')
                GestorUsuarios.mostrar(self.view.tree)
                self.view.limpiar_seleccion()
            except Exception as e:
                messagebox.showerror('Error', f'Error al eliminar usuario: {e}')

    def seleccionarUsandoClick(self, event):
        seleccionar_haciendo_click(
            tree=self.view.tree,
            event=event,
            id_var=self.view.miID_usuario,
            campos_vars=[self.view.miNombres, self.view.miApellidos, self.view.miUsuario]
        )

class Admin:
    def __init__(self):
        vista = VistaAdmin(ventana_login)
        controlador = ControladorAdmin(vista)

class Materiales:
    def __init__(self):
        global ventana_materiales
        ventana_materiales = Toplevel(ventana_login)
        ventana_materiales.title("21° Design")
        ventana_materiales.configure(background='white')
        ventana_materiales.geometry("650x400")

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

        self.tree = ttk.Treeview(ventana_materiales, height=10, columns=("#1", "#2", "#3"))
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

        self.menubar = Menu(ventana_materiales)

        self.menubasedat = Menu(self.menubar, tearoff=0)
        self.menubasedat.add_command(label="Crear/Conectar Base de Datos", command=self.conexionBBDD)
        self.menubasedat.add_command(label="Salir", command=self.salirAplicacion)
        self.menubar.add_cascade(label="Inicio", menu=self.menubasedat)

        self.ayudamenu = Menu(self.menubar, tearoff=0)
        self.ayudamenu.add_command(label="Resetear Campos", command=self.limpiarCampos)
        self.ayudamenu.add_command(label="Acerca", command=GestorMateriales.mensaje)
        self.menubar.add_cascade(label="Ayuda", menu=self.ayudamenu)

        ventana_materiales.config(menu=self.menubar)

        Label(ventana_materiales, text="ID", background='lightblue').place(x=50, y=10)
        self.e1 = Entry(ventana_materiales, textvariable=self.miID, state="readonly")
        self.e1.place(x=120, y=10)

        Label(ventana_materiales, text="Descripción", background='lightblue').place(x=50, y=40)
        self.e2 = Entry(ventana_materiales, textvariable=self.miDescripcion, width=50)
        self.e2.place(x=150, y=40)

        Label(ventana_materiales, text="Unidad", background='lightblue').place(x=50, y=70)
        self.e3 = Entry(ventana_materiales, textvariable=self.miUnidad)
        self.e3.place(x=150, y=70)

        Label(ventana_materiales, text="Precio Unitario", background='lightblue').place(x=300, y=70)
        self.e4 = Entry(ventana_materiales, textvariable=self.miPrec_unitario, width=10)
        self.e4.place(x=420, y=70)

        Label(ventana_materiales, text="Q.", background='lightblue').place(x=490, y=70)

        Button(ventana_materiales, text="", image=self.imagen_buscar, bg="black", compound="left", command=self.buscar).place(x=520, y=10)
        Button(ventana_materiales, text="", image=self.imagen_crear, bg="black", compound="left", command=self.crear).place(x=50, y=110)
        Button(ventana_materiales, text="", image=self.imagen_actualizar, bg="black", compound="left", command=self.actualizar).place(x=180, y=110)
        Button(ventana_materiales, text="", image=self.imagen_mostrar, bg="black", compound="left", command=self.mostrar).place(x=320, y=110)
        Button(ventana_materiales, text="", image=self.imagen_eliminar, bg="red", compound="left", command=self.borrar).place(x=460, y=110)

        self.mostrar()
        ventana_materiales.mainloop()

    def conexionBBDD(self):
        GestorMateriales.conexionBBDD()

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
        GestorMateriales.mostrar(self.tree)

    def salirAplicacion(self):
        valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir del programa?")
        if valor == "yes":
            ventana_materiales.destroy()

    def crear(self):
        GestorMateriales.crear(
            self.miDescripcion.get(),
            self.miUnidad.get(),
            self.miPrec_unitario.get()
        )
        self.limpiarMostrar()

    def actualizar(self):
        GestorMateriales.actualizar(
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

        GestorMateriales.borrar(self.miID.get())
        self.limpiarMostrar()

    def buscar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        GestorMateriales.buscar(self.tree, self.miDescripcion.get())

    def seleccionarUsandoClick(self, event):
        seleccionar_haciendo_click(
            tree=self.tree,
            event=event,
            id_var=self.miID,
            campos_vars=[self.miDescripcion, self.miUnidad, self.miPrec_unitario],
            readonly_widget=self.e1
        )


class MenuPrincipal:
    def __init__(self, id_usuario):
        global ventana_menu_principal
        ventana_menu_principal = Toplevel(ventana_login)
        ventana_menu_principal.title("21° Design")
        ventana_menu_principal.configure(background='black')
        ventana_menu_principal.geometry("400x600")
        ventana_menu_principal.state("zoomed")

        self.ventana = ventana_menu_principal
        self.id_usuario = id_usuario
        self.menu_bar_colour = 'white'

        # Vincular el cierre de ventana
        ventana_menu_principal.protocol('WM_DELETE_WINDOW', self.cerrar_sesion)

        self.inicializar_variables()
        self.cargar_iconos()
        self.crear_frames()
        self.configurar_menu_lateral()
        self.proyectos_page()

    def inicializar_variables(self):
        # Inicializa todas las variables StringVar para los proyectos
        self.id_proyecto = StringVar()
        self.nombre = StringVar()
        self.descripcion = StringVar()
        self.n_usuarios = StringVar()
        self.fecha_inicio = StringVar()
        self.duracion = StringVar()
        self.fecha_final = StringVar()
        self.estado = StringVar()
        self.presupuesto_total = StringVar()
        self.id_cliente = StringVar()

        # Variables para agregar proyecto
        self.nombre_var = StringVar()
        self.descripcion_var = StringVar()
        self.no_usuarios_var = StringVar()
        self.fecha_inicio_var = StringVar()
        self.fecha_fin_var = StringVar()

        # Variables para Administración
        self.total_costo_administracion = StringVar()

        #Variables para DetallesManoObra
        self.total_costo_mano_obra = StringVar()

        # Variables para DetallesMateriales
        self.id_material = StringVar()
        self.descripcion_material = StringVar()
        self.unidad_material = StringVar()
        self.costo_unitario = StringVar()
        self.cantidad_material = StringVar()
        self.costo_total = StringVar()
        self.total_costo_materiales = StringVar()

        self.cliente_nombre_var = StringVar()
        self.cliente_apellido_var = StringVar()
        self.cliente_telefono_var = StringVar()
        self.cliente_mail_var = StringVar()
        self.cliente_datos_ref_var = StringVar()
        self.cliente_direccion_var = StringVar()

    def cargar_iconos(self):
        ruta_icono_tresb = os.path.join(os.path.dirname(__file__), 'imagenes', 'tresb.png')
        ruta_icono_mas = os.path.join(os.path.dirname(__file__), 'imagenes', 'mas.png')
        ruta_icono_block = os.path.join(os.path.dirname(__file__), 'imagenes', 'block.png')
        ruta_icono_home = os.path.join(os.path.dirname(__file__), 'imagenes', 'home.png')
        ruta_icono_salir = os.path.join(os.path.dirname(__file__), 'imagenes', 'salir.png')
        ruta_icono_x = os.path.join(os.path.dirname(__file__), 'imagenes', 'x.png')

        self.toggle_icon = PhotoImage(file=ruta_icono_tresb)
        self.mas_icon = PhotoImage(file=ruta_icono_mas)
        self.block_icon = PhotoImage(file=ruta_icono_block)
        self.home_icon = PhotoImage(file=ruta_icono_home)
        self.salir_icon = PhotoImage(file=ruta_icono_salir)
        self.x_icon = PhotoImage(file=ruta_icono_x)

    def crear_frames(self):
        self.page_frame = Frame(self.ventana, bg='black')
        self.page_frame.place(relwidth=1.0, relheight=1.0, x=50)

        self.menu_bar_frame = Frame(self.ventana, bg=self.menu_bar_colour)
        self.menu_bar_frame.pack(side=LEFT, fill=Y, pady=4, padx=3)
        self.menu_bar_frame.pack_propagate(False)
        self.menu_bar_frame.configure(width=45)

    def configurar_menu_lateral(self):
        self.home_btn_indicator = Label(self.menu_bar_frame, bg='black')
        self.home_btn_indicator.place(x=3, y=250, height=40, width=3)

        self.mas_btn_indicator = Label(self.menu_bar_frame, bg='white')
        self.mas_btn_indicator.place(x=3, y=310, height=40, width=3)

        self.block_btn_indicator = Label(self.menu_bar_frame, bg='white')
        self.block_btn_indicator.place(x=3, y=370, height=40, width=3)

        # Botón de toggle
        self.toggle_menu_btn = Button(
            self.menu_bar_frame,
            image=self.toggle_icon,
            bg=self.menu_bar_colour,
            activebackground=self.menu_bar_colour,
            bd=0,
            command=self.extend_bar_frame
        )
        self.toggle_menu_btn.place(x=7, y=10)

        # Botón Home/Proyectos
        self.home_menu_btn = Button(
            self.menu_bar_frame,
            image=self.home_icon,
            bg=self.menu_bar_colour,
            activebackground=self.menu_bar_colour,
            bd=0,
            command=lambda: self.switch_indication(self.home_btn_indicator, self.proyectos_page)
        )
        self.home_menu_btn.place(x=9, y=250, width=30, height=40)

        self.home_page_lb = Label(
            self.menu_bar_frame,
            text='Proyectos',
            bg='white',
            fg='black',
            font=('Arial', 10),
            anchor=W
        )
        self.home_page_lb.place(x=45, y=250, width=100, height=40)
        self.home_page_lb.bind(
            "<Button-1>",
            lambda e: self.switch_indication(self.home_btn_indicator, self.proyectos_page)
        )

        # Botón Agregar/Más
        self.mas_menu_btn = Button(
            self.menu_bar_frame,
            image=self.mas_icon,
            bg=self.menu_bar_colour,
            activebackground=self.menu_bar_colour,
            bd=0,
            command=lambda: self.switch_indication(self.mas_btn_indicator, self.agregar_page)
        )
        self.mas_menu_btn.place(x=9, y=310, width=30, height=40)

        self.mas_page_lb = Label(
            self.menu_bar_frame,
            text='Crear Proyecto',
            bg='white',
            fg='black',
            font=('Arial', 10),
            anchor=W
        )
        self.mas_page_lb.place(x=45, y=310, width=100, height=40)
        self.mas_page_lb.bind(
            "<Button-1>",
            lambda e: self.switch_indication(self.mas_btn_indicator, self.agregar_page)
        )

        # Botón Materiales
        self.block_menu_btn = Button(
            self.menu_bar_frame,
            image=self.block_icon,
            bg=self.menu_bar_colour,
            activebackground=self.menu_bar_colour,
            bd=0,
            command=self.ir_a_mat
        )
        self.block_menu_btn.place(x=9, y=370, width=30, height=40)

        self.block_page_lb = Label(
            self.menu_bar_frame,
            text='Materiales',
            bg='white',
            fg='black',
            font=('Arial', 10),
            anchor=W
        )
        self.block_page_lb.place(x=45, y=370, width=100, height=40)
        self.block_page_lb.bind(
            "<Button-1>",
            lambda e: (self.block_btn_indicator.config(bg='black'), self.ir_a_mat())
        )

        # Botón Salir
        self.salir_menu_btn = Button(
            self.menu_bar_frame,
            image=self.salir_icon,
            bg=self.menu_bar_colour,
            activebackground=self.menu_bar_colour,
            bd=0,
            command=self.cerrar_sesion
        )
        self.salir_menu_btn.place(relx=0.5, rely=1.0, anchor='s')

        salir_btn_indicator = Label(self.menu_bar_frame, bg='white')
        salir_btn_indicator.place(x=3, y=720, height=40, width=3)

    # ---------- MÉTODOS DE ANIMACIÓN DEL MENÚ ----------

    def _extending_animation(self):
        # Animación para extender el menú lateral
        current_width = self.menu_bar_frame.winfo_width()
        if not current_width > 200:
            current_width += 10
            self.menu_bar_frame.config(width=current_width)
            self.ventana.after(ms=8, func=self._extending_animation)

    def extend_bar_frame(self):
        # Extiende el menú lateral
        self._extending_animation()
        self.toggle_menu_btn.config(image=self.x_icon)
        self.toggle_menu_btn.config(command=self.fold_menu_bar)

    def _folding_animation(self):
        # Animación para contraer el menú lateral
        current_width = self.menu_bar_frame.winfo_width()
        if current_width != 45:
            current_width -= 10
            self.menu_bar_frame.config(width=current_width)
            self.ventana.after(ms=8, func=self._folding_animation)

    def fold_menu_bar(self):
        # Contrae el menú lateral
        self._folding_animation()
        self.toggle_menu_btn.config(image=self.toggle_icon)
        self.toggle_menu_btn.config(command=self.extend_bar_frame)

    # ---------- MÉTODOS DE NAVEGACIÓN ----------

    def switch_indication(self, indicador_lb, page):
        # Cambia el indicador activo y muestra la página correspondiente
        # Resetear todos los indicadores
        self.home_btn_indicator.config(bg='white')
        self.mas_btn_indicator.config(bg='white')
        self.block_btn_indicator.config(bg='white')

        # Activar el indicador seleccionado
        indicador_lb.config(bg='black')

        # Contraer menú si está extendido
        if self.menu_bar_frame.winfo_width() > 45:
            self.fold_menu_bar()

        # Limpiar página actual
        for frame in self.page_frame.winfo_children():
            frame.destroy()

        # Mostrar nueva página
        page()

    # ---------- MÉTODOS DE PÁGINAS ----------

    def proyectos_page(self):
        home_page_fm = Frame(self.page_frame, bg='black')
        lb = Label(home_page_fm, text='Proyectos', font=('Arial', 20), bg='black', fg='white')
        lb.place(x=100, y=20)
        home_page_fm.pack(fill=BOTH, expand=True)

        # Configurar TreeView
        self.cabecera = ["ID", "Nombre", "Descripción", "Estado", "Fecha Inicio", "Fecha Fin"]

        self.tree = ttk.Treeview(home_page_fm, height=10, columns=("#1", "#2", "#3", "#4", "#5"))
        self.tree.place(x=50, y=100)

        self.tree.column("#0", width=50)
        self.tree.heading("#0", text=self.cabecera[0], anchor=CENTER)
        self.tree.column("#1", width=150)
        self.tree.heading("#1", text=self.cabecera[1], anchor=CENTER)
        self.tree.column("#2", width=350)
        self.tree.heading("#2", text=self.cabecera[2], anchor=CENTER)
        self.tree.column("#3", width=150)
        self.tree.heading("#3", text=self.cabecera[3], anchor=CENTER)
        self.tree.column("#4", width=150)
        self.tree.heading("#4", text=self.cabecera[4], anchor=CENTER)
        self.tree.column("#5", width=150)
        self.tree.heading("#5", text=self.cabecera[5], anchor=CENTER)
        self.tree.bind("<Button-1>", self.seleccionarProyectosUsandoClick)

        # Cargar datos
        GestorDetalleProyecto.mostrar(self.tree, self.id_usuario)

        # Botón de selección
        Button(
            home_page_fm,
            text="Seleccionar",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='black',
            width=12,
            command=self.mostrar_detalle_proyecto
        ).place(x=50, y=360)

    def agregar_page(self):
        agregar_page_fm = Frame(self.page_frame, bg='black')
        lb = Label(agregar_page_fm, text='Agregar proyecto', font=('Arial', 20), bg='black', fg='white')
        lb.place(x=150, y=20)
        agregar_page_fm.pack(fill=BOTH, expand=True)

        Label(agregar_page_fm, text="Nombre:", bg='black', fg='white', font=('Arial', 12)).place(x=50, y=80)
        Entry(agregar_page_fm, textvariable=self.nombre_var, width=30).place(x=250, y=80)

        Label(agregar_page_fm, text="Descripción:", bg='black', fg='white', font=('Arial', 12)).place(x=50, y=120)
        Entry(agregar_page_fm, textvariable=self.descripcion_var, width=50).place(x=250, y=120)

        Label(agregar_page_fm, text="No. Personas:", bg='black', fg='white', font=('Arial', 12)).place(x=50, y=160)
        Entry(agregar_page_fm, textvariable=self.no_usuarios_var, width=30).place(x=250, y=160)

        Label(agregar_page_fm, text="Fecha de Inicio:", bg='black', fg='white', font=('Arial', 12)).place(x=50, y=200)
        DateEntry(
            agregar_page_fm,
            textvariable=self.fecha_inicio_var,
            width=27,
            date_pattern='yyyy-mm-dd',
            background='darkblue',
            foreground='white',
            borderwidth=2
        ).place(x=250, y=200)

        Label(agregar_page_fm, text="Fecha de Fin (Estimado):", bg='black', fg='white', font=('Arial', 12)).place(x=50, y=240)
        DateEntry(
            agregar_page_fm,
            textvariable=self.fecha_fin_var,
            width=27,
            date_pattern='yyyy-mm-dd',
            background='darkblue',
            foreground='white',
            borderwidth=2
        ).place(x=250, y=240)

        cliente_frame = LabelFrame(
            agregar_page_fm,
            text="Datos del cliente",
            bg='black',
            fg='white',
            font=('Arial', 10, 'bold'),
            labelanchor='n',
            bd=2
        )
        cliente_frame.place(x=50, y=290, width=550, height=210)

        Label(cliente_frame, text="Nombre:", bg='black', fg='white').place(x=10, y=10)
        Entry(cliente_frame, textvariable=self.cliente_nombre_var, width=20).place(x=100, y=10)

        Label(cliente_frame, text="Apellido:", bg='black', fg='white').place(x=280, y=10)
        Entry(cliente_frame, textvariable=self.cliente_apellido_var, width=20).place(x=360, y=10)

        Label(cliente_frame, text="Teléfono:", bg='black', fg='white').place(x=10, y=45)
        Entry(cliente_frame, textvariable=self.cliente_telefono_var, width=20).place(x=100, y=45)

        Label(cliente_frame, text="Mail:", bg='black', fg='white').place(x=280, y=45)
        Entry(cliente_frame, textvariable=self.cliente_mail_var, width=20).place(x=360, y=45)

        Label(cliente_frame, text="Referencia:", bg='black', fg='white').place(x=10, y=80)
        Entry(cliente_frame, textvariable=self.cliente_datos_ref_var, width=42).place(x=100, y=80)

        Label(cliente_frame, text="Dirección:", bg='black', fg='white').place(x=10, y=115)
        Entry(cliente_frame, textvariable=self.cliente_direccion_var, width=42).place(x=100, y=115)

        Button(
            agregar_page_fm,
            text="Guardar",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='black',
            width=12,
            command=self.guardar_proyecto
        ).place(x=150, y=520)


    def mostrar_detalle_proyecto(self):
        if not self.id_proyecto.get():
            messagebox.showerror("Error", "No se ha seleccionado un proyecto.")
            return

        # Limpiar página actual
        for frame in self.page_frame.winfo_children():
            frame.destroy()

        detalle_fm = Frame(self.page_frame, bg='black')
        detalle_fm.pack(fill=BOTH, expand=True)

        menu_superior_fm = Frame(detalle_fm, bg='black', height=150)
        menu_superior_fm.pack(side=TOP, fill=X, pady=20)

        contenido = Frame(detalle_fm, bg='black')
        contenido.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=10)

        self.frame_administracion = Frame(contenido, bg='#1a1a1a')
        self.frame_administracion.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_mano_obra = Frame(contenido, bg='#1a1a1a')
        self.frame_mano_obra.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_materiales = Frame(contenido, bg='#1a1a1a')
        self.frame_materiales.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_detalles = Frame(contenido, bg='#1a1a1a')
        self.frame_detalles.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.contenido_detalles()
        self.contenido_administracion()
        self.contenido_mano_obra()
        self.contenido_materiales()

        Button(
            menu_superior_fm,
            text='← Volver a Proyectos',
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='black',
            command=lambda: self.switch_indication(self.home_btn_indicator, self.proyectos_page)
        ).pack(side=LEFT, padx=10)

        Button(
            menu_superior_fm,
            text='Detalles',
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='black',
            command=lambda: self.frame_detalles.tkraise()
        ).pack(side=LEFT, padx=10)

        Label(
            menu_superior_fm,
            text='Opciones - presupuesto:',
            font=('Arial', 12),
            bg='black',
            fg='white'
        ).pack(side=LEFT, padx=15)

        Button(
            menu_superior_fm,
            text='Administración',
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='black',
            command=lambda: self.frame_administracion.tkraise()
        ).pack(side=LEFT, padx=10)

        Button(
            menu_superior_fm,
            text='Mano de obra',
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='black',
            command=lambda: self.frame_mano_obra.tkraise()
        ).pack(side=LEFT, padx=10)

        Button(
            menu_superior_fm,
            text='Materiales',
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='black',
            command=lambda: self.frame_materiales.tkraise()
        ).pack(side=LEFT, padx=10)

    def contenido_detalles(self):
        Label(self.frame_detalles, text='Detalles del Proyecto', font=('Arial', 16, 'bold'), bg='#1a1a1a', fg='white').pack(pady=20)

        Label(self.frame_detalles, text=f'Nombre:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(anchor='w', padx=30, pady=5)
        Entry(self.frame_detalles, textvariable=self.nombre, width=40).pack(anchor='w', padx=30, pady=5)

        Label(self.frame_detalles, text=f'Descripción:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(anchor='w', padx=30, pady=5)
        Entry(self.frame_detalles, textvariable=self.descripcion, width=40).pack(anchor='w', padx=30, pady=5)

        Label(self.frame_detalles, text=f'No. Usuarios:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(anchor='w', padx=30, pady=5)
        Entry(self.frame_detalles, textvariable=self.n_usuarios, width=40).pack(anchor='w', padx=30, pady=5)

        Label(self.frame_detalles, text=f'Estado:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(anchor='w', padx=30, pady=5)
        opciones = ['planeado','en_progreso','finalizado']
        OptionMenu(self.frame_detalles, self.estado, *opciones).pack(anchor='w', padx=30, pady=5)

        Label(self.frame_detalles, text=f'Fecha Inicio:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(anchor='w', padx=30, pady=5)
        self.date_inicio_widget = DateEntry(
            self.frame_detalles,
            width=27,
            date_pattern='yyyy-mm-dd',
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.date_inicio_widget.pack(anchor='w', padx=30, pady=5)
        fecha_inicio_obj = datetime.strptime(self.fecha_inicio.get(), '%Y-%m-%d')
        self.date_inicio_widget.set_date(fecha_inicio_obj)

        Label(self.frame_detalles, text=f'Fecha Fin:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(anchor='w', padx=30, pady=5)
        self.date_fin_widget = DateEntry(
            self.frame_detalles,
            width=27,
            date_pattern='yyyy-mm-dd',
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.date_fin_widget.pack(anchor='w', padx=30, pady=5)
        fecha_fin_obj = datetime.strptime(self.fecha_final.get(), '%Y-%m-%d')
        self.date_fin_widget.set_date(fecha_fin_obj)

        Label(self.frame_detalles, text=f'Duración (días):', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(anchor='w', padx=30, pady=5)
        Entry(self.frame_detalles, textvariable=self.duracion, width=40, state='readonly').pack(anchor='w', padx=30, pady=5)

        Label(self.frame_detalles, text=f'Presupuesto total:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(anchor='w', padx=30, pady=5)
        total = ServicioProyecto.calcular_presupuesto_total(self.id_proyecto.get())
        self.presupuesto_total.set(f'Q {total:.2f}')
        Label(self.frame_detalles, textvariable=self.presupuesto_total, font=('Arial', 12), bg='#1a1a1a', fg='white').pack(anchor='w', padx=30, pady=5)

        Button(self.frame_detalles, text='Guardar', font=('Arial', 11, 'bold'), bg='white', fg='black', command=self.actualizar_proyecto).pack(anchor='w', padx=30, pady=10)

    def contenido_administracion(self):
        Label(self.frame_administracion, text='Administración del Proyecto', font=('Arial', 16, 'bold'), bg='#1a1a1a', fg='white').pack(pady=20)

        total = ServicioAdministracion.obtener_costo_total_administracion(self.id_proyecto.get())
        self.total_costo_administracion.set(f'Total (Q): {total:.2f}')
        Label(self.frame_administracion, textvariable=self.total_costo_administracion, font=('Arial', 14, 'bold'), bg='#1a1a1a', fg='white').pack(pady=20)

    def contenido_mano_obra(self):
        Label(self.frame_mano_obra, text='Mano de Obra', font=('Arial', 16, 'bold'), bg='#1a1a1a', fg='white').pack(pady=20)

        total = ServicioDetalleManoObra.obtener_costo_total_mano_obra(self.id_proyecto.get())
        self.total_costo_mano_obra.set(f'Total (Q): {total:.2f}')
        Label(self.frame_mano_obra, textvariable=self.total_costo_mano_obra, font=('Arial', 14, 'bold'), bg='#1a1a1a', fg='white').pack(pady=20)

    def contenido_materiales(self):
        Label(self.frame_materiales, text='Materiales del Proyecto', font=('Arial', 16, 'bold'), bg='#1a1a1a', fg='white').pack(pady=20)

        total = ServicioDetalleMateriales.obtener_costo_total_materiales(self.id_proyecto.get())
        self.total_costo_materiales.set(f'Total (Q): {total:.2f}')
        Label(self.frame_materiales, textvariable=self.total_costo_materiales, font=('Arial', 14, 'bold'), bg='#1a1a1a', fg='white').pack(pady=20)

        self.cabecera_mat = ["ID", "Descripción", "Unidad", "Costo Unitario", "Cantidad", "Costo total"]

        self.tree_mat = ttk.Treeview(self.frame_materiales, height=10, columns=("#1", "#2", "#3", "#4", "#5"))
        self.tree_mat.pack(anchor='center', padx=10, pady=10)

        self.tree_mat.column("#0", width=50)
        self.tree_mat.heading("#0", text=self.cabecera_mat[0], anchor=CENTER)
        self.tree_mat.column("#1", width=350)
        self.tree_mat.heading("#1", text=self.cabecera_mat[1], anchor=CENTER)
        self.tree_mat.column("#2", width=150)
        self.tree_mat.heading("#2", text=self.cabecera_mat[2], anchor=CENTER)
        self.tree_mat.column("#3", width=150)
        self.tree_mat.heading("#3", text=self.cabecera_mat[3], anchor=CENTER)
        self.tree_mat.column("#4", width=150)
        self.tree_mat.heading("#4", text=self.cabecera_mat[4], anchor=CENTER)
        self.tree_mat.column("#5", width=150)
        self.tree_mat.heading("#5", text=self.cabecera_mat[5], anchor=CENTER)
        self.tree_mat.bind("<Button-1>", self.seleccionarMaterialesUsandoClick)
        GestorDetalleMateriales.mostrar(self.tree_mat, self.id_proyecto.get())

        frame_campos_mat1 = Frame(self.frame_materiales, bg='#1a1a1a')
        frame_campos_mat1.pack(anchor='center', pady=5)
        frame_campos_mat2 = Frame(self.frame_materiales, bg='#1a1a1a')
        frame_campos_mat2.pack(anchor='center', pady=5)

        Label(frame_campos_mat1, text=f'Descripción:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(side=LEFT, padx=4)
        Label(frame_campos_mat1, textvariable=self.descripcion_material, width=40, bg='white', fg='black').pack(side=LEFT, padx=4)
        Label(frame_campos_mat1, text=f'Unidad:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(side=LEFT, padx=4)
        Label(frame_campos_mat1, textvariable=self.unidad_material, width=20, bg='white', fg='black').pack(side=LEFT, padx=4)
        Label(frame_campos_mat2, text=f'Costo unitario:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(side=LEFT, padx=4)
        Label(frame_campos_mat2, textvariable=self.costo_unitario, width=10, bg='white', fg='black').pack(side=LEFT, padx=4)
        Label(frame_campos_mat2, text=f'Cantidad:', font=('Arial', 12), bg='#1a1a1a', fg='white').pack(side=LEFT, padx=4)
        Entry(frame_campos_mat2, textvariable=self.cantidad_material, width=10).pack(side=LEFT, padx=4)

        Button(self.frame_materiales, text='Guardar/Actualizar', font=('Arial', 11, 'bold'), bg='white', fg='black', command=self.guardar_detalle_material).pack(anchor='center', padx=30, pady=10)


    # ---------- MÉTODOS DE ACCIONES ----------

    def guardar_proyecto(self):
        nombre = self.nombre_var.get()
        descripcion = self.descripcion_var.get()
        n_usuarios = self.no_usuarios_var.get()
        fecha_inicio = self.fecha_inicio_var.get()
        fecha_fin = self.fecha_fin_var.get()

        estado = "planeado"
        presupuesto_total = 0

        cli_nombre = self.cliente_nombre_var.get()
        cli_apellido = self.cliente_apellido_var.get()
        cli_tel = self.cliente_telefono_var.get()
        cli_mail = self.cliente_mail_var.get()
        cli_ref = self.cliente_datos_ref_var.get()
        cli_dir = self.cliente_direccion_var.get()

        if not (validar_campo_lleno(nombre) and validar_campo_lleno(descripcion) and
                validar_campo_lleno(n_usuarios) and validar_campo_lleno(fecha_inicio) and
                validar_campo_lleno(fecha_fin)):
            messagebox.showerror("Error", "Todos los campos del proyecto deben estar llenos.")
            return

        if not validar_numero(n_usuarios):
            messagebox.showerror("Error", "La cantidad de usuarios debe ser un número.")
            return
        n_usuarios = int(n_usuarios)

        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            duracion = (fin - inicio).days

            if duracion < 0:
                messagebox.showerror("Error", "La fecha de fin debe ser posterior a la fecha de inicio.")
                return
        except ValueError:
            messagebox.showerror("Error", "Las fechas deben estar en formato válido.")
            return

        id_cliente = None

        if validar_campo_lleno(cli_nombre) and validar_campo_lleno(cli_apellido):
            try:
                id_cliente = ServicioClientes.crear(
                    cli_nombre,
                    cli_apellido,
                    cli_tel,
                    cli_mail,
                    cli_ref,
                    cli_dir
                )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el cliente: {e}")
                return

        id_proyecto = ServicioProyecto.crear(
            nombre=nombre,
            descripcion=descripcion,
            n_usuarios=n_usuarios,
            fecha_inicio=fecha_inicio,
            duracion=duracion,
            fecha_fin=fecha_fin,
            estado=estado,
            presupuesto_total=presupuesto_total,
            id_cliente=id_cliente
        )

        ServicioDetalleProyecto.crear(self.id_usuario, id_proyecto)

        try:
            GestorDetalleProyecto.mostrar(self.tree, self.id_usuario)
        except Exception:
            pass

        self.nombre_var.set("")
        self.descripcion_var.set("")
        self.no_usuarios_var.set("")
        self.fecha_inicio_var.set("")
        self.fecha_fin_var.set("")

        self.cliente_nombre_var.set("")
        self.cliente_apellido_var.set("")
        self.cliente_telefono_var.set("")
        self.cliente_mail_var.set("")
        self.cliente_datos_ref_var.set("")
        self.cliente_direccion_var.set("")

        messagebox.showinfo("Éxito", f"Proyecto '{nombre}' creado exitosamente.")

    def actualizar_proyecto(self):
        nombre = self.nombre.get()
        descripcion = self.descripcion.get()
        n_usuarios = self.n_usuarios.get()
        estado = self.estado.get()
        fecha_inicio = self.date_inicio_widget.get_date().strftime('%Y-%m-%d')
        fecha_fin = self.date_fin_widget.get_date().strftime('%Y-%m-%d')
        duracion = self.duracion.get()
        presupuesto = self.presupuesto_total.get()

        if not (validar_campo_lleno(nombre) and validar_campo_lleno(descripcion) and
                validar_campo_lleno(n_usuarios) and validar_campo_lleno(fecha_inicio) and
                validar_campo_lleno(fecha_fin)):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            duracion = (fin - inicio).days

            if duracion < 0:
                messagebox.showerror("Error", "La fecha de fin debe ser posterior a la fecha de inicio.")
                return
        except ValueError:
            messagebox.showerror("Error", "Las fechas deben estar en formato válido.")
            return

        self.duracion.set(f'{duracion}')

        ServicioProyecto.actualizar(
            nombre, descripcion, n_usuarios, fecha_inicio, duracion, fecha_fin, estado, presupuesto, self.id_proyecto.get()
        )

        messagebox.showinfo("Éxito", f"Proyecto '{nombre}' actualizado exitosamente.")

    def guardar_detalle_material(self):
        proyecto = self.id_proyecto.get()
        material = self.id_material.get()
        cantidad_nueva = self.cantidad_material.get()
        costo_unitario = self.costo_unitario.get()

        cantidad_cons = ServicioDetalleMateriales.buscar_por_id(proyecto, material)

        if not (validar_campo_lleno(cantidad_nueva) and validar_numero(cantidad_nueva)):
            messagebox.showerror("Error", "La cantidad debe llenarse y ser un número.")
            return

        costo_total = float(cantidad_nueva) * float(costo_unitario)

        if cantidad_cons is None:
            ServicioDetalleMateriales.crear(proyecto, material, cantidad_nueva, costo_total)
        else:
            ServicioDetalleMateriales.actualizar(cantidad_nueva, costo_total, proyecto, material)

        GestorDetalleMateriales.mostrar(self.tree_mat, self.id_proyecto.get())
        total_proyecto = ServicioProyecto.calcular_presupuesto_total(self.id_proyecto.get())
        self.presupuesto_total.set(f'Q {total_proyecto:.2f}')
        total_materiales = ServicioDetalleMateriales.obtener_costo_total_materiales(self.id_proyecto.get())
        self.total_costo_materiales.set(f'Total (Q): {total_materiales:.2f}')

        messagebox.showinfo("Éxito", f"Material registrado.")

    def seleccionarProyectosUsandoClick(self, event):
        id_seleccionado = seleccionar_haciendo_click(
            tree=self.tree,
            event=event,
            id_var=self.id_proyecto,
            campos_vars=[]
        )

        if not id_seleccionado:
            return

        # Cargar datos del proyecto
        datos = ServicioProyecto.buscar_por_id(id_seleccionado)
        if datos:
            self.nombre.set(datos[1])
            self.descripcion.set(datos[2])
            self.n_usuarios.set(datos[3])
            self.fecha_inicio.set(datos[4])
            self.duracion.set(datos[5])
            self.fecha_final.set(datos[6])
            self.estado.set(datos[7])
            self.presupuesto_total.set(datos[8])
            self.id_cliente.set(datos[9])

    def seleccionarMaterialesUsandoClick(self, event):
        id_seleccionado = seleccionar_haciendo_click(
            tree=self.tree_mat,
            event=event,
            id_var=self.id_material,
            campos_vars=[self.descripcion_material, self.unidad_material, self.costo_unitario, self.cantidad_material, self.costo_total]
        )

    def ir_a_mat(self):
        Materiales()

    def cerrar_sesion(self):
        ventana_menu_principal.destroy()
        ventana_login.deiconify()
        ventana_login.state('zoomed')


app = ControladorLogin.iniciar_app()
app.iniciar_mainloop()