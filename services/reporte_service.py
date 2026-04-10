import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Conexion.conexion import obtener_conexion
from datetime import datetime

class ReporteService:
    
    @staticmethod
    def generar_pdf_inventario():
        nombre_archivo = "reporte_inventario.pdf"
        ruta_pdf = os.path.join(os.getcwd(), nombre_archivo)
        
        c = canvas.Canvas(ruta_pdf, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "REPORTE DE INVENTARIO - FARMACARLO")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, "Listado oficial de productos en stock")
        c.line(100, 720, 500, 720)

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
            if y < 50: 
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

    @staticmethod
    def generar_pdf_ventas_hoy():
        nombre_archivo = "reporte_ventas_hoy.pdf"
        ruta_pdf = os.path.join(os.getcwd(), nombre_archivo)
        hoy = datetime.now().date()
        
        c = canvas.Canvas(ruta_pdf, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, f"REPORTE DE VENTAS - {hoy}")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, "Farmacarlo - Detalle de facturación diaria")
        c.line(100, 720, 500, 720)

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT v.id_venta, c.nombre as cliente, v.total, 
                   p.nombre as producto, dv.cantidad, dv.precio_unitario
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            JOIN detalle_ventas dv ON v.id_venta = dv.id_venta
            JOIN productos_mysql p ON dv.id_producto = p.id
            WHERE DATE(v.fecha) = %s
        """
        
        cursor.execute(query, (hoy,))
        ventas = cursor.fetchall()
        
        y = 690
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "ID")
        c.drawString(100, y, "Cliente")
        c.drawString(250, y, "Producto")
        c.drawString(400, y, "Cant.")
        c.drawString(450, y, "Precio U.")
        
        y -= 20
        c.setFont("Helvetica", 9)
        
        for v in ventas:
            if y < 50:
                c.showPage()
                y = 750
            
            c.drawString(50, y, f"#{v['id_venta']}")
            c.drawString(100, y, str(v['cliente'])[:25])
            c.drawString(250, y, str(v['producto'])[:30])
            c.drawString(400, y, str(v['cantidad']))
            c.drawString(450, y, f"${v['precio_unitario']:.2f}")
            y -= 15

        cursor.close()
        conn.close()
        c.save()
        return ruta_pdf