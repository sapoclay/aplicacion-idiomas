import flet as ft
from db import insert_diccionario, get_diccionario, eliminar_palabra_de_db, actualizar_palabra_en_db
from exportar_diccionario import exportar_a_pdf

def diccionario_tab(page):
    espacio_extra = ft.Container(height=20)
    palabra_input = ft.TextField(label="Palabra/Frase", multiline=True, min_lines=5, max_lines=20, width=400)
    definicion_input = ft.TextField(label="Definición/Traducción", multiline=True, min_lines=5, max_lines=20, width=400)
    categoria_input = ft.TextField(label="Categoría", width=400)
    buscador_input = ft.TextField(label="Buscar", width=400)
    resultados_column = ft.Column(spacing=10)
    palabra_editando = None

    # Función auxiliar para mostrar el SnackBar y actualizar la página
    def mostrar_snackbar(mensaje):
        page.snackbar = ft.SnackBar(ft.Text(mensaje), open=True)
        page.add(page.snackbar)
        page.update()

    # Función para guardar el diccionario
    def guardar_diccionario(e):
        nonlocal palabra_editando

        # Validación de campos
        if not palabra_input.value.strip():
            mostrar_snackbar("El campo 'Palabra' es obligatorio.")
            return
        if not definicion_input.value.strip():
            mostrar_snackbar("El campo 'Definición' es obligatorio.")
            return
        if not categoria_input.value.strip():
            mostrar_snackbar("El campo 'Categoría' es obligatorio.")
            return

        try:
            if palabra_editando:  # Si estamos en modo edición
                actualizar_palabra_en_db(palabra_editando, palabra_input.value, definicion_input.value, categoria_input.value)
                mostrar_snackbar("Palabra actualizada con éxito.")
            else:  # Si es una nueva palabra
                insert_diccionario(palabra_input.value, definicion_input.value, categoria_input.value)
                mostrar_snackbar("Palabra guardada con éxito.")
            
            # Limpiar los campos
            palabra_input.value = ""
            definicion_input.value = ""
            categoria_input.value = ""
            palabra_editando = None

            actualizar_diccionario()  # Actualizar la lista
        except Exception as e:
            print(f"Error al guardar: {e}")  # Registro en consola para depuración
            mostrar_snackbar(f"Error al guardar: {str(e)}")

    # Función para actualizar el diccionario en la vista
    def actualizar_diccionario(busqueda=""):
        palabras = get_diccionario(page)
        resultados_column.controls.clear()

        # Filtrar por búsqueda
        if busqueda:
            palabras = [p for p in palabras if busqueda.lower() in p[0].lower() or busqueda.lower() in p[1].lower() or busqueda.lower() in p[2].lower()]

        # Encabezados (se colocan fuera del bucle)
        encabezado_fila = ft.Row([
            ft.Text("Palabra/Frase", weight="bold", expand=True),
            ft.Text("Definición/Traducción", weight="bold", expand=True),
            ft.Text("Categoría", weight="bold", expand=True),
            ft.Text("Acciones", weight="bold", width=100)
        ], alignment=ft.MainAxisAlignment.CENTER)
        resultados_column.controls.append(encabezado_fila)

        # Agregar filas de palabras, definiciones y categorías
        for palabra, definicion, categoria in palabras:
            fila_palabra = ft.Row([
                ft.Text(palabra, expand=True),
                ft.Text(definicion, expand=True),
                ft.Text(categoria, expand=True),
                ft.Row([
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, p=palabra: borrar_palabra(p)),
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, p=palabra, d=definicion, c=categoria: editar_palabra(p, d, c))
                ], alignment=ft.MainAxisAlignment.END)
            ], alignment=ft.MainAxisAlignment.CENTER)
            resultados_column.controls.append(fila_palabra)

        page.update()

    # Función para buscar palabras
    def buscar_palabra(e):
        actualizar_diccionario(buscador_input.value)

    # Función para limpiar el buscador
    def limpiar_buscador(e):
        buscador_input.value = ""
        page.update()
        actualizar_diccionario()

    # Función para eliminar una palabra
    def borrar_palabra(palabra):
        def confirmar_borrado(e):
            if e.control.data == "Eliminar":
                try:
                    if eliminar_palabra_de_db(palabra):
                        mostrar_snackbar(f"Palabra '{palabra}' eliminada.")
                    else:
                        mostrar_snackbar(f"Error al eliminar la palabra '{palabra}'.")
                except Exception as err:
                    print(f"Error al eliminar: {err}")
                    mostrar_snackbar(f"Error al eliminar la palabra: {err}")

                actualizar_diccionario()  # Actualizar la lista después de borrar
            page.dialog.open = False
            page.update()

        # Diálogo de confirmación
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Borrado"),
            content=ft.Text(f"¿Estás seguro de que quieres eliminar la palabra '{palabra}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=confirmar_borrado, data="Cancelar"),
                ft.TextButton("Eliminar", on_click=confirmar_borrado, data="Eliminar"),
            ]
        )
        page.dialog.open = True
        page.update()

    # Función para editar una palabra
    def editar_palabra(palabra, definicion, categoria):
        nonlocal palabra_editando
        palabra_input.value = palabra
        definicion_input.value = definicion
        categoria_input.value = categoria
        palabra_editando = palabra
        page.update()

    # Configurar los eventos de los inputs
    buscador_input.on_change = buscar_palabra

    # Crear la interfaz scrollable
    scrollable_results = ft.Column(
        controls=[
            ft.Row([
                buscador_input,
                ft.IconButton(ft.icons.CLEAR, on_click=limpiar_buscador, tooltip="Limpiar búsqueda")
            ], alignment=ft.MainAxisAlignment.CENTER),
            resultados_column
        ],
        height=700,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    # Crear los botones
    boton_guardar = ft.ElevatedButton(
        "Guardar", on_click=guardar_diccionario, tooltip="Guardar la palabra y definición en el diccionario"
    )
    boton_exportar_pdf = ft.ElevatedButton(
        "Exportar Diccionario a PDF", on_click=lambda e: exportar_a_pdf(page), tooltip="Exportar el diccionario como archivo PDF"
    )

    # Organizar los botones en una fila
    fila_botones = ft.Row(controls=[boton_guardar, boton_exportar_pdf], alignment=ft.MainAxisAlignment.CENTER)

    # Devolver la estructura general
    return ft.Column([
        espacio_extra,
        ft.Row([palabra_input, definicion_input], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([categoria_input], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        fila_botones,
        ft.Divider(),
        scrollable_results
    ], expand=True)
