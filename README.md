# Aplicación Idiomas

![Aplicacion-idiomas](https://github.com/user-attachments/assets/42dba7d1-df5a-493b-9a03-83ea0a6c7e2c)

Esta es una aplicación de escritorio diseñada para ayudar a almacenar y gestionar vocabulario en diferentes idiomas. Permite a los usuarios guardar palabras o frases, sus definiciones o traducciones, y ofrece funcionalidades de búsqueda y exportación a PDF.

## Características

- **Gestión de Vocabulario**: Añade, edita y elimina palabras o frases junto con sus definiciones y categorías.
- **Traducción**: Herramienta integrada para traducir texto. Utiliza la API mymemory para funcionar. Tiene ciertas limitaciones diarias.
- **Listening**: Funcionalidades para gestionar recursos de escucha o de visualización.
- **Exportación**: Exporta el vocabulario almacenado a un archivo PDF.
- **Interfaz de Usuario Amigable**: Esta aplicación utiliza Flet para intentar ofrecer al usuario una experiencia interactiva agradable.
- **Permite cambiar el tema**: En la pestaña opciones, se puede cambiar el tema del oscuro (por defecto) a otro claro.

## Requisitos

- **Python 3.8 o superior**: Es imprescindible tener Python instalado en tu sistema.

## Instalación

1. **Clona el repositorio**:
   ```
   git clone https://github.com/sapoclay/aplicacion-idiomas
   cd aplicacion-idiomas
   ```

    Ejecuta el script para iniciar la aplicación:

    ```
    python run_app.py
    ```

Este script creará un entorno virtual, instalará automáticamente todas las dependencias necesarias (excepto Python) y ejecutará la aplicación.

### Dependencias

El proyecto utiliza las siguientes librerías, que se instalarán automáticamente:

    - flet: Para la creación de la interfaz de usuario.
    - fpdf: Para la generación de archivos PDF.
    - requests: Para realizar solicitudes HTTP.
    - gTTS: Para convertir texto a voz.
    - Pillow: Para el manejo de imágenes.
    - pystray: Para añadir un icono en la bandeja del sistema. (Pendiente)

Uso

    Abre la aplicación y navega a las diferentes pestañas: Vocabulario, Traducción, Listening y Opciones.
    Para gestionar el vocabulario, ve a la pestaña "Vocabulario" y utiliza los campos para añadir, buscar o editar palabras.
    En la pestaña "Opciones", puedes cambiar el tema y ver información sobre la aplicación.

### Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar esta aplicación, por favor abre un problema o envía un pull request.
Licencia

Este proyecto está bajo la licencia MIT.
