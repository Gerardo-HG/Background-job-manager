# Utilidades 
import json
import os

def read_json_file(file_path):
    try:
        with open(file_path,'r') as f:
            content = json.load(f)
            return {
                'status':'terminado',
                'words': len(content.split())
            }
    except Exception as e:
        return {
            'status':'error',
            'message': str(e)
        }

def save_result(job_id, content):
    PROCESSED_FOLDER = os.path.join(os.getcwd(),'processed')
    
    if not os.path.exists(PROCESSED_FOLDER):
        os.makedirs(PROCESSED_FOLDER)

    output_path = os.path.join(PROCESSED_FOLDER, f"{job_id}.json")
    try:
        with open(output_path,'w') as f:
            json.dump(content,f)

    except Exception as e:
        print(f"Error al guardar el resultado: {str(e)}")
