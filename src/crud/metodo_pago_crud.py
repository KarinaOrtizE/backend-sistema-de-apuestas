from sqlalchemy.orm import Session
from src.entities.metodo_pago import MetodoPago
from typing import List, Optional
import uuid


def registrar_metodo_pago(
    db: Session, tipo: str, titular: str, id_dueno: uuid.UUID, id_admin: uuid.UUID
) -> MetodoPago:
    nuevo_metodo = MetodoPago(
        tipo_metodo=tipo,
        nombre_titular=titular,
        id_usuario_dueno=id_dueno,
        id_usuario_creacion=id_admin,
    )
    db.add(nuevo_metodo)
    db.commit()
    db.refresh(nuevo_metodo)
    return nuevo_metodo


def actualizar_titular_metodo(
    db: Session, id_metodo: uuid.UUID, nuevo_titular: str, id_admin: uuid.UUID
) -> Optional[MetodoPago]:
    metodo = db.query(MetodoPago).filter(MetodoPago.id_metodo_pago == id_metodo).first()

    if metodo:
        metodo.nombre_titular = nuevo_titular
        metodo.id_usuario_edita = id_admin

        db.commit()
        db.refresh(metodo)
    return metodo


def listar_metodos_usuario(db: Session, id_dueno: uuid.UUID) -> List[MetodoPago]:
    return db.query(MetodoPago).filter(MetodoPago.id_usuario_dueno == id_dueno).all()
