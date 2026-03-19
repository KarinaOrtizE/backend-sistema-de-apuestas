from sqlalchemy.orm import Session
from src.entities.sorteo import Sorteo
from datetime import datetime
import uuid


def programar_sorteo(
    db: Session,
    fecha_evento: datetime,
    id_bingo: uuid.UUID = None,
    id_ruleta: uuid.UUID = None,
    id_loteria: uuid.UUID = None,
) -> Sorteo:

    nuevo_sorteo = Sorteo(
        fecha_sorteo=fecha_evento,
        id_bingo=id_bingo,
        id_ruleta=id_ruleta,
        id_loteria=id_loteria,
    )
    db.add(nuevo_sorteo)
    db.commit()
    db.refresh(nuevo_sorteo)
    return nuevo_sorteo
