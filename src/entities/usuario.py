import uuid
from sqlalchemy import Column, String, Date, DateTime, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    nombre = Column(String(150), nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    fecha_nac = Column(Date, nullable=True)

    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), default="usuario", nullable=False)
    activo = Column(Boolean, default=True)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario_creacion = Column(
        PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
    id_usuario_edita = Column(
        PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    metodos_pago = relationship(
        "MetodoPago", back_populates="usuario_dueno", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Usuario(username='{self.username}', rol='{self.rol}', activo={self.activo})>"
