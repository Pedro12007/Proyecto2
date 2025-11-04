import sqlite3

DB_NAME = "21design.db"

SCHEMA = r"""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT,
    mail TEXT,
    datos_referencia TEXT,
    direccion TEXT
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    usuario TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL
);

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

CREATE TABLE IF NOT EXISTS detalle_proyecto (
    id_detalle_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_proyecto INTEGER NOT NULL,
    UNIQUE(id_usuario, id_proyecto),
    FOREIGN KEY (id_usuario)  REFERENCES usuarios(id_usuario)  ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id_proyecto) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS mano_obra (
    id_trabajador INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    ocupacion TEXT
);

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

CREATE TABLE IF NOT EXISTS materiales (
    id_material INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    unidad TEXT,
    costo_unitario REAL CHECK(costo_unitario >= 0)
);

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
"""

def create_db():
    con = sqlite3.connect(DB_NAME)
    con.executescript(SCHEMA)
    con.commit()
    con.close()
    print(f"Base '{DB_NAME}' creada con éxito.")