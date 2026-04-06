from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import loteria_crud as crud_loteria

router = APIRouter(prefix="/loterias", tags=["loterias"])


class LoteriaCreate(BaseModel):
    numero_jugado: str
    costo_entrada: float = 1000.0
    recompensa: float = 100000.0


class LoteriaUpdate(BaseModel):
    numero_jugado: Optional[str] = None
    costo_entrada: Optional[float] = None
    recompensa: Optional[float] = None


class LoteriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_loteria: UUID
    numero_jugado: str
    costo_entrada: float
    recompensa: float
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None


@router.get("", response_model=List[LoteriaRead])
def listar_loterias(
    db: DbSession, skip: int = 0, limit: int = 100
) -> List[LoteriaRead]:
    return crud_loteria.listar_todos(db, skip=skip, limit=limit)


@router.get("/{id_loteria}", response_model=LoteriaRead)
def obtener_loteria(db: DbSession, id_loteria: UUID) -> LoteriaRead:
    l = crud_loteria.obtener_loteria(db, id_loteria)
    if not l:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Loteria no encontrada"
        )
    return l


@router.post("", response_model=LoteriaRead, status_code=status.HTTP_201_CREATED)
def crear_loteria(db: DbSession, body: LoteriaCreate) -> LoteriaRead:
    try:
        l = crud_loteria.crear_loteria(
            db,
            numero_jugado=body.numero_jugado,
            costo_entrada=body.costo_entrada,
            recompensa=body.recompensa,
        )
        return l
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_loteria}", response_model=LoteriaRead)
def actualizar_loteria(
    db: DbSession, id_loteria: UUID, body: LoteriaUpdate
) -> LoteriaRead:
    data = body.model_dump(exclude_unset=True)
    try:
        l = crud_loteria.actualizar_loteria(db, id_loteria, **data)
        if not l:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Loteria no encontrada"
            )
        return l
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_loteria}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_loteria(db: DbSession, id_loteria: UUID) -> None:
    if not crud_loteria.eliminar_loteria(db, id_loteria):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Loteria no encontrada"
        )
