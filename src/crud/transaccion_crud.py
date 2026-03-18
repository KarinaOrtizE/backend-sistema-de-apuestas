from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from entities.transaccion import Transaccion


class TransaccionCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_transaccion(
        self, tipo, monto, id_billetera, id_metodo_pago
    ) -> Transaccion:

        if monto <= 0:
            raise ValueError("El monto debe ser mayor que 0")

        transaccion = Transaccion(
            tipo=tipo,
            monto=monto,
            id_billetera=id_billetera,
            id_metodo_pago=id_metodo_pago,
        )

        self.db.add(transaccion)
        self.db.commit()
        self.db.refresh(transaccion)

        return transaccion

    def obtener_transaccion(self, id_transaccion: UUID) -> Optional[Transaccion]:

        return (
            self.db.query(Transaccion)
            .filter(Transaccion.id_transaccion == id_transaccion)
            .first()
        )

    def obtener_transacciones(
        self, skip: int = 0, limit: int = 100
    ) -> List[Transaccion]:

        return self.db.query(Transaccion).offset(skip).limit(limit).all()

    def actualizar_transaccion(
        self, id_transaccion: UUID, **kwargs
    ) -> Optional[Transaccion]:

        transaccion = self.obtener_transaccion(id_transaccion)

        if not transaccion:
            return None

        for key, value in kwargs.items():
            if hasattr(transaccion, key):
                setattr(transaccion, key, value)

        self.db.commit()
        self.db.refresh(transaccion)

        return transaccion

    def eliminar_transaccion(self, id_transaccion: UUID) -> bool:

        transaccion = self.obtener_transaccion(id_transaccion)

        if transaccion:
            self.db.delete(transaccion)
            self.db.commit()
            return True

        return False
