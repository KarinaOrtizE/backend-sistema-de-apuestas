## 🚀 Backend: Sistema de Apuestas
Este proyecto es una API REST desarrollada con FastAPI para la gestión de un sistema de apuestas. Incluye integración con un ORM (SQLAlchemy) para la persistencia de datos en una base de datos PostgreSQL (Neon.tech).

## ✨ Características

- **Gestión de Usuarios**: Registro, login con contraseñas hasheadas (bcrypt)
- **Billeteras Virtuales**: Cada usuario tiene su billetera con saldo
- **Múltiples Juegos**: Lotería, Bingo y Ruleta
- **Sorteos**: Programación y ejecución de sorteos
- **Apuestas**: Registro de apuestas con validación de saldo
- **Transacciones**: Control de movimientos de dinero
- **Métodos de Pago**: Registro de métodos de pago por usuario
- **Auditoría**: Trazabilidad de creación y modificación de registros
- **Integración de FastAPI**: Migración de la lógica base a una interfaz de API moderna.
- **Persistencia**: Uso de SQLAlchemy como ORM para la gestión de entidades en PostgreSQL.
- **Documentación**: Endpoints documentados y probables a través de Swagger UI.
- **Operaciones CRUD**: Soporte completo (GET, POST, PUT, DELETE) para las entidades principales.
- **Ejecución**: Servidor ASGI mediante Uvicorn.
- **Arquitectura Limpia**: Separación de responsabilidades en api, crud, entities y database.

## 🛠 Tecnologías

- **Python 3.13+**
- **SQLAlchemy 2.0** - ORM para base de datos
- **PostgreSQL** (Neon.tech) - Base de datos en la nube
- **python-dotenv** - Configuración de variables de entorno
- **Pydantic** - Validación de esquemas de datos.
- **Uvicorn** - Servidor ASGI para ejecutar la aplicación.

## 📁 Estructura del Proyecto

Backend-sistema-de-apuestas/  
├── .env  
├── .gitignore  
├── main.py  
├── migrardb.py  
├── README.md  
├── requirements.txt  
└── src/  
    ├── api/  
    │   │   ├── app.py  
    │   │   ├── apuesta.py  
    │   │   ├── billetera.py  
    │   │   ├── bingo.py  
    │   │   ├── deps.py  
    │   │   ├── loteria.py  
    │   │   ├── metodo_pago.py  
    │   │   ├── ruleta.py  
    │   │   ├── sorteo.py  
    │   │   ├── transaccion.py  
    │   │   └── usuario.py  
    ├── database/  
    │   └── config.py  
    ├── entities/  
    │   ├── apuesta.py  
    │   ├── billetera.py  
    │   ├── bingo.py  
    │   ├── loteria.py  
    │   ├── metodo_pago.py  
    │   ├── ruleta.py  
    │   ├── sorteo.py  
    │   ├── transaccion.py  
    │   └── usuario.py  
    ├── crud/  
    │   ├── apuesta_crud.py  
    │   ├── billetera_crud.py  
    │   ├── bingo_crud.py  
    │   ├── loteria_crud.py  
    │   ├── metodo_pago_crud.py  
    │   ├── ruleta_crud.py  
    │   ├── sorteo_crud.py  
    │   ├── transaccion_crud.py  
    │   └── usuario_crud.py  

La arquitectura sigue un patrón de separación de responsabilidades:

- src/api/: Definición de rutas, esquemas Pydantic y dependencias.
- src/database/: Configuración de la conexión y motor de SQLAlchemy.
- src/entities/: Modelos de datos (tablas de la DB).
- src/crud/: Lógica de negocio y operaciones de base de datos.

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd Backend-sistema-de-apuestas

### 2. Instalar dependencias
py -m pip install -r requirements.txt

### 3. Configurar variables de entorno
Crea un archivo .env en la raíz con la cadena de conexión de Neon:
DATABASE_URL='string_de_conexion_a_neon'

### 4. Ejecutar la aplicación
El punto de entrada principal es main.py, que arranca el servidor en el puerto 8000:
python main.py

La API estará disponible en http://localhost:8000

## 📖 Documentación de la API (Swagger)
Una vez el servidor esté corriendo, puedes acceder a la documentación interactiva en:
👉 http://localhost:8000/docs

Desde allí podrás probar los endpoints (por cada entidad):

- GET /entidad/: Lista todos los registros.
- GET /entidad/{id}: Obtiene un registro por su UUID.
- POST /entidad/: Crea un nuevo registro.
- PUT /entidad/{id}: Actualiza un registro existente.
- DELETE /entidad/{id}: Elimina un registro.

## 🎥 Evidencia en Video
Puedes ver la demostración del funcionamiento de la API, las pruebas en Swagger y la verificación de datos en Neon en el siguiente enlace:

🔗 https://youtu.be/2HVsYCrzE4M?si=-xOn39GUCHZuo4vJ