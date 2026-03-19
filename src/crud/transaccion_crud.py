from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.transaccion import Transaccion

db = SessionLocal()


def crear(
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


def obtener_por_id(id_transaccion: UUID) -> Optional[Transaccion]:
    return (
        db.query(Transaccion)
        .filter(Transaccion.id_transaccion == id_transaccion)
        .first()
    )


def listar_todos() -> List[Transaccion]:
    return db.query(Transaccion).all()


def actualizar(
    id_transaccion: UUID,
    **kwargs: dict,
) -> Optional[Transaccion]:

    transaccion = obtener_por_id(id_transaccion)

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


def eliminar(id_transaccion: UUID) -> bool:
    transaccion = obtener_por_id(id_transaccion)

    if transaccion:
        db.delete(transaccion)
        db.commit()
        return True

    return False
