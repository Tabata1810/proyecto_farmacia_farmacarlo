from database import conectar
from models.producto import Producto


class Inventario:
    """
    Clase que gestiona el inventario.
    Utiliza diferentes colecciones:
    - Lista para devolver productos
    - Diccionario para acceso rápido por ID
    - Conjunto para garantizar IDs únicos
    """

    def agregar_producto(self, nombre, cantidad, precio):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
            (nombre, cantidad, precio)
        )

        conexion.commit()
        conexion.close()

    def obtener_productos(self):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()

        # ===== Colecciones =====
        productos_lista = []     # Lista
        productos_dict = {}      # Diccionario
        ids_unicos = set()       # Conjunto

        for fila in filas:
            producto = Producto(
                fila["id"],
                fila["nombre"],
                fila["cantidad"],
                fila["precio"]
            )

            productos_lista.append(producto)
            productos_dict[fila["id"]] = producto
            ids_unicos.add(fila["id"])

        conexion.close()

        return productos_lista

    def eliminar_producto(self, id):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))

        conexion.commit()
        conexion.close()

    def actualizar_producto(self, id, nombre, cantidad, precio):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = ?, cantidad = ?, precio = ?
            WHERE id = ?
        """, (nombre, cantidad, precio, id))

        conexion.commit()
        conexion.close()

    def buscar_producto(self, nombre):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM productos WHERE nombre LIKE ?",
            ('%' + nombre + '%',)
        )

        filas = cursor.fetchall()
        productos = []

        for fila in filas:
            producto = Producto(
                fila["id"],
                fila["nombre"],
                fila["cantidad"],
                fila["precio"]
            )
            productos.append(producto)

        conexion.close()
        return productos