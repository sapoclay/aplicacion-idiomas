import flet as ft
from db import insert_diccionario, get_diccionario, eliminar_palabra_de_db, actualizar_palabra_en_db
from exportar_diccionario import exportar_a_pdf

def diccionario_tab(page):
    espacio_extra = ft.Container(height=20)
    palabra_input = ft.TextField(label="Palabra/Frase", multiline=True, min_lines=5, max_lines=20, width=400,)
    definicion_input = ft.TextField(label="Definición/Traducción",  multiline=True, min_lines=5, max_lines=20, width=400,)
    buscador_input = ft.TextField(label="Buscar", width=400)
    resultados_column = ft.Column(spacing=10)

    # Variable para controlar el modo de edición
    palabra_editando = None

    def guardar_diccionario(e):
        nonlocal palabra_editando  # Accedemos a la variable de modo edición

        if not palabra_input.value.strip():
            page.snackbar = ft.SnackBar(ft.Text("El campo 'Palabra' es obligatorio."))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()
            return

        if not definicion_input.value.strip():
            page.snackbar = ft.SnackBar(ft.Text("El campo 'Definición' es obligatorio."))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()
            return

        try:
            if palabra_editando:  # Si estamos en modo edición
                actualizar_palabra_en_db(palabra_editando, palabra_input.value, definicion_input.value)
                page.snackbar = ft.SnackBar(ft.Text("Palabra actualizada con éxito."))
            else:  # Si es una nueva palabra
                insert_diccionario(palabra_input.value, definicion_input.value)
                page.snackbar = ft.SnackBar(ft.Text("Palabra guardada con éxito."))

            palabra_input.value = ""
            definicion_input.value = ""
            palabra_editando = None  # Reiniciar el modo edición

            page.snackbar.open = True
            page.add(page.snackbar)
            actualizar_diccionario()
            page.update()
        except Exception as e:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al guardar: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()

    def actualizar_diccionario(busqueda=""):
        palabras = get_diccionario(page)
        resultados_column.controls.clear()

        if busqueda:
            palabras = [p for p in palabras if busqueda.lower() in p[0].lower() or busqueda.lower() in p[1].lower()]

        resultados_column.controls.append(ft.Row([
            ft.Text("Palabra", weight="bold", expand=True),
            ft.Text("Definición", weight="bold", expand=True),
            ft.Text("Acciones", weight="bold", width=100)
        ], alignment=ft.MainAxisAlignment.CENTER))

        for palabra, definicion in palabras:
            resultados_column.controls.append(ft.Row([
                ft.Text(palabra, expand=True),
                ft.Text(definicion, expand=True),
                ft.Row([
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, p=palabra: borrar_palabra(p)),
                    ft.IconButton(ft.icons.EDIT, on_click=lambda e, p=palabra, d=definicion: editar_palabra(p, d))
                ], alignment=ft.MainAxisAlignment.END)
            ], alignment=ft.MainAxisAlignment.CENTER))

        page.update()

    actualizar_diccionario()

    def buscar_palabra(e):
        actualizar_diccionario(buscador_input.value)

    def limpiar_buscador(e):
        buscador_input.value = ""
        page.update()
        actualizar_diccionario()

    def borrar_palabra(palabra):
        def confirmar_borrado(e):
            if e.control.data == "Eliminar":
                if eliminar_palabra_de_db(palabra):
                    # Crear el SnackBar con el mensaje de éxito
                    page.snackbar = ft.SnackBar(ft.Text(f"Palabra '{palabra}' eliminada."), open=True)
                else:
                    # Crear el SnackBar con el mensaje de error
                    page.snackbar = ft.SnackBar(ft.Text(f"Error al eliminar la palabra '{palabra}'."), open=True)
                
                # Asegurarse de añadir el SnackBar a la página y abrirlo
                page.add(page.snackbar)
                page.update()  # Actualiza la página para mostrar el SnackBar
                
                # Actualizar el listado del diccionario
                actualizar_diccionario()

            # Cerrar el diálogo
            page.dialog.open = False
            page.update()  # Actualizar la página para reflejar el cierre del diálogo

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
        page.update()  # Actualiza la página para abrir el diálogo



    def editar_palabra(palabra, definicion):
        nonlocal palabra_editando
        palabra_input.value = palabra
        definicion_input.value = definicion
        palabra_editando = palabra  # Guardamos la palabra que estamos editando
        page.update()

    buscador_input.on_change = buscar_palabra

    scrollable_results = ft.Column(
        controls=[
            ft.Row([
                buscador_input,
                ft.IconButton(ft.icons.CLEAR, on_click=limpiar_buscador, tooltip="Limpiar búsqueda")
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Column(
                controls=[resultados_column],
                height=700,
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )
        ],
        spacing=30
    )
    
    # Crear los botones con tooltips
    boton_guardar = ft.ElevatedButton(
        "Guardar", 
        on_click=guardar_diccionario,
        tooltip="Guardar la palabra y definición en el diccionario"
    )

    boton_exportar_pdf = ft.ElevatedButton(
        "Exportar Diccionario a PDF", 
        on_click=lambda e: exportar_a_pdf(page),
        tooltip="Exportar el diccionario como archivo PDF"
    )

    # Organizar los botones en un Row
    fila_botones = ft.Row(controls=[boton_guardar, boton_exportar_pdf], alignment=ft.MainAxisAlignment.CENTER)

    return ft.Column([
        espacio_extra,
        ft.Row(
               [palabra_input,definicion_input],
               alignment=ft.MainAxisAlignment.CENTER
        ),        
        fila_botones,  # Añadir la fila de botones aquí
        ft.Divider(),
        scrollable_results
    ], expand=True)
