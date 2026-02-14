from flask import Flask

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return "Bienvenido a FarmaCarlo – Sistema de Ventas y Control de Medicamentos"

# Ruta dinámica para consultar medicamentos
@app.route('/medicamento/<nombre>')
def medicamento(nombre):
    return f"Medicamento: {nombre} – disponible en FarmaCarlo."

# Ruta adicional para mostrar información del sistema
@app.route('/nosotros')
def nosotros():
    return "FarmaCarlo es una farmacia dedicada a la venta y control de medicamentos para el cuidado de la salud."

if __name__ == '__main__':
    app.run(debug=True)
