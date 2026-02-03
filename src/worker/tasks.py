# Worker
from celery import Celery
import time

from src.shared.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

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
@celery_app.task(name='process_file')
def process_file(filename):
    print(f"Iniciando el procesamiento del archivo: {filename}")
    
    # Simulando una tarea que toma tiempo
    time.sleep(10)

    print(f"Tarea terminada para el archivo: {filename}")

    return 'OK'
