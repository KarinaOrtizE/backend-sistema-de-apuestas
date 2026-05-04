from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.entities.billetera import Billetera


def obtener_por_id(db: Session, billetera_id: UUID) -> Optional[Billetera]:
    """Obtiene una billetera por su ID."""
    return db.query(Billetera).filter(Billetera.id_billetera == billetera_id).first()


def recargar_saldo(
    db: Session, billetera_id: UUID, monto: Decimal, id_usuario_operacion: UUID
) -> Billetera:
    """Recarga saldo directamente a la billetera (uso administrativo)."""
    if monto <= 0:
        raise ValueError("El monto debe ser positivo")

    billetera = (
        db.query(Billetera)
        .filter(Billetera.id_billetera == billetera_id)
        .with_for_update()
        .first()
    )

    if not billetera:
        raise ValueError("La billetera no existe")

    billetera.saldo += monto
    billetera.id_usuario_edita = id_usuario_operacion

    try:
        db.commit()
        db.refresh(billetera)
        return billetera
    except Exception as e:
        db.rollback()
        raise e


def consultar_saldo(db: Session, billetera_id: UUID) -> float:
    """Consulta el saldo actual de una billetera."""
    billetera = obtener_por_id(db, billetera_id)
    if not billetera:
        raise ValueError("La billetera no existe")
    return float(billetera.saldo)


def crear(
    db: Session, id_usuario: UUID, id_usuario_creacion: Optional[UUID] = None
) -> Billetera:
    """Crea una nueva billetera para un usuario."""
    # Verificar si ya existe para evitar duplicados
    billetera_existente = (
        db.query(Billetera).filter(Billetera.id_usuario == id_usuario).first()
    )
    if billetera_existente:
        raise ValueError("El usuario ya tiene una billetera")

    if id_usuario_creacion is None:
        id_usuario_creacion = id_usuario

    billetera = Billetera(
        id_usuario=id_usuario,
        saldo=Decimal("0.00"),
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(billetera)
    db.commit()
    db.refresh(billetera)
    return billetera


def eliminar(db: Session, billetera_id: UUID) -> bool:
    """Elimina una billetera si no tiene saldo."""
    billetera = obtener_por_id(db, billetera_id)
    if not billetera:
        return False

    if billetera.saldo > 0:
        raise ValueError("No se puede eliminar una billetera con saldo activo")

    db.delete(billetera)
    db.commit()
    return True
