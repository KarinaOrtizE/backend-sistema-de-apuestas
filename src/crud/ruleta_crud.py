from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from entities.ruleta import Ruleta


class RuletaCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_ruleta(
        self, eleccion_usuario: str, costo_entrada: float, recompensa: float
    ) -> Ruleta:

        if costo_entrada <= 0:
            raise ValueError("El costo de entrada debe ser mayor que 0")

        if recompensa <= 0:
            raise ValueError("La recompensa debe ser mayor que 0")

        ruleta = Ruleta(
            eleccion_usuario=eleccion_usuario,
            costo_entrada=costo_entrada,
            recompensa=recompensa,
        )

        self.db.add(ruleta)
        self.db.commit()
        self.db.refresh(ruleta)

        return ruleta

    def obtener_ruleta(self, id_ruleta: UUID) -> Optional[Ruleta]:

        return self.db.query(Ruleta).filter(Ruleta.id_ruleta == id_ruleta).first()

    def obtener_ruletas(self, skip: int = 0, limit: int = 100) -> List[Ruleta]:

        return self.db.query(Ruleta).offset(skip).limit(limit).all()

    def actualizar_ruleta(self, id_ruleta: UUID, **kwargs) -> Optional[Ruleta]:

        ruleta = self.obtener_ruleta(id_ruleta)

        if not ruleta:
            return None

        for key, value in kwargs.items():
            if hasattr(ruleta, key):
                setattr(ruleta, key, value)

        self.db.commit()
        self.db.refresh(ruleta)

        return ruleta

    def eliminar_ruleta(self, id_ruleta: UUID) -> bool:

        ruleta = self.obtener_ruleta(id_ruleta)

        if ruleta:
            self.db.delete(ruleta)
            self.db.commit()
            return True

        return False
