import uuid
from typing import List, Optional

from sqlalchemy.orm import Session
from src.entities.metodo_pago import MetodoPago


def crear_metodo_pago(
    db: Session,
    tipo_metodo: str,
    nombre_titular: str,
    id_usuario_dueno: uuid.UUID,
) -> MetodoPago:

    nuevo_metodo = MetodoPago(
        tipo_metodo=tipo_metodo.strip(),
        nombre_titular=nombre_titular.strip(),
        id_usuario_dueno=id_usuario_dueno,
    )

    db.add(nuevo_metodo)
    db.commit()
    db.refresh(nuevo_metodo)
    return nuevo_metodo


def obtener_por_id(db: Session, id_metodo: uuid.UUID) -> Optional[MetodoPago]:
    return db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo).first()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[MetodoPago]:
    return db.query(MetodoPago).offset(skip).limit(limit).all()


def listar_por_usuario(db: Session, id_usuario: uuid.UUID) -> List[MetodoPago]:
    return db.query(MetodoPago).filter(MetodoPago.id_usuario_dueno == id_usuario).all()


def actualizar_metodo_pago(
    db: Session, id_metodo: uuid.UUID, id_usuario_edita: uuid.UUID, **kwargs
) -> Optional[MetodoPago]:

    metodo = obtener_por_id(db, id_metodo)

    if not metodo:
        return None

    for key, value in kwargs.items():
        if value is not None:

            if hasattr(metodo, key):
                setattr(metodo, key, value)

    setattr(metodo, "id_usuario_edita", id_usuario_edita)

    try:
        db.commit()
        db.refresh(metodo)
        return metodo
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(db: Session, id_metodo: uuid.UUID) -> bool:
    metodo = obtener_por_id(db, id_metodo)

    if not metodo:
        return False

    db.delete(metodo)
    db.commit()
    return True
