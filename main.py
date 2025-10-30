from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from manejo_db import *
import os

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

class Login:
    def __init__(self):
        global ventana_login
        ventana_login = Tk()
        ventana_login.title("Login")
        ventana_login.state("zoomed")
        ventana_login.geometry('900x800')

        fondo = 'white'

        self.left_frame = Frame(ventana_login)
        self.left_frame.configure(bg=fondo)
        self.left_frame.pack(expand=True, fill="both", side='left')

        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        content = Frame(self.left_frame, bg=fondo)
        content.grid(row=1, column=0)

        Label(content, text="Usuario", font=("Arial", 20), fg="black", bg=fondo).pack(pady=10)
        self.usuario = Entry(content, width=40, bd=1)
        self.usuario.pack(pady=10)

        Label(content, text="Contraseña", font=("Arial", 20), fg="black", bg=fondo).pack(pady=10)
        self.contrasena = Entry(content, width=40, show='*', bd=1)
        self.contrasena.pack(pady=10)

        def acceder():
            self.user = self.usuario.get()
            self.password = self.contrasena.get()

            if self.user and self.password:
                if self.user == 'admin':
                    if self.password == '1234':
                        Admin()
                        ventana_login.withdraw()
                    else:
                        messagebox.showerror('Error', 'Contraseña incorrecta.')
                else:
                    usuario_encontrado = ServicioUsuarios.buscar_usuario_password(self.user, self.password)
                    if usuario_encontrado:
                        MenuPrincipal()
                        ventana_login.withdraw()
                    else:
                        messagebox.showerror('Error', 'Usuario o contraseña incorrectos.')
            else:
                messagebox.showerror("Error", "Ingrese su usuario y contraseña.")

        Button(content, text="Iniciar sesión", font=("Arial", 16), bg="white", fg="black", command=acceder).pack(pady=20)

        self.right_frame = Frame(ventana_login, bg= 'black')
        self.right_frame.pack(expand=True, fill="both", side='right')

        self.imagen_original = Image.open("21design2.png")
        self.label_img = Label(self.right_frame, bg="black")
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
        ventana_admin = Toplevel(ventana_login)
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
                self.usuario.delete(0, END)
                self.usuario.insert(0, usuario_generado)
                self.usuario.config(state='readonly')

            else:
                messagebox.showerror('Error', 'El nombre y/o apellido están vacíos.')

        def guardar_usuario():
            self.nombre_usuario = self.nombres.get()
            self.apellido_usuario = self.apellidos.get()
            self.usuario_nuevo = self.usuario.get()
            self.contrasena_usuario = self.contrasena.get()
            self.contrasena_conf_usuario = self.contrasena_conf.get()

            if validar_campo_lleno(self.nombre_usuario) and validar_campo_lleno(self.apellido_usuario) and validar_campo_lleno(self.usuario_nuevo) and validar_campo_lleno(self.contrasena_usuario) and validar_campo_lleno(self.contrasena_conf_usuario):
                if self.contrasena_usuario == self.contrasena_conf_usuario:
                    ServicioUsuarios.crear(self.nombre_usuario, self.apellido_usuario, self.usuario_nuevo, self.contrasena_usuario)
                    messagebox.showinfo('Usuario creado', 'Usuario creado satisfactoriamente.')
                else:
                    messagebox.showerror('Error', 'La contraseña debe coincidir.')
            else:
                messagebox.showerror('Error', 'Todos los campos deben estar llenos.')

        def mostrar_usuarios():
            GestorUsuarios.mostrar(self.tree)
            frame_mostrar_usuarios.tkraise()

        def seleccionar_usuario():
            if not self.miID_usuario.get():
                messagebox.showerror('Error', 'Seleccione un usuario primero.')
                return

            datos = ServicioUsuarios.buscar_id(self.miID_usuario.get())
            if datos:
                self.nombres_m.delete(0, END)
                self.nombres_m.insert(0, datos[1])
                self.apellidos_m.delete(0, END)
                self.apellidos_m.insert(0, datos[2])
                self.miUsuario.set(f'Usuario: {datos[3]}')
                self.contrasena_m.delete(0, END)
                self.contrasena_m.insert(0, datos[4])
                self.contrasena_conf_m.delete(0, END)
                self.contrasena_conf_m.insert(0, datos[4])
                frame_modificar_usuario.tkraise()
            else:
                messagebox.showerror('Error', 'Usuario no encontrado.')

        def modificar_usuario():
            ide = self.miID_usuario.get()
            nuevo_nombre = self.nombres_m.get()
            nuevo_apellido = self.apellidos_m.get()
            usuario_seleccionado = self.miUsuario.get().replace('Usuario: ', '')
            nueva_contrasena = self.contrasena_m.get()
            nueva_contrasena_conf = self.contrasena_conf_m.get()

            if validar_campo_lleno(nuevo_nombre) and validar_campo_lleno(nuevo_apellido) and validar_campo_lleno(nueva_contrasena) and validar_campo_lleno(nueva_contrasena_conf):
                if nueva_contrasena == nueva_contrasena_conf:
                    ServicioUsuarios.actualizar(nuevo_nombre, nuevo_apellido, usuario_seleccionado, nueva_contrasena, ide)
                    messagebox.showinfo('Usuario actualizado', 'Usuario actualizado satisfactoriamente.')
                    GestorUsuarios.mostrar(self.tree)
                    frame_mostrar_usuarios.tkraise()
                else:
                    messagebox.showerror('Error', 'La contraseña debe coincidir.')
            else:
                messagebox.showerror('Error', 'Todos los campos deben estar llenos.')

        def eliminar_usuario():
            if not self.miID_usuario.get():
                messagebox.showerror('Error', 'Seleccione un usuario primero.')
                return

            confirmar = messagebox.askyesno('Confirmar',f'¿Está seguro de eliminar el usuario con ID {self.miID_usuario.get()}?')

            if confirmar:
                try:
                    ServicioUsuarios.borrar(self.miID_usuario.get())
                    messagebox.showinfo('Éxito', 'Usuario eliminado correctamente.')
                    GestorUsuarios.mostrar(self.tree)
                    self.miID_usuario.set('')
                    self.miNombres.set('')
                    self.miApellidos.set('')
                    self.miUsuario.set('')
                except Exception as e:
                    messagebox.showerror('Error', f'Error al eliminar usuario: {e}')


        fondo = 'white'

        self.miID_usuario = StringVar()
        self.miNombres = StringVar()
        self.miApellidos = StringVar()
        self.miUsuario = StringVar()

        ventana_admin.protocol('WM_DELETE_WINDOW', cerrar_sesion)

        frame_principal = Frame(ventana_admin, bg='white')
        frame_principal.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame_add_usuario = Frame(ventana_admin, bg='white')
        frame_add_usuario.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame_mostrar_usuarios = Frame(ventana_admin, bg='white')
        frame_mostrar_usuarios.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame_modificar_usuario = Frame(ventana_admin, bg='white')
        frame_modificar_usuario.place(relx=0, rely=0, relwidth=1, relheight=1)


        # Contenido Frame principal
        Label(frame_principal, text='Menú de administrador', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)
        Button(frame_principal, text="Agregar usuario", font=("Arial", 16), bg="white", fg="black", command=lambda: frame_add_usuario.tkraise()).pack(pady=20)
        Button(frame_principal, text="Modificar datos de usuario", font=("Arial", 16), bg="white", fg="black", command=mostrar_usuarios).pack(pady=20)
        Button(frame_principal, text="Cerrar sesión", font=("Arial", 16), bg="white", fg="black", command=cerrar_sesion).pack(pady=20)


        # Contenido Frame - agregar usuario
        Button(frame_add_usuario, text='Regresar', font=('Arial', 16), bg="white", fg="black", command=lambda: frame_principal.tkraise()).pack(side='left', anchor='n', pady=20)
        Label(frame_add_usuario, text='Agregar usuario', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)
        Label(frame_add_usuario, text='Nombre:', font=("Arial", 14), bg=fondo).pack(anchor='center',pady=20)
        self.nombres = Entry(frame_add_usuario, width=40, bd=1)
        self.nombres.pack(anchor='center', pady=10)

        Label(frame_add_usuario, text='Apellido:', font=("Arial", 14), bg=fondo).pack(anchor='center',pady=20)
        self.apellidos = Entry(frame_add_usuario, width=40, bd=1)
        self.apellidos.pack(anchor='center', pady=10)

        fila_usuario = Frame(frame_add_usuario, width=100, bg=fondo)
        fila_usuario.pack(pady=20)
        Label(fila_usuario, text='Usuario:', font=("Arial", 14), bg=fondo).pack(side='left', padx=10)
        Button(fila_usuario, text='Generar usuario', font=('Arial', 12), bg="white", fg="black", command=generar_usuario).pack(side='right', padx=10)
        self.usuario = Entry(frame_add_usuario, width=40, bd=1, state='readonly')
        self.usuario.pack(anchor='center', pady=10)

        Label(frame_add_usuario, text='Contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center',pady=20)
        self.contrasena = Entry(frame_add_usuario, width=40, bd=1)
        self.contrasena.pack(anchor='center', pady=10)

        Label(frame_add_usuario, text='Confirmar contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center',pady=20)
        self.contrasena_conf = Entry(frame_add_usuario, width=40, bd=1)
        self.contrasena_conf.pack(anchor='center', pady=10)

        Button(frame_add_usuario, text='Guardar', font=('Arial', 16), bg="white", fg="black", command=guardar_usuario).pack(anchor='center', pady=10)

        # Contenido Frame - mostrar usuarios
        Button(frame_mostrar_usuarios, text='Regresar', font=('Arial', 16), bg="white", fg="black", command=lambda: frame_principal.tkraise()).pack(side='left', anchor='n', pady=20)
        Label(frame_mostrar_usuarios, text='Mostrar usuarios', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)

        self.cabecera = ["ID", "Nombres", "Apellidos", "Usuario"]
        self.tree = ttk.Treeview(frame_mostrar_usuarios, height=10, columns=("#1", "#2", "#3"))
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

        GestorUsuarios.mostrar(self.tree)

        Button(frame_mostrar_usuarios, text='Eliminar', font=('Arial', 16), bg="white", fg="black", command=eliminar_usuario).pack(side='left', pady=20)
        Button(frame_mostrar_usuarios, text='Modificar', font=('Arial', 16), bg="white", fg="black", command=seleccionar_usuario).pack(side='right', pady=20)


        # Contenido Frame - modificar usuario
        Button(frame_modificar_usuario, text='Regresar', font=('Arial', 16), bg="white", fg="black", command=lambda: frame_mostrar_usuarios.tkraise()).pack(side='left', anchor='n', pady=20)
        Label(frame_modificar_usuario, text='Modificar usuario', font=("Arial", 16, 'bold'), bg=fondo).pack(pady=20)

        Label(frame_modificar_usuario, textvariable=self.miUsuario, font=('Arial', 14), bg=fondo).pack(anchor='center',pady=20)

        Label(frame_modificar_usuario, text='Nombre:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.nombres_m = Entry(frame_modificar_usuario, width=40, bd=1)
        self.nombres_m.pack(anchor='center', pady=10)

        Label(frame_modificar_usuario, text='Apellido:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.apellidos_m = Entry(frame_modificar_usuario, width=40, bd=1)
        self.apellidos_m.pack(anchor='center', pady=10)

        Label(frame_modificar_usuario, text='Contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.contrasena_m = Entry(frame_modificar_usuario, width=40, bd=1)
        self.contrasena_m.pack(anchor='center', pady=10)

        Label(frame_modificar_usuario, text='Confirmar contraseña:', font=("Arial", 14), bg=fondo).pack(anchor='center', pady=20)
        self.contrasena_conf_m = Entry(frame_modificar_usuario, width=40, bd=1)
        self.contrasena_conf_m.pack(anchor='center', pady=10)

        Button(frame_modificar_usuario, text='Guardar', font=('Arial', 16), bg="white", fg="black", command=modificar_usuario).pack(anchor='center', pady=10)

        frame_principal.tkraise()

    def seleccionarUsandoClick(self, event):
        id_seleccionado = seleccionar_haciendo_click(
            tree=self.tree,
            event=event,
            id_var=self.miID_usuario,
            campos_vars = [self.miNombres, self.miApellidos, self.miUsuario]
        )

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

class MenuPrincipal():
    def __init__(self):
        global ventana_menu_principal
        ventana_menu_principal = Toplevel(ventana_login)
        ventana_menu_principal.title("21° Design")
        ventana_menu_principal.configure(background='black')
        ventana_menu_principal.geometry("400x600")
        ventana_menu_principal.state("zoomed")

        ventana_menu_principal.protocol('WM_DELETE_WINDOW', self.cerrar_sesion)

        menu_bar_colour = 'white'
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

        def switch_indication(indicador_lb):

            home_btn_indicator.config(bg='white')
            mas_btn_indicator.config(bg='white')
            block_btn_indicator.config(bg='white')

            indicador_lb.config(bg='black')

            if menu_bar_frame.winfo_width() > 45:
               fold_menu_bar()

        def extending_animation():
            current_width = menu_bar_frame.winfo_width()
            if not current_width > 200:
                current_width += 10
                menu_bar_frame.config(width=current_width)

                ventana_menu_principal.after(ms=8, func=extending_animation)

        def extend_bar_frame():
            extending_animation()
            self.toggle_menu_btn.config(image=self.x_icon)
            self.toggle_menu_btn.config(command=fold_menu_bar)

        def folding_animation():
            current_width = menu_bar_frame.winfo_width()
            if current_width != 45:
                current_width -= 10
                menu_bar_frame.config(width=current_width)

                ventana_menu_principal.after(ms=8, func=folding_animation)

        def fold_menu_bar():
            folding_animation()
            self.toggle_menu_btn.config(image=self.toggle_icon)
            self.toggle_menu_btn.config(command=extend_bar_frame)

        menu_bar_frame = Frame(ventana_menu_principal, bg=menu_bar_colour)
        menu_bar_frame.pack(side=LEFT, fill=Y, pady=4, padx=3)
        menu_bar_frame.pack_propagate(False)
        menu_bar_frame.configure(width=45)

        self.toggle_menu_btn = Button(
            menu_bar_frame,
            image=self.toggle_icon,
            bg=menu_bar_colour,
            activebackground=menu_bar_colour,
            bd=0,
            command=extend_bar_frame
        )
        self.toggle_menu_btn.place(x=9, y=10)

        self.home_menu_btn = Button(
            menu_bar_frame,
            image=self.home_icon,
            bg=menu_bar_colour,
            activebackground=menu_bar_colour,
            bd=0,
            command=lambda: switch_indication(indicador_lb=home_btn_indicator)
        )
        self.home_menu_btn.place(x=9, y=250, width=30, height=40)

        home_btn_indicator = Label(menu_bar_frame, bg='black')
        home_btn_indicator.place(x=3, y=250, height=40, width=3)

        self.home_page_lb = Label(menu_bar_frame, text='Proyectos', bg='white', fg='black',
                                  font=('Arial', 10), anchor=W)
        self.home_page_lb.place(x=45, y=250, width=100, height=40)
        self.home_page_lb.bind("<Button-1>", lambda e: switch_indication(indicador_lb=home_btn_indicator))

        self.mas_menu_btn = Button(
            menu_bar_frame,
            image=self.mas_icon,
            bg=menu_bar_colour,
            activebackground=menu_bar_colour,
            bd=0,
            command=lambda: switch_indication(indicador_lb=mas_btn_indicator)
        )
        self.mas_menu_btn.place(x=9, y=310, width=30, height=40)

        mas_btn_indicator = Label(menu_bar_frame, bg='white')
        mas_btn_indicator.place(x=3, y=310, height=40, width=3)

        self.mas_page_lb = Label(menu_bar_frame, text='Crear Proyecto', bg='white', fg='black',
                                  font=('Arial', 10), anchor=W)
        self.mas_page_lb.place(x=45, y=310, width=100, height=40)
        self.mas_page_lb.bind("<Button-1>", lambda e: switch_indication(indicador_lb=mas_btn_indicator))

        self.block_menu_btn = Button(
            menu_bar_frame,
            image=self.block_icon,
            bg=menu_bar_colour,
            activebackground=menu_bar_colour,
            bd=0,
            command=self.ir_a_mat
        )
        self.block_menu_btn.place(x=9, y=370, width=30, height=40)

        block_btn_indicator = Label(menu_bar_frame, bg='white')
        block_btn_indicator.place(x=3, y=370, height=40, width=3)

        self.block_page_lb = Label(menu_bar_frame, text='Materiales', bg='white', fg='black',
                                 font=('Arial', 10), anchor=W)
        self.block_page_lb.place(x=45, y=370, width=100, height=40)
        self.block_page_lb.bind("<Button-1>", lambda e: switch_indication(indicador_lb=block_btn_indicator))

        self.salir_menu_btn = Button(
            menu_bar_frame,
            image=self.salir_icon,
            bg=menu_bar_colour,
            activebackground=menu_bar_colour,
            bd=0,
            command=self.cerrar_sesion
        )
        self.salir_menu_btn.place(relx=0.5, rely=1.0, anchor='s')

        salir_btn_indicator = Label(menu_bar_frame, bg='white')
        salir_btn_indicator.place(x=3, y=720, height=40, width=3)

    def toggle_menu(self):
        print("Click en el botón del menú ✅")

    def agregar_proyecto(self):
        pass

    def ir_a_mat(self):
        Materiales()

    def cerrar_sesion(self):
        ventana_menu_principal.destroy()
        ventana_login.deiconify()
        ventana_login.state('zoomed')

login = Login()