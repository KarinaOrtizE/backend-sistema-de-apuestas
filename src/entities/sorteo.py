import uuid
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from src.database.config import Base


class Sorteo(Base):

    __tablename__ = "sorteo"

    id_sorteo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    fecha_sorteo = Column(DateTime(timezone=True), nullable=False)

    resultado = Column(JSONB, nullable=True)

    fecha_creacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        description="Fecha en que se programó el sorteo",
    )

    apuestas = relationship("Apuesta", back_populates="sorteo")

    def __repr__(self):
        return f"<Sorteo(id='{self.id_sorteo}', fecha='{self.fecha_sorteo}')>"
