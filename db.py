import sqlite3
from sqlite3 import Error
import flet as ft

# Conexión a la base de datos SQLite
def crear_base_de_datos(page=None):
    try:
        conn = sqlite3.connect("diccionario.db")
        cursor = conn.cursor()
        
        # Crear tablas si no existen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diccionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                palabra TEXT,
                definicion TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS traduccion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto_original TEXT,
                texto_traducido TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS listening (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nombre TEXT NOT NULL,
                      url TEXT NOT NULL)
        """)
        conn.commit()
        print("Base de datos y tablas creadas.")
        conn.close()
    except Error as e:
        print(f"Error: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al crear la base de datos: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()

# Conexión a la base de datos diccionario.db
def get_db_connection():
    try:
        return sqlite3.connect("diccionario.db")
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Funciones para Diccionario
def insert_diccionario(palabra, definicion, page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO diccionario (palabra, definicion) VALUES (?, ?)", (palabra, definicion))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error al insertar palabra: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al insertar palabra: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()

def get_diccionario(page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT palabra, definicion FROM diccionario ORDER BY palabra ASC")  # Orden alfabético
        palabras = cursor.fetchall()
        conn.close()
        return palabras
    except Error as e:
        print(f"Error al recuperar palabras: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al recuperar palabras: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()
        return []

def eliminar_palabra_de_db(palabra, page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diccionario WHERE palabra = ?", (palabra,))
        conn.commit()
        conn.close()
        return True  # Indica que la operación fue exitosa
    except Error as e:
        print(f"Error al eliminar la palabra: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al eliminar la palabra: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()
        return False  # Indica que hubo un error

# Función para actualizar una palabra existente en el diccionario
def actualizar_palabra_en_db(palabra_antigua, nueva_palabra, nueva_definicion, page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE diccionario 
            SET palabra = ?, definicion = ? 
            WHERE palabra = ?
        """, (nueva_palabra, nueva_definicion, palabra_antigua))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error al actualizar palabra: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al actualizar palabra: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()

# Funciones para Traducción
def insert_traduccion(texto_original, texto_traducido, page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO traduccion (texto_original, texto_traducido) VALUES (?, ?)", (texto_original, texto_traducido))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error al insertar traducción: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al insertar traducción: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()

def get_traduccion(page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT texto_original, texto_traducido FROM traduccion")
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    except Error as e:
        print(f"Error al recuperar traducciones: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al recuperar traducciones: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()
        return []

# Funciones para Listening

def guardar_url(nombre, url, page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO listening (nombre, url) VALUES (?, ?)", (nombre, url))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al guardar la URL: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()

# Función para recuperar las URLs de la base de datos
def cargar_urls(page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, url FROM listening ORDER BY nombre ASC")
        urls = cursor.fetchall()
        conn.close()
        return urls
    except Error as e:
        print(f"Error: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al cargar las URL guardadas: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()
        return []  # Asegúrate de devolver una lista vacía en caso de error


# Eliminar una URL por ID
def eliminar_url(id, page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM listening WHERE id = ?", (id,))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al borrar la URL: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()
    

# Actualizar una URL por ID
def actualizar_url(id, nuevo_nombre, nueva_url, page=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE listening SET nombre = ?, url = ? WHERE id = ?", (nuevo_nombre, nueva_url, id))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error: {e}")
        if page:
            page.snackbar = ft.SnackBar(ft.Text(f"Error al actualizar la URL: {str(e)}"))
            page.snackbar.open = True
            page.add(page.snackbar)
            page.update()