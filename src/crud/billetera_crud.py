from typing import Optional
from uuid import UUID
from decimal import Decimal

from entities.billetera import Billetera
from src.database.config import SessionLocal


db = SessionLocal()


def crear(id_usuario: UUID, id_usuario_creacion: UUID = None) -> Billetera:
    """
    Crea una nueva billetera para un usuario.
    """

    usuario = db.execute(
        "SELECT id_usuario FROM usuario WHERE id_usuario = :id_usuario",
        {"id_usuario": id_usuario},
    ).first()

    if not usuario:
        raise ValueError("El usuario no existe")

    billetera_existente = obtener_por_usuario(id_usuario)
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
    db.add(billetera)
    db.commit()
    db.refresh(billetera)
    return billetera


def obtener(billetera_id: UUID) -> Optional[Billetera]:
    """
    Obtiene una billetera por su ID.
    """
    return db.query(Billetera).filter(Billetera.id_billetera == billetera_id).first()


def obtener_por_usuario(id_usuario: UUID) -> Optional[Billetera]:
    """
    Obtiene la billetera de un usuario específico.
    """
    return db.query(Billetera).filter(Billetera.id_usuario == id_usuario).first()


def recargar_saldo(
    billetera_id: UUID, monto: float, id_usuario_operacion: UUID
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

    billetera = obtener(billetera_id)
    if not billetera:
        raise ValueError("La billetera no existe")

    billetera.saldo += monto_decimal
    billetera.id_usuario_edita = id_usuario_operacion

    db.commit()
    db.refresh(billetera)
    return billetera


def consultar_saldo(billetera_id: UUID) -> float:
    """
    Consulta el saldo actual de una billetera.
    """
    billetera = obtener(billetera_id)
    if not billetera:
        raise ValueError("La billetera no existe")
    return float(billetera.saldo)


def actualizar(
    billetera_id: UUID, id_usuario_edita: UUID = None, **kwargs
) -> Optional[Billetera]:
    """
    Actualiza información de la billetera (solo auditoría).
    """
    billetera = obtener(billetera_id)
    if not billetera:
        return None

    campos_prohibidos = ["saldo", "id_usuario"]
    for key in kwargs:
        if key in campos_prohibidos:
            raise ValueError(f"No se puede actualizar el campo '{key}' directamente")

    if id_usuario_edita is None:
        admin = db.execute(
            "SELECT id_usuario FROM usuario WHERE es_admin = true LIMIT 1"
        ).first()
        if not admin:
            raise ValueError("No se encontró un usuario administrador")
        id_usuario_edita = admin[0]

    billetera.id_usuario_edita = id_usuario_edita

    for key, value in kwargs.items():
        if hasattr(billetera, key) and key not in campos_prohibidos:
            setattr(billetera, key, value)

    db.commit()
    db.refresh(billetera)
    return billetera


def eliminar(billetera_id: UUID) -> bool:
    """
    Elimina una billetera (solo si saldo = 0).
    """
    billetera = obtener(billetera_id)
    if not billetera:
        return False

    if billetera.saldo != Decimal("0.00"):
        raise ValueError("No se puede eliminar: la billetera tiene saldo")

    db.delete(billetera)
    db.commit()
    return True
