from typing import Optional
from uuid import UUID
from decimal import Decimal

from entities.billetera import Billetera
from sqlalchemy.orm import Session


class BilleteraCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, id_usuario: UUID, id_usuario_creacion: UUID = None) -> Billetera:
        """
        Crea una nueva billetera para un usuario.
        """
        # Verificar si el usuario existe
        usuario = self.db.execute(
            "SELECT id_usuario FROM usuario WHERE id_usuario = :id_usuario",
            {"id_usuario": id_usuario},
        ).first()

        if not usuario:
            raise ValueError("El usuario no existe")

        # Verificar si ya tiene billetera
        billetera_existente = self.obtener_por_usuario(id_usuario)
        if billetera_existente:
            raise ValueError("El usuario ya tiene una billetera")

        if id_usuario_creacion is None:
            id_usuario_creacion = id_usuario

        billetera = Billetera(
            id_usuario=id_usuario,
            saldo=Decimal("0.00"),
            id_usuario_creacion=id_usuario_creacion,
            id_usuario_edita=None,
        )
        self.db.add(billetera)
        self.db.commit()
        self.db.refresh(billetera)
        return billetera

    def obtener(self, billetera_id: UUID) -> Optional[Billetera]:
        """
        Obtiene una billetera por su ID.
        """
        return (
            self.db.query(Billetera)
            .filter(Billetera.id_billetera == billetera_id)
            .first()
        )

    def obtener_por_usuario(self, id_usuario: UUID) -> Optional[Billetera]:
        """
        Obtiene la billetera de un usuario específico.
        """
        return (
            self.db.query(Billetera).filter(Billetera.id_usuario == id_usuario).first()
        )

    def recargar_saldo(
        self, billetera_id: UUID, monto: float, id_usuario_operacion: UUID
    ) -> Billetera:
        """
        Recarga saldo a la billetera.

        Reglas:
        - El monto debe ser positivo
        - Máximo 2 decimales
        """
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if round(monto, 2) != monto:
            raise ValueError("El monto no puede tener más de 2 decimales")

        monto_decimal = Decimal(str(monto))

        billetera = self.obtener(billetera_id)
        if not billetera:
            raise ValueError("La billetera no existe")

        billetera.saldo += monto_decimal
        billetera.id_usuario_edita = id_usuario_operacion

        self.db.commit()
        self.db.refresh(billetera)
        return billetera

    def consultar_saldo(self, billetera_id: UUID) -> float:
        """
        Consulta el saldo actual de una billetera.
        """
        billetera = self.obtener(billetera_id)
        if not billetera:
            raise ValueError("La billetera no existe")
        return float(billetera.saldo)

    def actualizar(
        self, billetera_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Billetera]:
        """
        Actualiza información de la billetera (solo auditoría).
        """
        billetera = self.obtener(billetera_id)
        if not billetera:
            return None

        campos_prohibidos = ["saldo", "id_usuario"]
        for key in kwargs:
            if key in campos_prohibidos:
                raise ValueError(
                    f"No se puede actualizar el campo '{key}' directamente"
                )

        if id_usuario_edita is None:
            admin = self.db.execute(
                "SELECT id_usuario FROM usuario WHERE es_admin = true LIMIT 1"
            ).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador")
            id_usuario_edita = admin[0]

        billetera.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(billetera, key) and key not in campos_prohibidos:
                setattr(billetera, key, value)

        self.db.commit()
        self.db.refresh(billetera)
        return billetera

    def eliminar(self, billetera_id: UUID) -> bool:
        """
        Elimina una billetera (solo si saldo = 0).
        """
        billetera = self.obtener(billetera_id)
        if not billetera:
            return False

        if billetera.saldo != Decimal("0.00"):
            raise ValueError("No se puede eliminar: la billetera tiene saldo")

        self.db.delete(billetera)
        self.db.commit()
        return True
