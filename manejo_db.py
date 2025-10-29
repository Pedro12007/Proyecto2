import sqlite3
from tkinter import messagebox

db_name = '21design.db'

def conectar():
    miConexion = sqlite3.connect(db_name)
    miCursor = miConexion.cursor()
    return miConexion, miCursor

def validar_campo_lleno(entrada):
    return len(entrada.replace(' ', '')) > 0

class Cliente:
    def __init__(self, nombre, apellido, telefono, mail, datos_referencia, direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.mail = mail
        self.datos_referencia = datos_referencia
        self.direccion = direccion

    def info(self):
        return self.nombre, self.apellido, self.telefono, self.mail, self.datos_referencia, self.direccion

class ConsultaClientes:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        telefono TEXT,
        mail TEXT,
        datos_referencia TEXT,
        direccion TEXT
    );
    '''

class ServicioClientes:
    pass

class Usuario:
    def __init__(self, nombres, apellidos, usuario, contrasena):
        self.nombres = nombres
        self.apellidos = apellidos
        self.usuario = usuario
        self.contrasena = contrasena

    def info(self):
        return self.nombres, self.apellidos, self.usuario, self.contrasena

class ConsultaUsuarios:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombres TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL
    );
    '''
    INSERT = "INSERT INTO usuarios VALUES (NULL,?,?,?,?)"
    SELECT = "SELECT * FROM usuarios"
    UPDATE = "UPDATE usuarios SET nombres=?, apellidos=?, usuario=?, contrasena=? WHERE id_usuario=?"
    DELETE = "DELETE FROM usuarios WHERE id_usuario=?"
    BUSCAR = "SELECT * FROM usuarios WHERE nombres LIKE '%' || ? || '%' OR apellidos LIKE '%' || ? || '%'"

class ServicioUsuarios:
    @staticmethod
    def conexionBBDD():
        miConexion, miCursor = conectar()
        miCursor.execute(ConsultaUsuarios.CREATE)
        miConexion.commit()
        miConexion.close()

    @staticmethod
    def consultar():
        miConexion, miCursor = conectar()
        miCursor.execute(ConsultaUsuarios.SELECT)
        datos = miCursor.fetchall()
        miConexion.close()
        return datos

    @staticmethod
    def crear(nombres, apellidos, usuario_a, contrasena):
        miConexion, miCursor = conectar()
        usuario = Usuario(nombres, apellidos, usuario_a, contrasena)
        miCursor.execute(ConsultaUsuarios.INSERT, usuario.info())
        miConexion.commit()
        miConexion.close()

    @staticmethod
    def actualizar(nombres, apellidos, usuario_a, contrasena, ide):
        miConexion, miCursor = conectar()
        miCursor.execute(ConsultaUsuarios.UPDATE, (nombres, apellidos, usuario_a, contrasena, ide))
        miConexion.commit()
        miConexion.close()

    @staticmethod
    def borrar(id_usuario):
        conexion = sqlite3.connect(db_name)
        cursor = conexion.cursor()
        cursor.execute(ConsultaUsuarios.DELETE, (id_usuario,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_id(id_usuario):
        miConexion, miCursor = conectar()
        miCursor.execute('SELECT * FROM usuarios WHERE id_usuario=?', (id_usuario,))
        datos = miCursor.fetchone()
        miConexion.close()
        return datos

    @staticmethod
    def buscar_usuario_password(nombre_usuario, contrasena):
        miConexion, miCursor = conectar()
        miCursor.execute('SELECT * FROM usuarios WHERE usuario=? AND contrasena=?', (nombre_usuario, contrasena))
        datos = miCursor.fetchone()
        miConexion.close()
        return datos

class GestorUsuarios:
    @staticmethod
    def conexionBBDD():
        try:
            ServicioUsuarios.conexionBBDD()
            messagebox.showinfo("CONEXIÓN", "Base de datos conectada exitosamente")
        except:
            messagebox.showerror("ERROR", "Error al conectar la base de datos")

    @staticmethod
    def mostrar(tree):
        # limpiar tabla
        for elemento in tree.get_children():
            tree.delete(elemento)

        try:
            usuarios = ServicioUsuarios.consultar()
            for row in usuarios:
                tree.insert(
                    "",
                    "end",
                    text=row[0],
                    values=(row[1], row[2], row[3], row[4])
                )
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

    @staticmethod
    def buscar(tree, criterio):
        registros = tree.get_children()
        [tree.delete(elemento) for elemento in registros]
        try:
            if criterio != "":
                usuarios = ServicioUsuarios.buscar(criterio)
                [tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4])) for row in usuarios]
            else:
                messagebox.showwarning("ERROR", "No ha escrito un criterio de búsqueda")
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

