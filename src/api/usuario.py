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
    nombre_completo: str
    nombre_usuario: str
    email: EmailStr
    clave: str
    rol: str = "admin"
    telefono: Optional[str] = None
    activo: bool = True


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_usuario: UUID
    nombre_completo: str
    nombre_usuario: str
    email: str
    rol: str
    activo: bool


class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    nombre_usuario: Optional[str] = None
    clave: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


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
            nombre=body.nombre_completo,  # mapeo
            username=body.nombre_usuario,  # mapeo
            password=body.clave,  # mapeo
            email=str(body.email),
            rol=body.rol,
        )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(
    id_usuario: UUID, body: UsuarioUpdate, db: Session = Depends(get_db)
):
    data = {}
    if body.nombre_completo is not None:
        data["nombre"] = body.nombre_completo
    if body.nombre_usuario is not None:
        data["username"] = body.nombre_usuario
    if body.clave is not None:
        data["password"] = body.clave
    if body.rol is not None:
        data["rol"] = body.rol
    if body.activo is not None:
        data["activo"] = body.activo

    usuario = crud_usuario.actualizar_usuario(db=db, id_usuario=id_usuario, **data)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    eliminado = crud_usuario.eliminar(db, id_usuario)

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
