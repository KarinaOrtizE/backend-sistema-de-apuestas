import uuid
from sqlalchemy import Column, DateTime, ForeignKey, func
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
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    id_bingo = Column(UUID(as_uuid=True), ForeignKey("bingo.id_bingo"), nullable=True)
    id_ruleta = Column(
        UUID(as_uuid=True), ForeignKey("ruleta.id_ruleta"), nullable=True
    )
    id_loteria = Column(
        UUID(as_uuid=True), ForeignKey("loteria.id_loteria"), nullable=True
    )

    bingo = relationship("Bingo", back_populates="sorteos")
    ruleta = relationship("Ruleta", back_populates="sorteos")
    loteria = relationship("Loteria", back_populates="sorteos")

    apuestas = relationship("Apuesta", back_populates="sorteo")
