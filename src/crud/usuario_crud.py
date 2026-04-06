import hashlib
import uuid
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from src.entities.usuario import Usuario


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def crear_usuario(
    db: Session,
    nombre: str,
    username: str,
    password: str,
    email: str,
    rol: str = "usuario",
    fecha_nac: Optional[date] = None,
    id_usuario_creacion: Optional[uuid.UUID] = None,
) -> Usuario:

    existente = db.query(Usuario).filter(Usuario.username == username.strip()).first()
    if existente:
        raise ValueError("El nombre de usuario ya está registrado")

    nuevo_usuario = Usuario(
        nombre=nombre.strip(),
        username=username.strip(),
        password_hash=_hash_password(password),
        email=email.strip().lower(),
        rol=rol,
        fecha_nac=fecha_nac,
        id_usuario_creacion=id_usuario_creacion,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def login(db: Session, username: str, password: str) -> Optional[Usuario]:
    usuario = db.query(Usuario).filter(Usuario.username == username.strip()).first()

    if not usuario or usuario.activo is False:
        return None
    if usuario.password_hash != _hash_password(password):
        return None

    return usuario


def obtener_por_id(db: Session, id_usuario: uuid.UUID) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def listar_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
    return db.query(Usuario).offset(skip).limit(limit).all()


def hay_usuarios(db: Session) -> bool:

    return db.query(Usuario).first() is not None


def actualizar_usuario(
    db: Session, id_usuario: uuid.UUID, id_usuario_edita: uuid.UUID, **kwargs
) -> Optional[Usuario]:

    usuario = obtener_por_id(db, id_usuario)
    if not usuario:
        return None

    for key, value in kwargs.items():
        if value is not None:

            if key == "password":
                setattr(usuario, "password_hash", _hash_password(value))

            elif key == "username":
                existente = db.query(Usuario).filter(Usuario.username == value).first()
                if existente and existente.id_usuario != id_usuario:
                    raise ValueError("El username ya está en uso")
                setattr(usuario, key, value)

            elif hasattr(usuario, key):
                setattr(usuario, key, value)

    setattr(usuario, "id_usuario_edita", id_usuario_edita)

    try:
        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar: {e}")
        return None


def eliminar(db: Session, id_usuario: uuid.UUID) -> bool:
    usuario = obtener_por_id(db, id_usuario)
    if not usuario:
        return False

    db.delete(usuario)
    db.commit()
    return True
