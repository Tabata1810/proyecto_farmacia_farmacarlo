class Producto:
    """
    Clase que representa un producto del inventario.
    Se aplica encapsulamiento usando atributos privados.
    """

    def __init__(self, id, nombre, cantidad, precio, id_categoria=None, id_proveedor=None):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
        self._id_categoria = id_categoria
        self._id_proveedor = id_proveedor

    # ===== Getters =====

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio
    
    def get_id_categoria(self):
        return self._id_categoria
    
    def get_id_proveedor(self):
        return self._id_proveedor

    # ===== Setters =====

    def set_nombre(self, nombre):
        self._nombre = nombre

    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def set_precio(self, precio):
        self._precio = precio

    def set_id_categoria(self, id_categoria):
        self._id_categoria = id_categoria

    def set_id_proveedor(self, id_proveedor):
        self._id_proveedor = id_proveedor

    # ===== Uso de Tupla (colección) =====
    def to_tuple(self):
        """
        Representación del producto en formato de tupla para persistencia.
        """
        return (self._id, self._nombre, self._cantidad, self._precio, self._id_categoria, self._id_proveedor)