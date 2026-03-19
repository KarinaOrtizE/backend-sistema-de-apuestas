import uuid
from src.database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Billetera(Base):
    __tablename__ = "billetera"

    id_billetera = Column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    saldo = Column(Numeric(precision=10, scale=2), nullable=False, default=0.00)

    id_usuario = Column(
        PgUUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario_creacion = Column(
        PgUUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        PgUUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    usuario = relationship("Usuario", foreign_keys=[id_usuario])
