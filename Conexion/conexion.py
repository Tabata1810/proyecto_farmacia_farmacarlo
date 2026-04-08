import mysql.connector

# Definición de la función para establecer la conexión con el servidor MySQL
def obtener_conexion():
    try:
        # Configuración de parámetros de conexión local
        # Se utiliza el puerto 3307 debido a la configuración específica del servicio en XAMPP
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            port=3307,    
            database="farmacarlo_db"
        )
        return conexion
    except Exception as err:
        # Captura y visualización de errores de red o autenticación
        print(f"Error de conexión: {err}")
        return None