class Proyecto:
    def __init__(self, nombre, descripcion, n_usuarios, fecha_inicio, duracion, fecha_fin, estado, presupuesto_total, id_cliente):
        self.nombre = nombre
        self.descripcion = descripcion
        self.n_usuarios = n_usuarios
        self.fecha_inicio = fecha_inicio
        self.duracion = duracion
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.presupuesto_total = presupuesto_total
        self.id_cliente = id_cliente

    def info(self):
        return self.nombre, self.descripcion, self.n_usuarios, self.fecha_inicio, self.duracion, self.fecha_fin, self.estado, self.presupuesto_total, self.id_cliente

class ConsultaProyecto:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS proyecto (
        id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        n_usuarios INTEGER DEFAULT 0 CHECK(n_usuarios >= 0),
        fecha_inicio TEXT,
        duracion TEXT,
        fecha_fin TEXT,
        estado TEXT CHECK(estado IN ('planeado','en_progreso','finalizado')),
        presupuesto_total REAL CHECK(presupuesto_total >= 0),
        id_cliente INTEGER,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON UPDATE CASCADE ON DELETE SET NULL
    );
    '''
    INSERT = "INSERT INTO proyecto VALUES (NULL,?,?,?,?,?,?,?,?,?)"
    SELECT = "SELECT * FROM proyecto "

class ServicioProyecto:
    pass

class DetalleProyecto:
    def __init__(self, id_usuario, id_proyecto):
        self.id_usuario = id_usuario
        self.id_proyecto = id_proyecto

    def info(self):
        return self.id_usuario, self.id_proyecto

class ConsultaDetalleProyecto:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS detalle_proyecto (
        id_detalle_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_proyecto INTEGER NOT NULL,
        UNIQUE(id_usuario, id_proyecto),
        FOREIGN KEY (id_usuario)  REFERENCES usuarios(id_usuario)  ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON UPDATE CASCADE ON DELETE CASCADE
    );
    '''
    INSERT = "INSERT INTO detalle_proyecto VALUES (NULL,?,?)"
    SELECT = '''
    SELECT p.id_proyecto, p.nombre, p.descripcion, p.estado, p.fecha_inicio, p.fecha_fin
    FROM detalle_proyecto dp
    INNER JOIN proyecto p ON dp.id_proyecto = p.id_proyecto
    WHERE dp.id_usuario = ?;
    '''
    UPDATE = "UPDATE usuarios SET nombres=?, apellidos=?, usuario=?, contrasena=? WHERE id_usuario=?"
    DELETE = "DELETE FROM usuarios WHERE id_usuario=?"
    BUSCAR = "SELECT * FROM usuarios WHERE nombres LIKE '%' || ? || '%' OR apellidos LIKE '%' || ? || '%'"


class ServicioDetalleProyecto:
    pass

class GestorDetalleProyecto:
    pass

class AvanceProyecto:
    def __init__(self, id_usuario, id_proyecto, mensaje):
        self.id_usuario = id_usuario
        self.id_proyecto = id_proyecto
        self.mensaje = mensaje

    def info(self):
        return self.id_usuario, self.id_proyecto, self.mensaje

class ConsultaAvanceProyecto:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS avances_proyecto (
        id_avance INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        id_proyecto INTEGER NOT NULL, 
        mensaje TEXT NOT NULL,
        FOREIGN KEY (id_usuario)  REFERENCES usuarios(id_usuario) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON UPDATE CASCADE ON DELETE CASCADE
    );
    '''

class ServicioAvanceProyecto:
    pass

class ImagenesMensaje:
    def __init__(self, id_avance, ubicacion):
        self.id_avance = id_avance
        self.ubicacion = ubicacion

    def info(self):
        return self.id_avance, self.ubicacion

class ConsultaImagenesMensaje:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS imagenes_mensaje (
        id_imagen INTEGER PRIMARY KEY AUTOINCREMENT,
        id_avance INTEGER NOT NULL,
        ubicacion TEXT NOT NULL,
        FOREIGN KEY (id_avance)  REFERENCES avances_proyecto(id_avance) ON UPDATE CASCADE ON DELETE CASCADE
    );
    '''

