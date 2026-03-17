import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class MetodoPago(Base):

    __tablename__ = "metodo_pago"

    id_metodo_pago = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    tipo_metodo = Column(String(50), nullable=False)
    nombre_titular = Column(String(100), nullable=False)

    id_usuario_dueno = Column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario", ondelete="CASCADE"),
        nullable=False,
    )

    fecha_creacion = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )

    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    usuario = relationship(
        "Usuario", foreign_keys=[id_usuario_dueno], back_populates="metodos_pago"
    )

    usuario_creador = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_editor = relationship("Usuario", foreign_keys=[id_usuario_edita])

    def __repr__(self):
        return (
            f"<MetodoPago(tipo='{self.tipo_metodo}', titular='{self.nombre_titular}')>"
        )
