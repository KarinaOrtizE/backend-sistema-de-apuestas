from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from src.api.deps import get_db
from src.crud import sorteo_crud as crud_sorteo

router = APIRouter(prefix="/sorteos", tags=["sorteos"])


class SorteoCreate(BaseModel):
    fecha_sorteo: datetime
    id_bingo: Optional[UUID] = None
    id_ruleta: Optional[UUID] = None
    id_loteria: Optional[UUID] = None


class SorteoUpdate(BaseModel):
    fecha_sorteo: Optional[datetime] = None
    resultado: Optional[dict] = None
    id_bingo: Optional[UUID] = None
    id_ruleta: Optional[UUID] = None
    id_loteria: Optional[UUID] = None


class SorteoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_sorteo: UUID
    fecha_sorteo: datetime
    resultado: Optional[dict] = None
    id_bingo: Optional[UUID] = None
    id_ruleta: Optional[UUID] = None
    id_loteria: Optional[UUID] = None


@router.get("", response_model=List[SorteoRead])
def listar_sorteos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_sorteo.listar_todos(db, skip=skip, limit=limit)


@router.get("/{id_sorteo}", response_model=SorteoRead)
def obtener_sorteo(id_sorteo: UUID, db: Session = Depends(get_db)):
    sorteo = crud_sorteo.obtener_por_id(db, id_sorteo)

    if not sorteo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sorteo no encontrado"
        )

    return sorteo


@router.post("", response_model=SorteoRead, status_code=status.HTTP_201_CREATED)
def crear_sorteo(body: SorteoCreate, db: Session = Depends(get_db)):
    return crud_sorteo.crear_sorteo(
        db=db,
        fecha_sorteo=body.fecha_sorteo,
        id_bingo=body.id_bingo,
        id_ruleta=body.id_ruleta,
        id_loteria=body.id_loteria,
    )


@router.put("/{id_sorteo}", response_model=SorteoRead)
def actualizar_sorteo(
    id_sorteo: UUID, body: SorteoUpdate, db: Session = Depends(get_db)
):
    data = body.model_dump(exclude_unset=True)

    sorteo = crud_sorteo.actualizar(db=db, id_sorteo=id_sorteo, **data)

    if not sorteo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sorteo no encontrado"
        )

    return sorteo


@router.delete("/{id_sorteo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sorteo(id_sorteo: UUID, db: Session = Depends(get_db)):
    eliminado = crud_sorteo.eliminar(db, id_sorteo)

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sorteo no encontrado"
        )
