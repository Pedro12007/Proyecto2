import sqlite3
from tkinter import messagebox

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

class Consulta:
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

class Servicio:
    @staticmethod
    def conectar():
        miConexion = sqlite3.connect("21design.db")
        miCursor = miConexion.cursor()
        return miConexion, miCursor

    @staticmethod
    def conexionBBDD():
        miConexion, miCursor = Servicio.conectar()
        miCursor.execute(Consulta.CREATE)
        miConexion.commit()
        miConexion.close()

    @staticmethod
    def consultar():
        miConexion, miCursor = Servicio.conectar()
        miCursor.execute(Consulta.SELECT)
        datos = miCursor.fetchall()
        miConexion.close()
        return datos

    @staticmethod
    def crear(descripcion, unidad, prec_unitario):
        miConexion, miCursor = Servicio.conectar()
        material = Material(descripcion, unidad, prec_unitario)
        miCursor.execute(Consulta.INSERT, material.info())
        miConexion.commit()
        miConexion.close()

    @staticmethod
    def actualizar(descripcion, unidad, prec_unitario, ide):
        miConexion, miCursor = Servicio.conectar()
        miCursor.execute(
            Consulta.UPDATE,
            (descripcion, unidad, prec_unitario, ide)
        )
        miConexion.commit()
        miConexion.close()

    @staticmethod
    def borrar(id_material):
        conexion = sqlite3.connect("21design.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM materiales WHERE id_material = ?", (id_material,))
        conexion.commit()
        conexion.close()

    @staticmethod
    def buscar(descripcion):
        miConexion, miCursor = Servicio.conectar()
        miCursor.execute(Consulta.BUSCAR, (descripcion,))
        datos = miCursor.fetchall()
        miConexion.close()
        return datos

class Gestor:

    @staticmethod
    def conexionBBDD():
        try:
            Servicio.conexionBBDD()
            messagebox.showinfo("CONEXION", "Base de datos conectada exitosamente")
        except:
            messagebox.showerror("ERROR", "Error al conectar la base de datos")

    @staticmethod
    def mostrar(tree):
        # limpiar tabla
        for elemento in tree.get_children():
            tree.delete(elemento)

        try:
            materiales = Servicio.consultar()
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
            if(criterio != ""):
                materiales = Servicio.buscar(criterio)
                [tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3])) for row in materiales]
            else:
                messagebox.showwarning("ERROR", "No ha escrito un criterio de búsqueda")
        except:
            messagebox.showinfo("ADVERTENCIA", "Error al mostrar")

    @staticmethod
    def crear(descripcion, unidad, prec_unitario):
        try:
            if (descripcion != "" and unidad != "" and prec_unitario != ""):
                Servicio.crear(descripcion, unidad, prec_unitario)
            else:
                messagebox.showwarning("ADVERTENCIA", "Por favor llene todos los campos")
        except:
            messagebox.showerror("ERROR", "Error al crear")

    @staticmethod
    def actualizar(descripcion, unidad, prec_unitario, ide):
        try:
            if (descripcion != "" and unidad != "" and prec_unitario != ""):
                Servicio.actualizar(descripcion, unidad, prec_unitario, ide)
            else:
                messagebox.showwarning("ADVERTENCIA", "Por favor llene todos los campos")
        except:
            messagebox.showerror("ERROR", "Error al actualizar")

    @staticmethod
    def borrar(ide):
            if messagebox.askyesno(message="¿Seguro desea eliminar el registro?", title="ADVERTENCIA"):
                Servicio.borrar(ide)
            else:
                messagebox.showerror("Error", "Error al eliminar")

    @staticmethod
    def mensaje():
        messagebox.showinfo("INFORMACIÓN", "Aplicación 21 Design"
                                           "Versión 1.0"
                                           "Tecnología Python Tkinter")
