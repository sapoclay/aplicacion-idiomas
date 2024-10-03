from fpdf import FPDF
import flet as ft
import os
import platform
from db import get_diccionario

# Función para exportar a PDF
def exportar_a_pdf(page):
    try:
        palabras = get_diccionario(page)
    
        if not palabras:
            page.snackbar = ft.SnackBar(ft.Text("No hay palabras para exportar."))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()
            return

        pdf = FPDF()
        pdf.add_page()
        
        # Configuración de la fuente para los encabezados
        pdf.set_font("Arial", 'B', size=12)

        # Dibujar las celdas con fondo gris claro
        pdf.set_fill_color(200, 200, 200)  # Gris claro
        pdf.cell(60, 10, "Palabra", border=1, fill=True)
        pdf.cell(90, 10, "Definición", border=1, fill=True)
        pdf.cell(40, 10, "Categoría", border=1, fill=True)
        pdf.ln()

        # Volver a la fuente normal para el contenido
        pdf.set_font("Arial", size=12)

        # Añadir cada palabra, definición y categoría al PDF
        for palabra, definicion, categoria in palabras:
            pdf.cell(60, 10, palabra, border=1)
            pdf.cell(90, 10, definicion, border=1)
            pdf.cell(40, 10, categoria, border=1)
            pdf.ln()

        # Guardar el PDF
        pdf_file_path = "diccionario_exportado.pdf"
        pdf.output(pdf_file_path)

        # Crear un botón para abrir el archivo PDF
        def abrir_pdf(e):
            if platform.system() == "Windows":
                os.startfile(pdf_file_path)  # Abre el archivo PDF en Windows
            elif platform.system() == "Linux":
                os.system(f'xdg-open "{pdf_file_path}"')  # Abre en Linux
            elif platform.system() == "Darwin":  # macOS
                os.system(f'open "{pdf_file_path}"')  # Abre en macOS

        # Crear el SnackBar con un botón
        page.snackbar = ft.SnackBar(
            ft.Row([
                ft.Text(f"Diccionario exportado a {pdf_file_path}."),
                ft.TextButton("Abrir el Diccionario", on_click=abrir_pdf)  # Cambia el color del texto a azul oscuro
            ])
        )
        
        page.snackbar.open = True
        page.add(page.snackbar)
        page.update()


    except Exception as e:
        page.snackbar = ft.SnackBar(ft.Text(f"Error al exportar a PDF: {str(e)}"))
        page.snackbar.open = True
        page.add(page.snackbar)
        page.update()
