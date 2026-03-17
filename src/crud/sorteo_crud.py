from sqlalchemy.orm import Session
from src.entities.sorteo import Sorteo
from datetime import datetime
from typing import Optional, List, Dict
import uuid


def programar_sorteo(db: Session, fecha_evento: datetime) -> Sorteo:
    nuevo_sorteo = Sorteo(fecha_sorteo=fecha_evento)
    db.add(nuevo_sorteo)
    db.commit()
    db.refresh(nuevo_sorteo)
    return nuevo_sorteo


def registrar_resultado_final(
    db: Session, id_sorteo: uuid.UUID, data_resultado: Dict
) -> Optional[Sorteo]:
    sorteo = db.query(Sorteo).filter(Sorteo.id_sorteo == id_sorteo).first()
    if sorteo:
        sorteo.resultado = data_resultado
        db.commit()
        db.refresh(sorteo)
    return sorteo


def obtener_sorteo(db: Session, id_sorteo: uuid.UUID) -> Optional[Sorteo]:
    return db.query(Sorteo).filter(Sorteo.id_sorteo == id_sorteo).first()


def listar_historial_sorteos(db: Session) -> List[Sorteo]:
    return db.query(Sorteo).all()
