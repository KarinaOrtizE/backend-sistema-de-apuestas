import uuid
import random
from typing import List, Optional
from datetime import datetime

from src.database.config import SessionLocal
from src.entities.sorteo import Sorteo

db = SessionLocal()


def programar_sorteo(
    fecha_evento: datetime,
    id_bingo: uuid.UUID = None,
    id_ruleta: uuid.UUID = None,
    id_loteria: uuid.UUID = None,
) -> Sorteo:

    nuevo = Sorteo(
        fecha_sorteo=fecha_evento,
        id_bingo=id_bingo,
        id_ruleta=id_ruleta,
        id_loteria=id_loteria,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def obtener_por_id(id_sorteo: uuid.UUID) -> Optional[Sorteo]:
    return db.query(Sorteo).filter(Sorteo.id_sorteo == id_sorteo).first()


def listar_todos() -> List[Sorteo]:
    return db.query(Sorteo).all()


def actualizar(id_sorteo: uuid.UUID, **kwargs) -> Optional[Sorteo]:
    sorteo = obtener_por_id(id_sorteo)

    if sorteo is None:
        print("Error: No se encontró el sorteo")
        return None

    for key, value in kwargs.items():
        if hasattr(sorteo, key):
            setattr(sorteo, key, value)

    try:
        db.commit()
        db.refresh(sorteo)
        return sorteo
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(id_sorteo: uuid.UUID) -> bool:
    sorteo = obtener_por_id(id_sorteo)
    if sorteo:
        db.delete(sorteo)
        db.commit()
        return True
    return False
