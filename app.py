from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF
from datetime import datetime

from Conexion.conexion import obtener_conexion 
from services.producto_service import ProductoService
from services.reporte_service import ReporteService
from forms.producto_form import ProductoForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'clave_secreta_farmacarlo_2024'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

login_manager.login_message = "🔒 Por favor, inicia sesión para acceder a esta página."

# Clase de Usuario para Flask-Login
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

# RUTAS DE NAVEGACIÓN

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html', usuario=current_user)

@app.route('/acerca')
@login_required
def acerca():
    return render_template('acerca.html', usuario=current_user)

# SISTEMA DE ACCESO

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_escrita = request.form['password']

        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email =  %s", (email,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()

            if user_data and check_password_hash(user_data['password'], password_escrita):
                user_obj = Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'])
                login_user(user_obj)
                return redirect(url_for('home'))
            else:
                flash("Correo o contraseña incorrectos", "danger")
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password_plana = request.form['password']

        password_encriptada = generate_password_hash(password_plana)

        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s,%s,%s)", (nombre, email, password_encriptada))
                conn.commit()
                flash("✅ Registro exitoso, ya puedes iniciar sesión", "success")
                return redirect(url_for('login'))
            except Exception as e:
                flash("❌ El correo ya está registrado o hubo un error", "danger")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# GESTIÓN DE INVENTARIO

@app.route('/datos', methods=['GET', 'POST'])
@login_required
def manejar_datos():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')
        id_categoria = request.form.get('id_categoria')
        id_proveedor = request.form.get('id_proveedor')
        
        if ProductoForm(nombre, cantidad, precio, id_categoria, id_proveedor).validar():
            ProductoService.insertar(nombre, cantidad, precio, id_categoria, id_proveedor)
            flash("✅ Producto registrado", "success")
        return redirect(url_for('manejar_datos'))

    # CARGA DE DATOS PARA LOS SELECTS Y TABLAS
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    
    cursor.execute("SELECT id_proveedor, nombre_empresa FROM proveedores")
    proveedores = cursor.fetchall()
    
    cursor.execute("SELECT * FROM productos_mysql")
    productos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('datos.html', 
                           productos_mysql=productos, 
                           lista_categorias=categorias, 
                           lista_proveedores=proveedores, 
                           usuario=current_user)

