from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

# --- IMPORTACIONES DE NUEVAS CAPAS ---
from Conexion.conexion import obtener_conexion 
from services.producto_service import ProductoService
from services.reporte_service import ReporteService
from forms.producto_form import ProductoForm

app = Flask(__name__)

# --- CONFIGURACIÓN DE SEGURIDAD ---
app.config['SECRET_KEY'] = 'clave_secreta_farmacarlo_2024'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- MODELO DE USUARIO ---
class Usuario(UserMixin):
    def __init__(self, id, nombre, email):
        self.id = id
        self.nombre = nombre
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'])
    return None

# --- RUTAS DE AUTENTICACIÓN ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = obtener_conexion()
        if conn:
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
                flash("Credenciales inválidas", "danger")
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            try:
                # Insertamos el nuevo usuario en la tabla de la base de datos
                query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query, (nombre, email, password))
                conn.commit()
                flash("Cuenta creada con éxito. Ahora puedes iniciar sesión.", "success")
                return redirect(url_for('login'))
            except Exception as e:
                flash("El correo ya está registrado o hubo un error.", "danger")
            finally:
                cursor.close()
                conn.close()
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- RUTA PRINCIPAL DE DATOS (GESTIÓN DE INVENTARIO) ---

@app.route('/datos', methods=['GET', 'POST'])
@login_required
def manejar_datos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        id_categoria = request.form.get('id_categoria')
        id_proveedor = request.form.get('id_proveedor')
        
        form = ProductoForm(nombre, cantidad, precio, id_categoria, id_proveedor)
        
        if form.validar():
            ProductoService.insertar(nombre, cantidad, precio, id_categoria, id_proveedor)
            flash("Producto registrado con éxito en el inventario", "success")
        else:
            flash("Error en la validación de los datos", "danger")
            
        return redirect(url_for('manejar_datos'))

    # --- LÓGICA PARA CONTAR Y LISTAR CATEGORÍAS ---
    total_cats = 0
    categorias_lista = []
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor(dictionary=True)
        # Obtenemos todas las categorías para el formulario
        cursor.execute("SELECT * FROM categorias")
        categorias_lista = cursor.fetchall()
        # Contamos cuántas hay
        total_cats = len(categorias_lista)
        cursor.close()
        conn.close()

    res_mysql = ProductoService.listar_todos()
    return render_template('datos.html', 
                           productos_mysql=res_mysql,
                           usuario=current_user,
                           total_categorias=total_cats,
                           lista_categorias=categorias_lista) # Enviamos la lista al HTML

# --- NUEVA RUTA PARA ACTUALIZAR ---
@app.route('/editar/<int:id>', methods=['POST'])
@login_required
def editar_producto(id):
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    id_categoria = request.form.get('id_categoria')
    id_proveedor = request.form.get('id_proveedor')
    
    if ProductoService.actualizar(id, nombre, cantidad, precio, id_categoria, id_proveedor):
        flash("Producto actualizado correctamente", "info")
    else:
        flash("Error al actualizar", "danger")
    return redirect(url_for('manejar_datos'))

# --- RUTA PARA ELIMINAR REGISTROS ---
@app.route('/eliminar/<int:id>')
@login_required
def eliminar_producto(id):
    ProductoService.eliminar(id)
    flash("Registro eliminado del sistema", "warning")
    return redirect(url_for('manejar_datos'))

# --- RUTA PARA GENERACIÓN DE REPORTES ---
@app.route('/reporte_pdf')
@login_required
def reporte_pdf():
    productos = ProductoService.listar_todos()
    ruta_pdf = ReporteService.generar_pdf_productos(productos)
    return send_file(ruta_pdf, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)