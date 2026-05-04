from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from src.entities.transaccion import Transaccion, TipoTransaccion
from src.entities.billetera import Billetera


def crear(
    db: Session,
    tipo: TipoTransaccion,
    monto: float,
    id_billetera: UUID,
    id_metodo_pago: UUID,
) -> Transaccion:

    if monto <= 0:
        raise ValueError("El monto debe ser mayor que 0")

    billetera = (
        db.query(Billetera)
        .filter(Billetera.id_billetera == id_billetera)
        .with_for_update()
        .first()
    )

    if not billetera:
        raise ValueError("La billetera vinculada no existe")

    monto_decimal = Decimal(str(monto))

    if tipo in [TipoTransaccion.DEPOSITO, TipoTransaccion.PREMIO]:
        billetera.saldo += monto_decimal
    elif tipo in [TipoTransaccion.RETIRO, TipoTransaccion.APUESTA]:
        if billetera.saldo < monto_decimal:
            raise ValueError(f"Saldo insuficiente. Saldo actual: {billetera.saldo}")
        billetera.saldo -= monto_decimal

    nueva_transaccion = Transaccion(
        tipo=tipo,
        monto=monto,
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


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Transaccion]:
    return db.query(Transaccion).offset(skip).limit(limit).all()


def actualizar(db: Session, id_transaccion: UUID, **kwargs) -> Optional[Transaccion]:
    """Actualiza una transacción y ajusta el saldo de la billetera si el monto cambia."""

    transaccion = obtener_por_id(db, id_transaccion)
    if not transaccion:
        return None

    if "monto" in kwargs:
        nuevo_monto = Decimal(str(kwargs["monto"]))
        monto_antiguo = Decimal(str(transaccion.monto))
        diferencia = nuevo_monto - monto_antiguo

        billetera = (
            db.query(Billetera)
            .filter(Billetera.id_billetera == transaccion.id_billetera)
            .with_for_update()
            .first()
        )

        if not billetera:
            raise ValueError("Billetera no encontrada para actualizar saldo")

        if transaccion.tipo in [TipoTransaccion.DEPOSITO, TipoTransaccion.PREMIO]:
            billetera.saldo += diferencia
        elif transaccion.tipo in [TipoTransaccion.RETIRO, TipoTransaccion.APUESTA]:
            if billetera.saldo < diferencia:
                raise ValueError("Saldo insuficiente para el nuevo ajuste de monto")
            billetera.saldo -= diferencia

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
