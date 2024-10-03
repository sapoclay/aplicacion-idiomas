import sqlite3
from sqlite3 import Error
import flet as ft
import traceback

# Función para mostrar snackbar de error
def mostrar_snackbar(page, mensaje):
    snackbar = ft.SnackBar(ft.Text(mensaje))
    snackbar.open = True
    page.add(snackbar)
    page.update()

# Función para obtener el mensaje de error detallado
def mostrar_error_completo(e):
    return f"{e}\n{traceback.format_exc()}"

# Crear base de datos y tablas si no existen
def crear_base_de_datos(page=None):
    conn = None
    try:
        conn = sqlite3.connect("diccionario.db")
        cursor = conn.cursor()
        
        # Crear tablas si no existen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diccionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                palabra TEXT,
                definicion TEXT,
                categoria TEXT  
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
                url TEXT NOT NULL
            )
        """)
        conn.commit()
        print("Base de datos y tablas creadas.")
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al crear la base de datos: {mostrar_error_completo(e)}")
    finally:
        if conn:
            conn.close()

# Conexión a la base de datos diccionario.db
def get_db_connection():
    try:
        return sqlite3.connect("diccionario.db")
    except Error as e:
        print(mostrar_error_completo(e))
        return None

# Función para insertar una nueva palabra con su definición y categoría
def insert_diccionario(palabra, definicion, categoria, page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO diccionario (palabra, definicion, categoria) VALUES (?, ?, ?)", (palabra, definicion, categoria))
        conn.commit()
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al insertar palabra: {mostrar_error_completo(e)}")
    finally:
        if conn:
            conn.close()

# Función para recuperar todas las palabras con su definición y categoría
def get_diccionario(page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT palabra, definicion, categoria FROM diccionario ORDER BY palabra ASC")  # Incluye categoría
        palabras = cursor.fetchall()
        return palabras
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al recuperar palabras: {mostrar_error_completo(e)}")
        return []
    finally:
        if conn:
            conn.close()

# Eliminar una palabra de la base de datos
def eliminar_palabra_de_db(palabra, page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diccionario WHERE palabra = ?", (palabra,))
        conn.commit()
        return True  # Indica que la operación fue exitosa
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al eliminar la palabra: {mostrar_error_completo(e)}")
        return False  # Indica que hubo un error
    finally:
        if conn:
            conn.close()

# Función para actualizar una palabra existente en el diccionario
def actualizar_palabra_en_db(palabra_antigua, nueva_palabra, nueva_definicion, nueva_categoria, page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE diccionario 
            SET palabra = ?, definicion = ?, categoria = ? 
            WHERE palabra = ?
        """, (nueva_palabra, nueva_definicion, nueva_categoria, palabra_antigua))
        conn.commit()
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al actualizar palabra: {mostrar_error_completo(e)}")
    finally:
        if conn:
            conn.close()

# Funciones para Traducción
def insert_traduccion(texto_original, texto_traducido, page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO traduccion (texto_original, texto_traducido) VALUES (?, ?)", (texto_original, texto_traducido))
        conn.commit()
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al insertar traducción: {mostrar_error_completo(e)}")
    finally:
        if conn:
            conn.close()

def get_traduccion(page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT texto_original, texto_traducido FROM traduccion")
        resultados = cursor.fetchall()
        return resultados
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al recuperar traducciones: {mostrar_error_completo(e)}")
        return []
    finally:
        if conn:
            conn.close()

# Funciones para Listening

def guardar_url(nombre, url, page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO listening (nombre, url) VALUES (?, ?)", (nombre, url))
        conn.commit()
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al guardar la URL: {mostrar_error_completo(e)}")
    finally:
        if conn:
            conn.close()

def cargar_urls(page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, url FROM listening ORDER BY nombre ASC")
        urls = cursor.fetchall()
        return urls
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al cargar las URL guardadas: {mostrar_error_completo(e)}")
        return []  # Asegúrate de devolver una lista vacía en caso de error
    finally:
        if conn:
            conn.close()

# Eliminar una URL por ID
def eliminar_url(id, page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM listening WHERE id = ?", (id,))
        conn.commit()
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al borrar la URL: {mostrar_error_completo(e)}")
    finally:
        if conn:
            conn.close()

# Actualizar una URL por ID
def actualizar_url(id, nuevo_nombre, nueva_url, page=None):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE listening SET nombre = ?, url = ? WHERE id = ?", (nuevo_nombre, nueva_url, id))
        conn.commit()
    except Error as e:
        print(mostrar_error_completo(e))
        if page:
            mostrar_snackbar(page, f"Error al actualizar la URL: {mostrar_error_completo(e)}")
    finally:
        if conn:
            conn.close()
