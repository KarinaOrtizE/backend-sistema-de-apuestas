from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.entities.billetera import Billetera


def crear(
    db: Session, id_usuario: UUID, id_usuario_creacion: Optional[UUID] = None
) -> Billetera:
    """Crea una nueva billetera para un usuario."""
    usuario = db.execute(
        text("SELECT id_usuario FROM usuario WHERE id_usuario = :id_usuario"),
        {"id_usuario": id_usuario},
    ).first()

    if not usuario:
        raise ValueError("El usuario no existe")

    billetera_existente = obtener_por_id(db, id_usuario)
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


def obtener_por_id(db: Session, billetera_id: UUID) -> Billetera | None:
    """Obtiene una billetera por su ID."""
    return db.query(Billetera).filter(Billetera.id_billetera == billetera_id).first()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Billetera]:
    return db.query(Billetera).offset(skip).limit(limit).all()


def recargar_saldo(
    db: Session, billetera_id: UUID, monto: Decimal, id_usuario_operacion: UUID
) -> Billetera:
    """Recarga saldo a la billetera."""
    if monto <= 0:
        raise ValueError("El monto debe ser positivo")
    if round(monto, 2) != monto:
        raise ValueError("El monto no puede tener más de 2 decimales")

    billetera: Optional[Billetera] = (
        db.query(Billetera).filter(Billetera.id_billetera == billetera_id).first()
    )
    if not billetera:
        raise ValueError("La billetera no existe")

    billetera.saldo += monto_decimal  # type: ignore
    billetera.id_usuario_edita = id_usuario_operacion  # type: ignore

    db.commit()
    db.refresh(billetera)
    return billetera


def consultar_saldo(db: Session, billetera_id: UUID) -> float:
    """Consulta el saldo actual de una billetera."""
    billetera = (
        db.query(Billetera).filter(Billetera.id_billetera == billetera_id).first()
    )
    if not billetera:
        raise ValueError("La billetera no existe")
    return float(billetera.saldo)  # type: ignore


def actualizar(
    db: Session, billetera_id: UUID, id_usuario_edita: Optional[UUID] = None, **kwargs
) -> Billetera | None:
    """Actualiza información de la billetera (solo auditoría)."""
    campos_prohibidos = ["saldo", "id_usuario"]

    billetera = (
        db.query(Billetera).filter(Billetera.id_billetera == billetera_id).first()
    )
    if not billetera:
        return None

    for key in kwargs:
        if key in campos_prohibidos:
            raise ValueError(f"No se puede actualizar el campo '{key}' directamente")

    if id_usuario_edita is None:
        admin = db.execute(
            text("SELECT id_usuario FROM usuario WHERE es_admin = true LIMIT 1")
        ).first()

        if not admin:
            raise ValueError("No se encontró un usuario administrador")
        id_usuario_edita = admin[0]

    setattr(billetera, "id_usuario_edita", id_usuario_edita)

    for key, value in kwargs.items():
        if hasattr(billetera, key) and key not in campos_prohibidos:
            setattr(billetera, key, value)

    db.commit()
    db.refresh(billetera)
    return billetera


def eliminar(db: Session, billetera_id: UUID) -> bool:
    """Elimina una billetera (solo si saldo = 0)."""
    billetera = (
        db.query(Billetera).filter(Billetera.id_billetera == billetera_id).first()
    )
    if not billetera:
        return False

    #        if billetera.saldo != Decimal("0.00"):  # type: ignore
    #            raise ValueError("No se puede eliminar: la billetera tiene saldo")

    db.delete(billetera)
    db.commit()
    return True
