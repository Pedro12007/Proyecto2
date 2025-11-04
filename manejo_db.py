import sqlite3
from tkinter import messagebox

db_name = '21design.db'

def conectar():
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    return conexion, cursor

def validar_campo_lleno(entrada):
    return entrada.strip() != ''

def validar_numero(entrada):
    return entrada.isdigit()

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
    INSERT = "INSERT INTO clientes VALUES (NULL,?,?,?,?,?,?)"
    SELECT = "SELECT * FROM clientes"
    UPDATE = "UPDATE clientes SET nombre=?, apellido=?, telefono=?, mail=?, datos_referencia=?, direccion=? WHERE id_cliente=?"
    DELETE = "DELETE FROM clientes WHERE id_cliente=?"
    BUSCAR = "SELECT * FROM clientes WHERE nombre LIKE '%' || ? || '%' OR apellido LIKE '%' || ? || '%'"

class ServicioClientes:
    @staticmethod
    def conexionBBDD():
        conexion, cursor = conectar()
        cursor.execute(ConsultaClientes.CREATE)
        conexion.commit()
        conexion.close()

    @staticmethod
    def consultar():
        conexion, cursor = conectar()
        cursor.execute(ConsultaClientes.SELECT)
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def crear(nombre, apellido, telefono, mail, datos_referencia, direccion):
        conexion, cursor = conectar()
        cliente = Cliente(nombre, apellido, telefono, mail, datos_referencia, direccion)
        cursor.execute(ConsultaClientes.INSERT, cliente.info())
        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()
        return nuevo_id

    @staticmethod
    def actualizar(nombre, apellido, telefono, mail, datos_referencia, direccion, ide):
        conexion, cursor = conectar()
        cursor.execute(ConsultaClientes.UPDATE, (nombre, apellido, telefono, mail, datos_referencia, direccion, ide))
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar(id_cliente):
        conexion = sqlite3.connect(db_name)
        cursor = conexion.cursor()
        cursor.execute(ConsultaClientes.DELETE, (id_cliente,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(criterio):
        conexion, cursor = conectar()
        cursor.execute(ConsultaClientes.BUSCAR, (criterio, criterio))
        datos = cursor.fetchall()
        conexion.close()
        return datos

class GestorClientes:
    @staticmethod
    def mostrar(tree):
        # limpiar tabla
        for elemento in tree.get_children():
            tree.delete(elemento)

        try:
            usuarios = ServicioClientes.consultar()
            for row in usuarios:
                tree.insert(
                    "",
                    "end",
                    text=row[0],
                    iid=row[0],
                    values=(row[1], row[2], row[3], row[4], row[5], row[6])
                )
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

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
    BUSCAR_BY_ID = 'SELECT * FROM usuarios WHERE id_usuario=?'
    BUSCAR_USUARIO = 'SELECT * FROM usuarios WHERE usuario=? AND contrasena=?'

class ServicioUsuarios:
    @staticmethod
    def conexionBBDD():
        conexion, cursor = conectar()
        cursor.execute(ConsultaUsuarios.CREATE)
        conexion.commit()
        conexion.close()

    @staticmethod
    def consultar():
        conexion, cursor = conectar()
        cursor.execute(ConsultaUsuarios.SELECT)
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def crear(nombres, apellidos, usuario_a, contrasena):
        conexion, cursor = conectar()
        usuario = Usuario(nombres, apellidos, usuario_a, contrasena)
        cursor.execute(ConsultaUsuarios.INSERT, usuario.info())
        conexion.commit()
        conexion.close()

    @staticmethod
    def actualizar(nombres, apellidos, usuario_a, contrasena, ide):
        conexion, cursor = conectar()
        cursor.execute(ConsultaUsuarios.UPDATE, (nombres, apellidos, usuario_a, contrasena, ide))
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar(id_usuario):
        conexion, cursor = conectar()
        cursor.execute(ConsultaUsuarios.DELETE, (id_usuario,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_id(id_usuario):
        conexion, cursor = conectar()
        cursor.execute(ConsultaUsuarios.BUSCAR_BY_ID, (id_usuario,))
        datos = cursor.fetchone()
        conexion.close()
        return datos

    @staticmethod
    def buscar_usuario_password(nombre_usuario, contrasena):
        conexion, cursor = conectar()
        cursor.execute(ConsultaUsuarios.BUSCAR_USUARIO, (nombre_usuario, contrasena))
        datos = cursor.fetchone()
        conexion.close()
        return datos

class GestorUsuarios:
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
                    iid=row[0],
                    text=row[0],
                    values=(row[1], row[2], row[3])
                )
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
    UPDATE = "UPDATE proyecto SET nombre=?, descripcion=?, n_usuarios=?, fecha_inicio=?, duracion=?, fecha_fin=?, estado=?, presupuesto_total=? WHERE id_proyecto=?"
    DELETE = "DELETE FROM proyecto WHERE id_proyecto=?"
    BUSCAR = "SELECT * FROM proyecto WHERE nombre LIKE '%' || ? || '%'"
    SELECT_BY_ESTADO = "SELECT * FROM proyecto WHERE estado=?"
    SELECT_BY_ID = "SELECT * FROM proyecto WHERE id_proyecto=?"

class ServicioProyecto:
    @staticmethod
    def conexionBBDD():
        conexion, cursor = conectar()
        cursor.execute(ConsultaProyecto.CREATE)
        conexion.commit()
        conexion.close()

    @staticmethod
    def consultar():
        conexion, cursor = conectar()
        cursor.execute(ConsultaProyecto.SELECT)
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def crear(nombre, descripcion, n_usuarios, fecha_inicio, duracion, fecha_fin, estado, presupuesto_total, id_cliente):
        conexion, cursor = conectar()
        proyecto = Proyecto(nombre, descripcion, n_usuarios, fecha_inicio, duracion, fecha_fin, estado, presupuesto_total, id_cliente)
        cursor.execute(ConsultaProyecto.INSERT, proyecto.info())
        conexion.commit()
        id_proyecto = cursor.lastrowid
        conexion.close()
        return id_proyecto

    @staticmethod
    def actualizar(nombre, descripcion, n_usuarios, fecha_inicio, duracion, fecha_fin, estado, presupuesto_total, ide):
        conexion, cursor = conectar()
        cursor.execute(ConsultaProyecto.UPDATE, (nombre, descripcion, n_usuarios, fecha_inicio, duracion, fecha_fin, estado, presupuesto_total, ide))
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar(id_proyecto):
        conexion = sqlite3.connect(db_name)
        cursor = conexion.cursor()
        cursor.execute(ConsultaProyecto.DELETE, (id_proyecto,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(criterio):
        conexion, cursor = conectar()
        cursor.execute(ConsultaProyecto.BUSCAR, (criterio,))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def buscar_por_estado(estado):
        conexion, cursor = conectar()
        cursor.execute(ConsultaProyecto.SELECT_BY_ESTADO, (estado,))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def buscar_por_id(ide):
        conexion, cursor = conectar()
        cursor.execute(ConsultaProyecto.SELECT_BY_ID, (ide,))
        datos = cursor.fetchone()
        conexion.close()
        return datos

    @staticmethod
    def calcular_presupuesto_total(id_proyecto):
        total_materiales = ServicioDetalleMateriales.obtener_costo_total_materiales(id_proyecto)
        total_mano_obra = ServicioDetalleManoObra.obtener_costo_total_mano_obra(id_proyecto)
        total_admin = ServicioAdministracion.obtener_costo_total_administracion(id_proyecto)

        presupuesto_total = total_materiales + total_mano_obra + total_admin
        return presupuesto_total

class GestorProyectos:
    @staticmethod
    def mostrar(tree, id_usuario=None):
        # limpiar tabla
        for elemento in tree.get_children():
            tree.delete(elemento)

        try:
            if id_usuario is not None:
                proyectos = ServicioDetalleProyecto.consultar(id_usuario)

                for row in proyectos:
                    tree.insert(
                        "",
                        "end",
                        text=row[0],
                        values=(row[1], row[2], row[7], row[4], row[6])
                    )
            else:
                proyectos = ServicioProyecto.consultar()
                for row in proyectos:
                    tree.insert(
                        "",
                        "end",
                        text=row[0],
                        values=(row[1], row[2], row[7], row[4], row[6])
                    )
        except Exception as e:
            messagebox.showinfo("ADVERTENCIA", f"Error al mostrar proyectos: {e}")

    @staticmethod
    def crear(nombre, descripcion, n_usuarios, fecha_inicio, duracion, fecha_fin,
              estado, presupuesto_total, id_cliente, id_usuario_para_detalle=None):
        try:
            if nombre != "":
                id_proyecto = ServicioProyecto.crear(
                    nombre,
                    descripcion,
                    n_usuarios,
                    fecha_inicio,
                    duracion,
                    fecha_fin,
                    estado,
                    presupuesto_total,
                    id_cliente
                )

                if id_usuario_para_detalle is not None:
                    ServicioDetalleProyecto.crear(id_usuario_para_detalle, id_proyecto)
                return id_proyecto
            else:
                messagebox.showwarning("ADVERTENCIA", "El nombre del proyecto es obligatorio.")
        except Exception as e:
            messagebox.showerror("ERROR", f"Error al crear proyecto: {e}")

    @staticmethod
    def actualizar(ide, nombre, descripcion, n_usuarios, fecha_inicio, duracion,
                   fecha_fin, estado, presupuesto_total, id_cliente):
        try:
            if nombre != "":
                ServicioProyecto.actualizar(
                    nombre,
                    descripcion,
                    n_usuarios,
                    fecha_inicio,
                    duracion,
                    fecha_fin,
                    estado,
                    presupuesto_total,
                    id_cliente,
                    ide
                )
            else:
                messagebox.showwarning("ADVERTENCIA", "El nombre del proyecto es obligatorio.")
        except Exception as e:
            messagebox.showerror("ERROR", f"Error al actualizar proyecto: {e}")

    @staticmethod
    def borrar(ide):
        try:
            if messagebox.askyesno(message="¿Seguro desea eliminar el proyecto?", title="ADVERTENCIA"):
                # esto también borra en cascada detalle_proyecto por tu FK
                ServicioProyecto.borrar(ide)
        except Exception as e:
            messagebox.showerror("ERROR", f"Error al eliminar proyecto: {e}")


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
    SELECT p.*
    FROM detalle_proyecto dp
    INNER JOIN proyecto p ON dp.id_proyecto = p.id_proyecto
    WHERE dp.id_usuario = ?;
    '''
    DELETE = 'DELETE FROM detalle_proyecto WHERE id_proyecto = ?;'

class ServicioDetalleProyecto:
    @staticmethod
    def conexionBBDD():
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleProyecto.CREATE)
        conexion.commit()
        conexion.close()

    @staticmethod
    def consultar(id_usuario):
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleProyecto.SELECT, (id_usuario,))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def crear(id_usuario, id_proyecto):
        conexion, cursor = conectar()
        detalle = DetalleProyecto(id_usuario, id_proyecto)
        cursor.execute(ConsultaDetalleProyecto.INSERT, detalle.info())
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar(id_proyecto):
        conexion = sqlite3.connect(db_name)
        cursor = conexion.cursor()
        cursor.execute(ConsultaDetalleProyecto.DELETE, (id_proyecto,))
        conexion.commit()
        conexion.close()

class GestorDetalleProyecto:
    @staticmethod
    def mostrar(tree, id_usuario):
        # limpiar tabla
        for elemento in tree.get_children():
            tree.delete(elemento)

        try:
            proyectos = ServicioDetalleProyecto.consultar(id_usuario)
            for row in proyectos:
                tree.insert(
                    "",
                    "end",
                    text=row[0],
                    iid=row[0],
                    values=(row[1], row[2], row[7], row[4], row[6])
                    # 1- nombre | 2- descripcion | 7- estado | 4- fecha_inicio | 6- fecha_fin
                )
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

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
    INSERT = "INSERT INTO mano_obra VALUES (NULL,?,?,?)"
    SELECT = "SELECT * FROM mano_obra"
    UPDATE = "UPDATE mano_obra SET nombre=?, telefono=?, ocupacion=? WHERE id_trabajador=?"
    DELETE = "DELETE FROM mano_obra WHERE id_trabajador=?"
    BUSCAR = "SELECT * FROM mano_obra WHERE nombre LIKE '%' || ? || '%' OR ocupacion LIKE '%' || ? || '%'"

class ServicioManoObra:
    @staticmethod
    def conexionBBDD():
        conexion, cursor = conectar()
        cursor.execute(ConsultaManoObra.CREATE)
        conexion.commit()
        conexion.close()

    @staticmethod
    def consultar():
        conexion, cursor = conectar()
        cursor.execute(ConsultaManoObra.SELECT)
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def crear(nombre, telefono, ocupacion):
        conexion, cursor = conectar()
        trabajador = ManoObra(nombre, telefono, ocupacion)
        cursor.execute(ConsultaManoObra.INSERT, trabajador.info())
        conexion.commit()
        conexion.close()

    @staticmethod
    def actualizar(nombre, telefono, ocupacion, ide):
        conexion, cursor = conectar()
        cursor.execute(ConsultaManoObra.UPDATE, (nombre, telefono, ocupacion, ide))
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar(id_trabajador):
        conexion, cursor = conectar()
        cursor.execute(ConsultaManoObra.DELETE, (id_trabajador,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(criterio):
        conexion, cursor = conectar()
        cursor.execute(ConsultaManoObra.BUSCAR, (criterio, criterio))
        datos = cursor.fetchall()
        conexion.close()
        return datos

class GestorManoObra:
    @staticmethod
    def mostrar(tree):
        # limpiar tabla
        for elemento in tree.get_children():
            tree.delete(elemento)

        try:
            trabajadores = ServicioManoObra.consultar()
            for row in trabajadores:
                tree.insert(
                    "",
                    "end",
                    text=row[0],
                    values=(row[1], row[2], row[3])
                )
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

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
    INSERT = "INSERT INTO detalle_mano_obra VALUES (NULL,?,?,?,?)"
    SELECT = '''
    SELECT d.id_detalle_trabajo, m.nombre, m.ocupacion, d.tipo_trabajo, d.costo_trabajo
    FROM detalle_mano_obra d
    INNER JOIN mano_obra m ON d.id_trabajador = m.id_trabajador
    WHERE d.id_proyecto = ?;
    '''
    UPDATE = "UPDATE detalle_mano_obra SET costo_trabajo=?, tipo_trabajo=? WHERE id_detalle_trabajo=?"
    DELETE = "DELETE FROM detalle_mano_obra WHERE id_detalle_trabajo=?"
    COSTO_TOTAL = '''
    SELECT IFNULL(SUM(costo_trabajo), 0) 
    FROM detalle_mano_obra 
    WHERE id_proyecto = ?
    '''

class ServicioDetalleManoObra:
    @staticmethod
    def conexionBBDD():
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleManoObra.CREATE)
        conexion.commit()
        conexion.close()

    @staticmethod
    def crear(id_proyecto, id_trabajador, costo_trabajo, tipo_trabajo):
        conexion, cursor = conectar()
        detalle = DetalleManoObra(id_proyecto, id_trabajador, costo_trabajo, tipo_trabajo)
        cursor.execute(ConsultaDetalleManoObra.INSERT, detalle.info())
        conexion.commit()
        conexion.close()

    @staticmethod
    def consultar(id_proyecto):
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleManoObra.SELECT, (id_proyecto,))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def actualizar(costo_trabajo, tipo_trabajo, ide):
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleManoObra.UPDATE, (costo_trabajo, tipo_trabajo, ide))
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar(id_detalle):
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleManoObra.DELETE, (id_detalle,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_costo_total_mano_obra(id_proyecto):
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleManoObra.COSTO_TOTAL, (id_proyecto,))
        total = cursor.fetchone()[0]
        conexion.close()
        return total

class GestorDetalleManoObra:
    @staticmethod
    def mostrar(tree, id_proyecto):
        # limpiar tabla
        for elemento in tree.get_children():
            tree.delete(elemento)

        try:
            trabajadores = ServicioDetalleManoObra.consultar(id_proyecto)
            for row in trabajadores:
                tree.insert(
                    "",
                    "end",
                    text=row[0],
                    values=(row[1], row[2], row[3], row[4])
                )
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

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
    DELETE = "DELETE FROM materiales WHERE id_material=?"
    BUSCAR = "SELECT * FROM materiales WHERE descripcion LIKE '%' || ? || '%'"
    BUSCAR_BY_ID = 'SELECT * FROM materiales WHERE id_material = ?'

class ServicioMateriales:
    @staticmethod
    def conexionBBDD():
        conexion, cursor = conectar()
        cursor.execute(ConsultaMateriales.CREATE)
        conexion.commit()
        conexion.close()

    @staticmethod
    def consultar():
        conexion, cursor = conectar()
        cursor.execute(ConsultaMateriales.SELECT)
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def crear(descripcion, unidad, prec_unitario):
        conexion, cursor = conectar()
        material = Material(descripcion, unidad, prec_unitario)
        cursor.execute(ConsultaMateriales.INSERT, material.info())
        conexion.commit()
        conexion.close()

    @staticmethod
    def actualizar(descripcion, unidad, prec_unitario, ide):
        conexion, cursor = conectar()
        cursor.execute(
            ConsultaMateriales.UPDATE,
            (descripcion, unidad, prec_unitario, ide)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar(id_material):
        conexion, cursor = conectar()
        cursor.execute(ConsultaMateriales.DELETE, (id_material,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(descripcion):
        conexion, cursor = conectar()
        cursor.execute(ConsultaMateriales.BUSCAR, (descripcion,))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def buscar_por_id(ide):
        conexion, cursor = conectar()
        cursor.execute(ConsultaMateriales.BUSCAR_BY_ID, (ide,))
        datos = cursor.fetchone()
        conexion.close()
        return datos

class GestorMateriales:
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
                    iid=row[0],
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
            if descripcion != "" and unidad != "" and prec_unitario != "":
                ServicioMateriales.crear(descripcion, unidad, prec_unitario)
            else:
                messagebox.showwarning("ADVERTENCIA", "Por favor llene todos los campos")
        except:
            messagebox.showerror("ERROR", "Error al crear")

    @staticmethod
    def actualizar(descripcion, unidad, prec_unitario, ide):
        try:
            if descripcion != "" and unidad != "" and prec_unitario != "":
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
    INSERT = "INSERT INTO detalle_materiales VALUES (NULL,?,?,?,?)"
    SELECT = '''
    SELECT m.id_material, m.descripcion, m.unidad, m.costo_unitario, IFNULL(d.cantidad, 0) AS cantidad_en_proyecto, IFNULL(d.costo_total, 0) AS costo_total
    FROM materiales m
    LEFT JOIN detalle_materiales d 
        ON m.id_material = d.id_material
        AND d.id_proyecto = ?;
    '''
    UPDATE = "UPDATE detalle_materiales SET cantidad=?, costo_total=? WHERE id_proyecto = ? and id_material = ?"
    DELETE = "DELETE FROM detalle_materiales WHERE id_proyecto = ? and id_material = ?"
    SELECT_BY_ID = 'SELECT cantidad FROM detalle_materiales WHERE id_proyecto = ? and id_material = ?'
    COSTO = """
    SELECT IFNULL(SUM(costo_total), 0) 
    FROM detalle_materiales 
    WHERE id_proyecto = ?
    """

class ServicioDetalleMateriales:
    @staticmethod
    def conexionBBDD():
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleMateriales.CREATE)
        conexion.commit()
        conexion.close()

    @staticmethod
    def crear(id_proyecto, id_material, cantidad, costo_total):
        conexion, cursor = conectar()
        detalle = DetalleMateriales(id_proyecto, id_material, cantidad, costo_total)
        cursor.execute(ConsultaDetalleMateriales.INSERT, detalle.info())
        conexion.commit()
        conexion.close()

    @staticmethod
    def consultar(id_proyecto):
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleMateriales.SELECT, (id_proyecto,))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def actualizar(cantidad, costo_total, id_proyecto, id_material):
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleMateriales.UPDATE, (cantidad, costo_total, id_proyecto, id_material))
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar(id_proyecto, id_material):
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleMateriales.DELETE, (id_proyecto, id_material))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar_por_id(id_proyecto, id_material):
        conexion, cursor = conectar()
        cursor.execute(ConsultaDetalleMateriales.SELECT_BY_ID, (id_proyecto, id_material))
        datos = cursor.fetchone()  # Obtener el resultado
        conexion.close()
        return datos

    @staticmethod
    def obtener_costo_total_materiales(id_proyecto):
        conexion, cursor = conectar()
        cursor.execute("""
            SELECT IFNULL(SUM(costo_total), 0) 
            FROM detalle_materiales 
            WHERE id_proyecto = ?
        """, (id_proyecto,))
        total = cursor.fetchone()[0]
        conexion.close()
        return total

class GestorDetalleMateriales:
    @staticmethod
    def mostrar(tree, id_proyecto):
        # limpiar tabla
        for elemento in tree.get_children():
            tree.delete(elemento)

        try:
            materiales = ServicioDetalleMateriales.consultar(id_proyecto)
            for row in materiales:
                tree.insert(
                    "",
                    "end",
                    text=row[0],
                    iid=row[0],
                    values=(row[1], row[2], row[3],row[4], row[5])
                )
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

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
    INSERT = "INSERT INTO administracion VALUES (NULL,?,?,?,?,?,?)"
    SELECT = "SELECT * FROM administracion WHERE id_proyecto=?"
    UPDATE = "UPDATE administracion SET tipo_gasto=?, fecha=?, forma_pago=?, proveedor=?, costo=?, id_proyecto=? WHERE id_administracion=?"
    DELETE = "DELETE FROM administracion WHERE id_administracion=?"
    BUSCAR = "SELECT * FROM administracion WHERE tipo_gasto LIKE '%' || ? || '%' OR proveedor LIKE '%' || ? || '%'"
    COSTO_TOTAL = '''
    SELECT IFNULL(SUM(costo), 0) 
    FROM administracion 
    WHERE id_proyecto = ?
    '''

class ServicioAdministracion:
    @staticmethod
    def conexionBBDD():
        conexion, cursor = conectar()
        cursor.execute(ConsultaAdministracion.CREATE)
        conexion.commit()
        conexion.close()

    @staticmethod
    def crear(tipo_gasto, fecha, forma_pago, proveedor, costo, id_proyecto):
        conexion, cursor = conectar()
        administracion = Administracion(tipo_gasto, fecha, forma_pago, proveedor, costo, id_proyecto)
        cursor.execute(ConsultaAdministracion.INSERT, administracion.info())
        conexion.commit()
        conexion.close()

    @staticmethod
    def consultar(id_proyecto):
        conexion, cursor = conectar()
        cursor.execute(ConsultaAdministracion.SELECT, (id_proyecto,))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def actualizar(tipo_gasto, fecha, forma_pago, proveedor, costo, id_proyecto, ide):
        conexion, cursor = conectar()
        cursor.execute(ConsultaAdministracion.UPDATE,
                         (tipo_gasto, fecha, forma_pago, proveedor, costo, id_proyecto, ide))
        conexion.commit()
        conexion.close()

    @staticmethod
    def borrar(id_administracion):
        conexion = sqlite3.connect(db_name)
        cursor = conexion.cursor()
        cursor.execute(ConsultaAdministracion.DELETE, (id_administracion,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(criterio):
        conexion, cursor = conectar()
        cursor.execute(ConsultaAdministracion.BUSCAR, (criterio, criterio))
        datos = cursor.fetchall()
        conexion.close()
        return datos

    @staticmethod
    def obtener_costo_total_administracion(id_proyecto):
        conexion, cursor = conectar()
        cursor.execute(ConsultaAdministracion.COSTO_TOTAL, (id_proyecto,))
        total = cursor.fetchone()[0]
        conexion.close()
        return total