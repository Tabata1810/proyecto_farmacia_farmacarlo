from Conexion.conexion import obtener_conexion

class ProductoService:
    @staticmethod
    def listar_todos():
        db = obtener_conexion()
        if db:
            cursor = db.cursor(dictionary=True)
            query = """
                SELECT p.id AS id_producto, p.nombre, p.cantidad, p.precio, 
                       c.nombre_categoria
                FROM productos_mysql p
                LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            db.close()
            return resultados
        return []

    @staticmethod
    def insertar(nombre, cantidad, precio, id_cat, id_prov):
        db = obtener_conexion()
        if db:
            cursor = db.cursor()
            query = """
                INSERT INTO productos_mysql (nombre, cantidad, precio, id_categoria) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, int(cantidad), float(precio), id_cat))
            db.commit()
            cursor.close()
            db.close()
            return True
        return False

    @staticmethod
    def eliminar(id_producto):
        db = obtener_conexion()
        if db:
            cursor = db.cursor()
            query = "DELETE FROM productos_mysql WHERE id = %s"
            cursor.execute(query, (id_producto,))
            db.commit()
            cursor.close()
            db.close()
            return True
        return False

    @staticmethod
    def actualizar(id_producto, nombre, cantidad, precio, id_cat, id_prov):
        db = obtener_conexion()
        if db:
            cursor = db.cursor()
            query = """
                UPDATE productos_mysql 
                SET nombre=%s, cantidad=%s, precio=%s, id_categoria=%s 
                WHERE id=%s
            """
            cursor.execute(query, (nombre, int(cantidad), float(precio), id_cat, id_producto))
            db.commit()
            cursor.close()
            db.close()
            return True
        return False