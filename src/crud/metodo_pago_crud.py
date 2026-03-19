import uuid
from typing import List, Optional

from src.database.config import SessionLocal
from src.entities.metodo_pago import MetodoPago

db = SessionLocal()


def registrar_metodo_pago(
    tipo: str, titular: str, id_dueno: uuid.UUID, id_admin: uuid.UUID
) -> MetodoPago:
    nuevo_metodo = MetodoPago(
        tipo_metodo=tipo,
        nombre_titular=titular,
        id_usuario_dueno=id_dueno,
        id_usuario_creacion=id_admin,
    )
    db.add(nuevo_metodo)
    db.commit()
    db.refresh(nuevo_metodo)
    return nuevo_metodo


def obtener_por_id(id_metodo: uuid.UUID) -> Optional[MetodoPago]:
    return db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo).first()


def listar_metodos_usuario(id_dueno: uuid.UUID) -> List[MetodoPago]:
    return db.query(MetodoPago).filter(MetodoPago.id_usuario_dueno == id_dueno).all()


def actualizar_metodo(
    id_metodo: uuid.UUID,
    nuevo_titular: Optional[str] = None,
    nuevo_tipo: Optional[str] = None,
    id_admin: Optional[uuid.UUID] = None,
) -> Optional[MetodoPago]:
    metodo = obtener_por_id(id_metodo)

    if metodo is None:
        print("Error: No se encontró el método de pago")
        return None

    if nuevo_titular is not None:
        setattr(metodo, "nombre_titular", nuevo_titular)

    if nuevo_tipo is not None:
        setattr(metodo, "tipo_metodo", nuevo_tipo)

    if id_admin is not None:
        setattr(metodo, "id_usuario_edita", id_admin)

    try:
        db.commit()
        db.refresh(metodo)
        return metodo
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(id_metodo: uuid.UUID) -> bool:
    metodo = obtener_por_id(id_metodo)
    if metodo:
        db.delete(metodo)
        db.commit()
        return True
    return False
