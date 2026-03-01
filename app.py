from flask import Flask, render_template, request, redirect
from database import crear_tabla
from models.inventario import Inventario
import os

app = Flask(__name__)
inventario = Inventario()

crear_tabla()


@app.route('/')
def inicio():
    productos = inventario.obtener_productos()
    return render_template('index.html', productos=productos)


@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    inventario.agregar_producto(nombre, cantidad, precio)
    return redirect('/')


@app.route('/eliminar/<int:id>')
def eliminar(id):
    inventario.eliminar_producto(id)
    return redirect('/')


@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    inventario.actualizar_producto(id, nombre, cantidad, precio)
    return redirect('/')


@app.route('/buscar', methods=['POST'])
def buscar():
    nombre = request.form['nombre']
    productos = inventario.buscar_producto(nombre)
    return render_template('index.html', productos=productos)


# 🔹 NUEVAS RUTAS (DEBEN IR FUERA DEL if)
@app.route("/acerca")
def acerca():
    return render_template("acerca.html")


@app.route("/productos")
def productos():
    productos = inventario.obtener_productos()
    return render_template("productos.html", productos=productos)


# 🔹 Esto SIEMPRE va al final y solo para ejecutar localmente
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)