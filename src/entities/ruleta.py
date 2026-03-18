import uuid

from sqlalchemy import Column, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Ruleta(Base):
    """Modelo de ruleta"""

    __tablename__ = "ruleta"

    id_ruleta = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    eleccion_usuario = Column(String, nullable=False)

    costo_entrada = Column(Float, nullable=False)

    recompensa = Column(Float, nullable=False)

    sorteos = relationship("Sorteo", back_populates="ruleta")
