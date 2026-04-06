from datetime import datetime
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import billetera_crud as crud_billetera

router = APIRouter(prefix="/billeteras", tags=["billeteras"])


class BilleteraCreate(BaseModel):
    id_usuario: UUID
    id_usuario_creacion: Optional[UUID] = None


class BilleteraUpdate(BaseModel):
    id_usuario_edita: UUID


class BilleteraRecarga(BaseModel):
    monto: Decimal = Field(..., gt=0)
    id_usuario_edita: UUID


class BilleteraRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_billetera: UUID
    id_usuario: UUID
    saldo: Decimal
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[BilleteraRead])
def listar_billeteras(
    db: DbSession, skip: int = 0, limit: int = 100
) -> List[BilleteraRead]:
    """Lista todas las billeteras"""
    return crud_billetera.listar(db, skip=skip, limit=limit)


@router.get("/{id_billetera}", response_model=BilleteraRead)
def obtener_billetera(db: DbSession, id_billetera: UUID) -> BilleteraRead:
    """Obtiene una billetera por su ID"""
    b = crud_billetera.obtener(db, id_billetera)
    if not b:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Billetera no encontrada"
        )
    return b


@router.post("", response_model=BilleteraRead, status_code=status.HTTP_201_CREATED)
def crear_billetera(db: DbSession, body: BilleteraCreate) -> BilleteraRead:
    """Crea una nueva billetera para un usuario"""
    try:
        b = crud_billetera.crear(
            db,
            id_usuario=body.id_usuario,
            id_usuario_creacion=body.id_usuario_creacion,
        )
        return b
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{id_billetera}/recargar", response_model=BilleteraRead)
def recargar_saldo(
    db: DbSession, id_billetera: UUID, body: BilleteraRecarga
) -> BilleteraRead:
    try:
        b = crud_billetera.recargar_saldo(
            db,
            billetera_id=id_billetera,
            monto=body.monto,
            id_usuario_operacion=body.id_usuario_edita,
        )
        return b
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{id_billetera}/saldo", response_model=float)
def consultar_saldo(db: DbSession, id_billetera: UUID) -> float:
    """Consulta el saldo actual de una billetera"""
    try:
        saldo = crud_billetera.consultar_saldo(db, id_billetera)
        return saldo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id_billetera}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_billetera(db: DbSession, id_billetera: UUID) -> None:
    """Elimina una billetera (solo si saldo = 0)"""
    try:
        if not crud_billetera.eliminar(db, id_billetera):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Billetera no encontrada"
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
