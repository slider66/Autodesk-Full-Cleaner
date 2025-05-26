import os
import shutil
import subprocess
import sys
import ctypes
import logging
from datetime import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def setup_logging():
    log_filename = f"autodesk_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    return log_filename

def eliminar_archivo_seguro(ruta):
    try:
        if os.path.isfile(ruta):
            os.remove(ruta)
        elif os.path.isdir(ruta):
            shutil.rmtree(ruta)
        return True
    except Exception:
        return False

def limpiar_carpeta_temp(carpeta):
    """Limpia archivos de Autodesk en la carpeta temp sin intentar eliminar archivos en uso"""
    if not os.path.exists(carpeta):
        return

    for elemento in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, elemento)
        try:
            if "autodesk" in elemento.lower():
                if eliminar_archivo_seguro(ruta_completa):
                    logging.info(f"Elemento eliminado: {ruta_completa}")
                else:
                    logging.warning(f"No se pudo eliminar: {ruta_completa}")
        except Exception as e:
            logging.error(f"Error al procesar {ruta_completa}: {e}")

def eliminar_carpeta(carpeta):
    if not os.path.exists(carpeta):
        logging.info(f"La carpeta no existe: {carpeta}")
        return

    # Manejo especial para la carpeta Temp
    if "Temp" in carpeta:
        limpiar_carpeta_temp(carpeta)
        return

    try:
        shutil.rmtree(carpeta)
        logging.info(f"Carpeta eliminada: {carpeta}")
    except Exception as e:
        logging.error(f"Error al eliminar la carpeta {carpeta}: {e}")

def eliminar_clave_registro(ruta_registro):
    try:
        # Separar la ruta en componentes
        partes = ruta_registro.split('\\', 1)
        if len(partes) != 2:
            logging.error(f"Formato de ruta de registro inválido: {ruta_registro}")
            return

        hkey, subruta = partes

        # Usar reg.exe con argumentos separados y sin shell=True
        comando = ['reg', 'delete', ruta_registro, '/f']
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            shell=False  # Importante: shell=False para mejor seguridad
        )

        if resultado.returncode == 0:
            logging.info(f"Clave de registro eliminada: {ruta_registro}")
        else:
            logging.error(f"Error al eliminar la clave del registro {ruta_registro}: {resultado.stderr.strip()}")
    except Exception as e:
        logging.error(f"Error inesperado al eliminar la clave del registro {ruta_registro}: {e}")

def main():
    if not is_admin():
        logging.error("Este script requiere privilegios de administrador.")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        except Exception as e:
            logging.error(f"Error al intentar ejecutar como administrador: {e}")
        sys.exit(1)

    # Carpetas relacionadas con Autodesk
    carpetas = [
        r"C:\Program Files\Autodesk",
        r"C:\Program Files (x86)\Autodesk",
        r"C:\ProgramData\Autodesk",
        os.path.expandvars(r"%AppData%\Autodesk"),
        os.path.expandvars(r"%LocalAppData%\Autodesk"),
        os.path.expandvars(r"%UserProfile%\Documents\Autodesk"),
        r"C:\Users\Public\Documents\Autodesk",
        r"C:\Users\Public\Autodesk",
        os.path.expandvars(r"%Temp%")
    ]

    # Claves de registro relacionadas con Autodesk
    claves_registro = [
        r"HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk",
        r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Autodesk",
        r"HKEY_CURRENT_USER\SOFTWARE\Autodesk",
        r"HKEY_CLASSES_ROOT\Autodesk"
    ]

    print("\n¡ADVERTENCIA!")
    print("Este script eliminará todos los archivos y registros relacionados con Autodesk.")
    print("Se recomienda hacer una copia de seguridad antes de continuar.")
    confirmacion = input("\n¿Desea continuar? (s/N): ").lower()

    if confirmacion != 's':
        logging.info("Operación cancelada por el usuario.")
        sys.exit(0)

    # Eliminar carpetas
    logging.info("Iniciando eliminación de carpetas...")
    for carpeta in carpetas:
        eliminar_carpeta(carpeta)

    # Eliminar claves de registro
    logging.info("Iniciando eliminación de claves de registro...")
    for clave in claves_registro:
        eliminar_clave_registro(clave)

    logging.info("Proceso de limpieza completado.")
    print(f"\nProceso completado. Puede revisar el registro de operaciones en el archivo: {log_filename}")

if __name__ == "__main__":
    log_filename = setup_logging()
    main()