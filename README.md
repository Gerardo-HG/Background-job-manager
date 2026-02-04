# 🚀 Sistema de Procesamiento de Archivos Asíncrono y Distribuido

Este proyecto es una implementación Full Stack de una arquitectura **Event-Driven** (basada en eventos) diseñada para procesar tareas pesadas en segundo plano sin bloquear la interfaz de usuario.

Utiliza un flujo de trabajo moderno con **Flask** como servidor web, **Celery** para el procesamiento distribuido y **Redis** (Dockerizado) como gestor de colas y memoria temporal.

---

## 🏗️ Arquitectura del Sistema

El sistema sigue el patrón **Productor-Consumidor** para garantizar escalabilidad:

1.  **Frontend (Cliente):** Sube el archivo y recibe un `job_id`. Inicia un proceso de _Polling_ (consulta periódica) para monitorear el estado.
2.  **API (Flask - Productor):** Recibe el archivo, lo guarda en disco y envía una "señal" (mensaje) al Broker. Retorna inmediatamente una respuesta al usuario (Non-blocking I/O).
3.  **Broker (Redis):** Actúa como intermediario y almacena la cola de tareas.
4.  **Worker (Celery - Consumidor):** Proceso independiente que "escucha" la cola, toma la tarea, procesa el archivo (conteo de palabras) y escribe el resultado.

---

## 🛠️ Tech Stack

- **Lenguaje:** Python 3.12+ 🐍
- **Web Framework:** Flask
- **Gestor de Tareas:** Celery
- **Message Broker & Result Backend:** Redis
- **Infraestructura:** Docker 🐳 (para Redis)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS + Fetch API)

---

## 📂 Estructura del Proyecto (Clean Architecture)

El proyecto ha sido refactorizado siguiendo principios **SOLID** y **Separación de Responsabilidades**:

```text
Background-job-system/
├── processed/                  # Resultados JSON generados por el worker
├── uploads/                    # Almacenamiento temporal de archivos recibidos
├── src/
│   ├── api/
│   │   ├── templates/          # Interfaz de Usuario
│   │   └── main.py             # Controlador API (Endpoints)
│   ├── worker/
│   │   └── tasks.py            # Definición de tareas Celery
│   ├── shared/
│   │   ├── config.py           # Configuración Centralizada (Singleton)
│   │   ├── file_utils.py       # Lógica de Negocio (I/O)
│   │   └── job_tracker.py      # Patrón Facade para gestión de estados
├── run.py                      # Entry Point: Servidor Web
├── run_worker.py               # Entry Point: Worker Celery
└── README.md                   # Documentación
```

--

## ⚙️ Instalación y Configuración

1. Prerequisitos
   - Python3 instalado
     \_ Docker Desktop instalado y corriendo

2. Clonar y preparar entorno

```
git clone <tu-repo-url>
cd Background-job-system

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Mac/Linux
# .venv\Scripts\activate   # En Windows

# Instalar dependencias
pip install flask celery redis
```

3. Levantar Infraestructura (Redis)

Usamos Docker para aislar el servicio de mensajería

`docker run -d -p 6379:6379 --name redis-server redis`

4. 🚀 Cómo Ejecutar el Proyecto

Para simular un entorno distribuido, se necesita tener **3 terminales abiertas**

Terminal 1: Infraestructura

Asegurarse de que Redis esté corriendo
`docker start redis-server`

Terminal 2: Worker (El procesador)

Este proceso se quedará escuchando tareas en segundo plano
`celery -A run_worker.celery_app worker --loglevel=info`

Terminal 3: API (El servidor Web)
`python3 run.py`

## 🧠 Decisiones Técnicas y Aprendizajes

Este proyecto demuestra competencias clave de Ingeniería de Software:

- Procesamiento Asíncrono: Solución al problema de Timeouts en peticiones HTTP largas.
- Patrón de Diseño Facade: Implementado en src/shared/job_tracker.py para desacoplar la lógica de Celery de los controladores de la API.
- Configuración Centralizada: Uso de src/shared/config.py para evitar valores "harcodeados" y facilitar el despliegue en diferentes entornos.
- Manejo de Estados: Implementación de lógica de Polling en JavaScript para sincronizar el Frontend con procesos Backend de larga duración.

## Funcionalidades

- Carga de archvios (txt,json,rtf,pdf)
- Validación de extensiones seguras
- Procesamiento en Background (Conteo de palabras)
- Interfaz reactiva (sin recarga de página)
- Persistencia de resultados en JSON

Autor: Gerardo-HG
