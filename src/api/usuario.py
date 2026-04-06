from typing import List, Optional
from uuid import UUID
from datetime import date

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict, EmailStr

from src.api.deps import get_db
from src.crud import usuario_crud as crud_usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


class UsuarioCreate(BaseModel):
    nombre: str
    username: str
    email: EmailStr
    password: str
    rol: Optional[str] = "usuario"
    fecha_nac: Optional[date] = None


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None
    id_usuario_edita: UUID


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    nombre: str
    username: str
    email: str
    rol: str
    activo: bool


@router.get("", response_model=List[UsuarioRead])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_usuario.listar_todos(db, skip=skip, limit=limit)


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    usuario = crud_usuario.obtener_por_id(db, id_usuario)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    return usuario


@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(body: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        usuario = crud_usuario.crear_usuario(
            db=db,
            nombre=body.nombre,
            username=body.username,
            password=body.password,
            email=str(body.email),
            rol=body.rol,
            fecha_nac=body.fecha_nac,
        )
        return usuario

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(
    id_usuario: UUID, body: UsuarioUpdate, db: Session = Depends(get_db)
):
    data = body.model_dump(exclude_unset=True)

    usuario = crud_usuario.actualizar_usuario(db=db, id_usuario=id_usuario, **data)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    return usuario


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    eliminado = crud_usuario.eliminar(db, id_usuario)

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
