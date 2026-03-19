Sistema de gestión de apuestas desarrollado en Python con SQLAlchemy y PostgreSQL (Neon). Permite administrar usuarios, billeteras, loterías, bingos, ruletas, sorteos y apuestas.


## ✨ Características

- ✅ **Gestión de Usuarios**: Registro, login con contraseñas hasheadas (bcrypt)
- ✅ **Billeteras Virtuales**: Cada usuario tiene su billetera con saldo
- ✅ **Múltiples Juegos**: Lotería, Bingo y Ruleta
- ✅ **Sorteos**: Programación y ejecución de sorteos
- ✅ **Apuestas**: Registro de apuestas con validación de saldo
- ✅ **Transacciones**: Control de movimientos de dinero
- ✅ **Métodos de Pago**: Registro de métodos de pago por usuario
- ✅ **Auditoría**: Trazabilidad de creación y modificación de registros

## 🛠 Tecnologías

- **Python 3.13+**
- **SQLAlchemy 2.0** - ORM para base de datos
- **PostgreSQL** (Neon.tech) - Base de datos en la nube
- **bcrypt** - Hashing de contraseñas
- **python-dotenv** - Configuración de variables de entorno

## 📁 Estructura del Proyecto
backend-sistema-de-apuestas/
├── src/
│ ├── database/
│ │ └── config.py 
│ ├── entities/ 
│ │ ├── usuario.py
│ │ ├── billetera.py
│ │ ├── transaccion.py
│ │ ├── metodo_pago.py
│ │ ├── loteria.py
│ │ ├── bingo.py
│ │ ├── ruleta.py
│ │ ├── sorteo.py
│ │ └── apuesta.py
│ └── crud/ 
│ ├── usuario_crud.py
│ ├── billetera_crud.py
│ ├── transaccion_crud.py
│ ├── metodo_pago_crud.py
│ ├── loteria_crud.py
│ ├── bingo_crud.py
│ ├── ruleta_crud.py
│ ├── sorteo_crud.py
│ └── apuesta_crud.py
├── .env 
├── migrardb.py
├── init_db.py 
├── main.py 
├── requirements.txt 
└── README.md 

Link demostración: https://docs.google.com/document/d/1FbFqtLKpNuSOXfd-PHKaC_vuazrBdWiZdn5Yo2GNhZw/edit?usp=sharing