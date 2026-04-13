import random
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.bingo import Bingo


def generar_matriz_bingo():
    rangos = {
        "B": range(1, 16),
        "I": range(16, 31),
        "N": range(31, 46),
        "G": range(46, 61),
        "O": range(61, 76),
    }
    cols = [random.sample(rangos[l], 5) for l in ["B", "I", "N", "G", "O"]]
    cols[2][2] = 0
    return [[cols[c][f] for c in range(5)] for f in range(5)]


def crear(
    db: Session,
    aciertos: int = 0,
    costo_entrada: float = 5000.0,
    recompensa: float = 250000.0,
) -> Bingo:
    nuevo = Bingo(
        aciertos=aciertos,  # 🔥 SOLUCIÓN
        costo_entrada=costo_entrada,
        recompensa=recompensa,
        carton_json=generar_matriz_bingo(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def obtener_por_id(db: Session, id_bingo: UUID) -> Optional[Bingo]:
    return db.query(Bingo).filter(Bingo.id_bingo == id_bingo).first()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Bingo]:
    return db.query(Bingo).offset(skip).limit(limit).all()


def actualizar(db: Session, id_bingo: UUID, **kwargs: dict) -> Optional[Bingo]:
    bingo = obtener_por_id(db, id_bingo)

    if bingo is None:
        print("Error: No se encontró el bingo")
        return None
    for key, value in kwargs.items():
        if hasattr(bingo, key):
            setattr(bingo, key, value)
    try:
        db.commit()
        db.refresh(bingo)
        return bingo
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(db: Session, id_bingo: UUID) -> bool:
    bingo = obtener_por_id(db, id_bingo)
    if bingo:
        db.delete(bingo)
        db.commit()
        return True
    return False
