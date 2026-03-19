import uuid

from sqlalchemy import Column, Integer, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship


from src.database.config import Base


class Bingo(Base):
    """Modelo de bingo"""

    __tablename__ = "bingo"

    id_bingo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    aciertos = Column(Integer, nullable=True)
    carton_json = Column(JSONB, nullable=False)
    costo_entrada = Column(Float, nullable=False, default=5000.0)
    recompensa = Column(Float, nullable=True)

    sorteos = relationship("Sorteo", back_populates="bingo")
