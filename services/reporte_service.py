from fpdf import FPDF
import os

class ReporteService:
    @staticmethod
    def generar_pdf_productos(productos):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Reporte de Inventario - Farmacarlo", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        
        for p in productos:
            # Usamos los nombres que vienen del JOIN de la base de datos
            texto = f"Producto: {p['nombre']} - Stock: {p['cantidad']} - Precio: ${p['precio']}"
            pdf.cell(200, 10, txt=texto, ln=True)
        
        # Guardar en una carpeta temporal o la raíz
        ruta = "reporte_productos.pdf"
        pdf.output(ruta)
        return ruta