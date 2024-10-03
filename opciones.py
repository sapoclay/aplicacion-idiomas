import flet as ft
import os
import platform
import webbrowser

def opciones_tab(page: ft.Page):
    # Variable para almacenar el estado del tema
    tema_oscuro = False
    diccionario_path = "diccionario_exportado.pdf"  # Ruta del archivo PDF exportado

    # Función para cerrar la aplicación
    def cerrar_aplicacion(e):
        page.window_destroy()

    # Función para alternar entre tema oscuro y claro
    def toggle_tema(page: ft.Page, tema_oscuro: bool) -> bool:
        tema_oscuro = not tema_oscuro
        page.theme_mode = ft.ThemeMode.DARK if tema_oscuro else ft.ThemeMode.LIGHT
        page.update()
        return tema_oscuro

    # Función para mostrar la información de la aplicación
    def mostrar_informacion(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Aplicación de Idiomas", text_align="center"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.TextButton("Repositorio en GitHub", url="https://github.com/sapoclay"),
                        ft.Image(src="resources/Logo.png", width=100, height=100),
                        ft.Text(
                            "Esta es una aplicación en la que poder almacenar recursos de manera rápida y sencilla.\n"
                            "En principio va a permitir almacenar palabras o frases y su significado o traducción, listenings y un traductor online.",
                            text_align="center"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                padding=20,
                width=300,
                height=300
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=cerrar_dialogo)
            ],
        )
        page.dialog.open = True
        page.update()

    # Función para cerrar el diálogo
    def cerrar_dialogo(e):
        page.dialog.open = False
        page.update()

    # Función para manejar el clic del botón de tema
    def cambiar_tema(e):
        nonlocal tema_oscuro
        tema_oscuro = toggle_tema(page, tema_oscuro)

    # Función para abrir el diccionario
    def abrir_diccionario(e):
        if os.path.exists(diccionario_path):
            # Detectar el sistema operativo y abrir el archivo
            if platform.system() == "Windows":
                os.startfile(diccionario_path)
            else:
                webbrowser.open(f"file://{os.path.abspath(diccionario_path)}")
        else:
            # Mostrar mensaje en Snackbar si el archivo no existe
            page.snack_bar = ft.SnackBar(ft.Text("El diccionario no ha sido exportado aún. Expórtalo desde la pestaña Vocabulario."))
            page.snack_bar.open = True
            page.update()

    # Diseño de la pestaña Opciones
    opciones_row1 = ft.Row(
        [
            ft.ElevatedButton("Mostrar Información", on_click=mostrar_informacion),
            ft.ElevatedButton("Cambiar Tema", on_click=cambiar_tema),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )
    
    opciones_row2 = ft.Row(
        [
            ft.ElevatedButton("Ver diccionario", on_click=abrir_diccionario),  # Nuevo botón
            ft.ElevatedButton("Cerrar Aplicación", on_click=cerrar_aplicacion),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    # Retornar la fila con un espacio adicional arriba para empujar los botones hacia abajo
    return ft.Column(
        [
            ft.Container(height=200),
            opciones_row1,
            ft.Container(),
            opciones_row2,
        ],
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )
