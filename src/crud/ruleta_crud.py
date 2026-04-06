from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.ruleta import Ruleta


def crear(
    db: Session,
    eleccion_usuario: str,
    costo_entrada: float,
    recompensa: float,
) -> Ruleta:

    if costo_entrada <= 0:
        raise ValueError("El costo de entrada debe ser mayor que 0")

    if recompensa <= 0:
        raise ValueError("La recompensa debe ser mayor que 0")

    nueva_ruleta = Ruleta(
        eleccion_usuario=eleccion_usuario,
        costo_entrada=costo_entrada,
        recompensa=recompensa,
    )

    db.add(nueva_ruleta)
    db.commit()
    db.refresh(nueva_ruleta)

    return nueva_ruleta


def obtener_por_id(db: Session, id_ruleta: UUID) -> Optional[Ruleta]:
    return db.query(Ruleta).filter(Ruleta.id_ruleta == id_ruleta).first()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Ruleta]:
    return db.query(Ruleta).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_ruleta: UUID,
    **kwargs: dict,
) -> Optional[Ruleta]:

    ruleta = obtener_por_id(db, id_ruleta)

    if ruleta is None:
        print("Error: No se encontró la ruleta")
        return None

    for key, value in kwargs.items():
        if hasattr(ruleta, key):
            setattr(ruleta, key, value)

    try:
        db.commit()
        db.refresh(ruleta)
        return ruleta
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(db: Session, id_ruleta: UUID) -> bool:
    ruleta = obtener_por_id(db, id_ruleta)

    if ruleta:
        db.delete(ruleta)
        db.commit()
        return True

    return False
