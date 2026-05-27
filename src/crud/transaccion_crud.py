from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.billetera import Billetera
from src.entities.transaccion import TipoTransaccion, Transaccion


def crear(
    db: Session,
    tipo: TipoTransaccion,
    monto: Decimal,
    id_billetera: UUID,
    id_metodo_pago: UUID,
) -> Transaccion:
    monto_decimal = Decimal(str(monto))

    if monto_decimal <= Decimal("0"):
        raise ValueError("El monto debe ser mayor que 0")

    billetera = (
        db.query(Billetera)
        .filter(Billetera.id_billetera == id_billetera)
        .with_for_update()
        .first()
    )

    if not billetera:
        raise ValueError("La billetera vinculada no existe")

    if tipo in [TipoTransaccion.DEPOSITO, TipoTransaccion.PREMIO]:
        billetera.saldo += monto_decimal
    elif tipo in [TipoTransaccion.RETIRO, TipoTransaccion.APUESTA]:
        if billetera.saldo < monto_decimal:
            raise ValueError(f"Saldo insuficiente. Saldo actual: {billetera.saldo}")
        billetera.saldo -= monto_decimal

    nueva_transaccion = Transaccion(
        tipo=tipo,
        monto=monto_decimal,
        id_billetera=id_billetera,
        id_metodo_pago=id_metodo_pago,
    )

    try:
        db.add(nueva_transaccion)
        db.commit()
        db.refresh(nueva_transaccion)
        return nueva_transaccion
    except Exception as e:
        db.rollback()
        raise e


def obtener_por_id(db: Session, id_transaccion: UUID) -> Optional[Transaccion]:
    return (
        db.query(Transaccion)
        .filter(Transaccion.id_transaccion == id_transaccion)
        .first()
    )


def listar_por_usuario(db: Session, usuario_id: UUID, skip: int = 0, limit: int = 100) -> List[Transaccion]:
    """Lista transacciones de un usuario filtrando a través de su billetera."""
    return (
        db.query(Transaccion)
        .join(Billetera, Transaccion.id_billetera == Billetera.id_billetera)
        .filter(Billetera.id_usuario == usuario_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Transaccion]:
    return db.query(Transaccion).offset(skip).limit(limit).all()
