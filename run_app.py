import os
import subprocess
import sys
import venv
import urllib.request

# Ruta del entorno virtual
venv_dir = os.path.join(os.getcwd(), "venv")

def crear_entorno_virtual():
    """Crea el entorno virtual si no existe."""
    if not os.path.isdir(venv_dir):
        print("Creando entorno virtual...")
        venv.create(venv_dir, with_pip=False)  # No habilitamos pip aquí
        print("Entorno virtual creado.")
    else:
        print("Entorno virtual ya existe.")

def instalar_pip_si_no_existe():
    """Instala pip manualmente si no está presente en el entorno virtual."""
    pip_executable = os.path.join(venv_dir, "bin", "pip") if os.name != 'nt' else os.path.join(venv_dir, "Scripts", "pip.exe")
    
    if not os.path.isfile(pip_executable):
        print("pip no encontrado, descargando e instalando pip...")
        
        # Descargar el script get-pip.py
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_script = os.path.join(venv_dir, "get-pip.py")
        
        try:
            urllib.request.urlretrieve(get_pip_url, get_pip_script)
            # Instalar pip utilizando el script descargado
            python_executable = os.path.join(venv_dir, "bin", "python") if os.name != 'nt' else os.path.join(venv_dir, "Scripts", "python.exe")
            subprocess.check_call([python_executable, get_pip_script])
            print("pip instalado exitosamente.")
        except Exception as e:
            print(f"Error al intentar instalar pip: {e}")
            sys.exit(1)
    return pip_executable

def instalar_dependencias():
    """Instala las dependencias en el entorno virtual."""
    # Verifica si pip está disponible e instálalo si no está presente
    pip_executable = instalar_pip_si_no_existe()

    # Actualizar pip, setuptools y wheel
    print("Actualizando pip, setuptools, y wheel...")
    subprocess.check_call([pip_executable, "install", "--upgrade", "pip", "setuptools", "wheel"])
    
    # Instalar dependencias del archivo requirements.txt
    print("Instalando dependencias desde requirements.txt...")
    subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])

def ejecutar_aplicacion():
    """Ejecuta la aplicación dentro del entorno virtual."""
    python_executable = os.path.join(venv_dir, "bin", "python") if os.name != 'nt' else os.path.join(venv_dir, "Scripts", "python.exe")
    
    print("Ejecutando la aplicación...")
    subprocess.run([python_executable, "main.py"], check=True)

if __name__ == "__main__":
    try:
        # Crear el entorno virtual si no existe
        crear_entorno_virtual()
        
        # Instalar dependencias
        instalar_dependencias()
        
        # Ejecutar la aplicación
        ejecutar_aplicacion()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
