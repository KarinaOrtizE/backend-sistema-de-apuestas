from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from src.entities.billetera import Billetera


def obtener_por_id(db: Session, billetera_id: UUID) -> Optional[Billetera]:
    """Obtiene una billetera por su ID."""
    return db.query(Billetera).filter(Billetera.id_billetera == billetera_id).first()


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


def obtener_por_usuario_id(db: Session, usuario_id: UUID) -> Optional[Billetera]:
    """Obtiene la billetera asociada a un usuario."""
    return db.query(Billetera).filter(Billetera.id_usuario == usuario_id).first()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Billetera]:
    """Lista todas las billeteras con paginación."""
    return db.query(Billetera).offset(skip).limit(limit).all()
