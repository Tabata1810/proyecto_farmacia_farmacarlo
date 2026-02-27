from flask import Flask, render_template

app = Flask(__name__)

# ------------------------
# Ruta principal
# ------------------------
@app.route('/')
def inicio():
    return render_template('index.html')


# ------------------------
# Ruta acerca de
# ------------------------
@app.route('/about')
def about():
    return render_template('about.html')


# ------------------------
# Ruta productos
# ------------------------
@app.route('/productos')
def productos():
    return render_template('productos.html')


# ------------------------
# Ruta dinámica producto
# ------------------------
@app.route('/producto/<nombre>')
def producto(nombre):
    return f'Producto: {nombre} disponible en Farmacia FarmaCarlo.'


# ------------------------
# Ejecutar aplicación
# ------------------------
if __name__ == '__main__':
    app.run(debug=True)