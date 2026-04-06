from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import ruleta_crud as crud_ruleta

router = APIRouter(prefix="/ruletas", tags=["ruletas"])


class RuletaCreate(BaseModel):
    eleccion_usuario: str
    costo_entrada: float
    recompensa: float


class RuletaUpdate(BaseModel):
    eleccion_usuario: Optional[str] = None
    costo_entrada: Optional[float] = None
    recompensa: Optional[float] = None


class RuletaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_ruleta: UUID
    eleccion_usuario: str
    costo_entrada: float
    recompensa: float


@router.get("", response_model=List[RuletaRead])
def listar_ruletas(db: DbSession, skip: int = 0, limit: int = 100) -> List[RuletaRead]:
    return crud_ruleta.listar_todos(db, skip=skip, limit=limit)


@router.get("/{id_ruleta}", response_model=RuletaRead)
def obtener_ruleta(db: DbSession, id_ruleta: UUID) -> RuletaRead:
    r = crud_ruleta.obtener_por_id(db, id_ruleta)
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruleta no encontrada",
        )
    return r


@router.post("", response_model=RuletaRead, status_code=status.HTTP_201_CREATED)
def crear_ruleta(db: DbSession, body: RuletaCreate) -> RuletaRead:
    r = crud_ruleta.crear(
        db,
        eleccion_usuario=body.eleccion_usuario,
        costo_entrada=body.costo_entrada,
        recompensa=body.recompensa,
    )
    return r


@router.put("/{id_ruleta}", response_model=RuletaRead)
def actualizar_ruleta(db: DbSession, id_ruleta: UUID, body: RuletaUpdate) -> RuletaRead:
    data = body.model_dump(exclude_unset=True)
    r = crud_ruleta.actualizar(db, id_ruleta, **data)
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruleta no encontrada",
        )
    return r


@router.delete("/{id_ruleta}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ruleta(db: DbSession, id_ruleta: UUID) -> None:
    if not crud_ruleta.eliminar(db, id_ruleta):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruleta no encontrada",
        )
