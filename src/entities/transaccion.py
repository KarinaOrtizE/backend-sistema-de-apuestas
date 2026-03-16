import uuid
import enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class TipoTransaccion(enum.Enum):
    DEPOSITO = "deposito"
    RETIRO = "retiro"
    APUESTA = "apuesta"
    PREMIO = "premio"


class Transaccion(Base):
    """Modelo de transacción"""

    __tablename__ = "transaccion"

    id_transaccion = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    tipo = Column(Enum(TipoTransaccion), nullable=False)

    monto = Column(Float, nullable=False)

    fecha = Column(DateTime(timezone=True), server_default=func.now())

    id_billetera = Column(
        UUID(as_uuid=True), ForeignKey("billetera.id_billetera"), nullable=False
    )

    id_metodo_pago = Column(
        UUID(as_uuid=True), ForeignKey("metodo_pago.id_metodo_pago"), nullable=False
    )

    billetera = relationship("Billetera", foreign_keys=[id_billetera])
    metodo_pago = relationship("MetodoPago", foreign_keys=[id_metodo_pago])
