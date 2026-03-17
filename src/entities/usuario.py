import uuid
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Usuario(Base):

    __tablename__ = "usuario"

    id_usuario = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
        index=True,
    )

    nombre = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    fecha_nac = Column(Date, nullable=True)

    fecha_creacion = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    id_usuario_creacion = Column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario", ondelete="SET NULL"),
        nullable=True,
    )

    id_usuario_edita = Column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario", ondelete="SET NULL"),
        nullable=True,
    )

    creado_por = relationship(
        "Usuario", foreign_keys=[id_usuario_creacion], remote_side=[id_usuario]
    )
    editado_por = relationship(
        "Usuario", foreign_keys=[id_usuario_edita], remote_side=[id_usuario]
    )

    def __repr__(self):
        return f"<Usuario(username='{self.username}', email='{self.email}')>"
