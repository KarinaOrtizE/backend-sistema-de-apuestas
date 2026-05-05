import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.entities.sorteo import Sorteo


def crear_sorteo(
    db: Session, fecha_sorteo: datetime, id_bingo=None, id_ruleta=None, id_loteria=None
):
    juegos = [id_bingo, id_ruleta, id_loteria]
    cantidad_juegos = len([j for j in juegos if j is not None])

    if cantidad_juegos > 1:
        raise ValueError("Error: No puedes asignar un sorteo a varios juegos a la vez.")
    if cantidad_juegos == 0:
        raise ValueError(
            "Error: Debes asignar el sorteo a un juego (Bingo, Ruleta o Lotería)."
        )

    nuevo = Sorteo(
        fecha_sorteo=fecha_sorteo,
        id_bingo=id_bingo,
        id_ruleta=id_ruleta,
        id_loteria=id_loteria,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def obtener_por_id(db: Session, id_sorteo: uuid.UUID) -> Optional[Sorteo]:
    return db.query(Sorteo).filter(Sorteo.id_sorteo == id_sorteo).first()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Sorteo]:
    return db.query(Sorteo).offset(skip).limit(limit).all()


def actualizar(db: Session, id_sorteo: uuid.UUID, **kwargs) -> Optional[Sorteo]:

    sorteo = obtener_por_id(db, id_sorteo)

    if not sorteo:
        return None

    for key, value in kwargs.items():
        if value is not None and hasattr(sorteo, key):
            setattr(sorteo, key, value)

    try:
        db.commit()
        db.refresh(sorteo)
        return sorteo
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(db: Session, id_sorteo: uuid.UUID) -> bool:
    sorteo = obtener_por_id(db, id_sorteo)

    if not sorteo:
        return False

    db.delete(sorteo)
    db.commit()
    return True
