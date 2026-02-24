"""Módulo de Bingo (5x5).

Implementa un cartón con una x en el medio por defecto,
y realiza el sorteo de balotas del 1 al 75.
"""

import random
import time
from .Juego import Juego
from .Jugador import Jugador


class Bingo(Juego):

    def __init__(self) -> None:
        super().__init__("Bingo 5x5", 5000, 500000)
        self.multiplicador: float = 100

    def generar_carton(self) -> list[list[int]]:
        """Genera una matriz 5x5.

        Returns:
            list[list[int]]: Una matriz que representa el cartón completo.
        """
        col_b: list[int] = random.sample(range(1, 16), 5)
        col_i: list[int] = random.sample(range(16, 31), 5)
        col_n: list[int] = random.sample(range(31, 46), 5)
        col_g: list[int] = random.sample(range(46, 61), 5)
        col_o: list[int] = random.sample(range(61, 76), 5)

        carton: list = []
        for i in range(5):
            fila: list[int] = [col_b[i], col_i[i], col_n[i], col_g[i], col_o[i]]
            carton.append(fila)

        carton[2][2] = "X"
        return carton

    def mostrar_carton(self, carton: list[list[int]]) -> None:
        """Muestra en consola el cartón de Bingo

        Args:
            carton (list[list[int]]): una matriz 5x5
        """
        print("\n  B    I    N    G    O")
        print("---------------------------")
        for fila in carton:
            print(f"| {' | '.join(str(n).center(3) for n in fila)} |")
        print("---------------------------")

    def ejecutar_sorteo(self) -> list[int]:
        """Extrae 25 balotas al azar del 1 al 75."""
        return random.sample(range(1, 76), 25)
