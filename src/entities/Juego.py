"""Módulo de clase abstracta base para todos los juegos de apuestas.

Obliga a las clases hijas a implementar la lógica de comprar_boleto,
ejecutar_sorteo y calcular_premio para asegurar la consistencia.
"""

from abc import ABC, abstractmethod
from .Jugador import Jugador
from typing import Any


class Juego(ABC):

    def __init__(self, nombre: str, costo: float, recompensa: float) -> None:
        """Configura los datos base del juego.

        Args:
            nombre (str): Nombre comercial.
            costo (float): Precio de la entrada.
            recompensa (float): Premio en caso de ganar.
        """
        self.nombre: str = nombre
        self.costo: float = costo
        self.recompensa: float = recompensa

    @abstractmethod
    def comprar_boleto(self, jugador: Jugador) -> bool:
        """Valida fondos antes de permitir la ejecución."""
        pass

    @abstractmethod
    def ejecutar_sorteo(self) -> Any:
        """Crea la lógica de generación de resultados aleatorios."""
        pass

    @abstractmethod
    def calcular_premio(self, jugador: Jugador, resultado: Any) -> str:
        """Compara el resultado con la apuesta y actualiza la billetera."""
        pass
