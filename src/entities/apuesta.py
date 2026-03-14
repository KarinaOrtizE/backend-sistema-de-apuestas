import uuid
import enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class EstadoApuesta(enum.Enum):
    GANADA = "ganada"
    PERDIDA = "perdida"
    PENDIENTE = "pendiente"


class Apuesta(Base):
    """Modelo de apuesta"""

    __tablename__ = "apuesta"

    id_apuesta = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_sorteo = Column(
        UUID(as_uuid=True), ForeignKey("sorteo.id_sorteo"), nullable=False
    )

    monto_apostado = Column(Float, nullable=False)
    estado = Column(
        Enum(EstadoApuesta), nullable=False, default=EstadoApuesta.PENDIENTE
    )

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    usuario = relationship("Usuario", foreign_keys=[id_usuario])
    sorteo = relationship("Sorteo", foreign_keys=[id_sorteo])
