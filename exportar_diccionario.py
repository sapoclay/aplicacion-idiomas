from fpdf import FPDF
import flet as ft
from db import get_diccionario

# Función para exportar a PDF
def exportar_a_pdf(page):
    try:
        palabras = get_diccionario()

        if not palabras:
            page.snackbar = ft.SnackBar(ft.Text("El diccionario está vacío."))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título del PDF
        pdf.cell(200, 10, txt="Diccionario de Conceptos", ln=True, align='C')

        # Añadir palabras y definiciones
        for palabra, definicion in palabras:
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Palabra/Frase: {palabra}", ln=True)
            pdf.cell(200, 10, txt=f"Definición/Traducción: {definicion}", ln=True)

        # Guardar PDF en un archivo
        pdf.output("diccionario_exportado.pdf")

        # Mensaje de éxito
        page.snackbar = ft.SnackBar(ft.Text("Diccionario exportado como PDF con éxito."))
        page.snackbar.open = True
        page.add(page.snackbar)
        page.update()

    except Exception as e:
        page.snackbar = ft.SnackBar(ft.Text(f"Error al exportar a PDF: {str(e)}"))
        page.snackbar.open = True
        page.add(page.snackbar)
        page.update()
