from celery.result import AsyncResult
from src.worker.tasks import celery_app

class JobTracker:
    def __init__(self,job_id = str):
        self.job_id = job_id

        # Encapsulamos la creación de AsyncResult usando la app de Celery
        self.job = celery_app.AsyncResult(self.job_id)


    def get_status(self):
        """Traduce el estado complejo de Celery a un lenguaje simple"""
        state = self.job.state
        response = {
            "id": self.job_id,
            "status": state,
            "result": None
        }

        if state == "SUCCESS":
            response["result"] = self.job.result

        elif state == "FAILURE":
            # Cuando ocurre el fallo, result contiene la excepción/mensaje de error
            response["result"] = str(self.job.result)

        elif state == "PENDING":
            response["status"] = "WAITING"

        return response