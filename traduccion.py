import flet as ft
import requests
from gtts import gTTS
import subprocess
import sys
import os

# Función para usar la API de MyMemory
def traducir_mymemory(texto, idioma_origen, idioma_destino):
    url = "https://api.mymemory.translated.net/get"
    
    params = {
        'q': texto,
        'langpair': f'{idioma_origen}|{idioma_destino}'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanza un error para respuestas no exitosas
        data = response.json()
        return data['responseData']['translatedText']
    except requests.exceptions.RequestException as e:
        return f"Error al traducir: {str(e)}"

def reproducir_audio(archivo_audio):
    try:
        if sys.platform.startswith('win'):
            os.startfile(archivo_audio)  # Windows
        elif sys.platform.startswith('darwin'):
            subprocess.call(['open', archivo_audio])  # macOS
        else:
            subprocess.call(['xdg-open', archivo_audio])  # Linux
    except Exception as e:
        return f"Error al reproducir audio: {str(e)}"

def mostrar_snackbar(page, mensaje):
    page.snackbar = ft.SnackBar(ft.Text(mensaje), open=True)
    page.add(page.snackbar)  # Añadir el SnackBar a la página
    page.update()

def traduccion_tab(page):
    espacio_extra = ft.Container(height=20)
    
    # TextField para el texto original
    texto_original_input = ft.TextField(
        label="Texto a traducir",
        multiline=True,
        min_lines=10,
        max_lines=20,
        width=500,
    )

    # Opciones con iconos de banderas
    opciones_idiomas = [
        ft.dropdown.Option(
            key="es", 
            text="Español", 
            content=ft.Row([ft.Image(src="resources/espana.png", width=20), ft.Text("Español")])
        ),
        ft.dropdown.Option(
            key="en", 
            text="Inglés", 
            content=ft.Row([ft.Image(src="resources/reino-unido.png", width=20), ft.Text("Inglés")])
        ),
        ft.dropdown.Option(
            key="fr", 
            text="Francés", 
            content=ft.Row([ft.Image(src="resources/francia.png", width=20), ft.Text("Francés")])
        ),
        ft.dropdown.Option(
            key="pt", 
            text="Portugués", 
            content=ft.Row([ft.Image(src="resources/portugal.png", width=20), ft.Text("Portugués")])
        ),
        ft.dropdown.Option(
            key="de", 
            text="Alemán", 
            content=ft.Row([ft.Image(src="resources/alemania.png", width=20), ft.Text("Alemán")])
        ),
    ]

    # Desplegables para los idiomas de origen y destino
    idioma_origen_input = ft.Dropdown(
        options=opciones_idiomas,
        label="Idioma de origen",
        value="es",  # Valor por defecto
        width=150,
    )

    idioma_destino_input = ft.Dropdown(
        options=opciones_idiomas,
        label="Idioma de destino",
        value="en",  # Valor por defecto
        width=150,
    )

    # Botón para intercambiar idiomas
    def intercambiar_idiomas(e):
        idioma_origen = idioma_origen_input.value
        idioma_destino = idioma_destino_input.value
        idioma_origen_input.value = idioma_destino
        idioma_destino_input.value = idioma_origen
        texto_traducido_input.value, texto_original_input.value = texto_original_input.value, texto_traducido_input.value
        page.update()  # Actualiza la página para reflejar los cambios

    # Botón para intercambiar idiomas
    boton_intercambiar = ft.IconButton(
        icon=ft.icons.SWAP_HORIZ,
        on_click=intercambiar_idiomas,
        tooltip="Intercambiar Idiomas"
    )

    # TextField para el texto traducido
    texto_traducido_input = ft.TextField(
        label="Texto traducido",
        multiline=True,
        min_lines=10,
        max_lines=20,
        width=500,
    )
    
    def leer_texto_traducido(e):
        texto_traducido = texto_traducido_input.value
        idioma_destino = idioma_destino_input.value
        
        if texto_traducido:  # Verifica que hay texto para leer
            try:
                tts = gTTS(text=texto_traducido, lang=idioma_destino)
                audio_file = "traduccion.mp3"
                tts.save(audio_file)  # Guarda el archivo de audio
                reproducir_audio(audio_file)  # Reproduce el audio
            except Exception as e:
                mostrar_snackbar(page, f"Error al leer la traducción: {str(e)}")

    # Función para traducir el texto
    def traducir_texto(e):
        texto_original = texto_original_input.value.strip()
        if not texto_original:  # Verifica si el campo de texto está vacío
            mostrar_snackbar(page, "Por favor, ingresa un texto para traducir.")
            return  # Sale de la función si el campo está vacío

        idioma_origen = idioma_origen_input.value
        idioma_destino = idioma_destino_input.value
        
        # Llamar a la API de MyMemory
        traduccion = traducir_mymemory(texto_original, idioma_origen, idioma_destino)
        
        # Si hay un error, mostrarlo
        if "Error" in traduccion:
            mostrar_snackbar(page, traduccion)
        else:
            # Mostrar el resultado en el cuadro de texto traducido
            texto_traducido_input.value = traduccion
            page.update()

    # Función para borrar el texto
    def borrar_texto(e):
        texto_original_input.value = ""
        texto_traducido_input.value = ""
        page.update()
        
    # Botones de acción
    boton_traducir = ft.ElevatedButton(text="Traducir", on_click=traducir_texto, tooltip="Traducir Texto")
    boton_borrar = ft.ElevatedButton(text="Borrar", on_click=borrar_texto, tooltip="Borrar Campos")
    boton_leer = ft.ElevatedButton(text="Leer Traducción", on_click=leer_texto_traducido, tooltip="Leer Texto Traducido")
    
    # Diseño de la pestaña con los elementos organizados
    return ft.Column([
        espacio_extra,
        ft.Column(
            [
                texto_original_input,  # Texto original en la primera línea
                ft.Row(
                    [idioma_origen_input, boton_intercambiar, idioma_destino_input], alignment=ft.MainAxisAlignment.CENTER
                ),
                texto_traducido_input,  # Texto traducido en la tercera línea
                ft.Row(
                    [boton_traducir, boton_borrar, boton_leer],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    ])
