from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy import text

from sqlalchemy.orm import Session
from entities.bingo import Bingo
from src.entities.loteria import Loteria


def crear_loteria(
    db: Session, numero_jugado: str, costo_entrada: float, recompensa: float
) -> Loteria:
    if len(numero_jugado) != 4:
        raise ValueError("El número debe tener exactamente 4 dígitos")

    for caracter in numero_jugado:
        if caracter not in "0123456789":
            raise ValueError("Solo se permiten dígitos del 0 al 9")

    if costo_entrada <= 0:
        raise ValueError("El costo de entrada debe ser mayor que 0")

    if recompensa <= 0:
        raise ValueError("La recompensa debe ser mayor que 0")

    loteria = Loteria(
        numero_jugado=numero_jugado,
        costo_entrada=Decimal(str(costo_entrada)),
        recompensa=Decimal(str(recompensa)),
    )

    db.add(loteria)
    db.commit()
    db.refresh(loteria)

    return loteria


def obtener_loteria(db: Session, id_loteria: UUID) -> Optional[Loteria]:
    return db.query(Loteria).filter(Loteria.id_loteria == id_loteria).first()


def obtener_loterias(db: Session, skip: int = 0, limit: int = 100) -> List[Loteria]:
    return db.query(Loteria).offset(skip).limit(limit).all()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Loteria]:
    return db.query(Loteria).offset(skip).limit(limit).all()


def actualizar_loteria(db: Session, id_loteria: UUID, **kwargs) -> Optional[Loteria]:
    loteria = obtener_loteria(db, id_loteria)

    if not loteria:
        return None

    if "numero_jugado" in kwargs:
        numero = kwargs["numero_jugado"]
        if len(numero) != 4:
            raise ValueError("El número debe tener exactamente 4 dígitos")
        for caracter in numero:
            if caracter not in "0123456789":
                raise ValueError("Solo se permiten dígitos del 0 al 9")

    if "costo_entrada" in kwargs:
        costo = kwargs["costo_entrada"]
        if costo <= 0:
            raise ValueError("El costo de entrada debe ser mayor que 0")
        kwargs["costo_entrada"] = Decimal(str(costo))

    if "recompensa" in kwargs:
        premio = kwargs["recompensa"]
        if premio <= 0:
            raise ValueError("La recompensa debe ser mayor que 0")
        kwargs["recompensa"] = Decimal(str(premio))

    for key, value in kwargs.items():
        if hasattr(loteria, key):
            setattr(loteria, key, value)

    db.commit()
    db.refresh(loteria)

    return loteria


def eliminar_loteria(db: Session, id_loteria: UUID) -> bool:
    loteria = obtener_loteria(db, id_loteria)

    if loteria:
        db.delete(loteria)
        db.commit()
        return True
    return False
