# Utilidades 
import json
import os

# Importación de módulos
from src.shared.config import config


def allowed_file(filename):
    """
    Verifica si la extensión del archivo está permitido
    """

    # Validación Inicial
    if not filename or filename.strip() == "":
        return False
    
    # Extraer la extensión de forma segura
    _, extension = os.path.splitext(filename)
    extension = extension.lower()

    # Comparar si es una extensión permitida en el set de config
    return extension in config.ALLOWED_EXTENSION_FILES


def words_count(file_path):
    """
    Cuenta las palabras de un archivo de forma eficiente. Sin manejo de estados ni errores internamente. El worker se encargara de eso
    """    
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(len(line.split()) for line in f)

def save_result(job_id, content):
    """Salvamos el resultado en un archivo JSON """
    output_path = os.path.join(config.PROCESSED_FOLDER_PATH, f"{job_id}.json")

    try:
        with open(output_path,'w', encoding='utf-8') as f:
            json.dump(content,f, indent=4)


    except Exception as e:
        print(f"Error al guardar el resultado: {str(e)}")

