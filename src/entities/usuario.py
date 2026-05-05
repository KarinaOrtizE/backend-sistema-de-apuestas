import uuid
from sqlalchemy import Column, String, Boolean, Date
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

    metodos_pago = relationship(
        "MetodoPago",
        back_populates="usuario_dueno",
        cascade="all, delete-orphan",
        foreign_keys="[MetodoPago.id_usuario_dueno]",
    )

    @property
    def nombre_completo(self):
        return self.nombre

    @property
    def nombre_usuario(self):
        return self.username

    def __repr__(self):
        return f"<Usuario(username='{self.username}', rol='{self.rol}', activo={self.activo})>"
