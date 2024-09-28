import os
import subprocess
import sys
import platform

def crear_entorno_virtual():
    """Crear el entorno virtual si no existe."""
    if not os.path.exists("venv"):
        print("Creando entorno virtual...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])

def instalar_dependencias():
    """Instalar las dependencias si es necesario."""
    print("Instalando dependencias...")
    pip_executable = os.path.join("venv", "Scripts", "pip") if platform.system() == "Windows" else os.path.join("venv", "bin", "pip")
    subprocess.check_call([pip_executable, "install", "--upgrade", "pip"])  # Actualiza pip primero
    subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])
    
    # Asegúrate de actualizar flet
    subprocess.check_call([pip_executable, "install", "--upgrade", "flet"])

def ejecutar_aplicacion():
    """Ejecutar la aplicación en el entorno virtual."""
    print("Ejecutando aplicación...")
    python_executable = os.path.join("venv", "Scripts", "python") if platform.system() == "Windows" else os.path.join("venv", "bin", "python")
    subprocess.run([python_executable, "main.py"], check=True)

if __name__ == "__main__":
    crear_entorno_virtual()

    if not os.path.exists("requirements.txt"):
        with open("requirements.txt", "w") as f:
            f.write("flet\nfpdf\nrequests\ngTTS\nPillow\npystray\n")

    instalar_dependencias()
    ejecutar_aplicacion()
