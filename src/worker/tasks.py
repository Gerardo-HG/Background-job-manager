# Worker
from celery import Celery
import time

# Importando configuraciones y funcionalidades
from src.shared.config import config
from src.shared.file_utils import words_count, save_result, allowed_file

# 1. Inicializando la aplicación Celery
celery_app = Celery(
    'worker',
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_RESULT_BACKEND
)

# 2. Configuración adicional
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# 3. Tarea de procesamiento
@celery_app.task(bind=True, name='process_file')
def process_file(self,  filename):
    print(f"Iniciando el procesamiento del archivo: {filename}")
    
    # Verificamos si el archivo a procesar es uno permitido
    allowed = allowed_file(filename)

    if not allowed:
        raise ValueError(f"Extensión no permitida para el archivo: {filename}")

    try:
        count = words_count(filename)

        # Estructura del resultado
        result = {
            'id': self.request.id,
            'status':'SUCCESS',
            'word_count': count
        }

        # Persistencia en JSON
        save_result(self.request.id, result)

        return result

    except FileNotFoundError:
        error_msg = f"El archivo no se encontró en la ruta: {filename}"
        print(f"Error: {error_msg}")
        raise Exception(error_msg)


    except Exception as e:
        error_msg = f"Error inesperado al procesar el archivo: {str(e)}"
        print(f"Error: {error_msg}")
        raise Exception(error_msg)
