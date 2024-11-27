<h1 align="center">FASTAPI</h1>
<p>
    <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
    <img alt="Python" src="https://img.shields.io/badge/FastAPI-green.svg"/>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.11.0-yellow.svg" />
  <a href="https://github.com/alaya-digital-solutions/data_driven_mining_trazabilidad_back#readme" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-no-green.svg" />
  </a>
</p>

### Descripción de las Carpetas

- **`app`**: Carpeta principal que contiene toda la lógica de la aplicación.
- **`api`**: Contiene los endpoints organizados por versiones para facilitar el versionado de la API.
- **`core`**: Almacena configuraciones centrales, seguridad, y otras configuraciones globales.
- **`models`**: Modelos de datos definidos con ORM (como SQLAlchemy) o clases de Pydantic.
- **`services`**: Contiene la lógica de negocio, organizando funciones que realizan operaciones complejas.
- **`db`**: Configuración de la base de datos y manejo de sesiones.
- **`schemas`**: Define los esquemas de Pydantic para validación y serialización de datos.
- **`tests`**: Pruebas para la aplicación, organizadas según las funcionalidades.
- **`migrations`**: Manejo de migraciones de la base de datos, usando herramientas como Alembic.

```
/project-root
│
├── /app                            # Carpeta principal de la aplicación
│   ├── /api                        # Endpoints o rutas
│   │   ├── v1                      # Versionado de la API (opcional)
│   │   │   ├── __init__.py
│   │   │   ├── endpoints.py        # Definición de endpoints
│   │   │   └── dependencies.py     # Dependencias comunes de los endpoints
│   │   └── v2                      # Otra versión de la API si es necesario
│   │       ├── __init__.py
│   │       └── endpoints.py
│   │
│   ├── /core                       # Configuración central de la aplicación
│   │   ├── __init__.py
│   │   ├── config.py               # Configuración general (variables de entorno)
│   │   └── security.py             # Configuración de seguridad (JWT, OAuth, etc.)
│   │
│   ├── /models                     # Modelos de datos (SQLAlchemy, Pydantic)
│   │   ├── __init__.py
│   │   └── user.py                 # Ejemplo de modelo
│   │
│   ├── /services                   # Lógica de negocio (servicios o casos de uso)
│   │   ├── __init__.py
│   │   └── user_service.py         # Ejemplo de servicio
│   │
│   ├── /db                         # Base de datos (configuración y manejo)
│   │   ├── __init__.py
│   │   ├── base.py                 # Configuración básica de la base de datos
│   │   └── session.py              # Manejo de sesiones de la base de datos
│   │
│   ├── /schemas                    # Esquemas de Pydantic (validación y serialización)
│   │   ├── __init__.py
│   │   └── user.py                 # Ejemplo de esquema
│   │
│   ├── /tests                      # Pruebas (unitarias e integrales)
│   │   ├── __init__.py
│   │   └── test_user.py            # Ejemplo de prueba
│   │
│   ├── main.py                     # Punto de entrada de la aplicación
│   └── __init__.py
│
├── /migrations                     # Migraciones de la base de datos (al usar SQLAlchemy o Alembic)
│   └── env.py
│
├── .env                            # Variables de entorno
├── requirements.txt                # Dependencias del proyecto
├── Dockerfile                      # Docker para despliegue
├── docker-compose.yml              # Archivo de configuración de Docker Compose (opcional)
└── README.md                       # Documentación del proyecto
```

## Run Project

1. Create Virtual Enviroment

```
python -m venv venv
```

2. Activate enviroment

   > Windows:

   ```sh
   source venv/Scripts/activate
   ```

   > Linux

   ```sh
   source .venv/bin/activate
   ```

3. Install dependencies

```sh
pip install -r requirements.txt
```

4. start the server:

```sh
uvicorn app.main:app --reload --port 8001
```

5. Run test:

```sh
pytest
```

## Requirements.txt

> Update Dependencies

```sh
pip3 freeze > requirements.txt
```

## Format Code (black)

### VS Code

Install Black Formatter (plugin vs code)
added in user setting.JSON ->

```
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
```

### CMD

1. check code format
   > black --check --diff app/main.py
2. Apply format
   > black app/main.py
3. Apply in all files
   > black .
