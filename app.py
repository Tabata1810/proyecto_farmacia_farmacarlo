from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import csv
import os

app = Flask(__name__)

# =========================================================
# CONFIGURACIÓN DE LA BASE DE DATOS (SQLAlchemy)
# =========================================================
# Creamos el archivo farmacia.db automáticamente en la carpeta del proyecto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmacia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definimos el modelo de los productos para la farmacia (POO)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

# Este comando crea la tabla en SQLite si aún no existe
with app.app_context():
    db.create_all()

# =========================================================
# RUTAS HACIA NUESTROS ARCHIVOS DE DATOS
# =========================================================
# Usamos os.path.join para que funcione bien en cualquier computadora
CARPETA_DATOS = os.path.join('inventario', 'data')
ARCHIVO_TXT = os.path.join(CARPETA_DATOS, 'datos.txt')
ARCHIVO_JSON = os.path.join(CARPETA_DATOS, 'datos.json')
ARCHIVO_CSV = os.path.join(CARPETA_DATOS, 'datos.csv')

# =========================================================
# RUTAS DE LA APLICACIÓN
# =========================================================

@app.route('/')
def index():
    # Página principal de Farmacarlo
    return render_template('index.html')

@app.route('/datos', methods=['GET', 'POST'])
def manejar_datos():
    if request.method == 'POST':
        # 1. Capturamos lo que el usuario escribió en el formulario
        nombre_med = request.form['nombre']
        stock_med = request.form['cantidad']
        precio_med = request.form['precio']

        # 2. GUARDAR EN SQLITE (Base de Datos profesional)
        nuevo_item = Producto(nombre=nombre_med, cantidad=int(stock_med), precio=float(precio_med))
        db.session.add(nuevo_item)
        db.session.commit() # Guardamos los cambios en el archivo .db

        # 3. GUARDAR EN ARCHIVO DE TEXTO (.txt)
        with open(ARCHIVO_TXT, 'a', encoding='utf-8') as f_txt:
            f_txt.write(f"Medicamento: {nombre_med} | Stock: {stock_med} | PVP: {precio_med}\n")

        # 4. GUARDAR EN ARCHIVO JSON (Con manejo de errores para que no falle)
        lista_temporal = []
        try:
            if os.path.exists(ARCHIVO_JSON):
                with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f_json:
                    contenido = f_json.read()
                    if contenido:
                        lista_temporal = json.loads(contenido)
        except Exception as e:
            print(f"Error al leer JSON: {e}")
            lista_temporal = []

        # Agregamos el nuevo medicamento a la lista y guardamos
        lista_temporal.append({
            "nombre": nombre_med, 
            "cantidad": stock_med, 
            "precio": precio_med
        })
        
        with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f_json:
            json.dump(lista_temporal, f_json, indent=4)

        # 5. GUARDAR EN ARCHIVO EXCEL (.csv)
        with open(ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as f_csv:
            escritor = csv.writer(f_csv)
            # Si el archivo está vacío, podrías poner encabezados aquí
            escritor.writerow([nombre_med, stock_med, precio_med])

        # Después de guardar, refrescamos la página
        return redirect(url_for('manejar_datos'))

    # --- LECTURA DE DATOS PARA MOSTRAR EN PANTALLA ---
    
    # Consultamos la base de datos SQLite
    lista_db = Producto.query.all()
    
    # Leemos el JSON para mostrarlo en la otra columna
    lista_json = []
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f_json:
            try:
                lista_json = json.load(f_json)
            except:
                lista_json = []

    return render_template('datos.html', 
                           productos_db=lista_db, 
                           productos_json=lista_json)

if __name__ == '__main__':
    # Iniciamos la aplicación en modo prueba
    app.run(debug=True)