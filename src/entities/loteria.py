import uuid

from src.database.config import Base
from sqlalchemy import Column, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Loteria(Base):
    __tablename__ = "loteria"

    id_loteria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    numero_jugado = Column(String(4), nullable=False)
    costo_entrada = Column(Numeric(10, 2), nullable=False)
    recompensa = Column(Numeric(10, 2), nullable=False)

    sorteos = relationship("Sorteo", back_populates="loteria")

    def __repr__(self):
        return f"<Loteria(id={self.id_loteria}, numero={self.numero_jugado})>"