class ServicioImagenesMensaje:
    pass

class ManoObra:
    def __init__(self, nombre, telefono, ocupacion):
        self.nombre = nombre
        self.telefono = telefono
        self.ocupacion = ocupacion

    def info(self):
        return self.nombre, self.telefono, self.ocupacion

class ConsultaManoObra:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS mano_obra (
        id_trabajador INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        ocupacion TEXT
    );
    '''

class ServicioManoObra:
    pass

class DetalleManoObra:
    def __init__(self, id_proyecto, id_trabajador, costo_trabajo, tipo_trabajo):
        self.id_proyecto = id_proyecto
        self.id_trabajador = id_trabajador
        self.costo_trabajo = costo_trabajo
        self.tipo_trabajo = tipo_trabajo

    def info(self):
        return self.id_proyecto, self.id_trabajador, self.costo_trabajo, self.tipo_trabajo

class ConsultaDetalleManoObra:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS detalle_mano_obra (
        id_detalle_trabajo INTEGER PRIMARY KEY AUTOINCREMENT,
        id_proyecto INTEGER NOT NULL,
        id_trabajador INTEGER NOT NULL,
        costo_trabajo REAL NOT NULL CHECK(costo_trabajo >= 0),
        tipo_trabajo TEXT,
        FOREIGN KEY (id_proyecto)   REFERENCES proyecto(id_proyecto)    ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (id_trabajador) REFERENCES mano_obra(id_trabajador) ON UPDATE CASCADE ON DELETE RESTRICT,
        UNIQUE(id_proyecto, id_trabajador, tipo_trabajo)
    );
    '''

class ServicioDetalleManoObra:
    pass

class Material:
    def __init__(self, descripcion, unidad, prec_unitario):
        self.descripcion = descripcion
        self.unidad = unidad
        self.prec_unitario = prec_unitario

    def info(self):
        return self.descripcion, self.unidad, self.prec_unitario
'''
material = Material("Block", "unidad", 15)
print(material.info())
'''

