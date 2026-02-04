# Worker
from celery import Celery
import time

# Importando configuraciones y funcionalidades
from src.shared.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from src.shared.file_utils import read_json_file, save_result


# 1. Inicializando la aplicación Celery
celery_app = Celery(
    'worker',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# 2. Configuración adicional
celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# 3. Creando una tarea de ejemplo
@celery_app.task(bind=True, name='process_file')
def process_file(self,  filename):
    print(f"Iniciando el procesamiento del archivo: {filename}")
    
    # Leer el archivo y contar palabras
    content = read_json_file(filename)

    # Verificamos si la lectura tuvo un error
    if content['status'] == 'error':
        print(f"Error al leer el archiv: {content.get('message')}")
    
        # Guardamos el resultado con estado de error
        save_result(self.request.id, content)
        return 'READING_ERROR'

    # Si la lectura fue exitosa, preparamos el resultado
    result = {
        'task_id': self.request.id,
        'status': content.get('status'),
        'word_count': content.get('words')
    }

    # Intentamos guardar el resultado
    try:
        save_result(self.request.id, result)
    except Exception as e:
        print(f"Error al guardar el resultado: {str(e)}")
        return 'SAVING_ERROR'
    
    return 'OK'
