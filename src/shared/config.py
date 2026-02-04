# Centralizar rutas, URLs de conexión y configuraciones de seguridad
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

class Config:

    # Ruta del Sistema
    PATH_BASE = os.path.abspath(os.getcwd())

    # Configuración de Celery
    CELERY_BROKER_URL = os.getenv("REDIS_URL", None)
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", None)

    # Gestión de Archivos
    UPLOAD_FOLDER_PATH = os.path.join(PATH_BASE,'uploads')
    PROCESSED_FOLDER_PATH = os.path.join(PATH_BASE,'processed')

    # Filtro y Seguridad
    ALLOWED_EXTENSION_FILES = {'.json','.txt','.pdf', '.rtf'}
    MAX_CONTENT_LENGTH = 16*1024*1024


    @classmethod
    def init_directories(cls):
        """Crea las carpetas necesarias si no existen al arrancar la app"""
        for path in [cls.UPLOAD_FOLDER_PATH, cls.PROCESSED_FOLDER_PATH]:
            if not os.path.exists(path):
                os.makedirs(path)





config = Config()

if __name__ == "__main__":
    print("Ejecutando config.py")
