import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Conexion.conexion import obtener_conexion

class ReporteService:
    @staticmethod
    def generar_pdf_inventario():
        # Nombre del archivo y ruta
        nombre_archivo = "reporte_inventario.pdf"
        ruta_pdf = os.path.join(os.getcwd(), nombre_archivo)
        
        # Creamos el PDF
        c = canvas.Canvas(ruta_pdf, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "REPORTE DE INVENTARIO - FARMACARLO")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, "Listado oficial de productos en stock")
        c.line(100, 720, 500, 720)

        # Consultamos los datos
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos_mysql")
        productos = cursor.fetchall()
        
        y = 690
        c.setFont("Helvetica-Bold", 10)
        c.drawString(100, y, "Producto")
        c.drawString(300, y, "Cantidad")
        c.drawString(400, y, "Precio")
        y -= 20
        c.setFont("Helvetica", 10)

        for p in productos:
            if y < 50: # Si se acaba la hoja, creamos otra
                c.showPage()
                y = 750
            
            c.drawString(100, y, str(p['nombre']))
            c.drawString(300, y, str(p['cantidad']))
            c.drawString(400, y, f"${p['precio']:.2f}")
            y -= 20

        cursor.close()
        conn.close()
        
        c.save()
        return ruta_pdf