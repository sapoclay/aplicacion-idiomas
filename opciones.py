import flet as ft

def opciones_tab(page: ft.Page):
    # Variable para almacenar el estado del tema
    tema_oscuro = False

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
                        ft.Image(src="resources/Logo.png", width=100, height=100),  # Ajusta el tamaño si es necesario
                        ft.Text(
                            "Esta es una aplicación en la que poder almacenar recursos de manera rápida y sencilla.\n"
                            "En principio va a permitir almacenar palabras o frases y su significado o traducción, listenings y un traductor online.",
                            text_align="center"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrar contenido verticalmente
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrar horizontalmente
                    spacing=20  # Espacio entre los elementos
                ),
                padding=20,  # Añadir padding alrededor del contenido
                width=300,  # Controlar el ancho del diálogo
                height=300  # Controlar la altura del diálogo
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=cerrar_dialogo)  # Botón para cerrar el diálogo
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
        nonlocal tema_oscuro  # Permitir la modificación de la variable externa
        tema_oscuro = toggle_tema(page, tema_oscuro)

    # Diseño de la pestaña Opciones
    opciones_row1 = ft.Row(
        [
            ft.ElevatedButton("Mostrar Información", on_click=mostrar_informacion),
            ft.ElevatedButton("Cambiar Tema", on_click=cambiar_tema),  # Botón para cambiar de tema
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,  # Espacio entre los botones
    )
    
    opciones_row2 = ft.Row(
        [
            ft.ElevatedButton("Cerrar Aplicación", on_click=cerrar_aplicacion),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,  # Espacio entre los botones
    )

    # Retornar la fila con un espacio adicional arriba para empujar los botones hacia abajo
    return ft.Column(
        [
            ft.Container(height=200),  # Añadir un espacio vacío con altura fija para empujar los botones hacia abajo
            opciones_row1,
            ft.Container(),  # Elemento vacío debajo, si es necesario
            opciones_row2,
        ],
        alignment=ft.MainAxisAlignment.START,  # Mantener el contenido alineado al inicio
        expand=True
    )