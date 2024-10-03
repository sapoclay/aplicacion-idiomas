import flet as ft
import sqlite3
import webbrowser
import os
import subprocess
from db import guardar_url, cargar_urls, eliminar_url, actualizar_url
import webbrowser
import urllib.parse 

# Función para reproducir la URL o el archivo MP3 en el reproductor predeterminado
def reproducir(e, ruta):
    if ruta.startswith("http://") or ruta.startswith("https://"):
        webbrowser.open(ruta)  # Reproducir URL
    elif os.path.isfile(ruta):  # Comprobar si es un archivo local
        if os.name == 'nt':  # Windows
            os.startfile(ruta)
        else:  # Unix/Linux/Mac
            subprocess.call(["xdg-open", ruta])  # Para Linux
            # Para Mac, podrías usar: subprocess.call(["open", ruta])

# Definir la interfaz gráfica
def listening_tab(page: ft.Page):
    espacio_extra = ft.Container(height=20)

    # Ejemplo de mejora de la función guardar
    def guardar(e):
        """Guarda la URL o MP3 en la base de datos."""
        nombre = nombre_input.value
        url_o_mp3 = url_input.value
        if nombre and url_o_mp3:
            guardar_url(nombre, url_o_mp3)
            nombre_input.value = ""
            url_input.value = ""
            page.update()
            cargar_listado()
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Por favor, completa ambos campos."),
                duration=3000
            )
            page.snack_bar.open = True
            page.update()

    def borrar(e):
        nombre_input.value = ""
        url_input.value = ""
        page.update()

    def seleccionar_archivo(e):
        file_picker.pick_files()  # Abrir el selector de archivos

    # Función para mostrar un diálogo de confirmación antes de eliminar
    def confirmar_eliminar(nombre, id):
        def on_confirm(e):
            eliminar_url(id)  # Eliminar de la base de datos
            cargar_listado()  # Recargar el listado después de la eliminación
            dialog.open = False  # Cerrar el diálogo
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"'{nombre}' fue eliminado correctamente."),
                duration=3000  # Duración del Snackbar en milisegundos
            )
            page.snack_bar.open = True  # Mostrar el Snackbar
            page.update()

        def on_cancel(e):
            dialog.open = False  # Cerrar el diálogo sin eliminar
            page.update()

        # Crear el diálogo de confirmación
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar '{nombre}'?"),
            actions=[
                ft.TextButton("No", on_click=on_cancel),
                ft.TextButton("Sí", on_click=on_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Mostrar el diálogo en la página
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Función para eliminar una URL
    def eliminar(e, id, nombre):
        confirmar_eliminar(nombre, id)  # Llamar a la función de confirmación



    # Función para editar una URL
    def editar(e, id, nombre_actual, url_actual):
        nombre_input.value = nombre_actual
        url_input.value = url_actual
        page.update()

        def actualizar(e):
            nuevo_nombre = nombre_input.value
            nueva_url_o_mp3 = url_input.value
            if nuevo_nombre and nueva_url_o_mp3:
                actualizar_url(id, nuevo_nombre, nueva_url_o_mp3)  # Actualiza el mismo campo
                nombre_input.value = ""
                url_input.value = ""
                page.update()
                cargar_listado()

        guardar_btn.on_click = actualizar  # Cambiar el comportamiento del botón guardar

    # Formulario
    nombre_input = ft.TextField(label="Nombre")
    url_input = ft.TextField(label="URL o Ubicación del MP3")
    guardar_btn = ft.ElevatedButton("Guardar", on_click=guardar, tooltip="Guardar en la Base de Datos")
    borrar_btn = ft.ElevatedButton("Borrar", on_click=borrar, tooltip="Borrar Campos")
    seleccionar_btn = ft.ElevatedButton("Seleccionar MP3", on_click=seleccionar_archivo, tooltip="Seleccionar Archivo MP3/MP4 Local")

    # Definir una función para manejar el resultado del FilePicker
    def manejar_seleccion_archivo(e):
        if e.files:
            url_input.value = e.files[0].path  # Asignar el valor correctamente
        else:
            url_input.value = ""  # Limpiar si no se selecciona ningún archivo
        page.update()  # Actualizar la página

    file_picker = ft.FilePicker(on_result=manejar_seleccion_archivo)
    # Asegúrate de agregar el file_picker a la página
    page.controls.append(file_picker)

    # Campo de búsqueda
    buscador_input = ft.TextField(label="Buscar por Nombre", on_change=lambda e: cargar_listado(buscador_input.value))

    # Contenedor para el listado de URLs
    listado = ft.Column(scroll="adaptive")  # Añadir scroll adaptable al tamaño del contenido

    # Función para compartir la URL por correo
    def compartir_por_correo(nombre, url):
        try:
            destinatario = ""  # Puedes predefinir un destinatario si lo deseas
            asunto = f"Esto es una recomendación: {nombre}"
            cuerpo = f"Hola,\n\nTe recomiendo que le eches un vistazo al siguiente contenido contenido:\n\nNombre: {nombre}\nURL: {url}\n\nEspero que te guste. Saludos."
            
            # Construir la URL mailto
            mailto_url = f"mailto:{destinatario}?subject={urllib.parse.quote(asunto)}&body={urllib.parse.quote(cuerpo)}"
            
            # Abrir en el cliente de correo por defecto
            webbrowser.open(mailto_url)
            
        except Exception as e:
            print(f"Error al intentar abrir el cliente de correo: {e}")

    # Ejemplo del botón compartir en Flet
    def crear_icono_compartir(nombre_o_mp3, url_o_mp3):
        return ft.IconButton(
            icon=ft.icons.MAIL,  # Cambiamos el icono a un sobre
            on_click=lambda e: compartir_por_correo(nombre_o_mp3, url_o_mp3),
            tooltip="Compartir por correo"
        )
        
        # Función para cargar el listado de URLs guardadas
    def cargar_listado(busqueda=""):
        listado.controls.clear()
        
        # Cabeceras de la tabla
        listado.controls.append(
            ft.Row([
                ft.Text("Nombre", weight="bold", expand=True, text_align=ft.TextAlign.START),
                ft.Text("URL / MP3", weight="bold", expand=True, text_align=ft.TextAlign.CENTER),
                ft.Text("Acciones", weight="bold", expand=True, text_align=ft.TextAlign.END)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)  # Ajustar el espacio entre cabeceras
        )
        
        urls = cargar_urls()
        if busqueda:
            urls = [url for url in urls if busqueda.lower() in url[1].lower()]  # Filtrar por nombre

        for id, nombre, url_o_mp3 in urls:
            listado.controls.append(
                ft.Row([
                    ft.Text(nombre, text_align=ft.TextAlign.START),  # Alineación a la izquierda
                    ft.Text(url_o_mp3, expand=True, text_align=ft.TextAlign.CENTER),  # Alineación centrada
                    ft.Row([
                        ft.IconButton(ft.icons.PLAY_ARROW, on_click=lambda e, r=url_o_mp3: reproducir(e, r), tooltip="Reproducir"),
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, i=id, n=nombre, u=url_o_mp3: editar(e, i, n, u), tooltip="Editar"),
                        crear_icono_compartir(nombre, url_o_mp3),  # Añadir el botón compartir
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, i=id, n=nombre: eliminar(e, i, n), tooltip="Eliminar")                    
                        ], alignment=ft.MainAxisAlignment.END)  # Alineación a la derecha
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)  # Ajustar el espacio entre columnas
            )
        page.update()

    # Cargar el listado al iniciar
    cargar_listado()
    
    # Agregar elementos al layout principal
    return ft.Column([
        espacio_extra,
        ft.Text("Añadir nueva URL o archivo MP3:"),
        nombre_input,
        url_input,
        ft.Row([guardar_btn, borrar_btn, seleccionar_btn]),  # Agregar el botón de selección
        ft.Divider(),
        buscador_input,  # Añadir el campo de búsqueda
        ft.Divider(),
        ft.Text("Listado de URLs y archivos MP3 guardados:"),
        ft.Divider(),
        ft.Container(content=listado, expand=True, height=500)  # Aquí el contenedor con scroll
    ], expand=True)