@app.route('/eliminar_producto/<int:id>')
@login_required
def eliminar_producto(id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos_mysql WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("🗑️ Producto eliminado", "success")
    except Exception as e:
        flash(f"❌ Error: {str(e)}", "danger")
    return redirect(url_for('manejar_datos'))

# GESTIÓN DE CLIENTES 

@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def manejar_clientes():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        try:
            cursor.execute("INSERT INTO clientes (nombre, cedula, telefono, correo) VALUES (%s,%s,%s,%s)", (nombre, cedula, telefono, correo))
            conn.commit()
            flash("✅ Cliente registrado", "success")
        except:
            flash("❌ Error: La cédula ya existe", "danger")
        return redirect(url_for('manejar_clientes'))
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', lista_clientes=clientes, usuario=current_user)

@app.route('/eliminar_cliente/<int:id>')
@login_required
def eliminar_cliente(id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("🗑️ Cliente eliminado", "success")
    except Exception as e:
        flash(f"❌ Error: {str(e)}", "danger")
    return redirect(url_for('manejar_clientes'))

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')

        try:
            sql = """
                UPDATE clientes 
                SET nombre=%s, cedula=%s, telefono=%s, correo=%s 
                WHERE id_cliente=%s
            """
            cursor.execute(sql, (nombre, cedula, telefono, correo, id))
            conn.commit()
            flash("✏️ Datos del cliente actualizados", "success")
        except Exception as e:
            flash(f"❌ Error al actualizar: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('manejar_clientes'))

    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if cliente:
        return render_template('editar_cliente.html', cliente=cliente, usuario=current_user)
    
    return redirect(url_for('manejar_clientes'))

# GESTIÓN DE PROVEEDORES 

@app.route('/proveedores', methods=['GET', 'POST'])
@login_required
def manejar_proveedores():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        empresa = request.form.get('empresa')
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        direccion = request.form.get('direccion')
        try:
            sql = "INSERT INTO proveedores (nombre_empresa, contacto_vendedor, telefono_proveedor, correo, direccion) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql,(empresa,nombre,telefono,correo,direccion))
            conn.commit()
            flash("✅ Proveedor registrado correctamente","success")
        except Exception as e:
            flash(f"❌ Error al registrar proveedor: {str(e)}","danger")
        return redirect(url_for('manejar_proveedores'))
    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', lista_proveedores=proveedores, usuario=current_user)

@app.route('/eliminar_proveedor/<int:id>')
@login_required
def eliminar_proveedor(id):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proveedores WHERE id_proveedor=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("🗑️ Proveedor eliminado","success")
    except Exception as e:
        flash(f"❌ Error: {str(e)}","danger")
    return redirect(url_for('manejar_proveedores'))

@app.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        empresa = request.form.get('empresa')
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        direccion = request.form.get('direccion')

        sql = """
            UPDATE proveedores 
            SET nombre_empresa=%s, contacto_vendedor=%s, telefono_proveedor=%s, correo=%s, direccion=%s 
            WHERE id_proveedor=%s
        """
        cursor.execute(sql, (empresa, nombre, telefono, correo, direccion, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("✏️ Proveedor actualizado con éxito", "success")
        return redirect(url_for('manejar_proveedores'))

    cursor.execute("SELECT * FROM proveedores WHERE id_proveedor = %s", (id,))
    proveedor = cursor.fetchone()
    cursor.close()
    conn.close()

    if proveedor:
        return render_template('editar_proveedor.html', prov=proveedor, usuario=current_user)
    
    flash("❌ Proveedor no encontrado", "danger")
    return redirect(url_for('manejar_proveedores'))

# GESTIÓN DE VENTAS

@app.route('/ventas', methods=['GET', 'POST'])
@login_required
def manejar_ventas():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    hoy = datetime.now().date()

    if 'carrito' not in session:
        session['carrito'] = []

    if request.method == 'POST':
        accion = request.form.get('accion')
        
        if accion == 'agregar':
            id_p = request.form.get('id_producto')
            cant = int(request.form.get('cantidad', 1))
            
            cursor.execute("SELECT nombre, precio FROM productos_mysql WHERE id = %s", (id_p,))
            p = cursor.fetchone()
            if p:
                precio_original = float(p['precio'])
                subtotal = precio_original * cant
                
                session['carrito'].append({
                    'id': id_p, 
                    'nombre': p['nombre'], 
                    'cantidad': cant, 
                    'precio': precio_original,
                    'subtotal': subtotal
                })
                session.modified = True
        
        elif accion == 'finalizar':
            id_c = request.form.get('id_cliente')
            if session['carrito'] and id_c:
                total_v = sum(item['subtotal'] for item in session['carrito'])
                cursor.execute("INSERT INTO ventas (id_cliente, total, fecha) VALUES (%s, %s, NOW())", (id_c, total_v))
                id_v = cursor.lastrowid
                for item in session['carrito']:
                    cursor.execute("""
                        INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal) 
                        VALUES (%s,%s,%s,%s,%s)
                    """, (id_v, item['id'], item['cantidad'], item['precio'], item['subtotal']))
                conn.commit()
                session.pop('carrito', None)
                flash("✅ Venta registrada con éxito", "success")
        
        elif accion == 'limpiar':
            session.pop('carrito', None)
        return redirect(url_for('manejar_ventas'))

    cursor.execute("SELECT v.id_venta, c.nombre as cliente_nombre, v.total, v.fecha FROM ventas v JOIN clientes c ON v.id_cliente = c.id_cliente WHERE DATE(v.fecha) = %s ORDER BY v.fecha DESC", (hoy,))
    lista_ventas = cursor.fetchall()
    for v in lista_ventas:
        cursor.execute("SELECT p.nombre as producto_nombre, dv.cantidad, dv.precio_unitario as precio FROM detalle_ventas dv JOIN productos_mysql p ON dv.id_producto = p.id WHERE dv.id_venta = %s", (v['id_venta'],))
        v['detalles'] = cursor.fetchall()
    cursor.execute("SELECT id_cliente, nombre FROM clientes")
    clientes = cursor.fetchall()
    cursor.execute("SELECT id, nombre, precio FROM productos_mysql")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('ventas.html', lista_ventas=lista_ventas, clientes=clientes, productos=productos, carrito=session.get('carrito', []))

# REPORTES 

@app.route('/reporte_pdf')
@login_required
def reporte_pdf():
    try:
        ruta_pdf = ReporteService.generar_pdf_inventario()
        return send_file(ruta_pdf, as_attachment=True)
    except Exception as e:
        flash(f"Error al generar el PDF: {str(e)}","danger")
        return redirect(url_for('manejar_datos'))

@app.route('/descargar_reporte_pdf')
@login_required
def descargar_reporte_ventas():
    try:

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        hoy = datetime.now().date()

        query = """
            SELECT v.id_venta, c.nombre as cliente, v.total, v.fecha,
                   p.nombre as producto, dv.cantidad, dv.precio_unitario
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            JOIN detalle_ventas dv ON v.id_venta = dv.id_venta
            JOIN productos_mysql p ON dv.id_producto = p.id
            WHERE DATE(v.fecha) = %s
        """
        cursor.execute(query, (hoy,))
        datos = cursor.fetchall()
        
        ruta_pdf = ReporteService.generar_pdf_ventas_hoy() 
        
        return send_file(ruta_pdf, as_attachment=True)
        
    except Exception as e:
        print(f"Error en reporte de ventas: {e}")
        flash(f"Error al generar reporte: {e}", "danger")
        return redirect(url_for('manejar_ventas'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)