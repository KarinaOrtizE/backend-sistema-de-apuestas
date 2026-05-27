from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import transaccion_crud as crud_transaccion
from src.entities.transaccion import TipoTransaccion

router = APIRouter(prefix="/transacciones", tags=["transacciones"])


class TransaccionCreate(BaseModel):
    tipo: TipoTransaccion
    monto: float
    id_billetera: UUID
    id_metodo_pago: UUID


class TransaccionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_transaccion: UUID
    tipo: TipoTransaccion
    monto: float
    id_billetera: UUID
    id_metodo_pago: UUID


@router.get("", response_model=List[TransaccionRead])
def listar_transacciones(
    db: DbSession, skip: int = 0, limit: int = 100, usuario_id: Optional[UUID] = None
) -> List[TransaccionRead]:
    if usuario_id is not None:
        return crud_transaccion.listar_por_usuario(db, usuario_id, skip=skip, limit=limit)
    return crud_transaccion.listar_todos(db, skip=skip, limit=limit)


@router.get("/{id_transaccion}", response_model=TransaccionRead)
def obtener_transaccion(db: DbSession, id_transaccion: UUID) -> TransaccionRead:
    t = crud_transaccion.obtener_por_id(db, id_transaccion)
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaccion no encontrada",
        )
    return t


@router.post("", response_model=TransaccionRead, status_code=status.HTTP_201_CREATED)
def crear_transaccion(db: DbSession, body: TransaccionCreate) -> TransaccionRead:
    try:
        t = crud_transaccion.crear(
            db,
            tipo=body.tipo,
            monto=body.monto,
            id_billetera=body.id_billetera,
            id_metodo_pago=body.id_metodo_pago,
        )
        return t
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
