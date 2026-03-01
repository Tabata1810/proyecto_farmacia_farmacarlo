class Producto:
    """
    Clase que representa un producto del inventario.
    Se aplica encapsulamiento usando atributos privados.
    """

    def __init__(self, id, nombre, cantidad, precio):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # ===== Getters =====

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # ===== Setters =====

    def set_nombre(self, nombre):
        self._nombre = nombre

    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def set_precio(self, precio):
        self._precio = precio

    # ===== Uso de Tupla (colección) =====
    def to_tuple(self):
        """
        Se utiliza una tupla para representar el producto
        de forma inmutable.
        """
        return (self._id, self._nombre, self._cantidad, self._precio)