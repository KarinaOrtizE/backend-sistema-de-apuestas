from typing import List, Optional
from uuid import UUID
import json

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import ruleta_crud as crud_ruleta

router = APIRouter(prefix="/ruletas", tags=["ruletas"])


class EleccionRuleta(BaseModel):
    numero: Optional[int] = None
    color: Optional[str] = None
    paridad: Optional[str] = None
    rango: Optional[str] = None


class RuletaCreate(BaseModel):
    eleccion_usuario: EleccionRuleta
    costo_entrada: float
    recompensa: float


class RuletaUpdate(BaseModel):
    eleccion_usuario: Optional[EleccionRuleta] = None
    costo_entrada: Optional[float] = None
    recompensa: Optional[float] = None


class RuletaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_ruleta: UUID
    eleccion_usuario: dict
    costo_entrada: float
    recompensa: float


def parse_ruleta(r):
    r.eleccion_usuario = json.loads(r.eleccion_usuario)
    return r


@router.get("", response_model=List[RuletaRead])
def listar_ruletas(db: DbSession, skip: int = 0, limit: int = 100):
    data = crud_ruleta.listar_todos(db, skip=skip, limit=limit)
    return [parse_ruleta(r) for r in data]


@router.get("/{id_ruleta}", response_model=RuletaRead)
def obtener_ruleta(db: DbSession, id_ruleta: UUID):
    r = crud_ruleta.obtener_por_id(db, id_ruleta)
    if not r:
        raise HTTPException(status_code=404, detail="Ruleta no encontrada")
    return parse_ruleta(r)


@router.post("", response_model=RuletaRead, status_code=status.HTTP_201_CREATED)
def crear_ruleta(db: DbSession, body: RuletaCreate):
    try:
        r = crud_ruleta.crear(
            db,
            eleccion_usuario=body.eleccion_usuario.model_dump(),
            costo_entrada=body.costo_entrada,
            recompensa=body.recompensa,
        )
        return parse_ruleta(r)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id_ruleta}", response_model=RuletaRead)
def actualizar_ruleta(db: DbSession, id_ruleta: UUID, body: RuletaUpdate):
    try:
        data = body.model_dump(exclude_unset=True)

        r = crud_ruleta.actualizar(db, id_ruleta, **data)

        if not r:
            raise HTTPException(status_code=404, detail="Ruleta no encontrada")

        return parse_ruleta(r)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id_ruleta}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ruleta(db: DbSession, id_ruleta: UUID):
    if not crud_ruleta.eliminar(db, id_ruleta):
        raise HTTPException(status_code=404, detail="Ruleta no encontrada")
