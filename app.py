from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import csv
import os
# --- NUEVAS IMPORTACIONES PARA SEGURIDAD ---
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# -------------------------------------------
from Conexion.conexion import obtener_conexion 

app = Flask(__name__)

# --- CONFIGURACIÓN DE SEGURIDAD (SEMANA 14) ---
app.config['SECRET_KEY'] = 'clave_secreta_farmacarlo_2024'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirige aquí si no hay sesión

# --- CONFIGURACIÓN DE SQLite ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmacia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para la tabla de productos (SQLite)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

# --- MODELO DE USUARIO PARA LOGIN ---
class Usuario(UserMixin):
    def __init__(self, id, nombre, email):
        self.id = id
        self.nombre = nombre
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if user_data:
        return Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'])
    return None

# Creación de tablas SQLite
with app.app_context():
    db.create_all()

# --- RUTAS DE ARCHIVOS ---
CARPETA_DATOS = os.path.join('inventario', 'data')
ARCHIVO_TXT = os.path.join(CARPETA_DATOS, 'datos.txt')
ARCHIVO_JSON = os.path.join(CARPETA_DATOS, 'datos.json')
ARCHIVO_CSV = os.path.join(CARPETA_DATOS, 'datos.csv')

# --- RUTAS DE AUTENTICACIÓN ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", 
                       (nombre, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email, password))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user_data:
            user_obj = Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'])
            login_user(user_obj)
            return redirect(url_for('manejar_datos'))
        else:
            return "Credenciales incorrectas. <a href='/login'>Intentar de nuevo</a>"
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- RUTAS DEL SISTEMA ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datos', methods=['GET', 'POST'])
@login_required # <-- AHORA ESTA RUTA ESTÁ PROTEGIDA
def manejar_datos():
    if request.method == 'POST':
        nombre_med = request.form['nombre']
        stock_med = request.form['cantidad']
        precio_med = request.form['precio']

        # 1. SQLite
        nuevo_prod = Producto(nombre=nombre_med, cantidad=int(stock_med), precio=float(precio_med))
        db.session.add(nuevo_prod)
        db.session.commit()

        # 2. MySQL
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
                print(f"Error MySQL: {e}")

        # 3. Archivos Planos (TXT, JSON, CSV)
        with open(ARCHIVO_TXT, 'a', encoding='utf-8') as f:
            f.write(f"{nombre_med} | {stock_med} | {precio_med}\n")

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

        with open(ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as f_csv:
            writer = csv.writer(f_csv)
            writer.writerow([nombre_med, stock_med, precio_med])

        return redirect(url_for('manejar_datos'))

    # Recuperación de datos para la tabla
    res_sqlite = Producto.query.all()
    
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
            print(f"Error MySQL Select: {e}")

    res_json = []
    if os.path.exists(ARCHIVO_JSON):
        try:
            with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f:
                res_json = json.load(f)
        except:
            res_json = []
    
    return render_template('datos.html', 
                            productos_db=res_sqlite, 
                            productos_mysql=res_mysql,
                            productos_json=res_json,
                            usuario=current_user) # Pasamos el usuario a la vista

if __name__ == '__main__':
    app.run(debug=True)