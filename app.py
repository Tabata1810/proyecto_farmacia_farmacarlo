from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import csv
import os
# Importación del módulo de conexión a MySQL
from Conexion.conexion import obtener_conexion 

app = Flask(__name__)

# --- Configuración de SQLite ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmacia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para la tabla de productos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

# Creación de tablas en el contexto de la aplicación
with app.app_context():
    db.create_all()

# --- Rutas de archivos de datos ---
CARPETA_DATOS = os.path.join('inventario', 'data')
ARCHIVO_TXT = os.path.join(CARPETA_DATOS, 'datos.txt')
ARCHIVO_JSON = os.path.join(CARPETA_DATOS, 'datos.json')
ARCHIVO_CSV = os.path.join(CARPETA_DATOS, 'datos.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datos', methods=['GET', 'POST'])
def manejar_datos():
    if request.method == 'POST':
        # Captura de datos desde el formulario
        nombre_med = request.form['nombre']
        stock_med = request.form['cantidad']
        precio_med = request.form['precio']

        # 1. Persistencia en SQLite
        nuevo_prod = Producto(nombre=nombre_med, cantidad=int(stock_med), precio=float(precio_med))
        db.session.add(nuevo_prod)
        db.session.commit()

        # 2. Persistencia en MySQL (HeidiSQL)
        conexion_mysql = obtener_conexion()
        if conexion_mysql:
            try:
                cursor = conexion_mysql.cursor()
                query = "INSERT INTO productos_mysql (nombre, cantidad, precio) VALUES (%s, %s, %s)"
                valores = (nombre_med, int(stock_med), float(precio_med))
                
                cursor.execute(query, valores)
                conexion_mysql.commit() 
                
                cursor.close()
                conexion_mysql.close()
            except Exception as e:
                print(f"Error en la transacción MySQL: {e}")

        # 3. Registro en archivos planos
        # Guardar en TXT
        with open(ARCHIVO_TXT, 'a', encoding='utf-8') as f:
            f.write(f"{nombre_med} | {stock_med} | {precio_med}\n")

        # Guardar en JSON
        datos_json = []
        if os.path.exists(ARCHIVO_JSON):
            try:
                with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f_json:
                    datos_json = json.load(f_json)
            except: 
                datos_json = []
        
        datos_json.append({"nombre": nombre_med, "cantidad": stock_med, "precio": precio_med})
        with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f_json:
            json.dump(datos_json, f_json, indent=4)

        # Guardar en CSV
        with open(ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as f_csv:
            writer = csv.writer(f_csv)
            writer.writerow([nombre_med, stock_med, precio_med])

        return redirect(url_for('manejar_datos'))

    # --- RECUPERACIÓN DE DATOS PARA MOSTRAR EN LA WEB ---
    
    # Lista 1: SQLite
    res_sqlite = Producto.query.all()
    
    # Lista 2: MySQL (HeidiSQL)
    res_mysql = []
    con = obtener_conexion()
    if con:
        try:
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT * FROM productos_mysql")
            res_mysql = cur.fetchall()
            cur.close()
            con.close()
        except Exception as e:
            print(f"Error al recuperar datos MySQL: {e}")

    # Lista 3: ESTA ES LA PARTE QUE HACEMOS PARA EL JSON
    res_json = []
    if os.path.exists(ARCHIVO_JSON):
        try:
            with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f:
                res_json = json.load(f)
        except Exception as e:
            print(f"Error al leer el archivo JSON: {e}")
            res_json = []
    
    # Se envían todas las listas al archivo HTML
    return render_template('datos.html', 
                            productos_db=res_sqlite, 
                            productos_mysql=res_mysql,
                            productos_json=res_json)

if __name__ == '__main__':
    app.run(debug=True)