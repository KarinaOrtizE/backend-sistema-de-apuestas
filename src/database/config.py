"""
Configuración de la base de datos.
Conexión mediante variables de entorno (.env).
Soporta PostgreSQL y SQLite.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en el archivo .env")

# Configuración específica según el tipo de base de datos
connect_args = {}
if DATABASE_URL.startswith("postgresql://") or "neon.tech" in DATABASE_URL:
    # Configuración para PostgreSQL/Neon.tech
    connect_args = {"sslmode": "require"}
elif DATABASE_URL.startswith("sqlite://"):
    # Configuración para SQLite
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True if not DATABASE_URL.startswith("sqlite://") else False,
    pool_recycle=300 if not DATABASE_URL.startswith("sqlite://") else None,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Generador de sesiones de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crea todas las tablas definidas en los modelos."""
    Base.metadata.create_all(bind=engine)
