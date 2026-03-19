from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.ruleta import Ruleta

db = SessionLocal()


def crear(
    eleccion_usuario: str,
    costo_entrada: float,
    recompensa: float,
) -> Ruleta:
    """Crea una ruleta."""

    if costo_entrada <= 0:
        raise ValueError("El costo de entrada debe ser mayor que 0")

    if recompensa <= 0:
        raise ValueError("La recompensa debe ser mayor que 0")

    nueva_ruleta = Ruleta(
        eleccion_usuario=eleccion_usuario,
        costo_entrada=costo_entrada,
        recompensa=recompensa,
    )

    db.add(nueva_ruleta)
    db.commit()
    db.refresh(nueva_ruleta)

    return nueva_ruleta


def obtener_por_id(id_ruleta: UUID) -> Optional[Ruleta]:
    return db.query(Ruleta).filter(Ruleta.id_ruleta == id_ruleta).first()


def listar_todos() -> List[Ruleta]:
    return db.query(Ruleta).all()


def actualizar(
    id_ruleta: UUID,
    **kwargs: dict,
) -> Optional[Ruleta]:

    ruleta = obtener_por_id(id_ruleta)

    if ruleta is None:
        print("Error: No se encontró la ruleta")
        return None

    for key, value in kwargs.items():
        if hasattr(ruleta, key):
            setattr(ruleta, key, value)

    try:
        db.commit()
        db.refresh(ruleta)
        return ruleta
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(id_ruleta: UUID) -> bool:
    ruleta = obtener_por_id(id_ruleta)

    if ruleta:
        db.delete(ruleta)
        db.commit()
        return True

    return False
