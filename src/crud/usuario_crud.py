from sqlalchemy.orm import Session
from src.entities.usuario import Usuario
from typing import List, Optional
import uuid


def crear_usuario(
    db: Session,
    nombre: str,
    username: str,
    password_hash: str,
    email: str,
    id_admin: Optional[uuid.UUID] = None,
) -> Usuario:

    nuevo_usuario = Usuario(
        nombre=nombre,
        username=username,
        password_hash=password_hash,
        email=email,
        id_usuario_creacion=id_admin,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def obtener_usuario_por_id(db: Session, id_usuario: uuid.UUID) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def listar_usuarios(db: Session) -> List[Usuario]:
    return db.query(Usuario).all()


def actualizar_usuario(
    db: Session,
    id_usuario: uuid.UUID,
    id_admin: uuid.UUID,
    nombre: Optional[str] = None,
    email: Optional[str] = None,
) -> Optional[Usuario]:

    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if usuario:
        if nombre:
            usuario.nombre = nombre
        if email:
            usuario.email = email

        usuario.id_usuario_edita = id_admin

        db.commit()
        db.refresh(usuario)
    return usuario
