from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import bingo_crud as crud_bingo

router = APIRouter(prefix="/bingos", tags=["bingos"])


class BingoCreate(BaseModel):
    aciertos: int = 0
    costo_entrada: float = 5000.0
    recompensa: float = 250000.0


class BingoUpdate(BaseModel):
    aciertos: Optional[int] = None
    costo_entrada: Optional[float] = None
    recompensa: Optional[float] = None


class BingoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_bingo: UUID
    aciertos: int
    costo_entrada: float
    recompensa: float
    carton_json: list


@router.get("", response_model=List[BingoRead])
def listar_bingos(db: DbSession, skip: int = 0, limit: int = 100) -> List[BingoRead]:
    return crud_bingo.listar_todos(db, skip=skip, limit=limit)


@router.get("/{id_bingo}", response_model=BingoRead)
def obtener_bingo(db: DbSession, id_bingo: UUID) -> BingoRead:
    b = crud_bingo.obtener_por_id(db, id_bingo)
    if not b:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bingo no encontrado"
        )
    return b


@router.post("", response_model=BingoRead, status_code=status.HTTP_201_CREATED)
def crear_bingo(db: DbSession, body: BingoCreate) -> BingoRead:
    b = crud_bingo.crear(
        db,
        aciertos=body.aciertos,
        costo_entrada=body.costo_entrada,
        recompensa=body.recompensa,
    )
    return b


@router.put("/{id_bingo}", response_model=BingoRead)
def actualizar_bingo(db: DbSession, id_bingo: UUID, body: BingoUpdate) -> BingoRead:
    data = body.model_dump(exclude_unset=True)
    b = crud_bingo.actualizar(db, id_bingo, **data)
    if not b:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bingo no encontrado"
        )
    return b


@router.delete("/{id_bingo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_bingo(db: DbSession, id_bingo: UUID) -> None:
    if not crud_bingo.eliminar(db, id_bingo):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bingo no encontrado"
        )
