# Servidor Web API principal
from flask import Flask, jsonify, request, render_template

# Seguridad de archivos
from werkzeug.utils import secure_filename

# Ruta de acceso al sistema operativo
import os

# Importación de Módulos
from src.worker.tasks import process_file, celery_app
from celery.result import AsyncResult
from src.shared.config import config
from src.shared.job_tracker import JobTracker

# 1. Inicializando la aplicación Flask
app = Flask(__name__)

# 2. Inicilizando Config
config.init_directories()

# 4. Configuración de la aplicación
app.config.update(
    UPLOAD_FOLDER = config.UPLOAD_FOLDER_PATH,
    MAX_CONTENT_LENGTH = config.MAX_CONTENT_LENGTH,
    DEBUG = True
)


# 5. Definiendo las rutas de la APIS
@app.route('/', methods=["GET"])
def health_check():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({
            'error':'No se envió parte del archivo'
        }),400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify(
            {
                'error':'No se seleccionó ningún archivo'
            }
        ),400
    
    file_sec = secure_filename(file.filename)
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file_sec)
    
    file.save(filename)
    print(f"Archivo guardado en: {filename}")

    # Llamando a la tarea asíncrona
    async_task = process_file.delay(filename)

    return jsonify(
        {
            'mensaje':'Archivo subido exitosamente',
            "job_id": async_task.id
        }
    ), 200

@app.route('/status/<job_id>', methods=['GET'])
def get_status_by_id(job_id):
    # Conectamos con el backend de resultado usando el ID
    tracker = JobTracker(job_id)

    response = tracker.get_status()

    return jsonify(response),200