class ConsultaMateriales:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS materiales (
        id_material INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        unidad TEXT,
        costo_unitario REAL CHECK(costo_unitario >= 0)
    );
    '''
    INSERT = "INSERT INTO materiales VALUES (NULL,?,?,?)"
    SELECT = "SELECT * FROM materiales"
    UPDATE = "UPDATE materiales SET descripcion=?, unidad=?, costo_unitario=? WHERE id_material=?"
    DELETE = "DELETE FROM materiales WHERE id_material="
    BUSCAR = "SELECT * FROM materiales WHERE descripcion LIKE '%' || ? || '%'"

class ServicioMateriales:
    @staticmethod
    def conexionBBDD():
        miConexion, miCursor = conectar()
        miCursor.execute(ConsultaMateriales.CREATE)
        miConexion.commit()
        miConexion.close()

    @staticmethod
    def consultar():
        miConexion, miCursor = conectar()
        miCursor.execute(ConsultaMateriales.SELECT)
        datos = miCursor.fetchall()
        miConexion.close()
        return datos

    @staticmethod
    def crear(descripcion, unidad, prec_unitario):
        miConexion, miCursor = conectar()
        material = Material(descripcion, unidad, prec_unitario)
        miCursor.execute(ConsultaMateriales.INSERT, material.info())
        miConexion.commit()
        miConexion.close()

    @staticmethod
    def actualizar(descripcion, unidad, prec_unitario, ide):
        miConexion, miCursor = conectar()
        miCursor.execute(
            ConsultaMateriales.UPDATE,
            (descripcion, unidad, prec_unitario, ide)
        )
        miConexion.commit()
        miConexion.close()

    @staticmethod
    def borrar(id_material):
        conexion = sqlite3.connect(db_name)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM materiales WHERE id_material = ?", (id_material,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(descripcion):
        miConexion, miCursor = conectar()
        miCursor.execute(ConsultaMateriales.BUSCAR, (descripcion,))
        datos = miCursor.fetchall()
        miConexion.close()
        return datos

class GestorMateriales:
    @staticmethod
    def conexionBBDD():
        try:
            ServicioMateriales.conexionBBDD()
            messagebox.showinfo("CONEXIÓN", "Base de datos conectada exitosamente")
        except:
            messagebox.showerror("ERROR", "Error al conectar la base de datos")

    @staticmethod
    def mostrar(tree):
        # limpiar tabla
        for elemento in tree.get_children():
            tree.delete(elemento)

        try:
            materiales = ServicioMateriales.consultar()
            for row in materiales:
                tree.insert(
                    "",
                    "end",
                    text=row[0],
                    values=(row[1], row[2], row[3])
                )
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

    @staticmethod
    def buscar(tree, criterio):
        registros = tree.get_children()
        [tree.delete(elemento) for elemento in registros]
        try:
            if criterio != "":
                materiales = ServicioMateriales.buscar(criterio)
                [tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3])) for row in materiales]
            else:
                messagebox.showwarning("ERROR", "No ha escrito un criterio de búsqueda")
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

    @staticmethod
    def crear(descripcion, unidad, prec_unitario):
        try:
            if (descripcion != "" and unidad != "" and prec_unitario != ""):
                ServicioMateriales.crear(descripcion, unidad, prec_unitario)
            else:
                messagebox.showwarning("ADVERTENCIA", "Por favor llene todos los campos")
        except:
            messagebox.showerror("ERROR", "Error al crear")

    @staticmethod
    def actualizar(descripcion, unidad, prec_unitario, ide):
        try:
            if (descripcion != "" and unidad != "" and prec_unitario != ""):
                ServicioMateriales.actualizar(descripcion, unidad, prec_unitario, ide)
            else:
                messagebox.showwarning("ADVERTENCIA", "Por favor llene todos los campos")
        except:
            messagebox.showerror("ERROR", "Error al actualizar")

    @staticmethod
    def borrar(ide):
            if messagebox.askyesno(message="¿Seguro desea eliminar el registro?", title="ADVERTENCIA"):
                ServicioMateriales.borrar(ide)
            else:
                messagebox.showerror("Error", "Error al eliminar")

    @staticmethod
    def mensaje():
        messagebox.showinfo("INFORMACIÓN", "Aplicación 21 Design"
                                           "Versión 1.0"
                                           "Tecnología Python Tkinter")

class DetalleMateriales:
    def __init__(self, id_proyecto, id_material, cantidad, costo_total):
        self.id_proyecto = id_proyecto
        self.id_material = id_material
        self.cantidad = cantidad
        self.costo_total = costo_total

    def info(self):
        return self.id_proyecto, self.id_material, self.cantidad, self.costo_total

class ConsultaDetalleMateriales:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS detalle_materiales (
        id_detalle_material INTEGER PRIMARY KEY AUTOINCREMENT,
        id_proyecto INTEGER NOT NULL,
        id_material INTEGER NOT NULL,
        cantidad REAL NOT NULL CHECK(cantidad >= 0),
        costo_total REAL CHECK(costo_total >= 0),
        FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (id_material) REFERENCES materiales(id_material) ON UPDATE CASCADE ON DELETE RESTRICT,
        UNIQUE(id_proyecto, id_material)
    );
    '''

class ServicioDetalleMateriales:
    pass

class Administracion:
    def __init__(self, tipo_gasto, fecha, forma_pago, proveedor, costo, id_proyecto):
        self.tipo_gasto = tipo_gasto
        self.fecha = fecha
        self.forma_pago = forma_pago
        self.proveedor = proveedor
        self.costo = costo
        self.id_proyecto = id_proyecto

    def info(self):
        return self.tipo_gasto, self.fecha, self.forma_pago, self.proveedor, self.costo, self.id_proyecto

class ConsultaAdministracion:
    CREATE = '''
    CREATE TABLE IF NOT EXISTS administracion (
        id_administracion INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_gasto TEXT NOT NULL,
        fecha TEXT,
        forma_pago TEXT CHECK(forma_pago IN ('efectivo','tarjeta','transferencia','cheque','otro')),
        proveedor TEXT,
        costo REAL NOT NULL CHECK(costo >= 0),
        id_proyecto INTEGER NOT NULL,
        FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON UPDATE CASCADE ON DELETE CASCADE
    );
    '''

class ServicioAdministracion:
    pass