"""Módulo de Bingo (5x5).

Implementa un cartón con espacio libre central y sorteo de balotas del 1 al 75.
"""

import random
import time
from .Juego import Juego
from .Jugador import Jugador


class Bingo:

    def __init__(
        self,
        nombre: str = "Bingo",
        costo: float = 500000,
        recompensa: float = 500000,
        multiplicador: float = 100,
        meta: int = 10,
    ) -> None:
        """Configura los datos base del juego.

        Args:
            nombre (str): Nombre comercial.
            costo (float): Precio de la entrada.
            recompensa (float): Premio en caso de ganar.
        """
        self.nombre: str = nombre
        self.costo: float = costo
        self.recompensa: float = recompensa
        self.multiplicador: float = multiplicador
        self.meta: int = meta

    def comprar_boleto(self, jugador: Jugador) -> bool:
        """Verifica saldo antes de entregar el cartón.

        Args:
            jugador (Jugador)

        Returns:
            bool: El resultado de si se pudo descontar el saldo
        """
        return jugador.billetera.descontar_saldo(self.costo)

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
        """Muestra en consola el cartón de Bingo.

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

    def _marcar_numero(self, carton: list[list[any]], balota: int) -> bool:
        """Busca y marca una balota en el cartón. Retorna True si la encontró."""

        for f in range(5):
            for c in range(5):
                if carton[f][c] == balota:
                    carton[f][c] = "X"
                    return True
        return False

    def calcular_premio(self, jugador: Jugador, balotas: list[int]) -> str:
        """
        Dirige el sorteo, marca el cartón, verifica si el jugador ganó,
        calcula el premio y actualiza la billetera del jugador.

        Args:
            jugador (Jugador)
            balotas (list[int]): números aleatorios que salieron.
        Returns:
            str: Un mensaje que indica si ganó o perdió.
        """

        carton = self.generar_carton()
        self.aciertos: int = 1

        print("\n--- COMENZAMOS ---")
        self.mostrar_carton(carton)

        for i, balota in enumerate(balotas):
            print(f"Balota #{i+1}: [{balota}]")

            if self._marcar_numero(carton, balota):
                self.aciertos += 1
                print("¡ACIERTO!")
                self.mostrar_carton(carton)
                time.sleep(1.0)
            else:
                print("No está")

            if self.aciertos >= self.meta:
                print(f"\n¡META ALCANZADA! Has marcado {self.meta} números.")
                break

        if self.aciertos >= self.meta:
            premio = self.costo * self.multiplicador
            jugador.billetera.sumar_saldo(premio)
            return (
                f"¡FELICIDADES! Alcanzaste los {self.meta} aciertos. Premio: ${premio}."
            )
        return f"Fin del sorteo. Solo lograste {self.aciertos} aciertos. Se requieren {self.meta} para ganar."
