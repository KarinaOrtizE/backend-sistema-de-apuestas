from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.usuario import Usuario

db = SessionLocal()


def crear(
    nombre: str,
    username: str,
    password_hash: str,
    email: str,
    id_usuario_creacion: Optional[UUID] = None,
) -> Usuario:
    """Crea un usuario."""

    nuevo_usuario = Usuario(
        nombre=nombre,
        username=username,
        password_hash=password_hash,
        email=email,
        id_usuario_creacion=id_usuario_creacion,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


def obtener_por_id(id_usuario: UUID) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def listar_todos() -> List[Usuario]:
    return db.query(Usuario).all()


def actualizar(
    id_usuario: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Usuario]:

    usuario = obtener_por_id(id_usuario)

    if usuario is None:
        print("Error: No se encontró el usuario")
        return None

    for key, value in kwargs.items():
        if hasattr(usuario, key) and value is not None:
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


def eliminar(id_usuario: UUID) -> bool:
    usuario = obtener_por_id(id_usuario)

    if usuario:
        db.delete(usuario)
        db.commit()
        return True

    return False
