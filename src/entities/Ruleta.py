"""Módulo de la clase Ruleta Rápida.

Implementa una ruleta simplificada donde un jugador puede apostar por:
color, paridad o rango. Gestiona apuestas, sorteo, cálculo de premios e historial.

Reglas especiales:
- Si el resultado es 0, el jugador recibe la mitad de su apuesta.
"""

import random
from src.entities.Juego import Juego
from src.entities.Jugador import Jugador


class RuletaRapida(Juego):

    def __init__(self) -> None:
        """Inicializa la ruleta con sus números, colores y estado de juego."""
        super().__init__("Ruleta Rápida", 0, 0)

        self.numeros: list[int] = [
            0,
            32,
            15,
            19,
            4,
            21,
            2,
            25,
            17,
            34,
            6,
            27,
            13,
            36,
            11,
            30,
            8,
            23,
            10,
            5,
            24,
            16,
            33,
            1,
            20,
            14,
            31,
            9,
            22,
            18,
            29,
            7,
            28,
            12,
            35,
            3,
            26,
        ]

        self.rojos: set[int] = {
            1,
            3,
            5,
            7,
            9,
            12,
            14,
            16,
            18,
            19,
            21,
            23,
            25,
            27,
            30,
            32,
            34,
            36,
        }

        self.negros: set[int] = {
            2,
            4,
            6,
            8,
            10,
            11,
            13,
            15,
            17,
            20,
            22,
            24,
            26,
            28,
            29,
            31,
            33,
            35,
        }

        self.apuesta_actual: str | None = None
        self.monto_actual: float = 0
        self.historial: list[dict] = []

    def comprar_boleto(self, jugador: Jugador) -> bool:
        """Permite al jugador seleccionar una apuesta y monto válido.

        Parámetros:
            jugador (Jugador): jugador que realiza la apuesta.

        Retorna:
            bool: True si la apuesta fue registrada, False si no hay saldo.
        """
        while True:
            print("\n--- RULETA RÁPIDA ---")
            print("Saldo actual:", jugador.saldo)
            print("1. Rojo")
            print("2. Negro")
            print("3. Par")
            print("4. Impar")
            print("5. 1-18 (Falta)")
            print("6. 19-36 (Pasa)")

            opcion: str = input("Seleccione su apuesta: ")

            if opcion not in ["1", "2", "3", "4", "5", "6"]:
                print("Opción inválida.")
                continue

            monto_texto: str = input("Ingrese monto a apostar: ")

            es_numero = True
            puntos = 0

            for c in monto_texto:
                if c == ".":
                    puntos += 1
                elif c < "0" or c > "9":
                    es_numero = False

            if not es_numero or puntos > 1 or monto_texto == "":
                print("Monto inválido.")
                continue

            monto: float = float(monto_texto)

            if monto <= 0:
                print("El monto debe ser mayor a 0.")
                continue

            if jugador.saldo < monto:
                print("Saldo insuficiente.")
                return False

            jugador.saldo -= monto
            self.monto_actual = monto

            if opcion == "1":
                self.apuesta_actual = "rojo"
            elif opcion == "2":
                self.apuesta_actual = "negro"
            elif opcion == "3":
                self.apuesta_actual = "par"
            elif opcion == "4":
                self.apuesta_actual = "impar"
            elif opcion == "5":
                self.apuesta_actual = "falta"
            elif opcion == "6":
                self.apuesta_actual = "pasa"

            return True

    def ejecutar_sorteo(self) -> int:
        """Realiza el sorteo de la ruleta.

        Retorna:
            int: número resultante de la ruleta.
        """
        resultado: int = random.choice(self.numeros)

        if resultado == 0:
            color = "Verde"
        elif resultado in self.rojos:
            color = "Rojo"
        else:
            color = "Negro"

        print("\nGirando ruleta...")
        print(f"Resultado: {resultado} - {color}")

        return resultado

    def calcular_premio(self, jugador: Jugador, resultado: int) -> str:
        """Calcula y paga el premio según la apuesta realizada.

        Parámetros:
            jugador (Jugador): jugador que apostó.
            resultado (int): número obtenido en la ruleta.

        Retorna:
            str: mensaje con el resultado de la jugada.
        """
        premio: float = 0
        gano: bool = False

        if resultado == 0:
            premio = self.monto_actual / 2
            gano = True

        else:
            if self.apuesta_actual == "rojo" and resultado in self.rojos:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "negro" and resultado in self.negros:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "par" and resultado % 2 == 0:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "impar" and resultado % 2 != 0:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "falta" and 1 <= resultado <= 18:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "pasa" and 19 <= resultado <= 36:
                premio = self.monto_actual * 2
                gano = True

        if gano:
            jugador.saldo += premio
            mensaje = f"Ganaste {premio}. Nuevo saldo: {jugador.saldo}"
        else:
            mensaje = f"Perdiste. Saldo actual: {jugador.saldo}"

        self.historial.append(
            {
                "apuesta": self.apuesta_actual,
                "resultado": resultado,
                "monto": self.monto_actual,
                "ganancia": premio,
            }
        )

        print(mensaje)
        return mensaje

    def mostrar_historial(self) -> None:
        """Muestra el historial de jugadas realizadas."""
        print("\n===== HISTORIAL =====")

        if len(self.historial) == 0:
            print("No hay jugadas registradas.")
            return

        for i in range(len(self.historial)):
            jugada = self.historial[i]
            print(
                f"Ronda {i+1} -> "
                f"Apuesta: {jugada['apuesta']} | "
                f"Resultado: {jugada['resultado']} | "
                f"Monto: {jugada['monto']} | "
                f"Ganancia: {jugada['ganancia']}"
            )
