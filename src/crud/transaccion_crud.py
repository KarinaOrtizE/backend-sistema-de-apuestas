from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.transaccion import Transaccion


def crear(
    db: Session,
    tipo,
    monto: float,
    id_billetera: UUID,
    id_metodo_pago: UUID,
) -> Transaccion:
    """Crea una transacción."""

    if monto <= 0:
        raise ValueError("El monto debe ser mayor que 0")

    nueva_transaccion = Transaccion(
        tipo=tipo,
        monto=monto,
        id_billetera=id_billetera,
        id_metodo_pago=id_metodo_pago,
    )

    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)

    return nueva_transaccion


def obtener_por_id(db: Session, id_transaccion: UUID) -> Optional[Transaccion]:
    return (
        db.query(Transaccion)
        .filter(Transaccion.id_transaccion == id_transaccion)
        .first()
    )


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Transaccion]:
    return db.query(Transaccion).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_transaccion: UUID,
    **kwargs: dict,
) -> Optional[Transaccion]:

    transaccion = obtener_por_id(db, id_transaccion)

    if transaccion is None:
        print("Error: No se encontró la transacción")
        return None

    for key, value in kwargs.items():
        if hasattr(transaccion, key):
            setattr(transaccion, key, value)

    try:
        db.commit()
        db.refresh(transaccion)
        return transaccion
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(db: Session, id_transaccion: UUID) -> bool:
    transaccion = obtener_por_id(db, id_transaccion)

    if transaccion:
        db.delete(transaccion)
        db.commit()
        return True

    return False
