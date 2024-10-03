import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import sys

# Función para cargar el ícono desde un archivo de imagen
def cargar_icono_desde_archivo(ruta_icono):
    # Cargar la imagen del archivo
    return Image.open(ruta_icono)

# Función para salir de la aplicación
def salir(icon, item):
    icon.stop()  # Detener el icono de la bandeja
    sys.exit(0)  # Cerrar la aplicación completamente

# Función para iniciar el ícono en la bandeja del sistema
def iniciar_icono_bandeja():
    # Ruta del icono (ajustar si es necesario)
    ruta_icono = "resources/icono.png"
    
    # Cargar el ícono desde el archivo
    icon_image = cargar_icono_desde_archivo(ruta_icono)
    
    # Crear el menú del ícono
    menu = (item('Salir', salir),)  # Solo una opción de salir
    
    # Crear el objeto Icon con el menú
    icon = pystray.Icon("test_icon", icon_image, "Mi Aplicación", menu)
    
    # Iniciar el ícono en un hilo separado
    icon.run()  # Cambiar a run() directamente sin un hilo adicional

# Esto se llamará desde el main.py
