class ProductoForm:
    def __init__(self, nombre, cantidad, precio, id_categoria=None, id_proveedor=None):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.id_categoria = id_categoria
        self.id_proveedor = id_proveedor

    def validar(self):
        """
        Verificación de integridad de datos del formulario
        """
        try:
            # Comprobar campos obligatorios
            if not self.nombre or len(self.nombre.strip()) == 0:
                return False
            
            # Validación de rangos numéricos
            if float(self.precio) <= 0 or int(self.cantidad) < 0:
                return False
            
            # Validar que se haya seleccionado categoría y proveedor (opcional pero recomendado)
            if not self.id_categoria or not self.id_proveedor:
                return False
                
            return True
        except (ValueError, TypeError):
            return False