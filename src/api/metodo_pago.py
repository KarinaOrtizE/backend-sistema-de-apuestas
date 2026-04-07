from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from src.api.deps import get_db
from src.crud import metodo_pago_crud as crud_metodo

router = APIRouter(prefix="/metodos-pago", tags=["metodos_pago"])


class MetodoPagoCreate(BaseModel):
    tipo_metodo: str
    nombre_titular: str
    id_usuario_dueno: UUID


class MetodoPagoUpdate(BaseModel):
    tipo_metodo: Optional[str] = None
    nombre_titular: Optional[str] = None
    id_usuario_edita: UUID


class MetodoPagoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_metodo_pago: UUID
    tipo_metodo: str
    nombre_titular: str
    id_usuario_dueno: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[MetodoPagoRead])
def listar_metodos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_metodo.listar_todos(db, skip=skip, limit=limit)


@router.get("/{id_metodo}", response_model=MetodoPagoRead)
def obtener_metodo(id_metodo: UUID, db: Session = Depends(get_db)):
    metodo = crud_metodo.obtener_por_id(db, id_metodo)

    if not metodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Método de pago no encontrado"
        )

    return metodo


@router.get("/usuario/{id_usuario}", response_model=List[MetodoPagoRead])
def listar_por_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    return crud_metodo.listar_por_usuario(db, id_usuario)


@router.post("", response_model=MetodoPagoRead, status_code=status.HTTP_201_CREATED)
def crear_metodo(body: MetodoPagoCreate, db: Session = Depends(get_db)):
    return crud_metodo.crear_metodo_pago(
        db=db,
        tipo_metodo=body.tipo_metodo,
        nombre_titular=body.nombre_titular,
        id_usuario_dueno=body.id_usuario_dueno,
    )


@router.put("/{id_metodo}", response_model=MetodoPagoRead)
def actualizar_metodo(
    id_metodo: UUID, body: MetodoPagoUpdate, db: Session = Depends(get_db)
):
    data = body.model_dump(exclude_unset=True)

    metodo = crud_metodo.actualizar_metodo_pago(db=db, id_metodo=id_metodo, **data)

    if not metodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Método de pago no encontrado"
        )

    return metodo


@router.delete("/{id_metodo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_metodo(id_metodo: UUID, db: Session = Depends(get_db)):
    eliminado = crud_metodo.eliminar(db, id_metodo)

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Método de pago no encontrado"
        )
