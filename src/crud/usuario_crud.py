import hashlib
import uuid
from typing import List, Optional
from datetime import date
from src.database.config import SessionLocal
from src.entities.usuario import Usuario

db = SessionLocal()


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def crear_usuario(
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


def login(username: str, password: str) -> Optional[Usuario]:
    usuario = db.query(Usuario).filter(Usuario.username == username.strip()).first()

    if not usuario or usuario.activo is False:
        return None
    if usuario.password_hash != _hash_password(password):  # type: ignore
        return None

    return usuario


def obtener_por_id(id_usuario: uuid.UUID) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def listar_todos() -> List[Usuario]:
    return db.query(Usuario).all()


def hay_usuarios() -> bool:

    return db.query(Usuario).first() is not None


def actualizar_usuario(
    id_usuario: uuid.UUID,
    id_usuario_edita: uuid.UUID,
    nombre: Optional[str] = None,
    password: Optional[str] = None,
    rol: Optional[str] = None,
    activo: Optional[bool] = None,
) -> Optional[Usuario]:
    usuario = obtener_por_id(id_usuario)
    if not usuario:
        return None

    if nombre:
        setattr(usuario, "nombre", nombre.strip())
        if password:
            setattr(usuario, "password_hash", _hash_password(password))
        if rol:
            setattr(usuario, "rol", rol.strip())
        if activo is not None:
            setattr(usuario, "activo", activo)

        setattr(usuario, "id_usuario_edita", id_usuario_edita)

    db.commit()
    db.refresh(usuario)
    return usuario


def eliminar(id_usuario: uuid.UUID) -> bool:
    usuario = obtener_por_id(id_usuario)
    if not usuario:
        return False
    db.delete(usuario)
    db.commit()
    return True
