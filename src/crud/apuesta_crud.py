from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.apuesta import Apuesta, EstadoApuesta


def crear(
    db: Session,
    id_usuario: UUID,
    id_sorteo: UUID,
    monto_apostado: float,
    id_usuario_creacion: UUID,
) -> Apuesta:
    """Crea la apuesta. Por defecto el estado será PENDIENTE."""
    nueva_apuesta = Apuesta(
        id_usuario=id_usuario,
        id_sorteo=id_sorteo,
        monto_apostado=monto_apostado,
        id_usuario_creacion=id_usuario_creacion,
        estado=EstadoApuesta.PENDIENTE,
    )
    db.add(nueva_apuesta)
    db.commit()
    db.refresh(nueva_apuesta)
    return nueva_apuesta


def obtener_por_id(db: Session, id_apuesta: UUID) -> Optional[Apuesta]:
    return db.query(Apuesta).filter(Apuesta.id_apuesta == id_apuesta).first()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Apuesta]:
    return db.query(Apuesta).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_apuesta: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Apuesta]:
    apuesta = obtener_por_id(db, id_apuesta)
    if apuesta is None:
        print("Error: No se encontró la apuesta")
        return None
    for key, value in kwargs.items():
        if hasattr(apuesta, key):
            setattr(apuesta, key, value)
    setattr(apuesta, "id_usuario_edita", id_usuario_edita)
    try:
        db.commit()
        db.refresh(apuesta)
        return apuesta
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(db: Session, id_apuesta: UUID) -> bool:
    apuesta = obtener_por_id(db, id_apuesta)
    if apuesta:
        db.delete(apuesta)
        db.commit()
        return True
    return False


def listar_por_usuario(db: Session, id_usuario: UUID) -> List[Apuesta]:
    """Para que el usuario vea su historial de apuestas."""
    return db.query(Apuesta).filter(Apuesta.id_usuario == id_usuario).all()
