"""
Script para crear las tablas en Neon (PostgreSQL).
Ejecutar una vez después de configurar DATABASE_URL en .env:

python migrardb.py
"""

import os
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

import src.entities.apuesta  # noqa: F401 - registrar modelo
import src.entities.billetera  # noqa: F401 - registrar modelo
import src.entities.metodo_pago  # noqa: F401 - registrar modelo
import src.entities.ruleta  # noqa: F401 - registrar modelo
import src.entities.sorteo  # noqa: F401 - registrar modelo
import src.entities.transaccion  # noqa: F401 - registrar modelo
import src.entities.usuario  # noqa: F401 - registrar modelo
import src.entities.bingo  # noqa: F401 - registrar modelo
import src.entities.loteria  # noqa: F401 - registrar modelo
from src.database.config import create_tables

if __name__ == "__main__":
    try:
        create_tables()
        print("Tablas creadas correctamente en Neon.")
    except OperationalError as e:
        if "password authentication failed" in str(e).lower():
            print("Error: Neon rechazó la contraseña (password authentication failed).")
            print(
                "  - Entra a https://console.neon.tech y revisa la conexión del proyecto."
            )
            print(
                "  - Copia de nuevo la connection string (Connection string) y actualiza .env."
            )
            print(
                "  - Si la contraseña tiene caracteres especiales (& # @ ?), codifícala en URL (ej. @ → %40)."
            )
        else:
            print("Error de conexión a la base de datos:", e)
        raise SystemExit(1)
