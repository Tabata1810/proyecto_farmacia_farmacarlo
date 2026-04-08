import mysql.connector

# Configuración del conector para MySQL en XAMPP
def obtener_conexion():
    try:
        # Se utiliza el puerto 3307 por conflicto de servicios
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            port=3307,    
            database="farmacarlo_db"
        )
        return conexion
    except Exception as err:
        print(f"Error de conexión: {err}")
        return None