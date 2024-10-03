import flet as ft
from diccionario import diccionario_tab
from traduccion import traduccion_tab
from listening import listening_tab
from db import crear_base_de_datos
from opciones import opciones_tab



def main(page: ft.Page):

    try:
        crear_base_de_datos()
    except Exception as e:
        page.snackbar = ft.SnackBar(ft.Text(f"Error al inicializar la base de datos: {str(e)}"), open=True)
        page.update()
        return  # Termina la ejecución si hay un error en la base de datos

    # Configurar la ventana de la aplicación
    page.title = "Aplicación de Idiomas"
    page.window.width = 800
    page.window.height = 800

    # Definir las pestañas de la aplicación
    tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Vocabulario", content=diccionario_tab(page)),
            ft.Tab(text="Traducción", content=traduccion_tab(page)),
            ft.Tab(text="Listening", content=listening_tab(page)),
            ft.Tab(text="Opciones", content=opciones_tab(page)),
        ]
    )

    page.add(tabs)


# Ejecutar la aplicación Flet
ft.app(target=main)
