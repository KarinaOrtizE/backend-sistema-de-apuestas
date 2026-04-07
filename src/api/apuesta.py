from datetime import datetime
from typing import List, Optional
from uuid import UUID
from src.entities.apuesta import EstadoApuesta

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import apuesta_crud as crud_apuesta

router = APIRouter(prefix="/apuestas", tags=["apuestas"])


class ApuestaCreate(BaseModel):
    id_usuario: UUID
    id_sorteo: UUID
    monto_apostado: float
    estado: EstadoApuesta = EstadoApuesta.PENDIENTE
    id_usuario_creacion: UUID


class ApuestaUpdate(BaseModel):
    id_usuario: Optional[UUID] = None
    id_sorteo: Optional[UUID] = None
    monto_apostado: Optional[float] = None
    estado: Optional[EstadoApuesta] = None
    id_usuario_edita: UUID


class ApuestaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_apuesta: UUID
    id_usuario: UUID
    id_sorteo: UUID
    monto_apostado: float
    estado: EstadoApuesta
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[ApuestaRead])
def listar_apuestas(
    db: DbSession, skip: int = 0, limit: int = 100
) -> List[ApuestaRead]:
    return crud_apuesta.listar_todos(db, skip=skip, limit=limit)


@router.get("/{id_apuesta}", response_model=ApuestaRead)
def obtener_apuesta(db: DbSession, id_apuesta: UUID) -> ApuestaRead:
    a = crud_apuesta.obtener_por_id(db, id_apuesta)
    if not a:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Apuesta no encontrada"
        )
    return a


@router.post("", response_model=ApuestaRead, status_code=status.HTTP_201_CREATED)
def crear_apuesta(db: DbSession, body: ApuestaCreate) -> ApuestaRead:
    a = crud_apuesta.crear(
        db,
        id_usuario=body.id_usuario,
        id_sorteo=body.id_sorteo,
        monto_apostado=body.monto_apostado,
        id_usuario_creacion=body.id_usuario_creacion,
    )
    return a


@router.put("/{id_apuesta}", response_model=ApuestaRead)
def actualizar_apuesta(
    db: DbSession, id_apuesta: UUID, body: ApuestaUpdate
) -> ApuestaRead:
    id_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    a = crud_apuesta.actualizar(db, id_apuesta, id_usuario_edita=id_edita, **data)
    if not a:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Apuesta no encontrada"
        )
    return a


@router.delete("/{id_apuesta}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_apuesta(db: DbSession, id_apuesta: UUID) -> None:
    if not crud_apuesta.eliminar(db, id_apuesta):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Apuesta no encontrada"
        )
