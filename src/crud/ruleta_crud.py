from typing import List, Optional
from uuid import UUID
import json

from sqlalchemy.orm import Session
from src.entities.ruleta import Ruleta


def validar_eleccion(eleccion: dict) -> None:

    if not any(eleccion.values()):
        raise ValueError("Debes elegir al menos una opción")

    if eleccion.get("numero") is not None:
        if not (0 <= eleccion["numero"] <= 36):
            raise ValueError("Número inválido")

    if eleccion.get("color") not in [None, "rojo", "negro"]:
        raise ValueError("Color inválido")

    if eleccion.get("paridad") not in [None, "par", "impar"]:
        raise ValueError("Paridad inválida")

    if eleccion.get("rango") not in [None, "alto", "bajo"]:
        raise ValueError("Rango inválido")


def crear(
    db: Session,
    eleccion_usuario: dict,
    costo_entrada: float,
    recompensa: float,
) -> Ruleta:

    if costo_entrada <= 0:
        raise ValueError("El costo de entrada debe ser mayor que 0")

    if recompensa <= 0:
        raise ValueError("La recompensa debe ser mayor que 0")

    validar_eleccion(eleccion_usuario)

    nueva_ruleta = Ruleta(
        eleccion_usuario=json.dumps(eleccion_usuario),
        costo_entrada=costo_entrada,
        recompensa=recompensa,
    )

    db.add(nueva_ruleta)
    db.commit()
    db.refresh(nueva_ruleta)

    return nueva_ruleta


def obtener_por_id(db: Session, id_ruleta: UUID) -> Optional[Ruleta]:
    return db.query(Ruleta).filter(Ruleta.id_ruleta == id_ruleta).first()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Ruleta]:
    return db.query(Ruleta).offset(skip).limit(limit).all()


def actualizar(db: Session, id_ruleta: UUID, **kwargs) -> Optional[Ruleta]:

    ruleta = obtener_por_id(db, id_ruleta)

    if ruleta is None:
        return None

    if "eleccion_usuario" in kwargs:

        eleccion_actual = json.loads(ruleta.eleccion_usuario)

        nueva_eleccion = kwargs["eleccion_usuario"]

        eleccion_final = {**eleccion_actual, **nueva_eleccion}

        validar_eleccion(eleccion_final)

        kwargs["eleccion_usuario"] = json.dumps(eleccion_final)

    if "costo_entrada" in kwargs and kwargs["costo_entrada"] <= 0:
        raise ValueError("El costo de entrada debe ser mayor que 0")

    if "recompensa" in kwargs and kwargs["recompensa"] <= 0:
        raise ValueError("La recompensa debe ser mayor que 0")

    for key, value in kwargs.items():
        if hasattr(ruleta, key):
            setattr(ruleta, key, value)

    try:
        db.commit()
        db.refresh(ruleta)
        return ruleta
    except Exception:
        db.rollback()
        return None


def eliminar(db: Session, id_ruleta: UUID) -> bool:
    ruleta = obtener_por_id(db, id_ruleta)

    if ruleta:
        db.delete(ruleta)
        db.commit()
        return True

    return False
