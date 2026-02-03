# Servidor Web API principal
from flask import Flask, jsonify, request

# Seguridad de archivos
from werkzeug.utils import secure_filename

# Ruta de acceso al sistema operativo
import os

# 1. Inicializando la aplicación Flask
app = Flask(__name__)

# 2. Definiendo rutas absolutas
UPLOAD_FOLDER = os.path.join(os.getcwd(),'uploads')

#3. Si la carpeta UPLOAD_FOLDER no existe se crea
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 4. Configuración de la aplicación
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = True

# 5. Definiendo una ruta de prueba
@app.route('/', methods=["GET"])
def health_check():
    return jsonify(
        {'estado':'El servidor está vivo'}
    ), 200

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
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    file.save(file_path)
    print(f"Archivo guardado en: {file_path}")

    return jsonify(
        {
            'mensaje':'Archivo subido exitosamente'
        }
    ), 200


if __name__ == '__main__':
    app.run(debug=True)
    